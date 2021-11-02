class BayesianNode:
    def __init__(self, name=str(), parents=[], children=[], states=[], probabilities={}):
        self.name = name
        self.parents = parents
        self.children = children
        self.states = states
        self.probabilities = probabilities

    def setName(self, name):
        self.name = name

    def setProbability(self, probabilities):
        self.probabilities = probabilities
