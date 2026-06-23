# Dispatch — 2026-06-22 — drax — Path B Step 1a — loadout app surfaces 10 slots (SEAM 4)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-06-22 (seam 4, after seams 2-3 Gate-2 PASS)
**Estimated effort:** ≤1 day (presentation widening; consumes the serialized 10-slot form)
**Acceptance:** the loadout web app surfaces the 10 serialized equipped slots; existing 4-key loadout data still renders without breaking; jack-ryan Gate-2 PASS.

## Context

Path B Step 1a — the `Loadout` schema widening 4→10 — is landed and Gate-2-clean through three seams:
- rocket (seam 1, schema): engine `14ee022`, tag `rocket/v-pathb-1a-loadout-schema`, Gate-2 PASS (`e2413ef`).
- gamora (seam 2, sim): `bae3bf1`, Gate-2 PASS.
- star-lord (seam 3, telemetry/export): `3320403`, Gate-2 PASS. Export is opaque-TEXT pass-through; serialized loadout now carries 10 keys.
- Combined Gate-2 findings: `agentic_orchestration/qa/findings/2026-06-22-pathb-1a-seams-2-3-gate2.md` (`260986f`).

You are **seam 4 of 4** — the player-facing presentation. You consume the **serialized 10-slot form** in the loadout web app (`reincarnated-loadout/`). This is a **structural-presentation** wave: surface the 10 slots. **No design/balance work, no resist-magnitude display logic** (the mint that fills resist on the 9 slots is 1b — you render whatever the loadout carries; post-1a that is still the single-element mint). Post-1a state is NOT a balance signal (CONCERN-3).

## The 10 canonical serialized slot keys (authoritative)

From `serialize_loadout` (star-lord verified the export emits exactly these): `main_hand`, `off_hand`, `head`, `chest`, `hands`, `feet`, `belt`, `ring_1`, `ring_2`, `amulet`. **Empty slots serialize to JSON `null`.** `main_hand` carries no resist; the other 9 are resist-capable. Order: use the canonical `EQUIPPED_SLOTS` order above.

## Scope

- [ ] Loadout web app surfaces all 10 equipped slots (consumes the serialized 10-slot form).
- [ ] Empty slots (JSON `null`) render cleanly as empty, not as errors/blanks-that-break-layout.
- [ ] **Brownfield tolerance:** any existing 4-key loadout data the app may load (`weapon`/`off_hand`/`armor`/`accessory`) must still render without breaking. If the app has its own slot-name constants or a TS mirror of the slot list, widen it to the 10 canonical keys; keep a tolerant mapping for legacy 4-key shapes (`weapon→main_hand`, `armor→chest`, `accessory→amulet`) so historical data renders.
- [ ] Smoke / app builds + renders cleanly with a 10-slot fixture AND a legacy 4-key fixture (Discipline #2).
- [ ] AGENT_STATE.md updated at session end (drax keeps state for `reincarnated-loadout/`).
- [ ] Tag: `drax/v-pathb-1a-loadout-app` (intermediate — NO milestone tag).

## Cross-seam contract change? (Principle 6 gate)

**NO new cross-seam contract authored by this seam** — you are a downstream CONSUMER of the serialized form rocket/star-lord already MIGRATION'd. You do not add/rename/remove a field that another seam consumes. **Round-trip: not applicable — this seam consumes the serialized 10-slot form; it authors no contract.** (Your app-render check with a 10-slot fixture + a legacy 4-key fixture IS your boundary verification.)

## Acceptance criteria

- [ ] App renders all 10 slots from a serialized 10-slot loadout fixture, in canonical order, with `main_hand` distinguished as the non-resist weapon slot.
- [ ] Empty (`null`) slots render as empty without layout/JS errors.
- [ ] A legacy 4-key loadout fixture still renders (brownfield tolerance).
- [ ] Round-trip: not applicable — consumer seam, authors no contract.

## Out of scope (explicit non-goals)

- **NO resist-magnitude / breadth-affix display logic** — that is 1b content; render what the loadout carries.
- **NO budget / calibration / balance surfacing** — that is 1c.
- **NO redesign of the loadout UX** beyond surfacing the 6 additional slots. Minimal structural widening; do not re-theme or re-flow beyond what 10 slots require.
- **NO milestone tag.** Intermediate `drax/v-pathb-1a-*` only.
- **Do not touch any path inside `reincarnated-engine/`** — you consume the serialized form, you do not modify the schema or export.

## Required reading before starting
- Rocket MIGRATION: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` → `[2026-06-22] Path B Step 1a` section (the 10 serialized keys + star-lord's export-side co-author section `### star-lord seam 3`)
- Wave MASTER: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`
- Combined seams 2-3 Gate-2: `agentic_orchestration/qa/findings/2026-06-22-pathb-1a-seams-2-3-gate2.md`
- Path B spec §3.0/§3/§3.1, §15; decisions-log Path B supersession entry (engine `dafcd99`)

## References
- Serialized contract: `serialize_loadout` emits the 10 `EQUIPPED_SLOTS` keys, empties → null
- star-lord round-trip smoke (the export shape you consume): `~/Games/reincarnated-engine/src/reincarnated/export/pathb_1a_telemetry_roundtrip_smoke_2026_06_22.py`
- engineering-disciplines #2 (smoke), #11 (empirical inspection), #12 (semantic-shift)
