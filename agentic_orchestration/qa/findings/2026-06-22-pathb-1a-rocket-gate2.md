# Finding — 2026-06-22 — Path B Step 1a — sim Loadout schema widening 4→10 (rocket)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no WARN, no BLOCK)
**Target:** tag `rocket/v-pathb-1a-loadout-schema` (commit `14ee022`, push held)
**Developer:** rocket
**Mode:** DEV-MODE Gate-2 (DESIGN half pre-cleared by gandalf; re-verified here under own eyes)
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 3 + Principle 6 (cross-seam MIGRATION + round-trip), Principle 4 (decisions-log as truth)
**Disciplines applied:** #1 / #1.2 (math-note with code-line refs), #2 / #2.1 (smoke-before-regen), #11 (empirical inspection), #12 (semantic-shift)

## Verdict

**PASS-WITH-INFO.** Step 1a is a clean structural widening. All 9 acceptance criteria verified first-hand; the load-bearing design anchor (`RESIST_CAPABLE_SLOTS` cardinality) confirmed = **9 at runtime**, not merely by source-read. Smoke reproduced independently: **23/23 PASS, exit 0**. No regen occurred (correct). Tag is intermediate `rocket/v-pathb-1a-*` (no milestone tag — correct). Cleared to unblock gamora (seam 2) + star-lord (seam 3); drax (seam 4) consumes serialized output. This is NOT a milestone tag and post-1a win-rates are NOT a balance signal (CONCERN-3 — a known caveat, not a defect).

## What I found

rocket widened the equipped sim `Loadout` from 4 fields (`weapon/off_hand/armor/accessory`) to the 10 canonical equipped slots (`main_hand/off_hand/head/chest/hands/feet/belt/ring_1/ring_2/amulet`), driven by an ordered `EQUIPPED_SLOTS` tuple that is the single source of truth for `_slots()` iteration. The four aggregations (`combined_stats`, `combined_ability_modifiers`, `combined_traits`, `total_power_score`) iterate `_slots()` with unchanged bodies and therefore span all 10 automatically; the 0.80 per-element ceiling / -1.0 floor clamp is byte-for-byte unchanged. The widening is correctly handled as **rename-and-add, not pure-add**: a `model_validator(mode="before")` migrates legacy kwargs (`weapon→main_hand`, `armor→chest`, `accessory→amulet`), three read-only compat properties keep out-of-seam legacy readers alive, and ONE auditable bridge function (`equipped_slot_for()`) folds the 11-member generation `GearSlot` enum onto the 10 equipped ids (`LEGS→CHEST` fold without deleting the enum member, `SECONDARY_ITEM→off_hand`, `MAIN_WEAPON→main_hand`, raises on unknown). The `EQUIPPED_SLOTS` order is deliberately chosen so a legacy 4-field loadout's non-empty subset iterates in the same order as pre-1a, making `combined_stats()` byte-identical (float addition is order-sensitive — the math note proves this in §4). MIGRATION.md, math-note, AGENT_STATE checkpoint, and the Discipline #12 semantic-shift declaration are all present and accurate.

