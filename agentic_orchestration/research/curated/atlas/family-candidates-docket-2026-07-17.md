# Family Candidates — Discovery Docket (Atlas Edition IV, 2026-07-17)

**Status:** provisional · **names_review_pending:** TRUE · **served_layer:** provisional-islands (galadriel-rendered, visually distinct)
**Date:** 2026-07-17 · **Author:** elrond (data steward) · **Seed:** 20260717
**Charge:** Matt 2026-07-17 — add potential build-family islands to The Build Horizon (E4 ratified)
**Generator:** `agentic_orchestration/research/scripts/atlas_family_candidates_2026_07_17.py`

> **Purpose.** Provisional candidate rosters for six discovery-docket working families, with **per-sub-cluster tau** so propagation NEVER leaps Leiden chains — the exact defect that shelved the 2026-07-16 archipelago mock (global tau=0.80 umbrella).
> **Precision target.** Matt's names-level review, one complete sitting, >=80% precision over >=20 proposals. Below: self-scored per docket; Matt scores at review.

## 1. READ-ONLY PROOF (585-row conservation, corpus md5)

| item | value |
|---|---|
| `corpus.db` md5 (start) | `48a1f90c407826e438aa5f53ef45215f` |
| `corpus.db` md5 (end)   | `48a1f90c407826e438aa5f53ef45215f` |
| match  | YES |
| `canon_corpus` row count | 585 (585-row conservation) |
| `canon_corpus` kit-grain rows | 563 |
| E4 points (served plate) | 562 |
| `atlas-edition4.json` emitted_at | `2026-07-17T02:42:46.614907+00:00` |

## 2. METHOD (why this fixes the wave-4 defect)

**Full-space evidence.** Each E4 kit → an L2-normalized one-hot mech-fingerprint over eight ratified `canon_engine_key` axes (`geometry_value`, `delivery_value`, `ctrl_function`, `ctrl_treatment`, `def_bin`, `economy_model`, `activation_val`, `dependency_val`) plus two engagement proxies (`geo_raw`, `mob_raw`). This is the ratified full-space evidence — the same axes the engine-key layer is built on, NOT the 2D plate.

**Sub-clusters.** 506 kits have an E1-ratified `leiden_cluster` (2026-07-14 derivation, resolution 0.3, 60-seed consensus). 56 post-E1 kits (mostly LA, a handful d3/d4/di) are forward-extended by mech-fingerprint nearest-neighbor to an E1 kit's cluster — a defensible extension because E1 Leiden was derived from the same ratified mech-axis material.
  - in E1 leiden map: 469 / 562
  - extended via NN: 93
  - distinct Leiden sub-clusters: 153

**Per-sub-cluster tau.** For each docket D and each Leiden sub-cluster c that carries at least one seed of D:
  - if chain has >=2 D-seeds: `tau_D_c = min(P75 of intra-chain seed-seed distance, GLOBAL_TAU_CEIL=1.05)`
  - if chain has exactly 1 D-seed: `tau_D_c = min(P50 of ALL intra-docket seed-seed distances, GLOBAL_TAU_CEIL)` — a docket-typical fallback radius.
A non-seed kit k is PROPOSED for D iff `cluster(k)` is in D's chains AND `dist(k, nearest-D-seed-in-cluster(k)) <= tau_D_cluster(k)`. **NEVER propagates across chains.** This is the fix.

