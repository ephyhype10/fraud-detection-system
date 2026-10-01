import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph
from bfs import bfs, find_all_connected_groups


class TestBFS(unittest.TestCase):

    def test_bfs_order(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        self.assertEqual(bfs(g, "A"), ["A", "B", "C"])

    def test_bfs_unknown_start(self):
        g = Graph()
        self.assertEqual(bfs(g, "ghost"), [])

    def test_connected_groups_ignores_lone_nodes(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("Z")
        groups = find_all_connected_groups(g)
        self.assertEqual(len(groups), 1)


if __name__ == "__main__":
    unittest.main()