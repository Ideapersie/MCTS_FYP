# Results

Every match in `ladder.csv`, newest last. Agents are compared at equal playouts per move, colours alternate, and the interval is a Wilson 95% interval on the win rate.

| Board | Playouts | A | B | A won | 95% CI | A as black / white | A's mean margin | Note |
|---|---|---|---|---|---|---|---|---|
| 9x9 | 1000 | `fyp_flat` | `random` | 42/50 (84%) | 72% to 92% | 92% / 76% | - | baseline: FYP agent vs random |
| 9x9 | 1000 | `uct` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | - | fixed tree search vs FYP agent |
| 7x7 | 800 | `uct` | `random` | 40/40 (100%) | 91% to 100% | 100% / 100% | - | 7x7 sanity: UCT vs random |
| 9x9 | 300 | `uct:rave=1,k=300` | `uct` | 99/100 (99%) | 95% to 100% | 98% / 100% | - | RAVE vs plain UCT, after the pass fix |
| 9x9 | 300 | `uct:rave=1,k=300,heavy=1` | `uct:rave=1,k=300` | 30/100 (30%) | 22% to 40% | 20% / 40% | - | heavy playouts on top of RAVE |
| 9x9 | 1000 | `uct:rave=1,k=300` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | - | best search (RAVE) vs FYP agent |
| 7x7 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 42/80 (52%) | 42% to 63% | 5% / 100% | 2.24 (-1.65 to 6.13) | gate: candidate vs gen0 |
| 7x7 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 49/80 (61%) | 50% to 71% | 22% / 100% | 3.3 (-0.42 to 7.02) | gate: candidate vs gen0 |
| 7x7 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 42/80 (52%) | 42% to 63% | 5% / 100% | 0.74 (-2.70 to 4.17) | gate: candidate vs gen1 |
| 7x7 | 200 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 32/60 (53%) | 41% to 65% | 23% / 83% | 25.35 (18.88 to 31.82) | net-guided PUCT (200 sims) vs RAVE (200 playouts), 7x7 |
| 7x7 | 400 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 23/60 (38%) | 27% to 51% | 7% / 70% | 17.73 (11.43 to 24.03) | net-guided PUCT vs RAVE at 400 |
| 7x7 | 128 | `puct:weights=weights/best.pt,temp_moves=6` | `puct:weights=weights/gen0.pt,temp_moves=6` | 37/60 (62%) | 49% to 73% | 23% / 100% | 2.4 (-1.77 to 6.57) | best net vs the bootstrap net |

## Superseded

Rows run before a bug fix, kept for the record.

| Board | Playouts | A | B | A won | 95% CI | A as black / white | A's mean margin | Note |
|---|---|---|---|---|---|---|---|---|
| 9x9 | 1000 | `uct:rave=1` | `uct` | 30/60 (50%) | 38% to 62% | 20% / 80% | - | RAVE k=600 vs plain UCT |
| 9x9 | 300 | `uct:rave=1,k=300` | `uct` | 3/60 (5%) | 2% to 14% | 3% / 7% | - | RAVE k=300 vs UCT at low playouts |
| 7x7 | 96 | `puct:weights=weights/candidate.pt` | `puct:weights=weights/best.pt` | 40/80 (50%) | 39% to 61% | 0% / 100% | - | gate: candidate vs gen0 |
