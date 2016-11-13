from collections import defaultdict

class GraphException(Exception):
    pass


class Graph:
    def __init__(self):
        self._graph = defaultdict(dict)
        self._node_list = set()

    @classmethod
    def load(cls, fileName):
        graph = cls()
        with open(fileName,"r") as file:
            graphData = file.read()
        for i, line in enumerate(graphData.splitlines()):
            if i == 0:
                #skip first line
                continue
            node1, node2, weight = line.split(" ")
            weight = int(weight)
            graph.add_edge(node1, node2, weight)
            graph._node_list.add(node1)
            graph._node_list.add(node2)
       
        return graph

    def add_edge(self, node1, node2, weight):
        self._graph[node1][node2] = {"weight": weight}
      
    def get_weight(self, node1, node2):
        if node1 not in self._graph and node2 not in self._graph[node1]:
            raise GraphException("No edge between {} and {}".format(node1, node2))
        return self._graph[node1][node2]["weight"]

    def DepthFirst(self):
        vertexTag = dict()
        parcours = []
        for v in self._node_list:
            vertexTag[v] = 'white'
        for i in range(len(self._node_list)):
            if vertexTag[self._node_list[i]] != "black":
                parcours.append(self.dfs(self._node_list[i], vertexTag))
                print(vertexTag) 
        return parcours

    def dfs(self, s, vertexTag):
        traversing = [s]
        vertexTag[s] = 'grey'
        stack = [s]
        while stack:
            u = stack[-1]
            if s not in self._graph:
                stack.pop()
                vertexTag[u] = "black"
                continue
            vertexSuccessor = [successor.node for successor in self._graph[u] if vertexTag[successor.node] == 'white']
            if vertexSuccessor:
                successor = vertexSuccessor[0]
                vertexTag[successor] = 'grey'
                traversing.append(successor)
                stack.append(successor)
            else:
                stack.pop()
                vertexTag[u] = 'black'
        return traversing

    def find_all_cycles(self):
        cycle_detected = set()
        for node in self._node_list:
            self._visit(node, cycle_detected)
        return cycle_detected

    def _visit(self, node, cycle_detected, visited=list()):
        if node in visited:
            # Cycle trouvé
            # On veut l'ajouter en partant du node avec la plus petite valeur
            index = visited.index(node)  
            cycle = visited[index:]
            min_node = min(cycle)
            min_index = cycle.index(min_node)
            cycle = cycle[min_index:] + cycle[:min_index]
            cycle_detected.add(tuple(cycle))
        else:
            visited.append(node)
            connected_nodes = self._graph[node]
            for connected_node in connected_nodes:
                self._visit(connected_node, cycle_detected, visited)
            visited.pop()