# Dispatch — 2026-07-13 — gamora — Cell-key dedup v1 (⛔ BLOCKED on elrond materialization)

**From:** knight-rider (sequencing)
**To:** gamora (simulation seam — dedup/matchup consumes the cell key per register §7)
**Spec author:** gandalf (register §6.1 Stage 1 + §7)
**Status:** ⛔ **HARD-BLOCKED.** Do NOT launch until elrond's `2026-07-13-elrond-cell-key-materialization.md` carries a completion record confirming `cell_key` is serialized and `GROUP BY`-able for the 470 combat-kit rows. KR brokers the gate — gamora launches only after KR confirms elrond is done. Launching early = `GROUP BY` on a non-existent/partial column.
**Pattern:** B (analysis over corpus.db; own session memory)
**Approved by:** Matt 2026-07-13 (§6.1 ratified: strict-13 first; dedup v1 = strict `GROUP BY cell_key`). This is execution of the ratified key — no new design decision inside this dispatch.

## Context

The cell key is ratified (register §6.1) and (once elrond completes) materialized as a serialized `cell_key` on `canon_engine_key`. Dedup v1 is deliberately the **maximally-split** start: strict exact-match on the full 13-tuple. It **never wrong-merges** — a later Stage-2 split/coarsen is cheap; a wrong early merge is a re-key (§6.1: split-late beats merge-wrong; the isotope/early-chemistry model). The output of Stage 1 IS the evidence that drives the Stage-2 coarsening review — the grain is *measured*, never guessed.

## Required reading before starting

- `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6/§6.1 (ratified key + isotope/tiebreak model) + §7 (your consumer contract).
- elrond's completion record on `dispatches/2026-07-13-elrond-cell-key-materialization.md` (the `cell_key` contract you consume — storage mechanism, row scope, unknown/blank footprint).

## The build

- **Dedup v1 = strict exact-match `GROUP BY cell_key`** over the 470 `row_class='combat-kit'` rows → **cells** (each distinct `cell_key` = one mechanical "element") + **isotope stacks** (kits sharing a fully-resolved cell = true variants, retained, never deleted).
- **Representative-selection rides the §6 tiebreak — grain-independent, no new decision:** longevity of lineage across games → recency → primary. Losers are **kept as mouseover "isotopes,"** never deleted (breadth is the pitch).
- Report the **collapse structure**: cell count vs 470 rows, isotope-stack size distribution, the largest cells, and any cell whose members carry `unknown`/`blank` slots (candidates the strict key kept apart on absence — informs Stage-2).

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
