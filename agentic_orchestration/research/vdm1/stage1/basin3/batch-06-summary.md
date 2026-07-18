# VDM-1 Basin-3 Batch-06 Summary
**Kits:** L61–L72 (all d3) | **Date:** 2026-07-18 | **Legolas instance:** batch-06

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | neg_canon | dossier |
|---|---|---|---|---|---|
| d3-akkhan-condemn | CONFIRMED | CONFIRMED (Wrath, Condemn nova, Akarat's) | set-era CONFIRMED · late-sets CONFIRMED | n/a | full |
| d3-aov-foth | CONFIRMED | CONFIRMED (Wrath, FotH large AoE, unlimited range) | late-sets CONFIRMED · s39 CONFIRMED | n/a | full |
| d3-arachyr-firebats | CONFIRMED | CONFIRMED (Firebats cone channel, Mana) | set-era CONFIRMED · late-sets CONFIRMED | n/a | full |
| d3-call-of-the-ancients | CONFIRMED | CONFIRMED (CotA summon mechanic, official Blizzard page) | NULL era — nothing to contradict; attested eras: set-era (IK HotA context) | n/a | partial (author_credit abstained — no standalone guide author) |
| d3-dashing-strike-monk | CONFIRMED | CONFIRMED (DS primary damage, Spirit resource, Raiment set) | NULL era — nothing to contradict; attested era: set-era (Patch 2.4, post-nerf non-viable) | n/a | full |
| d3-dmo-twister | CONFIRMED | CONFIRMED (Energy Twister, Slow Time, Arcane Power, wandering projectile) | set-era CONFIRMED | n/a | full |
| d3-firebird | CONFIRMED | CONFIRMED (Disintegrate channel, Ignite/Combustion mechanic, Arcane Power) | set-era CONFIRMED · late-sets CONFIRMED · s39 CONFIRMED | n/a | full |
| d3-firebomb | CONFIRMED | CONFIRMED (lob mechanic, free Signature spell; NOT ground-targeted) | vanilla UNSUPPORTED · set-era UNSUPPORTED | CONFIRMED (no set, no scaling synergy, LoN-only novelty) | partial (item_alterations abstained, author_credit abstained) |
| d3-frenzy-h90 | CONFIRMED | CONFIRMED (Frenzy primary, Fury generator, H90 introduced S20) | late-sets CONFIRMED · s39 CONFIRMED | n/a | full |
| d3-god-hungering | CONTRADICTED on alias | CONFIRMED (Strafe+HA, projectile behavior) | late-sets CONFIRMED · s39 CONFIRMED | n/a | full (resource RED FLAG recorded) |
| d3-helltooth-garg | CONFIRMED | CONFIRMED (Gargantuan×3, Wall of Death activator, Mana) | set-era CONFIRMED · late-sets CONFIRMED · s39 CONFIRMED | n/a | full |
| d3-ik-hota | CONFIRMED | CONFIRMED (HotA+CotA, Fury, IK 6pc mechanic) | vanilla UNSUPPORTED · set-era CONFIRMED (Season 4) · s39 CONFIRMED | n/a | full |

---

## Advisory verdict histogram (DO NOT USE AS COUNT — file truth governs)

- CONFIRMED: ~43
- CONTRADICTED: 1 (d3-god-hungering identity alias)
- UNSUPPORTED: 4 (d3-firebomb vanilla, d3-firebomb set-era, d3-ik-hota vanilla, d3-ik-hota vanilla)
- SOURCE_NOT_FOUND: 0

---

## Contradictions (one line each)

1. **d3-god-hungering / identity**: Alias "Grace of Inarius DH" is CONTRADICTED — the set is named "Gears of Dreadlands" throughout all sources. "Grace of Inarius" does not appear in any fetched text and appears to be a fabricated alias mixing D3 set names. Anchor: "Gears of Dreadlands Hungering Arrow Demon Hunter has made its entry during Season 21" (maxroll.gg/d3/guides/god-ha-demon-hunter-guide).

---

## UNSUPPORTED claims (source found, silent on the claim)

- **d3-firebomb / era / vanilla**: Official skill page confirms skill exists and is free (Signature), but no source attests vanilla meta presence.
- **d3-firebomb / era / set-era**: Icy-veins WD builds page lists no Firebomb build; absent entirely from viable build lists.
- **d3-ik-hota / era / vanilla**: Both maxroll and icy-veins guides reference earliest IK HotA season as Season 4 (RoS set-era) with no vanilla mention. IK set existed at vanilla launch but current set bonuses (CotA+WotB 6pc synergy) are set-era reworks; no source confirms a vanilla IK HotA meta identity.

---

## SOURCE_NOT_FOUND kits

None.

---

## NULL-era kits — attested eras for steward backfill

- **d3-call-of-the-ancients** (L64, era=NULL): Skill attested in official Blizzard game guide as Barbarian level-25 skill present since launch. In IK HotA context, attested from Season 4 (set-era) through S39. Recommended backfill: `set-era;late-sets;s39` (as support skill in IK HotA).
- **d3-dashing-strike-monk** (L65, era=NULL): Raiment DS build attested at Patch 2.4; guide explicitly states "no longer viable" after Patch 2.4 nerfs. Modern Monk builds use DS as utility/mobility only. Recommended backfill: `set-era` (primary damage identity existed in set-era only, specifically Patch 2.4 window).

---

## Dossier coverage

12 kits × 6 families = 72 family slots.
- Abstained: 3 slots (d3-call-of-the-ancients/author_credit; d3-firebomb/item_alterations; d3-firebomb/author_credit)
- Non-abstained and populated: 69 slots
- Coverage: **96%** (69/72 family slots have payload)

---

## Author credits recovered

| kit_id | handle | site |
|---|---|---|
| d3-akkhan-condemn | Northwar | maxroll.gg |
| d3-aov-foth | Northwar | maxroll.gg |
| d3-arachyr-firebats | Deadset | icy-veins.com |
| d3-dashing-strike-monk | Deadset | icy-veins.com |
| d3-dmo-twister | sVr (updated: Chewingnom) | maxroll.gg |
| d3-firebird | Chewingnom | maxroll.gg |
| d3-frenzy-h90 | Rob (updated: Chewingnom; reviewed: Northwar, Raxxanterax) | maxroll.gg |
| d3-god-hungering | wudijo (co: Northwar) | maxroll.gg |
| d3-helltooth-garg | wudijo (updated: Chewingnom; reviewed: Northwar, Raxxanterax) | maxroll.gg |
| d3-ik-hota | Rob (intro: Chewingnom; icy-veins: Deadset) | maxroll.gg |
| d3-call-of-the-ancients | (none — official skill page; no standalone guide author) | blizzard.com |
| d3-firebomb | (none — no dedicated viable build guide exists) | — |

---

## Red flags for steward / erratum queue

**RED FLAG 1 — GoD DH probe resource fabrication (probe-artifact watch):**
`canon_probe_facts` records `resource_verbatim: "spirit/focus"` for d3-god-hungering. Fetched sources confirm Demon Hunter uses Hatred+Discipline — "Demon Hunters have a unique dual-resource system, using both Hatred & Discipline to power their skills" (maxroll.gg/d3/resources/demon-hunter). "Spirit" and "Focus" are Monk and Necromancer resources respectively. This is a fabrication error in the probe layer identical to the basin-2 GD spirit/focus pattern. Recommend elrond erratum correction: `resource_verbatim` → "hatred+discipline", `meter_type` → "dual-resource".

**RED FLAG 2 — d3-god-hungering alias "Grace of Inarius DH" not attested:**
"Grace of Inarius" does not appear in any fetched text. The set is consistently "Gears of Dreadlands" (GoD). The alias appears to be a confabulation mixing D3 set names. Elrond should remove or flag this alias in the corpus.

**RED FLAG 3 — d3-ik-hota vanilla era flag:**
DB records `vanilla` in eras for d3-ik-hota. No fetched source supports a vanilla IK HotA build identity — earliest attested is Season 4 (set-era). The IK set existed at vanilla launch but the current CotA+WotB 6pc synergy mechanic is a set-era rework. Steward should consider flagging the vanilla era row for erratum review: likely CONTRADICTED (floor too early given set bonus rework) OR retain UNSUPPORTED as honest.

**RED FLAG 4 — d3-firebomb delivery: "lob" not "ground-targeted":**
`negative_canon_target` calls Firebomb a "ground-targeted fire grenade mechanic." Official Blizzard page says: "Lob an explosive skull" — it's a LOBBED projectile that explodes on impact, not a ground-targeted skill in the D3 mechanic sense (ground-targeted would be a cursor-placed AoE like Wall of Death). Minor terminology discrepancy in the negative_canon framing; the substance (no scaling synergy, no set identity) is confirmed.

**RED FLAG 5 — d3-frenzy-h90 probe resource_verbatim "on-hit stacks" imprecision:**
The probe records `resource_verbatim: "on-hit stacks"` for d3-frenzy-h90. Fetched sources confirm Frenzy is a Fury-GENERATING Primary skill (Barbarian resource = Fury). "On-hit stacks" refers to the Bastion's Revered Frenzy-stack mechanic, not the resource system. The actual resource is Fury. Elrond may wish to note this probe imprecision.

---

## Notes on Firebird identity claim

The spec records `core_skills: ["Disintegrate", "Ignite(set mechanic)"]`. Modern S39 Firebird builds use Explosive Blast or Flame Blades as the primary damage skill — however, Disintegrate remains the TRIGGER for Ignite/Combustion stacks ("Disintegrate is the cornerstone of the reworked Firebird's Finery set"). The `core_skills` claim is CONFIRMED for the Disintegrate+Ignite interaction, though Explosive Blast is now the damage payload in the S39 Explosive Blast variant. This is an evolution of the kit, not a contradiction. Folk name "Ignite Wizard" accurately reflects the Combustion/Ignite mechanic.

---

## Crawl notes

- reddit.com blocked by Anthropic crawler policy — no reddit sources used this batch. All verify and dossier material sourced from maxroll.gg/d3 and icy-veins.com (primary domain order followed).
- diablowiki.net returned 403 for Immortal King's Call page; diablo.fandom.com returned 402 for two pages. Used available Blizzard official pages and maxroll/icy-veins as substitutes.
- Icy-veins Dashing Strike Monk guide is archived Patch 2.4 content — acknowledged as historical, not current meta. Valid for set-era era verification.
- All junk/SEO domains quarantined; none cited.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18 — CW2, audited on return)

