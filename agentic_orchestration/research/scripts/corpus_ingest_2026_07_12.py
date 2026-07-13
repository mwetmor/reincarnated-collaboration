"""
corpus_ingest_2026_07_12.py
Canon-corpus DB staged ingest — three-layer schema per DELTA v2 + Q24 rulings.
Authority: 2026-07-12-elrond-corpus-ingest-brief.md (gandalf)
Matt authorization: Q24(a)/(b)/(c) 2026-07-12

WHAT THIS SCRIPT DOES:
  1. Creates agentic_orchestration/research/curated/corpus.db from DDL v2.0
  2. Layer 1: ingest 515 canon corpus rows (Q24(b): 48 roster/bench rows SKIPPED)
  3. Layer 2: ingest probe facts (478 positives × families; negatives Layer-1 only)
  4. Layer 3: ingest engine-key verbatim (478 rows)
  5. Roster: ingest roster_atlas (45) + roster_lineage_enrichment (45) with FK checks
  6. D4 reconciliation: CSV is_system vs engine-key system-record
  7. D6 acceptance harness: reproduce every Board count from SQL

LAWS:
  - NO rekey_elem / rekey_mob tables (element=free axis, mobility=emergent)
  - suffix_rekey_status: geo/ctrl/def/econ → 'keyed-v1'; mob/elem → 'descriptor-final'
  - ctrl.treatment: 'support' never legal (Q22)
  - HoT tier='T3', tier_confirm_pending=0 (Q24(c))
  - Negatives: Layer-1 only, no facts/key rows
  - Mint kits: mint=1, dossier_owed=1
"""

import csv
import json
import pathlib
import sqlite3
import sys

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
CSV_PATH = BASE / "claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv"
PROBE_DIR = BASE / "agentic_orchestration/legolas/research/megaprobe-2026-07-12"
ENGINE_KEY = BASE / "agentic_orchestration/gandalf/views/engine-key/corpus-engine-key-v1.jsonl"
ROSTER_CSV = BASE / "agentic_orchestration/gandalf/views/roster-atlas-rebuilt-v1.csv"
LINEAGE_ENRICH = PROBE_DIR / "roster-lineage-enrichment.jsonl"
MINT_DOSSIERS = PROBE_DIR / "mint-dossiers-reexpressed.jsonl"
DDL_PATH = BASE / "agentic_orchestration/research/scripts/catalogue_migrations/corpus_v2_0_three_layer.sql"
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
PROBE_FAMILIES = [
    "delivery", "footprint", "control", "defense", "economy",
    "element", "movement", "geo_text", "rank1_upgrade", "sources_used"
]

ATTR_MAP = {"D": "DEX", "S": "STR", "I": "INT", "W": "WIS", "_": None}
RANGE_MAP = {"R": "ranged", "M": "melee", "D": "dual", "_": None}
TEMPO_MAP = {"H": "high", "M": "med", "L": "low", "_": None}
AMP_MAP = {"F": "flat", "S": "spiky", "V": "var", "_": None}
PROXY_MAP = {"S": "solo", "L": "light", "H": "heavy", "_": None}
COMMIT_MAP = {"I": "instant", "W": "wind-up", "C": "channel", "_": None}


def decode_atlas_key(atlas_key):
    """Decode the 6-slot prefix from atlas_key (positions 0-5 of the pre-dash segment)."""
    if not atlas_key or len(atlas_key) < 6:
        return None, None, None, None, None, None
    seg = atlas_key.split("-")[0] if "-" in atlas_key else atlas_key
    if len(seg) < 6:
        return None, None, None, None, None, None
    attr_val = ATTR_MAP.get(seg[0].upper())
    range_val = RANGE_MAP.get(seg[1].upper())
    tempo_val = TEMPO_MAP.get(seg[2].upper())
    amp_val = AMP_MAP.get(seg[3].upper())
    proxy_val = PROXY_MAP.get(seg[4].upper())
    commit_val = COMMIT_MAP.get(seg[5].upper())
    return attr_val, range_val, tempo_val, amp_val, proxy_val, commit_val


def is_sys_row(row):
    """Detect SYS-annex rows from CSV: key_group starts with 'SYS' or flags contains 'SYS'."""
    kg = row.get("key_group", "")
    fl = row.get("flags", "")
    return kg.startswith("SYS") or "SYS" in fl


def parse_bool(val):
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, (int, float)):
        return 1 if val else 0
    if isinstance(val, str):
        return 1 if val.lower() in ("1", "true", "yes") else 0
    return 0


def safe_real(val):
    try:
        return float(val) if val not in (None, "", "None") else None
    except (ValueError, TypeError):
        return None


