from graph import Graph
if __name__ == '__main__':
	fileName = "graphe.txt"
	graph = Graph.load(fileName)
	import pdb;pdb.set_trace()
	print(graph.detection_cycle())
