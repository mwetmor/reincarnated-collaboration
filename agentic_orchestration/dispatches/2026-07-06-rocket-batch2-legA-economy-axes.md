# Dispatch — 2026-07-06 — rocket — batch-2 Leg A: economy-axes build (math-first)

**From:** knight-rider
**To:** rocket (with gamora adjacency on sim-consumption binding)
**Approved by:** Matt 2026-07-06 ("Batch-2 authorized... Fire per its §7: Leg A rocket dispatch (economy-axes build, math-first)")
**Estimated effort:** ~4–6h (math-first design + composition rules; NO fire, NO population emit)
**Acceptance:** economy axes defined as composable variation dimensions (mana cost curve, regen curve, throughput/cast-cadence) on INT-band kits, with ranges + composition rules documented math-first, same shape as the landed variation axes; gamora sim-binding adjacency confirms the economy actually binds in fight resolution (not just in declaration); Gate-1 (jack-ryan DESIGN-MODE) rides the axis math before Leg B fires.

## Context

This operationalizes `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §2 (LEG A). Matt ruled **Q1(a): resource-economy joins the variation build as explorable AXES, not a hand-tuned config.** Substrate-led discipline applied to the economy question: *don't tune the caster — let the population vote on what a viable mana economy is.* The population searches economy space; the gauntlet + the C2 plain-caster floor (9.90 open_arena / 11.65 chokepoint, byte-verified `db2df69`) select the viable region.

**Motivating finding (structural-honesty clause):** gamora's Leg-4 read — *"band re-tune alone may be insufficient"* — is the reason economy became an axis. Leg A builds the axes; Leg B tests whether economy space contains a floor-clearing region **at all**. If it does not, the problem is deeper than economy (cast mechanics / damage-vs-trash scaling), and that outcome is a **designed HALT** (spec §3), not a failure of this dispatch. Build the axes honestly; do not pre-bias them toward a floor-clear you cannot yet prove exists.

## Required reading before starting
- `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` — the governing spec (§1 banked inputs, §2 Leg A, §3 the GO/HALT this feeds, §5 provenance law, §8 defaults). Authoritative.
- `reincarnated-engine/src/reincarnated/simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` — the finalized calibration note; §2.3 quantifies the plain-caster band gap that placed the C2 floor.
- `reincarnated-engine/src/reincarnated/simulation/notes/leg4-attribution-report-2026-07-06.md` — the mechanism-CONFIRMED verdict + the chassis finding that motivates the economy axis.
- The **landed variation axes** in your own seam — economy axes must be the **same shape** (axis definitions, ranges, composition rules). Cite the existing variation-axis code as the pattern.
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #24 single-parameter sweep isolation (each economy axis must be independently swept, not confounded), #20 density-based row-duplication prohibition.

## Math-before-code (REQUIRED — this dispatch is math-first; no emit)
Document, before any code:
1. **Axis definitions** — the three economy dimensions as composable variation knobs on INT-band kits:
   - mana **cost curve** (per-cast cost as a function of skill tier / cast index)
   - mana **regen curve** (recovery rate; flat vs ramping vs on-kill)
   - **throughput / cast-cadence** (casts-per-window; the cadence the economy actually sustains)
2. **Ranges** per axis — the span the population searches. Justify each bound. The output of Leg B is a *map*, so the ranges must span a real space (§3 sampling coverage).
3. **Composition rules** — how the three axes compose with each other and with the already-landed variation axes (chain-variants, G4 proxy-share knob). Where economy identity emerges: cheap-sustained vs builder/spender vs flat-cost (the caster-feel read Leg B reports back to Matt either way).
4. **#24 sweep-isolation statement** — confirm each economy axis is independently varied at Leg-B sampling; no confounded pair that would make the map uninterpretable.
5. **Sampling-scheme recommendation for Leg B** (§8 D4 — you + gamora pick at Gate-1): grid vs latin-hypercube-class across the axis ranges. State your recommendation and reasoning; jack-ryan ratifies at Gate-1.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**gamora ADJACENCY required, but NO contract-field change is authored in this dispatch.** The economy axes are generation-side variation dimensions (rocket seam). BUT the axes must **actually bind in fight resolution** — gamora confirms the sim consumes the economy (mana pool depletes, regen ticks, cadence gates casts) rather than the economy living only in kit declaration. If binding the economy requires a new field on the kit→sim loadout dict, **that IS a cross-seam contract change** and MUST be surfaced with a MIGRATION.md note + round-trip smoke at that point — flag it to knight-rider rather than silently adding it.

**For this math-first dispatch as scoped:** `Round-trip: not applicable — no code emit, no contract field added; math + composition-rule design only. If gamora's binding review reveals a required loadout-dict field, that finding escalates to knight-rider before any code lands (becomes a Gate-1 item, not a silent add).`

