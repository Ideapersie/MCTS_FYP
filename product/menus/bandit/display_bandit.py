from menus.bandit.simulate_random import SimulateRandom
from menus.bandit.simulate_egreedy import SimulateEGreedy
from menus.bandit.simulate_decayepsilon import SimulateDecayEpsilon
from menus.bandit.simulate_ucb import SimulateUCB

def display_bandit():
    while True:
        print("\nTest bandit algorithm\n")
        print("1) Random Selection")
        print("2) Epsilon-greedy")
        print("3) Decay Epsilon")
        print("4) Upper Confidence Bound")
        print("5) Back to main menu")

        user_input = input("\nEnter choice: ")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            SimulateRandom().plot_results()

        elif user_input == '2':
            SimulateEGreedy().plot_results()

        elif user_input == '3':
            SimulateDecayEpsilon().plot_results()

        elif user_input == '4':
            SimulateUCB().plot_results()

        elif user_input == '5':
            print("Returning to main menu....")
            break

        else: 
            print("Error, please try again")

        