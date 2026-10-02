#!/usr/bin/env python3
"""KC2-PLAY · H-6 pre-read (jack-ryan, 2026-10-02) · THE GATE's OWN ORACLE PROBE. READ-ONLY on the engine.

Written by the gate, NOT derived from gamora's instruments (they were read first; nothing is imported from them).
Runs the oracle of record exactly as the pack names it:
    engine scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py  run_one("V311-FULL", (0..4), period, arm)  (+ v3p8.graded_arm)
for one arm, with forwarding read-only hooks, and records the quantities the gate re-computes independently:

  G-OBS1   the SHARED OBS-1 guard (engine 9c756081, gamora_join1_obs1_guard_2026_10_02.cell_check: G1 10 rows w151..160
           with raw outcome, G2 w160 not at the tick cap, G3 9N rows) applied to run_one's own result, PLUS the gate's
           innermost simulate_wave observer (outcome / termination_reason / escaped exceptions, per wave).
  G-TRAJ   a per-cell trajectory digest over the oracle's own outputs (per wave: tick range, outcome, actors, the full
           event-row list, the ring ledger) -> distinct-trajectory count and the arm-identity relations TA-X-03/04/05.
  G-30a    TA-X-30(a') re-checked by the gate's own rule: every roster step whose target is the step's player_xy argument
           obeys travel = min(v dt, max(0, dist - op)) unless held/clipped; the operand is classified by MEMBERSHIP
           against the PACK (not against halt_for's return): op == 0 <=> a waypoint step (gate's own waypoint hook);
           op == the pre-step centre distance (Attack); op == 2.4 (ring halt); op / (1 - 1e-9) in the record's pack reach
           set {gr2 gd_use_range_m_HI rows} U {GD Default-attack formula from gr1 rows} U {the record's packed slot reach}.
  G-30b    every ArenaFold.clamp_body call and every call that RETURNED True (an actual stop), per cell.
  G-CLIP   every call into geometry.max_admissible_travel (the non-penetration clip) and every roster step that it shortened.
  G-29div  every CompositionFold.dot call by damage_type; for SlowChaos / SlowAether: whether the divisor branch is
           ELIGIBLE (gmag terms fold the attribute limb, duration_attr_mult None) and the value under int/200+1 vs 1.0.
           Static reachability: every SlowChaos/SlowAether DoT row on any profile the RUN's loader built.
  G-ROWS   independent re-measures of TA-X-10, 11, 12, 13, 15(a), 16, 24 and TA-X-25's POOL-466 membership.

Usage: python3 h6_gate_probe.py <ARM> <out.json>
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from collections import Counter

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
ENGINE_SRC = "/Users/admin/Games/reincarnated-engine/src"
ARM, OUT = sys.argv[1], os.path.abspath(sys.argv[2])   # absolute BEFORE the chdir (the oracle needs cwd = engine src)
sys.path.insert(0, ENGINE_SRC)
os.chdir(ENGINE_SRC)
MODEL = ("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
         "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model")

from reincarnated.simulation.kc2 import run as kr  # noqa: E402
from reincarnated.simulation.kc2 import locomotion as lo  # noqa: E402
from reincarnated.simulation.kc2 import gd_reposition as gdr  # noqa: E402
from reincarnated.simulation.kc2 import gd_composition as gc  # noqa: E402
from reincarnated.simulation.kc2 import arena_fold as af  # noqa: E402
from reincarnated.simulation.kc2 import geometry as gm  # noqa: E402
from reincarnated.simulation.kc2 import c11a_corrections as c11a  # noqa: E402
from reincarnated.simulation.kc2 import referent_lineup as rl  # noqa: E402
from reincarnated.simulation.kc2 import threat as th  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311  # noqa: E402
from reincarnated.simulation.scripts import gamora_join1_obs1_guard_2026_10_02 as OBS1  # noqa: E402

CUR = {"rec": False, "salt": None, "wave": None}
S = {}


def st():
    return S.setdefault(str(CUR["salt"]), {
        "waves": [], "exceptions": [], "traj": [], "t30": Counter(), "t30_fail": [], "op_class": Counter(),
        "clamp_calls": 0, "clamp_true": 0, "clamp_true_player_target_nonwp": 0, "clip_calls": 0, "clip_shortened": 0,
        "dot_by_type": Counter(), "chaos_aether": Counter(), "chaos_aether_examples": [],
        "lu_keys": {}, "crit_sources": Counter(), "spawn_t": Counter(), "phase_model": set(), "pool_tags": Counter(),
        "arena": [], "max_body_r": 0.0, "max_spawn_r": 0.0, "records": Counter()})


# ---------------------------------------------------------------------------------------- PACK reach sets (gate's own)
_mo = json.load(open(os.path.join(MODEL, "monster_offense.json")))
REACH = {}        # record -> set of admissible reaches from the pack's gr2 rows
RBODY = {}
for r in _mo["⚑ v3p8_rows"]["gr2_gd_fire_range"]:
    v = r["value"]
    REACH.setdefault(r["record_path"], set()).add(float(v["gd_use_range_m_HI"]))
    if v.get("monster_actor_radius_m") is not None and r["record_path"] not in RBODY:
        RBODY[r["record_path"]] = float(v["monster_actor_radius_m"]) * float(v.get("monster_scale") or 1.0)
_mr = json.load(open(os.path.join(MODEL, "math_rules.json")))
GR1 = {r["id"]: r["value"] for r in _mr["⚑ v3p8_rows"]["gr1_gd_fire_range_constants"]}
LADDER_MELEE = float(GR1["V38-GR1-LADDER-MELEE"]["range_m"])
TOL = float(GR1["V38-GR1-TOLERANCE"]["value_m"])
ARENA = json.load(open(os.path.join(MODEL, "arena.json")))
RING = float(ARENA["d_engage_m"]["value"])          # arena.json :: d_engage_m (the ring halt, 2.4)
PLAYER_R = None   # read from the oracle module once (declared constant), compared to the pack-free formula below
PROFILES = {}
PET_PROFILES = {}

_olp = th.load_profiles


def _lp(*a, **kw):
    out = _olp(*a, **kw)
    PROFILES.update(out[0])          # roster_by_record
    PET_PROFILES.update(out[1])      # pet_by_record
    return out
th.load_profiles = _lp


def _admissible(record):
    """the record's admissible reach set: gr2 rows, the GD Default-attack formula, its packed slot reaches."""
    s = set(REACH.get(record, ()))
    from reincarnated.simulation.kc2 import gd_engagement as ge
    s.add(LADDER_MELEE + RBODY.get(record, ge.BODY_RADIUS_FALLBACK_M) + ge.PLAYER_RADIUS_M + TOL)
    p = PROFILES.get(record) or PROFILES.get(record.lower()) or PET_PROFILES.get(record)
    if p is not None:
        for sl in p.slots:
            s.add(float(sl.reach_m))
    return s


