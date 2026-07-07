# Gauntlet Run-Beat Families — the re-based certification instrument (four families, genre-anchored)

**STATUS:** ✓ RATIFIED — **Matt 2026-07-07, R1–R5 as drafted**, one named contingency (verbatim): *"assuming no issues on monster count for godot game's playable PC or mobile phone system specs."* **Contingency operationalized:** the §3 density targets (F1 ~24 · F2 ~40 · F4 continuous) must be render-feasible at the ruled 60-FPS floor (Q5 ruling, GTX-1650/RTX-3050 min-spec class) AND on mobile-class targets → **drax perf spike** (composes with the pre-D7 horde-density spike the Q5 ruling already governs). **Spike failure = re-open trigger** (§3 populations shrink → §6 bars re-derive) — **NOT a blocker on sim-side build.** Authored 2026-07-07 (gandalf, design half of the instrument design session). Two passes execute inside the ratified structure: **gamora feasibility pass** (§8 implementation items) and **jack-ryan metrology pass** (§6 bar-derivation + saturation guards). Neither reopens the family structure. Fire order: `agentic_orchestration/gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md`. **✓ CONTINGENCY DISCHARGED 2026-07-07:** drax spike PASS (112K–228K tris / 45–91 draw calls ≈ 1–2% GTX-1650 frame budget; mobile ~380–510 eq-FPS pre-LOD) — re-open trigger NOT tripped; §3 densities stand; absolute GPU-ms certification stays `matt_to_do/` T2 (Godot Metal backend reports no GPU time). **✓ INSTRUMENT BUILT + BARS DERIVED same-day:** gamora `gamora/v-batch2-gauntlet-four-family-instrument-1` (engine `8d45f95`) · jack-ryan `simulation/math/gauntlet-four-family-metrology-2026-07-07.md` (bars provisional-pending-playtest; all four saturation guards PASS).
**Governing laws (Matt 2026-07-07, this doc's spine):**
> **(a) Fit-direction law:** *"I do not want to fit the simulation gauntlet parameters to pass kits into my game, I want to fit kits from my game into ARPG genre canonical monsters per area, KPM, win rate."* Bars derive from genre canon (external reference standard); the kit population is the SUBJECT under measurement, never the calibration source. A kit that fails a genre-anchored bar gets fixed; the bar moves only if genre evidence says the bar misread canon.
> **(b) One-spatial-contract law:** room dimensions are authored ONCE, in meters, and consumed by BOTH the sim gauntlet arenas and the Godot presentation rooms — no runtime re-determination of the Godot room representation.
**Evidence base:** `agentic_orchestration/legolas/findings/2026-07-07-arpg-genre-canon-encounter-metrology.md` (Mode A commission, 32 sources, per-row confidence) · `spatial_gauntlet/arena.py` inventory · `martial_bar_rederivation_driver.py` Step-1 finding (2026-07-07) · `../reap-die-rise-story/gameplay-loop-design.md` §23.1 (the run model).
**Supersedes as certification structure:** the 6-room monster-tier ladder (W0.9.2, 2026-05-21 — my own design authority; correct for its era, which pre-dated the §23 run model). The rooms largely survive (§4); the LADDER as the certification question retires.

---

## 1. Why re-base (three defects, one recognition)

1. **The instrument is broken (Step-1 finding, 2026-07-07):** the F-d wall bars (9.90 / 11.65 mean-kills) exceed the 8-mob supply cap of the shells they're judged on; 7/8 martial cells saturate at exactly 8.0. A metric pinned at its own ceiling can rank nothing.
2. **The ladder certifies the wrong question:** trash→champion→elite→mini-boss→boss is the *genre's monster taxonomy*, not *our run's shape*. The run (§23.1) has four beats; a kit that climbs the ladder has never been asked "can you play the run?"
3. **The genre-conformance recognition (the deep one):** our six rooms are **pack-scale probes** (3–8 mobs) where genre rooms are **population-scale spaces** (15–60 mobs; legolas F1/F2 anchors, MED). The saturation defect and the genre-density defect are THE SAME DEFECT — too few monsters — and law (a) fixes both with one move: **re-populate to genre density, and headroom returns for free.** (The 2026-05-17 KPM cross-check genre-confirmed our *scale*; nobody ever genre-checked our *supply*.)

## 2. Unit + screen contract (law (b) groundwork)

- **Meters, everywhere.** Sim `Arena(width_m=…)` and Godot (native meters) already share the unit. Genre conversions per legolas (HIGH unless noted): **1 D3 yard = 0.3 m** (NOT a real yard — the single most dangerous conversion trap; naive reading over-sizes rooms 3×) · PoE post-v3.22.1 = real meters · D2 = LOW confidence, use as qualitative only.
- **Screen reference:** D3 visible playfield ≈ 36×36 m. Our locked camera (FOV 40 / pitch −55° / yaw 47° / dist 34 m) ⇒ **MEASURED visible floor: near-edge width 40.6 m · legible-band width ~48.9 m · depth span 36.5 m** (drax harness verify, Camera B, 2026-07-07 — SUPERSEDES the prior camera-geometry estimate of ~28–35 m × 20–26 m). This is **our strongest absolute anchor** (legolas warning #3: no ARPG publishes room dims — community-inferred MED/LOW throughout; our own measured camera outranks them as an absolute). **Ruling (gandalf, R2 authority, 2026-07-07):** measurement RECORDED, no family dim widened. F2's 36×36 m sits inside the ~48.9 m legible band with margin (reads full, not cramped); widening toward the band would (a) raise F2's "travel is the tax" repositioning cost and shift its KPM bar before Lane-3 derives it — a fit-direction inversion (law (a), one layer down), and (b) walk toward legolas warning #2 (rooms past ~50 m read empty on a fixed camera). Record-only; all four family dims stand as ratified (R2 §108).
- **"1-screen room" ≈ 24–30 m** on our camera. Boss arenas at 1–2 screens (25–50 m) — genre puts them SMALLER than designer instinct wants (legolas warning #2); rooms past ~50 m read empty on a fixed camera.

## 3. The four families

Certification question per family; a kit certifies by passing **all four** (the run forces all four beats on every kit — see §5 note on the STR carve-out).

### F1 — Tight-interior dense-pack ("blow through it") — Structure 1, §23.1
- **Certifies:** confined-space clear throughput — density handling, AOE-vs-swarm economy, kinetic pacing.
- **Arena:** **16 × 22 m** cell/corridor (genre band 12–20 × 15–25 m, MED). Chokepoint variant keeps its funnel geometry.
- **Population:** **~20 trash + 1 champion pack (3–5 same-type, no minions — D3 canon, HIGH)** ≈ 24 total (genre 15–25 trash + 1–2 elite packs, MED). Trash HP at sub-second TTK for a functional kit (HIGH); champion pack at 3–15 s pack-clear (MED).
- **Metric + genre band:** KPM, genre target **30–60** (MED; prior 30–50 band confirmed-conservative). Win-rate expectation >95% (rooms that kill average players here are mis-built, MED).
- **Members:** NEW `dense_cell` (canonical) · `chokepoint_corridor` re-populated 8→genre (funnel variant) · `magic_pack` re-roled as the champion-pack variant, +trash to genre.

### F2 — Open-field dispersed elites — biome crossing, §23.1
- **Certifies:** spread-target throughput — repositioning cost, sustained single-ish-target pressure between packs, the path-symmetric spatial signal in its natural habitat.
- **Arena:** **36 × 36 m** (1 D3-screen; genre band 28–50 m, MED).
- **Population:** **~40 total, spread:** ~34 trash + **3–4 rare packs (1 rare leader + 3–4 minions — D3 canon, HIGH)** (genre 30–60 total, 3–6 elite packs, MED). Elite-pack TTK 5–20 s (MED); elites ~5–10% of population (MED).
- **Metric + genre band:** KPM, genre target **20–40** (MED — lower than F1 by design; travel is the tax). WR 85–95% (elites are the competency check, not the fail state).
- **Members:** `open_arena` **re-populated 8→~40 (THE repair — this dissolves the saturation defect)** · `elite_pack` re-roled as an isolated-pack probe variant.

### F3 — Single-target champion (+ add waves) — Structure 2, §23.1
- **Certifies:** boss-fight viability — sustained single-target output, survival under the run's intended hard gate.
- **Arena:** ~**30 m** (existing; genre band 25–50 m diameter, MED — already conformant).
- **Population:** boss + adds. Genre wants **2–8 adds in 1–3 waves DURING the fight** (HIGH); existing rooms field 2 static-spawn adds → **enhancement: 1–2 timed add-waves** (non-gating; gamora feasibility).
- **Metric:** **success-rate judged, NOT KPM** (genre HIGH — matches our existing SURV judging; KPM stays a wide sanity rail). Genre rails: boss TTK **15–90 s** at-level (MED; 5–15 s = overpowered flag); WR per attempt 60–80%; add TTK 1–5 s. *Bosses are allowed to kill people — 20–40% death-per-attempt is genre-normal (MED). C2's floor lives here, vindicated.*
- **Members:** `boss_with_adds` + `mini_boss` carried substantially as-is.

### F4 — Escape plow-through (under the clock) — The Escape, §23.3 · THE NEW ROOM
- **Certifies:** the run's crescendo — currently the only beat NO instrument measures. Forward-pressure throughput at champion power: target acquisition + movement + mow rate. *This is the purest measurement of the spatial/geometry signal the HALT investigation isolated.*
- **Arena:** **60 × 16 m directional lane** (exit at far end; genre zone 40–80 m, MED; lane structure per PoE Blight/Delve precedent).
- **Population:** **continuous reinforcement** (genre-native, HIGH — Blight/Delve/cursed-events all stream spawns): 2–4× F1 trash density (HIGH), 20–50 engaged at any moment, 150+ total over the window. Fodder TTK <0.5 s at champion power (HIGH).
- **Power state:** the kit under test runs **champion-elevated** (the §23.3 escape is played in the just-claimed champion body; elevation = the §8 sidegrade-law level-heat, gamora feasibility item for the sim expression).
- **Metric + genre band:** KPM (genre target **60–150**, MED) + forward-progress rate + exit-reached within a **fixed generous window** — intended pass rate for functional kits **80–90%+** (HIGH; Hades/D3-rift timer canon: the clock urges, it doesn't usually kill). *Instrument uses a fixed window for determinism; whether the GAME's escape timer is pure-countdown or kill-to-extend (PoE Incursion pattern) is a game-side decision, non-gating here.*
- **Members:** NEW `escape_lane` — the one genuinely new room.

## 4. Genre-conformance disposition of the existing six

| Room | Disposition | Change |
|---|---|---|
| `open_arena` | F2 canonical | re-populate 8 → ~40 (trash + 3–4 rare packs) — the saturation repair |
| `chokepoint_corridor` | F1 funnel variant | re-populate to genre F1 density |
| `magic_pack` | F1 champion-pack variant | +trash to genre; pack composition already D3/PoE-canonical |
| `elite_pack` | F2 isolated-pack probe | keep as variant; not the F2 canonical room |
| `mini_boss` | F3 member | as-is |
| `boss_with_adds` | F3 canonical | +timed add-waves enhancement (non-gating) |
| *(new)* `dense_cell` | F1 canonical | author at §3-F1 spec |
| *(new)* `escape_lane` | F4 canonical | author at §3-F4 spec |

Nothing is deleted; the 300k-HP "wall" parametrization retires as a certification shell (it was the broken instrument) but stays available as a diagnostic probe.

## 5. Instrument requirements (headroom law + judging)

- **Headroom law:** no KPM-judged shell may cap below **~2× its bar** — supply (population or continuous spawn) must exceed any plausible kit's clearing capacity within the window. Genre density delivers this automatically for F1/F2; F4 gets it by construction (continuous spawn); F3 is success-judged (exempt).
- **Judging per family:** F1/F2 = KPM band (floor + ceiling, per genre targets §3) · F3 = success-rate + TTK rails · F4 = KPM + progress + exit within window.
- **Universality note (flag, needs Matt):** the existing carve-out *"STR ships via the clear-room floor without boss shells"* (gauntlet_sim.py) predates the run-beat law. Under four-family certification **every kit plays every beat** — the run does not offer a boss-free path. Lean: carve-out retires; if a chassis can't pass F3, that's a chassis gap (exactly what the caster HALT taught us), not a certification exemption.

## 6. Bar-derivation protocol (jack-ryan's half — framed here, executed there)

1. Genre bands (§3, legolas file) are the **exterior reference**; the 30–50 TMPM anchor (2026-05-17, re-validated 2026-07-07) is the **scale bridge** into our economy.
2. Bars derive on the **new instrument only** — never carry a bar across instruments (the 9.90-on-8-mobs lesson; instrument-matched derivation per the Step-1 driver's own discipline).
3. **Saturation guard at derivation time:** reject any derived bar within 2× of the shell's supply ceiling.
4. Balanced cohort first (per the existing §2-S.1 reduction); cohort expansion after.
5. All bars remain **provisional hypotheses pending playtest** per `gauntlet-metrics-as-provisional-hypotheses-recognition` — genre-anchoring upgrades their provenance, only the Godot descent-floor playtest validates feel.
6. **Numeric bars are deliberately NOT set in this doc** — that is the metrology pass, on the built instrument, against the genre bands.

## 7. One spatial contract (law (b) — the Godot half)

- The §3 arena dims **are** the Godot room dims: F1 16×22 m · F2 36×36 m · F3 ~30 m · F4 60×16 m lane. drax's D6 three-beat floor authoring consumes these as the room-size grammar (§23.1's "room-size grammar = the pacing signal" now has genre-anchored numbers); the sim certifies kits on the literal geometry the player will stand in.
- **Camera-fit check:** all four sit inside 1–2 screens of the locked camera (measured ~48.9 m legible-band width; F2's 36×36 fits with margin, F4's lane is multi-screen by length, single-screen by width — correct for a flight corridor). Boss arena deliberately NOT epic-huge (legolas warning #2).
- Changes to family dims after ratification are **spec amendments** (both consumers re-point), never a runtime translation.

## 8. Migration + sequencing

1. **Matt ratifies this doc** (§9 asks) → the instrument fork closes; KR Steps 3–4 unblock against the new instrument plan.
2. **gamora feasibility pass:** continuous-spawn capability (F4) · population re-parametrization (F1/F2) · champion-elevation expression (F4 power state) · timed add-waves (F3, non-gating) · cost estimate. Config-dominant; the one plausible plumbing item is the F4 spawner.
3. **jack-ryan metrology pass** (§6) after the rooms exist: derive bars, register saturation guards, re-run the martial distribution + the caster cells on the new instrument.
4. **Then the paused sequence resumes:** stratified re-pilot → F-b residual sizing (if it survives re-measurement) → Leg C.
5. **The loot §7 fairness campaign inherits this instrument as-built** (`agnostic-loot-engine-spec.md` §7) — one instrument, two customers.

## 9. Ratification asks (Matt) — ✓ RULED 2026-07-07

**All five ratified AS DRAFTED** (Matt verbatim: *"Ratify R1–R5 as drafted, assuming no issues on monster count for godot game's playable PC or mobile phone system specs."*). The monster-count assumption is the **standing contingency on R3** (and on R2's dims insofar as density scales with area) — operationalization + re-open trigger in the STATUS banner. Table kept as lineage:

| # | Ask | My lean | Ruling |
|---|---|---|---|
| R1 | Four-family structure + certification = pass all four | as specced | ✓ as drafted |
| R2 | Family dims (16×22 / 36×36 / ~30 / 60×16 lane) as the one spatial contract | as specced; drax camera-verify may adjust ±20% | ✓ as drafted |
| R3 | Genre density targets (F1 ~24, F2 ~40, F4 continuous 2–4×) | as specced | ✓ as drafted — **carries the perf contingency** |
| R4 | STR boss-shell carve-out retires under §5 universality | retire | ✓ retire |
| R5 | F3 add-waves + F4 spawner as the two build enhancements | approve, gamora sequences | ✓ approve |

---

**Signed:** gandalf, 2026-07-07. *The ladder measured monsters; the families measure the run. And the test answers to the genre, not to the kits it tests.*
