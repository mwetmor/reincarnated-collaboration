# Enchanted-Forest Ravine — Vignette Generator Spec (structure skeleton)

**Status:** SIZING-COMPLETE (2026-06-20) — structural skeleton + Legolas-derived sizing truth now both landed. The `⟦LEGOLAS⟧` placeholders are filled from `agentic_orchestration/research/knowledge/arpg-level-design/2026-06-20-arpg-room-sizing-monster-density-ravine-wfc.md`. **One load-bearing design-fit decision is surfaced for Matt: the research shows the ravine archetype is genre-canonically LINEAR (corridor), which is in tension with the locked 2×2-square assembly — see §0.5.** Pending that call, the spec is firing-ready for drax (geometry + gate contract complete).
**Author:** gandalf (design steward), 2026-06-20.
**Parents:** `2026-06-20-enchanted-forest-ravine-plan-and-floor-sizing-research.md` (the locked plan + R1–R9 rules + Legolas brief); `reincarnated-godot/data/act_graph_node_schema_draft.json` (the proven crypt node-schema being generalized); `reincarnated-godot/scripts/check_crypt_vault_gate1.gd` (the proven 6-criterion Gate-1 being ported).
**Discipline:** recognition→validate→commit. This spec is the *carry test* of the architecture-conversation thesis (coordinate-vs-rule; gate-as-carry-mechanism). It commits NO sizing numbers until the substrate (genre research) votes.

---

## 0. What this spec IS

The crypt-vault PoC proved a single hand-authored node stands up structure-first and passes a camera-independent structural gate. This spec **generalizes that one node into a 4-tile procedural assembly** for the outdoor ravine. It does two things:

1. **Ports the crypt's node-schema** (`act_graph_node_schema_draft.json`) from a single indoor clear-room to an outdoor ravine vignette tile-type.
2. **Encodes R1–R9 as an ALGORITHM** — each rule becomes (a) a concrete generation step and (b) a Gate-1 check that the rule held. The rules are CARRIED (they travel with the generator), never baked as coordinates.

The output is the carry chain: **author ONE exemplar ravine tile → seed-vary to 4 distinct vignettes → snap into a 2×2 → A* traverses the assembled map start→end.**

---

## 0.5. Load-bearing design-fit finding (Matt's call) — LINEAR vs SQUARE assembly

The Legolas research returned an unambiguous genre signal: **every ARPG ravine/gorge/pass zone is LINEAR** — a narrow corridor, not a square. D2's three gorge-family zones (Spider Forest, Great Marsh, Flayer Jungle) are all **64×192 tiles (3:1 aspect)**; D2's near-square 80×80 zones (Blood Moor, Cold Plains) are the OPEN-field archetype, NOT ravines. Torchlight's "Passes," D4's tube dungeons, Grim Dawn's "Passages" — all linear. The genre says: *the corridor IS the ravine; a square open space is a field.*

This is in direct tension with the 2×2-square assembly locked in the plan doc §1. The tension is real, not cosmetic: **the ravine's entire structural value (plan §2) is the bounded corridor where walls = boundary. A square open footprint undercuts the very thing the ravine buys us — it reads as Blood Moor (open field), not Spider Forest (gorge).** A 2×2 can be rescued by snaking a U/S-corridor through it (R6 topology note), but that adds interior-turn complexity AND still reads more "open arena with a path" than "gorge."

