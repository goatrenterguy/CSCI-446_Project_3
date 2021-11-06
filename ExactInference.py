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
        return self.pointWiseProduct(factors)

    def matchingVariables(self, f1, f2):
        matchingVariables = []
        for fv in range(len(f1.variables)):
            for ov in range(len(f2.variables)):
                if f1.variables[fv] == f2.variables[ov]:
                    matchingVariables.append((fv, ov))
        return matchingVariables

    def pointWiseProduct(self, factors):
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
        return Factor(factors[0].variables, factors[0].cpt)

    def sumOut(self, var, factors, BNet):
        keep = []
        varInFactor = []
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
        factored = self.pointWiseProduct(varInFactor)
        if factored and len(factored.variables) > 1:
            # Get index of var
            indexVar = factored.variables.index(var)
            cpt = {}
            for k1 in factored.cpt:
                for k2 in factored.cpt:
                    if k1 != k2:
                        match = True
                        for i in range(len(factored.variables)):
                            if i != indexVar and k1[i] != k2[i]:
                                match = False
                        if match:
                            key = []
                            for val in range(len(k1)):
                                if val != indexVar:
                                    key.append(k1[val])
                            if tuple(key) in cpt:
                                cpt[tuple(key)] = cpt[tuple(key)] + factored.cpt[k2]
                            else:
                                cpt[tuple(key)] = factored.cpt[k1] + factored.cpt[k2]
                            break
            factored.variables.remove(var)
            keep.append(Factor(factored.variables, cpt))
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
        variables = node.parents + [node.name]
        cpt = {}
        for p in node.probabilities:
            for i in range(len(node.states)):
                if p == "table":
                    cpt[(node.states[i],)] = float(node.probabilities[p][i])
                else:
                    cpt[p + (node.states[i],)] = float(node.probabilities[p][i])
        return Factor(variables, cpt)
