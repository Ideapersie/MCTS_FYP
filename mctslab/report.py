"""Render results/ladder.csv as results/RESULTS.md. Superseded rows are listed
separately so the history stays visible.

    python -m mctslab.report
"""

import csv
import os

HERE = os.path.join(os.path.dirname(__file__), "..", "results")


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, "ladder.csv"))))
    live = [r for r in rows if "SUPERSEDED" not in r["note"]]
    old = [r for r in rows if "SUPERSEDED" in r["note"]]

    def table(rs):
        out = ["| Board | Playouts | A | B | A won | 95% CI | A as black / white | A's mean margin | Note |", "|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            out.append(f"| {r['size']}x{r['size']} | {r['playouts']} | `{r['a']}` | `{r['b']}` | {r['a_wins']}/{r['games']} "
                       f"({float(r['a_rate']):.0%}) | {float(r['ci_low']):.0%} to {float(r['ci_high']):.0%} | "
                       f"{float(r['a_black_rate']):.0%} / {float(r['a_white_rate']):.0%} | "
                       f"{(r.get('a_margin') or '-') + (' (' + r['margin_ci'] + ')' if r.get('margin_ci') else '')} | {r['note'].split(' | ')[0]} |")
        return "\n".join(out)

    text = ["# Results", "", "Every match in `ladder.csv`, newest last. Agents are compared at equal playouts per move, "
            "colours alternate, and the interval is a Wilson 95% interval on the win rate.", "", table(live)]
    if old:
        text += ["", "## Superseded", "", "Rows run before a bug fix, kept for the record.", "", table(old)]
    open(os.path.join(HERE, "RESULTS.md"), "w").write("\n".join(text) + "\n")
    print(f"{len(live)} rows, {len(old)} superseded")


if __name__ == "__main__":
    main()
