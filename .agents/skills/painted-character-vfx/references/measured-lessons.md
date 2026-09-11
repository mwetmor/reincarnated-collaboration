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
