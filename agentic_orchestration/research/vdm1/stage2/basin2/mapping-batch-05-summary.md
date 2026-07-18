# VDM-1 basin-2 mapping — batch-05 summary (b05 window, all Last Epoch)

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18 · **Window:** b05 (le-49–60) · **Roster:** 12 kit_ids; MAPPED 11, SKIPPED 1 (le-harvest-lich).

> Histogram is ADVISORY — the steward recounts from committed files (D-2c). Grade honesty over optimism.

## Grade histogram (11 mapped)

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 8 | lightning-blast · fire-aura-spellblade · flame-reave-spellblade · frost-claw · frost-wall-rm · hammer-throw-paladin · healing-hands-paladin · judgement-paladin |
| APPROX | 1 | ghostflame-warlock |
| GAPPED | 2 | low-life-ward · manifest-armor |

**Terminal:** 9 MAPPED · 2 MAPPED_DOCKET (low-life-ward, manifest-armor). R-M7 biconditional clean (GAPPED ⟺ MAPPED_DOCKET; the lone APPROX stays MAPPED).

## SKIP annotation (roster completeness)

**le-harvest-lich SKIPPED — CHIMERA** (kb folk name conflates Harvest Flay Lich + Death Seal Lich; all families UNSUPPORTED); cannot grade fidelity against a build that does not exist as recorded; split/re-anchor rides the review book; mapping deferred to post-split. No mapping row and no empty-shell row emitted.

## Per-kit one-liners

