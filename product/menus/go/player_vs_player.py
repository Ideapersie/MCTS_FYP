from menus.go.goboard import GoState, Move
from menus.go.goplayer import Point


class PlayerVsPlayer:
    # Initialise Go game with board size of 9x9 
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.game = GoState.new_game(board_size)
        print(f"\nWelcome to Go! \
              \n\nYou can type 'pass' to pass a turn or 'resign' to forfeit the game. \
              \nENJOY!")
        self.run_PvPgame()
        
    # Helper funciton to display board state 
    def print_board(self):
        print(self.game.board)
        
    def player_input(self):
        player_input = input("\nEnter your move : ")
        player_input = player_input.strip().upper()
        
        if player_input == "PASS":
            return Move.pass_turn()
        elif player_input == "RESIGN":
            return Move.resign()
        elif player_input == "":
            print("\nEmpty move, please input the move")
        elif not player_input[1:].isdigit():
            print("Invalid move, please move is not an integer!") 
        elif int(player_input[1:]) > self.board_size:
            print("Invalid move, input is larger than board size")
        else:
            col, row = player_input[0], player_input[1:]
            # Upper-case therefore the ASCII value is the same
            # Ord converts to ASCII value of the column letter
            convert_col = ord(col) - ord('A') + 1 
            
            return Move.play(Point(int(row), convert_col))
        
    def run_PvPgame(self):
        
        while not self.game.game_over():
            # since next_player is stored as Player.colour
            current_player = str(self.game.next_player).split('.', 1)

        print(f"\n{current_player[1]}'s turn: \n")
        print_board(new_game.board)
        
        move = None 
        while move is None or not new_game.valid_move(move):
            move = player_input()
            if move and not new_game.valid_move(move):
                print("Invalid move! Please try again")
                
        new_game = new_game.play_move(move)
    
    print("\n Game Over!")
    print_board(new_game.board)
    
    if new_game.last_move.is_resign:
        next_player = str(new_game.next_player).split('.', 1)
        print(f"{next_player[1]} wins by resignation")
        
    elif new_game.last_move.is_pass:
        print("\nBoth players passed, the game is a draw")
        
if __name__ == "__main__":
    print(f"""Welcome to Go! 
You can type 'pass' to pass a turn or 'resign' to forfeit the game
        ENJOY!""")
    player_vs_player_game()