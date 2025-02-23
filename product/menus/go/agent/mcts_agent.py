from menus.go.agent.base import Agent
from menus.go.agent.mcts_node import MCTsNode


class MCTsAgent(Agent):
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
                
    
        