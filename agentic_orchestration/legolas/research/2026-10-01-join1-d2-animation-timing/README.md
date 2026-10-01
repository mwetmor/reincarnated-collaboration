# Research — JOIN-1 D2 animation timing packet (d2-ww-barb, d2-fire-sorc) — 2026-10-01

**Mode:** A (analytical; primary-source probe)
**Commissioner:** gandalf · **Consumer:** Run C-9 (Graphic Arts) and the drax port, under JOIN-1 J4a/J4b
**Machine-readable twin:** `packet.json` in this directory (one entry per kit and mode, plus `laws` and `sources`)
**Game version for every number unless flagged:** Diablo II: Lord of Destruction, **expansion game**, 1.10–1.14d mechanics, using the 1.13 txt data we hold (`fabd/diablo2 @ 45112569`). Where D2R differs, the law says so.
**Tick:** D2 game logic runs at 25 frames per second. One tick is 0.04 s. Every duration below is in ticks unless marked s.

**Labels.** **DATAMINED** means read from a game data file, a named AnimData dump, or the D2MOO reverse-engineered DLL source. **COMMUNITY-VERIFIED** means a community table or formula that at least two independent sources agree on, and that this packet's generator reproduced by computation. **INFERRED** means this packet derived it from labelled inputs, and the derivation is stated.

---

## Summary

1. **Every breakpoint table in this packet is reproduced exactly by its formula plus the AnimData inputs.** The generator aborts on any mismatch. The tables are Sorceress and Barbarian FCR (with action ticks), both FHR tables, Sorceress FBR, Barbarian 1SS attack speed and the Whirlwind cadence.
2. **At 0% FCR the Sorceress casts in 13 ticks (0.52 s) and releases on tick 7 (0.28 s).** Her FCR breakpoints are 0/9/20/37/63/105/200 → 13/12/11/10/9/8/7 ticks. Fire Ball and Meteor use the same D2 animation (`SC`), so their timing law is identical.
3. **Meteor:**
   - impact lands **60 ticks (2.4 s) after the action tick**;
   - its cooldown is **30 ticks (1.2 s) from the action tick**;
   - the fire field lasts `30 + 15·(slvl−1)` ticks (12.6 s at slvl 20).
4. **Whirlwind does not run on an attack animation.** It is a fixed **8-tick sequence** (A1 frames 0–6) whose MELEE_ATTACK events fall every 4 ticks.
   - The first two checks (ticks 4 and 8) always attack.
   - After that, attacks are spaced by **D ∈ {4, 6, 8, 10, 12}**, set only by the weapon's own IAS and WSM, and land on the 4-tick event grid.
   - Each attack hits **one** target, chosen round-robin. Dual wield gives up to two attacks per check.
5. **Two kit-reachable modes are MISSING from the contract:**
   - the Barbarian's plain **attack**: Whirlwind aimed at a target already in melee range does one normal Attack;
   - the Sorceress's **block**: her kit-record loadout carries a shield.

---

## 1. The full animation list, and what the contract covers

D2 player modes (PlrMode): NU neutral · WL walk · RN run · TN/TW town neutral/walk · A1/A2 attack · SC cast · SQ sequence · GH get-hit · BL block · DT death · DD dead · KK kick · TH throw · S1–S4 skill specials · KB knockback.

**`d2-ww-barb`** has dual-wielded sword + axe. Both are Weapons.txt wclass `1hs`, so the composite weapon class is **1SS**.

| D2 mode | Role in the kit | Contract state | Status | D2 frames/dir · AnimSpeed | Base duration at 0% gear |
|---|---|---|---|---|---|
| NU | field idle | `idle` (12) | COVERED | 8 · 96 | loop 21.33 ticks (0.853 s) |
| WL | walk | `walk` (12) | COVERED | 8 · 168 | loop 12.19 ticks (0.488 s) ⚠ Q3 |
| RN | run | `run` (12) | COVERED | 8 · 216 | loop 9.48 ticks (0.379 s) ⚠ Q3 |
| SQ (seqnum 10) | Whirlwind, Id 151 | `whirlwind` (16) | COVERED, see C2 | sequence of 8 frames from A1 1SS (16 · 256), frames 0,1,2,3,3,4,5,6 | loop **8 ticks (0.32 s)**; hit events every 4 ticks |
| SC | Battle Orders, Id 149 | `shout` (12) | COVERED | 14 · 256, action 9 | **13 ticks (0.52 s)**; release tick 9 (0.36 s) |
| GH | hit recovery | `hit` (8) | COVERED | 5 · 256 | 9 ticks (0.36 s) |
| DT → DD | death → corpse | `death` (16, hold last) | COVERED | 27 · 240, then DD 1 frame | ≈28.8 ticks (≈1.15 s), then hold |
| **A1** | the plain Attack when WW targets a unit already in melee range | — | **MISSING** | 16 · 256, action 7 | 15 ticks (0.60 s); action tick 7 (0.28 s) |
| BL | block | — | NOT APPLICABLE | — | no shield, so no block |
| TN / TW | town | — | NOT NEEDED | 16 · 80 / 8 · 256 | — |

