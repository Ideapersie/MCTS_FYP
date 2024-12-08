import numpy as np 
import math 

class UpperConfidenceBound:
    def __init__(self, num_arms, temperature):
        self.num_arms = num_arms
        self.temperature = temperature
        self.count = np.zeros(num_arms)
        self.mean = np.zeros(num_arms)
        self.total_per_arm = np.zeros(num_arms) # total rewards for each arm
        self.ucb_value = np.zeros(num_arms)
        self.total_rewards = 0
        
    def reset(self):
        self.count = np.zeros(self.num_arms) 
        self.mean = np.zeros(self.num_arms) 
        self.total_per_arm = np.zeros(self.num_arms) 
        self.total_rewards = 0 

    # apply UCB algorithm to select arm
    def select_arm(self, arm):
        # each arm has to be pulled once
        for arm in range(self.num_arms):
            if self.count[arm] == 0:
                return arm # return one which has not been pulled yet
         
        
        # calculating the upper confidence bound, higher temperature = more exploration 
        for arm in range(self.num_arms):
            confidence_bound = math.sqrt(2* math.log(sum(self.count))/self.count[arm])
            self.ucb_value[arm] = self.mean[arm] + self.temperature * confidence_bound


        # select arm with highest UCB value 
        return np.argmax(self.ucb_value)
        
    def update(self, arm, reward):
        self.count[arm] += 1 
        self.total_rewards += reward 
        self.total_per_arm[arm] += reward 
        # incremental update to mean without storing past results
        self.mean[arm] = self.mean[arm] + (1 / self.count[arm]) * (reward - self.mean[arm]) 