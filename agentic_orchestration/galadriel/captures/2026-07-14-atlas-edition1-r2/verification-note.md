# Atlas Edition-I — render verification note (r2 amendment)

**r2 amendment (2026-07-14):** three CONTENT-LOCKED explainer texts added per spec §2 r2 clause
(Matt: "we need to add something somewhere explaining what the axes are") — pole glosses,
density-field legend line, derivation gloss. Same atlas.json input, same layout, same coordinate
set as the first render. Outputs land in `.../2026-07-14-atlas-edition1-r2/`; the first render
(`.../2026-07-14-atlas-edition1/`) is preserved as lineage.

**Rendered by:** galadriel/pipeline/atlas-edition1-render.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json
**atlas_version:** Edition-I · **basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T03:02:30.091239+00:00
**emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition1.py

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-14-atlas-edition1-r2/atlas-edition1-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-14-atlas-edition1-r2/atlas-edition1-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-14-atlas-edition1-r2/atlas-edition1-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-14-atlas-edition1-r2/atlas-edition1-archive.png`

## Point accounting
- active (supplementary=false): **469** — neutral 383 + grouped 86
- supplementary corpses: **37** (extrinsic-content-mix:2, extrinsic-itemization:5, extrinsic-no-lever:3, extrinsic-split-scaling:3, extrinsic-tuning:6, intrinsic-red:5, system-evidence:1, unknown-pending-recrawl:12)
- total: **506**
- condensation groups (labeled-member centroids):
  - WHIRLWIND: n=15, centroid=(0.8191, -1.0816)
  - TOTEM-SENTRY: n=24, centroid=(-0.7307, -0.3518)
  - TRAP-MINE: n=23, centroid=(-0.0982, 0.2171)
  - CHANNELED-BEAM: n=9, centroid=(1.1408, -0.2724)
  - AURA: n=8, centroid=(0.3458, -0.4282)
  - MINION-PET: n=7, centroid=(-0.1908, -0.9987)

## Acceptance tests
- [PASS] **point-counts** — active=469 (exp 469), supp=37 (exp 37), total=506 (exp 506)
- [PASS] **grouped-count** — grouped=86 (exp 86: 15+24+23+9+8+7)
- [PASS] **layout-equality** — identical coordinate fingerprint
- [PASS] **determinism** — instrument:byte-equal, archive:byte-equal
- [PASS] **R2-no-2.57-numeral** — clean (naive-box 2.57 absent as content; pixel-coord fragments excluded by boundary)
- [PASS] **R3-no-season-N** — clean
- [PASS] **RIDER-1-badge** — inertia_pct + retained_dims + structure_statement present both skins
- [PASS] **r2-pole-glosses** — all 4 pole glosses present both skins
- [PASS] **r2-density-legend-line** — density-field legend line present both skins
- [PASS] **r2-derivation-gloss** — derivation gloss present both skins
- [PASS] **continuum-single-terrain-fill** — terrain is one continuous fill (no discrete-region coloring)

## Smoke tests (orientation / axis-flip guards)
- [PASS] **WHIRLWIND x>0 (PERFORM)** — x=0.8191
- [PASS] **WHIRLWIND y<0 (EMBODY)** — y=-1.0816
- [PASS] **TOTEM-SENTRY x<0 (DEPLOY)** — x=-0.7307
- [PASS] **charged-dash near WHIRLWIND condensation** — poe1-charged-dash=(0.936,-0.909) dist=0.209 (< 0.848 = 20% diag)
- [PASS] **charged-dash is a corpse (supplementary)** — supplementary=true, death_class=intrinsic-red

## Layout calls made
- **Plane:** x=point.x, y=point.y; math y+ mapped to SVG top (LAUNCH up / EMBODY down). World bounds = min/max over ALL points (corpses in-frame) + 6% pad.
- **Axis end-labels:** x+ PERFORM (right), x- DEPLOY (left), y+ LAUNCH (top), y- EMBODY (bottom) — ratified names from basis.axis_names, orientation per prompt (no flip).
- **Continuum underlay:** Gaussian KDE of the 469 active kits on a 120x120 grid, bandwidth = 5.5% of each axis span, drawn as 6 translucent iso-bands in ONE terrain fill, blurred (stdDev 7) → smooth density with NO cell borders / NO grid / NO discrete-region coloring. Soft dashed zero-axes are orientation guides, not partitions.
- **Condensation anchors:** 86 grouped actives color-coded by 6 groups; one plaque annotation at each group's labeled-member centroid (annotation, never region outline). 383 unlabeled actives = neutral dots.
- **Graveyard (F-1):** 37 corpses as dagger (†) glyphs, inked by death-class; the 12 unknown-pending-recrawl carry an open dashed ring = their own visible class; each corpse individually titled + indexed. NEVER a shaded danger region.
- **Franchise:** never a visual encoding — SVG <title> payload only.
- **r2 explainer texts (CONTENT LOCKED; typography/placement per skin, quiet — never competing with the field):** (i) pole glosses — one clause under each of the four axis end-labels, bound to its pole; (ii) density-field legend line — appended to the CONDENSATIONS legend with a terrain swatch (full locked clause carried verbatim in a non-rendering <desc> so visual line-wrapping stays grep-clean); (iii) derivation gloss — one line under the RIDER-1 badge. instrument = upright sans; archive = serif-italic devlog register. All three grep-verified present on both skins.
- **Two skins, one layout engine:** instrument (quiet, mobile-legible) + archive (God's Archive gilt-on-dark). Skin-invariance proven by identical coordinate fingerprint (MATCH).
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal.

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not.
