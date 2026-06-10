# Phase 5 Amendment Close — Design-Side Review

**Date:** 2026-06-10
**Author:** gandalf
**Mode:** Pattern A-deep (design-review verdict)
**Subject:** drax /forge Phase 5 amendment close report design-side critique
**Composed with:** jack-ryan Gate-2 (concurrent process-side review)
**Authority chain:** § 12 canonical lock (commit `861403d`, gandalf-authored) → Matt 2026-06-10 sequenced directive → Phase 5 GREEN (drax verdict commit `31fb76e`)

---

## Top-line verdict

**PASS-WITH-DESIGN-RECOMMENDATIONS.**

§ 12 architectural pattern is validated at the player surface at the level of architectural fidelity I can assess from code + close report (preview URL is auth-walled, expected). The implementation honors the four load-bearing recognitions captured in § 12.1 — two-layer primitive split, input-vs-output, spirit-guide-driven precedent elicitation, cycling != committing — and the iPad-text / sky-runes split per § 12.2 is faithfully realized. The 29 placeholder icons are RETIRED at the player surface (TierTwoPanel suppressed in `cascadeMode`); they have not drifted into replacement-icon scope. D7 AI-tell line is preserved end-to-end at the templated voice surface. Discipline #40 scaffold flags are in place on Tier 2/3 vocabulary and spatial layout.

Design-side recommendations are concentrated on three surfaces — none of which RETURN the work to drax for amendment:

1. **Cluster spatial layout** — drax surfaced the 1:1 sky/rune-group correspondence honestly as a tradeoff; this should NOT carry into Pattern B unmodified. Recommendation: Pattern B explicitly addresses spatial-layout-as-independent-of-rune-group-positions.
2. **Cascade text vocabulary (Tier 2/3 questions)** — most draft phrasings are usable starting points; 3 of 7 Tier 2 + 2 of 5 Tier 3 have specific landings I'd want to revisit at Pattern B (detail below).
3. **Spirit guide voice templates** — D28-D32 neutral-data-oracle pattern is structurally honored but slightly drifts toward romantic-mystical at three commit-response moments. Pattern B should harden voice toward Diablo-IV-Lilith-Council neutral-observation register, not Genshin-spirit-companion register.

**No recognitions surfaced that § 12 didn't anticipate.** § 12.13 deferred-refinement list matches the open items drax surfaces in the close report. The architecture survives empirical contact at the player surface.

---

## 1. § 12.2 cognitive-load split fidelity

**Finding: PASS.** The implementation honors iPad text + sky rune split with no drift.

- `Forge.tsx` lines 485-516: cascade view path renders `RuneLayerCanvas` with `cascadeMode={true}` + `CascadePanel` overlay. The Tier 2 placeholder-icon TierTwoPanel is rendered ONLY when `cascadeMode={false}` (`RuneLayerCanvas.tsx:1364`). Default view (`viewMode === 'cascade'`) is the canonical surface.
- The 29 placeholder icons are not just suppressed — they are not loaded into the cascade-view DOM at all. Per-primitive iconography is RETIRED at the scope § 12.10 requires.
- `?view=rune` Phase 4 baseline is preserved as fallback (CascadePanel absent; TierTwoPanel present). This is the right disposition: Phase 4 work is preserved as a referenceable predecessor, not deleted; § 12 does not require Phase 4 retirement.
- iPad text typography in `CascadePanel.tsx` uses `font-mono` + `font-semibold` consistent with existing loadout app HD-2D pixel-typography register per `canonical/story/style-register.md` Candidate B lock. No raster-anime drift; no flat-vector drift.

**Design-side observation, not blocking:** the violet-700/Tailwind-class register (`text-violet-200`, `bg-violet-950`, etc.) is the loadout app's existing dev-typography register. This is fine for Phase 5 prototype. At WS2 UE-port + at production-skin Pattern B, the spirit-guide voice color register should be reviewed against the canonical style-register HD-2D pixel-art palette — violet-as-spirit is a defensible choice (associates with mystical-feminine-voice in fantasy register), but it should be a canonical choice, not a Tailwind-default-inherited choice. Flag for Pattern B style-register subsidiary review.

---

## 2. § 12.3 + § 12.4 cascade vocabulary

**Finding: PASS-WITH-SPECIFIC-RECOMMENDATIONS.**

### 2.1 Tier 1 anchor labels — CANONICAL per § 12.3; verified verbatim

