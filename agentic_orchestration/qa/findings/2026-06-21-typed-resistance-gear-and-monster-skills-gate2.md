# Finding — 2026-06-21 — typed-resistance gear-minting + typed monster skills (Gate-2 DEV-MODE)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (verdict: **PASS** — gamora released)
**Target:** tag `rocket/v-typed-resistance-gear-and-monster-skills-1`, engine commit `75d7dd4` (9 files, +922 lines, LOCAL)
**Developer:** rocket
**Mode:** Gate-2 DEV-MODE (HARD-BLOCKS gamora — this PASS releases the calibration fire)
**Principles applied:** Review #1 (math-before-code), #2 (smoke/scope-gate), #3 (cross-seam round-trip), #5 (severity); Disciplines #1 (math-before-code), #11 (empirical inspection over assumption — every claim re-derived first-hand from source + run), #12 (semantic-shift declared).

## What I found

I re-derived every load-bearing claim first-hand from live source and ran the artifacts myself (Discipline #11 — took nothing on faith). The Path-A/Path-B scope call is **SOUND**: Path A (`gear_generation`/`GearStats` → `combined_stats` → `combatant.elemental_resistances` → `damage_resolver.py:478`) is genuinely the production-sim consumption path the resolver reads off, element selection genuinely already rides the EXISTING `RolledEffect.element` field (`gear_schema.py:54-58`, populated from `EffectPoolEntry.element`), so the delta was genuinely the SMALL mint (new `element_resist` effect type + one `_derive_stats` branch + a 0.80 clamp) with no schema/aggregation/sim change — and it satisfies the §4 DoD cleanly. Path B (partition/keystone diagnostic + `compute_balance_gear_stats` stopgap) is the surface my Gate-1 0b-c3 MEDIUM-add sized, and it is correctly confirmed "NOT wired into the sim," deferred as a logged choice in the math-note §0 + MIGRATION RESIDUAL — not silent drift. The anti-tax property (G-A) is genuine reward-for-matching, not a tax-in-disguise. The geometry HARD constraint genuinely raises on unwired geometry. The 7 (broader: 55) test failures are genuinely pre-existing — I confirmed the failure set at HEAD is byte-identical to HEAD~1 (pristine, pre-commit). One real foundation gap exists for gamora to bridge, and rocket disclosed it explicitly (handoff note 5 + MIGRATION SURFACE-1) — it is gamora's lane per the design, not a rocket DoD failure. Verdict: **PASS.**

### Claim-by-claim, all from live source / first-hand runs

1. **Path A is the production-sim path — CONFIRMED end-to-end.** `_derive_stats` writes `resistances[e.element] += mag` (`gear_generation.py:969-980`) → `combined_stats` sums per-element + clamps to `[−1.0, 0.80]` (`gear_schema.py:252-267`) → `combatant.py:575` reads `gs.elemental_resistances` into `g_resistances` → `combatant.py:926` sets `elemental_resistances=g_resistances` → resolver reads `defender.elemental_resistances.get(element, 0.0)` (`damage_resolver.py:478`). The element key is preserved at every hop. `RolledEffect.element: str | None` exists at `gear_schema.py:54-58`. **The SMALL-mint sizing is correct on this path; the MEDIUM-add lands on Path B (the diagnostic surface), which is genuinely off the critical path.**

2. **Differentiation end-to-end through PRODUCTION aggregation — CONFIRMED (ran the smoke first-hand, 15/15 PASS).** A fire-weighted loadout yields `combined_stats().elemental_resistances = {'fire': 0.55, 'water': 0.10}` — fire > water > earth(0). The stacked-cap case (4×0.25 fire = 1.00 raw) clamps to 0.80. This is the production `Loadout.combined_stats()`, not a fixture. The round-trip ratio **0.315789** = `(1−0.70)/(1−0.05)` matches the 0a-spike analytic to float precision (verified `abs(observed−analytic) < 1e-6`).

3. **Anti-tax (G-A) — GENUINE reward-for-matching, not a tax.** Verified arithmetic: budget `N·r_hi ≤ 6·0.25 = 1.5` resist-units; capping all 7 elements needs `K·C = 7·0.80 = 5.6` — physically impossible (3.7× short, confirmed in smoke). Matching the signature element concentrates the budget into one element → `min(1.5, 0.80) = 0.80` → eats 20%; spreading puts `1.5/7 = 0.214` on the signature → eats ~78.6%; matched-take/spread-take = **0.255** (~4× the defensive return for matching). Because the budget forbids an all-element wall, the ONLY paying defensive play is to choose-which-element = match-the-fight. It cannot collapse into "cap everything" within the envelope. **This is the §3.1 "build against a named threat" property, structurally satisfied — not a mandatory cap.**

4. **Geometry HARD constraint — CONFIRMED at the boundary.** The wired spatial set is `{circle, cone, line, point, mixed, none}` (`spatial_engine.py:316`); `mixed`/`none`/unmapped fall to the no-hit `return []` (`:740-741`). The emitter's `WIRED_SPATIAL_GEOMETRIES = {point, circle, line, cone}` is exactly the four hit-detecting geometries, and `make_typed_attacker_skill` RAISES `ValueError` on anything else (also raises on `element="physical"`). Verified in smoke S2.h. **No silent damage-less threat can be minted.**

5. **The 7 (55) test failures — GENUINELY pre-existing.** Full suite: 55 failures at HEAD; 55 at HEAD~1 (pristine). `diff` of the two failing-node-id sets = **IDENTICAL — zero failures introduced by this commit.** The family is element-count drift (`test_foundation::test_has_five_elements`, `test_substrate_identity_loader::test_rotating_elements_count_is_four`, the cycle12 convergence/wireup suites) — tests asserting 4/5 rotating elements against the live 7-substrate config. None touch gear/typed-monster-skills. All 613 gear-tagged tests pass. rocket's "7 on touched modules" was a conservative under-statement, not an over-claim.

6. **MIGRATION.md + round-trip smoke — both surfaces covered, honest.** SURFACE 1 (differentiated `GearStats.elemental_resistances`, no reader change, RESIDUAL Path-B deferral documented) + SURFACE 2 (typed monster-skill dict contract, the live gamora handoff). Discipline #12 semantic-shift declared. Round-trip present and run (15/15).

## The one foundation gap — disclosed, and it is gamora's lane (NOT a rocket DoD failure)

The recal sweep's PLAYER-defender combatant in `t4_sim_cycling` is built via `_build_cohort_combatant_stats` (`:909`) → `from_player_class(with_gear_stats=…)`, which takes the legacy-dict branch `g_resistances = d.get("resistances", {})` (`combatant.py:602`). The four cohort dicts carry **no `"resistances"` key** — so the sweep's player defender currently has EMPTY per-element resist. Path A's differentiated output flows through `with_gear=Loadout` (`combatant.py:566/575`), a DIFFERENT branch the sweep does not currently use.

This is NOT a Path-A/Path-B conflation and NOT a DoD miss:
- The §4 DoD is "a kit can build a defensive elemental identity, minted onto per-instance `GearStats.elemental_resistances` with the element key preserved." Path A satisfies that exactly — verified.
- WHICH combatant-build path the recal sweep uses for its player defender is gamora's §5 spine work (design-half §5/§8a: "route the death channel ... with the player as a real DEFENDER ... the kit now provides mitigation"). The dispatch puts resolver-route wiring + cohort profiles explicitly in gamora's lane (§54; handoff note 5).
- rocket disclosed this verbatim: handoff note 5 ("the synthetic-cohort dicts still carry no `resistances` key — populate with typed cohort profiles ... separate path; not changed here") AND MIGRATION SURFACE-1 ("that is a SEPARATE non-gear path and is gamora's to populate"). No papering-over.

**Why this does NOT block:** gamora cannot calibrate a false foundation, because bridging this gap IS step one of gamora's calibration work — she must wire the player defender to carry real per-element resist (either route the sweep through `with_gear=Loadout`/Path A, or populate the cohort dicts' `resistances` key with typed profiles) before the typed band means anything. Path A is the correct, verified source of that resist. The foundation is sound; the wiring that consumes it is gamora's next move. I elevate this to a first-class gamora-carried item below so it cannot be missed.

