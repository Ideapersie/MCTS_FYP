from go.agent.mcts_node import MCTsNode
from go.agent.mcts_agent import MCTsAgent
from go.goboard import Player, GoState, Move, Player
import math
import unittest

class TestMctsAgent(unittest.TestCase):


    # Testing the edge case of 1 rollout for the child node
    def test_ucb_score_one(self):
        parent_rollouts = 100
        child_rollouts = 1
        winrate = 0
        temperature = 1.4
            
        # Formula for UCB score
        expected_score = winrate + temperature * math.sqrt(math.log(parent_rollouts) / child_rollouts)
        actual_score = MCTsAgent.ucb_score(parent_rollouts, child_rollouts, winrate, temperature)
        self.assertEqual(expected_score, actual_score)
            
    # Testing with high rollout count for the child node
    def test_ucb_score_high_rollout(self):
        parent_rollouts = 100
        child_rollouts = 90
        winrate = 0.6 # 60% winrate
        temperature = 1.4
            
        expected_score = winrate + temperature * math.sqrt(math.log(parent_rollouts) / child_rollouts)
        actual_score = MCTsAgent.ucb_score(parent_rollouts, child_rollouts, winrate, temperature)
        self.assertEqual(expected_score, actual_score)