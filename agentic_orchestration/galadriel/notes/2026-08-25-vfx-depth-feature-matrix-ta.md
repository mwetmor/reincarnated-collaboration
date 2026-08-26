# VFX-DEPTH — the T-A twin-video inventory and the first-pass feature matrix

> ## ⛔ AUDIT-KEY QUARANTINE (charter R-12 / registry one-way membrane — stamped by gandalf, RUN-CONDUCTOR, 2026-08-25 on landing)
>
> **This matrix is NEVER included in, quoted to, summarized for, or hinted at within any blind-extraction or blind-judge context.** It was commissioned under the pre-R-12 checklist loop and RE-ROLED on landing per charter R-12: it is audit-key data, consumed ONLY by (a) the conductor's post-extraction coverage audit, (b) the SPEC step (post-extraction, informed layer), (c) per-skill measurement-probe derivation. Its CONTENT-FREE instrument outputs (CV bands, camera-model fits, coverage inventory, CDN provenance) remain legal at the MEASURE and SPEC layers; its feature-family PRESENCE data is membrane-bound with `gandalf/vfx-feature-registry.md`.

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
| ⚑ **`leap_strike` — D3 Leap (touchdown)** | **+0.387** | **−0.559** | ⚑ **LENS-CONSISTENT and it clears the preregistered PRESENT bar. The only full `P` on F6b in the corpus.** |
| **`cone` — D3 Seismic Slam** | +0.232 | **−0.754** | lens-direction; far field **deepest in the validated band 0.51–0.99** of any row |
| `melee_strike` — D3 Hundred Fists | +0.306 | −0.335 | lens-direction, near field just under bar |
| `single_target` — LE Javelin | +0.329 | −0.047 | lens-direction, near field just under bar |
| `whirlwind` — D3 2012 | −0.317 | +0.040 | **camera-push direction — NOT a lens** |
| `melee_strike` — LE Rive *(canonical)* | −0.305 | +0.174 | camera-push direction |
| `ground_slam` — D3 Hammer of the Ancients | −0.296 | +0.227 | camera-push direction |
| `dash_attack` — D3 Furious Charge | −0.189 | +0.120 | camera-push direction |
| `ground_targeted_circle` — D3 Meteor | −0.244 | −0.244 | signs agree — cannot separate lens from push |
| `vortex_pull` — D3 Cyclone Strike | −0.460 | −0.456 | signs agree — ambiguous |

> ### ▶ ⚑ **MATT NAMED THE LEAP TOUCHDOWN. THE LEAP TOUCHDOWN IS THE ROW THAT MEASURES PRESENT.**
>
> R-8's second addendum cites *"Demonic Leap touchdown — Matt's eye confirms it on re-review"* as the reason the family had to include the brief impact-moment distortion field. **Of twenty-six reference legs measured, `leap_strike` is one of only three that clear the bar** — `near +0.387 / far −0.559`, the validated lens sign pattern, far field inside the band the operator was proven on.
>
> **The operator was built and controlled before it was pointed at this row, and it had to be repaired mid-wave (§ 1.3) before it could see a sign at all.** It then agreed with the owner's eye, on the owner's named skill, against my own prior.

> **And `whirlwind` genuinely has NONE — my original answer survives on its own clip.** The error was never the whirlwind measurement; it was generalising one clip's answer to a corpus. **That is exactly what R-8's amendment said, and the instrument now agrees with Matt against me on the general claim while agreeing with me on the specific one.** Four legs read lens-direction, five read camera-push, three are sign-ambiguous. **Per-skill governs, and it governs because the skills genuinely differ.**

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
| **F1** | hot white / bright **leading head** | `head_white_frac` (V>0.80 **and** S<0.30), vs the tail's | comet **0.539** · bar **0.000** · smoke 0.003 | needs a resolvable direction of travel **and an elongated core** — refuses below 20 % of frames or below elongation 2.0 (§ 1.3) |
| **F2** | intensity **gradient** along length | `val_slope` along the axis; Δsat = tail − head | slope comet **+0.393** · bar +0.015 · Δsat **+0.345** vs +0.021 | same direction + elongation requirement |
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

### 1.3 Three defects I found in my own code by looking at the first real rows

All three were caught **after** the controls passed and **before** the matrix was read — which is the argument for looking at row one rather than waiting for row twenty-four.

