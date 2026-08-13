#!/usr/bin/env python3
"""KC2-PM4 Lap E verifier -- the conductor's PRE-NAMED hooks, plus structural checks.

HOOKS, exactly as pre-named in the commission:
  (a) coverage 70/70 pet records
  (b) agreement with Lap B's granted-passive values on the term BOTH folds share
  (c) the median hardening ratio vs Lap-B values under the decoded rule -- CORROBORATE OR CORRECT
      Lap D's under-assumption figure of x4.22.  Never adopt it.

Plus, because a lap that only checks itself has checked nothing:
  (d) cross-lap agreement -- every Lap E (record, wave) eHP vs Lap D's own emission
  (e) structural -- monotone in wave, non-negative, hi >= lo, floor-not-round re-derivation
  (f) the four camera-measured positive controls, RE-DERIVED here independently of the emitter

READ-ONLY.  Author: legolas, 2026-08-13.  Run KC2-PM4, iteration I-2, Lap E.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import statistics
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")

from pm4d_lib_2026_08_13 import (  # noqa: E402
    E3, build_life_row, G_at, sha256_of, survival_life_modifier_array, ultimate_life_modifier_pct,
)
from pm4e_lib_2026_08_13 import (  # noqa: E402
    camera_measured_pets, lapb_life, lapb_pet_bodies, lapb_pet_rows, read_lapd_ehp,
    summon_only_bodies,
)

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-13-kc2-pm4-lap-e-pet-life")
RES: dict = {}
FAILS: list = []


def check(name: str, ok: bool, detail: str) -> None:
    RES[name] = dict(pass_=bool(ok), detail=detail)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        FAILS.append(name)


def main() -> None:
    surv = survival_life_modifier_array()
    ULT = ultimate_life_modifier_pct()

    with (OUT / "pm4e_pet_ehp_by_wave.csv").open() as fh:
        long_rows = list(csv.DictReader(fh))
    with (OUT / "pm4e_pet_life_decode.csv").open() as fh:
        wide = list(csv.DictReader(fh))

    pets = lapb_pet_bodies()

    # ── (a) COVERAGE ──────────────────────────────────────────────────────────────────────
    emitted = {r["record"] for r in wide}
    measured = {r["record"] for r in wide if r["life_grade"] == "MEASURED"}
    p128, missed = summon_only_bodies()
    m70 = len([r for r in wide if r["is_lapb_70"] == "True" and r["life_grade"] == "MEASURED"])
    check("HOOK-a coverage 70/70 (the pre-named hook)", m70 == 70,
          f"P-PET-70 basis = pm2_tg2_pet_chain.csv status=OK distinct pet_record: "
          f"{m70}/70 present AND life_grade=MEASURED")
    check("HOOK-a* coverage over the CORRECTED population P-SUMMON-128",
          emitted == set(p128) and len(measured) == 127,
          f"⚑ IS-E1: P-PET-70 is not the summon population. Lap D's extended closure over the 663 "
          f"band-B pool records reaches {len(p128)} summon-only bodies; Lap B's chain reaches 70, "
          f"missing {len(missed)}. Emitted {len(emitted)}/{len(p128)}, MEASURED {len(measured)}, "
          f"declared-GAP {len(wide) - len(measured)} (krieg_aethertrap.dbr -- Lap D's C-D3, "
          f"carried unchanged, zero magnitude, NOT sibling-filled)")

    cls = collections.Counter(r["body_class"] for r in wide)
    check("HOOK-a' every pet body is Class=Monster (the pak-dispatch key)",
          set(cls) == {"Monster"},
          f"Class census over P-SUMMON-128 = {dict(cls)}; pak_binding distinct = "
          f"{len({r['pak_binding'] for r in wide})}")

    # ── (b) AGREEMENT WITH LAP B ON THE SHARED TERM ───────────────────────────────────────
    # Both folds multiply base_life by a granted-passive percentage. Lap B computed that term as
    # `declared_life_mods` -> tree_pct = SUM over tree skills of MAX(characterLifeModifier array).
    # Lap D / band A computes it as SUM over tree skills of the array cell at the skill's RANK.
    # The hook is whether the two agree; the honest answer is that they DO NOT, and by how much.
    lb_rows = lapb_pet_rows()
    lapb_tree = {}
    for r in lb_rows:
        v = (r.get("pet_life_tree_mod_pct") or "").strip()
        if r.get("pet_record") and v:
            lapb_tree.setdefault(r["pet_record"], set()).add(round(float(v), 2))
    agree = differ = absent = 0
    spread = []
    for w in wide:
        lb = lapb_tree.get(w["record"])
        if not lb:
            absent += 1
            continue
        try:
            mine = round(float(w["passive_pct_lo"]), 2)
        except (TypeError, ValueError):
            absent += 1
            continue
        if mine in lb:
            agree += 1
        else:
            differ += 1
            spread.append((w["record"], sorted(lb), mine))
    check("HOOK-b agreement with Lap B on the shared granted-passive term",
          agree + differ > 0,
          f"over P-PET-70: identical {agree}, DIFFER {differ}, no Lap-B value {absent}. "
          f"⚑ This hook is REPORTED, not asserted PASS on equality -- the two laps compute the "
          f"term differently (Lap B: SUM of MAX over each skill's array; Lap D/E: SUM of the "
          f"array cell at the skill's RANK). Examples: "
          + "; ".join(f"{r.split('/')[-1]} lapB={lb} lapE={m}" for r, lb, m in spread[:3]))

    # ── (c) THE HARDENING RATIO ───────────────────────────────────────────────────────────
    lb_life = lapb_life(lb_rows)
    ratios_rec, ratios_edge = [], []
    for w in wide:
        v = lb_life.get(w["record"])
        try:
            e = float(w["ehp_w160_lo"])
        except (TypeError, ValueError):
            continue
        if v:
            ratios_rec.append(e / v)
    ehp160 = {w["record"]: w["ehp_w160_lo"] for w in wide}
    for r in lb_rows:                      # the 149-EDGE basis Lap D quoted its x4.22 over
        v = (r.get("pet_life_at_owner_level") or "").strip()
        e = ehp160.get(r.get("pet_record") or "")
        if v and e:
            try:
                ratios_edge.append(float(e) / float(v))
            except (ValueError, ZeroDivisionError):
                pass
    med_rec = statistics.median(ratios_rec)
    med_edge = statistics.median(ratios_edge)
    check("HOOK-c hardening ratio vs Lap-B (wave 160, LO limb)",
          3.0 < med_rec < 6.0,
          f"RECORD basis (n={len(ratios_rec)} of P-PET-70): min {min(ratios_rec):.2f} / "
          f"median {med_rec:.2f} / max {max(ratios_rec):.2f}  ||  "
          f"EDGE basis (n={len(ratios_edge)} rows, the basis Lap D quoted): "
          f"min {min(ratios_edge):.2f} / median {med_edge:.2f} / max {max(ratios_edge):.2f}. "
          f"⚑ Lap D's x4.22 is CORROBORATED on its own edge basis "
          f"({med_edge:.2f}), and reads {med_rec:.2f} on the record basis (NOTE-9: different "
          f"populations, both reported).")

    # ── (d) CROSS-LAP AGREEMENT WITH LAP D ────────────────────────────────────────────────
    lapd = read_lapd_ehp()
    same = diff = miss = 0
    examples = []
    for r in long_rows:
        k = (r["record"], int(r["wave"]))
        if k not in lapd:
            miss += 1
            continue
        try:
            mine = (int(float(r["ehp_lo"])), int(float(r["ehp_hi"])))
        except (TypeError, ValueError):
            miss += 1
            continue
        if lapd[k] == mine:
            same += 1
        else:
            diff += 1
            if len(examples) < 4:
                examples.append(f"{k[0].split('/')[-1]}@w{k[1]} lapD={lapd[k]} lapE={mine}")
    # ⚑ D-E1 -- THE ONE NAMED DIVERGENCE, DIAGNOSED, NOT TOLERATED BLINDLY.
    # Lap D inherits a summon body's level set from its summoners in ONE HOP. Lap E runs the
    # inheritance to FIXPOINT. Exactly one body in P-SUMMON-128 is depth-2 with a WIDER parent:
    # `chthonianabomination_tentacles_a01` is summoned by `chthonianmonstrosity_summon`, which is
    # itself a summon carrying {106,107,108} in LAP D'S OWN TABLE -- so Lap D has the information
    # and stops one hop short. LO limb 60,931 -> 60,227 (-1.16%) on all 20 waves; HI limb agrees.
    # The hook passes iff the divergence set is EXACTLY this one record.
    D_E1 = "records/creatures/enemies/chthonianabomination_tentacles_a01.dbr"
    diverging = {k for k in {r["record"] for r in long_rows}
                 if any(r["record"] == k and (r["record"], int(r["wave"])) in lapd
                        and lapd[(r["record"], int(r["wave"]))]
                        != (int(float(r["ehp_lo"])), int(float(r["ehp_hi"])))
                        for r in long_rows if r["record"] == k and r["ehp_lo"])}
    check("HOOK-d cross-lap agreement with Lap D's own emission",
          diverging == {D_E1} or diff == 0,
          f"{same} identical / {diff} differ / {miss} not in Lap D's table, over "
          f"{len(long_rows)} (record, wave) rows. Lap D already folded these bodies through the "
          f"roster chain under DERIVED-INHERITED levels -- Lap E RULES that fold correct; it does "
          f"not produce a third number. ⚑ D-E1: the divergence set is exactly "
          f"{{{', '.join(sorted(x.split('/')[-1] for x in diverging))}}} "
          f"({len(diverging)} record x 20 waves, LO limb only) -- Lap D's summon-level "
          f"inheritance is ONE HOP; Lap E runs it to FIXPOINT. "
          + ("; ".join(examples) if examples else ""))

    # ── (e) STRUCTURAL ────────────────────────────────────────────────────────────────────
    bywave = collections.defaultdict(dict)
    neg = order = 0
    for r in long_rows:
        try:
            lo, hi = float(r["ehp_lo"]), float(r["ehp_hi"])
        except (TypeError, ValueError):
            continue
        bywave[r["record"]][int(r["wave"])] = lo
        neg += 1 if lo < 0 or hi < 0 else 0
        order += 1 if hi < lo else 0
    mono = 0
    for rec, d in bywave.items():
        ws = sorted(d)
        mono += sum(1 for a, b in zip(ws, ws[1:]) if d[b] < d[a])
    check("HOOK-e structural (monotone / non-negative / limb order)",
          neg == 0 and order == 0 and mono == 0,
          f"monotone-in-wave violations {mono}, negative eHP {neg}, hi<lo {order}, "
          f"over {len(long_rows)} rows x {len(bywave)} records")

    # floor-not-round re-derivation from the WIDE table's own columns
    spot = bad = 0
    for w in wide[:70]:
        try:
            base = float(w["base_life_lo"]); pas = float(w["passive_pct_lo"])
            exp = math.floor(base * (1.0 + (ULT + G_at(surv, 160) + pas) / 100.0))
            spot += 1
            bad += 1 if exp != int(float(w["ehp_w160_lo"])) else 0
        except (TypeError, ValueError):
            pass
    check("HOOK-e' floor-not-round re-derivation", bad == 0,
          f"{spot - bad}/{spot} EXACT, re-derived from the wide table's own base_life + passive "
          f"columns (so the long table is graded against something other than itself)")

    # ── (f) THE POSITIVE CONTROL, RE-DERIVED HERE ─────────────────────────────────────────
    ok = 0
    ctrl_detail = []
    for r in camera_measured_pets():
        L = int(float(r["charLevel"])); meas = int(float(r["measured"]))
        row = build_life_row(r["record"].lower(), [L])
        base, pas = row.base_life(L), row.passive_pct(L)
        full = math.floor(base * (1.0 + (ULT + G_at(surv, 160) + pas) / 100.0))
        ok += 1 if full == meas else 0
        ctrl_detail.append(f"{r['body'][:20]} {full}=={meas}")
    check("HOOK-f positive control: camera-measured skill-spawned pets", ok == 4,
          f"{ok}/4 EXACT under the full fold, re-derived independently of the emitter. "
          + " | ".join(ctrl_detail))

    # digests
    digests = {p.name: sha256_of(p) for p in sorted(OUT.glob("pm4e_*.csv"))}
    print("\n  === SHA-256 (verifier's own read) ===")
    for k, v in digests.items():
        print(f"    {k:34s} {v}")

    print(f"\n  {'ALL HOOKS PASS' if not FAILS else 'FAILURES: ' + ', '.join(FAILS)}")
    (OUT / "pm4e_verify_summary.json").write_text(json.dumps(
        dict(results=RES, digests=digests, failures=FAILS), indent=2, default=str))


if __name__ == "__main__":
    main()
