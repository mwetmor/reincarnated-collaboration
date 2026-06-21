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

---

## Completion record — 2026-06-21 — rocket

**Status:** BUILT + round-trip-smoked + MIGRATION'd + tagged. Auto-committed (team addendum; authorized cycle work). NOT pushed (ADR-006, Matt-gated). Reported to KR for Gate-2 via jack-ryan before gamora fires.

**Tag:** `rocket/v-typed-resistance-gear-and-monster-skills-1` (engine commit `75d7dd4`).

**Math-note (Discipline #1, BEFORE code):** `reincarnated-engine/src/reincarnated/generation/math/typed-resistance-gear-and-monster-skills-math-2026-06-21.md`.

### What shipped (files)
- `generation/gear_catalog.py` — per-element `element_resist` pool entries (one per rotating element; raw mitigation fraction [0.05,0.25]) + `_add(raw_magnitude=…)` flag.
- `generation/gear_generation.py` — `_derive_stats` `element_resist` mint branch; `_dominant_element` resist-exclusion; `_EFFECT_POWER_WEIGHT["element_resist"]=0.50` scaffold.
- `generation/gear_schema.py` — `combined_stats` 0.80 single-element ceiling clamp (enforces existing cap; does not change it).
- `foundation/effect_categorization.py` — `DEFENSIVE_EFFECTS += element_resist`.
- `generation/typed_monster_skills.py` — NEW. Typed resolver-attacker skill-dict emitter (heavy-slow boss / medium elite / light-variance swarm; geometry HARD-constrained to {point,circle,line,cone}).
- `generation/MIGRATION.md` — gen→sim entry (BOTH surfaces).
- `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py` — round-trip smoke (15/15 PASS).
- `generation/AGENT_STATE.md` — session record.

### Gear element-selection DELTA SIZE (confirm-trace, Discipline #11)
TWO paths, opposite sizes. **Path A** (`gear_generation`/`GearStats`, the LOAD-BEARING production-sim path): element selection ALREADY EXISTS via `RolledEffect.element` (from `EffectPoolEntry.element`) → delta is the **SMALL mint** (new effect type + one derive branch); NO schema/element-field add. This satisfies the §4 DoD. **Path B** (partition/keystone diagnostic + `compute_balance_gear_stats` stopgap): jack-ryan's MEDIUM-add (no element field on `PartitionModifier`/`RolledPartitionModifier`, even-spreads `resist_total/4.0`) — CONFIRMED at source, but Path B is "NOT wired into the sim." DEFERRED, off critical path. Net delta built: Path A small mint; downstream bound INTACT (schema/aggregation/sim unchanged).

### Anti-tax (G-A) — satisfied, and how shaped
Single-element-keyed mint + 0.80 ceiling clamp + bounded resist budget. Arithmetic: matching the boss's element is ~4.4× the defensive return of spreading thin (matched take = 0.255× spread take in smoke); "cap everything" is unreachable within budget (`N·r ≈ 1.5 ≪ K·C = 7×0.80 = 5.6`). **gamora joint constraint:** keep production `N·r_hi < ~2.0` (caps ~one element, never multiple). First-class gate, proven in smoke + at the production-roller level (random-kit max single-element 0.30 median vs mean 0.20; deliberate matching concentrates toward cap).

### Round-trip smoke (BOTH surfaces) — 15/15 PASS
(1) fire-weighted kit → `combined_stats().elemental_resistances["fire"] > water > earth` through the production aggregation + 0.80 clamp; (2) signature-element boss skill stepped through the production resolver shim applies TYPED damage mediated by per-element resist — ratio **0.315789** matches the 0a-spike analytic `(1−0.70)/(1−0.05)` to float precision; swarm mixed-element < boss multiplier (trash<boss); unwired-geometry guard raises. Production `generate_gear_item` end-to-end mints differentiated resist (599/600 legendary chests). 718 tests pass on touched modules; 7 pre-existing element-count-drift fails confirmed RED on pristine via stash round-trip (not mine).

### MIGRATION.md status
WRITTEN (gen→sim, BOTH contract surfaces; downstream consumers + reader-change analysis; G-A joint gate; Discipline #12 semantic-shift declared).

### What gamora needs to know (handoff)
1. Plug the emitted `skills` list (`emit_skills_for_threat_tier(tier, sig)` / `emit_boss_signature_skills` / `emit_swarm_minor_mixed_skills`) into the synthetic-mob dict at `t4_sim_cycling.py:1082` (the `"skills": []` site).
2. Route the death channel through `resolve_skill` (player-as-defender / mob-as-attacker) and populate `resolver_skills` (today hardcoded `[]` at `spatial_engine.py:2508`) from the projected typed skills — both call-site/wiring per the 0a spike; resolver byte-untouched.
3. Own ALL magnitude CONSTANTS (`damage_multiplier`/`cooldown_seconds`/per-hit-variance distribution) — re-derive from scratch under the resolver; **flat anchor INVALID**. rocket emitted SCAFFOLD shapes inside the per-archetype envelope (math note §2); tune constants within the SHAPE, do not change the heavy-slow/light-variance SHAPE.
4. Keep production resist constants inside the anti-tax `N·r_hi < ~2.0` envelope — the joint G-A gate.
5. The gear `combined_stats().elemental_resistances` dict now carries differentiated values for the player defender; the synthetic-cohort dicts (`_build_cohort_combatant_stats`) still carry no `resistances` key — populate with typed cohort profiles if you want typed DEFENDERS in the sweep (separate path; not changed here).