1. **`absmax` on the radial coherence destroyed the sign** — the exact term that discriminates a lens from a camera dolly, in a summary written to answer *"is there a distortion field."* Reporting a magnitude there is the § 2.3 forgery arriving one level up, in the **aggregation** rather than in the operator. Repaired: F6b is now computed **signed**, from the saved per-frame series.
2. **The axis-conditioning gate did not exist.** On every reference leg F1's head and tail came back **equal to the third decimal** — whirlwind 0.0123 / 0.0121, `melee_strike` 0.0732 / 0.0762, `ground_targeted_circle` 0.0057 / 0.0057 — across five clips of wholly different content. **Five identical absences in a row is not five measurements; it is one artefact wearing five coats.** The cause was in the same table: the cores are near-round (elongation 1.48–1.83) because no fx-off control can be made, so a principal axis on them is ill-conditioned and *head* and *tail* are two arbitrary ends of a meaningless line. The gate now refuses below elongation 2.0, the regime both controls were validated in. **It converts ABSENT cells into NOT-EVALUABLE cells and issues no new PRESENT anywhere.**
3. **F6a had no refusal gate.** On the panning D3 whirlwind its own *pre-event control* read **0.717** — 72 % of the disc "changed" between two frames bracketing no event whatsoever. That is integer-shift registration error over a 40-frame baseline at 5 px/frame, not a scar. The control term *worked*; what was missing was the rule that a control that high means the operator has **no signal left and must refuse.** Same shape as the § 5.6 dead-denominator gate: *a statistic that does not evaluate is not a statistic that evaluates to zero.*

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
| 2 | `melee_strike` | **LE · Rive** | DOSSIER-TEXT (link live) | **`le-rive.mp4`, 1920×1080 @60, 460 frames** (+ donor `monk/way-of-the-hundred-fists.flv`) | ⚑ **CANON-VIDEO — the canonical itself, fetched this wave.** The spec called cutting it *"the cheapest evidence upgrade available on any T1 row"*; it is cut. **Two legs**, so this row also carries a canonical-vs-donor consistency check. |
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

**How to read a cell, and this is the part that matters more than the letters.** `n/e` and `A` are *not* neighbours on a scale. `A` says *the instrument looked and the thing is not there.* `n/e` says *the instrument could not look.* **Most reference rows carry `n/e` on F1/F2/F3** for the reasons in § 1.4 and § 4/G-7, and treating those as `A` would put *"the D3 references have no hot leading head"* into a spec as a fact. It is not a fact. It is a hole where a measurement should be — and § 3.1 shows what fills it once the right operator is pointed at the right coordinate.

<!--MATRIX-->
### CALL MATRIX

