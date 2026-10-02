"""POST-REGISTRATION diagnostic arms (NOT in the pre-registration; added after AIFULL showed the
waves stalling). They do not alter any pre-registered arm; arms_extra.py is unchanged.

AIFULL-P: AIFULL + the oracle's OWN pilot rule (KP-205 change 4: JC-G9's collect rule lifted to
K-MILL) with its `stationary` predicate widened to GD's standing bodies (a roster body in the
Attack state stands still by R3, exactly as the plant does). A PILOT MODEL CHOICE, labelled
INFERRED, never a GD decode: GD has no player AI; the referent's pilot is Matt.
"""
from contextlib import contextmanager

from reincarnated.simulation.kc2 import stationary as STN

import arms_extra as AX
from arms import reg, setattr_patch


@contextmanager
def p_pilot_collect_standing():
    real = STN.StationaryFold.mill_superseded

    def ms(self, *, live_movers, any_pet_alive, all_spawned):
        lm = list(live_movers)
        if not all_spawned or any_pet_alive or not lm:
            return real(self, live_movers=lm, any_pet_alive=any_pet_alive, all_spawned=all_spawned)
        ai = AX.CUR["ai"]
        if all(getattr(m, "stationary", False) or (ai.get(m.actor_id, {}).get("mode") == "A")
               for m in lm):
            self.n_mill_superseded_ticks += 1
            AX._tel("pilot_collect_standing_ticks")
            return True
        return real(self, live_movers=lm, any_pet_alive=any_pet_alive, all_spawned=all_spawned)

    with setattr_patch(STN.StationaryFold, "mill_superseded", ms):
        yield


reg("AIFULL-P", "V38-FULL", "POST-REG DIAGNOSTIC: AIFULL + pilot collect rule widened to standing bodies",
    AX.p_default_attack, AX.p_ai(sp=True), p_pilot_collect_standing)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# GATES (POST-REG): D-11's decoded special-slot rules, ARMED in full (both directions):
#   (iii) reuse = max(Delay, skillCooldownTime)  [DOWN]  ·  (iv) first cast gated by Timeout [UP]
#   counted from the actor's own acquisition, one-shot [DOWN]. The annulus (i) stays off (v3.8's
#   GD band already gates specials). Engine fold `gate_model.SpecialGateFold`, unmodified.
# ══════════════════════════════════════════════════════════════════════════════════════════════
@contextmanager
def p_gates():
    from reincarnated.simulation.kc2 import gate_model as GMOD
    from reincarnated.simulation.scripts import gamora_kc2_w1w2_lift_build_2026_08_25 as DRV
    real = DRV.replay

    def rp(*a, **kw):
        kw["special_gate_fold"] = GMOD.SpecialGateFold(arms=GMOD.GateArms(
            conjunction=True, first_cast_field=True, acquisition_anchor=True, annulus=False))
        return real(*a, **kw)
    with setattr_patch(DRV, "replay", rp):
        yield


reg("GATES", "V38-FULL", "POST-REG: D-11 special gates armed (max reuse, Timeout first cast from acquisition)",
    p_gates)
reg("SP+GATES", "V38-FULL", "POST-REG: swing pause + D-11 gates (incumbent movement/selection)",
    AX.p_swing_pause, p_gates)


# ── POST-REG combinations on roster-averaged boards (the ROSTER arm's re-draw, salt 0 = seed 9) ──
reg("SP|R", "V38-FULL", "POST-REG: swing pause on re-drawn rosters", AX.p_swing_pause, AX.p_roster())
reg("SP+C11B|R", "V38-FULL", "POST-REG: swing pause + C-11b B on re-drawn rosters",
    AX.p_swing_pause, AX.p_c11b(fa=1.0), AX.p_roster())
reg("AIFULL|R", "V38-FULL", "POST-REG: GD AI in full on re-drawn rosters",
    AX.p_default_attack, AX.p_ai(sp=True), AX.p_roster())
