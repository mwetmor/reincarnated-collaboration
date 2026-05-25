# MIGRATION — Cycle 12 SC-2 substrate-subtype classification backfill (v1_scope=1 fantasy + military_modern)

**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-2) + KR-DIRECTIVE 2026-05-25 Option A scope ratification
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-12-sc-2-subtype-classification.md`
**Executor:** elrond (Phase 1 enumeration HALT + scope-clarification; Phases 2-5 resume per KR Option A)
**Date:** 2026-05-25
**Cross-seam scope:** data-only change on existing column; no schema change; no fixture-dict shape change
**ADR reference:** ADR-004 (cross-seam coordination + MIGRATION.md)

---

## Summary

Backfilled `weapon_kind_classified_subtype` on **1,021 v1_scope=1 rows** in `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries` where the column was previously NULL and `register_canonical IN ('fantasy', 'military_modern')`. Post-update, **0 v1_scope=1 NULL rows remain in scope**; all 1,054 v1_scope=1 fantasy+military_modern rows now carry a non-NULL subtype.

Phase 3 rocket consultation SKIPPED — Phase 1 spot-sample evidence (56 rows across 4 sub-populations) confirmed all v1_scope=1 items are mechanically obvious from existing 10-value canonical subtype enum; no enum extension, no fantasy-naming Pattern A-light routing needed.

**19,749 v1_scope=0 rows DEFERRED to v1.1+** per KR-DIRECTIVE Option A scope (Cycle 12 scope-doc § 0 deferred items list).

---

## Schema changes

**None.** Column `weapon_kind_classified_subtype` already existed on `weapon_knowledge_entries` per Cycle 10 Stage 0a (accessory+armor classifier, commit `6f3c288`) + Wave 5.5 Phase 0c (Tier-A coverage). This is a pure data-backfill on existing column. Existing 10-value canonical enum holds (no extension).

---

## Data changes

### Bulk default (948 rows) — handheld_weapon

Fantasy named_template + fantasy category + military_modern category items that are conventionally handheld weapons. Includes swords, axes, polearms, staves, rods, daggers, whips, flails, maces, bows, crossbows, handheld magical implements ("Censer", "Sword of X"), and the DARPA flamethrower (man-portable per modern doctrine).

### Exception 1 — ammo_consumable (13 rows)

| id | canonical_name | rationale |
|---|---|---|
| 13731 | Arcano Bomb | D&D 5e Grenade-class thrown consumable |
| 14269 | Bramble Bomb | D&D 5e Grenade-class thrown consumable |
| 16197 | Gas Grenade | D&D 5e Grenade weapon profile |
| 16390 | Gravitic Grenade | D&D 5e Grenade weapon profile |
| 17182 | Laughing Gas Bomb | D&D 5e Grenade-class thrown consumable |
| 18125 | Phosphorus Grenade | D&D 5e Grenade weapon profile |
| 19817 | Stun Grenade | D&D 5e Grenade weapon profile |
| 20076 | Thermobaric Bomb | D&D 5e Grenade-class thrown consumable |
| 20313 | Venom Bomb | D&D 5e Grenade-class thrown consumable |
| 178154 | Dreadquake Bomb | Warhammer AoS missile weapon (thrown) |
| 181148 | Cannon Ball | Warhammer standalone ammo profile (not weapon: ammo compound) |
| 179548 | Cannon Shell | Warhammer standalone ammo profile |
| 181151 | Mortar Shell | Warhammer standalone ammo profile |

Per Cycle 10 precedent: M18 smoke grenade and similar thrown ordnance classify as `ammo_consumable`.

### Exception 2 — siege_vehicle fantasy (25 rows)

Large fixed/mounted artillery in fantasy game systems. Includes Warhammer war machines (Dread Catapult variants, Sky Cannon variants, Ironblaster Cannon variants, Grundstok Mortar, Warp Lightning Cannon, Plagueclaw Catapult, Steam Cannon, etc.), standalone Ballista and Brutal Ballista, and Warhammer "Weapon: Ammo" compound names (e.g., "Great Cannon: Cannonball", "Ironblaster Cannon: Hail Shot") which are **weapon profiles of siege weapons**, NOT pure ammo. Per Cycle 10 precedent: all mounted cannons/catapults/mortars/SP-howitzers → `siege_vehicle`.

### Exception 3 — siege_vehicle military_modern (13 rows)

Modern self-propelled howitzers (PCL-181, 2S19M2, 2S22, M110A1, ATMOS 2000, 2S35-1), ATGM systems (FGM-148F Javelin), towed howitzers (PL-96), self-propelled mortars (KBA.48M), artillery rocket systems (9K52 Luna-M FROG-7), off-route mines (PARM 2), and command/reconnaissance vehicles supporting artillery (1V15). AMX-10 PAC 90 is the French amphibious tank destroyer / SP artillery piece. Per Cycle 10 military_modern precedent (extensive prior assignment of analogous artillery to `siege_vehicle`).

### Exception 4 — other (11 rows)

| id | canonical_name | rationale |
|---|---|---|
| 13513 | Abyssal Bane Knuckle Duster (rare variant) | Cycle 10 precedent: all knuckle dusters → other |
| 13514 | Abyssal Bane Knuckle Duster (very rare variant) | same |
| 13561 | Abyssal Bane Spiked Knuckle Duster (rare variant) | same |
| 14595 | Consecrated Weapon Knuckle Duster (uncommon variant) | same |
| 16832 | Hellscape Chatterbane Spiked Knuckle Duster | same |
| 18595 | Rootbound Multiweapon Knuckle Dusters | same |
| 18662 | Rootbound Multiweapon Spiked Knuckle Dusters (very rare variant) | same |
| 19441 | Spiked knuckle duster | same |
| 19641 | Starforged Weapon Knuckle Duster (legendary variant) | same |
| 13846 | Baba Yaga's Mortar and Pestle | Wondrous-item / transport, not weapon-class handheld; per Cycle 10 "wondrous item" precedent → other catch-all |
| 177340 | Crystal Healer | PF2e BACKGROUND, not a weapon — substrate pollution from `pf2ools-pf2ools-data-quarantined` source. Tagged other as catch-all; flagged for v1.1+ substrate-curation removal review (see anomalies section below) |

### Exception 5 — accessory_handheld (11 rows)

Fantasy talismans per Cycle 10 Tier-S doctrine. All 11 v1_scope=1 talisman entries (Talisman, Canvas Talisman, Thorolund Talisman, Ivory Talisman, Sunlight Talisman, Darkmoon Talisman, plus duplicates and White Hair Talisman / Sunless Talisman): all → `accessory_handheld`.

### Update arithmetic

| Update group | Row count |
|---|---|
| Exception 1 ammo_consumable | 13 |
| Exception 2 siege_vehicle (fantasy) | 25 |
| Exception 3 siege_vehicle (military_modern) | 13 |
| Exception 4 other | 11 |
| Exception 5 accessory_handheld | 11 |
| Bulk default handheld_weapon | 948 |
| **Total updated** | **1,021** |

### Idempotency

The UPDATE statements all include `weapon_kind_classified_subtype IS NULL AND v1_scope = 1 AND register_canonical IN (...)` guards. Re-running is a no-op. Pre-existing 33 already-classified rows in the v1_scope=1 fantasy+military_modern slice (979 handheld_weapon + 2 accessory_handheld pyromantic foci) were not touched.

### Final post-update distribution (v1_scope=1 fantasy + military_modern; 1,054 total non-NULL)

| weapon_kind_classified_subtype | count |
|---|---|
| handheld_weapon | 979 |
| siege_vehicle | 38 |
| accessory_handheld | 13 |
| ammo_consumable | 13 |
| other | 11 |

---

## Anomalies captured for v1.1+ queue (NOT corrected in SC-2 scope)

### Anomaly 1 — register-mistag: id=172596 "naginata"

`register_canonical='military_modern'` is incorrect; naginata is a feudal Japanese polearm and should be `historical` or `fantasy`. Subtype assignment in SC-2 is `handheld_weapon`, which is correct regardless of register. Captured for v1.1+ register-tagging cleanup. Per KR-DIRECTIVE: do NOT correct in SC-2 scope.

### Anomaly 2 — substrate pollution: id=177340 "Crystal Healer"

Source: `pf2ools-pf2ools-data-quarantined`. Description text is a Pathfinder 2e *character background* description ("Choose two attribute boosts. One must be to Wisdom or Charisma..."), not a weapon. This is a non-weapon entry that slipped into `weapon_knowledge_entries` table. Tagged `other` as a catch-all per Cycle 10 precedent. Flag for v1.1+ substrate-curation removal review (possibly extend `dedup_status='polluter_non_weapon'` or similar tag, or drop from corpus entirely). The fact that this row is `v1_scope=1` suggests v1_scope filter may not screen non-weapon substrate effectively — surface this as a v1_scope hygiene question for v1.1+.

### Anomaly 3 — possible additional substrate pollution (not enumerated)

The `pf2ools-pf2ools-data-quarantined` source label suggests further non-weapon entries may exist in the broader corpus. SC-2 scope inspected v1_scope=1 only; v1.1+ Tier-B/Tier-C cleanup should grep for additional "Crystal Healer"-pattern background/feat entries during the next substrate hygiene pass.

---

## Deferral — Tier-B + Tier-C v1_scope=0 substrate (19,749 rows)

Per Cycle 12 scope-doc § 0 deferred items list + KR-DIRECTIVE 2026-05-25:

| register | v1_scope=0 NULL-subtype count | status |
|---|---|---|
| fantasy | 16,355 | DEFERRED to v1.1+ |
| military_modern | 3,394 | DEFERRED to v1.1+ |

Per Phase 1 enumeration, this 19,749-row substrate population includes 14,144 fantasy named_template + 2,619 military_modern category + 2,345 fantasy category + 743 fantasy unknown + 670 military_modern ammo_or_consumable + 119 military_modern unknown + 65 fantasy ammo_or_consumable + 33 fantasy banner + 20 fantasy tome + 11 fantasy talisman + 1 military_modern named_template, all NULL subtype.

This v1_scope=0 substrate is out-of-scope for Cycle 12. Subtype classification on this surface is v1.1+ substrate hygiene work, not v1-unblocking work. If a future cycle expands v1_scope membership (e.g., v1.1 boss surface, v1.2 named-mythological enrichment), the v1_scope=0 rows surfacing into scope will need classification at that time. Pre-classifying the full 19,749 is wasteful if v1.1+ never reaches those rows.

---

## Downstream consumer impact

Per current `grep` across `reincarnated-engine/src/`, `reincarnated-loadout/src/`, `reincarnated-demo/`:

- **No production code consumers** of `weapon_kind_classified_subtype` as of 2026-05-25. The column is currently consumed only by documentation references in `agentic_orchestration/`.
- **Cycle 12 Layer 2/3 substrate-binding** (per framing brief § 4 PlayerClass contract substrate-binding spec) is the planned future consumer. Rocket + star-lord designing Layer 2/3 should consume the now-complete v1_scope=1 subtype population.
- **Composition policy v1** (`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 + § 3 + § 5): per-cell register-share targets will use subtype as part of Option α/β/C cell-matching tuple. Pre-SC-2, 1,021 v1_scope=1 rows defaulted to unknown-subtype in cell-tuple matching; post-SC-2, they carry their canonical subtype.
- **Cohesion-judge naming** (Phase 5; not yet implemented): can use subtype as part of per-instance vocabulary disambiguation if relevant.

