# Tier-3 W2 → Lane-2: Harness-Extension Requirements (T3-V7 routing artifact)

**From:** gandalf `RUN-CONDUCTOR` (Tier-3 encounter-geometry run, ruling L-12)
**To:** KR sim-capacity lane (Lane-2) — requirements-INPUTS to `simulation/spec/sim-capacity-extension-spec-2026-07-22.md` per charter T3-V7 (one-way coupling: Tier-3 → lanes; scope placement is the lane's own gate process)
**Evidence:** gamora W2 report `agentic_orchestration/gamora/notes/2026-07-22-tier3-w2-fit-layer-report.md` §1 (probe verdicts line-cited at engine HEAD `a57ee1f`, re-verified stable at `99aaf50`)
**Blocking status:** Tier-3 does NOT block on any of these — W3/RD-1 proceed on expressible scope; RD-1's gamora smoke will class-proxy the affected behaviors until the mechanisms exist.

---

## Context

The sim-capacity spec §A3 verified the four COMMON formation classes (swarm / volley-fan / lane / emplacement) as fully expressible — that claim holds. The Tier-3 W1 grammar spec §7 flagged four deliberately-harder STRAIN formations; W2 probed them against the live harness and they land **PARTIAL ×3 + CANNOT ×1**. These are the requirements that close the gap, priority-ordered.

## R-1 — Mid-fight entity-mutation-on-trigger (`ss_phase_transform`) — **NET-NEW MECHANISM, highest priority**

- **Finding (CANNOT):** `preferred_behavior` is read once at spawn (`spatial_engine.py:5335/5410`) and is immutable per entity for the fight. No HP-threshold / phase / aggro trigger can swap an entity's behavior or skill-set mid-fight. `proximity_trigger` is spawn-fixed, not a transform.
- **Requirement:** a trigger hook (HP-threshold at minimum; phase/aggro desirable) that mutates a live entity's behavior + skill rotation mid-fight.
- **What it unlocks:** the entire SHAPESHIFT verb class — **2 of the 5 Tier-3 RDR-NATIVE-DERIVED templates** (SHAPESHIFT-I and SHAPESHIFT-III are form-transition monsters: handler-form → beast-brawl form on trigger, swapping their MICRO verb) plus the `ss_phase_transform` formation. Genre-core: boss phase-transitions are ARPG-universal (D2 Diablo, PoE2 Geonor form-swap — the Age-IV *attested* monster-side SHAPESHIFT this mechanism would let the sim express).

## R-2 — Killable-spawner-entity (`ts_environmental_nest`) — primitive-extension

- **Finding (PARTIAL):** the spawner is a fixed-window GLOBAL injector (`ContinuousSpawnSpec`, `arena.py:230` — clones the last mob, injects in a band, engaged_cap=50). No source-entity whose death halts spawning.
- **Requirement:** a terrain-anchored spawner ENTITY with HP; killing it stops its injection stream.
- **What it unlocks:** destroy-the-source gameplay — a 25-year genre staple (D2 Mummy sarcophagi, GD Chthonian nests, PoE essence monoliths). Converts the existing injector primitive into a player-facing verb.

## R-3 — Projectile wall-reflection (`cbn_corridor_arc`) — primitive-extension

- **Finding (PARTIAL):** corridor geometry exists (`SCENARIO_CHOKEPOINT`, 5m bottleneck) and beams/bolts are `line` geometry, but walls are positional bounds only (`spatial_engine.py:3036/3122`) — no projectile bounce/LOS/occlusion. Chains capped depth-0/1 (`:460`); "reflect" is thorns damage, not geometry.
- **Requirement:** geometric wall-reflection for projectile/chain entities within bounded arenas (corridor bounce amplification).
- **What it unlocks:** the CHAIN-BOUNCE strain formation (arc bouncing player→adds→walls) — the family's headline pressure in enclosed spaces. Also relaxes the chain-depth cap in bounded contexts.

## R-4 — Native paired-emitter cross-tracking (`cb_crossfire`) — primitive-extension, lowest urgency

- **Finding (PARTIAL):** single tracking-beam expressible (`spatial_engine.py:3116`); crossfire is composable TODAY as two independent `stationary_caster` channelers. Missing only a first-class construct modeling the beam-CROSS forced-reposition zone.
- **Requirement:** paired-emitter primitive with a modeled intersection zone.
- **What it unlocks:** fidelity upgrade over the existing composition — workaround exists, so sequence last.

---

**Coupling law reminder (T3-V7):** these are inputs, not commands. The lane's own gate process decides placement (follow-on slice vs. future wave — step (b) has landed and Gate-2 is firing, so the follow-on queue is the natural home). Tier-3 never blocks on the lane; the lane never writes into Tier-3 namespaces.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22 — ruling L-12.
