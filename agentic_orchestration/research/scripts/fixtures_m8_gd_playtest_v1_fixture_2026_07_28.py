#!/usr/bin/env python3
"""M8 -- fixtures-v0.5 -- GD play-test v1 measured fixture ingest (G-3 / KC1-2026-07-27 P-1).

Part 1 of 2. This part applies the DDL, seeds measure_dict, and lands the two
measured SERIES (T-A panel counters, T-B health-globe frames) plus the regime and
segmentation definitions they will be partitioned by.

Part 2 (fixtures_m8b_*.py) lands the engagement grain, the rollup grain, the fixture
identity, the conditions and the evidence claims -- all of which are partitions OF
what this script banks, and all of which are re-runnable without touching it.

Sources (all committed, all read-only here):
  S-A  galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-raw.jsonl.gz   (13,633)
  S-A' galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv      (13,633)
  S-A" galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-summary.json
  S-B  galadriel/captures/2026-07-26-gd-playtest-v1-tb/tb-intake-frames.jsonl.gz (19,348)
"""

import csv
import gzip
import json
import os
import shutil
import sqlite3
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB = os.path.join(ROOT, "agentic_orchestration/research/curated/fixtures.db")
DDL = os.path.join(ROOT, "agentic_orchestration/research/scripts/fixtures_v0_5_ddl.sql")
CAP = os.path.join(ROOT, "agentic_orchestration/galadriel/captures")
TA = os.path.join(CAP, "2026-07-26-gd-playtest-v1")
TB = os.path.join(CAP, "2026-07-26-gd-playtest-v1-tb")

SESSION = "GP-gd-2026-07-26-s1"
SERIES_A = "T-A-panel"
SERIES_B = "T-B-globe"
VERSION = "fixtures-v0.5"

# CSV column -> (measure_key, measure_subkey). The subkey convention is the .dbr
# record path, matching session_ledger and corpus.db exact_skill.record_path.
SKILL_PATH = {
    "defaultkickattack": "records/skills/default/defaultkickattack.dbr",
    "defaultweaponattack": "records/skills/default/defaultweaponattack.dbr",
    "onslaught": "records/skills/playerclass10/onslaught.dbr",
    "werewolf1": "records/skills/playerclass10/werewolf1.dbr",
    "werewolf1_skill01_claws": "records/skills/playerclass10/werewolf1_skill01_claws.dbr",
    "werewolf1_skill02_charge": "records/skills/playerclass10/werewolf1_skill02_charge.dbr",
}
SCALAR = {
    "kills": "kills",
    "deaths": "deaths",
    "max_level": "max_level_achieved",
    "life_healed": "life_healed",
    "total_score": "total_score",
    "health_potions": "health_potions_used",
    "mana_potions": "mana_potions_used",
    "dps": "dps_field",
    "shield_block_chance": "shield_block_chance",
}

