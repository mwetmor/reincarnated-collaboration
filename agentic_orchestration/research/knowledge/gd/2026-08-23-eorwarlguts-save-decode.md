# Research — `_EoRWarlGuts` save decode: settling the `circle` archetype referent — 2026-08-23

**Mode:** A (analytical / primary-source probe)
**Commissioner:** knight-rider (for gandalf as RUN-CONDUCTOR, VFX archetype-binding run)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access:** read-only. No game or save file was modified. Work performed on local copies in
`~/gd-scratch/save-probe/`; nothing written back to `/Volumes/reincarnated` (ADR-006).

---

## Summary

**Judgment is not in this build — at all.** It is absent from the character's skill-allocation
block (zero hits for `judg*` across all 367 stored skill entries, in either spelling; the real
record is `judgment1.dbr`, American spelling, and it is not there). **War Cry is allocated at
rank 12** and sits at the third hotbar cell — the contested slot. The skill-bar block was recovered
in full, and the rendered icon for that cell, extracted from the game's own `UI.arc`, is War Cry's
icon: a shouting face in profile with a light burst, which is galadriel's description verbatim.

**Galadriel's read was correct on all three of her claims, including the strong one.** The
`circle` referent for this frameset is **War Cry** (Soldier), not Judgment (Oathkeeper).

The build's other circular effect — the *sustained* player-centred disc galadriel documented
separately in her § 3 — is **Eye of Reckoning**. These are two different circles and should not be
collapsed into one archetype: EoR is a continuous channelled disc with no impact beat; War Cry is a
discrete, cadenced, expanding shockwave ring.

---

## Method and its cost

Prior art carried almost all of this. Before writing anything I checked the existing GD datamine
lane and found a validated `.gdc` reader already in it:

