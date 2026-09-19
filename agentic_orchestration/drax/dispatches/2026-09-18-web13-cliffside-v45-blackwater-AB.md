# Dispatch — web13: cliffside v45 (Blackwater A/B — runtime vs video-spine, 19 kits) to `/playtest/cliffside/` (Matt-authorized R-C7-5)

**From:** gandalf (RUN-CONDUCTOR, Run C-7) · **To:** drax · **Authorization:** Matt 2026-09-18, R-C7-5 in `astra_test_01/burst/runs/C-7/ledger.json`: load the finished Blackwater into the current cliff scene — *"(a) web13 as soon as v45 stages, before the A/B verdict, so the A/B is played on the phone."* **Push gate:** build, stage, verify and HOLD; the `git push` to `reincarnated-loadout` fires only when gandalf relays Matt's word in this file's completion record (the conductor told Matt he would ask at push time — keep that promise).

**Source:** `~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/artifacts/CS-pack-v45/godot` (19 kits = v44's eighteen + `blackwater_cocktail_e3_V`, arm B: the video-spine flipbook field body — picker slot 19; arm A `blackwater_cocktail_e3` = slot 12, byte-identical to v44; props v25 targets; capsule collider; tip sockets; FL-6c dancing flames). **Proof gate:** build only after gandalf's rendered A/B proof exists at `runs/C-7/t3/AB-v45/` (A_E / B_E / A_W / B_W sheets + MP4s) — check the directory, as for web12.

**Procedure:** exactly web12's (`agentic_orchestration/drax/dispatches/2026-09-17-web12-cliffside-v44.md` + `deploy_truth.txt`): `~/Games/reincarnated-godot/web/README.md` one-liner (`build_playtest.sh <SOURCE> cliffside`, `PLAYWRIGHT_CORE` set), `web/cliffside/.godot` moved OUT of the tree before the import (the web11 lesson), dangling-`res://` fence, size report, stage into `reincarnated-loadout/public/playtest/cliffside/`, local boot test. Then `git status --porcelain -- public/playtest` → `add` → `commit --only public/playtest …` in the loadout repo — **and STOP before the push.** Record the local pck sha + bytes; after the push (on the relayed word) fetch the live `index.pck` and hash it independently — the pair must match.

**What is new in v45 (read the source before building):** one kit added, `vfx/blackwater_cocktail_e3_V/` — 145 frames under `primitives/spine/` (four-plane greyscale RGBA, 485×581, coloured by the kit's palette material at runtime), a `g2_flipbook` scene/script path, the G2 script dispatching on `body_mode`. Expect the pck to grow by roughly the frames' size (~0.35 MB of PNG source; larger after Godot's import). Every other kit's exported tree is byte-identical to v44 (`runs/C-7/t3/BL-2v/byte_identity.json`).

**Touch check on production (record in deploy_truth):** Tab to slot 12 (A) — cast east from the clearing spawn; then Tab to slot 19 (B) — cast east THREE times ~4 s apart. Six back-to-back screenshots per cast per the README. Verdict lines: `A casts forward = FORWARD/NOT` · `B frame 0 at the landing point = YES/NO` · `B pool boils (not a still) = YES/NO` · `B scorch persists after the pool dies = YES/NO` · `three B scorches coexist after three casts = YES/NO` · `smoke over the B pool = YES/NO` · `grey/unshaded pixels in either pool = NONE/PRESENT`.

**Report back:** deploy_truth path, the pck sha pair, the loadout commit, the production URL, the seven verdict lines. Do not touch `astra_test_01/burst/` or any C-7 run file; do not push `reincarnated-godot` (the standing pattern does not extend there).

---

## Completion record

*(drax fills in.)*