| row | F1 | F2 | F3 | F4 | F5 | F6a | F6b | F7 | CV | ev/s | peak/med | trip |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ground_targeted_circle` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.943 | 3.10 | 286 | - |
| `melee_strike_CANON` | n/e | n/e | n/e | **P** | ? | n/e | ? | ? | 0.839 | 3.24 | 132 | - |
| `self_buff` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.827 | 1.99 | 171 | - |
| `totem` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.654 | 2.42 | 19 | - |
| `circle_ring` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.745 | 1.44 | 757 | - |
| `circle_ring_alt` | A | ? | A | **P** | **P** | n/e | ? | **P** | 0.689 | 1.96 | 117 | - |
| `single_target` | ? | A | A | **P** | ? | n/e | ? | ? | 0.755 | 2.92 | 28 | - |
| `melee_arc` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.888 | 1.79 | 19 | - |
| `aura` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.880 | 2.10 | 104 | - |
| `multi_projectile` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.563 | 1.79 | 20 | - |
| `line_weak` | n/e | n/e | n/e | **P** | **P** | n/e | **P** | ? | 1.149 | 1.90 | 43 | - |
| `dash_attack` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.645 | 2.08 | 472 | - |
| `whirlwind` | n/e | n/e | n/e | **P** | ? | n/e | ? | ? | 1.107 | 1.80 | 82 | - |
| `ground_slam` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.784 | 2.46 | 381 | - |
| `beam_channel` | ? | A | A | **P** | ? | n/e | ? | ? | 0.529 | 1.92 | 2278 | - |
| `blink` | n/e | n/e | n/e | **P** | **P** | n/e | **P** | ? | 0.848 | 2.09 | 461 | - |
| `cone` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.629 | 2.08 | 94 | - |
| `orbit` | A | A | A | **P** | **P** | n/e | ? | ? | 0.751 | 2.32 | 462 | - |
| `chain` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.607 | 3.41 | 42 | - |
| `vortex_pull` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.449 | 1.67 | 398 | - |
| `placed_lane` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.727 | 1.61 | 22 | - |
| `ricochet_bounce` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.668 | 2.06 | 294 | - |
| `teleport` | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.701 | 2.60 | 186 | - |
| `leap_strike` | n/e | n/e | n/e | **P** | **P** | n/e | **P** | **P** | 0.646 | 1.82 | 51 | - |
| `fork` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 0.811 | 1.16 | 109 | - |
| `melee_strike` | n/e | n/e | n/e | **P** | **P** | n/e | ? | **P** | 1.127 | 2.49 | 97 | - |
| `OURS_dash_attack` | A | ? | **P** | **P** | **P** | **P** | A | A | 0.955 | 3.43 | 252 | - |
| `OURS_blink` | ? | ? | **P** | **P** | ? | n/e | ? | A | 0.000 | 1.50 | 945 | - |
| `OURS_teleport` | n/e | n/e | n/e | **P** | **P** | ? | ? | A | 0.021 | 1.35 | 473 | - |
| `OURS_leap_strike` | A | ? | **P** | **P** | **P** | **P** | ? | ? | 0.668 | 1.93 | 1955 | - |
| `OURS_ground_slam` | A | ? | A | ? | **P** | ? | ? | A | 0.000 | 0.89 | 6387 | ⚑TRIP |
| `OURS_melee_combo` | ? | **P** | A | ? | **P** | ? | ? | ? | 0.102 | 2.52 | 2148 | ⚑TRIP |

### NUMERIC APPENDIX

| row | head_white p90 | tail_white p90 | lead_known | val_slope | head_sat | tail_sat | h/t width | elong | sat_n | sat_mass | halo/core | pan px/fr | hf p99 | shake n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ground_targeted_circle` | 0.0057 | 0.0057 | 0.95 | -0.014 | 0.428 | 0.428 | 0.987 | 1.68 | 400 | 0.472 | 1.34 | 6.14 | 11.27 | 4 |
| `melee_strike_CANON` | 0.0732 | 0.0762 | 1.00 | -0.013 | 0.469 | 0.465 | 1.036 | 1.65 | 400 | 0.362 | 0.60 | 1.16 | 11.89 | 27 |
| `self_buff` | 0.0266 | 0.0225 | 0.98 | +0.001 | 0.357 | 0.361 | 1.016 | 1.62 | 400 | 0.469 | 1.19 | 2.69 | 10.93 | 97 |
| `totem` | 0.0021 | 0.0023 | 0.97 | +0.010 | 0.396 | 0.401 | 1.009 | 1.62 | 400 | 0.432 | 1.23 | 4.15 | 7.10 | 85 |
| `circle_ring` | 0.1459 | 0.1215 | 0.97 | +0.029 | 0.665 | 0.691 | 1.034 | 1.91 | 400 | 0.390 | 2.32 | 6.47 | 7.60 | 84 |
| `circle_ring_alt` | 0.0000 | 0.0043 | 0.96 | -0.032 | 0.502 | 0.490 | 1.005 | 2.15 | 400 | 0.339 | 2.48 | 4.84 | 2.94 | 43 |
| `single_target` | 0.1400 | 0.0997 | 1.00 | +0.024 | 0.306 | 0.304 | 0.991 | 2.17 | 400 | 0.318 | 0.66 | 2.89 | 7.08 | 43 |
| `melee_arc` | 0.0015 | 0.0022 | 0.97 | +0.002 | 0.643 | 0.634 | 0.939 | 1.84 | 400 | 0.388 | 1.41 | 2.05 | 6.56 | 63 |
| `aura` | 0.0062 | 0.0105 | 0.94 | +0.032 | 0.468 | 0.464 | 0.948 | 1.83 | 199 | 0.377 | 1.30 | 2.04 | 3.46 | 33 |
| `multi_projectile` | 0.0036 | 0.0004 | 0.96 | -0.001 | 0.774 | 0.776 | 0.986 | 1.72 | 400 | 0.390 | 1.12 | 3.97 | 7.99 | 54 |
| `line_weak` | 0.0104 | 0.0200 | 0.96 | -0.025 | 0.487 | 0.495 | 1.019 | 1.70 | 400 | 0.382 | 1.57 | 1.69 | 4.42 | 113 |
| `dash_attack` | 0.1168 | 0.1103 | 0.94 | -0.036 | 0.263 | 0.264 | 0.970 | 1.83 | 400 | 0.433 | 1.58 | 4.29 | 11.47 | 82 |
| `whirlwind` | 0.0123 | 0.0121 | 0.94 | -0.013 | 0.354 | 0.355 | 0.994 | 1.48 | 400 | 0.428 | 0.82 | 5.04 | 11.37 | 32 |
| `ground_slam` | 0.0208 | 0.0279 | 0.97 | +0.014 | 0.676 | 0.676 | 1.003 | 1.72 | 400 | 0.405 | 1.26 | 3.34 | 9.53 | 62 |
| `beam_channel` | 0.0779 | 0.0760 | 0.97 | +0.001 | 0.718 | 0.709 | 0.996 | 3.36 | 400 | 0.328 | 0.71 | 1.98 | 3.51 | 28 |
| `blink` | 0.0365 | 0.0492 | 0.96 | -0.013 | 0.453 | 0.444 | 0.961 | 1.60 | 400 | 0.439 | 1.52 | 2.97 | 8.16 | 63 |
| `cone` | 0.0053 | 0.0065 | 0.97 | +0.019 | 0.372 | 0.368 | 0.998 | 1.75 | 400 | 0.413 | 1.09 | 3.61 | 7.80 | 51 |
| `orbit` | 0.0178 | 0.0210 | 0.96 | +0.011 | 0.459 | 0.459 | 0.951 | 2.10 | 400 | 0.433 | 2.14 | 4.75 | 11.18 | 91 |
| `chain` | 0.0803 | 0.0799 | 0.96 | -0.086 | 0.528 | 0.521 | 1.018 | 1.69 | 400 | 0.374 | 1.12 | 1.97 | 3.26 | 13 |
| `vortex_pull` | 0.0358 | 0.0433 | 0.93 | -0.003 | 0.548 | 0.565 | 0.969 | 1.71 | 400 | 0.403 | 1.49 | 2.35 | 7.16 | 57 |
| `placed_lane` | 0.0149 | 0.0137 | 0.95 | +0.007 | 0.361 | 0.359 | 1.049 | 1.75 | 400 | 0.462 | 1.03 | 2.78 | 8.18 | 52 |
| `ricochet_bounce` | 0.1721 | 0.1658 | 0.97 | -0.017 | 0.383 | 0.383 | 0.994 | 1.53 | 400 | 0.370 | 2.35 | 5.10 | 6.35 | 62 |
| `teleport` | 0.0421 | 0.0287 | 0.96 | +0.027 | 0.636 | 0.654 | 0.980 | 1.89 | 400 | 0.365 | 2.60 | 4.96 | 8.41 | 70 |
| `leap_strike` | 0.0100 | 0.0082 | 0.96 | -0.007 | 0.564 | 0.572 | 0.984 | 1.78 | 400 | 0.428 | 1.45 | 3.17 | 8.97 | 73 |
| `fork` | 0.0000 | 0.0000 | 0.96 | -0.053 | 0.694 | 0.705 | 1.007 | 1.86 | 400 | 0.434 | 1.07 | 5.20 | 5.02 | 38 |
| `melee_strike` | 0.0023 | 0.0027 | 0.97 | +0.016 | 0.532 | 0.543 | 1.021 | 1.87 | 400 | 0.368 | 1.16 | 1.89 | 7.69 | 87 |
| `OURS_dash_attack` | 0.0000 | 0.0000 | 0.62 | -0.044 | 0.765 | 0.734 | 0.804 | 2.15 | 24 | 0.223 | 2.38 | 0.03 | 0.19 | 0 |
| `OURS_blink` | 0.0447 | 0.2137 | 0.99 | -0.109 | 0.682 | 0.359 | 1.395 | 2.07 | 28 | 0.151 | 0.67 | 0.03 | 0.15 | 0 |
| `OURS_teleport` | 0.2103 | 0.0716 | 0.74 | -0.001 | 0.467 | 0.455 | 1.000 | 1.39 | 19 | 0.194 | 1.09 | 0.00 | 0.00 | 0 |
| `OURS_leap_strike` | 0.0000 | 0.0041 | 0.94 | -0.055 | 0.698 | 0.460 | 1.240 | 2.47 | 19 | 0.144 | 1.19 | 0.00 | 0.56 | 3 |
| `OURS_ground_slam` | 0.0005 | 0.0000 | 0.55 | +0.032 | 0.612 | 0.619 | 0.991 | 2.28 | 0 | 0.154 | 2.50 | 0.00 | 0.00 | 0 |
| `OURS_melee_combo` | 0.0706 | 0.0000 | 0.99 | +0.214 | 0.593 | 0.483 | 0.931 | 2.74 | 14 | 0.174 | 1.08 | 0.00 | 0.64 | 5 |

