import random
from functools import reduce

from Objects import *
from BayesianNetwork import BayesianNetwork


class ExactInference:
    def eliminationAsk(self, X, e, BNet: BayesianNetwork):
        factors = []
        for var in BNet.getVariables():
                factors.append(self.makeFactor(var, e, BNet))
        for var in self.order(BNet.getVariables()):
            if var != X and var not in e:
                factors = self.sumOut(var, factors)
        finalFactor = self.pointWiseProduct(factors)
        cpt = finalFactor.cpt.copy()
        for evidence in e:
            index = finalFactor.variables.index(evidence)
            for key in finalFactor.cpt:
                if key[index] != e[evidence]:
                    del cpt[key]
            finalFactor.variables.remove(evidence)
        finalFactor.cpt = cpt
        return self.normalize(finalFactor)

    def matchingVariables(self, f1, f2):
        matchingVariables = []
        for fv in range(len(f1.variables)):
            for ov in range(len(f2.variables)):
                if f1.variables[fv] == f2.variables[ov]:
                    matchingVariables.append((fv, ov))
        return matchingVariables

    def pointWiseProduct(self, factors):
        while len(factors) > 1:
            f1 = factors[0]
            f2 = factors[1]
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
                factors.append(Factor("", variables, cpt))
        return Factor(factors[0].name, factors[0].variables, factors[0].cpt)

    def sumOut(self, var, factors):
        keep = []
        varInFactor = []
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
        if len(varInFactor) > 1:
            factored = self.pointWiseProduct(varInFactor)
            # Get index of var
            indexVar = factored.variables.index(var)
            cpt = {}
            flagged = []
            for k1 in factored.cpt:
                for k2 in factored.cpt:
                    if k1 != k2 and k2 not in flagged:
                        match = True
                        for i in range(len(factored.variables)):
                            if i != indexVar and k1[i] != k2[i]:
                                match = False
                        if match:
                            flagged.append(k1)
                            flagged.append(k2)
                            key = []
                            for val in range(len(k1)):
                                if val != indexVar:
                                    key.append(k1[val])
                            if tuple(key) in cpt:
                                cpt[tuple(key)] = cpt[tuple(key)] + factored.cpt[k2]
                            else:
                                cpt[tuple(key)] = factored.cpt[k1] + factored.cpt[k2]
            factored.variables.remove(var)
            keep.append(Factor(factored.name, factored.variables, cpt))
        return keep

    def normalize(self, factor):
        sum = 0
        for k in factor.cpt:
            sum += factor.cpt[k]
        for k in factor.cpt:
            factor.cpt[k] = factor.cpt[k] / sum
        return factor

    def order(self, variables):
        # Random order can change later
        random.seed(1)
        random.shuffle(variables)
        return variables

    def makeFactor(self, var, evidence, BNet: BayesianNetwork):
        node = BNet.getNode(var)
        variables = node.parents
        name = var
        if len(variables) == 0 or var not in evidence:
            variables += [name]
        cpt = {}
        for p in node.probabilities:
            for i in range(len(node.states)):
                if p == "table":
                    cpt[(node.states[i],)] = float(node.probabilities[p][i])
                else:
                    cpt[p + (node.states[i],)] = float(node.probabilities[p][i])
        return Factor(name, variables, cpt)
