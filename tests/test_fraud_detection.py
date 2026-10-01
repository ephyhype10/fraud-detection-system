import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transaction import Transaction
from fraud_detection import FraudDetector

BASE = datetime(2025, 1, 15, 10, 0, 0)


def make_txn(txn_id, sender, receiver, amount, minutes=0):
    return Transaction(txn_id, sender, receiver, amount, BASE + timedelta(minutes=minutes))


class TestFraudDetector(unittest.TestCase):

    def test_normal_transaction_is_clean(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", "U2", 2000))
        self.assertEqual(t.risk_score, 0)
        self.assertFalse(t.is_flagged())

    def test_blacklisted_sender_is_flagged(self):
        d = FraudDetector()
        d.add_to_blacklist("BAD")
        t = d.process(make_txn("T1", "BAD", "U2", 1000))
        self.assertIn("blacklisted_sender", t.flags)
        self.assertTrue(t.is_flagged())

    def test_high_amount_alone_is_not_flagged(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", "U2", 150000))
        self.assertIn("high_amount", t.flags)
        self.assertFalse(t.is_flagged())   # 25 points, below the 50 threshold

    def test_amount_spike(self):
        d = FraudDetector()
        for i in range(3):
            d.process(make_txn(f"T{i}", "U1", "U2", 1000, minutes=i * 10))
        t = d.process(make_txn("T9", "U1", "U2", 10000, minutes=100))
        self.assertIn("amount_spike", t.flags)

    def test_first_transaction_never_a_spike(self):
        d = FraudDetector()
        t = d.process(make_txn("T1", "U1", "U2", 90000))
        self.assertNotIn("amount_spike", t.flags)

    def test_connected_groups(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", "U2", 1000))
        d.process(make_txn("T2", "U2", "U3", 1000))
        d.process(make_txn("T3", "U5", "U6", 1000))
        groups = d.get_connected_groups()
        self.assertEqual(len(groups), 2)

    def test_money_loop_detected(self):
        d = FraudDetector()
        d.process(make_txn("T1", "A", "B", 1000))
        d.process(make_txn("T2", "B", "C", 1000))
        d.process(make_txn("T3", "C", "A", 1000))
        self.assertTrue(d.has_money_loop())
        self.assertEqual(d.get_money_loop(), ["A", "B", "C", "A"])

    def test_no_money_loop(self):
        d = FraudDetector()
        d.process(make_txn("T1", "X", "Y", 1000))
        d.process(make_txn("T2", "Y", "Z", 1000))
        self.assertFalse(d.has_money_loop())
        self.assertIsNone(d.get_money_loop())

    def test_shortest_chain(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", "U2", 5000))
        d.process(make_txn("T2", "U2", "U3", 4800))
        d.process(make_txn("T3", "U1", "U3", 20000))   # expensive direct route
        path, total = d.find_chain("U1", "U3")
        self.assertEqual(path, ["U1", "U2", "U3"])
        self.assertEqual(total, 9800)

    def test_shortest_chain_no_path(self):
        d = FraudDetector()
        d.process(make_txn("T1", "U1", "U2", 1000))
        path, total = d.find_chain("U1", "U999")
        self.assertIsNone(path)
        self.assertEqual(total, float('inf'))


if __name__ == "__main__":
    unittest.main()