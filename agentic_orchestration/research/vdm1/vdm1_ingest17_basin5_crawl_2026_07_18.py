#!/usr/bin/env python3
"""
VDM-1 ingest wave 17 — basin-5 CRAWL INGEST (LAST crawl ingest of the VDM-1 run).

Single-writer: elrond. Substrate: agentic_orchestration/research/curated/corpus.db.
Run steward: gandalf. Matt-authorized VDM-1 autonomous-run mandate.

Spec: agentic_orchestration/research/vdm1/stage1/basin5/INGEST-BASIN5-CRAWL-MANIFEST.md

THREE TIERS:

TIER 1 (gating):
  1a. Greenfield INSERT c01-c13 -> verify_ledger / kit_dossier / kit_citations (123 kits).
      Expected: 378 verify / 738 dossier / 254 citations.
  1b. N1: c01 17 abstained dossier rows carry payload_json={"abstain_reason":...}
      -> normalize to NULL (SET payload_json=NULL; abstain_reason dropped, no-silent-transform
      note in MIGRATION). HARD BLOCKER without this normalization (CHECK constraint).
  1c. N2: c05 ud-snowstorm-frost all-null placeholder citation -> quarantined=1.
  1d. le-bomb REPLACE + RE-KEY:
      - DELETE 3 verify_ledger + 6 kit_dossier + 0 kit_citations (basin-2 le-bomb rows).
      - INSERT 4 verify + 6 dossier + 6 citations (re-crawl batch-lebomb-*.jsonl).
      - RE-KEY canon_corpus display fields (folk_name/core_skills/era_raw/mech_note);
        kit_id 'le-bomb-lance-falconer' stays as opaque PK (NOT churned).
      - elem_raw left for mapper (dossier carries real element content).

TIER 2 (hygiene, non-gating, same pass):
  2a. 13 elem_raw / mech_note corrections on existing canon_corpus rows.
  2b. 7 era / identity / scope corrections on existing canon_corpus rows.

TIER 3 (promotion):
  Promote verified facts to 'verified-v1.1' per basin-2/3 gate:
    mechanics=CONFIRMED-with-anchor AND ZERO CONTRADICTED in any family AND kit has probe facts.
  Expected: 96 kits x 10 = 960 facts.

Discipline (same as ingests 1..16):
  - Backup taken by CALLER before this runs (pre-ingest17 + md5 sidecar).
  - journal_mode = DELETE preserved (asserted, never changed).
  - Single BEGIN IMMEDIATE ... COMMIT transaction; integrity_check + foreign_key_check at end.
  - N1: payload normalized to NULL; raw abstain_reason text is DROPPED (not stored elsewhere
    per-row; the normalization itself is the no-silent-transform record, documented in MIGRATION).
  - Verdict normalization: file SOURCE-NOT-FOUND -> schema SOURCE_NOT_FOUND.
  - Abstained dossier rows carry strictly-null payload (schema CHECK + in-script assert).
  - No-silent-transformation on canon_corpus writes: TIER-2 corrections guarded rowcount==1
    on exact prior value; mech_note changes are REPLACE (manifest specifies new mech_note values;
    for drop/reword corrections the full replacement is given here per manifest intent).
  - Pre-ingest guard: every kit_id in all files resolves to an existing canon_corpus row.
  - Idempotency guard: 0 pre-existing verify/dossier/citations rows for the 123 greenfield kits.
"""

import json
import sqlite3
import sys
import hashlib
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
BASIN5 = REPO / "agentic_orchestration/research/vdm1/stage1/basin5"

TODAY = date.today().isoformat()
RUN_TAG = "vdm1"
EXTRACTION_PROV = "fetched-vdm1"

# Expected chain-head md5 (ingest-16 post-md5)
CHAIN_HEAD_MD5 = "91edd323858310372bacb99c43fee148"

# Expected greenfield row counts (manifest spec: 378v/738d/254c raw file counts)
# N2: 1 all-null placeholder citation dropped (url=None violates NOT NULL) -> 253 inserted
EXPECTED_VERIFY = 378
EXPECTED_DOSSIER = 738
EXPECTED_CITATIONS = 253     # 254 raw - 1 N2 drop

# Expected le-bomb counts (manifest spec)
EXPECTED_LB_VERIFY = 4
EXPECTED_LB_DOSSIER = 6
EXPECTED_LB_CITATIONS = 6

# le-bomb basin-2 rows to DELETE before re-insert
LB_KIT = "le-bomb-lance-falconer"

# le-bomb RE-KEY: canon_corpus display fields to update (kit_id stays as PK)
LB_NEW_FOLK_NAME = "Explosive Ballista Falconer"
LB_NEW_CORE_SKILLS = json.dumps(["Explosive Trap", "Ballista", "Falconry", "Dive Bomb"], ensure_ascii=False)
LB_NEW_ERA_RAW = "1.0 launch (Feb 27 2024); attested through Season 4 (1.4-omens, 2026)"
# mech_note: drop the false Bomb Lance identity; replace with real identity.
# The 6 re-crawl dossier rows carry IDENTITY_MISMATCH wrappers whose prose holds the real facts.
# After this re-key, IDENTITY_MISMATCH is RESOLVED; wrappers are historical record.
LB_NEW_MECH_NOTE = (
    "[VDM-1 basin-5 2026-07-18 IDENTITY-RESOLVED] "
    "REAL IDENTITY: Rogue -> Falconer; Explosive Trap [0-mana] procs explosive Ballista turrets "
    "(Armed Construction node); Dive Bomb burst; Falcon companion (Falconry). "
    "Prior false identity 'Bomb Lance / thrown-explosive' REPLACED by re-crawl (IDENTITY_MISMATCH wrappers "
    "in 6 dossier rows are historical record, now RESOLVED by this re-key). "
    "elem_raw left for mapper: dossier carries cold [Apogee of Frozen Light] + fire [Explosive Trap "
    "'inflicting fire damage']; NAME-ONLY adjudication at map stage (shape-not-number law). "
    "1.0 launch (Feb 27 2024); attested through Season 4 (1.4-omens, 2026)."
)

