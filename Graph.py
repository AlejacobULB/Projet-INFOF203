from Vertex import*
class Graph:
    def __init__(self,fileName):
        self.graphMap = dict()
        self.vertexDict = dict()
        self.graphOrder = 0
        self.graphData = list()
        self.readFile(fileName)
        self.graphOrder =int(self.graphData[0][0])
        self.addNodesDebtsFromFile()


    def readFile(self,fileName):
        file = open(fileName,"r")
        self.graphData = file.read()
        self.graphData = self.graphData.split("\n")
        for i in range(len(self.graphData)-1):
            self.graphData[i] = self.graphData[i].split(" ")
    
    def addNodesDebtsFromFile(self):
        count = 0
        countData = 1
        while count < self.graphOrder and countData < len(self.graphData)-1:
            vertexName = self.graphData[countData][0]
            if vertexName in self.vertexDict:
                countData +=1
                continue
            vertex = Vertex(vertexName)
            self.vertexDict[vertexName] = vertex
            count += 1

        countData = 1
        while countData < len(self.graphData)-1:
            vertexNameFrom = self.graphData[countData][0]
            vertexNameTo = self.graphData[countData][1]
            amount = self.graphData[countData][2]
            if vertexNameTo not in self.vertexDict:
                vertex = Vertex(vertexNameTo)
                self.vertexDict[vertexNameTo] = vertex
            self.vertexDict[vertexNameFrom].addDebt(self.vertexDict[vertexNameTo], amount)
            countData += 1

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
        couleur = dict()
        for v in sorted(self.graphMap):
            couleur[v] = 'blanc'
        for vertex in sorted(self.graphMap):
            if couleur[vertex] != "noir":
                print("".join(self.dfs(vertex, couleur)))

    def dfs(self, s, couleur):
        P = [s]
        couleur[s] = 'gris'
        Q = [s]
        while Q:
            u = Q[-1]
            if self.graphMap[u] is None:
                Q.pop()
                couleur[u] = "noir"
                continue
            R = [y for y in self.graphMap[u] if couleur[y] == 'blanc']
            if R:
                v = R[0]
                couleur[v] = 'gris'
                P.append(v)
                Q.append(v)
            else:
                Q.pop()
                couleur[u] = 'noir'
        return P

    def printGraph(self):
        for key in self.vertexDict:
            vertex = self.vertexDict[key]
            print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
            print("Debts :")
            for item in vertex.getDebt():
                print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
            print()
