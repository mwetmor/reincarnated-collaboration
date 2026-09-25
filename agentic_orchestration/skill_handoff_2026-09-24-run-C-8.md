# Session hand-off — Run C-8, the EoR Warlord (gandalf, RUN-CONDUCTOR)

> **SCOPE — READ THIS FIRST.** This hand-off covers **one run: C-8**, the pixel EoR Warlord — its animation matrix, the whirlwind VFX port, and the playable web build. Work performed **2026-09-20 → 21**; doc written **2026-09-24** at Matt's request.
>
> ⚠ **It is NOT a whole-project hand-off and does not supersede `skill_handoff_2026-09-15.md`.** A concurrent run, **KC2-PLAY**, has been live throughout and beyond this session; its charter (`agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`) governs everything in its lane, including its own use of this run's output. Where the two touch, **KC2-PLAY's records govern and this doc defers.**
>
> Everything below cites its id in `astra_test_01/burst/runs/C-8/ledger.json` (9 rulings · 14 milestones · 14 notes · 2 halts).

---

## 0. The one thing to know before touching anything

**C-8 is CLOSED to outside writes, by a ruling from another session.** KC2-PLAY **KP-50** (Matt, 2026-09-21) adopted the EoR Warlord as its player body, superseding the Keeper, and declared `runs/C-8/` **read-and-copy-only** — drax copies the registered PNGs into his own tree and builds his own `SpriteFrames` there rather than writing here.

Matt's words, via that record: *"A separate session created an EOR Warlord with whirlwind VFX that we can use for this scene: `astra_test_01/burst/runs/C-8/cliffside_v40-warlord5`."*

So: **read C-8, copy from C-8, do not write into C-8** unless this run is deliberately re-opened.

---

## 1. What is DONE and standing

| Item | Where | State |
|---|---|---|
| **48 cells, 8 directions** — idle · walk · run · jump · cast · **attack** | `astra_test_01/burst/runs/C-8/cells/` | complete; `matrix_index.json` reports `complete: 48` |
| **Playable build, current** | `runs/C-8/cliffside_v40-warlord5/godot/project.godot` | attack + whirlwind patched; proof clean |
| **Playable on the web, production** | **https://reincarnated-loadout.vercel.app/play** | three characters, select-before-boot, live |
| Whirlwind VFX, 2D port | `runs/C-8/conductor_scripts/whirlwind_patch.py` → `scripts/whirlwind.gd` | ported from the 3D mint; counter-clockwise |
| Attack state (engine-side) | `runs/C-8/conductor_scripts/attack_patch.py` | post-export patch; frozen exporter untouched |
| Cast sockets (mace head) | `runs/C-8/sockets_v1.json` + `runs/C-8/conductor_scripts/mace_sockets.py` | 8 cells; glint rule beats far-point at the release frame |
| Measured fit for the VFX | `runs/C-8/vfx_fit.json` | figure 239 px, body centre (252,270), sole 399, `R_TRAIL_px` 186.97, `R_ENGAGE_px` 278.49 |
| Web build tooling | `runs/C-8/web/{build_char.sh,lossy_sprites.py,assemble_trio.py,verify_trio.js}` | committed `1aa5c706e`, `bd6720b62` — **not pushed** |

**Controls:** arrows/WASD move · **hold F** (or the on-screen WHIRLWIND button) to spin · Space jump · E cast · Shift run. The whirlwind is a **held channel** — a tap reads as broken, which is why the copy says *hold* in all three places.

---

## 2. The five rulings that carry design weight

- **R-C8-2 — the VFX rate is met at PLAYBACK, not at generation.** Grok never held 2.5 rev/s. Each attack cell is **one native revolution resampled** and played at `n × 2.5` fps, so one loop is 0.400 s = the 900 °/s of `reincarnated-godot/scripts/wwcr_whirlwind.gd`. Generator drift is therefore not a defect of the cell.
- **R-C8-4 — phase-roll: one revolution serves all eight facings.** A full 360° spin is direction-agnostic under a fixed camera; the cells loop, so start-phase is free. 16 frames ÷ 8 facings = exactly 2 frames per 45°. Cost: no bespoke per-direction lean. Benefit: the eight attack cells are **perfectly consistent with each other**, the property Matt ruled matters most — *and it is why the attack alone escaped the handedness defect in § 3.*
- **R-C8-5 — turnaround-as-spin.** A whirlwind and a turnaround are the same artifact. Superseded in the end by R-C8-7's clip, but the reasoning stands and the technique is banked.
- **R-C8-6 — fit the VFX by measurement, anchored on the WEAPON.** ⚠ **This one is contested — see § 4.**
- **R-C8-7 — spin sense is counter-clockwise** (Matt: a right-hander sweeps forehand and turns left; right-handed hammer and discus throwers rotate counter-clockwise from above). Achieved by **reversing frame order**, which flips the sense while **preserving handedness** — mirroring would have done the opposite and caused § 3.

---

## 3. OPEN — deferred by Matt, with the cost attached

