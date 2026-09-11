# Measured lessons

## ASTRA run 02 — preparation and measurement

Evidence: `astra_test_01/run_02/REPORT.md`, `evidence/checkpoint_2/checks.json`
and `evidence/instrument_audit.json`, relative to repository root.

- Master-conditioned green plates plus matting removed prior baked-checkerboard
  failures. Final eight views passed alpha-format, height and literal light checks.
- Staff tips, not body height, caused SW/NW silhouette parity failures. Targeted
  staff-placement edits corrected the silhouette range to 240–241 px. Do not remove
  the staff from the literal measurement to claim a pass.
- Manual thumbnail anchor estimation caused SW's 5.25 px registration error. This
  is a preparation defect and does not establish generator incapability.
- Rectangular sole regions could intersect another leg or truncate a sole. Four
  apparent contact passes became unverified under the stricter audit. Reject
  boundary contacts; use reviewed polygons/contours for overlap, then independent
  output-space validation. Seven synthetic utility tests passed; no animation
  or VFX art was qualified by those tests.
- Fixed camera guides improve conditioning but do not prove exact 3D consistency.
- The browser runtime had no available browser. JavaScript syntax and atlas checks
  passed, but they do not substitute for composite playback inspection.

Append further findings with links to the measured artifact. Label hypotheses and
proposed methods as unvalidated until applied successfully.

## ASTRA run 03 — qualified turnaround and first animation probe

- Global lower-alpha contours computed BEFORE foot-region selection avoid crop-created sole edges. Visible sole overlay review plus integer translations brought all eight static contact errors to ≤0.5 px and yielded turnaround PASS. Evidence: `astra_test_01/run_03/evidence/turnaround/checks.json`.
- Two successive 2×2 idle sheets changed body scale despite shared references: first 240–243 px, second 257–260 px under the fixed scale. Reject the second batch; do not normalize its poses independently to hide growth. Evidence: `evidence/idle_S_sheet_method_check.json`.
- Individual master-conditioned edits restored scale; the revised S idle seam is 0.661 versus minimum internal transition 0.718. This qualifies only that loop seam, not the full character or drift comparator. Evidence: `evidence/idle_S_revised_check.json`.

## Run 03 — S pilot, east batches and VFX

- All 28 S frames pass current numerical checks, including fixed cast-05 drift comparators; motion and planted-foot interpretation remain separate. Evidence: `astra_test_01/run_03/evidence/current_checks.json`.
- Local loop repairs must inherit the complete original registration transform, including scale and anchor. Re-estimating a repaired boot anchor can manufacture a new seam jump.
- A 640px crop of the 1024px approved reference, repeated only as a 2x2 conditioning layout, better matches generated cell occupancy. The E idle batch holds 240–243px under one fixed scale. This does not yet qualify its loop seam (currently fails). Never independently fit each pose's full silhouette to hide proportion changes.
- Sole-contour width thresholds must scale with character extent, not padded canvas size; otherwise a staff base can become a false boot when batch cell size changes. Source and output contours still require visible evidence.
- Green keying with G=max(R,B) as an edge prior turns blue frost cyan. A documented blue-edge foreground prior reduces that extraction defect while retaining opaque body pixels. Evidence: `evidence/blue_matte_comparison.png`; this prior is an approximation, not recovered ground truth.
- VFX black-emission matting must retain detached particles. Use alpha=max(RGB) and unassociated RGB, preserving emission over black. Never use the character's largest-component cleanup for VFX.
- Register projectile energy to a fixed vertical centerline before the 256x128 crop. All 24 VFX frames exist; impact final frame has zero residual. Visual playback remains unverified.
- The literal light-centroid gate includes spell pixels. East-facing frost on the right failed. An overhead, upper-left gathering motion passes the unchanged light gate. Passing numbers still did not guarantee recovery returned to idle; visual review required a second correction.

## Run 03 — complete frame inventory, repairs still active

