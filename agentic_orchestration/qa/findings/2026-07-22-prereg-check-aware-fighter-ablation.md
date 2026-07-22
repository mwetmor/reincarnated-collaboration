# Finding — 2026-07-22 — Aware-Fighter Ablation Gate Pre-Registration Check

**Reviewer:** jack-ryan (DEV-MODE, chartered PRE-REGISTRATION CHECK gating the aware-fighter ablation run)
**Verdict:** **PASS-WITH-CONCERNS**
**Target:** prereg sheet `2026-07-22-aware-fighter-ablation-prereg.md` (PINNED, commit `dee9f040`; L-27 all four pins ruled)
**Author under check:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat)
**Gate engine hash:** `2f43045` (verified `git rev-parse` at check = `2f43045`; my own Gate-2 delta PASS `3f26b00b`)
**Developer (execution):** named-gamora (charter to follow freeze)
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #4 (decisions/rulings-log as truth), #5 (severity); Disciplines #1, #2, #3, #11, #12, #18; run rulings L-21→L-27; ADR-006 (read-only external)
**Concerns:** C1 (WARN), C2 (WARN), C3 (INFO), C4 (INFO), C5 (INFO)

---

## Verdict rationale

I re-derived every load-bearing number first-hand from the sealed working-tree battery (`…/gamora/notes/2026-07-22-aware-fighter-bw11-battery-after-full.json`) rather than accepting the conductor's preview, and re-read the two calibration sources, the engine at the frozen hash, and the harness. Every battery-preview claim reproduced EXACTLY: 29/32 baseline + 21/32 encounter cells seed-deterministic on `player_damage_total`; encounter aggregate sample-CV 4.70% dealt / 1.30% time-proxy; baseline time-proxy 0.53%. The D2=10% pin sits inside the 5–15% calibrated window; k=2 maps to the rliable 95%-CI-non-overlap standard; both are grounded in the legolas consult + the Black & Darken full-PDF addendum. The margin definition, D3 estimator (aggregate-per-seed → sample-SD, honest 3 df), and degenerate guard are internally consistent and computable. The no-confound guarantee is real IN CODE: both target-choice sites route through one seam that differs between arms by the `policy_config` value ALONE. The instrument is directionally correct and the bar is the ruled bar. Two WARNs obligate a one-line pin each before freeze — both are precedence/verifiability edges the sheet under-specifies, not defects in the bar (no bar-parameter moves, per the W3′ folding convention). Three INFOs travel into the result read. No concern rises to BLOCK.

---

## Dimension 1 — Internal consistency

**Finding: WELL-FORMED. Two under-specified edges (C1, C2); everything else complete.**

