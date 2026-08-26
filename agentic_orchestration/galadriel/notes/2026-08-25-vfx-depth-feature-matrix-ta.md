# VFX-DEPTH — the T-A twin-video inventory and the first-pass feature matrix

**STATUS:** COMPLETE (first pass) — **no row graded, no canonical displaced, no bar proposed.**
**Date:** 2026-08-25 · **Author:** galadriel (visual perception + UX-similarity steward)
**Run:** VFX-DEPTH RUN, **wave W-E1** (parallel, non-godot arm) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Charter of record:** `gandalf/notes/2026-08-25-vfx-depth-run-charter.md` — § 4 core loop, **R-8** (terrain response incl. the brief impact-moment distortion flash), **R-10** (screen-shake, camera-layer, with the pan-null trip-wire)
**Governing fence:** T-A spec `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` **§ 6.6** — the post-seal 2012-Blizzard-tree evidence-upgrade authorization. *Probe and record; upgrade an evidence tier; add an archival donor; discharge a confound with measurement.* **Finding is not adopting.** Nothing below displaces, promotes, re-scores or re-ranks anything.
**Predecessor:** `galadriel/notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md` (the instrument, its validated envelope, and its published blind spots)

**Instruments of record (mine, written for this wave):**
`galadriel/pipeline/frame_forensics_depth.py` (the seven families) · `work/2026-08-25-vfx-depth-ta/score_matrix.py` (the **preregistered** PRESENT/ABSENT/UNCERTAIN bars)
**Receipts:** `work/2026-08-25-vfx-depth-ta/out/{ta_depth,ours_depth,feature_matrix,synth_controls,synth_controls2,synth_controls3,f7_control_postpatch}.json`, `series_<row>.json` (per-frame rows, every leg), `cdn_probe.tsv` (111 URLs probed), `MEDIA-SHA256SUMS.txt`

---

## 0 · READ THIS FIRST — four things, and the first one changes the run's arithmetic

### (a) ⚑ THE TWIN-VIDEO PROBLEM WAS REAL, AND IT IS NOW MOSTLY SOLVED — but not by the corpus we had

**Before this wave, the number of T-A rows whose canonical reference could be opened as a VIDEO and cut into frames was TWO** — `melee_strike` (Last Epoch Rive, a first-party forum MP4 nobody had downloaded) and `single_target`'s runner-up (LE Javelin, cut at the P3 delta). Every other canonical is a YouTube URL from which this lane has only ever taken **published thumbnails**, and five of those thumbnails are **title cards** that contain no gameplay at all.

**A charter whose core loop begins `EXTRACT → …` had, on the day it was signed, twenty-two of twenty-four rows with nothing to extract from.**

legolas's RT-4 note had already found the door: the **2012 Blizzard skill-video tree** on the publisher's own Akamai origin, eight assets probed 200 at 720p, and the § 6.6 authorization was written specifically to let it be walked. **I walked it: 111 URLs probed, 67 live**, all `vp6f 1280×720`, all with original 2012 `Last-Modified` stamps. Twenty-three were fetched and measured.

> **Twin-video coverage, before and after this wave:**
>
> | | canonical openable as video | measurable leg of ANY kind |
> |---|---:|---:|
> | before W-E1 | **2 / 24** | 2 / 24 |
> | after W-E1 | **6 / 24** | **23 / 24** |
>
> **The one row with nothing is `line`** (§ 2.4). It is a **NAMED FINDING**, not a silent skip.

### (b) ⚑ R-8's AMENDMENT IS VINDICATED — and in the precise form Matt stated it, which is not the form I would have guessed

R-8's amendment says my no-distortion figure *"was taken on the D3 Whirlwind reference only and does NOT generalize; per-skill extraction governs."* **Per-skill extraction has now been run, and that sentence is correct on both of its halves — including the half that lets my original whirlwind answer stand.**

Signed near/far radial coherence, at each clip's **own measured impact frame** (the validated discriminator is a SIGN PATTERN — a lens is near-**positive** / far-**negative**; a camera dolly is the exact opposite; first reading § 2.3):

| leg | near | far | reading |
|---|---:|---:|---|
| **`cone` — D3 Seismic Slam** | **+0.232** | **−0.754** | ⚑ **LENS-DIRECTION, and the far field is deep inside the validated band 0.51–0.99** |
| `single_target` — LE Javelin | **+0.329** | −0.047 | lens-direction, near field just under bar |
| `whirlwind` — D3 2012 | −0.317 | +0.040 | **camera-push direction — NOT a lens** |
| `melee_strike` — LE Rive | −0.305 | +0.174 | camera-push direction |
| `dash_attack` — D3 Furious Charge | −0.189 | +0.120 | camera-push direction |
| `ground_targeted_circle` — D3 Meteor | −0.244 | −0.244 | signs agree — cannot separate lens from push |

> **So: `whirlwind` genuinely has no impact distortion — my original answer survives on its own clip. And `cone` genuinely does.** The error was never the whirlwind measurement; it was generalising one clip's answer to a corpus. **That is exactly what Matt said, and the instrument now agrees with him against me on the general claim while agreeing with me on the specific one.**