- **le-low-life-ward** — GAPPED/DOCKET. §B ward-from-missing-health, item-defined archetype (Exsanguinous + Last Steps); mapped WITH-items form as core (no rankable skill → null geometry). Ward-from-missing-health inversion = defense-from-inverted-stat, no native lane → docket (consolidates basin-1 overheal-above-cap). T4 DEFENSIVE_TRADEOFF.
- **le-lightning-blast** — CLOSE. `chain` lightning; §B Reowyn ward-burst rider EXERCISED (first attestation). shock WITHHELD (Spark Charge = named proc; "electrify" only in claim_text). T4 ELEMENTAL_ECHO.
- **le-fire-aura-spellblade** — CLOSE. `aura` fire (+water cold-conversion), freeze on cold-variant only; aura is PASSIVE-EMERGENT not Flame Ward (corrected). Depth-3 Firebrand→FrostClaw→IceBarrage cascade capped at MAX_CHAIN_DEPTH=1 → rider. T4 ELEMENT_CONVERSION_MONO.
- **le-flame-reave-spellblade** — CLOSE. `cone` fire (Sunwreath cone→circle transform = rider); Flame Drinker aura-consume-for-mana economy. T4 GEOMETRY_COLLAPSE.
- **le-frost-claw** — CLOSE. `multi_projectile` water, chill+freeze; Elemental Nova per-cast proc (Celestial Conflux) = trigger rider; Frostbite (cold-DoT) NO-HOME withhold. T4 ELEMENTAL_ECHO.
- **le-frost-wall-rm** — CLOSE. `placed_lane` water, freeze (boss-immune, guaranteed) + chill; Pyroglass fire-conversion→Brand of Trespass = RM rune rider. T4 ZONE_CONTROL.
- **le-ghostflame-warlock** — APPROX. `cone` shadow(+fire) channel jet (geo-erratum reading); channel tick-cost economy. TWO+ status withholds (see near-misses) leave the DoT payload uncarried. T4 PERSISTENCE_ENGINE_uptime.
- **le-hammer-throw-paladin** — CLOSE. `orbit` physical-neutral (THE PHYSICAL RULE); Sigils→Symbols era name note; Nova-form (Enra's+Avatar) variant fork disables orbit. T4 GEOMETRY_PROPAGATION_cascade.
- **le-healing-hands-paladin** — CLOSE. `ring` fire+holy proc-on-melee (Cleric's Hammer on-hit trigger); heal-as-weapon. era restamped 1.0-launch (1.1 CONTRADICTED/errata'd); Rahyeh's Chariot role-conversion = fidelity rider. T4 RETRIBUTION_ENGINE.
- **le-judgement-paladin** — CLOSE. `ground_targeted_circle` fire+holy, consecrate; stacking Consecrated Ground zones (Lingering Force multiplier). T4 ZONE_CONTROL.
- **le-manifest-armor** — GAPPED/DOCKET. Pet-core autonomous construct → summoner-deferral GAP (null geometry, pursue/follow no-placement convention). Resource CORRECTED **Mana** ("Forge Stacks" = probe fabrication, NEVER echoed). gear-stat-as-minion-scaling → docket. T4 PROXY_ASCENSION.

## T4-door frequency

| T4 door | Count | Kits |
|---|---|---|
| ZONE_CONTROL | 2 | frost-wall-rm · judgement-paladin |
| ELEMENTAL_ECHO | 2 | lightning-blast · frost-claw |
| DEFENSIVE_TRADEOFF | 1 | low-life-ward |
| ELEMENT_CONVERSION_MONO | 1 | fire-aura-spellblade |
| GEOMETRY_COLLAPSE | 1 | flame-reave-spellblade |
| PERSISTENCE_ENGINE_uptime | 1 | ghostflame-warlock |
| GEOMETRY_PROPAGATION_cascade | 1 | hammer-throw-paladin |
| RETRIBUTION_ENGINE | 1 | healing-hands-paladin |
| PROXY_ASCENSION | 1 | manifest-armor |

All single-door (R-M1: engine tokens only). No door assigns >2 — a spread batch (LE Sentinel/Mage/Acolyte mix); the two ZONE_CONTROL and two ELEMENTAL_ECHO are the only repeats, both well-motivated (placed-lane control; per-cast echo cascades).

## Candidates

**mint-candidates: NONE.** Parsimony ladder honest — every gap this batch routes either to the existing summoner-deferral GAP or to an existing docket class; no new geometry/ailment/economy PRIMITIVE is forced. No `mint-candidates-batch-05.jsonl` written.

**docket-candidates: 2** (`docket-candidates-batch-05.jsonl`):
1. **ward-from-missing-health (low-life inversion economy)** — evidence: low-life-ward, fire-aura-spellblade (host variant). CONSOLIDATES basin-1 overheal-above-cap (ward = decaying overshield; missing-health = the docket-worthy scaler). §B row governs. Steward-held; do NOT merge with GD retaliation-substrate or the armour cluster.
2. **gear-stat-as-minion-scaling** — evidence: manifest-armor. Player's equipped-gear stats scale a summoned proxy (Helmet/Body/Gloves/Boots/+Weapon). Distinct from generic minion scaling (§A: pet-stat lane ≠ player-stat lane); rides with the summoner-deferral resolution. Own row.

## §0 near-misses (statuses WANTED but could not attest, per kit)

- **low-life-ward** — none (n/a element, no status semantics).
- **lightning-blast** — **shock** WITHHELD. `elem_raw=lightning` + mechanics claim "shock/electrify," but "Spark Charge" is a named skill/item PROC not a status (§0.4), and "electrify" lives only in `verify_ledger.claim_text` = INADMISSIBLE (§0.2). No fetched behavioral status language. (Main-law reminder: even if attested, LE shock → `sunder` + the shock-requires-CC rule.)
- **fire-aura-spellblade** — **burn** WITHHELD for the fire aura ("deal Damage to anything nearby" ≠ burn, §0.1). freeze ADMITTED only on the cold-conversion behavioral line ("freezing and breaking apart entire packs").
- **flame-reave-spellblade** — **burn** WITHHELD (fire cone, no NAMED status; "fire hit damage" is claim_text).
- **frost-claw** — **Frostbite** (LE cold-DoT, fetched "apply Frostbite") WITHHELD — NO engine registry home (same NO-HOME class as GD frostburn, WAVE-PLAN review-book list). chill + freeze ADMITTED (registry-native, behaviorally fetched).
- **frost-wall-rm** — none withheld (freeze + chill both behaviorally fetched; "guaranteed Freeze" is strong).
- **ghostflame-warlock** — **THREE withholds** (the APPROX driver): (1) **burn**/fire-DoT WANTED ("fire damage over time") but not a NAMED ignite/burn status → withheld (strict §0.1, m02 frostburn/electrocute precedent); (2) **necrotic-DoT** — no registry home (drain needs leech/decay language, absent) → withheld; (3) **Bone Curse curse:variant** — application-as-aura fetched but NO effect (amplify/weaken/decrepify/sap) fetched → variant withheld (shape-silent §2 + §0.4).
- **hammer-throw-paladin** — **bleed** WITHHELD — appears ONLY in the Bleed-Hammerdin VARIANT ("bleed DoT via spiral"), not the mapped orbit core.
- **healing-hands-paladin** — none withheld (no offensive status fetched for Healing Hands itself; heal is not an ailment).
- **judgement-paladin** — **burn** WITHHELD (fire zone "damages enemies" as a DoT patch but not NAMED as burn/ignite). **consecrate** ADMITTED ("Consecrated Ground," §2).
- **manifest-armor** — none withheld (no status named; "fire and metal" held as construct-appearance flavor not element, §0.1).

## Anything forced / judgment calls flagged LOUDLY

1. **ghostflame-warlock burn/DoT withhold (the batch's hardest §0 call).** "Fire and necrotic damage over time" is behavioral-DoT language sitting right at the §0.1 boundary — burn's DEFINITION is a fire-DoT tick, so a looser reading would admit burn. I took the STRICT reading (no NAMED ignite/burn/decay status → withhold) consistent with the m02 frostburn/electrocute NO-HOME precedent and the repeated §0 emphasis on the NAMED status. Consequence: the row's delivery (cone channel) maps but the ailment-free skill does NOT carry the DoT payload that IS the skill's damage — hence APPROX, not CLOSE. **Steward: if the run's §0 posture admits "damage-TYPE-over-time" as behavioral status attestation, this flips ghostflame burn→emit and likely CLOSE; I flag it as the single most reviewable line in the batch.**
2. **fire-aura-spellblade element_secondary=water.** The cold-conversion (Freezing Aura) is a variant, not the default; I set secondary=water + freeze to carry the ELEMENT_CONVERSION_MONO identity, but the DEFAULT build is mono-fire. Defensible either way; noted so the steward can null the secondary if variant-elements shouldn't populate the slot.
3. **healing-hands `ring` geometry.** "Small radius around the melee target" on a proc — `ring` (burst-around) vs `melee_arc` vs `ground_targeted_circle` all had a claim. Chose `ring` for the burst-around-melee-target shape; the proc-on-hit trigger carries the identity regardless.
4. **judgement ZONE_CONTROL vs PERSISTENCE_ENGINE_saturation.** DoT-uptime reading argued for PERSISTENCE; chose ZONE_CONTROL because the STACKING placement of multiple Consecrated Grounds (Lingering Force), not raw uptime, is the dominant §7.2 loop. Alternative noted in fidelity.
5. **manifest-armor null geometry (gapped-pet two-lane convention applied).** Manifest Armor "pursues enemies" = follow/pursue with no placement language → null geometry honest (not `totem`, which is the placement-attested lane). Forge Strike mapped as a secondary `ground_targeted_circle` bolt-on but is NOT the identity. chain_count=3 (Manifest Armor + Forge Strike + Shield Throw = 3 load-bearing actives, R-M2).

## Cross-batch note for the steward
low-life-ward and fire-aura-spellblade are LINKED (fire-aura is a Low-Life-Ward host variant per fetched item_alterations) — the ward-inversion docket has two evidence kits inside this single batch, strengthening the consolidation with basin-1 overheal-above-cap.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18 — D-2c recount from committed files + corpus.db)

**Recount:** advisory histogram 0E/8C/1A/2G · 9 MAPPED / 2 DOCKET = **EXACT match** against the committed JSONL (mapping-agent advisory drift now **0-for-5**: m01–m05 all exact). SKIP annotation (harvest-lich CHIMERA) verbatim-correct vs WAVE-PLAN; correctly an annotation line, NOT an empty-shell row (the m01 empty-projection convention applies to all-abstain kits, not chimera-deferrals). Docket side-file verified: 2 rows, both well-formed, destinations + evidence lists intact.

**VERDICT: ACCEPTED with 5 in-place corrections** (applied to mapping-batch-05.jsonl, audit-stamped). Post-audit histogram: **0E/9C/0A/2G · 9 MAPPED / 2 MAPPED_DOCKET.**

### Corrections
1. **healing-hands Vengeance `element_primary physical→null`** — THE PHYSICAL RULE (§1 line 30): physical is element-NEUTRAL, never an element token. Null is the honest physical carrier.
2. **hammer-throw `t4_doors GEOMETRY_PROPAGATION_cascade→PERSISTENCE_ENGINE_uptime`** — an orbit propagates nothing on-kill; `_cascade` is pinned to on-kill propagation (m04 ruling). The dominant loop is walking-damage-field uptime — the RF-class exemplar door. **The T4-door frequency table above shifts accordingly** (GEOMETRY_PROPAGATION_cascade 1→0; PERSISTENCE_ENGINE_uptime 1→2).
3. **fire-aura core row `ailments [freeze]→[]` + `element_secondary water→null`** — cold-conversion (Freezing Aura) is a listed VARIANT; fetched core is "fire (default)". Variant-scoped attributes do not ride the core row (§7.2 dominant loop; hammer-throw-bleed parity — the mapper enforced this discipline on hammer-throw and broke it here; the mapper's own flag #2 invited the null). **ELEMENT_CONVERSION_MONO door KEPT** — the conversion-capable identity is the T4 hint; the core row stays mono-fire.
4. **ghostflame `grade APPROX→CLOSE`** — the mapper's flag #1 resolved by the **damage-type-over-time RULING** (m04 audit, binding): "fire and necrotic damage over time" attests delivery TIMING, not a status — burn/decay withholds are UPHELD (the ruling does NOT admit burn), but the DoT payload IS carried by element_primary/secondary + delivery_notes, so nothing is mechanically understated → the APPROX rationale ("payload uncarried") dissolves. Forcewave-regrade precedent. Disdain + Bone Curse riders are minor, noted.
5. **manifest-armor Forge Strike `element_secondary fire→null`** — "fire and metal" is construct-APPEARANCE flavor (the mapper's own near-miss note says so); appearance never routes an element token.

### Upheld (exercised clean this batch)
- **§B ward-from-missing-health first exercise** — low-life-ward GAPPED/DOCKET honest (R-M7 "not that build"); WITH-items core per §B; null geometry on no-rankable-skill. Inversion docket consolidation with basin-1 overheal-above-cap ACCEPTED as filed (steward-held; no merge with retaliation-substrate/armour cluster).
- **§B Reowyn ward-burst rider first attestation** — lightning-blast trigger_grammar rider with DEFENSE payload; clean.
- **Withhold discipline** — lightning-blast shock (claim_text INADMISSIBLE; Spark Charge = name, §0.3/§0.4) · hammer-throw bleed (variant-scoped) · flame-reave/judgement burn (unnamed) all correct. **LE Frostbite → NO-HOME list** (joins GD confusion/electrocute/frostburn; review-book).
- **consecrate/holy CONFIRMED LEGAL** — steward's own flag withdrawn on law-check: holy IS the 6th of 7 families (§1 line 15); consecrate is holy-only (§2 line 58) and judgement carries holy secondary. Mapper right, steward flag wrong.
- **Geometry judgment calls** — healing-hands `ring` (burst-around-melee-target) · judgement ZONE_CONTROL over PERSISTENCE (stacking-placement IS the §7.2 dominant loop) · manifest-armor null geometry (two-lane convention: "pursues enemies," zero placement language) + chain_count=3 (R-M2, three load-bearing actives). All upheld.
- **gear-stat-as-minion-scaling docket** — own-row separation from the generic pet gap is correct (§A pet-stat lane ≠ player-stat lane); rides with summoner-deferral resolution.

**W2 wave verdict:** m04 ACCEPTED w/ 4 corrections + m05 ACCEPTED w/ 5 corrections → **W2 CLOSED: 22/22 mapped kits (2 SKIPs annotated) · post-audit 1E/18C/1A/2G · 20 MAPPED / 2 MAPPED_DOCKET.**
