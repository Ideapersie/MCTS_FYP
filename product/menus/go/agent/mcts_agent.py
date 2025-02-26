from menus.go.agent.base import Agent
from menus.go.agent.mcts_node import MCTsNode
from menus.go.goboard import Move, Player, GoState
import math, random


class MCTsAgent(Agent):
    # Temperature controls the exploration-exploitation tradeoff, 
    def __init__(self, temperature, num_rounds=100):
        self.temperature = temperature
        self.num_rounds = num_rounds
    
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
                
        # Select the best move based on the number of rollouts
        best_move = None
        highest_winrate = -1
        
        # Find the child node with the highest winrate
        for child in root.children:
            child_winrate = child.rollout_winrate(game_state.next_player)
            if child_winrate > highest_winrate:
                highest_winrate = child_winrate
                best_move = child.move.point
                
        return Move.play(best_move)
    
    # Simulate a random game and returns the winner
    def simulate_random_game(self, game_state):
        simulate_state = game_state
        # Play until the game is over
        while not simulate_state.game_over():
            possible_moves = simulate_state.legal_moves()
            # Break if no possible moves left
            if not possible_moves:
                break
            
            print(f"Possible moves: {possible_moves}")
            
            random_move = random.choice(possible_moves)
            random_move = Move.play(random_move)
            simulate_state = simulate_state.play_move(random_move)
            
        # Compare score to determine the winner
        black_score, white_score = simulate_state.final_score()
        if black_score > white_score:
            return Player.black
        else:
            return Player.white
                
    def ucb_score(total_rollouts, child_rollouts, winrate, temperature):
        ucb_score = winrate + temperature * math.sqrt(math.log(total_rollouts) / child_rollouts)
        return ucb_score
                
    # Select the child node with the highest UCB1 value
    def select_child(self, node):
        # no. of rollouts in total 
        total_rollouts = node.total_rollouts
        
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
            
        
        