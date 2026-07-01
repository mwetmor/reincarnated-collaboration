# Cancelled Godot prototypes (RAVINE + CRYPT-VAULT) — learnings carry-forward to the seasonal descent

> **STATUS:** CURRENT — durable lineage note for the project's **two cancelled Godot
> presentation prototypes**. (1) The enchanted-forest **ravine biome-prototype is CANCELLED**
> (Matt, 2026-06-30: *"the ravine work was cancelled. But there may be some learnings
> there."*). (2) The **crypt-vault clear-room node** scene is **ALSO CANCELLED** (Matt,
> 2026-06-30: *"The crypt/vault learnings can be added to the ravine learnings, but the
> scene was cancelled."*) — but it was the **methodology PARENT** the ravine generalized
> from, and it produced the project's strongest camera + composition recognitions, so its
> learnings are folded here (§ 8). **A third scene that uses the same Synty map-pack — the
> small square-room with a king character (`2026-06-22-king-rig-mcp-alignment-brief.md`) —
> is the LIVE game being built and is explicitly NOT pruned** (Matt 2026-06-30). This note
> **promotes** the load-bearing learnings out of the raw iteration notes into one durable
> home, so those notes become prune-eligible (promote-then-prune — § 7). The active home for
> the substance is the **descent procgen-middle** — now folded into
> `canonical/current-to-end-state/current-to-end-state-game.md` **PART B (B2 descent
> floor-authoring queue)** + the settled descent spec
> `canonical/reap-die-rise-story/gameplay-loop-design.md` §6/§9 — exactly what most of these
> learnings feed. (The source recognition doc was folded + deleted 2026-06-30; its **§ 3
> procedural-middle** / **gate G3 socket-snap** live in game-tracker B2.)

**Authored:** 2026-06-30
**Author:** gandalf (story/design steward)
**Authority:** Matt 2026-06-30 — ravine cancellation + crypt-vault cancellation + learnings-extraction directive; king-rig scene explicitly protected.
**Source notes promoted here — RAVINE cluster (9 raw notes → § 8 disposition):**
`2026-06-20-enchanted-forest-ravine-plan-and-floor-sizing-research.md` ·
`2026-06-20-ravine-vignette-generator-spec.md` ·
`2026-06-20-ravine-cutout-pattern-spec.md` ·
`2026-06-20-ravine-atgrade-matt-gate-package.md` ·
`2026-06-20-ravine-tripod-autonomous-run-verdict.md` ·
`2026-06-21-ravine-carve-and-sculpt-spec.md` ·
`2026-06-21-ravine-carved-r1-matt-gate-package.md` ·
`2026-06-21-ravine-carved-r2-matt-gate-package.md` ·
`2026-06-21-ravine-carved-r3-matt-gate-package.md`
**Source notes promoted here — CRYPT-VAULT cluster (5 raw notes → § 6 + § 8 disposition):**
`2026-06-19-crypt-vault-node-poc-brief.md` ·
`2026-06-19-crypt-vault-node-gate3-coherence-capture.md` ·
`2026-06-19-crypt-vault-gate3-verdict-1-calibration.md` ·
`2026-06-19-crypt-vault-rebuild-brief-camera-committed.md` ·
`2026-06-19-crypt-vault-phase1-verification-and-preread.md`
**Explicitly NOT pruned (LIVE):** `2026-06-22-king-rig-mcp-alignment-brief.md` — the
small square-room king scene, the live game being built (Matt 2026-06-30). Same Synty
map-pack, different scene, not cancelled.
**Cross-refs:** the seasonal-descent recognition record (the active home);
`reincarnated-godot/data/act_graph_node_schema_draft.json` (the node-schema the crypt-vault
PoC derived substrate-led and the ravine generalized — survives as a live engine artifact);
`canonical/story/battle-room-presentation-decoupling-2026-06-15.md` + `style-register.md`
(the crypt PoC's design parents — the annulus rule + cathedral register live there, not in
the cancelled notes).

---

## 0. Why this note exists (and why it is NOT just a tombstone)

The ravine prototype is cancelled, but it was the project's **first full procgen-biome
carry test** — author one exemplar, encode the rules as an *algorithm* (not coordinates),
seed-vary, snap-assemble, gate. That methodology is **biome-agnostic** and is precisely
the capacity the seasonal-descent §3 procedural-middle prototype must prove (gate G3).
**The geometry dies; the method and the gotchas carry.** This note separates the two
honestly: § 2–§ 6 are what transfers (§ 6 = the crypt-vault methodology parent), § 7 is what
dies with the prototype forms.

The discipline is **promote-then-prune** (verify-then-prune first-run finding, § 5b):
notes accumulate because load-bearing reasoning lives in notes instead of being promoted;
auto-prune can never delete load-bearing substance; the fix is to *promote the substance
to a durable home, then the raw notes clear predicate 3 (totally-superseded) and become
prunable.* Cancelled work is the cleanest case of this — the iteration record is spent
the moment its learnings are banked.

---

## 1. The carry-forward map (learning → where it lands in the active work)

| # | Learning | Lands at (seasonal-descent recognition record) |
|---|---|---|
| L1 | **Edge-socket snap-by-construction** (R4) — the load-bearing primitive | **§ 3.2 socket/snap contract; gate G3.** This IS the same problem the descent's modular-middle assembler must solve. Direct transfer. |
| L2 | **exemplar → seed-vary → assemble** carry chain | **§ 3 "smallest first test"; gate G3.** The descent's seeded assembler test is structurally identical. |
| L3 | **generate → gate → graduate** rule-discovery loop (we already own the rule-discovery engine) | **§ 3 procedural-middle**, and § 9 generation-quality bar. We do NOT need WFC to *find* rules — the gate loop finds them. |
| L4 | **WFC-as-scale-path** — overkill at small N, earns its keep at 50+ tiles | **§ 3 "how procedural" open decision.** The *infinite* descent IS the 50+ regime where WFC earns evaluation. Sharpens the open question. |
| L5 | **Two-footprint rule** (playable ⊂ visual; flat combat floor; undulation in the rim band) | Any procgen room in **§ 3**; presentation discipline for the modular middle. |
| L6 | **The 28×28 vestigial-removal principle** — balance-sim arenas size for FIGHT MATH; ARPG rooms by GENRE CONVENTION | **§ 4 content-JSON boundary** (*engine emits content, Godot owns geometry; the JSON never carries room dimensions*). The ravine caught this as a category error; the descent must not re-import it. **Reinforces § 4 directly.** |
| L7 | **Massive-zone-illusion / no-void** (R10–R14, NV-1…5) | Any open-air biome in the descent; the camera-dependent half of the gate. |
| L8 | **Tripod gate + eye-overrides-hard-gate** (process) | Any visual gate in drax's seam; the gate proves structure+zero-void, NOT credibility. |
| L9 | **Synty/Godot asset gotchas** (§ 5) | drax-seam reference for ALL Godot presentation work, descent included. |
| L10 | **Register-evolution staleness** — a dark-first CV rubric goes stale against a brightened target; CV becomes advisory until re-baselined | galadriel CV discipline for any register shift; the descent will shift registers per anchor/biome. |

---

## 2. The transferable methodology (the gold — biome-agnostic)

These are the patterns that survive the cancellation intact and feed gate G3:

- **Rules carry; coordinates don't.** Each design rule becomes (a) a concrete generation
  step and (b) a gate check that the rule held. The rules *travel with the generator*;
  nothing is baked as hand-placed coordinates. This is the whole reason a procgen middle
  is possible — the engine carries the rules into every new floor.

- **The edge-socket contract — snap-by-construction, NOT snap-by-tolerance (L1, the
  load-bearing primitive).** Two abutting pieces share ONE socket profile: piece N+1
  **consumes** piece N's published profile rather than generating its own. The seam is
  continuous *by construction* — there is no tolerance check that can fail, because there
  is no second independent profile to disagree. This generalizes a point-socket (a door
  on a shared grid) to an edge-socket (a shared floor+rim profile along a whole seam),
  and it is **topology-agnostic**: linear, dogleg, U-shape, or grid all ride the same
  contract with zero geometry rework. *For the descent: the socket/snap contract (§ 3.2)
  is the alignment problem; MCP is the right tool to verify it (the king-rig +50% win).
  Get this right or nothing assembles.*

- **exemplar → seed-vary → assemble is the carry test (L2).** Author ONE good exemplar
  piece that passes its standalone gate; hold the ruleset + register constant; vary the
  seed to produce N distinct pieces with distinct focal elements; snap them via the socket
  contract; run the assembled gate (traversal start→end). *If the rules carry, seed-
  variation yields coherent-but-distinct pieces with no per-piece hand-authoring.* That
  passing assembly IS the proof of procedural capacity — it is exactly the descent's
  "smallest first test" (§ 3).

- **generate → gate → graduate is the rule-discovery engine (L3).** Every human catch
  ("that tree's floating," "you can walk up that slope and out") becomes a new standing
  gate criterion. We *own* a rule-discovery loop; we do not need to import WFC to discover
  rules. (WFC's exemplar-mode can infer adjacency, but the gate loop already does the
  discovery and keeps it auditable.)

- **WFC is the scale-path, not the starter (L4).** WFC's native abstraction IS a snap-rule
  system (tiles + adjacency + propagation; it only ever places matching edges). But at
  small N a clean edge-socket contract + a hand-authored adjacency table suffices — WFC is
  overkill and adds contradiction/backtracking cost. It **earns its keep at 50+ tiles
  (Diablo/PoE scale).** Its failure mode is the north-star's weak spot: great at *locally*
  coherent "looks natural," weak at *globally intentional* "feels authored" (Townscaper /
  Bad North — gorgeous, composition-agnostic). Focal points and paced difficulty must be
  imposed on top; they don't emerge. **Name it for the descent's scale regime; adopt on
  evidence, not by default.**

- **The two-footprint rule (L5).** Playable footprint ⊂ visual footprint. Keep the combat
  floor flat (cheap, legitimate — most ARPG outdoor arenas are flattish clearings); push
  all undulation + non-passable scatter into the rim/annulus band. Structure is grid-
  snapped and few; scatter is Poisson-disk and inset from seams. Two distinct rule-sets.

- **The 28×28 vestigial-removal — a category error to never re-import (L6).** Map rooms had
  been sized from the balance/gauntlet sim's arenas (`arena_scenarios.json` `elite_pack` =
  28×28). That is a **category error: the balance sim sizes arenas for FIGHT MATH; ARPG
  rooms are sized by GENRE CONVENTION** (encounter pacing, screen real-estate, density).
  The *mechanism* (two-footprint) carries; the *magic number* and its "sim-invariant /
  sacrosanct" status are removed; the real size is **re-derived from genre research**
  (substrate-led: let the genre vote, don't pre-impose the sim's number). **This is the
  same boundary the descent's content-JSON seam draws (§ 4): the engine emits CONTENT
  (which monsters, scaled to tier; theme; loot), Godot owns GEOMETRY (room sizes/walls/
  props). The JSON must never carry room dimensions.** The moment the engine emits
  geometry, balance authority and presentation authority fork (cf. D3's launch client/
  server difficulty split).

  *Open cross-seam question this surfaced (carries forward, route to KR/gamora):* does
  re-sizing rooms feed back into the balance sim? If gamora's sim models SPACE (kiting /
  LoS / AoE-overlap) → smaller rooms shift balance; if it's spatially ABSTRACT (DPS/EHP/
  time-to-kill) → presentation-only. The descent's adjustment algorithm (§ 5) needs this
  answered before it ties floor difficulty to a physical room.