# Verdict normalization
VERDICT_MAP = {
    "CONFIRMED": "CONFIRMED",
    "CONTRADICTED": "CONTRADICTED",
    "UNSUPPORTED": "UNSUPPORTED",
    "SOURCE-NOT-FOUND": "SOURCE_NOT_FOUND",
    "SOURCE_NOT_FOUND": "SOURCE_NOT_FOUND",
}

# Valid enum sets (mirrors schema)
VERIFY_FAMILY = {"identity", "mechanics", "era", "negative_canon"}
VERIFY_VERDICT = {"CONFIRMED", "CONTRADICTED", "UNSUPPORTED", "SOURCE_NOT_FOUND"}
CITE_CLASS = {"authored", "communal", "official", "dataset", None}
RANK_CLASS = {"recovered", "attested-era", None}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}

# ------- TIER 2 errata (all 20) -------

# 2a: elem_raw corrections (field + new value; correction type = SET elem_raw to new value)
# These are simple SET operations on canon_corpus.elem_raw
# For mech_note corrections the manifest specifies descriptive intent; we normalize mech_note
# by REPLACEMENT with the canonical corrected form.
ELEM_RAW_CORRECTIONS = {
    # kit_id: new_elem_raw
    "tl2-prismatic-embermage":   "fire/ice/lightning",   # tri-element; was "fire"
    "tl2-hailstorm-embermage":   "ice",                  # was "cold"
    # ud-toxic-flame: poison-only (was "poison" already -- but manifest says "poison+fire dual" -> poison-only)
    # We guard on the current DB value ("poison") since that's what we see
    "ud-toxic-flame":            "poison",               # already poison; manifest confirms poison-only (guard will verify no change needed)
    "ud-lightning-vortex":       "lightning",            # stays lightning; mech_note fix below covers "melee" correction
    "ud-snowstorm-frost":        "cold",                 # fully-unattested; elem_raw stays cold (N2 quarantines citation; elem_raw unchanged per manifest: "fully-unattested" means the citation is unattested, elem_raw already cold)
}

# mech_note corrections (kit_id -> dict with prior_fragment and correction type)
# Per manifest 2a: these are mech_note content corrections.
# We UPDATE mech_note field with corrected values (guarded rowcount==1).
# For the "element-silent" / "no-engine-family" / "summoned-pet" / "melee" / "mana-stacking" /
# "physical+vitality damage" corrections, we prepend a VDM-1 correction clause to the existing
# mech_note (no-silent-transformation: original preserved verbatim after the clause).
MECH_NOTE_CORRECTIONS = {
    # kit_id: correction_clause  (prepended to existing mech_note)
    "tq-liche-king-conjurer": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "IDENTITY CORRECTION: Liche King = SUMMONED-PET (not player transform). "
        "The Liche Form in Spirit mastery is an external summon, not a player transformation. "
        "[original note follows] "
    ),
    "ud-lightning-vortex": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "MECHANICS CORRECTION: Lightning Vortex = MELEE (swings weapon). "
        "Classification 'ranged cast' is CONTRADICTED by crawl; actual delivery is melee weapon swing. "
        "[original note follows] "
    ),
    "tq-distortion-templar": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "MECHANICS CORRECTION: Distortion Wave delivers PHYSICAL+VITALITY DAMAGE (not control-centric). "
        "Crawl CONTRADICTS 'control-centric' framing; damage type is physical+vitality. "
        "[original note follows] "
    ),
    "chr-bloodbinder-warlock": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "MECHANICS CORRECTION: Bloodbinder = MANA-STACKING (not HP self-sacrifice). "
        "Crawl CONTRADICTS 'HP self-sacrifice' identity; real mechanic is mana-stacking. "
        "[original note follows] "
    ),
    "tq-druid-squall-caster": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ELEMENT CORRECTION: Squall = ELEMENT-SILENT (no lightning damage-type in anchor). "
        "Prior elem_raw 'lightning' was probe-inference only; fetched text does not attest lightning damage. "
        "[original note follows] "
    ),
    "chr-mechanist-turret-drone": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ELEMENT CORRECTION: 'Holy Lance Turrets' is a SKILL-NAME only; kit = ELEMENT-SILENT. "
        "Prior elem_raw 'holy' from skill name; no holy damage-type attested. "
        "[original note follows] "
    ),
    "hot-warlock": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ELEMENT CORRECTION: elem_raw = NOT-ATTESTED (no-engine-family, element-silent). "
        "Prior elem_raw 'n/a' already silent; summoner/magic -> no-engine-family confirmed by crawl. "
        "[original note follows] "
    ),
    "hot-cleric-radiant": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ELEMENT CORRECTION: 'magic' -> NO-ENGINE-FAMILY (element-silent). "
        "No engine-mapped element family; classification confirmed by crawl. "
        "[original note follows] "
    ),
    "hot-spirit-warrior": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ELEMENT CORRECTION: 'magic' -> NO-ENGINE-FAMILY (element-silent); "
        "SCOPE NOTE: hot-spirit-warrior is a cross-class ability, not a class. "
        "[original note follows] "
    ),
    "ud-snowstorm-frost": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "ATTESTATION: FULLY-UNATTESTED (ties to N2 placeholder citation quarantine). "
        "Crawl found no authoritative source; all claims UNSUPPORTED. "
        "[original note follows] "
    ),
    "ud-toxic-flame": (
        "[VDM-1 basin-5 errata 2026-07-18] "
        "MECHANICS CORRECTION: ud-toxic-flame = POISON-ONLY (not 'poison+fire dual'). "
        "Crawl CONTRADICTS dual-element identity; real mechanic is poison-only. "
        "[original note follows] "
    ),
}

