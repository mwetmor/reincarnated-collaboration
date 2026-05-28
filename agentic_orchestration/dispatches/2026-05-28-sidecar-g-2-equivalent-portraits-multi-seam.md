# Dispatch — 2026-05-28 — Sidecar G-2-Equivalent: Per-kit portrait generation (legolas image gen + galadriel AI-tell inspection + drax Summary tab wiring; ~3-4 days)

**From:** knight-rider
**To:** legolas (image generation) + galadriel (AI-tell inspection) + drax (Summary tab portrait wiring)
**Approved by:** Matt 2026-05-28 verbatim parallel-firing authorization: "NEW Sidecar Dispatch (G-2-equivalent) — legolas image generation per surviving kit + galadriel AI-tell inspection (<5 fingers; same-outfit; standard AI-tells) + drax Summary tab portrait wiring (could fold into Dispatch C OR fire independently); fires post Wave 5 Step 1 (~3-4 days total)"
**Estimated effort:** ~3-4 days combined (legolas image gen ~1-2 days; galadriel AI-tell inspection ~0.5-1 day; drax wiring ~0.5-1 day)
**Acceptance:** Per-kit portrait images generated for surviving Wave 5 production season kits (or smoke-test subset); AI-tell inspection PASS per <5 fingers + same-outfit + standard AI-tell criteria; drax Summary tab portrait wiring (per Dispatch C spotlight slot fallback chain OR independent integration); composes with seasonal_hero spotlight Meshy embed Dispatch H (portrait = fallback static when Meshy fails)

**Gate:** Wave 5 Step 1 GENERATION completion (post gamora SC-7 PASS + Phase 3 + 4 + 5 + 7 cascade) — fires post surviving-kit set known. Parallel with gandalf Step 2 audit + Dispatch F + Dispatch C drax workstreams.

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** provide static portrait fallback for Summary tab seasonal_hero spotlight (Dispatch H Meshy embed gates on Matt manual rigging; portrait gives immediate player-facing visual surface). Composes with Dispatch C Summary tab faction-grouped re-architecture (portrait slots in faction cards + spotlight). G-2-equivalent because Cycle 14 lighter sidecar G-2 was the prior portrait sidecar precedent in drax Pattern-A response.

**Refutation conditions** (seam-owner surfaces if any apply):
- Image generation service (legolas selection) produces AI-tells beyond galadriel inspection threshold
- AI-tell inspection rejects > acceptable threshold of generated portraits (re-generation cycle may exceed budget)
- Drax portrait wiring conflicts with Dispatch C spotlight slot interface contract
- D-Sharpened invariance breaks (portrait reveals substrate-anchored named-personage identity that should be hidden)

## Context

**Authority chain:**
- Matt 2026-05-28 verbatim parallel-firing authorization
- Drax Cycle 14 Pattern-A response `a0a449e` (Summary tab spotlight + G-2 portrait fallback reference)
- Gandalf seasonal_hero H-5 hybrid spec (`574624a`) — Summary tab seasonal hero surface
- Dispatch H queued (Meshy embed; portrait = fallback static)
- Dispatch C firing in parallel (Summary tab spotlight slot consumes portrait when sidecar lands)

**D-Sharpened invariance LOAD-BEARING:** portraits represent Phase 5 LLM-named kits (uniform player-facing per D-Sharpened spec) NOT substrate-anchored named-personages (which remain hidden at engine layer). Galadriel inspection must verify portrait identity matches LLM-generated name + cohort + element, NOT substrate-anchored personage if one exists.

**AI-tell criteria** (per Matt verbatim):
- <5 fingers per hand
- Same-outfit across portrait set (visual consistency at Summary tab level)
- Standard AI-tells avoided (extra limbs / merged objects / impossible geometry / text artifacts / etc.)

## Required reading

**Legolas:**
- `agentic_orchestration/cycle-14-wave-5-season-001/` (Wave 5 production season output; surviving kits per `season_emit=True`)
- Existing G-2 sidecar precedent (if available — drax Pattern-A reference; legolas to surface)
- `.claude/skills/reincarnated-legolas-operating-procedure`

