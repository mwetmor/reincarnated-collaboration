# Atlas Edition-I — render verification note (r6: plaque legibility + footer de-collision)

**r6 amendment (2026-07-15, spec §9.6):** STRICTLY-CORRECTIVE — the first corrective rN. Moves
existing chrome GEOMETRY; adds/removes/rewords NOTHING (ZERO-CONTENT LAW, §9.6.3). Fired by Matt's
directive ("fire the r6 legibility pass") on gandalf's DRIFT-CRITIC finding during r5 verification:
two byte-proven PRE-EXISTING chrome flaws (present since r3.2, surfaced by a 2× plaque crop) —
(1) the clip-disclosure line overran the plaque's right edge; (2) the footer census line overprinted
the sealed-ledger rows inside the plaque footprint. r6 fixes exactly these two, NOTHING else.

## r6 acceptance tally
- **ACCEPTANCE: 30/30 PASS** (0 fail) · **SMOKE: 16/16 PASS**
- **21 spec criteria (§7 #1-8 · §9.3 #9-12 · §9.4 #13-15 · §9.5 #16-17 · §9.6 #18-21): ALL COVERED, ALL PASS.**
  The test list carries 30 rows because several carried criteria are realised as multiple
  sub-checks (the §9.3.11 explainer-trio → 3 rows: pole-glosses/density-legend/derivation-gloss; §9.2.2
  continuum → `ghost-glyphs-not-regions`; §7 determinism/provenance → their own rows). Every one of the
  21 named criteria maps onto a PASS row; the four r6 criteria are the four `r6-*` rows below.
- r6 criteria: **#18 `r6-clip-wrap`** · **#19 `r6-footer-anchor`** · **#20 `r6-frozen-layer-regression-vs-r5`** · **#21 `r6-occlusion-guard`** (HALT-gate).

## r6 exact SVG diff shape vs r5 (both skins — direct line-set diff)
**2 hunks, 6 changed lines per side (−6 / +6):**
- **HUNK 1 — the GHOST FIELD ledger plaque block (5 lines → 5 lines; 5 changed each side):**
  1. **plaque `<rect>`** — `y=1066 height=134` → `y=1056 height=144` (grew UPWARD 10px; x=1144, width=360, bottom pinned at y=1200 unchanged).
  2. **GHOST FIELD header** — `y=1084` → `y=1074` (shifted up 10px; CONTENT byte-identical).
  3. **feasible/lit/unmapped line** — `y=1101` → `y=1091` (shifted up 10px; CONTENT byte-identical).
  4. **clip-disclosure line (FIX A)** — old single `<text x="1156" y="1115">…</text>` → new wrapped `<text><tspan y="1105">…</tspan><tspan y="1116">…</tspan><title>[full clip string]</title></text>` (2 rows + `<title>`; the `<title>` content is BYTE-IDENTICAL to r5's clip string).
  5. **beyond-horizon block** — tspans `y=1130..1163` → `y=1131..1164` (shifted; CONTENT byte-identical, `<title>` unchanged).
- **HUNK 2 — the footer census line (FIX B; 1 line changed each side):**
  6. **footer census** — `<text x="1504" y="1188" text-anchor="end">points:…</text>` → `<text x="1132.00" y="1188" text-anchor="end">points:…</text>` (re-anchored to plaqueRect.x−12; y + content + anchor UNCHANGED).
- **NOT in the diff (byte-frozen, confirmed):** all 469 point circles · all 7128 ghost-glyph circles · all 37 tombstone daggers · the horizon polyline + label · the headline pair + secondary · the explainer trio + RIDER-1 badge · **the sealed-ledger rows (y=1178/1192)** — these land at the SAME absolute y in r6 (ledY dropped 10, CLIP_ROW rose 10, net-zero), so they never enter the diff.

## r6 plaque geometry — before (r5) / after (r6)
| | r5 (before) | r6 (after) | Δ |
|---|---|---|---|
| plaque TOP edge y | 1066 | **1056** | −10 (grew UP) |
| plaque BOTTOM edge y | 1200 | **1200** | 0 (pinned, §9.6.2) |
| plaque height | 134 | **144** | +10 |
| clip line rows | 1 (unwrapped, overran) | **2** (wrapped, budget 62) | +1 |
| CLIP_ROW reservation (px) | 12 (fixed) | **22** (= 2×11) | +10 |
| footer census end-anchor x | 1504 (plaque RIGHT edge) | **1132.00** (plaqueRect.x−12) | −372 |

## r6 occlusion-guard (spec §9.6.4.21 — HALT-gate) — NO HALT
- **data-mark CENTERS inside the grown plaque rect [x 1144-1504, y 1056-1200]: 0** → guard PASSES (zero occlusion; no HALT).
- **nearest data-mark above the new top edge:** a settled point at y=1051.93 (cx=1180.51) → **margin = 4.07px** between the plaque top edge (y=1056) and the mark center.
- **judgment call:** the margin is 4.07px (positive, criterion defined on CENTERS). The settled point at y≈1052 is the one §9.6.4.21 warns about ("a settled point sits ≈y=1050 near the plaque's projected new top edge"). Its center + upper ~4px sit clear ABOVE the plaque; because the plaque can ONLY grow upward (down would hit the footer at y=1188, §9.6.2) and the growth is a mechanical 10px, the clearance is COMPUTED, not lucky — exactly what the guard makes true. The point's glyph (r=5.2) has ~1px of its lower rim behind the plaque's top border, but its center and the bulk of the mark remain fully legible; the guard's center-based criterion is the correct honesty test (a mark whose CENTER is readable is not occluded).

## r6 fixes — the two named diffs (spec §9.6.1)
- **FIX A — clip-line wrap (§9.6.1.a):** the §9.2.3 clip-disclosure line now flows through the SAME deterministic wrap the §9.5 beyond-horizon line uses — `wrapByChars(ghostClipLine, 62)` at font 9.5 → 2 `<tspan>` rows + the FULL contiguous string in a `<title>` on the parent `<text>`. The old single row (~100 chars) overran the ~348px usable plaque width from x=1156; it now wraps within budget. **Content byte-identical to r5's clip string — geometry only.** The plaque grows UPWARD by 10px to hold the extra clip row (bottom pinned; the r5 growth mechanism, §9.6.2).
- **FIX B — footer-census re-anchor (§9.6.1.b):** the right-anchored frame-footer census line ("points: 469 active + 37 corpse = 506 · …", y=1188) had its end-anchor at x=1504 — the plaque's RIGHT edge — so it printed leftward INTO the plaque footprint (x-range 1144-1504), overprinting the sealed-ledger rows at y=1178/1192. Re-anchored to **plaqueRect.x − 12 = 1132.00** (COMPUTED from the shared plaque x `GHOST_PLAQUE_X`, not a constant — the acceptance test parses the emitted `<rect>` x and asserts anchor == rectX − 12). y + content + `text-anchor=end` UNCHANGED. Mid-frame clearance vs the left footer line pre-verified by measure (left ends ≈x=550; census now starts ≈x=757 sweeping left from 1132.00).
- **Footer render-script string held FROZEN** (single-purpose-diff discipline, per r4/r5): the in-SVG footer still reads `render: galadriel/atlas-edition1-render-r3.mjs`. r6 provenance lives HERE + in the script filename (`atlas-edition1-render-r6.mjs`).

---

## (inherited) r5: beyond-horizon disclosure line

**r5 amendment (2026-07-15, spec §9.5):** STRICTLY-ADDITIVE — ONE microcopy line in the GHOST FIELD
ledger box (both skins), rendered DIRECTLY AFTER the clip-disclosure line (§9.2.3). Fired by Matt's
directive ("cut §9.5 and fire the r5 pass") after the chart's first reader hit the SECOND misreading
within one session of r4 going live: *"how can we have kits outside the ghost's meso area?"*. The r4
horizon label kills misreading #1 (dark beyond the line = mined-out); this line kills misreading #2
(kits beyond the line = paradox). **Rendered line (both skins), N computed from the render pass:**

> "14 settled kits stand beyond the horizon — kits project with all 14 coordinates; ghost cells carry the 7 core only (the strongest east pulls — cone/whirlwind geometry, channel commit — are invisible at meso grain)."

- **N = 14** — COMPUTED FROM THE RENDER PASS by a point-in-polygon test of all
  469 ACTIVE (`supplementary=false`) points against the **SAME world-space convex hull**
  the r4 §9.4.1 code computes (`ghostHullWorld`, 22 vertices) — ONE code path, ONE
  hull, NEVER a second hull, NEVER hard-coded. Boundary convention (spec §9.5.1): a kit exactly ON the
  hull edge counts as INSIDE (not beyond). N matches gandalf's independent computation (14: 10 WHIRLWIND
  + 3 CHANNELED-BEAM + 1 neutral, all `commit=channel`) — the render pass agrees, so no HALT.
- **Group profile of the 14 beyond-horizon kits:** CHANNELED-BEAM 3 · NEUTRAL 1 · WHIRLWIND 10.
- **Kit ids (beyond the hull, sorted):** `d2-bvc`, `d2-ww-barb`, `d2-ww-sin`, `d3-ww-wastes`, `di-whirlwind-barb`, `gd-eor-warlord`, `gd-flames-of-ignaffar-purifier`, `le-warpath-vk`, `poe1-cyclone`, `poe1-incinerate`, `tl1-alchemist-summoner`, `tq2-whirlwind-rogue`, `ud-flamethrower-channel`, `ud-whirlwind-str`.
- **Zero-case omission:** if no active kit lay outside the hull the line would be OMITTED entirely (no
  "0 kits") — same protocol as the clip line. Proven by the r5-beyond-horizon doctored all-inside test.
- **Supplementary points (tombstones) EXCLUDED** from N — the graveyard is its own register. (The 3
  easternmost points of the whole plane ARE dead channel kits — beyond the horizon by the same
  mechanism, already disclosed by their own tombstone layer.)
- The coordinate examples in the string (cone/whirlwind geometry, channel commit) are CONTENT-LOCKED
  disclosure copy — same class as the pole glosses (empirical facts about the frozen basis, loading
  ranks #2/#3, immutable within Edition-I) — carried VERBATIM.
- The exact contiguous string is carried in a `<title>` node so acceptance greps it whole (same
  pattern as the r4 horizon label). Every frozen layer — points, ghost glyphs, horizon polyline +
  label + marker, tombstones, headline callout, explainer trio, RIDER-1, AND the clip-disclosure line
  — is BYTE-FROZEN vs the r4 baseline; the ONLY diff is this one line (+ the plaque's downward shove
  to make room). Verified by DIRECT SVG diff, exactly like r4-vs-r3.2.

**Frozen-layer baseline (r5):** `agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon` (r4)

**r4 amendment (2026-07-15, spec §9.4):** STRICTLY-ADDITIVE chrome on top of the r3.2 render line,
fired by Matt's ratification ("I agree with all four") of gandalf's INTERIOR-1 memo review
(review-of-record: `agentic_orchestration/gandalf/design-inputs/2026-07-15-interior1-memo-review.md`).
INTERIOR-1 §3 (interior-aware placement) is REJECTED as specced; this amendment implements the memo's
§4 (horizon) and §6 (headline statistics) only. TWO changes, both skins:
  1. **GHOST HORIZON** — the convex hull of ALL 10,080 projected ghost positions (incl. the 21
     out-of-frame cells; the hull is of the lattice's REACH, then CLIPPED to the plane frame exactly
     like the ghost glyphs). Faint dashed envelope, chrome-weight, drawn BENEATH the ghost glyphs so
     it never reads as data. Mandatory label (exact string) placed adjacent to the EAST gap.
  2. **HEADLINE COVERAGE PAIR** — the coverage callout re-leads with two meso-grain statistics
     computed at render from emitted fields (lit_cells / meso_feasible, active / lit_cells). The
     exact-grain line (469 ≈ 6.8×10⁻⁵ % of 693,146,160) DEMOTES to a secondary flavor line.
Every frozen layer (points, tombstones, ghost glyph positions, sealed ledger, clip-disclosure line,
explainer trio, RIDER-1 badge) is BYTE-FROZEN vs the r3.2 baseline — verified by direct SVG diff:
the ONLY changes are the horizon chrome (added) + the re-led coverage callout (the old single line
replaced by two leads + the demoted secondary).

**r3 amendment (2026-07-15, spec §9):** the feasible-lattice GHOST FIELD renders as GROUND beneath
the settled points, fired by Matt's Q30 ruling (Q30a cut-predicate amendments ratified + Q30b zero
taste cuts). Data source: elrond ghost-field emission (`atlas.json` ghost_field block, commit
d0b2a025). EXTENDS the r2 render line: the 506 point positions, KDE terrain, condensation anchors,
graveyard tombstone layout, RIDER-1 badge, and r2 explainer trio are all FROZEN; the ghost layer is
strictly additive and drawn FIRST (bottom of stack). The 12 formerly-unknown tombstones now carry
emitted death_class verdicts.

**r3.2 amendment (2026-07-15, spec §9.2.3, r3.2/commit `7cf1eeca`):** gandalf's r3 verification verdict
was ACCEPT-WITH-ONE-AMENDMENT. The clip call on the out-of-frame ghost cells was correct (frozen plane
bounds; zero-mass ground never rescales the frame) but was disclosed only in this note — on the chart, the
GHOST FIELD ledger claimed all feasible cells without saying some project beyond the frame. §9.2.3 now binds:
any clip MUST be disclosed on-chart in the ghost ledger. FIX: a clip-disclosure microcopy line renders in the
GHOST FIELD ledger box (both skins); the count is COMPUTED FROM THE RENDER PASS (cells whose projected
position falls outside the plane rect), never hard-coded — it follows any future atlas.json change; if zero
cells clip the line is omitted entirely (no "0 clipped"). Acceptance suite gains `r3.2-clip-disclosure`.

**Rendered by:** galadriel/pipeline/atlas-edition1-render-r6.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json (unchanged, elrond d0b2a025)
**r6 frozen-layer baseline (primary check #20):** agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r5-beyond-horizon (r5)
**Inherited frozen-layer baselines:** r5-vs-r4 (2026-07-15-atlas-edition1-r4-horizon) · r4-vs-r3.2 (2026-07-15-atlas-edition1-r3-ghost)
**atlas_version:** Edition-I · **basis frozen:** 2026-07-14 · **inertia:** 8.36% · **retained dims:** 14
**emitted_at (from atlas):** 2026-07-15T04:37:20.241687+00:00
**emitter:** agentic_orchestration/research/scripts/build_atlas_json_edition1.py

## Outputs
- instrument: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r6-legibility/atlas-edition1-instrument.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r6-legibility/atlas-edition1-instrument.png`
- archive: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r6-legibility/atlas-edition1-archive.svg` + `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r6-legibility/atlas-edition1-archive.png`

## Ghost field accounting (spec §9, all from emitted fields)
- feasible meso cells: **10,080** (each {core 7-tuple, depth, kit_count, lit, x, y})
- lit by census: **192** · unmapped pending curation: **14**
- sealed meso cells (OFF-plane ledger): **1,260** — L1-treatment-function-coherence 756 · L2-summon-implies-proxy 504
- coincident-projection aggregation: 10,080 cells → **7,128** distinct glyph positions (max multiplicity 6); size-stepped deterministically, NO jitter
- ghost cells outside frozen plane box (clipped): **21** (all unlit=true; 7 distinct positions) — CLIP DISCLOSURE (r3.2, spec §9.2.3) rendered in the GHOST FIELD ledger, count from the render pass
- clip-disclosure line as rendered (both skins): **"21 unlit cells project beyond the frame (clipped, not rescaled — frame frozen to the settled points)"**
- depth Σ: **693,146,160** == depth_sum_check == post-red-law denom
- RED-3' note (emitted, drives off-plane seal semantics): RED-3' seals live at GEOMETRY drill-in, not the meso plane (geometry is a demotable non-core coord). Meso SEALED cells are L1' + L2 only. Depth badges already net out RED-3' within-cell (geometry x commit!=instant) survivors.

## Ghost HORIZON accounting (r4, spec §9.4.1 — all COMPUTED FROM THE RENDER PASS)
- **hull vertex count: 22** (convex hull of 7,128 distinct projected ghost positions, INCLUDING the 21 out-of-frame cells — the hull is of the lattice's REACH, then clipped to the plane frame)
- hull east reach (world x): **1.2581** · settled points east reach (world x): **1.6276** · **EAST gap = 0.3695** (settled kits stand east of the horizon there — the load-bearing disclosure direction)
- envelope: dashed polyline (open, closed back to first vertex), CLIPPED to plane frame via the same planeClip used by ghost glyphs; drawn BENEATH the ghost glyphs (chrome, sub-ghost — must not read as data)
- label (exact string, verbatim): **"ghost coverage limit — dark beyond this line is unmapped at meso grain, not absent."** — placed adjacent to the EAST gap, tied to the hull's east vertex by a thin dashed leader; visible two-line wrap (split at the em-dash); the exact contiguous string is carried in the envelope's `<title>` (grep-verified present both skins)
- computed-not-constant: PROVEN by the r4-horizon doctored-input test (remove the extreme corner cell → hull recomputes → CHANGES); vertices are never hard-coded

## Headline COVERAGE PAIR accounting (r4, spec §9.4.2 — ratios COMPUTED, not hard-coded)
- lead 1: **"192 / 10,080 ≈ 1.9% of feasible meso ground ever lit"** (lit_cells 192 / meso_feasible 10,080)
- lead 2: **"469 kits over 192 lit cells ≈ 2.4 kits per lit cell — the genre didn't explore; it remade."** (active 469 / lit_cells 192)
- demoted secondary (retained, no longer lead): **"469 active ≈ 6.8×10⁻⁵ % of 693,146,160 feasible exact-grain kits"** — the 693M exact-grain line; present ONLY in the secondary position (grep-verified NOT in either lead)
- anti-"422,445,240" grep: verified ABSENT (superseded denominator never appears)

## Beyond-horizon accounting (r5, spec §9.5.1 — N COMPUTED FROM THE RENDER PASS)
- **N = 14** active kits stand beyond the ghost hull — point-in-polygon of the 469 active points against the SAME 22-vertex world hull (`ghostHullWorld`) the r4 horizon uses; boundary convention ON-hull ⇒ INSIDE (spec §9.5.1). Matches gandalf's independent receipt (14).
- **group profile:** CHANNELED-BEAM 3 · NEUTRAL 1 · WHIRLWIND 10 — 10 WHIRLWIND (of the 15 members) + 3 CHANNELED-BEAM + 1 neutral; ALL carry `commit=channel`.
- **kit ids (sorted):** `d2-bvc`, `d2-ww-barb`, `d2-ww-sin`, `d3-ww-wastes`, `di-whirlwind-barb`, `gd-eor-warlord`, `gd-flames-of-ignaffar-purifier`, `le-warpath-vk`, `poe1-cyclone`, `poe1-incinerate`, `tl1-alchemist-summoner`, `tq2-whirlwind-rogue`, `ud-flamethrower-channel`, `ud-whirlwind-str`
- rendered line (both skins), OMITTED entirely when N==0: **"14 settled kits stand beyond the horizon — kits project with all 14 coordinates; ghost cells carry the 7 core only (the strongest east pulls — cone/whirlwind geometry, channel commit — are invisible at meso grain)."**
- the line renders DIRECTLY AFTER the clip-disclosure line in the GHOST FIELD ledger box; the full contiguous string is in a `<title>` for whole-grep; the plaque grows to hold the wrapped rows and the sealed ledger shifts down.
- **why they overshoot:** kits project with all 14 basis coordinates; ghost cells carry only the 7 core, so the strongest EAST pulls (geometry=cone/whirlwind loading #3, commit=channel loading #2) are MASKED at meso grain — the lit channel kits reach east of the 7-core hull. Position ≠ membership.
- **excluded — supplementary tombstones:** the graveyard is its own layer. The 3 easternmost points of the whole plane are dead channel kits (tl2-arc-beam · d4-incinerate · d2-inferno-sorc), beyond by the same mechanism, disclosed by their tombstone layer.

## Point accounting (FROZEN from r2)
- active: **469** (neutral 383 + grouped 86) · corpses: **37** · total: **506**
- death classes: extrinsic-content-mix:3, extrinsic-itemization:7, extrinsic-no-lever:4, extrinsic-split-scaling:3, extrinsic-tuning:7, intrinsic-red:12, system-evidence:1

## Acceptance tests
- [PASS] **point-counts** — active=469 (exp 469), supp=37 (exp 37), total=506 (exp 506)
- [PASS] **grouped-count** — grouped=86 (exp 86)
- [PASS] **ghost-counts** — feasible=10080 (exp 10080), sealed=1260 (exp 1260)
- [PASS] **ghost-lit-conformance** — feasible lit=true 192 == emitted lit_cells 192
- [PASS] **ghost-depth-sum** — Σdepth=693,146,160 == depth_sum_check 693,146,160 == denom 693,146,160
- [PASS] **sealed-cut_id-conformance** — all 1260 sealed cut_ids in {L1-,L2-}: L1-treatment-function-coherence, L2-summon-implies-proxy
- [PASS] **point-layout-equality** — identical point coordinate fingerprint
- [PASS] **ghost-layout-equality** — identical ghost coord+status fingerprint (both skins)
- [PASS] **determinism** — instrument:byte-equal, archive:byte-equal
- [PASS] **R2-no-2.57-numeral** — clean (naive-box 2.57 absent as content)
- [PASS] **R2ext-no-422445240** — clean (superseded denominator absent)
- [PASS] **R3-no-season-N** — clean
- [PASS] **RIDER-1-badge** — inertia_pct=8.36 + retained_dims=14 + structure_statement present both skins
- [PASS] **r2-pole-glosses** — all 4 pole glosses present both skins
- [PASS] **r2-density-legend-line** — density-field legend line present both skins
- [PASS] **r2-derivation-gloss** — derivation gloss present both skins
- [PASS] **r3-census-line** — mandatory census line present both skins
- [PASS] **r3.2-clip-disclosure** — clip line present both skins (count=21, from render pass; all clipped cells unlit=true)
- [PASS] **r3-coverage-callout** — active 469 + denom 693,146,160 present both skins
- [PASS] **r3-sealed-ledger** — sealed 1,260 + cut ids [L1-treatment-function-coherence, L2-summon-implies-proxy] present both skins
- [PASS] **ghost-glyphs-not-regions** — ghost is <circle> glyphs; no polygon/pattern/region fills
- [PASS] **frozen-layer-regression** — instrument: point-circles FROZEN (469 pts), tombstone-positions FROZEN | archive: point-circles FROZEN (469 pts), tombstone-positions FROZEN
- [PASS] **r4-horizon** — envelope=true, exact-label=true, computed-not-constant: removed extreme cell @ (-1.0910,-1.6548) ×2; hull CHANGED (canonical 22 vtx)
- [PASS] **r4-headline-pair** — lead present=true, ratios match indep (lit 1.9%, density 2.4)=true, 693M in secondary only=true
- [PASS] **r4-frozen-layer-regression-vs-r3.2** — instrument: points FROZEN, ghost-glyphs FROZEN, tombstones FROZEN, frozen-text PRESENT | archive: points FROZEN, ghost-glyphs FROZEN, tombstones FROZEN, frozen-text PRESENT
- [PASS] **r5-beyond-horizon** — line-present=true, N=14 (indep=14, expected=14, numeral-match=true); doctored (a) removed beyond-horizon kit 'ud-flamethrower-channel' (x=1.390) -> N 14 -> 13 (CHANGED by 1); doctored (b) all-inside (points -> hull centroid): BEYOND_N=0; on-chart line omitted both skins=true
- [PASS] **r6-clip-wrap** — instrument: title=true, rows=2 each<=62=true present=true, old-single-line-gone=true | archive: title=true, rows=2 each<=62=true present=true, old-single-line-gone=true (wrap: 2 rows @ budget 62)
- [PASS] **r6-footer-anchor** — instrument: at-x=1132.00=true, old-1504-gone=true, tracks-rect(1144-12=1132.00)=true | archive: at-x=1132.00=true, old-1504-gone=true, tracks-rect(1144-12=1132.00)=true
- [PASS] **r6-frozen-layer-regression-vs-r5** — instrument: pts FROZEN, ghost FROZEN, tomb FROZEN, horizon FROZEN, frozen-text PRESENT, fixes[clip+true/-true,footer+true/-true], direct-diff CLEAN (+6/-6; only the 2 named fixes + plaque reflow) | archive: pts FROZEN, ghost FROZEN, tomb FROZEN, horizon FROZEN, frozen-text PRESENT, fixes[clip+true/-true,footer+true/-true], direct-diff CLEAN (+6/-6; only the 2 named fixes + plaque reflow)
- [PASS] **r6-occlusion-guard** — instrument: plaque=[1144,1056]-[1504,1200], centers-inside=0, nearest-above-margin=4.07px | archive: plaque=[1144,1056]-[1504,1200], centers-inside=0, nearest-above-margin=4.07px — nearest data-mark margin above plaque top = 4.07px

## Smoke tests
- [PASS] **WHIRLWIND x>0 (PERFORM)** — x=0.8191
- [PASS] **WHIRLWIND y<0 (EMBODY)** — y=-1.0816
- [PASS] **TOTEM-SENTRY x<0 (DEPLOY)** — x=-0.7307
- [PASS] **charged-dash near WHIRLWIND condensation** — poe1-charged-dash dist=0.209 (< 0.848 = 20% diag)
- [PASS] **all lit ghost glyphs inside plane frame (not clipped)** — 192 lit glyph positions, all in-frame=true
- [PASS] **coincident-projection aggregation active** — max multiplicity=6 (aggregated 10080 cells -> 7128 glyph positions)
- [PASS] **ghost hull is a small polygon** — hull vertex count=22
- [PASS] **EAST gap real (ghost hull east < settled east)** — ghost hull east x=1.2581 < settled east x=1.6276 (gap=0.3695)
- [PASS] **headline lit-fraction ≈ 1.9%** — lit fraction=1.9% (192/10080)
- [PASS] **headline density ≈ 2.4 kits/cell** — density=2.4 (469/192)
- [PASS] **beyond-horizon N == 14 (spec §9.5.1 receipt)** — N=14 active kits beyond the ghost hull
- [PASS] **beyond-horizon group profile (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral)** — WHIRLWIND=10, CHANNELED-BEAM=3, NEUTRAL=1 (CHANNELED-BEAM:3, NEUTRAL:1, WHIRLWIND:10)
- [PASS] **point-in-hull: most actives INSIDE (N << active count)** — 14 beyond / 469 active = 3.0% (the lit archipelago sits mostly within the ghost reach)
- [PASS] **r6 plaque grew upward, bottom pinned at 1200** — plaque top y=1056.00 (r5 was 1066), height=144.00 (r5 was 134), bottom=1200.00 (must be 1200)
- [PASS] **r6 footer census re-anchored to plaqueRect.x-12** — census end-anchor x=1132.00 == plaqueRect.x(1144.00)-12 = 1132.00 (expected 1132)
- [PASS] **r6 clip line wraps to >=2 rows** — clip wraps to 2 rows @ budget 62 (was 1 unwrapped row in r5)

## Layout calls / judgment made (r5 — the ONE call this amendment adds)
- **The point-in-hull judgment (spec §9.5.1 — the load-bearing r5 call).** N is the count of ACTIVE points that fall OUTSIDE the ghost hull. The judgment has three parts, each made to keep this a single honest measurement, not a second computation: **(1) ONE hull, not two.** The test polygon is `ghostHullWorld` — the *exact same* convex hull the r4 horizon draws (Andrew's monotone chain over the distinct world positions of all 10,080 feasible cells). I did NOT recompute a hull for the count; the disclosure line and the drawn envelope are guaranteed consistent because they are the same 22-vertex object. **(2) Test in WORLD space, not SVG space.** The hull lives in world coordinates (its true reach, incl. its out-of-frame vertices); `sx`/`sy` is affine-monotone, so world-containment ≡ projected-containment — but testing in world space avoids re-introducing the clip frame. This matters for the load-bearing EAST case: a channel kit east of the hull but *inside* the plane frame is still beyond the hull, and must count. **(3) Boundary convention: ON ⇒ INSIDE (spec §9.5.1).** The point-in-polygon does an explicit on-edge check FIRST (collinear + within the segment span, eps 1e-9); an on-edge point returns INSIDE and is NOT counted as beyond. Then a standard ray-cast parity test decides strict interior. Result: N=14, matching gandalf's independent receipt exactly. **Fail-loud guard:** if the render pass had computed N≠14 on the real input, the run HALTS (`die`) rather than shipping a wrong count — the disclosure would be dishonest, and a moved N means the hull, the input, or the receipt drifted and needs a human look.
- **The line's placement + wrap (layout call).** It renders DIRECTLY AFTER the clip-disclosure line inside the GHOST FIELD ledger plaque, with the SAME faint/gloss treatment (spec §9.5.1 "match the clip-disclosure line's treatment"). Because the locked string is ~230 chars it WRAPS: a deterministic character-budget greedy wrap (`wrapByChars`, budget 62 chars ≈ the ~336px usable plaque width at font 9.5) splits it into rows rendered as `<tspan>`s; the plaque `<rect>` height grows by the row count and the sealed ledger below shifts down by the same amount, so nothing overprints. The FULL contiguous string is carried in a single `<title>` node on the parent `<text>` — so acceptance greps the whole sentence as one unit even though the visible text is multi-line (same pattern the r4 horizon label uses). **Zero-case:** if N==0 the entire block (rect-grow, `<text>`, `<title>`) is skipped — no "0 kits" ever renders (proven by the doctored all-inside test).
- **Footer render-script string held FROZEN (frozen-diff discipline).** The in-SVG footer still reads `render: galadriel/atlas-edition1-render-r3.mjs` (inherited from r3/r4). I deliberately did NOT bump it to r5: spec §9.5.2.17 demands the ONLY diff vs r4 be the new ledger line, verified by direct SVG diff — changing the footer string would introduce a second diff region. True r5 provenance is carried here in the note + the script filename. (Same discipline r4 used to preserve its r3.2 diff.)

## Layout calls / judgment made (r4 — the calls the r4 amendment added, unchanged)
- **Hull computed in WORLD space, drawn projected, clipped to frame (spec §9.4.1).** The convex hull is taken over the DISTINCT world positions of ALL 10,080 feasible cells (Andrew's monotone chain; deterministic sort x-asc then y-asc; ≤0 cross-product test drops collinear points → a tight 22-vertex ring). This is the lattice's true reach — it INCLUDES the 21 out-of-frame outliers. Each vertex is then projected through sx/sy and the polyline is clipped to the plane rect by the SAME planeClip that trims the ghost glyphs. Rationale: hulling in world space (not the in-frame subset) means the envelope describes the real reach; clipping (not rescaling) keeps the frozen frame. **Vertices are from the render pass — never hard-coded** (doctored-input test proves it).
- **Horizon drawn BENEATH the ghost glyphs (spec §9.4.1 "sub-ghost, chrome not data").** The envelope polyline is emitted at the TOP of the LAYER-0 clip group, BEFORE the ghost dark/lit glyph groups — so the glyphs paint OVER it. This is the judgment call that keeps it from reading as data: a limit line the eye registers as ground, not as a plotted boundary. (Consequence: the ghost glyph `<circle>` byte-strings are unchanged vs r3.2 — frozen-layer regression holds.)
- **Stroke treatment (layout call):** hairline dashed. `stroke-width` 1.1 (both skins), `stroke-dasharray` "7 5" (a long-dash reads as "limit/threshold", distinct from the zero-axis "2 6" fine-dot and the tombstone "2 2"), `stroke-linejoin=round` so hull corners don't spike. Instrument: cool gray `#93a0b3` @ 0.62 opacity. Archive: dim gilt `#5a5340` @ 0.75 — "embers at the edge of the walked dark". NO fill (a fill would assert the region-claim §9.2.2 forbids — the envelope is an open dashed line, never a shaded area).
- **Label placement (layout call — named per spec ask): adjacent to the EAST gap.** The mandatory string is anchored off the hull's EAST vertex (the greatest-projected-x vertex, computed from the render pass — not hard-coded). A thin dashed leader + a small hollow marker tie the label to that vertex; the label itself drops into the sparse lower-right interior (measured: only 3 settled points in the east-gap band) and reads right-anchored into the gap. This is the load-bearing direction: settled kits reach x=1.628, the ghost hull ends x=1.258; the two gold flame-kits visibly sit EAST of the envelope, in the "dark beyond" the label names. **Two-line visible wrap** (split at the em-dash, a natural clause break) for legibility of an 85-char disclosure sentence; the exact contiguous string lives in the polyline `<title>` so the acceptance grep matches the whole label verbatim.
- **HEADLINE PAIR re-lead (spec §9.4.2):** the two meso-grain stats now LEAD the callout (font 13.5/12, bold, ink) at lower-left; the exact-grain 693M line DEMOTES directly below at font 10, faint (`glossStyle`, `faint` ink) — retained and honest, no longer the lead. Both ratios (1.9%, 2.4) are computed from emitted fields (lit_cells/meso_feasible, active/lit_cells); the prose halves are content-locked disclosure copy (same class as the pole glosses). The 693M numeral is grep-verified ABSENT from both leads.

## Layout calls / judgment inherited (r3/r3.2 — unchanged, byte-frozen)
- **FROZEN PLANE BOUNDS (load-bearing):** world bounds computed from POINTS ONLY (min/max over all 506 + 6% pad), byte-identical to the r2 baseline — so the 506 point SVG coordinates never move. The ghost field is zero-mass ground (spec §9.1a) and must NOT rescale the plane.
- **Ghost outliers CLIPPED, not rescaled — DISCLOSED on-chart (r3.2, spec §9.2.3):** 21 feasible cells (all unlit=true, 7 distinct positions) project outside the frozen point-box. They are clipped to the plane frame via SVG clip-path. Rescaling to fit un-settled outliers would break frozen-layer regression AND shrink the settled archipelago — clip is the correct call. **The clip is no longer silent:** a disclosure line renders in the GHOST FIELD ledger (both skins), count computed FROM THE RENDER PASS (cells whose projected position falls outside the plane rect), so it follows any future atlas.json change; if zero cells clipped the line is omitted entirely (no "0 clipped"). §9.2.3: the dark the reader sees implicitly claims to be the feasible space — silent truncation is an under-claim.
- **Coincident-projection aggregation (spec §9.2.4):** cells sharing a 2-dp SVG position are merged into one glyph; radius grows by log2(multiplicity+1) (deterministic size-step, NO RNG). A merged position is LIT if ANY coincident cell is lit (census-current, spec §9.1b).
- **Ghost as GLYPHS never regions (spec §9.2.2):** ghost cells are <circle> marks only — no Voronoi, no hatching, no painted boundaries (RIDER-1 continuum discipline; over-claim discipline shared with F-1).
- **Figure-ground:** unlit ghost = the feasible dark (faint near-ground); lit ghost = a touch stronger (census-lit, still sub-point). Layer order bottom→top: unlit ghost → lit ghost → density → points → tombstones → chrome. The chart's story: settled territory is a lit archipelago in a vast feasible dark.
- **Sealed = OFF-plane LEDGER (spec §9.2.4):** 1,260 sealed cells carry NO coordinates (never projected); rendered as a chrome register with cut ids verbatim from cut_id. cut_id conformance to {L1-, L2-} is a HARD refusal gate (R4).
- **Coverage + census line:** coverage callout and mandatory census line ("ghost field lit from the current census; positions from the frozen Edition-I basis.") from emitted fields. Superseded denominator 422,445,240 grep-verified ABSENT.
- **Depth is emitted, never derived (spec §9.1d):** depth per cell rendered from the field; Σ is an emitter TEST only.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (MATCH); point fingerprint identical (MATCH). Skins vary only ghost + horizon ink/opacity chrome. The horizon hull, label placement, and headline-pair layout are one code path — both skins carry the same 22-vertex hull and the same label anchor.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal (verified across separate process invocations).

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not. The r5 addition honors this: **N=14** is COMPUTED from the render pass (a point-in-polygon of the emitted active points against the emitted-ghost-derived hull — never a literal; the doctored-input tests prove it follows the data: remove a beyond kit ⇒ N drops, move all kits inside ⇒ N=0 ⇒ line omitted); the rest of the sentence (the 14-coordinate / 7-core framing, the cone/whirlwind/channel examples) is content-locked disclosure copy carried VERBATIM — empirical facts about the frozen basis, same class as the pole glosses. The r4 additions still hold: the ghost horizon's 22 vertices are COMPUTED from the emitted ghost field; the headline-pair ratios (1.9%, 2.4) are COMPUTED from emitted counts. The renderer computes layout; it never invents content.
