#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from copy import deepcopy


class GraphException(Exception):
    pass

class Graph():

    def __init__(self):
        self._graph = defaultdict(dict)
        self._nodes = set()

    def __eq__(self, other):
        return self._graph == other._graph

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

    def __str__(self):
        output = ""
        for node in self._graph:
            for successor in self._graph[node]:
                weight = self.get_weight(node, successor)
                output += ("{} {} {} \n".format(node, successor, weight))
        return output


class DirectedGraph(Graph):

    @classmethod
    def load(cls, fileName):
        graph = cls()
        with open(fileName, "r") as file:
            graphData = file.read()
        for i, line in enumerate(graphData.splitlines()):
            if i == 0:
                # skip first line
                continue
            node1, node2, weight = line.split(" ")
            weight = int(weight)
            graph.add_edge(node1, node2, weight)
        return graph

    def _resolve_cycle(self, cycle):
        all_weight = []
        for index, node in enumerate(cycle):
            if index != len(cycle) - 1:
                weight = self.get_weight(node, cycle[index + 1])
            else:
                weight = self.get_weight(node, cycle[0])
            all_weight.append(weight)
        min_weight = min(all_weight)
        all_weight = [weight - min_weight for weight in all_weight]
        for index, node in enumerate(cycle):
            if index != len(cycle) - 1:
                self.set_weight(node, cycle[index + 1], all_weight[index])
            else:
                self.set_weight(node, cycle[0], all_weight[index])

    def detected_and_solve_all_cycles(self):
        cycles = sorted(self.find_all_cycles(), key=len)
        for cycle in cycles:
            self._resolve_cycle(cycle)

    def find_all_cycles(self):
        def visit(node, visited=list()):
            if node in visited:
                # Cycle trouvé
                # On veut l'ajouter en partant du node avec la plus petite valeur
                index = visited.index(node)
                cycle = visited[index:]
                cycle = self._normalize(cycle)
                cycle_detected.add(tuple(cycle))
            else:
                visited.append(node)
                connected_nodes = self._graph[node]
                for connected_node in connected_nodes:
                    visit(connected_node, visited)
                visited.pop()

        cycle_detected = set()
        for node in self._nodes:
            visit(node)
        return cycle_detected

    def _normalize(self, nodes):
        """
        Re-arrange the sequence of nodes starting by the smallest.

        This allows for easy comparison between ordered sequences of nodes

        :param nodes: sequence of nodes
        :return: normalized sequence of nodes
        """
        min_node = min(nodes)
        min_index = nodes.index(min_node)
        nodes = nodes[min_index:] + nodes[:min_index]
        return nodes

    def iter_edges(self):

        for node1, edge in self._graph.items():
            for node2, attr in edge.items():
                yield node1, node2, attr["weight"]

    def find_communities(self):
        undirected_graph = GraphUndirected.from_graph(self)
        return undirected_graph.find_communities()

    def find_social_hub(self, k):
        undirected_graph = GraphUndirected.from_graph(self)
        return undirected_graph.find_social_hub(k)

    def find_highest_friend_group(self):
        undirected_graph = GraphUndirected.from_graph(self)
        friend_group = undirected_graph.find_highest_friend_group()
        return friend_group


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

    def find_social_hub(self, k):
        articulation_points = self._find_articulation_points()
        social_hub = set()
        for articulation_point in articulation_points:
            count = 0
            subgraph = self.find_subgraph(articulation_point)
            subgraph.remove(articulation_point)
            communities = subgraph.find_communities()
            for community in communities:
                if len(community) >= k:
                    count += 1
            if count == 2:
                social_hub.add(articulation_point)
        return social_hub

    def remove(self, node):
        edges = set()
        for successor in self._graph[node]:
            edges.add((node, successor, self._graph[node][successor]["weight"]))
            del self._graph[successor][node]
        del self._graph[node]
        self._nodes.remove(node)
        return edges

    def find_subgraph(self, node):
        """
        Trouve le sous-graphe contenant tous les noeuds atteignables depuis `node`.
        :param node: Noeud d'où part la recherche
        :return: Sous-graphe [GraphUndirected]
        """
        nodes = self._dfs(node)
        subgraph = GraphUndirected()
        for node in nodes:
            subgraph._graph[node] = deepcopy(self._graph[node])
        subgraph._nodes = nodes
        return subgraph


    def _find_articulation_points(self):
        pre = dict()
        post = dict()
        articulation_points = set()
        count = 0
        for node in self._nodes:
            pre[node] = -1
            post[node] = -1
        for node in self._nodes:
            self._explore(node, node, pre, post, articulation_points, count)
        return articulation_points

    def _explore(self, node, successor, pre, post, articulation_points, count):
        children = 0
        count += 1
        pre[successor] = count
        post[successor] = count
        for next_node in self._graph[successor]:
            if pre[next_node] == -1:
                children += 1
                self._explore(successor, next_node, pre, post, articulation_points, count)
                post[successor] = min(post[successor], post[next_node])
                if post[next_node] >= pre[successor] and node != successor:
                    articulation_points.add(successor)
            elif next_node != node:
                post[successor] = min(post[successor], pre[next_node])
        if (node == successor) and (children > 1):
            articulation_points.add(successor)

    def find_highest_friend_group(self):
        # Find all cycles
        # For each cycle sorted by length decreasing:
        #   If it's a complete subgraph:
        #       Return the solution
        #
        all_cycles = self.find_all_cycles()
        for cycle in sorted(all_cycles, key=len, reverse=True):
            valid = True
            for node in cycle:
                neighbours = set(cycle)
                neighbours.remove(node)
                if not neighbours.issubset(self._graph[node].keys()):
                    valid = False
                    break
            if not valid:
                continue
            return cycle

    def find_all_cycles(self):

        def visit(node, cycle_detected, visited=list()):
            if visited and node == visited[0]:
                if len(visited) <= 2:
                    return
                # Cycle trouvé
                # Normalisation du cycle trouvé:
                # On veut ajouter le cycle en partant du node avec la plus petite valeur
                # suivi du node ayant la deuxième plus petite valeur
                visited = self._normalize(visited)

                cycle_detected.add(tuple(visited))
            else:
                visited.append(node)
                connected_nodes = self._graph[node]
                avoid_nodes = set(visited[1:])
                for connected_node in connected_nodes.keys() - avoid_nodes:
                    visit(connected_node, cycle_detected, visited)
                visited.pop()

        cycle_detected = set()
        for node in self._nodes:
            visit(node, cycle_detected)

        return cycle_detected

    def _normalize(self, nodes):
        """
        Re-arrange the sequence of nodes starting by the smallest and followed by the second smallest.

        This allows for easy comparison between ordered sequences of nodes

        :param nodes: sequence of nodes
        :return: normalized sequence of nodes
        """
        min_node = min(nodes)
        min_index = nodes.index(min_node)
        nodes = nodes[min_index:] + nodes[:min_index]
        if nodes[1] > nodes[-1]:
            nodes = self._invert_cycle(nodes)
        return nodes

    @staticmethod
    def _invert_cycle(cycle):
        return [cycle[0]] + cycle[1:][::-1]