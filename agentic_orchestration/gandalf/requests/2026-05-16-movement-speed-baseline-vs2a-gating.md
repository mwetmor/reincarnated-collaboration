# Request to knight-rider — Movement-Speed Baseline (VS2a gating)

**From:** gandalf
**To:** knight-rider (to author dispatches per ADR-002)
**Date:** 2026-05-16 (Day 4)
**Priority:** **HIGH — VS2a SHIP GATE.** Matt directive: *"I don't want to ship demo VS2a without this."* Demo VS2a does not ship until the movement-speed baseline locked in `canonical/story/movement-speed-baseline.md` is implemented in the demo and named in the engine-emitted schema.
**Type:** Cross-seam commission + roadmap amendment + decisions-log entry draft request.

---

## Approval trail

Matt directed this commission directly in 2026-05-16 dialogue:

> *"Ok, I don't want to ship demo VS2a without this. Please update all documents pass out memos as needed. BTW, what I do not see here is a mathematical expression of move speed. This is all percentages. I want the actual per tile movement speed for the player to be exactly set on the Tier 1 ARPG AVG dimension. We may use different tile sizes, or not use tiles at all.. I'm not sure how we will measure it, but we need a way to decipher this exact speed of the character combatant to bring it to life in the demo."*

Gandalf authored the canonical baseline doc in response. This commission operationalizes it.

**Reverses prior deferral:** `canonical/16-project-roadmap.md` § VS2a "Out of scope" — *"B12 (movement speed / boots / gear slot audit) — defers; not visually load-bearing for VS2a."* A scoped subset of B12 (the baseline anchor specifically; not full gear-slot audit) is now in VS2a scope.

