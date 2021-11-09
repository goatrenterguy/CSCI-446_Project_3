import re
from BayesianNetwork import BayesianNetwork as BNet
from BayesianNode import BayesianNode as BNode


class FileParser:
    def __init__(self):
        self.bayesNet = BNet()
        self.bif = ""

    def readFile(self, path):
        """
        Function for reading in a .bif file
        :param path: Path to a .bif file
        :return: Returns a bayesian network generated from the bif file
        """
        # Open the file
        with open(path, "r") as bif:
            self.bif = bif.read()
        # Get the first block with network name and network properties
        networkBlock = self.getNetworkBlock()
        # Set the name of the Bayesian network
        self.bayesNet.setName(networkBlock.split()[1])
        # Get all variable blocks
        variableBlocks = self.getBlocks("variable")
        # Get all probability blocks
        probabilityBlocks = self.getBlocks("probability")
        # Parse the variable blocks
        self.parseVariables(variableBlocks)
        # Parse the probability blocks
        self.parseProbabilities(probabilityBlocks)
        # Return the Bayes net
        return self.bayesNet

    def getNetworkBlock(self):
        """
        Function to get the blocks for netowrks
        :return: Name of the network
        """
        # Get the name of the network
        start = self.bif.index("network")
        end = self.bif.index("}\n") + 1
        networkString = self.bif[start:end]
        return networkString

    def getBlocks(self, blockType: str):
        """
        Parse input into blocks denoted by the type and ending with a }\n
        :param blockType: Type of block to parse
        :return: A list of all blocks of that type
        """
        start = self.bif.index(blockType)
        end = self.bif.index("}\n", start) + 1
        blocks = []
        while start != -1:
            blocks.append(self.bif[start:end])
            start = self.bif.find(blockType, end)
            end = self.bif.find("}\n", start) + 1
        return blocks

    def parseVariables(self, blocks):
        """
        Function to generate nodes from a variable block
        :param blocks: String of for a block
        """
        for block in blocks:
            start = block.index("type")
            end = block.index("};") + 1
            self.bayesNet.addNode(BNode(name=block.split()[1], states=self.parseState(block[start:end])))

    @staticmethod
    def parseState(block):
        """
        Function to parse the states of a block
        :param block:
        :return:
        """
        start = block.index("{") + 1
        end = block.index("}")
        return block[start:end].replace(",", "").split()

    def parseProbabilities(self, blocks):
        """
        Function to parse the probabilities for a given block
        :param blocks: String representation of a block
        """
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
            # if "table" in probabilities:
            #     values = probabilities["table"]
            #     probabilities = {tuple(node.states): values}
            node.setProbability(probabilities)

    @staticmethod
    def parseProbabilityValues(block):
        """
        Function to parse the values of given probabilites
        :param block: String representation of a block
        :return: The probabilities for that block
        """
        probabilities = {}
        if " table " in block:
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
