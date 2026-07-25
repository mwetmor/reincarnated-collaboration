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
