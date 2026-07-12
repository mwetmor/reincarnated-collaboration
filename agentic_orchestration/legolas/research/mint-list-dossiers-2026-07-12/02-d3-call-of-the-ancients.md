# Dossier — d3 Call of the Ancients (IK Ancients Barbarian)

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** K5 (STR proxy-light anchor ancestor)
**Corpus gap confirmed:** `d3-ik-hota` exists in corpus but captures the HotA-primary variant; no record where the Ancients are the DEFINING proxy mechanism (K5 is proxy-LIGHT, which aligns with CotA as a force-multiplier alongside player attacks rather than pure proxy executor)
**Crawl date:** 2026-07-12

---

## Identity

**Game:** d3 (Diablo 3)
**Patch/era span:** Reaper of Souls (2.0, March 2014) through Season 39 (Patch 2.7.8, 2024+); Immortal King set reworked in Patch 2.4 to enable permanent Ancients uptime via Fury-spending; deep canon across 10+ years.
**Canon tier:** deep
**Folk names:** "IK Ancients," "IK CotA Barb," "Immortal King Call of the Ancients," "Ancients Barbarian"
**Shipped / negative-canon status:** SHIPPED — enduring top-tier Barbarian build across many seasons; one of the most iconic set-empowered archetypes in D3.

## Build identity (2–4 sentences)

The Immortal King's Call + Call of the Ancients build defines the "warrior-plus-warriors" proxy-light kit: the player Barbarian and three named Ancestral warriors (Talic, Korlic, Madawc) fight together as a joint force, each dealing 270% weapon damage per swing. The Immortal King 4-piece bonus reduces CotA and Wrath of the Berserker cooldowns by 3 seconds per 10 Fury spent, and the 6-piece provides 4,000% increased damage while both buffs are active — meaning the player's own Hammer of the Ancients is the primary spike while the Ancients provide sustained supplementary pressure. Unlike a heavy-proxy kit (where the player stands aside and lets proxies fight), the IK CotA player is always attacking alongside their Ancients, creating a LIGHT proxy coordination. The canonical K5 ancestor reading: the Ancients are a force-multiplier, not a substitute — the player's own presence is load-bearing.

## Lineage

**Ancestors:**
- D2: Barbarian War Cry / shouts that buff allies (non-proxy; support flavor)
- D2: Necromancer Skeleton Army (heavy proxy; the CONTRAST to CotA's light proxy)

**Descendants / related records:**
- poe1 "Warchief Totem" — shares the "warrior-proxy-who-fights-alongside-you" concept but moves to HEAVY proxy
- PoE2 Warbringer Totems (GX-19 evidence; "totem absorbs wind-up")
- D3: Raekor's Boulder Toss (separate IK variant; different primary skill)
- D3: IK HotA (already in corpus; captures the HotA-primary damage arm — this mint captures the PROXY-LIGHT characterization of the same set as a distinct lens)
- RDR: K5 Ancestor-Warrior cell `SMLSL_`

**Mint distinction from existing d3-ik-hota:**
The existing `d3-ik-hota` record characterizes the build through HotA as primary DPS. This record characterizes the CotA mechanism as the defining identity — the proxy-light coordination that makes K5 work. They may ultimately be the same corpus row with different lens-focus; Elrond decides on the merge/distinct ruling.

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | HIGH | Barbarian = STR archetype in D3; all Barbarian primary stats are STR |
| range | MELEE | HIGH | Hammer of the Ancients is a melee attack; the Ancients attack in melee; all engagement is at close range |
| tempo | HIGH | HIGH | HotA spamming with Bracers of the First Men grants very high attack speed; Fury-spending loop is rapid; high action density |
| amp | SPIKY | MED | 4,000% damage multiplier when both CotA and WotB are active = very large multiplier window; when cooldowns lapse (brief gap) damage drops dramatically. Builds with perfect Fury management maintain uptime but the mechanic is inherently spiky. |
| proxy | LIGHT | MED | Ancients deal 270% weapon damage per swing × 3 Ancients = substantial supplement but player's own HotA (amplified by the 6-piece to massive numbers) is still primary. LIGHT (not solo — Ancients are meaningful — but not HEAVY — player must attack). |
| commitment | INSTANT | HIGH | CotA is a cooldown cast (instant); HotA is a single melee attack hit (instant). No wind-up or channel in the primary loop. |

## Raw descriptors (not engine keys)

**geo:** Single-target melee slam (HotA ground impact); cone AoE on the slam; Ancients provide sweeping melee swings around the player position; effective at clustered enemies.

**ctrl:** Damage-pure; Ancients' attacks have no meaningful CC; HotA creates a brief stagger on impact but no sustained control.

**mob:** Moderate mobility; player attacks in place or near targets; no movement skill built into the core loop (Sprint/Leap Slam are optional utility). Cannot fight at range.

**def:** Toughness-heavy (max life + physical damage reduction via Berserker/Ignore Pain); Barbarain passive armor contribution. "Hammer of the Ancients Barbarian" — built to absorb hits, not evade them.

**econ:** Fury-based; primary resource is Fury (generated by attacks, spent by HotA); the Fury-spending mechanic maintains CotA/WotB cooldown reduction. No unusual econ: build is self-sustaining in the Fury loop once in combat.

**elem:** Physical primary (HotA ground smash; Ancients physical melee); some builds convert to fire via Cindercoat or rings, but physical is the canonical form.

## Sources

- Icy Veins D3 IK HotA guide (patch 2.7.8 / Season 39): https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king
- Maxroll D3 IK HotA guide (Season 39): https://maxroll.gg/d3/guides/ik-hota-barbarian-guide
- Knowledge base (kb) — IK set mechanics confirmed via training data
- V4-r2 §F4 mint-list (gandalf, 2026-07-12)

## Knowledge gaps

- The IK set's exact 6-piece bonus wording across patch versions varies; "4000%" is a Season 29+ figure — earlier seasons had different multipliers
- Exact DPS split between player's HotA and Ancients' attacks in current patch not measured (would confirm LIGHT vs HEAVY proxy call)
- "IK Charge" (Furious Charge primary variant) is a distinct build in the same set family — separate G1 check owed
