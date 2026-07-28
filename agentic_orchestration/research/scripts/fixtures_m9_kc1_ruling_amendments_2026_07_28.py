#!/usr/bin/env python3
"""
M9 -- fixtures-v0.6 -- KC1 ruling amendments (R-KC1-7/8/9 + charter sec 11.3).

Commission: elrond amendment pass, fired non-gating from charter sec 12.2 item (d),
run KC1-2026-07-27. Charter: gandalf/notes/2026-07-27-kit-cal-1-run-charter.md.

Three semantics land, plus the structural machinery each one needs:

  1. R-KC1-9  -- kills_per_engagement is RETIRED as an accountability target.
                 A (kills per kill-event) and B (kill-events per burst) are the
                 successors; C (bursts per engagement) is a DECLARED NON-TARGET.
                 A and B are NOT ingested -- that is banked as a declared gap
                 (C-AB-NOT-INGESTED), not fabricated.
  2. R-KC1-7/8 -- the engagement grain is INSTRUMENT-CANONICAL. A `harness_version`
                 table records what harness-v1 MEANS and its declared limits;
                 `segmentation_run` gains `harness_version` + `grain_role`, so
                 future sim-adapter and Godot-OCR ledgers join like-for-like.
                 C-SEG-GRAIN-UNRULED is discharged for accountability quantities
                 with its original hazard text preserved.
  3. sec 11.3  -- the R2/R3 boundary is DERIVED-NONIDENTIFYING (no combat between
                 play_time 5808 and 6475; every candidate boundary in that
                 667 s interval partitions the engagements identically).

Nothing is destructively rewritten. Every amended text field is APPENDED to with a
marked block; superseded rows are marked `superseded` and linked, never deleted.

Idempotent: re-running is a no-op (each step is state-guarded).
"""

import hashlib
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CURATED = os.path.normpath(os.path.join(HERE, "..", "curated"))
DB = os.path.join(CURATED, "fixtures.db")

MARK = "[M9/KC1 2026-07-28]"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
SCHEMA_VERSION = "fixtures-v0.6"

CHARTER = "gandalf/notes/2026-07-27-kit-cal-1-run-charter.md"

SESSION = "GP-gd-2026-07-26-s1"
SEG_ENC = f"{SESSION}/S1-gap5s-v1"
SEG_BURST = f"{SESSION}/S1-burst1.5s-v1"
R3 = f"{SESSION}/R3"
R2 = f"{SESSION}/R2"
FIX = "GD-R2-werewolf"

G2B = "galadriel/captures/2026-07-28-gd-playtest-v1-g2b"


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def table_sql(cx, name):
    row = cx.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row[0] if row else None


def has_column(cx, table, col):
    return any(r[1] == col for r in cx.execute(f"PRAGMA table_info({table})"))


def append_text(cx, table, where, params, col, block):
    """Append a marked block to a text column, once. Original text is preserved.

    `where` is a full predicate so composite-key tables (fixture_target) are
    scoped correctly -- target_key alone is NOT unique across fixtures.
    """
    rows = cx.execute(
        f"SELECT rowid, {col} FROM {table} WHERE {where}", params
    ).fetchall()
    if not rows:
        print(f"  ! {table} WHERE {where} {params} not found; skipping {col}")
        return
    for rowid, existing in rows:
        existing = existing or ""
        if MARK in existing:
            continue
        cx.execute(
            f"UPDATE {table} SET {col}=? WHERE rowid=?",
            ((existing + ("\n\n" if existing else "") + block).strip(), rowid),
        )


def rebuild(cx, name, new_ddl, extra_sql=()):
    """SQLite 12-step table rebuild, used only to WIDEN a CHECK vocabulary.

    Column list is unchanged, so the copy is `SELECT <cols> FROM old`.
    """
    cols = [r[1] for r in cx.execute(f"PRAGMA table_info({name})")]
    collist = ", ".join(f'"{c}"' for c in cols)
    tmp = f"{name}__m9_new"
    cx.execute(f"DROP TABLE IF EXISTS {tmp}")
    cx.execute(new_ddl.replace(f"CREATE TABLE {name}", f"CREATE TABLE {tmp}", 1))
    n_before = cx.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    cx.execute(f"INSERT INTO {tmp} ({collist}) SELECT {collist} FROM {name}")
    cx.execute(f"DROP TABLE {name}")
    cx.execute(f"ALTER TABLE {tmp} RENAME TO {name}")
    for s in extra_sql:
        cx.execute(s)
    n_after = cx.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    assert n_before == n_after, f"{name}: {n_before} -> {n_after} rows lost in rebuild"
    print(f"  rebuilt {name} ({n_after} rows preserved)")


# ----------------------------------------------------------------------------
# DDL for the three widened tables (column lists IDENTICAL to v0.5; only the
# CHECK vocabularies grow) + the one new table.
# ----------------------------------------------------------------------------

DDL_SESSION_REGIME = """
CREATE TABLE session_regime (
  regime_id        TEXT PRIMARY KEY,
  session_id       TEXT NOT NULL REFERENCES fixture_session(session_id),
  regime_key       TEXT NOT NULL,
  regime_ordinal   INTEGER NOT NULL,
  play_time_s_lo   INTEGER NOT NULL,
  play_time_s_hi   INTEGER NOT NULL,
  build_label      TEXT NOT NULL,
  build_break_evidence TEXT,
  -- M9: DERIVED-NONIDENTIFYING added. It is STRONGER than DERIVED, not weaker:
  -- the placement is uncertain within a bracket AND provably immaterial, because
  -- every candidate boundary in the bracket partitions the data identically.
  boundary_grade   TEXT NOT NULL CHECK (boundary_grade IN
                     ('MEASURED','DERIVED','DERIVED-NONIDENTIFYING',
                      'INFERRED','ATTESTED','UNVERIFIED')),
  kills            INTEGER,
  engagements      INTEGER,
  char_level_lo    INTEGER,
  char_level_hi    INTEGER,
  distribution_role TEXT NOT NULL CHECK (distribution_role IN
                     ('fixture','secondary','report-only')),
  distribution_role_rationale TEXT,
  source_ref       TEXT,
  notes            TEXT,
  UNIQUE (session_id, regime_key)
)
"""

DDL_EVIDENCE_CLAIM = """
CREATE TABLE evidence_claim (
  claim_id        TEXT PRIMARY KEY,
  session_id      TEXT REFERENCES fixture_session(session_id),
  subject_kind    TEXT NOT NULL CHECK (subject_kind IN
                    ('control','series','build-identity','measurement','boundary',
                     'anomaly','fixture','instrument')),
  subject_ref     TEXT NOT NULL,
  claim_text      TEXT NOT NULL,
  grade           TEXT NOT NULL CHECK (grade IN
                    ('MEASURED','DERIVED','DERIVED-NONIDENTIFYING','INFERRED',
                     'ATTESTED','UNVERIFIED','REFUTED')),
  method          TEXT,
  source          TEXT NOT NULL,
  source_date     TEXT NOT NULL,
  upgrade_criterion TEXT,
  upgrade_gate_ref TEXT,
  upgraded_from   TEXT,
  supersedes      TEXT REFERENCES evidence_claim(claim_id),
  status          TEXT NOT NULL DEFAULT 'current'
                    CHECK (status IN ('current','superseded','withdrawn'))
)
"""

