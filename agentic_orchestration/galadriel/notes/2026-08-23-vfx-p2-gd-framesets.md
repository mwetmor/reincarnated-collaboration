# GD-kit framesets — VFX archetype-binding run (P2), index note

**Date:** 2026-08-23 (amended same day, attempt 3 — see § 8)
**Author:** galadriel (visual-perception seam) — second resume of the GD-kit supplement
**Run:** VFX ARCHETYPE-BINDING RUN (P2), conducted by gandalf (RUN-CONDUCTOR)
**Governing rulings:** charter ledger L-16 (referent), L-18 (two skills / two roles), L-19 (owner criterion)
**Status:** CURRENT — evidentiary note
**Frames:** `agentic_orchestration/galadriel/captures/2026-08-23-vfx-p2-gd-framesets/`
**Companion:** `captures/2026-08-23-vfx-p2-gd-framesets/RESUMPTION.md` (knight-rider, stop record)

---

## 0. Resumed vs newly extracted

| Prior-spawn artifact | Disposition |
|---|---|
| `~/gd-scratch/eor-test-{1,2}/*.mp4` local copies (2.73 GB total) | **REUSED** — no re-copy from `/Volumes/`. This is the expensive part and it held. |
| `~/gd-scratch/eor1-gray-4fps.raw` (323.8 MB) | **REUSED** — geometry re-derived as **240×135 @ 4 fps, 9,993 frames** (the prior spawn left it unlabelled; 180×180 also divides evenly and is the wrong answer — 16:9 is correct for a 1920×1080 source). New detection series computed on top of it. |
| `~/gd-scratch/eor2-gray-4fps.raw` | Reused for reference only; eor-test-2 was **rejected as a frame source** (§ 2). |
| `_workbench/tt-names-*.png` (tooltip-name harvest) | **REUSED** — established the build is Soldier + Oathkeeper and yielded six confirmed skill names. |
| `_workbench/q1/`, `_workbench/q2/` (truncated orphan-ffmpeg output) | **NOT USED, NOT REGENERATED.** Both were sourced from the SMB mount and `q2` was truncated mid-write. Superseded by fresh native-resolution extraction from local copies. Left in `_workbench/`, which is now git-ignored. |
| `eor-test-2/{circle,whirlwind}/` 1,812 verification JPGs @ 900×600 | **INSPECTED, NOT PROMOTED.** These are downscaled crops of Crucible waves 150–160 and are not legible (§ 2). Retained as scratch, git-ignored. |
| `eye_of_reckoning/`, `judgment/` | Were empty. `eye_of_reckoning/` now filled; `judgment/` deliberately still empty (§ 4). |

Everything under `eye_of_reckoning/`, `circle_candidate_unresolved/` and `_evidence/` is **newly
extracted in this session** at native 1920×1080 from the local copies.

---

## 1. Referent selection (L-16 compliance)

Both L-16 fixtures were opened. `play-test-v1` was not touched.

| Fixture | Probe | Verdict |
|---|---|---|
| `eor-test-1/eor-warlord-2026-08-04 21-09-31.mp4` — 1920×1080, 60 fps, **2498.37 s** | Crucible **of the Deeps**, x10 spawn multiplier, Gladiator. Sustained combat band **≈798–1940 s** plus a second band ≈2000–2240 s. Moderate on-screen density; player silhouette and ground plane readable. | **SELECTED — all delivered frames come from here.** |
| `eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` — 1920×1080, 60 fps, **1034.10 s** | Crucible **of the Dead**, waves 150–160. | **REJECTED as a frame source.** Used only for the skill-window / tooltip evidence at t≈173–300 (pre-combat), which is where the build identification came from. |

**Why eor-test-2 was rejected.** The brief's own preference ("prefer legible instances, not fully
horde-occluded") disqualifies it. At waves 150–160 the frame is a superposition of 10–20
simultaneous emitters: the player aura, several devotion procs, riftspawn portals, enemy
telegraphs and a continuous curtain of floating damage numbers. In the prior spawn's own
`_workbench` contact sheets and in my re-check of `eor-test-2/circle/cast-806.50/`, no single
skill's boundary can be traced. It is excellent *density* footage and useless *identity* footage.
The richer-per-minute hypothesis in the L-16 note is true and irrelevant: density is what destroys
legibility here.

