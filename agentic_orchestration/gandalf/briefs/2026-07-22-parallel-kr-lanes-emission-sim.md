# Parallel KR Lanes — Emission Demo-Critical + Sim Capacity (fireable by Matt)

**STATUS:** DRAFTED 2026-07-22 — awaiting Matt's fire-word(s). Each lane is independently fireable; neither blocks Tier-3.
**Author:** gandalf (`RUN-CONDUCTOR`), under Matt's 2026-07-22 grant: *"Are there any parallel KR runs that can be drafted which I can fire? … feel free to elicit, draft and/or begin anything that you need autonomously."*
**Queue row:** Q42 (`canonical/matt_decision_needed/README.md`).
**Coordination law:** Tier-3 charter T3-V7 (one-way coupling; mirrored in §4 below).

---

## §1 — Why lanes, not run-legs (the routing rationale)

Matt asked whether Tier-3 as chartered is the most comprehensive autonomous run plannable. Verdict: **Tier-3 v1.1 is the most comprehensive run over its own substrate** (now including the RD-1 conditional leg — the first emitted run-object). The rest of the emission→sim→Godot chain CANNOT fold into it without failing the desirable-run-pattern §3 fit test at **F4 (authority-resident)**: emission wiring is star-lord production code, sim capacity is gamora production code — both are the pattern's *"fork profile technical-not-design → spec-frozen build wave (KR-conducted)"* case. The maximal shape is therefore a **three-lane braid**: Tier-3 (gandalf-conducted) × Lane-1 × Lane-2, converging at THE BUNDLE — the Godot-loadable season artifact.

**Macro-arc twins (the "potential larger run," held as a horizon, not one run):** FROM scored catalogue + ruled encounter grammar (design-space) → TO Godot-loadable season bundle consumed by drax's loader (playable-space). It decomposes into the braid precisely because no single conductor legitimately holds all three seams' authority.

## §2 — Lane-1: EMISSION DEMO-CRITICAL (star-lord seam)

**Twin:** built-but-unwired emitters + 100%-NULL skill flavor + no faction/weapon/gear blocks → ONE season bundle emitted end-to-end, all blocks present, flavor filled, Gate-2-checked.

**Paste-ready prompt (open a KR session, paste verbatim):**

> Fire a spec-frozen build wave on the serial-content emission demo-critical lane (star-lord seam). Authorization: Matt fire-word on gandalf brief `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §2. Read `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` (PARTs D–F + latest deltas) first. Scope = demo-critical queue D.1 items #1–#5 ONLY: (1) unified assembly driver — one callable that emits a complete season bundle end-to-end; (2) flavor passes — skill `flavor_text` is 100% NULL, wire the flavor emission path; (3) wire `emit_faction_block()` (`cycle14_unified_bundle_emitters.py:211` — built, never wired); (4) wire `emit_weapon_descriptor()` (`:522` — built, never wired); (5) gear-pool block in the bundle (via `build_unified_season_content_blocks()` `:620`). Done-predicate: ONE season bundle emitted end-to-end through the unified path with faction + weapon + gear blocks present and flavor filled; jack-ryan Gate-2 on the wave. Laws: §F.4 no-governing-count law untouched (emission TIMING stays Matt's); coordination rider — reserve a top-level `encounters` key in the bundle schema but build NO encounter emission (Tier-3 W1 freezes the encounter-grammar schema; its RD-1 run-object becomes this lane's acceptance fixture when it lands); summoner un-gate (#7) stays its own in-flight item — do not fold it in. Namespace discipline: own dispatch namespace; no writes into Tier-3 run files.

## §3 — Lane-2: SIM CAPACITY — multi-actor / horde (gamora seam)

**Twin:** single-kit-slot fight entry + ≤8-concurrent arena shells → audited capacity-extension spec + built extension (formation topology + horde ≥50 + SCENARIO_OVERRUN KPM bands), Gate-2-checked.

**Paste-ready prompt:**

> Fire a two-step spec-frozen wave on battle-sim capacity (gamora seam). Authorization: Matt fire-word on gandalf brief `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §3. Read `canonical/current-to-end-state/current-to-end-state-engine.md` PART I §I.2 + PART IV §IV.2 first. **Step (a) AUDIT+SPEC:** gamora audits what multi-actor + horde capacity requires — the sole fight entry (`spatial_engine.py:2944`) takes ONE player class vs monster dicts (no second-kit slot); all 6 arena shells cap ≤8 concurrent, vs the I.2 end-state extensions (horde-density ≥50 concurrent · matchup-temperature · per-kit level-scaling) and formation-topology needs (swarm / volley-fan / lane / emplacement formations); include SCENARIO_OVERRUN + horde KPM-bands (IV.2 #2 — already clocked). Output: capacity-extension spec, jack-ryan-checked. **Step (b) BUILD** behind the checked spec. Coordination riders: Tier-3 W2 (fit-layer + scenario compute) surfaces harness-expressiveness findings — any W2 red-flag routes INTO this lane's spec as requirements, never a new lane; the multi-actor DESIGN consult (IV.2 #1) stays gandalf-seam — request Pattern-A input when the spec needs design decisions. Namespace discipline: own dispatch namespace; no writes into Tier-3 run files.

## §4 — Coordination law (T3-V7 mirror — ONE-WAY coupling)

1. Lane-1 **reserves** the `encounters` bundle key; builds no encounter emission until Tier-3 W1 freezes the grammar schema. RD-1 (Tier-3's conditional run-object) is Lane-1's acceptance fixture, not its blocker — items #1–#5 are fully buildable without it.
2. Lane-2 is spec-first; Tier-3 W2 red-flags flow INTO its spec. If Lane-2 lands before W2, the charter's named risk (harness can't express formation topology) is pre-hedged; if W2 fires the red-flag first, the honorable-fallback spec routes here instead of spawning a new lane.
3. Coupling direction is **Tier-3 → lanes only.** Neither lane writes into Tier-3 artifacts; Tier-3 never blocks on either lane.

## §5 — Reserve + exclusions

- **Reserve (third fireable, lower urgency):** #9 PROXY-T4 suite — B1-REBASE pending (spec v3 exists; engine-side).
- **EXCLUDED — drax/Godot loader:** Matt's own rider gates drax until serial-content JSON emits + SURFACE-LEDGER GATE1. Honored, not re-opened. Note the braid is exactly what clears the JSON half of that gate: Lane-1 wires the bundle path, RD-1 supplies the first encounter-bearing content. The Godot bundle loader remains the named longest pole — it becomes fireable the beat drax's gate clears, and not before.

---

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22.
