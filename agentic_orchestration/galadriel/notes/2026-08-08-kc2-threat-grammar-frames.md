# Rider-2 — frame-level threat-grammar extraction against the KC2 fixture's own roster

**Date:** 2026-08-08 · **Author:** galadriel (visual perception + benchmark seam)
**Status:** CURRENT — evidentiary note of record for the Rider-2 companion lap
**Commission:** `gandalf/notes/2026-08-08-q52-ruling-and-riders.md` § 3 (Matt-approved 2026-08-08, Q52 ruling)
**Track:** PARALLEL — reports into the **Godot PLAYTEST milestone**. It is **NOT** a KC2-SIM gate,
it blocks nothing in that run, and nothing here is entangled with KC2 gate machinery.
**Vocabulary precedent:** `legolas/research/2026-07-30-wr3-stage2-referent-extraction.md`
(Primordian 0.489 s wind-up / 0.879 s recovery / 0.80 s nova telegraph / 79.6 % rooted).
**Companion (same lap, other half):** legolas — Edition-III `.arz` attack-timing field join.

**Substrate (frozen, read-only):**
- s1 `…/GD-matt-test/eor-test-1/video/eor-warlord-2026-08-04 21-09-31.mp4` (1920×1080, 60/1 CFR, 2498.367 s)
- s2 `…/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (1920×1080, 60/1 CFR, 1034.100 s)
- Local frame-work copies: `/tmp/eor-w150-160.mp4` (byte-exact s2) · `/tmp/tg/s1_death.mp4`
  (stream-copy of s1 **orig t = clip t + 2225.000**, offset pinned against the 92→93 badge flip at 2243.22)
  · `/tmp/tg/s1_early.mp4` (orig t = clip t + 799.000)

**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-threat-grammar/evidence/` (UNTRACKED — by-reference per convention)
**New instruments (committed):** `galadriel/pipeline/eor_playerhp.py` · `eor_hpevents.py` · `eor_campan.py` · `eor_kinematics.py`

**Commit-only, NO push** per commission standing rules.

---

## 0. Headline

> **The six timing axes the commission names — wind-up, recovery, telegraph shape, cadence,
> root-lock, approach speed — are NOT-OBSERVED for every family in this roster, and the reason is
> not occlusion. It is ATTRIBUTION.** This substrate names a body only while the cursor hovers it,
> and it times a hit only through the player's own health readout. The two instruments almost never
> point at the same body in the same frame. That boundary is measured in § 5, not asserted.
>
> **What the substrate DOES yield at frame resolution is the receiving end of the grammar**, and it
> yields it exactly: a 60 fps damage clock read off the player's HUD numerals, 100 % parsed across
> the s2 band. From it, the per-wave incoming envelope (§ 3), and both deaths reconstructed frame by
> frame and verified by eye (§ 4).
>
> **Three corrections to my own committed record fall out of that clock, one of them material:**
> **s2's death is at t = 864.8167, not 943.60.** Wave 160 ran **25.95 s**, not 104.73 s. The 943.60
> event I recorded on 2026-08-07 as "death (HUD fade onset)" is the **ESC menu** opening over an
> already-frozen post-death HUD, 78.8 s later.
>
> **The single most decision-relevant number in this lap:** at s2 t = 864.7500 the player went from
> **20,005/20,005 to 2,118 in ONE frame — 17,887 damage, 89.4 % of max health, inside ≤ 16.7 ms** —
> and was dead 4 frames later. From full health. Any Godot threat model that cannot produce that
> event is not reproducing this fixture.

---

## 1. THE INSTRUMENT — a 60 fps damage clock

### 1.1 What it reads

Grim Dawn draws the player's health as **numerals** on the HUD orb (`cur/max`), at a fixed box, in
cream-white over a saturated red orb. Fixed position means it never has to be *located* per frame —
unlike the in-world monster readouts, which is why every previous extraction of mine was hover-bound
and this one is not.

Box `x 572..689, y 1004..1027`. Mask = `min(R,G,B) > 140`. **The threshold is calibrated, not
picked:** at 110/125 the orb's specular breaks into the glyph runs and the segmenter returns 12
runs where the string has 11; at 155+ the strokes thin and `8` splits. 140 returns the correct run
count on 5/5 hand-checked frames spanning the brightest and darkest orb fills
(`evidence/hpb.png`, `evidence/hp_atlas_src.png`).

Glyph atlas: 11 classes (`0`–`9`, `/`), built by segmenting 14 hand-read frames across both sittings.
Per-glyph prototype counts `{/ :14, 0:33, 1:18, 2:13, 3:13, 4:4, 5:20, 6:9, 7:4, 8:7, 9:18}`.

| trace | window | frames | parsed |
|:--|:--|---:|---:|
| s2 full band | 682.10 → 943.90 | 15,708 | **15,505 (98.71 %)** |
| s2 wave 153 (calibration) | 714.83 → 729.65 | 889 | **889 (100.00 %)** |
| s1 death clip | orig 2225.0 → 2270.0 | 2,700 | 2,538 (94.00 %) — the deficit is the **post-death dark HUD**, not the live window |

