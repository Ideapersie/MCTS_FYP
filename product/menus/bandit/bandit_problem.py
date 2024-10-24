from bandit.simulate_random import SimulateRandom
from bandit.simulate_egreedy import SimulateEGreedy
from bandit.simulate_decayepsilon import SimulateDecayEpsilon

def display_bandit():
    while True:
        print("\nTest bandit algorithm\n")
        print("1) Random Selection Algorithm")
        print("2) Epsilon-greedy Algorithm")
        print("3) Decay Epsilon Algorithm")
        print("4) Back to main menu")

        user_input = input("\nEnter choice: ")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            SimulateRandom()

        elif user_input == '2':
            SimulateEGreedy()

        elif user_input == '3':
            SimulateDecayEpsilon()

        elif user_input == '4':
            print("Returning to main menu....")
            break

        else: 
            print("Error, please try again")

        