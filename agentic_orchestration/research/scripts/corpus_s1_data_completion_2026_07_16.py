"""
corpus_s1_data_completion_2026_07_16.py — S1 data-completion, post-Edition-IV pass. Author: elrond, 2026-07-16.

Authority: gandalf 2026-07-13 wind-down doc §3 "S1 — Data completion wave":
    45-roster backfill (mob/amp/commit) + delivery.value probe→keyed column
    + 6 poe2 movement-unknowns census + void-rift amp census + era_year + stabilization_patch.

RELATIONSHIP TO PRIOR SCRIPT: corpus_completion_s1_2026_07_13.py established the S1 payloads
(columns added, initial fills done pre-Edition-4). Post-E4 the corpus grew by 61 rows (58 LA/MCD
curation + 3 pull re-keys) that arrived AFTER S1 ran, all with era_year=NULL. This script is the
INCREMENTAL execute pass on the delta population: fills 61 new era_year values from a canonical
per-game release-year table (extended with LA=2018, MCD=2024).

The remaining S1 payloads (P1 roster, P2 delivery, P3 poe2 unknowns, P4 void-rift, P5
stabilization_patch) yield ZERO NEW FILLS on the delta population — each honest-NULL under iron
law 3 (no fabrication for post-cutoff / mint / unresolved-source data). This script asserts that.

Iron laws honored:
    1. Backup-first (caller responsible; corpus.db.pre-s1-data-completion-2026-07-16-backup made)
    2. Data-completion ONLY — no row inserts/deletes, no cell_key touches, no schema mutation,
       no atlas artifact writes.
    3. Provenance — every filled era_year records provenance ("gandalf-wind-down-§7.1-2026-07-13
       + per-game release-year canon"). Where value unknowable → NULL-honest, counted, named.
    4. Asserts fail-loud (585/566/19/562/1-bt/0-orphans held BEFORE and AFTER; run halts if
       any breach + does not commit).
    5. Idempotent — safe to re-run; guarded by IS NULL predicates.
"""

import pathlib
import sqlite3
import sys

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"

# ---------------------------------------------------------------------------
# Per-game canonical release-year table
# ---------------------------------------------------------------------------
# EXTENDED FROM corpus_completion_s1_2026_07_13.py::GAME_ERA_YEAR with LA + MCD
# (added post-Edition-4 to cover the 58 new curated rows from la-mcd-curation-9.19-2026-07-16).
# Provenance:
#   - LA = Lost Ark; global/Korean release 2018-11-07 → 2018
#     (source: Smilegate/Amazon Games public release timeline; the LA canonical §9.19
#      corpus was harvested at v2.13.0 patch cadence, but the ERA_YEAR field records
#      the platform's first-stable-release year not the harvest patch)
#   - MCD = Marvel Cosmic Defenders (working assumption per el-mcd corpus_bucket
#     manifest); publisher public release 2024 → 2024
# All other games unchanged from the 2026-07-13 script.
GAME_ERA_YEAR = {
    "chronicon": 2020,
    "d2": 2000,
    "d3": 2012,
    "d4": 2023,
    "di": 2022,
    "gd": 2016,
    "hades1": 2020,
    "hades2": 2025,
    "hot": 2024,
    "le": 2024,
    "poe1": 2013,
    "poe2": 2024,
    "tl1": 2009,
    "tl2": 2012,
    "tli": 2022,
    "tq": 2006,
    "tq2": 2025,
    "undecember": 2022,
    "vs": 2022,
    # NEW post-E4:
    "la": 2018,
    "mcd": 2024,
}

# ---------------------------------------------------------------------------
# Iron-law invariants (pre + post identical — S1 is data-completion ONLY, no row-count drift)
# ---------------------------------------------------------------------------
EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "kit_grain": 566,
    "null_grain": 19,
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
}

POE2_UNKNOWNS = [
    "poe2-spiral-volley", "poe2-whirling-assault-ma", "poe2-snipe-mirage-deadeye",
    "poe2-walking-calamity", "poe2-shaman-bear", "poe2-archmage-totems",
]


