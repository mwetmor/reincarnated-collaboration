# Finding — 2026-06-07 — Cosmograph A/B Spike (Phase 2 Full Corpus)

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO
**Target:** loadout commits `bb7176c` + `e63f667` + `986334d` + `7d411a2`; collab commit `bb9e5f4`
**Developer:** drax
**Principles applied:** Principles 2, 3, 4, 5; ADR-004, ADR-006; Disciplines #2, #25, #41

---

## Verdict

**PASS-with-INFO.** Spike formally closes. Push-authorization request may proceed to Matt for both repos (collab `bb9e5f4`; loadout `bb7176c..7d411a2`).

No BLOCKs. No WARNs. Two INFO observations noted below; neither holds up shipping.

---

## What I found

Phase 2 deliverables are complete and correctly scoped. The full deliverable set exists at `agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/`: `phase-2-full-corpus-findings.md`, `phase-2-screenshot-primitive-full.png`, `phase-2-screenshot-constellation-full.png`. The Vercel preview URL is documented. Code-level review of `ConstellationModeCanvas.tsx` and `compute-constellation-layout.py` confirms:

- LOD architecture is operational: `dotsLayer` / `starsLayer` / `boundsLayer` visibility-toggled at `normalizedZoom = stage.scale.x / initialScale` threshold 2.0; single-frame switch with no redraw.
- Substrate-led discipline honored (Disciplines #25, #41): per-kit instance node IDs (`kit_001:fire`) exist only in the Pixi.js render layer. Lasso deduplication `nodeId.slice(colonIdx + 1)` extracts `primitive_id` before calling `scoreKitsByPrimitiveSet`, which scores against the kit registry — no per-kit instance identity propagates into substrate vote or scoring.
- Python pre-compute pipeline (`compute-constellation-layout.py`) consumes `kit_constellations.json` + `primitive_registry.json` from `public/data/cosmograph/`; outputs `constellation_layout.json`. UMAP centroid_x/y explicitly NOT used for constellation placement (meta.umap_caveat field in the JSON). The JSON IDs are rendering-layer artefacts only.
- Mode B is the `/forge` default: `Forge.tsx` line 61 resolves `viewParam === 'primitive' ? 'primitive' : 'constellation'` — any absent or non-'primitive' param yields constellation mode. `setViewMode('constellation')` clears query param rather than adding one. Correct.
- "SPIKE·P2·1000 kits" badge retired; player-facing kit-discovery copy installed per commit `7d411a2`.
- FPS target: 60 FPS in both dot (1.0×) and star (2.0×+) modes documented in `phase-2-full-corpus-findings.md` § 3. Static Pixi.js Graphics with no per-frame draw updates.
- Substrate-coverage caveat carried forward in Phase 2 findings § 9, watermark text in ConstellationModeCanvas.tsx line 342, and in the Python script header comment. Scope discipline preserved.
- Gate-1 Finding 4 REFUTED: UMAP centroid_x/y structural degenerate finding confirmed at full corpus scale, recorded in `phase-2-full-corpus-findings.md` § 7. `TODO(drax)` annotation present in `compute-constellation-layout.py` line 31 — names owner, describes trigger (engine kit-to-kit similarity 2D embedding when available), traceable to Phase 1 findings and dispatch.
- F-R force layout abandonment rationale documented: mean Jaccard ~0.224 at 1000 kits; aggregate spring attraction overwhelms per-pair repulsion; grid layout correct for uniform-similarity corpora. Drax surfaced the failure empirically and pivoted (smoke-then-scale pattern honored — Discipline #2 ratified).
- Grid layout preserves macro-pattern signal: element-sorted (ELEMENT_ORDER: fire→lightning→water→wind→earth→physical→shadow→holy) produces legible element-regional clustering in dot view per findings § 2. The sort is the macro-pattern signal; force-layout gradient was never the right mechanism given substrate uniformity.
- drax-OP discipline: no engine-side changes; no LLM-driven content; no demo1 touch; elrond ingestion contract consumed read-only.
- AGENT_STATE.md updated (Phase 2 session summary + active TODO overrides + pending commits listed).

---

## Rationale

### Review item 3.1 — Grid-layout architectural pivot: decisions-log candidacy

**Determination: NO — not a separate decisions-log entry at this time.**

Reasoning: The primitive-as-star + kit-as-constellation architectural lock was captured in `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 and is already binding. The F-R→grid pivot is an empirical implementation finding nested WITHIN that architectural commitment, not a new architectural commitment with downstream-binding force on its own. The pattern ("uniform-similarity substrate corpora require grid layout over force-directed layout") is real but has one founding instance. Per decisions-log threshold: architectural commitment YES requires downstream-binding force on future workstreams — this finding is informative to mantis UE 3.7 STRETCH 3D cosmograph and elrond Phase B, but it does not independently lock any design direction not already locked by the cosmograph-pivot § 9 entry. The correct home is the Phase 2 findings doc (where it lives) + AGENT_STATE.md TODO(drax) breadcrumb (where it lives), not the decisions-log. If the pattern recurs in mantis 3D or a second substrate-visualization workstream, that second instance is the trigger for a decisions-log entry.

**Discipline-amendment candidacy:** The pattern ("uniform-similarity substrate corpora: force-directed layout has no gradient to exploit; element-sorted grid is the correct fallback") is a one-instance candidate. Per discipline-ratification precedent, one instance is not sufficient for a numbered discipline. Queue as a candidate; activate if a second cross-workstream instance confirms.

### Review item 3.2 — Substrate-led discipline at rendering layer

**Determination: PASS.** Code-level verification confirms rendering-layer isolation is clean. Per-kit instance node IDs (`kit_001:fire`) exist only in: `allNodes[]` array (render-layer enumeration), `firstClassNodes[]` filter (visibility), and `capturedKitNodeIds` Set (lasso capture). The dedup at `nodeId.slice(colonIdx + 1)` correctly extracts raw `primitive_id` before any substrate operation. `scoreKitsByPrimitiveSet` receives only `uniquePrimitiveIds: Set<string>` — undecorated primitive IDs with no kit-instance prefix. The `constellation_layout.json` clusters dict uses `kit_id` as key and `{p, x, y}` as node records — the `p` field is raw `primitive_id`, no kit decoration. No substrate identity manufactured.

### Review item 3.3 — constellation_layout.json payload: Vercel preview budget

**Determination: INFO (no action required now; note for Phase B planning).**

2.04MB raw / ~600KB gzip is within acceptable range for a player-facing surface loaded on first constellation-mode selection. Lazy loading on first Mode B mount (not at page load) is the correct architecture and is implemented in `Forge.tsx` lines 70-91. Cold-cache first-paint cost of ~200-400ms on typical connection is acceptable for a non-game-critical visualization at Vercel preview stage; production CDN behavior closes the gap further. Cache-Control headers for deterministic pre-computed artifacts (immutable + long-TTL) are worth adding when the asset graduates from preview to production deploy — this is a Phase B concern, not a spike-close blocker.

One observation: `loadConstellationLayout()` is triggered at `viewMode !== 'constellation'` check (`layoutLoadState !== 'idle'` guard prevents re-fetch). If a user loads `/forge` (default = constellation), the layout fetch fires immediately at mount — this is correct behavior and intended. If a user loads `/forge?view=primitive`, the layout fetch is deferred until they first switch to constellation. No issue.

**INFO: Add Cache-Control: immutable + long-TTL to constellation_layout.json at production Vercel deploy time (Phase B). Not blocking for preview.**

### Review item 3.4 — TODO(drax) breadcrumb form correctness

**Determination: PASS with one minor INFO.**

Form is correct: `TODO(drax)` names owner. The annotation appears in two locations:
1. `compute-constellation-layout.py` line 31 — header comment, describes trigger (engine kit-to-kit similarity 2D embedding when available), references the Phase 1 UMAP-degenerate finding.
2. `constellation_layout.json` meta.umap_caveat field — machine-readable record of the override.

The breadcrumb is discoverable: the dispatch completion record references it; the AGENT_STATE.md TODO section names it explicitly. The elrond commission trigger (real cycle-15+ kits) is documented in AGENT_STATE.md and findings § 7.

**INFO (minor): The TODO in `compute-constellation-layout.py` does not cite the dispatch filename or findings doc path. A reader encountering this file cold cannot follow the reference chain without grep. Suggest adding `# See: agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-2-full-corpus-findings.md § 7` to the TODO comment at drax's next touch of this file. Non-blocking.**

### Review item 3.5 — Gate-2 standard checks

- **Math-before-code (Principle 1, Discipline #1):** N/A for rendering-layer spike. Force-config starting parameters were dispatch-provided (§ 3.3); drax's grid-spacing math is documented in `compute-constellation-layout.py` header comment and Phase 2 findings § 5 (cell_h - 2×JITTER_PX = 169.4 px > 140 px threshold). The abandonment of F-R at full corpus is empirical, not a math-before-code violation — the dispatch explicitly designated Phase 1 as the empirical gate for this question.
- **Smoke-gate (Principle 2, Discipline #2):** Phase 1 (10-kit sample) served as the smoke run. Phase 2 (full corpus) scaled from that baseline. F-R collapse at 1000 kits was caught by the smoke-then-scale discipline. Build output `tsc -b && vite build` PASS documented in AGENT_STATE.md (Phase 2: 1499 modules, 0 TS errors; Phase 1: 1500 modules, 0 TS errors, 79/79 tests pass). PASS.
- **Cross-seam impact (Principle 3, ADR-004):** Elrond ingestion contract consumed read-only. No elrond commission fired. No MIGRATION.md required — drax-seam-internal change consuming an existing packet. PASS.
- **Decisions-log as truth (Principle 4):** No conflict with any locked decision. Cosmograph-pivot § 9 architectural lock honored throughout. PASS.
- **Discipline #25 (semantic-layer rep-audit) + #41 (substrate-led):** Verified above at § 3.2. PASS.

---

## Action

- [x] No actions required for spike close.
- [ ] drax (INFO, non-blocking, next touch): Add dispatch/findings doc path to `TODO(drax)` in `compute-constellation-layout.py` for cold-reader traceability.
- [ ] drax (INFO, Phase B): Add `Cache-Control: immutable` to `constellation_layout.json` at production Vercel deploy time.
- [ ] knight-rider: Surface push-authorization request to Matt for both repos. Collab: `bb9e5f4`. Loadout: `bb7176c`, `e63f667`, `986334d`, `7d411a2`.

---

## Decisions-log determination

**NO new decisions-log entry required.** The grid-layout pivot is a within-spike implementation finding nested inside the already-locked primitive-as-star + kit-as-constellation architectural commitment (`canonical/story/2026-06-05-cosmograph-pivot.md` § 9). The cosmograph-pivot § 9 entry is the correct decisions-log anchor for this workstream. A new entry would duplicate the anchor and add noise without downstream-binding gain. Pattern recurrence in a second workstream (mantis 3D, future season visualizations) is the activation trigger.

---

## References

- `/Users/admin/Games/reincarnated-loadout/src/components/Cosmograph/ConstellationModeCanvas.tsx` — code-level review: rendering-layer isolation, LOD switch, lasso dedup
- `/Users/admin/Games/reincarnated-loadout/scripts/compute-constellation-layout.py` — Python pre-compute: grid layout, UMAP caveat, TODO(drax) annotation
- `/Users/admin/Games/reincarnated-loadout/src/pages/Forge.tsx` — Mode B default verification, lazy layout load
- `/Users/admin/Games/reincarnated-loadout/AGENT_STATE.md` — build evidence, Phase 2 session summary, TODO overrides
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-2-full-corpus-findings.md` — Phase 2 verdict, FPS evidence, substrate-coverage caveat, architectural learning
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-1-sample-findings.md` — Phase 1 baseline, UMAP-degenerate founding instance
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-07-drax-cosmograph-a-b-spike.md` — original dispatch + completion records
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-07-jack-ryan-gate-2-cosmograph-a-b-spike.md` — this review's dispatch
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-05-cosmograph-pivot.md` § 9 — architectural lock anchor
