from graph import Graph

if __name__ == '__main__':
    fileName = "graphe.txt"
    graph = Graph.load(fileName)
    print(graph.find_highest_friend_group())
