#!/usr/bin/env python3
"""M8 part 2 -- the engagement grain + the quality ledger (G-3 / KC1-2026-07-27 P-1).

Lands, all as PARTITIONS of the series banked by part 1:
  * 106 engagements as fixture_trial rows, regime-stamped, pinned to a segmentation_run
  * their measurements in trial_measurement, each coverage-bearing figure carrying its
    own coverage (the schema will ABORT the insert otherwise)
  * series_field_quality at THREE grains -- session, regime, engagement -- with the
    same columns at each, so the same question can be asked at any grain

Re-run is idempotent and scoped to one segmentation_id: a G-2b re-cut lands as a NEW
segmentation_run and leaves these rows untouched.
"""

import csv
import json
import os
import sqlite3
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB = os.path.join(ROOT, "agentic_orchestration/research/curated/fixtures.db")
CAP = os.path.join(ROOT, "agentic_orchestration/galadriel/captures")
TA = os.path.join(CAP, "2026-07-26-gd-playtest-v1")
TB = os.path.join(CAP, "2026-07-26-gd-playtest-v1-tb")

SESSION = "GP-gd-2026-07-26-s1"
SEG = f"{SESSION}/S1-gap5s-v1"
SERIES_A, SERIES_B = "T-A-panel", "T-B-globe"
SRC_TB = "galadriel/captures/2026-07-26-gd-playtest-v1-tb/tb-rollup.json"
SRC_TA = "galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-summary.json"

# Deaths on the game clock (T-A summary). An engagement containing one is 'player-died'.
DEATH_PTS = [2837.0, 5151.5]


def log(m):
    print(f"[m8b] {m}", flush=True)


def trial_id(eng_id):
    return f"{SEG}/e{eng_id:03d}"


# --- engagement measurements ---------------------------------------------------
# (measure_key, csv_field, phase, read_method, coverage_field, coverage_basis)
# coverage_field=None means the measure_dict entry does not require coverage.
COV_FRAME = ("coverage", "T-B frame coverage: decoded frames returning an accepted read "
                        "/ frames decoded. THE GATE COVERAGE (totals require >= 0.80).")
COV_DPS = ("damage_dps_coverage", "fraction of the dps-field integration window covered "
                                  "by accepted panel reads")

# trial_measurement.coverage carries FRAME coverage on every globe-derived figure,
# because frame coverage is what the >=0.80 totals gate is defined on -- a consumer
# filtering on this column reproduces galadriel's inclusion sets exactly. DELTA coverage
# is a different quantity (admissible pair-time) and lives in series_field_quality as
# covered_s / wallclock_s. Storing delta here and calling it 'coverage' silently moves
# one R2 and one R3 engagement into the totals (63/10 instead of 62/9) and shifts the
# R3 mean from 163.3 to 188.4. Verified empirically before this line was written.
ENG_MEASURES = [
    ("intake_hp", "intake_hp", "during", "video-frame-ocr", COV_FRAME),
    ("healed_hp", "healed_hp", "during", "video-frame-ocr", COV_FRAME),
    ("hp_drop_count", "n_drops", "during", "video-frame-ocr", COV_FRAME),
    ("hp_drop_max", "drop_max", "during", "video-frame-ocr", COV_FRAME),
    ("hp_drop_p50", "drop_p50", "during", "video-frame-ocr", COV_FRAME),
    ("hp_max_observed", "hp_max_seen", "during", "video-frame-ocr", COV_FRAME),
    ("hp_min_observed", "hp_min", "during", "video-frame-ocr", COV_FRAME),
    ("damage_spent", "damage_spent", "derived", "derived", COV_DPS),
]


