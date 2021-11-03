class ApproximateInference:
    def gibbsAsk(self, X, e, bnet: BayesianNetwork, N):
        # --- Create first sample ---
        sample = Sample()
        currentLevel = {}
        while True:
            # get the root nodes
            for node in bnet.network:
                if len(node.parents) == 0:
                    currentLevel.add(node)  # add the nodes with no parents to the current network level
            # sample each of the parent nodes
            for node in currentLevel:
                # select sample value from table
                # select the right probability table
                parentValues = ()  # parent node values
                for parent in node.parents:  # for each parent of the current node
                    parentValues = parentValues + (sample.get(parent.name))  # add parent value from sample
                probability = node.probabilities[parentValues]  # get probabilities given the parents
                choice = random.choose(node.states, probability)  # choose a state based on probabilities
                sample.addNode(node.name, choice)  # add the sampled value to the set
            # gather children of current nodes
            nextLevel = {}
            for node in currentLevel:
                for child in node.children
                    nextLevel.add(child)
            # break if there are no children
            if len(nextLevel) == 0:
                break
            # set the current level to the next set of nodes
            currentLevel = nextLevel

        # --- Create N-1 samples ---

        pass

    def markovBlanket(self, X, BNet):
        pass