# --- new measure_dict entries -------------------------------------------------
# (key, label, unit, value_kind, layer, requires_coverage, definition, confounds,
#  semantics_status, semantics_note, derivation, depends_on)
NEW_MEASURES = [
    ("engagement_count", "Engagements", "count", "counter", "derived", 0,
     "Count of engagement windows produced by a named segmentation_run.",
     "Entirely a function of the segmentation rule. Not comparable across segmentation_ids.",
     "settled", None, "COUNT(fixture_trial) per regime per segmentation_run", "kills"),
    ("engagement_seconds", "Engagement duration", "s", "gauge", "observed", 0,
     "Wallclock span from first to last kill event in the window, on the camera clock.",
     "0.5 s panel sampling quantises this; a 4.5 s median engagement is 9 samples "
     "(~11% quantisation, verdict sec 4). Duration is measured between KILL EVENTS, "
     "so it excludes approach and any post-last-kill combat.",
     "settled", "The TTK-shape carrier. PRIMARY accountability target per R-KC1-2.",
     None, None),
    ("kills_per_engagement", "Kills per engagement", "count", "gauge", "derived", 0,
     "Kills attributed to the window divided by one.",
     "Confounds three separable causes: pack size, dash-chaining, AoE proficiency. "
     "The 3.3 -> 8.4 -> 11.9 regime progression is NOT a clean build-power signal.",
     "contested",
     "PROVISIONAL as an accountability target per Matt ruling R-KC1-2, pending the "
     "G-2b causal decomposition. Do not band. Do not headline.",
     "kills / engagement", "kills"),
    ("intake_hp", "Damage intake", "HP", "counter", "observed", 1,
     "Sum of admissible negative HP deltas across a window, health-globe numerals at 15 fps.",
     "Zero-inflated. Deltas never cross an unreadable break >2 s. Refusals are not "
     "interpolated, so an intake figure is a LOWER bound on true intake within its coverage.",
     "settled", None, None, None),
    ("healed_hp", "In-combat healing", "HP", "counter", "observed", 1,
     "Sum of admissible positive HP deltas across a window.",
     "Contaminated by three single-frame full-restore events (see C-RESTORE-ON-LOAD). "
     "Intake is unaffected -- it is a strictly negative-delta quantity.",
     "contested", "restore-on-load vs Constitution regen unresolved (verdict sec 9).",
     None, None),
    ("hp_drop_count", "Damage-intake events", "count", "counter", "observed", 1,
     "Count of admissible negative HP delta events in the window.", None,
     "settled", None, None, None),
    ("hp_drop_max", "Largest single intake event", "HP", "gauge", "observed", 1,
     "Largest single admissible negative HP delta in the window.",
     "The tail carries the signal: 27 R2 drops >=10% EHP carry 46.8% of R2 intake.",
     "settled", None, None, None),
    ("hp_drop_p50", "Median intake event", "HP", "gauge", "observed", 1,
     "Median admissible negative HP delta in the window.", None, "settled", None, None, None),
    ("hp_drop_size", "Intake event size", "HP", "gauge", "observed", 1,
     "Distribution of individual admissible negative HP deltas, regime grain.", None,
     "settled", None, None, None),
    ("hp_drop_pc_ehp", "Intake event size, %EHP", "pct", "gauge", "derived", 1,
     "hp_drop_size normalised by the window's observed max HP.",
     "Denominator is a LOWER bound on true max HP.", "settled", None,
     "drop_hp / hp_max_observed", "hp_drop_size,hp_max_observed"),
    ("hp_drop_count_ge_10pc_ehp", "Intake events >=10% EHP", "count", "counter", "derived", 1,
     "Count of drops at or above one tenth of observed max HP.", None, "settled",
     "The R2 tail. 27 events. Tune against these.", None, "hp_drop_size,hp_max_observed"),
    ("frac_intake_from_drops_ge_10pc_ehp", "Share of intake from >=10% EHP drops",
     "frac", "gauge", "derived", 1,
     "Fraction of regime intake carried by drops at or above 10% of observed max HP.",
     None, "settled", None, None, "hp_drop_size,intake_hp"),
    ("drop_events_per_covered_s", "Intake events per covered second", "count/s", "gauge",
     "derived", 1, "Drop events divided by admissible pair-time.", None, "settled",
     "The hazard-frequency axis. Rises 0.186 -> 0.400 -> 0.655 across regimes.",
     "hp_drop_count / covered_s", "hp_drop_count"),
    ("hp_max_observed", "Observed max HP", "HP", "gauge", "observed", 1,
     "Modal max-HP denominator read in the window.",
     "A LOWER BOUND on true max HP. Moves 250 -> 1600 across the run, so absolute HP "
     "is not comparable between regimes.", "settled", None, None, None),
    ("hp_min_observed", "Lowest HP reached", "HP", "gauge", "observed", 1,
     "Minimum accepted HP read in the window.",
     "Conditioned on coverage; the true minimum may sit inside a refusal.",
     "settled", None, None, None),
    ("intake_pc_ehp", "Intake, %EHP", "pct", "gauge", "derived", 1,
     "intake_hp as a percentage of observed max HP.", None, "settled", None,
     "intake_hp / hp_max_observed", "intake_hp,hp_max_observed"),
    ("intake_hp_per_s", "Intake rate", "HP/s", "gauge", "derived", 1,
     "intake_hp per COVERED second (admissible pair-time), not per wallclock second.",
     "Rates and totals use different inclusion rules and are never mixed (galadriel sec 6).",
     "settled", None, "intake_hp / covered_s", "intake_hp"),
    ("intake_pc_ehp_per_s", "Intake rate, %EHP/s", "pct/s", "gauge", "derived", 1,
     "intake_pc_ehp per covered second.", None, "settled", None, None,
     "intake_hp,hp_max_observed"),
    ("healed_hp_per_s", "Healing rate", "HP/s", "gauge", "derived", 1,
     "healed_hp per covered second.", None, "contested",
     "Carries the restore-on-load contamination.", "healed_hp / covered_s", "healed_hp"),
    ("intake_per_kill", "Intake per kill", "HP/kill", "gauge", "derived", 1,
     "intake_hp divided by kills in the same window.", None, "settled", None,
     "intake_hp / kills", "intake_hp,kills"),
    ("intake_per_kill_pc_ehp", "Intake per kill, %EHP", "pct/kill", "gauge", "derived", 1,
     "intake_per_kill normalised by observed max HP.", None, "settled", None, None,
     "intake_hp,kills,hp_max_observed"),
    ("damage_spent", "Damage spent", "dmg", "gauge", "derived", 1,
     "Integral of the trailing rolling-mean dps field over the window plus kernel K.",
     "The dps kernel is 5.0 s (p50, measured over 22 clean falling edges), so a 4.5 s "
     "engagement's integral leaks into its neighbour's. Per-engagement attribution below "
     "12 s is NOT supported; use the merged-interval aggregate.",
     "contested",
     "An OVERKILL-INFLATED UPPER BOUND on monster EHP. It is inflated by overkill, by "
     "damage to monsters that die outside the window, and by anything that misses. "
     "494.2 does NOT mean an R2 monster has 494 health.",
     "integral(rolling_mean(dps_field), t_start, t_end+K)", "dps_field"),
    ("damage_per_kill", "Damage spent per kill", "dmg/kill", "gauge", "derived", 1,
     "damage_spent divided by kills, long-engagement (>=12 s) subset.",
     "Same upper-bound caveat as damage_spent, on a small n (R2 n=8, R3 n=3).",
     "contested", "UPPER BOUND. See damage_spent.", "damage_spent / kills",
     "damage_spent,kills"),
    ("damage_per_kill_merged", "Damage per kill, merged intervals", "dmg/kill", "gauge",
     "derived", 1,
     "Overlapping engagement windows merged, then total damage / total kills. Immune to "
     "the kernel attribution problem; covers 612 of R2's 647 kills.",
     "Still an upper bound. Kernel sensitivity K=5.0->7.5 s moves R2 by 1.9%.",
     "contested", "The better of the two damage estimators. Still an UPPER BOUND.",
     "merged_damage_total / merged_kills", "damage_spent,kills"),
]


