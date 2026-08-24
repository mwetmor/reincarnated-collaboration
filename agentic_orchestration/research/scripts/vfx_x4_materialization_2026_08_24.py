#!/usr/bin/env python3
"""
X-4 — VFX archetype-binding materialization (elrond, catalogue seam).

Commissioned at charter L-35 (conductor ruling 1), EXPANDED at L-38 (the bridge column),
extended at L-39 (the `aura` finding). Run SEALED at L-40.

Three deliverables, all ADDITIVE:

  (1) `v_vfx_kit_skill_binding` — the durable T-K materialization. The view BODY is the
      spec's § 4.1 "derivation of record", reproduced verbatim. No derivation is invented here.

  (2) The `folded_into` bridge on `vfx_archetype` — five new columns that make the
      DB-says-27 / spec-says-24 delta self-explaining WITHOUT reading the ledger, and that
      keep FOLDED and HELD as the distinct states the spec was careful to preserve.

  (3) The `aura` emitter-anchor mis-attestation finding (L-39 item 4), recorded as
      catalogue findings with per-row evidence. NOT a grain change — the key grain was
      Matt-audited and confirmed at L-39; reopening it is a HALT to Matt, not this script's call.

Iron laws honoured:
  - No UPDATE/DELETE against any pre-existing COLUMN. New columns only; new rows only in
    `vfx_curation_finding` (an append-only findings table by construction).
  - `vfx_archetype_member` is not touched at all — not one row, not one column.
  - Transactional + idempotent (re-run == verified no-op).
  - PRE-state asserted before any write; POST-state asserted before commit.

Substrate: agentic_orchestration/research/curated/corpus.db
Backup of record: corpus.db.pre-vfx-x4-20260824-backup (md5 5831c8bff5d1b50dc4fd2b0cd96c35c8)
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "curated" / "corpus.db"

VOTE_RUN = "vfx-archetype-vote-2026-08-23"
CURATION_RUN = "vfx-x4-materialization-2026-08-24"
RAISED_AT = "2026-08-24T00:00:00Z"
SOURCE_NOTE = "elrond/X-4 (charter L-35 commissioned, L-38 expanded, L-39 extended, L-40 sealed)"

# ---------------------------------------------------------------------------
# (1) The view. BODY IS THE SPEC § 4.1 DERIVATION OF RECORD, VERBATIM.
#     Do not "improve" this SELECT. If it needs to change, the spec changes first.
# ---------------------------------------------------------------------------
VIEW_SQL = f"""
CREATE VIEW v_vfx_kit_skill_binding AS
-- T-K: kit-skill -> (archetype, tier-1 layer flag)
-- Fold-aware per L-29(1) and L-29(2). Read-only. Body verbatim from spec § 4.1.
-- Materialized at X-4 (L-35 conductor ruling 1) so the binding is durable, not
-- re-derived by hand each time. The spec remains the authority; this is its executable form.
SELECT m.kit_id,
       m.skill_ordinal,
       m.source_skill,
       CASE m.archetype_id
            WHEN 'ring'           THEN 'circle'
            WHEN 'defensive_dash' THEN 'dash_attack'
            ELSE m.archetype_id
       END                                              AS archetype_id,
       CASE m.archetype_id
            WHEN 'ring'           THEN 'annulus'        -- Tier-1 layer flag: open travelling annulus
            WHEN 'defensive_dash' THEN 'defensive'      -- Tier-1 layer flag: i-frame / deflect flash
            ELSE NULL
       END                                              AS tier1_layer_flag,
       m.archetype_id                                   AS archetype_id_prefold,  -- lineage, never dropped
       m.geometry_value_raw,
       m.banded
FROM   vfx_archetype_member m
WHERE  m.vote_run     = '{VOTE_RUN}'
  AND  m.archetype_id IS NOT NULL
  AND  m.archetype_id <> 'knockback'                    -- HELD, § 3.2
