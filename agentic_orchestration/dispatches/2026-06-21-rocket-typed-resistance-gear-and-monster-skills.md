# Dispatch — 2026-06-21 — rocket — typed-resistance gear-minting + typed monster skills

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-21 — publish-go on the typed-resistance recal wave.
**Estimated effort:** ~2 waves. **This dispatch HARD-BLOCKS gamora** — gamora cannot start calibration until (a) the mob emits typed resolver-attacker skills and (b) gear mints DIFFERENTIATED per-element resist. Both reasons below.
**Acceptance:** gear mints differentiated per-element resist verifiable end-to-end; typed signature-element monster skills fire through the resolver and the player's per-element resist mediates the damage; the anti-tax generation constraint holds.

> **Parent MASTER (Gate-1 ENDORSE):** `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`. This pickup is the rocket section extracted verbatim. Gate-1 finding: `qa/findings/2026-06-21-recal-wave-typed-resistance-MASTER-gate1.md`.

## Context

Matt LOCKED typed resistances as the headline of the defensive-axis recal wave. The death channel reroutes through the kernel resolver with the player as a real DEFENDER, so the kit's per-element resist goes live. But the payoff is INERT until two generation gaps close — both yours:
1. **Mobs are not attackers.** The endgame boss/elite/synthetic mobs carry `"skills": []` / `elemental_resistances={}` and `resolver_skills=[]` — they emit no typed offense for the resolver to process.
2. **Kits are undifferentiated on resist.** The main gear roll path emits EMPTY resist; the paths that populate spread evenly across all four elements. Typed offense into an even-spread surface buys nothing a single armor number wouldn't — the resolver runs the same `res` for every element. Typed resistance is worth the complexity ONLY if kits can build toward SPECIFIC elements.

The 0a resolver spike already proved the sim CONSUMES per-element differentiation (fire-res 0.70 vs 0.05 → analytic damage ratio 0.31579). You close the GENERATION half of that path.

