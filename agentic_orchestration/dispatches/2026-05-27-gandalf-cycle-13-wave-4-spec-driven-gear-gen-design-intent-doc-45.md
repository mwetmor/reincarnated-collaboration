# Dispatch — 2026-05-27 — gandalf — Cycle 13 Wave 4 Spec-Driven Gear Gen Design INTENT Canonical Authoring (Doc 45)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777`) UNBLOCKS Wave 4 dispatch authoring + Wave 3 CLOSED + WARN-pattern PRESERVED
**Estimated effort:** 2-4 hrs canonical authoring (mirror doc 43+44 Wave 2+3 pattern; rocket track focus for Wave 4 spec-driven gear gen; gamora sim cycling track is SC-7 methodology output not doc 45 scope)
**Acceptance:** NEW canonical doc 45 authored at `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` with spec-driven gear gen operationalization for rocket Wave 4 implementation + gear instances at all rarity tiers per partition design + tier 1+2 legendary/set T4-attunement annotation + triggered-passive added skills on legendaries per D55 + integration with Wave 1 partition schema (doc 42) + Wave 2+3 T4 architecture (doc 43+44) + composition with gamora SC-7 sim cycling track (separate seam)

## Context

Cycle 13 Wave 3 CLOSED 2026-05-27 (jack-ryan Wave 3 Gate-2 PASS verdict commit `99ec777`; WARN-pattern PRESERVED). Wave 4 dispatch authoring UNBLOCKED.

Wave 4 = spec-driven gear gen + T4 Phase 4 sim cycling per framing brief § 3 Wave 4 + doc 40 § 3 spec-driven gear gen + doc 40 D81 Phase 4 sim cycling + closeout § 3 Block B gear architecture lock. Two tracks:

- **Track A (rocket): spec-driven gear gen** — gear instances at all rarity tiers per partition design (doc 42); tier 1+2 legendary/set with T4-attunement annotation; triggered-passive added skills on legendaries per D55 high-probability rule
- **Track B (gamora): T4 Phase 4 sim cycling** — full sim cycling against multi-T4 architecture per D85; methodology output by gamora SC-7 (firing concurrently with this dispatch)

This dispatch authors design intent for **Track A (rocket spec-driven gear gen ONLY)**. Track B methodology is gamora SC-7 output (separate seam; firing in parallel). Doc 45 cross-references gamora SC-7 + flags any rocket-track data-field implications for sim cycling consumption.

**Per jack-ryan Wave 3 Gate-2 I5 carryover noted (Wave 4 drax cross-seam touch):** per-scope projection emission via `scope_projection_data` dict on T4CandidateV2 (Wave 3 W3.5 output) — drax cross-seam touch for Wave 4+ integration. Doc 45 may surface drax-consumption flag.

**Per jack-ryan Wave 3 Gate-2 I4 closure note:** Wave 2 Gate-2 WARN W1 (synthetic same-bucket test gap) ALSO closed per jack-ryan Wave 3 Gate-2 verdict (test PASSes in current run). No action needed.

## Required reading before starting

1. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 precedent + 3-category taxonomy + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan)
2. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (Wave 3 precedent + scope-dimension + 6-step selection algorithm + biggest-design-risk handling)
3. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition substrate; gear gen consumes per-slot affinity matrix + per-rarity grid + tier-restricted modifier surface + 6 principles)
4. `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + cell × node × cohort)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 (spec-driven gear gen architectural foundation per D7) + § 3.6 (per-rarity × per-slot grid) + D8 (gear instances at all rarities) + D33/D38/D51 (content-compositional attunement) + D48-D52 (legendary 4-tier + unique 4-tier + set 2-tier) + D55 (high-probability triggered-passive on weapons) + D56 (modifier-surface expansion legendary-exclusive)
6. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3 (Block B gear architecture substantive locks)
7. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` (Wave 3 Gate-2 PASS + I5 drax cross-seam touch flag)
8. Wave 1+2+3 rocket implementation files (engine commits `2aa6813` + `2445bad` + `7287b43` + `2e8bc33`):
   - `reincarnated-engine/src/reincarnated/generation/partition_schema.py` + `partition_modifier_pool.py` + `partition_roller.py` (Wave 1; gear gen consumes)
   - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (Wave 2+3; T4 attunement annotation source)
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 — all relevant)
10. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)
11. `agentic_orchestration/operating-procedures/canonical-doc-format.md` (canonical doc spec)

