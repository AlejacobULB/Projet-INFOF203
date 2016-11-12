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

    # def test_get_node_to(self):
    #     test_graph = Graph.load("graphe.txt")
    #     self.assertEqual(test_graph.get_node_to("A",10), "B")
    #     self.assertEqual(test_graph.get_node_to("H",10), None)
    
    # def test_depth_first(self):
    #     test_graph =Graph.load("graphe.txt")
    #     self.assertEqual(test_graph.DepthFirst(), [["A","B","H","C","D","E","G","F"],["L","M","N"]])

    def test_detection_cycle(self):
        test_graph = Graph.load("graphe.txt")
        self.assertEqual(test_graph.detection_cycle(),[])
        
if __name__ == "__main__":
    unittest.main()