- `agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py` — full stream-cipher
  reader (KIT-CAL-1 pass G-7, 2026-07-28), including the key-sync trick that makes block-level
  resync possible.
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` — `.arz` record reader.
- `.../2026-07-28-gdc-parse-g7/arc_text.py` — `.arc` reader + localization tag bridge.

The cipher constants quoted in the commission are **correct** and are confirmed by that
implementation: `key = seed ^ 0x55555555`; a 256-entry table built by rotate-right-1 then
`* 39916801`; per byte `plain = enc ^ (key & 0xFF)` then `key ^= table[enc]`. One refinement worth
recording: an *int* is decrypted against the key as it stood at the **start** of its four bytes,
whereas four consecutive *byte* reads each use a freshly-advanced key. The key **state** afterwards
is identical either way (it advances on ciphertext only), which is what makes skip-and-resync work
— but the recovered **values** differ. That distinction cost me one wrong turn and is the reason a
naive flat byte dump of a block shows string *contents* correctly while showing every length prefix
as garbage.

The `strings`-and-grep shortcut the commission suggested would have answered Q1 and Q3 on its own.
It did not answer Q2, which needed the `ui_settings` block, which had drifted (see below).

---

## Q1 — Is Judgment allocated? **No. Not at any rank.**

**Confidence: very high. The record path is literally absent from the save.**

The `character_skills` block parses cleanly (v8 drift already solved in the G-7 prior art; block
consumes to its declared end with a zero sentinel). It holds **367 entries, 92 with `level > 0`**.

- A case-insensitive search for `judg` across **all 367 entries** returns **zero hits**.
- The real record is `records/skills/playerclass09/judgment1.dbr` — confirmed by enumerating all
  170 Oathkeeper skill records in the shipped database, where it resolves to display name
  `'Judgment'`. So the string I searched for is the right string.
- Every one of the 15 stored `playerclass09` entries has `level > 0`, i.e. this block stores only
  skills the character has actually invested in. Absence from the block therefore *is* evidence of
  non-allocation, not merely of a zeroed rank.

Two internal consistency checks that the decode is real and not noise:

| Check | Result |
|---|---|
| `totalDevotionUnlocked` in the bio block | 55 |
| Devotion records with `level > 0` in the skills block | **55** — exact match |
| Header class tag | `tagSkillClassName0109` → masteries 01 + 09 |
| Masteries actually present | `playerclass01` (Soldier) + `playerclass09` (Oathkeeper) — exact match |
| `masteriesAllowed` | 2 |

The **fresh-character control** the commission suggested worked, and worked better than expected —
see Q2, where it independently validated a field I had only guessed at.

---

## Q2 — The skill bar, slot by slot

**Confidence: very high for the numbered cells (1–9); medium for the mouse-button assignment.**

This required solving a block the prior art had failed on. `ui_settings` had drifted from the
1.1.9.1 reference (v5) to **v7**, and the G-7 parser bailed out and resynced past it.

### The v7 drift, and why the solution is trustworthy

The slot struct is **unchanged**. I did not assume that — I measured it. The gap between the end of
one skill record-path string and the start of the next is invariantly **17 bytes** across all ten
populated slots, which is exactly `isItemSkill(1) + itemLen(4) + equipLocation(4) + nextType(4) +
nextSkillLen(4)`. A struct that had gained a field could not produce that constant.

The drift is confined to the **preamble**, which gains three int words after the five
`(string, string, byte)` groups:

```
pageCount(int)   slotsPerPage(int)   unknown(int)
```

Empty slots carry `type == 0xFFFFFFFF`. My first solver attempt failed precisely because it
rejected that as an implausible slot type — a reminder that an over-tight oracle silently hides the
answer.

Oracle satisfied, on both files: slots consume the block to exactly `end − 4`; the trailing float is
a plausible `cameraDistance`; the end-of-block sentinel decrypts to 0. **Preamble size 63 is the
only value in 0..99 that satisfies the oracle on both saves.**

Three independent corroborations that the field names are right, not just arithmetically lucky:

1. The second int reads **47** on all three files.
2. The first int reads **1** for `_EoRWarlGuts` and **2** for `_Fresh Character 01` — and the fresh
   character is a Shaman-tree build with **Werewolf**, a transform, which is exactly why it would
   have a second action-bar page. Under the two-page reading its page 1 contains nothing but
   werewolf-form skills (`werewolf1_skill01_claws`, `werewolf1_skill02_charge`).
3. The parsed slot order matches galadriel's own hotbar screenshot cell-for-cell (below).

### Correction and independent replication — prior art I initially missed

**I missed a prior solve of this exact block in my own lane and should not have.** My first
prior-art sweep was truncated and I did not see
`agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/`, which contains a *separately
written* parser (`gdc2.py`, legolas 2026-08-05) that had already solved `ui_settings` v7 against the
same block-end oracle, and had already parsed this same save.

Its conclusion, reached independently three weeks earlier, is the same: v7 writes **three int32**
after the five `(string, string, byte)` groups, and the **second of them is the hotslot count
(47)**. It also records that the FoA fork of the community tooling hard-codes **95** hotslots for
v ≥ 7, which is wrong for a 1.3.0.5-written save and overruns the block.

Its parsed hotslot table for `_EoRWarlGuts` is **identical to mine, index for index**:

```
hotslots[ 1] playerclass09/viremight1.dbr        hotslots[11] default/defaultweaponattack.dbr
hotslots[ 2] playerclass01/warcry1.dbr           hotslots[12] playerclass09/eyeofreckoning1.dbr
hotslots[ 3] playerclass09/ascension1.dbr        hotslots[13] playerclass09/eyeofreckoning1.dbr
hotslots[ 6] itemskillsgdx2/runes/rush_d203.dbr  hotslots[18] playerclass09/summon_celestialguardian1.dbr
hotslots[10] playerclass01/blitz1.dbr            hotslots[19] itemskillsgdx1/relics/summondeathstalker.dbr
```

Zero `judgment` hits in that parse as well. This is a **fourth independent confirmation** of the
answer, from a different decoder written at a different time.

**Where the prior art corrects me:** I named the first int `pageCount` and the second
`slotsPerPage`. That reading is *not* established. For `_EoRWarlGuts` the second int (47) is simply
the slot count and my "1 page × 47" is indistinguishable from "47 slots". For
`_Fresh Character 01` the second int also reads 47, yet 47 slots does **not** consume the block —
95 slots does, and 95 is exactly the FoA fork's hard-coded value. So the fresh file admits two
readings of the same bytes, `2 × 47 + 1 trailing int` or a flat `95`, and I cannot separate them.

**Status: the third word is unnamed, and the first word is `1`/`2` with an unproven meaning.** The
Werewolf-second-bar story is suggestive, not demonstrated. **None of this touches the answer for
`_EoRWarlGuts`**, where the block parses to exactly 47 slots with a zero sentinel under both
readings and under two independently written decoders.

### The bar

Hotbar-key mapping is read off galadriel's capture
`_evidence/hotbar-eor1-t1398.900-x4.png`, whose visible cells run `1 2 3 4 5 [L] [R] 6 7 8 9`.

| ui idx | Key | English | Record |
|---|---|---|---|
| 0 | `1` | *(configured, empty)* | — |
| 1 | `2` | **Vire's Might** | `playerclass09/viremight1.dbr` |
| 2 | **`3`** | **War Cry** ← the contested slot | `playerclass01/warcry1.dbr` |
| 3 | `4` | **Ascension** | `playerclass09/ascension1.dbr` |
| 4 | `5` | *(empty)* | — |
| 5 | `6` | *(empty)* | — |
| 6 | `7` | **Violent Delights** (rune, item skill) | `itemskillsgdx2/runes/rush_d203.dbr` |
| 7 | `8` | *(empty)* | — |
| 8 | `9` | *(empty)* | — |
| 9 | `0` | *(empty)* | — |
| 10 | LMB | **Blitz** | `playerclass01/blitz1.dbr` |
| 11 | LMB (alt set) | Weapon Attack | `default/defaultweaponattack.dbr` |
| 12 | RMB | **Eye of Reckoning** | `playerclass09/eyeofreckoning1.dbr` |
| 13 | RMB (alt set) | Eye of Reckoning | `playerclass09/eyeofreckoning1.dbr` |
| 18 | — | Summon Guardian of Empyrion | `playerclass09/summon_celestialguardian1.dbr` |
| 19 | — | Summon Deathstalker (relic skill) | `itemskillsgdx1/relics/summondeathstalker.dbr` |
| 24, 25 | — | type 2 / type 3 (health & mana potion cells) | — |

**Nine of nine numbered cells match** galadriel's screenshot on both occupancy and icon appearance.
That is the mapping lock.

The LMB/RMB rows are the softer claim. Indices 10–13 are four mouse-button bindings covering GD's
two weapon sets; I read them as LMB-A / LMB-B / RMB-A / RMB-B because the visible `[R]` cell shows
Eye of Reckoning's red swirl, which requires RMB-set-A to be EoR. The alternative pairing
(10/11 = LMB-A/RMB-A) would put the default weapon attack on the visible `[R]` cell and contradict
the screenshot. **Flagged as inference, not record text** — but it does not bear on the question.

### Icon-pixel confirmation

I extracted the actual icon textures from the shipped `resources/UI.arc` (TEX v2: 12-byte header,
then a 124-byte DDS header, then 32×32 uncompressed BGRA) and rendered them. Left to right —
Vire's Might, **War Cry**, Ascension, *(Violent Delights, compressed variant, failed to decode)*,
Eye of Reckoning, **Judgment**:

- Vire's Might — orange running figure → galadriel's cell `2`. Match.
- **War Cry (`skillicon_battlefury_up.tex`) — shouting face in profile with a light burst →
  galadriel's cell `3`. Match, and her description of the icon is verbatim correct.**
- Ascension — purple ascending figure → cell `4`. Match.
- Eye of Reckoning — red swirl → cell `[R]`. Match.
- **Judgment — a vertical column of light striking down. Appears nowhere on the bar.**

Sheet at `~/gd-scratch/save-probe/icon_sheet.png` (scratch, not committed).

---

## Q3 — Is War Cry present and allocated? **Yes, rank 12 (+ its rank-12 modifier).**

**Confidence: very high — record text.**

| Record | English | Rank |
|---|---|---|
| `playerclass01/warcry1.dbr` | **War Cry** | **12** |
| `playerclass01/warcry2.dbr` | Break Morale (modifier) | 12 |

From the shipped database, `warcry1.dbr`:

- `Class = Skill_AttackRadius`
- `skillCooldownTime = 7.5`
- `instantCast = True`
- **no `targetingMode` field** → cast is player-centred
- `distanceProfile = Short`
- `skillSpecialAnimationName = Warcry`
- `skillTargetRadius` at rank 12 → **16.0**
- `radiusEffectName` at rank 12 → `records/fx/skillclass01/warcry4_radius_fxpak01.dbr`

### This settles galadriel's geometry argument from primary source

Her evidence #1 was that the effect is caster-emitted and never cursor-displaced. That is exactly
the field that separates these two skills:

| | Judgment | War Cry |
|---|---|---|
| `Class` | `Skill_AttackRadius` | `Skill_AttackRadius` |
| **`targetingMode`** | **`Point`** (cursor-placed) | *absent* (self-centred) |
| `instantCast` | *absent* | `True` |
| `distanceProfile` | `Moderate` | `Short` |
| `skillCooldownTime` | 5.0 | 7.5 |
| `skillTargetRadius` | 6.0 → 12.0 | 5.0 → 18.0 |
| `skillSpecialAnimationName` | `Nova` | `Warcry` |

Both share a template class, so class alone would not have discriminated them — but `targetingMode
= Point` is present on Judgment and absent on War Cry. Galadriel inferred that distinction from
pixels alone, correctly.

### Cadence

**Zero cooldown reduction on this build.** I resolved all 12 equipped items plus their prefixes,
suffixes, components and augments against `skillCooldownReductionModifier`; nothing carries it.
War Cry's effective cooldown is therefore its 7.5 s base.

Galadriel's **modal 8–12 s** interval sits just above that floor — exactly what a player pressing a
7.5 s skill on-or-near cooldown produces. Her positive identification holds on cadence too.

**One residual tension, stated rather than smoothed:** she also reports a *minimum* observed
re-fire of **5.5 s**, which is below War Cry's 7.5 s floor and cannot happen without CDR. Her own
note anticipates this — she flags that some of her eleven detected onsets are "threshold noise from
the animated cooldown sweep." I think the 5.5 s is a false onset, but I have not proved that, and I
would rather leave it visible. It does not reopen Judgment: Judgment is absent from the save
outright, which is a stronger fact than any cadence argument.

Note also that **Ulzaad's Decree** (devotion, 22 s cooldown, self-buff) is auto-cast *off War Cry*
at 20% on attack — so a minority of War Cry presses carry a second, larger visual. That may account
for galadriel's "six of eleven onsets carry a large flash."

---

## Q4 — What is the circle-shaped ground AoE, if not Judgment?

**Answer: War Cry**, for the discrete cadenced ring in `circle_candidate_unresolved/`. And **Eye of
Reckoning** for the sustained disc she documented separately in § 3. Two distinct circles.

### Full allocated Oathkeeper list (rank)

| Record | English | Rank | Class |
|---|---|---|---|
| `_classtraining_class09` | Oathkeeper (mastery) | 50 | — |
| `eyeofreckoning1` | **Eye of Reckoning** | **15** | `Skill_AttackRadiusSpin`, radius 3.0 |
| `eyeofreckoning2` | Soulfire (modifier) | 12 | orbiting projectile |
| `viremight1` | **Vire's Might** | 1 | `Skill_AttackPathCharge`, cd 3.6, radius 2.2 |
| `viremight2` | Volcanic Stride (modifier) | 1 | ground AoE trail, 4.0 s duration |
| `viremight3` | Tectonic Shift (modifier) | 1 | cooldown reduction on Vire's Might |
| `ascension1` | **Ascension** | 1 | self-buff, cd 24, duration 10 |
| `ascension2` | Clarity of Purpose (modifier) | 1 | — |
| `divinemandate1` | Divine Mandate | 12 | toggled self-buff |
| `presenceofvirtue1` | Presence of Virtue | 12 | toggled radius aura |
| `presenceofvirtue2` | Haven (modifier) | 9 | — |
| `presenceofvirtue3` | Rebuke (modifier) | 10 | — |
| `passive02` | Resilience | 2 | passive |
| `summon_celestialguardian1` | Summon Guardian of Empyrion | 1 | pet, cd 20 |
| `summon_celestialguardian2_petmodifier` | *(pet modifier)* | 12 | — |

**Judgment, Aegis of Menhir, Righteous Fervor, Path of the Three, Safeguard — all absent.**

### Full allocated Soldier list (rank)

| Record | English | Rank | Class |
|---|---|---|---|
| `_classtraining_class01` | Soldier (mastery) | 46 | — |
| `warcry1` | **War Cry** | **12** | `Skill_AttackRadius`, cd 7.5, radius 16.0 |
| `warcry2` | Break Morale (modifier) | 12 | — |
| `blitz1` | **Blitz** | 1 | `Skill_AttackWeaponCharge`, cd 3.5 |
| `blitz2` | Blindside (modifier) | 1 | — |
| `fieldcommand1` | Field Command | 10 | toggled radius aura |
| `fieldcommand2` | Squad Tactics (modifier) | 8 | — |
| `fightingspirit1` | Fighting Spirit | 1 | passive on-hit |
| `passive1` | Military Conditioning | 6 | passive |
| `passive2` | Veterancy | 1 | passive |
| `passive3` | Decorated Soldier | 8 | passive |
| `passive4` | Scars of Battle | 1 | passive |
| `willtolive1` | Menhir's Will | 1 | passive on-life |

**Cadence and Blade Arc are absent.**

### Devotions — 55 stars, and the proc hypothesis does not survive

The commission flagged devotion procs as a wide-open possibility. **It is closed.** The constellations
taken are: Assassin's Blade, Tortoise, Jackal, Stag, Toad, Scales of Ulcama, Dire Bear, Crab,
Kraken, Ulzaad Herald of Korvaak, Azrakaa the Eternal Sands.

**Elemental Storm, Meteor Shower and Reckless Tempest are not among them.** The seven active procs:

| Proc | Class | Bound to (autocast) | Shape |
|---|---|---|---|
| Assassin's Mark | `Skill_AttackBuff` | Eye of Reckoning (on crit, 100%) | single-target debuff |
| Maul (Dire Bear) | `Skill_AttackBuffRadius`, radius 4.5 | Vire's Might (on attack, 20%) | small radius debuff |
| Tip the Scales | `Skill_AttackSpell`, cd 1.0 | Presence of Virtue (on hit, 33%) | targeted spell |
| Turtle Shell | `Skill_BuffSelfShield` | Field Command (at 50% health) | self shield |
| Arcane Barrier | `Skill_BuffSelfShield`, cd 3.0 | Divine Mandate (on hit, 30%) | self shield |
| **Ulzaad's Decree** | `Skill_BuffSelfDuration`, cd 22.0 | **War Cry** (on attack, 20%) | self buff |
| Shifting Sands | `Skill_AttackProjectile`, cd 0.5 | Guardian of Empyrion (on attack, 20%) | projectile |

None is a large expanding ground ring. The autocast bindings are recorded in the save itself
(`autoCastSkill` / `autoCastController` per skill entry), so this is record text, not inference.

### A falsifiable scale prediction for galadriel

If the contested ring is War Cry, its radius is **16.0 game units** against Eye of Reckoning's
**3.0** — a ratio of ~5.3×. Galadriel independently measured the EoR disc at ≈150–160 px radius,
≈1.9× character height, at 1920×1080. War Cry's ring should therefore read at roughly **800 px
radius**, i.e. filling much of the screen. Her language — "large pale shockwave ring", "ring edge at
maximum radius, clean arc readable against terrain" — is consistent with that, but she has not
published a pixel radius for the contested event. **If the ring measures anywhere near the EoR
disc's size, something in this identification is wrong and I want to know.** I do not expect that
outcome, but it is the cheapest remaining refuting test.

---

## Recommendation for the conductor (advisory only — gandalf and Matt decide)

1. Rebind `circle_candidate_unresolved/` to **War Cry**, Soldier, rank 12. The frameset is good;
   only the name was wrong.
2. Do **not** merge it with the Eye of Reckoning frameset. Sustained-channel-disc and
   discrete-expanding-ring are different motion signatures, and the run's archetype vocabulary will
   be worse if they are collapsed. EoR arguably wants an `aura`/`sustained-disc` archetype rather
   than `circle`.
3. Judgment has **no referent in this fixture set**. If the run needs a cursor-placed ground AoE
   (`targetingMode = Point`), it must come from a different capture or a different character.
4. Galadriel's HALT was correct and cost the run nothing. Worth saying plainly: had she labelled
   these frames "Judgment," the corpus would now contain a Soldier shout filed as an Oathkeeper
   targeted AoE, and the error would have been invisible downstream.

---

## Knowledge gaps not resolved

- **`ui_settings` v7 slot semantics beyond type 0/4.** Types 2, 3 and 5 appear at fixed indices
  (24, 25, 46) in every file and are almost certainly the health-potion, mana-potion and a trailing
  sentinel cell. I did not confirm this; they carry no payload, so it did not block the answer.
- **The three new v7 preamble ints.** The second is the hotslot count (47) — established, and
  independently confirmed by the 2026-08-05 prior art. The first (`1` / `2`) and the third (`0` in
  all three files) are **unnamed**; my `pageCount` / `slotsPerPage` reading is a hypothesis, not a
  result. See the correction note in Q2.
- **Indices 14–23 of the slot table.** Occupied by Guardian of Empyrion and the Deathstalker relic
  at 18/19, but these do not correspond to visible numbered cells in the capture. Probably a second
  bar page or the pet-command row. Not determined.
- **The 5.5 s minimum re-fire interval** (see Q3). Unresolved; I lean "detection artifact."
- **Item affix stat rolls** were not resolved — I checked base/prefix/suffix/component/augment
  *records* for `skillCooldownReductionModifier` but did not expand randomizer tables. The CDR
  conclusion is therefore "no source of CDR found," which is strong but not exhaustive.
- **Corpus edition.** Name resolution used the Edition-II depot (2026-07-24), which the G-7 prior
  art validated. The saves date 2026-08-05 / 08-12 and an Edition-III depot (2026-08-08) exists.
  Skill record paths and display names are stable across these, so this does not affect any finding
  above, but a strict re-run should use Edition-III.

---

## Reproduction

```
~/gd-scratch/save-probe/          # scratch, not committed
  gdc_parse.py                    # copied from the G-7 prior art, unmodified
  resolve.py                      # record path -> English, via .arz + Text_EN.arc
  parse_ui.py                     # ui_settings v7, solved
  solve_ui2.py                    # the preamble-size solver + oracle
