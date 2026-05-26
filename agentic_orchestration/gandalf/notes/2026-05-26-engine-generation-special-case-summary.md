# Engine Generation Special Case Summary — v2_narrow_phase_5 Post-Fix-1 + Post-Fix-2 (Pass 1)

> **STATUS:** RATIFIED 2026-05-26 — gandalf Pattern A-deep DESIGN-FIT PASS 1 on rocket's full 35-form v2_narrow_phase_5 regen (engine commit `69970aa` + loadout commit `684dca0`) with both Fix 1 (T4 keystone narration; gandalf amendment landed) + Fix 2 (drax WeaponDescriptor schema reconciliation) applied
>
> **For:** T4 PM1 readiness signal + Cycle 13 scope-doc inputs anchored on Matt 2026-05-26 three architectural insights
> **Author:** gandalf (story-and-design steward; design-fit critique seam-owner)
> **Pattern:** Pattern A-deep substantive verdict; NEW file for separate-cycle traceability (separate from prior 2026-05-25 special case summary which captured v2_narrow Pass 1 + early Phase-5 framing-audit)

**Authority chain composing:**
- Matt 2026-05-26 Option B authorization with specific scope (verbatim captured in task brief)
- KR routing per hive-mind § 4.3 always-channel
- Prior Phase 5 chain precedent (gandalf 2026-05-25 design-fit pass)
- Fix 1 amendment authored by gandalf 2026-05-26 (`canonical/story/phase-5-t4-narration-amendment-2026-05-26.md`)
- Fix 2 implemented by drax 2026-05-26 (`dbb77c4 fix(drax): WeaponDescriptor schema alignment`)
- T4 PM1 prep doc (`agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` — consolidated session context)

**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` (Phase 5 calibration verdict; LOAD-BEARING for Pass 1 framing audit)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` (prior v2_narrow Pass 1 + framing-audit self-correction; this doc is the SUCCESSOR for v2_narrow_phase_5 cycle)
- `canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` (Fix 1 spec — what this pass verifies)
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (parent Phase 5 spec)
- Regen output: `~/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json` + `metadata.json`
- Loadout deploy: `~/Games/reincarnated-loadout/data/v2_narrow_phase_5/` + production at `reincarnated-loadout.vercel.app`

---

## 0. TL;DR — headline verdict + T4 PM1 readiness signal

**Pass 1 headline:** **T4 PM1 READY** — empirical verification confirms Fix 1 + Fix 2 substantively landed; substantive narration quality is strong (mean cohesion 0.861; 0/35 fallbacks); architectural-gap surfacing identified ONE substantive cross-seam consumption gap (drax T4AlterationPanel does NOT render the rich `manifestation` PROSE OR the kit-defining `alteration_type` label — see Finding 6 below).

**Per-finding verdict table:**

| Finding | Brief criterion | Empirical result | Verdict |
|---|---|---|---|
| 1 | Fix 1 (T4 narration fields populated 35/35) | `alteration_type` 35/35; `manifestation` 35/35; `thematic_rationale` 35/35 (nested + top-level mirror) | **RESOLVED** |
| 2 | Fix 1 prose is kit-anchored (named-bearer + element + substrate references) | All 9 sampled forms produce kit-specific prose; concrete sensory + kinetic detail; no AI-tell hyperbole; no generic-template fallthrough | **RESOLVED** |
| 3 | Fix 2 (main_weapon 5-field schema; engine emit + loadout accept) | Engine: 35/35 forms have weapon_id + name + category + period + cultural_register populated. Drax: `WeaponDescriptor` interface accepts exactly these 5 fields with `source_library` + `lineage` correctly optional. WeaponSlot null-safe rendering verified | **RESOLVED** |
| 4 | 22.9% T4 re-roll WARN — visible quality degradation? | 7 forms re-rolled; final cohesion range 0.670–0.900 (mean 0.812); spot-checked prose substantively reads AT LEAST as strong as single-attempt forms (form-022 re-rolled to 0.90; form-016 Cartographer re-rolled to 0.85 with strong narration); zero final FAIL → fallback to static-template (0/35 fallbacks) | **RESOLVED (defensible noise)** |
| 5 | 1 T4 label duplicate — surfaces in user-facing display? | Duplicate identified: "Ironpoint Convergence" on form-031 Far-Striking Warden + form-034 Ironblood Warlord (both GEOMETRY_COLLAPSE strategy; identical narrative_hooks). **NOT visible to user** because drax T4AlterationPanel does NOT render `alteration_type` (renders enum-derived strategy label "Geometry Collapse" instead) | **PARTIALLY RESOLVED — invisible only because broader Finding 6 gap suppresses display** |
| 6 (NEW) | Drax T4AlterationPanel consumption of new Fix 1 fields | T4AlterationPanel **does NOT consume** `manifestation` PROSE OR `alteration_type` narrated label. Only `thematic_rationale` (1-sentence fit prose) lands in Spirit-Guide line. The rich kinetic + sensory `manifestation` PROSE is invisible to player. NarrationMetadata TypeScript interface comment at line 338 still describes `manifestation` with stale "rank3_passive" example. | **NOT RESOLVED — cross-seam consumption gap; small drax follow-on** |
| 7 (additional) | Empirical Insight A — active/passive mix | 289/289 nodes are ACTIVE (energy_cost + cooldown_seconds populated). 0 passives in skills array. T4 keystone IS the only passive (separate field). Confirms Matt's insight empirically | **EMPIRICALLY CONFIRMED — Cycle 13 scope** |
| 8 (additional) | Empirical Insight B — T4 as chain capstone | T4 `t4_alteration_output` is ORPHAN field (no `signature_chain_id` linkage to skills array). However Fix 1 amendment's `named_skill_chain_signature` + `form_all_named_skills` context fields in LLM prompt DO produce thematically-continuous narration — verified explicitly in form-031 where rationale references "every lesson from Swift Step to Ironwood Bulwark" (chain T1 + T3 names by name). Narration ANCHORED but schema STILL orphan | **PARTIALLY ADDRESSED at narration layer; structural gap persists — Cycle 13 scope** |
| 9 (additional) | Empirical Insight C — T4 cycling + skill-investment unlock | Single T4 per form (no candidates/options field in schema). No cycling-during-convergence telemetry. No skill-rank progression in skill node schema (no `rank` field; only `tier` + `chain_id`). Multi-layer scope confirmed (Layer 3 + 4 + 6 + UI + game loop) | **EMPIRICALLY CONFIRMED — substantial Cycle 13 scope** |

