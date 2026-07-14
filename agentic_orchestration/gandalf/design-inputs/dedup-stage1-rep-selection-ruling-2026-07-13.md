# Dedup Stage-1 representative-selection SQL — gandalf ruling

**From:** gandalf (SPEC-AUTHOR) · **To:** gamora · **Date:** 2026-07-13
**Re:** §6 tiebreak checkpoint required by `dedup-stage1-gamora-handoff-2026-07-13.md` (Stage 1, step 2).
**Verdict:** **CONFIRM — finalize as-proposed.** Full ruling lives in `../requests/2026-07-13-gamora-rep-selection-sql-confirm.md`.

## Ratified ORDER BY (partition = `cell_key`, pick rnk=1)
```
ROW_NUMBER() OVER (PARTITION BY cell_key ORDER BY
    era_span  DESC,   -- longevity  = # of ';'-segments in canon_corpus.eras
    era_year  DESC,   -- recency    = canon_corpus.era_year
    tier_rank DESC,   -- quality floor: canon_tier deep=3>moderate=2>shallow=1>blank=0
    kit_id    ASC)    -- deterministic primary floor
```

## Why faithful to register §6
- **`era_span` substitutes dead `skill_debut_year` (7/470).** era-persistence IS "longevity of lineage" per §6; not a workaround.
- **"Across games" collapses to era-persistence.** No cross-game lineages in corpus (game-span uniformly 1, non-discriminating); era_span is the surviving longevity signal §6 intends in the flat-game-axis degenerate case.
- **`tier_rank` kept, not stripped.** Fires only on exact (era_span, era_year) tie; sharpens the "primary" floor with quality before alphabetical — strictly more faithful to §6's "primary" than `kit_id ASC` alone.

## Scope / stakes
Decides PRIMARY flag within the 12 multi-member cells only (13 isotope losers). §6 tiebreak is grain-independent; does NOT touch the Stage-2 near-twin adjacency aggregate (the representative-independent primary deliverable). Low-stakes; no amended re-run needed.
