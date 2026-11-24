"""UCT with optional RAVE, tree reuse and prior knowledge.

- Selection: UCB1 on win rate from the point of view of the player who made
  the move, so each level maximises for the side to move (the minimax view
  the FYP agent and the browser port were missing).
- Expansion: one untried move per simulation, in random order. Pass is a
  candidate once the board is half full.
- Simulation: random playout to the end, never filling own eyes, area scoring.
- Move choice: the most visited child (robust child), not the best win rate.
- rave=1: AMAF statistics blended in with beta = sqrt(k / (3n + k)), the
  classic MoGo schedule; selection then uses no exploration term.
- reuse=1: keep the subtree under the moves actually played.
"""

import math

import numpy as np

from ..board import BLACK, PASS, Board, playout

RESIGN = -2


class Node:
    __slots__ = ("move", "parent", "children", "untried", "n", "w", "rn", "rw", "to_play")

    def __init__(self, move, parent, to_play):
        self.move = move
        self.parent = parent
        self.children = {}
        self.untried = None
        self.n = 0
        self.w = 0.0  # wins for the player who played `move`
        self.rn = 0  # AMAF visits
        self.rw = 0.0
        self.to_play = to_play  # side to move at this node


class UCT:
    name = "uct"

    def __init__(self, playouts=1000, seed=0, c=1.0, rave=0, k=600, reuse=0, resign=0.05):
        self.playouts = playouts
        self.rng = np.random.default_rng(seed)
        self.c = c
        self.rave = bool(rave)
        self.k = k
        self.reuse = bool(reuse)
        self.resign = resign
        self.root = None

    # Tree helpers
    def _moves(self, board: Board):
        m = board.legal_moves(skip_eyes=True)
        self.rng.shuffle(m)
        moves = [int(x) for x in m]
        stones = int(np.count_nonzero((board.cells == 1) | (board.cells == 2)))
        if stones >= board.n * board.n // 2 or not moves:
            moves.append(PASS)
        return moves

    def _score(self, parent: Node, child: Node, log_n: float) -> float:
        q = child.w / child.n
        if self.rave and child.rn:
            beta = math.sqrt(self.k / (3 * parent.n + self.k))
            q = (1 - beta) * q + beta * (child.rw / child.rn)
            return q + self.c * 0.3 * math.sqrt(log_n / child.n)
        return q + self.c * math.sqrt(log_n / child.n)

    def _select(self, node: Node) -> Node:
        log_n = math.log(node.n)
        best, best_s = None, -1e9
        for ch in node.children.values():
            s = self._score(node, ch, log_n)
            if s > best_s:
                best, best_s = ch, s
        return best

    def search(self, board: Board) -> Node:
        if self.root is None or not self.reuse:
            self.root = Node(None, None, board.to_play)
        root = self.root
        size = board.cells.shape[0]
        amaf = np.zeros(size, dtype=np.int8)
        for _ in range(self.playouts):
            node, b = root, board.copy()
            path_moves = []
            # Selection
            while True:
                if node.untried is None:
                    node.untried = self._moves(b)
                if node.untried or b.over():
                    break
                node = self._select(node)
                b.play(node.move)
                path_moves.append((node.move, 3 - node.to_play))
            # Expansion
            if node.untried and not b.over():
                m = node.untried.pop()
                mover = b.to_play
                b.play(m)
                ch = Node(m, node, b.to_play)
                node.children[m] = ch
                node = ch
                path_moves.append((m, mover))
            # Simulation
            amaf[:] = 0
            for m, col in path_moves:
                if m != PASS and amaf[m] == 0:
                    amaf[m] = col
            if b.over():
                score = b.score()
            else:
                score = playout(b.cells, b.to_play, b.ko, b.n, b.komi, b.max_moves - b.moves,
                                int(self.rng.integers(2**31)), amaf)
            winner = BLACK if score > 0 else 3 - BLACK
            # Backpropagation
            while node is not None:
                node.n += 1
                mover = 3 - node.to_play  # who played node.move
                if winner == mover:
                    node.w += 1
                if self.rave:
                    # AMAF: credit every child whose move the same player made later in this simulation
                    for mv, ch in node.children.items():
                        if mv != PASS and amaf[mv] == node.to_play:
                            ch.rn += 1
                            if winner == node.to_play:
                                ch.rw += 1
                node = node.parent
        return root

    def select(self, board: Board) -> int:
        root = self.search(board)
        if not root.children:
            return PASS
        best = max(root.children.values(), key=lambda ch: ch.n)
        if best.w / best.n < self.resign:
            return RESIGN
        return best.move

    def advance(self, move: int):
        """Tree reuse: descend into the subtree of the move just played."""
        if not self.reuse or self.root is None:
            return
        ch = self.root.children.get(move)
        if ch is None:
            self.root = None
        else:
            ch.parent = None
            self.root = ch
