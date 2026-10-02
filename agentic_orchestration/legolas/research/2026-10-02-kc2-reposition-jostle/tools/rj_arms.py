"""KC2 reposition / contact-jostle counterfactual (legolas, 2026-10-02). ⚑ NOT-A-GRADED-RUN.

Runs gamora's v3.9 oracle of record (`gamora_kc2_play_v3p9_oracle_2026_10_02`, `Folds39("V39-FULL")`, salts 0-19,
the fixed seed-9 line-up, imported UNCHANGED from a read-only `git archive` snapshot of engine 86218701) with the
GD rules decoded in this lap installed IN MEMORY as method patches restored in `finally`. No engine, pack or vendor
file is edited.

The rules (every constant DATAMINED from Game.dll Ed IV / Engine.dll Ed IV / the Ed II database; see README § 1):

  RFA     RepositionForAttack. On each skill completion in Attack, if the re-chosen skill is the SAME skill and still
          CloseEnough, roll rand()%100 < randomRepositionChance (and CanMove) -> RFA: run to the point at
          r_target + r_self from the target along the straight path (GetMoveToPoint(target, skill=0) ->
          GetPointAwayFromGoal(targetPos, r_t + r_s)). Leave on arrival (EndOfPathReached: CloseEnough ? Attack : Pursue)
          or after 2.5 s if CloseEnough. No skill use inside RFA. (Attack::OnUpdate 0x100a1c-0x100abe;
          RFA OnBegin 0x1024b0, OnUpdate 0x1025c0, EndOfPathReached 0x1028b0.)
  SLOT    Attack slots + WaitToAttack + GD's fixed move-to point. A Melee-profile skill requests one of the player's
          6 slots (numAttackSlots 6; SlotMode 0 = one ring) at radius 1.25 + r_m + r_p, world-fixed angles 2*pi*j/6;
          own slot released first, nearest free slot taken, else override an occupant whose (d^2 - e^2)+ to that slot
          exceeds the requester's (e = GetExtents: Small .5 / Medium 1 / Large 1.75); the robbed body gets LostSlot.
          No slot -> WaitToAttack: poll every 333 ms (slot -> Pursue; none -> 50 % RFA), roam every 1 s to a point R
          from a centre R toward the body (R = clamp(d,4,10)/2). Pursue walks to a FIXED point computed at entry
          (slot point; non-melee: r_t + ladder from the target on the line); if it arrives out of range,
          EndOfPathReached -> release slot -> WaitToAttack. (SlotManager 0x460710 et seq.; Pursue OnBegin 0x0ff37d,
          OnUpdate 0x0ff783, EndOfPathReached 0x0ffcf0; WaitToAttack 0x104cf0-0x1055e3.)
  CROWD   Engine.dll crowd depenetration (0x2080a2-0x208215) in place of the oracle's symmetric converging solver:
          an overlapping pair pushes body i away from j by 0.35*pen (averaged over i's eligible overlaps) iff
          Depenetrate(i.state, i.prio, j.state, j.prio): i moving -> j standing, or j moving with prio_j <= prio_i;
          i standing -> only a STANDING j with prio_j > prio_i (= the standing player). Monsters prio 1, player 2.
          Boss/Quest/SuperBoss and forceCollision bodies never move (Monster::CrowdAgentDepenetrate 0x2d70a0).
          The player stays FIXED (the oracle's pilot owns its position; GD would displace a MOVING player).
  PERSIST Attack-state persistence: a body in Attack stands until its swing fires and does not re-test range until
          the skill completes (Attack::OnUpdate fires AttackEnemyOrReturn at timer <= 0 with no range test,
          0x1009e4-0x100a17, 0x101410). ⚑ INFERRED limb: a swing whose target is out of reach at fire time lands no
          damage (it is consumed as a whiff: animation + pause); GD's hit resolution for that case is not decoded.

usage (from <snapshot>/src, PYTHONDONTWRITEBYTECODE=1):
    python3 rj_arms.py run <ARM> <a-b> <out.json>       # salts a..b
    python3 rj_arms.py smoke <ARM>                       # crash-only, salt 0, prints counters only
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Tuple

from reincarnated.simulation.kc2 import geometry as gm
from reincarnated.simulation.kc2 import gd_engagement as ge
from reincarnated.simulation.kc2 import locomotion as lo
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.kc2.swing_pause import rng_for
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_play_v3p8_oracle_2026_10_02 as V8
from reincarnated.simulation.scripts import gamora_kc2_play_v3p9_oracle_2026_10_02 as V9

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = json.load(open(os.path.join(HERE, "..", "results", "gd_tables.json")))
REC = {k: v["II"] for k, v in TAB["records"].items()}
PROFILE = TAB["skill_profile"]

# ── DATAMINED constants ────────────────────────────────────────────────────────────────────────
N_SLOTS = 6                 # malepc01/femalepc01 numAttackSlots (Ed II = Ed IV); Character::Load 0x0422d7
RFA_TIMER_S = 2.5           # RFA OnBegin [esi+0x10] = 0x9c4 ms (0x102590)
WTA_POLL_S = 0.333          # WaitToAttack [esi+0x10] = 0x14d ms (0x104d2e, 0x105032)
WTA_ROAM_S = 1.0            # WaitToAttack [esi+0x2c] = 0x3e8 ms (0x104d39)
WTA_RFA_PCT = 50            # rand()%100 < 0x32 (0x104fd0)
ROAM_MIN, ROAM_MAX = 4.0, 10.0   # StartRoaming clamp (0x105485/0x105491), x 0.5 (0x1054a1)
CROWD_K = 0.35              # Engine.dll 0x20811c
GOAL_R = 0.1                # CrowdAgentParams[0x18] = 0.1 m goal-reached radius (Character::CrowdAgentCreated 0x052855)
STUCK_V = 1.1               # CrowdAgentParams[0x28] = 1.1 m/s: achieved speed below it ... (0x0528c6; crowd 0x208679)
STUCK_S = 0.4               # ... for longer than CrowdAgentParams[0x2c] = 400 ms -> stopped, reason 3 (0x0528cd; 0x2086fd)
RFA_FAIL_RMIN, RFA_FAIL_RMAX = 3.0, 5.0   # RFA::PathFailed random point around self, 3-5 m (0x102b95, 0x102bb0)
PRIO_MONSTER, PRIO_PLAYER = 1, 2     # CrowdAgentCreated: [0x20] = 1; Player inc -> 2 (0x32fb4a)
MELEE_LADDER = 1.25         # gameengine.dbr meleeRange (range audit L5)
LADDER = {"Melee": 1.25, "Short": 4.75, "Moderate": 9.0, "Long": 15.0, "Maximum": 18.0, "Boss": 32.0}
PLAYER_R = ge.PLAYER_RADIUS_M   # 0.32 x 1.05 = 0.336
PLAYER_ID = kr._PLAYER_BODY_ID

ARMS: Dict[str, Dict[str, bool]] = {
    "CTRL":       {},                                   # V39-FULL + the inert RJ instruments (must equal V39-FULL)
    "RJ-RFA":     {"rfa": True},
    "RJ-SLOT":    {"slots": True},
    "RJ-CROWD":   {"crowd": True},
    "RJ-PERSIST": {"persist": True},
    "RJ-CORE":    {"rfa": True, "slots": True, "crowd": True},
    "RJ-FULL":    {"rfa": True, "slots": True, "crowd": True, "persist": True},
}

HB = V9.HBANDS


def _band(d: float) -> Optional[int]:
    for i in range(len(HB) - 1):
        if HB[i] <= d < HB[i + 1]:
            return i
    return None


# ══════════════════════════════════════════════════════════════════════════════════════════════
# shared run-time registry (filled by the inner Mover.step wrapper)
# ══════════════════════════════════════════════════════════════════════════════════════════════
class Reg:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.movers: Dict[str, Any] = {}
        self.last_tick: Dict[str, int] = {}
        self.moved: Dict[str, bool] = {}
        self.player_xy: Optional[Tuple[float, float]] = None
        self.tick: int = -1
        self.pet_prev: Dict[str, Tuple[float, float]] = {}
        self.player_prev: Optional[Tuple[float, float]] = None


REG = Reg()
TEL: Dict[str, Any] = {}


def tel(k: str, v: float = 1.0) -> None:
    TEL[k] = TEL.get(k, 0.0) + v


#: the referent's still threshold: Lap H-2 V_STILL = 50 ground px/s at 122 ground px/m (d1run.py)
V_STILL_M_S = 50.0 / 122.0


def _new_wave_tel() -> Dict[str, Any]:
    return {"mode_band": {m: [[0, 0] for _ in range(len(HB) - 1)] for m in ("A", "P", "R", "W", "x")},
            # ⚑ second instrument (declared before any counterfactual): NET world speed per tick (step + solver
            #   displacement) against the referent's own 50 gpx/s threshold; [moving, still] per band, roster only
            "net_band": [[0, 0] for _ in range(len(HB) - 1)], "_prev": {}}


WTEL: Dict[str, Any] = _new_wave_tel()


# ══════════════════════════════════════════════════════════════════════════════════════════════
# the fold
# ══════════════════════════════════════════════════════════════════════════════════════════════
class RJFold(ge.GdEngagementFold):
    """gamora's `GdEngagementFold` (inherited unchanged) + the decoded rules, each behind its own flag."""

    def __init__(self, rfa: bool = False, slots: bool = False, crowd: bool = False, persist: bool = False) -> None:
        super().__init__()
        self.rfa, self.slots, self.crowd, self.persist = rfa, slots, crowd, persist
        self.any = rfa or slots or persist
        self._eng_id: Optional[int] = None
        self.X: Dict[str, Dict[str, Any]] = {}
        self.occ: List[Optional[str]] = [None] * N_SLOTS
        self.eng: Any = None

    # ── helpers ──────────────────────────────────────────────────────────────────────────────
    def _wave(self, eng: Any) -> None:
        if id(eng) != self._eng_id:
            self._eng_id = id(eng)
            self.X = {}
            self.occ = [None] * N_SLOTS
            self.eng = eng

    def _x(self, aid: str) -> Dict[str, Any]:
        X = self.X.get(aid)
        if X is None:
            X = {"m": None, "wp": None, "kind": None, "lost": False, "t0": 0, "S": None,
                 "wc": None, "wR": None, "wpoll": 0, "wroam": 0}
            self.X[aid] = X
        return X

    def _rec(self, aid: str) -> Optional[str]:
        m = REG.movers.get(aid)
        return m.record if m is not None else None

    def _rbody(self, rec: Optional[str]) -> float:
        r = self._r_body.get(rec) if rec else None
        return r if r is not None else ge.BODY_RADIUS_FALLBACK_M

    def _profile(self, rec: Optional[str], S: Any) -> Optional[str]:
        if S is None:
            return None
        if S.skill == ge.DEFAULT_SKILL:
            return "Melee"
        p = PROFILE.get(f"{rec}|{S.slot}|{S.skill}")
        if p is None:                                  # same skill under another slot name
            for k, v in PROFILE.items():
                if k.startswith(f"{rec}|") and k.endswith(f"|{S.skill}"):
                    p = v
                    break
        if p is None:
            tel("profile_unknown")
            ld = S.reach_m - self._rbody(rec) - PLAYER_R - ge.TOLERANCE_M
            p = "Melee" if abs(ld - MELEE_LADDER) < 0.05 else "Other"
        return p

    @staticmethod
    def _same(a: Any, b: Any) -> bool:
        return a is not None and b is not None and a.skill == b.skill and a.slot == b.slot

    def _pos(self, aid: str) -> Optional[Tuple[float, float]]:
        m = REG.movers.get(aid)
        return m.xy if m is not None else None

    def _alive(self, aid: str) -> bool:
        return REG.last_tick.get(aid, -10) >= REG.tick - 1

    def _roll(self, eng: Any, aid: str, purpose: str, pct: float) -> bool:
        key = f"_rj_{purpose}"
        d = getattr(self, key, None)
        if d is None:
            d = {}
            setattr(self, key, d)
        r = d.get((id(eng), aid))
        if r is None:
            r = rng_for(eng.seed, aid, "rj-" + purpose)
            d[(id(eng), aid)] = r
        return r.randrange(100) < pct

    # ── the slot manager (SlotManager::RequestSlot, SlotMode 0) ──────────────────────────────
    def _request(self, eng: Any, aid: str, S: Any) -> Optional[Tuple[float, float]]:
        tel("slot_requests")
        p = REG.player_xy
        me = self._pos(aid)
        if p is None or me is None:
            return None
        rec = self._rec(aid)
        R = MELEE_LADDER + self._rbody(rec) + PLAYER_R          # GetTargetDistance (no tolerance)
        for j in range(N_SLOTS):                                # CleanupRing: own slot + dead occupants
            o = self.occ[j]
            if o is not None and (o == aid or not self._alive(o)):
                self.occ[j] = None
        P = [(p[0] + R * math.cos(2 * math.pi * j / N_SLOTS), p[1] + R * math.sin(2 * math.pi * j / N_SLOTS))
             for j in range(N_SLOTS)]

        def d2(a: Tuple[float, float], b: Tuple[float, float]) -> float:
            return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        free = sorted((d2(P[j], me), j) for j in range(N_SLOTS) if self.occ[j] is None)
        if free:
            j = free[0][1]
            self.occ[j] = aid
            tel("slot_free")
            return P[j]
        e_me = (REC.get(rec) or {}).get("extents_m", 0.5)
        cand = []
        for j in range(N_SLOTS):
            o = self.occ[j]
            po = self._pos(o)
            if po is None:
                continue
            e_o = (REC.get(self._rec(o)) or {}).get("extents_m", 0.5)
            vr = max(d2(P[j], me) - e_me * e_me, 0.0)
            vo = max(d2(P[j], po) - e_o * e_o, 0.0)
            if vo > vr:
                cand.append((d2(P[j], me), j))
        if cand:
            j = min(cand)[1]
            o = self.occ[j]
            self.occ[j] = aid
            self._x(o)["lost"] = True
            tel("slot_override")
            return P[j]
        tel("slot_none")
        return None

    def _release(self, aid: str) -> None:
        for j in range(N_SLOTS):
            if self.occ[j] == aid:
                self.occ[j] = None

    # ── state entries ────────────────────────────────────────────────────────────────────────
    def _enter_pursue(self, eng: Any, aid: str, A: Dict[str, Any], X: Dict[str, Any], tick: int,
                      why: str) -> None:
        """Pursue::OnBegin: GetMoveToPoint(target, chosen) (slot request for Melee) -> MoveTo a FIXED point."""
        A["mode"] = "P"
        X["m"], X["wp"], X["kind"] = None, None, None
        if not self.slots:
            return
        tel("pursue_entries")
        S = A["S"]
        if S is None:
            return
        rec = self._rec(aid)
        if self._profile(rec, S) == "Melee":
            pt = self._request(eng, aid, S)
            if pt is None:
                self._enter_wta(eng, aid, A, X, tick, "no_slot_" + why)
                return
            X["wp"], X["kind"] = pt, "slot"
        else:
            p, me = REG.player_xy, self._pos(aid)
            if p is None or me is None:
                return
            prof = self._profile(rec, S)
            rr = LADDER.get(prof, S.reach_m - ge.TOLERANCE_M - self._rbody(rec) - PLAYER_R) + PLAYER_R
            dx, dy = me[0] - p[0], me[1] - p[1]
            dd = math.hypot(dx, dy)
            X["wp"] = me if dd <= rr else (p[0] + dx / dd * rr, p[1] + dy / dd * rr)
            X["kind"] = "point"

    def _enter_rfa(self, eng: Any, aid: str, A: Dict[str, Any], X: Dict[str, Any], tick: int, S: Any,
                   why: str) -> None:
        p, me = REG.player_xy, self._pos(aid)
        if p is None or me is None:
            return
        A["mode"], A["S"] = "R", S
        X["m"], X["S"], X["t0"], X["kind"] = "R", S, tick, "rfa"
        rr = PLAYER_R + self._rbody(self._rec(aid))
        dx, dy = me[0] - p[0], me[1] - p[1]
        dd = math.hypot(dx, dy)
        X["wp"] = me if dd <= rr else (p[0] + dx / dd * rr, p[1] + dy / dd * rr)
        tel("rfa_" + why)
        tel("rfa_entries")

    def _enter_wta(self, eng: Any, aid: str, A: Dict[str, Any], X: Dict[str, Any], tick: int, why: str) -> None:
        p, me = REG.player_xy, self._pos(aid)
        if p is None or me is None:
            return
        A["mode"] = "W"
        X["m"], X["t0"] = "W", tick
        dx, dy = me[0] - p[0], me[1] - p[1]
        dd = math.hypot(dx, dy) or 1e-9
        R = min(max(dd, ROAM_MIN), ROAM_MAX) * 0.5
        X["wc"], X["wR"] = (p[0] + dx / dd * R, p[1] + dy / dd * R), R
        tps = eng.ticks_per_s
        X["wpoll"] = tick + max(1, int(round(WTA_POLL_S * tps)))
        X["wroam"] = tick + max(1, int(round(WTA_ROAM_S * tps)))
        self._roam(eng, aid, X)
        tel("wta_" + why.split("_")[0] + ("_" + why.split("_")[1] if why.startswith("no_slot") else ""))
        tel("wta_entries")

    def _roam(self, eng: Any, aid: str, X: Dict[str, Any]) -> None:
        r = getattr(self, "_rj_roam", None)
        if r is None:
            r = {}
            self._rj_roam = r
        g = r.get((id(eng), aid))
        if g is None:
            g = rng_for(eng.seed, aid, "rj-roam")
            r[(id(eng), aid)] = g
        phi = g.uniform(0.0, 2.0 * math.pi)
        c, R = X["wc"], X["wR"]
        X["wp"], X["kind"] = (c[0] + R * math.cos(phi), c[1] + R * math.sin(phi)), "roam"
        tel("wta_roams")

    # ── crowd PathFailed detection (in the oracle's frame) ───────────────────────────────────
    def _active_wp(self, A: Dict[str, Any], X: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        if X["m"] in ("R", "W"):
            return X["wp"]
        if self.slots and A["mode"] == "P":
            return X["wp"]
        return None

    def _pathfail(self, eng: Any, aid: str, A: Dict[str, Any], X: Dict[str, Any], tick: int) -> Optional[str]:
        me = self._pos(aid)
        prev, X["prev"] = X.get("prev"), me
        wp = self._active_wp(A, X)
        if me is None or wp is None or math.hypot(me[0] - wp[0], me[1] - wp[1]) <= GOAL_R:
            X["stuck"] = 0.0
            return None
        dt = 1.0 / eng.ticks_per_s
        m = REG.movers.get(aid)
        if m is None or m.stationary:
            return None
        if prev is not None and m.speed_m_per_s > STUCK_V:
            v = math.hypot(me[0] - prev[0], me[1] - prev[1]) / dt
            X["stuck"] = X.get("stuck", 0.0) + dt if v < STUCK_V else 0.0
            if X["stuck"] > STUCK_S:
                X["stuck"] = 0.0
                return "stuck"
        ux, uy = wp[0] - me[0], wp[1] - me[1]
        L = math.hypot(ux, uy)
        st = min(m.speed_m_per_s * dt, L)
        pr = (me[0] + ux / L * st, me[1] + uy / L * st)
        for j, mj in REG.movers.items():
            if j == aid or not self._alive(j) or mj.ghost:
                continue
            if (math.hypot(mj.xy[0] - wp[0], mj.xy[1] - wp[1]) <= mj.radius_m and
                    math.hypot(pr[0] - mj.xy[0], pr[1] - mj.xy[1]) < m.radius_m + mj.radius_m):
                return "goal"
        return None

    def _repath_random(self, eng: Any, aid: str, X: Dict[str, Any]) -> None:
        r = getattr(self, "_rj_rp", None)
        if r is None:
            r = {}
            self._rj_rp = r
        g = r.get((id(eng), aid))
        if g is None:
            g = rng_for(eng.seed, aid, "rj-repath")
            r[(id(eng), aid)] = g
        me = self._pos(aid)
        phi = g.uniform(0.0, 2.0 * math.pi)
        rho = g.uniform(RFA_FAIL_RMIN, RFA_FAIL_RMAX)
        X["wp"] = (me[0] + rho * math.cos(phi), me[1] + rho * math.sin(phi))

    # ── the opportunity site ─────────────────────────────────────────────────────────────────
    def is_opportunity(self, eng: Any, actor_id: str, prof: Any, tick: int) -> bool:
        self._wave(eng)
        if not self.any:
            return super().is_opportunity(eng, actor_id, prof, tick)
        aid = actor_id
        if eng._emerge_until_k and tick < eng._emerge_until_k.get(aid, -1):
            return False
        A = eng._ge_state.get(aid)
        if A is None:
            A = {"S": None, "mode": "P", "next_choose": -1, "busy_until": -1, "swing_ready": -1,
                 "need": True, "fire": None}
            eng._ge_state[aid] = A
        X = self._x(aid)
        tps = eng.ticks_per_s
        d = eng._ge_dist.get(aid, 1e9)
        rch = max(1, int(math.ceil(ge.RECHOOSE_S * tps - 1e-9)))
        rec = self._rec(aid)

        # ── LostSlot (only the SLOT rule produces it) ─────────────────────────────────────────
        if X["lost"]:
            X["lost"] = False
            tel("lost_slot")
            if X["m"] is None and A["mode"] == "A":            # Attack::LostSlot -> Pursue(ChooseBestSkill)
                A["S"] = self._choose(eng, aid, prof, d, tick)
                self.n_choose += 1
                if A["S"] is not None:
                    self._enter_pursue(eng, aid, A, X, tick, "lost")
                    if X["m"] == "W":
                        return False
            elif X["m"] is None and A["mode"] == "P":          # Pursue::OnUpdate +0x1d -> re-request
                if A["S"] is not None and self._profile(rec, A["S"]) == "Melee":
                    pt = self._request(eng, aid, A["S"])
                    if pt is None:
                        self._enter_wta(eng, aid, A, X, tick, "no_slot_lost")
                        return False
                    X["wp"], X["kind"] = pt, "slot"
            # RFA / WaitToAttack: LostSlot is a no-op (vtable +0x40 = empty)

        if tick < A["busy_until"]:
            if X["m"] is None:
                A["mode"] = "A"
                X["wp"] = None
            return False

        # ── the crowd's PathFailed signals (Engine.dll: stuck 0x208668-0x20873a, goal occupied 0x207da8-0x207f4a
        #    -> state 6 -> ICrowdAgent+0x1c CrowdAgentError -> action idle + controller PathFailed) ───────────────
        pf = self._pathfail(eng, aid, A, X, tick)
        if pf:
            tel("pathfail_" + pf + "_" + (X["m"] or A["mode"]))
            if X["m"] == "R":                                   # RFA::PathFailed: random point 3-5 m from self
                self._repath_random(eng, aid, X)
            elif X["m"] == "W":                                 # WaitToAttack::PathFailed: idle until the next roam
                me = self._pos(aid)
                X["wp"] = me
            elif A["mode"] == "P":                              # Pursue::PathFailed: release slot -> RFA
                self._release(aid)
                if A["S"] is not None:
                    self._enter_rfa(eng, aid, A, X, tick, A["S"], "pursue_pathfail")
                return False

        # ── RepositionForAttack ───────────────────────────────────────────────────────────────
        if X["m"] == "R":
            me = self._pos(aid)
            S = X["S"]
            arrived = me is not None and math.hypot(me[0] - X["wp"][0], me[1] - X["wp"][1]) <= GOAL_R
            if arrived:
                tel("rfa_ticks", tick - X["t0"])
                tel("rfa_exit_arrive")
                X["m"], X["wp"], X["kind"] = None, None, None
                if d <= S.reach_m:
                    A["mode"], A["S"], A["need"] = "A", S, False
                else:
                    A["S"] = self._choose(eng, aid, prof, d, tick)
                    self.n_choose += 1
                    A["need"] = False
                    A["next_choose"] = tick + rch
                    if A["S"] is not None:
                        self._enter_pursue(eng, aid, A, X, tick, "rfa")
                return False
            if tick - X["t0"] >= int(round(RFA_TIMER_S * tps)) and d <= S.reach_m:
                tel("rfa_ticks", tick - X["t0"])
                tel("rfa_exit_timer")
                X["m"], X["wp"], X["kind"] = None, None, None
                A["mode"], A["S"], A["need"] = "A", S, False
            return False

        # ── WaitToAttack ──────────────────────────────────────────────────────────────────────
        if X["m"] == "W":
            tel("wta_ticks")
            if tick >= X["wpoll"]:
                X["wpoll"] = tick + max(1, int(round(WTA_POLL_S * tps)))
                S = self._choose(eng, aid, prof, d, tick)
                self.n_choose += 1
                A["S"] = S
                if S is not None:
                    if self._profile(rec, S) == "Melee":
                        pt = self._request(eng, aid, S)
                        if pt is not None:
                            X["m"] = None
                            A["mode"], A["need"], A["next_choose"] = "P", False, tick + rch
                            X["wp"], X["kind"] = pt, "slot"
                            tel("wta_exit_slot")
                            return False
                        if self._roll(eng, aid, "wta", WTA_RFA_PCT):
                            X["m"] = None
                            self._enter_rfa(eng, aid, A, X, tick, S, "wta")
                            return False
                    else:
                        X["m"] = None
                        A["need"], A["next_choose"] = False, tick + rch
                        self._enter_pursue(eng, aid, A, X, tick, "wta")
                        tel("wta_exit_point")
                        return False
            if tick >= X["wroam"]:
                X["wroam"] = tick + max(1, int(round(WTA_ROAM_S * tps)))
                self._roam(eng, aid, X)
            return False

        # ── Pursue / Attack ───────────────────────────────────────────────────────────────────
        completion = bool(A["need"])
        old_mode, oldS = A["mode"], A["S"]
        if A["need"] or (A["mode"] == "P" and tick >= A["next_choose"]):
            A["S"] = self._choose(eng, aid, prof, d, tick)
            A["need"] = False
            A["next_choose"] = tick + rch
            self.n_choose += 1
            S = A["S"]
            if S is None:
                A["mode"] = "P"
                self.n_no_skill += 1
                return False
            inr = d <= S.reach_m
            if completion and old_mode == "A":
                if inr:
                    if self.rfa and self._same(oldS, S):
                        pct = (REC.get(rec) or {}).get("randomRepositionChance") or 0
                        m = REG.movers.get(aid)
                        if pct > 0 and m is not None and not m.stationary:
                            tel("rfa_rolls")
                            if self._roll(eng, aid, "rfa", pct):
                                self._enter_rfa(eng, aid, A, X, tick, S, "attack")
                                return False
                    A["mode"] = "A"
                else:
                    self._enter_pursue(eng, aid, A, X, tick, "attack")
                    if X["m"] == "W":
                        return False
            elif A["mode"] == "P" and (oldS is None or not self._same(oldS, S)):
                self._enter_pursue(eng, aid, A, X, tick, "rechoose" if oldS is not None else "acquire")
                if X["m"] == "W":
                    return False
        S = A["S"]
        if S is None:
            A["mode"] = "P"
            return False
        # Pursue: the fixed point reached out of range -> EndOfPathReached -> release slot -> WaitToAttack
        if self.slots and A["mode"] == "P" and X["wp"] is not None and d > S.reach_m:
            me = self._pos(aid)
            if me is not None and math.hypot(me[0] - X["wp"][0], me[1] - X["wp"][1]) <= GOAL_R:
                self._release(aid)
                tel("pursue_eop_out_of_range")
                self._enter_wta(eng, aid, A, X, tick, "eop")
                return False
        if self.persist and A["mode"] == "A":
            if eng.swing_pause is not None and tick < A["swing_ready"]:
                return False                                  # stands through the wait, no range test
            if d <= S.reach_m or self._profile(rec, S) != "Melee":
                A["fire"] = S                                 # a ranged skill is launched at the target
                return True
            # ⚑ INFERRED limb: a MELEE swing fired out of reach = a whiff (animation + pause consumed, no damage)
            tel("persist_whiff")
            n = eng.swing_period_ticks(prof)
            A["busy_until"] = tick + n
            A["need"] = True
            if eng.swing_pause is not None:
                pt = eng.swing_pause.pause_ticks(eng, aid, prof.record)
                A["swing_ready"] = tick + (pt if pt is not None else 0)
            return False
        if d <= S.reach_m:
            A["mode"] = "A"
            X["wp"], X["kind"] = None, None
            if eng.swing_pause is not None and tick < A["swing_ready"]:
                return False
            A["fire"] = S
            return True
        if A["mode"] == "A":
            tel("attack_to_pursue_noncompletion")         # the incumbent's re-test during the wait
            A["mode"] = "P"
            self._enter_pursue(eng, aid, A, X, tick, "attack_wait")
            return False
        A["mode"] = "P"
        return False

    def halt_for(self, eng: Optional[Any], actor_id: str, body_xy: Tuple[float, float],
                 player_xy: Tuple[float, float], default_m: float) -> float:
        return super().halt_for(eng, actor_id, body_xy, player_xy, default_m)

    # ── the waypoint the inner step wrapper substitutes ──────────────────────────────────────
    def waypoint(self, aid: str, xy: Tuple[float, float], player_xy: Tuple[float, float]
                 ) -> Optional[Tuple[float, float]]:
        if not self.any:
            return None
        X = self.X.get(aid)
        eng = self.eng
        if X is None or eng is None:
            return None
        A = eng._ge_state.get(aid)
        if A is None:
            return None
        if X["m"] in ("R", "W"):
            return X["wp"] if X["wp"] is not None else xy
        if A["mode"] == "P" and X["wp"] is not None and A["S"] is not None:
            wx, wy = X["wp"]
            ux, uy = wx - xy[0], wy - xy[1]
            L = math.hypot(ux, uy)
            if L < 1e-9:
                return xy
            ux, uy = ux / L, uy / L
            fx, fy = xy[0] - player_xy[0], xy[1] - player_xy[1]
            R = A["S"].reach_m
            b = fx * ux + fy * uy
            c = fx * fx + fy * fy - R * R
            disc = b * b - c
            if c > 0.0 and disc >= 0.0:
                t1 = -b - math.sqrt(disc)
                if 0.0 <= t1 < L:
                    return (xy[0] + ux * t1, xy[1] + uy * t1)   # stop where CloseEnough first holds
            return (wx, wy)
        return None

    def mode_of(self, aid: str) -> str:
        X = self.X.get(aid)
        if X is not None and X["m"] in ("R", "W"):
            return X["m"]
        eng = self.eng
        A = eng._ge_state.get(aid) if eng is not None else None
        return A["mode"] if A is not None and A["mode"] in ("A", "P") else "x"

    def report(self) -> Dict[str, Any]:
        r = super().report()
        r["rj_flags"] = {"rfa": self.rfa, "slots": self.slots, "crowd": self.crowd, "persist": self.persist}
        return r


FOLD: Dict[str, Any] = {"f": None}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# the inner Mover.step wrapper (registry + waypoint substitution + per-mode instrument)
# ══════════════════════════════════════════════════════════════════════════════════════════════
@contextmanager
def rj_patches(fold: RJFold, crowd: bool) -> Iterator[None]:
    real_step = lo.Mover.step
    real_conv, real_jac = gm.separate_overlaps_converging, gm.separate_overlaps

    def step(self: Any, dt_s: float, player_xy: Any, *, d_engage_m: float, **kw: Any) -> Any:
        t = kw.get("tick")
        if t is not None and t != REG.tick:
            REG.tick = t
        REG.movers[self.actor_id] = self
        REG.last_tick[self.actor_id] = REG.tick
        REG.player_xy = (float(player_xy[0]), float(player_xy[1]))
        if ge._is_roster(self.actor_id):
            pv = WTEL["_prev"].get(self.actor_id)
            if pv is not None and t is not None and t == pv[0] + 1 and pv[2] is not None:
                v = math.hypot(self.xy[0] - pv[1][0], self.xy[1] - pv[1][1]) / dt_s
                WTEL["net_band"][pv[2]][1 if v < V_STILL_M_S else 0] += 1
        pre_xy = self.xy                                 # ⚑ fix (post-prereg, disclosed): the net instrument
        wp = fold.waypoint(self.actor_id, self.xy, player_xy)   # must difference PRE-step positions
        if wp is None:
            r = real_step(self, dt_s, player_xy, d_engage_m=d_engage_m, **kw)
        else:
            r = real_step(self, dt_s, wp, d_engage_m=0.0, **kw)
        REG.moved[self.actor_id] = self.last_step_travel_m > 0.0
        if ge._is_roster(self.actor_id):
            dd = math.hypot(self.xy[0] - player_xy[0], self.xy[1] - player_xy[1])
            b = _band(dd)
            if b is not None:
                WTEL["mode_band"][fold.mode_of(self.actor_id)][b][0 if self.last_step_travel_m > 0.0 else 1] += 1
            if t is not None:
                bp = _band(math.hypot(pre_xy[0] - player_xy[0], pre_xy[1] - player_xy[1]))
                WTEL["_prev"][self.actor_id] = (t, pre_xy, bp)
        return r

    def gd_separate(live: Dict[str, Tuple[float, float, float]], *, fixed: Any = (), player_xy: Any = None,
                    **kw: Any) -> Tuple[Dict[str, Tuple[float, float]], Any]:
        ids = sorted(live)
        pxy = (float(player_xy[0]), float(player_xy[1])) if player_xy is not None else None
        p_moving = REG.player_prev is not None and pxy is not None and (
            abs(pxy[0] - REG.player_prev[0]) + abs(pxy[1] - REG.player_prev[1]) > 1e-9)
        REG.player_prev = pxy
        mov: Dict[str, bool] = {}
        prio: Dict[str, int] = {}
        immov: Dict[str, bool] = {}
        for i in ids:
            if i == PLAYER_ID:
                mov[i], prio[i], immov[i] = p_moving, PRIO_PLAYER, True        # the pilot owns the player
                continue
            prio[i] = PRIO_MONSTER
            if i in REG.movers:
                mov[i] = bool(REG.moved.get(i, False))
                immov[i] = bool((REC.get(REG.movers[i].record) or {}).get("immovable", False))
            else:                                                              # a pet: moved since last call?
                pv = REG.pet_prev.get(i)
                mov[i] = pv is not None and (abs(live[i][0] - pv[0]) + abs(live[i][1] - pv[1]) > 1e-9)
                immov[i] = False
        acc: Dict[str, List[float]] = {i: [0.0, 0.0, 0.0] for i in ids}
        npair = 0
        for a in range(len(ids)):
            i = ids[a]
            xi, yi, ri = live[i]
            for b in range(a + 1, len(ids)):
                j = ids[b]
                xj, yj, rj = live[j]
                dx, dy = xi - xj, yi - yj
                dd2 = dx * dx + dy * dy
                R = ri + rj
                if R * R <= dd2:
                    continue
                dd = math.sqrt(dd2)
                npair += 1
                for (u, v, sx, sy) in ((i, j, dx, dy), (j, i, -dx, -dy)):
                    if u in fixed or immov[u]:
                        continue
                    if mov[u]:
                        ok = (not mov[v]) or prio[v] <= prio[u]
                    else:
                        ok = (not mov[v]) and prio[v] > prio[u]
                    if not ok:
                        continue
                    if dd > 0.001:
                        k = CROWD_K * (R - dd) / dd
                        acc[u][0] += k * sx
                        acc[u][1] += k * sy
                    else:
                        acc[u][0] += 0.001 * (1.0 if u < v else -1.0)
                    acc[u][2] += 1.0
        out: Dict[str, Tuple[float, float]] = {}
        travel = 0.0
        nst = nmv = 0
        for i in ids:
            c = acc[i][2]
            if c > 0.0001:
                ddx, ddy = acc[i][0] / c, acc[i][1] / c
                if ddx * ddx + ddy * ddy > 0.0:
                    out[i] = (ddx, ddy)
                    travel += math.hypot(ddx, ddy)
                    if mov[i]:
                        nmv += 1
                    else:
                        nst += 1
        for i in ids:
            if i != PLAYER_ID and i not in REG.movers:
                x, y, _r = live[i]
                o = out.get(i, (0.0, 0.0))
                REG.pet_prev[i] = (x + o[0], y + o[1])
        tel("crowd_ticks")
        tel("crowd_overlap_pairs", npair)
        tel("crowd_displaced_standing", nst)
        tel("crowd_displaced_moving", nmv)
        stats = {"sweeps": 1.0, "projections": float(len(out)), "converged": 1.0,
                 "worst_penetration_before_m": 0.0, "worst_penetration_after_m": 0.0,
                 "pairs_before": float(npair), "pairs_after": float(npair),
                 "pairs_above_tol_before": float(npair), "pairs_above_tol_after": float(npair),
                 "tolerance_m": 0.0, "max_sweeps": 1.0, "travel_m": travel, "max_body_displacement_m": 0.0}
        return out, stats

    def gd_separate_jac(live: Any, *, fixed: Any = (), player_xy: Any = None, **kw: Any) -> Any:
        out, st = gd_separate(live, fixed=fixed, player_xy=player_xy)
        return out, int(st["pairs_before"])

    lo.Mover.step = step                                         # type: ignore[assignment]
    if crowd:
        gm.separate_overlaps_converging = gd_separate            # type: ignore[assignment]
        gm.separate_overlaps = gd_separate_jac                   # type: ignore[assignment]
    try:
        yield
    finally:
        lo.Mover.step = real_step                                # type: ignore[assignment]
        gm.separate_overlaps_converging, gm.separate_overlaps = real_conv, real_jac


# ══════════════════════════════════════════════════════════════════════════════════════════════
# capture + runner (mirrors V9.run_one; the RJ fold replaces the eng fold)
# ══════════════════════════════════════════════════════════════════════════════════════════════
def _cap(r: Any) -> Dict[str, Any]:
    out = V9._cap(r)
    out["rj_mode_band"] = WTEL["mode_band"]
    out["rj_net_band"] = WTEL["net_band"]
    f = FOLD["f"]
    if f is not None:
        f._eng_id, f.X, f.eng, f.occ = None, {}, None, [None] * N_SLOTS
        # ⚑ fix (post-prereg, disclosed): per-wave RNG caches were keyed by id(engine), which CPython can reuse
        #   for the next wave's engine -> run-to-run nondeterminism. Fresh streams per wave, as intended.
        for k in ("_rj_rfa", "_rj_wta", "_rj_roam", "_rj_rp"):
            if hasattr(f, k):
                setattr(f, k, {})
    WTEL.clear()
    WTEL.update(_new_wave_tel())
    REG.reset()
    return out


def run_arm(arm: str, salts: Tuple[int, ...]) -> Dict[str, Any]:
    flags = ARMS[arm]
    TEL.clear()
    WTEL.clear()
    WTEL.update(_new_wave_tel())
    REG.reset()
    period = FP._period()
    f = V9.Folds39("V39-FULL")
    f.eng = RJFold(**flags)
    FOLD["f"] = f.eng
    V8._CUR["em"] = f.base.em
    V9._CUR["f"] = f
    c11._capture = _cap
    try:
        with rj_patches(f.eng, bool(flags.get("crowd"))), V9.mover_observer(), V9.v3p9_oracle(f), \
                V8.graded_arm("M-POL-2"):
            res = FP.run_arm("PW-FOLDED", salts, period)
    finally:
        c11._capture = V8._base_cap
        V8._CUR["em"] = None
        V9._CUR["f"] = None
    res["fold_reports"] = {"eng": f.eng.report(), "hunt": f.hunt.report() if f.hunt is not None else None}
    res["rj_tel"] = dict(sorted(TEL.items()))
    return res


def mode_band_summary(res: Dict[str, Any], salts: Tuple[int, ...]) -> Dict[str, Any]:
    tot = {m: [[0, 0] for _ in range(len(HB) - 1)] for m in ("A", "P", "R", "W", "x")}
    for s in salts:
        for r in res["salts"][str(s)]["rows"]:
            mb = r.get("rj_mode_band")
            if not mb:
                continue
            for m, bands in mb.items():
                for i, (a, b) in enumerate(bands):
                    tot[m][i][0] += a
                    tot[m][i][1] += b
    net = [[0, 0] for _ in range(len(HB) - 1)]
    for s in salts:
        for r in res["salts"][str(s)]["rows"]:
            for i, (a, b) in enumerate(r.get("rj_net_band") or []):
                net[i][0] += a
                net[i][1] += b
    out = {"moving_standing_by_mode_and_band": tot, "net_speed_moving_still_by_band": net,
           "net_still_frac_by_band": [round(b / (a + b), 3) if a + b else None for a, b in net],
           "net_still_2p46_4p92": round((net[4][1] + net[5][1]) / max(1, sum(net[4]) + sum(net[5])), 4)}
    allb = [sum(tot[m][i][0] + tot[m][i][1] for m in tot) for i in range(len(HB) - 1)]
    out["mode_share_2p46_4p92"] = {m: round(sum(tot[m][i][0] + tot[m][i][1] for i in (4, 5)) /
                                            max(1, allb[4] + allb[5]), 4) for m in tot}
    st = sum(tot[m][i][1] for m in tot for i in (4, 5))
    out["roster_still_2p46_4p92"] = round(st / max(1, allb[4] + allb[5]), 4)
    return out


def main() -> None:
    mode = sys.argv[1]
    if mode == "smoke":
        arm = sys.argv[2]
        res = run_arm(arm, (0,))
        print(arm, "RAN; raised:", res["salts"]["0"].get("raised"))
        print("telemetry:", res["rj_tel"])
        return
    arm, sl, outp = sys.argv[2], sys.argv[3], sys.argv[4]
    a, b = (int(x) for x in sl.split("-"))
    salts = tuple(range(a, b + 1))
    t0 = time.time()
    res = run_arm(arm, salts)
    out = {"artifact_class": "NOT-A-GRADED-RUN — legolas reposition/jostle counterfactual on the v3.9 oracle "
                             "(V39-FULL, fixed seed-9 line-up, salts listed). Nothing tuned.",
           "arm": arm, "flags": ARMS[arm], "salts": list(salts),
           "summary": V9.summarise(res, salts), "rj_modes": mode_band_summary(res, salts),
           "rj_tel": res["rj_tel"], "fold_reports": res["fold_reports"], "wall_s": round(time.time() - t0, 1)}
    json.dump(out, open(outp, "w"), indent=1, default=str)
    print(f"[{time.time() - t0:6.0f}s] {arm} done", file=sys.stderr)


if __name__ == "__main__":
    main()
