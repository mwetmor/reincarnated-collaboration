# Pull-Intrinsic Class-Kit Tranche
## Edition-II Evidence: Fully Legible Class-Kit Rows

**Date:** 2026-07-15
**Mode:** B (systematic catalogue crawl — targeted genre sweep)
**Commissioner:** Gandalf (Edition-II §10.2 chain, Matt-authorized 2026-07-15)
**Evidence bar:** Skill / rune / talent / class level ONLY — intrinsic to class-kit identity.
  Gear-assembled pull documented in Exclusions section; NOT as kit rows.
**Corpus prefix:** `la-` (new source — Lost Ark, no prior prefix); D3/DI rows are enrichment notes
  against existing corpus rows (`di-cyclone-monk-pvp`, `d3-zbarb`), NOT new rows.
**pull_pending_vocab:** true on all rows (elrond resolves at v1.2 keying)

**Sources per row documented in `source_url` field. All source access: 2026-07-15.**

---

## Tranche Table — Intrinsic Pull Class-Kit Rows

| kit_id | source | display_name | class | skill_name | movement_verb | delivery | geometry | tempo | commit | attribute | element | treatment | anchor_flavor | cooldown_s | resource_economy | containment_notes | mech_note | pull_pending_vocab | source_url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| la-destroyer-vortex-gravity | lost-ark | Destroyer — Vortex Gravity | Destroyer (Warrior/Heavy) | Vortex Gravity | rooted | melee | radial-nova (6m pull radius; hammer slam + gravitational explosion in front) | instant | instant (no charge — fires on Hypergravity Mode activation) | STR | Physical/Gravity | hybrid (pull-to-self + damage; Stagger=High; Armor Destruction 12% debuff ~180s; the pull and damage fire together on the same cast; neither half is configurable-out) | pull-to-self | 20 | Hypergravity Mode gate (identity meter must be full); left-click basic attacks feed DPS while VG provides pull+stagger burst | CC-res: not specified; elite immunity: not specified (raid boss centric — modest 6m pull has limited boss leverage); Hypergravity Mode grants full CC/debuff immunity to the Destroyer while active | Destroyer's identity skill. Hammer slams down inflicting physical damage + explodes gravitational energy in front, pulling foes within 6m. High stagger. Debuffs enemy armor. In Hypergravity Mode, all other skills disabled — only basic attack and Vortex Gravity available. The pull is the core identity mechanic, not an add-on. Damage is real but secondary to pull+stagger function. Assessment: closest to treatment=hybrid of any intrinsic kit found — pull and damage co-fire on same cast with no configurable separation; Hypergravity also area-slows all enemies in range, compounding density. | true | https://lostarkcodex.com/us/skill/18011/ |
| la-destroyer-gravity-impact | lost-ark | Destroyer — Gravity Impact | Destroyer (Warrior/Heavy) | Gravity Impact | rooted | melee | radial-point-blank (multi-pull sequence; caster stationary; enemies drawn in 8× then explosion) | wind-up | channel (8-hit gravitational pull sequence over ~2–3s before explosion) | STR | Physical/Gravity | damage-primary, pull-rider (pull delivers the 8× hit density; damage is the primary output; explosion caps the sequence) | pull-to-self | 12 | Gravity Core generation (+2 on hit); Concentration skill (blue) — does NOT spend cores, generates them | Paralysis Immunity (super armor) during cast — Destroyer rooted while channeling; CC-res: not specified; Tier III tripod expands attack range up to 40% | Concentration skill. Caster stationary; gravitational field forms at caster location. Enemies pulled in 8 times (195.2 dmg total) then gravitational explosion pulls remaining foes + 63 dmg. Generates 2 Gravity Cores. Tripod options: Gravity Echo adds 2s stun on initial explosion; Will Enhancement strengthens pull force; Tier III expands range. This is the Destroyer's core builder skill — pull as density mechanic for multi-hit damage. | true | https://lostark.wiki.fextralife.com/Gravity+Impact |
| la-destroyer-gravity-force | lost-ark | Destroyer — Gravity Force | Destroyer (Warrior/Heavy) | Gravity Force | walk (partial — free to reposition between phases per source) | melee | linear-pull (frontal swing releases gravitational energy along straight line 7×; enemies pulled to a nearby position) | wind-up | wind-up (initial frontal swing then 7 gravitational pull attacks along line) | STR | Physical/Gravity | damage-primary, pull-rider (linear pull groups enemies along axis for multi-hit damage chain) | pull-to-point (along axis) | 14 | Gravity Core generation (+2 on hit); Concentration skill — generates not spends | Paralysis Immunity (super armor); 14s cooldown; Tripod: Toughened Body gives 40.8% damage reduction during cast — implies sustained exposure while channeling the 7-hit sequence | Concentration skill. Swings hammer releasing gravitational energy in a straight line; gravitational energy attacks foes 7× (206.4 dmg total) pulling them close along the axis. Generates 2 Gravity Cores. Geometry is LINEAR not radial — pull toward a point along a line rather than toward the caster. Tripod options: Fatal Strength (+40% outgoing dmg), attack speed, shield, debuffs. Two-phase: initial hammer swing (35 dmg) + gravitational energy chain (206.4). | true | https://lostark.wiki.fextralife.com/Gravity+Force |
| la-destroyer-gravity-compression | lost-ark | Destroyer — Gravity Compression | Destroyer (Warrior/Heavy) | Gravity Compression | rooted | melee | point-blast (black hole forms at targeted location up to 10m from caster; 5–6m explosion radius; hits up to 9×) | wind-up | channel (hold 2s to release; initial gravitational wave on press; full charge releases black hole over 9 hits) | STR | Physical/Gravity | damage-primary (no explicit pull on living enemies in base description; explosion hits are multi-strike at black hole position; Gravity Release = spender skill) | pull-to-point (black hole location; enemies hit by the 9-hit sequence at that point) | 24 | Gravity Core spender (Gravity Release type — purple, consumes cores); Highest stagger rating | Paralysis Immunity during cast; Stagger = Highest; Part Break Level 2; long 24s cooldown; Move Position tripod (T3) changes black hole creation point to cursor up to 10m away | Gravity Release skill (spender, purple icon). Thrust hammer into ground, release gravitational wave (29 dmg), then hold 2s to release black hole (265.4 dmg over up to 9 hits). Very high stagger. The pull mechanic is implicit (9 hits at the black hole location suggest sustained enemy magnetism to the impact zone) rather than an explicit "enemies moved toward caster" description. Highest stagger damage of the Destroyer skill set. Move Position tripod makes it a placed black hole rather than self-centered — pull-to-point when modified. | true | https://lostark.wiki.fextralife.com/Gravity+Compression |
| d4-spiritborn-vortex | diablo-4 | Spiritborn — Vortex | Spiritborn (Vessel of Hatred DLC) | Vortex | unknown (not documented in available sources) | ranged/targeted | radial-vortex (cyclone that pulls enemies inward + crushing downdraft; "larger area" upgrade option implies fixed-radius default) | instant | instant (no charge indicated; 12s cooldown is cooldown not charge time) | DEX/WIS (Spiritborn scales Jaguar/Eagle/Gorilla/Centipede — element is Lightning = Eagle spirit) | Lightning | damage-primary, pull-rider (pull clusters enemies; downdraft delivers damage; upgrade path scales damage 200% suggesting pull is density mechanic) | pull-to-point (center of cyclone, player-targeted) | 12 | Vigor generation (20 via upgrade); Lucky Hit 20%; 12s base CD; CD reduced 1s per crit (via upgrade) | No elite immunity documented; 1000 Year Storm upgrade: +5s cooldown penalty + 20% damage reduction trade-off for 200% dmg increase + 50% larger area; Knock Down 2s available via upgrade | Spiritborn Focus skill (intrinsic class skill tree — NOT gear/aspect assembled). Creates cyclone at targeted location that pulls enemies inward followed by crushing downdraft (35% → 171% dmg at rank 15). Lightning element. Multiple upgrade paths including area expansion, knockdown, damage amplification. Full upgrade tree: Enhanced Vortex (next skill +20% dmg); upgrades branch to Overcharged (Vulnerable+Spark), 1000 Year Storm (200% dmg boost), or Insect Swarm (converts to Poison/Centipede). This is the only intrinsic pull skill found in D4's base class skill trees. | true | https://diablo4.wiki.fextralife.com/Vortex |
| d3-wizard-black-hole | diablo-3 | Wizard — Black Hole | Wizard | Black Hole | rooted (cast animation; ground-targeted placement) | ranged | radial-point (black hole placed at target location; 15–20y radius pulls enemies to center; duration 2s) | instant | instant (20 arcane power + 12s cooldown; cast time is the placement animation only) | INT | Arcane | damage-primary, pull-rider (pull groups enemies at point; 700–1290% weapon damage arcane over 2s is the primary output) | pull-to-point (center of placed black hole) | 12 | 20 Arcane Power; 12s cooldown; no charges; counts as Knockback (triggers Strongarm Bracers damage buff) | 12s cooldown floor; pull counts as knockback (implies CC-resistance accumulation on targets); elite immunity: not explicitly documented but per-enemy 5s immunity similar to Ranslor's not confirmed for Black Hole; solo skill (not group-meta due to CD) | Wizard offensive skill. Conjures black hole at ground-targeted location that draws enemies in and deals 700% weapon damage as Arcane over 2s to all within 15y. Counts as Knockback — triggers Strongarm Bracers +25% damage buff. Runes: Supermassive (20y radius, 1290% dmg, Lightning); Absolute Zero (Cold, +3% cold dmg per enemy hit stacking); Event Horizon (absorbs enemy projectiles + objects + +3% dmg per enemy hit, 5s); Blazar (Fire, 170% + 454% explosion after dissipation); Singularity (additional 300% dmg, standard arcane). Community note: considered underpowered relative to cooldown cost; primarily solo-play utility. | true | https://diablo.fandom.com/wiki/Black_Hole |
| di-cyclone-strike-monk-base | diablo-immortal | DI Monk — Cyclone Strike (base) | Monk | Cyclone Strike | rooted-while-charging (charge mechanics; longer charge = greater range and damage; rooted implied by charge type and PvE rotation requiring Imprisoned Fist lock before charging) | melee | radial-nova (vortex of wind centered on caster; radius increases with charge duration; base radius unknown, charged radius ~documented-implosion equivalent in D3 at up to 34y-class) | wind-up | wind-up (Charge type skill — "Charging longer increases range and damage"; fully charged = full pull range) | DEX | Holy/Physical (Wind) | hybrid (pull and damage co-fire; base skill intrinsically pulls AND damages in same cast; essence variants modify which half dominates — Storm Spirit = damage-only, Frigid Cyclone = pull+freeze; but the BASE has both) | pull-to-self | 12 | 2 charges; 12s cooldown per charge; base skill is Charge type (hold to charge) | Charge type = Monk slowed/rooted during charge-up; 12s cooldown; 2 charges available; CC-resistance in PvP with repeated use noted by community; essence variants that modify pull (Tempest's Heart: pull + detonate; Frigid Cyclone: pull + freeze) are gear-assembled via Legendary chest armor and are EXCLUDED from this row per evidence bar | Base (unmodified) Cyclone Strike: "Generate a vortex of wind which pulls in enemies and deals damage. Charging longer increases range and damage." Keywords: Gather, Charge. Unlock Level 1. The pull IS intrinsic to the base skill — no legendary required. Essence variants (Storm Spirit, Driven Thunder, Tempest's Heart, Frigid Cyclone, Mystic Winds, Sandstorm) are ALL gear-assembled (equipping specific Legendary chest armor) and documented in Exclusions. The base skill is the intrinsic evidence row. NOTE: existing corpus row `di-cyclone-monk-pvp` covers the PvP/helicopter build — this row captures the BASE SKILL MECHANICS layer that was missing from that enrichment pass. See Enrichment Notes section. | true | https://diabloimmortal.wiki.fextralife.com/Cyclone_Strike |

