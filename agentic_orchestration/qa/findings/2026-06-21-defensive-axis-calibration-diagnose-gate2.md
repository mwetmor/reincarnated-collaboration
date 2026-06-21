# Finding — 2026-06-21 — defensive-axis-calibration-diagnose

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no production-gate change to BLOCK; methodology + knob-set soundness reviewed in full)
**Target:** `gamora/v-defensive-axis-calibration-diagnose-1` (commit `fbbeacf`, LOCAL, not pushed)
**Developer:** gamora (simulation seam)
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log/provenance as truth); Disciplines #1, #3, #11, #12, #24

## Verdict

**PASS-WITH-INFO.** This is a DIAGNOSE-ONLY note with a confirmed 0-line production diff; the tag commit touches only the throwaway harness, the math note, and the raw JSON (4337 insertions, none in production paths). My authority is over methodology and the soundness of the load-bearing calibration claims. I verified each first-hand against the engine code and reproduced the arithmetic independently. The mechanism correction, the homogenization guard, the tier_1-bypass, and the recommended knob-set all survive scrutiny. Two reproducibility/provenance INFO items and two real constraints the future recalibration wave must carry.

## What I found

**1. The mechanism correction HOLDS first-hand (highest-priority claim, verified).** The death channel at `spatial_engine.py:1950-1955` is exactly `raw = dm × 300 × MOB_DAMAGE_SCALE`, `dmg = raw × (1 − armor_factor)`, `hp ≤ 0 → is_alive = False` — matching the note's formula verbatim. I reproduced the inversion arithmetic independently: at scale=0.40, boss_armor driven to 0.10 (player takes 90%), 3 mobs deal ~162 DPS → glass 10k-HP TTD = **61.7s** (note: ~62s ✓), but the kit kills the boss in ~39.7s and out-races the channel. **Boss-armor at its most extreme value still cannot kill at the production mob-scale.** The commission's premise ("boss-armor primary") and gandalf §1 ("boss-armor dominant") are corrected in MAGNITUDE: boss-armor only grades once `MOB_DAMAGE_SCALE` is large enough to bring the channel inside the TTK window. At scale=4.0 I reproduced the §4.4 death thresholds — glass (dm=1.0, TTK≈37s) flips from safe into the death band exactly where TTD crosses below TTK (~ba 0.80→0.74), matching the measured table. The correction is empirically and arithmetically sound.

**2. tier_1-bypass is GENUINE, elite_pack measurement is REAL (verified).** `run_spatial_fight` (`spatial_engine.py:2516`) contains zero `tier_1` references — the Pareto admission gate lives entirely upstream of this entry point, so driving it directly bypasses the gate by construction, not by artifact. The committed JSON confirms all six shells in Q6 including elite_pack (survival 1.000, a_dead=0, b_dead=16, ttk=4.5s, n=16) — a genuine fight outcome, closing gandalf §10's unmeasured/all-REJECT gap. The winner→termination mapping (`player`→b_dead=survive+kill, `monster`→a_dead=death) correctly mirrors the engine loss-on-player-dead branches.

