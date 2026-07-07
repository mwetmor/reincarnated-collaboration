# Finding — 2026-07-07 — leg-2 summoner-emission-route (COORDINATED THREE-SEAM Gate-2)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** PASS-WITH-FOLLOWUPS
**Target (unit):** `rocket/v-batch2-leg2-summoner-emission-route-1` @ `996f77d` + `gamora/v-batch2-primary-t4-consume-widen-1` @ `8d8e76b` + `star-lord/v-batch2-dda-lock-validator-widen-1` @ `0f7de25` (=HEAD)
**Developers:** rocket (PRODUCE), gamora (CONSUME), star-lord (VALIDATE)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact / MIGRATION), 4 (decisions-log truth), 6 (cross-seam round-trip)
**Disciplines cited:** #2, #11, #12
**Governs Gate-1:** `a5ebd17` (leg-2 PASS-WITH-CONDITIONS, C1–C4)

## Verdict

**PASS-WITH-FOLLOWUPS** for all three tags reviewed AS A UNIT. Independently verified against SOURCE (not the submission records). The leg-2 machinery — route fn + validator-widen + consume-side re-derive — lands correctly, is single-sourced on C2, closes the C1 divergence by construction, preserves the DDA lock and the cert baseline byte-intact, and is genuinely INERT on the emitted population pre-leg-3. No BLOCK. The two followups are leg-3-boundary items, not leg-2 defects.

## What I found (descriptive — verified independently vs SOURCE)

**Structure.** The three tags are linear on HEAD: rocket `996f77d` → gamora `8d8e76b` → star-lord `0f7de25`(=HEAD); all three verified ancestors-of-HEAD. Exactly 5 production code files changed across the range (`t4_catalog_v2.py`, `mechanic_alteration.py`, `cycle14_wave5_emitter.py`, `gauntlet_sim.py`, `unified_calibration_loop.py`) + 2 smokes + 2 math notes + tests + 3 MIGRATION + 4 AGENT_STATE. 378 insertions net of the expected surface; nothing else touched.

**(1) C2 single-source — CLEAN.** `ACCEPTED_PROXY_PRIMARY_T4` is defined exactly ONCE (`t4_catalog_v2.py:150`), derived from named PROXY constants (not literals), with all four import-time guards present and live-passing on import: exactly-5, subset-of-PROXY-family, INVERSION excluded, ZONE_CONTROL excluded. No divergent copy exists anywhere — a full `PROXY_FISSION`-in-set-literal sweep found only the C2 def, an unrelated `layer2_dimensions.py:256` data-table keyed by the constant, smoke assertions that check equality against C2, and a pre-existing unrelated `w0_prereqs` membership pin. star-lord IMPORTS it and its retired W0 local `_PROXY_FAMILY_PRIMARY_T4_STRATEGIES` is now a bare ALIAS (`= ACCEPTED_PROXY_PRIMARY_T4`, `cycle14_wave5_emitter.py:734`) pinned by a test to equal C2. gamora IMPORTS it in its smoke. No copies, no drift.

**(2) C1 divergence — CLOSED by construction.** Both gamora sim sites (`gauntlet_sim.py:2279`, `unified_calibration_loop.py:3592`) call rocket's EXACT `route_primary_t4()` (imported from `mechanic_alteration`), with `proxy_decls=build_proxies_surface(kit.skills)`. Emit sources proxy_decls from the SAME `build_proxies_surface(self.skills)` (`season_generation_pipeline.py:528`, defined `proxy_vocabulary_bridge.py:295`). Same derivation function + same proxy source ⇒ sim == emit, not a mirror. All three MIGRATION lockstep entries cross-reference the other two seams + the C2 constant + tags (ADR-004 / Principle 3 satisfied).

**(3) C3 + C4 — GREEN, re-run by me at HEAD.** rocket route smoke: 14/14 GREEN — S1 bone→PROXY_FISSION, crypt→PROXY_SOVEREIGNTY under DoF-A `focus`; routed member == ranker argmax (faithful pass-through, no re-score); S2 8-kit non-summoner corpus × {[], None} BYTE-IDENTICAL and still DDA (the `$0` no-op-off-summoner-bin proof). gamora consume smoke: S2 8/8 non-summoner byte-identical to `select_primary_t4`; C1 summoner fixtures draw accepted members; C2 anchor asserts imported-not-copied.

**(4) Validator both directions — verified at SOURCE + suite re-run.** `validate_class_data()` (`cycle14_wave5_emitter.py:~795-840`) gates on `is_proxy_bearing = bool(proxy_decls)`: proxy-family member + proxy-bearing → ADMIT; proxy-family member + empty-decl → REJECT (DDA lock preserved); DDA → ADMIT on both branches (fallback); ZONE_CONTROL (absent from C2) and unknown strings → REJECT via the `elif strategy is not None` branch. Suite `test_cycle14_wave5_loadout_emission.py`: 115/115 PASS, including the ×5 accept-on-summoner, ×5 reject-on-empty-decl, ZONE_CONTROL-reject, and C2-pin tests.

**(5) Cert-baseline byte-intact + freeze guards — HOLD.** Code-diff token scan for `2.3384`/chassis/`_SCAFFOLD_MAGNITUDE`/bar/band found zero added-or-removed magnitude/chassis/bar/band values (the single "magnitude" hit is a replaced comment line in the validator, no value change). The emit path does NOT call `route_primary_t4` — `season_generation_pipeline.py:404-412` still holds `primary_t4` as a plain DDA slot, and emit assigns from the DDA `PRIMARY_T4` constant (`cycle14_wave5_emitter.py:546`). The certified population is entirely non-summoner ⇒ every certified kit hits `build_proxies_surface → []` ⇒ route falls back to `select_primary_t4` with identical args ⇒ byte-identical. **Disc #12: no live-behavior semantic shift landed early — leg-2 is genuinely inert pre-leg-3.**

