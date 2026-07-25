# DISPATCH — TCP-L6-PREP: does Matt's Synty animation corpus reach a rendered swing?

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Trigger:** Matt supplied six Synty animation packs and asked *"Will these work?"*
**Standing:** TCP-38 ③ registered an L6 blocker — 2,178 `.glb` with **zero** animation channels,
the animated corpus all `.fbx` with no runtime import path. **These packs may dissolve it.**
**TCP-30 binds: I will not answer a capability question by reasoning. Answer it with a frame.**

## §0 — What the conductor already measured (facts, not a steer)

`~/Games/reincarnated-collaboration/matt_notes_handoff_docs/recent-synty-packs/synty-animations/` —
**3,386 `.fbx`**, binary (Kaydara), across six packs: `base-locomotion` 721 · `bow-combat` 1052 ·
`idles` 670 · `goblin-locomotion` 417 · `emotes-taunts` 283 · `sword-combat` 243. Trees are
`Animations/{Sidekick,Polygon}/{Masculine,Feminine,Neutral}/…` — **both rig generations ship, and
our hero already uses the Sidekick rig** (`hero_walker.gd`'s Sidekick→GeneralSkeleton bone map).
`sword-combat/Models/` carries `SM_Wep_Sword_01.fbx`, `ModularSyntyCharacter.fbx`, `KidRig_01`,
`BigRig_01`; `goblin-locomotion` is a monster rig. Four `.controller` files are Unity
AnimatorControllers — **unusable by Godot, readable as Synty's intended state machine.**

## §1 — The question, in three decidable parts

1. **DOES IT IMPORT?** Godot 4.3+ imports FBX through **ufbx**, built in, no external FBX2glTF. Does
   a Synty animation FBX import cleanly on 4.6.3 — skeleton, bone names, `AnimationPlayer`, clip
   length?
2. **★ CAN IT BE DONE WITHOUT A HUMAN AT THE GUI?** `godot --headless --import` exists for CI.
   **If it works, TCP-38 ③'s "capability fork" softens from *H cannot* to *H pays a one-time import
   pass* — and that changes what L6 measures.** If it does not, the fork is real and the wires own
   rigged content. **Either answer is a finding of the first rank; do not favour one.**
3. **★★ DOES THE `.glb` ROUND-TRIP CARRY THE ANIMATION?** Hypothesis worth testing precisely because
   it would make the corpus first-class for headless H forever: **import FBX once → in-engine
   `GLTFDocument.append_from_scene()` + `write_to_filesystem()` → `.glb` with animation channels →
   runtime-loadable by anything, no import cache.** Verify by loading the emitted `.glb` in a project
   that never imported it and playing the clip. If channels survive, our whole animated corpus
   becomes available to the route we have been calling production.

## §2 — Scope: a probe, not a pipeline

**Home: `~/Games/mcp-lab/l6prep/` — a new project.** Do **not** import into `reincarnated-godot`
(3,386 FBX would swamp its cache) and **not** into `mcp-lab/harness/` (its no-`.godot` property is
load-bearing and deliberate). `mcp-lab/project/` is the concurrent L5-D cell's floor — **forbidden.**

**Import a HANDFUL, chosen to answer the question:** one Sidekick character, `SM_Wep_Sword_01`, one
idle, one locomotion clip, **one sword swing**, and **one goblin clip** (monsters are L6's subject).
Six-ish files. Not the corpus.

**The weapon-in-hand question is in scope and is the reason the sword is on the list:** does the
imported skeleton expose a hand bone a `BoneAttachment3D` can carry the sword on, and does the sword
stay in the hand through the swing? A weapon that detaches mid-arc is exactly the class of defect a
still cannot show — which is why the harness exists.

## §3 — The answer is a picture (L-A)

Render through **`~/Games/mcp-lab/harness/`** — your own rig, `seek_all_players(node, t)` is the
one-line bridge you shipped. **A ≥2 s clip at ≥24 fps of a Sidekick character swinging a sword,
weapon in hand, at an ARPG camera** — plus the film-strip. If the character reaches the harness only
as an emitted `.glb`, that is the §1.3 answer arriving as a picture, which is the best possible
outcome.

**Accumulator lockout binds (TCP-38 ①);** if you need glow, declare a tolerance first.

## §4 — Exit predicate

1. §1.1/§1.2/§1.3 each resolved to a recorded fact or `UNRECOVERABLE` — **with the command lines**.
2. The clip + film-strip; weapon-in-hand verified across the arc, not at one frame.
3. **Bone-name/rig report:** do the pack's Sidekick clips address the same bones as our hero's
   imported skeleton? Is a Godot bone-map/`SkeletonProfileHumanoid` retarget needed, and does
   `rest_fixer`/`fix_silhouette` come into it? Name the gap if there is one; **do not fix it** —
   scoping that is L6's job, not this probe's.
4. **Root motion:** do the locomotion clips translate the root or run in place? One sentence; it
   decides how L6 stages movement.
5. Rulings + read-list + wall-clock (authoring separate from execution, TCP-32).
6. Hygiene: `mcp-lab/project/` untouched — state it; `reincarnated-godot` **read-only** (its
   `project.godot` carries a pre-existing uncommitted line that is not yours); `user://` clean.
   **The probe project stays** if §1.3 works — it is the corpus's front door.

**Honorable fallback (L-F):** a blocked probe that names *which of the three questions blocked and
why* is a PASS. **Ceiling-finding is a PASS (L-G).**

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md`
**HALT to gandalf:** any temptation to import the full corpus; any need to write in
`reincarnated-godot` or `mcp-lab/project`; a finding that re-scopes L6.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). §0 is a census I ran myself — **treat every
sentence in it as a hypothesis, including the ones about which rig our hero uses.** TCP-39 is the
standing record of what happens when I describe a mechanism I did not read.

---

## Completion record

**Executed by:** drax (presentation seam) · **2026-07-25, 16:51 → 17:28 EDT (37 min)**
**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md`
**Status: PASS — all three questions resolved to recorded facts, none `UNRECOVERABLE`.**

### §1 — the three questions

| # | answer | headline evidence |
|---|---|---|
| **1.1 imports?** | **YES** | `Skeleton3D` + `AnimationPlayer` + correctly-named clip of correct length, 11/11 FBX. Only errors are missing `.psd` texture refs. Tracks are position+rotation only, no scale. |
| **1.2 ★ headless?** | **YES** | `godot --headless --import --path <proj>` → **exit 0, 2.78 s**, 7 FBX, from a directory with **no `.godot/` at all**. No GUI, no operator. |
| **1.3 ★★ round-trip?** | **YES** | `append_from_scene` + `write_to_filesystem` → `.glb`; re-loaded via `append_from_file` in `tcp-l6prep-verify`, **a project holding zero assets**. Channels, lengths **and root translation** all survive. |

**TCP-38 ③ softens as gandalf framed it:** from *"H cannot reach rigged content"* to
*"H pays a one-time import pass."* **The wires do not own rigged content.**

### §2 — the picture

`~/Games/mcp-lab/harness/out/l6prep_sidekick_swing/` — **100 frames @ 40 fps = 2.500 s**,
1280×720, mp4 + gif + 12-thumb timestamped strip + `render.log` with a full per-frame arc trace.
Subject reaches the harness **only as an emitted `.glb`**, which is §1.3's answer arriving as a
picture. Accumulator lockout **held; no tolerance declared or needed.**

**Weapon-in-hand across the arc, not at one frame:** grip-to-socket separation over 101 samples —
min **0.000000000 m**, max **0.000000000 m**, **drift 0.000000000 m**, while the socket travels
1.783 m and the blade tip peaks at **46.7 m/s**.

**Bonus:** the harness's determinism property, previously proven only for scripted motion, **holds
for a rigged `AnimationPlayer`-driven skeleton** — 100/100 byte-identical across processes, matching
MP4 sha256. `seek_all_players` needed **no change**; the harness required no modification at all.

### §3 — bone/rig gap, NAMED not fixed

**Name-match is not rig-match.** Pack clips share **98.7%** of their bone names with the pack
character and still cannot drive it: per-bone rest deltas are **~28° mean / 180° max**. The failure
mode is a character whose **head sits at y = −0.69** with a **perfectly intact skin** — invisible to
every name-based check, and it cost a render to see.

**A `sidekick_bone_map` → `SkeletonProfileHumanoid` / `GeneralSkeleton` retarget with
`rest_fixer/fix_silhouette` IS required, on BOTH sides.** Measured on our hero, same FBX imported
two ways: a raw pack clip binds **54%** to the raw hero and **6%** to the retargeted hero — the two
name spaces do not mix, and `reincarnated-godot` ships the retargeted one. `fix_silhouette` is
load-bearing (`hero_walker.gd` records why). **Scoping is L6's**; the probe's patched `.import`
sidecars are a working example. Open sub-item for L6: the **121-bone base-locomotion pack inverts an
88-bone pack character even after retarget**, while the 91-bone packs retarget cleanly — which
character a clip binds to changes whether the retarget succeeds.

### §4 — root motion, one sentence

**Synty ships every locomotion and attack clip twice — the plain name is in place with no `root`
position track at all, and the `_RM_` twin carries a real root translation track (walk **+1.500 m**
per 1.033 s cycle = 1.452 m/s; the sword combo **+0.500 m** as a lunge) — so L6 chooses its regime
per clip rather than authoring one.**

### §0 hypotheses corrected

- **"`goblin-locomotion` is a monster rig" — FALSE.** It is goblin-*flavoured* locomotion on the same
  humanoid Sidekick rig (98.4% name-bind to the pack character).
- **"our hero already uses the Sidekick rig" — TRUE**, confirmed from the build; but the hero is
  **50 bones** and lives in the *renamed* `GeneralSkeleton` space.
- **Two of the six packs are already vendored** in `reincarnated-godot/Assets` (`anim-base-locomotion`,
  `anim-goblin-locomotion`). Genuinely new: **bow-combat, idles, emotes-taunts, sword-combat**.
- §0's `sword-combat/Models/` list was incomplete (also `POLYGONRig_01`, `PolygonSyntyCharacter`,
  `SM_Generic_SkyDome`).

### Findings that re-scope L6 (flagged per the HALT clause, not acted on)

1. The retarget patch must be applied to **every** pack clip's `.import` — mechanical, and
   `--headless --import` applies it unattended. 3,386 files.
2. Pipeline shape is **forced and favourable**: a bare animation FBX cannot round-trip (glTF has no
   skeleton without a skinned mesh), so it is **one `.glb` per character carrying its whole clip
   library** — 3,386 files collapse to a handful of artifacts. `sidekick_library.glb` is 1.5 MB for
   one character and five clips.
3. **Mount weapons on `prop_r`** — the Sidekick rig ships `prop_l`/`prop_r` sockets and the
   sword-combat clips animate them.
4. **`BoneAttachment3D` must not be used inside a harness clip**: its once-per-frame deferred refresh
   violates `set_time()` purity and fakes up to 0.54 m of weapon drift.
5. **Raised, untouched:** `hero_walker.gd:44` declares `STRIDE_PER_CYCLE := 1.35`; the clip it drives
   measures **1.500 m/cycle** — an ~11% foot-skate error in the shipped hero walk.

### Instrument bugs — four, all mine

Each produced a **confident wrong answer about Matt's assets**: work run in `_initialize()` (reported
*"POSE IS DEAD"* for three intact files); `position_track_interpolate` at `length` on a `LOOP_LINEAR`
clip (reported **0.0 m** travel for a clip that moves **1.5 m** — a false negative on the probe's most
valuable property); sampling `BoneAttachment3D` many times per frame; a sanity gate that also ran in
`_initialize()` and measured rest pose. **~1/3 of authoring time went to fixing the frame before
trusting its output.**

### Hygiene

- **`mcp-lab/project/` — UNTOUCHED**, verified by mtime; the L5-D cell's floor was never entered.
- **`mcp-lab/harness/` — no `.godot/` acquired**; one file added (`clips/l6prep_sidekick_swing.gd`).
- **`reincarnated-godot/` — READ-ONLY honoured**; four files copied *out*, nothing written. Its
  pre-existing uncommitted `M project.godot` is untouched and not mine.
- **`user://` clean** — file logging off via both keys; no logs under either new project.
- **Corpus NOT imported**: 11 FBX, not 3,386. `l6prep` totals 16 MB.

### §4.6 — the probe project STAYS

`~/Games/mcp-lab/l6prep/` is the corpus's front door. `README.md` documents the three commands
(import → inspect → emit) and the clean-room verify.

**Wall clock:** execution **~7 min** (4 imports, 13 script runs, 4 renders, 1 framediff) ·
authoring + analysis **~30 min**. Execution was never the constraint.

**Signed:** drax, 2026-07-25.