## Math-before-code (canonical authoring; no code)

NOT applicable — design intent authoring.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 45 is canonical design-intent artifact. (Wave 4 rocket implementation downstream WILL introduce cross-seam contracts via gear instance schema; downstream of THIS dispatch.)

## Scope

Author NEW canonical doc at: `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md`

Mirror doc 43+44 structure; ~12-14 sections; ~250-450 lines:

### Required sections (proposed; gandalf seam-owner adjusts as needed)

- [ ] **§ 0 TL;DR + § 1 architectural foundation cross-references** — doc 38 + 39 + 40 amended + 41 + 42 + 43 + 44 + closeout + jack-ryan Wave 3 Gate-2 as authority basis
- [ ] **§ 2 — Spec-driven gear gen operationalization** (per doc 40 § 3 D7) — algorithm produces gear instances per partition design (doc 42) at all rarity tiers
- [ ] **§ 3 — Per-rarity gear instance generation** (per doc 40 § 3.6 + closeout § 3.2 per-rarity × per-slot grid):
  - Common: 1-2 modifiers; categories 1-3 rollable
  - Uncommon: 2-3 modifiers; categories 1-6 rollable
  - Rare: 3-4 modifiers; categories 1-6 + 9 rollable
  - Epic: 4-5 modifiers; full 1-9 rollable; no added-skill
  - Legendary T0: 4-5 + Epic-exclusion modifiers (D56); chain-aligned added-skill
  - Legendary T0.5: higher density; chain-aligned added-skill
  - Legendary T1: higher density + T4-attunement annotation; chain + T4-attuned added-skill
  - Legendary T2: highest density + T4-attunement; chain + T4-attuned added-skill
  - Unique T0-T2: signature-mod patterns; per-tier added-skill
  - Set T1-T2 (endgame-only): per-tier + set bonus rank
- [ ] **§ 4 — T4-attunement annotation per content-compositional model** (per closeout § 3.4 + doc 40 D33+D38+D51 amended):
  - Annotation as metadata recording generation-time alignment intent (NOT toggle mechanism)
  - Gear content IS the attunement; magnitude IS content quality
  - Algorithm uses annotation for drop pool restriction (D50) + spirit-guide projection (D34) + algorithm-side optimization
  - Reference Wave 2+3 T4 architecture (Categories A/B/C + scope-dimension)
- [ ] **§ 5 — Triggered-passive added skills on legendaries (per D55 high-probability)** — algorithm specifies how legendaries generate triggered-passive content per slot family:
  - Weapons: spawns geometric AOE on hit; thorny on hit; etc.
  - Armor: on-being-hit triggers
  - Accessories: general passives + rare true-actives
  - Probability calibration starting anchors (per doc 40 D55)
- [ ] **§ 6 — Modifier-surface expansion at legendary (per D56)** — legendaries unlock NEW stat types Epic cannot roll; per-rarity expansion specification
- [ ] **§ 7 — Capability toolkit at legendary tier (per Wave 1 partition § 7 SC-4 Gate 5 LOCKED HYBRID)** — capability-toolkit-legendary-exclusive enforcement: multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill categories at legendary T0-T2 only
- [ ] **§ 8 — Set bonus structure (Set T1-T2 endgame-only)** — 4-piece sets standard (2pc minor always-active + 4pc full T4-attuned per closeout § 3.4)
- [ ] **§ 9 — Sub-wave structure W4R.0-W4R.X for rocket Wave 4 implementation** (mirror Wave 1/2/3 sub-wave pattern; ~5-7 sub-waves):
  - **W4R.0** — Substrate prep + repo-scaffold (review Wave 1 partition schema + Wave 2+3 T4 architecture)
  - **W4R.1** — Per-rarity gear instance generation algorithm
  - **W4R.2** — T4-attunement annotation per content-compositional model
  - **W4R.3** — Triggered-passive added-skill generation per D55
  - **W4R.4** — Modifier-surface expansion per D56 + capability toolkit at legendary
  - **W4R.5** — Set bonus structure (Set T1-T2)
  - **W4R.6** — Cross-cohesion validation per #26 + Block C (extend Wave 1+2+3 cross-cohesion to gear gen)
  - **W4R.7** — Round-trip smoke per Principle 6 (all 10 rarity tiers; including legendary_t0_5 carryover; verify scope_projection_data field consumed by drax-ready data structure)
