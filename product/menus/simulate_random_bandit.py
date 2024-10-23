from menus.bandit_environment import MultiArmedBanditEnv
from menus.bandit_random import Random_select

class Simulate_random:
    def __init__(self):

        probabilites = [0.2,0.5,0.8]
        num_arms = len(probabilites)

        # initialise env bandit
        bandit = MultiArmedBanditEnv(probabilites)

        # initialise random selection 
        random_selection = Random_select(num_arms)

        iterations = 1000


        #Loop through num of iterations 
        for i in range(iterations):
            arm = random_selection.select_arm()
            reward = bandit.pull(arm)

            random_selection.update(arm,reward)

        print(f"\nfinal total rewards per arm: {random_selection.total_rewards}")
        print(f"final estimated value of each arm: {random_selection.mean}") 
        print(f"total number of times each arm pulled: {random_selection.count}")