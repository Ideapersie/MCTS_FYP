import unittest

from unittest.mock import patch 
from go.goboard import GoState, Move
from go.goplayer import Point 
from go.player_vs_player import PlayerVsPlayer

class TestPlayerInput(unittest.TestCase):  
    def setUp(self):
        player_input = PlayerVsPlayer.player_input
      
    def test_print_board(self):
        board = GoState.new_game(board_size=9)
        print(board)
        
        self.assertEqual(board.num_rows, 9)
        
    @patch('builtins.input', return_value='')
    def test_player_empty(self, mock_input):
        with self.assertRaises(ValueError):
            PlayerVsPlayer.player_input
        
    @patch('builtins.input', return_value='pass')
    def test_player_input_pass(self, mock_input):
        move = player_input
        self.assertTrue(move.is_pass)
        
    @patch('builtins.input', return_value='resign')
    def test_player_input_resign(self, mock_input):
        move = player_input()
        self.assertTrue(move.is_resign)
        
    @patch('builtins.input', return_value='A3')
    def test_player_input_valid(self, mock_input):
        move = player_input()
        self.assertTrue(move.is_play)
        
        
        
        
        
        