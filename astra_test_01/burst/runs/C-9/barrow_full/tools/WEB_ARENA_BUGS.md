# Web arena parity and mobile bugs — 2026-10-10

Matt reopened the deferred web work after the native Windows package was complete.
The original report was missing 3D/physics features, washed colors, missing monster
art, Vercel login on mobile, and failure to load on his phone.

Native reference: `godot/scenes/bv2f_arena.tscn`.
Public playtest route: https://reincarnated-loadout.vercel.app/playtest/barrow-arena/
See `../audio_review/ARENA_RELEASE_2026-10-10.md` for current deployment and evidence.

| ID | Finding and change | Remaining acceptance |
| --- | --- | --- |
| WEB-01 | Old web packs contained none of the raw `.f32` terrain fields. Current packs contain all 24 active fields, byte-identical to the native source. Hero rig, world meshes, snow, water and 51 enemy VFX sets load in Chrome. | User comparison of any specifically missing objects. Compatibility rendering and reduced textures remain intentional web differences. |
| WEB-02 | The same missing raw terrain inputs affected collision/traversal setup. They are restored. Chrome reports 86,653 walk-floor cells, matching native; 29,264 reachable cells versus native 29,200. Movement and combat advance. | Reproduce any specific interaction that still differs. The small platform-dependent reachability difference is not claimed as exact simulation parity. |
| WEB-03 | The 3D hero was created after the world's web color correction, and an HDR albedo gain clamped its armor colors. Apply the correction to the hero and move that gain into lighting. Captured armor now preserves darker metal/gold detail. | Matt's visual acceptance; WebGL Compatibility is not pixel-identical to native Forward+. |
| WEB-04 | Old web catalogue contained 39 kits. Add the missing burrow worm, crawler larva and EOR overlay; actual packs now contain all 42 native catalogue kits and their referenced strips. | Visual confirmation of every later-wave animation during a full playthrough. |
| WEB-05 | Protected preview link required Vercel authentication. Publish this route on the existing public production alias. | RESOLVED for the public route: all 21 files download unauthenticated with exact release hashes. Preview protection remains enabled. |
| WEB-06 | A phone model/browser and exact failure stage have not been provided. Fresh public Chrome touch emulation passes every skill, movement, Whirlwind, zoom and mutes at 3x DPR. Sustained real touch combat averaged 59.9 FPS. | Physical-phone startup, Safari compatibility, memory, speed, audio unlock and every touch control remain unverified until a device playtest. |
| WEB-07 | First-use animation/shader work caused large action hitches. Prepare first-wave cells, Whirlwind, snow puffs, both zoom sizes and the default score before enabling play. Make perf accounting linear instead of repeatedly summing the entire frame history. | Short first-action/later-wave hitches may remain. Sustained desktop measurements cannot establish zero lag on every phone or all ten waves. |
| WEB-08 | Cold public startup was 214.5 seconds with serial pack downloads. Three bounded concurrent downloads reduce the measured startup to 145.3 seconds (32% shorter), preserving mount order and fail-closed startup. | The 461.8 MB raw payload and remaining loading time still need mobile memory/network testing; no instant-load claim. |

The audit verifies every retained raw scene input, all local presentation scripts,
all selected audio, the sealed runtime/model members and all converted character
strips in the actual exported packs. Historical unused levels are excluded from
web staging. The sealed runtime and model pack are unchanged. Both web and Windows
use the existing reference contact solver; the native Mac can use its compiled solver.