All 7 labels in `cascadeData.ts:77-155` match § 12.3 CANONICAL LIST verbatim: Race/ancestry, Element/flow, Weapon/craft, Power/mastery, Style/way, Harvest/rewards, Horizon/goal. Per drax close report § 1 acceptance #3 PASS. No drax-discretion drift.

### 2.2 Opening question — CANONICAL per § 12.3; verified verbatim

`SPIRIT_GUIDE_VOICE.tier1_opening` in `cascadeData.ts:198` carries the exact § 12.3 canonical text: *"What is most important for your journey this season?"* No drift.

### 2.3 Tier 2 follow-up questions (drax discretion within § 12.13 deferral)

7 Tier 2 questions reviewed against neutral-data-oracle voice (canonical 40 D28-D32) + spirit-guide-as-interpreter-of-the-Throne register (canonical 17). Per-question disposition:

| Tier 1 anchor | Draft question | gandalf disposition | Reason |
|---|---|---|---|
| Race/ancestry | "Which tradition calls to you?" | **REVISIT at Pattern B** | "Tradition" reads as generic-fantasy; "calls to you" is acceptable but trends romantic. § 12.6 names this anchor "Race / ancestry" as a Layer 0 INPUT primitive; D29-D31 says oracle voice is "projection / pattern / typical." Better Pattern B candidate: *"Which lineage shapes your form?"* (echoes § 12.5 example "Which tradition calls?" — preserve verb "calls" if Pattern B locks it; "lineage" lands closer to ancestry register than "tradition"). |
| Element/flow | "Which current runs through your form?" | **ACCEPT as draft starting point** | "Current" works — the element-AS-flow framing was a § 12.3 author choice; "runs through your form" composes with the elemental-as-substance reading. Slight romantic lean but tolerable. |
| Weapon/craft | "What form does your craft take?" | **ACCEPT as draft starting point** | The double meaning of "craft" (weapon-craft + skill-craft) is good. The question shape ("What form does X take") is neutral-observation appropriate. |
| Power/mastery | "What expression of power calls to you?" | **REVISIT at Pattern B** | "Expression" is fine but slightly abstract; "calls to you" repeats the Race question's verb without intentional rhyme. Better Pattern B: *"What shape does your power take?"* (echo Weapon's "What form X take" structure across anchors — consistent grammatical register, oracle-pattern-recognition voice). |
| Style/way | "How do you move through your fights?" | **REVISIT at Pattern B** | "Fights" is genre-correct (ARPG) but slightly too literal for spirit-guide register. The drax close report flags "encounters" as alternative — agreed. Better Pattern B: *"How do you move through encounters?"* OR *"What is the shape of your engagement?"* (the latter lands closer to identity-axis Layer 2 framing per § 12.6). |
| Harvest/rewards | "What do you seek to gather?" | **ACCEPT** | Clean; "gather" is neutral; matches loot-focus precedent semantic per § 12.3 cosmograph response. |
| Horizon/goal | "Where does your horizon lie this season?" | **REVISIT at Pattern B** | The literal echo of the anchor label ("horizon" → "horizon") is acceptable but flat. Better Pattern B: *"How far does your path reach this season?"* OR *"What stage do you build toward?"* (closer to progression-stage Layer 2 framing per § 12.6). The "this season" qualifier is good — preserves the seasonal-arc framing from `project_earth_meta_layer` + § 12.3 opening. |

### 2.4 Tier 3 follow-up questions

5 Tier 3 questions reviewed:

| Tier 2 option | Draft question | gandalf disposition | Reason |
|---|---|---|---|
| Fire | "Does the fire erupt or flow?" | **ACCEPT — STRONG** | Binary that captures burst-vs-sustained cleanly; "erupt or flow" is etymologically and operationally honest; oracle-pattern-voice appropriate. This is the strongest Tier 3 question in the draft set. |
| Water | "Does the water control or drown?" | **REVISIT at Pattern B** | "Drown" is harsh — drax flagged this in close report; agreed. The harshness drifts toward menacing-register, which is wrong for spirit-guide-as-Throne-resident-data-oracle. Better Pattern B: *"Does the water hold or sweep?"* (hold = control-AOE; sweep = sustained-flow). |
| Lightning | "Does the lightning strike once or cascade?" | **REVISIT at Pattern B — meta-collision** | drax surfaced the meta-issue (player is "cascading" through the cascade, and option talks about "cascade") — agreed. The meta-collision is a real cognitive dissonance. Better Pattern B: *"Does the lightning strike once or arc?"* (single-target vs chain). |
| Dwarven | "What does the forge produce?" | **ACCEPT — STRONG** | Lineage-evocative; the question shape (output-question to choose between weapon/ward) honors the dwarven-as-craft semantics. Composes with weapon-craft Tier 1 anchor coherently. |
| Burst | "Does the burst land once or again and again?" | **REVISIT at Pattern B** | Verbose; the "again and again" reads as conversational-spirit, not data-oracle. Better Pattern B: *"Does the burst peak once or stack?"* (peak = single big spike; stack = repeated bursts). |

