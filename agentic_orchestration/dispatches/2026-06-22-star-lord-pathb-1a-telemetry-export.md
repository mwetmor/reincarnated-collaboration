# Dispatch — 2026-06-22 — star-lord — Path B Step 1a — telemetry/export of the widened Loadout (SEAM 3)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-22 (release seams 2-3 after rocket 1a Gate-2 PASS)
**Estimated effort:** ≤1 day (additive, brownfield-safe export widening + export-side MIGRATION section)
**Acceptance:** `loadout_json` / `player_loadout` / per-element resist export surface carries the 10 slots; existing 4-key rows still parse; export-side MIGRATION section co-authored; jack-ryan Gate-2 PASS.

## Context

Rocket landed Path B Step 1a — the `Loadout` schema widening 4→10 (engine commit `14ee022`, tag `rocket/v-pathb-1a-loadout-schema`; jack-ryan Gate-2 PASS-WITH-INFO, findings `e2413ef`). You are **seam 3 of 4**, consuming rocket's schema; you may run **concurrently with gamora (seam 2)**. This is a **structural-export** wave — surface the 10-slot loadout + per-element resist in telemetry/export, additively and brownfield-safe. **No calibration, no balance work** (1c); post-1a win-rates are NOT a balance signal (CONCERN-3).

Read rocket's MIGRATION entry first: `src/reincarnated/generation/MIGRATION.md` → `[2026-06-22] Path B Step 1a` section, **⚠️ DOWNSTREAM CONSUMERS → star-lord (seam 3)**. **You co-author the export-side MIGRATION section** there (rocket authored the gen→sim side).

## The 10 canonical equipped slots (authoritative)

Serialized keys (from `serialize_loadout`): `main_hand`, `off_hand`, `head`, `chest`, `hands`, `feet`, `belt`, `ring_1`, `ring_2`, `amulet`. Empty slots serialize to JSON `null`. `main_hand` carries no resist; the other 9 are resist-capable.

## Scope

- [ ] Widen the `loadout_json` / `player_loadout` / per-element resist **export surface** from 4 keys to the 10 `EQUIPPED_SLOTS` keys.
- [ ] **Brownfield parse-tolerance (load-bearing):** existing 4-key `loadout_json` rows MUST still parse. Per rocket's MIGRATION, the `serialize_loadout` consumers (`balance_loop.py` / `recorder.py`) pass the JSON through as **opaque TEXT** — the shape change is in the keys. New rows carry 10 keys; historical rows carry 4. **Your export/parse path must tolerate BOTH** (the 4-key shape is historical and must not error).
- [ ] **Co-author the export-side MIGRATION section** in `src/reincarnated/generation/MIGRATION.md` under rocket's `[2026-06-22] Path B Step 1a` entry (extend it; do not start a new dated entry — this is the same cross-seam contract).
- [ ] Smoke-test passes (Discipline #2 — BEFORE any regen).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `star-lord/v-pathb-1a-telemetry-export` (intermediate — NO milestone tag).

## Cross-seam contract change? (Principle 6 gate — YES, export side)

This dispatch modifies the **telemetry/export field surface** (`loadout_json` / `player_loadout` / per-element resist export). MIGRATION export-side section REQUIRED (co-author under rocket's entry). Acceptance MUST include a round-trip smoke (below).

## Acceptance criteria

- [ ] Export surface emits the 10-slot loadout + per-element resist fields.
- [ ] **Round-trip smoke:** a production-path 10-slot serialized loadout fixture → exported (telemetry write path) → read back, field-presence checked across all 10 keys; AND a historical 4-key `loadout_json` row → parsed without error (brownfield parse-tolerance). Use a production-path fixture, not a hand-rolled dict.
- [ ] Export-side MIGRATION section present under rocket's `[2026-06-22] Path B Step 1a` entry.

## Out of scope (explicit non-goals)

- **NO breadth-affix / per-element-resist-magnitude content** — the mint that fills resist on the 9 slots is 1b; you export whatever the loadout carries, which post-1a is still the single-element mint.
- **NO budget / band / calibration**, no re-rate — that is **1c**.
- **NO content emission, no season regen for balance signal.** Post-1a win-rates NOT representative (CONCERN-3).
- **NO breaking change to historical rows.** Widening is additive; the 4-key historical shape must keep parsing.

## Required reading before starting
- Rocket MIGRATION: `src/reincarnated/generation/MIGRATION.md` → `[2026-06-22] Path B Step 1a` section (star-lord seam-3 hand-off + brownfield-parse note verbatim there)
- Wave MASTER: `agentic_orchestration/dispatches/2026-06-22-pathb-1a-loadout-widening-MASTER.md`
- Path B spec §3.0/§3/§3.1, §4, §15; decisions-log Path B supersession entry (engine `dafcd99`)
- ADR-004 (MIGRATION); engineering-disciplines #1, #2, #11, #12

## References
- rocket Gate-2: 1a findings (`e2413ef`); rocket commit `14ee022`, tag `rocket/v-pathb-1a-loadout-schema`
- Code anchors: `serialize_loadout` (10 keys, empties→null), `balance_loop.py` / `recorder.py` (opaque-TEXT pass-through), the `loadout_json` / `player_loadout` export sites