### 1.2 The failure mode, and the two one-sided guards

The OCR fails in exactly **one** direction: two glyph strokes touch at threshold and segment as one,
so the read **loses a digit** (`11418/15939` → `1140/15939`). It never gains one — single-column
specular runs are filtered upstream. Both guards in `eor_hpevents.py` are therefore one-sided, and
**neither can invent a damage event out of a clean frame**:

- **G1** `max` must equal the modal max of its own ±150-frame window. Genuine max steps are sustained
  and become the window mode themselves, so they survive; one-frame disagreements are faults.
- **G2** the digit-count of `cur` must not be a strict minority (< 25 %) of its own ±15-frame window.
  A merge shortens `cur`; a real 10000→9999 crossing is sustained and never a minority.

**Declared limit of G2, because it bit exactly once and it matters:** at a *genuine* collapse from
5 digits to 4 to 3 inside 5 frames — which is what a death looks like — G2 rejects the true
intermediate reads. Both death sequences in § 4 are therefore taken from a **frame-by-frame eye-read
of magnified crops**, not from the guarded event stream, and the guarded stream's collapsed
single-event version of each death is named as such wherever it appears.

### 1.3 Event definitions (falsifiable, stated)

- **DAMAGE** = `cur[k] < cur[k−1]` on consecutive surviving frames with equal `max`. Magnitude =
  the difference. **Simultaneous hits inside one frame are indistinguishable and count as ONE event.
  Every event count below is a FLOOR on hit count, never a ceiling.**
- **HEAL** = `cur[k] > cur[k−1]`. Warlord regen (steady ~1–2 HP/frame ≈ 60–120 HP/s), ADCtH leech
  spikes, and potions are **not** separated. Reported, not interpreted.
- **MAXSHIFT** = `max[k] ≠ max[k−1]`.

### 1.4 Capture integrity — measured, because frame-exact claims depend on it

Exact-duplicate-frame rate (mean |Δ| < 0.02 on a 1/3-subsampled luma of the play area):

| window | duplicates | effective render rate |
|:--|---:|---:|
| s2 799.5–808.5 (w158) | **5.2 %** | ~56.9 fps |
| s2 860–866 (w160, to death) | **0.3 %** | ~59.8 fps |
| s1 2245–2253 (w93, to death) | **0.0 %** | 60.0 fps |

So the timing floor is **16.7 ms**, with a ≤ 5.2 % duplicate hazard declared in the s2 mid-band. In
the two death windows — the load-bearing ones — the duplicate rate is ≤ 0.3 % and the floor is clean.

---

## 2. THE PLAYER IS NOT A CONSTANT — max-health steps, MEASURED

`max` is piecewise constant and it **steps four times inside the s2 band**, plus once at each death.
This is a first-order confound on every survivability read anyone takes off this fixture, and it was
not in the record.

| sitting | t (s) | max: from → to | Δ | as ratio | duration of the low state |
|:--|---:|:--|---:|---:|---:|
| s2 | **713.383** | 20,005 → **16,368** | −3,637 | 0.8182 | **8.284 s** |
| s2 | 721.667 | 16,368 → 20,005 | +3,637 | — | — |
| s2 | **864.833** | 20,005 → **18,065** | −1,940 | 0.9030 | at death — persists |
| s2 | 873.500 | 18,065 → 20,005 | +1,940 | — | (post-death frozen HUD; do not use) |
| s1 | **2250.9667** | 15,939 → **14,239** | −1,700 | 0.8933 | at death — persists |

