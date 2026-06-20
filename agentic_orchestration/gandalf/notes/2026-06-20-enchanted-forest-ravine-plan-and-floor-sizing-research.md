# Enchanted-Forest Ravine — 4-Vignette Procedural Plan + Floor-Sizing Research Commission

**Status:** ACTIVE PLAN — next-session loader. Pattern B disposition (Matt + gandalf, 2026-06-20). Nothing fires this session (context wind-down); this doc is the start-state for next session.
**Author:** gandalf (design steward).
**Parents:** crypt-vault PoC notes (`2026-06-19-crypt-vault-*` ×3); the architecture conversation this session (carry thesis: coordinate-vs-rule · gate-as-carry-mechanism · carry-layers); `reincarnated-godot/data/act_graph_node_schema_draft.json`.
**Supersedes-in-part:** the schema-draft's `footprint.playable._invariant:true` "sacrosanct 28×28" premise — see §4.

---

## 1. The product unit (locked this session)

- **Biome:** Enchanted Forest. Reference target: **Slime's Forest of Jura** (reincarnation-isekai; enchanted forest; single great-tree focal landmark) + PoE twilight/overgrown zones + D2 outdoor acts.
- **4 vignettes, ALL "middle" type.** The map's **start + end are HAND-AUTHORED** (the hero/bookend moments — genre-canonical: D2/PoE hand-author town + act-boss, procgen the connective middle). The 4 procedural vignettes are the connective tissue, ordered 1→2→3→4 as the middle traversal.
- **Assembly:** 4 same-dimension SQUARE tiles snap into a **full square (2×2)**. Single playable floor Y across all 4 (combat on one plane). [A 1×4 strip is the alternative; the edge-socket contract (R4) is topology-agnostic and handles either.]

## 2. The load-bearing insight — the RAVINE solves the outdoor-boundary problem for FREE

The hardest outdoor problem flagged in the design conversation was *"how do you bound the play space without walls / without an invisible-wall-in-a-field."* The ravine dissolves it: **the ravine IS the boundary.** Overgrown rock walls on the sides (can't climb out — natural, not a cheat); trees on the rim above (the never-entered false-front background — the outdoor analog of the crypt's never-capped tower); play on the gorge floor. Three planes along the oblique sightline ⟹ the committed camera reads depth, *exactly* the crypt's layered-far-wall logic ported outdoors. This is the single best structural move available for outdoor — it makes "naturally bounded" free, and it makes the focal/landmark composition easy (the gorge frames everything).

## 3. The rule set (Matt's + gandalf-added) — all RULES (carry), never coordinates

**Matt's rules:**
- **R1. Single floor Y** across all 4 tiles (one combat plane).
- **R2. No tree stacks** — two trees never overlap/snap atop one another ⟹ a min-spacing constraint. Canonical tool: **Poisson-disk sampling**.
- **R3. Rim slope-continuity** — adjacent rim rocks can't slope up/down too severely ⟹ max-delta between adjacent rim sample heights, within a tile AND across seams.