**Distance scale note.** Mech-fingerprint distances are on a Hamming-derivative scale (L2 of concatenated one-hot / sqrt(n_axes)). Empirical intra-family P90 for ratified families is 0.80-1.10 (max theoretical sqrt(2)~=1.41). The GLOBAL_TAU_CEIL=1.05 is a permissive ceiling — the per-chain / no-cross-cluster-leap discipline is what fixes the wave-4 defect (global tau=0.80 umbrella across all six families' terrain), not aggressive absolute tightening.

**Conflict rule.** A kit already in a ratified `gateA_group` (different from the docket's target) is NEVER proposed; if it's within tau, we conflict-flag LOUDLY (this is the row-integrity discipline: kits do not become members of two families).

## 3. DOCKETS (rosters + credentials)

### Docket 1 — MELEE-STRIKE

- **Seed criterion:** canon_engine_key.geometry_value = 'melee_strike'
- **Axis-signature requirement:** geometry_value = 'melee_strike'
- **Method note:** seeds = ratified geometry_value='melee_strike' kits from canon_engine_key (n=37 in E4, 34 after removing ratified-gateA members); the axis signature is REQUIRED for propagation admits, so a close-neighbor without melee_strike is NOT admitted
- **Self-scored precision:** 0.899  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 20/21 = 0.952 (leave-one-out admit rate on chain seeds)
  - Coherence: 0.944 = 1 - conflict_rate (2/36)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 10 | 1 | 0.8944 |
| 11 | 1 | 0.8944 |
| 14 | 1 | 0.8944 |
| 15 | 5 | 0.7746 |
| 18 | 3 | 0.8944 |
| 29 | 4 | 0.6325 |
| 40 | 1 | 0.8944 |
| 43 | 2 | 0.4472 |
| 46 | 1 | 0.8944 |
| 48 | 1 | 0.8944 |
| 52 | 2 | 0.7746 |
| 57 | 3 | 0.7035 |
| 69 | 1 | 0.8944 |
| 77 | 1 | 0.8944 |
| 85 | 2 | 0.6325 |
| 102 | 1 | 0.8944 |
| 103 | 1 | 0.8944 |
| 121 | 1 | 0.8944 |
| 148 | 1 | 0.8944 |
| 149 | 1 | 0.8944 |

- **Roster:** 36 total (0 ratified-seed, 36 proposed, 2 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `hades1-aspect-chiron` | proposed | 10 | 0.0 | 0.0 | `hades1-aspect-chiron` | TRAP-MINE (0.8938) | - | geo=melee_strike / deliv=projectile / ctrl=none/damage / econ=finite / dep=build→spend / act=triggered / note: "Mark-consume loop: attack → mark → specials auto-seek → repeat. The bow's aiming becomes irrelevant once mark is established; specials find the target regardless. AM..." |
| `d2-fireclaw-wolf` | proposed | 11 | 0.0 | 0.0 | `d2-fireclaw-wolf` | TOTEM-SENTRY (0.7597) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Werewolf whose claws deal fire via Fire Claws synergy stack — form-shift melee wearing an elemental damage identity." |
| `tq2-stormblade-ice-shards` | proposed | 14 | 0.0 | 0.0 | `tq2-stormblade-ice-shards` | CHANNELED-BEAM (0.9532) | - | geo=melee_strike / deliv=projectile / ctrl=hard-stop/damage / econ=spend / dep=one-shot / act=active / note: "POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. Cold projectile caster; 'Stormblade' suggests Storm/Blade mastery combo in TQ2. All details from atlas key provenance." |
| `gd-retaliation-warlord` | proposed | 15 | 0.0 | 0.0 | `gd-retaliation-warlord` | AURA (0.8515) | - | geo=melee_strike / deliv=aura-pulse / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Damage by BEING HIT — stacked retaliation stats reflected on every enemy swing, plus 'retaliation added to attack' converting the thorns wal" |
| `d2-conc-barb` | proposed | 15 | 0.0 | 0.0 | `d2-conc-barb` | TOTEM-SENTRY (0.7317) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Uninterruptible defensive single-target swing; the safe-melee identity and hardcore staple." |
| `d3-invoker-thorns` | proposed | 15 | 0.0 | 0.0 | `d3-invoker-thorns` | AURA (0.8515) | - | geo=melee_strike / deliv=aura-pulse / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Damage BY being hit — Invoker converts the Thorns stat into the whole offense; stand in the crowd, punish every swing against you; the defen" |
| `d2-avenger` | proposed | 15 | 0.0 | 0.0 | `d2-avenger` | TOTEM-SENTRY (0.8576) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Vengeance melee converts each swing into tri-element damage under Conviction — the immunity-proof melee answer." |
| `d2-berserker` | proposed | 15 | 0.0 | 0.0 | `d2-berserker` | CHANNELED-BEAM (0.8418) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Berserk converts to magic damage at the cost of zero defense while swinging — the all-in single-target trade." |
| `tq-onslaught-assassin` | proposed | 18 | 0.0 | 0.0 | `tq-onslaught-assassin` | TRAP-MINE (0.8229) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=build→spend / act=triggered / note: "Onslaught = Warfare mastery's signature melee skill (3 rapid strikes per activation). Dual-wield synergizes with Rogue's dual-wield bonuses. Warfare STR + Rogue DEX = Assassin..." |
| `gd-righteous-fervor-dervish` | proposed | 18 | 0.0 | 0.0 | `gd-righteous-fervor-dervish` | TOTEM-SENTRY (0.7919) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=build→spend / act=active / note: "The Oathkeeper's stacking default attack — Righteous Fervor ramps a fervor meter as you swing, acid conversions and WPS filling the gaps; ra" |
| `tli-erika3-vendetta` | proposed | 18 | 0.0 | 0.0 | `tli-erika3-vendetta` | TOTEM-SENTRY (0.9672) | - | geo=melee_strike / deliv=at-target / ctrl=hard-stop/damage / econ=spend / dep=build→spend / act=active / note: "POST-CUTOFF: TLI ss11-12-2026. Erika Season 3 variant (2026 season content). All conf ≤0.50. Cold melee kit per atlas key. Details unverified." |
| `d2-frenzy-barb` | proposed | 18 | 0.8944 | 0.7746 | `tq-onslaught-assassin` | TRAP-MINE (0.7032) | TRAP-MINE | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=free / dep=build→spend / act=triggered / note: "Dual-wield attack-speed stacker: Frenzy hits ramp self-haste; momentum melee limited by physical-immune density." |
| `tq-thane-storm-warfare` | proposed | 29 | 0.0 | 0.0 | `tq-thane-storm-warfare` | TOTEM-SENTRY (0.7813) | - | geo=melee_strike / deliv=at-target / ctrl=knockback/damage / econ=spend / dep=one-shot / act=active / note: "Thane is Warfare+Storm — the lightning-infused warrior archetype. Thunderous Strike = proc-based lightning burst on melee hits (proc model). Old econ code MT may mean..." |
| `tq-dream-harbinger` | proposed | 29 | 0.0 | 0.0 | `tq-dream-harbinger` | MINION-PET (0.7902) | - | geo=melee_strike / deliv=at-target / ctrl=stun/damage / econ=reserve / dep=one-shot / act=active / note: "RS old code = 'reserve-sustain'; captured as reserve here for Dream passive buffs. Sustain-leech in defense captures Dream's Dream Steal (life drain component). Harbinger is..." |
| `tq-rune-weapon-thunderer` | proposed | 29 | 0.0 | 0.0 | `tq-rune-weapon-thunderer` | TOTEM-SENTRY (0.7317) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=reserve / dep=one-shot / act=active / note: "Ragnarok expansion class. Rune Weapon = reserve-economy toggle that enchants physical attacks with lightning. Economy model = reserve (ongoing EPS cost). The 'Thunderer' name labels..." |
| `chr-bleed-berserker` | proposed | 29 | 0.0 | 0.0 | `chr-bleed-berserker` | TOTEM-SENTRY (0.6785) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Damage_mode=dot (bleed is the damage engine). Low tempo (L) is the key distinction — fewer but harder strikes that each apply max bleed stacks efficiently...." |
| `gd-cadence-witchblade` | proposed | 40 | 0.0 | 0.0 | `gd-cadence-witchblade` | TOTEM-SENTRY (0.7202) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=finite / dep=apply→detonate / act=active / note: "Every third swing DETONATES — Cadence's rhythm melee under Occultist curses, the 2016 launch's definitive physical bruiser and the template " |
| `d3-raiment-shenlong` | proposed | 43 | 0.0 | 0.0 | `d3-raiment-shenlong` | TOTEM-SENTRY (0.7919) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=build→spend / act=active / note: "Lightning-punch generator monk under Shenlong's spirit-dump rhythm — build spirit to the cap, the fist weapons ignite it into a damage windo" |
| `gd-savagery-warder` | proposed | 43 | 0.0 | 0.0 | `gd-savagery-warder` | TOTEM-SENTRY (0.8023) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=build→spend / act=active / note: "The two-handed lightning ramp — Savagery charges stack with every swing until the maul hums; Shaman's auto-attack identity under Soldier's s" |
| `d2-maul-bear` | proposed | 46 | 0.0 | 0.0 | `d2-maul-bear` | TRAP-MINE (0.6316) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=free / dep=one-shot / act=triggered / note: "Bear form stacks Maul damage charges per hit; slow heavy swings, tank identity, the other half of the form-shift family." |
| `le-smite-paladin` | proposed | 46 | 0.8944 | 0.6325 | `d2-maul-bear` | TRAP-MINE (0.6106) | TRAP-MINE | geo=melee_strike / deliv=at-target / ctrl=stun/damage / econ=free / dep=one-shot / act=triggered / note: "prov=let;kb. mech_note ref: 'Bolts of holy lightning called down on every trigger the tree can wire — smite-on-hit, smite-on-throw, smite raining from procs.' LI suffix..." |
| `vs-thunder-loop` | proposed | 48 | 0.0 | 0.0 | `vs-thunder-loop` | TRAP-MINE (0.9412) | - | geo=melee_strike / deliv=at-target / ctrl=stun/damage / econ=finite / dep=one-shot / act=active / note: "Double-hit per bolt ('loop') is the evolved mechanic: base Lightning Ring hits once; Thunder Loop hits twice per bolt. 'Off-screen artillery you neither aim nor..." |
| `poe2-snipe-mirage-deadeye` | proposed | 52 | 0.0 | 0.0 | `poe2-snipe-mirage-deadeye` | CHANNELED-BEAM (0.893) | - | geo=melee_strike / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "POST-CUTOFF. prov=kb. mech_note ref: 'Snipe's channeled shot one-taps bosses while Mirage Deadeye lets clones continue sniping.' Full dossier required." |
| `tq-ranger-hunting-nature` | proposed | 52 | 0.0 | 0.0 | `tq-ranger-hunting-nature` | MINION-PET (0.8256) | - | geo=melee_strike / deliv=projectile / ctrl=none/damage / econ=reserve / dep=one-shot / act=active / note: "Light proxy (L) distinguishes from Petmaster (heavy proxy): Ranger's arrows are the primary damage source; wolves supplement. SU economy in old code = sustain/nature; here..." |
| `tli-rosa-unsullied` | proposed | 57 | 0.0 | 0.0 | `tli-rosa-unsullied` | TOTEM-SENTRY (0.8478) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "A hero that doesn't exist in my training — Rosa's Unsullied Blade trait tops the current Supreme Showdown data across three regions, with Ho" |
| `tq-warlock-poison-vitality` | proposed | 57 | 0.0 | 0.0 | `tq-warlock-poison-vitality` | TOTEM-SENTRY (0.8329) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Econ=RS in old code = 'reserve-sustain' (hybrid). Spirit tree may add reserve-based aura (Phantom Lancer) or vitality leech. Vitality in folk_name captures Spirit's life steal...." |
| `gd-belgothian-blademaster` | proposed | 57 | 0.0 | 0.0 | `gd-belgothian-blademaster` | TOTEM-SENTRY (0.872) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=one-shot / act=active / note: "The dual-wield auto-attacker whose damage lives in the WPS pool — weapon-pool skills firing off default swings while the Belgothian set auth" |
| `d2-smiter` | proposed | 69 | 0.0 | 0.0 | `d2-smiter` | TRAP-MINE (0.8437) | - | geo=melee_strike / deliv=at-target / ctrl=stun/damage / econ=free / dep=one-shot / act=active / note: "Smite shield-bashes with auto-hit, stun, and crushing-blow percent-HP shred — THE uber-boss executioner role build." |
| `d3-s6-impale` | proposed | 77 | 0.0 | 0.0 | `d3-s6-impale` | TOTEM-SENTRY (0.8229) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Shadow's Mantle turns Impale into a single-target execution profession — melee-range knife throws deleting elites while trash is someone els" |
| `d2-zealot` | proposed | 85 | 0.0 | 0.0 | `d2-zealot` | TRAP-MINE (0.8229) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=free / dep=one-shot / act=active / note: "Zeal locks a five-hit melee flurry per click under self-Fanaticism; commitment-locked swing sequence, weapon-scaled." |
| `poe2-rake-ritualist` | proposed | 85 | 0.0 | 0.0 | `poe2-rake-ritualist` | TOTEM-SENTRY (0.8624) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "prov=kb. mech_note: 'Rake dash-slash stacks aggravated bleeds while Ritualist blood mechanics multiply the bleed count per dash.' damage_mode=dot (bleed is the primary damage, not initial..." |
| `d2-daggermancer` | proposed | 102 | 0.0 | 0.0 | `d2-daggermancer` | TOTEM-SENTRY (0.8576) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Poison Dagger melee necromancer made semi-real by 2.4 — a shallow-canon curiosity proving the buff-promotes-build pattern." |
| `d2-enchantress` | proposed | 103 | 0.0 | 0.0 | `d2-enchantress` | TOTEM-SENTRY (0.8768) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=cooldown / dep=one-shot / act=active / note: "Enchant converts the sorceress (and party/mercenary) into fire-melee attackers; self-buff-as-build plus external scaling — the buff-economy " |
| `hades1-beowulf-cast` | proposed | 121 | 0.0 | 0.0 | `hades1-beowulf-cast` | TRAP-MINE (0.8591) | - | geo=melee_strike / deliv=projectile / ctrl=stun/damage / econ=finite / dep=one-shot / act=triggered / note: "Ammo economy (AM): the bloodstone becomes ammunition. Retrieval loop = melee-bass the lodged enemy to get bloodstone back. Distinctive: ammo-retrieve forces engagement with the target..." |
| `tl2-wolf-shade-berserker` | proposed | 148 | 0.0 | 0.0 | `tl2-wolf-shade-berserker` | TRAP-MINE (0.8015) | - | geo=melee_strike / deliv=at-target / ctrl=knockback/damage / econ=generator-spender / dep=one-shot / act=triggered / note: "Economy=meter with builder_source=on_hit captures the Charge mechanic precisely. 'Multi-trigger' (MT old code) = proc on Charge activation — Wolf Shade appearance is a proc event...." |
| `tli-carino2-lethal-flash` | proposed | 149 | 0.0 | 0.0 | `tli-carino2-lethal-flash` | CHANNELED-BEAM (0.9763) | - | geo=melee_strike / deliv=projectile / ctrl=none/damage / econ=finite / dep=one-shot / act=active / note: "The Lunaria rework gave Carino's projectiles AUTOMATIC RETURN and an AMMO economy — shotgun volleys that fly back through the pack while res" |


### Docket 2 — IDENTITY-GAUGE

- **Seed criterion:** canon_engine_key.economy_model = 'identity-gauge'
- **Axis-signature requirement:** economy_model = 'identity-gauge' (the LA-cohort archetype)
- **Method note:** seeds = ratified economy_model='identity-gauge' kits (n=31, 31 after ratified-gateA removal); the tight LA-identity-gauge signature; broader dependency_val='build→spend' would balloon to 100+ and drown one-sitting review
- **Self-scored precision:** 0.967  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 29/30 = 0.967 (leave-one-out admit rate on chain seeds)
  - Coherence: 1.0 = 1 - conflict_rate (0/31)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 8 | 6 | 0.6325 |
| 9 | 9 | 0.0000 |
| 20 | 15 | 0.6325 |
| 31 | 1 | 0.4472 |

- **Roster:** 31 total (0 ratified-seed, 31 proposed, 0 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `la-taijutsu-scrapper` | proposed | 8 | 0.0 | 0.0 | `la-taijutsu-scrapper` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Taijutsu emphasizes direct skill uptime using TS identity bonuses (rather than Shock Training's gauge-spend structure); faster animations and consistent mobile damage; the 'simpler' Scrapper identity..." |
| `la-rage-hammer-destroyer` | proposed | 8 | 0.0 | 0.0 | `la-rage-hammer-destroyer` | TOTEM-SENTRY (1.0298) | - | geo=vortex_pull / deliv=at-target / ctrl=pull/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Same 3-core builder-spender loop as Gravity Training but identity use is optional and forfeited for sustained Gravity Release skill damage; Seismic Hammer, Perfect Swing, Earth..." |
| `la-asuras-path-breaker` | proposed | 8 | 0.0 | 0.0 | `la-asuras-path-breaker` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Alternates Stamina/Shock skills to generate meter and enter Asura Destruction state, unleashing a rush of punches; Defensive Speculation shield unique to Asura's Path provides survivability;..." |
| `la-robust-spirit-soulfist` | proposed | 8 | 0.0 | 0.0 | `la-robust-spirit-soulfist` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Robust Spirit allows bursting into Level 3 Hype immediately, making all damage buffs available in a short window; maintains steady DPS between windows with Hype..." |
| `la-energy-overflow-soulfist` | proposed | 8 | 0.0 | 0.0 | `la-energy-overflow-soulfist` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Inner Energy never drops below 1 with Energy Overflow so skills never shut down mid-rotation; high attack and move speed enable constant aggressive uptime; forgiving..." |
| `la-shock-training-scrapper` | proposed | 8 | 0.0 | 0.0 | `la-shock-training-scrapper` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Generates Shock Gauge via normal skills then spends it on powerful Shock Skills for burst damage; the builder-spender Scrapper versus Taijutsu's identity-uptime approach; more gauge..." |
| `la-berserkers-technique` | proposed | 9 | 0.0 | 0.0 | `la-berserkers-technique` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Fills Fury Meter through normal skills then enters timed Burst Mode for +30% crit rate, +20% attack speed, +36% damage, immune to Exhaustion on exit;..." |
| `la-igniter-sorceress` | proposed | 9 | 0.0 | 0.0 | `la-igniter-sorceress` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Fills Arcane Meter via generator skills then releases Arcane Rupture (Z) burst window granting shortened cast times and +18% elemental skill damage; burst window demands..." |
| `la-deathblow-striker` | proposed | 9 | 0.0 | 0.0 | `la-deathblow-striker` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Generates 3 Esoteric Orbs via skill use then consumes all 3 for Deathblow Esoteric Skills dealing maximum burst damage; strict 3-orb gate makes every cycle..." |
| `la-predator-slayer` | proposed | 9 | 0.0 | 0.0 | `la-predator-slayer` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Builds Fatigue stacks during Burst Mode to reduce Exhaustion duration, enabling prolonged Burst Mode uptime; Swiftness-based back-attack playstyle with spammy rotations while in Burst; the..." |
| `la-brawl-king-storm-breaker` | proposed | 9 | 0.0 | 0.0 | `la-brawl-king-storm-breaker` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Uses Stamina skills to generate Shock gauge, expends all Shock at once for powerful burst blows; non-positional (attacks from any angle); burst compressed into a..." |
| `la-barrage-enhancement-artillerist` | proposed | 9 | 0.0 | 0.0 | `la-barrage-enhancement-artillerist` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Removes Exhaustion from exiting Barrage Mode, allowing consistent re-entry for massive burst damage; blasts all damage in a few seconds like Igniter/Full Moon Souleater; non-positional..." |
| `la-punisher-slayer` | proposed | 9 | 0.0 | 0.0 | `la-punisher-slayer` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Maximizes damage within Burst Mode while accepting shorter Burst Mode duration; Specialization-scales more aggressively than Predator for burst payoffs; the build-spend Slayer versus Predator's sustained..." |
| `la-mayhem-berserker` | proposed | 9 | 0.0 | 0.0 | `la-mayhem-berserker` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Enters permanent Burst Mode locking HP at 25% of max for -60% healing, gaining 18% damage and 15% attack/move speed; rotation delivers burst inside the..." |
| `la-esoteric-flurry-striker` | proposed | 9 | 0.0 | 0.0 | `la-esoteric-flurry-striker` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Esoteric Flurry enables spending single Esoteric Orbs for enhanced multi-hit skill barrages rather than Deathblow's 3-orb all-or-nothing gate; higher orb generation and more consistent sustained..." |
| `la-grace-empress-arcanist` | proposed | 20 | 0.0 | 0.0 | `la-grace-empress-arcanist` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Stacks 4 Ruin marks on a target via normal skills then detonates with Ruin Skill for amplified burst; draws Card Deck between stacks to gain..." |
| `la-wind-fury-aeromancer` | proposed | 20 | 0.0 | 0.0 | `la-wind-fury-aeromancer` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Sun Shower lasts 8 seconds and boosts ally attack/move speed by 12%; Supersonic Breakthrough skill requirement makes Wind Fury sharper for coordinated burst windows and..." |
| `la-death-strike-sharpshooter` | proposed | 20 | 0.0 | 0.0 | `la-death-strike-sharpshooter` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Builds Hawk Meter rapidly via Death Strike passive to deploy Silverhawk Assault (Z) frequently, maintaining a damage debuff on target for maximum uptime; burst cycle..." |
| `la-order-emperor-arcanist` | proposed | 20 | 0.0 | 0.0 | `la-order-emperor-arcanist` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Boosts Card Deck meter gain and adds Emperor, Royal, Chancellor cards; constant card draws amplify normal skill damage rather than Ruin detonations; faster APM than..." |
| `la-surge-deathblade` | proposed | 20 | 0.0 | 0.0 | `la-surge-deathblade` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Enters Death Trance (Z), stacks Surge charges via multi-hit skills during the window, then fires Surge skill for massive burst damage scaled by stacks accumulated;..." |
| `mcd-dynamo-torment` | proposed | 20 | 0.0 | 0.0 | `mcd-dynamo-torment` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Dynamo enchantment stacks damage bonuses with each consecutive roll (up to 20×); the loop is ROLL to stack Dynamo, then ATTACK to unload — every..." |
| `la-perfect-suppression-shadowhunter` | proposed | 20 | 0.0 | 0.0 | `la-perfect-suppression-shadowhunter` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Perfect Suppression completely disables Demonize in exchange for +30% normal skill damage and +50% Shadowburst Meter generation; normal Cruel Cutter and Demolition become the damage..." |
| `la-lunar-voice-reaper` | proposed | 20 | 0.0 | 0.0 | `la-lunar-voice-reaper` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Persona Mode (Z) grants immediate Swoop damage boost without needing Chaos stacks; identity fires on demand with consistent returns; the smoother, more mobile Reaper path..." |
| `la-remaining-energy-deathblade` | proposed | 20 | 0.0 | 0.0 | `la-remaining-energy-deathblade` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Activates Death Trance identity immediately consuming Death Orbs to cast Deathblade Surge and grant 30s of attack/move speed buffs; consistent uptime damage cycling the identity..." |
| `la-esoteric-skill-wardancer` | proposed | 20 | 0.0 | 0.0 | `la-esoteric-skill-wardancer` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Generates Esoteric Orbs through skills and expends them on powerful Esoteric Skills; high mobility fast-animation burst in orb windows; consistent orb generation keeps Esoteric Skills..." |
| `la-hunger-reaper` | proposed | 20 | 0.0 | 0.0 | `la-hunger-reaper` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Hunger engraving focuses on generating maximum Chaos Meter for enhanced damage in Chaos Mode; builds Chaos stacks through skill use, dealing more damage the higher..." |
| `la-pinnacle-glaivier` | proposed | 20 | 0.0 | 0.0 | `la-pinnacle-glaivier` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Alternates between Focus (spear) and Flurry (glaive) stances at maxed Dual Meter to gain powerful self-buffs on each switch: +20% damage/+50% crit damage for Focus..." |
| `la-loyal-companion-sharpshooter` | proposed | 20 | 0.0 | 0.0 | `la-loyal-companion-sharpshooter` | TOTEM-SENTRY (0.9585) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Silverhawk companion contributes a significant portion of damage and provides massive buffs; more consistent and relaxed playstyle than Death Strike with fewer timing demands; rated..." |
| `la-full-moon-souleater` | proposed | 20 | 0.0 | 0.0 | `la-full-moon-souleater` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Generates and consumes Soul Stones to fill Possession Meter; enters Deathlord Mode for massive burst damage in seconds (Deathlord skill cooldown resets on entry; +15%..." |
| `la-demonic-impulse-shadowhunter` | proposed | 20 | 0.0 | 0.0 | `la-demonic-impulse-shadowhunter` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Builds Shadowburst Meter using Intrude skills (Demon Vision, Demon's Grip) then Demonizes — transforming into demon form for +20% move speed, +30% crit rate, specialized..." |
| `la-gravity-training-destroyer` | proposed | 31 | 0.0 | 0.0 | `la-gravity-training-destroyer` | TOTEM-SENTRY (0.9276) | - | geo=vortex_pull / deliv=at-target / ctrl=pull/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Generates 3 Gravity Cores via blue Concentration skills, spends them with purple Gravity Release skills to fill the Gravity Gauge, then activates Hypergravity Mode (60%..." |


### Docket 3 — SHAPESHIFT

- **Seed criterion:** canon_corpus.mech_note or folk_name contains werewolf/werebear/wereform/shapeshift/demonize/demon-form/wildsoul/shadowhunter/ferality/spirit-form/shape-form
- **Axis-signature requirement:** mech_note or folk_name contains a shape-form token
- **Method note:** seeds = corpus shape-token match (n=15 in E4, 14 after ratified-gateA removal); propagation halo REQUIRES the shape token (no engine-key shape axis exists yet — rocket dispatch pending per docket-3 sequencing)
- **Self-scored precision:** 0.8  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 4/5 = 0.8 (leave-one-out admit rate on chain seeds)
  - Coherence: 1.0 = 1 - conflict_rate (0/14)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 2 | 1 | 1.0000 |
| 11 | 3 | 0.7746 |
| 17 | 1 | 1.0000 |
| 19 | 1 | 1.0000 |
| 20 | 2 | 0.0000 |
| 21 | 1 | 1.0000 |
| 46 | 1 | 1.0000 |
| 49 | 1 | 1.0000 |
| 53 | 1 | 1.0000 |
| 91 | 1 | 1.0000 |
| 140 | 1 | 1.0000 |

- **Roster:** 14 total (0 ratified-seed, 14 proposed, 0 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `poe2-shaman-bear` | proposed | 2 | 0.0 | 0.0 | `poe2-shaman-bear` | WHIRLWIND (0.8246) | - | geo=circle / deliv=self-origin / ctrl=none/damage / econ=free / dep=build→spend / act=active / note: "POST-CUTOFF. prov=kb. mech_note ref: 'Druid shapeshifts into bear — built-in armour tank body, Rampage momentum clear.' Full dossier required." |
| `d2-fireclaw-wolf` | proposed | 11 | 0.0 | 0.0 | `d2-fireclaw-wolf` | TOTEM-SENTRY (0.7597) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Werewolf whose claws deal fire via Fire Claws synergy stack — form-shift melee wearing an elemental damage identity." |
| `d2-rabies-wolf` | proposed | 11 | 0.0 | 0.0 | `d2-rabies-wolf` | TRAP-MINE (0.8741) | - | geo=chain / deliv=at-target / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Werewolf bite spreads a contagious poison that jumps target-to-target; DoT plague delivered by a shapeshifted melee body." |
| `d2-fury-wolf` | proposed | 11 | 0.0 | 0.0 | `d2-fury-wolf` | TOTEM-SENTRY (0.7597) | - | geo=single_target / deliv=at-target / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Shapeshift into werewolf form — a different stat-and-skill body — then Fury multi-bite at extreme attack speed; the form IS the kit." |
| `gd-berserker-wereforms` | proposed | 17 | 0.0 | 0.0 | `gd-berserker-wereforms` | TRAP-MINE (0.8069) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hard-stop/damage / econ=free / dep=one-shot / act=active / note: "Grim Dawn's tenth mastery — a shapeshifter who transforms into 'vicious beastlike forms,' dual-wields between forms, and infuses weapons wit" |
| `d4-pulverize` | proposed | 19 | 0.0 | 0.0 | `d4-pulverize` | TOTEM-SENTRY (0.7027) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Werebear ground-slam shockwaves rolling forward off overpower windows — the launch druid's identity build; slow, wide, and satisfying, form-" |
| `la-perfect-suppression-shadowhunter` | proposed | 20 | 0.0 | 0.0 | `la-perfect-suppression-shadowhunter` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Perfect Suppression completely disables Demonize in exchange for +30% normal skill damage and +50% Shadowburst Meter generation; normal Cruel Cutter and Demolition become the damage..." |
| `la-demonic-impulse-shadowhunter` | proposed | 20 | 0.0 | 0.0 | `la-demonic-impulse-shadowhunter` | TOTEM-SENTRY (0.9585) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=identity-gauge / dep=build→spend / act=active / note: "Builds Shadowburst Meter using Intrude skills (Demon Vision, Demon's Grip) then Demonizes — transforming into demon form for +20% move speed, +30% crit rate, specialized..." |
| `di-spiritform-druid-pvp` | proposed | 21 | 0.0 | 0.0 | `di-spiritform-druid-pvp` | WHIRLWIND (0.6928) | - | geo=circle / deliv=self-origin / ctrl=none/damage / econ=cooldown / dep=one-shot / act=active / note: "PHANTOM (mob-harvest v3 mis-naming) — DI Druid class IS real (launched 2025-07-03, Blizzard official) but 'spirit form' mechanic does NOT exist; real transformations = Werewolf/Werebear/Stag..." |
| `d2-maul-bear` | proposed | 46 | 0.0 | 0.0 | `d2-maul-bear` | TRAP-MINE (0.6316) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=free / dep=one-shot / act=triggered / note: "Bear form stacks Maul damage charges per hit; slow heavy swings, tank identity, the other half of the form-shift family." |
| `d4-tornado-werewolf` | proposed | 49 | 0.0 | 0.0 | `d4-tornado-werewolf` | TOTEM-SENTRY (0.8229) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "A WEREWOLF casting storm magic — Grizzly Rage swapped for wolf-form tornado spam via the Stormchaser aspect steering the twisters; form-shif" |
| `d4-rabies-lacerate` | proposed | 53 | 0.0 | 0.0 | `d4-rabies-lacerate` | TOTEM-SENTRY (0.7651) | - | geo=chain / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=one-shot / act=active / note: "Werewolf contagion returns — RABIES, the D2 wolf's plague bite, resurfaces as a D4 S-tier paired with Lacerate's shred ultimate; a twenty-ye" |
| `le-werebear-druid` | proposed | 91 | 0.0 | 0.0 | `le-werebear-druid` | WHIRLWIND (0.7659) | - | geo=circle / deliv=self-origin / ctrl=hex/damage / econ=generator-spender / dep=one-shot / act=active / note: "prov=mx-le;eg;kb. mech_note ref: 'The bear form with its own bar — swipe, roar, maul on rage-drain fuel, massive built-in tankiness; the Season 4 bossing king.'..." |
| `poe2-demon-form` | proposed | 140 | 0.0 | 0.0 | `poe2-demon-form` | TOTEM-SENTRY (0.9885) | - | geo=circle / deliv=self-origin / ctrl=none/damage / econ=self-cost / dep=build→spend / act=active / note: "prov=kb. mech_note: 'Transform into a demon — a DIFFERENT body with its own skill economy — gaining scaled fire power.' Era=0.1;0.2-dawn;0.4. Variable amp (V): the..." |


### Docket 4 — DOT-AILMENT

- **Seed criterion:** canon_engine_key.ctrl_function IN ('poison','hex') OR mech_note/folk_name contains DoT/poison/bleed/rabies/toxic-rain/blight/plague tokens
- **Axis-signature requirement:** ctrl_function IN ('poison','hex') OR mech_note carries a DoT token
- **Method note:** seeds = ratified ctrl_function poison/hex + corpus DoT-token match (n=42, 35 after ratified-gateA removal)
- **Self-scored precision:** 0.972  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 11/11 = 1.0 (leave-one-out admit rate on chain seeds)
  - Coherence: 0.972 = 1 - conflict_rate (1/36)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 11 | 2 | 0.6325 |
| 24 | 1 | 1.0500 |
| 27 | 1 | 1.0500 |
| 28 | 1 | 1.0500 |
| 29 | 1 | 1.0500 |
| 34 | 1 | 1.0500 |
| 37 | 1 | 1.0500 |
| 41 | 1 | 1.0500 |
| 42 | 1 | 1.0500 |
| 47 | 3 | 0.7035 |
| 48 | 1 | 1.0500 |
| 50 | 1 | 1.0500 |
| 53 | 2 | 0.6325 |
| 55 | 1 | 1.0500 |
| 63 | 1 | 1.0500 |
| 64 | 1 | 1.0500 |
| 67 | 1 | 1.0500 |
| 84 | 2 | 0.7746 |
| 91 | 1 | 1.0500 |
| 92 | 2 | 0.8944 |
| 93 | 1 | 1.0500 |
| 115 | 1 | 1.0500 |
| 119 | 1 | 1.0500 |
| 120 | 1 | 1.0500 |
| 126 | 1 | 1.0500 |
| 135 | 1 | 1.0500 |
| 136 | 1 | 1.0500 |
| 137 | 1 | 1.0500 |
| 141 | 1 | 1.0500 |

- **Roster:** 36 total (0 ratified-seed, 36 proposed, 1 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `d2-rabies-wolf` | proposed | 11 | 0.0 | 0.0 | `d2-rabies-wolf` | TRAP-MINE (0.8741) | - | geo=chain / deliv=at-target / ctrl=none/damage / econ=unknown / dep=one-shot / act=active / note: "Werewolf bite spreads a contagious poison that jumps target-to-target; DoT plague delivered by a shapeshifted melee body." |
| `poe1-dark-pact` | proposed | 11 | 0.0 | 0.0 | `poe1-dark-pact` | TRAP-MINE (0.9225) | - | geo=chain / deliv=at-target / ctrl=hex/damage / econ=self-cost / dep=one-shot / act=active / note: "Chaining chaos nova that SACRIFICES skeleton life to fuel its damage — or your own life if no skeletons; minions as batteries, the self-dama" |
| `poe1-bane` | proposed | 24 | 0.0 | 0.0 | `poe1-bane` | TOTEM-SENTRY (0.9002) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=spend / dep=one-shot / act=active / note: "One cast applies chaos DoT AND every linked curse simultaneously — the curse-bundler damage spell." |
| `d2-ghost-pvp` | proposed | 27 | 0.0 | 0.0 | `d2-ghost-pvp` | TOTEM-SENTRY (0.8672) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=stun/damage / econ=spend / dep=apply→detonate / act=active / note: "Authoritative D2 PvP Ghost = Assassin WW/Trap archetype: Mind Blast stun (Shadow Discipline) + Fade DR + Open Wounds bleed stacking on Whirlwind weapons +..." |
| `poe2-acolyte-darkness` | proposed | 28 | 0.0 | 0.0 | `poe2-acolyte-darkness` | TOTEM-SENTRY (1.0378) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/control / econ=generator-spender / dep=one-shot / act=active / note: "prov=kb. mech_note: 'Chaos monk who trades spirit for the Waking Dream darkness resource, converting [Spirit] into chaos-skill powered attacks.' Era=0.1;0.2-dawn only — earlier PoE2 version..." |
| `chr-bleed-berserker` | proposed | 29 | 0.0 | 0.0 | `chr-bleed-berserker` | TOTEM-SENTRY (0.6785) | - | geo=melee_strike / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Damage_mode=dot (bleed is the damage engine). Low tempo (L) is the key distinction — fewer but harder strikes that each apply max bleed stacks efficiently...." |
| `gd-doom-bolt-sentinel` | proposed | 34 | 0.0 | 0.0 | `gd-doom-bolt-sentinel` | TOTEM-SENTRY (0.8075) | - | geo=single_target / deliv=at-target / ctrl=hex/damage / econ=cooldown / dep=one-shot / act=active / note: "The chaos hammer from the sky on a hard cooldown — Doom Bolt deletes one target per cast while acid-chaos DoTs carry the between-time; nuke-" |
| `poe1-ward-loop` | proposed | 37 | 0.0 | 0.0 | `poe1-ward-loop` | MINION-PET (0.954) | - | geo=multi_projectile / deliv=self-origin / ctrl=hex/damage / econ=self-cost / dep=one-shot / act=active / note: "Skeletons die instantly, Heartbound Loop self-damages you, CWDT recasts skeletons, Olroth's ward absorbs it all — a PERPETUAL MOTION cast en" |
| `vs-vlad-dracula` | proposed | 41 | 0.0 | 0.0 | `vs-vlad-dracula` | TOTEM-SENTRY (0.8478) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=unknown / dep=one-shot / act=active / note: "DLC character (Castlevania / Operation Guns DLC). Secret unlock. Provenance = VV (video/wiki), limited documentation. Reduced conf for DLC content. Era: dlc-era + s11-2025+ (s11..." |
| `hot-warlock` | proposed | 42 | 0.0 | 0.0 | `hot-warlock` | CHANNELED-BEAM (0.8678) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=spend / dep=one-shot / act=active / note: "'The SEVENTH game in the corpus to ship a caster-summoner archetype' — Elrond/Gandalf note: convergence data point for summoner-caster pattern. Corpus cites this explicitly as..." |
| `poe1-caustic-arrow` | proposed | 47 | 0.0 | 0.0 | `poe1-caustic-arrow` | TRAP-MINE (0.8938) | - | geo=circle / deliv=projectile / ctrl=hex/damage / econ=spend / dep=one-shot / act=triggered / note: "Arrow leaves a caustic ground cloud ticking chaos DoT — the original ground-DoT bow archetype, TR's ancestor." |
| `poe1-edc` | proposed | 47 | 0.0 | 0.0 | `poe1-edc` | TRAP-MINE (0.8986) | - | geo=chain / deliv=projectile / ctrl=hex/damage / econ=spend / dep=one-shot / act=triggered / note: "Essence Drain ticks chaos DoT; Contagion makes the DoT JUMP to neighbors on death — a two-button plague that clears rooms by spreading. The " |
| `poe1-toxic-rain` | proposed | 47 | 0.0 | 0.0 | `poe1-toxic-rain` | TRAP-MINE (0.8437) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=spend / dep=one-shot / act=triggered / note: "Arrows rain pods that slow and tick chaos DoT in overlapping zones — the perennial low-budget league-start king." |
| `chr-plague-curse-warlock` | proposed | 48 | 0.0 | 0.0 | `chr-plague-curse-warlock` | TOTEM-SENTRY (1.0577) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/control / econ=finite / dep=build→spend / act=active / note: "Control centrality=CORE: curses ARE the purpose of this kit (debuff-centric playstyle). Ammo economy = curse charges (limited stock, accumulates over time). Shadow element from shadow/dark..." |
| `poe1-hexblast-mines` | proposed | 50 | 0.0 | 0.0 | `poe1-hexblast-mines` | TRAP-MINE (0.7215) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=free / dep=apply→detonate / act=triggered / note: "Hexblast consumes the curse on the target for a huge chaos hit; mine cadence automates the curse-then-consume loop — ailment mark-and-detona" |
| `poe1-forbidden-rite` | proposed | 50 | 1.05 | 1.0 | `poe1-hexblast-mines` | TOTEM-SENTRY (0.6847) | TOTEM-SENTRY | geo=totem / deliv=at-target / ctrl=hex/damage / econ=self-cost / dep=apply→detonate / act=active / note: "Forbidden Rite: chaos spell that costs life to cast (in addition to mana), dealing chaos damage plus launching seeking chaos projectiles that home on enemies...." |
| `d4-rabies-lacerate` | proposed | 53 | 0.0 | 0.0 | `d4-rabies-lacerate` | TOTEM-SENTRY (0.7651) | - | geo=chain / deliv=at-target / ctrl=none/damage / econ=generator-spender / dep=one-shot / act=active / note: "Werewolf contagion returns — RABIES, the D2 wolf's plague bite, resurfaces as a D4 S-tier paired with Lacerate's shred ultimate; a twenty-ye" |
| `gd-bloody-pox-conjurer` | proposed | 53 | 0.0 | 0.0 | `gd-bloody-pox-conjurer` | TOTEM-SENTRY (0.8127) | - | geo=chain / deliv=at-target / ctrl=expose/damage / econ=cooldown / dep=one-shot / act=active / note: "Infect one target and watch the PLAGUE JUMP — Bloody Pox spreads body to body on proximity, fumble transmuters making whole screens miss whi" |
| `poe1-viper-poison` | proposed | 55 | 0.0 | 0.0 | `poe1-viper-poison` | TOTEM-SENTRY (0.9365) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=spend / dep=build→spend / act=active / note: "Fast poison-stacking strikes where kills burst remaining poison to neighbors — DoT melee with contagion pops." |
| `le-shield-throw-time-rot-vk` | proposed | 63 | 0.0 | 0.0 | `le-shield-throw-time-rot-vk` | TRAP-MINE (0.9504) | - | geo=chain / deliv=projectile / ctrl=hex/control / econ=spend / dep=one-shot / act=triggered / note: "POST-CUTOFF. 1.4-omens only; conf=0.40 in atlas. prov=mx-le. mech_note ref: 'Ricocheting shield throws carrying Time Rot void stacks — the captain-america delivery finally earning a tier..." |
| `gd-blight-fiend-ritualist` | proposed | 64 | 0.0 | 0.0 | `gd-blight-fiend-ritualist` | TRAP-MINE (0.5181) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=free / dep=one-shot / act=triggered / note: "Summon the rotting horror that EXPLODES on death and gets resummoned INTO packs — the disposable-bomber pet whose corpse is the payload; pet" |
| `d2-poison-nova-necro` | proposed | 67 | 0.0 | 0.0 | `d2-poison-nova-necro` | WHIRLWIND (0.8485) | - | geo=ring / deliv=self-origin / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Poison Nova blankets the whole screen in an expanding DoT ring on cooldown cadence, Lower Resist amplifying; sweep-and-move plague caster." |
| `d2-poison-javazon` | proposed | 84 | 0.0 | 0.0 | `d2-poison-javazon` | TOTEM-SENTRY (0.8075) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=spend / dep=apply→detonate / act=active / note: "Plague Javelin blankets areas in overlapping poison clouds; damage-over-time identity with delayed kill confirmation." |
| `poe1-lacerate-glad` | proposed | 84 | 0.0 | 0.0 | `poe1-lacerate-glad` | TOTEM-SENTRY (0.8624) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=none/damage / econ=spend / dep=build→spend / act=active / note: "Physical bleed DoT stacking with max-block defense; hit once, watch them bleed out while blocking everything." |
| `le-werebear-druid` | proposed | 91 | 0.0 | 0.0 | `le-werebear-druid` | WHIRLWIND (0.7659) | - | geo=circle / deliv=self-origin / ctrl=hex/damage / econ=generator-spender / dep=one-shot / act=active / note: "prov=mx-le;eg;kb. mech_note ref: 'The bear form with its own bar — swipe, roar, maul on rage-drain fuel, massive built-in tankiness; the Season 4 bossing king.'..." |
| `poe1-pconc` | proposed | 92 | 0.0 | 0.0 | `poe1-pconc` | AURA (0.9354) | - | geo=circle / deliv=projectile / ctrl=hex/damage / econ=finite / dep=one-shot / act=active / note: "UNARMED flask-thrower: lobs exploding poison vials whose damage scales off LIFE FLASK charges — the consumable-charge pool as ammunition; le" |
| `poe1-venom-gyre` | proposed | 92 | 0.0 | 0.0 | `poe1-venom-gyre` | MINION-PET (1.0122) | - | geo=dash_attack / deliv=projectile / ctrl=hex/damage / econ=generator-spender / dep=one-shot / act=active / note: "Thrown poison projectiles that RETURN and are caught, then re-released in a burst via Whirling Blades — catch-and-release ammo economy on a " |
| `tq-druid-squall-caster` | proposed | 93 | 0.0 | 0.0 | `tq-druid-squall-caster` | TOTEM-SENTRY (0.6599) | - | geo=totem / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Tempo=low is the distinguishing characteristic here — Squall ticks at a slow rate but persistently. This is a 'place-and-move' zone kit rather than an active-spam..." |
| `d4-shadowblight` | proposed | 115 | 0.0 | 0.0 | `d4-shadowblight` | TOTEM-SENTRY (0.7374) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=blind/damage / econ=spend / dep=apply→detonate / act=active / note: "Stacked shadow damage-over-time detonating Shadowblight key-passive pulses — the darkness-plague necro promoted from tail to tier rows by th" |
| `gd-wendigo-totem-ritualist` | proposed | 119 | 0.0 | 0.0 | `gd-wendigo-totem-ritualist` | TOTEM-SENTRY (0.6661) | - | geo=totem / deliv=at-target / ctrl=none/damage / econ=cooldown / dep=apply→detonate / act=triggered / note: "Plant hungering totems that LEECH the room for you while bleed stacks tick — the totem-warfare strand where furniture does the drinking and " |
| `hades1-ares-doom` | proposed | 120 | 0.0 | 0.0 | `hades1-ares-doom` | TRAP-MINE (0.8229) | - | geo=single_target / deliv=at-target / ctrl=hex/control / econ=free / dep=one-shot / act=triggered / note: "Tag-bank-payout grammar: the 'bank' is the Doom window; the 'payout' is detonation. Wind-up commit because the damage is temporally decoupled from the hit — you..." |
| `le-chthonic-fissure-warlock` | proposed | 126 | 0.0 | 0.0 | `le-chthonic-fissure-warlock` | CHANNELED-BEAM (0.9532) | - | geo=line / deliv=line / ctrl=hex/damage / econ=spend / dep=one-shot / act=active / note: "prov=gg;lw;kb. mech_note ref: 'Tear the ground open — the fissure crawls forward belching chaos SPIRITS that seek and burn while curse stacks multiply damage.' Correction..." |
| `poe1-hoag` | proposed | 135 | 0.0 | 0.0 | `poe1-hoag` | TRAP-MINE (0.7452) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=hex/damage / econ=generator-spender / dep=one-shot / act=triggered / note: "YOUR poison hits do nothing but feed virulence stacks to a scorpion crawler pet who does ALL the killing — the player is the pet's..." |
| `poe1-poison-bv` | proposed | 136 | 0.0 | 0.0 | `poe1-poison-bv` | CHANNELED-BEAM (1.0316) | - | geo=unknown / deliv=orbit / ctrl=hex/damage / econ=generator-spender / dep=build→spend / act=active / note: "Stacks up to ten spinning blades ORBITING the body, each hitting everything nearby on rotation — maintain the stack, walk into packs, everyt" |
| `poe1-scourge-arrow` | proposed | 137 | 0.0 | 0.0 | `poe1-scourge-arrow` | CHANNELED-BEAM (1.0208) | - | geo=multi_projectile / deliv=projectile / ctrl=hex/damage / econ=spend / dep=build→spend / act=active / note: "Channel to grow thorn charge stages, release a spore-pod fan — bow channel-and-release with poison stacking." |
| `poe2-erasure-edc-lich` | proposed | 141 | 0.0 | 0.0 | `poe2-erasure-edc-lich` | CHANNELED-BEAM (0.9415) | - | geo=chain / deliv=projectile / ctrl=expose/damage / econ=spend / dep=one-shot / act=active / note: "prov=kb. mech_note: 'The ED-and-Contagion plague loop reborn in PoE2's Lich chassis with the Erasure-[mechanic] amplifying spread.' Era=0.2-dawn through 0.5-ancients. The Lich ascendancy (Sorceress path) enables..." |


### Docket 5 — MULTI-PROJECTILE-VOLLEY

- **Seed criterion:** membership in U-1 islet from shelved archipelago mock (largest unseeded coherent cluster, size 20)
- **Axis-signature requirement:** geometry_value = 'multi_projectile' (U-1 seeds are 100% multi_projectile)
- **Method note:** seeds = U-1 islet from 2026-07-16 archipelago mock (retained derivation layer); 20 of 20 in E4 after ratified-gateA removal; the U-1 axis signature is geometry_value='multi_projectile' (20/20 seeds); propagation halo REQUIRES this axis, so cross-family drift is prevented
- **Self-scored precision:** 1.0  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 15/15 = 1.0 (leave-one-out admit rate on chain seeds)
  - Coherence: 1.0 = 1 - conflict_rate (0/20)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 4 | 7 | 0.6325 |
| 14 | 2 | 0.6325 |
| 16 | 1 | 0.6325 |
| 23 | 1 | 0.6325 |
| 49 | 2 | 0.6325 |
| 55 | 2 | 0.4472 |
| 58 | 2 | 0.6325 |
| 74 | 1 | 0.6325 |
| 78 | 1 | 0.6325 |
| 129 | 1 | 0.6325 |

- **Roster:** 20 total (0 ratified-seed, 20 proposed, 0 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `d4-quill-volley` | proposed | 4 | 0.0 | 0.0 | `d4-quill-volley` | TOTEM-SENTRY (0.8229) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Eagle-spirit feather volleys that pierced, returned, and multiplied through bugged interactions into damage ORDERS OF MAGNITUDE past every o" |
| `poe1-spark` | proposed | 4 | 0.0 | 0.0 | `poe1-spark` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Sprays duration projectiles that wander randomly, bouncing off walls until they find flesh — corridor-flooding stochastic swarm; reborn as t" |
| `hot-sorceress-splinters` | proposed | 4 | 0.0 | 0.0 | `hot-sorceress-splinters` | CHANNELED-BEAM (0.8678) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Projectile-count platform: 'stacked for range and screen coverage' — the scaling axis is splinter count, not per-hit amplitude. Forum-paired with Ring Blades (hot-sage-ring-blades) as the..." |
| `poe1-split-arrow-bleed` | proposed | 4 | 0.0 | 0.0 | `poe1-split-arrow-bleed` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Wide arrow fan applying stacked bleeds with Gladiator explosion pops — physical DoT at range." |
| `hot-archer` | proposed | 4 | 0.0 | 0.0 | `hot-archer` | CHANNELED-BEAM (0.8678) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "'The projectile-count platform of the roster, the Diablo-3-Demon-Hunter homage' per mech_note. EA-2023 anchor = solid pre-cutoff provenance. Multistrike + Pierce traits = the Archer's two..." |
| `poe1-tornado-shot` | proposed | 4 | 0.0 | 0.0 | `poe1-tornado-shot` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Arrow flies to a point then bursts into secondary arrows in all directions — projectile-spawns-projectiles; the endgame magic-find throne fo" |
| `poe1-wander` | proposed | 4 | 0.0 | 0.0 | `poe1-wander` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Wand shots explode in clustered secondary blasts around impact — screen-paint clearing; the named wander MF archetype, refreshed by the 3.27" |
| `d2-frozen-orb-sorc` | proposed | 14 | 0.0 | 0.0 | `d2-frozen-orb-sorc` | CHANNELED-BEAM (0.9296) | - | geo=multi_projectile / deliv=projectile / ctrl=hard-stop/damage / econ=spend / dep=one-shot / act=active / note: "Frozen Orb travels then shatters, spraying radial ice bolts along its whole path; low-invest one-point wonder and the projectile-that-emits " |
| `d4-frozen-orb` | proposed | 14 | 0.0 | 0.0 | `d4-frozen-orb` | TOTEM-SENTRY (0.8956) | - | geo=multi_projectile / deliv=projectile / ctrl=hard-stop/damage / econ=spend / dep=one-shot / act=active / note: "The D2 heirloom in D4 clothes — orb travels and sprays radial bolts, Fractured Winterglass recursion spawning free orbs from conjuration pro" |
| `ud-spread-rapid-dex` | proposed | 16 | 0.0 | 0.0 | `ud-spread-rapid-dex` | CHANNELED-BEAM (0.9648) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=build→spend / act=active / note: "The 'launch floor' of Undecember: Multishot as a LINK rune attaches to a base attack, multiplying projectile count. Spread Shot + Rapid Shot under the..." |
| `poe1-sst` | proposed | 23 | 0.0 | 0.0 | `poe1-sst` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Throws a copy of the shield that shatters into shrapnel; damage scales off shield defenses — gear-stat-as-weapon oddity." |
| `d2-wind-druid` | proposed | 49 | 0.0 | 0.0 | `d2-wind-druid` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Tornado throws erratic-path physical-magic twisters while Hurricane spins a cold aura around the body; the wandering-rotator archetype with " |
| `d4-tornado-werewolf` | proposed | 49 | 0.0 | 0.0 | `d4-tornado-werewolf` | TOTEM-SENTRY (0.8229) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "A WEREWOLF casting storm magic — Grizzly Rage swapped for wolf-form tornado spam via the Stormchaser aspect steering the twisters; form-shif" |
| `poe1-lightning-strike` | proposed | 55 | 0.0 | 0.0 | `poe1-lightning-strike` | TOTEM-SENTRY (0.8229) | - | geo=multi_projectile / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Melee strike that also fires converted-lightning projectiles forward — melee and ranged in one button; the modern era's dominant strike skil" |
| `poe1-frost-blades` | proposed | 55 | 0.0 | 0.0 | `poe1-frost-blades` | TOTEM-SENTRY (0.8956) | - | geo=multi_projectile / deliv=at-target / ctrl=hard-stop/damage / econ=spend / dep=one-shot / act=active / note: "Cold strike whose hits throw icy projectiles to targets behind — the cold sibling of the strike-plus-projectiles family." |
| `poe1-kinetic-fusillade` | proposed | 58 | 0.0 | 0.0 | `poe1-kinetic-fusillade` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "New wand attack from the 3.27 wand rework, holding tier-list placement into 3.28 Mirage. SEARCH-DERIVED (post-cutoff); mechanics thin — doss" |
| `d2-bowazon` | proposed | 58 | 0.0 | 0.0 | `d2-bowazon` | TRAP-MINE (0.8986) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=free / dep=one-shot / act=active / note: "Pure physical ranged attacker: Multishot fans arrows for density, Strafe autotargets sequential shots; damage entirely weapon-and-attack-spe" |
| `poe1-molten-strike` | proposed | 74 | 0.0 | 0.0 | `poe1-molten-strike` | TOTEM-SENTRY (0.8576) | - | geo=multi_projectile / deliv=at-target / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "Melee hit sprays fire projectiles that rain back down around the target — strike-emits-projectiles; the Uber Elder era's boss-killer throne." |
| `poe2-spiral-volley` | proposed | 78 | 0.0 | 0.0 | `poe2-spiral-volley` | CHANNELED-BEAM (0.9176) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=one-shot / act=active / note: "POST-CUTOFF. prov=kb. mech_note ref: 'Spear projectiles on spiraling flight paths, named among 0.4's top-tier archetypes.' Full dossier required." |
| `le-umbral-blades` | proposed | 129 | 0.0 | 0.0 | `le-umbral-blades` | TOTEM-SENTRY (0.914) | - | geo=multi_projectile / deliv=projectile / ctrl=none/damage / econ=spend / dep=apply→detonate / act=active / note: "Two-phase mechanic (throw-lodge-recall) means a single cast applies damage on the way out AND on recall. Scale via cast speed + projectile count nodes. mech_note..." |


### Docket 6 — MINION-PET

- **Seed criterion:** gateA-ratified MINION-PET (7 members, atlas_gateA_labels_2026_07_14)
- **Axis-signature requirement:** ctrl_function='taunt' AND economy_model='reserve' AND dependency_val='one-shot' (all 7 seeds share this signature)
- **Method note:** seeds = ratified gateA MINION-PET family (n=7); axis signature is ctrl_function='taunt' + economy_model='reserve' + dependency_val='one-shot' (7/7 seeds); this is the seed-poverty case — same-family propagation to find the ~12 obvious members
- **Self-scored precision:** 0.8  (method: LOO x coherence (1 - conflict_rate))
  - LOO: 4/5 = 0.8 (leave-one-out admit rate on chain seeds)
  - Coherence: 1.0 = 1 - conflict_rate (0/1)
- **Chains (Leiden sub-clusters spanned):**

| Leiden | seeds | tau (P75, capped @ 1.05) |
|---:|---:|---:|
| 3 | 3 | 0.6325 |
| 6 | 2 | 0.4472 |
| 30 | 1 | 0.7746 |
| 147 | 1 | 0.7746 |

- **Roster:** 8 total (7 ratified-seed, 1 proposed, 0 conflict-flagged)

| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |
|---|---|---:|---:|---:|---|---|---|---|
| `chr-demon-legion-warlock` | ratified-seed | 3 | - | - | `-` | MINION-PET (0.4738) | - | geo=circle / deliv=self-origin / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "EA-2015-2019 + 1.0-2020 (early archetype, kb confirmed). Shadow element from demon/dark magic. D1: shield-absorb = Warlock has arcane/dark barrier defense. Heavy proxy = the defining..." |
| `di-minion-necro` | ratified-seed | 3 | - | - | `-` | MINION-PET (0.4738) | - | geo=circle / deliv=self-origin / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "D1: Bone Armor (shield-absorb) is the primary defense layer on top of HP-stack; not a melee-dodge kit. Heavy proxy = the defining feature — Necro..." |
| `chr-pet-warden` | ratified-seed | 3 | - | - | `-` | MINION-PET (0.5307) | - | geo=circle / deliv=self-origin / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "'Pet Zoo' = maximum pet diversity build. Heavy proxy is the defining feature. The 'range=melee' (M in pos 2) is unusual for a pet master..." |
| `tli-moto-bots` | ratified-seed | 6 | - | - | `-` | MINION-PET (0.5307) | - | geo=totem / deliv=at-target / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "TLI live-2022+ only (no 2026 content); moderate conf. Moto is TLI's mechanical/bot commander hero — TL2 Bot Engineer archetype adapted to TLI's hero system. SU..." |
| `tl2-bot-engineer` | ratified-seed | 6 | - | - | `-` | MINION-PET (0.6061) | - | geo=totem / deliv=at-target / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "Heavy proxy (H) = bot army delivers all damage; Engineer is the commander. SU old code = sustain (reserve maintenance). TL2 Bot Engineer mirrors TQ..." |
| `tq-petmaster-summoner` | ratified-seed | 30 | - | - | `-` | MINION-PET (0.5031) | - | geo=self_buff / deliv=self-origin / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "Heavy proxy is the defining characteristic. Economy=reserve captures the continuous pet upkeep cost. TQ summoner can use Nature (wolves + call of the wild), Spirit..." |
| `tl2-shadowling-outlander` | ratified-seed | 147 | - | - | `-` | MINION-PET (0.6292) | - | geo=ground_targeted_circle / deliv=at-target / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "Shadowlings spawn from killed enemies (proc economy on kill events) rather than via direct summon skill. This is a kill-to-summon proxy model — proxy=heavy because..." |
| `tl1-alchemist-summoner` | proposed | 30 | 0.7746 | 0.4472 | `tq-petmaster-summoner` | MINION-PET (0.6061) | - | geo=self_buff / deliv=self-origin / ctrl=taunt/damage / econ=reserve / dep=one-shot / act=active / note: "Commit=channel is unusual for a summoner but captures the TL1 Alchemist's casting animations — raising Zombie minions or summoning Golem requires a brief channel animation..." |


## 4. ROSTER TALLY (totals across all six dockets)

| docket | working label | ratified-seed | proposed | conflict-flagged | self-scored precision |
|---:|---|---:|---:|---:|---:|
| 1 | MELEE-STRIKE | 0 | 36 | 2 | 0.899 |
| 2 | IDENTITY-GAUGE | 0 | 31 | 0 | 0.967 |
| 3 | SHAPESHIFT | 0 | 14 | 0 | 0.8 |
| 4 | DOT-AILMENT | 0 | 36 | 1 | 0.972 |
| 5 | MULTI-PROJECTILE-VOLLEY | 0 | 20 | 0 | 1.0 |
| 6 | MINION-PET | 7 | 1 | 0 | 0.8 |
| **TOTAL** | 6 dockets | **7** | **138** | **3** | — |

**Row-count self-audit.** E4 corpus: 562 kit-points served. `canon_corpus` row count: 585 (585-row conservation). Ratified-seeds + proposals emitted across all dockets: 7 + 138 = 145. This is expected to be LESS than 562 — many E4 kits fall in no chain (their Leiden sub-cluster carries no seed of any docket). Docket 6 (MINION-PET) is a same-family re-seed and emits ratified members alongside proposals.

## 5. HONEST NOTES (things Matt should see at review)

- **Channel-C intuitive-name gap (MELEE-STRIKE).** The wave-4 shelving text listed six intuitive channel-C members: `d2-smiter`, `d2-kicksin`, `gd-heavy-strike`, `primal-strike`, `blade-arc`, `onslaught`. Of these, ONLY TWO (`d2-smiter` and `tq-onslaught-assassin`) actually carry `canon_engine_key.geometry_value = 'melee_strike'` and thus appear in this docket. The other four have different ratified geometry axes: `d2-kicksin` = 'single_target' (multi-kick per activation), `poe1-heavy-strike-stun` = 'totem', `gd-primal-strike-vindicator` = 'ground_targeted_circle', `gd-blade-arc-warder` = 'circle'. This is a data-truth-vs-intuition gap: intuitive naming is 'melee strike' but the ratified engine-key axis says otherwise. The MELEE-STRIKE docket-1 roster follows corpus truth, not intuition. Matt may (a) accept this as the axis definition and name the family after what the axis IS, (b) request an engine-key axis re-review for these four intuitively-melee kits (the axis may be recording nova/aoe SHAPE rather than melee-strike identity), or (c) fold them under a different working family whose axis matches.

- **Docket-2 tightening (GX-19).** The docket text called out '~8 cross-game exhibits + LA identity-gauge cohort'. Broader `dependency_val='build→spend'` catches 100+ kits (any builder-spender), which would drown a one-sitting review. This roster tightens to `economy_model='identity-gauge'` exclusively — the LA cohort archetype (31 kits: LA + 1 MCD). This is a smaller, more coherent family. If Matt intended the broader lineage, we can re-derive with the wider criterion (and expect ~100+ proposals). The tight variant is served here as the defensible-review-shape.

- **U-1 islet axis truth.** The 20 U-1 members are 100% `geometry_value='multi_projectile'` — a beautiful mech-truth signature. Working label MULTI-PROJECTILE-VOLLEY reflects this. This is docket 5's strongest self-scored result (precision 1.0).

- **MINION-PET signature clarity.** All 7 ratified seeds share `ctrl_function='taunt'` + `economy_model='reserve'` + `dependency_val='one-shot'`. Only 1 kit (`tl1-alchemist-summoner`) in the E4 corpus matches this signature without being ratified. That's a lean halo — the seed-poverty case is TIGHTER than 12 candidates once we apply the ratified triple-axis signature. If Matt wants more MINION-PET candidates, the axis signature would need loosening (e.g., drop `ctrl_function='taunt'` constraint).

- **Conflict-flagged proposals.** 3 total across dockets: kits whose mech-fingerprint is within tau of a docket's chain-seed AND satisfy the docket axis, BUT are already ratified in another gateA family. These are surfaced (not admitted) so Matt can rule on whether the mech-axis reading is right, the gateA-family assignment is right, or both hold and the kit is a genuine cross-family case.

## 6. GUARDRAILS (what this pass does NOT do)

- **Not names-review.** Working labels ('MELEE-STRIKE', 'IDENTITY-GAUGE', 'MULTI-PROJECTILE-VOLLEY', etc.) are provisional; Matt names them at review or replaces them.
- **Not a plate rewrite.** The E4 2D coordinates are unchanged. Galadriel's islands layer joins by `kit_id` against `atlas-edition4.json` for x/y — this file does NOT duplicate coordinates.
- **Not gateA-ratified.** Every proposed member carries `status='proposed'`; only docket-6 MINION-PET (a same-family re-seed) carries `status='ratified-seed'` for its 7 existing gateA members.
- **Not a full-corpus classification.** Non-seed kits in chains without seeds are silently deferred — the pass is docket-driven, not exhaustive.

## 7. FILES

- `atlas-e4-family-candidates.json` — the serving artifact; galadriel joins by `kit_id`.
- `family-candidates-docket-2026-07-17.md` — this report (method, tallies, per-docket rosters, self-scores).
