# Final Year Project

This repository has been created to store your final year project.

You may edit it as you like, but please do not remove the default topics or the project members list. These need to stay as currently defined in order for your supervisor to be able to find your project.

### Main key files in this project 

go-game-mcts/
├── menus/
│   └── go/
│       ├── agent/
│       │   ├── base.py             # Base agent class
│       │   ├── mcts_agent.py       # MCTS AI implementation
│       │   ├── mcts_node.py        # MCTS node representation
│       │   ├── point_eye.py        # Eye detection utilities
│       │   └── random.py           # Random move agent
│       ├── goboard.py              # Go board and game state
│       ├── goplayer.py             # Player and point classes
│       └── go_moves.py             # Move handling
├── fast_go.py                      # Optimized Go implementation
├── go_gui.py                       # GUI implementation (run this for game through GUI)
└── player_vs_mcts.py               # CLI version of player vs AI
└── player_vs_player.py             # CLI version of player vs player