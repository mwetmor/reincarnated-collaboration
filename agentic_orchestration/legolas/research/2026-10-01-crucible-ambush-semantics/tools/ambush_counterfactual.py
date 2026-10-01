"""legolas 2026-10-01 -- p05 ProxyAmbush EMERGENCE + STATIONARY-PLANT counterfactual. NOT-A-GRADED-RUN.

READ-ONLY. Imports gamora's C-11a fold-pricing harness (PW-FOLDED = the x3.17 oracle state, v1.8 seat
cell) and the C-11 per-wave capture, unmodified on disk. In-process wraps only; nothing in the engine
is written. Run from `reincarnated-engine/src`:

    python3 <this> <n_salts> <arms,comma,separated> <out.json>

WHAT EACH WRAP ENCODES (and the DATAMINED fact it stands for; see ../README.md):
  * EMERGE-HOLD(D): a p05 (ProxyAmbush) body spawns at +4.0 s exactly as today, but for the first D s
    it neither moves (Mover.step called with dt=0) nor attacks (ThreatEngine.is_opportunity -> False).
    It IS on the board, so the player's disc / secondary streams can damage and kill it.
    -> GD: ProxyAmbush::PlaceNextObject calls Monster::EnableSpawnAnimation (vt+0x318); the
       controller sits in ControllerMonsterStateStartup (ShouldFindEnemy FALSE, OnUpdate empty) until
       the spawn clip's "End" event; the action layer installs SpawnAction (type 19) whose
       permission row gives Attack/Move = PENDING, Die = REPLACE; no invincible/targetable write.
    D = the record's spawn clip length, (frames-1)/30 at speed 1.0 (anm headers). Where the anim
    table carries a speed != 1.0 the composition is UNDECODED (cf. D-1 RESID-D1-1), so two arms:
    SHORT = clip/speed, LONG = clip.
  * PLANT-STATIONARY: livingplant_a01 movers never move (dt=0 always); they still attack when the
    oracle's reach test passes. -> GD: controller_livingplant.dbr is ControllerStationaryMonster;
    its registered Pursue state's OnBegin issues SetState("Attack"|"Idle") and no MoveTo; its
    Move/Return/Flee/FollowLeader/DefendLeader are bound to one state whose OnBegin is
    SetState("Idle"). (A generic MoveTo inside the shared template UseSkill is UNREACHED.)
  * EMERGE-ABSENT(D) (bound, NOT GD): p05 bodies' spawn_t_s += D -- absent, unhittable, idle.
NOT ENCODED (UNKNOWN, named in the README): the AI re-acquisition latency after Startup->Idle (>= 1
AI tick); whether a body's damage AURA runs during the spawn clip; the AlertBeforePursue limb
(off in PW-FOLDED; left off).
"""
import json, math, os, sys, time
from collections import defaultdict
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.kc2 import locomotion as lo
from reincarnated.simulation.kc2 import threat as th
from reincarnated.simulation.kc2 import run as RUN

REF = 1605.6
W9 = set(range(151, 160))
TRUE_A = (-8.245, -5.824)

# DATAMINED spawn-clip lengths, seconds: (SHORT, LONG). Source: anm headers via
# legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json; record->clip via Ed-IV .arz.
D = {
    "aetherialcorruption_b01.dbr": (2.45, 4.9), "aetherialcorruption_b02.dbr": (2.45, 4.9),
    "aetherialcorruption_b03.dbr": (2.45, 4.9),
    "aetherialcorruption_h01.dbr": (2.45, 4.9), "aetherialcorruption_h02.dbr": (2.45, 4.9),
    "aetherialcorruption_h03.dbr": (2.45, 4.9), "aetherialcorruption_h04.dbr": (2.45, 4.9),
    "aetherialcorruption_h05.dbr": (2.45, 4.9),
    "aetherialimp_h01.dbr": (1.533, 1.533), "aetherialimp_h02.dbr": (1.533, 1.533),
    "aetherialimp_h03.dbr": (1.533, 1.533), "aetherialimp_h04.dbr": (1.533, 1.533),
    "aetherialimp_h05.dbr": (1.533, 1.533),
    "chthonianrylok_ekketzul.dbr": (3.5, 3.5),
    "hypporaven_h01.dbr": (1.667, 1.667), "hypporaven_h02.dbr": (1.667, 1.667),
    "hypporaven_h03.dbr": (1.667, 1.667), "hypporaven_h04.dbr": (1.667, 1.667),
    "korvaakmessenger_02.dbr": (1.4, 1.867), "korvaakmessenger_02b.dbr": (1.4, 1.867),
    "livingplant_a01.dbr": (1.5, 1.5),
    "swampgolem_a01.dbr": (3.567, 3.567),
    "wight_h01.dbr": (2.467, 2.833), "wight_h02.dbr": (2.467, 2.833),
    "wight_h03.dbr": (2.467, 2.833), "wight_h04.dbr": (2.467, 2.833),
    "wraith_h01.dbr": (0.867, 0.867), "wraith_h02.dbr": (0.867, 0.867), "wraith_h03.dbr": (0.867, 0.867),
    "wraith_h04.dbr": (0.867, 0.867), "wraith_h05.dbr": (0.867, 0.867),
}
PLANT = "livingplant_a01.dbr"

