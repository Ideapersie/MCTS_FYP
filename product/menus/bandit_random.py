import numpy as np

class Random_select:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.count = np.zeros(num_arms) # times each arms has been selected
        self.mean = np.zeros(num_arms) # mean value of each arm 
        self.total_rewards = np.zeros(num_arms) # total rewards for each arm 

    def select_arm(self):
        #select an arm randomly
        return np.random.randint(0,self.num_arms)
    
    def update(self, arm, reward):

        
        self.count[arm]+=1
        self.total_rewards[arm] += reward 

    def average(self, arm):
        self.mean[arm] =  (self.total_rewards[arm] / self.count[arm])
        
    
    
