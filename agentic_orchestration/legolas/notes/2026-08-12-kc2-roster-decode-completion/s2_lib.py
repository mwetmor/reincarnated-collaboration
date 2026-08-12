#!/usr/bin/env python3
"""s2-band roster basis for the E-s09-cp150 scene run. READ-ONLY.

Schema lineage: agentic_orchestration/legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/tg_lib.py
Delta: roster() is re-pointed from the t22 band-A 968-record basis to the
169-record E-s09-cp150 baton roster (gap G2 in elrond's 2026-08-12 recon).
"""
import sys, json, pathlib, collections

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

BATON = pathlib.Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
                     "kc2-baton-v1-E-s09-cp150-20260809_052836.json")
POOLS = pathlib.Path("/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv")


class Ed3:
    def __init__(self):
        self._arc = None; self._idx = None; self._cache = {}

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

    def merged(self, p):
        """Last-wins field merge across every archive carrying the record."""
        p = (p or "").lower().replace("\\", "/")
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


E3 = Ed3()


def stratum(rec_path):
    s = rec_path.lower().split("records/creatures/enemies/")[-1]
    return s.rsplit("/", 1)[0] if "/" in s else "trash"


def roster():
    """169 distinct records of the E-s09-cp150 roster, with baton-side facts folded in."""
    b = json.loads(BATON.read_text())
    agg = collections.OrderedDict()
    for a in b["actors"]:
        rp = a["record_path"].lower()
        e = agg.setdefault(rp, dict(record=rp, display_name=a["display_name"],
                                    archetype_tag=a.get("archetype_tag", ""),
                                    stratum=stratum(rp), levels=set(), tiers=set(),
                                    waves=set(), n_actors=0, n_champion=0,
                                    life_mod_pcts=set(), hp_maxes=set()))
        e["levels"].add(a.get("level")); e["tiers"].add(a.get("threat_tier"))
        e["waves"].add(a.get("wave")); e["n_actors"] += 1
        e["n_champion"] += 1 if a.get("is_champion") else 0
        if a.get("life_modifier_pct") is not None:
            e["life_mod_pcts"].add(a["life_modifier_pct"])
        if a.get("hp_max") is not None:
            e["hp_maxes"].add(a["hp_max"])
    out = []
    for rp, e in agg.items():
        lv = sorted(x for x in e["levels"] if x is not None)
        wv = sorted(x for x in e["waves"] if x is not None)
        lm = sorted(x for x in e["life_mod_pcts"] if x is not None)
        out.append(dict(record=rp, display_name=e["display_name"],
                        archetype_tag=e["archetype_tag"], stratum=e["stratum"],
                        level_min=lv[0] if lv else "", level_max=lv[-1] if lv else "",
                        threat_tier="|".join(sorted(str(t) for t in e["tiers"] if t is not None)),
                        wave_first=wv[0] if wv else "", wave_last=wv[-1] if wv else "",
                        n_actors=e["n_actors"], n_champion_actors=e["n_champion"],
                        life_modifier_pct_min=lm[0] if lm else "",
                        life_modifier_pct_max=lm[-1] if lm else ""))
    out.sort(key=lambda r: (r["stratum"], r["record"]))
    return out


def pool_membership():
    """record -> sorted list of pool_record basenames touching it (A1, 100% coverage)."""
    import csv
    m = collections.defaultdict(set)
    kind = {}
    with POOLS.open() as f:
        for row in csv.DictReader(f):
            pool = (row.get("pool_record") or "").rsplit("/", 1)[-1].replace(".dbr", "")
            for col in ("roster_records", "champ_records"):
                for r in (row.get(col) or "").split("|"):
                    r = r.strip().lower()
                    if r:
                        m[r].add(pool)
                        kind.setdefault(r, set()).add(row.get("pool_kind", ""))
    return m, kind