- **Margin definition** (§5): `M_rel = (Ī_blind − Ī_aware) / Ī_blind`, Ī = mean per-fight intake across the 32-cell × 4-seed ENCOUNTER arm. Well-formed and computable — `Ī` is a plain mean over a materialized set; sign convention (positive = aware takes less) is stated. The PRIMARY metric `player_damage_taken` is a real per-fight scalar on `SpatialFightResult` at the frozen hash (engine line 4987, fed from `self.player.damage_taken`; enemy-inflicted only, LC HP-cost payments excluded — matches §4's "self-inflicted LC HP costs excluded" verbatim). The runner extension (§7 pin 7) is therefore well-defined and NOT a schema change: the field already exists; the runner reads it + trace-length. §7 pin 8 ("no telemetry-schema changes") holds.
- **D3 estimator** (§5): seed-to-seed SD of the blind encounter-arm aggregate mean intake. Computable from the sealed blind arm — I re-derived its SHAPE on the dealt stand-in channel (intake unavailable pre-run): 4 seeds → aggregate per seed → `statistics.stdev` (n−1, 3 df). This matches the pinned "honest 3 df" language exactly. The predicate `(Ī_blind − Ī_aware) ≥ 2 × SD_seed` is a scalar comparison — mechanical.
- **Degenerate guard** (§5): SD=0 ⇒ D3 auto-satisfies, D2 + clear-guard bind. Sound: a fully-deterministic blind arm makes the noise floor vacuous by construction (nothing to clear), so ceding D3 to D2 is the correct failure-safe. On my stand-in re-derivation SD_seed = 133.4 ≠ 0, so D3 is a LIVE floor at realistic noise, not auto-satisfied — the guard is conditional, not a blanket escape.
- **PASS/FAIL/PARTIAL semantics** (§6): PASS = D2 ∧ D3 ∧ clear-clean ∧ specificity-clean; FAIL = honorable fallback (not-PASS, not-PARTIAL); PARTIAL = clear-trip ∨ specificity-trip. Complete over the outcome space. **Mutual exclusivity has one unstated precedence edge → C1.**
- **Honorable fallback** (§6): pre-registered, no relitigating, BLIND stays shipped, geometry reads archive as L-26 boss-garnish candidates, zero rip-out (config-only ablation property). No leg-dropping — a FAIL bank the seam + metric + harness and closes the question decisively (the full-6-set design makes a null unambiguous, per §3 rationale). This is the W3′ §4-degeneracy analog: the fallback tightens/closes, never launders.

→ **C1 (WARN): pin the PARTIAL-over-FAIL precedence as an explicit rule.** A run can simultaneously trip the clear-guard (→ PARTIAL) AND miss D2/D3 (→ FAIL-shaped). §4 says a clear-guard mismatch makes the verdict PARTIAL "regardless of margins," which IMPLIES PARTIAL dominates — but §6 lists PASS/FAIL/PARTIAL as three states without stating the resolution order when a PARTIAL trigger and a FAIL condition co-occur. Pin the one line: *"PARTIAL triggers (clear-guard trip OR specificity trip) take precedence over the D2/D3 verdict; if either fires, the verdict is PARTIAL-investigate irrespective of whether D2/D3 were met or missed — no confound-tainted run is scored PASS or FAIL."* This closes the only residual ambiguity in the verdict lattice; it does not move a bar parameter. Verify at freeze.

## Dimension 2 — Anti-gaming shape

**Finding: SOUND on all three devices. One verifiability pin (C2).** This is the dimension I stress-tested hardest — a preregistered bar is only as good as its resistance to a motivated post-hoc read.

- **Clear-guard** (§4): differential clear voids the intake comparison and forces PARTIAL "in EITHER direction." Stress test — can it soften a FAIL into a PASS? **No.** It can only DEMOTE a would-be verdict to PARTIAL; it never promotes. Because it fires symmetrically (aware clearing MORE is PARTIAL just as aware clearing FEWER is), it cannot be selectively invoked only when a FAIL is inconvenient. The "different claim, re-opens the frame not the bar" framing (§4) is honest: an aware-clears-more result is a real finding but a NEW prereg, not a pass on THIS one. Passes the stress test.
- **Specificity control** (§5/§6): matched-baseline `M_rel` should ≈0; baseline-margin > ½ × encounter-margin ⇒ PARTIAL-investigate. Stress test — can it become a backdoor re-roll? **No.** It is a TIGHTENING predicate (adds a PARTIAL path), not a re-run trigger and not a PASS path. A clean specificity read is NECESSARY but not SUFFICIENT for PASS (which still requires D2 ∧ D3 ∧ clear-clean). It cannot manufacture a pass; it can only catch a confound. The ½× threshold is a fixed pre-registered ratio, not an executor judgment. Passes.
- **C2 seal** (§2): blind arm runs FIRST, complete, hash-sealed before ANY aware fight. The W3′ C2 lineage precedent exists on disk (`…-tier3-w3prime-pregate-seal.json`, verified present). This is the correct no-peeking device. **However**, §2 states the seal is written "before ANY aware fight fires" but — exactly as in my W3′ C2 finding — does not pin the seal as an md5-embedded auditable artifact whose mutation HALTs. In a single-process run nothing structurally prevents the blind aggregate from being (re)computed after aware data exists in memory and reported as "pre-sealed." → C2.

→ **C2 (WARN): pin the blind-arm seal as an md5-embedded, mutation-HALTs artifact (W3′ §8 C2 lineage).** §2 must obligate the same shape my W3′ check obtained: the blind arm's 256 per-fight records + the derived encounter-arm aggregate-per-seed means + SD_seed are written to a sealed seal-JSON, flushed BEFORE the first aware fight; the final verdict JSON embeds that seal's md5; any post-seal mutation of the blind record ⇒ red-flag HALT (no verdict). This converts "sealed before aware" from a sequence ASSERTION into a hash-checkable INVARIANT the conductor's DRIFT-CRITIC pass can confirm independent of the aware outcome. §2 already names the W3′ seal precedent; C2 asks only that the ARTIFACT make the ordering auditable. Does not move a bar parameter. Verify at freeze.

## Dimension 3 — Numbers re-derivation (first-hand)

**Finding: EVERY preview claim reproduced EXACTLY. D2 and k in-window.**

- **Deterministic-cell counts** — re-derived from the battery `results` dict (keyed `island|tier|cell|arm|seed`, 256 records, 32 frame-cells × 2 arms × 4 seeds), grouping per (cell, arm) and taking population-SD across the 4 seeds on `player_damage_total`:
  - baseline: **29/32** seed-deterministic (SD=0) — matches §4/§5 claim.
  - encounter: **21/32** seed-deterministic — matches §4/§5 claim.
  - (mobs_killed identical 29/21; total_aoe_hits 29/23 — the dealt-degeneracy §4 cites is real: dealt ≈ Σ mob HP under full-clear, the W3/W3′ convergence lesson.)
- **Encounter aggregate CV** — mean per seed across the 32 encounter cells, then CV across the 4 seed-aggregates using SAMPLE SD (n−1): **4.70% dealt, 1.30% time-proxy (trace length)**; baseline time-proxy **0.53%**. All three match §4/§5 EXACTLY. Confirms the sheet uses the sample estimator (3 df) consistent with the pinned D3 estimator — not population SD.
- **D2 = 10% window** — legolas consult bifurcation: regime-shift cluster >100% (Uriarte kiting; Black & Darken +475.975% at complexity-3, confirmed in the full-PDF addendum Table 1) vs subtle trained-agent cluster 3–17 pp (HRL-IM 3–7, Multi-UAV 1–6, HoK 15–17); ours predicted subtle by the competent-play-convergence lesson; the 5–15% relative window is the defensible D2 space in BOTH sources. **10% sits at the window center-plus.** In-window, correctly justified.
- **k = 2 anchor** — legolas Q2 + Black & Darken §2: rliable 95%-CI-non-overlap ≈ 2σ under normality; k=2 is the practical floor at 4 seeds (noisy SD estimate, 3 df). Primary protection is D2; D3 is the anti-noise floor. Correctly anchored.
- **Predicate liveness** — on the dealt stand-in: D2-implied margin (10% × 2838 ≈ 284) vs D3-implied margin (2 × 133.4 ≈ 267) are close, D2 binding marginally. Both legs are LIVE (neither vacuous); both must hold. This is the intended design — D2 primary, D3 the floor against a noise-driven pass.

## Dimension 4 — Carried pins present

**Finding: ALL NINE present and verifiable.** §7 enumerates: (1) `player_gather_primitive` OFF both arms — carried, and the harness `run_traced` passes `track_proxy_population=False` (the gather-adjacent toggle) so the pin is code-consistent; (2) sequential fights (Disc #3) + smoke slice first (Disc #2, 1 cell × both arms × 4 seeds) — the harness runs sequentially within each leg and has a `--smoke` path (2 pairs × 1 seed), smoke JSONs present on disk; (3) decision-trace capture ON both arms — harness sets `trace_decisions=True`, traces present in the battery records; (4) seeds fixed {20260722–25}, no additions after seal — matches `SEEDS` in the harness; (5) site-coverage attestation — grounded (see Dimension-5 no-confound); (6) `max_hp` substrate deviation DISCLOSED as ARCHITECT item (exposure map reads runtime max_hp + preferred_behavior + aggro_radius_m, not spawn-time threat_tier/archetype labels) — honest disclosure, carried as the map's substrate definition; (7) runner extends the battery harness, verdict + seal JSON committed, traces regenerable-not-committed (BW-1 precedent); (8) corpus.db READ-ONLY, no schema changes, engine diff seal→verdict = ∅ (ADR-006); (9) commit-never-push, conductor pushes, `git -C` explicit. All present.

## Dimension 5 — Reproducibility & no-confound

**Finding: REPRODUCIBLE. No-confound guarantee VERIFIED IN CODE.**

- **Frame reproduction** — compositions reproduce via the battery harness cell/seed/parity logic (`…/gamora/notes/2026-07-22-aware-fighter-bw1-equivalence-battery.py`): the runner imports the frozen W3′ selection→formation→scenario machinery (`load_full_fit_rows`, `round_robin_draft`, `courts_swap`, `assign_formation`, `make_encounter_scenario`, `make_matched_baseline_scenario`) — the SAME logic that produced the sealed battery. Deterministic given the frozen fit rows + seeds.
- **Engine hash** — recorded `2f43045` in the sheet; verified `git rev-parse --short HEAD = 2f43045` at check time. §7 pin 8 forbids engine diff between seal and verdict.
- **No-confound (charter §1.4 ablation property)** — the load-bearing verification for §1's "any engine-code difference between arms voids the gate": at the frozen hash BOTH player target-choice sites (`spatial_engine.py:1574` and `:1957`) route through one seam `_policy_choose_target(config=policy_config)`; `policy_config` is threaded from `SpatialFightEngine._policy_config` (`:2407`), default BLIND; the AWARE config (line comment `:1559`) "swaps behavior WITHOUT touching this code path." The arms differ by the `policy_config` VALUE alone — no branch, no code-path fork. This is the config-only guarantee, confirmed in source, not just asserted in the sheet.
- **Config fidelity** — `AWARE_CANDIDATE_CONFIG` (considerations.py:171) = exactly the 6 §3 entries (`distance_normalized` + `exposure_incoming_threat_density`, `cluster_density`, `crossfire_overlap`, `lane_pressure`, `escape_gradient`), all weights 1.0. `BLIND_CONFIG` (:162) = `(("distance", 1.0),)` raw. Both match §3 verbatim.

---

## Action

- [ ] **Conductor (C1, WARN):** §6 — pin the PARTIAL-over-FAIL precedence rule (a clear-guard OR specificity trip forces PARTIAL-investigate irrespective of D2/D3 outcome; no confound-tainted run is scored PASS or FAIL). Closes the verdict-lattice ambiguity; no bar-parameter move.
- [ ] **Conductor (C2, WARN):** §2 — pin the blind-arm seal as an md5-embedded artifact (blind per-fight records + encounter aggregate-per-seed means + SD_seed, flushed before the first aware fight; verdict JSON embeds the md5; post-seal mutation ⇒ HALT). Converts "sealed before aware" from assertion to auditable invariant (W3′ §8 C2 lineage). No bar-parameter move.
- [ ] **Conductor (C3/C4/C5, INFO):** carry into the result read — (C3) below; (C4) below; (C5) below.
- [ ] **jack-ryan:** re-verify the two WARN pins (C1, C2) at the freeze beat, each on three axes — PRESENT? MECHANICAL (no residual executor discretion)? CONSISTENT with §1–§7 (no contradiction introduced)? On both present + mechanical, PASS-WITH-CONCERNS converts to clean PASS and the sheet freezes verbatim. No re-review of the INFO items.

## Additional INFO

→ **C3 (INFO): the D3 estimator was re-derived on the DEALT stand-in channel, not intake.** The intake field (`player_damage_taken`) is not in the recorded battery `triple` (which carries only the equivalence-battery metrics), so I could verify the estimator SHAPE and the deterministic-cell/CV claims on `player_damage_total` but not the intake numbers themselves — those only exist post-run. The shape is correct and the field is confirmed present in the engine; the actual intake SD_seed and margin land at execution. The conductor's DRIFT-CRITIC read should confirm the run's intake aggregate-per-seed and SD_seed are computed by the SAME estimator (sample SD, 3 df) I verified on the stand-in. Record in the result read.

→ **C4 (INFO): the intake channel's determinism profile is unknown pre-run.** Dealt is near-degenerate (21/32 encounter cells zero-noise) because it ceilings at Σ mob HP under full-clear; §4 correctly argues intake has "no such ceiling." That is the RATIONALE for intake-primary, and it is sound — but it also means the D3 degenerate-guard (SD=0 ⇒ auto-satisfy) is MORE likely to matter on the dealt-like tail than on intake, and the intake SD_seed could be either larger (more exposure variance) or, if the fighter is highly deterministic defensively too, small enough to make D3 near-vacuous. Neither breaks the gate (the guard + D2 handle both), but the conductor should REPORT the realized intake determinism profile alongside the verdict so a near-vacuous-D3 outcome is visible, not silent. Record in the result read.

→ **C5 (INFO): AWARE `distance_normalized` (F9) vs BLIND raw `distance` is a deliberate scale choice, correctly disclosed.** The AWARE config uses `distance_normalized` (not raw `distance`) so the reachability term is scale-commensurate with the five [0,1] geometry reads (considerations.py:168–170, BW-1.1 F9); BLIND keeps RAW `distance` for fast-path bit-exactness. This is the intended design (raw −distance ~tens of meters would dominate the utility sum), and the ablation still isolates geometry — but it means the arms differ by BOTH the geometry reads AND the distance-normalization, so a strict reading of "config-only difference" includes the normalize flag on the shared distance term. Immaterial to the no-confound guarantee (still one code path, config-valued), and the normalization is the correct engineering choice; noted only so the result read does not attribute a margin PURELY to the five geometry reads when `distance_normalized` is also in the AWARE mix. The shipped-config pruning lap (post-gate) owns disentangling the reads' individual contributions. Record in the result read / pruning-lap book.

## References

- `agentic_orchestration/gandalf/notes/2026-07-22-aware-fighter-ablation-prereg.md` (sheet under check, PINNED, `dee9f040`) — §1–§8
- `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw11-battery-after-full.json` (untracked working-tree battery; `results` keyed island|tier|cell|arm|seed) — re-derived 29/32 + 21/32 deterministic, 4.70%/1.30%/0.53% CV first-hand
- `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw1-equivalence-battery.py` — frame-reproduction machinery; `PRIMARY_METRICS` (dealt-triple, no intake); `--smoke` path; sequential-within-leg
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (@ `2f43045`) — `player_damage_taken` field (:4987, fed :3845/:4370, LC-cost-excluded per :1230–1238); seam call sites (:1574, :1957); `_policy_config` thread (:2407)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/considerations.py` (@ `2f43045`) — `AWARE_CANDIDATE_CONFIG` (:171, 6 entries all 1.0), `BLIND_CONFIG` (:162, raw distance), F9 normalize note (:168–170)
- `agentic_orchestration/legolas/notes/2026-07-22-ablation-bar-calibration-modeA.md` — 5–15% D2 window, k=2 rliable anchor, regime bifurcation
- `agentic_orchestration/gandalf/notes/2026-07-22-blackdarken-extraction-bar-calibration-addendum.md` — Black & Darken full-PDF: +475.975% regime-shift confirmation, D3 form precedent (margin ÷ reference σ)
- `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-pregate-seal.json` — C2 seal lineage precedent (present)
- `agentic_orchestration/qa/findings/2026-07-22-prereg-check-tier3-w3prime.md` — W3′ precedent (C2 seal shape, §4 degeneracy/leg-dropping stress-test method, folding convention)

---

## Re-verify (freeze beat)

**Target of re-verify:** amended sheet (folded pins). **Scope:** the two WARN pins ONLY (C1, C2), each on three axes — PRESENT? MECHANICAL (no residual executor discretion)? CONSISTENT with §1–§7 (no contradiction introduced)? INFO items (C3/C4/C5) not re-reviewed; they route into the result read / DRIFT-CRITIC pass per this finding's Action.

- **C1 — PARTIAL-over-FAIL precedence:** re-verify §6 states the precedence rule explicitly; no run with a clear-guard or specificity trip is scored PASS or FAIL.
- **C2 — md5-embedded blind seal:** re-verify §2 names the seal artifact, its pre-first-aware-fight flush, the md5 embed in the verdict JSON, and the mutation-HALT.

On both present + mechanical + consistent: **PASS-WITH-CONCERNS → clean PASS; the sheet may FREEZE verbatim.** The instrument is then fully pre-registered with zero residual executor discretion on the pinned degrees of freedom; the conductor judges results as DRIFT-CRITIC against the frozen sheet.

**Reviewed by:** jack-ryan (DEV-MODE, pre-registration check), 2026-07-22.

---

## Re-verify result (freeze beat) — 2026-07-22

**Amended sheet reviewed** (READ-ONLY): `…/gandalf/notes/2026-07-22-aware-fighter-ablation-prereg.md` — §2 (lines 43–50), §6 (lines 138–148), §8 (lines 177–184). Both C1 + C2 pins folded by the conductor (gandalf). Three-axis check run against THIS finding's pin language (C1 line 30, C2 line 40).

**C1 — PARTIAL-over-FAIL precedence (§6 "Precedence rule", lines 138–141):**
- **PRESENT** ✓ — new §6 bullet, verbatim my proposed line including the "no confound-tainted run is scored PASS or FAIL" clause.
- **MECHANICAL** ✓ — "irrespective of whether D2/D3 were met or missed" is a strict override; a PARTIAL trigger deterministically dominates the D2/D3 verdict. No residual executor discretion on state resolution.
- **CONSISTENT** ✓ — matches §4's "regardless of margins" (line 88); completes the §6 verdict lattice (the one unstated precedence edge my Dimension-1 flagged). No §1–§7 contradiction introduced.

**C2 — md5-embedded blind seal (§2 C2-seal bullet, lines 43–50):**
- **PRESENT** ✓ — §2 bullet rewritten to name the seal artifact.
- **MECHANICAL** ✓ — all four required elements present, each a mechanical check: (1) seal-JSON = 256 blind per-fight records + encounter-arm aggregate-per-seed means + `SD_seed`; (2) flushed to disk BEFORE the first aware fight; (3) verdict JSON embeds the seal md5; (4) post-seal mutation ⇒ red-flag HALT, no verdict. md5 compare is hash-checkable; zero discretion. Converts "sealed before aware" from sequence assertion to auditable invariant (W3′ §8 C2 lineage).
- **CONSISTENT** ✓ — the sealed object (`SD_seed` on the blind encounter-arm aggregate mean intake) matches the §5 D3 estimator (lines 106–117) EXACTLY; DRIFT-CRITIC-confirmable per §8 (line 182). No §1–§7 contradiction introduced.

**INFO riders (C3/C4/C5):** NOT re-reviewed per prereg. Confirmed present as §6 result-read riders (lines 142–148); their presence introduces no §1–§7 contradiction (non-gating result-read directives — DRIFT-CRITIC estimator-echo, intake-determinism report, `distance_normalized` attribution caveat).

**Conversion verdict: PASS-WITH-CONCERNS → clean PASS.** Both WARN pins pass all three axes; no bar-parameter moved (folding-only, per the W3′ convention). **The sheet may FREEZE VERBATIM.** The instrument is fully pre-registered with zero residual executor discretion on the pinned degrees of freedom; the conductor now judges results as DRIFT-CRITIC against the frozen sheet, and execution (named-gamora charter → seal → run → verdict) may proceed.

**Re-verified by:** jack-ryan (DEV-MODE, freeze-beat re-verify), 2026-07-22.
