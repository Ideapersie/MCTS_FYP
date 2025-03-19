import unittest
from menus.go.goplayer import Player, Point
from menus.go.fast_go import FastBoard

class TestFastBoard(unittest.TestCase):
    def setUp(self):
        self.board = FastBoard(9, 9)

    def test_initial_board_empty(self):
        for row in range(1, 10):
            for col in range(1, 10):
                self.assertEqual(self.board.grid[row, col], 0)

    def test_place_black_stone(self):
        point = Point(3, 3)
        self.board.grid[point.row, point.col] = 1
        self.assertEqual(self.board.grid[point.row, point.col], 1)

    def test_place_white_stone(self):
        point = Point(4, 4)
        self.board.grid[point.row, point.col] = 2
        self.assertEqual(self.board.grid[point.row, point.col], 2)

    # Test for self capture, with no liberties
    def test_fast_self_capture_no_liberties(self):
        self.board.grid[2, 3] = 2
        self.board.grid[4, 3] = 2
        self.board.grid[3, 2] = 2
        self.board.grid[3, 4] = 2
        # Place black stone in the middle, self capture move
        point = Point(3, 3)
        self.assertTrue(self.board.fast_self_capture(point, Player.black))

    # Test for self capture, where white captures
    def test_fast_self_capture_white_capture(self):
        self.board.grid[3, 3] = 1
        self.board.grid[2, 3] = 2
        self.board.grid[4, 3] = 2
        self.board.grid[3, 2] = 2
        # White capturing black stone, no self capture
        point = Point(3, 4)
        self.assertFalse(self.board.fast_self_capture(point, Player.black))

    def test_has_no_liberties_except(self):
        self.board.grid[3, 3] = 1
        self.board.grid[2, 3] = 2
        self.board.grid[4, 3] = 2
        self.board.grid[3, 2] = 2
        self.board.grid[3, 4] = 2
        self.assertTrue(self.board.has_no_liberties_except(3, 3, 3, 4))

if __name__ == '__main__':
    unittest.main()