def log(msg):
    print(f"[m8] {msg}", flush=True)


def has_column(cx, table, col):
    return col in {r[1] for r in cx.execute(f"PRAGMA table_info({table})")}


def backup():
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dst = f"{DB}.pre-v0.5-{ts}-backup"
    shutil.copy2(DB, dst)
    log(f"backup -> {os.path.basename(dst)}")
    return dst


def apply_ddl(cx):
    if has_column(cx, "fixture_trial", "segmentation_id"):
        log("DDL already applied (fixture_trial.segmentation_id present) -- skipping")
        return False
    with open(DDL) as f:
        cx.executescript(f.read())
    log("DDL fixtures-v0.5 applied")
    return True


def seed_measures(cx):
    for (k, label, unit, kind, layer, reqcov, definition, confounds,
         sem_status, sem_note, derivation, depends) in NEW_MEASURES:
        cx.execute("""
            INSERT INTO measure_dict
              (measure_key, label, unit, value_kind, lane_availability, layer,
               requires_coverage, definition, confounds, semantics_status,
               semantics_note, derivation, depends_on)
            VALUES (?,?,?,?, 'both', ?,?,?,?,?,?,?,?)
            ON CONFLICT(measure_key) DO UPDATE SET
              label=excluded.label, unit=excluded.unit, value_kind=excluded.value_kind,
              layer=excluded.layer, requires_coverage=excluded.requires_coverage,
              definition=excluded.definition, confounds=excluded.confounds,
              semantics_status=excluded.semantics_status,
              semantics_note=excluded.semantics_note, derivation=excluded.derivation,
              depends_on=excluded.depends_on
        """, (k, label, unit, kind, layer, reqcov, definition, confounds,
              sem_status, sem_note, derivation, depends))
    log(f"measure_dict: {len(NEW_MEASURES)} keys upserted "
        f"(total now {cx.execute('SELECT COUNT(*) FROM measure_dict').fetchone()[0]})")


