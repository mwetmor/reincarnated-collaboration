# Finding — 2026-06-21 — recal-wave defensive-axis MASTER dispatch (Gate-1 DESIGN-MODE)

**Reviewer:** jack-ryan
**Mode:** Gate-1 DESIGN-MODE (peer collaborator; pre-publish gate on a dispatch artifact — no BLOCK authority; verdict is ENDORSE / ENDORSE-WITH-CONCERNS / PUSH-BACK). ENDORSE is what releases knight-rider to publish the per-seam pickup files.
**Target:** `agentic_orchestration/dispatches/2026-06-21-recal-wave-defensive-axis-MASTER.md`
**Author:** knight-rider (orchestrator; sequencing lane)
**Principles applied:** Review #1 (math-before-code / design-before-build), #3 (cross-seam impact), #5 (cross-seam round-trip), #6 (Principle-6 round-trip gate); Disciplines #1 (math-before-code), #3 (seed hygiene), #11 (empirical inspection), #12 (semantic-shift care)

## Verdict

**ENDORSE.** The dispatch faithfully carries all nine ruled constraints, folds my CONCERN B1 into the gamora line as a ruled acceptance test with enough teeth that gamora cannot inherit the stale 2s-cadence guard result, makes the rocket geometry constraint hard, keeps the clear-shell re-derivation JOINT (no boss-only patch) with the coverage-weak concern carried, gets the dependency spine right (rocket content genuinely BLOCKS gamora calibration), carries the Principle-6 round-trip clause on all three cross-seam boundaries, and re-opens NO ruled design question. This is a sequencing artifact that stays cleanly in its lane. Releases for per-seam pickup-file publication.

---

## What I found

I checked the seven judgment-call items against the two Stage-1 gandalf docs (encounter-model ruling PART 3; threat-design spec §6) and my own threat-spec Gate-1 (CONCERN B1), reading the source text first-hand rather than taking the dispatch's framing.

1. **Nine constraints carried faithfully (lines 39-47).** Each of the nine reproduces the ruling's PART 3 (lines 111-127) in substance, none softened. One faithful tightening worth recording: constraint 5 in the dispatch (line 43) drops the ruling's "OR enabling coverage-pressure" alternative for restoring boss death and keeps only the spatial-skill route. This is correct, not a silent softening — the threat-spec §1 already established coverage cannot reach the endgame boss path (skill-less synthetic mobs, coverage off by construction), so the spatial-skill route is the only live restoration mechanism. The drop sharpens; it does not weaken.

2. **CONCERN B1 folded with teeth (line 96).** The gamora line carries B1 as a checkbox-titled RULED ACCEPTANCE TEST, names the exact stale fixture (`circle, dm=1.0, cooldown_seconds=2.0`), states the result "does NOT transfer," demands the re-run at the chosen production heavy-slow profile, adds the one-shot check (no single slam one-shots a glass-pole kit at band-center, per the PoE-rip boundary §2 forbids), and closes "it is your empirical burden, not an assumption." This is verbatim-faithful to my Gate-1 §B1 and the threat-spec §6 gamora bullet. gamora cannot read this and skip the re-run.

3. **Geometry constraint HARD (line 81).** Tagged "HARD — Gate-1 INFO #2," enumerates the four wired shapes `{point,circle,line,cone}`, names the six unwired (`burst/ring/nova/wave/chain/arc`), cites the `return []` fall-through at `spatial_engine.py:740-741`, and labels emitting an unwired shape a "damage-less threat (silent defect)" that would be net-new engine contradicting recompose-first. Correctly hard.

