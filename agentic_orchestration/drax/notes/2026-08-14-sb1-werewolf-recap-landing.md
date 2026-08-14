# SB-1 werewolf-recap micro-cell — LANDING NOTE (drax, 2026-08-14)

**Cell:** produce one fresh werewolf-room still from the WR1 level rig at the rig's own
existing shot framing — R-CPB-17b ground truth for Matt's camera-match side-by-side.
**Class:** capture-only. Zero edits to any tracked file in `reincarnated-godot`.

**VERDICT: HALT.** The chartered deliverable is not producible as specified, and the reason
is not ambiguity — it is absence.

---

## 1. What fired

Four blocking renders, two exhibits, both at their own rig's frozen in-file camera. **No
camera value was touched anywhere**: no 72.857 m boom applied, no 134 m applied, no
yaw/pitch/fov/distance/aim override flag passed.

| Exhibit | Rig | Shot | Camera (rig's own) | Gate |
|---|---|---|---|---|
| **A** | `scripts/wr1_level_rig.gd` | `--shot room:0` | yaw 47 / pitch −50 / fov 24 / **dist 72.86 m** | **FAIL-DECLARED** |
| **B** | `scripts/vh_race_rig.gd` | `--brief aura` | yaw 47 / pitch −50 / fov 24 / **dist 34.000 m** | **PASS** |

All four passes exited 0.

## 2. The HALT and its evidence

**No room in the WR1 level contains a werewolf. No room contains any character.**
`wr1_level_rig.gd --shot room:N` renders an empty architectural room for every N in 0..3.

1. `wr1_level.gd:100-105` — the `ROOMS` table is four rows of **tier + kit**
   (`trash`/`dark-fortress`, `champion`/`dwarven-dungeon`, `mixed_pack`/`dungeon-realms`,
   `boss`/`dark-fantasy`). Encounter class and art kit. Not occupants.
2. `wr1_level.gd` instantiates exactly **one** PackedScene in the whole file —
   `wr1_level.gd:491` loading `ROOM_AMBIENT` (`vfx/ambient/room_ambient.tscn`). No character
   asset is referenced anywhere in the file.
3. `wr1_level_rig.gd:19-20`, the rig's own header, verbatim: *"The rig contributes a camera
   and a clock."* Full 171-line read confirms it: `_ready()` adds a `WR1Level` and a
   `Camera3D`, nothing else.
4. `scenes/wr1_level_rig.tscn` is two nodes — one `Node3D` with the script attached.
5. **Rendered.** Exhibit A is the chartered invocation at the chartered framing. Empty room,
   zero subjects. Confirmed by eye.

Candidate rooms, each with its evidence, are enumerated in the receipt. Room 0 was rendered
on a real correspondence rather than a guess: `wr1_level.gd:101` `ROOMS[0].kit ==
"dark-fortress"` equals `vh_race_rig.gd:42` `const KIT := "dark-fortress"` — room 0 is the
WR1 room built from the same art kit as the frozen L7/R-6 stage the werewolf actually stands
on. It still contains no werewolf.

## 3. Where the werewolf actually is (provenance located)

`scripts/vh_race_rig.gd` — the L7 race rig — carries **byte-identical lens numbers** to the
WR1 level rig (`vh_race_rig.gd:38-41` vs `wr1_level_rig.gd:25-27`: yaw 47 / pitch −50 /
fov 24) and a **fixed 34.0 m** distance. The body arrives via `--brief aura` →
`vh_brief_aura.gd:62` → `vh_caster.gd:38` → `SK_Chr_Werewolf_01.fbx`, printed at render time
as `[vh_caster] built — height=1.8000`.

The two rigs differ in exactly one term — **distance** — and only the 34 m one has ever had a
werewolf in front of it.

## 4. Declared variance (GL-12)

Exhibit A's two passes produced **different** digests. Declared, **not chased** — this cell is
not a determinism probe. Named candidate cause is documented in-tree by the seam's own
authors at `wr1_level.gd:178-181`: `GPUParticles3D` is unseeded in this tree, so any two-render
peel is contaminated unless the ambient is off. Exhibit A ran `--ambient on` (the rig's own
default, i.e. the rig's own framing). Magnitude fits that cause: mean-luma delta 0.003/255,
byte delta 165 B on a 622 KB PNG. Both passes kept on disk. The exhibit's value is a proof of
absence, and both passes show the same absence. Exhibit B, on the same machine minutes later,
was **bit-identical across two passes** — so the renderer is not broadly nondeterministic here.

## 5. Routed up, not filled

R-CPB-17b calls 72.857 m *"the conductor's TRANSCRIPTION of the werewolf frame."* This cell
can now say what the transcription step was: a **distance** step, not a lens step. The lens
transplanted exactly; the distance came from a rig that has **no subject in it**.

Lens geometry from the rigs' own printed constants (frame height = 2·d·tan(fov/2),
tan 12° = 0.2125566): **14.454 m** of world spans the frame height at 34.0 m; **30.972 m** at
72.857 m — a **2.143×** taller frame for the same 1.8000 m werewolf.

**Deliberately not converted to a subject percentage.** At pitch −50 the on-screen extent of a
standing body is foreshortened and pose-dependent, so subject fraction is a measurement off
pixels, not desk arithmetic (NOTE-62). Flagged: the ledger's *"subject ≈ 12.96% at 72.857 m"*
has **no rendered werewolf behind it anywhere in this tree** — before this cell fired, no
render of a werewolf at 72.857 m existed at all. That is the conductor's call, not drax's.

## 6. Containment

- Tracked-file changes in `reincarnated-godot`: **none**. Godot HEAD `be7f0c2` unmoved.
- Pre-existing dirty file, **not touched by this cell**: `M tmp/br2watch/measure/census.json`
  (BR-2-era leftover, already accounted at A1b-7).
- **Rig-written artifacts inside the godot repo tree: NONE.** Both rigs accept an absolute
  `--outdir`, so all four PNGs and all four logs were written directly to the capture dir
  outside the repo. The harness `.sh` wrappers were bypassed for exactly this reason (and so
  `run_wr1_level.sh:20`'s `rm -f` prefix-sweep never ran against anyone's frames).
- PNG bytes and raw Godot logs: on disk, **untracked** (class-E law; `.gitignore` in the
  capture dir). `receipt.txt` is the tracked bridge and carries every sha256 and number.

## 7. Deliverables

- `agentic_orchestration/galadriel/captures/2026-08-14-sb1-werewolf-recap/receipt.txt` (tracked)
- `.../frames/wwrecap-room0-p1.png` · `-p2.png` — Exhibit A (untracked)
- `.../frames/wwrecap-vhaura-p1.png` · `-p2.png` — Exhibit B (untracked)
- `.../logs/*.log` — full Godot stdout, four runs (untracked)

## 8. What the conductor has to decide

The cell will not choose between these; both are re-charters, not seam calls.

1. **Is Exhibit B the frame Matt's eye ratified?** It is the only in-tree render of the
   werewolf at the canon lens. If yes, the eyeball packet has its werewolf half now.
2. **Does the boom candidate list survive?** 72.857 m is the WR1 *room-verification*
   distance and has never had a subject at it. 34.0 m is the distance that has. Neither this
   note nor this cell rules on that.
