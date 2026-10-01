#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.13 DRAFT · THE ORACLE CHECKS (gamora, 2026-10-01). DRAFT INSTRUMENT, NOT A PREREG.

Checks, on the ORACLE'S OWN 25 reference realisations (5 arms x 5 salts, leg A), that:
  1. the per-wave V11-P06-1 vector is what `waves.json` says (derived here by script, 54/47 as the checksum), and
     equals both the pack's `V11-P06-1` row and the oracle's own `pools_for(w, bonus_spawns_enabled=False)`;
  2. TA-X-16 RESTATED (per wave played) passes 25/25, and v1.12's text (`n_pool_picks == 47`) fails as KP-177 found;
  3. TA-X-08 identity 1 passes 25/25; identity 2 AS WRITTEN fails on the cells KP-180 names; identity 2 RESTATED with
     the seal's own control term passes 25/25, with `n_released` on the population the draft declares;
  4. the census convention (lethal tick censused alive; one PRE_FIGHT per wave played) holds on all 25;
  5. the once-per-version law (a) audit: every EXACT row that an oracle outcome can be measured for is measured here
     on the 25 traces; the rest are cited (structural / no-run) with their basis.

Inputs (all read-only):
  * the 25 filed oracle traces, godot b4c1ff3 `evidence/kc2-play/2026-10-01-g3-25cell-kp177/` (MANIFEST 78bbcc8d...),
    read through `git show` and each checked against the MANIFEST (gz sha and uncompressed sha);
  * the 25 hook records of `oracle_channel_hook.py` (gzipped beside this file, `oracle_hook/`), each from a re-run of
    the UNCHANGED oracle tool whose trace was byte-identical to the filed one (`oracle_hook/rerun_trace_sha256.json`);
  * the model pack's `waves.json`, `rng_contract.json`, `arena.json` (hashed against the pack manifest).

No expected value in here is taken from port output. jack-ryan's KP-180 shortfall table is carried as a CROSS-REFERENCE
(printed beside the measurement), never as an expected value.

Run:  python3 check_v1p13_draft.py [--ingest <scratch dir with *.hook.json and re-run *.json traces>]
      -> prints a report; writes results.json beside itself; exit 0 iff every check holds.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

HOME = Path.home() / "Games"
ENGINE = HOME / "reincarnated-engine"
GODOT = HOME / "reincarnated-godot"
MODEL = ENGINE / "src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
HERE = Path(__file__).resolve().parent
HOOKDIR = HERE / "oracle_hook"
G3REV = "b4c1ff3"
G3DIR = "evidence/kc2-play/2026-10-01-g3-25cell-kp177"
G3_MANIFEST_PIN = "78bbcc8dbf39eb30fc8e89b35a7a80b8375394a4ddbe64d39a65b4984d351fcb"   # charter KP-179 / KP-180
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
WAVES = list(range(151, 161))
W1_RADIUS_BOUND = 43.758085029822276       # TA-X-10, v1.12 § F.2 (carried)
EXTENTS = 8.0                              # TA-X-17, v1.12 § F.2 (carried)
# CROSS-REFERENCE ONLY (jack-ryan, ea0317306, WARN-1 table): (n_channelling + n_released) - D per cell, as he measured
JR_KP180_SHORT = {"M0": [-3, 0, -5, -1, -5], "M-POL-2-NULL": [-3, 0, -5, -1, -5], "M-POL-2": [-4, -2, -2, 0, -1],
                  "W1-NULL": [-4, -2, -2, 0, -1], "W1": [0, -2, -2, 0, -2]}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def gshow(path: str) -> bytes:
    return subprocess.run(["git", "-C", str(GODOT), "show", f"{G3REV}:{path}"], check=True,
                          capture_output=True).stdout


def ingest(scratch: Path) -> None:
    """Copy the 25 hook records in (gzipped, mtime 0 so the bytes are reproducible) and hash the re-run traces."""
    HOOKDIR.mkdir(exist_ok=True)
    rr = {}
    for a in ARMS:
        for s in SALTS:
            raw = (scratch / f"{a}_s{s}.hook.json").read_bytes()
            (HOOKDIR / f"{a}_s{s}.hook.json.gz").write_bytes(gzip.compress(raw, mtime=0))
            rr[f"{a}_s{s}"] = sha((scratch / f"{a}_s{s}.json").read_bytes())
    (HOOKDIR / "rerun_trace_sha256.json").write_text(json.dumps(rr, indent=1, sort_keys=True) + "\n")


