#!/usr/bin/env python3
"""Edition-III overlay-stack reader, pinned to III only. READ-ONLY."""
import sys, pathlib, csv, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
REL = [("base",   "database/database.arz"),
       ("gdx1",   "gdx1/database/GDX1.arz"),
       ("gdx2",   "gdx2/database/GDX2.arz"),
       ("gdx3",   "gdx3/database/GDX3.arz"),
       ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
       ("sm1",    "survivalmode1/database/SurvivalMode1.arz"),
       ("sm2",    "survivalmode2/database/SurvivalMode2.arz"),
       ("sm3",    "survivalmode3/database/SurvivalMode3.arz")]

T22 = pathlib.Path("/Users/admin/Games/reincarnated-engine/data/kc2/t22_band_a_monster_stats.csv")


class Ed3:
    def __init__(self):
        self._arc = None
        self._idx = None
        self._cache = {}

    @property
    def arcs(self):
        if self._arc is None:
            self._arc = [(k, ArzArchive(ROOT / r)) for k, r in REL]
        return self._arc

    @property
    def idx(self):
        if self._idx is None:
            d = {}
            for k, a in self.arcs:
                for r in a.records:
                    d.setdefault(r.lower().replace("\\", "/"), []).append((k, r))
            self._idx = d
        return self._idx

    def rtype(self, p):
        p = p.lower().replace("\\", "/")
        ent = self.idx.get(p)
        if not ent:
            return None
        k, real = ent[-1]
        for kk, a in self.arcs:
            if kk == k:
                return a.record_type(real)
        return None

    def merged(self, p):
        """Last-wins field merge across every archive carrying the record."""
        p = p.lower().replace("\\", "/")
        if p in self._cache:
            return self._cache[p]
        ent = self.idx.get(p)
        if not ent:
            self._cache[p] = (None, [])
            return None, []
        out = {}
        for k, real in ent:
            for kk, a in self.arcs:
                if kk == k:
                    try:
                        out.update(a.read_record(real))
                    except Exception:
                        pass
        res = (out, [k for k, _ in ent])
        self._cache[p] = res
        return res

    def exists(self, p):
        return (p or "").lower().replace("\\", "/") in self.idx

    def find(self, subs, require_all=True):
        subs = [s.lower() for s in ([subs] if isinstance(subs, str) else subs)]
        return sorted(p for p in self.idx if (all if require_all else any)(s in p for s in subs))


E3 = Ed3()


def roster():
    """968 record paths in t22 order, with the t22 row dict."""
    with open(T22) as f:
        return list(csv.DictReader(f))
