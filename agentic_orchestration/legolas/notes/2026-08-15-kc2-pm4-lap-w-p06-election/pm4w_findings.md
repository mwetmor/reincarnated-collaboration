# RUN KC2-PM4 · LAP W — THE p06 ELECTION READ (the `R-V-1` video route) · FINDINGS

**Agent** legolas (UNKNOWN-RESEARCHER) · **Conductor** gandalf (RUN-CONDUCTOR)
**Fired under** `R-PM4-58 part 1` (Matt 2026-08-15, Q-a verbatim: *"I don't remember"*)
**Date** 2026-08-15 · **Discipline** GL-12 decode-never-estimate · full-64-hex digests (`R-PM4-55 part 2`)
**Preregistration** `PREREGISTRATION.md`, committed ALONE at `f4d20ef5` **before any frame was decoded**
(`L-46` git-attested-priority discipline, second use), sha256
`0e0b8b8068606c61157cf33404e40a61363f24935df56b648f4b98318d79a61b`.

---

## § 0 — THE HEADLINE

| | |
|---|---|
| **VERDICT** | **OFF — the p06 bonus spawn point was NOT elected in the recorded fight.** |
| **Carried by** | **D-A (start-of-run UI read)** — the recording reaches back to the Crucible start; the ENTIRE election sequence is on camera and the complete click record is frame-attested. |
| **Confidence** | **STRONG, not DECISIVE.** One named artefact would make it decisive and it is absent from the intake (`D-W-1`). |
| **Corroboration** | **D-C** returned **0 hits in 1 011 OCR observations over 127 frames** against the p06-distinct name sets on all seven declaring waves — a null in the same direction, but **not admissible as OFF on its own** (coverage is hovered-target-only) and **not counted toward the verdict**. |
| **D-B** | **NOT-USABLE**, as the prereg predicted it would be — and now *quantified*: p06 sits **49.4 – 79.3 m** from the dialogue position in all ten arenas, ~6× outside the camera frustum. |
| **What would overturn it** | `conversations/npc_event_01.cnv` binding `gd.survival.rewards.bonusChest` to the **"I wish to raise the stakes."** node or to the **"Start on Wave 150"** node rather than to a **"…can do better"** node. |
| **⚑ New decoded fact (records)** | The static `fx_eldritchrift_medium01` marks spawn points **1–4 in every arena, and never 5 or 6**. p06's rift is created **only** by the election. The 4-vs-5 rift signature is real and is the correct instrument for any future in-arena check. |
| **Fourth-mechanism finds** | **two, NAMED and NOT DECODED** (§ 6.1): spawn point 1 is **tier-specific**; the election emits **no on-screen notification**, by exhaustive tag census. |

**The one-sentence answer for `I-22`:** fold **`P06_BONUS_SPAWNS = False`** as the referent-true limb,
carry the STRONG (not DECISIVE) grade and the single named falsifier with it, and do **not** re-open
the +25.000 bodies unless the `.cnv` is obtained and contradicts this.

---

## § 1 — THE REFERENT REACHES BACK TO THE RUN START. IT WAS NOT KNOWN THAT IT DID.

`ffprobe` at instrument start: 1920×1080, h264, **60/1 fps, 1034.100 s, 62 046 frames**. Lap H-2 puts
the fought band 151–160 at **683.0 – 866.0 s**. The prereg therefore registered `t ∈ [0, 683)` as
**available but unknown**, and D-A's contact-sheet scan (1 frame / 5 s, 138 frames, cadence fixed
before the scan) as the first instrument. It found this:

| span (s) | wall clock | content |
|---|---|---|
| 0 – 35 | 21:37:25 – 21:38:00 | Crate splash → main menu → character select |
| 40 – 48 | | loading screen |
| 50 – 440 | | in the Crucible lobby; character sheet, skill trees, devotion constellations |
| 446 – 562 | | **Defense Site** panels — beacons/banners priced, one Defense Site upgraded |
| **565.0 – 573.7** | 21:46:50 | **Lokarr root dialogue (S1)** |
| **573.8 – 682.05** | 21:47:00 – 21:48:47 | **Lokarr wager dialogue (S2)** — held open, unchanged, for **108 s** |
| **682.10** | | dialogue gone; **run starts** |
| 683.0 – 866.0 | | the fought band (Lap H-2) |

