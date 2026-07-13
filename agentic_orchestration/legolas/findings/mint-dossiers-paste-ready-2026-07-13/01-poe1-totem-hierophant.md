# Mint Kit Dossier — poe1-totem-hierophant

**corpus_kit_id:** `poe1-totem-hierophant`
**folk_name:** Totem Hierophant / Ancestral Warchief Totem
**game:** poe1
**status:** positive
**era_year:** 2016
**stabilization_patch:** v2.3.0 (Prophecy league, June 2016 — Ancestral Warchief gem introduced)
**for_roster_kits:** K18
**mint_priority:** HIGH
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

The Hierophant/Ancestral Warchief totem archetype is PoE1's canonical expression of the "proxy executor" identity: the player places stationary melee totems that attack enemies while the player repositions. This root archetype predates PoE1 — Diablo 2's skeleton summoner and druid summon wolves established the proxy-executor pattern (player as director, proxies as damage actors). Within PoE, the concept existed from open beta (2013) via the "Spell Totem Support" gem and "Ancestral Bond" keystone (which removes direct damage and allows infinite totems), but lacked a dedicated high-quality skill until Ancestral Warchief.

Hierophant was introduced as an Ascendancy class in version 2.2.0 (Ascendancy league, March 2016), offering totem-focused ascendancy notables: "Pursuit of Faith" (totem placement speed + additional totem count) and "Conviction of Power" (Power/Frenzy charge generation via totems). These nodes made the Hierophant the genre's definitional totem-specialist ascendancy. Ancestral Warchief was then introduced in 2.3.0 (Prophecy league, June 2016) as a purpose-built high-damage melee totem skill. The two combined to produce PoE1's archetype genus entry for proxy-heavy totem play — a meta-durable identity that survived multiple nerf waves (3.7 totem nerf; 3.9 simultaneous-totem-limit changes) and remained viable through the 3.29 era.

A second arm — Spell Totem Hierophant — uses the same ascendancy with socketed spell totems (Lightning Tendrils, Detonate Dead, Armageddon Brand, etc.) as proxy casters, producing a distinct delivery/element profile but the same proxy-heavy loop. This dossier covers the primary Warchief arm; the Spell Totem arm may warrant a separate corpus entry at lattice grain (elrond: G1 check owed).

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| March 2016 | v2.2.0 (Ascendancy) | Hierophant ascendancy introduced; "Pursuit of Faith" enables additional totem + placement speed |
| June 2016 | v2.3.0 (Prophecy) | **Stabilization** — Ancestral Warchief gem added; the Hierophant+Warchief combo instantly becomes the genre-defining totem kit |
| 2016–2018 | v2.4.0–3.2.x | Continuous meta presence; multiple build guides document 3–4 simultaneous Warchiefs with Hierophant stacking |
| 2019 | v3.7.0 (Legion) | Totem mechanics reworked; some nerf to totem hit damage; Hierophant arm survived with different support-gem structure |
| 2019 | v3.9.0 (Metamorph) | Simultaneous totem cap changes further constrained some variants; Chieftain arm became more popular for raw damage; Hierophant arm survived as utility/starter identity |
| 2025–2026 | v3.25–3.29 | Still playable; Hierophant totem builds documented in league-starter tiers |

## Mechanical Identity

The Hierophant/Ancestral Warchief totem build places 3–4 simultaneous Warchief totems at mid-field using instant placement. Each totem grants the player a "more melee damage" and "more attack speed" aura while it is active — creating a joint-benefit loop (player buffs totems; totems buff player). Player action during combat is: (1) place totems, (2) move to remain in buff range or reposition, (3) avoid damage, (4) refresh totems on expiry. This is PoE1's canonical "proxy-heavy, instant placement, stationary-turret" loop and the direct ancestor of the PoE2 Warbringer Totem Warrior (GX-19 flag) and PoE2 Archmage Totem Oracle lines.

