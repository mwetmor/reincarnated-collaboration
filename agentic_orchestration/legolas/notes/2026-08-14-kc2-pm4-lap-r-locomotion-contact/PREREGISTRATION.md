# LAP R — PRE-REGISTRATION (written and hashed BEFORE any instrument ran on the full video)

**Run:** KC2-PM4 · **Lap:** R (locomotion-and-contact decode) · **Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf (RUN-CONDUCTOR) · **Fired under:** R-PM4-42 part 3 · **Date:** 2026-08-14
**Discipline:** GL-12 decode-never-estimate · outcome-firewalled · FULL 64-hex digests

This file exists so that every threshold this lap uses is on the record before the numbers are.
Nothing below was chosen after seeing a result.

---

## 0. Outcome firewall — declared

The sim's `dry_fraction_whole_run = 0.4118` and `final-200 = 0.33` are named in the commission and are
therefore known to this observer. **They enter NO instrument.** No threshold below was selected to
bring a referent number near them; the sweep is a fixed geometric-ish ladder chosen for readability.
The comparison is reported side-by-side WITHOUT adjustment of either side, per commission.

---

## 1. LIMB A — FCT gap analysis

### A.0 What the FCT stream can and cannot proxy (declared before measuring)

An FCT (floating combat text) damage number proves **damage LANDED** at that instant. Therefore:

* An FCT **gap** = an interval in which **no player-outgoing damage landed**.
* A gap **does NOT** distinguish: (i) no body in reach, (ii) body in reach but the player was not
  attacking (relocating, casting a non-damaging skill, dead-time between channel ticks), (iii) attacks
  that MISSED, (iv) damage that landed but whose FCT was occluded / OCR-dropped.
* The sim's `dry_fraction` is defined as *no body in the kill disc*. The FCT proxy is a **strict
  superset** of that condition: every truly-dry tick is FCT-dry, but not every FCT-dry tick is truly
  dry. **The FCT dry fraction is therefore an UPPER BOUND on the referent's true dry fraction.**
  This direction is stated now, before the numbers, and it is one-directional.

### A.1 Player-outgoing predicate `P-OUT` (pre-registered, applied unchanged)

An OCR text observation qualifies as a player-outgoing damage FCT event iff **all** hold:

1. `cls ∈ {crit, crit_garbled}` **OR** (`cls == bare` **AND** `colour_class == cream_dealt`);
2. it is not classified `hud`, `health_readout`, or `other` (Lap N's classifier, imported unchanged
   from `method/build.py`, sha256 `1d8032185626bd74ca7458b60f837b7beb106527a19cea3194387a71691bab9a`);
3. **static-element exclusion:** the (rounded) bounding-box position must NOT recur in ≥ 50 % of
   sampled frames. A screen element present in half the frames at the same place cannot be floating
   combat text. Position key = `(round(bbox_x,2), round(bbox_y,2))`. Threshold **0.50**, fixed here.
4. parsed `damage ≥ 1`.

**Known, declared attribution limit (carried from Lap N § A.6):** cream FCT cannot be attributed to a
source from pixels. Pet damage, devotion procs, retaliation and player direct attacks all print cream.
`P-OUT` therefore measures **"the player's side of the board landed damage"**, not "the player's own
weapon landed damage". This is stated as a limit, not corrected for.

### A.2 Sampling — two passes, both declared now

* **PASS 1 (existing bytes, fires first, zero new video work):** `pm4n_fct_events.csv`, 95 frames at
  **2.0 s** cadence over t = 680–868 s. Gap resolution floor = 2.0 s. Sub-2 s structure is **UNREACHED
  at this cadence** and will be recorded as such, not interpolated.
* **PASS 2 (dense re-sample, new):** cadence **0.5 s**, span **t = 683.0 → 866.0 s** (367 frames),
  identical `ocr.swift` binary and identical classifier. 0.5 s is chosen because it is **below** the
  measured FCT on-screen lifetime (1.2–1.5 s, Lap N), so every FCT event is sampled at least twice and
  presence/absence becomes a reliable per-instant read.

### A.3 The lifetime dilation, declared before measuring

Because an FCT number persists ~1.2–1.5 s after the hit that produced it, "text present at time *t*"
means "damage landed somewhere in [t − L, t]" with L ≈ 1.35 s. Consequently a run of consecutive dry
samples of observed length D corresponds to a **true no-damage gap of at least D + L**. Two numbers
are therefore reported for every threshold:

* `raw` — the observed presence-gap (a **LOWER BOUND** on true dry time);
* `L-corrected` — `D + 1.35 s` per gap (the **point read** under the measured lifetime).

