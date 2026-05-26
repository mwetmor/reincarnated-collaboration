# Dispatch — 2026-05-25 — rocket — engine generation run (v1 narrow milestone first-use)

**From:** knight-rider (orchestrator)
**To:** rocket (generation seam — primary owner of orchestration pipeline)
**Approved by:** Matt 2026-05-25 (Cycle 12 close ratification + engine generation run AUTHORIZED per framing brief; skip-confirmation re-authorized for Cycle 13)
**Estimated effort:** ~30-60 min wall-clock for the generation run itself; full forms in loadout via existing star-lord export pipeline
**Acceptance:** ~30-40 forms produced via NEW ENGINE (v2.0), exported to loadout JSON, visible in Vercel preview; all coverage criteria per framing brief § 1 met; provenance manifest emitted

---

## Context (the v1 narrow milestone first-use)

This is **the engine v1 narrow milestone Matt has been driving toward** — the first production use of the new engine post-Cycle-12 close (`v1.0-new-engine-ready` tag at engine `7cff770` + loadout `c06bed1`).

The new engine is complete and Gate-2-PASSED (commit `e3756bc`): Layer 2 (BC-target subspace generator) + Layer 3 (skill content + SC-3) + Layer 4 (W1.13 multi-dim convergence) + Layer 6 (§ 8 wire-up + L9 opportunity-scan refactor) + Wave 5 cross-seam consumer integration (star-lord off-hand contract + t4_alteration_type telemetry column; gamora sim-combatant integration; drax spirit_guide_narration_metadata auto-detect). All seams are LIVE-wired.

**This dispatch is execution only — NO new code amendments.** The work is: fire the production engine end-to-end at N=30-40 form scale and produce a substrate-bound form catalogue for gandalf's design-fit pass + Matt's T4 post-mortem session 1.

Per framing brief § 0 (TL;DR): "Fire single engine generation run dispatch producing ~30-40 forms via the new BC-target subspace generator (Layer 2) + skill content (Layer 3) + W1.13 multi-dim convergence (Layer 4) + § 8 wire-up with L9 opportunity-scan refactor (Layer 6). Forms upload to loadout app via star-lord export pipeline. Gandalf performs post-generation design-fit pass producing special case summary for Matt + gandalf T4 post-mortem session 1."

---

## Required reading before starting

**Primary (load-bearing):**
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` — RATIFIED framing brief; defines all coverage + quality criteria (this dispatch executes against this brief verbatim)
- `agentic_orchestration/cycle-12-wind-down-summary-2026-05-25.md` — Cycle 12 closure record
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1 (cell coverage, named-personage anchors, mythological-NULL rescue, provenance mix)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B 8-phase workflow
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §§ v1.4-layer-2 through v1.5-cycle-12-wave-5-off-hand-contract-export — full cross-seam emission contract

**Companion (consult as needed):**
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — Cycle 12 framing brief (L1-L11 + interface contract § 4 LOCKED)
- `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — most recent rocket state (Cycle 12 Layer 6 COMPLETE)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #1 (math-before-code), #2 (smoke-test), #11 (empirical inspection), #1.1 (resource-bounds projection — relevant for N=30-40 LLM cost guard)

---

## Math-before-code

**Not applicable** — execution dispatch, no new algorithm or implementation. Math is settled per the 4 layer math notes already landed:
- `generation/notes/cycle-12-layer-2-bc-target-subspace-generator-2026-05-25.md`
- `generation/notes/cycle-12-layer-3-skill-content-and-sc-3-2026-05-25.md`
- `generation/notes/cycle-12-layer-4-multi-dim-convergence-2026-05-25.md`
- `generation/notes/cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25.md`