## Per-criterion result

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Exactly 10 equipped slots; exactly 9 resist-capable; `main_hand` no resist | **PASS** | Runtime: `len(EQUIPPED_SLOTS)==10`, `len(RESIST_CAPABLE_SLOTS)==9`, `"main_hand" not in RESIST_CAPABLE_SLOTS`. `gear_schema.py:206-211` |
| 2 | All 4 aggregations iterate/sum across 10; 0.80 clamp preserved exactly | **PASS** | All four iterate `self._slots()` (iterates `EQUIPPED_SLOTS`, all 10); bodies unchanged. Clamp `_RESIST_CEILING=0.80` / `_RESIST_FLOOR=-1.0` byte-identical. `gear_schema.py:326-402`, `:358-363` |
| 3 | Canonical serialization round-trips 10 slots | **PASS** | `serialize_loadout` + `count_legendary` iterate `EQUIPPED_SLOTS`. Smoke L1a.f round-trips 10 keys byte-identical. `canonical_loadout.py:16-38` |
| 4 | Enum→equipped bridge is ONE auditable function | **PASS** | `equipped_slot_for()` is the sole reconciliation point; `LEGS→CHEST` fold, `SECONDARY_ITEM→off_hand`, `main_weapon→main_hand`, raises on unknown. `gear_schema.py:242-253` |
| 5 | Brownfield byte-identity through the legacy 4-FIELD map | **PASS** | Smoke L1a.c constructs `Loadout(weapon=w, off_hand=o, armor=a, accessory=c)` (a genuine 4-FIELD legacy loadout, NOT all-empty-new-slots) and asserts `combined_stats()` byte-identical to the canonical 10-field form AND against an independent ordered Python sum. INFO-1 satisfied exactly. |
| 6 | Consumer sweep to zero (INFO-2) | **PASS** | Grep `weapon=|armor=|accessory=|\.weapon|\.armor|\.accessory` across generation/: all production hits are non-`Loadout` (`weapon_type_family`, `weapon_kind`, `GearStats.bonus_armor=`, monster `armor=round()`, `selected_weapon`, `weapon_identity`, `MaterializedLoadout` enum-keyed dict). The only `Loadout(weapon=/armor=/accessory=)` constructors are inside the smoke harness as deliberate legacy-path tests — handled by the migration validator (proven PASS). `combatant.py`/`damage_resolver.py` hits confirmed `CombatantState armor=` / `GearInstance` reads, NOT `Loadout`-field reads. Zero unhandled production sites. |
| 7 | MIGRATION.md present, gen→sim section authored (ADR-004) | **PASS** | `generation/MIGRATION.md` top entry: full gen→sim→telemetry→app contract; per-seam hand-offs for gamora/star-lord/drax; brownfield-safety section. |
| 8 | Discipline #12 semantic-shift declared (cardinality 4→10) | **PASS** | Declared in MIGRATION.md, math-note §6, and AGENT_STATE checkpoint. |
| 9 | Round-trip smoke reproduced (don't trust the claim) | **PASS** | Ran `typed_resistance_roundtrip_smoke_2026_06_21.py` myself: **23/23 PASS, exit 0** (15 original typed-resistance — no regression — + 8 new L1a.a–h). Single smoke surface extended per INFO-3, not a parallel harness. No regen present in the commit (no `output/`/season/`.json` artifacts). |

## Design anchor — verified under own eyes

`RESIST_CAPABLE_SLOTS = frozenset(EQUIPPED_SLOTS) - {"main_hand"}` (`gear_schema.py:211`). **Runtime cardinality = 9** (confirmed by executing `len(RESIST_CAPABLE_SLOTS)`, not by source-read alone): `['amulet','belt','chest','feet','hands','head','off_hand','ring_1','ring_2']`. `main_hand` confirmed absent. The `legs→chest` fold (`gear_schema.py:234`) keeps the resist-capable count at exactly 9 without deleting the `LEGS` enum member. The load-bearing property holds: 9 resist-capable × +9 resist-all ceiling = +81 → just-caps 7 elements; no 10th resist-capable slot exists to make capping free / reopen the spec §9 tax. gandalf's hard Gate-2 check passes independently.

## INFO items (record only — no action gating 1a)

- **INFO-A (carry-item, NOT a 1a defect):** Two consumer updates are correctly DEFERRED to gamora seam-2 and are documented in MIGRATION.md: (1) `spirit_guide.py:228-251 _displaced_value` hard-codes the 4 legacy slot-name STRINGS and returns 0.0 for unknown slots — the "6-of-10 silently mis-valued" bug — must widen to all 10 names; the compat read-properties keep the *attribute* reads alive but NOT the slot-name string switch. (2) `combatant.py:889` reads `carried_gear.get("weapon")` from the serialized dict, which now emits `main_hand` — gamora must add `main_hand` to the weapon-key lookup. Their absence in 1a is correct per spec §15 seam-ownership; flagging only so the gamora Gate-2 verifies both.
- **INFO-B:** The three `.weapon/.armor/.accessory` read-only compat properties are explicitly temporary shims (documented as such in `gear_schema.py:296-307` and math-note §3). The empirical-evidence criterion that gates their removal: each is superseded when its consuming seam (gamora spirit_guide for the displaced-value path; any other out-of-seam reader) completes its own widening. They should not outlive 1c. Not a 1a action.
- **INFO-C:** Step 1a is correctly scoped — no breadth-affix mint (1b), no Rule-1 dedupe (1b), no budget/range/band recalibration (1c), no content emission / `_DEFERRED_PROXY_BINS` lift / regen. The `gear_generation.py:1333` constructor still mints the same 4 items, remapped to canonical kwargs only. Verified via commit diff.

## Approval authority note (ADR-002)

This is a **cross-seam schema change** (the `Loadout` dict shape + canonical serialization cross the rocket/gamora → star-lord/drax boundary). Per ADR-002, cross-seam schema changes escalate to Matt — but this Gate-2 carries no BLOCK and no unresolved WARN, so the escalation is informational: the verdict is PASS-WITH-INFO and the only Matt-gated actions remaining are (a) the held push and (b) milestone tagging (which is correctly NOT requested — intermediate tag only). gandalf relays this verdict to Matt.

## Action

- [x] jack-ryan: Gate-2 PASS-WITH-INFO recorded. 1a cleared — gamora (seam 2) + star-lord (seam 3) unblocked; drax (seam 4) consumes serialized output.
- [ ] gamora (seam-2 Gate-2): verify the two INFO-A carry-items land (`_displaced_value` 4→10 names; `combatant.py:889` add `main_hand`) + re-assert G-SOLO byte-identity through the sim boundary.
- [ ] Matt (informational, not blocking): held push remains Matt-gated; no milestone tag requested (correct).

## References

- Tagged commit: `rocket/v-pathb-1a-loadout-schema` = `14ee022`
- `reincarnated-engine/src/reincarnated/generation/gear_schema.py:196-421` (EQUIPPED_SLOTS, RESIST_CAPABLE_SLOTS, _LEGACY_FIELD_MAP, equipped_slot_for, Loadout + 4 aggregations + clamp)
- `reincarnated-engine/src/reincarnated/generation/canonical_loadout.py:16-78`
- `reincarnated-engine/src/reincarnated/generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py:287-414` (the 1a checks; reproduced 23/23 PASS)
- `reincarnated-engine/src/reincarnated/generation/math/pathb-1a-loadout-schema-widening-math-2026-06-22.md`
- `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (2026-06-22 Path B 1a entry, top)
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (2026-06-22 checkpoint)
- Dispatch: `agentic_orchestration/dispatches/2026-06-22-rocket-pathb-1a-loadout-schema-widening.md`
- Wave MASTER: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`
- Spec: `agentic_orchestration/gandalf/notes/2026-06-22-path-b-resist-design-spec.md` §3.0/§3/§3.1/§4/§15
