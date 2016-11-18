from graph import Graph
import time

if __name__ == '__main__':
    fileName = "graphe.txt"
    start_time = time.time()
    graph = Graph.load(fileName)
    print(graph.find_all_cycles())
    print(graph.find_highest_friend_group())
    print("--- %s seconds ---" % (time.time() - start_time))
