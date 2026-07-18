#!/usr/bin/env python3
"""
VDM-1 stale-flag bulk reclassification — STALE-LANDED tier ONLY.
Owner: elrond (single-writer of corpus.db).
Charter: agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md §2
  (2026-07-12 mobile_blocking_mechanics flags ruled "stale; refreshed during probe
   backfill, never trusted as current truth").
Triage input: agentic_orchestration/research/vdm1/stage0/stale-flag-inventory.md
  (legolas Stage-0 inventory, commit 6ea07069 — triaged all 515 flagged rows).
MIGRATION doc: agentic_orchestration/research/curated/MIGRATION-stale-flag-reclass-2026-07-18.md
Backup (taken by caller BEFORE this runs):
  corpus.db.pre-stale-reclass-2026-07-18-backup

WHAT THIS DOES (mechanical tier only):
  For the 14 flag values legolas classed STALE-LANDED (~397 rows), move the flag
  aside ADDITIVELY — the mechanism has landed in-engine (mechanics-run Waves A/B/C
  + ailment-layer, i.e. Waves A-D per current-to-end-state-engine.md), so the flag
  no longer describes a current blocker.

  Pattern (requirements from the dispatch):
    (a) original flag string SURVIVES, queryable, in a NEW column
        `mobile_blocking_mechanics_archived`, provenance-tagged as
        'LANDED-<wave>: <original string>'  (history NOT deleted).
    (b) live `mobile_blocking_mechanics` for those rows set to the non-blocker
        sentinel 'expressible-now' (no longer presents as a current blocker).
    (c) a per-flag-value count ledger is emitted (lands in the MIGRATION doc).

WHAT THIS DOES NOT TOUCH (explicitly deferred — listed in MIGRATION doc):
  - STALE-PARTIALLY / STALE-LARGELY (~74 rows, 6 flags): per-kit split needed.
  - classification-workflow artifact ('evidence record — see harvest report', 18).
  - STILL-OPEN: 'form-swap stat-block hotswap' (10, GX-02 Matt-gated) +
    'union/recipe evolution system (pair-grain authoring)' (6, docket candidate).

LAWS enforced here (mirrors the VDM-1 schema-landing discipline):
  - fail-loud, single transaction, ROLLBACK on any assert mismatch.
  - total canon_corpus row count UNCHANGED.
  - content-md5 over the 66 UNTOUCHED columns (everything except
    `mobile_blocking_mechanics`) byte-identical PRE vs POST — proves the only
    live-field mutation is on the archived flag, and the new archived column is
    purely additive.
  - the DO-NOT-TOUCH 16 rows (form-swap 10 + union/recipe 6) verifiably unchanged
    across ALL columns (all-column md5 PRE == POST).
  - every STALE-LANDED row ends with BOTH: archived string prefixed 'LANDED-...',
    AND live flag == 'expressible-now'. No STALE-LANDED row left half-migrated.
  - no flag value outside the 14 STALE-LANDED is altered.
  - PRAGMA integrity_check == ok.
  - all pre-existing table row counts conserved; corpus_schema_meta +1.

Concurrency: two legolas crawlers read via sqlite3 -readonly concurrently.
  Keep the write transaction short (single UPDATE per flag + one ALTER + one
  meta INSERT). WAL journalling already active on this DB.
"""
import sqlite3, hashlib, sys, os

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"

# ---- pre-migration invariants (captured read-only before this run) ----
# content-md5 over the 66 columns that are NOT `mobile_blocking_mechanics`
# (the archived column does not exist yet, so 66 == all-1).
PRE_UNTOUCHED_MD5 = "e11b431380a2b2ba97ae994e15fc1dbe"
# all-column fingerprint of the 16 DO-NOT-TOUCH rows (form-swap 10 + union/recipe 6)
PRE_DEFER16_MD5   = "b69e11dfaff0c2a2bab454313078beb0"

# the 65 original cols + core_skills(+_prov) landed by vdm1-schema = 67 total live cols.
# UNTOUCHED = all of them minus mobile_blocking_mechanics (computed at runtime from
# table_info so a future column-add can't silently fall out of the invariant).
TOUCHED_FIELD = "mobile_blocking_mechanics"
ARCHIVE_FIELD = "mobile_blocking_mechanics_archived"
SENTINEL      = "expressible-now"   # non-blocker live reading for landed mechanisms

# ---- the 16 DO-NOT-TOUCH kit_ids (form-swap 10 + union/recipe 6) ----
DEFER16_IDS = [
    # form-swap stat-block hotswap (STILL-OPEN, GX-02 Matt-gated)
    "chr-fire-berserker","d4-pulverize","d4-rabies-lacerate","di-blood-knight",
    "di-druid-bear","gd-berserker-wereforms","le-reaper-form-lich",
    "le-swarmblade-druid","poe2-demon-form","poe2-shaman-bear",
    # union/recipe evolution system (STILL-OPEN, docket candidate)
    "hades1-merciful-end","hades2-glorious-disaster","hades2-hail-storm",
    "vs-fuwalafuwaloo","vs-phieraggi","vs-vandalier",
]

