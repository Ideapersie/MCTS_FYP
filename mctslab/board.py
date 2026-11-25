"""A small, fast Go board for search and self-play.

Layout: a flat int8 array of (n+2)^2 cells with a one-cell border, so every
point has four neighbours without bounds checks. 0 empty, 1 black, 2 white,
3 border. A move is a flat index; PASS is -1.

Rules: simple ko, suicide is illegal, area (Tromp-Taylor) scoring with komi.
Positional superko is not enforced: on 7x7 and 9x9 long cycles are rare in
practice, and every game is also capped at 3 * n * n moves.

The hot loops (legality, captures, random playouts) are compiled with numba.
"""

from __future__ import annotations

import numpy as np
from numba import njit

EMPTY, BLACK, WHITE, BORDER = 0, 1, 2, 3
PASS = -1


def other(c: int) -> int:
    return 3 - c


@njit(cache=True)
def _neighbours(stride):
    return np.array([-stride, -1, 1, stride], dtype=np.int64)


@njit(cache=True)
def _libs_and_stones(board, p, stride, mark, stamp, out):
    """Liberties of the group at p, and its stones written to out[:size]."""
    colour = board[p]
    nb = _neighbours(stride)
    pending = np.empty(board.shape[0], dtype=np.int64)
    pending[0] = p
    top = 1
    size = 0
    libs = 0
    mark[p] = stamp
    while top > 0:
        top -= 1
        q = pending[top]
        out[size] = q
        size += 1
        for k in range(4):
            r = q + nb[k]
            if mark[r] == stamp:
                continue
            v = board[r]
            if v == colour:
                mark[r] = stamp
                pending[top] = r
                top += 1
            elif v == EMPTY:
                mark[r] = stamp
                libs += 1
    return size, libs


@njit(cache=True)
def is_legal(board, p, colour, ko, stride, mark, stamp, buf):
    if p == PASS:
        return True
    if board[p] != EMPTY or p == ko:
        return False
    nb = _neighbours(stride)
    opp = 3 - colour
    for k in range(4):
        if board[p + nb[k]] == EMPTY:
            return True
    # No empty neighbour: legal if it captures, or joins a group with a spare liberty.
    board[p] = colour
    ok = False
    for k in range(4):
        r = p + nb[k]
        v = board[r]
        if v == opp or v == colour:
            stamp[0] += 1
            _, libs = _libs_and_stones(board, r, stride, mark, stamp[0], buf)
            if v == opp and libs == 0:
                ok = True
                break
            if v == colour and libs > 0:
                ok = True
                break
    board[p] = EMPTY
    return ok


@njit(cache=True)
def play(board, p, colour, stride, mark, stamp, buf):
    """Play a legal move. Returns (captured, new_ko)."""
    if p == PASS:
        return 0, PASS
    nb = _neighbours(stride)
    opp = 3 - colour
    board[p] = colour
    captured = 0
    last_cap = PASS
    for k in range(4):
        r = p + nb[k]
        if board[r] == opp:
            stamp[0] += 1
            size, libs = _libs_and_stones(board, r, stride, mark, stamp[0], buf)
            if libs == 0:
                for i in range(size):
                    board[buf[i]] = EMPTY
                captured += size
                last_cap = buf[0]
    ko = PASS
    if captured == 1:
        # Ko only if the capturing stone is now a lone stone in atari.
        stamp[0] += 1
        size, libs = _libs_and_stones(board, p, stride, mark, stamp[0], buf)
        if size == 1 and libs == 1:
            ko = last_cap
    return captured, ko


@njit(cache=True)
def is_eye(board, p, colour, stride):
    """A point every neighbour of which is ours, with at most one enemy diagonal
    (none on the edge). Playouts never fill these, so games end naturally."""
    if board[p] != EMPTY:
        return False
    nb = _neighbours(stride)
    for k in range(4):
        v = board[p + nb[k]]
        if v != colour and v != BORDER:
            return False
    diag = np.array([-stride - 1, -stride + 1, stride - 1, stride + 1], dtype=np.int64)
    bad = 0
    edge = False
    for k in range(4):
        v = board[p + diag[k]]
        if v == BORDER:
            edge = True
        elif v != colour:
            bad += 1
    return bad == 0 if edge else bad <= 1


