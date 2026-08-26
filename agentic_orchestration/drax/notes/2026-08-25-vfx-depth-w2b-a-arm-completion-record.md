# VFX-DEPTH RUN — WAVE 2b (drax) — THE A-ARM — COMPLETION RECORD

**Date:** 2026-08-25 · **Agent:** drax (presentation seam, `reincarnated-godot/`)
**Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** `gandalf/notes/2026-08-25-vfx-depth-run-charter.md`, **R-15 · R-16 · R-18**
**Class:** evidentiary note · **Status:** CURRENT
**Commits:** godot `58c0f87` · `c029c03` · collab `6ccd57bb` (+ this note)
**Start commit (defeat-condition basis):** godot `27baafc`

**Status: COMPLETE — 4 of 4 tasks landed.** The A-arm PARKED-NAMED at W2 is **discharged**. Both arms
now exist in the Cathedral at the ratified camera, the AB cut exists, the prune law is in force, and
the W1 over-correction is struck. **Five findings routed (§ 8).**

---

## 0. THE ARTIFACT PATHS — the deliverable, because the media is gitignored

| # | arm / cut | path | verified |
|---|---|---|---|
| **A** | HITL treatment, Cathedral, ratified camera | `/Users/admin/Games/reincarnated-godot/harness_logs/kc2_2026-08-25-w2b-acath/acath-hitl-ww-plk0665-60fps-1920x1080.mp4` | h264 yuv420p **1920×1080 · 60/1 fps · 210 frames · 3.500000 s** · 2,023,251 B · sha256 `5a5e1514e02750e31ffd376aad6ffa6bedc465c026644777df60564c1883263f` |
| **B** | twin + 4a, same room, same camera (W2, unchanged) | `…/harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxon.mp4` | 210 frames · sha256 `19d5e9c29dbc67cb…` |
| **AB-1** | **sequential**, A → black seam → B, labelled | `…/harness_logs/w2b_ab_cut/w2b-ab-sequential-A-then-B-plk0665-cathedral-1920x1080.mp4` | 1920×1080 · 60/1 · **456 frames** · 3,933,946 B · sha256 `f82607763cc6b8f1…` |
| **AB-2** | **side-by-side**, A \| B at native res | `…/harness_logs/w2b_ab_cut/w2b-ab-sidebyside-AB-plk0665-cathedral-3840x1080.mp4` | **3840×1080** · 60/1 · **210 frames** · 3,817,955 B · sha256 `74a523ea2c7de3db…` |

