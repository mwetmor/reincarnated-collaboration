# Dispatch — 2026-08-25 — galadriel — REFERENCE FRAME-FORENSICS: build the instrument that can see depth

**Status:** PENDING
**From:** knight-rider (Step-2 build wave, conductor)
**To:** galadriel (visual-perception seam)
**Pattern:** B — needs its own session; this is instrument construction, not a measurement pass
**Occasioned by:** Matt, 2026-08-25, verbatim (recorded in full because the whole dispatch is downstream of it):

> *"the VFX thus far are basic representations but they lack ALOT of the depth of the original VFX that we're working from. For example, in my HITL Whirlwind run, we added TONs of internal VFX such as claw and sword metal scraping timing and intermittent laser effects, alternating through a specific color range as well as smoke and wind effects. We could probably do well to add cavitation or gravity appearence effects to show distortion of the environment in some of these. But all of this can be found in the originals if we slow it down and statistically pick each clip apart for what the originals are doing."*

> Also: *"Drax and Galadriel both need to zoom in and pause more on each individual frame."*

---

## ⚑ 0. The finding this dispatch exists to remedy — read this before anything else

**Matt's critique is not a disagreement with your gates. It names a region your gates do not cover, and I can show that from the record rather than assert it.**

The clean-room whirlwind (`drax/v0.1-s2-whirlwind-cleanroom-1` = `1692d6e`) passed on two terms:
`lower-body occlusion 1.78% over noise floor` and `tint TRAIL-BOUNDED across 4 elements`.

Those are **a coverage fraction and a colour bound.** Neither is capable of observing:

- **cadence** — the rate at which discrete internal events fire
- **intermittency** — whether an element is continuous or pulsed, and on what interval
- a colour **CYCLE** — a bound says "inside the trail palette"; it cannot distinguish a *static* tint from one *alternating through a range*, which is precisely what Matt describes
- **scrape timing** — specular events keyed to weapon/claw contact
- **smoke / wind** — advected, non-emissive, low-contrast media
- **environmental distortion** (cavitation, gravity-lensing appearance) — a *background* displacement signature, not a foreground emitter at all

**An effect with zero depth would have passed those two terms identically.** That is the whole finding. The instrument returned cleanly and returned an answer to a different question — the shape this session has now hit four times (`factory/permissions.py` non-defect; `git diff HEAD~1`; the crop that could not see the aim difference; this).

**The corroborating record, which makes this stronger than my opinion:** the WW-7 v2 gate-2 receipt (`galadriel/captures/2026-08-16-sb1-gate2-clip/receipt.txt`, 2026-08-16) already states the principle, about this very comparison:

> *"GATE 2 (article FEEL — density, palette knee, cadence read, FX draw) is judged on **MOTION**, and a still cannot carry it."*

**That standard was applied to the HITL arm and not to the clean-room arm.** Your own seam wrote the rule nine days ago. This dispatch is not introducing a new idea; it is finishing one that was left half-applied.

## 1. What you are building

**A per-frame decomposition instrument that runs identically on (a) a reference clip and (b) one of our renders, and emits comparable numeric SERIES — not verdicts.**

The output of this dispatch is **an instrument plus a first reading**, not a PASS/FAIL on any row. Do not grade anything. The point is to make depth *measurable* so that a later gate can have terms.

### 1.1 The four series (this is the proposed set — you own the final selection, see § 4)

| # | Series | What Matt's language it makes measurable |
|---|---|---|
| **S-1** | **Discrete-event count per frame** — connected-component count above a local-contrast threshold, in the body-adjacent annulus | *"TONs of internal VFX"* — density of distinct internal elements, vs one big blob |
| **S-2** | **Per-frame hue histogram** over the effect mask (not a bound — the full distribution, frame by frame) | *"alternating through a specific color range"* — a cycle shows as periodic mass-migration between hue bins; a static tint does not |
| **S-3** | **Inter-event interval on specular/luma spikes** — 99th-percentile luma events, timestamped, then the interval distribution | *"claw and sword metal scraping timing"*, *"intermittent laser effects"* — intermittency IS an interval distribution; a continuous effect has none |
| **S-4** | **Optical-flow field**, split into (i) near-body and (ii) background-plate regions | *"smoke and wind effects"* (near-body advection) AND *"cavitation or gravity appearence effects to show distortion of the environment"* — environmental distortion is by definition **background** displacement uncorrelated with camera motion. If the reference has it and we don't, S-4(ii) is where it shows. |

**S-4(ii) is the one I most want a real answer on**, because Matt raised distortion as a *suggestion* (*"we could probably do well to add"*) rather than an observation. **The instrument can tell us whether the originals actually do it** — which converts a design guess into a measured property of the referent. Report it either way; a clean "the references show no background displacement signature" is a valuable result and should be stated as plainly as a positive one.

### 1.2 The comparison shape

For each clip pair, emit the four series for **reference** and for **ours**, at matched frame rate, and report the *difference in the series*, not a similarity score. Matt's word for the method is **"statistically pick each clip apart"** — that is a decomposition, and a single scalar re-composes it, which is the thing to avoid.

## 2. Corpus — what to run it on FIRST

**Start with `whirlwind`, because it is the only row where both a human-in-the-loop build and a clean-room build exist**, which makes it the calibration case for everything else.

