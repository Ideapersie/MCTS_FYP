import numpy as np

class Random_select:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.count = np.zeros(num_arms) # times each arms has been selected
        self.mean = np.zeros(num_arms) # mean using new formula 
        self.total_rewards = np.zeros(num_arms) # total rewards for each arm 

    # select an arm randomly
    def select_arm(self):
        return np.random.randint(0,self.num_arms)
    
    # updates number of times an arm has been pulled, total and average reward per arm
    def update(self, arm, reward):
        self.count[arm]+=1
        self.total_rewards[arm] += reward 
        # incremental update to mean without storing past results
        self.mean[arm] = self.mean[arm] + (1 / self.count[arm]) * (reward - self.mean[arm]) 

        
    
    