**The HUD clock is an exact time base**: it reads `9:47:25 PM` at t = 600.0 s, and the file is named
`…2026-08-05 21-37-25`. **t = 0 ⇔ 21:37:25**, to the second. HUD also reads difficulty **Gladiator**
and arena **"Crucible of the Dead"**.

---

## § 2 — D-A: THE ELECTION SEQUENCE, READ FRAME BY FRAME

### 2.1 The two dialogue states, verbatim (Vision OCR, `.accurate`, correction OFF)

**S1 — root** (`t = 565.0 – 573.7`):

> **Lokarr, Master of the Crucible**
> Greetings and welcome to my Crucible. I have seen your potential, and I am most intrigued. So I've
> summoned you here to battle for my amusement. But I am not a cruel master. Succeed, and you shall
> be rewarded with vast wealth. Fail, and know only my scorn.
>
> ✔ I am ready to begin! · 💬 I wish to raise the stakes. · 💬 **I think you can do better.** ·
> 💬 I have some questions first. · ➜ I need some time to prepare.

**S2 — the wager** (`t = 573.8 – 682.05`):

> **Lokarr, Master of the Crucible**
> Oh, is that so? Very well. I wager that you will die, but…if you surprise me, I will raise your
> reward substantially. Do we have a deal?
>
> ✔ Forget the bet. Let's begin. (Standard Crucible) · ✔ Start on Wave 50 · ✔ Start on Wave 100 ·
> ✔ **Start on Wave 150** · ✔ Start on Wave 180 · 💬 **Sure, but I bet you can also do better.** ·
> ➜ I need some time to prepare.

### 2.2 The complete click record — TWO clicks, both frame-attested

| # | t (s) | highlighted option under the cursor | icon | effect | evidence |
|---|---|---|---|---|---|
| 1 | **573.70** | **"I wish to raise the stakes."** | 💬 blue speech bubble | S1 → S2 at 573.80 | `evidence/click1_t573.70_raise-the-stakes.png` |
| 2 | **682.00** | **"Start on Wave 150"** | ✔ green check | dialogue gone at 682.10; run starts | `evidence/click2_t682.00_start-on-wave-150.png`, `…_t682.10_dialog-closed.png` |

Both are direct reads of the highlight bar with the cursor on it, not inferences. The highlight was
traced continuously through the final approach — 679.6 "Forget the bet" → 679.7 "Start on Wave 50"
→ 679.9 "Start on Wave 100" → 680.1 "Start on Wave 150" → held → click at 682.00.

**Corroboration, independent of the read:** the fought band is waves **151–160 = tier 16**, exactly
what "Start on Wave 150" delivers. The dialogue read and the fought roster agree.

### 2.3 ⚑ THE OPTIONS THAT WERE NEVER TAKEN

**"I think you can do better."** (S1) and **"Sure, but I bet you can also do better."** (S2) were
**both never clicked**. The second is still present, un-taken, and carrying its 💬 continue-icon in
the **final frame of the dialogue at t = 682.05**, one tenth of a second before the run begins.

**S2 still offers the "…can do better" option.** That is itself structural evidence: S2 is reached
from S1, and a branch that had already consumed the "do better" election would have no reason to
re-offer it. So the S1 click was navigation, not election — which is exactly what the frame read
independently shows (💬 icon, and S2 appears rather than the dialogue closing).

### 2.4 What the records say about where the election lives

`game/questevents.lua`, `serverQuestTable` — verbatim structure:

