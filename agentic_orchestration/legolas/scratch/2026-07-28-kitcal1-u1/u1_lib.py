#!/usr/bin/env python3
"""SCRATCH (U-1) — multi-archive .arz record reader + rank-array indexer.

Reuses the G-7 `arz_index.Arz` low-level reader (raw struct + lz4), wrapped in a
corpus-wide resolver with expansion-override precedence (gdx3 > gdx2 > gdx1 > base).
Read-only.
"""
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7")
from arz_index import Arz  # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [
    ("gdx3", "gdx3/database/GDX3.arz"),
    ("gdx2", "gdx2/database/GDX2.arz"),
    ("gdx1", "gdx1/database/GDX1.arz"),
    ("base", "database/database.arz"),
]

_cache = None


def archives():
    global _cache
    if _cache is None:
        _cache = []
        for tag, rel in ARZS:
            p = VENDOR / rel
            if p.exists():
                _cache.append((tag, rel, Arz(p)))
    return _cache


def rec(path):
    """Return (srctag, srcrel, recordType, fields) for the first archive holding `path`."""
    for tag, rel, a in archives():
        if path in a.recs:
            rtype, f = a.fields(path)
            return tag, rel, rtype, f
    return None, None, None, None


def grep(pat, limit=200):
    seen = {}
    p = pat.lower()
    for tag, rel, a in archives():
        for n in a.recs:
            if p in n.lower() and n not in seen:
                seen[n] = (tag, a.recs[n][0])
    return sorted(seen.items())[:limit]


def at(f, key, rank, one_indexed=True):
    """Value of field `key` at skill rank `rank`.

    GD rank arrays are 0-indexed: element[0] is rank 1. Scalars return as-is.
    """
    if key not in f:
        return None
    v = f[key]
    if not isinstance(v, list):
        return v
    i = rank - 1 if one_indexed else rank
    if i < 0 or i >= len(v):
        return ("OUT_OF_RANGE", len(v))
    return v[i]


def nonzero(f, rank, skip=()):
    """All fields with a non-zero/non-empty value at `rank`."""
    out = {}
    for k, v in f.items():
        if k in skip:
            continue
        val = at(f, k, rank)
        if val in (0, 0.0, "", None):
            continue
        if isinstance(val, tuple):
            continue
        out[k] = val
    return out


def dump(path, rank=None, only_nonzero=False):
    tag, rel, rtype, f = rec(path)
    if f is None:
        print(f"!! NOT FOUND: {path}")
        return None
    print(f"== {path}\n   src={rel}  recordType={rtype}  fields={len(f)}")
    if rank is None:
        for k in sorted(f):
            print(f"   {k} = {str(f[k])[:240]}")
    else:
        src = nonzero(f, rank) if only_nonzero else {k: at(f, k, rank) for k in f}
        for k in sorted(src):
            arr = isinstance(f[k], list)
            print(f"   {k}{'[' + str(rank) + ']' if arr else ''} = {src[k]}")
    return f


if __name__ == "__main__":
    if sys.argv[1] == "--grep":
        for n, (tag, rt) in grep(sys.argv[2]):
            print(f"{tag:5} {rt:34} {n}")
    else:
        rank = int(sys.argv[2]) if len(sys.argv) > 2 else None
        nz = "--nz" in sys.argv
        dump(sys.argv[1], rank, nz)
