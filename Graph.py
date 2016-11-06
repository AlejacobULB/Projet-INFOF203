from Vertex import*
class Graph:
    def __init__(self,fileName):
        self.grahMap = dict()
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
            if vertexName in self.grahMap:
                countData +=1
                continue
            vertex = Vertex(vertexName)
            self.grahMap[vertexName] = vertex
            count += 1
        countData = 1
        while countData < len(self.graphData)-1:
            vertexNameFrom = self.graphData[countData][0]
            vertexNameTo = self.graphData[countData][1]
            amount = self.graphData[countData][2]
            if vertexNameTo not in self.grahMap:
                vertex = Vertex(vertexNameTo)
                self.grahMap[vertexNameTo] = vertex
            self.grahMap[vertexNameFrom].addDebt(self.grahMap[vertexNameTo], amount)
            countData += 1
    
    def printGraph(self):
        for key in self.grahMap:
            vertex = self.grahMap[key]
            print("Vertex {} has {} connexions".format(key, vertex.getNumberOfConnexions))
            print("Debts :")
            for item in vertex.getDebt():
                print(" Vertex {} has debt to Vertex {} for {} euro".format(key, item[1].getName(),item[2]))
            print()