```lua
startEvent       = gd.survival.eventControl.startSurvivalModeEvent,
startTier05Event = gd.survival.eventControl.startTier05Event,
startTier10Event = gd.survival.eventControl.startTier10Event,
startTier01..15  = gd.survival.tierNNWaves.startSurvivalModeEvent,
endEvent         = gd.survival.eventControl.eventFinishedCashOut,
upgradeReward    = gd.survival.rewards.upgradeRewards,
bonusChest       = gd.survival.rewards.bonusChest,      -- <= the election
```

**`bonusChest` is its own server quest event, disjoint from every `start*` event.** It is one-shot
and monotone (`if Server && not bonusChest then …`, `rewards.lua` L889-907), and the module-local is
reset at `resetLootVariables` (L946) — so it cannot have been carried in from an earlier session;
the map was loaded fresh at t ≈ 45 s.

Three further records-side supports that the wave-start choice does **not** imply the election:

1. **`achS003Desc`** = "Complete the Crucible through Wave 150 on Gladiator Difficulty." ·
   **`achS007Desc`** = "…on Gladiator Difficulty **with the 6th Spawn Point active**." Two distinct
   achievements. If the wave-150 start set the flag, achS007 would be co-extensive with achS003.
2. **`tagTutorialTip64TextB`** = "…any additional bonuses **you activated** at the start" — an
   opt-in, phrased as separate from starting.
3. The option's own wording — "Sure, but I bet you can **also** do better" — is an *addition* to the
   deal, and `bonusChest` is the only election-shaped server event in the entire survival table.

### 2.5 D-A's verdict under the pre-registered rule

The prereg's D-A rule asks for a start-of-run control **legible in an ACTIVE or INACTIVE state**. The
Lokarr conversation is that control; the election-bearing option is legible, present, and **un-taken
at the moment the run begins**. **D-A returns DIRECT-OFF.**

Graded **STRONG, not DECISIVE**, because one link in the chain is read from records *structure* and
*shipped text* rather than from the conversation binding itself, which is `D-W-1` below.

---

## § 3 — D-B: NOT-USABLE, AND NOW QUANTIFIED

### 3.1 The decode that made D-B worth registering — and the decode that closed it

Lap V captured the setter: activating the election creates
`records/fx/ambient/fx_eldritchrift_medium01.dbr` at the 6th spawn point's coordinates. Lap W then
decoded **where** that is, and **what else** carries the same FX.

**`records/scriptentities/spawnpoint06_fx.dbr` → `onAddToWorld = gd.survival.rewards.spawnPoint06FXOnAddToWorld`.**
It is map-placed in all ten arenas, 0.02 – 2.9 m from `records/scriptentities/spawnpoint06.dbr`.
**p06's world position is therefore decoded per arena** (`pm4w_geometry_p06.csv`).

**⚑ `W-1` — the static rift marks spawn points 1–4 and never 5 or 6, in every arena.** Census of
`fx_eldritchrift_medium01` map placements (80 rows → **4 unique per map** after the 2× archive
duplication): every one lands on `tier16spawnpoint01`, `spawnpoint02`, `spawnpoint03` or
`spawnpoint04` (0.09 – 1.6 m). Distance from the nearest static rift to **`spawnpoint05` is
25.6 – 40.3 m** and to **`spawnpoint06` is 15.2 – 43.3 m** — never adjacent, in any arena.

So the in-arena signature is exact and asymmetric: **a rift at p06 ⟺ election ON**, and it is the
only rift-bearing point that is election-gated. That is the correct instrument for any future
in-arena check, and it is now fully specified.

### 3.2 Why it could not be used here

| arena | Lokarr → p06 | player-spawn → p06 |
|---|---:|---:|
| survivalworld_a | **49.4 m** | 36.4 m |
| b | 59.0 | 48.3 |
| c | 53.9 | 45.6 |
| d | 65.1 | 55.3 |
| e | 54.9 | 44.6 |
| f | **79.3** | 64.3 |
| g | 53.6 | 43.4 |
| h | 65.9 | 51.9 |
| i | 54.0 | 41.8 |
| j | 75.7 | 64.6 |

