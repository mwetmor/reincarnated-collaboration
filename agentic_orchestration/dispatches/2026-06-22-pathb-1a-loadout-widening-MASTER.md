# Dispatch MASTER — 2026-06-22 — Path B Step 1a — sim Loadout widening 4→10

**From:** knight-rider
**To:** rocket (foundational) → gamora + star-lord (consumers) → drax (presentation)
**Approved by:** Matt 2026-06-22 ("GO on 1a author+fire")
**Estimated effort:** multi-day, 4 seams, sequenced
**Gate:** jack-ryan Gate-1 on this MASTER before any seam fires; jack-ryan Gate-2 per seam. MIGRATION.md per ADR-004.

## Context

Path B (cap-everything-but-costly resist) is the resist design-of-record (gandalf spec `2026-06-22-path-b-resist-design-spec.md`; jack-ryan Gate-1 ENDORSE-WITH-CONCERNS, CONCERN-1 closed + ratified, Gate-1 fully PASSES). Per spec §15, **Step 1a — widening the equipped sim Loadout from 4 slots to 10 (9 resist-capable) — is the FOUNDATIONAL first build piece and it GATES 1b (breadth-affix taxonomy) and 1c (budget recalibration).**

The spec's §3.1 claim is jack-ryan-verified first-hand: the live sim sums only a **4-slot** `Loadout` (`gear_schema.py:198-228` — weapon/off_hand/armor/accessory; 3 resist-capable), while a 10-slot generation-side slot model exists separately. 1a **bridges** the existing 10-slot generation representation into the equipped Loadout the sim runs. The authoritative slot inventory (gandalf reconciliation, commit `d538865`) is **`gear_slot_labels` (`class_schema.py:131-142`): 10 equipped slots = 1 weapon (`main_hand`, no resist) + 9 resist-capable.**

**This is a structural widening ONLY.** No affix mint changes (that's 1b), no budget/range calibration (that's 1c). The existing single-element resist mint and existing budget flow through unchanged. Balance is NOT representative until 1c — see Out-of-scope.

## The 10 canonical equipped slots (authoritative — `gear_slot_labels`)

`main_hand` (weapon, **no resist**), `off_hand`, `head`, `chest`, `hands`, `feet`, `belt`, `ring_1`, `ring_2`, `amulet` → **9 resist-capable** (everything except `main_hand`).

**Name-reconciliation the rocket bridge owns (jack-ryan Gate-1 carry-items):**
- The generation `GearSlot` enum (`partition_schema.py:53-64`) is **11 members**, includes a **`LEGS`** slot the equipped 10-model omits, and names the off-hand `SECONDARY_ITEM`. **`LEGS` folds into `CHEST`** on the bridge (gandalf ruling — keeps resist-capable count at exactly 9; an 11th resist-capable slot would be the §9 free-baseline tax). **`SECONDARY_ITEM`→`off_hand`**, **`MAIN_WEAPON`/`main_weapon`→`main_hand`** normalized in the same one place (jack-ryan INFO). All enum→equipped naming reconciliation happens in ONE bridge function so it is auditable.

## Why the +9 count is load-bearing (do not alter without re-deriving the spec)

Spec §4 property-2 / Rule-2: 9 resist-capable slots × resist-all `+9` ceiling = `+81` → just-caps all 7 elements. If the resist-capable count drifts to 10, capping gets free → reopens the §9 tax. **1a must land exactly 9 resist-capable slots.** This is a Gate-2 check.

## Seam sequence + ownership

| Order | Seam | Work | Gates |
|---|---|---|---|
| **1 (foundational)** | **rocket** | `Loadout` schema 4→10; `_slots()`; `combined_stats()`, `combined_ability_modifiers()`, `combined_traits()`, `total_power_score()` (all sum/iterate across 10); 0.80 per-element clamp preserved; `canonical_loadout.py` serialize/count/select 4→10; the enum→equipped bridge (LEGS→CHEST, SECONDARY_ITEM→off_hand, main_weapon→main_hand). Authors the MIGRATION.md (gen→sim→telemetry→app contract). | jack-ryan Gate-2; GATES seams 2-4 |
| **2** | **gamora** | spirit-guide aggregation: `spirit_guide.py:228-251` `_displaced_value` hard-codes the 4 slot-names and returns 0.0 for unknown slots → widen to all 10 (the "6-of-10-silently-mis-valued" bug jack-ryan flagged). Verify sim consumption of the widened `combined_stats()` is correct; G-SOLO byte-identity check where a 4-slot-equivalent loadout is run. | jack-ryan Gate-2; consumes rocket schema |
| **3** | **star-lord** | telemetry/export of the player loadout + per-element resist fields widened 4→10 (`player_loadout` / resist export surface). Additive/brownfield-safe; existing 4-slot rows must still parse. MIGRATION export-side section. | jack-ryan Gate-2; consumes rocket schema |
| **4** | **drax** | loadout web app surfaces the 10 slots (consumes the serialized 10-slot form). | jack-ryan Gate-2; consumes serialized output |

