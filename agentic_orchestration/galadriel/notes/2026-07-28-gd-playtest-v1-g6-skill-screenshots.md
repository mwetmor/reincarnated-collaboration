# G-6 — the skill window, read: five allocated nodes, a dated A-step, and a gear step itemised

**Run:** `KC1-2026-07-27` (KIT-CAL-1) · **Pass:** G-6 · **Seam:** galadriel
**Commissioned by:** gandalf (`RUN-CONDUCTOR`), charter §12a
**Date:** 2026-07-28
**Status:** executed **blind to T11/G-7**, which landed mid-pass — see §0.1 for the
instrument-agreement table before reading anything else
**Substrate:** the 313 stills at `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/`
(`Screenshot (40).png` … `Screenshot (352).png`, contiguous, all 1920×1080)
**Captures:** `agentic_orchestration/galadriel/captures/2026-07-28-gd-playtest-v1-g6/`
(curated evidence + index at `…/evidence/`)
**Pipeline:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/g6_*.py`

---

## §0 — The one-line answer

**Onslaught ends at 13/16. The werewolf transform ends at 16/16, and reached 16 at
`play_time` 3619 — mid-R2. `werewolf2` and `werewolf3` are absent. `werewolf1b` — *Blight of
Ch'thon* — is ALLOCATED at 1/1, and has been since somewhere in `play_time` (2918, 3619].**

Two further things the stills gave up that nobody asked for and that matter more than the
Onslaught rank: **the claws A-step is now dated against `play_time`**, and **the build carries a
crit-triggered self-heal (Battle Surge, 8% max-HP per second for 3 s on a 6 s recharge) that the
G-4 kit spec does not model at all.**

### 0.1 — Read this first: G-6 ran in parallel with T11/G-7 and did not see it

**This pass was executed blind to G-7.** The charter §12a commission fired G-6 while T11 was still
outstanding; by the time I filed, the run had moved — T11 executed by SSH (§14.2), G-7 parsed the
`.gdc` (§14.5), and Matt reconciled his testimony (§14.5, verbatim: *"I did level to 13… I did
level the two werewolf nodes"*). **Nothing below was informed by any of that.** Every read here
comes from pixels alone.

That makes this pass worth more, not less: **two instruments with no shared failure mode landed on
the same numbers.**

| Claim | G-7 (`.gdc` save) | **G-6 (screenshots)** | Agree? |
|---|---|---|---|
| Onslaught rank | 13 | **13 / 16** | ✓ |
| `werewolf1` rank | 16 | **16 / 16** | ✓ |
| `werewolf1b` | rank 1 | **1 / 1, named "Blight of Ch'thon"** | ✓ |
| `werewolf1b` effect | 100% Pierce→Chaos | **"100% Piercing Damage converted to Chaos Damage"** | ✓ |
| `werewolf2` | absent | **absent** (by effect-absence in the transform tooltip) | ✓ |
| potions | 0 / 0 | **0 / 0** (36 stills) | ✓ |
| deaths | 2 | **2** | ✓ |
| kills | 882 | **882** | ✓ |
| `playTime` | 7096 | **7088** (last still) | ✓ |
| character level | **13** (bio); `play_stats.maxLevel` **lags at 12** | **12** — every still, to the end | ✓ *(independently confirms the lag)* |
| gear names | 4/4 exact vs testimony | **4/4 exact vs testimony, read off the tooltips** | ✓ |

**Three things G-6 has that the save cannot give**, because a save is one snapshot and this is a
time series:

1. **WHEN each rank was allocated**, on the run clock (§3.1) — the save says the build ended at
   16/13/1; only the stills say the transform maxed at `play_time` 3619 and Onslaught sat at rank 1
   until level 9.
2. **The A-step dated** (§6 F-G6-5) — target cap 2→3→4→5 and arc 90°→150°, with timestamps. R2 is
   **not** A-stationary.
3. **Two skills the save's rank list would show as bare records** but which the stills read out in
   full, with live values: **Battle Surge** (a crit-gated self-heal, §6 F-G6-6) and a **reserved
   cold aura** (+16 Armor / +20 DA) — neither in the G-4 kit spec.

Plus, in §7.1, the **rolled affix values on all four gear items read straight off the tooltips** —
which is G-7's follow-on **U-1** ("extract … the four items' rolled stats"), delivered here from
pixels, including an **87.6% itemised decomposition of the 759→1600 gear step**.

---

## §1 — Triage of the 313 stills

Cheap-first, per methodology. Pass 1 (`g6_triage.py`) decoded each still once, cached a 320×180
thumbnail, computed brightness / saturation / dark-desaturated-fraction / column-flatness /
temporal-delta features, and emitted eight ID-labelled contact sheets for visual scan. Pass 2
(`g6_detect.py`) then separated the classes by fixed-region normalised cross-correlation against
reference strips harvested from two frames — the GD windows render at fixed screen positions, so
one strip per window type separates the classes with no OCR at all.

| Class | Detector | Count | Frame IDs |
|---|---|---|---|
| **Skill window** (Berserker mastery tab) | mastery-level track at panel foot ∪ tab bar, NCC > 0.80 | **37** | 68, 84, 107, 151–153, 170–172, 209–214, 240–245, 273–277, 314–319, 348–352 |
| **Character window** (paperdoll + stat pages) | paperdoll equip-slot strip, NCC > 0.80 | **216** | 41–67, 69–83, 88–91, 94–106, 108–122, 126–129, 133–150, 157–169, 183–186, 190–208, 216–219, 223–239, 250–253, 257–272, 288–291, 296–313, 323–326, 331–347 |
| **Devotion window** | — | **0** | *(see §7)* |
| Gameplay / other | remainder | ~60 | — |

Artifacts: `triage-features.csv`, `g6-window-detect.csv`, `sheets/sheet-00..07_*.png`.

**A correction worth stating, because I made it and it would have cost the pass.** On first scan
of the contact sheets I read the dark, star-field-looking frames as the *devotion constellation
map*. They are not. They are the **Berserker mastery tree** — a dark panel of ringed skill icons
on connectors, which at thumbnail scale is visually indistinguishable from a constellation map.
The full-resolution read (f316) settled it. Had I filed the triage off the thumbnails, this pass
would have reported "devotion frames found, skill frames absent" — the exact inversion of the
truth. Thumbnail-scale classification of two dark node-graph UIs is not a safe instrument, and I
am recording that so the next capture pass does not repeat it.

### 1.1 Every still is self-dating — the pass's most useful accident

The stills carry the in-game **PlayStats panel** in the top right. The panel reader built for the
T-A video ledger (`panel_ocr.py`) applies to them **unchanged** — same 1920×1080 UI, same
right-anchored panel, same glyph model. `g6_panel_stills.py` ran it over the 37 skill-window
frames and got a clean read on **36 of 37** (one skill-row occlusion on f212, of a field this pass
does not use).

That means **every rank read below carries a `play_time`, a character level, a kill count and a
death count from the same frame**. Frame-ID order is monotone in `play_time` across the whole set
(f68 → 960 s, f352 → 7088 s), so ID order *is* run order, verified rather than assumed.

**Cross-validation, and it is exact.** f352 (`play_time` 7088) reads
`kills=882 · defaultweaponattack=74 · onslaught=54 · claws=358 · charge=175` —
**identical to the T-A ledger's endpoints** (charter §1, S-1). The stills are an independent
second instrument landing on the same terminal state. The panel reader transfers, and the
screenshot set spans `play_time` 960 → 7088, i.e. essentially the whole run.

Artifact: `g6-panel-all-skillframes.json`.

---

## §2 — Method: how the tree was read at all

Three obstacles, each of which defeated a naive approach, each recorded because the next pass over
this UI will meet them again.

1. **Rank counters render only on *reachable* nodes.** Locked nodes show an icon and no `N / M`.
   So the allocation is a small table, not a thirty-row one — but you cannot tell "locked" from
   "zero" without knowing this.
2. **The tooltip moves with the cursor and covers part of the tree in every single frame.** No one
   still shows the whole tree. Three locator attempts failed before one worked: the gold-border
   mask returns the panel's own frame (same gold); the white-text-block mask misses (tooltip body
   text is warm grey, not white); the FFT template-match on the "Current Level" heading works only
   where the heading renders identically. Recorded in `g6_tiplocate{,2,3}.py` rather than deleted.
3. **What finally worked: a two-pass robust composite per burst** (`g6_composite2.py`). Within a
   burst Matt hovered a different node in each frame, so the tooltip sits somewhere different in
   each. Pass 1 takes the per-pixel median; pass 2 marks pixels far from that median as OUTLIER
   (which is what a tooltip *is* — a big opaque frame-specific deviation) and averages only the
   inliers. Where every frame is occluded the pixel is stamped **magenta**, so occlusion stays
   visible instead of becoming plausible. No inpainting, ever. End-run composite: **0.01%
   no-data**.

**Composites are finding aids, not evidence of record.** Every counter reported below was
re-verified on at least one raw single frame at ≥1× native delivered resolution, and the raw crop
is preserved. The delivered-pixel floor for reading this panel's counters is ~0.75× native; crops
were sized to clear it.

---

## §3 — THE RANK TABLE (end of run: f348–f352, `play_time` 7079–7088, character level 12)

Character identity, read from the character-sheet header (f327 / f331 / f333):
**"Fresh Character 01" · Level 12 · Berserker.** *(A `save_identity` fragment for the T11 join.)*

Every counter-bearing node in the panel. Everything not listed is **locked** (no counter rendered)
— verified by a nine-tile sweep of the whole panel at ≥1× native (`grid/end_*`).

| Node position (native px) | Shape | Counter | Identity | Grade |
|---|---|---|---|---|
| (722, 322) | circle | **0 / 12** | unallocated | CLEAN |
| (812, 322) | circle | **0 / 10** | unallocated | CLEAN |
| (880, 440) | circle | **0 / 1** | unallocated | CLEAN |
| (730, 462) | circle | **13 / 16** | **Onslaught** (`onslaught1.dbr`) | CLEAN |
| (815, 536) | **square** | **1 / 12** | *Battle Surge* **or** the reserved cold aura | rank CLEAN · name **UNCERTAIN** |
| (732, 607) | circle | **16 / 16** | **Werewolf transform** (`werewolf1.dbr`) | CLEAN |
| (817, 630) | circle | **1 / 1** | **Blight of Ch'thon** (`werewolf1b.dbr`) | CLEAN |
| (792, 710) | circle | **1 / 12** | *Battle Surge* **or** the reserved cold aura | rank CLEAN · name **UNCERTAIN** |

**Total allocated: 32 ranks** (13 + 1 + 16 + 1 + 1).

**On the one UNCERTAIN row.** Five nodes carry rank; five distinct tooltips carry a
`Current Level` line. Three pair unambiguously (Onslaught, the transform, Blight of Ch'thon). The
remaining two tooltips — **Battle Surge** and an unnamed **reserved cold aura** — both belong to
the two 1/12 nodes, but the pairing between them does not close: the hover cue (GD renders the
hovered node's counter bright-bold, the rest dim grey) resolves f352 → the *circle* is Battle
Surge, yet no frame in which the aura tooltip is open exposes a matching bold counter on the
square. **The rank table is unaffected — both are rank 1 either way** — so this is graded
UNCERTAIN and the crops are preserved for human eyes rather than guessed:
`node-series/SERIES_sq12hover.png`, `node-series/SERIES_circ12hover.png`,
`crops/f349_665-420-945-800_cluster_x3.png`.

There is a second, structural oddity in that row worth a source lookup: **one of the two is drawn
as a SQUARE**, and in GD's mastery UI squares are modifier/transmuter nodes attached to a parent,
while both named skills read as standalone. → **REQUEST to gandalf/legolas** (`.arz` is not my
seam): which `playerclass10` records carry 12 base ranks, and which of them is a `Skill_Modifier`?
That one lookup closes the row.

### 3.1 The rank TIME SERIES — every value dated on the run clock

Read from the same fixed pixel boxes across bursts (`g6_nodeseries.py`); `play_time` and level
from the PlayStats panel of the same frame.

| frame | `play_time` | lvl | kills | Werewolf | Onslaught | Blight of Ch'thon | sq 1/12 | circ 1/12 |
|---|---|---|---|---|---|---|---|---|
| f68 | 960 | 2 | 16 | **1 / 16** | 1 / 16 | locked | locked | locked |
| f84 | 1457 | 3 | 45 | **3 / 16** | 1 / 16 | locked | locked | locked |
| f107 | 1789 | 4 | 81 | **5 / 16** | 1 / 16 | locked | locked | locked |
| f151 | 2597 | 6 | 194 | **12 / 16** | 1 / 16 | locked | locked | locked |
| f170 | 2918 | 7 | 213 | **15 / 16** | 1 / 16 | locked | locked | locked |
| f209 | 3619 | 8 | 271 | **16 / 16** | 1 / 16 | **1 / 1** | **1 / 12** | **1 / 12** |
| f240 | 4174 | 9 | 434 | 16 / 16 | **4 / 16** | 1 / 1 | 1 / 12 | 1 / 12 |
| f273 | 4955 | 10 | 568 | 16 / 16 | **7 / 16** | 1 / 1 | 1 / 12 | 1 / 12 |
| f314 | 6445 | 11 | 692 | 16 / 16 | **10 / 16** | 1 / 1 | 1 / 12 | 1 / 12 |
| f348 | 7079 | 12 | 882 | 16 / 16 | **13 / 16** | 1 / 1 | 1 / 12 | 1 / 12 |

Series images: `node-series/SERIES_rednode.png` (transform), `SERIES_bluenode.png` (Onslaught),
`SERIES_blight.png`, `SERIES_sq12.png`, `SERIES_battlesurge.png`.

Two shapes fall straight out:

- **The transform is maxed by `play_time` 3619 and never moves again** — the whole of the
  transform's rank climb happens inside R2's first half.
- **Onslaught sits at rank 1 for the entire run up to level 9**, then takes *every* point from
  level 9 to 12 (+3 per level, exactly). Matt poured his whole late-run investment into the one
  skill the transform excludes. See §5.
- **Three nodes light up in one window** — Blight of Ch'thon, and both 1/12 nodes — all inside
  `play_time` ∈ (2918, 3619]. **R2 is not homogeneous**: it contains a build-composition event
  that no existing instrument in this run has represented.

---

## §4 — FINDING F-G6-1: `werewolf1b` IS ALLOCATED

**Charter §12a recorded Matt's attestation — "no points in `werewolf2`/`werewolf3`/`werewolf1b`
('no I didn't')" — and G-4 §7.1 item 4 upgraded the spec's inference to ATTESTED on it. The
screenshots say otherwise for `werewolf1b`. I filed this as a loud contradiction, per the
commission's grading discipline and charter §14.1's standing instruction that any G-6/G-7 conflict
with the attested set is "a loud finding, not a silent overwrite."**

**It has since been reconciled, from both ends, without my involvement** — G-7's save parse read
`werewolf1b` rank 1 independently, and Matt corrected himself in §14.5 (*"I did level the two
werewolf nodes, and if I indicated otherwise, I must not have understood your question in
context"*). So this is no longer a live dispute. I am leaving the finding stated at full strength
rather than softening it retroactively, because the shape of what happened is the point: **three
instruments — pixels, save bytes, and the owner's memory on re-ask — converged, and the two that
were mechanical got there first.** The section below is what the pixels said, written before any
of that was known.

The node at (817, 630) — a teal-ringed circle hanging directly off the werewolf transform node by
a connector — reads **1 / 1** in every skill-window frame from f209 (`play_time` 3619) to the end
of the run. Its tooltip, read at 6× from f351 (`crops/f351_580-520-900-600_blightpct_x6.png`):

> **Blight of Ch'thon**
> *The corrupted blood of Ch'thon has taken hold within you, twisting your transformation into a
> ravenous abomination bent on destruction.*
> **Current Level : 1**
> **100% Piercing Damage converted to Chaos Damage**

That is `records/skills/playerclass10/werewolf1b.dbr` verbatim as the G-4 spec §1.6 describes it:
`Skill_Transmuter`, 1/1 ranks, `conversionInType=Pierce → conversionOutType=Chaos`, 100%,
`skillTier=2`. The spec's own row predicted the effect exactly; only the *state* was wrong.

**Grade: MEASURED-by-screenshot.** Clean read: the node counter is unambiguous at 6× in three
independent frames, and the tooltip names the record's exact mechanic.

**Allocation window: `play_time` ∈ (2918, 3619]** — locked at f170, allocated at f209. That is
**inside R2** (1134–6052), at character level 7→8, roughly 30% of the way through the fixture
regime. It is not a late-run detail; it covers the majority of R2's combat and the whole of R3.

### 4.1 What it does to the kit spec — and the one caveat that keeps me from over-claiming

The G-4 kit spec carries the kit's damage as physical + pierce. Claws at rank 16 carries **237
flat pierce**; charge carries **375 flat pierce** plus its bleed. Under a 100% Pierce→Chaos
transmuter, **the entire flat-pierce channel of both actives is Chaos damage for ~57% of R2's
duration and all of R3** — a different resistance interaction against every enemy in the fixture.

**The caveat, stated because it cuts against the clean story.** The transform's own tooltip read
at f210 (`play_time` **3621** — *after* Blight was allocated) still labels those lines
"**237 Piercing Damage**" and "**375 Piercing Damage**", not chaos. Two readings are available:
GD's granted-skill tooltip renders pre-conversion values, or the conversion applies at a layer the
transform tooltip does not reflect. I cannot separate them from pixels.

So I split the grade:

- **the allocation** — `werewolf1b` at 1/1 from `play_time` ≤3619 — **MEASURED**, no caveat;
- **the damage-type consequence** — the pierce channel becoming chaos in play — **REQUIRES SOURCE
  CONFIRMATION** (`.arz` conversion semantics + whether GD tooltips display pre- or post-conversion).
  That is elrond/legolas/gandalf's lane, not mine. → **REQUEST.**

---

## §5 — FINDING F-G6-2/3: `werewolf2` and `werewolf3` ARE absent — the attestation holds there

The spec's §7.3 named `werewolf2` as *"the one thing I would most like you to check … the
assumption with the largest blast radius."* The stills close it.

**`werewolf2` — ABSENT, MEASURED by effect-absence.** The transform's tooltip enumerates its
granted abilities with their live, ranked values. At f210 (`play_time` 3621 — after every
allocation in the run had been made; the tree is static from f209 on except Onslaught), the
**Feral Claws** block reads, in full and with nothing omitted
(`crops/f210_320-310-660-450_wt_x5.png`):

> **Feral Claws** — 5 Energy Cost · **150 Degree Attack Arc** · **5 Target Maximum** ·
> **150% Main Hand Damage (69 – 85)** · **237 Piercing Damage**

Five lines. `werewolf2`'s entire content is a **bleed DoT, a life-leech and a crit-damage bonus on
claws**. None appears. The spec's largest sensitivity resolves **in the spec's favour**.

**`werewolf3` — ABSENT, high confidence, one inference step.** The **Rip and Tear** (charge) block
at the same frame reads (`crops/f210_320-440-660-575_wt_x5.png`, `…-570-660-705_wt_x5.png`):

> **Rip and Tear** — 42 Energy Cost · **4 Second Skill Recharge** · **2.5 Meter Target Area** ·
> **14 Meter Range** · 295% Main Hand Damage (135 – 166) · 295% Off-Hand Damage (177 – 181) ·
> **375 Piercing Damage** · **810 Bleeding Damage over 3 Seconds** ·
> **Knockdown target for 0.5 Seconds** · **+200% Movement Speed**

No cooldown-refresh line. GD may not surface a modifier's proc in its parent's block, so that
alone is not decisive — but both 12-max-rank allocated nodes are already accounted for by the
Battle Surge and cold-aura tooltips, which closes it. Graded **ABSENT** with the inference step
named.

### 5.1 The `.arz` reads are corroborated at the pixel level — five for five, twice

The G-4 spec's numbers were read from source. The game's own UI, at the fixture's actual in-play
rank, agrees on every field it displays:

| Spec §1.3 / §1.4 field | Source (`.arz`) | Screenshot (f210, transform rank 16) |
|---|---|---|
| claws `skillTargetNumber` @16 | 5 | **5 Target Maximum** ✓ |
| claws `skillTargetAngle` @16 | 150° | **150 Degree Attack Arc** ✓ |
| claws `weaponDamagePct` @16 | 150 | **150% Main Hand Damage** ✓ |
| claws `offensivePierceMin` @16 | 237 | **237 Piercing Damage** ✓ |
| charge `skillCooldownTime` | 4.0 s | **4 Second Skill Recharge** ✓ |
| charge `skillTargetRadius` | 2.5 | **2.5 Meter Target Area** ✓ |
| charge `waveDistance` | 14.0 | **14 Meter Range** ✓ |
| charge `characterRunSpeedModifier` | +200% | **+200% Movement Speed** ✓ |
| charge `offensiveSlowBleedingDurationMin` | 3.0 s | **810 Bleeding Damage over 3 Seconds** ✓ |
| charge `offensiveKnockdownMin` | 0.5 s | **Knockdown target for 0.5 Seconds** ✓ |

And again at rank 12 from f153 (`play_time` 2605): *"Current Level : 12 … Feral Claws · 130 Degree
Attack Arc · 4 Target Maximum · 130% Main Hand Damage"* — spec rank 12 is `targetNumber=4`,
`angle=130`, `weaponDamagePct=130`. Its **"Next Level : 13"** block reads *150 Degree / 5 Target*,
which is the spec's rank-13 row. **The `.arz` extraction is confirmed against the running game.**

*(One field does not reconcile and is graded UNCERTAIN: f153's rank-12 claws shows "103 Piercing
Damage" where the spec's array interpolates to ~177. Rank 16 matches exactly at 237. Crop saved:
`Screenshot (153)` region. Low consequence; named rather than smoothed.)*

*(One unmodelled mechanic, surfaced: the charge block carries a separate **"295% Off-Hand Damage
(177 – 181)"** line alongside main-hand. The form's attacks strike with both hands. The kit spec
carries a single weapon-damage term.)*

---

## §6 — FINDINGS the commission did not ask for, and which outrank the ones it did

### F-G6-4 — the §2 replacement ruling is now stated by the game, in words, to the player

The werewolf transform's tooltip, immediately above its `Current Level` line, ends with:

> **"…cannot trigger weapon pool skills."**

Onslaught is `Skill_WeaponPool_BasicAttack`. `defaultweaponattack` is `Skill_WeaponPool_Default`.
The G-4 §2 ruling — set-partition exclusion, corroborated by four independent lines — has a
**fifth line, and it is the game's own UI text**. Nothing was hidden from the player; it was in
the tooltip the whole time.

Read alongside §3.1's Onslaught series this becomes something sharper than a mechanism note.
**Onslaught sat at rank 1 for 6,100 seconds of play, then absorbed every skill point from level 9
to level 12 — 12 ranks — while its use counter stayed frozen at 54 from `play_time` ~1457
onward.** Matt spent his entire late-run progression on a skill that could not fire. The testimony
("I was pressing Onslaught"), the frozen counter, the source partition, and now the allocation
curve all describe the same thing from four directions.

### F-G6-5 — the claws A-step is DATED

The transform's rank governs the claws rank, and the claws rank governs target count and arc. With
§3.1's dated transform series and the spec's §1.3 arrays, the A-step now has timestamps:

| `play_time` | lvl | transform rank | **targets** | **arc** | wpn dmg % | tooltip-confirmed |
|---|---|---|---|---|---|---|
| 960 | 2 | 1 | **2** | 90° | 70% | — |
| 1457 | 3 | 3 | **3** | 110° | 84% | — |
| 1789 | 4 | 5 | **3** | 110° | 95% | — |
| 2605 | 6 | 12 | **4** | 130° | 130% | **YES (f153)** |
| 2918 | 7 | 15 | **5** | 150° | 145% | — |
| 3621 → end | 8–12 | 16 | **5** | 150° | 150% | **YES (f210)** |

R2 spans `play_time` 1134–6052. **Within R2 the kit's target cap goes 2 → 3 → 4 → 5 and its arc 90°
→ 150°, and it reaches the cap at `play_time` ~2918 — less than 40% of the way through the
regime.** G-2b measured the A-step as an emergent multi-kill signature; this is its *mechanical
cause*, dated. G-5 should not model R2's A-factor as stationary, and the intra-R2 partition is now
available: pre-2918 (climbing) vs post-2918 (capped at 5 targets / 150°).

Grade: transform ranks MEASURED; the per-rank claws parameters DERIVED from the spec's `.arz`
arrays, with **two of the six rows independently tooltip-confirmed**.

### F-G6-6 — the build carries a SUSTAIN CHANNEL the kit spec does not model

The 1/12 node named **Battle Surge** (`tooltips/REP_f213_x3.png`, `crops/f352_640-340-1000-740_tooltip_x3.png`):

> **Battle Surge** — *"To a trained berserker, there is no greater thrill than the glory of combat.
> As you land **critical blows**, you feel invigorated."*
> **Current Level : 1** — **100% Chance of Activating** · **6 Second Skill Recharge** ·
> **3 Second Duration** · **Restores 8% Health Per Second** · +4 Energy Regenerated per second

A **crit-triggered, 100%-chance, auto-firing self-heal: up to 24% of maximum health per 6-second
window.** It needs no keypress, which is exactly why it never appears in the PlayStats
`Skills Used` list and why no instrument in this run has seen it.

The second 1/12 node is a **reserved aura**: *50 Energy Reserved · 12 Meter Radius · 8–10 Cold
Damage · +20 Defensive Ability · +16 Armor* (Current Level 1; cold damage reads 6–8 at f211,
8–10 at f316, 9–10 at f350 — it scales with something the tooltip does not name).

**Both were allocated in the same window, `play_time` ∈ (2918, 3619] — inside R2.**

Consequences I can see from here, for gandalf and gamora to rule on:

1. `life_healed` **12468.06** is a charter endpoint and a live column in elrond's fixture ingestion
   (T-3, the 3.1% rejection rate). Battle Surge is a plausible large contributor: at R2's max HP
   ~759, one proc is ~182 HP. It is not the only channel, but it is an unmodelled one.
2. **G-2c ruled the survivability channel CLOSED (null)** on the finding that within-R2 EHP is a
   monotone function of the clock with zero residual variance. That ruling is not overturned — but
   its premise was that the only survivability lever was the HP pool. A crit-gated regeneration
   proc switching on mid-R2 is a *second* lever, and it switches on inside the regime, not at its
   boundary. G-2c's Q1 null should be re-read with that named.
3. **The +16 Armor / +20 DA aura** lands in exactly the gap G-4 §1.8 left open — *"armour remains
   an uninstrumented candidate for the residual magnitude collapse; the sim spec must treat
   `mitigation_delta` as a free parameter fitted to the intake tail."* Part of the armour is now
   identified, and it is **not** gear and **not** at the R2/R3 boundary.

Taken together: **R2 contains a build-composition event at `play_time` ≈ 2918–3619** that adds a
damage-type conversion, a sustain proc and an armour/DA aura, on top of the transform hitting its
target cap at 2918. R2's status as "the fixture on sample size" (G-4 §13.3 C-2, amended once
already) takes another qualifier.

### F-G6-7 — a seventh skill record, small

`defaultkickattack` appears in the PlayStats `Skills Used` list, climbing **4 → 19** over the run.
It is not in the G-4 spec's §1.1 record table and not among the T-A ledger's tracked counters.
Trivial in magnitude; recorded so it is not re-discovered as a surprise.

---

## §7 — The bonus items: gear FULLY READ, devotion NULL

### 7.1 Gear: names AND rolled affixes, from the tooltips

*(First-pass conclusion here was "the three that matter were never hovered." That was wrong. It
came from sampling the frames a green-pixel heuristic ranked highest — and that heuristic ranks the
character window's own green slot-borders, not tooltips. Charter §14.1 names **Screenshot (323)**
and **Screenshot (328)** outright; reading those and walking their neighbours opened the whole set.
The heuristic was the error, recorded rather than quietly replaced.)*

**All four of Matt's §14.1 attested items are on the pixels, character-for-character**, plus five
slots he did not name. This is a **third independent instrument** on the gear names — testimony,
`.gdc`→`.arz`→`.arc` (G-7), and the running game's own tooltips — and it delivers G-7's follow-on
**U-1** (the items' rolled stats) for all four attested items.

| Slot | Name (read at 4–5×) | Rolled values read | Frame |
|---|---|---|---|
| **Weapon** *(major)* | **Poisoned Pusquill's Tail of Corrosion** — Rare One-Handed Mace | 14–40 Physical · 6–12 Acid · **1.78 Attacks/sec** · **50 Poison Damage over 5 Seconds** · +18% Acid Damage · **+38% Poison Damage with +64% Increased Duration** · **18% Physical Damage converted to Acid Damage** · **+242 Health** · +3 Nidalla's Hidden Hand · +3 Vulnerability | **f323** |
| **Amulet** *(major)* | **Menacing Putrid Necklace of Protection** — Rare Amulet | **+21% Poison Damage** · +14 Cunning · **+321 Health** | **f328** |
| **Chest** *(minor)* | **Mystic Salvaged Armor of Menhir's Wall** — Rare Heavy Chest Armor | **58 Armor** · **+76 Health** · +5% Spirit · **+13 Defensive Ability** · (+Physical Res, +Bleeding Res) · req. lvl 4 | **f324** |
| **Belt** *(minor)* | **Mystic Woven Cord of Soulwarding** — Rare Belt | **7 Armor** · +11% Physical Damage · +17% Vitality Damage · **+98 Health** · +6% Spirit | **f299** |
| Head | Sheltering Salvaged Helmet of the Draughul — Rare Heavy Helm | +Offensive Ability · +Defensive Ability · +% Health Regen · +% Cold Resistance | f327 |
| Shoulders | Magestorm Fur-lined Mantle of Frostbite — Rare | 16 Armor · +8% Cold · +8% Lightning · +9% Pierce · +8 OA · +8% Vitality Res · req. lvl 5 | f296, f331 |
| Legs | Glacial Patchwork Leggings of the Fox — Rare Pants | 16 Armor · +Cold / +Frostburn · +8 Cunning · +38 Spirit · req. lvl 3 | f325 |
| Boots | Vigorous Reinforced Greaves — Magic Heavy Boots | 12 Armor · **+75 Health** | f333 |
| Ring | Vampiric Silver Band — Magic Ring | +% Attack Damage converted to Health · +Energy Regenerated | f326 |

**Matt's major/minor split is visible in the numbers**: weapon and amulet carry +242 and +321
Health; chest and belt carry +76 and +98. §14.6's refinement — weapon+amulet are Rare *bases*,
chest+belt are Common bases with Rare-class *suffixes* — matches the tooltip type lines exactly
("Rare One-Handed Mace" / "Rare Amulet" against "…of Menhir's Wall" / "…of Soulwarding").

#### F-G6-9 — the 759→1600 gear step, ITEMISED (87.6% closed)

G-4 §1.8 carried the gear step as `ehp_multiplier = 2.11 [MEASURED]` with
`mitigation_delta = UNKNOWN — a free parameter fitted to the intake tail`, and named **armour** as
"an uninstrumented candidate." The tooltips instrument it.

| Source | +Health |
|---|---|
| Weapon — Poisoned Pusquill's Tail of Corrosion | **+242** |
| Amulet — Menacing Putrid Necklace of Protection | **+321** |
| Belt — Mystic Woven Cord of Soulwarding | **+98** |
| Chest — Mystic Salvaged Armor of Menhir's Wall | **+76** |
| **Four attested items, total** | **+737** |
| **Measured step (T-A max-HP series)** | **759 → 1600 = +841** |

**+737 of +841 = 87.6%, from four flat `+Health` affixes.** The residual ~104 is level-up base HP
(11→12→13) plus physique. **The gear step is no longer a black box, and `ehp_multiplier` need not
enter G-5 as a fitted parameter** — it can be built from named affixes.

The armour side, which §1.8 could not see at all: **58 (chest) + 16 (shoulders) + 16 (legs) + 12
(boots) + 7 (belt) = 109 Armor read**, before helmet / gloves / shield — **plus +16 Armor and +20
Defensive Ability from the cold aura** (§6 F-G6-6), which is *not gear* and switches on **mid-R2**,
not at the boundary. `mitigation_delta` has named components now.

#### F-G6-10 — the poison DoT has a source magnitude, and the spec's damage typing is wrong

G-4 §1.8 carried `added_dot = poison, ~1.000 s tick period [MEASURED, T-B]` with no magnitude and
no source. The weapon tooltip supplies both: **"50 Poison Damage over 5 Seconds"**, amplified by
its own **+38% Poison Damage with +64% Increased Duration** and the amulet's **+21% Poison
Damage**. Five seconds at T-B's measured ~1.000 s tick = **five ticks** — instrument and item agree
on the tick structure. *(This also lands legolas's `componentName`-vs-affix hypothesis: neither —
it is the weapon's own prefix/suffix roll, "Poisoned … of Corrosion".)*

**And the kit's damage typing is not physical + pierce.** At end of run it is, measured:

- base weapon **14–40 Physical + 6–12 Acid** @ **1.78 attacks/sec**;
- **18% Physical → Acid** (weapon affix);
- **100% Pierce → Chaos** (Blight of Ch'thon, §4) — claws' 237 and charge's 375 flat pierce;
- **poison DoT** 50 / 5 s (weapon), at +38% magnitude / +64% duration / +21%;
- **bleed DoT** 810 / 3 s (charge, §5.1);
- cold, on the aura — and on Onslaught, which cannot fire (§5).

**Six damage channels and two conversions**, against a spec that carries physical + pierce. §14.6
ruled the Pierce→Chaos conversion compiles statically into the kit spec as retyped damage;
**the Physical→Acid conversion is a second one and needs the same treatment**. The weapon's
**1.78 attacks/sec** is also a measured cadence input G-5 currently has no source for.

### 7.2 Devotion — zero frames, and the tab was never opened

**No devotion-window frame exists in the 313.** All 37 skill-window frames sit on the **Berserker**
mastery tab; the tab bar reads *"Berserker | Devotion | Select Class"* in every one of them and
**Devotion is never selected**. (The two frames matching the tab bar but not the mastery-level
track — f153, f172 — are Berserker-tab frames whose bar is occluded by a tooltip, verified at full
resolution, not devotion frames.)

**Devotion is settled by G-7, not by me** — §14.5's conjunctive test PASSES (3 earned / 3 unspent /
0 reclaimed / all `devotionLevel` 0). The stills add only a behavioural consistency note, which is
worth exactly what it is worth: **a player who never once opened the Devotion tab across 313
captures spanning the whole run is a player consistent with having spent nothing there.**

---

## §8 — Grades, and the ledger

Written against G-4 §7.1's ATTESTED list. Where G-7 also lands on a row, both are shown — the
value of two instruments is that they can be compared, not that one replaces the other.

| G-4 §7.1 claim | Was | **G-6 (pixels)** | G-7 (`.gdc`) | Agree |
|---|---|---|---|---|
| 4 — `werewolf2` not allocated | ATTESTED (inference) | **MEASURED-ABSENT** — Feral Claws block, f210 | measured-absent | ✓ |
| 4 — `werewolf3` not allocated | ATTESTED (inference) | **ABSENT** (one inference step) | absent | ✓ |
| 4 — `werewolf1b` not allocated | ATTESTED (Matt, §12a) | **CONTRADICTED — ALLOCATED 1/1, "Blight of Ch'thon", 100% Pierce→Chaos** | rank 1, same record, same effect | ✓ *(and Matt reconciled, §14.5)* |
| §1.1 — skill ranks UNKNOWN → T11 | UNKNOWN | **MEASURED — all 5 allocated nodes, plus a DATED SERIES** | measured (snapshot) | ✓ *(G-6 adds the dating)* |
| §1.3 — claws rank (re-centres the A band, §6.5) | UNKNOWN | **MEASURED — 16 from `play_time` 3619; full dated series** | 16 | ✓ |
| §1.5 — Onslaught rank | UNKNOWN | **MEASURED — 13/16; rank 1 until level 9** | 13 | ✓ |
| 1 — devotion zero | ATTESTED | no frames; behavioural consistency only | **MEASURED (conjunctive test passes)** | — |
| 3 — level-12 gear identity | ATTESTED | **MEASURED — 4/4 names + rolled affixes, from tooltips** | 4/4 names exact | ✓ |
| 5 — potions 0/0 | MEASURED | MEASURED (36 stills) | MEASURED | ✓ |
| character level | — | `play_stats` **12** in every still | bio **13**; `maxLevel` lags at 12 | ✓ *(G-6 confirms the lag independently)* |

**New, not on any prior list:** F-G6-5 (A-step dated) · F-G6-6 (Battle Surge sustain + cold aura) ·
F-G6-7 (`defaultkickattack`) · F-G6-9 (gear step itemised, 87.6%) · F-G6-10 (poison magnitude +
six damage channels + 1.78 aps).

**UNCERTAIN, crops preserved for human eyes** (`evidence/`):
(a) which of the two 1/12 nodes is Battle Surge and which is the cold aura — *rank unaffected,
both are 1*; (b) claws' displayed pierce at rank 12 (103 read vs ~177 interpolated; rank 16 matches
exactly at 237); (c) whether the Pierce→Chaos conversion is live in play, given the transform
tooltip still prints "Piercing Damage" after allocation — **§14.6 has since ruled the conversion
static and total, which resolves this; the pixel-level oddity is recorded as a
tooltip-display artifact, not a mechanic.**

**REQUESTS out of seam** (`.arz` is not mine — routed to gandalf as RUN-CONDUCTOR):
1. Is there a `playerclass10` record matching **Battle Surge** (crit-triggered, 100% chance, 6 s
   recharge, 3 s duration, **8% max-health per second**, +4 energy regen/sec) and one matching the
   **reserved cold aura** (50 energy reserved, 12 m radius, cold damage, +20 DA, +16 Armor)?
   **Both are allocated, both are mid-R2, and neither is in the kit spec.** This is the highest-value
   request on the list — it rides U-1 and needs no new tooling.
2. Which `playerclass10` records carry **12 base ranks**, and which of them is a `Skill_Modifier`?
   — closes the 1/12 node pairing and re-confirms `werewolf2`/`werewolf3` absence from the source side.
3. The weapon's **18% Physical→Acid** conversion — same static-compile treatment §14.6 gave
   Pierce→Chaos?

---

## §9 — For H-2 (the band-timing fork), stated plainly

G-4 §6.5 said the exact claws rank would re-centre the A band, and §12a anticipated G-6 might
deliver it without waiting on T11. **It did.** T11 landed anyway, and agrees. §14.5 already
concludes the kit spec and H-2 bands *"now redraft on measured identity."*

What this pass adds to that redraft, beyond the ranks:

- the A-factor is **non-stationary within R2**, and now has a dated partition — target cap climbs
  2→3→4→5 and caps at `play_time` **2918**, less than 40% into the regime (§6 F-G6-5);
- the kit gains a **sustain proc** (8% max-HP/sec, crit-gated) and an **armour/DA aura** at
  `play_time` ∈ (2918, 3619] — **mid-R2, not at the boundary** — neither in the spec (§6 F-G6-6);
- `ehp_multiplier` and `mitigation_delta` **need not be fitted parameters**: +737 of the +841 step
  is four named affixes, and 109+ Armor is itemised (§7.1 F-G6-9);
- the DoT has a magnitude and a duration from source (§7.1 F-G6-10), and the kit runs **six damage
  channels**, not two.

Net: **R2 is not a single-composition regime.** That is the third amendment R2 has taken (G-4
§13.3 C-2 was the second), and it is the one with teeth — the earlier two moved rationale, this one
moves the model. Whether that argues for an intra-R2 partition at `play_time` ≈ 2918/3619 or for
carrying wider bands is a call for gandalf and Matt. I record only that the evidence which would
move the bands arrived, and that it moves considerably more than the one number the fork was drawn
around.

---

## §10 — The Mirror

The player was told. It was written in the tooltip he had open — *"cannot trigger weapon pool
skills"* — sitting three lines above the number he was reading. And for six thousand seconds he
went on feeding points into the one skill the wolf had already taken from him, thirteen ranks of
patient investment in a hand that could not close.

The Mirror does not show what a thing means. It shows that the counter froze at fifty-four while
the rank climbed to thirteen, and that both were on screen at once, in the same frame, the whole
time.

---

**Filed:** galadriel, 2026-07-28. Evidence: `captures/2026-07-28-gd-playtest-v1-g6/`.
Pipeline: `pipeline/gd-playtest-v1/g6_{triage,detect,tooltips,panel_stills,counters,composite,composite2,nodeseries,grid,crop,hover,tiplocate,tiplocate2,tiplocate3,itemtip}.py`.
