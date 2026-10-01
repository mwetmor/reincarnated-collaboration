# C-12 — the D2 WW Barbarian's home frontier point — 2026-10-01

**Mode:** A (analytical; open-question search)
**Commissioner:** gandalf, Run JOIN-1 wave J4a (charter § 4.5, J-S7, commission C-12)
**Question:** what is the hardest content this build is known to clear in its home game, and how fast? The answer has to be a point the arena margin can be measured against.

---

## Verdict

**C-12 returns SEARCHED-UNLOCATED for a timed point.** Under the charter, home margin is therefore **`DEFERRED`**, with the re-entry criterion below printed on the fidelity-cost table.

The search found:

- **Capability is located.** The build clears **Hell Chaos Sanctuary**, and players farm it there. Uber Tristram clears are also claimed.
- **No defensible clear time exists.** Every timed report found fails at least three of the four tests a margin anchor needs:
  1. **Version match.** Our kit is DATAMINED from LoD 1.13. Every timed report found is from **D2R** (patch 2.5 to Season 13).
  2. **Gear match** against the kit record.
  3. **A defined content and clock.** The report must say the /players setting and what the timer measures.
  4. **Independent corroboration.**

The version gap matters directly for this kit. D2R changed both Whirlwind laws that set clear speed:

| Whirlwind at slvl 20 | LoD 1.13 (our data) | D2R (the benchmarks) |
|---|---|---|
| Damage | +102% | +125% |
| Attack rating | +95% | +145% |
| Cadence driven by | the weapon's own IAS | the character's total IAS |

Source: Basin Whirlwind, LoD and D2R tables (`formulas.json` F01 and F02).

The gap cannot be corrected without a model, so a D2R time is not a 1.13 home point.

---

## Candidate points found, with source quality

All candidates are D2R. None is LoD 1.13.

**Area references:**
- Hell Chaos Sanctuary is `Levels.txt` **Id 108** "Chaos Sanctum", Hell area level 85.
- Uber Tristram is **Id 136** "Tristram" (Pandemonium Finale), Hell area level 83. Its bosses `ubermephisto`, `uberdiablo` and `uberbaal` are level 110, with 6500–6600 base HP.
- All of this is DATAMINED from the J-S7 tables (`fabd/diablo2 @ 45112569`).

| # | Content | Claimed result | Version | Gear | Source and quality |
|---|---|---|---|---|---|
| P1 | **Uber Tristram** (hardest content in the game) | "in Under 3 Minutes" (title claim; the video is 224 s long) | D2R Season 13 | **Grief main + Beast off-hand**. This is the closest match to the contract's sword + axe off-hand. Also: CTA/Spirit swap, Guillaume's Face, Treachery/Enigma, Laying of Hands, String of Ears, Gore Rider, Highlord's, Raven Frost / BK ring, skill GCs, Torch, Anni | YouTube `hT1XJvOjQTg`, channel "D2R Build Guide", uploaded 2026-05-13. **TERTIARY, single source, unverified.** No /players setting, no definition of what the timer covers, no merc stated. The channel's authority is unknown. |
| P2 | **Hell Chaos Sanctuary, /players 8**, full clear | **6 min 10 s**; "Diablo drops in about 3 seconds" | D2R 2.5 | "Fort/GFace on barb and Infinity on merc". Weapon not stated in that reply; the poster's main build was an eth BotD maul (2H) | Blizzard D2R forum, Endugu-1671, 2022-11-14, thread 149563. **TERTIARY, single self-report, no video for this time.** Gear does not match: not dual-wield, and Infinity is not in the kit record. |
| P3 | Hell Chaos Sanctuary, /players 8 | "under 4 minutes" | D2R 2.5 | "Fort and double Grief". **This is the best gear match to the kit record** (Grief and Fortitude are both named in it) | Blizzard D2R forum thread 150006: Endugu-1671 relaying "another forum user", 2022-11. **HEARSAY.** No poster identity, no video, no definition of the clock. |
| P4 | Hell Chaos Sanctuary, /players 8 | "under 8 minutes" | D2R 2.5 | eth BotD maul (2H), Treachery, Guillaume's Face, Nosferatu's, Gore Rider, LoH | Blizzard D2R forum, Endugu-1671, 2022-11-13, thread 149563; video linked. **TERTIARY.** Gear does not match the kit (a two-hander). |
| P5 | **Capability**: Hell Chaos Sanctuary, The Pit, Travincal are the build's farming areas; an Uber variant exists | No time given | D2R Season 14 (updated 2026-05-22) | Kit-record gear family (Grief Phase Blade, Beast Berserker Axe, BotD Berserker Axe, Fortitude/Enigma) | Maxroll, Teo1904, "Whirlwind Barbarian Endgame Build Guide". **SECONDARY, authored.** This is the kit record's own primary citation. |
| P6 | Capability: Chaos /players 7 used as the testing standard; dual Grief Phase Blade "fastest" | No times | D2R, before 2.4 | Dual Grief Phase Blade, Enigma vs Fortitude | diablo2.io thread t1452119 (Nate2.0 and others). **TERTIARY.** |