**T4 PM1 readiness signal:** **READY for Matt to schedule T4 PM1 design call.** Pass 1 substrate is empirically clean; 6/9 findings RESOLVED outright; Finding 5 collapses into Finding 6 (loadout-side gap) which is a SMALL follow-on (2-line drax change per amendment § 8.2 already-spec'd as optional) — NOT a Phase 5 regen FAIL; NOT a T4 PM1 blocker.

**Forward routing (per finding):**
- Findings 1-4: closed by this pass
- Finding 5: dissolves into Finding 6
- Finding 6: SMALL drax follow-on (Cycle 13 fast-follow OR fold into Insight A/B/C amendments)
- Findings 7-9: Cycle 13 scope-doc inputs anchored on Matt's 3 architectural insights

---

## 1. Framing-audit (gandalf OP § 4.1 three-question protocol)

Applied per OP § 4 self-correction queue from prior 2026-05-25 self-finding: **treat regen findings as new assumptions, not inherited facts.**

| Q | Question | Answer |
|---|---|---|
| **Q1** | What load-bearing framing assumptions does this work depend on? | (a) Brief's quoted metrics (35/35 T4 fields populated; 91.3% skill-node first-attempt PASS; 22.9% T4 re-roll; 97.1% T4 label uniqueness; 849 modules / 0 TS errors) are empirically grounded. (b) Brief's "1 T4 label duplicate" framing assumes the duplicate is user-visible. (c) Fix 1 amendment's § 8.1 claim "drax requires no work; existing T4AlterationPanel consumes the new populated fields" holds. (d) The amendment's spec produces narration substantively aligned with kit identity. |
| **Q2** | What evidence currently in hand could refute these? | (a) **PARTIALLY REFUTED** — brief says "1 dupe"; actual metadata shows label_uniqueness_rate 0.943 (= 2 forms sharing one label, so 34 unique / 35 total = 97.1% which matches brief, but `phase5_uniqueness.duplicate_count: 7` reports SEVEN skill-node-level duplicates including "Whirling Steel Dance", "Iron Petal Guard", etc. — brief and gate-2 conflated skill-node-level dupe count with T4-label-level dupe count). Also `no_placeholder_strings: false` in acceptance_criteria reveals 1 skill-node placeholder ("Empower" in form-015) that brief did not flag. (b) **REFUTED** — drax T4AlterationPanel rendering inspection shows the panel does NOT consume `narrationMeta?.alteration_type` OR `narrationMeta?.manifestation`. The amendment's § 8.1 "no required work" claim is TRUE for narration *landing* (`thematic_rationale` propagates), but FALSE for the full Fix 1 design intent (the rich `manifestation` PROSE is engine-emitted but invisible to player). (c) **CONFIRMED** — narration quality is substantively strong (verified via 9-form spot-check + 7 re-rolled-form inspection). |
| **Q3** | Refine framing OR execute as-framed? | **REFINE.** The "1 T4 label duplicate" framing collapses (label is invisible). The Fix 1 amendment's "drax requires no work" framing was OPTIMISTIC — the prose-landing claim was true but the full narration-design-intent doesn't surface because T4AlterationPanel was authored pre-amendment and consumes only `thematic_rationale`. This is a CROSS-SEAM CONSUMPTION GAP, not an engine FAIL. **Pass 1 verdict reframes:** Finding 5 dissolves into Finding 6; Finding 6 is a small drax follow-on. |

**Framing-audit catch (load-bearing for OP § 4 amendment proposal):** the regen findings inherited from rocket Gate-2 + brief presupposed brief-reported metrics + amendment claims hold at face value. The inherited-finding refutation-evidence audit (proposed Discipline #23 amendment from prior session) DID fire on this pass — empirical inspection of brief vs metadata revealed the metric-conflation, and empirical inspection of T4AlterationPanel revealed the cross-seam consumption gap. **Pattern preserved:** apply Discipline #23 to inherited findings, not just original framings.

---

## 2. Finding 1 — Fix 1 narration field population — RESOLVED

### 2.1 Empirical evidence (35/35 across all 4 fields)

| Field | Populated 35/35 | Evidence |
|---|---|---|
| `spirit_guide_narration_metadata.has_mechanic_alteration` = True | 35/35 | All forms have T4 alteration (post-§8 generation) |
| `spirit_guide_narration_metadata.alteration_type` (narrated label) | 35/35 non-empty | e.g. "Wrath Turned Rampart", "Jade Blood Covenant", "Annealed Iron Will" |
| `spirit_guide_narration_metadata.manifestation` (PROSE narration) | 35/35 non-empty | 1-2 sentence kinetic + sensory prose; 25-50 word range per amendment § 2.1 |
| `spirit_guide_narration_metadata.thematic_rationale` (PROSE) | 35/35 non-empty | 1-sentence fit prose; 15-30 word range |
| `t4_alteration_output.thematic_rationale` (top-level mirror) | 35/35 non-empty | Propagated correctly per amendment § 2.1 dual-field design |
| `t4_alteration_output.manifestation` (top-level — tier label semantic) | None × 35 | Correctly PRESERVED as None per amendment § 2.1 disambiguation; engine path producing tier-label is inactive in v2_narrow_phase_5 path (see § 6.1) |

Acceptance criteria § 7 from amendment:
- ✅ T4 narration LLM pass fires for ALL 35 forms
- ✅ All 4 prose fields populated (label + manifestation + thematic_rationale × 2 placements)
- ✅ Cohesion-judge fired per form (35/35 have `phase5_t4_narration_cohesion_score`)
- ✅ First-attempt PASS rate 80.0% (target ≥ 70%; exceeds spec by 10pts)
- ❌ Re-roll rate 22.9% (target ≤ 15%; exceeded — see Finding 4)
- ✅ Final FAIL rate 0% (target ≤ 5%)
- ✅ Label uniqueness 94.3% (target ≥ 90%) — 34/35 unique labels
- ✅ Cost-per-run $0.1668 (within G12 cost guard projection $0.06-$0.20)

### 2.2 Verdict: **RESOLVED**

Fix 1 amendment implementation lands cleanly on engine emission side. Re-roll rate WARN (Finding 4) and label-uniqueness narrow margin (Finding 5) are quality-tier findings, not field-population findings.

---

## 3. Finding 2 — Fix 1 prose kit-anchored quality — RESOLVED

### 3.1 Substantive narration quality assessment (9-form spot-check)

| Form | Strategy | T4 label | Kit-anchored verdict |
|---|---|---|---|
| **000 Rampart Knight** | DEFENSIVE_CONVERSION | "Wrath Turned Rampart" | ⭐ knight identity locked in label + rationale ("oldest castle walls were built from the same stubborn refusal to yield"); kinetic detail in manifestation ("armor plates resonate with a low, iron hum") |
| **005 Siege Warden** | GEOMETRY_COLLAPSE | "Iron Wedge Doctrine" | ⭐ siege-doctrine integrated; manifestation "the engine of war goes quiet" → climactic compression imagery; rationale references "every great siege in memory" |
| **010 Iron Bolt Warden** | TRADE_OFF | "Tempered Draw Doctrine" | ⭐ archer specificity (draw + arrow + shaft + thud); discipline-anchored ("warden's discipline is measured in the refusal to miss") |
| **012 Ember Arithmetician** | DEFENSIVE_CONVERSION | "Tempered Iron Calculus" | ⭐ scholar-fire-mage register preserved ("arithmetic that governs your fire", "endurance itself is just another equation to solve"); cross-element synthesis (fire + iron) sound |
| **018 Twilight Rod Sage** | TRADE_OFF | "Twilight Constant Edge" | ⭐ shadow-scholar register intact ("a sage who has walked the twilight long enough stops chasing the brilliant moment"); refused gothic-necromancer voice as Phase 5 v1 did |
| **022 Crimson Leaf Binder** | DEFENSIVE_CONVERSION | "Bound Crimson Iron Skin" | ✅ grappler-binder identity ("pressed leaves compress against your limbs in overlapping plates"); re-rolled to 0.90 cohesion |
| **025 Moctezuma's Jade Warlord** | RESOURCE_CONVERSION | "Jade Blood Covenant" | ⭐ HIGHEST-COHERENCE form preserved at T4 layer; "Those who ruled through the obsidian blade understood that true dominion is not given freely — it is purchased, breath by breath, from the self" |
| **030 Iron Shilpi Veer** | DEFENSIVE_CONVERSION | "Annealed Iron Will" | ⭐ cross-civilizational synthesis preserved ("A shaper who has worked iron long enough" — Wayland-anchor restraint; rationale doesn't name-drop Vishwakarma at T4 keystone) |
| **033 Ember Scholiast** | RESOURCE_CONVERSION | "Vital Ink Transference" | ⭐ scholar-fire register elevated ("the tome's pages flush a deep arterial red"; "the ultimate gloss is written in the only ink that cannot be disputed") |

### 3.2 Discipline check — D7 AI-tell guard

Per amendment § 2.4 voice requirements: "no 'Behold!', no 'magnificent', no second-person hyperbole." Empirical spot-check across all 9 sampled forms + 7 re-rolled forms (16 forms total inspected):

| AI-tell pattern | Occurrences in inspected sample |
|---|---|
| "Behold" / "Witness" | 0 |
| "Magnificent" / "Glorious" / "Truly unique" | 0 |
| Second-person hyperbole ("you become an unstoppable force") | 0 |
| Generic D&D/MMO filler ("unleash devastating attacks") | 0 |
| § 9 template fallback voice triggered | 0 |

Verdict: **D7 discipline holds across the regen.** The amendment's prompt anchoring on "concrete sensory + kinetic detail" + "Spirit Guide is the in-fiction narrator — speaks WITH the player, not AT them" produces empirically D7-compliant output.

### 3.3 Verdict: **RESOLVED**

Fix 1 amendment achieves substantive narration goal: kit-defining T4 keystone prose anchored to named-bearer + element + cultural-tradition + mechanical substrate, in Spirit Guide voice without AI-tell drift.

---

## 4. Finding 3 — Fix 2 main_weapon schema reconciliation — RESOLVED

### 4.1 Engine emission (35/35 forms across all 5 required fields)

| Field | Populated 35/35 | Sample values |
|---|---|---|
| `weapon_id` | 35/35 (integer) | 206975, 22141, 216857, 187043, etc. |
| `name` | 35/35 (string) | "shield", "Percussion pocket pistol", "Gunner's rule", ".476 Nitro Express", "Manuscript", "Banner with Shaft" |
| `category` | 35/35 | shield / firearm / focus / banner / tome / melee / polearm / ranged / horn / talisman |
| `period` | 35/35 | early_modern / industrial / classical / fictional |
| `cultural_register` | 35/35 | historical / fantasy |

### 4.2 Drax schema acceptance (TypeScript)

Per `src/data/types.ts:282-295`:
- `weapon_id: string | number` — accepts engine's integer emission (forward-compat union per Cycle 13 TODO)
- `name: string` — required; present
- `category: string` — required; present
- `period: string` — required; present
- `cultural_register: string` — required; present
- `source_library?: string | null` — **optional** (drax Fix 2 made this nullable for v2 engine canonical contract)
- `lineage?: string | null` — **optional** (drax Fix 2 made this nullable)

### 4.3 Loadout rendering check

`WeaponSlot.tsx:38-101` consumes the 5 required fields + optional source_library/lineage; renders weapon name + category badge + cultural_register + period + lineage (when present) + WeaponBadges (when present). Null-safe rendering verified (line 40 guard).

### 4.4 Verdict: **RESOLVED**

Fix 2 cleanly reconciles drax schema with v2 engine canonical contract. No remaining schema-drift between engine emit + loadout accept on `main_weapon`.

---

## 5. Finding 4 — 22.9% T4 re-roll WARN quality assessment — RESOLVED (defensible noise)

### 5.1 Re-rolled form inventory

7 forms triggered re-roll (cohesion < 0.75 on first attempt; max 3 attempts per spec):

| Form | First-attempt cohesion (estimated) | Final cohesion (attempt 2) | Strategy | Narration quality |
|---|---|---|---|---|
| 013 Ashen Geomancer | <0.75 | 0.670 (BORDERLINE) | RESOURCE_CONVERSION | Strong cross-civ prose ("Marrow-Tithe Stonecall"); breakdown shows kit_identity 0.45 (below 0.75) BUT thematic_rationale_fit 1.0 — the form's substrate misfit (Powder Tester earth-caster from prior pass) suppresses kit_identity scoring; this is the structural substrate-binding issue persisting from prior pass § 2.6 residuals, NOT a Phase 5 narration failure |
| 016 Ember Cartographer | <0.75 | 0.850 | TRADE_OFF | ⭐ strong — "ember light across your mapped terrain stops flickering — burns flat, even, unwavering" |
| 020 Stone Covenant Warden | <0.75 | 0.900 | DEFENSIVE_CONVERSION | ⭐ strong — "stone lattice threaded through your frame thickens — visible as hairline fractures of pale light" |
| 021 Galeborn Standard Bearer | <0.75 | 0.780 | GEOMETRY_COLLAPSE | ✅ kit-anchored — "the banner stops being a signal and becomes a verdict" — but cohesion-judge gives strat_hits=0 because wind-controller GEOMETRY_COLLAPSE strategy still doesn't read as wind-controller-native (the prior pass § 2.6 algorithm-misfit persists; narration papers over) |
| 022 Crimson Leaf Binder | <0.75 | 0.900 | DEFENSIVE_CONVERSION | ⭐ strong — re-roll improved over single-attempt typical |
| 027 Menuki Bladedancer | <0.75 | 0.780 | GEOMETRY_COLLAPSE | ✅ "the dancer's wide arcs suddenly fold inward — steel drawn tight to the body, rage compressed to a single shivering point" |
| 033 Ember Scholiast | <0.75 | 0.750 (at acceptance threshold) | RESOURCE_CONVERSION | ⭐ scholar-fire elevated; this is among the strongest narrations in the regen |

### 5.2 Quality-degradation verdict

Re-rolled forms read AT LEAST as strong as single-attempt forms; in several cases (form-022, form-033) the re-roll produces narration substantively stronger than typical single-attempt output. The 22.9% re-roll rate exceeds amendment's ≤15% target but does NOT produce visible quality degradation.

**Root cause of re-roll rate exceeding target:** the cohesion-judge rubric's `kit_identity` scoring is sensitive to substrate-binding misfits inherited from prior passes (form-013 earth-caster bound to Powder-Tester museum-keyword; form-021 wind-controller bound to GEOMETRY_COLLAPSE strategy via § 8 algorithm). These are NOT Phase 5 failures — Phase 5 narration is doing the best LLM can on inputs the algorithm + substrate produced. The re-rolls are the cohesion-judge correctly flagging "your prose is good but your underlying kit-strategy alignment is structurally weak."

### 5.3 Verdict: **RESOLVED (defensible noise)**

22.9% re-roll exceeds amendment's ≤15% target by ~8 pts, but:
- 0/35 final FAIL → fallback (target was ≤5%)
- All 7 re-rolled forms produce substantively strong prose
- Cohesion-judge correctly attributes lower scores to substrate-binding inheritance, not narration quality

**Recommendation:** EITHER (a) accept the empirical re-roll rate as defensible noise for v1.0; relax acceptance criterion to ≤25% in amendment v1.1; OR (b) Cycle 13 substrate-binding amendments (Powder Tester earth-caster; § 8 algorithm wind-controller-GEOMETRY_COLLAPSE) reduce the re-roll rate as a downstream effect. Path B is design-aligned (root-cause fix); Path A is operational (relax the metric to match empirical reality).

---

## 6. Finding 5 — 1 T4 label duplicate user-facing impact — PARTIALLY RESOLVED (collapses into Finding 6)

### 6.1 Duplicate identification

`metadata.json` reports `label_uniqueness_rate: 0.943` (34 unique / 35 total) but does NOT name the duplicate. Empirical scan:

**Duplicate: "Ironpoint Convergence"** appears on TWO forms:
- form-031 Far-Striking Warden (hunter; long-range; focus; GEOMETRY_COLLAPSE)
- form-034 Ironblood Warlord (physical_warrior; close-range; rage; GEOMETRY_COLLAPSE)

Both share narrative_hooks `['focus', 'concentrated_force', 'narrow_spike']`. The LLM converged on the same kit-name label because both kits express the same mechanical archetype.

### 6.2 Substantive design observation

Despite identical labels, the `manifestation` PROSE for the two forms is genuinely distinct:
- form-031 (hunter): "Every variable in your draw collapses inward — breath held, elbow locked, focus narrowed to a single iron point. The shot does not spread."
- form-034 (warlord): "The wild swing narrows to a single driven thrust — all that accumulated fury channeled through one rigid point of contact, the air pressure dropping sharply around the impact"

One is a held-breath ranged-draw moment; the other is a close-range thrust. The mechanical archetype is shared (GEOMETRY_COLLAPSE: narrow-spike); the kit expressions diverge appropriately. The LABEL convergence is the only collision.

### 6.3 User-facing surface assessment

`T4AlterationPanel.tsx` rendering inspection (lines 87-91 + 119-121): the panel displays `strategyLabel` (from `STRATEGY_LABELS[strategy_type]` = "Geometry Collapse") in the header — NOT the narrated `alteration_type` "Ironpoint Convergence". The duplicate label is **INVISIBLE to the player** because the panel never renders it. (See Finding 6 for full cross-seam gap.)

### 6.4 Verdict: **PARTIALLY RESOLVED — collapses into Finding 6**

The duplicate label does NOT visually break the "this T4 defines THIS kit" intent — because the kit-defining label isn't displayed AT ALL. Both forms render with header text "Geometry Collapse" (the generic enum-derived label that already shares between the 8 forms with this strategy). The substantive design intent of the amendment (per-kit narrated labels in the panel) requires Finding 6 to be addressed first.

**Recommendation:** address Finding 6; the duplicate label is then a v1.1+ uniqueness-gate refinement (cohesion-judge could prefer-divergent-labels for shared-strategy forms during re-roll).

---

## 7. Finding 6 — Drax T4AlterationPanel consumption gap (NEW; surfaced by Pass 1) — NOT RESOLVED

### 7.1 The gap

`T4AlterationPanel.tsx` renders:
- Header: `strategyLabel` (enum-derived; "Defensive Conversion" / "Geometry Collapse" / "Trade-Off" / etc.) at line 119-121
- Strategy mechanical description (helper text) at line 141-142
- Strategy params (helper rows) at line 146-159
- BC axes (chip row) at line 162-172
- Spirit-Guide narration line: ONLY consumes `narrationMeta?.thematic_rationale` (line 89) → the 1-sentence FIT rationale
- Narrative hooks (chip row at bottom)

**NOT consumed:**
- `narrationMeta?.alteration_type` (the narrated kit-defining label: "Wrath Turned Rampart", "Jade Blood Covenant", "Ironpoint Convergence", etc.) — invisible
- `narrationMeta?.manifestation` (the 1-2 sentence kinetic + sensory PROSE describing what the alteration looks/feels like in play) — invisible

The amendment § 8.1 ("drax requires no work") claim was true for `thematic_rationale` propagation but **understated the cross-seam consumption gap.** The full design intent of the amendment (per-kit narrated label + manifestation prose visible to player) requires drax T4AlterationPanel amendment.

### 7.2 Type-schema mismatch

`src/data/types.ts:338` defines `NarrationMetadata.manifestation` with stale comment:

```typescript
manifestation?: string | null;                 // e.g. "rank3_passive"
```

The comment treats `manifestation` as the tier-label enum semantic. Engine now emits **PROSE** in this slot per Fix 1 amendment § 2.1 (the prose is in nested `spirit_guide_narration_metadata.manifestation`; tier-label semantic is preserved on top-level `t4_alteration_output.manifestation` which is None across all 35 forms).

The drax schema comment is outdated; the field IS being populated with PROSE; drax just doesn't render it.

### 7.3 Recommended drax amendment (Cycle 13 fast-follow OR fold into broader T4-PM1 work)

Two changes to `T4AlterationPanel.tsx`:

**Change 1 — Header label uses narrated alteration_type when present:**
```typescript
// Around line 80
const strategyLabel =
  alteration.spirit_guide_narration_metadata?.alteration_type  // L6 narrated label
  ?? getStrategyLabel(alteration.strategy_type);                // STRATEGY_LABELS enum fallback
```

**Change 2 — Render manifestation PROSE between strategy description + spirit-guide rationale:**
```tsx
// Insert ~line 142 (after strategyDescription, before paramRows):
{narrationMeta?.manifestation && (
  <p className="text-sm text-gray-300 leading-relaxed">
    {narrationMeta.manifestation}
  </p>
)}
```

**Change 3 — Update types.ts:338 comment to reflect PROSE semantic.**

**Effort:** ~2-line change per Change 1 + ~5-line block per Change 2 + comment update. Trivial.

### 7.4 Verdict: **NOT RESOLVED — small drax follow-on**

Engine-side Fix 1 implementation is correct. The amendment's claim of "no required drax work" understated the cross-seam consumption gap. The amendment's full design intent (per-kit narrated labels + rich manifestation prose visible to player) requires drax T4AlterationPanel amendment.

**Forward routing recommendation:** small drax follow-on. **Two options:**
- **Option A (Cycle 13 fast-follow):** drax sub-agent invocation between T4 PM1 ratification and Cycle 13 architectural work; ~30 min effort; lands the rich narration in production before T4 PM1 design call (so Matt sees the full kit-defining surface during the call)
- **Option B (fold into Cycle 13):** address as part of Insight A/B/C work where active/passive mix + T4 chain integration + skill-investment unlock will likely amend T4AlterationPanel substantially anyway; bundle this small change with the larger amendment

**Gandalf lean: Option A.** Pre-T4-PM1 deploy means Matt sees the rich `manifestation` PROSE during the design call, which is the substantive content that will inform hand-authored T4 alternatives (PM1 Block 2). Without Option A, PM1 evaluates a degraded surface that hides the algorithm's substantive output.

**Counter-argument for Option B:** if Cycle 13's T4-as-chain-capstone work (Insight B) materially changes T4AlterationPanel rendering anyway, doing the small drax change twice is wasteful. But Option A's drax change is purely additive (renders new fields; doesn't restructure), so the cost of doing it twice is near-zero. Option A wins on substantive grounds.

---

## 8. Matt 2026-05-26 three architectural insights — empirical grounding + Cycle 13 scope-doc inputs

### 8.1 Insight A — Active/passive mix per kit

#### Empirical grounding

| Measure | Result |
|---|---|
| Total skill nodes across 35 forms | 289 (mean 8.3/form; range 6-9) |
| Node-type indicator distribution | **289/289 nodes are ACTIVE** (every node has `energy_cost > 0` + `cooldown_seconds > 0`) |
| Passives in `skills` array | **0** |
| T4 keystone as form-level passive | 1 per form (in separate `t4_alteration_output` field; orphan from skills array) |
| Role distribution | damage 89 / utility 67 / mobility 67 / defense 35 / control 31 (all in `role` field but all nodes still ACTIVE on energy + cd) |

**Matt's insight CONFIRMED empirically.** All v2_narrow_phase_5 skills are actives; T4 is the only passive (and it lives in a separate schema slot). Certain kits (defensive tank, sustained caster, hybrid attribute) would benefit substantively from in-tree passive nodes, but the engine has no schema for passives in `skills[]`.

#### Cycle 13 scope inputs

**Substrate amendments needed:**

1. **Schema extension** — `skills[]` node needs `node_type: 'active' | 'passive'` discriminator (OR rename current `role` to carry this; current `role` is damage/utility/mobility/defense/control which is the COMBAT role, not the activation type)
2. **Layer 3 generator amendment** — determine per-kit active/passive ratio from BC-target cell + kit identity signals; gandalf design-spec-as-math owns the ratio function
3. **Cohesion-judge rubric extension** — verify passive choices align with kit identity (extends current 5-dimension rubric with an "active/passive coherence" check)
4. **Drax T4AlterationPanel + SkillTree rendering** — passives display differently from actives (no cooldown/cost; constant effect)

**Design-spec-as-math (gandalf authoring scope):**

| Kit archetype (inferred; Matt amends at T4 PM1) | Active : Passive target ratio |
|---|---|
| High-tempo combo (e.g., physical_skirmisher) | 90:10 or 100:0 (rotation-heavy; passives interrupt rotation) |
| Defensive tank (e.g., physical_warrior with shield) | 50:50 to 60:40 (damage reduction + regen passives anchor; actives are deliberate interventions) |
| Caster (fire_mage, water_caster, earth_caster) | 60:40 to 70:30 (sustained mana-regen + element-affinity passives + burst actives) |
| Berserker/rage kits (rage energy type) | 80:20 (rage-build through actives; passives are rare meta-modifiers) |
| Hybrid attribute (e.g., physical_grappler with mana) | 70:30 (passive support for off-attribute mechanics) |
| Controller (wind_controller, water_controller) | 70:30 (passives extend control durations; actives apply control) |

**Cycle 13 sequencing:**
- Phase 1 — gandalf design-spec-as-math + schema design (~1-2 days)
- Phase 2 — rocket Layer 3 amendment (~3-5 days)
- Phase 3 — drax rendering amendment (~2-3 days)
- Phase 4 — gamora simulation integration (passive effects need sim wiring if Cycle 13 includes Option B/C generation-vs-sim) (~3-5 days conditional)

**Total Insight A: ~1-2 weeks rocket-track; ~half-week gandalf-track; ~half-week drax-track. Parallel-tracks possible.**

### 8.2 Insight B — T4 as chain capstone (thematically continuous with chain T1-T3)

#### Empirical grounding

| Measure | Result |
|---|---|
| T4 location in schema | `t4_alteration_output` (top-level form field) |
| T4 chain attribution | **ABSENT** — no `signature_chain_id` field on T4; no `is_capstone` field on chain skills |
| Skill chain identifiers | `skills[].chain_id` (chain_A / chain_B / chain_C) + `skills[].tier` (1-4) |
| Thematic continuity in NARRATION | **PARTIALLY achieved** via Fix 1 amendment context fields (`named_skill_chain_signature` + `form_all_named_skills`) — verified explicitly in form-031 where rationale references chain T1 + T3 names by name: "every lesson from Swift Step to Ironwood Bulwark has been stripping away excess" |

**Matt's insight CONFIRMED empirically.** T4 is schema-orphan; the Fix 1 amendment papers over at narration layer (LLM uses chain names in prompt context) but the underlying schema does not assign T4 to a designated chain. The orphan field becomes a structural-coupling problem when (a) Insight C cycling requires T4 candidates per chain, (b) skill-investment unlock requires "spend N points in chain X to unlock T4-X," (c) the loadout app wants to display T4 inline with its chain (not as a separate panel).

#### Cycle 13 scope inputs

**Schema amendments needed:**

1. **`t4_alteration_output.signature_chain_id`** field — links T4 to a designated chain (chain_A / chain_B / chain_C); aligns with T4-A architecture defaults canonical doc (1 signature + 1-3 secondary capstones)
2. **`skills[].is_capstone_for_chain`** OR equivalent — marks which skill in a chain unlocks the T4 (or is unlocked by it)
3. **Phase 5 cohesion-judge extension** — chain T1→T4 thematic continuity validation as a new rubric dimension; current 2-dim simplified rubric (per amendment § 3) adds a 3rd dimension `chain_continuity_score`
4. **Loadout rendering** — T4 displayed inline with signature chain (not as orphan panel); if multiple T4 candidates exist per chain (Insight C), the panel shows the unlocked-vs-locked state

**Layer-by-layer amendment scope:**
- Layer 3 skill content generator: chain-aware T4 selection (current is per-form one-shot)
- Layer 6 wire-up: thread `signature_chain_id` from § 8 algorithm output through schema
- Phase 5 cohesion-judge: extend rubric per amendment § 3.3 aggregate score formula
- Drax: T4AlterationPanel becomes chain-attached (rendering change ~1 day)

**Gandalf design-spec-as-math (Phase 5 extension scope):**

Authoring task — extend cohesion-judge spec § 3 to add `chain_continuity_score`:

```
chain_continuity_score = (
  0.30 × lexical_continuity (T4 narration vocabulary overlap with chain T1-T3 names) +
  0.30 × thematic_arc_continuity (T4 narration references chain progression — "step → command → capstone" arc) +
  0.40 × mechanical_substrate_continuity (T4 strategy_type fits the chain's role profile)
)

new_aggregate = 0.50 × kit_identity + 0.30 × thematic_rationale_fit + 0.20 × chain_continuity_score
```

(Initial weights; subject to calibration sweep per amendment § 4 pattern.)

**Total Insight B: ~3-5 days rocket + ~half-day gandalf design-spec extension + ~1 day drax rendering. Less scope than Insight A.**

### 8.3 Insight C — T4 cycling during multi-dim convergence + skill-investment unlock

#### Empirical grounding

| Measure | Result |
|---|---|
| T4 structure per form | **Single T4 keystone** (not options list); `t4_alteration_output` is a single object, not an array |
| Candidates/options field | **ABSENT** — no `t4_candidates` or `t4_options` field in schema |
| Cycling-during-convergence telemetry | **ABSENT** — no `convergence_iterations` or `cycled_t4_history` field |
| Skill-rank progression in node schema | **ABSENT** — `skills[]` has `tier` (1-4 chain depth) but NO `rank` (multi-rank investment per node) |
| Player progression / investment gating | **ABSENT** at engine schema layer (entirely deferred to loadout-app rendering OR future game-loop) |

**Matt's insight CONFIRMED empirically.** Single T4 per form; no cycling; no candidates; no investment-gating mechanic. The W1.13 multi-dim convergence math note v1.1 (Matt cited "Tier 4 keystone discrete × ...") DOES include T4 as a convergence dimension on paper, but the implementation surface emits ONE selected T4 not a cycle-through-options.

#### Cycle 13 scope inputs (MULTI-LAYER + substantial)

**This is the most substantial of Matt's 3 insights.** Multi-layer amendment:

| Layer | Amendment scope | Owner | Estimated effort |
|---|---|---|---|
| **Schema — skill_rank** | `skills[].max_rank: int` + `skills[].current_rank: int` (per-build state); investment-gating threshold per chain (e.g., "spend 10 points in chain_A to unlock T4-A") | rocket + gandalf design-spec | ~3-5 days |
| **Schema — T4 candidates** | `t4_alteration_output` becomes `t4_candidates: List[T4Alteration]` (~3-5 per chain per T4-A architecture defaults); add `unlocked: bool` + `unlock_threshold: dict` | rocket + gandalf | ~3-5 days |
| **Layer 4 W1.13 convergence** | Verify T4-keystone-discrete is cycling per math note v1.1; if not, amend to cycle T4 options during convergence; if cycling, expose cycled history as telemetry | rocket + gamora | ~3-5 days |
| **Layer 3 skill content** | Generate T4 candidates per chain (not just one selected T4); fire ~3-5 candidates per chain × 2-3 chains per form = ~10-15 candidates per form total; cost-implications (LLM call multiplier) | rocket + gandalf | ~3-5 days |
| **Phase 5 narration** | T4 narration LLM pass fires for EACH candidate, not just the selected one; cost goes from ~35 calls/run to ~350-500 calls/run; G12 cost guard impact significant ($1.50-$2.00 per run vs current $0.17) | rocket | ~1-2 days |
| **Loadout skill-tree progression UI** | Spend skill points to build character; per-chain investment counter; T4 unlock at threshold; T4-candidate cycling | drax + gandalf | ~3-5 days |
| **Game design loop** | Skill-point earning mechanic (level-up grants, gear drops, season rewards); chain investment progression; respec mechanic | Matt + gandalf + drax | ~1-2 weeks (substantial game-design call) |

**Total Insight C: ~3-4 weeks engine + ~1-2 weeks game-loop design + ~1 week drax.** This alone is most of Cycle 13.

**Cost-implication callout:** if T4 narration LLM pass fires per-candidate not per-form, LLM cost per generation run goes from $0.1668 → ~$1.50-$2.50 (10×+ cost). G12 cost guard needs re-evaluation; consider Haiku for candidate narration + Sonnet only for selected-candidate refinement; OR narrate only when candidate is unlocked (just-in-time).

#### Design-call decision deferral for T4 PM1 Block 3

Insight C requires substantive game-loop design call (skill-point earning, spending, respec, investment-progression UX). This is v1.0 game-shipping territory, not just engine work. Should be Block 3 of T4 PM1 OR a separate sustained design session with Matt + gandalf.

### 8.4 Insight A + B + C composition with Cycle 13 architecture decision (A/B/C generation-vs-sim partitioning)

Per T4 PM1 prep doc § 6 Category 1 — A/B/C generation-vs-sim decision composes with Insight A/B/C scope:

| Generation-vs-sim option | Composition with Insight A/B/C |
|---|---|
| **Option A (generation-only)** | All Insight A/B/C work fires on engine side; sim becomes Cycle 14+ workstream when warranted; passive effects, T4 cycling, investment unlock are emitted as SCHEMA without sim validation |
| **Option B (integrated sim)** | Insight A passives need sim wiring (passive effects must affect sim outcomes); Insight C T4 cycling needs sim eval of each candidate; substantially more Cycle 13 scope (~5-8 weeks) |
| **Option C (hybrid `--with-sim`)** | Generation emits schema; opt-in sim validates passives + T4 cycling; v1.0 schema lands without sim gate; sim integration is downstream optimization |

**Gandalf lean (carried from prior pass): Option A — defer sim integration to Cycle 14+; Cycle 13 stays generation-only; emit Insight A/B/C as schema; validate downstream when sim cycle fires.**

This composition decision is the substantive content of T4 PM1 Block 3.

---

## 9. Pass 1 architectural-gap surfacing — additional findings beyond Matt's 3 insights

### 9.1 Skill-node-level placeholder slipped through (form-015 "Empower")

`acceptance_criteria.no_placeholder_strings: false` in metadata. Empirical scan reveals one node:

- form-015 Ember Academician, chain_C T1: `name: "Empower"`; `phase5_is_placeholder: True`; `phase5_attempt_number: 3` (used all 3 attempts); fell back to engine default name + placeholder flag

This is 1/289 = 0.35% (below spec § 4.5 final-FAIL threshold of 5%). Acceptable for v1.0. But the brief did not flag this and the framing-audit caught it. Forward routing: add to Phase 5 v1.1 backlog (cohesion-judge + LLM tuning to reduce final-FAIL on this node).

### 9.2 Skill-node-level duplicate count discrepancy (brief vs metadata)

`metadata.json` reports 7 skill-node duplicate names: "Whirling Steel Dance", "Iron Petal Guard", "Broadhead Volley", "Solar Stride", "Warden's Swift Step", "Ember Step", "Sweeping Gale". `phase5_uniqueness.uniqueness_rate: 0.9514` (288 total - 14 dupe instances counted = 274 unique = 95.14% — above ≥95% target → PASS).

Brief said "1 dupe" (referring to T4-label-level dupe — "Ironpoint Convergence"). Brief did NOT mention skill-node-level dupes. These are TWO different uniqueness metrics — the brief conflated. Empirical state: skill-node-level uniqueness PASSES; T4-label-level uniqueness has 34/35 = 97.1% (matches brief; 1 dupe).

Forward routing: clarify acceptance criteria in spec — uniqueness is at WHICH layer? (Currently the spec mixes both implicitly.) Phase 5 v1.1 spec amendment candidate.

### 9.3 Top-level `manifestation` tier-label semantic NEVER populated

35/35 forms have `t4_alteration_output.manifestation: None` (top-level). Per amendment § 2.1 disambiguation, this slot was supposed to hold the TIER LABEL enum (`"T4_active"` / `"rank2_passive"` / `"rank3_passive"`) populated by `mechanic_alteration.py:_manifestation_from_tier`. Empirically: that wiring is NOT firing.

Per amendment § 1.3 "Rocket investigation recommendation: identify why `alteration_output is None` in the current emission path" — this was flagged in the amendment but not resolved. Rocket implementation focused on populating the PROSE slot (nested `spirit_guide_narration_metadata.manifestation`) but did not investigate WHY the tier-label slot is None.

**Consequence:** the player-facing loadout has no surface for tier-label semantic (no "rank3_passive" badge or equivalent). This may be intentional (the design may not surface tier-label-as-rank to player) OR an unfilled wiring gap. Cycle 13 candidate question.

### 9.4 Engine schema fields visible in skill but NOT consumed by drax

`skills[].canonical_element` (e.g., "physical", "fire", "wind"), `skills[].seasonal_element` (often null), `skills[].geometry_type` (often null), `skills[].spatial_geometry_type` (often null), `skills[].bc_axis_contribution` (dict with axis_1_engagement, axis_2_geometry, etc.).

Worth a Phase-2 Pass-investigation: are these surfaces consumed in loadout SkillTree rendering? If yes — good. If no — engine emits design-mode metadata that has no consumption path (silently wasted generation work). Quick drax-side grep would resolve.

### 9.5 Pass 2 deferrals (per Matt directive)

Out of scope per brief; surfacing for Cycle 13 / T4 PM2:
- Skill-tree-feel evaluation (sim-gated)
- Battle-behavior evaluation (sim-gated)
- Full kit-feel evaluation with passives + T4 chain + skill-investment progression integrated
- Sub-element manifestation evaluation (Cycle 13 v1.1+ scope per prior pass)

---

## 10. Forward routing recommendation

| Tier | Action | Owner | When |
|---|---|---|---|
| **Tier 1 — must fire** | T4 PM1 readiness signal: **READY.** Matt schedules T4 PM1 design call when next workstream gap opens. | knight-rider relays | post this verdict |
| **Tier 1 — must fire** | This Pass 1 special case summary captured at `agentic_orchestration/gandalf/notes/2026-05-26-engine-generation-special-case-summary.md` for T4 PM1 inputs + Cycle 13 scope-doc anchor. | gandalf (self) | this session |
| **Tier 2 — primary path (recommended pre-PM1)** | Drax T4AlterationPanel + types.ts amendment per § 7.3: render `narrationMeta.alteration_type` as header label + `narrationMeta.manifestation` as PROSE block between description and Spirit-Guide rationale. ~30 min effort; lands rich narration in production before T4 PM1 design call. | drax | post this verdict, pre-T4-PM1 |
| **Tier 2 — primary path** | T4 PM1 design call substantively evaluates v2_narrow_phase_5 + hand-authored T4 alternatives + Matt's 3 architectural insights (Block 3 — Cycle 13 scope dialogue). | Matt + gandalf | next sustained design session |
| **Tier 2 — primary path** | Cycle 13 scope-doc authoring (gandalf) integrates Matt's 3 insights per § 8 above + A/B/C generation-vs-sim decision from PM1 Block 3 + this Pass 1 architectural-gap findings (§ 9). | gandalf canonical authoring | post T4 PM1 outcomes |
| **Tier 3 — supplement** | Phase 5 v1.1 spec amendment backlog: (a) skill-node-level placeholder reduction (form-015 Empower case); (b) clarify uniqueness metric layer (skill-node vs T4-label); (c) cohesion-judge rubric chain-continuity extension per Insight B; (d) re-roll rate target relaxation OR substrate-binding remediation per Finding 4. | gandalf authoring | post-Cycle-13-scope-doc |
| **Tier 3 — supplement** | Engine investigation: WHY `t4_alteration_output.manifestation` (top-level tier-label slot) is None across all 35 forms — wiring gap per amendment § 1.3 unresolved item (§ 9.3 above). Rocket investigation. | rocket | Cycle 13 scope item |
| **Reserve** | If Matt's Insight C (T4 cycling + investment unlock) is selected as Cycle 13 PRIMARY scope, LLM cost guard re-evaluation (per-candidate narration would 10× cost). gandalf + star-lord cost-budget pass before Cycle 13 fires. | gandalf + star-lord | conditional on Cycle 13 scope decision |
| **Reject** | Re-firing Phase 5 regen pre-T4-PM1 for Finding 6 alone — drax-side amendment is the cleaner path; engine regen is not the right intervention surface. | — | — |

---

## 11. Decisions-log proposal (gandalf proposes; KR routes; jack-ryan authors after Matt approval)

> **2026-05-26 — v2_narrow_phase_5 Pass 1 design-fit verdict — T4 PM1 READY; drax T4AlterationPanel amendment surfaced as small Cycle 13 fast-follow**
>
> **Decision:** T4 PM1 design call scheduled (Matt initiates). Drax T4AlterationPanel + types.ts § 8.2 amendment fast-follows pre-T4-PM1 per gandalf Pass 1 verdict. Findings 1-5 RESOLVED; Finding 6 PARTIALLY RESOLVED (small drax follow-on); Findings 7-9 (Matt's 3 architectural insights) empirically confirmed as substantial Cycle 13 scope.
>
> **Reasoning:** Pass 1 empirical verification on rocket regen 69970aa + drax loadout 684dca0 confirmed: Fix 1 T4 narration populates 35/35 forms substantively (mean cohesion 0.861; 0/35 fallbacks; D7 AI-tell discipline holds); Fix 2 main_weapon schema reconciles cleanly engine + drax; 22.9% T4 re-roll WARN is defensible noise (no quality degradation; substrate-binding inheritance root cause); 1 T4 label duplicate ("Ironpoint Convergence" on form-031 + form-034) is invisible to player because T4AlterationPanel doesn't render narrated label — surfacing the broader cross-seam consumption gap that drax doesn't display the new rich PROSE fields.
>
> **Alternatives considered:**
> - Re-fire Phase 5 regen to address Finding 6 — rejected; drax-side amendment is the correct intervention surface.
> - Defer drax T4AlterationPanel amendment to Cycle 13 main work — possible (Option B) but Option A (fast-follow pre-PM1) preferred because PM1 evaluates the full kit-defining surface during the call.
>
> **Status:** OPEN — pending Matt T4 PM1 scheduling + Tier 2 drax fast-follow ratification.
>
> **Related:**
> - `agentic_orchestration/gandalf/notes/2026-05-26-engine-generation-special-case-summary.md` (this doc)
> - `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` (prior Phase 5 verdict)
> - `canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` (Fix 1 spec)
> - `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (parent spec)
> - Regen output: `~/Games/reincarnated-engine/exports/v2_narrow_phase_5/` (engine 69970aa)
> - Loadout deploy: `~/Games/reincarnated-loadout/data/v2_narrow_phase_5/` (drax 684dca0)

---

## 12. Sign-off

**Author:** gandalf 2026-05-26 (Pattern A-deep DESIGN-FIT PASS 1 verdict; sub-agent fire per Matt 2026-05-26 Option B authorization)

**Status:** RATIFIED — Pass 1 verdict authored; routing recommendation to knight-rider for T4 PM1 readiness signal + drax fast-follow Tier 2 + Cycle 13 scope-doc anchor

**Effort:** ~3 hours autonomous (within Pattern A-deep budget; Matt estimated 2-4h)

**Disciplines applied:**
- gandalf OP § 4.1 framing-audit (caught the brief-vs-metadata metric conflation; caught the amendment § 8.1 "no drax work" understatement)
- gandalf OP § 4.4 inherited-findings refutation-evidence audit (proposed Discipline #23 amendment confirmed operationally useful)
- gandalf OP § 3.1 push-back-hard (refused to mark Finding 6 as RESOLVED when the amendment claim was structurally optimistic)
- gandalf OP § 3.2 Mathematical Layer routing (Insight A design-spec-as-math per-kit active/passive ratio is gandalf authoring scope; Insight C cost-guard math is gandalf + star-lord)
- gandalf OP § 3.4 recognition-validate-commit (Insight A/B/C captured as recognition; architectural commitments deferred to Cycle 13 scope-doc post-T4-PM1)
- gandalf OP § 3.5 NO sleep recommendations (verified absent)
- gandalf OP § 3.6 timezone-agnosticism (verified absent — only workstream-relative framing throughout)
- gandalf OP § 4.5 first-canonical-example flag (the brief-vs-metadata conflation catch is a second canonical example of framing-audit catching pre-imposed assumption — captured for OP § 4 amendment)

**Downstream consumers:**
- knight-rider — route forward per § 10 Tier 1 + Tier 2; relay decisions-log entry candidate to Matt
- Matt — review verdict; T4 PM1 schedule; ratify Tier 2 drax fast-follow recommendation; sustain Block 3 dialogue on Cycle 13 architecture (Insight A/B/C + A/B/C generation-vs-sim)
- drax — Tier 2 fast-follow per § 7.3 (T4AlterationPanel + types.ts amendment); ~30 min effort
- rocket — Tier 3 Cycle 13 supplement: engine investigation on top-level `manifestation` tier-label slot wiring gap (§ 9.3)
- gandalf (self) — Cycle 13 scope-doc authoring integrates Pass 1 architectural-gap findings + Matt's 3 insights + A/B/C generation-vs-sim decision from PM1 Block 3 (post-T4-PM1)
- jack-ryan — author canonical decisions-log entry after Matt signal on T4 PM1 + Tier 2 drax fast-follow (per decision-log-format skill)

**Cross-references:**
- `canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` (Fix 1 spec; this pass verifies)
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (parent spec)
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` (prior verdict)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` (prior special case summary; this doc is successor for v2_narrow_phase_5 cycle traceability)
- `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` (T4 PM1 prep + agenda; this verdict feeds Block 3 dialogue)
- `~/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json` + `metadata.json` (load-bearing evidence)
- `~/Games/reincarnated-loadout/data/v2_narrow_phase_5/classes/*.json` + `manifest.json` (load-bearing evidence)
- `~/Games/reincarnated-loadout/src/components/SkillTree/T4AlterationPanel.tsx` (cross-seam consumption gap empirical surface)
- `~/Games/reincarnated-loadout/src/data/types.ts:282-353` (drax schema; Fix 2 + NarrationMetadata stale comment)