## Required reading before starting
1. `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` — design of record. **§3** (signature-element + reward-for-matching), **§4** (gear prerequisite DoD — your build target), **§7** (swarm shallow-typing), **§8** (rocket handoff).
2. `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md` — jack-ryan Gate-1; **concern 0b-c3 sizes your gear work as the MEDIUM add** (see below).
3. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` — the 0a spike (proves the sim consumes your differentiated output).
4. `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md` — **threat SHAPE** (heavy-slow boss / light-variance swarm) — UNCHANGED; typing is layered ON this shape.

## NON-NEGOTIABLE GUARDS (carry verbatim)
- **G-A — ANTI-TAX (JOINT gate with gamora):** resistance is REWARD-for-matching, NEVER a mandatory cap. Your generation constraint: do NOT make broad all-element resist trivially stackable to where "cap everything" dominates "match the fight." Specializing into the boss's element must be a BETTER defensive return than spreading thin. **This is the single point where the anti-tax headline can quietly fail — it is a first-class acceptance gate, not a footnote.** Converge with gamora+gandalf on the exact shape.
- **G-B — Trash < boss:** swarm/clear-shell mobs carry minor/mixed elemental damage (broad resist mildly helps) — NOT a per-element resist-check (that re-imports the D4 every-white-mob tax and risks inverting trash<boss).
- **G-D — Flat anchor INVALID:** out of your lane (gamora's), but for context: do NOT reason about gear magnitudes from the old `0.40/0.95` flat constants — they are inert under the resolver.

## Scope

**(a) Gear per-element-resist MINTING (the prerequisite — §4):**
- [ ] A piece of gear can roll resist toward a **specific element** (e.g. `{"fire": 0.30}`), NOT an even spread across all four. The `element_resistance` modifier category (`generation/.../gear_instance_generator.py:66`, range −1.0..0.80) is the magnitude source; mint it onto per-instance `GearStats.elemental_resistances` with the **element key preserved**.
- [ ] **SIZING (jack-ryan 0b-c3 — this is the MEDIUM add, NOT the small fix):** source-confirmed neither `PartitionModifier` nor `RolledPartitionModifier` carries an element field (`generation/.../partition_schema.py:505-546`); projection matches by modifier-id only. So element SELECTION must be **ADDED** to the roll — not merely preserved through the per-instance build. Size against that. **The downstream bound is INTACT** — schema/aggregation/sim are unchanged (non-lossy per `gear_schema.py:252-253` → `combatant.py:575/926`); the blast radius is the roll only. Confirm-trace this first and document the delta.
- [ ] **Differentiation verifiable end-to-end:** a kit built with a fire-weighted loadout shows higher `combatant.elemental_resistances["fire"]` than its other elements.
- [ ] **ANTI-TAX generation constraint (G-A):** per the guard above — a first-class acceptance gate.

**(b) Typed resolver-attacker monster skills (§8 + threat-spec §2):**
- [ ] Give the endgame boss/elite/synthetic mobs (replacing `"skills": []` / `elemental_resistances={}` at `simulation/.../t4_sim_cycling.py:1082`/`:1016`) **typed resolver-attacker skills**: `element` + magnitude + `scaling_stat` + `substrate` (so `resolve_skill` processes them), each trial-boss carrying its **SIGNATURE element**, on the **heavy-slow** boss shape (few big readable hits — threat-spec §2).
- [ ] **Geometry HARD constraint:** emit ONLY wired hit-geometries `{point, circle, line, cone}`. `burst/ring/nova/wave/chain/arc` → no-hit (`simulation/spatial_gauntlet/spatial_engine.py:740-741`). An unwired geometry mints a damage-less (silent-defect) threat.
- [ ] **Swarm minor/mixed (§7):** swarm/clear-shell mobs carry minor/mixed elemental damage (broad resist mildly helps) — NOT a per-element resist-check (keeps trash<boss). Plus the per-hit variance field (threat-spec §3a swarm death lever — unchanged).
- [ ] **(optional richness, 0a-c1 — NOT a blocker):** registering a KNOWN mob substrate adds canonical/luminance valence on top of the per-element resist; per-element differentiation flows WITHOUT it. Add only if cheap; the route does not require it.
- [ ] Math-before-code: math-note the emitted per-archetype magnitude SHAPE envelope (heavy-slow boss signature-element ranges; light-variance swarm) BEFORE wiring; gamora tunes exact constants within it.
- [ ] MIGRATION.md (gen→sim) — see cross-seam below.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `rocket/v-typed-resistance-gear-and-monster-skills-N`

## Cross-seam contract change? (Principle 6 — YES, round-trip REQUIRED)
TWO contract surfaces change: (1) per-instance `GearStats.elemental_resistances` now element-keyed differentiated; (2) the synthetic-mob dict now carries `resolver_skills` with `element`. **MIGRATION.md required (gen→sim).**
Round-trip smoke (BOTH):
- (1) build a fire-weighted kit → assert `combatant.elemental_resistances["fire"]` > its other elements through the production aggregation.
- (2) build a signature-element boss → step it through `spatial_engine` one tick → assert the resolver-attacker cast fires and applies TYPED damage that the player's per-element resist mediates.

## Out of scope (explicit non-goals)
- Setting production constants (gamora's lane).
- Changing the 80% resist ceiling / the resolver mitigation curve / the substrate matrix (§4 out-of-scope).
- The band finalization / content emission (Matt-gated joint close).
- Re-opening any ruled design question (typed direction, signature-element + reward-for-matching, the gear DoD, swarm shallow-typing) — all RULED.

## Open questions for you to resolve (and document)
- The gear-resist roll element-selection mechanism (the MEDIUM add) — confirm-trace and document the delta.
- Which mob roles carry the signature-element heavy-slow boss skill vs the swarm minor/mixed.
- (JOINT with gamora+gandalf) the exact gear-resist generation SHAPE that makes element-matching a better return than all-resist stacking — the anti-tax gate's load-bearing convergence.

## References
- Typed-resistance design-half: `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md`
- Typed-resistance Gate-1: `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md`
- 0a resolver spike: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md`
- Gen — resist surface: empty main path `gear_generation.py:943-972`; even-spread `keystone_loadout_materializer.py:275-279`/`gear_catalog.py:188-190`; non-lossy aggregation `gear_schema.py:252-253`; modifier category+range `gear_instance_generator.py:66/487`; NO element field on modifiers `partition_schema.py:505-546`; combatant resist source `combatant.py:566/575/926`
- Gen — endgame boss empty + skill-less: `t4_sim_cycling.py:1016/1082`
- Engine — resolver typed paths: `damage_resolver.py:456/460/478/485/502`; geometry dispatch `spatial_engine.py:716-741`
- Disciplines: #1 math-before-code, #11 empirical inspection, #12 semantic-shift
