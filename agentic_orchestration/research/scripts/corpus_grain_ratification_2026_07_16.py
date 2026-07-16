#!/usr/bin/env python3
"""
GRAIN LAW ratification — Part A of the elrond charge 2026-07-16.

Adds a ratified `grain` column (kit | gear | class) to canon_corpus, derived
PER ROW FROM PROVENANCE (never assumed), implementing Matt's rulings 2026-07-16:
  (1) "Exclude the Minecraft Dungeons kits entirely."   -> mcd rows = gear grain
  (2) "On Lost Ark, yes we CANNOT emit full classes...   -> LA class-engraving = class grain
       I would recommend deleting these entirely            LA Destroyer skill-grain (la-destroyer-*) = kit grain
       rather than decomposing."                            (grain-based survival, not source-based)

THE GRAIN LAW: corpus grain = emission grain. The engine emits kits; the atlas
plots what the engine can emit. Every future fit-stage predicate MUST include
`grain = 'kit'`. Rows stay catalogued INERT (score/filter at consumption, never
purge) -- this is a column add + backfill ONLY, zero deletes.

Derivation rules (provenance-anchored, applied in order):
  mcd  (game='mcd', architecture='notable', 120 rows)          -> grain='gear'
  LA   (game='la') AND kit_id LIKE 'la-destroyer-%' (6 rows)   -> grain='kit'   [skill-grain]
  LA   (game='la') everything else (56 rows)                   -> grain='class' [class-engraving]
  system-record (row_class='system-record', 18 rows, no la/mcd)-> grain=NULL    [not kit/gear/class emittable;
                                                                   deterministic NULL, NOT ambiguous;
                                                                   grain_note records why]
  everything else (515 combat-kit rows)                        -> grain='kit'

FLAG (returned, not halted): the 2 Destroyer rows whose kit_id says skill-grain
(la-destroyer-*) but whose architecture column says 'class-engraving'
(la-destroyer-rage-hammer, la-destroyer-gravity-training). Matt's ruling is
explicit and authoritative that all 6 Destroyer rows are kit-grain; the kit_id
prefix reading yields exactly the ruled 6/56 split. These 2 rows carry
grain='kit' PER THE RULING, with grain_note recording the architecture conflict
so the source-vs-grain tension stays visible. Count = 2 (well under the HALT>20).

Idempotent: re-running re-derives and re-backfills to the same values. The
column is created IF NOT EXISTS; the grain_note column likewise.

Iron laws honored: no atlas artifact re-fit/re-emitted here; no served artifact
touched; corpus.db is the only mutation and it is additive (ALTER ADD COLUMN +
UPDATE), fully reversible (grain is re-derivable from provenance columns).

Run:  python3 corpus_grain_ratification_2026_07_16.py
"""
import os
import sqlite3
import sys

CUR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
DB = os.path.join(CUR, "corpus.db")

GRAIN_VOCAB = ("kit", "gear", "class")  # NULL is a legitimate 4th state for non-emittable system-records

# The 2 architecture-vs-kitid-prefix conflicted Destroyer rows (kept for the flag list).
DESTROYER_ARCH_CONFLICT = ("la-destroyer-rage-hammer", "la-destroyer-gravity-training")


def derive_grain(game, kit_id, row_class, architecture):
    """Provenance-anchored grain derivation. Returns (grain_or_None, note_or_None).
    Order matters: mcd and LA are decided by game+kit_id; system-records only fall
    through for non-mcd/non-la rows (asserted disjoint below)."""
    if game == "mcd":
        return "gear", None
    if game == "la":
        if kit_id.startswith("la-destroyer-"):
            # skill-grain Destroyer -> kit (Matt ruling: the 6 survive as kit-grain)
            if kit_id in DESTROYER_ARCH_CONFLICT:
                return "kit", ("FLAG: kit_id prefix says skill-grain (kit) but architecture="
                               "'class-engraving' says class; grain=kit set per Matt ruling "
                               "2026-07-16 (all 6 Destroyer rows are kit-grain citizens); "
                               "source-vs-grain tension recorded")
            return "kit", "Destroyer skill-grain (la-destroyer-*) -> kit per Matt ruling"
        # all other LA rows are class-engraving (a class + engraving identity = a full
        # class build the engine cannot emit) -> class
        return "class", None
    if row_class == "system-record":
        # not kit/gear/class emittable; deterministic NULL (documented), NOT ambiguous
        return None, "system-record: not kit/gear/class emittable; excluded from fits by row_class"
    return "kit", None


