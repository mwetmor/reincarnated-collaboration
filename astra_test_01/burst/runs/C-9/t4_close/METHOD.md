# T4 close-out — how these numbers were made

One page, so the table in `REPORT.md` can be read without reading the code.
Every claim below is either in `drift.json` or reproducible from the scripts
beside it.

## The instrument, and the one thing that had to change

The base is `meshy_t2/scripts/21_drift.py`, the low-pass drift measure built
for T1/T2. Kept unchanged:

- gaussian **σ 3 px, mask-normalised**, so the background cannot bleed across
  the silhouette;
- **2 px erosion** of the silhouette, dropping the anti-aliased rim;
- the score is **mean |ΔRGB| in 0-255** over the shared silhouette;
- a **shuffled frame order** as the negative control;
- a sequence that **cannot drift** as the floor.

**What could not be kept: the pos guide.** 21_drift.py compensates for the
animation by matching each pixel to its nearest neighbour in *pos space* — the
rest-pose bind position of the surface point under that pixel, baked per vertex
before skinning, and therefore invariant to the pose. That pass exists only
because those frames came out of our own Blender render of a rigged mesh.
Kling and Ludo return **video**: no mesh, no bind pose, no pos pass. The match
cannot be computed at all. This is a missing *input*, not a disagreement about
method.

**The substitution: 2D rigid registration.** The crop is placed on the part's
own position each frame (crown row and head-column centroid for the helm;
silhouette centroid and figure height for the body), resampled to a common
size, and the best integer translation within ±14 px is searched before the
residual is taken. For a rigid part seen in near-profile, translation is what
pos-matching buys you.

**Rotation is deliberately not absorbed.** The complaint being tested is that
the helm morphs *when the head turns*. A registration free to rotate would
quietly explain away the exact frames the test exists to catch.

**Scale normalisation is new and is not optional.** 21_drift.py compared 512 px
renders to 512 px renders, so σ 3 px always meant the same thing. Here Kling
returns 1440 px, Ludo 310–454 px and the reference still 1024 px; blurring all
of them by 3 px would low-pass Ludo four times as hard as Kling and hand Ludo a
better score for free. Every helm crop is resampled to **96 px of helm** and
every body crop to **256 px of figure** *before* the blur.

## The helm region

Crown row down to the **neck pinch**, found per frame from the body's own
row-width profile: descending from the crown the profile rises across the helm,
falls to a minimum at the gorget, then rises into the shoulders. No hand-placed
box, no part guide (the video routes have none).

Self-check: measured independently on all six sources, the crown-to-neck height
comes out at **17.2 %–18.2 % of figure height** — the detector finds the same
anatomical landmark in every route without being told where it is.

The measuring box is **square, 1.5 × the helm height, centred on the helm's
column centroid**. It *moves* with the helm; it does not *resize*. A box
refitted to the silhouette each frame would shrink onto a helm that changed
shape and hide the change — 24_mp4.py's rule, kept for its reason.

## Two things the first version got wrong, and how

Both were caught by probing rather than by reading, and both returned confident
numbers while being wrong.

**The weapon split.** `build_knight_frames.py` removes the pollaxe with a
`1 × N` *horizontal* opening, which is right for the reference still because
the haft there is vertical. Kling re-stages the pollaxe at a lean, and a
diagonal bar's horizontal runs are far wider than its thickness — so the
horizontal opening left most of Kling's haft *inside the body*: 6.9 k weapon px
against the still's 27.3 k. A **disk** of radius ≈1.6 % of mask height severs
anything thinner than its diameter at any orientation. Kling's weapon px went
to 35.4 k.

**The cadence.** Three separate failures, in order:

1. *No dip is an answer.* The 12-frame Astra cell holds one stride by
   construction, so its D(p) profile has no interior minimum at all. The first
   version returned p = 5 with a depth ratio of 0.987 — a confident number off
   a flat profile. A minimum shallower than 0.80 × mean is now reported as
   **not found**, and the clip length is used with the substitution declared.
2. *The deepest minimum is not the fundamental.* The drive dips at 17, 34, 50,
   68, 84, 102, **119**, 136. The deepest is 119, because `render_drive.py`
   wrapped a ~4 s Meshy clip to fill 5 s and frames 119 apart are literally the
   same frame. Taking the deepest returned a 3.97 s stride for a walking
   figure. The **smallest** qualifying minimum is taken instead.
