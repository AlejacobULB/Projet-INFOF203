#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from copy import deepcopy


class GraphException(Exception):
    pass

class Graph():

    def __init__(self):
        """Function who initialize a empty graph"""
        self._graph = defaultdict(dict)
        self._nodes = set()

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

    def iter_edges(self):
        for node1, edge in self._graph.items():
            for node2, attr in edge.items():
                yield node1, node2, attr["weight"]

    def __str__(self):
        """Represent the graph"""
        output = ""
        for node in self._graph:
            for successor in self._graph[node]:
                weight = self.get_weight(node, successor)
                output += ("{} {} {} \n".format(node, successor, weight))
        return output


class DirectedGraph(Graph):

    @classmethod
    def load(cls, fileName):
        """Class method which create the graph from a file who contains all the data like : NodeFrom NodeTo weight"""
        graph = cls()
        with open(fileName, "r") as file:
            graphData = file.read()
        for i, line in enumerate(graphData.splitlines()):
            if i == 0:
                # skip first line, because we don't need it in our implementation of the problem
                continue
            node1, node2, weight = line.split(" ")
            weight = int(weight)
            graph.add_edge(node1, node2, weight)
        return graph

    def detect_and_solve_all_cycles(self):
        cycles = sorted(self.find_all_cycles(), key=len)
        for cycle in cycles:
            self._resolve_cycle(cycle)

    def _resolve_cycle(self, cycle):
        """
        Function which solve the debts of a cycle by simplifying all the debts by smallest amounts.
        One starts with the cycle having the smallest size.
        Once a cycle is simplified, we place the new debts instead of old
        """
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

    def find_all_cycles(self):
        """
        Function which finds all the cycles contained in a graph.
        A cycle is a continuation of node whose last node makes it possible to return to the first node.
        :return: all cyles contains in a graph. The return value is contained a set.
        """
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



    def find_communities(self):
        undirected_graph = GraphUndirected.from_graph(self)
        return undirected_graph.find_communities()

    def find_highest_friend_group(self):
        undirected_graph = GraphUndirected.from_graph(self)
        friend_group = undirected_graph.find_highest_friend_group()
        return friend_group


class GraphUndirected(Graph):

    @classmethod
    def from_graph(cls, directed_graph):
        """Function which creates an undirected graph starting from a directed graph."""
        undirected_graph = cls()
        for node1, node2, weight in directed_graph.iter_edges():
            undirected_graph.add_edge(node1, node2, weight)
        return undirected_graph

    def add_edge(self, node1, node2, weight):
        super().add_edge(node1, node2, weight)
        super().add_edge(node2, node1, weight)

    def find_communities(self):
        """
        Function which finds all communities of a graph, that is made by depth first search starting from a node.
        Depth First Search  is an algorithm for traversing graph
        One starts at  a selecting some arbitrary node and explores recursively as far as possible along each branch.
        When a traversing is found, we add it to a set and we update the visited set.
        :return: a set with all the communities.
        """
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

    def find_highest_friend_group(self):
        """
        Find all cycles
        For each cycle sorted by length decreasing:
        If it's a complete subgraph:
        Return the solution
        """
        all_cycles = self.find_all_cycles()
        for cycle in sorted(all_cycles, key=len, reverse=True):
            valid = True
            for node in cycle:
                neighbours = set(cycle)
                neighbours.remove(node) # remove the node to have all the possible successors
                if not neighbours.issubset(self._graph[node].keys()):
                    # check if the set is a subset of all the successors of the withdrawn node.
                    valid = False
                    break
            if not valid:
                continue
            return cycle

    def find_all_cycles(self):
        """
        Function which finds all the cycles contained in a graph.
        A cycle is a continuation of node whose last node makes it possible to return to the first node.
        :return: all cyles contains in a graph. The return value is contained a set.
        """
        def visit(node, cycle_detected, visited=list()):
            if visited and node == visited[0]:
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
        """
        Function which reverses a list starting from the second item until the end
        """
        return [cycle[0]] + cycle[1:][::-1]