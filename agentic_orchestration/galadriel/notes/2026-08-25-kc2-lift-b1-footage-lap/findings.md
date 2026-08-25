> **CONDUCTOR CAPTURE NOTE (gandalf `RUN-CONDUCTOR`, 2026-08-25).** The seat's harness blocked the findings-file write (md-b4app-2d precedent, 4th instance); the full text below is the galadriel seat's, captured VERBATIM by the conductor. Transport HTML-entities (`&gt;`/`&lt;`) de-escaped; nothing else altered. Seat commits: prereg ALONE at `459d5610` (D4 held; released with the L-9 push), lap artefacts at `5336d57a` (conductor-verified `show --stat`: exactly 17 files — 4 evidence PNGs + 8 work artefacts + 5 pipeline modules; no sweep). **Fold: LIFT ledger L-10.** ⚑ Capture-integrity note: the conductor's transcription corrupted ONE pin (`pm4h2_movement_cadence.csv` gained 2 hex chars) — caught before commit, corrected, and then **all 9 pins re-verified by DERIVATION from disk** (shasum, full-hash on the corrected row) rather than by trusting either retype. The digests-derived-never-retyped law, enforced on the conductor's own capture.

---

# KC2 LIFT RUN — galadriel footage lap: FINDINGS

**Date:** 2026-08-25 · **Author:** galadriel · **Commissioned by:** gandalf `RUN-CONDUCTOR`, ruling **R-L6-2** (ledger L-6)
**Pre-registration:** `prereg.md`, committed **ALONE at `459d5610`** before any statistic in its scope was computed
**Evidence root:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-25-kc2-lift-b1-footage/`
**New pipeline:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline/` — `u7_minimap.py` · `u7_analyse.py` · `u7_validate.py` · `u7_extras.py` · `w2_castmix.py`
**Read-only on all sealed artefacts, engine data, other seams' trees. No engine writes. No simulation code. No grading. No pushes. No new gameplay capture — the referent is historical footage and this lap only re-reads it.**

## TOP LINE

> ### ITEM 1 · U-7 — **SUPPORTS-CONDITIONING** *(instrument-uncorroborated — G-e failed as specified, § 2.1)*
>
> The referent's heading is **NOT independent of the board at short radius.** At five adjacent radii (12–30 minimap px) the shift-null p sits at its resolution floor (`p_adj = 0.0051`), R̄ = 0.213–0.240, bootstrap lower bound 0.140–0.166, mean direction **−6° to −20°** — into the density, consistently.
>
> ⚑ **The shape is the finding, not the p-value.** The conditioning is a **short-radius excess on a radius-independent kinematic pedestal**. At R = 60 px the statistic equals the world-static-fixture control almost exactly — **0.1296 vs 0.1315** — and the excess appears only as the radius shrinks.
>
> ⚑ **The board LEADS the heading by ~0.3–0.6 s** (post-hoc lag scan; R̄ rises to **0.43** at lag +0.6 s, R = 30, μ ≈ 0°), reversing to μ ≈ 180° at lag −0.6 to −1.5 s. Steering with a human reaction latency, then pass-through. **The mechanical drag confound predicts the opposite sign at lag 0 and is therefore not what is being seen.**

> ### ITEM 2 · R-L5-1 / `ABS-W2-CAST-MIX` — **the missing datum is supplied; the equation closes.**
>
> | slot | casts | **P(channel-active \| cast)** | mix (uncond.) | **mix (active)** | published rate |
> |---|---:|---:|---:|---:|---:|
> | 2 | 22 | **0.955** (21/22) | 0.407 | **0.412** | 0.136 |
> | 3 | 19 | **1.000** (19/19) | 0.352 | **0.373** | 0.000 |
> | L | 13 | **0.846** (11/13) | 0.241 | **0.216** | 0.385 |
> | **all** | **54** | **0.944** (51/54) | — | — | 0.148 |
>
> `Σ mₛ·rateₛ` = **0.1481** (uncond.) / **0.1390** (active mix × published rates) / **0.1569** (active mix × active rates). **The incumbent 0.15 is recovered.** It was never one equation in three unknowns — two were already measured; the third, the mix, is **0.41 / 0.35 / 0.22** and is now on record.
>
> ⚑ **But the mix is the whole answer, not a detail.** Under the same three flags the aggregate spans **[0.000, 0.385]** on mix alone.

