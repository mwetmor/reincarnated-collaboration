# VDM-1 Crosswalk Tables — source-game vocabulary → engine vocabulary

> **STATUS:** CURRENT (load-bearing for VDM-1 Stage-2 mapping authoring) — run artifact under the VDM-1 charter (`2026-07-18-vdm1-charter.md` §3 stream-4, §7 seam routing).

**Date:** 2026-07-18 · **Author:** gandalf (run steward; SPEC-AUTHOR) · **Authority:** Matt 2026-07-18 — VDM-1 autonomous run mandate (R-1..R-9)

**Purpose:** deterministic translation from source-game terms (as the dossier extracts them) to engine coordinates, so mapping rows are consistent across 585 kits and across sessions. Every table has a judgment escape: a per-kit override is legal iff it carries a `fidelity_note`. When NO lane fits → parsimony ladder (charter §5), terminal `MAPPED_DOCKET`.

**Engine-truth sources (read 2026-07-18):** `generation/geometry_derivation.py` (26 geometries) · `config/ailments.yaml` (16 ailments) · `data/seasonal_elements/pool.json` (7 families / 214 names) · `generation/t4_catalog_v2.py` + `layer2_dimensions.py` (26 T4 strategies + CAPSTONE_LAYER2) · `generation/resource_economy.py` (40 keys + enums, Waves B/C) · trait architecture per B9a (intrinsic pool + element/mechanic-gated gear affixes).

---

## §1 — Element crosswalk (source damage type → 7 engine families)

Engine families (pool primary_slot): **fire · water · wind · earth · lightning · holy · shadow**. Water carries the cold/ice name register (frost, ice, glacier…). **There is NO physical element family** — see the physical rule below.

| Source term | Engine family | Note |
|---|---|---|
| fire / burn / ignite (all games) | fire | |
| cold / ice / frost (all games) | water | ice-register names within water family |
| lightning / shock damage (all games) | lightning | |
| poison / nature / acid (PoE chaos-poison, GD acid, D2 poison) | earth OR shadow | earth when nature/venom-themed (druid, plants); shadow when corruption-themed (necro, chaos); ailment lane = `poison` either way |
| chaos (PoE) | shadow | drain-DoT lineage; chaos-poison kits see row above |
| shadow / dark / bone / necrotic (D2/D3/D4 necro, LE void/necrotic) | shadow | |
| holy / sacred / light (D2 pala, D4 sacred, LE void-touched inverse) | holy | |
| arcane (D3 wizard) | shadow default | void-register read; per-kit override legal (e.g. arcane-lightning behavior → lightning) w/ fidelity_note |
| aether (GD) | lightning OR shadow | per-kit: aether-ray/energy → lightning; aether-corruption → shadow |
| vitality (GD) | shadow | life-drain register |
| elemental (GD tri-element) | kit's dominant OR fire | pick the build's actual scaling element from dossier; fidelity_note the composite |
| **physical (all games)** | **no family** | THE PHYSICAL RULE: physical is ailment-substrate only (bleed/stun/poison-venom). Physical kits keep element-slot = the kit's secondary element if any; pure-physical kits map element-neutral (element carries flavor only) and express identity via geometry+ailment (bleed/stun) + `ELEMENT_CONVERSION_PHYSICAL` T4 when conversion is the build's point |

**Hybrids:** source dual-element kits (elem_p + elem_s columns already in corpus) map both slots directly; 7×7 space is native. Triple+ → keep top-2 by scaling weight, fidelity_note the drop.

## §2 — Ailment crosswalk (source status → 16-ailment registry)

Registry: burn · chill · root · knockback · bleed · shock · consecrate · drain · sunder · freeze · stun · poison · blind · curse{amplify, weaken, decrepify, sap} · fear · execute. Deflect is NOT an ailment (def-bin rider `deflect_condition`).

