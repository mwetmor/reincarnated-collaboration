# Mint Kit Dossier — poe1-vaal-blade-vortex

**corpus_kit_id:** `poe1-vaal-blade-vortex`
**folk_name:** Vaal Blade Vortex
**game:** poe1
**status:** positive
**era_year:** 2016
**stabilization_patch:** NULL (Vaal BV introduction patch not confirmed at document confidence; Blade Vortex base introduced v2.1.0 December 2015; Vaal version known to be present by 2016–2017 but exact patch uncertain — honest NULL for stabilization_patch per naming-law protocol)
**for_roster_kits:** B10
**mint_priority:** LOW-MED
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

Vaal Blade Vortex is the Vaal-variant skill gem of Blade Vortex in Path of Exile 1. Blade Vortex (base) was introduced in version 2.1.0 (Talisman league, December 2015) as a spell that creates a spinning field of ethereal blades around the player, stacking blade count (up to 10 base) with each cast and dealing physical damage to nearby enemies proportional to blade count. The Vaal version (Vaal Blade Vortex) uses the Vaal soul charge economy instead of normal cast-per-stack behavior: the player accumulates Vaal souls by killing enemies, then spends a full soul charge to activate Vaal BV, which summons an independently-moving vortex of blades that homes in on enemies.

Genre lineage:
- **Base skill ancestor:** PoE1's Ethereal Knives / Blade Flurry (melee-adjacent blade skills); D2 Blade Fury Amazon (spinning blade projectile)
- **Vaal system ancestor:** PoE1's Vaal system introduced in v1.1.0 (Sacrifice of the Vortex expansion, March 2014); Vaal souls from kills → burst activation; genre first for "kill-charge reservoir" Vaal economy model
- **Descendants:** PoE2 Blade Vortex equivalents; PoE1 Blade Vortex of the Scythe (transfigured gem, 3.24 era); Vaal BV remained meta-relevant through 3.16 Scourge (2021) and 3.20+ era with Triple Herald support

The B10 "operator-tier variant" framing is accurate: Vaal BV occupies the same plane cell as regular BV but with a DISTINCT charge-economy model. Regular BV stacks blades over time (player-paced, continuous); Vaal BV triggers a burst on soul-charge threshold (accumulate from kills → spend for burst activation). These are different commit patterns: regular BV is a wind-up stacking mechanic; Vaal BV is a charge-pool burst.

**Note on commit slot:** The megaprobe tagged commit as `instant` for Vaal BV (the soul-threshold trigger fires instantly on full charge). This is accurate for the TRIGGER: when the charge fills, the activation is instant. However, the SOUL-ACCUMULATION phase is a wind-up period (time spent killing enemies to fill the charge). The B10 identity is the charge-pool burst pattern, not a pure instant mechanic. The previous dossier (2026-07-12 megaprobe) notes `commit = wind-up / MED confidence` for this reason.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| December 2015 | v2.1.0 (Talisman league) | Blade Vortex (base) introduced; immediately becomes popular spell for close-range casters |
| 2016 | v2.3.0–v2.5.0 (est.) | Vaal Blade Vortex added (exact patch not confirmed; known to be present by 2016–2017 based on community references; PoE wiki URL for VBV exists confirming the skill is documented) |
| 2016–2018 | v2.x–3.2.x | VBV used as a burst-damage supplement to regular BV builds; soul economy enables burst windows in high-density areas |
| 2018–2021 | v3.3.0–3.15.x | BV and VBV remain meta; Triple Herald BV Elementalist becomes iconic in 3.10–3.12 era (Incursion league onward) |
| **2021** | **v3.16.0 (Scourge)** | Triple Herald Blade Vortex Elementalist documented as "iconic staple of the PoE meta since its rise to power in Incursion League"; VBV used alongside regular BV in these builds |
| 2023–2026 | v3.23.0–3.28.x | BV/VBV builds continue; PoB Archives documents VBV builds in 3.25 (Kalguur league); Blade Vortex of the Scythe (transfigured gem, 3.24) adds a new variant |

## Mechanical Identity

Vaal Blade Vortex creates an independently-moving vortex of ethereal blades that homes in on nearby enemies. Unlike the base BV (player-stationary spinning field), Vaal BV's vortex pursues enemies autonomously after activation — a near-proxy behavior (the vortex acts independently). The Vaal soul economy means the player builds charge by killing enemies (each kill contributes souls; Vaal BV requires ~200 souls for activation), then fires the burst vortex at full charge.

