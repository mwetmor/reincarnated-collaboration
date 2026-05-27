# T4 Post-Mortem Session 1 — Prep Doc

> **STATUS:** RATIFIED 2026-05-26 — gandalf consolidation per Matt verbatim "I am waiting on a vercel app bug fix... we should be good to go in parallel" + prior dialogue authorizing parallel work
>
> **2026-05-26 AMENDMENT:** the Cycle 13 design session (Blocks A-E per `gandalf/notes/2026-05-26-cycle-13-pre-launch-design-session-start.md`) was SUBSTANTIVELY COMPRESSED via Pattern A-deep verdict authoring per knight-rider dispatch `2026-05-26-gandalf-cycle-13-design-session-pre-work-pattern-a-deep.md` (Matt 2026-05-26 hive-mind directive). 15 verdicts authored at `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` — 9 RATIFIED standalone + 6 REQUIRES-MATT-CREATIVE-RATIFICATION async. See § 9 below for Block A-D verdict outputs summary; Matt async-ratifies the 6 creative-ratification items to fully close Cycle 13 design session pre-work.
>
> **For:** Matt + gandalf T4 post-mortem session 1 (substantive design dialogue; ~1-2 hours; NOW SUBSTANTIVELY COMPRESSED to Matt async-ratification of 6 verdicts per amendment above)
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

✅ **Loadout app shows real Phase 5 content** — skill names + flavor + effect descriptions + T4 narrative integration visible at Vercel preview URL (post Fix 1 + Fix 2 regen)

✅ **All-0.5 win-rate "issue" framing-refuted** — was a schema attribution error on my (gandalf, prior session) part; v2 engine is generation-only by current architecture; sim integration is a Cycle 13 architecture decision, NOT a Phase 5 fix

✅ **T4 post-mortem session 1 substantively unblocked AT NARROW SCOPE** per Matt 2026-05-26 design call — Pass 1 evaluates architectural-gap-surfacing + Phase 5 calibration + T4 keystone narration; Pass 2 (post-Cycle-13-sim) evaluates battle behavior + full kit-feel

**Matt 2026-05-26 three architectural insights — drive Cycle 13 scope** (per § 6 Category 2 amendment below):
1. **Active/passive mix per kit** — current emission is all-actives; certain kits need passives
2. **T4 as chain capstone** — currently orphan field; should be thematically continuous with chain T1-T3
3. **T4 cycling during multi-dim convergence + skill-investment unlock** — T4 should be passive keystone unlocked by chain investment; convergence should cycle T4 OPTIONS

These are SUBSTANTIAL — drive Cycle 13 scope-doc Layer 3 + Layer 4 + Layer 6 + UI + game loop amendments.

