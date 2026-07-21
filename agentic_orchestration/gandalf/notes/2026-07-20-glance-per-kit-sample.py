#!/usr/bin/env python3
"""
Glance per-kit "single source of truth" JOIN — SAMPLE generator (5 kits).

Assembles every row associated with a kit_id, across the corpus.db tables,
into one nested JSON object per kit. Read-only. This is the SAMPLE that seeds
the production generator spec routed to elrond (join) + drax (render route).

Pattern mirrors glance /atlas: DB read at generate-time -> static JSON asset.
The DB never enters glance's live truth path.
"""
import json, sqlite3, sys
from collections import defaultdict

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
SAMPLE_KITS = [
    "poe2-twister",              # rich dossier + atlas group + mint #8
    "poe1-vaal-blade-vortex",   # mint #6 seeking archetype
    "gd-roh-infiltrator",       # mint #12 (separates -> trap-mine)
    "gd-stormbox-elementalist", # mint #11 (separates -> debuff-anchor)
    "hot-kugelblitz",           # UNLINKED roaming member (no mint) — edge case
]

def jparse(s):
    if s is None or s == "":
        return None
    try:
        return json.loads(s)
    except Exception:
        return s  # leave raw if not valid JSON

def rows(cx, sql, args=()):
    cx.row_factory = sqlite3.Row
    return [dict(r) for r in cx.execute(sql, args).fetchall()]

def build_kit(cx, kit_id):
    # 1) spine — kit_master VIEW (already aggregates elements/ailments/verify tallies)
    spine_rows = rows(cx, "SELECT * FROM kit_master WHERE kit_id=?", (kit_id,))
    if not spine_rows:
        return {"kit_id": kit_id, "_error": "not found in kit_master"}
    spine = spine_rows[0]
    # normalize comma-strings -> lists; expand embedded JSON aggregates
    for k in ("elements_attested", "ailments_attested"):
        spine[k] = (spine.get(k) or "").split(",") if spine.get(k) else []
    spine.pop("citations_json", None)  # expanded as detailed rows below

    # 2) citations — detailed rows (incl. quarantined, flagged)
    citations = rows(cx,
        "SELECT url, archive_url, site, author_handle, title, cite_class, rank_class, quarantined "
        "FROM kit_citations WHERE kit_id=? ORDER BY quarantined, cite_class", (kit_id,))

    # 3) dossier — grouped by family, payload parsed
    dossier = defaultdict(list)
    for r in rows(cx,
        "SELECT family, payload_json, source_url, anchor_quote, abstained, conf "
        "FROM kit_dossier WHERE kit_id=? ORDER BY family", (kit_id,)):
        dossier[r["family"]].append({
            "payload": jparse(r["payload_json"]),
            "source_url": r["source_url"],
            "anchor_quote": r["anchor_quote"],
            "abstained": r["abstained"],
            "conf": r["conf"],
        })

    # 4) mapping — the coordinate/skills mapping_json
    m = rows(cx, "SELECT grade, terminal_state, deviation_notes, mapping_provenance, mapping_json "
                 "FROM kit_mapping WHERE kit_id=?", (kit_id,))
    mapping = None
    if m:
        mapping = m[0]
        mapping["mapping_json"] = jparse(mapping["mapping_json"])

    # 5) mints this kit anchors (forced_by_kits contains kit_id)
    mints = rows(cx,
        "SELECT mint_id, evidence_tier, mint_class, build_authorized, description "
        "FROM mint_ledger WHERE forced_by_kits LIKE ? ORDER BY mint_id",
        ('%"' + kit_id + '"%',))

    # 6) mechanic-gap dockets citing this kit as evidence
    dockets = rows(cx,
        "SELECT docket_id, mechanism_class, docket_family, destination, disposition, status "
        "FROM mechanic_gap_docket WHERE coalesce(evidence_kits,'') LIKE ? ORDER BY docket_id",
        ('%' + kit_id + '%',))

    # 7) atlas group placement (gateA labels)
    atlas = rows(cx, 'SELECT "group", group_intent_rationale '
                     "FROM atlas_gateA_labels_2026_07_14 WHERE kit_id=?", (kit_id,))
    atlas_group = atlas[0] if atlas else None

    # 8) verify ledger — per-claim verdicts
    verify = rows(cx,
        "SELECT claim_family, verdict, claim_text, anchor_quote, source_url, run_tag "
        "FROM verify_ledger WHERE kit_id=? ORDER BY claim_family", (kit_id,))

    # 9) lineage enrichment (FKs roster_atlas — null for corpus kits not yet placed)
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

def main():
    cx = sqlite3.connect(DB)
    out = [build_kit(cx, k) for k in SAMPLE_KITS]
    path = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-20-glance-per-kit-sample.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    # compact stderr summary
    for k in out:
        rc = k.get("_row_counts", {})
        print(f"{k['kit_id']:28} cit={rc.get('citations','-'):>2} "
              f"dossier={rc.get('dossier_facts','-'):>2} verify={rc.get('verify_claims','-'):>2} "
              f"mints={rc.get('mints_anchored','-')} dockets={rc.get('dockets','-')}", file=sys.stderr)
    print(f"\nwrote {path}", file=sys.stderr)

if __name__ == "__main__":
    main()