- All 224 character and 24 VFX frames are present. At this checkpoint 11 of 16 character loops fail the unchanged minimum-transition seam test; numerical completeness is not campaign acceptance. Evidence: `astra_test_01/run_03/evidence/current_checks.json`.
- Inspect alpha at each native source-cell border before registration. Transparent output padding can hide a frost cluster that was already clipped in generation. Regenerate the cropped effect with compact margins; do not call padding a repair.
- Never mix facing directions in a repair reference sheet. A combined N/NW repair copied the first cell's NW orientation into north poses. North-only repair restored the straight back view. Evidence: `records/rear_frost_margin_repairs.json` and `records/N_margin_idle_repairs.json`.
- Prompts assigning left/right foot contacts do not establish actual gait. Several batches repeated the same leading leg, and one hid a boot entirely. Review contact and passing poses visually before accepting timing; unique frame hashes and sole-midpoint checks do not establish an alternating walk.
- A raised sole may fall above the generic lower-leg band. Use visually documented source/output regions around actual global contours, rejecting artificial region-boundary edges. These measurements establish the two-visible-sole midpoint, not planted-foot stability. Evidence: `source_contact_regions.json`, `output_contact_regions.json`.
- Check semantic phase order: NW release peaked in source cell 2 instead of cell 1. Assemble according to observed action and retain the source-cell mapping, then verify cast index 5 is the actual release peak.
- Proposed, not yet validated on production art: composite generated moving regions onto an unchanged painted base to reduce full-frame repaint drift. `composite_motion.py` has synthetic utility checks only. Explicit Python image-editing authorization is pending; no production compositing has been performed.

- All eight walk seams now pass after generated pre-contact edits using the original first-contact transform. SW improved from 1.630 with re-centered registration to 0.535 with inherited registration, while actual output midpoint remained within tolerance. Evidence: `evidence/walk_SW_07_close_metrics.json`, `evidence/current_checks.json`. This does not repair repeated leg leads or establish a standard gait.
- A native-alpha idle edit returned a baked checkerboard despite a transparent input. Extraction rejected it before publication. Evidence: `records/idle_N_07_native_edit.json`. Do not infer transparency support from the displayed checkerboard.

## Painted-world E01 — source eligibility and recovery

- A publisher screenshot listing included class/skill menus and HUD-hidden
  promotional scenes alongside gameplay. File provenance and scene eligibility
  are separate checks. Exclude menus from camera measurements; retain HUD-hidden
  scenes for explicitly scoped composition observations. Evidence: [E01 source
  ledger](../../../../astra_test_01/design/experiments/E01/sources.json), rows
  LE-01 through LE-11. Confidence: high for these inspected files; no claim that
  every publisher list behaves this way.
- Hash comparison recovered exact publisher URLs for four previously retained
  Last Epoch images and three PoE1 images. Reuse verified bytes rather than
  substituting visually similar images. Evidence: the same ledger's
  `byte_identical_existing_files` fields. This verifies provenance recovery,
  not default camera settings or motion quality.
- The official Grim Dawn broken/repaired bridge pair shows a visible geometry
  change at essentially the same view. It supports an art/state comparison but
  cannot prove traversal, state-transition timing or navigation-cache updates.
  Evidence: E01 GD-04/GD-05; those claims remain unverified in the report.

## Painted-world E02 — perspective and renderer comparison

- Exact ground-following camera motion keeps its followed actor's relative
  viewpoint constant. This does not protect off-center props/actors or camera
  lag/clamps. Evidence: [E02 sample analysis](../../../../astra_test_01/design/experiments/E02/evidence/analysis.json)
  and paired Godot/Pixi runtime validation. Scope: registered C camera and flat ground.
- A diagnostic close-up redrawn from source at higher resolution is not comparable
  to an enlarged native render. Initial Pixi/Godot review panes mixed these methods;
  v2 uses captured render textures in both. Preserve the invalid comparison and
  judge native gameplay size separately. Evidence: [E02 report](../../../../astra_test_01/design/experiments/E02/REPORT.md).
- The chosen scale-only upright image differs from a known C-projected cuboid by
  up to 6.93 px at lateral positions. This detects a geometric approximation; it
  does not establish hidden painted anatomy or a perceptual failure. The old
  mage source's depicted camera remains uncalibrated. Do not turn this component
  result into a rule that perspective is unsuitable for painted art.

## 2026-09-11 — browser screenshot dimensions can invalidate renderer comparisons

E02P batch 01 used Playwright element screenshots at a fractional CSS position: all 18 native-size checks failed at 720×406 although engine coordinates passed. Capturing the actual rendered canvas buffer produced 720×405 in batch 02 without changing thresholds or painting bytes. Preserve both batches; inspect native buffer dimensions before interpreting sharpness across renderers. This lesson concerns capture geometry, not Phaser art quality. Evidence: `astra_test_01/design/experiments/E02P/REPORT.md` and its batch-01/batch-02 validation records. User delivery observation: Matt's Canvas links opened as code; the standalone HTML review was verified directly from disk across all 18 position/camera combinations.

## 2026-09-11 — Phaser 4 masks and native-alpha failure

