"""Counterfactual arms for the residual hunt (harness-only method patches, restored in `finally`).

Every arm is GD's decoded rule implemented in memory on the v3.8 oracle of record, or a declared
diagnostic. Nothing here is tuned toward the referent; every parameter is a DATAMINED value or the
oracle's own constant. RNG: the arms that need draws (swing-pause rolls, special chance rolls in
the AI selection) use DEDICATED generators keyed by (engine seed, actor id), so the oracle's own
THREAT stream is perturbed only through the changed decisions themselves.
"""
from __future__ import annotations

import csv
import dataclasses
import json
import math
import random
import zlib
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional

from reincarnated.simulation.kc2 import c11a_corrections as C11A
from reincarnated.simulation.kc2 import global_magnitude as GM
from reincarnated.simulation.kc2 import locomotion as LO
from reincarnated.simulation.kc2 import threat as TH

from arms import reg, setattr_patch

H = ("/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/"
     "ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad/hunt2")
SP_TABLE = json.load(open(f"{H}/out/swing_pause_table.json"))["records"]
FR_ROWS = list(csv.DictReader(open(f"{H}/eng/data/kc2/kc2_gd_fire_range_v3p8.csv")))
R_BODY: Dict[str, float] = {}
for _r in FR_ROWS:
    if _r["monster_actor_radius_m"] and _r["record"] not in R_BODY:
        R_BODY[_r["record"]] = float(_r["monster_actor_radius_m"]) * float(_r["monster_scale"] or 1.0)
#: GD ladder + tolerance + player radius (range audit L1-L6, L8 HI): Melee 1.25, tol 0.5, player
#: actorRadius 0.32 x scale 1.05 = 0.336.
MELEE_LADDER, TOL, R_PLAYER = 1.25, 0.5, 0.336
DEFAULT_SKILL = "records/skills/default/defaultweaponattack.dbr"
TEL: Dict[str, Any] = {}


def _tel(k: str, n: int = 1) -> None:
    TEL[k] = TEL.get(k, 0) + n


def _pause_ms(record: str) -> Optional[tuple]:
    s = SP_TABLE.get(record) or {}
    lo, hi = s.get("minSwingPause"), s.get("maxSwingPause")
    if lo is None or hi is None:
        return None
    lo, hi = int(float(lo) * 1000.0), int(float(hi) * 1000.0)   # Load: x1000, cvttss2si (truncate)
    return (lo, max(lo, hi))


def _st(engine: Any) -> Dict[str, Any]:
    st = getattr(engine, "_legolas_st", None)
    if st is None:
        st = {"anchor": {}, "last_call": {}, "rng": {}, "dist": {}, "ai": {}}
        object.__setattr__(engine, "_legolas_st", st)
    return st


def _rng(engine: Any, st: Dict[str, Any], actor_id: str, salt: str) -> random.Random:
    k = (actor_id, salt)
    r = st["rng"].get(k)
    if r is None:
        r = random.Random(zlib.crc32(f"{engine.seed}|{actor_id}|{salt}".encode()))
        st["rng"][k] = r
    return r


def _pause_ticks(engine: Any, st: Dict[str, Any], actor_id: str, record: str) -> Optional[int]:
    p = _pause_ms(record)
    if p is None:
        return None
    ms = _rng(engine, st, actor_id, "swing").randint(p[0], p[1])     # IGenerate(min, max) inclusive
    # the timer is decremented by dt each controller update; the swing fires on the first update
    # at which it is <= 0  ->  ceil(ms / tick_ms) ticks after the swing that rolled it.
    return int(math.ceil(ms / 1000.0 * engine.ticks_per_s - 1e-9))


# ══════════════════════════════════════════════════════════════════════════════════════════════
# SP — GD's swing pause (D-3 Rule A; countdown in ControllerMonster::Update unless UseAction;
#      gate in ControllerMonsterStateAttack::OnUpdate). Next swing at max(animation, pause).
# ══════════════════════════════════════════════════════════════════════════════════════════════
@contextmanager
def p_swing_pause() -> Iterator[None]:
    real_iso, real_cs = TH.ThreatEngine.is_opportunity, TH.ThreatEngine.choose_slot

    def iso(self, actor_id, prof, tick):
        st = _st(self)
        if st["last_call"].get(actor_id) == tick:          # the toggled-aura loop: aura cadence
            return real_iso(self, actor_id, prof, tick)    # is NOT swing-gated in GD
        st["last_call"][actor_id] = tick
        a = st["anchor"].get(actor_id)
        if a is None:
            return real_iso(self, actor_id, prof, tick)
        if tick < a:
            return False
        n = self.swing_period_ticks(prof)
        return n > 0 and (tick - a) % n == 0

    def cs(self, actor_id, prof, dist_m, tick):
        s = real_cs(self, actor_id, prof, dist_m, tick)
        if s is not None:
            st = _st(self)
            pt = _pause_ticks(self, st, actor_id, prof.record)
            n = self.swing_period_ticks(prof)
            if pt is None:
                _tel("sp_no_pause_record")
            else:
                st["anchor"][actor_id] = tick + max(n, pt)
                _tel("sp_swings")
                if pt > n:
                    _tel("sp_pause_binds")
        return s

    with setattr_patch(TH.ThreatEngine, "is_opportunity", iso), \
            setattr_patch(TH.ThreatEngine, "choose_slot", cs):
        yield


