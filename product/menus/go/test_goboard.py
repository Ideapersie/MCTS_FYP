import unittest

from go.goplayer import Point, Player
from go.goboard import Move, GoString, Board, GoState

class TestMove(unittest.TestCase):
    def test_play(self):
        # Create test point (4, 4)
        point = Point(4,4)
        move = Move.play(point)
        
        # Assert the play move 
        self.assertTrue(move.is_play)
        self.assertFalse(move.is_pass)
        self.assertFalse(move.is_resign)
        self.assertEqual(move.point, point)
        
    def test_pass(self):
        # Create pass move
        move = Move.pass_turn()
        
        # Assert the pass move
        self.assertFalse(move.is_play)
        self.assertTrue(move.is_pass)
        self.assertFalse(move.is_resign)
        
    def test_resign(self):
        # Create resign move 
        move = Move.resign()
        
        # Assert resign move 
        self.assertFalse(move.is_play)
        self.assertFalse(move.is_pass)
        self.assertTrue(move.is_resign)
        
class TestGoString(unittest.TestCase):
    # Settings up stones with different lengths and no. of neighbours
    def setUp(self):
        self.str1 = GoString(Player.black, {(1,1)}, {(1,2),(2,1)})
        self.str2 = GoString(Player.black, {(2,1),(2,2)},{(1,1),(1,2),(2,3),(3,2),(3,1)})
        self.str3 = GoString(Player.white, {(3,3)},{(2,3),(4,3),(3,4),(3,2)})
        
    def test_init(self):
        self.assertEqual(self.str1.colour, Player.black)
        self.assertEqual(self.str1.stones, {(1,1)})
        self.assertEqual(self.str1.liberties, {(1,2),(2,1)})
    
    def test_add_liberty(self):
        self.str1.add_liberty((1,2))
        self.assertIn((1,2), self.str1.liberties)
        
    def test_remove_liberty(self):
        self.str1.remove_liberty((1,2))
        self.assertNotIn((1,2), self.str1.liberties)
        self.assertEqual(self.str1.num_liberties, 1)
        
    # Test combinining connected stones 
    def test_merged_with(self):
        merged_string = self.str1.merged_with(self.str2)
        expected_stones = {(1,1),(2,1),(2,2)}
        expected_liberties = {(1,2),(2,3),(3,2),(3,1)}
        
        self.assertEqual(merged_string.colour, Player.black)
        self.assertEqual(merged_string.stones, expected_stones)
        self.assertEqual(merged_string.liberties, expected_liberties)
        
    def test_num_liberties(self):
        self.assertEqual(self.str1.num_liberties, 2)
        self.assertEqual(self.str2.num_liberties, 5)
        
    def test_equal(self):
        str1_dup = GoString(Player.black, {(1,1)}, {(1,2),(2,1)})
        
        self.assertEqual(self.str1, str1_dup)
    
