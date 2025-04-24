import unittest
from unittest.mock import patch
from go.goplayer import Point
from go.player_vs_player import PlayerVsPlayer

class TestPlayerInput(unittest.TestCase):
    def setUp(self):
        # Mock the `run_PvPgame` to avoid running the game loop during tests
        with patch.object(PlayerVsPlayer, 'run_PvPgame', return_value=None):
            self.pvpgame = PlayerVsPlayer(board_size=9)

     # Mocked input should return 'pass'
    @patch('builtins.input', return_value='pass')
    def test_player_input_pass(self, mock_input):
        move = self.pvpgame.player_input()  
        self.assertTrue(move.is_pass)  
        
    # Mocked input should return 'resign'
    @patch('builtins.input', return_value='resign')
    def test_player_input_resign(self, mock_input):
        move = self.pvpgame.player_input()  
        self.assertTrue(move.is_resign) 
        
    # Mocked input should return 'A3', a valid move
    @patch('builtins.input', return_value='A3')
    def test_player_input_valid(self, mock_input):
        move = self.pvpgame.player_input()  
        self.assertTrue(move.point, Point(3,1)) 
        
    # Mocked input should return 'Invalid Move!'
    @patch('builtins.input', return_value='')
    def test_player_input_empty(self, mock_input):
        move = self.pvpgame.player_input()  
        self.assertIsNone(move)
        
     
        
if __name__ == '__main__':
    unittest.main()
