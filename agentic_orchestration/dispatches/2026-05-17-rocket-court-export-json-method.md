# 2026-05-17 — rocket — Court.export_json() method for loadout consumption

**Authority:** Matt L3 standing delegation (sign-off pillar — "always toward Phase-1 completion"); drax-loadout QUESTION → rocket per D17 ship.
**Type:** Pattern A (short task) — ~0.5 day.
**Predecessor:** drax-loadout D17 Court browser surface shipped (`drax/v1.0-d17-court-browser-surface-1` @ `9430a35`); drax filed QUESTION → rocket explicitly.
**Status:** QUEUED — auto-spawn after rocket v1.9 perception_asymmetry ships.

---

## Why this matters

Drax-loadout shipped the D17 Court browser. UI is fully functional but **renders empty state until rocket adds a JSON export step.** Without this dispatch, the Court browser is permanently dark; with this dispatch, the player's accumulated Court of Forms surfaces in loadout.

Per Matt's pillar "always toward Phase-1 completion": this is the unlock that makes the Court visible. Critical-path.

Drax-loadout chose **Path A (static JSON export)** as the data-flow architecture (per gandalf D17 dispatch options A/B/C). Rocket adds the export step to `court_persistence.py`.

---

## Required reading (in order)

1. `reincarnated-engine/src/reincarnated/foundation/court_persistence.py` — your prior D17 ship; existing `list_forms()` returns dataclasses; no `export_json()` yet
2. `reincarnated-loadout/MIGRATION.md` §v1.2 — drax-loadout's full spec for the JSON shape; CourtForm / CourtSkill / CourtVisualSignature / CourtExport schemas mirror your Python dataclasses
3. `reincarnated-loadout/src/data/courtTypes.ts` — drax-loadout's TypeScript types (mirror of your Python schema)
4. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — drax-loadout D17 STATE + QUESTION → rocket

---

## Scope

### Item 1 — Add `Court.export_json(earth_self_id, output_path)` method

Per drax-loadout MIGRATION.md §v1.2 spec, the method should:

- Accept `earth_self_id` (the player's persistent identity) and `output_path` (where to write the JSON)
- Query the SQLite DB for all Court forms belonging to the earth_self_id
- Serialize each Court form per the TypeScript schema drax-loadout authored (CourtForm with nested CourtSkill[] + CourtVisualSignature)
- Wrap in CourtExport envelope: `{ "schema_version": "1.0", "earth_self_id": "...", "exported_at": "...ISO8601...", "forms": [...] }`
- Write JSON to `output_path` atomically (write to temp + rename to avoid partial-write reads)

### Item 2 — Cross-language schema parity

The TypeScript schema in `reincarnated-loadout/src/data/courtTypes.ts` is the authoritative shape; your Python serialization must match it field-by-field:

- `CourtForm`: form_id, form_name, season_number, season_id, archetype, substrate, role, class_role_function, iconic_skill, path_taken, court_resonance, ascended_at (ISO timestamp), is_recent (boolean for N=5 indicator), visual_signature (nested CourtVisualSignature), skills (nested array of CourtSkill)
- `CourtSkill`: skill_id, skill_name, geometry_type, canonical_element, role, cooldown_seconds, flavor_text
- `CourtVisualSignature`: thumbnail_substrate, thumbnail_path_override (optional)

Field names + types in Python serialization must match TypeScript exactly. If your existing dataclasses don't have all these fields, propose schema extensions OR document gaps in MIGRATION.md.

**Discipline #11 attribution:** include `engine_version` or `engine_git_sha` in the CourtExport envelope so loadout can correlate exports across engine versions.

### Item 3 — Auto-export trigger

When does the export fire? Options:

- **A. On Court mutation:** export fires whenever a Court form is ascended/changed (engine-side). Loadout always sees fresh.
- **B. On season generation:** export fires at end of each gamora regen. Loadout sees post-regen state.
- **C. CLI command:** `reincarnated-engine export-court <earth-self-id>` — explicit invocation. Loadout sees on-demand.

**Recommended:** A (on Court mutation) — simplest user-facing flow; loadout always reflects engine truth.

If A is complex (e.g., requires hook into many call sites), fall back to B (export at season end; happens often enough that loadout stays fresh in practice).

### Item 4 — Default output path

Drax-loadout's empty-state bootstrap is at `reincarnated-loadout/public/data/court.json`. Two options for the engine-side write target:

- **A. Write directly to loadout public/data/court.json:** simplest; loadout reads its own filesystem path
- **B. Write to `~/.config/reincarnated/court_export.json`:** engine writes to a user-config location; loadout reads from that location (requires loadout webapp to know the path, possibly via env var or build constant)

**Recommended:** A — write directly to loadout's public/data path. Both repos are sibling directories; the engine can compute the path:

```python
DEFAULT_EXPORT_PATH = Path("../reincarnated-loadout/public/data/court.json")  # relative to engine repo root
```

OR make the path configurable via parameter / env var.

### Item 5 — Tests + MIGRATION

- Unit test: export creates valid JSON matching TypeScript schema
- Unit test: empty Court exports valid empty CourtExport envelope (loadout's empty-state path)
- Unit test: trigger A (on Court mutation) fires correctly
- `foundation/MIGRATION.md` entry documenting:
  - New method + cross-language schema parity
  - Default output path decision (A vs B above)
  - Trigger decision (A/B/C above)
  - Discipline #11 attribution (engine_version/sha in envelope)

### Item 6 — Hive log + tag

- STATE entry documenting export_json shipped
- HANDOFF → drax-loadout (their Court browser now populates; verify with their existing empty-state-to-populated transition)
- Tag `rocket/v1.10-court-export-json-method-1` (or whichever next-available rocket version after v1.9 perception_asymmetry)

---

## Out of scope (DO NOT)

- ❌ DO NOT modify drax-loadout's TypeScript schema (consume + match it)
- ❌ DO NOT add Court write/edit functionality (read-only export only)
- ❌ DO NOT modify the rest of court_persistence.py beyond adding the method
- ❌ DO NOT change earth-self identity persistence
- ❌ DO NOT touch demo or loadout files (export-only side)
- ❌ DO NOT extend scope to other foundation features

---

## Acceptance criteria

- [ ] `Court.export_json(earth_self_id, output_path)` method authored
- [ ] Cross-language schema parity with `reincarnated-loadout/src/data/courtTypes.ts`
- [ ] Atomic write (temp + rename)
- [ ] Discipline #11 attribution: engine_version/sha in envelope
- [ ] Trigger mechanism decided + implemented (A/B/C; recommend A)
- [ ] Default output path decided (recommend Path A — write to loadout/public/data/court.json)
- [ ] Unit tests added (3+ tests)
- [ ] `foundation/MIGRATION.md` entry authored
- [ ] Hive-log STATE + HANDOFF → drax-loadout
- [ ] Tag `rocket/v1.10-court-export-json-method-1`

---

## Smoke test expectation

- `python -c "from reincarnated.foundation import Court; c = Court(...); c.export_json('test-earth-self', '/tmp/court.json')"` writes valid JSON
- Output JSON loads cleanly in loadout (drax-loadout's `useCourtData()` hook deserializes without error)
- Drax-loadout's Court browser transitions from empty state to populated state on next page load

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. Pull-rebase before engine commits.

---

*Queued 2026-05-17 by knight-rider per Matt sign-off pillar + drax-loadout QUESTION. Spawn after rocket v1.9 ships. Estimated 0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `rocket/v1.10-court-export-json-method-1`
**Commits:** `1f3585c` (feat), `b77e5f0` (AGENT_STATE)

### Acceptance criteria — all satisfied

- [x] `Court.export_json(earth_self_id, output_path)` method authored
- [x] Cross-language schema parity with `reincarnated-loadout/src/data/courtTypes.ts`
- [x] Atomic write (temp + rename via `os.replace`)
- [x] Discipline #11 attribution: `engine_git_sha` in envelope (`_get_engine_git_sha()` inline)
- [x] Trigger mechanism: **Option A** (on Court mutation via `export_earth_self_id` constructor param)
- [x] Default output path: **Path A** (`DEFAULT_COURT_EXPORT_PATH` → loadout `public/data/court.json`)
- [x] Unit tests: 7 new tests (50 total, all GREEN)
- [x] `foundation/MIGRATION.md §v1.10` entry authored
- [x] Hive-log PRE-SIGNAL + STATE + HANDOFF → drax-loadout
- [x] Tag `rocket/v1.10-court-export-json-method-1`

### Key decisions

| Decision | Choice | Rationale |
|---|---|---|
| Trigger | Option A (on mutation) | Auto-export via `export_earth_self_id` constructor param; zero extra call sites for the caller |
| Output path | Path A (loadout public/data) | Both repos sibling dirs; `DEFAULT_COURT_EXPORT_PATH` computed at import time |
| Atomic write | temp + `os.replace` | POSIX-atomic; no partial-file reads in `useCourtData()` |
| engine_git_sha | Inline subprocess | Avoids cross-seam telemetry import; same pattern as `telemetry/db.py` |

### Schema note

TypeScript `CourtExport` interface does not declare `engine_git_sha` — it is an additive field TS silently ignores. Drax may optionally add `engine_git_sha?: string` to the interface to surface it in the UI.