# ══════════════════════════════════════════════════════════════════════════════════════════════
# DEF — GD's DefaultAttack fallback (ChooseBestSkill tail: Normal [+0x3bc] = attackSkillName,
#       then Default [+0x3b8] = SkillManager::LoadDefaultSkills = defaultweaponattack.dbr,
#       weaponDamagePct 100, no distanceProfile -> Melee). Synthesised ONLY for roster profiles that
#       carry no Normal attack (no `basic` and no `chain_initial` slot). Damage = the body's own
#       natural weapon rows (`prof.weapon_rows`), the oracle's own chain for weapon swings.
# ══════════════════════════════════════════════════════════════════════════════════════════════
def _with_default(prof: Any) -> Any:
    if any(s.slot in ("basic", "chain_initial") for s in prof.slots):
        return prof
    r = R_BODY.get(prof.record)
    if r is None:
        _tel("def_radius_fallback")
        r = 0.5
    slot = TH.AttackSlot(slot="basic", skill=DEFAULT_SKILL, reach_m=MELEE_LADDER + r + R_PLAYER + TOL,
                         cooldown_s=0.0, chance_pct=0.0, rows=(), extent_m=0.0, detonation_s=None,
                         range_band="", extent_carrier="", delay_s=0.0, timeout_s=0.0)
    _tel("def_profiles_added")
    if not prof.weapon_rows:
        _tel("def_profiles_without_weapon_rows")
    return dataclasses.replace(prof, slots=(slot,) + tuple(prof.slots))


@contextmanager
def p_default_attack() -> Iterator[None]:
    real_lp = TH.load_profiles

    def lp(*a, **kw):
        out = real_lp(*a, **kw)
        out = list(out)
        for i in (0, 1):
            if isinstance(out[i], dict):
                out[i] = {k: (_with_default(v) if v is not None and v.swing_period_s is not None else v)
                          for k, v in out[i].items()}
        return tuple(out)

    with setattr_patch(TH, "load_profiles", lp):
        yield


# ══════════════════════════════════════════════════════════════════════════════════════════════
# AI — GD's monster AI selection + pursuit + attack-stand, decoded this leg:
#   ChooseBestSkill(target, false) [Pursue::OnUpdate / Attack::OnUpdate push 0]: specials in slot
#   order (delay/timeout <= 0, chance roll, enabled, IsSkillInProperRange band), else Normal, else
#   Default. Re-chosen every 200 ms in Pursue (timer 0xc8) and after every completed skill.
#   Pursue ends when CloseEnoughToUseSkill(chosen) holds -> Attack; Attack::OnBegin calls Idle()
#   (the body stands); the skill fires (swing pause gating when `sp`); after it completes the body
#   re-chooses and stays (in range) or pursues (out of range). Roster bodies only (pets keep the
#   oracle's rule: they have no Mover). `initial` slots excluded (GD: one self-cast at Startup).
# ══════════════════════════════════════════════════════════════════════════════════════════════
CUR: Dict[str, Any] = {"ai": {}}
SPECIAL_ORDER = ("special1", "special2", "special3", "special4", "special5", "tree_attack")


def _gd_choose(engine, st, actor_id, prof, d, tick):
    tps = engine.ticks_per_s
    for name in SPECIAL_ORDER:
        for s in prof.slots:
            if s.slot != name:
                continue
            key = (actor_id, s.slot)
            if engine._special_arm_k and s.slot.startswith("special") and \
                    tick < engine._special_arm_k.get(key, -1):
                continue
            gate = engine._cooldown_until.get(key)
            if gate is None:
                gate = max(1, int(round(s.delay_s * tps))) if s.delay_s else 0
                engine._cooldown_until[key] = gate
            if tick < gate:
                continue
            if s.chance_pct > 0.0 and _rng(engine, st, actor_id, "choose").uniform(0.0, 100.0) > s.chance_pct:
                continue
            if engine.gd_fire_range is not None and s.slot.startswith("special") and \
                    not engine.gd_fire_range.band_admits(prof.record, s.slot, d):
                continue
            return s
    for name in ("basic", "chain_initial"):
        for s in prof.slots:
            if s.slot == name:
                return s
    return None


