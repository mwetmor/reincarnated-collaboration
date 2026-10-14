# C-9 session handoff: barrow_v2 ratified, north extension, the barrow arena on Vercel

> **STATUS:** CURRENT (working-memory, session pointer). **Author:** gandalf (C-9 RUN-CONDUCTOR). **Date:** 2026-10-13.
> **Read first:** the canonical procedure `canonical/reap-die-rise-game/painted-2d-pipeline/painted-site-scene-and-arena-pipeline.md`; the ledger `astra_test_01/burst/runs/C-9/ledger.json` (rulings through R-C9-397); the review `agentic_orchestration/gandalf/notes/2026-10-13-c9-arena-astra-completion-review.md`.

## 1. Where things stand

| Item | State | Record |
|---|---|---|
| barrow_v2 painting, site_ph3 | **Ratified** (M3′). Painting closed. | R-C9-350, M-C9-BV2F-M3P-RATIFIED |
| North extension, site_ph4 (6656×4864) | Built. Identity proof PASS; seam tone and shape PASS. Pool removed. N1 images 12/14. | R-C9-384..389, M-C9-BV2F-SITE-PH4-BUILT, PT a5c6cad09 |
| The arena, the fight inside barrow_v2 | Playable locally and **public** at https://reincarnated-loadout.vercel.app/playtest/barrow-arena/ | R-C9-345..396; drax commits through e2b234846; Codex commits c6ac9b55f..56a5024bc |
| Canon | The pipeline is canonized; the 2D workflow carries a partial-supersession banner; the game tracker has a 2026-10-13 delta. | this session's commit |

**Local play:**
```
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full/godot && /Applications/Godot.app/Contents/MacOS/Godot --path . res://scenes/bv2f_arena.tscn
```
Defaults: site_ph4, the 3D warlord at light 1.5, painted-v1 snow, enemy VFX on, interpolation on, doorway entry on.

Fallback flags:
- `--arena-hero sprite`
- `--arena-site ph3`
- `--arena-vfx off`
- `--arena-interp off`
- `--arena-entry off`

## 2. Open, in rough priority

1. **Matt's ratifications:**
   - **DEV-30**, the north-band stager.
   - **WARN-1**, the arena's platform-solver fallback on web and Windows: it selects the runtime's own GDScript reference solver and clears the refusal. Pair it with a same-seed native-vs-GDScript probe.
2. **Whirlwind smoke missing** (R-C9-396, deferred by Matt). Suspect the R-C9-392 mace emission in `eor_kc2_fx.gd` / `arena_warlord3d.gd`.
3. **Phone confirmation** of the public build (WEB-06). The export is about 650 MB before compression (WEB-08); trim per-wave packs if phones struggle.
4. **Monsters as live 3D rigs.** All 45 en-* source GLBs are on disk. Strips are baked at 12 frames per clip and read as choppy. Parked by Matt until the plan finished; the plan has now finished.
5. **Small items:**
   - the NE snow slope by the barrow (Matt's call whether it reads as a bank);
   - two slow-return probe spots (sea-cliff stair, palisade post 41), not traps;
   - the slash is presentation-only (0.1× a whirlwind tick; R-C9-373).
6. **T34 quiet window:** P10 frame-rate run (§66 west-shore loop + parked sea hold). Reported, not gating.
7. **Host:** a Mac restart frees about 12 GB of staged macOS update. Disk was about 28–30 GiB free at last check.
8. **Untracked files of unknown owner** in barrow_full/godot: `data/bv2f/stair_snow/`, `tools/probe_burn_cost.gd`, `tools/probe_eor_q.gd`. Not swept into any commit; ask before touching.

## 3. Standing constraints, carried

- **Ledger and git:**
  - The conductor alone commits the ledger: `git commit --only`; `git status --porcelain` before, `git show --stat HEAD` after; `git -C` across repos.
  - Collaboration push-as-you-go (R-C9-164). Loadout: push once, check once.
- **Permissions:**
  - Never route around a permission refusal, and never edit your own permissions.
  - Matt's standing rules: Read, Edit and Write on `…/C-9/barrow_full/godot/**`, and the Godot binary.
- **Disk and cleanup:**
  - Lanes halt at 21 GiB; the conductor gate is 20 (one-time releases recorded).
  - The conductor runs build-safe cleanup manifests: untracked only, excluding build inputs and cited files. A raw `rm` outside the repo is Matt's.
- **Shared Mac:** kill only your own PIDs; small auto-quit test windows.
- **Asking Matt:** one recommendation per question.
