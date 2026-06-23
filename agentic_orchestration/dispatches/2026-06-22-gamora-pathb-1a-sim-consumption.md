# Dispatch — 2026-06-22 — gamora — Path B Step 1a — sim consumption of the widened Loadout (SEAM 2)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-22 (release seams 2-3 after rocket 1a Gate-2 PASS)
**Estimated effort:** ≤1 day (two pinpoint consumer fixes + a byte-identity re-assert)
**Acceptance:** `spirit_guide._displaced_value` values all 10 slots (no silent 0.0); `combatant.py:889` resolves `main_hand` from the serialized loadout; G-SOLO byte-identity re-asserted through the sim boundary; jack-ryan Gate-2 PASS.

## Context

Rocket landed Path B Step 1a — the foundational `Loadout` schema widening 4→10 (engine commit `14ee022`, tag `rocket/v-pathb-1a-loadout-schema`; jack-ryan Gate-2 PASS-WITH-INFO, findings `e2413ef`). The schema + the gen→sim MIGRATION contract are in place; you are **seam 2 of 4**, consuming rocket's schema. This is a **structural-consumption** wave — you make the sim correctly value and resolve the 10-slot loadout. **No calibration, no balance work** (that is 1c; post-1a win-rates are NOT a balance signal — jack-ryan CONCERN-3).

Read rocket's MIGRATION entry first: `src/reincarnated/generation/MIGRATION.md` → the `[2026-06-22] Path B Step 1a` section, especially **⚠️ DOWNSTREAM CONSUMERS → gamora (seam 2)**. It specifies both fixes precisely.

## The 10 canonical equipped slots (authoritative)

`gear_schema.EQUIPPED_SLOTS` (ordered tuple) is the single source of truth. `RESIST_CAPABLE_SLOTS` = that set minus `main_hand` (cardinality **9**). Use these constants — do NOT re-hardcode slot-name lists.

## Scope (the two rocket hand-offs + the invariant re-assert)

- [ ] **Fix 1 — `spirit_guide.py:228-251` `_displaced_value`.** It hard-codes the 4 legacy slot-name STRINGS (`weapon/off_hand/armor/accessory`) and returns `0.0` for any unknown slot → the "**6-of-10 silently mis-valued**" bug. **Widen the slot-name string switch to all 10 `EQUIPPED_SLOTS` names** so the 6 new slots are valued, not silently zeroed. (The compat `.weapon/.armor/.accessory` properties keep *attribute* reads alive in the interim, but the slot-name STRING switch is what must widen.)
- [ ] **Fix 2 — `combatant.py:889`.** It reads `carried_gear.get("weapon") or carried_gear.get("main_weapon")` from the **serialized** loadout dict. `serialize_loadout` now emits `main_hand`, not `weapon`. The substrate-binding `carried_gear` path (`season_generation_pipeline.py:1536` `{"main_weapon": …}`) still resolves; the `select_canonical_loadout`/`serialize_loadout` path no longer does. **Add `main_hand` to the weapon-key lookup:** `_carried.get("main_hand") or _carried.get("weapon") or _carried.get("main_weapon")`.
- [ ] **Invariant — G-SOLO byte-identity through the sim boundary.** Rocket asserted the brownfield invariant at the schema (a 4-slot-equivalent loadout → byte-identical `combined_stats()`; smoke L1a.c/d). **Re-assert it through the sim boundary:** run a 4-slot-equivalent loadout through the sim and confirm the result is byte-identical to pre-1a (the 6 empty slots contribute 0). This is the G-SOLO-equivalent check for seam 2.
- [ ] Verify sim consumption of the widened `combined_stats()` is correct (it iterates `_slots()` which now spans 10; rocket left the bodies unchanged — confirm the sim reads them correctly).
- [ ] Smoke-test passes (Discipline #2 — BEFORE any full regen).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-pathb-1a-sim-consumption` (intermediate — NO milestone tag).

## Cross-seam contract change? (Principle 6 gate)

**NO new cross-seam contract authored by this seam** — you consume rocket's already-MIGRATION'd `Loadout` shape; you do not add/rename/remove a field crossing sim→telemetry. **Round-trip: not applicable — no cross-seam contract change authored in this dispatch** (the G-SOLO byte-identity re-assert above IS your boundary check against rocket's schema).

## Acceptance criteria

- [ ] `_displaced_value` returns a non-zero value for all 10 occupied slot names; no slot silently zeroed.
- [ ] `combatant.py:889` resolves the weapon from a `serialize_loadout`-emitted dict (`main_hand` key) AND still resolves the legacy `carried_gear` substrate path (`main_weapon`).
- [ ] G-SOLO byte-identity: a 4-slot-equivalent loadout run through the sim yields byte-identical result vs pre-1a.
- [ ] Round-trip: not applicable — no cross-seam contract change authored in this dispatch.

## Out of scope (explicit non-goals)

- **NO breadth-affix mint consumption** (dual/trio/all resist) — that machinery doesn't exist until 1b.
- **NO budget / band / magnitude calibration**, no re-rate, no balance loop run-for-signal — that is **1c** (and 1c is the coupled compound re-open; not this seam's job).
- **NO content emission, no season regen for balance signal.** Post-1a win-rates are NOT representative (CONCERN-3).
- **Do NOT lean on the compat shims as permanent.** `.weapon/.armor/.accessory` are rocket's TEMPORARY read-only properties to keep out-of-seam legacy readers alive until each widens. **They must not outlive 1c** — supersede the slot-name STRING reads in this seam now; flag any shim you cannot yet remove for the 1c cleanup.

## Required reading before starting
- Rocket MIGRATION: `src/reincarnated/generation/MIGRATION.md` → `[2026-06-22] Path B Step 1a` section (the gamora seam-2 hand-off list is verbatim there)
- Rocket math note: `generation/math/pathb-1a-loadout-schema-widening-math-2026-06-22.md` (§4 brownfield invariant)
- Wave MASTER: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`
- Path B spec §3.0/§3/§3.1, §4, §15; decisions-log Path B supersession entry (engine `dafcd99`)
- 1c coupling (downstream context — this seam must NOT touch calibration): `agentic_orchestration/2026-06-22-path-b-1c-defensive-axis-recal-coupling.md`
- engineering-disciplines #1, #2, #11, #12

## References
- rocket Gate-2: `agentic_orchestration/qa/findings/` 1a findings (`e2413ef`); rocket commit `14ee022`, tag `rocket/v-pathb-1a-loadout-schema`
- Code anchors: `spirit_guide.py:228-251`, `combatant.py:889`, `gear_schema.py EQUIPPED_SLOTS/RESIST_CAPABLE_SLOTS`, `canonical_loadout.py serialize_loadout`
