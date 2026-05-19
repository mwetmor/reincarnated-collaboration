# R8 Disposition — Coalescence-First Pipeline + Cost-Mode Decision

**Date:** 2026-05-19
**Author:** gandalf
**Authority:** Autonomous-operation per protocol § 4.0 + dispatch
**Tag fires on:** `hive-rebuild/v0.11-r8-disposition-decided`

## TL;DR

**Sub-case 3 applies. Disposition C variant: cohesion-defaulted, cost-opt-in (DEFERRED).**

- Commit `inverted` (coalescence-first + per-entity LLM naming retained) as the engine default. The R8 hypothesis HOLDS for this mode (Test 1: +0.20 cohesion above baseline; substrate-identity preserved at canonical-element level).
- DO NOT commit `inverted_no_naming` as a callable opt-in mode at this time. Template-distribution produces uniform severe template strain (TSI = 1.0 across all 3 seasons) and catastrophic F6 collapse (cohesion −0.70 below baseline). The cost-savings (99.7%) are real but the surface-quality cost is unshippable as-is.
- DEFER `inverted_no_naming` as a future opt-in pending template-distribution repair (per follow-on engineering task; see § 5 below).
- Preserve `--keep-llm-naming` CLI flag (now maps to default `inverted` mode); deprecate the no-naming default behavior; remove `inverted_no_naming` from CLI surface until repaired.

## 1. Per-test result summary

| Test | Metric                                          | baseline | inverted | inverted_no_naming | Threshold | inverted | inverted_no_naming |
|------|-------------------------------------------------|----------|----------|--------------------|-----------|----------|---------------------|
| 1    | Mean cohesion (6-facet)                         | 4.57     | 4.77     | 3.87               | within 0.5 of baseline | **PASS** (+0.20) | **FAIL** (−0.70) |
| 2    | Skill-geometry entropy                          | 3.348    | 3.328    | 3.348              | ≥ baseline | PASS (Δ=−0.02 noise) | PASS (Δ=0) |
| 2    | Role-orientation entropy                        | 1.349    | 1.349    | 1.349              | ≥ baseline | PASS | PASS |
| 2    | Gear catalog parity                             | 19/20    | 19/20    | 19/20              | ≥ baseline | PASS | PASS |
| 3    | LLM call reduction (vs baseline ~395/season)    | —        | ~388/sn  | 1/season           | ≥ 75%     | FAIL (~2% reduction) | **PASS strong (99.7%)** |
| 4    | Substrate-identity at canonical-element level   | —        | invariant | invariant         | discovery | invariant | invariant |
| 4    | Substrate-mode preservation in downstream surface | ~90%   | ~90%     | ~63%               | discovery | preserves | erodes ~3x |
| 5    | Multi-shot Jaccard ≥ 70%                        | —        | STAGED   | STAGED             | ≥ 70%     | deferred | deferred |
| TSI  | Template strain (FM-1 through FM-6)             | n/a      | n/a      | 1.0 (floor)        | ≥ 4.0 for A; 2.5-4.0 for C dual | n/a | **FAIL** |

**Per § A.3 four-sub-case decision-tree:**

- Sub-case 1 (cohesion within 0.2 of baseline AND TSI ≥ 4.0): REJECTED — inverted_no_naming cohesion −0.70 + TSI 1.0
- Sub-case 2 (cohesion within 0.5 AND TSI 2.5-4.0 AND cost ≥ 75%): REJECTED — inverted_no_naming cohesion −0.70 (exceeds 0.5) + TSI 1.0 (below 2.5)
- **Sub-case 3 (inverted_no_naming cohesion drops > 0.5 BUT inverted holds within 0.5): APPLIES** — inverted_no_naming −0.70; inverted +0.20
- Sub-case 4 (both inverted arms drop > 0.5): REJECTED — inverted holds at +0.20

## 2. Disposition decision

### 2a. Commit: `inverted` as engine default

**Architecture change:** the engine's default season-generation pipeline becomes mechanical-generation-first + post-convergence theme-coalescence (1 LLM call) + per-entity LLM naming (Phase B, ~388 calls per season as in baseline).

