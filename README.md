# Game Playing with Monte Carlo Tree Search

BSc Computer Science (AI) final year project, Royal Holloway, University of London (2025). Supervisor: Magnus Wahlström.

A study of why Monte Carlo Tree Search works, in two parts:

1. **Multi-armed bandits.** Four selection strategies (random, epsilon-greedy, decaying epsilon-greedy and UCB) compared experimentally on 10 to 100 arms over 1,000 iterations. UCB gives the best exploration/exploitation balance: higher reward and more accurate value estimates for the best arms. This is the selection rule MCTS is built on.
2. **Go with an MCTS opponent.** A complete Go implementation (ko and self-capture rules, territory scoring with komi) with a Qt (PySide6) GUI, a CLI, and player-vs-player and player-vs-AI modes. The MCTS agent was optimised with an array-based board and parallel rollouts, cutting computation time by 99.7% to 10,000 simulations in 7.67 seconds, plus adaptive rollout depth and early termination.

**Video demo:** https://youtu.be/Yw8vwLQCCxw

**Documents:** [final report](documents/THARITMOHAMEDHUSSAINKHAN.final.pdf) (79 pages), [user manual](documents/FYP_User_Manual.pdf), [interim report](documents/THARITMOHAMEDHUSSAINKHAN.interim.pdf), [project plan](documents/THARITMOHAMEDHUSSAINKHAN-plan.pdf). Development diary: [`diary.md`](diary.md).

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