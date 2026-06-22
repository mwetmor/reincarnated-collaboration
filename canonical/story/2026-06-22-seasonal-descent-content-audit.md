# Seasonal-Descent Content Audit — Engine Capability × Descent Requirement

> **STATUS: AUDIT** (2026-06-22). This is the **G1-reframed deliverable** — the
> requirements-vs-capability gap analysis that is *the front-half of G2*, not a
> serialization diff. It measures the gap between what the descent (recognition
> record `2026-06-22-seasonal-descent-architecture-recognition.md`) NEEDS and what
> the engine PRODUCES today. Architectural commitments remain deferred
> (recognition → validate-against-evidence → commit). Verdicts marked **[VERIFIED]**
> were read directly from engine code/schema this session; **[CONSULT]** awaits a
> seam-owner judgment.

**Author:** gandalf (story/design steward)
**Session:** Pattern-B with Matt, 2026-06-22 (continues the recognition-record session)
**Parent:** `canonical/story/2026-06-22-seasonal-descent-architecture-recognition.md`
**Engine substrate read:** `export/schemas.py` (`ExportSeason`, `ExportMonster`,
`ExportGearItem`, `ExportFactionCluster`, `ExportMetadata`), `export/arena_scenario_emitter.py`,
`anchor/selector.py`, `generation/` + `anchor/` floor/depth grep, `seasons/season_000046/manifest.json`,
star-lord `export/AGENT_STATE.md`, decisions-log typed-resistance G-C close.

---

## 0. Purpose + the framing guard

The audit exists to answer one question: **does the engine's content model support
the descent's content model?** The answer governs sequencing — you cannot design a
per-floor content contract (G1) as "a projection of what the engine already emits"
if the engine doesn't yet emit the structure the contract projects.

**THE GUARD (load-bearing).** This audit's value is in the **structural rows**, not
the **atom row**. A naive "diff the JSON shape" exercise lights up green on the cheap
rows (the atoms exist) and reports "80% there" — which is false. The expensive,
load-bearing gaps are *generation-model* gaps that a serialization diff cannot see.
If this audit ever reduces to a field-map, it has failed.

## 1. The seam inventory — four seams, one already built

The descent is not one seam. Disentangling them is the audit's first product:

| Seam | What it carries | State |
|---|---|---|
| **Bookend-arena geometry** | Engine→Godot: combat-arena footprint, spawn positions, choke zones, win conditions, tier/archetype slot labels | **BUILT** — `arena_scenario_emitter.py` (sim-parity-by-construction). *This is the entrance + mega-boss bookend seam, and it already works.* |
| **Procedural-middle geometry** | Godot-owned: corridors / junctions / chambers, seeded assembler, socket-snap | **BUILD** — G3 (drax). Zero engine dependency. |
| **Content-binding** | Engine→Godot: which content-unit fills which room-slot, room *type* requested (combat vs boss). NEVER geometry. | **BUILD — trivial.** The only genuinely-new *serialization* layer, and it is small. |
| **Depth-structured content generation** | Engine-internal: floors, per-floor faction roster, depth-tiering, encounter composition | **BUILD — the big one** (G2). Most of the gap table below lives here. |

**One of four is already done.** The bookend-arena seam (`arena_scenario_emitter`)
is exactly the mechanism the authored bookends need. This reframes the descent's
engineering footprint as *one large new capability (depth-structured generation) +
one small serialization layer (binding) + one Godot prototype (procedural middle)*,
sitting on top of a proven arena-parity seam.

## 2. The gap table (the spine)

