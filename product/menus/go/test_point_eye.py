import unittest

from go.goplayer import Point, Player
from go.goboard import Move, GoString, Board, GoState
from go.agent.point_eye import is_point_eye

class TestPointEye(unittest.TestCase):
    def setUp(self):
        self.board = Board(num_rows=9,num_cols=9)
        self.game = GoState.new_game(9)
        
    def test_is_point_eye_middle_false(self):
        # Black stones with empty point in the middle 
        black_move1 = Move.play(Point(1,3)) # left 
        black_move2 = Move.play(Point(3,3)) # right
        black_move3 = Move.play(Point(2,4)) # top 
        black_move4 = Move.play(Point(2,2)) # bottom
        
        # White stones to simulate game 
        white_move1 = Move.play(Point(7,7)) 
        white_move2 = Move.play(Point(8,8)) 
        white_move3 = Move.play(Point(9,9)) 
        
        play1 = self.game.play_move(black_move1)
        play2 = play1.play_move(white_move1)
        play3 = play2.play_move(black_move2)
        play4 = play3.play_move(white_move2)
        play5 = play4.play_move(black_move3)
        play6 = play5.play_move(white_move3)
        play7 = play6.play_move(black_move4)
        
        point_is_eye = is_point_eye(play7.board, Point(2,3), Player.black)
        
        # Test if eye is emtpy and surrounding corners are same colour
        self.assertIsNone(play7.board.get_player(Point(2,3)))
        self.assertFalse(point_is_eye)
        
    def test_is_point_eye_middle_true(self):
        # Black stones with empty point in the middle 
        black_move1 = Move.play(Point(1,3)) # left 
        black_move2 = Move.play(Point(3,3)) # right
        black_move3 = Move.play(Point(2,4)) # top 
        black_move4 = Move.play(Point(2,2)) # bottom
        black_move5 = Move.play(Point(1,2)) # bottom left corner
        black_move6 = Move.play(Point(1,4)) # top left corner
        black_move7 = Move.play(Point(3,2)) # bottom right corner
        black_move8 = Move.play(Point(3,4))
        
        
        # White stones to simulate game 
        white_move1 = Move.play(Point(7,7)) 
        white_move2 = Move.play(Point(8,8)) 
        white_move3 = Move.play(Point(9,9))
        white_move4 = Move.play(Point(7,8))
        white_move5 = Move.play(Point(9,7))
        white_move6 = Move.play(Point(8,7))
        white_move7 = Move.play(Point(8,9))
        
        play1 = self.game.play_move(black_move1)
        play2 = play1.play_move(white_move1)
        play3 = play2.play_move(black_move2)
        play4 = play3.play_move(white_move2)
        play5 = play4.play_move(black_move3)
        play6 = play5.play_move(white_move3)
        play7 = play6.play_move(black_move4)
        play8 = play7.play_move(white_move4)
        play9 = play8.play_move(black_move5)
        play10 = play9.play_move(white_move5)
        play11 = play10.play_move(black_move6)
        play12 = play11.play_move(white_move6)
        play13 = play12.play_move(black_move7)
        play14 = play13.play_move(white_move7)
        play15 = play14.play_move(black_move8)
        
        point_is_eye = is_point_eye(play15.board, Point(2,3), Player.black)
        
        # Test if eye is emtpy and surrounding corners are same colour
        self.assertIsNone(play15.board.get_player(Point(2,3)))
        self.assertTrue(point_is_eye)
        
if __name__ == '__main__':
    unittest.main()