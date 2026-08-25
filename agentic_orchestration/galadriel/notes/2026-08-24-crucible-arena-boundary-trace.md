# Crucible-of-the-Dead arena boundary trace — (h-a′) baton row

> **STATUS:** CURRENT
> **Date:** 2026-08-24
> **Author:** galadriel (visual-perception + benchmark steward)
> **Authority:** conductor ruling **R-L64-1**, KC2 MODEL-COMPLETION run charter
> `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`
> (ledger rows L-49 · L-59 · L-64)
> **Input:** `agentic_orchestration/galadriel/captures/2026-08-24-crucible-arena-perimeter/`
> — 21 captures, `Screenshot (612).png` … `Screenshot (632).png`, 1920×1080,
> continuous perimeter walk 22:48:38 → 22:50:49 local (131 s), SHA-256 verified at L-64.
> **Machine-readable output:** `crucible-arena-geometry-v1.json` (beside this file)
> **Figure:** `crucible-arena-trace-figure.png` (beside this file)
> **Pipeline:** `agentic_orchestration/galadriel/pipeline/gd_arena_*.py`, `gd_green_zones.py`,
> `gd_footprint_vote.py`, `gd_boundary_extract2.py`, `gd_zone_occupancy.py`

---

## 0. TL;DR

**Class 1 — HARD BOUNDARY: TRACED, and it came in stronger than the ask.**
177-vertex outer ring plus **4 interior obstruction rings**, in an arena-local frame,
registered globally from the minimaps. Registration is not merely adequate — it is
*checkable*, and it checked: 17 of 20 stations agree to ≤2 px between two independent
registration routes, and every one of the six load-bearing stations is confirmed by
3–4 separate anchors with ≤0.7 px spread. **No segment of the boundary is INTERPOLATED.**
Zero of 1755 boundary pixels abut an unobserved region. Matt's walk fully enclosed the
arena in minimap coverage.

**Class 2 — GREEN SPAWN ZONES: PARTIAL. Positions measured, extents NOT.**
Six mutually distinct zones are *demonstrated* — 15 of 15 pairs separated on evidence.
Each ships as a measured interior point with a measured **upper bound** on its radius.
Their **outlines are not traceable from this capture set**, and I have not drawn them.
The reason is specific and is stated in § 5; this is an honourable pause on one facet
of one class, not on the class.

**Damage corroboration of Matt's attestation: 5 of the 6 in-zone stations show a
depressed health readout.** The sixth (622) shows full health — reported, not explained.
**No DoT magnitude is derived here.** It ships `ATTESTED-UNMEASURED`, per L-64.

