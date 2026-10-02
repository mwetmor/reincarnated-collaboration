"""KC2 lethality hunt, residual leg (legolas, 2026-10-02). NOT-A-GRADED-RUN.

Runs the v3.8 oracle of record (gamora `v3p8_oracle(Folds("V38-FULL"))`, imported unchanged) with
an EXTENDED capture (first-hit timing, landed by time bin / record / skill, w160 death anatomy,
heal events), and optional harness-only counterfactual arms installed as method patches that are
restored in `finally`. Nothing in the engine is edited; the engine tree used is a read-only
`git archive` snapshot of engine a40e609b.

usage (from <snapshot>/src):  python3 hunt2.py <arm> <n_salts|a-b> <out.json>
"""
from __future__ import annotations

import json
import math
import sys
import time
from collections import defaultdict
from contextlib import ExitStack, contextmanager
from typing import Any, Dict, Iterator, List

from reincarnated.simulation.scripts import gamora_kc2_play_v3p8_oracle_2026_10_02 as V
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11

sys.path.insert(0, __import__("os").path.dirname(__file__))
import arms as ARMS  # noqa: E402  (counterfactual registry)

BINS = (0, 3, 5, 7.5, 10, 15, 20, 30, 1e9)
#: distance-at-hit bins (m, centre to centre), monster direct hits on the player
DBINS = (0, 1.5, 2.5, 3.5, 5, 7.5, 11.5, 16, 1e9)
#: Lap H-2 range-profile bands, ground px / 122 gpx-per-m (Lap S bracket 119-125, midpoint)
HBANDS = tuple(x / 122.0 for x in (0, 100, 150, 220, 300, 400, 600, 900, 1400))

# ── INERT OBSERVER on Mover.step: per (band, moving/still) counts for live bodies within the
#    referent camera's plate range (<= 1400 gpx), the same functional as Lap H-2's range profile.
from reincarnated.simulation.kc2 import locomotion as _lo  # noqa: E402
_MOV = {"cnt": None}


def _reset_mov():
    _MOV["cnt"] = [[0, 0] for _ in range(len(HBANDS) - 1)]


_reset_mov()
_real_step = _lo.Mover.step


def _obs_step(self, dt_s, player_xy, **kw):
    r = _real_step(self, dt_s, player_xy, **kw)
    d = math.hypot(self.xy[0] - player_xy[0], self.xy[1] - player_xy[1])
    for i in range(len(HBANDS) - 1):
        if HBANDS[i] <= d < HBANDS[i + 1]:
            _MOV["cnt"][i][0 if self.last_step_travel_m > 0.0 else 1] += 1
            break
    return r


_lo.Mover.step = _obs_step


