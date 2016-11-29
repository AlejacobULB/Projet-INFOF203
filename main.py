#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph import DirectedGraph, GraphUndirected
import time

if __name__ == '__main__':
    files = ["graphe.txt", "graphe_2.txt", "graphe_3.txt", "graphe_4.txt"]
    for file in files:
        print("--------- Exemple d'exécution pour {} ---------".format(file))
        directed_graph = DirectedGraph.load(file)
        print("Voici le graphe avant simplification")
        print(directed_graph)
        directed_graph.detect_and_solve_all_cycles()
        print()
        print("Voici le graphe après simplification s'il y en a eu")
        print(directed_graph)
        print("Voici les coummunautés:")
        communities = directed_graph.find_communities()
        output = ""
        for community in communities:
            res =""
            for node in community:
                res += node
            output += ",".join(res)
            output += "\n"
        print(output)
        print()
        highest_friend_group = directed_graph.find_highest_friend_group()
        print("Voici le plus grand groupe d'amis")
        print(highest_friend_group)
        print()
