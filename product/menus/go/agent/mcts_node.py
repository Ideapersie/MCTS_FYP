from menus.go.goboard import Player, Move
from menus.go.fast_go import FastGoState, FastBoard
import random,copy

class MCTsNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = FastGoState(game_state.board.num_rows, game_state)
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = {Player.black: 0, Player.white: 0}
        self.num_rollouts = 0
        self.total_rollouts = 0
        self.unvisited_moves = self.game_state.board.fast_legal_moves(game_state.next_player)

    # If there are legal moves left, we can add a child
    def add_child(self):
        return len(self.unvisited_moves) > 0
    
    # No legal moves left, can't search the tree further
    def search_over(self):
        return self.game_state.fast_game_over()
    
    # Returns the rollout outcome winrate as float 
    def rollout_winrate(self, player):
        if self.num_rollouts == 0:
            return 0
        else:
            return (self.wins[player] / self.num_rollouts) 
        
    # Defining the expansion step of the MCTS algorithm
    def random_child(self):
        
        # Select moves from central moves in the opening game
        if self.num_rollouts < 8 and len(self.unvisited_moves) > 20:
            central_moves = [ move for move in self.unvisited_moves 
                if 3 <= move.row <= 7 and 3 <= move.col <= 7]
            
            if central_moves:
                random_move = random.choice(central_moves)
            else:
                random_move = random.choice(self.unvisited_moves)
        
        else: 
            random_move = random.choice(self.unvisited_moves)
                
        # remove move from unvisited moves        
        self.unvisited_moves.remove(random_move)
        move = Move.play(random_move)
        
        # Create a deep copy of the game state to ensure node independence
        next_state = copy.deepcopy(self.game_state)
        next_state.fast_play_move(move)
        
        child_node = MCTsNode(next_state, self, move)
        self.children.append(child_node)
        return child_node
        
    # Update the rollout statistics to use for backpropagation step 
    def update_rollout(self, winner):
        self.num_rollouts += 1
        self.wins[winner] += 1
        
        # Update the total rollouts until the root node
        node = self 
        while node is not None:
            node.total_rollouts += 1
            node = node.parent