REGIMES = [
    ("R1", 1, 358, 1134, "four-skill pre-transform (weapon attack, kick, onslaught)",
     "C-2 correction, verdict sec 2: defaultweaponattack climbs one at a time 61->74 "
     "between play_time 1019 and 1134; onslaught bursts 47->54 by 1145; then 11,486 "
     "consecutive samples read exactly 74. Verified a clean climb, not an OCR jump. "
     "Supersedes the spot-sampled 1757.",
     "MEASURED", "report-only",
     "43 kills over 13 engagements is an anecdote about the opening nineteen minutes "
     "(verdict sec 3). Report it; do not fit it. Ruling R-KC1-2."),
    ("R2", 2, 1134, 6052, "two-skill werewolf (claws + charge)",
     "Lower edge = the C-2 build break at 1134. Upper edge = the C-1 corrected gear-gated "
     "poison-DoT boundary.",
     "MEASURED", "fixture",
     "647 kills over 77 engagements, the run's only real distribution, and the span where "
     "the build stopped moving. THE fixture per ruling R-KC1-1."),
    ("R3", 3, 6052, 7094, "werewolf + gear-gated poison DoT",
     "C-1 correction, verdict sec 2: the DoT is gear-gated, not level-gated. Gear equip "
     "BRACKETS to play_time 6052-6282 (level 11); the boundary is banked at the bracket's "
     "LOWER edge. A `WHERE play_time < 6816` filter would leave 178 poison-DoT kills inside "
     "the pre-DoT pool.",
     "DERIVED", "secondary",
     "190 kills over 16 engagements -- thin in engagements, rich in kills. Usable with its "
     "own error bars, and with the declared coverage hole (C-R3-COV-HOLE). Ruling R-KC1-2 "
     "grades it report-only as an accountability target."),
]


def land_regimes(cx):
    cx.execute("DELETE FROM session_regime WHERE session_id=?", (SESSION,))
    for key, ordinal, lo, hi, build, ev, grade, role, rationale in REGIMES:
        cx.execute("""
            INSERT INTO session_regime
              (regime_id, session_id, regime_key, regime_ordinal, play_time_s_lo,
               play_time_s_hi, build_label, build_break_evidence, boundary_grade,
               distribution_role, distribution_role_rationale, source_ref)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (f"{SESSION}/{key}", SESSION, key, ordinal, lo, hi, build, ev, grade,
              role, rationale,
              "gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md sec 2-3"))
    log("session_regime: 3 rows (R1 report-only / R2 fixture / R3 secondary)")


def land_segmentation(cx):
    win = json.load(open(os.path.join(TB, "tb-engagement-windows.json")))
    seg_id = f"{SESSION}/S1-gap5s-v1"
    cx.execute("DELETE FROM segmentation_run WHERE segmentation_id=?", (seg_id,))
    cx.execute("""
        INSERT INTO segmentation_run
          (segmentation_id, session_id, segmentation, rule_text, params_json,
           derived_from, n_engagements, n_kills, dur_median_s, dur_mean_s, dur_max_s,
           authored_by, authored_date, ruling_ref, status, reproduction_note, source_ref)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        seg_id, SESSION, "S1-kill-to-kill",
        "An engagement boundary falls wherever the inter-KILL-EVENT gap on the gated "
        "monotonic kills series exceeds 5.0 s. Capture windows pad 3.0 s each side. "
        "Duration is measured first-kill-event to last-kill-event, not approach to death.",
        json.dumps({"gap_threshold_s": win["gap_threshold_s"], "pad_s": win["pad_s"],
                    "series": "kills (gated, monotonic)", "sampling_s": 0.5}),
        "galadriel/captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv",
        win["n_engagements"], win["total_kills"], win["dur_median"], win["dur_mean"],
        win["dur_max"], "galadriel (tb_windows.py), reproducing gandalf verdict sec 4",
        "2026-07-27",
        "verdict sec 4. THE GRAIN IS NOT YET RULED: charter HALT H-1 places the "
        "engagement-grain ruling with Matt, WITH the G-2b decomposition in hand. This row "
        "is the cut every current figure was computed on, not a ratified definition.",
        "current",
        "Reproduced independently from the committed T-A ledger before any downstream work "
        "was permitted: 106 engagements, median 4.5 s, mean 6.151, max 37.5, and the sec 3 "
        "regime table cell-for-cell (R1 13/43, R2 77/647, R3 16/190).",
        "galadriel/captures/2026-07-26-gd-playtest-v1-tb/tb-engagement-windows.json"))
    log(f"segmentation_run: {seg_id} (status=current, grain ruling GATED at H-1)")
    return seg_id