def p_ai(sp: bool):
    @contextmanager
    def _p() -> Iterator[None]:
        real_np, real_iso, real_cs = (TH.ThreatEngine.note_position, TH.ThreatEngine.is_opportunity,
                                      TH.ThreatEngine.choose_slot)
        real_step = LO.Mover.step

        def is_roster(aid):
            return "_pet" not in aid

        def np_(self, actor_id, prof, dist_m, tick):
            st = _st(self)
            st["dist"][actor_id] = dist_m
            CUR["ai"] = st["ai"]
            return real_np(self, actor_id, prof, dist_m, tick)

        def iso(self, actor_id, prof, tick):
            st = _st(self)
            if st["last_call"].get(actor_id) == tick:       # toggled-aura loop: unchanged
                return real_iso(self, actor_id, prof, tick)
            st["last_call"][actor_id] = tick
            if not is_roster(actor_id):
                a = st["anchor"].get(actor_id)               # pets: oracle rule (+ swing pause)
                if a is None or not sp:
                    return real_iso(self, actor_id, prof, tick)
                if tick < a:
                    return False
                n = self.swing_period_ticks(prof)
                return n > 0 and (tick - a) % n == 0
            if self._emerge_until_k and tick < self._emerge_until_k.get(actor_id, -1):
                return False
            A = st["ai"].get(actor_id)
            if A is None:
                A = {"S": None, "mode": "P", "next_choose": -1, "busy_until": -1,
                     "swing_ready": -1, "need": True, "fire": None}
                st["ai"][actor_id] = A
            if tick < A["busy_until"]:
                A["mode"] = "A"
                return False
            d = st["dist"].get(actor_id, 1e9)
            if A["need"] or (A["mode"] == "P" and tick >= A["next_choose"]):
                A["S"] = _gd_choose(self, st, actor_id, prof, d, tick)
                A["need"] = False
                A["next_choose"] = tick + max(1, int(math.ceil(0.2 * self.ticks_per_s - 1e-9)))
                _tel("ai_choose")
            S = A["S"]
            if S is None:
                A["mode"] = "P"
                _tel("ai_no_skill")
                return False
            if d <= S.reach_m:
                A["mode"] = "A"
                if sp and tick < A["swing_ready"]:
                    return False
                A["fire"] = S
                return True
            A["mode"] = "P"
            return False

        def cs(self, actor_id, prof, dist_m, tick):
            st = _st(self)
            if not is_roster(actor_id):
                s = real_cs(self, actor_id, prof, dist_m, tick)
                if sp and s is not None:
                    pt = _pause_ticks(self, st, actor_id, prof.record)
                    if pt is not None:
                        st["anchor"][actor_id] = tick + max(self.swing_period_ticks(prof), pt)
                return s
            A = st["ai"].get(actor_id)
            s = A["fire"] if A else None
            if s is None:
                return None
            A["fire"] = None
            key = (actor_id, s.slot)
            cd = s.effective_cooldown_s
            if cd > 0.0:
                self._cooldown_until[key] = tick + max(1, int(round(cd * self.ticks_per_s)))
            n = self.swing_period_ticks(prof)
            A["busy_until"] = tick + n            # stands for the animation (proxy: the swing period)
            A["need"] = True                      # re-choose after the skill completes
            if sp:
                pt = _pause_ticks(self, st, actor_id, prof.record)
                A["swing_ready"] = tick + (pt if pt is not None else 0)
            self.telemetry.n_attack_opportunities += 1
            _tel("ai_fire_" + ("default" if s.skill == DEFAULT_SKILL else s.slot.rstrip("12345")))
            return s

        def step(self, dt_s, player_xy, *, d_engage_m, **kw):
            A = CUR["ai"].get(self.actor_id)
            if A is not None:
                dist = math.hypot(player_xy[0] - self.xy[0], player_xy[1] - self.xy[1])
                if A["mode"] == "A":
                    d_engage_m = dist                 # Attack state: Idle() -> no travel
                    _tel("ai_step_stand")
                elif A["S"] is not None:
                    d_engage_m = A["S"].reach_m * (1.0 - 1e-9)   # pursue to CloseEnough(chosen)
                    _tel("ai_step_pursue")
            return real_step(self, dt_s, player_xy, d_engage_m=d_engage_m, **kw)

        with setattr_patch(TH.ThreatEngine, "note_position", np_), \
                setattr_patch(TH.ThreatEngine, "is_opportunity", iso), \
                setattr_patch(TH.ThreatEngine, "choose_slot", cs), \
                setattr_patch(LO.Mover, "step", step):
            yield
    return _p


