# KF-2/3 Harvest — d2-fire-sorc supplement (Fire Ball + Meteor)
**Legolas Mode B** | 2026-07-23 | Kit: `d2-fire-sorc` (Fire Ball / Meteor Sorceress)
**Charter ref:** KFL-4 — d2-fire-sorc entered Pilot roster via LE-swap (KFL-3(b) pre-authorized, KFL-4 executed). KFL-5 trust-but-verify finding fired this supplement pass.

---

## CORRECTION ON RECORD

The d2 pass note (`agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-d2.md`) claimed d2-fire-sorc "overlaps substantially — Fire Wall is the primary skill in both." **This is wrong.** Per `kit_mapping` for `d2-fire-sorc` (conductor-verified, KFL-5): primary skills are **Fire Ball** (arc projectile, primary spam) + **Meteor** (ground-targeted delayed AoE). Fire Wall is NOT a d2-fire-sorc skill. This note corrects that claim on record.

---

## SHARED SUBSTRATE — reference only, NOT re-fetched

All of the following were anchored verbatim in the d2 pass note and are referenced here by path.

- **Fire Mastery level table (slvl 1–20, +30% at slvl 1 → +163% at slvl 20, +7%/lvl)** — d2 note §"Fire Wall — Synergies"
- **Sorceress base attributes** (Str 10 / Dex 25 / Vit 10 / Energy 35 / Base Life 40 / Base Mana 35 / Life/lvl +1 / Mana/lvl +2) — d2 note §"Character Attributes"
- **FCR breakpoints** (0%=13f · 9%=12f · 20%=11f · 37%=10f · 63%=9f · 105%=8f · 200%=7f) — d2 note §"Cast Speed / FCR Breakpoints"
- **Act-1 Normal starter mobs** (Fallen, Zombie, Skeleton, Corrupt Rogue, Spike Fiend — HP, defense, damage, XP, resist refs) — d2 note §"KF-3 MONSTER SIDE"

Shared substrate reference path: `agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-d2.md`

---

## KIT SIDE (KF-2 input) — Fire Ball

### Fire Ball — Skill Level Table

**Source 1:** rankedboost.com/diablo-2/sorceress/fire-ball/ (accessed 2026-07-23)
**Source 2 (corroborating):** diablo2.wiki.fextralife.com/Fire+Ball (accessed 2026-07-23)
Both sources return identical values for all 20 levels.

Fextralife verbatim: "Required Level: 12 | Prerequisite: Fire Bolt | Cast Delay: None | Explosion Radius: 1 yard | Damage Type: Fire"

| Skill Level | Mana Cost | Min Fire Dmg | Max Fire Dmg |
|-------------|-----------|-------------|-------------|
| 1  | 5    | 6   | 15  |
| 2  | 5.5  | 14  | 24  |
| 3  | 6    | 21  | 33  |
| 4  | 6.5  | 29  | 41  |
| 5  | 7    | 36  | 50  |
| 6  | 7.5  | 43  | 58  |
| 7  | 8    | 51  | 67  |
| 8  | 8.5  | 58  | 75  |
| 9  | 9    | 71  | 90  |
| 10 | 9.5  | 84  | 104 |
| 11 | 10   | 98  | 118 |
| 12 | 10.5 | 111 | 132 |
| 13 | 11   | 124 | 147 |
| 14 | 11.5 | 137 | 161 |
| 15 | 12   | 150 | 175 |
| 16 | 12.5 | 163 | 189 |
| 17 | 13   | 179 | 206 |
| 18 | 13.5 | 195 | 224 |
| 19 | 14   | 211 | 241 |
| 20 | 14.5 | 227 | 258 |

**At slvl 20: 227–258 fire damage per cast, mana cost 14.5, no cast delay, radius 1 yard.**

### Fire Ball — Synergies

Source: rankedboost.com/diablo-2/sorceress/fire-ball/ + diablo2.wiki.fextralife.com/Fire+Ball (both accessed 2026-07-23). Both sources agree verbatim.

**Receives synergy bonuses from:**
- Fire Bolt: "+14% fire damage per level"
- Meteor: "+14% fire damage per level"

**Provides synergy bonuses to:**
- Fire Bolt: "+16% fire damage per level"
- Meteor: "+5% fire damage per level"
- Hydra: "+3% fire damage per level"

**Damage model note for KF-2:** Fire Ball is a single-hit projectile (impact damage, fire type). No DoT component. Crit note: D2 Sorceress has no spell crit — confirmed in d2 shared substrate (d2 note §"Crit Mechanics"). Expected = mean roll (non-crit, no crit weighting needed for Fire Ball). Fire Mastery synergy applies multiplicatively per shared substrate table.

---

## KIT SIDE (KF-2 input) — Meteor

### Meteor — Skill Level Table

**Source 1:** rankedboost.com/diablo-2/sorceress/meteor/ (accessed 2026-07-23)
**Source 2 (corroborating):** diablo2.wiki.fextralife.com/Meteor (accessed 2026-07-23)
Both sources return identical values for all 20 levels.

Fextralife verbatim: "Required Level: 24 | Cast Delay: 1.2 seconds (does not share cooldown with other skills) | Radius: 4 yards | Damage Type: Fire"

