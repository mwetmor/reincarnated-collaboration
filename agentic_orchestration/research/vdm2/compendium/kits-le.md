# VDM-2 Compendium — le (37 kits)

> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries (render-layer joins; DB never mutated). **v2.0** · db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` · generated 2026-07-22T09:46:42Z.
> `court` is the reconciled element court (enum-checked); `original_element` carries raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). `kit_citations` is the sole citation authority.

| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |
|---|---|---|---|---|---|---|
| E 0 · C 22 · A 10 · G 5 | 37 | 171/5/79 | 222 | 37/37 | 78 | 59 |

## le-bladestorm-bd — Bladestorm Bladedancer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @LizardIRL · https://maxroll.gg/last-epoch/build-guides/bladestorm-bladedancer-guide
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Bladestorm**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Shurikens**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Bladestorm Bladedancer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Bladestorm's placed spinning-blade entity is not a perfect 26-enum fit — `totem` captures placed-emitter honesty but loses the spinning/whirlwind visual texture (whirlwind rejected: it implies player-centered spin, fetched explicitly denies this). · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Bladestorm's placed spinning-blade entity is not a perfect 26-enum fit — `totem` captures placed-emitter honesty but loses the spinning/whirlwind visual texture (whirlwind rejected: it implies player-centered spin, fetched explicitly denies this). Source player loses no mechanic, only the geometry-flavor precision. Low-Life stacking mapped as economy note, not a §B inversion row (attestation gap).

## le-bomb-lance-falconer — Explosive Ballista Falconer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 3 / 3 · **dossier rows:** 6
- **citations (6):** [authored] maxroll.gg · @BinaQc · https://maxroll.gg/last-epoch/build-guides/explosive-ballista-falconer-guide; [authored] maxroll.gg · @LizardIRL · https://maxroll.gg/last-epoch/build-guides/dive-bomb-falconer; [authored] icy-veins.com · @EMP1241 · https://www.icy-veins.com/last-epoch/falconer-explosive-dive-bomb-endgame-build; [authored] maxroll.gg · @BinaQc · https://maxroll.gg/last-epoch/build-guides/ballista-falconer-guide; [official] maxroll.gg · https://maxroll.gg/last-epoch/news/falconer-reveal; [authored] loltank.com · @Dwight · https://loltank.com/2024/02/27/last-epoch-1-0-build-dive-bomb-explosive-ballista-falconer
- **t4 doors:** `PROXY_ASCENSION`, `DUAL_PROXY`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Explosive Trap (0-mana, thrown placed trap, AoE explosion on trigger)**: delivery=zone, cadence=spam, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Ballista (stationary turret, ranged projectile auto-targeting, triggered by Explosive Trap)**: delivery=summon_delegate, range=screen, width=wide, cadence=cooldown, count=1 · conf 0.75
  - `#2` **Dive Bomb (Falcon descends, large AoE burst against priority targets)**: delivery=zone, width=wide, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#3` **Falconry (Falcon companion — passive Falcon Strikes, following companion)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#4` **Smoke Bomb (placed cloud AoE — defense and mobility)**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Explosive Ballista Falconer: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Fire element not attested in non-abstained dossier rows (brief hot-fact references 'inflicting fire damage' but this phrase not found in fetched abstained=0 text); · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Fire element not attested in non-abstained dossier rows (brief hot-fact references 'inflicting fire damage' but this phrase not found in fetched abstained=0 text); mapping as water-only with fidelity note. Dual placed-proxy identity (Trap+Ballista both placed) is richer than a single totem; DUAL_PROXY T4 captures this. Falcon companion following vs placed nuance: companion lane not a T4 door class but noted in delivery.

## le-chthonic-fissure-warlock — Chthonic Fissure Warlock `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,shadow
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] forum.lastepoch.com · @unknown · https://forum.lastepoch.com/t/chthonic-fissure-and-grim-tide-application/62794; [official] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/news/warlock-wrap-up-falconer-teaser; [authored] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/build-guides/torment-warlock-guide
- **t4 doors:** `ELEMENT_CONVERSION_HYBRID`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Chthonic Fissure**: delivery=zone, cadence=cooldown, motion_signature=lane_place, count=1 · conf 0.75
  - `#1` **Chaos Bolts**: delivery=projectile, cadence=spam, motion_signature=fan_spread, count=1 · conf 0.75
  - `#2` **Infernal Shade**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Chthonic Fissure Warlock: placed lane zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The signature 'fire damage over time' of Chthonic Fissure almost certainly IS the Ignite ailment in-game, but the guide never names the status, so burn is withheld under strict §0.1 — a source player would feel the DoT as their core damage and our map understates it (no burn token). · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The signature 'fire damage over time' of Chthonic Fissure almost certainly IS the Ignite ailment in-game, but the guide never names the status, so burn is withheld under strict §0.1 — a source player would feel the DoT as their core damage and our map understates it (no burn token). Seeking-spirit pursuit is a behavioral delta noted but not minted (not the sole identity loop).

