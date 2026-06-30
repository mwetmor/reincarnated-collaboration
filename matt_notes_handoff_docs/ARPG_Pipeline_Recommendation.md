# ARPG Act Generation — Pipeline & Procedural Map Recommendation

**Project:** Godot ARPG + serial content generation engine
**Audience:** Claude orchestrator / designer / judge team
**Status:** Architecture recommendation — supersedes the snapshot-scoring loop
**Core principle:** *The AI builds the parts and the rules. The generator assembles the level. Humans author the intent.*

---

## 1. The reframe (read this first)

The current pipeline asks the Claude designer to author **finished levels**, then grades the output with a visual judge. That is the single hardest job to give an agent, and it is exactly where the "AI tells" come from — uncanny geometry, clipping, arrangements that no human designer would choose.

The fix is to **move the AI off the critical path of final geometry.** Levels are no longer authored by an agent. They are *assembled at runtime* by a deterministic generator from three classes of input:

| Layer | Owner | What it produces | Why it lives here |
|---|---|---|---|
| **Intent** | Human (Hale) | Hand-authored vignettes / set-pieces | Carries deliberate artistic meaning; immune to AI tells because it isn't AI geometry |
| **Structure** | Deterministic generator (code) | Macro layout, node graph, seeded per-run variation | Variety you can trust and reproduce; no live AI re-rolling |
| **Content** | Claude pipeline | Tile pools, StyleProfiles, variant rooms, vignette concepts | This is where the AI is genuinely fast and good |

Everything below follows from this table.

---

## 2. Chosen map strategy: Graph grammar + vignette hybrid

After comparing graph-grammar templates, prefab meta-tile stitching, Wave Function Collapse, algorithmic-layout-plus-substitution, and cyclic generation, the recommended approach for a Synty-modular ARPG act is a **hybrid**:

