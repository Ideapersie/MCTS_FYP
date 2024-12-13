from menus.main_menu import display_main_menu
from menus.bandit.display_bandit import display_bandit
from menus.go.display_go import display_go

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