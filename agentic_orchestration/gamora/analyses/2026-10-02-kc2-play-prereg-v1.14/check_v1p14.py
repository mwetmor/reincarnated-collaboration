#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.14 · THE ORACLE CHECKS (gamora, 2026-10-02): COMPLETENESS, INERTNESS, LAW (a), LAW (b).

Reads the oracle traces written by `oracle_trace_v3p11.py` (gzipped beside this file, `oracle_trace/`) and the static
derivations of `derive_v1p14.py` (`derive_v1p14.json`). No port output is read anywhere.

  0. COMPLETENESS (jack-ryan OBS-1, collab 29124a46e; conductor precondition): per arm x salt, the ladder ran w151..w160
     contiguous, every wave ended `cleared/board_empty` or `player_death/player_died`, no exception escaped the true
     simulate_wave, `raised` is None, 10 capture rows; a leg-A survival is a w160 `cleared/board_empty`. ANY FAILURE IS A
     STOP: nothing is derived from that cell (the checker exits non-zero before deriving).
  1. INERTNESS: the hooked run's capture rows (the oracle's own per-wave summaries) are byte-identical to the bare run's,
     every arm x salt; and per-salt (`single`) runs equal the batch run on the same rows AND on the whole trace.
  2. LAW (a): every EXACT row measurable on the oracle is measured on the 25 cells (leg A); the rest are cited.
  3. LAW (b): the v3.8-v3.11 regime measurements each re-opened row reads (cleared terminals, pursuit operands, ...).

