# Drax /forge Phase 4 Commission — Substrate-Led Glyph-Anchor Prototype (Branch A Empirical Validation)

**STATUS:** ACTIVE (commission ready to fire)
**Date authored:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — "select that as the pattern and drax delivers in seam" + "Let's go ahead now" + Legolas zodiac-substrate-corpus N=423 ≥ ~400 empirically confirms Branch A architectural viability
**Mode:** Mode L (loadout React/Vite/Tailwind/Vercel; /forge sub-route extension; Phase 4 ADDS to Phase 3 GREEN baseline)
**Audience:** drax (executor), gandalf (design-review consumer at Vercel preview milestones), Matt (architectural feedback)
**Companion docs (read first):**
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md` (Phase 3 close GREEN; per-criterion verdicts; YELLOW observations; methodology hotspots)
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md` (drax Phase 3 close report — full)
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/synthesis.md` (Legolas zodiac corpus complete; N=423; Branch A confirmed)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A architectural recognition; Tier-1 commitments per § 4 fire post-confirmation — THIS COMMISSION OPERATIONALIZES Branch A)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.4 (dual-creation Path L + Path I; sign-as-input gesture context)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (20 primitive families; canonical-7+1 element catalog as Phase 3+4 anchor framing)
- `agentic_orchestration/gandalf/notes/2026-06-09-next-session-plan-zodiac-cosmograph-design.md` (Matt 2026-06-08 buffer-space + 2026-06-09 substrate-led pivot dialogue)

---

## 0. TL;DR

**Mission:** Extend /forge Phase 3 GREEN baseline (currently deployed at `https://reincarnated-loadout-bvy27r3hf-matthew-wetmore-s-projects.vercel.app`) with **substrate-led glyph-anchor implementation** for the primitive layer per Matt 2026-06-09 locked pattern. Phase 4 is the empirical validation of Branch A architecture (Tal Rasha recognition record § 4 commitments fire here).

**Empirical trigger:** Legolas zodiac-substrate-corpus commission COMPLETE at N=423 ≥ ~400 (even excluding all 16 high-sensitivity entries leaves 407 — still clears). Branch A architecture is viable per substrate-evidence.

**Locked pattern (Matt 2026-06-09 verbatim):**
1. Surface primitive clusters first (the 8 element-family anchors from Phase 3 are the starting set; primitive-curation refinement deferred)
2. Cross-language glyph selection (generic glyph systems; per-meaning match across cuneiform, Norse runes, I Ching trigrams, enochian, similar draw-able systems)
3. Per-primitive best-meaning-match (substrate-led; semantic content votes; not pre-imposed)
4. Draw-ability as sub-criterion filter (angular + stroke-primitive + small-alphabet; touch-input friendly)
5. Drax delivers in-seam with gandalf review at Vercel preview milestones

**Phase 4 SCOPE:**
- Glyph-anchor visual register for the 8 primitive (element-family) anchors — figurative nebulas (Phase 3 baseline) preserved as A/B toggle; glyph anchors as B
- Per-primitive cross-language glyph selection per locked pattern (drax-discretion within bounded glyph candidates per § 2.2)
- Sign-as-input gesture prototype — player traces glyph to select primitive (touch + mouse; iPad gesture-framing per Earth-Avatar canonical)
- Composition with Phase 3 buffer-space + lasso ergonomics + force-directed alternative positioning + mobile-responsive layout (preserved)
- Address Phase 3 YELLOW Observation 3 (`classifyLasso()` scaffold thresholds re-validated against glyph-anchor geometry)

**Phase 4 OUT OF SCOPE (explicitly deferred):**
- Kit-binds-1:1-to-star-sign architecture (separate workstream; engine-side substrate work via gandalf design-spec-as-math handoff to elrond/rocket; NOT drax-implementable solo; Phase 4 prepares architectural placeholders only)
- Zodiac-anchor implementation as constellation overlay layer (the 423-entry zodiac corpus integration is downstream of kit-to-star-sign assignment; not Phase 4)
- Legolas Mode A archaic-glyph-corpus crawl (drax uses well-documented public-domain glyph systems for Phase 4; deeper Legolas Mode A crawl deferred unless Phase 4 surfaces unmet glyph substrate needs)
- Canonical primitive-curation lock (which 12-20 of 20 primitives become visible — deferred to Pattern B with Matt post-Phase-4)
- Spherical-shell celestial-sphere geometry (UE-port scope; WS2 commission)
- AAA fidelity visual register (UE-port scope)
- Earth avatar + grassy knoll + spirit form context (UE-port scope)

