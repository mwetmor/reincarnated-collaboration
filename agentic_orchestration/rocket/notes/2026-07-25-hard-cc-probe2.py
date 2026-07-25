#!/usr/bin/env python3
"""THROWAWAY read-only probe 2 — what effect NAMES does the census population actually carry?

Re-materializes the SAME population the F8 A/B censused (build_population, seed 14001) and
dumps the full effect-name histogram + per-role breakdown. No config change, no write.
"""
from __future__ import annotations
import os, sys, json, logging, collections, contextlib, io

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
sys.path.insert(0, os.path.join(ENGINE, "src"))
logging.disable(logging.CRITICAL)

with contextlib.redirect_stdout(io.StringIO()):
    from reincarnated.simulation.clean_boss_numbers_harness_2026_06_19 import build_population
    pop, n_kits = build_population()

eff_names = collections.Counter()
role_x_eff = collections.Counter()
elem_x_eff = collections.Counter()
per_cfg_cc = collections.Counter()
CC = frozenset({"stun", "freeze", "root", "chill", "silence", "knockback", "shock"})

for p in pop:
    pc = p["player_class"]
    n_cc = 0
    for s in getattr(pc, "skills", []):
        role = getattr(s, "role", "?")
        el = getattr(s, "canonical_element", "?")
        for e in (getattr(s, "effects", []) or []):
            nm = getattr(e, "name", None)
            eff_names[nm] += 1
            role_x_eff[(role, nm)] += 1
            elem_x_eff[(el, nm)] += 1
            if nm in CC:
                n_cc += 1
    per_cfg_cc[n_cc] += 1

print(json.dumps({
    "n_configs": len(pop),
    "n_kits": n_kits,
    "effect_name_histogram": dict(eff_names.most_common()),
    "role_x_effect": {f"{r}|{n}": c for (r, n), c in sorted(role_x_eff.items())},
    "element_x_effect": {f"{e}|{n}": c for (e, n), c in sorted(elem_x_eff.items())},
    "cc_effects_per_config": dict(per_cfg_cc),
}, indent=2))