**gandalf recommendation: shift to 1×4 LINEAR assembly (a straight gorge stretch).** Rationale:
- It IS the genre-canonical ravine shape (Spider Forest's spine, exactly).
- The edge-socket contract (R4) is **topology-agnostic** — this swap is FREE; nothing in the geometry/gate contract changes (the plan doc itself flagged "[A 1×4 strip is the alternative; the edge-socket contract handles either]").
- It reconciles with the committed SE→NW oblique camera: a gorge receding along the sightline is the strongest possible depth read (the three-plane logic of plan §2 lands hardest down a corridor's length).
- It makes R7 focal-points into **pacing beats along a path** (encounter rhythm) instead of four quadrants of a square — the genre's "elite pack every 10–20 tiles of travel" cadence (research §1d) maps directly onto a linear 4-vignette stretch.

**This overturns a decision Matt locked, so it is a RECOMMENDATION, not a commit.** If Matt keeps 2×2, the spec still works (U/S corridor); the sizing below is given per-tile and applies to either topology. **Matt decides.** Everything downstream of this section is topology-neutral except the assembly diagram in §5 Stage C.

## 1. The product (locked, from the plan doc §1–2)

- Enchanted Forest biome; ravine/gorge structure bounds the play space (walls = boundary, rim trees = never-entered false-front, play on the gorge floor).
- 4 procedural "middle" vignettes; hand-authored start/end bookends; 2×2 square assembly; single combat plane (R1: one floor Y).
- Three depth planes on the oblique sightline (gorge floor / rim band / false-front rim trees) — ports the crypt's layered-far-wall depth read.

---

## 2. The generalized node schema — `ravine_vignette` tile-type

Port of `act_graph_node_schema_draft.json`. Field-by-field carry (CONFIRMED = ports as-is; GENERALIZED = same concept, outdoor form; NEW = ravine needs it, crypt didn't):

| Crypt field | Ravine carry | Notes |
|---|---|---|
| `node_type` | `architected_outdoor_ravine_vignette` | a tile IS its type; drives focal-element class + socket topology |
| `footprint.playable` | GENERALIZED | the gorge-FLOOR walkable extent. **`20 m × 20 m` per tile (8×8 tiles @ 2.5 m grid)** — **NO LONGER `_invariant:true`** (28×28 sim-inheritance removed; re-derived from genre research, §5 sizing table) |
| `footprint.visual` | GENERALIZED | **`35 m × 35 m` per tile** = playable + 2×7.5 m rim band (gorge walls + false-front rim trees) |
| `annulus_band_m` | GENERALIZED → **rim band** | **7.5 m each side** (ports the crypt annulus). The up-slope rim between the walkable floor and the false-front. ALL terrain undulation + non-passable scatter lives here (R9) |
| `fight_shell_ref` | CONFIRMED (with caveat) | still a read-only pointer to a spawn set — but the SHELL SIZE is now Legolas-derived, not `elite_pack`'s 28×28. Open cross-seam Q (plan §4): does re-sizing feed the balance sim? Routes to KR/gamora. |
| `kit_ref` | GENERALIZED | outdoor kit (enchanted-forest: rock-wall modules, tree prefabs, foliage scatter, water/shrine focal props). Grid locked per kit before placement. |
| `register_preset` | CONFIRMED | a named outdoor register held constant across all 4 tiles (NO per-tile laddering — spatial coherence is the variable under test) |
| `sockets` | GENERALIZED → **edge-sockets (R4)** | the load-bearing generalization — see §3. Crypt = POINT-socket (a door). Ravine = EDGE-socket (a shared rim+floor profile along a whole tile edge). |
| `vertical_elements` | GENERALIZED | crypt stair+mezzanine → ravine focal verticals (fallen-tree bridge / rope-bridge overhead / waterfall). Same both-ends-land load-path discipline. |
| `dressing_rules` | CONFIRMED | structure-scale (grid-snapped, few: great-trees, rock outcrops, the focal prop) vs scatter-scale (Poisson foliage, rim-band only). Two rule-sets. |
| `nonpassable_group` | CONFIRMED | `nonpassable_dressing` collision group ports verbatim |
| `gate1_invariants` | GENERALIZED | the ported 6→N criteria — see §4 |
| — | NEW: `focal_element` | R7. One hero element per vignette (the thing that makes it a vignette, not a tile). Class enum below. |
| — | NEW: `rim_profile` | R3/R4. The per-edge sampled rim-height curve + max-adjacent-delta. The snap currency. |

**`focal_element` enum (R7):** `fallen_greattree_bridge` · `glowing_pool` · `rockwall_shrine` · `rope_bridge_overhead` · `waterfall`. Exactly one per vignette; the 4 chosen ones must be distinct.

---

## 3. The edge-socket contract (R4) — the load-bearing generalization

The crypt proved a **point-socket**: a door at a grid cell with an orientation index, and the gate checks the door is a wall-variant on the shared grid. The ravine needs the same *snap-by-construction* guarantee along a whole **edge**.

**Definition.** Each tile edge publishes an **edge-socket** = `{edge, floor_profile, rim_profile, corridor_opening}`:
- `floor_profile` — the floor-Y samples across the edge (R1: constant Y, so this is flat — but the contract carries the general case for free).
- `rim_profile` — the rim-height samples across the edge (the gorge-wall top along that seam).
- `corridor_opening` — the [start,end] span along the edge where the walkable gorge floor crosses the seam (R6).

**The contract (snap-by-construction, NOT by-tolerance).** Two abutting tiles share ONE edge-socket: the second tile **consumes** the first's published profile rather than generating its own. Therefore the seam is continuous *by construction* — there is no tolerance check that can fail, because there is no second independent profile to disagree. (This is the crypt's "door is a wall-variant on the shared grid" generalized: the shared grid becomes the shared edge-profile.)

**Consequence for the rules:**
- **R3 (rim slope-continuity)** now governs ONLY the *within-tile* rim (max-delta between adjacent rim samples inside a tile). The *seam* is exact by R4. R3's cross-seam clause is subsumed.
- **R5 (seam keep-out band)** — free-scatter (Poisson foliage/rocks) insets from every edge by the keep-out width; only edge-matched rim features touch the seam. Direct port of the crypt annulus discipline (structure in the band, scatter inset). No cross-seam overlap possible.
- **R6 (path-corridor + A* continuity)** — the `corridor_opening` of abutting edges must align (they do, by R4 consumption). A* across the assembled 2×2 must traverse start→end. **Topology note:** a single entry+exit visiting all 4 cells of a 2×2 is a U/S-shaped gorge with interior turns — so the edge-socket must support a corridor that ENTERS one edge and EXITS an adjacent OR opposite edge. The adjacency table (§5) pins which.

---

## 4. The ported Gate-1 — `check_ravine_vignette_gate1` (criteria)

Generalize the crypt's 6 camera-independent, engine-truth structural criteria. Each maps to a rule. (Drax owns the GDScript; this is the design contract the gate must enforce.)

| # | Crypt criterion | Ravine criterion | Rule | Engine-truth check |
|---|---|---|---|---|
| 1 | no structure overlaps | no structure overlaps (great-trees/rock-outcrops/focal-prop AABBs don't interpenetrate; **no tree stacks**) | R2 | AABB interpenetration > eps on all axes; PLUS Poisson min-spacing assertion on tree centers |
| 2 | door = wall-variant on shared grid | **edge-socket continuity**: abutting tiles share one floor+rim profile; corridor openings align | R4 | per-seam: tile B's edge-profile == tile A's published profile (exact, by construction — assert equality) |
| 3 | A* entrance→exit | A* traverses the **assembled 2×2** start-bookend→end-bookend across the gorge floor | R6 | BFS/A* over the assembled passability grid; path EXISTS through all required cells |
| 4 | stair really climbable | **focal-vertical load-path**: the bridge/rope-bridge/waterfall both-ends-land; no false-affordance | R7+R8 | both-ends-land (port verbatim); PLUS rim-aperture check: no walkable escape from the gorge floor |
| 5 | fight-spawn parity | spawn parity: N-in==N-out; **all spawns inside the playable gorge floor** (not the rim band) | (shell) | multiset compare spec vs placed; all inside playable footprint |
| 6 | no name-clash on reload | (ports verbatim — bake hygiene) | — | .tscn structural signature: no [node] serialized into an instance subtree |
| 7 (NEW) | — | **rim slope-continuity within tile**: adjacent rim samples within max-delta | R3 | per-tile rim curve: max |Δ| between adjacent samples ≤ threshold |
| 8 (NEW) | — | **no false-affordance on rim**: apertures/side-canyons never create a walkable exit from the floor | R8 | flood-fill from gorge floor must NOT reach the rim-top / outside the visual footprint |

Criteria 7–8 are the genuinely-new outdoor gates; 1–6 are ports. The **generate→gate→graduate loop carries as-is**: every human catch ("that tree's floating", "you can walk up that slope and out") becomes a new criterion. We already own the rule-discovery engine (plan §6) — we do not need WFC to find rules; the gate loop finds them.

---

## 5. The generation pipeline — exemplar → seed-vary → assemble

**Stage A — author ONE exemplar ravine tile (hand-authored, gate-passing).** A single canonical vignette with one focal element (recommend `fallen_greattree_bridge` — the most legible gorge-spanning hero). It must pass criteria 1–2,4–8 standalone (criterion 3 needs the assembly). This is the "author one good ravine, read off the constraints it implies" exemplar (plan §6 — the design-method cousin of substrate-led; the gate loop, not WFC, reads off the constraints).

**Stage B — seed-vary to 4 distinct vignettes.** Hold the rule set + register constant; vary the seed to produce 4 tiles with DISTINCT focal elements (R7: the 4 chosen `focal_element`s must differ). Intra-tile scatter = Poisson-disk + raycast-to-terrain + min-spacing (R2) — NOT WFC. Each tile re-passes the standalone gate. **This is the carry test:** if the rules carry, seed-variation yields 4 coherent-but-distinct vignettes with no per-tile hand-authoring.

**Stage C — assemble into 2×2.** Hand-authored adjacency table routes the corridor through all 4 cells (U/S-shape per R6 topology note) and pins start-bookend→tile→tile→tile→tile→end-bookend ordering. Edge-sockets consume shared profiles (R4) → seams continuous by construction. Run the full assembled Gate-1 (criterion 3: A* start→end). **Assembly + traversal passing IS the carry proof.**

**Sizing inputs (Legolas-derived; replaces 28×28):**

| Input | Value | Derivation (research artifact) |
|---|---|---|
| `playable.w_m × h_m` per tile | **20 m × 20 m** (8×8 @ 2.5 m grid) | combat corridor 6–10 tiles wide (research §2c) → 8 tiles = 20 m, mid-range comfortable for AoE; square per-tile for snap-uniformity |
| `corridor_opening` width | **full 20 m** (1×4 straight) / **~15 m, 6 tiles** (2×2 snaking turn) | linear gorge = full-width seam; snaking turn narrows the opening at interior corners |
| rim band | **7.5 m** each side | ports crypt annulus |
| per-vignette **spawn budget** | **trash 6–10; elite pack 0–1** | the *encounter-pull* unit (research §1d), NOT a whole-zone count: D2 pull = 1–3 trash groups (3–12) + 0–1 elite; tuned to mid-D2/D3 density |
| total across 4 vignettes | **~30–42 monsters; ~2 elite packs** | sits in the D2 open-zone family (37–65) — right for a short connective stretch, not a full zone |
| assembly topology | **1×4 LINEAR recommended** (Matt's call, §0.5) | research: ravine archetype is genre-canonically linear; 2×2 falls back to U/S corridor if Matt keeps it |

**Spawn-budget pacing (R7 focal-points double as elite anchors):**
- Vignette 1 (entry): trash only (~6–8)
- Vignette 2 (focal — fallen-tree bridge): trash (~6–8) + 1 elite pack (3–5)
- Vignette 3 (variety): trash only (~6–8)
- Vignette 4 (focal — shrine/waterfall, last beat before end-bookend): trash (~6–8) + 1 elite pack (3–5)
- This is the genre "elite pack every 10–20 tiles of travel" cadence (research §1d) mapped onto the 4-vignette stretch.

**Unit note:** adopt **1 tile = 2.5 m** as the working conversion — it matches the crypt grid AND the D2 community estimate (~2–3 m/tile; research §1a + gap #1). NOT Blizzard-official, so flagged as a working assumption, re-derivable if play-testing says the corridor reads too wide/narrow.

**Scale-path note (do NOT build now):** at N=4, WFC is overkill (it earns its keep at 50+ tiles, Diablo/PoE scale). The clean edge-socket + hand-authored adjacency table suffices. WFC is NAMED as the scale-path; the Legolas §5.4 survey decides whether to adopt it for the later act-scale generator on evidence.

---

## 6. Open items carried OUT of this spec (not resolved here)

- **Sizing/density — RESOLVED** (Legolas return; §2 footprint + §5 table filled). 20×20 m playable per tile replaces 28×28.
- **Assembly topology — Matt's call (§0.5)** — 1×4 linear (gandalf-recommended, genre-canonical) vs 2×2 square (locked-but-now-evidence-challenged). Free swap either way (R4 topology-agnostic).
- **Balance-sim feedback question (plan §4) — sharpened, routes to KR/gamora.** Two coupled sub-questions now: (1) does re-sizing the gorge floor feed back into gamora's balance sim? (spatial sim → yes; abstract sim → no). (2) **The `fight_shell_ref` mismatch:** the crypt consumed `elite_pack` (a square 28×28 shell). A 20×20 m corridor tile needs a CORRIDOR-shaped shell with spawns that fit the narrower playable footprint — the existing square shell's spawn coords may fall outside the new playable (Gate-1 crit-5 parity would FAIL). gamora owns `arena_scenarios.json`; a corridor-shaped shell (or a per-vignette spawn budget per §5) is needed. NOT a design-seam call to resolve — but design SETS the budget (§5), gamora REALIZES the shell.
- **Kit selection** — the enchanted-forest outdoor kit (rock-wall + tree + foliage + focal props). Needs the asset-availability pass (drax/galadriel territory once the spec is sizing-complete).
- **Drax GDScript** — `check_ravine_vignette_gate1.gd` (the §4 criteria) + the exemplar tile generator are drax's to build from this design contract; gandalf reviews against the rules.

---

## Sign-off
gandalf, 2026-06-20. Structural skeleton authored against the proven crypt schema + Gate-1; sizing/density then set from the Legolas genre-research return (substrate voted; 28×28 retired; 20×20 m playable per tile + encounter-pull spawn budget). One load-bearing design-fit decision surfaced for Matt (§0.5: 1×4 linear vs 2×2 square — the genre says linear). Cross-seam balance + shell-reshape question routed to KR/gamora (§6). Pending Matt's topology call, the spec is firing-ready for drax (geometry + gate contract complete; drax owns `check_ravine_vignette_gate1.gd` + the exemplar generator).