def land_engagements(cx):
    rows = list(csv.DictReader(open(os.path.join(TB, "tb-rollup-engagements.csv"))))
    win = {w["eng_id"]: w for w in
           json.load(open(os.path.join(TB, "tb-engagement-windows.json")))["windows"]}
    assert len(rows) == 106, len(rows)

    cx.execute("DELETE FROM trial_measurement WHERE trial_id LIKE ?", (SEG + "/%",))
    cx.execute("DELETE FROM fixture_trial WHERE segmentation_id=?", (SEG,))

    # cumulative kills at each window edge, straight off the banked panel series --
    # gives v_trial_wide its before/after pair and an independent closure check.
    kills_at = {}
    for pt, v in cx.execute("""
            SELECT s.play_time_ms/1000, MAX(r.value_num)
            FROM panel_series_reading r JOIN panel_series_sample s
              ON s.session_id=r.session_id AND s.series=r.series
             AND s.sample_ordinal=r.sample_ordinal
            WHERE r.measure_key='kills' AND r.read_status='accepted'
              AND s.play_time_ms IS NOT NULL
            GROUP BY 1"""):
        kills_at[pt] = v

    def cum_kills(pt):
        keys = [k for k in kills_at if k <= pt]
        return kills_at[max(keys)] if keys else None

    n_meas = 0
    for r in rows:
        eng = int(r["eng_id"])
        w = win[eng]
        tid = trial_id(eng)
        died = any(w["pts_start"] <= d <= w["pts_end"] for d in DEATH_PTS)
        pt_lo, pt_hi = int(r["play_time_start"]), int(r["play_time_end"])
        cx.execute("""
            INSERT INTO fixture_trial
              (trial_id, session_id, fixture_set_id, trial_ordinal, lane, segmentation,
               segmentation_params, outcome, t_start_playtime_s, t_end_playtime_s,
               t_start_playtime_ms, t_end_playtime_ms, t_start_pts_ms, t_end_pts_ms,
               derived_from_ledger, segmentation_id, regime_id, notes)
            VALUES (?,?,NULL,?,'gd-live','S1-kill-to-kill',?,?,?,?,?,?,?,?,1,?,?,?)
        """, (tid, SESSION, eng,
              json.dumps({"gap_threshold_s": 5.0, "pad_s": 3.0}),
              "player-died" if died else "monster-killed",
              pt_lo, pt_hi, pt_lo * 1000, pt_hi * 1000,
              int(w["pts_start"] * 1000), int(w["pts_end"] * 1000),
              SEG, f"{SESSION}/{r['regime']}",
              f"capture window pts {w['cap_start']}-{w['cap_end']} "
              f"({w['cap_dur']} s incl. 3 s pad); n_events={w['n_events']}"))

        def put(mk, phase, val, rm, cov=None, basis=None, unc=None, note=None):
            nonlocal n_meas
            cx.execute("""INSERT INTO trial_measurement
                (trial_id, measure_key, measure_subkey, phase, value_num, unit,
                 read_method, uncertainty_abs, validity_note, coverage, coverage_basis,
                 evidence_grade)
                VALUES (?,?,'',?,?,(SELECT unit FROM measure_dict WHERE measure_key=?),
                        ?,?,?,?,?,?)""",
                (tid, mk, phase, val, mk, rm, unc, note, cov, basis,
                 "DERIVED" if rm == "derived" else "MEASURED"))
            n_meas += 1

        put("engagement_seconds", "during", float(r["dur_s"]), "video-frame-ocr",
            unc=0.5, note="first-to-last kill event on the 0.5 s panel clock; "
                          "+/-0.5 s quantisation")
        put("kills", "during", float(r["kills"]), "video-frame-ocr")
        put("kills_per_engagement", "derived", float(r["kills"]), "derived",
            note="PROVISIONAL accountability target per R-KC1-2 -- see C-KPE-PROVISIONAL")
        kb, ka = cum_kills(pt_lo), cum_kills(pt_hi)
        if kb is not None:
            put("kills", "before", kb, "video-frame-ocr")
        if ka is not None:
            put("kills", "after", ka, "video-frame-ocr")

        for mk, field, phase, rm, (covf, basis) in ENG_MEASURES:
            v = r[field]
            if v == "":
                continue
            put(mk, phase, float(v), rm, cov=float(r[covf]), basis=basis)

    log(f"fixture_trial: {len(rows)} engagements · trial_measurement: {n_meas} rows")
    return rows


