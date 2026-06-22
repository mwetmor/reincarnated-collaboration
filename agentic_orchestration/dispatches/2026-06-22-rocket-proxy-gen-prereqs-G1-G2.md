# Dispatch — 2026-06-22 — rocket — proxy generation prereqs (G1 + G2)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-22 — proxy-combat BUILD authorized.
**Estimated effort:** ~1.5 waves (the first-class generation prerequisite — NOT folded into calibration).
**Concurrent** with gamora W1 (which is independent of your output). You are the LONG POLE: W2 (gamora realized-damage) cannot test a fighting proxy until you emit one, so land G1/G2 first-or-concurrent with the sim waves.

> **Parent MASTER:** `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`. Read it for the full guard set + gate plan.

## Acceptance
The gen→sim proxy seam is SOLDERED in the middle: generation emits a `proxies` stat-surface into the exported class JSON, and a vocabulary-bridge translates gen-speak → sim-speak so a fighting proxy is fully specified end-to-end. Today `grep -rl '"proxies"' exports/` = 0 — the dict the spec says generation will "emit into" does not exist. You build it.

## Required reading before starting
1. Gen-side build spec (THIS IS YOUR SPEC): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-gen-addendum-2026-06-21.md`
2. Sim-side spec (the consumer contract you emit toward): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-2026-06-21.md`
3. T2.2 Gate-1 scope-honesty concern (why G1/G2 is first-class, not invisible): `agentic_orchestration/qa/findings/2026-06-21-t2.2-proxy-combat-gate1-design.md`
4. Parent MASTER (guards + not-unlocked fences): `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`

## Scope
- [ ] **G1 — proxy vocabulary-bridge (gen→sim translator).** Gen speaks `proxy_power_per` / `proxy_geometry` / `proxy_max_active`; sim speaks `damage_multiplier` / `base_hp` / `range_m`. **No translator exists.** Build the translation layer so a gen-emitted proxy is consumable by the sim's realized-entity loop.
- [ ] **G2 — proxy stat-surfaces.** Emit (all net-new; no `proxies` key in any exported class JSON today): `base_hp`, fighting-proxy `damage_multiplier`, `proxy_max_active` setting-mechanism, geometry→`range_m` map.
- [ ] MIGRATION.md (rocket↔gamora gen→sim boundary, ADR-004) — the `proxies` surface is a NEW cross-seam interface; document the contract so W2 can consume it.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `rocket/v-proxy-gen-prereqs-N`

## Cross-seam contract change (Principle 6 — YES)
You CREATE the `proxies` stat-surface that gamora W2 consumes. MIGRATION.md is REQUIRED (the seam was specified at both ends, never soldered — you solder it). The round-trip is W2's job (gamora tests a fighting proxy against your emitted surface); your job is to make the surface real + documented so W2 has something to consume.

## NON-NEGOTIABLE GUARDS (from MASTER)
- **No content emission** — `_DEFERRED_PROXY_BINS` stays deferred; the 25% proxy emission stays Matt-gated. You build the GENERATION MACHINERY (vocabulary + stat-surface), you do NOT un-defer the bin or emit a proxy kit into a season.
- **Push HELD** — auto-commit your work-products; do NOT push (Mac per-cycle Matt-ask).
- **Extension-not-fork** — minimal-change path; no autonomous-AI design.

## Out of scope (explicit non-goals)
- **G3 (Beast-Taming mob-capturable tag + tamed-proxy stat inheritance)** — SEPARABLE per packet §3, the heaviest single net-new item, NOT a hard prereq for the core. Do NOT build it in this dispatch.
- The `_DEFERRED_PROXY_BINS` lift / 25% emission (Matt-reserved, separate).
- Any sim-side change (gamora's lane).

## Open questions for you to resolve (and document)
- Exact shape of the `proxies` key in the exported class JSON (your call at build, per the gen addendum spec) — document it in MIGRATION.md so W2 consumes the real shape, not a guess.
- The geometry→`range_m` map: which proxy geometries map to which sim range bands.

## References
- Disciplines: #1 math-before-code (if any magnitude/translation constant), #11 empirical inspection, #12 semantic-shift, #2 smoke-test.
- Coordinating MASTER: `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`

## Report back to knight-rider
The `proxies` surface shape (the exact JSON key contract), the vocabulary-bridge translation table (gen-term → sim-term), the MIGRATION.md entry, the tag, and confirmation no bin was un-deferred / no kit emitted. Flag anything that changes what W2 can assume about the emitted surface.
