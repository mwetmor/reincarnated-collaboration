#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.15 · LAW (a) ON THE TWO RESTATED ROWS (Matt Q104, KP-240) (gamora, 2026-10-02). READ-ONLY.

Runs the oracle of record (engine 969fbd8d `scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py` run_one("V311-FULL") +
v3p8.graded_arm, imported unmodified) on one arm, salts 0-4 in one call (as graded), with read-only hooks that check:

TA-X-30 (restated):
  (a') every roster `Mover.step` whose target is the step's `player_xy` argument computes
       travel_law = min(v·dt, max(0, dist − op)) with op = the step's own `d_engage_m`, and
       halt flag = (dist − op) <= 0 exactly; the applied travel equals travel_law unless the non-penetration clip
       (`n_blocked_steps` incremented) shortened it or a hold (emergence / stationary / mech / alert) zeroed it; the
       post-step position is pre + unit·travel; no NaN operand or distance.
       The operand's PROVENANCE: on a non-waypoint step op is exactly the value `GdEngagementFold.halt_for` returned for
       that body at that step, by branch: ATTACK -> the centre distance (the body stands); PURSUE -> chosen slot's
       reach × (1 − 1e-9), where the reach is the pack's `monster_offense.json :: ⚑ v3p8_rows.gr2_gd_fire_range`
       `gd_use_range_m_HI` for (record, slot, skill), or for GD's Default attack 1.25 + r_body + 0.336 + 0.5;
       DEFAULT (no state / no skill) -> the ring halt radius (2.4). On a waypoint step op = 0.
  (b) R-G4-V311: distinct roster bodies with >= 1 player-targeted, non-waypoint, non-hold, non-emerging step that
       `ArenaFold.clamp_body` stopped with pre-step distance > the step's op. Expected 0. Vacuous where no armed
       ArenaFold exists (counted: clamp calls per arm).
TA-X-29(b) (restated): every `CompositionFold.instant` / `.dot` return value is RECOMPUTED here from its inputs by the
       law as Matt ruled it (CompositionFold, LO physical limb, the declared SlowChaos/SlowAether divisor), with the
       physical factor map rebuilt from the pinned CSV by this script, and compared BIT FOR BIT.
OBS-1 guard: per salt, w151..w160 banked, every wave cleared/board_empty or player_death/player_died, no exception
       escaping the true simulate_wave, raised None. A failure is a STOP (exit 2, nothing derived).

Usage:  python3 audit_v1p15.py <ARM> <out.json>
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
ENGINE_SRC = "/Users/admin/Games/reincarnated-engine/src"
sys.path.insert(0, ENGINE_SRC)
os.chdir(ENGINE_SRC)
ARM, OUT = sys.argv[1], sys.argv[2]
MODEL = ("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
         "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model")

from reincarnated.simulation.kc2 import run as kr  # noqa: E402
from reincarnated.simulation.kc2 import locomotion as lo  # noqa: E402
from reincarnated.simulation.kc2 import gd_engagement as ge  # noqa: E402
from reincarnated.simulation.kc2 import gd_reposition as gdr  # noqa: E402
from reincarnated.simulation.kc2 import gd_composition as gc  # noqa: E402
from reincarnated.simulation.kc2 import arena_fold as af  # noqa: E402
from reincarnated.simulation.kc2 import discrete_volley as dv  # noqa: E402
from reincarnated.simulation.kc2 import c11a_corrections as c11a  # noqa: E402
from reincarnated.simulation.kc2.opposition import DATA_DIR  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311  # noqa: E402

CUR = {"rec": False, "salt": None, "wave": None}
S = {}            # salt -> stats


def st():
    return S.setdefault(str(CUR["salt"]), {
        "waves": [], "exceptions": [], "raised": None, "rows_n": None,
        "t30": Counter(), "t30_fail_examples": [], "beyond_bodies": set(), "clamp_calls": 0,
        "arena_armed_waves": 0, "op_classes": Counter(),
        "t29": Counter(), "t29_fail_examples": [], "t29_instances": Counter()})


# ---------------------------------------------------------------------------------------------- pack: the reach rows
_mo = json.load(open(os.path.join(MODEL, "monster_offense.json")))
GR2 = {}
RBODY = {}
for r in _mo["⚑ v3p8_rows"]["gr2_gd_fire_range"]:
    v = r["value"]
    GR2[(r["record_path"], v["slot"], v["skill"])] = float(v["gd_use_range_m_HI"])
    if v.get("monster_actor_radius_m") is not None:
        RBODY.setdefault(r["record_path"], float(v["monster_actor_radius_m"]) * float(v.get("monster_scale") or 1.0))
_mr = json.load(open(os.path.join(MODEL, "math_rules.json")))
GR1 = {r["id"]: r["value"] for r in _mr["⚑ v3p8_rows"]["gr1_gd_fire_range_constants"]}


def _num(x):
    if isinstance(x, dict):
        for k in ("value", "m", "value_m"):
            if k in x and isinstance(x[k], (int, float)):
                return float(x[k])
        return None
    return float(x) if isinstance(x, (int, float)) else None


LADDER_MELEE = float(GR1["V38-GR1-LADDER-MELEE"]["range_m"])
TOL = float(GR1["V38-GR1-TOLERANCE"]["value_m"])

# ---------------------------------------------------------------------------------------------- TA-X-30 hooks
LAST_HALT = {}
_ohf = ge.GdEngagementFold.halt_for


def _hf(self, eng, actor_id, body_xy, player_xy, default_m):
    out = _ohf(self, eng, actor_id, body_xy, player_xy, default_m)
    if CUR["rec"]:
        A = eng._ge_state.get(actor_id) if eng is not None else None
        if eng is None or A is None:
            br, s_ = "DEFAULT(no state)", None
        elif A["mode"] == "A":
            br, s_ = "ATTACK", None
        elif A["S"] is not None:
            br, s_ = "PURSUE", A["S"]
        else:
            br, s_ = "DEFAULT(no skill)", None
        LAST_HALT[actor_id] = (br, out, s_, default_m, tuple(body_xy), tuple(player_xy))
    return out
ge.GdEngagementFold.halt_for = _hf

WP = {}
WPS = {}   # aid -> the chosen slot whose reach a Pursue waypoint's stop point uses
_owp = gdr.GdRepositionFold.waypoint


def _wp(self, aid, xy, player_xy):
    r = _owp(self, aid, xy, player_xy)
    if CUR["rec"]:
        WP[aid] = r is not None
        X = self.X.get(aid)
        A = self.eng._ge_state.get(aid) if self.eng is not None else None
        WPS[aid] = (A["S"] if (r is not None and X is not None and X["m"] not in ("R", "W") and A is not None
                               and A["mode"] == "P" and X["wp"] is not None and A["S"] is not None) else None)
    return r
gdr.GdRepositionFold.waypoint = _wp

STEP = {}
_ostep = lo.Mover.step


def _step(self, dt_s, player_xy, **kw):
    if not CUR["rec"] or kw.get("tick") is None:
        return _ostep(self, dt_s, player_xy, **kw)
    pre = self.xy
    nb0 = self.n_blocked_steps
    op = float(kw["d_engage_m"])
    to_wp = WP.pop(self.actor_id, False)
    hal = LAST_HALT.pop(self.actor_id, None)
    out = _ostep(self, dt_s, player_xy, **kw)
    T = st()["t30"]
    roster = "_pet" not in self.actor_id
    if not (roster and self.mech_is_player_target_step):
        return out
    T["n_player_arg_steps"] += 1
    dx, dy = player_xy[0] - pre[0], player_xy[1] - pre[1]
    dist = math.hypot(dx, dy)
    law = min(self.speed_m_per_s * dt_s, max(0.0, dist - op))
    held = bool(self.emerge_hold_active_step or getattr(self, "stationary_hold_active_step", False)
                or self.mech_hold_active_step or self.alert_hold_active_step or self.stationary)
    blocked = self.n_blocked_steps > nb0
    trav = self.last_step_travel_m
    fails = []
    if math.isnan(op) or math.isnan(dist):
        fails.append("nan")
    if bool(self.mech_ring_halt_step) != ((dist - op) <= 0.0):
        fails.append("halt_flag")
    if held:
        T["n_held"] += 1
        if trav != 0.0:
            fails.append("held_but_moved")
    elif blocked:
        T["n_clipped"] += 1
        if not (trav < law):
            fails.append("clip_not_shorter")
    else:
        T["n_unclipped"] += 1
        if trav != law:
            fails.append("travel_ne_law")
    if dist > 0.0 and trav > 0.0:
        ex = (pre[0] + dx / dist * trav, pre[1] + dy / dist * trav)
        if self.xy != ex:
            fails.append("position")
    # operand provenance
    if to_wp:
        T["n_waypoint_steps"] += 1
        st()["op_classes"]["WAYPOINT(op=0)"] += 1
        if op != 0.0:
            fails.append("waypoint_op_ne_0")
        s_ = WPS.pop(self.actor_id, None)
        if s_ is not None:                       # a Pursue waypoint: its stop point is CloseEnoughToUseSkill(S)
            if s_.skill == ge.DEFAULT_SKILL:
                want = LADDER_MELEE + RBODY.get(self.record, ge.BODY_RADIUS_FALLBACK_M) + ge.PLAYER_RADIUS_M + TOL
                st()["op_classes"]["WAYPOINT:pursue_reach=default_attack"] += 1
            else:
                want = GR2.get((self.record, s_.slot, s_.skill))
                if want is None:
                    want = s_.reach_m
                    st()["op_classes"]["WAYPOINT:pursue_reach=slot_without_gr2_row(packed)"] += 1
                else:
                    st()["op_classes"]["WAYPOINT:pursue_reach=gr2_row"] += 1
            if s_.reach_m != want:
                fails.append("waypoint_reach_ne_pack")
    else:
        if hal is None:
            fails.append("no_halt_for_call")
        else:
            br, val, s_, dflt, bxy, pxy = hal
            st()["op_classes"][br] += 1
            if val != op:
                fails.append("op_ne_halt_for")
            if br == "ATTACK":
                if op != math.hypot(pxy[0] - bxy[0], pxy[1] - bxy[1]):
                    fails.append("attack_op_ne_distance")
            elif br == "PURSUE":
                if s_.skill == ge.DEFAULT_SKILL:
                    rb = RBODY.get(self.record, ge.BODY_RADIUS_FALLBACK_M)
                    want = LADDER_MELEE + rb + ge.PLAYER_RADIUS_M + TOL
                    st()["op_classes"]["PURSUE:default_attack"] += 1
                else:
                    want = GR2.get((self.record, s_.slot, s_.skill))
                    if want is None:
                        st()["op_classes"]["PURSUE:slot_without_gr2_row(packed reach)"] += 1
                        want = s_.reach_m
                    else:
                        st()["op_classes"]["PURSUE:gr2_row"] += 1
                if s_.reach_m != want:
                    fails.append("reach_ne_pack")
                if op != s_.reach_m * (1.0 - 1e-9):
                    fails.append("pursue_op_ne_reach")
            else:
                if op != dflt:
                    fails.append("default_op_ne_ring_halt")
    pursuit = not to_wp and not held and not bool(self.emerge_hold_active_step)
    STEP[self.actor_id] = (pursuit, dist, op)
    T["n_checked"] += 1
    if fails:
        T["n_fail"] += 1
        for f in fails:
            T["fail:" + f] += 1
        if len(st()["t30_fail_examples"]) < 10:
            st()["t30_fail_examples"].append([CUR["wave"], self.actor_id, fails, op, dist, trav, law])
    return out
lo.Mover.step = _step

_ocb = af.ArenaFold.clamp_body


def _cb(self, mover, pre_xy):
    r = _ocb(self, mover, pre_xy)
    if CUR["rec"]:
        st()["clamp_calls"] += 1
        if r:
            p = STEP.get(mover.actor_id)
            if p is not None and p[0] and p[1] > p[2]:
                st()["beyond_bodies"].add(f"{CUR['wave']}|{mover.actor_id}")
    return r
af.ArenaFold.clamp_body = _cb

# ---------------------------------------------------------------------------------------------- TA-X-30: PETS
#   The pet step is inline in run.py (`if d > halt and speed > 0: step = min(speed*period, d - halt)`, then the same
#   non-penetration clip, then `ps["x"] += dx/d*step`), with halt = D_ENGAGE_M (2.4) on the incumbent walk or
#   pet_target's own halt (0.0 toward its slot stop point / RFA / roam point / own spot). Under V311-FULL every pet step
#   is preceded by a `pet_target` call (it returns None on the incumbent walk). The moved position is observed where
#   run.py writes it into the tick's occupancy map (`live[pid] = (x, y, r)`), immediately after the move.
PERIOD = [None]
PET_PENDING = {}
_opt = gdr.GdRepositionFold.pet_target


def _ptt(self, pid, ps, player_xy, tick):
    r = _opt(self, pid, ps, player_xy, tick)
    if CUR["rec"]:
        if r is None:
            tgt, halt, cls = (float(player_xy[0]), float(player_xy[1])), lo.D_ENGAGE_M, "PET:incumbent_walk(op=2.4)"
        else:
            tgt, halt, cls = (r[0], r[1]), r[2], "PET:pet_target(op=%r)" % r[2]
            S_ = self._pet_normal(self.eng.pets.get(ps["pet_record"])) if self.eng is not None else None
            if S_ is not None:
                want = GR2.get((ps["pet_record"], S_.slot, S_.skill))
                st()["op_classes"]["PET:reach=" + ("gr2_row" if want is not None else "no_gr2_row(packed)")] += 1
                if want is not None and S_.reach_m != want:
                    st()["t30"]["fail:pet_reach_ne_pack"] += 1
                    st()["t30"]["n_fail"] += 1
        st()["op_classes"][cls] += 1
        dx, dy = tgt[0] - ps["x"], tgt[1] - ps["y"]
        d = math.hypot(dx, dy)
        v = float(ps["speed"])
        moves = d > halt and v > 0.0
        PET_PENDING[pid] = (ps["x"], ps["y"], dx, dy, d, halt, v, moves)
        T = st()["t30"]
        T["pet_steps"] += 1
        if math.isnan(halt) or math.isnan(d):
            T["fail:pet_nan"] += 1
            T["n_fail"] += 1
        if not moves:
            T["pet_steps_no_travel_by_law"] += 1
    return r
gdr.GdRepositionFold.pet_target = _ptt


# ⚑ the ONLY write that reports a pet's MOTION is the motion loop's own `live[pid] = (ps["x"], ps["y"], ...)`, the first
#   such line after the `pet_target(` call in run.py, located here by its source text (not a typed line number). The
#   contact solver's later write of displaced pets (`live[bid] = ...`) and a new pet's spawn write must not resolve a
#   pending motion record (instrument defect found and fixed before the verdict; disclosed in v1.15 § K').
_SRC = open(kr.__file__).read().splitlines()
_i0 = next(i for i, l in enumerate(_SRC) if "gd_engagement.pet_target(pid, ps, (px, py), k)" in l)
MOTION_WRITE_LINE = next(i + 1 for i in range(_i0, len(_SRC))
                         if _SRC[i].strip() == 'live[pid] = (ps["x"], ps["y"], float(ps.get("radius_m", 0.0)))')


class _LiveLog(dict):
    def __setitem__(self, k, val):
        p = (PET_PENDING.pop(k, None) if (CUR["rec"] and sys._getframe(1).f_lineno == MOTION_WRITE_LINE)
             else None)
        if p is not None:
            x0, y0, dx, dy, d, halt, v, moves = p
            T = st()["t30"]
            if not moves:
                T["fail:pet_moved_against_law"] += 1
                T["n_fail"] += 1
            else:
                law = min(v * PERIOD[0], max(0.0, d - halt))
                ex = (x0 + dx / d * law, y0 + dy / d * law)
                if (val[0], val[1]) == ex:
                    T["pet_moved_law_exact"] += 1
                else:
                    tr = math.hypot(val[0] - x0, val[1] - y0)
                    on_ray = abs((val[0] - x0) * dy - (val[1] - y0) * dx) <= 1e-9 * max(1.0, d)
                    if on_ray and tr < law:
                        T["pet_moved_clipped_shorter"] += 1
                    else:
                        T["fail:pet_travel_ne_law"] += 1
                        T["n_fail"] += 1
                        if len(st()["t30_fail_examples"]) < 10:
                            st()["t30_fail_examples"].append(["pet", CUR["wave"], k, val[:2], ex, law])
        super().__setitem__(k, val)


_ogl = kr._geom_live


def _gl(*a, **kw):
    out = _ogl(*a, **kw)
    if CUR["rec"]:
        # pets that did not move this tick leave their PENDING record; clear it at the next occupancy build
        pet_state = a[1] if len(a) > 1 else kw.get("pet_state", {})
        for pid, p in list(PET_PENDING.items()):
            if not p[7]:
                continue
            ps = pet_state.get(pid)
            T = st()["t30"]
            if ps is None or not ps.get("ghost"):
                T["pet_moved_by_law_but_unobserved"] += 1
                continue
            x0, y0, dx, dy, d, halt, v, _m = p
            law = min(v * PERIOD[0], max(0.0, d - halt))
            if (ps["x"], ps["y"]) == (x0 + dx / d * law, y0 + dy / d * law):
                T["pet_moved_law_exact_ghost(next-tick read)"] += 1
            else:
                T["fail:pet_ghost_travel_ne_law"] += 1
                T["n_fail"] += 1
        PET_PENDING.clear()
        return _LiveLog(out)
    return out
kr._geom_live = _gl

# ---------------------------------------------------------------------------------------------- TA-X-29(b) hooks
def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


assert _sha(DATA_DIR / gc.LAPM_TABLE_CSV) == gc.LAPM_TABLE_CSV_SHA256
assert _sha(DATA_DIR / gc.WAVE_PHYS_CSV) == gc.WAVE_PHYS_CSV_SHA256
_PF = defaultdict(set)
with open(DATA_DIR / gc.LAPM_TABLE_CSV, newline="") as fh:
    for r in csv.DictReader(fh):
        v = (r.get("type_modifier_clamped_to_zero") or "").strip()
        if v.startswith("Physical("):
            _PF[r["body_record"]].add(float(v[len("Physical("):-1]))
PF = {k: next(iter(s)) for k, s in _PF.items() if len(s) == 1}
F_LO = min(PF.values())
WPHYS = {}
with open(DATA_DIR / gc.WAVE_PHYS_CSV, newline="") as fh:
    for r in csv.DictReader(fh):
        WPHYS[int(r["wave"])] = float(r["D_offensivePhysicalModifier_pct"]) + float(r["U_offensivePhysicalModifier_pct"])
LAPM = 160


def _law_instant(fold, eng, prof, r, a, om, t):
    m = r.magnitude()
    P = om - 1.0
    if r.damage_type in dv.PHYSICAL_CLAMP_FAMILIES:
        w = int(getattr(eng, "wave", 0) or 0)
        if t == 0.0:
            gt = eng.gmag.terms_for(prof.record) if eng.gmag is not None else None
            f = None
            for rec in (prof.record, getattr(gt, "record", None),
                        (eng.gmag.bio_bridge or {}).get(prof.record) if eng.gmag is not None else None):
                if rec and rec in PF:
                    f = PF[rec]
                    break
            fam = "phys_clamped" if f is not None else "phys_clamped_unmapped(LO)"
            if f is None:
                f = F_LO
            f = f + (WPHYS.get(w, WPHYS[LAPM]) - WPHYS[LAPM]) / 100.0
            return m * max(0.0, a + P + (f - 1.0)), fam
        return m * max(0.0, a + P + WPHYS.get(w, 0.0) / 100.0), "phys_unclamped"
    return m * max(0.0, a + P), "instant_nonphys"


def _law_dot(fold, eng, prof, r, om):
    if r.damage_type in gc.DOT_LEECH_TYPES:
        return r.lo * om, "dot_leech_type"
    gt = eng.gmag.terms_for(prof.record) if eng.gmag is not None else None
    a_dur, fam = 1.0, "dot"
    if gt is not None and eng.gmag.attr_on and getattr(gt, "folds_attr", False):
        d = c11a.duration_attr_mult(gt, r.damage_type)
        if d is None and r.damage_type in gc.CHAOS_AETHER_DOT_TYPES:
            if DIVISOR_DECLARED:
                vi = getattr(gt, "intelligence", None)
                d = 1.0 if vi is None else float(vi) / 200.0 + 1.0
                fam = "dot_chaos_aether_int/200+1"
            else:
                fam = "dot_chaos_aether_1.0"
        a_dur = 1.0 if d is None else d
    tdm = (eng.offense.instant_mult - 1.0) if eng.offense is not None else 0.0
    own = gt.own_add if (gt is not None and eng.gmag.own_on) else 0.0
    return r.lo * max(0.0, a_dur + (om - 1.0) + tdm + own), fam


DIVISOR_DECLARED = True    # the pack's a8: CompositionFold(chaos_aether_dot_divisor=True) (IC7-A-V311-0179 et al.)
_oin = gc.CompositionFold.instant


def _in(self, eng, prof, r, a_mult, om, t_mult):
    v = _oin(self, eng, prof, r, a_mult, om, t_mult)
    if CUR["rec"]:
        T = st()["t29"]
        st()["t29_instances"][f"instant|limb={self.phys_limb.name}|divisor={self.chaos_aether_dot_divisor}"] += 1
        w, fam = _law_instant(self, eng, prof, r, a_mult, om, t_mult)
        T["instant:" + fam] += 1
        T["z5_form_differs"] += int(r.magnitude() * a_mult * om * t_mult != v)
        if w != v or self.phys_limb is not gc.PhysLimb.LO:
            T["FAIL:instant:" + fam] += 1
            if len(st()["t29_fail_examples"]) < 10:
                st()["t29_fail_examples"].append(["instant", fam, prof.record, r.damage_type, v, w])
    return v
gc.CompositionFold.instant = _in
_odt = gc.CompositionFold.dot


def _dt(self, eng, prof, r, om):
    v = _odt(self, eng, prof, r, om)
    if CUR["rec"]:
        T = st()["t29"]
        st()["t29_instances"][f"dot|limb={self.phys_limb.name}|divisor={self.chaos_aether_dot_divisor}"] += 1
        w, fam = _law_dot(self, eng, prof, r, om)
        T["dot:" + fam] += 1
        if w != v or self.chaos_aether_dot_divisor is not DIVISOR_DECLARED:
            T["FAIL:dot:" + fam] += 1
            if len(st()["t29_fail_examples"]) < 10:
                st()["t29_fail_examples"].append(["dot", fam, prof.record, r.damage_type, v, w])
    return v
gc.CompositionFold.dot = _dt

# ---------------------------------------------------------------------------------------------- OBS-1 guard hooks
_real_arm = c11.run_arm


def _arm(runner, a, salt, period):
    CUR["rec"], CUR["salt"] = True, int(salt)
    st()
    try:
        r = _real_arm(runner, a, salt, period)
    finally:
        CUR["rec"] = False
    st()["raised"] = r.get("raised")
    st()["rows_n"] = len(r.get("rows") or [])
    return r
c11.run_arm = _arm
_true_sw = kr.simulate_wave


def _sw(*a, **kw):
    if not CUR["rec"]:
        return _true_sw(*a, **kw)
    w = int(a[0] if a else kw["wave"])
    CUR["wave"] = w
    afo = kw.get("arena_fold")
    if afo is not None and bool(getattr(afo, "armed", False)):
        st()["arena_armed_waves"] += 1
    try:
        r = _true_sw(*a, **kw)
    except Exception as e:
        st()["exceptions"].append({"wave": w, "type": type(e).__name__, "msg": str(e)[:300]})
        raise
    w0 = r.waves[0]
    st()["waves"].append([w, w0.get("outcome"), w0.get("termination_reason")])
    return r
kr.simulate_wave = _sw


def main():
    t0 = time.time()
    period = FP._period()
    PERIOD[0] = period
    res = V311.run_one("V311-FULL", (0, 1, 2, 3, 4), period, arm=ARM)
    out = {"arm": ARM, "constants": {"LADDER_MELEE(pack gr1)": LADDER_MELEE, "TOLERANCE(pack gr1)": TOL,
                                     "PLAYER_RADIUS_M(oracle)": ge.PLAYER_RADIUS_M, "F_LO (min measured)": F_LO,
                                     "gr2_rows": len(GR2), "pet_motion_write_line(run.py)": MOTION_WRITE_LINE},
           "salts": {}}
    stop = []
    for s in range(5):
        x = S[str(s)]
        ws = [w for w, _, _ in x["waves"]]
        oc = x["waves"]
        death = next((w for w, o, _ in oc if o == "player_death"), None)
        complete = (ws == list(range(151, 161)) and x["exceptions"] == [] and x["raised"] is None and x["rows_n"] == 10
                    and all((o, t) in (("cleared", "board_empty"), ("player_death", "player_died")) for _, o, t in oc))
        leg = res["salts"][str(s)]["leg_a_terminal"]
        complete = complete and ((leg.get("wave") == death) if death else (leg.get("wave") is None and oc[-1] == [160, "cleared", "board_empty"]))
        if not complete:
            stop.append(s)
        out["salts"][str(s)] = {"complete": complete, "waves": oc, "leg_a": leg, "raised": x["raised"],
                                "exceptions": x["exceptions"], "rows_n": x["rows_n"],
                                "t30": dict(x["t30"]), "t30_fail_examples": x["t30_fail_examples"],
                                "op_classes": dict(x["op_classes"]),
                                "R-G4-V311 n_bodies_halted_beyond_d_engage": len(x["beyond_bodies"]),
                                "arena_clamp_calls": x["clamp_calls"], "arena_armed_waves": x["arena_armed_waves"],
                                "t29": dict(x["t29"]), "t29_instances": dict(x["t29_instances"]),
                                "t29_fail_examples": x["t29_fail_examples"]}
    out["STOP"] = stop
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(OUT, "w"), indent=1, sort_keys=True, default=str)
    print(f"[v115-audit] {ARM} wall={out['wall_s']}s STOP={stop}", flush=True)
    sys.exit(2 if stop else 0)


if __name__ == "__main__":
    main()
