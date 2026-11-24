"""The FYP agent, re-implemented on the fast board so it can be compared fairly.

What `product/menus/go/agent/mcts_agent.py` does, step by step:
- every simulation starts a fresh node at the root and expands one random
  child, so the UCB selection code is never reached: this is flat Monte Carlo
  over the root moves, not a tree search;
- rollouts are truncated (85%, 65% or 40% of the board depending on how full
  it is) and stop early once one side leads by more than 1.5 x board size;
- a rollout is scored by stones on the board plus captures (no territory), with
  komi;
- the move with the highest win rate is chosen, however few visits it had;
- it passes when its best win rate is low late in the game and resigns below 10%.
The parameters below are the original ones.
"""

import numpy as np
from numba import njit

from ..board import EMPTY, PASS, Board, is_legal, play

RESIGN = -2


@njit(cache=True)
def truncated_playout(board, colour, ko, n, komi, depth, seed, caps_b, caps_w):
    """Random playout for `depth` moves (no eye rule, as in the original).
    Returns black score minus white score, stones plus captures, minus komi."""
    np.random.seed(seed)
    stride = n + 2
    mark = np.zeros(board.shape[0], dtype=np.int64)
    stamp = np.zeros(1, dtype=np.int64)
    buf = np.empty(board.shape[0], dtype=np.int64)
    cand = np.empty(n * n, dtype=np.int64)
    passes = 0
    threshold = n * 1.5
    for moves in range(depth):
        if passes >= 2:
            break
        if moves > 30:
            b = 0
            w = 0
            for i in range(board.shape[0]):
                if board[i] == 1:
                    b += 1
                elif board[i] == 2:
                    w += 1
            if abs((b + caps_b) - (w + caps_w + komi)) > threshold:
                break
        m = 0
        for r in range(1, n + 1):
            for c in range(1, n + 1):
                p = r * stride + c
                if board[p] == EMPTY and is_legal(board, p, colour, ko, stride, mark, stamp, buf):
                    cand[m] = p
                    m += 1
        if m == 0:
            passes += 1
            ko = -1
        else:
            passes = 0
            p = cand[np.random.randint(m)]
            cap, ko = play(board, p, colour, stride, mark, stamp, buf)
            if colour == 1:
                caps_b += cap
            else:
                caps_w += cap
        colour = 3 - colour
    b = 0
    w = 0
    for i in range(board.shape[0]):
        if board[i] == 1:
            b += 1
        elif board[i] == 2:
            w += 1
    return (b + caps_b) - (w + caps_w + komi)


class FlatMC:
    name = "fyp_flat"

    def __init__(self, playouts: int = 1000, seed: int = 0):
        self.playouts = playouts
        self.rng = np.random.default_rng(seed)
        self.caps = {1: 0, 2: 0}

    def select(self, board: Board) -> int:
        moves = board.legal_moves()
        if not len(moves):
            return PASS
        n = board.n
        full = n * n
        stones = int(np.count_nonzero((board.cells == 1) | (board.cells == 2)))
        ratio = stones / full
        depth = int(full * (0.85 if ratio < 0.25 else 0.65 if ratio < 0.5 else 0.4))
        me = board.to_play
        wins = np.zeros(len(moves))
        visits = np.zeros(len(moves))
        for _ in range(self.playouts):
            i = int(self.rng.integers(len(moves)))
            child = board.copy()
            cap = child.play(int(moves[i]))
            cb = self.caps[1] + (cap if me == 1 else 0)
            cw = self.caps[2] + (cap if me == 2 else 0)
            d = truncated_playout(child.cells, child.to_play, child.ko, n, board.komi, depth,
                                  int(self.rng.integers(2**31)), cb, cw)
            visits[i] += 1
            if (d > 0) == (me == 1):
                wins[i] += 1
        rate = np.where(visits > 0, wins / np.maximum(visits, 1), -1)
        best = int(np.argmax(rate))
        winrate = rate[best]
        # The original's pass and resign rules
        move_ratio = (stones + self.caps[1] + self.caps[2]) / (full * 0.8)
        pass_at = 0.25 + (move_ratio - 0.7) * (0.45 - 0.25) / 0.25 if move_ratio > 0.65 else 0.25
        if winrate < pass_at and move_ratio > 0.6:
            return PASS
        if winrate < 0.1:
            return RESIGN
        return int(moves[best])

    def observe(self, colour: int, captured: int):
        """The arena reports captures so the stone-count evaluation can use them."""
        self.caps[colour] += captured
