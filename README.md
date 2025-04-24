# Final Year Project

This repository has been created to store your final year project.

You may edit it as you like, but please do not remove the default topics or the project members list. These need to stay as currently defined in order for your supervisor to be able to find your project.

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

- `main.py` - Entry point for the graphical interface
- `cli.py` - Entry point for the command-line interface
- `menus/go/` - Core game implementation
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
- PySide6 or PyQt6 (for graphical interface)
- NumPy (for AI optimizations)