⚠ **And it took catching a defect in my own summary code to see any of this.** My first summary reported the radial coherence as an **absolute maximum** — which destroys the sign, i.e. destroys the one term that separates a distortion field from a camera push, inside a statistic written to answer *"is there a distortion field."* Unsigned, `whirlwind` read `+0.317` and would have been reported as the vindicating row. Signed, it is `−0.317` and is a camera push. **A magnitude where a sign was load-bearing is the § 2.3 forgery arriving one level up — in the AGGREGATION rather than in the operator** (§ 1.3).

### (c) ⚑ THREE OF MY SEVEN OPERATORS FAILED THEIR OWN CONTROLS. They were disqualified before any row was read.

Acceptance discipline from the first reading § 2.3: *a blind operator and an absent phenomenon produce the same reading.* So every family was run against synthetic arms with known ground truth **first**, and the results are not flattering:

| sub-metric | positive arm | matched null | verdict |
|---|---:|---:|---|
| `cv_width` (F3) | comet 0.283 | bar **0.305** | ⚑ **DISQUALIFIED — backwards** |
| `sat_dist_norm` (F4) | comet 1.84 | bar **4.01** | ⚑ **DISQUALIFIED — backwards** |
| `halo_softness` (F5) | smoke 4.14 | comet **8.77** | ⚑ **DISQUALIFIED — backwards** |
| `sat_count`, pre-patch (F4) | comet 191 | **scar 1,141** *(no sparks at all)* | counting compression speckle; repaired |

**Everything reported below runs on what survived.** The disqualifications are in the commit that landed *before* the extraction finished (`f29b7faf`), which is what makes "preregistered" checkable rather than asserted.

### (d) What the wave did NOT do, stated so silence is not read as permission

- **No canonical displaced, no runner-up promoted, no re-score, no L-19 reclassification** — the § 6.6 fence, honoured line by line.
- **No godot capture launched.** The serial lane is drax's; every one of our legs is an already-existing file.
- **No YouTube stream extracted.** This lane's sourcing precedent is *published thumbnails + first-party CDN files*. Ripping a video stream is a different sourcing class with a different ToS question and I do not have pre-authorization for it (§ 2.5). It is also moot: no `yt-dlp` exists on this host.

---

## 1 · The instrument, and where it is blind

### 1.1 What each family is measured by, and what its control says

| # | Family | Surviving carrier(s) | Control: positive vs matched null | Envelope |
|---|---|---|---|---|
| **F1** | hot white / bright **leading head** | `head_white_frac` (V>0.80 **and** S<0.30), vs the tail's | comet **0.539** · bar **0.000** · smoke 0.003 | needs a resolvable direction of travel; refuses below 20 % of frames |
| **F2** | intensity **gradient** along length | `val_slope` along the axis; Δsat = tail − head | slope comet **+0.393** · bar +0.015 · Δsat **+0.345** vs +0.021 | same direction requirement |
| **F3** | **variable width** | `head_tail_width_ratio` only | comet **0.746** · bar **0.944** | ⚠ **0.20 of margin — WEAK. Every F3 call is low-confidence.** `cv_width` disqualified |
| **F4** | **spark shedding** | `sat_count_med` (≥4 px components), `sat_massfrac` | comet **26 / 0.208** · bar **7 / 0.030** · scar **0 / 0.034** | ⚠ count **CAPS at 400** and real references saturate it; `sat_dist_norm` disqualified |
| **F5** | embedding in a **smoke/dust volume** | `halo_area_ratio` only | smoke **1.444** · bar **0.477** | ⚠ **CANNOT separate smoke from BLOOM** — the scar arm, with no smoke, reads **5.14**, the highest in the set |
| **F6a** | terrain **persistent scar** | `scar_frac` on a long baseline, with its own pre-event control | scar **13,886× control** · scar-null **0.0** | ⚑ **refuses when the pre-event control exceeds 0.10** — a panning camera destroys the baseline |
| **F6b** | **impact-moment distortion flash** | **signed** near/far radial coherence at the impact window | validated at ‖0.51–0.99‖, refuses on a null, separates lens from dolly **by sign** (first reading § 2.3) | aggregation changed (impact window, not clip median); operator unchanged, so its envelope carries |
| **F7** | **screen-shake / quake** | high-frequency component of the **fitted camera translation**; spike count; **impact enrichment** | shake **13.798 px / 14 spikes** · 6 px/frame pan **0.000 px / 0 spikes** | ⚠ null is a **RIGID** pan; a 3-D tracking camera manufactures HF that the null cannot model — see § 1.2 |
| **CV** | timing irregularity | inter-event interval on specular mass | reference 1.107 vs our melee_combo 0.102 (first reading § 4.1) | 30 fps caps observable intermittency at 14.985 Hz |

### 1.2 ⚑ R-10's TRIP-WIRE, discharged — and then honestly narrowed

The charter's instruction was precise: *the pan-null that withdrew `novel_frac` must MODEL shake, not be defeated by it.*