**`d2-fire-sorc`** (Meteor Sorceress) has a weapon-class assumption: **1HS orb main hand plus a shield**. The kit record names:
- Eschuta's Temper, an Eldritch Orb, Weapons.txt wclass `1hs`;
- Heart of the Oak in a flail (`1hs`) as the alternative;
- a Spirit Monarch shield.

It names no staff. **This choice does not change any timing she uses.** In the AnimData dump her SC, NU, WL, RN, TN, TW and GH records are identical across every weapon class, and DT/DD are HTH-only. The only effect of the shield is that BL becomes reachable. (INFERRED from the kit record, Weapons.txt and the dump.)

| D2 mode | Role in the kit | Contract state | Status | D2 frames/dir · AnimSpeed | Base duration at 0% gear |
|---|---|---|---|---|---|
| NU | field idle | `idle` (12) | COVERED | 8 · 128 | loop 16 ticks (0.64 s) |
| WL | walk | `walk` (12) | COVERED | 8 · 256 | loop 8 ticks (0.32 s) ⚠ Q3 |
| RN | run | `run` (12) | COVERED | 8 · 256 | loop 8 ticks (0.32 s) ⚠ Q3 |
| SC | Fire Ball, Id 47 | `cast_fireball` (12) | COVERED | 14 · 256, action 7 | **13 ticks (0.52 s)**; release tick 7 (0.28 s) |
| SC | Meteor gesture, Id 56 | `cast_meteor` (16) | COVERED | **the same SC animation** | **the same: 13 ticks, release tick 7** |
| GH | hit recovery | `hit` (8) | COVERED | 8 · 256 | 15 ticks (0.60 s) |
| DT → DD | death → corpse | `death` (16, hold last) | COVERED | 24 · 256, then DD 1 frame | 24 ticks (0.96 s), then hold |
| **BL** | shield block | — | **MISSING** (only if the model resolves blocks) | 5 · 256 | 9 ticks (0.36 s) |
| A1 | melee attack | — | NOT NEEDED | 20 · 256, start 2, action 12 | — |
| TN / TW | town | — | NOT NEEDED | 16 · 80 / 8 · 256 | — |
| — | Teleport (54) | — | EXCLUDED by the charter | (would be SC) | — |

Operand rows 36 (Fire Bolt), 61 (Fire Mastery) and 37 (Warmth) need no animation. 61 and 37 are passives, and 36 is never cast in this kit.

**Labels and cross-checks for the frame data.** All of it is DATAMINED from the Basin AnimData dump. These rows are cross-checked:
- SC, GH and BL against Maxroll's per-class "casting base / hit base / block base / animation speed" table;
- A1 against Basin's "Attack speed" page;
- the WW sequence against D2MOO `gPlayerSequenceWhirlwind`.

NU, WL, RN, TN and DT appear in **one dump only**. That dump agrees with the second sources on every row that can be checked, but these rows have no independent confirmation. Decoding `animdata.d2` with `pastelmind/d2animdata` from any D2 install would settle them.

---

## 2. Render sampling is not D2 frame count (contract § 2.1)

The contract's counts are **render sampling**: 12 for locomotion and casts, 16 for whirlwind, death and Meteor, 8 for hit. They are not D2 frame counts, and **neither count carries duration**. D2's own frames per direction are 8 / 8 / 8 / 14 / 5–8 / 24–27, and an 8-frame sequence for WW. Each duration comes from the speed laws in § 3.

