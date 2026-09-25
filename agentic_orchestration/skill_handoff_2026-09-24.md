# Session hand-off — Run KC2-PLAY, folds F1–F3 + the audit lap

> **Written by gandalf (RUN-CONDUCTOR) at Matt's request, 2026-09-24, covering the working session of 2026-09-21/22.**
> **63 commits · charter ledger KP-59 → KP-81 · 4 discipline landings · 1 standing policy · 1 pack cut.**
> Charter + full ledger: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`. **This file is a router, not a substitute** — every claim below is traceable to a KP row, and where they disagree the ledger governs.

---

## 0 · START HERE next session — three lines

1. **Read this file, then the charter ledger from KP-59 forward.** If the conversation has been compacted, re-read `.claude/agents/gandalf.md` and `operating-procedures/gandalf.md § 2` from disk first — charter-freshness rule.
2. **Ask Matt for four rulings** (§ 3). Two are cheap; **Q85 is now urgent and blocks the next graded run.**
3. **The first unblocked work is the prereg `v1.6` re-derivation** (§ 4.1). Everything else can follow it.

---

## 1 · What Matt has in his hands

**A playable build of the referent fight**, double-clickable, no editor and no terminal:

```
~/Games/reincarnated-godot/desktop/KC2Play/build/desktop/KC2Play.app
```

207 MB, macOS universal, quarantine clear. Opens at **wave 151** from the cp150 fixture. Rebuilt four times this session; the current build is godot `00b1689`.

**Binds:** RMB held = Eye of Reckoning · LMB = Blitz + move-to-cursor · `1` potion (manual) · `2` Vire's Might · `3` War Cry · `4` Rune of Rush (**mis-named — see § 5**) · numpad `1`–`4` also live · `Z` zoom · `N` damage numbers (hits **and** ground) · `R` restart · `H` the card · `C` capture. **Quit with Cmd-Q** — a kill leaves a torn telemetry line.

Telemetry: `~/Library/Application Support/Godot/app_userdata/KC2Play/telemetry/`, one file per life.

**Twelve honesty headlines** at open and on `H`, each with a register row id; the skill bar repeats the relevant one per slot. As of F3 the card is **filled at draw time from the arena's own data** — *it can only be wrong if the room is wrong.*

### The two things still owed to Matt's eye

- ⚑ **Hold RMB in a pack for ten seconds: does the ring REACH what it should?** The ring draws at the model's **3.0 m**; the spin art is composed for **0.4446×** that, and **neither was resized** — a probe now reds if a later hand makes them agree. **If the reach feels wrong, we need to know whether he is objecting to the RING or the ART; those are two different repairs.** (KP-59, KP-69)
- **Does the room sit right at t = 0** — are the five mouths where he would expect the doors? The frame registration is drax's declared choice, made alone. (KP-59)

---

## 2 · What happened, in one pass

**The build got into his hands and he played it**, which is the whole reason the session was worth having: **every one of his six reported defects was real, and three of them were things no instrument in the build could have caught.**

| his report | what it was |
|---|---|
| walk animations backwards | a full 180° in one expression — **not** the Y-inversion I hypothesised |
| too little energy per cast / per spin | **two causes**: the port paid an invented off-channel income (+175/s), and **all four bound skills are free on the energy axis** |
| whirlwind VFX absent | **never ported** — the staging script copied the cells and the fit's *numbers* and left the effect behind. *The build carried the measurement of a thing it did not have.* |
| enemies stuck in the spawn zone | **still open** — NOT the no-data path (`spawn_inert: 0` in his own telemetry). A genuine port defect. |
| haphazard spawns | **decoded truth**: `p05` sits 7.16 m from his spawn while the others are at 33–36 m |
| summons unkillable / taking damage | his own summons; they *cannot* take damage (no friendly faction exists) — he was seeing damage floats anchored at screen centre |

**Then Matt asked the question that reframed the run:** *why do we not have the data from the oracle and sim for these mechanics?* Answering it honestly produced **the Commission Rule** (§ 6), and everything after that follows from it.

---

## 3 · ⚑ BLOCKED ON MATT — ask for these first

| # | Ask | Cost | State |
|---|---|---|---|
| **T30** | ⚑ **Mount the `reincarnated` external volume.** The EoR footage is **not destroyed** — `/Volumes/reincarnated/…/eor-test-2/video/`, `479,438,089 B`, sha256 `4c60960d…4de8`, identity already pinned. `/Volumes` holds only `Macintosh HD`. **~1 minute.** | trivial | **Deferred by Matt this session.** Unblocks tier-C (side-by-side against his play) and any re-measurement. |
| **Q85** | **Does the graded-run cap reset at the v3.4 re-base?** Rec **YES**. ⚑ **Now urgent:** a new prereg version against a new pack *is* a new graded-run context, and this must come from outside the run. | one word | **BLOCKING the next graded run.** |
| **Q83(b)** | Retire `TA-X-06`? ⚑ **Now priced, and he should see the price before ruling:** inertness rows work only in **pairs** — retire it and **a port with NO ARENA FOLD AT ALL passes every remaining `W1` EXACT row.** Not a reason to keep it; a reason to know. | one word | open |
| **Q83(c)** | `TA-X-07` tolerance | one word | open |
| **S1 / S4 / S5** | Arena layout · the six pools · the world beyond the walls. **The Astra cathedral burst is parked on exactly these three and nothing else.** | a sitting | **Matt parked the art side deliberately.** |
| **T24** | One screenshot **while channelling EoR**, with a landmark legible on the minimap | ~10 s | open — settles arena scale (`u = 0.285` is a registered choice) |
| **T31** | Restore an Edition-III Grim Dawn tree | — | open |

**Also awaiting his veto (process-tier, non-blocking):** `#86`, `#87`, `#75` cl. 1(b), `#76` cl. 5, `#78` cl. 7. ⚑ **jack-ryan asked explicitly that the MINT RATE be put in front of Matt at run close rather than discovered by him** — four disciplines in two days. He is not slowing it (every merge test genuinely failed) and neither am I; it is a datum Matt should own.

