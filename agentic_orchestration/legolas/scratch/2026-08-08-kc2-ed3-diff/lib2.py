#!/usr/bin/env python3
"""Parameterized overlay-stack resolver — Edition-II vs Edition-III. READ-ONLY."""
import sys, pathlib, functools
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOTS = {
 "II":  pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724"),
 "III": pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808"),
}
REL = [("base",   "database/database.arz"),
       ("gdx1",   "gdx1/database/GDX1.arz"),
       ("gdx2",   "gdx2/database/GDX2.arz"),
       ("gdx3",   "gdx3/database/GDX3.arz"),
       ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
       ("sm1",    "survivalmode1/database/SurvivalMode1.arz"),
       ("sm2",    "survivalmode2/database/SurvivalMode2.arz"),
       ("sm3",    "survivalmode3/database/SurvivalMode3.arz")]

class Ed:
    def __init__(self, tag):
        self.tag = tag
        self.root = ROOTS[tag]
        self._arc = None
        self._idx = None
    @property
    def arcs(self):
        if self._arc is None:
            self._arc = [(k, ArzArchive(self.root / r)) for k, r in REL]
        return self._arc
    @property
    def idx(self):
        if self._idx is None:
            d = {}
            for k, a in self.arcs:
                for r in a.records:
                    d.setdefault(r.lower(), []).append((k, r))
            self._idx = d
        return self._idx
    def owners(self, p):
        return [k for k, _ in self.idx.get(p.lower().replace("\\","/"), [])]
    def read(self, p, which=None):
        p = p.lower().replace("\\","/")
        ent = self.idx.get(p)
        if not ent: return None, None
        key = which or ent[-1][0]
        for k, real in ent:
            if k == key:
                for kk, a in self.arcs:
                    if kk == k:
                        return a.read_record(real), k
        return None, None
    def merged(self, p):
        """Last-wins field merge across every archive carrying the record."""
        p = p.lower().replace("\\","/")
        ent = self.idx.get(p)
        if not ent: return None, []
        out = {}
        for k, real in ent:
            r, _ = self.read(p, which=k)
            if r: out.update(r)
        return out, [k for k, _ in ent]
    def find(self, subs, require_all=True):
        subs = [s.lower() for s in ([subs] if isinstance(subs,str) else subs)]
        return sorted(p for p in self.idx if (all if require_all else any)(s in p for s in subs))

E2 = Ed("II"); E3 = Ed("III")

def norm(v):
    if isinstance(v, list): return tuple(norm(x) for x in v)
    if isinstance(v, float):
        return round(v, 6)
    return v

def diff_rec(path):
    """-> (verdict, details). verdict in IDENTICAL / CHANGED / ONLY-II / ONLY-III / ABSENT"""
    a, oa = E2.merged(path); b, ob = E3.merged(path)
    if a is None and b is None: return "ABSENT", {}
    if a is None: return "ONLY-III", {"owners_III": ob}
    if b is None: return "ONLY-II", {"owners_II": oa}
    fa = {k: norm(v) for k, v in a.items()}
    fb = {k: norm(v) for k, v in b.items()}
    added = sorted(set(fb) - set(fa)); removed = sorted(set(fa) - set(fb))
    ch = {k: (fa[k], fb[k]) for k in sorted(set(fa) & set(fb)) if fa[k] != fb[k]}
    if not added and not removed and not ch:
        v = "IDENTICAL" if oa == ob else "IDENTICAL-FIELDS"
        return v, {"owners_II": oa, "owners_III": ob}
    return "CHANGED", {"added": added, "removed": removed, "changed": ch,
                       "owners_II": oa, "owners_III": ob}