- **Graph grammar** for the macro structure of the act — guarantees pacing and the existence of boss / shop / branch nodes.
- **Prefab meta-tiles** (large Synty chunks) to fill *architected dungeon* nodes — big chunks read as deliberate; offset entrances mask the tiling.
- **Wave Function Collapse (socket-based, 3D, C#)** to fill *organic biome field* nodes — local coherence from a small tile set.
- **Hand-authored vignettes** dropped into nodes flagged `needs_setpiece` — the artistic anchors.

### Why this hybrid

- Synty kits are built to snap on consistent socket boundaries → favors grid/socket assembly (meta-tiles + WFC).
- Graph grammar gives the "purposefully architected" pacing the pure-procedural options can't.
- Vignettes give intent that no generator produces.
- **Seasonal swap is trivial** because of the *separation principle* (next section).

---

## 3. The separation principle (this is what makes seasons cheap)

> **Keep the layout/graph logic theme-agnostic. Put everything theme-specific into a swappable pool.**

A season is not a new generator. It is a new **content pool** plugged into the same generator:

```
Generator (theme-agnostic, never changes per season)
   │
   ├── consumes ──> ActGraph definition      (node types, pacing, constraints)
   ├── consumes ──> TilePool                 (Synty chunks tagged by socket + theme)
   ├── consumes ──> StyleProfile             (palette, density, dressing rules)
   └── consumes ──> VignetteLibrary          (hand-authored set-pieces)

Season swap = swap TilePool + StyleProfile + VignetteLibrary. Graph logic untouched.
```

This is the Diablo I insight: separate the abstract passability/layout pass from the art pass, so reskinning touches only the substitution table — never the algorithm. It also dovetails with the serial content engine, whose JSON packets *are* the TilePool/StyleProfile inputs.

---

## 4. Repointing the Claude team

The agents keep their identities but change their targets. Stop authoring levels; start authoring the generator's inputs.

### Orchestrator
- Owns the per-node assembly pipeline and the seasonal-swap batch jobs.
- Routes fight-sim JSON to the correct layer (see open question §8).
- Manages validation gates (playability A*, socket-fit, StyleProfile conformance).

### Designer
- Generates **TilePool definitions** and **StyleProfiles** (the serial-engine JSON it already outputs).
- Authors **variant connective rooms** in bulk (the boring tissue between set-pieces).
- Proposes **vignette concepts** for Hale to hand-finish — does *not* ship final vignette geometry.
- **Works directly in Godot via MCP** (see §5), populating/dressing *within* generator-laid constraints.

### Judge
- **Stops grading whole levels.** New target: per-asset / per-tile-fit conformance to the StyleProfile.
- Narrow target = far fewer noisy signals = fewer false "AI tells" verdicts.
- Cross-model is reasonable to reduce correlated blind spots, but **use a current vision model** (GPT-5-class or Gemini), not GPT-4 — it's dated now. The *what-it-judges* change matters more than the model swap.

---

## 5. Move the Designer into Godot via MCP

The snapshot-scoring loop (guess → render mp4/png → score → guess) is **open-loop**, which is *why* geometry drifts uncanny. A Godot MCP closes the loop:

- Agent manipulates **real nodes** — snaps Synty pieces to actual sockets, respects collision, reads the scene tree.
- Structural correctness is enforced **by the engine**, not retroactively by the judge.
- Judge is freed to catch only *aesthetic* problems, not "wall clips through floor." Removes an entire class of AI tells.

**Guardrail:** the in-Godot agent dresses and populates *inside* the generator's topology. It must **not** freely author whole-level topology in-engine — that just relocates the open-loop problem inside Godot. Topology stays in the deterministic graph generator.

---

## 6. End-to-end pipeline

```
┌──────────────────────────────────────────────────────────────────────────┐
│  OFFLINE — content authoring (slow, batched, AI + human)                   │
└──────────────────────────────────────────────────────────────────────────┘

  [Fight-sim engine] ──JSON──┐
                             ▼
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │  routes inputs, owns batch jobs
                    └────────┬────────┘
                             ▼
        ┌────────────────────┴────────────────────┐
        ▼                                          ▼
┌───────────────┐                        ┌───────────────────┐
│   DESIGNER    │                        │      HALE          │
│ (Godot MCP)   │                        │  hand-authors      │
│               │                        │  15–30 vignettes   │
│ • TilePools   │                        │  (set-pieces,      │
│ • StyleProfiles│                       │   story beats,     │
│ • variant rooms│                       │   mini-bosses)     │
│ • vignette     │ ──concepts──────────► │                    │
│   concepts     │                       └─────────┬──────────┘
└───────┬────────┘                                 │
        ▼                                           │
┌───────────────┐                                  │
│    JUDGE      │  per-asset StyleProfile           │
│ (cross-model) │  conformance only                 │
└───────┬───────┘                                   │
        ▼                                           ▼
   ┌─────────────────────────────────────────────────────────┐
   │   CONTENT POOLS  (versioned, per-season)                 │
   │   TilePool  +  StyleProfile  +  VariantRooms  +          │
   │   VignetteLibrary  +  ActGraph definition                │
   └────────────────────────────┬────────────────────────────┘
                                 │
┌────────────────────────────────────────────────────────────────────────┐
│  RUNTIME — assembly (fast, deterministic, NO live AI)                    │
└────────────────────────────────────────────────────────────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │   SEEDED GENERATOR       │  seed → reproducible run
                    │                          │
                    │ 1. Graph grammar expands │  pacing, boss/shop/branch
                    │    ActGraph → node list  │
                    │ 2. Per node, pick filler:│
                    │    • setpiece → Vignette │
                    │    • dungeon  → meta-tile│
                    │    • field    → WFC (C#) │
                    │ 3. Stitch via sockets    │
                    │ 4. VALIDATE:             │
                    │    • A* start→end (retry)│
                    │    • socket-fit check    │
                    │    • contradiction retry │
                    │ 5. Dress via StyleProfile│
                    └────────────┬─────────────┘
                                 ▼
                       ┌───────────────────┐
                       │   PLAYABLE ACT     │
                       │  (10–15 areas)     │
                       └───────────────────┘
```

### Seasonal swap, in one line
Swap `TilePool + StyleProfile + VignetteLibrary` → same generator → a new themed act of 10–15 areas. No code change.

---

## 7. How this hits the three goals

- **Speed of development** — AI batch-produces pools/rooms/profiles offline; the generator assembles in milliseconds at runtime. No agent-per-level wait.
- **Player-unique experience** — deterministic seeded graph guarantees real per-run variation; nothing re-rolled live by AI.
- **Purposeful artistic feel** — hand-authored vignettes carry intent; the in-Godot MCP agent enforces structural correctness so nothing reads as broken; the narrowed judge keeps dressed assets on-theme.

---

## 8. Open decision that steers implementation

**Is the fight-sim JSON the macro layout, or a single encounter?**

- If the **6 connected areas ARE the act's structure** → the graph grammar *wraps* the existing JSON; the JSON defines the node graph directly.
- If it's **one combat encounter** → it becomes a single node inside a larger generated act; the graph grammar adds the surrounding 9–14 areas.

This answer determines whether the generator consumes or replaces part of the current JSON contract. Resolve before building the ActGraph schema.

---

## 9. Concrete next steps

1. Decide §8 (encounter vs. act-structure).
2. Pick the Godot MCP and stand up the Designer's in-engine loop on one node.
3. Define the `ActGraph` + `TilePool` + `StyleProfile` JSON schemas (the serial engine likely already half-produces these).
4. Hand-author 3 vignettes as a vertical slice; flag matching nodes `needs_setpiece`.
5. Implement the seeded generator's validate pass (A* playability + socket-fit) before scaling content.
6. Swap the judge to per-asset StyleProfile conformance on a current vision model.
