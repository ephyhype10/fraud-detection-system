import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph


class TestGraph(unittest.TestCase):

    def test_add_edge_creates_nodes(self):
        g = Graph()
        g.add_edge("A", "B")
        self.assertIn("A", g.nodes)
        self.assertIn("B", g.nodes)

    def test_neighbors(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        self.assertEqual(g.neighbors("A"), {"B", "C"})

    def test_weight_stored(self):
        g = Graph()
        g.add_edge("A", "B", weight=5000)
        self.assertEqual(g.get_weight("A", "B"), 5000)

    def test_weight_none_if_not_set(self):
        g = Graph()
        g.add_edge("A", "B")
        self.assertIsNone(g.get_weight("A", "B"))

    def test_adjacency_matrix_directed(self):
        g = Graph()
        g.add_edge("A", "B")
        self.assertEqual(g.get_adjacency_matrix(), [[0, 1], [0, 0]])


if __name__ == "__main__":
    unittest.main()