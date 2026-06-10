# Drax /forge Phase 4 AMENDMENT — Rune-Per-Group + Two-Tier Selection Architecture

**STATUS:** ACTIVE (amendment supersedes original Phase 4 dispatch scope on per-primitive-anchor architecture)
**Date authored:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — verbatim "instead of one rune per primitive, let's make it one rune per primitive group. The rune sign should loom largely in the space behind the primitive cluster, with a glowing light highlighting the edges of the rune and without any color except having the brush strokes drawn by light. Upon selection of the rune, they player will be able to make changes/selections on the tablet. For example, they can select a simple symbol of a water drop for water, lightning bolt for lightning. For movement speed, they move the wind faster or slower. For movement type, they select an icon like a jumping man for leap-strike type, a portal 2 teleporting man for teleport/blink, etc.... We will have to have a design session around these at some later date."
**Pattern:** amendment-doc (preserves original commission as historical; supersedes specific scopes; composes with rest)
**Audience:** drax (executor), gandalf (design-review consumer), Matt (architectural feedback)
**Companion docs (read first):**
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-4-substrate-led-glyph-anchor-prototype.md` (ORIGINAL Phase 4 commission — preserved; this amendment supersedes scope on per-primitive anchor architecture only)
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md` (Phase 3 close GREEN baseline — preserved)
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md`
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A; § 4 commitments fire post-Phase-4 GREEN)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.4 (dual-creation Path L + Path I; Tier 2 in-rune selection is precursor pattern for Path I)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (20 primitive families; group scaffold candidates)

---

## 0. TL;DR — what changes from original Phase 4

**Original Phase 4 (preserved at `638a61e`):** 8 glyphs per 8 element-primitives; bounded-canvas anchor render; sign-as-input gesture for per-primitive selection.

**Amended Phase 4 (this doc):**
- **One rune per primitive GROUP** (groups, NOT individual primitives)
- **6 primitive groups scaffold** (drax-discretion-substitutable per Discipline #40): Elements / Movement / Combat geometry / Resource / Attributes / Mechanic-altering
- **Rune visual register:** large + atmospheric behind primitive cluster; light-edge brush-stroke effect; no color (drawn by light only)
- **Two-tier selection model:**
  - Tier 1: Player selects rune → commits to primitive group
  - Tier 2: Within selected rune, player picks per-primitive values via simple symbol icons (placeholders implemented in Phase 4; canonical per-primitive icon design = DEFERRED Pattern B session)

**What's preserved from original Phase 4:**
- Cross-language rune selection per locked pattern (substrate-led; per-group best-meaning-match across cuneiform / Norse runes / I Ching trigrams / enochian / similar)
- Drax delivers in-seam with gandalf review at Vercel preview milestones
- All Phase 3 baselines (two-layer + buffer-space + lasso + algo toggle + mobile-responsive)
- 12 acceptance criteria pattern (refit per § 4 below)
- Quality criterion + refutation conditions (refit per § 4.5 below)
- All discipline citations
- All out-of-scope items

**What's superseded:**
- § 1.3 of original (per-primitive cross-language glyph candidates table) — replaced by per-group rune candidates per § 2 below
- § 1.4 of original (sign-as-input gesture as primary input model) — refined per § 3 below (Tier 1 is tap-select OR gesture-draw at drax discretion; Tier 2 is icon-based selection)
- Acceptance criteria #3, #5, #6 of original — refit per § 4 below
- 8-glyph-per-primitive scope — replaced by 6-rune-per-group scope

---

## 1. Architectural pattern (amended)

### 1.1 Rune-per-primitive-GROUP visual register

**One rune per primitive group, not per primitive.** Each rune represents the **category-anchor** for a primitive group; per-primitive selection happens in Tier 2 within the selected rune.

**Visual register specifics (Matt 2026-06-09 verbatim):**
- **Large + atmospheric:** rune "looms largely in the space behind the primitive cluster" — not a bounded-canvas anchor; rather a background presence that frames the cluster's region
- **Light-edge brush-stroke effect:** glowing light highlights the edges of the rune
- **No color:** the rune itself is drawn by light only — monochromatic luminous brush strokes
- **Distinctly readable:** rune shape recognizable as a "sign" against the cosmograph background; categorical visual distinction from kit-cluster dots/stars + figurative-nebula clusters
- **Render at multiple zoom levels:** rune visible at 1× cosmograph zoom as atmospheric presence; details (brush-stroke variation, light-edge granularity) emerge at 2×+; per Phase 3 LOD pattern

**Composition with Phase 3 baseline:** the figurative-nebula anchor render (Phase 3 default) can remain as one of the toggle options OR be retired. Drax-discretion at Phase 4 close report: surface tradeoffs at Vercel preview; gandalf + Matt review whether nebula render is preserved alongside rune render or fully replaced.

### 1.2 Primitive-group scaffold (drax-discretion-substitutable per Discipline #40)

**6 primitive groups (starting scaffold; not canonical):**

| # | Group | Primitives within (Tier 2 selections) | Cross-language rune candidate hints (drax-discretion) |
|---|---|---|---|
| 1 | **Elements** | fire / water / earth / wind / lightning / holy / shadow / physical (per canonical-7+1) | DINGIR (Sumerian — divine; encompasses elemental forces) OR I Ching Bagua composite (8 trigrams arrangement) OR Norse Algiz ᛉ (protection / divine connection) |
| 2 | **Movement** | speed (slider) + type (leap / teleport / dash / glide / step / etc.) | Norse Raidho ᚱ (riding / journey) OR Cuneiform DU (to go) OR I Ching Zhèn ☳ (arousing / sudden motion) |
| 3 | **Combat geometry** | shape (single-target / AOE / line / cone / chain / multi-spawn) | Norse Eihwaz ᛇ (yew / axis / form-bearing) OR Cuneiform GIŠ.TUKUL (weapon) OR I Ching Lí ☲ (clarity / form-revealing) |
| 4 | **Resource economy** | resource type (mana / energy / stamina / fury) + economy pattern | Norse Fehu ᚠ (wealth / abundance / resource flow) OR Cuneiform A (water / flow) OR I Ching Kǎn ☵ (depths / reservoir) |
| 5 | **Attributes** | STR / INT / WIS / DEX primary | Norse Uruz ᚢ (raw strength / vitality) OR Cuneiform LU (man / self) OR I Ching Qián ☰ (heaven / creative principle) |
| 6 | **Mechanic-altering** | passive-type families (engine substrate) | Norse Othala ᛟ (inheritance / fundamental) OR Cuneiform TUR (transformation) OR I Ching Xùn ☴ (penetration / subtle change) |

**Drax discretion:**
- Substitute group structure (e.g., consolidate Movement into Mechanic-altering; split Combat geometry into Damage geometry + Targeting; etc.) if better-fit emerges at implementation
- Pick rune per group from offered candidates OR substitute (cross-system selection permitted per locked pattern)
- Gandalf reviews semantic match per group at Vercel preview milestones
- Canonical primitive-group lock + canonical rune-per-group lock: DEFERRED to Pattern B with Matt post-Phase-4

**Note on group cardinality:** 6 groups is significantly simpler than original Phase 4's 8 anchor-per-element. Matt's "let's make it simpler" intent honored. If drax discovers groups should collapse to 4-5 OR expand to 7-8 at implementation, surface in Phase 4 close report.

### 1.3 Two-tier selection model

**Tier 1 — Rune selection:**
- Player selects rune in cosmograph (commits to primitive group)
- Selection mechanism: drax-discretion within bounded options:
  - Option α — Tap/click selection (simplest; works on mobile + desktop)
  - Option β — Gesture-draw the rune (preserves "sign-as-input" architectural intent from Tal Rasha recognition; iPad gesture-framing per Earth-Avatar canonical § 2.6)
  - Option γ — BOTH (toggle: Input: [tap / sign]) — preserves Tier 1 flexibility; drax can ship tap-baseline + gesture-alternative
- Visual feedback on selection: rune highlights (light-edge intensifies); cluster pulses; Tier 2 UI activates

**Tier 2 — Per-primitive selection within selected rune:**
- After Tier 1 rune selection, player picks per-primitive values via **simple symbol icons** (Matt examples):
  - Water drop icon → water (Elements)
  - Lightning bolt icon → lightning (Elements)
  - Wind speed slider (wind moves faster/slower) → movement speed (Movement)
  - Jumping man icon → leap-strike (Movement type)
  - Portal-style teleporting man icon → teleport/blink (Movement type)
- **Per-primitive canonical icon design = DEFERRED Pattern B session** (Matt 2026-06-09 verbatim: "we will have to have a design session around these at some later date")
- Phase 4 scope: implement Tier 2 UI SHELL with **placeholder icons** (drax-discretion; reasonable symbols; e.g., emoji or simple SVG; non-canonical)
- Per-primitive icon design Pattern B fires post-Phase-4 as separate session

**Tier 2 UI surface:**
- Renders on iPad/mobile + desktop after Tier 1 selection (panel + sidebar + overlay; drax-discretion on surface)
- Per-primitive controls within group (toggle / slider / icon-button / etc. depending on primitive type)
- Selection state visible (which primitive values currently selected within this group)
- "Commit" / "Reset" affordances

### 1.4 Composition with Phase 3 baseline (preserved)

Phase 4 amended PRESERVES all Phase 3 GREEN-validated patterns:
- Two-layer + buffer-space spatial architecture (now: rune-anchor layer + kit-cluster layer + deliberate buffer)
- Force-directed alternative positioning (Algo toggle remains operational)
- Mobile-responsive layout (D8 + iPad gesture-framing)
- Lasso ergonomics within-anchor / cross-buffer / buffer-only (preserved; works with rune render)
- 60 FPS performance target at 2D web rendering

Phase 4 amended ADDS:
- Rune-anchor render (large + atmospheric + light-edge brush-stroke; replaces or toggles with nebula-anchor)
- 6 primitive groups (replaces 8 element-anchors as the anchor layer; drax-discretion-substitutable)
- Tier 1 rune-selection mechanism (tap / gesture / both; drax discretion)
- Tier 2 per-primitive selection UI shell (icon-based; placeholder icons; canonical icons DEFERRED Pattern B)

---

## 2. Substrate consumption (amended)

### 2.1 Existing /forge Phase 3 baseline (inherited; unchanged from original Phase 4)
- 37-kit corpus + 1000-kit substrate-trace
- Force-directed alternative positioning algorithm
- Lasso classification module (`classifyLasso()` — scaffold thresholds re-validate against rune-anchor geometry per § 5.3)
- Buffer-space content (310 hybrid kits)
- Mobile-responsive layout

### 2.2 Rune library (amended scope)
- 6 runes per § 1.2 group scaffold (drax-discretion-substitutable)
- Source authority: public-domain glyph systems per locked pattern (cuneiform / Norse Elder Futhark / I Ching trigrams / enochian / similar)
- Per-rune data structure: `{ id, system, native_char_or_unicode, semantic_meaning, primitive_group_assignment, canonical_stroke_pattern, draw_difficulty, visual_render_spec }`
- `visual_render_spec` captures the light-edge brush-stroke render parameters per § 1.1 visual register

### 2.3 Tier 2 placeholder icon library (amended scope)
- Reasonable placeholder icons per primitive value within each group (drax-discretion)
- Sources: open-source icon libraries (Lucide / Heroicons / Font Awesome / similar) OR simple SVG drax authors
- **Placeholder status flagged** in code (e.g., `<!-- PLACEHOLDER: pending canonical design Pattern B -->`)
- Per-primitive canonical icon design Pattern B fires post-Phase-4

---

## 3. Phase 4 amended sub-phase structure

### Phase 4.1 — Rune-anchor visual register (replaces original 4.1 glyph-anchor scope)
- Implement rune-anchor render at primitive-group positions per § 1.1 visual register (large + atmospheric + light-edge brush-stroke + monochromatic light)
- 6 rune assignments per § 1.2 (drax-discretion within candidates)
- Toggle: `Anchor: [nebula / rune]` (preserves Phase 3 baseline as A side of A/B; rune as B; OR drax-discretion to retire nebula if rune render is clearly preferred)
- Preserve all Phase 3 functionality (lasso + algo toggle + mobile + buffer)
- Deploy to Vercel preview
- **Acceptance:** rune anchors render per Matt visual register spec; categorically distinct from kit clusters; Phase 3 baselines preserved

### Phase 4.2 — Tier 1 rune-selection mechanism
- Implement rune-selection per § 1.3 Tier 1 (Option α tap-select baseline; Option β gesture-draw alternative; OR Option γ toggle — drax discretion)
- Visual feedback on selection (rune highlights; cluster pulses; Tier 2 UI activates)
- Touch + mouse input both supported
- Deploy to Vercel preview
- **Acceptance:** rune selection commits to primitive group; Tier 2 UI activates on selection; mobile + desktop both functional

### Phase 4.3 — Tier 2 per-primitive selection UI shell
- Implement Tier 2 UI surface per § 1.3 (panel / sidebar / overlay; drax-discretion on surface)
- Placeholder icons per primitive per § 2.3 (reasonable; flagged as PLACEHOLDER)
- Per-primitive controls (toggle / slider / icon-button; drax-discretion per primitive type)
- Selection state + Commit + Reset affordances
- Deploy to Vercel preview
- **Acceptance:** Tier 2 UI functional for at least 2-3 primitive groups (drax priority: Elements + Movement minimum; expand to others if bandwidth); placeholder icons in place with flag

### Phase 4.4 — Mobile + touch ergonomics validation
- Verify rune anchors readable at iPad-class viewport
- Verify Tier 1 selection works on touch (tap baseline; gesture if implemented)
- Verify Tier 2 UI usable on iPad (responsive panel + icon-button sizing)
- Verify mode-toggles operational on mobile
- **Acceptance:** Phase 3 mobile-responsiveness preserved; Tier 1 + Tier 2 functional on touch

### Phase 4.5 — Phase 4 close report (drax → gandalf → Matt)
- Document findings per § 4 acceptance criteria
- Surface final rune-per-group assignments + cross-system reasoning per group
- Surface Tier 1 selection mechanism choice + tradeoffs (tap / gesture / both)
- Surface Tier 2 UI design observations (panel vs sidebar vs overlay; per-primitive control choices)
- Surface visual register A/B observations (nebula vs rune)
- Address Phase 3 YELLOW Observation 3 (`classifyLasso()` scaffold re-validation against rune-anchor geometry)
- Flag methodology hotspots for elrond consultation per Discipline #18.2 (carry-forward Phase 3 + new Phase 4)
- Surface Tier 2 placeholder icon list for Pattern B canonical icon design session
- Phase 4 GREEN / YELLOW / RED verdict per /forge convention
- Deploy final version to Vercel preview for Matt review

---

## 4. Acceptance criteria (amended; supersedes original § 4)

| # | Criterion | How validated |
|---|---|---|
| 1 | Rune anchors render per Matt visual register spec (large + atmospheric behind primitive cluster + light-edge brush-stroke + no color + drawn by light only) | Visual inspection at Vercel preview; gandalf design review at preview milestone |
| 2 | `Anchor: [nebula / rune]` toggle operational OR rune render replaces nebula (drax discretion at close report) | Vercel preview toggle (if both retained) OR rune-only render (if drax surfaces nebula retirement rationale) |
| 3 | 6 primitive groups operational (drax-discretion-substitutable per § 1.2) | Code review + close report names final groups + per-group rune + reasoning |
| 4 | All 6 group runes have semantic-match-per-group reasoning documented (cross-system selection permitted per locked pattern) | Drax close report names per-group rune + system + semantic-justification; gandalf reviews semantic match |
| 5 | Tier 1 rune-selection mechanism functional (tap OR gesture OR both per drax choice) | Selecting rune commits to primitive group; Tier 2 UI activates |
| 6 | Tier 2 per-primitive selection UI shell operational for at least 2-3 groups (priority: Elements + Movement minimum) | Per-primitive selection within selected group functional; placeholder icons in place; selection state visible |
| 7 | Phase 3 baselines preserved (lasso + algo toggle + buffer + mobile + force-directed alternative) | Phase 3 acceptance criteria all still PASS |
| 8 | Mobile-responsive at iPad-class viewport with Tier 1 + Tier 2 | Test on iPad or browser-DevTools touch emulation |
| 9 | 60 FPS at 2D web rendering layer (preserved from Phase 3) | Browser performance profiler at Vercel preview |
| 10 | No raw LLM player-facing content (D7 AI-tell line) | Code review; rune library + placeholder icons are hand-curated; no runtime LLM |
| 11 | `classifyLasso()` scaffold thresholds re-validated against rune-anchor geometry per Phase 3 YELLOW Observation 3 — **priority elevated** vs Phase 3 YELLOW 3 framing because the rune's "large + atmospheric behind primitive cluster" diffuse spatial footprint (§ 1.1) is architecturally different from Phase 3's bounded-canvas nebula; the 4 hardcoded scaffold constants (`within_anchor_centroid_threshold=1100`, `nearby_anchor_threshold=1200`, `cross_buffer_min_lasso_radius=600`, `min_lasso_polygon_points=2`) were calibrated against Phase 3 nebula geometry, not atmospheric diffuse rune | Drax documents rune bounding box (or atmospheric-footprint extent if not bounded) for each of the 6 group runes at Phase 4.1 deployment milestone, BEFORE Phase 4.2 fires; confirms `classifyLasso()` thresholds still produce semantic modes correctly across all 6 rune geometries; surfaces threshold drift in Phase 4 close report if any constant requires recalibration |
| 12 | Tier 2 placeholder icons FLAGGED as pending canonical design Pattern B (per Discipline #40 scaffold-with-pending-decision) | Code review: PLACEHOLDER comments in code; close report surfaces icon list for Pattern B agenda |

---

## 4.5 Quality criterion (amended)

**Game-quality goal this dispatch serves:** Players experience the **rune-as-primitive-group-anchor** as load-bearing player-agency moment — the large atmospheric rune (light-edge brush-stroke; drawn by light) communicates "this is a meaningful sign" categorically distinct from "this is a kit cluster"; selecting a rune commits the player to a primitive group (Tier 1); within the rune, simple symbol icons let the player compose per-primitive values intuitively (Tier 2); the two-tier composition makes the player feel they are **assembling a spirit from foundational categories** rather than picking from a flat list. The Tal Rasha tomb sigil precedent translates from Diablo 2 atmosphere into Reincarnated mechanics — runes are the elder vocabulary; icons are the player's instrument. Absent this, Branch A architecture degenerates into either a flat icon menu (loses mythic weight) or a single-tier glyph-tap (loses compositional depth that two-tier provides).

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X (e.g., Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 — Branch A; Earth-Avatar Creation Moment Architecture § 2.4 dual-creation; atomic-substrate-registry 2026-06-06; cosmograph-pivot 2026-06-05 § 9)
- Alternative execution Y serves the named quality goal better (e.g., single-tier glyph-tap with no Tier 2 selection; per-primitive runes after all without grouping; flat icon grid without rune framing)
- Acceptance criteria can pass without advancing the quality goal (e.g., runes render + Tier 1 works + Tier 2 shows icons, yet players cannot intuit "rune = primitive group anchor; icons within = per-primitive selection" as the architectural pattern; visual register fails to carry meaning)
- Dispatch framing pre-commits to a decision Matt has not ratified (canonical primitive-group lock; canonical rune-per-group lock; canonical per-primitive icon lock — these are scaffold-with-pending-decision per #40)
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate — § 1.2 6-group scaffold framing — see § 5.2 Discipline #41 rationale)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40 candidate — e.g., group cardinality count; rune-per-group canonical choice; per-primitive icon canonical design)
- **Phase-4-amended-specific:** Phase 4 amendment results do NOT inform canonical Branch A commitment because two-tier complexity at 2D web is structurally insufficient to be predictive of iPad UE-port ergonomic; surface if Phase 4 cannot validate enough of the rune-per-group + two-tier pattern (e.g., requires deeper UE-port validation). **Falsifiable floor:** at minimum, Tier 1 rune-selection must function operationally for all 6 groups (rune-anchor visual register coherent across all 6 even if Tier 2 implementation only covers 2-3 priority groups). If Tier 1 fails at any group, the rune-per-group architectural pattern is structurally unvalidated at the 2D web layer regardless of Tier 2 completion. If Tier 2 cannot achieve coherent per-primitive selection in at least the 2 priority groups (Elements + Movement minimum per criterion 6), the two-tier compositional intent is structurally unvalidated. Additionally, if Tier 1 selection mechanism is tap-only alpha (gesture-draw Option β never prototyped under any group), surface this refutation condition — sign-as-input architectural intent from Tal Rasha recognition is under-validated for canonical Branch A commitment.

---

## 5. Discipline citations (amended; composes with original § 5)

### 5.1 Discipline #18 + #18.2 (math hotspot + methodology consultation timing)
**Tier 1 gesture-recognition algorithm** (if drax implements Option β or γ) IS a math hotspot at the implementation layer. Per Discipline #18.2 refinement: methodology consultation fires AFTER baseline at extension hotspots. Phase 4 amendment prototype tries reasonable algorithm empirically AS the baseline; elrond formal methodology consultation fires post-Phase-4 if pain surfaces. Phase 3 carry-forward hotspots remain queued — not in Phase 4 amendment scope.

### 5.2 Discipline #41 (pre-authored taxonomy interrogation)
**Primitive-group selection** is NOT canonically locked. § 1.2 6-group scaffold is starting candidate (drax-discretion-substitutable). **Per-primitive icon selection** is explicitly DEFERRED to Pattern B session per Matt verbatim. Canonical primitive-group lock + canonical rune-per-group lock + canonical per-primitive icon lock all DEFERRED to Pattern B with Matt post-Phase-4. Substrate-led discipline preserved at all three layers.

**Substrate-emergence-insufficiency rationale (per Phase 3 dispatch Gate-1 WARN-3 pattern):** primitive-group emergence from substrate analysis would require (a) canonical primitive-curation pass (which 12-20 of 20 primitive families per atomic-substrate-registry 2026-06-06 become canonical) PLUS (b) post-Hotspot-A substrate-vector-grouping methodology (e.g., UMAP+labeling at substrate-vector layer) — both downstream of Phase 4 timing. Canonical primitive-curation is explicitly DEFERRED to Pattern B with Matt post-cosmograph; substrate-vector-grouping methodology is Hotspot B timing per Elrond Hotspot A forward-compat note (post-Branch-A/B-call; Branch A now selected, so Hotspot B becomes post-Phase-4-amended-GREEN). Phase 4 prototype TESTS the rune-per-group + two-tier architectural pattern with a pre-offered 6-group scaffold; the canonical group-lock question remains substrate-led-resolved at the appropriate downstream layer. Matt's verbatim refinement examples (water drop / lightning bolt for Elements; jumping man / teleport man for Movement) land naturally in the 6-group taxonomy, indicating the scaffold is substrate-adjacent at the player-surface layer even though canonical lock cannot fire pre-Phase-4. Drax close-report subset-bias observation (per § 8 deliverable) surfaces whether the chosen 6-group structure materially shaped architectural-pattern findings — alternation hypothesis input to canonical Pattern B.

### 5.3 Discipline #25 (semantic-layer rep-audit)
**Per-rune semantic match per group audit** is load-bearing. gandalf reviews at Vercel preview milestones whether each rune's embedded semantic content actually matches the primitive group's symbolic role. Cross-system rune selection only works if semantic-layer rep-audit validates each selection.

### 5.4 Discipline #40 (scaffold-with-pending-decision)
Multiple scaffold values flagged in Phase 4 amendment:
- § 1.2 primitive-group scaffold (6 groups; drax can substitute; canonical group lock deferred)
- § 1.2 per-group rune candidates (cross-system; drax can substitute; canonical rune lock deferred)
- § 1.3 Tier 1 selection mechanism (tap / gesture / both; drax discretion)
- § 1.3 Tier 2 placeholder icons (canonical icon design DEFERRED Pattern B session)
- § 2.3 placeholder icon library sources (Lucide / Heroicons / SVG; drax discretion)
- § 1.1 + § 2.2 `visual_render_spec` render parameter values (brush-stroke weight, light-edge intensity, atmospheric diffusion parameters, monochromatic-light luminosity; drax picks reasonable defaults at Phase 4.1; § 1.1 visual register spec is Matt's design direction NOT canonical lock on render parameters; canonical visual-register render-parameter lock DEFERRED to Pattern B post-Phase-4 — composes with WS2 Niagara VFX UE-port scope authoring per § 9 trigger)
All flagged per Phase 4 close report.

### 5.5 D7 (AI-tell line; no raw LLM player-facing content)
Phase 4 amendment rune library + placeholder icon library are hand-curated substrate from public-domain sources. No runtime LLM. Tier 1 gesture-recognition (if implemented) is algorithmic; not LLM-based.

### 5.6 D8 (mobile-friendly-from-day-one)
Phase 4 amendment mobile-responsive validation per § 3.4. iPad-class viewport + touch-input ergonomics required. Composition with Earth-Avatar Creation Moment Architecture iPad gesture-framing. Tier 2 UI must be touch-friendly at iPad resolution.

### 5.7 Recognition-validate-commit (gandalf OP § 3.4 + 4.1)
Phase 4 amendment IS empirical validation of the rune-per-group + two-tier Branch A architecture refinement. Recognition captured (Matt 2026-06-09 verbatim refinement); empirical validation in flight; canonical commitment fires post-Phase-4 GREEN.

### 5.8 Tal Rasha recognition record § 4 commitments
Per recognition record § 4 Trigger 2 (Matt architectural-decision call selects Branch A — empirically confirmed via Legolas N=423 + corroborated by Elrond Hotspot A):
- § 4.1 Canonical amendment to cosmograph-pivot § 9 (gandalf-seam; post-Phase-4-amended-GREEN)
- § 4.2 Canonical addendum to Earth-Avatar Creation Moment Architecture (gandalf-seam; post-Phase-4-amended-GREEN; absorbs rune-per-group + two-tier + sign-overloading refinement)
- § 4.3 Legolas Mode A follow-on commission (DEFERRED unless Phase 4 amended surfaces rune substrate gaps)
- § 4.4 Drax /forge Phase 4 = THIS AMENDED COMMISSION (fires now per Matt 2026-06-09 direction)
- § 4.5 WS2 commission scope expansion (gandalf-seam; downstream; absorbs rune-per-group architecture)

---

## 6. What Phase 4 amendment does NOT include (preserved from original; explicit)

- ❌ Kit-binds-1:1-to-star-sign architecture (separate engine-side workstream)
- ❌ Zodiac-anchor constellation overlay layer (downstream of kit-to-star-sign)
- ❌ Legolas Mode A archaic-rune-corpus crawl (deferred unless Phase 4 surfaces unmet needs)
- ❌ Canonical primitive-group lock (Pattern B post-Phase-4)
- ❌ Canonical rune-per-group lock (Pattern B post-Phase-4)
- ❌ **Canonical per-primitive icon design lock** (explicit Pattern B per Matt 2026-06-09 verbatim "we will have to have a design session around these at some later date")
- ❌ Spherical-shell celestial-sphere geometry (UE-port scope)
- ❌ Volumetric nebula 3D context (UE-port scope)
- ❌ Niagara VFX rendering (UE-port scope)
- ❌ AAA fidelity visual register (UE-port scope)
- ❌ Earth avatar + grassy knoll + spirit form context (UE-port scope)
- ❌ Path I (drop-ingredients) full creation mechanism (UE-port scope; Phase 4 Tier 2 selection is precursor pattern, not full Path I)
- ❌ LLM-generated player-facing content (D7)

---

## 7. Composition with prior work (amended composition table)

| Prior work | Composition |
|---|---|
| Phase 4 ORIGINAL (`638a61e`) | This amendment SUPERSEDES per-primitive anchor scope; preserves cross-language pattern + drax-in-seam discipline + Phase 3 baseline preservation + discipline citations + out-of-scope items |
| `/forge Phase 3 GREEN` | Phase 4 amendment EXTENDS — preserves all Phase 3 baselines; adds rune-anchor + two-tier selection |
| `2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` | Branch A confirmed; Phase 4 amendment IS the refined player-surface empirical validation; rune-per-group + two-tier is the architectural refinement Matt directed; canonical commitments fire post-Phase-4-amended-GREEN |
| Legolas zodiac-substrate-corpus (N=423) | Branch A architectural-decision empirically triggered; the 423-entry zodiac corpus is for kit-to-star-sign workstream (separate; NOT Phase 4 scope) |
| `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.4 | Tier 2 per-primitive selection is precursor pattern for Path I (drop-ingredients) full creation mechanism; UE port productionizes |
| `2026-06-06-atomic-substrate-registry.md` | Phase 4 amendment uses 6 primitive groups as scaffold; canonical primitive-group lock deferred to Pattern B with Matt post-Phase-4-amended |
| Phase 3 close report YELLOW Observation 3 | Phase 4 amendment § 5.3 re-validates against rune-anchor geometry |
| Phase 3 close report methodology hotspots | Carry-forward; not in Phase 4 amendment scope; elrond consultation queued |
| Elrond Hotspot A consultation (substrate-vector proximity metric; force-directed validation; element-family-layer substrate-proximity preservation +13pp kNN purity@5) | Phase 4 amendment ships force-directed as production default per drax seam discretion + Elrond recommendation. YELLOW 2 (physical corpus dominance) retracted by Matt 2026-06-09 as ARPG genre-correct (~40-55% physical range per established genre-historical research); no corpus-rebalance commission fires; Elrond's force-directed recommendation stands as production default independent of corpus-rebalance question. |

