import unittest

from graph import Graph

class TestGraph(unittest.TestCase):

    def test_load_from_filename(self):
        test_graph = Graph.load("graphe.txt")
        self.assertIsInstance(test_graph, Graph)
    
    def test_get_weigth(self):
        test_graph = Graph.load("graphe.txt")
        self.assertEqual(test_graph.get_weight("A","B"), 10)
        self.assertEqual(test_graph.get_weight("H","B"), None)

    def test_get_node_to(self):
        test_graph = Graph.load("graphe.txt")
        self.assertEqual(test_graph.get_node_to("A",10), "B")
        self.assertEqual(test_graph.get_node_to("H",10), None)


if __name__ == "__main__":
    unittest.main()