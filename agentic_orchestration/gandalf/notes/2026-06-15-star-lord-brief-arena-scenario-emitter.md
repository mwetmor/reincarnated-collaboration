# star-lord brief — arena-scenario geometry emitter (`arena_scenarios.json`)

**Type:** direct gandalf→star-lord brief (Matt is the conduit to star-lord's session; NOT a KR dispatch).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 — *"author the star-lord brief and hand it direct."* The two gating investigations Matt set are cleared (see § 8).
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-parametric-arenaroom-refactor.md` — the CONSUMER. drax's parametric ArenaRoom reads this JSON as data and builds all 6 rooms off it.
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` — the SOURCE OF TRUTH (`ALL_SCENARIOS`).

---

## 0. One line

Emit `arena.py :: ALL_SCENARIOS` to a versioned `arena_scenarios.json` so the Godot parametric ArenaRoom consumes the **same spec the `SpatialFightEngine` runs** — parity-by-construction. drax already hand-bootstrapped the file to unblock his build; this makes it **canonically regenerable** so it can never drift from `arena.py`, and the committed JSON doubles as a cross-seam parity audit trail.

## 1. Why (the seam this externalizes)

The engine is the architectural authority; Godot is a consumer. The scenario spec is **Layer 1 — encounter geometry**: arena footprint, choke zones, spawn positions, threat-tier/archetype SLOT LABELS, win conditions, durations. It is frozen and substrate-agnostic (arena.py's own comment: *"Substrate-AGNOSTIC: arena shape and AI are identical for all substrate manifestations"*). Content (the actual generated characters that fill the tier-slots) is **Layer 2** — placeholder now, generated later. The emitter externalizes **Layer 1 only**; content plugs into the tier-slots downstream. Genre precedent for the indirection: D3 rift / D4 dungeon assembly / PoE map layouts all separate encounter geometry from the monster roster via spawn-table indirection.

## 2. What to emit (mechanism — it's nearly free)

- `ALL_SCENARIOS` is a dict of 6 `ArenaScenario` dataclasses. Every nested type (`ChokeZone`, `Arena`, `SpawnSpec`, `ArenaScenario`) is a plain dataclass whose fields are JSON primitives (float / str / bool / None / nested dataclass). **Verified.**
- So the emit is: `dataclasses.asdict(scenario)` → `json.dump`. No custom serializer needed.
- **Provenance wrapper** (so the file self-documents its origin and can't be mistaken for hand-authored):
  ```json
  {
    "_generated_from": "reincarnated.simulation.spatial_gauntlet.arena.ALL_SCENARIOS",
    "_schema_version": 1,
    "_emitted_at": "<iso8601>",
    "_do_not_hand_edit": "regenerate via python -m reincarnated.export.arena_scenario_emitter",
    "scenarios": { "<scenario_id>": { ...asdict(scenario)... } }
  }
  ```
- **Deterministic formatting:** `json.dump(..., sort_keys=True, indent=2)`. This is load-bearing (see § 4).
- Preserve drax's `_schema_version: 1` contract — the emitter is the canonical PRODUCER of the file he hand-bootstrapped, not a new schema.

## 3. Output path + regen

- **Output:** `reincarnated-godot/data/arena_scenarios.json` (overwrite drax's bootstrap). This is a **deliberate cross-repo write** — the emitter lives in the engine repo and writes into the sibling Godot repo. Make the output dir a configurable arg defaulting to the Godot `data/` path; you own the exact path-resolution choice (direct-write vs emit-to-engine-then-sync — direct-write is simplest; your call).
- **Emitter home:** `src/reincarnated/export/arena_scenario_emitter.py` (export seam; consistent with `season_exporter`, `kit_space_emitter`).
- **Regen command:** `python -m reincarnated.export.arena_scenario_emitter` (or a CLI entry of your choosing). The Godot `data/arena_scenarios.json` is **never hand-edited** — it is a generated mirror.

## 4. The free bonus — a cross-seam parity audit trail

Because the output is deterministic and committed in the Godot repo, **a spawn move in `arena.py` becomes a one-line JSON diff in the Godot repo.** Encounter geometry can no longer silently drift between what the `SpatialFightEngine` simulates and what the player-facing room renders — git makes any divergence visible at review time. This is the same discipline as the committed-JSON-as-contract pattern; the emitter is what makes it real.

## 5. Scope — what this emits and what it deliberately does NOT

**Emits:** Layer-1 encounter geometry only (footprint, choke zones, spawn positions, tier/archetype slot labels, win conditions, durations).

**Does NOT emit (each a separate concern, confirmed by the export-seam survey):**
1. **Content** — no character/monster data. `archetype_tag` is a SLOT LABEL ("magic", "elite/brute"), not a roster. Content fills the slot later.
2. **AI behavior / damage / skill geometry** — these are ENGINE CODE, not separately emitted. The survey confirms the export seam emits *content* (seasons, kit-spaces, cycle artifacts), never encounter *behavior*. AI lives in `spatial_engine.py`, damage in `damage_resolver.py`. There is no separate AI/damage/skill emitter, and this brief does not create one.
3. **The perception-asymmetry near-miss mechanic** — that is engine BEHAVIOR (the AI-decision layer), not emitted geometry. Per Matt: *"regardless of if it's in the emitter, it should be pushed all the way back into the battle sim."* It lives in `spatial_engine.py` (gamora's companion brief), NOT in this JSON. Clean separation: **emitter = structure; engine = behavior.**

## 6. Roles / acceptance

- **star-lord:** author the emitter; regenerate `arena_scenarios.json`; **diff the regenerated file against drax's hand-bootstrap** (modulo provenance fields like `_emitted_at`).
  - If the diff is empty → drax serialized faithfully; the emitter just makes it regenerable. Ship it.
  - If the diff is non-empty → drax's hand-version drifted from `arena.py`. **That diff is the first value the emitter delivers** — surface it; the canonical (emitted) version wins.
- **jack-ryan Gate-1:** new export artifact + new output schema (light gate). The `_schema_version` field is the contract anchor; confirm the provenance wrapper + determinism.
- **Acceptance:** the regenerated JSON round-trips through drax's parametric-room loader with **no room-script change**; the diff vs the bootstrap is empty or explained.

## 7. Sequence

1. star-lord authors `arena_scenario_emitter.py`, regenerates, diffs against drax's bootstrap.
2. If diff non-empty: surface it (drax's hand-serialization drifted — exactly what the emitter prevents going forward).
3. jack-ryan Gate-1 (light).
4. Commit the regenerated `arena_scenarios.json` as the canonical mirror; drax's room consumes it unchanged. From here, arena.py is the single source and the Godot mirror is git-diff-auditable.

## 8. The two investigations Matt gated this brief on — both cleared

1. **"Does the asymmetric near-miss mechanic exist in the sim?"** — Surveyed. It does NOT live in the emitted geometry and should not (it's behavior). It belongs in `spatial_engine.py` and is the subject of the companion gamora brief. This brief is orthogonal to it.
2. **"Is there a separate emitter for encounter AI / damage / skill data?"** — No. The export seam emits content (seasons, kit-spaces, cycle artifacts). AI/damage/skill geometry are engine code, not emitted. This arena-geometry emitter is the FIRST emitter to externalize encounter *structure* — and it stays scoped to structure.

---

**Signed:** gandalf, 2026-06-15
**For:** teeing up the arena-scenario geometry emitter — `dataclasses.asdict(ALL_SCENARIOS)` + provenance wrapper + deterministic formatting → `reincarnated-godot/data/arena_scenarios.json`, making drax's hand-bootstrap canonically regenerable, parity-by-construction with the `SpatialFightEngine`, and a git-diff-auditable cross-seam contract; scoped to Layer-1 geometry only (no content, no AI/damage/skill, no perception-asymmetry — that's engine behavior, gamora's brief).
