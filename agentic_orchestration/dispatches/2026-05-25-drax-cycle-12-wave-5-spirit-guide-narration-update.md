# Dispatch — 2026-05-25 — drax — Cycle 12 Wave 5 Spirit Guide panel update (L6 narration metadata consumption)

**From:** knight-rider
**To:** drax (player-facing presentation seam — reincarnated-loadout React/Vite/Tailwind + reincarnated-demo Pixi.js)
**Approved by:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ includes cross-seam wiring per Gate-2-on-L3 INFO-D) + skip-confirmation re-auth 2026-05-25 + KR autonomously orchestrates per scope-doc § 1
**Estimated effort:** ~30-60 min drax (synthetic-agent throughput)
**Acceptance:** Spirit Guide panel updated to consume L6 narration_metadata field; existing Cycle 11 T4AlterationPanel + spirit-guide narration enhanced with L6 emission; null-safe for pre-L6 classes; 773 modules / 0 TS errors smoke maintained; Vercel preview READY (Q5 preview-only); no regression on Cycle 11 v1.0 M3 T4AlterationPanel display

---

## Context

Cycle 12 Wave 5 cross-seam follow-on fan-out. Rocket Layer 6 ✅ COMPLETE + Gate-2 ✅ PASS — emits Spirit Guide narration metadata per `t4_wireup.py` `emit_cross_seam_fields()` (per Gate-2 on L3 INFO-D obligation enumeration).

**This is enhancement** — Cycle 11 v1.0 already shipped M3 T4AlterationPanel + M6 T4ComparisonPanel + spirit-guide narration display (per drax/v0.1-cycle-11-m3-m6-t4-display-wave-3b-2026-05-25 at loadout commit b948d3d). The Cycle 11 implementation displays Tier 2 intent metadata (works regardless of L6 wire-up). L6 now adds richer narration_metadata that drax can consume to enhance the Spirit Guide narration content.

Per Cycle 11 Wave 3b dispatch: "If star-lord schema includes a narration field on AlterationOutput, consume that; otherwise drax static-maps strategy_name → human-readable narration template" — Cycle 11 implemented the static-template fallback. Cycle 12 L6 now ships the narration_metadata field; drax can consume it directly.

---

## Required reading before starting

