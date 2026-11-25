"""Board to network input, and the eight symmetries of the square.

Input planes (side to move first, so the net never needs to know the colour):
0 own stones, 1 opponent stones, 2 empty, 3 legal moves for the side to move,
4 ones if the side to move is white (komi changes who is favoured).
The policy has n*n + 1 outputs; the last one is pass.
"""

import numpy as np

from .board import BLACK, PASS, WHITE, Board

PLANES = 5


def encode(board: Board) -> np.ndarray:
    n = board.n
    g = board.grid()
    me = board.to_play
    x = np.zeros((PLANES, n, n), dtype=np.float32)
    x[0] = g == me
    x[1] = g == (WHITE if me == BLACK else BLACK)
    x[2] = g == 0
    for p in board.legal_moves():
        r, c = board.rc(int(p))
        x[3, r, c] = 1
    if me == WHITE:
        x[4] = 1
    return x


def move_index(board: Board, move: int) -> int:
    if move == PASS:
        return board.n * board.n
    r, c = board.rc(move)
    return r * board.n + c


def index_move(board: Board, i: int) -> int:
    n = board.n
    return PASS if i == n * n else board.point(i // n, i % n)


def symmetries(x: np.ndarray, pi: np.ndarray, n: int):
    """Yield the 8 rotations/reflections of planes x and policy pi together."""
    board_pi = pi[:-1].reshape(n, n)
    for k in range(4):
        for flip in (False, True):
            xs = np.rot90(x, k, axes=(1, 2))
            ps = np.rot90(board_pi, k)
            if flip:
                xs = xs[:, :, ::-1]
                ps = ps[:, ::-1]
            yield np.ascontiguousarray(xs), np.concatenate([ps.reshape(-1), pi[-1:]])
