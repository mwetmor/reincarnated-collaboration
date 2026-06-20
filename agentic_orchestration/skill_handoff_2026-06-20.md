# Skill Handoff — 2026-06-20

**Author:** knight-rider
**Prior handoff:** `skill_handoff_2026-06-19.md`

## Instrument-validity workstream — DROVE Phases 1-4 to completion; HALTED at the Phase-R/Phase-5 wall (Matt decision)

Autonomous orchestration run driving the gandalf-authored instrument-validity workstream (`gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md`). Four instrument defects on the combat damage equation, each fixed and **measured in isolation against the standing (untouched) bands**; bands refit ONCE at Phase 5 against the composed instrument; then the first honest STR-lever read at Phase 6.

### Phases 1-4 — COMPLETE, all Gate-2 PASS-WITH-INFO (gamora implement, jack-ryan gate)

| Phase | Fix | Result | Tag | Gate-2 |
|---|---|---|---|---|
| **1** | Resource-economy wiring (gate + decrement + energy_type-branched pool, ported from kernel `_ENERGY_CONFIGS`) | G2 auto-resolve: KPM flat-not-rising (gate correct but inert until Phase 2 fires expensive tiers); flag `WIRE_RESOURCE_ECONOMY`, OFF=byte-identical | `gamora/v-resource-economy-phase1-1` (engine `c28d027`) | PASS-WITH-INFO |
| **2** | Rotation selector (energy_type-branched build-vs-spend; FULL branch set built) | G3a PASS: T1-collapse BROKEN (100% T1 → 53.9% T1 / 46.1% T4 burst→lull); G3b (rage falsifier) BUILT-but-UNMEASURED (false-PASS guard held) | `gamora/v-rotation-selector-phase2-1` (engine `e2f3929`) | PASS-WITH-INFO |
| **3** | DoT activation + physical-DoT scaling (F1/F2 pre-committed `e537b29`; + NEW F3-DEFECT fix) | G4 auto-resolve: STR bleed now >0 (`dot_dps=0.10`); per-tick symmetry holds (STR 1.24 / INT 1.27); realized gap is throttle-driven not magnitude | `gamora/v-dot-activation-phase3-1` (engine `9e1d25d`) | PASS-WITH-INFO |
| **4** | Armor/resist symmetry (Path-B `from_monster` off-element floored to armor curve) | G5 auto-resolve: caster boss-survive fell toward martial (int boss KPM 98.96→0.73); martial unchanged (str Δ=0.000 every shell); no over-correction; flag `MITIGATION_SYMMETRY` | `gamora/v-armor-resist-symmetry-phase4-1` (engine `d2d3dde`) | PASS-WITH-INFO |

**Disciplines held throughout:** math-note-first (#1), recompose-first (PORT not BUILD — no new mechanic in any phase), measure-ISOLATED (bands UNTOUCHED in 1-4; `bands_untouched:true` verified each gate), fresh disjoint seed bases per phase (820000 / 8.5M / 16M / 24M), semantic-shift declared at all four boundaries (#12 — jack-ryan confirms the four-boundary chain is assembled + coherent), no production-gate regression. All commits local on `main`; **NOT pushed** (Matt-gated, ADR-006).

**New mechanism bug found + fixed in-phase (Phase 3, recompose-first):** `_add_or_refresh` let the ~22×-more-frequent zero-tick T1 bleed clobber the live T4 bleed (tick=5) to zero — a second, independent zeroing mechanism distinct from the SESSION-31 selector collapse. Fix: DoT refresh keeps MAX tick_damage (faithful ARPG rule, scoped to DoT-only). jack-ryan ruled SOUND. Routed gamora→re-gate→proceed per the autonomy envelope; did NOT go to Matt.

### THE SCOPE SURPRISE — Phase R (rocket reference-economy hardening) — AWAITING MATT SCOPE AUTHORIZATION

**What gamora found at Phase-1 G1 (verified first-hand by gamora + gandalf):** the *generated population* never carries the doc-48 economies. Generation infers resource type from BC-tempo (`_BC_TEMPO_TO_RESOURCE`) → `{cooldown, energy, mana}`, all collapsing to mana-default. The doc-48 per-class economies never reach the spatial layer. **The Barbarian-rage build-spend lever — the entire hinge of the Phase-6 STR read — is absent from the population.** Phase 2 corroborated empirically: STR throttles (2.2× vs casters 16-40×) purely because it borrows the wrong economy.

**gandalf ruled** (`gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`): (a) the rocket change is REQUIRED — Phase 6 on mana-default is a null instrument; (b) new **Phase R**, parallel to 1-4, **hard-prerequisite to Phase 5** (doc-48 economies move KPM → refitting before they exist forces a second refit, violating the one-refit discipline); (c) Phases 2/3/4 proceed now (done); (d) recompose-first PORT-not-BUILD with one guard (bc_target round-trip must thread); (e) G1 mapping HOLDS (the finding revised an implicit assumption beneath the table, not the table). **If Matt declines Phase R → Phase 6 is HELD, not run** (no honest STR read without the economies in the population). G3 split: G3a gated now; G3b re-arms post-Phase-R.

**Ready-to-fire draft dispatch authored:** `dispatches/2026-06-20-rocket-phaseR-reference-economy-hardening-DRAFT.md` (marked DO-NOT-FIRE-until-Matt-authorizes).

### OPEN MATT DECISIONS (the halt wall — both land here)
1. **Phase R scope authorization** (halt-point 3, scope surprise): authorize rocket reference-economy hardening, OR accept Phase 6 STR read is HELD/deferred and Phase 5 refits as explicitly mana-default-only-scoped. No third path runs Phase 6 honestly.
2. **Phase 5 band approval** (halt-point 1): the composed re-baseline produces new bands → jack-ryan structural Gate-2 (G6, BLOCK authority) → Matt decisions-log decision. Gated on #1 (refit on the full-economy population requires Phase R first).

### Hand-back chain if Matt authorizes Phase R
rocket Phase R (doc-48 economies into population) → jack-ryan Gate-2 → gamora re-arms G3b (rage branch materializes on real rage entity) → Phase 5 composed re-baseline (gamora + jack-ryan G6) → Matt band approval → Phase 6 STR fires its rage economy + bleed lever → gandalf rules O1-O4 → feeds the (A)-vs-(B) skill investigation.

### Carryover / standing items
- **60 pre-existing test failures** (rocket-seam config drift: 5-element vs 7-substrate `season_emit`; + star-lord LLM auth; + cycle12 convergence shape) — verified identical on the clean baseline, NOT introduced by this workstream. Relevant if Phase R authorizes rocket work (rocket should be aware of the drift).
- Crypt-Vault Node PoC (2026-06-19 handoff): drax dispatch still awaiting drax session launch (Pattern B, needs open Godot editor) — untouched this session.

### Push gate
All instrument-validity commits (Phases 1-4 engine tags + collab results + qa findings + dispatches + this handoff) are local on `main`, NOT pushed. Awaiting Matt push authorization (ADR-006).
