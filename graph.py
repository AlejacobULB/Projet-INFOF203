from collections import defaultdict

class GraphException(Exception):
    pass


class Graph:
    def __init__(self):
        self._graph = defaultdict(dict)
        self._nodes = set()

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
        return graph

    def add_edge(self, node1, node2, weight):
        self._graph[node1][node2] = {"weight": weight}
        self._nodes.add(node1)
        self._nodes.add(node2)

    def get_weight(self, node1, node2):
        if node1 not in self._graph and node2 not in self._graph[node1]:
            raise GraphException("No edge between {} and {}".format(node1, node2))
        return self._graph[node1][node2]["weight"]
    
    def set_weight(self, node1, node2, weight):
        if node1 not in self._graph and node2 not in self._graph[node1]:
            raise GraphException("No edge between {} and {}".format(node1, node2))
        self._graph[node1][node2]["weight"] = weight

    def _resolve_cycle(self, cycle):
        all_weight = []
        for index, node in enumerate(cycle):
            if index != len(cycle)-1:
                weight = self.get_weight(node, cycle[index+1])
            else:
                weight = self.get_weight(node,cycle[0])
            all_weight.append(weight)
        min_weight = min(all_weight)
        all_weight = [weight - min_weight for weight in all_weight]
        for index, node in enumerate (cycle):
            if index != len(cycle)-1:
                self.set_weight(node, cycle[index+1], all_weight[index])
            else:
                self.set_weight(node, cycle[0], all_weight[index])

    def detected_and_solve_all_cycles(self):
        cycles = self.find_all_cycles()
        for cycle in cycles:
            self._resolve_cycle(cycle)

    def find_all_cycles(self):
        cycle_detected = set()
        for node in self._nodes:
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

    def iter_edges(self):

        for node1, edge in self._graph.items():
            for node2, attr in edge.items():
                yield node1, node2, attr["weight"]

    def find_communities(self):
        undirected_graph = GraphUndirected.from_graph(self)
        return undirected_graph.find_communities()


class GraphUndirected(Graph):
    @classmethod
    def from_graph(cls, directed_graph):
        undirected_graph = cls()
        for node1, node2, weight in directed_graph.iter_edges():
            undirected_graph.add_edge(node1, node2, weight)
        return undirected_graph

    def add_edge(self, node1, node2, weight):
        super().add_edge(node1, node2, weight)
        super().add_edge(node2, node1, weight)

    def find_communities(self):
        communities = set()
        visited = set()
        for node in self._nodes:
            if node in visited:
                continue
            community = frozenset(self._dfs(node))
            visited.update(community)
            communities.add(community)
        return communities

    def _dfs(self, node, visited=None):
        if visited is None:
            visited = set()
        visited.add(node)
        for other in self._graph[node]:
            if other in visited:
                continue
            self._dfs(other, visited)
        return visited