Cross-seam impact is **forward-looking** (Cycle 12 Layer 2/3 will surface the change when those layers land). **No coordinated change required from other seams now.** This MIGRATION.md flags the data state for Cycle 12 Layer 2/3 implementers to design against.

---

## Reproducibility

- **Backfill SQL script:** `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/sc2_backfill.sql`
- **Backfill log JSON:** `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/sc2_backfill_log.json`
- **Dispatch + Phase 1 halt-completion record:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-12-sc-2-subtype-classification.md` (final completion record below Phase 1 halt record)

---

## Audit

**Per-item before/after sample (16 rows spanning all 5 subtype buckets + bulk default):**

| id | canonical_name | weapon_kind | register | before_subtype | after_subtype |
|---|---|---|---|---|---|
| 13513 | Abyssal Bane Knuckle Duster (rare variant) | named_template | fantasy | NULL | other |
| 13731 | Arcano Bomb | named_template | fantasy | NULL | ammo_consumable |
| 13846 | Baba Yaga's Mortar and Pestle | named_template | fantasy | NULL | other |
| 13848 | Ballista | category | fantasy | NULL | siege_vehicle |
| 16317 | Glaive | category | fantasy | NULL | handheld_weapon |
| 172596 | naginata | category | military_modern | NULL | handheld_weapon |
| 173617 | DARPA flamethrower | category | military_modern | NULL | handheld_weapon |
| 177340 | Crystal Healer | unknown | fantasy | NULL | other |
| 178154 | Dreadquake Bomb | named_template | fantasy | NULL | ammo_consumable |
| 179557 | Shortsword | category | fantasy | NULL | handheld_weapon |
| 179723 | Great Cannon: Cannonball | named_template | fantasy | NULL | siege_vehicle |
| 180076 | Sword of Teclis | category | fantasy | NULL | handheld_weapon |
| 181236 | Talisman | talisman | fantasy | NULL | accessory_handheld |
| 183144 | JPMRC VISMOD PCL-181 (SH-15) Chinese 155mm SPH | category | military_modern | NULL | siege_vehicle |
| 186697 | FGM-148F Javelin American ATGM | category | military_modern | NULL | siege_vehicle |
| 187586 | Sunless Talisman | talisman | fantasy | NULL | accessory_handheld |

**Pre-state:** 1,021 NULL rows in v1_scope=1 AND register_canonical IN ('fantasy','military_modern')
**Post-state:** 0 NULL rows in same scope; 1,054 non-NULL (1,021 newly populated + 33 pre-existing Cycle 10 coverage)
**Deferred-state:** 19,749 v1_scope=0 NULL rows untouched (DEFERRED per Option A)

---

## Discipline satisfaction

- **Discipline #1 (math-before-code):** no math; data-cleanup correctly characterized in dispatch + Phase 1 halt record + here
- **Discipline #11 (empirical inspection):** direct-inspected catalogue rows BEFORE updating across 8 distinct queries spanning total counts + per-register + per-parent × register + per-quality_tier + per-v1_scope + per-v1_scope subset + spot-checks of 56 v1_scope=1 rows + edge-case enumerations on bomb/grenade/cannon/knuckle-duster/talisman/non-weapon patterns; verified Cycle 10 precedent for 4 enum buckets before classification (bomb→ammo_consumable, knuckle-duster→other, mounted-cannon→siege_vehicle, Hand-X→handheld_weapon)
- **Discipline #25 (semantic-layer rep-audit):** confirmed `weapon_kind_classified_subtype` mechanically identifies sub-category (handheld_weapon vs siege_vehicle vs ammo_consumable vs accessory_handheld vs other); independent of `cultural_lineage_canonical` and `historical_period_canonical` semantic-overlay columns; no semantic drift introduced; existing 10-value enum coverage adequate for v1_scope=1 surface (no extension needed)
- **§ 3.1 (push back hard when warranted within data domain):** Phase 1 halted-for-scope when enumerated count diverged 200× from dispatch estimate; surfaced Options A/B/C with rationale + recommendation; KR ratified Option A
- **ADR-004 (cross-seam coordination + MIGRATION.md):** this document satisfies Phase 5 of dispatch

---

## Sign-off

**Executor:** elrond
**Completion timestamp:** 2026-05-25
**Status:** COMPLETE — all 5 phases executed per KR-DIRECTIVE Option A
**Tag:** `elrond/cycle-12-sc-2-subtype-classification-2026-05-25` (cut at Phase 4 completion per cycle-completion artifact convention)