# =========================================================================================== 1 · V11-P06-1 by script
def derive_vector() -> dict:
    pman = json.loads((MODEL / "manifest.json").read_text())
    want = {m["path"]: m["sha256"] for m in pman["members"]}
    for f in ("model/waves.json", "model/rng_contract.json", "model/arena.json"):
        assert sha((MODEL / f).read_bytes()) == want[f], f
    ws = json.loads((MODEL / "model/waves.json").read_text())["pools"]["wave_spawn"]
    pts_all = {w: sorted({r["spawn_point"] for r in ws if r["global_wave"] == w}) for w in WAVES}
    vec_off = [len([p for p in pts_all[w] if p != 6]) for w in WAVES]          # LAW: distinct points, p06 dropped
    vec_on = [len(pts_all[w]) for w in WAVES]
    p06_key = [int(6 in pts_all[w]) for w in WAVES]                             # key grain: one (w, 6) key or none
    p06_rows = [sum(1 for r in ws if r["global_wave"] == w and r["spawn_point"] == 6) for w in WAVES]   # row grain
    rc = json.loads((MODEL / "model/rng_contract.json").read_text())
    row = [r for r in rc["⚑ v3p2_rows"]["v11_release_schedule_and_scatter"] if r["id"] == "V11-P06-1"][0]
    # the oracle's own filter, called directly (read-only)
    sys.path.insert(0, str(ENGINE / "src"))
    cwd = os.getcwd()
    os.chdir(ENGINE)
    try:
        from reincarnated.simulation.kc2 import wave_engine as we
        oracle_off = [sorted(we.pools_for(w, bonus_spawns_enabled=False)) for w in WAVES]
        oracle_on = [sorted(we.pools_for(w, bonus_spawns_enabled=True)) for w in WAVES]
    finally:
        os.chdir(cwd)
    out = {"law": "V11-P06-1[w] = |{spawn_point of model/waves.json pools.wave_spawn rows with global_wave == w} \\ {6}|,"
                  " w = 151..160",
           "vector_p06_off": vec_off, "sum_off": sum(vec_off), "vector_p06_on": vec_on, "sum_on": sum(vec_on),
           "p06_key_per_wave": p06_key, "p06_rows_per_wave": p06_rows,
           "pack_row_V11-P06-1": row["value"],
           "oracle_pools_for_off_keys": oracle_off, "oracle_pools_for_on_keys": oracle_on}
    out["checks"] = {
        "checksum 47/54": (sum(vec_off), sum(vec_on)) == (47, 54),
        "p06 keys = 54 - 47 = 7": sum(p06_key) == 7,
        "equals the pack's V11-P06-1 row": vec_off == row["value"]["active_points_per_wave_151_160"],
        "equals the oracle's pools_for(w, False) key counts": vec_off == [len(k) for k in oracle_off],
        "oracle pools_for(w, True) key counts = vector_on": vec_on == [len(k) for k in oracle_on],
        "oracle's filter drops exactly key 6": all(sorted(set(b) - set(a)) == ([6] if p else [])
                                                  for a, b, p in zip(oracle_off, oracle_on, p06_key)),
        "data keys == oracle keys (on)": [pts_all[w] for w in WAVES] == oracle_on,
    }
    return out


# =========================================================================================== 2 · load the 25 cells
def load_cells() -> dict:
    man_b = gshow(f"{G3DIR}/MANIFEST.json")
    assert sha(man_b) == G3_MANIFEST_PIN, "G3 MANIFEST pin"
    man = json.loads(man_b)
    rr = json.loads((HOOKDIR / "rerun_trace_sha256.json").read_text())
    cells = {}
    for a in ARMS:
        for s in SALTS:
            key = f"{a}_s{s}"
            gzb = gshow(f"{G3DIR}/oracle_traces/{key}.json.gz")
            ent = man["files"][f"oracle_traces/{key}.json.gz"]
            raw = gzip.decompress(gzb)
            assert sha(gzb) == ent["sha256"] and sha(raw) == ent["uncompressed_sha256"], key
            hook = json.loads(gzip.decompress((HOOKDIR / f"{key}.hook.json.gz").read_bytes()))
            assert hook["arm"] == a and hook["salt"] == s
            cells[key] = {"arm": a, "salt": s, "trace": json.loads(raw), "hook": hook,
                          "rerun_identical": rr[key] == ent["uncompressed_sha256"],
                          "g3_cell": man["cells"][key]}
    return cells