The contract's rule "N is art resolution, not timing" is therefore consistent with D2. **Nothing in the data contradicts the contract's choice of N.**

**D2's playback model** (Maxroll, Basin, and D2MOO `Units.cpp`):
- An animation counter advances `AnimRate/256` drawn frames per tick.
- The animation ends when the counter reaches the last frame. That is why a 14-frame cast takes 13 ticks: the `−1` in the formulas.
- An event fires on the tick where the counter reaches the ActionFlag frame.
- The port's two-segment warp (contract § 1.2, § 6) is the right model for this: segment `[0, r]` spans `[0, action_tick]` and `[r, N−1]` spans `[action_tick, end]`.

**The release fraction moves with gear**, and the port's independent segment warp absorbs this:

| Cast | 0% FCR | Max FCR (200%) |
|---|---|---|
| Sorceress | 7/13 = 0.538 | 4/7 = 0.571 |
| Barbarian Battle Orders | 9/13 = 0.692 | 6/7 = 0.857 |

**A suggestion, if C-9 authors its clips in D2 proportions at 0% FCR** (INFERRED, not a requirement). Using the contract's own `r = round((N−1)·release_s/T)`:

| Clip | N | r |
|---|---|---|
| `cast_fireball` | 12 | 6 |
| `cast_meteor` | 16 | 8 |
| `shout` | 12 | 8 |

---

## 3. Speed laws and breakpoint tables

**Effective-stat conversion:** `E = floor(120·X/(120+X))`. It applies to IAS, FCR, FHR and FBR. FCR and IAS are capped at 75 effective; this is DATAMINED from D2MOO and matches Maxroll. Faster Run/Walk uses 150 in place of 120.

### 3.1 Sorceress cast rate: Fire Ball and Meteor (COMMUNITY-VERIFIED)

`ticks = ceil(256·14 / floor(256·(100+EFCR)/100) − 1)` · `action = ceil(7·256 / floor(256·(100+EFCR)/100))`

| FCR ≥ | 0 | 9 | 20 | 37 | 63 | 105 | 200 |
|---|---|---|---|---|---|---|---|
| cast ticks | 13 | 12 | 11 | 10 | 9 | 8 | 7 |
| seconds | 0.52 | 0.48 | 0.44 | 0.40 | 0.36 | 0.32 | 0.28 |

| FCR ≥ | 0 | 20 | 63 | 200 |
|---|---|---|---|---|
| action tick | 7 | 6 | 5 | 4 |

**Sources:** Maxroll (D2R 2.4), Basin Sorceress table (LoD), and the formula over AnimData `SO SC 14/256/7`. All three agree, so LoD and D2R are identical here. Lightning and Chain Lightning use a separate 19-frame table, which this kit does not use.

### 3.2 Barbarian cast rate: Battle Orders, Skills row 149 (COMMUNITY-VERIFIED)

`ticks = ceil(256·14 / floor(256·(100+EFCR)/100) − 1)` · `action = ceil(9·256 / …)`

| FCR ≥ | 0 | 9 | 20 | 37 | 63 | 105 | 200 |
|---|---|---|---|---|---|---|---|
| cast ticks | 13 | 12 | 11 | 10 | 9 | 8 | 7 |

| FCR ≥ | 0 | 15 | 39 | 86 |
|---|---|---|---|---|
| action tick | 9 | 8 | 7 | 6 |

**Battle Orders is FCR-driven, not IAS-driven:**
- Its Skills.txt row has `seqtrans=SC`.
- D2MOO sends `PLRMODE_CAST` down the FCR path before any attack-rate check. So the row's `UseAttackRate=1` is inert for this skill.

**Sources:** Maxroll, Basin Barbarian table, and the formula.

### 3.3 Hit recovery (FHR) (COMMUNITY-VERIFIED)

`ticks = ceil(256·Base / floor(256·(50+EFHR)/100) − 1)`. Base is 5 for the Barbarian and 8 for the Sorceress. D2MOO confirms the `50+` (get-hit plays at half rate).

| Barbarian FHR ≥ | 0 | 7 | 15 | 27 | 48 | 86 | 200 |
|---|---|---|---|---|---|---|---|
| ticks | 9 | 8 | 7 | 6 | 5 | 4 | 3 |

