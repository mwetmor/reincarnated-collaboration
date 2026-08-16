#!/usr/bin/env python3
"""
KC2-PM4 · MICRO-LAP AD — THE T LEG.

Authority: R-PM4-75 part 4(ii) — the SECOND licensed referent-functional carve-out:
per-wave referent wave-window duration in referent-clock seconds, waves 151-160, from
Lap AC's own 9-cut segmentation arithmetic (n_observed_instants / observed_fraction / 60).

REFERENT-SIDE ONLY.  This instrument opens no sim artifact, computes no sim quantity, and
places nothing beside a sim number.  Every criterion it applies is fixed in
    agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-microlap-ad-t-leg/prereg.md
committed ALONE at 052008ee before a single number was computed.

Usage:  python3 pm4ad_t_leg_2026_08_16.py <outdir>
"""
import csv
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")

# ── PREREG § 1 — INPUT PINS.  Mismatch => HALT before any content is read. ──────────────────
PINS = {
    "I1_residence": (
        "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/"
        "pm4ac_residence.json",
        "bdf02b2278d2f62d23d590b6a196efd0e4ef181dff8e9992b75f1c805f037f14"),
    "I2_occupancy": (
        "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/"
        "pm4r_contact_occupancy.csv",
        "913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6"),
    "I3_ac_digests": (
        "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/"
        "pm4ac_digests.json",
        "17f10603ecc45faf0002ee4978d198a741484f23f4be17f77ccc69ca2dc6a1e3"),
    "I4_ac_residence_py": (
        "agentic_orchestration/research/scripts/pm4ac_residence_2026_08_16.py",
        "58b7a87c94791f83b497ee9ba23d0defdafd731825c28f7b35f9d12f426c1c07"),
    "I5_ac_lib_py": (
        "agentic_orchestration/research/scripts/pm4ac_lib_2026_08_16.py",
        "4cd928bf265fb15972d1bd7a0a4aed5ab0b6209d1c96d8e4c3de0687b5e26b74"),
    "I6_r_contact_py": (
        "agentic_orchestration/research/scripts/pm4r_contact_2026_08_14.py",
        "8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7"),
    "I7_r_lib_py": (
        "agentic_orchestration/research/scripts/pm4r_lib_2026_08_14.py",
        "630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b"),
    "I8_ac_findings": (
        "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/"
        "pm4ac_findings.md",
        "28cd24aaf05116ea5c363f1ecaf1b02cd51486564b933be7f02cd137b856d4bd"),
    "I9_prereg": (
        "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-microlap-ad-t-leg/prereg.md",
        "93ffe4b9927eb94f100f5c5ba826bfeeafc6f447c52f4d712bf38c00381d7505"),
}

# ── PREREG § 2 / § 4 — FIXED CONSTANTS, none added or altered after the numbers ─────────────
FPS = 60.0                       # pm4ac_lib_2026_08_16.py:83
DT = 1.0 / FPS                   # pm4ac_lib_2026_08_16.py:84
WAVES = tuple(range(151, 161))   # the 10-wave window; 9 internal cuts
RUNG_PRIMARY = "293.6"           # pm4ac_lib_2026_08_16.py:104 — declared before measurement
RUNGS_SECONDARY = ("285.7", "300.0")
RUNG_150 = "150.0"               # touched ONLY for T-invariance (prereg § 2.4 / AC DO-NOT 7)
TOL = 5.0e-3                     # prereg § 4.2, budget-justified a priori
NEAR_MISS_CEIL = 5.0e-2          # prereg § 8(a)/(b) boundary
MIN_N_OBS = 10000                # prereg § 4.3 evaluability floor
FIGHT_T0, FIGHT_T1 = 683.0, 864.0            # pm4r_lib_2026_08_14.py:57
FIGHT_SPAN = FIGHT_T1 - FIGHT_T0             # 181.0 s
SIGMA_BAND = 0.05                            # prereg P-3

# prereg § 4.4.2 — EXPLICIT key assignment.  An unassigned key HALTs.  No default.
RUNG_KEYS_USED = {"R_gpx", "n_intervals", "per_wave"}
RUNG_KEYS_UNUSED = {
    "body_time_all", "censored_fraction", "distinct_bodies_with_ring_time",
    "n_censored_either_side", "n_left_censored", "n_right_censored",
    "n_touching_wave_boundary", "n_with_internal_gap",
    "residence_all", "residence_uncensored_only",
}
PW_KEYS_USED = {"wave", "n_observed_instants", "observed_fraction",
                "total_body_time_s", "n_intervals"}
