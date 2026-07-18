# VDM-1 Basin-3 Batch-14 Summary — kits 157–168 (di)
Date: 2026-07-18

## Per-kit one-liners

- **di-bombardment-wizard-pvp** — All claims UNSUPPORTED. No Bombardment Wizard build exists on icy-veins or Dexerto (Patch 5.0). Wizard PvP meta in 2026 is Arcane Wind/Scorch/Disintegrate. "Bombardment" does not appear as a DI Wizard skill in any fetched source. Full source coverage obtained; source simply does not attest the build.
- **di-bone-wall-necro-pvp** — Identity CONFIRMED (Bone Wall-centric CC devastator framing attested). Era CONFIRMED (May 2022 guide). Mechanics UNSUPPORTED: Essence not named as a resource in DI Necromancer sources; stun-chain framing not attested (Bone Spikes has a stun but chain framing absent). Wraith Form confirmed as mobility skill. Two variants attested.
- **di-corpse-explosion-necro** — Identity CONFIRMED (Corpse Explosion as Necromancer skill detonating corpses at target area). Era CONFIRMED (launch-2022). Mechanics partial: Corpse Explosion confirmed; Bone Spikes not found in Gamerant CE build (may be in other builds); Essence resource not attested in DI sources.
- **di-crusader-banner-support** — Identity CONFIRMED. Era CONFIRMED (launch-2022 guide). Mechanics: Holy Banner + Conjuration of Light + Spinning Shield all confirmed as Crusader skills; Wrath resource NOT attested in any fetched DI Crusader source. Capstone legendaries extracted (Arrowkeeper + Sinkhole Cross + Justice Without Favor).
- **di-cyclone-monk-pvp** — Identity CONFIRMED (Cyclone Strike vortex pull confirmed; Imprisoned Fist listed as control skill). Era CONFIRMED (launch-2022 guide). Mechanics: Cyclone Strike + Imprisoned Fist confirmed; Spirit resource NOT attested in fetched DI Monk sources (icy-veins Monk overview does not name a "Spirit" resource explicitly). PvP angle: Imprisoned Fist PvP build is the attested Monk PvP guide; Cyclone Strike absent from that build (it's in raids and general builds, not the dedicated PvP guide).
- **di-cyclone-strike-monk-base** — NULL-era roster-hygiene kit. No era claims to verdict. Identity CONFIRMED (Cyclone Strike confirmed as DI Monk skill). Attested eras from fetched sources: icy-veins guide dated June 2022 + used in raid build + raid context → skill present from di-launch-2022. Steward note: backfill era with di-launch-2022 minimum.
- **di-draw-quarter-crusader** — Identity CONFIRMED with strong verbatim anchor. Era CONFIRMED. Mechanics: Draw and Quarter confirmed as horse mount with holy-chain enemy dragging; Sweep Attack listed as Crusader skill; Wrath resource NOT attested in DI Crusader fetched sources. Excellent geometry capture.
- **di-druid-bear** — Identity CONFIRMED (Werebear transformation + heal suite + summons confirmed via official Blizzard article). Era CONFIRMED (July 3, 2025 launch). ONE CONTRADICTION: DB `resource_verbatim: "Spirit (Druid)"` is WRONG — fetched Blizzard source explicitly names the resource "Primal Power." This is a probe_facts fabrication.
- **di-essence-transfer** — SYSTEM kit. Identity + mechanics + era all CONFIRMED. Essence Transfer = extract legendary power (destroys item, costs 3000 Gold) via NPC Zamina; inherit into target (free, reversible); extracted essence reusable. Launched at DI launch-2022. Class-resource instruments correctly not applied. Strong capstone_alterations entry.
- **di-frenzy-barb** — Identity CONFIRMED with strong verbatim anchor (attack speed stacking mechanic confirmed). Era CONFIRMED (launch-2022 guide). Mechanics: Frenzy attack-speed stacking confirmed; Sprint not found in any attested build (Frenzy Raid build uses Furious Charge not Sprint); Fury resource NOT attested in DI Barbarian fetched sources (DI uses energy mechanic for channeled skills, not D3-style Fury). Partial mechanics UNSUPPORTED.
- **di-hota-wotb-barb** — Identity CONFIRMED (HotA + WotB + Ground Stomp all confirmed as DI Barbarian skills). Era CONFIRMED (launch-2022 + Lasting Hate/Broken Soul legendaries). Mechanics: skill trio confirmed; Fury resource NOT attested in DI sources (same energy system issue). Capstone legendaries extracted (Lasting Hate + Broken Soul).
- **di-inferno-ladder** — SYSTEM kit. Identity + mechanics + era all CONFIRMED. Challenge Rifts + Paragon progression confirmed from launch. Inferno difficulty tiers I-III confirmed (post-launch, Paragon 800+ requirement). CR thresholds: I=34900, II=37320, III=39320. Author credit: Deadset (icy-veins.com). Strong coverage.

## Verdict histogram (ADVISORY — steward recounts from files)

- CONFIRMED: 22
- UNSUPPORTED: 11
- CONTRADICTED: 1
- SOURCE_NOT_FOUND: 0

## Contradictions (1 — NOT zero; note LOUDLY)

1. **di-druid-bear / mechanics / resource_verbatim**: DB field records "Spirit (Druid)" as the Druid's resource. Fetched official Blizzard source (news.blizzard.com, July 2025) explicitly states: "Primal Power is a resource unique to Druids, represented by a green bar above the skill buttons." The DB claim is CONTRADICTED — correct resource name is Primal Power, not Spirit.

## SOURCE_NOT_FOUND kits

None. All 12 kits found coverage from at least one valid source.

## Dossier coverage

- skill_loop: 10/12 populated (di-bombardment-wizard-pvp abstained all; abstain rate expected for SNF-class kit)
- skill_geometry: 10/12 populated
- item_alterations: 2/12 populated (di-essence-transfer has extraction cost mechanics; di-corpse-explosion-necro abstained; most build kits abstained — item names not retrieved in depth)
- capstone_alterations: 7/12 populated (di-crusader-banner-support legendaries; di-hota-wotb-barb legendaries; di-inferno-ladder inferno CR thresholds; di-essence-transfer system entry; di-druid-bear The Craw legendary; di-bone-wall-necro-pvp legendary note; di-corpse-explosion-necro Rotspur note)
- author_credit: 1/12 populated (Deadset for di-inferno-ladder icy-veins guide; other guides no named author available)
- variants: 2/12 populated (di-bone-wall-necro-pvp has 2 attested variants; di-crusader-banner-support has no distinct variants)

Overall non-abstained dossier rows: ~32/72 = ~44%

## Author credits

- Deadset (icy-veins.com) — di-inferno-ladder Challenge Rifts guide

## Red flags for steward/elrond erratum queue

1. **DI class resource fabrication pattern confirmed batch-wide.** DB probe_facts `resource_verbatim` fields for DI kits appear to have inherited D3 resource names. Fetched DI sources do NOT name class resources the same way:
   - Wizard: no "Arcane Power" resource in DI (only referenced in legendary item flavor text); channeled skills use an energy mechanic
   - Barbarian: no "Fury" resource in DI; Whirlwind uses an energy mechanic
   - Necromancer: no "Essence" resource named in DI guide text (skills use cooldowns and energy)
   - Monk: no "Spirit" resource explicitly named in DI Monk overview
   - Crusader: no "Wrath" resource named in DI Crusader guide
   - Druid: CONTRADICTED — DB says "Spirit (Druid)"; actual resource is "Primal Power" (Blizzard official)
   This is a systematic probe_facts issue across all DI kits. The one confirmed CONTRADICTED verdict is Druid/Spirit, but the others are all UNSUPPORTED rather than CONTRADICTED because DI simply doesn't surface the named resource prominently (D3 names them; DI abstracts them away). Steward should flag resource_verbatim fields for all DI kits as unreliable.

2. **di-bombardment-wizard-pvp: zero evidence kit.** No Bombardment skill exists in DI Wizard skill list on icy-veins (not listed among ~15 named Wizard skills). In Patch 5.0 (June 2026), meta is Arcane Wind/Lightning Nova/Scorch. This kit may be a fabrication or a misapplication of the D3 Bombardment skill to DI. Flag for Elrond mint review.

3. **di-cyclone-monk-pvp: PvP framing tension.** The attested DI Monk PvP guide (icy-veins, Imprisoned Fist PvP) does NOT include Cyclone Strike. Cyclone Strike appears in raid and general builds. The PvP alias "Imprisoned Fist Cyclone Monk DI" is partially attested but no dedicated PvP build centering Cyclone Strike + Imprisoned Fist together was found.

4. **di-frenzy-barb Sprint claim: not attested.** The Frenzy Raid build on icy-veins uses Furious Charge as the mobility skill, not Sprint. Sprint not found in any fetched Frenzy build. The spec alias "DI Frenzy Sprint Barb" may be inaccurate.

5. **di-crusader-banner-support: Wrath resource not attested in DI.** DI Crusader guides on icy-veins do not name a "Wrath" resource. Unlike D3 where Wrath is named explicitly, DI guides describe skills on cooldowns without naming the resource pool.

6. **di-hota-wotb-barb capstone source note.** The Lasting Hate / Broken Soul legendary data was surfaced via a web search summary (gamerdigest.com returned 500). The anchor quote was reconstructed from the search result snippet. The source URL is flagged as conf=0.65 — lower confidence due to no direct fetch verification.

7. **di-cyclone-strike-monk-base (NULL-era kit):** Steward backfill recommendation — di-launch-2022 minimum confirmed by icy-veins guide dated June 2022 featuring Cyclone Strike as an active Monk skill.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18)

