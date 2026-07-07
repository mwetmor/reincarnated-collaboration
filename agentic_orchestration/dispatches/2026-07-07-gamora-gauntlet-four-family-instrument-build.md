# Dispatch — 2026-07-07 — gamora — four-family gauntlet instrument: feasibility pass + build (Lane 1)

**From:** knight-rider
**To:** gamora (simulation seam — `spatial_gauntlet/`)
**Approved by:** Matt 2026-07-07 (Q11 RATIFIED, R1–R5 as drafted — fire order relayed via gandalf)
**Estimated effort:** multi-day (config-dominant; one plausible plumbing item — the F4 continuous spawner)
**Acceptance:** the four family arenas exist as buildable/registered configs at the spec §3 dimensions and populations, the STR boss-shell carve-out is retired, the wall parametrization is demoted to diagnostic (not deleted), a compute-cost estimate is produced, and smoke confirms each family instantiates and runs a functional kit without erroring. **This lane produces the INSTRUMENT; it does NOT derive bars (that is jack-ryan Lane 3) and does NOT re-pilot (that is the resumed Step 3).**

## Context — what this closes and why

Q11 is RATIFIED. The old certification instrument is dead: the Step-1 finding proved the 9.90/11.65 martial bars exceed the 8-mob supply cap of the shells they were judged on (7/8 martial cells saturate at exactly 8.0 — a metric pinned at its ceiling ranks nothing). The recognition (spec §1.3) is that the saturation defect and the genre-density defect are THE SAME DEFECT — too few monsters. The fix is to re-populate to genre density; headroom returns for free. This lane builds that re-populated instrument as four run-beat families (F1 dense-pack, F2 open-field dispersed, F3 single-target champion + adds, F4 escape lane under the clock).

**The two governing laws are binding on your build:**
- **Fit-direction law:** the instrument answers to the genre, never to the kits. You build the rooms to genre density/dims; you do NOT tune them to make current kits pass.
- **One-spatial-contract law:** the spec §3 dims ARE the Godot floor dims — authored once in meters, consumed by BOTH your sim arenas AND drax's Godot rooms. **You read the §3 dims; you never invent or re-determine a room dimension at runtime.** drax's Lane-2 camera-verify may feed a ±20% spec amendment back; if that lands mid-build, both consumers re-point (spec amendment, not runtime translation).

