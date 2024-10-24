from menus.main_menu import display_main_menu
from menus.bandit.bandit_problem import display_bandit
from menus.go.go_game import display_go

def main():
    while True:
        choice = display_main_menu()

        if (choice == "1"):
            display_bandit()
        elif(choice =="2"):
            display_go()
        elif(choice =="3"):
            print("\nExiting the program")
            break
        else:
            print("Invalid input: please try again")

if __name__ == "__main__":
    main()