import random 
from menus.go.agent.base import Agent
from menus.go.goplayer import Point
from menus.go.agent.point_eye import is_point_eye
from menus.go.goboard import Move, GoState


class RandomBot(Agent):
    def select_move(self, current_game):
        # Choose a random valid move which doesn't fill own eyes
        
        moves = [] 
        
        for r in range(1, current_game.board.num_rows + 1):
            for c in range(1, current_game.board.num_cols + 1):
                candidate_move = Point(row=r, col=c)
                if current_game.valid_move(Move.play(candidate_move)) and not is_point_eye(current_game.board, candidate_move, current_game.next_player):
                    moves.append(candidate_move)
                    
        if not moves:
            return Move.pass_turn()
        chosen_move = random.choice(moves)
        return Move.play(chosen_move)