---

## 4 · Owed work, in dependency order

### 4.1 · The prereg `v1.6` re-derivation — do this first

v3.4 makes **`TA-X-25(c)` unpassable** and sends **`TA-B-15`'s two pinned points to 0.0000**. ⚑ **Carried forward unchanged they RED A CORRECT PORT ON EVERY ARM.**

**Ruled (KP-80): this is a SUBSTRATE change, not a goalpost change — the goalposts did not move, the ground under them did.** Re-derive as `v1.6`, seal `v1.5`, diff explicit per row, **D4** (the note commits alone, zero code), landing **before** any graded run touches the new pack. Owner: gamora.

### 4.2 · The live pack defect

⚑ **Nine records in the shipped pack carry campaign attacks that the Crucible strips** — in the direction that makes the board **harder** than the referent. Lifted 2026-08-12 under `merged()`, named at W46 with `in_338=false`, **not re-lifted** (a separate call, correctly not taken). **This is the right shape to test `OPEN-UNKILLABLE` (~30×) against.**

### 4.3 · Owed by the cut / before graded run #2

- **G-3's port-side half** — the emission discharged the emitter side only, and said so.
- **jack-ryan's `register_choice` census repair.** ⚑ **Correction to his own framing:** only `kc2_runtime/` is committed; the two vendor trees are gitignored and reproduced by `tools/vendor.py`, so it is **a single-tree edit plus a re-vendor, not three edits.** Two limbs: assert arg 5 is a behaviour identifier, not free text; and fix the denominator — `ROOT` cannot see `kc2_play/src/`, so a population reported as 13 is at least 15.
- **T-A as a DIAGNOSTIC, not graded** (KP-76) — deferred until the energy thread settles, because grading the port against an oracle mid-correction spends the run to learn nothing.

### 4.4 · Energy — the largest open thread

**Two terms, separately owned, both identified:**

- **SLOPE** — `leech_uptime` is pinned at **1.0**; the honest end state is a **disjoint union `[0.1933, 0.2763] ∪ [0.3293, 0.4123]`**, verdict **`UNPINNABLE-FROM-COMMITTED-PIXELS`**. Math note written (D4, zero code). **No constant moved.** ⚑ **The midpoint of the range the audit originally published, 0.2980, falls in the excluded gap** — split-the-difference would have produced a number no reading of the evidence supports.
- **AMPLITUDE** — C-2 delivered the four per-cast costs (**43.2 / 27.9 / 106.2 / 59.4** after ×0.90, ≈**59.3 /s** at perfect uptime = **79 % of income**). **The pack charges zero for all four and the absence was never registered.** This is the term that closes drax's measured 1.1 %-of-bar excursion against the referent's 7–12 %. **Not yet folded.**

**Unadjudicated and routed:** the pixel gross re-derives to **`[104.1, 112.0]`**, containing **neither** 176.4 nor ≈190 — *a third number measuring a different object*, after SPEND/SPILL split every tick at **zero residual over 1,626 ticks**.

### 4.5 · Commissions open (issuing is sequencing, not a fresh ruling)