**3. The homogenization guard HOLDS (the load-bearing result, verified).** The death channel is independent of glass OFFENSE (the mob deals the damage), so at fixed HP+armor (ba=0.78, scale=4.0) TTD is fixed (~25.3s) and survival is purely a TTK-vs-TTD race driven by the swept offense lever — a clean single-parameter isolation (Discipline #24). The supplemental JSON `guard_scale4` block matches §4.5 cell-for-cell (dm≤0.8 → 24/24 dead; dm=1.0 → 0.917; dm≥1.6 → 1.000). Same HP, same armor: slow dies, fast survives-by-killing. Offense partially substitutes for defense; combined with the bruiser surviving-by-enduring at the same knob-set, the axis is genuinely 2D with no mandatory armor floor. Conclusion follows from the isolation.

**4. The recommended knob-set produces the claimed spread (verified).** The supplemental `death_axis_scale4` block reproduces §4.4: at scale=4.0, glass lands 0.75 (ba=0.74) → 0.92 (ba=0.76) inside/at the 0.6–0.8 target; bruiser pinned 1.000 throughout. Headroom (§4.6) ~0.60 armor between glass-death-onset (~0.80) and bruiser-death-onset (<0.20), tracking the 3.3× HP ratio. The two honest flags are REAL constraints (see Action).

**5. Discipline compliance (verified).** Math-note-first with falsifiable predictions pre-registered before runs (#1 ✓). Seed hygiene: BASE_SEED 50,000,021, disjoint from this run's prior 41M–46M bases (#3 ✓). First-hand provenance Q5 — both `PLAYER_ARMOR_FACTOR_VS_BOSS=0.95` and `MOB_DAMAGE_SCALE=0.40` confirmed pre-defect-fix and never re-validated against the 240s/binary model; I confirmed the `:1950` formula and `:2516` entry-point independently (#11 ✓). Mechanism correction surfaced and logged mid-run (#12 ✓). 0-line production diff confirmed.

## Rationale

The note clears Review Principles #1/#2/#4 and Disciplines #1/#3/#11/#12/#24. Every load-bearing claim was re-derived first-hand from the engine source and the raw JSON, not taken on the note's framing. The arithmetic, the channel-independence argument behind the guard, and the bypass are all sound. PASS-WITH-INFO rather than clean PASS because of two provenance/reproducibility gaps (below) that do not affect the conclusions but should be corrected before this note is cited as the recalibration anchor.

## Action

- [x] jack-ryan: Gate-2 methodology review complete — verdict PASS-WITH-INFO.
- [ ] gamora (INFO, reproducibility): The committed harness script (`scripts/...SPIKE_THROWAWAY_.py` line 161) writes only four output keys; the JSON contains a fifth `supplemental` key (`death_axis_scale4`, `coverage_clear_death`, `guard_scale4`) holding the scale=4.0 results that the note's HEADLINE findings (§4.4/§4.5/§4.6) depend on. The committed script does NOT reproduce those results — they came from a follow-on run not captured in the committed harness. The DATA is genuine and the note's tables transcribe it faithfully, but a reader re-running the committed script gets only the scale={0.4,0.6} grid. If this note becomes the recalibration anchor, fold the supplemental sweep back into the committed harness so it is reproducible end-to-end.
- [ ] gamora (INFO, provenance line): The commit message and note say "Raw JSON local-only (output/ git-ignored)"; the JSON is in fact tracked and committed (it is not matched by the engine `.gitignore`, which only excludes `output/**/fights.jsonl` and `gear_pool_staged.json`). Harmless, but the provenance line is inaccurate — correct or drop it.
- [ ] Future recalibration wave (CONSTRAINT, carry forward): The two honest flags are real and must be carried — (a) **coverage-pressure is a weak clear-shell death lever for fast AOE kits** (swept cov_per_mob 8→150, glass+bruiser survive 1.000 at every value because a circle-AOE kit covers+clears the swarm before bleed accrues); clear-shell death needs its own mechanism review, coverage alone won't punish a fast AOE glass on trash. (b) **The instrument-wide recal must JOINTLY re-derive `PLAYER_ARMOR_FACTOR_VS_STANDARD` + `MOB_DAMAGE_SCALE` for clear shells alongside the boss knobs**, NOT bolt a boss-only patch — otherwise trash (15% taken) becomes safer than the boss in OUTCOME, inverting gandalf §10's danger-asymmetry. The note recommends only the boss-path knob-set; the clear-shell half is explicitly the wave's remaining work.
- [ ] Matt (no decision needed now): This is DIAGNOSE-ONLY; no decisions-log entry and no production change until the recalibration is authorized as its own Matt-scoped wave. The knob-set (`MOB_DAMAGE_SCALE=4.0`, `PLAYER_ARMOR_FACTOR_VS_BOSS≈0.76`, standard-armor 0.85 held, coverage off) is the validated ANCHOR that wave starts from.

## INFO — minor observations for the record (non-blocking)

- The glass death-band is sharp (0.82 safe → 0.72 all-dead over ~0.10 armor); the note's §4.7 attributes this to flat mob hits (no per-hit variance) + single HP fixture, and predicts a real population HP-spread softens it. Sound, and honestly flagged.
- The guard sweep's dm=1.0 row (ttk 39.7s, survives 0.917) vs dm=1.3 (ttk 43.7s — SLOWER — survives only 0.833) is non-monotonic in offense near the knife-edge. This is a genuine measured self-heal/kill-ramp nonlinearity at the boundary, not an error; the §4.7 caveat covers it. The structural claim (offense buys survival) holds across the full sweep.
- Single-kit fixture (one season-001 faithful kit, HP via stat-injection, offense via damage_modifier). Direction + magnitude are robust (analytic TTD/TTK matches measured thresholds); a full-population sweep is correctly named as the recalibration-wave validation, not this diagnostic's burden.

## References

- Reviewed note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`
- Harness: `~/Games/reincarnated-engine/scripts/gamora_defensive_axis_calibration_diagnose_2026_06_21_SPIKE_THROWAWAY_.py`
- Raw: `~/Games/reincarnated-engine/src/reincarnated/simulation/output/defensive-axis-calibration-diagnose-2026-06-21.json`
- Engine death channel: `spatial_engine.py:1950-1955`; entry point `:2516`; loss-on-player-dead `:2095/:2112/:2124`
- Design-half converged-with: `agentic_orchestration/gandalf/notes/2026-06-21-monster-to-player-calibration-design-half.md` (§1, §10, §11.2, §11.3)
