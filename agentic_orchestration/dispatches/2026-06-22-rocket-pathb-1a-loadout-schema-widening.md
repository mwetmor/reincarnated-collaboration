# Dispatch — 2026-06-22 — rocket — Path B Step 1a — Loadout schema widening 4→10 (FOUNDATIONAL)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-22 ("GO on 1a author+fire")
**Estimated effort:** multi-day (foundational seam; GATES gamora/star-lord/drax)
**Acceptance:** `Loadout` carries exactly 10 equipped slots (9 resist-capable); all aggregation methods iterate/sum across 10; canonical serialization round-trips 10; the enum→equipped bridge is a single auditable function; MIGRATION.md authored; brownfield byte-identity invariant holds; smoke passes BEFORE any regen. Intermediate `rocket/v-pathb-1a-*` tags only — NO milestone tag.

## Context

This is the **foundational first build piece of Path B** (cap-everything-but-costly resist, the resist design-of-record per gandalf spec `2026-06-22-path-b-resist-design-spec.md`; jack-ryan Gate-1 fully PASSES). Read the wave MASTER first: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`. Your seam is **seam 1 of 4** and your schema + MIGRATION **gate** gamora (seam 2), star-lord (seam 3), and drax (seam 4) — they cannot start until your schema and MIGRATION land.

The live sim sums only a **4-slot** `Loadout` (`gear_schema.py:198-228` — weapon/off_hand/armor/accessory; 3 resist-capable), while a 10-slot generation-side slot model exists separately. 1a **bridges** the existing 10-slot generation representation into the equipped `Loadout` the sim runs. The authoritative slot inventory is **`gear_slot_labels` (`class_schema.py:131-142`): 10 equipped slots = 1 weapon (`main_hand`, no resist) + 9 resist-capable.**

**This is a STRUCTURAL WIDENING ONLY.** No affix mint changes (that's 1b), no budget/range calibration (that's 1c). The existing single-element resist mint and existing budget flow through unchanged.

## The 10 canonical equipped slots (authoritative — `gear_slot_labels`)

`main_hand` (weapon, **no resist**), `off_hand`, `head`, `chest`, `hands`, `feet`, `belt`, `ring_1`, `ring_2`, `amulet` → **9 resist-capable** (everything except `main_hand`).

## Why the +9 count is load-bearing (do not alter without re-deriving the spec)

Spec §4 property-2 / Rule-2: 9 resist-capable slots × resist-all `+9` ceiling = `+81` → just-caps all 7 elements. If the resist-capable count drifts to 10, capping gets free → reopens the §9 tax. **You must land EXACTLY 9 resist-capable slots; `main_hand` carries no resist.** This is a Gate-2 check.

## Math-before-code (Discipline #1 — document before implementing)

Before touching code, write a short math-note (in your AGENT_STATE.md or a sibling note) that records:
1. The 10 equipped slots and which 9 are resist-capable (verbatim from `gear_slot_labels`).
2. The enum→equipped name map you will implement in the bridge:
   - `LEGS` → `CHEST` (fold; keeps resist-capable count at exactly 9 — an 11th resist-capable slot would be the §9 free-baseline tax; gandalf ruling)
   - `SECONDARY_ITEM` → `off_hand`
   - `MAIN_WEAPON` / `main_weapon` → `main_hand`
   - all other enum members → their identity equipped-label
3. The brownfield invariant statement: a 4-slot-equivalent loadout (6 new slots empty) yields **byte-identical** `combined_stats()` vs pre-1a (the 6 empty slots contribute 0). This is the G-SOLO-equivalent invariant for 1a.
4. **(jack-ryan Gate-1 INFO-1) The legacy 4-field → 10-field migration map.** The live 4-slot Loadout (`gear_schema.py:207-210`) uses field names `weapon` / `armor` / `accessory` / `off_hand` — NOT `main_hand` / `chest` / `amulet`. Widening 4→10 is therefore **rename-and-add, not pure-add.** Write down the explicit map used to load legacy/4-field data into the 10-field schema: `weapon→main_hand`, `armor→<target slot, document which>`, `accessory→<target slot, document which>`, `off_hand→off_hand`. The brownfield byte-identity invariant is asserted **across THIS map** — the Gate-2 test must construct a legacy 4-FIELD loadout and assert `combined_stats()` identity *through* the migration, NOT merely an all-empty-new-slots 10-field loadout.

## Cross-seam contract change? (Principle 6 gate — YES)

This dispatch modifies the **`Loadout` dict shape** (rocket/gamora → star-lord/drax boundary) and **canonical serialization**. **MIGRATION.md REQUIRED per ADR-004.** You author the gen→sim side of the contract (gen→sim→telemetry→app); star-lord co-authors the export-side section in seam 3. Your Acceptance MUST include a round-trip smoke.

## Scope

- [ ] `Loadout` schema (`gear_schema.py:198-228`) widened from 4 slots to 10 equipped slots (9 resist-capable; `main_hand` no resist).
- [ ] `_slots()` (or equivalent slot-iterator) returns all 10.
- [ ] `combined_stats()` (`:230`), `combined_ability_modifiers()` (`:281/:290`), `combined_traits()` (`:298/:301`), `total_power_score()` (`:305/:306`) all iterate/sum across 10.
- [ ] 0.80 per-element resist clamp (`:262-267`) preserved exactly.
- [ ] `canonical_loadout.py` (`:16-41`) serialize/count/select widened 4→10; round-trips 10 slots.
- [ ] The enum→equipped bridge implemented as **ONE auditable function** (LEGS→CHEST, SECONDARY_ITEM→off_hand, main_weapon→main_hand). All naming reconciliation lives in this one place.
- [ ] **(jack-ryan Gate-1 INFO-2) In-seam consumer sweep for the renamed fields.** Sweep all in-seam `Loadout` constructors and `.weapon`/`.armor`/`.accessory` readers (`keystone_loadout_materializer.py`, `gear_generation.py`, `canonical_loadout.py`, the `typed_resistance_roundtrip_smoke` harness) — legacy kwargs must either map or be migrated. Grep `weapon=|armor=|accessory=|\.weapon|\.armor|\.accessory` to **zero unhandled sites before tag.** (Note for the gamora seam-2 Gate-2: `combatant.py` / `damage_resolver.py` appear in the grep — those must be verified as `GearInstance` weapon-handedness reads, NOT `Loadout`-field reads.)
- [ ] MIGRATION.md authored (gen→sim→telemetry→app contract; you own gen→sim side).
- [ ] Smoke-test passes (BEFORE any full regen — Discipline #2 / #2.1).
- [ ] Round-trip smoke per Principle 6 (see Acceptance).
- [ ] Discipline #12 semantic-shift declared (Loadout cardinality change 4→10).
- [ ] AGENT_STATE.md updated at session end with math-note + what landed + what gamora/star-lord need.
- [ ] Tag: `rocket/v-pathb-1a-loadout-schema` (intermediate — NO milestone tag).

## Acceptance criteria

- [ ] `Loadout` carries exactly 10 equipped slots; 9 resist-capable; `main_hand` carries no resist.
- [ ] All four aggregation methods correctly iterate/sum across 10; 0.80 per-element clamp intact.
- [ ] Canonical serialization round-trips 10 slots.
- [ ] Enum→equipped bridge is a single function; LEGS→CHEST, SECONDARY_ITEM→off_hand, main_weapon→main_hand all normalized there.
- [ ] **Brownfield invariant:** a 4-slot-equivalent loadout (6 new slots empty) yields byte-identical `combined_stats()` vs pre-1a.
- [ ] **Round-trip smoke:** a production-path 10-slot loadout fixture, generated → serialized (`canonical_loadout.py`) → deserialized → summed (`combined_stats()`), field-presence + byte-identity checked. (The sim-boundary + export legs are exercised by gamora/star-lord in seams 2/3 against your schema; your round-trip is gen→serialize→sum.)
- [ ] MIGRATION.md present, gen→sim section authored.

## Out of scope (explicit non-goals — prevents scope creep)

- **NO breadth-affix mint** (dual/trio/all resist branches) — that is **Step 1b**.
- **NO Rule-1 one-resist-affix-per-slot dedupe** — that is **Step 1b**. Do NOT touch `gear_generation.py` mint logic or the `replace=False` at `:1129`.
- **NO budget / range recalibration**, no band refit, no §4 magnitude changes — that is **Step 1c**.
- **NO content emission**, no `_DEFERRED_PROXY_BINS` lift, no season regen.
- **NO 11th slot.** Exactly 9 resist-capable.
- **Balance is NOT representative after 1a.** Do NOT milestone-tag 1a; do NOT read post-1a win-rates as a balance signal (jack-ryan CONCERN-3). Intermediate `rocket/v-pathb-1a-*` tags only.

## Open questions for the agent to resolve (document your call)

- Whether `LEGS`-tagged generated gear is re-slotted onto `CHEST` at bridge time or whether `LEGS` is dropped from generation entirely for now. The MASTER requires LEGS→CHEST **fold on the bridge** (keeps equipped count at 10 / resist-capable at 9) — implement the fold; do not delete the enum member (that risks generation-side breakage). Document the exact fold semantics you chose.
- Default representation of an empty slot such that it contributes 0 to all four aggregations and serializes/deserializes cleanly (the brownfield invariant depends on this).
- **(jack-ryan Gate-1 INFO-3)** A round-trip smoke harness already exists: `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py` (from the 2026-06-21 typed-resistance wave; exercises serialize→sum). **Extend it for 10-slot rather than authoring a parallel harness** — keeps the smoke surface single (Discipline #2.1).

## References

- Wave MASTER: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`
- Path B spec: `agentic_orchestration/gandalf/notes/2026-06-22-path-b-resist-design-spec.md` §3.0/§3/§3.1, §4, §15
- 1c coupling (downstream context — 1a must NOT touch calibration): `agentic_orchestration/2026-06-22-path-b-1c-defensive-axis-recal-coupling.md`
- gandalf slot reconciliation: spec commit `d538865`; §11.3 fold `7901379`
- Code anchors (jack-ryan-verified): `gear_schema.py:198-306`, `class_schema.py:131-142`, `partition_schema.py:53-64`, `canonical_loadout.py:16-41`
- ADR-004 (MIGRATION); engineering-disciplines #1 (math-before-code), #2/#2.1 (smoke-test), #11 (empirical inspection), #12 (semantic-shift)