# --- the quality ledger, three grains ------------------------------------------
def land_quality(cx, eng_rows):
    cx.execute("DELETE FROM series_field_quality WHERE scope_ref=? OR scope_ref LIKE ? "
               "OR scope_ref LIKE ?", (SESSION, f"{SESSION}/%", f"{SEG}/%"))

    def put(scope_kind, scope_ref, series, mk, subkey, n_samples, n_present, n_acc,
            n_rej, n_missing, greedy=None, hist=None, brk=None, src=None,
            covered_s=None, wallclock_s=None):
        cx.execute("""INSERT INTO series_field_quality
            (scope_kind, scope_ref, series, measure_key, measure_subkey, n_samples,
             n_present, n_accepted, n_rejected_nonmonotonic, n_missing, n_greedy_path,
             refusal_hist_json, unreadable_break_s, source_ref, covered_s, wallclock_s)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (scope_kind, scope_ref, series, mk, subkey, n_samples, n_present, n_acc,
             n_rej, n_missing, greedy, hist, brk, src, covered_s, wallclock_s))

    # -- T-A, session + regime + engagement grain, straight off the banked series.
    n_run = cx.execute("SELECT COUNT(*) FROM panel_series_sample WHERE session_id=?",
                       (SESSION,)).fetchone()[0]
    fields = list(cx.execute("""SELECT DISTINCT measure_key, measure_subkey
                                FROM panel_series_reading WHERE session_id=?""", (SESSION,)))

    def counts(where, params):
        d = {}
        for mk, sk, st, n in cx.execute(f"""
                SELECT r.measure_key, r.measure_subkey, r.read_status, COUNT(*)
                FROM panel_series_reading r JOIN panel_series_sample s
                  ON s.session_id=r.session_id AND s.series=r.series
                 AND s.sample_ordinal=r.sample_ordinal
                WHERE {where} GROUP BY 1,2,3""", params):
            d.setdefault((mk, sk), {})[st] = n
        return d

    run_c = counts("r.session_id=?", (SESSION,))
    for mk, sk in fields:
        c = run_c.get((mk, sk), {})
        acc, rej = c.get("accepted", 0), c.get("rejected-nonmonotonic", 0)
        put("session", SESSION, SERIES_A, mk, sk, n_run, acc + rej, acc, rej,
            n_run - acc - rej, src=SRC_TA)
    # play_time is a sample-row property, not a reading; account it explicitly.
    pt = dict(cx.execute("""SELECT play_time_read_status, COUNT(*) FROM panel_series_sample
                            WHERE session_id=? GROUP BY 1""", (SESSION,)))
    put("session", SESSION, SERIES_A, "play_time", "", n_run,
        pt.get("accepted", 0) + pt.get("rejected-nonmonotonic", 0), pt.get("accepted", 0),
        pt.get("rejected-nonmonotonic", 0), pt.get("missing", 0), src=SRC_TA)

    for (rid,) in cx.execute("SELECT regime_id FROM session_regime WHERE session_id=?",
                             (SESSION,)):
        n = cx.execute("SELECT COUNT(*) FROM panel_series_sample WHERE regime_id=?",
                       (rid,)).fetchone()[0]
        rc = counts("s.regime_id=?", (rid,))
        for mk, sk in fields:
            c = rc.get((mk, sk), {})
            acc, rej = c.get("accepted", 0), c.get("rejected-nonmonotonic", 0)
            put("regime", rid, SERIES_A, mk, sk, n, acc + rej, acc, rej, n - acc - rej,
                src="elrond M8b recompute over banked panel_series_*")

    for r in eng_rows:
        tid, lo, hi = trial_id(int(r["eng_id"])), int(r["play_time_start"]), int(r["play_time_end"])
        n = cx.execute("""SELECT COUNT(*) FROM panel_series_sample WHERE session_id=?
                          AND play_time_ms BETWEEN ? AND ?""",
                       (SESSION, lo * 1000, hi * 1000)).fetchone()[0]
        ec = counts("r.session_id=? AND s.play_time_ms BETWEEN ? AND ?",
                    (SESSION, lo * 1000, hi * 1000))
        for mk, sk in fields:
            c = ec.get((mk, sk), {})
            acc, rej = c.get("accepted", 0), c.get("rejected-nonmonotonic", 0)
            if acc + rej == 0 and n == 0:
                continue
            put("engagement", tid, SERIES_A, mk, sk, n, acc + rej, acc, rej,
                n - acc - rej, src="elrond M8b recompute over banked panel_series_*")

    # -- T-B, all three grains, from the banked globe frames + the reader's own rollup.
    roll = json.load(open(os.path.join(TB, "tb-rollup.json")))
    wins = {w["eng_id"]: w for w in roll["windows"]}
    tot = {"n": 0, "ok": 0, "greedy": 0, "cov_s": 0.0, "wall_s": 0.0}
    for r in eng_rows:
        eng = int(r["eng_id"])
        w = wins[eng]
        n, ok = int(r["n_frames_decoded"]), int(r["n_ok"])
        put("engagement", trial_id(eng), SERIES_B, "hp_current", "", n, ok, ok, 0, n - ok,
            greedy=int(r["n_greedy_path"]), hist=json.dumps(w.get("refusal_hist", {})),
            brk=float(r["unreadable_break_s"]), src=SRC_TB,
            covered_s=float(r["delta_covered_s"]), wallclock_s=float(w["cap_dur"]))
        tot["cov_s"] += float(r["delta_covered_s"])
        tot["wall_s"] += float(w["cap_dur"])
        tot["n"] += n
        tot["ok"] += ok
        tot["greedy"] += int(r["n_greedy_path"])
    rg_cov = {}
    for r in eng_rows:
        k = r["regime"]
        c, w2 = rg_cov.setdefault(k, [0.0, 0.0])
        rg_cov[k] = [c + float(r["delta_covered_s"]), w2 + float(wins[int(r["eng_id"])]["cap_dur"])]
    for key, rg in roll["regimes"].items():
        put("regime", f"{SESSION}/{key}", SERIES_B, "hp_current", "", rg["frames"],
            rg["frames_ok"], rg["frames_ok"], 0, rg["frames"] - rg["frames_ok"],
            greedy=rg["greedy_path_frames"],
            hist=json.dumps({"trunc_refusals": rg["trunc_refusals"],
                             "spike_refusals": rg["spike_refusals"]}),
            brk=float(rg["unreadable_break_s"]), src=SRC_TB,
            covered_s=round(rg_cov[key][0], 3), wallclock_s=round(rg_cov[key][1], 3))
    hist = dict(cx.execute("""SELECT refusal_code, COUNT(*) FROM globe_series_frame
                              WHERE session_id=? GROUP BY 1""", (SESSION,)))
    put("session", SESSION, SERIES_B, "hp_current", "", tot["n"], tot["ok"], tot["ok"], 0,
        tot["n"] - tot["ok"], greedy=tot["greedy"], hist=json.dumps(hist),
        brk=71.5, src=SRC_TB, covered_s=round(tot["cov_s"], 3),
        wallclock_s=round(tot["wall_s"], 3))

    n = cx.execute("SELECT COUNT(*) FROM series_field_quality").fetchone()[0]
    log(f"series_field_quality: {n} rows (session + regime + engagement grain)")


def main():
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys = ON")
    try:
        cx.execute("BEGIN")
        rows = land_engagements(cx)
        land_quality(cx, rows)
        cx.commit()
    except Exception:
        cx.rollback()
        raise
    fk = list(cx.execute("PRAGMA foreign_key_check"))
    log(f"foreign_key_check: {'CLEAN' if not fk else fk[:5]}")
    for rid, n, k in cx.execute("""SELECT regime_id, COUNT(*),
              SUM((SELECT value_num FROM trial_measurement m WHERE m.trial_id=t.trial_id
                   AND m.measure_key='kills' AND m.phase='during'))
           FROM fixture_trial t WHERE segmentation_id=? GROUP BY 1 ORDER BY 1""", (SEG,)):
        log(f"  {rid}: {n} engagements / {int(k)} kills")
    cx.close()


if __name__ == "__main__":
    main()
