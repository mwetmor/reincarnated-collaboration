#!/usr/bin/env python3
"""
gd_deviation_reverify_2026_07_25.py — re-verification of the six GD `engine_inexpressible`
deviation rows against post-Wave-D engine surfaces.

TRIGGER: gandalf's GD surface-fit mapping §1.2 row 68 / §2.3 — "`kit_deviation` still marks
`gd-retaliation-warlord` `engine_inexpressible` (docket 153). Wave-C's §6.3 TH roster names that
exact kit. The docket is stale; the gap closed. Route to elrond for a deviation re-classify."
Plus §  "there is no reason to believe 153 is the only one" — so all six are re-verified.

DESIGN OF THE CORRECTION — why a resolution LAYER, not a class mutation.
`kit_deviation.deviation_class` records what was true WHEN THE ROW WAS AUTHORED (2026-07-22, VDM-2
W4). Overwriting it would destroy the authored claim and make the corpus unable to answer "what did
we believe then, and what changed?" — the exact question a stale-docket incident should leave
answerable. So this migration is ADDITIVE: three new nullable columns carry the CURRENT truth
alongside the authored one. NULL = not re-verified.

AUTHORITY BOUNDARY. Establishing whether an engine surface EXISTS is evidentiary (elrond's domain);
deciding whether an existing-but-partial surface still counts as a deviation is a DESIGN call
(gandalf's). Rows where the evidence is unambiguous are resolved here; rows where it is partial are
marked `class-under-review` and routed, NOT silently flipped.

USAGE: python3 gd_deviation_reverify_2026_07_25.py [--dry-run]
"""
import sys, sqlite3, pathlib, hashlib, shutil, datetime

DB = pathlib.Path(__file__).resolve().parent.parent / "curated" / "corpus.db"
SCHEMA_VERSION = "gd-deviation-reverify-2026-07-25"
TODAY = "2026-07-25"

E_RETAL = (
    "VERIFIED IN ENGINE SOURCE 2026-07-25 (read-only). generation: "
    "src/reincarnated/generation/resource_economy.py:185 sub-shape 'stack-fill' whose comment reads "
    "'D2 rage-on-damage / GD retaliation stack builder'; :87-88 reflect_damage_fraction (0.0..1.00 "
    "LOCKED) + reflect_scaling_stat. simulation: src/reincarnated/simulation/damage_resolver.py:502 "
    "'Apply Wave-C TH damage-taken-converts reflect'. bin lift: "
    "generation/bc_target_composer.py:364 'damage-taken-converts -> LIFTED (Wave-C; the 3 TH "
    "thorns-reflect kits)'. Design owner's verdict: gandalf gd-surface-fit-mapping §1.2 row 68 = FIT. "
    "The surface is BUILT on both seams; the authored gap is closed.")

E_WERE = (
    "CAUSE VOID 2026-07-25. The row's stated cause was 'the source content does not yet exist -- "
    "Fangs of Asterkarn is unshipped'. That is now false: GDX3.arz (depot 2699230, manifest "
    "1575323658468418166, sha256 1661be5e...dcf0) is banked at "
    "/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/ and byte-verified this run. It holds "
    "24,178 records including 333 wereform/berserker records (records/fx/skillclass10/werewolf_*, "
    "wereraven_*) and a playerclass10 skill lane (40 records) -- the new mastery. "
    "The deviation is NOT thereby resolved: no dossier has been built against the now-held source. "
    "DISPOSITION: re-crawl required (legolas Mode B against gdx3), then re-derive the row.")

E_PET = (
    "PARTIAL SURFACE VERIFIED 2026-07-25 (read-only). BUILT: delivery=SUMMON "
    "(generation/summon_economy.py:215,261); one-summon-one-decl bridge "
    "(generation/proxy_vocabulary_bridge.py:243 proxy_decl_from_summon); proxy bins LIFTED -- "
    "generation/bc_target_composer.py:113 _DEFERRED_PROXY_BINS = frozenset() (Wave-A drain), :360 "
    "'proxy-light / proxy-heavy -> LIFTED'. NOT BUILT: proxy P2 nav/command (autonomous behaviour "
    "grammar), which is a named OPEN Matt thread, not a GD-program item (gandalf "
    "gd-surface-fit-mapping §3: 'the census's five engine_inexpressible pet kits resolve there, not "
    "here'). So 'engine_inexpressible' (= no native expression at all) is now too strong: hosting "
    "and emission exist; autonomy does not. Whether the residual is engine_inexpressible or "
    "param_gap is a DESIGN call -- routed to gandalf, deliberately NOT decided here.")

