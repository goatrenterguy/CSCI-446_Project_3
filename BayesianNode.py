class BayesianNode:
    def __init__(self, name="", parents=[], children=[], states=[], probabilities={}):
        self.name = name
        self.parents = parents
        self.children = children
        self.states = states
        self.probabilities = probabilities

    def setName(self, name):
        self.name = name

    def addParent(self, parent):
        self.parents.append(parent)

    def addChild(self, child):
        self.children.append(child)

    def addState(self, state):
        self.states.append(state)

    def addProbability(self, key, value):
        self.probabilities[key] = value
