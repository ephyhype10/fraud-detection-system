import sys
import os
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transaction import Transaction
from avl_tree import AVLTree
from hash_table import HashTable
from sorting_search import merge_sort, binary_search_by_amount, linear_search_by_amount

class PlainBSTNode:
    def __init__(self, transaction):
        self.transaction = transaction
        self.amount = transaction.amount
        self.left = None
        self.right = None


class PlainBST:
    """Ordinary BST, no self-balancing - used ONLY to demonstrate why AVL is needed."""

    def __init__(self):
        self.root = None

    def insert(self, transaction):
        new_node = PlainBSTNode(transaction)

        if not self.root:
            self.root = new_node
            return

        current = self.root
        while True:
            if transaction.amount < current.amount:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def height(self):
        """Iterative height calculation using level-order traversal (BFS-style)."""
        if not self.root:
             return 0

        max_depth = 0
        stack = [(self.root, 1)]   # (node, depth at this node)

        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)

            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))

        return max_depth

def generate_random_transactions(n):
    """Creates n Transaction objects with random amounts, for benchmarking."""
    transactions = []
    for i in range(n):
        amount = random.randint(100, 500000)
        t = Transaction(
            txn_id=f"T{i}",
            user_id=f"U{i % 1000}",       # 1000 distinct users, reused
            amount=amount,
            timestamp="2025-01-15T10:00:00",
            location="City",
            device_id=f"D{i % 500}",
            merchant="Merchant",
        )
        transactions.append(t)
    return transactions


def generate_sorted_transactions(n):
    """Creates n Transaction objects with STRICTLY INCREASING amounts -
    the worst case for a plain BST."""
    transactions = []
    for i in range(n):
        t = Transaction(
            txn_id=f"T{i}",
            user_id=f"U{i}",
            amount=i * 10,          # 0, 10, 20, 30... always increasing
            timestamp="2025-01-15T10:00:00",
            location="City",
            device_id=f"D{i}",
            merchant="Merchant",
        )
        transactions.append(t)
    return transactions


# ---------- Benchmark 1: Linear vs Binary Search ----------

def benchmark_search(n=10000):
    print(f"\n{'='*60}")
    print(f"BENCHMARK 1: Linear vs Binary Search (n={n})")
    print(f"{'='*60}")

    transactions = generate_random_transactions(n)
    sorted_txns = merge_sort(transactions, key=lambda t: t.amount)

    target = sorted_txns[n // 2].amount   # pick a real amount that exists, from the middle

    start = time.perf_counter()
    linear_search_by_amount(sorted_txns, target)
    linear_time = time.perf_counter() - start

    start = time.perf_counter()
    binary_search_by_amount(sorted_txns, target)
    binary_time = time.perf_counter() - start

    print(f"Linear search time:  {linear_time*1000:.4f} ms")
    print(f"Binary search time:  {binary_time*1000:.4f} ms")
    print(f"Binary search was {linear_time / binary_time:.1f}x faster")


# ---------- Benchmark 2: AVL vs Plain BST ----------

def benchmark_tree_height(n=2000):
    print(f"\n{'='*60}")
    print(f"BENCHMARK 2: AVL Tree vs Plain BST (n={n}, SORTED input)")
    print(f"{'='*60}")

    sorted_txns = generate_sorted_transactions(n)

    avl = AVLTree()
    start = time.perf_counter()
    for t in sorted_txns:
        avl.insert(t)
    avl_time = time.perf_counter() - start

    bst = PlainBST()
    start = time.perf_counter()
    for t in sorted_txns:
        bst.insert(t)
    bst_time = time.perf_counter() - start

    print(f"AVL tree  -> height: {avl.height()}, insert time: {avl_time*1000:.2f} ms")
    print(f"Plain BST -> height: {bst.height()}, insert time: {bst_time*1000:.2f} ms")
    print(f"(For n={n} sorted inserts, a balanced tree's ideal height is ~{n.bit_length()})")


# ---------- Benchmark 3: Hash Table Collisions ----------

def benchmark_hash_collisions(n=1000):
    print(f"\n{'='*60}")
    print(f"BENCHMARK 3: Hash Table Collisions at Different Sizes (n={n} keys)")
    print(f"{'='*60}")

    for size in [11, 101, 1009]:
        ht = HashTable(size=size)
        for i in range(n):
            ht.insert(f"U{i}", f"txn_{i}")

        print(f"Table size={size:5d} -> collisions: {ht.collision_count:4d}, "
              f"load factor: {ht.load_factor():.2f}")


if __name__ == "__main__":
    random.seed(42)   # reproducible results across runs

    benchmark_search(n=10000)
    benchmark_tree_height(n=2000)
    benchmark_hash_collisions(n=1000)