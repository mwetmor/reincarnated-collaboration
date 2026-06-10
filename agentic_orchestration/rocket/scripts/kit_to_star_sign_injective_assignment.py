#!/usr/bin/env python3
"""
kit_to_star_sign_injective_assignment.py — Fable-5 Phase 2 implementer artifact (rocket)

Forward spec (SOLE design input):
  agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md

Deterministic, offline, injective kit -> star-sign assignment (spec schema_version 1.1).
Supersedes the MVP's collision-tolerant per-kit independent draws (v1.0) with
deterministic open addressing (linear probe +1 cyclic) over the eligible pool,
enforcing the Branch A 1:1 binding constraint (spec section 4).

- No network, no LLM, no database — file inputs only (spec section 1.1).
- Pure function of (faction_assignments.json, corpus.yaml, anchor table, SALT,
  flag-level filter sets); only non-deterministic output field is
  generated_at_utc (spec section 5.2 determinism guarantee).
- On ANY validation/assert failure: writes NOTHING, prints failure to stderr,
  exits non-zero (spec section 5.4 step 8).

Python 3.10+; stdlib hashlib/json + PyYAML only (spec section 1.1).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Step 0 — Configuration constants (spec section 5.4 step 0)
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

# Spec section 5.1 — scaffold value (spec section 9); bumping = sanctioned fresh-randomization.
SALT = "kit-to-star-sign-injective-v2-2026-06-10"

# Spec section 2.3 — authoritative canonical anchors, verbatim. Implementation
# supports N rows generically; these 3 are the complete table at authoring time.
ANCHOR_TABLE: list[tuple[str, str, str]] = [
    # (kit_id, star_sign_id, hand_curated_anchor output string — verbatim)
    ("kit_shadow_000007", "vedic-nakshatra-019", "Mula — gandalf doc § 1"),
    ("kit_holy_000005", "vedic-nakshatra-003", "Krittika — gandalf doc § 2"),
    ("kit_physical_000026", "iau-constellations-040-hercules", "Hercules — gandalf doc § 3"),
]

# Spec section 3.2 / 3.3 — named, single-point-of-change flag-level sets.
ELIGIBLE_FLAG_LEVELS = {"none", "low", "medium"}
DEFERRED_FLAG_LEVELS = {"high"}
EXCLUDED_FLAG_LEVELS = {"restricted"}

# Spec section 7.2 — fixed output literals.
SCHEMA_VERSION = "1.1"
ARTIFACT_KIND = "kit_star_sign_assignments"
SPEC_LITERAL = (
    "agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md"
)
PHASE1_DOC_LITERAL = (
    "agentic_orchestration/gandalf/notes/2026-06-09-3-kit-to-star-sign-canonical-mappings.md"
)
SOURCE_CORPUS_LITERAL = (
    "agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml"
)
SOURCE_KIT_LIST_LITERAL = "reincarnated-loadout/public/kit-space/faction_assignments.json"
RANDOM_SEED_METHOD_LITERAL = (
    "sha256(salt + '::' + kit_id)[:16hex] mod "
    "len(eligible_pool_minus_anchor_signs_sorted_by_sign_id), "
    "linear probe +1 cyclic on claimed slots, kits processed in ascending kit_id order"
)


class SpecValidationError(RuntimeError):
    """Raised on any spec section 6 edge-case violation (E1-E11) or post-condition failure."""


def _fail(code: str, msg: str) -> None:
    raise SpecValidationError(f"[{code}] {msg}")


# ---------------------------------------------------------------------------
# Step 1 — Load corpus (E6, E7)
# ---------------------------------------------------------------------------


def load_corpus(path: Path) -> list[dict]:
    try:
        with path.open(encoding="utf-8") as f:
            entries = yaml.safe_load(f)
    except FileNotFoundError:
        _fail("E6", f"corpus.yaml missing at {path}")
    except yaml.YAMLError as exc:
        _fail("E6", f"corpus.yaml unparseable: {exc}")
    if not isinstance(entries, list):
        _fail("E6", f"corpus.yaml root must be a list, got {type(entries).__name__}")
    return entries


def build_sign_index(corpus: list[dict]) -> dict[str, dict]:
    """sign_id -> entry. Duplicate OR missing sign_id is a hard failure (E7; v2: no skip)."""
    index: dict[str, dict] = {}
    for i, entry in enumerate(corpus):
        sid = entry.get("sign_id") if isinstance(entry, dict) else None
        if not sid or not isinstance(sid, str):
            _fail("E7", f"corpus entry at position {i} has missing/invalid sign_id")
        if sid in index:
            _fail("E7", f"duplicate sign_id in corpus: {sid}")
        index[sid] = entry
    return index


# ---------------------------------------------------------------------------
# Step 2 — Load kit list (E4, E5); extraction rule spec section 2.1
# ---------------------------------------------------------------------------


def load_active_kit_ids(path: Path) -> list[str]:
    """K_all = union of all factions[].kit_ids, sorted ascending (ordinal string order)."""
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    kit_ids: list[str] = []
    for faction in data["factions"]:
        kit_ids.extend(faction["kit_ids"])
    seen: set[str] = set()
    for kid in kit_ids:
        if not isinstance(kid, str) or kid == "":
            _fail("E5", f"empty/null/non-string kit_id encountered: {kid!r}")
        if kid in seen:
            _fail("E4", f"duplicate kit_id across/within factions: {kid}")
        seen.add(kid)
    return sorted(kit_ids)  # Python sorted() on str = ordinal codepoint order (no locale)


# ---------------------------------------------------------------------------
# Step 3 — Partition corpus (spec section 3.2; E13: missing/unknown -> DEFERRED)
# ---------------------------------------------------------------------------


def partition_corpus_by_flag_level(
    corpus: list[dict],
) -> tuple[list[dict], list[dict], list[dict]]:
    eligible: list[dict] = []
    deferred: list[dict] = []
    excluded: list[dict] = []
    for entry in corpus:
        cs = entry.get("cultural_sensitivity") or {}
        flag = cs.get("flag_level") if isinstance(cs, dict) else None
        if flag in ELIGIBLE_FLAG_LEVELS:
            eligible.append(entry)
        elif flag in EXCLUDED_FLAG_LEVELS:
            excluded.append(entry)
        elif flag in DEFERRED_FLAG_LEVELS:
            deferred.append(entry)
        else:
            # E13: missing / null / unrecognized -> DEFERRED (never silently include, never fail)
            deferred.append(entry)
    return eligible, deferred, excluded


# ---------------------------------------------------------------------------
# Step 4 — Validate anchors (E8-E11; each fatal)
# ---------------------------------------------------------------------------


def validate_anchors(
    anchors: list[tuple[str, str, str]],
    k_all: list[str],
    sign_index: dict[str, dict],
) -> None:
    k_set = set(k_all)
    seen_kits: set[str] = set()
    seen_signs: set[str] = set()
    for kit_id, sign_id, anchor_str in anchors:
        if kit_id in seen_kits:
            _fail("E11", f"kit appears twice in anchor table: {kit_id}")
        seen_kits.add(kit_id)
        if sign_id in seen_signs:
            _fail("E11", f"two anchors share a sign_id: {sign_id}")
        seen_signs.add(sign_id)
        if kit_id not in k_set:
            _fail("E8", f"anchor kit_id '{kit_id}' ({anchor_str}) not in active kit list (K_all)")
        if sign_id not in sign_index:
            _fail("E9", f"anchor sign_id '{sign_id}' ({anchor_str}) not in corpus")
        cs = (sign_index[sign_id].get("cultural_sensitivity") or {})
        flag = cs.get("flag_level") if isinstance(cs, dict) else None
        if flag not in ELIGIBLE_FLAG_LEVELS:
            _fail(
                "E10",
                f"anchor sign '{sign_id}' ({anchor_str}) has flag_level={flag!r} "
                f"(not in {sorted(ELIGIBLE_FLAG_LEVELS)}). A sensitivity re-flag of an "
                f"anchor sign is a design event, not a data event — surface to gandalf.",
            )


# ---------------------------------------------------------------------------
# Steps 5-6 — Pool build + assignment math (spec sections 5.1, 5.2; E1, E2)
# ---------------------------------------------------------------------------


def base_index(kit_id: str, salt: str, n: int) -> int:
    """h(k) = int(SHA256(UTF8(SALT || '::' || k)).hexdigest()[0:16], 16) mod n.

    Bit-identical to the MVP's deterministic_pick_index; '::' separator is load-bearing.
    """
    digest = hashlib.sha256(f"{salt}::{kit_id}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % n


def assign_injective(
    k_all: list[str],
    anchors: list[tuple[str, str, str]],
    eligible: list[dict],
    sign_index: dict[str, dict],
    salt: str,
) -> list[dict]:
    """Anchors first (HAND_CURATED), then K_rand in ascending order via open addressing.

    Emission order of the returned list is ascending kit_id across ALL kits
    (spec section 7.2), independent of claim-processing order.
    """
    anchor_map = {kit_id: (sign_id, a) for kit_id, sign_id, a in anchors}
    anchor_signs = {sign_id for _, sign_id, _ in anchors}

    # P = sorted eligible sign_ids minus anchor signs (ascending ordinal order); n = |P|
    pool = sorted(e["sign_id"] for e in eligible if e["sign_id"] not in anchor_signs)
    n = len(pool)
    k_rand = [k for k in k_all if k not in anchor_map]  # preserves ascending order

    if n == 0:
        _fail("E2", "empty eligible pool (n = 0) — nothing to assign from")
    if len(k_rand) > n:
        _fail(
            "E1",
            f"more kits than eligible signs: |K_rand| = {len(k_rand)} > n = {n}. "
            f"Injectivity is canon (Branch A 1:1); refusing many-to-one degradation.",
        )

    # Claim pass — anchors are pre-claimed by exclusion from P; C tracks pool claims only.
    claimed: set[str] = set()
    rand_assignment: dict[str, str] = {}
    for kit_id in k_rand:  # ascending kit_id order = the tie-breaking rule (spec section 5.2)
        h = base_index(kit_id, salt, n)
        j = 0
        while pool[(h + j) % n] in claimed:
            j += 1
        sign_id = pool[(h + j) % n]
        claimed.add(sign_id)
        rand_assignment[kit_id] = sign_id

    # Emission records, ascending kit_id (spec section 7.2)
    records: list[dict] = []
    for kit_id in k_all:
        if kit_id in anchor_map:
            sign_id, anchor_str = anchor_map[kit_id]
            method, hand_anchor = "HAND_CURATED", anchor_str
        else:
            sign_id = rand_assignment[kit_id]
            method, hand_anchor = "RANDOM", None
        entry = sign_index[sign_id]
        # E12: missing display denormalizations -> "" (do NOT fail)
        sign_name = (entry.get("sign_name") or {}).get("primary") or ""
        tradition = (entry.get("cultural_tradition") or {}).get("primary_culture") or ""
        records.append(
            {
                "kit_id": kit_id,
                "star_sign_id": sign_id,
                "star_sign_name": sign_name,
                "star_sign_tradition": tradition,
                "star_sign_assignment_method": method,
                "hand_curated_anchor": hand_anchor,
            }
        )
    return records


# ---------------------------------------------------------------------------
# Steps 7-8 — Post-conditions + emission (spec sections 5.4 / 7.2)
# ---------------------------------------------------------------------------


def run(
    corpus_path: Path = CORPUS_YAML,
    faction_path: Path = FACTION_ASSIGNMENTS_JSON,
    output_path: Path = OUTPUT_SIDECAR,
    anchors: list[tuple[str, str, str]] = ANCHOR_TABLE,
    salt: str = SALT,
) -> int:
    """Normative step order per spec section 5.4. Parameterized (defaults = step-0 constants)
    so the spec section 8.1 item-9/10 synthetic hard-fail tests can inject inputs."""
    # 1. Load corpus + index
    corpus = load_corpus(corpus_path)
    sign_index = build_sign_index(corpus)
    print(f"[rocket] corpus entries: {len(corpus)}; indexed sign_ids: {len(sign_index)}")

    # 2. Load kit list
    k_all = load_active_kit_ids(faction_path)
    print(f"[rocket] active kits (K_all): {len(k_all)}")

    # 3. Partition corpus
    eligible, deferred, excluded = partition_corpus_by_flag_level(corpus)
    print(
        f"[rocket] sensitivity audit: eligible={len(eligible)} "
        f"deferred={len(deferred)} excluded={len(excluded)}"
    )

    # 4. Validate anchors
    validate_anchors(anchors, k_all, sign_index)
    print(f"[rocket] anchors validated: {len(anchors)}")

    # 5-6. Pool + assignment (E1/E2 enforced inside)
    assignments = assign_injective(k_all, anchors, eligible, sign_index, salt)
    anchor_signs = {sign_id for _, sign_id, _ in anchors}
    pool_set = {e["sign_id"] for e in eligible} - anchor_signs
    n = len(pool_set)
    print(f"[rocket] random pool n = {n}")

    # 7. Post-conditions (assert -> fail with no output on violation)
    hand = [a for a in assignments if a["star_sign_assignment_method"] == "HAND_CURATED"]
    rand = [a for a in assignments if a["star_sign_assignment_method"] == "RANDOM"]
    if len(assignments) != len(k_all):
        _fail("POST", f"|assignments| = {len(assignments)} != |K_all| = {len(k_all)}")
    if len(hand) != len(anchors):
        _fail("POST", f"HAND_CURATED count {len(hand)} != |A| = {len(anchors)}")
    all_signs = [a["star_sign_id"] for a in assignments]
    if len(set(all_signs)) != len(all_signs):
        dupes = sorted({s for s in all_signs if all_signs.count(s) > 1})
        _fail("POST", f"INJECTIVITY VIOLATION — duplicate star_sign_ids: {dupes}")
    for a in rand:
        if a["star_sign_id"] not in pool_set:
            _fail("POST", f"RANDOM sign {a['star_sign_id']} not in pool P")
    print(f"[rocket] post-conditions OK: HAND_CURATED={len(hand)} RANDOM={len(rand)} "
          f"distinct_signs={len(set(all_signs))}")

    # 8. Emit (spec section 7.2 — exact key order; 2-space indent; ensure_ascii=False; trailing \n)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": ARTIFACT_KIND,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "spec": SPEC_LITERAL,
        "phase1_hand_curation_doc": PHASE1_DOC_LITERAL,
        "source_corpus": SOURCE_CORPUS_LITERAL,
        "source_kit_list": SOURCE_KIT_LIST_LITERAL,
        "methodology": {
            "hand_curated_overrides_count": len(hand),
            "random_assignment_count": len(rand),
            "injectivity": "ENFORCED",
            "random_seed_method": RANDOM_SEED_METHOD_LITERAL,
            "random_seed_salt": salt,
            "cultural_sensitivity_audit": {
                "eligible_pool_size": len(eligible),
                "random_pool_size": n,
                "deferred_for_gandalf_review_count": len(deferred),
                "excluded_count": len(excluded),
                "eligible_flag_levels": sorted(ELIGIBLE_FLAG_LEVELS),
                "deferred_flag_levels": sorted(DEFERRED_FLAG_LEVELS),
                "excluded_flag_levels": sorted(EXCLUDED_FLAG_LEVELS),
            },
        },
        "assignments": assignments,
    }
    serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    with output_path.open("w", encoding="utf-8") as f:
        f.write(serialized)
    print(f"[rocket] sidecar written: {output_path}")
    return 0


def main() -> int:
    try:
        return run()
    except SpecValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # any unexpected failure also: no output, non-zero
        print(f"FAIL (unexpected): {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