# ---- STALE-LANDED flag -> (wave-provenance label, expected row count) ----
# Wave labels + counts read straight from legolas's inventory ("Status:" line names
# the landing wave; the consolidated register names the count). Sum of counts = 397.
STALE_LANDED = {
    "direct-hit instant verbs native":
        ("A", 193),
    "soul-control troop command exists; turret/pet AI variants + summon economy needed":
        ("A+B", 66),
    "sustained-stream/channel verb + movement-tax tuning":
        ("B+C", 39),
    "mark/tag ledger + consume-trigger operators":
        ("C", 32),
    "rotational/orbital substrate addendum — build pending":
        ("C", 18),
    "thorns/stat-retaliation channel":
        ("C", 11),
    "self-cost contract operators":
        ("B+C", 8),
    "battle-sim auto-aim native":
        ("A", 8),
    "return-path/carom projectile solver":
        ("C+D", 7),
    "reservation/aura toggles — loot-operator extension":
        ("B", 7),
    "on-kill resource-spawn economy (corpse/soul ammo)":
        ("B", 3),
    "finite-ammo/consumable economy":
        ("B", 3),
    "element-application addendum covers hybrid caps — status-gate ops verify":
        ("C", 3),
    "lodge/retrieve ammo economy + return-path solver":
        ("B+C", 2),
    "reap/possession is RDR-native":
        ("A", 1),
    "default-attack scaling native to sim":
        ("A", 1),
}
# legolas's inventory summarized this tier as "~397"; the EXACT sum of the 16
# STALE-LANDED per-flag counts in his consolidated register is 402. The 402/113
# partition (402 + 79 STALE-PARTIALLY/LARGELY + 18 artifact + 16 STILL-OPEN = 515)
# is exact — see MIGRATION doc reconciliation note.
EXPECTED_STALE_LANDED_TOTAL = 402

# deferred tiers (untouched) — for the ledger only; NOT written to.
DEFERRED_UNTOUCHED = {
    # STALE-PARTIALLY / STALE-LARGELY (per-kit split — not this run)
    "no rule matched — Mac pass to classify": 45,
    "dash/blink verb — sim support verify; deflect riders new": 17,
    "echo/clone actors — troop-command adjacent": 9,
    "persistent/mobile zone entities — VFX slot model adjacent; follow-zones new": 5,
    "stochastic ops in loot-operator framework — per-cast roll verify": 3,
    # classification-workflow artifact
    "evidence record — see harvest report": 18,
    # STILL-OPEN
    "form-swap stat-block hotswap": 10,
    "union/recipe evolution system (pair-grain authoring)": 6,
}


def untouched_cols(con):
    allc = [r[1] for r in con.execute("PRAGMA table_info(canon_corpus)")]
    return [c for c in allc if c not in (TOUCHED_FIELD, ARCHIVE_FIELD)]


def content_md5(con, cols):
    sel = ",".join(f'"{c}"' for c in cols)
    h = hashlib.md5()
    for row in con.execute(f"SELECT {sel} FROM canon_corpus ORDER BY kit_id"):
        h.update(("\x1f".join("" if v is None else str(v) for v in row) + "\x1e").encode("utf-8"))
    return h.hexdigest()


def defer16_md5(con):
    # hash over the columns that existed PRE-migration (i.e. exclude the freshly
    # ALTER-added archive column, which is NULL for these rows anyway). This is the
    # true "did any real value on a DO-NOT-TOUCH row change" test; the PRE baseline
    # was computed before the archive column existed, so column sets align.
    allc = [r[1] for r in con.execute("PRAGMA table_info(canon_corpus)")
            if r[1] != ARCHIVE_FIELD]
    sel = ",".join(f'"{c}"' for c in allc)
    qs = ",".join("?" * len(DEFER16_IDS))
    h = hashlib.md5()
    for row in con.execute(
        f"SELECT {sel} FROM canon_corpus WHERE kit_id IN ({qs}) ORDER BY kit_id",
        DEFER16_IDS,
    ):
        h.update(("\x1f".join("" if v is None else str(v) for v in row) + "\x1e").encode("utf-8"))
    return h.hexdigest()


def all_table_counts(con):
    tbls = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tbls}