## le-detonating-arrow-mm — Detonating Arrow Marksman `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 1 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Volca · https://maxroll.gg/last-epoch/build-guides/blast-rain-marksman-guide; [official] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/news/last-epoch-1-0-patch-notes-released
- **t4 doors:** `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Detonating Arrow**: delivery=projectile, cadence=spam, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Multishot**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Detonating Arrow Marksman: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] The kit's real identity is a trigger-driven proc-multiplication engine (traps proc DA explosions), not a manually-fired arrow spam — mapped via GEOMETRY_PROPAGATION_cascade + linked-cast trigger grammar. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The kit's real identity is a trigger-driven proc-multiplication engine (traps proc DA explosions), not a manually-fired arrow spam — mapped via GEOMETRY_PROPAGATION_cascade + linked-cast trigger grammar. Source player feels a screen-filling explosion storm; our chain_count=2 + single door understate the density of the proc-multiply (accrual-adjacent, but no numbers filed — the proc COUNT is not a family member yet). No status token despite 'explosive' theme.

## le-erasing-strike-vk — Erasing Strike Void Knight `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: void
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @Volca · https://maxroll.gg/last-epoch/build-guides/erasing-strike-void-knight-guide
- **t4 doors:** `RESOURCE_CONVERSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Erasing Strike**: delivery=melee_arc, range=melee, cadence=spam, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#1` **Anomaly**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Erasing Strike Void Knight: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Core loop (one telegraphed void cleave, spammed via cooldown-removal + Mana regen) maps cleanly as melee_arc + RESOURCE_CONVERSION. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Core loop (one telegraphed void cleave, spammed via cooldown-removal + Mana regen) maps cleanly as melee_arc + RESOURCE_CONVERSION. Two texture losses: (a) Mark of Rot's boss-hit payload is un-tokened (name-only, unfetched); (b) Anomaly's time-replay/echo utility has no engine analog and maps only as a generic self_buff — a source player loses the 'replay your interactions' feel, but it is buff-utility, not damage identity.

## le-explosive-trap-falconer — Explosive Trap Falconer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/build-guides/explosive-ballista-falconer-guide; [official] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/news/last-epoch-1-0-patch-notes-released
- **t4 doors:** `PROXY_ASCENSION`, `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Explosive Trap**: delivery=summon_delegate, cadence=cooldown, count=1, chain=2 · conf 0.75
  - `#1` **Ballista (Explosive)**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Explosive Trap Falconer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Trap+Ballista both map `totem` (placed-proxy) — clean, but the DEPLOY-AND-DETONATE tempo (pre-place, then chain-trigger) is a placed-detonator rhythm that `totem` (a persistent emitter) approximates rather than nails. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Trap+Ballista both map `totem` (placed-proxy) — clean, but the DEPLOY-AND-DETONATE tempo (pre-place, then chain-trigger) is a placed-detonator rhythm that `totem` (a persistent emitter) approximates rather than nails. The falcon companion is a pet-rider gap (autonomous strikes not deliverable). Source player loses the falcon chip-damage and the precise trigger-detonation timing feel, but the trap-carpet identity is deliverable.

## le-fire-aura-spellblade — Fire Aura Spellblade `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** 1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/fire-aura-spellblade-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/lightning-fire-aura-rf-spellblade-build-0-8-1i/36327
- **t4 doors:** `ELEMENT_CONVERSION_MONO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Fire Aura (passive-emergent, stacked)**: delivery=aura, range=self, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Fire Aura Spellblade: aura aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Aura-pulse damage delivery maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Aura-pulse damage delivery maps clean. Source player would miss the depth-3 DPS cascade (Firebrand -> Frost Claw -> Ice Barrage), which the engine caps at chain-depth 1 — a real scaling delta, though not the core identity loop. Fire->cold Freezing-Aura conversion is captured by ELEMENT_CONVERSION_MONO. Flame Ward burst-defense button has no aura-identity role and is a rider.

## le-flame-reave-spellblade — Flame Reave Spellblade `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 0 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/flame-reave-spellblade-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/1-to-75-flame-reave-spellblade-leveling-guide-0-8-4f/47091; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/searing-blade-pure-flame-reave-spellblade-build-showcase-1-1-7-8/74646
- **t4 doors:** `GEOMETRY_COLLAPSE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Flame Reave**: delivery=zone, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Firebrand**: delivery=aura, range=self, cadence=builder_spender, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Flame Reave Spellblade: cone zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Cone melee AoE maps directly. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Cone melee AoE maps directly. Source player would miss (1) the Sunwreath cone->giant-circle transform that redefines clear geometry (approximated by GEOMETRY_COLLAPSE, not a native cone->ring swap), and (2) the aura-consume-for-mana self-refund loop (Flame Drinker) — an unusual sustain cadence the engine notes but does not natively model as an aura-spend.

## le-frost-claw — Frost Claw Sorcerer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** beta-0.8-0.9;1.0-launch · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 1 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/frostbite-frost-claw-sorcerer-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/my-best-frost-claw-nova-mage-rm-sorc/69060
- **t4 doors:** `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Frost Claw**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frost Claw Sorcerer: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Cold projectile-barrage with chill/freeze maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Cold projectile-barrage with chill/freeze maps clean. Source player would miss (1) the Elemental Nova free-proc-per-cast cascade (an on-cast linked-cast the engine approximates, not a dedicated proc-Nova), and (2) Frostbite stacking DoT — a cold damage-over-time status with no engine registry token (chill/freeze cover the CC but not the DoT). ELEMENTAL_ECHO stands in for the doubled cold-hit cadence.

## le-frost-wall-rm — Frost Wall Runemaster `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** cold · _raw_: cold
- **elements attested:** water
- **ailments attested:** chill,freeze
- **eras:** 1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 3 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/lightning-blast-runemaster-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/runemaster-question-frost-wall-spec-chill-touched-vs-pyroglass/75990
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Frost Wall**: delivery=zone, cadence=cooldown, motion_signature=lane_place, count=1 · conf 0.75
  - `#1` **Glacier**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Frost Wall Runemaster: placed lane zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Placed ice-lane with guaranteed freeze maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Placed ice-lane with guaranteed freeze maps clean. Source player would miss (1) the wall physically blocking enemy projectiles/movement (engine placed_lane is a hit-lane, not a collision barrier), and (2) the Pyroglass fire-conversion -> Brand of Trespass -> damage-multiplier Runemaster chain (a rune-interaction rider with no native lane). Control identity preserved via ZONE_CONTROL + freeze/chill.