```

Banked into the lane for reuse:

- `agentic_orchestration/research/scripts/gd_gdc_ui_settings_v7_2026_08_23.py`
- `agentic_orchestration/research/scripts/gd_gdc_skill_name_resolve_2026_08_23.py`

## Source list

**Primary — binary fixtures (read-only local copies):**

- `_EoRWarlGuts/player.gdc`, 98,101 bytes, sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`.
  Both supplied paths — `/Volumes/reincarnated/matt-notes-from-pc/gd-save/` and
  `/Volumes/reincarnated/GD-matt-test/eor-test-2/save/` — are **byte-identical** (hashes verified
  equal), so "two copies" is one artifact.
- `_Fresh Character 01/player.gdc`, 15,473 bytes, sha256 `0be3a99f6ead980210a5c06cd12a09bfe51235c09b9da7d41745fa4eacd5ee91`.
  Control. Also byte-identical to the fixture the G-7 prior art was validated against.

**Primary — shipped game data:**

- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — `database.arz`, `GDX1/2/3.arz`,
  `Text_EN.arc` ×4 (20,245 localization tags).
- `/Users/admin/Games/vendor/grim-dawn/resources/UI.arc` + `gdx1,gdx2/resources/UI.arc` — icon
  textures.

**Project prior art:**

- `agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/` — `gdc_parse.py`, `arc_text.py`
  (KIT-CAL-1 pass G-7, 2026-07-28).
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`.
- `agentic_orchestration/research/scripts/gd_gdc_parse.py` (KC2-PM2 Lap A, 2026-08-12).

**The claim under test:**

- `agentic_orchestration/galadriel/notes/2026-08-23-vfx-p2-gd-framesets.md` § 3, § 4.1–4.4.
- `agentic_orchestration/galadriel/captures/2026-08-23-vfx-p2-gd-framesets/_evidence/hotbar-eor1-t1398.900-x4.png`.

Accessed 2026-08-23/24.
