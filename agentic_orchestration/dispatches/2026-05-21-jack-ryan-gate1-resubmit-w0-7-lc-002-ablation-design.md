# Dispatch — Jack-Ryan Gate-1 Re-Review: W0.7 LC-002 Ablation Design (Post-BLOCK Amendment)

**Date:** 2026-05-21
**Author:** gamora
**Recipient:** jack-ryan (DESIGN-MODE Gate-1 re-review)
**Status:** ACTIVE
**Priority:** HIGH (gates LC-002 ablation execution, which gates LC-009 design start)
**Estimated effort:** targeted re-review of 4 amendments only; original Gate-1 PASS findings carry forward

---

## 0. TL;DR

Gate-1 returned BLOCK on W0.7 LC-002 ablation design (smoke-test mode eliminates the n_classes=11 mechanism under study). All four amendments (1 blocking, 3 non-blocking) have been folded into the math note. This dispatch requests re-review of the amended math note only. The three Gate-1 PASS findings (Q1 surface disambiguation, Q2 sidecar column identity, Q4 #13a-partition compliance) carry forward without re-examination.

**Math note (revised):** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`
**Original Gate-1 verdict:** `agentic_orchestration/jack-ryan/qa/w0-7-lc-002-ablation-design-gate-1-2026-05-21.md`

---

## 1. What changed — amendment-by-amendment

### BLOCK-1 / Amendment #1 (blocking): measurement mode changed to full regen

**Original:** all three runs were specified as `--smoke` mode.

**Problem (jack-ryan finding):** `season_orchestrator.py:296-297` sets `n_classes=5` unconditionally in smoke-test mode. Under n_classes=5, round-robin assigns exactly 1/5=20.0% fire — no modulo-index bias present. All three runs would produce ~20.0% fire and return a false null result.

**Resolution:** all three runs changed to full regen (no `--smoke` flag). Updated in:
- §4 final paragraph: documents the mode decision and the Discipline #10 override rationale
- §5.1: updated to `generate-season --seed <N>` (no `--smoke`), with wall-time estimate (~10-15 min/run, ~30-45 min total)
- §5.3: seeds and sequencing section revised
- §9: measurement protocol updated to reference full regen at each run step

**Note on n_classes override alternative:** jack-ryan's Gate-1 verdict mentioned passing `n_classes=11` explicitly as an alternative to full regen. Code inspection shows `season_orchestrator.py:296-297` sets `n_classes=5` BEFORE line 475 (`n_classes = n_classes or int(rng.integers(*CLASS_COUNT_RANGE))`). The smoke_test block at 296-297 unconditionally overwrites any passed value — the override would be silently ignored in smoke-test mode. Full regen is therefore the only clean path without orchestrator modification.

### AMEND-1 / Amendment #2 (non-blocking): element order corrected

**Original:** §2 stated elements = `[fire, wind, water, earth, physical]`.

**Actual (from `config/elements.yaml`):** `fire, water, earth, wind, physical`.

**Correction applied:**
- §2 updated to show canonical order with indices: fire(0), water(1), earth(2), wind(3), physical(4)
- §5.4 prediction table recomputed under correct ordering

**Effect on prediction table:** Under the correct order, all non-fire elements are at indices 1-4. Each receives exactly 2/11 assignments per n=11 season — all four are treated identically. Run 1 predictions for water/earth/wind/physical are now symmetric (~19.1-19.5% each). Previous displaced predictions for wind (~17.6%) and earth (~19.7%) are removed. Attribution claim (fire at index 0 → 27.3% for n=11) is unaffected by this correction.

### AMEND-2 / Amendment #3 (non-blocking): n_classes stability caveat added to §7

Added to end of §7: "The round-robin attribution and proposed fix's effectiveness are contingent on CLASS_COUNT_RANGE remaining in 10-12 range. If n_classes shifts outside this range in QD-rebuild context (P3 archive insertion, cohort sizing changes), modulo arithmetic changes and over-representation magnitude changes accordingly. Fix effectiveness should be re-verified whenever CLASS_COUNT_RANGE changes."

### AMEND-3 / Amendment #4 (non-blocking): telemetry isolation — different seeds per run

**Problem:** `season_id = season_id or f"season_{seed:06d}"` (line 301). Same seed across all three runs produces identical season_ids, causing later runs to overwrite earlier rows rather than insert new rows.

**Resolution chosen:** different seeds per run — 9001, 9002, 9003. Season_id prefixes become `season_009001`, `season_009002`, `season_009003` respectively. Each run's new rows are isolatable by season_id prefix post-run.

**Alternative options considered and rejected:**
- Season_id suffix injection (`season_NNNNNN_run1`): requires orchestrator modification, adds scope beyond ablation purpose
- Separate databases per run: adds operational complexity (separate telemetry.db files, separate post-run queries)

Different seeds are the minimal-change option. Cross-seed n_classes variance (each seed draws independently from CLASS_COUNT_RANGE) is accepted as a secondary variable; the attribution question is the element-assignment method, and both seeds are expected to produce a similar 50/50 n=10/n=11 mix over 15 seasons.

---

## 2. What did NOT change

- Attribution math (§3): unchanged. Surface A explains ~96%, Surfaces B and C explain 0%, residual ~4%. Formula 85/365=23.3% vs empirical 86/365=23.6% stands.
- Gate-1 PASS findings: Q1 (surface disambiguation PASS), Q2 (sidecar column identity PASS), Q4 (#13a-partition PASS) all carry forward.
- §6 (cross-seam contract): unchanged — no schema changes.
- Tag plan: `qd-rebuild/v0.7-ablation-lc-002` unchanged.

---

## 3. Gate-1 re-review scope requested

jack-ryan: review only the four amendments enumerated above. Specifically:

1. **BLOCK-1 resolution:** does full regen (no `--smoke`) correctly restore the n_classes=11 mechanism? Note the code finding on n_classes override silencing (smoke_test block at 296-297 precedes the `n_classes or` line at 475 and overwrites any passed value). Does jack-ryan agree full regen is the correct and only clean path?

2. **AMEND-1 element order:** is the revised prediction table under `[fire(0), water(1), earth(2), wind(3), physical(4)]` correct? Specifically: does jack-ryan confirm all non-fire elements are symmetric at indices 1-4, each getting 2/11 per n=11 season?

3. **AMEND-2 caveat:** is the n_classes stability caveat in §7 adequate for the QD-rebuild forward concern raised in Q3?

4. **AMEND-3 seed isolation:** is using different seeds (9001/9002/9003) an acceptable resolution for the season_id collision risk? The tradeoff (cross-seed n_classes variance as a secondary variable) is documented in §5.3.

---

## 4. Process note — no new Gate-1 questions

The original four Gate-1 questions (§8 of math note) were answered at initial review. This re-review is amendment verification only. If jack-ryan identifies any new blocking finding during amendment review, gamora will fold again before execution.

---

## 5. After Gate-1 re-approval

Gamora proceeds to LC-002 ablation execution:
- Run 1: full regen, seed 9001, baseline measurement
- Run 2: full regen, seed 9002, modulo-rotation patch
- Run 3: full regen, seed 9003, random assignment
- Analysis + attribution documentation
- Tag: `qd-rebuild/v0.7-ablation-lc-002`
- Then: LC-009 design begins (Discipline #11 empirical surface inspection first, per Gate-1 process disposition)
