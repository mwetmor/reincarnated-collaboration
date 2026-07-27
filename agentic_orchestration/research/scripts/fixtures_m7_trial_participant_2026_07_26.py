#!/usr/bin/env python3
"""
fixtures.db - MILESTONE 7: a trial is a MANY-monster event
===========================================================
Agent: elrond (store owner). Run AFTER m5. Idempotent. Additive + one rebuild.

THE DEFECT THIS FIXES
---------------------
v0.1 defines `fixture_set` as "the N-trial group: ONE MONSTER, one rig, one ladder rung",
and `fixture_trial.fixture_set_id` is NOT NULL. So every trial must hang off a
single-monster group. That is exactly right for L0, where Matt spawns one zombie and
kills it three times.

Protocol sec 5.1 carries that hierarchy into the general-play run: `fixture_set`
"partitioned by (epoch, monster_display_name, monster_level, monster_rank, area,
difficulty)", `fixture_trial` "one per engagement". Those two sentences cannot both hold.
sec 5.3 declares `single-monster` VIOLATED "(packs)" in the same document. A pack
engagement has several monsters, of several display names, at several levels, of several
ranks - it belongs to several of those partitions AT ONCE. There are only two ways to
force it into one:

  (a) pick a "representative" monster per engagement    -> a fabricated identity
  (b) duplicate the trial into every set it touches     -> double-counted engagements

Both are worse than the problem. The hierarchy is simply the wrong shape: monster
participation in an engagement is MANY-TO-MANY, and a one-to-many parent cannot carry it.

THE FIX
-------
  * `fixture_trial.fixture_set_id` becomes NULLABLE. A trial can exist as a window over
    the session ledger with no set at all - which is what a pack engagement is.
  * `fixture_trial.session_id` added and NOT NULL. The session is the real parent.
  * NEW `trial_participant`: one row per monster in the engagement, each with its OWN
    identity, level, rank and provenance. `identity_method='unidentified'` is first-class
    - O-8 pushed down from the set to the individual, which is where sec 5.4 says most of
    the failures will land ("camera angle, pack overlap, no hover").
  * `fixture_set` is UNCHANGED and keeps meaning what it meant: a one-monster group.
    L0 still works exactly as before; `v_fixture_bank_certified` still returns 3.

A general-play trial that HAPPENS to have one participant is then recognisable by query
(`v_trial_homogeneous`) rather than by construction - which is the honest direction. You
discover that an engagement was single-monster; you do not assert it in order to store it.
"""

import datetime
import os
import sqlite3
import sys

REPO = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO, "agentic_orchestration/research/curated/fixtures.db")
VERSION = "fixtures-v0.4"

TRIAL_NEW = r"""
CREATE TABLE fixture_trial_new (
  trial_id       TEXT PRIMARY KEY,
  -- v0.4: the SESSION is the real parent of a trial. A set is optional grouping.
  session_id     TEXT NOT NULL REFERENCES fixture_session(session_id),
  -- v0.4: NULLABLE. A pack engagement belongs to no single-monster set.
  fixture_set_id TEXT REFERENCES fixture_set(fixture_set_id),
  trial_ordinal  INTEGER NOT NULL,
  lane           TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  segmentation   TEXT NOT NULL DEFAULT 'S0-explicit'
                   CHECK (segmentation IN ('S0-explicit','S1-kill-to-kill',
                                           'S2-combat-window','S3-per-entity')),
  segmentation_params TEXT,
  outcome        TEXT CHECK (outcome IN
                   ('monster-killed','player-died','monster-fled','aborted','timeout',
                    'no-fight-baseline')),
  t_start_playtime_s INTEGER,
  t_end_playtime_s   INTEGER,
  t_start_playtime_ms INTEGER,
  t_end_playtime_ms   INTEGER,
  t_start_pts_ms INTEGER,
  t_end_pts_ms   INTEGER,
  before_capture_id  TEXT REFERENCES capture(capture_id),
  after_capture_id   TEXT REFERENCES capture(capture_id),
  monster_entity_id  TEXT,           -- retained for the L0 rows; superseded by trial_participant
  contaminated       INTEGER NOT NULL DEFAULT 0,
  contamination_reason TEXT,
  spans_break_id TEXT REFERENCES session_break(break_id),
  derived_from_ledger INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  UNIQUE (fixture_set_id, segmentation, trial_ordinal)
);
"""