`C-4` (the 0.33 trigger — partly answered), `C-5` (the Guardian's `IMPL` cell), `C-6` (`OPEN-UNKILLABLE`). `C-1` closed as *searched*-unlocated with a ~19.0 /s residual; **`C-3` SOLVED** — the 0.90 factor is **Seal of Annihilation**, read out of Matt's save.

### 4.6 · Smaller, named, not lost

Rune naming (§ 5) · the 7 T-B warrants' **affirmative half stays unfiled** until someone runs a set-level discrimination test · `TA-X-24` left bounded (needs a cross-seam read of drax's runtime) · **15 committed files carry DBR paths with no provenance column** (`CORROBORATED-NOT-PROVEN`; ⚑ the cheap instrument is a provenance column, not a re-derivation) · SurvivalMode inter-ordering `CONSISTENT-NOT-SOURCED` · `threat.py:115`'s duplicated `PLAYER_HP_MAX` literal · E/W shield-handedness (`R-C8-7`, **deferred by Matt**, flagged so nobody re-files it).

---

## 5 · ⚑ Corrections to the record — read these before citing anything from earlier

| claim | status |
|---|---|
| "the card doesn't enumerate summons" | **FALSE** — headline #4 since the first build. The row was true and written in *oracle vocabulary*; it never said what a summon looks like. |
| "the guard is structurally unreachable from production" | **FALSE** — 13 of 20 sites pass behaviour names; the guard fires at the founding defect's exact coordinates. |
| "the oracle and the footage agree; both disagree with the build" | **FALSE** — the band constrains **depth**, never **rate**. |
| "64.6 % of combat at the ceiling" | **`E ≥ 1560`.** True ceiling duty is **0.2801**. drax priced his build's 55.9 % against my wrong figure. |
| "`physique 74 / cunning 858 / spirit 74` can't be right" | **WRONG, and I was wrong about Grim Dawn.** Cunning is the physical-damage attribute; Physique was never the constraint. |
| "the above-ceiling energy reads are physically impossible" | **WITHDRAWN** by galadriel against her own note. |
| "key 4 is Rune of Rush" | **Rune of Violent Delights.** "Rush" is a different rune Matt does not have; the file path is misleading. **The build still mis-labels it.** |

⚑ **Four of these are mine, and three came from relaying a seam's characterisation as the run's record without opening the surface.** The conductor's seat is the last point at which reading the surface is still cheap. Next session: **derive, don't relay.**

---

## 6 · Governance landed this session

**THE COMMISSION RULE** — Matt's standing policy, `agentic_orchestration/gandalf/notes/2026-09-21-the-commission-rule.md`. *At a knowledge boundary in the referent, buy the knowledge; do not choose a value.* It converts a declared absence from a terminal state into **a backlog of things we have not yet bought**. Warranted by **absence of knowledge, not presence of symptom**; a **negative result is a result**; Law 3 governs inside a commission as outside it.

His rationale governs everything downstream: *a line in the sand that we have a referent battle system… so that this game becomes a join key and also its own game.* ⚑ **A fitted constant is a lie you can only tell once** — uninvertible, untransportable.

**And he overruled my Failure Mode 1**, correctly: *"I would rather start from an opaque referent that we know players had fun playing, than a perfect concept piece where fun is unknown."* Recorded in full, with my concession, in that file. **Failure Mode 2 stands and is untouched: a join key needs a SCHEMA, not a correct instance** — the pack shape is Grim-Dawn-shaped and nothing has tested whether its concepts survive a game with no energy.

**Disciplines:** `#86` (a refusal binds the STATE, not the frame it was rendered in) · `#87` (name the rival or write the warrant) · `#75` cl. 1(b) · `#76` cl. 5 · `#78` cl. 7. **The 33 warrants: 26 filed on their rows, 7 folded by galadriel, 1 stopped at the HALT.**

**Canon repair:** the engineering-disciplines count claim was in **24 files**, not one — every per-agent OP and skill told its agent at session start that there are 20 while the corpus ran to 87. Zero residual now.

---

## 7 · The shape worth carrying forward

⚑ **One defect fired six times today, across five seats, four of them by the rule's own author: a rule not applied to its own neighbourhood.** `T-1` already enforced `#87` in executable code and it was never asked of the energy band. The disciplines skill enumerated 20. My repair of it broke its own invariant one section below where I wrote it. drax's ≥2-non-hue-channel rule was enforced on the pair that prompted it and never the pair beside it. The tautology guard committed the defect it repairs on its first run. And galadriel's own words:

> *"The control that proved where the ceiling was, and the trace that climbed a hundred points above it, were printed four paragraphs apart in the same note, in the same hour, by me. Twice this run the instrument was already on the page. What was missing was somebody turning the glass on the work beside it."*

**jack-ryan's retrieval note, recorded as an open substrate item and NOT repaired:** four times this run a rule was proposed as novel that the corpus already held — twice by that rule's original author. ⚑ **The corpus is indexed by number and by trigger. It is not indexed by DEFECT SHAPE, which is the only key a proposer holds at the moment of proposing.**

That is the most valuable unsolved problem the session produced, and it is not a KC2 problem.

---

**Signed:** gandalf (RUN-CONDUCTOR). Run KC2-PLAY remains OPEN; no gate is failed, nothing is halted, and the build is in Matt's hands.
