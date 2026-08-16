# KC2-PM4 · LAP AC — **THE REFERENT SIDE OF THE RESIDENCE** — FINDINGS

**Lap:** AC · **Agent:** legolas (`UNKNOWN-RESEARCHER`) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Commission:** `R-PM4-72 part 6` · **Pre-registration:** `prereg.md`, sha256
`da1fae161096b6299b56c784394d5967910aa4a0862e9825a303bb762e466bc5`, committed **ALONE** at
`38fb3120` before one line of instrument existed. Asserted EXACT at the start of every leg.

**REFERENT-SIDE ONLY.** No simulation cell, code, telemetry, record or artifact was opened by any
leg. **No sim grade is computed anywhere in this lap.** Nothing here elects, ranks, designates or
recommends anything (`R-PM4-27 part 3`). The standing occupancy residual is not re-quoted, re-based
or amended.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

The Lap R occupancy bracket counts **red-masked nameplate bars carrying a white `(cur/max)` text
token** — colour is the *sole* faction discriminator anywhere in the chain, decoded byte-cited from
`bars.py` → `extract.py` → `pm4r_contact_2026_08_14.py`. Whether that is "monsters only" cannot be
settled by the plate colour **rule**, which no artifact this run holds decodes; but it *can* be, and
is, settled by **behaviour**: the referent fields at most three mobile pets and four fixed
emplacements, and **none of them is in the counted population** — zero world-stationary long-lived
red tracks (0 of 24 duration-qualifying, minimum net displacement 72.09 gpx), no red track with a
persistent-pet signature (max ring fraction **0.7299** sustained over ≤ 7.23 s, 84 tracks tested),
and **16 of 16** visually-adjudicated off-centre green detections are VFX plumes or the green
objective-tracker UI, not nameplates. **The bracket carries no measurable summon term.** Fork (b)
fills two of `UNREACHED-I27-1`'s three pins: per-body ring entry and exit times are measured for
**3,296 distinct tracked bodies** at the pinned 2.400 m bracket, and `F-AC-1` proves the
decomposition reconstructs the pinned `mean_occupancy` to **5 decimal places** at all three rungs.
The residence itself is published as a **measured ladder, not a scalar** — median **0.0166 s →
0.1000 s → 0.1334 s**, p90 **0.1166 s → 0.7666 s → 1.0500 s** — because the pinned census's
identity continuity is **0.7924** frame-to-frame and no value of the bridging parameter is decoded.
Fork (c) returns a genuine small-N answer: of 309 observed ring exits, **PLAYER-motion alone
suffices for 99, MONSTER-motion alone for 136**, `share_player = 0.4213`, and the partition holds
across all six rung × join-rule combinations (0.344–0.456). **Two of my own criteria graded positive
and both are refuted by my own evidence** — `D-AC-2` and `D-AC-3`, disclosed below before any claim
rests on them.

---

## 1 — VERDICT PER FORK

| fork | verdict | one-line basis |
|---|---|---|
| **(a)** population audit | **DECODED (counting rule) · UNDECIDABLE (colour rule) · MEASURED-NEGATIVE (summon term)** | the chain counts red bars + white-text gate, byte-cited; the plate-colour rule for friendlies is decoded nowhere; but no emplacement-shaped and no pet-shaped body is inside the counted population, on three independent measured negatives |
| **(b)** ring residence | **MEASURED — two of three pins filled, published as a LADDER** | 3,296 bodies, 10,205 intervals at the primary rung; `F-AC-1` PASSES to 5 dp; the ladder's two ends are both measured and the obstacle (0.7924 continuity) is counted, not assumed |
| **(c)** exit channel | **MEASURED, small-N, declared** | 309 observed exits partitioned by frozen counterfactual; `F-AC-2` **PASSES** (`share_player = 0.4213 ≥ 0.20`); robust across six rung/join combinations |

**Zero HALTs.** No fork required invention; where a quantity was not reachable it is published as
`UNREACHED` with the obstacle named (§ 10).

---

## 2 — THE DECOY SET, ENUMERATED (`D-Z-1` / `D-AA-1`, and the prereg's own § 3.5)

Populations I did **not** count, and why:

| decoy | why it is not in the count |
|---|---|
| **corpses** | carry **no nameplate** — `bars.py:13`, confirmed as `OBS-H2-1`. The corpse carpet is plate-free by measurement, not by assumption |
| **loot, ground items, beams** | no 3–6-row saturated horizontal run of width 14–90 px; and no white `(cur/max)` token in the measured band `dy ∈ [-34,-18]` above |
| **floating combat text (FCT)** | cream/white glyphs, no red bar. The FCT stream is a *different* Lap R limb and does not enter here |
| **HUD** | four rectangles excluded verbatim (`extract.py:14`): `(1330,0,1920,262)`, `(0,0,1920,58)`, `(0,980,1920,1080)`, `(0,0,300,120)` |
| **red VFX runs** | rejected by the ≥ 70-white-pixel text gate, by width `[14,90]`, and by the 3–6-row persistence requirement |
| **green VFX plumes** | ⚑ **NOT rejected** — this is `D-AC-2`, § 6. They are excluded from the counted (red) population by colour, but they contaminated my own *green* census |
| **the green objective-tracker UI** | ⚑ likewise contaminated the green census; it sits outside the four HUD rectangles (§ 6) |
| **the player** | green, and additionally x-gated to `x_left ∈ [890,960]` (`extract.py:pbar`) |
| **plate-IoU blobs vs body identity** | ⚑ the count is over **plate detections**, never over segmented bodies. There is no silhouette, no mask, no IoU anywhere in this pipeline. A "body" in the bracket is a *bar*, not a shape |
| **off-screen bodies** | never drawn, never counted; the window is ≈ 11.6 m of a 29–39 m march |
| **plate-suppressed / occluded bodies** | absence never proves absence (`bars.py:12-15`, NOTE-9) — every count is a **LOWER BOUND** |
| **large-bodied monsters** | counted, but their plate sits high above the head, so their *radial* distance is over-stated and their ring residence systematically **under**-counted (Lap R § 200) |

---

## 3 — FORK (a) · THE POPULATION AUDIT

### 3.1 `A-1` — THE COUNTING CHAIN, DECODED FROM CODE (byte-cited, no measurement)