**What is MEASURED:** the values, the frames, the durations. Eye-verified at ×5
(`evidence/hpb.png` shows `16368/16368` at 715.0 and `14680/16368` at 720.0 in Matt's own footage).

**What is UNRESOLVED:** the mechanism. Three observations constrain it and none closes it:

1. `20005 / 16368 = 1.2222` — a clean **+22.2 %**, i.e. 16,368 reads as an *unbuffed* base and 20,005
   as the buffed value. `18065 / 16368 = 1.1037`. Two stacking sources of ≈ +10.4 % and ≈ +10.7 %
   would produce exactly this triple.
2. Recovery is **instantaneous** (one frame) and the two magnitudes are unequal — that is the shape
   of a *player-side buff lapsing and being re-applied*, not of a monster debuff wearing off.
3. It is **not the Vanguard Banner**: my own 2026-08-07 § 1 read the purchase dialogue verbatim —
   *"Vanguard Banners grant nearby players bonus **offensive** stats."* And s1 had **zero** defenses
   (tribute pinned at 150 across the entire 1→93 ramp) yet shows the same step at its death.

**Routed to legolas's half of this lap:** which Edition-III record grants the level-100 Warlord a
+22.2 % health envelope in two stacking parts, and what drops it for 8.3 s mid-fight.

### 2.1 CORRECTION to my own record — the 16,368 "green-bar body"

My fifth extraction (`…-kc2-fifth-extraction-w153-identity.md` § 0) graded a wave-153 in-world
fingerprint of **16,368** as *"NOT A MONSTER — green bar on 92 of 93 frames, player-side, no
nameplate on any of its 93 on-camera frames."* The direction was right. The identity is now pinned:
**16,368 is the player's own max health during the [713.383, 721.667] reduced window**, which overlaps
wave 153's first 6.84 s. Green bar = player-side, no nameplate = it is the player's own overhead
readout. Not a summon, not a pet: **the player.** The exclusion from the w153 body census stands and
is now reasoned rather than merely observed.

---

## 3. THE INCOMING ENVELOPE — per wave, at frame resolution

s2, player max 20,005. `hits ≥ 1 %` counts damage events of ≥ 200 HP; the sub-1 % events are a
continuous DoT/aura floor and are excluded from the rate column but included in the sums.
**Wave 160's span is corrected to 838.87 → 864.82 per § 4.2.**

| wave | span (s) | hits ≥1 % | hits/s | total dmg | DPS | **% maxHP/s** | p50 | p90 | p99 | peak | peak % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | 16.28 | 22 | 1.35 | 31,371 | 1,927 | 9.63 | 56 | 971 | 9,483 | 16,209 | 81.0 |
| 152 | 16.45 | 6 | 0.36 | 12,477 | 759 | 3.79 | 17 | 124 | 1,542 | 2,795 | 14.0 |
| 153 | 14.79 | 14 | 0.95 | 20,736 | 1,402 | 7.01 | 40 | 1,279 | 2,281 | 2,378 | 11.9 |
| 154 | 14.13 | 17 | 1.20 | 37,780 | 2,674 | 13.37 | 50 | 113 | 3,252 | 4,359 | 21.8 |
| 155 | 16.33 | 10 | 0.61 | 16,517 | 1,012 | 5.06 | 20 | 76 | 1,432 | 2,684 | 13.4 |
| 156 | 20.22 | 26 | 1.29 | 33,428 | 1,653 | 8.26 | 31 | 215 | 2,495 | 3,370 | 16.8 |
| 157 | 19.13 | 49 | 2.56 | 41,190 | 2,153 | 10.76 | 37 | 706 | 1,728 | 2,195 | 11.0 |
| 158 | 13.19 | 8 | 0.61 | 3,750 | 284 | **1.42** | 324 | 679 | 679 | 679 | 3.4 |
| 159 | 26.25 | 37 | 1.41 | 60,822 | 2,317 | 11.58 | 59 | 1,414 | 3,354 | 3,830 | 19.1 |
| **160** | **25.95** | 36 | 1.39 | 115,680 | **4,458** | **22.28** | 61 | 595 | 5,721 | **17,887** | **89.4** |

s1, player max 15,939, no defenses purchased:

| window | span (s) | hits ≥1 % | hits/s | total | DPS | % maxHP/s | peak | peak % |
|:--|---:|---:|---:|---:|---:|---:|---:|---:|
| w92 tail (2225→2243.22) | 18.22 | 18 | 0.99 | 34,345 | 1,885 | 11.83 | 3,798 | 23.8 |
| **w93 (2243.22→2250.95)** | 7.74 | 9 | 1.16 | 20,338 | 2,628 | **16.49** | 6,083 | **38.2** |

### 3.1 Four things this table shows

1. **Wave-to-wave threat variance is enormous and it is not monotone in wave number.** Wave 158
   delivered **1.42 % maxHP/s**; wave 160 delivered **22.28 %** — a **15.7×** spread inside ten
   consecutive waves of the same fixture. A Godot reproduction that emits a smooth difficulty ramp
   across 151→160 will not feel like this footage. The composition, not the index, sets the threat.
2. **Threat is spike-shaped, not throughput-shaped.** Median event 17–324 HP; p99 1.4 k–9.5 k; peak
   up to 89.4 % of the bar. The ratio p99/p50 runs **26× to 168×**. This is the single most
   transferable statement in the lap: **the fixture kills with tail events, and the tail is where
   the whole design pressure lives.**
3. **Pooled inter-arrival of hits ≥ 1 % maxHP across the whole band: median 350 ms** (p10 67 ms,
   p90 1,247 ms, n = 225). That is a *board* cadence, not a per-monster cadence — see § 5.
4. **Repeated identical magnitudes betray single recurring sources.** Wave 160 carries
   `1,113 / 1,114 / 1,114` at +0.48 / +1.75 / +2.08 s and `1,243 / 1,243` at +2.56 / +2.61 s; s1
   wave 93 carries `1,046 / 1,045 / 1,094` at 116 ms and 83 ms spacing. **These are the only
   per-source cadence signatures the substrate offers**, and they are unattributed (§ 5).

---

## 4. THE DEATH FORENSICS

The commission names s1's as "the fixture's ONE death". **The substrate contains two**, and the
second one was mis-timed in my own record. Both are reconstructed here.

### 4.1 s1 — wave 93, death at t = 2250.9500

Frame-by-frame, **eye-read at ×4 from magnified crops of each frame's own HUD**
(`evidence/death_s1_hp.png` — 22 tiles, every frame from 2250.3333 to 2250.9833 labelled with its
own timestamp). Not taken from the guarded event stream.

| frame | orig t (s) | HP read | Δ | Δ as % max |
|---:|---:|:--|---:|---:|
| 1520 | 2250.3333 | 6487/15939 | — | — |
| 1544 | 2250.7333 | 6677/15939 | regen | — |
| 1545 | **2250.7500** | **5685**/15939 | **−992** | −6.2 % |
| 1546 | **2250.7667** | **879**/15939 | **−4,806** | **−30.2 %** |
| 1547 | 2250.7833 | 840/15939 | −39 | −0.2 % |
| 1548–1553 | 2250.80–2250.8833 | 841 → 847 | regen +1/frame | — |
| 1554 | 2250.9000 | 808/15939 | **−39** | −0.2 % |
| 1555–1556 | 2250.9167–2250.9333 | 809 → 810 | regen | — |
| 1557 | **2250.9500** | **0**/15939 | **−810** | −5.1 % |
| 1558 | 2250.9667 | 0/**14239** | max steps (§ 2) | — |

**Sequence in words.** The player is at 6,677 with 200 ms to live. A 992 lands. **16.7 ms later a
4,806 lands** — 30.2 % of the bar in one frame — leaving 879. Then a 200 ms lull in which regen
gives back 7 HP and a **39-HP tick** fires twice at exactly 116.7 ms apart (a DoT, not a swing).
Then 810 removes the remainder.

**The wave-93 approach, the part that actually killed him.** Wave 93 opened at 2243.22. The player
was at **full 15,939 at 2245.60** and dead at 2250.95 — **5.35 s from full health to zero.** The
whole run to zero is nine hits ≥ 1 % of max:

| t (s) | +wave (s) | amount | % max | HP after |
|---:|---:|---:|---:|---:|
| 2248.0000 | +4.78 | 1,046 | 6.6 | 14,893 |
| 2248.1167 | +4.90 | 1,045 | 6.6 | 14,566 |
| 2248.2000 | +4.98 | 1,094 | 6.9 | 13,479 |
| 2248.3167 | +5.10 | **4,204** | **26.4** | 9,454 |
| 2248.6667 | +5.45 | 548 | 3.4 | 8,939 |
| 2248.7333 | +5.51 | 460 | 2.9 | 8,484 |
| 2250.1333 | +6.91 | **6,083** | **38.2** | 6,212 |
| 2250.7500 | +7.53 | 992 | 6.2 | 5,685 |
| 2250.7667 | +7.55 | **4,806** | **30.2** | 879 |

Between the 8,484 trough and the 6,083 hit the player **healed 3,821 in 1.13 s** (2248.07 → 2245.60
window shows the same shape: +65 HP/frame ≈ 3,900 HP/s, a potion) — and it bought him 2.4 s.
**Three hits of ≥ 26 % of max inside 2.44 s is what the sustain could not answer.**

**Roster at the moment of death — read off the hovered nameplates, glyph-colour-measured per the
R-L50-2 rule (rank is the glyph colour, never the name shape):**

| t (s) | name | level | family | measured G/R | rank |
|---:|:--|---:|:--|---:|:--|
| 2250.0500 | **Haunted Noble** | **103** | Undead | **0.929** | yellow → **champion** (band 0.91–0.95) |
| 2250.7000 | **Chillpincer** | **108** | Beast | **0.752** | orange → **hero** (band 0.71–0.79) |

Evidence: `evidence/death_s1_plate2.png` (×4, both plates, level numeral and family line legible).
**Both names are new to the project's record** — neither appears in the s2 roster table of my fourth
extraction. `Chillpincer` at **level 108** is at the corpus ceiling established in
`…-kc2-crabling-rotmouth-touch.md` § 2.3, in a **wave-93** cohort.

**What the plate does NOT establish** (my own § 8.3 correction, carried): the plate reports whatever
the *cursor* is over — which in an ARPG is what the player is *attacking*. **Neither name is
graded as the killer.** They are graded **PRESENT-AT-DEATH, MEASURED-FRAME**.

**Body count in contact at death.** In-world HP readouts inside a ~4.4 m ground disc centred on the
GAL-CAM player anchor: **1–3 across 2250.0→2250.6, then 0 at 2250.70–2250.80 — the two killing
frames.** Floor only: the blob detector merges readouts that overlap and rejects runs wider than
300 px, so this undercounts. Taken as an indicator, not a census: **at the frames that killed him,
no hostile readout was rendered inside the contact disc**, which is consistent with the killing
damage arriving from **outside melee contact**. Graded **INDICATOR, not MEASURED.**

**Correction to the wave-93 end timestamp.** My 2026-08-07 table records wave 93 ending at
**2253.63 (death)**. That is the **HUD-fade onset**. **HP reached zero at 2250.9500** — 2.68 s
earlier. The clear-time statistics are unaffected (wave 93 was already excluded as "not a clear"),
but any survival-duration or time-to-kill claim built on 2253.63 is long by 2.68 s.

### 4.2 s2 — wave 160, death at t = 864.8167 — **a NEW finding, and a correction**

**My 2026-08-07 record says: "Death at t = 943.60 (HUD fade onset; overlay frozen from 943.85)."
That is wrong.** The 943.60 event is the **ESC menu** opening over an already-frozen post-death HUD
(`evidence/d946z.png` — the panel reads *Return to Game / Options Menu / Exit to Main Menu / Quit to
Desktop*, cursor on *Options Menu*). The death is 78.8 s earlier.

Frame-by-frame, **eye-read at ×5** (`evidence/death_s2_hp.png` — 10 tiles, f10956→f10965, each
labelled with its own absolute timestamp):

| frame | t (s) | HP read | Δ | Δ as % max |
|---:|---:|:--|---:|---:|
| 10956–10958 | 864.7000–864.7333 | 20,005/20,005 | — | **FULL HEALTH** |
| 10959 | **864.7500** | **2,118**/20,005 | **−17,887** | **−89.4 %** |
| 10960 | 864.7667 | 2,222/20,005 | +104 (leech/regen) | — |
| 10961 | **864.7833** | **703**/20,005 | **−1,519** | −7.6 % |
| 10962 | 864.8000 | 703/20,005 | 0 | — |
| 10963 | **864.8167** | **0**/20,005 | **−703** | −3.5 % |
| 10964–10965 | 864.8333–864.8500 | 0/**18065** | max steps (§ 2) | — |

> **Time-to-kill from 100 % health: 4 frames. 66.7 ms.**
> **The opening blow alone was 89.4 % of the bar, delivered in ≤ 16.7 ms.**

*(The guarded event stream reports this as a single 20,005 event at 864.8167 with `gap_f = 5` —
that is G2 rejecting the genuine 4- and 3-digit intermediates per § 1.2. The eye-read above governs.)*

**Corroboration that this is the death and 943.60 is not** (`evidence/badge_post.png`, twelve badge
crops 860 → 943.5):
- The three player buff icons visible at t = 860 and t = 864 are **gone by t = 880** — buffs drop on death.
- The hourglass field reads 01:26 → 01:22 → 01:33 (refreshed) and then **00:00 from t = 880 through 943.5**.
- The wave badge **holds at 160** for the entire 78.8 s, and the arena is empty of monsters from ~875 on.
- The HUD numerals hold `0/18065` with an *identical* classifier margin (6.1) frame after frame — a
  frozen overlay, not a live readout.

**Therefore wave 160 spans 838.87 → 864.82 = 25.95 s, not 104.73 s.** The s2 sitting is a
**150 → 160 attempt that ended in death on wave 160 after 25.95 s of it**, not a 104 s grind.

**The 25.95 s that led there** (events ≥ 200 HP; full list in `evidence/ev_s2band.json`):

| t (s) | +wave | amount | % max | note |
|---:|---:|---:|---:|:--|
| 839.35 / 840.62 / 840.95 | +0.48 / +1.75 / +2.08 | 1,113 / 1,114 / 1,114 | 5.6 each | **identical magnitudes — one recurring source** |
| 841.43 / 841.48 | +2.56 / +2.61 | 1,243 / 1,243 | 6.2 each | identical pair, **50 ms apart** |
| **843.40** | +4.53 | **12,515** | **62.6** | one frame |
| 847.617 / 847.650 / 847.667 | +8.75 / +8.78 / +8.80 | 4,016 / 4,088 / 5,464 | 20.1 / 20.4 / 27.3 | **13,568 across three consecutive frames — 50 ms** |
| **850.583** | +11.71 | **8,032** | **40.2** | one frame |
| 855.70 → 859.33 | +16.8 → +20.5 | 2,222 / 2,807 / 3,740 / 1,944 / 2,947 / 2,386 / 2,221 / 3,035 | 9.7–18.7 | sustained band |
| **864.750** | **+25.88** | **17,887** | **89.4** | **the kill** |

**Read plainly: this fixture put the player from full health to dead four times over inside 26 s,
and he survived the first three only because his sustain out-healed everything below ~63 % of the
bar.** The fourth was 89.4 % and there was nothing to out-heal it with.

**Scene at the kill.** `evidence/s2_kill_wide.png` (15 tiles, 862.6 → 864.75, 150 ms spacing) and
`evidence/s2_kill_zoom.png` (14 tiles, 864.10 → 864.75, 50 ms spacing) show a **large expanding red
ground ring** that recurs at roughly 0.45–0.5 s intervals through the whole approach, and a
screen-filling white/cyan burst on the killing frames. **The ring is NOT graded as a telegraph**,
because it is not attributed: s2 carries a player-owned **Inferno Beacon** whose description Matt's
own purchase dialogue gives as *"frequently release bursts of flame at nearby enemies in a large
area"* — a site-anchored friendly effect with exactly this signature. **The discriminating test is
named and not run: a site-anchored effect is world-fixed, so with camera-pan compensation
(`eor_campan.py`, § 5.3) the ring centre is stationary in world coordinates if it is the beacon and
mobile if it is a monster ability.** One camera-compensated pass over 858–865 closes it.

---

## 5. THE BOUNDARY — why the six timing axes are NOT-OBSERVED, measured rather than asserted

The commission's provenance discipline requires that a family which never landed a visible attack on
camera be declared NOT-OBSERVED and never interpolated. **Every family here is NOT-OBSERVED on every
timing axis.** The reason is worth stating precisely, because it is the finding.

### 5.1 It is not occlusion

Fraction of a ~4.4 m ground disc centred on the player that is bright, saturated emissive VFX:

| window | median | p90 | frames > 30 % |
|:--|---:|---:|---:|
| s1 wave 1 (800–810) | 2.4 % | 48.1 % | 28.3 % |
| s1 wave 93 (2243.5–2251.5) | 5.5 % | 12.0 % | 0.0 % |
| s2 wave 153 | 10.4 % | 18.2 % | 0.0 % |
| s2 wave 158 | 13.9 % | 27.6 % | 7.4 % |
| s2 wave 160 (to death) | 19.7 % | 31.4 % | 13.2 % |

**Bodies are visible most of the time.** My first anecdotal crop suggested otherwise
(`evidence/ee_z.png` — a body entirely inside a green player-AoE plume) and the systematic
measurement corrected me. Occlusion costs frames; it does not close the axis.

### 5.2 It is attribution

The substrate offers exactly two identity instruments and they are mutually exclusive in practice:

| instrument | what it gives | when it fires |
|:--|:--|:--|
| **hovered nameplate** | name + level + family + rank | only while the cursor rests on the body — 22 plates across five wave-start windows in my fourth extraction; the 5 Hz scan that found them **missed 5 of 11 w153 hovers and 9 of 13 w157 hovers** |
| **player HP clock** | the exact frame a hit lands | always — but it is **source-blind**; 10–27 bodies are on the board and simultaneous hits inside one frame are one event |

To time *a family's* wind-up you need the same body named **and** its hit instant isolated **and**
its sprite pose legible across ~40 consecutive frames, with no other hostile contributing to the
player's HP in that span. **In waves of 12–28 simultaneous bodies with a Warlord standing inside the
pile, that conjunction does not occur.** `evidence/s1_kill_native.png` (six native-resolution crops
of the 520×390 px contact zone across the s1 killing second) is the plain demonstration: twelve or
more stacked in-world readouts and the player's own melee flashes blanket the bodies at exactly the
frames that matter.

### 5.3 What would cross the boundary — the cheapest refuting test, per axis

Named so this note is a specification and not a shrug. Each requires **new capture**, not new
analysis of the frozen substrate:

| axis | cheapest test that closes it |
|:--|:--|
| wind-up, recovery, telegraph shape/duration | a **single-monster capture**: one family, no player attacks, camera static, 60 fps, ~20 s. Grim Dawn's own devotion/faction farming areas supply this trivially; Crucible never will |
| attack cadence per family | same capture; count contact events on the HP clock with exactly one hostile alive |
| root-lock fraction | same capture + `eor_campan.py` pan compensation; the readout anchor then gives world-frame translation directly |
| approach speed at contact | same capture; a body closing from ~15 m with the camera static |
| **all six, without new capture** | the **`.arz`/`.anm` join — legolas's half of this lap.** The WR3 precedent extracted Primordian's 0.489 s / 0.879 s / 0.80 s **from source, not from footage.** That is the right instrument for these axes and this note's boundary is the argument for it |

**This is the load-bearing recommendation of the lap: the timing grammar is a DB/animation fact, not
a footage fact. The footage's unique contribution is the RECEIVING end — §§ 3 and 4 — and that is
where its evidence should be spent.**

### 5.4 The pan instrument, built and validated, parked

`eor_campan.py` measures per-frame camera translation by weighted-SAD registration on the achromatic
luma of the play band, with saturation-weighted suppression of the VFX layer. Validated over
s2 799.43–803.43: 240 frames, **31.0 % camera-static**, residual median 5.72 / p95 8.55, longest
static run 19 frames. It works and it is committed. **It is not used for any number in this note**,
because without family attribution a compensated velocity is a velocity of *something*. Parked
against the single-monster capture in § 5.3, where it becomes the primary instrument.

`eor_kinematics.py` (readout-anchor tracking) is likewise committed and likewise **not used for any
graded number**: on the w158 window it returned 116 tracks whose median step-speed was 0 px/s while
p90 exceeded 700 px/s — the signature of an anchor that fragments and re-associates, not of a body
that moves. **Named as a failed instrument rather than quietly dropped.** Its two defects are known:
the readout's x-centre shifts when the value's digit count changes, and un-compensated camera pan
enters every screen displacement.

---

## 6. THE PER-FAMILY THREAT-GRAMMAR TABLE — the fold target, with grades

Roster as named on camera, from my fourth extraction § 5 (s2 band) + the fifth extraction (w153
bindings) + **two names new in this pass** (s1 w93). Grades are per the commission's vocabulary:
**MEASURED-FRAME** / **ESTIMATED** / **NOT-OBSERVED**.

**Every timing cell below is NOT-OBSERVED for the reason in § 5.2. No cell is interpolated.**

### 6.1 By family — s2 band waves 151–160 (priority per commission)

| family | named bodies in band | wind-up | recovery | telegraph | cadence | root-lock | approach speed |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **Undead** | Wraith · Ancient Wraith · Spiteful Wraith · Tildoom ~ Timewarped · Arcanom the Soulthief · Storm Revenant · Frost Revenant · Skeletal Archer · Culldar Endbringer ~ Celestial | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Beast** | Mudflinger ~ Reflective · Ugdenbog Crabling · Chaosshell ~ Voidtouched · Chillslither ~ Arctic · Stonegaze Basilisk · Juvenile Basilisk · Venomgaze Basilisk · Diremane Brute · Starhorn ~ Celestial · Ugdenbog Spikeshell · Ugdenbog Crab · Sandclaw ~ Matriarch · Sandclaw | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Undead · Beast** | Wendigo · Wendigo ~ Ancient | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Plant · Eldritch** | Carnivorous Plant · Ugdenbog Golem · Ferrosius ~ Swift | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Chthonic (· Insectoid)** | Chthonian Devourer · Chthonian Bloodkeeper · Chthonian Unraveler | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Aetherial** | **Fleshweaver Haraxis** (BOSS, L108, w152) | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |
| **Aether Corruption** | **Blugrug the Living Plague** (BOSS, L108, w157) | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS | NOT-OBS |

### 6.2 By family — s1 (second priority per commission)

| family | named bodies | all six axes |
|:--|:--|:--|
| **Undead** | **Haunted Noble** (L103, champion, G/R 0.929) — w93, PRESENT-AT-DEATH | NOT-OBSERVED |
| **Beast** | **Chillpincer** (L108, hero, G/R 0.752) — w93, PRESENT-AT-DEATH | NOT-OBSERVED |

### 6.3 What DOES fold to drax's Godot runtime, and its grade

The table above is a declaration. **This is the payload.** All rows MEASURED-FRAME unless marked.

| row | value | grade |
|:--|:--|:--|
| incoming DPS as % player maxHP/s, per wave 151–160 | § 3 table — **1.42 % (w158) → 22.28 % (w160)**, 15.7× spread | MEASURED-FRAME |
| per-hit magnitude distribution | p50 17–324 HP · p99 1.4 k–9.5 k · **p99/p50 = 26×–168×** | MEASURED-FRAME |
| board-level hit inter-arrival, hits ≥ 1 % maxHP | **median 350 ms** (p10 67, p90 1,247; n = 225) | MEASURED-FRAME (board, **not per-monster**) |
| largest single-frame hit observed | **17,887 = 89.4 % of maxHP in ≤ 16.7 ms** (s2 864.750) | MEASURED-FRAME, eye-verified |
| second/third largest | 12,515 (62.6 %, s2 843.400) · 8,032 (40.2 %, s2 850.583) | MEASURED-FRAME |
| burst structure | **13,568 across 3 consecutive frames = 50 ms** (s2 847.617–847.667) | MEASURED-FRAME |
| time-to-kill from 100 % health | **s2: 66.7 ms (4 frames)** · **s1: 5.35 s from last full-health frame** | MEASURED-FRAME, eye-verified |
| DoT floor | continuous sub-1 % events; s1 w93 shows a **39-HP tick at 116.7 ms spacing** | MEASURED-FRAME |
| recurring same-magnitude sources | `1,113/1,114/1,114`, `1,243/1,243` (s2 w160); `1,046/1,045/1,094` (s1 w93) | MEASURED-FRAME (magnitude + interval); **source UNATTRIBUTED** |
| player sustain envelope | regen ~60–120 HP/s baseline; potion burst **≈ 3,900 HP/s for ~1.13 s (≈ 4,460 total)** | MEASURED-FRAME |
| player max-health is **not constant** | four steps in-band; −18.16 % for 8.284 s, −9.70 % at death | MEASURED-FRAME; **mechanism UNRESOLVED** |
| wave 160 true span | **838.87 → 864.82 = 25.95 s** (was 104.73 s) | MEASURED-FRAME — **correction** |
| wave 93 true death instant | **2250.9500** (was 2253.63) | MEASURED-FRAME — **correction** |

**How drax should read this.** The baton's Rider-1 declaration says the baton "does NOT underwrite
live threat resolution: monster attack-TIMING grammar … is NAMED-ABSENT-DECLARED, arriving via the
threat-grammar companion lap." **This note does not lift that declaration for the timing axes.** It
converts the absence from *unspecified* to *specified*: the six axes are NOT-OBSERVED, the reason is
attribution, the crossing test is named (§ 5.3), and the correct instrument is legolas's `.arz`/`.anm`
join. What it *adds* to the Godot runtime is the **acceptance envelope** — the shape of incoming
damage the reproduction must be able to produce. Reproduce §§ 3 and 6.3 and the arena feels like this
footage even before the per-family timings land. Miss the 89.4 %-in-one-frame tail and it never will,
whatever the wind-ups turn out to be.

---

## 7. CORRECTIONS TO MY OWN COMMITTED RECORD

1. **`…-eor-sittings-extraction.md` § 2.2 — s2 death timestamp.** Recorded as **943.60**. Measured
   here at **864.8167** (HP zero), eye-verified across 10 consecutive frames. **943.60 is the ESC
   menu.** Wave 160's span becomes **25.95 s**, not 104.73 s. The n = 9 cleared-wave statistics for
   s2 are unaffected (wave 160 was already excluded as "not a clear").
2. **`…-eor-sittings-extraction.md` § 2.3 — s1 wave-93 death timestamp.** Recorded as **2253.63**.
   That is the HUD-fade onset; **HP reached zero at 2250.9500**, 2.68 s earlier. Clear-time
   statistics unaffected; survival-duration claims are long by 2.68 s.
3. **`…-kc2-fifth-extraction-w153-identity.md` § 0 — the 16,368 fingerprint.** Graded "NOT A
   MONSTER — player-side". Correct in direction; identity now pinned: **it is the player's own
   overhead readout during the [713.383, 721.667] reduced-max-health window** (§ 2.1). Its exclusion
   from the w153 body census stands and is now reasoned.

---

## 8. LIMITS, HAZARDS, AND WHAT WAS DELIBERATELY NOT DONE

- **Attribution.** No damage event in this note is attributed to a named monster. Not one. §§ 4.1/4.2
  name bodies as **PRESENT-AT-DEATH**, never as killers.
- **Simultaneity.** Every damage-event count is a **floor**: hits landing inside one 16.7 ms frame
  are one event.
- **Duplicate frames.** ≤ 5.2 % in the s2 mid-band (§ 1.4). In both death windows ≤ 0.3 %.
- **G2 rejection at deaths.** Named in § 1.2; both death sequences bypass the guard by eye-read.
- **Contact-disc body counts (§ 4.1)** are floors: the blob detector merges overlapping readouts and
  rejects runs > 300 px. Graded INDICATOR.
- **GAL-CAM scale transfer.** The player anchor (962, 595) and the scale field
  `g_x(y) = 0.021404·(y+1950)` come from `…-gal-cam-fixture-camera.md`, measured on
  `play_test_2026-07-26.mp4`. **Applying them to the eor sittings is an unverified transfer
  assumption**, carried explicitly in `eor_kinematics.py`. It is used only for the ~4.4 m disc radius
  in § 4.1/§ 5.1 — both of which are graded INDICATOR — and for **no** graded number.
- **The red ring at the s2 kill** is NOT graded as a telegraph; the discriminating test is named
  (§ 4.2) and not run.
- **Max-health mechanism** is UNRESOLVED and routed to legolas, not guessed.
- **Not done, and deliberately:** no wind-up/recovery number was estimated by analogy to the WR3
  Primordian figures. The commission forbids interpolation and the temptation was real — Primordian's
  0.489/0.879 sits right there and would have filled the § 6 table. **An interpolated table is worse
  than an empty one, because a Godot runtime cannot tell them apart.**
- **No sub-agent was invoked** (galadriel HARD NO, role definition § "No sub-agent invocation").
- **Read-only** against all substrate and all other agents' trees. **Committed, not pushed.**

---

## 9. Mirror voice

The Mirror was pointed at the monsters and it showed me the man.

Every instrument I built to ask *what does the thing do before it strikes* came back pointing the
other way — because in a Crucible wave at 160 there is no *the thing*. There are twenty-seven of
them, and they arrive as weather. The footage cannot tell you which one swung, and it was never
going to; that answer lives in a `.dbr`, in a keyframe named `RightHandHit`, in the place legolas is
already looking.

But the same footage, asked the question it *can* answer, is unsparing. It says: at 864.7333 he was
whole, and at 864.8167 he was not, and the distance between those two facts is four frames. It says
the bar came off in one stroke — eighty-nine percent of a man, in less time than it takes to blink —
and that three times before that stroke the arena had already tried the same thing and only his
potion had argued. It says wave 158 was nothing and wave 160 was everything and they are two waves
apart.

That is the grammar. Not the wind-up — **the tail.** This fixture does not grind a player down; it
waits, and then it removes him. Build the wind-ups from the database when they come. But build the
tail first, because the tail is what the death was made of, and a reproduction that is merely
*dangerous on average* will be, at the exact moment it matters, a different game.

---

**Signed:** galadriel · visual perception + benchmark seam
**For:** the Rider-2 companion lap. Parallel to KC2-SIM; reports into the Godot playtest milestone.
The durable note is the artifact of record.
