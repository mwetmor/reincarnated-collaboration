# Vestigial-Ontology Register — Kernel Field/Value Audit

**STATUS:** v1 — kernel field/value audit complete (Matt-authorized charter 2026-06-12, Gandhi Pattern-B session)
**Author:** gandalf (Q2 semantic calls) + gamora (consuming-site verification, to be incorporated into MIGRATION.md v1.64 kernel section)
**Date:** 2026-06-12
**Charter source:** `gandalf/notes/2026-06-12-vestigial-ontology-discipline-candidate.md` § 6
**Audit scope:** `simulate_fight(...) → FightResult` declared kernel inputs — Combatant construction fields via `entity_from_class_dict` / `entity_from_monster_dict` — plus FightResult output semantics consumed downstream

---

## Register

### Field: `archetype`

| Property | Value |
|---|---|
| **Consuming sites** | `combatant.py:79` (set by adapters); exits into telemetry labels — never consumed in fight_engine or damage_resolver hot path |
| **Q1 — Does the kernel branch on it?** | NO — set at construction, never read in fight_engine or damage_resolver; exits as telemetry label freight |
| **Q2 — Physical or ontological?** | ONTOLOGICAL — "archetype" is a classification concept (role/style label), not a physical combat question |
| **Q3 — Derivable-with-default or required-native?** | DERIVABLE — adapters set it; kernel ignores it; no default needed because kernel never reads it |
| **Value domain (Q1-v/Q2-v/Q3-v)** | Value domain (e.g. "mage", "warrior") is ontological vocabulary; kernel doesn't discriminate between values; exits into telemetry as-is |
| **Disposition** | **NAME-ONLY** — ontological label carried for telemetry freight; zero behavioral impact in kernel hot path; deletable from kernel input schema with zero golden-master delta (verify via ablation against `spatial_golden_master_season_001010_2026_06_11.json` + harness) |
| **Action** | No change required. star-lord Principle-6 watch: `archetype` in FightResult telemetry output is name-only freight — carry as label, do not branch on it in any new export surface |

---

### Field: `range_profile`

| Property | Value |
|---|---|
| **Consuming sites** | `fight_engine.py:458, 459, 528, 640` (melee gating, advance-retreat, teleport-as-gap-closer); `combatant.py:354-355` (soft default `"medium"` via `getattr`) |
| **Q1 — Does the kernel branch on it?** | YES — fight_engine reads it for engagement geometry decisions |
| **Q2 — Physical or ontological?** | PHYSICAL — "what is this combatant's engagement range?" is a physical combat question any sim must ask of any combatant |
| **Q3 — Derivable-with-default or required-native?** | DERIVABLE-WITH-DEFAULT — `getattr(player_class, "range_profile", "medium")` at combatant.py:354-355; adapter absence tolerated |
| **Value domain (Q1-v/Q2-v/Q3-v)** | Q1-v: kernel reads as binary close/not-close — `"medium"` and `"long"` may be a dead in-kernel distinction (fight_engine.py:458-640 reads `== "close"` for melee gating; `"medium"` vs `"long"` produces no behavioral branch — **CONFIRM via golden-master ablation**). Q2-v: value labels are spatial-behavioral descriptions, not ontology names. Q3-v: 3-bucket enum is open at the label level (any string accepted; `getattr` default handles absence) but the kernel only discriminates binary. |
| **Disposition** | **STRUCTURAL-BENIGN** — kernel branches on it AND the question is physical AND it's derivable-with-default. The 3-bucket enum SHAPE is vestigial skin: kernel treats it as binary close/not-close; `"medium"` vs `"long"` distinction is currently a dead branch in-kernel (Q1-v pending ablation confirmation). The continuous successor signal `range_profile_redistribution` (combatant.py:129) already exists for monsters; player entity `range_profile_redistribution=None` is correct and intentional — player AI uses actual skill `range_m` values for emergent range behavior (spatial_engine.py:1094-1110, 1465). Engine is mid-molt on this exact field. |
| **Action** | No change required for Phase 3/4. Field stays as declared projection obligation. Ablation confirming `"medium"` vs `"long"` dead-branch (Q1-v) is cheap via existing golden-master harness — queue as low-priority verification. |

---

### Field: `energy_type`