- [ ] **§ 10 — Wave 4 implementation guidance for rocket** — concrete next-steps; integration with Wave 1 partition + Wave 2+3 T4 + gamora SC-7 sim cycling (Track B)
- [ ] **§ 11 — Composition with gamora SC-7 Track B** — gamora sim cycling consumes rocket gear gen output; doc 45 flags data-field implications for SC-7 (cross-reference SC-7 dispatch firing concurrently)
- [ ] **§ 12 — § 11 Discipline #23 framing-audit section** (INCLUDED FROM START per doc 44 § 11 precedent — avoid prior W1 amendment pattern)
- [ ] **§ 13 — Wave 4 close criterion** (rocket track) — jack-ryan Gate-2 PASS on rocket implementation; coordinated with gamora SC-7 Track B close
- [ ] **§ 14 — Sign-off**

### Discipline compose-check

- [ ] #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 — all relevant; compose throughout
- [ ] **§ 12 framing-audit INCLUDED FROM START** (per doc 44 precedent; avoid jack-ryan W1 amendment pattern)
- [ ] **WARN-pattern PRESERVED status** — Wave 3 maintained it; Wave 4 rocket implementation expectation: 100% accurate post-script empirical count assertions

## Acceptance criteria

- [ ] NEW canonical doc 45 authored at `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md`
- [ ] All 14 sections complete per § Required sections itemization (gandalf seam-owner may adjust)
- [ ] § 12 Discipline #23 framing-audit section INCLUDED FROM START
- [ ] Cross-validate against doc 40 § 3 + § 3.6 + D33/D38/D51/D55/D56 + closeout § 3 (no contradiction)
- [ ] Cross-reference gamora SC-7 Track B firing concurrently
- [ ] Tag intent: `gandalf: Cycle 13 Wave 4 spec-driven gear gen design intent canonical (doc 45; rocket track)`
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Track B gamora sim cycling design intent (SC-7 methodology output; separate seam)
- Rocket Wave 4 implementation (separate dispatch post-Gate-1)
- Jack-ryan Gate-1 critique on doc 45 (separate dispatch post-authoring)
- Wave 5 gauntlet sim + season gen + close (separate)
- Phase 5 cohesion coalescence (Cycle 14)
- Doc 40/41/42/43/44 modifications (cross-seam gandalf authority preserves)
- Production code modifications
- decisions-log entries

## Open questions for the agent to resolve

- Doc 45 numbering: 45 next available; confirm or pick alternate
- Section count: 14 proposed; adjust per scope
- Sub-wave structure W4R.0-W4R.7 proposed (8 sub-waves); adjust per scope
- Cross-track coordination with gamora SC-7: how explicit; recommend cross-reference only (SC-7 has its own seam ownership)

## References

- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 + D33/D38/D51/D55/D56 (foundation)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 substrate)
- `canonical/43+44-t4-algorithm-wave-2+3-intent` (Wave 2+3 precedent)
- `canonical/41-progression-framework-2026-05-27.md`
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md`
- Wave 1+2+3 rocket implementation (engine commits)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

**Cycle:** 13
**Wave:** 4 design intent (rocket track)
**Gates:** jack-ryan Wave 4 Gate-1 critique on doc 45 → rocket Wave 4 implementation dispatch authoring (post-Gate-1 PASS) → Wave 4 close (post-rocket-implementation Gate-2 coordinated with gamora SC-7 + Track B implementation)
**Priority:** P1 — critical-path Wave 4 start (rocket track; fires in parallel with gamora SC-7)
