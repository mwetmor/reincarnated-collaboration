#!/usr/bin/env python3
"""THROWAWAY read-only probe — hard-CC generation analysis (C5).

NO production code, NO config change. Imports generation modules and reports what
the emission surfaces actually do at HEAD. Everything here is a read.

Run: python3 2026-07-25-hard-cc-probe.py
"""
from __future__ import annotations
import os, sys, json, logging, contextlib, io

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
sys.path.insert(0, os.path.join(ENGINE, "src"))
logging.disable(logging.CRITICAL)

out = {}

# ---------------------------------------------------------------- P1: registry
from reincarnated.foundation.ailment_loader import (
    load_ailments, get_hard_control_ailments, get_control_ailments,
)
A = load_ailments()
out["P1_registry_hard_control"] = sorted(get_hard_control_ailments(A))
out["P1_registry_control_all"] = sorted(get_control_ailments(A))
out["P1_registry_all"] = sorted(A)

# ------------------------------------------- P2: per_skill_emitter exclude set
import reincarnated.generation.per_skill_emitter as PSE
out["P2_PSE_HARD_CONTROL_AILMENTS"] = sorted(PSE._HARD_CONTROL_AILMENTS)
out["P2_PSE_comment_claims"] = "frozenset({root, knockback, shock})  # per :797 comment"

# P3: what does _make_signature_ailment_effect return for every registry ailment?
res = {}
for name in sorted(A):
    try:
        e = PSE._make_signature_ailment_effect(name, 2)
    except Exception as ex:
        res[name] = f"RAISED {type(ex).__name__}: {ex}"
        continue
    res[name] = None if e is None else {"name": e.name, "params": dict(e.params)}
out["P3_make_signature_ailment_effect_tier2"] = res

# ------------------------------------------------ P4: element -> what emits
from reincarnated.generation.element_biases import (
    ELEMENT_AILMENT, SECONDARY_AILMENT_MAP, AILMENT_IS_CONTROL,
)
emit = {}
for el, ail in ELEMENT_AILMENT.items():
    e = PSE._make_signature_ailment_effect(ail, 2)
    emit[el] = {
        "signature_ailment": ail,
        "is_control": A[ail].is_control,
        "PSE_emits": None if e is None else e.name,
        "secondary_map": SECONDARY_AILMENT_MAP.get(el, []),
    }
out["P4_element_emission"] = emit

# ------------------------------- P5: ability_grammar reachability for hard CC
from reincarnated.generation import ability_grammar as AG
from reincarnated.generation.role_constraints import ROLE_CONSTRAINTS
import numpy as np
rng = np.random.default_rng(4242)
ag_emit = {}
for el in sorted(ELEMENT_AILMENT):
    for role in ("control", "utility", "damage_over_time", "primary_attack"):
        names = set()
        for _ in range(300):
            effs = AG._sample_effects(role, el, 40.0, 40.0, ROLE_CONSTRAINTS[role], rng)
            names |= {e.name for e in effs}
        ag_emit[f"{el}/{role}"] = sorted(names)
out["P5_ability_grammar_effect_names"] = ag_emit

# ------------------------------ P6: is SECONDARY_AILMENT_MAP read by anything?
import subprocess
r = subprocess.run(
    ["grep", "-rn", "SECONDARY_AILMENT_MAP", os.path.join(ENGINE, "src")],
    capture_output=True, text=True,
)
out["P6_secondary_map_readers_in_src"] = [
    ln.replace(ENGINE + "/", "") for ln in r.stdout.strip().splitlines()
]

# --------------------------- P7: typed monster skills — any ailment effect?
from reincarnated.generation.typed_monster_skills import emit_skills_for_threat_tier
tms = {}
for tier in ("boss", "elite", "swarm"):
    try:
        sk = emit_skills_for_threat_tier(tier, "fire")
    except TypeError:
        try:
            sk = emit_skills_for_threat_tier(tier)
        except Exception as ex:
            tms[tier] = f"RAISED {type(ex).__name__}: {ex}"
            continue
    except Exception as ex:
        tms[tier] = f"RAISED {type(ex).__name__}: {ex}"
        continue
    ns = set()
    for s in sk:
        for e in (s.get("effects") or []):
            ns.add(e.get("name"))
    tms[tier] = sorted(ns)
out["P7_typed_monster_skill_effect_names"] = tms

print(json.dumps(out, indent=2, default=str))
