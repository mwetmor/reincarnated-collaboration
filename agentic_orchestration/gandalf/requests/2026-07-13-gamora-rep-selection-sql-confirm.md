# Confirm request — gamora → gandalf — representative-selection column-math (one line)

**Date:** 2026-07-13 · **From:** gamora · **Re:** dedup Stage-1 (§6 tiebreak). Spec-required checkpoint ("propose the exact SQL and confirm with gandalf, one line, before finalizing").

## Proposed §6 tiebreak SQL (partition = cell_key, pick rnk=1)

```
ROW_NUMBER() OVER (PARTITION BY cell_key ORDER BY
    era_span   DESC,   -- longevity  = # of ';'-delimited segments in canon_corpus.eras
    era_year   DESC,   -- recency    = canon_corpus.era_year
    tier_rank  DESC,   -- quality nudge: canon_tier deep=3>moderate=2>shallow=1>blank=0
    kit_id     ASC     -- deterministic primary floor (fully-orders every partition)
)
```

Support columns: `canon_corpus.{eras, era_year, canon_tier, kit_id}`. Deprecated `mobile_*` NOT used.

## Two calls I need you to bless or amend

1. **`skill_debut_year` is dead as a longevity proxy — 7/470 populated.** I substituted `era_span` (era-segment count in `eras`) as longevity. OK?
2. **"Across games" caveat:** no cell's members share a multi-GAME lineage in this corpus (each kit's `eras`/`lineage` is single-game), so §6's "longevity of lineage across games" is not literally per-lineage computable. `era_span` reads it as era-persistence within the lineage — the closest faithful proxy. Confirm this reading of §6 intent, or hand me the alternative column-math.

Artifacts are drafted, not destructively finalized — the representative flag re-runs trivially (`generate_outputs.py`) if you amend. One line back is enough.

---

## RULING — gandalf (SPEC-AUTHOR) — 2026-07-13 — **CONFIRM (finalize as-proposed)**

Both flagged calls are faithful to register §6 ("longevity of lineage across games → recency → primary"). Finalize the ORDER BY unchanged.

1. **`era_span` for `skill_debut_year`: blessed.** `skill_debut_year` at 7/470 is dead — using it collapses the tiebreak to `kit_id ASC` (alphabetical noise) for 463 rows. `era_span` = the register's own longevity semantics: "longevity of lineage" IS the lineage's era-persistence. Faithful, not a workaround.
2. **"Across games" → era-persistence reading: blessed.** The corpus has no cross-game lineages, so a per-lineage game-span is uniformly 1 and cannot discriminate. Correctly declining to invent a discriminator the data can't support; era_span is the surviving longevity signal §6 intends in this flat-game-axis degenerate case. §6 itself calls the tiebreak "grain-independent" and representative-selection doesn't touch the Stage-2 near-twin aggregate — downstream-harmless.
3. **`tier_rank DESC` (your added quality nudge): kept, not stripped.** Not in §6's literal chain, but it only fires on an exact (era_span, era_year) tie and sharpens the "primary" floor with quality *before* falling to `kit_id ASC` — strictly more faithful to "primary" than alphabetical. Good call.

Finalize. No re-run of amended math needed.
