from menus.go.agent.base import Agent
from menus.go.agent.mcts_node import MCTsNode
import math


class MCTsAgent(Agent):
    # Temperature controls the exploration-exploitation tradeoff, 
    def __init__(self, temperature, total_rollouts):
        self.temperature = temperature
        self.rollouts = total_rollouts
    
    def select_move(self, game_state):
        # Initialising the root node 
        root = MCTsNode(game_state)
        
        # Set number of iterations
        for _ in range(self.num_rounds):
            node = root 
            # Selection step: traverse tree until leaf node is reached
            while (not node.add_child()) and not node.search_over():
                node = self.select_child(node)
                
            # Expansion step: adds new child node to the tree 
            if node.add_child():
                node = node.random_child()
                
            # Simulation step: simulate a random game from the new child node
            winner = self.simulate_random_game(node.game_state)
            
            # Backpropagation step: update the node statistics
            while node is not None:
                node.update_rollout(winner)
                # Keep updating until the root node is reached
                node = node.parent
                
    def ucb_score(total_rollouts, child_rollouts, winrate, temperature):
        ucb_score = winrate + temperature * math.sqrt(math.log(total_rollouts) / child_rollouts)
        return ucb_score
                
    # Select the child node with the highest UCB1 value
    def select_child(self, node):
        # no. of rollouts in total 
        total_rollouts = 0 
        
        for child in node.children:
            total_rollouts += child.num_rollouts
        
        # Assign -1 so the first child is always selected 
        highest_score = -1
        best_child = None
        
        # Calculate UCB1 score for each child node
        for child in node.children:
            ucb_score = MCTsAgent.ucb_score(total_rollouts, child.num_rollouts, 
                                            child.rollout_winrate(node.game_state.next_player), self.temperature)
            
            # UCB score per move used for analysis and testing
            print(f"Possible move: {child.move.point}, UCB score: {ucb_score}")
            
            if ucb_score > highest_score:
                highest_score = ucb_score
                best_child = child
                
        return best_child
            
        
        