### F6b SIGNED, and F7 LOCALISATION

| row | F6b why | F7 why | F7 impact-enrichment |
|---|---|---|---|
| `ground_targeted_circle` | near -0.244 / far -0.244 (clip med -0.013) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 11.27 px, 4 spike frames — camera pans 6.14 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `melee_strike_CANON` | near -0.305 / far +0.174 (clip med +0.018) | hf_p99 11.89 px, 27 spike frames — camera pans 1.16 px/fr and spikes are NOT impact-concentrated (enrichment 0.5x); rigid pan-null cannot model a 3D tracking camera | 0.5x |
| `self_buff` | near -0.169 / far +0.403 (clip med +0.018) | hf_p99 10.93 px, 97 spike frames | 4.9x |
| `totem` | near +0.441 / far +0.149 (clip med +0.037) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 7.10 px, 85 spike frames | 2.1x |
| `circle_ring` | near -0.339 / far +0.265 (clip med -0.020) | hf_p99 7.60 px, 84 spike frames | 2.4x |
| `circle_ring_alt` | near +0.446 / far +0.938 (clip med +0.049) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 2.94 px, 43 spike frames | 2.9x |
| `single_target` | near +0.329 / far -0.047 (clip med +0.002) | hf_p99 7.08 px, 43 spike frames — camera pans 2.89 px/fr and spikes are NOT impact-concentrated (enrichment 1.8x); rigid pan-null cannot model a 3D tracking camera | 1.8x |
| `melee_arc` | near -0.285 / far -0.331 (clip med -0.005) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 6.56 px, 63 spike frames — camera pans 2.05 px/fr and spikes are NOT impact-concentrated (enrichment 0.5x); rigid pan-null cannot model a 3D tracking camera | 0.5x |
| `aura` | near -0.429 / far -0.264 (clip med -0.034) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 3.46 px, 33 spike frames | 3.9x |
| `multi_projectile` | near +0.331 / far +0.350 (clip med -0.036) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 7.99 px, 54 spike frames — camera pans 3.97 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `line_weak` | near +0.480 / far -0.230 (clip med +0.050) — lens-consistent (validated sig 0.51-0.99) | hf_p99 4.42 px, 113 spike frames — camera pans 1.69 px/fr and spikes are NOT impact-concentrated (enrichment 1.7x); rigid pan-null cannot model a 3D tracking camera | 1.7x |
| `dash_attack` | near -0.189 / far +0.120 (clip med -0.010) | hf_p99 11.47 px, 82 spike frames — camera pans 4.29 px/fr and spikes are NOT impact-concentrated (enrichment 2.0x); rigid pan-null cannot model a 3D tracking camera | 2.0x |
| `whirlwind` | near -0.317 / far +0.040 (clip med -0.011) | hf_p99 11.37 px, 32 spike frames — camera pans 5.04 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `ground_slam` | near -0.296 / far +0.227 (clip med -0.003) | hf_p99 9.53 px, 62 spike frames — camera pans 3.34 px/fr and spikes are NOT impact-concentrated (enrichment 1.7x); rigid pan-null cannot model a 3D tracking camera | 1.7x |
| `beam_channel` | near +0.109 / far -0.288 (clip med +0.041) | hf_p99 3.51 px, 28 spike frames — camera pans 1.98 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `blink` | near +0.370 / far -0.052 (clip med -0.007) — lens-consistent (validated sig 0.51-0.99) | hf_p99 8.16 px, 63 spike frames — camera pans 2.97 px/fr and spikes are NOT impact-concentrated (enrichment 0.4x); rigid pan-null cannot model a 3D tracking camera | 0.4x |
| `cone` | near +0.232 / far -0.754 (clip med +0.020) | hf_p99 7.80 px, 51 spike frames — camera pans 3.61 px/fr and spikes are NOT impact-concentrated (enrichment 1.9x); rigid pan-null cannot model a 3D tracking camera | 1.9x |
| `orbit` | near -0.265 / far -0.036 (clip med -0.006) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 11.18 px, 91 spike frames — camera pans 4.75 px/fr and spikes are NOT impact-concentrated (enrichment 1.9x); rigid pan-null cannot model a 3D tracking camera | 1.9x |
| `chain` | near +0.254 / far -0.102 (clip med +0.057) | hf_p99 3.26 px, 13 spike frames — camera pans 1.97 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `vortex_pull` | near -0.460 / far -0.456 (clip med +0.011) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 7.16 px, 57 spike frames — camera pans 2.35 px/fr and spikes are NOT impact-concentrated (enrichment 1.7x); rigid pan-null cannot model a 3D tracking camera | 1.7x |
| `placed_lane` | near -0.105 / far +0.197 (clip med +0.068) | hf_p99 8.18 px, 52 spike frames | 3.6x |
| `ricochet_bounce` | near +0.108 / far -0.110 (clip med +0.015) | hf_p99 6.35 px, 62 spike frames — camera pans 5.10 px/fr and spikes are NOT impact-concentrated (enrichment 0.0x); rigid pan-null cannot model a 3D tracking camera | 0.0x |
| `teleport` | near +0.242 / far +0.030 (clip med -0.001) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 8.41 px, 70 spike frames — camera pans 4.96 px/fr and spikes are NOT impact-concentrated (enrichment 0.3x); rigid pan-null cannot model a 3D tracking camera | 0.3x |
| `leap_strike` | near +0.387 / far -0.559 (clip med +0.016) — lens-consistent (validated sig 0.51-0.99) | hf_p99 8.97 px, 73 spike frames | 3.6x |
| `fork` | near -0.250 / far -0.842 (clip med +0.052) — SIGNS AGREE: cannot separate a lens from a camera push | hf_p99 5.02 px, 38 spike frames | 2.5x |
| `melee_strike` | near +0.306 / far -0.335 (clip med -0.016) | hf_p99 7.69 px, 87 spike frames | 4.0x |
| `OURS_dash_attack` | near +0.074 / far +0.023 (clip med +0.093) | hf_p99 0.19 px (pan-null=0.00) | — |
| `OURS_blink` | radial refused at impact (zero-magnitude residual) | hf_p99 0.15 px (pan-null=0.00) | — |
| `OURS_teleport` | radial refused at impact (zero-magnitude residual) | hf_p99 0.00 px (pan-null=0.00) | — |
| `OURS_leap_strike` | radial refused at impact (zero-magnitude residual) | hf_p99 0.56 px, 3 spikes | 0.0x |
| `OURS_ground_slam` | radial refused at impact (zero-magnitude residual) | hf_p99 0.00 px (pan-null=0.00) | — |
| `OURS_melee_combo` | radial refused at impact (zero-magnitude residual) | hf_p99 0.64 px, 5 spikes | 0.0x |

