from menus.bandit.bandit_decayepsilon import DecayEpsilonGreedy
from menus.bandit.bandit_environment import MultiArmedBanditEnv
import numpy as np

class SimulateDecayEpsilon:
    def __init__(self):

        probabilities = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        num_arms = len(probabilities)
        epsilon = 0.35
        decay = 0.8
        decay_interval = 200

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        decay_epsilon = DecayEpsilonGreedy(num_arms, epsilon, decay, decay_interval)

        iterations = 1000


        #Loop through num of iterations 
        for i in range(iterations):
            arm = decay_epsilon.select_arm()
            reward = bandit.pull(arm)

            decay_epsilon.update(arm, reward)

            # applying the decaying of the epsilon value, less exploration 
            if i % decay_interval == 0:
                decay_epsilon.epsilon = decay_epsilon.epsilon * decay

            # illustration of the effects of the decay on the arm selection
            if (i + 1) % 200 == 0 and (i + 1) != iterations:
                mean_rewards = decay_epsilon.mean
                pulls_per_arm = decay_epsilon.count

                print(f"""After {i + 1} iterations -> Estimated Mean rewards per arm:{np.round(mean_rewards,3)} Total pulls per arm:{pulls_per_arm}\n""")


        # Important information - for further analysis later 
        print(f"Final total rewards: {decay_epsilon.total_rewards}")
        print(f"Final total rewards per arm: {decay_epsilon.total_per_arm}")
        print(f"Total number of times each arm pulled: {pulls_per_arm}\n")

        join_mean_rewards = ', '.join([f"{x:.3f}" for x in mean_rewards]) # format each value in the array to string with 3f
        print(f"Final estimated Mean of each arm: {join_mean_rewards}") 