| Skill Level | Mana Cost | Impact Fire Dmg (min-max) | Fire Dmg/sec (min-max) |
|-------------|-----------|--------------------------|------------------------|
| 1  | 17 | 88–110   | 35–58   |
| 2  | 17 | 113–137  | 44–67   |
| 3  | 18 | 138–165  | 53–77   |
| 4  | 18 | 163–192  | 63–89   |
| 5  | 19 | 189–220  | 72–98   |
| 6  | 19 | 214–247  | 84–107  |
| 7  | 20 | 239–275  | 93–117  |
| 8  | 20 | 265–302  | 103–126 |
| 9  | 21 | 308–347  | 114–138 |
| 10 | 21 | 350–392  | 126–150 |
| 11 | 22 | 393–437  | 138–164 |
| 12 | 22 | 436–482  | 150–175 |
| 13 | 23 | 479–528  | 164–187 |
| 14 | 23 | 522–573  | 175–199 |
| 15 | 24 | 565–618  | 187–210 |
| 16 | 24 | 608–663  | 199–222 |
| 17 | 25 | 696–752  | 213–236 |
| 18 | 25 | 782–841  | 227–253 |
| 19 | 26 | 869–930  | 243–267 |
| 20 | 26 | 955–1019 | 257–281 |

**At slvl 20: 955–1,019 impact fire damage + 257–281 fire damage/sec (ground burn), mana cost 26, cast delay 1.2 sec, radius 4 yards.**

### Meteor — Synergies + Cast Delay

Source: rankedboost.com/diablo-2/sorceress/meteor/ + diablo2.wiki.fextralife.com/Meteor (both accessed 2026-07-23). Both sources agree verbatim.

**Receives synergy bonuses from:**
- Fire Bolt: "+5% fire damage per level"
- Fire Ball: "+5% fire damage per level"
- Inferno: "+3% average fire damage per second per level"

**Provides synergy bonuses to (Fextralife):**
- Fire Bolt: "+16% fire damage per level"
- Fire Ball: "+14% fire damage per level"

**Cast delay:** 1.2 seconds (Fextralife verbatim: "does not share cooldown with other skills"). This is an independent 1.2-sec lockout per Meteor cast — NOT shared with Fire Ball.

**Prerequisites (Fextralife verbatim):** "Fire Bolt, Inferno, Blaze, Fire Ball, Fire Wall must be learned first."

**Damage model note for KF-2:** Meteor has two distinct damage components per cast: (1) impact — single-hit fire damage on landing; (2) ground burn — fire damage per second (DoT) at the impact crater. The per-second DoT duration is NOT stated verbatim in either fetched source — see GAPS. Both components are fire type; Fire Mastery applies to both. No spell crit (same as Fire Ball above).

---

## Build-Point Note (d2-fire-sorc)

**Source attempt:** maxroll.gg/d2/guides/fire-sorceress-guide — HTTP 404.
**Source attempt:** maxroll.gg/d2/guides/meteor-sorceress-guide — HTTP 404.

GAP: build-point note (skill allocation, FCR target for Fire Ball / Meteor sorc) not reachable via Maxroll. Both URL attempts failed. Community guidance (not verbatim-anchor grade) consistently cites: Fire Ball maxed (20), Meteor maxed (20), Fire Mastery maxed (20), Fire Bolt to 1 or maxed for synergy, FCR target 105% or 63%; but no verbatim anchor retrieved for this variant. Not recorded as anchored data.

---

## GAPS

| Field | Status |
|---|---|
| Meteor ground burn duration (seconds) | GAP — neither rankedboost nor fextralife states burn duration verbatim in fetched content. Known from game: ~2 seconds per crater; not citable from these fetches |
| Meteor ground burn tick rate | GAP — same as Fire Wall (per-second stated; per-tick not verbatim-anchored in any public source) |
| Fire Ball explosion radius confirmation | PARTIAL — fextralife states "1 yard" verbatim; rankedboost does not state radius. One-source anchor |
| Build-point skill allocation (Fire Ball / Meteor sorc) | GAP — Maxroll guide URL 404 ×2; no verbatim anchor retrieved for this build variant |
| FCR target for d2-fire-sorc specifically | GAP — shared FCR breakpoint table (d2 note) is verbatim; the preferred breakpoint for this build is guidance-level only (105% cited broadly) |
| Fire Ball mana cost fractional values | NOTE — mana cost increments in 0.5 steps (5, 5.5, 6, …, 14.5); D2 internally uses a fixed-point mana system. Both sources agree; not a gap, noted for formula rule authors |
| Stat allocations at build point | GAP (same as d2 note) — base start values verbatim; build-point totals for this variant not retrieved |

---

## Sources consulted (all read-only, 2026-07-23)

| URL | Result |
|---|---|
| https://rankedboost.com/diablo-2/sorceress/fire-ball/ | Fetched — full level table slvl 1–20, synergies verbatim |
| https://diablo2.wiki.fextralife.com/Fire+Ball | Fetched — corroborating full level table, required level 12, radius 1 yard, synergies verbatim |
| https://rankedboost.com/diablo-2/sorceress/meteor/ | Fetched — full level table slvl 1–20, synergies verbatim |
| https://diablo2.wiki.fextralife.com/Meteor | Fetched — corroborating full level table, required level 24, cast delay 1.2 sec, radius 4 yards, synergies verbatim |
| https://maxroll.gg/d2/guides/fire-sorceress-guide | HTTP 404 — GAP |
| https://maxroll.gg/d2/guides/meteor-sorceress-guide | HTTP 404 — GAP |
