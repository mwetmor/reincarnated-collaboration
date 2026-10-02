"""legolas 2026-10-01 -- THE LETHALITY HUNT, Leg 2: GD's damage-COMPOSITION form vs the oracle's.

    ⚑ NOT-A-GRADED-RUN. Diagnostic counterfactual only. Nothing tuned, no arm is a candidate oracle.

READ-ONLY. Imports gamora's C-11a fold-pricing harness (PW-FOLDED = the x3.17 oracle state, v1.8 seat
cell) and the C-11 per-wave capture, unmodified on disk. In-process wraps only, undone in `finally`.
Run from `reincarnated-engine/src` with PYTHONDONTWRITEBYTECODE=1:

    python3 <this> <n_salts> <arms,comma,separated> <out.json>

THE DECODED RULE (Edition-IV x64/Game.dll; see ../README.md section 3):
  * `offensiveTotalDamageModifier` (class DamageAttributeAbsMod_TotalDamageModifier, type 0x3c) is NOT
    applied at a total layer. Its AddModifierToAccumulator @0x1801899d0 pushes ONE inert bookkeeping
    CombatAttributeTotalDamageMod (Execute = empty stub, as C-11a found) PLUS one
    CombatAttributeAbsDamageMod per instant damage type {2 Phys, 4 Pierce, 5 Cold, 6 Fire, 7 Poison,
    8 Lightning, 9 Life, 10 Chaos, 11 Aether} and one CombatAttributeDurDamageMod per DoT type
    {2, 5, 6, 7, 8, 9, 15 Bleed, 10, 11}, each carrying the SAME value.
  * Those are the very objects a per-type modifier (offensiveFireModifier, offensivePhysicalModifier,
    ...; DamageAttributeAbsMod::AddModifierToAccumulator @0x180177360) creates. Their Execute adds the
    value into the damage row's percent field (+0x2c; +0x48 physical / +0x50 pierce on BasePhysical;
    +0x34 on DoT rows).
  * Each row's Process then computes  base*attr_equation(base)/base + |base|*pct/100  -- the percent
    term on the UNSCALED base, ADDED to the attribute-scaled base (C-11a 2.3's form, now shown to hold
    for the WHOLE pool, wave/difficulty/own TotalDamageModifier included), clamped at 0 at the end.
  So GD:      row = base * max(0, a + P/100)        P = sum of every % term that reaches the row's type
     oracle:  row = base * a * (1 + P_T/100) * t    (t = 0 on `physical_clamped` Physical rows)

ARMS (instant = direct/leech kinds; DoT = dot kind; PCL untouched in every arm):
  A0          oracle expression, through the patched function (inertness control)
  G-INST      non-physical instant rows: base*max(0, a + (om-1)); Physical rows as oracle
  G-PHYS-LO   G-INST + Physical rows in the pool: base*max(0, a + (om-1) + (f-1)), f = the body's
              Lap-M type factor where measured (re-based to the wave's survival physical term),
              f_unmapped = -0.44 (the most negative measured factor); unclamped bodies take
              (om-1) + D/U_offensivePhysicalModifier(w)/100 (C-10's fold)
  G-PHYS-HI   as G-PHYS-LO with f_unmapped = -0.23 (the least negative measured factor)
  G-DOT       DoT rows only: base*max(0, a_dur + (M_dot-1) + (M_inst-1) + own), a_dur from
              c11a_corrections.duration_attr_mult (int/200, dex/215); undecoded types a_dur=1.0
  G-FULL-LO   G-PHYS-LO + G-DOT          G-FULL-HI   G-PHYS-HI + G-DOT
DECLARED, NOT ENCODED: crit-damage composition (pthMult + offensiveCritDamageModifier, decoded
additive, crits are 1.2 % of hits); DamageScaleInfo factors; grant om_add on DoT rows; leech rows
take the instant form (TDM's expansion list carries no LifeLeech type; G3 drops leech rows anyway).
"""
import csv, inspect, json, math, os, sys, textwrap, time, hashlib
from collections import defaultdict
from pathlib import Path
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.kc2 import threat as th
from reincarnated.simulation.kc2 import discrete_volley as dv
from reincarnated.simulation.kc2 import c11a_corrections as C11A
from reincarnated.simulation.kc2 import run as RUN