def ext_capture(r: Any, base: Any) -> Dict[str, Any]:
    out = base(r)
    w = r.waves[0]
    t0 = float(w["t_start_s"])
    A = {a["actor_id"]: a for a in r.actors}
    rows = r.rows_as_dicts()
    ev = sorted((x for x in rows if x["event_type"] in ("damage_dealt", "dot_tick")
                 and x["target_id"] == "player" and (x["damage_applied"] or 0) > 0),
                key=lambda x: x["t_s"])
    rec = lambda sid: str(A.get(sid, {}).get("record_path", sid or "?")).split("/")[-1]  # noqa: E731
    by_rec: Dict[str, float] = defaultdict(float)
    by_skill: Dict[str, float] = defaultdict(float)
    bins = [0.0] * (len(BINS) - 1)
    for x in ev:
        a = float(x["damage_applied"])
        tt = float(x["t_s"]) - t0
        by_rec[rec(x["source_id"])] += a
        by_skill[rec(x["source_id"]) + ":" + str(x["source_skill_id"] or x["damage_source_tag"]).split("/")[-1]] += a
        for i in range(len(BINS) - 1):
            if BINS[i] <= tt < BINS[i + 1]:
                bins[i] += a
                break
    first = None
    if ev:
        f = ev[0]
        d = (math.hypot(f["source_x"] - f["target_x"], f["source_y"] - f["target_y"])
             if f["source_x"] is not None and f["target_x"] is not None else None)
        first = {"t": round(float(f["t_s"]) - t0, 3), "rec": rec(f["source_id"]),
                 "skill": str(f["source_skill_id"]).split("/")[-1], "dist_m": d and round(d, 2),
                 "type": f["event_type"]}
    # first hit by a body that spawned at t0 (excludes p05 burst)
    heals = [x for x in rows if x["event_type"] == "heal_tick" and x["target_id"] == "player"]
    heal_by_src: Dict[str, float] = defaultdict(float)
    for x in heals:
        heal_by_src[str(x["source_skill_id"] or x["damage_source_tag"] or x["source_id"]).split("/")[-1]] += float(
            x["damage_applied"] or 0.0)
    spawn_t = sorted(round(float(a["spawn_t_s"]) - t0, 2) for a in r.actors)
    ext = {"first_hit": first, "landed_bins": [round(b, 1) for b in bins],
           "landed_by_record": {k: round(v, 1) for k, v in sorted(by_rec.items(), key=lambda kv: -kv[1])},
           "landed_by_skill": {k: round(v, 1) for k, v in sorted(by_skill.items(), key=lambda kv: -kv[1])[:25]},
           "heal_by_source": {k: round(v, 1) for k, v in heal_by_src.items()},
           "n_spawn_t0": sum(1 for s in spawn_t if s <= 0.01), "n_spawn": len(spawn_t),
           "roster": sorted({rec(a["actor_id"]) for a in r.actors})}
    if out.get("died"):
        td = out.get("t_death_s")
        tdr = (td - t0) if td is not None else None
        last3: Dict[str, float] = defaultdict(float)
        for x in ev:
            if tdr is not None and float(x["t_s"]) - t0 > tdr - 3.0:
                last3[rec(x["source_id"]) + ":" + str(x["source_skill_id"]).split("/")[-1]] += float(x["damage_applied"])
        ext["death_t_into_wave"] = tdr
        ext["last3s_by_skill"] = {k: round(v, 1) for k, v in sorted(last3.items(), key=lambda kv: -kv[1])[:10]}
        ext["heal_landed_wave"] = sum(float(x["damage_applied"] or 0) for x in heals)
    for k in ("disc_census", "player_sustain"):
        v = w.get(k)
        if isinstance(v, dict):
            ext[k] = {kk: vv for kk, vv in v.items() if isinstance(vv, (int, float, str, bool)) or vv is None}
    dh = [0.0] * (len(DBINS) - 1)
    for x in ev:
        if x["event_type"] != "damage_dealt" or x["source_x"] is None or x["target_x"] is None:
            continue
        if "_pet" in str(x["source_id"]):
            continue
        d = math.hypot(x["source_x"] - x["target_x"], x["source_y"] - x["target_y"])
        for i in range(len(DBINS) - 1):
            if DBINS[i] <= d < DBINS[i + 1]:
                dh[i] += float(x["damage_applied"])
                break
    ext["landed_by_hit_distance"] = [round(v, 1) for v in dh]
    ext["mover_band_moving_still"] = _MOV["cnt"]
    _reset_mov()
    out["ext"] = ext
    return out


def run(arm: str, salts: tuple) -> Dict[str, Any]:
    cfg, patches = ARMS.get(arm)
    base = c11._capture
    real_base = V._base_cap
    V._base_cap = lambda r: ext_capture(r, real_base)
    try:
        with ExitStack() as es:
            for p in patches:
                es.enter_context(p())
            res = V.run_one(cfg, salts, V.FP._period())
    finally:
        V._base_cap = real_base
        c11._capture = base
    return res


def main() -> None:
    arm, ns, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    salts = tuple(range(int(ns))) if "-" not in ns else tuple(range(int(ns.split("-")[0]), int(ns.split("-")[1]) + 1))
    t0 = time.time()
    res = run(arm, salts)
    summ = V.summarise(res, salts)
    out = {"artifact_class": "NOT-A-GRADED-RUN (legolas residual hunt, KC2-PLAY). Harness-only "
                             "counterfactual; nothing tuned; engine snapshot a40e609b read-only.",
           "arm": arm, "arm_doc": ARMS.doc(arm), "salts": list(salts), "summary": summ,
           "fold_reports": res.get("fold_reports"),
           "rows": {s: res["salts"][str(s)]["rows"] for s in salts},
           "leg_a": {s: res["salts"][str(s)]["leg_a_terminal"] for s in salts},
           "wall_s": round(time.time() - t0, 1)}
    json.dump(out, open(outp, "w"), indent=None, default=str)
    print(f"{arm}: x{summ['ratio_vs_referent']} terms={summ['leg_a_terminals']} "
          f"tint={summ['leg_a_t_into_wave_s']} wall={out['wall_s']}", flush=True)


if __name__ == "__main__":
    main()
