# Dedup Stage-1 → gamora handoff (strict cell_key dedup + Stage-2-readiness outputs)

**From:** gandalf (SPEC-AUTHOR) · **To:** gamora (execution), via knight-rider · **Date:** 2026-07-13
**Canon:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6 (dedup + isotopes) + §6.1 (ratified strict-13-first) + §8 (gamora hook).
**HARD GATE:** consumes elrond's materialized `cell_key` (`cell-key-materialization-elrond-handoff-2026-07-13.md`). **Do NOT start until `cell_key` exists AND has been verified** (KR owns the verification checkpoint).

---

## What this is
Dedup v1 = **Stage 1** of the ratified two-stage key (§6.1): strict exact-match on `cell_key`. PLUS the output artifacts that make the Stage-2 coarsening review a data call instead of hand-waving. This is **pure data work** (~470 rows) — a `GROUP BY` + a Hamming-distance-1 scan. It is **NOT a sim run**: no gauntlet, no batch, no cert instrument, no compute campaign.

## Input
- **`cell_key`** (elrond-materialized, verified). 14 value-positions (13 coords; #5 = treatment + function). Unknown / blank = literal value.
- **Representative-selection support columns:** `canon_corpus.{lineage, eras, era_year, skill_debut_year, game, canon_tier}`. **Do NOT use the deprecated `mobile_*` fields** (`mobile_representative` / `mobile_rank_in_cell` / `mobile_key_group` — mobile scaffold, DEPRECATED per register §0).

## Stage 1 — strict dedup (the run)
1. **Cells = `GROUP BY cell_key`.** Each distinct `cell_key` = one cell; its members = the kits sharing it = **isotopes.**
2. **Representative per cell = the §6 tiebreak:** longevity of lineage across games → recency → primary. Losers are **retained as isotopes, never deleted** (breadth is the pitch). *Operationalization note:* the §6 rule is canon; the column-math is yours to draft — e.g. longevity ≈ distinct-game span or earliest `skill_debut_year`; recency ≈ max `era_year`. Propose the exact SQL and **confirm with gandalf** before finalizing (one line).
3. **No coarsening, no merging beyond exact match, no deletion.** Strict only.

## Stage-2-readiness OUTPUTS (the design-relevant part — this is why the spec is mine)
Emit three artifacts that turn the Stage-2 coarsening decision from a guess into evidence:

1. **Cell table:** `cell_key` · representative `kit_id` · isotope member `kit_id`s · population count.
2. **Isotope-depth distribution:** histogram of cell populations (how many cells at depth 1, 2, 3, 4+). This answers "did strict-13 collapse meaningfully, or is it ~470 flat cells?" — the shape of this histogram is the first thing the cluster review reads.
3. **★ Near-twin adjacency view (THE Stage-2 driver):** all pairs of cells whose `cell_key`s differ in **exactly one** of the 14 positions, annotated with *which* coord differs and the two values. Then **aggregate: count near-twin pairs per differing-coord.** The coord with the most near-twin pairs is the strongest demotion candidate — e.g. "312 near-twin pairs differ only on #10 tempo" → tempo is behaving as texture; demote it and those 312 pairs collapse into their partners. This aggregate is the empirical object §6.1 Stage-2 rules on.

## The stopping point (Matt gate)
Stage 1 + the three outputs run **autonomously** — pure execution, no Matt gate. Then **STOP.** The **Stage-2 coarsening decision** (which coords to demote from cell-defining to isotope-distinguishing) is the **cluster review = gandalf + gamora + Matt**, ruled against the near-twin aggregate (§6.1). Do NOT demote anything in Stage 1. Report the three outputs and hold.

## Guardrails (non-negotiable)
1. Strict exact-match only; **never** pre-coarsen (§6.1 — split-late beats merge-wrong).
2. Never delete a loser — isotopes retained (breadth is the pitch).
3. Unknown / blank = literal `cell_key` value (elrond's serialization should already guarantee this — verify on read).
4. Data work, not sim — no gauntlet / batch / cert instrument touched.
