# KC2-PM2 Lap A — player defense/sustain sheet extraction

**Seat:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-12-kc2-pm2-run-charter.md`, Cell "Lap A"
**Fork ruling governing this cell:** F-1 (KC2-PM1 ledger § E-1) — screenshots PRIMARY, `player.gdc` CROSS-CHECK, disagreement resolves toward the screenshots.
**Date:** 2026-08-12 · **Status:** LANDED, with two named gaps (§ 6) — neither is HALT-worthy.

## 1. Headline

The 117-frame corpus is **not** a gameplay dump — it is a deliberate build-documentation
sweep, and it contains the full character sheet. Both sheet pages were recovered; nothing
had to be substituted from community builds.

| quantity | value | frame |
|---|---|---|
| Health | **20,005** | 495, 508 |
| Offensive / Defensive Ability | **3,259 / 2,591** | 495, 508 |
| Armor Rating | **3,557** | 495, 508 |
| Resistances | **80 / 80 / 80 / 80 / 80** (fire, cold, lightning, acid, pierce) · **85 / 80 / 80 / 80** (bleed, vitality, aether, chaos) · **16** (physical) | 495, 508 |
| Life Steal (ADCtH) | **21 %** | 513 |
| Health regeneration | **129.38 /s** | 511 |
| Block / Dodge / Deflect | **0 % / 0 % / 0 %** | 519 |

Two findings the fight cell should not miss:

1. **This build has no avoidance layer at all.** Chance to Block 0 %, Dodge Chance 0 %,
   Deflect Chance 0 % (frame 519). Every incoming melee/ranged attack that passes the
   OA-vs-DA roll connects. Whatever F-4 models as "dodging" is therefore **purely
   positional** — it cannot borrow a sheet-level avoidance term, because there isn't one.
2. **Life Leech Resist is −25 %** (frame 519). Enemy life-leech is *amplified* against this
   player. If the threat decode (Lap B) surfaces leech-bearing attack slots, the sign
   matters.

## 2. Method

**Sources, read-only.**

* `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/screenshots/` — 117 PNGs,
  `Screenshot (495).png` … `Screenshot (611).png`, contiguous, 1920×1080.
* Pristine save zip, re-downloaded 2026-08-12 from the forum URL preserved at
  `/Volumes/reincarnated/agent-prompts/2026-08-01-eor-warlord-playtest-directions-v3.md` § R-V3-2.

| artifact | sha256 |
|---|---|
| `gdc/pristine-save.zip` | `13756973c7a089b0c09c035a28dac98fd8448144873a42c88c68f35f91ff6a4f` |
| `gdc/_EoRWarlGuts/player.gdc` | `c8738da31f494462637fbc79189f4adb9d522cd21d30c315388d6e6e8b587e0d` |

**Screenshot pass.** The Read tool downsamples any image to roughly 600 px on its long
edge, which destroys 1920×1080 UI text. Two purpose-built helpers were written to defeat
that (they live in `agentic_orchestration/research/scripts/`, and are reusable by any later
lap that needs to read a screenshot corpus):

* `kc2_pm2_lap_a_contact_sheet.py` — 4×4 contact sheets across the whole corpus, for
  cheap UI-state triage.
* `kc2_pm2_lap_a_crop.py` — crop a named full-resolution region and upscale it. A crop
  ~330 px wide survives the downsample at ~1.8× effective magnification, which is the
  legibility floor for GD's sheet font.
* `kc2_pm2_lap_a_region_strip.py` — tile the *same* screen region across a frame range, to
  spot which frame a UI state changes on.

**Save pass.** `agentic_orchestration/research/scripts/gd_gdc_parse.py` — written from
scratch. GDStash / gd-edit were consulted as prose reference for field *order* only; no
third-party code was used.

The load-bearing discovery: **this save is plaintext.** GD's `.gdc` stream cipher derives
its key table from `seed ^ 0x55555555`, where `seed` is the leading `uint32`. This file's
seed *is* `0x55555555`, so the key is 0, the whole table is 0, and the XOR stream is the
identity. No decryption layer was needed. (A save with any other seed would need the real
key schedule — see cliff C-3.)

## 3. Screenshot index — which frames carry which UI

| frames | count | content |
|---|---|---|
| 495–510 | 16 | **Character sheet page I** + inventory. Attributes, vitals, combat stats, resistance grid. |
| 495 | 1 | Equipped-weapon tooltip: **Gutsmasher** (full affix list, granted skill, component, augment, requirements). |
| 500–507 | 8 | Equipped-item tooltips (head, neck, chest, shoulders, rings, medal, relic class). Titles legible; per-item affix transcription NOT performed — the aggregate sheet supersedes it for the sim, and every item is independently identified by DBR record from the save (§ 5). |
| 511–522 | 12 | **Character sheet page II**, scrolled top-to-bottom. Sections in order: Damage Per Hit · Character · Skill bonuses · Physical · Magical · Pet Bonuses · **Defense** · Retaliation · Stats. |
| 523–552 | 30 | Mastery / skill-tree windows (Soldier + Oathkeeper) with per-skill tooltips. |
| 553–610 | 58 | Devotion constellation map with per-constellation tooltips. |
| 611 | 1 | In-world frame with an open panel (not a sheet page). |

No frame anywhere in the corpus hovers the `Armor Rating (?)` marker or any individual
resistance icon — that is the origin of both gaps in § 6.

## 4. Measured sheet

Full machine-readable table: **`measured-player-sheet.csv`** (186 rows; columns
`stat, value, unit, source_screenshot_or_gdc, notes`). Every row cites its frame. This CSV
is the artifact gamora's fight cell consumes.

Structure of the CSV, by section:

* identity / level / experience
* attributes, vitals (Physique 914 · Cunning 1219 · Spirit 398 · Health 20,005 · Energy 2,576)
* combat stats (OA 3,259 · DA 2,591 · sheet-DPS 20,233 · Armor 3,557)
* the 10-entry resistance grid
* character block (attacks/s 2.66 · attack speed 196 % · crit damage +57 % · **run speed
  135 %** · healing increase +22 % · **health regen 129.38/s** · energy regen 75.37 ·
  energy absorption 20 % · constitution bonus +53 %)
* skill-rank bonuses (+1 all · +3 Soldier · +2 Occultist · +1 Necromancer · 0 elsewhere,
  including 0 Oathkeeper)
* physical / magical damage blocks, including **Life Steal 21 %**
* pet bonuses (relevant only if F-6(a) fires — the single summon is Celestial Guardian)
* **defense block** (block/dodge/deflect all 0; stun 79 · disruption 30 · life-leech −25 ·
  energy-leech 0 · trap 76 · petrify 34 · freeze 80 · slow 69 · reflect 26)
* retaliation (physical 1,008 flat, +371 % modifier; all other types 0 flat)
* lifetime stats (avg ilvl 92 · 6:21:16 played · 162,091 kills · 24,211 boss/hero · 603 deaths)
* weapon + Eye of Reckoning detail

### Notes for the fight cell

* **Sustain (F-3) inputs are complete:** leech = Life Steal 21 % (rides damage-dealt rows,
  per the F-3(a) ruling) and regen = 129.38 hp/s. Healing Increase +22 % and Constitution
  Bonus +53 % are *also* on the sheet if the cell chooses to model potion/heal effects;
  the charter does not require them.
* **Armor absorption is a declared gap, not a measured value.** GD's stock absorption is
  70 %, but that number is *not* in this corpus. If the damage math needs it, the cell must
  declare the assumption on the wire rather than sourcing it here (GL-12).
* **The player attack is unchanged for PM-2** per charter, but the Eye of Reckoning
  numbers are recorded anyway: base rank 15 (+12 in the modifier), sheet damage-per-hit
  43,691–59,761, and Gutsmasher grants +4 ranks plus 100 % fire→physical conversion on it.

## 5. `player.gdc` cross-check

**Parsed cleanly** (all 15 blocks walked, every block's zero end-marker validated):

| field | gdc | sheet | verdict |
|---|---|---|---|
| name | `EoRWarlGuts` | `EoRWarlGuts` | AGREE |
| class tag | `tagSkillClassName0109` → 01 Soldier + 09 Oathkeeper | "Warlord" | AGREE |
| level | 100 | 100 | AGREE |
| experience | 28,475,316 | — | sheet does not show |
| devotion | 55 spent / 0 unspent | — | 55/55 = maximum |
| unspent skill + attribute points | 0 / 0 | — | fully allocated |
| Soldier mastery | rank 46 | — | block 8 |
| Oathkeeper mastery | rank 50 | — | block 8 |

**Skill + devotion allocation** (block 8, 318 entries declared, 318 parsed, zero desync).
83 non-default entries at rank > 0. Soldier: `_classtraining` 46, `passive1` 6, `passive3` 8,
`fieldcommand1/2` 10/8, `warcry1/2` 12/12, `blitz1/2` 1/1, `willtolive1` 1,
`fightingspirit1` 1, `passive2/4` 1/1. Oathkeeper: `_classtraining` 50, `eyeofreckoning1/2`
15/12, `divinemandate1` 12, `presenceofvirtue1/2/3` 12/9/10, `summon_celestialguardian1` 1
+ `_petmodifier` 12, `ascension1/2` 1/1, `viremight1/2/3` 1/1/1, `passive02` 2. Devotion:
55 star-nodes across constellations `tier1_08 / tier1_29 / tier1_38 / tier1_39 / tier1_42 /
tier2_02 / tier2_05 / tier2_17 / tier2_21 / tier2_37 / tier3_20`, with six bound proc
skills (`*_skill.dbr` entries carrying devotion levels 15–25).

**Equipped gear** (recovered from the tail of block 3, where the equipment array sits;
slot assignment is by GD's standard equipment order and is an inference, the *records*
are read directly):

| slot | base record | component | augment |
|---|---|---|---|
| head | `upgraded/gearhead/d028_head` | `compb_arcanediamond` | `c203a_enchant` |
| neck | `gearaccessories/necklaces/b201e_necklace` | `compb_sealannihilation` | `b130a_enchant` |
| chest | `upgraded/geartorso/d026_torso` | `compb_chainsofoleron` | `c104a_enchant` |
| legs | `gearlegs/b002e_legs` | `compb_ancientarmorplate` | `c06a_enchant` |
| feet | `upgraded/gearfeet/d007_feet` | `compa_spellscorchedplating` | `c14a_enchant` |
| hands | `gearhands/d206_hands` | `compa_restlessremains` | `c14a_enchant` |
| ring 1 | `gearaccessories/rings/d110_ring` | `compa_runeboundtopaz` | `b126a_enchant` |
| ring 2 | `gearaccessories/rings/b103e_ring` | `compa_bloodiedcrystal` | `b130a_enchant` |
| waist | `gearaccessories/waist/d108_waist` | `compa_spellscorchedplating` | `c203a_enchant` |
| shoulders | `upgraded/gearshoulders/d026_shoulder` | `compb_livingarmor` | `c203a_enchant` |
| medal | `gearaccessories/medals/b016e_medal` | `compb_arcanespark` | `enchants/runes/d203_rune` |
| relic | `gearrelic/d114_relic` | — | completion bonus `ao17a_oa` |
| weapon (2H) | `gearweapons/melee2h/d107_blunt2h` | `compa_sealmight` | `b06a_enchant` |

**The weapon slot is an exact three-way match** with the screenshot: `d107_blunt2h` =
Gutsmasher (Legendary Two-Handed Mace), `compa_sealmight` = "Seal of Might" component,
`b06a_enchant` = "Potent Oleron's Fervor" (Black Legion augment). This is strong evidence
that the pristine save and the played character are the *same build*, which in turn makes
the one discrepancy below worth flagging rather than shrugging off.

### Discrepancy table

Total discrepancies: **3** (one cluster, one semantic, one absence). Resolution is toward
the screenshots in every case, per F-1.

| # | quantity | screenshot (PRIMARY) | gdc | resolution | note |
|---|---|---|---|---|---|
| D-1 | Physique / Cunning / Spirit | 914 / 1219 / 398 | 74.0 / 858.0 / 74.0 | **use the screenshot values** | All three gdc floats fit `50 + 8k` exactly (k = 3, 101, 3 → 107 attribute points, consistent with `attribute_points_unspent = 0` at level 100). That is the signature of a *base-allocation-only* record, i.e. gear/skill/devotion contributions excluded. It does **not** explain the ordering: taking the block's field order at face value gives Physique 74 → 914 (+840 from gear) but Cunning 858 → 1219 (+361), and a 101-point Cunning dump is an odd read for a build whose weapon requires Physique 592. Either the field order is not `physique, cunning, spirit`, or the stored value excludes something large. **Field-order mapping is marked UNCERTAIN in the CSV.** The sim is unaffected: it consumes the sheet totals. |
| D-2 | Health / Energy | 20,005 / 2,576 | 1142.0 / 298.0 | **use the screenshot values** | Same block, same float run. Neither gdc value is a plausible level-100 total nor the current pool at save time (the sheet shows 1594/2576 energy). Semantics UNCERTAIN — recorded raw, not interpreted. |
| D-3 | Armor absorption, resistance overcaps | absent | absent | **neither source has it** | Not a disagreement — a shared gap. See § 6. |

No other conflict was found. Level, name, class, mastery ranks, devotion count and the
entire weapon slot agree across both sources.

## 6. Gaps and cliffs (GL-12 — documented, never guessed)

**G-1 — Armor absorption %.** NOT CAPTURED. GD shows this only in the `Armor Rating (?)`
hover tooltip, and no frame in the 117-frame corpus hovers it. GD's stock value is 70 %,
but that is genre knowledge, not a measurement of *this* character, so it is recorded as
`GAP` in the CSV. **The fight cell must declare whatever absorption it uses on the wire.**

**G-2 — Resistance caps / overcaps.** NOT CAPTURED, same cause (per-resistance tooltips
never hovered). All ten resistances are measured at their *effective* value; nine of the
ten sit at or above the stock 80 % cap (bleed reads 85 %, which means the build carries at
least one max-resist source), so the effective numbers are what a damage calculation
wants. Overcap headroom against enemy resist-reduction is unmeasurable from this corpus.
If Lap B surfaces RR-bearing attack slots, this becomes a live limitation and should be
re-raised rather than estimated.

**C-3 — The parser handles only the plaintext (`seed == 0x55555555`) case.** This save is
plaintext, so the cliff never bit. Any other GD save would need the real CRC-style key
schedule implemented. Cost is low; it was simply not needed and was therefore not written.

**C-4 — The inventory block's bag structure was not decoded.** Block 3's per-bag header
did not yield to a first-pass field walk. The equipment array at the block's tail *was*
recovered by length-prefixed record scanning (§ 5), which is what the cross-check needed.
Full bag/stash inventory decoding is unattempted and out of Lap-A scope.

**C-5 — Item affix → stat attribution was not decomposed.** The sheet gives aggregates
(e.g. Life Steal 21 %); which item, skill or devotion contributes which share is not
established. The sim consumes aggregates, so this was not pursued. Frames 500–507 hold the
per-item tooltips if a later lap needs the decomposition.

**C-6 — Devotion constellation *names* not resolved.** Block 8 gives raw devotion DBR ids
(`tier2_37a` etc.); mapping them to constellation names needs the `.arz` lookup, which is
Lap B's substrate. The 55/55 count and the six bound procs are established regardless.

## 7. Files

* `README.md` — this note
* `measured-player-sheet.csv` — **the deliverable gamora consumes** (186 rows)
* `gdc/pristine-save.zip`, `gdc/_EoRWarlGuts/player.gdc` — downloaded source + extracted save
* `work/gdc-parse.json` — full parser output
* `work/contact/` — 8 corpus contact sheets
* `work/crops/`, `work/strips/` — the evidence crops behind every transcribed value
* scripts (in `agentic_orchestration/research/scripts/`): `gd_gdc_parse.py`,
  `kc2_pm2_lap_a_contact_sheet.py`, `kc2_pm2_lap_a_crop.py`, `kc2_pm2_lap_a_region_strip.py`

---

*Filed by legolas (UNKNOWN-RESEARCHER), 2026-08-12, under the KC2-PM2 charter, Lap A.
Read-only on `/Volumes/reincarnated/` and on the forum source. No engine-repo writes.*
