import copy

import numpy.random as random
from BayesianNode import BayesianNode
from BayesianNetwork import BayesianNetwork


class ApproximateInference:
    def gibbsAsk(self, X, e, bnet: BayesianNetwork, n):
        # --- Create first sample ---
        sample_list = []
        sample = copy.deepcopy(e)
        frontier = []

        # add root nodes to frontier
        for node in bnet.network.values():
            if len(node.parents) == 0:
                frontier.append(node)  # add the nodes with no parents to the current network level

        # sample root nodes
        root_nodes = copy.copy(frontier)
        for node in root_nodes:
            sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)

        # while there are nodes to sample
        while len(frontier) > 0:
            for node in frontier:  # for each of the frontier nodes
                if e.get(node.name) is None:  # if the node is not in the evidence
                    s_flag = True  # set the sample flag true by default
                    for p in node.parents:  # check each parent of the node
                        if p not in sample:  # if the parent has not been sampled yet
                            s_flag = False  # set the sample flag for the current node to false
                    if s_flag:  # if all parents have been sampled
                        sample, frontier = self.sample_node(node, bnet, sample, sample, frontier)  # sample the node

        # add the sample to the list
        sample_list.append(sample)

        # --- Create N-1 more samples ---
        for i in range(n - 1):
            sample = copy.deepcopy(e)
            frontier = []
            # add root nodes to frontier
            for node in bnet.network.values():
                if len(node.parents) == 0:
                    frontier.append(node)  # add the nodes with no parents to the current network level

            # sample root nodes
            for node in frontier:
                sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)

            # while there are nodes to sample
            while len(frontier) > 0:
                for node in frontier:  # for each of the frontier nodes
                    if e.get(node.name) is None:  # if the node is not in the evidence
                        s_flag = True  # set the sample flag true by default
                        for p in node.parents:  # check each parent of the node
                            if p not in sample:  # if the parent has not been sampled yet
                                s_flag = False  # set the sample flag for the current node to false
                        if s_flag:  # sample the node according to the sample flag
                            sample, frontier = self.sample_node(node, bnet, sample, sample_list[i], frontier)  # sample

            # save the sample
            sample_list.append(sample)

        # --- Combine sample values ---
        probabilities = []
        for variable in X:
            states = []
            for state in bnet.network[variable].states:
                states.append(0)
            for sample in sample_list:
                if sample[variable] == 'TRUE':
                    states[0] += 1
                elif sample[variable] == 'FALSE':
                    states[1] += 1
                elif sample[variable] == 'ZERO':
                    states[0] += 1
                elif sample[variable] == 'LOW':
                    if len(states) == 4:
                        states[1] += 1
                    else:
                        states[0] += 1
                elif sample[variable] == 'NORMAL':
                    if len(states) == 4:
                        states[2] += 1
                    elif variable == 'INTUBATION':
                        states[0] += 1
                    else:
                        states[1] += 1
                elif sample[variable] == 'HIGH':
                    if len(states) == 4:
                        states[3] += 1
                    else:
                        states[2] += 1
            for i in range(len(states)):
                states[i] /= n
            probabilities.append(states)
        return probabilities

    def sample_node(self, node: BayesianNode, bnet: BayesianNetwork, cur_sample, prev_sample, frontier):
        if len(node.parents) == 0:  # if the node has no parents
            s_val = random.choice(node.states, 1, p=node.probabilities["table"])
        else:
            p_vals = ()  # parent node values
            for p in node.parents:  # for each parent of the current node
                p_vals += (prev_sample.get(p),)  # add parent value from sample
            denom = sum(float(prob) for prob in node.probabilities[p_vals])  # get denominator to normalize distribution
            p = ()
            for prob in node.probabilities[p_vals]:
                p += (float(prob) / denom,)
            s_val = random.choice(node.states, 1, p=p)  # choose a state based on probabilities
        cur_sample[node.name] = s_val[0]  # add the sampled value to the set
        for child in node.children:  # for each child of the sampled node
            if bnet.network[child] not in frontier:
                frontier.append(bnet.network[child])  # add the child to the frontier
        frontier.remove(node)  # remove the sampled node from the frontier
        for node in frontier:
            if node.name in cur_sample:
                frontier.remove(node)
        return cur_sample, frontier
