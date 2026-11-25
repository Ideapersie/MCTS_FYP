"""Play agents against each other and log the result.

Games alternate colours, every game has its own seed, and games run in
parallel processes. Each match appends one row to results/ladder.csv with the
git commit, so every number the README or the portfolio quotes can be traced
to a row here.

    python -m mctslab.arena uct fyp_flat --size 7 --playouts 400 --games 100
"""

from __future__ import annotations

import argparse
import csv
import math
import multiprocessing as mp
import os
import subprocess
import time
from datetime import datetime, timezone

from .agents import make
from .board import BLACK, PASS, Board, default_komi

RESIGN = -2
LADDER = os.path.join(os.path.dirname(__file__), "..", "results", "ladder.csv")
FIELDS = ["when", "commit", "size", "komi", "playouts", "a", "b", "games", "a_wins", "a_rate", "ci_low", "ci_high",
          "a_black_rate", "a_white_rate", "sec_per_game", "note", "a_margin", "margin_ci", "resigns", "black_rate"]


def wilson(wins: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = wins / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def play_game(args) -> tuple[int, int, float, int]:
    """Returns (winner colour, colour agent A played, final score black minus
    white, colour that resigned or 0).

    A resignation decides the game, but the game is then played out to the end
    by the same agents with resignation switched off, so the score is a real
    area score rather than the old "lost by the whole board" placeholder."""
    spec_a, spec_b, size, komi, playouts, seed, a_colour = args
    a = make(spec_a, playouts, seed)
    b = make(spec_b, playouts, seed + 1)
    players = {a_colour: a, 3 - a_colour: b}
    board = Board(size, komi)
    resigned = 0
    while not board.over():
        agent = players[board.to_play]
        mv = agent.select(board)
        if mv == RESIGN:
            resigned = resigned or board.to_play
            for ag in (a, b):
                if hasattr(ag, "resign"):
                    ag.resign = -1.0
            mv = agent.select(board)
            if mv == RESIGN:
                mv = PASS
        if mv != PASS and not board.legal(mv):
            mv = PASS
        mover = board.to_play
        cap = board.play(mv)
        for ag in (a, b):
            if hasattr(ag, "observe"):
                ag.observe(mover, cap)
            if hasattr(ag, "advance"):
                ag.advance(mv)
    winner = 3 - resigned if resigned else board.winner()
    return winner, a_colour, board.score(), resigned


def commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True,
                                       cwd=os.path.dirname(__file__)).strip()
    except Exception:
        return "unknown"


def _migrate():
    """Add columns introduced after a ladder was started; old rows get blanks."""
    if not os.path.exists(LADDER):
        return
    with open(LADDER, newline="") as f:
        rows = list(csv.DictReader(f))
        header = rows and list(rows[0].keys())
    if not rows or header == FIELDS:
        return
    with open(LADDER, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) or "" for k in FIELDS})


def match(spec_a, spec_b, size=7, komi=None, playouts=400, games=100, seed=0, procs=None, note="", log=True):
    komi = default_komi(size) if komi is None else komi
    jobs = [(spec_a, spec_b, size, komi, playouts, seed + 1000 * g, BLACK if g % 2 == 0 else 3 - BLACK)
            for g in range(games)]
    t = time.time()
    with mp.Pool(procs or os.cpu_count()) as pool:
        results = pool.map(play_game, jobs, chunksize=1)
    secs = (time.time() - t) / games * (procs or os.cpu_count())
    a_wins = sum(w == ac for w, ac, _, _ in results)
    a_b = [w == ac for w, ac, _, _ in results if ac == BLACK]
    a_w = [w == ac for w, ac, _, _ in results if ac != BLACK]
    black_wins = sum(w == BLACK for w, _, _, _ in results)
    resigns = sum(r != 0 for _, _, _, r in results)
    # Score margin from A's side: still informative when colour decides most games.
    # Resigned games were played out, so every margin is a real area score.
    margins = [sc if ac == BLACK else -sc for _, ac, sc, _ in results]
    m = sum(margins) / len(margins)
    sd = (sum((x - m) ** 2 for x in margins) / max(len(margins) - 1, 1)) ** 0.5
    half = 1.96 * sd / math.sqrt(len(margins))
    lo, hi = wilson(a_wins, games)
    row = {
        "when": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), "commit": commit(), "size": size, "komi": komi,
        "playouts": playouts, "a": spec_a, "b": spec_b, "games": games, "a_wins": a_wins,
        "a_rate": round(a_wins / games, 3), "ci_low": round(lo, 3), "ci_high": round(hi, 3),
        "a_black_rate": round(sum(a_b) / max(len(a_b), 1), 3), "a_white_rate": round(sum(a_w) / max(len(a_w), 1), 3),
        "sec_per_game": round(secs, 2), "note": note,
        "a_margin": round(m, 2), "margin_ci": f"{m - half:.2f} to {m + half:.2f}",
        "resigns": resigns, "black_rate": round(black_wins / games, 3),
    }
    if log:
        _migrate()
        new = not os.path.exists(LADDER)
        with open(LADDER, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerow(row)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--komi", type=float, default=None)
    ap.add_argument("--playouts", type=int, default=400)
    ap.add_argument("--games", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--note", default="")
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    r = match(a.a, a.b, a.size, a.komi, a.playouts, a.games, a.seed, note=a.note, log=not a.no_log)
    print(f"{r['a']} vs {r['b']} on {r['size']}x{r['size']} at {r['playouts']} playouts: "
          f"{r['a_wins']}/{r['games']} = {r['a_rate']:.0%} (95% CI {r['ci_low']:.0%} to {r['ci_high']:.0%}), "
          f"as black {r['a_black_rate']:.0%}, as white {r['a_white_rate']:.0%}, "
          f"mean margin {r['a_margin']:+.1f} points ({r['margin_ci']}), black won {r['black_rate']:.0%}, "
          f"{r['resigns']} resigned (played out), {r['sec_per_game']}s per game")


if __name__ == "__main__":
    main()