PW_KEYS_UNUSED = {"n_distinct_bodies", "median_residence_s", "p90_residence_s"}
TOP_KEYS_USED = {"residence", "n_observed_instants"}
TOP_KEYS_UNUSED = {
    "F_AC_1", "F_AC_2", "F_AC_2_robustness", "bound_direction", "emitted",
    "exit_life_bounds", "firewall", "forks", "lap", "leg_A3", "leg_A3b",
    "n_monster_plate_rows", "n_player_plate_rows", "n_tracked_plate_instants",
    "n_tracks", "plate_continuity", "prereg_sha256", "residence_ladder",
    "right_censored_exits", "player_speed_context", "track_length_census",
}

HALTS = []


def halt(code, msg):
    raise SystemExit(f"HALT ({code}): {msg}")


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def assign_keys(where, present, used, unused):
    """PREREG § 4.4.2 / R-PM4-75 part 3 operational form.
    Every key explicitly assigned; an unassigned key HALTs; nothing defaults."""
    present = set(present)
    unassigned = present - used - unused
    if unassigned:
        halt("PREREG-4.4.2",
             f"{where}: key(s) present in the artifact but assigned to neither "
             f"USED-BY-THIS-LAP nor DECLARED-UNUSED: {sorted(unassigned)}. "
             f"The partition is assembled from the artifact's own construction; "
             f"a remembered list does not scale (D-I27-1 / D-E7-1 / D-I28-1).")
    missing = used - present
    if missing:
        halt("PREREG-4.4.2",
             f"{where}: key(s) this lap declares it USES are absent: {sorted(missing)}")
    return {"present": sorted(present), "used": sorted(used & present),
            "declared_unused": sorted(unused & present),
            "unassigned": [], "verdict": "TOTAL-AND-EXHAUSTIVE"}


