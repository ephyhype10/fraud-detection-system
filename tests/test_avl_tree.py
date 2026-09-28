import sys
import os
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transaction import Transaction
from avl_tree import AVLTree


def make_txn(amount, i=0):
    return Transaction(f"T{i}", f"U{i}", amount, "2025-01-15T10:00:00", "City", "D1", "M")


class TestAVLTree(unittest.TestCase):

    def test_inorder_is_sorted(self):
        tree = AVLTree()
        amounts = [5000, 200, 90000, 15000, 500, 120000, 3000]
        for i, a in enumerate(amounts):
            tree.insert(make_txn(a, i))
        result = [t.amount for t in tree.inorder()]
        self.assertEqual(result, sorted(amounts))

    def test_stays_balanced_on_sorted_input(self):
        tree = AVLTree()
        for i in range(1000):
            tree.insert(make_txn(i * 10, i))
        # a plain BST would be height 1000 here; AVL guarantees ~1.44*log2(n)
        self.assertLessEqual(tree.height(), 15)

    def test_stays_balanced_on_random_input(self):
        random.seed(1)
        tree = AVLTree()
        for i in range(1000):
            tree.insert(make_txn(random.randint(1, 100000), i))
        self.assertLessEqual(tree.height(), 15)

    def test_range_query(self):
        tree = AVLTree()
        for i, a in enumerate([100, 500, 1000, 5000, 20000]):
            tree.insert(make_txn(a, i))
        result = [t.amount for t in tree.range_query(500, 5000)]
        self.assertEqual(result, [500, 1000, 5000])   # inclusive on both ends

    def test_range_query_no_results(self):
        tree = AVLTree()
        tree.insert(make_txn(100))
        self.assertEqual(tree.range_query(500, 1000), [])

    def test_duplicate_amounts_are_kept(self):
        tree = AVLTree()
        for i in range(3):
            tree.insert(make_txn(500, i))
        self.assertEqual(len(tree.inorder()), 3)

    def test_empty_tree(self):
        tree = AVLTree()
        self.assertEqual(tree.height(), 0)
        self.assertEqual(tree.inorder(), [])


if __name__ == "__main__":
    unittest.main()