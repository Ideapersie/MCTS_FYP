import numpy as np

class RandomSelect:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.count = np.zeros(num_arms) # times each arms has been selected
        self.mean = np.zeros(num_arms) # mean using new formula 
        self.total_per_arm = np.zeros(num_arms) # total rewards for each arm
        self.total_rewards = 0 # total rewards  

    # select an arm randomly
    def select_arm(self):
        return np.random.randint(0,self.num_arms)
    
    # updates number of times an arm has been pulled, total and average reward per arm
    def update(self, arm, reward):
        self.count[arm]+=1
        self.total_per_arm[arm] += reward 
        self.total_rewards += reward
        # incremental update to mean without storing past results
        self.mean[arm] = self.mean[arm] + (1 / self.count[arm]) * (reward - self.mean[arm]) 

        
    
    
