# KF-2 Normalization-Rule Lane — rule authoring + rdr_value derivation report

**Author:** gamora (`rule_owner`, sim-seam) | **Date:** 2026-07-23 | **Run:** KIT-FIDELITY (KFL-9c)
**Math note (Discipline #1, authored BEFORE code):**
`reincarnated-engine/src/reincarnated/simulation/math/kf2-rdr-normalization-convention.md`
**Committed scripts (idempotent, byte-rebuildable):**
- `research/scripts/catalogue_migrations/corpus_kf2rules_rules.sql` — the 37 `normalization_rule` rows.
- `research/scripts/catalogue_migrations/corpus_kf2rules_formulas.sql` — E/F/G verbatim formula anchors + input-presence assertions.
- `research/scripts/catalogue_migrations/corpus_kf2rules_derivations.sql` — the `rdr_value` derivation UPDATEs + guard asserts.

**Backup:** `corpus.db.pre-kf2-rules-2026-07-23-backup` (pre-write, Discipline #8/#11).

---

## 1. RDR-unit convention (the seam call — two sentences)

> **One RDR damage point = one point of the source game's own damage number, carried through 1:1
> (IDENTITY) within that game's own scale; one RDR HP point = one source HP point; one RDR defense
> point = one point of the source game's defensive-rating number (Defense/Armour/Evasion/resist-%).**
> The transform is identity because any cross-game rescale constant cancels in the fidelity gauge
> (realized/expected) — so identity preserves each game's internal ratios exactly and makes every
> on-screen deviation from 100% a pure pipeline-drift signal; tempo scales convert UNIT (frames/cast →
> casts/sec) without changing cadence magnitude, and resolution formulas (hit/crit/mitigation) are the
> anchored expressions the composition multiplies by, not leaf rescalings.

Full derivation + rationale (why identity, not a fifth balance scale; per-hit/per-tick basis; context
fences) lives in §0 of the math note — the ONE documented home; future rules reuse it.

## 2. Per-rule table (rule_id · scale · rows derived · transform · anchor/PIN)

**37 rules authored** (all `status='active'`, `rule_owner='gamora'`, `rule_version=1`). 3 BLOCKED rules
NOT authored: **R-K5** (gd FoI base, GAP-D1), **R-N5** (gd monster, GAP-D2), **R-G4** (poe2 armour DR,
GAP-B1).

### Magnitude / tempo rules (derive a leaf rdr_value)

| rule | source_scale(s) | rows | transform | anchor/PIN |
|---|---|---|---|---|
| R-K1 | d2_fire_dps | 80 | IDENTITY (dmg/sec) | rankedboost |
| R-K2 | d2_fire_hit | 80 | IDENTITY (single-hit) | rankedboost; non-crit (PIN-A) |
| R-K3 | poe2_phys_hit | 80 | IDENTITY (proj+expl) | poe2db; N_shards via R-M3 |
| R-K4 | poe1_effectiveness_pct_v315 (+base_damage_pct_v315) | 2 | IDENTITY (59% bp) | PIN #1 (3.15); weapon DPS GAP |
| R-M1 | d2_pct_bonus_fire | 12 | IDENTITY (bonus %) | rankedboost fire-mastery |
| R-M2 | poe2_pct_more | 2 | IDENTITY (more %) | poe2db; multiplicative |
| R-M2b | poe2_pct_increased | 1 | IDENTITY (increased %) | poe2db; additive-bucket |
| R-M3 | pin_shard_count | 1 | PINNED const 10 (fixed mult) | PIN-N10 / PIN #5 |
| R-M4 | poe1_attack_speed_pct | 1 | IDENTITY (×3.0 cadence) | poedb; tempo |
| R-M5 | poe1_pct, poe2_pct | 6 | IDENTITY (mod/mitig %) | poedb/poe2db/poe-vault |
| R-A1 | d2_stat, d2_flat_life, d2_flat_mana, d2_life_per_level, d2_life_per_vit, d2_mana_per_level, d2_mana_per_energy | 20 | IDENTITY (coeff/base) | maxroll (PIN-C3 conflict) |
| R-A2 | gd_hp_per_point, gd_da_per_point, gd_oa_per_point, gd_energy_per_point, gd_hpregen_per_point, gd_dmg_pct_per_point, gd_attr_per_invested_point, gd_invested_points, gd_oada_base, gd_oada_level_coeff | 15 | IDENTITY (coeff/base) | grimdawn.com |
| R-A3 | poe2_stat_req, poe2_spirit | 6 | IDENTITY (gate) | poe2db |
| R-A4 | poe1_stat_req | 2 | IDENTITY (gate) | poedb |
| R-A5 | poe1_flat_life | 1 | IDENTITY (player pool) | overgear (one-source) |
| R-T1 | d2_frames_per_cast | 14 | **25 / sv** (casts/sec) | maxroll FCR; UNIT CONVERT |
| R-T2 | d2_seconds, poe2_seconds, gd_seconds | 5 | IDENTITY (seconds) | fextralife/poe2db/grimdawn |
| R-T3 | d2_mana, poe2_mana_per_sec, poe1_mana | 67 | IDENTITY (resource) | rankedboost/poe2db |
| R-C2 | gd_crit_mult, gd_pth_pct | 9 | IDENTITY (crit-mult tier + pth leaves) | grimdawn.com (Source E) |
| R-G3 | gd_pct | 1 | IDENTITY (absorption % leaf) | grimdawn.com (70%) |
| R-CTX-BP | poe1_effectiveness_pct_v327_context | 6 | IDENTITY, FENCED (not build point) | poedb [CONTEXT ONLY] |
| R-CTX-GEO | d2_level, d2_yards, poe1_level, poe1_weapon_dps, poe1_radius_units, poe2_count, poe2_metres, poe2_metres_per_sec | 33 | IDENTITY, FENCED (geometry/gating) | per-source geometry |
| R-N1 | d2_flat_hp, d2_defense_rating, d2_phys_hit, d2_attack_rating, d2_xp | 38 | IDENTITY (monster) | d2-act1-normal |
| R-N2 | poe1_flat_life, poe1_armour_rating, poe1_evasion_rating, poe1_damage, poe1_attack_time_sec | 38 | IDENTITY (monster) | poe1-zone68 |
| R-N3 | poe2_flat_life, poe2_armour_rating, poe2_evasion_rating, poe2_damage, poe2_accuracy_rating | 25 | IDENTITY (monster) | poe2-levelscale |
| R-N4 | pct | 44 | IDENTITY (monster resist/block/cap) | all 3 games |

### Resolution-formula rules (no leaf transform; `formula_ref` → verbatim anchor in formulas.sql)

| rule | scope | formula implemented | anchor/PIN | status |
|---|---|---|---|---|
| R-H1 | D2 received | `min(max(200%×(AR/(AR+Dr))×(ALVL/(ALVL+TLVL)),5%),95%)` | maxroll/fextralife; Dr GAP → partial | active |
| R-H2 | D2 dealt | hit_chance = 1 (spell bypass) | PIN-C2 / PIN #3 (pinned) | active |
| R-H3 | PoE1 dealt+recv | evasion-applies-to-attacks-only; **expr GAP-A2** → partial | formulas A2 (image-only) | active |
| R-H4 | PoE2 dealt+recv | projectile EVADABLE / explosion AoE-EXEMPT | PIN #6 / B2 (load-bearing) | active |
| R-H5 | GD dealt+recv | `PTH=((((OA/((DA/3.5)+OA))×300)×0.3)+(((((OA×3.25)+10000)−(DA×3.25))/100)×0.7))−50; floor 55` | grimdawn.com; OA/DA GAP → partial | active |
| R-C1 | D2 all | crit_ev = 1 (no spell crit) | PIN-A / PIN #2 (pinned) | active |
| R-C2 | GD | crit=PTH−90; mult tier 1.0→1.5 | grimdawn.com (Source E) | active |
| R-C3 | PoE1 | crit-weighted mean; **mult GAP** → partial | poe-vault (96% leaf) | active |
| R-C4 | PoE2 | crit-weighted mean; **total+mult GAP** → partial | poe2db (15% leaf) | active |
| R-G1 | PoE1 dealt | `ArmourRed = Armour/(Armour + 10×PhysRawDmg), cap 90%` | pathofexile.com forum A1 (the loud case) | active |
| R-G2 | D2 dealt | `dmg × (1 − fire_resist_pct/100)` | standard; Act-1 0% inferred | active |
| R-G3 | GD dealt | 70% absorption / 30% always through; **rating GAP** → partial | grimdawn.com | active |
| R-G5 | ALL received | player-sheet mitigation **GAP** → PRE-MITIGATION fallback, named | charter §9 ladder | active-partial |

## 3. Derivation counts

| table | rows | derived | context-fenced | NULL-remaining |
|---|---|---|---|---|
| kit_numeric (pilot) | 444 | 405 (magnitude+tempo+formula-leaf) | 39 (R-CTX-BP 6 + R-CTX-GEO 33) | **0** |
| monster_numeric | 145 | 145 | 0 | **0** |

- **kit_numeric:** 444/444 resolved. Sum by rule = 444 (verified). The 2 pre-existing seed rows
  (`poe1-glacial-hammer`, `poe2-walking-calamity`) untouched (rdr_value NULL, rule_id NULL) — NOT part
  of the 444.
- **monster_numeric:** 145/145 derived IDENTITY (R-N1 38 + R-N2 38 + R-N3 25 + R-N4 44).

## 4. NULL-remaining breakdown by reason

**0 kit_numeric rows + 0 monster_numeric rows remain NULL.** The blocked-rule / GAP reasons do not
produce NULL LEAVES here (they are expressed in the composition ledger's gap_excluded factors), because:

- **R-K5 (gd FoI base, GAP-D1):** 0 kit_numeric rows exist for FoI base damage (FULL GAP — never
  curated). The gap lives in `kit_composition` comp_id 112 (`base_foi_damage` gap_excluded), not a leaf.
  All 26 gd kit rows that DO exist (attribute coeffs, crit table, pth leaves, absorption, tick) derive
  under R-A2/R-C2/R-G3/R-T2.
- **R-N5 (gd monster, GAP-D2):** 0 monster rows exist for gd. Nothing to block.
- **R-G4 (poe2 armour DR, GAP-B1):** a FORMULA block, not a leaf. The poe2 `poe2_armour_rating` LEAF
  rows (5) derive IDENTITY under R-N3 (the armour *number* is faithful); only the DR *formula* is
  excluded (`kit_composition` comp_id 105, `target_armour` gap_excluded). Dealt-% renders PRE-ARMOUR,
  named per charter §9.

**Semantic distinction (Discipline #12 flag):** "a value we lack" → NULL leaf (e.g. gd FoI rank rows,
which simply do not exist); "a formula we lack that would consume an existing value" → gap_excluded
composition factor + blocked formula rule (poe2 armour). The charter phrase "except
poe2-armour-dependent" refers to the latter, which is a composition exclusion, not a monster leaf NULL.
See math note §3 reconciliation.

## 5. Spot-check worked derivations (one per game)

- **D2** (Fire Ball, IDENTITY): `fireball_dmg_max_lvl20` source 258 → rdr **258** (R-K2); Fire Mastery
  `firemastery_bonus_pct_lvl20` 163 → **163** (R-M1). Composition assembles (227–258 base) ×
  (1+163/100)=×2.63. FCR unit-convert verified: 13 frames → **1.9231** casts/sec, 7 frames → **3.5714**
  (R-T1, 25/sv).
- **PoE1** (Cyclone, build-point fence): `effectiveness_pct_gem20_bp` 59 → **59** (R-K4, the 3.15 build
  point); `basedmg_pct_gem20_v327ctx` 150 → **150** but under **R-CTX-BP** (fenced CONTEXT, never the
  build point); `weapon_dps_target` 650 → **650** under **R-CTX-GEO** (weapon-dependent, per-hit
  assembly gap_excluded).
- **PoE2** (Bonestorm, two-component + pin): `bonestorm_proj_max_gem20` 175 → **175**,
  `bonestorm_expl_max_gem20` 134 → **134** (R-K3 IDENTITY); `n_shards_expected_pin` 10 → **10** (R-M3
  fixed multiplier). Per-release composition = 10 × (proj+expl).
- **GD** (FoI, character formulas curate; base blocked): `oada_formula_base_const` 115 → **115**,
  `oada_formula_level_coeff` 12 → **12**, `physique_hp_per_point` 2.5 → **2.5** (R-A2); `crit_mult_pth135`
  1.5 → **1.5** (R-C2); `armor_absorption_default_pct` 70 → **70** (R-G3). FoI base damage stays a
  composition GAP (comp_id 112), no kit_numeric leaf NULL.
- **Monster** (the loud KFL-7 leaf): `poe1-corrupted-rhoa-l68.armour` 35988 → **35988** (R-N2) — the
  anchored armour the R-G1 DR formula `Armour/(Armour+10×PhysRawDmg)` consumes; `d2-fallen` HP 1, AR 8,
  fire_resist 0 all IDENTITY (R-N1/R-N4).

## 6. Verification summary (all green)

- **Coverage:** 52/52 kit scales + 16/16 monster scales claimed by exactly one derivation rule (diff:
  zero unclaimed, zero phantom).
- **Row totals:** kit sum-by-rule = 444; monster = 145. Exact.
- **Guards (in-script):** seeds-untouched = 2 NULL; pilot NULL-remaining = 0; monster NULL-remaining =
  0; source_value spot immutable (fireball lvl20 = 258).
- **Dual-column audit vs backup:** `kit_numeric.source_value` SHA MATCH; `monster_numeric.source_value`
  SHA MATCH — source_value bit-unchanged from KF-2 entry.
- **Idempotency:** re-run of rules+derivations → derived-column SHA byte-identical (deterministic,
  rerunnable, elrond standard).
- **Composition ledger:** untouched (61 rows — outside seam scope).

## 7. GATE-2 READINESS (jack-ryan review targets)

1. **PIN-C3 conflict (already on jack-ryan's list):** R-A1 derives D2 life/mana coeffs from the
   **maxroll** anchor (`life_per_level`=1, `life_per_vit`=2). The **fextralife** alternative (+2/level,
   +3/vit) is dual-anchored on record. Rule uses maxroll leaves as-is (PIN-C3 primary). A `rule_version`
   bump to fextralife coeffs would re-derive R-A1's 20 dependents. Reviewable.
2. **Context-row disposition (seam call, override-open):** R-CTX-BP (6) + R-CTX-GEO (33) stamp rdr=sv
   with a fence-description rather than leaving NULL — because the schema's only "NULL means" states are
   not-yet-derived and blocked-GAP, and a faithfully-anchored geometry value is neither. If the reviewer
   prefers context rows stay NULL-with-context-rule_id, it is a one-line swap (set rdr NULL, retain
   rule_id). Flagged as open to override. (math note §1 CTX + §5.2)
3. **"except poe2-armour-dependent" reconciliation (Discipline #12):** confirm the poe2 armour *leaf*
   deriving IDENTITY (R-N3) while the *DR formula* stays gap_excluded (comp_id 105, R-G4 blocked)
   matches charter intent — a value-vs-formula-GAP semantic distinction, not a leaf NULL. (math note §3)
4. **IDENTITY-transform seam call (load-bearing):** RDR = source-game-own-number-carried-1:1, no
   cross-game rescale. Within-seam transform math (ADR-002 reasoning-boundary per charter §7), but its
   rationale (the gauge is only a pipeline-drift detector *because* the leaf is identity) is the run's
   whole thesis. Surfaced for the record. (math note §0)
5. **R-G5 / R-H3 / R-C3 / R-C4 / R-G3 partial renders:** these formula rules are `active` but render
   PARTIAL/PRE-MITIGATION where a build-point input is GAP (player defensive sheet, poe1 entropy
   expression, poe1/poe2 crit multiplier, gd armor rating). Each names its GAP in the rule text +
   formulas.sql header (charter §9 GAP-display law: no silent estimation). Confirm the partial-render
   contract is acceptable for KF-5 pct plumbing.