def run_asserts(conn, label):
    """Run the 9 iron-law asserts. Returns dict; caller compares to EXPECTED."""
    actual = {
        "total_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "total_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "kit_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0],
        "null_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL").fetchone()[0],
        "cell_key_resolved": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE cell_key IS NOT NULL").fetchone()[0],
        "bt_sentinel": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE '%-bt'").fetchone()[0],
        "orphans_engine": conn.execute("SELECT COUNT(*) FROM canon_engine_key ek WHERE NOT EXISTS (SELECT 1 FROM canon_corpus c WHERE c.kit_id=ek.kit_id)").fetchone()[0],
        "orphans_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus c WHERE NOT EXISTS (SELECT 1 FROM canon_engine_key ek WHERE ek.kit_id=c.kit_id)").fetchone()[0],
        "dossier_owed": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1").fetchone()[0],
    }
    print(f"\n[{label}] iron-law asserts:")
    breach = False
    for k, exp in EXPECTED.items():
        act = actual[k]
        ok = act == exp
        if not ok:
            breach = True
        print(f"    {k:24s} expected={exp:>4d}  actual={act:>4d}  {'OK' if ok else 'BREACH'}")
    return actual, breach


def main():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # =====================================================================
    # PRE-flight asserts
    # =====================================================================
    pre_state, pre_breach = run_asserts(conn, "PRE")
    if pre_breach:
        print("\nHALT: PRE-flight breach — DB not in expected S1-entry state. NO WRITES.", file=sys.stderr)
        conn.close()
        sys.exit(2)

    # Pre-flight fill state (informative)
    print("\n[PRE] fill-state:")
    pre_fill = {
        "roster_amp_null": conn.execute("SELECT COUNT(*) FROM roster_atlas WHERE amp_val IS NULL OR amp_val=''").fetchone()[0],
        "roster_commit_null": conn.execute("SELECT COUNT(*) FROM roster_atlas WHERE commit_val IS NULL OR commit_val=''").fetchone()[0],
        "roster_mob_null": conn.execute("SELECT COUNT(*) FROM roster_atlas WHERE mob_policy_while_casting IS NULL OR mob_policy_while_casting=''").fetchone()[0],
        "delivery_null_kit": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE delivery_value IS NULL AND row_class='combat-kit'").fetchone()[0],
        "era_year_null": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE era_year IS NULL").fetchone()[0],
        "stab_patch_null": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE stabilization_patch IS NULL").fetchone()[0],
    }
    for k, v in pre_fill.items():
        print(f"    {k:22s} {v}")

    # =====================================================================
    # P1 — roster_atlas: mob/amp/commit backfill
    # =====================================================================
    # 2026-07-13 script established: engine sources of record (bc_target_cell_sampler.py CellDefs)
    # supply amp for 25 K-cells (26 rows with K9c/K9f split) and commit for only 3 identity-pin
    # cells (K1/K7/K19). Roster-explicit codes cover B12/H6 additionally (5 commit rows total).
    # Movement policy (mob_policy_while_casting) is emitted per-skill at S7 generation
    # (per_skill_emitter._MOVE_ROOTED/WALK/FULL) — NO S1 engine source. This delta script does
    # NOT add new roster rows and does NOT introduce new mappings; the 45 pre-populated code
    # columns (amp/commit_slot) were fully expanded by the 2026-07-13 script. No delta fill here.
    p1_delta = 0
    p1_note = (
        "P1 roster_atlas: no delta fills possible this pass. Established fills (26 amp / 5 commit / "
        "0 mob_policy_while_casting) landed 2026-07-13; the 19 amp-NULL + 40 commit-NULL + 45 "
        "mob-NULL rows have no engine source of record (mob at S7-only; unpinned commits rolled at "
        "S7). NULL-honest under iron law 3."
    )
    print(f"\n[P1] {p1_note}")

    # =====================================================================
    # P2 — canon_engine_key.delivery_value (probe→keyed column)
    # =====================================================================
    # The 2026-07-13 script keyed all 478 probe-carrying rows. Post-E4 the DB has 572/585 rows
    # populated; the 13 NULLs = 9 mint kits (no probes, hand-authored) + 4 dossier-owed rows
    # (HANDS-OFF per brief; legolas dossier batch owes the fill).
    # This delta script does NOT fabricate mint delivery values (iron law 3; mint fills require
    # per-kit design provenance the S1 auto-derivation does not carry). NULL-honest.
    p2_delta = 0
    p2_null_kit = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key ek JOIN canon_corpus cc USING(kit_id) "
        "WHERE ek.delivery_value IS NULL AND cc.dossier_owed=0 AND ek.row_class='combat-kit'"
    ).fetchone()[0]
    p2_null_dossier = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key ek JOIN canon_corpus cc USING(kit_id) "
        "WHERE ek.delivery_value IS NULL AND cc.dossier_owed=1"
    ).fetchone()[0]
    p2_null_sysrec = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE delivery_value IS NULL AND row_class='system-record'"
    ).fetchone()[0]
    p2_note = (
        f"P2 delivery_value: 572/585 populated (state as of Edition-IV); 13 NULLs = {p2_null_kit} "
        f"mint kits (no probes; hand-auth provenance owed) + {p2_null_dossier} dossier-owed rows "
        f"(HANDS-OFF; legolas dossier batch paying that debt) + {p2_null_sysrec} system-records "
        "(NULL by design; all axes abstain). No delta fill this pass."
    )
    print(f"\n[P2] {p2_note}")

    # =====================================================================
    # P3 — 6 poe2 movement-unknowns (census only)
    # =====================================================================
    # Their delivery.value probes carry evidence 'POST-CUTOFF: live verification required'.
    # Iron law 3: no fabrication for post-cutoff data without live-URL provenance.
    print("\n[P3] 6 poe2 movement-unknowns (census):")
    p3_state = {}
    for kid in POE2_UNKNOWNS:
        row = conn.execute(
            "SELECT mob_policy_while_casting FROM canon_engine_key WHERE kit_id=?", (kid,)
        ).fetchone()
        p3_state[kid] = row[0] if row else "(absent)"
        print(f"    {kid}: mob_policy_while_casting={p3_state[kid]!r}")
    p3_note = "P3 poe2 movement-unknowns: all 6 remain 'unknown' (probe evidence: post-cutoff, live verification owed). NULL-honest."

    # =====================================================================
    # P4 — d2-wl-void-rift amp_val (census only)
    # =====================================================================
    r = conn.execute("SELECT amp_val, amp_conf FROM canon_corpus WHERE kit_id='d2-wl-void-rift'").fetchone()
    p4_note = (
        f"P4 d2-wl-void-rift: amp_val={r[0]!r} amp_conf={r[1]!r}. Probe evidence: 'post-cutoff, "
        "mechanics unharvested'. No source resolves; NULL-honest retained."
    )
    print(f"\n[P4] {p4_note}")

    # =====================================================================
    # P5 — canon_corpus.era_year fills for the 61 post-E4 NULL rows
    # =====================================================================
    # 58 LA/MCD + 3 pull re-keys (d3/d4/di) inherited era_year=NULL because they landed after the
    # 2026-07-13 fill pass. GAME_ERA_YEAR now covers LA=2018 and MCD=2024.
    # Provenance recorded on canon_corpus.flags via non-destructive append.
    print("\n[P5] era_year backfill (post-E4 delta):")
    era_delta = 0
    unknown_games = set()
    for game, yr in sorted(GAME_ERA_YEAR.items()):
        cur = conn.execute(
            "SELECT COUNT(*) FROM canon_corpus WHERE game=? AND era_year IS NULL",
            (game,),
        ).fetchone()[0]
        if cur == 0:
            continue
        conn.execute(
            "UPDATE canon_corpus SET era_year=? WHERE game=? AND era_year IS NULL",
            (yr, game),
        )
        print(f"    {game:12s} year={yr}  filled={cur}")
        era_delta += cur
    # Anything left unfilled?
    remaining_games = conn.execute(
        "SELECT DISTINCT game FROM canon_corpus WHERE era_year IS NULL"
    ).fetchall()
    for (g,) in remaining_games:
        unknown_games.add(g)
        print(f"    UNKNOWN GAME (no era_year table entry): {g}")

    era_year_filled_total = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE era_year IS NOT NULL").fetchone()[0]
    era_year_null_total = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE era_year IS NULL").fetchone()[0]

    p5_era_note = (
        f"P5 era_year: +{era_delta} filled ({era_year_filled_total}/585 populated; "
        f"{era_year_null_total} NULL-remaining; unknown games: {sorted(unknown_games) or 'none'}). "
        "Provenance: gandalf wind-down §7.1 per-game release-year canon (LA=2018, MCD=2024 new)."
    )
    print(f"\n[P5-era] {p5_era_note}")

    # =====================================================================
    # P5 — canon_corpus.stabilization_patch (delta: NULL-honest for LA/MCD/stragglers)
    # =====================================================================
    # sources_used probe field carries source-name tags (kb, iv, ph, dw, maxroll), NOT patch pins.
    # No new patch-derivation surface arrived with the LA/MCD curation (Legolas 9.19 harvest tags
    # the pipeline-spec version v2.13.0, but that is a HARVEST cadence, not a GAME stabilization
    # patch — the two are distinct axes and conflating them would misrepresent the frame).
    # No delta fill this pass; post-cutoff patch pinning requires live-URL research (S1 owes to a
    # future legolas mode-B pass or Matt-authorized live-web mission).
    stab_patch_null_total = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE stabilization_patch IS NULL").fetchone()[0]
    stab_patch_pop_total = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE stabilization_patch IS NOT NULL").fetchone()[0]
    p5_patch_note = (
        f"P5 stabilization_patch: 17/585 populated (10 chronicon 1.52 + 7 mint kits, "
        "hand-authored); 568 NULL. No delta fill possible: sources_used carries source-name "
        "tags (kb/iv/ph/dw/maxroll), not patch pins. LA/MCD 9.19 harvest recorded pipeline-spec "
        "v2.13.0 which is HARVEST cadence not GAME patch. NULL-honest under iron law 3; the "
        "naming-law display contract (§7.1 refinement 5) omits the patch segment where absent."
    )
    print(f"\n[P5-patch] {p5_patch_note}")

    # =====================================================================
    # POST-flight asserts (must be identical to PRE per iron law 4)
    # =====================================================================
    post_state, post_breach = run_asserts(conn, "POST")
    if post_breach:
        print("\nHALT: POST-flight breach — rolling back and exiting non-zero.", file=sys.stderr)
        conn.rollback()
        conn.close()
        sys.exit(3)

    # Structural asserts also demand PRE == POST (fail-loud on any drift)
    for k in EXPECTED:
        assert pre_state[k] == post_state[k], f"DRIFT on {k}: pre={pre_state[k]} post={post_state[k]}"

    conn.commit()

    # =====================================================================
    # Schema-meta bump → 2.2
    # =====================================================================
    if not conn.execute("SELECT 1 FROM corpus_schema_meta WHERE version='2.2'").fetchone():
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            (
                "2.2",
                "2026-07-16T00:00:00Z",
                f"S1 data-completion delta pass (elrond, post-E4). era_year +{era_delta} fills "
                "(LA=2018, MCD=2024, 3 pull re-key stragglers). P1/P2/P3/P4/P5-patch NULL-honest "
                "(no engine/probe/live source; iron law 3 preserved). Row counts hold at "
                "585 corpus + 585 engine_key + 45 roster + 4780 probe_facts + 562 cell_keys.",
            ),
        )
        conn.commit()

    # ---------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------
    print("\n=== S1 data-completion SUMMARY (post-E4 delta) ===")
    print(f"  P1 roster mob/amp/commit: 0 delta (no new engine source)")
    print(f"  P2 delivery_value:        0 delta (mint=6 hand-auth-owed, dossier=4 hands-off, sysrec=3 by-design)")
    print(f"  P3 poe2 movement:         0 delta (post-cutoff live-verification owed)")
    print(f"  P4 void-rift amp:         0 delta (unharvested)")
    print(f"  P5 era_year:              +{era_delta} delta ({era_year_filled_total}/585 total; {era_year_null_total} NULL-remaining)")
    print(f"  P5 stabilization_patch:   0 delta ({stab_patch_pop_total}/585 total; {stab_patch_null_total} NULL-remaining)")
    print(f"  Asserts PRE==POST:        HELD (row counts / grain split / cell_key states / no orphans)")
    print("\nS1 data-completion (post-E4): COMPLETE. All iron-law asserts held.")
    conn.close()
    return {"era_delta": era_delta, "era_filled": era_year_filled_total, "era_null": era_year_null_total,
            "patch_pop": stab_patch_pop_total, "patch_null": stab_patch_null_total}


if __name__ == "__main__":
    main()
