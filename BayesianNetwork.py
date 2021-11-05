from BayesianNode import BayesianNode as BNode


class BayesianNetwork:
    def __init__(self):
        self.network = dict()
        self.name = str

    def setName(self, name):
        self.name = name

    def addNode(self, node: BNode):
        self.network[node.name] = node

    def getNode(self, name) -> BNode:
        return self.network[name]

    def getVariables(self) -> list:
        return list(self.network.keys())
