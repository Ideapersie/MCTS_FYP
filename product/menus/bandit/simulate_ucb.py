from menus.bandit.bandit_ucb import UpperConfidenceBound
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np


class SimulateUCB:
    def __init__(self):

        # Probabilities from 0% to 99% win rate
        probabilities = np.arange(0.0,1.00,0.01)
        num_arms = len(probabilities)
        temperature = 0.49 # balance between exploration and exploitation 
        
        # No. of iterations per simulation 
        self.iterations = 1000
        # No. of simulations for graph results 
        self.simulation = 10

        # initialise env bandit
        self.bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        self.upper_confidence = UpperConfidenceBound(num_arms,temperature)
        
    def run_simulation(self):
        all_rewards = []
        all_counts = []
        all_means = []
        
        # New simulation
        for x in range(self.simulation):
            # Resets the environment for each simulation run 
            self.upper_confidence.reset()
            # Loop through num of self.iterations 
            for i in range(self.iterations):
                arm = self.upper_confidence.select_arm(i)
                reward = self.bandit.pull(arm)

                self.upper_confidence.update(arm, reward)

                if (i + 1) % 200 == 0 and (i + 1) != self.iterations and x == (self.simulation-1):
                    mean_rewards = self.upper_confidence.mean
                    pulls_per_arm = self.upper_confidence.count

                    #print(f"""After {i + 1} iterations -> Estimated Mean rewards per arm:{np.round(mean_rewards,2)} Total pulls per arm:{pulls_per_arm}\n""")

                    
            # Store the rewards and counts for each simultion   
            all_rewards.append(self.upper_confidence.total_per_arm.copy())  # Per-arm rewards
            all_counts.append(self.upper_confidence.count.copy())           # Per-arm counts
            all_means.append(self.upper_confidence.mean.copy()) 

            # Final results for last simulation
            if x == (self.simulation - 1):
                #join_mean_rewards = ', '.join([f"{x:.2f}" for x in mean_rewards]) # format each value in the array to string with 2f
                #join_confidence_bound = ', '.join([f"{x:.3f}" for x in self.upper_confidence.ucb_value]) # format each value in the array to string with 3f
                
                print(f"Final total rewards: {self.upper_confidence.total_rewards}")
                #print(f"Final total rewards per arm: {self.upper_confidence.total_per_arm}")
                #print(f"Total number of times each arm pulled: {pulls_per_arm}")
                #print(f"Final estimated Mean of each arm: {join_mean_rewards}\n") 
                
                # Important information - for further analysis later 
                #print(f"UCB score: {join_confidence_bound}")    
                 
                
        return np.array(all_rewards), np.array(all_counts), np.array(all_means)

    def plot_results(self):
        # %%
        import matplotlib.pyplot as plt
        from menus.bandit.plot_utils import plot_simulation_results
        
        # Run simulation to gather rewards and counts
        all_rewards, all_counts, all_means = self.run_simulation()

        # Plot the simulation results
        plot_simulation_results(all_rewards, all_counts, all_means, algorithm_name="UCB score")
        plt.show()

if __name__ == "__main__":
    SimulateUCB.plot_results()
        