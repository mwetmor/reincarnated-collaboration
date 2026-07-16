#!/usr/bin/env python3
"""
corpus_dual_hard_delete_2026_07_16.py  —  elrond data-steward tool script

IMMEDIATE dual hard-delete of all 182 spec-orphaned rows from corpus.db per
Matt wave-2/wave-3 rulings 2026-07-16 (the catalogue never-purge philosophy's
Matt's-word carve-out, EXERCISED — a real DELETE, not an inert grain flag).

Delete set (asserted EXACT before delete; HALT on mismatch):
  - 62 Lost Ark  (game='la') : 56 grain='class' + 6 grain='kit' (Destroyer)
  - 120 Minecraft Dungeons (game='mcd') : 120 grain='gear' (94 keyed + 26 no-key)
  + 156 cascade children in canon_engine_key (FK enforcement is OFF; deleted
    explicitly to honor the never-orphan discipline).

Fail-loud contract:
  - PRE  asserts: 62/120 counts, zero E1-469 membership, provenance archivable.
  - POST asserts: grain census kit=509/NULL=18/gear=0/class=0/total=527,
    canon_engine_key 1:1 with canon_corpus (527, zero orphans),
    zero la/mcd remaining, served+evidence artifacts byte-identical (sha256).
  - Any mismatch -> raise (transaction rolled back; nothing deleted/committed).

Reproducible + reversible from ../curated/corpus.db.pre-dual-hard-delete-2026-07-16-backup.
This is a tool script (curation), NOT engine code; not consumed by the engine.
"""
import hashlib
import pathlib
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
CURATED = HERE.parent / "curated"
DB = CURATED / "corpus.db"
ATLAS = CURATED / "atlas"
E1_CELLKEYS = ATLAS / "atlas-frozen-fit-cellkeys-edition1.csv"

# Served + evidence artifacts that MUST remain byte-identical (baseline sha256
# captured pre-delete; re-verified post-delete).
READONLY_ARTIFACTS = {
    "atlas-edition3.json":
        "38c3bc00f20b7782eaab77735769531af286c3bb632cd95f367b41811b8fd435",
    "atlas-refit-candidate-1.json":
        "758126a8bc55f7eef6254066d4426d2ecb03c9fad1786754d0a42d27eaa9cf09",
    "atlas-archipelago-mock.json":
        "141153bf850f76a5d19d333a70b363f0c5465501d645938f917cb4128de7a8c2",
    "atlas-frozen-fit-cellkeys-edition1.csv":
        "e79042441283635c252310c6990513a58b0562dc04e7222a9d3345a2c5b0a92d",
}

DELETE_GAMES = ("la", "mcd")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def die(msg: str) -> None:
    raise SystemExit(f"HALT (fail-loud): {msg}")


def load_e1_members() -> set[str]:
    members: set[str] = set()
    with E1_CELLKEYS.open() as fh:
        next(fh)  # header: kit_id,cell_key
        for line in fh:
            line = line.strip()
            if line:
                members.add(line.split(",", 1)[0])
    return members