**Galadriel:**
- Generated portrait set from legolas at agreed staging path
- AI-tell inspection rubric (galadriel canonical authority)
- `.claude/skills/reincarnated-galadriel-operating-procedure`

**Drax:**
- Dispatch C Summary tab spec at `agentic_orchestration/dispatches/2026-05-28-drax-dispatch-c-summary-tab-faction-grouped-re-architecture.md` § Part 4 spotlight slot
- Dispatch H spec at `agentic_orchestration/dispatches/2026-05-27-drax-dispatch-h-summary-tab-meshy-embed-seasonal-hero.md` § Part 4 fallback handling
- `.claude/skills/reincarnated-drax-operating-procedure`

**Cross-cutting:**
- `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md` § 6.4 D-Sharpened invariance (substrate_anchored_personage NEVER surfaced)
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` § 10.2 Gate-2 grep audit pattern
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #41 + #42 + #44 + #45

## Discipline #46 compliance

- N/A — image generation + UI wiring; no DB queries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) legolas image generation service is available + appropriate for Cycle 14 v1 portrait scope; (2) galadriel AI-tell inspection rubric covers Matt's criteria (<5 fingers + same-outfit + standard AI-tells); (3) drax spotlight slot fallback chain accommodates portrait + Meshy embed + placeholder; (4) D-Sharpened invariance preserved across all 3 seams
- **Q2 refutation evidence to seek:** verify legolas image gen path available; verify galadriel inspection rubric matches Matt criteria; verify drax spotlight interface contract; smoke-test on small kit subset before full surviving-set run
- **Q3 outcome trigger:** if any seam-owner's framing exceeds Pattern-A scope OR cross-seam contract mismatch surfaces, invoke #44 framing-refusal + surface back to KR

## Scope — multi-seam

### Seam 1 — legolas: per-kit image generation (~1-2 days)

- [ ] Image generation per surviving Wave 5 production season kit (or smoke-test subset if Wave 5 surviving-set large)
- [ ] Input: kit metadata (Phase 5 LLM-generated name + element + cohort + cluster) from ExportFactionCluster
- [ ] Output: portrait images at staged path (your judgment on convention — e.g., `agentic_orchestration/cycle-14-wave-5-season-001/portraits/<kit_id>.png`)
- [ ] D-Sharpened invariance: image prompts use Phase 5 LLM-uniform name + element + cohort ONLY; NEVER substrate-anchored named-personage identity
- [ ] Per-image metadata sidecar (prompt + model + timestamp)
- [ ] **Apply Discipline #19 background-process pattern** for batch image generation (multi-image; may have wall-clock duration)

### Seam 2 — galadriel: AI-tell inspection (~0.5-1 day)

- [ ] Inspect legolas-generated portrait set per AI-tell rubric:
  - **<5 fingers per hand** check
  - **Same-outfit** consistency across portrait set (Summary tab visual coherence)
  - **Standard AI-tells** check (extra limbs / merged objects / impossible geometry / text artifacts / asymmetry)
- [ ] Per-portrait PASS / RE-GENERATE / REJECT verdict
- [ ] Surface RE-GENERATE candidates to legolas (single regeneration cycle max)
- [ ] Surface REJECT candidates (kit gets placeholder fallback at Summary surface OR drops from spotlight pool)
- [ ] **Apply Discipline #11 empirical-inspection** with visual rubric (galadriel canonical authority)

### Seam 3 — drax: Summary tab portrait wiring (~0.5-1 day)

- [ ] Spotlight slot consumes seasonal_hero portrait (post galadriel PASS)
- [ ] Faction card per-kit portrait surfacing (composition with Dispatch C faction-grouped layout)
- [ ] Fallback chain: portrait (post galadriel PASS) → placeholder if portrait REJECT / RE-GENERATE pending
- [ ] D-Sharpened verification at consumption: kit's portrait identity matches Phase 5 LLM-uniform name (NOT substrate-anchored personage if one exists)
- [ ] Composition with Dispatch C spotlight slot interface contract (portrait container expects `<img>` child)
- [ ] Composition with Dispatch H Meshy embed (when Meshy URL lands; iframe child replaces `<img>` child at runtime)

### Cross-cutting

- [ ] D-Sharpened invariance preserved across all 3 seams (substrate_anchored_personage NEVER surfaced; Gate-2 grep audit pattern per Wave 3 Seam 1 § 10.2)
- [ ] Discipline #45 vocab-lock CLEAN (no class/role/archetype non-exempt vocabulary in portrait metadata OR Summary tab labels)
- [ ] Discipline #41 substrate-led preserved (image generation uses substrate-emergent kit identity from Wave 5 output; not pre-authored taxonomy)
- [ ] D7 AI-tell compliance composition (gandalf Wave 3 Seam 1 § 8 specified ai_tell_compliance_score for LLM output; galadriel inspection is the visual analog for image output)

### Closure (per seam)

**Legolas:**
- [ ] Portrait set landed at staged path + per-image metadata sidecar
- [ ] AGENT_STATE update
- [ ] Discipline #19 background-process pattern compliance
- [ ] Completion record appended

**Galadriel:**
- [ ] AI-tell inspection report at `agentic_orchestration/galadriel/notes/2026-05-28-sidecar-portraits-ai-tell-inspection.md`
- [ ] Per-portrait verdict log
- [ ] AGENT_STATE update
- [ ] Completion record appended

**Drax:**
- [ ] Summary tab portrait wiring landed (composes with Dispatch C spotlight slot)
- [ ] Build verification (tsc -b + vite build clean)
- [ ] AGENT_STATE update
- [ ] Completion record appended

**Cross-cutting:**
- [ ] All 3 seams committed + pushed per Matt's per-cycle push pattern
- [ ] KR consolidates sidecar close

## Acceptance criteria (cross-seam)

- [ ] Legolas portraits generated for surviving Wave 5 kits OR smoke-test subset
- [ ] Galadriel AI-tell inspection PASS per <5 fingers + same-outfit + standard AI-tells criteria
- [ ] Drax Summary tab portrait wiring landed
- [ ] D-Sharpened invariance preserved across all seams
- [ ] Discipline #45 + #41 verified across all artifacts
- [ ] Per-seam completion records + commits + pushes per per-cycle pattern

## Out of scope

- Do NOT execute Wave 5 Step 1 GENERATION (gamora seam; sidecar fires POST Wave 5 Step 1 completion)
- Do NOT execute Dispatch H Meshy embed (drax seam; sidecar provides fallback static, NOT Meshy iframe)
- Do NOT execute Dispatch C faction-grouped re-architecture (drax seam; composition only — sidecar wires INTO spotlight slot Dispatch C provides)
- Do NOT modify Phase 5 LLM prompts OR THEMATIC_REGISTRY (gandalf seam LOCKED)
- Do NOT change ExportSeasonHero schema (star-lord seam LOCKED)

## Open questions (per seam)

- **Q-Sidecar-L1 (legolas):** image generation service selection — which provider/model fits Cycle 14 v1 portrait scope + AI-tell criteria + cost envelope? Your judgment + reference G-2 precedent
- **Q-Sidecar-G1 (galadriel):** AI-tell rubric authoritative source — your existing rubric OR new rubric per Matt criteria? Your judgment
- **Q-Sidecar-D1 (drax):** spotlight fallback chain priority — portrait > placeholder if Meshy URL not yet available; portrait remains as static fallback after Meshy URL provided. Your UX judgment on fallback transition

## References

- Matt 2026-05-28 verbatim parallel-firing authorization
- Drax Pattern-A response `a0a449e` (G-2 portrait fallback reference)
- Gandalf seasonal_hero H-5 hybrid spec `574624a` (D-Sharpened invariance)
- Wave 3 Seam 1 § 10.2 Gate-2 grep audit pattern
- Disciplines #11 / #19 / #41 / #42 / #44 / #45

---

## Completion record (three seams; KR consolidates cross-seam close)

### Seam 1 — legolas
(pending)

### Seam 2 — galadriel
(pending)

### Seam 3 — drax
(pending)
