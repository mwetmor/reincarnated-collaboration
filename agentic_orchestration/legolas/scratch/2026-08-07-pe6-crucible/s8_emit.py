#!/usr/bin/env python3
"""S8 — PE6 emit: machine-readable per-wave and per-(wave,spawnpoint,pool) tables for the sim.
RAW = DB-resident pool values. ADJ = + Gladiator (Ultimate) gameproxies adjustment.
gameproxies (survival, sm_mod): spawnMin=[0,0,1] spawnMax=[0,1,1] championMin=[0,0,1]
championMax=[0,1,1] spawnMinModifier=[0,112,120]  (index Normal/Elite/Ultimate)
"""
import json, csv, pathlib, collections

W = json.load(open("s4_waves_full.json"))
ADJ_SMIN, ADJ_SMAX, ADJ_CMIN, ADJ_CMAX, SMIN_MOD = 1.0, 1.0, 1.0, 1.0, 1.20

def kind_of(p):
    if "/poolsboss" in p: return "BOSS"
    if "/poolshero" in p: return "HERO"
    if "/poolsdevotion" in p: return "DEVOTION"
    if "/poolsbounty" in p: return "BOUNTY"
    return "trash"

rows_wave, rows_pool = [], []
for w in sorted(W, key=lambda x: x["gwave"]):
    g = w["gwave"]
    rmin = rmax = rexp = 0.0
    amin = amax = aexp = 0.0
    kinds = collections.Counter(); nem = False; amb = 0
    for e in w["points"]:
        opts = [o for o in e["diffs"]["gladiator"] if not o.get("UNRESOLVED")]
        if not opts: continue
        if e["cls"] == "ProxyAmbush": amb += 1
        wt = sum(o["w"] for o in opts) or 1.0
        rmin += min(o["smin"] for o in opts)
        rmax += max(o["smax"] + o["cmax"] for o in opts)
        rexp += sum(o["w"] * (((o["smin"] + o["smax"]) / 2) + (o["cch"] / 100) * ((o["cmin"] + o["cmax"]) / 2))
                    for o in opts) / wt
        # GUARDED adjustment (INFERRED): the gameproxies spawn/champion deltas are applied ONLY to
        # multi-spawn (trash) pools, spawnMax >= 2. Applying them to 1-of-1 boss/nemesis pools would
        # yield 2 nemeses per spawn point at wave 160, which the DB cannot corroborate. Guard declared.
        def adj(o):
            if o["smax"] < 2:                       # singleton boss / champion-only pool: untouched
                return o["smin"], o["smax"], o["cmin"], o["cmax"]
            return ((o["smin"] + ADJ_SMIN) * SMIN_MOD, o["smax"] + ADJ_SMAX,
                    o["cmin"] + (ADJ_CMIN if o["cch"] else 0), o["cmax"] + (ADJ_CMAX if o["cch"] else 0))
        A = [adj(o) for o in opts]
        amin += min(a[0] for a in A)
        amax += max(a[1] + a[3] for a in A)
        aexp += sum(o["w"] * (((a[0] + a[1]) / 2) + (o["cch"] / 100) * ((a[2] + a[3]) / 2))
                    for o, a in zip(opts, A)) / wt
        for o in opts:
            k = kind_of(o["pool"]); kinds[k] += 1
            if "nemesis" in o["pool"]: nem = True
            rows_pool.append(dict(
                global_wave=g, tier=w["tier"], tier_wave=w["wave"], spawn_point=e["pt"],
                proxy_class=e["cls"], proxy_record=e["path"], proxy_archive=e["owner"],
                legendary_override=(not e["fallback"]["gladiator"]),
                pool_record=o["pool"], pool_archive=o["owner"], pool_weight=o["w"], pool_kind=k,
                spawn_min=o["smin"], spawn_max=o["smax"],
                champion_chance=o["cch"], champion_min=o["cmin"], champion_max=o["cmax"],
                roster_n=len(o["roster"]), champ_roster_n=len(o["champroster"]),
                roster_names=" | ".join(r["name"] for r in o["roster"]),
                roster_records=" | ".join(r["rec"] for r in o["roster"]),
                champ_names=" | ".join(r["name"] for r in o["champroster"]),
                champ_records=" | ".join(r["rec"] for r in o["champroster"]),
            ))
    rows_wave.append(dict(
        global_wave=g, tier=w["tier"], tier_wave=w["wave"], spawn_points=w["npts"],
        ambush_points=amb, archives="+".join(w["owners"]),
        raw_min=round(rmin, 2), raw_max=round(rmax, 2), raw_E=round(rexp, 2),
        glad_adj_min=round(amin, 2), glad_adj_max=round(amax, 2), glad_adj_E=round(aexp, 2),
        n_trash=kinds.get("trash", 0), n_boss=kinds.get("BOSS", 0), n_hero=kinds.get("HERO", 0),
        n_devotion=kinds.get("DEVOTION", 0), n_bounty=kinds.get("BOUNTY", 0),
        nemesis_wave=nem,
        aspirant_E=w["aspirant"]["E"], challenger_E=w["challenger"]["E"], gladiator_E=w["gladiator"]["E"],
    ))

with open("pe6_crucible_waves.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows_wave[0])); wr.writeheader(); wr.writerows(rows_wave)
with open("pe6_crucible_wave_pools.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows_pool[0])); wr.writeheader(); wr.writerows(rows_pool)
print(f"[wrote pe6_crucible_waves.csv]      {len(rows_wave)} rows")
print(f"[wrote pe6_crucible_wave_pools.csv] {len(rows_pool)} rows")

print("\n=== PRIORITY BAND totals ===")
for lo, hi, lbl in ((1, 93, "sitting 1: waves 1-93"), (150, 160, "sitting 2: waves 150-160")):
    sub = [r for r in rows_wave if lo <= r["global_wave"] <= hi]
    print(f"  {lbl}: n={len(sub)}  Σraw_E={sum(r['raw_E'] for r in sub):.1f}  "
          f"Σglad_adj_E={sum(r['glad_adj_E'] for r in sub):.1f}  "
          f"nemesis waves={[r['global_wave'] for r in sub if r['nemesis_wave']]}")
print("\n=== priority-band per-wave (raw / gladiator-adjusted) ===")
print(f"{'wave':>4} {'raw_min':>7} {'raw_max':>7} {'raw_E':>7} | {'adj_min':>7} {'adj_max':>7} {'adj_E':>7}  kinds")
for r in rows_wave:
    if not (1 <= r["global_wave"] <= 93 or 150 <= r["global_wave"] <= 160): continue
    print(f"{r['global_wave']:4d} {r['raw_min']:7.1f} {r['raw_max']:7.1f} {r['raw_E']:7.2f} | "
          f"{r['glad_adj_min']:7.1f} {r['glad_adj_max']:7.1f} {r['glad_adj_E']:7.2f}  "
          f"t{r['n_trash']} B{r['n_boss']} H{r['n_hero']} D{r['n_devotion']} Y{r['n_bounty']}"
          + ("  <NEMESIS>" if r["nemesis_wave"] else ""))
