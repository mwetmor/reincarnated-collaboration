# Finding — 2026-06-22 — Path B Step 1a seam 4 (drax — loadout app)

**Reviewer:** jack-ryan
**Severity:** PASS (PASS-WITH-INFO)
**Target:** tag `drax/v-pathb-1a-loadout-app`, commit `075f692` (repo: reincarnated-loadout; LOCAL, not pushed, not deployed)
**Developer:** drax
**Principles applied:** #1 (math-before-code / contract fidelity), #2 (smoke-gate), #3 (cross-seam impact), #6 (cross-seam round-trip), #11 (empirical inspection), #12 (semantic-shift)

## What I found

Seam 4 — the final Path B Step 1a seam — consumes the engine's `serialize_loadout` 10-key form in the loadout web app, and does so as a clean downstream consumer that authors no contract. The four flagged claims all hold under first-hand verification. (1) EMPIRICAL: the app had no prior consumer of the serialized 10-key form. The pre-existing equipped-view paths are `synthesizeSampleLoadout` (verified: maps to legacy 4-key engine slots `weapon`/`off_hand`/`armor`/`accessory`), the `gear_representative` Cycle-14 artifact (verified: separate 11-slot shape with `main_weapon`/`secondary_item`/`legs` in `Cycle14GearDisplay.tsx` + `cycle13Types.ts`), and the `/loadout` kit-space substrate proxy with no equipped grid. A new consumer is the correct structural move, not a redundant path. (2) NEW FILES: all four present and as described. (3) CONTRACT FIDELITY: `EQUIPPED_SLOTS` matches the engine MIGRATION `[2026-06-22] Path B Step 1a` section exactly — 10 keys in canonical order (`main_hand, off_hand, head, chest, hands, feet, belt, ring_1, ring_2, amulet`), `RESIST_CAPABLE_SLOTS` derived as 9 (= minus `main_hand`), `main_hand` the non-resist weapon slot, with the +9-just-caps-7-elements rationale correctly cited. `RESIST_CAPABLE_SLOTS` is `.filter`-derived from `EQUIPPED_SLOTS` so it cannot silently drift — a sound defensive choice. (4) BROWNFIELD / NO CONFLATION: `normalizeSerializedLoadout()` maps the `serialize_loadout` legacy 4-key shape (`weapon→main_hand`, `armor→chest`, `accessory→amulet`; `off_hand` already canonical) and explicitly does NOT touch the `gear_representative` `main_weapon`/`legs`-fold shape. The two shapes are confirmed kept distinct — `Cycle14GearDisplay.tsx` was untouched. Canonical-key-wins-over-legacy-alias is tested. (5) SMOKE: `npm run build` clean (0 TS errors; the >500kB chunk warning is pre-existing, not introduced here); `npm run test` 91/91 (+12 new across both 10-slot and legacy-4-key fixtures + edge cases). (6/7) HOLDS: structural-presentation only — no resist-magnitude/breadth display, no calibration surfacing, no UX re-theme beyond the 6 added slots, intermediate tag only, no `reincarnated-engine/` edits, no push/deploy. The kit-space route renders 10 empty slots today (kit JSON carries no serialized loadout; gear pending EAA-8) behind a documented `TODO(drax)` fallback, correctly framed in-code as expected structural state and explicitly NOT a balance signal (CONCERN-3). All holds observed.

## Rationale

Discipline #11 (empirical inspection) satisfied: drax inspected the actual consumer paths rather than assuming, and the inspection is reproducible — I re-ran the greps and confirmed each path. Discipline #12 (semantic-shift) satisfied: the 4→10 cardinality widening is surfaced structurally with the resist-capable=9 invariant preserved and called out, with no bleed into 1b magnitude or 1c budget interpretation. Discipline #1 (contract fidelity) satisfied: the consumer-side mirror matches the authoritative engine `EQUIPPED_SLOTS` byte-for-byte in key set, order, and cardinality. Principle #6 (cross-seam round-trip) correctly assessed N/A — this seam consumes a contract the upstream seams already MIGRATION'd and emits none; the dual-fixture render test is the appropriate boundary verification for a consumer. Discipline #2 (smoke-gate) satisfied with build + dual-fixture tests, run first-hand. No principle violated; nothing rises to WARN or BLOCK.

## Action

- [x] Developer: no action required for PASS.
- [ ] Developer (1b, non-blocking INFO): when 1b lands resist-magnitude/breadth display, extend `EquippedSlotView` past the opaque `unknown` `item` type and drive per-slot resist surfacing off `RESIST_CAPABLE_SLOTS`; the seam is already shaped for this (`resistCapable` flag present per row).
- [ ] Developer (EAA-8, non-blocking INFO): drop the `?? null` fallback in `Loadout.tsx` and the `kit as unknown as {...}` cast once EAA-8 ships a `serialized_loadout` / `loadout` field per kit; the `TODO(drax)` markers are in place.

## INFO carried forward (no action this seam)

- INFO-A (to 1b): per-slot value is intentionally opaque (`item: unknown`); the grid shows filled/empty + a best-effort compact name only. 1b is the seam that introduces resist-magnitude interpretation. The structural surface is ready for it.
- INFO-B (to EAA-8): the kit-space route renders 10 empties today because kit JSON carries no serialized loadout. This is structural state, NOT a balance reading (CONCERN-3 holds). The grid activates automatically once a kit carries the field.
- INFO-C (cosmetic, no action): `EquippedSlotsGrid.tsx` reaches into the opaque payload for `obj.name ?? obj.gear_id ?? obj.id` to derive a compact name. This is a thin, null-safe best-effort that does NOT interpret resist content, so it stays within the 1a hold. Noted only so 1b is aware the name-derivation exists.

## References

- `~/Games/reincarnated-loadout/src/data/serializedLoadout.ts`
- `~/Games/reincarnated-loadout/src/components/GearGrid/EquippedSlotsGrid.tsx`
- `~/Games/reincarnated-loadout/src/pages/Loadout.tsx` (Equipment section, ll. 615-638)
- `~/Games/reincarnated-loadout/src/__tests__/serialized-loadout-10slot.test.ts`
- `~/Games/reincarnated-loadout/src/utils/synthesizeSampleLoadout.ts` (legacy 4-key path — confirms no conflation)
- `~/Games/reincarnated-loadout/src/components/Cycle14/Cycle14GearDisplay.tsx` (gear_representative 11-slot shape — confirmed untouched/distinct)
- Engine contract source: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` → `[2026-06-22] Path B Step 1a`
- Dispatch + completion record: `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-22-drax-pathb-1a-loadout-app.md`

## Path B Step 1a status

With this PASS, all 4 Path B Step 1a seams are Gate-2-clean: rocket (schema, `14ee022`), gamora (sim, `bae3bf1`), star-lord (telemetry/export, `3320403`), drax (loadout app, `075f692`). **Step 1b is unblocked.**
