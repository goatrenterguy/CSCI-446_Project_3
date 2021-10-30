from BayesianNode import BayesianNode as BNode


class BayesianNetwork:
    def __init__(self, Name):
        self.network = {}
        self.name = Name

    def addNode(self, node):
        self.network[node.name] = node

    def getNode(self, name):
        pass
