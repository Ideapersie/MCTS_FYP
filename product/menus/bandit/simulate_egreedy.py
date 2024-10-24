from bandit.bandit_egreedy import EpsilonGreedy
from bandit.bandit_environment import MultiArmedBanditEnv

class SimulateEGreedy:
    def __init__(self):

        probabilities = [0.2,0.5,0.8]
        num_arms = len(probabilities)
        epsilon = 0.13

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilities)

        # initialise E-greedy selection & variables
        epsilon_selection = EpsilonGreedy(num_arms, epsilon)
        mean_rewards = epsilon_selection.mean
        pulls_per_arm = epsilon_selection.count

        iterations = 1000


        #Loop through num of iterations 
        for i in range(iterations):
            arm = epsilon_selection.select_arm()
            reward = bandit.pull(arm)

            epsilon_selection.update(arm, reward)

            if (i + 1) % 200 == 0 and (i + 1) != iterations:
                print(f"""After {i + 1} iterations:, \nEstimated Mean rewards per arm:{mean_rewards} Total pulls per arm:{pulls_per_arm}\n""")


        # Unessential results
        print(f"Final total rewards: {epsilon_selection.total_rewards}")
        print(f"Final total rewards per arm: {epsilon_selection.total_per_arm}\n")

        print(f"Final estimated Mean of each arm: {mean_rewards}") 
        print(f"Total number of times each arm pulled: {pulls_per_arm}")