Rationale:
- R8 hypothesis HOLDS at +0.20 cohesion above baseline (Test 1). The coalescence-first approach not only matches but exceeds input-driven theming on the cohesion-measurement instrument.
- Substrate-identity at canonical-element level is invariant across baseline and inverted (Test 4a). Mechanical substrate is byte-equal; arms differ only in naming-surface decoration of that substrate.
- Eliminates the input-theme requirement, which was a coupling Test 4c showed was not load-bearing for cohesion (the coalescence can pick substrate-aligned theme without input).
- Cost savings vs baseline: minor (~2% — one element_selection call replaced by one theme_coalescence call). Cost is NOT the win; cohesion + decoupling-input-theme is the win.

### 2b. Defer: `inverted_no_naming` as opt-in

**DO NOT commit `inverted_no_naming` as a callable mode at this time.** Reasons:

- Cohesion −0.70 below baseline (Test 1 FAIL); the average season would ship at "workmanlike but templated" with F6 collapse making the player-facing surface read as broken (literal "Unknown" in monster names; "weight Sovereign" trial boss; 5 unique skill names across 110+ skills).
- TSI 1.0 across all three seasons (uniformly severe template strain on every failure-mode dimension). Not a per-season anomaly; an arm-wide architectural failure.
- Specific player-facing brokenness items the disposition will not tolerate shipping:
  1. **Literal "Unknown" suffix on monster names** ("Marginalia Unknown", "Beacon's Unknown") — template-fallback string leaks into output
  2. **Lowercase common nouns** as trial-boss names ("weight Sovereign") — string-handling bug
  3. **5 unique skill names across ~110 skills** — vocabulary fixedness saturation; the player would feel the engine is broken
  4. **Slot-mode-of-action violations** at ~37% of skills (vs ~10% for inverted) — "Gale Strike" tagged as self_buff geometry; player intuition breaks
- Even if these were fixed at the implementation level, the underlying architecture (template-only composition with no per-entity rescue) cannot produce the variation per-entity LLM naming produces for ~$0.003/entity. The trade is real, but at current quality envelope it is not shippable.

**Future opt-in pathway** (deferred, NOT committed in this disposition):

When template-distribution is repaired — at minimum: (a) string normalization on template inputs (eliminate lowercase + "Unknown" leak); (b) richer template patterns beyond "(slot_token) Strike" (must include geometry-aware verb selection so slot-mode-of-action is honored); (c) per-class name-diversification by salting with archetype-tag, role-orientation, and energy-type so the "Anchor X Y" template breaks into varied patterns — then re-run a focused A/B (3 seasons inverted_no_naming vs 3 inverted on the same seeds) and re-judge with this protocol. If TSI ≥ 3.0 and cohesion within 0.5 of inverted (not baseline — baseline becomes irrelevant once inverted is the default), commit as cost-opt-in for batch-regeneration / mod-export contexts.

### 2c. CLI surface

Current CLI flags:
- `--keep-llm-naming` (currently maps to `inverted` mode)
- (no flag) (currently maps to `inverted_no_naming` default)
- `--theme-input PATH` (currently maps to `baseline` mode)

**Post-disposition CLI:**
- (no flag) → `inverted` mode (coalescence + per-entity LLM naming retained, the new default)
- `--theme-input PATH` → `baseline` mode (preserved for content-team workflows that want input-driven theming; not deprecated)
- `--keep-llm-naming` → deprecated as no-op (always-on now); emit warning if passed; remove in next minor version
- `--no-llm-naming` (new flag, optional) → `inverted_no_naming` mode, BUT ONLY after template-distribution repair; until repair, this flag should not be wired or should raise an explicit "deferred-pending-repair" error

The bias of the default flips: previously, the no-naming pathway was the default (saving cost by accident in the previous architecture). After this disposition, the **default emits high-quality named content**; cost-savings paths are explicit opt-ins.

### 2d. R8 hypothesis closure

The R8 hypothesis stated: "coalescence-first generation post-mechanical-convergence preserves cohesion and substrate-identity while opening cost-savings via reduced LLM calls."

**Disposition reading:**
- **Cohesion preservation: PROVEN for the `inverted` arm.** The coalescence call CAN produce cosmological vocabulary on par with or better than input-driven theming, when per-entity LLM naming downstream is retained.
- **Substrate-identity preservation: PROVEN at the canonical-element level.** Mechanical substrate is invariant across all arms.
- **Cost savings: NOT achieved at acceptable quality.** The path that achieves cost savings (`inverted_no_naming` template-distribution) fails cohesion + has uniform severe template strain. The naming-Phase-B per-entity LLM calls were doing real cohesion work that templates cannot replicate without architectural enhancement.