**Substrate consumed:** existing /forge Phase 3 baseline (37-kit corpus + 8 element anchors + 1000-kit substrate-trace) + drax-curated glyph subset from public-domain glyph systems per § 2.2.

**Estimated wall-clock:** 1-3 wall-clock days per drax convention; deployable to Vercel preview at each sub-phase milestone.

**Critical constraint:** Phase 4 is **empirical validation of Branch A architecture pattern**. Per recognition-validate-commit discipline + Phase 3 precedent, validate the pattern empirically; canonical commitment fires post-Phase-4 GREEN.

---

## 1. Architectural pattern to validate

### 1.1 Glyph-anchor visual register

**The shift from Phase 3:** Phase 3 rendered primitive-anchors as figurative nebulas (Layer 1 — substantial cloud structures with 5-ring gradient). Phase 4 adds **glyph-anchor visual register** as alternative Layer 1 rendering — abstract-symbolic glyphs floating in the cosmograph, visually distinct from both figurative nebulas AND kit-cluster dots/stars.

**Visual register requirements:**
- **Abstract-symbolic** (NOT figurative — no lions / dragons / human figures; geometric stroke compositions only)
- **Distinctly readable** (player recognizes glyph shape without explanation; categorical "this is a sign, not a constellation")
- **Mythic / elder vocabulary tone** (ancient-feeling; Diablo 2 Tal Rasha tomb sigil precedent as visual register anchor)
- **Bounded canvas** (each glyph occupies bounded region of cosmograph; not diffuse like nebula)
- **Render at multiple zoom levels** (readable at 1× cosmograph zoom; details emerge at 2×+; per Phase 3 LOD pattern)

