#!/usr/bin/env python3
"""
Glance per-kit "single source of truth" JOIN — PRODUCTION generator (ALL 574 kits).

Productionization of gandalf's seed (`agentic_orchestration/gandalf/notes/
2026-07-20-glance-per-kit-sample.py`), against the FROZEN interface contract
(`2026-07-20-glance-per-kit-sample.json`, Matt-approved 2026-07-20).

Assembles every row associated with a kit_id across corpus.db into one nested JSON
object per kit, plus a small browse/filter index, plus a git-independent provenance
stamp. Read-only. Deterministic. NO LLM, NO network, NO judgment — pure projection
(honors glance's truth-path law: the DB is read at generate-time only, never in the
live truth path).

Pattern mirrors glance /atlas exactly: this Python generator is the UPSTREAM RENDER
(elrond seam), run against corpus.db, emitting a vendored static artifact into the
curated tree. glance's build then byte-copies that artifact into public/kits/
(stage-assets step, drax seam) — glance itself runs no Python and never touches the DB.

OUTPUTS (into --out, default = the vendored curated home):
  index.json                — [{kit_id, folk_name, game, tier, grade, _row_counts}]  (574 rows, browse/filter)
  <kit_id>.json             — the full 10-section object per kit (574 files)
  kits-provenance.json      — corpus.db content-md5 (git-independent SoT id) + repo HEAD
                              + schema-meta version + generate timestamp + emit tallies

SHAPE FIDELITY: emits byte-for-byte the same per-kit shape as the frozen sample. The
ONLY behavioral change from the seed is collision-proof linkage matching — mints and
dockets are matched by JSON-array MEMBERSHIP (json_each) rather than substring LIKE.
This is identical output on every non-colliding kit (all 574 today) and correct-by-
construction on the two latent substring-collision pairs the seed's bare-substring
docket match would misjoin (la-rage-hammer-destroyer ⊂ …-bt ; poe1-arc ⊂ poe1-archmage).

Usage:
    python3 build_glance_per_kit_json_2026_07_20.py           # emit to vendored curated home
    python3 build_glance_per_kit_json_2026_07_20.py --out DIR # emit elsewhere
    python3 build_glance_per_kit_json_2026_07_20.py --stats-only  # census, no file writes
"""
import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone

# --- fixed paths (absolute; agent cwd is not stable) ---
REPO_ROOT = "/Users/admin/Games/reincarnated-collaboration"
DB = os.path.join(REPO_ROOT, "agentic_orchestration/research/curated/corpus.db")
# Vendored upstream-render home (committed; the single source of truth glance stages from).
DEFAULT_OUT = os.path.join(REPO_ROOT, "agentic_orchestration/research/curated/kits-export")

# The canonical atlas gateA label table. Both the dated table and its refit_candidate_1
# sibling carry 86 rows; the dated table is the ratified one (matches the frozen sample).
# Single named constant so a future label re-version is a one-line change.
ATLAS_GATEA_TABLE = "atlas_gateA_labels_2026_07_14"


def jparse(s):
    """Parse a JSON string; None/'' -> None; leave raw if not valid JSON (seed parity)."""
    if s is None or s == "":
        return None
    try:
        return json.loads(s)
    except Exception:
        return s


def rows(cx, sql, args=()):
    cx.row_factory = sqlite3.Row
    return [dict(r) for r in cx.execute(sql, args).fetchall()]


