#!/usr/bin/env python3
"""
kit_to_star_sign_mvp_assignment.py — Phase 2 of elrond kit-to-star-sign MVP commission

Commission: agentic_orchestration/dispatches/2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md
Phase 1 input: agentic_orchestration/gandalf/notes/2026-06-09-3-kit-to-star-sign-canonical-mappings.md
Corpus input: agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml
Kit list input: reincarnated-loadout/public/kit-space/faction_assignments.json (37 active kits)

Output: reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json
        (parallel sidecar artifact to faction_assignments.json; consumed by drax /forge)

Methodology (per dispatch § 3.3):
- 3 hand-curated overrides per gandalf Phase 1 doc (kit_shadow_000007 → Mula;
  kit_holy_000005 → Krittika; kit_physical_000026 → Hercules)
- Rest random-assigned uniformly from filtered Legolas corpus pool
- Filter: exclude cultural_sensitivity.flag_level == "high" (defer to gandalf review per
  dispatch § 3.4); none/low/medium eligible
- Random seed: deterministic per-kit (hash(kit_id + fixed_salt)) for reproducibility

Engineering disciplines invoked:
- #11 empirical inspection over assumption — entry counts verified pre/post
- #20 robots.txt / source-cleanliness — inherited from Legolas crawl (clean)
- #25 semantic-layer rep-audit — hand-curation IS rep-audit at per-kit layer;
  flag_level filter IS rep-audit at corpus pool layer
- #40 scaffold-with-pending-decision — random-assignment scaffolded;
  Cycle 15+ Pattern B replaces with canonical semantic mapping
- #41 substrate-led — no pre-imposed weighting on random pool;
  uniform random is honest about absent semantic methodology

No LLM at runtime (D7 AI-tell line preserved).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT_META = Path("/Users/admin/Games/reincarnated-collaboration")
REPO_ROOT_LOADOUT = Path("/Users/admin/Games/reincarnated-loadout")

CORPUS_YAML = (
    REPO_ROOT_META
    / "agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml"
)
FACTION_ASSIGNMENTS_JSON = (
    REPO_ROOT_LOADOUT / "public/kit-space/faction_assignments.json"
)
OUTPUT_SIDECAR = (
    REPO_ROOT_LOADOUT / "public/kit-space/kit_star_sign_assignments.json"
)

# Fixed salt — locks deterministic reproducibility across re-runs.
# Bump this constant only if a fresh-randomization pass is intentionally desired
# (Discipline #40 scaffold flag; revisit in Cycle 15+ Pattern B if needed).
RANDOM_SEED_SALT = "kit-to-star-sign-mvp-2026-06-09"

# Hand-curated overrides — sourced verbatim from gandalf Phase 1 doc § 6.
HAND_CURATED_OVERRIDES: list[tuple[str, str, str]] = [
    # (kit_id, star_sign_id, gandalf-doc § anchor)
    ("kit_shadow_000007", "vedic-nakshatra-019", "Mula — gandalf doc § 1"),
    ("kit_holy_000005", "vedic-nakshatra-003", "Krittika — gandalf doc § 2"),
    ("kit_physical_000026", "iau-constellations-040-hercules", "Hercules — gandalf doc § 3"),
]

# Cultural-sensitivity filter policy — dispatch § 3.4.
ELIGIBLE_FLAG_LEVELS = {"none", "low", "medium"}
# "high" → excluded from random pool (deferred to gandalf review)
# "restricted" → excluded (substrate-cleanliness > volume)
DEFERRED_FLAG_LEVELS = {"high"}
EXCLUDED_FLAG_LEVELS = {"restricted"}


# ---------------------------------------------------------------------------
# Substrate loading
# ---------------------------------------------------------------------------


def load_corpus(path: Path) -> list[dict]:
    """Load Legolas 423-entry zodiac corpus."""
    with path.open() as f:
        entries = yaml.safe_load(f)
    if not isinstance(entries, list):
        raise RuntimeError(f"Expected list at corpus root, got {type(entries).__name__}")
    return entries


def load_active_kit_ids(faction_path: Path) -> list[str]:
    """Extract the 37-kit active corpus from faction_assignments.json."""
    with faction_path.open() as f:
        data = json.load(f)
    kit_ids: list[str] = []
    for faction in data["factions"]:
        kit_ids.extend(faction["kit_ids"])
    return sorted(kit_ids)


# ---------------------------------------------------------------------------
# Cultural-sensitivity audit (Discipline #25 corpus-pool rep-audit)
# ---------------------------------------------------------------------------


def partition_corpus_by_flag_level(
    corpus: list[dict],
) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (eligible, deferred, excluded) entries per cultural_sensitivity flag.

    Per dispatch § 3.4:
      - none / low / medium → eligible for random pool
      - high → deferred (gandalf review required before inclusion)
      - restricted → excluded (substrate-cleanliness gate)
    Entries with missing/unknown flag are treated as deferred (conservative default).
    """
    eligible: list[dict] = []
    deferred: list[dict] = []
    excluded: list[dict] = []
    for entry in corpus:
        cs = entry.get("cultural_sensitivity") or {}
        flag = cs.get("flag_level") if isinstance(cs, dict) else None
        if flag in ELIGIBLE_FLAG_LEVELS:
            eligible.append(entry)
        elif flag in DEFERRED_FLAG_LEVELS:
            deferred.append(entry)
        elif flag in EXCLUDED_FLAG_LEVELS:
            excluded.append(entry)
        else:
            # Missing or unrecognized — conservative: defer (don't silently include)
            deferred.append(entry)
    return eligible, deferred, excluded


