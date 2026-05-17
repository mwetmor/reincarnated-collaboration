# Dispatch — 2026-05-16 — star-lord — V2.4 telemetry migration: `modifier_flag_tier` column on `class_balance_results`

**From:** knight-rider (authored per gamora modifier-clamp gate completion cross-seam flag 2026-05-16; flagged-but-not-authored loop-close per star-lord Stage 2 completion report)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 (small Pattern A; ADR-006 standard process)
**Status:** PENDING — ACTIVE (your Stage 2 just returned; this is the next item in your chain)
**Estimated effort:** 1 session (~2-3h); small schema migration + recorder wiring + defensive null + MIGRATION.md entry; standard v2.x pattern.
**Acceptance:** Telemetry schema v2.4 migration adds `modifier_flag_tier TEXT NULL` column to `class_balance_results` table; recorder wired to read `getattr(result, "modifier_flag_tier", None)` defensively; smoke test verifies persistence + defensive NULL handling; MIGRATION.md v2.4 entry per ADR-004; intermediate tag.

---

## Why this dispatch exists

Per gamora modifier-clamp gate completion (`gamora/v1.3-modifier-clamp-gate` tag) MIGRATION.md §v1.6:

> Star-lord cross-seam flag (MEDIUM PRIORITY): MIGRATION.md §v1.6 documents the required V2.4 telemetry migration — add `modifier_flag_tier TEXT NULL` to `class_balance_results` table; recorder reads `getattr(result, "modifier_flag_tier", None)` defensively. Historical rows get NULL. Separate star-lord dispatch required.

Closes the modifier-clamp gate cross-seam contract. Once landed, the gate's `modifier_flag_tier="review"` flag persists per-class to telemetry for downstream analysis (jack-ryan calibration analysis; modifier-anomaly trend detection across regens).

## What this dispatch does (v2.4 telemetry migration)

Following the pattern from your v2.1 + v2.2 + v2.3 schema work:

### Step 1 — Schema addition (v2.4 telemetry migration)

Append a new migration entry to `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (v2.4):

**class_balance_results** (per-class balance loop outcomes):

```sql
ALTER TABLE class_balance_results ADD COLUMN modifier_flag_tier TEXT NULL;
```

NULL-permitting (consistent with v2.x pattern; historical rows carry NULL; fresh rows carry actual values when the modifier-clamp gate flags them).

**Field semantics**:
- `modifier_flag_tier: str | None` — modifier-clamp gate tier classification
- Current values: `"review"` (set when `final_modifier > MODIFIER_REVIEW_FLAG_THRESHOLD` (3.0))
- NULL for normal-range modifiers (no flag triggered)
- Future tiers could include `"clamp"` / `"reject"` if gate evolves (NOT in scope here; field accepts arbitrary TEXT)

### Step 2 — Recorder wiring

Update `recorder.py` (or whichever module owns `record_class_balance_results`):

- Accept `modifier_flag_tier` from the ClassBalanceResult object via `getattr(result, "modifier_flag_tier", None)` (defensive: gracefully handles pre-modifier-clamp-gate result objects that lack the attribute)
- Write to the INSERT statement
- Per R11(d) recorder fail-loud discipline: if any required field is None unexpectedly, use the established skip-counter + WARN-log pattern (don't silently drop)

### Step 3 — Smoke test

Per Discipline #2:
- Existing tests in `tests/test_telemetry.py` pass
- New unit test for v2.4 migration + recorder wiring
- Smoke: a small balance loop with one class triggering the gate (per gamora smoke pattern) → recorder writes `"review"` to the new column for that class
- Defensive-null smoke: a class WITHOUT modifier_flag_tier attribute (pre-fix simulation) → recorder writes NULL; no error

### Step 4 — MIGRATION.md v2.4 entry

Append to `reincarnated-engine/src/reincarnated/export/MIGRATION.md`:

- v2.4 entry with `modifier_flag_tier` field + semantics
- Cross-references to gamora modifier-clamp gate dispatch + MIGRATION.md §v1.6
- Downstream consumer notes:
  - **jack-ryan** (future calibration analysis): may query `modifier_flag_tier='review'` rows for anomaly trend detection
  - **gamora** (READ-ONLY): the producer; no coordination needed
  - **knight-rider**: notify when consumer use cases arise

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `star-lord/v1.3-telemetry-schema-v2.4-modifier-flag-tier`
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Gamora**: READ-ONLY upstream (gate produces the value; recorder persists)
- **Knight-rider**: notify at completion; closes outstanding modifier-clamp gate cross-seam flag from earlier today
- **Future jack-ryan calibration analysis**: persisted `modifier_flag_tier='review'` rows enable trend detection across multiple regens

## Out of scope (explicit)

- **NO production DB migration** — V2.4 DB migration to live data/telemetry.db requires separate Matt ADR-006 authorization (same pattern as v2.1/v2.2/v2.3 migration which is now applied)
- **NO new modifier-clamp gate logic** — gamora's seam; this dispatch only persists the value
- **NO new analysis tools / queries** — separate jack-ryan dispatch if needed
- **NO existing v2.x migration re-architecture** — append v2.4 entry following the pattern
- **NO Stage 3 cipher migration work** — separate dispatch (queued)
- **NO V2 regen mode work** — separate dispatch (queued)

## Required reading

- Gamora modifier-clamp gate dispatch + MIGRATION.md §v1.6 (cross-seam flag source)
- Your prior v2.1 / v2.2 / v2.3 dispatches (pattern reference)
- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` + `recorder.py` (target files)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #11 (attribution); #12 (semantic-shifting: telemetry schema expansion); Pattern P7 R11(d) prevention prescription (recorder fail-loud — already operationalized; ensure new code path complies)

