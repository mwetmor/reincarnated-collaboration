#!/usr/bin/env python3
"""
VDM-1 schema landing zone + Stage-0 ingestion fix.
Owner: elrond (single-writer of corpus.db).
Charter: agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md
MIGRATION doc: agentic_orchestration/research/curated/MIGRATION-vdm1-schema-2026-07-18.md

Discipline #8 (schema at boundaries): builds the six VDM-1 tables + provenance
separation BEFORE any crawl payload arrives.

LAWS enforced here:
  - fail-loud, single transaction, ROLLBACK on any assert mismatch
  - row counts conserved on ALL pre-existing tables
  - md5 of canon_corpus content-dump over the 65 ORIGINAL columns UNCHANGED
    (proves core_skills is purely additive; no existing value mutated)
  - no invented rows: JSONL ids with no canon_corpus row are LOGGED as orphans,
    never inserted (legolas reconciles census in parallel)
  - no fabrication: fact_provenance is a classification of EXISTING evidence,
    not a new claim
Backup (taken by caller BEFORE this runs): corpus.db.pre-vdm1-schema-2026-07-18-backup
"""
import sqlite3, hashlib, json, sys, os, glob

DB   = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
JROOT= "/Users/admin/Games/reincarnated-collaboration/claude-mobile-session-docs/ARPG-canonical-kit-research"

# ---- pre-migration invariants (captured read-only before this run) ----
PRE_CONTENT_MD5 = "ae67fe2e255467d5daf0dc43c2ac1eb2"   # canon_corpus, 65 cols, ORDER BY kit_id
# original 65 columns (BEFORE core_skills is added) — the md5 is computed over exactly these
ORIG_COLS = ["kit_id","folk_name","game","corpus_bucket","tier","tier_confirm_pending","canon_tier","eras","negative","lineage","gx","source","is_system","unresolved","mint","dossier_owed","atlas_key_orig","key_completeness","provenance_tag","source_date","lattice_coord","attr_val","attr_conf","range_val","range_conf","tempo_val","tempo_conf","amp_val","amp_conf","proxy_val","proxy_conf","commit_val","commit_conf","prefix_conf_provenance","avg_conf","mob_raw","geo_raw","ctrl_raw","def_raw","econ_raw","elem_raw","ctrl_def_from_code","suffix_rekey_status","motion_frame","t4_doors","option_c_substrate_flags","commit_provenance","mobile_cell_id","mobile_key_group","mobile_rank_in_cell","mobile_representative","mobile_mechanics_status","mobile_blocking_mechanics","mech_note","flags","prov","era_year","stabilization_patch","skill_debut_year","source_urls","death_class","architecture","pull_pending_vocab","grain","grain_note"]

# tables whose row counts MUST be conserved (every table that exists pre-run)
CONSERVE = ["atlas_feasibility_cuts_2026_07_14","atlas_feasibility_cuts_v1_2_2026_07_15",
    "atlas_feasibility_ladder_2026_07_14","atlas_feasibility_ladder_v1_2_2026_07_15",
    "atlas_feasibility_ladder_v1_3_2026_07_15","atlas_franchise_rollup",
    "atlas_franchise_rollup_refit_candidate_1","atlas_gateA_labels_2026_07_14",
    "atlas_gateA_labels_refit_candidate_1","canon_corpus","canon_engine_key",
    "canon_probe_facts","roster_atlas","roster_lineage_enrichment"]
# corpus_schema_meta is intentionally EXCLUDED (we add exactly one row to it)

def content_md5(con):
    sel = ",".join(f'"{c}"' for c in ORIG_COLS)
    rows = con.execute(f"SELECT {sel} FROM canon_corpus ORDER BY kit_id").fetchall()
    h = hashlib.md5()
    for row in rows:
        h.update(("\x1f".join("" if v is None else str(v) for v in row) + "\x1e").encode("utf-8"))
    return h.hexdigest()

def counts(con):
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in CONSERVE}

# provenance-artifact bookkeeping tokens (NOT sources — strip before classifying)
ARTIFACT = ("rdr-kit-atlas","rdr-kit","csv provenance","rdr-roster")
def classify_sources(arr):
    """kb-legacy if every substantive token is a memory projection (kb*/od*), else named-source-unfetched."""
    substantive = [t for t in arr if not any(a in t.lower() for a in ARTIFACT)]
    if not substantive:
        return "kb-legacy"          # only bookkeeping present -> no named external source
    if all(t.strip().lower().startswith(("kb","od")) for t in substantive):
        return "kb-legacy"
    return "named-source-unfetched"

