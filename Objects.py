
class Factor:
    def __init__(self, variables, cpt, pFor=[], evidence=[]):
        self.pFor = pFor
        self.evidence = evidence
        self.variables = variables
        self.cpt = cpt


class Probability:
    def __init__(self):
        variable = ""
        evidence = []


class Sample:
    def __init__(self):
        self.nodes = dict()

    def addNode(self, variable, value):
        self.nodes.add(variable, value)
