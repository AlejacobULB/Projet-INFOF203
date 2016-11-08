class Vertex:
    def __init__(self,name):
        self.name = name
        self.debt = []
        self.getNumberOfConnexions = 0
    
    def getName(self):
        return self.name
    
    def getNumberOfConnexions(self):
        self.getNumberOfConnexions
    
    def getDebt(self):
        return self.debt
    
    def addDebt(self, VertexTo, amount):
        self.debt.append(list())
        self.debt[self.getNumberOfConnexions].append(self)
        self.debt[self.getNumberOfConnexions].append(VertexTo)
        self.debt[self.getNumberOfConnexions].append(amount)
        self.getNumberOfConnexions +=1
    
    
    
    