Neither is preferred; both are published. L is taken from Lap N's measured 1.2–1.5 s band; the band
edges are carried as a sensitivity (L = 1.2 and L = 1.5).

### A.4 Threshold sweep — FIXED HERE, BEFORE RUNNING

Fraction of fight time spent inside no-damage gaps longer than:

> **0.5 s · 1.0 s · 2.0 s · 3.0 s · 5.0 s · 10.0 s**

Six rungs, declared. No rung will be added, removed, or re-cut after the numbers land. (Pass 1 can only
report rungs ≥ 2.0 s; the rest are UNREACHED at 2 s cadence and say so.)

### A.5 Wave attribution

Wave boundaries are taken from Lap H-2 `OBS-H2-6` — measured to ±0.25 s from the wave-counter digit
crop 52×26 at (1582,138): 151 ≤ 683.0 · 152 @ 698.6 · 153 @ 714.9 · 154 @ 729.8 · 155 @ 744.0 ·
156 @ 760.2 · 157 @ 780.4 · 158 @ 799.7 · 159 @ 812.7 · 160 @ 839.0. A gap is attributed to the wave
containing its **start**; gaps that straddle a boundary are flagged `straddles_wave_boundary`.

### A.6 The w154 question

Pre-registered as a **descriptive** measurement, no hypothesis to confirm: report wave 154's span,
its dry fraction, its longest gap, its gap distribution, and — from the independent Lap H-2 camera and
nameplate traces — what the player was doing and what was on the board during that longest gap. The
sim's 38.12 s / 51.2 % pet-TTL wait is NOT a target; the referent's number is whatever it is.

---

## 2. LIMB B — video locomotion

### B.1 Movement detector — pre-registered

**Primitive:** Lap H-2's whole-fight camera-translation trace
`2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy`
(sha256 `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33`, 11,024 rows × 4,
columns `[t, dx_screen_px, dy_screen_px, correlation_peak]`, 60 fps, phase correlation on terrain
gradient magnitude). **The camera is measured rigidly player-locked (Lap H-2 OBS-H2-7), so camera
translation IS player world displacement.** This is a re-use of a validated instrument, not a new one.

**Ground-pixel convention (Lap H-2 OBS-H2-8):** `speed_gpx_s = hypot(dx, dy / K) * fps`, K = 0.537.

**Smoothing:** centred rolling median, window **9 frames (0.15 s)**, applied to the per-frame speed.
Window fixed here.

**Episode segmentation — Schmitt trigger, thresholds fixed here:**

| parameter | value | rationale (a priori, not fitted) |
|---|---|---|
| `V_ON` | **200 ground px/s** | Lap H-2 already published moving-fraction at 60/200/400 gpx/s; 200 is its middle rung, adopted unchanged rather than invented |
| `V_OFF` | **100 ground px/s** | half of `V_ON` — standard hysteresis convention |
| `MIN_EPISODE` | **0.25 s** (15 frames) | shorter than the shortest bout Lap H-2 measured (0.517 s median at its tightest wave); rejects single-frame correlation noise only |
| `MIN_GAP_MERGE` | **0.15 s** (9 frames) | two episodes separated by less than the smoothing window are one episode |

**Sensitivity:** the whole episode table is re-derived at `V_ON` = 100 / 200 / 400 gpx/s and the
headline counts reported at all three. The 200 rung is the pre-registered primary.

### B.2 Detector validation — pre-registered protocol

The detector is validated **against an independent second instrument**, not against itself:

* **Instrument 2:** normalised cross-correlation (NCC) template matching of a raw-luminance terrain
  patch across a frame pair — a different registration principle (raw intensity template match vs
  FFT phase correlation on gradient magnitude) than the trace under test.
* **Protocol:** draw **20 validation instants** — 10 classified MOVING and 10 classified STATIONARY —
  by a **fixed-seed** (`seed = 154`) uniform draw over the eligible instants. At each, extract the
  frame pair (t, t + 0.25 s), run NCC on **4 terrain patches** at fixed screen positions away from
  the player, take the best-confidence patch, and compare its displacement to the trace's cumulative
  displacement over the same interval.
* **PASS criterion, fixed here:** ≥ 16 of 20 instants agree in **class** (NCC displacement over
  0.25 s ≥ 50 ground px ⇒ moving; < 50 ⇒ stationary — 50 gpx/0.25 s = 200 gpx/s, the same `V_ON`),
  **and** the median relative magnitude error on the MOVING instants ≤ 25 %.