# ---------------------------------------------------------------------------
# Anchor validation — Discipline #11 (empirical inspection before assignment)
# ---------------------------------------------------------------------------


def build_sign_index(corpus: list[dict]) -> dict[str, dict]:
    """Index corpus by sign_id for O(1) lookup."""
    index: dict[str, dict] = {}
    for entry in corpus:
        sid = entry.get("sign_id")
        if not sid:
            continue
        if sid in index:
            raise RuntimeError(f"Duplicate sign_id in corpus: {sid}")
        index[sid] = entry
    return index


def validate_overrides(
    overrides: list[tuple[str, str, str]],
    active_kit_ids: list[str],
    sign_index: dict[str, dict],
) -> None:
    """Pre-flight: every override kit_id is in active corpus; every star_sign_id resolves."""
    active_set = set(active_kit_ids)
    for kit_id, star_sign_id, anchor in overrides:
        if kit_id not in active_set:
            raise RuntimeError(
                f"Hand-curated kit_id '{kit_id}' ({anchor}) not in active 37-kit corpus."
            )
        if star_sign_id not in sign_index:
            raise RuntimeError(
                f"Hand-curated star_sign_id '{star_sign_id}' ({anchor}) not in Legolas corpus."
            )
        # Spot-check cultural_sensitivity is clean for anchors
        cs = (sign_index[star_sign_id].get("cultural_sensitivity") or {}).get("flag_level")
        if cs not in ELIGIBLE_FLAG_LEVELS:
            raise RuntimeError(
                f"Hand-curated star_sign '{star_sign_id}' has flag_level='{cs}' "
                f"(expected none/low/medium). Surface to gandalf before proceeding."
            )


# ---------------------------------------------------------------------------
# Deterministic random assignment
# ---------------------------------------------------------------------------


def deterministic_pick_index(kit_id: str, salt: str, pool_size: int) -> int:
    """Deterministically map kit_id → index in eligible-corpus pool.

    Uses SHA-256 truncated to 64 bits, then modulo pool_size. The salt allows a
    fresh-randomization pass to be requested by bumping the salt constant.
    """
    digest = hashlib.sha256(f"{salt}::{kit_id}".encode("utf-8")).hexdigest()
    seed_int = int(digest[:16], 16)
    return seed_int % pool_size


def assign_star_signs(
    active_kit_ids: list[str],
    overrides: list[tuple[str, str, str]],
    eligible_pool: list[dict],
    sign_index: dict[str, dict],
    salt: str,
) -> list[dict]:
    """Produce per-kit assignment records.

    Returns list of dicts with shape:
      {
        kit_id: str,
        star_sign_id: str,
        star_sign_name: str,
        star_sign_tradition: str,
        star_sign_assignment_method: "HAND_CURATED" | "RANDOM",
        hand_curated_anchor: str | None,
      }
    """
    override_map = {kit_id: (sid, anchor) for kit_id, sid, anchor in overrides}
    # Sort eligible pool by sign_id for deterministic indexing across re-runs.
    pool_sorted = sorted(eligible_pool, key=lambda e: e["sign_id"])
    pool_size = len(pool_sorted)
    if pool_size == 0:
        raise RuntimeError("Eligible random pool is empty.")

    assignments: list[dict] = []
    for kit_id in active_kit_ids:
        if kit_id in override_map:
            star_sign_id, anchor = override_map[kit_id]
            method = "HAND_CURATED"
            hand_anchor = anchor
        else:
            idx = deterministic_pick_index(kit_id, salt, pool_size)
            star_sign_id = pool_sorted[idx]["sign_id"]
            method = "RANDOM"
            hand_anchor = None

        entry = sign_index[star_sign_id]
        sign_name = (entry.get("sign_name") or {}).get("primary", "")
        tradition = (entry.get("cultural_tradition") or {}).get("primary_culture", "")

        assignments.append(
            {
                "kit_id": kit_id,
                "star_sign_id": star_sign_id,
                "star_sign_name": sign_name,
                "star_sign_tradition": tradition,
                "star_sign_assignment_method": method,
                "hand_curated_anchor": hand_anchor,
            }
        )
    return assignments


