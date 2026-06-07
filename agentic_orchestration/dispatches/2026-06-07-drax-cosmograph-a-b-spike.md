# Dispatch — Drax Cosmograph A/B Spike (Primitive-Galaxy vs Kit-Constellation Render Modes)

**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 ratification of Option α-prime staged spike + c1 global-bound starting parameter, post Pattern-B design dialogue diagnosing /forge constellation-visibility failure
**To:** drax (loadout + demo player-surface seam)
**Cycle:** Post-cosmograph-Phase-A iteration spike — rendering-unit-of-visualization architecture question
**Type:** SPIKE — empirical visual-architecture validation; A/B render mode comparison; staged Phase 1 sample → empirical gate → Phase 2 full corpus + toggle UI
**Cost budget:** $0 LLM (no LLM calls at /forge per Option B amendment + D7)
**Time budget:** Phase 1 sample ~1-2 hr; Phase 2 full toggle ~3-6 hr if Phase 1 GREEN. Total ~4-8 hr drax wall-clock if both phases fire.
**Critical anchors:**
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 (primitive-as-star + kit-as-constellation architectural lock — substrate truth)
- `canonical/story/2026-06-06-cosmograph-phase-a-creation-moment-wave-close.md` § 7 (Phase A production state — 570 primitives + 1000 PROVISIONAL constellations live at `/forge`)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` § 1 (Layer 0 primitive families)
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/cosmograph_README.md` (current drax ingestion contract — load-bearing input; this spike consumes the same packet)
- `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md` § 4.3 (constellation-overlap composite score algorithm — lasso resolution path inherited)
- `agentic_orchestration/dispatches/2026-06-06-drax-cosmograph-phase-a-rendering.md` (predecessor Phase A dispatch — this spike extends, does not replace)

---

## 0. TL;DR

Matt's empirical observation on the live `/forge` Phase A surface: **8 element-primary primitives cluster tightly in the upper-right; lassoing recovers arbitrary primitive subsets rather than whole constellations; the kit-as-constellation metaphor is architecturally cemented but visually scattered.** Per Pattern-B design dialogue 2026-06-07, the diagnosis is that the current "primitive-galaxy" rendering (unique primitives positioned by substrate-similarity) is failing as the player-facing surface — kits' component primitives are dispersed across the galaxy because each primitive sits in its substrate-similarity neighborhood, so constellation-membership is non-local.

**The architectural question:** does **kit-as-bounded-constellation** (per-kit duplicate primitive instances arranged in centroid-bounded local subspace, with inter-constellation similarity expressed via centroid-proximity) read more clearly than **primitive-similarity-galaxy** (current Phase A) as the kit-as-discovery metaphor?

**The empirical refutation surface:** drax A/B spike at `/forge` toggling between the two render modes. Cheapest test point for this metaphor question (vs deferring to mantis 3.7 STRETCH where 3D rendering would confound the metaphor signal with 3D-perf signal).

**Spike scoping per Matt 2026-06-07 ratification:**
- **Option α-prime staged:** Phase 1 sample (5-10 constellations only; rest hidden) → empirical visual-readability gate → Phase 2 full corpus + toggle UI if Phase 1 GREEN
- **c1 global-bound starting parameter:** all constellations same max-diameter; centroid placement by inter-constellation similarity; force-directed-within-bound for intra-constellation arrangement
- **A/B toggle target:** `/forge?view=primitive` (current Phase A render) vs `/forge?view=constellation` (new Option C render); both modes coexist; primitive-galaxy preserved for analyst-toggle diagnostic use

**Deliverable:** screenshot pair (current vs Option C, same 5-10 constellations at Phase 1; full corpus at Phase 2) + toggle UI operational at production Vercel preview + brief findings doc with verdict (READS-CLEAN / YELLOW-needs-tuning / RED-architecturally-wrong).