# ---------------------------------------------------------------------------------------- waypoint flag (gate's own)
WP = {}
_owp = gdr.GdRepositionFold.waypoint


def _wp(self, aid, xy, player_xy):
    r = _owp(self, aid, xy, player_xy)
    if CUR["rec"]:
        WP[aid] = r
    return r
gdr.GdRepositionFold.waypoint = _wp

# ---------------------------------------------------------------------------------------- the clip
_omat = gm.max_admissible_travel


def _mat(*a, **kw):
    out = _omat(*a, **kw)
    if CUR["rec"]:
        st()["clip_calls"] += 1
    return out
gm.max_admissible_travel = _mat
if hasattr(lo, "_geometry") and getattr(lo._geometry, "max_admissible_travel", None) is _omat:
    lo._geometry.max_admissible_travel = _mat

# ---------------------------------------------------------------------------------------- TA-X-30(a') gate rule
LASTSTEP = {}
_ostep = lo.Mover.step


def _step(self, dt_s, player_xy, **kw):
    if not CUR["rec"] or kw.get("tick") is None:
        return _ostep(self, dt_s, player_xy, **kw)
    pre = self.xy
    nb0 = self.n_blocked_steps
    op = float(kw["d_engage_m"])
    wp = WP.pop(self.actor_id, None)
    out = _ostep(self, dt_s, player_xy, **kw)
    if self.n_blocked_steps > nb0:
        st()["clip_shortened"] += 1
    LASTSTEP[self.actor_id] = None
    if "_pet" in self.actor_id or not self.mech_is_player_target_step:
        return out
    T = st()["t30"]
    T["roster_player_arg_steps"] += 1
    dist = math.hypot(player_xy[0] - pre[0], player_xy[1] - pre[1])
    law = min(self.speed_m_per_s * dt_s, max(0.0, dist - op))
    held = (self.emerge_hold_active_step or self.stationary_hold_active_step or self.mech_hold_active_step
            or self.alert_hold_active_step or self.stationary)
    trav = self.last_step_travel_m
    f = []
    if op != op or dist != dist:
        f.append("nan")
    if bool(self.mech_ring_halt_step) != (dist - op <= 0.0):
        f.append("halt_flag")
    if held:
        T["held"] += 1
        if trav != 0.0:
            f.append("held_moved")
    elif self.n_blocked_steps > nb0:
        T["clipped"] += 1
        if not trav < law:
            f.append("clip_not_shorter")
    else:
        T["unclipped"] += 1
        if trav != law:
            f.append("travel_ne_law")
    # operand membership (the gate's rule, against the pack)
    is_wp = wp is not None
    if is_wp:
        cls = "op0_waypoint" if op == 0.0 else "WAYPOINT_op_ne_0"
        if (wp[0], wp[1]) != (player_xy[0], player_xy[1]):
            f.append("waypoint_not_step_target")
    elif op == 0.0:
        cls = "op0_NOT_waypoint"
    elif op == dist:
        cls = "attack_stand(op=dist)"
    elif op == RING:
        cls = "ring_halt(op=2.4)"
    else:
        reach = op / (1.0 - 1e-9)
        adm = _admissible(self.record)
        hit = any(abs(reach - x) <= 1e-12 * max(1.0, x) for x in adm)
        exact = any(x * (1.0 - 1e-9) == op for x in adm)
        cls = "pursue_reach_in_pack" if (hit or exact) else "OP_NOT_IN_PACK_SET"
    st()["op_class"][cls] += 1
    if cls in ("WAYPOINT_op_ne_0", "op0_NOT_waypoint", "OP_NOT_IN_PACK_SET"):
        f.append(cls)
    LASTSTEP[self.actor_id] = (not is_wp and not held, dist, op)
    if f:
        T["fail"] += 1
        for x in f:
            T["fail:" + x] += 1
        if len(st()["t30_fail"]) < 12:
            st()["t30_fail"].append([CUR["wave"], self.actor_id, self.record, f, op, dist, trav, law])
    return out
