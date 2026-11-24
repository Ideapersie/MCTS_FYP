# Game Playing with Monte Carlo Tree Search

BSc Computer Science (AI) final year project, Royal Holloway, University of London (2025). Supervisor: Magnus Wahlström.

A study of why Monte Carlo Tree Search works, in two parts:

1. **Multi-armed bandits.** Four selection strategies (random, epsilon-greedy, decaying epsilon-greedy and UCB) compared experimentally on 10 to 100 arms over 1,000 iterations. UCB gives the best exploration/exploitation balance: higher reward and more accurate value estimates for the best arms. This is the selection rule MCTS is built on.
2. **Go with an MCTS opponent.** A complete Go implementation (ko and self-capture rules, territory scoring with komi) with a Qt (PySide6) GUI, a CLI, and player-vs-player and player-vs-AI modes. The MCTS agent was optimised with an array-based board and parallel rollouts, cutting computation time by 99.7% to 10,000 simulations in 7.67 seconds, plus adaptive rollout depth and early termination.

**Video demo:** https://youtu.be/Yw8vwLQCCxw

**Documents:** [final report](documents/THARITMOHAMEDHUSSAINKHAN.final.pdf) (79 pages), [user manual](documents/FYP_User_Manual.pdf), [interim report](documents/THARITMOHAMEDHUSSAINKHAN.interim.pdf), [project plan](documents/THARITMOHAMEDHUSSAINKHAN-plan.pdf). Development diary: [`diary.md`](diary.md).

## mctslab: measuring and improving the engine (2026)

`mctslab/` is a test bench built after the project was submitted. `product/` is untouched. The bench re-implements the board with flat numba arrays (about 2,300 random playouts a second on one core for 9x9), re-implements the original agent on it so it can be compared fairly, and adds stronger searches one at a time. Every number below is a row in [`results/ladder.csv`](results/ladder.csv), with the commit that produced it; [`results/RESULTS.md`](results/RESULTS.md) renders the whole ladder.

**What the review of the original agent found.** Each simulation in `mcts_agent.py` starts a fresh node at the root and expands one random child, so the UCB selection code is never reached: the agent is flat Monte Carlo over the root moves, not a tree search. Rollouts are cut short and scored by stones plus captures rather than territory, and the move with the best win rate is played however few visits it had. The TypeScript port on the portfolio had its own bug: it scored every node from the root player's side, so in its tree the opponent tried to help it.

**Results so far (9x9, komi 7, equal playouts per move):**

| Match | Result | 95% interval |
|---|---|---|
| Original agent vs random, 1,000 playouts | 42/50 | 72% to 92% |
| UCT (a real tree, per-side values, most-visited move) vs original | 50/50 | 93% to 100% |
| UCT + RAVE vs plain UCT, 300 playouts | 99/100 | 95% to 100% |
| UCT + RAVE + heavy playouts vs UCT + RAVE, 300 playouts | 30/100 | 22% to 40% |
| UCT + RAVE vs original, 1,000 playouts | 50/50 | 93% to 100% |

Heavy playouts (capture or escape around the last move, MoGo style) made the bot weaker at equal playouts, so they are off by default; the code and the result stay in for the record. An early RAVE run lost because pass was over-explored; the fix and the superseded rows are in the ladder.

**Learning from self-play (7x7, komi 9).** `selfplay.py`, `train.py` and `iterate.py` are a small AlphaZero-style loop sized for a laptop CPU: a policy and value network (4 residual blocks, 32 channels, 84k parameters) guides a PUCT search with no playouts. It is bootstrapped on 500 games of UCT + RAVE playing itself, then improved by self-play, and a new network only replaces the old one if it wins at least 55% of a gate match.

First results, 7x7, one night on a 2-core CPU (about 94,000 self-play and teacher positions):

| Match | Result | 95% interval |
|---|---|---|
| Net + PUCT vs UCT + RAVE, 200 simulations each | 32/60 | 41% to 65% |
| Net + PUCT vs UCT + RAVE, 400 each | 23/60 | 27% to 51% |
| Best net (one promotion) vs the bootstrap net, 128 each | 37/60 | 49% to 73% |

So far the network matches RAVE at 200 simulations without a single playout, falls behind at 400, and self-play has given one modest promotion in three gates. On 7x7 with komi 9 colour decides many games (white won 70 to 100% of games in every match), which is why the ladder also logs the mean score margin; the margins in these rows are inflated because UCT resigns lost games, and a resignation counts as losing by the whole board. More self-play is the obvious next step: `python -m mctslab.iterate --iters 10`.

```bash
pip install numpy numba torch pytest
python -m pytest tests                                  # board rules, parity with product/, agents
python -m mctslab.arena uct:rave=1,k=300 fyp_flat --size 9 --playouts 1000 --games 50
python -m mctslab.selfplay teacher --games 500 --size 7 --komi 9 --playouts 400 --out results/selfplay/teacher1.npz
python -m mctslab.iterate --iters 3                     # bootstrap, then self-play, train, gate
python -m mctslab.report                                # results/RESULTS.md from the ladder
```

The improved search (UCT + RAVE on a flat typed-array board) is ported to TypeScript and plays on [the portfolio](https://github.com/Ideapersie/MainPortfolio).

## Quick start

```bash
cd product
pip install PySide6 numpy matplotlib
python main.py        # GUI: main menu with the Go game and the bandit experiments
python cli.py         # terminal version of Go
```

The bandit experiments live in `product/menus/bandit/` (one `simulate_*.py` per strategy, plotted by `plot_utils.py`).

# Go Game Implementation

This is an implementation of the game of Go with both graphical and command-line interfaces. The game includes support for player vs. player and player vs. AI modes.

## Features

- Complete Go rules implementation including ko-rule and self-capture detection
- Territory scoring with komi
- Monte Carlo Tree Search (MCTS) AI opponent
- Graphical interface with realistic stone rendering
- Command-line interface for terminal play

## Running the Game

### Graphical Interface (Default)

To launch the graphical version of the game:

```bash
python main.py
```

This will open a window with a Go board and game controls.

### Command-Line Interface

To launch the command-line version of the game:

```bash
python cli.py
```

This will start the game in your terminal with text-based representation of the board.

## Game Modes

Both interfaces support:

1. **Player vs. Player**: Two human players take turns placing stones
2. **Player vs. AI**: Play against an MCTS-powered AI opponent

## Project Structure

- `product/main.py` - Entry point for the graphical interface (main menu)
- `product/cli.py` - Entry point for the command-line interface
- `product/menus/bandit/` - Multi-armed bandit strategies and simulations
- `product/menus/go/` - Core game implementation
  - `goboard.py` - Game state and rules
  - `goplayer.py` - Player and point representation
  - `go_moves.py` - Move handling for CLI
  - `go_gui.py` - Graphical interface implementation
  - `fast_go.py` - Optimized implementations for AI
  - `agent/` - AI implementations
    - `mcts_agent.py` - Monte Carlo Tree Search agent
    - `mcts_node.py` - MCTS tree representation
    - `point_eye.py` - Eye detection for Go patterns
    - `random.py` - Random move agent

## Dependencies

- Python 3.6+
- PySide6 (for graphical interface)
- NumPy (for AI optimizations)