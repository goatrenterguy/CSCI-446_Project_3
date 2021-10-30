import re
from BayesianNetwork import BayesianNetwork as BNet
from BayesianNode import BayesianNode as BNode


class FileParser:
    def __init__(self):
        self.bayesNet = None
        self.bif = None

    def makeBNet(self, name):
        self.bayesNet = BNet(name)

    def readFile(self, path):
        with open(path, "r") as bif:
            self.bif = bif.read()
        networkBlock = self.getNetworkBlock()
        self.makeBNet(networkBlock.split()[1])
        variableBlocks = self.getBlocks("variable")
        probabilityBlocks = self.getBlocks("probability")
        self.parseVariables(variableBlocks)

    def getNetworkBlock(self):
        start = self.bif.index("network")
        end = self.bif.index("}\n") + 1
        networkString = self.bif[start:end]
        return networkString

    def getBlocks(self, type: str):
        start = self.bif.index(type)
        end = self.bif.index("}\n", start) + 1
        blocks = []
        while start != -1:
            blocks.append(self.bif[start:end])
            start = self.bif.find(type, end)
            end = self.bif.find("}\n", start) + 1
        return blocks

    def parseVariables(self, blocks):
        for block in blocks:
            start = block.index("type")
            end = block.index("};") + 1
            self.bayesNet.addNode(BNode(name=block.split()[1], states=self.parseState(block[start:end])))

    def parseState(self, block):
        start = block.index("{") + 1
        end = block.index("}")
        return block[start:end].replace(",", "").split()

    def parseProbabilites(self, blocks):
        for block in blocks:
            pass
