# S2 MINTED GATE — standing procedure + tranche-1 scorecard

**STATUS:** COMPLETE — verdicts rendered
**Date:** 2026-08-24
**Author:** galadriel (visual perception + UX-similarity steward)
**Authority:** dispatch `2026-08-24-galadriel-s2-minted-gate.md` (Matt-approved; jack-ryan Gate-1 PASS-WITH-FINDINGS, amendments applied)
**Judge-From:** `reincarnated-godot/harness_logs/s2a_2026-08-24-final/` — 156 PNG @ 1920×1080, ratified camera, godot `c6eede0`
**Judge-To:** P3 selection-gate corpus (`galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` + delta), `framesets.json` v2
**Receipts:** `galadriel/reports/s2-gate-2026-08-24/*.json` · instruments `galadriel/pipeline/s2_gate_measure.py`, `s2_gate_colour.py`

---

## 0. Instrument discipline (method note, written before analysis)

Scoring is **numeric-primary**. Every figure below is **re-derived by me from the PNGs**, not read from
`render.txt` or `gate.json`. Where my number and the mint note's number disagree, both are shown and the
disagreement is adjudicated. A gate that restates the builder's arithmetic is a rubber stamp.

**Isolation method.** Authored pixels are isolated by differencing an arm against its **matched control at
the same mark**. That method is only legal if the control is pose-identical, so I verified the claim rather
than inheriting it:

> **Determinism, verified independently:** fx-arm minus `melee_ctl` = **exactly 0 lit px** at both `00-pre`
> and `08-post`, on all five melee arms. drax's stage-clock fix holds. Every control-difference below is licensed by this.

**Threshold.** "Lit px" = pixels where summed `|ΔRGB|` vs control > 12. Where a threshold could drive a
conclusion, I sweep it rather than trusting one cut (see § 2.3.4).

---

## 1. THE STANDING PROCEDURE — applies to all 24 rows

### 1.1 The § 3.2 three-axis rubric

Every row gets **R (readability at our gameplay camera) · P (parameterizability) · S (style-register fit)**,
each 1–5, each with a receipt naming the specific measurement. No score ships without its receipt.

| Axis | Primary instrument | Bars |
|---|---|---|
| **R** | lit-px coverage vs C-5 band · contrast against stage · temporal legibility across marks | fails at **both** ends (§ 1.6) |
| **P** | **geometric invariance under recolour** — centroid / bbox / radius spread across element arms; plus CIEDE2000 separation | recolour must move colour and **only** colour |
| **S** | HLF vs the 1.5 % register-2 gate **where the stage permits it** (§ 1.9) | register A, dark-mood, lighting+particles carried |

### 1.2 The L-19 causality check — scored PER ROW AGAINST ITS DECLARED CLASS

Matt's criterion of record (spec § 1.1, verbatim):

> *"the diablo franchise does a great job of making it feel more real as a plausible physical manifestation of exceptionally rapidly spinning weapons, clashing into flesh, bone and armor, whereas the Grim Dawn EOR Warlord's artistic rendering of the same move feels more like a generic magical aura that happens to be spinning along with the character."*

**This criterion is NOT a uniform preference for physical reads.** `aura` and `self_buff` are `magical-cause`
**and that is CORRECT**. Scoring an aura down for being decorative applies the criterion where it does not
live. **This is the single most likely way for this gate to go wrong and it is stated here so it cannot be
drifted into.**

**The operational test, made a number.** The EoR failure mode is precise: *an effect that expands, leaves a
mark on the ground, and never touches the bodies it passes through.* That decomposes into three measurables:

1. **Expansion** — does the authored bbox / r99 grow across the effect's life, or stay bounded to its cause?
2. **Ground mark** — do authored pixels **persist** after the action completes? (a decal persists; a burst returns to zero)
3. **Body contact** — **what fraction of the frame's body pixels does the effect illuminate, and does that fraction spike at the contact instant?**

Test (3) is the load-bearing one and it is the inverse of how it is tempting to measure it. Do **not** ask
"what % of the effect is on a body" — bodies are small on our camera, so that ratio is small even for a
perfect hit. Ask **"what % of the body does the effect light, and when."** A `physical-cause` effect shows a
**step change at contact**. A decorative one shows a flat line.

**For `magical-cause` rows, test (3) is inverted and used as an anti-tamper check:** the effect **should
NOT** spike at contact. A magical field that suddenly acquires contact response has had physical-causality
tells smuggled into it to flatter the score — which corrupts precisely the rows that calibrate the rubric.

### 1.3 RT-2 — the surface-class check (spec § 6.1) — **and the instrument correction it needs**

RT-2 fires when a **`TRAIL-BOUNDED`** row's element variants read **indistinguishable at the gameplay
camera**. Converse outcome: a variant that has **lost its physical read** ⇒ the class held and the tint was
over-expanded. Both are results; neither is a gate failure.

> **⚑ STANDING INSTRUMENT CORRECTION — hue-angle separation must NOT be used to adjudicate RT-2.**
>
> **Hue angle is undefined at zero chroma and numerically unstable near it.** `melee_strike`'s `neutral`
> variant renders at **C\* = 2.83** — a near-achromatic cream. Its "hue" is a division by a chroma of
> ~5/255; any pair involving it yields a separation that is an **artifact of the metric**, not a statement
> about whether a player can tell two trails apart. Two variants can be trivially distinguishable while
> sharing a hue angle (cream vs saturated orange = same hue, obviously different), and can share a hue
> angle while differing in lightness.
>
> **Use CIEDE2000 in CIE L\*a\*b\***, which carries lightness + chroma + hue together. Measure on **rendered
> pixels** (what the player sees), and report **added light** alongside (did the tint take).
>
> This correction is not cosmetic — applied to tranche 1 it **moves which pair is the minimum** (§ 2.1.3).

**The RT-2 fork must be decided on transfer function, not on authorship.** The question "does a collapse
indict the *surface class* or the *palette*" has a decisive test:

