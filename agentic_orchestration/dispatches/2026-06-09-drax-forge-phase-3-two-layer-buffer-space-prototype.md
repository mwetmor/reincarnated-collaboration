# Drax /forge Phase 3 Commission — Two-Layer + Buffer-Space Cosmograph Prototype

**STATUS:** ACTIVE (commission ready to fire)
**Date authored:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — sequence Options 1+2 (Tal Rasha recognition record + drax /forge Phase 3 commission) per gandalf-lean recommendation; this commission is Option 2
**Mode:** Mode L (loadout React/Vite/Tailwind/Vercel; /forge sub-route extension)
**Audience:** drax (executor), gandalf (design-review consumer), Matt (preview review + architectural-decision feedback)
**Companion docs (read first):**
- `agentic_orchestration/dispatches/2026-06-07-drax-cosmograph-a-b-spike.md` (Phase 2 commission — predecessor; understand the existing /forge architecture before extending)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (foundational architecture this prototype prepares for)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 amendment 2026-06-06 (primitive-as-star + kit-as-constellation — Phase 3 refines visual relationship)
- `agentic_orchestration/gandalf/notes/2026-06-09-next-session-plan-zodiac-cosmograph-design.md` § 1.1 (two-layer + buffer-space architecture from 2026-06-08 mobile-Claude dialogue)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A glyphic-anchor architecture — DEFERRED; do NOT implement glyph-as-primitive-anchor in Phase 3; the Branch A vs Branch B decision is post-Legolas-zodiac-commission)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (20 primitive families; Phase 3 tests with curated subset)

---

## 0. TL;DR

