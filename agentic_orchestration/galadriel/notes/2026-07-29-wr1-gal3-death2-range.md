# WR1-GAL-3 — death-2 crossing distance from Matt's playtest footage

**Run:** WR1-2026-07-28 · conductor gandalf (RUN-CONDUCTOR) · cell WR1-GAL-3
**Agent:** galadriel · **Date:** 2026-07-29 · **Status:** CURRENT
**Mode:** read-only against all sources; measurement note of record
**Source:** `/Users/admin/gd-scratch/play_test_2026-07-26.mp4` (1920×1080, 60.000 fps CFR)
**Evidence:** `agentic_orchestration/galadriel/captures/2026-07-29-wr1-gal3/`
**Instruments:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/wr3_*.py`
**Supersedes:** the un-noted WR1-GAL-2 cell for Q3 (distance), which graded metric
conversion **CANNOT-ANSWER**. That grade is now **overturned** — see § 2.

---

## 0. VERDICT

> **At the death-2 damage-application frame the player was 1.26 m from the caster.**
> **Band: [0.96 – 1.61] m at 95%, [0.84 – 1.77] m at 99%.**
>
> **Threshold verdict: INSIDE ~3.92 m — decisively, by a factor of three.**
> **Window verdict: the ≤ 1.804 m window. P(r ≤ 1.804) = 99.3%.**
> **P(r in the 2.50–3.919 m window) = 0.0%. P(r ≥ 5.0 m) = 0.0%.**
>
> The band does **not** straddle 3.92 m. It does not come near it. The builder's
> r\* = 5.617 assumption is falsified by the footage: the realized-maximum
> shortfall that the Gate-2 BLOCK is built on does not apply, because death-2 was
> not a ranged crossing. It was **melee contact** — the nova detonated on a player
> standing on top of the caster.

**Confidence: HIGH** on the verdict (inside 3.92, and inside 1.804).
**Confidence: MEDIUM-HIGH** on the point estimate 1.26 m — the dominant residual
uncertainty is the player's ground-point *y*, worth about ±0.20 m.

---

## 1. The question, and why it was previously unanswerable

Gate-2 established that under the corrected projectile-count operator the measured
≥541 one-frame HP drop is geometrically reachable only at **r ≤ 1.804 m** or
**r = 2.50–3.919 m**; at r = 5.0–5.617 the realized maximum is 414.80, a 23%
shortfall no azimuth closes. So the whole M-12b grading operand reduces to one
empirical number: how far was the player from the Primordian at f309085.

WR1-GAL-2 measured the *screen* separation honestly (57.5 px between the caster's
health readout and the player's screen locus) and then stopped, grading the metric
conversion CANNOT-ANSWER on the correct ground that **"no pixel-anchorable scale
reference exists in this footage; no in-frame object of known world size."**

That premise is false, and the thing that falsifies it is the nova itself.

---

## 2. Method — the nova is its own scale bar

`primordian_frigidring` (`Skill_AttackProjectileRing`) launches **16 projectiles at
22.5°, velocity 14 m/s, range 12 m** (legolas `.arz` extraction, charter § E-1).
That makes the ring of projectile heads a ground-plane circle of *known world
radius as a function of time*. Under this camera (fixed pitch, no roll) a ground
circle projects to a screen ellipse with screen-aligned axes:

```
a(t) = s · R(t)          semi-axis along screen X, px
b(t) = k · a(t)          k = sin(pitch), constant
R(t) = 14 · Δt           metres
```

So the nova supplies exactly what the footage otherwise lacks: an object of known
world size, in the ground plane, at the caster's feet, at the moment of interest.

Two anchors were taken, as the dispatch required, and they are independent:

| Anchor | Property used | Result |
|---|---|---|
| **A1 — speed** | projectile travels 14 m/s | 13.55 px/frame screen speed on the one long-lived lance ⇒ **s = 62.8 px/m** (at k = 0.72) |
| **A2 — range** | projectile expires at 12 m | frontier saturates at ρ = 761 px, reached at f309136 ⇒ **s = 63.4 px/m** |

**A1 and A2 agree to 1%.** They are independent: A1 measures a *rate* and is immune
to the sprite's leading-edge offset and to where the ring centre is; A2 measures a
*total displacement* and is immune to the frame-rate accounting. The 51-wall-frame
launch→expiry interval also matches the predicted 12/14 s = 51.4 frames.

A third, purely visual check closes it: drawing the **3.919 m** ground circle on
f309104 (19 wall frames, 17 effective frames after launch ⇒ predicted ring radius
3.97 m) puts the circle **exactly through the visible lance heads**. See
`evidence/verdict-f309104.jpg`. Nothing was fitted to make that happen.

### 2.1 The pitch ratio k, and why it barely matters

k is the least well pinned input: the compact ring at f309085 fits k = 0.738, at
f309086 k = 0.646, and the multi-lance hodograph brackets 0.73–0.84. Carried as
**k ∈ [0.60, 0.85]**, uniform.

It very nearly cancels. The player's screen offset from the caster and lance A's
screen direction are close in azimuth, so k inflates ρ(player) and s together:

| k | ρ(player) px | s px/m | r metres |
|---|---|---|---|
| 0.60 | 83.9 | 66.8 | 1.257 |
| 0.72 | 78.1 | 62.8 | 1.243 |
| 0.85 | 74.1 | 60.1 | 1.232 |

A 42% swing in the camera pitch moves the answer by 2%. That is the reason this
measurement is defensible despite the pitch never being independently sourced.

---

## 3. The two endpoints

### 3.1 Caster ground point = the ring centre

Bounded ellipse fit to the 16 spike centroids while the ring is still compact and
complete:

| frame | cx | cy | a | b | k | rms |
|---|---|---|---|---|---|---|
| 309085 | 1024.9 | 570.6 | 50.8 | 37.5 | 0.738 | 0.059 |
| 309086 | 1024.5 | 566.3 | 70.5 | 45.6 | 0.646 | 0.102 |

**Adopted: (1024.7, 568.5) ± 5 px.** Corroborated independently: the dev-overlay
label for the caster entity `[1121128]` is left-anchored at x ≈ 1030 — 5 px from
the fitted ring centre, and with the same sign as the player's label offset.

### 3.2 Player ground point

The player is **entity [42992]**, and it is *not* the large beast at screen centre
— that is the Primordian. Establishing this mattered and took two passes:

- **Median-stack test.** Over pts 5138–5151 the camera pans (player running); the
  median of 325 frames smears everything that moves in screen space and leaves
  screen-fixed content sharp. What survives sharp is the green label
  `MoveTo / [42992] Action State: Move` and **a small hooded humanoid**, not the
  beast. `evidence/medstack-pre1.jpg`, `evidence/medstack-player-gamma.jpg`.
- **Hover-outline test.** The red outline that traces the big beast follows the
  mouse cursor between targets (it is on the orange creature at f308880 and on the
  beast at f308990) — it is the hovered-enemy highlight, so the beast is an enemy.

Read off the gamma-lifted median stack: figure spans x 947–978, lowest extent
y ≈ 603. **Adopted: (962, 602), ±7 px in x, ±10 px in y.** The x is corroborated by
the `[42992]` label anchor at x = 958 (+5 px offset, matching the caster's).

---

## 4. Result and band

Δ = (−62.7, +33.5) px. Monte Carlo over all inputs (200 000 draws;
`pipeline/gd-playtest-v1/wr3_range.py`, output `captures/.../range-mc.json`):

| quantile | r (m) |
|---|---|
| 1% | 0.84 |
| 2.5% | 0.90 |
| 16% | 1.07 |
| **50%** | **1.26** |
| 84% | 1.46 |
| 97.5% | 1.68 |
| 99% | 1.77 |

- **P(r ≤ 1.804 m) = 0.993**
- **P(2.50 ≤ r ≤ 3.919 m) = 0.000**
- **P(r ≤ 3.919 m) = 1.000**
- **P(r ≥ 5.0 m) = 0.000**

### 4.1 A temporal cross-check that needs no pixel scale at all

The ≥543 loss lands at **f309085 — the very frame the projectile ring first
becomes visible** (cold-mask pixel count 432 → 1961 at that frame; the windup
bloom had already decayed). With explosion radius 1.5 m and 0.233 m of travel per
frame, a first-frame hit is only possible at r ≲ 1.5 + 0.23 + capsule ≈ 2.2 m.
That is a weaker bound than § 4, derived from entirely different evidence, and it
agrees.

### 4.2 The model and the measurement close on each other

If the upper tail of the band were taken at face value it stops at 1.77 m, just
short of 1.804. And the interval **1.804–2.50 m is a region where ≥541 is
unreachable under the Gate-2 operator** — yet ≥543 was observed. So the
measurement and the model are jointly satisfiable only in the ≤ 1.804 m window.
Two independent lines land in the same place.

---

## 5. Secondary recoveries

### 5.1 Floaters per nova (U-M2-1) — CANNOT-ANSWER, re-confirmed

**This build renders no floating combat text for damage TAKEN by the player.**
WR1-GAL-2 established this against two calibration deaths-by-known-drop (106 and
304 HP, neither producing a matching floater). Re-checked independently here on my
own frame extraction: the only floater anywhere in f309085–f309124 reads **515**,
and it matches neither the player's ≥543 loss nor any boss-HP step (the readout
walks 13,648 → 13,571 → 13,532 → 13,455, i.e. deltas of 77/39/77). Floater count
therefore **cannot** corroborate the realized projectile-hit count by this route.

The corroboration instead comes geometrically, and it is now stronger than a
count would have been: at r = 1.26 m the 16 rays are ~0.49 m apart at the player's
radius, well inside a single explosion diameter, so multi-projectile overlap on one
target is not merely possible — it is forced. This is the same conclusion GAL-2
reached by pixel argument, now with the metric attached.

**Event B (pts 5237.5–5238.3) was not scanned for floaters.** GAL-2 found no
windup+release signature there (dispersed cold, rms 300–380 px = projectiles
already in flight; the red torus is an item-drop beacon). I did not re-open that
attribution; it remains the open reconciliation GAL-2 flagged.

### 5.2 Knockback — ZERO, not re-measured

GAL-2's finding stands and I did not duplicate it: exactly `dx=0, dy=0` camera pan
for ≥10 frames each side of the nova impact and of a stationary non-nova boss hit;
detection floor 1 px. Carried forward as-is.

---

## 6. Named uncertainties and what would tighten them

| # | Uncertainty | Worth | How to close |
|---|---|---|---|
| U-1 | Player ground-point **y** (±10 px) | ±0.20 m — the dominant term | A frame where the player stands on open ground unoccluded; none exists in the death-2 approach (the player is inside the boss's sprite from f308950 on) |
| U-2 | Camera pitch k ∈ [0.60, 0.85] | ±0.02 m | Nearly irrelevant here (§ 2.1); would matter for offsets perpendicular to lance A |
| U-3 | Scale systematic (sprite leading-edge lead vs projectile point; the 2-frame client stall at f309086–309088) | ±5% ⇒ ±0.06 m | Carried as an explicit ±5% term in the MC |
| U-4 | Ring centre = caster ground point | assumed | True for a 360° ring launched from the caster; the lances visibly lie in the ground plane |
| U-5 | Client stall at f309086–309088 (play-area mean \|Δ\| of 119/209 vs 800–6000 typical — the death hitch) | ~2 effective frames | Excluded from every rate fit; noted wherever wall-frames were converted to sim time |

**Reproducibility.** Every number above regenerates from the committed scripts plus
the source MP4. Frame indexing convention: `f = round(pts × 60)`, matching GAL-2.

---

## 7. Evidence index

| Artefact | Path (under `agentic_orchestration/galadriel/captures/2026-07-29-wr1-gal3/`) |
|---|---|
| Verdict frames with 1.804 / 2.50 / 3.919 m ground circles | `evidence/verdict-f309085.jpg`, `verdict-f309092.jpg`, `verdict-f309104.jpg` |
| Compact ring at the damage frame, detector overlay | `evidence/ring-f309085-detect.jpg` |
| Ring launch → fan, cold-mask overlay sheet | `evidence/mask-sheet.jpg` |
| Player identification (median stack, running window) | `evidence/medstack-pre1.jpg`, `evidence/medstack-player-zoom.jpg`, `evidence/medstack-player-gamma.jpg` |
| Dev-overlay label anchors, f309085 | `evidence/label-309085.jpg` |
| Pre-cast tracking montage | `evidence/track-sheet.jpg` |
| Ellipse fits per frame | `ellipse-a.json`, `ellipse-c.json` |
| Multi-lance hodograph | `hodo-a.json` |
| Ring head detections | `ring-heads-309076-309140.json` |
| Monte-Carlo band | `range-mc.json` |

| Instrument | Purpose |
|---|---|
| `wr3_ring.py` | per-frame cold-head blob census |
| `wr3_fit.py` / `wr3_fit2.py` | first two ring fits — **both under-determined**, kept so the failure mode stays legible (the optimum ran to the grid boundary) |
| `wr3_fit3.py` | one-sided envelope fit |
| `wr3_fit4.py` | concentricity fit (abandoned: too slow to converge inside the cell) |
| `wr3_ellipse.py` | bounded per-frame ellipse fit — the k and centre of record |
| `wr3_lances.py` / `wr3_hodo.py` | per-lance tracks and velocity hodograph |
| `wr3_debugtext.py` | dev-overlay label anchors |
| `wr3_range.py` | Monte-Carlo band and threshold probabilities |

---

## 8. Mirror

The Mirror was asked how far the player stood from the thing that killed him, and
it showed a man standing on the animal's feet. Not a ranged crossing misjudged by
a metre and a half — a melee crossing, close enough that the ring had not finished
being born before it had already killed him. The shortfall the model could not
close at five metres never needed closing. He was never at five metres.