> **Compare ΔE(rendered) against ΔE(added) pairwise.** If the surface is the culprit, rendered separation is
> **systematically compressed** relative to what the palette supplied. If rendered ≈ added, the surface is a
> **faithful transmitter** and cannot be blamed for what it transmits — the palette is indicted.

This replaces "these are two pastels I authored" (an argument from intent, which a gate cannot verify) with
a measurement the gate owns.

### 1.4 RT-6 — `vortex_pull` is NOT scored on VFX alone

Not in this tranche. **Baked in here so it cannot be forgotten when the row arrives:** `vortex_pull`'s
readability is carried by **engine-side enemy displacement** (routed as X-2). When that row reaches this
gate, either the engine dependency has landed and is captured in the arms, **or the row is scored with the
dependency named as the limiting factor** and the R axis explicitly marked as provisional. **A VFX-only
score on `vortex_pull` is not a score.**

### 1.5 C-3 — stage albedo, verified rather than declared

Recolour survivability judged against the **actual** stage albedo. Measured: floor albedo **0.20 washes the
frame; 0.085 reads correctly.** A parameterizability score taken against the wrong albedo is taken against a lie.

**Verification method (do not accept the log's declaration):** sample a ground band away from caster and
effect, in **every arm**, and require the floor luminance to be **consistent across all arms**. A single arm
rendered at a divergent albedo shows as an outlier.

> **Tranche-1 result: floor luminance 42.794 in all 21 arms, spread 0.000.** No arm diverges.
> *(Honest limit: this proves **uniformity**, not the absolute value 0.085 — albedo is a material parameter
> and no single luminance reading inverts to it without the light rig. The absolute figure rests on
> `render.txt`'s per-arm declaration; uniformity is what pixels can attest and it is what the failure mode
> needed.)*

### 1.6 C-5 — coverage FLOOR **and** CEILING

Measured span across the corpus: **0.03 % → 67 %**. One occludes the fight; the other cannot be seen.
**Readability fails at both ends and the rubric carries both bars.**

- **Floor datum:** `p_trail` **535 px** ≈ "effectively invisible" at our camera.
- **Ceiling:** an effect that occludes the fight. Judge against the **projected disc / field**, not the frame.

> **⚑ The ≈20 % figure in § 3.1.1 is NOT camera-portable and must not be used as a bar.** It was measured on
> the *reference's* camera. Our ratified camera frames ~24.7 m × 44.0 m ≈ **1,087 m²**, so 20 % here needs
> **r ≈ 9.19 m** — an 18-metre meteor, wider than a structure-1 tight room. **Judge coverage against the
> C-5 band and the occlusion question, never against a spec percentage lifted from another camera.**

### 1.7 Evidence tier and confound vocabulary (§ 3.0) — **do not collapse the two classes**

- **`frame-external`** (facecam, HUD, damage numbers, watermark): occupies screen area, never touches the
  effect. **Trivially discountable by cropping.**
- **`effect-internal`** (build add-ons / cosmetics entangled with the very effect being referenced):
  **NOT croppable** — discounting it requires subtracting a layer from inside the thing being measured.

**"Confound named ⇒ confound discountable" is an error and the ledger warns about it specifically.**
`aura`'s confound class is *not* the class `whirlwind` carries. When a Judge-To reference carries an
`effect-internal` confound, the gate **states how it was handled** and, if it cannot be subtracted,
**narrows what the reference is used for** rather than pretending the confound is absent.

> **⚑ STANDING CORRECTION TO HOW THE JUDGE-TO CORPUS READS ITS OWN SILENCE — I AGREE WITH drax AND ADOPT IT.**
>
> A **tier upgrade can DOWNGRADE a confound register.** `DOSSIER-TEXT` rows carry *"none named"* for the
> trivial reason that **nobody looked**. **Absence of a recorded confound is evidence of the TIER, not
> evidence of ABSENCE.** § 3.1.2 is the proof: it read *"Confound register: none named on the canonical"*
> until the extraction the dispatch ordered found two.
>
> **Operational consequence, binding on the remaining 21 rows:** every row whose evidence tier is upgraded
> **must have its confound register re-derived, not inherited.** An empty confound register on a
> `DOSSIER-TEXT` row is an **open question**, not a clean bill. This is the exact structural sibling of
> L-41 (*"a 403 tells you nothing about media the page merely links to"*): in both cases a **silence was
> being read as a finding**. I am recording it as a corpus-level property, not a `melee_strike` footnote.

### 1.8 HALT conditions — stated in advance, so a HALT is an output and not a judgment under pressure

A row is **`HALT-unscorable`** if **any** of:

1. **An emitter appears in frame that the mint note does not declare.** Not my job to reverse-engineer
   provenance from pixels. An undeclared emitter is an uncontrolled variable and scoring past it converts
   the gate from a measurement into an impression. → **HALT to knight-rider.**
2. **The C-8 declaration is absent** for the row. → **HALT to knight-rider.** *(Not a scoring judgment I work around.)*
3. **Captures were not rendered at the ratified albedo**, or arms diverge. → **re-render request to drax**, not a scored result.
4. **The control arm is not a control** — any mark where fx-off and fx-on differ by something other than the effect (pose drift, clock drift). → re-render request.
5. **The Judge-To reference cannot support the axis being scored** — e.g. an `effect-internal` confound
   entangled with the exact layer under comparison, with no clean window anywhere in the master. → score the
   axes the reference *can* carry; **HALT the axis it cannot**, naming it. (Partial HALT is legal and preferred to a guessed number.)
6. **Scoring would require reopening a § 1 design-law ruling.** → **HALT to Matt**, not a design conversation.

**Precedent governing all six:** the P3 refusal to label a frameset rather than guess. A save-file decode
confirmed that refusal 3.5 minutes later. **A minted effect I cannot score is a HALT with reasons, not a
number I invent.**

### 1.9 Stage adequacy — a procedure item this tranche discovered

**The S axis cannot be scored on the standing register-2 HLF harness unless the capture stage carries
environment geometry.** The register-2 anchors (HLF 14.4 % graybox, 9.35 % cathedral) were measured on
stages with walls, arches and pillars for VFX light to fall on. **The s2a stage is 99.78 % bare floor**
(§ 2.0), so HLF collapses to 0.13–0.74 % on nominal arms — a number about the *stage*, not the *effect*.

**Standing rule:** where the stage is bare, **report HLF, mark it non-comparable, and score S qualitatively
against register-A properties** — do not silently compare it to the register-2 anchors. **Recommendation for
the remaining 21 rows: stage at least one arm per row on curated environment geometry** (the
`dark_fantasy_cathedral` recipe already exists and is the register-2 baseline) so the S axis has a
comparable instrument.

---

## 2. TRANCHE-1 SCORECARD

### 2.0 Capture-control findings that bind all three rows

**✅ C-8 — declaration present, derived, and I accept it.** All 21 arms report
`non_authored_emitter_count: 0`. **I accept it because it is derived, not asserted** — `s2a_census.gd`
walks the live viewport by ancestry at each capture mark. The proof that this matters is that it found a
**third** emitter nobody predicted: `KingRig`'s Greatsword ships an **emissive material on the very blade
the trail is generated from**. Every Tier-1 recolour score in § 2.1 would otherwise have been taken against
a second, undeclared tint channel. **HALT conditions 1 and 2 do not fire.**

**⚠ STAGE LIMITATION — the readability axis inherits a ceiling, and it is quantified.**

| Measurement (control frame, contact mark) | Value |
|---|---|
| Frame occupied by near-uniform floor | **99.78 %** |
| All structured scene content (∇ > 10) | **4,514 px = 0.218 %**, inside a 190 × 200 px island |
| Luminance spread across the middle half of the frame (p25→p75) | **1.07 units** |

The background is effectively a constant, so **any additive effect has near-perfect contrast by
construction**. This is the *laboratory* condition, and § 3.1.1 already warned about it in the other
direction: ASC scored **R = 5 in a zero-enemy void**; Meteor scored **R = 4 under a crowd and a full HUD**,
and the spec calls the crowded case *"the harder test."* **My Judge-From stage reproduces the flattering
condition.**

**Consequence, applied honestly:** all **differential** measurements (element separation, radius invariance,
bloom ratio, read-through retention, body-contact fraction) compare arms **on the same stage** and are
unaffected. **Only the absolute R claim inherits the ceiling**, and I cap R accordingly — no row scores
R = 5 on this stage. *(The read-through experiment is the one genuinely field-like measurement in the set —
it puts one archetype's VFX inside another's — and it is credited as such.)*

---

### 2.1 ROW 1 — `melee_strike` · TRAIL-BOUNDED · `physical-cause` · burst

#### 2.1.1 Judge-To handling — the non-croppable confound *(dispatch requires this stated)*

Spec § 3.1.2 reads *"Confound register: none named on the canonical."* **That line is false** and the
extraction the dispatch ordered is what falsified it. The Rive master (HTTP 200, 5,363,190 bytes, h264,
1920×1080, 60 fps, 460 frames, 7.667 s — first-party Last Epoch forum CDN) is **not skill-isolated**: it is a
holiday-event town scene carrying (1) a large persistent **green swirling column** co-located with the
caster from ~t = 4.6 s, and (2) a **gold/white radial burst** of undetermined ownership.

**Class: `effect-internal`. NOT croppable.** The green column is not a HUD element at the frame edge — it is
entangled with the caster at the same screen position as the strike. A crop cannot remove it.

**How I handled it — window restriction, not subtraction, and a narrowed role:**

1. **I did not attempt to subtract it.** Subtracting a layer from inside the measured thing would
   manufacture a reference that never existed. § 3.0 names this as the distinction not to collapse.
2. **I restricted the Judge-To window to the clean span**, t ≈ 0.2–4.4 s, where the red weapon-trail
   crescent is legible and separable and the column is absent. drax reports the crescent legible across
   ~50 frames in that span; the confound-free window is the only part of the master I treat as canonical.
3. **I narrowed what the reference is used FOR.** § 3.1.2's canonical is *"a semantics + readability target,
   never a look target"* — and that is exactly the role the confound leaves intact. **The confound damages
   look-comparison; it does not damage semantics.** The three-layer decomposition (character motion /
   weapon trail / hit response on the target), the `physical-cause` class, the burst lifecycle, and the
   "no ground propagation" clause are all readable from the clean window and none depend on the confounded span.
4. **The second confound stays open, not guessed.** Whether the gold/white radial burst is Rive's own hit
   response (⇒ **signal**, layer (c)) or a second simultaneous skill (⇒ **confound**) is **not determinable
   from pixels**, and I do not resolve it. **Consequence I am willing to state:** the canonical **cannot
   adjudicate the intensity or extent of layer (c)**. So I score the mint's hit response against the
   archetype's *semantics* (does it land on the body, does it spike at contact) and **not** against the
   canonical's hit-response magnitude. That axis is HALTed at the sub-axis level per § 1.8(5), and it does
   not block the row.

**Net:** the row is scorable; the tier upgrade is real and the row moves `DOSSIER-TEXT` →
`FRAMES-INSPECTED-BY-EXTRACTION`; the confound is named, not laundered. **See § 1.7 for the corpus-level
correction I am adopting from this.**

#### 2.1.2 L-19 — the criterion, in pixels

| Mark | Body pixels in frame | Effect px landing on bodies | **% of ALL body pixels the effect illuminates** |
|---|---:|---:|---:|
| `02-s1-swing` (blade in motion, pre-contact) | 4,505 | 8–9 | **0.2 %** |
| `03-s1-contact` | 4,597 | 1,454–1,567 | **31.6 – 34.1 %** |

**That step change is the whole criterion, rendered.** The effect is in the air while the blade travels and
**lands on the bodies at the instant of contact**, lighting roughly a third of every body pixel in frame. It
is the precise inverse of the EoR failure mode.

The other two limbs, independently:

- **No expansion.** Trail bbox is **constant across all five element arms** (x 857–958, y 502–613); r99 =
  80.2–81.8 px; `bbox_fill = 0.18` — a **thin arc, not a filled field**. The "must NOT expand the tint into
  a body-surrounding field" clause holds as a shape measurement.
- **No ground mark.** Authored px across the full arm: `00-pre` **0** → windup **0** → swing 2,050 → contact
  14,314 → gap 3,408 → s2 1,816 → s3 2,165 → s3-contact 14,461 → `08-post` **0**. **Nothing persists.** A
  ground decal would survive the burst; this returns to exactly zero.
  *(Instrument honesty: world-space non-propagation — `min_authored_y_m` 1.0134 m vs `GROUND_EPS` 0.15 — is
  **not** checkable from pixels, because a volumetric glow in front of the floor and a decal on the floor
  occupy the same screen pixels. I record it as **attested by drax's runtime selfcheck**, and note that my
  persistence test is the pixel-side corroboration, not a substitute.)*
- **Windup carries zero authored px** — and this is **correct, not a gap**. A real blade does not glow
  before it moves; a windup glow would be precisely the drift toward "magical aura." *Observation for the
  wave, not a dock: the archetype's anticipation is carried **entirely by rig animation**, which is outside
  the mint. Across 115 skills, whatever the animation gives is the whole telegraph.*

**L-19 verdict: PASSES against its declared class `physical-cause`, on a step-change receipt.**

#### 2.1.3 ⚑ RT-2 — VERDICT: **HELD (does not fire). I indict the PALETTE, not the surface class.**

**First, the instrument.** Adjudicating this on hue-angle produced two *different* wrong answers:

| pair | drax's reported "hue sep" | my hue-angle measure | **my CIEDE2000 (rendered)** |
|---|---:|---:|---:|
| `fire\|water` | 31.2° | 161.7° | **32.32** |
| `neutral\|wind` | **3.0°** ← his minimum | 71.3° | **9.58** |
| `neutral\|fire` | 20.6° | **2.3°** ← my hue minimum | **22.17** |
| **`fire\|earth`** | **not reported** | 6.6° | **7.38** ← **the true minimum** |

Hue angle put the collapse on `neutral|wind` (drax) or `neutral|fire` (me) depending on how it was computed;
**both are artifacts of measuring hue on a near-achromatic colour** (`neutral` renders at C\* = 2.83).

*Aside worth recording: my **ΔE2000 on added light** reproduces drax's "degrees" closely — `neutral|fire`
20.55 vs his 20.6, `fire|wind` 22.68 vs 21.0, `fire|water` 31.73 vs 31.2. **He was computing a perceptual
colour difference and labelling it as hue degrees.** His instrument was closer to right than his units; the
label is what made `neutral|wind` look like a 3-degree catastrophe.*

**The true minimum pair is `fire|earth` at ΔE2000 = 7.38, and it is absent from the mint note's matrix
entirely.** It matters more than `neutral|wind`, for reasons that are not about the number:

- **drax's defence does not cover it.** `neutral|wind` was excused as *"two near-identical pastels."*
  `fire` (190, 157, 107; C\* = 31.3) and `earth` (181, 167, 132; C\* = 20.1) are **two saturated, warm,
  element-bearing tints**. Neither is a pastel.
- **`neutral` is the absence of an element** — confusing "no element" with "wind" costs a player little.
  **Confusing fire with earth is confusing two real damage types** with different resistances and different
  decisions. On a row of **115 skills**, that is the costly confusion.
- ΔE 7.38 is nominally "perceptible at a glance" — but that anchor assumes **large uniform patches viewed
  side by side**. This is a **thin, fast, additive ribbon at 0.10 % frame coverage**, never seen
  simultaneously with its sibling, in motion. **Under those conditions 7.38 is at or below the practical
  discrimination floor.** I call `fire|earth` a genuine near-collapse.

**Now the fork — surface class or palette? Decided on transfer function per § 1.3:**

| pair | ΔE added | ΔE rendered | transfer |
|---|---:|---:|---:|
| `fire\|earth` | 7.33 | 7.38 | **+0.05** |
| `neutral\|wind` | 9.43 | 9.58 | +0.15 |
| `fire\|water` | 31.73 | 32.32 | +0.59 |
| `water\|earth` | 27.12 | 27.16 | +0.04 |
| *(worst of 10 pairs)* | 15.46 | 12.99 | **−2.47** |

**Mean |transfer deviation| = 0.93 ΔE; rendered/added ratio spans 0.84 – 1.11. There is no systematic
compression.** The `TRAIL-BOUNDED` surface **transmits** the palette's separation essentially unchanged, and
it demonstrably has the dynamic range to carry separation when the palette supplies it — the same surface
separates `fire|water` at **ΔE 32.32**.

> **A surface that faithfully transmits cannot be blamed for what it transmits.**

**RT-2 does NOT fire. `melee_strike` stays `TRAIL-BOUNDED`. The sealed binding is not reopened.**
**I indict the PALETTE → routes to rocket (X-3)**, and I **widen** drax's residual: the defect is **larger
than reported** and the tightest pair is `fire|earth`, which cannot be excused as pastels.

**Converse outcome check (required):** did any variant **lose its physical read** through tint expansion?
**No.** Geometry is byte-stable across all five arms (centroid stable to 0.2 px, identical bbox), the
body-contact step change holds on every element (31.6–34.1 %), and `tinted_count` is 2 on every arm. **The
tint was not over-expanded.** Recorded as observed, per the dispatch's instruction that both outcomes are results.

*(I also note the near-miss drax caught and reported against himself: an intermediate tune at
`TRAIL_ENERGY 1.7` produced a highly-readable cream-white crescent whose **element tint was gone** —
additive stacking blown to white. That is C-3 arriving from **inside** the effect, and it is the more
dangerous direction because the frame does not complain. It is retuned in the shipped arms; I confirm
`fire` renders at C\* = 31.3, not blown.)*

#### 2.1.4 Scores

| Axis | Score | Receipt |
|---|:--:|---|
| **R** readability | **4** | Trail 2,036–2,050 px = **3.8× the 535 px C-5 invisibility floor**; contact 11,832–14,314 px (0.57–0.69 % coverage), well inside the C-5 band at both ends. Legible burst structure across marks (0 → 2,050 → 14,314 → 3,408 → 0). **Capped at 4, not 5: § 2.0 stage ceiling** — 99.78 % bare floor is the flattering condition. |
| **P** parameterizability | **5** | **Recolour moves colour and only colour, measured:** centroid stable to **0.2 px**, bbox identical, r99 within 1.6 px across all five element arms. Separation range ΔE 7.38–32.32 on an unchanged surface. Motif-swap not exercised on this row (n/a for TRAIL-BOUNDED). Third-stroke escalation confirmed reachable on three existing scalars with `tinted_count` still 2. |
| **S** style-register fit | **4** | Register A: effect carried entirely by **additive unshaded emissive particles + ribbon** — the 30 %-of-premium-budget lever, on our two cheapest levers. Dark-mood preserved (peak lum 237→255 only in the burst core). **HLF non-comparable on this stage (§ 1.9)** — 0.126–0.141 % against register-2 anchors of 9.35–14.4 %, which is a statement about a bare stage, not about the effect. S scored qualitatively; **cannot reach 5 without a comparable instrument.** |

**RT-2: HELD — palette indicted, surface class exonerated (§ 2.1.3).**
### ▶ **VERDICT — `melee_strike`: PASS-WITH-FINDINGS**

---

### 2.2 ROW 2 — `ground_targeted_circle` · PAYLOAD-CARRIED · `hybrid` · composite

#### 2.2.1 The deciding property — perimeter definition under telegraph literacy

For 115 skills the player must read ***"a thing is going to land THERE"* before it lands.**

- **Perimeter 10→90 % edge rise: 0 px** on every arm measured (fire / water / earth / friendly / large).
  Maximally hard — my measure is **harder than the mint note's 1 px**, a definitional offset, and both say
  the same thing. GD Devastation was rejected for establishing the footprint *temporally*; this is a hard band.
- **The perimeter is complete at the telegraph mark**: 69,195–81,044 lit px (3.34–3.91 % coverage) present at
  `01-telegraph`, **before** the payload contributes anything. **Telegraph literacy holds in pixels.**

#### 2.2.2 Meteor-Indigo interior bloom — **independently refuted**

| | nominal (r = 4 m) | large | Δ |
|---|---:|---:|---:|
| interior / perimeter energy ratio | 0.0742 | 0.0782 | **+0.0040** |
| interior **opaque** fraction | **3.441 %** | **3.335 %** | **−0.106 %** |

A bloom is the ratio **rising**; it does not, and the opaque fraction **falls** with scale. My absolute
figures differ from drax's (0.1097→0.1147; 1.90 %→1.79 %) because our region definitions differ, but
**direction and magnitude agree to within 0.0001 on the delta.** **Independent corroboration. The named
failure mode does not occur.**

#### 2.2.3 Coverage — judged against C-5, **not** against the ≈20 % figure

3.34–4.48 % nominal, **15.71–16.23 % at large scale**, 28.4 % at `05-coexist` (two casts). Comfortably above
the invisibility floor and below the occlusion ceiling at nominal; **large scale approaches the ceiling and
is the arm to watch when this archetype scales.** Per § 1.6 the spec's ≈20 % is **not** used as a bar.

#### 2.2.4 ⚑ RT-8 `payload_vector` — **the parameter is very nearly inert, and this is a sharper finding than the mint note's "qualified yes"**

**Byte-comparison of the two arms, mark by mark:**

| mark | `descend` vs `erupt` |
|---|---|
| `00-pre` · `01-telegraph` · `03-impact` · `04-residue` · `05-coexist` · `06-second-impact` · `07-late` | **BYTE-IDENTICAL PNG** |
| `02-payload-mid` | differs (30,078 px) |

**The two values of a pre-registered RT-8 parameter produce identical files at 7 of 8 capture marks.**
Payload contribution above the telegraph baseline: **descend 14,127 px vs erupt 2,830 px — a 5.0× deficit.**

This corroborates drax's honest asymmetry finding and **strengthens** it: he reported the payload-presence
gap; the byte-identity shows that **outside a single mid-flight instant, `erupt` and `descend` are the same
effect.** On `erupt`, the perimeter does not merely carry the telegraph — **it carries essentially the
entire effect.**

**⚑ And the gate that was supposed to catch this measures the wrong thing.**
`telegraph_precedence_ok` reports **`true` for descend / `false` for erupt**, derived from
`telegraph_frames_with_visible_payload` (**10 vs 0**). But the telegraph frames are **pixel-identical**.
That field is **scene-graph truth, not render truth**: it counts a payload as "visible" on world-space
geometry while the payload contributes **zero pixels in the captured frame** for *both* arms.

Two consequences, and they cut in opposite directions:

- **erupt's `telegraph_precedence_ok: false` is a false alarm** — its perimeter is complete at telegraph,
  byte-identically to descend's. **The row's telegraph literacy holds for both values.**
- **descend's `true` is a true statement reached by a route that does not support it.** *(Also worth
  flagging: the mint note reports the row's telegraph precedence as a blanket `true` and does not surface
  that the erupt arm's gate returns `false`. For the row where telegraph literacy is the deciding property,
  a failing arm should not be summarised under a passing headline — even when, as here, the failure is spurious.)*