Run:  python3 check_v1p14.py [--ingest <scratch dir>]   -> results_v1p14.json; exit 0 iff completeness + inertness hold.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TDIR = HERE / "oracle_trace"
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
WAVES = list(range(151, 161))
DSTATES = ("CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(o) -> bytes:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), default=str).encode()


def ingest(scratch: Path) -> None:
    TDIR.mkdir(exist_ok=True)
    names = [f"hooked_{a}.json" for a in ARMS] + [f"bare_{a}.json" for a in ARMS] + \
            [f"single_{a}_s{s}.json" for a in ARMS for s in SALTS] + ["repeat_M0_s2.json"]
    for n in names:
        (TDIR / (n + ".gz")).write_bytes(gzip.compress((scratch / n).read_bytes(), mtime=0))


def load(n: str) -> dict:
    return json.loads(gzip.decompress((TDIR / (n + ".gz")).read_bytes()))


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--ingest":
        ingest(Path(sys.argv[2]))
    D = json.loads((HERE / "derive_v1p14.json").read_text())
    H = {a: load(f"hooked_{a}.json") for a in ARMS}
    B = {a: load(f"bare_{a}.json") for a in ARMS}
    S1 = {(a, s): load(f"single_{a}_s{s}.json") for a in ARMS for s in SALTS}
    REP = load("repeat_M0_s2.json")
    R: dict = {"files": {p.name: sha(p.read_bytes()) for p in sorted(TDIR.glob("*.gz"))}}

    # ============================================================================== 0 · COMPLETENESS (STOP on failure)
    comp, stop = {}, []
    for a in ARMS:
        for s in SALTS:
            t = H[a]["trace"]["salts"][str(s)]
            ws = [w["wave"] for w in t["waves"]]
            oc = [(w["wave"], w["outcome"], w["termination_reason"]) for w in t["waves"]]
            good_end = all((o, tr) in (("cleared", "board_empty"), ("player_death", "player_died")) for _, o, tr in oc)
            first_death = next((w for w, o, _ in oc if o == "player_death"), None)
            leg_a = t["leg_a_terminal"]
            ok = {"ladder w151..w160 contiguous": ws == WAVES,
                  "every wave cleared/board_empty or player_death/player_died": good_end,
                  "no exception escaped simulate_wave": t["exceptions"] == [],
                  "raised is None": t["raised"] is None,
                  "10 capture rows": t["capture_rows_n"] == 10,
                  "run_one's leg A == the first player_death wave (else survived to 160)":
                      (leg_a.get("wave") == first_death) if first_death else (leg_a.get("wave") is None
                                                                               and leg_a.get("survived_to") == 160),
                  "a leg-A survival is a genuine w160 clear": (first_death is not None) or oc[-1] == (160, "cleared", "board_empty")}
            comp[f"{a}|{s}"] = {"waves": ws, "outcomes": oc, "leg_a": leg_a, "checks": ok,
                                "terminal": first_death or "cleared_w160"}
            if not all(ok.values()):
                stop.append(f"{a}|{s}")
    R["completeness"] = {"per_cell": comp, "STOP_cells": stop,
                         "counts": {"cells": len(comp), "complete": len(comp) - len(stop)}}
    if stop:
        (HERE / "results_v1p14.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str) + "\n")
        print("⛔ STOP: incomplete oracle cells", stop)
        return 2

    # ============================================================================== 1 · INERTNESS + DETERMINISM
    inert = {f"{a}|{s}": H[a]["run_one_salts"][str(s)]["rows_sha256"] == B[a]["run_one_salts"][str(s)]["rows_sha256"]
             for a in ARMS for s in SALTS}
    batch_eq_rows = {f"{a}|{s}": S1[(a, s)]["run_one_salts"][str(s)]["rows_sha256"] == H[a]["run_one_salts"][str(s)]["rows_sha256"]
                     for a in ARMS for s in SALTS}
    def _nopc(t):
        # `pools_calls` is the INSTRUMENT's log of calls to the PURE `pools_for`; its call COUNT depends on memoisation
        # warm-up across salts in one process (9 vs 7 calls at one wave), not on the oracle. Compared separately.
        return {**t, "waves": [{k: v for k, v in w.items() if k != "pools_calls"} for w in t["waves"]]}
    batch_eq_trace = {f"{a}|{s}": (canon(_nopc(S1[(a, s)]["trace"]["salts"][str(s)])) == canon(_nopc(H[a]["trace"]["salts"][str(s)]))
                                   and canon(S1[(a, s)]["streams"][str(s)]) == canon(H[a]["streams"][str(s)]))
                      for a in ARMS for s in SALTS}
    batch_eq_pools_calls = {f"{a}|{s}": [sorted({json.dumps(x[1:]) for x in w["pools_calls"]}) for w in S1[(a, s)]["trace"]["salts"][str(s)]["waves"]]
                            == [sorted({json.dumps(x[1:]) for x in w["pools_calls"]}) for w in H[a]["trace"]["salts"][str(s)]["waves"]]
                            for a in ARMS for s in SALTS}
    rep_eq = (canon(REP["trace"]) == canon(S1[("M0", 2)]["trace"]) and canon(REP["streams"]) == canon(S1[("M0", 2)]["streams"])
              and REP["run_one_salts"] == S1[("M0", 2)]["run_one_salts"])
    R["inertness"] = {"hooked == bare (capture rows), cells": sum(inert.values()),
                      "single == batch (capture rows), cells": sum(batch_eq_rows.values()),
                      "single == batch (whole trace minus the instrument's pools_for call log, + streams), cells": sum(batch_eq_trace.values()),
                      "single == batch (pools_for call log as a SET of distinct calls), cells": sum(batch_eq_pools_calls.values()),
                      "TA-X-01 repeat (M0 salt 2, run twice): byte-identical trace + streams + rows": rep_eq,
                      "per_cell": {"inert": inert, "batch_rows": batch_eq_rows, "batch_trace": batch_eq_trace}}
    if not (all(inert.values()) and all(batch_eq_rows.values())):
        (HERE / "results_v1p14.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str) + "\n")
        print("⛔ STOP: inertness / batch equivalence failed")
        return 2

    # ============================================================================== 2 · per cell, leg A
    wall = H["W1"]["trace"]["salts"]["0"]["waves"][0]["arena"]["wall_block"]
    emit = wall["emitters"]
    active = [k for k in emit if k != "p06"]
    bound10 = max(emit[k]["r_m"] for k in active) + float(wall["placement_extents_m"])
    pool = None   # POOL-466 membership: record basenames from the derive step's set digest are not listed; rebuild:
    import os
    sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src")
    cwd = os.getcwd()
    os.chdir("/Users/admin/Games/reincarnated-engine/src")
    from reincarnated.export.kc2_baton_v3p5p1_schema import pool466
    MODEL = Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
                 "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143")
    waves_json = json.loads((MODEL / "model/waves.json").read_text())
    pool, _ = pool466({"model/waves.json": waves_json})
    os.chdir(cwd)
    keys_on = {w: sorted({r["spawn_point"] for r in waves_json["pools"]["wave_spawn"] if r["global_wave"] == w})
               for w in WAVES}
    LU = dict(zip(WAVES, D["TA-X-16"]["LU-KEYS"]))
    P06 = dict(zip(WAVES, D["TA-X-16"]["P06-KEY"]))
    nonswing = set(D["sets"]["NONSWING (v3.11 graded loader)"]["members"])

    cells = {}
    for a in ARMS:
        cs_spawned = H[a]["can_swing_spawned"]
        for s in SALTS:
            t = H[a]["trace"]["salts"][str(s)]
            T = comp[f"{a}|{s}"]["terminal"]
            Tw = 160 if T == "cleared_w160" else T
            legA = [w for w in t["waves"] if w["wave"] <= Tw]
            c = {"terminal": T, "waves_played": len(legA)}
            # ---- TA-X-08 (v1.13 § F.2n / § F.2o), on the oracle's own census
            cen = Counter()
            for w in legA:
                cen.update(w["census"])
            obs = sum(len(w["ticks"]) for w in legA)
            PF = cen.get("PRE_FIGHT", 0)
            Dn = sum(cen.get(x, 0) for x in DSTATES)
            nch = cen.get("CHANNELLING", 0) + cen.get("CHANNELLING_AND_MOVING", 0)
            t8 = Counter()
            for w in legA:
                t8.update(w["ta_x_08"])
            fold = a != "M0"
            last = legA[-1]
            ntr = (last["fold_counters"][0]["n_ticks_released"] if (fold and last["fold_counters"]) else 0)
            lethal_ok = True
            if T != "cleared_w160":
                lr = last["census_last_row"]
                lethal_ok = (last["ticks"][-1][4] is not None and last["ticks"][-1][4] <= 0.0
                             and "DEAD" not in last["census"] and last["census_n_rows"] == len(last["ticks"]))
            align = all(w["obs_alignment"] and all(w["obs_alignment"].values()) for w in legA) if fold else None
            c["TA-X-08"] = {
                "observed": obs, "PRE_FIGHT": PF, "D": Dn, "n_channelling": nch, "n_released": t8["n_released"],
                "n_released_pre_fight": t8["n_released_pre_fight"],
                "n_control_suppressed_channelling": t8["n_control_suppressed_channelling"],
                "n_control_suppressed_released": t8["n_control_suppressed_released"],
                "n_control_suppressed_pre_fight": t8["n_control_suppressed_pre_fight"],
                "n_ticks_released": ntr, "trace_control_channel_entries": sum(w["ctrl_channel_entries"] for w in legA),
                "id1": obs == Dn + PF,
                "id2_restated": nch + t8["n_released"] + t8["n_control_suppressed_channelling"] == Dn,
                "id2_v1.12_text": nch + t8["n_released"] == Dn,
                "id2p": ntr == t8["n_released"] + t8["n_released_pre_fight"],
                "census_convention": {"one PRE_FIGHT per wave played": all(w["census"].get("PRE_FIGHT", 0) == 1 for w in legA),
                                      "no DEAD": "DEAD" not in cen,
                                      "lethal tick censused alive (dying cells)": lethal_ok,
                                      "census covers every observed tick": all(w["census_n_rows"] == len(w["ticks"]) for w in legA)},
                "fold_alignment": align,
                "M0 no fold": (not fold) and all(not w["fold_present"] for w in legA) if a == "M0" else None}
            c["TA-X-08"]["holds"] = (c["TA-X-08"]["id1"] and c["TA-X-08"]["id2_restated"] and c["TA-X-08"]["id2p"]
                                     and all(c["TA-X-08"]["census_convention"].values()) and (align is not False))
            # ---- TA-X-16 (v1.13 § F.2m, on the line-up fold's keys)
            per = []
            ok16 = True
            for w in legA:
                wv = w["wave"]
                lu = w["lineup"]
                picks = w["incumbent_picks"]
                filt = sorted(set(keys_on[wv]) - set(picks))
                row = {"wave": wv, "fought_keys": len(lu["fold_keys"]), "expected": LU[wv],
                       "fought_points_with_bodies": len(lu["fought_points"]),
                       "incumbent_keys_rolled": len(picks), "p06_keys_rolled_fought": int(6 in lu["fold_keys"]),
                       "p06_keys_rolled_incumbent": sum(1 for p in picks if p == 6),
                       "p06_keys_filtered": sum(1 for p in filt if p == 6), "filtered_expected": P06[wv],
                       "filtered_are_p06_only": set(filt) <= {6},
                       "bonus_off_passed": lu["bonus_spawns_enabled_passed"] is False and w["kw"]["bonus_spawns_enabled"] is False}
                row["holds"] = (row["fought_keys"] == row["expected"] and row["incumbent_keys_rolled"] == row["expected"]
                                and row["p06_keys_rolled_fought"] == 0 and row["p06_keys_rolled_incumbent"] == 0
                                and row["p06_keys_filtered"] == row["filtered_expected"] and row["filtered_are_p06_only"]
                                and row["bonus_off_passed"] and sorted(lu["fold_keys"]) == sorted(set(picks)))
                ok16 &= row["holds"]
                per.append(row)
            c["TA-X-16"] = {"per_wave": per, "n_pool_picks": sum(x["fought_keys"] for x in per),
                            "expected_sum": sum(LU[w["wave"]] for w in legA), "holds": ok16,
                            "v1.12_text (== 47)": sum(x["fought_keys"] for x in per) == 47}
            # ---- TA-X-15(a)
            bad15 = [(w["wave"], x[5], x[4]) for w in legA for x in w["actors"]
                     if (x[5] in ("p01", "p02", "p03", "p04") and x[4] != 0.0) or (x[5] == "p05" and x[4] != 4.0)
                     or x[5] not in ("p01", "p02", "p03", "p04", "p05")]
            c["TA-X-15a"] = {"holds": not bad15, "violations": bad15[:5],
                             "p05_bodies": sum(1 for w in legA for x in w["actors"] if x[5] == "p05")}
            # ---- TA-X-17 (anchor = the oracle's own emitter_xy for that placement)
            worst17, mis = 0.0, 0
            for w in legA:
                if len(w["anchors"]) != len(w["actors"]):
                    mis += 1
                    continue
                for x, an in zip(w["actors"], w["anchors"]):
                    if f"p{an[0]:02d}" != x[5]:
                        mis += 1
                    worst17 = max(worst17, math.hypot(x[2] - an[2], x[3] - an[3]))
            c["TA-X-17"] = {"max_offset_m": worst17, "anchor_alignment_failures": mis,
                            "holds": worst17 <= 8.0 and mis == 0}
            # ---- TA-X-10 / TA-X-11
            if a == "W1":
                rb = max(w["ledger"]["max_live_body_radius_m"] or 0.0 for w in legA)
                rs = max(math.hypot(x[2], x[3]) for w in legA for x in w["actors"])
                c["TA-X-10"] = {"max_body_radius_m": rb, "max_spawn_radius_m": rs, "bound": bound10,
                                "holds": max(rb, rs) <= bound10,
                                "r_wall_m (ArenaFold)": legA[0]["arena"]["r_wall_m"]}
            if a in ("W1", "W1-NULL"):
                c["TA-X-11"] = {"clamps_player": sum(w["arena"]["clamps_player_delta"] for w in legA),
                                "clamps_body": sum(w["arena"]["clamps_body_delta"] for w in legA),
                                "armed": legA[0]["arena"]["armed"]}
                c["TA-X-11"]["holds"] = c["TA-X-11"]["clamps_player"] == 0 and c["TA-X-11"]["clamps_body"] == 0
            # ---- TA-X-12 / 13 / 14 / 22 / 24
            tags = Counter()
            types = Counter()
            crit = Counter()
            for w in legA:
                tags.update(w["events"]["tags"])
                types.update(w["events"]["types"])
                crit.update(w["events"]["crit_by_source_class"])
            c["TA-X-12"] = {"pool_tags": {k: v for k, v in tags.items() if "pool" in k.lower()},
                            "holds": not any("pool" in k.lower() for k in tags)}
            c["TA-X-13"] = {"crit_by_source_class": dict(crit), "holds": crit.get("player", 0) == 0 and crit.get("player_summon", 0) == 0}
            kinds = Counter()
            for w in legA:
                kinds.update(w["release_kinds"])
            c["TA-X-14"] = {"release_kinds": dict(kinds), "energy_dryout_events": types.get("energy_dryout", 0),
                            "holds": set(kinds) <= {"None", "TYPE_A_TARGET_CYCLE", "TYPE_B_CAST_LINKED"}
                            and types.get("energy_dryout", 0) == 0}
            ia = sorted({x for w in legA for x in w["interrupts_fold_active"]})
            c["TA-X-22"] = {"interrupts_fold_active_values": ia, "holds": True not in ia}
            pm = sorted({w["kw"]["phase_model"] for w in legA})
            c["TA-X-24"] = {"phase_model": pm, "holds": pm == ["PhaseModel.ENGAGE"]}
            # ---- TA-X-25 (spawn partition at the fight grain, the RUN's loader)
            recs = Counter(x[1] for w in legA for x in w["actors"])
            not_pool = [r for r in recs if r.lower() not in pool]
            cls = {r: ("measured_offense" if cs_spawned.get(r) else ("nodata_inert" if cs_spawned.get(r) is None
                                                                     else "measured_inert")) for r in recs}
            c["TA-X-25"] = {"n_bodies": sum(recs.values()), "n_records": len(recs), "not_in_POOL-466": not_pool,
                            "classes": dict(Counter(cls[r] for r in recs.elements())),
                            "nonswing_spawned": [r for r in recs if r.lower() in nonswing],
                            "holds": not not_pool and all(v == "measured_offense" for v in cls.values())}
            # ---- TA-X-27(c): live draw sites in leg-A waves
            st = H[a]["streams"][str(s)]
            sites = Counter()
            for lab, wd in st.items():
                n = sum(v[0] for wk, v in wd.items() if wk != "None" and int(wk) <= Tw)
                if n:
                    sites[lab.split("|")[0]] += n
            c["TA-X-27c"] = {"live_sites": sorted(sites), "n_live_sites": len(sites)}
            # ---- TA-X-30
            P = Counter()
            for w in legA:
                for k, v in w["pursuit"]["steps"].items():
                    P[k] += v
            c["TA-X-30"] = {"steps": dict(P),
                            "halted_beyond_2.4_literal": sum(w["pursuit"]["halted_beyond_2.4_literal"] for w in legA),
                            "halted_beyond_2.4_literal_max_m": max(w["pursuit"]["halted_beyond_2.4_literal_max_m"] for w in legA),
                            "halted_with_operand_not_2.4": sum(w["pursuit"]["halted_with_operand_not_2.4"] for w in legA),
                            "pet_steps_aimed_at_reposition_target": sum(w["pursuit"]["pet_steps_aimed_at_reposition_target"] for w in legA),
                            "arena_clamp_stops_beyond_step_operand (R-G4)": sum(w["pursuit"]["arena_clamp_stops_beyond_step_operand (R-G4)"] for w in legA),
                            "arena_clamp_stops_beyond_2.4_literal": sum(w["pursuit"]["arena_clamp_stops_beyond_2.4_literal"] for w in legA),
                            "ledger_d_engage_m": sorted({w["ledger"]["d_engage_m"] for w in legA})}
            c["TA-X-30"]["(a) every body halts at 2.4"] = (P.get("op=other", 0) == 0 and P.get("op=0", 0) == 0)
            c["TA-X-30"]["(b) literal: halted beyond 2.4 == 0"] = c["TA-X-30"]["halted_beyond_2.4_literal"] == 0
            # ---- regime facts (law (b)) and residuals
            c["regime"] = {"wave_s": {str(w["wave"]): round((w["tick_end"] - w["tick_start"]) * H[a]["period"], 3) for w in legA},
                           "pets_spawned_per_wave": {str(w["wave"]): len(w["pets"]) for w in legA},
                           "pet_records": sorted({p[1].rsplit("/", 1)[-1].replace(".dbr", "") for w in legA for p in w["pets"]}),
                           "t_into_terminal_s": (round((legA[-1]["tick_end"] - legA[-1]["tick_start"]) * H[a]["period"], 3))}
            # ---- digest subject for TA-X-01/03/04/05 (the oracle's OWN outputs; hook-on-fold data excluded)
            subj = {"waves": [{k: w[k] for k in ("wave", "tick_start", "tick_end", "outcome", "termination_reason", "died",
                                                 "actors", "pets", "anchors", "ticks", "census", "incumbent_picks")}
                              | {"ledger": w["ledger"]["sha256"], "events": w["events"]["rows_sha256"],
                                 "lineup": w["lineup"]["fought_records"]} for w in legA],
                    "streams": {lab: {wk: v for wk, v in wd.items() if wk != "None" and int(wk) <= Tw} for lab, wd in st.items()}}
            c["digest"] = sha(canon(subj))
            c["digest_full_ladder"] = sha(canon({"t": [{k: w[k] for k in ("wave", "tick_start", "tick_end", "outcome", "actors", "ticks", "census")}
                                                       | {"ledger": w["ledger"]["sha256"], "events": w["events"]["rows_sha256"]} for w in t["waves"]],
                                                 "streams": st}))
            cells[f"{a}|{s}"] = c
    R["cells"] = cells

    def rel(x, y, ident):
        same = [cells[f"{x}|{s}"]["digest"] == cells[f"{y}|{s}"]["digest"] for s in SALTS]
        return {"compares": f"{x} vs {y}", "identical_per_salt": same, "holds": all(same) if ident else not all(same)}
    rows = {}
    rows["TA-X-01"] = {"basis": "MEASURED", "holds": R["inertness"]["TA-X-01 repeat (M0 salt 2, run twice): byte-identical trace + streams + rows"],
                       "detail": "M0 salt 2 run twice: trace, streams, capture rows byte-identical; plus single == batch on 25/25"}
    rows["TA-X-03"] = {"basis": "MEASURED", **rel("M-POL-2-NULL", "M0", True)}
    rows["TA-X-04"] = {"basis": "MEASURED", **rel("W1-NULL", "M-POL-2", True)}
    rows["TA-X-05"] = {"basis": "MEASURED", **rel("M-POL-2", "M0", False)}
    rows["TA-X-06 (printed, not graded)"] = rel("W1", "M-POL-2", False)
    allc = [cells[f"{a}|{s}"] for a in ARMS for s in SALTS]
    for rid, key in (("TA-X-08", "TA-X-08"), ("TA-X-12", "TA-X-12"), ("TA-X-13", "TA-X-13"), ("TA-X-14", "TA-X-14"),
                     ("TA-X-15(a)", "TA-X-15a"), ("TA-X-16", "TA-X-16"), ("TA-X-17", "TA-X-17"), ("TA-X-22", "TA-X-22"),
                     ("TA-X-24", "TA-X-24"), ("TA-X-25", "TA-X-25")):
        rows[rid] = {"basis": "MEASURED", "holds": all(c[key]["holds"] for c in allc),
                     "n_pass": sum(1 for c in allc if c[key]["holds"])}
    rows["TA-X-10"] = {"basis": "MEASURED", "holds": all(cells[f"W1|{s}"]["TA-X-10"]["holds"] for s in SALTS),
                       "bound": bound10, "max_body": max(cells[f"W1|{s}"]["TA-X-10"]["max_body_radius_m"] for s in SALTS),
                       "max_spawn": max(cells[f"W1|{s}"]["TA-X-10"]["max_spawn_radius_m"] for s in SALTS)}
    rows["TA-X-11"] = {"basis": "MEASURED", "holds": all(cells[f"{a}|{s}"]["TA-X-11"]["holds"] for a in ("W1", "W1-NULL") for s in SALTS),
                       "per_cell": {f"{a}|{s}": [cells[f"{a}|{s}"]["TA-X-11"]["clamps_player"], cells[f"{a}|{s}"]["TA-X-11"]["clamps_body"]]
                                    for a in ("W1", "W1-NULL") for s in SALTS}}
    rows["TA-X-30"] = {"basis": "MEASURED",
                       "(a) holds on cells": sum(1 for c in allc if c["TA-X-30"]["(a) every body halts at 2.4"]),
                       "(b) literal holds on cells": sum(1 for c in allc if c["TA-X-30"]["(b) literal: halted beyond 2.4 == 0"]),
                       "(b) R-G4 arena-clamp reading holds on cells": sum(1 for c in allc if c["TA-X-30"]["arena_clamp_stops_beyond_step_operand (R-G4)"] == 0),
                       "holds": all(c["TA-X-30"]["(a) every body halts at 2.4"] and c["TA-X-30"]["(b) literal: halted beyond 2.4 == 0"] for c in allc)}
    # ---- TA-X-27(c) at the REGISTRY's grain (rng_contract V9 SITE rows + v3.11 rg1 DRAW rows): every draw CALL SITE the
    #      oracle exercised on the 25 cells (leg A), mapped to its registry row and VERIFIED against the v3.11 source line
    rc = json.loads((MODEL / "model/rng_contract.json").read_text())
    v9 = {r["id"]: r["value"] for r in rc["⚑ v3p2_rows"]["v9_draw_site_registry"] if r["id"].startswith("V9-SITE")}
    rg1 = {r["id"]: r["value"] for r in rc["⚑ v3p11_rows"]["rg1_fold_draw_sites"]}
    rg1_draw = {k: v for k, v in rg1.items() if v.get("kind") == "DRAW"}
    REG = {"alert.py:evaluate:703": "V9-SITE-08", "channel_policy.py:_bernoulli:404": "V9-SITE-13",
           "control_application.py:apply:898": "V9-SITE-05", "counterplay.py:absorb:755": "V9-SITE-06",
           "kinematics.py:_draw_heading:362": "V9-SITE-09", "player_kit_residual.py:_roll:353": "V9-SITE-07",
           "spawn_structure.py:offset:311": "V9-SITE-14", "spawn_structure.py:offset:312": "V9-SITE-15",
           "spawn_structure.py:facing_rad:345": "V9-SITE-16", "summon_offense.py:swing:869": "V9-SITE-17",
           "threat.py:resolve_attack:1874": "V9-SITE-02", "threat.py:resolve_attack:2024": "V9-SITE-03",
           "wave_engine.py:_emit:892": "V9-SITE-23", "wave_engine.py:_folded_emit:949": "V9-SITE-24",
           "wave_engine.py:_folded_emit:958": "V9-SITE-25", "wave_engine.py:_folded_emit:960": "V9-SITE-26",
           "wave_engine.py:_weighted_pick:983": "V9-SITE-29",
           "gd_engagement.py:_choose:130": "V311-RG-005", "gd_reposition.py:_roll:248": "V311-RG-007",
           "gd_reposition.py:_roam:372": "V311-RG-008", "gd_reposition.py:_repath_random:426": "V311-RG-009",
           "gd_reposition.py:_repath_random:427": "V311-RG-010", "pilot_move.py:_next:124": "V311-RG-012",
           "referent_lineup.py:roll:232": "V311-RG-014", "referent_lineup.py:roll:248": "V311-RG-015",
           "referent_lineup.py:roll:254": "V311-RG-016", "referent_lineup.py:roll:257": "V311-RG-017",
           "referent_lineup.py:roll:258": "V311-RG-018", "swing_pause.py:pause_ticks:90": "V311-RG-003"}
    KC2 = Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2")
    exercised = Counter()
    for a in ARMS:
        for s in SALTS:
            Tw = 160 if comp[f"{a}|{s}"]["terminal"] == "cleared_w160" else comp[f"{a}|{s}"]["terminal"]
            for site, wd in H[a]["draw_callsites"][str(s)].items():
                n = sum(v for wk, v in wd.items() if wk != "None" and int(wk) <= Tw)
                if n:
                    exercised[site] += n
    ver = {}
    for site in sorted(exercised):
        rid = REG.get(site)
        fn, func, ln = site.split(":")
        src = (KC2 / fn).read_text().splitlines()[int(ln) - 1].strip()
        if rid is None:
            ver[site] = {"registry": None, "ok": False, "src": src}
            continue
        if rid.startswith("V9"):
            reg_site = v9[rid]["site"]
            same_line = reg_site == f"{fn}:{ln}"
            par = v9[rid].get("parameters", "")
            expr = par.split(" vs ")[0].split(" -> ")[0].strip()
            ok = same_line or (expr.split("(")[0] in src)
            ver[site] = {"registry": rid, "registry_site": reg_site, "line_moved": not same_line, "ok": ok, "src": src,
                         "consuming_rule": v9[rid].get("consuming_rule")}
        else:
            v = rg1[rid]
            ok = v["module"].endswith(fn.replace(".py", "")) and int(v["line"]) == int(ln) and v["kind"] == "DRAW"
            ver[site] = {"registry": rid, "registry_site": f"{v['module']}:{v['line']}", "ok": ok, "src": src,
                         "call": v["call"]}
    ex_v9 = sorted({v["registry"] for v in ver.values() if v["registry"] and v["registry"].startswith("V9")})
    ex_rg = sorted({v["registry"] for v in ver.values() if v["registry"] and v["registry"].startswith("V311")})
    lu_unk_only = [k for k, v in rg1_draw.items() if "cands" in v.get("call", "") and k == "V311-RG-019"]
    rows["TA-X-27(c) registry"] = {
        "basis": "MEASURED + pack",
        "registry_v9_site_rows": len(v9), "registry_rg1_draw_rows": len(rg1_draw),
        "rg1_draw_rows_not_live_in_V311-FULL (LU-UNK sensitivity only)": lu_unk_only,
        "registered_live_sites_v1.14 (V9 + rg1 live)": len(v9) + len(rg1_draw) - len(lu_unk_only),
        "exercised_call_sites": len(exercised), "exercised_V9": ex_v9, "exercised_rg1": ex_rg,
        "V9_not_exercised_at_v3.11": sorted(set(v9) - set(ex_v9)),
        "rg1_draw_not_exercised": sorted(set(rg1_draw) - set(ex_rg)),
        "every_exercised_site_registered_and_verified": all(v["ok"] for v in ver.values()),
        "per_site": {k: {**ver[k], "draws_leg_A_25_cells": exercised[k]} for k in sorted(exercised)},
        "p05_emergence draws": sum(n for k, n in exercised.items() if k.startswith("p05_emergence"))}
    rows["TA-X-29(c)"] = {"basis": "MEASURED (oracle fold_at) vs pack z3",
                          "per_wave": D["TA-X-29c"],
                          "holds": all(v[1] is not None and abs(v[0] - v[1]) <= 1e-9 for v in D["TA-X-29c"].values())}
    sites_all = sorted({x for c in allc for x in c["TA-X-27c"]["live_sites"]})
    rows["TA-X-27(c) live sites"] = {"basis": "MEASURED", "n": len(sites_all), "sites": sites_all,
                                     "per_cell_n": sorted({c["TA-X-27c"]["n_live_sites"] for c in allc})}
    R["law_a"] = rows

    # honest n: distinct realisations
    R["distinct_realisations"] = len({c["digest"] for c in allc})
    R["terminals"] = {a: [cells[f"{a}|{s}"]["terminal"] for s in SALTS] for a in ARMS}
    R["t_into_terminal_s"] = {a: [cells[f"{a}|{s}"]["regime"]["t_into_terminal_s"] for s in SALTS] for a in ARMS}
    gw = [float(v) for a in ARMS for s in SALTS for w, v in cells[f"{a}|{s}"]["regime"]["wave_s"].items() if int(w) <= 159]
    R["residuals"] = {"mean_wave_s_151_159 (all 25 cells)": round(sum(gw) / len(gw), 3),
                      "n_cells_clearing_w160": sum(1 for c in allc if c["terminal"] == "cleared_w160"),
                      "pets_per_cell_mean": round(sum(sum(c["regime"]["pets_spawned_per_wave"].values()) for c in allc) / 25, 2),
                      "pet_records_union": sorted({p for c in allc for p in c["regime"]["pet_records"]})}
    (HERE / "results_v1p14.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str, ensure_ascii=False) + "\n")
    print("COMPLETENESS", R["completeness"]["counts"], "STOP", stop)
    print("INERTNESS", {k: v for k, v in R["inertness"].items() if k != "per_cell"})
    for k, v in rows.items():
        print(" ", k, json.dumps({kk: vv for kk, vv in v.items() if kk not in ("per_cell", "sites")}, default=str)[:300])
    print("terminals", R["terminals"]); print("t_into_terminal", R["t_into_terminal_s"])
    print("distinct realisations", R["distinct_realisations"]); print("residuals", R["residuals"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
