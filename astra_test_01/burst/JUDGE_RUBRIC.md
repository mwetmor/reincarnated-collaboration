## 6. JUDGE rubric (extracted into `astra_test_01/burst/JUDGE_RUBRIC.md` by T0)

Five axes, 1–5, one-line reason each. **Mandatory:** axes 1–3 ≥ 4. Composite ≥ 3.8. Judged at native and at 64 px.

| # | Axis | Anchor |
|---|---|---|
| 1 | **Register fidelity** — F04 clarity (clean planes, restrained texture, no grain) | `E07V/art/F04.png` figures |
| 2 | **Identity persistence** vs the approved master (face, hair mass, costume elements, proportions, accessory count) | the approved master |
| 3 | **Light obedience** — key upper-left; spell the only saturated source | `run_03` cast frame (`vfx_style_match.png`, left) |
| 4 | **Silhouette read at 64 px** (rod head + hair / pauldron distinct) | `run_03/character/turnaround_64px.png` |
| 5 | **Brush-register consistency** across frames and with VFX | `run_03/evidence/vfx_style_match.png` |

**Known-bad controls — one hidden control in every JUDGE batch; a judge that passes its control VOIDS the batch:** (a) a horizontally mirrored candidate (key now upper-right) must fail axis 3; (b) `E05W` low-poly pilot crop (`design/experiments/E05W/evidence/batch-04/review.png` figure) must fail axis 1; (c) for plates, `E07V/art/F01.png`'s bottom-right doorway must fail the doorway-side check; (d) for gear, a 20-px-shifted overlay must fail identity. Two VOID judgments in a run → HALT.

