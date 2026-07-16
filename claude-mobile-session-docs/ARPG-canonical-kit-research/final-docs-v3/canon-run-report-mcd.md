# Canon Run Report — Minecraft Dungeons (MCD)
# Narrow scope · Tier 2 tail · §9.19.3 spec

**Run date:** 2026-07-16
**Operator:** legolas (Mode B)
**Authority:** Matt wave-3 ratification 2026-07-16 (BEST-ONLY floor, §9.19.5)
**Spec sections governing this run:** §1 (grain laws G3), §9.10 (low-cred quarantine / negative-decay rider), §9.15 (sizing-law precedence), §9.19.3 (MCD run spec + verdict), §9.19.5 (ratification conditions)
**Output:** `canon-corpus-mcd.jsonl` (5 records) — CATALOGUED-ONLY per §9.19.5 law 3

---

## Era verification (POST-CUTOFF LAW)

**Final content stratum confirmed at run:** v1.17 + Fauna Faire (Season 3), released October 19 2022. Development EOL announced September 28 2023. Six paid DLCs all released by July 28 2021 (Echoing Void final DLC). Source: Minecraft Wiki DLC page (minecraft.wiki), Windows Central. **Stable canon — ZERO §9.2 delta obligations.**

**Negative-decay rider status: HEAVY.** MCD is an old console-native community (≥3 years post-EOL). Negative canon has evaporated: wiki documents mechanical limitations ("build performs poorly in scattered arenas", "cannot fire fireworks continuously") but the community no longer maintains a named negative-build discourse. Zero negative records emitted; missing-data treatment per §9.10 applied.

---

## Stage counts

| Stage | Action | Count |
|---|---|---|
| 1 CENSUS | Named archetype candidates from ≥1 source | 12 |
| 1 CENSUS | Candidates with ≥2 independent source attestation | 8 |
| 2 DOSSIER | Candidates reaching 3–5 source dossier threshold | 6 |
| 3 PROJECTION | Candidates entering projection pass | 5 |
| 4 RECONCILIATION | Deduped, lineage assembled | 5 |
| 5 AUDIT | 100% sample (5/5 records, small corpus) | 5 |

**Records emitted: 5**

---

## Floor-rejection list (§9.19.5 law 1 — BEST-ONLY)

The following candidates were REJECTED before or during projection. Each rejection reason is cited against a spec law.

### Rejected — ROLE not LOOP (fails G3 grain law)

**Tank Build** — ≥4 sources name a "tank" archetype (Renegade Armor, Hammer of Gravity, Gong of Weakening). Rejected: tanking is a survivability ROLE, not an item-defined loop. No single item IS the tank loop — Renegade Armor reduces damage (amplifier); Hammer of Gravity knocks back (amplifier); Gong of Weakening debuffs enemies (amplifier). No loop anchor item that generates a distinct mechanical cycle. G3 fails.

**Healer Build** — ≥3 sources name a healer (Mystery Armor, Totem of Regeneration, Radiance enchant). Rejected: healer is a party-support ROLE; the spec's G3 grain requires the item to BE the loop, not to enable a role. In MCD solo play Radiance is a survivability enchantment; the "build" reduces to "put Radiance on your weapon," which is an enchant choice, not a loop. Additionally, multiplayer-support canonicity is GX-16 party-external scaling — outside this run's solo filter.

### Rejected — AMPLIFIER not LOOP ANCHOR (fails G3)

**Melee DPS / Death Cap Mushroom burst** — sources name a fast-melee burst build (Death Cap Mushroom + Gauntlets/Daggers). Rejected: Death Cap Mushroom is a SPEED AMPLIFIER (temporary attack speed buff on activation). The loop is "use melee weapon fast" — the item does not define a distinct mechanical cycle independent of the weapon. The Speed Build record (mcd-speed) subsumes the fast-hit-rate component under the mobility loop anchor (Evocation Robe).

**Radiance sustain melee** (candidate from brief) — sources discuss Radiance enchantment for melee healing. Rejected: Radiance is an enchantment proc (20% chance on-hit to spawn heal zone), not a loop anchor item. No convergent folk name for a "Radiance build" separate from generic fast-melee. The Steam discussion confirms "life drain is a must on Apocalypse Plus" but names it as an ENCHANTMENT CHOICE on any build, not a named archetype.

### Rejected — FOLK NAME fails convergence (§9.19.5 law 1 — "only if multiple independent sources converge on the same named loop")

**Dynamo Melee / Shadow Anchor** — the wiki's "Shadow Anchor" and "Jumpslash" variants are mechanically rich but the folk name does NOT converge across ≥2 independent non-wiki sources. Gamewith references Dynamo builds but in the context of ranged torment, not as named melee archetypes. The ranged Dynamo-Torment variant absorbed the Dynamo folk name across two sources (wiki + gamewith) and was admitted; the melee variants remain wiki-only and are rejected under the BEST-ONLY floor.

