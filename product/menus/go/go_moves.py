from menus.go.goplayer import Point
from menus.go.goboard import GoState, Move

class GoMoves:
    # Initialise Go game with board size of 9x9 
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.game = GoState.new_game(board_size)
        print(f"\nWelcome to Go! \
              \n\nYou can type 'pass' to pass a turn or 'resign' to forfeit the game. \
              \nENJOY!")

    # Helper funciton to display board state 
    def print_board(self):
        print(self.game.board)

    def player_input(self):
        # To avoid capitalization or spacing issues
        player_input = input("\nEnter your move : ").strip().upper()
        
        if player_input == "PASS":
            return Move.pass_turn()
        elif player_input == "RESIGN":
            return Move.resign()
        elif player_input == "":
            print("\nEmpty move, please input the move")
        elif not player_input[1:].isdigit():
            print("Invalid move, move is not an integer!") 
        elif int(player_input[1:]) > self.board_size:
            print("Invalid move, input is larger than board size")
        else:
            col, row = player_input[0], player_input[1:]
            # Upper-case therefore the ASCII value is the same
            # Ord converts to ASCII value of the column letter
            convert_col = ord(col) - ord('A') + 1 
            
            return Move.play(Point(int(row), convert_col))