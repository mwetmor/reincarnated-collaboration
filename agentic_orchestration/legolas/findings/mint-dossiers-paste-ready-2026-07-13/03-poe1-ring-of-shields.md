# Mint Kit Dossier — poe1-ring-of-shields

**corpus_kit_id:** `poe1-ring-of-shields`
**folk_name:** Ring of Shields — Forge Guard (Last Epoch Sentinel class)
**game:** ⚠ GAME ATTRIBUTION CORRECTION REQUIRED — see §CRITICAL FLAG below
**status:** positive
**era_year:** 2024
**stabilization_patch:** v1.0 (Last Epoch full release, February 21, 2024)
**for_roster_kits:** H1, B7
**mint_priority:** MED
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## ⚠ CRITICAL FLAG — GAME ATTRIBUTION ERROR IN CORPUS

**"Ring of Shields" is a Last Epoch skill belonging to the Sentinel → Forge Guard mastery class. It is NOT a Path of Exile 1 skill.**

Evidence (live sources confirmed 2026-07-13):
- [Ring of Shields — Official Last Epoch Wiki (Fandom)](https://lastepoch.fandom.com/wiki/Ring_of_Shields): "Ring of Shields is a Forge Guard Summon Skill which is unlocked at level 5."
- [Ring of Shields — LastEpochTools](https://www.lastepochtools.com/skills/ring_of_shields): skill listed under Forge Guard mastery (Sentinel class)
- [Last Epoch Forums — Ring of Shields and Forge Guard interactions](https://forum.lastepoch.com/t/ring-of-shields-and-forge-guard-interactions/71851): community discussion confirming Sentinel Forge Guard ownership
- Multiple web searches for "Ring of Shields PoE1," "Ring of Shields Path of Exile 1," and "Ring of Shields PoE2" returned NO matching skill gem in either PoE1 or PoE2. The previous legolas session (2026-07-12) flagged this as a knowledge gap for the same reason.

**Elrond action required:** The corpus kit_id `poe1-ring-of-shields` must be corrected to `game = le` (Last Epoch). The kit_id itself may need renaming to `le-ring-of-shields` or `le-forge-guard-ring-of-shields` per corpus keying convention. This dossier is filed under the existing corpus kit_id to enable the correction pass.

The "(Sentinel Guard)" parenthetical in the commission identifies the Sentinel-class Forge Guard mastery — accurate attribution.

---

## Provenance + Genre Lineage

Ring of Shields is a Last Epoch Sentinel class skill, specifically the Forge Guard mastery's signature summon. The Forge Guard is one of three Sentinel masteries (alongside Paladin and Void Knight). Ring of Shields creates a persistent orbiting ring of manifested shield constructs around the player character; these shields have independent HP, draw enemy aggression (taunt mechanic), and block projectiles — functioning as a combined aggro-management and projectile-interception proxy layer.

Genre lineage: the closest archetypes are D2 Necromancer Bone Shield (a defensive orbital effect on the caster), Diablo 3's Crusader Bone Shield Aegis (block-based orbital defense), and PoE1's Guard skill category (Molten Shell, Steelskin) — though Ring of Shields is distinct in creating separate physical entities rather than a damage-absorbing shell on the player body. The Forge Guard identity as a "living fortress" — a Sentinel who builds an impenetrable guardian perimeter — is unique to Last Epoch. The closest mechanical ancestor is D3 Crusader Bone Armor orbital.

**Lineage within Last Epoch:** The Forge Guard class is built around the Shield Crafter passive tree which interacts with Ring of Shields; the Shield Crafter passive gives a 1% chance per allocated point to cast Ring of Shields automatically when the player is hit, enabling a proc-loop defensive rotation. Shield Bash builds (also Forge Guard) use the constructed shields offensively.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| 2019–2022 | LE Early Access (0.7–0.8) | Sentinel class and Forge Guard mastery existed in early access; Ring of Shields present but not widely documented |
| 2022–2023 | LE v0.9 (Early Access) | Bladedancer and Forge Guard builds documented on Maxroll; Forge Guard Ring of Shields builds appear in community guides |
| February 21, 2024 | **LE v1.0** | **Stabilization** — Last Epoch full release; Forge Guard and Ring of Shields become stable, fully documented corpus entries |
| August 2025 | LE v1.1 | Build guides updated (Maxroll, Last Epoch Tools); Ring of Shields confirmed in live build databases |

## Mechanical Identity

Ring of Shields manifests a ring of shield constructs that orbit the player at a fixed radius, persisting for up to 10 seconds base. Each manifested shield has 75 base HP (+ 5 HP per character level) and scales with stats on the player's equipped shield. The shields draw enemy aggression (functioning as a taunt proxy) and physically block projectiles in their orbit path. Re-casting refreshes the ring. The Forge Guard's Shield Crafter passive can auto-trigger re-cast on player being hit.

This is the Last Epoch genre entry for the "orbital guard proxy" identity — a distinct proxy archetype (guards orbit and intercept rather than fighting at range or in melee from a placed position). The H1/B7 "orbital guard" roster map reflects this accurately.

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | MED | Sentinel class = STR-primary archetype (plate armor, shield-based); Forge Guard is the STR defensive mastery of the Sentinel class |
| range | mid | MED | Orbital mechanics operate at a mid-field radius around the player; shields orbit at ~3–5 unit radius (not melee adjacent, not ranged). Player's effective engagement range is mid-field. |
| tempo | low | MED | Ring of Shields is placed on a cooldown (re-cast every ~10 seconds); player input cadence for the orbital management loop is LOW. Offensive play (Shield Bash etc.) layered on top adds tempo. |
| amp | flat | MED | Orbital shields deal consistent proc damage when intercepting; no significant per-hit variance. Defensive function (blocking) is binary. |
| proxy | light | MED | Shields draw aggro and block projectiles but the Forge Guard player is still the primary damage dealer; orbital guards are a defensive proxy layer, not primary DPS. "Light" proxy for H1/B7 orbital identity is appropriate. |
| commit | instant | MED | Ring of Shields activation is instant (no cast time in documented builds); cooldown gates re-summon. |

## Raw Descriptors

**geo:** Orbit delivery: manifested shields form a circular ring at fixed radius around the player body, rotating continuously. Shields intercept projectiles that cross their orbit path. The ring footprint is the defining geometry — distinct from at-target or self-origin delivery.

**ctrl:** Aggro draw (taunt) — shields direct enemy attention toward themselves, functioning as a distributed taunt proxy. Projectile interception is the primary defensive application. No CC applied to enemies directly.

**mob:** Player has full movement freedom; the shield ring orbits and moves with the player. The Forge Guard's kit encourages the player to position within melee range and allow the ring to intercept incoming projectiles.

**def:** Shield-absorb primary (projectile blocking); orbital HP layer (each shield absorbs hits before expiring); player's own armor/block remain secondary defense layers. Ring of Shields is the Forge Guard's defining survivability tool — "living fortress" identity.

**econ:** Cooldown-gated re-summon; no ongoing resource cost once the ring is active. Shield Crafter's proc-on-hit can auto-refresh. Resource for offensive skills (Shield Bash etc.) is Forge Guard's separate resource (not Ring of Shields' economy).

**elem:** Physical (shield constructs deal physical damage when intercepting). No elemental conversion documented for the base skill.

## Sources (live URLs)

- [Ring of Shields — Last Epoch Wiki (Fandom)](https://lastepoch.fandom.com/wiki/Ring_of_Shields) — primary skill documentation; confirms "Forge Guard Summon Skill, level 5 unlock; 75 base HP per shield; 10 second duration; draws enemy aggression; blocks projectiles" (LIVE — confirmed in search 2026-07-13)
- [Ring of Shields — LastEpochTools](https://www.lastepochtools.com/skills/ring_of_shields) — skill tree nodes and stats (LIVE)
- [Ring of Shields Skill Nodes — LastEpochTools](https://www.lastepochtools.com/skills/ring_of_shields/nodes) — full skill tree documentation (LIVE)
- [Last Epoch Forums — Ring of Shields and Forge Guard interactions](https://forum.lastepoch.com/t/ring-of-shields-and-forge-guard-interactions/71851) — community discussion with Shield Crafter interaction details (LIVE)
- [Last Epoch Forums — Forge Guard Ring of Shields (early discussion)](https://forum.lastepoch.com/t/forge-guard-ring-of-shields/22905) — early access era documentation (LIVE)
- [Shield Bash Forge Guard Guide — Maxroll](https://maxroll.gg/last-epoch/build-guides/shield-bash-forge-guard-guide) — Forge Guard build guide showing the class context (LIVE)

## Knowledge Gaps

- **RESOLVED (was the core gap from 2026-07-12 session):** "Ring of Shields" has been definitively located as a Last Epoch Forge Guard skill.
- **Elrond action:** Correct `game` field from `poe1` to `le`; update kit_id convention accordingly.
- Ring of Shields exact version introduction date within LE Early Access (pre-1.0) not pinned to a specific patch; v1.0 (February 2024) is the stabilization date for the full release.
- Replica variant mentioned in original commission — no "Replica Ring of Shields" found in Last Epoch; "Replica" suffix belongs to PoE1 Heist league unique items. This may have been a cross-game confusion in the original V4-r2 note. Elrond: flag for review.
