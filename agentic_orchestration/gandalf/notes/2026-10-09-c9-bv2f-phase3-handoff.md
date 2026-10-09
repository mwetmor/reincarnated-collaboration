# C-9 BV2F Phase 3′: handoff at the image-service limit

**STATUS:** CURRENT. **Authored:** 2026-10-09 by gandalf (C-9 RUN-CONDUCTOR). The ledger of record is `astra_test_01/burst/runs/C-9/ledger.json` (rulings through **R-C9-308**). The ledger wins over this note.

## Where it stands
- **barrow_v2 painting: 22 of 25 canvases done.**
  - Pilot 4: kept, plus DEV-24 layers 1–4.
  - Phase 3′ done: 3_0, 4_0, 0_3-r2, 1_3-r2, 2_3, 3_1-r1, 4_1, 3_2-r1, 4_2-r1, 3_3-r1, 4_3, 0_4, 1_4-r1.
- **Halted on the image-service usage limit** (H-C9-BV2F-ASTRA-LIMIT-2). No images were lost.
- **Remaining:** 2_4 (paint it as `-r2`; ids `-` and `-r1` are consumed), then 3_4 and 4_4. Then ONE DEV-24 corner seam patch (~384×384 at plate 1536,3328; R-C9-307), staged on the full-site stitch.
- **Budget left:** Phase 3′ 6 of 44; DEV-24 2 of 24.

## Resume (fresh session)
1. Read this note, then `barrow_v2/fid/RESUME_PT.md`, then ledger R-C9-268..308.
2. Spawn a fresh drax lane PT pointed at `RESUME_PT.md`. Run:
   `PH3_SUF0=-r2 PH3_SUF1=-r3 zsh barrow_v2/fid/pt/tools/ph3_prepare.sh wave 2_4`, then 3_4, then 4_4.
   - The QA stop applies only on a failed check.
   - Standing carries: R-C9-292..305.
   - The snow-spectrum rule: R-C9-305.
3. Then the corner patch. Then the final deliverables:
   - the 5×5 stitched painting (DEV-23/25/26/27/29 + DEV-24 L1–4 + corner);
   - a contact sheet;
   - a QA summary;
   - the M3′ packet: carried joins, disclosed FAILs, and the items for Matt's eye.
4. **After painting:** Gate-2 (jack-ryan), then the full-site BUILD.
   - The build needs disk ≥ 25 GiB; a restart should clear the staged macOS update.
   - P10 needs a quiet host (matt_to_do T34).
   - Run P-4, the full-site stitch proof on the real canvases.

## Items for Matt's eye (in the M3′ packet)
- 0_3: the heart-shaped floe.
- The ash yard's cobble look.
- Pale exposed ice near the stern.
- A small dark block on a pilot floe edge, locked outside the rects.
- A crack-line net over 0_4's open water.
- Stepped, tiered rocks at the cave mouth (blockout).
- Notched outlines on some S-pack floes.

## Disk and host
- Disk 22 GiB (gate 21).
- Matt turned off auto-update. A restart should free the staged 12 GB macOS update.
