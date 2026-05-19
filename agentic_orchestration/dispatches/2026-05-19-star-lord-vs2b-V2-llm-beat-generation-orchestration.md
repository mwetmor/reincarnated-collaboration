# Dispatch — 2026-05-19 — star-lord — VS2b V2 LLM beat-generation call orchestration

**From:** knight-rider
**To:** star-lord (operational pipeline seam — LLM orchestration + cost telemetry + export OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when V1 schema field operational
**Estimated effort:** ~2–3 days star-lord
**Acceptance:** Per § Acceptance. Tag fires: `vs2b/v0.2-llm-beat-generation-operational`.
**Hive context:** VS2b hive — gated on V1 (rocket schema). V2 fills the field via per-class-per-season LLM call; V3 (drax) consumes via export packet.

---

## Context

Per `canonical/story/embodiment-display-loadout.md` § 15 "For rocket+star-lord" recommendation 3:

> Sequence the LLM beat-generation call relative to Stage 2 cosmological-vocabulary + Stage 3 cipher migration

V2 implements that LLM call orchestration. Folds into Stage 2 cosmological-vocabulary pipeline as a follow-on per spec (Stage 2 + Stage 3 already shipped 2026-05-16).

Beat generation is a per-class-per-season LLM call that takes:
- Class manifest fields (`embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `archetype_tag`)
- Per-season L3 cosmological vocabulary (post-Stage-3 cipher migration)
- Spec § 6 + § 7 prompt conventions (per gandalf beat quality rubric — forward-flagged but rubric refinement is post-V2)

Output: ≤40-word beat string written to V1's schema field.

---

## Required reading

In order:
1. V1 dispatch + design draft once authored: `reincarnated-engine/design/working-agreement/V1-embodiment-narrative-beat-schema-2026-05-19.md`
2. `canonical/story/embodiment-display-loadout.md` (full spec; particularly § 6 beat-quality conventions + § 7 exemplars + § 15 recommendations)
3. `canonical/story/embodiment-narrative-layer.md` § "Star-lord (LLM prompt construction)" subsection
4. Form-bias Stage 2 + Stage 3 dispatch completion records (`2026-05-16-star-lord-form-bias-stage-2-cosmological-vocabulary.md`, `2026-05-16-star-lord-form-bias-stage-3-cipher-migration.md`) — pipeline integration patterns
5. R8 disposition + theme-coalescence prompt (`agentic_orchestration/hive-mind/R8-theme-coalescence-prompt-2026-05-19.md`) — per-entity LLM call cost + prompt-engineering patterns
6. `canonical/19-llm-call-map.md` (post-R8-amendment; Phase A + Phase B)
7. `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` + `llm/AGENT_STATE.md`
8. `reincarnated-engine/src/reincarnated/export/MIGRATION.md` + `llm/MIGRATION.md`
9. `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.2 (V2)
10. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Math-before-code (Discipline #1)

Authoring required:

### Pipeline design draft

**Path:** `reincarnated-engine/design/working-agreement/V2-llm-beat-generation-design-2026-05-19.md`

Captures:

1. **LLM prompt construction** — per spec § 6 + § 7 + embodiment-narrative-layer doc; consumes class manifest + per-season L3 vocabulary; outputs ≤40-word concrete-sensory beat
2. **Call orchestration** — per-class-per-season invocation; folds into Stage 2 cosmological-vocabulary pipeline as follow-on (Stage 2 already shipped; V2 extends)
3. **LLM call topology** update — append to `canonical/19-llm-call-map.md`: `embodiment_narrative_beat_generation` per-class-per-season ~51 calls per season (or N_classes per season)
4. **Cost telemetry** — incremental LLM cost captured per-season ($ + call count) on the same per-mode tagging used in R8 (`baseline` / `inverted` / `inverted_no_naming` per disposition)
5. **Backfill strategy** for 5 shipped seasons — generate beats for already-shipped seasons + write back to season manifests. Idempotent.
6. **Anti-bias scaffolding** per spec § 6 + embodiment-narrative-layer Discipline #14 candidate: do NOT expose canonical-four element labels or humanoid-default action verbs as defaults in the prompt; use embodiment-aware vocabulary only.

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — export packet additive field; LLM call topology amendment; cost telemetry surface.

**MIGRATION.md REQUIRED:**
- Star-lord appends to `reincarnated-engine/src/reincarnated/llm/MIGRATION.md` (LLM call topology change)
- Star-lord appends to `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (export packet additive field consumption + emission)

**Round-trip smoke REQUIRED.** End-to-end fixture:
- V1 generator emits schema field → V2 LLM call writes beat → export packet contains beat → loadout consumer reads (V3 surface; can be mocked at V2 smoke time if V3 not yet shipped)
- Field-presence + beat-presence + canonical-four-leak check at each boundary

---

## Scope

- [ ] Pipeline design draft authored at `reincarnated-engine/design/working-agreement/V2-llm-beat-generation-design-2026-05-19.md`
- [ ] LLM prompt engineered per spec § 6 + § 7 (consume class manifest + per-season L3 vocab; output ≤40-word beat)
- [ ] Anti-bias scaffolding implemented (Discipline #14 candidate)
- [ ] Per-class-per-season call orchestration operational
- [ ] Stage 2 cosmological-vocabulary pipeline extended with beat-generation follow-on
- [ ] Cost telemetry per-season: $ + call count captured
- [ ] Backfill for 5 shipped seasons (generate beats + write to manifests; idempotent)
- [ ] Export packet emits `embodiment_narrative_beat` per class
- [ ] `canonical/19-llm-call-map.md` amended (star-lord routes via gandalf for canonical-doc amendment per ADR-004)
- [ ] MIGRATION.md appended at LLM + export seams
- [ ] Round-trip smoke per Principle 6
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request: `vs2b/v0.2-llm-beat-generation-operational`

---

## Acceptance criteria

- [ ] Pipeline design draft authored
- [ ] LLM beat-generation call operational + anti-bias scaffolding
- [ ] Backfill complete on 5 shipped seasons + idempotency verified
- [ ] Export packet emits beat per class
- [ ] LLM call map amended
- [ ] MIGRATION.md (LLM + export)
- [ ] Round-trip smoke
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on start + STATE at backfill completion + HANDOFF to drax V3 + completion STATE
- [ ] Tag: `vs2b/v0.2-llm-beat-generation-operational`

---

## Out of scope

- V1 schema field (rocket; upstream)
- V3 drax loadout surface (downstream consumer; separate dispatch)
- Beat-quality rubric authoring (gandalf; spec § 15 "For gandalf" item 2; not blocking V2 ship — V2 can ship with prompt-engineered baseline; rubric refines iteratively)
- Beat regeneration UI (out of VS2b per spec § 14)
- Localization (post-Phase-0)
- Demo-side beat surface (post-VS2b)
- Per-skill / per-monster beats (per-class-per-season only)

---

## Open questions for star-lord

- **LLM model + temperature** — L1 star-lord. Same model class as Stage 2 cosmological-vocabulary; low-temperature for stability per R8 Test 5 stability lessons. Document choice in design draft.
- **Prompt engineering iteration** — L1 star-lord initial; gandalf consult if quality regresses per beat-quality observations
- **Cost budget per season** — L1 star-lord. Incremental cost (~$0.02–0.05 per season per class; ~$1–2.50 per season aggregate at 51 classes). Surface in cost telemetry.
- **Anti-bias prompt scaffolding implementation** — L1 star-lord per spec § 6 + Discipline #14 candidate. Do NOT include canonical-four element words ("fire/earth/water/wind") in prompt; use embodiment-aware vocabulary derivative of substrate-identity declarations
- **Backfill failure handling** — L1 star-lord. Pattern P7 fail-loud on LLM call failure during backfill; re-runnable batch
- **Multi-shot stability** — L1 star-lord per R8 Test 5 pattern; verify 2-3 shot Jaccard ≥ 70% on representative class/season to confirm deterministic-enough generation. Document result.

---

## References

- V1 dispatch + design draft (upstream)
- `canonical/story/embodiment-display-loadout.md` § 6 + § 7 + § 15
- `canonical/story/embodiment-narrative-layer.md` § "Star-lord" subsection
- Form-bias Stage 2 + Stage 3 dispatch completion records
- `agentic_orchestration/hive-mind/R8-theme-coalescence-prompt-2026-05-19.md` (prompt pattern reference)
- `canonical/19-llm-call-map.md` (LLM topology; amended by V2)
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` + `llm/AGENT_STATE.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.2

---

## Autonomous-operation authority + activation gate

**Activation gate:** V1 lands (schema field operational; generator pipeline insertion point ready).

**Post-activation:** star-lord L1 within seam; gandalf consult on beat-quality if regression surfaces. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. V2 fills the field with the form's story; the L3 vocabulary becomes the player's surface; the canonical-four labels stay hidden where they belong.*