**It is discharged by construction first.** A pan and a shake both land in the affine fit's translation term — so hunting for shake in the **residual**, which is where the pan-null looked, would have found nothing *whether or not a shake was there*. The separation is not pan-versus-residual; it is **smooth-versus-impulsive inside the same translation series**. A running median is the smoothing kernel precisely because a spike does not drag it.

**And then by measurement:**

| synthetic arm | fitted pan | HF p99 | spike frames |
|---|---:|---:|---:|
| smooth pan at the reference's own 6 px/frame | 6.000 px/fr | **0.000 px** | **0** |
| impulse-decay shake at frame 60 | 0.039 px/fr | **13.798 px** | **14** |

**The pan does not defeat the detector and does not fool it.**

⚠ **The narrowing, stated because it bounds every F7 cell below.** My pan-null is a **rigid** translation of a still image. A real camera *following a character through a 3-D scene* generates genuine high-frequency translation from parallax and non-rigid content, and my null cannot model that. So F7 carries a second term — **impact enrichment**, the concentration of spike frames near the measured impact — and **an F7 `PRESENT` on a moving-camera clip is demoted to `UNCERTAIN` unless the spikes are impact-concentrated.** A quake is an impulse with a decay; tracking noise is spread. Without that term, "the reference has screen shake" would have been reportable off camera noise, and a spec would have inherited it.

### 1.3 Two defects I found in my own code by looking at the first real row

Both were caught **after** the controls passed and **before** the matrix was read — which is the argument for looking at row one rather than waiting for row twenty-four.

1. **`absmax` on the radial coherence destroyed the sign** — the exact term that discriminates a lens from a camera dolly, in a summary written to answer *"is there a distortion field."* Reporting a magnitude there is the § 2.3 forgery arriving one level up, in the **aggregation** rather than in the operator. Repaired: F6b is now computed **signed**, from the saved per-frame series.
2. **F6a had no refusal gate.** On the panning D3 whirlwind its own *pre-event control* read **0.717** — 72 % of the disc "changed" between two frames bracketing no event whatsoever. That is integer-shift registration error over a 40-frame baseline at 5 px/frame, not a scar. The control term *worked*; what was missing was the rule that a control that high means the operator has **no signal left and must refuse.** Same shape as the § 5.6 dead-denominator gate: *a statistic that does not evaluate is not a statistic that evaluates to zero.*

### 1.4 ⚑ THE LARGEST CAVEAT ON THE WHOLE MATRIX — there is no fx-off control on any reference

First reading § 5.2, and it binds harder here than it did there. On our renders the effect can be isolated by a matched fx-off render. **On every reference leg no such control exists and none can be made.** The novelty mask therefore contains the effect *and* the enemies' animation, their own emissive content, blood decals, damage numbers, HUD elements and churned ground.

**So F1–F5 on a reference leg measure "the dominant transient structure in the frame".** That is *usually* the effect and is *never provably* the effect. Concretely: `whirlwind`'s F4 satellite count sits at the operator's cap of 400, and an unknown share of those 400 are enemies rather than shed sparks.

**Consequence for spec authoring, stated plainly: an F4 or F5 cell on a reference row is weak evidence and must not carry a bar.** F1/F2/F3 are stronger because they are computed on the *largest connected component* rather than on the whole mask, and F6b/F7/CV are stronger still because they are camera-layer or timing quantities that do not depend on isolating the effect at all.

### 1.5 An independent reproduction, unlooked for

`whirlwind` re-measured through an entirely new module reads **CV 1.107, events/s 1.80** against the first reading's **CV 1.107, events/s 1.797** — on a separately re-fetched copy of the file. The metronome finding does not rest on one code path.

---

## 2 · The twin-video inventory — all 24 rows, none silently skipped

### 2.1 Provenance of the new corpus

**Source:** `http://us.media.blizzard.com/d3/flash/skills/<class>/<skill>.flv` — Blizzard's own Akamai origin, the canonical asset path, original 2012 `Last-Modified` stamps, fetched read-only over plain HTTP. **111 slugs probed, 67 live, 44 clean 404s** (`cdn_probe.tsv` carries every code and byte count). 23 fetched; sha256 for all in `MEDIA-SHA256SUMS.txt`.

**Two independent provenance legs, and I checked the weaker one rather than assume it:**