"""

# ---------------------------------------------------------------------------
# (2) The bridge columns.
# ---------------------------------------------------------------------------
BRIDGE_COLUMNS = [
    # (name, DDL)
    ("fold_status",
     "ALTER TABLE vfx_archetype ADD COLUMN fold_status TEXT NOT NULL DEFAULT 'active' "
     "CHECK (fold_status IN ('active','folded','held'))"),
    ("folded_into",
     "ALTER TABLE vfx_archetype ADD COLUMN folded_into TEXT"),
    ("fold_survives_as",
     "ALTER TABLE vfx_archetype ADD COLUMN fold_survives_as TEXT"),
    ("fold_receives",
     "ALTER TABLE vfx_archetype ADD COLUMN fold_receives TEXT"),
    ("fold_authority",
     "ALTER TABLE vfx_archetype ADD COLUMN fold_authority TEXT"),
    ("fold_note",
     "ALTER TABLE vfx_archetype ADD COLUMN fold_note TEXT"),
]

# --- The RECEIVING side of the bridge. ---------------------------------------------------
# Without this a reader lands on `circle`, reads member_skills = 43, and is wrong by 50 skills:
# member_skills is a PRE-FOLD column and it was deliberately NOT rewritten (no mutation).
# The bridge has to be readable from both ends or it only half-closes the gap.
# These rows stay fold_status='active' and folded_into=NULL -- they folded nothing away.
RECEIVERS = {
    "circle": (
        "ring (50 skills / 47 kits, L-29(1))",
        "RECEIVED A FOLD -- READ `member_skills` / `member_kits` ON THIS ROW AS PRE-FOLD. "
        "This row's stored 43 / 43 is the P1 vote's `circle`-only count and was deliberately NOT "
        "rewritten, because rewriting a P1 measurement would destroy the reversibility the vote was "
        "built on. POST-FOLD TRUTH IS 93 skills / 88 kits (43 + 50 skills; 43 + 47 - 2 kit overlap, "
        "and the overlap is real, not asserted). The authoritative post-fold count comes from "
        "`v_vfx_kit_skill_binding`, never from this column. Rows arriving from `ring` carry "
        "tier1_layer_flag = 'annulus' and archetype_id_prefold = 'ring'."
    ),
    "dash_attack": (
        "defensive_dash (4 skills / 4 kits, L-29(2))",
        "RECEIVED A FOLD -- READ `member_skills` / `member_kits` ON THIS ROW AS PRE-FOLD. "
        "Stored 32 / 31 is the P1 `dash_attack`-only count, deliberately not rewritten. "
        "POST-FOLD TRUTH IS 36 skills / 35 kits -- kit overlap with `defensive_dash` is ZERO "
        "(verified), so 32 + 4 = 36 exactly. Authoritative post-fold count is "
        "`v_vfx_kit_skill_binding`. Rows arriving from `defensive_dash` carry "
        "tier1_layer_flag = 'defensive' and archetype_id_prefold = 'defensive_dash'."
    ),
}

# archetype_id -> (fold_status, folded_into, fold_survives_as, fold_authority, fold_note)
#
# THE DISTINCTION THIS TABLE EXISTS TO PRESERVE:
#   folded  => the archetype's members MOVED to another archetype. `folded_into` is non-NULL.
#   held    => the archetype's members went NOWHERE. `folded_into` is NULL, and must stay NULL.
# L-38's shorthand "knockback -> HELD" is rendered here as a STATUS, never as a fold target.
NON_ACTIVE = {
    "ring": (
        "folded",
        "circle",
        "annulus",
        "L-29(1)",
        "LOSSLESS FOLD. All 50 skills / 47 kits moved to `circle` and none was dropped: "
        "circle 43 + ring 50 = 93 skills post-fold; kits 43 + 47 - 2 overlap = 88. "
        "`ring` survives as an ALIAS of `circle`; its distinguishing read -- the open travelling "
        "annulus -- survives as the `annulus` Tier-1 layer flag (variant reference D2R Poison Nova). "
        "Merged name is `circle` because that is the attested engine spatial primitive. "
        "Per-row lineage is recoverable from v_vfx_kit_skill_binding.archetype_id_prefold and from "
        "vfx_archetype_member.archetype_id, neither of which was rewritten."
    ),
    "defensive_dash": (
        "folded",
        "dash_attack",
        "defensive",
        "L-29(2)",
        "LOSSLESS FOLD. All 4 skills / 4 kits moved to `dash_attack`; kit overlap with `dash_attack` "
        "is ZERO (verified), so 32 + 4 = 36 skills exactly and 31 + 4 = 35 kits exactly. "
        "Its `motion_signature = NULL` was an UNBANDED ARTEFACT, not an attested pathless class -- "
        "all 5 curated candidates are dashes and `windup = N` across all five is the signature of an "
        "unbanded class. It is a LAYER, not a geometry: it survives as the `defensive` Tier-1 "
        "flourish layer (i-frame / deflect flash bound to the mover), reference Hades II Divine Dash."
    ),
    "knockback": (
        "held",
        None,                       # <-- deliberately NULL. HELD IS NOT A FOLD.
        None,
        "L-14 + L-29 (F-3), re-affirmed at the P3 gate",
        "HELD -- NOT FOLDED, and the difference is load-bearing. Its 1 skill / 1 kit "
        "(`Ancient Spear (Rage Flip rune)`) moved NOWHERE; it has zero corpus, no dossier, no "
        "canonical, no runner-up, no scores. `folded_into` is NULL BY INTENT: representing HELD as "
        "a fold would assert a destination the run deliberately refused to name. F-3 evidence: it is "
        "the ONLY archetype in the vote with motion_signature NULL AND delivery unbanded AND no "
        "engine_spatial_primitive AND a single member -- an EFFECT noun sitting in a GEOMETRY slot, "
        "the signature of a vocabulary leak rather than a real class. Kept rather than deleted per "
        "Discipline #41 (a cluster of one is a finding, not an error). Proposed disposition: re-band "
        "the single member at the next kit-mapping lap; if it survives re-banding it earns a P2 "
        "dossier job and a T-A row. It is EXCLUDED from v_vfx_kit_skill_binding."
    ),
}

# ---------------------------------------------------------------------------
# (3) The `aura` emitter-anchor findings (L-39 item 4).
#     Every row hand-adjudicated against its own delivery_notes. No regex verdicts:
#     the regex was used to NOMINATE, a human read decided, and both the false positives
#     and the regex's MISSES are recorded below.
# ---------------------------------------------------------------------------
AURA_FINDINGS = [
    ("X001", "emitter-anchor-mis-attestation", "WARN", "aura", "aura (73 members)",
     "SUMMARY OF RECORD. L-39 item 4 asked whether the Demonologist 39-demon companion swarm is "
     "mis-attested as `aura`. MEASURED, not estimated: it is, AND IT IS NOT ALONE. Of the 73 skills "
     "attested `aura`, SIX carry an emitter anchor that is NOT the caster, which is what T-A § 3.1.8 "
     "means by `aura` (caster-centred persistent field). They split into two distinct sub-shapes: "
     "(A) PLACED / WORLD-ANCHORED, n=4 -- the emitter is a stationary body or object standing at a "
     "point in the world (Oak Sage x2, Big Bad Voodoo, Holy Banner). This is `totem` emitter "
     "geometry (two-layered: delegate body + emitted effect), not `aura`. "
     "(B) DELEGATE-CARRIED / DISTRIBUTED, n=2 -- there are N fields, each bound to a MOVING delegate "
     "body (Infernal Legion, Demon army). "
     "A further TWO rows are composite-and-contradictory (see X004) for a nominal ceiling of 8/73. "
     "Confirmed rate 6/73 = 8.2%; ceiling 8/73 = 11.0%. "
     "THIS IS NOT A GRAIN CHANGE AND IS NOT PROPOSED AS ONE -- the `geometry_value` key grain was "
     "Matt-audited and CONFIRMED at L-39, and reopening it is a HALT to Matt, not elrond's call. "
     "It is an attestation-quality finding for the next kit-mapping lap: the axis these rows differ "
     "on is EMITTER ANCHOR (caster-centred / world-placed / delegate-bound), which the `aura` gloss "
     "does not test for and therefore cannot catch."),

    ("X002", "emitter-anchor-mis-attestation", "WARN", "aura",
     "d2-summon-druid#3; d2-wind-druid#3; d3-mundunugu-sb#3; di-crusader-banner-support#0",
     "SUB-SHAPE A -- PLACED / WORLD-ANCHORED (totem-shaped), n=4, evidence verbatim from each row's "
     "own delivery_notes. (1) `d2-summon-druid#3` Oak Sage: \"Spirit summon -- life-bonus aura for "
     "entire party/self. Totem-vs-companion: Oak Sage is stationary placed emitter = maps as aura "
     "(not summoner GAP).\" -- the curator NAMED the anchor as a stationary placed emitter and still "
     "routed it to `aura`; this is a DELIBERATE CALL to disagree with, not an oversight, and it is "
     "recorded as such. (2) `d2-wind-druid#3` Oak Sage: \"Spirit that grants life bonus to player and "
     "party\" -- the same skill in a second kit, WITHOUT the adjudicating note. (3) `d3-mundunugu-sb#3` "
     "Big Bad Voodoo -- D3's placed dancing fetish; the row's notes are entirely set-bonus uptime and "
     "attest no anchor at all. (4) `di-crusader-banner-support#0` Holy Banner: \"Planted stationary "
     "aura; 11.2s duration; buff range around placement point\" -- explicitly placement-anchored, and "
     "the row further notes an item (Arrowkeeper) that makes it follow the caster, i.e. the anchor is "
     "a VARIABLE of this skill, which is exactly the property `aura` cannot express."),

    ("X003", "emitter-anchor-mis-attestation", "WARN", "aura",
     "poe2-infernal-legion#0; chr-demon-legion-warlock#1",
     "SUB-SHAPE B -- DELEGATE-CARRIED / DISTRIBUTED, n=2. (1) `poe2-infernal-legion#0`: \"the MINIONS "
     "are the delivery vehicle... each burning minion carries a small self-origin fire aura, and "
     "multiple minions create overlapping distributed coverage... Geometry is per-minion aura "
     "(presence), not a player-aimed shape; the player positions the swarm.\" The field is REAL; the "
     "ANCHOR is wrong -- N fields on N moving bodies, not one field on the caster. This row is "
     "STRONGER evidence than the L-39 seed case because its own notes name the anchor outright. "
     "(2) `chr-demon-legion-warlock#1` Demon army (Demonologist companion swarm -- 39 demons): "
     "\"Companion swarm fills large combat zone independently. 'demons disperse and fill large combat "
     "zone independently.'\" NOTE THE ASYMMETRY, because it matters for Step 2: the L-39 seed case is "
     "the LEAST field-shaped of the six. Infernal Legion has a genuine field with a wrong anchor; the "
     "Demon army arguably has NO field at all -- `aura` is standing in for 'swarm coverage', i.e. an "
     "AREA OUTCOME produced by 39 independent bodies. A VFX built to the `aura` binding (radius ring "
     "+ influence particles, per T-A § 4.3) would render the wrong thing for this kit: the player "
     "would see a field where the game shows a crowd."),

    ("X004", "contradictory-cross-kit-attestation", "WARN", "aura",
     "tli-iris2-thunder-magus#1; tli-moto-bots#1",
     "COMPOSITE + CONTRADICTORY, n=2, carried as a CEILING not as a confirmed mis-attestation, "
     "because the rows disagree with each other and this finding will not resolve that by preference. "
     "The same named skill, `Machine Army`, is attested TWO WAYS in two kits: "
     "`tli-iris2-thunder-magus#1` says \"Machine Army summons front-line guard\" (a delegate) while "
     "`tli-moto-bots#1` says \"Machine Army = buff aura\" (a field). Both rows are bundle entries "
     "pairing Machine Army with Dark Gate under a single `aura` value, so neither row is cleanly "
     "one shape. The finding is the CONTRADICTION ITSELF -- one skill name, two incompatible attested "
     "shapes, inside one vote -- which is a source-fidelity item for the re-mapping lap, not "
     "something to adjudicate from the archetype table."),

    ("X005", "negative-result", "INFO", "self_buff",
     "self_buff (112 members) -- the control",
     "NEGATIVE RESULT, BANKED SO THE NEXT LAP DOES NOT RE-RULE-OUT THE SAME DEAD END. The obvious "
     "hypothesis after X001 is that FIELD-CARRIED archetypes generally absorb summon-shaped skills. "
     "TESTED AGAINST `self_buff`, the other FIELD-CARRIED archetype (T-A § 4.3): the same summon "
     "lexicon nominates 6 rows, and ZERO of the 6 is an anchor error. Every one is a deliberate, "
     "correctly-reasoned separation of the ACTIVATION HANDLE from the summoned consequence -- "
     "`poe1-generals-cry#0` states it outright: \"the cry itself is a self-origin proc-trigger, not "
     "damage. self_buff = the warcry activation handle; the summoned warriors carry the offense.\" "
     "Likewise Brand Recall (reposition utility), Mirage Deadeye (\"a proxy-echo of the player's own "
     "ranged attack, not an independent minion loop\"), Unstable Currents (timed proc), Wings of Storm "
     "(companion-uptime STAT buff on the player). CONCLUSION: this is NOT a general field-archetype "
     "defect. It is specific to `aura`, and specifically to the case where the delegate bodies "
     "THEMSELVES are the emitting surface -- which is the one case `self_buff`'s activation-handle "
     "convention never has to face."),

    ("X006", "method-note", "INFO", "aura",
     "method: regex nominates, a read decides",
     "METHOD, STATED SO THE NUMBERS CAN BE AUDITED -- and stated because L-39 itself admitted a regex "
     "over-count ('immobile turret' matched 'mobile'). A summon lexicon "
     "(summon|companion|minion|pet|swarm|golem|skeleton) over `source_skill` + `delivery_notes` "
     "nominated 8 of the 73 `aura` rows. Hand-reading all 8 CONFIRMED 3 and REJECTED 4 as false "
     "positives where the vocabulary is present but the emitter is genuinely caster-centred "
     "(`poe2-grim-feast` -- 'minion-revival rework' appears only in an errata aside; "
     "`di-blood-knight` -- 'Swarm of Bats' is the ESSENCE NAME, the mapped form is a player-centred "
     "AoE drain; `tq-trap-magician` -- pets are the buff TARGET, not the emitter; "
     "`tli-youga-spirit-magus` -- minions appear only in skill-loop context). "
     "THE REGEX ALSO MISSED THREE OF THE SIX CONFIRMED ROWS -- `d2-wind-druid#3` (Oak Sage, described "
     "without any lexicon word), `d3-mundunugu-sb#3` (Big Bad Voodoo), `di-crusader-banner-support#0` "
     "(Holy Banner) -- all three recovered only by reading the full 73-row member list by eye. "
     "PRECISION 3/8 = 37.5%, RECALL 3/6 = 50%. Anyone re-running a lexicon scan on this cell should "
     "expect it to both over- and under-count, and should read the cell."),

    ("X007", "derivation-count-discrepancy", "WARN", None,
     "spec 2026-08-24 § 3.1a headline and § 4.1 verification table: 'Bound rows returned 1,135'",
     "SURFACED, NOT SILENTLY RECONCILED. The spec's § 4.1 derivation of record, executed verbatim "
     "against corpus.db at X-4, returns 1,134 bound rows -- not the 1,135 printed in its own "
     "verification table and § 3.1a headline. The delta is ONE ROW and its cause is exact: the "
     "verification row's parenthetical formula is '1,138 skill rows - 3 unassignable' = 1,135, which "
     "stops one clause short of the derivation it is verifying -- the SQL also carries "
     "`AND m.archetype_id <> 'knockback'`, and the very next line of the same table records "
     "'knockback excluded: 1 row held out'. 1,135 is the count of ASSIGNED skills (P1's number, and "
     "the denominator in the P1 note's '847 / 1,135 = 74.6%'); 1,134 is the count of BOUND skills "
     "(post-hold, which is what T-K is). "
     "THE SPEC IS INTERNALLY CORRECT EVERYWHERE ELSE: its own § 3.1a index sums to exactly 1,134 "
     "across the 24 active rows, and `vfx_archetype.member_skills` summed over the 26 non-held "
     "archetypes is also exactly 1,134 (1,135 including knockback). So this is a headline/derivation "
     "off-by-one in two printed cells, NOT a substrate defect and NOT a lost skill. "
     "511 kits VERIFIED EXACTLY. Zero skills lost to the folds VERIFIED EXACTLY "
     "(pre-fold 43+50+32+4 = 129 = post-fold 93+36). "
     "Routed to gandalf (spec author) via KR as an editorial correction to two cells; no re-ruling "
     "is implied and none is requested."),
]

# Sub-shape tags per member row, recorded as individual findings so the evidence is per-row
# addressable rather than only readable as prose.
AURA_ROWS = [
    ("X010", "d2-summon-druid#3", "A/placed-world-anchored",
     "Oak Sage -- \"stationary placed emitter\" NAMED in the row's own delivery_notes; routed to "
     "`aura` deliberately ('not summoner GAP'). Totem emitter geometry."),
    ("X011", "d2-wind-druid#3", "A/placed-world-anchored",
     "Oak Sage, second instance -- \"Spirit that grants life bonus to player and party\". Same skill "
     "as X010 but WITHOUT the adjudicating note; the two rows are consistent with each other and "
     "inconsistent with `aura`'s caster-centred definition."),
    ("X012", "d3-mundunugu-sb#3", "A/placed-world-anchored",
     "Big Bad Voodoo -- D3's placed dancing fetish. The row's delivery_notes attest ONLY set-bonus "
     "uptime and no anchor at all, so `aura` here rests on no emitter evidence either way."),
    ("X013", "di-crusader-banner-support#0", "A/placed-world-anchored",
     "Holy Banner -- \"Planted stationary aura... buff range around placement point\". Explicitly "
     "placement-anchored; and an item variant (Arrowkeeper) makes it follow the caster, so the "
     "anchor is a VARIABLE of the skill, which `aura` cannot express."),
    ("X014", "poe2-infernal-legion#0", "B/delegate-carried",
     "\"the MINIONS are the delivery vehicle... each burning minion carries a small self-origin fire "
     "aura... Geometry is per-minion aura (presence), not a player-aimed shape; the player positions "
     "the swarm.\" Real field, wrong anchor, N of them."),
    ("X015", "chr-demon-legion-warlock#1", "B/delegate-carried",
     "THE L-39 SEED CASE. \"Companion swarm fills large combat zone independently.\" 39 independent "
     "bodies producing an AREA OUTCOME. Least field-shaped of the six -- arguably no field exists at "
     "all, and a T-A `aura` VFX (radius ring + influence particles) would render a field where the "
     "game shows a crowd."),
]


def col_exists(cx: sqlite3.Connection, table: str, col: str) -> bool:
    return any(r[1] == col for r in cx.execute(f"PRAGMA table_info({table})"))


def scalar(cx: sqlite3.Connection, sql: str, args=()) -> int:
    return cx.execute(sql, args).fetchone()[0]


def main() -> int:
    if not DB.exists():
        print(f"FATAL: {DB} not found", file=sys.stderr)
        return 2

    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys = ON")

    # ---------------- PRE-STATE ASSERTS ----------------
    # These are the numbers the whole deliverable rests on. If any has moved, STOP.
    pre = {
        "archetypes": scalar(cx, "SELECT COUNT(*) FROM vfx_archetype WHERE vote_run=?", (VOTE_RUN,)),
        "member_rows": scalar(cx, "SELECT COUNT(*) FROM vfx_archetype_member WHERE vote_run=?", (VOTE_RUN,)),
        "skill_rows": scalar(cx, "SELECT COUNT(*) FROM vfx_archetype_member WHERE vote_run=? AND skill_ordinal>=0", (VOTE_RUN,)),
        "assigned": scalar(cx, "SELECT COUNT(*) FROM vfx_archetype_member WHERE vote_run=? AND skill_ordinal>=0 AND archetype_id IS NOT NULL", (VOTE_RUN,)),
    }
    expect_pre = {"archetypes": 27, "member_rows": 1158, "skill_rows": 1138, "assigned": 1135}
    if pre != expect_pre:
        print(f"FATAL: PRE-state moved.\n  expected {expect_pre}\n  actual   {pre}", file=sys.stderr)
        return 3
    print(f"PRE-state OK: {pre}")

    already = col_exists(cx, "vfx_archetype", "folded_into")
    view_exists = scalar(cx, "SELECT COUNT(*) FROM sqlite_master WHERE type='view' AND name='v_vfx_kit_skill_binding'")
    print(f"idempotency probe: bridge_present={already} view_present={bool(view_exists)}")

    try:
        cx.execute("BEGIN")

        # ---------------- (2) BRIDGE COLUMNS ----------------
        # ALTER TABLE ADD COLUMN is schema-additive: SQLite appends the column and does not
        # rewrite a single existing value. No pre-existing column is read-modified-written.
        for name, ddl in BRIDGE_COLUMNS:
            if not col_exists(cx, "vfx_archetype", name):
                cx.execute(ddl)
                print(f"  + column vfx_archetype.{name}")

        for aid, (status, into, survives, authority, note) in NON_ACTIVE.items():
            n = scalar(cx, "SELECT COUNT(*) FROM vfx_archetype WHERE archetype_id=? AND vote_run=?", (aid, VOTE_RUN))
            if n != 1:
                raise RuntimeError(f"expected exactly 1 vfx_archetype row for {aid}, found {n}")
            cx.execute(
                "UPDATE vfx_archetype SET fold_status=?, folded_into=?, fold_survives_as=?, "
                "fold_authority=?, fold_note=? WHERE archetype_id=? AND vote_run=?",
                (status, into, survives, authority, note, aid, VOTE_RUN),
            )
            print(f"  ~ bridge {aid}: status={status} folded_into={into!r} survives_as={survives!r}")

        for aid, (receives, note) in RECEIVERS.items():
            n = scalar(cx, "SELECT COUNT(*) FROM vfx_archetype WHERE archetype_id=? AND vote_run=?", (aid, VOTE_RUN))
            if n != 1:
                raise RuntimeError(f"expected exactly 1 vfx_archetype row for {aid}, found {n}")
            cx.execute(
                "UPDATE vfx_archetype SET fold_receives=?, fold_note=? WHERE archetype_id=? AND vote_run=?",
                (receives, note, aid, VOTE_RUN),
            )
            print(f"  ~ bridge {aid}: receives={receives!r}")

        # ---------------- (1) THE VIEW ----------------
        cx.execute("DROP VIEW IF EXISTS v_vfx_kit_skill_binding")
        cx.execute(VIEW_SQL)
        print("  + view v_vfx_kit_skill_binding")

        # ---------------- (3) THE FINDINGS ----------------
        cx.execute("DELETE FROM vfx_curation_finding WHERE curation_run=?", (CURATION_RUN,))
        for fid, kind, sev, aid, subject, detail in AURA_FINDINGS:
            cx.execute(
                "INSERT INTO vfx_curation_finding "
                "(curation_run, finding_id, kind, severity, archetype_id, candidate_rank, "
                " subject, detail, status, raised_at, target_curation_run) "
                "VALUES (?,?,?,?,?,NULL,?,?,?,?,?)",
                (CURATION_RUN, fid, kind, sev, aid, subject, detail, "LOGGED", RAISED_AT, VOTE_RUN),
            )
        for fid, row_key, subshape, detail in AURA_ROWS:
            cx.execute(
                "INSERT INTO vfx_curation_finding "
                "(curation_run, finding_id, kind, severity, archetype_id, candidate_rank, "
                " subject, detail, status, raised_at, target_curation_run) "
                "VALUES (?,?,?,?,?,NULL,?,?,?,?,?)",
                (CURATION_RUN, fid, "emitter-anchor-row", "INFO", "aura", row_key,
                 f"[{subshape}] {detail}", "LOGGED", RAISED_AT, VOTE_RUN),
            )
        print(f"  + {len(AURA_FINDINGS) + len(AURA_ROWS)} findings under {CURATION_RUN}")

        # ---------------- POST-STATE ASSERTS ----------------
        v = "v_vfx_kit_skill_binding"
        post = {
            "bound_rows": scalar(cx, f"SELECT COUNT(*) FROM {v}"),
            "kits": scalar(cx, f"SELECT COUNT(DISTINCT kit_id) FROM {v}"),
            "archetypes": scalar(cx, f"SELECT COUNT(DISTINCT archetype_id) FROM {v}"),
            "annulus": scalar(cx, f"SELECT COUNT(*) FROM {v} WHERE tier1_layer_flag='annulus'"),
            "defensive": scalar(cx, f"SELECT COUNT(*) FROM {v} WHERE tier1_layer_flag='defensive'"),
            "circle_skills": scalar(cx, f"SELECT COUNT(*) FROM {v} WHERE archetype_id='circle'"),
            "circle_kits": scalar(cx, f"SELECT COUNT(DISTINCT kit_id) FROM {v} WHERE archetype_id='circle'"),
            "dash_skills": scalar(cx, f"SELECT COUNT(*) FROM {v} WHERE archetype_id='dash_attack'"),
            "dash_kits": scalar(cx, f"SELECT COUNT(DISTINCT kit_id) FROM {v} WHERE archetype_id='dash_attack'"),
            "knockback_in_view": scalar(cx, f"SELECT COUNT(*) FROM {v} WHERE archetype_id='knockback'"),
        }
        # NOTE: bound_rows is 1134, NOT the 1,135 the spec's verification table prints.
        # See finding X007. The assert encodes the MEASURED truth, not the printed claim.
        expect_post = {
            "bound_rows": 1134, "kits": 511, "archetypes": 24,
            "annulus": 50, "defensive": 4,
            "circle_skills": 93, "circle_kits": 88,
            "dash_skills": 36, "dash_kits": 35,
            "knockback_in_view": 0,
        }
        if post != expect_post:
            raise RuntimeError(f"POST-state assert FAILED.\n  expected {expect_post}\n  actual   {post}")

        # Losslessness, asserted rather than asserted-in-prose:
        # every pre-fold member row appears in the view exactly once, under its folded name.
        lost = scalar(cx, f"""
            SELECT COUNT(*) FROM vfx_archetype_member m
            WHERE m.vote_run='{VOTE_RUN}' AND m.archetype_id IS NOT NULL
              AND m.archetype_id <> 'knockback'
              AND NOT EXISTS (SELECT 1 FROM {v} b
                              WHERE b.kit_id=m.kit_id AND b.skill_ordinal=m.skill_ordinal)
        """)
        if lost:
            raise RuntimeError(f"LOSSLESSNESS assert FAILED: {lost} member rows absent from the view")

        # Every folded row is recoverable to its pre-fold identity from the view alone.
        unrecoverable = scalar(cx, f"""
            SELECT COUNT(*) FROM {v}
            WHERE archetype_id_prefold IN ('ring','defensive_dash')
              AND tier1_layer_flag IS NULL
        """)
        if unrecoverable:
            raise RuntimeError(f"RECOVERABILITY assert FAILED: {unrecoverable} folded rows carry no layer flag")

        # The bridge must be reciprocal: every fold target must itself declare what it received,
        # or a reader approaching from the receiving side silently gets a pre-fold count.
        one_way = cx.execute(
            "SELECT f.archetype_id, f.folded_into FROM vfx_archetype f "
            "WHERE f.vote_run=? AND f.folded_into IS NOT NULL "
            "  AND NOT EXISTS (SELECT 1 FROM vfx_archetype t WHERE t.vote_run=f.vote_run "
            "                  AND t.archetype_id=f.folded_into AND t.fold_receives IS NOT NULL)",
            (VOTE_RUN,),
        ).fetchall()
        if one_way:
            raise RuntimeError(f"RECIPROCITY assert FAILED: one-way folds {one_way}")

        # HELD must never look like a fold.
        bad_held = scalar(cx, "SELECT COUNT(*) FROM vfx_archetype WHERE fold_status='held' AND folded_into IS NOT NULL")
        if bad_held:
            raise RuntimeError("HELD/FOLDED assert FAILED: a held archetype carries a fold target")

        # The 27 -> 24 gap must be arithmetic that closes from the table alone.
        gap = cx.execute(
            "SELECT fold_status, COUNT(*) FROM vfx_archetype WHERE vote_run=? GROUP BY 1 ORDER BY 1", (VOTE_RUN,)
        ).fetchall()
        if dict(gap) != {"active": 24, "folded": 2, "held": 1}:
            raise RuntimeError(f"27->24 gap assert FAILED: {gap}")

        cx.execute("COMMIT")
        print(f"POST-state OK: {post}")
        print(f"27 = 24 active + 2 folded + 1 held  -> {dict(gap)}")
        print("COMMITTED.")

    except Exception as exc:  # noqa: BLE001
        cx.execute("ROLLBACK")
        print(f"ROLLED BACK: {exc}", file=sys.stderr)
        return 4

    cx.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    ok = cx.execute("PRAGMA integrity_check").fetchone()[0]
    print(f"integrity_check: {ok}")
    cx.close()
    return 0 if ok == "ok" else 5


if __name__ == "__main__":
    raise SystemExit(main())
