import random
from Objects import *
from BayesianNetwork import BayesianNetwork


class ExactInference:
    def eliminationAsk(self, X, e, BNet: BayesianNetwork):
        factors = []
        for var in BNet.getVariables():
            factors.append(self.makeFactor(var, e, BNet))
        for var in self.order(BNet.getVariables(), BNet):
            if var != X and var not in e:
                factors = self.sumOut(var, factors, BNet)
        finalFactor = self.pointWiseProduct(factors)
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
                if f1.name is not None:
                    variables = f1.variables + [X for X in [str(f1.name)] + f2.variables if X not in f1.variables]
                else:
                    variables = f1.variables + [X for X in f2.variables if X not in f1.variables]
                if f2.name not in variables and f2.name is not None:
                    variables += [f2.name]
                for pf in f1.cpt:
                    for po in f2.cpt:
                        for mv in matchingVariables:
                            if pf[mv[0]] == po[mv[1]]:
                                key = pf
                                for a in range(len(po)):
                                    if a != mv[1]:
                                        key += (po[a],)
                                cpt[key] = f1.cpt[pf] * f2.cpt[po]
                factors.append(Factor(None, variables, cpt))
        return Factor(None, factors[0].variables, factors[0].cpt)

    def sumOut(self, var, factors, BNet):
        keep = []
        varInFactor = []
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
        if len(varInFactor) > 0:
            factored = self.pointWiseProduct(varInFactor)
            # Get index of var
            indexVar = factored.variables.index(var)
            cpt = {}
            keys = list(factored.cpt.keys())
            nodeStates = len(BNet.getNode(var).states)
            # We know the states we could use the dict to look up the values... Generate all possible combos...
            for k1i in range(len(keys)):
                count = 0
                for k2i in range(k1i, len(keys)):
                    k1 = keys[k1i]
                    k2 = keys[k2i]
                    if k1 != k2:
                        match = True
                        for i in range(len(factored.variables)):
                            if i != indexVar and k1[i] != k2[i]:
                                match = False
                        if match:
                            count += 1
                            key = []
                            for val in range(len(k1)):
                                if val != indexVar:
                                    key.append(k1[val])
                            if tuple(key) in cpt:
                                cpt[tuple(key)] = cpt[tuple(key)] + factored.cpt[k2]
                            else:
                                cpt[tuple(key)] = factored.cpt[k1] + factored.cpt[k2]
                            if count == nodeStates:
                                break
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

    def order(self, variables, BNet):
        numParents = []
        for v in variables:
            numParents.append([v, len(BNet.getNode(v).children)])
        numParents.sort(key=lambda x: x[1], reverse=False)
        order = [v[0] for v in numParents]
        return order

    def makeFactor(self, var, evidence, BNet: BayesianNetwork):
        node = BNet.getNode(var)
        name = var
        variables = [X for X in node.parents + [var] if X not in evidence]
        cpt = {}
        for p in node.probabilities:
            for i in range(len(node.states)):
                if var in evidence:
                    if evidence[var] == node.states[i]:
                        if p == "table":
                            cpt[(node.states[i],)] = float(node.probabilities[p][i])
                        else:
                            cpt[p + (node.states[i],)] = float(node.probabilities[p][i])
                else:
                    if p == "table":
                        cpt[(node.states[i],)] = float(node.probabilities[p][i])
                    else:
                        cpt[p + (node.states[i],)] = float(node.probabilities[p][i])
        return Factor(name, variables, cpt)
