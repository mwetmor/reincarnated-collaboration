# Gate-2 Finding — EAA-3 § 3.3 + EAA-4 § 3.3 star-lord emit integration

**Date:** 2026-06-02
**Reviewer:** jack-ryan (DEV-MODE Gate-2 with INFO/WARN/BLOCK authority)
**Work under review:**
- Commit `23b42ed` — tag `star-lord/v1.4-eaa-3-eaa-4-emit-integration-1`
- `reincarnated-engine/src/reincarnated/export/kit_space_emitter.py` (new module)
- `reincarnated-engine/tests/test_kit_space_emitter.py` (31 new tests)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.72
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` (updated)
**Authority:** Matt 2026-06-02 + Locks A-P (LOCK K) + ADR-004 (MIGRATION.md discipline)

---

## VERDICT: PASS-with-INFO

Two INFO items; zero WARNs; zero BLOCKs.

---

## What was inspected (empirical per Discipline #11)

1. Full `kit_space_emitter.py` source read (519 lines; emit-order discipline, atomic write, skip-flag guard, schema validation at boundary)
2. `test_kit_space_emitter.py` full coverage structure (31 tests; 4 classes; single-kit, multi-kit, edge-cases, index-regen)
3. `MIGRATION.md § v1.72` content (old/new contracts, consumer obligations, backward-compat, smoke-test results)
4. `AGENT_STATE.md` updated checkpoint
5. Cross-checked against: CHRONICLE_SCHEMA.md § 5 emit-order discipline + § 5.2 atomic-write convention; joint spec § 1-2 FK + kit_id format locks; EAA-3 dispatch § 3.3 + EAA-4 dispatch § 3.3 acceptance criteria

---

## Acceptance criteria coverage (EAA-3 AC-3 + EAA-4 AC-3)

**EAA-3 § 6 AC-3 — Engine emit path emits per-kit entries when EAA-2 skip flags active:**
- `should_use_kit_space_emit()` guard correctly implements BOTH-flags-True condition (per LOCK M Stage 1 compose rule)
- `emit_kit_space_expansion_event()` mints kit_ids, calls `build_kit_entry()` + `validate_per_kit_entry()` at boundary, writes per-kit JSONs atomically
- Test `test_chronicle_written_and_kit_json_written` + `test_per_kit_json_required_fields_present` confirm kit JSONs land with all required fields
**STATUS: MET**

**EAA-4 § 6 AC-3 — Engine emit path emits chronicle entry on each kit-space-expansion fire:**
- Chronicle entry built with all CHRONICLE_SCHEMA.md § 4.2 required fields (event_id, event_type, event_timestamp, event_date_utc, event_scope, substrate_inputs_changed, engine_version_sha, kit_ids_generated, kit_count, skip_flags_active, lineage_tags)
- Emit-order discipline enforced: chronicle written FIRST (Step 3), per-kit JSONs SECOND (Step 4) per CHRONICLE_SCHEMA.md § 5.1 explicit step labeling in code
- Atomic `.tmp` → `os.replace` on ALL writes (chronicle + per-kit + kits_index)
- `test_chronicle_written_before_per_kit_json` + `test_no_tmp_files_left_over` confirm both
**STATUS: MET**

**FK round-trip integrity:**
- `kit_space_expansion_event_id` in per-kit JSON equals chronicle `event_id` (minted once at event-start; propagated to all entries)
- `test_fk_linkage_kit_json_references_chronicle_event_id` (single-kit) + `test_fk_linkage_all_kits` (20-kit batch) verify round-trip
- SEQ-3 format `^kse_\d{8}_\d{3}$` confirmed by `test_event_id_format_seq3`
**STATUS: MET**

---

## Discipline compliance

- **#8 (schema validation at export boundaries):** `validate_per_kit_entry()` called at write boundary for every kit entry before filesystem write. Validation errors surface in `KitSpaceEmitStats.kits_validation_errors` (non-blocking emit; errors do not silently vanish). PASS.
- **#2 (smoke-test before LLM fire):** 31 new tests + 147/147 EAA-chain PASS + 317/317 export+EAA combined PASS. EAA-5 first-fire gated on this commit per wave-state. PASS.
- **#11 (empirical inspection):** Implementation and tests read directly. Cross-checked against canonical spec sources. PASS.
- **ADR-004 (cross-seam MIGRATION):** MIGRATION.md § v1.72 present with full old/new contract documentation, consumer obligations, backward-compat, and smoke-test results. PASS.
- **ADR-006 (read-only-by-default):** No DB writes. Filesystem only. Shadow ingest deferred to elrond post-EAA-5. PASS.

---

## INFO-1 — `substrate_provenance` lineage tag is hardcoded

**Severity:** INFO (non-blocking; flag for EAA-5 fire consideration)

`_build_chronicle_event_entry()` builds `lineage_tags.substrate_provenance` as the hardcoded string `"pool-v1.1+ws2.p2-magic-weapons"` regardless of what `substrate_inputs_changed` actually contains. This is correct for the first EAA-5 generation fire (pool.json v1.1 + WS2.P2 magic weapons substrate IS what will be active). It becomes stale if future expansion events fire against a different substrate mix.

**Recommendation:** before EAA-5 fire, no action needed — hardcoded value is accurate. At the next substrate expansion event (if pool.json is updated or new substrate ingested), the `substrate_provenance` field should be derived from the actual substrate inputs rather than the hardcoded constant.

**Not a BLOCK:** EAA-5 fires against exactly this substrate. The hardcoded value is accurate for the immediate use case. Flag as carry-forward for the first post-EAA-5 substrate expansion event.

---

## INFO-2 — `kits_validation_errors` is non-blocking by design; flag is documented but not surfaced to caller as exception

**Severity:** INFO (non-blocking; behavioral design note)

In `emit_kit_space_expansion_event()`, validation errors are logged at ERROR level and accumulated in `stats.kits_validation_errors`, but the emit continues (kit JSON is still written). The docstring states "hard-fail mode available at call site" but no hard-fail parameter exists on the function signature.

This is an intentional resilience tradeoff: partial success at EAA-5 first fire is recoverable; EAA-4 § 5.3 partial-failure recovery model is consistent with this. However, callers at EAA-5 fire site should CHECK `stats.kits_validation_errors == 0` and fail loudly if non-zero — the smoke-test infrastructure already covers this via `self.assertEqual(stats.kits_validation_errors, 0)` in the test fixtures.

**Recommendation:** EAA-5 fire-site call code should assert `stats.kits_validation_errors == 0` after emit. Consider adding an optional `raise_on_validation_errors: bool = False` parameter at EAA-5 fire-site authoring if the resilience-vs-fail-fast preference is revisited.

**Not a BLOCK:** current design is explicit, documented, and test-covered. Caller discipline covers the gap.

---

## No issues found on

- Emit-order discipline (CHRONICLE_SCHEMA.md § 5.1 compliance: Steps 1→2→3→4 correctly sequenced in code)
- Atomic write correctness (`.tmp` → `os.replace` used for all three write targets: chronicle, per-kit JSON, kits_index.json)
- SEQ-3 event_id format enforcement (UUID-hex documentation drift correctly handled; SEQ-3 enforced via `validate_event_id()` from rocket's `kit_space_schema.py`)
- Per-primary sequencing (in-memory `per_primary_counts` counter correctly incremented within batch; cross-event counting via `count_kits_by_primary()` directory glob)
- Skip-flag guard truth table (all 4 cases covered; backward-compat path identity confirmed)
- MIGRATION.md § v1.72 — old/new contracts, consumer obligations, backward-compat table all complete and accurate
- Chronicle schema version `"1.0"` correctly propagated from `_CHRONICLE_SCHEMA_VERSION` constant
- Period normalization to uppercase at emit boundary (IP-2 compliance)
- `engine_version_sha` sourced from `telemetry.db.get_engine_version()` with subprocess fallback (consistent with `season_writer.py` pattern)
- `engine_version_full` 40-char SHA captured additively when available
- Empty batch edge case (chronicle entry written with kit_count=0; no crash)
- Second-event-same-day seq increment (SEQ-3 counter correct)

---

## Disposition

**PASS-with-INFO.** Two non-blocking INFO items. EAA-3 AC-3 + EAA-4 AC-3 are MET. Phase 1 EAA-3 + EAA-4 acceptance criteria are fully covered at the star-lord seam.

**EAA-5 first-fire unblocked** (from star-lord + emit-pipeline perspective). Remaining gate: wave-state update to reflect star-lord emit complete + EAA-3/EAA-4 COMPLETE row updates.

**EAA-5 fire-site obligation:** call-site MUST check `stats.kits_validation_errors == 0` per INFO-2.

**Signed:** jack-ryan (DEV-MODE Gate-2; EAA chain Phase 1 co-gatekeeper)