## le-ghostflame-warlock — Ghostflame Warlock `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: necrotic
- **elements attested:** fire,shadow
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [official] maxroll.gg · https://maxroll.gg/last-epoch/news/warlock-wrap-up-falconer-teaser; [official] maxroll.gg · https://maxroll.gg/last-epoch/news/1-1-patch-notes; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/torment-warlock-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ghostflame**: delivery=zone, cadence=channel, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Bone Curse**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ghostflame Warlock: cone zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Channeled fire+necrotic cone maps clean (cone + channel tick-cost economy carry the sustained-DoT identity; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Channeled fire+necrotic cone maps clean (cone + channel tick-cost economy carry the sustained-DoT identity; PERSISTENCE_ENGINE_uptime door). [STEWARD REGRADE 2026-07-18: APPROX -> CLOSE — the APPROX rationale rested on the withheld ailment ('the ailment-free row does not carry the DoT payload'), which the m04-audit damage-type-over-time RULING dissolves: 'fire and necrotic damage over time' attests delivery TIMING, not a status; dossier attests DoT only to 'enemies in cone path' during the stream (no lingering/stacking-beyond-channel language) — the engine channel-tick cone IS that shape. Forcewave-regrade precedent.] Remaining texture drift: the defensive-channel inversion (Disdain damage-reduction-while-channeling) and the Bone Curse variant-silent aura (no curse effect fetched) are riders the engine gestures at — noted, minor.

## le-hammer-throw-paladin — Hammer Throw Paladin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** genre/hammerdin
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/an-s-tier-hammerdin-yes-please-here-ya-go-0-8-1c/32261; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/nova-hammerdin-guide; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/crit-hammerdin-paladin-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Hammer Throw**: delivery=motion, range=screen, width=wide, motion_signature=orbit_fixed, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Hammer Throw Paladin: orbit motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Orbiting physical hammers map cleanly to orbit. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Orbiting physical hammers map cleanly to orbit. Source player would miss the geometry POLYMORPHISM across variants: the mapped core is orbit, but Nova Hammerdin (Enra's + Avatar of the Spire) converts to a screen-wide nova and DISABLES orbit — the engine picks one geometry, not a stance-swap between orbit and nova. PERSISTENCE_ENGINE_uptime (audit-corrected door) carries the always-on orbit-field identity but not the orbit<->nova fork. Physical-neutral element loses the 'holy hammerdin' flavor (carried in element-slot flavor only).

## le-harvest-lich — Harvest Death Seal Lich `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: necrotic
- **elements attested:** shadow,water
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 8 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/harvest-lich-guide; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/death-seal-lich-guide
- **t4 doors:** `DEFENSIVE_TRADEOFF`, `SACRIFICE_ASCENDANCY`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Harvest (primary damage — scythe sweeps at melee range, cold)**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#1` **Flay (melee clear in Harvest Flay variant)**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#2` **Death Seal (toggle — enables Low Life playstyle, pulsing Waves of Death)**: delivery=aura, range=self, count=1 · conf 0.75
  - `#3` **Rip Blood / Reap / Bone Curse (Death Seal variant support skills)**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
  - `#4` **Reaper Form (transform — Harvest Flay variant identity)**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Harvest Death Seal Lich: melee arc melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [accepted_downgrade] Two-variant identity (Harvest Flay cold vs Death Seal necrotic) means any single motion_frame undersells one variant. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Two-variant identity (Harvest Flay cold vs Death Seal necrotic) means any single motion_frame undersells one variant. The combined folk name is a mapping convenience, not a verified single build. DEFENSIVE_TRADEOFF covers Death Seal's Low Life tradeoff identity; cold melee Reaper Form maps cleanly to water + melee_arc. Grade CLOSE reflects good geometry and element coverage but the split-build nature introduces fidelity loss. [D-7.5 chimera-split 2026-07-19 — SUB-KIT 1 of 2 :: HARVEST FLAY :: cold-melee Reaper Form loop; maps to WATER + melee_arc (per basin-2 LE dossier skill_geometry anchor). This is the cold variant of the conflated folk name.] [D-7.5 chimera-split 2026-07-19 — SUB-KIT 2 of 2 :: DEATH SEAL LICH :: necrotic Low-Life tradeoff loop; maps to DEFENSIVE_TRADEOFF (per basin-2 LE dossier capstone_alterations anchor). This is the necrotic variant.] [D-7.5 note: annotation refinement on HELD basin-2 evidence — NO legolas re-fire (Matt: 'split at migration time, no legolas re-fire'). The kit_id remains one row; any true two-kit split defers to VDM-2 LE re-crawl.]

## le-healing-hands-paladin — Healing Hands Paladin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,holy
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 1 / 0 · **dossier rows:** 6
- **citations (3):** [official] maxroll.gg · https://maxroll.gg/last-epoch/news/healing-hands-skill-tree-revealed; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/last-epoch-healing-hands-melee-crit-paladin-build-guide-1-0/64114; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/judgement-paladin-guide
- **t4 doors:** `RETRIBUTION_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Healing Hands**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#1` **Vengeance**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Healing Hands Paladin: ring zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Proc-on-melee ring burst + on-hit trigger maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Proc-on-melee ring burst + on-hit trigger maps clean. Source player would miss the heal-as-weapon DUALITY: the primary damage skill is a HEAL that also strikes — the engine ring carries the fire/holy hit and the trigger carries the proc, but the healing payload doubling as DPS is an identity the engine represents as self-sustain, not as a heal-that-is-your-damage. Rahyeh's Chariot turning Healing Hands into a MOVEMENT skill is a role-conversion rider with no core-geometry home.

## le-judgement-paladin — Judgement Paladin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** fire · _raw_: fire
- **elements attested:** fire,holy
- **ailments attested:** consecrate
- **eras:** 1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/judgement-paladin-guide; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/judgement-aura-paladin-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/holy-judgement-paladin-sentinel-build-guide-0-8-4e/46868
- **t4 doors:** `ZONE_CONTROL`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Judgement**: delivery=zone, speed=slow, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Judgement Paladin: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] fire element register — _expressed by_ `element:fire`
- **deviations:**
  - [accepted_downgrade] Ground-targeted consecrate zone maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** Ground-targeted consecrate zone maps clean. Source player would miss the ZONE-STACKING accumulation (Lingering Force multiplying overlapping Consecrated Grounds for compounding damage+healing) — the engine ground_targeted_circle places a zone but does not natively model overlapping-zone multiplication; ZONE_CONTROL approximates the control-density, not the stack-multiplier. The self-heal-within-zone duality (offense + sustain in one patch) is captured by consecrate but not the healing-scaling.

