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

    # Helper function to print the move in the format 'A1'
    def print_move(self, move):
        if move.is_pass:
            return "PASS"
        elif move.is_resign:
            return "RESIGN"
        
        # Skip I column since it is not used in Go
        col = move.point.col
        if col >= 9:
            col += 1
        
        return f"{chr(col+ ord('A') - 1)}{(move.point.row)}"

    def player_input(self):
        # To avoid capitalization or spacing issues
        player_input = input("\nEnter your move : ").strip().upper()
        
        # Check before converting to row and column
        if not player_input:
            print("\nEmpty move, please input the move")
            return None
        
        col, row = player_input[0], player_input[1:]
        # Ord converts to ASCII value of the column letter
        convert_col = ord(col) - ord('A') + 1 
        
        # Skip I column since it is not used in Go
        if col > 'I':
            convert_col -= 1
        
        if player_input == "PASS":
            return Move.pass_turn()
        elif player_input == "RESIGN":
            return Move.resign()
        # Conditions to satisfy for input to be valid
        elif not player_input[1:].isdigit():
            print("Invalid move, move is not an integer!") 
        elif convert_col > self.board_size or int(player_input[1:]) > self.board_size:
            print("Invalid move, input is larger than board size")
        elif int(player_input[1:]) < 1:
            print("Invalid move, input is smaller than board size")
        # Dont allow I column to be used in Go
        elif col == 'I':
            print("Invalid move, I column is not used in Go, Please us A-H or J")
        else:
            return Move.play(Point(int(row), convert_col))