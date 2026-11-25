import numpy as np
import torch

from mctslab.board import Board, default_komi
from mctslab.features import PLANES, encode
from mctslab.net import PolicyValueNet
from mctslab.selfplay import game


def test_9x9_forward_pass():
    net = PolicyValueNet(n=9).eval()
    x = torch.from_numpy(encode(Board(9)))[None]
    assert x.shape == (1, PLANES, 9, 9)
    with torch.no_grad():
        logits, v = net(x)
    assert logits.shape == (1, 82) and v.shape == (1,)


def test_9x9_selfplay_game(tmp_path):
    torch.manual_seed(0)
    net = PolicyValueNet(n=9)
    path = str(tmp_path / "net9.pt")
    torch.save({"config": {"n": 9, "blocks": 4, "ch": 32}, "state": net.state_dict()}, path)
    x, pi, z = game(("net", 9, default_komi(9), 4, 0, path))
    assert x.shape[1:] == (PLANES, 9, 9) and pi.shape[1] == 82
    assert len(x) == len(pi) == len(z) and np.allclose(pi.sum(1), 1, atol=1e-5)
    assert set(np.unique(z)) <= {-1.0, 1.0}