## le-lightning-blast — Lightning Blast `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/lightning-blast-runemaster-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/infinite-lightning-blast-sorc-build-guide-great-for-starting-season-and-beginners-0-9-ready/52254; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/lightning-blast-mage-beginner-friendly-build-guide-last-epoch-0-9-0/58361
- **t4 doors:** `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Lightning Blast**: delivery=beam, motion_signature=chain_hop, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Lightning Blast: chain beam identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Chain-projectile spam maps clean. · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'beam'` [green]
- **mapping deviation notes:** Chain-projectile spam maps clean. Source player would miss (1) the Spark Charge self-cascading proc-engine (Lightning Blast procs charges that proc more — an on-cast proc-loop the engine only approximates via chain, not a dedicated charge-cascade), and (2) the Reowyn's Frostguard on-cast Ward burst (Runemaster variant) — a defensive on-cast rider with no native engine lane. Neither breaks the core loop; both are riders. ELEMENTAL_ECHO gestures at the repeated-hit lightning identity.

## le-shift-bladedancer — Shift Bladedancer `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** execute
- **eras:** beta-0.8-0.9;1.0-launch;1.1-harbingers;1.4-omens · **tier:** — · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @McFluffin (reviewed by Lizard_IRL) · https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide; [authored] maxroll.gg · @Terek · https://maxroll.gg/last-epoch/build-guides/bladedancer-leveling-guide
- **t4 doors:** `MOMENTUM_CASCADE`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shift**: delivery=motion, cadence=cooldown, motion_signature=straight_line, count=1 · conf 0.75
  - `#1` **Shadow Cascade**: delivery=zone, motion_signature=burst_around_self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shift Bladedancer: blink motion identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Minor drift: Shadow Daggers stack payoff unexpressed (no home) and Umbral Blades rider unmapped (name-only); · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Minor drift: Shadow Daggers stack payoff unexpressed (no home) and Umbral Blades rider unmapped (name-only); core loop - blink traversal with on-arrival ring payload, linked-cast riders, execute threshold - is native.

## le-smite-paladin — Smite Paladin `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** holy,lightning
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Volca · https://maxroll.gg/last-epoch/build-guides/smite-paladin-guide; [communal] odealo.com · https://odealo.com/articles/smiter-paladin-last-epoch-build
- **t4 doors:** `RESOURCE_CONVERSION`, `NETWORK_AMPLIFIER`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Smite**: delivery=projectile, motion_signature=straight_line, count=1, chain=2 · conf 0.75
  - `#1` **Holy Aura**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Smite Paladin: single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: missing-Mana damage substrate approximated via gear-numeric lane pending steward candidate; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Minor drift: missing-Mana damage substrate approximated via gear-numeric lane pending steward candidate; holy is carried by the aura skill while Smite itself rides lightning. The proc-storm loop (hit -> sky-bolt at target) is native trigger grammar.