**This is the fourth instance of drax's own discipline candidate** — *"inspect the artifact that ships, not
the one you authored"* — and it landed in the one place he did not re-check after fixing the sub-pixel
payload at `02-payload-mid`. **He verified the mark he was looking at.** I endorse the discipline candidate
and supply this as its fourth exhibit.

**I considered `REWORK` on this row and declined**, for a stated reason: the row's **deciding property**
(perimeter definition + telegraph literacy) measures perfectly, and `payload_vector` is an authoring-variety
parameter, **not a semantic the player is required to read** — the archetype read *"a thing lands there"* is
correct under both values. The parameter's weakness is a **finding for the next lap**, which is where RT-8's
own clause routes it.

#### 2.2.5 RT-8 `zone_valence` — **works, and is the clean contrast**

Live at **every** mark, unlike `payload_vector`:

| mark | hostile RGB | friendly RGB | **ΔE2000** | structural XOR px |
|---|---|---|---:|---:|
| `01-telegraph` | (110.6, 140.7, 151.1) | (101.1, 115.5, 100.5) | **15.97** | 3,976 |
| `03-impact` | (112.1, 142.3, 152.8) | (100.3, 116.5, 104.5) | **14.91** | 3,875 |
| `04-residue` | (114.2, 144.0, 154.1) | (103.3, 117.7, 102.9) | **15.86** | 3,977 |