**Mission:** Extend /forge cosmograph (currently Phase 2 GREEN; deployed at https://reincarnated-loadout.vercel.app/forge with constellation default + analyst toggle) with **two-layer + buffer-space spatial architecture** as cheap 2D web validation of the visualization pattern BEFORE UE port commits rendering resources.

**Validates:** positioning-algorithm choices + buffer-space tuning + lasso ergonomics across buffer boundaries + visual register distinction at 2D web rendering layer + rare-lineage discoverability in buffer space.

**Does NOT validate (deferred to UE):** spherical-shell celestial-sphere geometry, 3D nebula volumetric context, Niagara VFX, AAA fidelity, glyph-as-primitive-anchor (Branch A; gated on Legolas zodiac-substrate-corpus commission output).

**Substrate consumed:** current 37-kit corpus (existing /forge pipeline) + curated subset of 20 primitive families from atomic-substrate-registry as primitive-anchor test set + rare-lineage kit subset for buffer-space content.

**Estimated wall-clock:** 1-3 wall-clock days per drax convention; deployable to Vercel preview at each phase milestone.

**Critical constraint:** runs IN PARALLEL with Legolas zodiac-substrate-corpus background workstream. Does NOT block on zodiac substrate (Phase 3 tests architectural pattern with current substrate). Does NOT pre-commit Branch A or Branch B (architectural-decision call deferred to post-Legolas).

---

## 1. Architectural pattern to validate

### 1.1 Two-layer spatial architecture

**Layer 1 — Primitive-anchor layer.** Substantial nebula-like structures (or anchor-marker visual; primitive visual register is open design space for Phase 3) representing primitive families. Visually distinct from kit-clusters via SIZE + SHAPE + TONE + STRUCTURAL register. Each primitive-anchor is the "regional marker" identity ("this is the fire element cluster" / "this is the engagement cluster" / etc.).

**Layer 2 — Kit-cluster layer.** Smaller nebula-like structures representing individual kits. Kit-clusters are spatially proximate to their related primitive-anchors per substrate-vector proximity. Each kit-cluster carries the kit's identity (categorical labels, Q18 flavor identity, T4 selection, etc.).

### 1.2 Buffer-space architecture

**Deliberate empty-space buffer between primitive-anchor regions.** Buffer is NOT just empty negative space — it is **discoverable territory** that can hold:
- Rare-lineage kits (marginal cultural-tradition kits per 2026-05-23 recognition records × 5)
- Cross-substrate combinations (kits whose substrate-vector spans multiple primitives without clear primitive-anchor home)
- Easter-eggs (special kits, hidden content, designer-curated discoveries)

**Buffer scale carries natural meaning:**
- Tight lasso within-primitive = related kits (cohesive substrate)
- Cross-buffer lasso = unusual cross-substrate combinations (boundary-crossing kits)
- Buffer-exploration = discovery-moment for rare-lineage / cross-substrate / easter-egg content

### 1.3 Lasso ergonomics across buffer boundaries

Existing /forge Phase 2 lasso supports kit-selection within a single visual region. Phase 3 extends to:
- **Within-primitive lasso** (focused; tight-radius; selects 1-N kits within one primitive-anchor's cluster)
- **Cross-primitive lasso** (territory-crossing; wider-radius; selects kits across the buffer; surfaces unusual cross-substrate combinations)
- **Buffer-only lasso** (explores buffer territory; surfaces rare-lineage / easter-egg content)

The lasso behavior should make these three modes ergonomically distinct without explicit mode-toggle (the scale + position of the lasso gesture carries the semantic).

### 1.4 Positioning algorithm methodology

Per **Discipline #18.2 refinement** (methodology consultation fires AFTER baseline at extension hotspots), Phase 3 prototype tries **1-2 alternatives** empirically as part of the prototype:

| Methodology | Properties | When to prefer |
|---|---|---|
| **Force-directed (existing Phase 2 default)** | Proximity expresses relationship; tuning hard; gradient-friendly | Baseline — must include for comparison |
| **k-means anchors + radial projection** | Primitives anchor fixed; kits radiate; interpretable but rigid | Strong primitive-as-anchor signal; clean visual buffer between regions |
| **UMAP** | Non-linear; preserves local structure; axes lose interpretability | Strong cluster preservation; less interpretable spatial gradient |
| **Voronoi territory partitioning** | Each primitive owns territory; clean boundaries; loses gradient info | Strong buffer-space definition; loses smooth gradient between regions |

**Drax discretion:** pick baseline (force-directed) + ONE alternative for Phase 3 empirical comparison. Surface tradeoffs in Phase 3 close report. Elrond methodology consultation per Discipline #18 fires AFTER Phase 3 surfaces concrete methodology pain (per Discipline #18.2 timing refinement).

---

## 2. Substrate consumption

### 2.1 Kit corpus (existing /forge pipeline)
- Use existing 37-kit corpus loaded by /forge Phase 2 pipeline
- No new kit generation required
- If additional kits become available during Phase 3 execution (Cycle 14 Wave outputs), opportunistically include

### 2.2 Primitive-anchor curated subset
The 20 primitive families in atomic-substrate-registry are too many for Phase 3 visual test (visual chaos at 2D web rendering). **Curated subset for Phase 3 test:**

**Discipline #41 rationale for pre-offered curated subset:** substrate-emergent test set requires Phase B-equivalent full-corpus analysis (UMAP / clustering / cohesion-judge pass) which is OUT OF SCOPE for Phase 3's visual-pattern test. Phase 3 prototype VALIDATES the architectural pattern (two-layer + buffer-space) with a representative subset; canonical primitive-curation (which 12-20 of 20 primitives become canonical visible anchors) is DEFERRED to post-Phase-3 Pattern B with Matt on substrate-led principles. The three pre-offered framings below are NOT canonical proposals; they are prototype-scoped test sets that drax can substitute at discretion. The canonical primitive-curation question is preserved for substrate-led resolution at the appropriate analysis layer.

Suggested subset (gandalf-curated for Phase 3 testing; not canonical primitive-curation):
- **7 primary elements** (fire / water / earth / wind / lightning / holy / shadow + physical = 8) — natural primitive-anchor candidates per existing canonical-7+1 element catalog
- OR **5-7 weapon-form-family clusters** (blade / ranged / magical / brawl / hybrid) — alternative anchor framing
- OR **mixed test set** — 4 elements + 3 weapon-families = 7 anchors total

**Drax discretion:** pick one anchor framing for Phase 3 baseline test; surface tradeoffs in Phase 3 close report. The primitive-curation decision (which 12-20 of 20 primitives become canonical visible anchors) is DEFERRED to post-Phase-3 Pattern B with Matt; this prototype TESTS the pattern, doesn't lock the curation.

### 2.3 Buffer-space content
Phase 3 buffer-space populated by:
- Rare-lineage kits (marginal cultural-tradition kits per 2026-05-23 recognition records — if any exist in current 37-kit corpus; if not, surface this as a gap finding)
- Cross-substrate kits (kits whose substrate-vector doesn't strongly map to any single primitive-anchor; emergent from positioning algorithm)
- Optionally: 1-2 designer-curated easter-egg kits as buffer-content proof-of-concept (drax discretion)

---

## 3. Phase 3 sub-phase structure

### Phase 3.1 — Two-layer rendering baseline (deploy to Vercel preview)
- Primitive-anchor layer renders with distinct visual register from kit-cluster layer (size + shape + tone)
- Kit-clusters spatially proximate to their related primitive-anchors per substrate-vector proximity
- Force-directed positioning algorithm (existing Phase 2 default; baseline)
- Deploy to Vercel preview sub-route or feature flag
- **Acceptance:** primitive-anchors and kit-clusters visually distinguishable without explanation; spatial proximity reflects substrate-vector relationship

### Phase 3.2 — Buffer-space content + cross-buffer lasso ergonomics
- Deliberate empty-space buffer between primitive-anchor regions (positioning algorithm tuned for buffer)
- Buffer-space populated with rare-lineage + cross-substrate + easter-egg kits
- Lasso supports within-primitive + cross-buffer + buffer-only modes
- Lasso scale carries semantic naturally (without explicit mode-toggle UI)
- Deploy to Vercel preview
- **Acceptance:** buffer-space is visually distinct + holds discoverable content + lasso ergonomics across buffer feels natural

### Phase 3.3 — Positioning algorithm alternative comparison
- Implement ONE alternative positioning methodology per § 1.4 (drax discretion: k-means anchors / UMAP / Voronoi)
- Side-by-side comparison with force-directed baseline (toggle UI to switch)
- Surface visual + ergonomic + performance tradeoffs in Phase 3 close report
- Deploy to Vercel preview
- **Acceptance:** comparison toggle operational; tradeoffs visible to Matt at preview

### Phase 3.4 — Mobile-responsive validation
- Verify mobile rendering at iPad-class viewport (per D8 mobile-friendly-from-day-one + Earth-Avatar Creation Moment Architecture iPad gesture framing)
- Test lasso ergonomics on touch input (not just mouse)
- Performance budget: 60 FPS at 2D web layer
- **Acceptance:** mobile + desktop both ergonomically and performance-acceptable

### Phase 3.5 — Phase 3 close report (drax → gandalf → Matt)
- Document findings per § 4 acceptance criteria
- Surface positioning algorithm tradeoffs
- Surface buffer-space content design observations
- Surface lasso ergonomics observations
- Flag methodology hotspots requiring elrond consultation per Discipline #18.2
- Phase 3 GREEN / YELLOW / RED verdict per /forge convention
- Deploy final version to Vercel preview for Matt review

---

## 4. Acceptance criteria

| # | Criterion | How validated |
|---|---|---|
| 1 | Two-layer visual register distinction at 2D web rendering layer (primitives vs kits) | Visual inspection at Vercel preview; readable without explanation |
| 2 | Spatial proximity reflects substrate-vector relationship (kits near their primary primitive) | Substrate-trace data overlay (existing /forge analyst toggle) confirms spatial relationships |
| 3 | Deliberate empty-space buffer between primitive-anchor regions | Visual inspection; buffer is visually present (not zero-buffer cluster collision) |
| 4 | Buffer-space holds rare-lineage + cross-substrate + easter-egg content | Test data populated in buffer; lasso surfaces buffer content |
| 5 | Lasso supports within-primitive + cross-buffer + buffer-only modes via scale + position (no explicit mode-toggle) | Ergonomic test at preview; natural-feeling gesture semantics |
| 6 | Lasso scale carries semantic meaning (tight = related; wide = unusual combinations) | Test with multiple lasso scales; surfaced selections match expected semantic |
| 7 | Positioning algorithm alternative comparison toggle operational | Vercel preview toggle switches between force-directed + alternative |
| 8 | Mobile-responsive at iPad-class viewport (D8) | Test on actual iPad or browser-DevTools mobile emulation |
| 9 | Touch-input lasso ergonomics functional | Test on actual iPad or browser-DevTools touch emulation |
| 10 | 60 FPS at 2D web rendering layer | Browser performance profiler at Vercel preview |
| 11 | No raw LLM player-facing content (D7 AI-tell line) | Code review (Phase 3 is engineering visualization; no LLM at runtime) |
| 12 | No glyph-as-primitive-anchor implementation (Branch A deferred per Tal Rasha recognition record) — fences BOTH (a) visual register (primitive-anchors are NOT abstract symbolic glyphs) AND (b) interaction model (no sign-gesture / symbol-tracing input; Phase 3 lasso is spatial-selection only) | Code review: primitive-anchors render as figurative or nebula-cluster register; input gestures are lasso + pan + zoom + click; no glyph-tracing / sign-signing input model |

---

## 4.5 Quality criterion

**Game-quality goal this dispatch serves:** Players discover marginal-lineage and cross-substrate kit combinations through buffer-space exploration without explicit tutorial — buffer scale carries semantic meaning ergonomically (tight lasso = related kits; cross-buffer lasso = unusual combinations; buffer-only exploration = rare discoveries), and the visual register distinction between primitive-anchors and kit-clusters reads categorically (regional marker vs constellation member) without explanation. The two-layer + buffer-space pattern produces the "I found something" moment that Diablo II rare-affix discovery and isekai exploration-as-revelation conventions both depend on; absent this, the cosmograph degenerates into a flat browseable catalog where rarity and cross-substrate combinations require explicit tutorial surfacing.

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X (e.g., Earth-Avatar Creation Moment Architecture 2026-06-07, atomic-substrate-registry 2026-06-06, cosmograph-pivot 2026-06-05 § 9 amendment, Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09)
- Alternative execution Y serves the named quality goal better (e.g., single-layer with size-encoded primitive-vs-kit distinction; explicit mode-toggle UI for lasso semantics; no-buffer cluster-packing for spatial efficiency)
- Acceptance criteria can pass without advancing the quality goal (e.g., two-layer renders distinctly + buffer exists + lasso works, yet players cannot intuit cross-substrate-discovery as a mechanic — gesture semantics fail to carry meaning)
- Dispatch framing pre-commits to a decision Matt has not ratified (Branch A vs Branch B; primitive-curation lock; specific anchor count)
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate — § 2.2 curated subset framings; see § 5.2 Discipline #41 rationale)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40 candidate — e.g., 60 FPS performance target; iPad-class viewport bound; "5-7 weapon-form-family clusters" count)
- **Phase-3-specific:** Phase 3 results do NOT inform Branch A vs Branch B because they are structurally independent — surface if drax finds spatial-architecture results would require Branch A to validate, in which case the Branch decision composition with Phase 3 needs revisiting at close-report layer

---

## 5. Discipline citations

### 5.1 Discipline #18 + #18.2 (math hotspot + methodology consultation timing)
Positioning algorithm choice IS a math hotspot. Per Discipline #18.2 refinement: methodology consultation fires AFTER baseline at extension hotspots. Phase 3 prototype tries 1-2 alternatives empirically AS the baseline; elrond formal methodology consultation fires post-Phase-3 if pain surfaces.

### 5.2 Discipline #41 (pre-authored taxonomy interrogation)
Primitive-curation is NOT fixed in Phase 3. Drax tests with curated subset per § 2.2; primitive-curation decision (which 12-20 of 20 primitives become canonical visible anchors) is DEFERRED to post-Phase-3 Pattern B with Matt. Substrate-led discipline preserved.

### 5.3 Discipline #25 (semantic-layer rep-audit)
If Phase 3 surfaces kits where substrate-vector proximity to primitive-anchor doesn't match substrate-cultural-coherence (e.g., a kit positioned near "fire" anchor by mechanical-vector but kit's cultural-tradition is water-coded), flag for gandalf review. Substrate votes at geometry layer; design surfaces audit at semantic layer.

### 5.4 D7 (AI-tell line; no raw LLM player-facing content)
Phase 3 is engineering visualization. No LLM at runtime. Primitive-anchor labels + kit identity content come from existing pre-generated corpus (engine output + cohesion-judge identity content; NOT runtime LLM).

### 5.5 D8 (mobile-friendly-from-day-one)
Phase 3 mobile-responsive validation per § 3.4. iPad-class viewport + touch-input ergonomics required.

### 5.6 Recognition-validate-commit (gandalf OP § 3.4 + 4.1)
Phase 3 IS empirical validation of the two-layer + buffer-space architecture pattern recognized 2026-06-08. Recognition captured; validation in flight; commit post-validation. Branch A glyphic-anchor architecture (Tal Rasha recognition record 2026-06-09) is SEPARATE deferred recognition; do NOT pre-commit Branch A via Phase 3.

---

## 6. What Phase 3 does NOT include (explicitly out of scope)

- ❌ Spherical-shell celestial-sphere geometry (Earth-Avatar canonical § 2.6) — Phase 3 is 2D web flat-plane; spherical geometry is UE-port scope
- ❌ 3D nebula volumetric context beyond celestial shell — UE-port scope
- ❌ Niagara VFX rendering — UE-port scope (WS2 commission)
- ❌ AAA fidelity visual register — UE-port scope
- ❌ Glyph-as-primitive-anchor architecture (Branch A; pre-empirical; deferred per Tal Rasha recognition record)
- ❌ Zodiac-as-cosmograph-anchor architecture (gated on Legolas zodiac-substrate-corpus commission output)
- ❌ Primitive-curation lock (which 12-20 of 20 primitives become canonical visible anchors — deferred to Pattern B with Matt post-Phase-3)
- ❌ Path I (drop-ingredients) creation-mechanism implementation (Earth-Avatar Creation Moment Architecture § 2.4 dual-creation — UE-port scope; /forge is exploration surface not creation surface)
- ❌ Earth avatar + grassy knoll + spirit form context (UE-port scope)
- ❌ LLM-generated player-facing content (D7)
- ❌ Cross-cycle / scope-amendment commits without Matt-authorization (per CLAUDE.md addendum)

---

## 7. Composition with prior work

| Prior work | Composition |
|---|---|
| `/forge Phase 2` (deployed Vercel) | Phase 3 EXTENDS; preserves existing constellation default + analyst toggle; adds two-layer + buffer-space + alternative-positioning-algorithm |
| `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` | Phase 3 validates the visualization pattern that UE port will productionize at AAA fidelity; spherical-shell + 3D context deferred to UE |
| `2026-06-05-cosmograph-pivot.md` § 9 amendment | Primitive-as-star + kit-as-constellation Phase 3 tests under Branch B (primitive-as-figurative-anchor); Branch A glyphic-anchor architecture deferred |
| `2026-06-06-atomic-substrate-registry.md` | Curated primitive subset for Phase 3 testing; canonical primitive-curation decision deferred to Pattern B with Matt post-Phase-3 |
| `2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` | DEFERRED architectural-commitment per recognition-validate-commit; Phase 3 does NOT pre-commit Branch A; gated on Legolas commission output |
| Marginal-lineage recognition records 2026-05-23 × 5 | Rare-lineage kits compose into buffer-space as discoverable content; substrate-led discipline preserved |
| `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` | db-lyon empirically validated MCP rendering tooling; WS2 commission inherits Phase 3 findings for Niagara nebula rendering scope authoring |

---

## 8. Deliverables

1. **Vercel preview deployment** at each phase milestone (3.1 → 3.5)
2. **Phase 3 close report** at `agentic_orchestration/drax/notes/2026-06-XX-forge-phase-3-close-report.md` (date per actual close) including:
   - Per-acceptance-criterion verdict
   - Positioning algorithm tradeoff surface (force-directed vs alternative)
   - Buffer-space content design observations
   - Lasso ergonomics observations
   - Methodology hotspots flagged for elrond consultation per #18.2
   - Phase 3 GREEN / YELLOW / RED verdict
   - Gap notes for UE-port scope (what Phase 3 cannot validate; what defers to UE)
   - Subset-bias observation: did the chosen primitive-anchor subset (elements / weapon-forms / mixed) materially shift architectural-pattern findings? If yes, surface alternation hypothesis for canonical primitive-curation Pattern B input.
3. **Code changes** in `reincarnated-loadout/` per drax seam; auto-commit per CLAUDE.md addendum

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt directive (Options 1+2 sequence; this is Option 2).

**Authority:** gandalf cross-cutting design-steward commission authority for player-surface validation workstream + composition with cosmograph architectural commitments.

**Routing:** drax executes; per-phase Vercel preview deployments for Matt review; Phase 3 close report routes to gandalf for design review + Matt for architectural feedback.

**Empirical-evidence triggers:**
- Phase 3 close report surfaces methodology hotspots → elrond methodology consultation per Discipline #18.2 (fires post-baseline)
- Phase 3 visual register tradeoffs inform Branch A vs Branch B post-Legolas-commission architectural-decision call (Phase 3 validates pattern; Branch decision still requires Legolas N count)
- Phase 3 findings inform WS2 (Niagara VFX) commission scope authoring at UE-port phase
- Phase 3 mobile-responsive findings inform Earth-Avatar Creation Moment Architecture iPad gesture framing

**Composition with prior canonical commitments:** all preserved (Earth-Avatar Creation Moment Architecture 2026-06-07 + federated PC team architecture 2026-06-07 + atomic-substrate-registry 2026-06-06 + hypothesis-flow 2026-06-06 CANONICAL + cosmograph-pivot 2026-06-05 + Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09).

**End of commission.**