DDL = r"""
-- ============================ VDM-1 SCHEMA LANDING ZONE ============================
CREATE TABLE IF NOT EXISTS kit_dossier (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id                TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    family                TEXT NOT NULL CHECK (family IN
                            ('skill_loop','skill_geometry','item_alterations',
                             'capstone_alterations','author_credit','variants')),
    payload_json          TEXT,          -- NULL when abstained=1 (source silent)
    source_url            TEXT,
    anchor_quote          TEXT,          -- verbatim from the fetched page
    abstained             INTEGER NOT NULL DEFAULT 0,   -- 1 = source silent, payload NULL (no-fabrication law)
    conf                  REAL,
    extraction_provenance TEXT NOT NULL DEFAULT 'fetched-vdm1',
    created_date          TEXT NOT NULL DEFAULT (date('now')),
    CHECK (abstained IN (0,1)),
    CHECK (abstained = 0 OR payload_json IS NULL),   -- abstain => empty payload
    UNIQUE (kit_id, family, source_url)
);
CREATE INDEX IF NOT EXISTS idx_kd_kit    ON kit_dossier(kit_id);
CREATE INDEX IF NOT EXISTS idx_kd_family ON kit_dossier(family);
CREATE INDEX IF NOT EXISTS idx_kd_abst   ON kit_dossier(abstained);

CREATE TABLE IF NOT EXISTS kit_citations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id        TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    url           TEXT NOT NULL,
    archive_url   TEXT,          -- Wayback snapshot
    site          TEXT,
    author_handle TEXT,
    title         TEXT,
    cite_class    TEXT CHECK (cite_class IN ('authored','communal','official','dataset')),
    rank_class    TEXT CHECK (rank_class IN ('recovered','attested-era')),
    accessed_date TEXT,
    quarantined   INTEGER NOT NULL DEFAULT 0,   -- junk-tail domains: recorded, never citable
    CHECK (quarantined IN (0,1)),
    UNIQUE (kit_id, url)
);
CREATE INDEX IF NOT EXISTS idx_kc_kit   ON kit_citations(kit_id);
CREATE INDEX IF NOT EXISTS idx_kc_class ON kit_citations(cite_class);
CREATE INDEX IF NOT EXISTS idx_kc_quar  ON kit_citations(quarantined);

CREATE TABLE IF NOT EXISTS verify_ledger (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id         TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    claim_family   TEXT NOT NULL CHECK (claim_family IN
                     ('identity','mechanics','era','negative_canon')),
    claim_text     TEXT,
    verdict        TEXT NOT NULL CHECK (verdict IN
                     ('CONFIRMED','CONTRADICTED','UNSUPPORTED','SOURCE_NOT_FOUND')),
    anchor_quote   TEXT,          -- verbatim audit anchor; mandatory for CONFIRMED/CONTRADICTED (enforced in-app)
    source_url     TEXT,
    errata_applied INTEGER NOT NULL DEFAULT 0,
    run_tag        TEXT NOT NULL DEFAULT 'vdm1',
    verified_date  TEXT NOT NULL DEFAULT (date('now')),
    CHECK (errata_applied IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_vl_kit     ON verify_ledger(kit_id);
CREATE INDEX IF NOT EXISTS idx_vl_verdict ON verify_ledger(verdict);
CREATE INDEX IF NOT EXISTS idx_vl_family  ON verify_ledger(claim_family);

CREATE TABLE IF NOT EXISTS kit_mapping (
    kit_id              TEXT PRIMARY KEY REFERENCES canon_corpus(kit_id),
    mapping_json        TEXT,          -- motion_frame / t4_doors / option_c_substrate_flags / skill+element+scaffold coords
    grade               TEXT CHECK (grade IN ('EXACT','CLOSE','APPROX','GAPPED')),
    deviation_notes     TEXT,
    terminal_state      TEXT CHECK (terminal_state IN ('MAPPED','MAPPED_DOCKET')),
    mapping_provenance  TEXT NOT NULL DEFAULT 'authored-vdm1',
    authored_date       TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_km_grade    ON kit_mapping(grade);
CREATE INDEX IF NOT EXISTS idx_km_terminal ON kit_mapping(terminal_state);

CREATE TABLE IF NOT EXISTS mint_ledger (
    mint_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    mint_class        TEXT NOT NULL CHECK (mint_class IN ('quantitative','qualitative')),
    description       TEXT,
    forced_by_kits    TEXT,          -- JSON array of kit_ids that forced the mint
    ladder_step_audit TEXT,          -- which of the 4 parsimony-ladder steps were tried first
    created_date      TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_ml_class ON mint_ledger(mint_class);

CREATE TABLE IF NOT EXISTS mechanic_gap_docket (
    docket_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    mechanism_class  TEXT,
    spec_text_or_path TEXT,
    evidence_kits    TEXT,          -- JSON array of kit_ids
    destination      TEXT,          -- e.g. 'GX-02' for shapeshift
    status           TEXT NOT NULL DEFAULT 'open',
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_mgd_dest   ON mechanic_gap_docket(destination);
CREATE INDEX IF NOT EXISTS idx_mgd_status ON mechanic_gap_docket(status);
"""

