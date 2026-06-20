# Dispatch — 2026-06-20 — gamora — Phase 4: Armor/resist symmetry (instrument-validity workstream)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-20 (autonomous instrument-validity workstream authorization)
**Estimated effort:** quarter-to-half-day (mitigation-side correction)
**Acceptance:** casters mitigate the resist they currently bypass; measure-isolated harness shows caster KPM/boss-survive coming DOWN toward the martial range, against the CURRENT (untouched) bands; math-note-first; jack-ryan Gate-2 clean.

## Authoritative spec
This is **Phase 4** of the gandalf-authored instrument-validity workstream. Read it IN FULL first:
`agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§2 spine, §3 Phase-4 detail + GATE G5, §5 cautions).

## Context & PARALLELISM
This is the **mitigation-side** defect — confirmed via the Arm-C diagnostic STOP: armor/resist is asymmetric, casters ate ~zero resist, inflating caster bands and boss survive+kill (toward the implausible ~0.99). It is **selector-independent** and runs in **PARALLEL** with the offense-side chain (Phases 1–3). To avoid working-tree conflicts with the concurrently-running Phase 1, **this dispatch executes in an isolated git worktree of the engine repo** (KR provisions the worktree; you work on its branch). Your code edits land there; harness-result JSONs land in the collab repo as usual. KR merges your branch back to `main` before Phase 5.

## Math-before-code (Discipline #1 — REQUIRED FIRST)
Author `simulation/math/<...>-phase4-armor-resist-symmetry-2026-06-20.md` BEFORE the fix:
- Identify the exact asymmetry in code (where martial damage eats armor but caster damage bypasses resist, or whichever direction the asymmetry runs) — cite locations.
- Pre-compute the expected magnitude of the caster-side correction (how much resist they will now eat) and the expected direction of the band-delta.
- Cite code locations for every claim (Discipline #1.2).

## The work (recompose-first)
Correct the armor/resist asymmetry so casters mitigate the resist they currently bypass — symmetric with how martial damage is already mitigated by armor. **Recompose-first: activate/symmetrize the existing mitigation path; do not invent a new mitigation model.** Touch `damage_resolver.py` / `spatial_engine.py` mitigation as needed.

## Measure-ISOLATED (load-bearing, brief §5)
- **Do NOT touch** `ENCOUNTER_COHORT_KPM_BAND` or the production gate. Bands stay as-is so the mitigation-shift is visible against the CURRENT bands. Refit is Phase 5 only.
- Run on a **fresh disjoint seed base** (Discipline #3; avoid `[700000,766703]`, `[619000,684303]` AND whatever Phase 1 claims — coordinate seed base with KR so the four phases stay disjoint).
- **Semantic-shift declaration (Discipline #12):** mitigation changes the meaning of every caster KPM/DPS/boss-survive field. Declare the boundary.

## GATE G5 (AFTER measure) — report against this pre-registration
Expected: caster clear-room KPM should **DROP** (they now eat resist); caster boss survive+kill should fall from the inflated ~0.99 toward the martial range. **Report your result against this.** KR auto-resolves if caster numbers come down toward martial.
- **Flag to KR ONLY IF:** martial numbers MOVE (they already ate resist — they shouldn't shift → fix touched the wrong path), OR symmetry OVER-corrects (casters now BELOW martial → over-mitigation).

## Cross-seam contract change? (Principle 6 gate)
Mitigation is INTERNAL to the simulation seam. If any telemetry/fight_log field crossing gamora→star-lord changes, write `MIGRATION.md` per ADR-004. If not, note that explicitly.

## Out of scope (do NOT do)
- No band refit (Phase 5 only).
- No offense-side work (resource/rotation/DoT — separate dispatches).
- No over-reach beyond symmetrizing the armor/resist mitigation.

## Hand-back
Append a completion record: branch name + tag, math-note path, harness results path, G5 self-assessment vs the table, MIGRATION.md status, notes for jack-ryan Gate-2.

---

## Completion record (gamora, 2026-06-20)

**Status:** DONE. G5 AUTO-RESOLVE. No flags to KR.

**Worked on `main`** (per KR serialization — IGNORED the dispatch's git-worktree instruction as instructed by the KR prompt; Phases 1-3 already committed there, no concurrent gamora). **Tag:** `gamora/v-armor-resist-symmetry-phase4-1`. **Engine commit:** `d2d3dde`. **Collab commit (harness results):** `d8596a3`. NO push (Matt-gated).

**1. The exact asymmetry (math-note-first; code locations).** Math note: `reincarnated-engine/src/reincarnated/simulation/math/armor-resist-symmetry-phase4-2026-06-20.md`. There are TWO mob-construction paths feeding the resolver DEFENDER, and the prior F4 fix (`e537b29`) symmetrized only the first:
- **Path A (t4 synthetic, ALREADY symmetric):** `_synthetic_mob_dict_for_spatial` (`t4_sim_cycling.py:1001-1040`) emits `elemental_resistances={e: armor/(armor+3000) ...}` when `mitigation_symmetric=True`. The str_9pass + Phase-3 harnesses run THIS path.
- **Path B (PRODUCTION real-Monster, NOT symmetrized = the live defect):** `from_monster` (`combatant.py:1053`, my seam) propagated the generator's FLAT per-element rolls (`monster_generator._roll_resistances:486-498`: own-element `uniform(0.30,0.60)`, OFF-element `uniform(0.0,0.20)` ~0.10) DECOUPLED from armor. The resolver IS symmetric-capable (`damage_resolver.py:478/490` resist-by-attacker-element; `:460` armor) — the defect is the SOURCE VALUES. An off-element caster ate ~10% at every tier while martial ate the armor curve (66% elite / 90% mini-boss / 93% boss) → at boss martial kept ~7%, off-element caster ~90% → ~13× gap → the inflated caster boss survive+kill. Expected caster mitigation correction (math note §2.1): off-element raised from ~10% to the tier armor curve (magic 35.9% → boss 92.7%); near-zero at swarm (r_sym 8.1% < the ~10% roll). Expected band-delta: caster KPM DOWN monotone with tier, boss survive+kill DOWN toward martial; martial UNCHANGED. **Measured matches predicted.**

**2. What I symmetrized + recompose-first confirmation + flag name.** Symmetrized Path B at `from_monster` via new helper `_armor_symmetric_resistances` = `max(rolled, armor/(armor+ARMOR_MITIGATION_K))` per rotating element — raises off-element rolls to the armor floor (symmetry) while keeping the stronger rolled own-element. **Recompose-first HELD: no new mitigation model** — reuses the SAME `armor/(armor+K)` formula F4 already uses (Path A) + the same `ARMOR_MITIGATION_K` (imported from `math_model`, single source). **Flag: `MITIGATION_SYMMETRY: bool = True`** (`combatant.py`; mirrors the Phase-1 `WIRE_RESOURCE_ECONOMY` toggle; OFF = byte-identical pre-Phase-4 raw rolls).

**3. G5 self-assessment vs the table.** Full run (66 kits × 6 shells × 2 flags × 20 fights, base `24_000_000`, mob dominant=physical so casters attack OFF-element = the defect case). Harness self-assessment: `martial_str_kpm_unchanged=True`, `caster_kpm_drops_or_flat=True`, `no_obvious_overcorrection=True`, **AUTO-RESOLVE=True**.
- **Did caster KPM/boss-survive come down toward martial?** YES. Caster boss survive+kill fell toward the martial floor (str boss sk = 0.250/0.000): int boss_with_adds KPM 98.96→0.73 (−99.3%), mini_boss sk 1.000→0.000; wis boss_with_adds sk 1.000→0.945, mini_boss 1.000→0.000; dex boss_with_adds sk 0.838→0.421, mini_boss 0.833→0.000. Caster clear KPM drops monotone with tier (near-flat low-armor, larger at magic_pack, saturated at elite). DEX behaves like a caster at boss (83% elemental) — corroborates element-based mitigation.
- **Did martial numbers stay put?** YES. str KPM_d%=0.00 and survive+kill Δ=0.000 on EVERY shell. The fix touches only `elemental_resistances`; the physical/armor path is untouched. G5 falsifier NOT triggered.
- **Over-correction?** NONE. Casters converge TO the martial range, never below (guaranteed by `max()` construction — the floor can only raise caster mitigation to exactly the martial reduction).

**4. Tag + MIGRATION status.** Tag `gamora/v-armor-resist-symmetry-phase4-1`. **NO MIGRATION** — mitigation is INTERNAL to the simulation seam; the `elemental_resistances` VALUE on a defender CombatantState changes, but NO telemetry/fight_log/export SCHEMA field is added/renamed/removed (math note §7). Semantic-shift declaration (Discipline #12) is the obligation, not a schema migration.

**5. For jack-ryan Gate-2 + Phase 5.** Gate-2 focus: (a) the **two-path framing + Path-B harness validity** — the harness deliberately drives the real-Monster path (the only path the fix lives on; the str_9pass/Phase-3 harnesses run Path A which is already symmetric and cannot measure this fix); (b) `max(rolled, r_sym)` correctness + confirm no martial-path touch; (c) the **FOURTH (last) semantic-shift boundary** continuity across all four fixes; (d) no production-gate regression (bands UNTOUCHED, measure-isolated); (e) seed hygiene (fresh disjoint base `24_000_000`). **Phase 5 (composed refit) is now FULLY UNBLOCKED — all four instrument fixes (resource/rotation/DoT/mitigation) are live on the production path; the composed instrument Phase 5 refits the bands against now exists.**