## Required reading before starting
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` — **THE spec.** §3 (the four families: dims + populations + metrics), §4 (disposition of the existing six rooms — what survives as family member vs diagnostic), §5 (headroom law + the STR carve-out universality note = R4), §7 (one-spatial-contract), §8 (your feasibility-pass items, step 2).
- `agentic_orchestration/gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md` §2 Lane 1 — your scoped item list.
- `agentic_orchestration/legolas/findings/2026-07-07-arpg-genre-canon-encounter-metrology.md` — the genre density/dims evidence base (32 sources, per-row confidence) that the §3 numbers derive from. Read for the WHY behind the populations, especially the D3-yard = 0.3m conversion trap (warning #1) and boss-arenas-smaller-than-instinct (warning #2).
- `spatial_gauntlet/arena.py` — the existing arena registry you extend.
- `spatial_gauntlet/gauntlet_sim.py:207` / `:662` — the STR boss-shell carve-out (R4 retires it). **Verify these line numbers at session start** — they came from the design session and may have drifted; the carve-out is the "STR ships via the clear-room floor without boss shells" logic.
- `spatial_gauntlet/spatial_engine.py:2527,3262` + `arena.py:366-378` — the 8-mob spawn cap / no-respawn machinery the Step-1 finding located (the F4 continuous spawner is the plumbing that lifts this for the escape lane).
- Step-1 finding: `simulation/notes/caster-bar-rederivation-2026-07-07.md` + `simulation/math/caster-bar-rederivation-instrument-match-2026-07-07.md` (why the old instrument saturates — the defect you are repairing).

## Math/design-before-code (Discipline #1) — document BEFORE editing
Document, in a math/design note, BEFORE touching config or code:
- **Per-family population parametrization** — the exact mob counts + composition you will instantiate per §3: F1 ~24 (≈20 trash + 1 champion pack of 3–5 same-type, no minions) · F2 ~40 (≈34 trash + 3–4 rare packs of 1 leader + 3–4 minions) · F3 boss + adds (+1–2 timed add-waves) · F4 continuous reinforcement (2–4× F1 trash density, 20–50 engaged, 150+ over the window). Cite the §3 line for each.
- **Trash-HP-at-TTK mapping** — §3 sets trash HP at sub-second TTK (F1) / fodder <0.5s at champion power (F4). Document the HP values you'll use and the TTK assumption; this is a design parameter, not a runtime discovery.
- **F4 champion-elevation expression** — how the kit-under-test runs champion-elevated (the §23.3 escape is played in the just-claimed champion body; = the sidegrade-law level-heat). Document the sim expression before wiring.
- **F4 continuous-spawn contract** — the spawner's fixed-window determinism (spec §3-F4: instrument uses a fixed generous window for determinism; whether the GAME's timer is countdown vs kill-to-extend is game-side, non-gating here). Document the spawn cadence + engaged-count target + window.
- **Compute-cost estimate** — projected per-family and full-instrument run cost (Discipline #1.1 pre-fire resource-bounds: F2 ~40-mob + F4 continuous are the heavy cells; declare peak concurrent-entity count and verify against host bounds).

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**Arena/room dims: NO cross-seam handoff in the MIGRATION sense** — the §3 dims are the shared contract, authored in the spec, consumed independently by your arenas and by drax's Godot rooms. Neither seam hands a dict to the other; both read the spec. **BUT:** if your build surfaces that a §3 dim is infeasible in-sim (or the population can't instantiate at the specced dims), that is a SPEC-AMENDMENT trigger, not a unilateral change — STOP and flag to knight-rider → gandalf (spec author) rather than deviate from the one spatial contract.

**No telemetry-schema / fight_log / loadout-dict field change is expected** from a config-dominant build. If the F4 spawner or champion-elevation expression adds a fight_log key or a telemetry field (star-lord boundary), that IS a cross-seam change → MIGRATION.md REQUIRED + flag it.

## Scope
- [ ] **Design/math note first** (all bullets above), committed before code.
- [ ] **F1 `dense_cell`** — NEW canonical room at 16×22 m, ~24 population per §3-F1.
- [ ] **F1 variants** — re-populate `chokepoint_corridor` (8→genre F1 density, keep funnel geometry) + re-role `magic_pack` as champion-pack variant (+trash to genre).
- [ ] **F2 `open_arena`** — re-populate 8→~40 (THE saturation repair) per §3-F2; keep `elite_pack` as an isolated-pack probe variant.
- [ ] **F3** — `boss_with_adds` + `mini_boss` carried substantially as-is; **enhancement: 1–2 timed add-waves DURING the fight** (R5; non-gating — if it proves expensive, flag and ship F3 without it, note as follow-up).
- [ ] **F4 `escape_lane`** — NEW room at 60×16 m directional lane, continuous reinforcement spawner (R5 — the one plausible plumbing item), champion-elevated kit-under-test, fixed generous window.
- [ ] **R4 — retire the STR boss-shell carve-out** (`gauntlet_sim.py:207`/`:662`): certification = pass ALL FOUR families, no population exemptions. If a chassis can't pass F3, that's a chassis gap, not an exemption.
- [ ] **§4 wall disposition** — the 300k-HP wall parametrization DEMOTES to diagnostic (stays in codebase for throughput-isolation probes; never certifies). Nothing deleted; the six existing rooms survive as family members or diagnostics per the §4 table.
- [ ] **Compute-cost estimate** produced (per-family + full instrument).
- [ ] Smoke: each of the four families instantiates + runs a functional kit end-to-end without erroring (this is a BUILD smoke — "does the room work," NOT a certification run).
- [ ] AGENT_STATE.md updated.
- [ ] Tag: `gamora/v-batch2-gauntlet-four-family-instrument-1`.
- [ ] **Submit tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (code + config change to the certification instrument). Note in the submission that Lane-3 metrology depends on this landing.

## Out of scope (explicit non-goals)
- **NO bar derivation** — numeric bars are jack-ryan's Lane-3 metrology pass on the built instrument (spec §6). You build the rooms; you do not set the KPM floors/ceilings.
- **NO re-pilot / no caster-vs-martial re-measurement** — that is the resumed Step 3, after Lane 1 + Lane 3.
- **NO F-fork adjudication, NO constant changes** (BASE_SPELL, multipliers, seed ratios) — constants are FROZEN until new-instrument numbers land. This is instrument construction only.
- **NO tuning rooms to make current kits pass** (fit-direction law violation) — build to genre density/dims; the kits get measured against the result.
- **NO Godot-room authoring** — that is drax (D6, consumes these same §3 dims when the Q7 rig unblock lands). You do not touch `reincarnated-godot/`.
- **NO deletion of the six existing rooms or the wall** — demote/re-role/re-populate per §4; preserve diagnostics.

## References
- Spec `gauntlet-run-beat-families-spec.md` (RATIFIED 2026-07-07); fire order `gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md`
- legolas genre metrology `legolas/findings/2026-07-07-arpg-genre-canon-encounter-metrology.md`
- ADR-004 (MIGRATION if any cross-seam field surfaces), Discipline #1 (design-before-code), #1.1 (resource-bounds), #11 (attribution), #12 (semantic-shift — the instrument change extends the certification contract)
- Run-state `batch2-run-state-2026-07-06.md` (the sequence this unblocks)

---

## Completion record — gamora, 2026-07-07 (Lane 1 BUILD complete)

**Status:** COMPLETE — instrument built + build-smoke green + tagged + submitted to Gate-2. Bars NOT derived (Lane 3). No re-pilot. Constants FROZEN (unchanged).

**Tag:** `gamora/v-batch2-gauntlet-four-family-instrument-1` (engine commit `8d45f95`) — **NOT pushed** (Matt-gated).
**Math/design note (Discipline #1, committed FIRST):** `simulation/math/gauntlet-four-family-instrument-build-2026-07-07.md` (commit `657524a`).
**Gate-2 submission:** `agentic_orchestration/qa/pending/2026-07-07-gamora-gauntlet-four-family-instrument-gate2-submission.md` (notes Lane-3 metrology depends on this landing).
**MIGRATION:** `simulation/MIGRATION.md` v1.84 (F4 `escape_reached` + `continuous_spawned_total` fight-result fields + `mobs_killed` range semantic-shift → star-lord telemetry boundary).

### Scope checklist (all items)
- [x] Design/math note first (all bullets), committed before code (`657524a`).
- [x] F1 `dense_cell` — NEW canonical, 16×22m, ~24 (20 trash + champion pack of 4). Per §3-F1.
- [x] F1 variants — `chokepoint_corridor` re-populated 8→24 (funnel kept); `magic_pack` re-roled champion-pack variant, +trash to 24.
- [x] F2 `open_arena` — re-dimensioned 50×50→36×36 AND re-populated 8→40 (28 trash + 3 rare packs). THE saturation repair. `elite_pack` kept as isolated-pack probe variant.
- [x] F3 — `boss_with_adds` + `mini_boss` as-is; +2 timed add-waves on `boss_with_adds` (R5, t=80/160s; injection VERIFIED at runtime 3→7 mobs).
- [x] F4 `escape_lane` — NEW canonical, 60×16m lane, continuous spawner (k=3/1s/cap50), champion-elevation ×2.0, `escape_reached` win at y≥58, fixed 60s window. Spawner FIRES + escape RESOLVES + ceiling LIFTED (pop 12→50).
- [x] R4 — STR boss-shell carve-out RETIRED (`family_certification_pass` four-family gate; `gauntlet_pass` keeps legacy floor until Lane-3 bars, one-line flip is Lane 3's; comments demoted).
- [x] §4 wall disposition — 300k-HP wall DEMOTED to diagnostic `open_arena_wall_diag` (not deleted); six existing rooms survive per §4 table.
- [x] Compute-cost estimate — peak ~51 live entities on 8GB host, no bounds risk; full-instrument ~53min worst-case (Lane-3 planning; smoke-first).
- [x] Smoke — BUILD smoke green (each family instantiates + runs a functional kit end-to-end without erroring). NOT a certification run.
- [x] AGENT_STATE.md updated (SESSION 52).
- [x] Tag `gamora/v-batch2-gauntlet-four-family-instrument-1`.
- [x] Submit tagged commit to `qa/pending/` for jack-ryan Gate-2 (notes Lane-3 dependency).

### Guardrails honored
- Read §3 dims verbatim; invented no dimension. No §3 dim proved infeasible in-sim → no spec-amendment flag raised.
- NO bar derivation, NO re-pilot, NO F-fork adjudication, NO constant changes (verified `SPATIAL_DAMAGE_SCALE`/`MOB_HP_DIFFICULTY_MULTIPLIER`/KPM bands byte-unchanged).
- Cross-seam field surfaced (F4 `escape_reached`/`continuous_spawned_total` + `mobs_killed` range) → MIGRATION.md v1.84 written + flagged to star-lord.
- Discipline #12 semantic-shifts framed (R4 contract / open_arena re-base / mobs_killed range) → routed to jack-ryan decisions-log.
- Regression: 254 tests pass across 8 spatial suites; 2 tests updated to the new instrument (magic_pack 4→24, open_arena mob-dict helper).

**Empirical criterion gating Lane 3:** the four family arenas exist + register + run a functional kit (this build, smoke-verified) → jack-ryan derives per-family bars on them (spec §6). Then the paused Step-3 re-pilot resumes.

**Signed:** gamora, 2026-07-07 — the four beats are four rooms; the carve-out retired; the bars are Lane 3's.
