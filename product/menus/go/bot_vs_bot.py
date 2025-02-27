from menus.go.goplayer import Player
from menus.go.goboard import GoState
from menus.go.go_moves import GoMoves
from menus.go.agent.mcts_agent import MCTsAgent
import winsound

class BotVsBot(GoMoves):
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.game = GoState.new_game(board_size)
        # Two bots with different values to test strength 
        self.bot = {
            Player.black: MCTsAgent(temperature=1.4, num_rounds=5),
            Player.white: MCTsAgent(temperature=1.4, num_rounds=10)
        }
        
        print(f"\nWelcome to Go! \
              \n\nMCTs Agent ({self.bot[Player.black].num_rounds} rounds) vs MCTs Agent ({self.bot[Player.white].num_rounds} rounds)")

        self.run_BvBgame()
    
    def run_BvBgame(self):
        # Loop until the game is over
        while not self.game.game_over():            
            self.print_board()
            
            bot_move = self.bot[self.game.next_player].select_move(self.game)
            self.game = self.game.play_move(bot_move)
            
            # To format displaying only the Player's colour
            current_player = str(self.game.next_player).split('.', 1)
            print(f"\n{current_player[1]}'s Player move: {self.print_move(bot_move)}")
            
    # Handles the end of the game and display results
    def end_PvBgame(self):
        # Show final board state
        print("\nFinal Board state: ")
        self.print_board()
        
        # Alert when game is over
        winsound.Beep(1000,500)
        
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
    BotVsBot()