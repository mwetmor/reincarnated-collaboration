# Tier-3 refit candidate + Edition-III polish pass — ultra-think record

**Date:** 2026-07-16 · **Author:** gandalf (SPEC-AUTHOR/ARCHITECT) · **Status:** execution spec, both workstreams fired this session
**Authority:** Matt 2026-07-16 (verbatim): *"Let's keep Edition 3, and then run the full Tier 3 with Last Ark and Pull/Gravity. It's important that we get this right, and I want to see both versions so we cna make a decision. Ultra-Think and take as long as you need and run autonomously, calling sub agents as needed to complete Tier 3. In parallel, can you please have one small set of last changes to Edition III? Currently the app fits screen size and the "box" is zoomed appropriately, but the legends/descriptive sections/title/axis-title/axis itself are all still set to fill the "box" that has now grown. So, they need to fit the box as it is now. Lastly the clickable legend should fit inside the box on the upper-left-hand side, opposite to the "Condensations" box (and the condensations box should be re-named to "Build Families"."*
**Companion:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §6–§7 · `agentic_orchestration/gandalf/notes/2026-07-15-atlas-interactive-glance-spec.md` (glance instrument spec, §9.x pass ledger)

---

## 0. TL;DR

- **Workstream A (Tier 3):** full re-derivation of the atlas fit on the CURRENT active corpus (N=628, incl. 62 Lost Ark + pull as a live feature column), emitted ALONGSIDE Edition III as **`Refit Candidate 1`** — a comparison artifact, NOT an Edition. Edition III stays served and byte-untouched. elrond runs the pre-registered methodology unchanged (same script forked, same SEED); galadriel renders the candidate plates with the SAME furniture head as the polished Edition III so Matt compares structure, not presentation.
- **Workstream B (polish):** B-1 galadriel re-scales plate FURNITURE (title/banner/axis titles+glosses/legends/ledger/footer/key boxes) for the post-D7 fluid-width display — data geometry byte-frozen; key header renamed `CONDENSATIONS` → `BUILD FAMILIES`. B-2 drax re-vendors, moves the clickable legend to the **top-left plane seat** (mirror of the top-right key), renames its `Condensations` entry → `Build Families`, re-runs the v2 occlusion law at 5 widths × 2 skins.
- **Sequencing law:** B-1 → (B-2 ∥ A-render). The refit plates MUST render from the B-1 furniture head (apples-to-apples). elrond's derivation runs in parallel with B-1 from the start.

## 1. Charter positioning (the naming law)

Charter §6: frozen frame, versioned occupancy; structure change = numbered Edition, rare, evidence-gated by §7 (sim falsification — un-run). Matt has ordered a comparison **experiment**, not (yet) an Edition. Therefore:

- The artifact is **`Refit-Candidate-1`** (`atlas-refit-candidate-1.json`, plates `atlas-refit-candidate-1-{instrument,archive}.svg`). The string "Edition IV" appears NOWHERE.
- Edition III remains the served truth at every layer (PRD `/atlas`, atlas-edition3.json, plates, slim JSON).
- If Matt adopts the candidate after comparison, adoption ratifies it as Edition IV by Matt's authority; the §7 sim-falsification remains un-run at that moment and is recorded as an explicit waiver in the adoption note. My comparison package will carry that flag.
- The refit changes the **FIT layer only.** The register/feasibility lattice (v1.3) does not move: denominators 767,411,820 / 11,160 meso / 1,314 sealed / pull 1,080+54 stay byte-identical. Corpus census unchanged (no new rows this pass).

## 2. Refit input facts (gandalf recon, corpus.db 2026-07-16)