class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(9,9)

    # Testing board dimensions 
    def test_init(self):
    
        self.assertEqual(self.board.num_rows, 9)
        self.assertEqual(self.board.num_cols, 9)
        
       
    def test_str(self):
        # White stone at bottom left 
        self.board.place_stone(Player.white, Point(1,1))
        
        expected_str = (
            
            "9 . . . . . . . . .\n"
            "8 . . . . . . . . .\n"
            "7 . . . . . . . . .\n"
            "6 . . . . . . . . .\n"
            "5 . . . . . . . . .\n"
            "4 . . . . . . . . .\n"
            "3 . . . . . . . . .\n"
            "2 . . . . . . . . .\n"
            "1 . . . . . . . .\n"
            "  A B C D E F G H I "
        )
        self.assertEqual(expected_str.strip(), str(self.board).strip())
        
    def test_str_false(self):
        # White stone at bottom left 
        self.board.place_stone(Player.white, Point(1,1))
        # Black stones at top right
        self.board.place_stone(Player.black, Point(9,9))
        
        wrong_str = (
            
            "9 . . . . . . . . .\n"
            "8 . . . . . . . . .\n"
            "7 . . . . . . . . .\n"
            "6 . . . . . . . . .\n"
            "5 . . . . X . . . .\n"
            "4 . . . . . . . . .\n"
            "3 . . . . . . . . .\n"
            "2 . . . . . . . . .\n"
            "1 O . . . . . . . .\n"
            "  A B C D E F G H I "
        )
        # Altered expected_str to be wrong 
        self.assertNotEqual(str(self.board).strip(), wrong_str.strip())
        
        
    # Testing if the point is on the grind  
    def test_in_grid(self):
        in_grid_point = Point(2,2)
        too_low_grid_point = Point(0,0)
        too_high_grid_point = Point(10,9)
        
        self.assertTrue(self.board.in_grid(in_grid_point))
        self.assertFalse(self.board.in_grid(too_low_grid_point))
        self.assertFalse(self.board.in_grid(too_high_grid_point))
        
    # Testing if the point is out of bounds and error exception 
    def test_stone_out_of_bounds(self):
        out_of_bounds_point = Point(10,10)
        
        with self.assertRaises(ValueError) as error_msg:
            self.board.place_stone(Player.black, out_of_bounds_point)
            
        self.assertEqual(
            str(error_msg.exception),
            "Illegal move: The point Point(row=10, col=10) is outside the board's bound"                 
        )
             
    # Testing player colour of placing stone function and occupied point        
    def test_place_stone(self):
        point = Point(4,4)
        
        self.board.place_stone(Player.black, point)
        self.assertIn(point, self.board._grid)
        
        # Testing get_player function 
        self.assertEqual(self.board.get_player(point), Player.black)
        
        # Test get_player empty point
        self.assertIsNone(self.board.get_player(Point(3,3)))
        
        # Testing placing stone on occupied point
        with self.assertRaises(ValueError):
            self.board.place_stone(Player.white, point)
            
    def test_merge_strings(self):
        self.board.place_stone(Player.black, Point(1,1))
        self.board.place_stone(Player.black, Point(1,2))
        self.board.place_stone(Player.black, Point(1,3))
        
        # Check if stones are in the same GoString
        str1 = self.board.get_go_string(Point(1,1))
        str2 = self.board.get_go_string(Point(1,3))
        
        self.assertEqual(str1,str2)
        
    def test_remove_strings(self):
        # White stone
        self.board.place_stone(Player.white, Point(3,3))
        # Black stones surrounding it 
        self.board.place_stone(Player.black, Point(4,3))
        self.board.place_stone(Player.black, Point(2,3))
        self.board.place_stone(Player.black, Point(3,4))
        self.board.place_stone(Player.black, Point(3,2))
        
        # Testing the remove_string function
        self.assertIsNone(self.board.get_go_string(Point(3,3)))
        
        # Testing neutral territory with empty board
    def test_calculate_territory_empty(self):
        black, white, neutral = self.board.calculate_territory()
        
        self.assertEqual(black, 0)
        self.assertEqual(white, 0)
        self.assertEqual(neutral, 81)
        
    def test_eq_notinstance(self):
        self.assertNotEqual(self.board, "Not a board")
        self.assertNotEqual(self.board, None)
        
    def test_eq_dimensions(self):
        wrong_rows = Board(8,9)
        wrong_cols = Board(9,8)
        diff_dimensions = Board(13,13)
        
        # Test various dimension changes 
        self.assertNotEqual(self.board, wrong_rows)
        self.assertNotEqual(self.board, wrong_cols)
        self.assertNotEqual(self.board, diff_dimensions)
        
        