**Batch ACCEPTED with corrections** (1 re-anchor, 3 verdict-downgrades). Post-correction file truth: **34 rows = 20C/13U/1X**. Advisory drift #22 (advisory 22C/11U vs pre-correction file 23C/10U).

1. **TOOLTIP-AS-ANCHOR pattern (new anchor-relevance sub-class, b12 non-probative lineage):** skill-tooltip text ("Generate a vortex of wind…", "Detonate all corpses…") was used to ground identity (folk-name usage) and era (meta presence) claims it cannot support — a tooltip attests the SKILL exists, never that the community uses a folk name or that a build was era-meta. Downgraded C→U ×3: di-cyclone-monk-pvp identity + era · di-corpse-explosion-necro era. CW5-closing note: this joins gloss-anchors (b07) and splices (b08) in the anchor-failure taxonomy.
2. **Re-anchor (b08 spectral-blade precedent):** di-corpse-explosion-necro identity C STANDS re-grounded on the same fetched page's title "Diablo Immortal: Best Corpse Explosion Necromancer Build" — title-as-identity-ground (bouldercane/b02 lineage; gamerant = journalism, admissible for identity/era, never mechanics).
3. **TOLERATED-amber:** di-cyclone-strike-monk-base identity C — base-kit constructed label ("DI Monk — Cyclone Strike (base)"): identity reduces to skill-existence; tooltip verbatim under the skill's class-page listing attests it. Base-kit identity ≠ folk-name identity (ruling noted for the book).
4. **SCOPING RULING minted:** the b02 journalism prohibition targets BUILD-meta mechanics paraphrase. A dedicated system-explainer (blizzardwatch essence-transfer, 2022-06-13 launch coverage) with verbatim functional description is **communal-admissible for SYSTEM-kit identity/mechanics/era** — di-essence-transfer 3C KEEP.
5. **di-druid-bear mechanics X STANDS — strongest ground class of the run:** OFFICIAL Blizzard class-intro page affirmatively names the Druid resource "Primal Power" vs kb "Spirit (Druid)". Official first-party sources were never in the journalism prohibition. → **erratum HIGH: di Druid resource = Primal Power.**
6. **BATCH-WIDE di resource-fabrication finding (agent red-flag 1 RATIFIED):** all di `resource_verbatim` probe fields inherited d3 names; none attested by fetched di text; druid-bear is the clean contradiction. → INGEST-13: flag ALL di resource probe rows unreliable (joins the ~10-item fabrication series; consolidated renumber pending).
7. **di-bombardment-wizard-pvp = kit-level SPEC-ERROR CANDIDATE #2 (void-rift class):** honest 3×U; Bombardment absent from icy-veins' full Wizard skill list — likely d3→di misapplication at kb-generation. → Unattested Register KIT-LEVEL + review-book Matt keep-vs-excise decision (with void-rift).
8. **Smaller errata:** di-frenzy-barb alias "DI Frenzy Sprint Barb" + core_skills Sprint unattested (fetched shows Furious Charge) — MEDIUM. di-cyclone-strike-monk-base NULL-era backfill: di-launch-2022 attested (icy-veins June-2022 guide) — roster-hygiene row delivered ✓; its mechanics row was NOT emitted (coverage miss) → BACKFILL-3 micro-task.
9. **Praise:** anchors formally clean (0 gloss, 0 splice, 0 >40w); abstain-null law HELD 42/42; zero commerce-SEO citations needed quarantining (the aggression warning landed); dossier 41.7% is the run's lowest but was predicted in-prompt for di — honest abstention over stretch.
