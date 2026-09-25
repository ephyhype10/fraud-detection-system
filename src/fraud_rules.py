from hash_table import HashTable
from velocity_check import VelocityChecker
from graph import Graph


class FraudDetector:
    """
    Central fraud detection engine. Ties together:
      - HashTable: user transaction history + blacklist
      - VelocityChecker: rapid-fire transaction detection
      - Graph: shared-device / money-transfer relationships

    Runs a set of weighted rules on each transaction and computes a risk_score.
    """

    # rule weights - tune these based on how serious each signal is
    WEIGHT_BLACKLIST = 50
    WEIGHT_HIGH_AMOUNT = 25
    WEIGHT_SPIKE = 20
    WEIGHT_VELOCITY = 30
    WEIGHT_LOCATION_JUMP = 15

    FLAG_THRESHOLD = 50
    HIGH_AMOUNT_LIMIT = 100000       # flat threshold, e.g. ₹1,00,000
    SPIKE_MULTIPLIER = 5             # amount > 5x user's average = spike

    def __init__(self):
        self.user_history = HashTable(size=101)
        self.blacklist = HashTable(size=101)
        self.velocity_checker = VelocityChecker(limit=3, window_seconds=300)
        self.device_graph = Graph()
        self.transfer_graph = Graph()

        self.all_transactions = []
        self.flagged_transactions = []

    def add_to_blacklist(self, user_id):
        self.blacklist.insert(user_id, True)

    def process(self, transaction):
        """
        Runs all fraud rules on a single transaction, updates its risk_score
        and flags, records it, and links it into the graphs.
        Returns the same transaction object (now scored).
        """
        self._check_blacklist(transaction)
        self._check_high_amount(transaction)
        self._check_amount_spike(transaction)
        self._check_velocity(transaction)
        self._check_location_jump(transaction)

        # record into graphs for later ring/cycle detection
        self.device_graph.add_edge(transaction.user_id, transaction.device_id, directed=False)

        # store into history AFTER checks, so "average" reflects PAST behaviour, not this txn
        self.user_history.insert(transaction.user_id, transaction)
        self.all_transactions.append(transaction)

        if transaction.is_flagged():
            self.flagged_transactions.append(transaction)

        return transaction

    # ---------- individual rules ----------

    def _check_blacklist(self, txn):
        if self.blacklist.contains(txn.user_id):
            txn.risk_score += self.WEIGHT_BLACKLIST
            txn.flags.append("blacklisted_user")

    def _check_high_amount(self, txn):
        if txn.amount >= self.HIGH_AMOUNT_LIMIT:
            txn.risk_score += self.WEIGHT_HIGH_AMOUNT
            txn.flags.append("high_amount")

    def _check_amount_spike(self, txn):
        history = self.user_history.get(txn.user_id)   # past transactions only
        if not history:
            return   # no history yet, nothing to compare against

        avg = sum(t.amount for t in history) / len(history)
        if avg > 0 and txn.amount > avg * self.SPIKE_MULTIPLIER:
            txn.risk_score += self.WEIGHT_SPIKE
            txn.flags.append("amount_spike")

    def _check_velocity(self, txn):
        if self.velocity_checker.check(txn.user_id, txn.timestamp):
            txn.risk_score += self.WEIGHT_VELOCITY
            txn.flags.append("high_velocity")

    def _check_location_jump(self, txn):
        history = self.user_history.get(txn.user_id)
        if not history:
            return

        last_txn = history[-1]   # most recent past transaction
        if last_txn.location != txn.location:
            time_gap = (txn.timestamp - last_txn.timestamp).total_seconds()
            if time_gap < 600:   # different city within 10 minutes = suspicious
                txn.risk_score += self.WEIGHT_LOCATION_JUMP
                txn.flags.append("location_jump")

    # ---------- reporting helpers ----------

    def get_flagged(self):
        return self.flagged_transactions

    def get_fraud_rings(self):
        return self.device_graph.find_all_clusters()


if __name__ == "__main__":
    from transaction import Transaction
    from datetime import datetime, timedelta

    detector = FraudDetector()
    detector.add_to_blacklist("U999")

    base_time = datetime(2025, 1, 15, 10, 0, 0)

    sample_txns = [
        Transaction("T001", "U001", 5000, base_time, "Chennai", "D01", "Amazon"),
        Transaction("T002", "U001", 4800, base_time + timedelta(minutes=1), "Chennai", "D01", "Swiggy"),
        Transaction("T003", "U001", 4900, base_time + timedelta(minutes=2), "Chennai", "D01", "Zomato"),
        Transaction("T004", "U001", 4700, base_time + timedelta(minutes=3), "Chennai", "D01", "BigBasket"),
        Transaction("T005", "U001", 150000, base_time + timedelta(minutes=5), "Mumbai", "D02", "Croma"),
        Transaction("T006", "U999", 2000, base_time, "Delhi", "D03", "Flipkart"),
        Transaction("T007", "U002", 3000, base_time, "Bangalore", "D04", "Amazon"),
        Transaction("T008", "U002", 3200, base_time, "Bangalore", "D01", "Myntra"),  # shares device with U001!
    ]

    for t in sample_txns:
        detector.process(t)
        print(f"{t.txn_id} | user={t.user_id} | amount={t.amount} | "
              f"risk={t.risk_score} | flags={t.flags}")

    print("\n--- Flagged transactions ---")
    for t in detector.get_flagged():
        print(" ", t)

    print("\n--- Suspicious device-sharing clusters ---")
    for cluster in detector.get_fraud_rings():
        print(" ", cluster)