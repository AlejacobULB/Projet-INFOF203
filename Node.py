class Node:
    def __init__(self, name):
        self.name = name
        self.reached = False
        self.loans = list()
        self.creditorCount = 0

    def getName(self):
        return self.name


    def getLoans(self):
        return self.loans

    def setLoans(self):
        return self.loans

    def addCreditor(self):
        self.creditorCount += 1

    def delCreditor(self):
        self.creditorCount -= 1

    def addLoan(self, loan):
        self.loans.append(loan)

    def removeLoan(self, loan):
        self.loans[self.loans.index(loan)] =  None

    def isHead(self):
        return self.creditorCount == 0

    def isReached(self):
        return self.reached

    def mark(self):
        self.reached = True
