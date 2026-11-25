"""The AlphaZero-style loop, sized for a laptop CPU. Works for any board size.

0. Bootstrap: train the net on teacher games (UCT + RAVE) at this size and
   komi, generating them first if there are none.
1. Self-play with the current best net (PUCT, root noise, sampled openings).
2. Train a candidate on the latest games (same size and komi only, since the
   value target depends on komi).
3. Gate: the candidate replaces the best net if it wins at least 55% of the
   gate games, or its mean score margin is above zero with 95% confidence.
   Every gate match is logged to the ladder.

    python -m mctslab.iterate --iters 3                       # 7x7, default komi
    python -m mctslab.iterate --size 9 --wdir weights/9x9 --iters 0 --teacher-games 100 --boot-epochs 6
"""

import argparse
import glob
import os
import shutil

from .arena import match
from .board import default_komi
from .selfplay import run as selfplay
from .train import train

D = "results/selfplay"


def tag(size, komi):
    return f"s{size}_k{komi:g}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=3)
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--komi", type=float, default=None)
    ap.add_argument("--wdir", default="weights", help="weights directory for this size")
    ap.add_argument("--games", type=int, default=200)
    ap.add_argument("--sims", type=int, default=96)
    ap.add_argument("--gate-games", type=int, default=100)
    ap.add_argument("--window", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--teacher-games", type=int, default=300)
    ap.add_argument("--teacher-playouts", type=int, default=300)
    ap.add_argument("--boot-epochs", type=int, default=14)
    ap.add_argument("--blocks", type=int, default=4)
    ap.add_argument("--ch", type=int, default=32)
    a = ap.parse_args()
    size = a.size
    komi = default_komi(size) if a.komi is None else a.komi
    t = tag(size, komi)
    W = a.wdir
    os.makedirs(W, exist_ok=True)
    best = os.path.join(W, "best.pt")
    if not os.path.exists(best):
        teach = sorted(glob.glob(f"{D}/teacher_{t}*.npz"))
        if not teach:
            out = f"{D}/teacher_{t}_0.npz"
            selfplay("teacher", a.teacher_games, size, komi, a.teacher_playouts, out, seed=0)
            teach = [out]
        train(teach, best, n=size, epochs=a.boot_epochs, blocks=a.blocks, ch=a.ch)
        shutil.copy(best, os.path.join(W, "gen0.pt"))
    gen = len(glob.glob(f"{W}/gen*.pt")) - 1
    for _ in range(a.iters):
        k = len(glob.glob(f"{D}/net_{t}_*.npz"))
        out = f"{D}/net_{t}_gen{gen}_{k}.npz"
        # A new seed every iteration, promoted or not, so no game is replayed.
        selfplay("net", a.games, size, komi, a.sims, out, seed=10000 + k * 1000, weights=best)
        # Only data from this size and komi: the outcome labels depend on komi.
        files = sorted(glob.glob(f"{D}/net_{t}_*.npz"), key=os.path.getmtime)[-a.window:]
        files += sorted(glob.glob(f"{D}/teacher_{t}*.npz"))
        cand = os.path.join(W, "candidate.pt")
        train(files, cand, n=size, epochs=a.epochs, init=best)
        # The first 6 moves are sampled by visit count; otherwise two deterministic
        # nets replay the same two games and the gate measures nothing.
        r = match(f"puct:weights={cand},temp_moves=6", f"puct:weights={best},temp_moves=6", size=size, komi=komi,
                  playouts=a.sims, games=a.gate_games, note=f"gate: candidate vs gen{gen} ({W})")
        print(f"gate: {r['a_wins']}/{r['games']}, margin {r['a_margin']:+.1f} ({r['margin_ci']})")
        # Promote on a clear win rate, or on a margin whose interval is above zero
        # (when colour decides most games, the margin is the finer signal).
        if r["a_rate"] >= 0.55 or float(r["margin_ci"].split(" to ")[0]) > 0:
            gen += 1
            shutil.copy(cand, os.path.join(W, f"gen{gen}.pt"))
            shutil.copy(cand, best)
            print(f"promoted to gen{gen}")
        else:
            print("kept the current best")


if __name__ == "__main__":
    main()