REF = 1605.6
W9 = set(range(151, 160))
ENGINE = Path(th.__file__).resolve().parents[4]
DATA = ENGINE / "data" / "kc2"

# ── substrate the PHYS arms read (DATAMINED via Lap M / Lap I, committed CSVs) ─────────────────
def _phys_factor_map():
    m = defaultdict(set)
    with (DATA / "pm4m_candidate_table.csv").open() as fh:
        for r in csv.DictReader(fh):
            v = (r.get("type_modifier_clamped_to_zero") or "").strip()
            if v.startswith("Physical("):
                m[r["body_record"]].add(float(v[len("Physical("):-1]))
    out = {}
    for k, s in m.items():
        if len(s) != 1:
            raise SystemExit(f"mixed physical type factor within {k}: {s}")
        out[k] = s.pop()
    return out

def _wave_phys():
    o = {}
    with (DATA / "pm4i_wave_damage_modifier.csv").open() as fh:
        for r in csv.DictReader(fh):
            o[int(r["wave"])] = float(r["D_offensivePhysicalModifier_pct"]) + float(r["U_offensivePhysicalModifier_pct"])
    return o

PHYS_F = _phys_factor_map()
WAVE_PHYS = _wave_phys()
LAPM_WAVE = 160          # Lap M composed its factors at wave 160 (method.md 6.3: wave term -21)
F_MIN, F_MAX = min(PHYS_F.values()), max(PHYS_F.values())

ARMS = {
    #             inst   phys    f_unmapped  dot
    "A0":        (False, False,  None,       False),
    "G-INST":    (True,  False,  None,       False),
    "G-PHYS-LO": (True,  True,   F_MIN,      False),
    "G-PHYS-HI": (True,  True,   F_MAX,      False),
    "G-DOT":     (False, False,  None,       True),
    "G-FULL-LO": (True,  True,   F_MIN,      True),
    "G-FULL-HI": (True,  True,   F_MAX,      True),
}
STATE = {"cfg": ARMS["A0"]}
TELE = defaultdict(float)

def _terms(eng, prof):
    return eng.gmag.terms_for(prof.record) if eng.gmag is not None else None

def _factor(eng, prof, gt):
    for rec in (prof.record, getattr(gt, "record", None),
                (eng.gmag.bio_bridge or {}).get(prof.record) if eng.gmag is not None else None):
        if rec and rec in PHYS_F:
            return PHYS_F[rec], True
    return STATE["cfg"][2], False

def _lg_inst(eng, prof, r, a_mult, om, t_mult):
    inst, phys, _fu, _dot = STATE["cfg"]
    m = r.magnitude()
    oracle = m * a_mult * om * t_mult
    is_phys = r.damage_type in dv.PHYSICAL_CLAMP_FAMILIES
    TELE["n_inst_rows"] += 1
    TELE["pre_oracle_inst"] += oracle
    if not inst or (is_phys and not phys):
        TELE["pre_gd_inst"] += oracle
        return oracle
    P = om - 1.0
    if is_phys:
        w = int(getattr(eng, "wave", 0) or 0)
        if t_mult == 0.0:
            gt = _terms(eng, prof)
            f, known = _factor(eng, prof, gt)
            # re-base Lap M's w160 factor to this wave's survival physical term
            f = f + (WAVE_PHYS.get(w, WAVE_PHYS[LAPM_WAVE]) - WAVE_PHYS[LAPM_WAVE]) / 100.0
            v = m * max(0.0, a_mult + P + (f - 1.0))
            TELE["n_phys_clamped_restored"] += 1
            TELE["n_phys_factor_unmapped"] += 0 if known else 1
        else:
            v = m * max(0.0, a_mult + P + WAVE_PHYS.get(w, 0.0) / 100.0)
            TELE["n_phys_unclamped"] += 1
        TELE["pre_gd_phys"] += v
        TELE["pre_oracle_phys"] += oracle
    else:
        v = m * max(0.0, a_mult + P)
    TELE["pre_gd_inst"] += v
    return v

