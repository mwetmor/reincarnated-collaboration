# Dispatch — web12: cliffside v44 (fire lane FL-6c, dancing flames unclipped) to `/playtest/cliffside/` (Matt-authorized R-C5-132)

**From:** gandalf (RUN-CONDUCTOR, Run C-5) · **To:** drax · **Authorization:** Matt 2026-09-17: "Once you finish with FL-6, please publish it to vercel/mobile so I can test it there too." (`astra_test_01/burst/runs/C-5/ledger.json` R-C5-132). Push to `reincarnated-loadout` `main` is authorized by this ask.

**Source:** `~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/artifacts/CS-pack-v44/godot` (18 kits; props v25 targets; capsule collider; tip sockets; FL-6 dancing flames). Only after gandalf's rendered proof of that pack (`runs/C-5/t3/FL1-fire-8dir-v44/`) — do not build from an unproven pack.

**Procedure:** `~/Games/reincarnated-godot/web/README.md` one-liner (`build_playtest.sh <SOURCE> cliffside` with `PLAYWRIGHT_CORE` set), then the deploy block (`git status --porcelain -- public/playtest` → `add` → `commit --only public/playtest` → `show --stat HEAD` → `push origin main`).

**The web11 lesson (deploy_truth v11):** the pck served was STALE — a uid-cache mismatch produced a grey burst peak. Before export: delete `web/cliffside/.godot/` and re-import headless from scratch; after deploy: fetch `index.pck` from production, sha256 it, and compare against the local `build/web/index.pck` — the sha must match and must differ from web11's (`dc888930…` corrected pck / whatever v11 served). Record both in `agentic_orchestration/drax/captures/2026-09-17-web-playtest-v12/deploy_truth.txt` with the route 200, wasm/pck fetch, and the live boot screenshot (`boot_test.js … ?touch=1 … live`).

**Touch check on production (record in deploy_truth):** Tab to kit index 9 (fire bolt B); cast east from the clearing spawn; six back-to-back screenshots per the README (f2 peak, f3 residue). Verdict lines: cast forward = FORWARD / NOT; burst present = YES / NO; grey peak = NONE / SEEN.

**Report back:** deploy_truth path, the pck sha pair, the loadout commit, and the production URL. Do not touch `astra_test_01/burst/` or any C-5 run file.

---

## Completion record

**Executed:** drax, 2026-09-17. **Status: COMPLETE. The deploy is live and it is clean.**

**Deploy truth:** `agentic_orchestration/drax/captures/2026-09-17-web-playtest-v12/deploy_truth.txt`
(collaboration commit `314d99bb`, committed NOT pushed — captures ride the next conductor push,
same posture as web10/web11).

**Proof gate honoured.** `runs/C-5/t3/FL1-fire-8dir-v44/` was confirmed present before I built.
Nothing under `astra_test_01/burst/` was written.

**PCK SHA PAIR — both halves of the web11 check, and they match.**

| | sha256 | bytes |
|---|---|---|
| LOCAL `build/web/index.pck` | `f7c5ff2496e5e50c43a394d1d0e9d913940df3523539ca7bcf257733bc265d75` | 39637352 |
| LIVE, downloaded from production and hashed independently of the build | `f7c5ff2496e5e50c43a394d1d0e9d913940df3523539ca7bcf257733bc265d75` | 39637352 |
| web11 SHIPPED (defective), for contrast | `d05c9ee729554ea1af1743217c4100b86689ce929f94e93ce2f0d5553ef54f2f` | 36688904 |

The web11 corrective push was never authorised and never made, so production sat on
`d05c9ee7` until this deploy superseded it. This deploy retires that defect.

**Loadout commits:** `762e1ff66953a3d608de1f4095221b6f947291e6` (the build), then
`d8b8238` (AGENT_STATE v1.24). Pushed `f3bb7d4..d8b8238` on `main`.
**Production URL:** https://reincarnated-loadout.vercel.app/playtest/cliffside/

