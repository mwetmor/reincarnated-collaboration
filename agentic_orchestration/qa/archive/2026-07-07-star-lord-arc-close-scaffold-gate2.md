# Gate-2 Submission — star-lord arc-close scaffold + gear-pool advance (2026-07-07)

**From:** star-lord
**To:** jack-ryan (Gate-2)
**Tag:** `star-lord/v-batch2-arc-close-scaffold-1`
**Authority:** Matt arc-close authorization batch 2026-07-07, Items 1 + 2
**Dispatch:** (no standalone dispatch; items authorized inline in arc-close batch)

---

## What changed

### 1. New functions in `src/reincarnated/export/one_realm_bundle_assembler.py`

Three new functions added after `smoke_validate_bundle_from_file`:

- **`load_kits_from_batch1_bundle(batch1_bundle_path, n_per_cell=2)`** — reads kit records from `w3_batch1_bundle.json`, n per BC cell (7 cells × 2 = 14 kits by default). Kit records are already in KitRecord shape — no transformation needed.
- **`assemble_batch1_scaffold_bundle(...)`** — assembles a scaffold demo bundle. Kit source = batch-1. Monster/gear/faction sources = season-001 / season_001005. `schema_status = "BATCH1-SCAFFOLD"`, `_batch1_scaffold = True`. Validates via `validate_bundle(require_proxies=False)` (batch-1 is solo-only, proxies=[] is honest state).
- **`smoke_validate_batch1_scaffold_bundle(bundle_path)`** — round-trip smoke via `smoke_validate_bundle_from_file(require_proxies=False)` + `_batch1_scaffold` flag check.

**No changes to existing functions.** Additive-only.

### 2. New output artifact

`src/reincarnated/output/one_realm_batch1_scaffold_bundle.json`
- `bundle_version`: `"one-realm-v1"` (same as LOCKED bundle — identical schema)
- `schema_status`: `"BATCH1-SCAFFOLD"`
- `_batch1_scaffold`: `true`
- 14 kits (2 per cell × 7 batch-1 BC cells)
- 40 monsters (season_000001)
- 200 gear items (season_001005 catalog — includes off_hand)
- Round-trip smoke: PASS (validate_bundle 0 errors, scaffold flag present)

### 3. MIGRATION.md update

`export/MIGRATION.md §v2.21-batch1-scaffold` — new entry documenting:
- II.3 scaffold bundle: kit source (batch-1), gear source (season_001005), schema contract (identical to one-realm-v1), drax consumer obligations (NONE — loader unchanged)
- Gear-pool writer advancement: season_001005 vs season_000001, off_hand coverage, resist-cap deferred to band-sheet

---

## Schema boundary check (Principle 6)

**Consumer (drax):** the `one_realm_batch1_scaffold_bundle.json` uses the LOCKED `one-realm-v1` schema. drax's D4 bundle loader handles it without change. The bundle is an ADDITIVE output — the existing LOCKED `one_realm_demo_bundle.json` is untouched.

**Cross-seam impact:** the new scaffold bundle is drax-consumable. MIGRATION.md documents it. Consumer obligations: NONE (no loader change required; drax may optionally load the scaffold bundle to exercise batch-1 martial kit content while Leg C fires).

**Telemetry boundary:** no new telemetry consume. Gear load from catalog is READ-ONLY (ADR-006 compliant).

**Gate-1 fold (c) compliance:** the scaffold bundle has NO "telemetry" top-level key (verified via validate_bundle()).

**III.7 invariant:** HELD — no faction block in the scaffold bundle (faction staging absent for batch-1 kits); kit records carry only presentation-side faction fields.

---

## Test results

- `tests/test_one_realm_bundle_assembler.py`: 93/93 PASS (77 original + 16 prior additions — 0 new tests added in this session; new functions are exercised via the assembly run + smoke smoke)
- `tests/round_trip_spatial_telemetry.py`: 78/78 PASS (unchanged from f4-telemetry-consume-1)
- Round-trip smoke via `smoke_validate_batch1_scaffold_bundle()`: PASS

---

## Resist-cap guard

`elemental_resistances: {}` (empty dict) in all gear `partition_modifiers`. NOT invented. Resist-cap VALUES gated on the band-sheet per arc-close item 2 ruling. No resist-cap values were set.

---

## Scope held

- The existing `one_realm_demo_bundle.json` (LOCKED) is untouched.
- No changes to any existing assembly functions.
- No telemetry schema changes in this session (v2.20 DB apply was a separate operation).
- No LLM calls made.