The spread among P2–P4 for the same content (under 4, 6:10 and under 8 minutes at /players 8) is a factor of 2. The gear differs between them, and none of them states what its clock measures. **These are not one point with noise. They are three different builds.**

---

## What is defensible

- **A capability anchor, MEDIUM confidence:** "the kit clears **Hell Chaos Sanctuary** (Levels Id 108) in its home game."
  - Sources: P5 (authored secondary, and the kit record's own citation) plus P2, P4 and P6 (tertiary, independent).
  - **It is non-numeric.** It can serve as a pass/fail annotation beside the arena margin: "does the joined kit survive and clear an Id-108-equivalent encounter?" It cannot serve as a distance.
- **A timed anchor: none.** P3 is the best gear match, but it is hearsay. P1 is the hardest content, but it is a single title claim from an unknown channel.

---

## Re-entry criterion (for the fidelity-cost table's face)

Home margin moves from `DEFERRED` to measured when a timed clear exists that meets **all** of the following:

1. **Version.**
   - The clear is LoD 1.13 (1.10–1.14d mechanics, expansion game).
   - **Or** the conductor rules a D2R point admissible. That ruling records the D2R-vs-1.13 Whirlwind delta (damage %, AR %, cadence law) as a named fidelity cost.
2. **Gear** matches the JOIN profile's pinned loadout: at least the two weapons and the armour (see README § Gear).
3. **Content is stated:** area by `Levels.txt` Id, difficulty, /players, merc yes/no, and what the clock spans (for example, "Chaos: entry to Diablo death, all five seals").
4. **Corroboration:** two independent reports, or one video in which the timer can be frame-counted.

**One cheaper path for the conductor to consider.** This is not a recommendation; it is a decision outside this seam. We hold the DATAMINED 1.13 frontier tables (J-S7) and this packet's formula set. A **home point computed in home rules** would meet criteria 1–3 by construction:

- run the kit, with pinned gear, through a 1.13-faithful replay of Id 108 at Hell and /players N;
- label the result MODEL-DERIVED, not sourced.

It would then lack only criterion 4, which is the one a model cannot supply.

---

## Sources (accessed 2026-10-01)

- Maxroll, Teo1904, Whirlwind Barbarian Endgame Build Guide (Season 14, updated 2026-05-22): https://maxroll.gg/d2/guides/whirlwind-barbarian-guide
- Blizzard D2R forums, Endugu-1671, "2 Hander WW Clears Chaos Under 8 Minutes On p8" (2022-11-13 and 14): https://us.forums.blizzard.com/en/d2r/t/2-hander-ww-clears-chaos-under-8-minutes-on-p8/149563
- Blizzard D2R forums, Skulm-21836, "Players 8 WW Barbarian Chaos Speedruns Terror Zones Farm Build" (2022-11-18, patch 2.5): https://us.forums.blizzard.com/en/d2r/t/players-8-ww-barbarian-chaos-speedruns-terror-zones-farm-build/150006
- YouTube, "D2R Build Guide", "Whirlwind Barbarian DESTROYS Uber Tristram in Under 3 Minutes | D2R Season 13" (2026-05-13, 224 s): https://www.youtube.com/watch?v=hT1XJvOjQTg (metadata read from the page JSON; the video itself was not watched)
- YouTube, "Toa", "What's Better Than Grief? TWO Griefs." (2025-08-03, dual Grief Phase Blade build; no times in the description): https://www.youtube.com/watch?v=YMZQ2NV2c3I
- diablo2.io, "Optimizing whirlwind - what's the best PVE set-up?": https://diablo2.io/forums/optimizing-whirlwind-what-s-the-best-pve-set-up-t1452119.html
- Searched without a usable timed result:
  - speedrun.com d2lod. Its Any% Baal runs time a full-game race, not an endgame-kit clear.
  - d2jsp: "Barbarian Pvm Guide, Diablo II LoD v1.13" (topic 52925876) and "P8 Whirlwind Godly Barbarian" (topic 97529430). Search snippets carried no times; these threads were not opened.
- Basin Wiki, Whirlwind (LoD vs D2R level tables): https://www.theamazonbasin.com/wiki/index.php?title=Whirlwind
- J-S7 tables: `Levels.txt` (sha256 `3163b66e…`), `MonStats.txt` (sha256 `973eedac…`), `fabd/diablo2 @ 45112569`
