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
        while len(factors) > 1:
            f = factors.pop(-1)
            cpt = {}
            for v in f.variables:
                for o in factors:
                    if o != f and v in o.variables:
                        variables = f.variables + [X for X in o.variables if X not in f.variables]
                        # TODO: Figure out how to merge where the value that the two factors have in common
                        #  have the same state need to be multiplied by that probability
                        # cpt[o.probabilities]
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
                cpt[(p,) + (node.states[i],)] = node.probabilities[p][i]
        return Factor(variables, cpt)
