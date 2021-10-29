class BayesianNode:
    def __init__(self, name, parents, children, states, probabilities):
        self.name = name
        self.parents = parents
        self.children = children
        self.states = states
        self.probabilities = probabilities