The player stands at Lokarr for the whole election. At Lap R's indicative **119–125 ground px/m**
(`U-R-1`, itself NOT ruled) the camera's ground patch is ≈ 16 × 17 m; p06 is **49–79 m away in every
arena**. It was off camera by roughly a factor of six, whichever arena this is.

A frame-difference test was nonetheless run across click 1 (median of 19 frames at t = 568.0–572.5
vs median of 21 at t = 575.0–580.0, dialogue box masked): **no new world FX anywhere in frame**
(`evidence/diff-across-click1_no-new-world-fx.png`; residual is VFX flicker on pre-existing glows and
the HUD clock digits). Per the prereg this is recorded as **UNINFORMATIVE, not as evidence of OFF** —
the p06 anchor was not in the frustum, so the test had no power. **D-B = NOT-USABLE.**

---

## § 4 — D-C: POSITIVE CONTROL PASSES, ZERO HITS, STILL UNINFORMATIVE FOR OFF

### 4.1 The p06-distinct name sets, computed before any OCR (prereg step 2)

Census of every pool declared at **every** spawn point on each band wave, member records resolved to
display names through the shipped tag tables. `S_w` = names reachable **only** through that wave's
p06 pool. Full sets in `pm4w_p06_distinct_names.json`.

| wave | p06 names | other-point names | **\|S_w\|** | examples from `S_w` |
|---|---:|---:|---:|---|
| 152 | 36 | 38 | **36** | Athraz the Watcher · Balladra Stormscion · Carath'Lud |
| 153 | 10 | 54 | **10** | Innugaru Terror of the Void · Wen'Kazul the Hungering Blade |
| 155 | 30 | 9 | **30** | Bogloth the Marrowdrinker · Halvastra Wrathfire |
| 156 | 3 | 25 | **3** | Ugdenbog Cannibal ~ Bloodsinger / Fleshcrazed / Wraithspeaker |
| 157 | 5 | 85 | **5** | Archanis ~ Arcane · Embrallis ~ Burning · Neverus ~ Celestial |
| 158 | 9 | 63 | **9** | Omegus ~ Celestial · Oppressius ~ Unstoppable |
| **160** | 5 | 14 | **5** | Allcadius the Unburied · Haldra the Bloodlust · Ulda Emberclaw |

`S_w` is non-empty on **all seven** declaring waves, so no wave was dropped. Wave 156's p06 pool is
basic trash and was excluded from D-C by the prereg — but its three names are distinct anyway, so it
is reported and simply not relied on.

### 4.2 The census, and the positive control

Vision OCR over the top HUD band (`crop=1920:150:0:0`, 2× upscale), **1 frame / 1 s across the seven
declaring waves** at Lap H-2's `OBS-H2-6` boundaries — **127 frames, 1 011 OCR observations**.

**Positive control: PASSES.** Named heroes from *non-p06* pools were read on declaring waves —
`Allostria, the Mindthief` (w155/156), `Dralgar, the Keeper` (w155), `Janaxia` (w156),
`Blugrug the Living Plague` · `Arum'Zoth ~ Burning` · `Phigillius Stormbile` (w157),
`Sandclaw ~ Matriarch` · `Arcanom` · `Soulthief` (w158),
`Galakros` · `Archmage Aleksander` · `Zantarin` · `Kubacabra` (w160). The instrument can read hero
names on exactly the waves under test.

**Result: 0 hits against `S_w`, on every wave, including wave 160** — where an ON election would have
put three *Wendigo Cannibal* heroes into a roster whose non-p06 name pool is only 14 strings, and
where 18 distinct proper-noun reads were harvested across 27 sampled frames.

### 4.3 Why this is still not OFF

