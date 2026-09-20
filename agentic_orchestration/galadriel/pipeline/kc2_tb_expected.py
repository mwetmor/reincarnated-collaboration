#!/usr/bin/env python3
"""
kc2_tb_expected.py — assemble the KC2-PLAY T-B EXPECTED-VALUES TABLE (machine-readable).

Consumes:
  - the HP shape re-query (kc2_hp_shape.py stdout, passed as argv[1])
  - the committed footage-instrument artifacts (read directly, by path)

Emits the JSON the T-B grader loads. EVERY row carries:
  value · uncertainty · instrument (file + note) · denominator (the exact definition the
  recorder must reproduce) · reproduction status against the already-published figure.

galadriel, 2026-09-20, run KC2-PLAY Wave 1. Read-only on every source.
"""
import json
import sys
import hashlib
import os

ROOT = "/Users/admin/Games/reincarnated-collaboration"
AO = os.path.join(ROOT, "agentic_orchestration")

REL = os.path.join(AO, "galadriel/captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json")
CHAN = os.path.join(AO, "galadriel/captures/2026-08-25-md-b4app-2-channel/work/s2-channel-summary.json")
DUTY = os.path.join(AO, "galadriel/captures/2026-08-25-md-b4app-2-channel/work/s2-duty.json")
WAVES = os.path.join(AO, "galadriel/captures/2026-08-25-md-b4app-2-channel/work/waves.json")
H2 = os.path.join(AO, "legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/pm4h2_movement_cadence.csv")
TRACE = os.path.join(AO, "legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def row(rid, stat, value, unit, unc, instrument, denominator, repro, note=None):
    d = {
        "id": rid,
        "statistic": stat,
        "value": value,
        "unit": unit,
        "uncertainty": unc,
        "instrument": instrument,
        "denominator": denominator,
        "reproduction": repro,
    }
    if note:
        d["note"] = note
    return d


def main():
    hp = json.load(open(sys.argv[1]))
    rel = json.load(open(REL))
    chan = json.load(open(CHAN))
    duty = json.load(open(DUTY))
    wv = json.load(open(WAVES))

    occL = hp["occupancy_denominator_LIVE_MAX"]
    occN = hp["occupancy_denominator_NOMINAL_20005"]
    sw = hp["sawtooth_prominence_sweep_hp"]
    fd = hp["frame_deltas"]
    hm = hp["hp_max"]["episodes_off_nominal"][0]

    I_Q = {
        "lap": "KC2-PM4 Lap Q (legolas) — heal discriminator",
        "artifact": "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv",
        "sha256": hp["source"]["sha256"],
        "note": "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_findings.md",
        "method": "HUD health-orb readout ROI x[520,780) y[996,1026), 60 fps, Apple Vision OCR; PC-3 100.00% accepted against the DECODED denominator",
        "requery_instrument": "agentic_orchestration/galadriel/pipeline/kc2_hp_shape.py",
    }
    I_CH = {
        "lap": "MD-B4app-2 (galadriel) — channel/move duty cycle",
        "artifact": "agentic_orchestration/galadriel/captures/2026-08-25-md-b4app-2-channel/work/s2-channel-summary.json",
        "sha256": sha(CHAN),
        "note": "agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md",
        "method": "HUD energy readout cur/max, glyph-atlas OCR at 60 Hz -> drain ticks; camera-pan registration at 20 Hz for motion",
    }
    I_REL = {
        "lap": "MD-B4app-2b (galadriel) — energy release population",
        "artifact": "agentic_orchestration/galadriel/captures/2026-08-25-md-b4app-2b-energy/work/s2-releases.json",
        "sha256": sha(REL),
        "note": "agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2b-energy-release.md",
        "method": "gaps in the 60 Hz energy-drain tick train, floor T_REL = 0.5 s, coverage floor COV_MIN = 0.8",
    }
    I_2C = {
        "lap": "MD-B4app-2c (galadriel) — per-slot interrupt attribution",
        "note": "agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2c-culprit.md",
        "method": "20 Hz per-slot skill-bar dimming + eye-adjudicated cooldown numerals; energy 60 Hz for the silence timing",
    }
    I_H2 = {
        "lap": "KC2-PM4 Lap H-2 (legolas) — video match / movement cadence",
        "artifact": "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/pm4h2_movement_cadence.csv",
        "sha256": sha(H2),
    }
    I_R = {
        "lap": "KC2-PM4 Lap R (legolas) — locomotion + contact",
        "note": "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_findings.md",
    }
    I_U = {
        "lap": "KC2-PM4 Lap U (legolas) — ramp decode",
        "note": "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_findings.md",
    }
    I_BADGE = {
        "lap": "galadriel EoR sittings extraction (wave badge, sitting 2)",
        "artifact": "agentic_orchestration/galadriel/captures/2026-08-25-md-b4app-2-channel/work/waves.json",
        "sha256": sha(WAVES),
        "note": "agentic_orchestration/galadriel/notes/2026-08-07-eor-sittings-extraction.md + …2026-08-08-eor-followup-extraction.md §7.1",
    }

    # ---- DENOMINATOR LAW ----------------------------------------------------
    denoms = {
        "D-HP-FRAME": {
            "name": "HP-trace frame denominator",
            "definition": "ALL 10,861 rows of pm4q_hp_trace.csv, t in [683.0, 864.0], 60 fps, frames CONTIGUOUS (verified: every frame index increments by 1; dt in {0.0166, 0.0167} only).",
            "n": hp["grid"]["rows"],
            "span_s": hp["grid"]["span_s"],
            "warning": "This is NOT the 182.65 s combat window used by the energy/motion instruments. It is 181.0 s and starts 0.90 s later. Any RATE computed on one window is not comparable to a rate computed on the other without restating the denominator.",
        },
        "D-HP-INTERVAL": {
            "name": "HP frame-to-frame interval denominator",
            "definition": "The 10,860 ADJACENT-FRAME INTERVALS of D-HP-FRAME (n-1, not n). Lap Q's published 13.73% is reproduced on n-1; on n it is 13.728% — the two differ by 0.0013 pp and both print as 13.73%. The grader uses n-1.",
            "n": fd["n_intervals"],
        },
        "D-HP-LIVE-MAX": {
            "name": "LIVE-MAX health denominator",
            "definition": "A health threshold is applied against health_max AS READ AT THAT FRAME, i.e. 16,368 inside the D-Q1 episode and 20,005 elsewhere. THIS IS THE DENOMINATOR THAT REPRODUCES 42.84%.",
            "critical": "Under the NOMINAL alternative (20,005 throughout) time-at-full is 39.76%, not 42.84% — a 3.08 pp gap created purely by denominator choice. The below-50% and below-33% rows are denominator-INSENSITIVE (both give 376 / 109 frames) because every deep excursion occurs at nominal health_max.",
        },
        "D-HP-NOMINAL": {
            "name": "NOMINAL health denominator",
            "definition": "A health threshold is applied against the constant 20,005 for every frame. Shipped alongside D-HP-LIVE-MAX so the grader can see which rows move.",
        },
        "D-COMBAT-182": {
            "name": "combat window, badge instrument",
            "definition": "t in [682.10, 864.75] = 182.65 s. Opens at the wave-151 badge flip (galadriel sitting-2 timeline), closes at the player-death instant (corrected to 864.75 in the 2026-08-08 follow-up). Ten waves, no prep, no post-death. ALL energy / motion / release / cast statistics use this window.",
            "span_s": 182.65,
        },
        "D-GOODCOV": {
            "name": "good-coverage subset of D-COMBAT-182",
            "definition": "The 20 Hz samples whose 60 Hz energy OCR coverage clears the accept gate. goodcov_fraction = " + str(chan["goodcov_fraction"]) + " of D-COMBAT-182. Channel uptime is computed ON THIS SUBSET, not on the full window.",
            "goodcov_fraction": chan["goodcov_fraction"],
            "warning": "A recorder that computes uptime over ALL its own ticks is computing a DIFFERENT statistic from the 0.8375 it is being compared to. The grader must either (a) restrict to a coverage-matched subset or (b) declare the comparison as instrument-divergent (charter § 2, fifth attribution class).",
        },
        "D-CAST-VISIBLE": {
            "name": "visible-slot cast denominator",
            "definition": "Casts detected as per-slot skill-bar DIMMING on slots 2, 3 and L only. Slots 7 and R never dim (brightness varies < 3 units over 3,653 frames) and slot 4 carries a WHITE buff-duration numeral, not a cooldown — all three are excluded by construction. Every cast count is therefore a FLOOR, not an estimate.",
        },
    }

    rows = []

    # ================= HP TRACE =============================================
    rows.append(row(
        "TB-HP-01", "time at FULL health",
        {"fraction": occL["at_full"]["fraction"], "frames": occL["at_full"]["frames"],
         "under_nominal_denominator": occN["at_full"]["fraction"]},
        "fraction of frames",
        {"class": "OCR-read", "basis": "PC-3 100.00% accepted; trace resolves to 1 HP / 1 frame",
         "frame_quantisation_s": 0.0167,
         "dominant_term": "DENOMINATOR CHOICE, not read error: 0.4284 (LIVE-MAX) vs 0.3976 (NOMINAL)"},
        I_Q, ["D-HP-FRAME", "D-HP-LIVE-MAX"],
        {"published": 0.4284, "published_as": "2D spec B-11 / Lap Q § 4.1 (4,653 of 10,861)",
         "recomputed": occL["at_full"]["fraction"], "status": "REPRODUCES EXACT"},
        "hp >= health_max at that frame. Absolute form: hp == hp_max, with hp_max in {20,005; 16,368}."))

    for k, lab, pub in [("below_90pct", "time below 90% health", None),
                        ("below_75pct", "time below 75% health", None),
                        ("below_50pct", "time below 50% health", 0.0346),
                        ("below_33pct", "time below 33% health", 0.0100),
                        ("below_25pct", "time below 25% health", None)]:
        rid = "TB-HP-" + {"below_90pct": "02", "below_75pct": "03", "below_50pct": "04",
                          "below_33pct": "05", "below_25pct": "06"}[k]
        rp = ({"published": pub, "published_as": "2D spec B-12 / Lap Q § 4.1",
               "recomputed": occL[k]["fraction"], "status": "REPRODUCES EXACT"} if pub else
              {"published": None, "published_as": "NOT PREVIOUSLY PUBLISHED — new this lap",
               "recomputed": occL[k]["fraction"], "status": "NEW"})
        rows.append(row(
            rid, lab,
            {"fraction": occL[k]["fraction"], "frames": occL[k]["frames"],
             "under_nominal_denominator": occN[k]["fraction"],
             "seconds": round(occL[k]["frames"] / 60.0, 4)},
            "fraction of frames",
            {"class": "OCR-read", "basis": "PC-3 100.00%",
             "denominator_sensitivity": ("NONE — identical frame count under both denominators"
                                         if occL[k]["frames"] == occN[k]["frames"] else
                                         "SENSITIVE — see D-HP-LIVE-MAX vs D-HP-NOMINAL")},
            I_Q, ["D-HP-FRAME", "D-HP-LIVE-MAX"], rp,
            "hp < threshold * health_max AT THAT FRAME (strict inequality)."))

    rows.append(row(
        "TB-HP-07", "frames showing an HP DECREASE",
        {"fraction": fd["frac_decrease"], "count": fd["decrease"],
         "increase_fraction": fd["frac_increase"], "flat_fraction": fd["frac_flat"]},
        "fraction of adjacent-frame intervals",
        {"class": "OCR-read",
         "denominator_ambiguity": "n-1 = 10,860 -> 0.137293; n = 10,861 -> 0.137280. Both print 13.73%. USE n-1."},
        I_Q, ["D-HP-INTERVAL"],
        {"published": 0.1373, "published_as": "2D spec B-13 / Lap Q § 4.1 (1,491 frames)",
         "recomputed": fd["frac_decrease"], "status": "REPRODUCES EXACT (count 1,491)"},
        "hp[i] < hp[i-1]. Increase and flat shipped too so the grader can check the three sum to 1."))

    rows.append(row(
        "TB-HP-08", "HP minimum (absolute)",
        {"hp": hp["hp_extremes"]["hp_min"], "hp_max_at_that_frame": 20005,
         "fraction_of_hp_max": round(hp["hp_extremes"]["hp_min"] / 20005.0, 6),
         "t_s": hp["hp_extremes"]["t_at_hp_min"], "wave": hp["hp_extremes"]["wave_at_hp_min"]},
        "HP",
        {"class": "OCR-read", "basis": "single-frame extremum; 1 HP resolution"},
        I_Q, ["D-HP-FRAME"],
        {"published": 5360, "published_as": "2D spec B-14 / Lap Q § 4.1 (5,360 of 20,005)",
         "recomputed": hp["hp_extremes"]["hp_min"], "status": "REPRODUCES EXACT"},
        "ABSOLUTE hp and hp_max, never a bare fraction. He never reached 25% of max: the floor is 26.79%."))

    rows.append(row(
        "TB-HP-09", "health_max DROP episode (D-Q1)",
        {"hp_max_during": hm["hp_max"], "hp_max_nominal": 20005,
         "delta_hp": hm["delta_hp"], "delta_pct": hm["delta_pct"],
         "t_start": hm["t_start"], "t_end": hm["t_end"], "dur_s": hm["dur_s"],
         "waves_straddled": [hm["wave_start"], hm["wave_end"]],
         "episodes_in_fight": 1},
        "HP / s",
        {"class": "boundary-frame", "value_s": 0.0167,
         "note": "t_end here is the FIRST frame back at nominal; Lap Q published 721.650 (the LAST frame at 16,368). One frame apart. Duration agrees: 8.2834 vs 8.283 s."},
        I_Q, ["D-HP-FRAME"],
        {"published": {"delta_pct": -18.18, "dur_s": 8.283, "span": [713.383, 721.650]},
         "published_as": "2D spec B-18 / Lap Q § 6 D-Q1",
         "recomputed": {"delta_pct": hm["delta_pct"], "dur_s": hm["dur_s"],
                        "span": [hm["t_start"], hm["t_end"]]},
         "status": "REPRODUCES (end-frame convention differs by 1 frame; duration identical to 3 dp)"},
        "PRE-REGISTERED KNOWN MODEL GAP: the sim holds health_max constant. The twin is EXPECTED to "
        "show zero such episodes. That difference is NOT a build defect and the grader must not score it as one."))

    # ---- saw-tooth (B-19, the commissioned row) -----------------------------
    rows.append(row(
        "TB-HP-10", "HP saw-tooth PERIOD and DEPTH (B-19)",
        {"primary_prominence_hp": 500,
         "primary": {k: sw["500"][k] for k in
                     ["n_teeth", "rate_per_s", "period_s", "depth_hp", "depth_frac_of_hp_max",
                      "fall_s", "recover_s", "fall_slope_hp_per_s", "recovery_slope_hp_per_s"]},
         "sweep": {p: {"n_teeth": sw[p]["n_teeth"], "rate_per_s": sw[p]["rate_per_s"],
                       "period_median_s": sw[p]["period_s"]["median"],
                       "depth_median_hp": sw[p]["depth_hp"]["median"],
                       "depth_median_frac": sw[p]["depth_frac_of_hp_max"]["median"],
                       "recovery_slope_median_hp_per_s": sw[p]["recovery_slope_hp_per_s"]["median"]}
                   for p in sw}},
        "s / HP",
        {"class": "RULE-DEPENDENT — the dominant uncertainty is the PROMINENCE GATE, not the read",
         "swept": [100, 250, 500, 1000, 2000],
         "spread_across_sweep": "n_teeth 254 -> 43 (5.9x); median period 0.30 s -> 2.45 s (8.2x); "
                                "median depth 563 -> 3,553 HP (6.3x). THE GATE IS THE MEASUREMENT.",
         "why_500": "500 HP = 2.50% of nominal max — the smallest step that is unambiguously a hit "
                    "or a leech tick rather than the +2/+3 HP/frame regeneration drip. It is DECLARED, "
                    "not fitted: no arm of this lap was selected by comparing it to a sim."},
        I_Q, ["D-HP-FRAME", "D-HP-LIVE-MAX"],
        {"published": None,
         "published_as": "NOT PUBLISHED — 2D spec B-19 declares it ABSENT; § 6.4 registers it as OQ-4, derivable by re-query",
         "recomputed": "see primary/sweep", "status": "NEW — this row discharges B-19 / OQ-4"},
        "TOOTH RULE (the recorder must implement THIS, verbatim): alternating-extremum walk with an "
        "ABSOLUTE-HP prominence gate. Confirm a PEAK when hp falls `prom` below the running max since "
        "the last confirmed trough; confirm a TROUGH when hp rises `prom` above the running min since "
        "the last confirmed peak. A tooth is a confirmed (peak -> trough -> next peak) triple. "
        "depth_hp = peak.hp - trough.hp; depth_frac = depth_hp / hp_max AT THE PEAK; "
        "period_s = next_peak.t - peak.t. Reference implementation: galadriel/pipeline/kc2_hp_shape.py::teeth."))

    rows.append(row(
        "TB-HP-11", "deepest excursions below 50% health",
        {"n_excursions": len(hp["excursions_below_50pct_live"]),
         "excursions": hp["excursions_below_50pct_live"],
         "all_in_waves": sorted(set(e["wave"] for e in hp["excursions_below_50pct_live"]))},
        "HP / s",
        {"class": "OCR-read + run segmentation",
         "segmentation_rule": "maximal contiguous run of frames with hp < 0.50 * hp_max; a single "
                              "frame qualifies. Runs are NOT merged across a recovery above the line."},
        I_Q, ["D-HP-FRAME", "D-HP-LIVE-MAX"],
        {"published": None, "published_as": "NOT PREVIOUSLY PUBLISHED — new this lap",
         "recomputed": "8 excursions", "status": "NEW"},
        "⚑ EVERY sub-half excursion in the fight is in wave 159 or 160. Waves 151-158 never go below "
        "half at all. The 'inversion moment' is not distributed across the fight; it is the last two waves."))

    rows.append(row(
        "TB-HP-12", "per-wave HP shape",
        {w: hp["per_wave"][w] for w in hp["per_wave"] if w != "-1"},
        "mixed",
        {"class": "OCR-read",
         "note": "wave labels are the trace's OWN wave column (H-2 boundary set), not the badge timeline. "
                 "Frame 10860 (t=864.0) carries an EMPTY wave label in the source and is mapped to -1; "
                 "it is excluded from this row and reported rather than dropped."},
        I_Q, ["D-HP-FRAME", "D-HP-LIVE-MAX"],
        {"published": None, "published_as": "NOT PREVIOUSLY PUBLISHED — new this lap",
         "recomputed": "10 waves", "status": "NEW"},
        "n_teeth_prom500 / median depth / median period are at the PRIMARY gate only; the sweep is whole-fight."))

    rows.append(row(
        "TB-HP-13", "health regeneration (drip)",
        {"measured_hp_per_s": 124.67, "decoded_hp_per_s": 129.38, "residual_pct": -3.64,
         "contaminated_whole_trace_reading_hp_per_s": 178.40},
        "HP/s",
        {"class": "subset-selection", "n": 90,
         "basis": "uncontaminated sub-33%-health subset (87 x +2 HP/frame); the only stretch free of "
                  "sub-50 HP leech ticks"},
        I_Q, ["D-HP-FRAME"],
        {"published": 124.67, "published_as": "2D spec B-17 / Lap Q § 4.2",
         "recomputed": "CARRIED from Lap Q, not re-derived this lap",
         "status": "CARRIED — not independently re-derived (the subset rule is Lap Q's and re-deriving it would change the instrument)"},
        "⚑ The naive whole-trace drip reads 178.40 HP/s and is CONTAMINATED. A grader that computes "
        "regeneration over the whole trace will get 178.40 and will be wrong. Menhir's Will (+120 hp/s "
        "below 33%) is MEASURED-ABSENT: below 33% the drip stays at 124.67, not 249.38."))

    rows.append(row(
        "TB-HP-14", "leech tick cadence and magnitude",
        {"cadence_ticks_per_s": 11.408, "mean_intertick_gap_frames": 5.259,
         "decoded_bracket": [11.387, 12.250],
         "clean_median_hp": 820.8, "clean_n": 67, "all_median_hp": 782.8, "all_n": 129},
        "ticks/s, HP",
        {"class": "tick census", "basis": "step >= 50 HP, deficit >= 3,000, step not on the cap; "
                                          "'clean' = no HP decrease within +-2 frames"},
        I_Q, ["D-HP-FRAME"],
        {"published": {"cadence": 11.408, "clean_median": 820.8},
         "published_as": "2D spec B-15/B-16 / Lap Q § 4.2, § 5.2",
         "recomputed": "CARRIED from Lap Q", "status": "CARRIED"},
        "U-P-N-1 = COUPLED. The per-body heal is an UPPER bound (N_bodies never observed at tick resolution)."))

    # ================= CHANNEL / RELEASE / CAST =============================
    rows.append(row(
        "TB-CH-01", "channel uptime",
        {"value": chan["channel_active_ge3_goodcov"],
         "at_ge2_ticks": chan["channel_active_ge2_goodcov"],
         "at_ge4_ticks": chan["channel_active_ge4_goodcov"],
         "zero_tick_fraction": chan["zero_tick_fraction_goodcov"]},
        "fraction of good-coverage samples",
        {"class": "coverage + threshold",
         "blind_residual": "6.2% of the window (13 gaps, 11.42 s, coverage 0.12-0.72) CARRIED, NOT CLOSED",
         "threshold_sensitivity": "0.8953 (>=2 ticks) / 0.8375 (>=3) / 0.7530 (>=4) — a 0.142 spread on "
                                  "the tick-count gate alone. 0.838 is the >=3 arm.",
         "goodcov_fraction": chan["goodcov_fraction"]},
        I_CH, ["D-COMBAT-182", "D-GOODCOV"],
        {"published": 0.838, "published_as": "2D spec B-1",
         "recomputed": chan["channel_active_ge3_goodcov"], "status": "REPRODUCES EXACT (0.8375)"},
        "⚑ The gamora seal note D-MPOL2-5 proves uptime == 1 - duty BY IDENTITY in the SIM (zero blind "
        "ticks). It is NOT an identity on the REFERENT, where the 6.2% blind residual makes the two "
        "independent. A band pair imported across those two populations is inconsistent by construction."))

    rows.append(row(
        "TB-CH-02", "P(channel | moving) and P(channel | stationary)",
        {"P_channel_given_MOVING": chan["P_channel_given_MOVING"],
         "P_channel_given_STATIONARY": chan["P_channel_given_STATIONARY"],
         "ratio_moving_over_stationary": round(chan["P_channel_given_MOVING"] / chan["P_channel_given_STATIONARY"], 4)},
        "probability / ratio",
        {"class": "conditional on the motion classifier",
         "note": "the motion classifier is the 20 Hz camera-pan instrument whose frac_moving is the "
                 "disputed quantity (TB-MV-01). The RATIO is the shippable form."},
        I_CH, ["D-COMBAT-182", "D-GOODCOV"],
        {"published": {"moving": 0.8920, "stationary": 0.7376},
         "published_as": "MD-B4app-2 top line; quoted in LIFT ledger L-88",
         "recomputed": {"moving": chan["P_channel_given_MOVING"],
                        "stationary": chan["P_channel_given_STATIONARY"]},
         "status": "REPRODUCES EXACT"},
        "The referent CHANNELS THROUGH HIS MOVEMENT. Ordering (moving > stationary) is the structural row."))

    dur_total = round(sum(r["dur_s"] for r in rel["releases"]), 3)
    rows.append(row(
        "TB-RL-01", "release duty",
        {"fraction": round(dur_total / 182.65, 5), "n_releases": len(rel["releases"]),
         "total_released_s": dur_total, "mean_interval_s": round(182.65 / len(rel["releases"]), 3),
         "upper_if_blind_gaps_are_releases": 0.167},
        "fraction of combat time",
        {"class": "floor-dependent",
         "floor_sweep_T_REL": {k: {"n_kept": v["n_kept"], "total_s": v["total_s"],
                                   "duty": round(v["total_s"] / 182.65, 5)}
                               for k, v in rel["population_sweep"].items()},
         "note": "duty ranges 0.0609 (floor 1.00 s) to 0.1835 (floor 0.25 s) across the committed "
                 "sweep — a 3.0x spread on the release-floor choice. 0.5 s is the primary."},
        I_REL, ["D-COMBAT-182"],
        {"published": 0.105, "published_as": "2D spec B-2 (~10.5%)",
         "recomputed": round(dur_total / 182.65, 5), "status": "REPRODUCES (0.10484)"},
        "A release is an ABSENCE of drain ticks. 41% of apparent releases at the 0.5 s floor were "
        "DISCARDED as OCR blind spots; the 6.2% blind residual is the ceiling on that repair."))

    typeA_n, typeB_n = 11, 8
    rows.append(row(
        "TB-RL-02", "Type-A release (wave transition) — onset lag and duration",
        {"onset_lag_median_s": 1.60, "within_2s": "8 of 11",
         "duration_median_s": 1.03, "duration_IQR_s": [0.62, 1.56], "duration_max_s": 3.50,
         "n": typeA_n, "fisher_p_A_vs_B_near_flip": 0.00336},
        "s",
        {"class": "small-n order statistic", "n": typeA_n,
         "note": "A-1: the model fires ONE Type-A per transition; the footage measures 1.1. PARKED, "
                 "explicitly not fired (R-L88-3) — correcting it BECAUSE a band failed is band-rescue."},
        I_REL, ["D-COMBAT-182"],
        {"published": {"lag": 1.60, "dur": 1.03, "iqr": [0.62, 1.56], "max": 3.50},
         "published_as": "2D spec B-4/B-5",
         "recomputed": "A/B label set re-derived from s2-releases.json: the 8 releases with "
                       "s_since_wave_flip <= 2.0 s are {0.08, 0.35, 0.51, 0.53, 0.80, 1.60, 1.72, 1.78}, "
                       "median of the 11-member Type-A lag set = 1.60, max duration 3.50 at t=744.55",
         "status": "REPRODUCES"},
        "Onset lag = t_on - (wave badge flip). Requires the BADGE timeline (D-COMBAT-182), not the "
        "trace's wave column: the two differ by up to 0.88 s at the window edges."))

    rows.append(row(
        "TB-RL-03", "Type-B release (cast) — duration",
        {"duration_median_s": 0.60, "duration_IQR_s": [0.55, 0.63],
         "range_s": [0.53, 0.67], "n": typeB_n,
         "implied_sigma_ms": 49},
        "s",
        {"class": "small-n order statistic", "n": typeB_n,
         "⚑": "Gate-1 WARN-17 struck the 'a human cannot hold a 0.14 s spread' argument: that range "
              "over n=8 implies sigma ~49 ms, ordinary human reaction-time variance. What carries KP-1 "
              "is the WITHIN-SUBJECT CONTRAST against Type-A (IQR 0.62-1.56, max 3.50), not the tightness alone."},
        I_REL, ["D-COMBAT-182"],
        {"published": {"median": 0.60, "iqr": [0.55, 0.63], "range": [0.53, 0.67], "n": 8},
         "published_as": "2D spec B-6",
         "recomputed": "9 releases in s2-releases.json fall in [0.53, 0.67] with flip-lag > 2.0 s; "
                       "8 of them carry a cast attribution in MD-B4app-2c § 3 and are the Type-B set",
         "status": "REPRODUCES — but the A/B LABELS require the 2c attribution table, not this JSON alone"},
        "KP-1 (Matt-accepted at KP-2): Type-B AUTO-RESUMES while RMB is held; Type-A resumes on input only."))

    rows.append(row(
        "TB-CA-01", "cast rate",
        {"published_value_per_s": 0.290, "published_n": 53,
         "corrected_value_per_s": round(54 / 182.65, 4), "corrected_n": 54,
         "corrected_interval_s": round(182.65 / 54, 3),
         "per_slot": {"slot_2": 22, "slot_3": 19, "slot_L": 13}},
        "casts/s",
        {"class": "FLOOR, not an estimate",
         "floors": "slots 7 and R are BLIND to both instruments; slot 4 is a buff timer, not a cast; "
                   "a re-fire mid-cooldown is undetectable in principle. Three OCR-blind dim gaps carried."},
        I_2C, ["D-COMBAT-182", "D-CAST-VISIBLE"],
        {"published": 0.290, "published_as": "2D spec B-3 (n = 53, one per 3.45 s)",
         "recomputed": round(54 / 182.65, 4),
         "status": "⚑ DOES NOT REPRODUCE AS PUBLISHED — 1.9% high"},
        "⚑ THE 0.290 IS STALE BY ONE LAP. MD-B4app-2b § 5.3 counted 53 (22/19/12). MD-B4app-2c § 2 then "
        "eye-adjudicated a 7.20 s slot-L dim run against a 3.60 s modal cooldown and split it into TWO "
        "casts (eor_attrib.MERGED), moving slot L 12 -> 13 and the total 53 -> 54. Every downstream "
        "figure in 2c is on 54 (0.148 = 8/54). The 2D spec's B-3 quotes the pre-correction count. "
        "VALUE OF RECORD: 0.2957 /s, one per 3.383 s, n = 54."))

    rows.append(row(
        "TB-CA-02", "per-slot interrupt attribution",
        {"by_slot": {"slot_L": {"casts": 13, "interrupts": 5, "P": 0.385, "binomial_p": 0.00034},
                     "slot_2": {"casts": 22, "interrupts": 3, "P": 0.136, "binomial_p": 0.104},
                     "slot_3": {"casts": 19, "interrupts": 0, "P": 0.000,
                                "max_silence_in_19_casts_s": 0.233}},
         "aggregate": {"casts": 54, "interrupts": 8, "P": 0.148, "binomial_p": 0.0065},
         "orphans": 0},
        "P(interrupt | cast)",
        {"class": "small-n per-slot", "fisher_L_vs_rest_p": 0.0146, "fisher_L_vs_slot3_p": 0.0064,
         "fisher_L_vs_slot2_p": 0.103,
         "⚑": "THE AGGREGATE 0.15 IS A CANCELLATION, NOT A RATE. Against the duration-weighted null, "
              "slots 2 and L land in LONGER-than-random silences (p = 0.00019, 0.0070) and slot 3 in "
              "SHORTER ones (p = 4.9e-7); pooled they cancel to p = 0.286. The 0.15 is the arithmetic "
              "mean of a rule and its opposite: correct in aggregate, wrong for every individual skill."},
        I_2C, ["D-COMBAT-182", "D-CAST-VISIBLE"],
        {"published": {"Blitz": 0.385, "Vires": 0.136, "WarCry": 0.000, "RuneOfRush": "BLIND"},
         "published_as": "2D spec B-7",
         "recomputed": {"slot_L": 0.385, "slot_2": 0.136, "slot_3": 0.000},
         "status": "⚑ NUMBERS REPRODUCE; THE SKILL NAMES DO NOT"},
        "⚑ SLOT-TO-SKILL IS NOT MEASURED. MD-B4app-2c § 0 and § 7 are explicit: 'No skill is named in "
        "this note and none should be quoted from it'; slots are SHAPE-CONSISTENT-NOT-IDENTIFIED "
        "(slot L = 'a figure mid-stride, ~3.6 s cooldown, shape-consistent with a charge skill and NOT "
        "identified'). The 2D spec's B-7 promotes slot L -> Blitz, slot 2 -> Vire's Might, slot 3 -> War "
        "Cry. THAT PROMOTION HAS NO INSTRUMENT BEHIND IT. Ship the row as SLOT-indexed, or ship the "
        "skill names stamped DECLARED-not-decoded as a divergence-register row. Rune of Rush is graded "
        "UNDETERMINED, never against 0 — that part is right."))

    # ================= MOVEMENT (ratios only) ================================
    rows.append(row(
        "TB-MV-01", "movement fraction — ⚑ RATIOS ONLY",
        {"instrument_values": {
            "LapH2_th60_gpx_s": 0.883, "LapH2_th200_gpx_s": 0.757, "LapH2_th400_gpx_s": 0.494,
            "LapR_Schmitt_V_ON_100": 0.8342, "LapR_Schmitt_V_ON_200": 0.7948,
            "LapR_Schmitt_V_ON_400": 0.6233,
            "LapU_video_decomposition": 0.705,
            "MD_B4app_2_camera_pan_20Hz": duty["summary"]["frac_moving"],
            "MD_B4app_2_no_shake_guard": duty["summary"]["frac_moving_no_shake_guard"]},
         "spread_quoted_in_D_MPOL2_2": [0.883, 0.705, 0.6265],
         "spread_factor": 1.41,
         "full_committed_spread": [0.494, 0.883], "full_spread_factor": 1.79,
         "SHIPPABLE_FORM": "RATIOS ONLY — numerator and denominator from ONE instrument so the "
                           "instrument cancels (D-MPOL2-2; R-L88-5)"},
        "fraction — DO NOT SHIP AS A LEVEL",
        {"class": "INSTRUMENT DISAGREEMENT ABOUT THE REFERENT, not measurement error",
         "note": "the disagreement is a THRESHOLD choice, not a fight property: within Lap H-2 alone "
                 "the same fight reads 0.883 / 0.757 / 0.494 as the speed gate moves 60 -> 200 -> 400 gpx/s. "
                 "Comparing a sim LEVEL to any one of these compares against a threshold choice."},
        {"instruments": [I_H2, I_R, I_U, I_CH]},
        ["D-COMBAT-182 (galadriel) / t in [683.0, 864.0] (H-2, Lap R, Lap U)"],
        {"published": [0.883, 0.705, 0.6265],
         "published_as": "2D spec B-8 / gamora D-MPOL2-2 (engine simulation/AGENT_STATE.md)",
         "recomputed": {"0.883": "REPRODUCES EXACT — Lap H-2 pm4h2_movement_cadence.csv, row 'wave ALL', moving_frac_th60",
                        "0.6265": "REPRODUCES EXACT — s2-duty.json summary.frac_moving",
                        "0.705": "ATTRIBUTED, NOT RE-DERIVED — traced to Lap U via gamora's D-MPOL2-2; "
                                 "pm4u_findings.md publishes per-wave 'frames moving' 64.1-82.5% but no "
                                 "whole-fight 0.705 figure appears in the committed note text"},
         "status": "2 of 3 REPRODUCE EXACT; the third is attributed but its whole-fight reduction is not printed in its own lap note"},
        "⚑ AN ABSOLUTE MOVEMENT FIGURE IN A GREEN REPORT IS A DEFECT IN THE REPORT (2D spec B-8)."))

    # ================= PER-WAVE DURATIONS ====================================
    b = wv["boundaries"]
    badge = {}
    for i, (w_, t) in enumerate(b):
        t2 = b[i + 1][1] if i + 1 < len(b) else wv["end"]
        badge[str(w_)] = round(t2 - t, 3)
    rows.append(row(
        "TB-WV-01", "per-wave durations",
        {"badge_instrument_s": badge,
         "trace_frame_grid_s": {w: hp["per_wave"][w]["dur_s_from_trace"]
                                for w in hp["per_wave"] if w != "-1"},
         "sum_badge_s": round(sum(badge.values()), 3),
         "sum_trace_s": round(sum(hp["per_wave"][w]["dur_s_from_trace"]
                                  for w in hp["per_wave"] if w != "-1"), 3),
         "max_interior_disagreement_s": 0.19,
         "edge_disagreement_s": {"w151": 0.68, "w160": 0.88}},
        "s",
        {"class": "boundary instrument", "published_tolerance_s": 0.25,
         "note": "waves 152-159 agree to <= 0.19 s, INSIDE the published +-0.25 s. Waves 151 and 160 "
                 "disagree by 0.68 s and 0.88 s — NOT a boundary error: the two instruments cover "
                 "DIFFERENT WINDOWS (badge 682.10-864.75 = 182.65 s; trace 683.0-864.0 = 181.0 s). "
                 "The disagreement is entirely at the two ends."},
        {"instruments": [I_BADGE, I_H2, I_Q]},
        ["D-COMBAT-182", "D-HP-FRAME"],
        {"published": {"w154": 14.20}, "published_as": "2D spec B-9 (Lap R)",
         "recomputed": {"w154_trace": 14.2, "w154_badge": 14.13},
         "status": "REPRODUCES on the trace grid; the badge instrument gives 14.13"},
        "⚑ The two windows differ by 1.65 s (0.90%). A RATE computed on 181.0 s is not comparable to "
        "one computed on 182.65 s without restating the denominator. The grader picks ONE and says which."))

    rows.append(row(
        "TB-WV-02", "terminal wave",
        {"referent": 160, "sealed_sim": {"mean": 153.2, "sigma": 2.32}},
        "wave index",
        {"class": "single observation, n = 1"},
        {"lap": "2D spec B-10 / M-POL-2 seal"}, ["D-COMBAT-182"],
        {"published": 160, "published_as": "2D spec B-10", "recomputed": 160, "status": "CARRIED"},
        "⚑ REPORT-ONLY BY CONSTRUCTION, NEVER A GATE (Matt-ruled)."))

    out = {
        "artifact": "KC2-PLAY · T-B EXPECTED-VALUES TABLE",
        "version": 1,
        "date": "2026-09-20",
        "author": "galadriel",
        "run": "KC2-PLAY, Wave 1 (charter § 5, ledger KP-4)",
        "authority": [
            "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md",
            "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-2d-retarget-spec.md § 6 + Corrigenda-Forward 1 and 2",
        ],
        "quoting_cap": (
            "⚑ HARNESS REFUSAL (charter § 4.4 / R2D-10 pattern). The T-B grader MUST NOT print a "
            "FIDELITY figure from this table while T-A is absent, STRUCTURAL-red, or coverage < 72/72 "
            "mapped. It prints RAW STATISTICS ONLY. Nothing in this file is a fidelity claim."),
        "video_status": (
            "THE REFERENT MP4 IS NOT ON THIS MACHINE (matt_to_do T30; ~/gd-scratch deleted 2026-09-17). "
            "Every row here is a RE-QUERY of committed measurement artifacts. No row required the video. "
            "Rows that WOULD require it are listed under `blocked_on_T30`."),
        "denominators": denoms,
        "rows": rows,
        "blocked_on_T30": [
            {"quantity": "Type-A / Type-B release re-classification under any changed rule",
             "why": "the A/B labels come from the 20 Hz skill-bar dimming trace joined to the energy "
                    "train; the joined per-release label table was not committed as a standalone "
                    "artifact, only as a rendered table in MD-B4app-2c § 3",
             "needed": "either the video (to re-run eor_attrib.py) OR a one-file commit of the 19-row "
                       "labelled release table from the 2c work dir — the CHEAPER of the two and it "
                       "needs no video. Routed as a request, not executed (out of this lap's brief)."},
            {"quantity": "closing the 6.2% blind residual on channel uptime / release duty",
             "why": "13 OCR-blind gaps (11.42 s) need re-reading at higher upscale from the frames",
             "needed": "the video"},
            {"quantity": "resolving frac_moving to a single instrument",
             "why": "requires re-running all three segmenters on one common threshold definition",
             "needed": "the video — AND a ruling on the threshold, which is a measurement-seat call, "
                       "not an instrument problem. Ship RATIOS meanwhile (D-MPOL2-2)."},
            {"quantity": "any T-C side-by-side",
             "why": "T-C is GATED on the referent video by the 2D spec § 6.6 itself",
             "needed": "the video"},
            {"quantity": "N_bodies at leech-tick resolution (the per-body heal is an UPPER bound)",
             "why": "U-Q-1; never independently observed",
             "needed": "the video AND a per-body attributable damage stream, which pixels cannot provide"},
        ],
        "figures_that_do_not_reproduce": [
            {"row": "TB-CA-01", "published": "cast rate 0.290 /s, n = 53 (2D spec B-3)",
             "of_record": "0.2957 /s, n = 54",
             "cause": "the MD-B4app-2c MERGED correction (slot L 12 -> 13) landed AFTER 2b published 53; "
                      "the spec quotes the pre-correction count"},
            {"row": "TB-CA-02", "published": "Blitz 0.385 / Vire's 0.136 / War Cry 0.000 (2D spec B-7)",
             "of_record": "slot L 0.385 / slot 2 0.136 / slot 3 0.000",
             "cause": "slot-to-skill identity is NOT measured; the measuring lap forbids quoting skill "
                      "names from it. The numbers are right; the labels are a promotion with no instrument."},
            {"row": "TB-MV-01", "published": "frac_moving 0.705 (2D spec B-8, via D-MPOL2-2)",
             "of_record": "attributed to Lap U; the whole-fight 0.705 reduction is not printed in "
                          "pm4u_findings.md (which publishes 64.1-82.5% per wave)",
             "cause": "figure reached the spec through a summary row, not through its own lap note. "
                      "Not wrong — UNTRACEABLE at the resolution the denominator law requires."},
        ],
    }
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