## Acceptance criteria

- [ ] migrations.py v2.4 entry added; 1 new column on class_balance_results
- [ ] Recorder wired to write modifier_flag_tier with defensive null handling (`getattr` pattern)
- [ ] Existing telemetry tests pass; new v2.4 unit test passes
- [ ] Smoke: gate-triggered class persists `"review"` to column
- [ ] Defensive-null smoke: pre-fix class results write NULL; no errors
- [ ] MIGRATION.md v2.4 entry filed (cross-references gamora modifier-clamp + downstream consumer notes)
- [ ] Intermediate tag `star-lord/v1.3-telemetry-schema-v2.4-modifier-flag-tier` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.4-modifier-flag-tier` at the commit closing migration + recorder + tests pass.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16
**Migration version (v2.4):** `_V2_4` — `ALTER TABLE class_balance_results ADD COLUMN modifier_flag_tier TEXT;`
**Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.4-modifier-flag-tier` at commit `501d616`
**Smoke status:** PASSED — 22/22 new tests pass; 121/121 full telemetry suite pass (zero regressions)
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — Schema 2.3 → 2.4 section appended
**Notes for knight-rider:**
- Cross-seam flag CLOSED: gamora modifier-clamp gate cross-seam flag from simulation/MIGRATION.md §v1.6 is now closed. Recorder wired.
- Gate-triggered classes persist "review" to modifier_flag_tier; normal-range classes and pre-fix result objects (defensive getattr) write NULL. Both paths verified by smoke.
- Live DB migration (V2.4 to data/telemetry.db) still pending — requires separate Matt ADR-006 authorization. V2.4 migration entry is in migrations.py and will apply on next apply_schema_migrations() call.
- test_telemetry_v23.py test_schema_version_is_23 equality pin updated to range check (Discipline #9) — same fix as V2.3 applied to V2.2's pin.
- Queue chain: V2 CLI flag + regen (authored; queued) → Stage 3 cipher migration (authored; queued) — as noted in dispatch, these are separate dispatches.
- jack-ryan calibration analysis (modifier anomaly trend detection): may query modifier_flag_tier='review' rows. Knight-rider routes when ready.
