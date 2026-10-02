#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.14 · THE ORACLE-SIDE INSTRUMENT (gamora, 2026-10-02). READ-ONLY ON THE ENGINE.

Runs THE ORACLE OF RECORD exactly as the pack names it (star-lord MIGRATION § 3, KP-235):
    scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py  run_one("V311-FULL", salts, period, arm)  (+ v3p8.graded_arm)
imported UNMODIFIED, for one arm, and records per (salt, wave) only what prereg v1.14's EXACT rows read. Every hook is a
wrapper that forwards to the oracle's own function and returns its value unchanged; nothing the oracle computes is
replaced. Inertness is PROVEN, not asserted: `bare` mode runs the same composition with no hook installed and the
checker compares the oracle's own per-wave capture rows (c11 `_capture`, the rows `run_one` returns) byte for byte.

Hooks (each read-only; the oracle site each one observes is named):
  * random.Random.__init__ / draw methods  -> per stream `<construction site>|<seed>`: per wave, the draw count and a
    sha256 over (k, method, args, value)                                   [TA-X-27(c), TA-X-01/03/04/05]
  * run.refuses_activation                 -> the wave-local tick k (called once per tick, run.py:2316)
  * channel_policy.ChannelPolicyFold.tick_apply / observe -> verdict kind per tick; already_suppressed per tick
                                                                           [TA-X-08 (2)/(2p), TA-X-14, TA-X-22]
  * control_application.ControlApplicationFold.tick -> the control `channel` switch per tick           [TA-X-08 (2)]
  * wave_engine._weighted_pick / pools_for -> the INCUMBENT roll's keys (still drawn under the line-up fold) [TA-X-16]
  * referent_lineup.ReferentLineupFold.roll -> the FOUGHT roll's points, records, report               [TA-X-16, 25]
  * geometry emitter_xy (both classes)     -> the anchor of every placement, in placement order        [TA-X-17]
  * locomotion.Mover.step + gd_reposition waypoint/pet_target + arena_fold.clamp_body -> the halt operand per step,
    halted-beyond counts under the row's literal operand (2.4) and under the step's own operand        [TA-X-30]
  * threat.load_profiles                   -> the profiles the RUN built (can_swing per spawned record) [TA-X-25]
  * run.simulate_wave (INNERMOST)          -> per wave: outcome, termination, actors, ticks, census
    (actor_state._player_rows, as run.py:5149 passes it), events summary, ledger max radius + digest, arena counters;
    and every exception escaping the true simulate_wave is RECORDED and re-raised (jack-ryan OBS-1, collab 29124a46e)

COMPLETENESS (gandalf/jack-ryan OBS-1 precondition, recorded per salt): the trace carries, per salt, the full wave set
the ladder ran, each wave's `outcome` / `termination_reason`, the exceptions observed, and `raised`. The checker STOPS
on any salt whose ladder is not w151..w160 contiguous, any wave that is neither `cleared` nor `player_death`, or any
observed exception; a leg-A "survival" counts only as w160 `cleared` / `board_empty`.