**(6) Regression — GREEN together at HEAD.** Broad cross-seam run of all three seams' cited suites (`test_proxy_pairing_layer`, `test_proxy_t4_suite_eval`, `test_proxy_t4_suite_strategies`, `test_layer2_dimensions_and_t4_catalog_v2`, `test_two_layer_t4_architecture`, `test_one_realm_bundle_assembler`, `test_cycle14_wave5_loadout_emission`): **378 passed**.

## Rationale

- **Principle 1 / Disc #1:** both math notes present and pre-date code (rocket `cbac6ed` note landed before the `996f77d` route; gamora note carries the equivalence + byte-faithful-sourcing + invariance proofs).
- **Principle 2 / Disc #2:** every landing carries a re-runnable closed-form smoke (no fights, no regen, no LLM). I re-ran all of them GREEN.
- **Principle 3 + Principle 6 / ADR-004 / Disc #12:** three-seam MIGRATION lockstep with mutual cross-refs; star-lord's validator round-trip (persist/read-back) exercises the consumer boundary both directions; the change is additive and the DDA lock domain is byte-preserved.
- **Disc #11 (attribution):** the `test_w3_emission_driver` pre-existing failure was independently confirmed NOT leg-2's — leg-2 did not touch that test and it has zero references to `route_primary_t4`/C2. It is a leg-3 readiness item, not a leg-2 BLOCK.

## Action

- [x] jack-ryan: three leg-2 pending items archived; Phase-1 housekeeping item disposed (see below).
- [ ] Developers (leg-3, future fire): leg-2 is certified inert; leg-3 owes the wiring + run (see boundary below) and must re-clear `test_w3_emission_driver` as part of its own gate.
- [ ] Matt: no BLOCK-escalation. Milestone-tagging (drop-prefix) of the leg-2 unit remains Matt's call per ADR-003 when/if desired; leg-2 sits fine as three intermediate seam-prefixed tags until leg-3.

## Leg-3 boundary (explicitly named — what leg-2 does NOT owe)

Leg-2 built the machinery; it did NOT wire emit. Leg-3 (a separate future fire) still owes:
1. **Emit-assignment wiring** — route `season_generation_pipeline.py:404-412` / the emitter's `primary_t4` assignment through `route_primary_t4` (currently DDA-only via `PRIMARY_T4`).
2. **The emission run itself** — held until this coordinated Gate-2 PASS (now satisfied) + Matt authorization; a bulk/LLM op per ADR-006.
3. **Disc #1.1 resource/LLM-cost projection** for the emission run (leg-2 carried none; leg-3 owes it before firing).
4. **`test_w3_emission_driver::test_smoke_dry_run_completes`** — pre-existing baseline failure, correctly flagged for separate triage; leg-3 (which actually populates a summoner emit) must re-clear it.

## Housekeeping disposition — Phase-1 rebase Gate-1 item

`2026-07-07-rocket-proxy-t4-b1-rebase-phase1-v3-refire-gate1.md` is disposed (archived), NOT because of a fresh review but because every obligation in it was ratified piecemeal — no genuine un-reviewed obligation remains on inspection:
- **DoF-A** (`energy_type="focus"` re-designation, gandalf's design call): ratified + landed `1af6889`; proven live in both leg-2 smokes I re-ran.
- **DoF-B** (F-f GEOMETRY max-1 = B4-scoped, `enforce_family_max_one` stays unreachable through the single-argmax summoner route): confirmed at leg-2 Gate-1 `a5ebd17` and re-confirmed here; re-surfaced to KR as still-B4-scoped.
- **Anchor tag + gamora extension**: `rocket/v-proxy-t4-rebase-phase1-v3-confirmed-1` landed; gamora's extension rode it through its own Gate-2 PASS `dce4ae4` (commit `8a29009` on HEAD).
- **Legs 2-3 scoping**: leg-2 is this finding; leg-3 boundary named above.

## References

- `src/reincarnated/generation/t4_catalog_v2.py:128-171` (C2 constant + guards)
- `src/reincarnated/generation/mechanic_alteration.py:1972` (`route_primary_t4`, predicate P)
- `src/reincarnated/export/cycle14_wave5_emitter.py:101,734,795-840` (import, alias, validator conditional)
- `src/reincarnated/simulation/gauntlet_sim.py:2228,2279` + `unified_calibration_loop.py:3554,3592` (consume sites)
- `src/reincarnated/generation/season_generation_pipeline.py:404-412,528,546` (leg-3 slot unwired; emit proxy_decls source; DDA assignment)
- `src/reincarnated/generation/notes/leg2_primary_t4_route_smoke_2026_07_07.py` (14/14 GREEN, re-run)
- `src/reincarnated/simulation/notes/leg2_primary_t4_consume_smoke_2026_07_07.py` (S2 8/8 + C1 + C2, re-run)
- `tests/test_cycle14_wave5_loadout_emission.py` (115/115) + broad regression (378 passed)
- MIGRATION lockstep: `generation/MIGRATION.md` [2026-07-07] LEG-2 / `export/MIGRATION.md` § leg-2 VALIDATOR-WIDEN / `simulation/MIGRATION.md:8447` LEG-2 CONSUME
- Gate-1: `agentic_orchestration/qa/findings/2026-07-07-rocket-leg2-summoner-primary-t4-routing-gate1.md` (`a5ebd17`)