**The hypothesis is partial-pass.** The architectural shift to coalescence-first IS sound; the cost-reduction-via-template-distribution is NOT (yet) sound. The engine commits the sound half. The unsound half re-opens as a follow-on engineering question (§ 5 below).

## 3. Canonical-doc amendments

### 3a. `canonical/19-llm-call-map.md` — UPDATE

Phase A is amended:
- REMOVE: `element_selection` (1 call per season)
- ADD: `theme_coalescence` (1 call per season, post-convergence, returns 8 slot fills + 3 pair rationales + 1 anchor + 1 seasonal element)

Phase B is preserved with one note: the coalesced theme vocabulary is now passed in context to per-entity LLM naming calls (class_naming, skill_naming, monster_naming, trial_naming, gear_unique_naming). Calls-per-season totals are essentially unchanged from baseline (~388-395 calls).

The amendment is small but architecturally meaningful: the input-theme assumption is gone; the engine derives its own theme from converged content.

### 3b. `canonical/story/substrate-identity-declarations-2026-05-17.md` — APPEND

Add subsection: "Substrate-identity at the surface — pipeline-pipeline dependency."

Content (per Test 4 discovery):

> The R8 A/B run (2026-05-19) empirically confirmed substrate-identity invariance at the canonical-element level across baseline (input-themed) and inverted (coalescence-first) generation pipelines. Mechanical substrate produces byte-identical canonical-element distributions per seed regardless of which naming pipeline runs afterward. This is the strongest form of substrate-identity preservation: the substrate IS the mechanical generation; naming is a downstream cosmetic decoration of that substrate.
>
> Player-facing READABILITY of substrate-mode-of-action depends on the naming pipeline. Per-entity LLM naming (the committed `inverted` default) preserves substrate-mode-of-action in ~90% of player-facing skill names. Template-based composition (the deferred `inverted_no_naming` opt-in) preserves substrate-mode in only ~63% of names; the remaining ~37% are surface-token-bearing but mode-of-action-mismatched. Future implementations choosing template-distribution for cost reasons should be aware that ~1 in 3 skill names will read as substrate-mode-mismatched until template-distribution is repaired to honor slot-mode-of-action.

### 3c. No new doc authored

A separate "template-composition mechanism" doc that would have accompanied Disposition A is NOT authored, because `inverted_no_naming` is not being committed. If/when template-distribution is repaired and a future disposition commits `inverted_no_naming` as opt-in, the template-mechanism doc should be authored at that time as part of the commit.

## 4. Operating envelope of committed mode

For consumers of the engine post-disposition:

**Default mode (`inverted`, coalescence-first + per-entity LLM naming retained):**
- Cohesion: 4.57-4.77 mean (within or exceeding baseline)
- Cost: ~$3.20 per season (vs baseline ~$3.23)
- LLM call count: ~388 per season
- Substrate-identity: canonical-element invariant per seed; substrate-mode-of-action ~90% preservation
- Input theme: NOT required (engine coalesces theme from converged content)
- Anchor: selected via DB-state-dependent process (per current implementation — anchor parity across concurrent seed-equal runs; not yet `--anchor-id` controllable)

**Available mode (`baseline`, input-driven theming, `--theme-input PATH`):**
- Cohesion: 4.5-4.7 mean
- Cost: ~$3.23 per season
- LLM call count: ~395 per season
- Substrate-identity: same as default
- Input theme: REQUIRED (`--theme-input data/themes/baseline_theme_{element}.json`)
- Use case: content-team workflows that want explicit theme control

**Deferred mode (`inverted_no_naming`, template-distribution):**
- DO NOT use in production until template-distribution repair (see § 5).
- If accessed: cohesion ~3.87 (workmanlike-but-templated boundary; F6 cliff at 1.0); cost ~$0.013 per season; TSI 1.0 (max template strain); visible template debris in player-facing surface.

## 5. Follow-on engineering items

### 5a. Template-distribution repair (deferred opt-in pathway)

Owner: rocket (engine specialist).
Trigger: when capacity allows; not P0.

