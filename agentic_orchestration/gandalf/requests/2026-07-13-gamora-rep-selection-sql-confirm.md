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
