import random
from Objects import *
from BayesianNetwork import BayesianNetwork


class ExactInference:

    def __init__(self):
        self.count = 0
        self.demo = False

    def eliminationAsk(self, X, e, BNet: BayesianNetwork):
        """
        Variable Elimination algorithm for exact inference
        :param demo:
        :param X: A string that is the query
        :param e: A dictionary containg the evidence
        :param BNet: A Bayesian network
        :return: Returns the probability of X given the evidence
        """
        # Initialize a counter for steps in for loops
        factors = []
        # Loop to create all factors
        for var in BNet.getVariables():
            factors.append(self.makeFactor(var, e, BNet))
            self.count += 1
        # Loop to eliminate factors based on the order
        for var in self.order(BNet.getVariables(), BNet):
            # If var is equal to the query or is in the evidence do not sum out
            if var != X and var not in e:
                factors = self.sumOut(var, factors, BNet)
            self.count += 1
        # Do one final point wise product to consolidate remaining factors that contain the evidence and query
        finalFactor = self.pointWiseProduct(factors)
        cpt = {}
        indexVar = finalFactor.variables.index(X)
        for k in finalFactor.cpt:
            kl = [X for X in k]
            cpt[kl[indexVar]] = finalFactor.cpt[k]
        finalFactor.cpt = cpt
        print("Major loop iterations: " + str(self.count))
        # Return the normalized form of the distribution
        return self.normalize(finalFactor)

    def matchingVariables(self, f1, f2):
        """
        Auxililary function to find the common indices between two factors
        :param f1: Factor 1
        :param f2: Factor 2
        :return: A list of indices for where f1 and f2 share a variable
        """
        matchingVariables = []
        # Loop through f1's variables
        for fv in range(len(f1.variables)):
            self.count += 1
            # Loop through f2's variables
            for ov in range(len(f2.variables)):
                # If they are equal then add the indices to matchingVariables
                if f1.variables[fv] == f2.variables[ov]:
                    matchingVariables.append([fv, ov])
        # Return the list of matching variables
        return matchingVariables

    def pointWiseProduct(self, factors):
        """
        Function for computing the point wise product for the input factors
        :param factors: A list of factors that all have a common variable
        :return: Returns a single factor that is a combination of all input factors
        """
        # While there are more than one factors
        while len(factors) > 1:
            self.count += 1
            # Set the factors to merge
            f1 = factors[0]
            f2 = factors[1]
            # Get the matching factors between f1 and f2
            matchingVariables = self.matchingVariables(f1, f2)
            # If they have matching variables and they arnt equal to each other
            # (Probably can be removed should never happen)
            if matchingVariables and f1 != f2:
                # Remove f1 and f2 from factors so that they dont get marginalized again
                factors.remove(f1)
                factors.remove(f2)
                cpt = {}
                # Generate all the variables for the marginalized factors
                variables = f1.variables + [X for X in f2.variables if X not in f1.variables]
                # Iterate through the list of keys in f1
                for pf in f1.cpt:
                    # Create a list of from the key
                    pfl = [X for X in pf]
                    # Iterate through all the keys in f2
                    for po in f2.cpt:
                        # Create a list from the key
                        pol = [X for X in po]
                        # Create a copy of pfl for the key of the new cpt
                        key = pfl.copy()
                        # Initialize a variable to check there is a match and the product needs to be computed
                        match = True
                        # Initialize an empty list for the the indices of pol to be removed
                        remove = []
                        # Iterate through the list of matching variables
                        for mv in matchingVariables:
                            # If the variables do not match set match to false and break
                            if pfl[mv[0]] != pol[mv[1]]:
                                match = False
                                break
                            # Otherwise add the indices to be removed from POL
                            else:
                                remove.append(mv[1])
                        # If there is a match create the new CPT entry
                        if match:
                            # Create a list of indices that are not all ready merged
                            other = [pol[i] for i in range(len(pol)) if i not in remove]
                            # Add values to key
                            key += other
                            # Add the entry to CPT where the values were marginalized and calculate their value
                            cpt[tuple(key)] = f1.cpt[pf] * f2.cpt[po]
                # Add the new factor to the end of factors so it can be marginalized against
                factors.append(Factor(variables, cpt))
        # Return the single marginalized factor
        return Factor(factors[0].variables, factors[0].cpt)

    def sumOut(self, var, factors, BNet):
        """
        Function for summing out a variable from the set of factors
        :param var: A variable that is to be summed out
        :param factors: A list of factors
        :param BNet: A bayesian network
        :return: A list of factors where var has been summed out
        """
        keep = []
        varInFactor = []
        # Iterate through all factors and separate out the ones that contain var
        for f in factors:
            if var in f.variables:
                varInFactor.append(f)
            else:
                keep.append(f)
        # If there are any factors that contain var
        if len(varInFactor) > 0:
            # Calculate the point wise product for all the factors that
            factored = self.pointWiseProduct(varInFactor)
            # Get index of var
            indexVar = factored.variables.index(var)
            cpt = {}
            # Get a list of all keys in factored
            keys = list(factored.cpt.keys())
            # Get the number of states for the node
            nodeStates = len(BNet.getNode(var).states)
            # Iterate through the range of keys
            for k1i in range(len(keys)):
                self.count += 1
                # Initialize a counter
                count = 0
                # Iterate through the rest of keys
                for k2i in range(k1i, len(keys)):
                    self.count += 1
                    # Get the keys for each index
                    k1 = keys[k1i]
                    k2 = keys[k2i]
                    # Check if they keys are the exact same
                    if k1 != k2:
                        # Initialize a variable for matching
                        match = True
                        # Iterate through the key and check that only the index to be removed is different
                        for i in range(len(factored.variables)):
                            # If they index where they keys should be different is not then set match to False
                            if i != indexVar and k1[i] != k2[i]:
                                match = False
                        # If the indices match
                        if match:
                            # Increment count
                            count += 1
                            key = []
                            # Generate the new key excluding the index to be removed
                            for val in range(len(k1)):
                                if val != indexVar:
                                    key.append(k1[val])
                            # Check if the key already exists if so add to it
                            if tuple(key) in cpt:
                                # Add to the sum
                                cpt[tuple(key)] = cpt[tuple(key)] + factored.cpt[k2]
                            else:
                                # Add to the sum and create a new entry
                                cpt[tuple(key)] = factored.cpt[k1] + factored.cpt[k2]
                            # If the count equals the number of states we
                            # know that we have found all the keys so we can break
                            if count == nodeStates:
                                break
            factored.variables.remove(var)
            keep.append(Factor(factored.variables, cpt))
        return keep

    def normalize(self, factor):
        """
        Utility function to normalize probabilities
        :param factor: A factor to be normalized
        :return: The normalized factor
        """
        total = 0
        for k in factor.cpt:
            total += factor.cpt[k]
        for k in factor.cpt:
            factor.cpt[k] = factor.cpt[k] / total
        return factor

    def order(self, variables, BNet):
        """
        Function for generating the order to eliminate variables by
        :param variables: list of all variables
        :param BNet: Bayesian network
        :return: A of the names to ordered by the number of children the have
        """
        numChildren = []
        for v in variables:
            self.count += 1
            numChildren.append([v, len(BNet.getNode(v).children)])
        # Sort by the number of children
        numChildren.sort(key=lambda x: x[1], reverse=False)
        # Extract the names
        order = [v[0] for v in numChildren]
        # Return the list of names
        return order

    def makeFactor(self, var, evidence, BNet: BayesianNetwork):
        """
        Function to generate factors
        :param var: Name of node to generate factors for
        :param evidence: Dictionary of evidence
        :param BNet: Bayesian network
        :return: Return the factor of var
        """
        # Retrieve the node names var from BNet
        node = BNet.getNode(var)
        # Generate the list of all variables including the its self
        pFor = [var]
        e = node.parents
        variables = [x for x in node.parents + [var]]
        cpt = {}
        ignore = []
        for v in range(len(e)):
            if e[v] in evidence:
                variables.pop(v)
                ignore.append(v)
        # Iterate through the list of probabilities
        for p in node.probabilities:
            self.count += 1
            # Iterate through the number of states
            for i in range(len(node.states)):
                self.count += 1
                key = [X for X in p]
                take = True
                for v in ignore:
                    if key[v] != evidence[e[v]]:
                        take = False
                    key.pop(v)
                if take:
                    # If var is in evidence
                    if var in evidence:
                        # Only select the probabilities where the state matches what is in evidence
                        if evidence[var] == node.states[i]:
                            # If the probability contains table then replace it with the state of var
                            if p == "table":
                                cpt[(node.states[i],)] = float(node.probabilities[p][i])
                            # If it does not add the state of the variable to the existing states
                            else:
                                cpt[tuple(key) + (node.states[i],)] = float(node.probabilities[p][i])
                    else:
                        # If the probability contains table then replace it with the state of var
                        if p == "table":
                            cpt[(node.states[i],)] = float(node.probabilities[p][i])
                        # If it does not add the state of the variable to the existing states
                        else:
                            cpt[tuple(key) + (node.states[i],)] = float(node.probabilities[p][i])
        # Return a new Factor
        return Factor(variables, cpt)
