from menus.go.goboard import GoState, Move
from menus.go.goplayer import Point
from menus.go.go_moves import GoMoves


class PlayerVsPlayer(GoMoves):
    # Initialise Go game with board size of 9x9 
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.game = GoState.new_game(board_size)
        print(f"\nWelcome to Go! \
              \n\nYou can type 'pass' to pass a turn or 'resign' to forfeit the game. \
              \nENJOY!")
        self.run_PvPgame()

    # Function to run the Player vs Player game    
    def run_PvPgame(self):
        
        while not self.game.game_over():
            # since next_player is stored as Player.colour
            current_player = str(self.game.next_player).split('.', 1)

            print(f"\n{current_player[1]}'s turn: \n")
            self.print_board()
            
            move = None 
            while move is None or not self.game.valid_move(move):
                move = self.player_input()
                if move and not self.game.valid_move(move):
                    print("Invalid move! Please try again")
                    
            self.game = self.game.play_move(move)
        # Display results
        self.end_PVPgame()
        
    # Handles the end of the game and display results
    def end_PVPgame(self):
        # Show final board state
        print("\nFinal Board state: ")
        self.print_board()
        
        scores = self.game.final_score()
        
        # If player resigns, other player wins immediately
        if self.game.last_move.is_resign:
            next_player = str(self.game.next_player).split('.', 1)
            print(f"\n{next_player[1]} wins by resignation\n")
            
        else:
            print(f"Final Score: Black {scores['Black']} - White {scores['White']}")
            
            if scores["Black"] > scores["White"]:
                print("Black wins!") 
            elif scores["Black"] == scores["White"]:
                print("It is a draw!")
            else:
                print("White wins!")
            
            
if __name__ == "__main__":
    PlayerVsPlayer()
    