def main() -> None:
    if not DB.exists():
        die(f"corpus.db not found at {DB}")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=OFF;")  # match existing DB posture
    cur = con.cursor()

    # ---------- PRE asserts ----------
    la = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='la'").fetchone()[0]
    mcd = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='mcd'").fetchone()[0]
    if la != 62:
        die(f"LA delete-set count {la} != 62")
    if mcd != 120:
        die(f"mcd delete-set count {mcd} != 120")

    la_class = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='la' AND grain='class'"
    ).fetchone()[0]
    la_kit = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='la' AND grain='kit'"
    ).fetchone()[0]
    mcd_gear = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='mcd' AND grain='gear'"
    ).fetchone()[0]
    if (la_class, la_kit, mcd_gear) != (56, 6, 120):
        die(f"grain split (class,kit,gear)=({la_class},{la_kit},{mcd_gear}) "
            f"!= (56,6,120)")

    delete_ids = [
        r[0] for r in cur.execute(
            "SELECT kit_id FROM canon_corpus WHERE game IN (?,?)", DELETE_GAMES
        ).fetchall()
    ]
    if len(delete_ids) != 182:
        die(f"delete set size {len(delete_ids)} != 182")

    # zero E1-469 membership (the critical HALT condition)
    e1 = load_e1_members()
    if len(e1) != 469:
        die(f"E1 frozen-fit member count {len(e1)} != 469 "
            f"(file integrity?)")
    overlap = sorted(set(delete_ids) & e1)
    if overlap:
        die(f"{len(overlap)} E1-469 member(s) in delete set: {overlap[:10]}")

    # provenance archivable: every row has the columns we archived
    missing_prov = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus "
        "WHERE game IN (?,?) AND (source IS NULL OR provenance_tag IS NULL "
        "OR source_date IS NULL OR grain IS NULL)", DELETE_GAMES
    ).fetchone()[0]
    if missing_prov:
        die(f"{missing_prov} delete-set row(s) missing an archivable "
            f"provenance column")

    ek_children = cur.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id IN "
        "(SELECT kit_id FROM canon_corpus WHERE game IN (?,?))", DELETE_GAMES
    ).fetchone()[0]
    pf_children = cur.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE kit_id IN "
        "(SELECT kit_id FROM canon_corpus WHERE game IN (?,?))", DELETE_GAMES
    ).fetchone()[0]
    if ek_children != 156:
        die(f"canon_engine_key children {ek_children} != 156")
    if pf_children != 0:
        die(f"canon_probe_facts children {pf_children} != 0 (unexpected)")

    print(f"PRE ok: LA=62 (class56+kit6) mcd=120(gear) total=182 · "
          f"E1-overlap=0 · ek-children=156 · pf-children=0 · prov-archivable")

    # baseline sizes for post-delete arithmetic
    cc_before = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    ek_before = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]

    # ---------- DELETE (single transaction) ----------
    cur.execute("BEGIN")
    cur.execute(
        "DELETE FROM canon_engine_key WHERE kit_id IN "
        "(SELECT kit_id FROM canon_corpus WHERE game IN (?,?))", DELETE_GAMES)
    ek_deleted = cur.rowcount
    cur.execute("DELETE FROM canon_corpus WHERE game IN (?,?)", DELETE_GAMES)
    cc_deleted = cur.rowcount

    # ---------- POST asserts (still in txn; rollback on any failure) ----------
    def post_fail(msg: str) -> None:
        con.rollback()
        die(f"POST assert failed -> ROLLED BACK (no delete committed): {msg}")

    if cc_deleted != 182:
        post_fail(f"deleted {cc_deleted} canon_corpus rows != 182")
    if ek_deleted != 156:
        post_fail(f"deleted {ek_deleted} canon_engine_key rows != 156")

    census = dict(cur.execute(
        "SELECT COALESCE(grain,'NULL'), COUNT(*) FROM canon_corpus "
        "GROUP BY grain").fetchall())
    want = {"kit": 509, "NULL": 18}
    if census.get("kit") != 509 or census.get("NULL") != 18:
        post_fail(f"grain census {census} != kit509/NULL18")
    if census.get("gear", 0) != 0 or census.get("class", 0) != 0:
        post_fail(f"grain census {census} still has gear/class")

    cc_after = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    ek_after = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    if cc_after != 527:
        post_fail(f"canon_corpus total {cc_after} != 527")
    if ek_after != 527:
        post_fail(f"canon_engine_key total {ek_after} != 527 (expected 1:1)")

    remaining = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game IN (?,?)", DELETE_GAMES
    ).fetchone()[0]
    if remaining:
        post_fail(f"{remaining} la/mcd rows still present in canon_corpus")

    orphans = cur.execute(
        "SELECT COUNT(*) FROM canon_engine_key k WHERE NOT EXISTS "
        "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=k.kit_id)").fetchone()[0]
    if orphans:
        post_fail(f"{orphans} orphaned canon_engine_key rows after delete")

    # served + evidence artifacts byte-identical (sha256) — before COMMIT so a
    # tampered artifact rolls the delete back too.
    for name, want_hash in READONLY_ARTIFACTS.items():
        got = sha256(ATLAS / name)
        if got != want_hash:
            post_fail(f"read-only artifact {name} changed "
                      f"(sha256 {got[:12]} != {want_hash[:12]})")

    con.commit()
    con.close()

    print(f"DELETE committed: -{cc_deleted} canon_corpus / -{ek_deleted} "
          f"canon_engine_key")
    print(f"POST ok: census kit=509 NULL=18 gear=0 class=0 total=527 · "
          f"engine_key=527 (1:1, 0 orphans) · la/mcd=0 remaining · "
          f"4 read-only artifacts byte-identical")
    print(f"arithmetic: canon_corpus {cc_before}->{cc_after} · "
          f"canon_engine_key {ek_before}->{ek_after}")


if __name__ == "__main__":
    main()
