# SB-1 Cell A2g — THE CANON FRAME · AND THE MAN IS 60 PIXELS TALL

**Cell ID:** `SB1-CELL-A2g` · **Date:** 2026-08-13 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — **R-CPB-16** (Matt's camera ruling)
GOVERNS; **A2g-0** is the charter; **R-CPB-15** (the rate) and **CLK-1-1 / CLK-1-2** (the clock) are
the inherited state.
**Base:** `drax/notes/2026-08-13-sb1-clk1-clock-landing.md` (the fixed clock) and
`drax/notes/2026-08-13-sb1-a2f-density-landing.md` § 1 (the rate-17 article).
**Godot repo:** `6eff089` → `c011182` → `03436f8`, **two commits, pushed as they landed (PL-7);**
the third (this note + the promote tool) lands in the collaboration repo.

---

## ⚑ VERDICT

**THE CLIP IS PROMOTED. NINETEEN CLAIMS CHECKED AGAINST MEASURED FACTS, ALL PASS. FG-10 RETURNED ONE
DISTINCT STATE ON ALL FIVE LEGS — AND THE TWO PROMOTED LEGS WERE PROBED AT THE **FULL 320-FRAME
SPAN**, WHICH CLOSES CLK-1's SURFACE 3 BY MEASUREMENT RATHER THAN BY PROMISE.**

⚑ **AND THE NUMBER MATT NEEDS BEFORE HE WATCHES IT: THE SUBJECT IS 5.59 % OF FRAME HEIGHT.** Sixty
pixels of 1080 for 2.40 m of man-and-hammer. That is not a defect and it is not a compensation I
declined to make — it is **the canon's own arithmetic meeting a room five times bigger than the one
the canon was set in.** The canon's own shots put a subject of this size at **27.78 %** (R-6's 17.5 m
room at 34 m) and **12.96 %** (wr1's 37.5 m room at 72.86 m). This arena, by the same law, at
**168.863 m**, puts it at **5.59 %** — two to five times smaller than the frame has ever shown a
body. The lens numbers are Matt's, verbatim. The distance is a FORMULA whose input is room size, and
nobody ruled on the room. **§ 1.4 has the fork arithmetic. It is NOT APPLIED.**

| item | commit | what |
|---|---|---|
| **1** | `c011182` | **THE CAMERA** — transplanted verbatim; the optics measured through the camera that renders; and the row written to check the law caught the law's claim instead |
| **2** | `03436f8` | **THE CLIP** — one canon frame, both cadences, FG-10 at full promoted span; two wiring defects fixed on the way past |
| **3** | *(collab)* | the promote tool's **first live run ever**, the manifest, this note |

**Deliverable:** `galadriel/captures/2026-08-13-sb1-a2g-canon/a2g-canon-cadence-ab.mp4`
**sha256** `4ab0e27357c5d44438a52197bfae35ebce214f30fe206bf0fe0965e635888467` · 3,999,919 B ·
21.933333 s · **658 frames** · 1920×1080 h264 yuv420p 30/1.

---

## 0 · GL-6 FIRST, BEFORE ANYTHING WAS TOUCHED

Baton `kc2-baton-v1-E-s09-cp150-20260809_052836.json` recomputed from bytes =
`d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa`, **1,065,632 B — MATCH.**
Re-asserted inside the render: the arena's own baton gate printed `digest d7ecd866ac45 (MATCH)` on
every one of the 22 process launches this cell made, and both promoted sidecars carry it.

**PL-5 before frames:** captures **6.74 G of 10 G**, disk free **26.2 G** — checked in the shell AND
again inside the Godot harness before a single frame was built. At close: **6.75 G**, the tree grew
by **4.08 MB** (the MP4, the manifest, two sidecars).

---

## 1 · ITEM 1 — THE CANON CAMERA · commit `c011182`

### 1.1 THE DERIVATION, DECLARED

Nothing below is a taste call. Three numbers are copied out of `scripts/wr1_level_rig.gd`; the
distance is that file's own law applied to GL-13's pinned rectangle; the aim is that file's own
look-height convention applied to the whirlwind station; the orbit is its own trig.

| quantity | value | source — **cited, not paraphrased** |
|---|---|---|
| yaw | **47.0°** | `wr1_level_rig.gd:25` — verbatim |
| pitch | **−50.0°** | `wr1_level_rig.gd:26` — verbatim |
| fov | **24.0** (vertical, KEEP_HEIGHT) | `wr1_level_rig.gd:27` — verbatim |
| the law | `DIST = 34.0 × (EDGE / 17.5)` | `wr1_level_rig.gd:28-29` — *"R-6 framed a 17.5 m room from 34 m. Same angular size for a 37.5 m room."* |
| GL-13 rectangle | **86.915 × 85.303 m** | read from `Kc2Arena.build().footprint`, never moved |
| **EDGE** | **86.915 m** | `maxf(size_x, size_z)` — ⚑ **A JUDGEMENT** (§ 1.2) |
| **DISTANCE** | **168.863429 m** | `34.0 × (86.915 / 17.5)`, recomputed in the promote tool and checked against the sidecar to 1e-6 |
| aim | **(0, 1, 0)** = station + 1.0 m | `wr1_level_rig.gd:104` — `_orbit(centres[idx] + Vector3(0, 1.0, 0), …)`. **TRANSPLANTED.** The demoted b-ring used 1.1 m; not inherited |
| eye | **(79.3836, 130.3569, 74.0264)** | `wr1_level_rig.gd:92-94` orbit trig, verbatim — **recomputed independently in Python and matched to 1e-3** |
| camera gate | **PASS**, 9 rays | run at fov 24, i.e. at the lens that renders |

### 1.2 ⚑ THE ONE JUDGEMENT, MADE AS SMALL AS A JUDGEMENT CAN BE — VETO-OPEN

The law was written for a **square** room. The arena is a rectangle. **EDGE = the longer side.**

* The law's content is *"the room subtends what R-6's room subtended"*, and a rectangle subtends what
  its **governing** dimension subtends. Frame the long side and the short one fits with room to
  spare; frame the short side and the long one is cropped — the one outcome the law forbids.
* **In-tree precedent, in the same function:** the a-field pose already reads the footprint as
  `maxf(size_x, size_z)`. This is the convention the file already had, not one invented for the cell.

**The fork is one identifier.** `minf` gives EDGE 85.303 m → DIST **165.72 m**, a **1.9 %**
difference. Declared in the code, in the sidecar and in the manifest. **Veto-open.**

### 1.3 ⚑ THE ROW I WROTE TO CHECK THE LAW CAUGHT THE LAW'S CLAIM INSTEAD

The first cut of the rectangle instrument asserted *"four corners inside the frame is the law,
checked."* The measurement came back **two of four** — one corner 351 px below the frame, one 31 px
above it.

**The law never promised the other two.** `34 × (EDGE/17.5)` fixes `dist/edge` at a constant 1.9429
— it fixes **SCALE**, and says nothing about **containment**. R-6's own 17.5 m room did not fit
either: a square seen at yaw 47° presents **1.414×** its edge in depth, against roughly **1.10×** its
edge that fov 24 covers on the ground at that distance. **Corners outside the frame are INHERITED
from the canon, not introduced by this cell.**

So the claim string was rewritten to what the law *does* fix, and the scale itself is now measured:
**the 86.915 m edge subtends 1,307.61 px** at the aim plane (15.0446 px per metre across the view) —
and that pixel count is a **constant for any room**, which is the entire content of "same angular
size". ⚑ **A row that only confirms is not an instrument.** (NOTE-77.)

### 1.4 ⚑ THE PARALLAX AND THE SUBJECT, RE-DECLARED AS **MEASURED** FACTS

Every optic below is read by putting world points through `Camera3D.unproject_position` on the camera
that renders. The analytic value is carried **beside** each one, never in place of it.

| | **canon (this clip)** | **b-ring (demoted)** | **d-close (demoted)** |
|---|---|---|---|
| fov | 24 | 48 | 48 |
| ring ellipse minor/major — **MEASURED** | **0.765857** | **0.434920** | **0.530515** |
| …**PREDICTED** by sin(depression) | 0.765830 | 0.427131 | 0.467890 |
| prediction error | **+0.004 %** | +1.82 % | ⚑ **+13.38 %** |
| ring major axis | **66.2 px** | 514.4 px | 1480.5 px |
| subject screen height | **5.59 %** | 38.75 % | 92.43 % |
| px per metre at the station | **9.63** | 99.09 | 230.00 |

⚑ **THE CUT RING OPENS TOWARD CIRCULAR — 0.4349 / 0.5305 → 0.7659.** At the old depressions it read
as a squashed band; at pitch −50 it reads as very nearly the circle it is. The charter predicted
≈ sin 50° = 0.766 and the measurement agrees to **3.5 × 10⁻⁵** — at 168.9 m a perspective camera is
an orthographic one for this purpose.

⚑ **AND MEASURING RATHER THAN ASSUMING PAID FOR ITSELF ON THE OTHER TWO.** The 0.4271 / 0.4679
figures in the A2e manifest — the ones Matt was given for the clip he watched — are **predictions**,
and the close one is **12 % low**. A 2.2 m circle seen from 4.3 m away is not a parallel projection.
The demoted frames were re-measured **for free**, off the FG-10 probe legs that rendered them in this
same run, through the same instrument — so the vs-old comparison is like for like instead of
measurement-against-formula.

**THE SUBJECT, AND THE NUMBER IS NOT SOFTENED.** The union of every `MeshInstance3D` AABB under
`body_holder` — the man and his hammer, **2.5945 × 2.3996 × 1.9373 m** — projects to **60.40 px of
1080 = 5.5926 %** of frame height at tick 1570. *(The anti-overfit leg at tick 1660 measures 67.19 px
= 6.221 %: the box's projected height moves with the hammer's spin phase, so the honest band is
**5.59–6.22 %** and the headline is the shot's own first tick.)*

⚑ **THE FORK, WITH ITS ARITHMETIC — AND IT IS NOT APPLIED.**

| frame | distance | a 2.40 m subject reads |
|---|---|---|
| R-6's reference — 17.5 m room | 34 m | **27.78 %** of frame height |
| wr1's own room shot — 37.5 m room | 72.857 m | **12.96 %** |
| **this clip** — 86.915 m arena | **168.863 m** | **5.59 %** |

R-CPB-16 rules the camera **angle** and **zoom**. Angle (47 / −50) and zoom (fov 24) are pure lens
and are transplanted exactly. **Distance is not a lens property** — in wr1 it is a formula whose
input is room size — so applying the canon to a room 5× larger moves the subject **even though not
one lens number changed**. Screen fraction scales as 1/distance off the measured 9.63 px/m: a subject
at 12 % wants **78.7 m**, at 8 % wants **118.0 m**. Either is one constant in `_canon_pose`.
**The charter said transplant the law, report the number, do not compensate. I did not compensate.
The ruling is Matt's and it now has figures under it.**

---

## 2 · ITEM 2 — THE CLIP · commit `03436f8`

**ONE SHOT, NOT TWO.** b-ring and d-close were lenses this cell chose; R-CPB-16(d) demotes both to
diagnostic instruments. They stay in `SHOTS` and in the FG-10 matrix as regression legs; neither is a
segment. So **segment A and segment B run the SAME window (ticks 1570–1700) through the SAME frame**,
and the A/B is exactly one boolean over one span — the cleanest cut this harness has cut.

### 2.1 ⚑ THE FG-10 MATRIX — AND THE PROMOTED LEGS RAN THE **FULL** SPAN

CLK-1 filed the hole itself as its surface 3: *"the gate probes 45 frames and certifies 320."*
CLK-1-2(4) ruled it closed here. It is closed.

| leg | span | passes | **distinct states** | disagreeing frames | digest-of-frame-digests |
|---|---|---|---|---|---|
| 1 · **canon / undulating** | ⚑ **FULL — 320 frames** | 4 | **1** | **none** | `cb0d294b0a90e82b…` |
| 2 · **canon / stationary** | ⚑ **FULL — 320 frames** | 4 | **1** | **none** | `faa3f39714f55343…` |
| 3 · canon / undulating, **tick0 1660** (anti-overfit) | 46 | 4 | **1** | **none** | `9adbd18dec484c63…` |
| 4 · d-close / undulating *(demoted)* | 46 | 4 | **1** | **none** | `0253761a43b374b9…` |
| 5 · b-ring / undulating *(demoted)* | 46 | 4 | **1** | **none** | `504b6d8b4c0929ff…` |

**5 legs × 4 passes = 3,112 rendered frames. ONE distinct state per leg. ZERO disagreeing frames
anywhere.** The gate now measures exactly what it certifies: a transient at frame 200 fails it
instead of shipping.

⚑ **AND THE LAST TWO DIGESTS ARE OLD FRIENDS.** `0253761a43b374b9…` and `504b6d8b4c0929ff…` are
**CLK-1's**, character for character, from a different commit. The demoted shots render
bit-identically at HEAD — **a cross-cell regression proof that item 1's camera work changed no pixel
of anything but the new frame**, asserted by digest rather than by reading a diff.

### 2.2 TWO WIRING DEFECTS, FOUND BY READING THE WIRING RATHER THAN TRUSTING IT

1. ⚑ **THE TEMP DELIVERABLE NAME WAS SHARED BETWEEN CELLS, AND A2e's FILE WAS STILL SITTING IN IT.**
   Every cell concatenated into `/tmp/kc2_cpb/tmp-cpbprime-cadence-ab.mp4`, and the promote tool reads
   that path. A render that failed **quietly** would have left the promote tool verifying, hashing and
   **promoting A2e's 43 MB under A2g's name — with every gate green all the way through.** FG-9
   protects the deliverable path; it cannot protect a temp path two cells share. The stem is now
   cell-specific. **(NOTE-76.)**
2. **PROBE SIDECARS NO LONGER LAND ON THE DELIVERABLE PATH.** `--out` decides only where the per-shot
   JSON goes — frames go to `--write-movie`, so no pixel changes — but the matrix probes the DEMOTED
   shots, and a `shot-B-undulating-d-close.json` in the A2g capture directory would be a record of a
   shot the clip does not contain (A2f's orphan crash record is the precedent). Probe legs write to
   `$TMP`; `$OUT` is swept of stale sidecars before the run. **It also caught a real trap:** the
   anti-overfit leg writes a `shot-B-undulating-canon.json` at **tick 1660**, and had that reached the
   deliverable path in the wrong order the manifest would have carried a subject measurement from a
   frame the clip does not contain.

### 2.3 THE ARTICLE, UNCHANGED

`PREROLL_FRAMES 60` and the per-tick `seek_phase` **as shipped** — untouched, verified at close.
Tick from the frame index, never accumulated delta. `WEAPON_SCALE` **1.95**, `GRIP_FRAC` 0.20,
`GRIP_SEAT_M` 0.10, `CUT_PER_REV` **17**, `CUT_PERSIST_REVS` 0.45, `CUT_SEED` 20260813, epoch bands
5..13 / 0.10..0.40, `player_rev_period_s` **0.36**, the whole `PAL_*` ramp — every one read back at
HEAD and unchanged. **The lens is the only authored change.**

---

## 3 · ITEM 3 — THE MANIFEST · the promote tool's **first live run ever**

A2f's surface 8: *"THE PROMOTE TOOL IS WIRED FOR A2f AND HAS NEVER BEEN RUN."* The FG-10 halt meant
no render ever reached it. So the charter's rider — *a manifest that asserts what wasn't measured is
a defect* — became the design principle of the rewrite rather than a promise in a comment.

### 3.1 ⚑ THE CLAIM LEDGER — 19 ROWS, EVERY ONE CHECKED, ALL PASS

`verify()` collects a verdict per assertion, prints it, folds it into the manifest as
`claims_verified`, **and halts before promotion if any row is false.** A sample of what that means in
practice: the canon **distance is recomputed** from the rectangle in Python and matched against the
sidecar; the **eye is recomputed** from the angles by the wr1 orbit formula and matched to 1e-3; the
concat is checked to be **exactly its parts** (658 = 320 + 18 + 320, no frame lost, none invented);
the seam is checked to **actually be black**; the A2e reference is **re-hashed from bytes** before it
is compared against.

**Two rows that would have been decoration if they had not been checked:**
* *"each segment plays 1× trace time"* — playback is **10.6667 s against 10.6122 s of trace, +1.63
  frames.** That is the frame quantization of a 130-tick window (`ceil()` plus the writer's quit
  frame), so the bar is **two frames**, stated as such, rather than a tolerance chosen to pass.
* *"the seam actually dips to black"* — **held-black Y = 16.0 mean and max over 14 frames**, which is
  true black in limited range, against **picture Y 58.36** immediately before the dip.

### 3.2 THE MEASURED BLOCK

**Realized cut density, both cadences, at rate 17 — read from the smoke's own evidence, with the
sentence it was parsed from shipped beside the numbers:**

| | **stationary (segment A)** | **undulating (segment B)** |
|---|---|---|
| births over 790 windows | 1,360 | 908 |
| **mean per revolution** | **16.999** | **11.371** |
| sd | 0.4134 | 1.9200 |
| range | 16..18 | 5..16 |
| **thick / thin** | **1.12** | **3.20** |

The undulating mean sits **+0.371** inside the ratified 11.0 ± 0.5 band. The breath is the **3.20**.

**The canon window itself (ticks 1570–1700 = 29.48 revolutions):** **36 sequence restarts**, thinnest
frame **1 cut**, longest fully-dark run **0.0000 s** measured at the render's own cadence (analytic
worst case anywhere the seed can reach: 0.0148 s = 0.44 of a frame). Segment B's manifest carries the
**full realized epoch schedule, all 36 rows** — first epoch **460 at tick 1571.13, re-anchored to
39.20°**; last epoch **495 at tick 1697.17, re-anchored to 248.32°** — computed from `CUT_SEED` alone
so the frames can be checked against it rather than believed.

**Ellipse, subject, seam, camera derivation:** § 1.1 and § 1.4 above, all in the manifest.

### 3.3 THE ANCESTRY BLOCK — THREE DELTAS, DECOMPOSED AND ATTRIBUTED

Matt watched **one** clip (`cpbprime-cadence-ab.mp4`, `e2f6a03cc490…`, re-hashed from bytes here).
Three things have moved since, and the block exists so he knows which is which **and on whose word**.

| # | what moved | on whose word | landed by |
|---|---|---|---|
| **1 · RATE** | `CUT_PER_REV` 11 → **17** | **MATT**, R-CPB-15 — *"increase the sequence rate across the board"* | A2f item 1, `34dcd41` |
| **2 · CLOCK** | locomotion phase = f(tick) + a 60-frame tick-frozen warm-up | **the run's** — A2f's halt proved the scene never rendered the same span twice | CLK-1, `e81a827` + `6eff089` |
| **3 · LENS** | fov 48 scene-derived → **47 / −50 / 24 at 168.863 m** | **MATT**, R-CPB-16 | A2g item 1, `c011182` |

**Delta 1** — undulating mean 8.333 → **11.371**, thick/thin 2.40 → **3.20**. CLK-1 measured the
raise against the A2e bytes at rate 11 and found **+0.40/channel** above the codec floor, i.e. A2e's
own jitter: the raise changed the cut layout and no other pixel.

**Delta 2** — **CITED from CLK-1, not re-measured**: codec floor 0.95 · A2e's own jitter +0.40 · **the
locomotion seek +0.14 (3 %)** · **the warm-up preroll +5.01 (97 %)**. ⚑ **And the manifest states the
caveat on citing it:** those numbers were measured **through the old lens**, where the smoke bed and
spark ring filled the lower centre of frame. Under the canon frame the same 3.0 m bed is a few dozen
pixels across, **so +5.01 does not transfer to this clip as a magnitude.** What transfers is the
DECOMPOSITION (3 % / 97 %) and the conclusion: no body, no geometry, no palette, no cut layout moved.
Re-measuring it here would confound the clock delta with the lens delta.

**Delta 3** — the parallax and subject re-declaration of § 1.4, with the demoted frames **measured**
rather than quoted, and the zoom fork's arithmetic supplied and **not applied**.

**What did NOT move:** scale 1.95, grip, palette and knee, epoch bands, spin 0.36, cut pool, seed,
tick window, baton. Verified in the sidecars and at the commit.

### 3.4 THE PROMOTED ARTIFACT

| file | sha256 | bytes |
|---|---|---|
| `a2g-canon-cadence-ab.mp4` | `4ab0e27357c5d44438a52197bfae35ebce214f30fe206bf0fe0965e635888467` | 3,999,919 |
| `MANIFEST.json` | `1a58a93e2c937568f2ddd02cdef1a2e79857a0020e6f505bd106c8e277927296` | 168,431 |
| `shot-A-stationary-canon.json` | `716968fae9d74152f1d4446a316f8c8c1fab5529888666396fb259547f005d36` | 48,046 |
| `shot-B-undulating-canon.json` | `263cfad7892c04b300be186119408de819d82507600a45272a20eb2e2d283144` | 58,844 |

**ffprobe:** h264 · yuv420p · 1920×1080 · 30/1 · **658 frames** · **21.933333 s** · 1,458,937 bit/s.
**Timeline:** A-stationary 0.00 → 10.67 s · dip to black 10.67 → 11.27 s · B-undulating 11.27 →
21.93 s.

---

## 4 · LAWS

**GL-6** — recomputed from bytes before anything was touched: `d7ecd866ac45…`, 1,065,632 B — **MATCH**
(§ 0), and re-asserted by the arena's own gate on all 22 process launches.

**GL-12 — THREE ABSENCES DECLARED, NONE FILLED.** (i) The `canon_derivation` block is **absent** on
the demoted diagnostics' sidecars rather than faked — a reader can tell from the sidecar alone which
frame they hold. (ii) The demoted-frame measurement block says `ABSENT` if a probe sidecar is not on
disk rather than falling back to the prediction. (iii) Inherited and unclosed: the particle phase is
still process-clocked (no seek API) and the warm-up transient's sub-mechanism is still **named, not
proven**. Both are written where a reader meets them, in `kc2_cpb_clip.gd`.

**GL-13** — the pinned rectangle was **READ and never moved**: 86.915 × 85.303 m. The canon distance
is derived FROM it; nothing in this cell writes to it.

**GL-15** — one ongoing-damage read, unchanged: bed + haze, the 24-node cut pool, 3 burst emitters,
one wire bit. Smoke row PASS.

**GL-17 / ADR-006** — **no acquisitions of any kind.** No asset copied, no mesh edited, no
dependency added. The wr1 rig was **read and cited**, never copied — the constants are transplanted
with line citations, which is reference-governs.

**GL-18** — one clock, as fixed by CLK-1, and **untouched by this cell**: tick from the frame index,
`PREROLL_FRAMES` 60, per-tick `seek_phase`. The five-leg matrix at full promoted span is the
artifact-level proof.

**R-A1-1** — re-asserted at HEAD with the canon camera in the tree: **5,123 nodes walked, 0
text/canvas nodes.** The dip is an encode filter, so the seam cannot introduce one either.

**D-14** — everything ran **classic**, off the factory spine. Only the post-hoc artifact gates
(`ffprobe_verifies`, `sha256_matches`) run on spine code, and they read a finished MP4 and change
nothing.

**PL-5** — floor-checked **before** frames, in two places: captures 6.74 G of 10 G, disk free 26.2 G.
At close **6.75 G**; the tree grew **4.08 MB**.

**FG-9** — temp → ffprobe → promote, green only. **FG-10** — five legs, promoted pairs at full span.
**FG-12** — **7 prune receipts, 5.0 G of intermediates reclaimed**, each with its regenerate command,
banked in the manifest.

**CL-2 / PL-7** — three commits, one per item; the two godot commits pushed as they landed.
**No CL-2 irregularity this cell.**

**Containment** — godot **229 untracked at open and 229 at close**; the one dirty tracked file
(`tmp/br2watch/measure/census.json`) is **not mine and was not touched**. ⚑ **No temporary
working-tree operations were performed in this cell** — nothing to declare under NOTE-69.

---

## 5 · SELF-ATTACK SURFACES (ranked, veto-open)

1. ⚑ **THE SUBJECT IS 5.59 % OF FRAME HEIGHT AND I SHIPPED IT ANYWAY.** The canon's own precedents
   put a body of this size at **13–28 %**. R-CPB-16 names "camera angle/zoom", and angle and zoom are
   pure lens numbers that transplant exactly; **distance is not a lens property**, it is a formula
   whose input is room size, and this room is 5× the werewolf room. So the frame that "matches Grim
   Dawn" at 17.5 m may not match it at 86.9 m — it matches the room's **angular size**, which is a
   different invariant. I executed the charter literally and did not compensate. **If the ruling meant
   the lens rather than the law, this clip is at the wrong distance and the fix is one constant
   (§ 1.4).**
2. ⚑ **THE BINDING EYE-CALLS NOW MOVE TO A FRAME WHERE THE ARTICLE IS 15× SMALLER THAN THE FRAME IT
   WAS RATIFIED IN.** R-CPB-16(c) routes density feel, palette knee and cadence read to this clip. The
   cut ring is **66 px across** here against **1,480 px** at d-close; the palette's knee lives inside a
   stroke a few pixels wide; the smoke bed is a few dozen pixels. **A ratification made through this
   frame is a ratification about a different visual quantity than the one made at d-close**, and I
   think that is worth Matt knowing before he uses it to rule on a ramp.
3. **THE EDGE JUDGEMENT IS MINE.** `maxf` vs `minf` is 1.9 % of distance. Small, reasoned,
   precedented — and still a call I made rather than one I was given.
4. ⚑ **CLK-1's +5.01 PREROLL DELTA DOES NOT TRANSFER TO THIS CLIP AND MATT STILL HAS NOT RATIFIED THE
   FX DRAW.** CLK-1 routed the FX-draw question to "Matt's eye at A2g". At this frame **he cannot
   settle it**: the layer that changed is tens of pixels across. The question is not answered by this
   clip; it is **deferred by geometry**, and saying so is better than letting a watch be mistaken for
   a ratification.
5. **THE DEMOTED DIAGNOSTICS STAYED AT 45-FRAME PROBE LEGS.** Full-span probing was spent on what the
   clip promotes. A regression in a diagnostic's frame 200 would pass. Declared trade; the legs are
   one word (`full`) from being upgraded.
6. **FG-10 CERTIFIES THE FRAMES, NOT THE LOOK, AND ON ONE MACHINE.** One distinct state across 3,112
   frames says the render is a function of the tick on **this** host at **this** load. CLK-1's
   surface 1 (the warm-up bound measured on one idle machine, load untested) is inherited unchanged.
7. **TWO OF FOUR GL-13 CORNERS ARE OUTSIDE THE FRAME.** Inherited from the canon rather than
   introduced (§ 1.3) — but it does mean this clip is not "the whole arena in one shot", and anyone
   reading it as an arena overview is reading it wrong.
8. **I REORDERED `apply_tick` IN `_ready`.** It moved above the sidecar write so the subject could be
   measured with the body posed where frame 0 stands it. It is still called exactly once, still before
   any frame, and the sidecar still lands before the frames — and the cross-cell digest match on legs
   4/5 (§ 2.1) is the proof that no pixel moved. But it is a reordering of shipped code in a cell whose
   charter says the lens is the only authored change, so it is declared rather than buried.
9. **THE CLAIM LEDGER CHECKS THE NINETEEN THINGS I THOUGHT OF.** It is a real improvement over a
   manifest of assertions and it is not a proof of correctness. Nothing in it would catch a claim I
   never wrote down.
10. **THE SUBJECT FRACTION MOVES WITH THE SPIN PHASE** — 5.59 % at tick 1570, 6.22 % at tick 1660,
    measured. I report the shot's own first tick as the headline and the band beside it; a reader who
    quotes one number to three decimals is over-reading it.
11. **I TOOK CLK-1's DECOMPOSITION ON TRUST, BY CHARTER.** The 3 % / 97 % split is cited, not
    reproduced. It was mine and it was measured, but not in this cell.
12. **Twenty unlicensed editor addons still stand in the tree; the helmet is still a tepid "ok."**
    Both untouched.

---

## NOTES (continuing from NOTE-75)

**NOTE-76 — FG-9 PROTECTS THE DELIVERABLE PATH, AND A TEMP PATH SHARED BETWEEN CELLS IS AN
UNPROTECTED PATH.** Four cells concatenated into the same `tmp-cpbprime-cadence-ab.mp4`, and A2e's
43 MB file was still sitting in it when this cell opened. A quietly-failed render would have had the
promote tool verify it, hash it, promote it and write a manifest about it — **every gate green, every
number self-consistent, the wrong movie.** A gate that checks "the promoted bytes are the verified
bytes" cannot notice that the verified bytes were never yours. **Name the temp after the cell, and
the whole class of failure disappears.**

**NOTE-77 — A ROW THAT ONLY CONFIRMS IS NOT AN INSTRUMENT: WRITE THE CHECK SO IT CAN CATCH THE CLAIM
YOU WROTE IT TO SUPPORT.** The rectangle row was written to prove the distance law framed the room; it
came back two corners of four and the *claim* turned out to be the wrong one, not the code. The law
fixes **scale**, not **containment**, and R-6's own room never fit either. **The measurement was worth
taking precisely because I already knew what it would say.**

**NOTE-78 — A CANON TRANSPLANTS ITS ANGLES EXACTLY AND ITS DISTANCE ONLY AS A FORMULA. ASK WHICH
INVARIANT THE RULING MEANT BEFORE YOU APPLY IT TO A DIFFERENT-SIZED SUBJECT.** Yaw, pitch and fov are
properties of a LENS and carry across unchanged. `DIST = 34 × (EDGE/17.5)` is a property of a
RELATIONSHIP, and its output moved 5× when the room did — so the same "canonical camera" put the
subject at 28 % of frame height in the room it was set in and 5.6 % in the room it was ported to,
with **not one ruled number changed**. **When you transplant a canon, transplant its constants and
then MEASURE what the formula did, because the formula is the part that can betray the ruling while
obeying it.**

**NOTE-79 — `[\d.]+` IS NOT A NUMBER, AND A PARSER OVER PROSE MUST SHIP THE SENTENCE IT PARSED.** The
density regex read `THICK/THIN = 1.12.` and returned the string `1.12.` — the full stop belongs to
the prose, and a decimal is `\d+(\.\d+)?`, not "digits and dots". It crashed, which was luck: one
character further and it would have returned a plausible wrong number into a manifest. **Two habits
fall out: use the grammar of the quantity rather than the alphabet of its characters, and carry the
source sentence beside the extracted value so a reader can check the parse by eye instead of trusting
it.**

---

*Landed by drax, presentation seam, 2026-08-13. The lens is Matt's, verbatim, and so is the arithmetic
that made the man small. HALTED after promote.*