def regime_of(pt_s):
    """Half-open [lo, hi) throughout, EXCEPT the terminal regime, which is closed [lo, hi].
    The run's last 11 samples read play_time exactly 7094 -- R3's stated upper bound. Under
    a uniform half-open rule they would fall out of every regime, which is a silent loss of
    real samples at the one boundary that is an endpoint rather than a build change. The
    verdict's numbers are left exactly as written; the rule carries the exception instead."""
    if pt_s is None:
        return None
    for idx, (key, _o, lo, hi, *_) in enumerate(REGIMES):
        last = idx == len(REGIMES) - 1
        if lo <= pt_s <= hi if last else lo <= pt_s < hi:
            return f"{SESSION}/{key}"
    return None


def land_panel_series(cx):
    """T-A: 13,633 samples. Raw jsonl carries what the reader SAW; the gated CSV carries
    what the monotonic gate ACCEPTED. The difference is a rejection, and the rejection
    keeps its raw value."""
    gated = {}
    with open(os.path.join(TA, "ta-full-2fps-gated.csv")) as f:
        for row in csv.DictReader(f):
            gated[int(row["i"])] = row

    cx.execute("DELETE FROM panel_series_reading WHERE session_id=? AND series=?",
               (SESSION, SERIES_A))
    cx.execute("DELETE FROM panel_series_sample WHERE session_id=? AND series=?",
               (SESSION, SERIES_A))

    samples, readings = [], []
    with gzip.open(os.path.join(TA, "ta-full-2fps-raw.jsonl.gz"), "rt") as f:
        for line in f:
            o = json.loads(line)
            i = o["i"]
            g = gated[i]

            # -- play_time lives on the sample row: it is the join key, not a reading.
            raw_pt = o.get("play_time")
            acc_pt = g["play_time"].strip()
            if acc_pt != "":
                pt_status, pt_ms = "accepted", int(float(acc_pt)) * 1000
            elif raw_pt is not None:
                pt_status, pt_ms = "rejected-nonmonotonic", None
            else:
                pt_status, pt_ms = "missing", None
            samples.append((SESSION, SERIES_A, i, int(round(o["pts_s"] * 1000)), pt_ms,
                            pt_status, raw_pt, o.get("play_time_conf"), o.get("status"),
                            o.get("L"), regime_of(pt_ms / 1000 if pt_ms is not None else None)))

            for col, mk in SCALAR.items():
                raw = o.get(col)
                if raw is None:
                    continue                      # refusal: absent, never interpolated
                acc = g.get(col, "").strip()
                if acc != "":
                    readings.append((SESSION, SERIES_A, i, mk, "", "accepted",
                                     float(acc), float(raw), o.get(col + "_conf"), None))
                else:
                    readings.append((SESSION, SERIES_A, i, mk, "", "rejected-nonmonotonic",
                                     None, float(raw), o.get(col + "_conf"), None))
            for col, path in SKILL_PATH.items():
                sk = (o.get("skills") or {}).get(col)
                if sk is None or sk.get("count") is None:
                    continue
                acc = g.get(col, "").strip()
                readings.append((
                    SESSION, SERIES_A, i, "skill_use_count", path,
                    "accepted" if acc != "" else "rejected-nonmonotonic",
                    float(acc) if acc != "" else None, float(sk["count"]),
                    sk.get("conf"), sk.get("path_corr")))

    cx.executemany("""INSERT INTO panel_series_sample
        (session_id, series, sample_ordinal, pts_ms, play_time_ms, play_time_read_status,
         play_time_raw, play_time_confidence, frame_status, panel_luma, regime_id)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""", samples)
    cx.executemany("""INSERT INTO panel_series_reading
        (session_id, series, sample_ordinal, measure_key, measure_subkey, read_status,
         value_num, value_raw, read_confidence, path_corr)
        VALUES (?,?,?,?,?,?,?,?,?,?)""", readings)
    log(f"panel_series_sample: {len(samples)} rows · panel_series_reading: {len(readings)} rows")
    return len(samples), len(readings)