| Leg | Object | Location / provenance |
|---|---|---|
| **Reference** | D4 Whirlwind official `3BnHvNZ_4YM` (P3 canonical) **and** the RT-4 donor `whirlwind.flv` — Blizzard D3, already proven fetchable at HTTP 200, 6,872,672 B, 1280×720, **374 frames** | `galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` row 26; `legolas/notes/2026-08-24-rt4-whirlwind-donor-playback.md` |
| **Ours — HITL arm** | `ww7-gate2-cadence-ab-plk0665-1920x1080.mp4`, 12,749,012 B, sha256 `7e9764e3fc53096128ef6b64d2a624962c1f3df599ae5e4aaf311347c0b828ca` | `galadriel/captures/2026-08-16-sb1-gate2-clip/` — untracked on disk, Class-E |
| **Ours — clean-room arm** | ⚑ **DOES NOT EXIST AS MOTION.** Stills only (`harness_logs/wwcr_2026-08-2*`). | queued to drax behind 3A — see § 5 |

**Then extend to the P3 canonical picks** for rows already sealed, so the wave learns its own depth-deficit *before* minting 13 more rows against a gate that cannot see it. The canonical URLs are in the P3 selection gate § 3 and the 30 dossiers at `research/vfx-p2-dossiers/dossiers/`.

⚑ **Precedent for pulling reference media:** RT-4 fetched Donor A live and decoded it to frames. This repo has done this before; it is not a new capability and does not need a new authorization. **Read-only, ADR-006 holds** — fetch and decode to a scratch/ignored path, do not commit media.

## 3. ⚑ Disk — Discipline #1.1 pre-fire resource-bounds projection is MANDATORY here, and I am the reason it says so

`/System/Volumes/Data` sat at **2.7 GiB free (0.6%)** earlier today and **halted a live build wave mid-tranche.** Matt cleared it to **66 GiB**. **I ran a projection and declined to fire** only *after* the failure; the discipline exists because I skipped it before.

**Before decoding anything:** project frames × resolution × bytes-per-frame against `df -h`, write the projection down, and **do not fire if it does not fit with margin.** 374 frames at 1280×720 is trivial; a 2,500-second 1920×1080 source is not. **Decode at reduced resolution and/or sampled frame rate where the series permits it** — S-2 and S-3 tolerate downscale far better than S-1 does. Say which you chose and why.

## 4. Where I am explicitly NOT instructing you — and want you to overrule me if the measurement says so

**§ 1.1's four series are my proposal, authored by an orchestrator, not by the perception seam.** I have named the mapping from Matt's language to a measurable because a dispatch that just said "measure depth" would be unactionable. **You own the instrument. If a series is the wrong operator for its phenomenon, replace it and say so plainly.**

Specific places I expect to be wrong:

- **S-3's "99th-percentile luma"** is a guess at a threshold. It is exactly the kind of literal bar that `#80 cl. 2(a)` says must be **derived**, not asserted. Derive it from the corpus's own noise floor.
- **S-1's connected-components** may fuse adjacent emitters into one blob at our render's scale and split one emitter into many at the reference's. If the operator is scale-sensitive in a way that makes the two legs incomparable, **that is a finding and it outranks the number.**
- **S-2 assumes hue is the carrier** of "a specific color range." It may be saturation or emissive intensity.
- Compression artifacts in a YouTube-sourced reference will contaminate high-frequency series. **Name the contamination; do not quietly absorb it.**

`#79` cl. 6 binds here as everywhere: **a mechanism claim carries an empirical-test obligation before relay.** I have been refuted three times this session on exactly that, once by Matt. Test before you report.

## 5. Cross-seam — what is NOT yours

- **The clean-room whirlwind MP4** is drax's to render, queued behind 3A (godot lane is serial per wave-record § 3 ruling 5). **Do not render godot content.** If your first reading needs it and it is not there, produce the reference-side and HITL-side reading and mark the third leg OWED.
- **Authoring new VFX** (lasers, scrape timing, smoke, cavitation) is drax's seam. You produce the *target numbers*; he authors against them.
- **The clean-room QUARANTINE remains binding** on any future clean-room build. Your measurement of the *existing* clean-room artifact is post-mint and does not contaminate it — but do not feed HITL-arm findings into a future clean-room dispatch without routing through gandalf.

## 6. Acceptance criteria

1. An instrument that runs on an arbitrary clip and emits the series as machine-readable data (per-frame rows, not summary stats), committed under your seam
2. A **first reading** on the whirlwind reference leg + the HITL arm leg, with the clean-room leg marked OWED if unavailable
3. The threshold/parameter for every series **derived from corpus data and shown**, not asserted (`#80 cl. 2(a)`)
4. A pre-fire disk projection recorded before any decode (§ 3)
5. An explicit statement, per series, of **what it cannot see** — the failure this dispatch exists to remedy was an instrument whose blind spot was never written down
6. A plain answer on S-4(ii): **do the reference clips exhibit background/environmental distortion, yes or no**
7. Media stays untracked; notes and instrument code are committed

## 7. Quality criterion

**Game-quality goal this dispatch serves:** the difference between an effect that reads as *"a spinning aura"* and one that reads as *a warrior tearing the air apart* is almost entirely internal detail and its timing. Matt can see that difference instantly and the wave's gates currently cannot see it at all. **Every row minted before this instrument exists is minted blind to the thing the player will actually judge.**

**Refutation conditions** (surface if any apply):
- The series in § 1.1 cannot be computed comparably across a compressed YouTube reference and a clean Godot render — in which case say so and propose what CAN be
- The depth deficit is not measurable in the frames at all and is a **model/asset capability** limit rather than an authoring one — that is a much bigger finding and should halt-and-route rather than be worked around
- Acceptance criteria can pass while producing series nobody can author against — the output must be *actionable by drax*, not merely correct
- This dispatch pre-commits to "our renders lack depth" as a conclusion. **It must not.** If the measurement says our renders match the references on these series, **report that**, and the finding becomes that Matt's read and the numbers disagree — which is a real and useful result, not a failure
- A series I named turns out to be a re-composition (a single scalar) in disguise, defeating the "pick it apart" method