ARMS = {
    #            emerge     plant   absent   p05_xy
    "PACK":          (None,     False,  None,    None),
    "HOLD-SHORT":    ("SHORT",  False,  None,    None),
    "HOLD-LONG":     ("LONG",   False,  None,    None),
    "PLANT":         (None,     True,   None,    None),
    "GD-SHORT":      ("SHORT",  True,   None,    None),
    "GD-LONG":       ("LONG",   True,   None,    None),
    "GD-LONG@TRUE-A":("LONG",   True,   None,    TRUE_A),
    "ABSENT-LONG":   (None,     False,  "LONG",  None),
}

STATE = {"cfg": ARMS["PACK"], "period": None, "cur": {}, "unmatched": defaultdict(int),
         "n_held": 0, "n_plants": 0, "held_steps": 0, "blocked_opps": 0}

# ---- capture (same census as the p05 position lap, plus p05 first-hit timing) --------------------
base_cap = c11._capture
def cap(r):
    out = base_cap(r)
    w = r.waves[0]; t0 = float(w["t_start_s"])
    actors = {a["actor_id"]: a for a in r.actors}
    by_sp = defaultdict(float); by_sp10 = defaultdict(float); first_hit = {}
    for x in r.rows_as_dicts():
        if x["event_type"] not in ("damage_dealt", "dot_tick") or x["target_id"] != "player":
            continue
        a = float(x["damage_applied"] or 0.0)
        if a <= 0: continue
        act = actors.get(x["source_id"])
        sp = act["spawn_point_id"] if act else "summon/other"
        by_sp[sp] += a
        tt = float(x["t_s"]) - t0
        if tt < 10.0: by_sp10[sp] += a
        first_hit[sp] = min(first_hit.get(sp, 1e9), tt)
    n_sp = defaultdict(int)
    for a in r.actors: n_sp[a.get("spawn_point_id")] += 1
    out["by_sp"] = dict(by_sp); out["by_sp_first10s"] = dict(by_sp10); out["n_bodies_by_sp"] = dict(n_sp)
    out["first_hit_t_by_sp"] = {k: round(v, 3) for k, v in first_hit.items()}
    return out
c11._capture = cap

# ---- build_mover wrap: register emergence windows / plants / absent shift -------------------------
real_build = RUN.build_mover
def build_mover(**kw):
    """Every built mover is registered under its actor_id (actor ids recur across waves and salts,
    so the CURRENT mover for an id is always the most recently built one). The emergence window and
    the plant pin live ON THE MOVER OBJECT, never in an id-keyed table, so they cannot leak to a
    later wave's body that happens to reuse the id."""
    emerge, plant, absent, _xy = STATE["cfg"]
    base = os.path.basename(str(kw.get("record", "")))
    if kw.get("is_ambush") and absent is not None:
        if base in D:
            kw["spawn_t_s"] = float(kw["spawn_t_s"]) + D[base][0 if absent == "SHORT" else 1]
        else:
            STATE["unmatched"][base] += 1
    m = real_build(**kw)
    m._lg_until = None
    m._lg_pinned = False
    if kw.get("is_ambush") and emerge is not None:
        if base in D:
            m._lg_until = float(m.spawn_t_s) + D[base][0 if emerge == "SHORT" else 1]
            STATE["n_held"] += 1
        else:
            STATE["unmatched"][base] += 1
    if plant and base == PLANT:
        m._lg_pinned = True; STATE["n_plants"] += 1
    STATE["cur"][m.actor_id] = m
    return m
RUN.build_mover = build_mover

real_step = lo.Mover.step
def step(self, dt_s, player_xy, **kw):
    t = kw.get("t_s")
    u = getattr(self, "_lg_until", None)
    if getattr(self, "_lg_pinned", False) or (u is not None and t is not None and t < u):
        STATE["held_steps"] += 1
        r = real_step(self, 0.0, player_xy, **kw)
        # the mechanism scan's A-3 guard (reengagement.classify_state) demands a NAMED halt cause
        # for an unmoved, gate-open, out-of-reach body. Label the emergence/pin as the existing
        # hold code (17). Telemetry-only field; nothing in the damage path reads it.
        self.mech_hold_active_step = True
        return r
    return real_step(self, dt_s, player_xy, **kw)
lo.Mover.step = step

real_opp = th.ThreatEngine.is_opportunity
def is_opportunity(self, actor_id, prof, tick):
    m = STATE["cur"].get(actor_id)
    u = getattr(m, "_lg_until", None) if m is not None else None
    if u is not None and tick * STATE["period"] < u:
        STATE["blocked_opps"] += 1
        return False
    return real_opp(self, actor_id, prof, tick)
th.ThreatEngine.is_opportunity = is_opportunity

real_exy = lo.CitedArenaGeometry.emitter_xy