**ACCEPTED, 0 corrections.** File truth: **47 rows = 43C/3U/1X/0SNF** (advisory "43C/1X/4U" — near-exact; drift series #15, U off by 1: the agent's own U-list double-counted ik-hota vanilla; kits 12 ✓, families 12/12/22/1, negative_canon exactly 1 per roster — d3-firebomb ✓). Anchors: C/X all present, zero >40w. Abstain-null law HELD 3/3. Citations 16/0 quarantined (maxroll 10 · icy-veins 4 · blizzard official 2). Dossier 72 rows, 69 non-abstained = **95.8%** — best coverage of the run so far (d3's living maxroll/icy-veins guide layer is dense; contrast b04 d2's 62.5%).

**The X is REAL and valuable:** d3-god-hungering identity CONTRADICTED — "Grace of Inarius DH" alias is a set-name confabulation; fetched text is uniformly **"Gears of Dreadlands"** ("Gears of Dreadlands Hungering Arrow Demon Hunter has made its entry…"). → ERRATUM (alias removal) INGEST-13. Second basin-3 X after b02 fishyzon.

**Erratum queue adds (INGEST-13):** GoD-DH probe `resource_verbatim: "spirit/focus"` FABRICATION — DH is Hatred+Discipline (the basin-2 gd spirit/focus pattern REAPPEARS in d3 — probe-artifact watch vindicated; template's d3 class-resource table was the catch instrument) · d3-ik-hota `vanilla` floor-too-early D-2a CANDIDATE (earliest attested Season 4 set-era; IK set existed at vanilla but the CotA/WotB 6pc synergy is a set-era rework — vanilla row honest-U in files; steward routes to D-2a adjudication at INGEST-13, not a unilateral X) · d3-firebomb negative_canon_target "ground-targeted" → "lobbed projectile" framing fix (official "Lob an explosive skull…"; substance of the negative CONFIRMED) · d3-frenzy-h90 probe `resource_verbatim: "on-hit stacks"` → Fury (Bastion's Revered stack mechanic ≠ resource). NULL-era roster clean: call-of-the-ancients + dashing-strike-monk zero era rows ✓ (attested eras in summary for backfill); firebird S39-evolution note (Disintegrate=trigger, Explosive Blast=payload) is good evolution-not-contradiction judgment.
