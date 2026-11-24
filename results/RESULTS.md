# Results

Every match in `ladder.csv`, newest last. Agents are compared at equal playouts per move, colours alternate, and the interval is a Wilson 95% interval on the win rate.

| Board | Playouts | A | B | A won | 95% CI | A as black / white | Note |
|---|---|---|---|---|---|---|---|
| 9x9 | 1000 | `fyp_flat` | `random` | 42/50 (84%) | 72% to 92% | 92% / 76% | baseline: FYP agent vs random |
| 9x9 | 1000 | `uct` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | fixed tree search vs FYP agent |
| 7x7 | 800 | `uct` | `random` | 40/40 (100%) | 91% to 100% | 100% / 100% | 7x7 sanity: UCT vs random |
| 9x9 | 300 | `uct:rave=1,k=300` | `uct` | 99/100 (99%) | 95% to 100% | 98% / 100% | RAVE vs plain UCT, after the pass fix |
| 9x9 | 300 | `uct:rave=1,k=300,heavy=1` | `uct:rave=1,k=300` | 30/100 (30%) | 22% to 40% | 20% / 40% | heavy playouts on top of RAVE |
| 9x9 | 1000 | `uct:rave=1,k=300` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | best search (RAVE) vs FYP agent |
| 7x7 | 96 | `puct:weights=weights/candidate.pt` | `puct:weights=weights/best.pt` | 40/80 (50%) | 39% to 61% | 0% / 100% | gate: candidate vs gen0 |

## Superseded

Rows run before a bug fix, kept for the record.

| Board | Playouts | A | B | A won | 95% CI | A as black / white | Note |
|---|---|---|---|---|---|---|---|
| 9x9 | 1000 | `uct:rave=1` | `uct` | 30/60 (50%) | 38% to 62% | 20% / 80% | RAVE k=600 vs plain UCT |
| 9x9 | 300 | `uct:rave=1,k=300` | `uct` | 3/60 (5%) | 2% to 14% | 3% / 7% | RAVE k=300 vs UCT at low playouts |
