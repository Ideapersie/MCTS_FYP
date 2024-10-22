from menus.simulate_random_bandit import Simulate_random

def display_bandit():
    while True:
        print("\nTest bandit algorithm\n")
        print("1) Random Selection Algorithm")
        print("2) More algorithms to continue")
        print("3) Back to main menu")

        user_input = input("\nEnter choice:")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            Simulate_random()

        elif user_input == '2':
            print("Please wait for updates")

        elif user_input == '3':
            print("Returning to main menu....")
            break

        else: 
            print("Error, please try again")

        