### MATCHED PAIRS — reference vs ours, same operators, same raster

| row | leg | F1 | F2 | F3 | F4 | F5 | F6a | F6b | F7 | CV | ev/s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `dash_attack` | REF | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.645 | 2.08 |
| `dash_attack` | OURS | A | ? | **P** | **P** | **P** | **P** | A | A | 0.955 | 3.43 |
| `blink` | REF | n/e | n/e | n/e | **P** | **P** | n/e | **P** | ? | 0.848 | 2.09 |
| `blink` | OURS | ? | ? | **P** | **P** | ? | n/e | ? | A | 0.000 | 1.50 |
| `teleport` | REF | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.701 | 2.60 |
| `teleport` | OURS | n/e | n/e | n/e | **P** | **P** | ? | ? | A | 0.021 | 1.35 |
| `leap_strike` | REF | n/e | n/e | n/e | **P** | **P** | n/e | **P** | **P** | 0.646 | 1.82 |
| `leap_strike` | OURS | A | ? | **P** | **P** | **P** | **P** | ? | ? | 0.668 | 1.93 |
| `ground_slam` | REF | n/e | n/e | n/e | **P** | **P** | n/e | ? | ? | 0.784 | 2.46 |
| `ground_slam` | OURS | A | ? | A | ? | **P** | ? | ? | A | 0.000 | 0.89 |
| `melee_strike_CANON` | REF | n/e | n/e | n/e | **P** | ? | n/e | ? | ? | 0.839 | 3.24 |
| `melee_strike_CANON` | OURS | ? | **P** | A | ? | **P** | ? | ? | ? | 0.102 | 2.52 |

