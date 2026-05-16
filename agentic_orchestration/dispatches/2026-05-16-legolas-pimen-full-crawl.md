# Dispatch — 2026-05-16 — legolas — Pimen full catalogue crawl

**From:** knight-rider
**To:** legolas (Mode B — systematic catalogue crawl)
**Approved by:** Matt at 2026-05-16 (Day 4 open)
**Status:** COMPLETE
**Estimated effort:** 1-3 sessions (depends on Pimen catalogue size — sample suggested ~20 packs visible from the eight element-spell series alone; full creator catalogue likely ranges from 50 to a few hundred packs across VFX + character + enemy + UI/icon assets)
**Acceptance:** `research/catalogue/pimen/full-2026-05-16.jsonl` complete; per-asset metadata aligned to the sample's field set; sample's 20 rows folded into the full file OR explicitly kept separate (your call — document which).

## Context — why now

Pimen's three-track viability gate **PASSED** on 2026-05-16:
- **Gandalf (design)** — PASS. Pimen IS the locked HD-2D-shaped pixel-art register (not adjacent-to — it IS). Paid tier-03+ packs are reference-grade.
- **Elrond (structural)** — PASS WITH FLAGS. v1.0 catalogue schema accepts representative-row inserts; four curation-pipeline pre-processor rules needed before live curation (not schema rework).
- **Drax (wiring)** — PASS WITH FLAGS. Two must-haves: RAR-unpack step in ingest pipeline; frame-assembly step for individual-frame packs. One nice-to-have: per-animation canvas metadata.

Matt's Day-4 directive: **full crawl, immediately.** Score-don't-filter principle applies (per AGENTS.md 2026-05-16 — Pattern 3). Crawl the full catalogue at Pimen; let the locked style register become a *consumption-time filter*, not a crawl-scope constraint. Capture everything Pimen produces, tag accurately, defer curation to elrond.

## Scope — full catalogue

Crawl the entire Pimen creator catalogue on itch.io. Specifically:

- **All element-spell-effect packs** beyond the sample-phase 8 elements — Pimen continues to release new element series, plus follow-on variations (e.g., spell effect 04, 05 for already-covered elements). Capture every one.
- **All character and enemy asset packs** — including the `fantasy-platformer-character` and `fantasy-skeleton-enemies` sampled previously, plus any additional character/enemy work in Pimen's catalogue.
- **All status / buff / debuff VFX packs** — the sample captured pack 01; Pimen reportedly has packs 02-09 in the series. Capture all.
- **All hit-effect / battle-VFX packs** — sample captured `battle-vfx-hit-spark`; capture sibling packs.
- **All mega/bundle packs** — capture with bundle-membership metadata so cost analysis downstream can map bundle items to constituents.
- **UI / icon / utility packs** — if Pimen produces any (e.g., elemental icons appeared in the mega-bundle); capture as `category: ui` or appropriate.
- **Anything else Pimen has released** — environment sprites, tilesets, audio, miscellaneous. The principle: if it's on Pimen's itch.io creator page, it's in scope.

## Required metadata per asset

Maintain the same field set used in the sample (`research/catalogue/pimen/sample-2026-05-16.json`):

- `asset_id`, `source` (`"itch-pimen"`), `url`, `name`, `category`, `dimensionality`, `style_register`, `style_tags`, `decomposition`, `file_format`, `license`, `cost`, `crawl_date`
- Pimen-specific: `pimen_element` (or null for non-element-typed assets)
- Six rubric axes per `research/curated/catalogue-rubric-schema.md`: `resolution_band`, `palette_size`, `shading_technique`, `linework_style`, `animation_frame_density`, derived stylistic register (axis 6)
- `extraction_notes` — free-text per row for anything you can't capture structurally (notable creator notes, decomposition surprises, sub-register uncertainty, etc.)

**Key signals to flag in `extraction_notes` (per elrond curation pipeline pre-processor expectations):**

