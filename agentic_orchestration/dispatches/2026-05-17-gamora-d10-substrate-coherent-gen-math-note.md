# 2026-05-17 — gamora — D10 substrate-coherent gen-math note (math + rules authoring)

**Authority:** Matt L3 2026-05-17 (~23:00 EDT). All 4 D10 input recommendations from your convergence sample analysis (v1.5 @ `088c0ec`) ready. Demo broken by pre-D10 shim data gaps (geometry_type=null on all skills + empty gear_pool); D10 is the structural fix.
**Type:** Pattern B — math note authoring + rule specification; ~0.5 day. NO code in this dispatch (code phase queues to rocket).
**Predecessors:**
- gamora v1.5 convergence sample analysis (`gamora/v1.5-convergence-sample-analysis-1` @ `088c0ec`) — your own 4 D10 input recommendations
- gandalf canonical-four trait pool L3 briefing (Phase-1 P1 D10 design framing)
- jack-ryan D10 end-to-end smoke recommendation (task #44)

---

## Why this matters

Tonight's regen demonstrated **systematic over-generation bias** in pre-D10 shim:
- 69% over-band non-convergence (no under-band cases observed)
- ALL 114 skills generated with `geometry_type: null`
- `gear_pool.json` empty
- hybrid_mage archetype = 0-33% convergence rate (worst archetype)
- physical/rage archetypes = 100% convergence (cleanest case)

D10 is the substrate-coherent gen-math layer that closes these gaps. Your math note is the canonical design specification that rocket then implements in generation/.

---

## Required reading

1. `reincarnated-engine/output/standard-demo-regen-2026-05-17/convergence-sample-analysis-2026-05-17.md` — your own v1.5 analysis (D10 input recommendations)
2. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/classes.json` — empirical reference (114 skills × geometry_type=null pattern)
3. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 11 — gandalf's substrate-windup canon (binds geometry_type → substrate)
4. `canonical/story/substrate-identity-declarations-2026-05-17.md` — canonical-7 substrate cosmology
5. `reincarnated-engine/src/reincarnated/generation/` — rocket's generation seam (your output spec target)
6. Prior D-series math notes (D3 / D7) for format pattern

---

## Scope

### Item 1 — geometry_type derivation rules (per skill)

Define how to populate `geometry_type` for each skill from existing structural fields:
- **Input:** role / canonical_element / damage_multiplier / energy_cost / cooldown_seconds / range_profile
- **Output:** geometry_type ∈ {melee_arc, melee_strike, cone, line, aura, ranged_physical, totem, projectile, circle, ground_slam, self_buff, self_cast, ...} (full list per old season_001005 vocabulary)

The rules should be deterministic — given the same input fields, produce the same geometry_type. This is critical for post-process backfilling of the 002011-015 staged seasons without re-running LLM naming.

For each (role × element × range_profile) tuple, document the canonical geometry_type. Capture edge cases:
- physical + melee_range → melee_arc / melee_strike / ground_slam (which?)
- mage + medium range → projectile / circle / line (which?)
- controller + various → totem / aura / cone
- defensive role → self_buff / self_cast / shield_aura

Reference the old season_001005 (60 skills with populated geometry_type) as ground truth for canonical patterns.

### Item 2 — Skill-count ceiling for mana archetypes (per your D10 input #1)

Hard max **10-11 skills** for non-hybrid mana archetypes. hybrid_mage allowed UP TO 12 but no more.

Document:
- Per-archetype max-skill table
- Pruning rules when generation overflows (lowest-cooldown? highest-overlap? lowest-damage?)
- Conflict-resolution when a kit has 14 skills and 12 are needed (choose 4 to drop)

### Item 3 — Multi-element breadth gate (per your D10 input #2)

Max **2 canonical elements** in non-hybrid mana kits. hybrid_mage allowed UP TO 4 (since hybrid is the hybrid-by-definition archetype).

Document:
- Per-archetype element-breadth ceiling
- Pruning rule when violated (drop lowest-DPS-contribution element? Drop seasonal-element-only skills first?)

### Item 4 — buff_damage stacking limit (per your D10 input #3)

Max **1 buff_damage effect** per kit. Multiple buff_damage = automatic over-generation.

Document:
- Detection rule for buff_damage stacking
- Pruning rule (drop highest-magnitude? Drop longest-duration? Drop most-recent?)

### Item 5 — Pre-balance-loop DPS density gate (per your D10 input #4)

Define the DPS density check that fires **before** the binary-search modifier loop wastes 10 iterations. Catches over-generation early.

- Formula: DPS density = Σ(skill_damage × skill_cd_factor) / kit_skill_count
- Threshold: if DPS density > N, flag kit as `over_generated`; either prune or set early modifier_flag_tier
- Document N (empirical; reference your v1.5 sample data; hybrid_mage outliers had DPS density ~X)

### Item 6 — `modifier_flag_tier="floor_over_band"` (per your D10 input #4)

Specify the new flag in balance_loop output:
- Trigger: `converged=False AND damage_modifier == 0.05` (floor hit)
- Symmetric to existing high-end flag pattern
- Surface in star-lord telemetry per Discipline #11 attribution (will need follow-on star-lord dispatch)

### Item 7 — gear_pool population (auxiliary)

Investigate why `gear_pool.json` is empty in the staged seasons. Document:
- Where gear_pool generation lives in the pipeline (rocket's seam)
- What the legendary-floor-per-class rule was supposed to enforce
- Recommended fix (call-site? data pipeline? LLM step missing?)

If the gear_pool fix is more substantial than expected, surface as separate rocket dispatch recommendation in your math note.

### Item 8 — Post-process plan for 002011-015 salvage

Document how D10 rules can be applied as POST-PROCESS to the 5 staged seasons (no LLM re-cost):
1. Per skill: derive geometry_type from rules in Item 1
2. Per kit: prune overflow per Items 2/3/4
3. Per class: re-run balance_loop (sim only, no LLM)
4. Per season: rebuild classes.json + manifest.json
5. Backfill gear_pool per Item 7

Estimated total cost: 0 LLM dollars (sim + math only).

### Item 9 — Output

File at `reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md` (or wherever your prior D-series math notes live).

Cross-references:
- Your v1.5 convergence sample analysis
- gandalf substrate-identity-declarations
- gandalf canonical-four trait pool briefing
- jack-ryan task #44 (D10 smoke recommendation)

### Item 10 — Hive log + tag + HANDOFF

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry: math note shipped; specifies post-process feasibility; documents geometry_type derivation rules
- HANDOFF → rocket: implementation queued (knight-rider will fire when math note lands)
- Tag `gamora/v1.6-d10-substrate-coherent-gen-math-note-1` (local; push gated per ADR-006)

---

## Out of scope (DO NOT)

- ❌ DO NOT write code (math note + rules only; rocket implements)
- ❌ DO NOT modify generation/ in engine (rocket's seam)
- ❌ DO NOT modify the staged 002011-015 data yet (post-process happens after rocket implementation)
- ❌ DO NOT re-run regen (post-process is the path; LLM cost-savings discipline)
- ❌ DO NOT extend to D11/D12 work; this is D10 only
- ❌ DO NOT touch demo/loadout

---

## Acceptance criteria

- [ ] geometry_type derivation rules documented (Item 1)
- [ ] Skill-count ceiling rules (Item 2)
- [ ] Multi-element breadth gate (Item 3)
- [ ] buff_damage stacking limit (Item 4)
- [ ] DPS density gate (Item 5)
- [ ] floor_over_band flag spec (Item 6)
- [ ] gear_pool population investigation (Item 7)
- [ ] Post-process plan for 002011-015 salvage (Item 8)
- [ ] Math note doc filed
- [ ] Hive-log STATE + HANDOFF → rocket
- [ ] Tag `gamora/v1.6-d10-substrate-coherent-gen-math-note-1` (local)

---

## Coordination

- **Drax v1.10 revert is firing in parallel** (different seam: demo-side hotfix while you author the structural fix)
- **Rocket queued for implementation** — knight-rider auto-fires rocket dispatch when your math note ships
- **PRE-SIGNAL § 14.1.1** before hive-log appends (multiple agents writing concurrently)
- **Bandwidth-friendly:** math-note authoring; no LLM cost; no fight-engine; ~0.5 day

---

*Dispatched 2026-05-17 by knight-rider per Matt L3. ~0.5 day. Append completion record when done.*
