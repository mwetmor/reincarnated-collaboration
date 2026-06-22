# Dispatch — 2026-06-22 — star-lord — proxy realized-damage telemetry (`proxy_realized_damage_dealt`)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-22 — proxy-combat BUILD authorized (`agentic_orchestration/2026-06-21-proxy-combat-decision-packet.md` §3; telemetry is the alongside-wave on the dependency table).
**No Gate-1** (operational pipeline, not a sim wave — per Matt's gate plan, only SIM waves take mandated Gate-1). **Normal Gate-2 chain** (jack-ryan DEV-MODE) before this is considered landed.
**Estimated effort:** ~½ wave (one additive field on a live producer contract). **Depends on:** gamora W2 (`gamora/v-proxy-W2-realized-damage-1`, commit `a84a395`, Gate-2 PASS — finding `agentic_orchestration/qa/findings/2026-06-22-proxy-W2-gate2.md`). The producer path is LANDED; you add the observer.

> **Parent MASTER:** `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`. Read it for the full guard set + gate plan.

## Acceptance
The realized-proxy-damage producer path gamora wired in W2 is OBSERVED: add `proxy_realized_damage_dealt` as an additive per-fight field reading the producer contract gamora documented. **Brownfield-safe — 0.0 on every production row TODAY** (`proxy_decls` is always `[]` on real kits; `_positioned_allies` empty → field reads 0.0), so no existing-consumer value shifts. The field instruments the path W3 (gamora + gandalf) then calibrates against.

## Required reading before starting
1. **YOUR producer contract** — gamora's MIGRATION v1.82, the authority for this field: `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §"v1.82 — Proxy-combat WAVE 2" → §(a) PRODUCER CONTRACT.
2. gamora W2 Gate-2 finding (the producer path verified clean; the cross-seam note that this needs NO pre-telemetry-wave Matt flag): `agentic_orchestration/qa/findings/2026-06-22-proxy-W2-gate2.md`
3. W2 dispatch (the wave you instrument): `agentic_orchestration/dispatches/2026-06-22-gamora-proxy-W2-realized-damage.md`
4. Parent MASTER (guards + not-unlocked fences): `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`
5. The v1.81 precedent (the typed-death telemetry field you added one wave back — same additive pattern): `agentic_orchestration/dispatches/2026-06-21-star-lord-typed-threat-telemetry.md`

## The producer contract (verbatim from gamora v1.82 §(a) — do NOT re-derive)
```
proxy_realized_damage_dealt = Σ over engine._positioned_allies of ally.delivered_damage_dealt
```
- `delivered_damage_dealt` is the V2 overkill-clamped DELIVERED measure (`spatial_engine.py:1476`) — the honest "damage that actually removed boss/mob HP," parallel to the player's measure.
- **0.0 in solo** (`_positioned_allies == []`) — brownfield-safe; pre-W2 rows / solo fights read 0.0.
- NOT a required field — `validate()` must NOT enforce it.

## Scope
- [ ] **Add `proxy_realized_damage_dealt`** reading the v1.82 producer contract. Wire it the same way you wired the v1.81 typed-death field one wave back.
- [ ] **SEMANTIC SHIFT — `player_damage_total` (Discipline #12, gamora flagged).** `SpatialFightResult.player_damage_total` (`spatial_telemetry.py:302`) is documented "player + ALL proxies (proxy term structurally 0)". W2 makes that proxy term non-zero whenever a fighting `proxy_decls` is present (always `[]` on real kits today, so production unchanged — but the path is live). **gamora RECOMMENDS option (a): keep `player_damage_total` player-ONLY and add `proxy_realized_damage_dealt` as the separate army term** (preserves the existing field's meaning; mirrors the `delivered_damage_dealt` split precedent; no existing-consumer value shifts). jack-ryan Gate-2 endorsed (a) as brownfield-safe. **The export-column-vs-internal-only call is explicitly YOUR lane** — option (a) is the recommendation, not a mandate; if you disagree, document the alternative in MIGRATION and flag it.
- [ ] **Export-column vs internal-to-seam decision (YOUR call).** Per the Wave A2 precedent (`mean_active_proxy_count` / `mean_proxy_contribution_pct` are NOT in the SQLite positional `_INSERT_SQL` — only the 8-tuple bc_cell exports), this is LIKELY a same-pattern additive per-fight field, NOT a new export column / DB schema change. Make the determination and document it. If it IS a DB schema change (new `_INSERT_SQL` column / migration), that is a separate Matt-gated DB-apply — do NOT apply a migration in this dispatch; author it and flag for Matt the way the typed-death `_V2_19` migration was apply-gated.
- [ ] **MIGRATION.md** (star-lord side, ADR-004) — record your consumer decision against gamora's v1.82 producer contract (which option you took, export-column-or-internal, and whether any DB migration is authored-but-held).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `star-lord/v-proxy-realized-damage-telemetry-N`

## NON-NEGOTIABLE GUARDS (from MASTER)
- **No existing-consumer value shift** — the whole field is 0.0 on production rows today; do NOT touch `player_damage_total`'s player-only meaning (option (a)). The shipped solo/production instrument must not move.
- **No content emission** — `_DEFERRED_PROXY_BINS` stays deferred; you observe a path, you do not emit a proxy kit. You test against an injected fixture the way gamora's W2 spike did, NOT a real kit.
- **No DB migration APPLY without Matt** — if the field needs a new DB column, author the migration and HOLD it (apply is a separate Matt-gated step, per the typed-death `_V2_17/_V2_18/_V2_19` precedent). The default expectation (Wave A2 precedent) is internal-to-seam, no migration.
- **Push HELD** — auto-commit your work-products; do NOT push (Mac per-cycle Matt-ask; wave-B push not yet authorized).
- **G-COUNT≠CONTRIBUTION** — `proxy_realized_damage_dealt` (the realized fight) is a DISTINCT instrument from the cancelled `mean_proxy_contribution_pct` COUNT/contribution selector. Do not conflate them; do not revive the contribution-selector.

## Out of scope (explicit non-goals)
- **Any sim-side change** — the producer path is gamora's, LANDED in W2. You add the observer only.
- **Calibration / W3** — you instrument the path; gamora + gandalf calibrate magnitudes against the instrument in W3. The WR=1.000 / delivered=60000.0 W2 fixture numbers are a LOAD-BEARING proof, NOT a calibration baseline — do not bake them into any band.
- **DB migration APPLY** — author-and-hold only if needed; apply is Matt-gated.
- **G3 (Beast-Taming)** — separable, not built.

## Disciplines
#1 math-before-code (the field is a documented sum — cite the producer locations), #11 empirical inspection (prove the field reads non-zero against an injected fixture with a fighting `proxy_decls` AND reads 0.0 on solo / a real kit), #12 semantic-shift (the `player_damage_total` shift above — declare your option (a)/(b) choice).

## Report back to knight-rider
The field added + how it reads the v1.82 producer contract, your option (a)/(b) decision on `player_damage_total`, your export-column-vs-internal-to-seam determination (and whether any DB migration is authored-and-held), empirical proof (non-zero on fixture, 0.0 on solo/real kit), the MIGRATION entry, the tag, and confirmation push is HELD + no content emitted + no migration applied. Flag anything that changes what W3 can observe. This goes through jack-ryan Gate-2.

---

## Completion record

**Completed:** 2026-06-22
**Tag:** `star-lord/v-proxy-realized-damage-telemetry-1` (engine commit `4dd8fd5`)
**Status:** ALL SCOPE ITEMS COMPLETE — 70/70 tests PASS; push HELD per ADR-006; no content emitted; no migration applied.

### The field + how it reads the producer contract

`SpatialFightResult.proxy_realized_damage_dealt: float = 0.0` added to
`simulation/spatial_gauntlet/spatial_telemetry.py`. Wired in `spatial_engine.py` result
construction (the site that already writes `player_damage_total=self.player.delivered_damage_dealt`):

```python
proxy_realized_damage_dealt=sum(
    a.delivered_damage_dealt for a in self._positioned_allies
),
```

Producer contract (simulation/MIGRATION.md §v1.82 §(a) — verbatim):
```
proxy_realized_damage_dealt = Σ over engine._positioned_allies of ally.delivered_damage_dealt
```
`delivered_damage_dealt` confirmed on `SpatialEntity` at build time (`spatial_engine.py` line ~644,
accumulated by `_apply_skill_damage` at line ~1527 for any attacker). `_positioned_allies` is `[]`
in solo → sum is 0.0. Producer citation matches: the ally is just another attacker through the same
damage path the player uses. Contract reads directly; no re-derivation.

### Option (a)/(b) decision

**OPTION (a) CHOSEN** — `player_damage_total` stays player-ONLY (`self.player.delivered_damage_dealt`).
`proxy_realized_damage_dealt` is the separate army term. Rationale:
1. `player_damage_total` already correctly reads only the player entity — option (a) requires zero
   change to its writer (the engine was already correct; only the docstring needed updating).
2. No existing-consumer value shifts: production `proxy_decls` always `[]` → `_positioned_allies == []`
   → proxy sum is 0.0 on all real rows today regardless of which option is chosen.
3. Mirrors the `delivered_damage_dealt` split: each `SpatialEntity.delivered_damage_dealt` is
   per-attacker at the entity level — option (a) preserves that split at the result level exactly.
4. jack-ryan Gate-2 endorsed (a) as brownfield-safe.

### Export-column-vs-internal-to-seam determination

**INTERNAL-TO-SEAM** — no new DB column, no `_INSERT_SQL` change, no migration authored or applied.
Determination rationale:
1. Wave A2 precedent: `mean_active_proxy_count` / `mean_proxy_contribution_pct` are not in the
   SQLite positional `_INSERT_SQL` — proxy per-fight scalars stay internal.
2. W3 consumer path: gamora + gandalf calibration reads `SpatialFightResult` directly from the
   engine at fight-result time, not from the DB — no DB round-trip needed.
3. Matt ADR-006 DB-apply gate is NOT triggered; no new standing gate opened.

An `ExportProxyRealizedDamageTelemetry` schema + `build_proxy_realized_damage_telemetry()` factory
were added to `export/schemas.py` as a validation-artifact boundary (same pattern as
`ExportTypedDeathTelemetry` from v1.81) — not an emission gate.

### Empirical proof (Discipline #11)

| Case | proxy_realized_damage_dealt | player_damage_total | Result |
|---|---|---|---|
| Injected fixture (60000.0 — gamora W2 spike value) | 60000.0 on SpatialFightResult | 0.0 (player-only, unchanged) | **PASS — NON-ZERO** |
| Solo (no override — default 0.0) | 0.0 | player-only | **PASS — 0.0** |
| Real-kit-like (player_damage_total=12345.0, no proxy) | 0.0 | 12345.0 (unchanged) | **PASS — 0.0** |
| Option (a) guard (both fields set) | 60000.0 | 5000.0 (unchanged) | **PASS — no bleed** |
| Pre-W2 result (no field on object) | 0.0 via getattr default | — | **PASS — brownfield-safe** |
| validate() not enforced | no raise | — | **PASS — not required** |

### MIGRATION entry

`export/MIGRATION.md §v1.82` authored and prepended. Covers:
- Option (a) semantic-shift decision with rationale
- Internal-to-seam determination with rationale
- Consumer obligations table (drax: none; gamora W3: read new field; gandalf W3: same)
- Empirical proof table
- Clear statement: no migration authored, held, or applied

### Guards confirmation

- **Push HELD** — auto-committed `4dd8fd5`; NOT pushed (Mac per-cycle Matt-ask).
- **No content emitted** — `_DEFERRED_PROXY_BINS` stays deferred; tested against injected fixture only; no real kit emitted.
- **No migration applied** — internal-to-seam determination; no `ALTER TABLE`; Matt ADR-006 gate not triggered.
- **G-COUNT≠CONTRIBUTION** — `proxy_realized_damage_dealt` (realized fight) is distinct from cancelled `mean_proxy_contribution_pct`; not conflated, not revived.
- **validate() not enforced** — confirmed by test `test_proxy_realized_damage_not_enforced_by_validate`.
- **Additive only** — 59 prior tests all pass; no field renamed/removed; 0 regressions.

### What W3 can observe

W3 (gamora + gandalf calibration) can read `SpatialFightResult.proxy_realized_damage_dealt` directly
from the engine at fight-result time. No further star-lord action is required for W3 to observe the
field — it's live at fight-result time in every `SpatialFightEngine.run()` call. On all real kits
(proxy_decls always []) the field reads 0.0 — exactly the solo baseline W3 calibrates against. On an
injected fighting fixture, it reads the army's realized damage total (60000.0 in the W2 spike).

Nothing changes what W3 can observe relative to the dispatch's scope. The field is a clean additive
observer on the producer gamora landed in W2.

**Goes through jack-ryan Gate-2 (DEV-MODE) before W3 chains.**