| Sorceress FHR ≥ | 0 | 5 | 9 | 14 | 20 | 30 | 42 | 60 | 86 | 142 | 280 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ticks | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 |

**Sources:**
- **Barbarian:** Maxroll, cross-checked against the formula over AnimData `BA GH 5/256`. Basin's Barbarian FHR table did not render when fetched.
- **Sorceress:** Maxroll and Basin both have it.

### 3.4 Sorceress block (FBR), only if blocks are modelled (COMMUNITY-VERIFIED)

`ticks = ceil(256·5 / floor(256·(50+EFBR)/100) − 1)`

| FBR ≥ | 0 | 7 | 15 | 27 | 48 | 86 | 200 |
|---|---|---|---|---|---|---|---|
| ticks | 9 | 8 | 7 | 6 | 5 | 4 | 3 |

### 3.5 Barbarian normal attack (A1, 1SS) (COMMUNITY-VERIFIED)

`ticks = ceil(256·16 / floor(256·(100+ΔEIAS)/100)) − 1`, where `ΔEIAS = EIAS(gear IAS) + skill IAS − WSM_eff`, clamped to [−85, 75].

**Dual-wield WSM** (Basin; D2MOO: `rate += (R+L)/2 − R`):
- main weapon in the **right** slot: `WSM_eff = (L+R)/2 − L + R`;
- main weapon in the **left** slot: `WSM_eff = (L+R)/2`.

| ΔEIAS ≥ | −30 | −26 | −23 | −19 | −15 | −10 | −5 | 0 | 8 | 15 | 24 | 34 | 46 | 61 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ticks | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 |

| ΔEIAS ≥ | −29 | −21 | −12 | 0 | 17 | 41 | 75 |
|---|---|---|---|---|---|---|---|
| action tick | 10 | 9 | 8 | 7 | 6 | 5 | 4 |

The action-tick row is INFERRED: it uses the same ceil rule as the cast action flag. The attack ticks reproduce the full Basin table.

### 3.6 Whirlwind hit cadence (LoD 1.10–1.14d, expansion game) (DATAMINED)

**Sources:**
- D2MOO `SKILLS_SrvDo076_Whirlwind`, `ITEMS_GetWeaponAttackSpeed` and `gPlayerSequenceWhirlwind`;
- cross-checked against Basin's Whirlwind table and the d2mods 1.09b worked example.

**The mechanism, step by step:**
1. **The sequence** is 8 sequence frames showing A1 frames `0,1,2,3,3,4,5,6`. Its MELEE_ATTACK events are on sequence frames 3 and 7.
2. **It plays at 256 × OTHER_ANIMRATE**, which is one sequence frame per tick. **IAS does not change it.** The reason is in the code: the `SQ` mode uses attack rate only when the skill has `UseAttackRate`, and row 151 leaves that column empty. So `srvdofunc 76` runs every 4 ticks: 4, 8, 12, …
3. **The first two events (ticks 4 and 8) always attack.**
4. **After that**, the next attack is scheduled D ticks after the *scheduled* (not actual) previous one, and fires on the first 4-tick event at or after it.
5. **D is computed** as follows:
   - `ws = (16<<8) // ((256·(100+E))//100)`, with integer division, where `E = weapon IAS − weapon WSM` and **only the weapon's own stats count**;
   - then D = 4 if ws<12 · 6 if <15 · 8 if <18 · 10 if <20 · 12 if <23 · 14 if <26 · else 16.

| Weapon E = IAS − WSM ≥ | 34 | 8 | −10 | −19 | −30 (e.g. a WSM +20 weapon with 0 IAS: E = −20) |
|---|---|---|---|---|---|
| D (ticks) | 4 | 6 | 8 | 10 | 12 |
| mean checks per second | 6.25 | 4.17 | 3.13 | 2.5 | 2.08 |

**Example hit ticks after the start of a whirl:**

| D | Hit ticks |
|---|---|
| 4 | 4, 8, 12, 16, 20 … |
| 6 | 4, 8, 16, 20, 28, 32, 40 … (gaps alternate 8 and 4) |
| 8 | 4, 8, 16, 24, 32 … |
| 10 | 4, 8, 20, 28, 40, 48 … |
| 12 | 4, 8, 20, 32, 44 … |

