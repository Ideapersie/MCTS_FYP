from menus.bandit.bandit_egreedy import EpsilonGreedy
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np

class SimulateEGreedy:
    def __init__(self):

        probabilities = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        num_arms = len(probabilities)
        epsilon = 0.2

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        epsilon_selection = EpsilonGreedy(num_arms, epsilon)
        iterations = 1000


        # Loop through num of iterations 
        for i in range(iterations):
            arm = epsilon_selection.select_arm()
            reward = bandit.pull(arm)

            epsilon_selection.update(arm, reward)

            if (i + 1) % 200 == 0 and (i + 1) != iterations:
                mean_rewards = epsilon_selection.mean
                pulls_per_arm = epsilon_selection.count

                print(f"""After {i + 1} iterations -> Estimated Mean rewards per arm: {np.round(mean_rewards,3)} Total pulls per arm:{pulls_per_arm}\n""")


        # Important information - for further analysis later 
        print(f"Final total rewards: {epsilon_selection.total_rewards}")
        print(f"Final total rewards per arm: {epsilon_selection.total_per_arm}")
        print(f"Total number of times each arm pulled: {pulls_per_arm}\n")

        join_mean_rewards = ', '.join([f"{x:.3f}" for x in mean_rewards]) # format each value in the array to string with 3f
        print(f"Final estimated Mean of each arm: {join_mean_rewards}") 