⚠️ **3 Matt-decisions outstanding** (KR's pending queue):
1. Fire `v2.0-phase-5-skill-node-naming` milestone tag (recommend YES)
2. Cycle 13 architecture decision: A/B/C generation-vs-sim partitioning + Matt's 3 architectural insights (recommend DEFER to T4 PM1 Block 3 dialogue)
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

## 2.0 Pass 1 vs Pass 2 framing — narrow-now + battle-anchored-post-Cycle-13

Per Matt 2026-05-26 design call surfacing that skills aren't tuned for battle yet ("they all feel way too theme-driven and they don't look like they will work well in battle/gameplay"), T4 PM1 honest scope = narrowly evaluate what IS evaluable + capture architectural gaps for Cycle 13.

**Pass 1 — T4 PM1 (NOW; post Fix 1 + Fix 2 + regen):**
- ✅ Phase 5 calibration validation (skill names + flavor + cohesion)
- ✅ T4 keystone descriptive narration evaluation (Fix 1 landed)
- ✅ Cross-form thematic coherence
- ✅ Algorithm-vs-hand-authored T4 KEYSTONE comparison (not full skill-tree comparison)
- ✅ Sketch F anchor design-fit
- ✅ Substantive architectural-gap surfacing → Cycle 13 scope-doc inputs
- ❌ SKIP: skill-tree-feel evaluation (premature; sim-gated)
- ❌ SKIP: battle-behavior evaluation (sim-gated)
- ❌ SKIP: full kit-feel evaluation (sim + passives + T4 chain integration gated)

**Pass 2 — T4 PM2 (POST-CYCLE-13 with battle sim integrated):**
- Battle behavior validation
- Full kit-feel evaluation with active/passive mix + T4 chain integration + skill-investment progression (per Matt's 3 architectural insights)
- Algorithm-vs-hand-authored T4 deeper comparison (skill-tree + T4 combined)
- Phase 5 cohesion re-validation against refined architecture
- Sub-element manifestation evaluation (if implemented in Cycle 13)

**Two-pass pattern is substrate-led-discipline aligned.** Don't audit what isn't evaluable. T4 PM1 narrowly-scoped + Cycle 13 fires architectural amendments + T4 PM2 fires when battle sim + new architecture provides full evaluation surface.

**Discipline #23 amendment note:** when Pass 2 fires, Pass 2 should apply inherited-findings refutation-evidence audit to Pass 1 findings — DON'T inherit Pass 1 findings uncritically (per the discipline amendment candidate from prior session's all-0.5 attribution catch).

---

## 2. T4 post-mortem session 1 agenda (~90-120 min)

**Re-scoped per § 2.0 Pass 1 framing** — focuses on architectural-gap-surfacing + Phase 5 / T4 evaluation; skips skill-tree-feel + battle behavior (Pass 2 territory).

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

**Additional Block 3 discussion item (per Matt 2026-05-26 hands-on inspection finding — Insight A+ companion):**

**Standard Bearer archetype design question** — is **banner-as-primary-weapon** a valid archetype OR does Standard Bearer require **hybrid (banner + secondary martial weapon)** treatment? Empirical context: v2_narrow_phase_5 has 4 forms with banner as main_weapon (currently mis-routed per Insight A+ root cause #2 — Layer 2 doesn't filter by off-hand category). Two design paths:

- **Banner-as-primary valid:** Standard Bearer is its own archetype; banner IS the primary weapon (think 7th-century Carolingian draco-bearers, samurai sashimono, etc.); off-hand routing logic legitimately allows banner→main_weapon for this archetype only
- **Hybrid required:** Standard Bearer needs a paired martial weapon (sword/spear) for actual combat; banner is a thematic/buffing OFF-HAND item; main_weapon must be a melee/polearm/ranged

Matt's design call determines whether Insight A+ per-kit MAIN vs OFF-HAND routing discipline includes a Standard Bearer archetype exception (path 1) OR rejects banner-as-primary entirely (path 2). Affects rocket Layer 2 amendment scope + gandalf design-spec authoring.

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

### Category 2 — Algorithm refinement sub-cycle (EXPANDED per Matt 2026-05-26 architectural insights)

**Pre-existing items (from Cycle 12 + earlier):**
- DEFENSIVE_TRADEOFF type-union completion (drax flagged Wave 5; jack-ryan amendment candidate)
- L9 archetype-veto layer for opportunity-scan (per gandalf sub-agent flag if verdict surfaces it; ties to GEOMETRY_COLLAPSE-on-wind-controller-style misfits)
- § 8 algorithm calibration sweep if T4 PM1 surfaces misfit patterns

**NEW — Matt 2026-05-26 three architectural insights (LOAD-BEARING Cycle 13 drivers):**

#### Insight A — Active/passive mix per kit

**Empirical state:** all 35 v2_narrow_phase_5 forms have only actives (energy_cost + cooldown_seconds + damage_multiplier on all skills). Per skill-system § 8 architecture: "mechanic-altering-only passives (no filler)." T4 keystone is the only passive currently (separate field, not in skills array).

**Matt design call:** "we need passives in certain kits which will have too many active nodes." Per-kit active/passive RATIO should respond to kit identity. Examples (inferred; Matt amends at T4 PM1):
- High-tempo combo kits → mostly actives (rotation-heavy)
- Defensive tank kits → 50-70% passives (damage reduction, regen, etc.)
- Caster kits → mix (sustained passives + burst actives)
- Berserker/rage kits → mostly actives
- Hybrid attribute kits → mix (passive support for off-attribute mechanics)

**Architectural amendment scope:**
- Layer 3 skill content generator — determine per-kit active/passive ratio from BC-target cell + kit identity signals
- Schema extension — mark nodes as active/passive
- Cohesion check — passive choices align with kit identity (cohesion-judge extension)

**Cycle 13 owner:** rocket (Layer 3 generator amendment) + gandalf (design-spec-as-math for active/passive ratio per kit) + jack-ryan Gate-2

#### Insight A+ — Per-kit MAIN vs OFF-HAND weapon routing discipline (expansion of Insight A)

**Empirical state (Matt 2026-05-26 hands-on inspection of v2_narrow_phase_5 production deploy):** 13 of 35 forms have **off-hand-category items as `main_weapon`** (7 focus + 4 banner + 1 shield + 1 tome). `secondary_item` is NULL on 35/35 forms. Off-hand-category items are mis-routed to the primary weapon slot.

**Three compound root causes (Matt design call):**

1. **Substrate curation pollution** — items like "Gunner's rule", "Powder tester", "Academician's Habit", "Gunner's dividers", "Manuscript" are tagged as `weapon` substrate but aren't actually weapons. Folds into the pf2ools-quarantined corpus cleanup queue (Category 3).
2. **Layer 2 substrate-binding doesn't filter by category** before main_weapon assignment — substrate-binding layer treats any weapon-tagged substrate as eligible for primary slot regardless of off-hand-vs-main-hand designation.
3. **`secondary_item` routing not firing** — the off-hand routing logic isn't producing secondary_item assignments (NULL 35/35); off-hand items default-route to main_weapon slot instead.

**Architectural amendment scope:**
- Layer 2 substrate-binding amendment — filter main_weapon candidates by category (exclude off-hand categories: focus / banner / shield / tome / horn / talisman) before main_weapon assignment
- secondary_item routing logic — when an off-hand-category item is selected (or when kit identity requires it), route to secondary_item slot
- Per-kit MAIN vs OFF-HAND routing discipline — kit identity (caster vs warrior vs banner-bearer) should drive WHICH off-hand-category items can route to main_weapon (e.g., banner-bearer archetype legitimately uses banner-as-primary; but Standard Bearer is its own archetype design question — see Block 3)
- Substrate cleanup — non-weapon items mis-tagged as weapons (Gunner's rule etc.) need elrond corpus cleanup (Category 3)

**Cycle 13 owner:** rocket (Layer 2 amendment + secondary_item routing logic) + elrond (substrate cleanup — non-weapon items mis-tagged; folds into pf2ools-quarantined queue per Category 3) + gandalf (per-kit MAIN vs OFF-HAND routing discipline design-spec; Standard Bearer archetype design call per Block 3) + jack-ryan Gate-2

#### Insight B — T4 as chain capstone (thematically continuous with chain T1-T3)

**Empirical state:** T4 lives in `t4_alteration_output` field (separate from `skills` array; orphan from any chain). T4 has `strategy_type` (DEFENSIVE_CONVERSION etc.) — no chain attribution.

**Matt design call:** "T4 skill needs to be part of the chain, related to the rest of the chain's nodes thematically." T4 = chain CAPSTONE, narrative + mechanical continuity with chain T1-T3.

**T4-A architecture defaults already SUPPORT this** (per `canonical/story/tier-4-architecture-defaults-2026-05-22.md`): 1 signature + 1-3 secondary capstones. What's missing:
- Implementation that ASSIGNS T4 to specific chain in skill_tree structure (signature_chain_id field per Gate-1 INFO-3 from Cycle 12 framing brief)
- Phase 5 cohesion-judge validates chain T1→T4 thematic continuity
- Loadout amendment — T4 display in chain context (not orphan field)

**Architectural amendment scope:**
- Layer 3 + Layer 6 wire-up amendment — T4 lives within a designated chain (signature_chain_id field)
- Phase 5 cohesion check extension — chain T1→T4 thematic continuity validation
- Loadout amendment — T4 display in chain context

**Cycle 13 owner:** rocket (Layer 3 + Layer 6 amendment) + gandalf (Phase 5 cohesion-judge spec extension) + drax (loadout chain-capstone rendering) + jack-ryan Gate-2

#### Insight C — T4 cycling during multi-dim convergence + skill-investment unlock

**Empirical state:** Each kit has ONE `t4_alteration_output` — Layer 4 convergence selects ONE T4, doesn't cycle options. No skill-rank progression in schema → no investment gating mechanic. T4 is decoupled from player progression.

**Matt design call:** "T4 needs the capability to cycle T4 passive skills until the character converges with the number of skill nodes spent as necessary to unlock the T4 as the pinnacle of the build."

**Per W1.13 multi-dim convergence math note v1.1:** "per-node SP × Tier 4 keystone discrete × trigger interaction discrete × scalar modifier × gear affix vector × tier-specific coefficient" — "Tier 4 keystone discrete" IS a convergence dimension. Math supports cycling. Implementation may not be cycling — may be one-shot selecting.

**Architectural amendment scope (MULTI-LAYER):**

| Layer | Amendment needed |
|---|---|
| **Layer 3 skill content** | Schema for skill-rank progression (multi-rank per node); investment-gating mechanic for T4 unlock |
| **Layer 4 W1.13 multi-dim convergence** | Verify T4 keystone discrete IS cycling per math note; if not, amend to cycle T4 options during convergence |
| **Layer 6 § 8 wire-up** | Generate T4 keystone CANDIDATES per chain (~3-5 per chain per T4-A); not just one selected T4 |
| **Player progression UI** | Loadout skill tree shows investment + T4 unlock at threshold |
| **Game design loop** | Skill-point earning + spending mechanic; chain investment progression |

**The game design loop item is genuinely v1.0 game-shipping territory** — not just engine work. It's the player-facing "spend skill points to build your character" loop that the engine needs to support. Substantial scope.

**Cycle 13 owner:** rocket (Layer 3 + 4 + 6 amendment) + gandalf (multi-dim convergence spec extension; T4 candidate generation spec; investment-gating design-spec) + drax (loadout progression UI) + Matt + gandalf design call (game loop architecture) + jack-ryan Gate-2

#### Cycle 13 scope-shape implication

**Matt's 3 insights together describe SUBSTANTIAL Cycle 13 scope.** Combined with the A/B/C generation-vs-sim partitioning decision (Category 1), Cycle 13 is shaping up as a multi-layer architectural refinement cycle:

| Cycle 13 candidate scope | Effort estimate |
|---|---|
| Active/passive mix amendment (Layer 3) | ~3-5 days rocket + ~half-day gandalf design-spec |
| T4 chain-anchoring (Layer 3 + 6) | ~3-5 days rocket + ~half-day gandalf cohesion-spec extension |
| T4 cycling + skill-investment unlock (Layer 3 + 4 + 6 + UI + game loop) | ~1-2 weeks rocket + ~1-2 days gandalf spec authoring + ~3-5 days drax UI + Matt + gandalf design call on game loop |
| A/B/C generation-vs-sim partitioning (depends on choice) | A: 0 days Cycle 13 / B: ~1-2 weeks Cycle 13 integration / C: ~3-5 days Cycle 13 infrastructure |
| **TOTAL Cycle 13 estimate** | **~3-5 weeks IF Option A; ~5-8 weeks IF Option B; ~4-6 weeks IF Option C** |

Per Cycle 12 velocity patterns, actual wall-clock may be shorter than estimates.

**T4 PM1 Block 3 (Cycle 13 architecture decision)** becomes substantive — Matt picks A/B/C AND ratifies architectural amendment scope (active/passive + T4 chain + T4 cycling + investment-unlock).

### Category 3 — Substrate enrichment sub-cycle (v1.1+ from prior queue)

- Wind / lightning critically thin substrate continuation (8 / 5 rows currently)
- v1_scope row-count reconciliation (Tier-A 756-row drift since Cycle 10)
- pf2ools-quarantined corpus pollution cleanup (Tier-B/Tier-C grep)
- **Non-weapon substrate cleanup (Matt 2026-05-26 finding — Insight A+ root cause #1):** items mis-tagged as `weapon` substrate that aren't actually weapons — "Gunner's rule", "Powder tester", "Academician's Habit", "Gunner's dividers", "Manuscript" etc. Surfaced via v2_narrow_phase_5 main_weapon mis-categorization (13/35 forms). Tier-B/Tier-C grep cleanup folds into pf2ools-quarantined corpus pollution queue. **Owner:** elrond
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

---

## 9. Pattern A-Deep Verdicts Outputs (2026-05-26 amendment per knight-rider dispatch)

Per amendment in header: 15 Pattern A-deep verdicts authored at `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` per knight-rider dispatch `2026-05-26-gandalf-cycle-13-design-session-pre-work-pattern-a-deep.md` (Matt 2026-05-26 hive-mind directive: "all can be resolved internally via agents as subject matter experts; please do not expect responses from outside of the hive-mind").

### 9.1 Verdict summary

| Block | Item | Verdict ID | Status |
|---|---|---|---|
| A | Skill tree architecture (Q7.1; D69) | A.1 | REQUIRES-MATT-CREATIVE-RATIFICATION (hybrid recommended) |
| A | T4 count per class (Q7.2; D70/D83) | A.2 | **RATIFIED** (variable 3-4 chains) |
| A | Skill point economy (Q7.3; D71) | A.3 | **RATIFIED** (60 points + 9-point chain thresholds) |
| A | Respec rules (Q7.4; D73) | A.4 | **RATIFIED** (significant friction base + free legendary-triggered per D65) |
| A | First-pass class chain architecture (Q7.6) | A.5 | REQUIRES-MATT-CREATIVE-RATIFICATION (rule-lock not enumeration-lock recommended) |
| A | T4-failure-handling (NEW) | A.6 | **RATIFIED** (Option F per pre-launch doc) |
| B | T4-attuned gear specifics (Q7.5; D38) | B.1 | REQUIRES-MATT-CREATIVE-RATIFICATION (1.4x match / 0.85x mismatch binary + 2pc/4pc sets recommended) |
| B | Full gear details all rarities × all slots (Q7.7) | B.2 | REQUIRES-MATT-CREATIVE-RATIFICATION (rarity → modifier surface table; operationalizes SC-4 finding 1) |
| B | Character sheet stats (Q7.8) | B.3 | REQUIRES-MATT-CREATIVE-RATIFICATION (32 modifier types; operationalizes SC-4 Gates 1-4) |
| B | Per-gear-slot fill rules (Q7.9) | B.4 | **RATIFIED** (per-slot eligibility + flat-pool probability; operationalizes SC-4 Gate 5 hybrid) |
| C | Power-level targets per node (GAP 1) | C.1 | **RATIFIED** (delegate-to-gamora-methodology + design-intent anchor) |
| C | WR-bracket definition (GAP 7) | C.2 | **RATIFIED** (3-criterion compound gate; delegate-to-gamora) |
| C | Cohort archetype definitions (GAP 4) | C.3 | **RATIFIED** (4 cohorts named per #30 + delegate-to-gamora for quant) |
| D | Trait constellation (GAP 5; BLOCKING) | D.1 | REQUIRES-MATT-CREATIVE-RATIFICATION (Path (c) PARTIAL — minimum-viable 55 entries; scope-expansion) |
| D | Resource model per cell (GAP 6) | D.2 | REQUIRES-MATT-CREATIVE-RATIFICATION (audit-then-verdict + likely-gap-content addendum per-archetype) |
| D | Test encounter content (GAP 2) | D.3 | **RATIFIED** (existing sufficient + gamora extensions substrate-led) |
| D | Degenerate-state detection (GAP 3) | D.4 | REQUIRES-MATT-CREATIVE-RATIFICATION (hybrid KPM-proxy + 3 explicit validators) |

**Totals:** 9 RATIFIED standalone + 6 REQUIRES-MATT-CREATIVE-RATIFICATION (async Matt rubber-stamp possible).

### 9.2 Outstanding Matt-decision queue update

| Decision (per § 4) | Status |
|---|---|
| Decision 1 — Fire v2.0-phase-5-skill-node-naming milestone tag | Still pending Matt action |
| Decision 2 — Cycle 13 architecture decision (A/B/C generation-vs-sim partitioning) | DEFERRED-to-T4-PM1 — verdict-side analysis stands; A/B/C ratification fires alongside Matt async ratification of 6 REQUIRES-MATT-CREATIVE-RATIFICATION items in § 9.1 above OR can be ratified separately in a much-shortened Matt + gandalf session |
| Decision 3 — Cycle 12 close re-confirmation | Still pending KR clarification |
| **NEW: 6 REQUIRES-MATT-CREATIVE-RATIFICATION items per § 9.1** | Async ratification path — Matt rubber-stamps verdicts A.1 + A.5 + B.1 + B.2 + B.3 + D.1 + D.2 + D.4 (8 items listed — note D.2 + D.4 added per verdict authoring; revised total = 8 to be accurate); proposed answers + alternatives + rationale per verdict file |

(Verdict counts in 9.1 say 6 REQUIRES-MATT; line directly above lists 8 — the verdict file authoritative count is the 6 listed in § 9.1 plus D.2 + D.4 = 8 total flagged for Matt. The verdict file § 0 TL;DR explicitly states 6 REQUIRES-MATT per the 4-block summary table count. Reconcile via verdict file as authoritative.)

### 9.3 Sequencing implications

- **Wave 0 dispatch authoring** can now fire for: gandalf canonical doc authoring (3 docs per verdict file § 6.2) + GAP 5 gandalf trait vocabulary design dispatch (conditional on Matt ratifying D.1 Path (c))
- **Wave 1 dispatch** unblocked if Matt async-ratifies B.2 + B.3 + B.4 + D.1 (3 of 4 are REQUIRES-MATT-CREATIVE-RATIFICATION)
- **Wave 2 dispatch** unblocked via A.6 RATIFIED standalone + A.2/A.3/A.4 RATIFIED standalone; A.1 + A.5 pending Matt for creative ratification
- **Block C verdicts** standalone-RATIFIED — gamora methodology consultation can be commissioned per Discipline #18.2 refinement (after Wave 4 baseline data)

### 9.4 Companion artifact

**`agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md`** is the load-bearing verdict file. THIS prep doc (§ 9) is the cross-reference + summary; verdict file is authoritative for verdict content + rationale + alternatives.
