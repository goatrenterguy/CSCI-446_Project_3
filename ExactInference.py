import random
from functools import reduce

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

    def matchingVariables(self, f1, f2):
        matchingVariables = []
        for fv in range(len(f1.variables)):
            for ov in range(len(f2.variables)):
                if f1.variables[fv] == f2.variables[ov]:
                    matchingVariables.append((fv, ov))
        return matchingVariables

    def pointWiseProduct(self, factors, BNet):
        for f1 in factors:
            for f2 in factors[1:]:
                matchingVariables = self.matchingVariables(f1, f2)
                if matchingVariables and f1 != f2:
                    factors.remove(f1)
                    factors.remove(f2)
                    cpt = {}
                    variables = f1.variables + [X for X in f2.variables if X not in f1.variables]
                    for pf in f1.cpt:
                        for po in f2.cpt:
                            for mv in matchingVariables:
                                if pf[mv[0]] == po[mv[1]]:
                                    key = pf
                                    for a in range(len(po)):
                                        if a != mv[1]:
                                            key += (po[a],)
                                    cpt[key] = f1.cpt[pf] * f2.cpt[po]
                    factors.append(Factor(variables, cpt))
                    break
        return factors

    def sumOut(self, var, factors, BNet):
        keep = []
        varInFactor = []
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
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
