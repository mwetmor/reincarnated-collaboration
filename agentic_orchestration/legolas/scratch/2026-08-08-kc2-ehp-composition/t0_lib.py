#!/usr/bin/env python3
"""Shared overlay-stack resolver for the KC2 eHP-composition probe. READ-ONLY."""
import sys, pathlib, functools

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("base",   ROOT / "database/database.arz"),
         ("gdx1",   ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2",   ROOT / "gdx2/database/GDX2.arz"),
         ("gdx3",   ROOT / "gdx3/database/GDX3.arz"),
         ("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1",    ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2",    ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3",    ROOT / "survivalmode3/database/SurvivalMode3.arz")]


@functools.lru_cache(maxsize=1)
def archives():
    out = []
    for k, p in STACK:
        out.append((k, ArzArchive(p)))
    return out


@functools.lru_cache(maxsize=1)
def index():
    """path(lower) -> list of archive keys carrying it, in overlay order."""
    idx = {}
    for k, a in archives():
        for r in a.records:
            idx.setdefault(r.lower(), []).append(k)
    return idx


def owners(path):
    return index().get(path.lower().replace("\\", "/"), [])


def read(path, which=None):
    """Read a record through the overlay stack (last-wins) or from a named archive."""
    p = path.lower().replace("\\", "/")
    o = owners(p)
    if not o:
        return None, None
    key = which or o[-1]
    for k, a in archives():
        if k == key:
            # ArzArchive keys may be case-sensitive; find the real key
            for r in a.records:
                if r.lower() == p:
                    return a.read_record(r), key
    return None, None


def merged(path):
    """Full last-wins field merge across every archive carrying the record."""
    p = path.lower().replace("\\", "/")
    o = owners(p)
    out, prov = {}, {}
    for k in o:
        rec, _ = read(p, which=k)
        if rec:
            for f, v in rec.items():
                out[f] = v
                prov[f] = k
    return out, prov, o


def find(substrs, require_all=True):
    """Corpus-wide path search."""
    subs = [s.lower() for s in ([substrs] if isinstance(substrs, str) else substrs)]
    hits = []
    for p in index():
        ok = all(s in p for s in subs) if require_all else any(s in p for s in subs)
        if ok:
            hits.append(p)
    return sorted(hits)
