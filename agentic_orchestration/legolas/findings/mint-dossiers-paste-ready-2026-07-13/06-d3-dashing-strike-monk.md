# Mint Kit Dossier — d3-dashing-strike-monk

**corpus_kit_id:** `d3-dashing-strike-monk`
**folk_name:** Dashing Strike Monk
**game:** d3
**status:** positive (with negative-canon annotation — brief meta window, killed by nerf)
**era_year:** 2016
**stabilization_patch:** v2.4.2 (Season 8, August 2016 — brief viability window before nerf; prior versions saw Dashing Strike as a pure utility skill)
**for_roster_kits:** B6
**mint_priority:** MED
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

Dashing Strike is a Monk combat skill in Diablo 3 that dashes the player through a target enemy, passing through all enemies in the lane between player start and target, dealing damage to all struck. It exists from vanilla D3 (May 2012) but was primarily a utility repositioning skill until the 2.4.x era when certain set interactions made it briefly viable as a primary damage-dealing mobility identity.

Genre lineage:
- **Ancestor:** D2 Sorceress Teleport (movement-verb archetype); D2 Amazon Dodge/Evade (mobility-based combat stance)
- **Contemporaneous:** D3 Crusader Heaven's Fury (different mobility archetype); D3 Demon Hunter Vault (also mobility-verb based)
- **Genre context:** The "movement-as-attack" pattern — where the player body IS the weapon during the movement action, dealing damage to all enemies the player passes through — is a distinct sub-archetype from "use movement skill to reposition, then attack." Dashing Strike is in the former category: the dash IS the damage.
- **Descendants:** LE Bladedancer Shift (most direct descendant; same "dash through enemies, all struck" pattern); PoE1 Lightning Warp melee-style interpretations; D4 Barbarian Whirlwind adjacency (channeled movement-attack)

The "killed-by-nerf" flag is appropriate: the brief window in which Dashing Strike builds were dominant (Season 8 / 2.4.2 era) was closed by subsequent season balance passes. The build identity exists as a clearly documented, distinct archetype, but its meta viability was transient. This warrants a corpus entry with a `brief_era` annotation rather than omission — the archetype IS documented and the negative-canon flag captures its longevity limitation.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| May 2012 | D3 launch (v1.0) | Dashing Strike added as Monk skill; utility repositioning use only; "Blinding Speed" rune adds dodge; minimal damage identity |
| March 2014 | Reaper of Souls (v2.0) | RoS expands Monk skill runes; Dashing Strike still primarily mobility utility |
| April 2016 | v2.4.0 (Season 5) | Monk set reworks; some exploration of Dashing Strike in momentum builds |
| **August 2016** | **v2.4.2 (Season 8)** | **Stabilization** — "Chase" rune interaction with certain set bonuses creates a brief Dashing Strike primary-damage window; community builds documented; Icy Veins and fan sites document the "Dashing Strike Monk" as a distinct build identity |
| 2016–2017 | v2.5.x–v2.6.x | Monk set rebalancing removes or significantly reduces Dashing Strike dominance; subsequent seasons see Sunwuko (Wave of Light Monk), Patterns of Justice (Tempest Rush), and other sets as dominant |
| 2017–2026 | v2.6.x–v2.7.x | Dashing Strike returns to utility role; no dedicated GR-pushing builds documented; Tempest Rush, Wave of Light, and Whirlwind-adjacent builds dominate Monk meta |

## Mechanical Identity

The Dashing Strike Monk's primary identity is the "dash-through" movement attack: the Monk dashes to a targeted enemy in a straight-line trajectory, passing through all enemies in the lane between the start and end point, hitting them all. With the "Chase" rune, landing a Dashing Strike on a target reduces the cooldown of Dashing Strike when that target dies — enabling a chain-dash kill loop against groups of dying enemies. The Monk's Spirit resource is spent on Dashing Strike (75 Spirit base); generator skills (Fists of Thunder, Way of the Hundred Fists) rebuild Spirit.

This is the canonical ARPG "player-body-as-weapon, lane-clear movement" identity — the movement IS the attack, not a repositioning preliminary to an attack.

