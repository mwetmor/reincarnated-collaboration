"""gamora 2026-10-01 -- KC2-PLAY KP-199: GD fire-range rule, lethality counterfactual.

NOT-A-GRADED-RUN. READ-ONLY against the oracle (engine 22cd2288; HEAD d2d9ee1f differs from it only by
new JOIN-1 scripts, no oracle file), the pack and the port. Nothing tuned. In-process wraps only.

Harness: gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm("PW-FOLDED") (the M-POL-2 seat, the
x3.17 oracle state) + c11._capture, reused exactly as legolas's p05_counterfactual.py does.

Every patched number comes from legolas's range audit (collab 2eb2ca138):
  range_audit_per_attack.csv  -- keyed (record, slot, pack_skill); cited per patched slot by pack_row_id
  p05_spawn_activation.csv    -- gd_spawn_anim_s and the special slots' Timeout per p05 record

Arms
  A0      control, no patch
  A1      AI-initiated slots: reach_m := gd_use_range_centre_m_HI
  A2      AI-initiated slots: reach_m := gd_use_range_centre_m_LO
  A3      A1 + GD p05 spawn behaviour (spawn animation: no attack, no swing-clock anchor, no pursuit
          travel, body hittable/killable; specials armed at anim end + Timeout)
  A4      AI-initiated slots: reach_m := min(pack reach_m, HI)   (over-range rows clipped only)
  A5      spawn behaviour only, ranges as packed (separates A3 into its two halves)
  A6      AI-initiated slots: reach_m := max(pack reach_m, HI)   (short rows raised only; A4's mirror)
  A1-BAND sensitivity: A1, specials capped by the band max (gd_reference_reach_m column)

"AI-initiated" = the CSV's delivery_class starting "AI-INITIATED" (basic, chain_initial, chain_next,
tree_attack, special1-5). initial / toggled_aura / dying rows are left as packed.
"""
import csv, json, math, sys, time, dataclasses
from collections import defaultdict
from statistics import mean, stdev

from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.kc2 import threat as th
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.kc2 import locomotion as lo

AUD = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-01-kc2-enemy-range-audit/"
REF = 1605.6
W9 = set(range(151, 160))
HALF_W, HALF_H = 12.69, 8.94

ROWS = list(csv.DictReader(open(AUD + "range_audit_per_attack.csv")))
IDX = {(r["record"], r["slot"], r["pack_skill"]): r for r in ROWS}
SPAWN = {}
for r in csv.DictReader(open(AUD + "p05_spawn_activation.csv")):
    anim = r["gd_spawn_anim_s (DATAMINED Ed III .anm header, (frames-1)/30, speed 1.0)"]
    sp = json.loads(r["gd_special_slots [slot,Timeout s,Delay s,Range] (DATAMINED)"] or "[]")
    SPAWN[r["record"]] = {"anim_s": float(anim) if anim else None,
                          "timeout_s": {s[0]: float(s[1]) for s in sp}}


SLOT_PROF = defaultdict(set)   # (record, slot) -> {melee|ranged}, fallback when the row's skill is a child
for _r in ROWS:
    if _r["delivery_class"].startswith("AI-INITIATED"):
        SLOT_PROF[(_r["record"], _r["slot"])].add("melee" if _r["gd_distanceProfile"] in ("", "Melee") else "ranged")


def is_ai(r):
    return r["delivery_class"].startswith("AI-INITIATED")


def src_class(record, tag, skill):
    """melee / ranged by GD distanceProfile of the slot (fixed across arms); else the non-AI class."""
    if tag == "pet":
        return "summon"
    tag = (tag or "").split("@cast")[0]          # deferred-landing rows carry "<slot>@cast<tick>"
    if tag in ("initial", "toggled_aura"):
        return "aura-initial"
    if tag == "dying":
        return "dying"
    r = IDX.get((record, tag, skill))
    if r is None:
        prof = SLOT_PROF.get((record, tag))
        if prof is None or len(prof) != 1:
            return "other/unkeyed"
        return next(iter(prof))
    if not is_ai(r):
        return "aura-initial" if tag in ("initial", "toggled_aura") else ("dying" if tag == "dying" else "other")
    return "melee" if r["gd_distanceProfile"] in ("", "Melee") else "ranged"