def land_globe_series(cx):
    """T-B: 19,348 decoded frames INCLUDING refusals -- the refusal code IS the coverage."""
    # guard: v0.5.0 keyed this table on pts alone, which silently dropped the 48 frames
    # that sit inside two adjacent padded windows. Recreate from the DDL when seen.
    sql = cx.execute("SELECT sql FROM sqlite_master WHERE name='globe_series_frame'").fetchone()
    if sql and "PRIMARY KEY (session_id, series, eng_id, pts_ms)" not in sql[0]:
        cx.execute("DROP TABLE globe_series_frame")
        ddl = open(DDL).read()
        blk = ddl[ddl.index("CREATE TABLE IF NOT EXISTS globe_series_frame"):]
        cx.executescript(blk[:blk.index("-- ------", 10)])
        log("globe_series_frame recreated with eng_id in the primary key")
    cx.execute("DELETE FROM globe_series_frame WHERE session_id=? AND series=?",
               (SESSION, SERIES_B))
    rows = []
    with gzip.open(os.path.join(TB, "tb-intake-frames.jsonl.gz"), "rt") as f:
        for line in f:
            o = json.loads(line)
            rows.append((SESSION, SERIES_B, int(round(o["t"] * 1000)), o.get("hp"),
                         o.get("raw"), o.get("conf"), o["st"],
                         "greedy-fallback" if o.get("g") else "validated", o.get("eng")))
    cx.executemany("""INSERT INTO globe_series_frame
        (session_id, series, pts_ms, hp_current, hp_raw, read_confidence, refusal_code,
         reader_path, eng_id) VALUES (?,?,?,?,?,?,?,?,?)""", rows)
    log(f"globe_series_frame: {len(rows)} rows "
        f"({sum(1 for r in rows if r[6] != 'OK')} refusals kept, 0 interpolated)")
    return len(rows)


def stamp(cx, note):
    cx.execute("INSERT INTO schema_meta (version, applied_utc, note) VALUES (?,?,?)",
               (VERSION, datetime.now(timezone.utc).isoformat(timespec="seconds"), note))


def main():
    if not os.path.exists(DB):
        sys.exit(f"missing {DB}")
    backup()
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys = ON")
    try:
        fresh = apply_ddl(cx)
        cx.execute("BEGIN")
        # Re-run is idempotent, but the deletes must run in dependency order or the
        # FKs from the series tables into session_regime block the rebuild.
        for stmt in ("DELETE FROM panel_series_reading WHERE session_id=?",
                     "DELETE FROM panel_series_sample WHERE session_id=?",
                     "DELETE FROM globe_series_frame WHERE session_id=?"):
            cx.execute(stmt, (SESSION,))
        seed_measures(cx)
        land_regimes(cx)
        seg_id = land_segmentation(cx)
        land_panel_series(cx)
        land_globe_series(cx)
        if fresh:
            stamp(cx, "M8 part 1. Measured-fixture layer: session_regime, segmentation_run, "
                      "panel_series_* (T-A), globe_series_frame (T-B), series_field_quality, "
                      "regime_stat, measured_fixture, fixture_target, fixture_condition, "
                      "evidence_claim. Coverage made structurally non-optional. "
                      "trial_measurement rebuilt: read_method CHECK -> FK to read_method_dict.")
        cx.commit()
    except Exception:
        cx.rollback()
        raise
    fk = list(cx.execute("PRAGMA foreign_key_check"))
    log(f"foreign_key_check: {'CLEAN' if not fk else fk[:5]}")
    log(f"segmentation of record: {seg_id}")
    cx.close()


if __name__ == "__main__":
    main()
