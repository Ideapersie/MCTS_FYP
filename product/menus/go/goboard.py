import copy 
from go.goplayer import Player,Point

class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign # bitwise XOR, returns True if exactly one is True
        self.point = point 
        self.is_play = (self.point is not None)
        self.is_pass = is_pass 
        self.is_resign = is_resign
        
    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign=True)
    
# Go strings are same coloured stones which are connected
class GoString():
    def __init__(self, colour, stones, liberties):
        self.colour = colour
        self.stones = set(stones)
        self.liberties = set(liberties)
        
    def add_liberty(self, point):
        self.liberties.add(point)
        
    def remove_liberty(self, point):
        self.liberties.remove(point)
        
    # Connect 2 Go Strings together to form a bigger String 
    def merged_with(self, go_string):
        assert go_string.colour == self.colour
        
        combined_stones = self.stones | go_string.stones
        combined_liberties = (self.liberties | go_string.liberties) - combined_stones
        
        return GoString(self.colour, combined_stones, combined_liberties )
        
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.colour == other.colour and \
            self.stones == other.stones and \
            self.liberties == other.liberties
            
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
    
    # Checking if the stone is in the board boundaries    
    def in_grid(self, point):
        # Too low 
        if point.row < 1 or point.col < 1:
            return False 
        # Too high 
        elif point.row > self.num_rows or point.col > self.num_cols:
            return False
        else:
            return True
    
    # Return player colour of stone on point else None 
    def get_player(self, point):
        stone_point = self._grid.get(point)
        if stone_point is None:
            return None
        else:
            return stone_point.colour
    
    # Return go string at a point else None 
    def get_go_string(self, point):
        string_point = self._grid.get(point)
        if string_point is None:
            return None 
        else: 
            return string_point
        
    # Removing a string, can create liberties for other string
    def _remove_string(self, string):
        for stone in string.stones:
            for neighbour in stone.neighbours():
                neighbour_string = self._grid.get(neighbour)
                if neighbour_string is None:
                    continue
                elif neighbour_string is not string:
                    neighbour_string.add_liberty(stone)
            self._grid[stone] = None
        
    # Placing a stone on the board & manages liberties of neighbouring stones    
    def place_stone(self, player, point):
        if not self.in_grid(point):
            raise ValueError(f"Illegal move: The point {point} is outside the board's bound")
        
        if self._grid.get(point) is not None:
            raise ValueError(f"Illegal move: The point {point} is already occupied")
        
        # stones neighbouring the new placed stone  
        same_colour_neighbours = [] 
        opposite_colour_neighbours = []
        liberties = []
        
        for neighbour in point.neighbours():
            # Skip neighbours which are out of bounds
            if not self.in_grid(neighbour):
                continue
            
            neighbour_string = self._grid.get(neighbour)
            
            if neighbour_string is None:
                liberties.append(neighbour)
            
            elif neighbour_string.colour == player:
                if neighbour_string not in same_colour_neighbours:
                    same_colour_neighbours.append(neighbour_string)
                    
            else:
                if neighbour_string not in opposite_colour_neighbours:
                    opposite_colour_neighbours.append(neighbour_string)
                    
        placed_string = GoString(player, [point], liberties)
        
        
        # Merge Strings if connected to same coloured strings 
        for placed_string_same in same_colour_neighbours:
            placed_string = placed_string.merged_with(placed_string_same)
            
        # Update board grid with new merged string
        for placed_string_point in placed_string.stones:
            self._grid[placed_string_point] = placed_string
            
        # Reduce liberties of opponent's neighbouring strings, If 0 then remove it 
        for place_string_other in opposite_colour_neighbours:
            place_string_other.remove_liberty(point)
            if place_string_other.num_liberties == 0:
                self._remove_string(place_string_other)
            
class GoState():
    def __init__(self, board, previous_state, last_move, next_player):
        self.board = board 
        self.previous_state = previous_state
        self.last_move = last_move
        self.next_player = next_player
        
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(board_size[0], board_size[1])
        # Player with black stone starts first 
        return GoState(board, None, None, Player.black)
        
    def play_move(self, move):
        if move.is_play:
            next_move = copy.deepcopy(self.board)
            next_move.place_stone(self.next_player, move.point)
        else:
            next_move = self.board
            
        return GoState(next_move, self, move, self.next_player.other)