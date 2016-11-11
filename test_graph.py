import unittest

from graph import Graph

class TestGraphLoad(unittest.TestCase):

	def test_load_from_filename(self):
		test_graph = Graph.load("graphe.txt")
		self.assertIsInstance(test_graph, Graph)


if __name__ == "__main__":
	unittest.main()