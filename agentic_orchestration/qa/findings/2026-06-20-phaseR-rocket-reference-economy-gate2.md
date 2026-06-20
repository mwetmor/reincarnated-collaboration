# Finding — 2026-06-20 — Phase R: reference-economy hardening (rocket)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: PASS-WITH-INFO)
**Target:** `rocket/v-phaseR-reference-economy-hardening-1` (commit `c502451`, engine, local, NOT pushed)
**Developer:** rocket (generation seam)
**Principles applied:** Review-process P1 (math-before-code), P2 (smoke-gate), P3 (cross-seam impact), P6 (cross-seam round-trip); Disciplines #1, #2, #3, #12; ADR-004 (MIGRATION); ADR-006 (no push)

## Verdict

**PASS-WITH-INFO.** Both guards held under first-hand verification; neither tripped. The change is a faithful recompose-first PORT of the LOCKED G1 contract, surgically confined to the harness generation seam, with zero scope leak and zero test entanglement. Two INFO items carry forward (neither blocks the tag); one forward-tracking note must reach Phase 5/6 owners.

## What I found

Rocket re-sourced the harness population's authoritative `energy_type` from BC-tempo inference (`_BC_TEMPO_TO_RESOURCE`, which collapsed the whole population to mana-default) to `_assign_doc48_economy(attr, range, tempo, amplitude)` — a PORT of doc-48 §3.1 projected onto population BC features via doc-48's own collision-free 4-axis signature, with a doc-48-native within-attribute fallback for off-grid cells. The result: the 54-kit harness population now carries rage:12 / combo:9 / stamina-as-resource:3 / mana:30 — all 9 STR-melee kits carry `energy_type=rage`, materializing the Barbarian-rage build-spend lever that is the Phase-6 hinge. The change touches only generation-seam files; the production gate, bands, and simulation seam are untouched.

## Gate-2 focus areas — verified first-hand

1. **GUARD #1 (design-side, population→kit-type KEY) — HELD.** Verified the `_DOC48_ECONOMY_BY_BC` table against doc-48 §3.1 (`canonical/48-cycle-14-class-roster-2026-05-27.md:285-298`) row-by-row: all 10 rows are a faithful port of the G1 contract (Barbarian→rage, Hoplite/Wildhunter→stamina-as-resource[steady], Siege-Master/Gunslinger→combo, Assassin→charge-stack, Duelist→rage, Magus→mana, Skirmisher/Crusader→mana[DEFER]). The math-note's collision test is sound: `(attr,range,tempo,amplitude)` is collision-free within doc-48; the only coarser-key collision (DEX-melee-high: Assassin charge-stack vs Wildhunter stamina) is resolved by `amplitude`, doc-48's OWN discriminator — not an expedient choice. The within-attribute fallback uses doc-48's native discriminator axis per attribute. The key is genuinely single-valued (function returns `str` by construction; smoke exhaustively checks all 5×3×3×3 off-grid combinations resolve single-valued + kernel-consumable). **The design trip-wire correctly did NOT trip; no gandalf escalation was warranted.**

2. **GUARD #2 (technical-side, bc_target round-trip) — HELD, and stronger than claimed.** Confirmed by grep: `season_generation_pipeline.py` has ZERO `bc_target`/`econ_bin`/`cost_type` references. Stronger finding: `bc_target_from_generation_params` has NO live `.py` caller anywhere in `src/reincarnated/` (only doc/state-file references) — so the harness edit cannot re-shape bc_target geometry by any path. The production round-trip holds by construction (no shared mutation). Rocket's framing ("lives in a separate production seam via class_generator/season_orchestrator") slightly overstates the live callers — those callers are not currently active code — but the conclusion is correct and the guard is satisfied either way. **No round-trip failure → no KR re-escalation warranted.**

3. **Contract correctness — VERIFIED.** Emitted vocabulary `{rage, combo, stamina-as-resource, charge-stack, mana}` is a strict subset of kernel `_ENERGY_CONFIGS` keys `{rage, combo, focus, stamina-as-resource, charge-stack}` + mana fall-through (`combatant.py:415-426`, `:635`). The G1 table is the contract; the value matches what gamora's selector + kernel already consume. No gamora code change required (the value now matches what the already-built branch expects).

4. **Recompose-first — HELD.** No new mechanic. The two DEFERRED economies (Skirmisher damage-taken-converts, Crusader HP-economy) map to mana-default exactly as the G1 table pre-ratifies.

5. **By-class verification — SOUND.** Reproduced via smoke (ALL PASS): cell distribution rage:4/combo:3/stamina:1/mana:10 (×3 = 54-kit rage:12/combo:9/stamina:3/mana:30), STR-melee = {rage} only, INT/WIS = {mana} only, DEX = {combo,rage,stamina-as-resource}. Matches math-note §3 prediction exactly. Rocket's reported PlayerClass round-trip (0/54 mismatches) is consistent with the assignment function being the single source feeding `_build_real_player_class`.

