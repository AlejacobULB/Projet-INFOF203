import unittest

from graph import Graph, GraphException, GraphUndirected

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.test_graph = Graph.load("graphe.txt")

    def test_load_from_filename(self):
        self.assertIsInstance(self.test_graph, Graph)
    
    def test_get_weigth(self):
        self.assertEqual(self.test_graph.get_weight("A","B"), 10)
        with self.assertRaises(GraphException) as cm:
            self.test_graph.get_weight("H","B")
        self.assertEqual(str(cm.exception), "No edge between H and B")
    
    def test_find_communities(self):
        self.assertEqual(self.test_graph.find_communities(), 
                        {frozenset(("A","B","H","C","D","E","G","F")), 
                         frozenset(("L","M","N"))})

    def test_find_all_cycles(self):
        self.assertEqual(self.test_graph.find_all_cycles(), {("A", "C", "B"),
                          ("A", "B"),
                          ("D", "E", "F"),
                          ("E", "G")})

    def test_iter_edges(self):
        self.assertEqual(set(self.test_graph.iter_edges()),
                        {
                        ("A", "B", 10),
                        ("A", "C", 50),
                        ("B", "A", 20),
                        ("B", "H", 40),
                        ("C", "B", 30),
                        ("C", "D", 40),
                        ("D", "E", 15),
                        ("E", "F", 25),
                        ("E", "G", 20),
                        ("F", "D", 50),
                        ("G", "E", 30),
                        ("L", "M", 20),
                        ("L", "N", 60),
                        ("M", "N", 10)
                        }
                    )   


class TestGraphUndirected(unittest.TestCase):

    def test_create_from_directed_graph(self):
        test_graph = Graph.load("graphe.txt")
        test_graph_undirected = GraphUndirected.from_graph(test_graph)
        self.assertEqual(test_graph_undirected.get_weight("D", "F"), 50)

    def test_add_edge(self):
        test_graph = GraphUndirected()
        test_graph.add_edge("A", "B", 10)
        self.assertEqual(test_graph.get_weight("B", "A"), 10)
        self.assertEqual(test_graph.get_weight("A", "B"), 10)
        
if __name__ == "__main__":
    unittest.main()