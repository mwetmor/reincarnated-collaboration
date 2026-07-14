# Dispatch — 2026-07-13 — gamora — Cell-key dedup v1 (✅ FIRED — gate cleared, Matt GO)

**From:** knight-rider (sequencing)
**To:** gamora (simulation seam — dedup/matchup consumes the cell key per register §7)
**Spec author:** gandalf — **authoritative build spec:** `agentic_orchestration/gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md` (register §6/§6.1/§8). **This authored spec SUPERSEDES the thin build summary in this wrapper — build straight off it.**
**Status:** ✅ **FIRED 2026-07-13 (Matt GO).** Gate fully cleared. elrond materialization COMPLETE + KR-verified (commits `2a02ed0d`/`6c726afd`): `cell_key` is a materialized column, `GROUP BY`-able, 470/470 combat-kit rows keyed (system-records NULL), all 4 keyed columns + `resource_verbatim` populated, #5 two-slot confirmed, unknown/blank preserved as literals. gandalf independent read-only verification PASSED (`30938cc1`; full record `gandalf/design-inputs/cell-key-verification-gandalf-2026-07-13.md`) — arity/coverage/enum-distribution/spot-rows all verified against the live DB. KR re-confirmed read-only 2026-07-13: 457 distinct / 470 rows / 0 missing / 14-arity. Nothing gates this. Matt GO given; fired as read-only subagent.
**Pattern:** B (pure data analysis over corpus.db — a `GROUP BY` + a Hamming-1 scan; ~470 rows. NOT a sim run: no gauntlet/batch/cert/compute campaign.)
**Approved by:** Matt 2026-07-13 (§6.1 ratified: strict-13 first; dedup v1 = strict `GROUP BY cell_key`). This is execution of the ratified key — no new design decision inside this dispatch.

## ▶ PICK-UP DIRECTIVE (gamora — execute on session start)

**This dispatch is FIRED and ready. Execute it.** Run mode: read-only over `corpus.db` (`PRAGMA query_only=ON` / `mode=ro` URI). No writes to corpus.db — analysis-only.

