from menus.go.goboard import Player, Move
import random

class MCTsNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = {Player.black: 0, Player.white: 0}
        self.num_rollouts = 0
        self.total_rollouts = 0
        self.unvisited_moves = game_state.legal_moves()

    # If there are legal moves left, we can add a child
    def add_child(self):
        return len(self.unvisited_moves) > 0
    
    # No legal moves left, can't search the tree further
    def search_over(self):
        return self.game_state.game_over()
    
    # Returns the rollout outcome winrate as float 
    def rollout_winrate(self, player):
        if self.num_rollouts == 0:
            return 0
        else:
            return (self.wins[player] / self.num_rollouts) 
        
    # Defining the expansion step of the MCTS algorithm
    def random_child(self):
        # Randomly select a move from the list of unvisited moves
        random_move = random.randint(0, len(self.unvisited_moves) - 1)
        move = self.unvisited_moves.pop(random_move) 
        move = Move.play(move)
        next_state = self.game_state.play_move(move)
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