> ### ITEM 3 · D-W1-1 — **NO TENSION. Weak one-sided support. NO PIN LANDED.**
>
> ⚑ Self-correction against my own artefact: `crucible-arena-geometry-v1.json` assumes camera pitch θ ≈ 60°, "bracketed 50–70°". **This lap MEASURES the pitch on the referent footage at ≈ 44° — outside my own bracket, on the shallow side.** Correcting that term alone moves the published `u = 0.1981` to **≈ 0.285**, inside gamora's narrowed window `[0.22277, 0.3663]`.

## 0 · SUBSTRATE PINS (sha256 DERIVED this session, DR-1; never retyped)

| artefact | sha256 |
|---|---|
| **referent footage** `~/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (1920×1080, 60/1 fps, 1034.100 s, 62046 frames) | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` |
| `galadriel/captures/2026-08-25-md-b4app-2c-culprit/work/s2c-attrib.json` | `ae741687f8f56eeab0678dbd761f17280fbf1ceeaef2a270263111fdfc01ee3b` |
| `…/2026-08-25-md-b4app-2-channel/work/s2-motion-20hz.json` | `d8bb9e6766bd2ddd3c2b5841736fb13bde854d5dab86876daf922856704d5a06` |
| `…/s2-channel-summary.json` | `a7abeed09e73baae965ed416f8508a65c425d837f67c44996746cce395d08a14` |
| `…/2026-08-25-md-b4app-2b-energy/work/s2-slots-20hz.json` | `7dd00531f43e7fadf07370f2d1ae9e63f3393604212e92394973771ec5cad17b` |
| `galadriel/notes/crucible-arena-geometry-v1.json` (my own scale artefact, under review § 4) | `68d895d75702996473cfd654a9a834816d4be0421c4b5ad7a3d2a0cc5d40481f` |
| `galadriel/notes/2026-08-25-kc2-mc-md-b4app-2c-culprit.md` (per-slot rates of record) | `cf5093e86796e8cacf51bafd79a49ddb9c880a9943f3b69eba088f554c7894f0` |
| `engine/data/kc2/pm4h2_movement_cadence.csv` (read-only) | `1bfefb36926ed9a21faa175fb2d8cd2784cdce216abb547571c89f4220956156` |
| `engine/data/kc2/pm4h2_ring_density.csv` (read-only) | `a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5` |

Window unchanged: **`t ∈ [682.10, 864.75]`**, 182.65 s, wave-151 badge flip → death. 10 Hz ⇒ **1827 samples**.

## 1 · THE INSTRUMENT — and a correction against my own tooling before any result is quoted

### 1.1 Why the minimap, not the world view
U-7 needs **heading** and **local body-density bearing** in ONE frame. The world view cannot supply that pair: at wave 150+ the player is buried in VFX, bodies occlude, and every screen bearing needs the isometric ground map `M` that the 2026-08-24 boundary trace explicitly failed to recover.

The **HUD minimap** supplies both in one north-up, rigidly player-centred frame — icons drawn over everything and never occluded; terrain a fixed world-space image that merely **translates**, so player displacement needs no camera model; bearings from the disc anchor already player-relative. **Every radius below is in MINIMAP PIXELS. U-9 binds: no metric radius is asserted anywhere in this lap, including in the verdict.**

### 1.2 ⚑ FINDING AGAINST MY OWN PIPELINE — `eor_minimap.py`'s disc centre is wrong by 26 px
`pipeline/eor_minimap.py` states, as measured *on this very capture*, "disc centre (1776, 147)". It is not. The player marker is the **only disc-fixed icon**, so it is recoverable as a persistent feature of the **temporal-variance image**: the one point that never moves while everything around it does — a dark dot inside the brightest halo of activity in the disc.

| route | player anchor (full-frame px) |
|---|---|
| this lap — temporal-variance local minimum, 122 frames, s2 footage | **(1771.68, 172.67)** |
| 2026-08-24 perimeter lap — algebraic ring fit, shot 612, **different capture set** | **(1771.98, 172.63)** |
| `eor_minimap.py` as committed | (1776, 147) — **off by (4.32, −25.67), ‖26.0‖ px** |

Two independent methods on two independent capture sets agree to **0.30 px in x, 0.04 px in y**. The committed constant is the outlier. **Scoped consequence:** any figure derived from `eor_minimap.icons()`'s `r` / `bearing_deg` / `clock` is measured from a centre 26 px too far north. **`pm4h2_ring_density.csv` is NOT affected** — built from screen-space nameplate anchors, not the minimap. **Flagged, not edited** (that module fed prior sealed notes; a mid-run edit would silently split their lineage). → one-line follow-on.