1. **Sub-register uncertainty** — flag any pack where you can't confidently assign `hand-drawn-pixel` vs `retro-pixel-art` without visual inspection. (Elrond's rule R5 derives sub-register from rubric axes; your inputs should be honest about uncertainty.)
2. **Multi-element / bundle membership** — if a pack is a bundle or sub-pack of a bundle, name the parent bundle in `extraction_notes` and use `pimen_element: "multi"` if applicable.
3. **Decomposition surprises** — most Pimen character/enemy assets are monolithic. If you encounter any that ship Aseprite source files with separated layers (the sample's `mega-pack-elemental-spell-effects` did), flag prominently — these enable per-layer wiring for drax and are operationally significant.
4. **Canvas-shape non-square** — note any pack where canvas sizes are notably non-square (e.g., `32x48`, `72x32`). This is drax's flagged wiring concern.
5. **Includes-enemy-character flag** — the sample's `earth-spell-effect-03` bundled an Earth Elemental enemy alongside spell VFX. Any pack that mixes categories should be tagged `includes-enemy-character` (or `includes-character`) in `style_tags` so elrond's curation can split or cross-reference correctly.

## Output format

JSON Lines (one JSON object per line) at: `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl`

**Disposition of the sample file:**
- Recommended: keep `sample-2026-05-16.json` as historical record; have `full-2026-05-16.jsonl` be the authoritative cumulative file with the sample rows re-crawled (since the sample is several days old and may have minor data updates). Document this choice at top of the full file or in a sibling `README.md` in the pimen folder.
- Alternative: append to the sample file or symlink — your discretion. Document whichever choice you make.

## Required reading

- `~/.claude/agents/legolas.md` — your own definition, especially Mode B field spec + score-don't-filter principle
- `agentic_orchestration/research/commissions/2026-05-16-legolas-pimen-mode-b-sample.md` — your prior sample commission (the structural template for this work)
- `agentic_orchestration/research/catalogue/pimen/sample-2026-05-16.json` — your own sample output (20 rows; reference for field-population pattern)
- `agentic_orchestration/research/curated/catalogue-rubric-schema.md` (elrond) — the six-axis rubric definitions and the derived-sub-register rule
- `agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md` — elrond's structural verdict with the four pre-processor rules
- `agentic_orchestration/qa/findings/2026-05-16-drax-pimen-sample-wiring-review.md` — drax's wiring verdict with the RAR / frame-assembly / per-animation-canvas asks
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` — gandalf's design verdict
- `canonical/story/style-register.md` — for tagging context only; score-don't-filter — do NOT scope-restrict by it
- `agentic_orchestration/CHANGELOG.md` 2026-05-16 entries on viability gate + score-don't-filter (pattern context)

## Constraints

- **Read-only across all sources.** Public itch.io pages only. Respect robots.txt; default 1 request per 2 seconds rate-limit.
- **No fabrication.** Null + flag in `extraction_notes` if a field is genuinely unknown. Do NOT guess license, cost, or rubric axes.
- **Cost field accuracy is critical** — capture exact price, currency, bundle pricing where applicable, and any noted sale state at crawl time. Elrond will do cost/coverage KPI work downstream; data accuracy gates it.
- **No asset downloads.** Metadata extraction only. URLs in the output are sufficient. Drax + elrond will handle acquisition decisions and ingest separately.

## Out of scope

- **Other catalogue sources.** CraftPix, CreativeKind, Elthen, LuizMelo, etc. Even if Pimen's pages link to them — don't follow. One source per commission. Other sources get separate dispatches once Matt scopes them.
- **Curation.** Raw extraction only. Tagging the six rubric axes per asset based on Pimen's stated metadata + your inspection of the page is the boundary. Elrond curates downstream — the four pre-processor rules are *their* work, not yours.
- **Schema design changes.** If you notice a Pimen-specific metadata pattern the schema doesn't capture cleanly, flag in `extraction_notes` and surface to knight-rider; do NOT extend the schema unilaterally.
- **Acquisition recommendations.** Do not recommend buy/skip per pack. That's a downstream Matt + Elrond decision based on the full catalogue analysis.

## Open questions for legolas to resolve during the crawl

- **Catalogue scale estimate.** Once you have the full crawl planned, estimate the row count and report back early. If the catalogue is much larger than expected (e.g., >500 rows), check in with knight-rider on whether to batch the output across multiple sessions or commit to one long run.
- **Crawl ordering.** Suggest: largest-to-smallest by pack content (paid tier-03+ first for design-grade exemplars), or chronological by Pimen's release date (newest first), or thematic by element group. Your call — pick one and document.
- **Updated info for sample-included packs.** Some packs in your sample may have been updated since 2026-05-12. Re-crawl them as part of the full crawl and document any deltas (price changes, new animations added, etc.) in `extraction_notes`.

## Cross-references

- `agentic_orchestration/AGENTS.md` § Viability-gate workflow + § Score-don't-filter
- `agentic_orchestration/CHANGELOG.md` 2026-05-16 entries

## Acceptance criteria

- [x] Full Pimen creator catalogue crawled
- [x] Output at `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl`
- [x] Six rubric axes populated where confidently inferable; nulled + flagged otherwise
- [x] Sample-file disposition documented
- [x] Crawl-statistics summary in `agentic_orchestration/research/catalogue/pimen/README.md`
- [x] Knight-rider notified at completion: row count, notable surprises, readiness signal for elrond curation pipeline

---

## Completion record

**Completed:** 2026-05-16
**Output path:** `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl`
**Row count:** 46 (catalogue page estimated 45; actual enumeration is 46 distinct packs)
**Coverage summary:** 44 VFX / 1 enemy / 1 character. 10 spell elements covered (fire/water/earth/wind/thunder/ice/dark/holy/acid/wood) each with tier-01 through tier-03 packs where released; 2 mega-bundles; 9 buff/debuff status VFX packs; 3 battle VFX packs; 4 smoke/dust ambient packs; explosion; halloween seasonal; 3 early/legacy packs. 19 free / 27 paid.
**Notable surprises:**
- Two packs are CC-BY 4.0 (require attribution): `pixel-battle-effects` and `cutting-and-healing`. All other 44 packs are commercial-royalty-free.
- Buff/Debuff Pack 09 is 24x24 canvas (retro band), distinct from packs 01-08 which are 48-64px (hd2d-pixel). Likely different style register tier.
- Battle VFX Projectile at 12x12 (tiny band) — delivered as ZIP not RAR (no unpack step needed).
- 13 of 46 packs include Aseprite source files (enables layer-separated wiring for drax).
- Earth Spell Effect 03 bundles a full Earth Elemental enemy character alongside spell VFX (tagged `includes-enemy-character`).
- 20 rows have `resolution_band: unknown` — free/early packs with no canvas size documentation; visual inspection required at curation.
- Multiple non-square canvases across dark, smoke, wood, buff packs — drax canvas-padding concern documented per-row.
**Notes for elrond / drax / knight-rider:**
- Elrond: 20 rows with `resolution_band: unknown` plus `palette_size/shading_technique/linework_style: unknown` on all 46 rows — visual inspection pass required to fill rubric axes 1-5 before axis-6 derivation. Four curation pre-processor rules (from prior structural review) still apply.
- Elrond: Earth Spell Effect 03 frame count discrepancy between sample and re-crawl — verify at acquisition.
- Elrond: Mega Pack 01 Aseprite status unclear (sample said included; re-crawl found no confirmation) — verify at acquisition.
- Drax: Buff/Debuff Pack 01 does NOT include Aseprite files (packs 02-09 do).
- Drax: Non-square canvas packs flagged inline with `drax canvas-shape flag` in extraction_notes — check before atlas packing.
- Drax: Battle VFX Projectile (12x12) delivered as ZIP not RAR — simpler pipeline for this specific pack.
- Knight-rider: Elrond curation pipeline dispatch not yet authored (pre-processor rules from prior structural review are the prerequisite).