def main():
    if not os.path.exists(DB):
        sys.exit("FATAL: corpus.db not found at %s" % DB)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    # ---- add columns (idempotent) ---------------------------------------
    cols = {r[1] for r in con.execute("PRAGMA table_info(canon_corpus)").fetchall()}
    if "grain" not in cols:
        con.execute("ALTER TABLE canon_corpus ADD COLUMN grain TEXT")
        print("ALTER: added canon_corpus.grain (TEXT)")
    else:
        print("grain column already present -- re-deriving/backfilling")
    if "grain_note" not in cols:
        con.execute("ALTER TABLE canon_corpus ADD COLUMN grain_note TEXT")
        print("ALTER: added canon_corpus.grain_note (TEXT)")

    # ---- derive + backfill ----------------------------------------------
    rows = con.execute(
        "SELECT c.kit_id, c.game, c.architecture, k.row_class "
        "FROM canon_corpus c LEFT JOIN canon_engine_key k ON k.kit_id=c.kit_id"
    ).fetchall()

    census = {"kit": 0, "gear": 0, "class": 0, "NULL(system-record)": 0}
    flags = []
    null_system = []
    updates = []
    for r in rows:
        g, note = derive_grain(r["game"], r["kit_id"], r["row_class"], r["architecture"])
        updates.append((g, note, r["kit_id"]))
        if g is None:
            census["NULL(system-record)"] += 1
            null_system.append(r["kit_id"])
        else:
            census[g] += 1
        if note and note.startswith("FLAG"):
            flags.append((r["kit_id"], note))

    con.executemany("UPDATE canon_corpus SET grain=?, grain_note=? WHERE kit_id=?", updates)

    # ---- fail-loud asserts ----------------------------------------------
    total = sum(census.values())
    assert total == len(rows), "row count drift: %d census vs %d rows" % (total, len(rows))
    # vocab check: every non-null grain is in the ratified vocabulary
    bad_vocab = con.execute(
        "SELECT DISTINCT grain FROM canon_corpus WHERE grain IS NOT NULL AND grain NOT IN (?,?,?)",
        GRAIN_VOCAB,
    ).fetchall()
    assert not bad_vocab, "grain values outside vocabulary: %s" % [b[0] for b in bad_vocab]
    # ruling arithmetic: mcd->gear=120, LA class=56, LA destroyer kit=6
    assert census["gear"] == 120, "expected 120 gear (mcd), got %d" % census["gear"]
    assert census["class"] == 56, "expected 56 class (LA class-engraving), got %d" % census["class"]
    la_kit = con.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='la' AND grain='kit'"
    ).fetchone()[0]
    assert la_kit == 6, "expected 6 LA Destroyer kit-grain, got %d" % la_kit
    # every mcd row is gear; every mcd row keeps its cataloguing (no deletes)
    mcd_nongear = con.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='mcd' AND (grain IS NULL OR grain!='gear')"
    ).fetchone()[0]
    assert mcd_nongear == 0, "%d mcd rows not grain=gear" % mcd_nongear
    # system-records that are NOT la/mcd are the only NULLs
    null_nonsys = con.execute(
        "SELECT COUNT(*) FROM canon_corpus c LEFT JOIN canon_engine_key k ON k.kit_id=c.kit_id "
        "WHERE c.grain IS NULL AND NOT (k.row_class='system-record' AND c.game NOT IN ('mcd','la'))"
    ).fetchone()[0]
    assert null_nonsys == 0, "%d NULL-grain rows are not non-mcd/la system-records" % null_nonsys
    # flag count must be under HALT threshold
    assert len(flags) <= 20, "grain-ambiguous flags %d exceed HALT threshold 20" % len(flags)

    con.commit()

    # ---- report ---------------------------------------------------------
    print("\n" + "=" * 66)
    print("GRAIN CENSUS (canon_corpus, %d rows)" % len(rows))
    print("=" * 66)
    for k in ("kit", "gear", "class", "NULL(system-record)"):
        print("  %-22s %4d" % (k, census[k]))
    print("  %-22s %4d" % ("TOTAL", total))
    print("\nFLAG LIST (grain-ambiguous, resolved-per-ruling, %d rows):" % len(flags))
    for kid, note in flags:
        print("  %s\n    %s" % (kid, note))
    print("\nNULL-deterministic (system-records, %d rows, NOT ambiguous):" % len(null_system))
    print("  " + ", ".join(sorted(null_system)))
    # per-game grain crosstab for the record
    print("\nPER-GAME grain crosstab (non-default rows):")
    for row in con.execute(
        "SELECT game, COALESCE(grain,'(NULL)') g, COUNT(*) n FROM canon_corpus "
        "WHERE game IN ('mcd','la') GROUP BY game, g ORDER BY game, n DESC"
    ):
        print("  %-5s %-8s %d" % (row[0], row[1], row[2]))
    con.close()
    print("\nDONE. grain column ratified, backfilled, committed. Zero deletes.")


if __name__ == "__main__":
    main()