@njit(cache=True)
def area_score(board, n, stride, komi):
    """Tromp-Taylor area score, black minus white (komi taken off black)."""
    mark = np.zeros(board.shape[0], dtype=np.int64)
    pending = np.empty(board.shape[0], dtype=np.int64)
    nb = _neighbours(stride)
    b = 0
    w = 0
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            p = r * stride + c
            v = board[p]
            if v == BLACK:
                b += 1
            elif v == WHITE:
                w += 1
            elif mark[p] == 0:
                # Empty region: belongs to a colour only if it borders that colour alone.
                mark[p] = 1
                pending[0] = p
                top = 1
                size = 0
                touch_b = False
                touch_w = False
                while top > 0:
                    top -= 1
                    q = pending[top]
                    size += 1
                    for k in range(4):
                        s = q + nb[k]
                        u = board[s]
                        if u == EMPTY and mark[s] == 0:
                            mark[s] = 1
                            pending[top] = s
                            top += 1
                        elif u == BLACK:
                            touch_b = True
                        elif u == WHITE:
                            touch_w = True
                if touch_b and not touch_w:
                    b += size
                elif touch_w and not touch_b:
                    w += size
    return b - w - komi


@njit(cache=True)
def legal_moves(board, colour, ko, n, stride, mark, stamp, buf, out, skip_eyes):
    """Write legal non-pass moves to out; returns how many."""
    m = 0
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            p = r * stride + c
            if board[p] != EMPTY:
                continue
            if skip_eyes and is_eye(board, p, colour, stride):
                continue
            if is_legal(board, p, colour, ko, stride, mark, stamp, buf):
                out[m] = p
                m += 1
    return m


@njit(cache=True)
def _urgent(board, last, colour, stride, mark, stamp, buf, ko):
    """Capture or escape around the last move, as in MoGo's playout policy.

    1. An enemy group next to the last move with one liberty: take it.
    2. One of our groups next to the last move in atari: extend at its
       liberty if that leaves more than one liberty.
    Returns a move or PASS (meaning no urgent move)."""
    if last < 0:
        return PASS
    nb = _neighbours(stride)
    opp = 3 - colour
    # Check the last stone itself and its neighbours.
    for k in range(5):
        q = last if k == 4 else last + nb[k]
        v = board[q]
        if v != opp and v != colour:
            continue
        stamp[0] += 1
        size, libs = _libs_and_stones(board, q, stride, mark, stamp[0], buf)
        if libs != 1:
            continue
        # find the single liberty
        lib = PASS
        for i in range(size):
            s = buf[i]
            for j in range(4):
                r = s + nb[j]
                if board[r] == EMPTY:
                    lib = r
                    break
            if lib != PASS:
                break
        if lib == PASS or not is_legal(board, lib, colour, ko, stride, mark, stamp, buf):
            continue
        if v == opp:
            return lib
        # Escape: only if the extension has more than one liberty.
        board[lib] = colour
        stamp[0] += 1
        _, l2 = _libs_and_stones(board, lib, stride, mark, stamp[0], buf)
        board[lib] = EMPTY
        if l2 > 1:
            return lib
    return PASS


@njit(cache=True)
def playout(board, colour, ko, n, komi, max_moves, seed, amaf, last=-1, heavy=False):
    """Random playout to the end (eyes are never filled).

    heavy=True first plays urgent captures and escapes around the last move.
    Plays on `board` in place. amaf[p] records which colour first played p
    (0 if nobody), for RAVE. Returns the final area score (black minus white)."""
    np.random.seed(seed)
    stride = n + 2
    mark = np.zeros(board.shape[0], dtype=np.int64)
    stamp = np.zeros(1, dtype=np.int64)
    buf = np.empty(board.shape[0], dtype=np.int64)
    cand = np.empty(n * n, dtype=np.int64)
    passes = 0
    moves = 0
    while passes < 2 and moves < max_moves:
        # Collect empty, non-eye points, then try them in random order.
        m = 0
        for r in range(1, n + 1):
            for c in range(1, n + 1):
                p = r * stride + c
                if board[p] == EMPTY and not is_eye(board, p, colour, stride):
                    cand[m] = p
                    m += 1
        played = False
        if heavy:
            u = _urgent(board, last, colour, stride, mark, stamp, buf, ko)
            if u != PASS:
                _, ko = play(board, u, colour, stride, mark, stamp, buf)
                if amaf[u] == 0:
                    amaf[u] = colour
                last = u
                passes = 0
                colour = 3 - colour
                moves += 1
                continue
        while m > 0:
            i = np.random.randint(m)
            p = cand[i]
            cand[i] = cand[m - 1]
            m -= 1
            if is_legal(board, p, colour, ko, stride, mark, stamp, buf):
                _, ko = play(board, p, colour, stride, mark, stamp, buf)
                if amaf[p] == 0:
                    amaf[p] = colour
                last = p
                played = True
                break
        if played:
            passes = 0
        else:
            ko = PASS
            last = -1
            passes += 1
        colour = 3 - colour
        moves += 1
    return area_score(board, n, stride, komi)