- **`~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`** § v1.4-layer-6 — **PRIMARY load-bearing** — documents Spirit Guide narration metadata shape Layer 6 emits
- **`~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py`** — `emit_cross_seam_fields()` Spirit Guide narration emission
- `canonical/story/skill-system-2026-05-24.md` § 9 (spirit-guide explainer pattern — narration design substrate)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md` Bucket 5 (cross-seam SC-3 emission contracts)
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m3-m6-t4-display-wave-3b.md` + completion record (Cycle 11 v1.0 T4AlterationPanel + spirit-guide narration baseline)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-11-wave-3b-drax-m3-m6.md` (Cycle 11 v1.0 Gate-2 PASS — Tier 2 framing COMPLIANT throughout; drax existing implementation is sound foundation)
- `~/Games/reincarnated-loadout/src/components/SkillTree/T4AlterationPanel.tsx` (Cycle 11 v1.0 implementation — primary modification target)
- `~/Games/reincarnated-loadout/src/data/types.ts` (T4AlterationOutput interface — may extend for narration_metadata)
- `~/Games/reincarnated-loadout/AGENT_STATE.md` (drax seam state)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#8 schema validation at consumer boundary + #11 empirical inspection + #13a implementation-vs-intent drift — Tier 2 framing compliance verification)

---

## Math-before-code (per Discipline #1)

No new math. Display-layer enhancement consuming new field. Math note OPTIONAL.

---

## Scope (drax Spirit Guide panel update)

### Consumer-side schema extension

- [ ] Extend `T4AlterationOutput` interface in `types.ts` with optional `narration_metadata` field (consume from L6 emission shape per MIGRATION.md § v1.4-layer-6)
- [ ] Null-safe consumer pattern: `narration_metadata ?? null`

### Spirit Guide narration enhancement

- [ ] Update T4AlterationPanel.tsx Spirit Guide narration section:
  - Consume `narration_metadata` from `t4_alteration_output` (Layer 6 enrichment)
  - Fallback to existing Cycle 11 `thematic_rationale` field if `narration_metadata` absent
  - Fallback to § 9 template voice if BOTH absent (existing Cycle 11 behavior)
- [ ] Per Tier 2 framing compliance (per Cycle 11 Gate-2 verdict): maintain "Build Identity" + "Intent Metadata" framing; no over-promising mechanical effect
- [ ] Drax design judgment on UI layout (woven into M3 description vs distinct in-card element)

### Smoke + acceptance

- [ ] Build smoke: `npm run build` — 773 modules / 0 TS errors (or current baseline; no regression)
- [ ] Null-case smoke: pre-L6 classes (without narration_metadata) render gracefully (fallback to existing behavior)
- [ ] Populated-case smoke: classes with narration_metadata render enhanced narration
- [ ] Vercel preview deploy + verify READY (Q5 preview-only per Cycle 11; do NOT promote to production)
- [ ] No regression on Cycle 11 v1.0 M3/M6 T4AlterationPanel + T4ComparisonPanel + spirit-guide narration display (all 11 real seasons unaffected)
- [ ] Cycle 12 fixture (if available) renders new narration_metadata correctly
- [ ] AGENT_STATE.md updated with Cycle 12 Wave 5 enhancement checkpoint
- [ ] Tag: `drax/cycle-12-wave-5-spirit-guide-narration-update-2026-05-25`

---

## Out of scope

- Layer 6 emission contract changes (LOCKED; consume as-is)
- New display panels beyond Spirit Guide narration enhancement
- Production Vercel deploy (Q5 RATIFIED preview-only)
- Star-lord schema changes (separate cross-seam dispatch)
- Gamora sim consumer code (separate cross-seam dispatch)
- M2 off-hand display surface change (Q3 RATIFIED main-weapon-only for T4 post-mortem; SHOW_OFF_HAND_SLOT remains false until v1.0 production launch)
- Architectural amendments (escalate via KR per scope-doc § 5 if needed)
- v1.1+ items

---

## Acceptance criteria

- [ ] T4AlterationOutput interface extended with narration_metadata field (null-safe)
- [ ] T4AlterationPanel consumes narration_metadata with fallback chain (Layer 6 narration_metadata → Cycle 11 thematic_rationale → § 9 template voice)
- [ ] Build smoke PASS (no TS errors; module count maintained)
- [ ] Null-case + populated-case smoke PASS
- [ ] Vercel preview deploy READY (Q5 preview-only)
- [ ] No regression on Cycle 11 v1.0 M3/M6 baseline (all 11 real seasons + sample_season class_0001 fixture)
- [ ] Tier 2 framing compliance maintained (per Cycle 11 Gate-2 standard)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `drax/cycle-12-wave-5-spirit-guide-narration-update-2026-05-25`
- [ ] Auto-commit + auto-push per drax seam authorization (CLAUDE.md addendum + Cycle 12 push-per-wave LIVE)

---

## Open questions for the agent to resolve

- Whether narration_metadata is a string (replacing template) OR structured (e.g., dict with multiple narration angles); drax inspects rocket emission shape at MIGRATION.md § v1.4-layer-6 + t4_wireup.py emit_cross_seam_fields
- Whether enhanced narration replaces existing § 9 template fallback OR layers on top (drax design judgment per UI/UX)
- Whether drax also wants to consume L6 signature_chain_id (cross-chain T4 election) for enhanced display (e.g., highlight which chain is build-defining); drax judgment per Cycle 12 enhancement scope OR defer to v1.0 production launch

---

## Cross-seam impact

Round-trip: not applicable (consumer-only). Verifying L6 emission shape consumer-readable at drax side; if shape gap surfaces, flag to KR for rocket L6 amendment per scope-doc § 5.

If drax extends loadout consumer code with new behavior, that's drax-seam-only (no upstream contract change).

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-6 (PRIMARY)
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py`
- `canonical/story/skill-system-2026-05-24.md` § 9
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md`
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m3-m6-t4-display-wave-3b.md` (Cycle 11 v1.0 baseline)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-11-wave-3b-drax-m3-m6.md` (Cycle 11 Tier 2 framing standard)
- `~/Games/reincarnated-loadout/src/components/SkillTree/T4AlterationPanel.tsx`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification + skip-confirmation re-auth + KR autonomously orchestrates per scope-doc § 1
**Status:** FIRE — Wave 5 parallel-fire with star-lord + gamora cross-seam consumers; **ENHANCEMENT on Cycle 11 v1.0 baseline** (Cycle 11 implementation provides Tier 2 intent metadata floor; L6 narration_metadata enriches)

**Matt-touch sequence:** drax completes → KR captures in state file → integration smoke + jack-ryan Gate-2 on full new engine fires when all 3 cross-seam consumers land
