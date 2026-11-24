import numpy as np

from ..board import PASS, Board


class RandomAgent:
    """Uniform over legal moves that do not fill its own eyes; passes when none."""

    name = "random"

    def __init__(self, playouts: int = 0, seed: int = 0):
        self.rng = np.random.default_rng(seed)

    def select(self, board: Board) -> int:
        moves = board.legal_moves(skip_eyes=True)
        return int(self.rng.choice(moves)) if len(moves) else PASS
