# Finding — 2026-07-08 — s4-inverted-surface-acceptance-reframe

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: CLEAR-WITH-CONDITIONS)
**Target:** `agentic_orchestration/gandalf/notes/2026-07-08-s4-inverted-surface-acceptance-reframe.md`
**Developer:** gandalf (self-amending own §4 criterion)
**Mode:** DESIGN-MODE (governance gate, mandatory per the note's own §6.1 / §1)
**Principles applied:** Review Principle 4 (decisions-log as truth); Disciplines #11 (semantic-shift honesty), #12, #13 (inherited-uncalibrated drift); Goodhart-guard; ADR-002 (tiered approval — architectural re-point → ESCALATE lane preserved via Matt's prior A-ruling)

## Verdict

**CLEAR-WITH-CONDITIONS.** No load-bearing defect. The reframe is sound engineering: it does not move goalposts, it corrects the axis on which the pre-existing certification architecture was already measuring. Matt's A-ruling stands unopposed. Conditions below are capture/audit hygiene, not blocks.

## Scrutiny point 1 — Goodhart self-test (does the amendment actually pass?)

PASSES, genuinely — this is not moving-goalposts. Test:

- **Falsifiable independent of gate outcome?** Yes. The reframe rests on (a) genre design facts (scrutiny 3) and (b) tier-1 KPM spread (~2.4×, open_arena p10/med/p90 22.3/31.9/53.8) measured IN THE SAME RUN that failed §4. The reframe is not fitted to green a gate — it relocates the observable to an axis that was already alive in the failing run's own data.
- **Preserves §4's spirit (spread-not-rails)?** Yes, and this is the crux. §4's spirit is "differentials persist as spread, not rails." The amendment does NOT delete that requirement — it moves it to KPM space, where it is empirically satisfied, AND leaves a live residual falsifier: **if KPM spread ever collapses to a point mass, the amended criterion FAILS** (§4 q2/q4a). That residual is what distinguishes a legitimate re-point from a quiet deletion. A moving-goalpost amendment removes the falsifier; this one carries it forward onto a new axis. Confirmed.
- **Residual falsifier real?** Yes — three named (§4 q4): KPM collapse to noise; genre evidence of a real fixed-rung WR gradient; playtest evidence clear-speed reads as meaningless. All three are checkable and none are pre-satisfied by the reframe. This is the load-bearing element and it holds.

The one honest tension: the same run furnished both the FAIL and the reframe data. gandalf discloses this (§4 q1b) rather than hiding it. Because the KPM axis pre-existed the §4 criterion (it is the tier-1 gate, not a post-hoc construct), the disclosure is sufficient — the data was not manufactured to fit.

## Scrutiny point 2 — architectural claim "certification ALREADY runs on KPM bands" — CODE-VERIFIED

**VERIFIED IN CODE. The claim is accurate.** `src/reincarnated/simulation/gauntlet_sim.py`:

- `season_emit` (property, :966-974) → `gauntlet_pass(cohort)` (:963-964) → `family_certification_pass(cohort)` (:864). The emission/certification spine is real and reads as the note describes.
- The ship-gate per-shell verdict `_shell_result_passed` (:810-829) splits by shell type: **CLEAR shells (open_arena, chokepoint_corridor, magic_pack, elite_pack) gate on `tier_2_kpm` within `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]`** (:778-779, :815); **BOSS shells gate on `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]`** (:781-784, :824-829) — a survive-and-kill VIABILITY BIT, KPM band never consulted (:783-784).
- The "win-condition split" doctrine is codified at :192-204: clear rooms gate on a KPM band; boss rooms gate on survive-and-kill within the enrage timer, "DPS/TTK MEASURED but NEVER gating and NO over-performance ceiling."

**Consequence for the risk profile:** the reframe is confirmed a SMALL overlay-correction, not a re-architecture. Certification already discriminates on KPM bands and already treats survival as a viability screen (for boss shells). The §4 overlay — demanding tier-2 WR show a continuous gradient on clear shells — was the mis-point, and it was an overlay on top of an architecture that never keyed the ship gate off a continuous WR number. The amendment brings the acceptance criterion into line with what the code already does. This materially LOWERS the risk of the reframe: no new machinery, `_route_tier_1` predicate untouched (per :453). The step-4-bis "expected PASS on existing run data, no re-run" claim (note §6.3) is credible on this basis.

One precision note (INFO, not a defect): the code's existing survive-and-kill bit lives on BOSS shells; the reframe extends the "WR = validity screen" framing to CLEAR shells too. That is a framing generalization, not a contradiction — clear shells still gate on the KPM band as before; the reframe only rules that their tier-2 WR feeds a viability bit rather than a demanded gradient. No code conflict.

## Scrutiny point 3 — genre claims (D3 GRift / PoE mapping / single-rung WR near-binary)

DEFENSIBLE, not convenient. Judged on internal consistency + domain knowledge:

- **D3 Greater Rift farm-tier ~100% survival + rifts/hour discrimination:** accurate. Farm-tier GRifts (well below a build's push wall) are cleared at ~100% by viable builds; the discriminant is clear speed / rifts-per-hour, and Blizzard's leaderboard keys on highest-tier-cleared + time, never survival-at-fixed-tier. Correct design fact.
- **PoE white/yellow maps cleared by all builds + maps/hour economy:** accurate. On-tier mapping is a throughput economy; survival gradient appears only in pinnacle/uber content (the ladder's top rungs). Correct.
- **Single-rung WR near-binary for a competent population:** structurally sound. The general claim — continuous discrimination requires either a continuous on-rung observable (time/speed) OR a discrete ladder of rungs (wall depth), and a single fixed rung produces near-binary clear/can't-engage — is correct and is the genre-grounded reason WR-on-one-rung is the wrong observable.

These are load-bearing and they bear the load. Not cherry-picked; they are the standard ARPG endgame grammar.

## Scrutiny point 4 — silent-deletion check

NO FINDING QUIETLY DROPPED. Verified against note §5:

- **boss_with_adds non-viability** — STAYS FLAGGED (117/189 kits kill zero mobs; §5 + §6 parallel lane; carried as a FLAGGED scenario into R4 so it cannot silently gate Leg-C). Preserved.
- **Lethality-floor** — STAYS ROUTED (to Godot game-feel/playtest, explicitly NOT a certification gate). Preserved, correctly re-homed (routing it into certification would repeat §4's error in mirror image — sound).
- **4-mid-cell count** — STAYS ON RECORD (§4 q3). Preserved.
- **magic_pack band** — FLAGGED FOR AUDIT (band (18.61,100.00) predates F2 re-pop, never got step-5 density-anchored re-derivation; §5). Preserved and correctly queued.
- **G2 bimodality** — RETRACTED IN PART (amplitude 0.000/1.000 rails = instrument artifact; DIRECTION — corridors favor melee, open favors kiting — survives). This is a disclosed partial retraction under Discipline #11/#12, not a deletion. gandalf applies his own "pattern=signal, amplitude=artifact" formula to his own prior read. Legitimate.

The retraction is honest semantic-shift accounting, not goalpost-hiding.

## Conditions (hygiene, non-blocking)

1. **magic_pack band audit is load-bearing for the "no finding dropped" claim.** The reframe leans on tier-1 KPM as THE measurement; a stale magic_pack ceiling ((18.61,100.00), pre-F2, un-re-derived) means the measurement instrument itself is partially uncalibrated on that shell. Condition: the step-5 density-anchored re-derivation for magic_pack (note §6.2) MUST land before step-4-bis is treated as a clean PASS on that shell — otherwise the validity screen inherits an uncalibrated gate. Discipline #13.
2. **boss_with_adds fork stays open, not resolved.** The note's own sub-question — is KPM even the right observable for boss rooms (TTK+deaths, not KPM)? — is correctly left to gamora's data pull. Condition: this must not be silently closed by the reframe's "tier-1 KPM = THE measurement" framing; boss shells already gate on survive-and-kill (code :824-829), so the reframe's KPM-primacy statement applies to CLEAR shells. Recommend the eventual finding-record note this explicitly to avoid a future reader over-reading "KPM = the measurement" as universal.

## Decisions-log capture advice (I am sole authoring authority)

**This reframe warrants decisions-log capture, and the cleanest home is a SEPARATE entry — do not fold it into the pending §6 proposal.** Rationale:

- The pending proposal (`qa/pending/2026-07-08-kr-decisions-log-proposal-s6-spatial-difficulty-ruling.md`) documents the **Option-A un-stack + serial-engagement** ruling — a difficulty-instrument change. That is a distinct decision from the **acceptance-criterion re-point** (what the certification gate MEASURES: tier-1 KPM = discrimination, tier-2 WR = validity bit, WR-gradient = post-demo ladder). Folding two architectural rulings into one entry would blur the supersession chain and make the §4-criterion history harder to trace.
- The reframe entry's Related field should cross-link the §6 un-stack entry (they are sequential: un-stack removed the lockout → inverted surface → this re-point interprets it), the code spine (`gauntlet_sim.py:192-204, :810-829, :864, :966-974`), and gandalf's note. It should record the residual falsifier (KPM point-mass collapse → criterion FAILS) as part of the Decision so the anti-Goodrart guard is captured, not just the outcome.
- Both entries can be authored in the same batch (alongside the R3a Gate-2 math-note reviews), but as two entries.

I am NOT authoring either entry in this pass (per the dispatch). Advice only. When authored: the §6 un-stack entry is ready to go as drafted (minor: fix a typo target if any); the reframe entry I will draft fresh keyed to Matt's A-ruling (2026-07-08).

## Action
- [ ] gamora: land step-5 density-anchored magic_pack band re-derivation before step-4-bis is scored clean on that shell (Condition 1).
- [ ] gandalf/gamora: keep the boss_with_adds observable-fork open; note KPM-primacy applies to clear shells (Condition 2).
- [ ] jack-ryan (me, next pass): author TWO decisions-log entries (§6 un-stack + this reframe), same batch, with cross-links + residual-falsifier captured.
- [ ] Matt: no new decision needed — A-ruling stands; this gate is CLEAR-WITH-CONDITIONS, not a BLOCK, so no re-litigation.

## References
- `agentic_orchestration/gandalf/notes/2026-07-08-s4-inverted-surface-acceptance-reframe.md`
- `agentic_orchestration/qa/pending/2026-07-08-kr-decisions-log-proposal-s6-spatial-difficulty-ruling.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — :192-204 (win-condition split), :211-214 (_BOSS_SHELL_GATE_TYPES), :405-453 (band architecture + R3a step-5 re-derivation), :810-829 (_shell_result_passed), :864 (family_certification_pass), :966-974 (season_emit)