# ---------------------------------------------------------------------------
# Output emission
# ---------------------------------------------------------------------------


def emit_sidecar(
    out_path: Path,
    assignments: list[dict],
    eligible_count: int,
    deferred_count: int,
    excluded_count: int,
    corpus_path: Path,
    faction_path: Path,
    salt: str,
) -> None:
    payload = {
        "schema_version": "1.0",
        "artifact_kind": "kit_star_sign_assignments",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "commission": "agentic_orchestration/dispatches/2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md",
        "phase1_hand_curation_doc": "agentic_orchestration/gandalf/notes/2026-06-09-3-kit-to-star-sign-canonical-mappings.md",
        "source_corpus": str(corpus_path.relative_to(REPO_ROOT_META)),
        "source_kit_list": "reincarnated-loadout/public/kit-space/faction_assignments.json",
        "methodology": {
            "hand_curated_overrides_count": sum(
                1 for a in assignments if a["star_sign_assignment_method"] == "HAND_CURATED"
            ),
            "random_assignment_count": sum(
                1 for a in assignments if a["star_sign_assignment_method"] == "RANDOM"
            ),
            "random_seed_method": "sha256(salt + kit_id) mod len(eligible_pool_sorted_by_sign_id)",
            "random_seed_salt": salt,
            "cultural_sensitivity_audit": {
                "eligible_pool_size": eligible_count,
                "deferred_for_gandalf_review_count": deferred_count,
                "excluded_count": excluded_count,
                "eligible_flag_levels": sorted(ELIGIBLE_FLAG_LEVELS),
                "deferred_flag_levels": sorted(DEFERRED_FLAG_LEVELS),
                "excluded_flag_levels": sorted(EXCLUDED_FLAG_LEVELS),
            },
        },
        "assignments": assignments,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print(f"[elrond] Loading Legolas corpus from: {CORPUS_YAML}")
    corpus = load_corpus(CORPUS_YAML)
    print(f"[elrond] Corpus entries: {len(corpus)}")

    print(f"[elrond] Loading active 37-kit list from: {FACTION_ASSIGNMENTS_JSON}")
    active_kit_ids = load_active_kit_ids(FACTION_ASSIGNMENTS_JSON)
    print(f"[elrond] Active kits: {len(active_kit_ids)}")

    sign_index = build_sign_index(corpus)
    print(f"[elrond] Indexed sign_ids: {len(sign_index)}")

    eligible, deferred, excluded = partition_corpus_by_flag_level(corpus)
    print(
        f"[elrond] Cultural-sensitivity audit: "
        f"eligible={len(eligible)} deferred={len(deferred)} excluded={len(excluded)}"
    )

    print("[elrond] Validating hand-curated overrides...")
    validate_overrides(HAND_CURATED_OVERRIDES, active_kit_ids, sign_index)
    print(f"[elrond] Overrides validated: {len(HAND_CURATED_OVERRIDES)} mappings")

    assignments = assign_star_signs(
        active_kit_ids=active_kit_ids,
        overrides=HAND_CURATED_OVERRIDES,
        eligible_pool=eligible,
        sign_index=sign_index,
        salt=RANDOM_SEED_SALT,
    )

    # Discipline #11: post-condition checks
    hand_count = sum(1 for a in assignments if a["star_sign_assignment_method"] == "HAND_CURATED")
    rand_count = sum(1 for a in assignments if a["star_sign_assignment_method"] == "RANDOM")
    assert hand_count == len(HAND_CURATED_OVERRIDES), \
        f"Expected {len(HAND_CURATED_OVERRIDES)} HAND_CURATED, got {hand_count}"
    assert hand_count + rand_count == len(active_kit_ids), \
        "Method-count sum != active-kit count"
    print(f"[elrond] Assignments: HAND_CURATED={hand_count} RANDOM={rand_count}")

    print(f"[elrond] Emitting sidecar: {OUTPUT_SIDECAR}")
    emit_sidecar(
        out_path=OUTPUT_SIDECAR,
        assignments=assignments,
        eligible_count=len(eligible),
        deferred_count=len(deferred),
        excluded_count=len(excluded),
        corpus_path=CORPUS_YAML,
        faction_path=FACTION_ASSIGNMENTS_JSON,
        salt=RANDOM_SEED_SALT,
    )
    print("[elrond] Sidecar written. Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
