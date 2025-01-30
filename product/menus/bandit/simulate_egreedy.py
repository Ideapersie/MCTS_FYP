from menus.bandit.bandit_egreedy import EpsilonGreedy
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np

class SimulateEGreedy:
    def __init__(self):

        # Probabilities from 0% to 99% win rate
        probabilities = np.arange(0.0,1.00,0.01)
        num_arms = len(probabilities)
        epsilon = 0.6

        # initialise env bandit
        self.bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        self.epsilon_selection = EpsilonGreedy(num_arms, epsilon)
        self.iterations = 1000
        self.simulation = 10
        
    def run_simulation(self):
        all_rewards = []
        all_counts = []
        all_means = []
        
        # New simulation
        for x in range(self.simulation):
            # Resets the environment for each simulation run 
            self.epsilon_selection.reset()
            # Loop through num of self.iterations 
            for i in range(self.iterations):
                arm = self.epsilon_selection.select_arm()
                reward = self.bandit.pull(arm)

                self.epsilon_selection.update(arm, reward)

                # Print mean_rewards and pull every 200 iterations and only on the last simulation 
                if (i + 1) % 200 == 0 and (i + 1) != self.iterations and x == (self.simulation-1):
                    mean_rewards = self.epsilon_selection.mean
                    pulls_per_arm = self.epsilon_selection.count

                    #print(f"""After {i + 1} self.iterations -> Estimated Mean rewards per arm: {np.round(mean_rewards,2)} Total pulls per arm:{pulls_per_arm}\n""")
                    
            # Store the rewards and counts for each simultion   
            all_rewards.append(self.epsilon_selection.total_per_arm.copy())  # Per-arm rewards
            all_counts.append(self.epsilon_selection.count.copy()) # Pulls pers arm 
            all_means.append(self.epsilon_selection.mean.copy()) # Estimated probability per-arm

            if x == (self.simulation - 1):
                # Important information - for further analysis later 
                print(f"Final total rewards: {self.epsilon_selection.total_rewards}")
                
                #print(f"Final total rewards per arm: {self.epsilon_selection.total_per_arm}")
                #print(f"Total number of times each arm pulled: {pulls_per_arm}\n")

                #join_mean_rewards = ', '.join([f"{x:.2f}" for x in mean_rewards]) # format each value in the array to string with 3f
                #print(f"Final estimated Mean of each arm: {join_mean_rewards}") 
                
        return np.array(all_rewards), np.array(all_counts), np.array(all_means)

    def plot_results(self):
        # %%
        import matplotlib.pyplot as plt
        from menus.bandit.plot_utils import plot_simulation_results
        

        # Run simulation to gather rewards and counts
        all_rewards, all_counts, all_means = self.run_simulation()

        # Plot the simulation results
        plot_simulation_results(all_rewards, all_counts, all_means, algorithm_name="Epsilon Greedy")
        plt.show()

if __name__ == "__main__":
    SimulateEGreedy.plot_results()
# %%