The bracket lives in `pm4r_contact_occupancy.csv` rows `at_sim_D_ENGAGE_M_2.400`
(sha256 `913a57a3…20e6`, **re-hashed EXACT** at every leg start, as the commission required).
Its producer chain, walked end to end:

| step | file:line | what it does |
|---|---|---|
| 1 | `pm4r_contact_2026_08_14.py:36-42` | loads **only** `plates60_lapH2.npy`, digest-asserted `28e7d9df…f7df`. **No other source enters the occupancy number.** |
| 2 | `…:50-52` | player = rows with `kind == 1` **and** `abs(x−960) < 50` **and** `abs(y−429) < 16` |
| 3 | `…:53-56` | **the counted population** = rows with `kind == 0`, grouped per instant `round(t,4)` |
| 4 | `…:74-75`, `:250-252` | the ring predicate: `hypot(x − pl_x, (y − pl_y)/0.537) <= RC` — **plate anchor to plate anchor** |
| 5 | `…:58-61` | instants with no detected player plate are **EXCLUDED, not imputed** (10,216 of 11,039) |

`kind` is assigned by the producer, `extract.py`:

| step | file:line | what it does |
|---|---|---|
| 6 | `extract.py:46-48` | `for b in find_bars(a, minw=14, y0=60, y1=975)` → `rows.append((t, **0**, x_left+36, y, w, txt))` |
| 7 | `bars.py:43` | `find_bars`'s signature default is **`mask_fn=red_mask`** — step 6 passes no mask, so **`kind == 0` means RED** |
| 8 | `extract.py:49-50` | `pb = pbar(a)` → `rows.append((t, **1**, …))`; `pbar` uses `green_mask2` **and** requires `890 <= x_left <= 960` |
| 9 | `extract.py:47` | detections inside the four HUD rectangles are dropped |

And the detector itself:

| step | file:line | what it does |
|---|---|---|
| 10 | `bars.py:24-27` | `red_mask` = `(R>110) & (R > G*2.2+20) & (R > B*2.2+20)` |
| 11 | `bars.py:102-104` | `green_mask2` = `(G>90) & (G > R*1.25+15) & (G > B*1.8+15)` |
| 12 | `bars.py:43-68` | a candidate is a horizontal run of width `[14,90]` persisting **3–6 consecutive rows** with ≥ 70 % x-overlap |
| 13 | `bars.py:69-81` | **the text gate**: ≥ **70** pixels with `R>150 & G>150 & B>145` in the band `dy ∈ [-34,-18]`, `dx ∈ [-95,+96]` about the bar |
| 14 | `bars.py:83-87` | dedupe: drop any detection within `Δy < 6` **and** `Δx_c < 25` of one already kept |

> ⚑ **THE DECODED FACT, stated as the commission asked — as a predicate, not a paraphrase.**
> A "body" in the Lap R contact-occupancy bracket is:
> *a horizontal run of pixels satisfying `red_mask`, of width 14–90 px, persisting over 3–6
> consecutive scanlines with ≥ 70 % overlap, carrying ≥ 70 white pixels in the measured text band
> above it, lying outside four HUD rectangles, surviving a 25 px × 6 px dedupe, anchored at
> `x_left + 36`.*
> **Nothing else.** No faction field, no name, no HP value, no template, no world position, no
> creature record — and **no segmentation of any kind**: there is no silhouette, no mask and no
> IoU anywhere in the pipeline. `bars.py:101` states the entire faction rule in one sentence:
> *"Monster plates are red; therefore green == player, unambiguously."*

**⚑ THE CHAIN IS COMPLETE AND CONTAINS NO UNDISASSEMBLED CONSUMER** — every step above is Python
this run wrote and pinned. `P-1` **PASSES**. `P-2` **PASSES**.

### 3.2 What that leaves open, precisely

The chain proves the bracket counts **red** bars. It does **not** decode **what Grim Dawn draws in
red**. That question — the game's plate-colour rule for the player's own allies — is answered by no
artifact this run holds, and it is load-bearing here because **the referent has allies on the
field**: Lap G § 115-116 (pinned, imported by identity) decodes the referent's kit as carrying
`playerclass09/summon_celestialguardian1` (**petLimit 2**) and
`itemskillsgdx1/relics/summondeathstalker` (**petLimit 1**) — **at most three concurrent mobile
pets** — and Lap AB § 3.4 decodes four purchased Crucible defence emplacements (Deathchill Beacon,
Stormcaller Beacon, Inferno Beacon, Vanguard Banner).

So fork (a) attacks the *consequence* instead of the *rule*, three ways.

### 3.3 `A-2` — THE GREEN-PLATE CENSUS · `F-AC-3` GRADED AS WRITTEN, THEN **QUARANTINED**

362 frames at 2.0 fps over `[683.0, 864.0]`, `bars.find_bars` imported **unchanged**, the only
change being the mask and the removal of `pbar`'s player x-gate.

| quantity | `green_mask2` | `green_mask` |
|---|---:|---:|
| frames sampled | 362 | 362 |
| frames with the **player's** plate | **331 (0.9144)** | 13 (0.0359) |
| off-centre green detections | **210** | 144 |
| frames carrying ≥ 1 | **95** | 73 |

`F-AC-3`'s population non-emptiness clause: 331 ≥ 181 required. **The detector is live.** `P-4`
**PASSES**. Criterion as written: `n_frames_with_offcentre_green = 95 ≥ 1` ⇒ **`F-AC-3` grades
DECISIVE-POSITIVE**, and `P-3` **PASSES**.

> ⚑ **AND IT IS WRONG.** See `D-AC-2` (§ 6). Direct visual inspection of the two densest frames
> shows the detections are **green VFX plumes**, and the white text satisfying the gate belongs to
> **neighbouring RED nameplates** — `evidence/crop-700-cluster.png` and
> `evidence/crop-702-cluster.png` show red bars with their own `(33,313/43…)` / `(32,564/42,798)`
> tokens sitting over a green lightning plume. **`F-AC-3`'s functional cannot separate a friendly
> nameplate from a green VFX run standing under a red plate's text.** The grade stands as written
> and the *inference* is quarantined: **`F-AC-3` may not be cited as evidence that friendly plates
> are green.**

### 3.4 `A-2b` — THE PERSISTENCE DISCRIMINATOR · GRADED AS WRITTEN, THEN **ALSO QUARANTINED**

