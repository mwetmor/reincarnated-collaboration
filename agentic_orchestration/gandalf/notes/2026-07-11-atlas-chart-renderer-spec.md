# The Periodic Table of Kits — atlas-chart renderer spec

> **STATUS:** SPEC — authored gandalf 2026-07-11 on Matt's "Go on the renderer spec." Build is
> **HARNESS-GATED**: nothing here fires until the Atlas emission harness exists
> (`canonical/current-to-end-state/projection-atlas.md` §4 — ladder #5, itself behind the emission
> primitive). Registered face: projection-atlas §4 "Named face" bullet + §5 arrival #3 (GO, four
> repairs). **§2 of this spec is written to Matt's plane-lock criteria** (2026-07-11 verbatim: *"I
> will lock them if they are arranged by columns/rows/axes and if the arrangement of the
> columns/rows/axes are purposeful and sensible for the search/exploration of the space"*) — the
> LOCK is Matt's ruling to grant; this spec makes the case and names exactly what the lock covers.

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

---

**Signed:** gandalf, 2026-07-11 — SPEC-AUTHOR. Anchors: `projection-atlas.md` §0/§3/§4/§5 ·
`substrate-coordinates.md` §0/§2/§7 · axes-lock (W-C.5) · Q-E4-4b · Matt GO + lock-criteria
messages 2026-07-11.