**Routes:** `/playtest/cliffside/`, `/index.html`, `/index.js`, `/index.wasm`, `/index.pck`,
the slash-less path and the `/playtest/` landing all 200 with the right content types.
**Live boot:** `live_01_boot.png`, booted=true, boot_ms=8164, 0 pageerror, 0 Godot ERROR.

**The web11 lesson:** `web/cliffside/.godot` moved out of the tree before the build (to a
scratch dir OUTSIDE `$DEST` — the README's "move it aside" still puts the backup where the
next `rsync --delete` eats it). Import/export logs: 0 errors, 0 warnings, 0 `invalid UID`.
Dangling-`res://` fence passed. On production: 0 Godot ERROR lines across both runs, where
web11's signature was six per run.

### ⚑ THE THREE VERDICT LINES

```
cast forward  ...  FORWARD
burst present ...  YES
grey peak     ...  NONE
```

Tab ×9 → kit index 9, HUD confirms `fire_bolt_e1_B`; cast east from the clearing spawn;
three casts, six back-to-back screenshots each; genuine CDP touch, mouse never moved.

**NONE is a measurement, and the web11 instrument would have filed a false defect report.**
Run unmodified, web11's criterion (saturation < 28, max channel > 110) reads **11-13 %** on
this kit — which looks exactly like the defect returning. It is not. `fire_bolt_e1_B` has a
white-hot core by design, and near-white is desaturated; the criterion cannot tell a
white-hot core from an unshaded index map. Split by max channel:

| | white-hot core (≥235) | UNSHADED-GREY (110-235) |
|---|---|---|
| control, two adjacent no-VFX frames | 0.00 % | 0.86 % / 2.52 % |
| cast 1 impact fan | 12.90 % | **0.21 %** |
| cast 2 bolt aloft | 11.01 % | **0.00 %** |
| cast 3 bolt aloft | 11.33 % | **1.03 %** |

Every unshaded-grey reading is at or below the no-VFX control floor. Cross-checked on
web11's own archived exhibits with the same instrument: its defect lived in the 110-200
mid-grey band (1.16 % vs the clean rebuild's 0.73 %). Different population; the one that
mattered is absent. Mechanism agrees — a dangling shader announces itself in the console
and there are none. Script and both corrections: `grey_measure.py`.

### ⚑ Two things the next conductor should carry forward

**1. The bolt-kit peak is at f0, not f2.** web11's "f2 peak, f3 residue" holds for BURST
kits and is wrong for BOLT kits: the projectile spawns on touchStart and the first
screenshot lands ~200 ms later, so the peak is already at f0 and by f3 the event is over
(the f3-f5 window measures 0 changed VFX pixels). I checked f2 first, saw an empty frame,
and briefly had a case that the kit had not fired. It had.

**2. The license fence failed this build as a FALSE POSITIVE, and it is fixed.**
`vfx_(frost|fire|…)_(bolt|impact)` had no trailing boundary, so `vfx_fire_bolt` matched as
a PREFIX of the self-authored `vfx_fire_bolt_e1_A_impact` — seven of v44's own files
rejected. v44 is the first pack with a `fire_bolt_*` kit, so the fence had never met the
case it gets wrong. Exact-name boundary added in both copies; **reincarnated-godot commit
`90ef2c5a`, COMMITTED NOT PUSHED** — this dispatch authorises a push to `reincarnated-loadout`
and says nothing about `reincarnated-godot`, and CLAUDE.md's standing pattern explicitly does
not extend there. Re-verified against the two library-bearing packs (CS-pack-v8b, CS-pack-v14):
180 hits each under both the old and new patterns, **LOST 0**. Their real filename shapes were
enumerated, not assumed — my first regression case asserted a `vfx_frost_bolt_material.gd`
form that I had invented and that exists in neither pack.

**Open ask for Matt:** none from this deploy. The pack renders as authored.