lo.Mover.step = _step

_ocb = af.ArenaFold.clamp_body


def _cb(self, mover, pre_xy):
    r = _ocb(self, mover, pre_xy)
    if CUR["rec"]:
        st()["clamp_calls"] += 1
        if r:
            st()["clamp_true"] += 1
            p = LASTSTEP.get(mover.actor_id)
            if p and p[0] and p[1] > p[2]:
                st()["clamp_true_player_target_nonwp"] += 1
    return r
af.ArenaFold.clamp_body = _cb

# ---------------------------------------------------------------------------------------- TA-X-29(b') divisor
_odt = gc.CompositionFold.dot


def _dt(self, eng, prof, r, om):
    v = _odt(self, eng, prof, r, om)
    if CUR["rec"]:
        X = st()
        X["dot_by_type"][r.damage_type] += 1
        if r.damage_type in gc.CHAOS_AETHER_DOT_TYPES:
            gt = eng.gmag.terms_for(prof.record) if eng.gmag is not None else None
            elig = bool(gt is not None and eng.gmag.attr_on and getattr(gt, "folds_attr", False)
                        and c11a.duration_attr_mult(gt, r.damage_type) is None)
            X["chaos_aether"]["rows"] += 1
            X["chaos_aether"]["divisor_eligible"] += int(elig)
            X["chaos_aether"]["divisor_flag_on_fold"] += int(bool(self.chaos_aether_dot_divisor))
            if len(X["chaos_aether_examples"]) < 6:
                X["chaos_aether_examples"].append([prof.record, r.damage_type, elig, v])
    return v
gc.CompositionFold.dot = _dt

# ---------------------------------------------------------------------------------------- line-up keys (TA-X-16)
_olr = rl.ReferentLineupFold.roll


def _lr(self, wave, incumbent, **kw):
    out = _olr(self, wave, incumbent, **kw)
    if CUR["rec"]:
        st()["lu_keys"][str(wave)] = {"fold_keys": sorted(int(k) for k in rl.REFERENT_LINEUP.get(int(wave), {}).keys()),
                                      "fought_points": sorted({int(b.spawn_point) for b in out.bodies}),
                                      "bonus": kw.get("bonus_spawns_enabled")}
    return out
rl.ReferentLineupFold.roll = _lr

# ---------------------------------------------------------------------------------------- innermost wave observer
_real_arm = c11.run_arm