E03 pillar and mage requests returned RGB with painted checkerboards. Do not call those native-alpha assets. A separately registered runtime polygon-mask experiment preserved original pixels and tested static contour/background leakage in all three engines. This does not qualify fine hair, translucency or moving gear silhouettes. Phaser 4.2.1 `setMask` was ignored in WebGL; its versioned source identifies the method as Canvas-only. `enableFilters().filters.external.addMask` fixed the tested WebGL path. Coordinate checks alone missed the visual failure: outside-silhouette pixel checks were added, with failed renders retained. Evidence: `astra_test_01/design/experiments/E03/REPORT.md`.

## 2026-09-11 — E04 resolution and contour falsification

Evidence: [E04 report](../../../../astra_test_01/design/experiments/E04/REPORT.md),
[matched capture](../../../../astra_test_01/design/experiments/E04/evidence/batch-02-resolution/resolution.json),
[multi-background board](../../../../astra_test_01/design/experiments/E04/evidence/batch-02-resolution/current-mask-backgrounds.png).

A 3× enlargement of an already rasterized ~50px mage looks softer than a fresh
150px render from the same original source. The same higher buffer cannot recover
detail absent from the 1536×1024 floor. Compare equal framing and displayed pixel
coverage before blaming the camera or selecting an engine. Confidence: high for
this controlled still, not a fullscreen/performance qualification.

A mask can pass exterior-background checks and still retain checkerboard inside
its boundary or cut away anatomy. Higher-resolution/dark/light/blue inspection
exposed pale mage coat contamination and an incorrect NPC hand/coat trace.
The NPC source uses a dark background and pale skin; not every pale patch is
white-matte leakage. Preserve source-coordinate contours, check both inclusion
and exclusion, and do not convert user rejection into a pass through a coarse
native-pixel allowance. E03's historical static-mask result stays recorded;
its broader visual transfer is falsified by E04. Confidence: high for these
observed regions; no blanket alpha-removal recipe established.

Headless movement validation caught a tiny floating-point remainder being treated
as a new zero-distance move and clearing the path. Preserve the failed 16/17
boundary evidence; stop movement-budget iteration below its numerical epsilon.
The corrected 17/17 boundary and actual two-size browser traversal support the
local fix. Typed effect descriptors and headless JSON boundaries were exercised;
they do not establish a finished Godot port, shared lighting or animated VFX.

## 2026-09-11 — holdout references must preserve material indices

[E05G](../../../../astra_test_01/design/experiments/E05G/REPORT.md) initially exceeded its frozen gear-composite tolerance even though source geometry and bone bindings passed. Clearing body material slots for holdout renders reset per-polygon material assignments in the reference scene. Restoring those indices removed the face/hair mismatch without changing source pixels, geometry or acceptance limits. The corrected36sparse Pixi comparisons pass; the original capture remains failed evidence. When swapping render materials, preserve both slots and polygon indices. Confidence high for this mechanism, limited to the tested rig/view; final gear lighting and full motion remain unqualified.

## 2026-09-11 — RGB emission plates are a material contract, not native alpha

[E06F](../../../../astra_test_01/design/experiments/E06F/REPORT.md) preserves two generated RGB frost plates and explicitly declares additive emission semantics. Their outer4pixel maximumRGB is1; multi-background on/off comparisons and a wrong-normal-blend control distinguish the material from a transparent sprite. Do not relabel black-backed RGB as native alpha. Additive composition passes the scoped launch/lifecycle checks but loses blue core detail against the light control. Neither border statistics nor timing tests qualify opaque ice, blood, receiver lighting or broad cross-element reuse.

## 2026-09-11 — whole-scene guides do not guarantee spatial or semantic fidelity

[E07R](../../../../astra_test_01/design/experiments/E07R/REPORT.md) corrects a specific foreground-doorway inside/outside reversal with explicit region/ray guides. Both initial paintings still enlarge/shift geometry well beyond the3native-pixel overlay tolerance. A changed-conditioning repair follows framing more closely but paints NPC/monster probes as jars and chest/crate probes as stone blocks. Preserve geometric and semantic failures separately; a pleasing scene or a close silhouette is not a typed-layout pass. The three-call branch is closed. Geometry-owned material painting is the registered next alternative, not yet a general production rule.


### E07S — surface sampling is separate from painted architecture

Two opaque material plates on exported geometry preserved source-camera exit witnesses, collision and sampled light blocking in native and fresh3× Pixi buffers. Declared mipmapped sampling reduced minification noise without changing source pixels. This did not supply missing architectural or prop detail: typed chest/crate cubes and mismatched actor shading still fail complete art. Preserve that distinction; use geometry-owned detail and separately authored prop states next. [Evidence](../../../../astra_test_01/design/experiments/E07S/REPORT.md).


