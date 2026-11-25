import os
import random
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "product"))

from mctslab.board import BLACK, PASS, WHITE, Board, is_eye  # noqa: E402


def place(b: Board, stones: str):
    """Set up a position from rows of X/O/. (row 0 at the top)."""
    for r, row in enumerate(stones.split()):
        for c, ch in enumerate(row):
            if ch in "XO":
                b.cells[b.point(r, c)] = BLACK if ch == "X" else WHITE


def test_capture_and_ko():
    b = Board(5)
    place(b, """
        .XO..
        X.XO.
        .XO..
        .....
        .....
    """)
    b.to_play = WHITE
    # White takes the black stone at (1,2) by playing (1,1)
    cap = b.play(b.point(1, 1))
    assert cap == 1 and b.cells[b.point(1, 2)] == 0
    # Black may not retake at once: that is ko
    assert not b.legal(b.point(1, 2))
    b.play(b.point(4, 4))  # black plays elsewhere
    b.play(b.point(4, 0))  # white answers
    assert b.legal(b.point(1, 2))


def test_suicide_illegal_but_capture_legal():
    b = Board(5)
    place(b, """
        .X...
        X....
        .....
        .....
        .....
    """)
    b.to_play = WHITE
    assert not b.legal(b.point(0, 0))  # no liberties, captures nothing
    b2 = Board(5)
    place(b2, """
        OX...
        .O...
        .....
        .....
        .....
    """)
    b2.cells[b2.point(1, 1)] = BLACK
    b2.to_play = BLACK
    assert b2.legal(b2.point(1, 0))  # captures the white stone at (0,0)
    assert b2.play(b2.point(1, 0)) == 1


def test_area_score_counts_stones_and_territory():
    b = Board(5, komi=0.0)
    place(b, """
        .X.O.
        .X.O.
        .X.O.
        .X.O.
        .X.O.
    """)
    # Black: 5 stones + 5 territory (column 0); white: 5 + 5 (column 4); column 2 is neutral
    assert b.score() == 0.0
    b.komi = 7.0
    assert b.score() == -7.0


def test_eye_detection():
    b = Board(5)
    place(b, """
        .X...
        XX...
        .....
        .....
        .....
    """)
    assert is_eye(b.cells, b.point(0, 0), BLACK, b.stride)
    b.cells[b.point(1, 1)] = WHITE  # an enemy diagonal on the edge breaks the eye
    assert not is_eye(b.cells, b.point(0, 0), BLACK, b.stride)
    assert not is_eye(b.cells, b.point(0, 0), WHITE, b.stride)


def test_legal_moves_match_the_original_engine():
    """On random games, the fast board allows exactly the moves the FYP engine allows."""
    from menus.go.goboard import GoState, Move
    from menus.go.goplayer import Point

    rng = random.Random(7)
    for game in range(4):
        fast = Board(5)
        slow = GoState.new_game(5)
        for _ in range(40):
            ours = {fast.rc(int(p)) for p in fast.legal_moves()}
            theirs = {(pt.row - 1, pt.col - 1) for pt in slow.legal_moves()}
            assert ours == theirs, (game, str(fast))
            if not ours:
                break
            r, c = rng.choice(sorted(ours))
            fast.play(fast.point(r, c))
            slow = slow.play_move(Move.play(Point(r + 1, c + 1)))


def test_game_ends_after_two_passes():
    b = Board(5)
    b.play(PASS)
    assert not b.over()
    b.play(PASS)
    assert b.over()