**Substrate-led discipline preserved:** primitives still ARE the substrate truth; per-kit instances at Option C are RENDER-LAYER duplicates referencing the same primitive identity. Substrate vote stays binding at geometry layer; render placement function shifts to constellation-bound at the semantic layer (per Discipline #25 semantic-layer rep-audit composition).

---

## 1. Scope

### 1.1 What drax produces (Phase 1 — empirical-gate slice)

Delivery packet at `agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/`:

| Artifact | Format | Purpose |
|---|---|---|
| `phase-1-sample-findings.md` | markdown | Phase 1 verdict + 5-10 sample constellation selection rationale + force-config tuning notes + visual-readability assessment |
| `phase-1-screenshot-primitive-mode.png` | PNG | Current `/forge` render of the same 5-10 constellation cohort |
| `phase-1-screenshot-constellation-mode.png` | PNG | Option C render of the same 5-10 constellation cohort |
| `phase-1-toggle-operational.md` (optional) | markdown | If Phase 1 deploys a sub-route or feature flag for Matt to A/B compare empirically before Phase 2 fires |

**Phase 1 close criterion:** drax authors `phase-1-sample-findings.md` with verdict + screenshots; pushes to origin; surfaces to gandalf (this dispatch's author) for Phase 2 ratification.

### 1.2 What drax produces (Phase 2 — full toggle, only if Phase 1 GREEN)

| Artifact | Format | Purpose |
|---|---|---|
| `phase-2-full-corpus-findings.md` | markdown | Phase 2 verdict + full corpus render notes + performance measurements (15k node visual readability + FPS at constellation mode) + force-config final parameter lock |
| `phase-2-screenshot-primitive-full.png` | PNG | Full-corpus primitive-galaxy render (existing Phase A, captured for parity) |
| `phase-2-screenshot-constellation-full.png` | PNG | Full-corpus Option C constellation render |
| Production deployment | Vercel preview URL | `/forge?view=primitive` and `/forge?view=constellation` both operational on live preview |

**Phase 2 close criterion:** toggle operational on Vercel preview + screenshot pair captured + findings doc + push to origin.

### 1.3 What drax does NOT produce in this spike

- **No engine-side changes.** Ingestion contract from elrond Phase A packet is read-only input. If a data gap surfaces (e.g., per-kit primitive-membership requires denormalization), surface to gandalf for elrond commission rather than self-resolve.
- **No LLM-driven content.** Spike preserves D7 — no LLM-named identities introduced at constellation mode either.
- **No new substrate-trace extraction commission.** Use the existing `cosmograph-substrate-trace-2026-06-06/` packet (`primitive_registry.parquet` + `kit_constellations.parquet`).
- **No demo1 (Pixi.js standalone) touch.** Spike scope is reincarnated-loadout `/forge` only.

---

## 2. Architectural framing

### 2.1 The two render modes

**Mode A — Primitive-galaxy (current Phase A; preserved as analyst diagnostic toggle):**
- Each unique Layer 0 primitive renders as a single star
- Positions: UMAP/t-SNE 2D projection over primitive co-occurrence space (per elrond Phase 4 packet)
- Substrate-similarity vote dominant — fire primitives cluster together; weapon-form-token primitives cluster together; etc.
- Constellation membership rendered via dotted MST lines on lasso/hover/Z-key (per Phase A wave-close § 7)
- **Strength:** substrate-coverage analysis (gandalf / elrond diagnostic use); compositional macro-pattern visibility
- **Failure mode (per Matt 2026-06-07):** kit-as-discovery metaphor scattered; constellation locality lost; lasso recovers arbitrary primitive subsets

**Mode B — Kit-constellation (new Option C; player-facing target if Phase 1 GREEN):**
- Each kit renders as a **bounded local cluster of per-kit primitive instances**
- Per-kit duplicate of each component primitive (e.g., kit_001 has its own copy of `fire` primitive, kit_002 has its own; both reference same underlying primitive identity)
- Force-directed within-bound: intra-constellation attraction (springs between kit-mate primitives) > inter-constellation repulsion; constellation diameter emerges naturally
- Constellations placed by inter-constellation similarity (centroid-proximity = shared-primitive-fraction); fire-heavy constellations cluster near other fire-heavy constellations at the macro level
- **c1 global bound starting parameter:** all constellations same max-diameter (`MAX_CONSTELLATION_RADIUS` — drax tunes; suggested starting value 60-80 px at 1.0× zoom)
- **Strength:** kit-as-bounded-unit reads as discovery metaphor; lasso recovers whole constellations or constellation-neighborhoods; player onboarding flow honors the substrate→kit composition story
- **Cost:** ~15× node count (1000 constellations × ~15 primitive-instances per kit ≈ 15,000 nodes). Pixi.js handles; visual readability needs empirical check at Phase 2

### 2.2 Toggle architecture

`/forge?view=primitive` ↔ `/forge?view=constellation` — URL query param toggle; defaults to `constellation` if Phase 2 ratifies (player-facing default); `primitive` preserved for analyst diagnostic use (gandalf / elrond). Toggle UI element (top-right of canvas, near zoom controls) for live mode switching without URL edit.

### 2.3 Lasso semantics under Mode B

- Lasso draws polygon → captures per-kit primitive instances
- **Dedupe to kits BEFORE running constellation-overlap composite-score resolution** (per `2026-06-06-cosmograph-star-granularity-verdict.md` § 4.3 algorithm)
- Composite-score lookup unchanged: `0.4 × coverage_fraction + 0.3 × density_score + 0.3 × β-weighted overlap`
- Side panel display unchanged: matched kit's pre-computed identity (placeholder for PROVISIONAL constellations per D7)
- **One semantic nuance:** Mode B lasso may now CLEANLY capture single-constellation selections (the "lasso this kit" UX); Mode A's "lasso a primitive-region" UX still preserved when toggle set to `primitive`

### 2.4 Intra-constellation edge rendering

Two options to consider during Phase 1 prototyping:
- **(i) Render intra-constellation edges as faint connection lines** between kit-mate primitives (constellation-as-figure visual reinforcement)
- **(ii) Rely on force positions alone** — no edges rendered; constellation membership conveyed by spatial proximity + bounded extent

**Lean (ii) for Phase 1 starting baseline** — 15k nodes × ~15 edges = ~225k edges; Pixi.js handles but visual clutter risk at full corpus; force positions should suffice if bound is tight enough. Drax may experiment with (i) at low-opacity if Phase 1 readability suffers; surface in `phase-1-sample-findings.md` if attempted.

---

## 3. Phase 1 execution

### 3.1 Sample selection (5-10 constellations)

Choose a diverse but small cohort for Phase 1 empirical assessment. Suggested selection criteria (drax has discretion):

- **2-3 cross-element pairs** (e.g., 2 fire + 2 water constellations to see element-clustering at constellation-centroid layer)
- **1-2 hybrid kits** (multiple element_primary or unusual primitive combinations to see cross-element constellation placement)
- **1-2 attribute-group representatives** (one STR-heavy, one INT-heavy to see faction-halo composition under Mode B)
- **1-2 named-bearer-or-equivalent simulated constellations** (varying kit sizes to see how bound responds to primitive count)

Document selection rationale in `phase-1-sample-findings.md` § "Sample cohort selection."

### 3.2 Data prep

From the existing elrond packet (`agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/`):

1. **For each kit in sample cohort:** read `kit_constellations.parquet` row → enumerate constituent primitive_ids → instantiate per-kit-primitive-instance node IDs (e.g., `kit_001:fire`, `kit_001:weapon_form_dao`, `kit_002:fire`, ...)
2. **Edge list:** intra-kit edges between all pairs of per-kit-primitive-instances (spring attraction → constellation cohesion)
3. **Inter-kit positioning hint (optional Phase 1):** seed centroids from primitive co-occurrence similarity (kits sharing more primitives → centroids closer); or let force layout discover positions from scratch
4. **Bound enforcement:** soft-clamp intra-constellation distances to `MAX_CONSTELLATION_RADIUS` via tuned spring strength + repulsion floor

### 3.3 Force config starting parameters (c1 global bound)

These are starting values; drax tunes during Phase 1:

| Parameter | Suggested starting value | Purpose |
|---|---|---|
| `MAX_CONSTELLATION_RADIUS` | 60-80 px (at 1.0× zoom) | Global diameter cap; all constellations bounded the same |
| `INTRA_KIT_SPRING_STRENGTH` | 0.8-1.0 (high) | Pull kit-mate primitives toward each other |
| `INTER_KIT_REPULSION` | 0.2-0.4 (moderate) | Push different kits' primitives apart |
| `CENTROID_ATTRACTION_BY_SHARED_PRIMITIVES` | 0.1-0.3 (gentle) | Inter-constellation positioning hint (fire-heavy near fire-heavy) |
| `REPULSION_FLOOR` | 8-15 px | Prevent overlap collapse of individual stars within a constellation |

### 3.4 Phase 1 verdict format

`phase-1-sample-findings.md` should answer:

1. **Visual readability:** does the kit-as-bounded-constellation metaphor read CLEAN, YELLOW (needs tuning), or RED (architecturally wrong) at the sample cohort scale?
2. **Force-config landing values:** what starting parameters converged on a readable rendering? Note any tuning iterations performed.
3. **Inter-constellation macro-pattern:** is element-similarity at the centroid layer legible (fire-heavy constellations cluster near each other)? If not — does that matter at sample scale, or is it a Phase 2 full-corpus concern?
4. **Lasso UX simulation:** mentally simulate lassoing — does Mode B's lasso semantics improve over Mode A at this sample? Concrete observations.
5. **Phase 2 readiness:** GREEN (proceed to full corpus + toggle) / YELLOW (proceed with caveats — document) / RED (do not proceed; architectural reconsideration needed; ping gandalf)

### 3.5 Phase 1 timebox

~1-2 hours wall-clock. If Phase 1 work expands past 3 hours (force-config tuning rabbit hole, etc.) — pause, document, surface to gandalf for Pattern-A query before continuing.

---

## 4. Phase 2 execution (only if Phase 1 GREEN)

### 4.1 Scope

- Scale Phase 1 rendering pattern to full corpus (1000 PROVISIONAL constellations + 570 unique primitives × per-kit instances ≈ 15k nodes)
- Build toggle UI element (top-right of canvas; toggle button + URL sync to `?view=primitive` / `?view=constellation`)
- Preserve all Phase A interactions in Mode A (primitive-galaxy view unchanged from current `/forge` Phase A); add Mode B interactions
- Performance check: target 60 FPS at full corpus Mode B; if hits drop below 30 FPS persistently, document for substrate-evidence-based viewport-culling Phase 3 work
- Deploy to Vercel preview; capture screenshot pair (Mode A full vs Mode B full)

### 4.2 Performance instrumentation

Existing FPS ticker from Phase A (`app.ticker.FPS` per frame; min/median/mean/p95 windows) carries forward unchanged. Phase 2 findings doc records observed FPS distribution at Mode B full corpus.

### 4.3 Phase 2 verdict format

`phase-2-full-corpus-findings.md` should answer:

1. **Full-corpus visual readability:** does Mode B hold up at 15k nodes, or does visual clutter degrade the constellation metaphor?
2. **Performance envelope:** FPS distribution at Mode B full corpus; concerns flagged for future LOD work if any
3. **Toggle UX:** does live A/B toggle work cleanly? Any state-management quirks?
4. **Final force-config parameter lock:** the values that landed for c1 global-bound architecture
5. **Recommendation for default mode:** does Mode B replace Mode A as default at `/forge`? Or stay co-equal toggle? Or revert to Mode A primary with Mode B as future-explore?

### 4.4 Phase 2 timebox

~3-6 hours wall-clock. If Phase 2 work expands past 8 hours total spike time — pause, document, surface to gandalf.

---

## 5. Empirical-evidence triggers + handoffs

### 5.1 Phase 1 → Phase 2 gate

Phase 1 GREEN verdict from drax + gandalf ratification (gandalf reviews `phase-1-sample-findings.md` + screenshot pair; ratifies Phase 2 fire OR requests architectural reconsideration).

### 5.2 Phase 2 → cosmograph-iteration-record close

Phase 2 close fires when:
- Toggle operational at Vercel preview
- Findings doc + screenshot pair pushed to origin
- Gandalf reviews + authors brief verdict (lock Mode B as default? co-equal toggle? revert?)

### 5.3 Downstream consumption by mantis UE 3.7 STRETCH

Whichever mode lands as `/forge` default informs mantis UE 3.7 STRETCH design (3D cosmograph viability) — mantis inherits the metaphor verdict from this spike + tests perf-feasibility in 3D independently. Decouples metaphor signal from 3D-rendering signal.

### 5.4 Future LOD work trigger

If Mode B full-corpus FPS drops below 30 FPS persistently OR visual clutter degrades readability, the substrate-evidence-based LOD optimization queued at `2026-06-06-cosmograph-phase-a-creation-moment-wave-close.md` § 6.2 fires.

---

## 6. Substrate-led discipline preservation

Per Discipline #41 (substrate-led; pre-imposed taxonomy interrogation) + #25 (semantic-layer rep-audit):

- **Substrate vote stays binding at geometry layer:** primitives ARE the substrate truth; per-kit instances at Mode B reference the SAME underlying primitive identity (e.g., `kit_001:fire` and `kit_002:fire` both bind to the unique `fire` primitive in `primitive_registry.parquet`). No substrate identity manufactured.
- **Render placement function shifts at semantic layer:** Mode B's centroid-bounded constellation placement is a render-time visualization choice, NOT a claim about substrate structure. The PRIMITIVE remains the unit-of-substrate; the CONSTELLATION becomes the unit-of-visualization.
- **Provenance tagging preserved:** if Phase A's provenance-tag visual encoding (cycle-14 corpus vs Move B simulated) survives to Mode B's per-kit instances, preserve. If not feasible at Phase 1 budget, document and route to Phase 2.

### 6.1 Substrate-coverage analyst use preserved via Mode A toggle

`/forge?view=primitive` remains operational for analyst-toggle use: gandalf / elrond can still see substrate-coverage diagnostic patterns (e.g., "fire primitive cluster shows over-representation"). The shift to Mode B as player-facing default does NOT retire Mode A's diagnostic value; both modes coexist behind the toggle.

---

## 7. Critical cross-seam touches

- **Elrond:** read-only consumer of existing Phase 4 packet (`cosmograph-substrate-trace-2026-06-06/`). No new elrond commission required. If Phase 1 surfaces an ingestion-contract gap (e.g., per-kit primitive-membership not denormalized as drax needs), surface to gandalf — gandalf decides whether to commission elrond Phase 4-supplement or have drax compute in-render.
- **Mantis:** consumer of metaphor verdict (downstream; not blocking this spike). UE 3.7 STRETCH inherits whichever mode lands.
- **Gandalf:** ratifies Phase 1 GREEN/YELLOW/RED + Phase 2 close + final mode disposition.
- **Jack-ryan:** Gate-2 review on spike close per critique-pair-gate-protocol (drax authors verdict; jack-ryan checks discipline compliance; INFO/WARN/BLOCK as warranted).

---

## 8. Framing-audit Q1-Q3 (Discipline #23; OP § 4.1)

Per the framing-audit checklist applied at dispatch consumption:

**Q1 — Load-bearing framing assumptions:**
- The metaphor failure Matt observed is at the **rendering-unit-of-visualization** layer (kits scattered as primitive-subsets), not at the **substrate-structure** layer (primitive clusters are substrate-honest).
- Mode B fixes the rendering-unit problem without touching substrate.
- Per-kit primitive instances at Mode B do not corrupt substrate vote (verified at § 6).

**Q2 — Refutation evidence in scope:**
- If Phase 1 sample readability shows constellation-bounding makes things WORSE (visual clutter from 15× node density even at sample scale), the architectural premise is wrong → Phase 1 RED → ping gandalf
- If sample readability is fine but full-corpus Phase 2 hits intractable visual clutter, the architecture is right but needs LOD support → Phase 2 YELLOW → document for future LOD work

**Q3 — Refine framing rather than execute?**
- The cheapest refutation IS to execute Phase 1 (~1-2 hr); not deferrable to paper analysis
- Pre-execution refinement opportunity: drax may surface concerns at Phase 0 (before Phase 1 fires) via Pattern-A query if force-config starting parameters look obviously wrong, or if the per-kit instance node-ID scheme surfaces a different data-shape problem. Otherwise execute Phase 1 directly.

---

## 9. Sign-off

**Authored:** gandalf 2026-06-07 per Matt Pattern-B design dialogue diagnosing /forge constellation-visibility failure + Option α-prime staged spike ratification + c1 global-bound starting parameter ratification.

**Empirical-evidence triggers for this spike's close:** Phase 1 verdict ratified → Phase 2 toggle operational at Vercel preview → gandalf authors mode-disposition verdict.

**Routing:** drax consumes at session-start; Phase 1 returns to gandalf for ratification; Phase 2 fires conditionally; jack-ryan Gate-2 at spike close.

**End of dispatch.**
