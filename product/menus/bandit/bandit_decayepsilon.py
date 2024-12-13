import numpy as np 

class DecayEpsilonGreedy:
    def __init__(self, num_arms, epsilon, decay, decay_interval):
        self.num_arms = num_arms
        self.epsilon = epsilon
        self.decay = decay # reducing the value of epsilon
        self.decay_interval = decay_interval # interval which decay is applied
        
        # Used for resetting simulations
        self.initial_epsilon = epsilon
        self.initial_decay = decay
        self.initial_decay_interval = decay_interval

        self.count = np.zeros(num_arms)
        self.mean = np.zeros(num_arms)
        self.total_per_arm = np.zeros(num_arms) 
        self.total_rewards = 0 
    # Resetting function, includes epsilon and decay since every 
    # simulation the epsilon needs to reset 
    def reset(self):
        self.count = np.zeros(self.num_arms) 
        self.mean = np.zeros(self.num_arms) 
        self.total_per_arm = np.zeros(self.num_arms) 
        self.total_rewards = 0 
        self.epsilon = self.initial_epsilon
        self.decay = self.initial_decay
        self.decay_interval = self.initial_decay_interval

    # apply decay epsilon-greedy algorithm to select arm
    def select_arm(self):
        # exploration: select a random arm
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.num_arms)
        
        # exploitation: choose arm with the highest estimated mean value
        else:
            return np.argmax(self.mean)
        
    def update(self, arm, reward):
        self.count[arm] += 1 
        self.total_rewards += reward 
        self.total_per_arm[arm] += reward 
        # incremental update to mean without storing past results
        self.mean[arm] = self.mean[arm] + (1 / self.count[arm]) * (reward - self.mean[arm])  