**Handedness in the mirrored directions.** Three directions are horizontal flips (**W ← E, SE ← SW, NW ← NE**), so the shield and mace trade hands: **15 cells**, those 3 directions across idle/walk/run/jump/cast. **Attack is unaffected** (the phase-roll reuses one unmirrored revolution).

Matt's ruling: **hold until he selects an animation style.** Not worked around, not partially patched.

Cost when he returns to it — native generation of those three directions:

| scope | clips |
|---|---|
| all five states | 15 |
| walk + run + idle | 9 |
| walk only | 3 |

---

## 4. OPEN — the VFX footprint, and why the parked question got harder

drax measured our effect against the reference (`ww7-gate2-cadence-ab-plk0665`), casters normalised to height. Two real gaps, **both parked with Matt, neither a port defect**:

- **contrast** — ribbon luminance 0.68 of the reference's, because the cliffside ground sits at luma 140 against the reference floor's 114; an additive ribbon on brighter ground clips at the apex and vanishes at the tail, truncating 150° of geometry to 60–100° of *visible* arc.
- **footprint** — dust radius 0.51 and sweep radius 0.33 of the reference's, relative to the caster.

⚑ **The footprint number is now known to rest on a bad comparison, and the correction came from the other run.** R-C8-6 anchored the radius on our character's mace reach (0.78 of figure height) rather than the reference's 1.9 × standing height, reasoning that the ribbon is generated from the weapon so the weapon should set the radius. KC2-PLAY **KP-50** then observed that *EoR is 3.0 m against a 1.9 m body = **1.579 body-heights in metres**, while `R_ENGAGE_px` 278.49 over a 239 px figure is **1.165 in canvas pixels** — and those are not the same quantity*, because the canvas is already under the 53° camera. **A horizontal pixel radius over a vertical pixel figure-height is a projection error.**

That is the **same class of mistake** as this run's own `MEASUREMENT-ERROR-1` (§ 6) — comparing across coordinate spaces — made twice, independently, about the same effect. KC2-PLAY commissioned drax to measure it properly through the projection law. **Whoever re-opens the footprint question should take that answer first and not re-derive it here.**

---

## 5. HALTED / queued on Matt

| id | what | state |
|---|---|---|
| `H-C8-GROK-BUDGET` / `-2` | Grok Build balance exhausted, twice | **T31** on `canonical/matt_to_do/README.md`. Clips are the expensive unit; stills are cheap. |
| `T25` | Codex usage limit | blocks the Necromancer's missing N/NE/NW seeds and the exporter `attack` state |
| burst-side tooling push | `1aa5c706e`, `bd6720b62` committed, **not pushed** | the loadout production push was authorised **for that piece only** (R-C8-8); `reincarnated-collaboration` is a **fresh ask** |

---

## 6. THE FINDING OF THIS RUN — nine instruments, one shape

> **An instrument that runs, returns cleanly, and is not answering the question asked of it.**
> **Every single one was caught by eye or by an adversarial reader. Not one was caught by an instrument.**

| # | instrument | what it said | what was true |
|---|---|---|---|
| 1 | SW walk stride autocorrelation | period 48, confidence **0.99** | a two-stride **harmonic**; the high confidence was the tell — a harmonic is twice as regular as the fundamental |
| 2 | mace-height comparison | spread 0.78 vs reference 0.195 → "not on a plane" | **screen-space vs world-space.** A level circle under 0.60 squash *predicts* 0.08–1.02. The mace was largely fine. (`MEASUREMENT-ERROR-1`) |
| 3 | width-normalisation before register | one frame scaled up | a foreshortened mace narrows the bbox; **height** was the invariant |
| 4 | one-off regex on `keeper.tres` | `attack_S` = 80 frames / 2.000 s | began counting at `attack_E` and swallowed four animations (4×16+16) |
| 5 | far-point mace tracker (conductor) | chaotic per-frame deltas | jumping between mace, shield and helm |
| 6 | teal-glint mace tracker (drax) | **the opposite rotation sense** | catching the shield's rim-light as often as the mace |
| 7 | `sense_check()` assertion | "the real verification" *(my words)* | **self-referential** — derives geometry *from* the sign and compares *against* it; passes at either sign (`INSTRUMENT-6`) |
| 8 | physics-frame capture | 190 files, 50 distinct | **below Nyquist** for 2.5 rev/s — a correct spin can alias and read backwards (`NYQUIST-1`) |
| 9 | tapped-F attack probe | "the Warlord's attack is broken" | it is a **held** channel; a tap releases on the next tick |

Three more of the same shape sit inside drax's own reports (a 390-frame clip of a character **standing still** that looked like a finished capture; a deploy poll fooled by a ranged `206` that the 707-byte SPA fallback also returns; a whirlwind check that failed a working build twice on single noisy samples).

**Two second-order lessons, which are the ones worth carrying:**
1. **An instrument that gets adjusted to agree with the build is not an instrument.** #7 shipped asserting a hard-coded "must be clockwise"; on the reversal it would have failed, and the natural repair would have been to edit the expectation.
2. **The conductor is not exempt.** #7 was *me* over-trusting an instrument I had not examined, in the same dispatch where I was warning about instruments.

