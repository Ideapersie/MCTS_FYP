import unittest
from menus.go.goboard import Move
from menus.go.goplayer import Player, Point
from menus.go.fast_go import FastBoard, FastGoState

class TestFastBoard(unittest.TestCase):
    def setUp(self):
        self.board = FastBoard(9, 9)
        self.state = FastGoState(9)
        self.state.board = self.board

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
        
    # Empty board should have 81 legal moves for 9x9 board 
    def test_legal_moves_empty_board(self):
        moves = self.board.fast_legal_moves(Player.black)
        self.assertEqual(len(moves), 81)
        
    # Test for one move on the board
    def test_legal_moves_one_moves(self):
        self.board.grid[3, 3] = 1
        moves = self.board.fast_legal_moves(Player.white)
        self.assertEqual(len(moves), 80)
        self.assertTrue(Point(3, 3) not in moves)
        
    # Test for no captures
    def test_handle_captures_no_captures(self):
        # Set up board with no captures
        self.state.board.grid[3, 3] = 1  
        self.state.board.grid[2, 3] = 2
        # Should have no captures 
        captures = self.state.handle_captures(Point(3, 3))
        self.assertEqual(captures, 0)
        
        # [3,3] should still be a black stone
        self.assertEqual(self.board.grid[3, 3], 1)
        
        
    # Test for capturing a single stone
    def test_handle_captures_single_stone(self):
        # Set up board with black stone surrounded by white stones
        self.state.board.grid[3, 3] = 1  
        self.state.board.grid[2, 3] = 2  
        self.state.board.grid[4, 3] = 2  
        self.state.board.grid[3, 2] = 2  
        
        # Set next_player to white (the capturing player)
        self.state.next_player = Player.white
        # Place the capturing stone
        self.state.board.grid[3, 4] = 2 
        
        # Check if the black stone is captured
        captures = self.state.handle_captures(Point(3, 4))  # Right side
        # Check if the black stone is removed
        self.assertEqual(captures, 1)
        self.assertEqual(self.board.grid[3, 3], 0)

    # Test for capturing multiple stones
    def test_handle_captures_multiple_stones(self):
        # Black stones
        self.state.board.grid[3, 3] = 1
        self.state.board.grid[4, 3] = 1
        # White stones
        self.state.board.grid[2, 3] = 2
        self.state.board.grid[3, 2] = 2
        self.state.board.grid[3, 4] = 2
        self.state.board.grid[4, 2] = 2
        self.state.board.grid[4, 4] = 2
        
        # Set next_player to white (the capturing player)
        self.state.next_player = Player.white
        # Place the capturing stone
        self.state.board.grid[5, 3] = 2 
        
        # Check if the black stone is captured
        captures = self.state.handle_captures(Point(3, 3))  
        captures += self.state.handle_captures(Point(4, 3))  
        
        # Check if the black stone is removed
        self.assertEqual(captures, 2)
        self.assertEqual(self.board.grid[3, 3], 0)
        self.assertEqual(self.board.grid[4, 3], 0)
    
    def test_fast_move(self):
        # Place black stone
        point = Point(3, 3)
        self.state.fast_play_move(Move.play(point))
        
        # Check if the stone is placed by black player first 
        self.assertEqual(self.board.grid[3, 3], 1)
        self.assertEqual(self.state.next_player, Player.white)
        self.assertEqual(self.state.last_move.point, point)
        
        # # Check if the stone is placed by white player next 
        point = Point(4, 4)
        self.state.fast_play_move(Move.play(point))
        self.assertEqual(self.board.grid[4, 4], 2)
        self.assertEqual(self.state.next_player, Player.black)
        self.assertEqual(self.state.last_move.point, point)
        
    # Test for pass move
    def test_fast_pass_move(self):
        # Place black stone
        point = Point(3, 3)
        self.state.fast_play_move(Move.play(point))
        
        # Pass move
        self.state.fast_play_move(Move.pass_turn())
        self.assertEqual(self.state.next_player, Player.black)
        self.assertTrue(self.state.last_move.is_pass)
        
    def test_fast_two_pass_moves(self):
        # Place black stone
        point = Point(3, 3)
        self.state.fast_play_move(Move.play(point))
        
        # 2 Pass moves
        self.state.fast_play_move(Move.pass_turn())
        self.state.fast_play_move(Move.pass_turn())
        # Check if game is over
        self.assertTrue(self.state.last_move.is_pass)
        self.assertTrue(self.state.previous_pass)
        self.assertTrue(self.state.fast_game_over())
        
    # Test for resignation
    def test_fast_resign(self):
        # Place black stone 
        # Place black stone
        point = Point(3, 3)
        self.state.fast_play_move(Move.play(point))
        
        # Resign move
        self.state.fast_play_move(Move.resign())
        
        self.assertTrue(self.state.is_resigned)
        self.assertTrue(self.state.fast_game_over())

if __name__ == '__main__':
    unittest.main()