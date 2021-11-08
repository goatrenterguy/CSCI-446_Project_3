import copy

import numpy.random as random
from BayesianNode import BayesianNode
from BayesianNetwork import BayesianNetwork


class ApproximateInference:
    def gibbsAsk(self, X, e, bnet: BayesianNetwork, n):
        # --- Create first sample ---
        sample_list = []  # list of samples
        sample = copy.deepcopy(e)  # first sample, initialized with evidence
        frontier = []  # frontier nodes to explore
        root_nodes = []

        # add root nodes to frontier
        for node in bnet.network.values():
            if len(node.parents) == 0:
                if node.name not in e:
                    frontier.append(node)  # add the nodes with no parents to the frontier
                    root_nodes.append(node)
                else:
                    [frontier.append(bnet.network[child]) for child in node.children]

        # sample root nodes
        for node in root_nodes:
            sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)

        # while there are nodes to sample
        while len(frontier) > 0:
            for node in frontier:  # for each of the frontier nodes
                if e.get(node.name) is None:  # if the node is not in the evidence
                    s_flag = True  # set the sample flag true by default
                    for parent in node.parents:  # check each parent of the node
                        if parent not in sample:  # if the parent has not been sampled yet
                            s_flag = False  # set the sample flag for the current node to false
                    if s_flag:  # if all parents have been sampled
                        sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)  # sample the node

        # add the sample to the list
        sample_list.append(sample)

        # --- Create N-1 more samples ---
        for i in range(n - 1):
            sample = copy.deepcopy(e)
            frontier = []
            root_nodes = []
            # add root nodes to frontier
            for node in bnet.network.values():
                if len(node.parents) == 0:
                    if node.name not in e:
                        frontier.append(node)  # add the nodes with no parents to the frontier
                        root_nodes.append(node)
                    else:
                        [frontier.append(bnet.network[child]) for child in node.children]

            # sample root nodes
            for node in root_nodes:
                sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)

            # while there are nodes to sample
            while len(frontier) > 0:
                for node in frontier:  # for each of the frontier nodes
                    if e.get(node.name) is None:  # if the node is not in the evidence
                        s_flag = True  # set the sample flag true by default
                        for parent in node.parents:  # check each parent of the node
                            if parent not in sample:  # if the parent has not been sampled yet
                                s_flag = False  # set the sample flag for the current node to false
                        if s_flag:  # sample the node according to the sample flag
                            sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)  # sample

            # save the sample
            sample_list.append(sample)

        # --- Combine sample values ---
        results = []
        for var in X:  # for each of the query variables
            values = []  # set of observed values
            for sample in sample_list:
                values.append(sample[var])  # get the values for the query variable from each sample
            dist = []  # probability distribution
            for state in bnet.network[var].states:  # for each of the possible states of the query variable
                count = 0  # initialize the value count
                for val in values:  # for each value gathered from the samples
                    if val == state:  # if the value matches the current state being counted
                        count += 1  # count the times each state is observed
                dist.append(str(state) + ": " + str(count / n))  # add the probability of observing the state to dist
            results.append(str(var) + ": " + str(dist))  # add the variable's distribution to the result set
        return results

    def sample_node(self, node: BayesianNode, bnet: BayesianNetwork, cur_sample, prev_sample, frontier):
        if len(node.parents) == 0:  # if the node has no parents
            s_val = random.choice(node.states, 1, p=node.probabilities["table"])  # get the probabilities
        else:
            p_vals = ()  # parent node values
            for parent in node.parents:  # for each parent of the current node
                p_vals += (prev_sample.get(parent),)  # add parent value from sample
            p = self.normalize_distribution(node, p_vals)  # normalize distribution
            s_val = random.choice(node.states, 1, p=p)  # choose a state based on probabilities
        cur_sample[node.name] = s_val[0]  # add the sampled value to the set
        for child in node.children:  # for each child of the sampled node
            if bnet.network[child] not in frontier:
                frontier.append(bnet.network[child])  # add the child to the frontier
        frontier.remove(node)  # remove the sampled node from the frontier
        frontier_nodes = copy.copy(frontier)  # create a copy of the frontier for iterating over
        for node in frontier_nodes:  # for each node in the frontier
            if node.name in cur_sample:  # if the node has been sampled already
                frontier.remove(node)  # remove it from the frontier
        return cur_sample, frontier  # return the updated sample and frontier

    # Utility method for normalizing probability distributions that don't add to 1 (i.e. [0.33, 0.33, 0.33])
    @staticmethod
    def normalize_distribution(node, p_vals):
        denom = sum(float(prob) for prob in node.probabilities[p_vals])  # get denominator to normalize distribution
        p = ()  # normalized distribution
        for prob in node.probabilities[p_vals]:  # for each probability
            p += (float(prob) / denom,)  # add the normalized probability to the distribution
        return p
