
class Factor:
    def __init__(self, variables, cpt, pFor=[], evidence=[]):
        self.evidence = evidence
        self.pFor = pFor
        self.variables = variables
        self.cpt = cpt

    def __repr__(self):
        return str(self.variables) + str(self.cpt)


class Probability:
    def __init__(self):
        variable = ""
        evidence = []