### 2.5 Substrate-truth-wins discipline at vocabulary

§ 12.7 specifies pre-display coverage filter (Hotspot D). Phase 5 prototype does NOT filter — Tier 2/3 options show unconditionally. drax surfaces this as Discipline #18.2 hotspot, deferred per close report § 4. Disposition: **ACCEPT deferral.** § 12.13 names this as open refinement; vocabulary discussion at Pattern B should compose with coverage filter scope (e.g., "if 'Dwarven' has zero kits in current substrate, the option simply does not display — this means the Race Tier 2 vocabulary should be designed to gracefully handle absence of options, not to depend on full presence").

**Drax discretion verdict for cascade vocabulary:** drax exercised discretion within § 12.13 deferral bounds. The draft set is usable. Pattern B should revisit specifically the 6 items flagged REVISIT above (4 Tier 2 + 3 Tier 3 minor edits, none of them re-architectural).

---

## 3. § 12.4 cycling-preview mechanic

**Finding: PASS — architectural pattern faithfully implemented.**

### 3.1 Cycling != committing — VERIFIED

- `CascadePanel.tsx` highlight is mediated through `setHighlightedIndex` (no state mutation beyond the highlight); commit is a separate explicit `commitHighlighted()` call gated on `committed === false`.
- Spirit guide narration is silent during cycling: `emitHighlight()` calls `setShowNarration(false)` on every highlight change (line 429). Narration appears only after `commitHighlighted()` calls `setShowNarration(true)` (lines 499, 527, 539, 562). This is § 12.4 CANONICAL property "Spirit guide silent during cycling" implemented correctly.
- Player can browse all options before committing — keyboard arrow nav (lines 373-394), touch swipe (lines 401-417), arrow-button taps (ArrowNav component), and pointer-enter highlight (line 148) all produce highlight-only state changes.

### 3.2 ~0.3-0.5 sec smooth transitions

`CYCLING_TRANSITION_DURATION_MS=400` is the named constant per Gate-1 D42 amendment, landing in the middle of the § 12.4 CANONICAL `~0.3-0.5 sec` range. Disposition: **ACCEPT.**

**Observation:** drax close report § 6 honestly surfaces that Pixi sky-overlay redraw is instantaneous (synchronous Graphics redraw), only the CSS option-list transition is 400ms. This is a Phase 5.5 tuning item drax has correctly named in TODO #13 (Pixi ticker alpha interpolation). Disposition: **PHASE 5 acceptable; Pattern B / WS2 vertical-slice should NOT ship with instant sky transition.** Cycling-as-discovery requires the player's attention to FOLLOW the sky's response, not to be jolted to it. Phase 5.5 ticker-based interpolation is mandatory for production feel. Confirmed alignment with drax's own recommendation.

### 3.3 7 sky cluster regions spatially distinguishable

The 7 region centers in `cascadeData.ts:77-155` span a distributed arc per § 12.3. Region radii 1600-2000px on an 11000×8500px world produce non-overlapping centers but partial atmospheric overlap. From the dim-all + radial punch-out implementation (`RuneLayerCanvas.tsx:1208-1237`), regions ARE visually distinguishable at default zoom.

**Design-side observation that joins drax's tradeoff list:** the 7-region center placement at world coordinates (0.17, 0.50, 0.83) × (0.25, 0.50, 0.75) makes the cosmograph read as a 3×3 grid with one cell empty. This is structural — the brain interprets near-orthogonal placement as a grid. § 12.3 says "celestial sphere" + § 12.4 "camera fly-through navigates between regions" — celestial-sphere reading is poorly served by a 3×3 grid. Recommended Pattern B layout: heptagram or 7-pointed-circular-arc, NOT 3×3 grid. drax close report § 3.1 already flags this; my disposition extends drax's observation with the specific structural reading.

