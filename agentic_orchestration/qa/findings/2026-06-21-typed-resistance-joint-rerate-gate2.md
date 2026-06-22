# Finding — 2026-06-21 — typed-resistance FINALIZED two-axis joint re-rate (G-C / §6h)

**Reviewer:** jack-ryan
**Severity:** PASS (verdict: **PASS** — bands are CLEAN for Matt to take at the G-C close)
**Target:** engine commit `2b52700` on `main`, tag `gamora/v-typed-resistance-joint-rerate-1` (push held, ADR-006)
**Developer:** gamora
**Mode:** Gate-2 DEV-MODE — terminal validation artifact of the typed-resistance recalibration wave; this gate is the last one before Matt's G-C close.
**Principles applied:** Review #1 (math-before-code spine), #2 (smoke-gate), #4 (decisions/disposition as truth), #5 (severity); Disciplines #1, #2, #3, #11, #12; ADR-006.

## What I found

I re-derived every load-bearing claim first-hand — from the live diff, the harness source, the raw output JSON, the math note §10, the anchor ruling, and my own prior calibration Gate-2 finding (Discipline #11 — nothing on faith). **All six gate teeth hold.** The two single most important checks both PASS at source: (1) the anchor is genuinely LOCKED — `DM_BOSS_LOCKED = 5.0`, `DM_SWARM_LOCKED = 0.20`, `CADENCE_LOCKED = BOSS_SHAPE["cooldown_seconds"]` (4.5 s) are hard constants (harness L52–55), `boss_mob_dict(DM_BOSS_LOCKED, CADENCE_LOCKED)` is the only call site (L177), and there is **no sweep over `dm_boss` anywhere** in the harness — the anchor cannot be silently re-opened by construction; the output JSON `anchor` block records `dm_boss_locked=5.0 / dm_swarm_locked=0.2 / cadence=4.5`, confirming the run executed at the ruled values, not a different dm. (2) the refit is **genuinely JOINT** — `survive_kill = sum(fr.winner == "player") / n` (L140); `winner=="player"` requires the kit BOTH outlived the boss AND killed it within the 240 s enrage window — a single survive∧kill outcome metric, ONE refit graded across the resist axis at the locked offense (L188–200 single loop), NOT a survive-only fit with a kill check bolted after. The §6h two-axis joint-gate contract is met. Every self-reported number verifies against the raw JSON: cohort unmatched r=0 = 0.333 (DPS-min-maxer, thinnest) / 0.500 (Hybrid) / 0.542 (Balanced) / 0.625 (Defensive), matched r≥0.20 = 1.00 across all four; population (n=36) unmatched mean 0.926 range [0.292, 1.00], matched 1.000; all four guards `True` (G1 mean_dur 12.4 s, G2 min 1.0, G3 max_total_resist 1.50 < 2.0, G4 trash a_dead 0 vs boss 4–11); live death channel typed fraction 1.0 (48/48 cohort, 1.0 population). Production-code reach: **zero** — the diff is harness (`scripts/`), `AGENT_STATE.md`, the math note, and two output JSONs; no production `.py` is touched, and the harness contains no DB-write / content-emission / `_V2_17/18/19` / `_DEFERRED_PROXY_BINS` reach (grep-confirmed NONE). The math note §10 is a true math-before-code deliverable: §10.1 records the locked anchor and §10.2 the derivation/contract BEFORE the §10.3 guard results; §9.6 is marked SUPERSEDED-BY-§10 and §9.7's reserved anchor question is marked RESOLVED.

The two CONCERNS I carried forward from the calibration Gate-2 are both cleanly retired here: **CONCERN-2** (do NOT lock 5.0 vs 6.0 without Matt disposition) is resolved by gandalf's anchor ruling (Matt-agreed) — gamora honors it exactly and does NOT self-resolve the anchor; **CONCERN-1** (noisy 16-seed offense-substitution limb) is moot at the locked anchor — this re-rate runs no offense sweep, so G1 is now a clean no-one-shot duration/ceiling check, not a 6-point monotone with a dip.

## Rationale

PASS (not PASS-WITH-CONCERNS) because every gate criterion holds at source AND in execution, and the two carried concerns are genuinely retired by the ruling + the lock — not deferred again:

1. **Gate tooth #1 — anchor LOCKED, not re-opened (the single most important check).** dm=5.0 / swarm=0.20 / cadence 4.5 s are compile-time constants with a single call site and no sweep grid; the anchor source is cited inline (L12, L52, output `anchor.source`). This is the §"why not 6.0" disposition honored to the value. Disposition-as-truth (Review #4). **PASS.**
2. **Gate tooth #2 — joint refit genuinely joint.** `winner=="player"` IS survive∧kill; one refit over both axes per the §6h contract. **PASS.**
3. **Gate tooth #3 — no production-code reach.** Diff is harness + doc + JSON only; zero production `.py`. The "throwaway harness + math-note §10 finalization, zero prod diff" claim verifies. Discipline #2 (smoke-gate is satisfied trivially: no prod code changed, so the 263-test PASS is a confirmation of un-regression, not a load-bearing gate). **PASS.**
4. **Gate tooth #4 — G-C emission held + no DB write.** Harness has no emission / DB-apply / proxy-lift path; the live channel read is in-process off `fr.player_death_element` (production typed channel, star-lord `d04edcc`), not a DB apply. §10.6 records `_DEFERRED_PROXY_BINS` NOT lifted, `_V2_17/18/19` un-applied. ADR-006 respected. **PASS.**
5. **Gate tooth #5 — 0.924 recorded, not acted on.** §10.5 records 0.924/0.926 as a named watch-item; no boss HP/TTK raise, no median firm-up bolted on; the firm-up is explicitly deferred to gandalf's separate encounter-model beat. Documentation only. **PASS.**
6. **Gate tooth #6 — seed hygiene #3 + math-before-code #1.** `BASE_SEED = 49_000_000` (disjoint from ≤46M / 47M 0a / 48M calibration), confirmed in both harness and output; §10 derivation precedes the guard results. **PASS.**

The 0.926 vs §9.5's 0.924 is a Δ+0.002 clean reproduction across an independent disjoint seed base — the band is stable, not a seed artifact. The G3 read of 1.50 (vs §9.4's 1.60) is two fresh rolls both ≪ the 2.0 envelope — the realized max wanders sub-2.0 across seeds, not a regression. Both are correctly characterized in §10.3/§10.5.

