# Results

Every match in `ladder.csv`, newest last. Agents are compared at equal playouts per move, colours alternate, and the interval is a Wilson 95% interval on the win rate.

Margins are black minus white area score from A's side, with a normal 95% interval. From the komi sweep on, a resigned game still counts as a loss for the side that resigned, but it is then played out to the end with resignation off, so the margin is a real score; `Resigned` counts those games. Margins marked * are from before that change and count a resignation as losing by the whole board, so they are inflated.

Komi sweep rows pit RAVE against itself, so only `Black won` matters in them.

| Board | Komi | Playouts | A | B | A won | 95% CI | A as black / white | Black won | A's mean margin | Resigned | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9x9 | 7 | 1000 | `fyp_flat` | `random` | 42/50 (84%) | 72% to 92% | 92% / 76% | - | - | - | baseline: FYP agent vs random |
| 9x9 | 7 | 1000 | `uct` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | - | - | - | fixed tree search vs FYP agent |
| 7x7 | 9 | 800 | `uct` | `random` | 40/40 (100%) | 91% to 100% | 100% / 100% | - | - | - | 7x7 sanity: UCT vs random |
| 9x9 | 7 | 300 | `uct:rave=1,k=300` | `uct` | 99/100 (99%) | 95% to 100% | 98% / 100% | - | - | - | RAVE vs plain UCT, after the pass fix |
| 9x9 | 7 | 300 | `uct:rave=1,k=300,heavy=1` | `uct:rave=1,k=300` | 30/100 (30%) | 22% to 40% | 20% / 40% | - | - | - | heavy playouts on top of RAVE |
| 9x9 | 7 | 1000 | `uct:rave=1,k=300` | `fyp_flat` | 50/50 (100%) | 93% to 100% | 100% / 100% | - | - | - | best search (RAVE) vs FYP agent |
| 7x7 | 9 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 42/80 (52%) | 42% to 63% | 5% / 100% | - | 2.24 (-1.65 to 6.13) * | - | gate: candidate vs gen0 |
| 7x7 | 9 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 49/80 (61%) | 50% to 71% | 22% / 100% | - | 3.3 (-0.42 to 7.02) * | - | gate: candidate vs gen0 |
| 7x7 | 9 | 128 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 42/80 (52%) | 42% to 63% | 5% / 100% | - | 0.74 (-2.70 to 4.17) * | - | gate: candidate vs gen1 |
| 7x7 | 9 | 200 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 32/60 (53%) | 41% to 65% | 23% / 83% | - | 25.35 (18.88 to 31.82) * | - | net-guided PUCT (200 sims) vs RAVE (200 playouts), 7x7 |
| 7x7 | 9 | 400 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 23/60 (38%) | 27% to 51% | 7% / 70% | - | 17.73 (11.43 to 24.03) * | - | net-guided PUCT vs RAVE at 400 |
| 7x7 | 9 | 128 | `puct:weights=weights/best.pt,temp_moves=6` | `puct:weights=weights/gen0.pt,temp_moves=6` | 37/60 (62%) | 49% to 73% | 23% / 100% | - | 2.4 (-1.77 to 6.57) * | - | best net vs the bootstrap net |
| 7x7 | 0.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 30/60 (50%) | 38% to 62% | 67% / 33% | 67% | 1.38 (-1.45 to 4.22) | 53 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 2.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 31/60 (52%) | 39% to 64% | 53% / 50% | 52% | -0.78 (-3.70 to 2.13) | 50 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 4.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 25/60 (42%) | 30% to 54% | 50% / 33% | 58% | -0.88 (-3.52 to 1.76) | 54 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 6.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 26/60 (43%) | 32% to 56% | 37% / 50% | 43% | -0.52 (-3.40 to 2.37) | 57 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 8.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 33/60 (55%) | 42% to 67% | 50% / 60% | 45% | 0.73 (-2.41 to 3.87) | 54 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 5.5 | 300 | `uct:rave=1,k=300` | `uct:rave=1,k=300` | 52/100 (52%) | 42% to 62% | 44% / 60% | 42% | 0.9 (-1.66 to 3.46) | 90 | komi sweep: RAVE vs itself, black win rate |
| 7x7 | 4.5 | 96 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 37/80 (46%) | 36% to 57% | 8% / 85% | 11% | -0.85 (-4.01 to 2.31) | 0 | gate: candidate vs gen1 (weights) |
| 7x7 | 4.5 | 96 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 47/80 (59%) | 48% to 69% | 18% / 100% | 9% | 2.35 (-0.40 to 5.10) | 0 | gate: candidate vs gen1 (weights) |
| 7x7 | 4.5 | 96 | `puct:weights=weights/candidate.pt,temp_moves=6` | `puct:weights=weights/best.pt,temp_moves=6` | 42/80 (52%) | 42% to 63% | 10% / 95% | 8% | -0.49 (-3.61 to 2.64) | 0 | gate: candidate vs gen2 (weights) |
| 7x7 | 4.5 | 200 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 27/60 (45%) | 33% to 57% | 37% / 53% | 42% | 11.97 (7.72 to 16.21) | 27 | net gen2 (komi 4.5) PUCT vs RAVE at 200 |
| 7x7 | 4.5 | 128 | `puct:weights=weights/best.pt,temp_moves=6` | `puct:weights=weights/k9_best.pt,temp_moves=6` | 35/60 (58%) | 46% to 70% | 20% / 97% | 12% | 0.93 (-2.47 to 4.33) | 0 | net gen2 (komi 4.5) vs previous best (komi-9 gen1) |
| 7x7 | 4.5 | 400 | `puct:weights=weights/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 16/60 (27%) | 17% to 39% | 13% / 40% | 37% | 4.83 (1.56 to 8.11) | 16 | net gen2 (komi 4.5) PUCT vs RAVE at 400 |
| 9x9 | 7 | 200 | `puct:weights=weights/9x9/best.pt,temp_moves=6` | `uct:rave=1,k=300` | 7/30 (23%) | 12% to 41% | 7% / 40% | 33% | -5.17 (-8.48 to -1.85) | 7 | 9x9 net (60 teacher games, no self-play) PUCT vs RAVE at 200 |

## Superseded

Rows run before a bug fix, kept for the record.

| Board | Komi | Playouts | A | B | A won | 95% CI | A as black / white | Black won | A's mean margin | Resigned | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9x9 | 7 | 1000 | `uct:rave=1` | `uct` | 30/60 (50%) | 38% to 62% | 20% / 80% | - | - | - | RAVE k=600 vs plain UCT |
| 9x9 | 7 | 300 | `uct:rave=1,k=300` | `uct` | 3/60 (5%) | 2% to 14% | 3% / 7% | - | - | - | RAVE k=300 vs UCT at low playouts |
| 7x7 | 9 | 96 | `puct:weights=weights/candidate.pt` | `puct:weights=weights/best.pt` | 40/80 (50%) | 39% to 61% | 0% / 100% | - | - | - | gate: candidate vs gen0 |
