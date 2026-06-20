# Finding — 2026-06-20 — gamora Phase 4: armor/resist symmetry (mitigation-side, instrument-validity workstream)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no WARN, no BLOCK)
**Target:** `gamora/v-armor-resist-symmetry-phase4-1` — engine `d2d3dde`, collab `d8596a3`, dispatch record `61a7b6e`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3/6 (cross-seam — N/A justification verified), 4 (decisions-log alignment)
**Disciplines cited:** #1, #2, #3 (seed hygiene), #11 (empirical inspection), #12 (semantic-shift), #24 (lever isolation)

## What I found

Phase 4 — the fourth and final isolated instrument-validity fix (mitigation side) — is correct, recompose-first, measure-isolated, and the strongest-scrutiny item (the two-path framing + Path-B harness validity) holds up to first-hand verification. The defect is genuinely on Path B (`from_monster`, `combatant.py`): the production real-Monster defender propagated the generator's flat per-element resist rolls (off-element ~0.10) decoupled from armor, so off-element casters ate ~10% at every tier while martial ate the armor curve (66% elite / 90% mini-boss / 93% boss) — a ~13x boss-tier gap inflating caster boss survive+kill toward ~0.99. Path A (`_synthetic_mob_dict_for_spatial`) was already symmetric since F4 `e537b29`, which is precisely why str_9pass and the Phase-3 harness (both Path A) could not measure this. The resolver was already symmetric-capable (`damage_resolver.py:478/490` elemental-by-attacker-element; `:460` physical-by-armor), so the defect was the SOURCE VALUES, not resolver logic — confirmed by reading both sites. The fix is a single-site floor in `from_monster`: `_armor_symmetric_resistances` = `max(rolled, armor/(armor+ARMOR_MITIGATION_K))` per element, flag-gated by `MITIGATION_SYMMETRY=True`, returning a NEW dict (no mutation of the Monster's stored rolls).

## Rationale / first-hand evidence

**Path-A-vs-Path-B validity ruling: VALID.** I read the harness (`armor_resist_symmetry_phase4_harness_2026_06_20.py`): it builds real `Monster` objects (`_build_shell_monster`) and threads them as `mob_objects=` into `run_spatial_fight` (line 149, "Path B: real Monster -> from_monster (the fix site)"), toggling `CMB.MITIGATION_SYMMETRY` off/on at matched seeds and restoring the default after. This genuinely exercises the only path the fix lives on; Path A is correctly left untouched (no double-symmetrize). Two-path framing confirmed.

**Fix correctness (a/b/c): CONFIRMED.** (a) Reuses the SAME formula + K as Path A — `ARMOR_MITIGATION_K=3000.0` imported from `math_model` (single source; verified value), identical to `compute_physical_damage`'s reduction. Because `r_sym <= 92.7% < 0.95` at every shipping tier, `compute_elemental_damage`'s 0.95 clamp never bites, so caster eats EXACTLY `(1 - r_sym)` = the physical factor — symmetry is exact, not approximate (verified algebraically against `math_model.py:116-142`). (b) `max(rolled, r_sym)` raises off-element to the armor floor while keeping the stronger rolled own-element — empirically confirmed: swarm (r_sym=8.1%) keeps both rolls; boss (r_sym=92.7%) floors both up; armor<=0 returns rolls unchanged; new-dict no-mutation verified by direct import test. (c) Does NOT touch the physical/armor path: str `kpm_delta_pct=0.00` and `survive_kill_delta=0.000` on EVERY shell off->on. `MITIGATION_SYMMETRY` OFF preserves the literal `monster.elemental_resistances` reference (byte-identical raw rolls) — confirmed in the diff.