DDL_FIXTURE_TARGET = """
CREATE TABLE fixture_target (
  fixture_id      TEXT NOT NULL REFERENCES measured_fixture(fixture_id),
  target_key      TEXT NOT NULL,
  -- M9 / R-KC1-9. The tier ladder is now four standings, not three:
  --   'structural-primary'     the PRIMARY claim: a signature the sim must express
  --                            at all (graded PRESENT-CALIBRATABLE / PRESENT-
  --                            MISCALIBRATED / ABSENT per R-KC1-12) BEFORE any
  --                            number is compared.
  --   'secondary-corroboration' numeric bands, wide and honest, that corroborate
  --                            a structural signature but do not carry the claim.
  --   'report-only'            reported, never banded.
  --   'non-target'             DECLARED not the sim's to reproduce (player/level
  --                            routing). Recorded so the omission is deliberate.
  --   'retired'                was a target, is no longer one, superseded by named
  --                            successors. Kept so the lineage is queryable.
  --   'primary' / 'provisional' retained for rows banked before R-KC1-9.
  tier            TEXT NOT NULL CHECK (tier IN
                    ('structural-primary','primary','secondary-corroboration',
                     'provisional','report-only','non-target','retired')),
  measure_key     TEXT REFERENCES measure_dict(measure_key),
  stat_family     TEXT,
  rationale       TEXT,
  gate_ref        TEXT,
  ruling_ref      TEXT,
  band_status     TEXT NOT NULL DEFAULT 'unratified'
                    CHECK (band_status IN ('unratified','ratified','waived')),
  band_lo         REAL, band_hi REAL, band_ref TEXT,
  PRIMARY KEY (fixture_id, target_key)
)
"""

DDL_FIXTURE_CONDITION = """
CREATE TABLE fixture_condition (
  condition_id    TEXT PRIMARY KEY,
  scope_kind      TEXT NOT NULL CHECK (scope_kind IN
                    ('session','regime','engagement','measure','fixture')),
  scope_ref       TEXT NOT NULL,
  -- M9: 'data-gap' added -- a quantity the store is ACCOUNTABLE to but does not
  -- hold. Distinct from 'coverage-hole', which is footage the instrument missed.
  condition_kind  TEXT NOT NULL CHECK (condition_kind IN
                    ('coverage-hole','confound','anomaly','control-violation',
                     'resolution-limit','instrument-dead','normalisation-caveat',
                     'sample-size','provisional-ruling','data-gap')),
  severity        TEXT NOT NULL CHECK (severity IN ('blocking','high','moderate','low','note')),
  headline        TEXT NOT NULL,
  detail          TEXT,
  affects_measure_keys TEXT,
  affected_engagement_ids TEXT,
  affected_kills  INTEGER,
  cause           TEXT,
  cause_grade     TEXT CHECK (cause_grade IN
                    ('MEASURED','DERIVED','DERIVED-NONIDENTIFYING','INFERRED',
                     'ATTESTED','UNVERIFIED')),
  recoverable_from_this_footage INTEGER NOT NULL DEFAULT 0,
  remedy          TEXT,
  evidence_ref    TEXT,
  status          TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','resolved','superseded','accepted')),
  raised_by       TEXT, raised_date TEXT
)
"""

DDL_HARNESS_VERSION = """
CREATE TABLE harness_version (
  -- R-KC1-8: the engagement grain is INSTRUMENT-CANONICAL. It is neither a fact
  -- about this fixture nor an RDR design ontology -- it is a versioned property of
  -- the shared measurement harness, applied identically to every ledger (GD-OCR,
  -- sim-adapter, Godot-OCR). Comparisons join on `harness_version`: structural
  -- like-for-like. Two ledgers on different harness versions do not compare, and
  -- this table is what makes that checkable rather than remembered.
  harness_version TEXT PRIMARY KEY,               -- 'harness-v1'
  status          TEXT NOT NULL CHECK (status IN ('current','superseded','draft')),
  ruling_ref      TEXT NOT NULL,
  encounter_rule  TEXT NOT NULL,                  -- the REPORTING / TTK / intake unit
  burst_rule      TEXT NOT NULL,                  -- the PACK-PROXY unit (carries A and B)
  params_json     TEXT NOT NULL,
  -- 0 while the rules still live in a fixture-specific script. R-KC1-8 routes a
  -- source-agnostic refactor to galadriel; this flag is the acceptance test for it.
  source_agnostic INTEGER NOT NULL DEFAULT 0,
  versioned_in    TEXT,                           -- where the code of record lives
  applies_to_ledgers TEXT,
  -- Stated limits are part of the version's identity, not a footnote to it.
  declared_limits TEXT NOT NULL,
  accountability_note TEXT,
  authored_by     TEXT NOT NULL,
  authored_date   TEXT NOT NULL,
  superseded_by   TEXT REFERENCES harness_version(harness_version),
  notes           TEXT
)
"""


# ----------------------------------------------------------------------------

