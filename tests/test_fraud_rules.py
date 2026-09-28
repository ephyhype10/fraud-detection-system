import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transaction import Transaction
from fraud_rules import FraudDetector

BASE = datetime(2025, 1, 15, 10, 0, 0)


def make_txn(txn_id, user, amount, minutes=0, location="Chennai", device="D1"):
    return Transaction(txn_id, user, amount, BASE + timedelta(minutes=minutes),
                       location, device, "Merchant")


class TestFraudDetector(unittest.TestCase):

    def test_normal_transaction_is_clean(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", 2000))
        self.assertEqual(t.risk_score, 0)
        self.assertEqual(t.flags, [])
        self.assertFalse(t.is_flagged())

    def test_blacklisted_user_is_flagged(self):
        d = FraudDetector()
        d.add_to_blacklist("BAD")
        t = d.process(make_txn("T1", "BAD", 1000))
        self.assertIn("blacklisted_user", t.flags)
        self.assertTrue(t.is_flagged())

    def test_high_amount_alone_is_not_flagged(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", 150000))
        self.assertIn("high_amount", t.flags)
        self.assertEqual(t.risk_score, 25)       # below the flag threshold of 50
        self.assertFalse(t.is_flagged())

    def test_amount_spike(self):
        d = FraudDetector()
        # three normal txns, an hour apart (so velocity doesn't fire)
        for i in range(3):
            d.process(make_txn(f"T{i}", "U1", 1000, minutes=i * 60))
        t = d.process(make_txn("T9", "U1", 10000, minutes=200))
        self.assertIn("amount_spike", t.flags)

    def test_first_transaction_never_a_spike(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", 90000))
        self.assertNotIn("amount_spike", t.flags)

    def test_velocity(self):
        d = FraudDetector()
        results = [d.process(make_txn(f"T{i}", "U1", 1000, minutes=i)) for i in range(4)]
        self.assertNotIn("high_velocity", results[2].flags)   # 3rd is at the limit
        self.assertIn("high_velocity", results[3].flags)      # 4th exceeds it

    def test_location_jump(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", 1000, minutes=0, location="Chennai"))
        t = d.process(make_txn("T2", "U1", 1000, minutes=2, location="Mumbai"))
        self.assertIn("location_jump", t.flags)

    def test_location_change_with_long_gap_is_fine(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", 1000, minutes=0, location="Chennai"))
        t = d.process(make_txn("T2", "U1", 1000, minutes=120, location="Mumbai"))
        self.assertNotIn("location_jump", t.flags)

    def test_shared_device_forms_ring(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", 1000, device="SHARED"))
        d.process(make_txn("T2", "U2", 1000, device="SHARED"))
        d.process(make_txn("T3", "U3", 1000, device="OWN"))
        rings = d.get_fraud_rings()
        together = [c for c in rings if "U1" in c and "U2" in c]
        self.assertEqual(len(together), 1)
        self.assertNotIn("U3", together[0])


if __name__ == "__main__":
    unittest.main()