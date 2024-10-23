from menus.bandit_environment import MultiArmedBanditEnv
from menus.bandit_random import RandomSelect

class SimulateRandom:
    def __init__(self):

        probabilities = [0.2,0.5,0.8]
        num_arms = len(probabilities)

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilities)

        # initialise random selection 
        random_selection = RandomSelect(num_arms)

        iterations = 1000


        #Loop through num of iterations 
        for i in range(iterations):
            arm = random_selection.select_arm()
            reward = bandit.pull(arm)

            random_selection.update(arm,reward)

        print(f"\nfinal total rewards per arm: {random_selection.total_rewards}")
        print(f"final estimated value of each arm: {random_selection.mean}") 
        print(f"total number of times each arm pulled: {random_selection.count}")