| What the descent needs | What the engine has today | Verdict |
|---|---|---|
| Floor / depth-as-position | **Zero.** Grep of `generation/` + `anchor/` → every "floor"/"depth" hit is numeric-minimum ("DPS floor", "defense-in-depth"). No positional-depth axis anywhere. | **ABSENT** [VERIFIED] |
| Per-floor sub-anchor (lieutenant per floor) | `select_seasonal_anchor` is **one-per-season**, flat (`anchor/selector.py`). No hierarchy. | **ABSENT as anchor → REFRAMED** (§4) [VERIFIED] |
| Faction-coherent floor roster *generated as* the faction | Phase-5 `faction_clusters[]` cluster a finished pool **post-hoc** (k=3/k=4 GMM; cohesion judge fires against a snapshot) | **PARTIAL — backwards** (§4) [VERIFIED] |
| Depth-tiering = f(depth, exp-level, exp-gear) | per-kit WR/KPM band calibration (solo Profile-A, dm=5.0). `threat_tier` is a *label*, not a depth-curve. Doc 33's curve is design-only. | **ABSENT** [VERIFIED] |
| Encounter-composition per step | `arena_scenario_emitter` emits per-scenario spawn slots (tier/archetype) — but a **hand-authored finite `ALL_SCENARIOS`**, and it emits **geometry** | **PARTIAL — wrong shape** (§3) [VERIFIED] |
| Mega-boss + claimable kit | trial-boss concept exists (`trial_defeat_rate` in metadata); source = §8 open (A/B/C/D) | **PARTIAL** — source is G5 [VERIFIED] |
| Room-binding hints (unit→slot, room *type*; never geometry) | nothing | **ABSENT-but-trivial** [VERIFIED] |
| Atom layer: monster tier/element/resist/skills/move; gear; faction | all present in `ExportMonster` / `ExportGearItem` / `ExportFactionCluster` | **EXISTS** [VERIFIED] |

**Read:** one row EXISTS (atoms). One ABSENT-but-trivial (binding — the only real
serialization work). **Everything expensive is generation-model.**

## 3. Finding A — the boundary is three-regime, not flat

The recognition record §4 says "engine emits CONTENT; Godot owns GEOMETRY." But
`arena_scenario_emitter.py` already ships the engine emitting **arena geometry**
(spawn x/y, width/height, choke zones) to `reincarnated-godot/data/arena_scenarios.json`,
explicitly: *"parity-by-construction: the Godot room consumes the SAME spec the
SpatialFightEngine runs."* That is the **opposite** boundary — and it is **correct**
to be opposite, because a *combat* arena was *balanced in that geometry*, so
presentation must match it or what you see ≠ what was tuned.

So the true boundary is three-regime:

- **Combat-arena geometry → engine-authoritative** (sim-parity). *The bookends.* BUILT.
- **Connective-middle geometry → Godot-authoritative** (procedural). *G3.*
- **Content + binding → engine-authoritative** (the new small layer).

**§4 of the recognition record should be rewritten to this three-regime boundary**,
or the content seam gets built assuming a flat rule the existing arena seam already
contradicts.

## 4. Finding B + Matt's lieutenant reframe

**Finding B (causality).** Phase-5 *generates a flat pool, then clusters it*
(`pm1_algorithm` = "gmm_k3"/"gmm_k4"; cohesion judge against a snapshot). §7 of the
record wants rosters "coherent from birth" — implying *generate under* a faction.
That is a reversal of the generation→clustering arrow.

**Matt's reframe (2026-06-22) — accept the clustering; don't reverse it.** The floor
lieutenant is **not** a newly-generated per-season anchor — it is **the leader of a
faction**. Reuse the existing faction judge / bi-modal clustering; tune it to produce
**as many distinct factions as possible**; each floor = a faction; the faction's
leader = the floor lieutenant. This **de-scopes the per-floor-anchor row** from "new
generation capability (ABSENT)" to "tune existing clustering + designate a leader."
**Steward verdict: embrace it.** It is a real simplification and it is structurally
right (see the unification, below). It rests on three precision-points:

- **P1 — population fork [CONSULT — likely Matt-answerable directly].** Phase-5
  `ExportFactionCluster` clusters **player KITS** (`member_kit_ids` = "surviving kits
  after Phase 4 eviction"), not monsters. The descent's floor-roster is **MONSTERS**.
  So "set the faction judge to produce many factions" needs a definite referent:
  (a) monsters inherit faction from the kit-clustering via a bridge; or (b) the
  relevant judge is **elrond's catalogue/lineage clustering** (the monster/content
  side — which recognition-record §9.2 actually points to); or (c) monsters are
  generated under a faction theme. *This fork must close before "tune the judge" has
  a target.*
- **P2 — coherence vs. count is a measurable tradeoff, not a free knob [VERIFIED
  instruments].** `cluster_compactness` (silhouette) = coherence; `diversity_flag`
  (cosine > 0.85) = faction collision. "As many as possible" hits a **knee** where
  compactness craters / collisions spike. *Runnable experiment (elrond/star-lord):
  sweep k, plot both metrics, find the knee.* That knee = coherent-faction supply
  per season. This **replaces** the ABSENT verdict with "tune k against a measurable
  coherence floor" — far cheaper, and it is the gate.
