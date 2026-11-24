"""The AlphaZero-style loop on 7x7, sized for a laptop CPU.

0. Bootstrap: train the net on teacher games (UCT + RAVE).
1. Self-play with the current best net (PUCT, root noise, sampled openings).
2. Train a candidate on the latest games plus a window of older ones.
3. Gate: the candidate replaces the best net if it wins at least 55% of the
   gate games, or its mean score margin is above zero with 95% confidence.
   Every gate match is logged to the ladder.

    python -m mctslab.iterate --iters 3
"""

import argparse
import glob
import os
import shutil

from .arena import match
from .selfplay import run as selfplay
from .train import train

W = "weights"
D = "results/selfplay"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=3)
    ap.add_argument("--games", type=int, default=200)
    ap.add_argument("--sims", type=int, default=96)
    ap.add_argument("--gate-games", type=int, default=100)
    ap.add_argument("--window", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(W, exist_ok=True)
    best = os.path.join(W, "best.pt")
    if not os.path.exists(best):
        train(sorted(glob.glob(f"{D}/teacher*.npz")), best, n=7, epochs=14)
        shutil.copy(best, os.path.join(W, "gen0.pt"))
    gen = len(glob.glob(f"{W}/gen*.pt")) - 1
    for _ in range(a.iters):
        k = len(glob.glob(f"{D}/net_*.npz"))
        out = f"{D}/net_gen{gen}_{k}.npz"
        # A new seed every iteration, promoted or not, so no game is replayed.
        selfplay("net", a.games, 7, 9.0, a.sims, out, seed=10000 + k * 1000, weights=best)
        files = sorted(glob.glob(f"{D}/net_*.npz"), key=os.path.getmtime)[-a.window:] + sorted(glob.glob(f"{D}/teacher*.npz"))
        cand = os.path.join(W, "candidate.pt")
        train(files, cand, n=7, epochs=8, init=best)
        # The first 6 moves are sampled by visit count; otherwise two deterministic
        # nets replay the same two games and the gate measures nothing.
        r = match(f"puct:weights={cand},temp_moves=6", f"puct:weights={best},temp_moves=6", size=7, playouts=a.sims, games=a.gate_games,
                  note=f"gate: candidate vs gen{gen}")
        print(f"gate: {r['a_wins']}/{r['games']}, margin {r['a_margin']:+.1f} ({r['margin_ci']})")
        # Promote on a clear win rate, or on a margin whose interval is above zero
        # (on 7x7 with komi 9 colour decides many games, so the margin is the finer signal).
        if r["a_rate"] >= 0.55 or float(r["margin_ci"].split(" to ")[0]) > 0:
            gen += 1
            shutil.copy(cand, os.path.join(W, f"gen{gen}.pt"))
            shutil.copy(cand, best)
            print(f"promoted to gen{gen}")
        else:
            print("kept the current best")


if __name__ == "__main__":
    main()
