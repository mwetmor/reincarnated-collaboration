# Dispatch — 2026-07-13 — gamora — Cell-key dedup v1 (⛔ BLOCKED on elrond materialization)

**From:** knight-rider (sequencing)
**To:** gamora (simulation seam — dedup/matchup consumes the cell key per register §7)
**Spec author:** gandalf — **authoritative build spec:** `agentic_orchestration/gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md` (register §6/§6.1/§8). Build straight off it; this dispatch is the sequencing wrapper.
**Status:** ✅ **GATE CLEARED — launch-ready, pending Matt's go.** elrond materialization COMPLETE + KR-verified 2026-07-13 (commits `2a02ed0d`/`6c726afd`): `cell_key` is a materialized column, `GROUP BY`-able, 470/470 combat-kit rows keyed (system-records NULL), all 4 keyed columns + `resource_verbatim` populated, #5 two-slot confirmed, unknown/blank preserved as literals. The "no-blind-chain checkpoint" (gandalf `ea4f18a1`, KR-owned) is CLEARED — arity/coverage/enum-distribution/spot-rows all verified against the live DB. Nothing technical gates this now; Matt owns the launch go.
**Pattern:** B (pure data analysis over corpus.db — a `GROUP BY` + a Hamming-1 scan; ~470 rows. NOT a sim run: no gauntlet/batch/cert/compute campaign.)
**Approved by:** Matt 2026-07-13 (§6.1 ratified: strict-13 first; dedup v1 = strict `GROUP BY cell_key`). This is execution of the ratified key — no new design decision inside this dispatch.

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
_(append: cell count vs 470; isotope-stack distribution; representative-vs-isotope counts; unknown/blank-slot cells; path to the collapse-structure report for the Stage-2 review)_
