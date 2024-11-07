from menus.bandit.bandit_ucb import UpperConfidenceBound
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np


class SimulateUCB:
    def __init__(self):

        probabilities = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        num_arms = len(probabilities)
        temperature = 0.7 # balance between exploration and exploitation 
        iterations = 1000

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        upper_confidence = UpperConfidenceBound(num_arms,temperature)


        #Loop through num of iterations 
        for i in range(iterations):
            arm = upper_confidence.select_arm(i)
            reward = bandit.pull(arm)

            upper_confidence.update(arm, reward)

            # illustration of the effects of the decay on the arm selection
            if (i + 1) % 200 == 0 and (i + 1) != iterations:
                mean_rewards = upper_confidence.mean
                pulls_per_arm = upper_confidence.count

                print(f"""After {i + 1} iterations -> Estimated Mean rewards per arm:{np.round(mean_rewards,3)} Total pulls per arm:{pulls_per_arm}\n""")

        join_mean_rewards = ', '.join([f"{x:.2f}" for x in mean_rewards]) # format each value in the array to string with 2f
        join_confidence_bound = ', '.join([f"{x:.3f}" for x in upper_confidence.ucb_value]) # format each value in the array to string with 3f
        
        # Important information - for further analysis later 
        print(f"Final total rewards: {upper_confidence.total_rewards}")
        print(f"Final total rewards per arm: {upper_confidence.total_per_arm}")
        print(f"Total number of times each arm pulled: {pulls_per_arm}\n")

        print(f"UCB score: {join_confidence_bound}")    
        print(f"Final estimated Mean of each arm: {join_mean_rewards}") 