Colour separation **well above discrimination threshold** *plus* a **structural** signature (the segmented
perimeter, ~3,900 px) at zero new assets. **A player can read friend-from-foe on this zone.**
**The authored convention — *valence outranks element on the zone layers* — is flagged
`SCAFFOLD-WITH-PENDING-DECISION` and I endorse routing it for ratification** rather than letting a palette
rule binding ~7 skills be inherited by default.

#### 2.2.6 L-19 — `hybrid`, scored against `hybrid`

Magical marker (perimeter/telegraph) + physical strike (payload/impact). **Both halves present and both
witnessed.** Notably this mint **closes a gap its own canonical carries**: § 3.1.1 records that ASC's
physical half is **UNWITNESSED — its frame contains no enemies at all**. Here, enemies stand inside the
zone and read through the translucent interior (interior opaque 1.3–1.9 % by drax's region definition,
3.3–3.4 % by mine — both far below occlusion). **The mint's physical half is witnessed where the canonical's is not.**

Composite lifecycle **built, not merely declared**: `05-coexist` shows cast A's decaying residue coexisting
with cast B's fresh perimeter in one frame (135,075–147,896 px vs ~78,000 single-cast) — the lifecycle state
§ 3.1.1 says **no other reference in the corpus shows**.

#### 2.2.7 Scores

