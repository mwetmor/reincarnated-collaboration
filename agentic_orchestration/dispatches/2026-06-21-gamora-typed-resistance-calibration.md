# Dispatch — 2026-06-21 — gamora — typed-resistance resolver spine + calibration

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-21 — publish-go on the typed-resistance recal wave.
**Estimated effort:** ~2 waves.
**BLOCKED-UNTIL-ROCKET:** do NOT start calibration until rocket lands BOTH (a) typed resolver-attacker monster skills (the mob carries `resolver_skills` with `element`) and (b) DIFFERENTIATED per-element gear resist. You cannot tune a death channel the mob doesn't emit, and the typed payoff is inert against undifferentiated kits — you can't validate "matching matters" until gear differentiates. rocket dispatch: `2026-06-21-rocket-typed-resistance-gear-and-monster-skills.md`.
**Acceptance:** death channel routed through the resolver with the kit's real per-element defense LIVE; signature-element boss moves from hard-but-doable (unmatched) to comfortable (matched) — no one-shot, no faceroll; re-founded guard PASSES on typed defense; anti-tax JOINT gate holds; trash<boss; bands re-rate ONCE jointly over both axes.

> **Parent MASTER (Gate-1 ENDORSE):** `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`. This pickup is the gamora section extracted verbatim. Gate-1 finding: `qa/findings/2026-06-21-recal-wave-typed-resistance-MASTER-gate1.md`.

## Context

The defensive-axis recal restores a real player-death channel (Matt ruled death a core pillar). Matt LOCKED typed resistances. The corrected spine reroutes the monster→player death channel through `damage_resolver.resolve_skill` with the player as a real DEFENDER (its real `armor` + per-element `elemental_resistances` off `combatant_state`) and the mob as a real resolver ATTACKER — the SAME resolver the player's offense already uses. The 0a de-risk spike (yours) proved this routes CLEAN, differentiation live to float precision, production diff 0 lines. The flat death branch `dmg = raw × (1 − player.armor_factor)` and its global constants are SUPERSEDED.

## Required reading before starting
1. `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` — design of record. **§5** (resolver spine + flat-anchor invalidation — your spine), **§3.3** (the typed band — your target), **§6** (re-founded guard — your acceptance test), **§7** (swarm/trash<boss), **§8** (gamora handoff).
2. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` — YOUR 0a spike (the spine proof + the two engine touches you wire here).
3. `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md` — jack-ryan Gate-1 (the anti-tax JOINT gate contingency).
4. `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md` — threat SHAPE (heavy-slow/variance) — UNCHANGED.
5. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md` — the prior flat diagnostic (anchor now INVALID; carry the analytic TTD/TTK method, NOT the flat numbers).

## NON-NEGOTIABLE GUARDS (carry verbatim)
- **G-A — ANTI-TAX (JOINT gate with rocket):** resistance is REWARD-for-matching, NEVER a mandatory cap. If the only survival path against the signature boss is match-capping its element (no out-play path), or if all-resist stacking dominates matching, the knob-set FAILS. Two viable paths — match the element OR out-play the unmatched fight — or reject the knob-set.
- **G-B — Trash < boss, always.** Boss = signature-element peak; swarm = minor/mixed shallow; trash death-rate STRICTLY below boss for every kit profile.
- **G-C — Content emission HELD until the two-axis joint close.** Do NOT finalize/emit bands.
- **G-D — Flat anchor INVALID.** Do NOT carry `4.0/0.76` or live `0.40/0.95` as a knob-set. Re-derive magnitude from scratch under the resolver curves.