---

## 8. Deliverables (amended)

1. **Vercel preview deployment** at each sub-phase milestone (4.1 → 4.5)
2. **Phase 4 amended close report** at `agentic_orchestration/drax/notes/2026-06-XX-forge-phase-4-amended-close-report.md` (date per actual close) including:
   - Per-acceptance-criterion verdict
   - Final primitive-group structure (6 or substituted)
   - Final rune-per-group assignments + cross-system reasoning per group
   - Tier 1 selection mechanism choice + tradeoffs (tap / gesture / both)
   - Tier 2 UI design observations
   - Tier 2 placeholder icon list (surface for Pattern B canonical design session)
   - Visual register A/B observations (nebula vs rune; or rune-only justification)
   - `classifyLasso()` re-validation outcome against rune-anchor geometry
   - Methodology hotspots flagged for elrond consultation per #18.2 (carry-forward Phase 3 + new Phase 4)
   - Phase 4 amended GREEN / YELLOW / RED verdict
   - Gap notes for UE-port scope
   - **Subset-bias observation:** did the chosen 6-group structure (or substituted count) materially shape architectural-pattern findings? If yes, surface alternation hypothesis for canonical primitive-group Pattern B input.
3. **Code changes** in `reincarnated-loadout/` per drax seam; auto-commit per CLAUDE.md addendum

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt verbatim refinement directive — "instead of one rune per primitive, let's make it one rune per primitive group. The rune sign should loom largely in the space behind the primitive cluster, with a glowing light highlighting the edges of the rune and without any color except having the brush strokes drawn by light. Upon selection of the rune, they player will be able to make changes/selections on the tablet... We will have to have a design session around these at some later date."