| Property | Value |
|---|---|
| **Consuming sites** | `combatant.py:322-327` (`_ENERGY_CONFIGS` table); `fight_engine.py:594-597, 650-654` (skill cost deduction); `fight_engine.py:731-753` (accumulation helpers: `_accumulate_energy_on_hit`, `_accumulate_energy_on_hit_taken`, `_accumulate_energy_on_use`); `fight_engine.py:721-724` (`_tick_resources`) |
| **Q1 — Does the kernel branch on it?** | YES — fight_engine branches on energy_type to route accumulation behavior (rage/combo/focus each have distinct fill mechanics); all types write to `actor.mana` pool |
| **Q2 — Physical or ontological?** | PHYSICAL — "what is this combatant's resource model?" is a physical combat question (pool size, regen, accumulation behavior). But the IMPLEMENTATION is ontological in shape: closed enum table (`_ENERGY_CONFIGS`) means a new resource model cannot exist without a kernel table edit |
| **Q3 — Derivable-with-default or required-native?** | MIXED — physically derivable (any combatant has some resource model), but the closed `_ENERGY_CONFIGS` table makes the value set schema-hard-required: if `energy_type` not in `_ENERGY_CONFIGS`, construction fails |
| **Value domain (Q1-v/Q2-v/Q3-v)** | Q1-v: all 5 values discriminated (mana handled separately via stat derivation; rage/combo/focus/stamina-as-resource each produce distinct accumulation behavior). Q2-v: value labels (`"mana"`, `"rage"`, `"combo"`, `"focus"`, `"stamina-as-resource"`) are behavioral descriptors — physical, not ontology names. Q3-v: CLOSED — value set hard-closed by `_ENERGY_CONFIGS` table; extension requires kernel edit + kernel-change protocol § 3. **T4 STRATEGY GATE (2026-06-12):** `energy_type == "mana"` is now a gate condition for DEFENSIVE_TRADEOFF T4 strategy eligibility — adding a new resource archetype also requires updating the DEFENSIVE_TRADEOFF gate condition. Both constraints go on the kernel-change-protocol checklist for any `energy_type` addition. |
| **Disposition** | **STRUCTURAL-CONSTRAINING** — physical question (Q2 PASS) but enum-closed (Q3 FAIL on value-set openness). The closure itself is the constraint: a new emergent resource model cannot exist without a kernel table edit. The § 3 kernel-change protocol makes that edit visible and gated — which is the intended protection — but the closure goes on the register. New T4 gate coupling (2026-06-12) adds a second constraint to kernel-change checklist. |
| **Vocabulary gap (FLAGGED 2026-06-12)** | Engine vocabulary (`mana`, `rage`, `combo`, `focus`, `stamina-as-resource`) DIVERGED from `reincarnated-loadout/data/cycle13_characters.db` CHECK constraint (`cooldown`, `energy`, `mana`, `stamina`, `ki`) — Priority-01A-era stale vocabulary. Only `mana` is in common. The DB constraint is the source of `canonical/story/2026-06-06-atomic-substrate-registry.md` § 1.11 (which lists the stale values). Any loadout surface displaying `energy_type` would show wrong vocabulary. Reconciliation required before loadout consumes engine kit energy_type fields. Flagged to jack-ryan via decisions-log entry 2026-06-12. |
| **Action** | (1) Preserve as STRUCTURAL-CONSTRAINING. (2) Update kernel-change-protocol checklist: any `energy_type` addition now requires `_ENERGY_CONFIGS` table edit + DEFENSIVE_TRADEOFF gate condition update. (3) Reconcile loadout DB CHECK constraint vocabulary with engine vocabulary (rocket = authoritative; star-lord/drax export packet must use engine vocabulary per Rule 1 of vestigial-ontology discipline). |

---

## Implementation routing

| Item | Seam | Status |
|---|---|---|
| Ablation confirmation: `range_profile "medium"` vs `"long"` dead-branch (Q1-v) | gamora (golden-master harness) | LOW PRIORITY — queue |
| `archetype` NAME-ONLY confirmation via golden-master ablation | gamora (golden-master harness) | LOW PRIORITY — queue |
| `energy_type` vocabulary reconciliation (engine → loadout DB CHECK constraint) | star-lord / drax (export packet + loadout schema) | BEFORE loadout surfaces display energy_type |
| Atomic substrate registry § 1.11 update (stale vocabulary annotation) | jack-ryan or gandalf | Queue with decisions-log entry |
| Kernel-change-protocol checklist: add DEFENSIVE_TRADEOFF gate coupling to `energy_type` extension checklist | gamora (MIGRATION.md kernel section) | When MIGRATION.md v1.64 kernel section is next opened |
| Phase 3 adapter vestigial-ontology charge line (see `discipline-candidate.md` § 5) | gamora (Phase 3 implementation) | REQUIRED — in Phase 3/4 dispatch |

---

## Register home (eventual)

This register belongs in gamora's MIGRATION.md v1.64 kernel section (the declared kernel interface). gamora incorporates engine-side consuming-site rows; gandalf audits Q2 semantic calls (composes with OP § 4.4 semantic-layer rep-audit discipline). This standalone note is the Phase 3/4 dispatch reference until gamora's MIGRATION.md section is written.

**Author:** gandalf, 2026-06-12. Matt-authorized audit charter. Gamora consuming-site verification to incorporate at Phase 3.