ARMS = {"A0": dict(reach=None, spawn=False), "A1": dict(reach="HI", spawn=False),
        "A2": dict(reach="LO", spawn=False), "A3": dict(reach="HI", spawn=True),
        "A4": dict(reach="CLIP", spawn=False), "A5": dict(reach=None, spawn=True),
        "A1-BAND": dict(reach="BAND", spawn=False),
        "A6": dict(reach="RAISE", spawn=False)}


def new_reach(r, mode):
    pk = float(r["pack_reach_m"])
    if mode == "HI":
        return float(r["gd_use_range_centre_m_HI"])
    if mode == "LO":
        return float(r["gd_use_range_centre_m_LO"])
    if mode == "CLIP":
        return min(pk, float(r["gd_use_range_centre_m_HI"]))
    if mode == "RAISE":
        return max(pk, float(r["gd_use_range_centre_m_HI"]))
    if mode == "BAND":
        return float(r["gd_reference_reach_m"])
    raise ValueError(mode)


# ── reach patch on th.load_profiles (installed outside FP.run_arm's own wrapper, so it composes) ──
PATCH_LOG = {}


def patched_profiles(mode, real_lp):
    def lp(**kw):
        ro, pe, rep = real_lp(**kw)
        if mode is None:
            return ro, pe, rep
        n = defaultdict(int)
        def fix(p):
            new = []
            for s in p.slots:
                r = IDX.get((p.record, s.slot, s.skill))
                if r is not None and is_ai(r):
                    v = new_reach(r, mode)
                    n["patched"] += 1
                    n["down" if v < s.reach_m else ("up" if v > s.reach_m else "same")] += 1
                    PATCH_LOG.setdefault(mode, {})[r["pack_row_id"]] = (round(s.reach_m, 3), round(v, 3))
                    s = dataclasses.replace(s, reach_m=v)
                elif r is None:
                    n["unkeyed_slot_left"] += 1
                new.append(s)
            return dataclasses.replace(p, slots=tuple(new))
        ro2 = {k: fix(p) for k, p in ro.items()}
        pe2 = {k: fix(p) for k, p in pe.items()}
        PATCH_LOG.setdefault("_counts", {})[mode] = dict(n)
        return ro2, pe2, rep
    return lp


# ── p05 spawn behaviour ──────────────────────────────────────────────────────────────────────────
class SpawnState:
    def __init__(self, period):
        self.period = period
        self.reset()
        self.tele = defaultdict(int)
        self.missing = set()

    def reset(self):
        self.until_t = {}       # aid -> spawn anim end (s, wave clock)
        self.until_k = {}
        self.arm_k = {}         # aid -> {slot: first tick a special may fire}
        self.spawn_t = {}