## le-storm-totem-shaman — Storm Totem Shaman `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning,wind
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 4 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @BinaQc · https://maxroll.gg/last-epoch/build-guides/tornado-shaman-guide; [authored] maxroll.gg · @BinaQc · https://maxroll.gg/last-epoch/build-guides/totem-shaman-guide
- **t4 doors:** `ZONE_CONTROL`, `PROXY_FISSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tornado**: delivery=summon_delegate, speed=fast, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Storm Totem Shaman: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Minor drift: tornado-as-mobile-weather flavor rides a stationary placed-emitter token (no wandering behavior attested, so no pursuit delta); · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Minor drift: tornado-as-mobile-weather flavor rides a stationary placed-emitter token (no wandering behavior attested, so no pursuit delta); autonomous per-zone bolt targeting is texture inside the emitter grammar. Placement loop, multi-zone coverage, and lightning payload are native.

## le-swarmblade-druid — Swarmblade Druid `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 3 · **dossier rows:** 6
- **citations (4):** [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/lightning-swarmblade-druid-guide; [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/frostbite-swarmblade-druid-guide; [authored] forum.lastepoch.com · @boardman21 · https://forum.lastepoch.com/t/1-to-76-swarmblade-locust-swarm-leveling-guide-0-9-2/61104; [official] forum.lastepoch.com · @elevengames-official · https://forum.lastepoch.com/t/druid-overhaul-overview-and-swarmblade-form/45307
- **t4 doors:** `MOMENTUM_CASCADE`, `PERSISTENCE_ENGINE_uptime`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Swarmblade Form**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Armblade Slash**: delivery=melee_arc, range=melee, cadence=spam, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#2` **Swarm Strike**: delivery=zone, width=wide, motion_signature=burst_around_self, count=1 · conf 0.75
  - `#3` **Locust Swarm**: cadence=spam, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Swarmblade Druid: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Swarm-entity texture thinned: Swarm Strike 360-finisher maps as ring; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Swarm-entity texture thinned: Swarm Strike 360-finisher maps as ring; Locust Swarm cycle is shape-silent (null row); Tornado proc payload carried as rider note; form-entry moment compressed into self_buff chassis. Loop verb (in-form melee spam + nova finisher + Rage pressure) survives intact -- that build.

## le-warpath-vk — Warpath Void Knight `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** chaos-poison · _raw_: void
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.1-harbingers;1.4-omens · **tier:** T1 · **lineage:** genre/spin
- **verify (C/X/U):** 7 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/echo-warpath-void-knight-guide; [authored] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/echo-warpath-void-knight-build-0-8-3b/43691; [communal] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/dual-wield-warpath-void-knight-0-8-1e-build-suggestions/35198
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `MOMENTUM_CASCADE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Warpath**: delivery=motion, range=melee, width=wide, cadence=channel, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#1` **Devouring Orb**: delivery=motion, motion_signature=orbit_fixed, count=1 · conf 0.75
  - `#2` **Abyssal Echoes**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Warpath Void Knight: whirlwind motion identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Void Essence -> Void Well sub-resource feedback compressed into regen_shape note; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'motion'` [green]
- **mapping deviation notes:** Void Essence -> Void Well sub-resource feedback compressed into regen_shape note; auto-cast-on-move nearest-mapped (AUTOCAST_ON_MOVE token); Anomaly/Symbols buff-layer texture thinned. Core loop (move-while-spinning tick-drain field + orbiting orb + ramp) maps near-natively -- that build.

## le-werebear-druid — Werebear Druid `[class:record]`

- **grade / terminal:** `CLOSE` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 8 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/swipe-werebear-druid-guide; [authored] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/earthquake-werebear-is-back-build-guide-0-8-4/46282; [authored] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/build-melee-druid-werebear-wip-0-7-2/15463
- **t4 doors:** `MOMENTUM_CASCADE`, `GEOMETRY_PROPAGATION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Werebear Form**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Swipe**: delivery=melee_arc, range=melee, cadence=spam, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#2` **Aftershock (proc)**: delivery=melee_arc, range=melee, cadence=spam, motion_signature=point_strike, count=1 · conf 0.75
  - `#3` **Warcry**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Werebear Druid: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Bear-form visual + Rampage traversal texture thinned; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Bear-form visual + Rampage traversal texture thinned; Earthquake-as-idol-scaler compressed into a delivery note; chance-roll proc kept as threshold trigger. In-form loop (melee arc spam + proc quakes + Rage pressure + DR stacking) survives intact -- that build.

## le-dive-bomb-falconer — Dive Bomb Falconer `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 7 / 0 / 0 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @LizardIRL · https://maxroll.gg/last-epoch/build-guides/dive-bomb-falconer; [official] maxroll.gg · @unknown · https://maxroll.gg/last-epoch/news/last-epoch-1-0-patch-notes-released
- **t4 doors:** `COMPANION_CONTRACT`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Dive Bomb**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
  - `#1` **Aerial Assault**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Dive Bomb Falconer: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] MANDATORY (APPROX): the falcon is a persistent autonomous companion — its between-command autonomous Falcon Strikes and the shadow-falcon phantom overlaps are core to the build's sustained DPS but fall in the engine summoner-deferral GAP (autonomous-combatant delivery deferred). · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** MANDATORY (APPROX): the falcon is a persistent autonomous companion — its between-command autonomous Falcon Strikes and the shadow-falcon phantom overlaps are core to the build's sustained DPS but fall in the engine summoner-deferral GAP (autonomous-combatant delivery deferred). Mapped the COMMANDED Dive Bomb strike as the deliverable core; a source player would MISS the constant falcon-autonomy chip damage and the boss-phase phantom-overlap burst that our single commanded-strike mapping cannot express. APPROX not GAPPED — the commanded strike IS deliverable (R-M7 player-test: 'that build, worse', not 'not that build'); terminal MAPPED not DOCKET.

## le-reaper-form-lich — Reaper Form Lich `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: necrotic
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 3 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @Volca (reviewed by Lizard_IRL) · https://maxroll.gg/last-epoch/build-guides/harvest-lich-guide
- **t4 doors:** `PERSISTENCE_ENGINE_uptime`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Reaper Form**: delivery=aura, range=self, count=1 · conf 0.75
  - `#1` **Harvest**: delivery=melee_arc, range=melee, motion_signature=arc_sweep, count=1 · conf 0.75
  - `#2` **Flay**: delivery=projectile, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Reaper Form Lich: self buff aura identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] Source player would miss the transform frame and the dramatic form-break/re-entry cycle; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Source player would miss the transform frame and the dramatic form-break/re-entry cycle; decay race approximated as tick-cost persistent condition sustained by leech. The in-form loop itself (scythe melee arc + secondary projectile + uptime economy) carries intact.