6. **Semantic-shift declaration (Discipline #12) — PRESENT + COHERENT.** Declared at the population boundary in math-note §3 and MIGRATION: 100% mana-default → rage:12/combo:9/stamina:3/mana:30; pre/post-Phase-R KPM are different instruments; Phase 5's ONE refit fits the post-Phase-R instrument.

7. **No scope leak — VERIFIED.** Tag `c502451` touches 5 files, all generation-seam: `season_generation_pipeline.py`, `MIGRATION.md`, `AGENT_STATE.md`, the math-note, the smoke script. No band, no production gate, no magnitude, no simulation-seam file.

8. **Test drift — VERIFIED NOT ENTANGLED.** Ran the economy/resource/energy subset: 41 passed, 0 failed. Ran generation/pipeline subset: 213 passed, 0 failed. The standing 60 failures are the documented set (foundation 5-vs-7 `season_emit`; cycle13 gauntlet; LLM auth) and contain zero economy/resource/energy failures. Phase R introduced none.

9. **charge-stack forward-note — GENUINELY INERT for the workstream; track for production.** Confirmed `charge-stack` is NOT in `bc_target_source._ENERGY_ECON` (would fall to `overflow` default). Confirmed the live 18-cell population never emits charge-stack (smoke: DEX economies = {combo,rage,stamina-as-resource}; the DEX-melee-spiky Assassin cell is in the *table* but absent from the 18-cell catalog). So it is inert for the harness and for Phase 5/6 (no charge-stack entity reaches the band refit or the STR read). It is a real latent gap ONLY if the production season_orchestrator path is later fed a charge-stack entity — correctly flagged in MIGRATION for that seam owner, correctly out of Phase-R scope.

## Rationale

The dispatch's two binding guards (GUARD #1 design-side key-ambiguity → gandalf; GUARD #2 technical-side round-trip → KR) are the load-bearing acceptance criteria. Both were verified to hold independently of rocket's self-report (P6 cross-seam round-trip; design trip-wire per the gandalf amendment). The math-before-code discipline (P1 / Discipline #1) was satisfied — math-note authored before code with the KEY derivation and collision proof. Smoke-gate (P2 / Discipline #2) present and passing. Cross-seam contract documented (P3 / ADR-004). The change is the cheapest-possible-place catch gandalf identified: the population level, before Phase 6 fired against a null instrument.

## Action

- [x] Developer (rocket): no action required to clear the tag. Work is PASS-WITH-INFO.
- [ ] gamora (G3b re-arm): the rage/combo/stamina arms now fire on real entities for the FIRST time. G3b must verify the BUILT rage branch MATERIALIZES (build-on-swarm/spend-on-anchor) on a real rage entity, and that distinct economies produce distinguishable tier-firing. This is the first non-degenerate G3b — the prior mana-default population could not exercise it.
- [ ] Phase 5 owner (gamora + jack-ryan): the ONE band refit must fit the POST-Phase-R composed instrument (rage:12/combo:9/stamina:3/mana:30), not a mana-default population. Pre/post-Phase-R KPM are different instruments per the Discipline #12 declaration.
- [ ] season_orchestrator seam owner (NOT this workstream): if the production path is ever fed a charge-stack entity, `bc_target_source._ENERGY_ECON` needs the `charge-stack` key (currently falls to `overflow`). Tracked in MIGRATION; latent, not active.

## INFO items (for the record; non-blocking)

- **INFO-1:** Rocket's GUARD #2 framing references `class_generator.py`/`season_orchestrator.py` as the live bc_target callers, but `bc_target_from_generation_params` has no current `.py` caller in the tree. The guard conclusion is unaffected (the binding is even more isolated than reported), but the math-note's caller attribution is slightly ahead of the live code. Cite: Discipline #9 (attribution clarity). No fix required.
- **INFO-2:** `_BC_TEMPO_TO_RESOURCE` / `_infer_resource_model` are correctly kept-in-place and marked RETIRED-as-economy-source to minimize blast radius. They are now dead-as-economy-source but `_infer_resource_model` is still defined. A future cleanup pass could remove the retired path once no consumer reads it; not now (correct call to minimize this tag's surface). Cite: Discipline #12 (declared retirement). No fix required.

## References

- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:213-307` (the `_DOC48_ECONOMY_BY_BC` table + `_assign_doc48_economy`), `:682-686` + `:806-811` (the two call sites)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/2026-06-20-phaseR-reference-economy-hardening-math.md` (KEY derivation §1; round-trip guard §2; distribution §3)
- `~/Games/reincarnated-engine/scripts/rocket_phaseR_economy_smoke_2026_06_20.py` (verified ALL PASS)
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md:8-73` (Phase R entry)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py:415-426` (`_ENERGY_CONFIGS` consuming contract)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_source.py:63-76` (`_ENERGY_ECON` — charge-stack absent, confirmed)
- `~/Games/reincarnated-collaboration/canonical/48-cycle-14-class-roster-2026-05-27.md:285-298` (doc-48 §3.1, the ported source)
- Dispatch: `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-20-rocket-phaseR-reference-economy-hardening-DRAFT.md`
- gandalf ruling: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`
- G1 contract: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` §3
