#!/usr/bin/env python3
"""U-8 shared corpus loader. READ-ONLY. Merged archive stack (campaign then survival overlay)."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
CAMP = [("base", ROOT / "database/database.arz"),
        ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
        ("gdx2", ROOT / "gdx2/database/GDX2.arz"),
        ("gdx3", ROOT / "gdx3/database/GDX3.arz")]
SURV = [("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
        ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
        ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
        ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]

_M = None
_OWNERS = None


def load(only_survival=False):
    """Return (M, OWNERS): M maps path -> (owner_key, archive); OWNERS maps path -> [all owners]."""
    global _M, _OWNERS
    if _M is not None:
        return _M, _OWNERS
    M = {}
    OWN = collections.defaultdict(list)
    stack = SURV if only_survival else (CAMP + SURV)
    for k, p in stack:
        a = ArzArchive(p)
        for r in a.records:
            M[r] = (k, a)
            OWN[r].append(k)
    _M, _OWNERS = M, dict(OWN)
    return _M, _OWNERS


def get(path):
    M, _ = load()
    e = M.get(str(path).lower()) or M.get(str(path))
    return e[1].read_record(e[0] if False else (str(path).lower() if str(path).lower() in M else str(path))) if e else None


def rec(path):
    M, _ = load()
    p = str(path)
    e = M.get(p)
    if e is None:
        e = M.get(p.lower())
        p = p.lower()
    if e is None:
        return None
    return e[1].read_record(p)


def grep(pat, flags=re.I):
    M, _ = load()
    r = re.compile(pat, flags)
    return sorted(p for p in M if r.search(p))