Post-hoc repair leg, declared as such. 20 bursts × 15 consecutive 60 fps frames, gate `30.0` gpx
(`d1b.track`'s own default, imported by identity), three populations in the **same** frames:

| population | role | persisted / tested | persistence |
|---|---|---:|---:|
| RED plates | REFERENCE | 1883 / 2319 | **0.8120** |
| player-gated GREEN | **positive control** | 271 / 278 | **0.9748** |
| off-centre GREEN | under test | 33 / 69 | **0.4783** |

Positive control ratio 1.2005 (passes). Test ratio **0.5890 ≥ 0.50** ⇒ verdict as written
**REAL-ENTITY-POPULATION**.

> ⚑ **AND IT IS ALSO WRONG.** See `D-AC-3` (§ 6). Burst 2 (`t = 701.0`) alone contributes
> **20 of the 69** tested detections at 17/20 persistence — and burst 2 is the *same* green plume
> at `t ≈ 702` that I had already refuted by eye. **A slow VFX plume persists across 0.25 s just as
> a nameplate does.** Persistence separates *frame-local noise* from *anything durable*; it does
> not separate a plume from a plate. Quarantined.

### 3.5 `A-2c` — THE ADJUDICATION THAT ACTUALLY DECIDES: **EYES ON PIXELS**

Both pixel-statistic criteria failed, so the question was answered by direct inspection, which is a
**measurement** (observation), not an estimate. The 210 `green_mask2` off-centre detections were
sorted by time and every 13th taken — **16 tiles spread across all ten waves**, cropped at native
resolution and inspected (`evidence/strip-green-0..3.png`, `evidence/contact-offcentre-green.png`;
per-tile verdicts and bases in `pm4ac_green_adjudication.csv`).

> ⚑ **16 of 16 are VFX plumes or the green objective-tracker UI text (`"…all Enemies"`). NOT ONE
> IS A NAMEPLATE.** Not one shows the geometry every genuine plate shows: a flat saturated run
> inside a fixed ~72 px frame with a dark depleted remainder and its **own** white `(cur/max)`
> token centred on it. The contrast is measurable as well as visible — at `t = 702.0` the player's
> own green bar has a text-centroid offset of **−1.1 px** from its frame centre, while the two
> off-centre green candidates sit at **−72.7** and **−30.8 px**; the player's bar block is at
> luminance 178 against a background of 83, while the candidates are 75.5 vs 71.2 and 93.9 vs 93.2
> — **no bar-to-background contrast at all**.

**Consequence, stated exactly:** in this footage **the green channel carries the player's plate and
nothing else that survives inspection**. Note the direction — this does **not** establish that GD
draws friendly plates red. It establishes that *no green non-player nameplate was drawn*, which is
equally consistent with "friendlies are red" and with "friendlies carry no plate here".

### 3.6 `A-3` — THE EMPLACEMENT SIGNATURE IN THE **RED** POPULATION · **MEASURED NEGATIVE**

An emplacement is world-stationary for its whole life. Over the 6,336 tracks (§ 4.1):

| quantity | value |
|---|---:|
| tracks meeting **both** halves (dur ≥ 8.0 s **and** net world displacement ≤ 40.0 gpx) | **0** |
| ⚑ tracks meeting the **duration** half alone | **24** |
| minimum net world displacement among those 24 | **72.09 gpx** |
| ⚑ tracks meeting the **displacement** half alone | **3,412** |
| maximum duration among those 3,412 | **4.5 s** |

> ⚑ **THE POPULATION IS NON-EMPTY ON BOTH HALVES, SO THE ZERO IS A MEASUREMENT AND NOT A CAPTION**
> (`R-PM4-72 part 4`; `D-I27-2`'s lesson applied by the next seam one lap after it banked).
> Twenty-four tracks were long enough to be an emplacement and every one of them moved at least
> 72 gpx; 3,412 tracks were still enough and none lasted past 4.5 s. **`P-12` FAILS** — and it
> fails informatively: **no fixed emplacement is inside the counted population.**

### 3.7 `A-3b` — THE **MOBILE**-PET SIGNATURE · **MEASURED NEGATIVE** (post-hoc, declared)

Leg A-3 can only see fixed things. A red-plated *pet* follows its owner and would be a long-lived
track resident at the ring. Of the **84** tracks with duration ≥ 4.0 s (population non-empty):

| quantity | value |
|---|---:|
| tracks with ring fraction ≥ 0.50 | **7** |
| **maximum** ring fraction | **0.7299** (`W157-T010`, 6.85 s lifetime, 5.00 s in ring) |
| next four | 0.7267 (5.18 s) · 0.6731 (4.33 s) · 0.6518 (4.50 s) · 0.5586 (5.40 s) |
| longest track in the whole fight | **17.10 s** |

Every one of the seven is a few seconds long and then gone — the signature of a monster that closed,
fought and died, not of a summon that accompanies its owner across a 181 s fight. **No track in this
footage carries a persistent-pet signature.** ⚑ **BOUND, NEVER IDENTIFICATION** — pixels cannot name
a body (NOTE-9), so this leg may say *"nothing behaves like a pet"* and may never say *"this track
is / is not a pet."*

### 3.8 ⚑ THE FORK (a) VERDICT, IN THE PRE-REGISTERED GRAMMAR, NAMING ITS QUANTITY / POPULATION / CLOCK

The prereg offered three outcomes. The measured answer does not fit one of them cleanly, and it is
reported that way rather than rounded into the nearest box:

- **Counting rule: DECODED** (§ 3.1). Quantity: a per-instant count of red-masked, text-gated
  nameplate bars. Population: whatever GD draws a red plate for, on screen, unoccluded. Clock: the
  60 fps frame grid of the referent capture, restricted to the 10,216 instants carrying a player
  plate.
- **Colour rule: UNDECIDABLE from the artifacts this run holds** — `UNREACHED-AC-1`. Obstacle: the
  plate-colour rule for player-allied entities is decoded by no `.arz` record, no disassembly and
  no pinned artifact in this run; the green channel is empirically empty of non-player plates, which
  is consistent with *both* remaining readings.
- **⚑ SUMMON TERM: MEASURED-NEGATIVE.** Whatever the rule is, **no body behaving like the
  referent's summons is inside the counted population** — 0 of 24 duration-qualifying tracks is
  stationary (§ 3.6), 0 of 84 long tracks is ring-persistent beyond 0.73 for 6.85 s (§ 3.7), and 16
  of 16 adjudicated green detections are not plates (§ 3.5).

**Therefore, on the axis `NAMED-I27-1` raised: the bracket is like-for-like with a count that
contains no summons.** It is **not** a pet-inclusive count in effect. Stated in the strongest form
the evidence supports: *the referent occupancy bracket carries no measurable summon term, so the
run's movers-only quoting is not comparing a movers-only sim figure against a summon-inflated
referent figure.* ⚑ **The definitional question — whether GD's plate rule would have included a
summon had one been at the ring — stays `UNREACHED-AC-1`, and no ruling on the run's definition of
record is issued or implied from my seat.**

---

## 4 — FORK (b) · REFERENT MONSTER RING-RESIDENCE

### 4.1 The tracking, and the obstacle measured before any residence number

`d1b.world` and `d1b.track` are imported **BY IDENTITY** from the pinned Lap H-2 tracker; `d1b.load()`
(which reads `/tmp`) is never called; nothing is re-implemented. Tracking runs per contiguous wave
window. **No minimum-track-length filter is applied** — `d1final.py:8` drops tracks under 1.0 s,
which is right for a locomotion taxonomy and wrong for a residence census, and the divergence was
declared in the prereg in advance.

| quantity | value |
|---|---:|
| monster plate-instants tracked, `[683.0, 864.0]` | **97,527** (asserted equal to the census's own count — the guard that caught `D-AC-1`) |
| instants with a detected player plate | **10,216** |
| tracks | **6,336** |
| track duration: median / p75 / p90 / p95 / max | **0.1166 / 0.400 / 1.083 / 1.900 / 17.100 s** |
| tracks ≥ 1 s / ≥ 2 s / ≥ 4 s / ≥ 8 s | 692 / 295 / **84** / **24** |

> ⚑ **THE OBSTACLE, COUNTED RATHER THAN ASSUMED.** Of 97,426 monster plate detections tested,
> **77,200 have a successor within the tracker's own 30 gpx gate one frame later: continuity
> `0.7924`.** Roughly **one plate detection in five simply is not there in the next frame.** That is
> the identity-continuity ceiling of the entire pinned pipeline, and it governs everything below.
> Track count is therefore an **UPPER** bound on bodies and track duration a **LOWER** bound on
> body lifetime.

### 4.2 The ring predicate and `F-AC-1` — **the gate that licenses the rest of fork (b)**

The predicate is the audited instrument's own, verbatim in form (`pm4r_contact…py:74-75`), at the
pinned three-rung 2.400 m bracket. `F-AC-1` asks whether my per-body decomposition puts back exactly
the occupancy the pinned instrument reports.

| rung `R_gpx` | `L_recon` (mine) | `L_pinned` (`913a57a3…20e6`) | relative deviation |
|---:|---:|---:|---:|
| 285.7 | 3.242169 | 3.2423 | **−0.000040** |
| **293.6** *(primary)* | **3.351899** | **3.3519** | **−0.0000004** |
| 300.0 | 3.425117 | 3.4251 | **+0.000005** |

Window: the 10,216 player-plate instants — the audited instrument's own population, not a superset.
Functional: `Σ n_frames / N_obs` in bodies, against `mean_occupancy` in bodies. Non-emptiness:
`N_obs = 10,216 ≥ 10,000` and 10,205 intervals ≥ 50. Tolerance 0.05.
**`F-AC-1` PASSES at all three rungs, by three to five orders of magnitude.** `P-5` **PASSES**.

⚑ This is a fidelity gate on **my** instrument against **my own lap's** pinned artifact. It is not a
sim comparison and issues no sim verdict. It licenses fork (b): the decomposition loses no body-time.

### 4.3 ⚑ `UNREACHED-I27-1`'s three pins — what this lap fills

| pin | disposition |
|---|---|
| per-body referent ring-**entry** time | ⚑ **FILLED** — `t_entry` for 10,205 intervals over **3,296 distinct bodies** at the primary rung, ±1 frame, censor-flagged, in `pm4ac_ring_intervals.csv` |
| per-body referent ring-**exit** time | ⚑ **FILLED** — `t_exit` likewise; **309** of them with an *observed* crossing, the rest censor-flagged with the reason on every row |
| referent body **population** at the ring | ⚑ **RULED by fork (a)** — red-plated bodies, no measurable summon term (§ 3.8); per-wave in-ring body counts in § 4.6 |

### 4.4 ⚑ THE RESIDENCE, PUBLISHED AS A **MEASURED LADDER**, NOT A SCALAR

Under 79.24 % continuity, one body's ring occupancy is chopped into pieces, and **how many pieces
depends entirely on how long an unobserved gap one bridges — a parameter no artifact decodes.** So
the answer is a ladder whose rungs are monotone by construction and whose ends are **both measured**.
At the primary rung `R = 293.6` gpx (all durations ±0.0167 s):

| rung | join | n | median | p75 | p90 | p95 | max | mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **A** — *pre-registered* | 0.05 s (`pm4r_contact…py:112`) | 10,205 | **0.0166** | 0.0500 | 0.1166 | 0.1833 | 3.3333 | 0.0478 |
| **B** — bridged *(post-hoc)* | 0.20 s = `d1b.track`'s own `maxgap=12` | 3,958 | **0.1000** | 0.3500 | 0.7666 | 1.1666 | 6.2167 | 0.2813 |
| **C** — track ring span *(post-hoc)* | whole track | 3,296 | **0.1334** | 0.4334 | 1.0500 | 1.5833 | **15.15** | 0.4189 |

- **Rung A is a LOWER bound** — detector dropouts split genuine residences into fragments.
- **Rung C is an UPPER bound** — it bridges everything inside one track, *including genuine
  exit-and-re-entry*.
- ⚑ **B and C were computed after seeing A's fragmentation and are labelled post-hoc everywhere.**
  Neither replaces the pre-registered functional. `0.20 s` is not a free parameter: it is the horizon
  beyond which the imported tracker itself refuses to assert identity.

Also published, a functional invariant to *within-track* fragmentation: **per-track ring body-time**
— median **0.0500 s**, p90 **0.3833 s**, max **7.25 s** over 3,296 bodies. And the ancestor's own
identity-holding sub-population (`d1final.py:8`'s ≥ 1.0 s filter, a **declared survivorship
selection**, not the answer): 522 tracks, ring span median **1.225 s**, p90 3.330 s, max 15.15 s;
ring body-time median **0.450 s**, p90 1.398 s.

All three 2.400 m rungs, and the separate `R = 150.0` gpx visual-abutment ring (**never pooled** with
the bracket — a different ring, not a sensitivity on the same one), are in
`pm4ac_residence.json :: residence_ladder`.

**Graded:** `P-6` **PASSES** (10,205 ≥ 300). **`P-7` FAILS** — median residence at rung A is
**0.0166 s**, far below the predicted ≥ 0.20 s. It fails for a reason the lap can name and did name:
rung A measures the detector's duty cycle as much as the body's dwell. **The failure is reported, not
re-worded** (`D-AB-3`'s lesson).

### 4.5 TRUNCATION HONESTY — mandatory, and it bites hard

At the primary rung, of 10,205 intervals: **10,138 (99.34 %) are censored on at least one side** —
9,818 left, 9,896 right, 2,643 carrying an internal unobserved gap, **30** touching a wave-window
boundary. **`P-8` PASSES** (> 25 % censored), by a margin that is itself the finding.

Right-censoring reasons, exhaustively: **`unobserved_gap_after` 7,006 · `track_end` 2,876 ·
`wave_window_end` 14.** The 67 fully-uncensored intervals are a **survivorship-selected**
sub-population (median 0.0334 s, p90 0.500 s, max 2.633 s) and are published as such, never as *the*
answer.

Named limits, published whether or not they bite:
1. **identity continuity 0.7924** (§ 4.1) — the dominant one;
2. **occlusion / VFX saturation / plate suppression** — absence never proves absence, so every
   residence is a truncated observation and every count a lower bound;
3. **large-bodied monsters** — plate high above the head ⇒ radial distance over-stated ⇒ residence
   under-counted;
4. **wave-window boundaries** — 9 internal cuts, **30** intervals touch one;
5. **player-plate coverage** — 0.8993–0.9765 per wave (§ 4.6); missing instants are **unobserved**,
   never imputed as out-of-ring;
6. **the 0.05 s gap-join can bridge a genuine exit-and-re-entry** — 2,643 intervals contain an
   internal gap and are flagged so the reader can bound it.

### 4.6 PER WAVE, at the primary rung

| wave | intervals | distinct bodies | observed instants | observed frac | median | p90 | total body-time |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | 650 | 212 | 870 | 0.9295 | 0.0166 | 0.1167 | 40.21 s |
| 152 | 631 | 247 | 955 | 0.9765 | 0.0166 | 0.1500 | 44.31 s |
| 153 | 388 | 167 | 836 | 0.9351 | 0.0167 | 0.1167 | 25.39 s |
| 154 | 1313 | 352 | 795 | 0.9331 | 0.0166 | 0.1000 | 58.29 s |
| 155 | 606 | 187 | 932 | 0.9588 | 0.0167 | 0.1250 | 36.95 s |
| 156 | 1116 | 358 | 1149 | 0.9480 | 0.0166 | 0.1166 | 57.39 s |
| 157 | 1328 | 414 | 1068 | 0.9223 | 0.0167 | 0.1000 | 81.02 s |
| 158 | 560 | 218 | 759 | 0.9731 | 0.0167 | 0.1167 | 33.64 s |
| 159 | 1859 | 583 | 1503 | 0.9525 | 0.0167 | 0.1167 | 113.65 s |
| 160 | 1754 | 558 | 1349 | 0.8993 | **0.0000** | 0.1000 | 79.96 s |

*(Wave 160's median of exactly 0.0000 s is not a typo and not a defect: more than half of its
intervals are single-frame, so `t_exit − t_entry = 0`. It is the fragmentation signature at its
sharpest and is left standing rather than smoothed. The per-track ring body-time functional, § 4.4,
is the one to read if a single-frame interval is unwelcome.)*

### 4.7 ⚑ WHAT FORK (b) DOES **NOT** DO

- It does **not** re-derive occupancy. The bracket is pinned and stays pinned; `F-AC-1` exists
  solely as a fidelity gate and is never a competing occupancy figure.
- It computes **no** sim comparison. `W` still has **no** referent-vs-sim grade, and this lap does
  not manufacture one. Referent per-body residence and gamora's `W` are the same *quantity* on
  different clocks over different populations measured by different instruments; placing them side
  by side in prose would be `D-CON-9`'s twin and is refused here as it was refused there.
  `R-PM4-72 part 3(i)` stands until the conductor rules otherwise.

---

## 5 — FORK (c) · THE EXIT-CHANNEL SPLIT

### 5.1 Alive vs dead — what the pins *can* and *cannot* resolve

Of the 10,205 intervals at the primary rung, **309 have an OBSERVED exit** (a detected plate at
`t_first_out` within 0.05 s). ⚑ **All 309 are `EXIT_ALIVE` BY CONSTRUCTION** — a non-right-censored
exit *requires* an observed plate at the exit instant, and a plate **proves** a living body
(`bars.py:14-15`). So the referent's observable ring exits are, with certainty at this resolution,
**bodies leaving the ring alive.**

The death signal lives in the 9,896 **unobserved** exits, and it cannot be cleanly extracted:
`track_end` accounts for **2,876** of them, which is *consistent with* death (corpses carry no
nameplate, `OBS-H2-1`) and equally consistent with occlusion, plate suppression, screen exit or a
tracker identity break. **`DEATH` is never claimed — only `DEATH-CANDIDATE`.** Two bounds are
emitted: **0** of the 309 observed exits occurred within 120 px of a frame edge (screen exit is not
confounding the observed set), and **197 of 309 (0.6375)** have their track ending within 1.0 s of
the exit. Under the prereg's § 5.1 abort rule the *alive/dead split* is therefore declared
**UNREACHED** for want of a death discriminator, and only the counterfactual partition is published
— which is what § 5.2 does.

### 5.2 ⚑ THE COUNTERFACTUAL PARTITION — *who moved?*

For each observed exit, with `t_i` the last in-ring instant and `t_e` the first out-of-ring instant,
in the world frame (screen minus cumulative camera translation), buckets are exhaustive and mutually
exclusive. At `R = 293.6` gpx, join rule A:

| bucket | n | share of 309 observed exits |
|---|---:|---:|
| **`MONSTER_SUFFICIENT`** (monster's motion alone carries the crossing) | **136** | 0.4401 |
| **`PLAYER_SUFFICIENT`** (player's motion alone carries it) | **99** | 0.3204 |
| `EITHER_SUFFICIENT` | 40 | 0.1294 |
| `NEITHER_SUFFICIENT` (only the joint motion crosses) | 34 | 0.1100 |

**`F-AC-2`:** window = all primary-rung intervals over `[683.0, 864.0]`, observed exits only;
functional = `share_player = PLAYER/(PLAYER+MONSTER)` with `EITHER_`/`NEITHER_` published separately
and **never folded in to move the number**; non-emptiness = decidable population **235 ≥ 30**.
`share_player = 0.4213 ≥ 0.20` ⇒ **`F-AC-2` PASSES**. `P-9` **PASSES**, `P-10` **PASSES**.

**Robustness across all six rung × join-rule combinations** (none of which was used to choose the
criterion — it was fixed in the prereg):

| join | R=285.7 | R=293.6 | R=300.0 |
|---|---:|---:|---:|
| A (0.05 s) | 0.4070 *(258 dec.)* | **0.4213** *(235)* | 0.4562 *(217)* |
| B (0.20 s) | 0.3439 *(570)* | 0.3695 *(525)* | 0.3967 *(489)* |

**The band is 0.344–0.456 and every cell passes.** The partition is not an artefact of the rung or
of the join rule.

### 5.3 Player displacement at exits — context, never a substitute

Smoothed player ground speed (`pm4r_lib.rolling_median` form, `SMOOTH_FRAMES = 9`, imported by
identity), in ±0.125 s about each exit versus fight-wide over the same instants:

| | n | p25 | median | p75 |
|---|---:|---:|---:|---:|
| at the 309 observed exits | 309 | 268.97 | **434.98** | 511.37 |
| fight-wide | 10,861 | 215.65 | **402.95** | 510.38 |

Ring exits happen while the player is moving **somewhat faster than his own typical**, most visibly
at the low end (p25 rises 215.65 → 268.97 gpx/s): exits are under-represented among the referent's
slowest moments. ⚑ **Units are ground px/s and are NOT converted** — the metre anchor is Lap H-2's
declared gap `OBS-H2-9` and travels as a bracket, never a scalar. ⚑ **No causal claim is made**; the
partition in § 5.2 is the measurement, this table is context.

### 5.4 ⚑ WHAT FORK (c) MAY AND MAY NOT BE CITED FOR

**May:** *"At this resolution, displacement is a materially present ring-exit channel in the
referent: the player's own motion alone suffices to explain 99 of 235 decidable observed exits,
0.4213, robust across rungs and join rules."*

**May NOT:** any comparison whatever to I-27's sim-side displacement shares. Different instrument
(nameplate tracking vs an event ledger), different clock (60 fps video vs sim scans), different
predicate, different population, different definition of "displacement". `R-PM4-72 part 4` forbids
it outright, and this lap does not compute it, quote it, or gesture at it.

---

## 6 — DEFECT TABLE (all mine · all self-caught · all disclosed **before** any claim rested on them)

| id | defect | disposition |
|---|---|---|
| **`D-AC-1`** | `d1b.track`'s window test is `t0-1e-6 <= t <= t1+1e-6` — **inclusive at both ends** — so instants landing exactly on a wave boundary were tracked in **both** adjacent waves and **16 plate-instants were double-counted** (97,543 vs the census's 97,527) | ⚑ **Caught by my own pre-registered conservation assertion, which fired and halted the run before a single number printed.** The imported tracker is **NOT modified**; the *window handed to it* was made half-open (`WAVE_END − dt/2` for waves 151–159, `FIGHT_T1` for 160) — a caller-side choice, not an instrument change. Verified: 97,527 exactly |
| **`D-AC-2`** | ⚑ **THE BIG ONE.** `F-AC-3`'s functional counts *green bar detections*, and a **green VFX plume** standing under a **red** plate's white `(cur/max)` token satisfies every clause of `bars.find_bars` including the text gate. The criterion graded **DECISIVE-POSITIVE** on 210 detections across 95 frames — a clean, wrong "friendly plates are green" | ⚑ **Refuted by my own evidence before publication**, `evidence/crop-700-cluster.png` / `crop-702-cluster.png`. The grade **stands as written**; the *inference* is **QUARANTINED** and the criterion is explicitly not citable for the verdict (§ 3.3). Repair legs `A-2b` and `A-2c` were built in its place |
| **`D-AC-3`** | the repair leg `A-2b`'s persistence discriminator **also** graded positive (`REAL-ENTITY-POPULATION`, ratio 0.589) — and **20 of its 69 tested detections come from burst 2 at `t = 701.0`, the very plume already refuted by eye.** Persistence separates frame-local noise from anything durable; **a slow VFX plume is durable** | ⚑ Disclosed and **QUARANTINED** the same way. Its failure is *why* § 3.5 exists: two independent pixel statistics both said "real" and both were wrong, so the question was settled by direct adjudication instead. **A repair that reproduces the original defect's blind spot is a second defect, not a fix** |
| **`D-AC-4`** | `pm4r_lib.PLAYER_SCREEN = (958, 544)` and `d1b.PX_S/PY_S = (960, 544)` disagree by 2 px — two pinned artifacts of this run carrying different player-screen anchors | declared in the prereg **in advance** (§ 8.1 note 4). Neither enters: the ring predicate uses the **per-instant detected player plate anchor**, exactly as the audited instrument does. Recorded, does not propagate |

> ⚑ **The pattern worth banking: `D-AC-2` and `D-AC-3` are the same defect twice.** I built a
> criterion that could not see the confound, then built a *repair* that could not see it either,
> and only direct observation broke the loop. The guard that worked was the one that did not run on
> statistics at all. `D-AC-1`, by contrast, was caught by a conservation identity asserted in the
> pre-registration — which is the cheapest guard in this lap and the only one that fired
> automatically.

---

## 7 — PRE-REGISTERED PREDICTIONS, GRADED **WORDING-UNCHANGED**

| # | prediction | grade | evidence |
|---|---|:-:|---|
| **P-1** | counting population decodable entirely from artifacts (2)–(6), no undisassembled consumer | **PASS** | § 3.1, ten byte-cited steps |
| **P-2** | population is red-masked bars with a white text token; colour is the sole discriminator | **PASS** | `bars.py:43` default, `bars.py:101` |
| **P-3** | ≥ 1 green detection outside the player x-gate in the 363-frame sample | **PASS** | 210 detections / 95 frames — ⚑ **and see `D-AC-2`: passing this prediction did not mean what it was written to mean** |
| **P-4** | player's green plate detected in ≥ 50 % of sampled frames | **PASS** | 331/362 = 0.9144 |
| **P-5** | `F-AC-1` passes at all three rungs within 5 % | **PASS** | max deviation 4.0 × 10⁻⁵ |
| **P-6** | ≥ 300 ring intervals at `R = 293.6` | **PASS** | 10,205 |
| **P-7** | median residence (all intervals, `R = 293.6`) ≥ 0.20 s | **FAIL** | 0.0166 s at rung A — reported as failing, not re-scoped (§ 4.4) |
| **P-8** | > 25 % of intervals censored on at least one side | **PASS** | 99.34 % |
| **P-9** | `F-AC-2`'s decidable population non-empty and ≥ 30 | **PASS** | 235 |
| **P-10** | `PLAYER_SUFFICIENT` exits present (≥ 1) | **PASS** | 99 |
| **P-11** | at least one leg returns UNREACHED with an obstacle named | **PASS** | six (§ 10) |
| **P-12** | ≥ 1 world-stationary red track meeting both thresholds | **FAIL** | 0 — informatively (§ 3.6) |

**10 PASS / 2 FAIL.** Both failures are reported in the words they were registered in.

---

## 8 — DETERMINISM AND METHOD

Three instruments, each run **twice**; **all nine emitted artifacts byte-identical across both
legs**, verified by digest comparison against a snapshot of leg 1. No stochastic element exists in
any leg (leg A-2b's burst starts are the arithmetic sequence `683.0 + k·9.0`; no seed is drawn
anywhere). `bars.py` and `d1b.py` are imported **unchanged**; the ring predicate is
`pm4r_contact_2026_08_14.py:74-75` verbatim in form; every constant in § 2 of the prereg carries a
`file:line` provenance. Prior-lap numbers enter **only** through emitted artifacts with digests
asserted, never from prose (`R-PM4-67 part 2` / `D-CON-6`).

---

## 9 — ⚑ DO-NOT BLOCK (binding on every downstream lap and fold)

1. **DO NOT** cite `F-AC-3`'s DECISIVE-POSITIVE, or leg `A-2b`'s REAL-ENTITY-POPULATION, as evidence
   about nameplate colour. Both are **quarantined** (`D-AC-2`, `D-AC-3`). § 3.5's adjudication is
   the sentence to quote.
2. **DO NOT** state that Grim Dawn draws friendly nameplates red, or green. **The colour rule is
   `UNREACHED-AC-1`.** What is measured is that *no green non-player plate was drawn in this
   footage* and that *no summon-shaped body is in the counted population* — three different claims.
3. **DO NOT** quote a single residence scalar for the referent. § 4.4's **ladder** is the finding:
   rung A is a LOWER bound, rung C an UPPER bound, and the bridging parameter is undecoded. Quoting
   rung A alone under-states residence; quoting rung C alone over-states it.
4. **DO NOT** compare any number in this lap to any sim quantity — most especially not fork (b)'s
   residence to gamora's `W`, and not fork (c)'s `share_player` to I-27's displacement shares.
   Different instruments, clocks, predicates and populations (`R-PM4-72 parts 3-4`). ⚑ `W` still has
   **no** referent comparator; this lap deliberately did not create one.
5. **DO NOT** read fork (c)'s 309 observed exits as "the referent's exits". They are the **observed**
   0.030 of 10,205 — the other 9,896 are censored, and the alive/dead split among them is
   **UNREACHED**. The 309 are alive-exits **by construction**, which is a selection, not a finding
   about mortality.
6. **DO NOT** treat any count in this lap as anything but a **LOWER BOUND**. Plate presence proves a
   living body; **absence never proves absence** (`bars.py:12-15`, NOTE-9). Identity continuity is
   **0.7924**, not 1.
7. **DO NOT** pool the `R = 150.0` gpx figures with the three 2.400 m rungs. It is a **different
   ring** (Lap H-2's visual melee abutment), reported separately by design, never a sensitivity on
   the bracket.
8. **DO NOT** convert any ground-pixel quantity in this lap to metres on a single anchor. `OBS-H2-9`
   is an open declared gap and the three-rung bracket governs (`R-PM4-70`: brackets stay brackets).
9. **DO NOT** use track counts as body counts. 6,336 tracks is an **UPPER** bound on bodies
   (fragmentation) and 3,296 "distinct bodies with ring time" inherits that bound exactly.
10. **All prior DO-NOT blocks are carried unchanged** — Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 ·
    Lap X § 12.2 · Lap Y § 11.6 · Lap Z § 5 · Lap AA § 6 · **Lap AB § 9 (all ten)**. In particular
    **Lap AB DO-NOT 9**: `pm4u_arrivals.csv` is a strict upper bound (`D-U-3`) and **this lap did not
    open it, cite it, or compute any referent `λ` from it.**

---

## 10 — UNREACHED CENSUS (obstacle named on every one)

| id | what | obstacle |
|---|---|---|
| **`UNREACHED-AC-1`** | Grim Dawn's nameplate **colour rule for player-allied entities** | decoded by no `.arz` record, no disassembly and no pinned artifact in this run; the green channel is empirically empty of non-player plates, which is consistent with *both* remaining readings ("friendlies are red" and "friendlies carry no plate here") |
| **`UNREACHED-AC-2`** | the **alive-vs-dead** split at ring exit | all 309 observed exits are alive **by construction**; the death signal lives in the 2,876 `track_end` censorings, where plate loss is equally consistent with death, occlusion, plate suppression and tracker identity break. `0.6375` of observed exits have their track end within 1 s — over the prereg's 0.35 abort threshold, so the split is declared UNREACHED rather than estimated |
| **`UNREACHED-AC-3`** | the **bridging horizon** for a per-body ring interval | no artifact decodes how long an unobserved gap belongs to the same residence; the ladder (§ 4.4) publishes bounds instead of choosing |
| **`UNREACHED-AC-4`** | the **true body count** at the ring | 6,336 tracks over 97,527 plate-instants under 0.7924 continuity is an upper bound on bodies; the pinned census carries no body identity token (the `(cur/max)` text is emitted only as a **pixel count**, `extract.py:48`, never parsed) |
| **`UNREACHED-AC-5`** | whether the four purchased **emplacements are ever on screen** | leg A-3's negative cannot separate "not in the counted population" from "never in frame"; the arena's defence-site positions are not pinned by any artifact in this run (and Lap AA DO-NOT 5's arena-identity UNREACHED bounds it further) |
| **`UNREACHED-AC-6`** | per-body ring residence at **full track identity** | the tracker's 30 gpx / 12-instant horizon; a body whose plate drops for > 0.2 s becomes a new track |
| carried in | `UNREACHED-AB-1/2/3/4/5/6`, `UNREACHED-AA-2`, `UNREACHED-T1`, `UNREACHED-S4`, `UNREACHED-U1`, `NAMED-AA-1`, `NAMED-AB-1/2`, `OBS-H2-9`, `UNREACHED-I27-2` | unchanged by this lap |

**NAMED, not decoded** (`R-PM4-56 part 4`): **`NAMED-AC-1`** — the **green objective-tracker UI
band** (`"Objectives / Eliminate all Enemies"`), a screen region that lies **outside** all four
`extract.py:HUD` rectangles and emits green bar-shaped runs with white text above them. It is named
here because it contaminated leg A-2 and would contaminate any future green-channel work on this
footage; it is **not** decoded, and no HUD rectangle is amended from my seat (that would silently
change a pinned instrument's output).

---

## 11 — WHAT THIS LAP DID NOT DO (the firewall, stated)

1. No simulation cell, code, telemetry, record or artifact was opened by any leg.
2. No sim grade, ratio, deficit or comparison was computed anywhere.
3. Nothing here elects, ranks, designates or recommends (`R-PM4-27 part 3`).
4. The standing occupancy residual is **not** re-quoted, re-based or amended; the definition of
   record stays exactly where `R-PM4-72 part 5` left it. Fork (a) reports the referent's side of
   `NAMED-I27-1` and **routes** it; it does not rule it.
5. No metre quantity is published on a single anchor.
6. `W` acquires **no** referent comparator by side-by-side placement anywhere in this prose.
7. No pinned artifact was modified. `bars.py`, `d1b.py`, `pm4r_contact_2026_08_14.py` and the
   nameplate census are byte-identical to their pinned digests after this lap as before it.

---

## 12 — ARTIFACT DIGESTS (full 64-hex sha256, ⚑ **computed AFTER the final write**, `D-AA-5`)

### 12.1 Emitted by this lap

See `pm4ac_digests.json` — the artifact the conductor should re-hash. It carries every emitted file
and every pinned input. Its own digest is not self-referential and is reported to the conductor with
this findings file's digest.

### 12.2 Asserted EXACT at every instrument start (HALT on mismatch)

| artifact | sha256 |
|---|---|
| `prereg.md` (this lap, committed ALONE at `38fb3120`) | `da1fae161096b6299b56c784394d5967910aa4a0862e9825a303bb762e466bc5` |
| `pm4r_contact_occupancy.csv` (**the bracket**) | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` |
| `plates60_lapH2.npy` (the census) | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` |
| `pm4r_contact_2026_08_14.py` (instrument under audit) | `8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7` |
| `pm4r_lib_2026_08_14.py` | `630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b` |
| `bars.py` (the detector) | `2ecfc75543d9498aa81f8d7b733d5f7eca2b7009a2ca7bbd834dffd10258e7e0` |
| `extract.py` (the producer) | `36f7f923501a7ddd4dccfad7e8fd2e688f8ee53e0647989a68e67ba6dea6b36d` |
| `d1b.py` (the tracker) | `c26388071e127a0fb8e8420bb4ae151a6a678d444848c67d84cbd445034b876f` |
| `d1run.py` | `2cebdc5df62979d0d7d208c1aaf7274c02ff2540ea8e7b44efcff9f61dbdf8c5` |
| `d1final.py` | `d9e296eee4e4324b210332b76fe978cf36f5ccc5e657f0ade327e1f940078519` |
| `d2.py` | `0366a39faf9586b11278118ba19c50e7d89c2bd49b03643b21ec6ef8a0fc0cd2` |
| `camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` |
| `pm4h2_tracks.csv` | `13bb3033cb35012846343dcb077902304eb163a92cb8f7423ba8cf8074563818` |
| `pm4h2_ring_density.csv` | `a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5` |
| `pm4ab_findings.md` (DO-NOT block source) | `a0279b1122c4de476e540a0bc34425c68e519a16d667a06abc2964a1675f07ba` |
| referent MP4 (**RECORD-class, pinned here for the first time**) | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` |

---

## 13 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. **`NAMED-I27-1`'s referent side is answered on the axis that matters and left open on the axis
   that does not.** The bracket carries **no measurable summon term** (§ 3.8), so the run's
   movers-only quoting is not a like-for-like violation *in effect*. Whether the definition of
   record should change is the conductor's, and nothing here presses for it.
2. **`UNREACHED-I27-1` closes two of three pins and the third is ruled** — but the residence pin
   closes as a **ladder**, not a scalar, and any future grade against it must declare which rung it
   is grading against, or it is not evaluable (the `D-AB-3` functional clause, applied to my own
   output).
3. **The exit-channel convergence is worth noting and is not mine to draw.** Fork (c) measures that
   the referent's own ring exits are, in 99 of 235 decidable cases, explicable by the player's motion
   alone. `R-PM4-72 part 2` routed the sim's displacement finding to the *pursuit-during-player-motion*
   seam. Whether these two facts belong in the same sentence is a conductor ruling, and § 9 DO-NOT 4
   forbids me from writing it.
4. **A cheap next pin exists if the conductor wants `UNREACHED-AC-1` closed:** the `(cur/max)` text
   is *rendered on screen* and `extract.py:48` throws it away as a pixel count. OCR-ing it would give
   a per-body identity token, which would collapse `UNREACHED-AC-4` (body count) and `UNREACHED-AC-6`
   (identity horizon) at once — and a friendly's max-HP value would be distinguishable from the
   tier-16 roster's decoded HP band. I name the lane; I do not open it.

---

*Lap AC executed by legolas (`UNKNOWN-RESEARCHER`), 2026-08-16. Referent-side only. Zero HALTs.*
