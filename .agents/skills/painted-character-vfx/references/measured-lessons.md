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