PARTICIPANT = r"""
CREATE TABLE IF NOT EXISTS trial_participant (
  trial_id        TEXT NOT NULL REFERENCES fixture_trial(trial_id),
  participant_ordinal INTEGER NOT NULL,
  -- the E5 overlay instance id. F4 proved these distinguish individuals, which makes
  -- this the only channel that can count pack members without identifying them.
  entity_id       TEXT,
  monster_display_name TEXT,
  monster_level   INTEGER,
  monster_level_method TEXT,
  -- OBSERVED rank, nameplate colour (protocol sec 4.3). 'unknown' is first-class and
  -- MUST NOT be silently binned as 'normal' - an unfiltered TTK distribution over mixed
  -- ranks is a mixture of at least three distributions and its variance means nothing.
  monster_rank_observed TEXT CHECK (monster_rank_observed IN
                    ('normal','champion','hero','boss','unknown')),
  monster_record  TEXT,
  monster_bio_record TEXT,
  identity_method TEXT NOT NULL CHECK (identity_method IN
                    ('spawn-command-verbatim','screenshot-nameplate','video-frame-nameplate',
                     'entity-id-only','area-roster-inference','unidentified')),
  identity_evidence TEXT,
  -- what this participant DID. 'present-unresolved' = it was in the fight and we do not
  -- know whether the player killed it, it fled, or it outlived the window.
  role            TEXT NOT NULL DEFAULT 'unknown' CHECK (role IN
                    ('killed','fled','survived','present-unresolved','unknown')),
  first_seen_play_time_ms INTEGER, first_seen_pts_ms INTEGER,
  died_play_time_ms       INTEGER, died_pts_ms       INTEGER,
  kill_attributed_to TEXT CHECK (kill_attributed_to IN
                    ('player','pet','dot','retaliation','environment','unknown')),
  capture_id      TEXT REFERENCES capture(capture_id),
  notes           TEXT,
  PRIMARY KEY (trial_id, participant_ordinal)
);
CREATE INDEX IF NOT EXISTS ix_participant_entity ON trial_participant (entity_id);
CREATE INDEX IF NOT EXISTS ix_participant_name
  ON trial_participant (monster_display_name, monster_level, monster_rank_observed);
"""

VIEWS = r"""
DROP VIEW IF EXISTS v_trial_participants_rollup;
CREATE VIEW v_trial_participants_rollup AS
SELECT
  t.trial_id, t.session_id, t.segmentation, t.fixture_set_id,
  COUNT(p.participant_ordinal) AS n_participants,
  COUNT(DISTINCT p.monster_display_name) AS n_distinct_names,
  COUNT(DISTINCT p.monster_level)        AS n_distinct_levels,
  COUNT(DISTINCT p.monster_rank_observed) AS n_distinct_ranks,
  SUM(CASE WHEN p.identity_method='unidentified' THEN 1 ELSE 0 END) AS n_unidentified,
  SUM(CASE WHEN p.monster_rank_observed='unknown' THEN 1 ELSE 0 END) AS n_rank_unknown,
  SUM(CASE WHEN p.role='killed' THEN 1 ELSE 0 END) AS n_killed,
  -- guard the LEFT JOIN's NULL row: a trial with zero participants must count zero,
  -- not one. (Caught in verification: `p.kill_attributed_to IS NULL` matched the
  -- synthesised NULL row of a participant-less trial.)
  SUM(CASE WHEN p.participant_ordinal IS NOT NULL
            AND COALESCE(p.kill_attributed_to,'unknown') <> 'player'
           THEN 1 ELSE 0 END) AS n_not_player_attributed
FROM fixture_trial t LEFT JOIN trial_participant p USING (trial_id)
GROUP BY t.trial_id;

-- A general-play engagement that turns out to be single-monster, single-level,
-- single-rank and fully identified is structurally an L0 fixture. DISCOVERED by query,
-- not asserted in order to be storable.
DROP VIEW IF EXISTS v_trial_homogeneous;
CREATE VIEW v_trial_homogeneous AS
SELECT r.*, 'single-monster-identified' AS homogeneity
FROM v_trial_participants_rollup r
WHERE r.n_participants = 1 AND r.n_unidentified = 0 AND r.n_rank_unknown = 0
UNION ALL
SELECT r.*, 'uniform-pack' AS homogeneity
FROM v_trial_participants_rollup r
WHERE r.n_participants > 1 AND r.n_distinct_names = 1 AND r.n_distinct_levels = 1
  AND r.n_distinct_ranks = 1 AND r.n_unidentified = 0;
"""


