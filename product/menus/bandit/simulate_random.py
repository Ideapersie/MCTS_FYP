from menus.bandit.bandit_environment import MultiArmedBanditEnv
from menus.bandit.bandit_random import RandomSelect
from menus.bandit.plot_utils import plot_simulation_results
import numpy as np


class SimulateRandom:
    def __init__(self):

        probabilities = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        num_arms = len(probabilities)

        # Initialise env bandit
        self.bandit = MultiArmedBanditEnv(probabilities)

        # Initialise random selection 
        self.random_selection = RandomSelect(num_arms)

        # Number of game iterations per simulation
        self.iterations = 1000
        
        # Number of simulations for graphs
        self.simulations = 100

    def run_simulation(self):
        all_rewards = []
        all_counts = []
        all_means = []
        # New simulation
        for x in range(self.simulations):
            # Resets the environment for each simulation run 
            #self.random_selection.reset
            self.random_selection.reset()
            
            # Run each simulation with given no. of iterations  
            for _ in range(self.iterations):
                arm = self.random_selection.select_arm()
                reward = self.bandit.pull(arm)
                self.random_selection.update(arm,reward)
            
            # Store the rewards and counts for each simultion   
            all_rewards.append(self.random_selection.total_per_arm.copy()) # Per arm rewards
            all_counts.append(self.random_selection.count.copy())  # pulls per arm 
            all_means.append(self.random_selection.mean.copy()) # estimated probability per-arm
    
                
            # Print the stats for the last simulation 
            if x == (self.simulations-1):
                # differentiate between total rewards and total per arm
                print(f"\nFinal total rewards: {self.random_selection.total_rewards}")
                print(f"Final total rewards per arm: {self.random_selection.total_per_arm}\n")
                print(f"Total number of times each arm pulled: {self.random_selection.count}")
                
                join_mean_rewards = ', '.join([f"{x:.2f}" for x in self.random_selection.mean]) # format each value in the array to string with 3f
                print(f"Final estimated Mean of each arm: {join_mean_rewards}") 
        
        return np.array(all_rewards), np.array(all_counts), np.array(all_means)

    def plot_results(self):  
        # %%
        import matplotlib.pyplot as plt
        from menus.bandit.plot_utils import plot_simulation_results
        
        # Run simulation to collect total rewards and counts
        all_rewards, all_counts, all_means = self.run_simulation()

        # Plot the simulation results
        plot_simulation_results(all_rewards, all_counts, all_means, algorithm_name="Random Selection")
        plt.show()

if __name__ == "__main__":
    SimulateRandom().plot_results()
        

# %%
