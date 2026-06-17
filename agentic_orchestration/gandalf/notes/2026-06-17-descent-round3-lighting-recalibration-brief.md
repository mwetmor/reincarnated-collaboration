# Round-3 Lighting RECALIBRATION Brief — Descent Scene (drax)

**STATUS:** GO — fires now. Round-2 Gate-A REJECTED 0/6 (galadriel commit `a3fe512`). Round-1 Gate-B PASS (all geometry landed; carries NO geometry into Round-3). No drax-instance collision (Round-2 closed).
**Author:** gandalf (design steward). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md` (the run-to-green tracker; Round-3 PLAN).
**Supersedes the Round-2 lever framing.** Round-2 chased "restore per-chamber key reach." That was a symptom-level fix. gandalf code-read (this brief §0) found the real cause is GLOBAL: the descent diverged from the proven register-2 env rig on every tonemap/ambient lever. **Fix the global rig FIRST; the per-chamber keys are likely already strong enough.**
**Measurement arbiter:** galadriel's COMMITTED scorer `reincarnated-collaboration/agentic_orchestration/galadriel/pipeline/register2-score-descent-iter5.mjs` (+ `register2-scores-descent-iter5.json`). drax self-measures candidate renders against THIS before any all-zones blind relight (math-before-code / smoke-test-one-seed).

---

## 0. THE DISCOVERY — why Round-2's stronger keys didn't move LDR (read first)

galadriel's photometry is authoritative on OUTPUT: iter5 LDR did not move (mean |dLDR| 1.7; bright%>180 stuck 0.1–0.4%; flat-dim-mid histogram unchanged). Her *causal* inference was "reach not energy — the keys are local points, not reaching pools." **The code refutes that inference.** The iter5 ZONE_LIGHT keys are ALREADY boss-class-or-stronger:

| zone key | energy | range | atten | vs proven boss CombatFill (1.5 / 34 / 1.5) |
|---|---|---|---|---|
| war_hall (#1 priority) | **3.4** | **40** | 1.3 | stronger energy, longer range, softer falloff |
| arcane | 2.3 | 38 | 1.35 | stronger/longer/softer |
| sanctum | 2.2 | 38 | 1.4 | stronger/longer/softer |
| antechamber | 2.1 | 36 | 1.45 | stronger/longer |

`_build_chamber_key` (render_descent_scene.gd:666-707) places these at height 11, range 40 → delivers ~2.2 intensity to the floor directly below vs the boss CombatFill's ~0.95. **The reach is already there. The keys are stronger than the lever that scored 176.** Yet LDR is flat. So the suppressor is NOT the key — it is GLOBAL.

**The real cause — the descent abandoned the proven register-2 global env rig.** Every PASS scene (boss arena LDR 176, cathedral 5.00, every `arena_*` variant) uses ONE rig. The descent is the lone outlier on every dynamic-range lever:

| lever | proven rig (boss/cathedral/all arena_*) | descent (FAIL) | effect of the descent's value |
|---|---|---|---|
| `tonemap_mode` | **3 (ACES)** | **2 (FILMIC)** | flatter curve → compressed dynamic range, milky mids |
| `tonemap_white` | **8.0** | **6.0** | (minor; lower white reads brighter — not the suppressor) |
| `tonemap_exposure` | **0.95** | **1.0 (default)** | (minor) |
| `ambient_light_energy` | **0.17** | **0.24** | floods surround to mid → lifts p05 (KILLS SHF) + compresses p95−p05 (KILLS LDR) |
| `fog_density` | 0.010–0.012 | 0.0052 | (descent has LESS fog — fog is NOT the suppressor; boss passed at 0.010) |

**Two levers produce galadriel's exact twin-low (LDR low AND SHF low) signature:** `ambient 0.24` (the surround-flood) and `FILMIC vs ACES` (the flat curve). The keys read flat because they are tonemapped flat and ambient-washed — not because they don't reach. **A global-rig match should lift ALL six zones toward the bar at once, because the keys are already built.** This is the cleanest hypothesis for "stronger keys, zero LDR movement," and it is testable cheaply (§1.1).

**Where it lives:** `render_descent_scene.gd` `_build_global_environment` (~2046-2089) is the SOURCE; `scenes/arena_descent.tscn:502-516` is its BAKE (values match exactly — ambient 0.24, tonemap_mode 2, white 6.0, fog 0.0052). Fix the script; re-bake. The "iter1 mood-lift" comment (`:2041`) shows the env was hand-built from scratch for the green-atmosphere reference instead of inheriting the proven rig — Discipline #13 implicit-pillar drift at the global level.

---

## 1. THE WORK — ordered by leverage, probe-first

### 1.1 PRIMARY — match the proven global rig, then re-measure zone2 (the one cheap high-leverage test)

In `_build_global_environment`, move the dynamic-range levers to the proven register-2 rig, **preserving the descent's GREEN fog identity** (the green is intentional mood — keep `fog_light_color` green; only the dynamic-range levers change):

- `tonemap_mode` → **ACES** (`Environment.TONE_MAPPER_ACES` / mode 3) — was FILMIC
- `tonemap_white` → **8.0** — was 6.0
- `tonemap_exposure` → **0.95** — was 1.0
- `ambient_light_energy` → **0.17** — was 0.24 (the surround-deepener; this is the SHF lever)
- `fog_density` → **~0.010** (into the proven band; secondary — boss passed at 0.010) — keep green `fog_light_color`

Re-bake, re-render **zone2 only** (the worst/flattest chamber, the hardest case), and self-score against `register2-score-descent-iter5.mjs`.

**Read the result:**
- **If zone2 LDR jumps toward ~176 + SHF deepens (bright%>180 climbs off ~0.2%, p95 climbs off ~125):** the global rig WAS the suppressor. The per-chamber keys were never the problem. Apply the global change, re-render all 6 + 3 establish, hand to galadriel. **Do NOT also retune the keys** — if the rig-match lands the bar with the existing keys, leave the keys alone (changing two things at once destroys the attribution).
- **If zone2 moves PARTWAY (LDR up but short of bar):** the rig was a major factor but not the whole gap. NOW run §1.2 (the key A/B isolation) to find the residual, one lever at a time.
- **If zone2 does NOT move at all:** the global env you edited is not the one applied at render time (two-env conflict — reconcile which WorldEnvironment wins; the script `add_child(we)` vs the baked `arena_descent.tscn` env). Resolve that first — it would mean iter5's env edits never applied either.

### 1.2 SECONDARY (only if §1.1 lands partway) — A/B key isolation in zone2

Before retuning keys again, prove they reach the framed region: render zone2 with `ChamberKey` ON vs OFF (comment out the `_build_chamber_key` call), measure ΔLDR.
- **ΔLDR ≈ 0** → the key's pool lands OUTSIDE the combat camera's framing, or is occluded (position `Vector3(W*0.5, 11, H*0.5+2)` is chamber-center; the combat camera may frame the player-spawn band off-center). This is a POSITION bug, not a tuning issue — move the key onto the framed engagement band, don't crank energy.
- **ΔLDR small-but-nonzero** → screen-area-fraction problem (pool is bright but covers too little of the frame to lift p95). Lower the key (closer to floor) for a tighter, brighter, larger-on-screen pool — OR confirm the combat camera framing matches the boss arena's (a further camera shrinks the pool's frame fraction).

One lever at a time. Self-measure each candidate against the committed scorer. Do not blind-relight all 6 until zone2 clears.

### 1.3 zone4 antechamber — REVERT the regression first

zone4 LDR fell **−9 (116→107, below the 115 floor it had PASSED at iter4)**; the iter4 red soulfire center-pool muted and walls cooled. The iter5 low key (2.1/r36) REDUCED the existing warm fill. **Revert zone4 toward its iter4 warmth** (restore the red soulfire pool), THEN shadow-deepen. zone4's iter4 problem was SHF (13%, too bright surround), NOT LDR — it already had a PASS-grade LDR. Keep the green identity (`_is_green`); restore the warm key it lost. The global-rig ambient drop (§1.1) will help the SHF directly.

### 1.4 zone3 oubliette — CONTRAST criterion, not LDR-176

galadriel confirmed the torch-line is the right KIND (warm points, genuinely dark void between, SHF 57.9% — by far the deepest dark of all zones). It is short in MAGNITUDE, not wrong in kind. **zone3 is a DREAD chamber — it should PASS on CONTRAST (high SHF + bright torch-pools + moderate LDR), NOT on boss-arena LDR-176.** Do NOT flood it to lift LDR — that destroys the dread identity. Widen the torch POINTS into POOLS (raise per-torch range from 13 toward ~20-24; keep them a ROW, keep the void dark between). Target: each torch reads as a bright pool punched in real black; LDR clears the floor on the torches; SHF stays deep (>40%) between them. **The galadriel re-score must judge zone3 on this contrast criterion** (high SHF + bright pools), not the uniform LDR-176 bar — gandalf design call, carried to galadriel in the re-score request.

### 1.5 establish ×3 — finish the recompose (light + 3 residuals)

galadriel confirmed the Round-2 recompose PARTIALLY landed (verticality + de-tabletop + de-clutter — real +0.25). Three residuals remain:
- **(a) Warm the floors.** warmCool went the WRONG way (1.025→0.999, crossed into cool). The global ACES rig + warm spine braziers should help; ensure the floor reads warm-dominant.
- **(b) Kill or resolve the Layer-3 blue deep-wall panels.** They are the single most eye-catching element and pull focus AWAY from the magenta sanctum payoff; they read as flat blue slabs. The iter5 establish-camera comment (`:2110-2114`) already identifies that looking down-spine makes deep walls read face-on as flat blue — keep the DIAGONAL across-chambers angle that avoids it, and tone the blue panels down so they read as atmospheric depth, not slabs.
- **(c) Plant the magenta focal payoff.** The sanctum arcane magenta should be the bright vanishing-point anchor where the eye lands, with the warm braziers reading as a leading-line down the spine. Right now the deep end dissolves with no anchor.
- Gate on light AND composition — a relit-but-still-blue-slab frame REJECTS.

### 1.6 VFX — NO WORK. Inherited-PASS FINAL.

galadriel's validator confirmed the eruption column POPS 2× against the relit backdrop (NOT washed). The 0.2%-baked HLF is an off-peak baked-replay undercount, not a wash — a known windowing artifact, ruled non-blocking. **No erupt re-capture needed.** VFX gate = inherited-PASS, final. (If quantitative 4%-peak confirmation is ever wanted, the fair instrument is a windowed lifecycle capture — deferred, not loop-blocking.)

---

## 2. PROCESS DISCIPLINE (the reason Round-2 wasted a round)

- **Probe-first, one lever at a time.** §1.1 (global rig) is the first probe; self-measure zone2 against galadriel's COMMITTED scorer before touching all 6. Round-2 blind-relit all 6 on an unverified lever and burned a round. Do not repeat.
- **Attribution clarity.** If §1.1 lands the bar, do NOT also retune keys — one change, clean attribution. Only stack a second change if the first lands partway.
- **Parity 35/35.** Lighting + env + camera only. No geometry, no spawn changes. Re-verify the both-ends-land parity holds (Gate B is PASS; don't perturb it).
- **Auto-commit your iter6 work-products; do NOT push** (Matt-gated). Captures stay git-ignored (Synty-derivative IP) — local evidence only, never committed.

---

## 3. ACCEPTANCE (the dual gate — unchanged criteria, sharpened per-zone)

- **Gate A (galadriel re-score):** each relit zone composite **≥ ~4.0 + both mandatory gates**, with the lighting axis showing **LDR lifted toward ~176 AND SHF deepened — BOTH simultaneously** — EXCEPT zone3, judged on the **contrast criterion** (high SHF + bright torch-pools + moderate LDR; §1.4). A zone that raised LDR but flattened SHF raised the fill, not the key → REJECT.
- **Gate B (load-path):** PASS, held from Round-1. No geometry changes in Round-3 → no new Gate-B ruling needed UNLESS the establish recompose perturbs geometry (it shouldn't — camera + lighting only).
- **VFX:** inherited-PASS FINAL (§1.6). No work.

---

## 4. OUTPUT (what comes back to gandalf)

1. **iter6 captures** — all 6 zones + 3 establish (combat camera; git-ignored, local).
2. **The locked global-rig recipe** — the exact env values that landed zone2 (so the run-to-green log records the proven descent env).
3. **Per-zone self-measured metrics** vs the committed scorer (LDR, SHF, bright%, p95) — your read before galadriel's independent re-score.
4. **Which hypothesis landed** — did §1.1 (global rig) alone lift the zones, or did it need §1.2 (key isolation)? This is the attribution the log needs.
5. **A short note on the two-env reconciliation** (script `_build_global_environment` vs baked `arena_descent.tscn`) — confirm which applies and that your edit took.

---

**Signed:** gandalf, 2026-06-17. Round-3 RECALIBRATION brief — root cause re-found via code-read as GLOBAL env divergence (descent abandoned the proven ACES/0.95/8.0/0.17 register-2 rig for a hand-built FILMIC/1.0/6.0/0.24 rig; ambient-flood + flat curve = galadriel's twin-low signature; the per-chamber keys are already stronger than the proven CombatFill and were a red herring). Fix the global rig FIRST, self-measure zone2 against galadriel's committed scorer, then isolate any residual one lever at a time. zone4 revert; zone3 contrast-criterion; establish finish; VFX none. Probe-first to avoid a third blind round. GO.
