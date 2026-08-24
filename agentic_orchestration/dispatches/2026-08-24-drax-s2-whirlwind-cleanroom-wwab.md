# Dispatch — 2026-08-24 — drax — `whirlwind` CLEAN-ROOM mint (the WW-AB experiment)

**Status:** PENDING — **GATED on RT-4 pre-flight clearing** (see § Gate below)
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-24 — ruling **L-37**, verbatim: **"ADOPT but hide."**
**Pattern:** B — **and it MUST be a fresh, dedicated session.** See § The clean-room condition.
**Position in wave:** you mint clean-room → galadriel gates the minted artifact → **gandalf DRIFT-CRITIC audits the LINEAGE** (verifies no quarantined artifact was read) → **Matt compares the two builds side-by-side and picks.**

---

## Context — read this, because the protocol only makes sense with it

`whirlwind` is the run's **most owner-invested row and its thinnest pixel evidence.** Matt's criterion of record (L-19) was articulated *about this move*. Not one whirlwind candidate in the entire corpus yields a frame-verified read — the incumbent is a title card, two archival donors are 120×90 placeholders, one archive is behind a Cloudflare challenge. The row's evidence tier is `OWNER-ATTESTATION + DOSSIER-TEXT`, and the spec says so plainly rather than dressing it up.

Two whirlwind artifacts will exist at wave end, **by design**:

1. **The adopted lineage** — an existing human-in-the-loop build is `whirlwind`'s binding-of-record lineage (ADOPTED per L-37).
2. **This build** — minted **clean-room**, from **T-A § 3.1.12 ALONE**.

**Matt then compares agent-built-without-human-in-loop against human-in-loop, side by side. Whichever he prefers ships; the comparison is banked either way.** This is the run's thesis put to empirical test, and it becomes **the calibration datum for every other row's expected quality.** That is why the isolation matters more than the convenience of reading prior work: a contaminated build answers no question at all.

---

## THE CLEAN-ROOM CONDITION — binding, and the reason this is its own dispatch

**Start a FRESH session for this dispatch.** Do not run it inside a session that has already been reading whirlwind prior art. Clean-room is a property of what this session has *seen*, not merely of what it copies.

### QUARANTINE LIST — you are FORBIDDEN to read any of the following

- **SB-1 A2-series cells**
- **The CPB shaders**
- **All `vfxbo_*` scripts**

Do not open them, do not grep them, do not read them "just to check what not to do," and do not read notes, ledger rows, commit messages or diffs that describe their contents. **If you have already read any of them in this session, STOP and report to knight-rider — a fresh session costs minutes; a contaminated comparison costs the experiment.**

If you encounter a quarantined artifact incidentally (a search result, a directory listing), that is not a violation — **reading it is.** Note the encounter and move on.

**gandalf DRIFT-CRITIC audits the lineage of this build and verifies no quarantined artifact was read.** Declare your reading honestly in the completion record; an honest disclosure costs nothing and a concealed one voids the datum.

---

## What you build FROM (this is the whole permitted input set)

**T-A § 3.1.12** in `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` (**STATUS: SEALED**; the STATUS line governs the filename), **plus** the spec's general law that binds every row: § 1 (design law digest), § 1.1 (L-19 owner criterion), § 1.2 (style register), § 2.3 (the seven P0-b constraints — your own probe's findings), § 3.0 (column semantics).

Plus the row's own named evidence, which § 3.1.12 points at directly:

- **The measured cadence data** — `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2**, frameset `ww-native-eor1`. ⚠ **This file is labelled a NEGATIVE STYLE ANCHOR and it is also the run's ONLY POSITIVE TIMING ANCHOR. A builder who reads "negative anchor" and closes the file loses the only quantified whirlwind timing and geometry numbers in the entire corpus.** Verbatim from the semantics block:
  - **`spin_up_s: 0.70` · `spin_down_s: 0.80`** (measured at 60 fps from unmodified native pixels)
  - **radius 150–160 px at 1080p ≈ 1.9× standing character height, constant**
  - anchoring: *"rigidly player-centred; no lag, no elastic trail, no lean into movement vector"*
  - movement while channelling is permitted and used constantly at full speed
  - **occlusion: renders over the caster's lower body and over enemies inside it — THE DEFECT TO CORRECT.**
- The row's PRIMARY and archival donor references as named in § 3.1.12, subject to the RT-4 gate below.

---

## The design core of the row — do not lose it under implementation

- **Emitter geometry:** caster-centred, **rigidly player-anchored. The CHARACTER rotates and the payload is the character's own weapons.** Layers: **(a) weapon-trail highlights synchronized with the weapon animation, (b) localized hit effects on contact.** The reference property, itemized: *"blade highlights synchronized with the weapon animation… localized hit effects preserve the rotating silhouette without obscuring nearby enemies."*
- **L-19: `physical-cause` — this archetype IS the L-19 exemplar.** Matt's words, verbatim, about this move: the good version reads as *"a plausible physical manifestation of exceptionally rapidly spinning weapons, clashing into flesh, bone and armor"*; the bad version reads as *"a generic magical aura that happens to be spinning along with the character."*
- **Tier-1 surface class: `TRAIL-BOUNDED`.** **Tint rides the WEAPON TRAIL and the CONTACT SPARK. It must NOT expand into a caster-surrounding field.** 82 % of this archetype's referent members are element-agnostic — the highest in T-A after `leap_strike`. **A tinted weapon-trail stays physical; a tinted field IS Eye of Reckoning.** This row is where that consequence is least negotiable.
- **Lifecycle:** `sustained` channel with **measured ramps** (0.70 s up / 0.80 s down). Beat model `channel`.
- ⚠ **ZERO windup coverage exists anywhere in the corpus for this archetype.** Both archival donors are `windup = N`; the incumbent is UNRATED by deliberate refusal; the negative anchor's windup is *"PRESENT but it is a fade-in, not a windup — opacity ramps, no anticipation pose, no charge tell."* **For a channel-lifecycle archetype at our telegraph-literacy bar, this is a real gap and it is carried openly.** Partial compensation is the measured ramp pair. **Whatever you author for windup is an authored decision — mark it as such in your mint note rather than implying a reference supports it.** (Run-wide, two strong windup donors exist and are reusable across rows: D3 Condemn's three-second charge and PoE Demonic Leap Slam's anticipation crouch.)

---

## Math-before-code (Discipline #1)

Mint note at `agentic_orchestration/drax/notes/2026-08-24-s2-whirlwind-cleanroom-mint-note.md`, before minting:

1. Layer decomposition — which node/material carries the weapon-trail highlight and which carries the contact response
2. How the 0.70 / 0.80 ramps are realized, and against what clock
3. Radius derivation from **1.9× standing character height** at our character scale — show the arithmetic
4. **What you authored for windup, explicitly flagged as authored-not-referenced**
5. What takes the tint and what must not (the `TRAIL-BOUNDED` clause, translated into concrete properties)
6. **Your clean-room declaration** — the reading you did, stated affirmatively

---

## Scope

- [ ] Fresh session; quarantine honored
- [ ] `whirlwind` base binding minted from § 3.1.12 alone
- [ ] Measured ramps honored (0.70 s / 0.80 s); radius ≈ 1.9× character height, **constant**
- [ ] Rigid player-anchoring — **no lag, no elastic trail, no lean into the movement vector**
- [ ] Movement while channelling works at full speed
- [ ] **THE DEFECT TO CORRECT is corrected:** the effect must NOT render over the caster's lower body, and must NOT obscure enemies inside it. This is the single most concrete quality delta available on this row — the negative anchor exists precisely to name it.
- [ ] Tier-1 tint demonstrated on trail + contact spark **only**
- [ ] C-1: shadow casting disabled on additive/emissive meshes
- [ ] Captures rendered at stage albedo **0.085** (C-3) for the gate
- [ ] Mint note incl. clean-room declaration, committed before minting
- [ ] `AGENT_STATE.md` updated; tag `drax/v-s2-whirlwind-cleanroom-1`

## Cross-seam contract change? (Principle 6 gate)

**NO.** **Round-trip: not applicable — no cross-seam contract change in this dispatch.** Godot-side presentation authoring only.

## Acceptance criteria

- [ ] The minted effect reads as **action-CAUSED**: spinning weapons meeting flesh, bone and armour — not an aura that happens to spin
- [ ] The tint does **not** expand into a caster-surrounding field at any element variant
- [ ] Occlusion defect corrected — caster's lower body and enclosed enemies remain readable
- [ ] Clean-room declaration present and honest; **no quarantined artifact read**
- [ ] Windup treatment present and explicitly marked authored-not-referenced
- [ ] Round-trip: not applicable
- [ ] Tag `drax/v-s2-whirlwind-cleanroom-1`

## Quality criterion

**Game-quality goal:** the archetype Matt cares most about must read as *physically caused*. And beyond this one row, this build is the **calibration datum for the whole factory** — it answers "what quality does an agent-built binding reach from spec alone?" That answer sets expectations for the remaining 23 rows.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- You have already read a quarantined artifact in this session — **STOP, report, restart fresh**
- § 3.1.12 alone is genuinely insufficient to build from — say exactly what is missing; **do not close the gap by reading prior art**, because that converts the experiment into a normal build
- Honoring `TRAIL-BOUNDED` makes the effect unreadable at the gameplay camera — an RT-2 finding, not a licence to widen the tint
- Acceptance criteria can pass while the effect still reads as an aura that happens to spin

## Out of scope

- **Any tier-2 flourish.** A-2 is ADOPT+WW-AB; the flourish layer is not this dispatch.
- **Comparing the two builds.** **Matt does that. Not you, not galadriel, not gandalf.**
- **Reading, referencing, or "harmonizing with" the adopted lineage.** That is the entire point.
- Re-hunting `3BnHvNZ_4YM` — closed as `TBD-UNRESOLVABLE` at L-30/L-32. **Do not re-run that hunt.**
- Other T-A rows.
- Modifying `Assets/` (read-only).

## Gate — RT-4 must clear before you mint

**RT-4** (spec § 6.1) is a pre-registered revisit trigger fired ahead of this dispatch: *verify archival whirlwind-donor playback BEFORE minting.* The incumbent carries an **`effect-internal`** confound (Dust-Devil cyclone add-ons that are a build modification rather than base-skill VFX, plus cosmetic wings on the very rotating silhouette that IS the reference). Effect-internal confounds are **not croppable** — subtracting them requires two structurally confound-free archival references to subtract against.

- **BOTH-LIVE or ONE-LIVE** → proceed; knight-rider records which donor carries the subtraction basis.
- **BOTH-FAIL** → the Dust-Devil confound is **un-subtractable**, the row's confidence drops materially below what "PRIMARY" implies, and **this dispatch does not fire until knight-rider re-shapes it.**

**Check the RT-4 result before you start.** Do not assume it cleared.

## References

- Sealed spec § 3.1.12 · charter L-18/L-19/L-30/L-32/L-34/L-36/L-37
- `gandalf/requests/2026-08-24-knight-rider-carveout2-step2-build-wave.md`
- RT-4 pre-flight: `legolas/notes/2026-08-24-rt4-whirlwind-donor-playback.md`

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **pending at authoring time** — Gate-1 batch review, 2026-08-24. **Gate-1 must specifically confirm this brief does not leak quarantined content.**
