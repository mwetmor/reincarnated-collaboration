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

---

## Completion record

**Completed:** 2026-05-17
**Author:** gamora
**Tag:** `gamora/v1.6-d10-substrate-coherent-gen-math-note-1` (local; push gated per ADR-006)
**Math note filed:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md`

### Acceptance criteria status

- [x] geometry_type derivation rules documented (§ 1 — 3-layer cascade, 24-type vocabulary, deterministic pure function, validation target ≥90% against season_001005)
- [x] Skill-count ceiling rules (§ 2 — per-archetype table; pruning algorithm)
- [x] Multi-element breadth gate (§ 3 — non-hybrid ≤2; hybrid ≤4; pruning rules)
- [x] buff_damage stacking limit (§ 4 — max 1 utility/mobility; keep longer-CD; defensive exempt)
- [x] DPS density gate (§ 5 — 5-fight pre-eval approach; threshold=0.90; formula non-discriminating finding documented)
- [x] floor_over_band flag spec (§ 6 — trigger condition, estimated_gap field, star-lord follow-on noted)
- [x] gear_pool population investigation (§ 7 — root cause: missing season_writer write step; fix is one-line; NOT separate dispatch)
- [x] Post-process plan for 002011–002015 salvage (§ 8 — 0 LLM cost; ~30–40 min; 5 steps detailed)
- [x] Math note doc filed (above path)
- [x] Hive-log STATE + HANDOFF → rocket (phase-1-p1-log.md appended)
- [x] Tag `gamora/v1.6-d10-substrate-coherent-gen-math-note-1` (local)

### Additional findings surfaced (not in dispatch scope, included in math note for completeness)

- geometry_type root cause clarified: lives in telemetry DB abilities table; generation seam does not emit it; export SQL query returns null with no DB → fix requires generation-seam emission (rocket D10 scope)
- gear_pool root cause clarified: orchestrator generates gear correctly in-memory; season_writer writes catalog.json but not gear_pool.json; export reads DB only; bridge is missing (one-line fix)
- DPS density formula proved non-discriminating cross-archetype: physical_warrior DPS density higher than hybrid_mage due to high base damage magnitudes, yet physical_warrior converges via structural engagement constraint. Quick-eval (5 fights at modifier=1.0) is more reliable discriminator.
- floor_over_band flag is gamora-seam work (balance_loop.py); gamora implements in D10 code phase (not rocket scope)

### Next

D10 code phase begins after:
1. Rocket implements derive_geometry_type() + kit constraints + gear_pool bridge
2. Jack-ryan reviews this math note
3. Post-process salvage script runs (gamora or rocket; knight-rider coordinates)

— gamora

---

## Jack-ryan Gate-1 review record

**Reviewer:** jack-ryan
**Tag reviewed:** `gamora/v1.6-d10-substrate-coherent-gen-math-note-1 @ 92a4691`
**Jack-ryan tag:** `jack-ryan/v1.4-d10-math-note-gate1-review-1` (engine repo, local)
**Date:** 2026-05-17
**Verdict:** CONDITIONAL ENDORSE — 3 pre-flags for rocket, 1 seam-owner action, 1 terminology advisory

### Findings

**[ENDORSE with conditions] Overall assessment**

The math note is well-structured and discipline-compliant. Discipline #1 (math-before-code) is clearly satisfied: empirical basis precedes every constraint, formula, and threshold. Discipline #12 (semantic shift) is explicitly declared at §§ 3.4 and 6.5. Discipline #11 (empirical inspection) is evident throughout — ground-truth vocabulary validated against season_001005 before any derivation rule was written. The three-layer cascade in § 1.3 is coherent, exhaustive-by-construction with a named fallback, and maps cleanly to the 002011–002015 field inventory. The DPS density finding (§ 5.3) is correctly self-correcting — gamora identifies the formula's failure mode and replaces it with a more reliable discriminator before handing off.

**[PRE-FLAG 1 — rocket — WARN] `range_profile` is on the class object, not the skill object**

§ 1.3 Layer 3 and § 1.4 specify `derive_geometry_type(role, canonical_element, effects_list, cooldown_seconds, range_profile)` with `range_profile` as a per-skill input. Empirical inspection of the 002011 data confirms `range_profile` lives on the class JSON object, not on individual skill objects. Rocket must pass `class.range_profile` as a per-class constant into `derive_geometry_type()` for all skills in that class. If rocket implements the function signature assuming per-skill `range_profile`, the post-process salvage script will fail at call-site. Cite: Discipline #11 (empirical inspection over assumption).

**[PRE-FLAG 2 — rocket — WARN] § 8.7 gear_pool backfill references `seed` but manifest field is `generation_seed`**

§ 8.7 states `rng = np.random.default_rng(seed + 999)` and says seed is "canonical seed offset per orchestrator line 464." Confirmed: line 464 of season_orchestrator.py uses `seed + 999`. However, empirical inspection of the 002011–002015 manifests shows the field name is `generation_seed`, not `seed`. Rocket's post-process salvage script must read `manifest["generation_seed"]` (e.g., `2011` for season_002011), not `manifest.get("seed")` (which returns None). A silent None → `default_rng(None)` would produce a non-deterministic gear backfill that cannot be reproduced. Cite: Discipline #11; Discipline #1 (reproducibility guarantee in § 8.1 depends on this).

**[PRE-FLAG 3 — rocket — INFO] R11(b) round-trip scope for `gear_pool_staged.json` and `estimated_gap`**

Two cross-seam contract additions are in scope for rocket's D10 implementation:
1. `gear_pool_staged.json` is a new output path in season_writer.py (export boundary); the exporter's fallback reads it. This is a cross-seam contract change per R11(b) trigger table ("export packet structure changed"). Rocket's acceptance criteria must include either a round-trip smoke spec or a `Round-trip: not applicable because <reason>` clause.
2. `estimated_gap` on `ClassBalanceResult` is gamora-seam (§ 6.4 correctly assigns it to gamora, not rocket). However, the star-lord follow-on ALTER TABLE is also a cross-seam contract change. The note correctly flags this as low-priority follow-on — no action needed in this dispatch, but the star-lord dispatch must include R11(b) round-trip spec when it fires.
Cite: Review Principle 6; R11(b).

**[SEAM-OWNER ACTION — gamora — INFO] `floor_over_band` is gamora-seam; MIGRATION.md entry required before tagging D10 code**

§ 6.5 correctly notes this is an additive semantic extension to `modifier_flag_tier`. The simulation seam's MIGRATION.md (at `src/reincarnated/simulation/MIGRATION.md`) already has a v1.6 entry for the `"review"` tier. When gamora implements `"floor_over_band"` + `estimated_gap` in the D10 code phase, a new MIGRATION.md entry (v1.7 or v1.8 as appropriate) is required at that boundary — both for the `modifier_flag_tier` new value and for the new `estimated_gap` field on `ClassBalanceResult`. This is not blocking the math note handoff but must be in place before the D10 code tag. Cite: ADR-004; Review Principle 3.

**[ADVISORY — INFO] § 5.3 DPS density finding: attribution framing is correct**

Gamora correctly frames the physical_warrior / hybrid_mage density paradox as a structural engagement constraint (close-range kiting penalty), not a formula flaw. This framing is compliant with Discipline #13b — it names a structural presupposition (physical_warrior's engagement-range constraint exists in the simulation) without claiming per-variable causal attribution to convergence outcome. No action needed; noting for the record.

**[WATCHPOINT 1 — § 1.5 validation methodology — INFO]**

The ≥90% match target against 60 season_001005 skills is an appropriate gate for a deterministic derivation algorithm. One structural gap: the ground-truth set is 60 skills from a single season (one seed, one generation run). If any geometry_type in season_001005 was manually corrected or LLM-influenced post-generation, it may not be a clean ground truth for a rule-derived comparison. Rocket should note any systematic miss patterns before adjusting the algorithm — do not chase individual mismatches without checking for pattern first (Discipline #1: re-diagnose mechanism before adjusting magnitude). The 90% gate is the right number; the methodology caveat is informational only.

### Summary for rocket dispatch

Pre-flags to address at implementation time:
1. `range_profile` is per-class, not per-skill — pass `class.range_profile` as constant into `derive_geometry_type()` for all skills in that class.
2. Gear backfill seed: read `manifest["generation_seed"]`, not `manifest["seed"]` (field name confirmed from 002011–002015 manifest inspection).
3. R11(b) round-trip clause required in rocket's acceptance criteria for `gear_pool_staged.json` export boundary.

No BLOCK conditions. Math note is ready for rocket execution.

— jack-ryan
