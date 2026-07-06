# Finding — 2026-07-06 — rocket Leg-1 VARIATION PILOT (summon gen-path + INT B1 + within-cell variation)

**Reviewer:** jack-ryan
**Severity:** PASS (INFO-level notes only; no WARN, no BLOCK)
**Target:** tag `rocket/v-pilot-leg1-summon-int-variation-1`, engine `0eb6e06` (verified: tag == HEAD)
**Developer:** rocket
**Gate:** DEV-MODE Gate-2 with BLOCK authority
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 3 (cross-seam impact), Principle 6 (cross-seam round-trip); Disciplines #1, #1.2, #2, #11, #12
**Gates:** Leg 3 pilot run (2 cells × 100 varied samples) — CLEARED TO FIRE.

## Verdict: PASS. Leg 3 may fire.

## Headline — the KitCandidate.to_character_dict() proxies amendment (A1, not in the ratified math note)

**Clean. It is a legitimate wire-of-the-existing-bridge onto the second emission surface — NOT a divergent/duplicate contract.** Empirically verified (Disc #11):

- Both emission boundaries call the identical bridge function on the identical input:
  - `bc_target_player_class.py:415` — `"proxies": build_proxies_surface(self.skills)` (PlayerClassV2)
  - `season_generation_pipeline.py:519` — `"proxies": build_proxies_surface(self.skills)` (KitCandidate, NEW)
- Same `build_proxies_surface`, same `self.skills` input, same output dict shape. There is one bridge, one contract, now emitted on both surfaces. rocket's "no new contract" claim holds.
- The summon discriminator is `Skill.proxy_geometry` (bridge `proxy_vocabulary_bridge.py:280`), consistent with the parked 2026-06-16 design. NO `PoolMechanic` migration — confirmed the composer is untouched.
- KEY IS ALWAYS PRESENT (`[]` for non-summoners) → consumers read `.get("proxies", [])` uniformly on both paths. Solo path byte-identical.
- Rationale for the amendment is sound: the season pipeline emits `KitCandidate`, not `PlayerClassV2`, so condition A1's round-trip could not hold without wiring the second surface. This was mandated-by-A1, not new design surface.

## What I found (per verification track)

1. **A1 wire (headline):** clean, single-contract, round-trips end-to-end. See above.
2. **proxies cross-seam contract + MIGRATION:** `MIGRATION.md [2026-07-06]` accurately documents `[]`→populated, SHAPE stable, NO PoolMechanic migration. gamora/star-lord/drax consumer notes all present and correct. F1 (roster-fill reads SURVIVAL/tier_2 clear-shell PASS, not emission) captured explicitly. Principle-6 round-trip adequate — smoke asserts field-presence + non-NULL + valid proxy_type at the KitCandidate boundary.
3. **A1 assertion genuine:** smoke asserts on `to_character_dict()["proxies"]` carrying a valid `autonomous_caster` proxy_type (behavioral_tier=full), NOT merely "summon skill present." Solo → `proxies == []`. No hollow-kit escape. Re-ran independently: GREEN with the full decl dict materialized.
4. **5-template set:** import-time assert genuinely enforces chain_A-all-primary_attack in EVERY template (fail-loud at module import) → signature-ailment gate (§1c, `:560`) stays invariant. Templates are mechanically distinct (balanced_striker/control_leaning/dual_offense/support_specialist/warden_leaning). warden_leaning chain_C = control→support×3 (rally/mend the construct). Ruling 2 satisfied.
5. **INT B1 fall-through:** tightly gated (`attribute=="INT" AND matching_policy=="option_beta"`), routes to the existing `_bind_and_build` Step-5 last-resort, stamps `leg1_int_b1_fallthrough=True`. Composes VALID candidates for Cells 12/16; 13 folds to 12, 14 via existing routing. All 4 compose against the real substrate DB. STR-substrate element-incoherence is FLAGGED in the warning log (not silently masked) with B2/elrond named as the out-of-scope quality fix.
6. **Two pre-existing failures — CONFIRMED pre-existing + orthogonal.** Ran on a `f23d353` (parent, math-note-only) worktree baseline: (a) d6 grouping-vocab-doc — collection RuntimeError, canonical `story/` path retired in the 2026-06-30 reorg; reproduces identically on baseline. (b) `test_w3_emission_driver::test_smoke_run_proxy_scaling_contract_present` — hardcoded consistency asserts (entry=2200, ids=22, survivors=700) incompatible with the N=1 smoke path; FAILED identically on baseline. Neither is a regression this build introduced or masked. 225 passed alongside; subspace-generator suite 27 PASS.
7. **Smoke integrity:** re-ran independently — no fights, no full regen, no LLM (T4 closed-form catalog draw). ALL GREEN, ~seconds wall-time. Disc #2 right-tool honored.

## Rationale

Principle 1 (math note ratified BEFORE code, Disc #1/#1.2 — all claims cite file:line, verified against actual code). Principle 2 (smoke gates, no full regen — re-run reproduces GREEN). Principle 3 + 6 (cross-seam `proxies` population change carries an ADR-004 MIGRATION with correct consumer notes + F1 survival-not-emission trigger; round-trip asserted). Disc #11 (empirical inspection — I re-ran the smoke and the baseline; did not trust the report). Disc #12 (signature-ailment semantic invariance preserved by import-assert).

## INFO notes (ride to Leg 4 — do NOT gate Leg 3)

- **INFO-1:** The A4 seed-collision guard `assert n_samples <= 499` is correct for pilot N=100. If any future cell exceeds 499 samples the `+500+sample_idx` offset collides with the next cell's T4 block — the assert fails loud, which is the right behavior, but the offset must widen before any >499-sample cell. Named, not a Leg-3 concern.
- **INFO-2:** INT B1 fall-through binds off any-attribute (STR-flavored) substrate for the 4 INT cells. The pilot will emit element/flavor-incoherent casters for Cells 12/16 within tolerance (dispatch bar is "compose real candidates," met). If Leg-3 pilot data shows the INT cells' flavor incoherence confounds the variation read, B2 (genuine INT substrate, elrond, cross-seam) is the named fix — out of scope here. Empirical criterion for re-engagement: Leg-3 pilot variation/coherence output.
- **INFO-3:** The cell-level representative T4 is retained only for shared-gear scope_preference while per-sample T4 drives the kit. Correct decoupling; noted for the record.

## Action
- [x] Developer (rocket): none required. All 7 conditions closed; build is sound.
- [x] Matt: none required — this is a PASS within jack-ryan's Gate-2 authority (in-seam code + generation-internal config + one wired cross-seam contract with a correct ADR-004 MIGRATION). No milestone tag, no locked-decision conflict, no unresolved BLOCK. Not escalated.
- [ ] knight-rider: Leg 3 (star-lord driver + gamora shells, detached) CLEARED TO FIRE.

## References
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:508-519,955-1130` (KitCandidate proxies wire + per-sample T4 + A4 guard)
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py:364-446,552-561,584-593,695-800` (5 templates + import-assert + _make_summon_skill)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_subspace_generator.py:266-295` (INT B1 fall-through)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_player_class.py:415` (parallel PlayerClassV2 proxies contract — confirmed identical)
- `~/Games/reincarnated-engine/src/reincarnated/generation/proxy_vocabulary_bridge.py:171-172,280,295` (projectile→autonomous_caster; discriminator; build_proxies_surface)
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` [2026-07-06] (proxies contract + F1)
- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/leg1_summon_int_variation_smoke_2026_07_06.py` (re-run GREEN, independent of report)
- Baseline verification: worktree at `f23d353` (both pre-existing failures reproduced identically)