**G5 empirical inspection (Discipline #11, on disk): HELD.** Caster-down: int boss_with_adds KPM 98.96->0.73 (-99.26%), mini_boss survive+kill 1.000->0.000; wis boss 97.60->0.69, boss sk 1.000->0.945; dex boss 308.67->0.37, boss sk 0.838->0.421, mini_boss sk 0.833->0.000. Martial-unchanged: str off==on to 4 decimals on all six shells (G5 falsifier NOT triggered). No over-correction: the `max()` construction guarantees convergence-to, not past — caster on-values sit at or above the str floor (dex boss on sk 0.421 > str 0.250), never below. AUTO-RESOLVE=True, flags_to_kr=[]. Smoke and full both carry the assertion block; smoke ran first per Discipline #2.1.

**Seed hygiene (Discipline #3): CLEAN.** `PHASE4_SEED_BASE = 24_000_000`, span `[24M, 30.617M]`, disjoint from all prior namespaces (all end below 16.66M). Matched-seed off/on toggle is a true single-lever isolation (Discipline #24).

**Semantic-shift continuity (Discipline #12) — FOUR-boundary chain assembled (I have now Gate-2'd all four):**
1. Resource gating (Phase 1) — casts gate on energy; free-spam throttled.
2. Rotation (Phase 2) — selector branches on energy_type; tiers > T1 now fire.
3. DoT (Phase 3) — burn/bleed/drain tick; physical-DoT routes str/dex.
4. Mitigation (Phase 4) — off-element casters now eat the armor-equivalent resist they bypassed.
Post-Phase-4 a production caster KPM = (direct elemental, NOW armor-symmetrically resisted) + (DoT, un-mitigated) gated by resource, fired by rotation. Declared coherently and consistently across all four math-notes. The composed instrument Phase 5 refits against now exists and is internally consistent. **Ready for Phase-5 Gate-6 on the mechanism-correctness axis.**

**Cross-seam (Principle 6): N/A justification VALID.** No telemetry/fight_log/export SCHEMA field added/renamed/removed; only the `elemental_resistances` VALUE on a defender CombatantState changes (internal to the sim seam). No gamora->star-lord contract change. No MIGRATION.md required — correct.

**Test posture (Discipline #2): ACCEPTABLE.** I re-ran the seam-relevant subset (`-k "combatant or from_monster or mitigation or resist or armor"`): 305 passed, 0 failed. The 59 full-suite failures gamora flagged as pre-existing config drift do not touch the mitigation surface — confirmed the seam-relevant surface is green.

## INFO items (carried into Phase-5 Gate-6)

- **[INFO-1] KPM-ceiling saturation masks the mitigation delta on clear shells.** int/wis magic_pack (600.0->600.0) and elite (450/600 caps) show `kpm_delta_pct=0.0` where the math note predicted a drop. This is a KPM ceiling artifact (caster still clears the pack within the window despite reduced per-hit damage), NOT the fix failing to reach the defender — proven by the boss/mini_boss collapse and by dex magic_pack -28.89% (exactly the math-note off-element prediction) where saturation lifts. At Phase-5 the band refit should be aware that caster mitigation shifts are invisible on ceiling-clamped clear shells; the honest mitigation signal lives at boss tiers and on uncapped cohorts.
- **[INFO-2] On-element vs off-element split is design-correct but unmeasured here.** The harness drives mob dominant=physical so all casters attack off-element (the defect case). On-element casters (attacker element == mob dominant) are floored differently (rolled 0.30-0.60 kept at low armor; floored up at high). Phase-5 composed population mixes both; the refit will see a blend. Note for band interpretation, not a defect.
- **[INFO-3 — carry from Phase 3] DoT magnitude un-tuned (0.003 coefficient).** Recompose-first held across all four phases (no magnitude re-tune anywhere). Phase 5 is the first place magnitudes are allowed to move (via band refit, not coefficient edit). The four fixes are mechanism-only; any "the number is wrong" read is Phase-5/Matt territory, not a Phase-1-4 defect.
- **[INFO-4] Two economies DEFER (Skirmisher damage-taken-converts, Crusader HP-economy)** per brief §G1 — 2/10 roster, neither STR, neither blocks the composed instrument. Intentional scope-hold; not a Gate-6 blocker but the composed population at Phase 5 covers 8/10 economies, which the refit framing must state.

## Action

- [x] Developer (gamora): none required. PASS-WITH-INFO; INFO items are for Phase-5 awareness, not rework.
- [ ] KR: Phase 4 closes the four-fix isolated chain. Per the workstream brief, **halt to Matt** before Phase 5 — Phase 5 is gated on the open Matt scope decision (Phase R, rocket reference-economy hardening: does the composed re-baseline refit on the current mana-default-only population, or wait for the doc-48 economies?). Phase 5 does not fire until Matt rules on Phase R.
- [ ] jack-ryan (self, Phase 5): Gate-6 is my structural BLOCK-authority gate (the one composed re-baseline -> Matt band approval). Carry INFO-1 through INFO-4 into it. Gate-6 pending the Phase R decision.

## References

- Math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/armor-resist-symmetry-phase4-2026-06-20.md`
- Fix: `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (`_armor_symmetric_resistances`, `MITIGATION_SYMMETRY`, `from_monster:1097-1142`)
- Resolver symmetry: `~/Games/reincarnated-engine/src/reincarnated/foundation/math_model.py:116-142`
- Harness: `~/Games/reincarnated-engine/src/reincarnated/simulation/armor_resist_symmetry_phase4_harness_2026_06_20.py`
- Results: `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/armor-resist-symmetry-phase4-2026-06-20-{full,smoke}.{json,txt}`
- Dispatch + completion record: `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-20-gamora-phase4-armor-resist-symmetry.md`
- Workstream brief: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§3 Phase-4 + GATE G5, §5)