def build_kit(cx, kit_id):
    """Assemble the full 10-section object for one kit. Shape is the FROZEN contract."""
    # 1) spine — kit_master VIEW (aggregates elements/ailments/verify tallies)
    spine_rows = rows(cx, "SELECT * FROM kit_master WHERE kit_id=?", (kit_id,))
    if not spine_rows:
        return {"kit_id": kit_id, "_error": "not found in kit_master"}
    spine = spine_rows[0]
    # normalize comma-strings -> lists (honest empty [] when the source aggregate is empty)
    for k in ("elements_attested", "ailments_attested"):
        spine[k] = (spine.get(k) or "").split(",") if spine.get(k) else []
    spine.pop("citations_json", None)  # expanded as detailed rows below

    # 2) citations — detailed rows (incl. quarantined, flagged; render quarantined distinct)
    citations = rows(
        cx,
        "SELECT url, archive_url, site, author_handle, title, cite_class, rank_class, quarantined "
        "FROM kit_citations WHERE kit_id=? ORDER BY quarantined, cite_class",
        (kit_id,),
    )

    # 3) dossier — grouped by family, payload parsed; abstained rows pass through (source silent)
    dossier = defaultdict(list)
    for r in rows(
        cx,
        "SELECT family, payload_json, source_url, anchor_quote, abstained, conf "
        "FROM kit_dossier WHERE kit_id=? ORDER BY family",
        (kit_id,),
    ):
        dossier[r["family"]].append(
            {
                "payload": jparse(r["payload_json"]),
                "source_url": r["source_url"],
                "anchor_quote": r["anchor_quote"],
                "abstained": r["abstained"],
                "conf": r["conf"],
            }
        )

    # 4) mapping — the coordinate/skills mapping_json
    m = rows(
        cx,
        "SELECT grade, terminal_state, deviation_notes, mapping_provenance, mapping_json "
        "FROM kit_mapping WHERE kit_id=?",
        (kit_id,),
    )
    mapping = None
    if m:
        mapping = m[0]
        mapping["mapping_json"] = jparse(mapping["mapping_json"])

    # 5) mints this kit forced — JSON-ARRAY MEMBERSHIP (collision-proof; see module docstring).
    #    forced_by_kits is a JSON array of kit_ids; json_each explodes it and we match exactly.
    mints = rows(
        cx,
        "SELECT mint_id, evidence_tier, mint_class, build_authorized, description "
        "FROM mint_ledger ml "
        "WHERE EXISTS (SELECT 1 FROM json_each(ml.forced_by_kits) je WHERE je.value=?) "
        "ORDER BY mint_id",
        (kit_id,),
    )

    # 6) mechanic-gap dockets citing this kit as evidence — JSON-ARRAY MEMBERSHIP (collision-proof).
    #    evidence_kits may be NULL/empty; json_each over NULL yields no rows (safe).
    dockets = rows(
        cx,
        "SELECT docket_id, mechanism_class, docket_family, destination, disposition, status "
        "FROM mechanic_gap_docket d "
        "WHERE EXISTS (SELECT 1 FROM json_each(d.evidence_kits) je WHERE je.value=?) "
        "ORDER BY docket_id",
        (kit_id,),
    )

    # 7) atlas group placement (gateA labels) — null for the ~489 kits not yet grouped
    atlas = rows(
        cx,
        f'SELECT "group", group_intent_rationale FROM {ATLAS_GATEA_TABLE} WHERE kit_id=?',
        (kit_id,),
    )
    atlas_group = atlas[0] if atlas else None

    # 8) verify ledger — per-claim verdicts
    verify = rows(
        cx,
        "SELECT claim_family, verdict, claim_text, anchor_quote, source_url, run_tag "
        "FROM verify_ledger WHERE kit_id=? ORDER BY claim_family",
        (kit_id,),
    )

    # 9) lineage enrichment (FKs roster_atlas — null for corpus kits not placed in roster_atlas;
    #    presently EVERY corpus kit is unplaced there, so this is uniformly null — a real
    #    diagnostic signal, passed through honestly, NOT papered over).
    lin = rows(cx, "SELECT * FROM roster_lineage_enrichment WHERE kit_id=?", (kit_id,))
    lineage = lin[0] if lin else None

    return {
        "kit_id": kit_id,
        "spine": spine,
        "mapping": mapping,
        "mints_anchored": mints,
        "dockets": dockets,
        "atlas_group": atlas_group,
        "lineage_enrichment": lineage,
        "citations": citations,
        "verify_ledger": verify,
        "dossier": dossier,
        "_row_counts": {
            "citations": len(citations),
            "dossier_facts": sum(len(v) for v in dossier.values()),
            "verify_claims": len(verify),
            "mints_anchored": len(mints),
            "dockets": len(dockets),
        },
    }


def git_head(root):
    try:
        return (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            or None
        )
    except Exception:
        return None