**gandalf-added:**
- **R4. Edge-socket = shared rim+floor profile.** Generalize the crypt's POINT-socket (a door) to an EDGE-socket: each tile edge publishes a rim-height + floor-level profile; abutting tiles CONSUME the shared profile, so the seam is continuous BY CONSTRUCTION, not by tolerance. This is the snap contract. (R3 then governs only the within-tile rim; the seam is exact.)
- **R5. Seam keep-out band.** Free-scatter (trees/rocks/foliage) insets from each edge; only edge-matched rim features touch the seam ⟹ no cross-seam overlap (handles R2 at the seams too). Direct reuse of the crypt's annulus discipline (structure in the band, scatter inset).
- **R6. Path-corridor socket + A* continuity.** The walkable gorge floor must connect entry-edge→exit-edge per tile and align across seams; A* across the assembled 2×2 must traverse start→end. (The crypt's crit-3, generalized to the assembled map.) Topology note: a single entry+exit visiting all 4 cells of a 2×2 = a **U/S-shaped gorge with interior turns** — the edge-socket must support a corridor that ENTERS one edge and EXITS an adjacent or opposite edge.
- **R7. Focal-point-per-vignette.** Each middle vignette gets ONE hero element (fallen great-tree bridging the gorge / glowing pool / shrine carved into the rock wall / rope-bridge overhead / small waterfall) so the 4 read DISTINCT, not 4 identical gorge segments. THIS is what makes them *vignettes*, not tiles — the outdoor analog of the crypt's grand hero wall.
- **R8. No false-affordance on the rim.** Apertures / side-canyons / collapsed sections in the rim are encouraged (variety + light) but must NEVER create a walkable escape from the gorge floor. (The crypt's K-rule.)
- **R9. Terrain-conform = flat gorge floor + terrain in the rim band.** Keep the playable floor flat (cheap, legitimate — most ARPG outdoor arenas are flattish clearings/floors); push all undulation into the rim/annulus. Direct reuse of the two-footprint rule.

## 4. Vestigial removal — gauntlet-sim arena-size as the map-room floor-plan authority

**Recognition (Matt; validated by gandalf):** map rooms have been sized from the gauntlet/balance sim's arenas (the crypt inherited **28×28** from `arena_scenarios.json` `elite_pack`). That's a **category error** — the balance sim sizes arenas for FIGHT MATH; ARPG rooms are sized by GENRE CONVENTION (encounter pacing, screen real-estate, density). The rooms built so far are too large for their enemy counts and don't match ARPG room construction.

- **What's removed:** the gauntlet-arena-dimensions-AS-map-room-sizing. The "sim replica" footprint inheritance leaves the mapping plan.
- **What CARRIES (unaffected):** the two-footprint MECHANISM (playable ⊂ visual; scatter in the annulus/rim band). Sound and biome-general. Only the MAGIC NUMBER (28×28) and its "sim-invariant/sacrosanct" status are removed.
- **What this supersedes:** the schema-draft treated the playable footprint as sim-invariant ground-truth (`_invariant:true`). That premise is now under revision — the playable footprint will be **RE-DERIVED from genre research** (§5), not inherited from the sim. (substrate-led: we pre-imposed 28×28 from the sim; let the genre substrate vote on the real size.)
- **Open cross-seam question (route to knight-rider/gamora next session; do NOT resolve here):** does re-sizing rooms feed back into the balance sim? If gamora's sim models SPACE (kiting / LoS / AoE-overlap), smaller rooms may shift balance; if it's spatially ABSTRACT (DPS/EHP/time-to-kill), it won't. The answer determines whether room-resizing is presentation-only or has a balance-loop consequence.
- **Does the balance sim itself survive?** YES, as a balance tool — only its role as map-room-sizing authority is removed. (Confirm with Matt next session if he intends a broader cut.)

## 5. Legolas research commission (Mode A — analytical; READY TO FIRE next session)

**Goal:** establish the genre-canonical ARPG room-size + monster-density truth that replaces the removed sim-derived sizing.

**Questions:**
1. **Ravine / mountain-pass floor plans** — canonical layouts for gorge/canyon/pass zones in ARPGs + adjacent genres. Dimensions, corridor widths, how they bound the player, how they branch.
2. **ARPG "middle-room" floor plans** (NOT start/end/unique/boss) — the average connective-room SIZE + SHAPE, in meters and/or tiles. Per-game across **D2, D3, D4, PoE, Last Epoch, Grim Dawn, Torchlight**.
3. **Monster density** — how many monsters, of which archetypes (trash / elite / pack-leader), spawn into these middle-rooms, PER room size. Density = monsters per unit area; pack composition; packs-per-room pacing.
4. **(Fold-in from §6)** — survey procedural tile-layout methods (**Wave Function Collapse** + constraint-solver cousins; Diablo's tile+adjacency system; PoE's map-layout grammar): how the genre actually GENERATES connective rooms, and whether adjacency-constraint methods are worth adopting vs a hand-authored edge-socket contract at small N.

**Deliverable:** a sizing+density table (room size → monster count/type) gandalf consumes to set the playable-footprint truth + per-room spawn budget, replacing 28×28.

## 6. Methodological question — "use a procedural method as the SOURCE of the rules?" (gandalf answer)

Matt asked whether to use a procedural method of choice as output/guidance for the snap-rules, rather than hand-authoring them.

- **The method whose NATIVE abstraction IS Matt's snap-rules is Wave Function Collapse (WFC).** Its whole model = tiles + adjacency constraints + propagation; it only ever places matching edges. It can be authored EITHER by explicit adjacency rules OR by **"learn-from-one-exemplar"** (author one good ravine; WFC infers the adjacency patterns). That exemplar mode IS "use the method to discover the rules" — the design-method cousin of substrate-led discipline (don't pre-impose; let the example vote).
- **BUT WFC's failure mode is exactly our north-star's weak spot:** great at LOCALLY-coherent "looks natural," weak at GLOBALLY-INTENTIONAL "feels authored/purposeful" (Townscaper / Bad North — gorgeous, composition-agnostic). Focal points, paced difficulty, the designed journey must be IMPOSED on top; they don't emerge. Plus contradiction/backtracking overhead.
- **Recommendation — HYBRID, mapped to carry-layers:**
  - **Macro tile layout** (which vignette where + corridor routing through the 2×2): at N=4 this is TINY — a clean edge-socket contract (R4/R6) + a hand-authored adjacency table suffices. WFC is overkill at N=4; it earns its keep at 50+ tiles (Diablo/PoE scale). **Name WFC as the SCALE-PATH** for later.
  - **Intra-tile scatter** (trees/rocks within a vignette): Poisson-disk + raycast-to-terrain + min-spacing (R2). NOT WFC.
  - **Rule DISCOVERY:** we ALREADY have a rule-discovery engine — the crypt's **generate→gate→graduate** loop (every human catch becomes a check). Use it. Optionally seed it by hand-authoring ONE exemplar ravine and reading off the constraints it implies. We don't need to import WFC to discover rules; the gate loop does it. (§5.4 research confirms whether WFC is worth adopting for the scale-path.)

## 7. Next-session sequence
1. Load this doc.
2. Fire the Legolas Mode A commission (§5).
3. On return: set the ARPG room-size + per-room spawn-budget truth (replaces 28×28). Route the balance-feedback question (§4) to knight-rider/gamora.
4. Spec the enchanted-forest ravine vignette generator (§1–3 rules) — ONE exemplar tile first → seed-vary to 4 → 2×2 assembly. (recognition→validate→commit: the seed-variation + assembly IS the carry test.)

## 8. Deferred / gated (carried from the crypt thread)
- **Crypt Gate-3:** still pending Matt's full-res eye on the round-3 frames (`harness_logs/crypt_vault_playercam_round3_2026-06-20/`, esp. Item-5 wall continuity). NOT blocked by the forest pivot.
- **Crypt seed-variation control:** the clean carry-signal experiment on the proven node — near-free; keep available.
- **Push authorization:** 12 commits ahead of origin (crypt rounds 1–3 + others), unpushed, awaiting Matt authorization (Mac team, ADR-006).
- **3 gate-graduation candidates** from crypt round-3 (no-deck-tile-overlaps-stair; every-elevated-mass-traces-a-support; every-wall-uses-canonical-clean-wall-role) — canonicalize at crypt Gate-3 pass (jack-ryan's gate-code territory).

## Sign-off
gandalf, 2026-06-20. Pattern B disposition + next-session plan. Anchors: crypt-vault PoC notes; architecture-conversation carry thesis; node-schema draft.