def safe_int(val):
    try:
        return int(val) if val not in (None, "", "None") else None
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Main ingest
# ---------------------------------------------------------------------------
def main():
    findings = []
    warnings = []

    # ---- 0. Load inputs ----
    print("Loading inputs...")
    csv_rows = list(csv.DictReader(open(CSV_PATH)))
    assert len(csv_rows) == 563, f"Expected 563 CSV rows, got {len(csv_rows)}"

    ek_rows = [json.loads(l) for l in open(ENGINE_KEY)]
    assert len(ek_rows) == 478, f"Expected 478 engine-key rows, got {len(ek_rows)}"
    ek_by_id = {r["kit_id"]: r for r in ek_rows}

    mint_rows = [json.loads(l) for l in open(MINT_DOSSIERS)]
    assert len(mint_rows) == 9, f"Expected 9 mint rows, got {len(mint_rows)}"
    mint_ids = {r["kit_id"] for r in mint_rows}

    roster_csv_rows = list(csv.DictReader(open(ROSTER_CSV)))
    assert len(roster_csv_rows) == 45, f"Expected 45 roster rows, got {len(roster_csv_rows)}"

    lineage_rows = [json.loads(l) for l in open(LINEAGE_ENRICH)]
    assert len(lineage_rows) == 45, f"Expected 45 lineage enrichment rows, got {len(lineage_rows)}"

    # Load all probe facts files
    probe_by_id = {}
    for fpath in sorted(PROBE_DIR.glob("*-facts.jsonl")):
        for line in open(fpath):
            row = json.loads(line)
            kit_id = row.get("kit_id")
            if kit_id:
                probe_by_id[kit_id] = row
    print(f"  Probe facts loaded: {len(probe_by_id)} kits")

    # ---- 1. Create DB ----
    print(f"Creating DB: {DB_PATH}")
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    ddl = DDL_PATH.read_text()
    conn.executescript(ddl)

    # Insert schema_meta
    conn.execute(
        "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        (
            "2.0",
            "2026-07-12T00:00:00Z",
            "Three-layer ingest: Layer1=canon_corpus(515), Layer2=probe_facts, "
            "Layer3=engine_key(478), roster_atlas(45), roster_lineage_enrichment(45). "
            "Q24(a)/(b)/(c) authorized. mob/elem=descriptor-final; geo/ctrl/def/econ=keyed-v1.",
        ),
    )

    # ---- 2. LAYER 1: ingest canon corpus ----
    # 515 from CSV (source=canon) + 9 mint kits from mint-dossiers (not in CSV)
    print("Layer 1: ingesting canon_corpus...")
    canon_rows = [r for r in csv_rows if r.get("source") == "canon"]
    assert len(canon_rows) == 515, f"Expected 515 canon rows, got {len(canon_rows)}"

    layer1_count = 0
    for r in canon_rows:
        kit_id = r["kit_id"]
        atlas_key = r.get("atlas_key", "")
        attr_v, range_v, tempo_v, amp_v, proxy_v, commit_v = decode_atlas_key(atlas_key)

        is_neg = parse_bool(r.get("negative", "0"))
        is_sys = 1 if is_sys_row(r) else 0
        kc = safe_int(r.get("key_completeness"))
        is_unres = 1 if (kc is not None and kc < 4) else 0
        is_mint = 1 if kit_id in mint_ids else 0
        dossier_owed_val = 1 if is_mint else 0

        # Q24(c): HoT tier confirmed T3, tier_confirm_pending=0
        tier = r.get("tier", "")
        if r.get("game") == "hot":
            tier = "T3"
            tier_conf_pend = 0
        else:
            tier_conf_pend = 0  # Q24(c) ruling clears all pending flags; hot was the only pending game

        # Lattice coord (6-char from atlas_key first segment)
        seg = atlas_key.split("-")[0] if atlas_key and "-" in atlas_key else (atlas_key[:6] if atlas_key else "")
        lattice_coord = seg[:6] if len(seg) >= 6 else None

        avg_conf = safe_real(r.get("avg_conf"))

        # suffix_rekey_status: mob/elem = 'descriptor-final'; geo/ctrl/def/econ = 'keyed-v1' if in EK else 'awaiting-rekey'
        if kit_id in ek_by_id:
            suffix_status = "keyed-v1"
        elif is_neg:
            suffix_status = "awaiting-rekey"
        else:
            suffix_status = "awaiting-rekey"

        conn.execute(
            """INSERT INTO canon_corpus (
                kit_id, folk_name, game, corpus_bucket, tier, tier_confirm_pending,
                canon_tier, eras, negative, lineage, gx,
                source, is_system, unresolved, mint, dossier_owed,
                atlas_key_orig, key_completeness, provenance_tag, source_date,
                lattice_coord,
                attr_val, attr_conf, range_val, range_conf,
                tempo_val, tempo_conf, amp_val, amp_conf,
                proxy_val, proxy_conf, commit_val, commit_conf,
                prefix_conf_provenance, avg_conf,
                mob_raw, geo_raw, ctrl_raw, def_raw, econ_raw, elem_raw,
                ctrl_def_from_code, suffix_rekey_status,
                mobile_cell_id, mobile_key_group, mobile_rank_in_cell,
                mobile_representative, mobile_mechanics_status,
                mobile_blocking_mechanics, mech_note, flags, prov
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?
            )""",
            (
                kit_id, r.get("folk_name"), r.get("game"), r.get("corpus"),
                tier, tier_conf_pend, r.get("canon_tier"), r.get("eras"),
                is_neg, r.get("lineage"), r.get("gx"),
                "canon", is_sys, is_unres, is_mint, dossier_owed_val,
                atlas_key, kc, "mobile-harvest-v3", "2026-07-12",
                lattice_coord,
                attr_v, avg_conf, range_v, avg_conf,
                tempo_v, avg_conf, amp_v, avg_conf,
                proxy_v, avg_conf, commit_v, avg_conf,
                "avg-collapsed", avg_conf,
                r.get("mob"), r.get("geo"), None, None,
                r.get("econ"), r.get("elem_p"),
                1,  # ctrl_def_from_code=1 (ctrl/def not in v3 CSV as raw)
                suffix_status,
                r.get("cell_id"), r.get("key_group"), safe_int(r.get("rank_in_cell")),
                parse_bool(r.get("representative")), r.get("mechanics_status"),
                r.get("blocking_mechanics"), r.get("mech_note"),
                r.get("flags"), r.get("prov"),
            ),
        )
        layer1_count += 1

    conn.commit()
    print(f"  Layer 1 (CSV canon): {layer1_count} rows ingested")

    # Ingest 9 mint kits from mint-dossiers (harvest holes; not in CSV; not in engine-key)
    # They are §F.5(1) candidate-pool members: mint=1, dossier_owed=1, negative=0
    mint_ingest_count = 0
    for mr in mint_rows:
        kit_id = mr["kit_id"]
        atlas_key = mr.get("atlas_key", "")
        attr_v, range_v, tempo_v, amp_v, proxy_v, commit_v = decode_atlas_key(atlas_key)
        seg = atlas_key.split("-")[0] if atlas_key and "-" in atlas_key else (atlas_key[:6] if atlas_key else "")
        lattice_coord = seg[:6] if len(seg) >= 6 else None

        conn.execute(
            """INSERT OR IGNORE INTO canon_corpus (
                kit_id, folk_name, game, corpus_bucket, tier, tier_confirm_pending,
                canon_tier, eras, negative, lineage, gx,
                source, is_system, unresolved, mint, dossier_owed,
                atlas_key_orig, key_completeness, provenance_tag, source_date,
                lattice_coord,
                attr_val, attr_conf, range_val, range_conf,
                tempo_val, tempo_conf, amp_val, amp_conf,
                proxy_val, proxy_conf, commit_val, commit_conf,
                prefix_conf_provenance, avg_conf,
                mob_raw, geo_raw, ctrl_raw, def_raw, econ_raw, elem_raw,
                ctrl_def_from_code, suffix_rekey_status,
                flags, prov
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,
                ?,?,?,?,?,?,?,?,?,?
            )""",
            (
                kit_id, mr.get("folk_name"), mr.get("game"), mr.get("game"),
                None, 0, None, None,
                0, None, None,
                "mint", 0, 0, 1, 1,
                atlas_key, None, "mint-dossier-reexpressed", "2026-07-12",
                lattice_coord,
                attr_v, None, range_v, None,
                tempo_v, None, amp_v, None,
                proxy_v, None, commit_v, None,
                "avg-collapsed", None,
                None, None, None, None, None,
                mr.get("element", {}).get("label_verbatim") if isinstance(mr.get("element"), dict) else None,
                0, "awaiting-rekey",
                None, "mint-dossier",
            ),
        )
        mint_ingest_count += 1

    conn.commit()
    print(f"  Layer 1 (mint kits): {mint_ingest_count} rows ingested")
    total_layer1 = layer1_count + mint_ingest_count
    print(f"  Layer 1 total: {total_layer1} rows (515 CSV + 9 mint = 524 total)")

    # Update: post-ingest assert will check 515 CSV canon + 9 mint = 524
    # Brief says "corpus rows ingested = 515 (496 substrate + 18 SYS-annex + 1 unresolved)"
    # The 9 mint kits are ADDITIONAL — they bring total to 524
    # canon_corpus will have 524 rows total

    # Track canon_kit_ids for FK checks
    canon_kit_ids_in_db = {r["kit_id"] for r in canon_rows} | mint_ids

    # ---- 3. LAYER 2: probe facts (positives only; negatives Layer-1 only) ----
    print("Layer 2: ingesting canon_probe_facts...")
    # Positives = canon rows that are in ek_by_id (478 kits; negatives = 37 not in EK)
    positive_kit_ids = set(ek_by_id.keys())

    layer2_kit_count = 0
    layer2_row_count = 0

    for kit_id in positive_kit_ids:
        # kit must be in canon_corpus (negatives are not in EK; mint kits may be new)
        probe_row = probe_by_id.get(kit_id)
        if probe_row is None:
            # mint kits have their own dossier rows — check mint_dossiers
            mint_probe = next((m for m in mint_rows if m["kit_id"] == kit_id), None)
            if mint_probe:
                probe_row = mint_probe
            else:
                warnings.append(f"L2: kit_id={kit_id} in engine-key but no probe facts found")
                continue

        # Probe row may not be in canon_corpus if it's a mint kit not yet in CSV
        # Mint kits: already ingested in Layer 1 IF they appear in CSV; if not, skip L2 (no FK)
        if kit_id not in canon_kit_ids_in_db:
            findings.append(f"FINDING: kit_id={kit_id} in engine-key/probe but not in CSV canon rows — mint kit not in corpus yet (Layer-2 rows skipped for this kit)")
            continue

        post_cutoff = parse_bool(probe_row.get("post_cutoff", False))
        dossier_owed_val = parse_bool(probe_row.get("dossier_owed", False))

        for family in PROBE_FAMILIES:
            fam_data = probe_row.get(family)
            if fam_data is None:
                continue  # family not present (some negatives or partial probes)

            facts_json = json.dumps(fam_data)
            # Extract conf if present
            if isinstance(fam_data, dict) and "conf" in fam_data:
                conf_val = safe_real(fam_data["conf"])
            else:
                conf_val = None
            # Extract prov if present
            prov_val = fam_data.get("prov") if isinstance(fam_data, dict) else None

            conn.execute(
                """INSERT OR REPLACE INTO canon_probe_facts
                   (kit_id, family, facts_json, conf, prov, post_cutoff_cap, dossier_owed)
                   VALUES (?,?,?,?,?,?,?)""",
                (kit_id, family, facts_json, conf_val, prov_val, post_cutoff, dossier_owed_val),
            )
            layer2_row_count += 1

        layer2_kit_count += 1

    conn.commit()
    print(f"  Layer 2: {layer2_kit_count} kits, {layer2_row_count} family rows")

    # ---- 4. LAYER 3: engine-key verbatim ----
    print("Layer 3: ingesting canon_engine_key...")
    layer3_count = 0
    layer3_skipped = []

    for ek_row in ek_rows:
        kit_id = ek_row["kit_id"]
        if kit_id not in canon_kit_ids_in_db:
            layer3_skipped.append(kit_id)
            findings.append(f"FINDING: engine-key kit_id={kit_id} not in canon_corpus — skipping Layer-3 row (FK would fail)")
            continue

        geo = ek_row.get("engine_geometry", {}) or {}
        ctrl = ek_row.get("ctrl", {}) or {}
        defn = ek_row.get("def", {}) or {}
        econ = ek_row.get("econ", {}) or {}
        mob = ek_row.get("mob", {}) or {}
        prov = ek_row.get("provenance", {}) or {}

        row_class_raw = ek_row.get("row_class", "")
        # Normalize: 'combat-kit' or 'system-record'
        if row_class_raw == "combat-kit":
            row_class = "combat-kit"
        elif row_class_raw == "system-record":
            row_class = "system-record"
        else:
            findings.append(f"FINDING: engine-key kit_id={kit_id} has unexpected row_class={row_class_raw!r}")
            row_class = row_class_raw

        flags_list = ek_row.get("flags", [])

        conn.execute(
            """INSERT INTO canon_engine_key (
                kit_id,
                geometry_value, geometry_rule_fired, geometry_conf,
                ctrl_treatment, ctrl_ailments_mapped, ctrl_ailment_gaps,
                def_bin, def_riders, def_conf,
                econ_status, econ_gaps, econ_meter_type,
                mob_skill_is_movement, mob_policy_while_casting, mob_verbs,
                row_class, route, flags, provenance_json, raw_json
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                kit_id,
                geo.get("value"), geo.get("rule_fired"), safe_real(geo.get("conf")),
                ctrl.get("treatment"),
                json.dumps(ctrl.get("ailments_mapped", [])),
                json.dumps(ctrl.get("ailment_gaps", [])),
                defn.get("bin"),
                json.dumps(defn.get("riders", [])),
                safe_real(defn.get("conf")),
                econ.get("status"),
                json.dumps(econ.get("gaps", [])),
                econ.get("meter_type"),
                parse_bool(mob.get("skill_is_movement", False)),
                mob.get("policy_while_casting"),
                json.dumps(mob.get("verbs", [])),
                row_class,
                ek_row.get("route"),
                json.dumps(flags_list),
                json.dumps(prov),
                json.dumps(ek_row),
            ),
        )
        layer3_count += 1

    conn.commit()
    print(f"  Layer 3: {layer3_count} rows ingested, {len(layer3_skipped)} skipped (FK)")

    # Update suffix_rekey_status on canon_corpus rows that have a Layer-3 key
    # geo/ctrl/def/econ → 'keyed-v1'; mob/elem stay 'descriptor-final' — set them now
    conn.execute("""
        UPDATE canon_corpus
        SET suffix_rekey_status = 'keyed-v1'
        WHERE kit_id IN (SELECT kit_id FROM canon_engine_key)
    """)
    # mob/elem permanent 'descriptor-final' for ALL canon rows (not 'keyed-v1'; these axes never map)
    # We store this distinction as a note in schema_meta — suffix_rekey_status is a single column
    # covering geo/ctrl/def/econ; mob/elem law is schema-by-omission (no rekey_mob/elem tables)
    conn.commit()

    # ---- 5. ROSTER: roster_atlas (45 rows) ----
    print("Roster: ingesting roster_atlas...")
    roster_count = 0
    for rr in roster_csv_rows:
        conn.execute(
            """INSERT INTO roster_atlas
               (kit_id, name, attr, range_slot, tempo, amp, proxy, commit_slot,
                econ, elem, provenance, lineage_targets, note, class_v4r2, source_date)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                rr["kit_id"], rr["name"], rr.get("attr"), rr.get("range"),
                rr.get("tempo"), rr.get("amp"), rr.get("proxy"), rr.get("commit"),
                rr.get("econ"), rr.get("elem"), rr.get("provenance"),
                rr.get("lineage_targets"), rr.get("note"), rr.get("class_v4r2"),
                "2026-07-12",
            ),
        )
        roster_count += 1
    conn.commit()
    print(f"  roster_atlas: {roster_count} rows")

    # ---- 6. ROSTER: lineage_enrichment (45 rows) with FK checks ----
    print("Roster: ingesting roster_lineage_enrichment...")
    roster_kit_ids = {rr["kit_id"] for rr in roster_csv_rows}
    enrich_count = 0
    dangling_roster_refs = []  # FK misses: roster kit_id not in roster_atlas
    dangling_corpus_refs = []  # lineage_target corpus_kit_id not in canon_corpus

    for er in lineage_rows:
        kit_id = er["kit_id"]

        # FK check: must be in roster_atlas
        if kit_id not in roster_kit_ids:
            dangling_roster_refs.append(kit_id)
            findings.append(f"FINDING: lineage_enrichment kit_id={kit_id} not in roster_atlas — dangling FK")
            continue

        # Check lineage_targets resolved corpus_kit_ids
        for lt in er.get("lineage_targets", []):
            cid = lt.get("corpus_kit_id")
            if cid and cid not in canon_kit_ids_in_db:
                dangling_corpus_refs.append((kit_id, cid))
                findings.append(f"FINDING: lineage_enrichment kit_id={kit_id} lineage_target corpus_kit_id={cid} not in canon_corpus — dangling ref")

        bc6 = er.get("bc6", {}) or {}
        conn.execute(
            """INSERT INTO roster_lineage_enrichment (
                kit_id, folk_name, class_v4r2,
                bc6_attr, bc6_range, bc6_tempo, bc6_amp, bc6_proxy, bc6_commit, bc6_raw,
                provenance, note,
                lineage_targets_json, target_count, targets_resolved, targets_gap,
                min_lineage_target_distance,
                nearest_corpus_neighbors_json,
                neighbor_count_d0, neighbor_count_d1, neighbor_count_d2,
                genre_density, whitespace_flag, source_date
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                kit_id, er.get("folk_name"), er.get("class_v4r2"),
                bc6.get("attr"), bc6.get("range"), bc6.get("tempo"),
                bc6.get("amp"), bc6.get("proxy"), bc6.get("commit"),
                er.get("bc6_raw"),
                er.get("provenance"), er.get("note"),
                json.dumps(er.get("lineage_targets", [])),
                safe_int(er.get("target_count")),
                safe_int(er.get("targets_resolved")),
                safe_int(er.get("targets_gap")),
                safe_int(er.get("min_lineage_target_distance")),
                json.dumps(er.get("nearest_corpus_neighbors", [])),
                safe_int(er.get("neighbor_count_d0")),
                safe_int(er.get("neighbor_count_d1")),
                safe_int(er.get("neighbor_count_d2")),
                safe_int(er.get("genre_density")),
                parse_bool(er.get("whitespace_flag", False)),
                "2026-07-12",
            ),
        )
        enrich_count += 1

    conn.commit()
    print(f"  roster_lineage_enrichment: {enrich_count} rows")
    if dangling_roster_refs:
        print(f"  WARN: {len(dangling_roster_refs)} dangling roster FK refs: {dangling_roster_refs}")
    if dangling_corpus_refs:
        print(f"  WARN: {len(dangling_corpus_refs)} dangling corpus refs from lineage targets: {dangling_corpus_refs}")

    # ---- 7. D4 RECONCILIATION: CSV is_system vs engine-key system-record ----
    print("\nD4 Reconciliation: CSV is_system vs engine-key row_class=system-record")
    csv_sys_ids = {r["kit_id"] for r in csv_rows if is_sys_row(r)}
    ek_sys_ids = {r["kit_id"] for r in ek_rows if r.get("row_class") == "system-record"}

    overlap = csv_sys_ids & ek_sys_ids
    csv_sys_only = csv_sys_ids - ek_sys_ids
    ek_sys_only = ek_sys_ids - csv_sys_ids

    print(f"  CSV is_system rows:         {len(csv_sys_ids)}")
    print(f"  EK system-record rows:      {len(ek_sys_ids)}")
    print(f"  Overlap (both):             {len(overlap)}")
    print(f"  CSV-sys ONLY (combat in EK): {sorted(csv_sys_only)}")
    print(f"  EK-sys ONLY (not CSV-sys):  {sorted(ek_sys_only)}")

    findings.append(f"D4: CSV is_system={len(csv_sys_ids)}, EK system-record={len(ek_sys_ids)}, overlap={len(overlap)}")
    findings.append(f"D4: CSV-sys-only (EK=combat-kit) — {len(csv_sys_only)} kits: {sorted(csv_sys_only)}")
    findings.append(f"D4: EK-sys-only (not CSV-sys-flagged) — {len(ek_sys_only)} kits: {sorted(ek_sys_only)}")
    findings.append("D4: Layer-3 row_class governs combat denominators per DELTA v2 §D4. Divergence is expected: different evidence sources, not an error.")

    # ---- 8. POST-INGEST ASSERTS ----
    # Total canon_corpus: 515 (CSV canon) + 9 (mint) = 524
    print("\nPost-ingest asserts:")

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    print(f"  canon_corpus rows: {r} (expected 524: 515 CSV + 9 mint)")
    assert r == 524, f"canon_corpus count mismatch: {r} != 524"

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE source='canon'").fetchone()[0]
    print(f"  canon_corpus source=canon: {r} (expected 515 CSV-sourced)")
    assert r == 515

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE is_system=1").fetchone()[0]
    print(f"  is_system=1: {r} (expected 18)")
    assert r == 18, f"is_system count mismatch: {r} != 18"

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE negative=1").fetchone()[0]
    print(f"  negative=1: {r} (expected 37)")
    assert r == 37, f"negative count mismatch: {r} != 37"

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE game='hot'").fetchone()[0]
    print(f"  game=hot: {r} (expected 19)")
    assert r == 19

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE game='hot' AND tier='T3' AND tier_confirm_pending=0").fetchone()[0]
    print(f"  HoT tier=T3, tier_confirm_pending=0: {r} (expected 19 — Q24(c))")
    assert r == 19, f"HoT T3 confirm mismatch: {r} != 19"

    r = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE mint=1").fetchone()[0]
    print(f"  mint=1: {r} (expected 9)")
    assert r == 9, f"mint count mismatch: {r} != 9"

    r = conn.execute("SELECT COUNT(*) FROM canon_probe_facts").fetchone()[0]
    print(f"  canon_probe_facts rows: {r}")

    r = conn.execute("SELECT COUNT(DISTINCT kit_id) FROM canon_probe_facts").fetchone()[0]
    print(f"  canon_probe_facts distinct kits: {r}")

    r = conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    print(f"  canon_engine_key rows: {r} (expected 478)")
    assert r == 478, f"engine-key count mismatch: {r} != 478"

    r = conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit'").fetchone()[0]
    print(f"  engine-key combat-kit: {r} (expected 463)")
    assert r == 463, f"combat-kit count mismatch: {r} != 463"

    r = conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record'").fetchone()[0]
    print(f"  engine-key system-record: {r} (expected 15)")
    assert r == 15, f"system-record count mismatch: {r} != 15"

    r = conn.execute("SELECT COUNT(*) FROM roster_atlas").fetchone()[0]
    print(f"  roster_atlas rows: {r} (expected 45)")
    assert r == 45, f"roster_atlas count mismatch: {r} != 45"

    r = conn.execute("SELECT COUNT(*) FROM roster_lineage_enrichment").fetchone()[0]
    print(f"  roster_lineage_enrichment rows: {r} (expected 45)")
    assert r == 45, f"roster_lineage_enrichment count mismatch: {r} != 45"

    # ---- 9. D6 ACCEPTANCE HARNESS: reproduce boards-v1.md counts ----
    print("\nD6 Acceptance harness (boards-v1.md):")
    harness_mismatches = []

    def check(label, query, expected, op="eq"):
        val = conn.execute(query).fetchone()[0]
        if op == "eq":
            ok = val == expected
        else:
            ok = True
        status = "OK" if ok else f"MISMATCH (got {val}, expected {expected})"
        print(f"  {label}: {val} {status}")
        if not ok:
            harness_mismatches.append(f"{label}: got {val}, expected {expected}")
        return val

    # Board 2: combat denominator
    check("Board2: combat denominator",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit'",
          463)
    check("Board2: system-record count",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record'",
          15)

    # Board 2: geometry distribution
    check("Board2: ground_targeted_circle",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='ground_targeted_circle'",
          102)
    check("Board2: circle",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='circle'",
          69)
    check("Board2: totem",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='totem'",
          48)
    check("Board2: multi_projectile",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='multi_projectile'",
          41)
    check("Board2: single_target",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='single_target'",
          38)
    check("Board2: melee_strike",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='melee_strike'",
          37)
    check("Board2: chain",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='chain'",
          28)
    check("Board2: whirlwind",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='whirlwind'",
          15)
    check("Board2: dash_attack",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='dash_attack'",
          14)
    check("Board2: vortex_pull",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='vortex_pull'",
          12)
    check("Board2: cone",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='cone'",
          11)
    check("Board2: ring",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='ring'",
          9)
    check("Board2: aura",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='aura'",
          8)
    check("Board2: line",
          "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='line'",
          8)

    # Board 2: Walls=3 (Q15 workstream), Orbit=4 (gx-candidate:orbit)
    # Walls demand set = 2 placed-lane re-keys (d2-firewall-sorc, di-bone-wall-necro-pvp) + 1 demand-set
    # member that KEEPS geometry=totem per judgment-resolutions-v1.md §5 (le-frost-wall-rm).
    # The §5 ruling was encoded into the JSONL 2026-07-12 (gandalf verification pass) as
    # flags=['resolved:walls-demand'] — the demand count is now fully machine-reproducible.
    walls_val = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' "
        "AND (flags LIKE '%placed-lane%' OR flags LIKE '%walls-demand%')"
    ).fetchone()[0]
    orbit_val = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND flags LIKE '%gx-candidate:orbit%'"
    ).fetchone()[0]
    print(f"  Board2: walls (placed-lane + walls-demand flags): {walls_val} (expected 3)")
    print(f"  Board2: orbit (gx-candidate:orbit flags): {orbit_val} (expected 4)")
    if walls_val != 3:
        harness_mismatches.append(f"Board2: walls (placed-lane + walls-demand flags): got {walls_val}, expected 3")
    if orbit_val != 4:
        harness_mismatches.append(f"Board2: orbit gx-candidate: got {orbit_val}, expected 4")

    # Board 3: ailment-gap census — requires parsing ctrl_ailment_gaps JSON
    # damage-amp: distinct kits where ailment_gaps contains 'GAP-AILMENT:damage-amp'
    def count_ailment_gap(gap_label, expected):
        q = f"""
            SELECT COUNT(DISTINCT kit_id) FROM canon_engine_key
            WHERE row_class='combat-kit'
            AND ctrl_ailment_gaps LIKE '%{gap_label}%'
        """
        val = conn.execute(q).fetchone()[0]
        ok = val == expected
        status = "OK" if ok else f"MISMATCH (got {val}, expected {expected})"
        print(f"  Board3: {gap_label}: {val} {status}")
        if not ok:
            harness_mismatches.append(f"Board3: {gap_label}: got {val}, expected {expected}")
        return val

    count_ailment_gap("GAP-AILMENT:damage-amp", 97)
    # freeze=42 per boards-v1.md ERRATA 2026-07-12 (gandalf verification pass): the board's
    # generation-time 43 (and damage-amp 100) pre-dated the J-GEO reclass stripping system-record
    # rows (incl. hades1-privileged-status) out of the gap censuses. Delivered JSONL = truth; DB governs.
    count_ailment_gap("GAP-AILMENT:freeze", 42)
    count_ailment_gap("GAP-AILMENT:stun", 36)
    count_ailment_gap("GAP-AILMENT:poison-dot", 36)

    # Board 1: SU mechanics-demand = 48 (totem + ratified)
    su_demand = conn.execute(
        """SELECT COUNT(DISTINCT kit_id) FROM canon_engine_key
           WHERE row_class='combat-kit'
           AND (geometry_value='totem'
                OR flags LIKE '%resolved:totem-ratified%'
                OR kit_id IN (
                    SELECT kit_id FROM canon_engine_key
                    WHERE econ_gaps LIKE '%SU%' OR econ_status='gap'
                ))"""
    ).fetchone()[0]
    # More precise: board says "economy=6 / mechanics-demand=48 (totem-keyed + J-SUM-resolved)"
    # This is totem geometry_value count + totem-ratified resolved flags
    totem_geo = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND geometry_value='totem'"
    ).fetchone()[0]
    totem_ratified = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND flags LIKE '%resolved:totem-ratified%'"
    ).fetchone()[0]
    totem_total = conn.execute(
        """SELECT COUNT(*) FROM canon_engine_key
           WHERE row_class='combat-kit'
           AND (geometry_value='totem' OR flags LIKE '%resolved:totem-ratified%')"""
    ).fetchone()[0]
    print(f"  Board1: SU totem (geometry): {totem_geo}, totem-ratified flags: {totem_ratified}, total unique: {totem_total} (expected 48)")
    if totem_total != 48:
        harness_mismatches.append(f"Board1: SU demand (totem+ratified): got {totem_total}, expected 48")

    # Board 4: def-bin distribution (all records = combat + system = 478)
    check("Board4: tank",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='tank'",
          215)
    check("Board4: mitigate",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='mitigate'",
          84)
    check("Board4: glass",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='glass'",
          67)
    check("Board4: evade",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='evade'",
          66)
    check("Board4: absorb",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='absorb'",
          28)
    # FLAGGED def_bin: engine-key stores None/NULL for flagged entries (no literal 'FLAGGED' string)
    # Board says FLAGGED=14; engine-key has 14 rows with def_bin=None (all system-records)
    flagged_null = conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE def_bin IS NULL").fetchone()[0]
    print(f"  Board4: FLAGGED (NULL def_bin): {flagged_null} (expected 14 — engine-key stores NULL not string 'FLAGGED')")
    if flagged_null != 14:
        harness_mismatches.append(f"Board4: FLAGGED/NULL def_bin: got {flagged_null}, expected 14")
    check("Board4: post-cutoff-deferred",
          "SELECT COUNT(*) FROM canon_engine_key WHERE def_bin='post-cutoff-deferred'",
          4)

    # damage-amp Board 3 note: board shows 100 in "damage-amp count" row but text says "97 unique kits"
    # The discrepancy is in the board wording: "damage-amp 97 unique kits" is the acceptance target
    # Let's also report the raw count
    raw_da = conn.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit' AND ctrl_ailment_gaps LIKE '%GAP-AILMENT:damage-amp%'"
    ).fetchone()[0]
    print(f"  Board3: damage-amp raw (non-distinct): {raw_da}")

    # ---- 10. Final summary ----
    def q(sql):
        return conn.execute(sql).fetchone()[0]

    print("\n--- INGEST LOG SUMMARY ---")
    print("canon_corpus:              " + str(q("SELECT COUNT(*) FROM canon_corpus")) + " (515 CSV + 9 mint)")
    print("  source=canon:            " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE source='canon'")) + " (CSV-sourced)")
    print("  source=mint:             " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE source='mint'")) + " (mint kits from dossiers)")
    print("  negative=1:              " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE negative=1")))
    print("  is_system=1:             " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE is_system=1")))
    print("  mint=1:                  " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE mint=1")))
    print("  HoT rows (T3,pending=0): " + str(q("SELECT COUNT(*) FROM canon_corpus WHERE game='hot' AND tier='T3' AND tier_confirm_pending=0")))
    print("canon_probe_facts:         " + str(q("SELECT COUNT(*) FROM canon_probe_facts")) + " rows / " + str(q("SELECT COUNT(DISTINCT kit_id) FROM canon_probe_facts")) + " kits")
    print("canon_engine_key:          " + str(q("SELECT COUNT(*) FROM canon_engine_key")) + " (combat=" + str(q("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit'")) + ", system=" + str(q("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record'")) + ")")
    print("roster_atlas:              " + str(q("SELECT COUNT(*) FROM roster_atlas")))
    print("roster_lineage_enrichment: " + str(q("SELECT COUNT(*) FROM roster_lineage_enrichment")))
    print(f"\nFindings ({len(findings)}):")
    for f in findings:
        print(f"  {f}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
    if harness_mismatches:
        print(f"\nACCEPTANCE HARNESS MISMATCHES ({len(harness_mismatches)}) — STOP:")
        for m in harness_mismatches:
            print(f"  MISMATCH: {m}")
        sys.exit(1)
    else:
        print("\nACCEPTANCE HARNESS: ALL COUNTS MATCH. Ingest complete.")

    conn.close()
    return findings, harness_mismatches


if __name__ == "__main__":
    main()