**Bee Build / Busy Bee** — gamewith names a "Creeping Winter Bee Build" (Busy Bee enchantment + Buzzy Nest artifact). Single source; DLC-specific; zero attestation elsewhere. Rejected.

**Boss Fighter (Heartstealer leech)** — gamewith names a "Boss Fight Build" (Heartstealer weapon with lifesteal). Single source; Heartstealer is a weapon amplifier (lifesteal property), not a distinct loop. Rejected.

**Power of Invincibility (Death Barter + Thorns exploit)** — wiki documents this as a mechanic-bug-exploit build. Rejected as degenerate/exploit. Per §7 degenerate-famous logic — if emitted it would be excluded from positive retrodiction. Not emitted; noted here for audit trail.

### Shallow-tail named but not recorded (COVERAGE CONTRACT)

The following were named by ≥1 source but do not reach the §9.19.5 floor and are documented here per the coverage-contract mandate (§3 emission law — "shallow tail DOCUMENTED BY NAME, not recorded"):

- Barbarian / Claymore DPS (heavy slow melee burst — amplifier-only)
- Double Axe Whirlwind (wiki cautions against due to Exploding conflict — potentially negative-canon but no convergent community documentation)
- Lightning Rod soul variant (folded into mcd-soul as a core_skills note)
- Arrow Recycler archer (Recycler enchant on bow — amplifier)
- Final Shout tank variant (Final Shout triggers on near-death — interesting mechanic, single source)

---

## Records emitted

| id | folk_name | canon_tier | key_items | floor verdict |
|---|---|---|---|---|
| mcd-soul | Soul Build (Corrupted Beacon economy) | deep | Corrupted Beacon, Soul Robe, Feral Soul Crossbow | PASS — 6+ independent sources; Corrupted Beacon IS the soul loop anchor |
| mcd-fireworks | Fireworks Arrow Artillery | deep | Fireworks Arrow, Scatter Crossbow/Winter's Touch, Evocation Robe | PASS — 4+ independent sources; Fireworks Arrow artifact IS the artillery loop |
| mcd-dynamo-torment | Dynamo Roll-Shoot (Standstill/Rolling Torment) | moderate | Dynamo enchant, Torment Quiver, roll-shoot rhythm | PASS (narrow) — 2 sources (wiki-hd + gamewith); Dynamo enchant IS the stack loop; flagged low-cred-sourcing |
| mcd-speed | Speed Build (Speedy Steve / Speedy Assassin) | deep | Evocation Robe, Boots of Swiftness, Dagger/Sickle, Light Feather | PASS — 4 independent sources with convergent folk names; Evocation Robe IS the loop closure |
| mcd-summoner | Companion / Beast Master Build | moderate | Golem Kit, Tasty Bone, Wonderful Wheat, Hunter's Promise | PASS — 3 independent sources; companion artifacts ARE the damage source |

**Total: 5 records. Floor minimum met (§9.19.5 "if fewer than ~5 survive, HALT" — 5 = at floor).**

---

## GX ledger

**New GX entries this run: 0.** Convergence metric series extended one step (D2·PoE1·PoE2·D3·D4·LE·GD·TQ·TL·Chronicon·Hades·DI·Undecember·VS/HoT → MCD: still 0 new top-level GX). Taxonomy stable.

**Existing GX entries gained evidence this run:**