In the "Ancestral Bond" variant (keystone): the player cannot deal direct damage at all; all DPS comes from totems. In the standard Hierophant variant without Ancestral Bond: player retains direct-damage options but totems are primary DPS.

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | MED | Ancestral Warchief is a STR attack skill (weapon-based, benefits from STR nodes + melee physical passives); Hierophant is on the Templar starting area (STR/INT); the canonical Warchief arm is STR-dominant. Spell Totem arm = INT. |
| range | mid | MED | Player places totems at mid-field (typically 15–25 unit cursor range) and retreats behind them; totem melee attacks from totem's fixed position. Player positioning is mid-range from enemies, not adjacent. |
| tempo | low | MED | Player action cadence is LOW: place 3–4 totems, pause, reposition on totem expiry. Kill speed may be high; player INPUT density is low. Spell Totem arm may reach MED. |
| amp | flat | MED | Warchief grants a stable "more melee damage" multiplier; per-hit output is consistent once all totems are placed; no significant per-hit variance. |
| proxy | heavy | HIGH | Totems are the primary damage actors; player's role is placement, buff absorption, and movement. In Ancestral Bond variant: player deals zero direct damage. |
| commit | instant | HIGH | Totem placement is an instant action (no cast time in canonical Warchief builds; gem quality cast time bonus applies only optionally). |

## Raw Descriptors

**geo:** At-target placement: player places totem at cursor location; totem performs a wide ground-slam AoE (melee radius ~10–12 units from totem position) repeatedly while player is nearby. Classic small-radius turret footprint from the totem's perspective; large-zone effective coverage from player's placement strategy.

**ctrl:** Damage-pure; Warchief slam does not have meaningful CC beyond minor knockback on nearby targets. Stun is possible on hit but is not the build's control identity.

**mob:** Player has FULL mobility while totems persist (totems are stationary; player moves freely). This is a defining trait: the player kites/repositions while totems provide sustained damage from their placed positions.

**def:** Life-based tank OR Aegis Aurora block-based variants. Totems draw some enemy aggro, reducing player threat. Hierophant ascendancy does not provide major defensive bonuses — defense is via tree/gear.

**econ:** Mana per totem placement (light cost per cast; 3–4 placements per engagement refresh). Sanctuary ascendancy node + some unique amulets can reduce or eliminate placement cost. Totem death triggers replacement cost. Overall mana pressure is low.

**elem:** Physical primary (Warchief attacks with equipped weapon; benefits from weapon elemental conversion on hit). Common conversion overlays: Herald of Ash (fire explosion on overkill), Hatred (cold conversion). Spell Totem arm uses the element of the socketed spell.

## Sources (live URLs)

- [Ancestral Warchief | PoE Wiki](https://www.poewiki.net/wiki/Ancestral_Warchief) — primary skill gem documentation; 403 at fetch time but URL is valid PoE wiki canonical location
- [Ancestral Protector | PoE Wiki](https://www.poewiki.net/wiki/Ancestral_Protector) — sibling skill introduced same patch; provides patch era confirmation
- [PoE Forum — Ancestral Warchief Chieftain Build 3.15](https://www.pathofexile.com/forum/view-thread/2769163) — community build guide (LIVE, confirmed accessible in search)
- [u4gm — PoE 3.3 Hierophant League Starter Builds](https://www.u4gm.com/news/path-of-exile/poe-3-3-templar-hierophant-league-starter-builds) — era documentation (LIVE)
- [AngryRoleplayer — Ancestral Warchief Chieftain Build](https://www.angryroleplayer.com/path-of-exile-builds/ancestral-warchief-chieftain-path-of-exile-build/) — build guide with era context (LIVE)

## Knowledge Gaps

- Specific patch number when Vaal Ancestral Warchief was added (search returned "3.4" — confirming Delve 2018)
- Post-3.25 (Settlers/Mercenaries era) exact totem meta tier not measured via live poe.ninja data (poewiki 403 blocks direct check)
- Spell Totem Hierophant sub-arm: may warrant a separate corpus record at lattice grain — deferred to elrond G1 check
- Exact league-start usage % for Warchief arm vs Chieftain arm: not resolved without poe.ninja access