- **P3 — faction supply across an infinite descent [DESIGN — open].** A single
  season's ~34–40-item pool caps coherent factions at single digits (34 kits / k=8 ≈
  4 members/faction — already thin). An infinite descent needs many floors × many
  re-descents. The thematically-aligned answer: **the faction library accumulates
  across descents**, exactly like the form library — floor N draws from the
  *accumulated* faction pool, deepening each reincarnation. Past lives' enemies
  persist as the world's factions. Gorgeous, but an architecture decision, not a free
  consequence.

**The unification bonus.** Because no leader concept exists today, we add
"designate a faction leader" **once**, and it serves **both** open problems:
floor lieutenant = floor-faction's leader; **mega-boss = the apex / season-faction's
leader** (or the held-out dark faction's leader — §8 Option B/D). This is the isekai
floor-master/overlord hierarchy by construction — *Slime*'s labyrinth guardians under
the dragon; Overlord's floor guardians under Ainz; Solo Leveling's monarchs. **One
primitive, two uses.** That a single small addition closes both the lieutenant and
the mega-boss theming is the signal the reframe is the right shape.

## 5. "Near complete" — recalibrated

"The pipeline is near complete" is **true for what it measures**: the Cycle-14
flat-season content export (loadout/demo) + the arena-parity seam. **Neither is the
descent's content model.** The descent is a *new target* the current "done" does not
cover — `build_unified_season_content_blocks` (the top-level assembly) is Matt-parked,
and even when lifted it assembles the **flat-season** shape. This is not a criticism
of the pipeline; it is the recalibration the audit exists to make explicit, on a desk,
before Godot wires to a flat-season JSON and finds no floors.

## 6. Build-cost ranking of the gap (cheapest → dearest)

1. **Content-binding layer** (trivial serialization; unit→slot + room-type). Small.
2. **Faction-leader designation** (additive; one elevated member per cluster). Small.
3. **Per-floor faction theming via k-sweep** (tune existing clustering to the P2 knee;
   resolve the P1 population fork). Moderate — *tuning + one experiment*, not a rebuild.
4. **Floor / depth-as-position model** (a positional axis the generator lacks). Large.
5. **Depth-tiering = f(depth)** (a new calibration axis; the balance loop is per-kit,
   not per-depth; doc 33's curve must become a *generator input*). Large — and it
   interacts with the §5 "spike is sacred" adjustment algorithm.
6. **Faction library accumulation across descents** (P3; if chosen). Large —
   architecture, persistence, cross-season draw.

## 7. Consults to fire

- **elrond** — P1 fork: does the catalogue/lineage clustering cover **monsters**
  (the floor-roster population)? Is *that* the judge Matt's reframe should tune? What
  is the coherent-faction ceiling there?
- **star-lord** — (a) P2: instrument a k-sweep over the Phase-5 clustering, report
  `cluster_compactness` + `diversity_flag` vs. k (find the knee). (b) Is the parked
  `build_unified_season_content_blocks` flat, or does it carry any structure depth can
  build onto?
- **rocket** — build-shape of (a) the floor/depth positional model and (b)
  depth-tiering as a generator input; and whether faction-leader designation is a
  generation-time or post-cluster step.

## 8. How this moves the gate ledger (recognition record §10)

- **G1** (content contract) — RESEQUENCED to *downstream of G2*; shrinks to the
  trivial binding layer once the depth-structured content exists.
- **G2** (per-floor anchor) — REFRAMED to faction-leader reuse (§4); de-scoped from
  "new anchor generation" to "k-sweep + leader designation + P1 fork resolution."
- **G3** (procedural middle) — unchanged; runs in parallel; recommend as next drax
  dispatch ahead of further crypt-vault dressing.
- **G5/G6** (mega-boss) — partially absorbed by the unification (§4): the mega-boss
  becomes a faction-leadership instance. The A/B/C/**D** source decision still stands
  (D = in-band kit + resourcing/AI/encounter menace + full kill-identity claim).

---

**Sign-off:** gandalf, 2026-06-22. The gap is a generation-model gap, not a
serialization gap. The single largest correction: the engine is "near complete" of a
**flat-season** model the descent does not consume. The single best simplification:
Matt's lieutenant = faction-leader reframe, which de-scopes per-floor theming to a
measurable k-sweep AND unifies the lieutenant + mega-boss under one new primitive.
Consults (§7) and the three precision-points (§4) are the next resolution targets.
