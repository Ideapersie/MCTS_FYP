"""PUCT search guided by the policy and value network (AlphaZero, scaled down).

No playouts: a leaf is valued by the network. Selection maximises
Q + c * P * sqrt(N_parent) / (1 + N_child). The move played is the most
visited child; in self-play the first moves are sampled by visit count and
the root gets Dirichlet noise, so games differ.
"""

import math

import numpy as np
import torch

from ..board import BLACK, PASS, Board
from ..features import encode, index_move, move_index
from ..net import PolicyValueNet

RESIGN = -2


class PNode:
    __slots__ = ("prior", "n", "w", "children", "to_play")

    def __init__(self, prior, to_play):
        self.prior = prior
        self.n = 0
        self.w = 0.0  # value for the player who moved into this node
        self.children = None
        self.to_play = to_play


_NETS = {}


def load(path):
    if path not in _NETS:
        ck = torch.load(path, map_location="cpu", weights_only=False)
        net = PolicyValueNet(**ck["config"])
        net.load_state_dict(ck["state"])
        net.eval()
        _NETS[path] = net
    return _NETS[path]


class PUCT:
    name = "puct"

    def __init__(self, playouts=100, seed=0, c=1.5, net=None, noise=0, temp_moves=0, weights="weights/best.pt"):
        torch.set_num_threads(1)
        self.playouts = playouts
        self.rng = np.random.default_rng(seed)
        self.c = c
        self.noise = bool(noise)
        self.temp_moves = temp_moves
        self.net = net if net is not None else load(weights)
        self.last_pi = None

    @torch.no_grad()
    def _evaluate(self, b: Board):
        logits, v = self.net(torch.from_numpy(encode(b))[None])
        logits = logits[0].numpy()
        n = b.n
        legal = np.zeros(n * n + 1, dtype=bool)
        for p in b.legal_moves():
            legal[move_index(b, int(p))] = True
        legal[n * n] = True
        logits = np.where(legal, logits, -1e9)
        p = np.exp(logits - logits.max())
        p /= p.sum()
        return p, float(v[0])

    def _expand(self, node: PNode, b: Board):
        p, v = self._evaluate(b)
        node.children = {}
        for i in np.flatnonzero(p > 0):
            node.children[index_move(b, int(i))] = PNode(float(p[i]), 3 - b.to_play)
        return v  # from the side to move at node

    def search(self, board: Board) -> PNode:
        root = PNode(1.0, board.to_play)
        self._expand(root, board)
        if self.noise and root.children:
            eta = self.rng.dirichlet([0.3] * len(root.children))
            for (m, ch), e in zip(root.children.items(), eta):
                ch.prior = 0.75 * ch.prior + 0.25 * e
        for _ in range(self.playouts):
            node, b, path = root, board.copy(), [root]
            while node.children:
                sq = math.sqrt(node.n + 1)
                best, best_s, best_m = None, -1e9, None
                for m, ch in node.children.items():
                    q = ch.w / ch.n if ch.n else 0.0
                    s = q + self.c * ch.prior * sq / (1 + ch.n)
                    if s > best_s:
                        best, best_s, best_m = ch, s, m
                b.play(best_m)
                node = best
                path.append(node)
                if b.over():
                    break
            if b.over():
                v_mover = 1.0 if (b.score() > 0) == (3 - b.to_play == BLACK) else -1.0
                # v for the side to move at the leaf is the negative of the mover's
                v = -v_mover
            else:
                v = self._expand(node, b)
            # v is from the side to move at `node`; node.w is for the player who moved into it
            for nd in reversed(path):
                nd.n += 1
                nd.w += -v
                v = -v
        return root

    def select(self, board: Board) -> int:
        root = self.search(board)
        moves = list(root.children.keys())
        visits = np.array([root.children[m].n for m in moves], dtype=np.float64)
        n = board.n
        pi = np.zeros(n * n + 1, dtype=np.float32)
        for m, c in zip(moves, visits):
            pi[move_index(board, m)] = c
        pi /= max(pi.sum(), 1)
        self.last_pi = pi
        if board.moves < self.temp_moves:
            i = int(self.rng.choice(len(moves), p=visits / visits.sum()))
        else:
            i = int(np.argmax(visits))
        return moves[i]
