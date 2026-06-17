# Legolas Mode-A Research Commission — Modular Procedural Dungeon/Biome Generation for Godot

**STATUS:** ACTIVE COMMISSION (Legolas Mode-A analytical research; Matt-authorized 2026-06-17)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 (Pattern-B battle-room visual session) — authorized a wide analytical scan for modular procedural dungeon + outdoor-biome generation options that work in Godot, to inform a *later* modularization phase of the battle-room replica work.
**Mode:** A (analytical research; read-only; web + prior-art synthesis). NOT a Mode-B catalogue crawl.
**Findings home:** file under `agentic_orchestration/legolas/research/2026-06-17-godot-procgen/` (synthesis + sources) per your OP.
**Companion docs:** `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (the sim-invariant vs presentation principle this research extends); `agentic_orchestration/gandalf/notes/2026-06-16-drax-render-spec-and-architecture-audit-camera.md`.

---

## 0. Why this research

We've validated that a single battle room can hold register-2 premium AND fight-readability (the boss-arena scorecard). The next ambition: treat these rooms as prototypes for encounter/room patterns that work both as fights and aesthetically, then **(A)** build them across all Synty packs/biomes and **(B)** make them modular so they assemble into procedurally-varied dungeons that play slightly differently every run/player. This commission scouts the **options for the procedural-assembly layer in Godot** — tooling, packs, codebases, integration patterns — so the team can make an architecture decision *before* adopting anything. It is options-and-fit, not an adoption recommendation.

## 1. The framing that governs the ENTIRE search (read this first)

"Procedural" in our system is **two layers**, and every option you find must be classified by which one it serves:

- **FIGHT layer (the sim-invariant) — owned by the engine; NOT in scope for adoption here.** The reincarnated-engine is the single source of truth for spawn positions, the playable footprint, and damage geometry. Procedural *fight* variation belongs there (rocket's generator), never in a Godot pack.
- **PRESENTATION-ASSEMBLY layer — the TARGET of this research.** Given a footprint/spec handed down by the engine, how does Godot assemble a modular, varied, dressed world *around* that fixed fight?

**The disqualifying pattern:** any tool that insists on owning its OWN layout generation and cannot consume an external spec would re-create the two-sources-of-truth conflict the engine's authority exists to prevent. Flag these explicitly. The IDEAL tool **assembles/dresses a GIVEN footprint**; a tool that generates layout is only useful if its layout authority can be subordinated to (or swapped out for) our engine's spec.

**Evaluate every option against:** *"Which layer does this serve, and can it respect the engine's authority over the sim-invariant?"*

## 2. Research questions, by category

### Category 1 — Godot generation frameworks & codebases (open-source / community)
- **Wave Function Collapse (WFC)** implementations for **Godot 4.x** — which exist, maturity, maintenance recency.
- **Graph/grammar-based dungeon generators** — cyclic-dungeon generation in the Joris Dormans / *Unexplored* / "Ludoscope" lineage; generative grammars.
- **Room-graph / template-stamp generators** — the Diablo tile-set / Hades room-graph model (hand-authored chunks placed by rules).
- **Cave/organic generators** — cellular automata, marching squares.
- For each: repo activity + last commit, license, Godot 4.x compatibility, doc quality, and crucially **does it emit a spec/data you can DRIVE, or is it a black box that owns the result?**

### Category 2 — Purchasable Godot procedural packs (marketplaces)
- Godot Asset Library, itch.io, and other marketplaces: procedural dungeon/level-gen kits, scatter/placement tools.
- For each: what it **actually** does (layout / assembly / scatter / terrain — be precise), Godot version, cost, **commercial-use license terms**, and whether it can consume an external footprint.

### Category 3 — Synty modular packs across biomes (asset-side modularity)
- Which **Synty POLYGON** packs are built for **true modular tiling / socket-snapping** (grid-modular building kits) vs hero-prop / set-dressing packs.
- **Biome coverage map:** dungeon, dark fantasy, nature/forest, desert, sci-fi, fantasy kingdom, apocalypse, etc. — which biomes have *modular-buildable* (not just prop) coverage.
- Godot import path + how the modular pieces sit on a GridMap / MeshLibrary / snapping workflow.

### Category 4 — Native Godot assembly substrate + integration patterns
- **Godot's native GridMap + MeshLibrary** as the modular-3D-tiling substrate — is it the right assembly target for spec-driven rooms? Limits at our scale.
- **Scatter/placement addons** (proton-scatter-style) for organic dressing density.
- **Terrain tools** for outdoor biomes (heightmap terrain addons) — the outdoor analog of the dungeon problem.
- **The integration pattern that matters most:** how teams drive Godot assembly from an EXTERNAL layout spec (JSON/data → GridMap population / prefab placement). This is the mechanism that lets the engine own layout and Godot own dressing.
- **The hybrid pattern:** authored room "stamps"/prefabs placed by a graph + procedural connective tissue (Hades / Dead Cells / Spelunky / Diablo) — how is it implemented in Godot specifically.

### Category 5 — Genre / design prior art (how the best do it)
- **Module granularity** across exemplars: tile-set (Diablo), 4×4 room template (Spelunky), biome room-pool (Dead Cells), room-graph (Hades), cyclic-dungeon-grammar (Unexplored). Which granularity fits a *spec-driven ARPG*.
- The **authored-vs-procedural split** each uses — what stays hand-built (bosses, set-pieces, narrative beats).
- Named **anti-patterns** (Diablo IV "same-y" dungeons; pure-noise soullessness, No Man's Sky launch) and what the good examples did to avoid them.
- **Outdoor-biome** procedural precedents (open-world ARPG zones) vs enclosed dungeons — note where they're different problems.

## 3. What good looks like (deliverable)

An **options matrix** — each option × { layer-served · what-it-actually-does · Godot-4.x-compat · license + commercial terms · maturity/maintenance · cost · integration-path-to-external-spec · biome/asset coverage · **engine-authority-fit verdict** }. Plus a short narrative synthesis and **your top-3 candidates with reasoning**. NOT an adoption call (that's a later team decision) — options + fit, with the layering verdict explicit for each.

## 4. Constraints + context
- **Engine:** Godot 4.x.
- **Assets:** Synty POLYGON modular packs; locked visual target is **register-2** (low-poly premium-lit; Dark Fantasy validated, other biomes need per-biome register calibration — out of scope for you, but note asset availability).
- **Game:** solo ARPG, Diablo-class loot/build; seasonal-journey structure (biome variety is inherent to the game, not a stretch goal).
- **Read-only.** License + IP flags matter — we must know commercial-use terms for anything purchasable.

## 5. Out of scope
- **Fight-balance / encounter-composition generation** — that's the engine/rocket (the FIGHT layer); do not evaluate tools for it.
- **The adoption decision** — you surface options + fit; the team decides.
- **Mode-B asset cataloguing** — the Synty-corpus crawl is a separate workstream; here you only need biome *coverage/modularity* at a survey level, not a per-asset catalogue.

---

**Signed:** gandalf, 2026-06-17.
**For:** commissioning a Legolas Mode-A scan of the Godot procedural-assembly option space — frameworks, packs, Synty biome modularity, native-GridMap integration patterns, and genre prior art — framed throughout by the engine-owns-the-sim-invariant / Godot-owns-presentation-assembly layering, so the team can choose an architecture-compatible path before adopting any tool.