**Candidate for a discipline mint** at the next ratification pass. jack-ryan's `#78` cl. 3 (*a gate shown only to convict has demonstrated that it fires, not that it discriminates*) is the nearest existing rule and is **not** the same claim — this is about a check aimed at the wrong question, not a gate never shown to acquit. Routing is jack-ryan's per `canonical-doc-format.md § 6.7`.

---

## 7. CONDUCTOR PROCESS DEFECT — recorded against myself

`CONDUCTOR-DEFECT-1`. Commit `2f19cf0b7` swept drax's in-flight edit to `whirlwind_patch.py` (the sign change) into a commit whose message describes only the cell export **and claims "warlord5 exported + proof clean" at a point when warlord5 had not yet been patched or proved.** No content damage; wrong attribution.

**Cause, precisely:** `git add` named explicit files, then `git commit --only -- <a DIRECTORY>`. **`--only` governs**, and a directory `--only` commits the worktree state of everything beneath it — including a concurrent session's edits. The careful `add` was decorative.

**This is one level up from the CLAUDE.md staging amendments.** Those fix *which instrument verifies the staged set*; none of them help when the commit **path** is broad.

> **Standing change to my practice: on this shared worktree, `git commit --only` takes an EXPLICIT FILE LIST, never a directory.**

Correcting commit `1e8e38e4a`. History not rewritten — concurrent sessions had committed on top.

---

## 8. How the animation was actually made (bankable method)

Four `image_to_video` passes each won the attribute its prompt **led with** and relaxed the rest — stance/spin/blur/reach, never together. What broke the deadlock:

1. **Seeds carry pose; prompts carry motion.** The winning clip (`r4`) is the **r2 prompt verbatim** — the only pass that won revolution + crouch + scale + zero blur — with the **seed swapped** to a still whose arm was already correct. The arm became the seed's job.
2. **Describe what the camera sees, not degrees.** "Turned 135°" does not land. "The back of his helmet" does.
3. **Landmarks, not anatomy words.** "Shoulder height" put the mace at head height, because on a chibi the helm spans the top quarter and the shoulder sits at ~0.71. "Level with his belt" is checkable inside a single frame.
4. **A cross-frame absolute is not a constraint an independently-generated still can represent.** "The same height in every frame" failed twice. Anatomy that *implies* the plane works.
5. **Geometric absolutes get drawn as objects.** "Shoulder, arm, haft and mace head form one long straight line" produced a floating barbell.
6. **A slow generated spin is a gift** — 44 native frames per revolution resampled to 16 beats 8 hand-gated stills on both frame count and temporal coherence.
7. **Never describe an arm as foreshortened toward camera** — it produced an empty pointing hand with the mace detached, twice.

---

## 9. Where things are

```
astra_test_01/burst/runs/C-8/
  ledger.json                       9 rulings · 14 milestones · 14 notes · 2 halts
  cells/                            48 cells + matrix_index.json
  cliffside_v40-warlord5/godot/     THE current playable (warlord / 2 / 3 / 4 superseded)
  sockets_v1.json · vfx_fit.json · battle_prompts.json · matrix_prompts.json
  conductor_scripts/                attack_patch.py · whirlwind_patch.py · mace_sockets.py
                                    turn_stills{,_v2,_v3}.py · oneshot_c8.py · assemble_c8.py
                                    probe_attack_c8.gd · probe_whirlwind_c8.gd · heavy_lock.py
  web/                              build_char.sh · lossy_sprites.py · assemble_trio.py · verify_trio.js
  HALT-P6-grok-budget.md

reincarnated-loadout/
  src/pages/Play.tsx · public/playtest/cliffside/   (3 packs + one shared engine)

agentic_orchestration/drax/captures/
  2026-09-20-c8-whirlwind/ · 2026-09-21-c8-whirlwind-w4/ · 2026-09-21-c8-whirlwind-w5/
~/Desktop/Astra Burst Review - 2026-09-20/Packet 104 …/
```

**Superseded builds, kept for lineage, do not play them:** `-warlord` (SW/SE double-speed) · `-warlord2` (original spin, A in the A/B) · `-warlord3` (8-still turnaround) · `-warlord4` (16-frame, clockwise).

---

## 10. If you pick this up

1. Read `canonical/00-ground-state.md`, then **the KC2-PLAY charter** — that run is live and it consumes this one.
2. Treat `runs/C-8/**` as **read-and-copy-only** (§ 0).
3. Matt's two open questions are § 3 (handedness — awaiting his style choice) and § 4 (footprint/contrast — take KC2-PLAY's projection-law measurement first).
4. Before re-firing anything at Grok, check **T31**; before anything needing Astra, check **T25**.
5. **Trust the eye over the instrument** until the instrument has been shown to answer the question asked of it (§ 6). This run went 0-for-9 the other way.

---

**Signed:** gandalf, RUN-CONDUCTOR, Run C-8. The run produced a character; what it *taught* is in § 6.
