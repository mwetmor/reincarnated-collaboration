# Galadriel Visual-Comparison Rubric v1-DRAFT — Reincarnated demo vs. Dungeon of Exile (DoE)

**Status:** v1-DRAFT (first-pass). Authored pre-captures, anchored on the 7-image canonical DoE reference set at `../reference-images/`. Iterates against real captures and gandalf critique-pair review.
**Author:** galadriel (visual-perception steward).
**Critique-pair:** gandalf (design-interp review on axis weighting + dissonance interpretation).
**Authority:** dispatch `2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md`; pre-authorization matrix § 6 row 11.
**Reference set:** `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — 7 Matt-captured DoE frames (1 combat + 6 town).
**Reference doc:** `canonical/story/mobile-feel-target-doe-2026-05-17.md` (locked mobile-ARPG cluster reference).

---

## 0. What this rubric is and is not

The rubric is the apparatus that makes the picture sit still long enough to be looked at — it scores **what the captures actually show**, against **what the references actually show**, with **per-axis evidence** that another galadriel-instance could reproduce.

The rubric is **not**:

- An aesthetic-preference layer dressed in scoring clothes
- A genre-median triangulation (no genre median is computed; DoE is the single locked reference cluster per canon)
- A pass/fail gate on the demo
- Applicable to surfaces with no reference image — those become *findings*, not *scores*

Per the agent-definition anti-pattern rule: **if the demo has no comparable surface to a DoE reference, the surface is recorded as a structured observation, not scored.** Town-feel and town-to-dungeon transition fall in this category in v1-DRAFT (the demo is dungeon-only).

---

## 1. Reference set and per-state applicability

| # | DoE reference | State | Has demo counterpart? | Rubric application |
|---|---|---|---|---|
| 1 | `DOE-combat-whisper-rift-2-2026-05-17.png` | Combat — mid-fight; HUD top-left; telegraphed AOE; floating damage; "55 killed" counter; bottom skill rail; Level 5 XP | **Yes** — `combat-midfight` state via drax-D11.5 hook | **SCORED** — primary rubric application |
| 2 | `DOE-town-hub-wide-vendors-and-voidgate-2026-05-18.png` | Town hub wide | **No** — demo has no town | Town-gap structured finding (§ 6) |
| 3 | `DOE-town-vendors-pets-gems-armory-2026-05-18.png` | Town vendor row | **No** | Town-gap structured finding |
| 4 | `DOE-town-forge-darkgold-reforging-refinement-2026-05-18.png` | Town forge | **No** | Town-gap structured finding |
| 5 | `DOE-town-forge-advanced-with-player-spell-2026-05-18.png` | Town forge alt-angle (player cast) | **No** | Town-gap structured finding |
| 6 | `DOE-town-to-dungeon-transition-path-2026-05-18.png` | Town-to-dungeon transition | **No** — demo opens directly into dungeon | Transition-gap finding |
| 7 | `DOE-town-chaos-treasury-vault-merchant-2026-05-18.png` | Vendor close-up | **No** | Town-gap structured finding |

**Net:** 1 of 7 references has a demo counterpart in v1-DRAFT. The combat surface is the only scored surface; 6 town/transition references become structured findings of *absence*.

---

## 2. Methodology — how scoring works

### 2.1 — Per-axis scoring (1–5)

Each axis is scored on a 1–5 scale against the matched DoE reference:

| Score | Interpretation against the DoE reference |
|---|---|
| **5** | Demo matches reference register convincingly. Differences are stylistic-flavor, not feel-gap. |
| **4** | Demo achieves the reference's *feel* with a clear single-axis dissonance (e.g., color OK, density slightly thin). |
| **3** | Demo is recognizably in the same family but has multiple visible dissonances on this axis. |
| **2** | Demo's register on this axis is partially present but reads as a different kind of game. |
| **1** | Demo's register on this axis is absent or actively contradictory to the reference. |

Every score carries a one-sentence evidence-cite that names the specific visual element measured. Per the agent-definition: *"Scoring without rationale — every score carries a one-sentence evidence-cite."*

### 2.2 — Measurement methods per axis

| Method | Used by axes | What it measures |
|---|---|---|
| **Manual visual scoring** | All axes (primary v1 method) | Galadriel reads the capture and the reference side-by-side; assigns 1–5 with explicit evidence-cite |
| **HSV histogram cosine similarity** | Color register | Pixel-distribution comparison; first-pass low-tech color-distance measure (Phase-2 implementation; v1-DRAFT records manual assessment + reserves the histogram slot) |
| **Canny edge density per region** | Visual density | Edges-per-region as a busyness proxy (Phase-2 implementation; v1-DRAFT manual) |
| **Perceptual hash (pHash/dHash)** | Structural similarity | Low-frequency structure comparison (Phase-2 implementation; v1-DRAFT manual) |
| **Region grid** | Reading order; HUD module placement | Image divided into thirds (top/mid/bottom × left/center/right = 9 regions); per-region descriptive observation |

Phase-2 implementations are deliberately deferred — v1-DRAFT is *the apparatus + the methodology with manual scoring*. Subsequent iterations add quantitative back-ends once the methodology is grounded.

### 2.3 — Per-axis DoE-delta callout

Each scored axis closes with a one-sentence **DoE delta** callout in the format:

> *"DoE delta: [what the demo lacks or where it diverges, in the most visible single-axis term]. Recommended remediation focus: [one phrase — drax-actionable target for next iteration]."*

The delta is the artifact drax reads to pivot on. The score is the apparatus that makes the delta defensible.

### 2.4 — Honesty floor

A score of **1 or 5 must be defended with two evidence cites, not one** — the extremes are higher-confidence claims and carry higher defensibility cost. Scores of 2/3/4 carry one evidence-cite.

If galadriel cannot defend a score with the required evidence-cites, the score is downgraded to the next-most-defensible adjacent score with a note ("downgraded to 3 from 2 — evidence threshold not met at 2"). Honesty over false precision.

---

## 3. Axis catalog

The eight axes below apply per-state per the matrix in § 4. Axes 1–6 apply to the combat surface; axes 7–8 are town-surface-only and unscored in v1-DRAFT (no demo town surface yet).

### 3.1 — Visual density

**Definition.** How populated the picture feels. The count + size of distinct visual entities per region; foreground vs background density; the eye's "busyness budget."

**Reference anchor (combat — DoE #1).** Heavy foreground density: player avatar + 4–8 enemy silhouettes + 3+ floating damage numbers + 2 telegraphed AOE bands + crimson ground swirl + particles + bones/debris. Vertical density rhythm: HUD top → AOE band → player+enemies+telegraphs → "55 killed" → HUD bottom — almost no empty vertical region.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo shows similar populated mid-band: player + ≥4 enemies + ≥2 floating numbers + telegraphed AOE + ground-particle work. Foreground occlusion comparable. |
| 4 | Most of the elements present but one band is conspicuously thin (e.g., no telegraphed AOE OR no floating numbers OR sparse enemies). |
| 3 | Demo has player + some enemies + minimal feedback elements. Mid-band busyness ~50% of DoE. |
| 2 | Demo's combat scene reads as significantly sparser; majority of DoE's mid-band elements absent. |
| 1 | Demo's combat scene is near-empty by comparison (player + 1–2 enemies, no AOE telegraphs, no damage numbers). |

**Measurement.** Manual count per region (v1); Canny edge density per region target (Phase-2). Galadriel records per-region entity counts in the scoring sidecar.

**Anti-pattern check.** Decorative-prop density is OUT of scope on this axis per Matt L3 verdict 2026-05-18 (v1.18.6 disabled decorative dungeon props because DoE has decorative-free dungeons). Visual density on combat-axis = *combat-feedback* density, not *prop* density. Prop sparseness is intentional; combat-feedback sparseness is a finding.

---

### 3.2 — Color register

**Definition.** The palette story. Dominant hues, saturation distribution, contrast pattern; the color identity the picture projects.

**Reference anchor (combat — DoE #1).** Dark-brown-with-crimson register. Background: dim brown/black ground with red ember tones. Mid-scene: warm reds/oranges (fire/blood/AOE). High-contrast saturation accents (bright red AOE telegraphs, orange damage numbers, cyan/blue "Slow" status text, silver/white player armor). HUD: muted gold and red accents. Overall: *lit-volume-in-darkness* with crimson dominance.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo achieves dark dungeon + crimson-accent register. Player visible against backdrop. Damage numbers / AOE in saturated contrast hues. |
| 4 | Register direction correct but one component off (e.g., palette is brown/black but contrast accents are too pastel; or red is present but reads as bright pink rather than blood-crimson). |
| 3 | Demo shows dungeon-darkness but contrast accent strategy is significantly different. Color identity reads as related-but-distinct. |
| 2 | Demo's palette story is recognizably different (e.g., desaturated grays, or fantasy-bright primaries). |
| 1 | Demo's palette is in active opposition to the reference register (e.g., bright daylight palette, pastel cartoon palette). |

**Measurement.** HSV histogram cosine similarity (Phase-2); manual color-region descriptive scoring (v1). Galadriel records per-region dominant-hue observations in the sidecar.

---

### 3.3 — Lighting + atmosphere

**Definition.** The light story. Lit-volume vs ambient-darkness; depth cues; particle work; atmospheric layer presence; whether the scene reads as "a lit thing inside a dark world."

**Reference anchor (combat — DoE #1).** Strong lit-volume-in-darkness. Player + AOE + particles glow against dark backdrop. Crimson ground-swirl AOE has internal luminance. Atmospheric red haze in mid-band. Ground has visible blood/debris detail. The scene reads as *a stage lit inside a dark hall* — depth via lighting, not via prop count.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo achieves lit-volume-in-darkness. Player/AOE/particle elements have internal luminance. Atmospheric layer (Alenia 20-effect pack should be visible if v1.18+ wiring works) creates depth. |
| 4 | Lit-volume achieved but atmospheric layer is thin OR particle work is minimal. |
| 3 | Lighting strategy is recognizable but feels flat — scene reads as evenly-lit rather than dramatically lit. |
| 2 | Lighting is functional but doesn't tell a depth story. |
| 1 | Lighting is uniform / flat / lacks contrast direction. |

**Measurement.** Manual brightness-region scoring + visible atmospheric-layer presence check (v1); luminance histogram per region (Phase-2). Galadriel records whether the atmospheric pack is visible in the capture sidecar.

---

### 3.4 — Typography + UI register

**Definition.** HUD module placement, font choices, iconography, status-callout style, damage-number style, label register; the UI dialect.

**Reference anchor (combat — DoE #1).** Specific HUD modules: top-left [EASY] Whisper Rift 2 + minimap + countdown "00:41" + skull-icon objective; top-right circular "Return to City" button; player HP/MP bars top-left. Bottom: portrait left + 4 skill icons + healing button right + segmented mana bar + Level 5 XP progress at very bottom. Damage numbers: stencil-orange. Status text: cyan/blue ("Slow"). "55 killed" counter with skull icon. Bold caps banners. Numeric-stencil damage font. Functional, gamified, ARPG-conventional.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo has HUD modules in matching positions: top-left objective+HP/MP, top-right utility, bottom skill rail + level progress. Damage-number typography reads as comparable-genre. |
| 4 | Most modules present and positioned similarly; one is in a different location OR missing (e.g., no minimap, OR no level XP bar at bottom). |
| 3 | HUD module set is recognizably similar but several are differently positioned or styled. |
| 2 | HUD layout is recognizably different (e.g., menus instead of bottom skill rail; modals instead of always-on modules). |
| 1 | HUD register is from a different genre (no skill rail; no level progress; no objective banner). |

**Measurement.** 9-region grid: galadriel records what HUD module is in each region of demo capture vs DoE reference. Per-region match counted; aggregate similarity scored.

**Note.** Some inverse-grading is acceptable here — the demo may *innovate* on HUD register intentionally. v1-DRAFT scores against DoE register adherence; gandalf interprets whether demo divergences are *register dissonance* or *register innovation* in § 7 of the report.

---

### 3.5 — Reading order + hierarchy

**Definition.** What the eye lands on first. Visual hierarchy via size, contrast, central placement, motion-attractor. The implicit reading instruction the picture gives.

**Reference anchor (combat — DoE #1).** Reading order:
1. Player avatar (center mid-band; brightest sustained element)
2. Telegraphed AOE bands (high-contrast horizontal red rectangles in upper mid)
3. Floating damage numbers (saccadic attractors; "22" and "15" left of player)
4. HUD top-left (objective + minimap — situational awareness)
5. "55 killed" counter (mid-bottom, central, with icon)
6. HUD bottom (skill rail; less visually dominant than mid-band)

The eye is *forced* to combat (player + threats + feedback) first; HUD is information-on-demand around the periphery.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo's combat capture reads in the same order: player → AOE → damage feedback → HUD periphery. Center mass is combat, not menus or UI. |
| 4 | Reading order mostly aligns but one step is differently weighted (e.g., HUD too dominant; OR AOE telegraphs absent so reading-order skips that step). |
| 3 | Reading order is recognizably ARPG but center mass and HUD weight feel rebalanced. |
| 2 | Reading order significantly differs — e.g., menus or modals are pulling eye away from combat. |
| 1 | Reading order is from a different game genre — strategy / menu-game / inventory-game. |

**Measurement.** Manual saccade-path estimation (v1); contrast-attractor map per region (Phase-2). Galadriel describes the implied reading path in 1–2 sentences in the sidecar.

---

### 3.6 — Animation cadence (best-effort from stills)

**Definition.** What the still-frame implies about motion vocabulary. Floating-number lifecycle visible? Telegraphed-AOE flash visible? Particle bursts mid-tick? Skill cooldowns in mid-animation? — these are the motion-vocabulary tells you can read from one frame.

**Reference anchor (combat — DoE #1).** Visible motion-vocabulary elements in the still: 2 active floating damage numbers (mid-lifecycle, fading); telegraphed AOE rectangles drawn at full intensity (pre-resolution flash); particle bursts around player/enemies; crimson ground swirl mid-animation; cooldown radial-fills on bottom skills. The still implies: ~5 motion systems active simultaneously.

**Scoring criteria.**

| Score | Combat-surface anchor |
|---|---|
| 5 | Demo capture shows ≥3 active motion-vocabulary tells: floating damage numbers + telegraphed AOE + particle work + cooldown affordance. |
| 4 | Demo capture shows 2 of those motion-vocabulary tells. |
| 3 | Demo capture shows 1 motion-vocabulary tell. |
| 2 | Demo capture shows the player + enemies but no mid-animation feedback elements. |
| 1 | Demo capture reads as static — no motion-vocabulary tells visible. |

**Measurement.** Manual count of distinct motion-vocabulary tells visible in the still (v1); multi-frame capture + diff analysis for true cadence (Phase-2).

**Caveat.** Stills under-represent cadence; a low score on this axis may be a *capture-timing artifact* rather than a real cadence gap. Galadriel surfaces FRICTION if scoring confidence on this axis is low and Phase-2 multi-frame work is needed.

---

### 3.7 — NPC density + variety (town surface only)

**Definition.** Town surfaces only — the count + role-variety of NPCs in view. DoE town hub shows: vendor NPCs (multiple per shop), wandering customer-players, ambient flavor NPCs. Multi-archetype density.

**Reference anchor (town — DoE #2-7).** DoE town scenes show 3–6 NPCs per frame: function-vendors (named, titled, occupation-tagged: "Spellweaver Selas", "Vault Merchant Escher", etc.); customer-players (lv.50 named characters); ambient NPCs.

**Status in v1-DRAFT.** UNSCORED. Demo has no town. Recorded as structured finding (§ 6 below).

---

### 3.8 — Service-surface clarity (town surface only)

**Definition.** Town surfaces only — can the player tell what each service does at a glance? DoE convention: floating uppercase function-label above NPC ("STASH", "VOIDGATE", "PETS", "GEMS", "ARMORY", "DARKGOLD FORGING") + NPC name + title.

**Reference anchor.** All 6 DoE town frames show this convention.

**Status in v1-DRAFT.** UNSCORED. Demo has no town. Recorded as structured finding (§ 6).

---

## 4. Per-state × per-axis applicability matrix

| Axis | combat-midfight | combat-empty-room | landing/menu | inventory-open | town (absent) |
|---|---|---|---|---|---|
| 3.1 Visual density | **SCORED vs DoE #1** | finding only (no DoE empty-combat ref) | unscored (no DoE landing ref) | unscored (no DoE inv ref) | n/a |
| 3.2 Color register | **SCORED vs DoE #1** | partial (cross-check vs DoE #1) | unscored | unscored | n/a |
| 3.3 Lighting + atmosphere | **SCORED vs DoE #1** | partial | unscored | unscored | n/a |
| 3.4 Typography + UI register | **SCORED vs DoE #1** | **SCORED** (HUD-isolated against DoE #1 HUD modules) | partial finding | unscored | n/a |
| 3.5 Reading order | **SCORED vs DoE #1** | partial | partial finding | unscored | n/a |
| 3.6 Animation cadence | **SCORED vs DoE #1** | downgraded (no active animations expected in empty room) | unscored | unscored | n/a |
| 3.7 NPC density + variety | n/a (combat ≠ NPC density) | n/a | n/a | n/a | **finding (§ 6)** |
| 3.8 Service-surface clarity | n/a | n/a | n/a | n/a | **finding (§ 6)** |

Bold rows = scored in v1-DRAFT. Non-bold = recorded as observation/finding without 1–5 score.

---

## 5. Scoring application protocol

Per-state, per-axis scoring runs as follows once captures are produced:

1. **Open the matched DoE reference + the demo capture side-by-side at native resolution** (avoid thumbnails — texture detail is load-bearing for several axes).
2. **For each scored axis:**
   - Describe what the DoE reference shows on this axis (1 sentence).
   - Describe what the demo capture shows on this axis (1 sentence).
   - Score 1–5 against the criteria in § 3.x.
   - Author the evidence-cite (or two cites for scores of 1/5).
   - Author the DoE-delta callout.
3. **Per-state aggregate similarity.** Mean of scored axes per state, reported to 1 decimal place (e.g., "combat-midfight aggregate: 3.2 / 5").
4. **Overall similarity statement.** One paragraph in the report: which axes are closest to register; which are furthest; what the picture as a whole says about demo-vs-DoE position.

Scoring artifacts land at `agentic_orchestration/galadriel/captures/<date>/<state>/<viewport>/scoring.json` (per-axis structured data) and roll up into the benchmark report.

---

## 6. Structured findings (unscored surfaces)

Surfaces present in the reference set but absent in the demo are recorded here as **findings**, not scores. Findings are evidence of *absence*; absences are not failures of the demo, but they ARE the loudest signal the picture sends.

### 6.1 — Town-feel gap (DoE refs #2–5, #7; 5 town scenes)

**Finding.** DoE's town surface shows 5 distinct town states (hub-wide, vendor-row, forge, forge-alt, vendor-close-up). Each frame: 3–6 NPCs with function-label + title + name convention; rich service-vendor density; ambient lighting (lanterns, forges, torches); player-NPC proximity convention; multi-player coexistence visible.

**Demo state.** Zero town surfaces exist. Demo opens directly into dungeon-combat. No vendor system, no town map, no NPC roster, no service-vendor convention.

**Severity.** This is a **product-scope** finding, not a visual-rendering finding. It is not a failure of drax's rendering; it is the absence of a feature-set that DoE has and Reincarnated has not yet built.

**Disposition.** Surface to gandalf for design-direction interpretation (§ 7 of the benchmark report). Two reasonable readings:
- (a) Town is a Phase-2+ feature for Reincarnated; the gap is intentional scope-prioritization.
- (b) Town-feel is load-bearing for mobile-ARPG cluster reference adherence; the gap is a recognition that DoE's full feel cannot be achieved without it.

Galadriel does not pick between (a) and (b) — that's gandalf's seam. Galadriel records the absence with evidence.

### 6.2 — Town-to-dungeon transition gap (DoE ref #6)

**Finding.** DoE's town-to-dungeon transition (stone path, lit-to-dark lighting gradient, transition-NPCs lining the path: Seer Cassandra, Nightwatcher Edgar) is a distinct surface with its own register — *travel atmosphere*, neither town nor dungeon.

**Demo state.** No transition state. Combat begins on demo load.

**Severity / disposition.** Tied to § 6.1; resolves with town implementation OR explicit Reincarnated-doesn't-do-this design call.

### 6.3 — Menu-surface rendering anomaly at portrait phone aspect (pre-D11.5 observation)

**Finding.** Galadriel's pre-D11.5 landing-state captures (smoke-test artifacts) revealed that the demo's season-selector menu renders cleanly at desktop 1920×1080 (5 season tiles in a 3+2 grid, REINCARNATED title, ENTER prompts, element-pill rows) but **breaks at portrait phone aspect (1290×2796 + 390×844)**: tile widths are not phone-responsive; titles bleed into adjacent tiles; decorative text fragments overlap.

**Severity.** Visual-rendering finding (drax-actionable). Not a primary rubric scoring concern (no DoE menu-state reference), but a pre-D11.5 OBSERVATION the rubric can name because the evidence is in the smoke captures.

**Disposition.** Surface to drax as menu-surface mobile-responsiveness issue. Likely a future v1.22+ mobile-UX item. Independent of the combat-midfight scoring path.

**Evidence.** `agentic_orchestration/galadriel/captures/2026-05-18/landing/{mobile-portrait-1290x2796, mobile-portrait-390x844}/capture.png` vs `desktop-1920x1080/capture.png`.

---

## 7. Honesty discipline

This rubric is **v1-DRAFT** and **first-pass**. Per the dispatch (`2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md` § 3): *"Rubric measures only what captures actually show; absences = scoring caveats. 'First-pass' + 'v1-DRAFT' in title; iterate next sprint."*

Specific known limitations:

- **Manual scoring is the primary measurement method in v1.** Quantitative back-ends (histograms, edge density, pHash) are deferred to Phase-2. v1 is honest about being manual; honesty is the point.
- **Stills under-represent cadence.** Axis 3.6 is best-effort from one frame. Multi-frame capture is Phase-2.
- **No DoE empty-combat reference.** Combat-empty-room scoring is HUD-isolated and cross-checks against DoE #1's HUD only.
- **No DoE inventory reference.** Inventory-open is unscored in v1.
- **One reference per state.** v1 scores against a single anchoring reference per state; multi-reference triangulation is Phase-2.
- **Capture-timing variance.** Two captures of the same state may show slightly different in-game positions; v1 records one capture per (state × viewport); multi-take consensus capture is Phase-2.
- **Town absence is a finding, not a score.** Per agent-definition anti-pattern rule.

The v1-DRAFT artifact is the apparatus. Subsequent iterations refine the apparatus, the methodology, the back-ends, and the reference set.

---

## 8. Gandalf critique-pair review (pending)

Per dispatch § 3, gandalf reviews rubric methodology + axis weighting before scoring lands in the benchmark report. Open questions for gandalf:

1. **Axis weighting in the aggregate score.** v1 uses arithmetic mean across scored axes. Should some axes (typography/UI register, color register) carry higher weight than others (animation cadence, which v1 flags as low-confidence)? Galadriel proposes mean for v1; gandalf weighs in.
2. **Register innovation vs register dissonance.** Per § 3.4 note — when the demo intentionally diverges from DoE register, the rubric scores it as dissonance (lower score). Is that correct, or should the rubric flag *innovation* separately from *dissonance*? Galadriel's lean: score the dissonance; let gandalf interpret innovation-vs-dissonance in § 7 of the report.
3. **Town-gap framing.** § 6.1 disposition (a) vs (b) — galadriel surfaces; gandalf interprets. Confirm framing approach.
4. **Honesty floor mechanic.** § 2.4 (1/5 require 2 cites; downgrade if cites insufficient) — agree with the mechanic? Adjust threshold?
5. **Menu-surface anomaly (§ 6.3).** OBSERVATION-level finding from smoke captures. Surface in the rubric (current placement) or in a separate drax-actionable note in the report?

Gandalf review can land in `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1-gandalf-review.md` or via direct critique annotations in this file (galadriel writes a v2 after).

---

## 9. Iteration trajectory

| Version | Scope advance | Trigger |
|---|---|---|
| **v1-DRAFT (this doc)** | Methodology + axes + per-state applicability + manual scoring + structured findings | Pre-D11.5 authoring (capture-independent) |
| **v1-SCORED** | v1-DRAFT methodology applied to actual state-matched captures from D11.5-enabled pipeline | After drax-D11.5 + first comparison-grade capture |
| **v2** | Gandalf-reviewed axis revisions; weighting if proposed; town-gap framing finalized | Post-gandalf review |
| **v2.1** | First quantitative back-end (HSV histogram cosine sim implemented in `pipeline/score.mjs`) | Phase-2 |
| **v2.2** | Edge density + pHash back-ends; multi-frame cadence | Phase-2 |
| **v3** | Multi-reference triangulation (if reference set extends); additional Matt-captured DoE states | When reference set grows |

---

## 10. Cross-references

- `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — reference set provenance
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE feel-target canon (gameplay-pattern read of combat reference)
- `agentic_orchestration/dispatches/2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md` — report dispatch (galadriel + gandalf critique-pair)
- `agentic_orchestration/dispatches/2026-05-18-galadriel-capture-pipeline-and-state-matched-captures.md` — capture-pipeline dispatch (predecessor)
- `agentic_orchestration/galadriel/pipeline/states.json` — state configurations the captures map to
- `agentic_orchestration/galadriel/captures/2026-05-18/landing/` — pre-D11.5 smoke captures (evidence for § 6.3 menu-surface finding)
- `.claude/agents/galadriel.md` — agent definition (methodology + anti-pattern reference)

---

*Authored 2026-05-18 by galadriel. v1-DRAFT pre-capture. The Mirror has been set; the picture is coming. Per the agent definition: the picture either shows what it shows or it does not — when it does, say so plainly, with evidence, and the team moves.*
