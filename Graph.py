from Vertex import*
class Graph:
    def __init__(self,fileName):
        self.graphMap = dict()
        self.vertexDict = dict()
        self.graphOrder = 0
        self.vertexList = list()
        graphData = self.readFile(fileName)
        self.graphOrder =int(graphData[0][0])
        self.addNodesFromFile(graphData)
        self.addDebtFromFile(graphData)
        self.createVertexDict()
        self.id = 0
        self.val = [0 for i in range(self.graphOrder)]

    def readFile(self,fileName):
        file = open(fileName,"r")
        graphData = file.read()
        graphData = graphData.split("\n")
        for i in range(len(graphData)-1):
            graphData[i] = graphData[i].split(" ")
        return graphData

    def addNodesFromFile(self, graphData):
        count = 0
        countData = 1
        while count < self.graphOrder and countData < len(graphData)-1:
            vertexName = graphData[countData][0]
            if vertexName in self.vertexDict:
                countData +=1
                continue
            vertex = Vertex(vertexName)
            self.vertexDict[vertexName] = vertex
            count += 1

    def addDebtFromFile(self, graphData):
        countData = 1
        while countData < len(graphData)-1:
            vertexNameFrom = graphData[countData][0]
            vertexNameTo = graphData[countData][1]
            if vertexNameFrom not in self.vertexList:
                self.vertexList.append(vertexNameFrom)
            if vertexNameTo not in self.vertexList:
                self.vertexList.append(vertexNameTo)
            amount = graphData[countData][2]
            if vertexNameTo not in self.vertexDict:
                vertex = Vertex(vertexNameTo)
                self.vertexDict[vertexNameTo] = vertex
            self.vertexDict[vertexNameFrom].addDebt(self.vertexDict[vertexNameTo], amount)
            countData += 1

    def createVertexDict(self):
        for key in self.vertexDict:
            vertex = self.vertexDict[key]
            if vertex.getNumberOfConnexions ==0:
                self.graphMap[key] = None
                continue
            for number in range(vertex.getNumberOfConnexions):
                if key not in self.graphMap:
                    self.graphMap[key] = list()
                self.graphMap[key].append(vertex.getDebt()[number][1].getName())

    def DepthFirst(self):
        vertexTag = dict()
        parcours = []
        for v in self.graphMap:
            vertexTag[v] = 'white'
        for i in range(self.graphOrder):
            if vertexTag[self.vertexList[i]] != "black":
                parcours.append(self.dfs(self.vertexList[i], vertexTag))
                print(vertexTag)
        return parcours

    def dfs(self, s, vertexTag):
        traversing = [s]
        vertexTag[s] = 'grey'
        stack = [s]
        while stack:
            u = stack[-1]
            if self.graphMap[u] is None:
                stack.pop()
                vertexTag[u] = "black"
                continue
            vertexSuccessor = [successor for successor in self.graphMap[u] if vertexTag[successor] == 'white']
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
        for vertexName in self.vertexList:
            if not self.vertexDict[vertexName].isTag():
                stack = Stack()
                self.cycle(self.vertexDict[vertexName], stack)

    def cycle(self, vertex, stack):
        debtList = vertex.getDebt()
        vertex.setTag()
        for i in range(len(debtList)):
            debt = debtList[i]
            if stack.getLastVertexIndex(vertex) == -1:
                stack.push(debt)
                self.cycle(debt[1], stack)
                stack.pop()
            else:
                print("cycle")

    def biconnected_component_search(self):
        for i in range(self.graphOrder):
            if self.val[i] == 0:
                self.bc(i)

    def bc(self, i):
        self.id +=1
        self.val[i] = self.id
        min = self.id
        if self.graphMap[self.vertexList[i]] == None:
            return min
        for vertex in self.graphMap[self.vertexList[i]]:
            vertexOrder = self.vertexList.index(vertex)
            if self.val[vertexOrder] == 0:
                m = self.bc(vertexOrder)
                if m < min:
                    min = m
                if m >= self.val[i]:
                    print(self.vertexList[i])
            else:
                if self.val[vertexOrder] < min:
                    min = self.val[vertexOrder]
        return min


    def printGraph(self):
        for key in self.vertexDict:
            vertex = self.vertexDict[key]
            print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
            print("Debts :")
            for item in vertex.getDebt():
                print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
            print()

class Stack:
    def __init__(self):
        self.stack = list()

    def getItem(self, index):
        return self.stack[index]

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def getSize(self):
        return len(self.stack)

    def getLastVertexIndex(self, vertex):
        vertexIndex = -1
        sizeStack = self.getSize()
        while sizeStack > 0 and vertexIndex == -1:
            sizeStack -= 1
            if self.getItem(sizeStack)[0] == vertex:
                vertexIndex = sizeStack
        return vertexIndex