| Source status | Engine ailment | Trap notes |
|---|---|---|
| PoE ignite / D-burn | burn | |
| chill / slow / cripple (movement) | chill | D3 slow, GD trap-slow → chill |
| **PoE shock (increased damage taken)** | **sunder** | ⚠ FALSE FRIEND: our `shock` = paralysis-on-arc hard CC. PoE damage-amp shock = our sunder (0.10-0.50 damage_taken_percent = PoE shock band exactly) |
| stun / interrupt (physical heavy hit) | stun | |
| freeze (hard immobilize, cold) | freeze | shatter payoff native (threshold burst) |
| root / immobilize / entangle | root | |
| knockback / repel | knockback | |
| bleed / lacerate / rupture | bleed | |
| poison / venom / caustic (stacking DoT) | poison | stack-additive native (cap 5-10) |
| life-drain / essence drain / decay | drain | |
| blind / smoke / dim vision | blind | accuracy-tax only |
| fear / terror / horrify | fear | boss-immune; exclusive with taunt |
| PoE Vulnerability / D2 Amp Damage | curse:amplify | caster-radius persistent |
| PoE Enfeeble / D2 Weaken | curse:weaken | |
| PoE Temporal Chains / D2 Decrepify | curse:decrepify | |
| PoE exposure / armor-shred / GD RR | curse:sap (persistent, caster-anchored) OR sunder (timed, on-hit) | pick by application shape: aura/hex → curse; hit-proc window → sunder |
| execute / culling strike (kill-threshold) | execute | PoE cull 10% = execute_threshold_fraction 0.10 |
| consecrated ground / hallowed zone | consecrate | holy only |
| taunt | — (fear-slot exclusive) | record in fidelity_note; no taunt ailment in solo scope |

## §3 — Supports / passives → five landing lanes

Source "supports" (PoE gems, D3 runes, GD devotion procs, LE skill-tree nodes) do NOT map to one lane. Route by what the support DOES:

| Support class | Engine lane | Vocabulary |
|---|---|---|
| geometry-modifying (GMP/LMP, Chain, Fork, Pierce, Spell Echo, Multistrike, AoE size, extra projectiles) | **skill_geometry fields** | geometry_value from the 26; projectile counts; chain/fork native geometries (`chain`, `fork`, `ricochet_bounce`); orbit_* keys; placed_lane_* keys |
| cost / cadence / efficiency (Inspiration, faster casting/attacks, reduced mana) | **resource_economy chassis** | cost_scale · cost_slope · cadence_scale · regen_shape/magnitude · on_kill_frac · ramp_per_s |
| trigger (CoC, CwDT, cast-on-melee-kill, D3 proc runes, GD devotion proc-on-X) | **trigger grammar (Wave-C)** | proc_trigger_condition ∈ {on-hit-threshold, on-crit, on-cast-linked, on-kill, on-damage-taken, on-mark-apply, on-mark-consume, on-block-successful, on-ailment-application, on-defender-death} · trigger_chain_shape ∈ {apply-only, consume-only, apply-consume-pair} · consequence_type ∈ {apply-mark, consume-mark, linked-cast, resource-fill, ailment-overwrite, burst-damage} · MAX_CHAIN_DEPTH=1 LOCKED — source trigger-chains deeper than 1 → APPROX grade + fidelity_note, never a depth mint |
| ailment-granting/scaling (Chance to Bleed, Unbound Ailments, Hypothermia) | **ailment registry params** | the 16 + param_ranges; ailment-scaling supports → trait-rank analog |
| pure numeric scalers (Ele Focus, Controlled Destruction, Melee Phys, %increased) | **traits / gear affixes** | B9a intrinsic trait pool (rank-stacked) OR element/mechanic-gated gear affix; NEVER skill-specific gear affixes (trait-architecture law) |
| reservation / blood-magic (Arrogance, aura reserves, LE reserve nodes) | **resource_economy RS/LC** | reservation_percent (≤0.75 LOCKED) · reservation_flat · reservation_resource ∈ {mana, focus, stamina-as-resource, rage, spirit, hp} · hp_cost_scale (≤0.30 LOCKED) |
| stance / toggle / channel-maintain | **resource_economy PC** | persistent_condition_shape ∈ {tick-cost, activation-toggle, proc-loop} |
| charge / stack builders (PoE charges, D3 stacks, LE rage) | **resource_economy charge-stack** | charge_stack_sub_shape ∈ {accumulator, cycle} + AM/RC fields |
| thorns / retaliation / leech-on-taken | **resource_economy TH** | damage_taken_converts_shape ∈ {reflect-damage, resource-fill, stack-fill}; reflect ≤1.0 LOCKED |

**Chain-link law:** engine skill chains are length {2,3}. A source 6-link is a SKILL + its modifiers, not six skills — decompose: primary skill → geometry+element; supports → lanes above. The "6-link" itself never maps to chain count.

## §4 — Items → lanes