def main():
    if not os.path.exists(DB):
        sys.exit(f"FATAL: {DB} missing")
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    report = {}
    try:
        # -------- PRE asserts --------
        pre_counts = counts(con)
        pre_md5 = content_md5(con)
        assert pre_md5 == PRE_CONTENT_MD5, f"PRE md5 mismatch: {pre_md5} != {PRE_CONTENT_MD5}"
        existing = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for t in ("kit_dossier","kit_citations","verify_ledger","kit_mapping","mint_ledger","mechanic_gap_docket"):
            assert t not in existing, f"table {t} already exists — refusing to clobber"
        cc_cols = {r[1] for r in con.execute("PRAGMA table_info(canon_corpus)")}
        assert "core_skills" not in cc_cols, "core_skills already present"
        cpf_cols = {r[1] for r in con.execute("PRAGMA table_info(canon_probe_facts)")}
        assert "fact_provenance" not in cpf_cols, "fact_provenance already present"

        con.execute("BEGIN")

        # ============ DELIVERABLE 1: six tables ============
        con.executescript(DDL)

        # ============ DELIVERABLE 2: fact_provenance on canon_probe_facts ============
        con.execute("ALTER TABLE canon_probe_facts ADD COLUMN fact_provenance TEXT "
                    "CHECK (fact_provenance IN ('kb-legacy','named-source-unfetched','verified-v1.1','fetched-vdm1'))")
        # classify each kit by its sources_used family, then stamp ALL of that kit's rows
        kit_class = {}
        for kit_id, fj in con.execute("SELECT kit_id, facts_json FROM canon_probe_facts WHERE family='sources_used'"):
            try:    arr = json.loads(fj)
            except Exception: arr = []
            kit_class[kit_id] = classify_sources(arr)
        n_kb = n_named = n_orphan_family = 0
        for kit_id in {r[0] for r in con.execute("SELECT DISTINCT kit_id FROM canon_probe_facts")}:
            cls = kit_class.get(kit_id)
            if cls is None:
                # a kit with probe rows but no sources_used family (should not happen; guard anyway)
                cls = "kb-legacy"; n_orphan_family += 1
            con.execute("UPDATE canon_probe_facts SET fact_provenance=? WHERE kit_id=?", (cls, kit_id))
        n_kb    = con.execute("SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='kb-legacy'").fetchone()[0]
        n_named = con.execute("SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='named-source-unfetched'").fetchone()[0]
        report["fact_provenance"] = {"kb_legacy_rows": n_kb, "named_source_unfetched_rows": n_named,
            "kits_kb": sum(1 for v in kit_class.values() if v=="kb-legacy"),
            "kits_named": sum(1 for v in kit_class.values() if v=="named-source-unfetched"),
            "orphan_family_guard": n_orphan_family}

        # ============ DELIVERABLE 3: core_skills on canon_corpus + JSONL ingest ============
        con.execute("ALTER TABLE canon_corpus ADD COLUMN core_skills TEXT")            # JSON array text
        con.execute("ALTER TABLE canon_corpus ADD COLUMN core_skills_prov TEXT")       # provenance tag per-row
        db_ids = {r[0] for r in con.execute("SELECT kit_id FROM canon_corpus")}
        # gather core_skills from every per-game JSONL (skip roster files which lack the field)
        jfiles = sorted(glob.glob(os.path.join(JROOT, "**", "canon-corpus-*.jsonl"), recursive=True))
        seen = {}           # id -> core_skills (last wins; final-docs-v3 sorts after per-game dirs? we prefer per-game then final-docs override)
        parse_err = 0
        for jf in jfiles:
            with open(jf, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line: continue
                    try:    rec = json.loads(line)
                    except Exception: parse_err += 1; continue
                    kid = rec.get("id"); cs = rec.get("core_skills")
                    if not kid or cs is None: continue
                    if isinstance(cs, str): cs = [cs]
                    # normalize: list of non-empty trimmed strings
                    cs = [s.strip() for s in cs if isinstance(s,str) and s.strip()]
                    seen[kid] = cs
        applied = 0; orphans = []
        for kid, cs in seen.items():
            if kid in db_ids:
                con.execute("UPDATE canon_corpus SET core_skills=?, core_skills_prov=? WHERE kit_id=?",
                            (json.dumps(cs, ensure_ascii=False), "jsonl-stage0-backfill-2026-07-18", kid))
                applied += 1
            else:
                orphans.append(kid)
        # DB rows with no JSONL core_skills at all (the other drift direction) — informational
        db_no_jsonl = sorted(db_ids - set(seen.keys()))
        report["core_skills"] = {"jsonl_files": len(jfiles), "jsonl_ids_with_core_skills": len(seen),
            "applied": applied, "orphan_ids_no_db_row": sorted(orphans), "orphan_count": len(orphans),
            "db_rows_no_jsonl_core_skills": len(db_no_jsonl), "parse_errors": parse_err}

        # ============ schema-meta ledger row ============
        con.execute("INSERT INTO corpus_schema_meta VALUES (?,?,?)", (
            "vdm1-schema-2026-07-18", "2026-07-18T00:00:00Z",
            ("VDM-1 schema landing zone (elrond, Discipline #8 — schema at boundaries, pre-crawl). "
             "+6 tables: kit_dossier, kit_citations, verify_ledger, kit_mapping, mint_ledger, mechanic_gap_docket "
             "(gandalf charter §3 four-output-streams shapes; no-fabrication CHECKs: dossier abstain=>payload NULL). "
             "+canon_probe_facts.fact_provenance {kb-legacy|named-source-unfetched|verified-v1.1|fetched-vdm1}; "
             f"backfill by sources_used family: kb-legacy={n_kb} rows, named-source-unfetched={n_named} rows "
             "(verified-v1.1/fetched-vdm1 reserved for in-run crawl landings). "
             f"+canon_corpus.core_skills(+_prov) Stage-0 fix: {applied} ingested from mobile JSONLs "
             f"(prov jsonl-stage0-backfill-2026-07-18), {len(orphans)} JSONL orphans LOGGED not invented "
             "(legolas reconciling census). ADDITIVE ONLY; 65-col content-md5 unchanged; all pre-existing "
             "row counts conserved. Backup: corpus.db.pre-vdm1-schema-2026-07-18-backup.")))

        # -------- POST asserts --------
        post_counts = counts(con)
        for t in CONSERVE:
            assert post_counts[t] == pre_counts[t], f"ROW COUNT DRIFT on {t}: {pre_counts[t]} -> {post_counts[t]}"
        post_md5 = content_md5(con)   # over the ORIGINAL 65 cols only
        assert post_md5 == pre_md5, f"CONTENT MUTATED: {post_md5} != {pre_md5}"
        # every new table present
        now_tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for t in ("kit_dossier","kit_citations","verify_ledger","kit_mapping","mint_ledger","mechanic_gap_docket"):
            assert t in now_tables, f"missing new table {t}"
        # fact_provenance fully populated (no NULLs across 4780)
        nulls = con.execute("SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance IS NULL").fetchone()[0]
        assert nulls == 0, f"{nulls} canon_probe_facts rows left NULL fact_provenance"
        # schema-meta grew by exactly 1
        assert con.execute("SELECT COUNT(*) FROM corpus_schema_meta").fetchone()[0] == 17, "schema_meta not +1"

        con.commit()
        report["asserts"] = {"pre_md5": pre_md5, "post_md5": post_md5, "md5_conserved": post_md5==pre_md5,
            "row_counts_conserved": True, "fact_provenance_nulls": nulls,
            "canon_probe_facts_total": post_counts["canon_probe_facts"],
            "schema_meta_rows": 17}
        print(json.dumps(report, indent=2))
        print("\nOK: VDM-1 schema landing committed.")
    except Exception as e:
        con.rollback()
        print(json.dumps(report, indent=2))
        sys.exit(f"ROLLED BACK — {type(e).__name__}: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    main()