# The one place komi defaults live. Every entry point (arena, selfplay, iterate,
# train metadata) takes --komi and falls back to this table by board size.
# 7x7: chosen from the RAVE-vs-RAVE sweep in results/ladder.csv (see README).
KOMI = {5: 3.0, 7: 4.5, 9: 7.0}


def default_komi(n: int) -> float:
    return KOMI.get(n, 7.0)


class Board:
    """Python-side game state. The arrays are handed to the numba kernels."""

    __slots__ = ("n", "stride", "komi", "cells", "to_play", "ko", "passes", "moves", "history", "_mark", "_stamp", "_buf")

    def __init__(self, n: int = 9, komi: float | None = None):
        self.n = n
        self.stride = n + 2
        self.komi = default_komi(n) if komi is None else float(komi)
        self.cells = np.full(self.stride * self.stride, BORDER, dtype=np.int8)
        for r in range(1, n + 1):
            self.cells[r * self.stride + 1 : r * self.stride + n + 1] = EMPTY
        self.to_play = BLACK
        self.ko = PASS
        self.passes = 0
        self.moves = 0
        self.history: list[int] = []
        self._mark = np.zeros(self.cells.shape[0], dtype=np.int64)
        self._stamp = np.zeros(1, dtype=np.int64)
        self._buf = np.empty(self.cells.shape[0], dtype=np.int64)

    def copy(self) -> "Board":
        b = Board.__new__(Board)
        b.n, b.stride, b.komi = self.n, self.stride, self.komi
        b.cells = self.cells.copy()
        b.to_play, b.ko, b.passes, b.moves = self.to_play, self.ko, self.passes, self.moves
        b.history = list(self.history)
        b._mark = np.zeros(self.cells.shape[0], dtype=np.int64)
        b._stamp = np.zeros(1, dtype=np.int64)
        b._buf = np.empty(self.cells.shape[0], dtype=np.int64)
        return b

    # Coordinates
    def point(self, r: int, c: int) -> int:
        """0-based row and column to a flat index."""
        return (r + 1) * self.stride + (c + 1)

    def rc(self, p: int) -> tuple[int, int]:
        return p // self.stride - 1, p % self.stride - 1

    @property
    def max_moves(self) -> int:
        return 3 * self.n * self.n

    def over(self) -> bool:
        return self.passes >= 2 or self.moves >= self.max_moves

    def legal(self, p: int) -> bool:
        return bool(is_legal(self.cells, p, self.to_play, self.ko, self.stride, self._mark, self._stamp, self._buf))

    def legal_moves(self, skip_eyes: bool = False) -> np.ndarray:
        out = np.empty(self.n * self.n, dtype=np.int64)
        m = legal_moves(self.cells, self.to_play, self.ko, self.n, self.stride, self._mark, self._stamp, self._buf, out, skip_eyes)
        return out[:m]

    def play(self, p: int) -> int:
        """Play a move (must be legal). Returns stones captured."""
        if p == PASS:
            self.passes += 1
            self.ko = PASS
            cap = 0
        else:
            cap, self.ko = play(self.cells, p, self.to_play, self.stride, self._mark, self._stamp, self._buf)
            self.passes = 0
        self.history.append(p)
        self.to_play = other(self.to_play)
        self.moves += 1
        return int(cap)

    def score(self) -> float:
        """Black minus white, area scoring with komi."""
        return float(area_score(self.cells, self.n, self.stride, self.komi))

    def winner(self) -> int:
        return BLACK if self.score() > 0 else WHITE

    def grid(self) -> np.ndarray:
        """n x n array of 0/1/2, row 0 at the top."""
        s = self.stride
        return self.cells.reshape(s, s)[1:-1, 1:-1].copy()

    def __str__(self) -> str:
        sym = {EMPTY: ".", BLACK: "X", WHITE: "O"}
        return "\n".join(" ".join(sym[int(v)] for v in row) for row in self.grid())
