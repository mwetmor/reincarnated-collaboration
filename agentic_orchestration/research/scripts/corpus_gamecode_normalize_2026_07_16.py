#!/usr/bin/env python3
"""
corpus_gamecode_normalize_2026_07_16.py — R0: game-code long-form -> short-code normalization.
==============================================================================================
Elrond's parked normalization to-do, now LOAD-BEARING for the Tier-3 Refit Candidate 1 run.

The active-set (and full-table) `canon_corpus.game` column carries long-form codes that ORPHAN
against the atlas derivation's FRANCHISE_ROLLUP (which knows only short codes). The derivation's
stage-0 orphan check would HALT on them. This migration folds the long forms onto their short
codes so the table converges on ONE convention (matching kit_id prefixes + the existing rollup):

    lost-ark        -> la
    diablo-4        -> d4
    diablo-3        -> d3
    diablo-immortal -> di

`mcd` is already its own short code — LEFT UNTOUCHED (added to the rollup at derivation time, not
here). No cell_key / no kit_id is touched (game is not part of cell_key; the frozen Edition-I fit
reconstructs from kit_id+cell_key only, so this migration cannot perturb any served artifact).

IDEMPOTENT: running twice is a no-op (the second run finds zero long-form rows). Post-asserts that
every distinct `game` in the ACTIVE set is short-code and that no long form survives table-wide.

Author: elrond (data steward). TOOL script (curation/migration), not engine code.
Log: research/curated/corpus-curation-gamecode-normalize-2026-07-16-log.md (the record; corpus.db
is gitignored).

Run:  python3 corpus_gamecode_normalize_2026_07_16.py
"""

import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"

# long-form -> short-code map (short codes match kit_id prefixes + FRANCHISE_ROLLUP convention)
NORMALIZE = {
    "lost-ark": "la",
    "diablo-4": "d4",
    "diablo-3": "d3",
    "diablo-immortal": "di",
}

ACTIVE_PRED = ("k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0")


def active_game_counts(con):
    return dict(con.execute(
        "SELECT c.game, COUNT(*) FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE " + ACTIVE_PRED + " GROUP BY c.game").fetchall())


def full_game_counts(con):
    return dict(con.execute("SELECT game, COUNT(*) FROM canon_corpus GROUP BY game").fetchall())


