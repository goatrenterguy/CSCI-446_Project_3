from BayesianNetwork import BayesianNetwork as BNet


class FileParser:
    def __init__(self):
        self.bayesNet = BNet()

    def makeBN(self):
        return self.bayesNet

    def readFile(self, path):
        pass

    def readVariables(self, file):
        pass

    def readProbabilities(self, file):
        pass
