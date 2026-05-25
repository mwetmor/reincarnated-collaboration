# Dispatch — 2026-05-25 — elrond + rocket — Cycle 12 SC-2 weapon_kind_classified_subtype backfill (~50-100 items)

**From:** knight-rider
**To:** elrond (lead — data steward; catalogue DB) + rocket (consultant — classification judgment for ambiguous items)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — Q5 sidecars SC-1 + SC-2; KR autonomously orchestrates Cycle 12 sidecars per scope-doc § 1)
**Estimated effort:** ~1-2 hours combined (~30-60 min elrond enumeration + bulk classification + ~30-60 min rocket consultation on ambiguous items + ~30 min finalization)
**Acceptance:** Backfill `weapon_kind_classified_subtype` field for ~50-100 currently-unset items in catalogue DB (fantasy + military_modern subset); per-item before/after audit; MIGRATION.md if cross-seam impact; rocket consults on ambiguous-classification items

---

## Context

Cycle 12 framing brief § 2 SC-2 surfaces a substrate-curation cleanup: ~50-100 items in the catalogue DB currently have `weapon_kind_classified_subtype` field unset, predominantly in the fantasy + military_modern subset. This field provides finer-grained classification beyond the parent `weapon_kind` (e.g., parent: `polearm`; subtype: `glaive` vs `naginata` vs `halberd` — capturing per-product-line register variation per Discipline #25 + composition policy v1).

Per framing brief § 2 SC-2, this sidecar is co-owned: elrond leads the DB enumeration + backfill execution; rocket consults on ambiguous-classification items (rocket has engine-canonical-library knowledge useful for classification judgment on fantasy items per Pattern A-light routing).

Cycle 12 fires in parallel with Cycle 11 close. SC-2 fires as a sidecar at any time during Cycle 12 Day 1 per scope-doc § 1; no specialist contention.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 2 SC-2 (scope statement) + § L9 (substrate split — weapon_kind_classified_subtype is mechanical-layer per L9, NOT semantic-overlay; subtype identifies mechanical sub-category)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 (per-register coverage targets) + § 3 (Option α/β/C cell-matching — subtype affects cell-tuple matching) + § 5 (per-cell coverage)
- Cycle 10 Stage 0a accessory+armor classifier precedent (elrond): `dispatches/2026-05-24-elrond-cycle-10-stage-0a-accessory-armor-classifier.md` or commit `6f3c288` (pattern: enumerate untagged + classify into subtype enum)
- Cycle 10 Stage 4 mechanical-tagging dispatch (rocket): `dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md` (rocket's subtype-classification authority context)
- v1_scope substrate state: 3,042 rows curated (per Cycle 10 wind-down); subset has `weapon_kind_classified_subtype` unset
- elrond seam state: `agentic_orchestration/elrond/` notes + recent commits
- rocket seam state: `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (engine-canonical-library subtype knowledge)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 empirical inspection + #25 semantic-layer rep-audit + ADR-004 MIGRATION.md cross-seam

---

## Math-before-code (per Discipline #1)

No math. Database enumeration + backfill operation; no new computation.

Pre-fire: elrond should query the catalogue DB to enumerate items currently with `weapon_kind_classified_subtype IS NULL` AND filtered to fantasy + military_modern register-subset (per framing brief § 2 SC-2 scope). Report scope finding back to KR in completion record: how many items found; per-parent-weapon-kind breakdown; per-register breakdown.

---

## Scope (elrond + rocket co-execution)

### Phase 1 — elrond enumeration (lead)

- Query catalogue DB for items with `weapon_kind_classified_subtype IS NULL` AND register in (`fantasy`, `military_modern`) per framing brief § 2 SC-2
- Report: total count; per-parent-weapon-kind count; per-register count
- Per-row metadata snapshot: weapon name + parent weapon_kind + register + cultural_tradition + period (for rocket consultation context)
- If count > 100, flag to KR — surface whether SC-2 scope expansion is in-scope per scope-doc § 1 (KR judgment; likely yes if cheap; escalate if >>100)
- If count <50, proceed with the smaller set; no scope adjustment needed

### Phase 2 — elrond classifies obvious items (lead)

- For items where subtype classification is obvious from name + parent weapon_kind + cultural_tradition (e.g., parent=polearm + cultural=feudal_japanese + name="naginata" → subtype="naginata"; parent=sword + cultural=european_medieval + name="longsword" → subtype="longsword"), elrond classifies directly per existing canonical subtype enum
- For ambiguous items (e.g., fantasy-original weapon with no clear historical precedent; military_modern items where parent could subdivide multiple ways), DEFER to rocket consultation per Phase 3
- Per-classified-item: rationale captured (e.g., "naginata: feudal_japanese polearm per cultural_tradition + canonical subtype enum")

### Phase 3 — rocket consultation on ambiguous items (consultant; sub-agent invocation by KR if needed)

- KR invokes rocket sub-agent (Agent tool) with the ambiguous-item list from elrond Phase 2
- Rocket consults engine-canonical-library + Cycle 10 Stage 4 mechanical-tagging context to recommend subtype classifications for ambiguous items
- For fantasy items with no historical precedent, rocket may invent a subtype (per existing fantasy subtype enum if available) OR flag for gandalf Pattern A-light if subtype-naming-design is genuinely a design question
- Rocket returns per-item classification recommendation + rationale
- Elrond consumes rocket's recommendation + applies backfill

### Phase 4 — elrond bulk backfill + audit (lead)

- Apply backfill SQL to all classified items (Phase 2 + Phase 3 combined)
- Post-update audit: confirm all enumerated items now have non-NULL `weapon_kind_classified_subtype`
- Per-item before/after sample in completion record (at least 10 items, covering both elrond Phase 2 + rocket Phase 3 classifications)

### Phase 5 — MIGRATION.md if cross-seam impact

- Per Discipline ADR-004 — if other seams consume `weapon_kind_classified_subtype` (likely: Architecture B Phase 2 substrate-binding uses subtype for cell-match; composition policy uses subtype for register-share; cohesion-judge uses for naming), MIGRATION.md authored
- MIGRATION.md flags the data change for downstream awareness

---

## Out of scope

- Backfill of register subsets outside fantasy + military_modern (per framing brief § 2 SC-2; defer historical / mythological to existing tags or v1.1+)
- Subtype enum schema extension (use existing canonical enum; if extension needed, route to gandalf via KR — likely escape-hatch)
- Cross-seam consumer code changes (other seams may consume the backfilled values, but elrond + rocket do not change their code)
- New items addition (this is cleanup of existing entries)
- SC-1 substrate-tagging cleanup (separate dispatch — fires in parallel)
- SC-3 off-hand mechanical contract design (absorbed into Layer 3 rocket dispatch per framing brief § 2)

---

## Acceptance criteria

- [ ] Phase 1 enumeration query authored + run; total count + per-parent-weapon-kind breakdown + per-register breakdown captured
- [ ] Phase 2 elrond direct classifications applied; per-classified-item rationale captured
- [ ] Phase 3 rocket consultation completed (if ambiguous items surfaced); rocket recommendations applied
- [ ] Phase 4 backfill audit: all enumerated items now have non-NULL `weapon_kind_classified_subtype`
- [ ] Per-item before/after sample in completion record (≥10 items)
- [ ] MIGRATION.md authored if cross-seam consumer impact per ADR-004
- [ ] Per Discipline #11 empirical inspection: direct-inspected catalogue DB rows BEFORE updating
- [ ] Per Discipline #25 semantic-layer rep-audit: confirm `weapon_kind_classified_subtype` correctly classifies mechanical sub-category, not semantic overlay
- [ ] Auto-commit + auto-push per elrond seam authorization (CLAUDE.md addendum)
- [ ] Tag: `elrond/cycle-12-sc-2-subtype-classification-2026-05-25`

---

## Open questions for the agent to resolve

- Exact enumerated count + scope adjustment (if count >>100, escalate to KR for scope decision; if count <50, proceed with smaller set)
- Whether rocket consultation needs to fire (depends on Phase 2 ambiguous-item count; if elrond classifies all directly, Phase 3 skips)
- Exact subtype enum values per parent weapon_kind — elrond reads existing canonical enum from catalogue schema OR rocket engine canonical library; if enum coverage incomplete, route to gandalf Pattern A-light for subtype-naming-design judgment
- Whether MIGRATION.md is needed (depends on which seams actually consume this field; elrond checks via grep)
- Whether gandalf Pattern A-light routing surfaces for items where subtype-naming-design is genuinely a design question (e.g., fantasy items with no historical precedent; KR routes via parallel sub-agent if rocket flags)

---

## Cross-seam impact

Round-trip: not applicable — substrate-classification backfill is a data update on existing column; no schema change; no fixture-dict shape change. Other seams (Architecture B Phase 2 substrate-binding; composition policy register-share targets; cohesion-judge naming) consume these values but their consumer code is unaffected (same column reads; new values). MIGRATION.md authored to flag the data change.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 2 SC-2 + § L9
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 + § 3 + § 5
- Cycle 10 Stage 0a accessory+armor classifier (elrond precedent): commit `6f3c288`
- Cycle 10 Stage 4 mechanical-tagging dispatch (rocket precedent): `dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 + #25 + ADR-004

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-2 fires); KR autonomously orchestrates per scope-doc § 1; co-execution per framing brief § 2 SC-2 owner declaration
**Status:** FIRE — Day-1 sidecar; fires in parallel with legolas MC-1+MC-2 + jack-ryan Gate-1 + elrond SC-1 + Cycle 11 close drax Wave 3b

**Matt-touch sequence:** elrond + rocket complete → KR captures completion in state file → if subtype-enum-extension OR fantasy-naming-design surfaces emerge, KR routes Pattern A-light to gandalf; otherwise auto-close

---

## KR-DIRECTIVE — 2026-05-25 — Option A scope approved per Phase 1 halt-point

**Context:** Elrond Phase 1 enumeration returned 20,770 rows vs dispatch estimate ~50-100 — 200× scope mismatch. Per dispatch own ">>100 → flag to KR for scope decision" gate, elrond correctly HALTED at Phase 1 + surfaced three scope options (A v1_scope=1 only = 1,021 rows; B fantasy bulk = 17,361; C full = 20,770) with Option A recommendation per seam-owner judgment. Halt commit: `dac63fb`.

**KR decision (autonomous in-scope per scope-doc § 1 + § 6):** **Option A** — v1_scope=1 only, 1,021 rows.

**Rationale:**
- Option A is closest to dispatch + framing brief § 2 SC-2 intent. The "~50-100" estimate was an undercount of the v1_scope=1 surface; Option A targets exactly the substrate Cycle 12 Layer 2/3 will consume per framing brief § 4 PlayerClass contract substrate-binding spec.
- Options B + C (Tier-B + Tier-C v1_scope=0 substrate) are v1.1+ substrate hygiene work — explicitly OUT of Cycle 12 scope per scope-doc § 0 deferred items list.
- Elrond Phase 1 spot-sample evidence (56 rows; Discipline #11) confirms v1_scope=1 path is mechanically obvious from existing 10-value subtype enum — no enum extension, no rocket consultation, no fantasy-naming Pattern A-light needed.
- Hive-mind decision-routing § 4.3: seam-owner (elrond) recommended; KR concurs; Matt-escalation reserved for last-resort (CLAUDE.md no-over-asking addendum).
- This is NOT scope amendment escalation per scope-doc § 5 — it's dispatch-estimate clarification + seam-owner recommendation concurrence within original intent.

**Elrond directive (Phases 2-5 against Option A scope):**
- Phase 2: classify 1,021 v1_scope=1 items directly using existing canonical subtype enum (Phase 1 spot-sample confirmed all 56 sampled are mechanically obvious; no enum extension)
- Phase 3: rocket consultation likely SKIPS per Phase 1 spot-sample evidence (no ambiguous items in v1_scope=1 surface). If any ambiguous item surfaces in the remaining 965 unsampled rows, elrond flags to KR rather than fires rocket sub-agent autonomously
- Phase 4: bulk backfill + post-update audit per dispatch acceptance criteria
- Phase 5: MIGRATION.md if cross-seam consumer impact per ADR-004
- Estimated continuation effort: ~30 min per elrond Phase 1 projection
- Separate register-mistag anomaly (id=172596 "naginata" tagged military_modern) surfaced in Phase 1 is OUT of SC-2 scope; capture in completion record for v1.1+ queue, do NOT correct here
- Tier-B + Tier-C v1_scope=0 substrate (the other 19,749 rows) DEFERRED to v1.1+ per scope-doc § 0; capture deferral in completion record

**Status:** RESUME — Phases 2-5 against Option A scope authorized.

**Authority:** knight-rider 2026-05-25 (autonomous in-scope decision per Cycle 12 scope-doc § 1 + § 6 + hive-mind decision-routing § 4.3 seam-owner concurrence)

---

## Completion record — Phases 2-5 COMPLETE per KR-DIRECTIVE Option A (elrond 2026-05-25)

**Status:** SC-2 COMPLETE. All 5 phases executed against Option A scope (v1_scope=1 only, 1,021 rows). Phases 2-5 resumed after KR Option A ratification per directive at file bottom. Phase 1 halt-completion record preserved below for full audit trail.

### Execution summary

| Phase | Status | Notes |
|---|---|---|
| Phase 1 — enumeration | COMPLETE (prior halt; see record below) | 1,021 v1_scope=1 NULL rows enumerated; per-parent + per-register + per-quality_tier breakdowns captured; 56 rows spot-sampled |
| Phase 2 — elrond direct classification | COMPLETE | All 1,021 v1_scope=1 items classified directly via existing 10-value canonical subtype enum; no enum extension needed |
| Phase 3 — rocket consultation | SKIPPED | Phase 1 + Phase 2 edge-case sweeps confirmed all v1_scope=1 items are mechanically obvious; no ambiguous items required rocket consultation per KR-DIRECTIVE |
| Phase 4 — bulk backfill + post-update audit | COMPLETE | Single-transaction backfill in `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`; 1,021 rows updated; 0 NULL remaining in scope; 16-row before/after audit captured |
| Phase 5 — MIGRATION.md | COMPLETE | `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/MIGRATION.md` authored |

### Classification distribution

| subtype | rows updated this run | distribution rationale |
|---|---|---|
| handheld_weapon | 948 | Bulk default — fantasy named_template + fantasy category + military_modern category for handheld weapons (swords, axes, polearms, staves, rods, daggers, whips, flails, maces, bows, crossbows, handheld magical implements, DARPA flamethrower) |
| siege_vehicle | 38 | 25 fantasy mounted artillery (Warhammer war machines + standalone Ballista/Brutal Ballista + Warhammer "Weapon: Ammo" compound profiles) + 13 modern self-propelled howitzers / ATGMs / mortars / off-route mines |
| ammo_consumable | 13 | 10 D&D 5e Grenade-class thrown consumables + 3 Warhammer standalone ammo profiles (Cannon Ball / Cannon Shell / Mortar Shell) |
| other | 11 | 9 knuckle dusters + Baba Yaga's Mortar and Pestle (wondrous-item transport) + Crystal Healer (PF2e BACKGROUND substrate-pollution) per Cycle 10 catch-all precedent |
| accessory_handheld | 11 | Fantasy talismans per Cycle 10 Tier-S doctrine |
| **Total updated** | **1,021** | |

### Anomalies captured for v1.1+ queue (NOT corrected in SC-2 scope per KR-DIRECTIVE)

1. **id=172596 "naginata"** — `register_canonical='military_modern'` is incorrect (naginata is feudal Japanese polearm; should be `historical` or `fantasy`). Subtype assignment `handheld_weapon` is correct regardless. Queue for v1.1+ register-tagging cleanup.
2. **id=177340 "Crystal Healer"** — substrate pollution from `pf2ools-pf2ools-data-quarantined` source. Description is a PF2e *character background*, not a weapon. Tagged `other` as catch-all; flag for v1.1+ substrate-curation removal review. Note: v1_scope filter did not screen this non-weapon entry — surface as v1_scope hygiene question.
3. **Possible additional pf2ools-quarantined background/feat pollution** — the `pf2ools-pf2ools-data-quarantined` source suggests further non-weapon entries may exist in broader corpus. v1.1+ Tier-B/Tier-C cleanup should grep for analogous patterns.

### Deferred substrate per Option A scope (per KR-DIRECTIVE)

| register | v1_scope=0 NULL count | status |
|---|---|---|
| fantasy | 16,355 | DEFERRED to v1.1+ |
| military_modern | 3,394 | DEFERRED to v1.1+ |
| **Total deferred** | **19,749** | per Cycle 12 scope-doc § 0 deferred items list |

### Concurrency note

Throughout Phase 4 backfill (single-transaction UPDATE), `PRAGMA busy_timeout=30000` applied. **No SQLite lock-busy contention observed.** SC-1 in flight at separate elrond sub-agent instance touches different columns (`cultural_lineage_canonical` + `historical_period_canonical` on Tier-S named-mythological subset); no row-level contention with SC-2's `weapon_kind_classified_subtype` column writes.

### Cross-seam impact assessment

**Grep results:** no production code consumers of `weapon_kind_classified_subtype` in `reincarnated-engine/src/`, `reincarnated-loadout/src/`, `reincarnated-demo/` as of 2026-05-25. Column is consumed only by documentation references in `agentic_orchestration/`. Forward-looking consumers per framing brief § 4: Cycle 12 Layer 2/3 substrate-binding (planned, not yet implemented) + composition policy v1 per-cell register-share (already authored against subtype column shape).

**MIGRATION.md scope:** authored as forward-flag for Cycle 12 Layer 2/3 implementers (rocket + star-lord) to design substrate-binding against the now-complete v1_scope=1 subtype population. No coordinated change required from other seams now.

### Discipline satisfaction

- **#1 math-before-code:** no math; data-cleanup correctly characterized
- **#11 empirical inspection:** direct-inspected catalogue rows BEFORE updating across 8+ queries spanning totals, per-register, per-parent × register, per-quality_tier, per-v1_scope, per-v1_scope subset, 56-row spot-checks, and edge-case enumerations on bomb/grenade/cannon/knuckle-duster/talisman/non-weapon patterns. Verified Cycle 10 precedent for 4 enum buckets before classification (bomb→ammo_consumable, knuckle-duster→other, mounted-cannon→siege_vehicle, Hand-X→handheld_weapon).
- **#25 semantic-layer rep-audit:** confirmed `weapon_kind_classified_subtype` mechanically identifies sub-category (handheld_weapon vs siege_vehicle vs ammo_consumable vs accessory_handheld vs other); independent of `cultural_lineage_canonical` and `historical_period_canonical` semantic-overlay columns; no semantic drift introduced; existing 10-value enum coverage adequate for v1_scope=1 surface (no extension needed).
- **§ 3.1 push back within data domain:** Phase 1 halted-for-scope when enumerated count diverged 200× from dispatch estimate; Phase 2 sub-population edge-case sweep (bombs/grenades/cannons/knuckle-dusters/talismans/non-weapons) prevented bulk-default over-application that would have mis-classified ~73 rows.
- **ADR-004 cross-seam:** MIGRATION.md authored at `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/MIGRATION.md` per Phase 5.

### Reproducibility artifacts

- Backfill SQL: `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/sc2_backfill.sql` (single-transaction; idempotent; all UPDATEs guarded by `weapon_kind_classified_subtype IS NULL AND v1_scope = 1 AND register_canonical IN (...)`)
- Backfill log JSON: `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/sc2_backfill_log.json` (run metadata + per-bucket counts + anomalies + discipline satisfaction)
- MIGRATION: `agentic_orchestration/elrond/research/cycle-12-sc-2-2026-05-25/MIGRATION.md`

### Acceptance criteria — all met

- [x] Phase 1 enumeration query authored + run; total count + per-parent-weapon-kind breakdown + per-register breakdown captured (see Phase 1 halt record below)
- [x] Phase 2 elrond direct classifications applied; per-classified-item rationale captured (in MIGRATION.md per-exception tables)
- [x] Phase 3 rocket consultation — SKIPPED per KR-DIRECTIVE (no ambiguous items in v1_scope=1 surface)
- [x] Phase 4 backfill audit: all 1,021 enumerated v1_scope=1 items now have non-NULL `weapon_kind_classified_subtype`; 0 NULL remaining in scope
- [x] Per-item before/after sample in completion record (16 rows in MIGRATION.md audit section)
- [x] MIGRATION.md authored — cross-seam consumer impact captured as forward-flag for Cycle 12 Layer 2/3
- [x] Discipline #11 empirical inspection: direct-inspected catalogue DB rows BEFORE updating + edge-case enumeration sweeps
- [x] Discipline #25 semantic-layer rep-audit: confirmed `weapon_kind_classified_subtype` correctly classifies mechanical sub-category, not semantic overlay
- [x] Tag: `elrond/cycle-12-sc-2-subtype-classification-2026-05-25` (cut at Phase 4 completion per cycle-completion artifact convention; auto-commit + auto-push per elrond seam authorization per CLAUDE.md addendum)

---

## Completion record — Phase 1 enumeration HALT-FOR-SCOPE (elrond 2026-05-25)

**Status:** Phase 1 enumeration COMPLETE. Execution HALTED before Phase 2 per dispatch directive ("If your enumerated count is >>100, flag to KR for scope decision before backfilling"). Enumerated count is **20,770 — ~200× the dispatch estimate of 50-100.** Returning to knight-rider for scope decision before proceeding.

### Database / location

- **DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (the substrate DB — `weapon_knowledge_entries` table is here, not in `agentic_orchestration/research/curated/catalogue.db`; the dispatch's "catalogue DB" framing is consistent with hive-mind P-phase nomenclature)
- **Table:** `weapon_knowledge_entries`
- **PRAGMA busy_timeout = 30000ms** applied per concurrency-mitigation guidance (SC-1 running in parallel against `cultural_lineage_canonical` + `historical_period_canonical` on a different row subset)

### Phase 1 enumeration — Discipline #11 empirical inspection of catalogue rows BEFORE any update

**Total `weapon_kind_classified_subtype IS NULL AND register_canonical IN ('fantasy','military_modern')`:** 20,770 rows

#### Per-register breakdown

| register_canonical | NULL-subtype count |
|---|---|
| fantasy | 17,361 |
| military_modern | 3,409 |

#### Per-parent `weapon_kind` × register breakdown

| weapon_kind | register | count |
|---|---|---|
| named_template | fantasy | 14,144 |
| category | military_modern | 2,619 |
| category | fantasy | 2,345 |
| unknown | fantasy | 743 |
| ammo_or_consumable | military_modern | 670 |
| unknown | military_modern | 119 |
| ammo_or_consumable | fantasy | 65 |
| banner | fantasy | 33 |
| tome | fantasy | 20 |
| talisman | fantasy | 11 |
| named_template | military_modern | 1 |

#### Per-`quality_tier` breakdown

| quality_tier | register | count |
|---|---|---|
| B | fantasy | 8,755 |
| C | fantasy | 8,586 |
| C | military_modern | 1,776 |
| B | military_modern | 1,633 |
| NULL_tier | fantasy | 20 |

(Confirms: 0 rows are Tier-S or Tier-A in this NULL-subtype population — Cycle 10 Stage 0a's Tier-S Phase 0a coverage and Wave 5.5 Phase 0c Tier-A coverage are complete. All 20,770 NULL rows are Tier-B + Tier-C + a tiny NULL-tier residual.)

#### `v1_scope` partition (CRITICAL)

| v1_scope | register | count |
|---|---|---|
| 0 (out-of-scope) | fantasy | 16,355 |
| 0 (out-of-scope) | military_modern | 3,394 |
| 1 (IN v1 scope) | fantasy | 1,006 |
| 1 (IN v1 scope) | military_modern | 15 |

**Only 1,021 of the 20,770 NULL-subtype rows are in v1_scope. The remaining 19,749 are v1_scope=0 — out-of-scope substrate.**

#### Per-parent × register breakdown for **v1_scope=1 only** (the consequential subset)

| weapon_kind | register | v1_scope=1 count |
|---|---|---|
| named_template | fantasy | 917 |
| category | fantasy | 77 |
| category | military_modern | 15 |
| talisman | fantasy | 11 |
| unknown | fantasy | 1 |

#### Existing `weapon_kind_classified_subtype` enum coverage (post Cycle 10 Stage 0a + Wave 5.5)

| subtype value | populated rows |
|---|---|
| handheld_weapon | 3,571 |
| siege_vehicle | 2,402 |
| armor_body_or_head | 818 |
| ammo_consumable | 766 |
| other | 548 |
| accessory_weapon_integrated | 405 |
| accessory_horse_or_equipment | 225 |
| art_object | 207 |
| armor_shield | 138 |
| accessory_handheld | 32 |

10 enum values present; no fantasy-specific subtype values (no need for enum extension for fantasy items — all are handheld_weapon or talisman/banner/tome which match the existing accessory subdivisions).

### Spot-sample rows (Discipline #11)

**v1_scope=1 fantasy named_template (sample 20 of 917):** "Vyrkos Barrow-blade", "Cursed Broadsword", "Femur-Shafted Mace", "Rod of the Ogre Magi", "Goat's Horn", "Mace of Tiamat - Common", "Massive Club", "Nadirite Spear", "Incantor's Staff", "Ranger Axe", "Ritual Dagger", "Hand Ballista", "Rod of Dire Shadows", "Marauder Javelin (Missile)", "Assassin's Throwing Axe", "Velvet Sword of St Trina", "Hellscape Chatterbane Quarterstaff (rare variant)", "Pokin' Lance", "Gargantuan Club", "Corpse Slayer Javelin". **All 20 are unambiguously `handheld_weapon`.**

**v1_scope=1 fantasy category (sample 10 of 77):** "Sword of Light", "Greatsword of The Forlorn", "Staff of Enlightenment", "Greataxe", "Sword of Teclis", "Flail", "dagger", "Whip", "Mace of Disruption", "Javelin +3". **All 10 are unambiguously `handheld_weapon`.**

**v1_scope=1 military_modern (all 15):** 14 are `siege_vehicle` (155mm self-propelled howitzers, FROG-7 artillery rocket system, FGM-148F Javelin ATGM, PARM 2 off-route mine, etc.) and 1 anomaly: id=172596 "naginata" mis-tagged as `register_canonical='military_modern'` (should be `fantasy` or `historical`; flagging for separate substrate-curation cleanup, not subtype-classification). DARPA flamethrower (id=173617) is `handheld_weapon` (per recent doctrine; man-portable). PCL-181 / 2S19M2 / AMX-10 PAC 90 / 1V15 / KBA.48M / 2S22 / M110A1 / ATMOS 2000 / 9K52 Luna-M / PL-96 / FGM-148F / PARM 2 / 2S35-1 are all `siege_vehicle`.

**v1_scope=1 fantasy talisman (all 11):** "Talisman", "Canvas Talisman", "Thorolund Talisman", "Ivory Talisman", "Sunlight Talisman", "Darkmoon Talisman", "Talisman" (dup), "Sunlight Talisman" (dup), "Canvas Talisman" (dup), "White Hair Talisman", "Sunless Talisman". **All 11 are `accessory_handheld` per existing enum convention (Cycle 10 doctrine: Tier-S talismans → `accessory_handheld`).**

### Decisions surfaced for KR

The enumerated count (20,770) is so far from the dispatch estimate (50-100; ~200× over) that proceeding without scope re-confirmation would violate the dispatch's explicit halt directive. Three plausible scopes for SC-2:

**Option A — v1_scope=1 only (RECOMMENDED).** Backfill the 1,021 in-scope rows. All are mechanically obvious from sample inspection (917 named_template + 77 category + 15 military_modern + 11 talisman + 1 unknown). Bulk-classifiable in a single pass: fantasy named_template + fantasy category → `handheld_weapon`; military_modern category (mostly artillery) → `siege_vehicle` mostly; talisman → `accessory_handheld`. Effort: ~30 minutes elrond, no rocket consultation needed (no ambiguous items in the v1_scope=1 sample). 1 anomaly surfaces for separate cleanup (id=172596 naginata register mis-tag).

**Option B — v1_scope=0/1 fantasy bulk (Tier-B/C named_templates + categories).** Backfill all 17,361 fantasy NULL rows. Substrate-cleanup hygiene wider than v1 needs; useful for v1.1+ substrate re-cuts where v1_scope membership may shift. All bulk-classifiable as `handheld_weapon` for named_template + category (per sample). Effort: ~1-2 hours elrond, no rocket consultation; SQL is the work. Note: this exceeds the dispatch's "fantasy + military_modern subset" framing in volume — Matt may not have anticipated this scale.

**Option C — Full enumerated 20,770.** Includes 3,409 military_modern items (mostly siege_vehicle artillery + 670 ammo_or_consumable). The 670 ammo_or_consumable parent already telegraphs `ammo_consumable` subtype obvious-mapping; the 2,619 military_modern category and 119 military_modern unknown rows would need sample inspection but are likely siege_vehicle / handheld_weapon dominant. Effort: ~2-3 hours elrond. Genuinely cleans the entire NULL-subtype population for these two registers.

**Defer-and-narrow.** Cycle 10 wave 5.5 dispatch (Phase 0c) explicitly scoped 940 Tier-A NULL-subtype rows. Phase 0a + Wave 5.5 covered Tier-S + Tier-A. **Tier-B + Tier-C never had a classification pass.** The "~50-100 items" estimate likely reflects an assumption that Cycle 10 covered everything, or an estimate of v1_scope=1 NULL items specifically. If the latter, 1,021 v1_scope=1 is the right cardinality bucket — still 10× the estimate but recoverable via Option A.

### Recommended scope decision (elrond seam-owner judgment per § 3.1 push-back)

**Option A (v1_scope=1 only; 1,021 items).** Reasoning:
1. Aligns with Cycle 12 framing brief § 2 SC-2 intent (substrate cleanup unblocking Cycle 12 v1 layers; v1_scope=1 IS the v1 scope)
2. Closest-fit cardinality to dispatch estimate (1,021 vs 50-100; still ~10× over but within scope-doc § 1 KR autonomous orchestration tolerance)
3. All v1_scope=1 NULL items are mechanically obvious from sample (no rocket consultation needed; no enum extension needed; no gandalf Pattern A-light needed)
4. Tier-B + Tier-C v1_scope=0 substrate cleanup is a v1.1+ hygiene task, not Cycle 12 v1-unblocking work
5. Discipline #25 satisfied: subtype identifies mechanical sub-category (handheld_weapon = mechanical), not semantic overlay; sample inspection confirms

### Concurrency note

SC-1 is firing in parallel against `cultural_lineage_canonical` + `historical_period_canonical` on Tier-S named-mythological rows (different subset). PRAGMA busy_timeout = 30000ms applied. No SQLite lock-busy contention observed during Phase 1 read-only enumeration. If Phase 4 bulk UPDATE is authorized, will re-apply busy_timeout + retry-with-backoff at the UPDATE step.

### Disciplines satisfied at halt-point

- **#11 (empirical inspection):** direct-inspected catalogue rows via 7 distinct queries (totals + per-register + per-parent × register + per-quality_tier + per-v1_scope + per-v1_scope subset + sample row spot-checks of 56 rows across 4 sub-populations) BEFORE any update fires
- **#25 (semantic-layer rep-audit):** confirmed `weapon_kind_classified_subtype` mechanically identifies sub-category (handheld_weapon vs siege_vehicle vs accessory_handheld) per existing 10-value enum; sample-row spot-check confirms no semantic-overlay drift (cultural_lineage / period are separate columns; subtype is mechanical only)
- **#1 (math-before-code):** no math; data-cleanup operation correctly characterized
- **§ 3.1 (push back hard when warranted within data domain):** halting at Phase 1 per dispatch's own >>100 escalation gate; not silently expanding scope by 200×
- **§ 3.5 (Discipline #11 every Phase D step):** non-negotiable for go/no-go; halt is the right call

### Awaiting KR scope decision

Phases 2-5 unfired. Will resume on KR/Matt scope ratification (Option A vs B vs C vs defer). Estimated resumption effort:
- Option A: ~30 min execution + audit (no rocket consultation; no MIGRATION.md cross-seam cost beyond existing composition policy)
- Option B: ~1-2 hr execution + audit (no rocket consultation expected)
- Option C: ~2-3 hr execution + audit (light rocket consultation for any ambiguous military_modern category items at sample inspection)

No commit fired (no UPDATE landed; Phase 1 read-only enumeration only). No tag cut. Scope-decision halt is the work-product.

**Elrond seam-owner recommendation:** Option A. KR/Matt to ratify.
