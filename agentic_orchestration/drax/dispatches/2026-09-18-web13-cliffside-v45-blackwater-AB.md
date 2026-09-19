# Dispatch — web13: cliffside v45 (Blackwater A/B — runtime vs video-spine, 19 kits) to `/playtest/cliffside/` (Matt-authorized R-C7-5)

**From:** gandalf (RUN-CONDUCTOR, Run C-7) · **To:** drax · **Authorization:** Matt 2026-09-18, R-C7-5 in `astra_test_01/burst/runs/C-7/ledger.json`: load the finished Blackwater into the current cliff scene — *"(a) web13 as soon as v45 stages, before the A/B verdict, so the A/B is played on the phone."* **Push gate:** build, stage, verify and HOLD; the `git push` to `reincarnated-loadout` fires only when gandalf relays Matt's word in this file's completion record (the conductor told Matt he would ask at push time — keep that promise).

**Source:** `~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/artifacts/CS-pack-v45/godot` (19 kits = v44's eighteen + `blackwater_cocktail_e3_V`, arm B: the video-spine flipbook field body — picker slot 19; arm A `blackwater_cocktail_e3` = slot 12, byte-identical to v44; props v25 targets; capsule collider; tip sockets; FL-6c dancing flames). **Proof gate:** build only after gandalf's rendered A/B proof exists at `runs/C-7/t3/AB-v45/` (A_E / B_E / A_W / B_W sheets + MP4s) — check the directory, as for web12.

**Procedure:** exactly web12's (`agentic_orchestration/drax/dispatches/2026-09-17-web12-cliffside-v44.md` + `deploy_truth.txt`): `~/Games/reincarnated-godot/web/README.md` one-liner (`build_playtest.sh <SOURCE> cliffside`, `PLAYWRIGHT_CORE` set), `web/cliffside/.godot` moved OUT of the tree before the import (the web11 lesson), dangling-`res://` fence, size report, stage into `reincarnated-loadout/public/playtest/cliffside/`, local boot test. Then `git status --porcelain -- public/playtest` → `add` → `commit --only public/playtest …` in the loadout repo — **and STOP before the push.** Record the local pck sha + bytes; after the push (on the relayed word) fetch the live `index.pck` and hash it independently — the pair must match.

**What is new in v45 (read the source before building):** one kit added, `vfx/blackwater_cocktail_e3_V/` — 145 frames under `primitives/spine/` (four-plane greyscale RGBA, 485×581, coloured by the kit's palette material at runtime), a `g2_flipbook` scene/script path, the G2 script dispatching on `body_mode`. Expect the pck to grow by roughly the frames' size (~0.35 MB of PNG source; larger after Godot's import). Every other kit's exported tree is byte-identical to v44 (`runs/C-7/t3/BL-2v/byte_identity.json`).

**Touch check on production (record in deploy_truth):** Tab to slot 12 (A) — cast east from the clearing spawn; then Tab to slot 19 (B) — cast east THREE times ~4 s apart. Six back-to-back screenshots per cast per the README. Verdict lines: `A casts forward = FORWARD/NOT` · `B frame 0 at the landing point = YES/NO` · `B pool boils (not a still) = YES/NO` · `B scorch persists after the pool dies = YES/NO` · `three B scorches coexist after three casts = YES/NO` · `smoke over the B pool = YES/NO` · `grey/unshaded pixels in either pool = NONE/PRESENT`.

**Report back:** deploy_truth path, the pck sha pair, the loadout commit, the production URL, the seven verdict lines. Do not touch `astra_test_01/burst/` or any C-7 run file; do not push `reincarnated-godot` (the standing pattern does not extend there).

---

## Completion record

**Executed:** drax, 2026-09-19. **Status: BUILT, STAGED, VERIFIED, COMMITTED — HELD BEFORE PUSH.**

**Deploy truth:** `agentic_orchestration/drax/captures/2026-09-19-web-playtest-v13/deploy_truth.txt`

**Nothing is pushed.** `reincarnated-loadout` `main` is **ahead 1** of `origin/main` and stays
there. `reincarnated-godot` is untouched this session (its web12 build-script commit `90ef2c5a`
is still committed-not-pushed, as web12 left it). The push fires only on gandalf's relay of
Matt's word — **see § PUSH RELAY below, which is the line to fill in.**

**Proof gate honoured, checked BEFORE the build.** `runs/C-7/t3/AB-v45/` exists and is
populated — A_E / B_E / A_W / B_W sheets, realtime + third_speed MP4s for all four,
`events_A_E.log`, `events_B_E.log`, `import_v45.log`. Nothing under `astra_test_01/burst/`
was written.

| | sha256 | bytes |
|---|---|---|
| LOCAL `build/web/index.pck` | `ac513a0f06e572856c0cc34473a4287c747245192ecfafa53af3c30c47e6bb18` | 40677216 |
| STAGED in the loadout commit | `ac513a0f…` (match) | 40677216 |
| LIVE | **PENDING PUSH** | — |
| web12, currently serving | `f7c5ff2496e5e50c43a394d1d0e9d913940df3523539ca7bcf257733bc265d75` | 39637352 |

**Loadout commit:** `822a089f1ee6c93199b00623e10c6706080e697a` — exactly two files
(`index.pck`, and `index.html` whose only change is the `fileSizes` stamp). **+1 039 864 B**,
and it is all one kit: `blackwater_cocktail_e3_V`, 145 spine frames. Every other kit
byte-identical to v44.

**Build clean.** `.godot` moved OUT of the tree before the import, to a scratch dir *outside*
`$DEST` (the web12 correction to the README's "aside"). Import + export logs: 0 errors,
0 warnings, 0 `invalid UID`. License fence and dangling-`res://` fence both passed. Local
boot `booted=true`, `boot_ms=6530`, 0 pageerror, 0 Godot ERROR.

**Kit order enumerated, not assumed.** The dispatch's picker slots are 1-indexed; `VFX_KITS`
is 0-indexed. **Slot 12 (A) = index 11 `blackwater_cocktail_e3`; slot 19 (B) = index 18
`blackwater_cocktail_e3_V`.** From a fresh boot: Tab ×11 reaches A, Tab ×18 reaches B. HUD
label confirms both.

### The seven verdict lines — PENDING PUSH

Production is still serving web12, so all seven read `PENDING PUSH` in `deploy_truth.txt`.
They are not back-filled from the local run: a verdict about what a phone shows is not
answered by a build machine.

### ⚑ Two things the conductor needs before the production pass

**1. An upstream defect exists on arm B, it is in YOUR artifact of record, and I did not
patch it.** Arm B logs exactly three console errors locally — one per cast, none on arm A:
`Cannot open file 'res://vfx/blackwater_cocktail_e3_V/materials/Additive.tres'`, at
`keeper.gd:276`. That branch hardcodes the V kit's `materials/Additive.tres` for the muzzle
flare; every other e3 kit emits that file and **the V kit does not** (its `materials/` holds
only `Body.tres`, `Field.tres` and two shaders — verified in the source pack). The identical
pair of lines at the identical line number is in `runs/C-7/t3/AB-v45/events_B_E.log`, so the
A/B proof was rendered with it present and my pck reproduces the pack exactly. Blast radius
is bounded: the flare draws non-additive; the flipbook **field body is unaffected** (it uses
`Body.tres`/`Field.tres`). **This is the same shape as F-C7-1** — the V kit naming an asset
the emitter does not emit — which makes it the second instance and argues for a sweep rather
than another one-off. Raising, not patching: I do not author pack content.

Related fence gap, named rather than widened mid-hold: the dangling-`res://` fence walks
`.gdshader` paths only (shaders bit web11). A missing `.tres` is the same failure with a
different extension. Widening it naively would fire false positives on remapped/generated
`.tres` paths — the exact defect web12 had to correct in the license fence — so it is logged
with its cost, not rushed into a held deploy.

**2. The pale pool interior is NOT a build defect — I checked instead of guessing.** Arm B's
pool reads near-white in the middle, which is precisely what the "grey/unshaded pixels"
verdict hunts, and the spine frames are greyscale coloured at runtime, so an unbound palette
would look like exactly this. It is not that: **`AB-v45/B_E_sheet.png` shows the same pale
interior, same dark-red rim, same flame tongues, same boil-then-collapse-to-scorch arc.** The
web build reproduces the proof. Whether that read is *wanted* is the A/B question for Matt's
eye, not a question about these bytes.

**3. Procedural, and it invalidates a verdict line if ignored.** My three local B casts were
fired from a standing position, so all three landed on the same point and merged into **one**
scorch. *"three B scorches coexist"* cannot be read off a stationary run at all — it would
read NO for a reason unrelated to the kit. **The production pass must move the Keeper between
casts.** Same family as web12's f0-vs-f2 lesson: shape the harness to the question or it
answers a different one cleanly.

### PUSH RELAY — gandalf fills this in

```
Matt's word relayed:   [ PENDING ]   by: ________  on: ________
```

On that word: push `822a089`, then close out `deploy_truth.txt` § WHAT IS STILL OWED —
live pck sha (must equal `ac513a0f…`, must differ from `f7c5ff24…`), production HTTP block,
live boot screenshot, the A/B touch pass and the seven verdict lines, the capture commit,
and loadout `AGENT_STATE.md` v1.25.

**Open ask for Matt:** none from the build. The pack renders as authored, including the one
upstream flare-material error that the artifact of record also carries.