Usage (from anywhere; chdir to the engine src is done here, as the oracle's docstring requires):
  python3 oracle_trace_v3p11.py hooked <ARM> <out.json>              # salts 0-4 in ONE run_one (the oracle of record)
  python3 oracle_trace_v3p11.py single <ARM> <salt> <out.json>       # one salt (TA-X-01 repeat / batch equivalence)
  python3 oracle_trace_v3p11.py bare   <ARM> <out.json>              # no hook: the inertness reference
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
import time
import traceback
from collections import Counter, defaultdict

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
ENGINE_SRC = "/Users/admin/Games/reincarnated-engine/src"
sys.path.insert(0, ENGINE_SRC)
os.chdir(ENGINE_SRC)

MODE = sys.argv[1]
ARM = sys.argv[2]
assert ARM in ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"), ARM
if MODE == "single":
    SALTS = (int(sys.argv[3]),)
    OUT = sys.argv[4]
else:
    SALTS = (0, 1, 2, 3, 4)
    OUT = sys.argv[3]
HOOKED = MODE in ("hooked", "single")
THIS = os.path.abspath(__file__)

CUR = {"rec": False, "salt": None, "wave": None, "k": 0}
TRACE = {"arm": ARM, "mode": MODE, "salts": {}}
STREAM_LABEL = {}
STREAMS = {}          # salt -> label -> wave -> [n, sha]
CALLSITES = {}        # salt -> draw call site -> wave -> n   (TA-X-27(c), the registry grain)
DEPTH = [0]


def _site():
    for fr in reversed(traceback.extract_stack()[:-2]):
        fn = fr.filename
        if fn.endswith("random.py") or os.path.abspath(fn) == THIS:
            continue
        return f"{fn.split('/')[-1]}:{fr.lineno}"
    return "?"


def _salt_rec():
    return TRACE["salts"].setdefault(str(CUR["salt"]), {"waves": [], "exceptions": [], "raised": None})


# per-wave buffers
BUF = {}


def _reset_buf():
    BUF.clear()
    BUF.update({"obs": {}, "kind": Counter(), "ctrl_channel": set(), "ctrl_any": 0, "picks": [], "pools_calls": [],
                "lineup": None, "anchors": [], "steps": Counter(), "halted_beyond_lit": 0, "halted_beyond_lit_max": 0.0,
                "halted_beyond_lit_bodies": set(), "halted_nonlit_operand": 0, "pet_target_non_none": 0,
                "clamp_beyond_step": 0, "clamp_beyond_lit": 0, "clamp_calls": 0, "wp": {}, "fold_objs": {},
                "interrupts_active": set()})


_reset_buf()

if HOOKED:
    _oinit = random.Random.__init__

    def _init(self, x=None):
        _oinit(self, x)
        xs = x
        if isinstance(x, int) and x >= 2 ** 63:
            xs = x - 2 ** 64
        STREAM_LABEL[id(self)] = f"{_site()}|{xs}"
    random.Random.__init__ = _init

    def _wrap(m):
        orig = getattr(random.Random, m)

        def w(self, *a, **k):
            if DEPTH[0]:
                return orig(self, *a, **k)
            DEPTH[0] += 1
            try:
                v = orig(self, *a, **k)
            finally:
                DEPTH[0] -= 1
            if CUR["rec"]:
                lab = STREAM_LABEL.get(id(self), "?")
                d = STREAMS.setdefault(str(CUR["salt"]), {}).setdefault(lab, {})
                e = d.get(str(CUR["wave"]))
                if e is None:
                    e = d[str(CUR["wave"])] = [0, hashlib.sha256()]
                e[0] += 1
                vv = v if isinstance(v, (int, float, str)) else repr(v)
                e[1].update(repr((CUR["k"], m, a, vv)).encode())
                # the DRAW CALL SITE (the registry's grain, rng_contract V9 / rg1): first frame outside random.py
                fr = sys._getframe(1)
                while fr is not None and (fr.f_code.co_filename.endswith("random.py") or fr.f_code.co_filename == THIS):
                    fr = fr.f_back
                cs = (f"{fr.f_code.co_filename.split('/')[-1]}:{fr.f_code.co_name}:{fr.f_lineno}" if fr else "?")
                cc = CALLSITES.setdefault(str(CUR["salt"]), {}).setdefault(cs, {})
                cc[str(CUR["wave"])] = cc.get(str(CUR["wave"]), 0) + 1
            return v
        setattr(random.Random, m, w)
    for _m in ("random", "randint", "randrange", "uniform", "choice", "choices", "shuffle", "sample", "gauss",
               "normalvariate", "expovariate", "getrandbits", "triangular", "betavariate", "vonmisesvariate"):
        _wrap(_m)

from reincarnated.simulation.kc2 import run as kr  # noqa: E402
from reincarnated.simulation.kc2 import actor_state as asf  # noqa: E402
from reincarnated.simulation.kc2 import channel_policy as cpm  # noqa: E402
from reincarnated.simulation.kc2 import control_application as cam  # noqa: E402
from reincarnated.simulation.kc2 import wave_engine as we  # noqa: E402
from reincarnated.simulation.kc2 import referent_lineup as rl  # noqa: E402
from reincarnated.simulation.kc2 import locomotion as lo  # noqa: E402
from reincarnated.simulation.kc2 import gd_reposition as gdr  # noqa: E402
from reincarnated.simulation.kc2 import arena_fold as af  # noqa: E402
from reincarnated.simulation.kc2 import threat as th  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311  # noqa: E402

PROFILES = []          # every roster dict load_profiles returned inside the recorded run

if HOOKED:
    _ora = kr.refuses_activation

    def _ra(e, c, *a, **k):
        CUR["k"] += 1
        return _ora(e, c, *a, **k)
    kr.refuses_activation = _ra

    _ota = cpm.ChannelPolicyFold.tick_apply

    def _ta(self):
        r = _ota(self)
        if CUR["rec"]:
            BUF["kind"][str(self._verdict_kind)] += 1
            BUF["fold_objs"][id(self)] = self
            ifo = getattr(self, "interrupts_fold", None)
            BUF["interrupts_active"].add(bool(ifo is not None and getattr(ifo, "active", False)))
        return r
    cpm.ChannelPolicyFold.tick_apply = _ta

    _oobs = cpm.ChannelPolicyFold.observe

    def _obs(self, *, run_tick, xy, already_suppressed):
        if CUR["rec"]:
            BUF["obs"][CUR["k"]] = [bool(already_suppressed), bool(self._verdict), self._prev_xy is None,
                                    bool(self._verdict_seq == self.n_observe + 1)]
            BUF["fold_objs"][id(self)] = self
        return _oobs(self, run_tick=run_tick, xy=xy, already_suppressed=already_suppressed)
    cpm.ChannelPolicyFold.observe = _obs

    _octk = cam.ControlApplicationFold.tick

    def _ctk(self):
        out = _octk(self)
        if CUR["rec"]:
            if out.get("channel"):
                BUF["ctrl_channel"].add(CUR["k"])
            if out.get("motion") or out.get("channel") or out.get("actives"):
                BUF["ctrl_any"] += 1
        return out
    cam.ControlApplicationFold.tick = _ctk

    _owp = we._weighted_pick

    def _wp(alts, rng):
        out = _owp(alts, rng)
        if CUR["rec"]:
            BUF["picks"].append(int(alts[0].spawn_point))
        return out
    we._weighted_pick = _wp

    _opf = we.pools_for

    def _pf(wave, *, bonus_spawns_enabled=True):
        out = _opf(wave, bonus_spawns_enabled=bonus_spawns_enabled)
        if CUR["rec"]:
            BUF["pools_calls"].append([sys._getframe(1).f_code.co_name, int(wave), bool(bonus_spawns_enabled),
                                       sorted(int(k) for k in out.keys())])
        return out
    we.pools_for = _pf
    if hasattr(kr, "pools_for"):
        kr.pools_for = _pf
    rl.we.pools_for = _pf

    _olr = rl.ReferentLineupFold.roll

    def _lr(self, wave, incumbent, **kw):
        out = _olr(self, wave, incumbent, **kw)
        if CUR["rec"]:
            BUF["lineup"] = {
                "incumbent_points": sorted({int(b.spawn_point) for b in incumbent.bodies}),
                "incumbent_n_bodies": len(incumbent.bodies),
                "fought_points": sorted({int(b.spawn_point) for b in out.bodies}),
                "fought_n_bodies": len(out.bodies),
                "fought_records": [[int(b.spawn_point), b.record.rsplit("/", 1)[-1], bool(b.is_champion)]
                                   for b in out.bodies],
                "fold_keys": sorted(int(k) for k in rl.REFERENT_LINEUP.get(int(wave), {}).keys()),
                "returned_incumbent_unchanged": out is incumbent,
                "bonus_spawns_enabled_passed": kw.get("bonus_spawns_enabled"),
                "report": (self.census["waves"].get(str(wave)) or [None])[-1]}
        return out
    rl.ReferentLineupFold.roll = _lr

    _geo_classes = [lo.Geometry] if hasattr(lo, "Geometry") else []
    for _nm in dir(lo):
        _o = getattr(lo, _nm)
        if isinstance(_o, type) and "emitter_xy" in _o.__dict__ and _o not in _geo_classes:
            _geo_classes.append(_o)
    for _nm in dir(we):
        _o = getattr(we, _nm)
        if isinstance(_o, type) and "emitter_xy" in _o.__dict__ and _o not in _geo_classes:
            _geo_classes.append(_o)

    def _mk_ex(orig):
        def _ex(self, spawn_point, tier=None):
            r = orig(self, spawn_point, tier)
            if CUR["rec"] and sys._getframe(1).f_code.co_name == "simulate_wave":
                BUF["anchors"].append([int(spawn_point), tier, float(r[0]), float(r[1]), type(self).__name__])
            return r
        return _ex
    for _c in _geo_classes:
        _c.emitter_xy = _mk_ex(_c.__dict__["emitter_xy"])

    _owpt = gdr.GdRepositionFold.waypoint

    def _wpt(self, aid, xy, player_xy):
        r = _owpt(self, aid, xy, player_xy)
        if CUR["rec"]:
            BUF["wp"][aid] = r is not None
        return r
    gdr.GdRepositionFold.waypoint = _wpt

    _opt = gdr.GdRepositionFold.pet_target

    def _ptt(self, pid, ps, player_xy, tick):
        r = _opt(self, pid, ps, player_xy, tick)
        if CUR["rec"] and r is not None:
            BUF["pet_target_non_none"] += 1
        return r
    gdr.GdRepositionFold.pet_target = _ptt

    STEP = {}
    _ostep = lo.Mover.step

    def _step(self, dt_s, player_xy, **kw):
        pre = self.xy
        to_wp = BUF["wp"].pop(self.actor_id, False) if CUR["rec"] else False
        out = _ostep(self, dt_s, player_xy, **kw)
        if CUR["rec"] and kw.get("tick") is not None:
            de = float(kw["d_engage_m"])
            S = BUF["steps"]
            S["n_steps"] += 1
            S["op=2.4" if de == 2.4 else ("op=0" if de == 0.0 else "op=other")] += 1
            pursuit = (bool(self.mech_is_player_target_step) and not bool(self.alert_hold_active_step)
                       and not bool(self.mech_hold_active_step) and not to_wp
                       and not bool(getattr(self, "emerge_hold_active_step", False)))
            if to_wp:
                S["n_waypoint_steps"] += 1
            if bool(getattr(self, "emerge_hold_active_step", False)):
                S["n_emerging_steps"] += 1
            dist = math.hypot(player_xy[0] - pre[0], player_xy[1] - pre[1])
            STEP[self.actor_id] = (pursuit, dist, de)
            if pursuit:
                S["n_pursuit_steps"] += 1
                if bool(self.mech_ring_halt_step):
                    S["n_pursuit_halted"] += 1
                    if de != 2.4:
                        BUF["halted_nonlit_operand"] += 1
                    if dist > 2.4:
                        BUF["halted_beyond_lit"] += 1
                        BUF["halted_beyond_lit_bodies"].add(self.actor_id)
                        BUF["halted_beyond_lit_max"] = max(BUF["halted_beyond_lit_max"], dist)
        return out
    lo.Mover.step = _step

    _ocb = af.ArenaFold.clamp_body

    def _cb(self, mover, pre_xy):
        r = _ocb(self, mover, pre_xy)
        if CUR["rec"]:
            BUF["clamp_calls"] += 1
            if r:
                st = STEP.get(mover.actor_id)
                if st is not None and st[0] and st[1] > st[2]:
                    BUF["clamp_beyond_step"] += 1
                if st is not None and st[0] and st[1] > 2.4:
                    BUF["clamp_beyond_lit"] += 1
        return r
    af.ArenaFold.clamp_body = _cb

    _olp = th.load_profiles

    def _lp(*a, **kw):
        out = _olp(*a, **kw)
        if CUR.get("in_arm"):
            PROFILES.append(out[0])
        return out
    th.load_profiles = _lp

    _real_arm = c11.run_arm

    def _arm(runner, a, salt, period):
        CUR["rec"], CUR["salt"], CUR["in_arm"] = True, int(salt), True
        _salt_rec()
        try:
            r = _real_arm(runner, a, salt, period)
        finally:
            CUR["rec"] = False
        sr = _salt_rec()
        sr["raised"] = r.get("raised")
        sr["leg_a_terminal"] = r.get("leg_a_terminal")
        sr["capture_rows_sha256"] = hashlib.sha256(json.dumps(r.get("rows"), sort_keys=True, default=str)
                                                   .encode()).hexdigest()
        sr["capture_rows_n"] = len(r.get("rows") or [])
        return r
    c11.run_arm = _arm

    # make_runner builds the runner (and load_profiles) BEFORE run_arm: mark it as inside the arm
    _omk = FP.make_runner

    def _mk(*a, **k):
        CUR["in_arm"] = True
        return _omk(*a, **k)
    FP.make_runner = _mk

    _true_sw = kr.simulate_wave

    def _sw(*a, **kw):
        if not CUR["rec"]:
            return _true_sw(*a, **kw)
        w = int(a[0] if a else kw["wave"])
        CUR["wave"], CUR["k"] = w, 0
        _reset_buf()
        afo = kw.get("arena_fold")
        a0 = ((afo.n_wall_clamps_player, afo.n_wall_clamps_body) if afo is not None else None)
        try:
            r = _true_sw(*a, **kw)
        except Exception as e:                       # OBSERVED (OBS-1), then re-raised unchanged
            _salt_rec()["exceptions"].append({"wave": w, "type": type(e).__name__, "msg": str(e)[:300]})
            raise
        w0 = r.waves[0]
        led = getattr(r, "ring_ledger", {}) or {}
        tr = r.tracks
        ticks = []
        for i, rt in enumerate(tr.player_path_tick):
            ticks.append([int(rt), tr.player_path_x[i], tr.player_path_y[i], bool(tr.circle_channel_active[i]),
                          (tr.player_hp[i] if i < len(tr.player_hp) else None)])
        # the oracle's own player census (actor_state._player_rows), as run.py:5149 passes player_dead_tick
        _pr = led.get("player_rows") or []
        died = bool(getattr(r, "player_died", False))
        _pdt = int(_pr[-1][0]) if (died and _pr) else None
        prow = asf._player_rows(led, r.tracks, _pdt, {})
        census = Counter(row[3] for row in prow)
        ts = int(w0["tick_start"])
        rows_k = [int(row[0]) - ts for row in prow]
        # TA-X-08 terms, per census row (k = rt - tick_start), from the fold verdict (OBS) + control switch (CTRL)
        Dset = ("CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE")
        t8 = Counter()
        for row, k in zip(prow, rows_k):
            o = BUF["obs"].get(k)
            rel = bool(o[1]) if o is not None else False
            cc = k in BUF["ctrl_channel"]
            onD, pf = row[3] in Dset, row[3] == "PRE_FIGHT"
            if cc:
                t8["n_control_suppressed"] += 1
                if pf:
                    t8["n_control_suppressed_pre_fight"] += 1
                elif onD and not rel:
                    t8["n_control_suppressed_channelling"] += 1
                elif onD:
                    t8["n_control_suppressed_released"] += 1
            if rel:
                if onD:
                    t8["n_released"] += 1
                elif pf:
                    t8["n_released_pre_fight"] += 1
        align = None
        if BUF["obs"]:
            align = {"observe_ks_equal_census_ks": sorted(BUF["obs"]) == sorted(rows_k),
                     "already_suppressed_equals_ctrl_channel": all(bool(BUF["obs"][k][0]) == (k in BUF["ctrl_channel"])
                                                                   for k in BUF["obs"]),
                     "no_predecessor_iff_pre_fight": all(bool(BUF["obs"].get(k, [0, 0, None, 1])[2]) == (row[3] == "PRE_FIGHT")
                                                         for row, k in zip(prow, rows_k)),
                     "seq_ok": all(v[3] for v in BUF["obs"].values()),
                     "verdict_consistent_with_track": all(
                         (bool(t[3]) == ((not BUF["obs"][t[0] - ts][0]) and (not BUF["obs"][t[0] - ts][1])))
                         for t in ticks if (t[0] - ts) in BUF["obs"])}
        folds = list(BUF["fold_objs"].values())
        rows = r.rows_as_dicts()
        tags = Counter(str(x.get("damage_source_tag")) for x in rows)
        ev_types = Counter(str(x.get("event_type")) for x in rows)
        crit_by_src = Counter()
        for x in rows:
            if x.get("is_crit"):
                s = str(x.get("source_id") or "")
                crit_by_src["player" if s == "player" else ("player_summon" if s.startswith("summon") or
                                                             s.startswith("player_") else "other")] += 1
        ev_sha = hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode()).hexdigest()
        lr = led.get("rows") or []
        live = [x for x in lr if x[2] == 1]
        max_body_r = max((math.hypot(x[4], x[5]) for x in live), default=None)
        led_sha = hashlib.sha256(json.dumps({"rows": lr, "pet_rows": led.get("pet_rows") or [],
                                             "player_rows": _pr}, default=str).encode()).hexdigest()
        arena = None
        if afo is not None:
            arena = {"armed": bool(getattr(afo, "armed", False)), "r_wall_m": getattr(afo, "r_wall_m", None),
                     "clamps_player_delta": afo.n_wall_clamps_player - a0[0],
                     "clamps_body_delta": afo.n_wall_clamps_body - a0[1],
                     "wall_block": getattr(afo, "wall_block", None)}
        cgf = kw.get("channel_gate_fold")
        rec = {
            "wave": w, "tick_start": ts, "tick_end": int(w0["tick_end"]),
            "outcome": w0.get("outcome"), "termination_reason": w0.get("termination_reason"),
            "died": died, "player_hp_end": getattr(r, "player_hp_end", None),
            "kw": {"phase_model": str(kw.get("phase_model")), "arena_fold": afo is not None,
                   "channel_gate_fold": cgf is not None,
                   "channel_gate_fold_armed": (bool(getattr(cgf, "armed", False)) if cgf is not None else None),
                   "lineup_fold": kw.get("lineup_fold") is not None, "mutator_fold": kw.get("mutator_fold") is not None,
                   "gd_engagement": kw.get("gd_engagement") is not None, "pilot_move": kw.get("pilot_move") is not None,
                   "p05_emergence": kw.get("p05_emergence") is not None, "composition": kw.get("composition") is not None,
                   "bonus_spawns_enabled": kw.get("bonus_spawns_enabled")},
            "actors": [[x["actor_id"], x["record_path"], x["spawn_x"], x["spawn_y"], x["spawn_t_s"],
                        x["spawn_point_id"], bool(x["is_champion"])] for x in r.actors],
            "pets": [[p["actor_id"], p["record_path"], p.get("owner_id"), p.get("spawn_tick")] for p in r.pet_actors],
            "anchors": BUF["anchors"],
            "ticks": ticks,
            "census": dict(census), "census_n_rows": len(prow),
            "census_last_row": (list(prow[-1][:4]) if prow else None),
            "ta_x_08": dict(t8), "ctrl_channel_entries": len(BUF["ctrl_channel"]), "ctrl_any_ticks": BUF["ctrl_any"],
            "obs_alignment": align, "fold_present": bool(BUF["obs"]),
            "fold_counters": ([{"n_ticks_released": int(f.n_ticks_released), "n_observe": int(f.n_observe),
                                "n_apply": int(f.n_apply), "n_desync": int(f.n_desync), "armed": bool(f.armed)}
                               for f in folds]),
            "release_kinds": dict(BUF["kind"]), "interrupts_fold_active": sorted(BUF["interrupts_active"]),
            "incumbent_picks": list(BUF["picks"]),
            "pools_calls": BUF["pools_calls"],
            "lineup": BUF["lineup"],
            "events": {"n_rows": len(rows), "types": dict(ev_types), "tags": dict(tags),
                       "crit_by_source_class": dict(crit_by_src), "rows_sha256": ev_sha},
            "ledger": {"max_live_body_radius_m": max_body_r, "n_rows": len(lr), "sha256": led_sha,
                       "d_engage_m": led.get("d_engage_m")},
            "pursuit": {"steps": dict(BUF["steps"]), "halted_beyond_2.4_literal": BUF["halted_beyond_lit"],
                        "halted_beyond_2.4_literal_bodies": len(BUF["halted_beyond_lit_bodies"]),
                        "halted_beyond_2.4_literal_max_m": BUF["halted_beyond_lit_max"],
                        "halted_with_operand_not_2.4": BUF["halted_nonlit_operand"],
                        "pet_steps_aimed_at_reposition_target": BUF["pet_target_non_none"],
                        "arena_clamp_calls": BUF["clamp_calls"],
                        "arena_clamp_stops_beyond_step_operand (R-G4)": BUF["clamp_beyond_step"],
                        "arena_clamp_stops_beyond_2.4_literal": BUF["clamp_beyond_lit"]},
            "arena": arena,
        }
        _salt_rec()["waves"].append(rec)
        return r
    kr.simulate_wave = _sw