1. Build straight off the authored spec `gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md` (it supersedes the thin summary below).
2. Run Stage-1 strict `GROUP BY cell_key` + the THREE outputs — **in the reshuffled priority below (★near-twin aggregate is PRIMARY, not #3).**
3. **STOP after the three outputs.** Do NOT coarsen, do NOT demote, do NOT delete isotopes. Stage-2 is the gandalf + gamora + Matt cluster review — a separate loop KR schedules once your collapse-structure report lands.
4. One-line-confirm your representative-selection SQL with gandalf before finalizing the cell table (per spec §Stage-1 step 2).
5. Auto-commit your analysis artifacts (log + any script); **NO push** (Matt-gated per ADR-006). `corpus.db` is gitignored-by-design — commit the log/script, not the binary.

**KR gate-clearance for your session start:** the "do NOT start until cell_key exists AND has been verified" HARD GATE in the spec (§HARD GATE) is **CLEARED** — elrond materialized it (`2a02ed0d`), gandalf independently verified it read-only (`30938cc1`), KR re-confirmed (457/470/0-missing/14-arity). You are clear to read `cell_key` immediately.

## Context

The cell key is ratified (register §6.1) and (once elrond completes) materialized as a serialized `cell_key` on `canon_engine_key`. Dedup v1 is deliberately the **maximally-split** start: strict exact-match on the full 13-tuple. It **never wrong-merges** — a later Stage-2 split/coarsen is cheap; a wrong early merge is a re-key (§6.1: split-late beats merge-wrong; the isotope/early-chemistry model). The output of Stage 1 IS the evidence that drives the Stage-2 coarsening review — the grain is *measured*, never guessed.

## Required reading before starting

- **Authoritative build spec:** `agentic_orchestration/gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md` — the strict `GROUP BY` + the 3 Stage-2-readiness outputs + the stopping point. **Build off this; the summary below is orientation, not a re-derivation.**
- `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6/§6.1 (ratified key + isotope/tiebreak model) + §8 (your hook).
- elrond's completion record on `dispatches/2026-07-13-elrond-cell-key-materialization.md` (the `cell_key` contract you consume — materialized column, combat-kit scope, unknown/blank footprint = 49 rows).

## The build (per gandalf's finalized spec — summary)

- **Stage 1 = strict exact-match `GROUP BY cell_key`** over the 470 `row_class='combat-kit'` rows → **cells** (each distinct `cell_key` = one mechanical "element") + **isotope stacks** (kits sharing a cell = true variants, retained, never deleted). Strict only — no coarsening, no merge beyond exact match, no deletion.
- **Representative per cell = the §6 tiebreak:** longevity of lineage across games → recency → primary; losers retained as mouseover "isotopes." **Column-math is yours to draft** (e.g. longevity ≈ distinct-game span or earliest `skill_debut_year`; recency ≈ max `era_year`) — propose the exact SQL and **confirm with gandalf (one line) before finalizing.** **Do NOT use the deprecated `mobile_*` fields** (`mobile_representative`/`mobile_rank_in_cell`/`mobile_key_group` — DEPRECATED per register §0).
- **Emit the 3 Stage-2-readiness outputs — but note the PRIORITY RESHUFFLE below.**

### ⚠ PRIORITY RESHUFFLE (Matt 2026-07-13, from the verified gate)
The strict-13 collapse is **near-maximally-split: 470 → 457 cells** = **445 singletons, 11 pairs, 1 triple** (gandalf-verified). The isotope-depth histogram is therefore **nearly trivial** — it tells the review almost nothing. **ALL the Stage-2 signal lives in the ★near-twin adjacency aggregate.** Treat it as the **PRIMARY deliverable**, not output #3. Spend your effort there.

  1. **Cell table** (support): `cell_key` · representative `kit_id` · isotope member `kit_id`s · population count.
  2. **Isotope-depth histogram** (support — expected trivial: ~445 depth-1, 11 depth-2, 1 depth-3): emit it, but it is not the decision object. Confirm the shape and move on.
  3. **★ Near-twin adjacency aggregate — THE PRIMARY DELIVERABLE (the Stage-2 driver):** all cell-pairs whose `cell_key`s differ in **exactly one** of the 14 positions, annotated with *which* coord differs + the two values; then **count near-twin pairs per differing-coord.** The coord with the most near-twin pairs is the strongest demotion candidate (e.g. "N near-twin pairs differ only on #10 tempo → tempo is behaving as texture"). This aggregate is the empirical object §6.1 Stage-2 rules on — it is where the grain decision is actually made now that the histogram is flat. Give it the depth: per-coord counts, the actual differing value-pairs, and your read on which coords are behaving as texture vs. identity.

## Out of scope

- **Do NOT coarsen the key.** Stage-2 coarsening is a *reviewed* pass (see follow-on below) — this dispatch is strict Stage-1 only.
- **Do NOT delete isotopes.** Retain all; representative is a flag, not a filter.
- No column materialization — that is elrond's completed upstream work; you consume `cell_key` read-only.

## Cross-seam contract change? (Principle 6)

**Round-trip: not applicable** — read-only analysis over elrond's `corpus.db` curation layer; no engine schema, no fight_log/loadout/export contract touched.

## Acceptance criteria

- [ ] Strict `GROUP BY cell_key` run over the 470 combat-kit rows; cell count + isotope-stack distribution reported.
- [ ] Representative flagged per §6 tiebreak; isotopes retained (count of retained-vs-representative).
- [ ] Collapse-structure report authored (the evidence packet for the Stage-2 review).
- [ ] Auto-commit analysis artifacts; NO push (Matt-gated).

## Follow-on (register, do not execute here) — Stage-2 cluster-review + coarsening

After dedup v1 lands, KR convenes a **cluster review: gandalf + gamora + Matt** to drive **Stage-2 coarsening** (§6.1): where two cells are the same build archetype differing only on one *texture* coord, demote that coord from cell-defining to isotope-distinguishing (reviewed merge, with the Stage-1 clusters as evidence).
- **Never-demote core** (stays in the key regardless): #2 delivery · #5 control (treatment+function) · #8 proxy · #1 movement · #12 activation · #13 dependency.
- **Demotable-with-evidence:** #3 amp · #4 geometry · #6 defense · #7 economy-model · #9 range · #10 tempo · #11 commit. (#7 is the contentious one — the data rules.)
- The demotable set is **RULED at Stage 2 with the cluster data, NOT a priori.** This follow-on is a decision loop, not a dispatch to auto-fire — KR schedules it once gamora's collapse-structure report exists.

## References
- Upstream (blocks this): `dispatches/2026-07-13-elrond-cell-key-materialization.md`
- Canon: register §6/§6.1/§7; ratification commit `fdfe220c`

## Completion record
_(append ALL of:_
- _cell count vs 470; isotope-stack distribution (depth-1/2/3+ histogram — expected trivial per reshuffle);_
- _representative-vs-isotope counts; the representative-selection SQL you finalized + gandalf's one-line confirmation;_
- _unknown/blank-slot cell count;_
- _**★ the near-twin-per-coord aggregate, RANKED — which of the 14 positions carries the MOST near-twin (Hamming-1) pairs, descending. This is the headline: the top-ranked coord is the strongest Stage-2 demotion candidate. Include the per-coord pair counts and your read on which coords behave as texture vs. identity;**_
- _path to the collapse-structure report artifact for the Stage-2 review;_
- _commit hash; round-trip disposition (expected: N/A — read-only over corpus.db).)_

---

### Completion record — gamora 2026-07-13 (commit `e00f4151`)

**Nature:** PURE DATA executed as specified — read-only strict `GROUP BY cell_key` + Hamming-1 scan over the 470 combat-kit rows (`row_class='combat-kit' AND cell_key IS NOT NULL`) in `agentic_orchestration/research/curated/corpus.db`. No sim, no gauntlet/batch/cert instrument. No coarsening, no deletion. STOPPED at the Stage-2 gate.

**Stage-1 collapse:** 470 kits → **457 cells** (strict exact-match on the 14-slot key; #5 control = 2 slots, 5a treatment + 5b function, per register §2 — arity 14/14 verified). **13 isotope losers RETAINED** (457 reps + 13 losers = 470); nothing deleted.

**Isotope-depth histogram (SUPPORT — trivial, as reshuffle predicted):** depth-1 = **445** cells · depth-2 = **11** · depth-3 = **1** (the `poe1` totem/cooldown/apply→detonate triple). 445+22+3=470 kits; 445+11+1=457 cells.

**Unknown/blank-slot cells:** 49 kit-rows carry ≥1 literal `unknown`/`blank` slot → **45 cells** (guardrail #3: literals preserved, never merged on absence).

**Representative-selection SQL (FINALIZED pending gandalf confirm — §6 tiebreak):**
`ROW_NUMBER() OVER (PARTITION BY cell_key ORDER BY era_span DESC, era_year DESC, tier_rank DESC, kit_id ASC)`, rnk=1 = representative. longevity=`era_span` (era-segment count in `canon_corpus.eras`) · recency=`era_year` · quality=`canon_tier` rank · deterministic floor=`kit_id`. Deprecated `mobile_*` NOT used. `skill_debut_year` unusable (7/470 populated) → `era_span` substituted. **gandalf one-line confirm PENDING** (spec-required checkpoint; request routed at `gandalf/requests/2026-07-13-gamora-rep-selection-sql-confirm.md`; artifacts non-destructive, re-run trivially via `generate_outputs.py` if amended).

**★ Near-twin-per-coord aggregate (THE headline — 92 Hamming-1 pairs, RANKED descending):**

| rank | coord | pairs | class |
|---|---|---:|---|
| 1 | **#4 geometry** | 17 | demotable |
| 1 | **#7 economy_model** | 17 | demotable (contentious) |
| 3 | #5b ctrl_function | 14 | never-demote core |
| 4 | #6 defense | 13 | demotable |
| 5 | #3 amp | 7 | demotable |
| 6 | #1 movement · #9 range · #10 tempo · #13 dependency | 4 each | mixed |
| 10 | #11 commit · #12 activation | 3 each | mixed |
| 12 | #8 proxy | 2 | core |
| 13 | **#2 delivery · #5a ctrl_treatment** | **0** | core (perfect identity partition) |

**Texture-vs-identity read:** shape is flat-topped — NO runaway texture coord (gandalf's "312-pair" illustration does not occur; the strict-14 key is near-orthogonal). Cleanest wholesale demote candidates: **#4 geometry** (same-delivery shape variants — register already flags "refine within #2") and **#3 amp** (low swap-diversity). **#6 defense** demotable with a glass~tank survivability caveat. **#7 economy_model is SPLIT-THE-VALUES, not demote-whole** — generator-spender / self-cost / reserve are build-defining (a Fury barb ≠ a spend-pool kit), while `spend~unknown` / `cooldown~finite` swaps read as texture; a blanket #7 demote would wrong-merge. **#5b ctrl_function** high (14) but that count is IDENTITY doing its job (`has-control ~ none` forks are real build differences) — keep. **#2 delivery & #5a treatment = zero near-twins** — strongest evidence for their never-demote status. #9/#10/#11 too few (3–4) to drive a confident call.

**Collapse-structure report (evidence packet for the Stage-2 review):** `agentic_orchestration/gamora/analyses/2026-07-13-cell-key-dedup-v1/collapse-structure-report.md`. Data artifacts alongside: `cell_table.csv` · `isotope_depth_hist.csv` · `near_twin_pairs.csv` · `near_twin_percoord.csv` · `generate_outputs.py` (reproducible).

**Round-trip:** N/A — read-only over elrond's corpus.db curation layer; no engine schema / fight_log / loadout / export contract touched. **Auto-committed** (`e00f4151`); **NO push** (Matt-gated per ADR-006).

**STOP confirmed:** no coord demoted, no coarsening. Stage-2 coarsening is the cluster review (gandalf + gamora + Matt), ruled against the §4 near-twin aggregate. Holding at the gate.
