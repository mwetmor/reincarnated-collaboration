# KC2 LIFT RUN — galadriel footage lap: PRE-REGISTRATION

**Date:** 2026-08-25
**Author:** galadriel (visual perception + benchmark seam)
**Commissioned by:** gandalf `RUN-CONDUCTOR`, KC2 LIFT RUN charter ruling **R-L6-2** (ledger L-6)
**Bundle:** (i) **U-7** short-radius heading conditioning · (ii) **R-L5-1 / `ABS-W2-CAST-MIX`** per-slot cast census while channel is ACTIVE · (iii) **D-W1-1** metre-scale reconciliation (report-only)
**This file commits ALONE, before any statistic in its scope is computed.** D4 (prereg-before-build) applied to a measurement lap. Nothing below may be moved after data are seen; anything I want to change afterwards becomes a *named amendment with a reason*, not a silent edit.

---

## 0 · SUBSTRATE PINS (derived this session, DR-1; never retyped)

| artefact | sha256 | role |
|---|---|---|
| `~/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` | **the referent footage** — 1920×1080, 60/1 fps, 1034.100 s, 62046 frames |

Further pins (prior-lap artefacts consumed read-only) are derived and tabled in `findings.md` § 0. **No new gameplay capture is possible or attempted** — the referent is historical footage and this lap only re-reads it.

**Window of record, unchanged from every prior KC2 S2 lap:** `t ∈ [682.10, 864.75]`, 182.65 s, wave-151 badge flip → death.

---

## 1 · ITEM 1 — U-7: SHORT-RADIUS HEADING CONDITIONING

### 1.1 The question, stated so it can fail

Legolas § 4.3 established that the incumbent instrument (Lap U § 1.2 net-displacement + straightness) **cannot separate** *board-blind mill* from *short-radius target-conditioned mill* — both produce low net displacement, low straightness, high moving-fraction.

The discriminator: **does the referent's HEADING correlate with the direction toward local body density at short radius?**

### 1.2 The surface, and why this one

Both terms must live in ONE frame. The world view cannot supply that: the player is buried under wave-150+ VFX, bodies occlude, and every screen bearing needs the isometric ground map `M` that the 2026-08-24 boundary trace explicitly failed to recover.

**The HUD minimap supplies both terms in one north-up, rigidly player-centred frame** (established 2026-08-24 § 1.1): monster icons are drawn over everything and never occlude; the mapped terrain is a fixed world-space image that merely TRANSLATES, so player displacement is recoverable with **no camera model**; and bearings from the disc anchor are already player-relative.

⚑ **U-9 CONSTRAINT, BINDING:** ground-px → metres is a **DECLARED GAP** on this referent (OBS-H2-9). **Every radius in this lap is swept and reported in MINIMAP PIXELS. No metric radius is asserted anywhere, in any sentence, including the verdict.** Every statistic reported is scale-free (angles, correlations, resultant lengths).

### 1.3 Instrument definition

Sampling **10 Hz** across the window (1827 samples). Per sample:

- **Player displacement.** The minimap content that is world-static translates by **−(player step)**. TWO INDEPENDENT ESTIMATORS, both computed, neither assumed:
  - **E1 (primary)** — matched teal pedestal-gem fixtures; sub-pixel centroids; ≥3 matched pairs; the estimator reports its OWN error as the spread of pair-deltas about their mean and REFUSES a step whose spread > 1.5 px rather than averaging a disagreement.
  - **E2 (cross-check)** — masked terrain SAD registration with icons and teal masked out, parabola sub-pixel refinement, peak-sharpness recorded.
