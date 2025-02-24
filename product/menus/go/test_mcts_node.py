from go.agent.mcts_node import MCTsNode
from go.goboard import Player, GoState, Move, Player
import unittest

class TestMctsNode(unittest.TestCase):
    def setUp(self):
        self.game_state = GoState.new_game(9)
        self.new_node = MCTsNode(self.game_state)
        
    # Test if the node can add children when there are legal moves left 
    def test_add_child(self):
        self.assertTrue(self.new_node.add_child())
        
    def test_search_over(self):
        self.assertFalse(self.new_node.search_over())
        
    # Both player's rollout winrate should be 0 at the start
    def test_rollout_winrate(self):
        self.assertEqual(self.new_node.rollout_winrate(Player.black), 0)
        self.assertEqual(self.new_node.rollout_winrate(Player.white), 0)
    
    def test_random_child_unvisited_moves(self):
        self.assertGreater(len(self.new_node.unvisited_moves), 0)
        # 81 possible moves on a 9x9 board
        self.assertEqual(len(self.new_node.unvisited_moves), 81)
        
    # Test if the node can add a child and remove the move from unvisited moves
    def test_random_child_adds_child(self):
        self.new_node.random_child()
        self.assertEqual(len(self.new_node.children), 1)
        # Remove the move from unvisited moves
        self.assertEqual(len(self.new_node.unvisited_moves), 80)
        self.assertNotIn(self.new_node.children[0].move.point, self.new_node.unvisited_moves)
        
if __name__ == "__main__":
    unittest.main()
        