def file_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def schema_meta_version(cx):
    """Latest corpus_schema_meta version row — a third strong SoT anchor."""
    try:
        r = rows(cx, "SELECT * FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1")
        return r[0] if r else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory (vendored render home)")
    ap.add_argument("--db", default=DB, help="corpus.db path")
    ap.add_argument(
        "--stats-only",
        action="store_true",
        help="print census + gap tallies, write NO files",
    )
    ap.add_argument("--indent", type=int, default=2, help="JSON indent (2 = sample parity)")
    args = ap.parse_args()

    cx = sqlite3.connect(args.db)

    # Universe = kit_master (the 574 mapped combat kits; system/economy kits without a
    # kit_mapping are correctly excluded by the view's INNER JOIN).
    kit_ids = [r["kit_id"] for r in rows(cx, "SELECT kit_id FROM kit_master ORDER BY kit_id")]

    # Build all kits.
    objs = {}
    index = []
    # gap counters (the diagnostic tallies the page is ALSO meant to surface)
    gaps = {
        "empty_mints": 0,
        "null_atlas_group": 0,
        "null_lineage": 0,
        "any_abstained_dossier": 0,
        "empty_elements_attested": 0,
        "empty_ailments_attested": 0,
        "zero_citations": 0,
        "zero_dossier_facts": 0,
        "zero_verify_claims": 0,
        "any_quarantined_citation": 0,
        "null_mapping": 0,
        "grade_GAPPED": 0,
        "has_docket": 0,
        "errors": 0,
    }
    grade_hist = defaultdict(int)
    game_hist = defaultdict(int)
    size_bytes = {}

    for kid in kit_ids:
        obj = build_kit(cx, kid)
        objs[kid] = obj
        if "_error" in obj:
            gaps["errors"] += 1
            continue
        rc = obj["_row_counts"]
        spine = obj["spine"]
        index.append(
            {
                "kit_id": kid,
                "folk_name": spine.get("folk_name"),
                "game": spine.get("game"),
                "tier": spine.get("tier"),
                "grade": spine.get("grade"),
                "_row_counts": rc,
            }
        )
        # gap census
        if rc["mints_anchored"] == 0:
            gaps["empty_mints"] += 1
        if obj["atlas_group"] is None:
            gaps["null_atlas_group"] += 1
        if obj["lineage_enrichment"] is None:
            gaps["null_lineage"] += 1
        if any(row.get("abstained") for fam in obj["dossier"].values() for row in fam):
            gaps["any_abstained_dossier"] += 1
        if not spine.get("elements_attested"):
            gaps["empty_elements_attested"] += 1
        if not spine.get("ailments_attested"):
            gaps["empty_ailments_attested"] += 1
        if rc["citations"] == 0:
            gaps["zero_citations"] += 1
        if rc["dossier_facts"] == 0:
            gaps["zero_dossier_facts"] += 1
        if rc["verify_claims"] == 0:
            gaps["zero_verify_claims"] += 1
        if any(c.get("quarantined") for c in obj["citations"]):
            gaps["any_quarantined_citation"] += 1
        if obj["mapping"] is None:
            gaps["null_mapping"] += 1
        if spine.get("grade") == "GAPPED":
            gaps["grade_GAPPED"] += 1
        if rc["dockets"] > 0:
            gaps["has_docket"] += 1
        grade_hist[spine.get("grade")] += 1
        game_hist[spine.get("game")] += 1

    # measure per-kit serialized size (bytes of the exact bytes we will write)
    for kid, obj in objs.items():
        size_bytes[kid] = len(
            json.dumps(obj, indent=args.indent, ensure_ascii=False).encode("utf-8")
        )

    index_bytes = len(json.dumps(index, indent=args.indent, ensure_ascii=False).encode("utf-8"))
    total_kit_bytes = sum(size_bytes.values())
    sizes_sorted = sorted(size_bytes.values())
    n = len(sizes_sorted)

    def kb(b):
        return b / 1024.0

    def pct(p):
        if n == 0:
            return 0
        return sizes_sorted[min(n - 1, int(round((p / 100.0) * (n - 1))))]

    # top-10 largest kits (pathology watch)
    largest = sorted(size_bytes.items(), key=lambda kv: kv[1], reverse=True)[:10]

    # --- census report to stderr (always) ---
    print(f"=== glance per-kit generator — census over {n} kits (universe: kit_master) ===", file=sys.stderr)
    print(f"index.json:        {kb(index_bytes):8.1f} KB ({index_bytes} bytes)", file=sys.stderr)
    print(f"per-kit total:     {kb(total_kit_bytes):8.1f} KB  ({total_kit_bytes/1024/1024:.2f} MB)", file=sys.stderr)
    print(
        f"per-kit size KB:   min={kb(sizes_sorted[0]):.2f}  p50={kb(pct(50)):.2f}  "
        f"p90={kb(pct(90)):.2f}  p99={kb(pct(99)):.2f}  max={kb(sizes_sorted[-1]):.2f}",
        file=sys.stderr,
    )
    print(f"grade histogram:   {dict(sorted(grade_hist.items(), key=lambda kv: str(kv[0])))}", file=sys.stderr)
    print(f"game histogram:    {dict(sorted(game_hist.items(), key=lambda kv: (-kv[1], str(kv[0]))))}", file=sys.stderr)
    print("gap census (honest-rendering diagnostic):", file=sys.stderr)
    for k in (
        "empty_mints", "null_atlas_group", "null_lineage", "any_abstained_dossier",
        "empty_elements_attested", "empty_ailments_attested", "zero_citations",
        "zero_dossier_facts", "zero_verify_claims", "any_quarantined_citation",
        "null_mapping", "grade_GAPPED", "has_docket", "errors",
    ):
        print(f"    {k:26} {gaps[k]:>4}", file=sys.stderr)
    print("top-10 largest kits (KB):", file=sys.stderr)
    for kid, b in largest:
        print(f"    {kb(b):8.1f}  {kid}", file=sys.stderr)

    if args.stats_only:
        print("\n[stats-only] no files written.", file=sys.stderr)
        return

    # --- write files ---
    out = args.out
    os.makedirs(out, exist_ok=True)

    # index.json
    with open(os.path.join(out, "index.json"), "w") as f:
        json.dump(index, f, indent=args.indent, ensure_ascii=False)

    # per-kit files
    for kid, obj in objs.items():
        with open(os.path.join(out, f"{kid}.json"), "w") as f:
            json.dump(obj, f, indent=args.indent, ensure_ascii=False)

    # provenance stamp — corpus.db is NOT git-tracked, so its CONTENT MD5 is the true,
    # git-independent source-of-truth identity (the atlas render stamps a git commit; we
    # can't, because the DB lives outside git — so we stamp the content hash, which is
    # strictly more honest for an untracked binary).
    meta = schema_meta_version(cx)
    provenance = {
        "generator": "agentic_orchestration/research/scripts/build_glance_per_kit_json_2026_07_20.py",
        "contract": "agentic_orchestration/gandalf/notes/2026-07-20-glance-per-kit-sample.json (FROZEN, Matt-approved 2026-07-20)",
        "derivation": "join(corpus.db) — 10-section per-kit assembly across kit_master + 8 detail tables",
        "source_db_path": "agentic_orchestration/research/curated/corpus.db",
        "source_db_md5": file_md5(args.db),  # git-independent SoT id (DB is untracked)
        "source_db_size_bytes": os.path.getsize(args.db),
        "corpus_schema_meta_version": (meta or {}).get("version") if meta else None,
        "corpus_schema_meta_stamp": (meta or {}).get("applied_utc") if meta else None,
        "repo_head": git_head(REPO_ROOT),  # secondary anchor (meta-repo commit at generate time)
        "atlas_gateA_table": ATLAS_GATEA_TABLE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kit_count": n,
        "index_bytes": index_bytes,
        "per_kit_total_bytes": total_kit_bytes,
        "gap_census": gaps,
        "grade_histogram": dict(grade_hist),
        "game_histogram": dict(game_hist),
        "notes": [
            "NO LLM, NO network, NO judgment — pure projection (glance truth-path law).",
            "Empty sections (mints/atlas/lineage/abstained/elements) pass through as-is: "
            "the page is ALSO a corpus-sparseness diagnostic (see companion recognition note).",
            "Mint/docket linkage matched by JSON-array membership (json_each), not substring "
            "LIKE — collision-proof vs the seed's bare-substring docket match.",
            "lineage_enrichment is uniformly null across the corpus today (roster_lineage_"
            "enrichment FKs roster_atlas, a disjoint kit universe) — a real diagnostic, not a bug.",
        ],
    }
    with open(os.path.join(out, "kits-provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2, ensure_ascii=False)

    print(
        f"\nwrote {n} per-kit files + index.json + kits-provenance.json -> {out}",
        file=sys.stderr,
    )
    print(f"corpus.db md5 = {provenance['source_db_md5']}", file=sys.stderr)


if __name__ == "__main__":
    main()