**Targeting rules:**
- **Per check:** each attack hits **one** target. With two melee weapons there are up to **two attacks per check**, and the second takes the next target. A flag toggles after every attack, which alternates the hands.
- **Per target:** targets are picked **round-robin by unit GUID** within a 5-subtile (3 1/3-yard) search radius. The pick is the next GUID above the last target, wrapping to the lowest. With N targets in reach, each is hit once per N attacks. The target must also be in melee reach.
- **Interrupts:** after the first attack, nothing interrupts the whirl: not hit recovery, block, knockback or stun.
- **Game mode:** in a **non-expansion** game every event attacks, so D = 4 for every weapon (D2MOO). JOIN-1's kit is LoD.

**Kit example.** Grief in a Phase Blade has WSM −30 and Grief adds 30–40% IAS, so E = 60–70 → ws 9–10 → **D = 4**. The off-hand axe base is not pinned (Q1).

**Conflict: Arreat Summit vs Basin and the code.**
- The Arreat Summit lists one-handed breakpoints at weapon speed 15/10/−10/−34, which is E ≥ −15/−10/10/34.
- That disagrees with Basin and the code at two of the four steps: the 10-tick and 6-tick ones.
- **I trust Basin and the code.** The integer formula reproduces Basin exactly; the Arreat values look rounded.

**D2R 2.4.3+ uses a different law** (COMMUNITY-VERIFIED, from a patch-note quote in a single forum source). The interval equals the character's basic-attack action frame with **all** IAS, including skills and slows, and dual wield averages the two weapons' frames, rounding up. This is **not** the version of our data. It is recorded for completeness only.

### 3.7 Movement (walk/run law COMMUNITY-VERIFIED; WW travel speed DATAMINED)

| Law | Formula | Source |
|---|---|---|
| Base speeds (both classes) | walk **6**, run **9** (Basin reads these as yards/s) | CharStats `WalkVelocity` / `RunVelocity`, DATAMINED |
| Walk | `max(6·(100+Speed)/100, 1.5)` | Basin |
| Run | `max(9 + 6·Speed/100, 1.5)` | Basin |
| Faster Run/Walk | `FRW_eff = floor(150·FRW/(150+FRW))` | Basin, D2MOO |
| **Whirlwind travel** | `CharStats WalkVelocity << 8` — the **walk** speed, not run — then normal movement modifiers apply | D2MOO, Basin |

---

## 4. Skill-timing fields (Skills.txt / Missiles.txt, 1.13, DATAMINED)

| Row | anim | seqtrans | seqnum | seqinput | delay | range | Other timing |
|---|---|---|---|---|---|---|---|
| 151 Whirlwind | SQ | A1 | 10 | — | — | none | weapsel 2 · itypea1 mele · srvst 38 / srvdo 76 · clt 31 / 45 · UseAttackRate **empty** · Param3 = 1 ("Attacks per tick") |
| 149 Battle Orders | SC | SC | — | — | — | none | interrupt 1 · UseAttackRate 1 (inert for SC) · duration `750 + 250·(slvl−1) + 125·synergy` ticks = 20 + 10·slvl s, +5 s per synergy level · missile `battleorders` Vel 30, Accel −500, Range 15, NextDelay 4 |
| 47 Fire Ball | SC | SC | — | — | — | none | interrupt 1 · missile `fireball` Vel 20 (px/tick), Range 50 ticks (2.0 s), explosion radius 4 subtiles (2 2/3 yd) |
| 56 Meteor | SC | SC | — | — | **30** (1.2 s) | none | interrupt 1 · `meteorcenter` Range 60 ticks (AlwaysExplode; client fall 59 ticks) · impact radius `ln12` = 6 subtiles (4 yd) · fire `Param3 30 + Param4 15/level` ticks · 18 `meteorfire` missiles, damage rate 41/1024 |
| 36 / 61 / 37 | SC / passive / passive | SC | — | — | — | none | operand rows only; Fire Bolt shares Vel 20 / Range 50 with Fire Ball |

### Meteor timeline at 0% FCR, slvl 20 (from the cast-start event)