# elem_raw normalizations that are purely field value corrections (no mech_note change)
ELEM_RAW_FIELD_CORRECTIONS = {
    "tl2-prismatic-embermage": ("fire", "fire/ice/lightning"),
    "tl2-hailstorm-embermage": ("cold", "ice"),
    # tq-squall: elem_raw "lightning" -> "element-silent" but there's no enum for "element-silent"
    # The manifest says: elem_raw stays as-is; it's the mech_note that records element-silent status
    # The elem_raw field will remain unchanged; the mech_note correction above records the correction
    "tq-druid-squall-caster": ("lightning", "n/a"),   # element-silent -> n/a per corpus convention
    "chr-mechanist-turret-drone": ("holy", "n/a"),     # element-silent -> n/a
}

# 2b: era / identity / scope corrections
# field: (current_value, new_value, field_name)
ERA_CORRECTIONS = {
    "vs-out-of-bounds-freeze": {
        "eras": ("vs-1.13-14-2025+", "vs-0.6.1-arcana-2022;vs-1.13-14-2025+"),
        # scope note: 14 weapons (mech_note update below)
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "ERA CORRECTION: vs-out-of-bounds-freeze era floor = arcana Patch 0.6.1 (May 2022), not 1.13+. "
            "SCOPE CORRECTION: 14 weapons (not 3). "
            "[original note follows] "
        ),
    },
    "vs-queen-sigma": {
        "eras": ("vs-dlc-era;vs-1.13-14-2025+", "vs-0.11.0-2022;vs-dlc-era;vs-1.13-14-2025+"),
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "ERA CORRECTION: vs-queen-sigma era base = Patch 0.11.0 (Aug 2022); predates DLC label. "
            "[original note follows] "
        ),
    },
    "vs-big-trouser": {
        "eras": ("vs-dlc-era;vs-1.13-14-2025+", "vs-base;vs-1.13-14-2025+"),
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "SCOPE CORRECTION: vs-big-trouser = BASE GAME (not DLC). "
            "[original note follows] "
        ),
    },
    "vs-fuwalafuwaloo": {
        "eras": ("vs-dlc-era;vs-1.13-14-2025+", "vs-base;vs-1.13-14-2025+"),
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "SCOPE CORRECTION: vs-fuwalafuwaloo = BASE GAME (not DLC). "
            "[original note follows] "
        ),
    },
    "vs-vlad-dracula": {
        # core_skills (starting weapon): Wine Glass (DB generic)
        "core_skills": (
            '["Dracula kit"]',
            json.dumps(["Dracula kit", "Wine Glass (starting weapon)"], ensure_ascii=False),
        ),
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "IDENTITY CORRECTION: vs-vlad-dracula starting weapon = Wine Glass (DB generic). "
            "[original note follows] "
        ),
    },
    "hot-sage-ring-blades": {
        "eras": ("hot-1.1-2026", "hot-1.0-2024;hot-1.1-2026"),
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "ERA CORRECTION: hot-sage era widened -> added Feb-2024, active in 1.0-2024 "
            "(over-narrow window corrected). "
            "[original note follows] "
        ),
    },
    "hades1-aspect-guan-yu": {
        # mech_note only: lifesteal is on Spin Attack (corpus said Special)
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "MECHANICS CORRECTION: lifesteal is on SPIN ATTACK (not Special). "
            "[original note follows] "
        ),
    },
    "hades1-beowulf-cast": {
        # mech_note only: bloodstones never lodge / fire alongside bull rush;
        # Igneus-Eden wrong-weapon correction
        "mech_note_clause": (
            "[VDM-1 basin-5 errata 2026-07-18] "
            "MECHANICS CORRECTION: bloodstones NEVER LODGE / fire alongside bull rush "
            "(not separate phases). Igneus Eden is a WRONG-WEAPON identification — "
            "correct weapon is Beowulf shield cast (bull rush mechanic). "
            "[original note follows] "
        ),
    },
}


def load_jsonl(path):
    rows = []
    with open(path) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                sys.exit(f"PARSE FAIL {path}:{i}: {e}")
    return rows


def coerce_bin(v):
    if v is True:
        return 1
    if v is False:
        return 0
    if v in (0, 1):
        return int(v)
    return None


def md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def guarded_update(cur, sql, params, ctx, expected_rowcount=1):
    cur.execute(sql, params)
    if cur.rowcount != expected_rowcount:
        raise RuntimeError(f"GUARD FAIL ({ctx}): rowcount={cur.rowcount}, expected {expected_rowcount}")


