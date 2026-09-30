"""KC2-PLAY · prereg v1.9 § F.2j · H-9 — the ORACLE's W1 containment under separation.

⚑ NOT-A-GRADED-RUN. Read-only against the oracle: no oracle file is edited, nothing is tuned.
It composes committed drivers and does not copy them:
  * `gamora_kc2_w1w2_lift_build_2026_08_25.make_runner` — the sealed M-POL-2 seat, whose
    `run_cell(arena=...)` is the W1 site;
  * `gamora_kc2_upn4_occupancy_by_pilot_2026_09_29._overrides` — the SEALED-KMILL | SEP-ON cell
    (contact_response='separate', geometry ON, seek_fold, K-MILL kinematics), as C-11 and the
    C-11a pricing ran it;
  * P-5: the loader call `load_profiles(dot_corrections=True, winner_surface=from_x8(P-n.2),
    pool_lift=load(), c11a=C11aLoader(CLASS))`, and `simulate_wave(c11a_corrections=C11aFold(
    retaliation_gate=True, duration_divisors=True, aura=loader))` — i.e. the P-n.3 PW-FOLDED cell.
  * W1: `ArenaFold(armed=True, avoidance=True)`, the W1 arm of record (w1w2 build arm_specs).

Observation-only harness patches (restored in `finally`): `Mover.displace` is wrapped to record the
maximum body radius AFTER a separation displacement. That is the board's true maximum. The W1
statistic of record (`ArenaFold.max_body_radius_m`) is read as the fold reports it.

Legs: A = stop at the player's first death (the graded semantics). B = death-continued through
waves 151–160 (a superset of the bodies A sees; a sensitivity, not the row's population).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import sys
import time
from typing import Any, Dict, List

sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src")

from reincarnated.simulation.kc2 import arena_fold as af
from reincarnated.simulation.kc2 import c11a_corrections as C
from reincarnated.simulation.kc2 import kinematics as kn
from reincarnated.simulation.kc2 import locomotion as lo
from reincarnated.simulation.kc2 import pool_lift as PL
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.kc2 import threat as th
from reincarnated.simulation.kc2 import winner_surface as WS
from reincarnated.simulation.kc2.run import PlayerPolicy
from reincarnated.simulation.scripts import gamora_kc2_upn4_occupancy_by_pilot_2026_09_29 as upn4
from reincarnated.simulation.scripts.gamora_kc2_w1w2_lift_build_2026_08_25 import make_runner

R_WALL = 43.758085029822276          # prereg v1.9 TA-X-10 (read back from arena.json below)
X8 = ("/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/"
      "kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json")
PACK = ("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
        "kc2-model-pack-v3-E-s09-cp150-mech-v3p6p1-20260930_110026/model/arena.json")


def _sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


MODE = sys.argv[2] if len(sys.argv) > 2 else "W1"


def main(out_path: str) -> None:
    ar = json.load(open(PACK))
    derived_wall = max(math.hypot(p["x"], p["y"]) for p in ar["spawn_points"]) \
        + ar["placement_extents_m"]["value"]
    assert derived_wall == R_WALL, (derived_wall, R_WALL)
    assert _sha(X8) == "cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960"

    loader = C.C11aLoader(scope=C.AuraScope.CLASS)
    extra = {"c11a": loader, "pool_lift": PL.load(),
             "winner_surface": WS.WinnerSurfaceFold.from_x8(X8)}
    real_lp = th.load_profiles
    th.load_profiles = lambda **kw: real_lp(**kw, **extra)          # type: ignore[assignment]
    try:
        runner = make_runner()
    finally:
        th.load_profiles = real_lp                                    # type: ignore[assignment]

    # the tick period READ off a control run, as the C-11a pricing reads it
    probe: List[Dict[str, Any]] = []
    with upn4._overrides(contact_response="separate", geometry_on=True, seek_fold=True,
                         policy=None, kinematics=None, death_continued=False, sink=probe):
        pr, _pt, _ = runner(salt=0, seat=False)
    period = float(pr[0].tick_period_s)

    real_sw = kr.simulate_wave
    real_disp = lo.Mover.displace
    obs: Dict[str, Any] = {}

    def disp(self: Any, dx: float, dy: float, *, tick: int, t_s: float) -> None:
        real_disp(self, dx, dy, tick=tick, t_s=t_s)
        if dx or dy:
            r = math.hypot(self.xy[0], self.xy[1])
            obs["n_disp"] = obs.get("n_disp", 0) + 1
            if r > obs.get("max_post_sep_r", 0.0):
                obs["max_post_sep_r"] = r
                obs["argmax_wave"] = obs.get("_wave")
            if r > R_WALL:
                obs["n_post_sep_beyond_wall"] = obs.get("n_post_sep_beyond_wall", 0) + 1

    def sw(*a: Any, **kw: Any) -> Any:
        w = int(a[0] if a else kw["wave"])
        obs["_wave"] = w
        kw["c11a_corrections"] = C.C11aFold(wave=w, retaliation_gate=True,
                                            duration_divisors=True, aura=loader)
        r = real_sw(*a, **kw)
        wv = r.waves[0]
        obs.setdefault("waves", []).append({"wave": w, "player_died": bool(wv.get("player_dead")
                                                                          or wv.get("player_death"))})
        return r

    result: Dict[str, Any] = {"legs": {}}
    t0 = time.time()
    kr.simulate_wave = sw                                             # type: ignore[assignment]
    lo.Mover.displace = disp                                          # type: ignore[assignment]
    try:
        for leg, cont in ((("A_stop_at_death", False), ("B_death_continued", True)) if MODE=="W1" else (("A_stop_at_death", False),)):
            per: Dict[str, Any] = {}
            for salt in (0, 1, 2, 3, 4):
                obs.clear()
                arena = {"W1": af.ArenaFold(armed=True, avoidance=True), "W1-NULL": af.ArenaFold(armed=False), "M-POL-2": None}[MODE]
                sink: List[Dict[str, Any]] = []
                kin = kn.KinematicsFold(shape=kn.Shape.K_MILL, tether=kn.TetherLimb.PER_WAVE,
                                        px_arm_label="PX-LO", seed_salt=salt)
                err = None
                with upn4._overrides(contact_response="separate", geometry_on=True,
                                     seek_fold=True, policy=PlayerPolicy.DRIVE_TO_PACK,
                                     kinematics=kin, death_continued=cont, sink=sink):
                    try:
                        runner(salt=salt, arena=arena, period_s=period, seat=True)
                    except Exception as exc:                          # noqa: BLE001
                        err = f"{type(exc).__name__}: {exc}"
                a = arena.as_dict() if hasattr(arena, "as_dict") else {}
                if arena is None: arena = af.ArenaFold(armed=False)
                per[str(salt)] = {
                    "max_body_radius_m": arena.max_body_radius_m,
                    "margin_to_R_wall_m": R_WALL - arena.max_body_radius_m,
                    "n_wall_clamps_body": arena.n_wall_clamps_body,
                    "n_wall_clamps_player": arena.n_wall_clamps_player,
                    "max_player_radius_m": arena.max_player_radius_m,
                    "max_wall_overlap_m": arena.max_wall_overlap_m,
                    "n_spawn_placements": arena.n_spawn_placements,
                    "n_spawn_outside_wall": arena.n_spawn_outside_wall,
                    "n_avoidance_vetoes": arena.n_avoidance_vetoes,
                    "waves_run": [x["wave"] for x in sink], "last_wave_t_s": sink[-1]["t_s"] if sink else None,
                    "⚑ observation_only.max_radius_after_separation_m": obs.get("max_post_sep_r"),
                    "⚑ observation_only.n_separation_displacements": obs.get("n_disp", 0),
                    "⚑ observation_only.n_post_separation_positions_beyond_R_wall":
                        obs.get("n_post_sep_beyond_wall", 0),
                    "raised": None if (err or "").startswith("_LadderHorizon") else err,
                    "raised_raw": err,
                }
                print(f"[H-9] {leg} salt {salt} {time.time() - t0:.0f}s "
                      f"max_r={arena.max_body_radius_m:.6f} clamps_body={arena.n_wall_clamps_body} "
                      f"clamps_player={arena.n_wall_clamps_player} waves={per[str(salt)]['waves_run']} "
                      f"post_sep_max={obs.get('max_post_sep_r')} err={err}",
                      file=sys.stderr, flush=True)
            mx = max(v["max_body_radius_m"] for v in per.values())
            result["legs"][leg] = {
                "per_salt": per,
                "max_over_salts_m": mx,
                "min_margin_m": R_WALL - mx,
                "total_wall_clamps_body": sum(v["n_wall_clamps_body"] for v in per.values()),
                "total_wall_clamps_player": sum(v["n_wall_clamps_player"] for v in per.values()),
            }
    finally:
        kr.simulate_wave = real_sw                                    # type: ignore[assignment]
        lo.Mover.displace = real_disp                                 # type: ignore[assignment]

    A = result["legs"]["A_stop_at_death"]
    result.update({
        "⚑ artifact_class": "NOT-A-GRADED-RUN. prereg v1.9 § F.2j H-9. ORACLE side only. "
                            "Read-only; nothing tuned (Law 3); no sealed cell opened (K-7).",
        "R_wall_m": R_WALL, "R_wall_rederived_from_arena_json": derived_wall,
        "tick_period_s": period,
        "config": {"cell": "SEALED-KMILL | SEP-ON (upn4._overrides, contact_response='separate', "
                           "geometry_on=True, seek_fold=True, DRIVE_TO_PACK, K_MILL PER_WAVE PX-LO)",
                   "arena": "ArenaFold(armed=True, avoidance=True) — W1 arm of record",
                   "loader": "load_profiles(dot_corrections=True, winner_surface=from_x8(P-n.2), "
                             "pool_lift=load(), c11a=C11aLoader(CLASS))",
                   "simulate_wave": "c11a_corrections=C11aFold(C1 retaliation_gate, C4 "
                                    "duration_divisors, C2 aura CLASS)",
                   "salts": [0, 1, 2, 3, 4]},
        "verdict_leg_A": ("OUTCOME 1 (PASS): oracle inside R_wall with zero clamps on every salt"
                          if A["max_over_salts_m"] <= R_WALL and A["total_wall_clamps_body"] == 0
                          and A["total_wall_clamps_player"] == 0 else
                          "OUTCOME 2 (BREACH): routes to Matt"),
        "wall_s": round(time.time() - t0, 1),
        "utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    })
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1, default=str)
    print(out_path, _sha(out_path))


if __name__ == "__main__":
    main(sys.argv[1])
