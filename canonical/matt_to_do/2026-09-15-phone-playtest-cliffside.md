# Matt to-do — test the cliffside web playtest on a real phone (and share the link)

> **STATUS:** OPEN — filed by gandalf 2026-09-15 (Run C-3, R-C3-102/110; drax deploy). Unblocks: the friends' phone playtest; the mobile-memory decision below.

- **URL:** https://reincarnated-loadout.vercel.app/playtest (landing) → game at `/playtest/cliffside/`. Landscape; left half = joystick (push past 60 % to run), right = CAST / JUMP / VFX. ~45 MB first load (Wi-Fi).
- **What to look for:** does it boot on your iPhone/Android at all (iOS memory is the risk — ~700 MB of decoded textures, most of it the 416 Keeper frames at 512²); frame rate while running; whether the mist layer draws (its texture is 4340 px wide, over some older Android GPUs' 4096 limit); black bars on wide phones (fixed 16:9).
- **If it crashes/reloads on iOS:** say so — the fix is mobile GPU texture compression (ASTC/ETC2; larger .pck) and/or trimming the Keeper frame set for web; drax has the repeatable build script (`reincarnated-godot/web/build_playtest.sh`).
- Optional: `vercel login` on the Mac if CLI preview deploys are ever wanted (git-push deploys work without it).