Seams 2 and 3 may run concurrently once rocket's schema + MIGRATION land. Seam 4 consumes the serialized form.

## Cross-seam contract change? (Principle 6 gate — YES)

This dispatch modifies the **`Loadout` dict shape** (rocket/gamora → star-lord/drax boundary), **canonical serialization**, and **telemetry export fields**. MIGRATION.md REQUIRED per ADR-004 (rocket authors gen→sim side; star-lord co-authors the export side). Each seam's Acceptance MUST include a round-trip smoke.

## Brownfield safety (load-bearing acceptance)

Existing 4-slot loadouts + existing telemetry rows MUST still parse after the widening (or be cleanly migrated). The widening is additive in spirit: the 6 new slots default empty/no-resist on legacy data. A 4-slot legacy loadout loaded into the 10-slot schema must produce byte-identical `combined_stats()` to today (the 6 empty slots contribute 0). This is the G-SOLO-equivalent invariant for 1a.

## Out of scope (explicit non-goals — prevents scope creep)

- **NO breadth-affix mint** (dual/trio/all resist branches) — that is **Step 1b** (separate dispatch, gated on 1a).
- **NO Rule-1 one-resist-affix-per-slot dedupe** — that is **Step 1b**.
- **NO budget / range recalibration**, no band refit, no §4 magnitude changes — that is **Step 1c** (gated on 1a+1b, and COUPLED to the defensive-axis recal + proxy-W3 per `2026-06-22-path-b-1c-defensive-axis-recal-coupling.md`).
- **NO content emission**, no `_DEFERRED_PROXY_BINS` lift, no season regen.
- **NO 11th slot.** Exactly 9 resist-capable.
- **Balance is NOT representative after 1a.** Do NOT milestone-tag 1a as a balance state; do NOT read post-1a win-rates as a balance signal (jack-ryan CONCERN-3). Intermediate `<seam>/v-pathb-1a-*` tags only.

## Acceptance criteria (wave-level; each seam carries its slice into its Gate-2)

- [ ] `Loadout` carries exactly 10 equipped slots; 9 resist-capable; `main_hand` carries no resist.
- [ ] `combined_stats()`, `combined_ability_modifiers()`, `combined_traits()`, `total_power_score()` all correctly iterate/sum across 10; 0.80 per-element resist clamp intact.
- [ ] canonical serialization round-trips 10 slots; `spirit_guide` `_displaced_value` handles all 10 names (no silent 0.0).
- [ ] telemetry exports the 10-slot loadout + per-element resist; existing 4-slot rows still parse.
- [ ] loadout web app surfaces 10 slots.
- [ ] Brownfield invariant: a 4-slot-equivalent loadout yields byte-identical `combined_stats()` vs pre-1a.
- [ ] MIGRATION.md authored (gen→sim→telemetry→app), per ADR-004.
- [ ] Round-trip smoke (rocket→sim, rocket→telemetry, rocket→app): a production-path 10-slot loadout fixture, summed at the sim boundary + exported + serialized, field-presence checked. Smoke BEFORE any full regen (Discipline #2 / #2.1).
- [ ] Discipline #12 semantic-shift declared (Loadout cardinality change).
- [ ] Intermediate `<seam>/v-pathb-1a-*` tags; NO milestone tag.

## Required reading before starting (each seam)
- Path B spec `agentic_orchestration/gandalf/notes/2026-06-22-path-b-resist-design-spec.md` §3.0/§3/§3.1, §4, §15 (and §13.4/§13.5 for context on what 1c will need — NOT 1a's job)
- jack-ryan Gate-1 ratify (CONCERN-1 close, the consumer list, main_weapon→main_hand INFO) — qa/findings or the prior Gate-1 record
- `2026-06-22-path-b-1c-defensive-axis-recal-coupling.md` — so you understand 1c is downstream + coupled; **1a must not touch calibration**
- ADR-004 (MIGRATION); engineering-disciplines #1 (math-before-code), #2 (smoke-test), #11 (empirical inspection), #12 (semantic-shift)

## References
- Supersession decisions-log draft (pending Matt approval): `agentic_orchestration/2026-06-22-path-b-supersession-decisions-log-draft.md`
- gandalf slot reconciliation: spec commit `d538865`; §11.3 fold `7901379`
- Code anchors (jack-ryan-verified): `gear_schema.py:198-306`, `class_schema.py:131-142`, `partition_schema.py:53-64`, `canonical_loadout.py:16-41`, `spirit_guide.py:228-251`