def run(arm, salts, period):
    STATE.update(cfg=ARMS[arm], period=period, cur={}, unmatched=defaultdict(int),
                 n_held=0, n_plants=0, held_steps=0, blocked_opps=0)
    ov = ARMS[arm][3]
    def exy(self, spawn_point, tier=None):
        if ov is not None and int(spawn_point) == 5:
            return ov
        return real_exy(self, spawn_point, tier)
    lo.CitedArenaGeometry.emitter_xy = exy
    try:
        res = FP.run_arm("PW-FOLDED", salts, period)
    finally:
        lo.CitedArenaGeometry.emitter_xy = real_exy
    meta = {"n_p05_bodies_held": STATE["n_held"], "n_plant_movers_pinned": STATE["n_plants"],
            "held_or_pinned_steps": STATE["held_steps"], "blocked_attack_opportunities": STATE["blocked_opps"],
            "unmatched_ambush_records": dict(STATE["unmatched"])}
    return res, meta

def summarise(res, salts):
    rows = [r for s in salts for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
    T = sum(r["t_s"] for r in rows); L = sum(r["landed"] for r in rows)
    sp = defaultdict(float); fh = defaultdict(list)
    pw = defaultdict(lambda: {"n": 0, "t": 0.0, "L": 0.0, "L10": 0.0, "L10_p05": 0.0, "t10": 0.0})
    for r in rows:
        for k, v in r["by_sp"].items(): sp[k] += v
        if "p05" in r.get("first_hit_t_by_sp", {}): fh[r["wave"]].append(r["first_hit_t_by_sp"]["p05"])
        w = pw[r["wave"]]; w["n"] += 1; w["t"] += r["t_s"]; w["L"] += r["landed"]
        w["L10"] += sum(r["by_sp_first10s"].values()); w["L10_p05"] += r["by_sp_first10s"].get("p05", 0.0)
        w["t10"] += min(10.0, r["t_s"])
    L10 = sum(w["L10"] for w in pw.values()); T10 = sum(w["t10"] for w in pw.values())
    deaths = [res["salts"][str(s)]["leg_a_terminal"] for s in salts]
    dw = [d["wave"] for d in deaths if d.get("wave")]
    return {"salts": list(salts), "landed_hp_per_s_151_159": round(L / T, 1), "ratio_vs_referent": round(L / T / REF, 3),
            "landed_total_151_159": round(L, 1), "t_s": round(T, 2),
            "first10s_landed_hp_per_s": round(L10 / T10, 1) if T10 else None,
            "first10s_ratio_vs_referent": round(L10 / T10 / REF, 3) if T10 else None,
            "landed_share_by_sp": {k: round(v / L, 4) for k, v in sorted(sp.items())},
            "p05_landed_hp_per_s": round(sp.get("p05", 0.0) / T, 1),
            "p05_first_hit_t_mean_by_wave": {w: round(sum(v) / len(v), 3) for w, v in sorted(fh.items())},
            "per_wave": {w: {"n_salt_rows": v["n"], "mean_duration_s": round(v["t"] / v["n"], 2),
                             "landed_hp_per_s": round(v["L"] / v["t"], 1) if v["t"] else None,
                             "first10s_hp_per_s": round(v["L10"] / v["t10"], 1) if v["t10"] else None,
                             "first10s_p05_share": round(v["L10_p05"] / v["L10"], 4) if v["L10"] else None}
                         for w, v in sorted(pw.items())},
            "leg_a_terminals": deaths, "mean_death_wave": round(sum(dw) / max(1, len(dw)), 2),
            "n_deaths": len(dw)}

if __name__ == "__main__":
    salts = tuple(range(int(sys.argv[1]))) if len(sys.argv) > 1 else (0, 1, 2, 3, 4)
    arms = sys.argv[2].split(",") if len(sys.argv) > 2 else list(ARMS)
    outp = sys.argv[3] if len(sys.argv) > 3 else "ambush_counterfactual_out.json"
    period = FP._period()
    out = {"artifact_class": "NOT-A-GRADED-RUN. legolas diagnostic counterfactual. Engine read-only; in-process wraps only.",
           "harness": "gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm('PW-FOLDED') + c11._capture",
           "control_expect_salts_0_4": {"landed_hp_per_s": 5090.3, "ratio": 3.17},
           "referent_intake_hp_per_s_151_159": REF, "tick_period_s": period,
           "arms": {k: {"emerge": v[0], "plant_stationary": v[1], "absent": v[2], "p05_xy": v[3]} for k, v in ARMS.items()},
           "emergence_D_s": D, "results": {}, "meta": {}}
    t0 = time.time()
    for a in arms:
        res, meta = run(a, salts, period)
        out["results"][a] = summarise(res, salts)
        if len(salts) > 5:
            out["results"][a + "@salts0-4"] = summarise(res, tuple(s for s in salts if s < 5))
        out["meta"][a] = meta
        print(a, json.dumps({k: out["results"][a][k] for k in ("landed_hp_per_s_151_159", "ratio_vs_referent",
              "first10s_landed_hp_per_s", "t_s", "mean_death_wave", "p05_landed_hp_per_s")}), json.dumps(meta), file=sys.stderr, flush=True)
        json.dump(out, open(outp, "w"), indent=1, default=str)
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(outp, "w"), indent=1, default=str)
    print("wrote", outp, file=sys.stderr)