def main():
    if not os.path.exists(DB):
        sys.exit(f"missing {DB}")

    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys=OFF")
    cx.execute("PRAGMA legacy_alter_table=ON")

    already = cx.execute(
        "SELECT COUNT(*) FROM schema_meta WHERE version=?", (SCHEMA_VERSION,)
    ).fetchone()[0]

    needs_rebuild = "DERIVED-NONIDENTIFYING" not in (table_sql(cx, "session_regime") or "")
    if already and not needs_rebuild:
        print(f"{SCHEMA_VERSION} already applied; re-running idempotent row writes only.")
    else:
        bak = os.path.join(CURATED, f"fixtures.db.pre-v0.6-{STAMP}-backup")
        print(f"backup -> {os.path.basename(bak)}")
        shutil.copy2(DB, bak)
        with open(bak + ".md5.txt", "w") as fh:
            h = hashlib.md5()
            with open(bak, "rb") as src:
                for chunk in iter(lambda: src.read(1 << 20), b""):
                    h.update(chunk)
            fh.write(f"{h.hexdigest()}  {os.path.basename(bak)}\n")

    cx.execute("BEGIN")

    # ---- STEP 1: widen the CHECK vocabularies ------------------------------
    print("\n[1] vocabulary widening (table rebuilds; column lists unchanged)")
    if "DERIVED-NONIDENTIFYING" not in (table_sql(cx, "session_regime") or ""):
        rebuild(cx, "session_regime", DDL_SESSION_REGIME)
    else:
        print("  session_regime already widened")

    if "DERIVED-NONIDENTIFYING" not in (table_sql(cx, "evidence_claim") or ""):
        rebuild(cx, "evidence_claim", DDL_EVIDENCE_CLAIM)
    else:
        print("  evidence_claim already widened")

    if "structural-primary" not in (table_sql(cx, "fixture_target") or ""):
        rebuild(cx, "fixture_target", DDL_FIXTURE_TARGET)
    else:
        print("  fixture_target already widened")

    if "data-gap" not in (table_sql(cx, "fixture_condition") or ""):
        rebuild(cx, "fixture_condition", DDL_FIXTURE_CONDITION,
                extra_sql=("CREATE INDEX IF NOT EXISTS ix_condition_scope "
                           "ON fixture_condition (scope_kind, scope_ref)",))
    else:
        print("  fixture_condition already widened")

    # ---- STEP 2: the harness layer (R-KC1-7 / R-KC1-8) ---------------------
    print("\n[2] harness layer")
    if table_sql(cx, "harness_version") is None:
        cx.execute(DDL_HARNESS_VERSION)
        print("  created harness_version")

    cx.execute("""
      INSERT INTO harness_version (harness_version, status, ruling_ref,
        encounter_rule, burst_rule, params_json, source_agnostic, versioned_in,
        applies_to_ledgers, declared_limits, accountability_note,
        authored_by, authored_date, notes)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(harness_version) DO UPDATE SET
        ruling_ref=excluded.ruling_ref, encounter_rule=excluded.encounter_rule,
        burst_rule=excluded.burst_rule, params_json=excluded.params_json,
        versioned_in=excluded.versioned_in,
        applies_to_ledgers=excluded.applies_to_ledgers,
        declared_limits=excluded.declared_limits,
        accountability_note=excluded.accountability_note, notes=excluded.notes
    """, (
        "harness-v1", "current",
        f"R-KC1-8 (charter {CHARTER} sec 12.1), Matt-ratified 2026-07-28",
        "ENCOUNTER = the reporting / TTK / damage-intake unit. A boundary falls "
        "wherever the inter-KILL-EVENT gap on the gated monotonic kills series "
        "exceeds 5.0 s. Capture windows pad 3.0 s each side. Duration is measured "
        "first-kill-event to last-kill-event, not approach to death.",
        "BURST = the pack-proxy unit, and the unit the accountability quantities "
        "live on. A burst is a maximal run of kill-events whose internal gaps are "
        "<= 1.5 s. B (kill-events per burst) is defined ON the burst; A (kills per "
        "kill-event) is grain-invariant by construction. Only C (bursts per "
        "encounter) depends on the encounter boundary -- and C is a declared "
        "non-target.",
        '{"encounter_gap_threshold_s": 5.0, "encounter_pad_s": 3.0, '
        '"burst_gap_threshold_s": 1.5, "series": "kills (gated, monotonic)", '
        '"sampling_s": 0.5}',
        0,
        "galadriel rollup harness (currently "
        "galadriel/pipeline/gd-playtest-v1/tb_rollup.py + g2b_decompose.py; a "
        "source-agnostic versioned refactor is routed separately per charter "
        "sec 12.2 item (a) and is the acceptance test for source_agnostic=1)",
        "GD-OCR (this store) | sim-adapter ledger (star-lord/gamora, spec via G-4 "
        "addendum) | Godot-OCR ledger (drax + galadriel, chartered later)",
        "(i) 19.2% of combat-state time is outside the padded encounter windows: "
        "240 s of the 1,250 s where dps > 0, across 27 stretches. (ii) Death-counter "
        "increments at play_time 2837 fall OUTSIDE both the windows and the dps "
        "spans -- invisible to every instrument on the table; the increment at "
        "play_time 5152 falls inside both. (iii) The dps-span / E family defers to "
        "harness-v2, to be informed empirically by the Godot calibration leg. "
        "(iv) Death attribution closes only at v2 capture (input log / death-moment "
        "capture -- added to the v2 recording requirements).",
        "R-KC1-9's accountability targets are grain-robust under this harness: A is "
        "grain-invariant, B is burst-defined. The encounter threshold carried a "
        "researcher-degrees-of-freedom pressure on THIS fixture (see "
        "C-SEG-GRAIN-UNRULED); that pressure is confined to the reporting unit and "
        "is a documented property of harness-v1, not a live hazard to the targets.",
        "elrond (M9)", "2026-07-28",
        "One row per harness version. A ledger measured under a different version "
        "does not join to this one; that is the point.",
    ))
    print("  harness-v1 banked")

    if not has_column(cx, "segmentation_run", "harness_version"):
        cx.execute("ALTER TABLE segmentation_run ADD COLUMN harness_version TEXT "
                   "REFERENCES harness_version(harness_version)")
        cx.execute("ALTER TABLE segmentation_run ADD COLUMN grain_role TEXT "
                   "CHECK (grain_role IS NULL OR grain_role IN "
                   "('encounter','pack-proxy-burst','other'))")
        print("  segmentation_run += harness_version, grain_role")

    cx.execute("UPDATE segmentation_run SET harness_version='harness-v1', "
               "grain_role='encounter' WHERE segmentation_id=?", (SEG_ENC,))
    append_text(cx, "segmentation_run", "segmentation_id=?", (SEG_ENC,), "ruling_ref",
                f"{MARK} GRAIN RULED. HALT H-1 released via R-KC1-8 (charter sec 12.1-12.2): "
                "the grain is INSTRUMENT-CANONICAL, not fixture-local. This cut is "
                "harness-v1's ENCOUNTER unit. It is no longer 'the cut every figure "
                "happens to sit on' -- it is the named reporting unit of a versioned "
                "instrument, and it stays 'current' unmodified.")

    # The burst unit gets a real, DECLARED-EMPTY partition rather than a sentence.
    cx.execute("""
      INSERT INTO segmentation_run (segmentation_id, session_id, segmentation,
        rule_text, params_json, derived_from, n_engagements, n_kills,
        dur_median_s, dur_mean_s, dur_max_s, authored_by, authored_date,
        ruling_ref, status, superseded_by, reproduction_note, source_ref,
        harness_version, grain_role)
      VALUES (?,?,?,?,?,?,NULL,NULL,NULL,NULL,NULL,?,?,?,?,NULL,?,?,?,?)
      ON CONFLICT(segmentation_id) DO UPDATE SET
        rule_text=excluded.rule_text, params_json=excluded.params_json,
        ruling_ref=excluded.ruling_ref,
        reproduction_note=excluded.reproduction_note,
        harness_version=excluded.harness_version, grain_role=excluded.grain_role
    """, (
        SEG_BURST, SESSION, "S1-kill-to-kill",
        "harness-v1 PACK-PROXY unit. A burst is a maximal run of kill-events whose "
        "internal gaps are <= 1.5 s, on the gated monotonic kills series. This is "
        "the unit the R-KC1-9 accountability quantities live on: B = kill-events "
        "per burst. It is NOT a replacement for the encounter cut -- two names, two "
        "jobs (charter sec 10.3 Option C).",
        '{"gap_threshold_s": 1.5, "series": "kills (gated, monotonic)", '
        '"sampling_s": 0.5, "unit": "burst"}',
        "panel kills series (gated, monotonic), 0.5 s sampling",
        "elrond (M9)", "2026-07-28",
        "R-KC1-8 (charter sec 12.1); identity kills/encounter = A x B x C, charter sec 10.3",
        "candidate",
        "DECLARED EMPTY, DELIBERATELY. No fixture_trial or regime_stat rows exist on "
        "this segmentation. The quantities that belong here were computed by G-2b and "
        "live OUTSIDE this store: "
        f"{G2B}/g2b-abc-factors.csv (A / B / C with CIs, at b in "
        "{1.0, 1.5, 2.0} x 3 regimes) and "
        f"{G2B}/g2b-per-engagement.csv (n_bursts_b1.5, active_s_b1.5, travel_s_b1.5 "
        "per engagement). Ingesting them is M10 -- a separate, named pass. The row "
        "exists now so the gap has a shape and an address instead of being a "
        "sentence in a document. See condition C-AB-NOT-INGESTED.",
        f"charter {CHARTER} sec 10.3, sec 12.1",
        "harness-v1", "pack-proxy-burst",
    ))
    print("  burst segmentation banked (declared empty)")

    # ---- STEP 3: measure_dict -- target standing + the A/B/C vocabulary ----
    print("\n[3] measure_dict")
    if not has_column(cx, "measure_dict", "target_standing"):
        # Accountability standing is a DIFFERENT axis from measurement semantics.
        # kills_per_engagement's semantics remain contested (it is a composite of
        # three quantities); its TARGET standing is now retired. Conflating the two
        # into semantics_status would hide one behind the other.
        cx.execute("ALTER TABLE measure_dict ADD COLUMN target_standing TEXT "
                   "CHECK (target_standing IS NULL OR target_standing IN "
                   "('structural-accountability-target','secondary-corroboration',"
                   "'retired-as-target','declared-non-target','not-a-target'))")
        cx.execute("ALTER TABLE measure_dict ADD COLUMN target_standing_ref TEXT")
        print("  measure_dict += target_standing, target_standing_ref")

    MD_COLS = ("measure_key,label,unit,value_kind,panel_field,lane_availability,"
               "ladder_rung_introduced,definition,confounds,off_trial_semantics,"
               "layer,derivation,depends_on,ingest_block,block_ref,semantics_status,"
               "semantics_note,requires_coverage,target_standing,target_standing_ref")
    md_rows = [
        (
            "kills_per_kill_event",
            "A -- kills per kill-event (simultaneity)",
            "kills/event", "gauge", None, "both", None,
            "How many kills land in the same instrument sample. Measures AoE breadth "
            "/ simultaneity -- the KIT's behaviour, which the sim must reproduce. "
            "GRAIN-INVARIANT BY CONSTRUCTION (charter sec 10.3): it depends on no "
            "encounter and no burst boundary, which is why R-KC1-8 leaves it "
            "untouched. The A-STEP -- multi-kill emerging at the build swap (R1: 43 "
            "kills in 43 separate half-seconds, P(0 of 43 | R2 rate) = 7.0e-11; R2/R3 "
            "multi-kill routinely) -- is the primary structural signature per R-KC1-9.",
            "The split INSIDE A -- 'the player centred an AoE on a pair' vs 'a pair "
            "happened to be standing there' -- is not measurable from counters. "
            "R-KC1-10 cancelled the T-C enemy census and routes this to a G-5 density "
            "sweep at .arz-plausible densities instead.",
            None, "derived",
            "kills / kill_events, on the gated monotonic kills series",
            "kills", None, None, "settled",
            "Registered by M9. NOT YET INGESTED at regime grain -- see C-AB-NOT-INGESTED.",
            0, "structural-accountability-target",
            f"R-KC1-9 (charter {CHARTER} sec 12.1); identity kills/encounter = A x B x C (sec 10.3)",
        ),
        (
            "kill_events_per_burst",
            "B -- kill-events per burst (sustained pressure)",
            "events/burst", "gauge", None, "both", None,
            "Sustained pressure within a pack: how many kill-events a single burst "
            "carries. The KIT's behaviour, which the sim must reproduce. Defined ON "
            "the burst (harness-v1: internal gaps <= 1.5 s), so it depends on the "
            "burst parameter and NOT on the encounter boundary. The B DoT-TAIL -- "
            "R3's entire lift confined to B (2.27 -> 2.94) with A and C unchanged, "
            "the mechanical signature of a damage-over-time tail -- is a primary "
            "structural signature per R-KC1-9.",
            "R3's lift is NOT statistically established (R2->R3 permutation p = 0.129) "
            "and R3 is post-gear-step on both sides of the ledger (F-KC1-1). B's R3 "
            "value must travel with both conditions.",
            None, "derived",
            "kill_events / bursts, burst = maximal run with internal gaps <= b "
            "(harness-v1: b = 1.5 s)",
            "kills", None, None, "settled",
            "Registered by M9. NOT YET INGESTED at regime grain -- see C-AB-NOT-INGESTED.",
            0, "structural-accountability-target",
            f"R-KC1-9 (charter {CHARTER} sec 12.1); identity kills/encounter = A x B x C (sec 10.3)",
        ),
        (
            "bursts_per_engagement",
            "C -- bursts per encounter (routing)",
            "bursts/encounter", "gauge", None, "both", None,
            "Dash-chaining, routing and travel between packs within one encounter. "
            "This is the PLAYER's and the LEVEL's behaviour, not the kit's.",
            "The only one of the three A x B x C factors that depends on the encounter "
            "boundary. Measured: charge predicts burst count at rho = 0.665 (R2, "
            "p = 7.5e-11) and rho = 0.772 (R3); R3's long encounters carry 31.6% "
            "travel-band gaps vs 4.3% in its short ones. The mechanism is real; its "
            "causal role in the kills/encounter climb is not (merge share is flat-to-"
            "falling across regimes, 2.46 -> 2.20 -> 2.13).",
            None, "derived", "bursts / encounter", "kills", None, None, "settled",
            "DECLARED NON-TARGET per R-KC1-9: the sim is not asked to reproduce it, "
            "and a G-5 miss on C is not a defect. Recorded as a target row with "
            "tier='non-target' so the omission is deliberate and queryable rather "
            "than an absence someone later reads as an oversight.",
            0, "declared-non-target",
            f"R-KC1-9 (charter {CHARTER} sec 12.1)",
        ),
    ]
    ph = ",".join("?" * 20)
    upd = ",".join(f"{c}=excluded.{c}" for c in MD_COLS.split(",")[1:])
    for r in md_rows:
        cx.execute(f"INSERT INTO measure_dict ({MD_COLS}) VALUES ({ph}) "
                   f"ON CONFLICT(measure_key) DO UPDATE SET {upd}", r)
    print(f"  {len(md_rows)} A/B/C measure keys banked")

    # kills_per_engagement: RETIRED as a target. Semantics stay contested --
    # a different axis, deliberately not overwritten.
    cx.execute(
        "UPDATE measure_dict SET target_standing='retired-as-target', "
        "target_standing_ref=? WHERE measure_key='kills_per_engagement'",
        (f"R-KC1-9 (charter {CHARTER} sec 12.1), Matt-ratified 2026-07-28",))
    append_text(cx, "measure_dict", "measure_key=?", ("kills_per_engagement",),
                "semantics_note",
                f"{MARK} RETIRED AS AN ACCOUNTABILITY TARGET (R-KC1-9, charter sec 12.1). "
                "Not de-provisionalised -- retired. G-2b showed it is a composite of two "
                "KIT quantities and one PLAYER quantity (kills/encounter = A x B x C, "
                "exact by construction), and that it behaves as a STEP FUNCTION of build "
                "identity rather than a continuous measurable: within R2, build held "
                "constant over 4,338 game-seconds and levels 3 -> 11, Spearman rho = 0.075 "
                "(p = 0.52). The whole established climb is the 2.54x jump across the "
                "335 s build-swap intermission. SUCCESSORS: kills_per_kill_event (A) and "
                "kill_events_per_burst (B) as targets; bursts_per_engagement (C) as a "
                "declared non-target. The rows already banked on this key remain valid "
                "DESCRIPTIVE statistics of the fixture -- they are simply no longer "
                "something the sim is held to. Do not band. Do not headline.")

    # hp_max_observed carries structural signature (iii), the gear-step regime change.
    cx.execute(
        "UPDATE measure_dict SET target_standing='structural-accountability-target', "
        "target_standing_ref=? WHERE measure_key='hp_max_observed'",
        (f"R-KC1-9 (charter {CHARTER} sec 12.1) signature (iii); F-KC1-1 (sec 9) as "
         "corrected by sec 11.2 -- the 2.11x pool step stands, block is falsified.",))

    for k in ("engagement_seconds", "intake_hp", "intake_hp_per_s",
              "hp_drop_count_ge_10pc_ehp"):
        cx.execute("UPDATE measure_dict SET target_standing='secondary-corroboration', "
                   "target_standing_ref=? WHERE measure_key=? AND target_standing IS NULL",
                   (f"R-KC1-9 (charter {CHARTER} sec 12.1): numeric bands are secondary "
                    "corroboration; the primary claim is structural fidelity.", k))
    print("  kills_per_engagement retired; band-bearing measures marked secondary")

    # ---- STEP 4: fixture_target re-tiering + successors --------------------
    print("\n[4] fixture_target")
    cx.execute(
        "UPDATE fixture_target SET tier='retired', band_status='waived', "
        "gate_ref='', ruling_ref=? "
        "WHERE fixture_id=? AND target_key='kills_per_engagement'",
        ("R-KC1-2, RETIRED by R-KC1-9 (charter sec 12.1). Successors: targets "
         "a_step_multikill_emergence (A) and b_dot_tail (B); c_bursts_per_encounter "
         "declared non-target.", FIX))
    append_text(cx, "fixture_target", "fixture_id=? AND target_key=?",
                (FIX, "kills_per_engagement"), "rationale",
                f"{MARK} The G-2b gate cleared and the answer was RETIREMENT, not "
                "promotion. A x B x C decomposes the 3.590 R3/R1 ratio into "
                "A x1.900 . B x2.188 . C x0.863 -- two kit factors and one player "
                "factor pulling in different directions inside one number. gandalf's "
                "'R3 packs ~3.6x R1' pack-size claim was struck in the same pass "
                "(no instrument in the artifact measures pack size at all, and R1 is "
                "the wrong denominator: different build, skills, level, zone, gear).")

    GATE_SECONDARY = ("R-KC1-12 signature grading (PRESENT-CALIBRATABLE / "
                      "PRESENT-MISCALIBRATED / ABSENT) precedes any numeric "
                      "comparison; bands then ratified at HALT H-2 before G-5 runs.")
    for tk in ("ttk_shape", "damage_intake_total", "damage_intake_rate", "hazard_tail"):
        cx.execute(
            "UPDATE fixture_target SET tier='secondary-corroboration', "
            "ruling_ref='R-KC1-2, amended by R-KC1-9 (charter sec 12.1)', gate_ref=? "
            "WHERE fixture_id=? AND target_key=? AND tier='primary'",
            (GATE_SECONDARY, FIX, tk))
        append_text(cx, "fixture_target", "fixture_id=? AND target_key=?", (FIX, tk),
                    "rationale",
                    f"{MARK} Demoted primary -> secondary-corroboration by R-KC1-9. Not a "
                    "downgrade in importance: STRUCTURAL fidelity is now the primary "
                    "claim, and these numeric bands corroborate it with wide honest "
                    "bands rather than carrying it. Rationale, triple-reinforced: "
                    "structure is what identity-bears about a build; structural "
                    "quantities are grain-robust; structure cannot be faked without "
                    "the producing mechanism class.")

    FT_COLS = ("fixture_id,target_key,tier,measure_key,stat_family,rationale,"
               "gate_ref,ruling_ref,band_status")
    GATE12 = ("R-KC1-12: G-5 grades this signature PRESENT-CALIBRATABLE / "
              "PRESENT-MISCALIBRATED / ABSENT BEFORE any numeric comparison. ABSENT "
              "routes to the build queue as a design finding (mechanism-class "
              "absence -- charter sec 7's fourth miss category), not a tuning target.")
    ft_rows = [
        (FIX, "a_step_multikill_emergence", "structural-primary",
         "kills_per_kill_event", "rates",
         "PRIMARY STRUCTURAL SIGNATURE (i) of R-KC1-9. The four-skill build never once "
         "killed two things in the same half-second across 43 kills; the werewolf did "
         "so immediately (R2's first four encounters read 1.33 / 1.80 / 1.00 / 1.40). "
         "The sim must express that step. CROSS-REGIME by nature: the signature is the "
         "R1 -> R2 discontinuity, evaluated against the session; the contract is held "
         "by the primary fixture row. Melee geometry is a live risk to expressibility "
         "(2026-05-08 engine finding: none exists) -- exactly the kind of gap "
         "R-KC1-12's mechanism-requirements manifest is meant to surface.",
         GATE12, f"R-KC1-9 (charter {CHARTER} sec 12.1)", "unratified"),
        (FIX, "b_dot_tail", "structural-primary",
         "kill_events_per_burst", "rates",
         "PRIMARY STRUCTURAL SIGNATURE (ii) of R-KC1-9: R3's lift confined to B "
         "(2.27 -> 2.94) with A and C unchanged -- the mechanical signature of a "
         "damage-over-time tail, exactly as the gear event predicts. CROSS-REGIME "
         "(R2 -> R3). Travels with two conditions: the R2->R3 difference is NOT "
         "statistically established (permutation p = 0.129), and R3 is post-gear-step.",
         GATE12, f"R-KC1-9 (charter {CHARTER} sec 12.1)", "unratified"),
        (FIX, "gear_step_survivability", "structural-primary",
         "hp_max_observed", "drops",
         "PRIMARY STRUCTURAL SIGNATURE (iii) of R-KC1-9: the gear-step survivability "
         "regime change -- max HP 759 -> 1600 (2.11x) at the R2/R3 boundary, then FLAT "
         "for all of R3, flipping the hazard shape (largest single-frame drop 541 -> "
         "136 raw HP; 27 drops >= 10% EHP in R2, zero in R3). The sim must express a "
         "gear step that changes the hazard REGIME, not merely the numbers. Note the "
         "mechanism narrowed: block is FALSIFIED as the cause (shield_block_chance "
         "moves once, 15.0 -> 18.0 at play_time 3256, mid-R2); the POOL step is "
         "measured and armour remains uninstrumented. STORE NOTE: hp_max_observed is "
         "banked at TRIAL grain (101 rows), not regime grain.",
         GATE12, f"R-KC1-9 (charter {CHARTER} sec 12.1); F-KC1-1 (sec 9) as corrected by sec 11.2",
         "unratified"),
        (FIX, "c_bursts_per_encounter", "non-target",
         "bursts_per_engagement", "rates",
         "DECLARED NON-TARGET per R-KC1-9. C is routing: the player's and the level's "
         "behaviour, not the kit's. A G-5 divergence on C is not a defect and must not "
         "be tuned toward. Banked as a row rather than left absent so the exclusion is "
         "a decision on the record, not a gap someone later fills by accident. This is "
         "also what makes the grain question nearly moot for accountability: C is the "
         "only factor the encounter boundary touches.",
         "", f"R-KC1-9 (charter {CHARTER} sec 12.1)", "waived"),
    ]
    ph = ",".join("?" * 9)
    upd = ",".join(f"{c}=excluded.{c}" for c in FT_COLS.split(",")[2:])
    for r in ft_rows:
        cx.execute(f"INSERT INTO fixture_target ({FT_COLS}) VALUES ({ph}) "
                   f"ON CONFLICT(fixture_id,target_key) DO UPDATE SET {upd}", r)
    print(f"  4 primary rows re-tiered, 1 retired, {len(ft_rows)} successor rows banked")

    # ---- STEP 5: the R2/R3 boundary (charter sec 11.3) ---------------------
    print("\n[5] boundary grade")
    cx.execute("UPDATE session_regime SET boundary_grade='DERIVED-NONIDENTIFYING' "
               "WHERE regime_id=?", (R3,))
    append_text(cx, "session_regime", "regime_id=?", (R3,), "build_break_evidence",
                f"{MARK} UPGRADED DERIVED -> DERIVED-NONIDENTIFYING (charter sec 11.3, "
                "ratified by inclusion in the sec 12 slate). The original DERIVED text "
                "above stands and is why the grade is not MEASURED. What it understates: "
                "the ledger shows NO COMBAT between play_time 5808 and 6475 -- a 667 "
                "game-second gap. Last kill before the boundary: play_time 5808 "
                "(engagement 89, 1 kill, max HP 759). Next kill after: play_time 6475 "
                "(engagement 90). The dps series falls to 0 at 5814 and does not resume "
                "until 6282. EVERY candidate boundary in that interval -- including 6052 "
                "and 6282 -- partitions the engagement data IDENTICALLY. The placement "
                "is therefore non-identifying for every engagement-level quantity, not "
                "merely derived-and-uncertain. 'DERIVED' alone invites a precision worry "
                "that does not exist here. The max-HP step brackets to the same dead "
                "interval (last confirmed 759 at engagement 89; first confirmed 1600 at "
                "engagement 94 -- engagements 90-93 are the zero-coverage hole, so the "
                "globe series cannot narrow it either): consistent, and immaterial for "
                "the same reason.")
    append_text(cx, "session_regime", "regime_id=?", (R2,), "build_break_evidence",
                f"{MARK} R2's UPPER edge is the same boundary, and is likewise "
                "NON-IDENTIFYING (no combat 5808-6475). This row's grade stays MEASURED "
                "because the edge that DETERMINES R2's identity is its lower edge, the "
                "C-2 build break at 1134, which is measured outright.")

    cx.execute("UPDATE evidence_claim SET status='superseded' "
               "WHERE claim_id='EC-DOT-BOUNDARY-6052'")
    cx.execute("UPDATE evidence_claim SET status='superseded' "
               "WHERE claim_id='EC-SEGMENTATION-GRAIN'")

    EC_COLS = ("claim_id,session_id,subject_kind,subject_ref,claim_text,grade,method,"
               "source,source_date,upgrade_criterion,upgrade_gate_ref,upgraded_from,"
               "supersedes,status")
    ec_rows = [
        ("EC-DOT-BOUNDARY-NONIDENTIFYING", SESSION, "boundary", R3,
         "The R2/R3 boundary is banked at play_time 6052, and its exact placement "
         "within the 6052-6282 bracket is NON-IDENTIFYING for every engagement-level "
         "quantity.",
         "DERIVED-NONIDENTIFYING",
         "Direct ledger read: last kill before the boundary at play_time 5808 "
         "(engagement 89); next kill at 6475 (engagement 90); dps falls to 0 at 5814 "
         "and does not resume until 6282. The 667 s interval contains no combat, so "
         "every candidate boundary inside it produces the same partition of "
         "engagements, kills and intake. The bracket remains MEASURED; its collapse to "
         "a point remains a derivation; the derivation is provably immaterial.",
         f"charter {CHARTER} sec 11.3 (elrond ledger read), ratified by inclusion in the sec 12 slate",
         "2026-07-28",
         "Nothing needs to move it for engagement-level use. It would only matter for "
         "a quantity defined on WALLCLOCK or on the dead interval itself (e.g. "
         "out-of-combat regen, time-to-regear). The R-KC1-4 .gdc probe would still "
         "pin the gear event, but the probe found no save on any reachable volume "
         "(T11 parked with Matt).",
         "T11 (canonical/matt_to_do/2026-07-28-gd-gdc-save-copy.md) -- optional, not blocking",
         "EC-DOT-BOUNDARY-6052", "EC-DOT-BOUNDARY-6052", "current"),
        ("EC-HARNESS-V1-GRAIN", SESSION, "instrument", "harness-v1",
         "The engagement grain is a versioned property of the shared MEASUREMENT "
         "HARNESS (harness-v1), not a fact about this fixture and not an RDR design "
         "ontology. Ledgers compare only when they share a harness_version.",
         "ATTESTED",
         "A ruling, not a measurement -- graded ATTESTED on the authority that issued "
         "it. R-KC1-8, Matt-ratified 2026-07-28 ('Ratified on all six rows, cascade'). "
         "This DISSOLVES the superseded claim rather than upgrading it: "
         "EC-SEGMENTATION-GRAIN asked whether gap > 5 s is the CORRECT definition of "
         "an engagement, which R-KC1-8 rules is not a question with a truth value. "
         "harness-v1 = encounter gap > 5 s (reporting / TTK / intake) + burst <= 1.5 s "
         "(pack-proxy, carrying A and B).",
         f"charter {CHARTER} sec 12.1 R-KC1-7 / R-KC1-8", "2026-07-28",
         "harness-v2: the dps-span / E-family segmentation, to be settled EMPIRICALLY "
         "by the Godot calibration leg (OCR against known truth yields the pipeline's "
         "error model). Death attribution closes only at v2 capture -- input log or "
         "death-moment capture, now a v2 recording requirement.",
         "Godot OCR leg (chartered later as its own run) + galadriel source-agnostic "
         "harness refactor (charter sec 12.2 item a)",
         None, "EC-SEGMENTATION-GRAIN", "current"),
    ]
    ph = ",".join("?" * 14)
    upd = ",".join(f"{c}=excluded.{c}" for c in EC_COLS.split(",")[1:])
    for r in ec_rows:
        cx.execute(f"INSERT INTO evidence_claim ({EC_COLS}) VALUES ({ph}) "
                   f"ON CONFLICT(claim_id) DO UPDATE SET {upd}", r)
    print("  boundary upgraded; 2 claims superseded, 2 successors banked")

    # ---- STEP 6: conditions -- discharge, retire, and DECLARE THE GAP ------
    print("\n[6] fixture_condition")
    cx.execute("UPDATE fixture_condition SET status='accepted', remedy=? "
               "WHERE condition_id='C-SEG-GRAIN-UNRULED'",
               ("None required for the accountability targets -- discharged by "
                "R-KC1-8. For the REPORTING unit the pressure is accepted and "
                "documented as a property of harness-v1 (see harness_version). "
                "harness-v2 revisits the segmentation family empirically via the "
                "Godot calibration leg.",))
    append_text(cx, "fixture_condition", "condition_id=?", ("C-SEG-GRAIN-UNRULED",), "detail",
                f"{MARK} DISCHARGED FOR THE ACCOUNTABILITY QUANTITIES by R-KC1-8 "
                "(charter sec 12.1-12.2). The hazard text above is retained verbatim "
                "for lineage -- it was real, it was correctly raised, and it fed the "
                "HALT H-1 package (charter sec 11.1). What discharges it: the "
                "accountability targets no longer depend on the encounter boundary. "
                "A is grain-invariant by construction; B lives on the burst; C -- the "
                "only grain-dependent factor -- is a DECLARED NON-TARGET. The residual "
                "selection pressure applies to the REPORTING unit only, and is now a "
                "documented property of a versioned instrument rather than an unruled "
                "researcher choice: harness-v1, ruled instrument-canonical, applied "
                "identically to GD-OCR, sim-adapter and Godot-OCR ledgers. Status "
                "'accepted', not 'resolved': the affects_measure_keys list above is "
                "still accurate for the reporting-unit figures, and consumers should "
                "keep seeing it ride on those rows.")

    cx.execute("UPDATE fixture_condition SET status='superseded', remedy=? "
               "WHERE condition_id='C-KPE-PROVISIONAL'",
               ("Gate cleared. G-2b filed the decomposition and the tier was re-ruled "
                "to RETIRED, not promoted. Superseded by C-KPE-RETIRED.",))
    append_text(cx, "fixture_condition", "condition_id=?", ("C-KPE-PROVISIONAL",), "detail",
                f"{MARK} SUPERSEDED BY C-KPE-RETIRED. The T-1 gate named in the remedy "
                "cleared: G-2b filed, and the confound this condition described turned "
                "out to be structural rather than removable -- kills/encounter is "
                "A x B x C, two kit factors and one player factor. The caution does "
                "not lapse; it changes character, and rides on C-KPE-RETIRED so it "
                "keeps attaching to the banked rows in v_regime_stat_conditioned.")

    FC_COLS = ("condition_id,scope_kind,scope_ref,condition_kind,severity,headline,"
               "detail,affects_measure_keys,cause,cause_grade,"
               "recoverable_from_this_footage,remedy,evidence_ref,status,"
               "raised_by,raised_date")
    fc_rows = [
        ("C-KPE-RETIRED", "measure", "kills_per_engagement", "provisional-ruling", "high",
         "kills/engagement is RETIRED as an accountability target. The banked rows are "
         "descriptive statistics, not a contract.",
         "R-KC1-9 (charter sec 12.1), Matt-ratified 2026-07-28. It is a composite of "
         "two KIT quantities and one PLAYER quantity -- kills/encounter = A x B x C, "
         "exact by construction -- and G-2b showed it behaves as a STEP FUNCTION of "
         "build identity, not a continuous measurable (within R2, build constant, "
         "4,338 game-seconds, levels 3 -> 11: Spearman rho = 0.075, p = 0.52; the "
         "entire climb is the 2.54x jump across the 335 s build-swap intermission). "
         "Successors: kills_per_kill_event (A) and kill_events_per_burst (B) as "
         "targets, bursts_per_engagement (C) as a declared non-target. The 106 banked "
         "kills_per_engagement rows remain a valid DESCRIPTION of this fixture -- they "
         "are simply no longer something the sim is held to. Do not band; do not "
         "headline; do not tune toward.",
         "kills_per_engagement",
         "Composite of heterogeneous quantities + step-function behaviour, established "
         "by the G-2b A x B x C decomposition.",
         "MEASURED", 1,
         "None -- this is a settled ruling, not an open defect. It closes only if the "
         "target set is re-ruled, which would need a fresh Matt ruling superseding "
         "R-KC1-9.",
         f"charter {CHARTER} sec 10.3, sec 12.1 R-KC1-9; "
         "galadriel/notes/2026-07-28-gd-playtest-v1-g2b-causal-decomposition.md",
         "open", "elrond (M9)", "2026-07-28"),
        ("C-AB-NOT-INGESTED", "fixture", FIX, "data-gap", "high",
         "DECLARED GAP: A and B -- the successor accountability targets -- are NOT "
         "banked in this store at regime grain.",
         "R-KC1-9 makes kills_per_kill_event (A) and kill_events_per_burst (B) the "
         "accountability targets, and fixture_target now carries them. regime_stat "
         "does not. The store holds 21 measure keys at regime grain; A, B and C are "
         "none of them. The quantities EXIST and are computed -- they live outside "
         "this store, in G-2b's committed capture: "
         f"{G2B}/g2b-abc-factors.csv gives A / B / C per regime with confidence "
         "intervals at three burst thresholds (b = 1.0, 1.5, 2.0), and "
         f"{G2B}/g2b-per-engagement.csv gives n_bursts / active_s / travel_s per "
         "engagement at each b. They were NOT copied in by M9, deliberately: M9 is a "
         "semantics amendment, and ingesting a new measurement family is a "
         "measurement pass with its own reproduction gate. The empty partition "
         f"'{SEG_BURST}' (status 'candidate') is their declared address. Until M10 "
         "lands, a consumer reading fixture_target will find the targets named with "
         "no numbers behind them -- which is the honest state, and is why this "
         "condition exists rather than a silently absent row.",
         "kills_per_kill_event,kill_events_per_burst,bursts_per_engagement",
         "Scope boundary: M9 amends semantics; the A/B/C ingest is M10.",
         "MEASURED", 1,
         "M10: ingest g2b-abc-factors.csv onto segmentation "
         f"'{SEG_BURST}' with the same Gate-0 reproduction discipline M8 used "
         "(recompute from g2b-per-engagement.csv, do not trust the rollup), banking "
         "all three burst thresholds so the b-sensitivity is visible rather than "
         "chosen. Blocks nothing today: G-5's first act under R-KC1-12 is a "
         "PRESENT/ABSENT signature grading, not a numeric comparison.",
         f"{G2B}/g2b-abc-factors.csv; {G2B}/g2b-per-engagement.csv; "
         f"{G2B}/g2b-decomposition.json (key 'abc_decomposition')",
         "open", "elrond (M9)", "2026-07-28"),
        ("C-HARNESS-V1-LIMITS", "session", SESSION, "resolution-limit", "moderate",
         "harness-v1's declared instrument limits: 19.2% of combat-state time falls "
         "outside the padded encounter windows, and one death is invisible to every "
         "instrument.",
         "Per R-KC1-8, stated as part of the harness version's identity rather than as "
         "a footnote. (i) 240 s of the 1,250 s where dps > 0 lies outside the padded "
         "windows, across 27 stretches. (ii) The death-counter increment at play_time "
         "2837 falls outside BOTH the windows and the dps spans -- no instrument on "
         "the table can see it; the increment at play_time 5152 falls inside both. "
         "(iii) The dps-span / E family of segmentations defers to harness-v2. Any "
         "figure defined on 'all combat' rather than 'all encounters' is understated "
         "by up to this margin.",
         "", "harness-v1 window construction (gap > 5 s + 3.0 s padding).", "MEASURED", 0,
         "harness-v2, informed empirically by the Godot calibration leg. Death "
         "attribution closes only at v2 capture (input log / death-moment capture).",
         f"charter {CHARTER} sec 12.1 R-KC1-8", "accepted", "elrond (M9)", "2026-07-28"),
    ]
    ph = ",".join("?" * 16)
    upd = ",".join(f"{c}=excluded.{c}" for c in FC_COLS.split(",")[1:])
    for r in fc_rows:
        cx.execute(f"INSERT INTO fixture_condition ({FC_COLS}) VALUES ({ph}) "
                   f"ON CONFLICT(condition_id) DO UPDATE SET {upd}", r)
    print(f"  2 conditions amended, {len(fc_rows)} banked")

    # ---- STEP 7: views -----------------------------------------------------
    print("\n[7] views")
    for v in ("v_fixture_accountability", "v_regime_stat_conditioned",
              "v_measurement_join_key", "v_harness_ledger"):
        cx.execute(f"DROP VIEW IF EXISTS {v}")

    cx.execute("""
      CREATE VIEW v_fixture_accountability AS
      SELECT f.fixture_id, f.fixture_role, f.kit_id, f.calibration_run,
             sr.harness_version, sr.grain_role,
             t.target_key, t.tier, t.measure_key, md.target_standing,
             t.stat_family, t.band_status, t.band_lo, t.band_hi,
             t.gate_ref, t.ruling_ref, t.rationale,
             -- is there anything behind this target in this store?
             (SELECT COUNT(*) FROM regime_stat rs
               WHERE rs.measure_key = t.measure_key
                 AND rs.regime_id = f.regime_id) AS n_regime_rows,
             (SELECT COUNT(*) FROM trial_measurement tm
               WHERE tm.measure_key = t.measure_key) AS n_trial_rows,
             (SELECT GROUP_CONCAT(c.condition_id, ' | ') FROM fixture_condition c
               WHERE c.status IN ('open','accepted')
                 AND ((c.scope_kind='measure' AND c.scope_ref = t.measure_key)
                   OR (c.scope_kind='fixture' AND c.scope_ref = f.fixture_id
                       AND (',' || c.affects_measure_keys || ',')
                             LIKE ('%,' || t.measure_key || ',%')))) AS condition_ids
      FROM measured_fixture f
      JOIN fixture_target t USING (fixture_id)
      LEFT JOIN measure_dict md ON md.measure_key = t.measure_key
      LEFT JOIN segmentation_run sr ON sr.segmentation_id = f.segmentation_id
    """)

    cx.execute("""
      CREATE VIEW v_regime_stat_conditioned AS
      SELECT
        s.*, r.regime_key, r.distribution_role, r.boundary_grade,
        sr.harness_version, sr.grain_role,
        md.target_standing,
        (SELECT COUNT(*) FROM fixture_condition c
          WHERE c.status IN ('open','accepted')
            AND ((c.scope_kind='regime' AND c.scope_ref = s.regime_id
                  AND (c.affects_measure_keys = ''
                       OR (',' || c.affects_measure_keys || ',')
                            LIKE ('%,' || s.measure_key || ',%')))
              OR (c.scope_kind='measure' AND c.scope_ref = s.measure_key))
        ) AS n_conditions,
        (SELECT GROUP_CONCAT(c.condition_id, ' | ') FROM fixture_condition c
          WHERE c.status IN ('open','accepted')
            AND ((c.scope_kind='regime' AND c.scope_ref = s.regime_id
                  AND (c.affects_measure_keys = ''
                       OR (',' || c.affects_measure_keys || ',')
                            LIKE ('%,' || s.measure_key || ',%')))
              OR (c.scope_kind='measure' AND c.scope_ref = s.measure_key))
        ) AS condition_ids,
        (SELECT GROUP_CONCAT(c.headline, ' | ') FROM fixture_condition c
          WHERE c.status IN ('open','accepted')
            AND ((c.scope_kind='regime' AND c.scope_ref = s.regime_id
                  AND (c.affects_measure_keys = ''
                       OR (',' || c.affects_measure_keys || ',')
                            LIKE ('%,' || s.measure_key || ',%')))
              OR (c.scope_kind='measure' AND c.scope_ref = s.measure_key))
        ) AS conditions
      FROM regime_stat s
      JOIN session_regime r ON r.regime_id = s.regime_id
      JOIN segmentation_run sr ON sr.segmentation_id = s.segmentation_id
      LEFT JOIN measure_dict md ON md.measure_key = s.measure_key
    """)

    # The cross-ledger join surface R-KC1-7/8 asks for. A sim-adapter or Godot-OCR
    # ledger banked in this store (or ATTACHed) exposes the same columns, and the
    # comparison is an equi-join on (harness_version, grain_role, measure_key).
    cx.execute("""
      CREATE VIEW v_measurement_join_key AS
      SELECT
        sr.harness_version, sr.grain_role,
        s.session_id AS ledger_id, s.lane AS ledger_lane, s.adapter AS ledger_adapter,
        rg.regime_key, rs.regime_id, rs.segmentation_id,
        rs.measure_key, md.target_standing, md.layer, md.semantics_status,
        rs.stat_family, rs.statistic, rs.value_num, rs.unit,
        rs.n_included, rs.n_total, rs.inclusion_rule, rs.coverage,
        rs.coverage_basis, rs.evidence_grade
      FROM regime_stat rs
      JOIN segmentation_run sr ON sr.segmentation_id = rs.segmentation_id
      JOIN session_regime rg ON rg.regime_id = rs.regime_id
      JOIN fixture_session s ON s.session_id = rg.session_id
      LEFT JOIN measure_dict md ON md.measure_key = rs.measure_key
    """)

    cx.execute("""
      CREATE VIEW v_harness_ledger AS
      SELECT h.harness_version, h.status, h.source_agnostic, h.versioned_in,
             h.ruling_ref, h.encounter_rule, h.burst_rule, h.declared_limits,
             sr.segmentation_id, sr.grain_role, sr.status AS segmentation_status,
             sr.n_engagements, sr.n_kills, sr.session_id
      FROM harness_version h
      LEFT JOIN segmentation_run sr ON sr.harness_version = h.harness_version
    """)
    print("  4 views (2 recreated, 2 new)")

    # ---- STEP 8: schema_meta ----------------------------------------------
    cx.execute("DELETE FROM schema_meta WHERE version=?", (SCHEMA_VERSION,))
    cx.execute(
        "INSERT INTO schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        (SCHEMA_VERSION, NOW,
         "M9 KC1 ruling amendments. R-KC1-9: kills_per_engagement RETIRED as an "
         "accountability target (measure_dict.target_standing added as an axis "
         "distinct from semantics_status); A/B registered as successors, C as a "
         "declared non-target; four numeric targets re-tiered primary -> "
         "secondary-corroboration; three structural-primary targets banked. "
         "R-KC1-7/8: harness_version table + segmentation_run.harness_version / "
         ".grain_role, populated harness-v1; burst segmentation banked DECLARED "
         "EMPTY; C-SEG-GRAIN-UNRULED discharged (status 'accepted', original hazard "
         "text preserved). Charter sec 11.3: boundary_grade vocabulary gains "
         "DERIVED-NONIDENTIFYING, R3 upgraded. New condition kind 'data-gap'; "
         "C-AB-NOT-INGESTED declares A/B absent rather than fabricating them. "
         "Applied by fixtures_m9_kc1_ruling_amendments_2026_07_28.py."))

    # ---- verify ------------------------------------------------------------
    print("\n[verify]")
    fk = cx.execute("PRAGMA foreign_key_check").fetchall()
    print(f"  foreign_key_check: {'CLEAN' if not fk else fk[:5]}")
    assert not fk, "FK violations after rebuild"
    ic = cx.execute("PRAGMA integrity_check").fetchone()[0]
    print(f"  integrity_check: {ic}")
    assert ic == "ok"

    cx.execute("COMMIT")
    cx.execute("PRAGMA foreign_keys=ON")

    print("\n[state]")
    for row in cx.execute(
            "SELECT target_key, tier, measure_key, band_status FROM fixture_target "
            "WHERE fixture_id=? ORDER BY CASE tier WHEN 'structural-primary' THEN 0 "
            "WHEN 'secondary-corroboration' THEN 1 WHEN 'report-only' THEN 2 "
            "WHEN 'non-target' THEN 3 ELSE 4 END, target_key", (FIX,)):
        print("  {:34s} {:24s} {:24s} {}".format(*(x or "" for x in row)))
    for row in cx.execute("SELECT regime_key, boundary_grade FROM session_regime "
                          "ORDER BY regime_ordinal"):
        print(f"  {row[0]}: {row[1]}")
    for row in cx.execute("SELECT segmentation_id, harness_version, grain_role, status, "
                          "n_engagements FROM segmentation_run"):
        print(f"  {row[0]}  {row[1]}/{row[2]}  {row[3]}  n={row[4]}")
    print("  measure_dict target_standing:",
          dict(cx.execute("SELECT target_standing, COUNT(*) FROM measure_dict "
                          "WHERE target_standing IS NOT NULL GROUP BY 1")))
    cx.close()
    print(f"\n{SCHEMA_VERSION} applied.")


if __name__ == "__main__":
    main()