**GD renders a monster's name only for the single hovered / targeted monster.** The census therefore
samples ~1 body per frame out of a 19–36 crowd. The prereg's OFF rule requires **full coverage**, and
full coverage is unattainable with a one-body sampler. **D-C returns UNINFORMATIVE.** It did not
return ON, and it is a null pointing the same way as D-A — but per the prereg it contributes
**nothing to the verdict** and is reported as corroboration only. Saying so plainly is the point:
the convenient reading is available here and is refused.

---

## § 5 — THE VERDICT UNDER THE PRE-REGISTERED GLOBAL RULE

| discriminator | outcome | admissible for |
|---|---|---|
| **D-A** start-of-run UI | **DIRECT-OFF** | **the verdict** |
| **D-B** p06 rift marker | **NOT-USABLE** (p06 49–79 m off camera) | nothing |
| **D-C** p06-distinct name census | **UNINFORMATIVE** (positive control passes; 0/1 011; coverage insufficient) | corroboration only |
| **D-D** aggregate counts | **not consulted** | inadmissible by construction |

No discriminator returned ON. No two admissible discriminators disagree. Rule 2 fires.

> ## **VERDICT — p06 ELECTION: OFF. Confidence STRONG (not DECISIVE).**

**What would overturn it, stated as required by prereg rule 5:** a reading of
`conversations/npc_event_01.cnv` showing `gd.survival.rewards.bonusChest` bound to the
**"I wish to raise the stakes."** node (clicked at t = 573.70) or to the **"Start on Wave 150"** node
(clicked at t = 682.00) instead of to a **"…can do better"** node (never clicked). Nothing else in
this lap's evidence chain is soft.

**The referent's 19–36 crowd number was not consulted at any point in this lap.** The verdict lands
on the limb that *loses* 25.000 expected bodies and therefore grades **worse** — which is the
outcome Lap V refused to prejudge and Lap W had no licence to prefer.

---

## § 6 — DEFECTS, DEVIATIONS, AND FOURTH-MECHANISM FINDS

### 6.1 ⚑ Fourth-mechanism finds — NAMED, NOT DECODED (`R-PM4-58 part 4`)

* **`F-4M-1` — SPAWN POINT 1 IS TIER-SPECIFIC.** The arena maps place `spawnpoint02` … `spawnpoint06`
  once each, but spawn point 1 is a **per-tier entity**: `tier01spawnpoint01` … `tier20spawnpoint01`
  are all separately placed (20 rows each for tiers 01–17, 10 rows each for 18–20). Tier 16 uses
  `tier16spawnpoint01`. **Any geometry keyed to "spawn point 1" is tier-dependent.** Named only —
  whether Laps S/T/U's labelling already absorbs this is not established here and I did not check it,
  because checking it is a geometry re-decode and this lap is a fixture read.
* **`F-4M-2` — THE ELECTION IS SILENT.** `tags_survival.txt`'s notification block is exhaustive
  (`Start`, `Active`, `Continue`, `Failure`, `Reward`, `Reset`, `Checkpoint05`, `Checkpoint10`) and
  contains **no** string announcing the 6th spawn point. The game gives the player **no on-screen
  confirmation** of the election. That is *why* the rift is the marker, and it is why no HUD read can
  ever settle this question. Named as a property of the source, not decoded further.

Neither is folded. Neither is priced. Neither is Lap W's to resolve.

### 6.2 Defect table

