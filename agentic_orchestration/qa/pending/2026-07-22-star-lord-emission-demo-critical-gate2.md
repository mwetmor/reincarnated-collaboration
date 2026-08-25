# Finding — 2026-07-22 — star-lord emission demo-critical (Lane-1)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** PASS-WITH-CONDITIONS
**Target:** tag `star-lord/v-emission-demo-critical-1` = engine `a3671d4` (origin/main); collab completion `ac5f9a15`
**Developer:** star-lord
**Principles applied:** #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #6 (cross-seam round-trip)
**Disciplines cited:** #1.1 (resource-bounds), #8 (schema validation at boundary), #14 (canonical-element non-leak)
**ADRs:** ADR-004 (MIGRATION), ADR-006 (read-only external)

## What I found
The three flavor-pass wiring fixes are sound. Both `apply_skill_flavor_pass()` and `apply_gear_flavor_pass()` correctly abandon the Phase-2 object API (`name_skill()`/`name_gear_item()`) — which expects Pydantic objects the bundle serializes as strings/dicts — for inline `complete_json()` prompts driven off dict fields. This is the correct call: bundle records are serialized, not live Phase-2 objects, so the object-based path could not have worked. Gear resumability fix (skip only when `name AND flavor_text` both non-null) correctly rescues the 90 named-but-unflavored records the old `name is not None` check skipped. `apply_monster_flavor_pass()` needs no change (its `_MonsterProxy` handles dicts). The `encounters` reserved dict is inert (empty marker only), validated at the boundary by `validate_bundle()` (required-key + `isinstance dict` guard). 102/102 tests pass. LOCKED baseline `one_realm_demo_bundle.json` verified untouched (`schema_status: LOCKED`, no encounters key); delta bundle carries `DRAFT-pending-drax-handshake`.

Verified against the three specific star-lord flags:
- **G6 flag persistence (load-bearing):** empirically confirmed — `apply_gear_flavor_pass()` does `rec = dict(rec)` (full copy) before writing name/flavor, so `_non_canonical=True` + `_non_canonical_reason` survive the fill. Ran a mock-LLM stub through the pass: name filled, flavor filled, `_non_canonical` PRESERVED. This is the correct G6 behavior.
- **encounters emits no content:** confirmed — reserved dict only; no encounter records; `_grammar_frozen_by: Tier-3-W1`.
- **No un-gate / no park resolution crept in:** diff touches none of `_DEFERRED_PROXY_BINS`, `season_exporter.py`, `cycle14_unified_driver.py` (nonexistent), or `P1_ARCHITECTURE_PARK`. Two melee proxy kits only. ADR-006 held: no write SQL introduced (telemetry gear read stays read-only).

## Rationale
Deferred-verification split honored per dispatch: the live flavor fire is CREDENTIAL-GATED (ANTHROPIC_API_KEY intentionally absent per Max-billing discipline). The delta bundle correctly shows dry-run state (skill 0/648, monster 0/40, gear 0/150 null — all expected pre-fire). Per Principle #2, I gate the PATH not the artifact: the mock-LLM Group-I tests + dry-run PASS + code read establish the fill path WILL produce non-null flavor when the key is present. Discipline #1.1 cost declaration present and reasonable (838 calls ≈ $1.86, within $1-3 projection; 3-retry backoff + per-item resumability = anomaly-guarded, zero double-billing). Discipline #8 satisfied at the validate_bundle boundary. §F.4 respected: build-fixture, not demo emission; no count asserted.

## Conditions (must close before final acceptance — none block the CODE tag)
- [ ] **C1 (Matt):** fire the live run — `export ANTHROPIC_API_KEY=... && python3 src/reincarnated/export/w3_demo_bundle_flavor_run.py` — then re-run `--smoke-only`. Deferred-verification item; closes the dispatch done-predicate ("flavor filled non-null"). After fire, confirm: skill 648/648, monster 40/40 name+flavor, gear 150/150 flavor, AND the 60 `_non_canonical` flags still present.
- [ ] **C2 (drax, KR routes):** re-handshake scoped to the `encounters` key only (schema shape change). `schema_status` stays DRAFT until drax signs. Not my review surface — noted per Principle #6.

## INFO (non-blocking; for the record)
- No dedicated test asserts `_non_canonical` persistence *through* the gear flavor pass (Group I covers marking and fills separately, not their interaction). Behavior is correct — verified empirically here — but a single regression test would lock it. Suggest adding on the live-fire follow-up.
- Schema-delta note line 47 says "all 150 gear retain `_scaffold: true`"; the actual code marker is `_non_canonical` on the 60 stubs. Prose imprecision in the note, not a code defect. Optional cleanup.

## Action
- [ ] Developer (star-lord): no code change required for PASS. Optionally add the G6-through-flavor-pass regression test on the live-fire follow-up.
- [ ] Matt: fire C1 live run (deferred verification).
- [ ] KR: route C2 drax re-handshake.

## References
- `~/Games/reincarnated-engine/src/reincarnated/export/one_realm_bundle_assembler.py` (`apply_skill_flavor_pass` :954, `apply_gear_flavor_pass` :1050, `apply_monster_flavor_pass` :863, `mark_non_canonical_gear_stubs` :1173, `validate_bundle` :1238, `assemble_one_realm_bundle` :1395, encounters key :1535)
- `~/Games/reincarnated-engine/src/reincarnated/export/w3_demo_bundle_flavor_run.py`
- `~/Games/reincarnated-engine/src/reincarnated/export/math/2026-07-22-one-realm-bundle-schema-delta.md`
- `~/Games/reincarnated-engine/tests/test_one_realm_bundle_assembler.py` (Group I `TestW3EmissionDemoCritical` :1228)
- `~/Games/reincarnated-engine/src/reincarnated/output/one_realm_demo_bundle_w3_flavor.json` (delta, DRAFT), `one_realm_demo_bundle.json` (baseline, LOCKED — untouched)
