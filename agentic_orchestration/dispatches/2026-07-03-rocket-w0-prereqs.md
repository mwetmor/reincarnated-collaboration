# Dispatch — 2026-07-03 — rocket — W0 prereqs (DEMO-READINESS UNATTENDED RUN)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-07-03 (run fire authorized; spec §1-C emission-exercise authorization)
**Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** (Gate-1 ✓ passed + folded). Cite it; do not re-derive scope from this dispatch.
**Estimated effort:** one focused session
**gates-on:** — *(W0 root; parallelizable with gamora + star-lord W0)*
**Failure policy:** spec §7 — halt-loud; never silent-skip.

## Context

The demo-readiness unattended run (W0→W4) makes engine + emission pipeline 100% demo-ready before any demo work opens. W0 is the prereq wave. Your five spec items + one KR scope-pin + one pulled-early precondition are below. Everything downstream (W2 pairing, W3 emission) gates on your returns.

## Required reading before starting

- `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` v1.1 — §1, §2 (G1/G2/G4), §3 W0, §5, §7, §10
- `canonical/reap-die-rise-engine/proxy-pairing-q6-q7-2026-07-02.md` v2 (RATIFIED) — the partition your classifier implements
- `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3 — the ratified family; F-f context
- Engine decisions-log latest entries (commit `a10a695` — G1–G10 + proxy-T4 + Q6/Q7 registrations)

## Math-before-code

- Composition-knob weighting math (what generation-side weight produces ~25% proxy-dominant emission) — a short math note per Disc #1/#1.2 before implementing. The target STEERS generation; it does not hard-gate emission (spec §5).

## Cross-seam contract change? (Principle 6 gate)

The classifier output (proxy_type→family) is consumed by gamora in W2; the composition knob shapes what star-lord's W3 emission draws. If any EMITTED shape changes (bundle/loadout dict keys), MIGRATION.md before tag. If changes are generation-internal only, state so explicitly in the completion record.
**Round-trip smoke:** required only if an emitted dict shape changes; otherwise `Round-trip: not applicable — generation-internal` with the explicit reason.

## Scope

- [ ] **Proxy composition knob** (spec §3 W0 + §5): generation-side weighting for the ~25% proxy-dominant target. Mechanism is yours: bin weights and/or proxy-skill weighting across the caster family. `gates-on: —` *(feeds W3 + §5 hypothesis test)*
- [ ] **2-type proxy-decl check** (spec §3 W0): verify generation can EMIT exactly-2 cross-family proxy decls, or CONVERGENCE kits cannot exist in the run. If it cannot: **file loud as a named gap in the completion record — no silent skip.** `gates-on: —` *(feeds W2)*
- [ ] **CONVERGENCE cert fixture** (spec §3 W0): the 2-summon-skill kit as **FIXTURE only** — zero-hand-authored-content rule: it never ships; shipping CONVERGENCE kits come from the W3 emission. `gates-on: —` *(feeds W2)*
- [ ] **proxy_type→family classifier** (spec §3 W0): 14 types → 6 families per the ratified pairing-spec partition. Phase-3 residual. `gates-on: —` *(feeds W2)*
- [ ] **F-f enforcement consumer** (KR scope-pin from spec §3 W0 "B4 prereq re-scope" row, per MASTER-board B1 closeout: this half is rocket-owned): `FAMILY_MAX_ONE` is currently inert data — build the live chain-builder consumer so GEOMETRY/DEFENSE max-1 is ENFORCED at emission. `gates-on: —` *(hard prereq for W3)*
- [ ] **Singleton-config smoke — GREEN** (spec §7, Gate-1 #2; precondition 3 pulled early by KR): Phase-1 η members live (ASCENSION / SOVEREIGNTY / FISSION / ZONE_CONTROL), CONVERGENCE + DUAL_PROXY η-gated to 0.0 — **verify this is an executable state and smoke it green now**, so W3 can fire regardless of W2 state. Report the smoke artifact path. `gates-on: —` *(hard precondition for W3)*
- [ ] Smoke-test passes (Disc #2; scaling rehearsal per #2.1 where applicable)
- [ ] MIGRATION.md if cross-seam impact
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v-demo-run-w0-1`

## Quality criterion (OP §3.11)

**Game-quality goal this dispatch serves:** the demo roster is emitted from a REAL pipeline in which summoners are first-class citizens (~25% share, G4) and pairing-capable generation exists — so Matt curates from abundance, not scarcity (G7: "the more kits emitted in band with passing KPM, the more options").

**Refutation conditions** (surface before executing if any apply):
- This dispatch contradicts the ratified pairing spec's partition or the proxy-T4 spec v3
- An alternative mechanism serves the ~25% target better than the one you'd default to — name it in the math note
- Acceptance can pass without advancing emission-readiness (e.g., a knob that exists but demonstrably can't steer)
- Any item's framing pre-commits to a decision Matt has not ratified
- A scaffold value is introduced without a pending-decision flag (#40)

## Acceptance criteria

- [ ] Composition knob implemented + math note committed; smoke shows the knob shifts proxy-bin draw share in the intended direction
- [ ] 2-type decl check: PASS (evidence: an emitted candidate with exactly-2 cross-family decls) OR loud named gap filed
- [ ] CONVERGENCE fixture exists, marked FIXTURE/never-ships
- [ ] Classifier maps all 14 types to the 6 ratified families; unit-tested
- [ ] F-f consumer live: a chain that would violate FAMILY_MAX_ONE is rejected in test
- [ ] Singleton-config smoke GREEN with artifact path reported
- [ ] Round-trip clause satisfied (smoke or explicit not-applicable)

## Out of scope (explicit non-goals)

- CONVERGENCE/DUAL_PROXY strategy classes themselves (W2, separate Gate-1-gated dispatch)
- The emission run (W3) · un-gating `_DEFERRED_PROXY_BINS` (W3 step 1)
- Precise proxy-share fine-tuning (launch — spec §10)
- PROXY_INVERSION (deferred-by-ruling)
- Any demo/Q7/Q8/slice work

## References

- Spec §11 Gate-1 record · engine `a10a695` (batched rulings registration) · B1-REBASE closeout (`40e351e`/`67fc0a9`) · MASTER board B1 row (F-f finding provenance)
