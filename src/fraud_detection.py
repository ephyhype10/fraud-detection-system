from hash_table import HashTable
from avl_tree import AVLTree
from graph import Graph
from bfs import find_all_connected_groups
from cycle_detection import has_cycle, find_cycle_path
from shortest_path import shortest_path


class FraudDetector:
    """
    Central fraud detection engine for a bank transaction graph.
    Users are nodes, transactions are weighted directed edges (sender -> receiver).

    Ties together:
      - HashTable: blacklist + per-user transaction history
      - AVLTree: transactions indexed by amount, for range queries
      - Graph + BFS/DFS/cycle_detection/shortest_path: network-level fraud signals
    """

    WEIGHT_BLACKLIST = 50
    WEIGHT_HIGH_AMOUNT = 25
    WEIGHT_SPIKE = 20

    HIGH_AMOUNT_LIMIT = 100000
    SPIKE_MULTIPLIER = 5

    def __init__(self):
        self.user_history = HashTable(size=101)
        self.blacklist = HashTable(size=101)
        self.amount_tree = AVLTree()
        self.transfer_graph = Graph()

        self.all_transactions = []
        self.flagged_transactions = []

    def add_to_blacklist(self, user_id):
        self.blacklist.insert(user_id, True)

    def process(self, transaction):
        """
        Runs fraud rules on a single transaction, updates its risk_score
        and flags, records it, and adds it as an edge in the transfer graph.
        """
        self._check_blacklist(transaction)
        self._check_high_amount(transaction)
        self._check_amount_spike(transaction)

        # add edge AFTER checks, weight = amount (used by shortest_path later)
        self.transfer_graph.add_edge(transaction.sender, transaction.receiver,
                                      weight=transaction.amount)

        # store into history AFTER checks, so "average" reflects PAST behaviour only
        self.user_history.insert(transaction.sender, transaction)
        self.amount_tree.insert(transaction)
        self.all_transactions.append(transaction)

        if transaction.is_flagged():
            self.flagged_transactions.append(transaction)

        return transaction

    # ---------- individual rules ----------

    def _check_blacklist(self, txn):
        if self.blacklist.contains(txn.sender):
            txn.risk_score += self.WEIGHT_BLACKLIST
            txn.flags.append("blacklisted_sender")

    def _check_high_amount(self, txn):
        if txn.amount >= self.HIGH_AMOUNT_LIMIT:
            txn.risk_score += self.WEIGHT_HIGH_AMOUNT
            txn.flags.append("high_amount")

    def _check_amount_spike(self, txn):
        history = self.user_history.get(txn.sender)
        if not history:
            return

        avg = sum(t.amount for t in history) / len(history)
        if avg > 0 and txn.amount > avg * self.SPIKE_MULTIPLIER:
            txn.risk_score += self.WEIGHT_SPIKE
            txn.flags.append("amount_spike")

    # ---------- graph-based fraud signals (core of the scope) ----------

    def get_flagged(self):
        return self.flagged_transactions

    def get_connected_groups(self):
        """Groups of users who transact among themselves (BFS)."""
        return find_all_connected_groups(self.transfer_graph)

    def has_money_loop(self):
        """True if the transfer graph contains any cycle (DFS-based)."""
        return has_cycle(self.transfer_graph)

    def get_money_loop(self):
        """Returns the actual cycle of users, e.g. ['U003','U004','U005','U003']."""
        return find_cycle_path(self.transfer_graph)

    def find_chain(self, start_user, end_user):
        """Shortest (lowest-amount) chain of transfers from start_user to end_user."""
        return shortest_path(self.transfer_graph, start_user, end_user)


if __name__ == "__main__":
    from transaction import Transaction
    from datetime import datetime, timedelta

    detector = FraudDetector()
    detector.add_to_blacklist("U999")

    base_time = datetime(2025, 1, 15, 10, 0, 0)

    sample_txns = [
        Transaction("T001", "U001", "U002", 5000, base_time),
        Transaction("T002", "U002", "U003", 4800, base_time + timedelta(minutes=5)),
        Transaction("T003", "U003", "U004", 5200, base_time + timedelta(minutes=10)),
        Transaction("T004", "U004", "U005", 3000, base_time + timedelta(minutes=15)),
        Transaction("T005", "U001", "U999", 180000, base_time + timedelta(minutes=20)),
        Transaction("T006", "U999", "U006", 2000, base_time + timedelta(minutes=25)),
        Transaction("T007", "U003", "U004", 8000, base_time + timedelta(minutes=30)),
        Transaction("T008", "U004", "U005", 7900, base_time + timedelta(minutes=35)),
        Transaction("T009", "U005", "U003", 7800, base_time + timedelta(minutes=40)),  # closes a loop
    ]

    for t in sample_txns:
        detector.process(t)
        print(f"{t.txn_id} | {t.sender}->{t.receiver} | amount={t.amount} | "
              f"risk={t.risk_score} | flags={t.flags}")

    print("\n--- Flagged transactions ---")
    for t in detector.get_flagged():
        print(" ", t)

    print("\n--- Connected user groups ---")
    for group in detector.get_connected_groups():
        print(" ", group)

    print("\n--- Money loop check ---")
    print("Has loop?", detector.has_money_loop())
    print("Loop path:", detector.get_money_loop())

    print("\n--- Shortest chain U001 -> U005 ---")
    path, total = detector.find_chain("U001", "U005")
    print("Path:", path, "| Total amount:", total)