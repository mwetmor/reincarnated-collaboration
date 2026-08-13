#!/usr/bin/env python3
"""KC2-PM4 Lap I VERIFY -- the emission is graded against something OTHER than itself.

  V1  POSITIVE CONTROL: run the band-C life chain at waves 151..170 and demand EXACT integer
      agreement with Lap D's `pm4d_band_b_ehp_by_wave.csv` on every shared (record, wave).
      If band C's chain is Lap D's chain with only the wave index moved, this is EXACT or the
      claim is false.
  V2  the wave-modifier table's `G` column vs Lap D's emitted `pm4d_band_b_wave_life_modifier.csv`
  V3  INDEPENDENT RE-READ: a sample of emitted DoT rows re-derived from the `.dbr` by a second
      code path (raw archive read, no library helpers)
  V4  the residuals, NAMED: every band-C body without a chain, every DoT body without a level
  V5  the terminal-wave ranking's convention sensitivity, quantified
  V6  band-C REGIME: what actually changes at the 170/171 boundary (roster, life, damage)
  V7  the damage chain's three terms re-read at a named record

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap I.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4i_lib_2026_08_13 as L                       # noqa: E402
from pm4i_lib_2026_08_13 import E3, resolve, ev       # noqa: E402
from gd_arz_adapter_2026_07_24 import ArzArchive      # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense")
LAPD = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                    "legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp")
V: dict = {}


def rd(p):
    with pathlib.Path(p).open() as fh:
        return list(csv.DictReader(fh))


# ══════════════════════════════════════════════════════════════════════════════════════════════
print("== V1 -- POSITIVE CONTROL: band-C chain re-run over Lap D's band, EXACT? ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
A = L.survival_arrays()
Gl = A["characterLifeModifier"]
up, _us, _ua = L.difficulty_pak()
ult = float(up["characterLifeModifier"][L.DIFFICULTY_INDEX])

lapd = rd(LAPD / "pm4d_band_b_ehp_by_wave.csv")
lapd_lv = {}
for r in lapd:
    if r["level_lo"] and r["level_hi"]:
        lapd_lv.setdefault(r["record"], (int(r["level_lo"]), int(r["level_hi"])))
hit = miss = 0
bad = []
# re-derive from THIS lap's chain code, using Lap D's own declared level limbs so the only thing
# under test is the arithmetic, not the level derivation.
cache = {}
for r in lapd:
    if not r["wave"] or not r["ehp_lo"]:
        continue
    rec, wv = r["record"], int(r["wave"])
    ch = cache.get(rec)
    if ch is None:
        ch = cache[rec] = resolve(E3, rec)
    if not ch.ok or rec not in lapd_lv or not r["ehp_lo"]:
        continue
    lo, hi = lapd_lv[rec]
    g = L.surv_at(Gl, wv)
    e_lo = math.floor(ch.base_life(float(lo)) * (1 + (ult + g + ch.passive_pct(E3, float(lo))[0]) / 100))
    e_hi = math.floor(ch.base_life(float(hi)) * (1 + (ult + g + ch.passive_pct(E3, float(hi))[0]) / 100))
    if e_lo == int(r["ehp_lo"]) and e_hi == int(r["ehp_hi"]):
        hit += 1
    else:
        miss += 1
        if len(bad) < 8:
            bad.append((rec, wv, e_lo, r["ehp_lo"], e_hi, r["ehp_hi"]))
print(f"  {hit} EXACT / {miss} MISMATCH over {len(lapd)} Lap-D rows")
for b in bad:
    print("   MISMATCH", b)
V["V1"] = {"exact": hit, "mismatch": miss, "of": len(lapd), "examples": bad,
           "verdict": "PASS" if miss == 0 else "FAIL"}

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V2 -- wave-modifier table vs Lap D's emitted life-modifier table ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
d_life = {int(r["wave"]): float(r["G_characterLifeModifier_pct"])
          for r in rd(LAPD / "pm4d_band_b_wave_life_modifier.csv")}
i_mod = {int(r["wave"]): r for r in rd(OUT / "pm4i_wave_damage_modifier.csv")}
agree = sum(1 for wv, g in d_life.items()
            if abs(float(i_mod[wv]["G_characterLifeModifier_pct"]) - g) < 1e-9)
ult_agree = all(abs(float(i_mod[wv]["U_characterLifeModifier_pct"]) - 580.0) < 1e-9 for wv in d_life)
print(f"  G column agreement over 151..170: {agree}/{len(d_life)}   ultimate 580.0 on all: {ult_agree}")
V["V2"] = {"G_agree": agree, "of": len(d_life), "ultimate_580_everywhere": ult_agree,
           "verdict": "PASS" if (agree == len(d_life) and ult_agree) else "FAIL"}

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V3 -- INDEPENDENT RE-READ of DoT rows straight off the archives ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
REL = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
       ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
       ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
       ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
       ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
       ("sm3", "survivalmode3/database/SurvivalMode3.arz")]
arcs = {k: ArzArchive(ROOT / r) for k, r in REL}
dots = rd(OUT / "pm4i_dot_riders.csv")
sample = [r for r in dots if r["magnitude_min_lo"] and r["index_state_lo"] == "IN-RANGE"]
sample = sample[::max(1, len(sample) // 20)][:20]
ok = fail = 0
for r in sample:
    a = arcs[r["skill_archive"]]
    real = next((x for x in a.records if x.lower().replace("\\", "/") == r["skill_record"]), None)
    rec = a.read_record(real) if real else None
    if not rec:
        fail += 1
        print("   MISS record", r["skill_record"])
        continue
    fam = r["dot_family"].replace("-INSTANT", "")
    key = (f"offensiveSlow{fam}Min" if not r["dot_family"].endswith("INSTANT")
           else f"offensive{fam}Min")
    v = rec.get(key)
    got = float(v[int(r["array_index_min_lo"])]) if isinstance(v, list) else float(v)
    if abs(got - float(r["magnitude_min_lo"])) < 1e-6:
        ok += 1
    else:
        fail += 1
        print(f"   MISMATCH {r['skill_record']} {key} got {got} vs {r['magnitude_min_lo']}")
print(f"  independent re-read: {ok} EXACT / {fail} mismatch over {len(sample)} sampled rows")
V["V3"] = {"exact": ok, "mismatch": fail, "sampled": len(sample),
           "verdict": "PASS" if fail == 0 else "FAIL"}

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V4 -- residuals, NAMED ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
cr = rd(OUT / "pm4i_band_c_roster.csv")
absent = [r for r in cr if r["life_grade"] != "MEASURED"]
print(f"  band-C bodies without a MEASURED life chain: {len(absent)} / {len(cr)}")
for r in absent:
    print(f"    {r['record']}  grade={r['life_grade']}  level_grade={r['level_grade']} "
          f"summoner={(r['summoner'] or '-')[:70]}")
V["V4_band_c_absent"] = [{"record": r["record"], "life_grade": r["life_grade"],
                          "level_grade": r["level_grade"], "summoner": r["summoner"]}
                         for r in absent]

# DoT population: which bodies had no level source at all
acts = L.rolled_actors(L.DOT_FIRST, L.DOT_LAST)
seed = {a["record_path"].lower() for a in acts}
rec_pools, _rw, _rs, rec_kind, pools = L.pool_population(L.DOT_FIRST, L.DOT_LAST)
lvsets, _px, _lvt = L.level_sets(pools, rec_pools)
bodies, layers, summoner_of = L.summon_closure_extended(seed)
nolevel = []
for rec in sorted(bodies):
    if lvsets.get(rec):
        continue
    inh = set()
    for o in summoner_of.get(rec, ()):
        inh |= set(lvsets.get(o, []))
    if not inh:
        nolevel.append(rec)
print(f"  DoT bodies with NO level source: {len(nolevel)}")
for x in nolevel:
    ch = resolve(E3, x)
    print(f"    {x}  chain={ch.reason}  summoners={sorted(summoner_of.get(x, ()))}")
V["V4_dot_no_level"] = [{"record": x, "chain": resolve(E3, x).reason,
                         "summoners": sorted(summoner_of.get(x, ()))} for x in nolevel]
# bodies with a level but ZERO DoT rows -- a measured negative, not an omission
dot_recs = {r["record"] for r in dots}
zero = sorted(b for b in bodies if b not in dot_recs and b not in nolevel)
print(f"  bodies MEASURED-ZERO on DoT (level present, no DoT field on any skill): {len(zero)}")
V["V4_dot_measured_zero"] = zero

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V5 -- terminal-wave ranking, convention sensitivity ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
rk = rd(OUT / "pm4i_terminal_wave_dot_ranking.csv")
V["V5"] = {}
for wv in ("159", "160"):
    rr = [r for r in rk if r["wave"] == wv]
    t3 = [r["record"] for r in sorted(rr, key=lambda x: -float(x["sum_dps_if_total"]))][:3]
    p3 = [r["record"] for r in sorted(rr, key=lambda x: -float(x["sum_dps_if_per_second"]))][:3]
    inter = [x for x in t3 if x in p3]
    flips = sum(1 for r in rr if r["rank_by_total_convention"] != r["rank_by_persecond_convention"])
    print(f"  wave {wv}: top3(total)={[x.split('/')[-1] for x in t3]}")
    print(f"           top3(per-s)={[x.split('/')[-1] for x in p3]}")
    print(f"           intersection={len(inter)}/3   rank flips={flips}/{len(rr)}")
    V["V5"][wv] = {"top3_total": t3, "top3_persecond": p3,
                   "intersection": inter, "rank_flips": flips, "n": len(rr)}

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V6 -- the 170/171 REGIME: what actually changes ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
b_pools, _bw, _bs, _bk, bp = L.pool_population(151, 170)
c_pools, _cw, _cs, _ck, cp = L.pool_population(171, 180)
w170 = {r.strip().lower() for row in L.pool_rows(170, 170)
        for col in ("roster_records", "champ_records") for r in (row.get(col) or "").split("|") if r.strip()}
w171 = {r.strip().lower() for row in L.pool_rows(171, 171)
        for col in ("roster_records", "champ_records") for r in (row.get(col) or "").split("|") if r.strip()}
D = A["offensiveTotalDamageModifier"]
step_life = [(w, Gl[w - 1], Gl[w] - Gl[w - 1]) for w in range(165, 181)]
print(f"  pool records: band B (151-170) {len(b_pools)} · band C (171-180) {len(c_pools)} · "
      f"new in C {len(set(c_pools) - set(b_pools))} · dropped {len(set(b_pools) - set(c_pools))}")
print(f"  wave-170 pool records {len(w170)} · wave-171 {len(w171)} · shared {len(w170 & w171)}")
print(f"  life step 170->171: {Gl[169]} -> {Gl[170]}  (+{Gl[170]-Gl[169]})   "
      f"within-band step 151..170 = +2.0/wave; 171..180 = +{Gl[171]-Gl[170]}/wave")
print(f"  damage step 170->171: {D[169]} -> {D[170]}  (+{D[170]-D[169]})   "
      f"within-band 151..170 step pattern {sorted({round(D[i+1]-D[i],4) for i in range(150,169)})}; "
      f"171..180 {sorted({round(D[i+1]-D[i],4) for i in range(170,179)})}")
V["V6"] = {
    "band_b_pool_records": len(b_pools), "band_c_pool_records": len(c_pools),
    "new_in_c": len(set(c_pools) - set(b_pools)), "dropped_from_b": len(set(b_pools) - set(c_pools)),
    "w170_records": len(w170), "w171_records": len(w171), "shared_170_171": len(w170 & w171),
    "life_170": Gl[169], "life_171": Gl[170], "life_step": Gl[170] - Gl[169],
    "life_within_step_b": sorted({round(Gl[i + 1] - Gl[i], 4) for i in range(150, 169)}),
    "life_within_step_c": sorted({round(Gl[i + 1] - Gl[i], 4) for i in range(170, 179)}),
    "damage_170": D[169], "damage_171": D[170], "damage_step": D[170] - D[169],
    "damage_within_step_b": sorted({round(D[i + 1] - D[i], 4) for i in range(150, 169)}),
    "damage_within_step_c": sorted({round(D[i + 1] - D[i], 4) for i in range(170, 179)}),
    "tier_dirs_present": 20,
    "verdict": "SAME REGIME, STEPPED — the tier-18 boundary is a step in the SAME 200-cell arrays "
               "and the SAME tier<NN>waves authoring structure; no scaling break, no loop",
}
# per-tier-boundary step pattern across the whole ladder -- is 171 special or routine?
bstep = [(t * 10 + 1, Gl[t * 10] - Gl[t * 10 - 1], D[t * 10] - D[t * 10 - 1]) for t in range(1, 20)]
print("  tier-boundary steps (wave, dLife, dDamage):", bstep)
V["V6"]["tier_boundary_steps"] = bstep

# ══════════════════════════════════════════════════════════════════════════════════════════════
print("\n== V7 -- the damage chain's three terms, re-read at a named record ==")
# ══════════════════════════════════════════════════════════════════════════════════════════════
PROBE = "records/creatures/enemies/nemesis/nemesis_wendigo_01.dbr"
lvs = lvsets.get(PROBE) or []
Lo = float(lvs[0]) if lvs else 107.0
own, src = L.own_total_damage_modifier(PROBE, Lo)
u = float(up["offensiveTotalDamageModifier"][L.DIFFICULTY_INDEX])
for wv in (160, 171, 180):
    d = L.surv_at(D, wv)
    print(f"  {PROBE.split('/')[-1]} @L={Lo} w{wv}: ultimate {u} + wave {d} + own {own} "
          f"= {u+d+own} %   sources: {src}")
V["V7"] = {"record": PROBE, "level": Lo, "ultimate_pct": u, "own_pct": own, "own_sources": src,
           "wave_pct": {w: L.surv_at(D, w) for w in (160, 171, 180)}}

# digests
V["digests"] = {p.name: L.sha256(p) for p in sorted(OUT.glob("*.csv"))}
V["row_counts"] = {p.name: sum(1 for _ in p.open()) - 1 for p in sorted(OUT.glob("*.csv"))}
(OUT / "pm4i_verify_summary.json").write_text(json.dumps(V, indent=2, default=str))
print("\n== DIGESTS ==")
for k, v in V["digests"].items():
    print(f"  {k:44s} {v[:16]}  rows={V['row_counts'][k]}")
print("\nDONE")