| GX | Evidence contributed |
|---|---|
| GX-01 (movement verbs load-bearing) | mcd-speed (Boots of Swiftness IS the build identity — movement verb IS the loop); mcd-dynamo-torment (rolling IS the damage generation mechanic — GX-01 at the roll grain) |
| GX-03 (mark-and-consume / apply-then-detonate) | mcd-dynamo-torment (roll-to-stack → attack-to-release; the clearest ARPG-adjacent roll-commit exhibit; the stack is the "mark", the attack is the "consume") |
| GX-05 (reservation economies) | mcd-soul (Soul resource functions as a capped pool: generate on kill, drain on artifact use — GX-05 family without a UI reservation panel; the closest Tier 2 tail exhibit) |
| GX-13 (enemy-roster-as-arsenal) | mcd-summoner (companion summons as the player's arsenal — GX-13 polarity inverted: player-summoned mobs fill the role of converted enemies) |

---

## Findings blocks (§9.19.3 rider deliverables)

### Finding A — Item-grain authorship pole (type specimen)

MCD is the corpus's **purest authored-at-item-grain game**. The authorship-grain table now reads:

| Grain | Type specimen | RDR relevance |
|---|---|---|
| Build | D3 sets | Authored capstones; LoD escape-valve rule |
| Item | **MCD** + D4 aspects, LE uniques | Gear+enchant IS the build; zero skill tree in MCD |
| Skill | LE per-skill trees | Preferred emergent pole (§9.8) |
| Pair | Hades duo-boons | Collision IS the unlock |
| Deck (⚑) | VS arcana | Modifier draft as authorship surface |

MCD is item-grain at maximum purity: **there is no skill tree, no class ability, no passive node**. The player has three slots (armor, melee weapon, ranged weapon) and three artifact slots. The enchantment system runs on those six item slots. The build IS the itemization. Every record in this corpus is an item configuration, not a playstyle choice — which is why MCD's 120 prior gear-grain rows were a grain error (item lists) and the correct grain is item-defined LOOPS (G3).

This makes MCD the **type specimen** for item-grain authorship in the pipeline's cross-game authorship classification (§9.6/§9.8a). Design implication for RDR: if RDR's loot operator grants items that define play loops (not just amplify existing loops), MCD provides the "authored at maximum" pole for design boundary calibration.

### Finding B — Enchantment-stacking as support-gem-grammar cousin

MCD's enchantment system maps onto PoE1's support-gem link grammar with three similarities and one structural divergence:

**Convergences with PoE1 support gems (GX-portability per §9.16):**
1. **Slot-gating:** each item has a finite number of enchantment slots (3 per item in MCD); PoE link counts gate support gems. The slot budget IS the build budget in both games.
2. **Cooldown-reduction as the support grammar:** in MCD, the dominant enchant strategy is stacking Cooldown Shot + Burst Bowstring + Refreshment to reduce artifact recharge — this IS the "link" that enables the artifact (the skill) to fire more often. Support gems in PoE reduce costs or increase frequency; MCD enchants do the same via cooldown reduction.
3. **Tag-gating analog:** MCD enchants are weapon-type specific (melee vs ranged) — the weapon's type gates which enchants can be slotted, analogous to PoE's skill-tag requirements for which supports can link.

**Structural divergence:**
MCD enchants are on ITEMS (weapon, armor), not on the artifact (skill). The artifact itself has no enchant slots. This means the support grammar is on the DELIVERY VEHICLE, not the SKILL — a different topology than PoE where supports plug directly into the gem socket of the active skill. The effect is the same (reduce cooldown / amplify output) but the locus of control differs: MCD players build around a fixed artifact and modify the items; PoE players build a linked gem setup around a fixed weapon base.

**Relevance to §9.16 support-grammar portability verdict:** the convergences confirm the portability finding — slot-based gating and cooldown/frequency as the support function survive across radically different systems. The locus-of-control divergence (item-locus vs skill-locus) is a free design dimension, as §9.16 found: "load-bearing parts survive any container; geometry is free design space."

---

## Source discipline record

| Source | Rank (§9.19.3) | Role |
|---|---|---|
| minecraft.wiki / minecraft.fandom.com (Build for High Difficulty page) | Rank-3 (community wiki, high-quality) | PRIMARY — only systematic endgame-difficulty treatment; Dynamo Torment dossier |
| gamingscan.com | Rank-3 | Soul Reaper, Speedy Assassin, Hunter Companion folk names |
| gamepur.com | Rank-3 | Soul Warrior, Archer (Fireworks), Speedy Steve folk names |
| thegamer.com | Rank-3 | Soul Fighter, Beast Lover, Speed Run folk names |
| segmentnext.com | Rank-3 | Warlock/Spellcaster, Ranger/Firework, Rogue, Healer archetypes |
| game8.co | Rank-2 (LOW-CRED quarantine per §9.10) | Corroboration-only — Soul Build, Tank, Attacker confirmed present; not sole attestation for any record |
| gamewith.net | Rank-2 (LOW-CRED quarantine per §9.10) | Corroboration-only — Dynamo Torment corroborated from wiki-primary |
| steamcommunity.com/app/1672970 discussions | Rank-3 | Apocalypse Plus build discourse — confirms "life drain essential"; no named build archetypes beyond that |
| minecraft.wiki/w/Dungeons:DLC | Rank-3 (official wiki) | Era verification (final update v1.17, Nov 2022, EOL Sept 2023) |
| Windows Central (soul guide) | Rank-3 | Soul mechanic mechanics detail; Corrupted Beacon role confirmed |
| sportskeeda.com | Rank-3 | Corrupted Beacon = best artifact corroboration |

**Rank-1 sources:** NONE (no build planner exists for MCD — per §9.19.3 spec, confirmed at run). Numeric rider: Apocalypse-Plus ladder discourse is informal; no ratio-scale power rating source found. Canonicity leans longevity + multi-source fame per §9.10 numeric-rider abstention class.

---

## Staging status

**CATALOGUED-ONLY.** Per §9.19.5 law 3: these 5 records are catalogued only. No corpus.db writes. No atlas touch. No fit inputs. Elrond curates; atlas admission waits for archipelago hold-out pass.

**Deliverable location:** `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-corpus-mcd.jsonl` (5 records, all valid JSON)

---

## Run verdict

Basin confirmed thin, naming weak as Gandalf's §9.19.3 verdict predicted. Floor bites hard: 7 of 12 candidates rejected. 5 records at floor minimum. Under-shoot honest — no padding. The two findings blocks deliver the GX-portability and authorship-grain evidence even at this narrow count.
