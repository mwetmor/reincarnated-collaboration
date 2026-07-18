# VDM-1 basin-5 batch-c01 — summary (tq, 11 kits)

**Batch:** c01 | **Game:** Titan Quest (tq) | **Date:** 2026-07-18

## Domain access notes
- titanquest.fandom.com: 402 (paywall/bot-gate) — canary confirmed, zero fandom fetches used
- archive.org: not attempted (canary protocol — fell back immediately to Steam/community)
- Primary sources used: almarsguides.com, steamcommunity.com guides/discussions, lonewardengaming.com, alteredgamer.com, bytesquire.github.io (TQ calculator), mobygames.com, gamepretty.com

## Per-kit one-liners

| kit_id | identity | mechanics | era | negative_canon | notes |
|---|---|---|---|---|---|
| tq-battlemage-warfare-earth | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Fire attested: Volcanic Orb "fire and physical damage" |
| tq-brigand-poison | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Poison attested: "big source of applying poison damage" |
| tq-calculated-strike | CONFIRMED | CONTRADICTED | CONFIRMED | CONFIRMED | Mechanics contradiction: "burst cooldown" claim — fetched says it fires every-fourth-hit (no cooldown), not a dedicated cooldown skill |
| tq-distortion-templar | CONFIRMED | CONTRADICTED | CONFIRMED | n/a | Mechanics: DB says knockback — fetched says STUN; also physical+vitality (not physical-only) |
| tq-dream-harbinger | CONFIRMED | UNSUPPORTED | CONFIRMED | n/a | Psionic Touch/Dream Steal specifics not attested in fetched text |
| tq-druid-squall-caster | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Squall element-SILENT (wind storm; no lightning damage-type descriptor found) |
| tq-elementalist-volcanic-storm | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Fire attested (Volcanic Orb); Thunderball lightning-type NOT attested in fetched text |
| tq-flame-surge | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | Fire attested (search: "pure fire damage"; community: "automatic piercing shotgun of fire") |
| tq-ice-shard-oracle | CONFIRMED | CONFIRMED | UNSUPPORTED | n/a | Cold attested: "inflicting cold damage"; era floor (anniv-2016) — Ice Shard is base Storm skill; floor may be conservative |
| tq-liche-king-conjurer | CONTRADICTED | CONFIRMED | CONFIRMED | n/a | Identity CONTRADICTED: kit folk_name implies player Liche-transformation; fetched: Summon Liche King = PET, not player form |
| tq-marksmanship-haruspex | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Pierce attested: "adds piercing damage"; Trance of Wrath not found in fetched sources |

## Verdict histogram (advisory — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 27 |
| CONTRADICTED | 3 |
| UNSUPPORTED | 3 |
| SOURCE_NOT_FOUND | 0 |

Total claim rows: 33 (11 kits × 3 families + 2 negative_canon rows)

## Contradictions (one line each)

1. **tq-calculated-strike / mechanics:** KB claims "cooldown model makes it a burst-cooldown tool" — fetched text says it is an every-fourth-hit proc mechanic with NO standalone cooldown timer; it applies buffs on the 4th hit, not a dedicated cooldown skill. "Burst" framing is imprecise but the no-cooldown mechanic is the correct reading.
2. **tq-distortion-templar / mechanics:** KB claims "mass knockback" as Distortion Wave effect — fetched text consistently says "stuns" (not knockback); also damage type is physical+vitality per fetched, not physical-only as implied.
3. **tq-liche-king-conjurer / identity:** folk_name "Liche King Conjurer" + mech_note imply Liche Form = player transformation — fetched text unanimous: Summon Liche King is a summoned PET; player never transforms into a Liche. "proxy=heavy" in mechanics is correct but via pet, not self-transformation.

## SOURCE_NOT_FOUND kits
None. All kits had at least one usable source. 0% SNF rate.

## Dossier coverage %

11 kits × 6 families = 66 possible rows

Abstained rows (source silent): 20
Non-abstained: 46

Coverage (non-abstained): 70%

