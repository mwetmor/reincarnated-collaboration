#!/usr/bin/env python3
"""KC2-PM4 Lap I -- band-C (waves 171-180) SPAWN/ROSTER table decode + basis re-verification.

Target 4 asks for "the roster/spawn tables" past wave 170, not only the eHP surface.  This module
emits the per-wave spawn composition AND re-verifies the pool basis
(`pe6_crucible_wave_pools_v2.csv`, a legolas emission) against the `.dbr` proxy records directly,
so band C does not rest on a CSV that is merely inherited.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap I.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4i_lib_2026_08_13 as L                     # noqa: E402
from pm4i_lib_2026_08_13 import E3                  # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense")
R: dict = {}
A = L.survival_arrays()

# ── per-wave composition, bands B and C side by side ──────────────────────────────────────────
hdr = ["wave", "content_tier", "band", "n_pool_rows", "n_spawn_points", "n_proxies",
       "n_distinct_pools", "n_roster_records", "n_champ_records", "n_distinct_records",
       "sum_spawn_min", "sum_spawn_max", "sum_champion_min", "sum_champion_max",
       "pool_kinds", "spawnMinAdj", "spawnMaxAdj", "spawnChampionMinAdj", "spawnChampionMaxAdj",
       "G_life_pct", "D_damage_pct", "grade", "basis"]
rows = []
for wv in range(151, 201):
    pr = L.pool_rows(wv, wv)
    if not pr:
        continue
    rost = {x.strip().lower() for r in pr for x in (r.get("roster_records") or "").split("|") if x.strip()}
    chmp = {x.strip().lower() for r in pr for x in (r.get("champ_records") or "").split("|") if x.strip()}
    rows.append(dict(
        wave=wv, content_tier=L.content_tier(wv),
        band=("B (Lap D)" if wv <= 170 else "C (Lap I)"),
        n_pool_rows=len(pr), n_spawn_points=len({r["spawn_point"] for r in pr}),
        n_proxies=len({r["proxy_record"] for r in pr}),
        n_distinct_pools=len({r["pool_record"] for r in pr}),
        n_roster_records=len(rost), n_champ_records=len(chmp),
        n_distinct_records=len(rost | chmp),
        sum_spawn_min=sum(float(r["spawn_min"] or 0) for r in pr),
        sum_spawn_max=sum(float(r["spawn_max"] or 0) for r in pr),
        sum_champion_min=sum(float(r["champion_min"] or 0) for r in pr),
        sum_champion_max=sum(float(r["champion_max"] or 0) for r in pr),
        pool_kinds="|".join(sorted({r["pool_kind"] for r in pr})),
        spawnMinAdj=L.surv_at(A["spawnMinAdj"], wv), spawnMaxAdj=L.surv_at(A["spawnMaxAdj"], wv),
        spawnChampionMinAdj=L.surv_at(A["spawnChampionMinAdj"], wv),
        spawnChampionMaxAdj=L.surv_at(A["spawnChampionMaxAdj"], wv),
        G_life_pct=L.surv_at(A["characterLifeModifier"], wv),
        D_damage_pct=L.surv_at(A["offensiveTotalDamageModifier"], wv),
        grade="MEASURED",
        basis="data/kc2/pe6_crucible_wave_pools_v2.csv (legolas pe6 emission, re-verified below) "
              "+ balancingadjustment_survivalmode_enemies03.dbr@sm_mod"))
p = OUT / "pm4i_band_c_wave_composition.csv"
with p.open("w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=hdr, extrasaction="ignore")
    wr.writeheader()
    wr.writerows(rows)
print(f"wrote {p.name} rows={len(rows)} sha256={L.sha256(p)[:16]}")
R["composition"] = {"rows": len(rows), "sha256": L.sha256(p)}

for r in rows:
    if r["wave"] in (168, 169, 170, 171, 172, 175, 180):
        print(f"  w{r['wave']} tier{r['content_tier']:>3} rows={r['n_pool_rows']:>3} "
              f"sp={r['n_spawn_points']} pools={r['n_distinct_pools']:>2} "
              f"recs={r['n_distinct_records']:>3} spawnmax={r['sum_spawn_max']:>5} "
              f"champmax={r['sum_champion_max']:>4} kinds={r['pool_kinds']}")

# ── BASIS RE-VERIFICATION: the pe6 CSV vs the proxy `.dbr` records, band C only ───────────────
print("\n== band-C pool basis re-verified against the proxy .dbr records ==")
ok = bad = 0
mismatch = []
seen = set()
for r in L.pool_rows(171, 180):
    key = (r["proxy_record"], r["pool_record"])
    if key in seen:
        continue
    seen.add(key)
    px, arc = E3.winner(r["proxy_record"])
    if not px:
        bad += 1
        mismatch.append(("PROXY-ABSENT", r["proxy_record"], ""))
        continue
    refs = set()
    for i in range(1, 41):
        for f in (f"spawnPool{i}", f"spawnObjects{i}", f"pool{i}", f"spawnPoolName{i}"):
            v = px.get(f)
            if isinstance(v, list):
                v = v[0] if v else None
            if isinstance(v, str) and v.lower().endswith(".dbr"):
                refs.add(v.lower().replace("\\", "/"))
    if r["pool_record"].lower() in refs:
        ok += 1
    else:
        bad += 1
        if len(mismatch) < 6:
            mismatch.append(("POOL-NOT-IN-PROXY", r["proxy_record"], r["pool_record"]))
print(f"  (proxy, pool) pairs confirmed on the proxy record: {ok} confirmed / {bad} not-confirmed "
      f"of {len(seen)}")
for m in mismatch[:6]:
    print("   ", m)
R["basis_recheck"] = {"confirmed": ok, "not_confirmed": bad, "pairs": len(seen),
                      "examples": mismatch[:6]}

# ── does any band-C ROSTER record fail to exist in Ed-III? ────────────────────────────────────
c_pools, _w, _s, _k, _p = L.pool_population(171, 180)
absent = sorted(rec for rec in c_pools if E3.winner(rec)[0] is None)
print(f"\n  band-C pool records ABSENT from Edition-III: {len(absent)} / {len(c_pools)}")
for a in absent:
    print("   ", a)
R["records_absent_from_corpus"] = absent

(OUT / "pm4i_bandc_spawn_summary.json").write_text(json.dumps(R, indent=2, default=str))
print("\nDONE")