## Scope
- [ ] Math-first axis design doc (definitions, ranges, composition rules, #24 isolation, Leg-B sampling recommendation) — the deliverable of this dispatch
- [ ] gamora adjacency review: confirm the economy binds in fight resolution; document any required loadout-dict field as a finding (do NOT silently add)
- [ ] NO population emit, NO fire, NO gauntlet — this is design-only, gates Leg B
- [ ] MIGRATION.md ONLY if gamora binding review surfaces a required cross-seam field (then escalate first)
- [ ] Round-trip: not applicable (no contract change) OR escalate per the Principle-6 gate above
- [ ] AGENT_STATE.md updated at session end
- [ ] No tag (math-first design doc, no production code) — OR seam-prefixed tag if any binding stub lands; your call, documented

## Acceptance criteria
- [ ] Three economy axes defined math-first with justified ranges + composition rules, same shape as landed variation axes (cited)
- [ ] #24 sweep-isolation confirmed per axis
- [ ] Leg-B sampling-scheme recommendation stated (grid vs LHS-class) for jack-ryan Gate-1 ratification (§8 D4)
- [ ] Structural-honesty clause respected: axes are not pre-biased toward a floor-clear; Leg B is a genuine test of whether the viable region exists
- [ ] gamora sim-binding adjacency documented; any required loadout field surfaced as a finding
- [ ] Round-trip: not applicable — no cross-seam contract change authored here (or escalated per gate)

## Out of scope (explicit non-goals)
- **NO population emit, NO fire, NO gauntlet.** Leg A is math-first design only. Leg B (star-lord fire) is the pilot; Leg C is the full 18-cell fire — both downstream, gated on this + Gate-1.
- **NO hand-tuned caster config.** Q1(a) rules economy as axes the population searches, NOT a picked config. Do not smuggle a tuned mana economy in as an axis default.
- **NO band re-tune, NO re-emit of pilot kits.** Provenance law (§5): only the Leg-C population votes. Pilot/pre-axes kits are fixture/regression bank only.
- Leg-B cell selection / candidate budgets — those are Leg-B outputs, not Leg-A design.

## Open questions for the agent to resolve (document your answers)
- Grid vs LHS-class sampling for Leg B (§8 D4) — recommend + justify; jack-ryan ratifies.
- Does binding the economy in fight resolution require any new kit→sim loadout field? If yes → escalate to knight-rider (Gate-1 item) before landing.
- Where does economy identity naturally partition (cheap-sustained / builder-spender / flat-cost)? Name the regions the axes make reachable so Leg B's map is interpretable.

## References
- `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` (§2 Leg A, §3 GO/HALT, §5 provenance, §8 D4/D5/D6)
- `agentic_orchestration/gandalf/notes/2026-07-06-kr-relay-av2-chassis-ruling-fire-order.md` (C2 ruling provenance)
- gamora calibration note + Leg-4 report (2026-07-06) — the C2 floor + chassis finding
- decisions-log: C2 registration batches on jack-ryan's next pass
- engineering-disciplines #1 (math-before-code), #24 (sweep isolation), #20 (row-duplication prohibition)

---

## Completion record
<!-- rocket appends on completion -->
