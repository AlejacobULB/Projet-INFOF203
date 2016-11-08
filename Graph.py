from Vertex import*
class Graph:
    def __init__(self,fileName):
        self.graphMap = dict()
        self.vertexDict = dict()
        self.graphOrder = 0
        graphData = self.readFile(fileName)
        self.graphOrder =int(graphData[0][0])
        self.addNodesFromFile(graphData)
        self.addDebtFromFile(graphData)
        self.createVertexDict()


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
        for vertex in sorted(self.graphMap):
            if vertexTag[vertex] != "black":
                parcours.append(self.dfs(vertex, vertexTag))
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
        id, cnt = 0, 0
        pre = dict()
        post = dict()
        for item in self.graphMap:
            pre[item], post[item] = 0, 0
        for item in self.graphMap:
            if pre[item] == 0:
                self.cycle(item, pre, post, id, cnt)
        print(pre)
        print(post)

    def cycle(self,item, pre, post, id, cnt):
        id += 1
        pre[item] = id
        if self.graphMap[item] == None:
            cnt+=1
            post[item] = cnt
            return
        for next in self.graphMap[item]:
            if pre[next] == 0:
                self.cycle(next,pre,post,id,cnt)
            elif post[next] == 0:
                print("Cycle")

        cnt +=1
        post[item] = cnt


    def printGraph(self):
        for key in self.vertexDict:
            vertex = self.vertexDict[key]
            print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
            print("Debts :")
            for item in vertex.getDebt():
                print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
            print()
        
