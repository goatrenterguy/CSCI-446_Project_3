import random

from Objects import *
from BayesianNetwork import BayesianNetwork


class ExactInference:
    def eliminationAsk(self, X, e, BNet: BayesianNetwork):
        factors = []
        for var in self.order(BNet.getVariables()):
            factors.append(self.makeFactor(var, e, BNet))
            if var != X and var not in e:
                factors = self.sumOut(var, factors, BNet)
        return self.normalize(self.pointWiseProduct(factors, BNet))

    def pointWiseProduct(self, factors, BNet):
        cpt = {}
        matchingVariables = []
        if len(factors) > 1:
            for f in range(len(factors)):
                for o in range(f, len(factors)):
                    for fv in range(len(factors[f].variables)):
                        for ov in range(len(factors[o].variables)):
                            if o.variables[ov] == f.variables[fv]:
                                matchingVariables.append((fv, ov))
                        variables = f.variables + [X for X in o.variables if X not in f.variables]
                        # TODO: Figure out how to merge where the value that the two factors have in common
                        #  have the same state need to be multiplied by that probability
                        # cpt[o.probabilities]
                        # Index of v in f
                        # Index of v in o
        return factors

    def sumOut(self, var, factors, BNet):
        keep = []
        varInFactor = []
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
        keep.extend(self.pointWiseProduct(varInFactor, BNet))
        return keep


    def normalize(self, factor):
        pass

    def order(self, variables):
        # Random order can change later
        random.seed(1)
        random.shuffle(variables)
        return variables

    def makeFactor(self, var, evidence, BNet: BayesianNetwork):
        node = BNet.getNode(var)
        variables = node.parents
        cpt = {}
        if var not in evidence:
            variables.append(var)
        for p in node.probabilities:
            for i in range(len(node.states)):
                if p == "table":
                    cpt[(node.states[i],)] = float(node.probabilities[p][i])
                else:
                    cpt[p + (node.states[i],)] = float(node.probabilities[p][i])
        return Factor(variables, cpt)