| id | defect | disposition |
|---|---|---|
| **`D-W-1`** | **`conversations/npc_event_01.cnv` is DECODE-ABSENT from the edition-III intake.** The record `records/creatures/npcs/npc_event_01.dbr` carries `conversation = conversations/npc_event_01.cnv`, and that path appears in the `.arz` string table — but the file is in **no** `.arc` in the corpus (all 28 archives enumerated and byte-searched for the dialogue strings; zero hits). The conversation-node → quest-event binding therefore cannot be read. | **OPEN.** This is the single reason the verdict is STRONG rather than DECISIVE. Named as the falsifier in § 5. Acquisition is a Matt/host action, not an agent action. |
| **`D-W-2`** | **My own pre-registration's D-B framing was loose.** § 2's `W-R2` said "4 of the 6 spawn points carry a static rift" and inferred a 4-vs-5 count signature *without* having identified which points. The subsequent decode (§ 3.1) shows the rifts sit on points **1–4**, never 5 or 6 — so the count framing was right by accident and the *identity* framing (a rift at p06 specifically) is the correct one. Self-caught, before it was relied on. | **CORRECTED IN PLACE.** The prereg text stands as written; this row is the correction. |
| **`D-W-3`** | **Temporal-resolution deviation from the prereg.** D-A step 2 fixed 2 fps; the click-resolution passes ran at **10 fps** inside windows already covered at 2 fps (570–575 s, 676–685 s). The window was **not** widened and no new span was opened; only the sampling rate inside an already-committed window was raised, to place the click to ±0.1 s. | **DECLARED, per prereg rule 6.** Recorded rather than silently absorbed. |
| **`D-W-4`** | The `ffprobe` scan of the pre-band span was performed *before* the prereg was written (duration and frame count only — container metadata, no pixel decoded). The prereg says so explicitly in its own preamble. | **DECLARED, non-material.** |
| **`D-W-5`** | Arena identity (which of `survivalworld_a…j` was played) was **not** established. It is not needed: every quantity this lap relies on (Lokarr → p06 distance, static-rift adjacency, `S_w`) was computed for **all ten** arenas and the conclusion is invariant across them. | **CLOSED by invariance, not by identification.** |

---

## § 7 — HAND-OFF, WITH DO-NOTs

### 7.1 What `I-22` (gamora) folds

1. **`P06_BONUS_SPAWNS = False` is the referent-true limb.** Fold the OFF arm as the run-of-record
   limb. The two-limb bracket that `R-PM4-58 part 1` held in reserve **does not need to be carried**
   — but the STRONG-not-DECISIVE grade and the § 5 falsifier travel with the number.
2. **The +25.000 bodies do not enter.** Lap V's `C-12` price stands as *correct arithmetic for a limb
   that was not elected*. Decoded band total is therefore Lap V's **p06-OFF 172.083**, not 197.083.
3. **Nothing else in Lap V's recipe is touched by this lap.** `F-8`'s −11.500 limit cap, the count
   model, `NO_OP_ON_EMPTY`, `D-V-2`/`D-V-3` — all unchanged.
