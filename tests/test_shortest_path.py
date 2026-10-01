import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph
from shortest_path import shortest_path


class TestShortestPath(unittest.TestCase):

    def test_picks_cheaper_indirect_route(self):
        g = Graph()
        g.add_edge("A", "B", weight=5000)
        g.add_edge("B", "C", weight=4800)
        g.add_edge("A", "C", weight=20000)
        path, total = shortest_path(g, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(total, 9800)

    def test_no_path_exists(self):
        g = Graph()
        g.add_edge("A", "B", weight=1000)
        path, total = shortest_path(g, "A", "ghost")
        self.assertIsNone(path)
        self.assertEqual(total, float('inf'))


if __name__ == "__main__":
    unittest.main()