def main(outdir):
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    # ── PREREG § 1 / § 8(e) — assert every pin BEFORE reading content ───────────────────────
    print("=" * 100)
    print("KC2-PM4 · MICRO-LAP AD — THE T LEG   (referent-side only)")
    print("=" * 100)
    pin_report = {}
    for name, (rel, want) in PINS.items():
        got = sha256(ROOT / rel)
        ok = got == want
        pin_report[name] = {"path": rel, "expected": want, "got": got, "match": ok}
        print(f"  {'EXACT' if ok else 'MISMATCH'}  {got}  {name}")
        if not ok:
            halt("PREREG-8e", f"input digest mismatch on {name}: got {got}, want {want}")

    # I3 double-verification of I1 (prereg § 1, row I3)
    ac_dig = json.loads((ROOT / PINS["I3_ac_digests"][0]).read_text())
    i1_per_ac = ac_dig["emitted"]["pm4ac_residence.json"]
    if i1_per_ac != PINS["I1_residence"][1]:
        halt("PREREG-8e", f"I1 pin disagrees with Lap AC's own manifest: {i1_per_ac}")
    print(f"  I1 verified TWICE — Lap AC's own manifest agrees: {i1_per_ac}")

    R = json.loads((ROOT / PINS["I1_residence"][0]).read_text())

    # ── PREREG § 4.4.2 — explicit key assignment at three levels ────────────────────────────
    part = {"top_level": assign_keys("I1 top level", R.keys(),
                                     TOP_KEYS_USED, TOP_KEYS_UNUSED)}
    part["rung_level"] = assign_keys(f"I1 residence[{RUNG_PRIMARY}]",
                                     R["residence"][RUNG_PRIMARY].keys(),
                                     RUNG_KEYS_USED, RUNG_KEYS_UNUSED)
    part["per_wave_element_level"] = assign_keys(
        f"I1 residence[{RUNG_PRIMARY}].per_wave[*]",
        R["residence"][RUNG_PRIMARY]["per_wave"][0].keys(),
        PW_KEYS_USED, PW_KEYS_UNUSED)
    print(f"\n  partition: three levels, all TOTAL-AND-EXHAUSTIVE, zero unassigned keys")

    # ── PREREG § 2.1 — T_ref(w) at every rung present ───────────────────────────────────────
    T_by_rung, nobs_by_rung, frac_by_rung = {}, {}, {}
    for rc, entry in R["residence"].items():
        pw = entry["per_wave"]
        seen = {}
        for el in pw:
            w = el["wave"]
            if w not in WAVES:
                halt("PREREG-4.4.1", f"rung {rc}: per_wave element carries wave={w}, "
                                     f"outside the declared window {WAVES[0]}-{WAVES[-1]}")
            if w in seen:
                halt("PREREG-4.4.1", f"rung {rc}: duplicate per_wave element for wave {w}")
            seen[w] = el
        if set(seen) != set(WAVES):
            halt("PREREG-4.3", f"rung {rc}: waves present {sorted(seen)} != required "
                               f"{list(WAVES)}")
        T_by_rung[rc] = {}
        nobs_by_rung[rc] = {}
        frac_by_rung[rc] = {}
        for w in WAVES:
            n = seen[w]["n_observed_instants"]
            f = seen[w]["observed_fraction"]
            if n <= 0 or f <= 0:
                halt("PREREG-4.3", f"rung {rc} wave {w}: n_obs={n} obs_frac={f}; "
                                   f"evaluability floor requires both > 0")
            T_by_rung[rc][w] = n / f / FPS
            nobs_by_rung[rc][w] = n
            frac_by_rung[rc][w] = f

    # ── PREREG § 2.4 / P-2 — T_ref must be rung-INVARIANT (rung-free by construction) ───────
    ref = {w: round(T_by_rung[RUNG_PRIMARY][w], 4) for w in WAVES}
    invariance = {}
    for rc in sorted(T_by_rung):
        same = all(round(T_by_rung[rc][w], 4) == ref[w] for w in WAVES)
        invariance[rc] = same
    P2 = all(invariance.values())
    if not P2:
        halt("PREREG-8d", f"T_ref is NOT rung-invariant: {invariance}. The artifact does "
                          f"not match its own construction (pm4ac_residence:384-388 builds "
                          f"obs_times without any ring radius).")
    print(f"  P-2 rung-invariance of T_ref across {sorted(T_by_rung)} : PASS "
          f"(150.0 used for this check ONLY — AC DO-NOT 7)")

    T = {w: T_by_rung[RUNG_PRIMARY][w] for w in WAVES}
    nobs = {w: nobs_by_rung[RUNG_PRIMARY][w] for w in WAVES}
    frac = {w: frac_by_rung[RUNG_PRIMARY][w] for w in WAVES}

    # ── PREREG § 2.3 — T_direct, the TRANSCRIPTION cross-check from I2's basis column ───────
    T_direct, L_pinned, occ_rows = {}, {}, []
    with open(ROOT / PINS["I2_occupancy"][0], newline="") as fh:
        for row in csv.DictReader(fh):
            occ_rows.append(row)
            if row["scope"] == "per_wave":
                m = re.search(r"wave span\s+([0-9.]+)-([0-9.]+)\s*s", row["basis"])
                if m:
                    T_direct[int(row["wave"])] = float(m.group(2)) - float(m.group(1))
            if row["scope"] == "at_sim_D_ENGAGE_M_2.400":
                L_pinned[row["R_gpx"]] = float(row["mean_occupancy"])
    P1_reachable = set(T_direct) == set(WAVES)
    P1_maxdev = (max(abs(T_direct[w] - T[w]) for w in WAVES) if P1_reachable else None)

    # ── POST-HOC VERIFICATION (added AFTER the first numbers were seen; labelled POST-HOC
    #    everywhere; grades NOTHING; cannot change any verdict).  Lap R's CSV records a
    #    per-wave instant count in its basis text; Lap AC's JSON records n_observed_instants.
    #    Two laps, two artifacts, same census — a transit-integrity check, not evidence
    #    about the referent. ────────────────────────────────────────────────────────────────
    inst_direct, inst_total_direct = {}, None
    for row in occ_rows:
        if row["scope"] == "per_wave":
            m = re.search(r"([0-9]+)\s+instants", row["basis"])
            if m:
                inst_direct[int(row["wave"])] = int(m.group(1))
        elif row["scope"] == "whole_fight_radius_curve" and inst_total_direct is None:
            m = re.search(r"([0-9]+)\s+instants", row["basis"])
            if m:
                inst_total_direct = int(m.group(1))
    post_hoc = {
        "LABEL": "POST-HOC — added after the numbers; grades nothing; changes no verdict",
        "per_wave_instants_LapR_basis_vs_LapAC_json": {
            "all_10_parsed": set(inst_direct) == set(WAVES),
            "exact_on_all_10": all(inst_direct.get(w) == nobs_by_rung[RUNG_PRIMARY][w]
                                   for w in WAVES) if set(inst_direct) == set(WAVES) else None,
            "per_wave": {str(w): [inst_direct.get(w), nobs_by_rung[RUNG_PRIMARY][w]]
                         for w in WAVES}},
        "whole_fight_N_obs_LapR_basis": inst_total_direct,
        "note": ("both descend from the same Lap H-2 nameplate census; agreement demonstrates "
                 "the census survived transit through two laps intact and demonstrates nothing "
                 "about whether the census is correct"),
    }

    # ── PREREG § 4.4.3 — exhaustiveness, VERIFIED not assumed ───────────────────────────────
    sum_nobs = sum(nobs.values())
    top_nobs = R["n_observed_instants"]
    sum_nint = sum(el["n_intervals"] for el in R["residence"][RUNG_PRIMARY]["per_wave"])
    rung_nint = R["residence"][RUNG_PRIMARY]["n_intervals"]
    exh = {"sum_n_obs": sum_nobs, "top_level_n_observed_instants": top_nobs,
           "n_obs_exact": sum_nobs == top_nobs,
           "sum_n_intervals": sum_nint, "rung_n_intervals": rung_nint,
           "n_intervals_exact": sum_nint == rung_nint}
    P6 = exh["n_obs_exact"] and exh["n_intervals_exact"]
    if not P6:
        halt("PREREG-8c", f"per-wave partition is NOT exhaustive: {exh}. The § 3.2 "
                          f"aggregation identity loses its last equality; this is "
                          f"unmodeled and belongs to the conductor.")
    print(f"  partition exhaustive: instants {sum_nobs} == {top_nobs}, "
          f"intervals {sum_nint} == {rung_nint}")
    if sum_nobs < MIN_N_OBS:
        halt("PREREG-4.3", f"evaluability floor: N_obs {sum_nobs} < {MIN_N_OBS}")

    # ── PREREG § 3.2 — THE GATE STATISTIC, and the two rules pre-declared WRONG ─────────────
    def rung_stats(rc):
        pw = {el["wave"]: el for el in R["residence"][rc]["per_wave"]}
        B = {w: pw[w]["total_body_time_s"] for w in WAVES}
        L_recon = {w: B[w] / T[w] for w in WAVES}
        omega = {w: frac[w] * T[w] for w in WAVES}              # observed time in wave w
        L_agg = sum(B.values()) / sum(omega.values())           # THE gate statistic
        L_naive = sum(L_recon.values()) / len(WAVES)
        L_wall = sum(B.values()) / sum(T.values())
        L_directid = sum(B.values()) / (DT * sum_nobs)          # § 8(b) fourth candidate
        Lp = L_pinned[rc]
        return dict(R_gpx=rc, L_pinned=Lp,
                    B_total_s=round(sum(B.values()), 6),
                    omega_total_s=round(sum(omega.values()), 6),
                    L_agg=L_agg, rel_dev=L_agg / Lp - 1.0,
                    L_naive_mean=L_naive, rel_dev_naive=L_naive / Lp - 1.0,
                    L_walltime=L_wall, rel_dev_walltime=L_wall / Lp - 1.0,
                    L_identity_check=L_directid, rel_dev_identity=L_directid / Lp - 1.0,
                    per_wave_B=B, per_wave_L_recon=L_recon, per_wave_omega=omega,
                    pass_=abs(L_agg / Lp - 1.0) <= TOL)

    gate = {rc: rung_stats(rc) for rc in (RUNG_PRIMARY,) + RUNGS_SECONDARY}
    prim = gate[RUNG_PRIMARY]
    dev = abs(prim["rel_dev"])
    if prim["pass_"]:
        verdict, landing = "PASS", None
    elif dev <= NEAR_MISS_CEIL:
        verdict, landing = "FAIL", "ROUNDING-DOMINATED NEAR-MISS (prereg § 8a)"
    else:
        verdict, landing = "FAIL", "AGGREGATION-RULE MISMATCH (prereg § 8b) — HALT to conductor"

    print(f"\n  F-AD-1 at R={RUNG_PRIMARY}: L_agg {prim['L_agg']:.6f} vs pinned "
          f"{prim['L_pinned']:.4f}  rel_dev {prim['rel_dev']:+.3e}  TOL {TOL:.1e}  => {verdict}")
    for rc in RUNGS_SECONDARY:
        g = gate[rc]
        print(f"       secondary R={rc}: L_agg {g['L_agg']:.6f} vs {g['L_pinned']:.4f}  "
              f"rel_dev {g['rel_dev']:+.3e}  {'PASS' if g['pass_'] else 'FAIL'}")

    # ── PREREG § 5 — Sigma vs the fight window.  A TAUTOLOGY, declared as one. ──────────────
    sigT = sum(T.values())
    gap = FIGHT_SPAN - sigT
    P3 = abs(gap) <= SIGMA_BAND
    if not P3:
        halt("PREREG-5", f"Sigma T_ref {sigT:.6f} vs fight window {FIGHT_SPAN}: gap "
                         f"{gap:.6f} s exceeds the {SIGMA_BAND} s band. The windows "
                         f"telescope by construction (pm4r_lib:58) so a real gap means an "
                         f"operand was mis-read.")

    # ── PREREG § 6 — predictions, graded in the wording committed at 052008ee ───────────────
    Tmax, Tmin = max(T.values()), min(T.values())
    w_longest = max(WAVES, key=lambda w: T[w])
    w_highest_L = max(WAVES, key=lambda w: prim["per_wave_L_recon"][w])
    preds = [
        ("P-1", "T_ref agrees with T_direct to within 0.01 s on all 10 waves",
         ("PASS" if (P1_reachable and P1_maxdev <= 0.01) else
          ("UNREACHED" if not P1_reachable else "FAIL")),
         {"max_abs_dev_s": P1_maxdev, "all_10_parsed": P1_reachable}),
        ("P-2", "T_ref identical to 4 dp across all four rungs", "PASS" if P2 else "FAIL",
         invariance),
        ("P-3", "Sigma T_ref = 181.00 s +- 0.05 s and equals FIGHT_T1 - FIGHT_T0",
         "PASS" if P3 else "FAIL", {"sum_T_ref_s": sigT, "fight_span_s": FIGHT_SPAN,
                                    "gap_s": gap}),
        ("P-4", "F-AD-1 PASSES at rung 293.6 within TOL = 5.0e-3",
         "PASS" if prim["pass_"] else "FAIL", {"rel_dev": prim["rel_dev"]}),
        ("P-5", "F-AD-1 also passes at 285.7 and 300.0",
         "PASS" if all(gate[rc]["pass_"] for rc in RUNGS_SECONDARY) else "FAIL",
         {rc: gate[rc]["rel_dev"] for rc in RUNGS_SECONDARY}),
        ("P-6", "per-wave partition exhaustive on both instants and intervals, exactly",
         "PASS" if P6 else "FAIL", exh),
        ("P-7", "BLIND: L_naive_mean misses the pinned bracket by more than TOL",
         "PASS" if abs(prim["rel_dev_naive"]) > TOL else "FAIL",
         {"rel_dev_naive": prim["rel_dev_naive"]}),
        ("P-8", "BLIND: L_walltime misses the pinned bracket by more than TOL",
         "PASS" if abs(prim["rel_dev_walltime"]) > TOL else "FAIL",
         {"rel_dev_walltime": prim["rel_dev_walltime"]}),
        ("P-9", "BLIND: max_w T_ref / min_w T_ref >= 2.0",
         "PASS" if (Tmax / Tmin) >= 2.0 else "FAIL",
         {"max_s": Tmax, "min_s": Tmin, "ratio": Tmax / Tmin}),
        ("P-10", "BLIND: the longest-window wave is not the highest-L_recon wave",
         "PASS" if w_longest != w_highest_L else "FAIL",
         {"wave_longest_window": w_longest, "wave_highest_L_recon": w_highest_L}),
    ]
    print("\n  predictions:")
    for pid, txt, gr, _ in preds:
        print(f"    {pid:5s} {gr:9s} {txt}")

    # ── EMIT ────────────────────────────────────────────────────────────────────────────────
    with open(out / "pm4ad_t_ref.csv", "w", newline="") as fh:
        wcsv = csv.writer(fh)
        wcsv.writerow(["wave", "T_ref_s", "T_direct_s", "T_dev_s", "n_observed_instants",
                       "observed_fraction", "observed_time_s", "B_A_total_body_time_s",
                       "L_recon_bodies", "rung", "bound_direction", "uncertainty_s"])
        for w in WAVES:
            wcsv.writerow([
                w, f"{T[w]:.6f}",
                f"{T_direct[w]:.6f}" if w in T_direct else "",
                f"{T_direct[w] - T[w]:+.6f}" if w in T_direct else "",
                nobs[w], f"{frac[w]:.4f}", f"{prim['per_wave_omega'][w]:.6f}",
                f"{prim['per_wave_B'][w]:.3f}",
                f"{prim['per_wave_L_recon'][w]:.6f}",
                f"A@{RUNG_PRIMARY}gpx",
                "B_A is rung-A: a LOWER bound on body-time (AC DO-NOT 3); "
                "L_recon inherits that direction",
                "+-0.25 per cut (OBS-H2-6); T_ref is the segmentation, not a finer clock",
            ])

    res = {
        "lap": "AD",
        "authority": "R-PM4-75 part 4(ii) — second licensed referent-functional carve-out",
        "side": "REFERENT-ONLY — no sim artifact opened, no sim quantity computed or compared",
        "prereg_sha256": PINS["I9_prereg"][1],
        "prereg_commit": "052008ee",
        "constants": {"FPS": FPS, "DT": DT, "rung_primary": RUNG_PRIMARY,
                      "rungs_secondary": list(RUNGS_SECONDARY), "TOL": TOL,
                      "fight_window": [FIGHT_T0, FIGHT_T1], "waves": list(WAVES)},
        "input_pins": pin_report,
        "partition": part,
        "exhaustiveness": exh,
        "T_ref": {
            "functional": "T_ref(w) = n_observed_instants(w) / observed_fraction(w) / 60",
            "unit": "referent-clock seconds",
            "what_it_actually_is": (
                "an ALGEBRAIC INVERSE of WAVE_END[w] - WAVE_START[w]: observed_fraction is "
                "constructed at pm4ac_residence_2026_08_16.py:388 as "
                "len(wobs)/((WAVE_END[w]-WAVE_START[w])/DT), so the division recovers the "
                "segmentation span to 4-dp rounding.  It is NOT an independent measurement "
                "of window duration."),
            "uncertainty_s": 0.25,
            "uncertainty_basis": (
                "Lap H-2 OBS-H2-6: wave-increment times read +-0.25 s from a 52x26 "
                "wave-counter digit crop at (1582,138) by 4 fps frame-difference "
                "(pm4r_lib_2026_08_14.py:50-51).  The +-1-frame resolution the arithmetic "
                "superficially suggests is NOT this quantity's uncertainty."),
            "rung_invariant": True,
            "per_wave_s": {str(w): T[w] for w in WAVES},
            "per_wave_n_observed_instants": {str(w): nobs[w] for w in WAVES},
            "per_wave_observed_fraction": {str(w): frac[w] for w in WAVES},
            "sum_s": sigT,
            "T_direct_transcription_check": {
                "source": "pm4r_contact_occupancy.csv basis column, scope=per_wave",
                "is_independent": False,
                "note": ("both descend from WAVE_START at pm4r_lib_2026_08_14.py:52-55; "
                         "agreement proves no lap mangled the segmentation in transit and "
                         "proves nothing about whether the segmentation is correct"),
                "per_wave_s": {str(w): T_direct.get(w) for w in WAVES},
                "max_abs_dev_s": P1_maxdev},
        },
        "sigma_vs_fight_window": {
            "sum_T_ref_s": sigT, "fight_window_span_s": FIGHT_SPAN, "gap_s": gap,
            "status": "TAUTOLOGY, NOT CONFIRMATION",
            "why": ("pm4r_lib_2026_08_14.py:58 sets WAVE_END[w] = WAVE_START[w+1] for w<160 "
                    "and WAVE_END[160] = FIGHT_T1, so the ten windows telescope across the "
                    "fight window by construction: exhaustive, non-overlapping, admitting no "
                    "inter-wave dead time BY DEFINITION.  A zero gap confirms this lap read "
                    "line 58 correctly and nothing else."),
            "UNREACHED_AD_1": ("whether inter-wave dead time exists IN THE REFERENT is "
                               "undecidable from these pins: OBS-H2-6 cuts at the "
                               "wave-counter digit change and PARTITIONS rather than "
                               "BRACKETS, assigning every intervening second to one wave or "
                               "the other."),
        },
        "F_AD_1": {
            "statement": ("L_agg(RC) = sum_w B_A(w) / sum_w [observed_fraction(w) * T_ref(w)] "
                          "vs the pinned mean_occupancy at scope=at_sim_D_ENGAGE_M_2.400"),
            "aggregation_rule": {
                "rule": "OBSERVED-INSTANT-WEIGHTED mean over the whole fight window",
                "neither_option_offered": ("it is NOT a per-wave mean and NOT a wall-clock "
                                           "time-weighted mean"),
                "byte_citation": [
                    "pm4r_contact_2026_08_14.py:58 — times = sorted(t for t in P if "
                    "FIGHT_T0 <= t <= FIGHT_T1)  [P = player-plate map, :50-52]",
                    "pm4r_contact_2026_08_14.py:248-252 — cc[i] built one integer per element "
                    "of times",
                    "pm4r_contact_2026_08_14.py:266 — mean_occupancy = round(cc.mean(), 4)",
                    "pm4r_contact_2026_08_14.py:59-61 — 'instants without a player plate are "
                    "EXCLUDED, not imputed'",
                    "pm4ac_residence_2026_08_16.py:388 — observed_fraction(w) * T_ref(w) == "
                    "n_obs(w) * DT identically, so the 4-dp rounding of observed_fraction "
                    "CANCELS in the weight",
                ],
                "weight": "omega(w) = observed_fraction(w) * T_ref(w) = OBSERVED time in wave w",
            },
            "tolerance": TOL,
            "tolerance_budget_a_priori": {
                "per_interval_body_time_round_4dp": 9.0e-4,
                "per_wave_total_round_3dp": 8.8e-6,
                "pinned_mean_occupancy_round_4dp": 1.5e-5,
                "observed_fraction_round_4dp": 0.0,
                "worst_case_total": 9.2e-4},
            "verdict": verdict,
            "landing_site": landing,
            "primary_rung": RUNG_PRIMARY,
            "rungs": {rc: {k: v for k, v in g.items()
                           if k not in ("per_wave_B", "per_wave_L_recon", "per_wave_omega")}
                      for rc, g in gate.items()},
            "per_wave": {str(w): {"B_A_s": prim["per_wave_B"][w],
                                  "T_ref_s": T[w],
                                  "omega_s": prim["per_wave_omega"][w],
                                  "L_recon_bodies": prim["per_wave_L_recon"][w]}
                         for w in WAVES},
        },
        "post_hoc_verifications": post_hoc,
        "predictions": [{"id": p, "text": t, "grade": g, "evidence": e}
                        for p, t, g, e in preds],
        "halts": HALTS,
        "firewall": [
            "no sim artifact, cell, ledger, output directory or code path opened",
            "no comparison of any quantity to any sim quantity, in prose or by adjacency",
            "the occupancy bracket is NOT re-derived; F-AD-1 is a fidelity gate only",
            "the 9 cuts are OBS-H2-6's; re-expressed, never re-measured, +-0.25 s not adjudicated",
            "pm4u_arrivals.csv not opened (Lap AB DO-NOT 9)",
            "R=150.0 used ONLY for the rung-free T-invariance check, never pooled (AC DO-NOT 7)",
            "no metre conversion, no body count, no arrival rate, no residence scalar quoted",
            "no pinned instrument modified",
        ],
    }
    (out / "pm4ad_t_ref.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print(f"\n  wrote {out/'pm4ad_t_ref.csv'} and {out/'pm4ad_t_ref.json'}")
    return verdict


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pm4ad/run1")