## Rationale

PASS rather than BLOCK because every load-bearing claim holds at source and in execution (Discipline #11), the cross-seam contract is MIGRATION-gated with both surfaces and a run round-trip (Review #3), math-before-code is satisfied (Review #1, Discipline #1 — math-note authored before code, anti-tax arithmetic proven), and the one foundation gap is (a) genuinely gamora's design-assigned lane, (b) explicitly disclosed, and (c) the necessary first step of gamora's own work rather than a defect rocket left behind. The scope divergence from my Gate-1 MEDIUM-add sizing is RESOLVED in rocket's favor: my sizing was correct for Path B (the surface I traced), and rocket correctly identified that the load-bearing path is Path A, where `RolledEffect.element` makes it the small mint. Better outcome than Gate-1 projected (smaller change, DoD met).

## Action

- [x] jack-ryan: PASS — gamora released to fire calibration.
- [ ] rocket: none required. (Optional, INFO: the `_EFFECT_POWER_WEIGHT["element_resist"]=0.50` is a documented scaffold; flag to gamora it is unvalidated against typed power-budget.)
- [ ] knight-rider: release gamora's calibration fire on this PASS.

## Five consumption notes gamora must carry (rocket handed these; I confirm 1–5 and ELEVATE one)

1. **[CONFIRMED]** Plug emitted `skills` (`emit_skills_for_threat_tier` / `emit_boss_signature_skills` / `emit_swarm_minor_mixed_skills`) into the synthetic-mob dict at `t4_sim_cycling.py:1082` (the `"skills": []` site). Verified that is the correct site (`_synthetic_mob_dict_for_spatial`, attacker side).
2. **[CONFIRMED]** Route the death channel through `resolve_skill` (player-as-defender/mob-as-attacker); populate `resolver_skills` (today `[]` at `spatial_engine.py:2508`) from the projected typed skills; resolver byte-untouched per the 0a spike.
3. **[CONFIRMED]** Own ALL magnitude CONSTANTS (`damage_multiplier`/`cooldown_seconds`/variance); re-derive from scratch under the resolver — flat anchor INVALID; tune CONSTANTS within the heavy-slow/light-variance SHAPE, do not change the SHAPE.
4. **[CONFIRMED + ELEVATED — the single load-bearing gate]** Keep production `N·r_hi < ~2.0` (the joint G-A anti-tax envelope). NOTE: the 0.80 clamp caps any SINGLE element but does NOT cap total budget across elements — the property holds only while `N·r_hi` stays well below `K·C=5.6`. This must be held in the PRODUCTION roller (`r_hi`/`N` from `gear_catalog` element_resist entries `[0.05,0.25]` × resist-eligible slot count), not just in the smoke. **This is the single point where the typed headline can quietly fail — verify it on the production-rolled kit distribution before locking the band, per design-half §4 + my Gate-1 Concern 2.**
5. **[CONFIRMED — and I ADD: this is the gating first step, not optional]** The synthetic-cohort dicts (`_build_cohort_combatant_stats`, `combatant.py:602` legacy-dict branch) carry no `resistances` key, so the sweep's PLAYER defender currently has EMPTY per-element resist. **Before the typed band means anything, wire the sweep's player defender to carry real per-element resist** — either route it through `with_gear=Loadout` (Path A, the verified source) or populate the cohort dicts' `resistances` key with typed profiles. Path A is the verified differentiation source. Treat this as step zero of calibration, not a separate-day nicety — a band calibrated against an empty-resist defender measures nothing the typed wave intends.

**Correction I'd add to rocket's framing:** note 5 reads as optional ("if you want typed defenders in the sweep"). It is not optional for THIS wave — the typed-resistance headline IS typed defenders in the sweep. Without it, gamora calibrates a band on a player who has no per-element resist, which is exactly the false foundation knight-rider asked me to guard against. The foundation (Path A) is sound; consuming it is mandatory, not discretionary.

## References

- Build: tag `rocket/v-typed-resistance-gear-and-monster-skills-1`, commit `75d7dd4`
- Path A chain (verified): `gear_schema.py:54-58` (RolledEffect.element), `gear_generation.py:969-992` (_derive_stats mint), `gear_schema.py:252-267` (combined_stats sum+clamp), `combatant.py:566/575/926` (consumption), `damage_resolver.py:478` (resolver read)
- Path B (deferred, confirmed diagnostic-only): `partition_schema.py:505-546` (no element field), `keystone_loadout_materializer.py:273-279` (even-spread, "NOT wired into sim"), `gear_catalog.py:173-192` (compute_balance_gear_stats stopgap)
- Emitter: `generation/typed_monster_skills.py` (raises on unwired geometry/physical); geometry boundary `spatial_engine.py:316/740-741`
- Pool/categorization: `gear_catalog.py:149-150` (element_resist raw [0.05,0.25]), `effect_categorization.py:49` (DEFENSIVE_EFFECTS)
- The gamora-bridge gap: `t4_sim_cycling.py:909` (_build_cohort_combatant_stats, no resistances key), `combatant.py:602` (with_gear_stats legacy-dict branch)
- Round-trip smoke (run first-hand, 15/15): `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py`
- Math-note: `generation/math/typed-resistance-gear-and-monster-skills-math-2026-06-21.md` (§0 Path-A/B confirm-trace; §1 anti-tax arithmetic)
- MIGRATION: `generation/MIGRATION.md` [2026-06-21] entry (both surfaces)
- Test parity: 55 failures HEAD == 55 HEAD~1, failure-node-id sets diff IDENTICAL (pre-existing element-count drift)
- Gate-1 this build resolves against: `qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md` (Concern 2 anti-tax, Concern 3 MEDIUM-add sizing)
