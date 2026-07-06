# Variation Pilot — run state (2026-07-06)

> Authored by knight-rider at Leg-3 launch. Records Matt's FORK RULING (Option 1 — fire the inert pilot now) and its four riders, so Leg-4 analysis and batch-2 sequencing honor them. Live ledger.

## ⇒⇒ LEG-4 COMPLETE — pilot chain ready to CLOSE (gamora `dddd569` / collab `f414f64`)

Merged gamora unit delivered (analysis+report only, zero compute): calibration note finalized + Leg-4 attribution report. Artifacts: `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (finalized) + `simulation/notes/leg4-attribution-report-2026-07-06.md` (new).

- **C2 plain-caster floor PLACED (measurement output, not a pick):** `bar_lo` = **9.90 KPM (open_arena) / 11.65 KPM (chokepoint)**. Current chassis = 0.0 on both → gap == full floor (hard solo timeout, not near-miss). **Structural nuance:** the full timeout-to-floor jump corroborates the Session-48 autopsy's PREDOMINANTLY-STRUCTURAL read — a band re-tune alone may be insufficient; the **gen-path + resource-economy dimension is named for batch-2**, not just a band number.
- **magic_pack 600.0 = METRIC-DOMAIN ARTIFACT** (not real DPS, not a min=max clamp): `observed_kpm = kills/(duration_s/60)`, `duration_s` quantized to `TICK_SIZE=0.1s`; sub-tick pack clear reads `1/(0.1/60)=600`. Engine already routes sub-`T_min` clears on COMPLETION (`CLEAR_SHELL_DOMAIN_TMIN_S=1.0`; `t4_sim_cycling.py:108-113,273-277,720`). Reported as `≥`-ceiling. **elite_pack 426.9 (spread 163.6–450.0, n=124) = pack-overperformance signal of record.**
- **Leg-4 verdict: mechanism thesis CONFIRMED** (40/81 season_emit; melee chain-variants 15/15 eligible-encounters-passed; G4 knob z≈−1.0 in-range at 4/25) + chassis finding = empirical basis for C2.
- Per-cohort-bucket-key spec line handed forward to gandalf's batch-2 spec (report §6).

**Closure gate:** light jack-ryan read on the two load-bearing derivations (C2 floor + magic_pack artifact verdict) before they anchor batch-2. Pilot chain CLOSES on that read's return.

## ⇒ C2 CHASSIS RULING (Matt 2026-07-06, relayed via gandalf) + merged fire-order

**C2 — TWO CHASSIS BANDS keyed on the existing proxy-share knob** (0.250000 exact, no new mechanism). C1 (one-band) and C3 (summons-everywhere) REJECTED.
- **Plain-caster band** (proxy ~0): solo single-target floor — MUST clear open_arena AND chokepoint solo. Current 0.0 KPM = gap-to-close, not a design position. **Floor placement = OUTPUT of gamora's calibration note.**
- **Summoner band** (proxy ≥0.25): solo timeout ACCEPTABLE, proxy DPS mandatory (already ruled 2026-07-02). Summoner-band magnitudes defer to batch-2 measured data.

**Fork resolved:** my (a) + report-first alternative MERGE into ONE gamora unit (dispatch `2026-07-06-gamora-calibration-finalize-leg4-report.md`, FIRED). My (b) sharpens: **no standalone calibrated re-emit/re-fight EVER — the plain-caster band re-tune becomes batch-2 config; the re-emit/re-fight IS batch-2. One batch, one fire, after the gen-path chain closes.**

**Sequence after the gamora unit returns (NOT now):** Leg-4 report lands → pilot chain CLOSED → gandalf authors batch-2 build spec (Option-1 scope + C2 band config + measured floor + tiered-shells lever + per-cohort bucket keys + variation build, ≥100/cell × 18 cells) → ARCHITECT pass gates run authorization → KR dispatches batch-2 → derivation chain (elrond consult → clustering → Matt cut-ratification).

**Paperwork:** serial-emission tracker ✓ RULED C2 (gandalf, done); decisions-log C2 registration batches with the 2026-07-06 ruling set on jack-ryan's next pass; gamora unit = analysis+report only → light jack-ryan read.

## Launch record

- **Fired:** 2026-07-06 ~14:54 local, detached (`nohup`, PID 11337) from persistent KR session per Discipline #19 (NOT a sub-agent).
- **Driver:** `star-lord/v-pilot-leg3-driver-1` (engine `2ac1ee6`), `reincarnated.export.variation_pilot_driver`.
- **Log:** `reincarnated-engine/src/reincarnated/output/variation_pilot_run.log`.
- **Checkpoints:** generation → `output/variation_pilot_generation_checkpoint.json`; gauntlet → `simulation/output/pilot/…`. Recovery: `--recover-from-canonical <path>`.
- **Completion sentinel:** `VARIATION PILOT COMPLETE`. Registry: `emission_runs WHERE season_id LIKE 'variation-pilot%'`.
- **Expected wall:** ~35–40 min. **Cells:** one physical-melee (full variation), one caster (G4 proxy knob live ~0.25).
- **PROXIES INERT BY DESIGN this run:** emitted proxy magnitudes = `None` → `_spawn_one_ally` resolves `None or 0.0 = 0.0` → `_is_fighting_decl=False`. Summoned allies do not fight. This is expected and is the reason for the four riders below.

## Matt's four riders (FORK RULING — binding on Leg 4 + batch 2)

### Rider 1 — Roster trigger DISARMED for this run, BOTH directions
- **No summoner seat fills from an inert-proxy fight.** A fail-artifact (~0 survivors) is NOT "summoners fail." A pass-artifact is WORSE: a proxy-dominant kit that clears on its non-summon remainder is NOT a validated summoner — seating it ships the F1 hazard as a demo kit whose skeletons stand there doing nothing.
- **Summoner seats fill ONLY from a live-proxy fight** (post-calibration re-fight).
- **Plain-caster survivors (~75) KEEP caster-seat candidacy** — their read is clean (no proxy dependence).

### Rider 2 — Leg-4 attribution PRE-REGISTERED (before data lands)
- Proxy-dominant results report as **"solo-baseline, summons inert by design"** — NEVER as summoner viability, in either direction.
- Emitted-vs-curated SIM comparison is DEFERRED to the re-fight.
- Take the FREE STATIC version now: emitted proxy-dominant tree shape / skill composition / offer-table vs the 2 curated summoners' structure — **no sim** — feeds calibration.

### Rider 3 — Calibration fires as its own gated task, IN PARALLEL (LAUNCHED)
- gamora math-note on proxy-magnitude architecture. Frame = **marginal value** (required summon contribution = clear-shell bar − solo baseline; baseline arrives from this run within the hour). Empirical anchors = the 2 certified curated summoners' known-good magnitudes (WR 1.0 both shells) scaled to chassis coordinates.
- **Gate-1 critique-pair on the note** (design eyes REQUIRED: summon strength is class-fantasy surface, not just a balance constant).
- Then calibrated re-emit + re-fight of the **CASTER CELL ONLY** (~20 min).
- **Status:** gamora math-note dispatched as background task at Leg-3 launch. Gate-1 (jack-ryan + gandalf) fires when note lands.

### Rider 4 — Batch-2 gains a NAMED GATE
- **Gates-on:** `proxy-magnitude-calibration` · `calibrated-caster-re-fight`.
- Leg-4 go/no-go is a **CONDITIONAL go** (all learnings EXCEPT summoner survival); the re-fight finalizes it.
- Firing batch-2 before calibration would reproduce inert summons at 18-cell scale. DO NOT fire batch-2 full-spectrum until both gate items clear.
- **TIERED-SHELLS LEVER (Matt 2026-07-06, do-not-lose):** the pruned pilot ran the FULL 18-encounter gauntlet on 50 kits (118,350 fights / 903s) instead of just the 2 cells' shells. This scoping inefficiency is NOT a triage fix — it is the **tiered-shells lever, already on the batch-2 books**. Batch-2 must scope the gauntlet to the relevant shells per cell rather than the full 18-encounter sweep. Preserved here so it cannot fall through.

## Run 2 (pruned, 25/cell) — join-contract defect + measurement-report decoupling (2026-07-06)

**What happened:** relaunched at `--n-per-cell 25` (Matt pruned 200→50). Generation OK (25 melee 0-proxy + 25 caster {none:21, light:4}, 4/25 proxy-dominant). Gauntlet COMPLETED (`GAUNTLET_SIM_PASS=True`, 118,350 fights, 903s) and wrote results to `simulation/output/pilot/cycle-13-gauntlet-sim-results-2026-05-27.json` (3.4 MB, 81 configs, **40 season_emit=True incl. melee**). But the pilot driver reported `0/50 in-band → 0 survivors → empty bundle → HALT-LOUD (Discipline #8)`.

**Root cause (leading hypothesis, star-lord to confirm):** the gauntlet keys results by `legendary_id` (e.g. `..._t4_chain_1`); the pilot driver joins survivors back by `character_id` (e.g. `..._s0`). Namespace mismatch → 0 join hits despite 40 emit=True. NOT a balance failure; the kits pass the gate.

**Matt's triage ruling (2026-07-06):**
1. **Fix the join via the PUBLISHED CONTRACT — not an ad-hoc rekey.** Locate the published gauntlet-results↔kit-identity contract (gamora is authority on what the gauntlet emits) and conform the driver to it.
2. **Measurement-report path — uncouple PERMANENTLY.** A measurement pilot's deliverable is a REPORT, not a demo bundle. Requiring monsters/gear validity to measure fights couples unrelated contracts. Uncouple it permanently; **SPRT-calibration runs will need the same path.** (Matt part-owns this scope error from the dispatch's demo-bundle inheritance.)
3. **Re-extract, DON'T re-fight.** Leg-4 attribution + the solo-caster baseline come off the on-disk results file. Dependency-inversion payoff: **gamora's proxy-magnitude calibration prerequisite exists on disk even though the report layer broke — calibration queues the moment extraction lands.**
4. Full-18-shell scoping → tiered-shells lever (see Rider 4 above); not a triage fix.

