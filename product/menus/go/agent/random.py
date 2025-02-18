import random 
from menus.go.agent.base import Agent
from menus.go.goplayer import Point
from menus.go.agent.point_eye import is_point_eye
from menus.go.goboard import Move


class RandomBot(Agent):
    def select_move(self, current_game):
        # Choose a random valid move which doesn't fill own eyes
        
        moves = [] 
        
        for r in range(1, current_game.board.num_rows + 1):
            for c in range(1, current_game.board.num_cols + 1):
                moves = Point(row=r, col=c)
                if current_game.is_valid_move(moves) and \
                    not is_point_eye(current_game.board, moves, current_game.next_player):
                    moves.append(moves)
                    
        if not moves:
            return Point.pass_turn()
        return Move.play(random.choice(moves))