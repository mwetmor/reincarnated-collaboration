# Finding — 2026-06-20 — boss-gate build (§6 encounter-measurement doctrine)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no BLOCK)
**Target:** `gamora/v-boss-gate-1` — engine commit `50caa12`; collab `2c75e0c`
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #1 (math-before-code), #3 (seed hygiene), #12 (semantic-shift declaration)
**ADRs:** ADR-004 (MIGRATION), ADR-006 (read-only verify)

## Verdict

**PASS-WITH-INFO.** The boss-gate instrument is mechanically sound. The three moves are correctly scoped to boss shells, the clear-shell KPM gate is provably untouched (no regression), DPS/TTK record and gate nothing, and the inverted §5 table is the composed instrument's honest output, NOT a wiring fault. The inverted boss-shell disposition is a DESIGN input that routes to gandalf + Matt (the boss-half approval halt), not a Gate-2 BLOCK.

## What I found

All six Gate-2 load-bearing items verified first-hand against current code, the commit diff, and the 1440-cell verification JSON:

**1. Mechanism correctness (scoping) — CONFIRMED.** A single `_BOSS_SHELL_GATE_TYPES = frozenset({"boss_with_adds", "mini_boss"})` (`gauntlet_sim.py:183-186`) gates BOTH moves. Move (a): the tier_1 REJECT short-circuit at `gauntlet_sim.py:1080-1081` now reads `if t1_routing == TIER_1_REJECT and not _is_boss_shell` — the guard is membership-keyed, boss-only. Move (b): `eligible_encounters_passed` at `gauntlet_sim.py:621-628` branches `if enc_type in _BOSS_SHELL_GATE_TYPES` to the sg2 survival predicate; the KPM-band branch (630-641) is the untouched `else`-path. No clear shell (open_arena, chokepoint_corridor, magic_pack, elite_pack) can enter either boss branch. Hard scope boundary holds.

**2. No clear-shell gate regression — CONFIRMED (this was the BLOCK-worthy condition).** From the verification cells: 719/720 clear (open_arena) control cells REJECTed at tier_1; ALL 719 short-circuited (sg_overall=BLOCK, tier_2_survival_rate==0) — zero clear cells ran tier_2 after a REJECT. `clear_control_pass_count = 0` (KPM-band). The one non-REJECT clear cell (str/DPS-min-maxer, KPM 18.1 in-band) ran tier_2 normally, which is correct pre-existing behavior. Clear-shell behavior is byte-equivalent.

