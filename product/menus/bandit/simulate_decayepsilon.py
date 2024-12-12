from menus.bandit.bandit_decayepsilon import DecayEpsilonGreedy
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np

class SimulateDecayEpsilon:
    def __init__(self):

        # Probabilities from 0% to 99% win rate
        probabilities = np.arange(0.0,1.00,0.01)
        num_arms = len(probabilities)
        # Specific variables for decay strategy
        epsilon = 0.35
        decay = 0.8
        decay_interval = 200

        # initialise env bandit
        self.bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        self.decay_epsilon = DecayEpsilonGreedy(num_arms, epsilon, decay, decay_interval)
        self.iterations = 1000
        self.simulation = 10

    def run_simulation(self):
        all_rewards = []
        all_counts = []
        all_means = []
        
        # New simulation
        for x in range(self.simulation):
            # Resets the environment for each simulation run, including epsilon and decay
            self.decay_epsilon.reset()
            
            #Loop through num of iterations 
            for i in range(self.iterations):
                arm = self.decay_epsilon.select_arm()
                reward = self.bandit.pull(arm)

                self.decay_epsilon.update(arm, reward)

                # applying the decaying of the epsilon value, less exploration (resetted every simulation)
                if i % self.decay_epsilon.decay_interval == 0:
                    self.decay_epsilon.epsilon = self.decay_epsilon.epsilon * self.decay_epsilon.decay

                # illustration of the effects of the decay on the arm selection
                if (i + 1) % 200 == 0 and (i + 1) != self.iterations and x == (self.simulation - 1):
                    mean_rewards = self.decay_epsilon.mean
                    pulls_per_arm = self.decay_epsilon.count

                    print(f"""After {i + 1} iterations -> Estimated Mean rewards per arm:{np.round(mean_rewards,2)} Total pulls per arm:{pulls_per_arm}\n""")
             
            # Printing total results from last simulation
            if x == (self.simulation - 1):
                # Important information - for further analysis later 
                print(f"Final total rewards: {self.decay_epsilon.total_rewards}")
                print(f"Final total rewards per arm: {self.decay_epsilon.total_per_arm}")
                print(f"Total number of times each arm pulled: {pulls_per_arm}\n")

                join_mean_rewards = ', '.join([f"{x:.2f}" for x in mean_rewards]) # format each value in the array to string with 3f
                print(f"Final estimated Mean of each arm: {join_mean_rewards}") 
        
            # Store the rewards and counts for each simultion   
            all_rewards.append(self.decay_epsilon.total_per_arm.copy())  # Per-arm rewards
            all_counts.append(self.decay_epsilon.count.copy()) # Total pulls per arm
            all_means.append(self.decay_epsilon.mean.copy()) # Estimated probability


        return np.array(all_rewards), np.array(all_counts), np.array(all_means)

    def plot_results(self):
        # %%
        import matplotlib.pyplot as plt
        from menus.bandit.plot_utils import plot_simulation_results
        
        # Run simulation to gather rewards and counts
        all_rewards, all_counts, all_means = self.run_simulation()

        # Plot the simulation results
        plot_simulation_results(all_rewards, all_counts, all_means, algorithm_name="Decay Epsilon")
        plt.show()

if __name__ == "__main__":
    SimulateDecayEpsilon.plot_results()