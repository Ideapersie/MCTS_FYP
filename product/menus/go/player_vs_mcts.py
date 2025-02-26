from menus.go.agent.mcts_agent import MCTsAgent
from menus.go.go_moves import GoMoves
from menus.go.goboard import Player,GoState,Move
from menus.go.goplayer import Point

class PlayerVsMcts(GoMoves):
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.game = GoState.new_game(board_size)
        self.bot = MCTsAgent(temperature=1.4, num_rounds=10)
        
        print(f"\nWelcome to Go! \
              \n\nYou can type 'pass' to pass a turn or 'resign' to forfeit the game. ")

        self.run_PvBgame()
        
    def run_PvBgame(self):
        
        while not self.game.game_over():
            # since next_player is stored as Player.colour
            current_player = str(self.game.next_player).split('.', 1)

            # Player's turn 
            if self.game.next_player == Player.black:
                print(f"\n{current_player[1]}'s turn: \n")
                self.print_board()
            
                move = None
                while move is None or not self.game.valid_move(move):
                    if self.game.next_player == Player.black:
                        move = self.player_input()
                        
                    if move and not self.game.valid_move(move):
                        print("Invalid move! Please try again")
                        
                self.game = self.game.play_move(move)  
            # Bot's turn    
            else:
                print(f"\n{current_player[1]}'s turn: \n")
                self.print_board()
                # Passes turn when player passes 
                if self.game.last_move.is_pass:
                    bot_move = Move.pass_turn()
                else:
                    bot_move = self.bot.select_move(self.game)
                self.game = self.game.play_move(bot_move) 
                # fix print statement 
                print(f"\nBot played: {bot_move.point}")
                
        # Display results
        self.end_PvBgame()
        
    # Handles the end of the game and display results
    def end_PvBgame(self):
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
        
if __name__ == '__main__':
    PlayerVsMcts()