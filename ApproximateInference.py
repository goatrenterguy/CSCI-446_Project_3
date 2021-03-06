import copy

import numpy.random as random
from BayesianNode import BayesianNode
from BayesianNetwork import BayesianNetwork


class ApproximateInference:
    def __init__(self):
        self.count = 0

    def gibbsAsk(self, X, e, bnet: BayesianNetwork, n, demo_flag):
        # --- Create first sample ---
        sample_list = []  # list of samples
        sample = copy.deepcopy(e)  # first sample, initialized with evidence
        frontier = []  # frontier nodes to explore
        root_nodes = []  # set of root nodes for beginning the sample

        # add root nodes to frontier
        for node in bnet.network.values():
            self.count += 1
            if len(node.parents) == 0:  # if the node is a root
                if node.name not in e:  # if the node is not in the evidence
                    frontier.append(node)  # add the nodes with no parents to the frontier
                    root_nodes.append(node)  # add the nodes with no parents to the root nodes
                else:  # if the node is in the evidence
                    [frontier.append(bnet.network[child]) for child in node.children]  # sample the node

        # sample root nodes
        for node in root_nodes:
            self.count += 1
            sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)

        # while there are nodes to sample
        while len(frontier) > 0:
            for node in frontier:  # for each of the frontier nodes
                self.count += 1
                if e.get(node.name) is None:  # if the node is not in the evidence
                    s_flag = True  # set the sample flag true by default
                    for parent in node.parents:  # check each parent of the node
                        self.count += 1
                        if parent not in sample:  # if the parent has not been sampled yet
                            s_flag = False  # set the sample flag for the current node to false
                    if s_flag:  # if all parents have been sampled
                        sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)  # sample the node

        # add the sample to the list
        sample_list.append(sample)

        # --- Create N-1 more samples ---
        for i in range(n - 1):
            self.count += 1
            sample = copy.deepcopy(e)
            frontier = []
            root_nodes = []
            # add root nodes to frontier
            for node in bnet.network.values():
                self.count += 1
                if len(node.parents) == 0:  # if the node is a root
                    if node.name not in e:  # if the node is not in the evidence
                        frontier.append(node)  # add the nodes with no parents to the frontier
                        root_nodes.append(node)  # add the nodes to the root_node list too
                    else:  # if the node is in the evidence
                        [frontier.append(bnet.network[child]) for child in node.children]  # add children to frontier

            # sample root nodes
            for node in root_nodes:
                self.count += 1
                sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)

            # while there are nodes to sample
            while len(frontier) > 0:
                for node in frontier:  # for each of the frontier nodes
                    self.count += 1
                    if e.get(node.name) is None:  # if the node is not in the evidence
                        s_flag = True  # set the sample flag true by default
                        for parent in node.parents:  # check each parent of the node
                            self.count += 1
                            if parent not in sample:  # if the parent has not been sampled yet
                                s_flag = False  # set the sample flag for the current node to false
                        if s_flag:  # sample the node according to the sample flag
                            sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)  # sample

            # save the sample
            sample_list.append(sample)
        if demo_flag:
            for s in sample_list:
                print(s)

        # --- Combine sample values ---
        results = []
        for var in X:  # for each of the query variables
            self.count += 1
            values = []  # set of observed values
            for sample in sample_list:
                self.count += 1
                values.append(sample[var])  # get the values for the query variable from each sample
            dist = []  # probability distribution
            for state in bnet.network[var].states:  # for each of the possible states of the query variable
                self.count += 1
                count = 0  # initialize the value count
                for val in values:  # for each value gathered from the samples
                    self.count += 1
                    if val == state:  # if the value matches the current state being counted
                        count += 1  # count the times each state is observed
                dist.append(str(state) + ": " + str(count / n))  # add the probability of observing the state to dist
            results.append(str(var) + ": " + str(dist))  # add the variable's distribution to the result set
            print(str(var) + ' count ' + str(self.count))
            self.count = 0
        return results

    def sample_node(self, node: BayesianNode, bnet: BayesianNetwork, cur_sample, prev_sample, frontier):
        if len(node.parents) == 0:  # if the node has no parents
            s_val = random.choice(node.states, 1, p=node.probabilities["table"])  # get the probabilities
        else:
            p_vals = ()  # parent node values
            for parent in node.parents:  # for each parent of the current node
                self.count += 1
                p_vals += (prev_sample.get(parent),)  # add parent value from sample
            p = self.normalize_distribution(node, p_vals)  # normalize distribution
            s_val = random.choice(node.states, 1, p=p)  # choose a state based on probabilities
        cur_sample[node.name] = s_val[0]  # add the sampled value to the set
        for child in node.children:  # for each child of the sampled node
            self.count += 1
            if bnet.network[child] not in frontier:
                frontier.append(bnet.network[child])  # add the child to the frontier
        frontier.remove(node)  # remove the sampled node from the frontier
        frontier_nodes = copy.copy(frontier)  # create a copy of the frontier for iterating over
        for node in frontier_nodes:  # for each node in the frontier
            self.count += 1
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