## Are the FINALIZED bands clean for Matt at the G-C close?

**YES.** The bands are finalized at the ruled anchor, every number verifies first-hand, the four guards hold, no semantic shift was introduced (Discipline #12 — finalization LOCKS the provisional band, does not re-interpret it), and nothing reaches production code, the DB, or content emission. Matt can take the §10 bands at the G-C close as-is.

## Is the WAVE complete pending only the Matt-gated items?

**YES.** All three build seams (rocket gear/monster-skills, gamora calibration spine, star-lord typed-telemetry) passed Gate-2 earlier in the wave; this finalized re-rate was the terminal validation artifact and it PASSES. What remains is exclusively Matt-gated and unchanged: (a) G-C content emission / `_DEFERRED_PROXY_BINS` lift; (b) the three additive DB-apply auths (`_V2_17` / `_V2_18` / `_V2_19`, ADR-006); (c) push of the whole held wave (ADR-006). None of these are in jack-ryan's or gamora's lane.

## Two minor INFO notes (non-blocking, no action required before the close)

- **INFO-1:** §10.3 G3 row text reads "(n=200)"; the harness `anti_tax_production_roll` is called with `n_kits=200 if args.full`. Consistent — recording only so the close reader knows the 1.50 is the full-run 200-kit roll, not the 60-kit smoke roll.
- **INFO-2:** the harness `build_population` / `anti_tax_production_roll` both re-seed kit generation from `seed_base=14001` (kit identity) independent of `BASE_SEED=49M` (fight RNG). This is correct — kit identity is held fixed across runs while the fight-RNG base is fresh-disjoint — but worth a one-line note for the record: seed hygiene #3 applies to the FIGHT base, not the kit-gen base, by design.

## Action

- [x] jack-ryan: **PASS** — FINALIZED bands are clean for Matt at the G-C close; wave complete pending only the Matt-gated emission / DB-apply / push items.
- [ ] knight-rider: report PASS to Matt; the G-C close is unblocked from a QA standpoint.
- [ ] Matt (G-C close, separate gate): take the §10 finalized bands; rule on (a) G-C content emission, (b) the three `_V2_17/18/19` DB-apply auths (ADR-006), (c) whole-wave push (ADR-006).

## References

- Commit/tag: `2b52700` / `gamora/v-typed-resistance-joint-rerate-1` (push held)
- Harness (verified line-by-line — anchor constants L52–55/177, joint metric L140, no DB/emission reach): `~/Games/reincarnated-engine/scripts/gamora_typed_resistance_joint_rerate_2026_06_21_FINALIZED.py`
- Raw output (every number verified against self-report): `~/Games/reincarnated-engine/src/reincarnated/simulation/output/typed-resistance-joint-rerate-2026-06-21-full-20260622_000411.json`
- Math note §10 FINALIZED (+ §9.6 SUPERSEDED, §9.7 RESOLVED): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-spine-and-calibration-2026-06-21.md`
- Checkpoint (SESSION 39): `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- Anchor ruling (the disposition honored): `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-boss-anchor-ruling.md`
- Coordinating MASTER (G-A..G-D): `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`
- Prior calibration Gate-2 (the provisional bands this finalizes; CONCERN-1/CONCERN-2 retired here): `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-06-21-typed-resistance-calibration-gate2.md`
