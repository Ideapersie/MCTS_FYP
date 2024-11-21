import random
from go.agent.base import Agent
from go.agent.helpers import is_point_an_eye
from go.goboard_slow import Move
from go.gotypes import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        """ Chooses random valid move that preserves own eyes"""
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board, candidate, game_state.next_player):
                        candidates.append(candidate)
                        
                if not candidate:
                    return Move.pass_turn()
                
                return Move.play(random.choice(candidates))