---

## 4. § 12.5 nested cascade

**Finding: PASS for 3-layer functional cascade.**

- Tier 1 → Tier 2 → Tier 3 → emergence path is functional per close report § 1 acceptance #7 PASS.
- Phase transitions use `setTimeout(..., CYCLING_TRANSITION_DURATION_MS * 2)` (800ms) for narration-then-advance. This is the right pacing — narration lands, player reads, next layer appears. Faster would be jarring; slower would lose attention.
- Step-back logic (`handleStepBack`, lines 576-591) correctly truncates `committedSteps` and resets phase. § 12.7 "Refine = step back in cascade" is implemented.
- `handleRefine` (lines 593-611) drops player back to Tier 2 from emergence with refine-prompt narration. This matches § 12.7 substrate-truth-wins / refine behavior.

**Design-side observation, not blocking:** only 5 of the possible Tier 2 → Tier 3 paths have Tier 3 layers defined (fire, water, lightning, dwarven, burst). The other 17 Tier 2 options proceed directly to emergence (2-layer paths). This is acceptable Phase-5 scaffold scope per drax close report § 1 acceptance #7 — `Minimum 3-layer paths available` is the criterion, not all-paths-3-layer. § 12.5 says "cascade continues 3-5 layers deep" without mandating per-Tier-2-option uniformity. Disposition: **ACCEPT.** Pattern B canonical vocabulary lock should establish whether all Tier 2 options must have Tier 3 follow-ups, or whether some genuinely terminate at depth-2 (the latter is structurally honest — earth/wind/holy/shadow/physical for Elements presumably don't need a tertiary distinction the way fire/water/lightning do, because fire's burst-vs-sustained is genuinely a player-experiential branch).

### 4.1 Final emergence narration

`EmergenceView` component (`CascadePanel.tsx:266-346`) displays:
- Spirit guide narration (templated emergence text)
- Kit identity (name + output primitives) labeled "synthesized — not engine output"
- Path breadcrumb (committed steps)
- Refine + Reset controls

The "synthesized — not engine output" label is the right honesty discipline; it matches the drax role definition synthesized-visualization-labeling pattern. Disposition: **PASS.** Pattern B + WS2 vertical-slice scope absorbs the real nearest-kit-centroid lookup; this is correctly deferred via TODO(drax) #11.

---

## 5. § 12.9 spirit guide voice + D7 AI-tell line

**Finding: PASS-WITH-VOICE-CHARACTER-RECOMMENDATIONS.**

### 5.1 D7 AI-tell line preservation — VERIFIED

All voice templates in `SPIRIT_GUIDE_VOICE` are explicit templated functions (`cascadeData.ts:196-218`). No raw LLM dialogue generation; all narration is fully template-driven with narrow blanks (anchor label, question text, kit name, precedent, commits, output primitive). D7 is preserved end-to-end at the Phase 5 surface.

### 5.2 D28-D32 neutral-data-oracle voice alignment

Canonical 40 § 5 D28-D32 establishes:
- D28: data-oracle voice (additive to existing character canon)
- D29: universal-pattern principle
- D30: throne-resident framing composes with Heroic Spirit canon; oracle reads patterns
- D31: projection language honesty ("projected to / typically / estimated")
- D32: simulation-accuracy maintenance flagged ongoing

Per-template review:

| Template | Voice register | Disposition |
|---|---|---|
| `tier1_opening` | "What is most important for your journey this season?" | **PASS** — opening question; "journey" + "this season" is appropriate elder/seasonal framing; question shape is oracle-neutral. |
| `tier1_commit` | "You are drawn to [anchor]. [Tier 2 question]." | **REVISIT at Pattern B** — "You are drawn to" is slightly romantic; D31 projection-language honesty would land as "Your path projects toward [anchor]." or "Your form aligns with [anchor]." Pattern: oracle reports patterns ("projects toward"); doesn't editorialize about feelings ("drawn to"). |
| `tier2_commit` | "[Tier 2 label] takes shape. [Tier 3 question]." | **PASS** — "takes shape" is neutral-observation; pattern-recognition voice; appropriate. |
| `final_emergence` | "Your form emerges as [kit name]. Within [precedent], your path — [commits] — projects most closely toward this form. Accept, or refine?" | **PASS — STRONG** | The "projects most closely toward" phrasing is verbatim canonical-40 D31 honesty language. The "Accept, or refine?" pattern preserves player agency. This is the strongest template in the set. |
| `substrate_gap` | "Your spirit's path projects no exact match in this season's pattern. Nearest available form: [matched kit] — your [precedent] is preserved, your direction emerges as [output primitive]. Accept or refine?" | **PASS — STRONG** | Substrate-truth-wins discipline at the voice layer; "projects no exact match" is honest; "preserved" + "emerges as" is the right composition of honored-commitment + emergent-output. |
| `refine_prompt` | "Your path remains open. Which thread do you wish to revisit?" | **PASS** | Neutral; agency-preserving. |