| Item effect class | Engine lane |
|---|---|
| numeric modulation (more damage, +levels, res, attribute stacking) | gear-affix lane (element/mechanic-gated rolls; tier sets per-rank rate) |
| mechanic-granting uniques (Mjölner trigger, The Squire, CoDominance) | trigger grammar as kit-declared fields (dossier `item_alterations` feeds this) — the ITEM dissolves; its MECHANIC lands on the kit |
| economy-warping (Shavronne's low-life, Mageblood, Blood Magic items) | resource_economy keys; pair with DEFENSIVE_TRADEOFF / SACRIFICE_ASCENDANCY T4 when the warp IS the build identity |
| skill-granting items (whispering-ice, D2 +skill charges) | the granted skill maps as a core skill; item recorded in fidelity_note |
| none of the above | parsimony ladder → mechanic_gap_docket |

## §5 — Capstones → 26 T4 strategies (routing groups)

| Source capstone shape | T4 candidates |
|---|---|
| element conversion (Avatar of Fire, phys-to-X, tri-ele) | ELEMENT_CONVERSION_MONO / _HYBRID / _PHYSICAL · ELEMENTAL_ECHO |
| life/defense trade (CI, Pain Attunement, low-life, MoM) | DEFENSIVE_TRADEOFF · SACRIFICE_ASCENDANCY · RETRIBUTION_ENGINE |
| shape/phase cycling (stance dancing, form rotation surrogates) | PHASE_MOMENTUM |
| AoE/geometry warps (conc effect identity, nova-shape keystones) | GEOMETRY_COLLAPSE · GEOMETRY_INVERSION · ZONE_CONTROL |
| on-kill propagation (Herald explosions, GD Devastation chains) | GEOMETRY_PROPAGATION_cascade (on-kill) / _overkill (on-hit scaling) |
| charge/stack engines (PoE charges, rampage, D3 momentum) | TEMPORAL_CHARGE · MOMENTUM_CASCADE · RESOURCE_CONVERSION |
| minion/proxy ascendancies (necro, totem hiero, GD pets) | PROXY_ASCENSION · PROXY_SOVEREIGNTY · PROXY_FISSION · PROXY_INVERSION · PROXY_CONVERGENCE · DUAL_PROXY |
| companion pacts (LE beastmaster, D4 companions) | COMPANION_CONTRACT · MONSTER_PACT |
| aura/network amps (Aurabot-adjacent self-stacking, curse networks) | NETWORK_AMPLIFIER · RESONANCE_LOOP |
| DoT/uptime ramps (RF, ED/C, GD DoT-tank) | PERSISTENCE_ENGINE_uptime / _saturation |

Layer-2 pins (trigger/stackability/magnitude/scaling per strategy) are already fixed in CAPSTONE_LAYER2 — mapping only picks the STRATEGY; never re-pins Layer-2.

## §6 — Geometry phrase-book (source language → 26 types)

nova/burst-around-self → `ring` · pool/patch/ground DoT → `ground_targeted_circle` · spin-to-win → `whirlwind` · dash-strike/charge → `dash_attack` or `leap_strike` · blink/flame-dash → `blink` (utility) / `teleport` (offensive reposition) · beam/ray/channel → `beam_channel` · shotgun/volley/barrage → `multi_projectile` · bouncing → `ricochet_bounce` · splitting → `fork` · arcing between targets → `chain` · cone/breath/sweep → `cone` · wall/lane → `placed_lane` · orbiting blades/stormcaller → `orbit` · totem/sentry/turret → `totem` · pull/vacuum → `vortex_pull` · slam/quake → `ground_slam` · wide melee swing → `melee_arc` · single hit melee → `melee_strike` · self-shield/guard → `self_buff` or `defensive_dash` · aura/presence → `aura` · straight-line pierce → `line` · single-target spell → `single_target` · expanding circle → `circle`.

## §7 — Precedence + escapes

1. Deterministic row applies → use it (grade EXACT/CLOSE per fit).
2. Two rows compete → pick by the build's DOMINANT loop (what the player does every 3 seconds, not what the guide brags about); fidelity_note the alternative.
3. No row fits → APPROX + fidelity_note, or ladder-step 3/4 (mint, ledgered) if approximation misses the kit's IDENTITY.
4. Mechanism class with no lane at all (e.g. union/recipe evolution; form-swap pending GX-02) → `MAPPED_DOCKET`, mechanic_gap_docket row.
5. Mapping provenance is always `authored-vdm1` — the epistemics wall: extraction speaks only what pages say; mapping is OUR authored judgment against it.

---

**Cross-references:** charter §3/§5/§7 · run-state ledger `notes/2026-07-18-vdm1-run-state.md` · elrond schema `research/curated/MIGRATION-vdm1-schema-2026-07-18.md` · Wave-B/C specs (reap-die-rise-engine) for enum lineage.

Tracker-delta: none (run-internal working reference; tracker registration lands with THE REVIEW BOOK per charter §8).

**Signed:** gandalf (SPEC-AUTHOR) · **For:** deterministic source→engine translation for VDM-1 mapping authoring.