## Scope
- [ ] **(a) Resolver-route spine (§5, 0a-c3 — two engine touches, resolver byte-untouched):** swap the death channel `simulation/spatial_gauntlet/spatial_engine.py:1951` from the flat branch to `resolve_spatial_hit` (live offense route at `:1391`; mob ATTACKER, player DEFENDER); ensure the mob projects a non-empty `resolver_skills` (composes with rocket's typed-skill emission, mob `resolver_skills=[]` today at `:2508`). The player's real `combatant_state` mitigation goes LIVE on defense. `PLAYER_ARMOR_FACTOR_*` (`:159`/`:1575-1578`/`:2390`) becomes inert on the death channel — retire/repurpose; any boss-harder-than-trash scaling moves to the monster attack-magnitude side.
- [ ] **(b) RE-DERIVE magnitude from scratch (G-D):** the flat anchor is INVALID. **Math-before-code the resolver mitigation curves** — `armor/(armor+K)`; per-element `(1 − clamp(res,0,0.95))`; substrate matrix (`damage_resolver.py:456/460/478/485/502`) — BEFORE the sweep, so the sweep is targeted not blind.
- [ ] **(c) Typed band (§3.3):** tune so the resist lever moves the signature boss from *hard-but-doable* (unmatched kit) to *comfortable* (matched kit) — NEVER unmatched-one-shot, NEVER matched-faceroll. Even at the 80% single-element ceiling the boss is a real fight; even at zero matching resist it is survivable-by-skill. The typed analog of the glass-0.6–0.8 / bruiser-0.95 spread.
- [ ] **(d) Re-founded homogenization guard on TYPED defense (§6):** at the chosen knob-set, an UNDER-RESISTED kit must survive the signature boss by playing well (kite the heavy-slow telegraphed slam / kill fast — offense+position substitute), while a MATCHED kit survives more comfortably. Two viable paths or reject. Re-run on real typed per-kit defense; do NOT inherit any flat sweep result.
- [ ] **(e) ANTI-TAX JOINT GATE (G-A):** the chosen band MUST satisfy the anti-tax criterion JOINTLY with rocket's gear differentiation. Converge with rocket+gandalf on the shape.
- [ ] **(f) Trash<boss + swarm typing (§7, G-B):** boss = signature element peak; swarm = minor/mixed shallow. Clear-shell death rare-by-design via per-hit variance (NOT coverage-crank — carried Gate-2 concern); boss-only death is the logged fallback if no guard-respecting clear-shell mechanism lands.
- [ ] **(g) Full-population validation (constraint 9):** typed band + heavy-slow + variance profiles are unmeasured at population scale — validate on a FULL-population sweep, not the single-kit throwaway. Realized band WIDTH at production is the empirical burden.
- [ ] **(h) Two-axis joint re-rate (constraints 7/8):** boss gate is now `survive AND kill`, both graded. Re-rate the banked PROVISIONAL offensive bands ONCE, JOINTLY, over both axes — NOT offense-then-defense in two refits. Output FEEDS the joint band-finalization. **Do NOT finalize/emit.**
- [ ] Single-parameter sweep isolation (#24): isolate the swept parameter per run; do not co-vary spread-target and guard levers in one sweep.
- [ ] Seed hygiene (#3): prior runs used through 46M+; 0a spike used 47M+. **Assign 48M+** (disjoint).
- [ ] MIGRATION.md with star-lord (live survive limb + typed death-cause surface new fight_log fields).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-typed-resistance-calibration-N`

## Cross-seam contract change? (Principle 6 — YES, round-trip REQUIRED)
The live survive limb + typed death-cause surface new fight_log fields → coordinate MIGRATION.md with star-lord. Round-trip smoke: a full-population fight producing a typed death → assert survive-rate + death-cause-WITH-element land in the export packet star-lord consumes.

## Out of scope (explicit non-goals)
- Monster-offense content + gear-resist minting (rocket's lane — you CONSUME both).
- The encounter-model SHAPE + typed-resistance DESIGN (gandalf-ruled — do NOT re-open).
- Band finalization / content emission (Matt-gated joint close).
- Any explicit dodge/reaction model — positional avoidance only (threat-spec §5 UNCHANGED; explicit telegraph-reaction is a named future fork).

## Open questions for you to resolve (and document)
- Exact resolver magnitude at which the typed band hits hard-but-doable/comfortable with no one-shot/faceroll — the band-center tuning under the resolver curves. Math-note it.
- Whether clear-shell death is deliverable via per-hit variance inside the guard+ordering, OR the boss-only fallback fires — log either way.
- (JOINT with rocket+gandalf) the gear-resist generation SHAPE that makes element-matching a better return than all-resist stacking.

## References
- Typed-resistance design-half: `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md`
- 0a resolver spike (spine + two engine-touches): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md`
- Typed-resistance Gate-1: `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md`
- Prior flat diagnostic + Gate-2 (anchor now invalid; carry the method): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`; `qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`
- Engine — death channel (flat, to be swapped): `simulation/spatial_gauntlet/spatial_engine.py:1951`; resolver route `:1391`/`:533-534`; player flat constant `:159`/`:1575-1578`/`:2390`; mob `resolver_skills=[]` `:2508`
- Engine — resolver typed paths: `damage_resolver.py:456/460/478/485/502`
- Disciplines: #1 math-before-code (resolver curves), #3 seed hygiene (48M+), #11 empirical inspection, #12 semantic-shift, #24 single-parameter sweep isolation

---

## Completion record — gamora, 2026-06-21 (SESSION 38)

**Status:** COMPLETE. All scope items (a)–(h) executed. Provisional bands HELD (G-C; NOT finalized/emitted — Matt-gated joint close). AUTO-COMMITTED; NO push.

**Tag:** `gamora/v-typed-resistance-calibration-1`. **Math note (Disc #1, BEFORE code):** `simulation/math/typed-resistance-resolver-spine-and-calibration-2026-06-21.md`. **Harness:** `scripts/gamora_typed_resistance_calibration_2026_06_21_SPIKE_THROWAWAY_.py`. **Raw:** `output/typed-resistance-calibration-2026-06-21-full-20260621_225617.json`. **Seed base:** 48,000,000 (disjoint).

### Scope outcomes
- **(a) Resolver-route spine — DONE, routes CLEAN.** Death channel `spatial_engine.py:1951` swapped to `resolve_spatial_hit` (mob ATTACKER / player DEFENDER) when an index-aligned typed `resolver_skill` + player `combatant_state` exist; flat branch is the byte-identical FALLBACK. Mob projects `resolver_skills` from its typed `skills` (`build_resolver_skills`; was `[]` at :2508). Resolver byte-untouched. `PLAYER_ARMOR_FACTOR_*` inert on the typed death channel (boss-harder scaling → mob `damage_multiplier`).
- **(b) Magnitude RE-DERIVED from scratch (G-D) — DONE.** Math note §1: resolver typed-elemental death dmg = `1000 × dm_boss × (1−clamp(res,0,0.95)) × ±20%var`. Flat anchor (`4.0/0.76` + live `0.40/0.95`) confirmed INVALID (different functional form). Math-before-code authored BEFORE the sweep.
- **(c) Typed band (§3.3) — PROVISIONAL: boss `damage_multiplier`=5.0 @ cd 4.5s.** Unmatched 0.50–0.625 (hard-but-doable, NO one-shot), matched 1.0 (comfortable, NO faceroll). dm=6.0 unmatched=0.0 (too hard); dm=3.0/4.0 unmatched=1.0 (too soft). Band correctly bracketed.
- **(d) Guard re-founded on TYPED defense (§6) — PASS, two viable paths.** Unmatched offense-sweep (24 seeds): dm_mod 1.0→sk 0.50 vs 3.0→0.96 — fast-kill substitutes for matched resist; matched-comfortable is the other path. No mandatory match-cap.
- **(e) ANTI-TAX JOINT GATE (G-A) — HOLDS in PRODUCTION ROLLER.** `sample_scenario_loadout` n=200 → max total resist **1.60 < 2.0** (3.5× short of 5.6 cap-all wall), max single-elem 0.60 < 0.80 clamp.
- **(f) Trash<boss (§7, G-B) — HOLDS** for every cohort once swarm `damage_multiplier` re-derived DOWN 0.85→0.20 (rocket scaffold made aggregate swarm DPS exceed boss). Swarm a_dead=0 vs boss 4–11. Clear-shell death rare-by-design → **boss-only-death fallback fires** (logged; no guard-respecting swarm-death at scale).
- **(g) Full-population validation (constraint 9) — DONE.** 36 legendary configs: unmatched mean sk 0.924 (realized WIDTH 0.438–1.0; ±20%var + pop diversity softens the knife-edge), matched 1.0.
- **(h) Two-axis joint re-rate (constraints 7/8) — PROVISIONAL, NOT finalized/emitted (G-C).** Output feeds the joint band-finalization; Matt-gated.

### Cross-seam (star-lord) — MIGRATION v1.81, ROUND-TRIP REQUIRED
NEW additive `SpatialFightResult.player_death_element` (None / "armor" / "<elem>") — the typed death-cause surface. star-lord: add the DB column + persist in `spatial_recorder._INSERT_SQL` + surface in the export packet; round-trip smoke (typed death → death-cause-WITH-element in the packet). gamora confirmed the field POPULATES (`"fire"` on every typed death).

### Open for Matt (math note §9.7)
Unmatched-difficulty anchor = COHORT fixture (~0.5–0.6, tense) OR POPULATION mean (~0.92)? Sets whether dm_boss pushes toward 6.0. RAISED at the joint close; band NOT locked without disposition.

### Discipline compliance
#1 math-before-code (resolver curves authored before sweep); #3 seed 48M+ disjoint; #11 every engine claim re-derived first-hand; #12 three semantic shifts declared (death re-route / cohort resistances key / mob-as-attacker); #24 single-parameter sweep (dm_boss isolated). Smoke (#2): 405 targeted tests PASS; 53 full-suite failures PRE-EXISTING (stash round-trip IDENTICAL, zero introduced); death-channel determinism golden-stable.
