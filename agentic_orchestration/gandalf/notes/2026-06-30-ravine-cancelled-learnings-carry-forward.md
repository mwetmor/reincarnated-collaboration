# Ravine (CANCELLED) — learnings carry-forward to the seasonal descent

> **STATUS:** CURRENT — durable lineage note. The Godot enchanted-forest **ravine
> biome-prototype is CANCELLED** (Matt, 2026-06-30: *"the ravine work was cancelled.
> But there may be some learnings there."*). This note **promotes** the load-bearing
> learnings out of the 9 raw iteration notes into one durable home, so those 9 become
> prune-eligible (promote-then-prune — § 7). The active home for the substance is the
> **seasonal-descent procgen architecture** (`canonical/story/2026-06-22-seasonal-descent-architecture-recognition.md`),
> whose **§ 3 procedural-middle prototype** and **gate G3 (socket/snap)** are exactly
> what most of these learnings feed.

**Authored:** 2026-06-30
**Author:** gandalf (story/design steward)
**Authority:** Matt 2026-06-30 — ravine cancellation + learnings-extraction directive.
**Source notes promoted here (the 9 raw ravine notes → § 7 disposition):**
`2026-06-20-enchanted-forest-ravine-plan-and-floor-sizing-research.md` ·
`2026-06-20-ravine-vignette-generator-spec.md` ·
`2026-06-20-ravine-cutout-pattern-spec.md` ·
`2026-06-20-ravine-atgrade-matt-gate-package.md` ·
`2026-06-20-ravine-tripod-autonomous-run-verdict.md` ·
`2026-06-21-ravine-carve-and-sculpt-spec.md` ·
`2026-06-21-ravine-carved-r1-matt-gate-package.md` ·
`2026-06-21-ravine-carved-r2-matt-gate-package.md` ·
`2026-06-21-ravine-carved-r3-matt-gate-package.md`
**Cross-refs:** the seasonal-descent recognition record (the active home);
`reincarnated-godot/data/act_graph_node_schema_draft.json` (the node-schema the
ravine generalized — survives as the crypt-vault artifact); the crypt-vault PoC
notes (the ravine's methodology parent — § 7 flags the open cancellation question).

---

## 0. Why this note exists (and why it is NOT just a tombstone)

The ravine prototype is cancelled, but it was the project's **first full procgen-biome
carry test** — author one exemplar, encode the rules as an *algorithm* (not coordinates),
seed-vary, snap-assemble, gate. That methodology is **biome-agnostic** and is precisely
the capacity the seasonal-descent §3 procedural-middle prototype must prove (gate G3).
**The geometry dies; the method and the gotchas carry.** This note separates the two
honestly: § 2–§ 5 are what transfers, § 6 is what dies with the ravine form.

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

Verified at the **tripod run** (fixed-camera multi-framing capture) via NV-1…5: zero void
pixels; walls close the upper frame; down-range terminus occluded; skydome + rim-treeline
middle plane legible; the illusion holds. NV-failures feed generate→gate→graduate exactly
like structural ones. *[biome-agnostic for any open-air descent floor; an enclosed/cavern
floor uses the crypt's never-capped-tower analog instead]*

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

## 6. What was ravine-SPECIFIC and dies with the cancellation (honest list)

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

The **methodology** in § 2 and the **rule-shapes** in § 3 are what survive; the **content**
of the rules is replaced per biome.

---

## 7. Disposition — the 9 source notes are now PRUNE-ELIGIBLE (Matt ratifies)

Per promote-then-prune: the load-bearing substance of all 9 ravine notes is now banked in
§ 2–§ 6 above (+ git history retains the originals verbatim regardless). The workstream is
**CANCELLED** (Matt 2026-06-30) — predicate 3 (totally-superseded / workstream-closed)
holds, and a cross-repo reference check is the only remaining gate before a clean prune.

**This re-classifies prune-list § 3c (the 9-note ravine cluster) from KEEP → PRUNE-RECOMMENDED.**
The original § 3c KEEP rationale ("r3 awaiting the Matt Gate; workstream OPEN") is void —
the workstream is cancelled, not awaiting a gate.

**I am NOT auto-rm'ing these** — Matt is in live dialogue and surface-for-ratification is the
correct mode (the auto-prune ceiling: ambiguity/judgment → surface, never auto-fire). One
verification remains before any `git rm`: confirm none of the 9 is **path-cited or basename-
cited** by an evidentiary home across BOTH repos (decisions-log lives in the engine repo).
On Matt's word + a clean reference check, the 9 `git rm` in one commit (NO push).

**Open question flagged, NOT assumed (out of scope to rule):** the ravine generalized its
node-schema + Gate-1 + generate→gate→graduate loop from the **crypt-vault PoC**. Matt
cancelled *"the ravine work"* — not, explicitly, the crypt-vault prototype. The crypt notes
(`2026-06-19-crypt-vault-*`) stay **KEEP** until Matt rules on whether the crypt-vault
Godot prototype is also retired. The methodology in § 2 transfers regardless of which
prototype proved it — so even a full Godot-prototype cancellation does not lose the gold.

---

**Tracker-delta:** STORY tracker — the seasonal-descent procgen-middle (recognition record
gate G3) now has a **banked methodology + worked rule template** from the cancelled ravine
(this note); no new commitment, but G3's "blank page" risk is retired. ENGINE tracker — the
open cross-seam question *(does physical room-resizing feed the balance sim? § 2 L6)*
remains unresolved and gates the descent's § 5 adjustment algorithm; route to KR/gamora.

**Signed:** gandalf, 2026-06-30. The ravine geometry is cancelled; its method, its rule-
shapes, its no-void ruleset, its gate process, and its Synty/Godot scar-tissue are promoted
here for the seasonal descent to consume. Nine raw iteration notes are now prune-eligible —
surfaced for Matt's ratification, not auto-pruned. The gold was never the gorge; it was the
proof that a biome can be carried as gated rules.
