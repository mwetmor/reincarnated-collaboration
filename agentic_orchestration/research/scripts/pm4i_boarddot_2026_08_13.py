#!/usr/bin/env python3
"""KC2-PM4 Lap I -- per-wave BOARD DoT load over waves 151-160, actor-weighted.

The per-record ranking (`pm4i_terminal_wave_dot_ranking.csv`) answers "which BODY carries the most
DoT".  This answers the different question "which WAVE carries the most DoT", which is the one
Matt's banked testimony ("some kind of poison/dot seemed to effect me in a major way on my last
wave") actually puts under test.  Every body's own summon closure rides with it, exactly as in the
ranking, so the two files are on the same footing.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap I.
"""
from __future__ import annotations
import collections, csv, pathlib, sys
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4i_lib_2026_08_13 as L                       # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense")
dots = list(csv.DictReader((OUT / "pm4i_dot_riders.csv").open()))
acts = L.rolled_actors(L.DOT_FIRST, L.DOT_LAST)
seed = {a["record_path"].lower() for a in acts}
bodies, _layers, summoner_of = L.summon_closure_extended(seed)

by_rec_tot, by_rec_ps, fam_tot = (collections.defaultdict(float), collections.defaultdict(float),
                                  collections.defaultdict(lambda: collections.defaultdict(float)))
for r in dots:
    if r["is_dot"] != "True":
        continue
    if r["dps_if_field_is_total_lo"]:
        by_rec_tot[r["record"]] += float(r["dps_if_field_is_total_lo"])
        fam_tot[r["record"]][r["dot_family"]] += float(r["dps_if_field_is_total_lo"])
    if r["dps_if_field_is_per_second_lo"]:
        by_rec_ps[r["record"]] += float(r["dps_if_field_is_per_second_lo"])

family_of = collections.defaultdict(set)
for rec in seed:
    family_of[rec].add(rec)
    for pet in bodies - seed:
        if rec in summoner_of.get(pet, ()):
            family_of[rec].add(pet)

FAM = ("Poison", "Bleeding", "Life", "Fire", "Cold", "Lightning", "Physical", "LifeLeach")
hdr = (["wave", "n_actors", "n_distinct_records", "n_dot_bearing_actors",
        "board_dot_dps_if_total", "board_dot_dps_if_per_second",
        "dot_per_actor_if_total", "top_record", "top_record_dps_if_total"]
       + [f"board_{f.lower()}_dps_if_total" for f in FAM] + ["grade", "basis"])
rows = []
for wv in range(L.DOT_FIRST, L.DOT_LAST + 1):
    aw = [a for a in acts if int(a["wave"]) == wv]
    tot = ps = 0.0
    per_fam = collections.defaultdict(float)
    per_rec = collections.defaultdict(float)
    nbear = 0
    for a in aw:
        rec = a["record_path"].lower()
        t = sum(by_rec_tot.get(x, 0.0) for x in family_of.get(rec, {rec}))
        p = sum(by_rec_ps.get(x, 0.0) for x in family_of.get(rec, {rec}))
        for x in family_of.get(rec, {rec}):
            for f, v in fam_tot.get(x, {}).items():
                per_fam[f] += v
        tot += t
        ps += p
        per_rec[rec] += t
        nbear += 1 if t else 0
    top = max(per_rec.items(), key=lambda kv: kv[1], default=("", 0.0))
    row = dict(wave=wv, n_actors=len(aw),
               n_distinct_records=len({a["record_path"].lower() for a in aw}),
               n_dot_bearing_actors=nbear,
               board_dot_dps_if_total=round(tot, 3), board_dot_dps_if_per_second=round(ps, 3),
               dot_per_actor_if_total=round(tot / len(aw), 3) if aw else 0,
               top_record=top[0], top_record_dps_if_total=round(top[1], 3),
               grade="MEASURED (magnitudes) — the two dps columns bracket the DECLARED GAP on the "
                     "total-vs-per-second field convention (method.md § 5)",
               basis="pm4i_dot_riders.csv x frozen baton actors[] at wave w, each body's summon "
                     "closure included")
    for f in FAM:
        row[f"board_{f.lower()}_dps_if_total"] = round(per_fam.get(f, 0.0), 3)
    rows.append(row)
p = OUT / "pm4i_board_dot_by_wave.csv"
with p.open("w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=hdr, extrasaction="ignore")
    wr.writeheader(); wr.writerows(rows)
print(f"wrote {p.name} rows={len(rows)} sha256={L.sha256(p)[:16]}")
for r in rows:
    print(f"  w{r['wave']}  actors={r['n_actors']:>2}  board_tot={r['board_dot_dps_if_total']:>10,.0f}  "
          f"per_actor={r['dot_per_actor_if_total']:>8,.0f}  poison={r['board_poison_dps_if_total']:>8,.0f} "
          f"bleed={r['board_bleeding_dps_if_total']:>8,.0f}  top={r['top_record'].split('/')[-1]}")