---

## Enrichment Notes — Existing Corpus Rows

These in-corpus kit rows already exist. No new rows emitted. Enrichment facts document what probe facts are MISSING or confirmed-incomplete in the existing record.

### `di-cyclone-monk-pvp` (Diablo Immortal Cyclone Strike Monk, PvP context)

**What the existing row likely captures:** PvP helicopter build, Driven Thunder essence variant, CC immunity combination, PvP balance signal.

**Missing probe facts (enrichment):**
- Base skill cooldown: **12 seconds, 2 charges** (not in prior probe notes)
- Commit type: **wind-up / Charge** (hold to charge; "charging longer increases range and damage")
- Movement verb: **rooted-while-charging** (player immobile during charge-up per PvE rotation evidence — Imprisoned Fist lock-then-charge is the documented sequence)
- Geometry: **radial-nova from caster** (vortex centered on Monk; radius scales with charge duration)
- Anchor flavor: **pull-to-self** (enemies drawn to Monk's location)
- Base skill pull is INTRINSIC (no Legendary required) — the `di-cyclone-monk-pvp` row's focus on the helicopter build (Driven Thunder essence = gear-assembled essence variant) obscures that the base pull exists without any gear
- Essence variants: Storm Spirit (removes pull → DPS-only, gear-assembled); Driven Thunder (converts to forward-channeled spin, gear-assembled); Tempest's Heart (pull + detonate, gear-assembled via chest armor); Frigid Cyclone (pull + freeze + no-charge, gear-assembled) — all EXCLUSIONS per evidence bar
- Treatment at base level: **hybrid** (pull and damage co-intrinsic to base skill; neither configurable-out without gear modification); at kit level the hybrid is configurable-out (Storm Spirit removes pull) — taxonomy note from defended-zero doc still holds at KIT level

### `d3-zbarb` (D3 Support Barbarian)

**What the existing row likely captures:** Ground Stomp Wrenching Smash + Ancient Spear Rage Flip as group-support GR meta tools; pixelpull density mechanic.

**Missing probe facts (enrichment):**
- Ground Stomp Wrenching Smash specific probe facts:
  - Pull radius: **24 yards** (confirmed from Maxroll zBarb guide)
  - Geometry: **radial-nova** from caster point (AoE pull-to-self)
  - Commit type: **instant** (30-frame base animation, not scaling with attack speed)
  - Movement verb: **rooted** during cast animation (30 fixed frames)
  - Containment: triggers **40% CC resistance on all targets pulled** (documented); immune classes: Juggernaut Rare Elites, Rift Guardians, large monsters; Waller affix blocks effect
  - Treatment: **control-primary, damage-suppressed** (zBarb deliberately gears to minimize own damage — this is the opposite of pull-intrinsic damage-primary)
- Ancient Spear Rage Flip probe facts:
  - Range: **60 yards** (off-screen range)
  - Geometry: **linear projectile** (throw spear → targets thrown BEHIND the Barbarian at ~same range)
  - Resource cost: **25 Fury** (base), no cooldown listed (Fury-gated not CD-gated)
  - Movement verb: **rooted** during throw animation (attack-speed-scaling animation with 1.2× innate multiplier)
  - Containment: Juggernaut and Rift Guardian immune; obstacle blocking applies
  - Note: Rage Flip throws AWAY, not pulls toward — it's a displacement mechanic creating pixelpull geometry by throwing targets behind the Barbarian to cluster at a new point, not literal inward pull to caster. The "pull" function is achieved by repositioning to a new density point. This is a corner case in the pull taxonomy — outward throw that achieves density equivalent to pull-to-self.

---

## Exclusions Section — Gear-Assembled Pull Cases

These cases confirm the mechanic's genre reality but are NOT kit rows per the evidence bar (intrinsic skill/rune/talent level only). Documented here for completeness.

| Case | Game | Source | Why excluded |
|---|---|---|---|
| Ranslor's Folly vacuum (DMO Energy Twister Wizard, D3) | D3 | Item: Ranslor's Folly unique bracers | Gear-assembled: bracers auto-pull enemies to active Energy Twisters twice per second. Pull is rider on an item proc, not a class skill. Elite-immune. 5s per-enemy immunity. |
| Empire's Grasp-class knockback reversals (PoE) | PoE 1 | Item: Empire's Grasp unique gloves | Gear-assembled: converts knockback into pull. The reversal is an item modifier, not an intrinsic class/skill mechanic. |
| D3 Raiment/In-geom teleport-pull set pieces (Monk) | D3 | Set: Raiment of a Thousand Storms + In-geom | Gear-assembled: set causes Dashing Strike to teleport enemies to the Monk's after-dash position. Pull is set-piece proc. |
| MCD Gravity enchant (Hammer of Gravity, Imploding Crossbow, Echo of the Valley, Voidcaller, Encrusted Anchor, Burst Gale Bow) | MCD | Weapon intrinsic + Gravity enchant economy | Documented in prior tranche (2026-07-15-mcd-mode-b-crawl-tranche1.md). MCD classless architecture = all pull is gear-assembled; no base class has intrinsic pull. Pull via weapon enchant = assembly/rider per taxonomy. |
| DI Cyclone Strike essence variants (Storm Spirit, Driven Thunder, Tempest's Heart, Frigid Cyclone, Mystic Winds, Sandstorm) | DI | Legendary chest armor equips | Gear-assembled: ALL DI essence variants require equipping a specific Legendary chest armor piece. The BASE skill has intrinsic pull (kit row `di-cyclone-strike-monk-base` above); the variants that modify pull behavior are gear-assembled overlays. |
| Hades 1: Poseidon "Rip Current" Aid augment | Hades 1 | Boon: Poseidon Aid augment | Boon-assembled: Poseidon boon applied to Aid activation. Boon-stack = assembly per established Hades-boon precedent. |
| D3 Ess of Johan pull (follower/player proc) | D3 | Amulet: The Ess of Johan | Gear-assembled: amulet triggers 60y pull on hit. Assembly item, not class skill. Counts as Knockback for Strongarm Bracers. |
| D3 Strongarm Bracers damage amplifier via pull | D3 | Item: Strongarm Bracers | Gear-assembled rider: bracers grant +20-30% damage buff for 6s when target is Knockback'd. Pull is a trigger for the damage buff, not the damage itself. |

---

## Per-Franchise Empty-Verdict Lines

Franchises with NO intrinsic pull class-kit found:

- **Diablo 2:** No intrinsic player-class pull skill. Sorceress has Static Field (damage) and Frozen Orb (projectile); Amazon has Valkryie/Valkyrie (summon); no vortex/gravity pull. EMPTY.
- **Path of Exile 1 / Path of Exile 2:** No intrinsic player-class pull skill. Void Sphere (PoE1) has corpse-vacuum on-death pull only — not live-enemy clustering, 10s cooldown, 1 charge. Whirlwind (PoE2) moves the PLAYER through enemies, not enemies to a point. GGG has actively avoided player-owned live-enemy pull by design. EMPTY (PoE1 Void Sphere documented as boundary case in prior probe — on-death only, not kit-grain intrinsic pull on living enemies).
- **Grim Dawn:** No intrinsic class skill with inward displacement pull on living enemies. Vortex of Souls is an item-granted proc (gear-assembled). Callidor's Tempest is an AoE damage skill with no pull mechanic. Monster-side pull exists but is not player kit. EMPTY.
- **Torchlight 1 / Torchlight 2:** No intrinsic class pull skill. Immolation Aura (Embermage) is stationary fire vortex; Prismatic Rift is a teleport-push (outward). No pull skill confirmed across character classes. EMPTY.
- **Torchlight Infinite:** Insufficient documented evidence of a class-intrinsic pull skill. No pull-primary skill found in available documentation. EMPTY (uncertain — limited coverage; flag for future crawl if corpus expands to TLI).
- **Titan Quest / Immortal Throne:** No intrinsic class pull skill found. Ternion Attack is a triple-staff-strike AoE with splash, not pull. No other pull-class mechanic documented. EMPTY.
- **Last Epoch:** Anomaly (Void Knight) — Time Bubble utility and time-related CC; no documented inward displacement pull mechanic. Warpath (Primalist/Paladin/etc.) is channeled spin that moves the PLAYER through enemies, not pull-to-point. Abyssal Echoes is a void AoE. No intrinsic pull found across Sentinel, Mage, Rogue, Acolyte, or Primalist mastery trees in documented sources. EMPTY (verify against full skill DB if corpus expands to LE).
- **Hades 1:** No intrinsic Zagreus/Melinoe pull mechanic. Poseidon boons are knockback (outward). "Rip Current" Aid augment is boon-assembled. No core weapon or dash mechanic has pull-to-self or pull-to-point as intrinsic output. EMPTY.
- **Hades 2:** Poseidon boons in H2 continue knockback (outward) identity. Demeter boons are Freeze and Gust effects. No inward pull boon documented in H2. EMPTY.
- **Vampire Survivors — Gorgeous Moon:** Vacuum phase ONLY pulls gems/pickups, not living enemies. The "pull" is a collectible magnet, not mob displacement force. Does NOT qualify as intrinsic mob-pull mechanic. EMPTY (non-qualifying).
- **Undecember:** Classless rune-based system; "Illusion Hook" pull skill confirmed in search results but Undecember is a classless game — pull is rune-assembled, not class-intrinsic. Evidence bar requires class-kit level. EXCLUDED per architecture (gear/rune-assembled in classless system). No kit-level intrinsic pull. EMPTY per bar.
- **Chronicon:** Four classes (Templar, Berserker, Warden, Mechanist, Warlock). No intrinsic pull skill found in documented class skill sets. Berserker Whirlwind is player-movement spin. No gravity/vortex/pull confirmed. EMPTY (limited coverage — smaller game; flag for future crawl if corpus expands to Chronicon).

---

## Source List

| Source | URL | Access date | Used for |
|---|---|---|---|
| Lost Ark Codex — Vortex Gravity | https://lostarkcodex.com/us/skill/18011/ | 2026-07-15 | la-destroyer-vortex-gravity |
| Lost Ark Fextralife — Gravity Impact | https://lostark.wiki.fextralife.com/Gravity+Impact | 2026-07-15 | la-destroyer-gravity-impact |
| Lost Ark Fextralife — Gravity Force | https://lostark.wiki.fextralife.com/Gravity+Force | 2026-07-15 | la-destroyer-gravity-force |
| Lost Ark Fextralife — Gravity Compression | https://lostark.wiki.fextralife.com/Gravity+Compression | 2026-07-15 | la-destroyer-gravity-compression |
| Lost Ark playlostark.com Academy — Destroyer | https://www.playlostark.com/en-us/news/articles/lost-ark-academy-destroyer-class | 2026-07-15 | All LA Destroyer rows (identity/Hypergravity/Gravity Core system) |
| Maxroll — Lost Ark Gravity Training Destroyer | https://maxroll.gg/lost-ark/build-guides/gravity-training-destroyer-raid-build-guide | 2026-07-15 | LA Destroyer build context |
| vulkk.com — Lost Ark Destroyer Beginners Guide | https://vulkk.com/2022/05/19/lost-ark-destroyer-class-guide-for-beginners/ | 2026-07-15 | Gravity Compression/Force/Impact cooldowns |
| Diablo 4 Fextralife — Vortex | https://diablo4.wiki.fextralife.com/Vortex | 2026-07-15 | d4-spiritborn-vortex |
| Wowhead — D4 Vortex skill | https://www.wowhead.com/diablo-4/skill/vortex-1489641 | 2026-07-15 | d4-spiritborn-vortex |
| Game8 — D4 Vortex | https://game8.co/games/Diablo-4/archives/477896 | 2026-07-15 | d4-spiritborn-vortex upgrade paths |
| Diablo 4 Fextralife — Spiritborn Skills | https://diablo4.wiki.fextralife.com/Spiritborn+Skills | 2026-07-15 | Confirming Vortex is intrinsic class tree |
| Diablo Fandom — Black Hole | https://diablo.fandom.com/wiki/Black_Hole | 2026-07-15 | d3-wizard-black-hole |
| Diablo Immortal Fextralife — Cyclone Strike | https://diabloimmortal.wiki.fextralife.com/Cyclone_Strike | 2026-07-15 | di-cyclone-strike-monk-base |
| Game8 — DI Cyclone Strike | https://game8.co/games/Diablo-Immortal/archives/377790 | 2026-07-15 | DI base skill mechanics |
| Maxroll — D3 zBarb S39 | https://maxroll.gg/d3/guides/support-zbarb-guide | 2026-07-15 | d3-zbarb enrichment (Ground Stomp 24y radius, CC-res) |
| DiabloFans — zMonk guide | https://www.diablofans.com/builds/98593-support-monk-an-in-depth-guide-to-zmonk | 2026-07-15 | D3 Cyclone Strike probe facts |
| Diablo Fandom — DI Cyclone Strike | https://diablo.fandom.com/wiki/Cyclone_Strike_(Diablo_Immortal) | 2026-07-15 | DI essence variants documentation (for Exclusions) |
| Hades Wiki Fandom — Boons H2 | https://hades.fandom.com/wiki/Boons/Hades_II | 2026-07-15 | Hades 2 empty verdict |
| Vampire Survivors Wiki — Gorgeous Moon | https://vampire.survivors.wiki/w/Gorgeous_Moon | 2026-07-15 | VS Gorgeous Moon empty verdict |
| Lost Epoch Tools — Anomaly nodes | https://www.lastepochtools.com/skills/anomaly/nodes | 2026-07-15 | Last Epoch empty verdict |
| GrimTools — Vortex of Souls | https://www.grimtools.com/db/items/2506 | 2026-07-15 | Grim Dawn empty verdict |