class TestGoState(unittest.TestCase):
    def setUp(self):
        self.board_size = 9 
        self.game = GoState.new_game(self.board_size)
        
    def test_game_initial_state(self):
        self.assertEqual(self.game.board.num_rows, self.board_size)
        self.assertEqual(self.game.board.num_cols, self.board_size)

        self.assertEqual(self.game.next_player.value, Player.black.value)
        self.assertIsNone(self.game.previous_state)

    # Testing different variables including current and next player
    def test_play_move(self):
        
        move = Move.play(Point(4,4))
        new_state = self.game.play_move(move)

        # Uses .value to compare the enum values instead of instances 
        self.assertEqual(new_state.board.get_player(Point(4,4)).value,Player.black.value)
        self.assertEqual(new_state.next_player.value, Player.white.value)
        self.assertEqual(new_state.last_move, move)
        self.assertEqual(new_state.previous_state, self.game)
        
    # Testing if move is pass
    def test_pass_move(self):
        move = Move.resign()
        new_state = self.game.play_move(move)
        
        # board should be unchanged 
        self.assertEqual(new_state.board, self.game.board)
        self.assertEqual(new_state.next_player.value, Player.white.value)
        self.assertEqual(new_state.last_move, move)
        self.assertEqual(new_state.previous_state, self.game)
      
    # Testing 1 move after another   
    def test_play_2_moves(self):
        move1 = Move.play(Point(3,3))
        move2 = Move.play(Point(4,4))
        
        play1 = self.game.play_move(move1)
        play2 = play1.play_move(move2)
        
        # Checking previous state
        self.assertEqual(play1.previous_state, self.game)
        self.assertEqual(play2.previous_state, play1)
        
        # Check if board state reflects the moves
        self.assertEqual(play1.board.get_player(Point(3, 3)).value, Player.black.value)
        self.assertEqual(play2.board.get_player(Point(4, 4)).value, Player.white.value)
        
    def test_play_capture(self):
        # the black stones are surrounding the (4,3) white stone
        black_move1 = Move.play(Point(3,3)) # left 
        white_move1 = Move.play(Point(4,3)) # middle 
        black_move2 = Move.play(Point(5,3)) # right
        white_move2 = Move.play(Point(1,1)) # elsewhere
        black_move3 = Move.play(Point(4,4)) # top 
        white_move3 = Move.play(Point(1,2)) # elsewhere 
        black_move4 = Move.play(Point(4,2)) # bottom
        
        play1 = self.game.play_move(black_move1)
        play2 = play1.play_move(white_move1)
        play3 = play2.play_move(black_move2)
        play4 = play3.play_move(white_move2)
        play5 = play4.play_move(black_move3)
        play6 = play5.play_move(white_move3)
        capture_play = play6.play_move(black_move4)
        
        # Before the stone is captured 
        self.assertEqual(play1.board.get_player(Point(3, 3)).value, Player.black.value)
        self.assertEqual(play2.board.get_player(Point(4, 3)).value, Player.white.value)
        # After the stone has been captured, the stone point is None
        self.assertIsNone(capture_play.board.get_player(Point(4,3)))
        self.assertIsNone(capture_play.board.get_go_string(Point(4,3)))
        
        
    # Test gameover function when player resigns 
    def test_game_resign(self):
        over_move = Move.resign()
        play_resign = self.game.play_move(over_move)
        
        self.assertTrue(play_resign.game_over())
        
    # Test when game starts 
    def test_game_start(self):
        start_move = Move.play(Point(4,4))
        play_start = self.game.play_move(start_move)
        
        self.assertFalse(play_start.game_over())
        
    # Test when both player passes 
    def test_game_passes(self):
        pass_move1 = Move.pass_turn()
        pass_move2 = Move.pass_turn()
        
        pass_turn1 = self.game.play_move(pass_move1)
        pass_turn2 = pass_turn1.play_move(pass_move2)
        
        self.assertFalse(pass_turn1.game_over())
        self.assertTrue(pass_turn2.game_over())
        
    # Test self_capture function if move is a self-capture  
    def test_self_capture(self):
        # Placing stones with 1 liberty left for black 
        self.game.board.place_stone(Player.black, Point(3,3))
        self.game.board.place_stone(Player.white, Point(2,3))
        self.game.board.place_stone(Player.white, Point(3,2))
        self.game.board.place_stone(Player.white, Point(3,4))
        self.game.board.place_stone(Player.white, Point(4,4))
        self.game.board.place_stone(Player.white, Point(4,2))
        self.game.board.place_stone(Player.white, Point(5,3))
        
        selfcap_move = Move.play(Point(4,3))
        outcome = self.game.self_capture(Player.black, selfcap_move)
        print(outcome)
        
        self.assertTrue(outcome)
        
    def test_self_capture_corner(self):
        # Placing stones around corner with 1 liberty left for black 
        self.game.board.place_stone(Player.black, Point(1,1))
        self.game.board.place_stone(Player.white, Point(2,1))
        self.game.board.place_stone(Player.white, Point(2,2))
        self.game.board.place_stone(Player.white, Point(1,3))
        
        cornercap_move = Move.play(Point(1,2))
        outcome = self.game.self_capture(Player.black, cornercap_move)
        
        self.assertTrue(outcome)
        
    def test_self_capture_false(self):
        # Placing stones with more than 1 liberty left for black 
        self.game.board.place_stone(Player.black, Point(3,3))
        self.game.board.place_stone(Player.white, Point(2,3))
        self.game.board.place_stone(Player.white, Point(3,2))
        self.game.board.place_stone(Player.white, Point(3,4))
        self.game.board.place_stone(Player.white, Point(4,4))
        self.game.board.place_stone(Player.white, Point(4,2))
        
        self_move = Move.play(Point(4,3))
        outcome = self.game.self_capture(Player.black, self_move)
        
        self.assertFalse(outcome)
        
    def test_self_capture_not_play(self):
        resign_move = Move.resign()
        pass_move = Move.pass_turn()
        
        outcome = self.game.self_capture(Player.black, resign_move)
        outcome_pass = self.game.self_capture(Player.black, pass_move)
        
        self.assertFalse(outcome)
        self.assertFalse(outcome_pass)
        
    # Test ko rule at start of the game (no previous moves)
    def test_ko_rule_start(self):
        first_move = Move.play(Point(3,3))
        
        self.assertIsNone(self.game.previous_state)
        self.assertFalse(self.game.ko_rule(Player.black, first_move))
        
    def test_ko_rule(self):
        # Black stones with empty point in the middle 
        black_move1 = Move.play(Point(1,3)) # left 
        black_move2 = Move.play(Point(3,3)) # right
        black_move3 = Move.play(Point(2,4)) # top 
        black_move4 = Move.play(Point(2,2)) # bottom
        
        # White stones with black point in the middle 
        white_move1 = Move.play(Point(4,3)) # right
        white_move2 = Move.play(Point(3,4)) # top
        white_move3 = Move.play(Point(3,2)) # bottom
        
        play1 = self.game.play_move(black_move1)
        play2 = play1.play_move(white_move1)
        play3 = play2.play_move(black_move2)
        play4 = play3.play_move(white_move2)
        play5 = play4.play_move(black_move3)
        play6 = play5.play_move(white_move3)
        play7 = play6.play_move(black_move4)
        
        # White captures black stone
        white_captures = Move.play(Point(2,3)) # middle
        play_white_captures = play7.play_move(white_captures)
        
        # Verify the black stone (3,3) was captured
        self.assertIsNone(play_white_captures.board.get_go_string(Point(3, 3)))
        
        # Captures white and returns to previous state 
        black_captures = Move.play(Point(3,3))
        
        # This move should violate the ko rule 
        self.assertFalse(play_white_captures.ko_rule(Player.black, black_captures))
        
        
    def test_ko_rule_not_play(self):
        resign_move = Move.resign()
        pass_move = Move.pass_turn()
        
        self.assertFalse(self.game.ko_rule(Player.black, resign_move))
        self.assertFalse(self.game.ko_rule(Player.black, pass_move))
        
    # Testing if valid move when game is over 
    def test_valid_move_gameover(self):
        pass_move1 = Move.pass_turn()
        pass_move2 = Move.pass_turn()
        
        # First player passes 
        pass_turn1 = self.game.play_move(pass_move1)
        # Second player passes 
        pass_turn2 = pass_turn1.play_move(pass_move2)
        
        # After first pass, move is still valid 
        self.assertTrue(pass_turn1.valid_move(pass_move2))
        # After both passes, move shouuld not be valid 
        self.assertFalse(pass_turn2.valid_move(pass_move2))
        
    def test_valid_move_true(self):
        move1 = Move.play(Point(3,3))
        move2 = Move.play(Point(4,4))
    
        play1 = self.game.play_move(move1)
        
        # Valid move 
        self.assertTrue(play1.valid_move(move2))
        
    def test_valid_move_selfcapture(self):
        # Placing stones around corner with 1 liberty left for black 
        black_move1 = Move.play(Point(1,1))
        white_move1 = Move.play(Point(2,1))
        black_move2 = Move.play(Point(4,3))
        white_move2 = Move.play(Point(2,2))
        black_move3 = Move.play(Point(4,4))
        white_move3 = Move.play(Point(1,3))
        
        play1 = self.game.play_move(black_move1)
        play2 = play1.play_move(white_move1)
        play3 = play2.play_move(black_move2)
        play4 = play3.play_move(white_move2)
        play5 = play4.play_move(black_move3)
        play6 = play5.play_move(white_move3)
        
        # Valid move before self-capture
        self.assertTrue(play5.valid_move(white_move3))
        
        cornercap_move = Move.play(Point(1,2))
        # False due to self-capture
        self.assertFalse(play6.valid_move(cornercap_move))
        
        
if __name__ == '__main__':
    unittest.main()