4. **Clear-shell JOINT re-derivation HARD + coverage-weak carried (line 98).** Marked "HARD CONSTRAINT 3," demands JOINT re-derivation of `PLAYER_ARMOR_FACTOR_VS_STANDARD` + `MOB_DAMAGE_SCALE`, forbids the boss-only patch with the inversion rationale (clear shells carry 3x the boss's per-hit), carries the Gate-2 coverage-is-a-weak-lever concern ("do NOT crank coverage"), routes clear-shell death via per-hit variance per constraint 4, and names boss-only death as the LOGGED fallback. Faithful to ruling §2.3 and my diagnostic Gate-2.

5. **Dependency spine correct (lines 60, 70).** rocket content prereq genuinely BLOCKS gamora calibration — "gamora cannot calibrate a death channel that does not exist." This is the load-bearing missed-layer finding from ruling §1.1 (skill-less synthetic mobs at `t4_sim_cycling.py:1082`), and the spine is drawn correctly: rocket G1/G2 first, gamora's calibration phase starts only once a fighting boss exists in the sim, star-lord additive telemetry concurrent.

6. **Principle-6 round-trip on all three lines.** rocket (line 89): build a synthetic boss with the emitted skill, step one tick, assert the cast branch fires and applies damage. gamora (line 110): a full-population fight producing a non-trivial death, assert survive-rate + death-cause fields land in the export packet. star-lord (line 120): explicit "YES on the Principle 6 gate — silence would be a Gate-1 BLOCK," round-trip a player-killing fight into the season JSON. All three boundaries change a fixture dict (lines 134-136); all three carry the clause + a MIGRATION.md requirement.

7. **No ruled design question re-opened.** Each per-seam Out-of-scope block (lines 87, 108, 122) fences the ruled questions back out (encounter SHAPE gandalf-ruled, the dodge/telegraph-reaction model is the named FUTURE fork, the schema lift is Matt-reserved), and line 145 names re-opening any ruled question (targets, gate-semantics, clear-shell scope, threat vocabulary, avoidance model) as a wave-level non-goal. The dispatch sequences the build; it does not re-rule. This is the one thing Matt explicitly forbade, and it is clean.

## Rationale

The dispatch clears Review Principles #1/#3/#5/#6 and is disciplined on #1/#3/#11/#12. The three non-negotiable guards (lines 51-53) restate constraints 6/3/8 verbatim as G-A/G-B/G-C and carry into every seam. Seed hygiene (Discipline #3) is correctly set disjoint at 47M+ (line 106), away from the consumed 700k-46M range. Math-before-code (Discipline #1) is required on both the rocket envelope (line 85) and the gamora TTD/TTK-vs-cadence derivation (line 102) before the sweep. The B1 fold is the single most important thing this gate had to verify carried forward, and it is carried at full strength with the stale fixture named explicitly. ENDORSE rather than ENDORSE-WITH-CONCERNS because there is no build-side caveat the dispatch failed to carry — every concern from the two Stage-1 Gate-1s and the diagnostic Gate-2 is present in the correct seam lane with the correct severity.

## Action

- [x] jack-ryan: Gate-1 DESIGN-MODE on the MASTER dispatch complete — verdict ENDORSE. All seven judgment-call items verified first-hand against the Stage-1 source.
- [ ] knight-rider: cleared to publish the per-seam pickup files (`2026-06-21-rocket-…`, `2026-06-21-gamora-…`, `2026-06-21-star-lord-…`) from the per-seam sections, on Matt go. Carry the per-seam sections verbatim — they are already gate-clean; do not paraphrase the B1 acceptance test or the geometry HARD constraint when splitting.
- [ ] jack-ryan (forward): Gate-2 DEV-MODE on each seam build in sequence per the dispatch's jack-ryan line (line 127) — rocket (seam soldered? cast branch fires?), gamora (heavy-slow guard RE-PASSES first-hand? clear-shell re-derivation JOINT not boss-only? trash strictly below boss? re-rate ONE joint refit?), star-lord (round-trip present?).
- [ ] Matt (no decision needed at this gate): this is a DESIGN gate on a dispatch artifact; no decisions-log entry, no production change. The "Matt go" referenced in the dispatch STATUS GATE (line 9) is the build-release authorization, separate from this Gate-1 ENDORSE.

## References

- Reviewed dispatch: `agentic_orchestration/dispatches/2026-06-21-recal-wave-defensive-axis-MASTER.md`
- Encounter-model ruling (nine constraints — PART 3): `agentic_orchestration/gandalf/notes/2026-06-21-defensive-axis-recal-encounter-model-ruling.md`
- Threat-design spec (§6 handoff; B1 acceptance test folded at §2/§6): `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md`
- My threat-spec Gate-1 (CONCERN B1 source): `agentic_orchestration/qa/findings/2026-06-21-threat-design-spec-gate1-design.md`
- Diagnostic Gate-2 (coverage-weak + joint-re-derivation carried concerns): `agentic_orchestration/qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`
- Calibration anchor (diagnostic): `reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`
- Engine — mob-cast death channel `spatial_gauntlet/spatial_engine.py:1933-2001`; geometry dispatch `:716-741` (`{point,circle,line,cone}` only, `return []` at `:740-741`); player-path variance `:1344`/`:1877` (NOT on mob channel); skill-less synthetic-mob gap `t4_sim_cycling.py:1082`
