def display_main_menu():
    
    print("\nWelcome to Main Menu\n")

    print("1) Test Bandit Problem algorithms")
    print("2) Go Game")
    print("3) Exit")

    choice = input("Enter choice: ")
    choice = choice.strip() # Incase user accidently enters space

    return choice