### E05V/E05H — inspect rear source geometry before blaming texture projection

Eight fixed-camera source views exposed face-like marks on the rear head. New native closeups and category-ID renders proved the hair shell intersected the skull. A347-vertex radial clearance repair removed960 exposed-skin ROI pixels; the hide-hair negative control exposed4058. Original source/non-hair geometry preserved. This repairs scalp coverage, not painted pilot or gear quality. [Evidence](../../../../astra_test_01/design/experiments/E05H/REPORT.md).


### E07D — sparse occlusion witnesses do not prove detailed surface ordering

Exit/light witnesses passed while crate braces visibly disappeared behind their own faces under cell-centroid painter sorting. Neutral part IDs and correct state transitions do not prove per-pixel visibility. Test depth handling or source-baked nativeRGBA layers before adding more surface decoration. Lossless browser-evidence archival preserved decoded pixels; capture transport failures stayed failed, with allocation deviation and byte limits recorded. [Evidence](../../../../astra_test_01/design/experiments/E07D/REPORT.md).


### E07Z — prove depth with pixels and an independent source oracle

The installed Pixi context supplied24 depth bits and passed draw-order/clear controls. Homogeneous camera depth plus opaque mesh depth tests repaired21/21 brace/band witnesses in normal and reversed order; painter controls matched12/21 and0/21. Original geometry/materials unchanged. This does not qualify actor sprites or translucent effects. [Evidence](../../../../astra_test_01/design/experiments/E07Z/REPORT.md).


### E09I — preserve the full source contract instead of copying a view projection

The actual Godot copy is LOCKED while current engine W3 is DRAFT. String effects/timing are intentional in the legacy schema. D4 omits timing/cooldown/energy from its presentation projection; do not adopt it as full combat interchange. Lossless neutral ingestion preserved both648-skill snapshots with23 checks, leaving180 large_aoe bindings unresolved instead of inventing radius from range. [Evidence](../../../../astra_test_01/design/experiments/E09I/REPORT.md).

### 2026-09-11 · Eight-view gear/hair transfer exceeds sparse proof (E05A)

Narrower helmet plus explicit hair visibility improved fit, but47/96 actual Pixi composites at50/150px exceeded unchanged E05G pixel limits (worstMAE1.8933, fractionerror>8=.05467). Failures cluster at hair/head and armor boundaries; denoising/shared sample coverage/secondary lighting are not yet isolated. Do not generalize sparse one-view holdout compositing into modular hair/gear qualification. Both bad controls fail as intended. F04 clean style remains unmet by generated swatch albedo over simple plates. [Evidence](../../../../astra_test_01/design/experiments/E05A/REPORT.md).

### 2026-09-11 · Native two-view success does not establish filtered eight-view transfer (E05O)

128samples/no-denoise plus joint holdouts/hair-secondary-off passed12source comparisons but failed complete GPU transfer: corrected mask accumulation57/96fail, native-over34/96, direct-over46/96. Mask complexity did not buy qualification. Keep the source/body painting and fit tests, stop this unchanged RGBA reconstruction branch, research a depth-bearing or common-sample representation. Custom offscreen shaders require asymmetric orientation preflight; batch3 invertedY was invalid, preserved and corrected in batch4. [Evidence](../../../../astra_test_01/design/experiments/E05O/REPORT.md).

### 2026-09-11 · Depth-bearing geometry supports sparse gear reuse in Pixi (E05J)

After failed independent-RGBA reconstruction, unchanged source painting plus rest geometry/bone palettes and separate gear passed288GPU-vs-Blender-evaluated comparisons (MAEmax.314765; fractionerror>8max.012627). Three sparse poses only; not full art/animation qualification. Near.1/far100yielded54order-dependent pixels; range-validated10–40mclip made reverse pixel-exact. Verify depth precision against actual scene range, not a copied near plane. Pixi reserves mesh`uColor`asvec4; customvec3collision emittedGL1282despite correct witness pixels, fixed by a distinct name. [Evidence](../../../../astra_test_01/design/experiments/E05J/REPORT.md).

### 2026-09-11 · Native sampling and pose-derived review bounds (E05Q)