Abstention breakdown by family:
- item_alterations: 8 of 11 abstained (gear specifics rarely extracted from discussion sources)
- author_credit: 7 of 11 abstained (community discussions, no named author)
- capstone_alterations: 1 abstained (tq-dream-harbinger)
- variants: 2 abstained (tq-calculated-strike, tq-dream-harbinger partial)

## Author credits (non-abstained)
- Almar (almarsguides.com): tq-battlemage-warfare-earth, tq-brigand-poison (via Almar elementalist guide), tq-dream-harbinger, tq-elementalist-volcanic-storm, tq-marksmanship-haruspex
- LoneWarden (lonewardengaming.com): tq-brigand-poison
- bytesquire (bytesquire.github.io): tq-calculated-strike

## Element-attestation summary (per kit)

| kit_id | element | verbatim anchor | verdict |
|---|---|---|---|
| tq-battlemage-warfare-earth | fire | "Volcanic Orb deals half fire and half Physical Damage" | ATTESTED |
| tq-brigand-poison | poison | "Poison Gas Bomb will be a big source of applying poison damage" | ATTESTED |
| tq-calculated-strike | physical/pierce | "every fourth hit doing extra damage as well as piercing damage" | ATTESTED (pierce, not fire) |
| tq-distortion-templar | physical + vitality | "physical and vitality damage in a circle around itself" | ATTESTED |
| tq-dream-harbinger | physical | no explicit damage-type text fetched | ELEMENT-SILENT |
| tq-druid-squall-caster | element-SILENT | Squall = "wind storm that does slight damage" — no lightning descriptor | ELEMENT-SILENT (DB elem_raw=lightning is probe inference, not attested) |
| tq-elementalist-volcanic-storm | fire | "explodes when it hits the ground inflicting fire and physical damage" | ATTESTED (fire via Volcanic Orb); Thunderball lightning NOT attested |
| tq-flame-surge | fire | "automatic piercing shotgun of fire" / search: "pure fire damage" | ATTESTED |
| tq-ice-shard-oracle | cold | "Projects a deadly shard of ice at the target inflicting cold damage" | ATTESTED |
| tq-liche-king-conjurer | vitality | "A ranged elemental / vitality damage pet" | ATTESTED |
| tq-marksmanship-haruspex | pierce | "Marksmanship greatly increases projectile speed and adds piercing damage" | ATTESTED (pierce = non-engine flavor; mapper decides family) |

## Red flags

1. **tq-liche-king-conjurer — player transformation claim is factually wrong.** The DB mech_note says "Liche Form = Spirit mastery's transformation skill — transforms the player into an undead liche entity." All fetched sources describe Summon Liche King as a summoned pet companion, not a player-form transformation. Conjurer never transforms. This is a significant mech_note error — recommend Elrond audit.

2. **tq-distortion-templar — knockback vs stun.** DB mech_note says "mass knockback that clears large groups." Fetched sources say "stuns." These are mechanically different crowd-control effects. Downstream mapping of control centrality should use STUN, not knockback.

3. **tq-calculated-strike — "cooldown model" framing.** The DB mech_note characterizes it as a "cooldown model" making it a burst tool. Fetched text: Calculated Strike has NO cooldown timer — it is an every-fourth-hit proc. The negative-canon reason is correct (infrequent compared to Onslaught) but the mechanism is not a cooldown; it is a hit-count gate.

4. **tq-druid-squall-caster — Squall element mismatch.** DB elem_raw = "lightning". Fetched sources consistently describe Squall as a "wind storm" with debuff/utility focus. Static Charge synergy adds lightning bonuses but Squall itself has no attested lightning damage-type descriptor. Downstream mapping should treat Squall as element-silent unless further source confirms.

5. **tq-ice-shard-oracle era floor.** Era stamped anniversary-2016 / ragnarok-2017. Ice Shard is a base Storm mastery skill present in base-2006. Floor is likely conservative but no source contradicts it (it remains viable in those eras). UNSUPPORTED only — not CONTRADICTED.