# ══════════════════════════════════════════════════════════════════════════════════════════════
# DOTDIV — SlowChaos / SlowAether take magicalDurationDamageEquation (int/200), the same code path
#          as SlowFire.. (DamageAttributeDur_Chaos/_Aether vtable slot 10 =
#          DamageAttributeDurBaseElemental::AddDamageToAccumulator -> CombatAttributeDurDamageElemental).
# ══════════════════════════════════════════════════════════════════════════════════════════════
@contextmanager
def p_dot_divisor() -> Iterator[None]:
    new = dict(C11A.DURATION_EQUATION)
    new["SlowChaos"] = ("intelligence", 200.0, "magicalDurationDamageEquation")
    new["SlowAether"] = ("intelligence", 200.0, "magicalDurationDamageEquation")
    with setattr_patch(C11A, "DURATION_EQUATION", new):
        yield


# ══════════════════════════════════════════════════════════════════════════════════════════════
# C11B — C-11b B (+10 % dex and int, monsterAttributePak at Ultimate / 1 player, DB-SOURCED-EXACT)
#        and A (the record's own charLevel equation; per-record table not committed -> the C-11b
#        mean x1.010 on `a`, applied as x1.010 on the attribute VALUE, DECLARED approximation).
# ══════════════════════════════════════════════════════════════════════════════════════════════
def p_c11b(fb: float = 1.10, fa: float = 1.010):
    @contextmanager
    def _p() -> Iterator[None]:
        real = GM.GlobalMagnitudeFold.terms_for

        def tf(self, record):
            t = real(self, record)
            if t is None:
                return t
            ch = {}
            for f in ("dexterity", "intelligence"):
                v = getattr(t, f, None)
                if v is not None:
                    ch[f] = float(v) * fb * fa
            if not ch:
                return t
            try:
                return dataclasses.replace(t, **ch)
            except Exception:                          # noqa: BLE001
                _tel("c11b_replace_failed")
                return t
        with setattr_patch(GM.GlobalMagnitudeFold, "terms_for", tf):
            yield
    return _p


# ══════════════════════════════════════════════════════════════════════════════════════════════
# ROSTER — diagnostic: the oracle replays ONE roster draw per wave (engine_seed(CONDUCTOR_SEED=9, w))
#          on every salt. This arm re-draws the roster per salt (salt 0 keeps seed 9).
# ══════════════════════════════════════════════════════════════════════════════════════════════
def p_roster():
    @contextmanager
    def _p() -> Iterator[None]:
        from reincarnated.simulation.scripts import gamora_kc2_pm4_i26_spawn_structure_fold_2026_08_16 as I26
        from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
        real_mr = FP.make_runner
        base = I26.CONDUCTOR_SEED

        def mr():
            rc = real_mr()

            def rc2(**kw):
                s = int(kw.get("salt", 0))
                I26.CONDUCTOR_SEED = base if s == 0 else 1000 + s
                try:
                    return rc(**kw)
                finally:
                    I26.CONDUCTOR_SEED = base
            return rc2
        with setattr_patch(FP, "make_runner", mr):
            yield
    return _p


def _stack(*ps):
    return list(ps)


reg("SP", "V38-FULL", "GD swing pause (D-3 Rule A + countdown semantics), incumbent selection/movement",
    p_swing_pause)
reg("DEF", "V38-FULL", "GD DefaultAttack fallback for roster bodies with no Normal attack", p_default_attack)
reg("AIMOVE", "V38-FULL", "GD AI: specials-first ChooseBestSkill + pursue-to-CloseEnough + stand in "
    "Attack + Default fallback; NO swing pause", p_default_attack, p_ai(sp=False))
reg("AIFULL", "V38-FULL", "GD AI in full as decoded: AIMOVE + swing pause", p_default_attack, p_ai(sp=True))
reg("DOTDIV", "V38-FULL", "SlowChaos/SlowAether a_dur = int/200 + 1 (shared elemental DoT path)", p_dot_divisor)
reg("C11B", "V38-FULL", "C-11b B (+10% dex/int pak) x A (mean x1.010, declared)", p_c11b())
reg("C11B-B", "V38-FULL", "C-11b B only (+10% dex/int pak, DB-SOURCED-EXACT)", p_c11b(fa=1.0))
reg("ROSTER", "V38-FULL", "diagnostic: roster re-drawn per salt (salt 0 = seed 9)", p_roster())
reg("ALLDEC", "V38-FULL", "every decoded correction of this leg together: AIFULL + DOTDIV + C11B-B",
    p_default_attack, p_ai(sp=True), p_dot_divisor, p_c11b(fa=1.0))
