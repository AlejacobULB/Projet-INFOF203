#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph import Graph, GraphUndirected
import time

if __name__ == '__main__':
    fileName = "graphe_2.txt"
    graph = Graph.load(fileName)
    undirected_graph = GraphUndirected.from_graph(graph)
    print(undirected_graph.find_highest_friend_group())