def main():
    if not os.path.exists(DB):
        sys.exit(f"missing {DB}")
    cx = sqlite3.connect(DB)
    cols = {r[1] for r in cx.execute("PRAGMA table_info(fixture_trial)")}
    if "session_id" not in cols:
        cx.execute("PRAGMA foreign_keys=OFF")
        cx.execute("PRAGMA legacy_alter_table=ON")
        for v in ("v_trial_wide", "v_trial_delta", "v_set_spread", "v_ledger_continuity",
                  "v_differential", "v_fixture_bank_certified",
                  "v_fixture_bank_certified_clean"):
            cx.execute(f"DROP VIEW IF EXISTS {v}")
        n0 = cx.execute("SELECT COUNT(*) FROM fixture_trial").fetchone()[0]
        cx.execute("DROP TABLE IF EXISTS fixture_trial_new")
        cx.executescript(TRIAL_NEW)
        keep = [c for c in cols if c != "session_id"]
        cx.execute(f"""INSERT INTO fixture_trial_new (session_id,{','.join(keep)})
            SELECT s.session_id,{','.join('t.'+c for c in keep)}
            FROM fixture_trial t JOIN fixture_set s USING (fixture_set_id)""")
        cx.execute("DROP TABLE fixture_trial")
        cx.execute("ALTER TABLE fixture_trial_new RENAME TO fixture_trial")
        n1 = cx.execute("SELECT COUNT(*) FROM fixture_trial").fetchone()[0]
        assert n0 == n1, f"fixture_trial {n0} -> {n1}"
        # ledger-derived trials carry no set, so the set-scoped UNIQUE cannot constrain
        # them. A partial index keys them on the session instead.
        cx.execute("""CREATE UNIQUE INDEX IF NOT EXISTS ux_trial_ledger_scoped
                      ON fixture_trial (session_id, segmentation, trial_ordinal)
                      WHERE fixture_set_id IS NULL""")
        print(f"  rebuilt fixture_trial: {n1} rows preserved, fixture_set_id now NULLABLE")
        # views were dropped; re-apply M5's definitions
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "m5", os.path.join(REPO, "agentic_orchestration/research/scripts/"
                                     "fixtures_m5_v0_3_schema_2026_07_26.py"))
        m5 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m5)
        cx.executescript(m5.VIEWS)
        cx.execute("PRAGMA foreign_keys=ON")

    cx.executescript(PARTICIPANT)
    cx.executescript(VIEWS)
    cx.execute("INSERT INTO schema_meta (version,applied_utc,note) VALUES (?,?,?)", (
        VERSION,
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "M7. A trial is a MANY-monster event: trial_participant added; "
        "fixture_trial.fixture_set_id NULLABLE; fixture_trial.session_id NOT NULL. "
        "fixture_set unchanged and still one-monster. Applied by "
        "fixtures_m7_trial_participant_2026_07_26.py."))
    cx.commit()
    print("foreign_key_check:", cx.execute("PRAGMA foreign_key_check").fetchall() or "CLEAN")
    print("integrity_check:", cx.execute("PRAGMA integrity_check").fetchone()[0])
    print("v_fixture_bank_certified:",
          cx.execute("SELECT COUNT(*) FROM v_fixture_bank_certified").fetchone()[0], "(expect 3)")
    print("v_trial_participants_rollup:",
          cx.execute("SELECT COUNT(*) FROM v_trial_participants_rollup").fetchone()[0])
    cx.close()


if __name__ == "__main__":
    main()
