from go.agent.mcts_node import MCTsNode
from go.agent.mcts_agent import MCTsAgent
from go.goboard import Player, GoState, Move, Point
import math
import unittest

class TestMctsAgent(unittest.TestCase):
    def setUp(self):
        self.game_state = GoState.new_game(9)
        self.new_node = MCTsNode(self.game_state)
        self.agent = MCTsAgent(temperature=1.4, num_rounds=5)
        self.total_rollouts = 100
        
        # Used as a test case for ucb_score method
        self.child0 = MCTsNode(self.game_state, parent=self.new_node, move=Move.play(Point(1,1)))
        
        # Child nodes with different number of rollouts for select_child method
        self.child1 = MCTsNode(self.game_state, parent=self.new_node, move=Move.play(Point(2,2))) 
        self.child2 = MCTsNode(self.game_state, parent=self.new_node, move=Move.play(Point(3,3))) 
        self.child3 = MCTsNode(self.game_state, parent=self.new_node, move=Move.play(Point(4,4))) 
        
        self.child0.num_rollouts = 1
        self.child1.num_rollouts = 10
        self.child2.num_rollouts = 20
        self.child3.num_rollouts = 30
        
        # Simulate winrate for each child node
        self.child0.rollout_winrate = lambda player: 0.0
        self.child1.rollout_winrate = lambda player: 0.2
        self.child2.rollout_winrate = lambda player: 0.4
        self.child3.rollout_winrate = lambda player: 0.8
    
    # Testing the edge case of 1 rollout for the child node
    def test_ucb_score_one(self):
        # Formula for UCB score
        expected_score = self.child0.rollout_winrate(Player.black) + self.agent.temperature * \
                                           math.sqrt (math.log(self.total_rollouts) / self.child0.num_rollouts)
        
        actual_score = MCTsAgent.ucb_score(self.total_rollouts, self.child0.num_rollouts, 
                                           self.child0.rollout_winrate(Player.black), self.agent.temperature)
        
        self.assertEqual(expected_score, actual_score)
            
    # Testing with high rollout count for the child node
    def test_ucb_score_high_rollout(self):
        # Formula for UCB score
        expected_score = self.child3.rollout_winrate(Player.black) + self.agent.temperature * \
                                           math.sqrt (math.log(self.total_rollouts) / self.child3.num_rollouts)
        actual_score = MCTsAgent.ucb_score(self.total_rollouts, self.child3.num_rollouts, 
                                           self.child3.rollout_winrate(Player.black), self.agent.temperature)
        
        self.assertEqual(expected_score, actual_score)
        
    # Test if method returns None when no children
    def test_select_child_no_children(self):
        empty_node = MCTsNode(self.game_state)
        self.assertIsNone(self.agent.select_child(empty_node))
        
    # Testing if the method selects the child with the highest UCB1 score    
    def test_select_child(self):
        
        self.new_node.children = [self.child1, self.child2, self.child3]
        self.new_node.total_rollouts = 0
        for child in self.new_node.children:
            self.new_node.total_rollouts += child.num_rollouts
        
        print(f"Total rollouts: {self.new_node.total_rollouts}")
        selected_child = self.agent.select_child(self.new_node)
        self.assertEqual(selected_child, self.child3)
        
        
if __name__ == "__main__":
    unittest.main()