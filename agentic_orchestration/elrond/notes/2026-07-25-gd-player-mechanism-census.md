# GD player-side mechanism census — the kit-count column for G-5 triage

**Agent:** elrond (data steward)
**Commissioned by:** gandalf, 2026-07-25 (GD three-goal program; G-5 ruling — a GD character
**re-instantiates** into engine-native mechanic surfaces, and where no surface exists the gap becomes
a mechanic-surface BUILD ITEM. Triage rule: "only impacts one build" → re-entry tag; "a handful of
builds" → build as we go.)
**Type:** ANALYSIS / DATA CENSUS — read-only over `corpus.db`. No schema changes, no writes, no
production code.
**Date:** 2026-07-25
**Reproducibility script:** `agentic_orchestration/research/scripts/gd_player_mechanism_census_2026_07_25.py`
(run bare for the census + zero-probes + rejection ledger; run `--evidence` for the per-kit evidence
snippet behind every single count in this document)

**Read-only attestation:** `corpus.db` mtime unchanged at `2026-07-24 21:29:04` after this run; the
script opens it `file:...?mode=ro`.

**Scope boundary honoured:** this document does NOT rule fit-vs-gap against our engine's surfaces.
That mapping pass is gandalf's, downstream. Where the corpus's own `t4_doors` / `kit_deviation` rows
already carry engine-side coordinates, they are reported in §7 as *appendix*, explicitly flagged as
engine-side annotations rather than GD-native mechanisms.

---

## SUMMARY (≤14 lines)

```
41 GD-lane kits. 89 distinct player-side mechanisms enumerated.
    STRUCTURED (typed column / typed JSON field)   58
    PROSE      (regex + hand-adjudicated)          29
    PROSE-ZEROED (every hit rejected in context)    2   (P-STUN, P-FREEZE)

TOP-5 BY KIT-COUNT
    19 / 46%   Ground-placed persistent zone / ground effect      STRUCTURED
    18 / 44%   Devotion (constellation) proc binding              PROSE
    17 / 41%   Cooldown-gated cadence                             STRUCTURED
    17 / 41%   Damage-type conversion (item/set/skill-mod)        PROSE
    16 / 39%   Resistance reduction (RR / shred)                  PROSE

BIGGEST HONEST-UNKNOWN: devotion PROC PAYLOADS. 18 of 41 kits (44%) name devotions —
the second-densest mechanism in the census — and the corpus holds ZERO behavioural
payload for any of them. Names fetched; behaviours not. See §5.1.
```

---

## 1. Substrate actually read — row counts, so the work is reproducible

All rows scoped `kit_id LIKE 'gd-%'` (equivalently `game='gd'`; the two agree — the GD lane is
exactly 41 kits, no `gdx3` rows, confirmed in my 2026-07-25 attestation-scope census §1).

| Table | rows (GD) | distinct kits | What it contributes to this census |
|---|---:|---:|---|
| `canon_corpus` | 41 | 41 | roster, lattice prefix coords, `core_skills` |
| `kit_master` (view) | 41 | 41 | grade / terminal_state / attested element+ailment rollups |
| `kit_mapping` | 41 | 41 | **primary structured source** — `mapping_json` carries `skills[]` (geometry_value, elements, ailments, delivery_notes), `trigger_grammar`, `t4_doors`, `scaffold`, `fidelity_notes` |
| `skill_geometry_band` | 73 | 40 | **primary structured source** — typed `delivery_class`, `cadence_class`, `pierce`, `chain`, `motion_signature`, range/width/speed bands |
| `kit_dossier` | 246 | 41 | 6 families × 41; 40 rows abstained. **primary prose source** |
| `verify_ledger` | 210 | 41 | 164 CONFIRMED / 13 CONTRADICTED / 33 UNSUPPORTED; claim_text + anchor_quote |
| `kit_deviation` | 34 | 32 | 6 `engine_inexpressible`, 28 `accepted_downgrade` |
| `kit_delta_t4` | 41 | 41 | 26 `step` / 15 `ramp` — shape only, no mechanism content |
| `recognition_hook` | 70 | 40 | 40 geometry hooks + 30 register hooks, all `expressed` |
| `kit_acceptance_assert` | 54 | 41 | `primary_delivery_class == X` asserts, 6 red (routed to dockets) |
| `kit_citations` | 86 | 41 | provenance only |
| **`kit_composition`** | **11** | **1** | damage-composition factors — `gd-flames-of-ignaffar-purifier` ONLY |
| **`kit_numeric`** | **26** | **1** | numeric anchors — `gd-flames-of-ignaffar-purifier` ONLY |
| **`exact_skill` / `exact_skill_field`** | **1 / 136** | **1** | `.arz` datamine — `gd-flames-of-ignaffar-purifier` ONLY (the GD-SLICE width-one proof) |
| **`kit_door_arg`** | **0** | **0** | no door-arg bindings exist for any GD kit |

Grade distribution: EXACT 9 · CLOSE 23 · APPROX 3 · GAPPED 6.

**The single most consequential row-count on this page:** `kit_composition`, `kit_numeric`, and
`exact_skill*` each cover **1 of 41 kits**. Every mechanism below is attested as *present*; almost
none is attested with a *magnitude*. See §5.6.

---

## 2. Method — two grades, never blurred

**STRUCTURED.** Read from a typed column or a typed JSON field. `delivery_class='zone'` is a value in
a `CHECK`-constrained column; `ailments:["burn"]` is a typed array element. No interpretation between
the row and the count. These are measurements.

**PROSE.** Regex over the curated prose corpus — `kit_dossier.payload_json` (non-abstained),
`kit_mapping$.skills[].delivery_notes`, `$.fidelity_notes`, `$.motion_frame`, `$.resource_economy`,
`$.scaffold`, `verify_ledger.claim_text`/`anchor_quote` (CONFIRMED only), and
`kit_deviation.missing_expression`/`source_anchor`. Every regex is in the script. **Every hit was
read in context.** 14 hits were rejected; the rejection ledger is §3 and is reproduced by the script.

**PROSE-ZEROED.** A mechanism family where every candidate hit was rejected. Reported as a zero row
rather than deleted, because the zero is the finding.

**Why the adjudication matters and is not optional:** this corpus records NEGATIVE tokens in the same
prose fields it records positive ones — e.g. `gd-forcewave-warlord.fidelity_notes` literally says
`"NO conversion attested"`. A naive scan reads that as a conversion kit. Fidelity-grade discipline
(era-substrate doc §4) makes the negation-aware pass mandatory, not a nicety.

---

## 3. Rejection ledger — 14 hits read in context and thrown out

| Mechanism | Kit | Reason |
|---|---|---|
| P-CONVERT | `gd-aar-spellbinder` | NEGATION — `fidelity_notes`: "no conversion/propagation capstone attested" |
| P-CONVERT | `gd-forcewave-warlord` | NEGATION — "NO conversion attested → no ELEMENT_CONVERSION_PHYSICAL door" |
| P-CONVERT | `gd-callidors-tempest-templar` | WINDOW ARTIFACT — matched "compressed **to fire**-primary" |
| P-DEVOTION | `gd-belgothian-blademaster` | CROSS-REFERENCE — "sibling of devotion-proc row" names an *engine mapping row*, not a devotion this kit takes. The kit's own `capstone_alterations` **ABSTAINED** |
| P-RR | `gd-pet-conjurer` | NEGATION + CROSS-KIT — "not attestable HERE — contrast `gd-doom-bolt-sentinel` where CoF's resistance reduction WAS fetched" |
| P-TRANSMUTE | `gd-bwc-demolitionist` | STRUCK ANCHOR — the "fumble transmuters" line is recorded INADMISSIBLE per the corpus's own §0.2 |
| P-TRANSMUTE | `gd-drain-essence-spellbinder` | RECLASSIFIED — "+2 extra targets via item modifier" is a gear affix; counted at P-PLUSTARGET |
| P-ITEMPROC | `gd-belgothian-blademaster` | RECLASSIFIED — "weapon procs firing every swing" is the WPS pool; counted at P-WPS |
| P-RETAL | `gd-aegis-paladin` | VARIANT-LANE — "Retaliation Warlord Aegis" is a *sibling kit* in `known_variants` |
| P-RETAL | `gd-flames-of-ignaffar-purifier` | VARIANT-LANE — "FoI retaliation Purifier (Hybris set)" is a listed variant, not the mapped form |
| P-STUN | `gd-canister-saboteur` | **STRUCK BY THE CORPUS ITSELF** — `kit_deviation`: "the engine emits NO CC token for it because the fetched anchor names only 'debuff'; stun/blind live in probe/claim-paraphrase, both inadmissible" |
| P-FREEZE | `gd-roh-infiltrator` | NEGATION — "NO freeze/chill token — 'cold shards' is element flavor only" |
| P-FREEZE | `gd-shadow-strike-infiltrator` | NEGATION — "NO chill/freeze token — cold is element flavor only" |
| P-FREEZE | `gd-trozan-druid` | NEGATION — "NO chill/freeze token: cold is element-flavor only" |

---

## 4. THE CENSUS — 89 mechanisms, sorted by kit-count descending

N = 41. `%` is of 41. Exemplars are folk names; the full kit list per mechanism is in the script's
`--evidence` output.

| # | id | mechanism | family | kits | % | grade | provenance | exemplars |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | D-ZONE | Ground-placed zone / persistent ground effect | delivery | 19 | 46% | STRUCTURED | `skill_geometry_band.delivery_class` | Blight Fiend Ritualist; BWC Demolitionist; Callidor's Tempest Templar |
| 2 | P-DEVOTION | Devotion / constellation proc binding | trigger | 18 | 44% | PROSE | `kit_dossier[capstone_alterations]` | Devastation Sorcerer; Doom Bolt Sentinel; EoR Warlord |
| 3 | C-COOLDOWN | Cooldown-gated cadence | cadence | 17 | 41% | STRUCTURED | `skill_geometry_band.cadence_class` | AAR Spellbinder; Blade Trap; Bloody Pox Conjurer |
| 4 | P-CONVERT | Damage-type conversion (item/set/skill-mod granted) | gear-borne | 17 | 41% | PROSE | `kit_dossier[item_alterations]`, `kit_mapping$.fidelity_notes` | Fire Strike Purifier; Shadow Strike Infiltrator; Righteous Fervor Dervish |
| 5 | P-RR | Resistance reduction (RR / shred) | buff-debuff | 16 | 39% | PROSE | `kit_dossier[skill_loop]` | Blade Arc Warder; BWC Demolitionist; Vitality Conjurer |
| 6 | G-GROUND | Ground-targeted circle placement | delivery | 16 | 39% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | BWC Demolitionist; Canister Saboteur; DEE Witch Hunter |
| 7 | M-GROUND_PLACE | Motion signature: ground-place | motion sig | 16 | 39% | STRUCTURED | `skill_geometry_band.motion_signature` | BWC Demolitionist; Canister Saboteur; DEE Witch Hunter |
| 8 | P-SET | Item-set threshold bonus as build enabler | gear-borne | 14 | 34% | PROSE | `kit_dossier[item_alterations]` | Belgothian Blademaster; Krieg Death Knight; Trozan Druid |
| 9 | D-PROJ | Projectile delivery | delivery | 11 | 27% | STRUCTURED | `skill_geometry_band.delivery_class` | Aegis Paladin; Canister Saboteur; Fire Strike Purifier |
| 10 | M-STRAIGHT_LINE | Motion signature: straight-line | motion sig | 10 | 24% | STRUCTURED | `skill_geometry_band.motion_signature` | AAR Spellbinder; Forcewave Warlord; Doom Bolt Sentinel |
| 11 | P-AURA-EX | Persistent support field (seal / aura / toggle) | passive/tree | 9 | 22% | PROSE | `kit_dossier[skill_loop]`, `[capstone_alterations]` | Aegis Paladin; Fire Strike Purifier; Word of Pain Tactician |
| 12 | D-DELEG | Delegated actor delivery (pet / totem / turret) | delivery | 8 | 20% | STRUCTURED | `skill_geometry_band.delivery_class` | Mortar Purifier; Primal Strike Vindicator; Wendigo Totem Ritualist |
| 13 | D-MELEE | Melee arc / sweep | delivery | 8 | 20% | STRUCTURED | `skill_geometry_band.delivery_class` | Belgothian Blademaster; Blade Arc Warder; Cadence Witchblade |
| 14 | G-TOTEM | Placed autonomous emitter (totem / trap / turret) | delivery | 8 | 20% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Bloody Pox Conjurer; Mortar Purifier; Skeleton Ritualist |
| 15 | P-ENERGY | Energy / mana economy pressure as build constraint | resource | 8 | 20% | PROSE | `kit_dossier[skill_loop]`, `kit_mapping$.resource_economy` | FoI Purifier; Stun Jacks; Skeleton Ritualist |
| 16 | P-LEECH | Life leech / ADCtH | buff-debuff | 7 | 17% | PROSE | `kit_dossier[skill_loop]`, `[capstone_alterations]` | Drain Essence Spellbinder; Krieg Death Knight; Wendigo Totem Ritualist |
| 17 | D-AURA | Aura / persistent self-field | delivery | 7 | 17% | STRUCTURED | `skill_geometry_band.delivery_class` | AAR Spellbinder; Pet Conjurer; RoH Infiltrator |
| 18 | G-MSTRIKE | Melee point strike | delivery | 7 | 17% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Cadence Witchblade; Savagery Warder; Righteous Fervor Dervish |
| 19 | M-POINT_STRIKE | Motion signature: point-strike | motion sig | 7 | 17% | STRUCTURED | `skill_geometry_band.motion_signature` | Cadence Witchblade; Savagery Warder; Primal Strike Vindicator |
| 20 | P-TRANSMUTE | Transmuter / skill modifier that changes behaviour | passive/tree | 7 | 17% | PROSE | `kit_dossier[skill_loop]`, `[capstone_alterations]` | Forcewave Warlord (Tremor); Stun Jacks (Quick Jack); Vire's Might Shieldbreaker (Volcanic Stride) |
| 21 | P-HEALZONE | Healing / sustain zone or totem | buff-debuff | 6 | 15% | PROSE | `kit_dossier[skill_loop]` | Savagery Warder; Skeleton Ritualist; Wendigo Totem Ritualist |
| 22 | C-SPAM | Spam cadence | cadence | 6 | 15% | STRUCTURED | `skill_geometry_band.cadence_class` | DEE Witch Hunter; Panetti's Mage Hunter; Stun Jacks |
| 23 | D-MOTION | Motion-fused attack (dash / spin / charge) | delivery | 6 | 15% | STRUCTURED | `skill_geometry_band.delivery_class` | EoR Warlord; Shadow Strike Infiltrator; Vire's Might Shieldbreaker |
| 24 | G-PIERCE | Pierce-all projectile | delivery | 6 | 15% | STRUCTURED | `skill_geometry_band.pierce='all'` | AAR Spellbinder; Phantasmal Blades Witch Hunter; Word of Pain Tactician |
| 25 | P-REPLACER | Default-attack replacer | delivery | 6 | 15% | PROSE | `kit_mapping$.skills[].delivery_notes` | Fire Strike Purifier; Savagery Warder; Righteous Fervor Dervish |
| 26 | P-CDR | Cooldown reduction as a scaling lever | gear-borne | 6 | 15% | PROSE | `kit_dossier[item_alterations]` | Doom Bolt Sentinel; Storm Box Elementalist; Vire's Might Shieldbreaker |
| 27 | T-CONS-BURST-DAMAGE | Proc consequence: burst-damage | trigger | 6 | 15% | STRUCTURED | `kit_mapping$.trigger_grammar.consequence_type` | Cadence Witchblade; Krieg Death Knight; Righteous Fervor Dervish |
| 28 | A-CURSE_SAP | Sap / weaken curse (debuff ailment) | ailment | 5 | 12% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | Doom Bolt Sentinel; Primal Strike Vindicator; Righteous Fervor Dervish |
| 29 | P-IMMUNE | Timed defensive cooldown / immunity window | buff-debuff | 5 | 12% | PROSE | `kit_dossier[skill_loop]` | AAR Spellbinder (Mirror); Drain Essence Spellbinder (Mark of Torment); Krieg Death Knight |
| 30 | C-CHANNEL | Channel cadence | cadence | 5 | 12% | STRUCTURED | `skill_geometry_band.cadence_class` | AAR Spellbinder; FoI Purifier; EoR Warlord |
| 31 | G-NOVA | Self-centred circle / nova | delivery | 5 | 12% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Callidor's Tempest Templar; EoR Warlord (Judgment); Wendigo Totem Ritualist |
| 32 | G-SELFBUF | Self-buff (non-aura) | delivery | 5 | 12% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | AAR Spellbinder; Pet Conjurer; RoH Infiltrator |
| 33 | P-ROOTCHAN | Movement lock while casting / channelling | delivery | 5 | 12% | PROSE | `kit_dossier[skill_geometry]`, `kit_mapping$.delivery_notes` | AAR Spellbinder; FoI Purifier; Forcewave Warlord |
| 34 | M-BURST_AROUND_SELF | Motion signature: burst-around-self | motion sig | 5 | 12% | STRUCTURED | `skill_geometry_band.motion_signature` | Callidor's Tempest Templar; EoR Warlord; Vitality Conjurer |
| 35 | P-ASPEED | Attack-speed / cast-speed as the scaling lever | resource | 5 | 12% | PROSE | `kit_mapping$.resource_economy`, `kit_dossier` | Belgothian Blademaster; Fire Strike Purifier; Forcewave Warlord |
| 36 | A-BLEED | Bleed DoT | ailment | 4 | 10% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | Blade Arc Warder; Forcewave Warlord; Skeleton Ritualist |
| 37 | A-BURN | Burn DoT | ailment | 4 | 10% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | BWC Demolitionist; FoI Purifier; Vire's Might Shieldbreaker |
| 38 | G-SINGLE | Single-target payload | delivery | 4 | 10% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Blade Trap; Doom Bolt Sentinel; Bloody Pox Conjurer |
| 39 | P-MOVEATK | Movement skill fused with attack / gap-close | delivery | 4 | 10% | PROSE | `kit_dossier[skill_geometry]` | Shadow Strike Infiltrator; Vire's Might Shieldbreaker; Cadence Witchblade (Blitz) |
| 40 | M-FAN_SPREAD | Motion signature: fan-spread | motion sig | 4 | 10% | STRUCTURED | `skill_geometry_band.motion_signature` | Canister Saboteur; Phantasmal Blades Witch Hunter; Stun Jacks |
| 41 | T-ON-CAST-LINKED | Proc trigger: on-cast-linked | trigger | 4 | 10% | STRUCTURED | `kit_mapping$.trigger_grammar.proc_trigger_condition` | EoR Warlord; Fire Strike Purifier; Trozan Druid |
| 42 | T-ON-HIT-THRESHOLD | Proc trigger: on-hit-threshold | trigger | 4 | 10% | STRUCTURED | `kit_mapping$.trigger_grammar.proc_trigger_condition` | Belgothian Blademaster; Cadence Witchblade; Krieg Death Knight |
| 43 | D-BEAM | Channelled beam | delivery | 3 | 7% | STRUCTURED | `skill_geometry_band.delivery_class` | AAR Spellbinder; Drain Essence Spellbinder; Storm Box Elementalist |
| 44 | G-CHAIN | Chain / hop to additional targets | delivery | 3 | 7% | STRUCTURED | `skill_geometry_band.chain` | Drain Essence Spellbinder; Storm Box Elementalist; Retaliation Warlord |
| 45 | G-MULTIP | Multi-projectile / fan spread | delivery | 3 | 7% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Canister Saboteur; Phantasmal Blades Witch Hunter; Stun Jacks |
| 46 | P-PLUSTARGET | Affix that adds targets / projectiles to a skill | gear-borne | 3 | 7% | PROSE | `kit_dossier[skill_geometry]`, `[item_alterations]` | Drain Essence Spellbinder (+2 targets); Stun Jacks (+1 projectile); Primal Strike Vindicator (100% pass-through) |
| 47 | M-ORBIT_FIXED | Motion signature: orbit-fixed | motion sig | 3 | 7% | STRUCTURED | `skill_geometry_band.motion_signature` | Belgothian Blademaster (Blade Spirit); EoR Warlord; Retaliation Warlord |
| 48 | P-PET-PERM | Persistent pet / summoned combatant | pets | 3 | 7% | PROSE | `kit_dossier[skill_loop]` | Pet Conjurer; Skeleton Ritualist; Blight Fiend Ritualist |
| 49 | P-PET-TEMP | Temporary / duration-limited summon | pets | 3 | 7% | PROSE | `kit_dossier[skill_loop]` | Reap Spirit (10s); Skeleton Ritualist (Primal Spirit); Pet Conjurer |
| 50 | P-WPS | Weapon-pool proc suite (on-attack proc pool) | trigger | 3 | 7% | PROSE | `kit_dossier[skill_loop]` | Belgothian Blademaster; Fire Strike Purifier; Righteous Fervor Dervish |
| 51 | T-CONS-LINKED-CAST | Proc consequence: linked-cast | trigger | 3 | 7% | STRUCTURED | `kit_mapping$.trigger_grammar.consequence_type` | Fire Strike Purifier; Trozan Druid; Word of Pain Tactician |
| 52 | A-DRAIN | Drain (life / resource siphon) | ailment | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | Drain Essence Spellbinder; Ravenous Earth Oppressor |
| 53 | P-ABSORB | Damage absorption / shield layer | buff-debuff | 2 | 5% | PROSE | `kit_dossier[skill_loop]`, `[item_alterations]` | Devastation Sorcerer; Mortar Purifier (Blast Shield) |
| 54 | G-AURA | Aura (geometry token) | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Ravenous Earth Oppressor; Righteous Fervor Dervish |
| 55 | G-BEAM | Channelled beam (geometry token) | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | AAR Spellbinder; Drain Essence Spellbinder |
| 56 | G-DASH | Dash / charge attack | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Cadence Witchblade (Blitz); Vire's Might Shieldbreaker |
| 57 | G-LINE | Line / lane payload | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Fire Strike Purifier; Forcewave Warlord |
| 58 | G-MARC | Melee arc sweep | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Blade Arc Warder; Krieg Death Knight (Bone Harvest) |
| 59 | G-SPIN | Sustained spin / whirlwind | delivery | 2 | 5% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | EoR Warlord; Retaliation Warlord |
| 60 | P-CONTAGION | Contagion / proximity spread between enemies | delivery | 2 | 5% | PROSE | `kit_dossier[skill_loop]`, `kit_mapping$.delivery_notes` | Bloody Pox Conjurer; DEE Witch Hunter |
| 61 | P-ITEMPROC | Skill-granting item proc | gear-borne | 2 | 5% | PROSE | `kit_dossier[item_alterations]` | DEE Witch Hunter (Dreeg's Infinite Gaze → Tainted Eruption); EoR Warlord (Beronath conversion aura) |
| 62 | M-ARC_SWEEP | Motion signature: arc-sweep | motion sig | 2 | 5% | STRUCTURED | `skill_geometry_band.motion_signature` | Blade Arc Warder; Krieg Death Knight |
| 63 | P-STACKMETER | Charge / stack accumulator meter | passive/tree | 2 | 5% | PROSE | `kit_dossier[skill_loop]` | Savagery Warder (charges per swing); Righteous Fervor Dervish (fervor meter) |
| 64 | P-PET-SCALE | Pet-scaling stat lane (pet% dmg, pet OA/DA) | pets | 2 | 5% | PROSE | `kit_dossier[item_alterations]`, `kit_mapping$.scaffold` | Pet Conjurer; Reap Spirit |
| 65 | A-BLIND | Blind / fumble (soft CC) | ailment | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | BWC Demolitionist |
| 66 | A-POISON | Poison / acid DoT | ailment | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | DEE Witch Hunter |
| 67 | A-ROOT | Root / immobilize (hard CC) | ailment | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].ailments[]` | Blade Trap |
| 68 | P-RETAL | Retaliation / damage-return (thorns) | buff-debuff | 1 | 2% | PROSE | `kit_dossier[skill_loop]` | Retaliation Warlord |
| 69 | G-BLINK | Teleport / blink strike | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Shadow Strike Infiltrator |
| 70 | G-CHAINH | Chain-hop between targets (geometry token) | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Storm Box Elementalist |
| 71 | G-CONE | Cone | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | FoI Purifier |
| 72 | G-FORK | Fork / split projectile | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Panetti's Mage Hunter |
| 73 | G-ORBIT | Orbiting proxy | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Belgothian Blademaster (Blade Spirit) |
| 74 | G-RICO | Ricochet / bounce | delivery | 1 | 2% | STRUCTURED | `kit_mapping$.skills[].geometry_value` | Aegis Paladin |
| 75 | P-TETHER | Enemy-attached tether / beacon | delivery | 1 | 2% | PROSE | `kit_dossier[skill_loop]` | Storm Box Elementalist |
| 76 | M-BLINK_TRANSLATE | Motion signature: blink-translate | motion sig | 1 | 2% | STRUCTURED | `skill_geometry_band.motion_signature` | Shadow Strike Infiltrator |
| 77 | M-CHAIN_HOP | Motion signature: chain-hop | motion sig | 1 | 2% | STRUCTURED | `skill_geometry_band.motion_signature` | Storm Box Elementalist |
| 78 | M-FORK_SPLIT | Motion signature: fork-split | motion sig | 1 | 2% | STRUCTURED | `skill_geometry_band.motion_signature` | Panetti's Mage Hunter |
| 79 | M-RICOCHET_RETURN | Motion signature: ricochet-return | motion sig | 1 | 2% | STRUCTURED | `skill_geometry_band.motion_signature` | Aegis Paladin |
| 80 | P-AUTOTURRET | Autonomous placed turret with own targeting | pets | 1 | 2% | PROSE | `kit_dossier[skill_loop]` | Mortar Purifier |
| 81 | P-DEATHNOVA | Explosion-on-death (proxy / corpse) | pets | 1 | 2% | PROSE | `kit_dossier[skill_loop]` | Blight Fiend Ritualist |
| 82 | P-TRAPTRIG | Contact-triggered placed trap (arms on enemy contact) | trigger | 1 | 2% | PROSE | `kit_dossier[skill_loop]` | RoH Infiltrator |
| 83 | T-ACCUM | Swing-count accumulator (every-Nth-swing) | trigger | 1 | 2% | STRUCTURED | `kit_mapping$.trigger_grammar.mark_identity` | Cadence Witchblade |
| 84 | T-APPLYCONSUME | Apply-then-consume pair (detonator) | trigger | 1 | 2% | STRUCTURED | `kit_mapping$.trigger_grammar.trigger_chain_shape` | Cadence Witchblade |
| 85 | T-CONS-RESOURCE-FILL | Proc consequence: resource-fill | trigger | 1 | 2% | STRUCTURED | `kit_mapping$.trigger_grammar.consequence_type` | Doom Bolt Sentinel |
| 86 | T-ON-DAMAGE-TAKEN | Proc trigger: on-damage-taken | trigger | 1 | 2% | STRUCTURED | `kit_mapping$.trigger_grammar.proc_trigger_condition` | Retaliation Warlord |
| 87 | T-ON-DEFENDER-DEATH | Proc trigger: on-defender-death | trigger | 1 | 2% | STRUCTURED | `kit_mapping$.trigger_grammar.proc_trigger_condition` | Blight Fiend Ritualist |
| 88 | **P-STUN** | **Hard CC — stun / daze** | ailment | **0** | **0%** | **PROSE-ZEROED** | all hits rejected — §3 | — |
| 89 | **P-FREEZE** | **Hard CC — freeze / petrify** | ailment | **0** | **0%** | **PROSE-ZEROED** | all hits rejected — §3 | — |

### 4.1 Three delivery lenses over the same skills — a redundancy that inflates the row count

`skill_geometry_band.delivery_class` (7-value CHECK enum), `mapping_json$.skills[].geometry_value`
(21 free-text values), and `skill_geometry_band.motion_signature` (11 values) are **three co-existing
typed vocabularies describing the same 73 skill rows**. Rows 1/6/7 above are the same mechanism seen
three ways, not three findings. So is 12/14, 13/18/58/62, 23/56/59/69.

Consolidated to one canonical set, the delivery layer is:

| Consolidated delivery mechanism | kits | % | union of |
|---|---:|---:|---|
| Ground-placed persistent zone / ground effect | 19 | 46% | D-ZONE ∪ G-GROUND ∪ M-GROUND_PLACE |
| Projectile (incl. multi / fan / fork / ricochet) | 16 | 39% | D-PROJ ∪ G-MULTIP ∪ G-FORK ∪ G-RICO ∪ M-STRAIGHT_LINE ∪ M-FAN_SPREAD ∪ M-FORK_SPLIT ∪ M-RICOCHET_RETURN |
| Aura / persistent self-field | 13 | 32% | D-AURA ∪ G-AURA ∪ P-AURA-EX |
| Placed autonomous proxy (totem / trap / turret) | 9 | 22% | D-DELEG ∪ G-TOTEM ∪ P-AUTOTURRET ∪ P-TRAPTRIG |
| Melee strike / arc sweep | 8 | 20% | D-MELEE ∪ G-MSTRIKE ∪ G-MARC ∪ M-POINT_STRIKE ∪ M-ARC_SWEEP |
| Motion-fused attack (dash / spin / blink / orbit) | 6 | 15% | D-MOTION ∪ G-DASH ∪ G-SPIN ∪ G-BLINK ∪ G-ORBIT ∪ M-BLINK_TRANSLATE ∪ M-ORBIT_FIXED ∪ P-MOVEATK |
| Self-centred nova / burst | 5 | 12% | G-NOVA ∪ M-BURST_AROUND_SELF |
| Chain / hop / spread to extra targets | 5 | 12% | G-CHAIN ∪ G-CHAINH ∪ M-CHAIN_HOP ∪ P-CONTAGION ∪ P-TETHER |
| Pets & summons (any) | 4 | 10% | P-PET-PERM ∪ P-PET-TEMP ∪ P-PET-SCALE ∪ P-DEATHNOVA |
| Channelled beam | 3 | 7% | D-BEAM ∪ G-BEAM |

**Steward note (schema, my domain, offered not ruled):** three vocabularies for one property is a
real schema defect in my layer, not merely a reporting artifact. `geometry_value` is free text with
21 values; `delivery_class` is a 7-value CHECK; `motion_signature` is an open registry. They
disagree in places (`Mortar Trap` is `totem` in one and `summon_delegate` in the other, and
`verify_ledger` flags the latter UNSUPPORTED). I am not proposing a migration inside a census — but
it belongs on my `MIGRATION.md` docket, and any downstream consumer that counts delivery shapes must
be told which lens it is reading.

---

## 5. HONEST UNKNOWNS — first-class

Each item states what is missing, why it is not inferable from held data, and **what would attest
it**. None of these is "probably fine."

### 5.1 Devotion proc PAYLOADS — the biggest hole, and it sits under the #2 mechanism

18 of 41 kits (44%) name devotions. **Not one devotion's behaviour is held anywhere in the corpus.**
The rows carry constellation *names* — "Meteor Shower", "Eldritch Fire", "Targo's Hammer",
"Bonds of Bysmiel" — and nothing about what any of them does, what triggers it, what it costs, or
what its internal cooldown is. The corpus says so itself, in two places, verbatim:

- `gd-eor-warlord.kit_deviation`: *"every devotion-proc payload (Maul and the whole bound-devotion
  damage layer that Judgment exists to fire) is EMPTY under 0.3: names fetched, payloads not."*
- `gd-ravenous-earth-oppressor.fidelity_notes`: *"Twin Fangs devotion proc named ('wonderful combo')
  but payload behavior unfetched."*

**CANNOT ATTEST from held data:** what a devotion proc does; devotion binding rules (which skill a
proc attaches to); devotion point-cost / affinity gating; the proc's trigger condition or ICD.
**What would attest it:** the `.arz` devotion records (`records/ui/skills/devotion/`) via the GD
adapter already productionized for `gd-flames-of-ignaffar-purifier`, or a targeted legolas Mode-B
crawl of a devotion reference. This is a **one-source-away** unknown, not a hard one.

**Why it is the biggest:** a mechanism at 44% kit-count clears any reasonable "handful of builds"
triage threshold on the G-5 rule — but the triage cannot be *run* on it, because we do not know what
we would be building. The kit-count says "build it"; the payload void says "you cannot yet specify
what."

### 5.2 Hard CC on the player side — attested at ZERO, and that is a finding, not a gap in my scan

`kit_mapping$.skills[].ailments[]` across all 41 kits yields exactly seven ailment tokens:
`curse:sap` (5) · `burn` (4) · `bleed` (4) · `drain` (2) · `root` (1) · `poison` (1) · `blind` (1).

**Stun: 0. Freeze: 0. Petrify: 0. Knockdown: 0. Slow/chill applied to enemies: 0.** These are not
scan misses — the corpus *actively struck* every candidate (§3) on the ground that fetched anchors
named element flavour or a paraphrase, never a status behaviour.

This is a **provenance-policy artifact, not a claim about Grim Dawn.** GD unquestionably has stun,
freeze, petrify and chill on player skills; my monster-side census found `offensiveStun*` on 19
player-class `.arz` skill records and `offensiveFreeze` on 7. The player-side corpus simply admitted
none of them, because guide prose says "cold shards" and not "applies Freeze."

**CANNOT ATTEST from held data:** whether any GD-lane kit applies hard CC.
**What would attest it:** the kit→`.arz`-skill-record join (my J3 from the attestation-scope census).
Once the GD adapter runs at width 41 instead of width 1, `offensiveStun*` / `offensiveFreeze` /
`offensiveSlowRunSpeed` become a SQL query. **This is the single cheapest unknown to close**, and it
would close §5.2, §5.6, and half of §5.4 in one pass.

### 5.3 Mastery-bar / tree structure — no surface at all

Two kits mention skill-point investment in passing (`gd-blade-arc-warder`: "requires the Soldier
mastery bar at level 10"; `gd-blade-trap`: "24 skill points"). There is **no table in my layer that
models mastery bars, tree topology, node prerequisites, exclusivity, or point budgets.** No column
holds "which mastery", "how deep", or "which nodes".

**CANNOT ATTEST:** anything about GD's two-mastery investment structure, which is arguably the single
most identity-forming player-side mechanism in the game.
**What would attest it:** a new schema (mastery / node / prerequisite tables) fed by `.arz`
`playerclass*` skill trees. This is a **build item on my side**, and I flag it as such — it is the
one census row where the corpus is not thin but *absent*.

### 5.4 Gear affixes below the named-item level

`item_alterations` names key sets and key items and what they do at build level ("Ulzuin's Infernal
Avatar 5pc → 50% chaos-to-fire"). It holds **no affix-level rows**: no `+N to skill` (0 kits), no
flat/% damage affix rolls, no affix tiers, no roll ranges, no slot rules.

**CANNOT ATTEST:** the gear-affix surface as an itemization system. What IS attested is the
*build-enabling set threshold* (14 kits) and *conversion granted by gear* (17 kits) — those are real
and dense. **What would attest the rest:** GD item `.arz` records, or a grimtools item-database crawl.

### 5.5 Trigger machinery below the shape level

`trigger_grammar` is populated on 10 of 41 kits (31 have it null). Where present it carries a
*shape* (`on-hit-threshold` → `burst-damage`) and no parameters. **Internal cooldowns: 0 kits.
On-block procs: 0 kits. On-kill procs: 0 kits** (the 3 "corpse" hits are pet-death payloads, not
on-kill triggers). Proc chance is attested in prose for exactly one kit
(`gd-belgothian-blademaster`: "100%+ WPS chance"), and individual WPS payloads are explicitly
unfetched for all three WPS kits.

### 5.6 Numeric magnitudes — 1 of 41

`kit_composition` (11 rows) and `kit_numeric` (26 rows) cover **`gd-flames-of-ignaffar-purifier`
only**. For the other 40 kits the corpus attests *that* a mechanism is present and *nothing* about
its size: no base damage, no cooldown seconds, no radius, no duration, no proc chance, no
conversion percentage in a typed field. `kit_door_arg` is empty for the entire GD lane (0 rows), so
no door argument has ever been bound from a GD kit.

**Consequence for G-5:** kit-count triage can be run today. Magnitude-faithful re-instantiation
cannot. If a build item needs a number, that number is currently unavailable for 40/41 kits.

### 5.7 Six kits are structurally unmappable and one is empty

Six kits carry `deviation_class='engine_inexpressible'` and are routed to open dockets 149–154:
`gd-berserker-wereforms` · `gd-blight-fiend-ritualist` · `gd-pet-conjurer` · `gd-reap-spirit` ·
`gd-retaliation-warlord` · `gd-skeleton-ritualist`. Five of the six are the **summoner/pet lane**;
the sixth (`gd-retaliation-warlord`) is the retaliation lane, described in its own row as *"the
absence IS the gap"* — there is no player-initiated delivery token for stand-and-tank-return.

`gd-berserker-wereforms` has **0 mechanisms** in this census and every dossier family abstained:
Fangs of Asterkarn is unshipped, so there is no source content. It is a roster placeholder, and any
denominator that includes it is honestly 40, not 41. All percentages here use 41.

### 5.8 What I did not probe

Loot / drop mechanics, movement outside combat, resistance caps, difficulty scaling, crafting.
Out of scope for a mechanism census; also unattested in these tables.

### 5.9 Zero-probe ledger (reproducible; run the script bare)

| Seed family searched | kits matched |
|---|---:|
| knockdown / knockback | 0 |
| soft CC: slow / chill applied to enemies | 0 |
| % current-HP or % max-HP damage | 0 |
| on-block proc / block chance | 0 |
| internal cooldown on a proc | 0 |
| exclusive-skill constraint | 0 |
| `+N to skill` affix | 0 |
| taunt / threat manipulation | 0 |
| health / energy regeneration stat | 1 (`gd-stun-jacks`) |
| reflect (as distinct from retaliation) | 3 — all three are retaliation prose, not a separate reflect mechanic |

---

## 6. Two things that surprised me

**(a) The corpus's ailment layer is a debuff layer, not a CC layer.** I expected GD's status set —
stun, freeze, petrify, trauma, electrocute — to be the densest player-side mechanism family after
delivery. It is the *thinnest*: seven tokens over 41 kits, top entry at 12%, and the two hard-CC
families at literal zero. The reason is that the curation policy admits a status only when a fetched
anchor NAMES it, and build-guide prose overwhelmingly names elements ("cold shards", "spitting
fire") rather than statuses. The GD lane's status layer is therefore not measured — it is
*policy-suppressed*, and it will stay at zero until the `.arz` join runs regardless of how many more
guides are crawled. That is a structural property of the extraction lane, and it is worth saying
out loud before anyone reads "hard CC: 0%" as a statement about Grim Dawn.

**(b) The gear layer out-ranks most of the skill layer.** Three of the top eight mechanisms are
gear-borne (conversion 41%, set-threshold 34%, CDR 15%), and conversion alone ties with the densest
*cadence* mechanism. On kit-count, "the item changes what the skill does" is a more common GD build
statement than any ailment, any trigger shape, and every delivery shape except ground-zone. I had
assumed gear-borne mechanics would sit in the long tail; they sit at the head.

A third, smaller: `gd-cadence-witchblade` is the **only** kit in the lane carrying a swing-count
accumulator (`mark_identity`) and the **only** one with an apply-consume trigger pair. On the G-5
rule that is a textbook "only impacts one build → re-entry tag" — except that `gd-krieg-death-knight`
runs the same Cadence skill and its deviation row asks for the same two-tier accumulator in prose
without the typed field being set. The kit-count says 1; the mechanism's real reach is 2. **Where a
mechanism sits at count 1, check the deviation prose before tagging it a singleton** — that is the
one place this census's headline column can mislead.

---

## 7. APPENDIX — engine-side annotations already on these rows (NOT GD mechanisms)

Reported because I hold them; flagged because they are our coordinates, not GD's. Gandalf's mapping
pass owns their interpretation.

**T4 doors assigned (`mapping_json$.t4_doors`), by kit-count:**
ELEMENT_CONVERSION_MONO 9 · ZONE_CONTROL 6 · PERSISTENCE_ENGINE_uptime 6 ·
PERSISTENCE_ENGINE_saturation 6 · PROXY_ASCENSION 5 · GEOMETRY_COLLAPSE 4 · MOMENTUM_CASCADE 3 ·
ELEMENT_CONVERSION_PHYSICAL 3 · TEMPORAL_CHARGE 2 · ELEMENT_CONVERSION_HYBRID 2 ·
RETRIBUTION_ENGINE / RESONANCE_LOOP / PROXY_SOVEREIGNTY / PROXY_FISSION /
GEOMETRY_PROPAGATION_overkill / DUAL_PROXY / DEFENSIVE_TRADEOFF 1 each.

**Element register attested (`element_primary`/`_secondary`), by kit-count:**
fire 11 · shadow 9 · lightning 9 · water 3 · earth 3. (Register, not mechanism.)

**T4 transition shape (`kit_delta_t4.shape`):** step 26 / ramp 15 — all 41 rows
`shape_signoff='unvalidated'`.

**Open GD-sourced dockets:** 149–154, all `engine-design-intake`, all `open`, all from §5.7's six
`engine_inexpressible` kits.

---

## 8. Provenance ledger

**MEASURED (typed columns / typed JSON fields; reproducible via the script):** every STRUCTURED row
in §4, all §1 row counts, §5.2's ailment tally, §5.6's coverage counts, §7 in full.

**PROSE-DERIVED, hand-adjudicated:** every PROSE row in §4. Regexes are in the script; every hit
carries an evidence snippet under `--evidence`; 14 hits were rejected with reasons in §3. A different
adjudicator could reasonably differ on two of my rejections (`P-RETAL` × 2 — I ruled variant-lane
mentions out of the primary count; counting them gives P-RETAL = 3). No other rejection is close.

**INFERENCE — two, labelled, neither banked:**
1. §6(a): that the zero hard-CC count is a *policy* artifact rather than a property of the kit
   population. Grounded in the corpus's own struck-token prose plus the `.arz` monster-side counts
   from my 2026-07-25 attestation census — but the player-side join that would prove it does not
   exist. Falsifiable by running J3.
2. §4.1's consolidation groupings. Which of the 21 `geometry_value` strings folds into which
   canonical delivery mechanism is my judgment. The unions are shown so the judgment is inspectable,
   and the un-consolidated rows are retained in §4 so nothing is lost by disagreeing with me.

**NOT DONE, by scope:** no fit-vs-gap ruling against engine surfaces (gandalf's pass). No schema
designed, no DDL authored, no `MIGRATION.md` entry written, no row written to `corpus.db`. The §4.1
schema-redundancy observation is a docket item, not a change.

---

**Signed:** elrond, 2026-07-25. Substrate votes. Measured and inferred are kept apart, and the
absences are named.