| t (s) | Event | Source / label |
|---|---|---|
| 0.00 | cast start | — |
| **0.28** | action tick: the call. Cooldown starts; the `meteorcenter` missile spawns at the target | Skills/Missiles, DATAMINED; Basin |
| 0.52 | gesture ends; the `cast_meteor` clip ends here | FCR law |
| 1.48 | cooldown ends (action + 1.2 s). In LoD the delay is global: no other delayed skill can be cast during it | Arreat, Basin, Maxroll |
| **2.68** | impact: action + 2.4 s (60 ticks); damage in a 4-yard radius; fire field spawns | Missiles.txt Range 60, DATAMINED; Basin "2.4 second (60 frame) delay between point of casting (action frame) and impact" |
| 15.28 | fire field ends at slvl 20 (`30 + 15·19` = 315 ticks = 12.6 s) | D2MOO MissMode SrvHit14 + Skills Param3/4, DATAMINED |

Basin gives the fire duration as `14 + 15·slvl`, one tick shorter (Q5).

**Source for each formula:**
- the missile-range rule `Param3 + (slvl−1)·Param4` is D2MOO `MISSMODE_SrvHit14_MeteorCenter`;
- the cooldown-starts-at-action rule is Basin and Maxroll;
- the radius conversion `subtiles × 2/3 = yards` is d2mods KB and Basin. It reproduces Basin's 2 2/3 yd for Fire Ball and 4 yd for Meteor.

---

## 5. Where the contract and the data disagree, or the contract is silent

| # | Contract says | Data says | Recommendation |
|---|---|---|---|
| C1 | 12/16/8 frame counts | D2 is 8/8/8/14/5/8/24/27 frames, plus an 8-frame WW sequence | No conflict. These are render sampling vs D2 counts; duration comes only from § 3 |
| C2 | `whirlwind`: one revolution per 16-frame cycle | D2's WW cycle is an 8-tick sequence showing a partial swing (A1 frames 0–6). The spin is a facing rotation at an UNKNOWN rate. Hits are phase-locked to sequence frames 3 and 7, i.e. on the 4-tick grid | The port should take hit events from the cadence law, never from art phase. The revolution period is open (Q2) |
| C3 | Separate `cast_fireball` / `cast_meteor` clips | Both are D2 `SC`, with identical timing | Separate clips are fine; feed both the one FCR law. Meteor differs only by its delay and its impact at action + 60 ticks |
| C4 | Sorceress `main_tip`/`main_grip` only if she has a staff; no `block` state | The kit record has an orb + Spirit Monarch shield, no staff. BL is reachable | Conductor call: add `block` (D2 BL, FBR law § 3.4) if the JOIN model resolves blocks |
| C5 | Barbarian state set: idle/walk/run/whirlwind/shout/hit/death | WW clicked on a unit already in melee range performs one A1 Attack | Add an `attack` one-shot with release (A1 1SS, § 3.5) or have the model forbid that case |
| C6 | Pre-emption: `death` beats all; `hit` does not interrupt a cast past release | D2 also: hit recovery does **not** interrupt Whirlwind after its first attack (tick 4). Casts hit before the action tick do not fire (`interrupt=1`) | Add "no `hit` during `whirlwind` after the first attack" to the port's pre-emption rules |
| C7 | WW travel speed is model data | D2 WW travels at **walk** velocity (6) plus movement modifiers, not run | Tell the model owner: walk-speed base for WW |
| C8 | Loadout `weapsel=2` | Skills.txt row 151 `weapsel=2` | Confirmed |

**Source-vs-source conflicts, and which I trust:**
- **WW breakpoints:** Arreat vs Basin/D2MOO. I trust Basin/D2MOO (§ 3.6).
- **`UseAttackRate`:** the d2mods KB calls it "unknown, no effect". D2MOO shows it gates IAS on S1–S4/SQ modes. I trust D2MOO. Its absence on row 151 is why IAS does not speed the spin.
- **CharStats `#spell` = 22 for the Barbarian:** a `#` comment column the game ignores, against AnimData SC 14. I trust AnimData; Maxroll's "casting base 14" agrees.
- **Walk/run playback rate:** AnimData speed field vs D2MOO hard-coded bases. Unresolved (Q3).
- **Meteor fire duration:** code vs Basin differ by 1 tick (Q5).

---

## 6. Open questions

