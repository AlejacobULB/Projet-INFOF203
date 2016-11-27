#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph import DirectedGraph, GraphUndirected
import time

if __name__ == '__main__':
    fileName = "graphe.txt"
    directed_graph = DirectedGraph.load(fileName)
    print("Voici le graphe avant simplification")
    print(directed_graph)
    directed_graph.detected_and_solve_all_cycles()
    print()
    print("Voici le graphe après simplification")
    print(directed_graph)
    print("Voici les coummunautés:")
    communities = directed_graph.find_communities()
    output = ""
    for community in communities:
        res =""
        for node in community:
            res += node
        output+= ",".join(res)
        output+= "\n"
    print(output)
    print()
    print("Voici les hubs sociaux pour des communautés de {} individus".format(3))
    social_hub = directed_graph.find_social_hub(3)
    print(social_hub)
    print()
    print("Voici le plus grand groupe d'amis")
    highest_friend_group = directed_graph.find_highest_friend_group()
    print(highest_friend_group)