ROWS = {
    818: ("gd-retaliation-warlord",  "surface-built-gap-closed",              E_RETAL),
    797: ("gd-berserker-wereforms",  "cause-void-recrawl-required",           E_WERE),
    799: ("gd-blight-fiend-ritualist", "partial-surface-class-under-review",  E_PET),
    815: ("gd-pet-conjurer",         "partial-surface-class-under-review",    E_PET),
    817: ("gd-reap-spirit",          "partial-surface-class-under-review",    E_PET),
    821: ("gd-skeleton-ritualist",   "partial-surface-class-under-review",    E_PET),
}
DOCKETS = {
    153: ("closed", "surface-built-verified-2026-07-25 (generation resource_economy stack-fill + "
                    "reflect_*; simulation damage_resolver TH reflect; bin LIFTED Wave-C)"),
    149: ("open",   "cause-void-2026-07-25: gdx3 source now held+verified; legolas re-crawl required "
                    "before the row can be re-derived"),
    150: ("open",   "partial-surface-2026-07-25: SUMMON+proxy hosting BUILT, proxy-P2 nav/command "
                    "SPEC-ONLY; routed to the pets-P2 open thread, class under gandalf review"),
    151: ("open",   "partial-surface-2026-07-25: SUMMON+proxy hosting BUILT, proxy-P2 nav/command "
                    "SPEC-ONLY; routed to the pets-P2 open thread, class under gandalf review"),
    152: ("open",   "partial-surface-2026-07-25: SUMMON+proxy hosting BUILT, proxy-P2 nav/command "
                    "SPEC-ONLY; routed to the pets-P2 open thread, class under gandalf review"),
    154: ("open",   "partial-surface-2026-07-25: SUMMON+proxy hosting BUILT, proxy-P2 nav/command "
                    "SPEC-ONLY; routed to the pets-P2 open thread, class under gandalf review"),
}


def main():
    dry = "--dry-run" in sys.argv
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # pre-flight: the rows must be exactly what we think they are
    bad = []
    for did, (kit, _, _) in ROWS.items():
        r = cur.execute("SELECT kit_id, deviation_class, docket_id FROM kit_deviation "
                        "WHERE deviation_id=?", (did,)).fetchone()
        if not r or r[0] != kit or r[1] != "engine_inexpressible":
            bad.append((did, r))
    if bad:
        raise SystemExit(f"HALT — deviation rows are not as expected: {bad}")
    print(f"pre-flight OK: 6 GD engine_inexpressible rows confirmed")
    if dry:
        for did, (kit, st, _) in ROWS.items():
            print(f"  WOULD SET {did} {kit:28s} -> {st}")
        for dk, (stat, disp) in DOCKETS.items():
            print(f"  WOULD SET docket {dk} status={stat} disposition={disp[:60]}…")
        return

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bak = DB.with_name(DB.name + f".pre-devreverify-{ts}-backup")
    shutil.copy2(DB, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    bak.with_suffix(bak.suffix + ".md5.txt").write_text(f"{md5}  {bak.name}\n")
    print(f"BACKUP {bak.name}  md5={md5}")

    cols = {c[1] for c in cur.execute("PRAGMA table_info(kit_deviation)")}
    for c, t in (("resolution_status", "TEXT"), ("resolution_evidence", "TEXT"),
                 ("resolution_date", "TEXT")):
        if c not in cols:
            cur.execute(f"ALTER TABLE kit_deviation ADD COLUMN {c} {t}")
            print(f"  + kit_deviation.{c}")

    for did, (kit, status, ev) in ROWS.items():
        cur.execute("UPDATE kit_deviation SET resolution_status=?, resolution_evidence=?, "
                    "resolution_date=? WHERE deviation_id=?", (status, ev, TODAY, did))
    for dk, (stat, disp) in DOCKETS.items():
        cur.execute("UPDATE mechanic_gap_docket SET status=?, disposition=? WHERE docket_id=?",
                    (stat, disp, dk))
    cur.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                (SCHEMA_VERSION,
                 datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "GD engine_inexpressible re-verification (elrond). ADDITIVE: kit_deviation gains "
                 "resolution_status/_evidence/_date; 6 GD rows annotated; dockets 149-154 given "
                 "dispositions; docket 153 CLOSED. deviation_class values UNCHANGED by design — "
                 "the authored claim is history, the resolution columns are current truth."))
    con.commit()

    print("\nRESULT")
    for r in cur.execute("""
        SELECT d.deviation_id, d.kit_id, d.deviation_class, d.resolution_status,
               g.docket_id, g.status
        FROM kit_deviation d LEFT JOIN mechanic_gap_docket g ON g.docket_id=d.docket_id
        WHERE d.resolution_status IS NOT NULL ORDER BY d.deviation_id"""):
        print(f"  {r[0]} {r[1]:28s} class={r[2]:22s} resolution={r[3]:36s} docket={r[4]}/{r[5]}")
    print(f"\n  integrity_check: {cur.execute('PRAGMA integrity_check').fetchone()[0]}")
    con.close()


if __name__ == "__main__":
    main()