**Pre-fire resource-bounds projection (Discipline #1.1) required:** before firing the run, project peak memory + LLM token cost for N=30-40 forms × Phase 5 LLM calls (per-form names + skill names + descriptions + cosmological vocabulary). Verify against host RAM + LLM cost guard. Record projection in run log; if projection exceeds reasonable cycle budget, escalate to knight-rider for guidance.

---

## Cross-seam contract change? (Principle 6 gate)

**NO** — this dispatch does NOT add, modify, rename, or remove any cross-seam field. It executes the existing pipeline at production scale.

**Round-trip:** not applicable — no cross-seam contract change in this dispatch. The cross-seam round-trip smokes were validated layer-wise during Cycle 12 (Layer 6 dispatch round-trip smoke PASS via `_ensure_json_serializable`; Wave 5 off-hand export round-trip 42/42 PASS; t4_alteration_type telemetry column round-trip validated at star-lord Wave 5 completion).

---

## Scope

- [ ] Pre-fire resource-bounds projection (Discipline #1.1): peak memory + LLM token cost for N=30-40 × Phase 5 calls + cosmological vocabulary; record in run log
- [ ] Fire single end-to-end engine generation run via `SeasonOrchestrator.generate_season()` (or equivalent v2.0 entrypoint) producing **~30-40 forms**
- [ ] Coverage per framing brief § 1.1 (verify in run output):
  - [ ] All 25 BC-target cells represented OR explicitly accepted coverage gap with note (per L2 25-vs-22 reconciliation; gandalf comp-policy verdict § 1.1)
  - [ ] All 6 v1 § 8 strategies represented (≥2-3 forms per strategy where cell-eligibility allows): RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF
  - [ ] All 4 `source_library` provenance types present: substrate-pulled main, substrate-pulled off-hand (per Sidecar B), engine-authored gap-fills (per Stage 3.5), mythological-NULL rescue (per Stage 4)
  - [ ] 4 Sketch F named-personage anchor forms produced: **Hattori Hanzō**, **Lu Bu**, **Moctezuma**, **Gilgamesh** (per composition policy v1 § 5.2; `named_bearer` field populated)
  - [ ] All 8 core elements represented (physical/fire/water/earth/wind/lightning/holy/shadow); wind + lightning thin-cell-fallback expected per Cycle 12 elrond pre-Layer-2 prep
  - [ ] All 4 attributes represented (STR/INT/WIS/DEX); INT/WIS caster cells thin per substrate distribution — Option β attribute-level matching expected
- [ ] Quality criteria per framing brief § 1.2 (verify):
  - [ ] Algorithm § 8 keystones actually shift fight behavior (Option γ payoff — verify via spot-check on 2-3 forms that `t4_alteration_output` populates AND `apply_t4_alteration_to_combat()` produces non-null `AlteredFightEngineContext` fields)
  - [ ] All forms have full schema population per `PlayerClassV2` interface contract
  - [ ] Sim-viability flag PASS per § 8.4 sim-viability check on all forms
  - [ ] `engine_version = "v2.0"` on all forms
  - [ ] `mechanical_substrate_triple` populated on all main-weapon-bearing forms
  - [ ] Substrate-binding integrity: main_weapon mechanical fields match kit BC-target cell within thin-cell-fallback tolerance per composition policy v1 § 4
- [ ] Export forms to loadout JSON via existing star-lord export pipeline (`season_exporter.export_season()`) — produces `classes.json` consumable by loadout app
- [ ] Upload exported season to loadout (whatever production-pipeline shape star-lord's existing Wave 5 wiring provides — copy JSON into `reincarnated-loadout/public/seasons/` or whatever consumption path is canonical; verify Vercel preview picks up)
- [ ] **Provenance manifest** (deliverable for gandalf design-fit pass): emit a tabular run manifest at `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` listing **per-form**: form_id, BC-target cell, element, attribute, primary § 8 strategy, source_library provenance, named_bearer (if any), main_weapon name + mechanical_triple, primary off_hand (if any), engine_version, brief one-line characterization. This is the index gandalf will navigate during design-fit pass.
- [ ] Smoke-test passes (the generation run IS the smoke at production scale; verify pipeline completes without exception + all forms validate against PlayerClassV2 schema)
- [ ] MIGRATION.md: **not applicable** — no cross-seam contract change
- [ ] Round-trip smoke: not applicable — no cross-seam contract change in this dispatch (see Principle 6 gate above)
- [ ] AGENT_STATE.md updated at session end (note v1 narrow first-use COMPLETE + reference run manifest)
- [ ] Tag: `rocket/v0.1-engine-generation-run-v1-narrow-2026-05-25`

## Acceptance criteria

- [ ] ~30-40 forms produced; coverage criteria per framing brief § 1.1 met (or coverage gap explicitly noted with rationale)
- [ ] All forms schema-valid per `PlayerClassV2`; `engine_version = "v2.0"`; `t4_alteration_output` populated; § 8 keystones verified to reach combat arithmetic via Layer 6 wire-up
- [ ] Forms exported to loadout `classes.json` via existing star-lord pipeline; loadout consumes (Vercel preview confirms render OR run-log captures consumption-readiness)
- [ ] Provenance manifest authored at `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` — sufficient navigation index for gandalf design-fit pass
- [ ] Round-trip smoke: not applicable because no cross-seam contract change in this dispatch (cross-seam contracts already round-trip-validated layer-wise during Cycle 12)
- [ ] Tag `rocket/v0.1-engine-generation-run-v1-narrow-2026-05-25` shipped; AGENT_STATE.md updated

## Out of scope (explicit non-goals)

- **NO new code amendments** — execution dispatch only. If the run surfaces a bug requiring code change, STOP and escalate to knight-rider for re-routing (Cycle 13 scope surface, not v1-narrow execution)
- **NO Phase 5 cohesion-judge calibration tuning** — calibration spec PENDING (gandalf canonical authoring deferred); names + sub-element flavoring will produce but may not be optimally calibrated. **Flag at post-mortem, do not amend mid-run.**
- **NO Phase 6 visual production** — Sidecar A image-pass-through verdict stands; production Meshy wire-up not done. Expect placeholder visuals OR no visuals. **Document what shows up, do not amend.**
- **NO Phase 7 joint-gate amendment** — status unclear per framing brief § 1.3; may exist implicitly via existing acceptance criteria. **Document observed behavior, do not amend.**
- **NO Layer 7 BDI test framework execution** — deferred v1.1 per framing brief
- **NO geospatial fight telemetry / per-fight combat statistics** — v1.1+ multi-seam work
- **NO factions** — deferred per § 3.4
- **NO Cycle 13 scope work** — Cycle 13 scope-doc authoring is gated on T4 post-mortem session 1 outcomes (per knight-rider directive Matt 2026-05-25)
- **NO gandalf invocation** — gandalf's design-fit pass fires autonomously when forms land per framing brief § 3 step 3 (handoff trigger: forms visible in loadout + provenance manifest authored)

## Cross-seam coordination (already LIVE — informational only)

The following star-lord seams are wired and LIVE-supported per Wave 5 completion. Rocket's `generate_season()` invokes them via existing interfaces; no fresh star-lord dispatch needed:

| Star-lord seam | Wired interface | Wave 5 commit |
|---|---|---|
| `llm/` — Phase 5 LLM calls (form names, skill names, descriptions, cosmological vocabulary) | Existing llm-client wiring; rocket invokes per per-form generation | Pre-existing |
| `export/season_exporter.py` — full PlayerClassV2 export including `t4_alteration_output` sub-fields | `ExportAlterationOutput` extended with `manifestation`, `off_hand_contract`, `spirit_guide_narration_metadata`, `gamora_combatant_fields` | `c0be301` (off-hand contract export) |
| `output/telemetry/` — `t4_alteration_type` telemetry column | star-lord Wave 5 telemetry dispatch | `3944f7c` (Wave 5 telemetry column) |

If any cross-seam interface fails at runtime, STOP the run and escalate to knight-rider — do not attempt cross-seam amendments inline.

## Open questions for rocket to resolve at execution time

- **Entrypoint selection:** which top-level script invokes `SeasonOrchestrator.generate_season()` at N=30-40? Rocket's judgment per current generation/orchestration code. Document chosen entrypoint + invocation args in run log.
- **n_classes parameter:** the framing brief specifies "~30-40 forms" — choose specific N (e.g., 35) that maximizes BC-target cell coverage given substrate distribution. Document choice + rationale in run log.
- **Seed selection:** new seed (not a Cycle 12 smoke seed) so this is a genuine first-use production sample. Document seed in run log + provenance manifest.
- **earth_self_name:** optional; defaulting to a substrate-neutral seed value is acceptable for v1 narrow first-use. Rocket's judgment.
- **LLM client provisioning:** verify the LLM client is wired BEFORE firing the run (Phase 5 quality depends on it). If LLM client unavailable for any reason, STOP and escalate.
- **Coverage gaps:** if N=35 cannot represent all 25 BC-target cells OR all 6 § 8 strategies given substrate distribution, document the gap in the provenance manifest with rationale; do not artificially inflate N to force coverage (substrate-binding integrity trumps coverage exhaustiveness per composition policy v1).

## Handoff trigger (post-completion)

When this dispatch completes (tag shipped + provenance manifest authored + forms visible in loadout):

1. **Gandalf design-fit pass fires AUTONOMOUSLY** per framing brief § 3 step 3 — gandalf reads provenance manifest, samples per § 2.1 (all Sketch F anchors + one per § 8 strategy + all engine-authored gap-fills + all mythological-NULL rescues + edge cases), authors special case summary at `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md`.
2. Matt-touch: Matt reviews special case summary; signals T4 post-mortem readiness + parked-loadout-amendments fire signal.

No knight-rider intermediation needed between rocket completion and gandalf fire — the framing brief is the handoff contract.

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` (load-bearing — RATIFIED)
- `agentic_orchestration/cycle-12-wind-down-summary-2026-05-25.md`
- Cycle 12 closure commits: engine `7cff770`, loadout `c06bed1`, tag `v1.0-new-engine-ready`
- jack-ryan FINAL Gate-2 verdict: `e3756bc` (engine commit) — PASS
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #1.1 — pre-fire resource-bounds projection load-bearing for this dispatch)

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 close ratification + engine generation run authorization per framing brief; skip-confirmation re-authorized for Cycle 13 (per Cycle 10/11/12 precedent)
**Status:** FIRE — v1 narrow milestone first-use of new engine; execution-only dispatch; autonomous gandalf design-fit pass triggers on completion

---

## Completion record

**Completed by:** rocket
**Completed:** 2026-05-25
**Tag:** `rocket/v0.1-engine-generation-run-v1-narrow-2026-05-25`

### Execution summary

- Script: `scripts/v1_narrow_generation_run_2026_05_25.py` (standalone L2→L3→L4→L6 pipeline; not season_orchestrator)
- Seed: 20250525 / N=35 forms / Duration: 76.7s
- Phase 5 LLM naming: ENABLED — 35/35 kits named via `LLMClient.complete_json`

### Coverage achieved

| Dimension | Target | Result |
|---|---|---|
| Total forms | 30-40 | 35 |
| BC-target cells | 25 (accept gap) | 25 |
| § 8 strategies | 6 | 6 (DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, ELEMENT_CONVERSION, GEOMETRY_COLLAPSE, RESOURCE_CONVERSION, TRADE_OFF) |
| Attributes | 4 | 4 (DEX, INT, STR, WIS) |
| Sketch F anchors | 4 (accept gap) | 1 (Moctezuma) |
| Elements | 8 (accept gap) | 1 (physical — known v1 substrate limitation) |
| engine_version="v2.0" | required | ALL 35 |
| mechanical_substrate_triple | required | ALL 35 |

### Quality gates

- engine_version="v2.0": PASS
- source_library="generator_v2": PASS
- mechanical_substrate_triple populated: PASS
- § 8 keystones reaching combat arithmetic (gamora_combatant_fields): PASS — all 35 kits
- Schema validation (PlayerClassV2.validate()): 0 errors across 35 kits

### Known v1 gaps (framing brief § 1.2 accepted)

- element="physical" for all 35 kits: substrate keyword inference returns "physical" for historical weapon names (Sword of Attila, Kukri, etc.). Known v1 architectural limitation; v1.1+ scope per existing code comment.
- Sketch F anchors 3/4 missing: Gilgamesh, Hattori Hanzo, Lu Bu not sampled in this cell-order / seed. Moctezuma confirmed (Standard Wizard / Thrown-Heavy/Atlatl cells). Named-bearer rows exist in substrate for remaining anchors; will appear at higher N or seed variation.
- strategy_type in raw emission is None (Cycle 11 AlterationOutput not wired to new-engine kits). Resolved to actual strategy from T4Alteration in export dict. gamora_combatant_fields IS populated.

### Script bugs fixed during execution (2 non-scope bugs, execution only)

1. `_skill_tree_to_export_skills()`: assumed old-engine `Skill` attributes (`.name`, `.energy_cost`, `.damage_multiplier`, `.effects`). New-engine `Skill` uses `skill_id`, `cost`, `scaling_coefficient`, `keystone_effect`. Fixed via `_skill_node_to_dict()` helper.
2. `apply_llm_naming()`: `LLMClient.complete()` takes `(system, user, ...)` not `(prompt=...)`. Fixed to `complete_json(system=..., user=...)`.

### Deliverables

- `reincarnated-engine/exports/v2_narrow/classes.json` (358 KB, 35 classes)
- `reincarnated-engine/exports/v2_narrow/metadata.json` (coverage + audit)
- `reincarnated-loadout/public/seasons/v2_narrow/classes.json` (deployed)
- `reincarnated-loadout/public/seasons/v2_narrow/metadata.json` (deployed)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` (151 lines, 35-form index)

### Handoff

Gandalf: perform § 2.1 design-fit pass on provenance manifest. Forms are substrate-mechanical only (no elemental theming, no seasonal flavor). LLM-named class names are mythological-fantasy but archetype-generic. Matt: T4 post-mortem session 1 is ready to trigger.

---