def install_spawn(st):
    real_bm, real_sw = kr.build_mover, kr.simulate_wave
    real_step = lo.Mover.step
    real_np, real_io, real_cs = (th.ThreatEngine.note_position, th.ThreatEngine.is_opportunity,
                                 th.ThreatEngine.choose_slot)
    P = st.period

    def bm(**kw):
        m = real_bm(**kw)
        if kw.get("is_ambush"):
            aid, rec, t0 = kw["actor_id"], kw["record"], float(kw["spawn_t_s"])
            sp = SPAWN.get(rec)
            st.tele["p05_bodies"] += 1
            if sp is None or sp["anim_s"] is None:
                st.missing.add(rec)
                st.tele["p05_bodies_no_anim_data"] += 1
                return m
            te = t0 + sp["anim_s"]
            st.until_t[aid] = te
            st.until_k[aid] = int(math.ceil(te / P - 1e-9))
            st.spawn_t[aid] = t0
            st.arm_k[aid] = {s: int(math.ceil((te + to) / P - 1e-9)) for s, to in sp["timeout_s"].items()}
        return m

    def sw(*a, **kw):
        st.reset()
        return real_sw(*a, **kw)

    def step(self, dt_s, player_xy, *, d_engage_m, node_tolerance_m=0.5, tick=None, t_s=None,
             blockers=None):
        te = st.until_t.get(self.actor_id)
        if te is not None and t_s is not None and t_s < te:
            if self.mech_hold_until_t_s is None or self.mech_hold_until_t_s < te:
                self.mech_hold_until_t_s = te
            st.tele["mover_steps_in_anim"] += 1
        return real_step(self, dt_s, player_xy, d_engage_m=d_engage_m,
                         node_tolerance_m=node_tolerance_m, tick=tick, t_s=t_s, blockers=blockers)

    def np_(self, actor_id, prof, dist_m, tick):
        uk = st.until_k.get(actor_id)
        if uk is not None and tick < uk:
            return
        return real_np(self, actor_id, prof, dist_m, tick)

    def io(self, actor_id, prof, tick):
        uk = st.until_k.get(actor_id)
        if uk is not None and tick < uk:
            st.tele["opportunities_suppressed_in_anim"] += 1
            return False
        return real_io(self, actor_id, prof, tick)

    def cs(self, actor_id, prof, dist_m, tick):
        arm = st.arm_k.get(actor_id)
        if arm is not None:
            keep = []
            for s in prof.slots:
                if s.slot.startswith("special"):
                    ak = arm.get(s.slot)
                    if ak is None:
                        st.tele["special_slot_without_timeout_row"] += 1
                    elif tick < ak:
                        st.tele["special_offers_blocked_by_timeout"] += 1
                        continue
                keep.append(s)
            if len(keep) != len(prof.slots):
                prof = dataclasses.replace(prof, slots=tuple(keep))
        return real_cs(self, actor_id, prof, dist_m, tick)

    kr.build_mover, kr.simulate_wave = bm, sw
    lo.Mover.step = step
    th.ThreatEngine.note_position, th.ThreatEngine.is_opportunity, th.ThreatEngine.choose_slot = np_, io, cs

    def restore():
        kr.build_mover, kr.simulate_wave = real_bm, real_sw
        lo.Mover.step = real_step
        th.ThreatEngine.note_position, th.ThreatEngine.is_opportunity, th.ThreatEngine.choose_slot = (
            real_np, real_io, real_cs)
    return restore


# ── capture (extends c11._capture, as legolas's tool does) ───────────────────────────────────────
CUR_SPAWN = {"st": None}
base_cap = c11._capture


def cap(r):
    out = base_cap(r)
    w = r.waves[0]
    t0 = float(w["t_start_s"])
    actors = {a["actor_id"]: a for a in r.actors}
    by_grp, by_cls, by_bin = defaultdict(float), defaultdict(float), defaultdict(float)
    by_grp_cls = defaultdict(float)
    for x in r.rows_as_dicts():
        if x["event_type"] not in ("damage_dealt", "dot_tick") or x["target_id"] != "player":
            continue
        a = float(x["damage_applied"] or 0.0)
        if a <= 0:
            continue
        sid = x["source_id"]
        act = actors.get(sid)
        tag = x["damage_source_tag"]
        if tag == "pet" or act is None:
            grp = "summon/other"
        else:
            grp = "p05" if act.get("spawn_point_id") == "p05" else "ring"
        cls = src_class(act["record_path"] if act else "", tag, x["source_skill_id"]) if act else (
            "summon" if tag == "pet" else "other/unkeyed")
        by_grp[grp] += a
        by_cls[cls] += a
        by_grp_cls[grp + "|" + cls] += a
        if x["event_type"] == "dot_tick" or x["source_x"] is None or x["target_x"] is None:
            b = "dot/no-position"
        else:
            dx = float(x["source_x"]) - float(x["target_x"])
            dy = float(x["source_y"]) - float(x["target_y"])
            d = math.hypot(dx, dy)
            b = ("<=3m" if d <= 3.0 else "3-8.94m" if d <= HALF_H else "8.94-12.69m" if d <= HALF_W
                 else ">12.69m (off-screen half-width)")
        by_bin[b] += a
    out["by_grp"], out["by_cls"], out["by_bin"], out["by_grp_cls"] = (dict(by_grp), dict(by_cls),
                                                                      dict(by_bin), dict(by_grp_cls))
    st = CUR_SPAWN["st"]
    if st is not None:
        # p05 bodies killed before their spawn animation ended (death permitted during SpawnAction)
        n_k = 0
        for x in r.rows_as_dicts():
            if x["event_type"] == "death" and x["target_id"] in st.until_t:
                if float(x["t_s"]) - t0 < st.until_t[x["target_id"]]:
                    n_k += 1
        out["p05_killed_during_anim"] = n_k
    return out


