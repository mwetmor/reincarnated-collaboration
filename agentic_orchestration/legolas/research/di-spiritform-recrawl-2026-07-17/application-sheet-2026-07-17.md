# Application Sheet — DI Spirit-Form Druid PvP Re-crawl (Third Attempt) — 2026-07-17

**For:** Elrond (mechanical DB application)
**Crawl date:** 2026-07-17
**Landed ailment vocab reference:** {damage-amp, freeze, stun, poison-dot, taunt, blind, curse/hex, fear, instant-kill, deflect} + soft_control variants (slow, root/immobilize, knockback, silence, burn/DoT, marking)

Iron law: every row cites live URLs or is marked UNVERIFIABLE / PHANTOM with search trail. Row counts reconcile with index summary block (1 phantom = 1 total).

---

## BATCH (1 kit)

---

### 1. `di-spiritform-druid-pvp` — "Spirit-Form Druid (complaint-tier)"

**disposition:** **phantom**
**target action for Elrond:** flag as provenance-integrity phantom kit (see recommendation A/B/C in `00-index.md`). Mirror `d2-wl-void-rift` precedent from econ-recrawl 2026-07-16 (finding #1). No landed-vocab classification is possible because the KIT AS NAMED does not exist as a mechanic; the class + PvP CC stack IS real but requires re-keying.

**corpus row context (from `SELECT ... FROM canon_corpus`):**
- `kit_id`: `di-spiritform-druid-pvp`
- `folk_name`: `Spirit-Form Druid (complaint-tier)`
- `game`: `di`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `atlas_key_orig`: `SDMFSI-HSMM-CD-PH-~~`
- `elem_raw`: `physical`
- `mech_note`: "POST-CUTOFF: di-2026-era only. Conf capped ≤0.50. 'Complaint-tier' = PVP overpowered at time of corpus capture. Spirit form = alternate Druid state (not Bear Form). All claims atlas-provenance only."
- `flags`: `kb-only-backfill-attempted-2026-07-16,econ-recrawl-unverifiable-2026-07-16`
- `prov`: `vx`

**Class + mechanic verification — POSITIVE confirms (class real):**

**live URL(s) — class exists, launched 2025-07-03:**
- https://news.blizzard.com/en-us/article/24216435 ("Introducing Diablo Immortal's Newest Class: Druid") — official Blizzard announcement
- https://massivelyop.com/2025/06/26/hands-on-with-diablo-immortals-newly-announced-druid-launching-july-3/ — hands-on preview with July 3 launch date
- https://news.xbox.com/en-us/2025/06/26/the-legacy-of-diablos-druid-class/ — XBOX Wire coverage
- https://blizzardwatch.com/2025/06/26/diablo-immortal-druid-class/ — Blizzardwatch hands-on with full skill list

**evidence quote (class existence):** Blizzard official news post (via WebSearch): "the Druid serves as a primal reimagining of the classic archetype" with class identity "revolves around elemental upheaval and overall volatility, while still retaining some familiar features of the Diablo 4 rendition including animal companions, shapeshifting, and elemental casting. Werebear, Stag Charge, and Raven Swarm aim to make the class feel uniquely aggressive and thoroughly unpredictable." Massively Overpowered: launch "scheduled for July 3, 2025." The DI Druid launched more than 12 months before the 2026-07-12 corpus source_date; class existence is not in question.

**Class + mechanic verification — NEGATIVE confirms (mechanic phantom):**

**Exhaustive DI Druid transformation set — no "spirit form":**

Two independent full-skill enumerations agree (WebFetch of news.blizzard.com/en-us/article/24216435; WebFetch of blizzardwatch.com/2025/06/26/diablo-immortal-druid-class):

- **Primary Attacks:** Ferocious Strike, Landslide (L34)
- **Transformations:** Werewolf (L3), Werebear (L38), Stag Charge, Raven Swarm
- **Nature Magic:** Fire Tornado, Summon Wolves, Earthquake, Thorn Armor, Summon Grizzly, Summon Oak Sage, Circle of Life (L47), Surging Stone, Rabid Might (L53)

**evidence quote (mechanic absence):** Blizzardwatch hands-on via WebFetch: "No separate 'spirit form' or 'spirit shift' mechanic exists beyond the transformations listed. The four transformation abilities (Werewolf, Werebear, Stag Charge, Raven Swarm) function as the class's shape-shifting system." Blizzard official news post via WebFetch: "No 'spirit form,' 'spiritform,' or 'spirit shift' mechanics are mentioned." Wowhead skills page (WebFetch of wowhead.com/diablo-immortal/skills) confirmed no Druid entry appears in the class filter as of skill-page load (Druid may not yet be enumerated in the WoWhead skill DB — separate issue), but the Blizzard-authoritative source is complete and exhaustive.

**"Spirit"-adjacent items that could have caused mob-harvest confusion:**
- **Spirit Essence** — a "Miscellaneous Item" used to level up familiars (via wowhead.com/diablo-immortal/misc-item/spirit-essence-80015). Unrelated to Druid class. Item-slot noise.
- **Summon Oak Sage** — a nature-spirit totem summon that **Immobilizes for 4 seconds**. This IS a Druid CC skill but is a summoned entity, not a self-transformation.
- **Beast Soul Awakening** — a **staff-strike essence** enhancement ("allowing the spirit of the beast to possess the user, granting a shield upon activation, turning basic attacks into area-of-effect attacks"). This is a gear-essence modifier, not a Druid class skill or transformation.

None of these matches the corpus mech_note description "alternate Druid state (not Bear Form)."

**live URL(s) — DI Druid CC vocabulary IS entirely landed:**
- https://diablo.fandom.com/wiki/Werebear_(Diablo_Immortal) — Werebear stuns (2s roar; Hulking Werebear 3s; Mangle 1s/3s)
- https://diablo.fandom.com/wiki/Werewolf_(Diablo_Immortal) — Werewolf marking + knockback
- https://diablo.fandom.com/wiki/Circle_of_Life_(Diablo_Immortal) — heal-field, no CC
- https://us.forums.blizzard.com/en/diablo-immortal/t/druid-still-ruins-the-whole-bg/11238 — PvP complaint thread (Q3-Q4 2025)
- https://us.forums.blizzard.com/en/diablo-immortal/t/it%E2%80%99s-wrong-to-nerf-druid/11249 — post-nerf discussion
- https://us.forums.blizzard.com/en/diablo-immortal/t/when-are-we-addressing-major-pvp-class-imbalances-in-battlegrounds/12960 — Feb 2026 balance discussion

**evidence quote (CC vocab all landed):** Blizzard official + Blizzardwatch full-skill enumeration (via WebFetch, verbatim classification): "Werebear transformation now causes you to roar, dealing damage and Stunning nearby enemies for 3 seconds" (Hulking Werebear essence variant). "Summon Grizzly: Stun: 'Stunning them for 4 seconds'." "Summon Oak Sage: Immobilize: 'Immobilizing them for 4 seconds'." "Stag Charge: Slow: 'reducing their Movement Speed by 40%'." "Thorn Armor: Slow: 'Slowing them by 40%'." "Earthquake: Knockback (enemies launched airborne)." "Werewolf — Howl: Marking effect" (damage-amp when target <50% HP). "Werebear — Bound: Knockback + self KB-immunity during dash." "Fire Tornado: Burn effect."

**IF Elrond re-keys as clean kit (recommendation B):** the CC vocab maps entirely to landed set — primary shape is **multi-source stun** (Werebear roar 2-3s + Summon Grizzly 4s + Mangle 1-3s), secondary **soft-control stack** (Slow 40%, Immobilize 4s, Knockback multi-source, damage-amp Marking). No new ailment vocabulary is needed.

**Search trail — where "spirit form" was NOT found:**
- WebSearch `"Diablo Immortal" "Druid" class PvP spirit form` — returned skill-list results; no "spirit form" skill found; only Beast Soul Awakening (essence, not form) as closest match
- WebSearch `"Diablo Immortal" Druid skills list Werebear Werewolf Raven Swarm crowd control` — enumerated all transformations (Werebear/Werewolf/Raven Swarm/Stag Charge) with CC effects; no "spirit form" in list
- WebSearch `"Diablo Immortal" Druid "spirit" transformation ability skill` — returned "spirit"-adjacent items (Spirit Essence, Beast Soul Awakening) but confirmed "there doesn't appear to be a specific transformation ability called 'spirit'"
- WebSearch `"Diablo Immortal" Druid essence "spirit" OR "spiritual" OR "specter"` — Spirit Essence (familiar-leveling item, unrelated); no Druid-class match
- WebSearch `"spirit form" druid diablo immortal PvP reddit` — **"No links found"** (WebSearch's follow-up narrative "Spirit Form is a skill used by Druids in Diablo Immortal" contained NO cited URLs and is model fabrication — flagged as invalid)
- WebSearch `reddit r/DiabloImmortal druid PvP broken spirit form crowd control` — **"No links found"**
- WebFetch of Blizzard official news post — negative confirmation: `"No 'spirit form,' 'spiritform,' or 'spirit shift' mechanics are mentioned."`
- WebFetch of Blizzardwatch hands-on — negative confirmation: `"No separate 'spirit form' or 'spirit shift' mechanic exists beyond the transformations listed."`

**Cross-game contamination candidates (why the harvest might have picked this up):**
- **D4 Spiritborn** — Diablo 4 Vessel of Hatred expansion class (Sept 2024); has "Spirit" resource + Jaguar/Eagle/Gorilla/Centipede spirit forms. Distinct game, distinct class, but the "spirit form" phrase is native to D4 Spiritborn discourse.
- **PoE Spirit** — Path of Exile 2 has "Spirit" as a passive resource; some PoE Druid-adjacent Warden ascendancies use nature/spirit vocabulary
- **WoW Druid** — Ghost Wolf, Tree of Life, Moonkin/Boomkin, and Bear/Cat forms are casually called "spirit form" in some player threads
- **D2 Druid Spirit-line spells** — Oak Sage, Heart of Wolverine, Spirit of Barbs (three Spirit-summon skills in D2 Druid tree). These are the DI Druid's Summon Oak Sage lineage; corpus harvester may have confused "Spirit summon" with "spirit form".

**None of these cross-game hits change the finding: the KIT AS NAMED does not exist in DI.**

**PvP complaint pattern verified — matches "complaint-tier" provenance:**

The DI Druid WAS the subject of major PvP-complaint discourse in Q3-Q4 2025, matching the corpus's "complaint-tier" provenance tag. Verified via us.forums.blizzard.com Diablo Immortal General Discussion threads:
- "Druid still ruins the whole bg" (2025)
- "It's wrong to nerf druid" (post-Sept 2025 nerf)
- "Druid and higl sec stats bk still overperforms"
- "When Are We Addressing Major PvP Class Imbalances in Battlegrounds?" (Feb 2026)

**evidence quote (complaint pattern):** WebSearch result citing Sportskeeda: "In competitive high-resonance Battleground scenarios, a high-res Druid sitting on or under the idol stacks healing, damage reduction, shields, and constant pressure. This makes them particularly effective at objective denial in PvP matches." Community forum consensus (via search summary): "High-resolution Druids sitting on or under the idol stacked healing, damage reduction, shields, and constant pressure, with players describing it as 'fighting a zone' rather than a player."

**So the SHAPE the mob-harvester picked up is real** — a CC-dense objective-denial Druid PvP archetype. It just does not have a skill or state named "spirit form." The atlas_key `SDMFSI-HSMM-CD-PH-~~` encodes CD (control-density) + PH (physical primary element) correctly for this shape.

**NOTE for Elrond (per index.md recommendation):**

Preferred handling: **Option A + B together** (mirror the `d2-wl-void-rift` phantom precedent AND recover the real kit shape):

1. **Retain `di-spiritform-druid-pvp` row with `negative=1`** — provenance-integrity flag; update `mech_note` to record "phantom kit — mob-harvest v3 mis-naming; DI Druid class real, 'spirit form' mechanic does NOT exist; see legolas di-spiritform-recrawl-2026-07-17"; add flag `phantom-mob-harvest-v3` (or similar).
2. **Create a new clean row** — proposed kit_id `di-druid-pvp-cc-stack-2026` or similar (elrond's naming). Populate:
   - `folk_name`: "DI Druid PvP CC stack"
   - `ctrl_raw`: `stun-multi-source, slow, root/immobilize, knockback, damage-amp/marking, self-cc-immunity` (all landed vocab)
   - `elem_raw`: `physical, fire, earth` (mixed — Fire Tornado is fire, Earthquake/Landslide/Surging Stone are earth, most CC is physical)
   - source_urls: Blizzard official news post + Fandom + Blizzardwatch (per URLs above)
   - source_date: 2026-07-17 (this re-crawl date)
   - provenance_tag: `legolas-recrawl-v1-2026-07-17` or similar

If Option A + B is too heavy, minimum-viable is **Option A alone** (phantom flag + retain for mob-harvest-v3 audit signal). If prune-first is preferred, Option C (delete) works but loses the audit signal.

**Provenance-integrity finding — SECOND mob-harvest v3 phantom kit surfaced by post-hoc re-crawl:**

1. `d2-wl-void-rift` — surfaced by econ-recrawl-2026-07-16 (finding #1 in that sheet); D2/Destiny-2 ambiguity produced phantom kit
2. `di-spiritform-druid-pvp` — surfaced by this pass; DI-class-real-mechanic-phantom mis-naming

Both from `provenance_tag='mobile-harvest-v3'` with `source_date='2026-07-12'`. Recommend Elrond schedule a targeted mob-harvest v3 audit pass over remaining complaint-tier kits (SELECT ... WHERE provenance_tag='mobile-harvest-v3' AND corpus_bucket='canon' AND source_date='2026-07-12') to catch other name-shape mis-matches before they consume further re-crawl bandwidth. Estimated batch size: ~30-50 residual complaint-tier kits by rough mob-harvest v3 total.

---

**Row count check:** 1 row in this sheet. 1 marked `**phantom**`. Matches index summary block (0 classify / 0 new-shape / 0 unverifiable / 1 phantom = 1 total). No discrepancy.