- Active predicate (`combat-kit` ∧ `cell_key NOT NULL` ∧ `negative=0`) → **N = 628** (Edition-I fit was 469).
- **Game-code split brain:** active set carries long-form codes `lost-ark` (62), `diablo-4` (1), `diablo-3` (1), `diablo-immortal` (1) alongside the short codes; `game='la'` count is **0**. The derivation script's `FRANCHISE_ROLLUP` knows only short codes → its stage-0 orphan check HALTs today. Normalization (elrond's parked to-do) is now load-bearing → refit step R0.
- `mcd` = 94 active rows (largest single game) — absent from `FRANCHISE_ROLLUP` → must be added.
- **Pull:** function=pull active count = **10 = FUSE_MIN exactly.** Zero margin: survives Greenacre fusing by the letter of `n<10 fuses`. Asserted pre-fit; if it fuses the run's purpose dies → HALT, never lower FUSE_MIN unilaterally.
- **Projectable negatives = 37** (unchanged) — the graveyard tombstone count carries over.
- Melee: `LIKE '%|melee|%'` returns 271 but collides with range=melee — per-field parse required; if delivery=melee reaches n≥10 it earns a fit column and the MELEE ghost-image collapse may partially close (report, don't engineer).
- Gate-A labels: same 86-kit CSV; all 86 are in the 628.
- Condensations ride automatically: the six groups are `gateA_group` on the points; labels carry over, anchors/centroids re-derive mechanically. No re-curation needed for the comparison.

## 3. The decision surface (how Matt sees both)

Static plates + a numbers report — structure is the question; interactivity follows adoption, not precedes it.

1. **Plates:** Edition III (post-B-1 furniture) vs Refit Candidate 1 (same furniture head), both skins.
2. **Comparison report** (elrond emits, I verify + synthesize): Procrustes congruence + RMS displacement on the 469 shared actives, top-20 movers, axis-identity correlations (did LAUNCH/EMBODY + PERFORM/DEPLOY survive?), inertia/retained-dims delta, LA landings with neighbors, the 10 pull kits at honest coordinates (do they cohere?), fuse-table delta, gates A–D old-vs-new, ghost-field deltas (pull cells masked→honest, unmapped/off-plane changes), **and the beyond-horizon census on the refit plane** (brief R3-ADDENDUM, Matt follow-up 2026-07-16): hull/beyond-horizon/P-DF-1 recompute automatically; the drill-in's EAST-half region pin does NOT — axis signs align to Edition-I orientation first, the pinned region re-runs verbatim, and the census reports uncovered overshoot directions. If new overshoot opens outside the pinned region, the candidate gets a drill-in-expansion pass BEFORE the package reaches Matt (comparability law: Edition III got its drill-in; an un-drilled candidate would read unfairly sparse at its frontier).
3. Delivery: side-by-side composite + full plates as receipts; a glance compare page only if Matt asks after seeing the static package.

## 4. Workstream B split (diagnosed)

Everything Matt lists as oversized is **in-SVG furniture** (galadriel's render head): title 26px internal (renders ~41px at 2560 display, scale ≈1.58), RIDER 13, glosses 11/9.5, pole titles 15, key rows 11, plaque/ledger/footer 8–11. The clickable legend is the HTML `AtlasLegend` overlay (currently bottom-right, 14.5%-width law) — drax's seam.

- **B-1 (galadriel):** furniture-only re-scale, data marks byte-frozen (incl. † tombstones at font-16 — the acceptance regexes key on it). Target: comfortable UI scale at 2560 viewport (title ≈24–30px rendered; rows ≈12–14px; poles ≈14–18px; glosses ≈10–12px ⇒ global furniture factor ≈0.6–0.65 with per-class judgment), floor: legible at 1440. Boxes (title band, key box 196w, ghost plaque 420w, ledger) hug their shrunken text. Rename key header `CONDENSATIONS` → `BUILD FAMILIES`. Both skins; fork script per series convention (r8-furniture).
- **B-2 (drax, after B-1):** re-vendor R8 SVGs; `AtlasLegend` moves to the top-left plane seat (mirror of the top-right key; below the title/banner band, clear of the left-rail rotated titles — seat derived by probe, fraction-anchored); rename legend entry label `Condensations` → `Build Families` (display string only — `LegendClass` id, data keys, `condensation` field names unchanged); mobile chip seat re-derived; v2 occlusion law re-verified (hardened probe, 2560/1920/1440/1280/375 × both skins); build + suite + preview; STOP at preview.

## 5. Sequencing + verification

```
elrond R0–R5 (derivation, background) ──────────────┐
galadriel B-1 (furniture re-scale) ─→ drax B-2 ─→ my verify ─→ promote polish (standing chain)
                       └─→ galadriel A-render (refit plates, R8 head) ─→ my verify ─→ comparison package → Matt
```

My verify gates every promotion (standing chain). NO push this cycle (batch list restarts post-push). Auto-commit in-scope artifacts per team discipline.

## 6. Held decisions (surfaced, not resolved here)

- Adoption fork (Edition III vs Refit Candidate 1) — Matt's, after the package.
- If adopted: Edition-IV ratification note + §7 waiver record + serving-layer cutover (slim JSON, vendored SVGs, displacement/condensation re-derivations against the new basis) — separately scoped wave.
- Display-name map upgrade ("Lost Ark" vs "La") becomes load-bearing at adoption (LA enters the served kit list/slicer).
- MELEE meso-image register gap (v1.4, Matt-gated) — unchanged by this pass unless the refit's melee column closes it empirically (report only).

---

**Tracker-delta:** new open decision (Refit Candidate 1 vs Edition III adoption fork) + two in-flight work items → `current-to-end-state-engine.md` SESSION-DELTA on wave close.

**Signed:** gandalf — operationalizing Matt's Tier-3 comparison order + Edition-III polish order; my verify gates all promotions.