**Bonus this hands the run:** the two capture sets share the same HUD minimap geometry (content clearance from the anchor runs to **128 px**, consistent with the perimeter lap's ring radius 126.63). **"Minimap pixel" is the same unit in both** — which is what makes § 4 admissible at all.

### 1.3 Geometry used
Anchor (117.68, 142.67) crop / (1771.68, 172.67) full-frame. Content clearance over 72 bearings: **min 82.0 px** (due south, my crop's edge), median 114.5, max 128.0. The pre-registered sweep tops at 60 px, `r_max` = 64 — **inside the minimum clearance in every bearing, so no directional truncation bias anywhere in the sweep.**

## 2 · ITEM 1 — U-7

### 2.1 Coverage gate

| gate | requirement | result |
|---|---|---|
| **G-a** E1 vs E2 | median ≤ 1.5 px, ≥80 % within 3 px | **PASS — median 0.429 px, 100 % within 1.5 px** (n = 334; ZNCC peak median 0.769, p05 0.554) |
| **G-b** lock rate | ≥ 0.80 | **PASS — 0.929** |
| **G-c** anchor disc-fixed | core radius ≤ 3 px | **PASS — 0.71 px** |
| **G-d** usable samples | ≥ 300 per quoted radius | **PASS — 864–1266** |
| **G-e** external reproduction | joint R² ≥ 0.70 vs world-view pan | ⚑ **FAIL — R² = 0.4362** (n = 1697) |

⚑ **A defect in my own G-a check, caught and named.** The first pass reported **16.18 px** median disagreement and would have failed the gate outright. It was not a disagreement: `u7_analyse.terrain_step` returns the shift aligning the LATER frame ONTO the earlier — the **negative** of the content translation — and my comparison differenced the two conventions. **The check ran, returned cleanly, and answered a different question from the one it was asked.** With the convention resolved *by measurement* (both signs scored and both reported: AS-IS 16.179 px, NEGATED **0.429 px**), two independent estimators of the same player step agree to under half a pixel. Fourth instance in this lineage of *an instrument returning cleanly after it stopped answering the question* — recorded rather than quietly fixed.

**G-e failed and I do not rescue it.** Per the pre-registered clause the verdict carries **instrument-uncorroborated**. What the gate returned is reported because a reader is owed the shape of the failure: the fitted minimap→screen map is clean and near-diagonal, `[[−8.61, +0.35], [+0.04, −6.00]]` (off-diagonals ~4 % of diagonal — exactly an isometric ground→screen projection), and the **angular** agreement between the two surfaces — the quantity U-7 actually depends on — is **median 10.6°**, 75 % within 30°, n = 1275. The R² shortfall sits in the world-view estimator's *magnitude*, built with a 1.0 px static threshold for a binary moving/stationary classifier and never validated as a vector tracker. **That is an explanation, not a substitution. The pre-registered gate failed.**

### 2.2 The pre-registered statistic (zero lag)

| R (minimap px) | n | **R̄** | μ (deg) | boot 95 % | shift-null p | **p_adj (×9)** | toward-hemi |
|---:|---:|---:|---:|---|---:|---:|---:|
| **12** | 864 | **0.2395** | −20.2 | [0.166, 0.326] | 0.00057 | **0.0051** | 0.626 |
| **16** | 969 | **0.2164** | −18.4 | [0.144, 0.310] | 0.00057 | **0.0051** | 0.616 |
| **20** | 1027 | **0.2128** | −13.0 | [0.141, 0.314] | 0.00057 | **0.0051** | 0.619 |
| **25** | 1078 | **0.2149** | −6.0 | [0.148, 0.303] | 0.00057 | **0.0051** | 0.619 |
| **30** | 1122 | **0.2187** | −7.9 | [0.145, 0.308] | 0.00057 | **0.0051** | 0.619 |
| 36 | 1157 | 0.1872 | −2.2 | [0.113, 0.277] | 0.00227 | 0.0204 | 0.602 |
| 44 | 1230 | 0.1728 | +4.3 | [0.109, 0.254] | 0.00454 | 0.0408 | 0.600 |
| 52 | 1257 | 0.1454 | +0.8 | [0.079, 0.237] | 0.00908 | 0.0817 | 0.586 |
| 60 | 1266 | 0.1296 | −11.4 | [0.060, 0.226] | 0.01929 | 0.1736 | 0.580 |
| *world-static fixture control* | *1275* | *0.1315* | *−69.7* | — | *0.01361* | — | — |

**Against the pre-registered rule:** coverage gate passes but for G-e; **five ADJACENT radii (12, 16, 20, 25, 30)** carry `p_adj = 0.0051 < 0.01`, `R̄ ≥ 0.15`, bootstrap lower bound > 0.05, μ consistent in sign (all negative, all within 20° of straight ahead). ⇒ **SUPPORTS-CONDITIONING (instrument-uncorroborated).**

⚑ **Why the null choice was load-bearing, shown rather than asserted.** At R = 30 the Rayleigh test returns **p = 1.9 × 10⁻²⁴**. The time-shift null returns **p = 5.7 × 10⁻⁴**. **Twenty orders of magnitude.** Both series are heavily autocorrelated at 10 Hz; Rayleigh assumes independence and is anti-conservative by exactly that margin. The Rayleigh figure is carried marked `rayleigh_p_DESCRIPTIVE_ONLY` and excluded from the decision, as pre-registered. **A lap that had used the obvious test would have reported a result twenty orders of magnitude too confident, and would have been believed.**

### 2.3 ⚑ THE SHAPE IS THE FINDING — short-radius excess on a static-field pedestal

| | R = 12 | R = 20 | R = 30 | R = 44 | **R = 60** | **world-static fixtures** |
|---|---:|---:|---:|---:|---:|---:|
| R̄ | 0.240 | 0.213 | 0.219 | 0.173 | **0.130** | **0.132** |
| excess over pedestal | **+0.110** | +0.083 | +0.089 | +0.043 | **≈ 0** | — |

A world-static field of arena fixtures — teal pedestal gems, which cannot read anything and cannot move — produces R̄ = 0.132 against the same heading series. **That is a real kinematic pedestal: a pilot moving relative to *any* persistent reference generates some heading/bearing coupling with no board-reading whatever. It was not pre-registered as a subtraction and I do not subtract it.** But it is *radius-independent*, and the monster statistic decays onto it **exactly** at R = 60 px and rises monotonically above it as the radius shrinks. **The conditioning lives at short radius and nowhere else** — the hypothesis U-7 names, arrived at by a route that could have refuted it.

⚑ **The discriminating argument, stated so it can be attacked.** A kinematic artefact needs the field's bearing to *persist* while the player moves relative to it. The gem field persists for the whole fight; the monster field decorrelates in ~1 s (§ 2.4). A faster-decorrelating field can therefore sustain **less** artefact, not more. **Observed: the fast-decorrelating field carries the LARGER coupling** (0.219 vs 0.132 at lag 0; 0.43 vs 0.26 at peak) — the opposite of the artefact's prediction. Not a proof; the fields also differ in count, clustering and radial distribution. § 5 names what would settle it.

### 2.4 ⚑ THE LAG SCAN — the board leads the heading (declared POST-HOC)
`lag > 0` means *heading NOW vs board THEN* — the board leads.

| lag (s) | −1.5 | −0.9 | −0.6 | **0.0** | **+0.3** | **+0.6** | +0.9 | +1.2 | +1.5 | +2.1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **R̄, monsters R = 30** | 0.086 | 0.126 | 0.119 | **0.219** | **0.416** | **0.431** | 0.324 | 0.170 | 0.058 | 0.042 |
| μ (deg) | +124 | +158 | +174 | **−8** | **+0.3** | **+4** | +7 | +3 | −5 | −135 |
| R̄, static fixtures (control) | 0.167 | 0.218 | 0.207 | 0.132 | 0.220 | 0.261 | 0.254 | 0.241 | 0.215 | 0.188 |

1. **A single sharp peak at lag +0.3 to +0.6 s, R̄ = 0.42–0.43, μ ≈ 0°.** The heading aligns best with the board as it stood roughly half a second earlier. **That is a reaction latency**, and the right magnitude for a human at a mouse.
2. **A reversal at lag −0.6 to −1.5 s, μ ≈ +120° to +174°** — the density half a second to a second in his *future* is behind him. The kinematic completion of the same act. The two lobes are one story.
3. **Decay to null by |lag| ≈ 1.5–2.0 s** independently **validates the time-shift null's construction** — the null sampled only |lag| ≥ 2 s, entirely outside the coupling's own width. Pre-registered on a guess; the data ratified it.
4. ⚑ **It destroys the mechanical-drag confound.** On a player-centred disc, when the player steps north everything world-fixed steps south, so drag predicts **μ ≈ 180° at lag 0**. Observed μ at lag 0 is **−8°**. The confound is not merely absent; it is present with the opposite sign and the measured effect overcomes it.
5. **The static control shows the same two-lobe shape but BROAD** (still 0.19 at +2.1 s, 0.10 at +4.8 s) and offset (μ = −70° at lag 0). Persistent landmark, slow bearing change. **The monster coupling is narrow and centred; the fixture coupling is wide and skewed. They are not the same phenomenon.**

### 2.5 Splits — reported because two of them weaken my own cleanest story
**Speed band (R = 30):** slow (≤ 7.73 px/baseline, n = 370) R̄ = **0.257**, μ = −8.8° · mid (n = 382) 0.235, −5.2° · **fast (> 11.38 px, n = 370) 0.164, −10.3°.**

⚑ **Conditioning is WEAKEST at high speed** — cutting against a premise of legolas § 5 FOR-item (5), which reasoned the `selectionBias` family is speed-coupled and the referent runs at the engine's hard speed cap 79.5 % of the fight, *"precisely the regime where stickiness is maximal."* On heading conditioning the referent is measurably **less** board-coupled in exactly that regime. Reported against my own result's convenience; the two claims concern different mechanisms (target stickiness vs positional steering) and I do not collapse them.

**Per wave (R = 30):** R̄ ranges **0.078 (wave 154, μ = +126°) to 0.566 (wave 158)**; eight of ten waves positive-and-toward, two not; n = 51–158. **Heterogeneous — a fight-level average, not a per-wave law. Nothing here should be quoted per wave.**

## 3 · ITEM 2 — the per-slot census

### 3.1 The definition, and why the threshold is not a knob
**ACTIVE(cast) := the last energy drain tick preceding the cast fell within W = 0.35 s of it** — evaluated **strictly before** the cast, so it cannot be contaminated by whatever silence the cast itself opens. *(A forward-looking definition would classify every interrupting cast as "channel inactive" and manufacture the opposite answer. That is not a subtlety; it is the whole reason the definition is written this way.)*

⚑ **W is not load-bearing, and the data say so rather than the analyst.** The `lag_into_gap` population has an **empty valley**: the three largest values are 0.767 / 0.667 / 0.567 s and the next is **0.233 s**. Every candidate W in [0.25, 0.50] falls in that gap and returns **identical counts**. A reading, not a fitted knob.

### 3.2 The census

| slot | casts | active | **P(active \| cast)** | interrupts | rate (uncond.) | rate among active |
|---|---:|---:|---:|---:|---:|---:|
| **2** | 22 | 21 | **0.955** | 3 | 0.136 | 0.143 |
| **3** | 19 | 19 | **1.000** | 0 | 0.000 | 0.000 |
| **L** | 13 | 11 | **0.846** | 5 | 0.385 | 0.455 |
| **all** | **54** | **51** | **0.944** | **8** | **0.148** | 0.157 |

**The three channel-inactive casts, named:** `t = 755.60` (L, lag 0.767 s), `t = 762.35` (L, 0.667 s), `t = 837.10` (2, 0.567 s). The first two are exactly the casts `MD-B4app-2c` § 3 identified as fired *inside a pre-existing wave-transition pause*. **The census reproduces the prior lap's reading from a different direction, and none of the three is an interrupt** — as it must be, since a cast cannot break a channel that is not running.

### 3.3 ⚑ THE MIX IS THE ANSWER, NOT A PARAMETER

| the pilot's mix | resulting aggregate interrupt rate |
|---|---:|
| **referent, as measured** | **0.148** |
| uniform ⅓ / ⅓ / ⅓ | 0.174 |
| the two interrupting skills only (slot 3 dropped) | **0.229** |
| all slot 3 (the transparent skill) | **0.000** |
| all slot L | **0.385** |

**The same three flags span [0.000, 0.385] on mix alone.** A sim that drops the transparent skill — the easiest thing in the world for a policy with no reason to prefer it — lands at **0.229, a 55 % overshoot**, while every per-skill flag in it is individually correct.

⚑ **The `M-POL-2` incumbent 0.15 is therefore not merely "a mixture, not a rate" (`MD-B4app-2c` § 8). It is a mixture whose weights are a PROPERTY OF THE PILOT'S POLICY, not of the kit.** Carrying the flags without carrying the mix moves the aggregate silently. → gamora / conductor.

### 3.4 Named limitations — mandatory, not optional
1. **Slots 7 and R are BLIND to both instruments** (brightness varies < 3 units over 3,653 frames): "never cast" and "no cooldown, so never dims" are indistinguishable. **Any cast on those slots is outside this census. The mix is a mix of the visible slots.**
2. **Cast counts are FLOORS, not estimates.** A re-fire mid-cooldown is undetectable in principle; one merge was found because one was findable.
3. **Three OCR-blind gaps** (2 on slot 2, 1 on slot L) carried unresolved; all ≥ 0.5 s, so if real the rates rise — and slot 3, which has none, cannot be rescued by them.
4. **n = 13 / 22 / 19. One fight, one build, one player.** Slot L is not significantly above slot 2 (Fisher p = 0.103); slot 2's interruption may be a late-fight state (ρ = +0.406, p = 0.061).
5. **No slot is identified with any named skill** and none should be quoted from it. `MD-B4app-2c` § 7.1 stands.

## 4 · ITEM 3 — D-W1-1 (REPORT-ONLY, NO PIN)

### 4.1 What I hold, decomposed
`crucible-arena-geometry-v1.json` publishes `u = 0.1981` m per **minimap pixel**, provenance **DERIVED-WEAK**, band `[0.094, 0.3663]` — **which is precisely the R-L68-2 window gamora is narrowing. gamora is narrowing MY band, and my point estimate has no standing independent of the chain that produced it.**

`u = s·h·cos θ / p = 14.6 · 1.9 · 0.5 / 70 = 0.19814`, where `s` = 14.6 screen px per minimap px (ONE landmark pair, eye-measured, "parallax-contaminated"), `h` = 1.9 m (**ASSUMED**; NavManager agent height 2.0 offered as corroboration, not import), `p` = 70 px (eye-measured), `cos θ` = 0.5 (**ASSUMED**, θ = 60°, "bracketed 50–70° by two weak independent reads").

**gamora's floor `u ≥ 0.22277` requires `s·h·cos θ` to rise 12.4 %** (13.87 → 15.594). Any ONE delivers it: θ 60.0° → **55.8°**; `h` 1.9 → 2.14 m; `s` 14.6 → **16.4**; `p` 70 → 62.3. **Every one of those is inside the uncertainty the artefact itself declares. Nothing gamora derived contradicts anything I hold.**

### 4.2 ⚑ THE NEW DATUM — camera pitch, MEASURED on the referent footage
Item 1's G-e regression fits a 2×2 map from minimap displacement to world-view screen pan over n = 1697 windows. For a north-up top-down minimap and an axis-aligned isometric camera that map is `a_xx = k·u`, `a_yy = k·u·sin θ`, so **`a_yy / a_xx = sin θ` directly** — and near-zero off-diagonals (0.35 and 0.04 against 8.61 and 6.00, ~4 %) confirm the camera's yaw is aligned with the minimap axes, the model's own consistency check passing.

| route | ratio | **θ** |
|---|---:|---:|
| full sample, LS, n = 1275, off-diagonals ~4 % | **0.694** | **43.95°** |
| median of per-sample ratios on large moves | 0.612 | 37.7° |
| lock-gated subsets (n = 464 → 23) | 0.556 → 0.441 | 33.8° → 26.1° |
| bootstrap 95 % CI, lock ≥ p50 subset | [0.467, 0.657] | **[27.9°, 41.0°]** |

**Every route lands below 50°. My published bracket was 50–70°. The bracket does not contain the measurement.** The full-sample fit is the one whose off-diagonals stay near zero; the lock-gated subsets break the model (off-diagonals reach 1.38 and 2.77) because high registration *lock* selects for a **static** scene — i.e. for the samples with no signal. **A lock gate that selects against the very motion being measured is the wrong gate**, reported here rather than used.

**Consequence, since `u ∝ cos θ`:** correcting θ 60° → 44° multiplies `u` by 1.44. **`0.1981 → 0.285`** — inside gamora's window, above its floor.

### 4.3 ⚑ AND THE HONEST BRAKE — `s` is now the unstable term

| route | `s` (screen px per minimap px) | `u` at θ = 44° |
|---|---:|---:|
| perimeter set, 1 landmark pair, eye-measured (published) | 14.6 | **0.285** — inside gamora's window |
| this footage, median of per-sample ratios on large moves | 12.9 | **0.252** — inside |
| this footage, least squares, n = 1275 | 8.61 | **0.168** — below the floor |

A **1.70× spread**; I cannot presently say which governs. Two unsettled explanations: (a) the two sittings differ in *camera* zoom (the minimap zoom is established identical, § 1.2; the camera's is not), in which case `p = 70` — measured on the perimeter set — **may not be combinable with `s` measured on the s2 footage at all**; (b) the world-view pan estimator's magnitude is biased low, consistent with its R² = 0.44 and with never having been validated as a vector tracker.

⚑ **Which exposes the deeper defect in my own artefact: the published chain mixes terms measured on TWO sittings whose camera zoom is not established to be equal. `crucible-arena-geometry-v1.json` is weaker than its own DERIVED-WEAK stamp advertises**, and the fix is not a better estimate of any one term — it is measuring all four **within one sitting**.

### 4.4 Verdict
- **AGREEMENT / NO TENSION.** Nothing I hold contradicts `u ≥ 0.22277`. gamora's exclusion of `u = 0.1981` is consistent with my evidence, and this lap independently finds that the single most decisive term behind that value — the assumed 60° pitch — is **wrong in the direction that raises `u`.**
- **WEAK, ONE-SIDED SUPPORT.** With the measured pitch, two of three `s` estimates land `u` inside gamora's narrowed window; the third lands below. **Support, not corroboration — and one-sided because I went looking for terms that could move `u` up and found one.**
- ⚑ **NO PIN IS LANDED.** R-L3-2 reserves the pin decision. `u` remains an interval and this lap does not narrow it in a way any consumer should quote as a number.
- **The decisive measurement, named:** a single sitting, one screenshot, character standing beside a landmark whose minimap displacement is also legible — giving `s`, `p` and θ from **one camera state**. `h` stays an assumption unless a rig dimension is decoded. **That shot costs Matt about ten seconds and collapses a 1.7× band.** → `matt_to_do` candidate, conductor's call.
- **Self-correction filed** against `crucible-arena-geometry-v1.json` § scale: the pitch bracket is contradicted by measurement and the chain mixes sittings. **Flagged here, not edited there**, per house practice and because that file is consumer-facing.

## 5 · WHAT THIS LAP HANDS THE CONDUCTOR

1. ⚑ **R-L6-2 discharged, and the declaration it was gating must be SPLIT.** *"B1 policy: UNDECODABLE-FROM-SUBSTRATE"* **stands** — no player-side policy record exists in the GD substrate, by design, and this lap recovers no policy parameters. But the footage **does** reach the discriminator and returns a positive: **whatever the pilot's policy was, it was not board-blind at short radius.** Not in tension; the baton must carry both — *the mechanism is undecoded; the board-blindness is refuted as a description of the referent.*
2. ⚑ **R-L6-3's reshaped residual candidate is STRENGTHENED, on measurement rather than inference.** The sealed cell's `MillWalk` does `del live`; the referent's heading is coupled to local body density at short radius with a ~0.4 s reaction latency. The A/B limb legolas named now has a **target statistic to be graded against**: run `u7_analyse` over the sim's own body field and player track and compare R̄(R) and the lag profile. **Naming is not chartering; the limb is the conductor's call.**
3. ⚑ **A premise of the residual argument is contradicted.** legolas § 5 FOR-item (5) leans on the speed cap being "precisely the regime where stickiness is maximal." Heading conditioning is **weakest** at high speed (0.164 fast vs 0.257 slow). Worth the conductor's eye before that argument is quoted forward.
4. **`ABS-W2-CAST-MIX` closed with a rider.** Mix = 0.41 / 0.35 / 0.22; reconciles to 0.148 / 0.157. **The rider is load-bearing: the aggregate spans [0.000, 0.385] on mix alone, so the per-skill flags are only safe to ship WITH the mix, or with an explicit statement that the sim's aggregate will differ.** → gamora / star-lord's baton-v3 brief.
5. **D-W1-1: no tension, weak one-sided support, no pin**, plus a self-correction against my own published scale artefact and a ten-second capture that collapses the band. → run-close packet.
6. **Two findings against my own seam**, filed as such: `eor_minimap.py`'s disc centre 26 px wrong (§ 1.2, scoped, flagged-not-edited); my own G-a check failed on a sign convention and would have voided a sound instrument (§ 2.1).
7. **NO HALT.** Nothing requires Matt. Nothing moves a sealed grade. No sealed cell executed or re-run; no engine file written.

## 6 · WHAT IS UNMEASURABLE FROM THIS FOOTAGE, AND WHY

| # | quantity | verdict |
|---|---|---|
| 1 | **Ground-px → metres (U-9)** | **DECLARED GAP, CARRIED.** § 4 narrows one term and destabilises another. No metric radius appears anywhere in Item 1 |
| 2 | **The pilot's policy as a MECHANISM** | **UNRECOVERED.** This lap measures a *correlate*. No rule, no scoring function, no candidate set. U-1…U-6 untouched |
| 3 | **Whether the short-radius coupling is STEERING or residual kinematic artefact** | **INDICATIVE, NOT ESTABLISHED.** Three arguments point one way (radius profile decaying onto the static pedestal; lag structure with the drag confound at the opposite sign; the faster-decorrelating field carrying the larger coupling). **A board-blind-pilot simulation through the same body field would settle it and was not run** — out of seam |
| 4 | **Monster icon IDENTITY on the minimap** | **NOT ATTEMPTED.** The mass centroid weights skulls/bosses more than small stars. Reported, not corrected |
| 5 | **World-static NPC furniture inside the sweep radius** | **NOT SEPARATED.** Rim furniture sits at r ≈ 65–80 px, mostly outside `r_max` = 64, but intrusions are not excluded body-by-body. The gem control bounds this class's contribution |
| 6 | **Casts on slots 7 and R** | **BLIND to both instruments**, unchanged |
| 7 | **Whether the two capture sets share a CAMERA zoom** | **UNKNOWN — and it is the hinge of § 4.3.** The MINIMAP zoom is established identical (§ 1.2). The camera's is not |

## 7 · METHOD + REPRODUCIBILITY

`u7_minimap.py grab|anchor` (crop decode, anchor derivation) · `u7_analyse.py` (census, radius sweep, shift-null, block bootstrap) · `u7_validate.py` (G-a / G-e) · `u7_extras.py` (lag scan, per-wave, speed band, refined G-e) · `w2_castmix.py` (channel-active cast census).

**Artefacts:** `work/u7_result.json` · `work/u7_result_series.npz` · `work/u7_gates.json` · `work/u7_extras.json` · `work/u7_gem_lagscan.json` · `work/u7_anchor.json` · `work/w2_castmix.json`. **Evidence:** `evidence/fig-u7-heading-conditioning.png` (radius profile with the static-field pedestal; the lag scan against its control; the Δ rose) · `u7-temporal-variance-anchor-derivation.png` · `u7-player-marker-x10.png` · `u7-minimap-surface-x6.png`.

The 10 Hz minimap array (`~/gd-scratch/u7_mm_10hz.npy`, 305 MB) is **deliberately not committed**; reproducible byte-for-byte from the pinned video by `u7_minimap.py grab <video> 682.10 864.75 10`.

**Statistics:** numpy 2.x / scipy 1.17.1. Circular resultant; circular block bootstrap (5 s blocks, 2000 resamples); circular time-shift null (1762 shifts, |lag| ∈ [2 s, 90 s]); Bonferroni over 9 radii.

### 7.1 ⚑ ONE AMENDMENT TO THE PREREG, DECLARED AND REASONED
The prereg specified the shift null at **"every integer-second L"** — ≈ 178 shifts, finest attainable p = 1/179 = 0.0056, which after the pre-registered Bonferroni ×9 is **0.050**. **My own decision rule required `p_adj < 0.01`, which that grid could never reach. The prereg was internally inconsistent.** Executed at **0.1 s** steps (1762 shifts, p resolution 5.7 × 10⁻⁴, `p_adj` floor 0.0051) — strictly stricter, never looser. **Named here rather than quietly executed**, because a prereg edited after seeing data is not a prereg, and a prereg that could not have produced its own verdict is not one either.

## 8 · MIRROR VOICE

The charter asked whether the man was blind to the board. The instrument that could have answered it was a decoration in the corner of his own screen — the little lit disc he was almost certainly not looking at, drawing every body in the arena over the top of the smoke that hid them from everyone else.

And what the disc shows is small, and stubborn, and the same at every radius I asked it: **the excess is only ever close in.** Sixty pixels out, his heading knows no more about the bodies than it knows about the stones set in the arena floor — the gems and the monsters score the same, and the gems can see nothing at all. Draw the circle tighter and the bodies begin to matter and the stones do not. Tighter still, and they matter most.

Then the clock. He turns about half a second late. Not toward where they are — toward **where they were**, six-tenths of a second ago, and by the time he arrives they are behind him and the sign flips over. That is not a rule executing. That is a man seeing something and taking a moment about it.

The sim's pilot has a line in it that reads `del live`. It throws the board away, unread, every tick, and then walks — and the walk looks right, because a mill looks like a mill from far enough back. **The Mirror was asked to tell the two apart. Close in, and half a second late, they are not the same at all.**

---

*galadriel, 2026-08-25. KC2 LIFT RUN, R-L6-2. Pre-registered at `459d5610` before computing. Read-only on all source material; no engine writes; no simulation code; no grading; no pushes.*