**Supersedes prior deferral:** `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b ("schedule-or-defer per Matt"). Matt has chosen schedule.

---

## What knight-rider needs to do

### Track 1 — Dispatches (author NOW; sequence per dependency chain)

**Dispatch A — rocket (schema): `movement_speed` field addition**
- Add `movement_speed` field to class-template + monster-tier JSON exports
- Unit: meters per second (m/s), float, 2-decimal precision
- **Default class value: 5.75 m/s** (Matt-locked 2026-05-16)
- **Default monster trash value: 5.75 m/s** (parity per genre convention; Matt-locked)
- Fast-archetype monster tier values: 6.6–7.5 m/s; specific values are gamora design-call but schema must support them
- Estimated lift: ~1-2 hours rocket; no co-dependency with anything else
- **Sequence: FIRST** (drax demo consumes this; can hardcode the constant pending schema if rocket slips)

**Dispatch B — drax (demo): movement-speed-baseline implementation**
- File to modify: `reincarnated-demo/src/world/movement.ts`
- Replace `MOVE_SPEED: { close, medium, long }` lookup with single `MOVE_SPEED_BASE` constant (or per-class read from engine data once schema lands)
- **Add `PIXELS_PER_METER = 48` constant** (Matt-locked 2026-05-16; standard ARPG isometric convention)
- Replace `speedForProfile(profile)` with `playerMoveSpeed(combatant)` reading from engine data when available; signature drops the `range_profile` parameter dependency
- **Re-derive `AI_SPEED_MULTIPLIER` from design intent: 0.767 for VS2a mid-game-equivalent gauntlet** (player at 7.5 m/s mid; trash at 5.75 m/s base)
- **Verify arena scale**: back-derive what current demo px/s values represent in m/s against `arena.ts` ellipse dimensions; report the magnitude of perceived feel-change the rebase to 48 px/m produces (no-op vs near-2× speed-up depending on current implicit scale)
- Re-validate AI engagement distances + chase margin against new baseline
- Re-run playtest cycle equivalent to phase 6.1/6.2 calibration against new values
- Update phase-6.x calibration comments to reference `canonical/story/movement-speed-baseline.md`
- Estimated lift: ~1-2 days drax (mostly re-tuning + playtest validation)
- **Sequence: SECOND** (depends on rocket schema; or hardcode pending schema)
- Drax bandwidth note: currently most-loaded seam per roadmap risk-1; this dispatch adds ~1-2 days to existing VS2a load

**Concrete locked px/s values for `world/movement.ts` (at PIXELS_PER_METER = 48):**

| Stage | m/s | px/s |
|---|---|---|
| Base | 5.75 | 276 |
| Early game | 6.0 | 288 |
| Mid game (VS2a target) | 7.5 | 360 |
| Late game | 8.0 | 384 |
| AI trash (player base × AI_SPEED_MULTIPLIER 0.767) | 5.75 × 0.767 = 4.41 m/s at mid; in absolute terms AI moves at 5.75 m/s (276 px/s) when player at 7.5 m/s mid | 276 |

**Note on AI semantics:** AI_SPEED_MULTIPLIER 0.767 is computed against the player's *current effective MS*, not against base. So at mid-game (player 7.5 m/s effective), AI moves at 7.5 × 0.767 = 5.75 m/s — which equals monster trash base. This makes the math self-consistent: AI multiplier expresses "trash base ÷ player effective" at the gauntlet's intended balance point. If gauntlet shifts to a different balance point in future tuning, the multiplier shifts.

**Dispatch C — gamora (sim): Gate 3b sim consumption (tightly-following, not VS2a-gating)**
- Per `engine-balance-stewardship.md` § Gate 3 Recommendation 3b in full
- Extend `fight_engine.py` with per-tick movement-speed-driven distance updates
- Replace binary at_melee_range with 3-band distance state (melee / near / mid)
- Enable basic kiting modeling for single-target archetypes
- Estimated lift: ~1.5-2 weeks gamora
- **Sequence: POST-VS2a tight follow** — does not gate VS2a ship, BUT closes the schema-emit-without-consumer drift (a P5 pattern jack-ryan will flag if left unactioned). Target ship within 2-4 weeks of VS2a.
- Already on gamora's `AGENT_STATE.md` as Stage A2 movement-speed sim extension (engine-balance-stewardship lock 3b); this commission re-affirms with VS2a context

**Dispatch D — star-lord (telemetry, optional minor): observed-MS emission**
- Add per-fight observed player MS to telemetry schema
- Enables post-hoc validation of design baseline against gameplay
- Estimated lift: ~1 hour
- **Sequence: any time before VS2a ship + first playtest cycle**

### Track 2 — Decisions-log entry (draft NOW; surface for Matt approval before drax begins)

Per ADR-001, this is a Matt-decision. Decisions-log entry should land **before drax begins implementation**, not after. Suggested entry shape:

**Title:** *Movement-speed baseline locked at Tier-1 ARPG average — excluding PoE 1 outlier (5.75 m/s base; early/mid/late curve 6.0/7.5/8.0 m/s; continuous m/s; 48 px/m demo scale; no range-profile variance)*

**Decision (Matt-locked 2026-05-16):**
- Player base MS: **5.75 m/s** (rounded from precise 5.7275)
- Early/mid/late effective MS: **6.0 / 7.5 / 8.0 m/s** (late excludes PoE 1 outlier)
- Monster trash MS: **5.75 m/s** (parity with player base, per genre convention)
- Fast-archetype monster MS: **6.6–7.5 m/s** (~10–15% of monster mix; specific values gamora design-call)
- Measurement: **continuous m/s** (not tile-based) at engine + sim layer; demo derives px/s via `PIXELS_PER_METER = 48` art-scale constant
- Range-profile MS variance: **dropped** per genre convention; mobility identity via ability design (B11 / B13)
- Late-game value: **excludes PoE 1 outlier** per Matt (Reincarnated lands in D3/D4/Last-Epoch design family, not PoE-1 zoom-zoom)
- AI_SPEED_MULTIPLIER (demo, VS2a): **0.767** (derived from monster trash ÷ player mid-game = 5.75/7.5)

**Rationale:** see `canonical/story/movement-speed-baseline.md` § "The Tier-1 ARPG average — math fully exposed" + § "Why this doc exists (and why now, not later)"

**Reference doc:** `canonical/story/movement-speed-baseline.md`

**Supersedes:**
- Prior roadmap deferral of B12 out of VS2a (scoped subset only; full B12 remains Stage A2)
- Prior engine-balance-stewardship Gate 3 Recommendation 3b "schedule-or-defer per Matt" framing

**Drift instances closed:** Drift-9 (Q2 movement empirically unknown — `drift-audit.md`)

### Track 3 — Roadmap amendment

Update `canonical/16-project-roadmap.md` § VS2a section:

1. **Remove from "Out of scope":** "B12 (movement speed / boots / gear slot audit) — defers; not visually load-bearing for VS2a"
2. **Add to "Scope" list:** "Movement-speed baseline implementation (per `canonical/story/movement-speed-baseline.md`)" — replaces existing demo px/s values with engine-emitted m/s values per Tier-1 ARPG average
3. **Note in "Out of scope":** "Full B12 — gear slots / boots / +% MS affixes / hard-cap design — remains Stage A2; only the baseline anchor lands in VS2a"
4. **Update "Ship trigger":** add "movement-speed baseline implementation validated via playtest cycle against new values"
5. **Add to "Seam allocation" table:** rocket and drax (and gamora for post-VS2a tight-follow row) gain movement-speed-baseline line items
6. **Update Stage A2 entry** for B12: note that "baseline subset shipped in VS2a; gear slot + affix economy remains Stage A2"

### Track 4 — RESOLVED

All 5 open questions resolved by Matt 2026-05-16. Locks baked into Tracks 1-3 above; no further Matt brief required before knight-rider proceeds.

For audit trail, Matt's answers:
1. **Late-game value: exclude PoE 1 outlier** → 8.0 m/s late game
2. **Range-profile MS variance: drop** (genre convention)
3. **Precise vs rounded base: rounded** → 5.75 m/s
4. **PIXELS_PER_METER: 48** (standard ARPG isometric convention)
5. **Decisions-log entry: before drax begins implementation**

### Track 5 — Notify seams

After dispatches authored, notify:
- **drax + rocket + gamora** that dispatches are inbound; coordinate ordering (rocket → drax in series; gamora in parallel post-VS2a)
- **jack-ryan** that decisions-log entry is forthcoming; pre-flag the Gate-2 review
- **star-lord** that the optional telemetry dispatch may follow

---

## Cross-references

- **Canonical baseline doc:** `canonical/story/movement-speed-baseline.md` (authoritative reference for all dispatches)
- **Numeric source:** `agentic_orchestration/research/knowledge/arpg-movement-speed-reference-2026-05-16.md` (Legolas research consumed)
- **Original stewardship framing:** `canonical/story/engine-balance-stewardship.md` § Gate 3 (Recommendation 3b being now operationalized)
- **Roadmap context:** `canonical/16-project-roadmap.md` § VS2a + § B12 + § Stage A2
- **Demo state:** `reincarnated-demo/src/world/movement.ts` (current hand-tuned values being replaced)
- **Engine sim state:** `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` § "Stage A2 movement-speed sim extension"
- **Drift instance closed:** `canonical/story/drift-audit.md` Drift-9

---

## What this commission does NOT do

- Does not lock the full B12 work (gear slots, +% MS affixes, hard-cap design) — those remain Stage A2
- Does not commission B13 (active mobility VFX — dash/charge/blink) — separate Stage A2 item
- Does not amend `style-register.md` or any cipher-substrate work — orthogonal
- Does not amend the form-bias-cadence-strategy — orthogonal
- Does not require new Legolas research — research already filed
- Does not require new elrond work — no catalogue impact

---

— gandalf, 2026-05-16 (Day 4)