### Triage OUTCOME (star-lord `2a9c31b`, tag `star-lord/v-pilot-join-contract-measurement-report-1`)

**KR's join hypothesis was DISCONFIRMED — and that is the win.** star-lord confirmed against the published contract that the join logic is STRUCTURALLY CORRECT: the driver already keys by `legendary_id` via `_build_legendary_config` (`variation_pilot_driver.py:661`), matching the gauntlet emit-key (`gauntlet_sim.py:1437` `legendary_id = f"{kit.bc_cell_id}_{chain_id}"`). The published contract lives in `AGENT_STATE.md §W3-Batch-1-Post-Run-Defect-Record`, `MIGRATION.md §v1.88`, and `season_generation_pipeline.py:1437,1385`. **The "confirm via published contract before fixing" instruction prevented an ad-hoc rekey of code that was never broken.**

**The ACTUAL defect was only the coupling (Item 2), now fixed:** `one_realm_bundle_assembler.validate_bundle()` fired demo constraints (no kits / no monsters) on a measurement run where 0 survivors is VALID DATA (log 8106-8111). New first-class module `export/measurement_report_writer.py` (own module, not a flag — SPRT-calibration imports it directly; MIGRATION §v2.10). Round-trip smoke ALL PASS.

**The 0 survivors is REAL, not a join artifact — and it is a load-bearing balance finding:**