**Authority:** gandalf cross-cutting design-steward amendment authority for player-surface Branch A empirical validation workstream refinement + composition with Tal Rasha recognition record § 4 architectural commitments.

**Routing:** drax executes per amended commission + drax-discretion within bounded scaffolding; per-sub-phase Vercel preview deployments for gandalf semantic-review + Matt architectural-feedback; Phase 4 amended close report routes to gandalf for design review + Matt for canonical Branch A commitment direction + per-primitive icon Pattern B agenda population.

**Empirical-evidence triggers (refined):**
- Phase 4 amended close report GREEN → canonical Branch A commitment per Tal Rasha record § 4.1 + § 4.2 fires (gandalf canonical amendments — absorbs rune-per-group + two-tier + sign-overloading)
- Phase 4 amended close report surfaces methodology hotspots → elrond methodology consultation per Discipline #18.2 (fires post-baseline)
- Phase 4 amended close report Tier 2 placeholder icon list → per-primitive icon canonical design Pattern B session activates (Matt + gandalf)
- Phase 4 amended visual register + selection model findings → WS2 (Niagara VFX) UE-port commission scope authoring (absorbs rune-per-group + atmospheric light-edge brush-stroke render)
- Phase 4 amended mobile + touch findings → Earth-Avatar Creation Moment Architecture iPad gesture-framing refinement

**Composition with prior canonical commitments:** all preserved (Earth-Avatar Creation Moment Architecture 2026-06-07 + federated PC team architecture 2026-06-07 + atomic-substrate-registry 2026-06-06 + hypothesis-flow 2026-06-06 CANONICAL + cosmograph-pivot 2026-06-05 + Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 + Legolas zodiac-substrate-corpus 2026-06-09 N=423 complete + Elrond Hotspot A consultation 2026-06-09 + Phase 3 close GREEN with three YELLOWs and two methodology hotspots).

**End of amendment.**