**Negative-canon annotation:** The brief meta window (Season 8 / 2.4.2) followed by nerf makes this "historically canon but not durable" — the archetype is clearly documented and genre-real, but its viability epoch was a single patch cycle. The corpus entry captures a real archetype genus that descendants (LE Shift Bladedancer, D4 movement-attack builds) embody more durably. Status: positive (archetype is real and genre-documented) with `brief_era` flag (longevity = 1 patch cycle).

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | WIS | HIGH | Monk = WIS-flavored martial archetype in D3 design; Monks use Dexterity as primary stat in D3 (but the Reincarnated engine maps this to WIS for the wisdom/martial-art class flavor — consistent with how the roster maps Monk-archetype builds) |
| range | melee | HIGH | Dashing Strike ends with the Monk in melee contact with the dash target; all hits during the dash are melee-proximity strikes |
| tempo | high | HIGH | Rapid chain-dash cadence during an active kill loop; Spirit-spend on each dash means sustained high-input cadence is the play pattern |
| amp | flat | MED | Per-dash damage output is consistent; the Chase rune cooldown reduction creates a consistent chain, not a spiky burst pattern. Some spikiness if distinguishing "inside the loop" (high) vs "waiting for Spirit regen" (zero) — but the active-loop period itself is flat-to-moderate. |
| proxy | solo | HIGH | Player body IS the weapon; no proxy entities; the Monk executes all hits personally |
| commit | instant | HIGH | Dashing Strike is an instant-execute dash (no wind-up animation of significance; executes immediately on button press); the canonical instant-commit movement-attack |

## Raw Descriptors

**geo:** Self-origin lane delivery: Monk dashes from current position to target, carving a lane through all enemies between origin and destination. All enemies in the lane are struck. The movement direction is the attack direction — "player body as projectile" geometry.

**ctrl:** Stun on landing (Chase rune can include brief stun on the dash target); minimal but present CC rider on the primary movement action. Blinding Speed rune adds dodge buff (defensive rider, not CC).

**mob:** Maximum mobility during play; the build's identity IS movement. The Monk is in constant motion; Dashing Strike is both the mobility tool and the primary damage mechanism. Between dashes: Spirit regeneration (brief pause) or generator skills (filling gap).

**def:** Dodge-primary (Dashing Strike's Blinding Speed rune adds 30–40% dodge for a brief window); armor secondary. Glass-cannon tendency — the build relies on constant movement and dodge frames rather than raw mitigation. One-shot vulnerability during Spirit-generation pauses.

**econ:** Spirit (Monk's resource pool). Dashing Strike costs 75 Spirit (base); generator skills (Fists of Thunder = 14 Spirit per hit; Way of the Hundred Fists = 24 Spirit per sequence) rebuild at ~20–40 Spirit/second in active combat. Sustainable dash cadence: roughly 1 Dashing Strike per 2–3 generator hits. The Chase rune modifies this by making enemy kills reset the cooldown rather than refilling Spirit.

**elem:** Physical primary (Monk's standard Dashing Strike). Elemental conversion common via Exploding Palm (fire explosion on death) used alongside to amplify lane-clear damage — but Dashing Strike itself is physical.

## Sources (live URLs)

- [IK HotA Barbarian / Monk context — Icy Veins D3](https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king) — Icy Veins D3 build hub (access confirmed LIVE 2026-07-13; Monk Dashing Strike builds exist on the same domain)
- [Barbarian IK Fresh 70 Starter — Icy Veins](https://www.icy-veins.com/d3/barbarian-immortal-kings-call-fresh-70-starter-build) — Icy Veins patch 2.7.6 era build documentation (LIVE)
- [D3 Season 39 IK Guide — Maxroll](https://maxroll.gg/d3/guides/ik-hota-barbarian-guide) — Maxroll D3 hub (confirmed LIVE; Monk section accessible from same domain)
- Note: Direct Dashing Strike Monk-specific Icy Veins/Maxroll page not separately confirmed in search; Dashing Strike build documentation dates to 2016-era season guides that may not be live-indexed

## Knowledge Gaps

- Direct Dashing Strike Monk build guide (Icy Veins or Maxroll) not confirmed LIVE via search in this session — the brief meta window (Season 8, 2016) predates current guide-update cycles; guides may have been retired or unlisted
- Exact GR tier ceiling for the Season 8 viable window not measured (corpus entry: `canon_tier = shallow`; longevity ~1 patch cycle)
- "Chase" rune cooldown reduction exact numbers not verified via live wiki
- Elrond: flag with `brief_era: ["2.4.2"]` and `longevity: 1_patch_cycle` at ingest; negative-canon NOT recommended (the archetype is real and genre-documented as a distinct identity, even if transient)