Solo-caster baseline (report at `output/variation_pilot_measurement_report.json`):
- `open_arena` / `chokepoint_corridor` (Balanced, Hybrid): **KPM = 0.0** — the caster TIMES OUT solo. Marginal-value → summon must carry the FULL clear (required contribution = 9.90 / 11.65).
- `magic_pack` / `elite_pack`: **KPM = 600.0 / 426.9** — caster OVER-performs. Summon must add NO DPS (survivability/positioning only — matches jack-ryan Gate-1 condition #3).

**⇒ The caster chassis is itself wildly out-of-band solo** (times out on single-target/corridor, over-clears on packs). This is arguably a bigger finding than the summon calibration: calibrating a summon to rescue an out-of-band chassis may be solving the wrong problem. **Belongs to Leg-4 analysis / a Matt read BEFORE spending on calibrated re-emit + re-fight** (band re-tuning was explicitly out-of-scope pre-pilot-evidence — this IS the evidence).

## Process lesson (Matt-flagged — for critique-pair run-boundary checklist)
- Holding the launch was CORRECT — the inert-proxy finding was a **premise-change to Leg-4 outputs, not a seam call**.
- rocket's `magnitudes=None` is a **legitimate layer-handoff** (named owner, named task), correctly caught at shell-prep.
- BUT the Gate-1 pass should have PRICED its Leg-4 consequence. **New checklist question: "does the emitted thing FIGHT?" joins the run-boundary checklist.** Route to jack-ryan + gandalf for the critique-pair operating-procedure / engineering-disciplines record.

## Leg-4 deliverables (pending pilot completion)
1. Solo caster baseline (KPM) → feeds gamora calibration note's open slot.
2. Melee-cell variation report (distinct t4/geometry/chains/role-split/resource — mechanics not palette per Ruling 2).
3. Caster-cell variation report + static emitted-vs-curated summoner structural comparison (Rider 2).
4. Conditional go/no-go framed per Rider 4.

## Calibration-note Gate-1 disposition (2026-07-06) — RATIFY-WITH-CONDITIONS

Critique-pair on `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (gamora `066ba37`). Both critics RATIFY-WITH-CONDITIONS. Math verified sound; NO Matt decision at this Gate; NO BLOCK; no MIGRATION.md (decl shape unchanged, ADR-004 untriggered).

- **jack-ryan** (technical, `cb040b0`): every load-bearing number verified first-hand (KPM bands `gauntlet_sim.py:393-398`; WR-1.0 anchors + gravecaller quote `proxy-fight-calibration:302-304`; `None or 0.0` coalesce + `damage_modifier=1.0` default `spatial_engine.py:1741-1742,1773`; `SPATIAL_DAMAGE_SCALE=0.6` `:326`).
- **gandalf** (design, per Matt's design-eyes requirement): endorses marginal-value frame ("the only frame that refuses to ship a lie"); proxy-dominant ceiling is a *design gate*, not a balance clamp.

**The crux resolved — ranged/melee caveat does NOT block the re-fight.** jack-ryan: the re-fight runs CLEAR shells (packs), not boss shells; gravecaller's WR 0.0 was a BOSS-specific nav evaporate; on a dense pack field the nearest-enemy nav gap is far less binding. So the pack re-fight IS the honest empirical test of whether the melee-derived anchor transfers to a ranged proxy — **the primitive question is answered BY the fight, not before it.** The ranged/melee tier split, if needed, is a rocket-seam generation primitive (ADR-002) escalated to knight-rider WITH re-fight evidence — not a sim patch, not masked by a magnitude bump (gandalf concurs, structural).

**Binding conditions on the calibrated re-emit + caster re-fight:**
1. **(jack-ryan #1, non-optional)** Engagement gate BEFORE reading KPM — a nav evaporate must not be misread as a magnitude shortfall. **This operationalizes Matt's "does the emitted thing FIGHT?" run-boundary check.**
2. **(jack-ryan #2)** State the 0.6-vs-1.0 `damage_modifier` regime as an explicit harness parameter (silent 1.67× otherwise).
3. **(jack-ryan #3)** No DPS lever on above-ceiling pack shells — survivability only.
4. **(jack-ryan #4 + gandalf #2)** Ranged-primitive escalation to knight-rider carries re-fight evidence; ranged-nav-evaporate is STRUCTURAL — do NOT mask with magnitude.
5. **(gandalf #1)** Grade `[0.15, ~0.30)` f_army share as "balance-passing / fantasy-marginal" on the read — no silent PASS. Ranged floor likely higher than melee floor.
6. **(gandalf #3, emission-time)** When rocket emits varied summoners, summons must READ as the summoner's own (thematic coherence with element/name/weapon), not generic proxies.

**Sequencing:** pilot solo baseline fills gamora's open slot → rocket calibrated re-emit (chassis-coordinate magnitudes + engagement-gate hook) → gamora caster-cell-only re-fight (~20 min) under conditions 1-5 → ranged-primitive question surfaces to KR/Matt only IF the pack re-fight shows the melee anchor doesn't transfer.
