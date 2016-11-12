# from Vertex import*
from collections import namedtuple, defaultdict

Edge = namedtuple("Edge", "node weight")

class Graph:
    def __init__(self):
        self._graph = defaultdict(set)
        self._node_list = list()
        # self.val = dict()
        # self.id = 0
        # self.biconnected_component =list()
        self.cycle_detected = list()

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
            if node1 not in graph._node_list:
                graph._node_list.append(node1)
            if node2 not in graph._node_list:
                graph._node_list.append(node2)
       
        return graph

    def add_edge(self, node1, node2, weight):
        self._graph[node1].add(Edge(node=node2, weight=weight))

      
    def get_weight(self, node1, node2):
        if node1 not in self._graph:
            print("No adjacent for this node")
            return
        for edge in self._graph[node1]:
            if edge.node == node2:
                return edge.weight

    # def get_node_to(self, node1, weight):
    #     if node1 not in self._graph:
    #         print("No adjacent for this node")
    #         return
    #     for edge in self._graph[node1]:
    #         if edge.weight == weight:
    #             return edge.node


    def DepthFirst(self):
        vertexTag = dict()
        parcours = []
        for v in self._node_list:
            vertexTag[v] = 'white'
        for i in range(len(self._node_list)):
            if vertexTag[self._node_list[i]] != "black":
                parcours.append(self.dfs(self._node_list[i], vertexTag))
                print(vertexTag) 

        #for i in self._node_list:
        #     if vertexTag[i] != "black":
        #         parcours.append(self.dfs(i, vertexTag))
        #         print(vertexTag)
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

    def detection_cycle(self):
        cycle_solution = list()
        vertexTag = dict()
        for node in self._node_list:
            vertexTag[node] = False
        for node in self._node_list:
            cycle_solution.append(node)
            vertexTag[node] = True
            self.cycle(node, cycle_solution, vertexTag)
            cycle_solution = []
        return self.cycle_detected

    def cycle(self, node, cycle_solution, vertexTag):
        if len(cycle_solution) != 1 and vertexTag[node] :
            if not self.verify_cycle(cycle_solution):
                self.cycle_detected.append(cycle_solution)
        else:
            edges = self._graph[node]
            for edge in edges:
                successor = edge.node
                if successor in self._graph and not vertexTag[successor]:
                    cycle_solution.append(successor)
                    vertexTag[successor] = True
                    self.cycle(successor, cycle_solution, vertexTag)
        vertexTag[node] = False

    def verify_cycle(self, cycle_solution):
        for cycle in self.cycle_detected:
            if all(node in cycle for node in cycle_solution) and len(cycle) == len(cycle_solution):
                return True
        return False




    # def biconnected_component_search(self):
    #     for node in self._node_list:
    #         self.val[node] = 0
    #     for node in self._node_list:
    #         if self.val[node] == 0:
    #             self.bc(node)
    #     print(self.biconnected_component)

    # def bc(self, node):
    #     self.id +=1
    #     self.val[node] = self.id
    #     min = self.id
    #     if node not in self._graph == None:
    #         return min
    #     edges = self._graph[node]
    #     for edge in edges:
    #         node = edge.node
    #         if self.val[node] == 0:
    #             m = self.bc(node)
    #             if m < min:
    #                 min = m
    #             if m >= self.val[node]:
    #                 self.biconnected_component.append(node)
    #         else:
    #             if self.val[node] < min:
    #                 min = self.val[node]
    #     return min


#     def printGraph(self):
#         for key in self.vertexDict:
#             vertex = self.vertexDict[key]
#             print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
#             print("Debts :")
#             for item in vertex.getDebt():
#                 print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
#             print()