4. **The roster residual now points harder at `F-3M-1`** (Lap V-2's `ProxyAmbush`), exactly as
   `R-PM4-57 part 2` pre-stated for the OFF branch. That is a consequence to observe, **not** a
   licence to fold a 30-body term.

### 7.2 DO-NOT

* **DO NOT re-read D-C's zero as the verdict.** It is a one-body-per-frame sampler against a 19–36
  crowd. It agrees with D-A, and agreeing is not the same as proving. The verdict rests on D-A alone.
* **DO NOT treat the frame-difference null (§ 3.2) as evidence of OFF.** The p06 anchor was 49–79 m
  outside the frustum. A test with no power produces no evidence, in either direction.
* **DO NOT promote the verdict to DECISIVE without `npc_event_01.cnv`.** The chain is: two clicks
  (frame-attested) → the "…can do better" options never taken (frame-attested) → `bonusChest` is a
  disjoint quest event (decoded) → therefore not elected (**inferred**). The last arrow is an
  inference from records structure and shipped text. It is a good one. It is still an inference.
* **DO NOT use Lap R's 119–125 ground px/m as a ruled scale.** `U-R-1` is INDICATIVE and `OBS-H2-9`
  is an open gap. § 3.2 uses it only to establish that 49 m ≫ one screen, a conclusion that survives
  any scale within a factor of three.
* **DO NOT fold `F-4M-1` or `F-4M-2`.** Named, not decoded (§ 6.1).
* **Lap V's entire § 7.2 DO-NOT block remains binding** and is carried forward unchanged.

### 7.3 If the conductor wants DECISIVE

Two routes, in cost order:

1. **Obtain `conversations/npc_event_01.cnv`** (a fuller depot pull, or the Asset Manager's
   conversation export). One artefact; closes `D-W-1`; converts STRONG → DECISIVE or overturns it.
   **This is the cheap route and it is a host action, not an agent action.**
2. **The in-arena rift census** — now fully specified by § 3.1: p06's world coordinate is decoded per
   arena, the static rifts are known to sit only on points 1–4, and the signature is
   *rift-at-p06 ⟺ ON*. It needs a world→screen registration that does not currently exist
   (`OBS-H2-9` open, camera player-locked only). **Expensive; do not commission it before route 1.**

A third route was considered and is **not** recommended: silhouette identification of the p06 hero
types (e.g. wave 157's *Aetherial Colossus*, wave 160's *Wendigo Cannibal*). It is plausible, but it
is a **different instrument from the one this lap pre-registered**, and swapping instruments after
grading has begun is the exact move the prereg discipline exists to forbid. If the conductor wants
it, it should be pre-registered in its own lap.

---

## § 8 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 8.1 Inputs, pinned at preregistration and re-verified at instrument start (no mismatch fired)

| input | sha256 |
|---|---|
| referent `eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` |
| `…/lap-u-ramp-decode/pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| `…/lap-u-ramp-decode/pm4u_map_placements_v3.csv` | `08308eb408f7f630c9bd310c4b5ba36ce1869bb4338caaa4028fd4c609f08a57` |
| `…/lap-v-roster-decode/pm4v_findings.md` | `5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895` |
| `…/lap-v-roster-decode/pm4v_bonusspawn.json` | `7c8d0b732d947c60c1a9344f3130482513195486f20ff49f6173ecd33fb84aa4` |
| `…/lap-v-roster-decode/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |

The three `pm4v_*` digests are byte-identical to the values Lap V published in its own § 8.1 and to
the conductor's recomputation at `L-48`. Game-data inputs (`edition-III` `.arz`/`.arc` set) are the
same bytes Lap V pinned in its § 8.2; `Game.dll` / `Engine.dll` were not needed by this lap and were
not read.

### 8.2 Outputs of this lap

Recorded in `pm4w_digests.json`, recomputed at commit.

### 8.3 Instruments (recipe, so the 1.4 GB of frame dumps need not be committed)

| step | recipe |
|---|---|
| container probe | `ffprobe -show_entries format=duration -show_entries stream=…` |
| D-A step 1 | `ffmpeg -ss 0 -to 690 -vf "fps=1/5,scale=640:-1"` → 138 frames → 6 contact sheets |
| D-A step 2 | `ffmpeg -ss 425 -to 695 -vf "fps=2"` → 540 frames; dialogue-region perceptual-hash segmentation (48×26 bit-string, Hamming > 60) → 174 state representatives → crop (640,470)-(1600,1010), 2× upscale → Vision OCR |
| click resolution (`D-W-3`) | `ffmpeg -ss 570 -to 575` and `-ss 676 -to 685`, `fps=10`; highlight-bar read |
| D-B frame difference | per-pixel median of t ∈ [568.0, 572.5] vs t ∈ [575.0, 580.0], dialogue box masked |
| D-B geometry | `pm4w_geometry_p06.csv` from the pinned `pm4u_map_placements_v3.csv` |
| D-C census | `agentic_orchestration/research/scripts/pm4w_census_2026_08_15.py` |
| D-C OCR | `ffmpeg -ss <t> -frames:v 1 -vf "crop=1920:150:0:0,scale=3840:300"`, 1 fps over the seven declaring waves at Lap H-2 `OBS-H2-6` boundaries → Vision OCR |
| OCR binary | `ocr.swift` copied verbatim from Lap N `method/`, sha256 `1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1`, compiled `swiftc -O` |

`work/` (frame dumps, 1.4 GB) is `.gitignore`d and regenerable from this recipe against the pinned
referent.
