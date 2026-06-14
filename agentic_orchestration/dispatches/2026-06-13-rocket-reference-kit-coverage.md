# Dispatch — 2026-06-13 — rocket — reference-kit coverage: resource/CC-differentiated kit (D5)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-13 (D5 disposition — ENDORSED).
**Status:** READY (arity=8 HELD). Coordinate sequencing with KR — this is the instrument the D1 decompose needs for Axis-5/Control, but it does NOT block the decompose surfacing.
**Estimated effort:** ~hours (hand-authored reference kit + validation against the existing §5 set).

## Context — what W-D surfaced

gamora's W-D six-axis MEASURE build (engine `5ec33bb`) wired all 8 BC axes from spatial telemetry, but the **hand-built reference-kit set (oracle §5) is UNIFORM on three axes**, so those axes are *wired-but-not-exercised*:
- **Axis-5 Resource = `starved` for ALL kits** — the kits use uniform `stamina`, low cost, high regen; the reduction reads the spend/regen flow correctly but there is no resource-*differentiated* kit to discriminate against.
- **Axis-2B Control = `damage-pure` for ALL kits** — none of the hand-built kits carry a control skill; the reduction reads `skill_type` correctly but the set has no CC-bearing kit.
- (Axis-2A Proxy is a *separate* issue — no spatial mechanic exists; that is the D4 proxy-port, not this dispatch.)

This is a **reference-kit-coverage gap, NOT a measurement bug** (gamora math note §10.6). The fix is a reference kit that *varies* on Resource and Control so the engine's discrimination on those axes can actually be tested.

## Scope

- [ ] Author a hand-built reference kit (or kits) that is **resource-differentiated** (e.g. a charge-stack or HP-cost / convert-damage-taken economy — something whose Axis-5 bin is NOT `starved`/uniform) AND/OR **control-bearing** (a CC skill so Axis-2B bins away from `damage-pure`)
- [ ] **arity=8 HELD** — do NOT add a 7th *MAP-Elites-archive* kit; this is a **reference/diagnostic** kit for exercising the measurement instrument, sized to the existing §5 reference set's role. If you believe coverage genuinely needs the archive arity to grow, that is the **Bucket-B question (gandalf's ruling, D4)** — surface to KR, do NOT presume.
- [ ] Validate the new kit against the existing §5 reference set (it should reproduce its own pre-registered Resource/Control bins, distinct from the uniform set)
- [ ] Math note before code (Discipline #1): pre-register the new kit's expected Resource/Control bins
- [ ] Coordinate with KR/gamora: this kit is the **instrument** the D1 per-axis decompose uses to confirm Axis-5/Control discrimination — hand off when ready
- [ ] AGENT_STATE.md updated; Tag: `rocket/v-reference-kit-coverage-1`

## Out of scope

- **Proxy/Axis-2A** — that is the D4 spatial-proxy-mechanic port (gamora seam + gandalf density-design contract), not this dispatch
- **Growing the MAP-Elites archive arity** — Bucket-B (gandalf), held
- **Hardening generation fixtures** — surface coverage findings, don't re-architect gen
- Pushing to remote (Matt's gate)

## References

- D5 in `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`
- gamora W-D math note §10.6 (the undifferentiated-axes finding): `reincarnated-engine/src/reincarnated/simulation/math/wd-six-axis-measure-build-2026-06-13.md`
- oracle §5 reference-kit set + §6.3 Bucket-B (arity authority): `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`

---

**Author:** knight-rider, 2026-06-13. Builds the resource/CC-differentiated reference kit that EXERCISES the Axis-5/Control discrimination W-D wired but the uniform §5 set could not test — arity=8 held, Bucket-B arity question deferred to gandalf.