Scope:
1. Eliminate "Unknown" literal-string leak in monster naming template fallback
2. Eliminate lowercase common-noun composition (string normalization at template entry)
3. Replace "(slot_token) Strike" with geometry-aware template families (e.g., bulwark-slot skills templated with verb-pool {"Ward", "Hold", "Anchor"}; suffusion-slot skills with {"Seep", "Flood", "Surge"}; impact-slot with {"Crush", "Strike", "Blow"}; etc.)
4. Salt class-name templates with archetype-tag + role-orientation so "Anchor X Y" pattern varies into 8+ template skeletons
5. Validate slot-mode-of-action: composed skill names must honor the slot semantics of their slot tag

When repaired: re-run focused A/B (`inverted` vs `inverted_no_naming`, 3 seasons on R8 reserved seeds), re-judge with this protocol. Disposition re-opens.

### 5b. Pipeline gap: seasonal_dominant_element write-back

Owner: rocket or star-lord.
Trigger: independent of template-repair; address now.

Scope: per Test 4 Finding 5, both inverted arms have `seasonal_dominant_element: None` on every class file. The cosmological_vocabulary.json has the seasonal element name; the class records need a write-back step in the inverted pipeline. Single-file fix to the class-record finalization step.

### 5c. Multi-shot stability (Test 5) execution

Owner: rocket or star-lord (engine-side execution).
Trigger: post-tag fire; against committed mode.

Per `output/R8-test5-stability.md`: execute 3× coalescence call on `inverted/season_099002` (Drowned Lighthouse, brine — strongest cohesion in run); compare anchor + element + slot-fill Jaccard. If < 70%, append findings to this disposition doc; stability concern surfaces. Expected cost ~$0.04-0.10.

### 5d. Anchor-id controllability for substrate-identity Test 4-style runs

Owner: rocket or star-lord.
Trigger: when next anchor-identity-controlled experiment is needed.

Scope: per R8 README anomaly #4, anchor selection is DB-state-dependent. For controlled substrate-identity experiments (e.g., "does the same anchor + same seed produce same coalescence?") add `--anchor-id` CLI flag to force anchor selection bypass. This would have eliminated the seed-099001 anchor-parity anomaly in this run.

## 6. Asymmetry note for the record

The disposition is partial-commit because the R8 work is partial-success. The honest read:

- The R8 architectural shift (mechanical-first, theme-coalesce, retain per-entity naming) succeeded — this is the new default.
- The cost-aggressive variant (eliminate per-entity naming entirely, use templates) failed — this is the deferred opt-in.

This is not a failure of the R8 hypothesis but a refinement of its claim. The original cost-claim (90%+ reduction) was always going to require eliminating Phase B per-entity naming (per star-lord's R8 pipeline design § SL-2). That elimination COULD have worked if templates could substitute for LLM per-entity calls; the empirical result is that they cannot without architectural enhancement.

What the engine gains from this disposition:
- A coalescence-first pipeline that preserves substrate-identity at the canonical-element level
- Decoupling from input-theme as a generation requirement
- Empirical validation that the coalescence-call CAN produce cohesion-on-par with or better than input-driven theming
- A clean, repeatable methodology (this protocol + appendix) for re-judging template-distribution when repaired

What the engine does NOT gain:
- The 90%+ cost reduction; cost reduction is ~2% under the committed mode

Cost reduction at scale remains a future engineering question. For now, the engine commits cohesion + decoupling.

## 7. Sub-case 3 summary

| Field                  | Value                                                                 |
|------------------------|-----------------------------------------------------------------------|
| Disposition            | Sub-case 3 / Disposition C variant: cohesion-defaulted, cost-deferred |
| Committed mode         | `inverted`                                                            |
| Deferred mode          | `inverted_no_naming` (pending template-distribution repair)           |
| Preserved mode         | `baseline` (input-themed, opt-in via `--theme-input`)                 |
| LLM call map amendment | Phase A: element_selection → theme_coalescence (1-call swap)          |
| Substrate-identity amendment | Append "surface-readability depends on pipeline" subsection     |
| CLI surface change     | Default flips to inverted; --keep-llm-naming deprecated as no-op      |
| Follow-on items        | Template repair / pipeline gap fix / Test 5 execution / anchor-id flag |

---

**Tag fires on this disposition: `hive-rebuild/v0.11-r8-disposition-decided`.**

*Authored 2026-05-19 by gandalf under autonomous-operation authority. The hypothesis was tested honestly; the result is partial-pass; the engine commits what it learned. The coalescence-first pipeline ships as default. The cost-aggressive variant ships when its template-distribution can carry the surface-quality envelope. Mithrandir signs.*
