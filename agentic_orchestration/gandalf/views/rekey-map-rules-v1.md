# Corpus → engine-key mapping rules v1 (the mapping pass)

> **Authored:** gandalf 2026-07-12, post-mega-probe. **Authority:** the six Q21 rulings (`rekey-prep/*-prep.md` §5/§6) + Q22 (support RETIRED — Matt 2026-07-12) + spec `corpus-rekey-spec-v1.md` §2 (engine frame = schema of record). **Input:** `agentic_orchestration/legolas/research/megaprobe-2026-07-12/*-facts.jsonl` (positives full-schema; SKIP negatives — count only). **Output:** `agentic_orchestration/gandalf/views/engine-key/` — `corpus-engine-key-v1.jsonl` + `judgment-queue-v1.md` + `boards-v1.md`.
>
> **Prime law:** these rules are DETERMINISTIC. Where a rule does not resolve, emit a `J-*` judgment flag and DO NOT guess — gandalf reviews flagged kits per-kit. Facts stay finer than vocabulary: every output row carries its probe facts as provenance regardless of what the key says.

## 1. GEO — (footprint × delivery × commitment) → engine 24-type rich palette

Target vocabulary (engine `_RICH_TO_SPATIAL` keys, `geometry_derivation.py`; `chain` rename live): `circle, ground_targeted_circle, aura, ring, vortex_pull, whirlwind, cone, melee_arc, line, beam_channel, chain, fork, ricochet_bounce, single_target, multi_projectile, melee_strike, ground_slam, leap_strike, totem, self_buff, blink, teleport, dash_attack, defensive_dash`.

Apply IN ORDER; first match wins:

| # | condition | engine type |
|---|---|---|
| R0a | `movement.skill_is_movement=true` | by geo_text verbs: blink/phase→`blink` · teleport/portal→`teleport` · dash/charge/rush→`dash_attack` · leap/jump/slam-landing→`leap_strike` · defensive reposition/backstep→`defensive_dash` · ambiguous→**J-MOV** |
| R0b | placement kit (totem/turret/trap PLACED as the cast; the placed object acts) | `totem` — the kit's own hit geometry is the placement; minion/totem attack texture stays in mechanics_notes. Army-summon kits whose primary output IS minions → `totem` + **J-SUM** flag (SU census carries mechanism) |
| R0c | no hit geometry at all (pure buff/stance) | `self_buff` |
| R1 | footprint `chain-hop` | `chain` |
| R2 | geo_text pull-to-center/vacuum verbs | `vortex_pull` |
| R3 | footprint `cone` | melee-range (atlas range or geo_text melee verbs) → `melee_arc`; else `cone` |
| R4 | footprint `ring` | `ring` |
| R5 | delivery `beam` (any footprint) | commitment `channel` → `beam_channel`; else `line` *(G2's 14 true beams land here; arc/spark confirmed NOT beams stay out)* |
| R6 | footprint `lane` (non-beam) | `line` |
| R7 | footprint `multi-point` | geo_text fork/split→`fork` · bounce/ricochet→`ricochet_bounce` · else `multi_projectile` |
| R8 | footprint `small-radius` or `large-zone` | delivery `at-target`→`ground_targeted_circle` · `self-origin`: spin/sustained-rotation→`whirlwind`, slam/quake @melee→`ground_slam`, else `circle` (nova/PBAoE) · `projectile`→`circle` (impact blast; delivery stays descriptor) · `aura-pulse`→`aura` · `orbit`→**J-ORB** (no orbit family in palette; candidates ring/vortex_pull; possible GX) |
| R9 | footprint `point` | melee verbs/range→`melee_strike` · delivery `self-origin`+slam→`ground_slam` · delivery `projectile` or `at-target`→`single_target` |
| R10 | anything else (`other`/conflict) | **J-GEO** — no forced bin |

Radius SIZE is a parameter, not a type (small-radius and large-zone both land in circle-family; carry footprint verbatim). Confidence = min(delivery.conf, footprint.conf); post-cutoff caps ride through.

## 2. CTRL — centrality → role treatment (Q22: support RETIRED — target enum `damage / control / hybrid`)

- centrality `core` → `control` *(C2 sweep: core kits are control-via-damage — that IS the genre's control class)*
- centrality `rider` → `damage` + `control_rider: [ailments]` *(the C1 prior, resolved per-kit by the probe's own facts — no blanket re-key of the old 123)*
- centrality `none`/absent → `damage`
- `hybrid` is NEVER auto-assigned — reserve for gandalf judgment (**J-CTRL** where facts genuinely split)

**Ailment mapping — map by MECHANIC, never by name** (name-lineage law; PoE "shock" = damage-amp ≠ engine `shock` = lightning hard-control):

| corpus mechanic | engine ailment |
|---|---|
| slow (move/action speed) | `chill` |
| ignite/burn DoT | `burn` |
| immobilize/root/entangle | `root` |
| push/knockback/pushback | `knockback` |
| phys bleed DoT | `bleed` |
| chain-propagating lightning lock | `shock` |
| holy ground / sanctify | `consecrate` |
| life-drain/decay DoT | `drain` |
| **hard freeze, stun, fear, blind, taunt, curse/hex, silence, damage-amp debuff (PoE shock), attack-slow-only** | **GAP-AILMENT:`<class>`** — no engine mechanic; census rows feed ailment-layer design (freeze-escalation already queued there) |

Output: `ctrl: {treatment, ailments_mapped[], ailment_gaps[]}`.

## 3. DEF — primary layer → ruled 5-bin (`tank / mitigate / evade / absorb / glass`)

| primary layer | bin |
|---|---|
| `armor`, `hp-stack` | `tank` |
| `resist` | `mitigate` |
| `dodge` | `evade` |
| `shield-absorb` | `absorb` |
| `glass` / no layers | `glass` |
| `sustain-leech` | `tank` + rider `sustain:leech` — **and count these** (Fork D4 below) |
| `block` | per D2 ruling: key to the layer the block-effect EXPRESSES (mechanics_notes/geo_text physics: binary negate→`evade` · flat-absorb→`absorb` · percent-reduce→`mitigate`) + rider `trigger:block`; physics unreadable → **J-DEF** |
| `minion-shield` | **`tank` + rider `su-proxy` — gandalf-RULED under the D2 delegation (veto open):** the VERB is tank (something stands between you and the hit); the MECHANISM (proxy army) belongs to the SU gap census; the fact layer keeps `minion-shield` verbatim, so D3 representational-completeness is satisfied where facts live — bins stay verb-pure. Genre: D2 skelemancer / PoE meat-shield / LE minion necro all play the army AS the armor plan |
| other/unlisted coinage | **J-DEF** — vocabulary-growth candidate per D3 condition; do not bend |

**Fork D4 (new, evidence-gated):** if `sustain-leech` PRIMARIES exceed ~10 kits, sixth-verb candidacy escalates to Matt (D3 growth condition); below that, rider-on-tank stands (D2 leech-barb IS the eat-the-hit archetype — leech funds the tank plan).

## 4. ECON — model → engine-native | partial | gap

| model | status |
|---|---|
| `spend`, `cooldown` | `native` |
| `self-cost` | `native` (T4 RESOURCE_CONVERSION) |
| `meter` | `native-partial` — record `meter_type` (rage/combo/focus/charge); feeds doc-48 assigner |
| leech-funded | `partial:LC` |
| `reserve` | `gap:RS` (GX-05 partial) |
| `ammo` | `gap:AM` · `proc` → `gap:PC` · `recipe` → `gap:RC` · `draft` → `gap:DR` · `harvest` → `gap:HV` |
| summon economy (model=summon OR builder_source=minions) | `gap:SU` |
| def rider `trigger:block` present | ALSO emit `gap:BT` (block-trigger census, D2 ruling) |

## 5. MOB + ELEM — descriptors only, NEVER keyed

- MOB: mobility is EMERGENT (Matt ruling — returns post-emission as battle-sim hypothesis-test label). Carry `{skill_is_movement, policy_while_casting, verbs}` as descriptor metadata. No axis.
- ELEM: element = FREE AXIS (no corpus→engine mapping EVER). Carry `elem_raw` (label_verbatim) provenance-only + `damage_mode` descriptor (feeds ailment-layer design). Emit NOTHING keyed.
- Prefix claims: pass through verbatim (already source-verified by the probe).

## 6. Output record + boards

Per positive row: `{kit_id, game, folk_name, engine_geometry:{value, rule_fired, conf}, ctrl:{treatment, ailments_mapped, ailment_gaps}, def:{bin, riders, conf}, econ:{status, gaps, meter_type}, mob:{...descriptors}, flags:[J-*], provenance:{delivery, footprint, elem_raw, atlas_key}}`

**Boards (`boards-v1.md`):**
1. **Mechanics-gap leverage** — per gap code (SU/AM/PC/RC/RS/DR/HV/BT): kit count + kit list → **pause-2/V3 consumes** (§F.5(2) maximal-coverage objective)
2. **Geometry distribution** — engine type → count (+ J-GEO/J-ORB counts) → atlas/census refresh
3. **Ailment-gap census** — GAP-AILMENT class → count → ailment-layer design
4. **Def-bin distribution** + sustain-leech-primary count (Fork D4 evidence) + block-physics split (evade/absorb/mitigate counts)

Judgment queue (`judgment-queue-v1.md`): every J-flagged kit with its facts inline, grouped by flag class — gandalf resolves per-kit.

## 7. v1.1 amendments (gandalf 2026-07-12, post-first-run verification — supersede where they touch)

First-run spot-check (verify-at-first-commit) caught three mechanical fixes + codified two adaptations:

1. **CTRL shock law (TIGHTENED — replaces any chain-context heuristic):** corpus `shock`/`jolt` maps to **GAP-AILMENT:damage-amp, ALWAYS.** Engine `shock` (chain-propagating hard-lock) is an RDR-original mechanic — NO corpus kit expresses it; it is unreachable from corpus facts. Hard locks in the corpus are `stun` (already GAP).
2. **GEO placed-lane:** delivery `at-target` + footprint `lane` → **J-GEO:placed-lane**, never `line` (these are placed walls/zones — D2 Firewall, DI Bone Wall — the engine's `line` is a cast pierce-line; placed blocking/zone-lane geometry is the Q15 **Walls** named-workstream gap; these rows are its corpus demand evidence).
3. **DEF layer synonyms (fact-register → bin, physics-identical):** `ward` (LE) → `absorb` · `energy-shield`/`ES` (PoE) → `absorb` · `evasion` → `evade`. These are game-verbatim names for listed physics, not new layers.
4. **ECON `channel` model** → `native` (spend-while-channeling variant; commitment axis already carries channel). Compound models (`spend+cooldown`, `spend+ammo`) → map each part (ammo part still censuses `gap:AM`). Post-cutoff `unknown` → stays `UNKNOWN` census row (post-cutoff law).
5. **Board 1 SU correction:** the SU *economy* count (kits whose resource model IS troop-management) understates mechanics DEMAND. Board 1's SU row must ALSO cite the placement/army demand number = `totem`-keyed kits + J-SUM flags (mechanics-leverage is what pause-2/V3 consumes; Matt's §F.5(1) explicitly names the summon/totem corpus).

**Fork D4 evidence landed:** sustain-leech primaries = **12 > 10 threshold → ESCALATED to Matt** (kit list in boards; gandalf lean documented in the escalation: PoE itself files leech under *recovery*, not defense — genre supports rider-not-verb).

**Signed:** gandalf 2026-07-12. Rules serve the corpus; where they can't express a kit, the kit flags rather than bends. v1.1 same-day post-verification.
