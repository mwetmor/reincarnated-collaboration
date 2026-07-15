# The Periodic Table of Kits — atlas-chart renderer spec

> **STATUS:** SPEC — authored gandalf 2026-07-11 on Matt's "Go on the renderer spec." Build is
> **HARNESS-GATED**: nothing here fires until the Atlas emission harness exists
> (`canonical/current-to-end-state/projection-atlas.md` §4 — ladder #5, itself behind the emission
> primitive). Registered face: projection-atlas §4 "Named face" bullet + §5 arrival #3 (GO, four
> repairs). **§2 of this spec is written to Matt's plane-lock criteria** (2026-07-11 verbatim: *"I
> will lock them if they are arranged by columns/rows/axes and if the arrangement of the
> columns/rows/axes are purposeful and sensible for the search/exploration of the space"*) — the
> LOCK is Matt's ruling to grant; this spec makes the case and names exactly what the lock covers.
> **r3 amendment 2026-07-15 (§9):** ghost-field layer clauses — fired by Matt's Q30 ruling (Q30a
> amendments ratified + Q30b zero taste cuts). The feasible lattice is now data; §9 binds how it renders.

---

## §0 — The one law everything below serves

**`chart = render(atlas.json)` — emitted, never hand-drawn.** The chart is a *display consumer* of
the Realized Atlas join (`Atlas vN = f(Codex vM, Projection vP)`, projection-atlas §4). No number,
dot, badge, or label on the chart may originate anywhere but an atlas.json field. The renderer
computes LAYOUT, never CONTENT. This is the same provenance law as everything on the mechanical
side: the archive records what the engine DID; the chart shows the archive; nobody draws the truth
by hand.