c11._capture = cap


def run(arm, salts, period):
    cfg = ARMS[arm]
    real_lp = th.load_profiles
    th.load_profiles = patched_profiles(cfg["reach"], real_lp)
    restore = None
    st = None
    if cfg["spawn"]:
        st = SpawnState(period)
        restore = install_spawn(st)
    CUR_SPAWN["st"] = st
    try:
        res = FP.run_arm("PW-FOLDED", salts, period)
    finally:
        th.load_profiles = real_lp
        if restore:
            restore()
        CUR_SPAWN["st"] = None
    res["spawn_tele"] = dict(st.tele) if st else None
    res["spawn_missing_records"] = sorted(st.missing) if st else None
    return res


def per_salt(res, s):
    rows = [r for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
    T = sum(r["t_s"] for r in rows)
    L = sum(r["landed"] for r in rows)
    return L / T / REF if T else None


def summarise(res, salts):
    rows = [r for s in salts for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
    T = sum(r["t_s"] for r in rows)
    L = sum(r["landed"] for r in rows)
    agg = {k: defaultdict(float) for k in ("by_grp", "by_cls", "by_bin", "by_grp_cls")}
    for r in rows:
        for k in agg:
            for kk, v in r.get(k, {}).items():
                agg[k][kk] += v
    deaths = {str(s): [r["wave"] for r in res["salts"][str(s)]["rows"] if r["died"]] for s in salts}
    term = {str(s): res["salts"][str(s)]["leg_a_terminal"] for s in salts}
    tw = [d["wave"] for d in term.values() if d.get("wave")]
    out = {"salts": list(salts), "landed_hp_per_s_151_159": round(L / T, 1),
           "ratio_vs_referent": round(L / T / REF, 4), "t_s_151_159": round(T, 2),
           "per_salt_ratio": {str(s): round(per_salt(res, s), 4) for s in salts},
           "leg_a_terminal": term, "mean_leg_a_death_wave": round(mean(tw), 2) if tw else None,
           "n_salts_survive_leg_a": sum(1 for d in term.values() if not d.get("wave")),
           "death_waves_per_salt_legB": deaths,
           "mean_deaths_per_salt_legB_151_160": round(mean(len(v) for v in deaths.values()), 2)}
    for k, d in agg.items():
        tot = sum(d.values())
        out[k + "_hp_per_s"] = {kk: round(v / T, 1) for kk, v in sorted(d.items())}
        out[k + "_share"] = {kk: round(v / tot, 4) for kk, v in sorted(d.items())} if tot else {}
    out["mean_max_landed_1s_per_wave_151_159"] = round(mean(r["max_landed_1s"] for r in rows), 1)
    out["mean_max_landed_0p25s_per_wave_151_159"] = round(mean(r["max_landed_0p25s"] for r in rows), 1)
    dd = [r["t_death_s"] for r in rows if r["died"] and r["t_death_s"] is not None]
    out["n_wave_deaths_151_159"] = len(dd)
    out["mean_t_death_into_wave_s"] = round(mean(dd), 2) if dd else None
    out["p05_killed_during_anim"] = (sum(r.get("p05_killed_during_anim", 0) for r in rows)
                                     if any("p05_killed_during_anim" in r for r in rows) else None)
    return out


T95 = {4: 2.776, 19: 2.093}


def delta(a, b, salts):
    """paired per-salt delta of the ratio, arm a minus arm b, with a t 95% interval."""
    d = [a["per_salt_ratio"][str(s)] - b["per_salt_ratio"][str(s)] for s in salts]
    m = mean(d)
    se = stdev(d) / math.sqrt(len(d)) if len(d) > 1 else float("nan")
    t = T95.get(len(d) - 1, 2.0)
    return {"pooled_ratio_delta": round(a["ratio_vs_referent"] - b["ratio_vs_referent"], 4),
            "pooled_ratio_rel": round(a["ratio_vs_referent"] / b["ratio_vs_referent"] - 1, 4),
            "paired_mean_delta": round(m, 4), "paired_se": round(se, 4),
            "paired_ci95": [round(m - t * se, 4), round(m + t * se, 4)],
            "salt_sd_of_ratio_in_control": round(stdev(b["per_salt_ratio"].values()), 4)}


if __name__ == "__main__":
    salts = tuple(range(int(sys.argv[1]))) if len(sys.argv) > 1 else (0, 1, 2, 3, 4)
    arms = sys.argv[2].split(",") if len(sys.argv) > 2 else list(ARMS)
    outp = sys.argv[3] if len(sys.argv) > 3 else "range_rule_counterfactual_results.json"
    period = FP._period()
    out = {"artifact_class": "NOT-A-GRADED-RUN. gamora diagnostic counterfactual (KC2-PLAY KP-199). "
                             "Oracle/pack/port read-only; in-process wraps only; nothing tuned.",
           "harness": "FP.run_arm('PW-FOLDED') + c11._capture (as legolas p05_counterfactual.py)",
           "oracle_commit": "22cd2288 (run from engine checkout d2d9ee1f: no oracle file differs)",
           "inputs": {"range_audit_per_attack.csv": "collab 2eb2ca138", "p05_spawn_activation.csv": "collab 2eb2ca138"},
           "referent_intake_hp_per_s_151_159": REF, "tick_period_s": period,
           "control_expect": {"salts_0_4_ratio": 3.17, "salts_0_19_ratio": 3.243,
                              "salts_0_4_terminals": [[156, 7.184], [152, 4.408], [155, 7.02], [152, 7.184], [152, 6.122]]},
           "arms": ARMS, "results": {}, "patch_counts": {}, "spawn_telemetry": {}}
    t0 = time.time()
    for a in arms:
        ta = time.time()
        res = run(a, salts, period)
        out["results"][a] = summarise(res, salts)
        if len(salts) > 5:
            out["results"][a + "@salts0-4"] = summarise(res, tuple(s for s in salts if s < 5))
        out["spawn_telemetry"][a] = {"tele": res["spawn_tele"], "missing": res["spawn_missing_records"]}
        out["patch_counts"][a] = PATCH_LOG.get("_counts", {}).get(ARMS[a]["reach"])
        r = out["results"][a]
        print(a, round(time.time() - ta), "s", r["ratio_vs_referent"], r["mean_leg_a_death_wave"],
              file=sys.stderr, flush=True)
        json.dump(out, open(outp, "w"), indent=1, default=str)
    if "A0" in out["results"]:
        out["deltas_vs_A0"] = {}
        for a in arms:
            if a == "A0":
                continue
            out["deltas_vs_A0"][a] = delta(out["results"][a], out["results"]["A0"], salts)
            if len(salts) > 5:
                p5 = tuple(s for s in salts if s < 5)
                out["deltas_vs_A0"][a + "@salts0-4"] = delta(out["results"][a + "@salts0-4"],
                                                             out["results"]["A0@salts0-4"], p5)
    out["patched_rows_by_mode"] = {m: {"n": len(v), "rows": v} for m, v in PATCH_LOG.items() if m != "_counts"}
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(outp, "w"), indent=1, default=str)
    print("wrote", outp, file=sys.stderr)
