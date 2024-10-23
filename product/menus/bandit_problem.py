from menus.simulate_random_bandit import SimulateRandom
from menus.simulate_egreedy_bandit import SimulateEGreedy

def display_bandit():
    while True:
        print("\nTest bandit algorithm\n")
        print("1) Random Selection Algorithm")
        print("2) Epsilon-greedy Algorithm")
        print("3) More algorithms to continue")
        print("4) Back to main menu")

        user_input = input("\nEnter choice: ")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            SimulateRandom()

        elif user_input == '2':
            SimulateEGreedy()

        elif user_input == '3':
            print("Please wait for updates")

        elif user_input == '4':
            print("Returning to main menu....")
            break

        else: 
            print("Error, please try again")

        