1. **Blog attestation** (legolas RT-4): the archived 2012-03-28 post states *"videos of core class skills, **unmodified by runes**"* and *"much like the last two updates"* — which covers the Feb-24, Mar-12 and Mar-26 batches. **It does NOT cover the Apr-25 and Jul-2012 batches**, and ten of my legs come from those.
2. **Path attestation, measured this session.** For the Jul-2012 batch I pulled the archived **base-skill** pages and read their player markup:

   | archived page | `flvPath` it loads |
   |---|---|
   | `us.battle.net/d3/en/class/barbarian/active/**cleave**` (2012-10-19) | `'/barbarian/cleave.flv'` |
   | `us.battle.net/d3/en/class/barbarian/active/**leap**` (2012-10-19) | `'/barbarian/leap.flv'` |

   **The file I downloaded is the file the BASE-SKILL page serves** — not a rune page, not a rune path. Rune videos in this era lived at their own paths (the P3-delta's five D3 Meteor rune videos are the corpus's own example). **So the base-skill status rests on page-attested path construction, with the blog text as corroboration rather than as its only basis.** (`monk/cyclone-strike`'s archive fetch timed out; same path construction, unverified by archive — flagged, not asserted.)

**Reference-sourcing compliance:** first-party publisher CDN and first-party developer forum, non-commercial internal genre benchmarking. No capture from a running game, no fan-extracted assets, no AI-generated references, no stream ripping.

### 2.2 The inventory table

`CANON-VIDEO` = a video of the row's own canonical (or co-reference-of-record) skill, openable and cuttable.
`DONOR` = a first-party archetype donor of a **different** skill; the identity delta is named. **A donor is not a twin.**
`WEAK` = the donor's mechanic diverges from the archetype's defining property; attribution is unsafe.

| # | Row | T-A canonical (spec § 3.1a) | canonical evidence tier at seal | Measured leg | Relation |
|---:|---|---|---|---|---|
| 1 | `ground_targeted_circle` | PoE Astral Storm Call **+ D3 Meteor (co-ref)** | FRAMES-INSPECTED | `wizard/meteor.flv` | **CANON-VIDEO** — the co-reference-of-record's own skill, first-party |
| 2 | `melee_strike` | **LE · Rive** | DOSSIER-TEXT (link live) | **`le-rive.mp4`, 1920×1080 @60, 460 frames** | ⚑ **CANON-VIDEO — the canonical itself, fetched this wave** |
| 3 | `self_buff` | PoE Illusionist Aura | THUMBNAIL-ONLY | `barbarian/wrath-of-the-berserker.flv` | DONOR |
| 4 | `totem` | PoE Ancestral Warchief | THUMBNAIL-ONLY | `demon-hunter/sentry.flv` | DONOR (placed autonomous delegate) |
| 5 | `circle` *(⊕`ring`)* | GD Ring of Steel | THUMBNAIL-ONLY | `demon-hunter/fan-of-knives.flv` + `wizard/wave-of-force.flv` | DONOR ×2 (filled burst / travelling annulus) |
| 6 | `single_target` | PoE Essence Drain | FRAMES-INSPECTED | **`le-javelin.mp4`** (the row's own runner-up master) | **CANON-VIDEO** (runner-up, not primary) |
| 7 | `melee_arc` | D3 Grim Scythe | FRAMES-INSPECTED | `barbarian/cleave.flv` | DONOR (frontal weapon sweep, same game) |
| 8 | `aura` | D2R Conviction | THUMBNAIL-ONLY | `monk/mantra-of-conviction.flv` | DONOR (a *Conviction* aura, different game) |
| 9 | `multi_projectile` | LE Multishot | THUMBNAIL-ONLY | `demon-hunter/multishot.flv` | DONOR (**same skill NAME**, different game) |
| 10 | `line` | D3 Bone Spear *(Necromancer, 2017)* | THUMBNAIL-ONLY | ⚑ **NONE** — see § 2.4 | ⚑ **PARKED-NAMED** |
| 11 | `dash_attack` *(⊕`defensive_dash`)* | **D3 · Furious Charge** | THUMBNAIL-ONLY | **`barbarian/furious-charge.flv`** | ⚑ **CANON-VIDEO — the canonical skill, first-party 720p** |
| 12 | `whirlwind` | D4 Whirlwind (Matt incumbent) | FRAME-VERIFIED (archival donor) + OWNER-ATTESTATION | `barbarian/whirlwind.flv` | **CANON-VIDEO** (the row's own attested archival donor) |
| 13 | `ground_slam` | D4 Hammer of the Ancients | THUMBNAIL-ONLY | `barbarian/hammer-of-the-ancients.flv` | **CROSS-VERSION** — same skill, **D3 not D4** |
| 14 | `beam_channel` | PoE Scorching Ray | THUMBNAIL-ONLY | `wizard/disintegrate.flv` | DONOR (sustained beam) |
| 15 | `blink` | Lost Ark Distortion | THUMBNAIL-ONLY | `monk/dashing-strike.flv` | DONOR |
| 16 | `cone` | **D3 · Seismic Slam** | DOSSIER-TEXT-ONLY, link **BOT-BLOCKED** | **`barbarian/seismic-slam.flv`** | ⚑ **CANON-VIDEO — the canonical skill; the bot-block is now moot** |
| 17 | `orbit` | LE Shurikens + Blade Shield | THUMBNAIL-ONLY | `monk/sweeping-wind.flv` | DONOR (sustained self-orbiting payload) |
| 18 | `chain` | PoE Celestial Arc | DOSSIER-TEXT-ONLY, link **BOT-BLOCKED** | `wizard/electrocute.flv` | DONOR (near-exact mechanic) |
| 19 | `vortex_pull` | Lost Ark Vortex Gravity | THUMBNAIL-ONLY | `monk/cyclone-strike.flv` | DONOR (near-exact mechanic) |
| 20 | `placed_lane` | LE Frost Wall | DOSSIER-TEXT (link live) | `witch-doctor/wall-of-zombies.flv` | DONOR (placed wall) |
| 21 | `ricochet_bounce` | LE Shield Throw | THUMBNAIL-ONLY | `demon-hunter/chakram.flv` | DONOR (curving returning projectile) |
| 22 | `teleport` | D2R Teleport | THUMBNAIL-ONLY | `wizard/teleport.flv` | DONOR (**same skill NAME**, different game) |
| 23 | `leap_strike` | PoE Demonic Leap Slam | THUMBNAIL-ONLY | `barbarian/leap.flv` | DONOR |
| 24 | `fork` | D3 Elemental Arrow (Frost Arrow) | THUMBNAIL-ONLY | `demon-hunter/cluster-arrow.flv` | ⚑ **WEAK** — § 2.4 |

**Coverage: 23 / 24 rows carry a measurable leg. 6 are CANON-VIDEO. 15 are DONOR. 1 is WEAK. 1 is PARKED-NAMED.**

### 2.3 Four evidence-tier upgrades the § 6.6 fence explicitly permits — routed as FINDINGS, not landed

1. **`cone`** — canonical **D3 Seismic Slam**, sealed `DOSSIER-TEXT-ONLY` with its link `UNVERIFIED-BOT-BLOCKED` on `gamestar.de`. **The same skill's first-party master is live at 720p on Blizzard's origin** (`8,165,864 B`, `Last-Modified 2012-03-12`). The row can move to `FRAME-VERIFIED` **on its own canonical skill**, and the bot-block stops mattering.
2. **`dash_attack`** — canonical **D3 Furious Charge**, sealed `THUMBNAIL-ONLY`. **Same skill, first-party master, 720p** (`6,004,529 B`, `Last-Modified 2012-02-24`).

Also worth the conductor's eye: **`ground_targeted_circle`'s non-PoE co-reference of record (D3 Meteor) now has a first-party 720p master**, and **`melee_strike`'s canonical is no longer merely "an extraction master waiting to be cut"** — it is cut. *(The spec itself named that the cheapest evidence upgrade available on any T1 row.)*

**None of this lands. It returns to gandalf as a finding, per § 6.6.**

### 2.4 ⚑ The NAMED FINDINGS — the two rows the corpus cannot serve

> **`line` — PARKED-NAMED. No adequate twin or donor exists in any corpus this lane can reach.**
>
> The canonical is **D3 Bone Spear**, a *Necromancer* skill from Rise of the Necromancer (2017). The 2012 tree predates that class by five years; there is no Necromancer branch to walk. And the archetype's defining property per spec is **PIERCE** — the payload passes *through* multiple bodies — which is exactly what separates `line` from `single_target`. **No live 2012 skill does that cleanly**: `arcane-orb` detonates, `rapid-fire` is a stream, `disintegrate` is a beam and would cross the very boundary § 4.3 protects.
>
> I measured `wizard/arcane-orb` anyway and report it **explicitly labelled `line_weak` and NOT attributed to `line`**. **51 skills sit behind this row and it has no measurable reference.**
> **What would resolve it:** a frame-extractable Bone Spear clip — the row's YouTube canonical carries a real timestamp (`07:40`), so this is a *sourcing-class* question (§ 2.5), not a hunt.

> **`fork` — WEAK. Its canonical skill is absent from the tree.**
>
> `demon-hunter/elemental-arrow` returns a clean **404** (re-probed twice, including the plural). The substitute, `cluster-arrow`, does split one payload into many with a forward bias — genuinely fork-shaped — but it is *not the canonical skill*, and its grenades arc rather than fly straight. **Every `fork` cell below inherits that delta.** 5 skills.

### 2.5 The gated upgrade I did NOT take, and why naming it matters more than taking it

**Eighteen of the twenty-four canonicals are YouTube URLs.** For all eighteen, this lane's entire evidence base is *published thumbnails* — a sourcing discipline chosen deliberately and held by legolas, elrond and me across three phases.

**Extracting the video streams would convert most DONOR rows into CANON-VIDEO rows in an afternoon.** It is also a **new sourcing class** with its own ToS question, and my reference-sourcing rules require pre-authorization for a new outside-Matt sourcing route. **I am not taking it on my own authority.** *(It is moot on this host regardless — no `yt-dlp` is installed — which is worth recording because it means the boundary was never actually tested by convenience.)*

**Routed to gandalf / knight-rider as a decision, not a request:** *is frame extraction from published YouTube masters an authorized sourcing class for internal non-commercial benchmarking?* A YES upgrades ~15 rows from donor-inference to canonical measurement. A NO is equally actionable — it means the donor structure in § 2.2 is the corpus's ceiling and the spec should be written against donors *knowingly*.

---

## 3 · The feature matrix

**Legend.** **P** = PRESENT · A = ABSENT · ? = UNCERTAIN (routes to per-skill re-measurement) · **n/e** = NOT EVALUABLE (the operator refused; a named reason, not a missing number).

**How to read a cell, and this is the part that matters more than the letters.** `n/e` and `A` are *not* neighbours on a scale. `A` says *the instrument looked and the thing is not there.* `n/e` says *the instrument could not look.* Five reference rows carry `n/e` on F1/F2/F3 for the reason in § 1.4, and treating those as `A` would put *"the D3 references have no hot leading head"* into a spec as a fact. It is not a fact. It is a hole where a measurement should be.

<!--MATRIX-->

## 4 · What the matrix cannot yet measure — the instrument-gap register

Named per the wave brief, with what each would take. These are gaps in **my instrument**, not in the corpus.

| # | Gap | Why it is not measurable today | What it would take |
|---|---|---|---|
| **G-1** | **F1 / F2 / F3 on any reference** — hot head, gradient, variable width | No fx-off control exists on a reference and none can be made (§ 1.4). The largest connected component is effect **+** character **+** enemies and comes out near-round; the principal axis is ill-conditioned and head/tail is arbitrary. | **A hand-annotated effect region on ~20 frames per row.** ~1 h per row, and it is the *same* owed item the first reading raised for D2 (colour). One annotation pass discharges both. **This is the single highest-value instrument job in the seam.** |
| **G-2** | **F4 spark shedding, on references** | The satellite count **saturates at the operator's cap of 400** on every reference leg, and an unknown share of those components are enemies and decals rather than shed material. The descriptor cannot discriminate where it saturates. | Same annotation as G-1, plus **per-component tracking across frames** (a spark is a fleck whose distance from the core *increases*; a decal is one that does not). Tracking is a genuine build, not a parameter change. |
| **G-3** | **F5 cannot separate SMOKE from BLOOM** | Measured, on the controls: the scar arm has no smoke and reads the **largest** halo/core ratio in the set (5.14). A soft glow and a dust volume are the same thing to a low-amplitude-band operator. | A **temporal-persistence** term (smoke outlives its emitter by ~1 s; bloom dies with it) plus an **advection** term (smoke drifts and expands; bloom does not). Both are computable from series I already save — this is the cheapest of the four gaps. |
| **G-4** | **F6a persistent scar, on any panning clip** | The long-baseline comparison needs sub-pixel registration over 30–60 frames; integer-shift compensation at 3–6 px/frame leaves a pre-event control of 0.72, which is no baseline at all. **Refused, not reported.** | **Sub-pixel motion compensation** (the affine model already fitted, applied as a resample rather than a roll). A day of work, and it would also sharpen every mask-based series on a moving camera. |
| **G-5** | **F7 on any moving-camera clip** | My pan-null is a **rigid** pan. A camera following a character through a 3-D scene manufactures high-frequency translation from parallax that the null does not model, so authored shake and tracking noise are not separable by amplitude alone. The impact-enrichment term narrows this but does not close it. | **A 3-D tracking-camera null** — a synthetic scene with depth, panned by a follow-cam, no shake authored. Buildable in the godot harness in an hour **by drax**, and it would convert every reference F7 `?` into a real call. ⚑ *This is the one gap that needs another seam.* |
| **G-6** | **Windup / anticipation phase** | Not a family the charter names, but it is the phase the corpus is thinnest on (`whirlwind` has **zero** windup reference anywhere) and nothing in this instrument measures anticipation as such. | A **phase segmenter** — pre-event / active / decay — derived from the specular-mass envelope. Cheap, and it would let every family be reported *per phase* rather than per clip. |

| **G-7** | ⚑ **F1 / F2 are AXIAL operators, and roughly half of T-A is RADIAL** | The operator asks *"is the LEADING END of an elongated form hotter than the trailing end."* For `ground_targeted_circle`, `circle`, `aura`, `self_buff`, `totem`, `whirlwind`, `orbit`, `vortex_pull` and `ground_slam` the payload is a **burst or a field, not a streak** — so the axial question is **ill-posed, not unanswered**, and the axis-conditioning gate refuses it for a reason that is *correct but conflated* with G-1's contamination. **Two different causes are currently producing the same `n/e`.** | ⚑ **BUILT AND CONTROLLED THIS WAVE — one run from being answered.** `radial_shape_features()` (`243d114e`) substitutes distance-from-centroid for position-along-axis; it needs **no direction of travel**, so it reaches stationary effects the axial operator never could. Control: a pulsing hot-core disc vs a matched flat disc of identical footprint — **`r_core_white_frac` 0.4798 vs 0.0000**, with `r_edge_white_frac` 0.0000 confirming the hot region is core-confined; `r_val_slope` −0.052 vs +0.025 is a weak secondary; **`r_sat_slope` disqualified** (−0.046 vs −0.056, does not separate). **Not run on the corpus** — the extraction was already in flight and had loaded the module. **This is the next lap's first command.** |

### 4.1 ⚑ EYE REGISTER — what I saw at the measured impact frames, reported separately from what the instrument measured

Survey-mode discipline: this is **what the picture shows**, not a score, and not an instrument reading. It is here because on two rows the instrument returned `n/e` while the phenomenon is plainly visible — and a reader who sees only the matrix would conclude the opposite.

| leg | frame | what the picture shows |
|---|---|---|
| `ground_targeted_circle` — D3 Meteor | t = 6.97 s | A large molten sphere descending, **surrounded by a hot bright corona**, a burning ground field beneath it with enemies standing inside, and dark foliage silhouetted against the light. **A hot bright core with a cooler periphery is unmistakably present.** The matrix reads `n/e` on F1/F2 — correctly, because the operator asks an axial question of a radial object. |
| `ground_slam` — D3 Hammer of the Ancients | t = 8.23 s | A **hot white-gold impact core** on the ground, a **cyan-teal weapon trail arcing in from upper-left**, radiating light throwing the terrain into relief, and small shed specks around the impact. **Hot core, colour gradient, spark shedding and terrain illumination are all visible.** The matrix reads `n/e` on F1/F2/F3 for the same reason. |
| `melee_strike` — LE Rive *(canonical)* | t = 1.40 s | A red crescent weapon trail, a **golden contact burst on an enemy body**, and the caster legible at the arc's origin — **the three separated authoring layers the spec cites, confirmed in motion rather than inferred from prose.** |
| `leap_strike` — D3 Leap | t = 2.83 s | The barbarian has **landed among a pack**, with a **hot white-gold core at the touchdown point** throwing light up the surrounding stonework and enemies scattering around it. ⚑ **This is the exact moment Matt named on re-review** (*"Demonic Leap touchdown"*) — and the touchdown carries a bright radial core, not an axial head. |
| `cone` — D3 Seismic Slam | t = 3.60 s | A barbarian on snow with a **compact forward-projected fire burst** and enemies adjacent. Identification confirmed; this is the row whose canonical link was `UNVERIFIED-BOT-BLOCKED` and which now has first-party pixels. |

> ⚑ **The register's own lesson:** on `ground_targeted_circle` and `ground_slam` the matrix says `n/e` and the eye says *"a hot core, a gradient, and sparks are right there."* **Both are correct.** `n/e` means *this instrument could not look*, and the eye is a different instrument. **G-7 is what closes the gap** — and until it is closed, a spec author reading only the letters would be reading the instrument's limits as the corpus's properties.

**What is NOT gap-limited, and is therefore where a spec can stand today:** **F6b** (impact distortion, signed, per-skill), **F7 on our own static-camera renders**, **F6a on our own renders**, and **CV timing on everything**. Those four are camera-layer or timing quantities that never required isolating the effect from the scene — which is precisely why they survived.

---

## 5 · ROUTED

| # | Finding | To | Class |
|---|---|---|---|
| 1 | ⚑ **Twin-video coverage went 2/24 → 23/24.** The 2012 Blizzard tree is live (67 of 111 slugs), first-party, 720p, base-skill-path attested. **The charter's `EXTRACT →` step now has something to extract from.** | gandalf | **FINDING — unblocks the loop** |
| 2 | ⚑ **`line` is PARKED-NAMED. 51 skills, no measurable reference of any kind.** Its canonical is a 2017 Necromancer skill and the archetype's defining property (PIERCE) has no analogue in the live corpus. | gandalf | ⚑ **PARKED-NAMED** (charter § 2 fallback) |
| 3 | **`fork` is WEAK.** Its canonical skill 404s on the tree; the substitute splits one payload into many but is not that skill. Every `fork` cell inherits the delta. | gandalf | **FINDING** |
| 4 | ⚑ **Four evidence-tier upgrades available under § 6.6** — `cone` and `dash_attack` on their **own canonical skills** (`cone`'s bot-blocked link becomes moot), `ground_targeted_circle`'s non-PoE co-reference, and `melee_strike`'s canonical, now cut. **FINDING, not landed** — the fence forbids me landing it. | gandalf | **FINDING — evidence tier** |
| 5 | ⚑ **R-8 vindicated per-skill, and the per-skill part is the whole point.** `cone` (Seismic Slam) carries a lens-direction impact field with the far term at **−0.754**, inside the validated band. `whirlwind` does **not** (−0.317 near / +0.040 far = camera push). **Matt's correction was right about the corpus; my original whirlwind answer survives on its own clip.** | **gandalf** | **ANSWER — design call** |
| 6 | ⚑ **R-10: our renders carry NO screen shake whatsoever** — `hf_p99` 0.00–0.56 px against a 0.5 px floor, zero spike frames on four of six rows. And **the references cannot tell us how much to add**: every reference F7 is `UNCERTAIN` because a 3-D tracking camera and an authored quake are not separable by my rigid pan-null. **This is an authoring decision with no reference target, like the cavitation question before it.** | **gandalf** (how much) · **drax** (build) | **ANSWER + FINDING** |
| 7 | ⚑ **The chartered CV trip-flag FIRES on `OURS_ground_slam`: CV = 0.000, single tone 6,387× its own spectral median**, six events at 1.1667 s exactly. **`OURS_blink` (CV 0.000, 945×) and `OURS_teleport` (CV 0.021, 473×) sit just under the 1000× tone bar** — under *"inspect, never auto-pass"* they are inspected, not passed. The first reading's metronome finding was one row; **it is now four, and it names them.** | **drax** | **FINDING — actionable, specific** |
| 8 | ⚑ **G-5 needs another seam.** Every reference F7 stays `UNCERTAIN` until a **3-D tracking-camera null** exists — a synthetic scene with depth, a follow-cam, no shake authored. **~1 hour in the godot harness, and it converts every reference F7 cell into a real call.** | **drax** | **REQUEST — cross-seam** |
| 9 | **G-1: a hand-annotated effect region, ~20 frames per row, unblocks F1/F2/F3/F4 on every reference.** It is the *same* owed item the first reading raised for colour (D2) — **one annotation pass discharges both.** ~1 h per row. | galadriel | **OWED** |
| 10 | ⚠ **F5 cannot separate SMOKE from BLOOM** — measured on the control, where a clip with no smoke read the largest halo ratio in the set. **A spec must not ask for "smoke" against this operator** until the persistence + advection terms exist (G-3, the cheapest of the four). | gandalf / drax | **WARN — do not build a bar on it** |
| 11 | **A sourcing-class decision is owed:** is frame extraction from published YouTube masters authorized for internal non-commercial benchmarking? **YES upgrades ~15 rows from donor-inference to canonical measurement. NO means the donor structure is the ceiling and the spec should say so knowingly.** I did not take it on my own authority. | **gandalf / knight-rider** | **DECISION REQUESTED** |
| 12 | **Four of my own operators were disqualified by their own controls** (`cv_width`, `sat_dist_norm`, `halo_softness`, `r_sat_slope`), and a fifth (`sat_count`) was counting compression speckle. **All five would have produced confident, wrong cells.** | jack-ryan | **RULING — instrument** |
| 13 | **Independent reproduction:** `whirlwind` re-measured through a new module on a re-fetched file reads **CV 1.107 / 1.80 ev-s** against the first reading's **1.107 / 1.797**. The metronome finding does not rest on one code path. | knight-rider | Support |

**No row graded. No canonical displaced. No bar proposed. Nothing escalated to Matt.**

---

## 6 · Mirror voice

*Reserved, and it speaks once.*

I was sent to read twenty-four references and I found that twenty-two of them could not be opened.

Not lost — **published, live, and shut.** A thumbnail is a photograph of a door. We had spent three phases scoring what was behind those doors from the grain of the wood, and we had been careful and honest about it, and every score we wrote was an inference standing on a still frame. The charter said `EXTRACT` as though extraction were the easy step.

The way in had been written down a day earlier by someone else, in a note about a single clip, in a paragraph he marked *not actioned — outside scope*. **Legolas found a corridor and recorded that he was not walking it.** Sixty-seven doors stood open at the end of it, on the publisher's own machine, with their original hands still on the locks: *March the twenty-sixth, two thousand and twelve.* Fourteen years, untouched, one plain fetch away.

So I walked it, and then I made the mistake that matters.

I built a glass for seven things and I trusted it, and when I looked at the first five references every one of them told me the same thing to the third decimal — *no hot head, no hot head, no hot head, no hot head, no hot head* — and it was **beautifully consistent, and it was nothing at all.** Five identical absences is not five findings. It is one artefact wearing five coats. The cores were round because I could not cut the effect away from the men standing in it, and a line drawn through a circle has two ends and no meaning, and my instrument was solemnly reporting which of two arbitrary ends was brighter.

Then I did the thing the whole seam is named for. **I cut the frames and I looked at them.**

A meteor, falling — molten, coronaed, white at the heart and cooling outward through amber to the burning ground, men standing inside the fire. A hammer coming down — a white-gold core, a cyan arc entering from the upper left, sparks thrown, the whole cave lifted out of the dark for one frame. **A hot core with a cool edge, twice, unmistakable, exactly the thing my seven-part glass had just told me four times over was not there.**

The glass was not lying. It was asking *"which END is hotter"* of a thing that has no ends. I had built an instrument for arrows and pointed it at suns.

**That is the finding I would keep if I could keep only one.** Not the sixty-seven doors, not the metronome at six thousand three hundred and eighty-seven times its own noise, not even the seismic slam bending its far field to three-quarters of a turn while the whirlwind beside it bends nothing. Those are all true and they are all in the tables above.

The one to keep is this: **`n/e` is not `A`.** *I could not look* is not *it is not there*. They cost the same to write, they sit in the same column, they are one character apart — and one of them is a measurement while the other is a hole. Four times today an operator went quiet and the quiet was mistaken for an answer, and four times the only thing that caught it was refusing to believe a silence I had not tested.

The Mirror shows what is. Sometimes what is, is that **the Mirror is turned the wrong way** — and there is no statistic anywhere in it that will say so. Only opening the door, and looking.

---

*Evidence, instrument and instrument-rulings: galadriel. **Design-meaning remains gandalf's** per the co-authorship convention — specifically routings 5 (whether to author a distortion two references disagree about), 6 (how much shake, with no reference target) and 11 (the sourcing-class decision). No sub-agents invoked (HARD NO, standing). Read-only on every working tree outside `galadriel/`, on `reincarnated-godot`, and on the T-A spec.*