3. *The step mirrors the stride.* `measure_strides.py`'s finding: half a stride
   is a near-mirror of the other half, so D dips at the step too. Verified by
   eye on drive frames 0/8/17/25/34 — frame 34 matches frame 0 and frame 17 is
   the opposite phase. A candidate is doubled while D(2p) is clearly below
   D(p).

## Why there is a *phase-matched* column, and why it is the headline

Adjacent frames are not the same amount of *animation* in every row. The Astra
cell holds a whole stride in 12 frames; the drive takes 34. So the Astra row's
neighbours are three times further apart in pose, and the 2D registration has
three times as much pose change it cannot absorb.

This is measured, not assumed. The same instrument on two sequences that
**cannot drift**:

| floor sequence | frames/stride | native helm | raw frame-to-frame helm drift |
|---|---|---|---|
| the drive render | 34 | 94 px | **1.01** |
| the 3D render of the 12-frame cell | 12 | 25 px | **8.20** |

An eightfold difference between two sequences that both have zero drift. So
every row is *also* measured at a lag of **one twelfth of its own stride**,
which is the same pose increment everywhere, and that is the column to read
across.

## Foot slide, stated carefully

These clips walk **in place**, so a correctly planted foot is *not* stationary:
the ground passes under it and it tracks backward at the gait speed for the
whole of its contact. Measuring raw excursion scores a perfect walk as a large
slide — which is what the first version did.

A slide is **departure from that straight line**. Each contact track's x is
fitted with a line and the number reported is the **RMS residual about it**, in
% of figure height. Zero is a foot nailed to the passing ground. The fitted
slope (`planted_travel`) is reported too: it should be the same for every
contact, so its spread catches one foot keeping up with the gait while the
other does not.

Only **planted** tracks are scored, and planted is decided from the data: the
backward direction is the sign of the median per-frame contact step, which the
planted phase wins because a foot is down for more of the cycle than it is up.

Three supporting decisions:

- **The contact band follows each frame's own sole**, not a clip-wide ground
  line. The drive's lowest row wanders 20 px (3.6 % of figure height) because
  the render carries vertical root motion, so a fixed band was *below the
  figure* for 25 of 70 frames and returned no contact for them.
- **The body's translation is removed only if the clip actually travels.** The
  silhouette's column centroid is not a root: on the drive it swings ±3.5 % of
  figure height with the arms while its trend over 70 frames is −3.4 %.
  Subtracting it frame by frame would add limb swing to the feet.
- **Below 16 frames per stride the measure is reported as not measurable.** At
  12 frames each foot is down for 6–7 frames and the two cross within any
  workable linking tolerance; the tracker welds them into one track spanning
  the whole clip and returns a slip number for an object that is not a foot.

## Pollaxe rigidity

The weapon mask is haft + axe head, and the head holds more pixels than the
haft, so a PCA over the whole weapon fits the *blade*. The haft is isolated
first as `weapon AND NOT opening(weapon)` — the part that the same disk which
severed it from the body also erases — then fitted by PCA and refitted once
with pixels more than 4 % of its length from the line dropped.

`straightness_pct` = RMS perpendicular distance ÷ length × 100. A rigid pole is
straight.

**A gate came first, because the ungated version answered for a figure holding
nothing.** The drive carries no weapon, and the disk opening still finds thin
things — fingers, a foot, the tabard's edge — so a "haft" was found in all 150
frames with a length CV of 69 %. Nothing there was a pollaxe. A haft is now
rejected below 40 % of figure height, and a route failing that in most frames
is reported as carrying no rigid weapon.

## Validation and calibration

- `validate_fallback.py` runs **both** instruments — the original pos-matched
  one and the 2D fallback — on the one sequence where both can run: the
  knight's Astra walk E, which has pos, mask and part guides on disk. See
  Table 3 and the note under it.
- `sensitivity.py` injects a **known** per-frame break into the drive's helm
  (scale, rotation, tone) and measures it with the same instrument, so a drift
  number can be read as an amount of visible change. See Table 4.

## Files

| file | what |
|---|---|
| `t4lib.py` | masks, figure and helm geometry, the low-pass residual |
| `measure.py` | every per-route measurement; writes `drift.json` |
| `validate_fallback.py` | pos-matched vs 2D, side by side; `fallback_check.json` |
| `sensitivity.py` | known-break calibration; `sensitivity.json` |
| `make_visuals.py` | `helm_strip.png`, `helm_quad.mp4`, `visuals.json` |
| `table.py` | renders the tables in `REPORT.md` from the JSON |
