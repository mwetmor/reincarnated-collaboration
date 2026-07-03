# §8 Curation shortlist prep — W3 batch 1 (700-kit bundle)

> **Authored:** knight-rider, 2026-07-03, at W4 close. Axes per gandalf W4 DRIFT-CRITIC verdict (`gandalf/notes/2026-07-03-w4-drift-critic-verdict.md`); population facts Disc #11-verified against the bundle-of-record.
> **Bundle-of-record:** engine `src/reincarnated/output/w3_batch1_bundle.json` @ tag `star-lord/v-demo-run-w3-emission-batch1-2` (`2839caf`) · registry run `cbeb9471` · 700 kits @ 38.9% yield.
> **This is PREP, not the final roster pick.** Final per-seat picks fire after (a) the LLM flavor pass (parked-resumable; scope question with Matt) and (b) Matt's summoner ruling (`canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`).

## Two-part deliverable (gandalf structure)

**Part 1 — 7 non-summoner seats: READY NOW, one seat per BC cell** (the only true mechanical differentiator; cells map 1:1 onto the ~7-8 non-summoner roster seats):

| Seat | BC cell | Candidates | Notes |
|---|---|---|---|
| 1 | melee_high_flat_str | 100 | |
| 2 | melee_low_spiky_str | 100 | |
| 3 | melee_medium_variable_str | 100 | |
| 4 | mid_high_flat_dex | 100 | only mid-range cell |
| 5 | ranged_high_flat_dex | 100 | |
| 6 | ranged_low_spiky_dex | 100 | |
| 7 | ranged_low_spiky_str | 100 | |

**Part 2 — 2-3 summoner seats: MATT-GATED.** Both certified melee summoners (`demo_bone_acolyte`, `demo_crypt_lieutenant`, propagation-live re-cert PASS) are the only certified candidates; whether they seat as `curated-not-emitted` (Option 2) or wait for batch-2 emission (Option 1) is exactly Matt's open ruling. No ranged summoners exist anywhere.

## Selection axes (per gandalf; in priority order)

1. **PRIMARY — BC cell** (one seat per cell; mechanical distinctness guaranteed)
2. **SECONDARY — element within cell.** Empirical spread (KR-measured, skill-level `canonical_element`): mono-physical 321 · mono-fire 255 · mixed pairs ~124 (holy/water/shadow/wind/lightning/earth × physical, fire×lightning, …). **82% of the population is mono-physical or mono-fire** — prefer the mixed-pair tail per cell for roster element diversity. (Fire over-representation echoes the known selection-bias sidecar finding.)
3. **TERTIARY — name/flavor** (deferred until the LLM pass; `name`/`flavor_text` None by ruled park-state — assembler docstring "Demo-scope decision: accept null names").

## Known caveats riding into curation

- **Geometry is cell-locked** (gandalf): within a cell all 100 kits share one geometry — within-cell abundance is skin not shape; the between-cell axis carries the differentiation. (III.4 "reskins" concern, surfaced early, not a batch-1 defect.)
- **Cells are a diagonal slice, not a grid** (no mid-STR, no ranged-variable).
- `archetype_tag`/`role_orientation`/`dominant_element` top-level fields are None — *derivable-but-unpopulated* (`derive_archetype_tag` exists in `cycle14_wave5_emitter`); cheap star-lord follow-on if curation tooling wants them. Not blocking (cell is the primary axis).
- **§8 "≥1 CONVERGENCE kit": DEFER to batch 2, don't drop** (gandalf re-interpretation ratified into this prep) — structurally impossible in solo batch 1; forcing it would fabricate a nonexistent kit.
- `proxy_dominant` tags sidecar: `src/reincarnated/output/w4_g4_proxy_dominant_tags.json` (gamora; all-zero in batch 1, structural).

## Empirical criteria that re-engage the final pick

1. Matt's summoner ruling (Option 1 vs 2) → Part 2 seats resolve.
2. Flavor-scope ruling (all 700 vs shortlist-first) → tertiary axis becomes usable.
3. If shortlist-first: KR fans per-cell finalists (3-5 per seat, mixed-element preferred) → flavor those → Matt picks.