def main():
    if not os.path.exists(DB):
        sys.exit(f"FATAL: {DB} missing")
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    con.execute("PRAGMA busy_timeout=15000")   # coexist with readonly crawlers
    ledger = {}
    try:
        # -------------------- PRE asserts --------------------
        allc = [r[1] for r in con.execute("PRAGMA table_info(canon_corpus)")]
        assert TOUCHED_FIELD in allc, f"{TOUCHED_FIELD} missing from canon_corpus"
        assert ARCHIVE_FIELD not in allc, f"{ARCHIVE_FIELD} already exists — refusing to clobber"
        # idempotency: no row already carries the LANDED- provenance
        pre_landed = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD} LIKE 'LANDED-%'").fetchone()[0]
        assert pre_landed == 0, f"{pre_landed} rows already LANDED- prefixed — re-run guard tripped"
        pre_sentinel = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD}=?", (SENTINEL,)).fetchone()[0]
        assert pre_sentinel == 0, f"{pre_sentinel} rows already == sentinel — re-run guard tripped"

        pre_total = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
        pre_flagged = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus "
            f"WHERE {TOUCHED_FIELD} IS NOT NULL AND {TOUCHED_FIELD}!=''").fetchone()[0]
        pre_counts = all_table_counts(con)
        ut = untouched_cols(con)
        assert len(ut) == 66, f"expected 66 untouched cols, got {len(ut)}"
        pre_ut_md5 = content_md5(con, ut)
        assert pre_ut_md5 == PRE_UNTOUCHED_MD5, \
            f"PRE untouched-md5 mismatch: {pre_ut_md5} != {PRE_UNTOUCHED_MD5}"
        pre_d16 = defer16_md5(con)
        assert pre_d16 == PRE_DEFER16_MD5, f"PRE defer16-md5 mismatch: {pre_d16} != {PRE_DEFER16_MD5}"

        # verify each STALE-LANDED flag's live count matches legolas's expected count
        for flag, (wave, exp) in STALE_LANDED.items():
            got = con.execute(
                f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD}=?", (flag,)).fetchone()[0]
            assert got == exp, f"count drift on STALE-LANDED flag {flag!r}: db={got} inventory={exp}"
        assert sum(e for _, e in STALE_LANDED.values()) == EXPECTED_STALE_LANDED_TOTAL, \
            "STALE_LANDED count table does not sum to 397"
        # verify deferred flags' counts too (belt-and-braces on the inventory match)
        for flag, exp in DEFERRED_UNTOUCHED.items():
            got = con.execute(
                f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD}=?", (flag,)).fetchone()[0]
            assert got == exp, f"count drift on DEFERRED flag {flag!r}: db={got} inventory={exp}"

        # -------------------- WRITE (single transaction) --------------------
        con.execute("BEGIN")
        con.execute(f'ALTER TABLE canon_corpus ADD COLUMN {ARCHIVE_FIELD} TEXT')

        per_flag = {}
        for flag, (wave, exp) in STALE_LANDED.items():
            archived_val = f"LANDED-{wave}: {flag}"
            cur = con.execute(
                f"UPDATE canon_corpus "
                f"SET {ARCHIVE_FIELD}=?, {TOUCHED_FIELD}=? "
                f"WHERE {TOUCHED_FIELD}=?",
                (archived_val, SENTINEL, flag),
            )
            per_flag[flag] = {"wave": wave, "reclassified": cur.rowcount,
                              "expected": exp, "archived_as": archived_val}
            assert cur.rowcount == exp, \
                f"UPDATE affected {cur.rowcount} rows for {flag!r}, expected {exp}"
        ledger["per_flag"] = per_flag
        total_reclassified = sum(v["reclassified"] for v in per_flag.values())
        ledger["total_reclassified"] = total_reclassified

        # schema-meta ledger row
        meta_txt = (
            "VDM-1 stale-flag bulk reclass (elrond, charter §2). STALE-LANDED tier only: "
            f"{total_reclassified} rows across {len(STALE_LANDED)} flag values moved aside additively. "
            f"+canon_corpus.{ARCHIVE_FIELD} holds the original flag string, provenance-prefixed "
            "'LANDED-<wave>: <flag>' (Waves A-D landed the mechanism per current-to-end-state-engine.md). "
            f"Live {TOUCHED_FIELD} for those rows set to '{SENTINEL}' (no longer a current blocker). "
            "DEFERRED untouched: STALE-PARTIALLY/LARGELY (~74, per-kit split), evidence-record artifact (18), "
            "STILL-OPEN form-swap (10, GX-02 Matt-gated) + union/recipe (6, docket candidate). "
            "ADDITIVE ONLY; 66-col untouched content-md5 unchanged; form-swap 10 + union/recipe 6 "
            "all-col md5 unchanged; all pre-existing row counts conserved. "
            "Backup: corpus.db.pre-stale-reclass-2026-07-18-backup.")
        con.execute("INSERT INTO corpus_schema_meta VALUES (?,?,?)",
                    ("stale-flag-reclass-2026-07-18", "2026-07-18T00:00:00Z", meta_txt))

        # -------------------- POST asserts --------------------
        post_total = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
        assert post_total == pre_total, f"TOTAL ROW COUNT DRIFT: {pre_total} -> {post_total}"

        post_counts = all_table_counts(con)
        for t, n in pre_counts.items():
            exp = n + 1 if t == "corpus_schema_meta" else n
            assert post_counts[t] == exp, f"ROW COUNT DRIFT on {t}: {n} -> {post_counts[t]} (exp {exp})"

        post_ut_md5 = content_md5(con, ut)   # same 66 untouched cols
        assert post_ut_md5 == pre_ut_md5, \
            f"UNTOUCHED COLUMNS MUTATED: {post_ut_md5} != {pre_ut_md5}"
        post_d16 = defer16_md5(con)
        assert post_d16 == pre_d16, f"DEFER16 ROWS MUTATED: {post_d16} != {pre_d16}"

        # every STALE-LANDED row fully migrated (archived present + live == sentinel)
        landed_rows = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus WHERE {ARCHIVE_FIELD} LIKE 'LANDED-%'").fetchone()[0]
        assert landed_rows == total_reclassified, \
            f"archived-prefix count {landed_rows} != reclassified {total_reclassified}"
        sentinel_rows = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD}=?", (SENTINEL,)).fetchone()[0]
        assert sentinel_rows == total_reclassified, \
            f"sentinel live-flag count {sentinel_rows} != reclassified {total_reclassified}"
        half = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus "
            f"WHERE ({ARCHIVE_FIELD} LIKE 'LANDED-%') != ({TOUCHED_FIELD}=?)", (SENTINEL,)).fetchone()[0]
        assert half == 0, f"{half} rows half-migrated (archived xor sentinel)"

        # no deferred flag value was altered — each still present at its inventory count,
        # and none of those rows acquired an archived value
        for flag, exp in DEFERRED_UNTOUCHED.items():
            got = con.execute(
                f"SELECT COUNT(*) FROM canon_corpus WHERE {TOUCHED_FIELD}=?", (flag,)).fetchone()[0]
            assert got == exp, f"DEFERRED flag {flag!r} count changed: {got} != {exp}"
        deferred_touched = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus "
            f"WHERE {ARCHIVE_FIELD} IS NOT NULL AND {TOUCHED_FIELD} IN "
            f"({','.join('?'*len(DEFERRED_UNTOUCHED))})",
            list(DEFERRED_UNTOUCHED.keys())).fetchone()[0]
        assert deferred_touched == 0, f"{deferred_touched} deferred-flag rows got an archived value"

        # live flagged rows now == 515 - 397 = 118 non-sentinel deferred + 397 sentinel;
        # blocker-presenting rows (exclude sentinel) == sum of deferred counts.
        blocker_rows = con.execute(
            f"SELECT COUNT(*) FROM canon_corpus "
            f"WHERE {TOUCHED_FIELD} IS NOT NULL AND {TOUCHED_FIELD}!='' AND {TOUCHED_FIELD}!=?",
            (SENTINEL,)).fetchone()[0]
        assert blocker_rows == sum(DEFERRED_UNTOUCHED.values()), \
            f"residual blocker rows {blocker_rows} != deferred sum {sum(DEFERRED_UNTOUCHED.values())}"

        integ = con.execute("PRAGMA integrity_check").fetchone()[0]
        assert integ == "ok", f"integrity_check: {integ}"

        con.commit()

        ledger["asserts"] = {
            "pre_total": pre_total, "post_total": post_total, "total_conserved": post_total == pre_total,
            "untouched_md5_pre": pre_ut_md5, "untouched_md5_post": post_ut_md5,
            "untouched_md5_conserved": post_ut_md5 == pre_ut_md5,
            "defer16_md5_pre": pre_d16, "defer16_md5_post": post_d16,
            "defer16_conserved": post_d16 == pre_d16,
            "stale_landed_rows_migrated": total_reclassified,
            "archived_rows": landed_rows, "sentinel_rows": sentinel_rows, "half_migrated": half,
            "residual_blocker_rows": blocker_rows, "deferred_flag_rows": sum(DEFERRED_UNTOUCHED.values()),
            "row_counts_conserved": True, "schema_meta_rows": post_counts["corpus_schema_meta"],
            "integrity_check": integ,
        }
        import json
        print(json.dumps(ledger, indent=2, ensure_ascii=False))
        print("\nOK: VDM-1 stale-flag reclass committed.")
    except Exception as e:
        con.rollback()
        import json
        print(json.dumps(ledger, indent=2, ensure_ascii=False))
        sys.exit(f"ROLLED BACK — {type(e).__name__}: {e}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