## le-ring-of-shields — Ring of Shields / Sentinel Guard `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers · **tier:** — · **lineage:** —
- **verify (C/X/U):** 2 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] icy-veins.com · https://icy-veins.com/last-epoch/forge-guard-overview; [communal] estnn.com · https://estnn.com/all-sentinel-builds-in-last-epoch/; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/ring-of-shields-and-forge-guard-interactions/71851
- **t4 doors:** `PROXY_FISSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Ring of Shields**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Ring of Shields / Sentinel Guard: self buff aura identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Shields-as-HP-entities absorbing hits and redirecting enemy aggression are not natively modeled; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'aura'` [green]
- **mapping deviation notes:** Shields-as-HP-entities absorbing hits and redirecting enemy aggression are not natively modeled; engine approximation = defensive self-buff + deflect rider. Source player would miss the bodyguard-entity feel and per-shield attrition.

## le-runic-invocation — Runic Invocation Runemaster `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** fire,lightning,water
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/hydrahedron-runemaster-guide; [communal] dotesports.com · https://dotesports.com/last-epoch/news/last-epoch-all-runic-invocations-listed
- **t4 doors:** `RESOURCE_CONVERSION`, `ELEMENTAL_ECHO`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Runic Invocation**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Runic Invocation Runemaster: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] The combinatorial identity (~40 outputs selected by specific rune sequences / spell rotations) has no engine lane; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
- **mapping deviation notes:** The combinatorial identity (~40 outputs selected by specific rune sequences / spell rotations) has no engine lane; realized loop approximated as accumulator-spend into one payoff zone. Source player would miss choosing WHICH output via rotation ordering. Terminal stays MAPPED per R-M7 (that build, worse - the rotate-then-nuke loop survives).

## le-shadow-bladedancer — Shadow Bladedancer `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** execute
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 3 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @BinaQc · https://maxroll.gg/last-epoch/build-guides/shadow-cascade-bladedancer-guide; [authored] maxroll.gg · @McFluffin (reviewed by Lizard_IRL) · https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide
- **t4 doors:** `PROXY_FISSION`, `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Synchronized Strike**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
  - `#1` **Shift**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shadow Bladedancer: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Shadows echoing the player's own attacks in sync is approximated as placed emitters striking nearby - source player would miss the mirror-choreography feel; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
- **mapping deviation notes:** Shadows echoing the player's own attacks in sync is approximated as placed emitters striking nearby - source player would miss the mirror-choreography feel; Shadow Daggers stacking payoff is unexpressed (no registry home).

## le-shield-bash-le — Shield Bash (LE) `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 4 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @Volca · https://maxroll.gg/last-epoch/build-guides/shield-bash-forge-guard-guide; [communal] forum.lastepoch.com · @DaddyLuvsYou · https://forum.lastepoch.com/t/build-forge-guard-shield-bash-v1-3-2/79874/12
- **t4 doors:** `RETRIBUTION_ENGINE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shield Bash**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Ring of Shields**: delivery=aura, range=self, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shield Bash (LE): melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] The block-cap chase AS the damage-scaling verb (defense stat converting to a more-damage multiplier) is unexpressed - approximated as flat numeric scaling; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** The block-cap chase AS the damage-scaling verb (defense stat converting to a more-damage multiplier) is unexpressed - approximated as flat numeric scaling; source player would miss capping block being offense. Core loop (single-target melee spam behind a defensive wall) carries.

## le-shield-throw-time-rot-vk — Shield Throw Time Rot VK `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: void
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 1 · **dossier rows:** 6
- **citations (1):** [authored] maxroll.gg · @Volca · https://maxroll.gg/last-epoch/build-guides/time-rot-void-knight-guide
- **t4 doors:** `ELEMENT_CONVERSION_MONO`, `PERSISTENCE_ENGINE_saturation`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Shield Throw**: delivery=projectile, motion_signature=ricochet_return, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Shield Throw Time Rot VK: ricochet bounce projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The named Time Rot ailment (the build's payload identity) is unexpressed pending a steward row - source player would miss the stacking void-rot on the boss; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The named Time Rot ailment (the build's payload identity) is unexpressed pending a steward row - source player would miss the stacking void-rot on the boss; delivery (void ricochet shuttle) and set-bonus scaling carry via geometry + gear lane.

## le-soul-feast — Soul Feast (as primary) `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** chaos-poison · _raw_: necrotic
- **elements attested:** shadow
- **ailments attested:** drain
- **eras:** 1.0-launch;1.1-harbingers;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 3 / 0 / 4 · **dossier rows:** 6
- **citations (2):** [authored] icy-veins.com · @GhazzyTV · https://icy-veins.com/last-epoch/warlock-soul-feast-torment-endgame-build; [communal] progameguides.com · https://progameguides.com/last-epoch/warlock-skills-tier-list-in-last-epoch/
- **t4 doors:** `RESONANCE_LOOP`, `RESOURCE_CONVERSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Soul Feast**: delivery=projectile, motion_signature=straight_line, count=1, chain=2 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Soul Feast (as primary): single target projectile identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [accepted_downgrade] The automated multi-skill chain compresses to carrier + linked-cast grammar because the proc skills' own behaviors are unfetched - source player would miss the distinct fissure/bolt/blood visuals and coverage; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** The automated multi-skill chain compresses to carrier + linked-cast grammar because the proc skills' own behaviors are unfetched - source player would miss the distinct fissure/bolt/blood visuals and coverage; the felt loop (one button, curse-fed drain, Ward stream) carries via grammar + proc-loop economy.

## le-tempest-strike — Tempest Strike `[NEGATIVE, class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** lightning · _raw_: lightning
- **elements attested:** lightning
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [authored] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/tempest-strike-shaman-build-last-epoch-patch-0-7-7f/19451; [official] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/news/gathering-storm-tempest-strike-rework; [communal] forum.lastepoch.com · @multiple-community · https://forum.lastepoch.com/t/question-for-a-build-lightning-primalist-shaman-with-tempest-strike/79364
- **t4 doors:** `TEMPORAL_CHARGE`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Tempest Strike**: delivery=melee_arc, range=melee, motion_signature=point_strike, count=1 · conf 0.75
  - `#1` **Sky Opener (Storm Stack spender)**: cadence=builder_spender, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Tempest Strike: melee strike melee_arc identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] lightning element register — _expressed by_ `element:lightning`