MSAA4+mips/aniso8 improved8/8scene comparisons against finite3×fresh-geometry reference and removed observed grain without obvious sampled material bleed. New4320×1380render is not enlarged800pxraster. The old strip clipped a casting hand on BOTH reference/test paths: equality does not prove full coverage. Corrected32idle/cast bounds pass; supplementalwalkstillneedsmorewidth. Derive every review extent from actual tested poses. Full art remains unqualified. [Evidence](../../../../astra_test_01/design/experiments/E05Q/REPORT.md).

### E07K · Shared depth and light do not establish finished chamber art

A depth-bearing pilot shares chamber camera/light data with372 passing CPU ray witnesses and closed-leaf light controls.38 interaction checks pass. Numeric foot Z is approximately zero, but missing contact/cast shadows still make it appear insufficiently grounded. Earlier NPC/monster sprites and unused internal-door state remain separate gaps. [Evidence](../../../../astra_test_01/design/experiments/E07K/REPORT.md).

### E07N · Committed door state must reach every consumer

Connecting the unused internal door to exact geometry/collision/navigation/light passes51headless and300pixel checks. Save pending time, reject occupied closing for both actor sizes, and invalidate routes by obstacle signature plus version. Stale visual and missing collider controls are detected. Committed-state success does not qualify smooth door motion or readable hardware; F01 panel still blends into wall. [Evidence](../../../../astra_test_01/design/experiments/E07N/REPORT.md).

### E07L · Project source geometry once, then shadow the light contribution

One opaque triangle-union mask from the same skinned pilot produces320passing CPU floor-ray witnesses. It avoids overlap darkening and follows root height/pose; missing and stale masks fail controls. Subtract directional light before final clamping. Displayed alpha255 on an opaque canvas does not disprove zero red mask clear; retain the bad assertion and actual context evidence. Hard floor-only shadow improves grounding without qualifying finished lighting or art. [Evidence](../../../../astra_test_01/design/experiments/E07L/REPORT.md).

### E05U · Painted gear detail does not repair base character art

Destination-specific albedo panels plus fitted bracers/greaves pass144idle source comparisons per revision and improve readability. Existing purple shoulders were a separate material omission, repaired without geometry changes. Size-matched F04comparison still exposes a broad smooth coat and simplified rear hair. Hold animation/roster expansion; change base material/silhouette method rather than spending remaining generation on more armor swatches. [Evidence](../../../../astra_test_01/design/experiments/E05U/REPORT.md).

### E05W · Inspect aggregate hair shape and declare active components

A smooth cap alone did not remove the rigid comb outline;17legacy parallel locks were a second cause. Preserve them as explicit disabled components rather than hiding the decision in rendering code.23Head-bound source components,6active, with960clearance rays and144idle comparisons per revision. Material separation plus selected hair composition passes scoped static working appearance; full motion/lighting/production style remain separate. [Evidence](../../../../astra_test_01/design/experiments/E05W/REPORT.md).

### E05Y — full-frame checks expose motion failures hidden by sparse evidence

Complete existing216-frame transfer retains source contacts and paired gear-core clearance, yet visual walk fails with severe body-height changes and split legs. Exact representation and contact metrics are insufficient motion-quality criteria. Full3456pose/view/scale bounds also invalidate the earlier diagnostic sheet size; widen native canvas while preserving scale, and retain failed framing.1290/1296raster comparisons pass; six starter cast135° cases fail the unchanged2%error-fraction bar. Source stance-duration/contact-flag name collision is suspected, not yet proven. Evidence: `astra_test_01/design/experiments/E05Y/REPORT.md` and `review.html`.

### E05Z — keep authored timing constants separate from sampled flags

E05Mstance=.4 was overwritten by an idle-contact Boolean. A1.0second stance-duration control exactly reproduced all49oldwalk palettes and never swung eitherfoot. Immutable stance duration restores supportexchange, meets sourcebars and576/576walk rastercomparisons. This is proven source-authoring causality, not a renderer workaround. Contact/loop tests can pass a visually unusable gait. Keep original failed assets and scope old visual-inference corrections explicitly; see E05M/E05Z_ERRATUM.md and E05Z/REPORT.md.

### E05N — isolate shading normals before changing geometry or artwork

Sixcast135°representation failures persisted with sourcepositions only, disappeared with sourcenormals only. Sparse engine-neutral deformednormaloverrides pass1296/1296unchangedcomparisons; removingthem reproduces2.1984%failure. Preserve immutablepaint/restmesh/palette hashes and resetoverrides perframe. This pilotmethod costs16.736MB/216frames and1.022MBcurrentattributeupload perpose; neither roster nor productionresidency isqualified. See E05N/REPORT.md and cause/rasterreceipts.
