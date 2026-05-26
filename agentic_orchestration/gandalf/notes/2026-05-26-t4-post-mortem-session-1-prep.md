# T4 Post-Mortem Session 1 — Prep Doc

> **STATUS:** RATIFIED 2026-05-26 — gandalf consolidation per Matt verbatim "I am waiting on a vercel app bug fix... we should be good to go in parallel" + prior dialogue authorizing parallel work
>
> **For:** Matt + gandalf T4 post-mortem session 1 (substantive design dialogue; ~1-2 hours)
> **Author:** gandalf (story-and-design steward)
> **Pattern:** consolidation + session-prep doc (NOT a duplicate design-fit pass — that already lives at the verdict cited below)

**Authority basis:**
- Phase 5 regen + design-fit pass complete (commit `2a73191`; gandalf sub-agent)
- Phase 5 milestone unblocked pending Matt-ratification (v2.0-phase-5-skill-node-naming tag)
- Loadout app shows real Phase 5 skill names + flavor + T4 narrative integration in preview URL (post rocket placement fix commit `cb52f91`)
- Matt 2026-05-26 authorization for consolidation + parallel work

**Companion docs (read order recommended):**
1. **`agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md`** — the substantive verdict (gandalf sub-agent design-fit pass on Phase 5 regen output; Finding 1 RESOLVED + Finding 2 FRAMING REFUTED; forward routing Tier 1/2/3)
2. `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` — original design-fit pass on v2_narrow + amended sections (Sketch F reframed per per-season anchor lock + all-0.5 framing error acknowledged inline § 3.7)
3. `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` — the spec that produced the Phase 5 regen
4. `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 5.4 — per-season anchor variability lock (Matt 2026-05-25 design lock)

---

## 0. TL;DR — what's ready for T4 PM1

✅ **Phase 5 calibration spec landed cleanly** — 0/289 placeholders; 91.3% first-attempt PASS; mean cohesion 0.838; strong cross-form differentiation

✅ **Loadout app shows real Phase 5 content** — skill names + flavor + effect descriptions + T4 narrative integration visible at Vercel preview URL

✅ **All-0.5 win-rate "issue" framing-refuted** — was a schema attribution error on my (gandalf, prior session) part; v2 engine is generation-only by current architecture; sim integration is a Cycle 13 architecture decision, NOT a Phase 5 fix

✅ **T4 post-mortem session 1 substantively unblocked** — Matt can evaluate skill-tree feel + T4 keystone narrative integration + cross-form patterns NOW; doesn't need sim integration to surface design-fit signals

⚠️ **3 Matt-decisions outstanding** (KR's pending queue):
1. Fire `v2.0-phase-5-skill-node-naming` milestone tag (recommend YES)
2. Cycle 13 architecture decision: A/B/C generation-vs-sim partitioning (recommend DEFER to T4 PM1 dialogue)
3. Cycle 12 close re-confirmation (was already closed yesterday via `v1.0-new-engine-ready` tag; clarify with KR)

---

## 1. Phase 5 regen status — per existing verdict (cite, don't duplicate)

Per `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` (commit `2a73191`):

### Finding 1 — placeholder issue — RESOLVED substantively

- 0/289 placeholders (vs 289/289 placeholders in v2_narrow original)
- 91.3% first-attempt PASS rate (target was ≥70% per spec § 6; substantially exceeded)
- Mean cohesion 0.838 (target was 0.75 acceptance threshold; substantially exceeded)
- Strong cross-form differentiation — Ember fire_mage family produced 4 genuinely distinct intellectual sub-archetypes per verdict § 2.4
- Cohesion-judge programmatic scoring AGREES with subjective design-fit read (drift check per verdict § 2.5)

**Residuals (v1.1+ scope per verdict § 2.6):**
- Within-kit lexical over-uniformization (form-022 Crimson Leaf X pattern)
- Form-layer duplicate (form-002 + form-027 Menuki Bladedancer cross-form duplicate; uniqueness gate candidate)
- Substrate-binding misfits at form level (specific cases per verdict)

### Finding 2 — all-0.5 win-rate "issue" — FRAMING REFUTED

**The cited fields (`actual_winrate`, `convergence_iterations`, `final_modifier`, `converged`) do not exist in v2 engine schema.** Per verdict empirical evidence:
- v2_narrow and v2_narrow_phase_5 have IDENTICAL balance_metadata keys
- Neither generation script invokes BalanceLoop / gauntlet / sim
- L3 skill generator REFUTED as failure candidate (real mechanical variance verified: damage_multiplier 1.05-1.249; cooldown + energy_cost variance; non-uniform bc_axis_contribution)

**Where my prior § 3.7 finding came from (honest acknowledgment):** I inherited the loadout app's BalanceMetadata TypeScript schema mental model and projected it onto v2 engine output without re-verifying schema. **Attribution error in my prior pass; self-corrected by gandalf sub-agent's framing-audit per Discipline #23.** Verdict OP § 4 amendment candidate: inherited findings deserve fresh Q2 (refutation-evidence) audit treatment, not just propagation.

**Verdict reframe:** v2 engine generation-vs-sim partitioning is a **Cycle 13 architecture decision** (3 options A/B/C per verdict § 3.5), NOT a Phase 5 problem to solve.

---

## 2. T4 post-mortem session 1 agenda (~90-120 min)

Recommended 4-block structure adapted from gandalf sub-agent's verdict § 5.1 framework:

### Block 1 — Phase 5 calibration validation (~20-30 min)

**Goal:** Matt evaluates substantive design-fit on real skill content.

**Walk through:**
- Open loadout preview URL (latest preview from commit `cb52f91`)
- Browse 3-5 forms across categories (Sketch F anchor; engine-original-mid-cohesion; cross-form-comparison pair)
- Recommended starting forms (per verdict empirical sampling):
  - **v2-form-025 Moctezuma's Jade Warlord** — highest-coherence form; Sketch F anchor; substantive narrative integration
  - **One Ember fire_mage** (per verdict § 2.4 cross-form distinction; 4 sub-archetypes in family)
  - **One engine-original with clean naming** (representative of bi-modal form library 68% engine-original mode)
  - **One with cohesion-judge BORDERLINE score** (per verdict residuals; subjective vs programmatic agreement check)

**Matt evaluates:**
- Does skill naming feel coherent with kit identity?
- Does T4 keystone narrative integration feel substantive vs decorative?
- Cross-form differentiation observable at skill-level?
- Cohesion-judge scoring agrees with your subjective read?

**Output:** Matt's qualitative assessment + flag any forms warranting amendment

### Block 2 — Hand-authored T4 alternative comparison (~30-40 min)

**Goal:** algorithm-vs-hand-authored comparison per T4-B reframe (Matt 2026-05-24 algorithm-as-v1-deliverable lock).

**Process:**
- Matt selects 3-5 forms from § 5 candidate list below
- Per form: Matt verbally + gandalf captures a HAND-AUTHORED alternative T4 keystone
- Compare algorithm output vs hand-authored:
  - Does algorithm fire reasonable strategy choice?
  - Would hand-authored offer meaningfully different player experience?
  - Where does algorithm shine vs need refinement?

**Output:** ~3-5 hand-authored T4 entries captured at `agentic_orchestration/gandalf/notes/2026-05-26-t4-hand-authored-alternatives.md` (post-session); design-fit deltas identified

### Block 3 — Cycle 13 architecture decision (~20-30 min)

**Goal:** Matt makes A/B/C generation-vs-sim partitioning call.

Per verdict § 3.5 + my prior recommendation:

| Option | Description | Best for |
|---|---|---|
| **A — Generation-only** | v2 stays generation-only; sim is a separate downstream cycle | Cleanest separation; aligns with Variant C engine-as-general-product + Option γ confirmation pattern; sim becomes its own cycle when needed |
| **B — Integrated sim** | v2 integrates sim per legacy season_001001 pattern; schema extends to carry sim outputs | Tighter coupling; matches legacy mental model; loadout app's BalanceMetadata schema becomes consumable from v2 directly |
| **C — Hybrid `--with-sim` flag** | Opt-in flexibility; supports both generation-only and integrated-sim modes | Most flexible; dev velocity benefit (inline sim for quick smoke during iteration); some operational complexity |

**Gandalf lean: Option A.** Reasoning per my prior post:
- Cleanest separation of concerns (generation vs validation)
- Aligns with Variant C engine-as-general-product framing
- Aligns with Option γ confirmation pattern (skip Layer 7 BDI test framework v1 → defer to v1.1+)
- Avoids tight coupling legacy pattern produced
- Sim can be its own Cycle 14+ workstream when warranted

**Counter-arguments worth weighing:**
- Option C (hybrid) if dev velocity benefits from inline sim during iteration
- Option B (integrated) if T4 PM1 reveals you genuinely want joint review of fight outcomes alongside skill content (less likely IMO given current observable scope)

**Output:** Matt's A/B/C decision → informs Cycle 13 scope-doc authoring + ADR-002 entry routing to jack-ryan

### Block 4 — Cycle 13 scope-doc input + close-out (~15-20 min)

**Goal:** capture T4 PM1 outcomes for Cycle 13 scope-doc authoring.

**Items to capture:**
- T4 keystone refinements surfaced (if any) → algorithm refinement candidate
- Phase 5 calibration refinements surfaced (if any) → calibration sweep candidate
- Substrate-binding misfits at form level (per verdict residuals) → substrate enrichment candidate
- Hand-authored T4 alternatives produced (Block 2) → T4-B catalogue authoring candidate
- A/B/C decision implications → architecture sub-cycle proposal
- Other v1.1+ items surfaced

**Output:**
- Matt-side decision queue cleaned up
- Gandalf has substantive input for Cycle 13 scope-doc authoring (~1-2 hr gandalf canonical authoring post-session)
- T4 post-mortem session 2 scheduled OR not (Matt's judgment per Block 2 hand-authored work pace)

---

## 3. Hand-authored T4 alternative candidate forms

Per verdict empirical sampling + my own design-fit reading, recommended candidates for Block 2 algorithm-vs-hand-authored comparison (Matt selects 3-5 from this list):

| Form | Why interesting candidate | Algorithm strategy elected | Hand-author angle |
|---|---|---|---|
| **v2-form-025 Moctezuma's Jade Warlord** | Sketch F anchor; highest-coherence form; algorithm RESOURCE_CONVERSION (Blood Magic) | RESOURCE_CONVERSION | Is RESOURCE_CONVERSION the right Aztec war-club keystone? Or would something more ritual-themed read better? |
| **One Ember fire_mage family form** (per verdict § 2.4 — 4 sub-archetypes) | Strong cross-form differentiation at skill-level; algorithm fired distinct strategies per sub-archetype | varies per sub-archetype | Does algorithm-chosen strategy align with sub-archetype intent? |
| **One cohesion-judge BORDERLINE form** (per verdict § 2.6 residuals) | Tests algorithm at the edge of acceptance | (per form) | Where does algorithm struggle; what would hand-author do differently? |
| **One Tier 3 v1.1+ residual form** (e.g., form-022 lexical over-uniformization OR form-002/027 Menuki duplicate) | Surfaces non-keystone design questions (naming + duplicates) alongside T4 evaluation | (per form) | Captures cross-cutting design feedback beyond just T4 |
| **One mythological-NULL-rescue form** (per Stage 4) | Tests algorithm on engine-generated mythological content | (per form; possibly elected via L9-refactored opportunity-scan) | Substrate-context engine-generated; does T4 keystone feel anchored or floating? |

**Matt selection note:** prioritize forms that surface design questions you specifically want to evaluate algorithm choices on. The hand-authoring is the substantive design comparison work.

---

## 4. Outstanding Matt-decisions (KR's pending queue + recommendations)

### Decision 1 — Fire `v2.0-phase-5-skill-node-naming` milestone tag

**Recommendation: YES.** Conditions satisfied per verdict + KR's reading:
- Gate-2 PASS-with-WARN
- Both WARNs cleared per rocket remediation
- Gandalf Finding 1 RESOLVED with substantial empirical evidence
- 91.3% first-attempt PASS + 0.838 mean cohesion

**Action:** send to KR "Fire `v2.0-phase-5-skill-node-naming` milestone tag."

### Decision 2 — Cycle 13 architecture decision (A/B/C generation-vs-sim partitioning)

**Recommendation: DEFER to T4 PM1 Block 3 dialogue.** Substantive design call deserves proper Pattern-B dialogue. My lean is Option A but better to think through with full T4 PM1 context.

### Decision 3 — Cycle 12 close re-confirmation

**Recommendation: CLARIFY with KR.** Cycle 12 was already CLOSED yesterday via `v1.0-new-engine-ready` tag (engine commit `7cff770` + loadout `c06bed1`). KR's "Cycle 12 close authorization" framing may be ambiguous — possibly meant "Phase 5 fast-follow milestone close" OR genuine re-confirmation.

**Action:** send to KR "Cycle 12 was officially closed yesterday via v1.0-new-engine-ready tag; Phase 5 regen is post-Cycle-12 fast-follow milestone (resolved via Decision 1 milestone tag fire). No additional Cycle 12 close action needed."

---

## 5. Lessons-learned — framing-audit discipline working as designed

**Honest gandalf self-reflection from prior session's all-0.5 attribution error:**

The original special case summary § 3.7 finding inherited the loadout app's BalanceMetadata TypeScript schema mental model and projected onto v2 engine output WITHOUT re-verifying schema. Gandalf sub-agent caught the error via Discipline #23 framing-audit on the inherited finding.

**Pattern observation:** when a prior pass surfaces a finding, subsequent passes should NOT inherit the finding's premises uncritically. Discipline #23 three-question protocol (Q1 framing assumptions / Q2 refutation evidence / Q3 refine vs execute) should fire on INHERITED findings too, not just original framings.

**OP § 4 amendment candidate** (per verdict + this prep doc):

> **Discipline #23 amendment proposal:** when a design-fit pass references findings from a PRIOR pass, the new pass should apply the three-question framing-audit to those inherited findings before acting on them. Inherited findings are NOT automatically valid — they are subject to the same refutation-evidence audit as original framings. Failure mode this guards against: projection of stale mental models / schema assumptions onto current empirical state without re-verification.

This amendment is canonical-authoring queue territory for gandalf OP § 4 next touch. Captured here for explicit recognition.

**Implication for T4 PM1:** if any T4 PM1 findings reference prior-session artifacts (special case summary, verdict, Cycle 12 framing brief, etc.), apply Discipline #23 + the inherited-findings amendment principle before acting on them.

---

## 6. Cycle 13 scope-doc inputs (preparation only; not authoring yet)

Per roadmap § 1.0 (2026-05-25) explicit deferral: "Cycle 13 scope-doc authoring DEFERRED until post-T4-post-mortem session 1 outcomes inform scope."

**Inputs that will inform Cycle 13 scope-doc** (consolidated from prior work + Phase 5 regen + this prep):

### Category 1 — Architecture sub-cycle (Tier 2; ADR-002 territory)

- A/B/C generation-vs-sim partitioning decision per T4 PM1 Block 3
- If Option A: sim integration becomes Cycle 14+ workstream
- If Option B: schema extension + sim integration in Cycle 13
- If Option C: hybrid flag implementation + opt-in sim infrastructure

### Category 2 — Algorithm refinement sub-cycle

- DEFENSIVE_TRADEOFF type-union completion (drax flagged Wave 5; jack-ryan amendment candidate)
- L9 archetype-veto layer for opportunity-scan (per gandalf sub-agent flag if verdict surfaces it; ties to GEOMETRY_COLLAPSE-on-wind-controller-style misfits)
- § 8 algorithm calibration sweep if T4 PM1 surfaces misfit patterns

### Category 3 — Substrate enrichment sub-cycle (v1.1+ from prior queue)

- Wind / lightning critically thin substrate continuation (8 / 5 rows currently)
- v1_scope row-count reconciliation (Tier-A 756-row drift since Cycle 10)
- pf2ools-quarantined corpus pollution cleanup (Tier-B/Tier-C grep)
- Substrate `element` column schema evolution (currently keyword-inferred)
- Substrate-tagging cleanup remainders (Subset C 94-row disposition; Greek/Norse period conventions)

### Category 4 — Phase coverage gaps sub-cycle

- Phase 6 visual coalescence production wire-up (Sidecar A image-pass-through verdict landed; production not done)
- Phase 7 joint-gate verification (status unclear pre-generation; may need explicit spec authoring)
- Phase 4 simplified archive math spec (gandalf canonical authoring; ~30-45 min)

### Category 5 — Loadout app enhancements (post-T4-PM1 fast-follow)

- `/the-work` analytics suite (per drax memo D1 deferred item)
- M1/M2/M5 verification (may already be shipped; verify post-T4-PM1)
- Per-fight-type telemetry instrumentation IF Option B/C architecture decided (swarmer/boss/etc.)

### Category 6 — Discipline amendments

- Discipline #23 amendment per § 5 above (inherited-findings refutation-evidence audit)
- Discipline #26 candidate (diagnostic triple-fire pattern per Cycle 11 BC-shift FAIL response)
- Export-target-discovery contract documentation (placement bug recurred TWICE — v2_narrow + v2_narrow_phase_5)

### Category 7 — Pi infrastructure execution (Matt "right moment")

- Decoupled from Cycle 13 scope per Matt 2026-05-25 deferral
- Surfaces when Matt schedules

---

## 7. What this prep doc does NOT decide

- Cycle 13 scope-doc actual content (gandalf authors post-T4-PM1 with outcomes informing scope)
- T4 post-mortem session 2 scheduling (Matt's call per Block 2 hand-authored work pace)
- Specific T4-B catalogue authoring (Matt + gandalf design call work; gated on T4 PM1 hand-authored alternatives outcome)
- Sim integration implementation (Cycle 14+ if Option A; Cycle 13 partial if Option B/C)
- ADR-002 entry authoring for architecture decision (jack-ryan territory post-Matt-A/B/C-decision)

---

## 8. Sign-off

**Author:** gandalf 2026-05-26 (consolidation + session-prep authored same-session as Phase 5 regen close + Matt parallel-work authorization)
**Status:** RATIFIED — for Matt + gandalf T4 post-mortem session 1
**Companion verdict (substantive design-fit pass):** `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` (commit `2a73191`; gandalf sub-agent; LOAD-BEARING for substantive findings; THIS doc is consolidation + session prep)
**Downstream:** T4 post-mortem session 1 (Matt + gandalf design call when scheduled) → Cycle 13 scope-doc authoring (gandalf post-session) → Cycle 13 fires when scope ratified

**For:** the Matt-facing T4 post-mortem session 1 prep — synthesizes what's ready, what's outstanding, session agenda (4 blocks ~90-120 min), hand-authored candidate forms, Cycle 13 scope-doc inputs, lessons-learned from prior session's framing-audit catch. Builds on (does not duplicate) the substantive Phase 5 regen design-fit pass verdict.
