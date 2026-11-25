"""Train the policy and value network on self-play data.

Loss = cross-entropy(policy, visit share) + MSE(value, outcome) + L2,
with all eight symmetries of every position.

    python -m mctslab.train results/selfplay/teacher.npz --out weights/best.pt
"""

import argparse
import time

import numpy as np
import torch
import torch.nn.functional as F

from .features import symmetries
from .net import PolicyValueNet


def augment(x, pi, z, n):
    X, P, Z = [], [], []
    for xi, pii, zi in zip(x, pi, z):
        for xs, ps in symmetries(xi, pii, n):
            X.append(xs)
            P.append(ps)
            Z.append(zi)
    return np.stack(X), np.stack(P), np.array(Z, dtype=np.float32)


def train(files, out, n=7, epochs=12, batch=256, lr=2e-3, init=None, blocks=4, ch=32, seed=0):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    data = [np.load(f) for f in files]
    x = np.concatenate([d["x"] for d in data])
    pi = np.concatenate([d["pi"] for d in data])
    z = np.concatenate([d["z"] for d in data])
    X, P, Z = augment(x, pi, z, n)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    split = int(0.92 * len(X))
    tr, va = idx[:split], idx[split:]
    X, P, Z = torch.from_numpy(X), torch.from_numpy(P), torch.from_numpy(Z)
    net = PolicyValueNet(n, blocks, ch)
    if init:
        net.load_state_dict(torch.load(init, weights_only=False)["state"])
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    t = time.time()
    for ep in range(epochs):
        net.train()
        perm = torch.from_numpy(rng.permutation(tr))
        for i in range(0, len(perm), batch):
            b = perm[i : i + batch]
            logits, v = net(X[b])
            loss = -(P[b] * F.log_softmax(logits, 1)).sum(1).mean() + F.mse_loss(v, Z[b])
            opt.zero_grad()
            loss.backward()
            opt.step()
        sched.step()
        net.eval()
        with torch.no_grad():
            vb = torch.from_numpy(va)
            logits, v = net(X[vb])
            pl = -(P[vb] * F.log_softmax(logits, 1)).sum(1).mean().item()
            vl = F.mse_loss(v, Z[vb]).item()
            acc = (logits.argmax(1) == P[vb].argmax(1)).float().mean().item()
        print(f"epoch {ep + 1}: val policy CE {pl:.3f}, value MSE {vl:.3f}, top-1 match {acc:.1%} ({time.time() - t:.0f}s)")
    komis = sorted({float(d["komi"]) for d in data if "komi" in d.files})
    torch.save({"config": {"n": n, "blocks": blocks, "ch": ch}, "state": net.state_dict(), "komi": komis,
                "val": {"policy_ce": pl, "value_mse": vl, "top1": acc}, "positions": len(x)}, out)
    print(f"saved {out}: {len(x)} positions x8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=12)
    ap.add_argument("--init", default=None)
    ap.add_argument("--n", type=int, default=7, help="board size")
    ap.add_argument("--blocks", type=int, default=4)
    ap.add_argument("--ch", type=int, default=32)
    a = ap.parse_args()
    train(a.files, a.out, a.n, a.epochs, init=a.init, blocks=a.blocks, ch=a.ch)