**Voice character summary:** 5 of 7 templates land in D28-D32 register cleanly. The `tier1_commit` "You are drawn to" is the single specific item I'd want Pattern B to revisit toward "Your path projects toward" register. This is a one-template edit, not a re-design.

### 5.3 Voice-character risk surface for Pattern B

Pattern B should harden voice character with explicit reference to canonical examples:
- **Diablo IV Lilith dialogue** — sister/elder/intermediary-of-power voice; not romantic; not chummy
- **Mushoku Tensei Roxy / Sylphiette** — companion register at instructional/recognition moments; the spirit-guide voice should sit between Lilith (too cold) and Roxy (too warm)
- **NOT** Genshin Impact Paimon (too playful), Persona 5 Igor (too cryptic), or Final Fantasy Auracite voice (too declarative)

Recommended Pattern B reference for voice character: **The voice the spirit guide uses is the voice your most experienced friend uses when explaining a system they understand and you don't — they describe what they see, they project from pattern, they preserve your agency to decide.** This is what D31 projection-language honesty operationalizes.

---

## 6. Cluster spatial layout (§ 12.13 deferred — drax discretion)

**Finding: PASS-WITH-RECOMMENDATION-FOR-PATTERN-B-REPLACEMENT.**

drax close report § 3 surfaces three tradeoffs honestly:

1. **7 sky regions exactly overlay the 6 rune-group positions** (5 of 7 align to rune anchor coordinates). drax names this as "coherent spatial logic" upside / "reinforces 6-group scaffolding rather than 7-anchor canonical structure" downside.
2. **Region radii (1600-2000px) are smaller than rune atmospheric radius (1800px).** Visual boundary between regions ambiguous at default zoom.
3. **"Style/way" at center creates dominant visual center** that could mislead players into treating it as default. § 12 specifies no hierarchy in Tier 1.

**Disposition: drax's tradeoff observations are honest and load-bearing.** The 1:1 sky/rune-group correspondence is the most consequential. § 12.10 explicitly RETIRES per-primitive-group iconography at the player-facing scope; reinforcing the 6-group scaffolding via spatial overlay creates a soft re-entry of the retired architecture through positional mirroring. The 7-anchor canonical structure should stand spatially independent.

**Substrate-led discipline #41 check:** is the cluster spatial layout substrate-driven or designer-imposed? Currently it is **designer-imposed** (drax placed regions to mirror existing rune-group positions). Per § 12.3, the 7 anchors correspond to substrate-defined cluster regions; cluster centroids in BC space should DRIVE the spatial layout, not the existing rune-group grid. Phase 5 prototype's designer-imposed-overlay is acceptable AS PROTOTYPE because the rune-anchor positional cosmos pre-existed and a hard substrate-driven recompute was out of Phase 5 scope. But Pattern B + Hotspot A elrond consultation should land substrate-driven sky-region positioning (cluster centroids in BC space projected to celestial-sphere coordinates).

**Recommendation for Pattern B spatial-layout session:**
1. Layout is INDEPENDENT of rune-group positions (not 1:1 overlay)
2. Heptagonal or 7-pointed-arc arrangement (NOT 3×3 grid)
3. Substrate-driven — cluster centroids in BC space drive sky-region centers per substrate-led discipline #41
4. Spatial relationships between anchors should suggest cosmological relationships (e.g., Race/ancestry + Element/flow as adjacent because both are Layer 0 INPUT precedents per § 12.6; Style/way isolated as Layer 2 experiential axis)

Discipline #41 check returns **PASS for Phase 5 prototype (with explicit drax-acknowledged scaffold flag); MUST be addressed substrate-led at Pattern B + Hotspot A**.

---

## 7. Sign-overloading semantic (§ 11.2 Tal Rasha § 4.2 + § 11.4)

**Finding: PRESERVED at architectural intent; specific copy not yet at canonical scope.**