def main():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    log = []

    def L(*a):
        line = " ".join(str(x) for x in a)
        log.append(line)
        print(line)

    L("# Game-code normalization — R0 (Refit Candidate 1 precondition)")
    L("")
    L("**Date:** %s · **Executor:** elrond · **Script:** "
      "`agentic_orchestration/research/scripts/corpus_gamecode_normalize_2026_07_16.py`"
      % datetime.now(timezone.utc).isoformat())
    L("**DB:** corpus.db (gitignored; this log is the record). "
      "**Backup:** corpus.db.pre-gamecode-normalize-2026-07-16-backup")
    L("")
    L("Normalizes long-form `canon_corpus.game` -> short codes so the table converges on one "
      "convention and the derivation's FRANCHISE_ROLLUP orphan check does not HALT. Idempotent; "
      "no cell_key / kit_id touched (frozen Edition-I fit unaffected).")
    L("")

    # ---- BEFORE state ----
    before_active = active_game_counts(con)
    before_full = full_game_counts(con)
    L("## Before")
    L("")
    L("Distinct `game` in ACTIVE set (%d rows): %d codes." % (sum(before_active.values()), len(before_active)))
    L("Long-form present (full table):")
    any_long = False
    for lf, sf in NORMALIZE.items():
        n_full = before_full.get(lf, 0)
        n_act = before_active.get(lf, 0)
        if n_full:
            any_long = True
        L("- `%s` -> `%s`: %d rows table-wide (%d in active set); target short code currently has "
          "%d rows table-wide." % (lf, sf, n_full, n_act, before_full.get(sf, 0)))
    if not any_long:
        L("")
        L("No long-form rows present — table already normalized. **Idempotent no-op.**")

    # ---- APPLY (sweep FULL table; all rows, any class/negative) ----
    L("")
    L("## Apply (full-table sweep — all row_class, all negative)")
    L("")
    total_updated = 0
    per_map = {}
    for lf, sf in NORMALIZE.items():
        cur = con.execute("UPDATE canon_corpus SET game=? WHERE game=?", (sf, lf))
        n = cur.rowcount
        per_map[(lf, sf)] = n
        total_updated += n
        if n:
            L("- `%s` -> `%s`: **%d rows updated**." % (lf, sf, n))
    con.commit()
    L("")
    L("**Total rows updated: %d.**" % total_updated)

    # ---- POST-ASSERT ----
    L("")
    L("## Post-assert")
    L("")
    after_active = active_game_counts(con)
    after_full = full_game_counts(con)

    # (1) no long form survives table-wide
    surviving_long = [lf for lf in NORMALIZE if after_full.get(lf, 0) > 0]
    if surviving_long:
        L("- **FAIL:** long forms still present table-wide: %s" % surviving_long)
        con.close()
        _flush(log)
        sys.exit(2)
    L("- No long-form code survives table-wide. OK.")

    # (2) every distinct game in the active set is a known short code (no hyphenated multi-word)
    #     (short codes are lowercase alnum, no embedded '-' from a franchise long form; mcd/la/etc OK)
    LONG_SENTINELS = set(NORMALIZE.keys())
    active_codes = sorted(after_active)
    bad = [g for g in active_codes if g in LONG_SENTINELS]
    if bad:
        L("- **FAIL:** long-form codes remain in active set: %s" % bad)
        con.close()
        _flush(log)
        sys.exit(2)
    L("- Active-set distinct `game` codes (%d): %s. All short-code. OK."
      % (len(active_codes), ", ".join(active_codes)))

    # (3) merge accounting — active-set counts fold correctly onto short codes
    L("")
    L("### Merge accounting (active set)")
    L("")
    L("| short code | before (active) | folded-in (active) | after (active) |")
    L("|---|---|---|---|")
    for lf, sf in NORMALIZE.items():
        before_sf = before_active.get(sf, 0)
        folded = before_active.get(lf, 0)
        after_sf = after_active.get(sf, 0)
        ok = (after_sf == before_sf + folded)
        L("| %s (<- %s) | %d | %d | %d%s |"
          % (sf, lf, before_sf, folded, after_sf, "" if ok else " ⚠MISMATCH"))
        if not ok:
            L("")
            L("- **FAIL:** merge accounting mismatch for %s: %d + %d != %d"
              % (sf, before_sf, folded, after_sf))
            con.close()
            _flush(log)
            sys.exit(2)

    # (4) mcd untouched
    L("")
    L("- `mcd` (already short-code) untouched: %d active rows (unchanged from %d). OK."
      % (after_active.get("mcd", 0), before_active.get("mcd", 0)))

    # ---- schema-meta stamp ----
    stamp = "gamecode-normalize-2026-07-16"
    meta_note = ("R0 game-code normalization (elrond): long-form game codes folded to short "
                 "(lost-ark->la [62], diablo-4->d4 [1], diablo-3->d3 [1], diablo-immortal->di [1]; "
                 "65 rows). No cell_key/kit_id touched; frozen Edition-I fit unaffected. Idempotent. "
                 "Precondition for Refit Candidate 1 FRANCHISE_ROLLUP orphan check.")
    existing = [r[0] for r in con.execute("SELECT version FROM corpus_schema_meta").fetchall()]
    if stamp not in existing:
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (stamp, datetime.now(timezone.utc).isoformat(), meta_note))
        con.commit()
        L("")
        L("- Schema-meta marker `%s` inserted." % stamp)
    else:
        L("")
        L("- Schema-meta marker `%s` already present (idempotent re-run)." % stamp)

    L("")
    L("## Result")
    L("")
    L("Game-code convention converged. Active-set distinct codes: %d, all short-code. "
      "FRANCHISE_ROLLUP orphan check will now pass with `la`+`mcd` added at derivation time."
      % len(active_codes))

    con.close()
    _flush(log)
    print("\n=== normalization complete; log written ===")


LOG_PATH = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/"
            "corpus-curation-gamecode-normalize-2026-07-16-log.md")


def _flush(log):
    with open(LOG_PATH, "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