def _lg_dot(eng, prof, r, om):
    _i, _p, _fu, dot = STATE["cfg"]
    oracle = r.lo * om
    TELE["n_dot_rows"] += 1
    TELE["pre_oracle_dot"] += oracle
    if not dot:
        TELE["pre_gd_dot"] += oracle
        return oracle
    if r.damage_type in ("SlowLifeLeach", "SlowManaLeach"):
        TELE["pre_gd_dot"] += oracle      # TDM's DoT expansion carries no leech type; a_dur = 1.0
        return oracle
    gt = _terms(eng, prof)
    a_dur = 1.0
    if gt is not None and eng.gmag.attr_on and getattr(gt, "folds_attr", False):
        d = C11A.duration_attr_mult(gt, r.damage_type)
        a_dur = 1.0 if d is None else d
    tdm = (eng.offense.instant_mult - 1.0) if eng.offense is not None else 0.0
    own = (gt.own_add if (gt is not None and eng.gmag.own_on) else 0.0)
    v = r.lo * max(0.0, a_dur + (om - 1.0) + tdm + own)
    TELE["pre_gd_dot"] += v
    return v

# ── the source transform: two expressions, five sites, nothing else touched ─────────────────────
_SRC = textwrap.dedent(inspect.getsource(th.ThreatEngine.resolve_attack))
_E1 = "r.magnitude() * a_mult * om * t_mult * mult"
_E2 = "r.lo * om * mult"
N1, N2 = _SRC.count(_E1), _SRC.count(_E2)
assert (N1, N2) == (4, 1), (N1, N2)
_NEW = (_SRC.replace(_E1, "_lg_inst(self, prof, r, a_mult, om, t_mult) * mult")
            .replace(_E2, "_lg_dot(self, prof, r, om) * mult"))
_ns = dict(vars(th)); _ns["_lg_inst"] = _lg_inst; _ns["_lg_dot"] = _lg_dot
exec(compile(_NEW, "<legolas-composition-patch>", "exec"), _ns)
PATCHED = _ns["resolve_attack"]
REAL = th.ThreatEngine.resolve_attack

base_cap = c11._capture
def cap(r):
    out = base_cap(r)
    phys = 0.0
    for x in r.rows_as_dicts():
        if x["event_type"] not in ("damage_dealt", "dot_tick") or x["target_id"] != "player":
            continue
        a = float(x["damage_applied"] or 0.0)
        if a > 0 and "armor" in str(x["mitigation_source"] or ""):
            phys += a
    out["landed_physical_tagged"] = round(phys, 1)
    return out

def run(arm, salts, period):
    STATE["cfg"] = ARMS[arm]
    TELE.clear()
    th.ThreatEngine.resolve_attack = PATCHED
    c11._capture = cap
    try:
        res = FP.run_arm("PW-FOLDED", salts, period)
    finally:
        th.ThreatEngine.resolve_attack = REAL
        c11._capture = base_cap
    return res, dict(TELE)

