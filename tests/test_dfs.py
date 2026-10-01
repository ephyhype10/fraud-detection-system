import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph
from dfs import dfs


class TestDFS(unittest.TestCase):

    def test_dfs_reaches_all_connected(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        result = dfs(g, "A")
        self.assertEqual(set(result), {"A", "B", "C"})

    def test_dfs_unknown_start(self):
        g = Graph()
        self.assertEqual(dfs(g, "ghost"), [])


if __name__ == "__main__":
    unittest.main()