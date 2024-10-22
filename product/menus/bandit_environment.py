import numpy as np 

class MultiArmedBanditEnv:
    # List of probabilties for each arm 
    def __init__(self, probabilities):
        self.probabilities = probabilities

    def pull(self,arm):
        if np.random.rand() < self.probabilities[arm]:
            return 1 
        return 0