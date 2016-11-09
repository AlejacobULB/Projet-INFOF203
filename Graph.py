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
        self.cnt = 0
        self.pre = list()
        self.post = list()

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
        vertexTag[s] = 'gris'
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

    def detectionCyle(self):
        self.pre = [-1 for i in range(self.graphOrder)]
        self.post = [-1 for i in range(self.graphOrder)]
        global cycleList
        cycleList = list()
        for i in range(self.graphOrder):
            if self.pre[i] == -1:
                self.cycle(self.vertexList[i], i)
        print(self.pre)
        print(self.post)

    def cycle(self, item, index):
        self.id += 1
        self.pre[index] = self.id
        if self.graphMap[item] is None:
            self.cnt+=1
            self.post[index] = self.cnt
            return
        cycleList.append(item)
        for next in self.graphMap[item]:
            nextIndex = self.vertexList.index(next)
            if self.pre[nextIndex] == -1:
                self.cycle(next, nextIndex)
            elif self.post[nextIndex] == -1:
                cycleList.append(next)
                print("Cycle")
                print(cycleList)
                print(next)
                cycleList[:] = []
        self.cnt +=1
        self.post[index] = self.cnt


    def printGraph(self):
        for key in self.vertexDict:
            vertex = self.vertexDict[key]
            print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
            print("Debts :")
            for item in vertex.getDebt():
                print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
            print()
        
