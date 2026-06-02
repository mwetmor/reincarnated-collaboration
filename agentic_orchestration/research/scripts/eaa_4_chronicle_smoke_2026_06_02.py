"""
EAA-4 chronicle smoke-test (Discipline #2).

Purpose:
  Verify the kit-space chronicle infrastructure (schema + storage layout +
  FK linkage with EAA-3 per-kit JSON) round-trips cleanly on a single-kit
  expansion event BEFORE EAA-5 first-fire consumes the infrastructure.

Format locks (per joint spec § 1 + § 2):
  - event_id format: kse_<YYYYMMDD>_<seq3>      (within-day monotonic seq)
  - kit_id format:   kit_<primary>_<seq6>       (per-primary monotonic seq)
  - chronicle storage: flat data/kit_space/kit_space_chronicle.json (option α)
  - per-kit JSON: data/kit_space/kits/<kit_id>.json

Joint design spec (authoritative on format + storage):
  agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md

What this script does:
  1. Mints a chronicle event_id per joint spec § 1.3 generation rule
  2. Mints a kit_id per joint spec § 2.4 generation rule (primary=shadow for smoke; smoke-test seq query is by primary)
  3. Appends a chronicle event entry to kit_space_chronicle.json (atomic write)
  4. Writes a per-kit JSON stub carrying matching kit_space_expansion_event_id
  5. Round-trip verifies linkage integrity
  6. Reports PASS / FAIL per check + overall

Usage:
  python eaa_4_chronicle_smoke_2026_06_02.py                # TempDir (CI-safe)
  python eaa_4_chronicle_smoke_2026_06_02.py --live         # write to live engine data/kit_space/
  python eaa_4_chronicle_smoke_2026_06_02.py --cleanup-live # remove smoke kit + event from live dir

Authority: Matt 2026-06-02 + LOCK K (EAA-4 dispatch § 3.4).
Author: elrond (data steward; EAA-4 primary owner).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# --- constants ---------------------------------------------------------------

ENGINE_DATA_KIT_SPACE = Path.home() / "Games" / "reincarnated-engine" / "data" / "kit_space"
EVENT_ID_REGEX = re.compile(r"^kse_\d{8}_\d{3}$")
KIT_ID_REGEX = re.compile(
    r"^kit_(fire|water|earth|wind|lightning|holy|shadow|physical)_\d{6}$"
)
CHRONICLE_SCHEMA_VERSION = "1.0"

# smoke uses a reserved primary slot so it's distinguishable from real kits;
# we use a high seq6 value to avoid colliding with real generation sequences
SMOKE_PRIMARY = "shadow"
SMOKE_SEQ6 = 999001  # reserved for smoke tests; far above any real expected count

# --- id minting (joint spec § 1.3 + § 2.4) -----------------------------------


def mint_event_id(today: datetime, prior_today_count: int) -> str:
    seq = prior_today_count + 1
    return f"kse_{today.strftime('%Y%m%d')}_{seq:03d}"


def mint_kit_id(primary: str, prior_primary_count: int) -> str:
    assert primary in {
        "fire", "water", "earth", "wind", "lightning", "holy", "shadow", "physical"
    }, f"primary {primary!r} not in canonical-7+1"
    seq = prior_primary_count + 1
    return f"kit_{primary}_{seq:06d}"


# --- atomic write ------------------------------------------------------------


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    os.replace(tmp, path)


# --- chronicle handling ------------------------------------------------------


def load_chronicle(chronicle_path: Path) -> dict:
    if chronicle_path.exists():
        with chronicle_path.open() as f:
            return json.load(f)
    return {
        "schema_version": CHRONICLE_SCHEMA_VERSION,
        "schema_notes": (
            "kit-space-expansion chronicle. "
            "Per canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md § 3.4. "
            "Event-type extensible via event_type field."
        ),
        "events": [],
    }


def count_events_today(chronicle: dict, today_date_utc: str) -> int:
    return sum(
        1 for e in chronicle.get("events", [])
        if e.get("event_date_utc") == today_date_utc
    )


def count_kits_for_primary(kits_dir: Path, primary: str) -> int:
    if not kits_dir.exists():
        return 0
    return len(list(kits_dir.glob(f"kit_{primary}_*.json")))


def make_chronicle_event(event_id: str, kit_id: str, now: datetime) -> dict:
    today_date_utc = now.strftime("%Y-%m-%d")
    return {
        "event_id": event_id,
        "event_type": "kit-space-expansion",
        "event_timestamp": now.isoformat().replace("+00:00", "Z"),
        "event_date_utc": today_date_utc,
        "event_scope": "EAA-4 smoke-test (Disc #2) — single-kit chronicle emit + FK linkage verification",
        "substrate_inputs_changed": [
            "smoke-test stub — no substrate change",
        ],
        "engine_version_sha": "smoke00",
        "engine_version_full": None,
        "kit_ids_generated": [kit_id],
        "kit_count": 1,
        "skip_flags_active": ["smoke_test_flag"],
        "lineage_tags": {
            "kit_space_lineage": f"kit-space-expansion-{event_id}",
            "engine_provenance": f"engine-smoke00-{event_id}",
            "substrate_provenance": "smoke-test-stub",
            "generation_cohort_date": today_date_utc,
        },
        "generation_parameters": {
            "n_kits_target": 1,
            "smoke_test": True,
        },
        "substrate_trace_summary": {
            "pool_entries_referenced": 0,
            "smoke_test_note": "no substrate consumed; FK + storage round-trip only",
        },
        "notes": "EAA-4 smoke-test artifact. Safe to remove via --cleanup-live.",
    }


def make_kit_stub(kit_id: str, event_id: str, now: datetime) -> dict:
    """Minimal per-kit JSON stub for FK round-trip verification.

    NOT the EAA-3 authoritative per-kit schema. EAA-3 (rocket primary)
    owns full per-kit field set per joint spec § 4. This stub carries only
    the FK fields necessary for round-trip verification.
    """
    return {
        "_smoke_test_stub": True,
        "_smoke_test_note": "EAA-4 smoke-test stub; NOT the EAA-3 authoritative per-kit schema",
        "schema_version": CHRONICLE_SCHEMA_VERSION,
        "kit_id": kit_id,
        "primary_element": SMOKE_PRIMARY,
        "kit_space_expansion_event_id": event_id,
        "engine_version": "smoke00",
        "generation_timestamp": now.isoformat().replace("+00:00", "Z"),
    }


# --- round-trip verification -------------------------------------------------


def verify_round_trip(
    kit_space_root: Path,
    event_id: str,
    kit_id: str,
) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []

    # 1. event_id regex
    checks.append(
        (
            "event_id regex match",
            bool(EVENT_ID_REGEX.match(event_id)),
            f"event_id={event_id} regex={EVENT_ID_REGEX.pattern}",
        )
    )

    # 2. kit_id regex
    checks.append(
        (
            "kit_id regex match",
            bool(KIT_ID_REGEX.match(kit_id)),
            f"kit_id={kit_id} regex={KIT_ID_REGEX.pattern}",
        )
    )

    # 3. chronicle JSON round-trips
    chronicle_path = kit_space_root / "kit_space_chronicle.json"
    try:
        with chronicle_path.open() as f:
            chronicle = json.load(f)
        checks.append(
            ("chronicle JSON round-trips", True, f"loaded {chronicle_path}; events={len(chronicle.get('events', []))}")
        )
    except Exception as e:
        checks.append(("chronicle JSON round-trips", False, f"FAILED: {e}"))
        return checks

    # 4. chronicle contains our event
    target_event = next(
        (e for e in chronicle.get("events", []) if e.get("event_id") == event_id),
        None,
    )
    checks.append(
        (
            "chronicle contains target event",
            target_event is not None,
            f"event_id={event_id} found={target_event is not None}",
        )
    )
    if target_event is None:
        return checks

    # 5. chronicle event's kit_ids_generated contains kit_id
    checks.append(
        (
            "chronicle event's kit_ids_generated contains kit_id",
            kit_id in target_event.get("kit_ids_generated", []),
            f"kit_ids_generated={target_event.get('kit_ids_generated')}",
        )
    )

    # 6. per-kit JSON exists + round-trips
    kit_path = kit_space_root / "kits" / f"{kit_id}.json"
    try:
        with kit_path.open() as f:
            kit = json.load(f)
        checks.append(("per-kit JSON exists + round-trips", True, f"loaded {kit_path}"))
    except Exception as e:
        checks.append(("per-kit JSON exists + round-trips", False, f"FAILED: {e}"))
        return checks

    # 7. per-kit FK matches chronicle event_id
    fk = kit.get("kit_space_expansion_event_id")
    checks.append(
        (
            "per-kit FK matches chronicle event_id",
            fk == event_id,
            f"kit.kit_space_expansion_event_id={fk!r} chronicle.event_id={event_id!r}",
        )
    )

    # 8. per-kit primary matches kit_id encoding
    primary_in_kit = kit.get("primary_element")
    primary_from_id = kit_id.split("_")[1]
    checks.append(
        (
            "per-kit primary_element matches kit_id encoding",
            primary_in_kit == primary_from_id,
            f"primary_element={primary_in_kit!r} from_id={primary_from_id!r}",
        )
    )

    # 9. chronicle event_date_utc derivable from event_id
    date_from_id = event_id.split("_")[1]
    date_in_event = target_event.get("event_date_utc", "").replace("-", "")
    checks.append(
        (
            "chronicle event_date_utc matches event_id date segment",
            date_from_id == date_in_event,
            f"date_from_id={date_from_id!r} event_date_utc(no-dashes)={date_in_event!r}",
        )
    )

    return checks


# --- main orchestration ------------------------------------------------------


def run_smoke(kit_space_root: Path) -> bool:
    chronicle_path = kit_space_root / "kit_space_chronicle.json"
    kits_dir = kit_space_root / "kits"
    kits_dir.mkdir(parents=True, exist_ok=True)

    # Mint ids per joint spec generation rules
    now = datetime.now(timezone.utc)
    today_date_utc = now.strftime("%Y-%m-%d")
    chronicle = load_chronicle(chronicle_path)
    prior_today = count_events_today(chronicle, today_date_utc)
    event_id = mint_event_id(now, prior_today)

    # For smoke: use reserved high seq6 to avoid colliding with real seqs
    prior_primary = count_kits_for_primary(kits_dir, SMOKE_PRIMARY)
    # If a smoke kit already exists at 999001, bump to 999002, etc.
    kit_seq = max(prior_primary, SMOKE_SEQ6 - 1) + 1
    kit_id = f"kit_{SMOKE_PRIMARY}_{kit_seq:06d}"

    # Per joint spec § 5 emit order: chronicle FIRST, then per-kit JSONs.
    event_entry = make_chronicle_event(event_id, kit_id, now)
    chronicle["events"].append(event_entry)
    chronicle["events"].sort(key=lambda e: e["event_id"])  # lexical = chronological
    atomic_write_json(chronicle_path, chronicle)

    # Then per-kit JSON
    kit_stub = make_kit_stub(kit_id, event_id, now)
    atomic_write_json(kits_dir / f"{kit_id}.json", kit_stub)

    print(f"[emit] event_id           = {event_id}")
    print(f"[emit] kit_id             = {kit_id}")
    print(f"[emit] chronicle          = {chronicle_path}")
    print(f"[emit] kit json           = {kits_dir / f'{kit_id}.json'}")
    print(f"[emit] prior_today_count  = {prior_today} (this is event #{prior_today + 1} today)")
    print(f"[emit] prior_{SMOKE_PRIMARY}_count   = {prior_primary}")
    print()

    checks = verify_round_trip(kit_space_root, event_id, kit_id)
    all_pass = all(p for _, p, _ in checks)

    print("=" * 72)
    print(f"Round-trip checks ({sum(1 for _, p, _ in checks if p)}/{len(checks)} PASS):")
    print("=" * 72)
    for name, passed, detail in checks:
        verdict = "PASS" if passed else "FAIL"
        print(f"  [{verdict}] {name}")
        print(f"         {detail}")

    print()
    print("=" * 72)
    print(f"OVERALL: {'PASS' if all_pass else 'FAIL'}")
    print("=" * 72)
    return all_pass


def cleanup_live() -> int:
    """Remove smoke-test artifacts from the live engine kit_space directory.

    Removes:
      - Any event in kit_space_chronicle.json whose notes start with "EAA-4 smoke-test"
      - Any kit JSON under kits/ matching the smoke kit_id pattern (kit_shadow_999xxx)
    """
    chronicle_path = ENGINE_DATA_KIT_SPACE / "kit_space_chronicle.json"
    kits_dir = ENGINE_DATA_KIT_SPACE / "kits"

    removed_kits = 0
    smoke_event_ids: list[str] = []

    if chronicle_path.exists():
        with chronicle_path.open() as f:
            chronicle = json.load(f)
        before = len(chronicle.get("events", []))
        smoke_events = [
            e for e in chronicle.get("events", [])
            if isinstance(e.get("notes"), str) and e["notes"].startswith("EAA-4 smoke-test")
        ]
        smoke_event_ids = [e["event_id"] for e in smoke_events]
        chronicle["events"] = [
            e for e in chronicle.get("events", []) if e.get("event_id") not in smoke_event_ids
        ]
        if smoke_event_ids:
            atomic_write_json(chronicle_path, chronicle)
            print(f"[cleanup] chronicle events: {before} -> {len(chronicle['events'])} (removed {len(smoke_event_ids)})")
            for eid in smoke_event_ids:
                print(f"[cleanup] removed chronicle event: {eid}")
        else:
            print("[cleanup] no smoke events found in chronicle")

    if kits_dir.exists():
        # smoke kit_ids are kit_shadow_999xxx (the SMOKE_SEQ6 region)
        for f in kits_dir.glob(f"kit_{SMOKE_PRIMARY}_999*.json"):
            try:
                with f.open() as fh:
                    data = json.load(fh)
                if data.get("_smoke_test_stub"):
                    f.unlink()
                    removed_kits += 1
                    print(f"[cleanup] removed kit: {f}")
            except Exception:
                continue

    print(f"[cleanup] removed {removed_kits} kit file(s); removed {len(smoke_event_ids)} chronicle event(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="EAA-4 chronicle smoke-test")
    parser.add_argument(
        "--live",
        action="store_true",
        help=f"Write to live engine data dir ({ENGINE_DATA_KIT_SPACE}) instead of TempDir",
    )
    parser.add_argument(
        "--cleanup-live",
        action="store_true",
        help="Remove smoke-test artifacts from live engine dir and exit",
    )
    args = parser.parse_args()

    if args.cleanup_live:
        return cleanup_live()

    if args.live:
        target = ENGINE_DATA_KIT_SPACE
        print(f"[smoke] writing to LIVE: {target}")
        ok = run_smoke(target)
        return 0 if ok else 1

    with tempfile.TemporaryDirectory(prefix="eaa4_smoke_") as tmpdir:
        target = Path(tmpdir) / "kit_space"
        print(f"[smoke] writing to TempDir: {target}")
        ok = run_smoke(target)
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
