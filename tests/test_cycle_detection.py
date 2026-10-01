import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import Graph
from cycle_detection import has_cycle, find_cycle_path


class TestCycleDetection(unittest.TestCase):

    def test_cycle_detected(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        self.assertTrue(has_cycle(g))
        self.assertEqual(find_cycle_path(g), ["A", "B", "C", "A"])

    def test_no_cycle(self):
        g = Graph()
        g.add_edge("X", "Y")
        g.add_edge("Y", "Z")
        self.assertFalse(has_cycle(g))
        self.assertIsNone(find_cycle_path(g))


if __name__ == "__main__":
    unittest.main()