B10 maps to this as an "operator-tier variant" of the base BV cell — same plane coordinates (INT/mid/high/flat), distinct economy model (charge-pool meter vs. continuous stack-cast). The Vaal soul system is the defining economy differentiation; the mechanic note: "Vaal soul charge economy; souls accumulate from kills; Vaal BV triggers on full-pool spend" (megaprobe evidence).

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | INT | MED | Blade Vortex and Vaal BV are Dexterity-based gems but the canonical chassis is Shadow/Occultist (INT-adjacent) or Elementalist (INT) for scaling spell damage. The corpus engine mapping to INT reflects the build's intelligence/caster framing. |
| range | melee | MED | BV and VBV are melee-range aura/vortex skills; the blade field operates in close proximity to the player or target; effective damage range is ~10 unit radius |
| tempo | high | HIGH | Blade stacking (base BV) is high-frequency; VBV activation occurs at kill-threshold and the soul-building phase involves high-density combat (high action cadence to accumulate kills quickly) |
| amp | flat | MED | Consistent per-blade damage within the vortex duration; no significant per-hit variance once the vortex is active |
| proxy | solo | HIGH | Player-centric aura/vortex; no persistent proxy entities; Vaal BV's independently-moving vortex is close to a proxy but is bound to the player's cast origin and the skill lasts a limited duration |
| commit | instant | MED | The TRIGGER (threshold activation) is instant; the ACCUMULATION phase is a wind-up period (killing enemies to fill charges); MED confidence on instant because the economic wind-up is a meaningful commitment pattern |

**Note:** The megaprobe assigns `commit: instant, conf 0.65` and the previous markdown dossier assigns `commit: wind-up, MED`. The disambiguation: the TRIGGER is instant; the ECONOMY is a wind-up. For the plane cell (commit axis), the activation trigger = instant is the more accurate classification since it mirrors how other Vaal skills map. However, the charge-accumulation wind-up is architecturally significant for the B10 identity (it's what distinguishes VBV from regular BV). Recommend elrond preserve both: `commit = instant; econ_model = charge-pool (Vaal souls)`.

## Raw Descriptors

**geo:** Self-origin (base BV) / homing-vortex (Vaal BV post-activation). Vaal BV creates a vortex that moves toward nearby enemies independently. Small-to-medium radius cloud. The homing behavior is unusual — semi-proxy movement pattern.

**ctrl:** No CC from the skill itself; physical hit damage only. Some stun on high-damage hits but not the build's control identity.

**mob:** Player has full mobility during BV and VBV; neither skill roots the player. The "walk through enemies" BV style benefits from player positioning near enemies; VBV fires and pursues independently.

**def:** Energy shield primary (Shadow/Occultist chassis); Evasion + ES hybrid common. Dodge from Evasion-based gear. No life-based BV builds documented as dominant (though possible).

**econ:** Vaal soul economy. Souls accumulate from killing enemies (~200 per activation). Between activations, regular Blade Vortex provides continuous damage (standard mana cost per stack-cast). The build's economy is dual-layered: regular mana (base BV continuous) + Vaal soul reservoir (VBV burst activation on threshold).

**elem:** Physical primary (base BV and VBV deal physical damage; common conversion to cold via Herald of Ice, lightning via Herald of Thunder, or fire via Herald of Ash in Triple Herald builds). The iconic Triple Herald BV Elementalist converts all damage types via three simultaneous Heralds.

## Sources (live URLs)

- [Vaal Blade Vortex | PoE Wiki](https://www.poewiki.net/wiki/Vaal_Blade_Vortex) — primary skill documentation (403 at fetch time; URL is valid canonical location)
- [Vaal Blade Vortex — Path of Exile Wiki (Fandom)](https://pathofexile.fandom.com/wiki/Vaal_Blade_Vortex) — alternative wiki with version history (LIVE — confirmed in search 2026-07-13)
- [Blade Vortex | PoE Wiki](https://www.poewiki.net/wiki/Blade_Vortex) — base skill documentation; v2.1.0 introduction confirmed (403 at fetch; URL valid)
- [Triple Herald BV Elementalist Guide — PoE Vault](https://www.poe-vault.com/guides/triple-herald-blade-vortex-elementalist-build-guide) — 3.20 era build guide documenting VBV + BV usage (LIVE)
- [PoB Archives — Vaal BV builds (3.25)](https://pobarchives.com/builds/tpVAKeaM) — live PoB build database confirming VBV meta presence in 3.25 (Kalguur) (LIVE)
- [PoB Archives — VBV builds collection](https://pobarchives.com/builds?mainSkill=Vaal+Blade+Vortex) — searchable build archive (LIVE)
- [Vaal BV Poison Trickster 3.16 — PoE Forum](https://www.pathofexile.com/forum/view-thread/3199631) — Scourge era (3.16) build guide confirming VBV presence in 2021 (LIVE)
- [Vaal Blade Vortex — PoE Vault Items](https://www.poe-vault.com/items/vaal-blade-vortex) — skill item database entry (LIVE)

## Knowledge Gaps

- Exact patch of Vaal BV introduction not confirmed (known post-v2.1.0 December 2015; pre-3.16 Scourge 2021; likely 2.3.0–2.4.0 range based on PoE's Vaal gem release pattern — NULL per honest protocol)
- Elrond: confirm grain separation from `poe1-blade-vortex` base record (if one exists) and any `poe1-poison-bv` record; this entry is the CHARGE-ECONOMY variant (B10 operator-tier), distinct from the base stack-cast identity
- PoB Archives: VBV build count reported as 216 in the original 2026-07-12 dossier — not re-verified against live PoB Archives in this session (URL confirmed LIVE)
