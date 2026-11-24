"""A small policy and value network, AlphaZero style, sized for a CPU."""

import torch
import torch.nn as nn
import torch.nn.functional as F

from .features import PLANES


class Res(nn.Module):
    def __init__(self, ch):
        super().__init__()
        self.c1 = nn.Conv2d(ch, ch, 3, padding=1, bias=False)
        self.b1 = nn.BatchNorm2d(ch)
        self.c2 = nn.Conv2d(ch, ch, 3, padding=1, bias=False)
        self.b2 = nn.BatchNorm2d(ch)

    def forward(self, x):
        y = F.relu(self.b1(self.c1(x)))
        return F.relu(x + self.b2(self.c2(y)))


class PolicyValueNet(nn.Module):
    def __init__(self, n=7, blocks=4, ch=32):
        super().__init__()
        self.n = n
        self.stem = nn.Sequential(nn.Conv2d(PLANES, ch, 3, padding=1, bias=False), nn.BatchNorm2d(ch), nn.ReLU())
        self.body = nn.Sequential(*[Res(ch) for _ in range(blocks)])
        self.p_conv = nn.Sequential(nn.Conv2d(ch, 2, 1, bias=False), nn.BatchNorm2d(2), nn.ReLU())
        self.p_fc = nn.Linear(2 * n * n, n * n + 1)
        self.v_conv = nn.Sequential(nn.Conv2d(ch, 1, 1, bias=False), nn.BatchNorm2d(1), nn.ReLU())
        self.v_fc = nn.Sequential(nn.Linear(n * n, 64), nn.ReLU(), nn.Linear(64, 1), nn.Tanh())

    def forward(self, x):
        h = self.body(self.stem(x))
        logits = self.p_fc(self.p_conv(h).flatten(1))
        v = self.v_fc(self.v_conv(h).flatten(1)).squeeze(1)
        return logits, v

    def params(self):
        return sum(p.numel() for p in self.parameters())
