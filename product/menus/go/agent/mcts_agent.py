import numpy as np
from menus.go.agent.base import Agent
from menus.go.agent.mcts_node import MCTsNode
from menus.go.fast_go import FastGoState
from menus.go.go_moves import GoMoves
from menus.go.goboard import Move, Player, GoState
import math, random, time
import multiprocessing as mp


class MCTsAgent(Agent):
    # Temperature controls the exploration-exploitation tradeoff, 
    def __init__(self, temperature, num_rounds):
        self.temperature = temperature
        self.num_rounds = num_rounds
        self.go_moves = GoMoves()
        self.move_counter = 0
            
    
    def select_move(self, game_state):
        # Initialising the root node 
        root = MCTsNode(game_state)
        
        # Compute the time taken for the move
        start_time = time.time()
        
        # Expand root node to analyse moves in parallel
        while root.add_child():
            root.random_child()

        # Prepare move for parallel processing 
        num_processes = mp.cpu_count()
        rollouts_per_process = self.num_rounds // num_processes 
        
        # Create pool which runs parallel simulations 
        with mp.Pool(processes=num_processes) as pool:
            rollout_result = pool.starmap(
                self.run_batch_simulation,
                [(root.game_state, rollouts_per_process, i) for i in range(num_processes)]
            )
            
        # Combine results dictionary
        combined_results = {}
        for result in rollout_result:
            # Combine results from each process
            for move_point, wins in result.items():
                # Create dictionary for each move point
                if move_point not in combined_results:
                    combined_results[move_point] = {Player.black: 0, Player.white: 0}
                combined_results[move_point][Player.black] += wins[Player.black]
                combined_results[move_point][Player.white] += wins[Player.white]     
                
        # Update the root node with the combined results
        for child in root.children:
            point = child.move.point
            # Update the wins for each child node
            if point in combined_results:
                child.wins[Player.black] += combined_results[point][Player.black]
                child.wins[Player.white] += combined_results[point][Player.white]
                # Update the number of rollouts
                child.num_rollouts += combined_results[point][Player.black] + \
                    combined_results[point][Player.white]
            
            
        # Select the best move based on the number of rollouts
        best_move = None
        highest_winrate = -1
        
        # Find the child node with the highest winrate
        for child in root.children:
            child_winrate = child.rollout_winrate(game_state.next_player)
            
            # DEBUG: Check the winrate of each child node
            print(f"Move: {self.go_moves.print_move(child.move)}, Win rate: {child_winrate:.2%}, Visits: {child.num_rollouts}")
            
            if child_winrate > highest_winrate:
                highest_winrate = child_winrate
                best_move = child.move.point
        
        # Compute the time taken for the move
        end_time = time.time()
                
        # DEBUG: Check the winrate of best node
        print(f"\n DEBUG: Best move -> {self.go_moves.print_move(best_move)}, Winrate: {highest_winrate:.2%}, \
              Time Taken: {end_time - start_time:.2f}")
        
        self.move_counter += 1
        
        # Use move counter to detect endgame
        total_moves = game_state.board.num_rows * game_state.board.num_cols * 0.8 # on average, about 80% of the board is filled
        move_ratio = self.move_counter / total_moves
        
        
        # Threshold for resigning move 
        resignation_threshold = 0.1 # Resign if winrate is below 10%
        
        # Dynamic threshold for passing move
        base_threshold = 0.25
        endgame_threshold = 0.40
        
        # Adjusting the passing threshold based on the move ratio 
        if move_ratio > 0.6: # After 60% of expected moves played
            passing_threshold = base_threshold + (move_ratio - 0.7) * (endgame_threshold - base_threshold) / 0.3
        else:
            passing_threshold = base_threshold
            
        # Debug information
        print(f"Moves ratio/81: {move_ratio:.2f}, Passing threshold: {passing_threshold:.2f}")
    
            
        # If opponent passes, then pass as well
        if game_state.last_move and game_state.last_move.is_pass:
            return Move.pass_turn()
        
        # If winrate is below threshold, then pass or resign
        if highest_winrate < passing_threshold and move_ratio > 0.6:
            return Move.pass_turn()
        elif highest_winrate < resignation_threshold:
            return Move.resign()
        else:    
            return Move.play(best_move)
    
    # Simulate a random game and returns the winner
    def simulate_random_game(self, game_state):
        # Convert game state to fast simulation
        sim_state = FastGoState(game_state.board.num_rows, game_state)
        
        # Play until the game is over
        max_moves = game_state.board.num_rows * game_state.board.num_cols
        
        for _ in range(max_moves):
            # Stop if game over 
            if sim_state.fast_game_over():
                break
            
            # Get faster legal moves
            possible_moves = sim_state.board.fast_legal_moves(sim_state.next_player)
            
            if not possible_moves:
                # if no legal moves then pass 
                sim_state.fast_play_move(Move.pass_turn())
                continue
            
            # Choose random move and play it 
            random_move = Move.play(random.choice(possible_moves))
            sim_state.fast_play_move(random_move)
        
        # Quick scoring without territory calculation
        return self.quick_eval(sim_state)

    # Running a batch simulation for parallel processing
    def run_batch_simulation(self, game_state, num_simulation, batch_no):
        win_count = {}
       
        # Local random num generator 
        local_random =  random.Random(batch_no) 
       
        for _ in range(num_simulation):
            
            # Create new node for each simulation
            node = MCTsNode(game_state)
            
           # Selection step: traverse tree until leaf node is reached
            while (not node.add_child()) and not node.search_over():
                node = self.select_child(node)
                
            # Expansion step: adds new child node to the tree 
            if node.add_child():
                node = node.random_child()
                
            # Store selected move before simulation
            sel_move = node.move.point
                
            # Simulation step: simulate a random game from the new child node
            winner = self.simulate_random_game(node.game_state)
            
            # Add number of wins depending on the move 
            if sel_move not in win_count:
                win_count[sel_move] = {Player.black: 0, Player.white: 0}
            win_count[sel_move][winner] += 1 
           
        return win_count
    
    # Quick evaluation of the game state, only compares the score
    def quick_eval(self, sim_state):
        black_stones = np.sum(sim_state.board.grid == 1)
        white_stones = np.sum(sim_state.board.grid == 2)
        
        # Combine number of stones and captures
        black_scores = black_stones + sim_state.captured[Player.black]
        white_scores = white_stones + sim_state.captured[Player.white] + 6.5 # Add komi for white player
        
        # Return the winner based on the score
        return Player.black if black_scores > white_scores else Player.white
                
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
            #print(f"Possible move: {child.move.point}, UCB score: {ucb_score:.2f}")
            
            if ucb_score > highest_score:
                highest_score = ucb_score
                best_child = child
                
        return best_child
            
        
        