**3. V-gates — CONFIRMED.**
   - (a) 693/720 boss cells REJECTed-at-tier_1 but ran tier_2 (matches gamora's report exactly).
   - (b) boss gate counts via sg2; pass counts {str:108, dex:99, int:108, wis:255} reproduce from JSON.
   - (c) `damage_to_boss` / `boss_max_hp` / `player_damage_dealt` appear ONLY in `t4_sim_cycling.py:210-211` dataclass field defs — grep-confirmed NO gate/conditional/band/floor predicate references any of them. Present and ungated.

**4. Substrate-drift claim (the central flag) — ADJUDICATED: the gate is sound and the inverted table is honest.** Verification reproduces str 1.000 / int 0.750 / wis 0.716 / dex 0.917 (the §5-inverted numbers). This is composed-instrument substrate drift, not a wiring bug, proven by three independently-verified legs:
   - **(strongest, I verified directly)** `git show --name-only 50caa12` touches ONLY `gauntlet_sim.py` (gate), the verification harness, the math note, AGENT_STATE.md, and the test file. The fight path (`t4_sim_cycling.py`, `spatial_engine.py`, `damage_resolver.py`, `arena.py`) is NOT in the commit — byte-unchanged. A gate-only diff is mechanically incapable of perturbing fight outcomes.
   - The composed-instrument chain landed BETWEEN §5 and the gate, confirmed by commit timestamp: §5 = `2f9c5c8` (2026-06-19 20:34) → `c28d027` Phase 1 → `e2f3929` Phase 2 → `9e1d25d` Phase 3 → `d2d3dde` Phase 4 → `c502451` Phase R (all 2026-06-20 15:32–18:55) → gate `50caa12` (20:35). Five fight-path-altering commits separate §5 from now.
   - gamora's third leg (§5 harness re-run unmodified gives the inverted numbers) I did not independently re-execute (478s harness; read-only review). Legs 1+2 are sufficient: fight path byte-unchanged + five fight-altering commits since §5 → §5 staleness is mechanically necessary, not optional.

   Conclusion: the wiring reads whatever the fight engine produces and does not corrupt it. The inverted disposition is the now-correct instrument honestly measuring the composed substrate.

**5. Seed hygiene (Discipline #3) — ACCEPTABLE.** Verification drove the gate's internal deterministic bases (t1=7000/t2=11000, per-config disjoint via `config_idx*100_000`). The declared-not-used fresh-48M base is acceptable here: this is a gate-wiring BEHAVIOR verification (deterministic correctness), not a fresh band-fit, so seed-collision is not a contamination risk. The reasoning is sound and explicitly declared. (INFO below.)

**6. Semantic-shift declaration (Discipline #12) — CONFIRMED.** Declared in math-note §7 AND embedded in the docstring at `gauntlet_sim.py:608-612`. Coherent with the four prior phase boundaries and the composed boundary: "passed" for boss shells moves from KPM-in-band (with ceiling) to survive-and-kill ≥ cohort floor (no ceiling). Clear shells unchanged.

**7. Tests — CONFIRMED legitimate (49/49 PASS, re-run first-hand).** The 7 updates are two legitimate categories, neither gate-masking: (i) stale-floor corrections (`2 of 4` → `9 of 18`) reflecting the live `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9` that landed 2026-05-28 (W-α6) and was never propagated to the fixtures — genuine pre-existing HEAD failures; (ii) win-condition-split adaptation deriving boss-shell pass from `tier_2_survival_rate` (0.99 PASS / 0.0 FAIL) mirroring the new gate branch. The added `assert GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 == 9` is a good guard. Assertions still test pass/fail at the floor — not masking.

## Rationale

REVIEW_PROCESS #1: math-note precedes code, pre-registers the falsifiable §5 expectation (math-note §4), and the FALSIFICATION (the inverted table) is surfaced not smoothed (math-note §10) — the discipline working exactly as intended. REVIEW_PROCESS #2: smoke-first then full verification (1440 cells, 478s). REVIEW_PROCESS #3 / ADR-004: no field crosses the sim→telemetry seam newly (DPS/TTK crossed in the Matt #8 build with its own MIGRATION); no new MIGRATION required — correctly assessed. Discipline #12 satisfied across the boundary. The scope boundary (boss-only via frozenset membership) is the structural guarantee that makes "no clear-shell regression" provable rather than merely tested, and the cell data confirms it empirically.

## Action

- [x] Developer (gamora): nothing required for Gate-2 clearance. Build is sound.
- [ ] knight-rider: draft the decisions-log entry implementing the §1/§6-AGREED doctrine (Matt 2026-06-19); route to jack-ryan for review. The entry records the boss-shell win-condition split as built; the resulting disposition lands at the Matt halt.
- [ ] gandalf + Matt (design-fit / approval halt): the inverted boss-shell disposition is the design input. STR now SHIPS boss shells (1.000 survive+kill) under the composed instrument — the §5a-predicted focus-fire lever is ACTIVE via the rotation/economy (Phase R), NOT via DoT (rocket 2026-06-20: STR bleed still not emitted in the generation population). Casters drop (int 0.992→0.750, wis 0.984→0.716) eating the boss armor wall from Phase 4 mitigation symmetry. The spec §3 "EXPECTED STR-timeout=1.000" is FALSIFIED — and that falsification is itself the finding. This is the boss-half of the Phase-5 band-approval halt; clear-half stays deferred behind the magnitude pass.

## INFO (non-blocking)

- **INFO-1 (seed):** the fresh-48M base was declared-not-used; the gate's internal fixed bases were used instead. Acceptable for a behavioral verification. If a future run on this gate needs band-fit characterization (not just wiring), use the declared 48M base then. Cite: Discipline #3.
- **INFO-2 (residual band rows):** the boss rows in `ENCOUNTER_COHORT_KPM_BAND` are left in the dict (no longer consulted for the boss ship gate) to preserve the structural assert and the tier_1 sweep's band_override telemetry. Deletion deferred (math-note §9). No correctness impact; flagged so a future reader does not mistake the dead rows for live gate inputs.
- **INFO-3 (two co-existing in-band defs):** the serialized per-row `enc_result.in_band` (set at `:1134` via `get_archetype_cohort_kpm_band`) is a DIFFERENT, non-shipping band from the ship gate `eligible_encounters_passed`. gamora correctly left `in_band` as telemetry-only and changed only the ship gate. This is a standing readability hazard (the GATE-1 addendum's "two in-band definitions"), not introduced by this build — noting for the record.

## References

- Spec: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-boss-gate-implementation-spec.md`
- Math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/boss-gate-2026-06-20.md`
- Code (re-traced first-hand): `gauntlet_sim.py:183-186` (frozenset), `:621-628` (move b), `:1080-1081` (move a guard), `:608-612` (semantic-shift docstring); `t4_sim_cycling.py:133-138` (SURVIVAL_FLOOR_BY_COHORT), `:210-211` (DPS fields, ungated)
- Tests: `~/Games/reincarnated-engine/tests/test_cycle13_wave5_gauntlet_sim.py` (49/49 PASS re-run)
- Verification JSON: `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/boss-gate-verification-2026-06-20.json` (1440 cells; clear 719/720 REJECT+short-circuit, boss 693/720 REJECT+ran-t2)
- Commit chain (substrate-drift proof): §5 `2f9c5c8` → `c28d027`/`e2f3929`/`9e1d25d`/`d2d3dde`/`c502451` → gate `50caa12`
