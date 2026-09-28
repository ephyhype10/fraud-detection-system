import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from hash_table import HashTable


class TestHashTable(unittest.TestCase):

    def test_insert_and_get(self):
        ht = HashTable(size=10)
        ht.insert("U001", "T1")
        self.assertEqual(ht.get("U001"), ["T1"])

    def test_same_key_appends_to_list(self):
        ht = HashTable(size=10)
        ht.insert("U001", "T1")
        ht.insert("U001", "T2")
        self.assertEqual(ht.get("U001"), ["T1", "T2"])

    def test_missing_key_returns_empty_list(self):
        ht = HashTable(size=10)
        self.assertEqual(ht.get("nobody"), [])

    def test_contains(self):
        ht = HashTable(size=10)
        ht.insert("U001", "T1")
        self.assertTrue(ht.contains("U001"))
        self.assertFalse(ht.contains("U002"))

    def test_delete(self):
        ht = HashTable(size=10)
        ht.insert("U001", "T1")
        self.assertTrue(ht.delete("U001"))
        self.assertEqual(ht.get("U001"), [])
        self.assertFalse(ht.delete("U001"))   # already gone

    def test_collisions_still_retrievable(self):
        # size=1 forces every key into the same bucket
        ht = HashTable(size=1)
        ht.insert("A", 1)
        ht.insert("B", 2)
        ht.insert("C", 3)
        self.assertEqual(ht.collision_count, 2)
        self.assertEqual(ht.get("A"), [1])
        self.assertEqual(ht.get("B"), [2])
        self.assertEqual(ht.get("C"), [3])

    def test_load_factor(self):
        ht = HashTable(size=10)
        for i in range(5):
            ht.insert(f"U{i}", i)
        self.assertEqual(ht.load_factor(), 0.5)


if __name__ == "__main__":
    unittest.main()