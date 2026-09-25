import heapq


class RiskHeap:
    """
    Max-heap of transactions by risk_score, used to efficiently retrieve
    the top-K riskiest transactions without sorting the entire list.

    Python's heapq is a min-heap, so we store (-risk_score, tie_breaker, transaction)
    to simulate a max-heap.
    """

    def __init__(self):
        self.heap = []
        self._counter = 0   # tie-breaker so heapq never tries to compare Transaction objects directly

    def push(self, transaction):
        self._counter += 1
        # negative risk_score -> highest risk ends up smallest -> sits at heap root
        heapq.heappush(self.heap, (-transaction.risk_score, self._counter, transaction))

    def pop_highest(self):
        """Remove and return the single highest-risk transaction."""
        if not self.heap:
            return None
        neg_score, _, transaction = heapq.heappop(self.heap)
        return transaction

    def top_k(self, k):
        """
        Return the top K riskiest transactions WITHOUT permanently modifying the heap.
        Uses heapq.nsmallest on our negated scores, which is O(n log k) - efficient
        for small k even on a large heap.
        """
        top = heapq.nsmallest(k, self.heap)
        return [item[2] for item in top]

    def __len__(self):
        return len(self.heap)


if __name__ == "__main__":
    from transaction import Transaction

    txns_data = [
        ("T001", "U001", 5000, 20),
        ("T002", "U002", 15000, 70),
        ("T003", "U001", 200, 10),
        ("T004", "U003", 90000, 95),
        ("T005", "U004", 3000, 55),
    ]

    risk_heap = RiskHeap()

    for txn_id, user_id, amount, risk in txns_data:
        t = Transaction(txn_id, user_id, amount, "2025-01-15T10:00:00", "City", "D01", "Merchant")
        t.risk_score = risk
        risk_heap.push(t)

    print("Heap size:", len(risk_heap))

    print("\nTop 3 riskiest transactions:")
    for t in risk_heap.top_k(3):
        print(" ", t.txn_id, "risk:", t.risk_score)

    print("\nPopping highest one at a time:")
    while len(risk_heap) > 0:
        t = risk_heap.pop_highest()
        print(" ", t.txn_id, "risk:", t.risk_score)