---

## 3. The worked ruleset (R1–R14) — preserved as the concrete example

The ravine's rules are the *worked instance* of § 2's methodology. Most are ravine-form-
specific in their *content* but exemplary in their *shape* — they show what "encode the
biome as gated rules" actually looks like end to end. Preserved verbatim so the descent's
first biome generator has a template, not a blank page.

### 3a. Structural rules (R1–R9) — camera-INDEPENDENT, engine-truth, the Gate-1 set

- **R1. Single floor Y** across all tiles (one combat plane). *[biome-agnostic for flat-
  floor biomes; the descent's combat rooms want this]*
- **R2. No structure stacks** — two structures never overlap/snap atop one another ⟹ a
  min-spacing constraint; canonical tool **Poisson-disk sampling**. *[biome-agnostic]*
- **R3. Rim slope-continuity** — adjacent rim samples can't slope too severely ⟹ max-delta
  between adjacent rim heights, within a tile (the seam is exact by R4). *[rim-specific]*
- **R4. Edge-socket = shared rim+floor profile** — the snap-by-construction contract
  (§ 2, L1). **The load-bearing generalization.** *[biome-agnostic — THE primitive]*
- **R5. Seam keep-out band** — free-scatter insets from every edge; only edge-matched
  features touch the seam ⟹ no cross-seam overlap. *[biome-agnostic]*
- **R6. Path-corridor socket + A\* continuity** — the walkable floor connects entry→exit
  per piece and aligns across seams; A* across the assembled map must traverse start→end.
  *[biome-agnostic — the traversal gate]*
- **R7. Focal-point-per-piece** — ONE hero element per piece (gorge: fallen-tree bridge /
  glowing pool / rock-wall shrine / rope-bridge / waterfall) so pieces read DISTINCT, not
  identical segments. *This is what makes a piece a vignette, not a tile.* *[biome-agnostic
  principle; the descent's per-floor sub-anchor (§ 7 of the recognition record) is the
  story-side analog — the floor exists because of who/what rules it]*
- **R8. No false-affordance** — apertures/side-paths add variety + light but must NEVER
  create a walkable escape from the play floor (flood-fill from the floor must not reach
  outside the visual footprint). *[biome-agnostic]*
- **R9. Terrain-conform = flat play floor + terrain in the rim band** — the two-footprint
  rule (§ 2, L5) in rule form. *[biome-agnostic]*

The ported **Gate-1** turns each rule into a camera-independent engine-truth check
(AABB interpenetration; per-seam profile equality; A* existence; both-ends-land on
verticals; spawn parity inside the playable footprint; rim max-delta; flood-fill no-escape).
**The generate→gate→graduate loop carries as-is** — every new human catch becomes a new
criterion.

### 3b. Massive-zone-illusion (R10–R14) — camera-DEPENDENT, the no-void / tripod set

The requirement: the player believes they are in a *massive open zone*, restricted ONLY by
diegetic geometry (the gorge wall height), never by a visible edge-of-world. **No pixel in
any framing renders the black/clear-color void.**

- **R10. Frustum-fill (the acceptance test).** 100% of every committed framing is geometry
  or skydome; zero void pixels. R11–R13 are the construction that guarantees it.
- **R11. Three fill-planes (depth stack):** (a) **floor plane** extends beyond the playable
  footprint and beyond the frustum's ground-intersection — non-playable continuation is
  cheap, low-detail, UNREACHABLE (restriction holds via wall height, not via a visible
  floor edge); (b) **wall planes** rise to ≥ top-of-frame, or the rim treeline closes any
  gap — the restriction is the diegetic wall, never an invisible wall in a flat field;
  (c) **far terminus** never shows a flat wall or void — closed by a dogleg/curve out of
  frame, distance haze, or a canopy occluder (*the hand-authored end-bookend earns its
  keep closing the down-range frustum*).
- **R12. Mandatory skydome.** Sky is legitimate fill, not void; the rim treeline (the
  never-entered false-front) is the middle depth plane between wall-tops and sky.
- **R13. Visual footprint = camera-derived OVERRUN, not a fixed pad.** The dressed extent
  is sized to overrun the frustum on every visible edge — a *function of the camera*
  computed at build, not a constant.
- **R14. The illusion contract (player-feel).** Restriction reads as "I am deep in a
  gorge"; the horizon reads as "this world is vast." If a framing makes the player think
  "the level just... ends there," R14 has failed even if R10 technically passed.

Verified at the **tripod run** (fixed-camera multi-framing capture) via the **NV-1…5
no-void criteria** (camera-dependent half of the gate, carried verbatim so the prune is
safe):

| NV | Check | Guards | Verification |
|---|---|---|---|
| **NV-1** | **Zero void pixels** — no black/clear-color anywhere in frame | R10 | per-framing: count clear-color pixels == 0 (CV histogram / clear-color-key sample); every pixel is geometry or skydome |
| **NV-2** | **Walls close the upper frame** — no void band between wall-top and frame-top (or rim treeline closes it) | R11b | per-framing: trace the L/R wall silhouette; no sky/void wedge below the intended horizon where a wall should occlude |
| **NV-3** | **Down-gorge terminus occluded** — far end shows curve/fog/canopy, never a flat wall or void | R11c | the committed down-gorge framing: terminus region is geometry+haze, not a hard edge or void |
| **NV-4** | **Skydome present + rim-treeline middle plane reads** — three depth planes legible | R11+R12 | upper frustum is sky; a treeline silhouette sits between wall-tops and sky (depth read) |
| **NV-5** | **Illusion holds (R14)** — no framing reads as "the level just ends here" | R14 | judgment check on the framing set: vastness + diegetic-wall-restriction, no edge-of-world tell |

NV-failures feed generate→gate→graduate exactly like structural ones (a void wedge caught
in a framing becomes a standing NV check). *[biome-agnostic for any open-air descent floor;
an enclosed/cavern floor uses the crypt's never-capped-tower analog instead]*

---

## 4. The depth-toward-the-climax beat (the one carve learning worth keeping)

The carve revisions (R1/R2/R3 in the carve-and-sculpt spec) were mostly **register-specific**
(brightness, the brighter hazy green-blue "Zelda" register, foliage-card ALPHA_SCISSOR,
water coherence) — those die with the ravine's particular look. **One carve learning is
mythic-structural and carries:** *depth varies toward the climax.* The gorge deepened as it
approached the boss arena; the carve drifted cave-ward as it descended. That is the
**katabasis beat** made geometric — the world closes in and drops as you near the
confrontation at the bottom. The seasonal descent is *literally* a descent (recognition
record § 1, § 6); this is a free, genre-true tool for its modular middle: **let geometry
deepen and tighten toward each floor's sub-anchor confrontation, and toward the season
mega-boss at the bottom.** Camera corollary (also carries): **look INTO the descent, not
back at the rim** — the strongest depth read is down the sightline of the corridor's length.

---

## 5. Synty / Godot asset gotchas (drax-seam reference — carries to ALL Godot work)

Concrete asset-pipeline traps the ravine work paid for once; bank them so the descent's
Godot presentation doesn't re-pay:

- **FBX broken texture paths → load the atlas directly.** Synty FBX imports often carry
  broken/relative texture paths; resolve by `Image.load()` of the atlas and assigning the
  material in code rather than trusting the imported material.
- **Mixed units — meters vs centimetres.** Synty source mixes scales; verify per-asset
  (e.g. `Troll_01` ≈ 2.89 m). A silently cm-scaled mesh is the classic "giant/ant" bug.
- **Goblin = roster mesh + green-skin atlas** (the enemy is a base humanoid mesh re-skinned
  via atlas swap, not a unique mesh) — the re-skin-via-atlas pattern generalizes to roster
  variety cheaply.
- **Foliage cards need ALPHA_SCISSOR**, not alpha-blend, or they z-fight / haze the frame.
- **Water = coherence, not tiled quads** — tiled water quads read as a grid; a single
  coherent surface reads as water.
- **Gold-girder / banded-metal = an atlas swatch-sheet stretched across BoxMesh UVs** —
  root-caused a magenta artifact to an asset sampling a red atlas region; the fix is UV
  control over which swatch the box samples. (General lesson: stray colour artifacts are
  usually an atlas-region sampling bug, not a lighting bug.)

---

## 6. CRYPT-VAULT PROTOTYPE — the methodology PARENT (also cancelled; richest learnings)

The crypt-vault clear-room node was the project's **first node-authoring PoC** of the
"author-in-MCP, structure-first, three-gate" method — the method the ravine then *generalized*
to an open-air biome. The scene is cancelled, but it produced the project's **strongest camera
+ composition + method recognitions to date.** These are MORE foundational than the ravine's
(the ravine inherited its node-schema, its Gate-1, and its generate→gate→graduate loop from
here). Banked below; the geometry dies, the method + the camera recommendation + the
composition grammar carry.

### 6.1. The three-gate authoring method (THE load-bearing carry — the descent's § 3 loop IS this)

The unit of authoring/judgment/Act-Graph schema is the **NODE**, defined precisely:

> a **presentation-room sized to *contain* its fight footprint (sim-invariant), with sockets
> to stitch to neighbors.** A pretty standalone room is NOT a node — it doesn't compose.

Judged by three instruments, IN ORDER, each catching what the prior cannot:

- **Gate 1 — Structural (camera-INDEPENDENT, deterministic, MCP engine-truth).** The
  load-bearing gate — catches breakage with *no camera at all*: (1) no structure-on-structure
  AABB overlap; (2) all GridMap cells valid, door = wall-variant cell on the shared grid
  (**cannot be half-occluded by construction**); (3) A\* passability entrance-socket→exit-socket;
  (4) vertical navigability (mezzanine reached via stair, clearance passable); (5) fight-spawn
  parity (chosen shell's footprint + spawns preserved, annulus rule). This is the *automation*
  of the descent run-to-green's **manual** structural ruling. **Identical in spirit to the
  ravine's ported Gate-1** (§ 2, § 3a) — same loop, enclosed-room flavor.
- **Gate 2 — Register (CV, galadriel).** Holds the locked register (cathedral, here) across
  framings; HFD/LMV/LDR/SAT/HLF within band. **Critical finding: register CV is structurally
  BLIND to spatial coherence** — galadriel's register pass *shipped an incoherent scene*
  (image statistics cannot see overlapping crypts or floating stairs). This is *why* Gate 1
  exists as a separate, prior gate.
- **Gate 3 — Coherence (Matt, human).** "Does it read as a place a human built?" — the
  semantic/aesthetic judgment Gate 1 can't yet make. **Matt's verdict + REASONS are captured
  as calibration triples** `(criterion, specific element, what he wants instead)` — the corpus
  of triples across iterations *is the HITL-removal investment* (it is what would eventually
  let an automated judge approximate Matt's eye). Capture verbatim; paraphrase loses the intent.

**generate→gate→graduate carries identically:** every human catch at Gate 3 that *escaped*
Gate 1 becomes a NEW Gate-1 criterion (see 6.3). recognition → validate → commit at the room
scale: nothing canonicalizes until the node passes Matt.

### 6.2. The project ARPG camera recommendation (BANKED — gated on re-ratification)

Matt committed a camera for this node, with the explicit note *"this is very likely THE
project ARPG camera — lock it project-wide once this node passes."* **The node did not pass
(cancelled), and the live king-rig scene uses a different rig (a `_seat_sword` prop angle,
pitch 75 — not a player camera). So this is a BANKED RECOMMENDATION, not a ratified lock.**
The seasonal-descent presentation should adopt it as the *starting* recommendation, and the
descent's first authored floor becomes its ratification. The recommendation, in full:

- **Bearing: SE, looking diagonally toward the NW** (SE-looking-NW isometric — the **Diablo II
  standard**). Justified geometrically, not by taste: **SE is the ONLY diagonal that keeps BOTH
  far walls in front of the camera** — the other three throw the grand wall or the gallery
  *behind* the lens.
- **Pitch: shallow oblique, ~35°** (the D2 / PoE end of the dial; **NOT top-down**). Chosen
  because a towering detailed backdrop only reads at a shallow pitch — steep foreshortens,
  flattens detail, and brings the tower-top back into frame.
- **Scripted, not hand-placed:** bake the transform into the render generator so it survives
  regenerate; never set it in the live editor (the next bake clobbers it).
- **Detail-budget asymmetry:** the **far hemisphere (N + W + NW) gets the detail budget +
  ALWAYS stays in frame**; the **near hemisphere (S + E) goes LOW / cull / fade** to get out
  of the way.
- **Left-handed-compass GOTCHA (load-bearing):** this scene labels `+Z = North` while keeping
  `+X = East / +Y = up`, so `(East, North, Up)` is a **left-handed** basis — a *mirror* of a
  normal north-up map, which flips L/R map-intuition. Matt's "camera looks SW / East wall is
  tall" read was this mirror. **Verify camera bearing against the generator math, not the
  rendered picture.**

### 6.3. "Only author + judge what the player camera sees" (Matt verbatim — the method's spine)

> *"we should only take pictures of what the ARPG 2.5D diagonal 'top-down' camera will see,
> otherwise we are optimizing for a game the player will never experience — and that's the
> wrong game."* — Matt, 2026-06-19

Consequence: **the multi-angle orbit is RETIRED as the acceptance unit.** Gate 1 (engine-truth,
camera-independent) owns breakage detection; Gate 2 + Gate 3 collapse to the **player's
committed 2.5D camera** (+ any allowed in-game rotation). Orbit/audit angles survive ONLY as
internal debug, never the judged unit. **Evidence the orbit was the wrong acceptance unit: the
15-frame orbit AND Gate 1 both PASSED the broken stairs — only Matt's eye, on the player
camera, caught them.** This reconciles with the anti-single-hero-shot rule: the orbit existed
*pre-Gate-1* to stop one angle hiding breakage; now that Gate 1 owns breakage, judgment
correctly collapses to the player camera. (The ravine's tripod/NV-1…5 run is the OPEN-AIR
analog — a *fixed* multi-framing set, not a free orbit, for a biome with no single committed
sightline; the descent picks per node-type which applies.)

### 6.4. The F1–F4 failure taxonomy (validated negatives) + proxy-vs-reality discipline

Four real Matt rejections of the prior open-loop scene — already-validated negative samples;
reproduce any and it is an automatic FAIL with a known reason:

| # | Failure mode (prior rejection) | The fix / discipline | Gate-1 criterion that should pre-catch |
|---|---|---|---|
| **F1** | ~50 identical crypts copy-pasted, overlapping each other + objects | large architectural pieces are **STRUCTURE** (grid-snapped, FEW, deliberate), **not dressing** | no structure-on-structure AABB overlap; pieces grid-snapped + few |
| **F2** | doors half-hidden by walls | door = **wall-variant cell on the shared grid** (cannot be half-occluded by construction) | A\* entrance→exit reachable; door-cell on grid |
| **F3** | second floors at mid-character height, clipping; broken/floating stairs | real stair, walkable height, clearance, grounded foot, correct climb direction, open landing | vertical navigability + clearance |
| **F4** | overly-tall plain walls with **no architectural reason** | every wall **does a job** (enclose / divide / support / frame) | **PARTIAL — Gate 1 checks overlap/passability, NOT "reason."** F4 is the criterion **least reducible to engine-truth** (semantic, not geometric) → Matt's F4 reasons are the **richest calibration signal** in the whole instrument |

**The proxy-vs-reality discipline (a Gate-1 ESCAPE worked example).** Gate-1 crit-4 ("vertical
both-ends-land") PASSED (foot y=-0.33, top y=6.99, deck y=6.00) yet the stair was *visibly
broken*. The criterion checked **endpoint PROXIES** (AABB foot/top y, deck proximity) but NOT:
stair **orientation** (climbable-face direction via the orthogonal index), visual **grounding**
(mesh-on-floor vs float — the Synty prefab pivot), clear **landing** (no railing blocking),
**support** reaching the deck (piers → full 6 m). gandalf flagged exactly this proxy-vs-reality
gap; Matt's walk confirmed it. **The fix is generate→gate→graduate: each escape grows the
gate** (crit-4 was strengthened with ORIENT/GROUND/LAND/SUPPORT checks + a negative-control
proof — break the stair → crit-4 fails 3 ways → revert → passes). *This is the same discipline
that recurs across the engine: a check that passes a known-bad input is testing a proxy, not
the property.*

### 6.5. The positive bar — "a place a human built" (P1–P4)

A node can trip zero F-checks (nothing *broken*) and still feel lifeless. The positive bar:
**P1** spatial logic reads (you can infer the room's purpose from its shape — a crypt reads as
*a place the dead were laid*, not a box with sarcophagi); **P2** dressing supports, doesn't
dominate (small clutter adds life, never becomes F1 at small scale); **P3** the footprint
reads as playable (a space combat happens in, not a diorama); **P4** register holds to the eye
(Gate-2's quantitative job; a register/coherence disagreement is itself a calibration signal).

### 6.6. The layered far-wall composition (the ornateness technique — why the camera is committed FIRST)

The far wall is **NOT a flat decorated plane** — it is **multi-plane depth the oblique camera
reads as ornate space.** Three planes stacked along the camera sightline: **back** (stone wall
with archways set INTO it + a wall behind each archway → recessed niches holding skull-piles —
the ossuary read); **mid** (vines/moss + small sideways-facing gargoyles/corbels); **front**
(a foreground colonnade carrying another archway — the camera looks *past* it INTO the recessed
niches). Parallax across the planes = "ornate purposeful architectural picture." **This is WHY
the camera was committed FIRST: the layering only reads with a fixed sightline.** Supporting
grammar:

- **The F1-resolution (major generative principle): repetition-IN-a-frame = design;
  repetition-WITHOUT-a-frame = the bug.** A row of identical arched bays reads GRAND, not
  stamped — the archways ARE the frame that converts copy-paste into intentional colonnade
  ornament. *This is how to get richness WITHOUT re-triggering the F1 ~50-overlapping-crypts
  failure.*
- **Never-capped tower / false-front economy (D2/D4/PoE):** the W/NW backdrop climbs *above*
  the camera frame and is **never capped** — out-of-frame ⟹ no wall-top, no ceiling authored.
  **Height gradient: near LOW → gallery MID → tower TOWERING** — the diagonal rise that sells
  the 2.5D depth. (The enclosed-room analog of the ravine's NV no-void requirement: instead of
  "no void to the sky," it's "the wall continues up past the frame so the eye never finds the
  top edge of the world.")
- **Self-justifying architecture (answers F4):** an arcade on **real columns** (NOT square
  bricks) beneath a gallery; **support reaches the full deck** (piers → 6 m, not halfway). A
  wall earns its height by doing structural work the eye can read.
- **An aged/tattered banner descending FROM out-of-frame** reinforces the towering read (cloth
  from unseen height implies the wall continues up), drops a warm accent on grey stone, and
  carries narrative (whose order interred the dead). Age it to match the moss pass.

### 6.7. The eye-flow / crossing-direction principle + the structural-checkpoint discipline

Matt's layout revision, verbatim: *"move the grand wall to the left (same side as the second
level)… swap the two doors one wall to the right, so that the character crosses from
bottom-left to upper right."* The principle: **consolidate the grand backdrop + gallery on ONE
side, and route the player's traverse along the screen diagonal (bottom-left → upper-right) so
the eye-path and the traverse-path AGREE** — arrival reveals the grand hero wall, then the
crossing pulls the eye toward the far exit (the D2/PoE "enter into a reveal, then traverse
toward the next gate"). And the discipline that protects the expensive pass: **re-jig structure
→ quick eye-check on the BARE skeleton → THEN dress.** Dressing the most expensive pass (the
layered far wall) before confirming the grand wall's *position* would put it on the wrong wall.
recognition → validate → commit, at the room scale.

### 6.8. The annulus soft-boundary (numbers + technique — shared with the locked decoupling doc)

The fight footprint is **28×28 m (sacrosanct)**; outer walls at **43×43 m**; a **7.5 m annulus
band** on every side. **Walls are NOT the battle extent** — the soft-boundary keeps combatants
in the playable footprint via *scene-appropriate LARGER scattered objects* across the annulus,
not via an invisible wall. (Matt re-derived the locked decoupling-doc soft-boundary rule by
eye — its canonical home is `battle-room-presentation-decoupling-2026-06-15.md`, NOT these
cancelled notes.) Supporting:

- **K-premium no-false-affordance:** a climbable-*looking* step blocked by a fallen column,
  raised coffins behind — variety + light without a real escape from the play floor. (Same
  principle as the ravine's **R8 no-false-affordance** — flood-fill from the floor must not
  reach outside the visual footprint.)
- **Near-wall fade discipline:** ONLY the near walls (S + E) fade, and ONLY when they would
  actually occlude the character; the far walls (N + W + NW) **never** fade. The *committed
  camera is what makes near-vs-far definable* — without it, an untuned fade made "the entire
  room feel transparent."
- **Reserve inner-annulus depth on the far sides** for the layered far-wall pass — don't let
  solid structure eat the depth the colonnade + niches need.

### 6.9. Schema co-emergence (substrate-led) + the surviving artifact

Do NOT pre-write the Act-Graph node schema — author the node, and let **what it actually
needs** define the first draft (`node_type, footprint, fight_shell_ref, sockets[],
meshlibrary_ref, register_preset, grid_size, vertical_layers, dressing_rules`). The derived
schema **survives the cancellation as a live engine artifact**:
`reincarnated-godot/data/act_graph_node_schema_draft.json` (this is the schema the ravine then
generalized — it is NOT in the pruned notes, so the prune loses nothing).

### 6.10. Godot / MCP operational gotchas (crypt-specific; complement the § 5 Synty list)

- **GridMap cells are base64 in the `.tscn`** — cannot be hand-edited; ALL cell placement goes
  through `godot_gridmap_edit`. This **tool-enforces structure-first** (a happy alignment).
- **GridMap orientation = an orthogonal index 0–23** (24 rotations), not Euler.
- **`get_scene_tree` is unbounded** — pass `max_depth` / `max_children`; prefer
  `godot_scene3d get_spatial_info` with filters for spatial work.
- **Single-occupancy of the Godot project** for any headless rebuild — a collision with the
  open editor dropped a `project.godot` config block (`[addons] sidekick_creator`). Close the
  editor WITHOUT saving first; verify `project.godot` integrity after.
- **Owner-recursion regression canary:** the baked scene node-count is a health signal (healthy
  ≈ 620 `[node]`, **0 MeshCollider, 0 CollisionShape3D**; the recursion bug yields ≈ 601).
- **Tool:** `satelliteoflove/godot-mcp v4.0.1` (validated fork). Plugin-enable mutates
  `project.godot` — diff-review the enable commit (it once dropped an unrelated config block).

---

## 7. What was prototype-SPECIFIC and dies with the cancellation (honest list)

So the carry-forward isn't padded with dead weight:

- The **enchanted-forest biome** choice itself, the **Forest-of-Jura / Zelda** reference
  target, and the specific bright hazy green-blue **register** (and its R1/R2 brightness
  revisions).
- The specific **focal_element enum** (fallen-tree bridge, glowing pool, rock-wall shrine,
  rope-bridge, waterfall) — examples only; the descent picks its own per biome.
- The **gorge geometry specifics** — single sunken floor, 7.5 m rim band, the SE→NW oblique
  framing, the 20×20 m playable / 35×35 m visual numbers (those were Legolas-derived for
  the *ravine*; the descent re-derives per its own genre-research per biome).
- The **1×4 linear assembly** decision and the **2×2-vs-linear** debate — ravine-shape-
  specific (resolved: genre says ravines are linear). The descent's topology is its own call.
- The carve-and-sculpt **R1/R2/R3 lighting/water/foliage** revisions (register-specific).

**Crypt-vault-specific deaths (the geometry, not the method):** the **cathedral register**
particulars (its canonical home is `style-register.md`, not the cancelled notes); the
specific **crypt-vault theme** (sarcophagi / ossuary / skull-niches — examples of the
layered-far-wall technique, not the technique itself); the specific **wall-role layout** (which
wall is grand, where the doors sit) — that was *this room's* solve; the **exact tuning numbers**
(`CAM_DIST=47`, cold/warm split, brazier flame range). The **node schema draft** does NOT die —
it survives as a live engine artifact (§ 6.9).

The **methodology** (§ 2 + § 6.1) and the **rule-/gate-/composition-shapes** (§ 3 + § 6) are
what survive; the **content** (biome, theme, register, numbers) is replaced per node.

---

## 8. Disposition — the source notes are now PRUNE-ELIGIBLE (Matt RATIFIED 2026-06-30)

Per promote-then-prune: the load-bearing substance of all **14** source notes (9 ravine +
5 crypt-vault) is now banked in § 2–§ 6 above (+ git history retains the originals verbatim
regardless). Both workstreams are **CANCELLED** (Matt 2026-06-30: ravine *"the ravine work
was cancelled"*; crypt *"the scene was cancelled"*) — predicate 3 (workstream-closed) holds
for both clusters.

**RATIFIED (Matt 2026-06-30):**

- **RAVINE ×9 → PRUNE.** Re-classifies prune-list § 3c (KEEP → PRUNED). Reference check:
  **clean** — every cross-repo citation of the 9 is intra-cluster (the ravine notes cite each
  other) or in the two governance docs (this carry-forward + the prune-list); **zero external
  evidentiary homes.** The cluster `git rm`s together as a unit. Citations from THIS note + the
  prune-list are intentional git-lineage pointers (the promote-then-prune trail), not live deps.
- **CRYPT-VAULT ×5 → PRUNE** (`2026-06-19-crypt-vault-{node-poc-brief, node-gate3-coherence-
  capture, gate3-verdict-1-calibration, rebuild-brief-camera-committed, phase1-verification-
  and-preread}`). Reference check: mostly intra-cluster; **one external-home caveat (surfaced,
  not silent):** `crypt-vault-node-poc-brief` is cited by a frozen historical dispatch
  (`dispatches/2026-06-19-drax-crypt-vault-node-poc.md`) and `skill_handoff_2026-06-19.md`.
  Those are point-in-time records (KR/handoff territory, not pruned); their references become
  intentional git-lineage pointers post-prune, exactly as the promote-then-prune pattern
  intends (substance is banked in § 6; git holds the originals). No live forward-tracking doc
  depends on them.
- **KING-RIG → KEEP (LIVE, do NOT prune).** `2026-06-22-king-rig-mcp-alignment-brief.md` — the
  small square-room king scene, the live game being built. Same Synty map-pack, different
  scene, **not** cancelled. Verified: it cites **zero** crypt notes, so pruning the crypt
  cluster does not orphan it.

**Auto-prune ceiling honored:** none of this auto-fired — Matt ratified in live dialogue; the
crypt external-home caveat was surfaced for his eye, not silently passed through.

---

**Tracker-delta:** STORY tracker — the seasonal-descent procgen-middle (recognition record
gate G3) now has a **banked methodology + worked rule template** from BOTH cancelled prototypes
(this note); G3's "blank page" risk is retired, and § 6.1's three-gate method is the worked
template for the descent's § 3 procedural-middle loop. The **project ARPG camera (§ 6.2) is
banked, NOT ratified** — the descent's first authored floor should adopt it as the starting
recommendation and ratify it (recognition → validate → commit). ENGINE tracker — the open
cross-seam question *(does physical room-resizing feed the balance sim? § 2 L6)* remains
unresolved and gates the descent's § 5 adjustment algorithm; route to KR/gamora.

**Signed:** gandalf, 2026-06-30. Two Godot prototypes are cancelled; the geometry of both
dies, but the **three-gate method, the F1–F4 taxonomy, the "only judge what the player sees"
spine, the layered-composition grammar, the project camera recommendation, the no-void ruleset,
and all the Synty/Godot/MCP scar-tissue** are promoted here for the seasonal descent to consume.
Fourteen raw iteration notes prune; the live king scene stays. The gold was never the gorge or
the crypt — it was the proof that a *node* can be carried as gated rules a camera can judge.