---

## 2. Build identification (load-bearing for everything below)

Character is a **Warlord (Soldier + Oathkeeper)**, confirmed twice: the class tabs in the skill
window (`Soldier | Devotion | Oathkeeper`) and the tooltip harvest.

Skill names positively read off tooltips (prior spawn's harvest, eor-test-2 t≈173–237):
**War Cry**, **Volcanic Stride**, **Eye of Reckoning**, **Tectonic Shift**,
**Summon Guardian of Empyrion**, **Divine Mandate**. Ascension confirmed separately by me from
its own tooltip at eor-test-2 t≈205.

**Judgment does not appear in any tooltip read, and I could not bind it to a hotbar slot.** See § 4.

Hotbar as read at native resolution (eor-test-1, t≈1396–1403; evidence
`_evidence/hotbar-cooldown-onset-stack-1396-1403.jpg` and the two `hotbar-eor1-*-x4.png` strips):

| Slot | Icon | Behaviour | Read |
|---|---|---|---|
| **R** (right mouse) | red swirling vortex | held; drives the red disc | **Eye of Reckoning — CONFIRMED.** Same icon as the tree node showing **26/16 invested**, adjacent to the hovered *Soulfire* node whose tooltip text explicitly says "…during the Eye of Reckoning". |
| 2 | running figure wreathed in flame | cooldown-gated, min observed interval **4.75 s** | Vire's Might / **Volcanic Stride** (high confidence, not load-bearing) |
| 3 | shouting face in profile + light burst | cooldown-gated, intervals 5.5–12 s, modal ≈8–12 s | **Unresolved.** Drives the pale expanding ring (§ 4). Icon and cadence both fit **War Cry**. |
| 4 | violet robed figure, arms raised | toggle/buff, never dark | **Ascension** — tooltip-confirmed |
| L (left mouse) | golden running silhouette | dark + countdown 1–2 s, then lit | movement action or a movement-rune component; not a VFX source of interest |
| 7 | orange figure, arm raised | not exercised in the sampled window | unread |

---

## 3. `eye_of_reckoning/` — archetype `whirlwind`

### 3.1 Role label (L-18)

**NOT a P3 style candidate.** Matt rejected this art at the owner instrument
("a generic magical aura that happens to be spinning along with the character"). These frames
enter P3 in exactly two roles:

1. **SEMANTICS GROUND TRUTH** — channel cadence, radius, and movement-while-channeling; the § 3.4
   "same move" layer.
2. **NEGATIVE STYLE ANCHOR** — the concrete referent for what the judge must score *down*.

Any downstream consumer that treats these as positive style exemplars is misusing them.

### 3.2 Frame table

Source `eor1` = `eor-test-1/eor-warlord-2026-08-04 21-09-31.mp4`. All frames PNG, 1920×1080,
unmodified native pixels (no crop, no resize, no colour transform).

| File | t (s) | Phase | Instance | What is visible |
|---|---|---|---|---|
| `eor1-t2015.600-prechannel.png` | 2015.600 | **pre / OFF** | A | Player mid-screen, no red disc. Immediate pre-onset baseline for the onset ramp. Ground plane and character silhouette both legible. |
| `eor1-t2015.733-windup-early.png` | 2015.733 | windup | A | First red return in the annulus (metric 10.0 → 19.2). A faint red wash appears under the feet; no defined edge yet. |
| `eor1-t2015.867-windup-mid.png` | 2015.867 | windup | A | Disc edge forming, ≈60 % of final radius; brightness still climbing. |
| `eor1-t2016.133-windup-late.png` | 2016.133 | windup | A | Near-final radius, brightness ≈80 % of steady state. |
| `eor1-t2016.400-active-established.png` | 2016.400 | **active (steady)** | A | Fully established disc. Canonical steady-state frame. Player silhouette largely swallowed. |
| `eor1-t1060.000-active-sustain.png` | 1060.000 | active | B | Clean mid-density instance. Player clearly at disc centre; two riftspawn portals (green) at frame left are *scene*, not skill. |
| `eor1-t1310.000-active-sustain-dense.png` | 1310.000 | active | C | Higher-density instance: disc competing with a green rift, a fire trail and several cyan crystal props. Included to show how the disc reads when contested. |
| `eor1-t1810.000-active-move-a.png` | 1810.000 | active + movement | D | Movement pair, frame 1. |
| `eor1-t1810.500-active-move-b.png` | 1810.500 | active + movement | D | Movement pair, frame 2. Background terrain has translated; the disc has not deformed, lagged, tilted or trailed. This pair is the movement-while-channeling evidence. |
| `eor1-t2012.667-active-late.png` | 2012.667 | active (pre-release) | A′ | Peak annulus response (72.5) immediately before release. |
| `eor1-t2013.200-release-decay.png` | 2013.200 | **release / decay** | A′ | Mid-decay, ≈45 % of peak. |
| `eor1-t2013.467-release-off.png` | 2013.467 | release complete | A′ | Disc extinguished (metric 5.1). Note: an unrelated pale bloom from another effect is present at frame right — it is **not** EoR. |

### 3.2b Supplementary cropped set — `eor-test-1/whirlwind/set-03-sustain-1118-LOWREAD/`

One cropped beat-set from the same (accepted) fixture is also tracked. It predates the switch to
native-resolution PNG delivery and survives only because it is the **one tracked contact-sheet
view** (`_sheet.jpg`) of an uninterrupted sustain burst, which is convenient for reading cadence
at a glance.

JPG 1040×640, crop `1040:640:440:230` (player-centred on the 1920×1080 source), sampled at 20 fps
from a 3.2 s window at t=1117.4.

| File | t (s) | Phase |
|---|---|---|
| `b1-sustain-a_t01117.80.jpg` | 1117.80 | sustain-a |
| `b2-sustain-b_t01118.35.jpg` | 1118.35 | sustain-b |
| `b3-sustain-c_t01118.85.jpg` | 1118.85 | sustain-c |
| `b4-sustain-d_t01119.40.jpg` | 1119.40 | sustain-d |
| `b5-sustain-e_t01119.90.jpg` | 1119.90 | sustain-e |

**Readability: LOW** — the acid-green Crucible-of-the-Deeps ground VFX washes the plate. Role is
the same as § 3.1 (negative anchor + semantics). **The § 3.2 native PNG set is authoritative for
any style read; do not use this set for colour or edge measurement**, only for cadence-at-a-glance.

Adjuncts in `_evidence/` (documented transformations, raw frames preserved above):

| File | Transformation | Purpose |
|---|---|---|
| `crop-eor1-t2016.400-player760.png` | `crop=760:560:580:220` | player-centred readability crop of the steady state |
| `crop-eor1-t1060.000-player760.png` | `crop=760:560:580:220` | same, second instance |
| `crop-ref-eor1-t2014.333-channel-absent.png` | none (full frame) | clean channel-absent reference from the same engagement |

### 3.3 Temporal-coverage flags

| Phase | Present? | Honest note |
|---|---|---|
| **Windup** | **Y — but it is a fade-in, not a windup.** | Measured spin-up **2015.667 → 2016.35 ≈ 0.70 s**. There is no anticipation pose, no wind-back, no charge tell. The disc's opacity ramps; the character animation does not lead it. Calling this "windup" is a courtesy to the taxonomy. |
| **Active** | **Y — dominant phase.** | Channel; held near-continuously through combat. In the 1040–1130 s window the player is channeling for the large majority of frames. Longest uninterrupted channel sampled: ≈2016.4 → beyond the sampled window. Measured release ramp **2012.67 → 2013.47 ≈ 0.80 s**. |
| **Impact** | **N — ABSENT.** | This is the single most important semantic finding. EoR has **no per-hit impact beat at all**. Enemies inside the disc take damage — floating numbers appear — but there is no contact flash, no hit spark, no stagger, no directional spatter, no secondary emitter at the point of contact. The impact channel is carried entirely by the damage-number HUD. |
| Cadence / rhythm | **N** | There is no visible periodicity in the disc. It does not pulse to a swing rate. Frame-to-frame it is a slowly rotating gradient. There is nothing in the art that tells the player how fast they are hitting. |

Because impact and cadence are absent rather than merely compressed, I have **not** forced frames
into those buckets.

### 3.4 Semantics measured (ground truth for the "same move" layer)

- **Radius:** disc outer edge ≈ **150–160 px** at 1920×1080 gameplay camera, ≈ **1.9×** the
  character's standing height. Constant; does not scale with enemy count or channel duration.
- **Anchoring:** rigidly player-centred. Across the 1810.0/1810.5 movement pair the disc's centre
  stays locked to the character with no lag, no elastic trail, no lean into the movement vector.
- **Spin-up:** ≈0.70 s opacity ramp. **Spin-down:** ≈0.80 s. Roughly symmetric.
- **Movement while channeling:** permitted and used constantly. The player walks at what looks like
  full or near-full speed with the channel up.
- **Occlusion behaviour:** the disc renders *over* the character's lower body and *over* enemies
  standing inside it. At steady state the caster is the least legible object in their own effect.

---

## 4. `circle_candidate_unresolved/` — HONORABLE PAUSE on Judgment

### 4.1 The pause, stated plainly

The brief specified a second skill, **Judgment** (thrown/targeted, creates a ground area →
archetype `circle`), and told me never to guess an identity into the corpus. **I am invoking the
pause.** `judgment/` is empty and carries a `README-EMPTY.md` saying why.

I did find, and have delivered, **one strong circle-archetype VFX event** — a large pale
shockwave ring — but I cannot bind it to the name *Judgment*.

### 4.2 What the event is, measured

| File | t (s) | Phase | Visible |
|---|---|---|---|
| `UNRESOLVED-eor1-t1400.400-pre.png` | 1400.400 | pre | Baseline, one frame before the hotbar cooldown starts |
| `UNRESOLVED-eor1-t1400.600-expand-early.png` | 1400.600 | expand | Pale wash beginning, centred near the player |
| `UNRESOLVED-eor1-t1400.750-peak.png` | 1400.750 | **peak** | Brightness peak; bright-pixel count 12.4× the local baseline |
| `UNRESOLVED-eor1-t1401.100-ring-max.png` | 1401.100 | ring maximum | Ring edge at maximum radius, clean arc readable against terrain |
| `UNRESOLVED-eor1-t1401.600-decay.png` | 1401.600 | decay | Residual dark ring decal on ground |
| `UNRESOLVED-eor1-t1423.500-onset.png` | 1423.500 | onset | Second instance, hotbar cooldown onset frame |
| `UNRESOLVED-eor1-t1423.750-peak.png` | 1423.750 | **peak** | 12.1× baseline |
| `UNRESOLVED-eor1-t1424.200-ring.png` | 1424.200 | ring / decay | |

Measurements:

- **It is a player-pressed hotbar skill, not a devotion proc.** This is the discriminator the brief
  worried about, and it is settled. I built a 4 fps brightness series for the hotbar slot-3 icon
  over 1380–1500 s and a screen-flash series over the same window. Slot-3 cooldown onsets at
  1400.50 / 1407.25 / 1423.50 / 1440.25 / 1465.00 are each followed by the screen flash at
  **exactly +0.25 s** (one sample), at 4.7×–12.4× the local baseline. Devotion procs do not put a
  hotbar slot on cooldown. Six of eleven detected onsets carry a large flash; the remainder are
  either threshold noise from the animated cooldown sweep or casts in sparse terrain.
- **Cooldown:** minimum observed re-fire interval **5.5 s**; modal interval **8–12 s**.
- **Geometry:** ring is **player-centred**, not offset toward the cursor. See
  `_evidence/UNRESOLVED-ring-centre-vs-player-crosshair.jpg` — four instances with a crosshair
  drawn at the player position (960, 520). The ring's centre tracks the crosshair across all four.

### 4.3 Why I will not call it Judgment

Two facts point away from it:

1. **Geometry contradicts the brief's own description.** The brief characterises Judgment as
   *thrown/targeted, creating a ground area*. This effect is emitted from the caster in every
   instance measured. A targeted cast should show its centre displaced toward the cursor at least
   sometimes; it never does.
2. **The icon and the cadence both fit War Cry.** Slot 3's icon is a shouting face in profile with
   a light burst — War Cry's iconography. War Cry is confirmed present in this build by tooltip.
   A player-centred pale shockwave ring at an 8–12 s cadence is War Cry's signature, and War Cry is
   a **Soldier** skill, which would make the identification *Judgment* not merely unproven but
   wrong.

And one fact points at absence: **Judgment is never named in any tooltip read from these fixtures,
and no hotbar slot's behaviour matches a ~4 s targeted ground AoE.** The plausible conclusion —
which I am flagging rather than asserting — is that **this build does not slot Judgment at all.**
EoR Warlords commonly run Eye of Reckoning + Vire's Might + Ascension + War Cry and skip it.

### 4.4 Two cheap experiments that would resolve it (for the conductor to route)

- **E-1 (≈15 min).** Template-match the slot-3 hotbar icon against every node in the Soldier and
  Oathkeeper trees at eor-test-2 t≈180–246 (both trees are open and at rest in that window;
  `_evidence/eor2-t232-oathkeeper-tree-zoom.jpg` is the Oathkeeper grid already cropped). A match
  in the Soldier tree falsifies *Judgment* outright and names the skill.
- **E-2 (owner, ≈2 min).** Ask Matt directly: *is Judgment on the gd-eor-warlord bar, and if so
  which key?* One sentence closes this. He built the character.

If both fail, the honest outcome is that the `circle` archetype has **no first-party GD frameset**
from the L-16 fixtures, and T-A should carry that as a provenance note rather than a silent gap.

---

## 5. Readability observations for P3 — action-CAUSED vs action-DECORATING (L-19)

Per-frame, against the owner's criterion.

### 5.1 Eye of Reckoning — the decoration failure, itemised

Best single frame for this: `_evidence/crop-eor1-t2016.400-player760.png`.

1. **No causal geometry.** The disc is a soft-edged radial gradient with faint concentric spiral
   striations. There are **no blades**, no weapon forms, no swept arcs, no motion-blur ribbons, no
   trail geometry of any kind. Nothing in the image asserts that a weapon is moving. The skill is
   named for spinning blades and contains no blade.
2. **The caster is occluded by their own effect.** At steady state (t2016.400, t1060.000) the disc
   renders over the character's lower body. You cannot see the arms, the weapon, or the swing. The
   move's *cause* — the character — is the least legible thing in the frame. This is the clearest
   single expression of "decorating": the decoration outranks the actor in the render order.
3. **No contact event on the receiving body.** In `eor1-t1060.000-active-sustain.png` and
   `eor1-t2016.400-active-established.png`, enemies stand inside the disc taking damage. There is
   **no flash on flesh, no spark on armour, no bone-crunch particle, no stagger, no directional
   spatter, no knock**. Damage exists only as HUD text. Under the owner's criterion the effect
   never touches anything.
4. **No cadence coupling.** The disc's brightness and rotation are constant. A player cannot read
   attack speed, hit rate, or crit from the art. Compare an action-caused reading, where each
   sweep would land as a discrete beat.
5. **Screen-space flatness.** The disc reads as a decal on the ground plane and a billboard on the
   character, not as a volume the character is carving. It does not respond to terrain, to props,
   or to bodies passing through it — nothing occludes it and it occludes everything.
6. **Colour carries all the identity.** Strip the red and this effect has no shape left. That is
   the operational definition of decoration: the VFX is a palette applied to a location, not a
   consequence of a motion.

**Verdict for the P3 judge:** action-DECORATING, unambiguously, on every axis tested. This is a
clean negative anchor precisely because it fails for *structural* reasons (missing geometry,
missing impact, missing cadence) rather than for taste reasons. A judge trained on it should learn
"aura ≠ move."

### 5.2 The unresolved circle candidate — a partial contrast

Worth noting even under the identity pause, because it is useful to the judge as *contrast*
regardless of its name:

- It **does** have a propagating front. `UNRESOLVED-eor1-t1400.600` → `t1400.750` →
  `t1401.100` show an expanding edge with a definite radius-over-time. That is a physical read: the
  thing travels.
- It **does** leave a residue (`t1401.600` shows a ground decal), i.e. it acknowledges the world.
- But it **still shows no contact response on bodies**: enemies overtaken by the front do not
  flash, stagger or spatter. So it lands roughly halfway — *caused* in its propagation, *decorating*
  in its termination.
- Practical caution for P3: at peak (`t1400.750`, `t1423.750`) the effect whites out ≈40 % of the
  frame. It is a poor style exemplar even if its identity resolves, because the blowout destroys
  the surrounding read. The ring-maximum frames (`t1401.100`, `t1424.200`) are the usable ones.

### 5.3 Scene confounds the judge must not learn

Two recurring elements in eor-test-1 are **environment, not player VFX**, and will contaminate any
naive frame-level judge:

- **Green crackling rings** (visible in `eor1-t1060.000`, `eor1-t1310.000`, `eor1-t2016.400`) are
  Crucible **riftspawn spawn portals**. They are circles on the ground and they are not a skill.
- **Cyan crystal fans** are static level props (Crucible of the Deeps decor), not an emitter.

---

## 6. Extraction commands (provenance)

All extractions read from **local copies** in `~/gd-scratch/`, byte-identical to the `/Volumes/`
originals (`/Volumes/reincarnated/` was read-only throughout; the only reads were the copies made
by the prior spawn).

```
V1="$HOME/gd-scratch/eor-test-1/eor-warlord-2026-08-04 21-09-31.mp4"
V2="$HOME/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
```

**Deliverable frames (all of `eye_of_reckoning/` and `circle_candidate_unresolved/`):**

```
ffmpeg -nostdin -v error -ss <T> -i "$V1" -frames:v 1 -y <OUT>.png
```

with `<T>` taken verbatim from the "t (s)" column of § 3.2 and § 4.2. No `-vf` — native
1920×1080, no resize, no colour transform.

**Evidence adjuncts (documented transformations):**

```
# player-centred crops
ffmpeg -nostdin -v error -ss 1060.000 -i "$V1" -frames:v 1 -vf "crop=760:560:580:220" -y _evidence/crop-eor1-t1060.000-player760.png
ffmpeg -nostdin -v error -ss 2016.400 -i "$V1" -frames:v 1 -vf "crop=760:560:580:220" -y _evidence/crop-eor1-t2016.400-player760.png
ffmpeg -nostdin -v error -ss 2014.333 -i "$V1" -frames:v 1 -y _evidence/crop-ref-eor1-t2014.333-channel-absent.png

# hotbar skill-icon strip, 4x lanczos upscale
ffmpeg -nostdin -v error -ss 1398.900 -i "$V1" -frames:v 1 -vf "crop=460:50:722:1032,scale=1840:200:flags=lanczos" -y _evidence/hotbar-eor1-t1398.900-x4.png
ffmpeg -nostdin -v error -ss 1403.000 -i "$V1" -frames:v 1 -vf "crop=460:50:722:1032,scale=1840:200:flags=lanczos" -y _evidence/hotbar-eor1-t1403.000-x4.png

# Oathkeeper skill tree (eor-test-2, pre-combat)
ffmpeg -nostdin -v error -ss 232 -i "$V2" -frames:v 1 -y ok-232.png     # then crop (690,280,1480,800), 1.15x
```

**Detection passes (reproducible, not deliverables):**

```
# activity + combat-band location, from the prior spawn's decimated scan
#   eor1-gray-4fps.raw : uint8, 240x135, 4 fps, 9993 frames
# screen-flash series: count of pixels > 205 in rows 10:112, cols 15:225

# hotbar cooldown series
ffmpeg -nostdin -v error -ss 1380 -i "$V1" -t 120 -vf "fps=4,crop=100:40:740:1042" -y hbs/f-%04d.png
#   slot-2 icon = local x 8:38, slot-3 icon = local x 47:77, rows 4:36

# EoR channel onset / release, red-annulus metric
ffmpeg -nostdin -v error -ss 2014.4  -i "$V1" -t 2.6 -vf "fps=15,crop=760:560:580:220,scale=380:280" -y ons/f-%03d.png
ffmpeg -nostdin -v error -ss 2012.6  -i "$V1" -t 1.9 -vf "fps=15,crop=760:560:580:220,scale=380:280" -y rel/f-%03d.png
#   metric = mean(R - (G+B)/2) over the ellipse annulus 25 < r < 95 (y scaled 1.6x for the isometric foreshortening)
```

---

## 7. Flags for the conductor

1. **`circle` archetype has no confirmed GD frameset.** `judgment/` is empty by decision, not by
   omission. Route E-1 or E-2 (§ 4.4) or accept the gap in T-A with a provenance note.
2. **EoR carries no impact beat whatsoever.** This is a semantics fact, not a style opinion, and it
   should reach the §3.4 "same move" layer: any Reincarnated whirlwind that *does* emit per-hit
   contact events is not merely prettier than GD's, it is doing something GD's does not do at all.
3. **eor-test-2 is unusable for identity work** but remains the right fixture for density/scale
   questions. Recommend it be re-labelled in the charter as a density referent, not a frame source.
4. **The reference set is one-sided.** Twelve `whirlwind` frames all pre-labelled negative, zero
   confirmed `circle` frames. If P3 trains or calibrates on this supplement alone it sees only what
   to reject. The Codex dossier lane is carrying the positive load; worth confirming that
   explicitly before P4 close.
5. **Scene confounds (§ 5.3)** — green riftspawn portals are ground circles that are not skills.
   If any part of P3 is automated over these frames, they will be mistaken for `circle` instances.
6. **`_workbench/` (746 MB) and `eor-test-2/` (117 MB) are now git-ignored** in that capture
   directory. They are scratch and fully regenerable from § 6. Say the word if the conductor wants
   them tracked instead.
7. **`framesets.json` v1 carried a wrong Judgment attribution; it is retracted (§ 8).** If anything
   downstream already consumed v1 — any Codex-lane fold-in, any P3 corpus staging — it must be
   re-read against v2. This is the one item in this note that requires an action rather than a
   decision.

---

## 8. Amendment (attempt 3, same day) — `framesets.json` retraction

A third spawn was fired against this workbench. It found the extraction **already complete and
already committed** (`a35e92cf`, 39 tracked files) and the resumption note already discharged
(`adefff2a`). No frames were re-extracted; nothing in `eye_of_reckoning/`,
`circle_candidate_unresolved/` or `_evidence/` changed. What it found instead was a **labelling
defect inside the landed commit**, which it has closed.

**The defect.** `framesets.json` v1 shipped in the same commit as `judgment/README-EMPTY.md` and
contradicted it. v1 described six framesets, three of them captioned:

```
"skill": "Judgment (attribution MODERATE)"
"p3_role": "style candidate — full status (L-18 unaffected)"
```

Three things are wrong with that, in ascending order of seriousness:

1. **It indexes files that are not in the repo.** Five of v1's six framesets live under
   `eor-test-2/`, which § 7.6 git-ignores. A consumer following that manifest finds nothing.
2. **It contradicts the pause it shipped beside.** § 4 invoked the honorable pause and left
   `judgment/` empty on purpose; v1 simultaneously asserted three Judgment framesets at full
   candidate status. Both statements were committed together.
3. **The name is probably not merely unproven but wrong.** § 4.3's leading hypothesis is
   **War Cry**, a *Soldier* skill. "Attribution MODERATE" dignifies a guess that the evidence
   actively leans against.

**Verification before retracting.** I did not retract on the mtime ordering alone — I looked at
the pixels. `eor-test-2/circle/set-01-cast-816/_sheet.jpg`: the pale front in `b4-spread` cannot be
separated from the green Crucible ground wash, and `b3-burst`'s white star sits at frame-left while
the ring centres elsewhere. `eor-test-2/whirlwind/set-01-wave-start-683/_sheet.jpg` degrades from
legible at `b1-approach` to total superposition by `b6-active-peak`. **§ 1's rejection of eor-test-2
as an identity frame source is correct**, and the sets built from it cannot carry a skill name.

**The fix.** `framesets.json` is now **v2** (`_schema: gd-kit-framesets/2`) and describes only what
is actually tracked: `ww-native-eor1` (12 frames), `ww-crop-eor1-set03` (5 frames, § 3.2b) and
`circle-unresolved-eor1` (8 frames, `skill: "UNRESOLVED — DO NOT NAME"`, both hypotheses carried
with their leans). It also carries a `_p3_consumer_warning`, the scene confounds of § 5.3 in
machine-readable form, and an `untracked_scratch` block so the git-ignored material is not mistaken
for an omission. The v1 Judgment attribution is recorded as **RETRACTED** in `_revision_note`.

**Net effect on the corpus: none of the evidence changed, and one wrong name was removed before it
could travel.** The frame count, the fixtures, the measurements and the pause all stand exactly as
§§ 1–7 record them.

---

*galadriel, 2026-08-23. Read-only on `/Volumes/reincarnated/` throughout. No other capture
directory was modified. No sub-agents invoked.*
