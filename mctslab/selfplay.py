"""Generate training games.

teacher: UCT with RAVE and heavy playouts plays itself; the policy target is the root's visit share.
net:     PUCT with the current network plays itself, with root noise and
         sampled opening moves, AlphaZero style.
Each game yields (planes, policy, outcome-for-side-to-move) for every move.

    python -m mctslab.selfplay teacher --games 400 --playouts 800 --out results/selfplay/teacher.npz
"""

import argparse
import multiprocessing as mp
import os

import numpy as np

from .agents.uct import UCT
from .board import BLACK, PASS, Board
from .features import encode, move_index

RESIGN = -2


def _teacher_pi(agent: UCT, board: Board, root) -> np.ndarray:
    n = board.n
    pi = np.zeros(n * n + 1, dtype=np.float32)
    for m, ch in root.children.items():
        pi[move_index(board, m)] = ch.n
    return pi / max(pi.sum(), 1)


def game(args):
    mode, size, komi, playouts, seed, weights = args
    rng = np.random.default_rng(seed)
    board = Board(size, komi)
    xs, pis, sides = [], [], []
    if mode == "teacher":
        agent = UCT(playouts=playouts, seed=seed, rave=1, k=300, heavy=1)
    else:
        from .agents.puct import PUCT

        agent = PUCT(playouts=playouts, seed=seed, noise=1, temp_moves=8, weights=weights)
    while not board.over():
        if mode == "teacher":
            root = agent.search(board)
            pi = _teacher_pi(agent, board, root)
            moves = list(root.children.keys())
            visits = np.array([root.children[m].n for m in moves], dtype=float)
            if not moves:
                mv = PASS
            elif board.moves < 6:
                mv = moves[int(rng.choice(len(moves), p=visits / visits.sum()))]
            else:
                mv = moves[int(np.argmax(visits))]
        else:
            mv = agent.select(board)
            pi = agent.last_pi
        xs.append(encode(board))
        pis.append(pi)
        sides.append(board.to_play)
        board.play(mv)
    winner = board.winner()
    z = np.array([1.0 if s == winner else -1.0 for s in sides], dtype=np.float32)
    return np.stack(xs), np.stack(pis), z


def run(mode, games, size, komi, playouts, out, seed=0, weights="weights/best.pt", procs=None):
    jobs = [(mode, size, komi, playouts, seed + g, weights) for g in range(games)]
    with mp.Pool(procs or os.cpu_count()) as pool:
        res = pool.map(game, jobs, chunksize=1)
    X = np.concatenate([r[0] for r in res])
    P = np.concatenate([r[1] for r in res])
    Z = np.concatenate([r[2] for r in res])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    np.savez_compressed(out, x=X, pi=P, z=Z)
    black_wins = sum(r[2][0] > 0 for r in res)
    print(f"{games} games, {len(X)} positions, black won {black_wins}/{games} -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["teacher", "net"])
    ap.add_argument("--games", type=int, default=100)
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--komi", type=float, default=9.0)
    ap.add_argument("--playouts", type=int, default=800)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--weights", default="weights/best.pt")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.mode, a.games, a.size, a.komi, a.playouts, a.out, a.seed, a.weights)