* A FAIL is reported as a FAIL and the movement table is down-graded to INDICATIVE. It is not re-tuned.

### B.3 Movement-while-channeling — pre-registered decision rule

**Question:** does the EoR channel visibly CONTINUE while the player relocates?

Decided on **two independent observables**, both required to be reported, neither assumed:

1. **Damage-output persistence.** Inside the *N* = 12 fastest movement episodes (ranked by mean speed;
   fixed selection rule), sample frames at **10 fps** and ask whether `P-OUT` FCT is present. Report
   the per-episode fraction of moving frames carrying player-outgoing damage.
2. **Channel-VFX persistence.** The EoR channel draws a player-centred ring. Detector: mean luminance
   in the **annulus 60–110 screen px** about the player's pinned ground point (958, 544) (Lap H-2
   OBS-H2-8), relative to a control annulus at **300–350 px**. Reported as a ratio per frame.
   **NOTE-9 declared in advance: pixels cannot name WHICH skill draws a ring.** The claim ceiling is
   "a player-centred channel VFX persists", never "eyeofreckoning1 specifically persists".

**Verdict rule, fixed here:** CONTINUES iff, across the 12 episodes pooled, player-outgoing FCT is
present in **≥ 50 %** of moving-frame samples AND the ring ratio during movement is statistically
indistinguishable from (or above) its value during stationary frames. INTERRUPTED iff FCT presence
during movement is **< 20 %** of its stationary rate. Anything between = **UNDECIDED**, reported as
UNDECIDED. Frame numbers of witnessed instances are emitted either way.

### B.4 Spawn-to-first-contact latency — pre-registered

Per wave 151–160, two latencies, both reported:

* `latency_fct` = (first `P-OUT` FCT sample time at or after the wave-increment time) − (wave-increment
  time). Resolution = the dense pass's 0.5 s cadence; the FCT lifetime means this is an **UPPER BOUND**
  offset by at most L (the hit may have landed up to 1.35 s before the sample that shows it) — so
  `latency_fct − L` is the lower bound and both are printed.
* `latency_plate` = time until the first living monster nameplate falls within **150 ground px** of the
  player (Lap H-2's `R_CONTACT` = 150, calibrated by visual inspection in that lap; reported also at
  120 and 180). Source: Lap H-2 nameplate census `plates60.npy`. **Every plate count is a LOWER BOUND**
  (nameplate presence proves a living body; absence does not prove absence) — Lap H-2 NOTE-9, carried.

Wave-increment times are the Lap H-2 OBS-H2-6 values (±0.25 s), which bounds every latency at ±0.25 s
before any other error.

---

## 3. LIMB C — game-side sheet/DB terms

Read-only walk of the pinned Edition-III corpus at
`/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` using the Lap I/M/O reader stack
(`pm4i_lib_2026_08_13.E3`, `pm4m_lib_2026_08_14`, `pm4o_lib_2026_08_14`).

Terms sought, each recorded MEASURED with a record+field citation or **UNREACHED**:

1. **player movement speed** — `characterRunSpeed` / `characterRunSpeedModifier` class fields on the
   player record chain + equipped-item / skill contributions; sheet value if the referent's character
   sheet carries one (Lap A `measured-player-sheet.csv`).
2. **monster movement speed, 151–160 roster** — per-body `characterRunSpeed`-class fields from each
   rostered creature record, joined to the frozen roster roll (`BATON_20W`).
3. **EoR movement-while-channeling rule** — the skill template's own fields
   (`canUseWhileMoving` / channel-class flags / any movement-speed penalty field) on the EoR record
   chain, read from `templates.arc` + the skill record.
4. **Crucible spawn geometry** — spawn-point / arena-dimension records if any exist in the corpus.
   **Pre-declared as likely UNREACHED** (level geometry lives in `.map`/`.lvl` assets, not the `.arz`
   record DB); if unreachable it is recorded UNREACHED, never estimated.

**Law 3 restatement for this lap:** no number below is chosen, rounded, or preferred because of what it
would do to any simulation outcome. Where the corpus and the sheet disagree, Lap L's standing ruling
holds (**the sheet governs**) and both are published.

---

## 4. Emission contract

Artifacts: `pm4r_fct_gaps.csv` · `pm4r_movement_episodes.csv` · `pm4r_speed_terms.csv` ·
`pm4r_findings.md` · `pm4r_digests.json`. Instruments to
`agentic_orchestration/research/scripts/pm4r_*_2026_08_14.py`. FULL 64-hex sha256 on every input and
every output. Row counts published. Every value cites file path + record/frame.