- **Player anchor `a`** — the gold arrowhead is the ONLY disc-fixed icon; located as the persistent peak of the icon mask across the window (not assumed to sit at the ring-fit centre).
- **Monster mask `M(t)`** — warm-cream star + pale-skull icon pixels within the disc, EXCLUDING teal gems, EXCLUDING a disc of radius `r_ex = 7 px` about `a` (the player's own arrow), EXCLUDING `r > 64 px`.
- **Heading θ_p(t)** — direction of player displacement over baseline **B = 0.5 s**, centred at `t`. Only samples with |Δp| ≥ **3.0 px** over B are used: *a stationary player has no heading, and inventing one is how a null becomes a result.* Sensitivity reported at B = 0.3 s and B = 1.0 s.
- **Density direction θ_c(t;R)** — direction from `a` to the **pixel-mass centroid** of `M(t)` restricted to `r ≤ R`. Pixel-mass rather than discrete-icon centroid because clustered stars merge into single blobs at wave 150+; merging destroys a discrete count but not a mass centroid. *Stated bias:* larger icons (skulls/bosses) carry more mass than small stars. Reported, not corrected.
- **Δ(t;R) = wrap(θ_p − θ_c) ∈ (−180°, 180°]**.

**Radius sweep, in PIXELS:** `R ∈ {12, 16, 20, 25, 30, 36, 44, 52, 60}` minimap px. Nine radii.

### 1.4 Statistics

- **Primary:** mean resultant length **R̄(R) = |mean e^{iΔ}|** with mean direction μ(R). R̄ = 0 ⇒ heading uniform w.r.t. the density bearing (board-blind); R̄ → 1 with μ ≈ 0° ⇒ heading toward density; μ ≈ 180° ⇒ heading away (kiting).
- **Secondary (sign-insensitive):** axial resultant **R̄₂ = |mean e^{2iΔ}|**, which detects alignment along the density AXIS whether approaching or retreating.
- **NULL — circular time-shift, NOT Rayleigh.** At 10 Hz both series are heavily autocorrelated, so the Rayleigh test is anti-conservative by a large and unknown factor. The null recomputes R̄ with the density-direction series **circularly shifted by lag L**, for every integer-second L with 2 s ≤ |L| ≤ 90 s. This preserves each series' own autocorrelation and destroys only their pairing. **p = fraction of shifts with R̄_shift ≥ R̄_obs.** The Rayleigh p is reported **DESCRIPTIVE ONLY and is explicitly excluded from the decision rule.**
- **Multiplicity:** nine radii ⇒ `p_adj = 9 · p`.
- **CI:** circular block bootstrap, block length **5 s**, 2000 resamples, percentile 95 % interval on R̄.

### 1.5 COVERAGE GATE (coverage-before-accuracy, F-5 G-0)

No verdict other than INSTRUMENT-CANNOT-REACH may be returned unless all of:

| id | gate |
|---|---|
| **G-a** | E1 and E2 agree: median \|E1−E2\| ≤ 1.5 px AND ≥ 80 % of jointly-locked intervals within 3.0 px |
| **G-b** | the displacement estimator locks on ≥ 80 % of sampled intervals |
| **G-c** | the player anchor is disc-fixed: persistent-core radius ≤ 3 px |
| **G-d** | ≥ 300 usable samples (moving AND ≥ 1 monster icon within R) at every radius quoted |
| **G-e** | **external reproduction** — minimap-derived player displacement is related to the independently-measured world-view screen pan (`s2-motion-20hz.json`, a different surface and a different algorithm) by a fixed 2×2 linear map with **R² ≥ 0.70**. Failing G-e alone does not void the lap; it downgrades the verdict to *instrument-uncorroborated* and that word appears in the verdict line. |

### 1.6 ⚑ DECISION RULE — fixed here, before computing

**Smallest interesting effect, declared now and not movable: `R̄* = 0.15`.** Rationale: R̄ = 0.15 is roughly a 4:3 excess of headings into the density hemisphere over away from it — the weakest conditioning that would still change what a Godot pilot policy has to implement. Below that, a "significant" result would be a true statement about a mechanism too weak to build.

| verdict | condition |
|---|---|
| **SUPPORTS-CONDITIONING** | coverage gate passes **AND** at **≥ 2 ADJACENT radii**: `p_adj < 0.01` **AND** `R̄ ≥ 0.15` **AND** bootstrap 95 % lower bound > 0.05 **AND** μ consistent in sign across those radii |
| **NOT-SUPPORTED** | coverage gate passes **AND** at **every** radius `p_adj > 0.05` **AND** the bootstrap 95 % **upper** bound on R̄ is **< 0.15** — i.e. an interesting effect is *excluded*, not merely undetected |
| **INSTRUMENT-CANNOT-REACH** | **every other case** — in particular whenever `p_adj > 0.05` but the R̄ upper bound exceeds 0.15 (underpowered), or the coverage gate fails |

⚑ **"The footage cannot reach this discriminator either" is a valid and valuable verdict and I will return it if that is what the picture shows.** The failure mode this rule exists to prevent is a p-value harvested from an autocorrelated series and dressed as a mechanism.

**Auxiliary reporting (NOT decision-bearing, declared so it cannot become the finding after the fact):** the Δ distribution and rose; hemisphere fraction `P(|Δ| < 90°)`; per-wave split; split by channel-active vs not; split by speed band.

---

## 2 · ITEM 2 — R-L5-1 / `ABS-W2-CAST-MIX`: PER-SLOT CAST CENSUS WHILE CHANNEL IS ACTIVE

### 2.1 The wall two seats hit independently

`0.15 = Σ_s m_s · rate_s` with three measured per-skill rates (slot L 0.385 / slot 2 0.136 / slot 3 0.000) is **one equation in three unknowns** — the missing datum is the **cast MIX**, and specifically `P(channel-active | cast)` per slot, because *a cast made while the channel is not running cannot interrupt it* and therefore does not belong in the denominator of an interrupt rate.

### 2.2 Substrate — re-query, no new capture

The committed 54-cast converse table (`s2c-attrib.json`, produced by `pipeline/eor_attrib.py`), which carries per cast: slot, cast time, the containing inter-tick silence `gap`, its opening tick `gap_t0`, and `lag_into_gap_s = t_cast − gap_t0`.

### 2.3 Definition, fixed before computing

**ACTIVE(cast) := `lag_into_gap_s` ≤ W**, i.e. the last energy drain tick preceding the cast fell within W seconds of it.

- **W = 0.35 s primary.** Justification stated in advance: the channelling drain cadence has median inter-tick 0.083 s and duration-weighted median 0.100 s; W = 0.35 s is ≈ 3.5–4× that cadence, so a genuinely-channelling cast cannot be misclassified as inactive by ordinary tick jitter.
- **Sensitivity reported at W ∈ {0.25, 0.50} s.** If the per-slot ordering is not stable across that range, that instability IS the finding and is reported as such.
- ⚑ **This definition is deliberately evaluated on the interval STRICTLY BEFORE the cast**, so it is *not* contaminated by whatever silence the cast itself may open. A definition that looked forward would classify every interrupting cast as "channel inactive" and manufacture the opposite answer.

### 2.4 Outputs, fixed in advance

1. Per slot: `n_cast`, `n_channel_active`, **`P(channel-active | cast)`**.
2. The **unconditional mix** `m_s` and the **channel-active-conditioned mix** `m_s^{active}`.
3. The reconciliation `Σ m_s · rate_s` under both mixes, against the incumbent 0.15.
4. **Named limitations, mandatory, not optional:** slots 7 and R are BLIND to both instruments (never dim; "never cast" and "no cooldown" are indistinguishable); cast counts are **FLOORS**, not estimates (a re-fire mid-cooldown cannot be seen); OCR-blind gaps; n = 13/22/19 in ONE fight, ONE build, ONE player; and no slot is identified with any named skill by this measurement.

---

## 3 · ITEM 3 — D-W1-1: METRE-SCALE RECONCILIATION (REPORT-ONLY)

gamora's W1 prereg derives that containment of tier-16 spawn emitters requires `u ≥ 0.22277`, excluding the published `u = 0.1981` and narrowing the R-L68-2 window `[0.094, 0.3663] → [0.22277, 0.3663]`.

**Declared in advance:**
- The scale evidence I hold is `notes/crucible-arena-geometry-v1.json`, provenance **DERIVED-WEAK**, whose own band IS `[0.094, 0.3663]` — i.e. gamora is narrowing *my* band, and I must not treat my own point estimate as a datum with independent standing.
- I will **decompose my own chain term by term** and report which term(s) must move, and by how much, for `u ≥ 0.22277` to hold — and whether that movement is inside or outside the uncertainty I myself declared.
- ⚑ **NO PIN IS LANDED.** The pin decision is not this lap's (R-L3-2). Output is AGREEMENT / TENSION plus the named decisive measurement, and nothing else.
- Any HUD-zoom mismatch between the arena-perimeter capture set and this video is to be checked and reported, because "minimap pixel" is only a unit if the zoom is the same.

---

## 4 · DISCIPLINE CARRIED

READ-ONLY on all sealed artefacts, all engine data, all other seams' trees. No engine writes. No simulation code. No grading of any sealed cell. Digests derived, never retyped. Every absence or unreachable NAMED, never estimated. Commit law R-L80-2 + the L-93 `--only -m` pathspec footgun. **No pushes — the conductor releases.**

---

*galadriel, 2026-08-25. Committed before computing.*
