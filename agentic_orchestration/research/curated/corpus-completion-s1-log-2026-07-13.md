# Corpus Completion S1 Log — 2026-07-13

**Author:** elrond
**Date:** 2026-07-13
**Authority:** gandalf wind-down §3 (`agentic_orchestration/gandalf/notes/2026-07-13-wind-down-corpus-to-demo-pipeline-resume.md`)
**Script:** `agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py`
**DB:** `agentic_orchestration/research/curated/corpus.db` (gitignored, schema_meta 2.1)
**MIGRATION entry:** v2.1

---

## 0. One-line intent

ONE data-completion rebuild carrying five payloads. Additive columns only — **zero row-count change** (524 / 4,780 / 478 / 45 hold). Every backfill traces to an ENGINE or probe source of record; where source is genuinely absent, **honest-NULL — never invented.**

## 1. D6 rebuild sequence (two committed scripts)

```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py        # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py  # S1 completion (idempotent)
```

Both deterministic. The completion pass is idempotent (`ADD COLUMN` pragma-guarded; pure-UPDATE backfills). Clean rebuild → byte-identical state. corpus.db stays gitignored; the two scripts + this log + the MIGRATION v2.1 entry are the committed truth.

## 2. Per-payload fill census

### P1 — roster_atlas (45 kits)

| Column | Source | Filled | Honest-NULL |
|---|---|---|---|
| `amp_val` | expand atlas amp code (S/F/V → spiky/flat/var) | 26/45 | 19 (undeclared `_` — B*/H*/K26–K29) |
| `commit_val` (+`commit_provenance`) | expand atlas commit code (W/I/C → wind-up/instant/channel) | 5/45 | 40 |
| `mob_policy_while_casting` | — | 0/45 | 45 |

- **amp_val (26/45):** all 26 CellDef-family kits (K1–K25 incl. K9c/K9f, K13). Validated **25/26 exact** against `bc_target_cell_sampler.py` CELL_DEFINITIONS amplitude. Sole divergence: **K9f** (`flat` vs cell9 target `var`) — the legitimate "fired-leg" engine emission; kept as-emitted, not overridden (reversibility: raw `amp` code preserved). The 19 NULLs are bench (B4–B12), hypothesis (H1–H6), and lineage-only (K26–K29) kits whose atlas amp code is `_` (undeclared).
- **commit_val (5/45):** the only kits carrying an explicit atlas commit code —
  - `celldef-pin`: K1=wind-up, K7=instant (snap), K19=channel
  - `roster-atlas-v1-engine`: B12=channel, H6=wind-up
  - The 40 NULLs: commitment is **rolled at generation (S7)** for unpinned cells (`bc_target_player_class.py` default `commitment="snap"` is the neutral leg, not a fixed pin) → honest-NULL, never snap-invented.
- **mob_policy_while_casting (0/45):** genuinely absent at S1. Movement policy is emitted **per-skill at S7** (`per_skill_emitter.py` `_MOVE_ROOTED/_MOVE_WALK/_MOVE_FULL`), not a static roster config. All 45 → NULL. **This contradicts the commission's assumption** that engine sources carry roster movement (Discipline #11 finding).

### P2 — canon_engine_key.delivery_value

- **478/478 filled** (100% coverage) — promoted from probe `delivery.value`.
- **Cone Path-2 split reproduces EXACTLY** (the ruled Q19 split):
  - **BEAM (5):** gd-flames-of-ignaffar-purifier, hot-dragons-breath, hot-exterminator-burn, poe1-incinerate, ud-flamethrower-channel
  - **PROJECTILE (6):** di-multishot-dh, di-vengeance-strafe-dh, le-frost-claw, poe2-galvanic-shards, tl2-shotgonne-outlander, tq-ternion-bone-charmer

### P3 — 6 poe2 movement-unknowns (census only, no schema change)

All 6 remain `mob_policy_while_casting='unknown'` in engine-key. Re-checked probe facts + megaprobe re-probe: unresolved in every source. Honest-NULL retained.

| kit_id | mob_policy_while_casting |
|---|---|
| poe2-spiral-volley | unknown |
| poe2-whirling-assault-ma | unknown |
| poe2-snipe-mirage-deadeye | unknown |
| poe2-walking-calamity | unknown |
| poe2-shaman-bear | unknown |
| poe2-archmage-totems | unknown |

### P4 — d2-wl-void-rift amp (census only, no schema change)

`amp_val = NULL` (amp_conf 0.27). atlas_key carries no amp code; probe/megaprobe supply no amp value. Honest-NULL retained — no source to backfill.

### P5 — canon_corpus.era_year + stabilization_patch

| Column | Source | Filled | Honest-NULL |
|---|---|---|---|
| `era_year` | per-game canonical release year (per-game-meta.jsonl `release_era`) | 524/524 | 0 |
| `stabilization_patch` | `current-X.Y` token, eras ∪ sources_used | 10/524 | 514 |

- **era_year (524/524):** documented per-game year table (`GAME_ERA_YEAR` in script; provenance = `release_era` field of per-game-meta.jsonl). All 19 games covered → all 524 kits filled. Raw per-kit `eras` column retained for finer signal.
- **stabilization_patch (10/524):** deterministic `current-(\d+\.\d+\+?)` extractor. All 10 hits are chronicon `current-1.52`. Sparse by nature; naming law omits the segment where absent (§7.1 refinement 5). **STEWARD SCOPE NOTE:** commission scoped this to `sources_used` (which yields 1 clean token); the richer signal is in the `eras` field (10 tokens). The extractor unions eras∪sources_used with provenance recorded. Flagged to gandalf for scope ratification (data-domain steward call; reversible; non-inventing).

## 3. Discipline #11 findings (empirical inspection over assumption)

1. **Roster movement genuinely absent at S1** — emitted at S7, not a static source. All 45 mob_policy NULL. (Contradicts commission premise.)
2. **Roster commit mostly rolled, not fixed** — only 5/45 have a fixed source; unpinned cells are rolled at S7. NULL, not snap-invented.
3. **Patch signal is in `eras`, not `sources_used`** — 10 vs 1. Steward scope expansion flagged.
4. **chronicon era-year source discrepancy** — `era_range` token `1.0-2020` vs `release_era` field `1.0 2021`. Chose 2020 (matches era_range + real-world release); flagged for Matt/gandalf.

## 4. Render-spec FLAGS to gandalf (follow-ups; NOT elrond's to change)

- **delivery_value column now exists.** `render_v1_2_stratified.py` (~line 116-119) still parses `json_extract(pf.facts_json,'$.value')` for delivery. It MAY now read `canon_engine_key.delivery_value` directly — schema-derivable, simpler. Render-spec change is gandalf's call.
- Roster placement is hardcoded UNMAPPED (movement-derived rows use engine-key movement, not roster columns), so the P1 backfill does not change render output — as expected/verified.

## 5. Verification (all gates passed)

- Row counts hold: 524 / 4,780 / 478 / 45.
- P2 cone split reproduces exactly (5 beam / 6 projectile).
- P1 amp validated 25/26 vs CellDef (K9f fired-leg divergence expected).
- V1.2 plane render reproduces from rebuilt DB (exit 0; 463 combat / 37 negative / 45 roster; cone Path-2 verified).

## 6. Reversibility

corpus.db is gitignored. Clean rebuild = base ingest + this completion script from committed inputs (v3 CSV + engine-key JSONL + probe JSONL + roster CSV + lineage JSONL + per-game-meta.jsonl). Raw columns (roster `amp`/`commit_slot`, `eras`) preserved untouched; all new columns derived at completion time. Output is byte-identical SQLite state.
