class Factor:
    def __init__(self):
        probabilities = []

    def makeFactor(self, var, evidence):
        pass


class Probability:
    def __init__(self):
        variable = ""
        evidence = []


class Sample:
    def __init__(self):
        nodes = dict()

    def addNode(self, variable, value):
        nodes.add(variable, value)