# Gate-1 Finding — 2026-07-06 — proxy-magnitude calibration math note

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 process/technical side)
**Verdict:** RATIFY-WITH-CONDITIONS
**Target:** `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (gamora, commit `066ba37`)
**Developer:** gamora (simulation seam)
**Companion reviewer:** gandalf (design / class-fantasy dimension, parallel)
**Principles/disciplines applied:** Review Principle #1 (math-before-code), #3 (cross-seam impact), #5 (severity matters); Discipline #1.2 (code citation), #2 (smoke vs regen), #11 (empirical inspection); ADR-002 (tiered approval), ADR-004 (MIGRATION on cross-seam contract).

---

## 1. Marginal-value math — SOUND (ratified)

`required_summon_KPM_contribution = clear_shell_KPM_bar − solo_caster_baseline_KPM` is the correct frame, not "does the pair clear." Subtracting the solo baseline is what distinguishes a validated summoner from a plain caster wearing a cosmetic pet, and it makes the proxy-dominant hazard (F1 / D2-dominance) a *ceiling* violation rather than an accident. Verified against the cited f_army split (`proxy-fight-calibration-2026-07-02.md:166-172`) — the `[0.15, 0.70]` band is the SAME band that governed the boss-shell cert, not a fresh arbitrary pick. The bounds are inherited, not invented; defensible.

**Degenerate case handled correctly.** §1 states: if `solo_caster_baseline_KPM ≥ clear_shell_KPM_bar_lo`, then `required_contribution ≤ 0` → FLAG to Gate, do NOT inflate the proxy to manufacture a pass. This is exactly right and is the trap most calibration notes fall into. Ratified without condition.

One nuance the note itself raises and the Gate must hold gamora to: on the two pack shells the Leg-3 autopsy predicts the solo caster is *above-ceiling*, so `required_contribution` there is not "add DPS" but "add survivability/positioning." The note names this as "the design tension the Gate must weigh" (§2) — correct to surface it, but see Condition 3: the re-fight must not silently apply a DPS lever on a shell where the discriminator is survivability.

## 2. Chassis-coordinate derivation — VERIFIED

All load-bearing numbers check first-hand:
- `PROXY_REFERENCE_HP = 20_000.0`, `PROXY_TIER_HP_FACTOR["full"] = 0.40` → base_hp 8000. Confirmed `proxy_vocabulary_bridge.py:67-73`.
- `proxy_power_per is None → damage_multiplier 1.0`. Confirmed `:232`.
- `PROXY_TIER_MAX_ACTIVE["full"] = 1`. Confirmed `:77-81`.
- `SPATIAL_DAMAGE_SCALE = 0.6` (G5 propagation floor). Confirmed `spatial_engine.py:326`.
- The sim CURRENTLY hard-codes ally `damage_modifier=1.0` at spawn. Confirmed `spatial_engine.py:1773`. The note correctly flags this default-vs-0.6-floor divergence and requires the re-fight to STATE its regime (§3, §5.3).
- The coalesce path (`None or 0.0`, `_is_fighting_decl` needs `damage_multiplier > 0`, `targetable = base_hp > 0`) all confirmed at `spatial_engine.py:103-108, 1741-1742, 1765`.
- Clear-bar table (9.90/15.53, 11.65/15.88, 18.61/100.00, 8.26/28.13) byte-matches `gauntlet_sim.py:393-398`; pass logic is floor-AND-ceiling on `tier_2_kpm`, confirmed `:680-691`.

Derivation transfers to emitted kits correctly: expressing anchors as `CHASSIS_HP_REFERENCE × hp_factor(tier)` rather than hard-coded 8000 is the right move for emission portability.

## 3. THE LOAD-BEARING CAVEAT — I AGREE. Cross-seam escalation, correctly deferred.

The two WR=1.0 anchors are MELEE; the caster proxy is RANGED, the same shape as `demo_gravecaller` which FAILED WR 0.0. Verified: `proxy-fight-calibration-2026-07-02.md:304` records gravecaller "delivers ONLY ~1000 vs 30k boss; never re-engages" — a NAV/re-engage gap, NOT a magnitude shortfall. This is the crux, and gamora's disposition of it is correct on both counts:

**(a) It is genuinely cross-seam and NOT resolvable in the sim seam.** A ranged/melee split lives in `PROXY_TIER_HP_FACTOR` / the count-wall table inside `proxy_vocabulary_bridge.py` — that is a rocket-seam GENERATION primitive, not a sim tuning knob. gamora is right to route it to knight-rider rather than patch it in sim. Per ADR-002 this exceeds the sim seam's authority. Ratified as escalation, not sim work.

**(b) It does NOT block THIS re-fight — because the re-fight runs the CLEAR shells (packs), not the boss shells.** The gravecaller failure was boss-specific: a single boss lets a ranged ally drift out of range and evaporate. On a pack shell the nearest-enemy nav target is a dense field, so the range gap is far less binding (Leg-3 note :116; nav `spatial_engine.py:~1996`). The caster-cell pack re-fight is therefore the HONEST test of whether the melee-derived anchor transfers to a ranged proxy. **This is the key finding: the caveat does NOT block the re-fight; it is precisely what the re-fight measures.** If the ranged proxy still evaporates on packs, THAT is the empirical trigger to raise the ranged-primitive question to knight-rider — with evidence, not speculation. The architecture is actionable now; the primitive question is answered BY the re-fight, not before it.

## 4. Code-citation discipline (#1.2) — one INFO drift

Every load-bearing NUMBER is cited to file:line and every one I spot-checked verified first-hand. **INFO (not blocking):** the note cites `spatial_engine.py:NNNN` but the file actually lives at `simulation/spatial_gauntlet/spatial_engine.py`. The basename is unique so greps resolve, but Discipline #1.2 prefers a resolvable path stem. Fix on next touch; no re-fight impact.

## 5. "Does the emitted thing FIGHT?" (Matt's new run-boundary checklist question) — PARTIALLY ADDRESSED → Condition 1

The note's re-fight plan (§5.4) reads `proxy_realized_damage_dealt` per clear shell and checks `f_army ∈ [0.15, 0.70]`. That correctly catches evaporate as an OUTCOME (contribution ≈ 0). But reading realized-damage AFTER the fight does not, on its own, verify the proxy ENGAGED — a magnitude that is right but a nav gap that keeps the proxy from re-engaging produces the same near-zero number, and the plan would then mis-attribute a NAV failure to a MAGNITUDE shortfall (or vice versa). The gravecaller lesson is exactly this confound. The plan needs an explicit engagement gate BEFORE reading KPM (see Condition 1).

---

## Conditions (RATIFY-WITH-CONDITIONS)

1. **[BLOCK-until-added to re-fight plan] Engagement verification precedes KPM read.** Before attributing a low `f_army` to magnitude, the re-fight must confirm the proxy actually engaged — e.g. proxy attack-count > 0, or time-in-range > 0, or a per-proxy "delivered any damage" flag distinct from total realized damage. Without it, a nav-borne evaporate is indistinguishable from an undersized magnitude, and the calibration lever chosen would be wrong. This is the direct answer to Matt's run-boundary question and is non-optional. gamora: add the engagement-gate assertion to §5 before the re-fight fires.

2. **[Condition] State the `damage_modifier` regime in the re-fight header, not just narratively.** The sim default is 1.0 (`:1773`); the G5 floor is 0.6 (`:326`). The anchor math is derived at 0.6. The re-fight must run and REPORT the 0.6 regime (or justify 1.0), because a 1.0/0.6 mismatch is a silent 1.67x on all contribution numbers. The note names this (§3, §5.3) — make it a stated harness parameter, not a footnote.

3. **[Condition] Do not apply a DPS lever on the above-ceiling pack shells.** On magic_pack/elite_pack the Leg-3 autopsy predicts the solo caster is above-ceiling; there `required_summon_KPM_contribution` must NOT be met by adding proxy DPS (that pushes further past the ceiling = D2-dominance). The lever there is survivability/positioning per §2. Hold the re-fight to selecting `base_hp` (not `damage_multiplier`/`proxy_max_active`) as the pack-shell knob, consistent with §4's stated preference order for the ranged cell.

4. **[Condition, procedural] The ranged/melee tier-split question routes to knight-rider as a rocket-seam primitive — with the re-fight evidence attached.** No MIGRATION.md is needed for THIS calibration (decl shape unchanged, values move off None — confirmed, ADR-004 not triggered). But if the pack re-fight shows the melee-derived anchor does not transfer, the escalation must carry the empirical delta, not just the a-priori caveat.

---

## Action
- [ ] gamora: add engagement-gate assertion (Condition 1) to the re-fight plan §5 before firing.
- [ ] gamora: promote `damage_modifier` regime (Condition 2) and pack-shell lever restriction (Condition 3) from narrative to stated harness parameters.
- [ ] gamora / knight-rider: hold Condition 4 — ranged-primitive escalation carries re-fight evidence.
- [ ] Matt: no decision needed at this Gate. Conditions 1-4 are sim-seam-executable; the note is ratified to proceed once Condition 1 is in the plan. The ranged-primitive question (Condition 4) reaches Matt via knight-rider ONLY IF the re-fight surfaces the non-transfer empirically.

## References
- `reincarnated-engine/src/reincarnated/simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md`
- `reincarnated-engine/src/reincarnated/simulation/math/proxy-fight-calibration-2026-07-02.md:302-304, 166-172`
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:389-401, 680-691`
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:103-108, 326, 1741-1742, 1765, 1773`
- `reincarnated-engine/src/reincarnated/generation/proxy_vocabulary_bridge.py:67-81, 232, 255`

**Signed:** jack-ryan, 2026-07-06 — Gate-1 process/technical review, RATIFY-WITH-CONDITIONS.