def leg_a(tr: dict) -> list:
    L = tr["leg_a"]["wave"]
    played = [w for w in tr["waves"] if w["wave"] <= L]
    assert [w["wave"] for w in played] == list(range(151, L + 1))
    return played


# =========================================================================================== 3 · per-cell evaluation
def eval_cell(c: dict, vec: dict, anchors: dict) -> dict:
    tr, hook = c["trace"], c["hook"]
    played = leg_a(tr)
    L = tr["leg_a"]["wave"]
    r = {"terminal_wave": L, "waves_played": len(played)}

    # ---- census convention + identity 1 (oracle's own classifier, actor_state._player_rows, per wave)
    cen = Counter()
    pf_per_wave, lethal_alive = [], None
    for w in played:
        cp = w["census_player"]
        assert "error" not in cp, cp
        cen.update(cp)
        pf_per_wave.append(cp.get("PRE_FIGHT", 0))
        assert sum(cp.values()) == len(w["ticks"]), (w["wave"], "census covers every observed tick")
    last = played[-1]
    lethal_alive = (last["died"] and last["ticks"][-1]["hp"] <= 0.0 and "DEAD" not in last["census_player"]
                    and sum(last["census_player"].values()) == len(last["ticks"]))
    observed = sum(len(w["ticks"]) for w in played)
    PF = cen.get("PRE_FIGHT", 0)
    D = cen["CHANNELLING"] + cen["CHANNELLING_AND_MOVING"] + cen["MOVING"] + cen["IDLE"]
    n_chan = cen["CHANNELLING"] + cen["CHANNELLING_AND_MOVING"]
    r["census"] = dict(cen)
    r["census_convention"] = {"one PRE_FIGHT per wave played": pf_per_wave == [1] * len(played),
                              "no DEAD state": "DEAD" not in cen,
                              "lethal tick censused alive (hp<=0, inside the census, not DEAD)": lethal_alive,
                              "D equals G3 D_oracle": D == c["g3_cell"]["census"]["D_oracle"],
                              "PF equals G3 PRE_FIGHT_oracle": PF == c["g3_cell"]["census"]["PRE_FIGHT_oracle"]}
    r["identity_1"] = {"observed": observed, "D": D, "PRE_FIGHT": PF, "holds": observed == D + PF}

    # ---- the channel fold, per tick, aligned to the trace (D ticks = every tick but each wave's first)
    n_rel_D = n_rel_PF = n_cs_chan_D = n_cs_rel_D = n_cs_PF = 0
    chan_D_trace = 0
    align_ok, verdict_consistent, seq_ok = True, True, True
    fold_seen = False
    ctrl_channel_entries = 0
    for w in played:
        ticks = w["ticks"]
        rts = [t["rt"] for t in ticks]
        ctrl_channel_entries += sum(1 for e in w["control"] if e[2])
        bucket = [b for b in hook["waves"] if b["wave"] == w["wave"] and b["obs"]
                  and [o[0] for o in b["obs"]] == rts]
        if c["arm"] == "M0":
            assert not any(b["obs"] for b in hook["waves"]), "M0 has no channel fold"
            obs = [[t["rt"], (not t["chan"]), False, False, True] for t in ticks]   # no fold: cc <=> not chan
        else:
            if len(bucket) != 1:
                align_ok = False
                continue
            obs = bucket[0]["obs"]
            fold_seen = True
        for i, (o, t) in enumerate(zip(obs, ticks)):
            _rt, cc, v, ret, sq = o
            seq_ok &= bool(sq)
            if c["arm"] != "M0":
                verdict_consistent &= (ret == ((not cc) and v)) and (t["chan"] == ((not cc) and (not v)))
            is_pf = (i == 0)
            if is_pf:
                n_rel_PF += int(v)
                n_cs_PF += int(cc)
                continue
            chan_D_trace += int(t["chan"])
            n_rel_D += int(v)
            n_cs_chan_D += int(cc and not v)
            n_cs_rel_D += int(cc and v)
    fold_counter = None
    if fold_seen:
        lastb = [b for b in hook["waves"] if b["wave"] == L and b["obs"]][-1]
        fold_counter = lastb["fold_report"]
    r["fold"] = {"aligned_every_wave": align_ok, "observe_verdict_consistent_with_trace": verdict_consistent,
                 "no_desync": seq_ok, "n_released_on_D": n_rel_D, "n_released_on_PRE_FIGHT": n_rel_PF,
                 "n_released_on_observed": n_rel_D + n_rel_PF,
                 "n_control_suppressed_channelling_on_D": n_cs_chan_D,
                 "n_control_suppressed_released_on_D": n_cs_rel_D, "n_control_suppressed_on_PRE_FIGHT": n_cs_PF,
                 "trace_control_channel_entries_leg_A": ctrl_channel_entries,
                 "fold_n_ticks_released_counter_at_terminal": None if fold_counter is None else fold_counter["n_ticks_released"],
                 "fold_n_observe_at_terminal": None if fold_counter is None else fold_counter["n_observe"]}
    if fold_counter is not None:
        r["fold"]["counter_equals_released_on_observed"] = fold_counter["n_ticks_released"] == n_rel_D + n_rel_PF
        r["fold"]["n_observe_equals_observed"] = fold_counter["n_observe"] == observed
    r["census_chan_equals_trace_chan_on_D"] = n_chan == chan_D_trace

    short = n_chan + n_rel_D - D
    r["identity_2_v1.12"] = {"n_channelling": n_chan, "n_released": n_rel_D, "D": D, "lhs_minus_D": short,
                             "holds": short == 0,
                             "jack_ryan_KP180_cross_reference": JR_KP180_SHORT[c["arm"]][c["salt"]]}
    r["identity_2_restated"] = {
        "n_channelling": n_chan, "n_released (D population)": n_rel_D,
        "n_control_suppressed_channelling (D population)": n_cs_chan_D, "D": D,
        "holds": n_chan + n_rel_D + n_cs_chan_D == D,
        "rival population (n_released on ALL observed ticks) would hold":
            n_chan + n_rel_D + n_rel_PF + n_cs_chan_D == D}

    # ---- TA-X-16 restated, at KEY grain (the board's roll), with the actor grain as a cross-check
    v = dict(zip(WAVES, vec["vector_p06_off"]))
    fk = dict(zip(WAVES, vec["p06_key_per_wave"]))
    per_wave = []
    ok16 = True
    for w in played:
        wv = w["wave"]
        calls = [pc for b in hook["waves"] for pc in b.get("pools_for", []) if pc[0] == "roll_wave" and pc[1] == wv]
        keysets = {tuple(pc[3]) for pc in calls}
        allsets = {tuple(pc[4]) for pc in calls}
        flags = {pc[2] for pc in calls}
        assert calls and len(keysets) == 1 and len(allsets) == 1, (wv, keysets)
        keys, allk = list(keysets.pop()), list(allsets.pop())
        filtered = sorted(set(allk) - set(keys))
        actor_pts = sorted({a[6] for a in w["actors"]})
        row = {"wave": wv, "picks": len(keys), "expected": v[wv], "p06_key_rolled": int(6 in keys),
               "filtered_keys": len(filtered), "filtered_expected": fk[wv], "filtered_are_p06_only": set(filtered) <= {6},
               "bonus_spawns_enabled_passed": sorted(flags), "actor_points": actor_pts,
               "actor_grain_equals_picks": len(actor_pts) == len(keys) and "p06" not in actor_pts}
        row["holds"] = (row["picks"] == row["expected"] and row["p06_key_rolled"] == 0
                        and row["filtered_keys"] == row["filtered_expected"] and row["filtered_are_p06_only"])
        ok16 &= row["holds"]
        per_wave.append(row)
    n_pool_picks = sum(x["picks"] for x in per_wave)
    r["TA-X-16_restated"] = {"per_wave": per_wave, "n_pool_picks": n_pool_picks,
                             "expected_sum": sum(v[w["wave"]] for w in played),
                             "n_spawn_point_6_keys_rolled": sum(x["p06_key_rolled"] for x in per_wave),
                             "n_p06_keys_filtered": sum(x["filtered_keys"] for x in per_wave),
                             "n_p06_keys_filtered_expected": sum(fk[w["wave"]] for w in played)}
    r["TA-X-16_restated"]["holds"] = (ok16 and n_pool_picks == r["TA-X-16_restated"]["expected_sum"]
                                      and r["TA-X-16_restated"]["n_spawn_point_6_keys_rolled"] == 0)
    r["TA-X-16_v1.12_text"] = {"n_pool_picks": n_pool_picks, "holds": n_pool_picks == 47}

    # ---- the other measurable rows (law (a))
    tags = Counter(e[6] for w in played for e in w["events"])
    r["TA-X-12"] = {"pool_tags": {t: n for t, n in tags.items() if t and "pool" in str(t).lower()},
                    "holds": not any(t and "pool" in str(t).lower() for t in tags)}
    t15 = True
    for w in played:
        for a in w["actors"]:
            p, t = a[6], a[5]
            if p in ("p01", "p02", "p03", "p04") and t != 0.0:
                t15 = False
            if p == "p05" and t != 4.0:
                t15 = False
    r["TA-X-15a"] = {"holds": t15, "p05_tick": 4.0 / tr["period"]}
    worst17 = max(math.hypot(a[2] - anchors[a[6]][0], a[3] - anchors[a[6]][1]) for w in played for a in w["actors"])
    r["TA-X-17"] = {"max_offset_m": worst17, "holds": worst17 <= EXTENTS}
    if c["arm"] == "W1":
        rb = max(math.hypot(b[1], b[2]) for w in played for t in w["ticks"] for b in t["bodies"])
        rs = max(math.hypot(a[2], a[3]) for w in played for a in w["actors"])
        r["TA-X-10"] = {"max_body_radius_m": rb, "max_spawn_radius_m": rs, "holds": max(rb, rs) <= W1_RADIUS_BOUND}
    r["TA-X-01_rerun_byte_identical"] = c["rerun_identical"]
    return r


