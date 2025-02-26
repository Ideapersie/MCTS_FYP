from menus.go.player_vs_player import PlayerVsPlayer
from menus.go.player_vs_bot import PlayerVsBot
from menus.go.player_vs_mcts import PlayerVsMcts

def display_go():
    while True:
        print("\n\nWelcome to the GO game:\n")
        print("1) Player Vs Player mode")
        print("2) Play against random AI")
        print("3) Play against AI with Minimax")
        print("4) Play against AI with MCTs")
        print("5) Exit")
        
        user_input = input("\nEnter choice: ")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            PlayerVsPlayer()
        elif user_input == '2':
            PlayerVsBot()
        elif user_input == '3':
            print("Work in Progress, please select another option")
        elif user_input == '4':
            PlayerVsMcts()
        elif user_input == '5':
            print("Returning to main menu....")
            break
        else: 
            print("Error, please try again")
    
    