- **deviations:**
  - [accepted_downgrade] Source player would miss the fixed 3-beat combo rhythm -- the deterministic HIT-HIT-TEMPEST cadence has no native beat-counter; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'melee_arc'` [green]
- **mapping deviation notes:** Source player would miss the fixed 3-beat combo rhythm -- the deterministic HIT-HIT-TEMPEST cadence has no native beat-counter; nearest-mapped as on-hit-threshold + accumulator, which reads as threshold/chance rather than counted beats. Fixed-attack-speed -> crit overflow conversion also lost (noted in economy). Loop skeleton (melee -> periodic self-AoE lightning -> stack payoff) survives: that build, worse.

## le-umbral-blades — Umbral Blades Rogue `[class:record]`

- **grade / terminal:** `APPROX` / `MAPPED`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 6 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [authored] forum.lastepoch.com · @boardman21 · https://forum.lastepoch.com/t/umbral-blades-bladedancer-build-guide-0-8-4/46067; [authored] forum.lastepoch.com · @unknown-op · https://forum.lastepoch.com/t/umbral-blades-bladedancer-rogue-build-guide-0-8-4c/46537; [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide
- **t4 doors:** `ZONE_CONTROL`, `PROXY_FISSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Umbral Blades**: delivery=projectile, motion_signature=fan_spread, count=1 · conf 0.75
  - `#1` **Shift**: delivery=motion, motion_signature=straight_line, count=1 · conf 0.75
  - `#2` **Synchronized Strike**: count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Umbral Blades Rogue: multi projectile projectile identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [accepted_downgrade] Source player would miss the recall: engine multi_projectile throws OUT only -- the plant-blades-then-sweep-them-back-through-enemies rhythm (the kit's econ_raw identity, 'field-plant-recall') has no native return leg; · downgrade-owner `elrond (W4 LE tranche; internal-consistency reconcile, no W1 evidence — W5 is LE's external check)`
- **acceptance asserts:**
  - `primary_delivery_class == 'projectile'` [green]
- **mapping deviation notes:** Source player would miss the recall: engine multi_projectile throws OUT only -- the plant-blades-then-sweep-them-back-through-enemies rhythm (the kit's econ_raw identity, 'field-plant-recall') has no native return leg; carried in notes + out-and-return accrual. Shadow-clone mirror-discharge softens to a linked-cast echo. Throw-scatter + traversal-proc skeleton survives: that build, worse -- not GAPPED (R-M7 player test).

## le-low-life-ward — Low-Life Ward (archetype) `[is_system, class:system]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** _(unassigned)_ · _raw_: n/a
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 1 · **dossier rows:** 6
- **citations (3):** [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/need-expert-info-on-low-life-aka-exsanguinous-last-steps-gear/36700; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/spark-charge-runemaster-guide; [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/fire-aura-spellblade-guide
- **t4 doors:** `DEFENSIVE_TRADEOFF`
- **mapping deviation notes:** Source player would lose the ENTIRE identity: the whole build IS 'drop HP to near-zero, convert missing-health into a giant Ward wall.' Engine has no ward-from-missing-health generation and no low-life inversion economy — nothing of the loop survives. DEFENSIVE_TRADEOFF is the nearest T4 door but only gestures at 'trade life for defense'; it does not reproduce the inverted-stat scaler.

## le-manifest-armor — Manifest Armor Forge Guard `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 4 · **dossier rows:** 6
- **citations (2):** [communal] maxroll.gg · https://maxroll.gg/last-epoch/build-guides/manifest-armor-forge-guard-guide; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/wrouks-manifest-armor-forge-guard-tankiest-build-in-the-game-last-epoch-build-guide/32913
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Manifest Armor**: count=1 · conf 0.75
  - `#1` **Forge Strike**: delivery=zone, motion_signature=ground_place, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Manifest Armor Forge Guard: ground targeted circle zone identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] MANDATORY (GAPPED): the kit IS 'summon one autonomous gear-scaled construct and let it fight' — an autonomous-combatant pet, which the engine defers by design (summoner-deferral). → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'zone'` [green]
  - `expresses: MANDATORY (GAPPED): the kit IS 'summon one autonomous gear-scaled construct and ` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** MANDATORY (GAPPED): the kit IS 'summon one autonomous gear-scaled construct and let it fight' — an autonomous-combatant pet, which the engine defers by design (summoner-deferral). The whole identity (a persistent construct that pursues and attacks on its own, scaled by YOUR worn gear) has no engine delivery: null geometry is the honest read. A source player has 'not that build' — there is no engine analog to a gear-stat-scaled autonomous construct. PROXY_ASCENSION names the proxy-ambition but the engine has no autonomous-combatant to ascend. The gear-stat-as-minion-scaling is separately docketed. Forge Strike (anvil ground-slam) survives as a bolt-on but is not the mapped identity.

## le-skeleton-necro — Skeleton Necromancer `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** water
- **ailments attested:** _(none)_
- **eras:** beta-0.8-0.9;1.0-launch;1.4-omens · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (3):** [authored] maxroll.gg · @VisionGL · https://maxroll.gg/last-epoch/build-guides/skeletal-roid-mage-necromancer-guide; [authored] icy-veins.com · @GhazzyTV · https://icy-veins.com/last-epoch/necromancer-skeletal-frost-mage-endgame-build; [communal] forum.lastepoch.com · https://forum.lastepoch.com/t/skeletal-mage-sacrifice-necromancer-300-corruption-last-epoch-build-guide-patch-8-3/45716
- **t4 doors:** `PROXY_ASCENSION`, `PROXY_FISSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Skeletal Mage**: count=1 · conf 0.75
  - `#1` **Summon Skeleton**: count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Skeleton Necromancer: pet-core delivery identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] water element register — _expressed by_ `element:water`
- **deviations:**
  - [engine_inexpressible] R-M7 player test: 'not that build' - the entire kit IS autonomous combatants ('Summon Skeletal Mage is the core of this build, and all other skills revolve around... → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `kit_identity_present == true` [green]
  - `expresses: R-M7 player test: 'not that build' - the entire kit IS autonomous combatants ('S` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** R-M7 player test: 'not that build' - the entire kit IS autonomous combatants ('Summon Skeletal Mage is the core of this build, and all other skills revolve around... your Archmage'); engine summoner-deferral gap means no honest delivery token exists. Null geometries + docket per post-W1 gapped-pet lane; autonomy gap filed to mechanic_gap_docket.

## le-squirrel-bm — Squirrel Beastmaster `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** physical · _raw_: physical
- **elements attested:** _(silent)_
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 5 / 0 / 2 · **dossier rows:** 6
- **citations (2):** [authored] maxroll.gg · @LizardIRL · https://maxroll.gg/last-epoch/build-guides/squirrel-beastmaster-guide; [communal] forum.lastepoch.com · @boardman21 · https://forum.lastepoch.com/t/last-epoch-raging-squirrels-beastmaster-build-guide-0-9-2/61272
- **t4 doors:** `COMPANION_CONTRACT`, `PROXY_FISSION`
- **t4 delta:** shape `step` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Squirrels**: speed=fast, count=1 · conf 0.75
  - `#1` **Summon Frenzy Totem**: delivery=summon_delegate, cadence=cooldown, count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Squirrel Beastmaster: totem summon_delegate identity — _expressed by_ `geometry.delivery_class`
- **deviations:**
  - [engine_inexpressible] R-M7 player test: 'not that build' - the swarm IS the kit (defining unique exists only to double companion count) and autonomous-companion delivery is the engine's summoner-deferral gap; → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `primary_delivery_class == 'summon_delegate'` [green]
  - `expresses: R-M7 player test: 'not that build' - the swarm IS the kit (defining unique exist` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** R-M7 player test: 'not that build' - the swarm IS the kit (defining unique exists only to double companion count) and autonomous-companion delivery is the engine's summoner-deferral gap; the mappable remainder (one buff totem) is support texture, not the build.

## le-wraithlord-necro — Wraithlord Necromancer `[class:record]`

- **grade / terminal:** `GAPPED` / `MAPPED_DOCKET`
- **element (court):** chaos-poison · _raw_: necrotic
- **elements attested:** shadow
- **ailments attested:** _(none)_
- **eras:** 1.0-launch;1.1-harbingers;1.2-woven · **tier:** T1 · **lineage:** —
- **verify (C/X/U):** 4 / 0 / 6 · **dossier rows:** 6
- **citations (4):** [authored] maxroll.gg · @maxroll-staff · https://maxroll.gg/last-epoch/build-guides/wraith-necromancer-guide; [communal] forum.lastepoch.com · @multiple-community · https://forum.lastepoch.com/t/wraithlord-is-busted/63932; [communal] forum.lastepoch.com · @multiple-community · https://forum.lastepoch.com/t/in-search-of-flame-wraiths/70666; [communal] forum.lastepoch.com · @multiple-community · https://forum.lastepoch.com/t/need-help-understanding-top-1-necromancer-build-on-let/66838
- **t4 doors:** `PROXY_ASCENSION`
- **t4 delta:** shape `ramp` (signoff: unvalidated)
- **skill geometry bands:**
  - `#0` **Summon Wraith (fed)**: count=1 · conf 0.75
  - `#1` **Wraithlord (Harbour-enabled)**: cadence=channel, count=1 · conf 0.75
  - `#2` **Drain Life**: count=1 · conf 0.75
  - `#3` **Dread Shade / Aura of Decay**: count=1 · conf 0.75
- **recognition hooks:**
  - `H1` [geometry/expressed] Wraithlord Necromancer: pet-core delivery identity — _expressed by_ `geometry.delivery_class`
  - `H2` [register/expressed] shadow element register — _expressed by_ `element:shadow`
- **deviations:**
  - [engine_inexpressible] Nothing of the loop survives natively: autonomous-combatant delivery is a known engine gap (summoner-deferral), and the consumption-feed economy (sacrifice summon stock to empower one capped boss-proxy) has no lane. → _fix_ `new_door_rfc`
- **acceptance asserts:**
  - `kit_identity_present == true` [green]
  - `expresses: Nothing of the loop survives natively: autonomous-combatant delivery is a known ` [red] · expected: RED until engine lane exists (routed to docket)
- **mapping deviation notes:** Nothing of the loop survives natively: autonomous-combatant delivery is a known engine gap (summoner-deferral), and the consumption-feed economy (sacrifice summon stock to empower one capped boss-proxy) has no lane. PROXY_ASCENSION gestures at the ascended-proxy fantasy but cannot host the wraith-stream harvest. Source player would find no wraiths, no Wraithlord, no feed loop -- not that build.