def digestable(tr: dict) -> str:
    t = dict(tr)
    t.pop("arm")
    return sha(json.dumps(t, sort_keys=True).encode())


def main() -> int:
    if "--ingest" in sys.argv:
        ingest(Path(sys.argv[sys.argv.index("--ingest") + 1]))
    vec = derive_vector()
    arena = json.loads((MODEL / "model/arena.json").read_text())
    anchors = {p["point_id"]: (p["x"], p["y"]) for p in arena["spawn_points"]}
    cells = load_cells()
    res = {k: eval_cell(c, vec, anchors) for k, c in cells.items()}

    def count(pred):
        return sum(1 for k in res if pred(res[k]))
    n = len(res)
    summary = {
        "V11-P06-1 derived": vec["vector_p06_off"], "V11-P06-1 checks": vec["checks"],
        "TA-X-16 restated (oracle passes)": f"{count(lambda r: r['TA-X-16_restated']['holds'])}/{n}",
        "TA-X-16 v1.12 text (oracle passes)": f"{count(lambda r: r['TA-X-16_v1.12_text']['holds'])}/{n}",
        "TA-X-08 identity 1 (oracle passes)": f"{count(lambda r: r['identity_1']['holds'])}/{n}",
        "TA-X-08 identity 2 AS WRITTEN (oracle passes)": f"{count(lambda r: r['identity_2_v1.12']['holds'])}/{n}",
        "TA-X-08 identity 2 RESTATED (oracle passes)": f"{count(lambda r: r['identity_2_restated']['holds'])}/{n}",
        "identity 2 restated, rival population (all observed ticks)":
            f"{count(lambda r: r['identity_2_restated']['rival population (n_released on ALL observed ticks) would hold'])}/{n}",
        "shortfall == jack-ryan KP-180 table": f"{count(lambda r: r['identity_2_v1.12']['lhs_minus_D'] == r['identity_2_v1.12']['jack_ryan_KP180_cross_reference'])}/{n}",
        "shortfall == -(control-suppressed channelling)": f"{count(lambda r: r['identity_2_v1.12']['lhs_minus_D'] == -r['fold']['n_control_suppressed_channelling_on_D'])}/{n}",
        "census convention holds": f"{count(lambda r: all(r['census_convention'].values()))}/{n}",
        "independent: trace control `channel` entries (leg A) == n_control_suppressed_channelling":
            f"{count(lambda r: r['fold']['trace_control_channel_entries_leg_A'] == r['fold']['n_control_suppressed_channelling_on_D'])}/{n}",
        "fold counter n_ticks_released == released on observed ticks (fold arms)":
            f"{count(lambda r: r['fold'].get('counter_equals_released_on_observed', True))}/{n}",
        "fold aligned + consistent + no desync": f"{count(lambda r: r['fold']['aligned_every_wave'] and r['fold']['observe_verdict_consistent_with_trace'] and r['fold']['no_desync'])}/{n}",
        "census chan == trace chan on D": f"{count(lambda r: r['census_chan_equals_trace_chan_on_D'])}/{n}",
        "released PRE_FIGHT ticks (all cells)": sum(r["fold"]["n_released_on_PRE_FIGHT"] for r in res.values()),
        "control-suppressed PRE_FIGHT ticks (all cells)": sum(r["fold"]["n_control_suppressed_on_PRE_FIGHT"] for r in res.values()),
        "control-suppressed RELEASED ticks on D (all cells)": sum(r["fold"]["n_control_suppressed_released_on_D"] for r in res.values()),
        "cells with identity-2 shortfall": [k for k, r in res.items() if not r["identity_2_v1.12"]["holds"]],
        "distinct oracle realisations among the 25 (trace minus arm label)":
            len({digestable(c["trace"]) for c in cells.values()}),
        "W1 salts whose trace differs from M-POL-2's":
            [s for s in SALTS if digestable(cells[f"W1_s{s}"]["trace"]) != digestable(cells[f"M-POL-2_s{s}"]["trace"])],
    }
    # law (a) over arm relations, measured on the traces
    rel = {}
    for s in SALTS:
        rel[s] = {"TA-X-03 M-POL-2-NULL == M0 (trace minus arm label)":
                  digestable(cells[f"M-POL-2-NULL_s{s}"]["trace"]) == digestable(cells[f"M0_s{s}"]["trace"]),
                  "TA-X-04 W1-NULL == M-POL-2 (trace minus arm label)":
                  digestable(cells[f"W1-NULL_s{s}"]["trace"]) == digestable(cells[f"M-POL-2_s{s}"]["trace"]),
                  "TA-X-05 M-POL-2 != M0 (trace)":
                  digestable(cells[f"M-POL-2_s{s}"]["trace"]) != digestable(cells[f"M0_s{s}"]["trace"]),
                  "terminal M-POL-2 vs M0": [res[f"M-POL-2_s{s}"]["terminal_wave"], res[f"M0_s{s}"]["terminal_wave"]]}
    law_a = {
        "TA-X-01": ("MEASURED", count(lambda r: r["TA-X-01_rerun_byte_identical"]) == n,
                    f"oracle re-run byte-identical to the filed trace {count(lambda r: r['TA-X-01_rerun_byte_identical'])}/{n}"),
        "TA-X-03": ("MEASURED", all(rel[s]["TA-X-03 M-POL-2-NULL == M0 (trace minus arm label)"] for s in SALTS), "5/5 full-trace equality"),
        "TA-X-04": ("MEASURED", all(rel[s]["TA-X-04 W1-NULL == M-POL-2 (trace minus arm label)"] for s in SALTS), "5/5 full-trace equality"),
        "TA-X-05": ("MEASURED", any(rel[s]["TA-X-05 M-POL-2 != M0 (trace)"] for s in SALTS),
                    f"differ on {sum(rel[s]['TA-X-05 M-POL-2 != M0 (trace)'] for s in SALTS)}/5 salts (>= 1 required)"),
        "TA-X-08 (restated, both identities)": ("MEASURED", count(lambda r: r["identity_1"]["holds"] and r["identity_2_restated"]["holds"]) == n,
                    summary["TA-X-08 identity 2 RESTATED (oracle passes)"]),
        "TA-X-10": ("MEASURED", all(res[f"W1_s{s}"]["TA-X-10"]["holds"] for s in SALTS),
                    f"W1 max body radius {max(res[f'W1_s{s}']['TA-X-10']['max_body_radius_m'] for s in SALTS):.6f} m, max spawn radius {max(res[f'W1_s{s}']['TA-X-10']['max_spawn_radius_m'] for s in SALTS):.6f} m <= {W1_RADIUS_BOUND}"),
        "TA-X-12": ("MEASURED", count(lambda r: r["TA-X-12"]["holds"]) == n, "no damage tag containing 'pool' on any leg-A event, 25/25"),
        "TA-X-15(a)": ("MEASURED", count(lambda r: r["TA-X-15a"]["holds"]) == n, "p01-p04 at 0.0 s, p05 at 4.0 s (tick 49), every wave played, 25/25"),
        "TA-X-16 (restated)": ("MEASURED", count(lambda r: r["TA-X-16_restated"]["holds"]) == n, summary["TA-X-16 restated (oracle passes)"]),
        "TA-X-17": ("MEASURED", count(lambda r: r["TA-X-17"]["holds"]) == n,
                    f"max ‖spawn − anchor‖ = {max(r['TA-X-17']['max_offset_m'] for r in res.values()):.6f} m <= 8.0"),
    }
    results = {"vector": vec, "summary": summary, "arm_relations": rel,
               "law_a_measured": {k: {"basis": b, "passes": bool(p), "detail": d} for k, (b, p, d) in law_a.items()},
               "cells": res}
    (HERE / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True, ensure_ascii=False) + "\n")

    print("== V11-P06-1 derived from waves.json:", vec["vector_p06_off"], "sum", vec["sum_off"], "| on", vec["vector_p06_on"],
          "sum", vec["sum_on"])
    for k, v in vec["checks"].items():
        print("   ", "OK " if v else "XX ", k)
    print("   p06 key grain per wave", vec["p06_key_per_wave"], "| row grain", vec["p06_rows_per_wave"],
          "sum", sum(vec["p06_rows_per_wave"]))
    print("== per cell: terminal | D PF | chan rel cs_chan | id2-as-written | id2-restated | TA-X-16 picks/expected restated")
    for k, r in res.items():
        print(f"   {k:16s} w{r['terminal_wave']} | {r['identity_1']['D']:5d} {r['identity_1']['PRE_FIGHT']} | "
              f"{r['identity_2_restated']['n_channelling']:5d} {r['identity_2_restated']['n_released (D population)']:4d} "
              f"{r['identity_2_restated']['n_control_suppressed_channelling (D population)']:2d} | "
              f"{r['identity_2_v1.12']['lhs_minus_D']:+d} (JR {r['identity_2_v1.12']['jack_ryan_KP180_cross_reference']:+d}) | "
              f"{'GREEN' if r['identity_2_restated']['holds'] else 'RED'} | "
              f"{r['TA-X-16_restated']['n_pool_picks']}/{r['TA-X-16_restated']['expected_sum']} "
              f"{'GREEN' if r['TA-X-16_restated']['holds'] else 'RED'}")
    print("== summary")
    for k, v in summary.items():
        print("   ", k, ":", v)
    print("== law (a), measured rows")
    for k, (b, p, d) in law_a.items():
        print(f"    {k:38s} {b:9s} {'PASS' if p else 'FAIL'}  {d}")
    ok = (all(vec["checks"].values())
          and summary["TA-X-16 restated (oracle passes)"] == f"{n}/{n}"
          and summary["TA-X-08 identity 2 RESTATED (oracle passes)"] == f"{n}/{n}"
          and summary["TA-X-08 identity 1 (oracle passes)"] == f"{n}/{n}"
          and summary["census convention holds"] == f"{n}/{n}"
          and summary["fold aligned + consistent + no desync"] == f"{n}/{n}"
          and summary["independent: trace control `channel` entries (leg A) == n_control_suppressed_channelling"] == f"{n}/{n}"
          and summary["fold counter n_ticks_released == released on observed ticks (fold arms)"] == f"{n}/{n}"
          and all(p for (_b, p, _d) in law_a.values()))
    print("== ALL DRAFT CHECKS HOLD" if ok else "== A CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