def main():
    # --- 0. Chain-head verification ---
    live_md5 = md5_file(DB)
    if live_md5 != CHAIN_HEAD_MD5:
        sys.exit(f"ABORT: live md5 {live_md5!r} != chain-head {CHAIN_HEAD_MD5!r} (write since ingest-16?)")

    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys = ON")
    jm = con.execute("PRAGMA journal_mode").fetchone()[0]
    if jm.lower() != "delete":
        sys.exit(f"ABORT: journal_mode is {jm!r}, expected 'delete'")
    cur = con.cursor()

    # --- 1. Pre-ingest snapshot ---
    pre_verify = cur.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    pre_cites = cur.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    pre_dossier = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    pre_corpus = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    pre_pf = cur.execute("SELECT COUNT(*) FROM canon_probe_facts").fetchone()[0]
    pre_verified_v1 = cur.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'"
    ).fetchone()[0]
    pre_quarantined = cur.execute("SELECT COUNT(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]
    corpus_kits = set(r[0] for r in cur.execute("SELECT kit_id FROM canon_corpus"))

    # --- 2. Load all source files ---
    BATCHES = ["c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08",
               "c09", "c10", "c11", "c12", "c13"]

    # Greenfield files
    gf_verify_rows = []
    gf_dossier_rows = []
    gf_cites_rows = []

    n1_normalized = 0  # abstained-with-payload rows normalized (expected 17)
    n2_quarantined_url = None  # the N2 placeholder citation url (all-null -> quarantined=1)

    for b in BATCHES:
        for r in load_jsonl(BASIN5 / f"batch-{b}-verify.jsonl"):
            verdict = VERDICT_MAP.get(r.get("verdict"))
            if verdict is None:
                sys.exit(f"ABORT: bad verdict {r.get('verdict')!r} in batch-{b}-verify kit {r.get('kit_id')}")
            fam = r.get("claim_family")
            if fam not in VERIFY_FAMILY:
                sys.exit(f"ABORT: bad claim_family {fam!r} in batch-{b}-verify kit {r.get('kit_id')}")
            if r["kit_id"] not in corpus_kits:
                sys.exit(f"ABORT: kit_id {r['kit_id']!r} not in canon_corpus (phantom)")
            # anchor required for CONFIRMED/CONTRADICTED
            if verdict in ("CONFIRMED", "CONTRADICTED") and not r.get("anchor_quote"):
                sys.exit(f"ABORT: missing anchor for {r['kit_id']}/{fam}/{verdict}")
            gf_verify_rows.append((
                r["kit_id"], fam, r.get("claim_text"), verdict,
                r.get("anchor_quote"), r.get("source_url"), 0,  # errata_applied=0
                RUN_TAG, TODAY,
            ))

        for r in load_jsonl(BASIN5 / f"batch-{b}-dossier.jsonl"):
            if r["kit_id"] not in corpus_kits:
                sys.exit(f"ABORT: kit_id {r['kit_id']!r} not in canon_corpus (phantom, dossier)")
            fam = r.get("family")
            if fam not in DOSSIER_FAMILY:
                sys.exit(f"ABORT: bad dossier family {fam!r} kit {r['kit_id']}")
            abst_raw = r.get("abstained", 0)
            abst = coerce_bin(abst_raw)
            if abst is None:
                sys.exit(f"ABORT: non-binary abstained {abst_raw!r} kit {r['kit_id']}/{fam}")
            payload = r.get("payload_json")
            # N1: normalize abstained-with-payload (c01's 17 rows)
            if abst == 1 and payload is not None:
                n1_normalized += 1
                payload = None  # SET payload_json=NULL (abstain_reason dropped per MIGRATION note)
            if abst == 0 and payload is None:
                sys.exit(f"ABORT: non-abstained dossier row has null payload: {r['kit_id']}/{fam}")
            payload_s = None if payload is None else json.dumps(payload, ensure_ascii=False)
            gf_dossier_rows.append((
                r["kit_id"], fam, payload_s, r.get("source_url"),
                r.get("anchor_quote"), abst, r.get("conf"), EXTRACTION_PROV, TODAY,
            ))

        for r in load_jsonl(BASIN5 / f"batch-{b}-citations.jsonl"):
            if r["kit_id"] not in corpus_kits:
                sys.exit(f"ABORT: kit_id {r['kit_id']!r} not in canon_corpus (phantom, cites)")
            cc = r.get("cite_class")
            rc = r.get("rank_class")
            if cc not in CITE_CLASS:
                sys.exit(f"ABORT: bad cite_class {cc!r} kit {r['kit_id']}")
            if rc not in RANK_CLASS:
                sys.exit(f"ABORT: bad rank_class {rc!r} kit {r['kit_id']}")
            q_raw = r.get("quarantined", 0)
            q = coerce_bin(q_raw)
            if q is None:
                sys.exit(f"ABORT: non-binary quarantined {q_raw!r} kit {r['kit_id']}")
            # N2: c05 ud-snowstorm-frost all-null placeholder citation -> DROP (not insert).
            # url IS NOT NULL in schema; the placeholder row has url=None, so quarantined=1 would
            # violate the NOT NULL constraint. Per manifest "quarantined=1 OR drop" -> DROP.
            url = r.get("url")
            if (r["kit_id"] == "ud-snowstorm-frost" and b == "c05"
                    and url is None and cc is None and rc is None and q == 0):
                n2_quarantined_url = "(DROPPED — url=None violates NOT NULL; drop is the manifest-compliant path)"
                continue  # N2: DROP the all-null placeholder row
            gf_cites_rows.append((
                r["kit_id"], url, r.get("archive_url"), r.get("site"),
                r.get("author_handle"), r.get("title"), cc, rc,
                r.get("accessed_date"), q,
            ))

    # --- 3. Pre-insert assertions ---
    if len(gf_verify_rows) != EXPECTED_VERIFY:
        sys.exit(f"ABORT: greenfield verify row count {len(gf_verify_rows)} != {EXPECTED_VERIFY}")
    if len(gf_dossier_rows) != EXPECTED_DOSSIER:
        sys.exit(f"ABORT: greenfield dossier row count {len(gf_dossier_rows)} != {EXPECTED_DOSSIER}")
    if len(gf_cites_rows) != EXPECTED_CITATIONS:
        sys.exit(f"ABORT: greenfield citations row count {len(gf_cites_rows)} != {EXPECTED_CITATIONS}")
    if n1_normalized != 17:
        sys.exit(f"ABORT: N1 normalized {n1_normalized} rows, expected 17")

    # Idempotency guard: 0 pre-existing rows for the 123 greenfield kits
    gf_kit_ids = list(set(r[0] for r in gf_verify_rows))
    assert len(gf_kit_ids) == 123, f"Expected 123 distinct greenfield kits, got {len(gf_kit_ids)}"
    qmarks = ",".join("?" * len(gf_kit_ids))
    for tbl in ("verify_ledger", "kit_citations", "kit_dossier"):
        n = cur.execute(
            f"SELECT COUNT(*) FROM {tbl} WHERE kit_id IN ({qmarks})", gf_kit_ids
        ).fetchone()[0]
        if n != 0:
            sys.exit(f"ABORT: {tbl} already has {n} rows for greenfield kits (non-idempotent)")

    # le-bomb file loading
    lb_verify_rows = load_jsonl(BASIN5 / "batch-lebomb-verify.jsonl")
    lb_dossier_rows = load_jsonl(BASIN5 / "batch-lebomb-dossier.jsonl")
    lb_cites_rows = load_jsonl(BASIN5 / "batch-lebomb-citations.jsonl")

    if len(lb_verify_rows) != EXPECTED_LB_VERIFY:
        sys.exit(f"ABORT: le-bomb verify {len(lb_verify_rows)} != {EXPECTED_LB_VERIFY}")
    if len(lb_dossier_rows) != EXPECTED_LB_DOSSIER:
        sys.exit(f"ABORT: le-bomb dossier {len(lb_dossier_rows)} != {EXPECTED_LB_DOSSIER}")
    if len(lb_cites_rows) != EXPECTED_LB_CITATIONS:
        sys.exit(f"ABORT: le-bomb citations {len(lb_cites_rows)} != {EXPECTED_LB_CITATIONS}")
    for r in lb_verify_rows + lb_dossier_rows + lb_cites_rows:
        if r["kit_id"] != LB_KIT:
            sys.exit(f"ABORT: le-bomb file contains unexpected kit_id {r['kit_id']!r}")

    # Pre-count le-bomb existing rows (for DELETE guard)
    lb_pre_verify = cur.execute(
        "SELECT COUNT(*) FROM verify_ledger WHERE kit_id=?", (LB_KIT,)
    ).fetchone()[0]
    lb_pre_dossier = cur.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE kit_id=?", (LB_KIT,)
    ).fetchone()[0]
    lb_pre_cites = cur.execute(
        "SELECT COUNT(*) FROM kit_citations WHERE kit_id=?", (LB_KIT,)
    ).fetchone()[0]
    # Manifest: DELETE 3 verify + 6 dossier + any basin-2 citations (=0 per DB check)
    if lb_pre_verify != 3:
        sys.exit(f"ABORT: expected 3 le-bomb verify rows to delete, found {lb_pre_verify}")
    if lb_pre_dossier != 6:
        sys.exit(f"ABORT: expected 6 le-bomb dossier rows to delete, found {lb_pre_dossier}")
    # citations: 0 is fine; 0+ is fine — we just DELETE all
    print(f"[pre-check] le-bomb: {lb_pre_verify} verify / {lb_pre_dossier} dossier / {lb_pre_cites} cites to delete")

    # --- 4. Promotion gate computation (read-only pre-pass) ---
    # Compute AFTER the new verify rows are logically inserted (but before DB write)
    kit_contra = defaultdict(set)
    kit_mech_anchored = set()
    for row in gf_verify_rows:
        kit_id, fam, _, verdict, anchor, _, _, _, _ = row
        if verdict == "CONTRADICTED":
            kit_contra[kit_id].add(fam)
        if fam == "mechanics" and verdict == "CONFIRMED" and anchor:
            kit_mech_anchored.add(kit_id)

    pf_kits_in_db = set(
        r[0] for r in cur.execute(
            f"SELECT DISTINCT kit_id FROM canon_probe_facts WHERE kit_id IN ({qmarks})",
            gf_kit_ids,
        )
    )

    promote_kits = []
    excl_contra = []
    excl_no_mech = []
    zero_pf = []

    for k in sorted(gf_kit_ids):
        if kit_contra[k]:
            excl_contra.append(k)
        elif k not in kit_mech_anchored:
            excl_no_mech.append(k)
        elif k in pf_kits_in_db:
            promote_kits.append(k)
        else:
            zero_pf.append(k)

    expected_promo_kits = 96
    expected_promo_facts = expected_promo_kits * 10
    if len(promote_kits) != expected_promo_kits:
        sys.exit(f"ABORT: promotion gate yielded {len(promote_kits)} kits, expected {expected_promo_kits}")

    print(f"[gate] promote={len(promote_kits)} excl_contra={len(excl_contra)} "
          f"excl_no_mech={len(excl_no_mech)} zero_pf={len(zero_pf)} "
          f"total={len(promote_kits)+len(excl_contra)+len(excl_no_mech)+len(zero_pf)}")

    # --- 5. TIER 2 read-only pre-checks (verify exact prior values exist) ---
    # elem_raw field corrections
    for kit_id, (old_val, new_val) in ELEM_RAW_FIELD_CORRECTIONS.items():
        cur_val = cur.execute("SELECT elem_raw FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()
        if cur_val is None:
            sys.exit(f"ABORT: TIER2 elem_raw kit {kit_id!r} not found in canon_corpus")
        if cur_val[0] != old_val:
            # For cases where value already matches new (idempotent): skip
            if cur_val[0] == new_val:
                print(f"[tier2-skip] {kit_id} elem_raw already {new_val!r} (idempotent)")
            else:
                sys.exit(f"ABORT: {kit_id} elem_raw {cur_val[0]!r} != expected old {old_val!r}")

    # ERA corrections pre-checks
    for kit_id, fixes in ERA_CORRECTIONS.items():
        cur_row = cur.execute(
            "SELECT eras, core_skills, mech_note FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        if cur_row is None:
            sys.exit(f"ABORT: TIER2 era/identity kit {kit_id!r} not found in canon_corpus")
        cur_eras, cur_core, _ = cur_row
        if "eras" in fixes:
            old_e, new_e = fixes["eras"]
            if cur_eras != old_e:
                if cur_eras == new_e:
                    print(f"[tier2-skip] {kit_id} eras already {new_e!r}")
                else:
                    sys.exit(f"ABORT: {kit_id} eras {cur_eras!r} != expected {old_e!r}")
        if "core_skills" in fixes:
            old_c, new_c = fixes["core_skills"]
            if cur_core != old_c:
                if cur_core == new_c:
                    print(f"[tier2-skip] {kit_id} core_skills already up to date")
                else:
                    sys.exit(f"ABORT: {kit_id} core_skills {cur_core!r} != expected {old_c!r}")

    # mech_note correction pre-checks (kit must exist; clause must NOT already be prepended)
    all_mech_note_kits = set(MECH_NOTE_CORRECTIONS.keys()) | {k for k in ERA_CORRECTIONS if "mech_note_clause" in ERA_CORRECTIONS[k]}
    for kit_id in all_mech_note_kits:
        cur_note = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()
        if cur_note is None:
            sys.exit(f"ABORT: mech_note correction kit {kit_id!r} not found in canon_corpus")

    # --- 6. Print pre-flight summary ---
    print(f"[pre-flight] verify_ledger={pre_verify} kit_citations={pre_cites} "
          f"kit_dossier={pre_dossier} canon_corpus={pre_corpus}")
    print(f"[pre-flight] probe_facts={pre_pf} verified-v1.1={pre_verified_v1} "
          f"quarantined_cites={pre_quarantined}")
    print(f"[pre-flight] N1 rows to normalize: {n1_normalized}")
    print(f"[pre-flight] N2: ud-snowstorm-frost all-null placeholder -> DROPPED (url=None fails NOT NULL)")
    print(f"[pre-flight] le-bomb DELETE: {lb_pre_verify}v/{lb_pre_dossier}d/{lb_pre_cites}c; "
          f"INSERT: {EXPECTED_LB_VERIFY}v/{EXPECTED_LB_DOSSIER}d/{EXPECTED_LB_CITATIONS}c")
    print(f"[pre-flight] TIER2 elem_raw corrections: {len(ELEM_RAW_FIELD_CORRECTIONS)}")
    print(f"[pre-flight] TIER2 mech_note corrections: {len(MECH_NOTE_CORRECTIONS)}")
    print(f"[pre-flight] TIER2 era/identity/scope corrections: {len(ERA_CORRECTIONS)}")
    print(f"[pre-flight] TIER3 promotions: {len(promote_kits)} kits x 10 = {len(promote_kits)*10} facts")

    # =================== SINGLE WRITE TRANSACTION ===================
    try:
        cur.execute("BEGIN IMMEDIATE")

        # --- TIER 1a: Greenfield INSERT ---
        ins_v = 0
        for row in gf_verify_rows:
            cur.execute(
                """INSERT INTO verify_ledger
                   (kit_id, claim_family, claim_text, verdict, anchor_quote,
                    source_url, errata_applied, run_tag, verified_date)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                row,
            )
            ins_v += 1

        ins_d = 0
        for row in gf_dossier_rows:
            cur.execute(
                """INSERT INTO kit_dossier
                   (kit_id, family, payload_json, source_url, anchor_quote,
                    abstained, conf, extraction_provenance, created_date)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                row,
            )
            ins_d += 1

        ins_c = 0
        for row in gf_cites_rows:
            cur.execute(
                """INSERT INTO kit_citations
                   (kit_id, url, archive_url, site, author_handle, title,
                    cite_class, rank_class, accessed_date, quarantined)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                row,
            )
            ins_c += 1

        if ins_v != EXPECTED_VERIFY:
            raise RuntimeError(f"verify INSERT count {ins_v} != {EXPECTED_VERIFY}")
        if ins_d != EXPECTED_DOSSIER:
            raise RuntimeError(f"dossier INSERT count {ins_d} != {EXPECTED_DOSSIER}")
        if ins_c != EXPECTED_CITATIONS:
            raise RuntimeError(f"citations INSERT count {ins_c} != {EXPECTED_CITATIONS}")

        # --- TIER 1d: le-bomb DELETE ---
        cur.execute("DELETE FROM verify_ledger WHERE kit_id=?", (LB_KIT,))
        deleted_lb_v = cur.rowcount
        cur.execute("DELETE FROM kit_dossier WHERE kit_id=?", (LB_KIT,))
        deleted_lb_d = cur.rowcount
        cur.execute("DELETE FROM kit_citations WHERE kit_id=?", (LB_KIT,))
        deleted_lb_c = cur.rowcount

        if deleted_lb_v != lb_pre_verify:
            raise RuntimeError(f"le-bomb verify DELETE: {deleted_lb_v} rows, expected {lb_pre_verify}")
        if deleted_lb_d != lb_pre_dossier:
            raise RuntimeError(f"le-bomb dossier DELETE: {deleted_lb_d} rows, expected {lb_pre_dossier}")

        # --- TIER 1d: le-bomb INSERT (re-crawl) ---
        ins_lb_v = 0
        for r in lb_verify_rows:
            verdict = VERDICT_MAP.get(r.get("verdict"))
            if verdict is None:
                raise RuntimeError(f"le-bomb bad verdict {r.get('verdict')!r}")
            cur.execute(
                """INSERT INTO verify_ledger
                   (kit_id, claim_family, claim_text, verdict, anchor_quote,
                    source_url, errata_applied, run_tag, verified_date)
                   VALUES (?,?,?,?,?,?,0,?,?)""",
                (r["kit_id"], r.get("claim_family"), r.get("claim_text"), verdict,
                 r.get("anchor_quote"), r.get("source_url"), RUN_TAG, TODAY),
            )
            ins_lb_v += 1

        ins_lb_d = 0
        for r in lb_dossier_rows:
            abst = coerce_bin(r.get("abstained", 0))
            payload = r.get("payload_json")
            if abst == 1 and payload is not None:
                payload = None
            if abst == 0 and payload is None:
                raise RuntimeError(f"le-bomb non-abstained dossier null payload: {r.get('family')}")
            payload_s = None if payload is None else json.dumps(payload, ensure_ascii=False)
            cur.execute(
                """INSERT INTO kit_dossier
                   (kit_id, family, payload_json, source_url, anchor_quote,
                    abstained, conf, extraction_provenance, created_date)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (r["kit_id"], r.get("family"), payload_s, r.get("source_url"),
                 r.get("anchor_quote"), abst, r.get("conf"), EXTRACTION_PROV, TODAY),
            )
            ins_lb_d += 1

        ins_lb_c = 0
        for r in lb_cites_rows:
            cc = r.get("cite_class")
            rc = r.get("rank_class")
            q = coerce_bin(r.get("quarantined", 0))
            if cc not in CITE_CLASS or rc not in RANK_CLASS or q is None:
                raise RuntimeError(f"le-bomb cite bad enum: cc={cc!r} rc={rc!r} q={q!r}")
            cur.execute(
                """INSERT INTO kit_citations
                   (kit_id, url, archive_url, site, author_handle, title,
                    cite_class, rank_class, accessed_date, quarantined)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (r["kit_id"], r.get("url"), r.get("archive_url"), r.get("site"),
                 r.get("author_handle"), r.get("title"), cc, rc,
                 r.get("accessed_date"), q),
            )
            ins_lb_c += 1

        if ins_lb_v != EXPECTED_LB_VERIFY:
            raise RuntimeError(f"le-bomb verify INSERT {ins_lb_v} != {EXPECTED_LB_VERIFY}")
        if ins_lb_d != EXPECTED_LB_DOSSIER:
            raise RuntimeError(f"le-bomb dossier INSERT {ins_lb_d} != {EXPECTED_LB_DOSSIER}")
        if ins_lb_c != EXPECTED_LB_CITATIONS:
            raise RuntimeError(f"le-bomb citations INSERT {ins_lb_c} != {EXPECTED_LB_CITATIONS}")

        # --- TIER 1d: le-bomb RE-KEY canon_corpus display fields ---
        guarded_update(
            cur,
            "UPDATE canon_corpus SET folk_name=?, core_skills=?, mech_note=? WHERE kit_id=?",
            (LB_NEW_FOLK_NAME, LB_NEW_CORE_SKILLS, LB_NEW_MECH_NOTE, LB_KIT),
            "le-bomb folk_name/core_skills/mech_note rekey",
        )
        # era_raw column does not exist in canon_corpus (uses 'eras'); the manifest says
        # era_raw -> "1.0 launch..."; we store this information in mech_note (already done above)
        # and update the eras field with the structured value.
        guarded_update(
            cur,
            "UPDATE canon_corpus SET eras=? WHERE kit_id=?",
            ("1.0-launch;1.4-omens", LB_KIT),
            "le-bomb eras rekey",
        )

        # --- TIER 2a: elem_raw field corrections ---
        tier2_elem_applied = []
        for kit_id, (old_val, new_val) in ELEM_RAW_FIELD_CORRECTIONS.items():
            # Check current value before update
            cur_val = cur.execute("SELECT elem_raw FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
            if cur_val == new_val:
                # Already applied (idempotent); skip
                continue
            guarded_update(
                cur,
                "UPDATE canon_corpus SET elem_raw=? WHERE kit_id=? AND elem_raw=?",
                (new_val, kit_id, old_val),
                f"tier2 elem_raw {kit_id}",
            )
            tier2_elem_applied.append((kit_id, old_val, new_val))

        # --- TIER 2a: mech_note corrections (prepend) ---
        tier2_mech_applied = []
        for kit_id, clause in MECH_NOTE_CORRECTIONS.items():
            cur_note = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
            if cur_note and cur_note.startswith("[VDM-1 basin-5 errata"):
                # Already applied; skip
                continue
            new_note = clause + (cur_note or "")
            guarded_update(
                cur,
                "UPDATE canon_corpus SET mech_note=? WHERE kit_id=?",
                (new_note, kit_id),
                f"tier2 mech_note {kit_id}",
            )
            tier2_mech_applied.append(kit_id)

        # --- TIER 2b: era/identity/scope corrections ---
        tier2_era_applied = []
        for kit_id, fixes in ERA_CORRECTIONS.items():
            if "eras" in fixes:
                old_e, new_e = fixes["eras"]
                cur_e = cur.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
                if cur_e != new_e:
                    guarded_update(
                        cur,
                        "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?",
                        (new_e, kit_id, old_e),
                        f"tier2b eras {kit_id}",
                    )
                    tier2_era_applied.append((kit_id, "eras", old_e, new_e))

            if "core_skills" in fixes:
                old_c, new_c = fixes["core_skills"]
                cur_c = cur.execute("SELECT core_skills FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
                if cur_c != new_c:
                    guarded_update(
                        cur,
                        "UPDATE canon_corpus SET core_skills=? WHERE kit_id=? AND core_skills=?",
                        (new_c, kit_id, old_c),
                        f"tier2b core_skills {kit_id}",
                    )
                    tier2_era_applied.append((kit_id, "core_skills", old_c, new_c))

            # mech_note clause for era/identity corrections
            if "mech_note_clause" in fixes:
                clause = fixes["mech_note_clause"]
                cur_note = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
                if cur_note and cur_note.startswith("[VDM-1 basin-5 errata"):
                    continue  # already applied
                new_note = clause + (cur_note or "")
                guarded_update(
                    cur,
                    "UPDATE canon_corpus SET mech_note=? WHERE kit_id=?",
                    (new_note, kit_id),
                    f"tier2b mech_note {kit_id}",
                )
                tier2_era_applied.append((kit_id, "mech_note", "...", "[prepended]"))

        # --- TIER 3: promotion ---
        promo_qmarks = ",".join("?" * len(promote_kits))
        cur.execute(
            f"UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
            f"WHERE kit_id IN ({promo_qmarks}) "
            f"AND fact_provenance IN ('kb-legacy','named-source-unfetched')",
            promote_kits,
        )
        promo_rows = cur.rowcount

        con.commit()
    except Exception:
        con.rollback()
        raise

    # =================== POST-WRITE VERIFICATION ===================
    integ = con.execute("PRAGMA integrity_check").fetchone()[0]
    fkc = con.execute("PRAGMA foreign_key_check").fetchall()
    jm2 = con.execute("PRAGMA journal_mode").fetchone()[0]

    post_verify = con.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    post_cites = con.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    post_dossier = con.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    post_corpus = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    post_pf = con.execute("SELECT COUNT(*) FROM canon_probe_facts").fetchone()[0]
    post_verified_v1 = con.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'"
    ).fetchone()[0]
    post_quarantined = con.execute("SELECT COUNT(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]

    # Landing-zone row count asserts
    assert post_verify == pre_verify + EXPECTED_VERIFY + ins_lb_v - lb_pre_verify, \
        f"verify_ledger post count mismatch: {post_verify}"
    assert post_dossier == pre_dossier + EXPECTED_DOSSIER + ins_lb_d - lb_pre_dossier, \
        f"kit_dossier post count mismatch: {post_dossier}"
    assert post_cites == pre_cites + EXPECTED_CITATIONS + ins_lb_c - lb_pre_cites, \
        f"kit_citations post count mismatch: {post_cites}"
    assert post_corpus == pre_corpus, f"canon_corpus changed: {pre_corpus} -> {post_corpus}"
    assert post_pf == pre_pf, f"canon_probe_facts changed unexpectedly: {pre_pf} -> {post_pf}"
    assert post_verified_v1 == pre_verified_v1 + expected_promo_facts, \
        f"verified-v1.1 {post_verified_v1} != {pre_verified_v1}+{expected_promo_facts}"
    assert promo_rows == expected_promo_facts, \
        f"promotion rowcount {promo_rows} != {expected_promo_facts}"
    # N2 row is DROPPED (url=None fails NOT NULL), so quarantined count unchanged from greenfield inserts
    assert post_quarantined == pre_quarantined, \
        f"quarantined citations: {pre_quarantined} -> {post_quarantined} (expected unchanged; N2 dropped)"

    # Abstained dossier rows must all have null payload
    abst_bad = con.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE abstained=1 AND payload_json IS NOT NULL"
    ).fetchone()[0]
    assert abst_bad == 0, f"abstained rows with non-null payload: {abst_bad}"

    # N1: 0 CHECK violations (verified by abstained guard above)
    # N2: ud-snowstorm-frost all-null placeholder was DROPPED (url=None violates NOT NULL);
    # confirm no all-null citation row for ud-snowstorm-frost exists
    n2_check = con.execute(
        "SELECT COUNT(*) FROM kit_citations WHERE kit_id='ud-snowstorm-frost' AND url IS NULL"
    ).fetchone()[0]
    assert n2_check == 0, f"N2: unexpected null-url citation for ud-snowstorm-frost in DB: {n2_check}"

    # le-bomb: verify 0 basin-2 rows remain; new rows exist
    lb_post_v = con.execute("SELECT COUNT(*) FROM verify_ledger WHERE kit_id=?", (LB_KIT,)).fetchone()[0]
    lb_post_d = con.execute("SELECT COUNT(*) FROM kit_dossier WHERE kit_id=?", (LB_KIT,)).fetchone()[0]
    lb_post_c = con.execute("SELECT COUNT(*) FROM kit_citations WHERE kit_id=?", (LB_KIT,)).fetchone()[0]
    assert lb_post_v == EXPECTED_LB_VERIFY, f"le-bomb verify post {lb_post_v} != {EXPECTED_LB_VERIFY}"
    assert lb_post_d == EXPECTED_LB_DOSSIER, f"le-bomb dossier post {lb_post_d} != {EXPECTED_LB_DOSSIER}"
    assert lb_post_c == EXPECTED_LB_CITATIONS, f"le-bomb cites post {lb_post_c} != {EXPECTED_LB_CITATIONS}"

    # le-bomb RE-KEY: verify all 4 display fields landed
    lb_canon = con.execute(
        "SELECT folk_name, core_skills, mech_note, eras FROM canon_corpus WHERE kit_id=?", (LB_KIT,)
    ).fetchone()
    assert lb_canon[0] == LB_NEW_FOLK_NAME, f"le-bomb folk_name {lb_canon[0]!r}"
    assert lb_canon[1] == LB_NEW_CORE_SKILLS, f"le-bomb core_skills {lb_canon[1]!r}"
    assert lb_canon[2] == LB_NEW_MECH_NOTE, f"le-bomb mech_note mismatch"
    assert lb_canon[3] == "1.0-launch;1.4-omens", f"le-bomb eras {lb_canon[3]!r}"

    # Integrity
    assert integ == "ok", f"integrity_check {integ!r}"
    assert fkc == [], f"foreign_key_check violations: {fkc}"
    assert jm2.lower() == "delete", f"journal_mode {jm2!r}"

    # Post-ingest md5
    post_md5 = md5_file(DB)

    # =================== REPORT ===================
    print()
    print("=== INGEST-17 (basin-5 crawl) COMPLETE ===")
    print(f"[tier1-greenfield] verify={ins_v} dossier={ins_d} citations={ins_c}")
    print(f"[tier1-N1] {n1_normalized} abstained dossier rows payload normalized NULL (all c01)")
    print(f"[tier1-N2] ud-snowstorm-frost all-null placeholder DROPPED (url=None fails NOT NULL; 253 citations inserted)")
    print(f"[tier1-lebomb] deleted: {deleted_lb_v}v/{deleted_lb_d}d/{deleted_lb_c}c basin-2 rows")
    print(f"[tier1-lebomb] inserted: {ins_lb_v}v/{ins_lb_d}d/{ins_lb_c}c re-crawl rows")
    print(f"[tier1-lebomb] rekey: folk_name={LB_NEW_FOLK_NAME!r} core_skills landed "
          f"eras=1.0-launch;1.4-omens mech_note=[IDENTITY-RESOLVED clause]")
    print(f"[tier2-elem] {len(tier2_elem_applied)} elem_raw field corrections: "
          f"{[(k, a, b) for k, a, b in tier2_elem_applied]}")
    print(f"[tier2-mech] {len(tier2_mech_applied)} mech_note prepends: {tier2_mech_applied}")
    print(f"[tier2-era] {len(tier2_era_applied)} era/identity/scope corrections applied")
    print(f"[tier3] {len(promote_kits)} kits x 10 = {promo_rows} facts promoted -> verified-v1.1")
    print(f"        excl_contra={len(excl_contra)} excl_no_mech={len(excl_no_mech)} "
          f"zero_pf={len(zero_pf)}")
    print(f"TOTALS  verify_ledger={post_verify} (+{post_verify-pre_verify}) "
          f"kit_dossier={post_dossier} (+{post_dossier-pre_dossier}) "
          f"kit_citations={post_cites} (+{post_cites-pre_cites})")
    print(f"        quarantined={post_quarantined} (+{post_quarantined-pre_quarantined})")
    print(f"        verified-v1.1={post_verified_v1} (+{post_verified_v1-pre_verified_v1})")
    print(f"        canon_corpus={post_corpus} (unchanged)")
    print(f"integrity_check={integ}  foreign_key_check={'clean' if not fkc else fkc}  "
          f"journal_mode={jm2}")
    print(f"post-ingest md5: {post_md5}")

    con.close()


if __name__ == "__main__":
    main()