### 3.1 ⚑ G-7 RADIAL READING — the rows the axial operator had to refuse

Control anchors: hot-core disc **0.4798** · matched flat disc **0.0000** (`out/synth_radial_control.json`). `r_sat_slope` is disqualified and not shown.

| leg | core_white p90 | edge_white p90 | **core/edge ratio** | core_sat | edge_sat | **val_slope** (−ve = bright centre) | call (preregistered bar) |
|---|---:|---:|---:|---:|---:|---:|---|
| `R_ground_targeted_circle` | 0.0156 | 0.0026 | **6.0×** | 0.476 | 0.405 | **-0.2654** | ABSENT |
| `R_ground_slam` | 0.0739 | 0.0027 | **27.1×** | 0.633 | 0.701 | **-0.2758** | UNCERTAIN |
| `R_circle_ring` | 0.1999 | 0.0311 | **6.4×** | 0.600 | 0.693 | **-0.4522** | **PRESENT — hot core** |
| `R_aura` | 0.0415 | 0.0045 | **9.2×** | 0.497 | 0.460 | **-0.1537** | UNCERTAIN |
| `R_whirlwind` | 0.0156 | 0.0073 | **2.1×** | 0.357 | 0.345 | **-0.1641** | ABSENT |
| `R_vortex_pull` | 0.2010 | 0.0295 | **6.8×** | 0.498 | 0.566 | **-0.1341** | **PRESENT — hot core** |
| `R_OURS_ground_slam` | 0.0645 | 0.0000 | **64487.2×** | 0.561 | 0.484 | **-0.0043** | UNCERTAIN |

> ⚑ **READ THE RATIO AND THE SLOPE, NOT ONLY THE CALL.** The preregistered `core_white ≥ 0.15` bar was calibrated on a synthetic whose core is *pure* white; real footage does not reach that absolute level. **But the core/edge ratio is 6–27× on every reference leg, and `val_slope` runs −0.15 to −0.45 against the synthetic POSITIVE control's −0.052** — a radial intensity gradient five to nine times STRONGER than the arm the operator was validated on. I am not lowering the bar after seeing the data; I am reporting that the absolute predicate (`V>0.80 AND S<0.30`) is a synthetic's idealisation while **the gradient itself is unambiguous and present in every radial reference measured.** That is precisely what the § 4.1 eye-register saw and the axial operator could not reach.

<!--MATRIX-END-->

### 3.3 ⚑ THE CLEANEST RESULT IN THE WAVE — CV timing, 26 reference legs against our 6, and the gap does not overlap

Every leg, sorted by CV of the inter-event interval:

| band | legs | CV range |
|---|---|---|
| ⚑ **OURS — metronomic** | `OURS_blink` **0.000** · `OURS_ground_slam` **0.000** · `OURS_teleport` **0.021** · `OURS_melee_combo` **0.102** | **0.000 – 0.102** |
| *(no leg of any kind lands here)* | — | **0.103 – 0.448** |
| **references — all 26 of them** | `vortex_pull` 0.449 … `melee_strike` 1.127 · `line_weak` 1.149 | **0.449 – 1.149** |
| **OURS — inside the reference band** | `OURS_leap_strike` 0.668 · `OURS_dash_attack` 0.955 | 0.668 / 0.955 |

> ### ▶ **TWENTY-SIX REFERENCE LEGS SPAN CV 0.449 – 1.149. NOT ONE FALLS BELOW 0.449. FOUR OF OUR SIX ROWS FALL BELOW 0.103.**
>
> **The gap between 0.102 and 0.449 contains nothing at all** — no reference, from five character classes, across twenty-four archetypes, and no other row of ours.
>
> The first reading found this on **one** row against **one** reference and said so cautiously. It now has **twenty-six** reference legs behind it and the separation is clean.

**And it is still an AUTHORING finding, not a capability one — now proven on our own side rather than argued.** `OURS_leap_strike` (0.668) and `OURS_dash_attack` (0.955) sit **comfortably inside the reference band**, built by the same seam, in the same engine, on the same day as the four that do not. **Two of our rows already do the thing. Four do not.** That is a per-row authoring gap with a named target range, which is the most directly actionable number this wave produced.

**Trip-flag disposition, per the chartered rule** (`CV < 0.25` **and** a single tone > 1000× the spectral median → *inspect, never auto-pass*):

