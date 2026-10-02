"""Counterfactual arm registry (harness-only patches, each restored in `finally`)."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Tuple

_REG: Dict[str, Tuple[str, List[Callable[[], Any]], str]] = {}


def reg(name: str, cfg: str, doc: str, *patches: Callable[[], Any]) -> None:
    _REG[name] = (cfg, list(patches), doc)


def get(name: str):
    cfg, p, _ = _REG[name]
    return cfg, p


def doc(name: str) -> str:
    return _REG[name][2]


@contextmanager
def setattr_patch(obj: Any, name: str, new: Any) -> Iterator[None]:
    old = getattr(obj, name)
    setattr(obj, name, new)
    try:
        yield
    finally:
        setattr(obj, name, old)


reg("CTRL", "V38-FULL", "control: the v3.8 oracle of record, unpatched")

try:
    import arms_extra  # noqa: F401  (counterfactual arms added per lead)
except ImportError:
    pass