**The metre scale is the weakest thing in this file.** The geometry is measured in
*minimap pixels*; the metre conversion carries a ~1.7× uncertainty factor and is marked
`DERIVED-WEAK`. Consumers who need metric truth should pin it against the sim-side
occupancy hull — deliberately not done here (that is the conductor's fold).

---

## 1. Method

### 1.1 The instrument the capture set actually offered

The capture spec asked for a perimeter walk with a character-at-edge scale anchor. What
the shots *also* carry — noted at L-64 as a bonus — turned out to be the load-bearing
instrument: **the HUD minimap is a north-up, rigidly player-centred disc.** Two facts
make it a survey instrument rather than a decoration:

1. The disc centre **is** the player. Fitted from the bright ring of shot 612 by
   iterative algebraic circle fit (luminance > 110, gated to |d−r| < 0.1r): centre
   **(1771.98, 172.63)** full-frame px, ring radius **126.63**, usable map content to
   r = 119. The gold player arrowhead sits on that centre to within a pixel.
2. The mapped arena terrain inside it is a **fixed world-space image that merely
   translates** as the player moves.

So the arena footprint can be recovered by registering the discs to each other, and the
registration offset *is* the player's arena-local position. No camera model is required.

### 1.2 Global registration

Masked normalised cross-correlation (Padfield's formulation, FFT) on the disc content,
with the player arrowhead (r < 10 px) and the gold "N" ornament (r > 95, ±11° of north)
masked out, and a ≥30 % overlap floor.

Sequential chain, shot *n* → *n*+1: **NCC peaks 0.832–0.948**, all 20 links.

**Sign convention was not assumed — it was verified by eye.** The masked-NCC offset is the
player's displacement, confirmed against three magnified minimaps: in 617 the arena mass
lies NE of the marker (player SW), in 620 due N (player S), in 623 NW (player SE). All
three match the sign as adopted.

**Drift check (independent route).** Every shot was *also* registered directly to shot
612. For 17 of 20 the two routes agree to ≤ 2 px. Three disagree — 618, 620, 623 — and
those three are exactly the shots whose minimap is flooded by green bleed, where the
direct NCC collapses (0.169–0.255) while the sequential NCC does not (0.843–0.918),
because neighbouring shots share the same wash. For those three I did **not** take the
chain on trust: each was re-registered against 4 independent well-anchored stations.

| shot | anchors | consensus position | spread |
|---|---|---|---|
| 618 | 615, 616, 617, 619 | (−66.5, 127.5) | (0.5, 0.5) |
| 620 | 617, 619, 621, 622 | (−7.0, 152.2) | (0.0, 0.4) |
| 623 | 621, 622, 624, 625 | (67.0, 135.0) | (0.0, 0.7) |
| 614 | 612, 613, 615 | (−65.0, −15.0) | (0.0, 0.0) |
| 626 | 624, 625, 627 | (74.3, −7.3) | (0.5, 0.5) |
| 622 | 621, 623, 624 | (49.0, 99.0) | (0.0, 0.0) |

The direct-to-612 disagreements were the outliers; the chain was right.

### 1.3 Footprint segmentation — and why the obvious method fails

The GD minimap disc is **semi-transparent**: outside the painted terrain, the live world
view bleeds through. Thresholding the registered mosaic therefore *leaks* — the bleed is
warm stone and scores like mapped terrain. The first extraction pass did exactly that and
wandered halfway to the canvas edge. That render was discarded, not shipped.

The bleed is however **different in every shot** (it is the live view, and the player
moved), whereas the painted overlay is identical in every shot that sees a given arena
pixel. So: classify *inside each shot independently*, register, and take the per-pixel
agreement rate `p = votes / observations`. The result is sharply bimodal —
**27 684 px at p > 0.95** and **17 334 px at p < 0.05** — with a clean valley. Threshold
p > 0.65, obs ≥ 3; keep the connected component containing the player's own track;
fill sub-60 px speckle; Moore-neighbour contour walk; Douglas–Peucker ε = 1.5 px.

### 1.4 One correction worth recording

The first obstruction extraction returned **7** interior rings. Three of them (61, 61,
60 px, all 8×8) sat **1.1–1.2 px** from a detected teal pedestal gem, with median colour
RGB ≈ (45, 102, 105) — bright, blue-dominant. Those are **HUD icons drawn over the map**,
which read as unpainted to a terrain classifier. They are not walls. They are now rejected
by colour test and returned to the floor. The surviving four have median colour (27, 26,
21) and (8, 10, 10) — dim and neutral/warm, i.e. genuine unpainted void — at p = 0.00–0.28
across 14–19 observations.

Had I not run that check, the Godot arena would have grown three phantom pillars.

### 1.5 Per-shot coverage map

All 21 stations, arena-local (minimap px, +x east, +y south, origin = shot 612):

| shot | clock | arena (x, y) | in zone | shot | clock | arena (x, y) | in zone |
|---|---|---|:--:|---|---|---|:--:|
| 612 | 22:48:38 | (0, 0) | – | 623 | 22:50:05 | (67, 135) | **yes** |
| 613 | 22:48:42 | (−29, 5) | – | 624 | 22:50:10 | (67, 60) | – |
| 614 | 22:48:53 | (−65, −15) | **yes** | 625 | 22:50:14 | (59, 26) | – |
| 615 | 22:49:01 | (−63, 35) | – | 626 | 22:50:18 | (74, −7) | **yes** |
| 616 | 22:49:27 | (−61, 55) | – | 627 | 22:50:23 | (25, 6) | – |
| 617 | 22:49:31 | (−54, 85) | – | 628 | 22:50:28 | (16, 39) | – |
| 618 | 22:49:36 | (−67, 127) | **yes** | 629 | 22:50:37 | (−19, 35) | – |
| 619 | 22:49:42 | (−23, 107) | – | 630 | 22:50:41 | (−19, 85) | – |
| 620 | 22:49:47 | (−7, 152) | **yes** | 631 | 22:50:45 | (21, 84) | – |
| 621 | 22:49:58 | (26, 103) | – | 632 | 22:50:49 | (1, 65) | – |
| 622 | 22:50:02 | (49, 99) | **yes** | | | | |

The circuit runs N → W → SW → S → SE → E → back to N across 612–627, then five interior
stations (628–632). Clock values are eye-read from the in-frame clock.

### 1.6 Scale derivation — stated as the weak link it is

Native measurement unit is the **minimap pixel**. Converting to metres needs the
ground-plane matrix M (screen px per minimap px), and **M is not recoverable from this
capture set** (§ 5.1). The chain I could assemble, with every term's uncertainty:

| term | value | band | source |
|---|---|---|---|
| s (screen px per minimap px, E–W) | 14.6 | 12.6–16.6 | north-gate landmark displacement 612→627: minimap Δ (25, 6) px against screen Δ (366, 90) px. **Eye-measured, parallax-contaminated** (the gate is an elevated structure). |
| character pixel height | 70 | 58–82 | measured at the player's locked screen position; heavily obscured by a persistent aura VFX |
| character height (m) | **1.9 ASSUMED** | 1.8–2.0 | stated assumption. *Corroborating, not importing:* the D-5b decode of `NavManager::SetDefaultConfig` reports agent height 2.0, consistent with a 1.8–2.0 m player model. |
| cos(camera pitch) | 0.50 | 0.34–0.64 | θ ≈ 60° assumed; bracketed 50–70° by two weak independent reads (the 612→627 north/east ratio, and the aspect of the central dais if it is square) |

**u = 0.198 m per minimap px, band [0.094, 0.366].**

That is a ~1.7× factor either side. Every metre figure in the JSON inherits it; the
native-px geometry does not. The named remedy is one measurement away: registering this
footprint against the sim-side derived occupancy hull, which carries real metric extents,
pins u exactly. **That reconciliation is not performed here** — R-L64-1 reserves it, and
the charter says count only.

---

## 2. Class 1 — HARD BOUNDARY

`provenance: MEASURED-APPROXIMATE-FROM-REFERENCE`

| quantity | native (minimap px) | metres (at u = 0.198, ±1.7×) |
|---|---|---|
| outer ring vertices | 177 | — |
| bbox | x [−98, 103], y [−101, 168] | — |
| extent (E–W × N–S) | 201 × 269 | 39.8 × 53.3 |
| walkable floor area | 27 875 px² | 1149 m² |
| interior obstruction rings | 4 | — |

**Shape.** A near-circular central body with an inner wall pair, four diagonal wing lobes
(NW, NE, SW, SE), east and west alcoves carrying the two vendor/NPC fixtures, a south
lobe, and a north corridor terminating in a small chamber at the gate — the "Master of the
Crucible" red door of shots 612 and 627.

**Interior obstructions.** These are enclosed *unpainted islands inside the floor*. Grim
Dawn's minimap paints walkable floor only, so an enclosed unpainted island is impassable
geometry. That inference is explicit and is the one non-trivial reading in Class 1.

| id | area px² | centroid | extent | reading |
|---|---|---|---|---|
| OB-1 | 309 | (−51.1, 53.6) | 10 × 44 | west inner wall arc |
| OB-2 | 284 | (53.9, 59.5) | 11 × 45 | east inner wall arc |
| OB-3 | 67 | (4.2, 134.3) | 9 × 7 | south-lobe block |
| OB-4 | 62 | (−14.5, 131.2) | 7 × 10 | south-lobe block |

OB-1 and OB-2 are near-mirror-symmetric about the arena's N–S axis at 10×44 and 11×45 px.
Threshold noise does not produce two symmetric 45-px bars; this is architecture.

**This is the class the Godot runtime clamp applies to.**

### Uncertainty — per vertex

**±2.5 minimap px (≈ ±0.5 m at u = 0.198)**, composed of:

- **registration residual ±1 px (1σ)** — empirical, from the multi-anchor cross-checks in
  § 1.2 (spread ≤ 0.7 px) and the 17/20 agreement at ≤2 px between two independent routes;
- **minimap edge softness ±2 px** — the painted terrain edge is antialiased and the
  vote threshold sits on a gradient.

Not a modelled guess: both terms are measured off this capture set.

Boundary witness density: **minimum 3 minimap observations per vertex, median 13.**

---

## 3. Class 2 — GREEN SPAWN ZONES

`class: ENTERABLE DAMAGE FIELD — NOT A WALL`
`geometry provenance: INTERIOR-POINT-MEASURED / EXTENT-UNMEASURED`

Per Matt's L-64 attestation the character can enter these at a severe immediate DoT
price. **The Godot arena must not collide-block them.** Kiting through a spawn zone at a
cost is a legal referent play, and blocking it would lose the referent's movement feel.

Detection needs no camera model: the camera is rigidly player-locked (the floating health
bar sits at exactly x[924, 996], y[428, 430] in every uncontaminated shot), so "is the
player standing in a field" is a fixed-screen-position question. Occupancy = green-field
pixel fraction within r < 60 px of the player's feet.

| id | witness shot | interior point (native) | radius **upper bound** | bounded by |
|---|---|---|---|---|
| Z-614 | 614 | (−65.0, −15.0) | ≤ 41.2 px | shot 613 (clean) |
| Z-618 | 618 | (−67.0, 127.0) | ≤ 44.0 px | shot 617 (clean) |
| Z-620 | 620 | (−7.0, 152.0) | ≤ 47.8 px | shot 619 (clean) |
| Z-622 | 622 | (49.0, 99.0) | ≤ 23.3 px | shot 621 (clean) |
| Z-623 | 623 | (67.0, 135.0) | ≤ 52.0 px | shot 621 (clean) |
| Z-626 | 626 | (74.0, −7.0) | ≤ 36.2 px | shot 625 (clean) |

The radius bound is a real measurement, not a guess: the nearest station at which the
player stood *outside* any field bounds how far that field can reach. All six interior
points verify as inside the traced floor mask.

**Distinctness: 15 of 15 pairs demonstrably distinct.** Each pair is separated either by an
intervening zone-free station or by more than one member's own radius bound. The tightest
case is Z-622 ↔ Z-623 at 40.2 px separation against Z-622's own ≤23.3 px bound — separated
on Z-622's evidence alone.

**Distribution.** The six sit in the outer lobes: NW wing, NE wing, SW wing, SE wing, south
lobe, and one between south and SE. None sits in the central body.

### DoT mechanic

`provenance: ATTESTED-UNMEASURED` · magnitude **null** · element **suspected-poison**
(Matt's own hedge). **No number is derived here.** Named decode paths, neither commissioned:
video HP-delta measurement, or GD spawn-area table decode.

---

## 4. Damage corroboration of the L-64 attestation

*Reported as observation. Graded by nothing.*

Six stations place the player inside a field. **Five show a depressed health readout** in
the bottom-left HUD (max 20 005):

| shot | in-zone (green frac, r<60) | HUD health | depressed |
|---|---|---|:--:|
| 614 | 0.589 | 15 460 / 20 005 | **yes** |
| 618 | 0.768 | 13 980 / 20 005 | **yes** |
| 620 | 0.623 | 15 527 / 20 005 | **yes** |
| 622 | 0.321 | 20 005 / 20 005 | no |
| 623 | 0.676 | 17 030 / 20 005 | **yes** |
| 626 | 0.249 | 16 947 / 20 005 | **yes** |

All 15 non-zone stations read 20 005 / 20 005. The correspondence is exact in both
directions but one: **the only station with green under the player and full health is 622,
which is also the station with the lowest green fraction (0.321) — plausibly an entry
frame before the first tick. I do not claim that; I report the discrepancy.**

Two instrument notes, because they change how the numbers should be read:

- **The floating health bar is not a usable instrument here.** It reads 51–63 px of 73 in
  the in-zone frames, but that is the green field VFX blending over the bar and defeating
  the colour test — not the HP value. I abandoned it for the HUD numeral readout, which
  sits away from the fields. Anyone re-deriving from the bar will get wrong numbers.
- **The health *numerals* are reported as read. No tick rate is computed from them.** These
  are six independent exposures at different depths into different fields with unknown
  dwell times and unknown regeneration — the differences are not a time series. Deriving a
  magnitude from them would be exactly the invention L-64 forbids.

Debuff-icon evidence was inspected and is **inconclusive** — the HUD status row differs
between clean and in-zone frames, but not in a way I can read cleanly at this resolution.
Not offered as corroboration.

---

## 5. What these shots cannot support

### 5.1 The screen ↔ arena ground map M — NOT RECOVERABLE

This is the single blocker behind both the zone extents and the weak metre scale, so it is
stated with its evidence rather than asserted.

- **Consecutive world-view registration: failed.** Masked NCC on high-passed, green-
  suppressed luminance across all 20 links: **peaks 0.18–0.42**, most locking at (0, 0).
- **Direct template matching on ground-only patches: failed.** 14 shot pairs including
  612↔627, which share the north gate outright: **peaks 0.039–0.268**, i.e. noise.
- **Cause, named:** the walk steps are larger than the useful overlap (a ~25 px minimap
  step is ~370 screen px), and the scene is a perspective render of 3D geometry, so a
  camera translation produces **parallax** — only the ground plane translates coherently,
  and there is not enough clean ground in frame to carry the correlation.
- **Green-field consensus fit (all-data, physically parameterised over s, sin θ, yaw):
  degenerate.** The agreement-rate objective climbed monotonically to the *corner* of the
  search grid (s = 7.0, sin θ = 0.35, both at the lower bound) with no discrimination in
  yaw (score spread 0.039–0.048 across the entire yaw range), and the earlier centroid-
  correspondence variant found only 14 inliers out of 812 at an implausible 20° pitch.
  That is a fit reporting its own failure, and I am reading it as such rather than
  quoting its numbers.

**Consequence, honestly drawn:** the green-zone *outlines* are not traceable from this
capture set. I have not drawn them. `green_zones.polygons` is `null` with the reason
recorded in the file. Each zone instead ships as a measured interior point plus a measured
radius bound — which is less than the ask, but is a measurement rather than a shape I made
up. **Per the L-59 pre-registered fallback, nothing is lost: Class 1 ships complete, and
Class 2 ships the part the evidence carries.**

**Cheapest refuting test, named** (Discipline #19.1): a *dense* capture pass — 8–12 shots
at one zone with small steps, or one video pan — would restore world-view overlap and
recover M immediately, at which point the zone outlines follow directly from the green
masks already extracted by `gd_green_zones.py`. Nothing else in this note would change.

### 5.2 Whether six is the total zone count

Six are demonstrated. Matt attests he entered all of them. Those two facts do not compose
into "there are six": **a zone entered between two exposures leaves no evidence.** Against
that, up to **7 simultaneous green fields ≥5000 px** are visible in a single frame (shot
620; 5 in 619; 4 in 618) — though large fields fragment behind occluders, so that is a
soft upper indication and not a count.

**The honest statement is: ≥6, exact total not established.**

---

## 6. Coverage gaps

**No arc of the boundary is INTERPOLATED.** Every outer-ring vertex was painted by at least
3 independent minimap observations (min 3, median 13), and **0 of 1755 boundary pixels abut
an unobserved region** of the mosaic canvas. Matt's circuit fully enclosed the arena in
minimap coverage — the walk over-delivered on the 8–12 shot spec, and it shows.

Two arcs are **mapped but never walked** — named, not silently smoothed:

| arc | vertices | min observations | max distance to nearest station | bearing from arena centre |
|---|---|---|---|---|
| A | 0–8 (9 verts) | 3 | 104 px | ~ +5° (due north) |
| B | 174–176 (3 verts) | 3 | 101 px | ~ −4° (due north) |

Both lie on the **north corridor and its terminal chamber**, which Matt approached (shots
612, 627, at the gate) but did not enter. Their *shape* is measured from a distance; their
*walkability* was never demonstrated by the player's own body. They carry
`MEASURED-APPROXIMATE-FROM-REFERENCE` with that caveat attached, not `INTERPOLATED` —
because nothing about them was invented to bridge a hole.

---

## 7. Counts observed (count only — no reconciliation)

Per the charter, these are reported for the conductor's fold and are **not** reconciled
against the sim's spawn-anchor expectations here.

| observed on the minimap footprint | count |
|---|---|
| green spawn zones **demonstrated** by in-zone occupancy | **6** (≥6; § 5.2) |
| max simultaneous green fields ≥5000 px in one frame | 7 (shot 620) |
| teal pedestal-gem fixtures on the minimap | **5** — one north-central at (6.8, −8.3), four in a rectangle at (−18.1, 45.1), (23.9, 48.8), (−21.1, 73.9), (22.2, 76.7); rectangle 42.6 × 28.4 px centred (1.7, 61.1) |
| vendor / NPC fixture icons | 2 (west and east alcoves) |
| outer-ring vertices | 177 |
| interior obstruction rings | 4 |

**The pedestal gems are not spawn zones.** They are static arena fixtures, consistent with
the icon vocabulary recorded in the earlier `eor_minimap.py` census work, and they are
distinguishable from the green fields by kind: the gems live on the minimap, the fields
live in the world and never appear as a map feature. The five-gem rectangle is centred
within 4 px of shot 632's station — Matt stood in the middle of it — and that station shows
a square stone dais in world view.

---

## 8. Mirror voice

The arena would not show itself from inside. Every attempt to read it from where the
player stood — frame against frame, ground against ground — came back noise, because
what the eye sees from inside a place is parallax and green fire, and neither of those
holds still long enough to be measured.

What held still was the small disc in the corner of the screen. Not the world: the
*map* of the world, drawn once and carried unchanged from station to station, waiting to
be laid over itself twenty-one times. The picture the Mirror returned is the one Matt was
never looking at.

So the walls are known and the fires are only located. That asymmetry is not a shortfall
in the walk — Matt gave nearly twice the shots asked for, and they closed the ring. It is
the shape of what a perimeter can tell you: where the edge is, and that the fire burns,
and not yet how wide it burns.

---

## 9. Deferred — with the empirical criterion that gates re-engagement

| item | gate |
|---|---|
| green-zone **outline polygons** | a dense capture pass at one zone (8–12 small-step shots, or one video pan) restoring world-view overlap → M recovers → outlines follow from the already-extracted green masks |
| metre scale pinned to ±5 % rather than ±1.7× | registration of this footprint against the sim-side derived occupancy hull (conductor's fold, R-L64-1) |
| DoT magnitude | video HP-delta measurement, or GD spawn-area table decode — neither commissioned |
| exact green-zone total | a zone-by-zone enumeration pass, or the spawn-area table decode above |

Not one of these is gated on time passing. Each is gated on a specific piece of evidence
that does not yet exist.

---

**Signed:** galadriel — visual-perception and benchmark steward.
Read-only against all production code and all other agents' trees; writes confined to
`agentic_orchestration/galadriel/`. No pushes.