**Composition with figurative-nebula baseline:** Add `Anchor: [nebula / glyph]` toggle to Forge.tsx (paralleling Phase 3's `Algo: [radial / force]` toggle). Same architectural pattern; different anchor render. Lets Matt A/B compare at Vercel preview.

### 1.2 Per-primitive cross-language glyph selection

**The mapping methodology (Matt 2026-06-09 substrate-led pivot):**
1. **Primitive clusters surface first** (Phase 4 inherits Phase 3's 8 element-family anchors as the starting set — fire / water / earth / wind / lightning / holy / shadow / physical)
2. **Each primitive's semantic-content brief** (element + symbolic-role + mythic-associations) drives glyph selection
3. **Search the glyph corpus for high-meaning-match candidates** across multiple glyph systems
4. **Apply draw-ability filter** (legibility / stroke-count / touch-input-friendliness)
5. **Pick best-fit per primitive — cross-system selection permitted** (one primitive might pull from Norse runes, another from I Ching trigrams, another from cuneiform)

### 1.3 Drax-discretion glyph-candidate subset (scaffold-with-pending-decision per Discipline #40)

**Pre-offered glyph candidates per primitive (drax-discretion; not canonical):**

| Primitive | Cuneiform | Norse Rune | I Ching trigram | Cross-system best-meaning lean (gandalf-pre-pondered; drax can substitute) |
|---|---|---|---|---|
| **Fire** | NE / IZI (fire) | Kenaz ᚲ (torch / fire-light) | Lí ☲ (fire / clarity) | **I Ching Lí ☲** — pure 3-stroke composition; "fire/clarity" semantic; extremely draw-able |
| **Water** | A (water) | Laguz ᛚ (water / lake) | Kǎn ☵ (water / abyss) | **I Ching Kǎn ☵** — pure 3-stroke composition; "water" semantic; extremely draw-able |
| **Earth** | KUR (mountain / land) | Berkana ᛒ (birch / earth-fertility); Jera ᛃ (year / harvest) | Kūn ☷ (earth / receptive); Gèn ☶ (mountain / stillness) | **I Ching Kūn ☷** — pure 3-stroke composition; "earth/receptive" semantic |
| **Wind** | IM (wind / storm) | Ansuz ᚨ (god / breath); Raidho ᚱ (riding / journey) | Xùn ☴ (wind / gentle / penetrating) | **I Ching Xùn ☴** — pure 3-stroke composition; "wind/penetrating" semantic |
| **Lightning** | NIMGIR (lightning) | Sowilo ᛋ (sun-lightning); Thurisaz ᚦ (Thor's hammer / storm) | Zhèn ☳ (thunder / arousing) | **I Ching Zhèn ☳** — pure 3-stroke composition; "thunder/arousing" semantic |
| **Holy** | DINGIR (god / divine) | Ansuz ᚨ (god); Tiwaz ᛏ (Tyr / sky-god / justice) | Qián ☰ (heaven / creative) | **I Ching Qián ☰** — pure 3-stroke composition; "heaven/creative" semantic |
| **Shadow** | EREŠ (underworld); LIL (spirit) | Eihwaz ᛇ (yew / death-passage); Hagalaz ᚺ (hail / disruption); Isa ᛁ (ice / stillness) | Duì ☱ (lake / depths); Gèn ☶ (mountain / stillness) | **Norse Eihwaz ᛇ** — 2-stroke composition; "death-passage / threshold" semantic; very draw-able; depth-and-passage feel matches shadow archetype better than I Ching alternatives |
| **Physical** | LU (man); GIŠ.TUKUL (weapon); GUD (bull / aurochs) | Uruz ᚢ (aurochs / raw-strength); Algiz ᛉ (defense / elk-protection) | Gèn ☶ (mountain / stability) | **Norse Uruz ᚢ** — 2-stroke composition; "raw strength / wild aurochs" semantic; very draw-able; primordial-physicality feel matches physical archetype |

**Observation:** the canonical-7+1 element catalog maps remarkably cleanly to I Ching's 8 trigrams (fire/water/earth/wind/thunder/heaven/lake/mountain). If drax adopts I Ching for the 6 elements that match cleanly + Norse runes for shadow + physical (where I Ching has weaker semantic match), the **cross-system selection lands at exactly the right semantic-richness per primitive**. This is substrate-led discipline operating at the mapping layer — the data votes for cross-system selection naturally.

**Drax discretion:** the pre-offered candidates are NOT canonical proposals; they are starting scaffold per Discipline #40 (scaffold-with-pending-decision). Drax can substitute alternatives per better semantic match OR draw-ability OR visual coherence at preview. The Phase 4 close report surfaces final glyph-per-primitive selection + reasoning. gandalf reviews semantic matches at Vercel preview milestones.

### 1.4 Sign-as-input gesture prototype

**The architectural payoff of Branch A** — the "sign" semantic overloading (sign-as-noun-celestial / sign-as-verb-input / sign-as-signature / sign-as-The-Sign) only lands if player can **draw / trace the glyph** as input gesture. Phase 4 prototypes this at /forge:

**Gesture model:**
- Player draws/traces glyph shape with finger (touch) or cursor (mouse) on cosmograph canvas
- Gesture-recognition: matches drawn-stroke pattern against glyph library
- Match → selects corresponding primitive cluster (equivalent semantic to within-anchor lasso, but via sign-gesture not spatial-selection)
- Visual feedback: drawn strokes render as fading glyph trace; on match, glyph briefly highlights + selected cluster pulses

**Bounded scope for Phase 4:**
- 8 glyphs total to recognize (one per primitive — per § 1.3)
- Tolerance-based matching (not strict shape-recognition; reasonable proximity to canonical glyph shape passes)
- Toggle: `Input: [lasso / sign]` — preserves Phase 3 lasso baseline + adds sign-gesture as alternative
- Drax-discretion on matching algorithm (e.g., $1 Recognizer / $P Recognizer family / template-matching with stroke-direction tolerance — well-documented public-domain algorithms suitable for finger-input)

**What Phase 4 sign-gesture does NOT validate (defers to UE port):**
- Sub-glyph precision (full match-against-200+-glyph corpus; Branch A canonical implementation)
- Gesture-stroke visual fidelity at AAA quality
- Multi-touch / pen-pressure / haptic feedback
- Composition with Path I (drop-ingredients) full creation mechanism (Earth-Avatar canonical § 2.4 — UE-port scope)

### 1.5 Composition with Phase 3 (preserved baselines)

Phase 4 PRESERVES all Phase 3 GREEN-validated patterns:
- Two-layer + buffer-space spatial architecture (anchors + kit clusters; deliberate buffer)
- Force-directed alternative positioning (Algo toggle remains operational)
- Mobile-responsive layout (flex-col / flex-row; touch pinch-zoom; D8)
- Lasso ergonomics within-anchor / cross-buffer / buffer-only (preserved; works with both nebula and glyph anchor renders)
- 8 element-family anchors as starting set
- 60 FPS performance target at 2D web rendering

Phase 4 ADDS:
- `Anchor: [nebula / glyph]` toggle for anchor visual register
- `Input: [lasso / sign]` toggle for input model
- Glyph-recognition module + glyph library
- Composition: nebula + lasso (Phase 3 baseline) / glyph + lasso (visual register only) / glyph + sign (full Branch A pattern) / nebula + sign (cross-toggle exploration)

---

## 2. Substrate consumption

### 2.1 Existing /forge Phase 3 baseline (inherited)
- 37-kit corpus + 1000-kit substrate-trace
- 8 element-family anchors (4×2 grid, SPACING_X=2750px, SPACING_Y=5700px)
- Force-directed alternative positioning algorithm
- Lasso classification module (`classifyLasso()` — scaffold thresholds re-validation per § 5.3)
- Buffer-space content (310 hybrid kits)
- Mobile-responsive layout

### 2.2 Glyph subset (drax-curated from public-domain glyph systems)
Per § 1.3 above — drax-discretion within candidate set. Source authority for each glyph:
- **I Ching trigrams (8 trigrams)** — Wilhelm/Baynes *I Ching* translation (Princeton Bollingen) + Wikipedia Bagua + I Ching primary sources; public domain; native Unicode characters ☰☱☲☳☴☵☶☷
- **Norse Elder Futhark runes (24 runes)** — Wikipedia Elder Futhark + academic Norse studies; public domain; native Unicode characters ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ
- **Cuneiform (selected signs)** — Wikipedia + CDLI (Cuneiform Digital Library Initiative); public domain; Unicode Cuneiform block 𒀀–𒎙
- **Enochian (optional supplement)** — Wikipedia Enochian + Dee/Kelley manuscripts; public domain; not in Unicode (would require font / SVG rendering)
- **Cross-language selection authority:** gandalf design-spec; drax-discretion on per-glyph choice within bounded candidates; gandalf review at Vercel preview milestones validates semantic match

### 2.3 Glyph library data structure (drax-implementable)
- Per-glyph: `{ id, system, native_char, semantic_meaning, primitive_assignment, canonical_stroke_pattern, draw_difficulty }`
- canonical_stroke_pattern as ordered stroke data (start_point, end_point, stroke_curvature) for gesture-matching algorithm
- semantic_meaning as text field (e.g., "fire / clarity / illumination") for gandalf review + future cohesion-judge consumption

---

## 3. Phase 4 sub-phase structure

### Phase 4.1 — Glyph anchor visual register (no input model change yet)
- Implement `Anchor: [nebula / glyph]` toggle
- Glyph render at primitive-anchor positions (preserves Phase 3 grid + force-directed positioning)
- 8 glyph assignments per § 1.3 (drax-discretion within candidates)
- Glyph render: distinct visual register (abstract-symbolic; readable at 1× + 2×+ zoom)
- Preserve all Phase 3 functionality (lasso + algo toggle + mobile + buffer)
- Deploy to Vercel preview
- **Acceptance:** glyph anchors render categorically distinct from kit clusters; toggle switches between nebula + glyph; Phase 3 baselines preserved

### Phase 4.2 — Sign-as-input gesture prototype
- Implement `Input: [lasso / sign]` toggle
- Gesture-recognition module for 8 glyphs (drax-discretion on algorithm; tolerance-based matching)
- Visual feedback: stroke trace + match highlight + cluster pulse
- Touch + mouse input both supported
- Deploy to Vercel preview
- **Acceptance:** drawing a glyph successfully selects corresponding primitive cluster; tolerance reasonable for finger-input; gesture works on iPad-class viewport

### Phase 4.3 — Gandalf semantic-match review at Vercel preview
- Drax surfaces glyph-per-primitive assignments + reasoning
- gandalf reviews semantic match per primitive (Discipline #25 semantic-layer rep-audit)
- Iterate per gandalf feedback (substitute glyphs / refine matching tolerance / adjust visual register)
- Re-deploy
- **Acceptance:** gandalf design-review PASS at semantic match layer

### Phase 4.4 — Mobile + touch ergonomics re-validation
- Verify glyph anchors readable at iPad-class viewport (375px width)
- Verify sign-gesture works on touch (no interference with pan / pinch / lasso)
- Verify mode-toggles operational on mobile
- **Acceptance:** Phase 3 mobile-responsiveness preserved; sign-gesture functional on touch

### Phase 4.5 — Phase 4 close report (drax → gandalf → Matt)
- Document findings per § 4 acceptance criteria
- Surface glyph-per-primitive final assignments + reasoning
- Surface gesture-recognition tradeoffs + tolerance choices
- Surface visual register A/B observations (nebula vs glyph)
- Surface input model A/B observations (lasso vs sign)
- Address Phase 3 YELLOW Observation 3 (`classifyLasso()` scaffold re-validation against glyph-anchor geometry)
- Flag methodology hotspots for elrond consultation per Discipline #18.2 (carry-forward + new)
- Phase 4 GREEN / YELLOW / RED verdict per /forge convention
- Deploy final version to Vercel preview for Matt review

---

## 4. Acceptance criteria

| # | Criterion | How validated |
|---|---|---|
| 1 | Glyph anchors render categorically distinct from kit clusters (abstract-symbolic visual register) | Visual inspection at Vercel preview; readable without explanation; not figurative |
| 2 | `Anchor: [nebula / glyph]` toggle operational; both render modes functional | Vercel preview toggle switches between renders |
| 3 | All 8 primitive-anchors have glyph assignments per cross-language best-meaning-match | Code review + drax close report names per-primitive glyph + system + semantic-justification |
| 4 | `Input: [lasso / sign]` toggle operational | Vercel preview toggle switches between input models |
| 5 | Sign-gesture recognition functional for all 8 glyphs (mouse + touch) | Drawing each glyph successfully selects corresponding primitive cluster |
| 6 | Gesture tolerance reasonable for finger-input (not strict shape-recognition) | Tested with imprecise finger strokes; reasonable match rate (>~80%); no false matches between distinct glyphs |
| 7 | Phase 3 baselines preserved (lasso + algo toggle + buffer + mobile) | Phase 3 acceptance criteria all still PASS |
| 8 | Mobile-responsive at iPad-class viewport with sign-gesture | Test on iPad or browser-DevTools touch emulation |
| 9 | 60 FPS at 2D web rendering layer (preserved from Phase 3) | Browser performance profiler at Vercel preview |
| 10 | No raw LLM player-facing content (D7 AI-tell line) | Code review; glyph library is hand-curated substrate; no runtime LLM |
| 11 | `classifyLasso()` scaffold thresholds re-validated against glyph-anchor geometry per Phase 3 YELLOW Observation 3 | Lasso classification still produces semantic modes correctly at glyph-anchor layout |
| 12 | Glyph library data structure includes semantic_meaning + primitive_assignment for each glyph | Code review of glyph library JSON / TS file |

---

## 4.5 Quality criterion

**Game-quality goal this dispatch serves:** Players experience the **sign-as-input gesture** as the load-bearing player-agency moment of Branch A architecture — drawing a glyph IS the act of committing to a primitive direction; the visual register distinction (figurative kit clusters vs abstract-symbolic glyph anchors) reads categorically without explanation; the "sign" semantic overloading lands ergonomically (sign-as-noun-celestial / sign-as-verb-input / sign-as-signature). The Tal Rasha tomb sigil precedent translates from Diablo 2 atmosphere into Reincarnated mechanics — players SIGN their build into existence. Absent this, Branch A architecture degenerates into "primitives are just differently-shaped anchors" — the architectural payoff (categorical visual register + load-bearing input gesture + semantic over-determination) does not land.

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X (e.g., Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 — Branch A; Earth-Avatar Creation Moment Architecture § 2.4 dual-creation paths; atomic-substrate-registry 2026-06-06; cosmograph-pivot 2026-06-05 § 9)
- Alternative execution Y serves the named quality goal better (e.g., glyphs render as figurative-iconography instead of abstract-symbolic; input gesture model is multi-touch instead of single-stroke trace; sign-as-input concept tested via different UI than glyph-trace)
- Acceptance criteria can pass without advancing the quality goal (e.g., glyphs render distinct + sign-gesture works + tolerance reasonable, yet players cannot intuit "draw the glyph to commit to a primitive direction" as a mechanic — the sign overloading fails to carry meaning ergonomically)
- Dispatch framing pre-commits to a decision Matt has not ratified (canonical primitive-curation lock; canonical glyph-per-primitive assignment; specific glyph-system canonical lock — these are scaffold-with-pending-decision per #40)
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate — § 1.3 glyph candidate framing — see § 5.2 Discipline #41 rationale)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40 candidate — e.g., gesture tolerance threshold; visual register specifics; glyph subset)
- **Phase-4-specific:** Phase 4 results do NOT inform canonical Branch A commitment because they are structurally insufficient — surface if Phase 4 cannot validate enough of the Branch A pattern (e.g., 2D web sign-gesture too constrained to be predictive of iPad UE-port full ergonomic; require deeper UE-port validation)

---

## 5. Discipline citations

### 5.1 Discipline #18 + #18.2 (math hotspot + methodology consultation timing)
**Gesture-recognition algorithm** IS a math hotspot at the implementation layer. Per Discipline #18.2 refinement: methodology consultation fires AFTER baseline at extension hotspots. Phase 4 prototype tries reasonable algorithm empirically AS the baseline; elrond formal methodology consultation fires post-Phase-4 if pain surfaces. Phase 3 carry-forward hotspots (Hotspot A substrate-vector proximity metric + Hotspot B UMAP vs force-directed at substrate-vector level) remain queued — not in Phase 4 scope.

### 5.2 Discipline #41 (pre-authored taxonomy interrogation)
**Glyph-system selection** is NOT pre-imposed — the locked pattern (Matt 2026-06-09) is substrate-led mapping: primitive semantics vote; glyphs serve meaning. § 1.3 pre-offered candidates are scaffold-with-pending-decision (#40); drax-discretion within bounded candidates; gandalf reviews semantic matches at Vercel previews; canonical glyph-per-primitive lock DEFERRED to Pattern B with Matt post-Phase-4. Deeper Legolas Mode A archaic-glyph-corpus crawl DEFERRED unless Phase 4 surfaces unmet glyph substrate needs.

### 5.3 Discipline #25 (semantic-layer rep-audit)
**Per-glyph semantic match audit** is load-bearing for Phase 4. gandalf reviews at Vercel preview milestones whether each glyph's embedded semantic content actually matches the primitive's symbolic role. Cross-system selection (cuneiform / runes / I Ching / enochian) only works if semantic-layer rep-audit validates each selection. Substrate (glyph corpus) votes; design surfaces (per-primitive assignment) audit at semantic layer.

### 5.4 Discipline #40 (scaffold-with-pending-decision)
Multiple scaffold values in Phase 4:
- § 1.3 per-primitive glyph candidates (drax can substitute; canonical lock deferred)
- § 1.4 gesture-recognition tolerance threshold (drax discretion; iterate per testing)
- § 1.4 8-glyph total recognition scope (matches Phase 3's 8-anchor framing; expands to 12+ post-canonical-primitive-curation)
- § 1.1 glyph visual register specifics (stroke width / color / canvas bounds; drax discretion within "abstract-symbolic" register)
All flagged as scaffold per drax close report.

### 5.5 D7 (AI-tell line; no raw LLM player-facing content)
Phase 4 glyph library is hand-curated substrate from public-domain glyph systems. No runtime LLM. Gesture-recognition is algorithmic (e.g., $1 Recognizer family — well-documented; not LLM-based).

### 5.6 D8 (mobile-friendly-from-day-one)
Phase 4 mobile-responsive validation per § 3.4. iPad-class viewport + touch-input gesture ergonomics required. Composition with Earth-Avatar Creation Moment Architecture iPad gesture-framing.

### 5.7 Recognition-validate-commit (gandalf OP § 3.4 + 4.1)
Phase 4 IS empirical validation of Branch A architecture pattern (Tal Rasha recognition record). Recognition captured 2026-06-09; Legolas empirical confirmation N=423 cleared substrate threshold; Phase 4 validates the player-facing pattern; canonical Branch A commitment fires post-Phase-4 GREEN with Matt-architectural-feedback.

### 5.8 Tal Rasha recognition record § 4 commitments fire
Per recognition record § 4 Trigger 2 (Matt architectural-decision call selects Branch A — empirically confirmed at Legolas N=423):
- § 4.1 Canonical amendment to cosmograph-pivot § 9 (gandalf-seam; post-Phase-4-GREEN)
- § 4.2 Canonical addendum to Earth-Avatar Creation Moment Architecture (gandalf-seam; post-Phase-4-GREEN)
- § 4.3 Legolas Mode A follow-on commission (DEFERRED unless Phase 4 surfaces glyph substrate gaps)
- § 4.4 Drax /forge Phase 4 = THIS COMMISSION (fires now per Matt 2026-06-09 directive)
- § 4.5 WS2 commission scope expansion (gandalf-seam; downstream)

---

## 6. What Phase 4 does NOT include (explicitly out of scope)

- ❌ Kit-binds-1:1-to-star-sign architecture implementation (separate workstream; engine-side substrate work via gandalf design-spec-as-math handoff to elrond/rocket; NOT drax-implementable solo)
- ❌ Zodiac-anchor constellation overlay layer (the 423-entry zodiac corpus integration is downstream of kit-to-star-sign assignment)
- ❌ Legolas Mode A archaic-glyph-corpus crawl (drax uses public-domain glyph systems; deeper crawl DEFERRED unless Phase 4 surfaces unmet needs)
- ❌ Canonical primitive-curation lock (which 12-20 of 20 primitives become canonical visible — deferred to Pattern B with Matt post-Phase-4)
- ❌ Canonical glyph-per-primitive lock (deferred to Pattern B with Matt post-Phase-4)
- ❌ Spherical-shell celestial-sphere geometry (UE-port scope; WS2 commission)
- ❌ Volumetric nebula 3D context (UE-port scope; WS2 commission)
- ❌ Niagara VFX rendering (UE-port scope; WS2 commission)
- ❌ AAA fidelity visual register (UE-port scope)
- ❌ Earth avatar + grassy knoll + spirit form context (UE-port scope)
- ❌ Path I (drop-ingredients) full creation mechanism (Earth-Avatar Creation Moment Architecture § 2.4 — UE-port scope; Phase 4 sign-gesture is a precursor pattern, not the full Path I)
- ❌ LLM-generated player-facing content (D7)
- ❌ Cross-cycle / scope-amendment commits without Matt-authorization (per CLAUDE.md addendum)

---

## 7. Composition with prior work

| Prior work | Composition |
|---|---|
| `/forge Phase 3 GREEN` (deployed Vercel) | Phase 4 EXTENDS — preserves all Phase 3 baselines (two-layer + buffer-space + lasso + algo toggle + mobile); adds glyph-anchor + sign-gesture as toggle layers |
| `2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` | Branch A confirmed empirically at Legolas N=423; Phase 4 IS the player-surface empirical validation per recognition-validate-commit; § 4 canonical commitments fire post-Phase-4 GREEN |
| Legolas zodiac-substrate-corpus (N=423) | Branch A architectural-decision empirically triggered; the 423-entry zodiac corpus is for kit-to-star-sign workstream (separate; NOT Phase 4 scope); Phase 4 validates the glyph-anchor primitive layer only |
| `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.4 | Phase 4 sign-as-input gesture is a precursor pattern for Path I (drop-ingredients) full creation mechanism; UE port productionizes |
| `2026-06-06-atomic-substrate-registry.md` | Phase 4 uses 8 element-family anchors (canonical-7+1) from Phase 3 baseline; canonical primitive-curation deferred to Pattern B with Matt post-Phase-4 |
| Phase 3 close report YELLOW Observation 3 (`classifyLasso()` scaffold) | Phase 4 § 5.3 re-validates against glyph-anchor geometry |
| Phase 3 close report methodology hotspots (substrate-vector proximity; UMAP comparison) | Carry-forward; not in Phase 4 scope; elrond consultation queued |
| `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` | WS2 commission inherits Phase 4 findings for Niagara glyph-anchor rendering scope authoring at UE-port phase |

---

## 8. Deliverables

1. **Vercel preview deployment** at each sub-phase milestone (4.1 → 4.5)
2. **Phase 4 close report** at `agentic_orchestration/drax/notes/2026-06-XX-forge-phase-4-close-report.md` (date per actual close) including:
   - Per-acceptance-criterion verdict
   - Final glyph-per-primitive assignments + cross-language reasoning per primitive
   - Gesture-recognition tradeoffs + algorithm choice + tolerance calibration
   - Visual register A/B observations (nebula vs glyph)
   - Input model A/B observations (lasso vs sign)
   - `classifyLasso()` re-validation outcome against glyph-anchor geometry
   - Methodology hotspots flagged for elrond consultation per #18.2 (carry-forward Phase 3 + new Phase 4)
   - Phase 4 GREEN / YELLOW / RED verdict
   - Gap notes for UE-port scope (sub-glyph precision; multi-touch; gesture-stroke visual fidelity; spherical-shell)
   - **Subset-bias observation:** did the chosen glyph subset (predominantly I Ching trigrams + 2 Norse runes per § 1.3 lean) materially shape architectural-pattern findings? If yes, surface alternation hypothesis for canonical glyph-per-primitive Pattern B input.
3. **Code changes** in `reincarnated-loadout/` per drax seam; auto-commit per CLAUDE.md addendum

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt directive ("select that as the pattern and drax delivers in seam" + "Let's go ahead now" + Legolas empirical confirmation N=423).

**Authority:** gandalf cross-cutting design-steward commission authority for player-surface Branch A empirical validation workstream + composition with Tal Rasha recognition record § 4 Trigger 2 architectural commitments.

**Routing:** drax executes per locked pattern + drax-discretion within bounded scaffolding; per-sub-phase Vercel preview deployments for gandalf semantic-review + Matt architectural-feedback; Phase 4 close report routes to gandalf for design review + Matt for canonical Branch A commitment direction.

**Empirical-evidence triggers:**
- Phase 4 close report GREEN → canonical Branch A commitment per Tal Rasha record § 4.1 + § 4.2 fires (gandalf canonical amendments)
- Phase 4 close report surfaces methodology hotspots → elrond methodology consultation per Discipline #18.2 (fires post-baseline)
- Phase 4 visual register + input model A/B findings → WS2 (Niagara VFX) UE-port commission scope authoring
- Phase 4 mobile + touch findings → Earth-Avatar Creation Moment Architecture iPad gesture-framing refinement
- Phase 4 surfaces glyph substrate gaps → Legolas Mode A archaic-glyph-corpus follow-on commission (per Tal Rasha record § 4.3; conditional)

**Composition with prior canonical commitments:** all preserved (Earth-Avatar Creation Moment Architecture 2026-06-07 + federated PC team architecture 2026-06-07 + atomic-substrate-registry 2026-06-06 + hypothesis-flow 2026-06-06 CANONICAL + cosmograph-pivot 2026-06-05 + Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 + Legolas zodiac-substrate-corpus 2026-06-09 N=423 complete).

**End of commission.**
