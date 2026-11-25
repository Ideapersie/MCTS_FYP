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

**Learning from self-play (7x7).** `selfplay.py`, `train.py` and `iterate.py` are a small AlphaZero-style loop sized for a laptop CPU: a policy and value network (4 residual blocks, 32 channels, 84k parameters) guides a PUCT search with no playouts. It is bootstrapped on games of UCT + RAVE playing itself, then improved by self-play, and a new network only replaces the old one if it wins at least 55% of a gate match (or its mean margin is above zero with 95% confidence). Gates sample the first 6 moves so they are not replays of two games.

First round, komi 9, one night on a 2-core CPU (about 94,000 self-play and teacher positions):

| Match | Result | 95% interval |
|---|---|---|
| Net + PUCT vs UCT + RAVE, 200 simulations each | 32/60 | 41% to 65% |
| Net + PUCT vs UCT + RAVE, 400 each | 23/60 | 27% to 51% |
| Best net (one promotion) vs the bootstrap net, 128 each | 37/60 | 49% to 73% |

The margins logged in that round are inflated: UCT resigns lost games, and a resignation then counted as losing by the whole board. Since the komi sweep the arena still scores a resignation as a loss, but plays the game out to the end with resignation switched off, so every margin in the ladder from then on is a real area score; `RESULTS.md` marks the old margins with *.

**Komi.** White won 70 to 100% of games in every 7x7 pairing at komi 9, so komi is now a parameter everywhere (`--komi` on arena, selfplay and iterate; agents read it from the board) with one default table, `board.KOMI`. To choose the 7x7 value, UCT + RAVE (300 playouts) played itself at six komi values; only black's win rate matters:

| Komi | Black won | 95% interval |
|---|---|---|
| 0.5 | 40/60 (67%) | 54% to 77% |
| 2.5 | 31/60 (52%) | 39% to 64% |
| 4.5 | 35/60 (58%) | 46% to 70% |
| 5.5 | 42/100 (42%) | 33% to 52% |
| 6.5 | 26/60 (43%) | 32% to 56% |
| 8.5 | 27/60 (45%) | 33% to 58% |

The curve is shallow and noisy: between bots this weak most games are decided by a large capture, not by a few points. The single value nearest 50% is 2.5, but that is one noisy point; a logistic fit over all 400 games puts black at 50% at komi 4.8, so the 7x7 default is now **4.5** (a half point, so there are no draws). Half points are used throughout so no game can end level (the board would give a level game to white).

Two caveats the data forces. First, at komi 8.5 RAVE against itself is close to even, so the white dominance seen at komi 9 was mostly not komi: it came from the networks. Second, the fair komi depends on strength. 7x7 is solved with a komi of 9 under perfect play, and the stronger the players the closer they get to that; the networks, which play more accurately than RAVE at equal search, still let white win most net-vs-net games at komi 4.5 (see the gates below). A komi chosen with RAVE is the fair komi for RAVE, not for the nets.

**Second round, komi 4.5.** The existing net was trained at komi 9 and its value head has learned that white wins. Re-bootstrapping from teacher games would have cost most of the time budget, so the loop continued from the komi-9 best net and trained only on new komi-4.5 self-play (the komi-9 data was dropped, since its outcome labels are wrong at the new komi). Three iterations, 120 self-play games each at 96 simulations (23,149 positions), 5 epochs per candidate, 80-game gates:

| Gate | Result | 95% interval | Mean margin | Black won | Outcome |
|---|---|---|---|---|---|
| candidate vs gen1 | 37/80 | 36% to 57% | -0.8 (-4.0 to 2.3) | 11% | kept |
| candidate vs gen1 | 47/80 | 48% to 69% | +2.4 (-0.4 to 5.1) | 9% | promoted to gen2 |
| candidate vs gen2 | 42/80 | 42% to 63% | -0.5 (-3.6 to 2.6) | 8% | kept |

Black won 29, 27 and then 8 of the 120 self-play games in the three iterations: as the nets improve, white's share goes up, as the caveat above predicts.

Evaluation of gen2 (never used for training or gating):

| Match (komi 4.5) | Result | 95% interval | Net as black / white | Net's mean margin |
|---|---|---|---|---|
| Net gen2 + PUCT vs UCT + RAVE, 200 each | 27/60 | 33% to 57% | 37% / 53% | +12.0 (7.7 to 16.2) |
| Net gen2 + PUCT vs UCT + RAVE, 400 each | 16/60 | 17% to 39% | 13% / 40% | +4.8 (1.6 to 8.1) |
| Net gen2 vs the komi-9 best net (gen1), 128 each | 35/60 | 46% to 70% | 20% / 97% | +0.9 (-2.5 to 4.3) |

So the net is still weaker than RAVE: level at best at 200 simulations and clearly behind at 400, and the second round did not change that (at komi 9 the same comparison was 32/60 and 23/60). The komi-4.5 net is probably a little better than the komi-9 one, but the interval still includes even. Against RAVE the net's mean margin is positive while its win rate is below half. In all three net-vs-RAVE matches (7x7 at 200 and 400, 9x9 below) the number of net wins equals the number of RAVE resignations: RAVE resigns every game it is losing, the net never resigns, so every net win is a resignation and every RAVE win is on the count. Played out with resignation off, RAVE then loses those games by a lot, while its own wins are narrow; that is where the positive margin comes from, so here the win rate is the better measure. The honest summary is that an 84k-parameter net trained for about an hour of CPU self-play replaces random playouts with a learned evaluation and matches RAVE at low search, but does not yet beat it.

**9x9.** The net, features, self-play, training, the loop and PUCT are size-generic (the net takes the board size from its weights file and refuses a board of another size), and `tests/test_net.py` checks a 9x9 forward pass and one full 9x9 self-play game. With the time left, a 9x9 net was bootstrapped from only 60 RAVE teacher games (300 playouts, 4,167 positions, 5 epochs, no self-play, komi 7):

| Match (9x9, komi 7) | Result | 95% interval | Net as black / white | Net's mean margin |
|---|---|---|---|---|
| 9x9 net + PUCT vs UCT + RAVE, 200 each | 7/30 | 12% to 41% | 7% / 40% | -5.2 (-8.5 to -1.9) |

It is clearly weaker than RAVE, as expected from so little data; the policy matches the teacher's first choice on under 5% of held-out positions. The validation split is by position, not by game, so the value loss it prints is optimistic. The commands to continue it are below.

The network has no komi input: komi only enters through the training labels. Mixing data from two komi values would therefore give it contradictory targets, which is why the loop keeps data per size and komi.

```bash
pip install numpy numba torch pytest
python -m pytest tests                                  # board rules, parity with product/, agents
python -m mctslab.arena uct:rave=1,k=300 fyp_flat --size 9 --playouts 1000 --games 50
python -m mctslab.arena uct:rave=1,k=300 uct:rave=1,k=300 --size 7 --komi 4.5 --playouts 300 --games 100  # komi check
python -m mctslab.iterate --iters 3 --games 120 --gate-games 80 --epochs 5 --window 3   # 7x7, komi from board.KOMI
python -m mctslab.iterate --size 9 --wdir weights/9x9 --iters 0 --teacher-games 60 --boot-epochs 5   # 9x9 bootstrap only
python -m mctslab.iterate --size 9 --wdir weights/9x9 --iters 3 --games 60 --gate-games 40 --epochs 5   # 9x9 self-play
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