def main():
    t0 = time.time()
    period = FP._period()
    res = V311.run_one("V311-FULL", SALTS, period, arm=ARM)
    out = {"arm": ARM, "mode": MODE, "salts_run": list(SALTS), "period": period,
           "oracle": "scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py run_one('V311-FULL', salts, period, arm)",
           "run_one_salts": {}, "wall_s": None}
    for s in SALTS:
        sr = res["salts"][str(s)]
        out["run_one_salts"][str(s)] = {
            "leg_a_terminal": sr["leg_a_terminal"], "raised": sr["raised"],
            "rows_n": len(sr["rows"]),
            "rows_sha256": hashlib.sha256(json.dumps(sr["rows"], sort_keys=True, default=str).encode()).hexdigest(),
            "waves": [[x["wave"], x.get("died"), x.get("t_death_s")] for x in sr["rows"]]}
    out["fold_reports_lineup"] = res["fold_reports"].get("lineup")
    out["fold_reports_mutators"] = res["fold_reports"].get("mutators")
    if HOOKED:
        out["trace"] = TRACE
        out["streams"] = {s: {lab: {w: [e[0], e[1].hexdigest()] for w, e in d.items()} for lab, d in labs.items()}
                          for s, labs in STREAMS.items()}
        out["draw_callsites"] = CALLSITES
        # TA-X-25: can_swing of every record the run spawned, under the loader the RUN built
        sw = {}
        if PROFILES:
            roster = PROFILES[-1]
            spawned = {a[1] for st in TRACE["salts"].values() for wv in st["waves"] for a in wv["actors"]}
            for rec in sorted(spawned):
                p = roster.get(rec) or roster.get(rec.lower())
                if p is None:
                    sw[rec] = None
                    continue
                s_ = p.can_swing
                sw[rec] = bool(s_() if callable(s_) else s_)
        out["can_swing_spawned"] = sw
        out["n_profile_loads_in_arm"] = len(PROFILES)
    out["wall_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, sort_keys=True, default=str)
    print(f"[v114-oracle] {MODE} {ARM} salts={list(SALTS)} wall={out['wall_s']}s "
          f"terms={[out['run_one_salts'][str(s)]['leg_a_terminal'] for s in SALTS]}", flush=True)


if __name__ == "__main__":
    main()
