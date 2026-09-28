import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph


class TestGraph(unittest.TestCase):

    def test_bfs_finds_connected_cluster(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("D", "E")
        self.assertEqual(sorted(g.bfs_cluster("A")), ["A", "B", "C"])

    def test_bfs_unknown_user(self):
        g = Graph()
        self.assertEqual(g.bfs_cluster("ghost"), [])

    def test_find_all_clusters_ignores_lone_nodes(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("C", "D")
        g.add_node("Z")   # isolated
        clusters = g.find_all_clusters()
        self.assertEqual(len(clusters), 2)

    def test_cycle_detected(self):
        g = Graph()
        g.add_edge("A", "B", directed=True)
        g.add_edge("B", "C", directed=True)
        g.add_edge("C", "A", directed=True)
        self.assertTrue(g.has_cycle_directed())

    def test_no_cycle_in_chain(self):
        g = Graph()
        g.add_edge("X", "Y", directed=True)
        g.add_edge("Y", "Z", directed=True)
        self.assertFalse(g.has_cycle_directed())

    def test_adjacency_matrix_undirected(self):
        g = Graph()
        g.add_edge("A", "B")
        self.assertEqual(g.get_adjacency_matrix(), [[0, 1], [1, 0]])

    def test_adjacency_matrix_directed(self):
        g = Graph()
        g.add_edge("A", "B", directed=True)
        self.assertEqual(g.get_adjacency_matrix(), [[0, 1], [0, 0]])


if __name__ == "__main__":
    unittest.main()