def _arm(runner, a, salt, period):
    CUR["rec"], CUR["salt"] = True, int(salt)
    st()
    try:
        return _real_arm(runner, a, salt, period)
    finally:
        CUR["rec"] = False
c11.run_arm = _arm
_true_sw = kr.simulate_wave


def _h(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()


def _sw(*a, **kw):
    if not CUR["rec"]:
        return _true_sw(*a, **kw)
    w = int(a[0] if a else kw["wave"])
    CUR["wave"] = w
    afo = kw.get("arena_fold")
    a0 = (afo.n_wall_clamps_player, afo.n_wall_clamps_body) if afo is not None else None
    try:
        r = _true_sw(*a, **kw)
    except Exception as e:
        st()["exceptions"].append([w, type(e).__name__, str(e)[:200]])
        raise
    X = st()
    w0 = r.waves[0]
    X["waves"].append([w, w0.get("outcome"), w0.get("termination_reason"), int(w0["tick_start"]), int(w0["tick_end"])])
    rows = r.rows_as_dicts()
    led = getattr(r, "ring_ledger", {}) or {}
    X["traj"].append(_h({"w": w, "ts": w0["tick_start"], "te": w0["tick_end"], "o": w0.get("outcome"),
                         "actors": r.actors, "rows": rows, "ledger": led.get("rows"), "pets": r.pet_actors}))
    for x in rows:
        if x.get("is_crit"):
            X["crit_sources"][str(x.get("source_id"))[:12]] += 1
        t = str(x.get("damage_source_tag"))
        if "pool" in t.lower():
            X["pool_tags"][t] += 1
    for x in r.actors:
        X["spawn_t"][f"{x['spawn_point_id']}@{x['spawn_t_s']}"] += 1
        X["records"][x["record_path"]] += 1
        X["max_spawn_r"] = max(X["max_spawn_r"], math.hypot(x["spawn_x"], x["spawn_y"]))
    for x in (led.get("rows") or []):
        if x[2] == 1:
            X["max_body_r"] = max(X["max_body_r"], math.hypot(x[4], x[5]))
    X["phase_model"].add(str(kw.get("phase_model")))
    if afo is not None:
        X["arena"].append([w, bool(getattr(afo, "armed", False)), bool(getattr(afo, "active", False)),
                           getattr(afo, "r_wall_m", None), afo.n_wall_clamps_player - a0[0],
                           afo.n_wall_clamps_body - a0[1]])
    return r
kr.simulate_wave = _sw


#: EVERY source line containing `round(` (not a comment) in every simulation/kc2 module: the gate does not pre-select
#: the sites it expects; it watches all of them and reports which ones the V311-FULL fight actually executes.
KC2_DIR = os.path.join(ENGINE_SRC, "reincarnated/simulation/kc2")
ROUND_SITES = {}
for _fn in sorted(os.listdir(KC2_DIR)):
    if _fn.endswith(".py"):
        _ls = [i + 1 for i, l in enumerate(open(os.path.join(KC2_DIR, _fn)).read().splitlines())
               if "round(" in l and not l.lstrip().startswith("#")]
        if _ls:
            ROUND_SITES[_fn] = tuple(_ls)
ROUND_HITS = Counter()


def _install_line_monitor():
    """sys.monitoring (PEP 669) LINE events, enabled LOCALLY on the code objects that hold the watched lines only."""
    import types
    mods = [m for n, m in list(sys.modules.items())
            if n.startswith("reincarnated.simulation.kc2.") and getattr(m, "__file__", None)
            and m.__file__.rsplit("/", 1)[-1] in ROUND_SITES]
    mon = sys.monitoring
    TOOL = mon.PROFILER_ID
    mon.use_tool_id(TOOL, "h6-round-sites")
    want = {}
    for mod in mods:
        fn = mod.__file__.rsplit("/", 1)[-1]
        lines = set(ROUND_SITES[fn])
        seen = set()
        stack = [v for v in vars(mod).values()]
        codes = []
        while stack:
            o = stack.pop()
            if id(o) in seen:
                continue
            seen.add(id(o))
            if isinstance(o, type) and o.__module__ == mod.__name__:
                stack.extend(vars(o).values())
            elif isinstance(o, (staticmethod, classmethod)):
                stack.append(o.__func__)
            elif isinstance(o, property):
                stack.extend([o.fget, o.fset])
            elif isinstance(o, types.FunctionType) and o.__module__ == mod.__name__:
                stack.append(o.__code__)
            elif isinstance(o, types.CodeType):
                codes.append(o)
                stack.extend(c for c in o.co_consts if isinstance(c, types.CodeType))
        for c in codes:
            ls = {ln for _, _, ln in c.co_lines() if ln is not None}
            if ls & lines:
                mon.set_local_events(TOOL, c, mon.events.LINE)
                want[c] = fn

    def _line(code, line):
        if CUR["rec"] and line in ROUND_SITES.get(want.get(code, ""), ()):
            ROUND_HITS[f"{want[code]}:{line}"] += 1
        return None
    mon.register_callback(TOOL, mon.events.LINE, _line)
    return {"n_modules_watched": len(mods), "n_lines_watched": sum(len(v) for v in ROUND_SITES.values()),
            "n_code_objects": len(want)}


def main():
    t0 = time.time()
    period = FP._period()
    salts = (0, 1, 2, 3, 4)
    tracing = len(sys.argv) > 3 and sys.argv[3] == "trace_round"
    monitored = _install_line_monitor() if tracing else None
    res = V311.run_one("V311-FULL", salts, period, arm=ARM)
    guard = OBS1.cell_check(res, salts, period)
    # static reachability of the divisor clause: SlowChaos / SlowAether DoT rows on ANY profile the run's loader built
    reach = []
    for rec, p in list(PROFILES.items()) + [("PET:" + k, v) for k, v in PET_PROFILES.items()]:
        for sl in tuple(getattr(p, "slots", ())) + tuple(getattr(p, "dying", ())) + tuple(getattr(p, "auras", ())):
            for row in sl.rows:
                if row.kind == "dot" and row.damage_type in gc.CHAOS_AETHER_DOT_TYPES:
                    reach.append([rec, sl.slot, sl.skill, row.damage_type])
        for row in getattr(p, "weapon_rows", ()):
            if row.kind == "dot" and row.damage_type in gc.CHAOS_AETHER_DOT_TYPES:
                reach.append([rec, "weapon", row.skill, row.damage_type])
    out = {"arm": ARM, "period": period, "ring_halt_m(arena.json)": RING, "obs1_guard": guard,
           "obs1_guard_module_sha256": hashlib.sha256(open(OBS1.__file__, "rb").read()).hexdigest(),
           "run_one_keys": sorted(res.keys()), "salt_keys": sorted(res["salts"]["0"].keys()),
           "n_profiles_seen": len(PROFILES), "n_pet_profiles_seen": len(PET_PROFILES),
           "round_site_hits (trace_round mode only)": dict(ROUND_HITS) if tracing else None,
           "round_site_monitored_functions": monitored, "chaos_aether_dot_rows_on_loaded_profiles": reach, "salts": {}}
    for s in salts:
        x = S[str(s)]
        out["salts"][str(s)] = {
            "waves": x["waves"], "exceptions": x["exceptions"], "leg_a": res["salts"][str(s)].get("leg_a_terminal"),
            "raised": res["salts"][str(s)].get("raised"),
            "capture_rows_sha256": _h(res["salts"][str(s)].get("rows")),
            "traj_digest": _h(x["traj"]), "traj_per_wave": x["traj"],
            "t30": dict(x["t30"]), "t30_fail": x["t30_fail"], "op_class": dict(x["op_class"]),
            "clamp_calls": x["clamp_calls"], "clamp_true": x["clamp_true"],
            "clamp_true_player_target_nonwp_beyond_op": x["clamp_true_player_target_nonwp"],
            "clip_calls": x["clip_calls"], "clip_shortened_steps": x["clip_shortened"],
            "dot_by_type": dict(x["dot_by_type"]), "chaos_aether": dict(x["chaos_aether"]),
            "chaos_aether_examples": x["chaos_aether_examples"], "lu_keys": x["lu_keys"],
            "crit_sources": dict(x["crit_sources"]), "spawn_t": dict(x["spawn_t"]),
            "phase_model": sorted(x["phase_model"]), "pool_tags": dict(x["pool_tags"]), "arena": x["arena"],
            "max_body_r": x["max_body_r"], "max_spawn_r": x["max_spawn_r"], "records": dict(x["records"])}
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(OUT, "w"), indent=1, sort_keys=True, default=str)
    print(f"[h6-probe] {ARM} wall={out['wall_s']}s guard_complete={guard['complete']}", flush=True)


if __name__ == "__main__":
    main()