def summarise(res, salts):
    rows = [r for s in salts for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
    T = sum(r["t_s"] for r in rows); L = sum(r["landed"] for r in rows)
    Ld = sum(r.get("landed_dot", 0.0) for r in rows); Lp = sum(r.get("landed_physical_tagged", 0.0) for r in rows)
    per_salt = []
    for s in salts:
        rr = [r for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
        t = sum(r["t_s"] for r in rr)
        per_salt.append(round(sum(r["landed"] for r in rr) / t / REF, 4) if t else None)
    term = [res["salts"][str(s)]["leg_a_terminal"].get("wave") for s in salts]
    tint = [res["salts"][str(s)]["leg_a_terminal"].get("t_into_wave_s") for s in salts]
    legb = [[r["wave"] for r in res["salts"][str(s)]["rows"] if r["died"]] for s in salts]
    pw = {}
    for w in range(151, 161):
        rr = [r for s in salts for r in res["salts"][str(s)]["rows"] if r["wave"] == w]
        t = sum(r["t_s"] for r in rr)
        if t:
            pw[w] = {"landed_hp_per_s": round(sum(r["landed"] for r in rr) / t, 1),
                     "deaths": sum(1 for r in rr if r["died"]), "mean_t_s": round(t / len(rr), 2)}
    return {"salts": list(salts), "landed_hp_per_s_151_159": round(L / T, 1),
            "ratio_vs_referent": round(L / T / REF, 4), "t_s": round(T, 2),
            "per_salt_ratio": per_salt,
            "dot_share_landed": round(Ld / L, 4) if L else None,
            "physical_tagged_share_landed": round(Lp / L, 4) if L else None,
            "leg_a_terminals": term, "leg_a_t_into_wave_s": tint,
            "mean_leg_a_wave": round(sum(x or 161 for x in term) / len(term), 2),
            "n_salts_dying_in_151": sum(1 for x in term if x == 151),
            "n_salts_reaching_160_alive": sum(1 for x in term if x is None or x >= 160),
            "leg_b_deaths_per_salt_151_160": round(sum(len(x) for x in legb) / len(salts), 2),
            "leg_b_death_waves": legb, "per_wave": pw}

def _hash_tree():
    h = hashlib.sha256()
    kc2 = ENGINE / "src" / "reincarnated" / "simulation" / "kc2"
    for p in sorted(list(kc2.glob("*.py")) + [Path(FP.__file__), Path(c11.__file__)]):
        h.update(p.name.encode()); h.update(p.read_bytes())
    for p in sorted(DATA.glob("*.csv")):
        h.update(p.name.encode()); h.update(p.read_bytes())
    return h.hexdigest()

if __name__ == "__main__":
    n = int(sys.argv[1]); arms = sys.argv[2].split(","); outp = sys.argv[3]
    salts = tuple(range(n))
    h0 = _hash_tree()
    runner = c11.make_runner()
    probe = []
    with c11.upn4._overrides(contact_response="separate", geometry_on=True, seek_fold=True, policy=None,
                             kinematics=None, death_continued=False, sink=probe):
        _pr, _pt, _ = runner(salt=0, seat=False)
    period = float(_pr[0].tick_period_s)
    out = {"artifact_class": "NOT-A-GRADED-RUN -- legolas lethality hunt Leg 2, composition counterfactual",
           "harness": "FP.run_arm('PW-FOLDED') + c11._capture, resolve_attack source-patched at 5 sites",
           "control_expect": {"salts_0_4_ratio": 3.1703, "salts_0_19_ratio": 3.2431,
                              "salts_0_4_terminals": [156, 152, 155, 152, 152]},
           "referent_hp_per_s": REF, "phys_factor_map": PHYS_F, "wave_phys_pct": WAVE_PHYS,
           "f_unmapped_LO_HI": [F_MIN, F_MAX], "engine_kc2_and_data_sha256_before": h0,
           "arms": {k: ARMS[k] for k in arms}, "results": {}, "telemetry": {}}
    t0 = time.time()
    for a in arms:
        res, tele = run(a, salts, period)
        out["results"][a] = {"all": summarise(res, salts),
                             "salts_0_4": summarise(res, tuple(s for s in salts if s < 5))}
        out["telemetry"][a] = {k: (round(v, 1) if isinstance(v, float) else v) for k, v in tele.items()}
        s = out["results"][a]["all"]
        print(f"[{time.time()-t0:6.0f}s] {a:10s} x{s['ratio_vs_referent']:.4f} dies151={s['n_salts_dying_in_151']}"
              f" meanA={s['mean_leg_a_wave']} legB/salt={s['leg_b_deaths_per_salt_151_160']}"
              f" dot={s['dot_share_landed']} phys={s['physical_tagged_share_landed']}", file=sys.stderr, flush=True)
    out["engine_kc2_and_data_sha256_after"] = _hash_tree()
    out["engine_unchanged_during_run"] = out["engine_kc2_and_data_sha256_after"] == h0
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(outp, "w"), indent=1, default=str)