§ 11.4 establishes "Sign" as overloaded across 4 readings: noun-celestial (sign-in-the-sky), verb-input (signing/tracing a glyph), signature (signing one's commitment), The Sign (mystical-portent).

Phase 5 cascade implementation:
- **Noun-celestial reading** preserved — rune anchors persist in sky in `?view=cascade` per § 12.2 (the sky carries runes; cascade overlay illuminates regions); RuneLayerCanvas renders rune anchors identically per close report § 7.
- **Verb-input reading** partially preserved — cascade tap/cycle is a different input model than Phase 4's sign-by-gesture-draw. Cascade's cycling is closer to "browse" than to "sign." § 11.4 anchors the verb-input reading specifically at Tier 1 gesture-draw Option β.
- **Signature reading** preserved — the Commit affordance at every cascade layer is a "signing" of the player's commitment per § 12.7 "Player commits via tap; cosmograph LOCKS focus on chosen region." The commit-bar button text reads "Begin this path" at Tier 1 and "Commit" at later tiers — this is signature-reading appropriate.
- **The Sign mystical-portent reading** preserved at the visual register — rune-in-sky atmospheric drawing + dim-all + radial-glow at commit produces the mythic register § 11.4 requires.

**Verdict: semantic NOT collapsed to one register.** All 4 readings remain accessible at Phase 5 scope. The cycling-cascade does shift the verb-input reading away from gesture-draw, but Phase 4 baseline at `?view=rune` preserves gesture-draw as the canonical sign-as-verb implementation.

**Pattern B consideration:** the canonical Tier 1 input model decision (Option α tap-only / Option β gesture-draw-only / Option γ both with toggle per § 11.4 close paragraph) interacts with Phase 5 cascade architecture. Cascade is structurally Option α at Tier 1 + Option α at Tier 2 + Option α at Tier 3 (text-list cycling tap). gesture-draw at Tier 1 is preserved in Phase 4 baseline but NOT integrated into cascade. Pattern B Tier 1 input-model lock should clarify whether cascade is "tap-only path" with gesture-draw as parallel alternative path, or whether cascade should support gesture-draw cycling (gesture-as-cycling-step). § 12.8 says Path L (Lasso) + Path I (Drop ingredients) compose at the architectural level on the same nearest-kit-centroid backend — the same composition principle should apply to cascade tap-cycling vs gesture-sign at Tier 1.

---

## 8. Recognition record check

**Finding: NO architectural recognitions surfaced that § 12 didn't anticipate.**

Phase 5 GREEN empirically validates § 12.1-§ 12.13 at the player surface. The deferred-refinement items in § 12.13 match the open items in drax close report § 10 (TODO #9-13). The methodology hotspots (Hotspot D pre-display coverage filter per § 12.7) are correctly identified.

**One observation worth capturing as Pattern B input (not § 12 amendment):** the meta-collision in "Does the lightning strike once or **cascade**?" while the player is in the cascade is a genuine cognitive-dissonance pattern that surfaced through implementation. § 12 didn't anticipate this specific collision because § 12 chose "cascade" as the UX vocabulary at the architectural level. The choice should be revisited at Pattern B vocabulary scope — either Tier 3 Lightning question replaces "cascade" with "arc/chain" (the easy fix; recommended above), OR the architectural-level vocabulary considers whether "cascade" remains the right UX word for the cycling-elicitation pattern (much larger scope; probably not worth re-opening). Disposition: easy fix is good enough; not architectural.

**No new canonical addendum required.** Pattern B follow-on can land the vocabulary + spatial-layout refinements without amending § 12.

---

## Discipline cross-check

### Discipline #40 — scaffold-with-pending-decision

**Status: PASS.**
- Tier 2/3 question strings carry inline `<!-- SCAFFOLD: pending Pattern B canonical ratification per § 12.13 -->` comments at every layer per close report § 2 Amendment 1
- File-level block comment at `cascadeData.ts` top names the scaffold scope
- TODO(drax) items 9-13 in close report § 10 align with § 12.13 deferred items:
  - #9 spatial layout ↔ § 12.13 "Cosmograph spatial layout specifics"
  - #10 Tier 2/3 vocabulary ↔ § 12.13 "Specific text vocabulary per Tier 2 / Tier 3 cascade questions"
  - #11 synthesized kit emergence ↔ § 12.14 deferred "vertical-slice spike scope"
  - #12 pre-display coverage filter ↔ § 12.7 + Hotspot D
  - #13 sky overlay animation ↔ § 12.13 "Cycling animation timing tuning"

All 5 active overrides are scoped to § 12.13 deferred items. No drax discretion exceeded.

### Discipline #41 — substrate-led

**Status: PASS-with-Pattern-B-elevation-required.** Phase 5 prototype spatial layout is designer-imposed (drax mirrored 6-group rune layout); Pattern B + Hotspot A must elevate to substrate-driven (cluster centroids in BC space drive sky-region centers). drax's tradeoff surface honestly flags this; the Phase 5 disposition is acceptable AS PROTOTYPE. Production layout must be substrate-led per § 6 above.

### Discipline #25 — semantic-layer rep-audit

**Status: PASS at Phase 5 scope.** The 7 anchor labels CANONICAL per § 12.3 are intentionally semantically open ("Race / ancestry" can be Race-as-cultural-tradition OR Race-as-genetic-lineage; the cascade Tier 2 narrows). At Phase 5 scaffold scope, no semantic-layer drift; cluster identity → cluster label mapping is provisional everywhere it can drift, with explicit drax-discretion flagging. Pattern B should compose with the semantic-layer rep-audit discipline (gandalf OP § 4.4 candidate Discipline #18 amendment) when cluster naming is locked — substrate clustering at the BC layer is binding; semantic interpretation of "the Race cluster" requires rep-audit.

### Discipline #42 — framing-audit at consumption

**Status: PASS.** drax executed within dispatch scope. The Phase 5 amendment dispatch authorized: (a) 29 placeholder icons removed, (b) 7 Tier 1 anchor cycling UI, (c) cosmograph response animation, (d) nested cascade. drax delivered exactly this scope. No scope-amendment-without-Matt-authorization; no scope-creep; no scope-shrink.

drax surfaced 5 TODO(drax) overrides — 4 of which are explicit § 12.13 deferrals (per OP § 4.1 framing-audit checklist, the Q3 "refine framing rather than execute" answer was correctly "no, deferrals are authorized scope at Phase 5; refine Pattern B not Phase 5"). Hotspot D pre-display coverage filter was correctly NEW-flagged as deferred (not silently consumed).

### Discipline #18.2 — methodology hotspot

**Status: PASS.** drax correctly flagged Hotspot D (pre-display coverage filter) as elrond consultation candidate post-star-lord kit-corpus cascade-dimension index. Did not silently consume the methodology question.

---

## Recommendations for next-phase work

### Pattern B cluster naming + cascade text vocabulary canonical session

Per § 12.14 sequencing item 4, this is the next gandalf-Matt Pattern B engagement. Scope per Phase 5 design review:

1. **Cluster naming canonical lock** — the 7 sky cluster regions corresponding to 7 Tier 1 anchors. Are they "Race-cluster" or evocative-name? § 12.13 names this as open. Recommendation: evocative-names with substrate-led semantic rep-audit (cluster centroid in BC space + top-reps from substrate → evocative-name appropriate to substrate, not pre-imposed).

2. **Cascade Tier 2/3 vocabulary refinement** — specific edits flagged in § 2.3 + § 2.4 above:
   - Tier 2 (4 revisit): Race "Which lineage shapes your form?", Power "What shape does your power take?", Style "How do you move through encounters?" OR "What is the shape of your engagement?", Horizon "How far does your path reach this season?"
   - Tier 3 (3 revisit): Water "Does the water hold or sweep?", Lightning "Does the lightning strike once or arc?", Burst "Does the burst peak once or stack?"

3. **Spirit guide voice character anchor** — pin voice between Diablo-IV-Lilith register (too cold) and Mushoku-Tensei-Roxy register (too warm); explicit reference: "the voice an experienced friend uses explaining a system." Specific template edit: `tier1_commit` "You are drawn to" → "Your path projects toward" per D31 honesty.

4. **Cluster spatial layout** — non-3×3-grid arrangement, ideally substrate-driven via Hotspot A elrond consultation; heptagonal or 7-pointed-arc; spatial relationships suggesting cosmological relationships between Layer 0 input precedents vs Layer 2 experiential axes.

5. **Tier 3 follow-up coverage policy** — Pattern B locks whether all Tier 2 options must have Tier 3 follow-ups OR some genuinely terminate at depth-2 (substrate-truth-wins recommends substrate-driven decision).

Estimated scope: ~1 hour gandalf+Matt Pattern B (matches § 12.13 + § 12.14 estimate).

### Vertical-slice spike scope refinement (per § 12.11)

Pattern B output composes natively into vertical-slice spike scope:
- iPad text-list cycling UI (Phase 5 → ports as design intent)
- Cycling-preview cosmograph response animation (Phase 5 → ports via Pixi ticker interpolation; UE-port via Niagara per drax close report § 8.2)
- Spirit guide narration cascade (templates locked at Pattern B)
- Nearest-kit-centroid lookup (engine-API; Hotspot D coverage filter integrated)
- Final form emergence narration (templates locked at Pattern B)

### WS2 Niagara commission scope refinement (per § 12.11)

Per § 12.10, per-primitive icon rendering NOT needed (RETIRED at scope). WS2 commission:
- Rune-anchors-in-sky AAA fidelity (7 sky cluster regions corresponding to 7 Tier 1 anchors)
- Sky-cluster spatial layout per Pattern B substrate-driven lock
- Camera fly-through animation specifications (~0.3-0.5 sec per § 12.4)
- Dim-all + radial glow / Niagara particle attenuation effects
- Spirit guide voice synthesis + spatial audio (drax close report § 8.4 gap)

### Phase 5.5 tuning (drax-owned)

Per drax close report § 6:
- Pixi ticker alpha interpolation for sky overlay (NOT instant) — mandatory before vertical-slice ships
- 400ms ramp matches § 12.4 ~0.3-0.5 sec intent

### Hotspot D pre-display coverage filter (elrond consultation; gated)

Per close report § 4 + § 9, elrond consultation gates on star-lord kit-corpus cascade-dimension index. Sequencing: star-lord adds cascade-anchor metadata to kit corpus → elrond consults methodology → drax implements coverage filter. This is the long-tail item that closes § 12.7 substrate-truth-wins discipline at the production scope.

---

## Sign-off

**Verdict: PASS-WITH-DESIGN-RECOMMENDATIONS.**

Phase 5 amendment delivers the § 12 architectural pattern at the player surface with high architectural fidelity. The work survives empirical contact at the React/Vite layer; no recognition surfaces require § 12 amendment. The design-side recommendations concentrate on Pattern B follow-on scope (cluster naming + vocabulary + voice + spatial layout) and on Phase 5.5 tuning (Pixi ticker interpolation). Discipline #40 #41 #42 cross-checks pass. D7 AI-tell line preserved. D28-D32 neutral-data-oracle voice mostly aligned (one template edit recommended). Sign-overloading semantic preserved across all 4 readings.

**Composition with jack-ryan Gate-2:** jack-ryan owns process-side review (scaffold flag verification + acceptance criteria #1-#12 + 5+6 review principles + BLOCK authority on process discipline failures). My design-side review composes additively; the two verdicts go to KR for aggregate Phase 5 close sequencing.

**Authority chain preserved:** § 12 canonical lock (gandalf-authored) → Matt 2026-06-10 sequenced directive → Phase 5 GREEN → gandalf design review PASS-WITH-DESIGN-RECOMMENDATIONS → KR sequences at wave-close.

**Auto-commit per CLAUDE.md addendum.** Push timing: KR sequences at wave-close per autonomous-cadence authority.

**Empirical-evidence triggers for downstream commitments:**
- Pattern B cluster naming + cascade text vocabulary fires per Matt scheduling
- Phase 5.5 Pixi ticker tuning fires before vertical-slice spike ships
- WS2 Niagara commission scope authoring fires post-mantis-windowed-mode-Niagara-verification (per Option A/B Matt decision queued from 2026-06-10 PC hive-mind close)
- Hotspot D pre-display coverage filter fires post-star-lord kit-corpus cascade-dimension index

**Anchor docs cited:**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 11.2, § 11.4, § 12.1-§ 12.15
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 5.6 D28-D32
- `canonical/story/style-register.md` Candidate B lock
- `agentic_orchestration/drax/notes/2026-06-10-forge-phase-5-amendment-close-report.md` § 1-§ 11
- `reincarnated-loadout/src/data/cascadeData.ts`
- `reincarnated-loadout/src/components/Cosmograph/CascadePanel.tsx`
- `reincarnated-loadout/src/components/Cosmograph/RuneLayerCanvas.tsx`
- `reincarnated-loadout/src/pages/Forge.tsx`

**Signed:** gandalf 2026-06-10