Two skins, ONE renderer (§5): `instrument` (working surface, Glance-class) and `archive` ("The
God's Archive" devlog dress). Skins are theme parameters over one layout engine — never forks.

## §1 — What the chart IS (grain, restated as binding)

- **The plane is ARCHIVE-grain:** geometry family × commitment. Geometry family = archive Axis 2,
  **BC-MEASURED** (R-3, catalog-blind — emergent from what skills DO, never sampled); commitment =
  the ninth archive axis (`bc_commitment`, L0 6th coordinate, Q-E4-4b). The chart plots kits where
  they **measured**, not where generation aimed — the Archive records what the soul did.
- **The ~972 L0 coordinates live INSIDE cells** as isotope sub-dots — they are not the plane.
- **The number of record is L4 ≈ 1.284×10⁹** (substrate-coordinates §0 grain table). "2.57B" is
  the naive box and appears nowhere.
- **Frames badge ladder levels** (FUN-ladder state, claim level, occupancy, alarms) — badges are
  per-Atlas-version payload; they change; position never does (§2.5).

## §2 — THE PLANE (the lock case)

> **⚠ AMENDED 2026-07-13 — Q19 LOCKED. The plane below (§2.1–§2.x: commitment × geometry, 15 cells) is SUPERSEDED as the ATLAS plane.** Matt ruled Q19 locked ("I rule Q19 as locked"): the atlas plane is now **3 movement rows (FREE-MOVE/WALK/ROOTED, from `mob_policy_while_casting`) × 7 delivery columns (PROJECTILE/ORBITAL/NOVA/ZONE/BEAM/MELEE/SUMMON) × amp-tempo strata (FLAT/SPIKY/VAR)** — see `views/v1-plane/plane-b-prime-lock-addendum.md` §10 (RULED render V1.2) for the authoritative rule + assignment logic (incl. cone Path 2, RING→ORBITAL merge). **Movement × delivery × amp SUPERSEDES commitment × dispersion for the atlas plane.** The commitment and dispersion/geometry axes are NOT demoted — they remain MEASURED substrate archive axes (design-active in GX-19/GX-20), just no longer the atlas browse plane. The §0/§1/§3–§5 provenance laws (chart = render(atlas.json); two skins, one renderer; badges = per-version payload; layout ≠ content) are UNCHANGED and carry forward to the locked plane. The PROMPT-5 harness (arc S3) builds against the locked plane; the §2.1–§2.x prose below is retained as lock-case lineage only.

> **⚠ AMENDED 2026-07-14 — PLANE *DERIVATION* SUPERSEDED by the atlas-derivation charter.** Matt rejected any governance-history-picked plane as the atlas frame ("we have no reason to believe that those rows/columns should in any way govern the periodic table") and adopted a statistically derived basis: `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` + its pre-registration. **The Q19 movement × delivery × amp plane is DEMOTED to a census-dashboard view** (still emitted, still useful — no longer THE atlas plane; the coordinate-register identity-key lock on coords 1–3 is untouched). The atlas plane is now the **Edition-I derived basis** (MCA/CATPCA-family, four validation gates, frozen frame + supplementary projection) — **RATIFIED + FROZEN 2026-07-14** (pipeline executed under prereg v1.1; A/C/D pass; Gate B → Finding F-1; Matt: *"Ratify a"*). **Ratified axis names: dim 1 PERFORM ↔ DEPLOY · dim 2 EMBODY ↔ LAUNCH** — carried in `basis.axis_names`, rendered on both skins. The §0/§1/§3–§7 laws (chart = render(atlas.json); determinism; two skins one layout engine; R1–R4; fail-loud enums) are UNCHANGED and carry to the derived plane. **atlas.json plane block gains:** `basis: {edition, frozen, ratified, method, loadings_ref, inertia_pct, retained_dims, structure_statement, axis_names}` + per-point `{x, y, supplementary: bool}` (+ `death_class` on supplementary points — the F-1 tombstone payload) + ghost-field layer (charter §4) — **landed 2026-07-15 under the Q30 ruling; binding render clauses at §9 (r3)**. Axis names arrive AFTER derivation (placeholders banned). *(RIDER-1, 2026-07-14: `retained_dims` (Edition I: 14) + `structure_statement` ("continuum with condensations, not discrete cells") are MANDATORY badge fields rendered on every chart, both skins, alongside `inertia_pct` — the 2-D view must never present as a faithful summary of the 14-D basis. GRAVEYARD overlay renders per-corpse tombstones with cause-of-death, never shaded danger regions — Finding F-1.)* *(r2 amendment 2026-07-14 — Matt: "we need to add something somewhere explaining what the axes are." Every render, both skins, carries three explainer texts (CONTENT LOCKED; typography/placement per skin): (i) **pole glosses** — one clause under each axis end-label: PERFORM = "you are the weapon — channel · beam · spin" · DEPLOY = "you place the weapon — totem · trap · detonate" · LAUNCH = "damage sent away — projectile · chain" · EMBODY = "damage from the body — spin · aura · dash"; (ii) **density-field legend line** — "shaded field = density of genre kits (settled territory — not a boundary)"; (iii) **derivation gloss** under the badge — "positions computed, not designed — MCA over 13 mechanical coordinates per kit; axes named from the loadings afterward.")*

### 2.1 The frame: 15 cells, both axes already governance-locked

**Rows (3) = `bc_commitment` · Columns (5) = damage geometry (Axis 2).** Arities are not this
spec's to invent: geometry = 5 ratified at the axes-lock (W-C.5); commitment = 3 ratified
(Q-E4-4b). Changing either arity is already a Matt-level re-ratification of locked canon. **The
frame cannot drift by accident — the lock Matt grants adds only the ordering rules below.**

```
                 single      chain      small-AOE    large-AOE    multi-spawn
              ┌───────────┬───────────┬────────────┬────────────┬─────────────┐
   instant    │ the flick │ the spark │ the burst  │ the nova   │ the scatter │
              │  (rogue's │  that     │            │            │             │
              │   dagger) │   leaps   │            │            │             │
              ├───────────┼───────────┼────────────┼────────────┼─────────────┤
   wind-up    │ the aimed │ the forked│ the hurled │ the called │ the seeded  │
              │   shot    │   bolt    │   flask    │   storm    │   field     │
              ├───────────┼───────────┼────────────┼────────────┼─────────────┤
   channel    │ the beam  │ the arc   │ the ground │ the        │ the ritual  │
              │           │  sustained│   flame    │  cataclysm │ (standing   │
              │           │           │            │            │    army)    │
              └───────────┴───────────┴────────────┴────────────┴─────────────┘
```

*(Cell nicknames are illustrative register, not canon labels — canon cell labels are the enum
pairs. The corners are the argument: top-left `instant × single` is the flick; bottom-right
`channel × multi-spawn` is the ritual. The main diagonal is the genre's whole fantasy arc — twitch
to ceremony.)*

### 2.2 Row ordering rule — `commitment-weight-v1`

**instant → wind-up → channel, top to bottom.** The axis is intrinsically ordinal — it has exactly
one honest monotone order, its own definition: how much of yourself you commit before/while the
effect exists. *Instant* commits nothing up front; *wind-up* pays time before; *channel* keeps
paying during. Reading DOWN a column = same damage shape, heavier ceremony. There is no arbitrary
choice here to defend; the rule merely writes down the axis's own arithmetic.

### 2.3 Column ordering rule — `dispersion-v1`

**single → chain → small-AOE → large-AOE → multi-spawn, left to right.** The intrinsic coordinate
is **dispersion** — in how many places the kit's damage exists, ordered lexicographically by
(instantaneous footprint, then total targets touched): one point → one *moving* point (sequential
hops; footprint 1, touch N) → compact region → wide region → many autonomous origins. Reading
ACROSS a row = same ceremony, damage spreading from a point to a field to an army. The order is
robust under both sub-metrics — chain sits second under instantaneous footprint AND under
touch-count; no tiebreak ambiguity exists in the pentad.

### 2.4 Why this arrangement serves search/exploration (Matt's criterion, answered directly)

1. **Gaps are predictions (the Mendeleev property).** With both axes intrinsically ordered, an
   empty cell is a meaningful hole, not a rendering accident — exactly how gallium and germanium
   were predicted from holes in a purposefully-ordered frame. "`channel × chain` holds 0 isotopes"
   is a design prompt legible at a glance. Under an arbitrary order (alphabetical), a hole means
   nothing. **This is frontier enumeration as a picture** — the projection-atlas §4 harness's
   frontier list, drawn.
2. **Every cardinal direction is a design question.** Scan right: "how does this weight class
   express as the footprint grows?" Scan down: "what does this shape cost in ceremony?" The
   diagonal is the power-fantasy escalation the genre runs on — D2's Sorceress lives high-right of
   the Assassin; the summoner's ritual anchors bottom-right of the rogue's flick.
3. **Adjacency = play-similarity.** Neighboring cells differ by ONE step on ONE axis, so *near*
   means *plays similarly* — and one-step exploration ("what's this build but heavier?") is how
   players actually shop. Arbitrary arrangement destroys adjacency-meaning; this one makes the
   metric honest.
4. **Addresses are permanent.** A kit's home ("K17 lives at `channel × multi-spawn`") survives
   every Atlas version, because position = ratified-arity coordinates + these two rules — never
   population statistics. Occupancy, FUN state, claim levels change per Atlas vN and render as
   **badges**; position does not. **Lock the rule, not the raster.**
5. **The lock is cheap and already half-granted.** Both arities are ratified canon; the lock adds
   two ordering rules + one sub-dot rule (§2.6). Growth clause: any future arity change is already
   a Matt-gated re-ratification, at which point the new member enters at its intrinsic coordinate
   (its dispersion / weight value) — existing addresses never renumber, because an address is a
   coordinate value, not a column index.

### 2.5 What moves between Atlas versions — and what it means

The FRAME never moves. **Dots may.** If re-measurement moves a kit to a different cell, the dot
moves — the archive is what-is, and the chart must not lie to protect a prior picture. A
cross-version cell migration is itself SIGNAL (measurement drift → §3 alarm-register adjacency),
and the diff of two Atlas versions reads as dots appearing/moving **in a stable frame** — which is
the entire devlog value of an iconic chart.

### 2.6 Within-cell isotope ordering — `isotope-seq-v1`

Sub-dots order deterministically: **attribute (STR → DEX → INT → WIS) → primary element (canonical
8-order) → remaining archive axes in substrate-coordinates §2 order.** The visual arrangement of
the sequence (grid, arc, spiral) is the renderer's layout choice per skin; the SEQUENCE is locked
so re-renders never shuffle dots and version-diffs stay readable.

### 2.7 The lock — exactly what Matt is ruling on

| LOCKED (this ruling) | NOT locked (per-version payload) |
|---|---|
| Axis assignment: rows = commitment, cols = geometry | Badges: occupancy, FUN-ladder state, claim level, alarms |
| `commitment-weight-v1` row order | Colors, typography, skin dressing |
| `dispersion-v1` column order | Annotation layers, callouts |
| `isotope-seq-v1` sub-dot sequence | Which dots exist (that's the archive's truth per vN) |
| The address scheme (`cell = (commitment, geometry)`) | |

Lean on the one soft fork: 3 rows × 5 columns (landscape) over the transpose — it matches the
periodic-table silhouette, reads on mobile-landscape and desktop, and gives isotope sub-dots
horizontal room. The transpose (5 rows × 3 cols) is workable but cramps cells; named for
completeness, not advocated.

## §3 — The four repairs, bound as renderer LAWS

| # | Repair (Matt-GO 2026-07-11) | Binding form |
|---|---|---|
| R1 | **Grain labels** | Legend states the plane is ARCHIVE-grain (measured), geometry family BC-MEASURED (R-3); the ~972 L0 live in sub-dots. A chart without the grain legend fails acceptance. |
| R2 | **Number of record** | Search-space callout renders the emitted L4 integer (≈1.284×10⁹) verbatim from atlas.json. The string "2.57" must not appear (grep-testable). |
| R3 | **Atlas-version framing** | All version chrome is `Atlas vN — f(Codex vM, Projection vP)`. No season-N strings anywhere on either skin (grep-testable; retired-canon guard). |
| R4 | **Canon enums only** | Every enum string on the chart comes from atlas.json and pins to canon vocabularies: commitment + geometry + archive axes (substrate-coordinates §2), FUN ladder (§7), alarm registers (projection-atlas §3). Unknown enum member → renderer REFUSES loud (Discipline #8) — an unknown value means vocabulary moved without re-ratification; that is an alarm, not a bucket. |

## §4 — atlas.json contract (input; emitted by the harness, ladder #5)

Sketch — the harness owns the authoritative schema; the renderer validates against it:

```
{
  "atlas_version": "v1",
  "inputs": { "codex_version": "vM", "projection_version": "vP",
              "engine_commit": "<sha>", "emitted_at": "<iso8601>" },
  "counts":  { "l0_coordinates": 972, "l4_search_space": <exact integer of record> },
  "plane": {
    "rows": { "axis": "bc_commitment",   "order": ["instant","wind_up","channel"],
              "rule_id": "commitment-weight-v1" },
    "cols": { "axis": "damage_geometry", "order": ["single","chain","small_aoe","large_aoe","multi_spawn"],
              "rule_id": "dispersion-v1" }
  },
  "cells": [ { "row": "channel", "col": "multi_spawn",
               "badges": { "occupancy": <int>, "fun_state": "<FUN-ladder enum>",
                           "claim_level": "<claim enum>", "alarms": [ "<§3 register enums>" ] },
               "isotopes": [ { "kit_id": "K17", "l0": { ...six coords... },
                               "claim": "...", "seq_key": "<isotope-seq-v1 tuple>" } ] } ]
}
```

Contract laws: (a) the renderer **refuses** unversioned input or unknown enums (fail-loud); (b) the
plane block's `order` arrays must equal the locked rules — a mismatch is a HALT, not a reorder;
(c) `counts` come from the emitter — the renderer never sums isotopes to derive a displayed count
(no-hand-derived-numbers law; occupancy badges render the emitted field even though the sum is
checkable — checking is a TEST, not a render path).

## §5 — The renderer

- **Home:** Python, engine-side `export/` seam (**star-lord**) — first-class module in the
  `measurement_report_writer.py` mold (own module, not a flag on something else).
- **Output:** standalone SVG artifact + stamped footer (`Atlas vN · f(Codex vM, Projection vP) ·
  engine <sha> · emitted <iso8601>` — all from atlas.json). Same-commit stamp law applies when the
  artifact lands anywhere Matt-facing.
- **Deterministic:** same atlas.json → byte-identical SVG. Sorted iteration everywhere; no
  wall-clock reads (time comes from `emitted_at`); no RNG. Test: render twice, `diff` — byte-equal.
- **Two skins, one layout engine:** `--skin instrument` (quiet Glance-class working surface,
  mobile-legible) · `--skin archive` (the God's Archive devlog dress — the ledger a long-lived
  being keeps of every soul's measured deed). Skins may vary palette, typography, dressing, dot
  glyphs; they may NOT vary layout, ordering, or content. One layout code path, asserted by test
  (both skins render the same cell/dot coordinate set).
- **No interactivity here:** the SVG is static truth. Interaction is drax's layer (§6).

## §6 — Seam contract

| Seam | Owns | Does NOT own |
|---|---|---|
| **star-lord** | atlas.json emitter (the §4 harness), the renderer module, the SVG artifact | HTML interactivity; Glance page composition |
| **drax** | Interactive HTML wrapper: hover isotope → L0 tooltip; tap cell → deep links into Glance `/coordinates` + `/mechanics` section anchors. **Consumes the same atlas.json** — never scrapes the SVG, never re-derives content | The emitter; the renderer; any content derivation |
| **Glance** | v1.10-class amendment, **HARNESS-GATED** — §7.7 rule 7 is already holding the door (no occupancy numbers until the harness exists). The chart page enters the contract only when atlas.json is real | — |
| **gandalf** | This spec; DRIFT-CRITIC review of the first render against it | Any code |

## §7 — Acceptance criteria (build-time, all testable)

1. Determinism: two renders of one atlas.json are byte-identical.
2. Provenance: every displayed number/string traces to an atlas.json field (audit: no literal
   numerics in renderer source beyond layout geometry).
3. R2/R3 greps clean: no "2.57", no season-N strings, in either skin's output.
4. R4 refusal: a doctored atlas.json with an unknown geometry enum → loud non-zero exit, no SVG.
5. Plane conformance: a doctored `order` array (rule mismatch) → HALT, no silent reorder.
6. Skin invariance: both skins emit identical cell/dot coordinate sets (layout-equality test).
7. Grain legend present (R1) + version footer present, stamped from input.
8. Empty-cell rendering: zero-occupancy cells render as explicit frontier (visible empty frame),
   never collapsed out of the grid — the gaps ARE the point (§2.4.1).

## §8 — Sequencing (what this spec does and does not authorize)

This spec **authorizes nothing to fire.** Build order stands: emission primitive → Atlas emission
harness (projection-atlas §4, ladder #5) → **this renderer as the harness's first consumer** →
drax HTML layer → Glance v1.10-class amendment. Zero collision with E4 PHASE-2, batch-2, or the F5
math note — different seams, later rung. When the harness lands, KR dispatches star-lord against
§4–§5 + §7 of this spec; gandalf takes the DRIFT-CRITIC pass on the first artifact.

**Matt ruling requested (the lock):** §2.7 table — axis assignment + `commitment-weight-v1` +
`dispersion-v1` + `isotope-seq-v1` + the address scheme. Matt's pre-stated criteria are answered
at §2.4; if the case holds, the lock makes the chart iconic-by-never-rearranging from its first
public frame.

## §9 — r3 amendment (2026-07-15): the ghost-field layer

> Fired by Matt's Q30 ruling (2026-07-15 — Q30a cut-predicate amendments L1′/L4″/RED-3′ RATIFIED;
> Q30b ZERO taste cuts). Data source: elrond's register **v1.1** + ghost-field emission (charter
> §4). Audit-of-record + corrected ladder:
> `agentic_orchestration/gandalf/design-inputs/2026-07-15-feasibility-register-audit-and-taste-slate.md` §3.

### 9.1 atlas.json gains the ghost block (contract extension)

```
"ghost_field": {                          // AS EMITTED (elrond d0b2a025) — authoritative over
  "version", "register_ref",              //   the r3 draft sketch, per §4 preamble
  "basis_ref", "frozen_fit_input",        // decoupling-law provenance (pre-C3 frozen-fit snapshot)
  "grain", "core_order": [7 core coords], "projection", "red3_note",
  "denominators": { exact_raw_naive, exact_post_logical, exact_post_red_law: 693146160,
                    meso_raw, meso_feasible: 10080, meso_sealed: 1260 },
  "depth_by_delivery": { MELEE: 55755, PROJECTILE: 55755, <others>: 74340 },
  "depth_sum_check": 693146160, "lit_cells": 192,
  "unmapped_pending_curation": 14, "unmapped_pending_curation_kits": [...],
  "unmapped_would_seal_excluded": 0, "unmapped_would_seal_kits": [],
  "feasible_cells": [ 10080 × { "core": [7-tuple], "depth", "kit_count", "lit", "x", "y" } ],
  "sealed_cells":   [ 1260  × { "core": [7-tuple], "cut_id": "L1-…|L2-…" } ]
}
```

*(Sealed cells carry `cut_id` (L1/L2 only — the `red-law` refusal in (c) binds on this field) and
NO coordinates — sealed ground is never projected; it renders in a legend/margin register, not on
the plane. Note the coincident-projection reality: cells differing only on coords outside the fit
vocabulary project to identical (x,y) — the renderer must aggregate coincident ghost glyphs
deterministically (multiplicity glyph or size step from emitted positions), never RNG-jitter.)*

Laws:

- **(a) Ghosts are zero-mass.** Ghost cells enter the plane as CA supplementary projections onto
  the FROZEN Edition-I basis — axes never move (decoupling law, charter §2). A ghost block whose
  presence changes any basis field or any of the 506 point coordinates is emitter malfunction →
  HALT.
- **(b) Positions frozen, lighting census-current.** Lit-mapping keys the CURRENT corpus at
  emission (post-ingestion keys, incl. the 9 `control×none`→`damage×none` treatment
  re-classifications — elrond C3, evidence-judged) — the documented
  hybrid. A mandatory legend line states it: *"ghost field lit from the current census; positions
  from the frozen Edition-I basis."* Kits whose keys resolve to no feasible cell are counted in
  `unmapped_pending_curation` and excluded — never force-lit.
- **(c) Meso seal-cause is ALWAYS logical.** The 1,260 sealed meso cells are L1′ + L2 composed
  (756 + 504), carried in `cut_id` (`L1-treatment-function-coherence` / `L2-summon-implies-proxy`).
  RED-3′ seals exact-grain ground that does not surface at meso grain (the emitted `red3_note`
  states this; depth badges already net out RED-3′ within-cell) — a sealed cell whose `cut_id` is
  outside the {L1-, L2-} set is an unknown-enum-class error → renderer REFUSES loud (R4).
  Drill-in/tooltip copy naming seal causes cites `cut_id` verbatim.
- **(d) Depth is emitted, never derived.** `depth` per cell (delivery∈{MELEE, PROJECTILE} →
  55,755; all others → 74,340; Σ over 10,080 = 693,146,160 exactly). The Σ-check is an EMITTER
  test; the renderer renders the field (§4c no-hand-derived-numbers law).

### 9.2 Render semantics — figure-ground, not data

1. **Layer order (bottom → top):** unlit ghost marks → density field → points → tombstones →
   badges/chrome. The ghost field is GROUND beneath everything that already exists. **Sealed
   cells render OFF-plane** (see 4) — the plane shows only ground that can exist.
2. **Glyphs, never regions.** Ghost cells render as small per-cell glyphs at their projected
   coordinates — **no Voronoi fills, no area hatching, no painted boundaries.** The 2-D view is a
   lossy shadow of the 14-D basis (RIDER-1's `structure_statement`: continuum, not discrete
   cells); painting regions would assert boundaries the basis does not claim — the same
   over-claim discipline as F-1's no-danger-regions rule.
3. **Unlit-feasible** = the dark of the map: faint near-ground marks (skin-tuned), visually
   subordinate to points and density. The chart's story is the point: *settled territory is a lit
   archipelago in a vast feasible dark.*
4. **Sealed = a margin/legend LEDGER, never on-plane marks.** The emitted sealed cells carry no
   coordinates (correct: a position claim for un-designable ground is one no kit will ever
   measure to validate — the F-1 over-claim discipline). Render as a chrome register: *"1,260
   meso cells sealed — L1′ treatment–function coherence 756 · L2 summon⇒proxy 504"*, cut ids
   verbatim from `cut_id`; drill-in may list tuples. The plane itself shows only feasible ground.
5. **Depth badges** render `depth` in the skin's compact-number style (order-of-magnitude
   acceptable on `instrument`; exact on drill-in).
6. **Coverage callout** renders from emitted fields only: *469 active ≈ 6.8×10⁻⁵ % of 693,146,160
   feasible exact-grain kits.* R2-extension greps: the superseded denominator string
   **"422,445,240" must not appear**; "900,169,200" may appear ONLY labeled as the pre-cut naive
   box, never as denominator.
7. **Tombstones:** the 12 death_class fills render as cause-of-death labels. F-1 unchanged —
   per-corpse tombstones, never danger shading. RIDER-1 badge + the r2 explainer trio
   (content-locked) carry forward verbatim.

### 9.3 Acceptance extensions (adds to §7)

9. **Frozen-layer regression:** ghost-ON render vs the r2 baseline artifact — basis block + all
   point coordinates byte-identical; the ONLY permitted diffs in pre-existing layers are (i) the
   12 tombstone death_class label strings, (ii) coverage-callout numerals re-sourced from the
   new denominator field, and (iii) the footer version stamp (`emitted_at` is provenance and is
   necessarily fresh on re-emission). Everything else new must be strictly additive (the ghost
   layer).
10. **Seal-cause conformance:** doctored sealed cell with `cut_id` outside the {L1-, L2-} set
    (e.g. a red-law id) → loud non-zero exit, no SVG.
11. **Grep set extended:** no "422,445,240"; explainer-trio strings present verbatim; RIDER-1
    fields rendered on both skins.
12. **Skin invariance extended:** both skins emit identical ghost-cell coordinate + status sets.

---

**Signed:** gandalf, 2026-07-11 — SPEC-AUTHOR. Anchors: `projection-atlas.md` §0/§3/§4/§5 ·
`substrate-coordinates.md` §0/§2/§7 · axes-lock (W-C.5) · Q-E4-4b · Matt GO + lock-criteria
messages 2026-07-11. **r3:** Q30 ruling 2026-07-15 · atlas-derivation-charter §2/§4 ·
feasibility-register audit §3.