| # | Question | What would settle it |
|---|---|---|
| Q1 | The kit record pins only "Grief Phase Blade" for the sword; **the off-hand axe base and both weapons' IAS are not pinned**. WW D for each hand, and the dual-wield WSM, depend on them | Matt or the conductor pins the two bases and their IAS |
| Q2 | **The WW facing-rotation rate (spin speed) is UNKNOWN.** It is client-side (cltdofunc 45), and the sequence carries no direction offsets | Frame-step an LoD WW capture, or decompile D2Client's cltdofunc 45 |
| Q3 | **The walk/run animation playback rate is CONTESTED.** The AnimData speed fields (Barbarian 168/216, Sorceress 256/256) disagree with D2MOO's hard-coded player bases of 213 (walk) and 101 (run) in an inlined reconstruction | Decode `animdata.d2` and measure a capture. Or the port uses a stride-locked rate (contract § 6.3 already reports foot-slide) |
| Q4 | Which hand's weapon drives D when the two weapons differ. Basin says "needs clarification"; D2MOO uses a "current weapon" helper (`sub_6FC7C7B0`) I did not read | Read `sub_6FC7C7B0` in D2MOO |
| Q5 | Meteor fire field: the code assigns `30+15·(slvl−1)` ticks; Basin says `14+15·slvl` | Frame-step a capture |
| Q6 | **Version:** this packet is LoD 1.13. D2R 2.4.3 changes the WW cadence law (§ 3.6) and makes cooldowns local | Conductor confirms LoD 1.13 as the law for JOIN-1. The charter pins the 1.13 data, so I assumed yes |
| Q7 | Which gear values (IAS, WSM, FCR, FHR, FBR, FRW) the JOIN model assumes for each kit. The kit records carry no stat values, and every duration above is a function of them | Model owner / conductor |
| Q8 | Whether a dual-wield normal Attack alternates A1 and A2 | Only matters if the C5 `attack` state is added. Settle in D2MOO or with a capture |

---

## 7. Source list (accessed 2026-09-30)

**Primary**
- D2 1.13 `Skills.txt`, `Missiles.txt`, `CharStats.txt`, `Weapons.txt`, from `fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9`. Local copy at `agentic_orchestration/research/datamine-acquisition/d2/raw/` (MANIFEST + ACQUISITION-LOG-2026-07-21).
- AnimData.d2 dump on the Basin Wiki "Animation" page: https://d2.lc/AB/wiki/index2a2a.html?title=Animation (mirror of theamazonbasin.com). This is a community-decoded dump, named and cross-checked as described in § 1.
- D2MOO, reverse-engineered D2 1.10f DLLs with many symbols mapped to 1.13c: https://github.com/ThePhrozenKeep/D2MOO @ `5596f5cb`. Files read: `SequenceTbls.cpp`, `SkillBar.cpp`, `Items.cpp`, `Units.cpp`, `Skills.cpp`, `MissMode.cpp`.
- Blizzard D2R 2.4.3 Whirlwind patch note, as quoted at https://us.forums.blizzard.com/en/d2r/t/how-is-whirlwind-speed-calculated-now/147656

**Secondary**
- Basin Wiki: Attack speed (`?title=Attack_speed`), Whirlwind, Sorceress, Barbarian_(Diablo_II), Cast_rate, Meteor, Fire_Ball, Battle_Orders, Walk/run speed — all at https://www.theamazonbasin.com/wiki/index.php
- Maxroll, Teo1904, "Diablo 2 Resurrected Breakpoints & Animations" (updated to 2.4): https://maxroll.gg/d2/resources/breakpoints-animations
- The Arreat Summit: Barbarian Combat Skills (https://classic.battle.net/diablo2exp/skills/barbarian-combatskills.shtml) and Sorceress Fire Spells (https://classic.battle.net/diablo2exp/skills/sorceress-fire.shtml)
- Phrozen Keep: "WhirlWind Attack Speed" 1.09b analysis (https://d2mods.info/forum/viewtopic.php?t=12561); Skills.txt KB (https://d2mods.info/forum/kb/viewarticle?a=440); Calculating Missile Distance KB (https://d2mods.info/forum/kb/viewarticle?a=463)

**Project inputs (read-only):**
- `reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md`
- the JOIN-1 charter rows J-S3 and J-S3b
- `research/curated/kits-export/d2-ww-barb.json` and `d2-fire-sorc.json`. No separate meteor-sorc record exists. `d2-meteorb.json` is a different kit (Meteor + Frozen Orb), so it was not used.
