# Research: KC2 footage reads, the referent's own line-up, mutators, p05 emergence, a stationary calibration, and nameplate stacking (2026-10-02)

**Mode:** A (analytical; primary-source footage reads)
**Commissioner:** gandalf (RUN-CONDUCTOR), for Matt's Q101 ("recover your line-up first", KP-216). **Agent:** legolas (UNKNOWN-RESEARCHER).
**Posture:** read-only on the Pi share. One byte-exact local copy was taken to the scratchpad for frame work and deleted afterwards. No pack, oracle, port or vendor file was touched.
**Labels:**
- **FOOTAGE**: read from the referent recording.
- **DATAMINED**: from GD's shipped data. This covers the Ed IV/II `.arz`, the Ed-I Lua, and the Lap D eHP chain.
- **PACK/SIM**: the oracle's own code and data.
- **INFERRED**: my reasoning.
- **UNKNOWN**: not established.

---

## 0. File of record: VERIFIED

| | value |
|---|---|
| path | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` |
| size | **479,438,089 B**, which matches Lap Q PREREGISTRATION, Lap R `pm4r_findings.md` and galadriel's notes |
| sha256 | **`4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8`**, an EXACT match to the Lap Q pin (`…/2026-08-14-kc2-pm4-lap-q-heal-discriminator/PREREGISTRATION.md`) and the Lap H-2 re-verification (`…/lap-h2-video-match/README.md`) |
| stream | h264 1920×1080, 60/1 fps, 1034.10 s, 62,046 frames (ffprobe) |

**Instrument note.** The first in-place `shasum -a 256` over smbfs returned a different digest, `bc1efbcc…ce60`, with an implausible 0.03 s of user CPU. Three later reads all gave the pin exactly:
- `openssl dgst` in place on the share;
- `openssl` on the local copy;
- `shasum` on the local copy.

The outlier was a read artefact, not a different file. **Hash smbfs files with `openssl`, or hash a local copy. Do not trust a single `shasum` over the share.**

The KC2 pack `provenance.json` files do not pin the MP4. They pin data files only, so the Lap Q/H-2 pins are the binding reference.

---

## Summary

1. **The referent's line-up is recovered for all ten waves:** 84 identities, each one tied to a max-HP fingerprint. The plates show `(cur/max)`, and every record's max HP at a given level is exact from the Lap D chain. **105 of the 118 recurring fingerprints (3 or more readouts) reproduce exactly; 13 do not.** 53 hovered nameplates were eye-read and bound to their records.
   - **The referent is a legal draw from the spawn pools.** Every resolved body is pool-legal at its wave and point, and each point's bodies come from a single pool alternative.
   - **It differs from seed 9 at roughly half the spawn points.** The biggest differences are exactly where the oracle spiked:
     - **w152:** p03 is basilisk trash, not thornedhorror-frost (the source of 47 % of seed-9 w152 intake), and p04 is Haraxis, not Carraxus.
     - **w158:** p01 is sandlizards, not devourers. p02 has different heroes: Everon (`skeleton_h04`) and Flamegore (`skeletalgolem_h03`) instead of `skeleton_h08`/`h09`, which carried 66 % of seed-9 w158 intake.
     - **w156:** p04 is statues, not heralds (29 %), and p03 is Larria, not the Kurn shaman (24 %).
     - **w151:** wraiths, not ghosts (ghosts carried 51 %), and wraith heroes, not wendigo heroes.
   - Summoned bodies are counted separately (17 summon identities).
2. **The six mutators** are, from left to right: **Brutal, Leeching, Cruel, Corrupted** (monsters) and **Resilient, Ascended** (player). Identification is HIGH: every icon matches GD's icon for that mutator, and the DATAMINED selection law says checkpoint 150 gives tier 15, which gives 6 mutators split 4 monster / 2 player, active for all of waves 151–160. The Ultimate effects are in `mutators.json`.
3. **p05 emergence is confirmed near the centre** (w151, w153, w157). Matt's "no plate or bar while emerging" is **not supported for the in-world plate**: the bar and `(cur/max)` text appear on the first spawn frame (+3.83 to +3.93 s on the badge clock), and a golem took damage 0.7 s into its 3.567 s clip. Hover and selection are UNTESTED.
4. **Stationary calibration:** the Carnivorous Plant never moves. Tracked by its own fingerprint at 60 fps through the referent's pipeline, it reads **still only 0.98 / 0.65 / 0.37 / 0.28**, and the still fraction falls as camera travel rises. The plate moves **1.27× (x) and 1.29× (y) the camera-trace displacement** on the cleanest track. **A stationary body reads as moving when Matt moves.** This bears directly on KP-221's referent 0.26.
5. **Nameplate stacking: NOT FOUND.** GD lets plates overlap; no offset rule is visible. The vertical jumps are better explained by false-positive bars in VFX (seen in frames) and re-linking.

---

## 1. Read 1: the referent line-up per wave

### 1.1 Instrument (FOOTAGE + DATAMINED)

- **Census.** 10 Hz over 682.0–866.0 s (1,840 frames), plus 30 Hz and 60 Hz in targeted windows.
  - Text location: galadriel's `eor_hptext` blob rules, re-implemented with scipy.
  - OCR: galadriel's eye-verified glyph atlas (`board-closure/work/atlas.npz`), with the comma-grouping parse check.
  - Allegiance: the colour of the bar under the text. Red is hostile; green is the player or allies (e.g. the player's 20,005 and 16,368).
  - 5,000+ parsed readouts in all.
- **Fingerprint → record.** `eHP(w, L) = floor(base_life(L) × (1 + (580 + G[w] + passive(L))/100))` over Lap D's 1,812 (record, level) rows (`pm4d_band_b_life_by_level.csv`), reproduced to 0 mismatches against `ehp_w151`. Matches are filtered to records legal in that wave's pools, including p06, from `wave_engine.pools_for`, and to summons whose owner is legal.
- **Count.**
  - `count_min` = the most bodies of that fingerprint seen in one frame, summed over levels. A record seen at two levels means at least two bodies.
  - **Validated on w160**, where all six of galadriel's MEASURED counts (2/1/1/2/3/1) are reproduced exactly.
  - `count_tracker_upper` comes from a world-frame tracker. **It over-counts** (w160 Kubacabra: 4 against the true 1), so read it only as a ceiling.
- **Names.** 53 hovered top-centre nameplates were eye-read (name, rank colour, level, family), each bound to a record by display name, level and an HP fingerprint present in the census. See `hover_nameplate_reads.json`.
- **Closure caveat** (galadriel, carried over): bodies never engaged on screen leave no readout. The counts are **lower bounds**, and the census is closed only for engaged, on-screen bodies.

### 1.2 Per-wave line-up: referent against seed 9

"Alt" means the pool alternative a spawn point rolled. Seed 9 is `roll_wave(w, Random(engine_seed(9,w)), …, bonus_spawns_enabled=False, RosterFold())`, the oracle's first draw (`seed9_lineup.json`). It reproduces the KP-211/215 descriptions. Every referent body here is pool-legal. All rows and confidence labels are in `referent_lineup_by_wave.csv`.

| wave | point | referent (FOOTAGE+DATAMINED) | seed 9 (PACK) | same? |
|---|---|---|---|---|
| 151 | p01+p04 | wraith_t3 at **both** points: Wraith, Spiteful, Ancient (≥10 bodies over 3 levels, so both points; one point maxes at 7) | ghost_t3 at both points (17) | **DIFF** |
| 151 | p02 | **wraith heroes**: Tildoom ~ Timewarped and Arcanom the Soulthief (both named), plus perhaps a third | wendigo heroes h01×2, h04 | **DIFF** |
| 151 | p03 | swampgolem hero alternative (L107/L108 class; plant summons prove a golem-hero owner) | swampgolem h01/h02/h05 | same alt |
| 151 | p05 | Carnivorous Plant ≥4 (L103, L104); **no swampgolem_a01 fingerprint** | 2 plants + 2 golems | partly |
| 152 | p01 | crab heroes (crabling summons prove it; swamp or springs is unresolved) | springscrab heroes | same or diff |
| 152 | p02 | basilisk heroes: Chillslither ~ Arctic (h05) and Rotmouth (h02), both named | basilisk h01/h02/h03 | same alt |
| 152 | p03 | **basilisk_t3**: Juvenile, Venomgaze, Stonegaze (≥7) | **thornedhorrorfrost_t3** (7) | **DIFF (largest)** |
| 152 | p04 | **Fleshweaver Haraxis** (named, boss) | **Carraxus** (swampcrab_ugdenbog_01) | **DIFF** |
| 152 | p05 | corruption heroes; galadriel read Vanallius (h02) | h01/h02/h05 | same pool |
| 153 | p01 | wendigo_t3: Wendigo, Flayer/Marroweater, Ancient | wendigo_t3 | same alt |
| 153 | p02/p04 | bounties: Chthonian Unraveler (kc_bounty13, named), dc_bounty08 or ku_bounty_06, kc_bounty09 or ro_bounty12, +1 | cu_bounty08/04/07; ro_bounty11/19, odv_bounty07 | members differ |
| 153 | p03 | **skeletonrevenant_t3**: Frost Revenant (named) and siblings, Death Revenant; Skeletal Archer summons | **giant_t3** | **DIFF** |
| 153 | p05 | plants and Ugdenbog Golems (≥3 golems) | 3 plants + 2 golems | same |
| 154 | p01 | **Father Kymon** (named) | Bloodlord (cultist_cultleader_01) | **DIFF** |
| 154 | p02 / p03 | Gabal'Thunn / Kubacabra (both named) | same | same |
| 154 | p04 | **wendigocannibal_t3**: Wretch, Turned (named) | **eldritcharmor_fire_t3** (firebreath, 25 %) | **DIFF** |
| 155 | p01 / p02 | Dralgar / Allostria (named) | same | same |
| 155 | p03/p04 | **eldritchwraith_t3** (Eldritch Spirit, ~Haunt and ~Ancient named) + corruption_poison (Fleshwarped Aberration named) | aetherialimp_t3 + corruption_poison | one point **DIFF** |
| 156 | p01 | Janaxia (named, L107) | Janaxia | same |
| 156 | p02 + p03 | two L108 bodies of the boss class: (Stone Basilisk or Siff) + **Larria** | Siff + **Kurn shaman** (chaosorb, 24 %) | p03 **DIFF** |
| 156 | p04 | **statue_t3**: Animated Keeper and Watcher (named) | **chthonianherald_t3** (heralds, 29 %) | **DIFF** |
| 156 | p05 | Fleshwarped Chilled One (ice; named) | ice ×7 | same |
| 157 | p01 | Blugrug (named) | Blugrug | same |
| 157 | p02 | devotion_heroes01 #2: Starhorn ~ Celestial (rhino_h02), Arum'Zoth ~ Burning (chthonianherald_h02) | same alt: herald_h01, rhino_h04, rhino_h01 | same alt, members differ |
| 157 | p03 | **chthonianservitor_t3**: Servitor, Harvester, Bloodkeeper (named), Drone | **chthonianleech_t3** | **DIFF** |
| 157 | p04 | **yetidire_t3**: Diremane Brute (named), Rager/Icebreaker, Alpha | **skeletalgolem_t3** | **DIFF** |
| 157 | p05 | **imp heroes**: Phigillius Stormbile (named) + 2 | corruption heroes | **DIFF** |
| 158 | p01 | **sandlizard_t3**: Sandclaw, ~Flayer (named), ~Matriarch | **chthoniandevourer_t3** (12) | **DIFF** |
| 158 | p02 | devotion_heroes04: **Everon ~ Burning (skeleton_h04)**, **Flamegore ~ Burning (skeletalgolem_h03)** (both named) | same alt: **skeleton_h06/h08/h09** (h08+h09 = 66 %) | same alt, **members differ** |
| 158 | p03/p04 | devourer_t3 (Gorger named) + swampcrab_t3 (Ugdenbog Crab named) | volcanic sandlizard + swampcrab | one point **DIFF** |
| 158 | p05 | wraith or hypporaven heroes (shared HP class; unresolved) | hypporaven h01×2, h03 | ? |
| 159 | p01 | Lunal'Valgoth (MEDIUM: shares the HP class and his Drone summons are present) | Lunal'Valgoth | same |
| 159 | p02 | **Venarius, the Backbreaker** (named) | Avinnia (rokwind_01) | **DIFF** |
| 159 | p03 | The Sentinel (named) | Sentinel | same |
| 159 | p04 | **Margul the Rotting** (named) + Korvan Maggot summons | Rimehorn | **DIFF** |
| 159 | p05 | **Ekket'Zul** (named) | **Okaloth, the Messenger** (40 %) | **DIFF** |
| 160 | p01 | **Zantarin** (named) | Kymon nemesis | **DIFF** |
| 160 | p02 | **Kubacabra** (named) | nemesis_wendigo_01 | **DIFF** |
| 160 | p03 | Archmage Aleksander (named) | same | same |
| 160 | p04 | **Galakros** (named) | The Steward | **DIFF** |

Percentages are each seed-9 record's share of seed-9 intake in that wave (KP-211 residual hunt, `perwave_residual.json`).

**Absence check (FOOTAGE).** Seed-9 records whose HP is distinctive were looked for at every level, with any number of readouts. **Zero readouts** for:
- ghosts a01–b04 (w151);
- swampgolem_a01 (w151);
- Carraxus;
- thornedhorrorfrost a01/b01/c01;
- giants and grobles;
- Bloodlord;
- eldritcharmor a/b/c;
- imps a01/b01;
- heralds and wretches;
- the Kurn shaman;
- chthonian leeches;
- skeletalgolem_b01;
- skeleton knight;
- revenants c01/c03 at w157.

Hero and boss classes share HP across records, so they can only be confirmed by name.

**Bodies, lower bound** (pool / summoned) against seed 9's roster:

| | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|
| pool bodies | ≥19 / 2 | ≥14 / 7 | ≥22 / 4 | ≥11 / 0 | ≥14 / 0 | ≥15 / 2 | ≥20 / 2 | ≥25 / 4 | ≥4 / 5 | ≥4 / 7 |
| seed 9 roster | 28 | 17 | 24 | 11 | 17 | 17 | 21 | 33 | 5 | 4 |

**Summoned monsters (red plates, spawned by a monster; FOOTAGE+DATAMINED):**

| wave | summon | owner |
|---|---|---|
| 151 | summoned Carnivorous Plants | golem heroes |
| 152 | Fleshwarped Aberrations | Haraxis |
| 152 | crablings | p01 crab heroes |
| 153 | Skeletal Archers | Death Revenant / odv_bounty13 |
| 156 | Spiteful Wraiths | Janaxia |
| 157 | aetherial worms | Blugrug |
| 158 | Ugdenbog Crablings | Stoneshell |
| 159 | Korvan Maggots | Margul |
| 159 | Chthonian Drones | Lunal'Valgoth |
| 159 | hellhound_witchgod summon | owner INFERRED |
| 160 | Aleksander's Shards, Death Revenant, Skeletal Archers | Aleksander / Zantarin |
| 160 | probable Bileeater L112 | galadriel |

**p06 (the bonus point):** no referent body needs p06 to be legal; the w153 638,564 is ambiguous. The referent is consistent with p06 OFF but does not prove it.

**Open, UNKNOWN:**
- **w155, 2,061,902:** a boss-class L108 body seen for 0.7 s at the wave seam. Its only legal member, Ishtal, cannot co-roll with Allostria at p02.
- **w156, 1,976,276:** a fourth boss-class body at L106, when the three boss points are already accounted for.
- **w153, 447,994** and **w156, 444,150:** no record reproduces them.
- **HP residuals:** Janaxia L107 reads 2,022,317 against the model's 2,018,819 (+0.17 %). Animated Keeper and Watcher read about +1.1 % over Lap D. All are name-bound. **This is a Lap D life-chain residual to route** (probably per-level passive).

**Incidental (FOOTAGE):** the player's HP globe reads **16,368/16,368 from about 714.5 to 718 s** (the w153 onset) and 20,005 otherwise (`evidence/player_globe_maxhp_16368_w153.png`). That is an 18.2 % temporary max-HP drop, cause UNKNOWN. It is the "16,368 green body" galadriel struck in her fifth extraction. The oracle consumes 20,005 as a constant (MO-4).

---

## 2. Read 2: the six-icon mutator row (`mutators.json`)

The row first appears at **682.12 s** with the "New Mutators Active" banner (`evidence/mutator_row_x4.png`). Left to right:

| # | icon (FOOTAGE) | mutator | affects | Ultimate effect (DATAMINED, Ed IV = Ed II) |
|---|---|---|---|---|
| 1 | hand gripping a dagger | **Brutal** | monsters | + flat Pierce (level-indexed array) and **+50 % Pierce damage** |
| 2 | fanged maw | **Leeching** | monsters | `offensiveLifeLeechMin` **600**: 600 % of attack damage returned as health |
| 3 | skull under a crosshair | **Cruel** | monsters | each hit: **−8 % total damage dealt by the target (the player) for 1 s** |
| 4 | magenta split-triangle rune | **Corrupted** | monsters | + flat Chaos and **+50 % Chaos damage** |
| 5 | green flask with a skull | **Resilient** | player | +8 % Poison and Bleed resistance, +8 % max Poison and Bleed resistance |
| 6 | green pentagram | **Ascended** | player | **+8 % total damage**, +4 % retaliation |

**Identification.** Each icon matches, by eye, GD's own icon for that mutator (`ui/hud/mutatoricon_*.tex`, as hosted on the GD wiki). The wiki is a secondary source; its effect text is out of date, so the effects above come from the Ed IV records. The `.tex` itself cannot be read locally because Ed IV ships no UI `.arc`.

**Selection law (DATAMINED, Ed-I `survivalevent.lua`).** `SelectMutators` runs once at event start, and `ResetMutators` runs at event end, so the six hold for waves 151–160. Checkpoint 150 gives `rewardTier` 15, which gives **6 mutators: 2 player + 4 monster**, matching 4 red and 2 green icons.

**Quirk (DATAMINED).** The roll loops accept `rand < listLength`, so **Vengeful (monster #17) and Voidmarked (player #10) can never be chosen.**

**Cross-check (FOOTAGE).** No life-multiplier mutator is active. Toughened (+12 % life) or Regenerating (+6 %) would have shifted every fingerprint, and 105 reproduce exactly.

---

## 3. Read 3: p05 emergence: see `p05_emergence_frames.md`

**Bodies emerge at p05 near the centre** (w151 dust burst and growing plant; w153 flash and debris; w157 teal burst on the central dais). **The in-world bar and `(cur/max)` appear on the first spawn frame at full HP** (+3.83 to +3.93 s on the badge clock), and **the w153 golem took damage 0.7 s into its 3.567 s clip.**

- Matt's "no nameplate or health bar while emerging" is **not supported for the in-world plate**.
- Top-centre hover and cursor selection are **UNTESTED**: no hover landed on an emerging body.
- `v3p8_rows.am6_emergence_presentation` conflicts with the footage for the in-world bar. AM-2/AM-3 (inert but hittable) are corroborated.

---

## 4. Read 4: known-stationary calibration (KP-221 R6; `stationary_calibration.json`)

**Body.** `livingplant_a01` is a `ControllerStationaryMonster`, DATAMINED never to move.

**Identity is certain at every frame,** because the body is tracked by its own fingerprint at 60 fps (census over 692–698 and 719–729.2 s). Positions are camera-compensated exactly as Lap H-2 `d1b.world` does it. Velocity uses the referent rule: a 15-frame boxcar, `np.gradient`, and still below 50 gpx/s, on segments with gaps of 12 frames or fewer.

| window | body | readouts | camera travel (px) | **still fraction** | world residual, median / p90 (gpx) |
|---|---|---|---|---|---|
| 692.0–692.9 | plant L104 (278,543) | 49 | 110 × 108 | **0.976** | 5.2 / 7.9 |
| 692.0–693.3 | plant L103 (272,948) | 59 | 226 × 108 | **0.646** | 7.8 / 27.3 |
| 693.2–698.0 | plant L104 (278,543); one body (HP falls continuously; never two at once) | 167 | 261 × 314 | **0.368** | 34.6 / 72.7 |
| 719.5–722.5 | plant L103 (273,975); two bodies exist, so this track may mix them | 111 | 327 × 298 | **0.279** | 85.5 / 179 |

**Camera gain.** On the clean 167-readout body, the plate's screen displacement regresses on the camera trace at **slope 1.27 (x) and 1.29 (y)**. With the slope free, the residual drops from 34.6 to 11.8 gpx. The second body gives 1.14 / 1.11. **The camera-compensated position of a body that cannot move wanders by tens of gpx as Matt moves, and reads "moving" for up to 63 % of frames.**

**What it means (INFERRED).**
- Lap H-2's R2 check found slope 1.00/1.05 on frame-to-frame steps. **Over seconds, the trace under-reads the plates' motion by roughly 10–25 %**, through trace drift or the plate's height parallax; these two are not separated here.
- At Matt's ≈3 m/s (88 % of the fight), a 20–25 % gain error alone is about 70–90 gpx/s of apparent speed, **above the 50 gpx/s still threshold**.
- **The referent's 0.26 still fraction inside 2.46 m is therefore biased low by an instrument term that KP-221's L3 layer does not emulate.** L3 injects transient anchor residuals, not a camera-gain error correlated with player motion.
- The like-for-like gap (+0.2) may shrink further.

**Recommended:** add a camera-gain layer (×1.1–1.3, applied to player displacement) to `tools/lfl.py` before ruling on standing.

---

## 5. Read 5: nameplate stacking: NOT FOUND (FOOTAGE)

1. **Direct frames.** At 688.6 s, the hero plate `(182,990/442,747)` and the player's plate `(20,005/20,005)` overlap with about a 6–7 px vertical offset, and their text runs into each other (`evidence/plate_overlap_t688.6_x3.png`). At w153 +5.5 s several plates overlap the same way. GD draws overlapping plates on top of each other and does not displace them.
2. **Statistics (4,082 OCR-verified, horizontally overlapping plate pairs).**
   - Vertical separations of 12–32 px are as common as 32–60 px.
   - If GD offset overlapping plates, we would see a pile-up at one plate height (about 28–32 px) and a hole below it. There is neither.
   - Below 12 px the text blobs merge, so the instrument is blind there by construction.
3. **The jumps, re-attributed (INFERRED).** Most small-separation "plate pairs" in the Lap H-2 `plates60` census are **false bars**: red VFX runs that pass the white-text gate on damage numbers. In a random sample of 9 pairs (dx < 20, dy 6–16), 5 were pure VFX or damage-number false bars; the other 4 contained a real plate, but not a stacked pair. Re-linking onto these false bars, plus the camera-gain term in § 4, are the stronger candidates for the 76 %-vertical jumps than any GD stacking rule.

---

## 6. What the oracle needs next (INFERRED; the conductor rules)

1. **Fight the referent's line-up** (Q101). Pin per wave, per point, the alternatives in § 1.2, plus the named records where resolved.
   - Where only a class is known (some hero and bounty members, w158 p05, w152 p01 species), roll within the referent's alternative rather than the full pool.
   - Treat counts as lower bounds; seed-9 count law is acceptable inside the referent's alternatives.
   - Carry the summon list (§ 1.2) as an observed layer.
2. **Fold the six mutators:**
   - Brutal: + flat Pierce and +50 % Pierce on every monster attack;
   - Corrupted: + flat Chaos and +50 % Chaos;
   - Leeching: 600 % of monster attack damage healed;
   - Cruel: player total damage −8 % for 1 s per hit taken;
   - Ascended: player +8 % total damage, +4 % retaliation;
   - Resilient: +8 % / +8 % max on Poison and Bleed.

   The flat arrays are level-indexed and need the array-index law: monster level is INFERRED, not decoded.
3. **Correct `am6_emergence_presentation`:** the in-world bar shows during emergence. Keep AM-2/AM-3.
4. **Standing instrument:** add a camera-gain layer to `lfl.py` (§ 4) before any further standing ruling. No stacking model is needed (§ 5).
5. **Route to the Lap D owner:** the Janaxia L107 and statue HP residuals (+0.17 % and about +1.1 %).
6. **Player max HP:** a transient 16,368 at w153 onset. The cause is UNKNOWN; check before treating 20,005 as constant.

## Knowledge gaps not resolved

- Which members within shared-HP hero and bounty classes are present, where no name was hovered:
  - w151 p02 third hero;
  - w152 p01 crab species;
  - w152 p05 members beyond Vanallius;
  - w153 bounties;
  - w156 p02 Stone Basilisk vs Siff;
  - w158 p05.
- The w155 and w156 extra boss-class bodies and two unmatched values (§ 1.2).
- Whether hover or selection is suppressed while emerging: no hover on an emerging body was found.
- The mutator flat-damage array index (level vs area tier).
- Whether the camera-gain term is trace drift or plate-height parallax (needs a ground-level stationary marker).
- Bodies never engaged on screen are invisible to the census.

## Files

| file | what |
|---|---|
| `referent_lineup_by_wave.csv` | 84 identities: wave, point, record(s), display name, summoner, fingerprints, levels, readouts, `count_min`, tracker ceiling, seed-9 count, identification basis, confidence, label, note |
| `fingerprints_by_wave.json` | every distinct max-HP readout per wave with all legal matches and near misses |
| `hover_nameplate_reads.json` | 53 eye-read hovered plates bound to records and fingerprints |
| `seed9_lineup.json` | the oracle's seed-9 roll per wave and point, with the call used |
| `mutators.json` | the six mutators: icon, record, Ultimate effects, the selection law |
| `p05_emergence_frames.md` | Read 3 |
| `stationary_calibration.json` | Read 4: identity-certain 60 fps results, Lap H-2 `plates60` seeded tracks, camera-gain fits |
| `evidence/*.png` | 8 crops, each under 1 MB: mutator row ×4, p05 sheets (w151/152/153/157), hovered nameplates w155–w158, plate overlap at 688.6, player globe 16,368 |
| `tools/` | `census.py` (plates + OCR + allegiance), `analyse*.py`, `bodies.py`, `names.py`, `assemble.py`, `plates_top.py`, `plantcal*.py`, `p05run.py`. Scratchpad paths are hard-coded; the logic is as described above. |

## Source list (accessed 2026-10-02)

- **Footage:** the referent MP4 above (FOOTAGE; sha256 pinned).
- **Lap D life chain:** `legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp/pm4d_band_b_life_by_level.csv` and `pm4d_band_b_wave_life_modifier.csv`.
- **Lap H-2:** `…/2026-08-13-kc2-pm4-lap-h2-video-match/method/{bars.py, d1b.py, camera_translation_60fps_683-866.npy}`, observables OBS-H2-6/7/8.
- **Lap R:** `…/2026-08-14-kc2-pm4-lap-r-locomotion-contact/method/plates60_lapH2.npy`.
- **galadriel:** `pipeline/eor_hptext.py`, `eor_hpocr.py`; `captures/2026-08-08-kc2-board-closure/work/atlas.npz`; notes `2026-08-08-kc2-{board-closure, third/fourth/fifth-extraction, barhue-cohort-correction, w152-skull-plate}.md`.
- **Roster packet** `legolas/research/2026-10-02-crucible-enemy-roster-packet/roster.json` (display names, summons).
- **Engine (read-only):** `simulation/kc2/wave_engine.py` (`pools_for`, `roll_wave`), `roster.py`, `scripts/gamora_kc2_pm4_i26_spawn_structure_fold_2026_08_16.py` (`CONDUCTOR_SEED`, `engine_seed`, `P06_BONUS_SPAWNS`).
- **Vendor (DATAMINED):** Ed IV `database.arz` `records/game/mutators/*` via `research/2026-10-01-kc2-enemy-range-audit/scripts/gdlib.py`; Ed II for the equality check; Ed-I Lua `legolas/scratch/2026-08-07-u8-tierwave/lua/smmod/game/events/survivalevent.lua`; tags `…/tags_all.json` (`tags_mutators.txt`, `tags_survivalui.txt`).
- **Secondary:** GD wiki "Mutators" page and its icon files ([grimdawn.fandom.com/wiki/Mutators](https://grimdawn.fandom.com/wiki/Mutators); MediaWiki API `parse`/`imageinfo`), used **only** to match icon art. Effects are not taken from it.
- **Charter rows** KP-211–KP-222; prior findings `2026-10-02-kc2-lethality-hunt-residual/`, `…-kc2-standing-instrument-validity/`, `2026-10-01-crucible-ambush-semantics/`.