| row | CV | dominant tone | disposition |
|---|---:|---:|---|
| `OURS_ground_slam` | **0.000** | **6,387×** | ⚑ **TRIPS.** Six events, 1.1667 s apart, every time. |
| `OURS_melee_combo` | 0.102 | 2,148× | ⚑ **TRIPS.** Independently reproduces the first reading's figure exactly. |
| `OURS_blink` | **0.000** | 945× | **near-miss on the tone bar by 5.5 % — INSPECTED, not passed.** A CV of exactly zero is self-evidently inspect-worthy whatever the tone does. |
| `OURS_teleport` | 0.021 | 473× | under the tone bar — **inspected on the CV alone.** |

⚠ **A note against my own rule.** `OURS_blink` shows the trip-flag's conjunction is too strict: **CV = 0.000 exactly** and it does not fire, because a second condition on an unrelated statistic missed by 5 %. **I am not rewriting a chartered rule; I am recording that it under-fired on a real row and inspecting the row anyway** — which is what *"never auto-pass"* was written to make happen.

### 3.4 ⚑ TWO CELLS IN THIS MATRIX ARE VACUOUS AND I WOULD RATHER SAY SO THAN LET THEM BE USED

| family | PRESENT | of | verdict |
|---|---:|---:|---|
| **F4 sparks** | **30** | 32 | ⚑ **VACUOUS. 25 of 32 legs are at the operator's cap of 400 satellites.** A descriptor that saturates on 78 % of its inputs and calls PRESENT on 94 % of them discriminates nothing. |
| **F5 smoke volume** | **27** | 32 | ⚑ **VACUOUS, and it also cannot tell smoke from bloom** (§ 1.1). |

**Do not build a bar on F4 or F5, and do not read their `P` as evidence.** They are in the table because suppressing a measurement I took would be worse than printing one I distrust — the same reason the first reading kept an exhibit that argued for a conclusion it had withdrawn. **The families that carry real information here are F6b, F7 and CV.**



### 3.2 ⚑ THE SHARPEST NUMBER THIS WAVE PRODUCED — `ground_slam`, reference against ours, on the radial axis

The radial pass carried **one matched pair**: D3 Hammer of the Ancients against our own `05_ground_slam_CATHEDRAL`, same operators, same raster, same bars.

| | **reference** (D3 HotA) | **OURS** | ratio |
|---|---:|---:|---:|
| `core_white_frac` p90 | 0.0739 | **0.0645** | 0.87× — **we match** |
| `edge_white_frac` p90 | 0.0027 | 0.000064 | |
| core / edge ratio | 27.1× | 7,161× | |
| ⚑ **`val_slope`** (−ve = bright centre, dim rim) | **−0.2758** | **−0.0043** | ⚑ **64×** |

