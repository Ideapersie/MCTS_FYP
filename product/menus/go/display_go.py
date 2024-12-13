from menus.go.player_vs_player import PlayerVsPlayer

def display_go():
    while True:
        print("\n\nWelcome to the GO game:\n")
        print("1) Player Vs Player mode")
        print("2) Play against an AI")
        print("3) Exit")
        
        user_input = input("\nEnter choice: ")

        user_input = user_input.strip() #incase whitespaces was added 
        
        if user_input == '1':
            PlayerVsPlayer()
        elif user_input == '2':
            print("Work in Progress, please select another option")
        elif user_input == '3':
            print("Returning to main menu....")
            break
        else: 
            print("Error, please try again")
    
    
