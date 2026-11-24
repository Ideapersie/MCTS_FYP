import numpy as np

from mctslab.agents import make
from mctslab.agents.uct import UCT
from mctslab.arena import play_game, wilson
from mctslab.board import BLACK, WHITE, Board


def test_uct_takes_a_free_capture():
    """A white group in atari next to black's centre: capturing it is clearly best."""
    b = Board(5, komi=0.0)
    for r, c in [(1, 2), (3, 2), (2, 1), (1, 3), (3, 3)]:
        b.cells[b.point(r, c)] = BLACK
    for r, c in [(2, 2), (2, 3)]:
        b.cells[b.point(r, c)] = WHITE
    b.cells[b.point(2, 4)] = 0  # the last liberty
    b.to_play = BLACK
    move = UCT(playouts=600, seed=1, heavy=1).select(b)
    assert move == b.point(2, 4)


def test_uct_beats_random():
    wins = 0
    for g in range(4):
        w, a_colour = play_game(("uct", "random", 5, 3.0, 150, g, BLACK if g % 2 == 0 else WHITE))
        wins += w == a_colour
    assert wins >= 3


def test_make_parses_options():
    a = make("uct:rave=1,c=0.7,k=300", 10, 0)
    assert a.rave and a.c == 0.7 and a.k == 300


def test_wilson_interval():
    lo, hi = wilson(50, 100)
    assert 0.39 < lo < 0.41 and 0.59 < hi < 0.61