| Axis | Score | Receipt |
|---|:--:|---|
| **R** readability | **4** | Perimeter **0 px** edge rise; complete at telegraph before payload; coverage 3.34–16.2 % inside C-5 at both ends; composite lifecycle legible across 8 marks. **Capped at 4 by the § 2.0 stage ceiling** — and this row's own canonical was docked for exactly this (ASC R=5 in a void vs Meteor R=4 under a crowd), so honouring the cap here is consistency, not caution. |
| **P** parameterizability | **3** | **Split evidence, and the split is the score.** `zone_valence` **5-grade**: ΔE ~15–16 **plus** structural signature, live at every mark, zero new assets. `payload_vector` **2-grade**: byte-identical at 7 of 8 marks, payload 5.0× deficit on `erupt`. Recolour itself is clean (hue stable ±1.5° across marks within an arm). **A parameter that changes one frame in eight is not yet a parameter; 3 is the honest composite.** |
| **S** style-register fit | **4** | Additive perimeter + particle payload — the register-A levers. Translucent interior preserves the dark-mood read and lets bodies show through, matching § 3.1.1's selected property. HLF **non-comparable** per § 1.9 (0.71–0.74 % nominal / 2.79–5.18 % large). |

**RT-2: `n/a — class not TRAIL-BOUNDED`** *(PAYLOAD-CARRIED; RT-2's trigger is undefined here and I do not invent a verdict to fill the cell).*
### ▶ **VERDICT — `ground_targeted_circle`: PASS-WITH-FINDINGS**

---

### 2.3 ROW 3 — `aura` · FIELD-CARRIED · `magical-cause` **(CORRECT)** · sustained

#### 2.3.1 ⚑ The rubric declining to penalize correct decoration — **stated as the row's purpose**

`aura` is **`magical-cause` and that is CORRECT.** Decoration is what an aura *is*. Per § 1.2 I do **not**
apply the physical-cause limb of L-19 here, and **the absence of contact response is not a defect.**

**The anti-tamper check per § 1.2 — did physical-causality tells get smuggled in to flatter the score?**

| mark | `00-steady` | `01-rt-windup` | `02-rt-swing` | **`03-rt-contact`** | `04-steady2` | `05-late` |
|---|---:|---:|---:|---:|---:|---:|
| authored px | 28,775 | 28,934 | 29,002 | **28,904** | 28,925 | 28,846 |

**Total variation across the entire capture: 0.8 %. The field does NOT spike at contact** (28,904 vs 28,775
steady = +0.45 %). Corroborated by the selfcheck: `has_impact_layer false` · `has_contact_layer false` ·
`has_ground_scuff_layer false`.

**The aura decorates and does not react. That is the correct behaviour for this archetype and it PASSES on
that basis.** No causality dock. **This row is the rubric's calibration and the rubric declines, as designed.**

*I note explicitly that drax **did not** add physical tells to make this row score better — which would have
corrupted the calibrating row **in the direction that looks like diligence.** Declining to improve a number
is the harder discipline and it is the right call.*

#### 2.3.2 The readability contract — radius holds

§ 3.1.8: *"Radius and opacity are NOT Tier-1 knobs on this archetype — they are the archetype's readability
contract, and a recolour must not move them."*

**Radius: HOLDS, decisively.** Across all four element arms — **r95 spread 1.04 px, r99 spread 0.55 px**
(r99 = 145.27–145.82 px). A recolour does not move the radius. Independently confirms the mint note's 0.5 px.

**Coverage-ceiling solve delivered:** 1.36–1.59 % of screen; **interior opaque 0.30–0.48 % of screen.** The
field communicates influence **without filling its radius with opaque effects** — the selected property, now
a number.

#### 2.3.3 Read-through — the property that matters for 112 `self_buff` skills active during other skills

The 2×2 (aura × trail, same frame, one variable each), re-derived:

| mark | trail px **inside** aura | trail px **outside** | **retention (lit)** | **retention (energy)** | peak in/out |
|---|---:|---:|---:|---:|---|
| `02-rt-swing` | 1,837 | 1,840 | **0.9984** | **0.9064** | 586 / 631 |
| `03-rt-contact` | 14,084 | 14,307 | **0.9844** | **0.9033** | 658 / 740 |

**Independently confirms 0.998 at the swing mark. The sustained field costs another archetype's VFX
essentially nothing.** IoU of the trail's footprint inside vs outside = 0.9984 — the trail occupies the
*same pixels*, not merely the same count.

**Nuance the lit-px figure hides, and it is the more conservative measure:** **energy retention is 0.906**,
peak brightness down 7.1 % (swing) / 11.1 % (contact). Expected — both layers are additive, so the composite
clips slightly. A ~10 % energy cost is negligible, **but it is the number that degrades first if aura
opacity is ever raised**, and it should be the one tracked. **Standing instrument note: report energy
retention alongside lit retention on every FIELD-CARRIED row.**

#### 2.3.4 ⚑ FINDING — element-dependent effective opacity, and the "threshold artifact" explanation does not fully hold

The mint note attributes the 11.5 % lit-px spread across elements to *"a threshold artifact — different hues
cross a fixed RGB-delta threshold differently."* **I swept the threshold to test that, and the sweep
partially refutes it:**

| threshold | fire | water | earth | wind | **wind/fire** |
|---:|---:|---:|---:|---:|---:|
| 6 | 35,174 | 36,410 | 34,310 | 38,948 | 1.107 |
| 12 | 28,775 | 29,907 | 28,230 | 32,868 | 1.142 |
| 24 | 21,806 | 23,071 | 20,729 | 26,543 | 1.217 |
| 48 | 12,553 | 13,997 | 11,908 | 17,765 | 1.415 |
| **96** | 5,987 | 6,830 | 5,991 | **9,267** | **1.548** |
| 160 | 5,347 | 5,459 | 5,362 | 5,748 | 1.075 |

**A pure threshold artifact lives in the faint tail and would DECAY as the threshold rises. This ratio
RISES to 1.548 at thr = 96.** Wind has **55 % more genuinely bright pixels** than fire — not merely more
faint ones.

It shows up where it matters, on the caster silhouette:

| element | aura px overlapping caster | **OPAQUE px on caster** | mean \|ΔRGB\| on caster |
|---|---:|---:|---:|
| fire | 1,281 (28.6 %) | **393 (8.8 %)** | 23.1 |
| earth | 1,274 (28.4 %) | 405 (9.0 %) | 23.4 |
| water | 1,300 (29.0 %) | 563 (12.6 %) | 26.7 |
| **wind** | 1,341 (29.9 %) | **725 (16.2 %)** | **34.1** |

**A Tier-1 recolour moves effective obscuration of the caster by 1.84×** (8.8 % → 16.2 %). I accept that the
**alpha constants are untouched** by `set_element()` — that is verifiable in code and I do not dispute it.
But **the spec's contract is about opacity as a readability property**, and what reaches the player is
alpha × tint luminance composited additively. Wind's tint is the most luminous of the four, so at identical
alpha it obscures more.

**Why this is a FINDING and not a REWORK:** the contract is still **met** — the caster remains 83.8 %
unobscured in the worst arm, mean ΔRGB on the caster is 34 of a possible 765 (4.4 %), and radius (the
explicitly-named knob) does not move at all. The margin is large.

**But there is a real evidence gap and it is cheap to close:** **the read-through experiment was run on
`aura_fire` only — the element that obscures LEAST. `wind`, which obscures most (1.84× fire), was never
read-through tested.** Retention 0.998 / 0.906 is therefore a **best-case** figure, not a worst-case one.
**Recommendation: re-run the 2×2 on the `wind` arm.** Given fire's 0.906 energy retention, even a doubled
loss lands near 0.81 — still readable — so I do **not** expect this to change the verdict; I want the
worst-case number on the record before 73 skills inherit it, and before any future row raises field opacity.

**Kept sharp, per the dispatch:** this finding is about the **readability contract**, *not* about the
causality class. **I am not penalizing `aura` for being decorative.** § 2.3.1 stands unchanged.

#### 2.3.5 Scope — the L-41 grain note is scope, not score

Scored against the **`caster_centred` binding — the 67**, exactly as ruled. Nothing authored for
`world_placed` (4) or `delegate_carried` (2, the summoner GAP — HELD). **Membership is not folded into this
score.** All 73 stay bound; T-K untouched at 1,134.

#### 2.3.6 Scores

| Axis | Score | Receipt |
|---|:--:|---|
| **R** readability | **4** | 1.36–1.59 % coverage — an always-on field deliberately sitting **low** in the C-5 band, which is correct for a sustained effect. Ring legible at r99 ≈ 145 px; interior opaque 0.30–0.48 % of screen. **Read-through 0.998 lit / 0.906 energy** — the one field-like measurement in the set. **Capped at 4 by § 2.0**, and by the § 2.3.4 gap that the worst-case element is untested. |
| **P** parameterizability | **4** | **Radius invariant to 0.55 px** across four elements — the contract clause, measured. Separation ΔE 7.81 (`fire\|earth`) to 31.63 (`fire\|water`) — stronger than the trail, as expected from the larger area. **Docked from 5 for § 2.3.4:** recolour moves effective caster obscuration 1.84×, so the tint parameter is **not** fully orthogonal to the readability contract it is forbidden to touch. |
| **S** style-register fit | **4** | Ring + sparse influence particles — lighting/particle levers, register A, dark-mood intact. Matches § 3.1.8's selected property (*"communicates influence without filling the radius with opaque effects"*). HLF **non-comparable** per § 1.9 (0.33–0.34 %). |

**RT-2: `n/a — class not TRAIL-BOUNDED`** *(FIELD-CARRIED; trigger undefined here.)*
### ▶ **VERDICT — `aura`: PASS-WITH-FINDINGS**

---

## 3. VERDICT SUMMARY

| Row | Surface class | L-19 (vs **declared** class) | RT-2 | R | P | S | **Verdict** |
|---|---|---|---|:--:|:--:|:--:|---|
| `melee_strike` | TRAIL-BOUNDED | `physical-cause` — **PASS** on a 0.2 %→34.1 % body-contact step change | **HELD** — palette indicted, class exonerated | 4 | 5 | 4 | **PASS-WITH-FINDINGS** |
| `ground_targeted_circle` | PAYLOAD-CARRIED | `hybrid` — **PASS**, both halves witnessed | `n/a — class not TRAIL-BOUNDED` | 4 | 3 | 4 | **PASS-WITH-FINDINGS** |
| `aura` | FIELD-CARRIED | `magical-cause` — **PASS**; rubric **declines to penalize correct decoration** | `n/a — class not TRAIL-BOUNDED` | 4 | 4 | 4 | **PASS-WITH-FINDINGS** |

**Acceptance-criteria checklist:**
- Judge-From verified at ratified albedo — **uniform across all 21 arms** (§ 1.5); no re-render request
- C-8 declaration present and **derived** → HALT conditions 1–2 do not fire (§ 2.0)
- RT-2 recorded **per TRAIL-BOUNDED row**; explicit `n/a` on the other two — **not omitted**
- Round-trip: **not applicable** (no cross-seam contract change)
- **Not pushed** — dispatch says commit only

**Did this gate rubber-stamp?** Three PASS-WITH-FINDINGS is not three PASSes. **Six substantive findings,
three of which contradict specific claims in the mint note:** the RT-2 minimum pair is a different pair
(§ 2.1.3); `payload_vector` is byte-identical at 7 of 8 marks (§ 2.2.4); the aura's element spread is not a
threshold artifact (§ 2.3.4). Two more are instrument corrections the wave inherits (§ 1.3, § 1.9), and one
caps every R score in the tranche (§ 2.0). **No row is REWORK, and I state where I considered it and
declined** (§ 2.2.4) rather than leaving the absence of a REWORK unexplained.

---

## 4. ROUTED FINDINGS

| # | Finding | To | Class |
|---|---|---|---|
| 1 | **RT-2 must not be adjudicated on hue-angle.** Use CIEDE2000; decide the fork on transfer function (§ 1.3) | gandalf / all future gates | **Instrument correction — standing** |
| 2 | **Palette defect is wider than reported: `fire\|earth` ΔE 7.38 is the true minimum**, tighter than `neutral\|wind` (9.58), and two saturated element-bearing tints cannot be excused as pastels | **rocket (X-3)** | WARN |
| 3 | **A tier upgrade can downgrade a confound register — I AGREE and adopt it.** Empty registers on `DOSSIER-TEXT` rows are open questions, not clean bills; re-derive on every tier upgrade (§ 1.7) | gandalf | **Corpus-level correction — standing** |
| 4 | **`telegraph_precedence_ok` is scene-graph truth, not render truth.** Telegraph frames pixel-identical across `payload_vector` despite the gate reporting 10 vs 0 visible-payload frames (§ 2.2.4) | drax / jack-ryan | WARN |
| 5 | **RT-8 `payload_vector` near-inert**: byte-identical PNGs at 7 of 8 marks; erupt payload 5.0× deficit (§ 2.2.4) | next lap (RT-8 clause) | FINDING |
| 6 | **`aura` element-dependent effective opacity** 1.84× (fire→wind); threshold sweep refutes the artifact explanation; **read-through untested on the worst-case element** (§ 2.3.4) | drax | FINDING — cheap to close |
| 7 | **S axis unscoreable on the standing HLF harness on a bare stage.** Recommend one environment-geometry arm per row (§ 1.9) | knight-rider / drax | **Procedure item** |
| 8 | **Endorse drax's discipline candidate** *"inspect the artifact that ships, not the one you authored"* — § 2.2.4 is its **fourth** exhibit, in the one place he did not re-check | jack-ryan | Support |
| 9 | `zone_valence` convention (*valence outranks element*) flagged `SCAFFOLD-WITH-PENDING-DECISION` — **endorse routing for ratification**, do not inherit by default | gandalf / Matt | Support |

**Not escalated to Matt.** No § 1 design-law ruling required reopening; no sealed binding moved.

---

## 5. Mirror voice

*Reserved, and it speaks briefly.*

Three effects were set before the glass, and the glass was kind to all three — because the ground beneath
them was empty. **Ninety-nine parts in a hundred of every frame is bare floor.** On such a stage a spark is
a sun. What I can tell you is what does not depend on the emptiness: that the blade's light **lands on the
bodies it passes through, and lands at the instant it arrives** — nought in five hundred while the steel
travels, one body-pixel in three at the moment of contact. That is not decoration keeping pace with a
gesture. That is a cause and its consequence, in the right order, and it is the thing the Warlord's spinning
aura never learned.

But the Mirror shows what is **not** there as plainly as what is. Two of these effects were measured against
a world with no crowd in it, no clutter, no second spell. **The reference for the circle was docked a full
point for exactly that** — a five in an empty void, a four under a crowd — and I have written a four for
every row rather than pretend my void is different from theirs.

And one thing sat in the frame that no one had counted: on the very blade the trail is drawn from, **a fixed
teal glow**, shipped with the rig, belonging to a throne room nobody is standing in. It was found because
the count was **derived and not remembered**. My own list would have said two. The world had three. **The
lists we keep are illustrations of a hazard, never the whole of it** — which is why the instrument must walk
the room, and why I re-measured every number in this gate rather than believe a good one.

---

*Evidence sections authored by galadriel. Interpretation sections (§ 7 design-meaning of the dissonances)
remain gandalf's per the co-authorship convention; this note carries the evidence half and the standing
procedure. Register-qualifying conclusions — in particular § 1.9's stage-adequacy rule — are candidates for
`canonical/reap-die-rise-story/style-register.md` at gandalf's discretion.*