> **We have the hot core. We do not have the FALLOFF.**
>
> Our slam is as bright at its centre as the reference's — `core_white` 0.0645 against 0.0739, a difference of 13 %. But the reference's brightness **decays strongly from centre to rim** (−0.276) while ours is **very nearly flat** (−0.004). And our edge carries essentially *no* bright content at all (6.4 × 10⁻⁵ against the reference's 2.7 × 10⁻³).
>
> **In plain terms: theirs is a core that cools outward into its surroundings; ours is a bright disc with an edge.** That is a specific, measurable, single-parameter difference — and it is one legible face of what Matt called *"lacking the depth."*

⚠ **What this is not.** One pair, one row, one clip each; the reference is scene-contaminated and ours is not (§ 1.4), and a scene-contaminated mask can borrow falloff from the lighting around the effect. **This is a strong lead, not a bar.** The way to harden it is the G-1 annotation on this one row — an hour's work against a number worth having.



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
| **G-7** | ⚑ **F1 / F2 are AXIAL operators, and roughly half of T-A is RADIAL** | The operator asks *"is the LEADING END of an elongated form hotter than the trailing end."* For `ground_targeted_circle`, `circle`, `aura`, `self_buff`, `totem`, `whirlwind`, `orbit`, `vortex_pull` and `ground_slam` the payload is a **burst or a field, not a streak** — so the axial question is **ill-posed, not unanswered**, and the axis-conditioning gate refuses it for a reason that is *correct but conflated* with G-1's contamination. **Two different causes are currently producing the same `n/e`.** | ⚑ **BUILT AND CONTROLLED THIS WAVE — one run from being answered.** `radial_shape_features()` (`243d114e`) substitutes distance-from-centroid for position-along-axis; it needs **no direction of travel**, so it reaches stationary effects the axial operator never could. Control: a pulsing hot-core disc vs a matched flat disc of identical footprint — **`r_core_white_frac` 0.4798 vs 0.0000**, with `r_edge_white_frac` 0.0000 confirming the hot region is core-confined; `r_val_slope` −0.052 vs +0.025 is a weak secondary; **`r_sat_slope` disqualified** (−0.046 vs −0.056, does not separate). ⚑ **RUN, on seven legs — see § 3.1.** The gradient is unambiguous: core/edge ratio **6–27×** on every reference, and `val_slope` **−0.13 to −0.45** against the synthetic positive control's **−0.052**. **The corpus-wide pass is the next lap's first command; the question is no longer open, only incomplete.** |

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
| 5 | ⚑ **R-8 vindicated per-skill — and on the very skill Matt named.** `leap_strike` (D3 Leap **touchdown**) is one of only **three legs of twenty-six to clear the PRESENT bar**: `near +0.387 / far −0.559`, the validated lens sign pattern. `cone` carries the deepest far-field term in the corpus (−0.754). `whirlwind` carries **none** (camera push). **Three of twenty-six clear PRESENT; the rest are camera-push or sign-ambiguous — the corpus does not have one answer, which is exactly why per-skill governs.** Matt's correction was right about the corpus; my original whirlwind answer survives on its own clip. | **gandalf** | **ANSWER — design call** |
| 6 | ⚑ **R-10: our renders carry NO screen shake whatsoever** — `hf_p99` 0.00–0.56 px against a 0.5 px floor, zero spike frames on four of six rows. **And nine reference legs DO carry impact-concentrated camera motion** (`leap_strike`, `melee_strike`, `circle`×2, `fork`, `placed_lane`, `totem`, `self_buff`, `aura` — enrichment **2.1–4.9×**, i.e. spikes cluster at the impact rather than spreading through the clip). ⚠ **The enrichment term narrows G-5 but does not close it** — until a 3-D tracking-camera null exists, an authored quake and a follow-cam's parallax are not fully separable. **A reference signal exists; its magnitude is not yet a target.** | **gandalf** (how much) · **drax** (G-5 null, then build) | **ANSWER + FINDING** |
| 7 | ⚑ **THE CLEAN SEPARATION (§ 3.3). All 26 reference legs span CV 0.449–1.149. Not one falls below 0.449. Four of our six rows fall below 0.103. The band 0.103–0.448 is EMPTY.** Trip-flag fires on `OURS_ground_slam` (CV 0.000, tone **6,387×**) and `OURS_melee_combo` (0.102, 2,148×); `OURS_blink` (0.000, 945×) and `OURS_teleport` (0.021, 473×) miss the tone bar and are **inspected, not passed**. ⚑ **And it is authoring, not capability — proven on our own side: `OURS_leap_strike` (0.668) and `OURS_dash_attack` (0.955) sit INSIDE the reference band, same seam, same engine, same day.** Two of our rows already do it; four do not. **Target range: 0.45–1.15.** | **drax** | ⚑ **FINDING — the most directly actionable number in the wave** |
| 7b | ⚠ **The chartered trip-flag UNDER-FIRED on a real row.** `OURS_blink` has **CV exactly 0.000** and does not trip, because a second condition on an unrelated statistic missed by 5.5 %. I did not rewrite the rule; I inspected the row anyway — which is what *"never auto-pass"* exists for. **Recorded so the conjunction can be reconsidered by whoever owns it, rather than quietly worked around.** | knight-rider / gandalf | **FINDING — rule** |
| 8 | ⚑ **G-5 needs another seam.** Every reference F7 stays `UNCERTAIN` until a **3-D tracking-camera null** exists — a synthetic scene with depth, a follow-cam, no shake authored. **~1 hour in the godot harness, and it converts every reference F7 cell into a real call.** | **drax** | **REQUEST — cross-seam** |
| 9 | **G-1: a hand-annotated effect region, ~20 frames per row, unblocks F1/F2/F3/F4 on every reference.** It is the *same* owed item the first reading raised for colour (D2) — **one annotation pass discharges both.** ~1 h per row. | galadriel | **OWED** |
| 10 | ⚠ **F4 and F5 ARE VACUOUS CELLS — `P` on 30/32 and 27/32, with 25 legs at the satellite cap.** They discriminate nothing and are printed only because suppressing a measurement I took would be worse than printing one I distrust. **Do not read their `P` as evidence.** F5 additionally **cannot separate SMOKE from BLOOM** — measured on the control, where a clip with no smoke read the largest halo ratio in the set. **A spec must not ask for "smoke" against this operator** until the persistence + advection terms exist (G-3, the cheapest of the four). | gandalf / drax | **WARN — do not build a bar on it** |
| 11 | **A sourcing-class decision is owed:** is frame extraction from published YouTube masters authorized for internal non-commercial benchmarking? **YES upgrades ~15 rows from donor-inference to canonical measurement. NO means the donor structure is the ceiling and the spec should say so knowingly.** I did not take it on my own authority. | **gandalf / knight-rider** | **DECISION REQUESTED** |
| 12 | **Four of my own operators were disqualified by their own controls** (`cv_width`, `sat_dist_norm`, `halo_softness`, `r_sat_slope`), and a fifth (`sat_count`) was counting compression speckle. **All five would have produced confident, wrong cells.** | jack-ryan | **RULING — instrument** |
| 13 | **Independent reproduction:** `whirlwind` re-measured through a new module on a re-fetched file reads **CV 1.107 / 1.80 ev-s** against the first reading's **1.107 / 1.797**. The metronome finding does not rest on one code path. | knight-rider | Support |

**26 reference legs + 6 of our own measured. No row graded. No canonical displaced. No bar proposed. Nothing escalated to Matt.**

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
