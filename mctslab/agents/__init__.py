"""Agents. Each has select(board) -> move, where a move is a flat index,
PASS (-1) or RESIGN (-2). Agents are configured by playouts per move, so
comparisons are at equal search effort, not equal time."""

from .random_agent import RandomAgent
from .flat import FlatMC
from .uct import UCT


def _puct(**kw):
    from .puct import PUCT  # imports torch, so only when asked for

    return PUCT(**kw)


REGISTRY = {"random": RandomAgent, "fyp_flat": FlatMC, "uct": UCT, "puct": _puct}


def make(spec: str, playouts: int, seed: int):
    """'uct' or 'uct:rave=1,c=0.7' -> an agent."""
    name, _, opts = spec.partition(":")
    kwargs = {}
    for kv in filter(None, opts.split(",")):
        k, v = kv.split("=")
        for cast in (int, float, str):
            try:
                kwargs[k] = cast(v)
                break
            except ValueError:
                continue
    cls = REGISTRY[name]
    return cls(playouts=playouts, seed=seed, **kwargs)