| record | path |
|---|---|
| **A-arm reproduction manifest** (Matt's hard requirement) | `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-25-vfx-depth-w2b-a-arm-reproduction-manifest.md` |
| A-arm sidecar (baton sha, camera derivation, anchor audit, epoch schedule, venue meta) | `…/kc2_2026-08-25-w2b-acath/shot-B-undulating-canon.json` |
| prune receipts | `…/kc2_2026-08-25-w2b-acath/prune_receipts.txt` · `…/wwcr_2026-08-25-w2-bcath/prune_receipts.txt` |
| AB cut receipt | `…/harness_logs/w2b_ab_cut/ab_cut_receipt.txt` |

**AB-2 is the first artifact of lap-1 and is Matt's next hard surface.**

---

## 1. TASK 1 — THE ENCODE-THEN-PRUNE LAW (R-18c). **FIRED FIRST, AND THE GATE IS A COUNT.**

`58c0f87` · `scripts/run_wwcr_stage.sh`, +100 lines, one file.

W2 F-3 measured the collision: identical camera, identical capture settings, **66,559 B/frame on
`bare` vs 2,779,536 B/frame in the Cathedral — 42×.** R-15 puts every depth-run render in the
Cathedral; R-5 retrofits all 24 T-A rows there. ~58 GB against ~48 GiB free. **R-15 and R-16 could not
both be obeyed, and this is where that is resolved.**

The mp4 + its sha receipt is the artifact of record. The PNG ladder is a Class-B intermediate **of its
own capture**, regeneratable by the literal command the receipt carries. Nothing cited by a seal, a
gate or a ruling is touched.

### ⚑ WHAT THIS ADDS THAT FG-12 DOES NOT: THE COUNT GATE

`run_ww7_gate2_clip.sh` prunes after the encoder returns. **But `ffmpeg` can exit 0 having written a
TRUNCATED stream** — a full ladder in, a short clip out, and a 2 MB file on disk that looks exactly
like a good one. So the gate here **decodes the whole stream, COUNTS the packets, and requires the
count to equal the PNGs that went in.** Mismatch, empty, or missing mp4 and the ladder **stays**, with
the reason printed.

> **A prune that fires on an unverified encode is not a disk policy. It is data loss with a receipt
> attached.**

### ⚑ THE LADDER IS DELETED IN BOTH PLACES IT EXISTS

`$OUT` (delivered) **and `$USERDIR`** (Godot's write target). The user dir is wiped at the *start* of
the next run — so without this it holds a **full duplicate** for however long the lane sits idle.
**Measured on the retro-prune: 0.543 GiB in each place, per arm. Half the reclaim came from the copy
nobody was counting.**

### ⚑ THE `marks` PATH IS EXEMPT, STRUCTURALLY

There the stills **are** the deliverable and there is no mp4 to be the artifact of record; the same
prune would delete the corpus. The exemption is **the prune's position inside
`if [ "$CAPTURE" = "seq" ]`**, not a setting somebody has to remember. `PRUNE=0` opts out for
isolation debugging, where the individual frames are the thing being looked at.

### The retro-prune, executed by the law's OWN BYTES

The function was extracted from the committed runner **verbatim** (`sed -n '/^encode_then_prune () {/,/^}$/p'`)
and invoked against the W2 B-arm corpus — **not a hand `rm` that merely resembles the law.**

```
PRUNE 2026-08-26T03:13:14Z  prefix=plk06650_cathedral_fxon
    sha256 19d5e9c29dbc67cbdaf8100d6362b210568f77487529153e4d49219327bf117b
    decoded frames 210 == PNGs in 210  (VERIFIED, counted)
  pruned : 210 PNG from harness_logs/…  (.543 GiB) + 210 PNG from $USERDIR (.543 GiB)
PRUNE 2026-08-26T03:13:14Z  prefix=plk06650_cathedral_fxctl
    sha256 f8434eb643c3e24b5e810e1fdb9a66ebfdc97675977d4e145f5ae6d558c7f44c
    decoded frames 210 == PNGs in 210  (VERIFIED, counted)
```

**Both sha256 match the banked B-arm manifest character for character** — the artifacts of record are
provably the same files after the prune as before it.

```
BEFORE  50,156,464 KiB avail
AFTER   52,437,728 KiB avail        FREED = 2,281,264 KiB = 2.176 GiB
```

**840 PNG deleted. 47.87 → 50.00 GiB free.**

---

## 2. TASK 2 — THE A-ARM. **RENDERED. THE PIN PRINTS `0.000000000000 m` IN THE CATHEDRAL.**

`c029c03` · `scripts/kc2_cpb_clip.gd` (+236) · new `scripts/run_kc2_cathedral_arm.sh`.

Full parameters at the reproduction manifest. **The dispatch's explicit ask, answered:**

```
[cpb] player_lock PIN vs tmp/br2watch/m6/pl_audit.json: offset delta 0.000000000000 m,
      z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
[cpb] PL-AUDIT anchor: delta (0.000000, 0.000000) frac = (0.0002, 0.0001) px at 1920 x 1080
```

⚑ **The anchor audit is a HARDER test here than on the B-arm.** The venue swap moves the entire world
around the subject *and* re-homes it against a station read out of the trace. Had the port shifted the
plane the anchor is solved against, the anchor would have moved and convicted the build. **It moved
two ten-thousandths of a pixel** — the same single-precision residue W1 recorded on the bare stage.

### 2a. ⚑ THE ROOM IS THE SAME ROOM, AND THAT IS A RECEIPT RATHER THAN A CLAIM

Both arms call the **same `S2StageEnv.build()` in the same build of the same file** — and
`s2_stage_env.gd` hashes to `65354ef1…` in **both** manifests. The A-arm's `STAGE_META` prints the
B-arm's numbers character for character:

| key | A-arm | B-arm |
|---|---|---|
| `arena_center_derived` | `[0.06, 1.593, -32.15]` | `[0.06, 1.593, -32.15]` |
| `floor_y_derived_m` | `1.593` | `1.593` |
| `fight_surface_r_m` / `tiles` / `rocks` / `seed` | `16.0` / `126` / `148` / `20260825` | `16.0` / `126` / `148` / `20260825` |

R-15 asked for *"both arms, one room, one camera; the only difference the eye sees is effect
authorship."* **That is now mechanical.**

### 2b. ⚑ THE ROOM MOVES TO THE ACTORS — and I did not take the seam map's route

The venue is built under **one `Node3D` translated to the kc2 player station**, and the builder is
handed *that* root. The offset reaches geometry, lights and environment **uniformly, by construction**.

**The W2 seam map called for building into `self` and RE-PARENTING `PackCathedral` + `FightSurface`
afterwards.** That is two node moves that must each preserve a global transform, **and it silently
leaves the directional lights and the `WorldEnvironment` behind at the origin** — invisible today (the
environment is position-free; the lights are directional) and a trap the moment a point light enters
the recipe. **Handing the builder an already-offset root cannot desynchronise, because there is
nothing to keep in sync.** My own prior session's map was good; this is one step better and the map is
what made finding it cheap.

⚑ **Why the station and not the world origin. MEASURED:** `player_station` reports
`player_moves = false` with x = y = 0 across all **3,732** samples — so on this trace the station **is**
the origin and the two choices coincide. **They coincide by accident of this baton.** Homing to the
station is what makes both arms see the venue from the same *relative* pose under a subject-locked
camera, and it survives a trace where the caster stands elsewhere.

### 2c. ⚑ THE ARENA'S OWN VENUE IS HIDDEN, NOT FREED

`visible = false` on `ArenaFloor`, `ArenaSkirtDress`, `Key`, `Fill` — which removes them from
rendering **and from shadow casting** — while leaving `kc2_arena.floor_mesh` / `.skirt_mesh` valid.
`kc2_arena_smoke.gd` asserts both non-null; `kc2_cpa_stills.gd` toggles the floor. **Freeing them
would have made this change reach two files it has no business reaching.** The `WorldEnvironment` is
not a `VisualInstance3D` and cannot be hidden, so it is **removed from the tree and parked in
`_venue_parked`: removed, referenced, never freed, never dangling.**

The whole port is **non-destructive**. `--stage` unset builds the arena this file has always built.

### 2d. ⚑ THE RATE IS A PARAMETER, AND THE RECORD'S RATE IS ITS DEFAULT

60 fps, because **an A/B judged at two frame rates is not an A/B** — the eye reads rate as cadence,
which is exactly the property under judgement. `--fps` unset yields the `FPS` const, so every banked
kc2 clip re-renders with byte-identical frame arithmetic.

### 2e. ⚑ THE OFF-BY-ONE IS A MEASURED HARNESS FACT, DECLARED AND ASSERTED

Godot's Movie Maker writes a PNG for the frame in which the scene quits: `--frames N --preroll P`
leaves **N + P + 1** on disk. Measured on the invocation smoke (N=6, P=4 → raw 11 → 7 delivered).
Uncorrected the A-arm would be **211** against the B-arm's **210**, and the two arms would not be
frame-for-frame comparable. The runner takes `DELIVER`, passes `DELIVER - 1`, **and ASSERTS the
post-prune count** — so if Movie Maker ever stops writing that terminal frame this **fails** rather
than silently shipping 209. Delivered: **270 raw → 210 after preroll prune → assertion PASS.**

---

## 3. TASK 3 — THE AB CUT. **BOTH FORMS, BOTH LABELLED, CLAMPED OFF THE STREAMS.**

`scripts/run_w2b_ab_cut.sh`. Paths + hashes in § 0.

- **`CLAMP = min(210, 210) = 210`, COUNTED off both streams** with `-count_frames`, never assumed from
  the invocations that made them. The W1 lesson in executable form: **`hstack` runs until its LONGEST
  input ends and holds the exhausted one on its final frame** — an unclamped stack shows a frozen arm
  beside a running one and reads as a rendering fault rather than a length difference.
- **Native resolution, no scale.** 1920+1920 = **3840×1080**. Downscaling a side-by-side is how a depth
  judgement gets made on a texture that is no longer there — and depth/texture/juice is the entire
  rubric.
- **The runner HALTS** if the arms differ in dimensions or frame rate, and says why in both cases.
- **Labels are PIL-rasterised PNGs composited with `overlay`.** MEASURED: `ffmpeg -version` on this
  host contains no `enable-libfreetype`, so every `drawtext` filter fails at graph-build time. **One
  labelled clip beside one unlabelled fallback is exactly the silent divergence a viewing artifact
  must not have.** Verified by cropping the 3840×68 banner strip out of the delivered side-by-side and
  reading it: both labels legible at native resolution.
- ⚑ **Both cuts are a SECOND ENCODE GENERATION of both arms**, with identical settings (libx264,
  yuv420p, crf 18, preset slow) **so neither arm is favoured by the compositor**. The artifacts of
  record are the two arm mp4s and their sha256s. **Nothing is measured on the cut.**

---

## 4. TASK 4 — THE W1 AMENDMENT. **STRUCK IN PLACE, NOT REWRITTEN.**

collab `6ccd57bb` · `drax/notes/2026-08-25-vfx-depth-w1-playerlock-camera-and-4a-completion-record.md`.

My W1 record said of the reference clip: *"It is **NOT a whirlwind**."* **`kc2_cpb_clip.gd:111-112`
refutes it in its own words:**

> *"It exists to answer ONE question — does the **whirlwind** read, now that the man has a head, a
> hammer, and a rate Matt chose?"*

The sentence is **struck through and left on the page**, with the retraction, the source quote, and a
two-row table separating the claim that survives (`WW-7` **is** an SB-1 run-ledger cell id —
knight-rider's retraction of the mis-citation stands, undisturbed) from the claim that does not
(*therefore the clip is not a whirlwind*).

⚑ **The lesson, which is why the strike is visible rather than edited away: the wrong claim arrived
dressed as a CORRECTION, so it carried more authority than the error it replaced.** A note that says
*"actually, no"* is read as the settled version. Mine was read that way — **by me, in the very next
wave** — which is how it reached a dispatch before anyone caught it.

**NOT this wave's write, named so it is not mistaken for an omission:** the adjacent knight-rider seal
(collab `950f6656`) may need its own reconciliation line. **R-18(b) flags that to jack-ryan.** Not
touched.

---

## 5. DEFEAT-CONDITION RECEIPT — pasted mechanically, no eye-curation (#72)

Basis: **`27baafc..HEAD`** (`27baafc` = this session's start commit). Instrument: the **corrected**
glob from R-11(b) (`scripts/run_wwcr_stage.sh`, not bare `run_wwcr_stage.sh`).

### [1] W2b's OWN contribution to the guarded set, isolated

```
$ git diff --stat 27baafc..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'scripts/run_wwcr_stage.sh'
 scripts/run_wwcr_stage.sh | 100 ++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 100 insertions(+)
```

**ONE file. The prune law. The A-arm work touched ZERO files in the guarded set.**

### [2] Token grep over that same diff

```
$ …same diff… | grep '^+' | grep -Ei 'vfxbo|cpb|kc2|a337d30|sb1|etch|claw|cut_|rig_poe1|cyclone|run_ww[0-9]|PAL_|decay_gamma|sheath'

+#    Proven pattern: `run_ww7_gate2_clip.sh`'s FG-12 prune. What is added here
```

**1 hit. ADJUDICATED:** a `+#` **comment line** naming the runner whose FG-12 prune this wave was
*ordered by the dispatch* to copy. Not code, not an effect parameter — same class as W1's four
adjudicated camera-provenance citations already ruled on at R-11(b). **CLEAN.**

### [3] Float-literal intersection, W2b's own added floats

```
$ …same diff… | grep '^+' | grep -oE '[0-9]+\.[0-9]+' | sort -u
2.4
2.78
```

**2 values. ADJUDICATED:** both appear on `+#` comment lines quoting **W2 F-3's own measurement**
(2.78 MB/PNG in the Cathedral; ~2.4 GB per AB pair). Verified by context:

```
$ …same diff… | grep '^+' | grep -nE '2\.4|2\.78|run_ww[0-9]'
10:+#    the Cathedral — 42x.** One AB pair is ~2.4 GB where it used to be 30 MB, and
27:+#    Proven pattern: `run_ww7_gate2_clip.sh`'s FG-12 prune. What is added here
51:+#   however long the lane sits idle. At the Cathedral's measured 2.78 MB/PNG that
```

**All three hits are `+#`. No float crossed from `kc2_player_channel.gd` or `kc2_etch.gdshader` — the
two effect-authoring quarantined files. CLEAN.**

### [4] The certified artifact

```
$ git diff --stat fde563c..HEAD -- scripts/wwcr_whirlwind.gd
    -> EMPTY
$ shasum -a 256 scripts/wwcr_whirlwind.gd
ce2204524a09bc5ac747b0db3050cdf0bc8e55b832b04c55249f0767d15de8b4
```

**`wwcr_whirlwind.gd` is BYTE-IDENTICAL to the W1 4a landing, and its sha256 matches the B-arm
manifest's pin character for character.** W1/W2/W2b: one file, one hash.

**VERDICT: LINEAGE CLEAN.** The provenance law held by construction — the HITL treatment rendered
**beside** the twin, in `kc2_*` files and two new non-`wwcr` runners, and not one line of it entered a
`wwcr_*` file.

---

## 6. SMOKE GATES RUN

| gate | result |
|---|---|
| `bash -n` on all three shell landings | OK (and it **caught a real defect** — F-4) |
| GDScript parse (`--check-only`) on `kc2_cpb_clip.gd` | clean, no errors |
| Invocation smoke, A-arm runner (6 frames) | full path exercised: args, pin, venue swap, gate, encode, ffprobe, prune, receipt |
| Full A-arm render | **270 raw → 210 delivered**, `DELIVER` assertion PASS, ffprobe 210/210 |
| Camera pin, post-port | **`0.000000000000 m` MATCH** |
| Anchor audit, post-port | delta `(0.0002, 0.0001)` px |
| Venue identity vs B-arm | `STAGE_META` equal on all 8 compared keys |
| **Eyes on the frames** | frame n=105 pulled from **both** arms and **looked at**: same room, same framing, same light; A carries a dust field + hot arc, B a thin ribbon |
| Label legibility | 3840×68 banner cropped at native res and read — both labels legible |
| Prune count gate, both runners | 210 decoded == 210 PNG, ×3 captures |
| Default paths unmoved | `--stage` unset ⇒ arena · `--fps` unset ⇒ `FPS` const · `PRUNE=0` keeps ladders |

---

## 7. DISK

| point | free |
|---|---|
| wave start | **47.87 GiB** |
| after retro-prune (TASK 1) | **50.00 GiB** *(+2.176 GiB)* |
| after A-arm render + its own prune | 49.71 GiB |
| **at close** | **49.61 GiB** |

**The 40 GiB floor was never approached and no deletion was improvised.** The A-arm runner carries a
pre-flight floor check that HALTS *before Godot starts* — projected cost is computed from W2 F-3's
measured 2.78 MB/PNG, and a render that has to be killed halfway is the expensive failure. It printed
`free after 49.02 GiB, floor 40.00 GiB` and proceeded.

⚑ **The prune law reclaimed 2.176 GiB retroactively and prevented 0.491 GiB from accumulating on the
new render. Under R-5's 24-row retrofit that second number is the one that compounds.**

---

## 8. FINDINGS ROUTED — five

**F-1 — ⚑ `camera_ground_gate` IS ANALYTIC AGAINST A SKIRT AND CANNOT SEE THE VENUE. IT RETURNS `PASS`
FOR A SURFACE THAT IS NOT BEING DRAWN.** Route: **gandalf** + **jack-ryan**.
It solves nine frustum rays onto y = 0 and tests each hit against `SKIRT_HALF_M` (400 m) or
`FOG_DEPTH_END_M` (260 m). **It never touches a mesh.** After a venue swap the skirt is hidden and the
lift environment has no depth-fog saturation at all — so both of its acceptance conditions are
vacuous, **and it returns `PASS (9 rays)` with an empty reason string.**
**This is the fifth instance in this project's record of one shape: an instrument returning cleanly
after it stopped answering the question** (the `factory/permissions.py` non-defect · the crop that
could not see the aim difference · `git diff HEAD~1` naming a concurrent session's file · `git diff
HEAD` blind to new files · this). **The transferable part is the same each time and it is not "test
your tests": it is that a CHANGE OF SUBJECT silently changes an instrument's DOMAIN, and the
instrument has no way to notice.**
Handled at source: the gate's **descend** leg is consumed (venue-independent, still HALTs, `0/9`
failures), its **skirt** leg is explicitly **not consumed**, and `_venue_coverage` measures the same
nine rays against the radii this venue actually has (`max ground radius 19.1788 m` · fight disc
`16.00 m` · pack stage `26.00 m` · `0/9` outside). **It reports; it does not refuse** — the
composition call is Matt's per R-18(d).

**F-2 — ⚑ THE VENUE'S COLOUR REGISTER INVERTS AT THE JUDGING CAMERA, AND W2 F-4 NAMED ONLY THE
FRAMING HALF OF THIS.** Route: **Matt**, at the lap gate. **A refinement of F-4, not a new object.**
The ratified referent (`04_leap_strike_CATHEDRAL.mp4`) reads **dark blue and amber — cathedral on a
mountain, seen whole.** At `player_lock` k=0.665 both arms read **maroon / magenta**: the tile floor
fills ~⅔ of frame, and the pack floor's warm albedo under `KeyLight` (1.0, 0.74, 0.50) with the lift
env's `adjustment_saturation 1.24` dominates a frame the cool background used to.
**This is NOT a build drift, and I verified that rather than assuming it:** both arms print identical
`STAGE_META`, and the referent was produced by the same `_lift_env()` in the same file. **Only the
camera differs.** F-4 said the diorama drama is gone; it did not say **the colour register also
inverts from cool-blue to warm-magenta** — and colour register is part of what the depth rubric is
scored on. **I am not touching it:** k=0.665 is Matt-ratified and the camera is not my lever
(R-18(d)). Both arms carry the cast equally, so **the AB comparison is unaffected**; it is a
venue-fidelity question for Matt's eye, not an AB-validity question.

**F-3 — ⚑ THE A-ARM SIDECAR WAS BEING WRITTEN TO `$TMP` WHILE THE MP4 IT DESCRIBES LIVES FOREVER.**
Route: **self, FIXED** (`cp -p "$SIDECARS"/shot-*.json "$OUT"/`). Recorded because of how it was
caught: **writing the reproduction manifest and having to read the file out of `/tmp` to do it.** The
sidecar carries the baton sha, the camera derivation, the anchor audit, the epoch schedule, the venue
meta and the tick period — most of what *"reproduce it exactly"* means — and it was one reboot from
gone. **A reproduction requirement is what exposed a durability gap that no smoke gate would have.**

**F-4 — ⚑ AN APOSTROPHE INSIDE `${VAR:-word}` SWALLOWS THE REST OF A SHELL FILE, AND `bash -n`
REPORTS THE ERROR 40 LINES AWAY.** Route: **self, FIXED** + noted for the seam. `${VAR:-word}`
undergoes quote removal **even inside double quotes**, so `"${A_LABEL:-… (Matt's hand) …}"` opened a
quoted region that ran to EOF; `bash -n` blamed the first unbalanced paren far below. Caught by the
syntax check before any run. **The misleading line number is the part worth carrying** — the reported
location was in correct code.

**F-5 — `_playerlock_aim` STILL IGNORES ITS `focus` ARGUMENT.** Route: **gandalf**, carried forward
from W1 and W2 **unchanged**. Parked at R-18(e); the pin verifies to 12 decimals regardless, and it
did so again through a venue swap this wave. Restated only so it does not age out of the record.

---

## 9. WHAT I DID NOT DO, AND WHY

- **Did not shrink the disc or move the camera.** R-18(d): k=0.665 is Matt-ratified and F-4 is held
  for his eye. F-2 above is a *report*, not an action.
- **Did not touch the banked corpora.** R-18(a) struck the Round-1 candidate; `s2c38*`/`s2c12*` are
  #81-cited Class A. Not approached.
- **Did not improvise a deletion.** Free space never neared the 40 GiB floor; the runner's pre-flight
  check exists so that it cannot be discovered mid-render.
- **Did not touch `run_ww7_gate2_clip.sh`.** It rendered the record Matt has already watched, and its
  own header states the property: byte-untouched so that record re-runs exactly as it ran.
- **Did not touch `wwcr_whirlwind.gd`, `wwcr_stage.gd` or `wwcr_stage.tscn`.** § 5 [4].
- **Did not touch knight-rider's seal `950f6656`.** R-18(b) routes that to jack-ryan.
- **Did not x2-determinism-gate either arm.** Declared in the manifest § 10 as a deferral, not waived
  by omission. The AB cut is a first look for Matt's eye, not a certified deliverable.
- **Did not render the canon shot's full 640-frame window.** Frame-parity with the B-arm is what makes
  the clamp inert; the full window is `DELIVER=0` and ~1.2 GB more.
- **Did not touch `tmp/br2watch/measure/census.json`** — dirty, another workstream's, under QA review.
  Left exactly as found, for the fifth time.

---

## 10. PUSH

Charter § 5 push posture **LIVE** (*"push as you go"*), both repos this wave writes. Instruments per
landing: `git status --porcelain -- <named paths>` before, `git show --stat HEAD` after, `git -C
<path>` on cross-repo operations. godot `58c0f87`, `c029c03` pushed; collab `6ccd57bb` + this note.
