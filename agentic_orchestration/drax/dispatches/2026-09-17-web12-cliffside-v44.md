# Dispatch — web12: cliffside v44 (fire lane FL-6c, dancing flames unclipped) to `/playtest/cliffside/` (Matt-authorized R-C5-132)

**From:** gandalf (RUN-CONDUCTOR, Run C-5) · **To:** drax · **Authorization:** Matt 2026-09-17: "Once you finish with FL-6, please publish it to vercel/mobile so I can test it there too." (`astra_test_01/burst/runs/C-5/ledger.json` R-C5-132). Push to `reincarnated-loadout` `main` is authorized by this ask.

**Source:** `~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/artifacts/CS-pack-v44/godot` (18 kits; props v25 targets; capsule collider; tip sockets; FL-6 dancing flames). Only after gandalf's rendered proof of that pack (`runs/C-5/t3/FL1-fire-8dir-v44/`) — do not build from an unproven pack.

**Procedure:** `~/Games/reincarnated-godot/web/README.md` one-liner (`build_playtest.sh <SOURCE> cliffside` with `PLAYWRIGHT_CORE` set), then the deploy block (`git status --porcelain -- public/playtest` → `add` → `commit --only public/playtest` → `show --stat HEAD` → `push origin main`).

**The web11 lesson (deploy_truth v11):** the pck served was STALE — a uid-cache mismatch produced a grey burst peak. Before export: delete `web/cliffside/.godot/` and re-import headless from scratch; after deploy: fetch `index.pck` from production, sha256 it, and compare against the local `build/web/index.pck` — the sha must match and must differ from web11's (`dc888930…` corrected pck / whatever v11 served). Record both in `agentic_orchestration/drax/captures/2026-09-17-web-playtest-v12/deploy_truth.txt` with the route 200, wasm/pck fetch, and the live boot screenshot (`boot_test.js … ?touch=1 … live`).

**Touch check on production (record in deploy_truth):** Tab to kit index 9 (fire bolt B); cast east from the clearing spawn; six back-to-back screenshots per the README (f2 peak, f3 residue). Verdict lines: cast forward = FORWARD / NOT; burst present = YES / NO; grey peak = NONE / SEEN.

**Report back:** deploy_truth path, the pck sha pair, the loadout commit, and the production URL. Do not touch `astra_test_01/burst/` or any C-5 run file.
