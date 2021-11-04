import re
from BayesianNetwork import BayesianNetwork as BNet
from BayesianNode import BayesianNode as BNode

# TODO: Fix file parser adding 'table' to the probability table when a node has no parents
class FileParser:
    def __init__(self):
        self.bayesNet = BNet()
        self.bif = ""

    def readFile(self, path):
        with open(path, "r") as bif:
            self.bif = bif.read()
        networkBlock = self.getNetworkBlock()
        self.bayesNet.setName(networkBlock.split()[1])
        variableBlocks = self.getBlocks("variable")
        probabilityBlocks = self.getBlocks("probability")
        self.parseVariables(variableBlocks)
        self.parseProbabilities(probabilityBlocks)

    def getNetworkBlock(self):
        start = self.bif.index("network")
        end = self.bif.index("}\n") + 1
        networkString = self.bif[start:end]
        return networkString

    def getBlocks(self, blockType: str):
        start = self.bif.index(blockType)
        end = self.bif.index("}\n", start) + 1
        blocks = []
        while start != -1:
            blocks.append(self.bif[start:end])
            start = self.bif.find(blockType, end)
            end = self.bif.find("}\n", start) + 1
        return blocks

    def parseVariables(self, blocks):
        for block in blocks:
            start = block.index("type")
            end = block.index("};") + 1
            self.bayesNet.addNode(BNode(name=block.split()[1], states=self.parseState(block[start:end])))

    @staticmethod
    def parseState(block):
        start = block.index("{") + 1
        end = block.index("}")
        return block[start:end].replace(",", "").split()

    def parseProbabilities(self, blocks):
        for block in blocks:
            # Parse variables for factor
            variables = list()
            start = block.index("(")
            end = block.index(")")
            variables = block[start + 1: end].replace(" |", "").replace(",", "").split()
            node = self.bayesNet.getNode(variables[0])
            node.parents = variables[1:]
            for var in variables[1:]:
                children = self.bayesNet.getNode(var).children.copy()
                children.append(node.name)
                self.bayesNet.getNode(var).children = children
            probabilities = self.parseProbabilityValues(block[end + 1:])
            if "table" in probabilities:
                values = probabilities["table"]
                probabilities = {tuple(node.states): values}
            node.setProbability(probabilities)

    @staticmethod
    def parseProbabilityValues(block):
        probabilities = {}
        if "table" in block:
            current = block[2:-3].replace(",", "").split()
            probabilities[current[0]] = current[1:]
        else:
            start = block.index("(")
            end = block.index(";\n", start)
            while start != -1:
                key = []
                value = []
                current = block[start:end]
                keyStart = current.index("(")
                keyEnd = current.index(")")
                key.extend(current[keyStart + 1: keyEnd].replace(",", "").split())
                value.extend(current[keyEnd + 1:].replace(",", "").split())
                probabilities[tuple(key)] = tuple(value)
                start = block.find("(", end)
                end = block.find(";\n", start)
        return probabilities

