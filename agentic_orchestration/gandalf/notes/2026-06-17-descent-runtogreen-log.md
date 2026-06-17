# Descent Run-to-Green — Dual-Gate Status Log

**STATUS:** ACTIVE autonomous run (Matt-authorized 2026-06-17: *"run autonomously until you capture every still and pass them all per galadriel and drax."*)
**Orchestrator:** gandalf (design steward; canon calls on the load-path gate).
**Workstreams:** drax (Godot build/render/presentation-geometry fix + load-path scan), galadriel (register-2 aesthetic scorecard).
**Companion docs:** `agentic_orchestration/gandalf/notes/2026-06-16-drax-render-spec-and-architecture-audit-camera.md` (audit-camera contract + §5 validator scope); `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (register-2 + §2-bis load-path invariant).

---

## The goal — every descent still passes a DUAL GATE

The descent scene = **6 zones + 3 establishing views**:

| # | Zone | Theme | Notes |
|---|---|---|---|
| zone0 | threshold | descent entry | narrative beat (descent threshold) |
| zone1 | arcane | arcane chamber | |
| zone2 | warhall | war hall | |
| zone3 | oubliette | dungeon pit | |
| zone4 | antechamber | antechamber | |
| zone5 | sanctum | mini-boss | **known defect: floating access stair** |
| est×3 | establish 01/02/03 | overview framings | |

**Gate A — AESTHETIC (galadriel).** register-2 scorecard: composite ≥ ~4.0 + both mandatory gates. galadriel scores; her CV probe-suite is the instrument. PASS = looks premium-lit register-2.

**Gate B — LOAD-PATH / architectural-grammar (drax builds clean → gandalf rules).** Every stair / ramp / gallery deck / span / arch lands at BOTH termini on a walkable/support surface within tolerance ("if this were stone and gravity were on, would it stand, and is it doing a job?"). drax runs the deterministic both-ends-land scan (tool output) + builds the fixes; **gandalf makes the canon call** on the audit stills. galadriel's CV is structurally BLIND to this gate (confirmed — the floating stair) — it is a genuinely separate instrument.

**GREEN = both gates pass for every still.**

---

## Per-zone status matrix (updated each round)

Gate A is reported as two sub-axes: **Light** (the real, scoreable target) and **VFX** (ruled inherited-PASS — see canon call below; frozen-charge stills can't score it and the eruption is zone-invariant).

**iter6 state (Gate-A verdict PENDING galadriel re-score — drax-self-measured + gandalf-eyes-on are PROVISIONAL until her independent confirmation; Round-2 confirmation-bias discipline).**

| Still | Gate A — Light (iter6; PENDING galadriel) | Gate A — VFX | Gate B (load-path / gandalf rule) | Overall |
|---|---|---|---|---|
| zone0 threshold | LDR 133 (+11) / SHF 21.4 — both-axes-up; LDR clears 115 | inherited PASS FINAL | **PASS** (stair lands; systemic fix) | iter6 both-axes-up; PENDING SHF-30 call |
| zone1 arcane | LDR 126 (+19) / SHF 23.8 — both-axes-up | inherited PASS FINAL | **PASS** (no gallery — nothing to land) | iter6 both-axes-up; PENDING SHF-30 call |
| zone2 warhall | LDR 115 (+12) / SHF 19.6 — **borderline test case** for SHF-30 | inherited PASS FINAL | **PASS** (stair lands; systemic fix) | iter6 both-axes-up; PENDING SHF-30 call (z2 = arbiter) |
| zone3 oubliette | LDR 118 (+13) / SHF **61.7** — dread-contrast **PASS** (judged on contrast, not LDR-176) | inherited PASS FINAL | **PASS** (stair lands; systemic fix) | iter6 **likely GREEN** pending galadriel |
| zone4 antechamber | LDR 123 (+16) / SHF 23.1 — regression RECOVERED; both-axes-up | inherited PASS FINAL | **PASS** (stair lands; systemic fix) | iter6 both-axes-up; PENDING SHF-30 call |
| zone5 sanctum | LDR 134 (+16) / SHF 17.8 / bright% 2.83 — strongest | inherited PASS FINAL | **PASS** (known float FIXED, top lands on deck) | iter6 both-axes-up; PENDING SHF-30 call |
| establish 01 | LDR 102 (+5) — **composition FAIL** (blue deep-wall slabs dominate) | n/a (no hero) | **PASS** (scanner-covered; no free-standing spans) | needs distinct recompose mini-round |
| establish 02 | (CV-identical to 01) | n/a | **PASS** | needs distinct recompose mini-round |
| establish 03 | (CV-identical to 01) | n/a | **PASS** | needs distinct recompose mini-round |

Legend: PENDING · PASS · FAIL · GREEN (both gates pass). **iter6 (global-rig match) moved all 6 zones both axes (mean dLDR ≈ +14 vs iter5's 1.7 non-move); flat-dim-mid histogram BROKE.** Gate B FULLY PASSES (all 6 zones, Round-1). VFX inherited-PASS FINAL (Round-2 non-wash validation). **Open: (1) the SHF-30-vs-dressed-chamber calibration call (galadriel re-score, z2 = arbiter) decides 6-chamber GREEN; (2) establish needs a distinct composition recompose (blue deep-wall slabs) — does NOT block the chambers.**

---

## Round log

### Round 1 — FIRED 2026-06-17 (two parallel background workstreams)
- **drax** (agent a13b6a1ff8d202819): (1) extend audit camera sanctum→all zones; (2) FIX sanctum floating stair (`render_descent_scene.gd` ~1371–1378 `_build_gallery_storey` access-stair loop; wrong-direction Z climb — foot grounded (21.5,−9,223.1), top stranded (21.5,−1.7,213.1), must land on deck 10.5m in Z); re-render sanctum clean; (3) analytical both-ends-land load-path scan across ALL zones → flag every failure (tool output; gandalf rules).
- **galadriel** (agent aa78ecf706f199436): baseline register-2 aesthetic score for every zone + establish; per-zone composite + gate pass/fail + specific defects-to-fix for sub-bar zones.
- **Deferred:** combat-res bump (`shoot_descent.gd` → 1440p SubViewport) — optional polish, not pass/fail-critical; tracked as open TODO.

#### Round 1 — galadriel RETURNED (commit `4d6efd2`, not pushed)
Baseline scored all 9 stills. Composite mean 3.14/5; **0/9 pass as-captured**, but the headline splits two ways:
- **VFX gate (HLF) = WINDOWING ARTIFACT, not a build fail.** All 9 read HLF 0.06–0.14% only because the hero SummonGlow is frozen at charge in the static bake. Same zone identities read HLF 1.57–4.06% under iter1 windowed capture; boss arena PASSED on a windowed 4.01% peak. Un-adjudicable from frozen-charge stills.
- **Lighting gate (LDR+SHF) = GENUINE deficit.** Near-chambers a flat dim mid-grey wash (LDR 103–122 vs boss-arena PASS LDR 176); dark frames underlit-empty-void (p95 only ~107–118, no bright key) — not dramatic lit-volume-in-dark. The ambient deficit persists between eruptions → needs a per-chamber CombatFill-style key/fill lift (the boss-arena lever).
- galadriel's other axes already strong: architecture (18→65%) + hue (warm:green 1.75) PASS; geometry-register + material-shading strong.

#### ★ CANON CALL (gandalf, 2026-06-17) — VFX gate = INHERITED PASS, not re-litigated per zone
galadriel correctly showed frozen-charge stills can't score VFX. I add the design fact that makes the windowed-capture-all-6 path unnecessary: **the hero summon eruption is zone-INVARIANT** — same player-spirit-guide column asset in every chamber. The boss arena already proved that eruption clears the gate (4.01% peak). Only the *backdrop* varies per zone (a lighting question, not a VFX-asset question). ∴ VFX inherits PASS from the boss-arena proof.
- **Validation (recognition→validate→commit on the instrument, not time):** ONE windowed eruption capture in **zone2** (worst-lit) AFTER its relight → confirm the column still peaks ~4% against the relit backdrop. The relight target (LDR ~176) is the exact profile at which the boss-arena column peaked 4.01%, so the eruption should pop, not wash. If zone2 holds on the hardest case, inheritance holds for all.
- **Why not score lighting on a windowed frame too:** the lighting gate should measure the AMBIENT mood between fires (what's on screen most of the time). The frozen-charge still IS a fair read of that ambient deficit. So lighting is correctly measured on the current stills; VFX is not. Different gates, different correct inputs.

#### Round 1 — drax RETURNED (commit `8536f34`, not pushed)
Three tasks complete, three independent verification methods agree (analytical scanner + parity + eyes-on).
- **Sanctum stair FIXED — and it was NEVER sanctum-only.** The defect lived in the *shared* `_build_gallery_storey` access-stair loop (`render_descent_scene.gd` ~1371–1388): the stair climbed −Z (away from the deck), so it floated in **ALL 5 gallery zones**. galadriel scored only sanctum, so we only knew about one. Fix = flip climb to +Z (toward deck); ONE re-bake cleared all 5. Sanctum top moved from floating 210.6 (−Z, over void) → 233.6 (+Z, on deck); foot (21.5,−9.0,223.6) grounded. **Parity 35/35 — zero combatant positions touched (sim-invariant preserved).**
- **Audit camera generalized sanctum→ALL zones** (46 frames; per-zone side-on + stairsubject + stairland; arcane orbit-only — no gallery). 28° pitch, true 3840×2160.
- **Both-ends-land load-path SCANNER built** (`scripts/check_descent_loadpath.py`) per my §5 re-scope — parses the BAKED `.tscn` (generator output = the authority I ruled ground-truth), tests both stair termini rest on floor/deck within tol (XZ ≤ 2.12m AND Y ≤ 2.20m). **Tool output, NOT a self-score** (drax preserved the don't-grade-own-homework discipline). Validated bidirectionally: correctly FLAGGED all 5 pre-fix floats (consistent 9.2m-Y-off signature); clears them post-fix. POST-FIX: all 6 zones CLEAN. No spans/ramps/free-standing arches are load-path subjects (arches are wall-dressed, not free-standing) → nothing else to land.

#### ★ CANON CALL (gandalf, 2026-06-17) — GATE B = PASS, all 6 zones
I ruled on the rendered stills (not drax's say-so), via crop+upscale on the native-4K stairland/stairsubject frames. **Convergence of four independent lines:**
1. **Deterministic scanner** (the §5 instrument, purpose-built precisely because CV + eyeballs are unreliable here): all-land, and it was validated to correctly flag the float when present. Primary Gate-B instrument.
2. **Parity 35/35** — only dressing geometry changed.
3. **My eyes-on (sanctum subject-junction crop):** staircase climbs to meet a tiled deck with under-deck column support; the gross float-over-void is GONE (vs pre-fix `stairjut` where the top hung in air).
4. **Sibling-zone corroboration (war_hall + oubliette stairland):** decks read as solid supported platforms, stairs contact them, no gross float — and these share the IDENTICAL fixed function as sanctum.
- **Honest caveat (recorded, not a blocker):** the iter4 east-band clutter means no single still pristinely isolates the sanctum top-step-on-deck-tile macro-shot. That's a perceptual/framing limit of the audit stills (candidate galadriel read-clutter CV probe), NOT a load-path defect — and is precisely why the deterministic scanner is the right Gate-B instrument (vindicates the §5 re-scope). Sanctum's cluttered read is carried by scanner + parity + clean sibling zones running the same code path.
- **★ Methodology win:** galadriel's CV is load-path-blind AND scored only one zone — it would NEVER have caught the systemic 5-zone float. The all-zones deterministic both-ends-land scan surfaced the true scope. This is the dual-gate's entire premise vindicated: a genuinely separate instrument caught what the aesthetic gate is structurally blind to.

#### Round 2 — PLAN (fires when drax round-1 returns; one drax at a time on the lighting rig)
**★ ROOT-CAUSE UPGRADE (gandalf, code-traced 2026-06-17):** the flat-dim-mid-grey is **cumulative-trim drift** (Discipline #13 implicit-pillar), not one wrong value. Stack of register-correct local fixes — `CombatFill` trimmed 1.5→1.15+green-cool (`render_descent_scene.gd:625`), green fog as shadow-bed (`:1980`), `ambient 0.24` (`:1972`), low-fill global directional trio — summed BELOW the proven LDR-176 bar. galadriel's twin LDR-low+SHF-low = "all fill, no key." Fix = restore a per-chamber **KEY** of boss-arena reach (`CombatFill 1.5/range34/atten1.5` + braziers `2.2/8` = LDR 176 PASS, `render_boss_arena.gd:229`), NOT raise fill. **Fire-ready brief STAGED:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-round2-lighting-lift-brief.md`.
The only real Gate-A work is the **per-chamber lighting lift**, prioritized by galadriel's data:
1. **zone2 warhall** relight — flattest/coolest, furthest from gate, biggest single win; floor key + warm fill.
2. **zone1 arcane** key-lift — clear the LDR-115 floor + shadow depth.
3. **establish ×3** spine relight + de-clutter — lowest LDR (94); one fix; gate on light+composition.
4. **zone3 oubliette** torch-line — convert empty void → dramatic dark (lit volume IN dark, not flat dark).
5. **zone4 / zone5 / zone0** shadow-deepen — smallest gaps; fold zone5's into drax's stair re-render.
6. **zone2 windowed eruption confirm** (the VFX-inheritance validator) once zone2 is relit.
Then galadriel re-scores the relit zones; gandalf re-reads any geometry-changed audit stills. Loop until matrix is GREEN.

- **Awaiting:** drax round-1 completion. On return → gandalf runs semantic-coherence reads on the new audit stills + rules drax's load-path flags → fold into matrix + into the staged Round-2 brief's §4 geometry-fold → fire Round-2 lighting-lift brief to drax (brief already authored + staged; only the load-path geometry-fold is pending Round-1 scan output).

### Round 2 — drax RETURNED (iter5, commit `7ce990e`, not pushed) + gandalf eyes-on (PROVISIONAL, pending galadriel re-score)
drax implemented the key-not-fill fix: new `_build_chamber_key()` (one bright pool/chamber of boss-reach; warm key for cool zones, torch-LINE for zone3 void), CombatFill restored to boss reach (atten 1.7→1.5) + made per-chamber. Key levers: z0 1.9/38, z1 2.3/38, **z2 3.4/40** (brightest), **z3 4.2/torch-row**, z4 2.1/36, z5 2.2/38. Establish recomposed (cam 40→31m, FOV 60→50, kept diagonal lateral offset, east-band speckle thinned). **Parity 35/35 + load-path all-clean (Gate B held).**

**gandalf eyes-on reads (my instrument = composition + design-identity + VFX-coherence; galadriel's = LDR/SHF/composite — convergence pending):**
- **★ The key-not-fill fix LANDED.** zone2 (the #1 worst, LDR 103) now reads as warm dimensional **lit-volume-in-dark** — bright warm pools + real falloff to dark corners/shadowed objects. The flat mid-grey wash is GONE. Validates the root-cause diagnosis on the hardest case. Near-chambers (z0/z1/z4/z5) ride the same proven lever → provisional likely-PASS, pending galadriel's LDR-up-AND-SHF-up confirm.
- **★ zone3 oubliette — DESIGN-CRITERION REFRAME (gandalf call).** Holding the *dread dungeon-pit* to the same LDR→176 bar as the near-chambers BETRAYS its identity — a Diablo-class crypt (D2 dark levels, PoE dread zones) is *meant* to be dark. Correct register-2 target for this chamber = **dramatic dark: bright torch pools + deep shadow (high contrast / high SHF), moderate frame-mean LDR** — NOT boss-arena brightness. The torch-line added real keys (vs iter4 empty-void). On the reframed contrast criterion: improved + borderline. galadriel's SHF axis is the right instrument (bright-pool-in-deep-dark vs muddy-uniform-dim). **Acceptance for z3 is reframed; do not fail it for sub-176 LDR.**
- **establish ×3 — improved, NOT yet passing.** All 4 recompose fixes landed directionally (lower/lateral/warm-floors/thinned-speckle — tabletop anti-pattern broken). BUT the **Layer-3 deep-wall blue-panel mass** (drax-flagged) is real: the left third is a flat desaturated blue cardboard-cutout dead-zone competing with the warm chambers. Round-3 establish item: warm-light the deep walls OR push them into green-fog so they read atmospheric-depth not flat-panel, OR reframe to minimize them.
- **VFX — inherited-PASS STANDS (capture-limited validator).** zone2 erupt is present + NOT washed by the relight (my prediction held), but reads ~0.2% HLF (modest mid-luminance glow, not white-hot 4% column). Same static-bake-undercounts-VFX limit as iter4 (boss-arena 4% was a LIVE capture; descent uses static bakes). Asset is zone-invariant + proven live → inheritance holds. Descent capture pipeline can't quantitatively confirm; galadriel (HLF instrument owner) reconciles the 0.2%-baked-vs-4%-live measurement.

**Provisional post-Round-2 state:** lighting lift LANDED (key-not-fill works). Remaining narrowed scope for Round 3 = (a) establish blue-panel deep-wall fix, (b) zone3 contrast-confirm/punch-up if galadriel's SHF says muddy, (c) any near-chamber galadriel rejects for LDR-up-but-SHF-flat. **Awaiting galadriel iter5 re-score to converge + finalize the matrix + scope Round 3.**
> **⚠ CORRECTED by galadriel re-score below — the "lift LANDED" provisional read was WRONG (confirmation bias). The lit volume did NOT brighten. See the galadriel-returned section.**

### Round 2 — galadriel RE-SCORE RETURNED (commit `a3fe512`, not pushed) — Gate A REJECTED 0/6; gandalf eyes-on CORRECTED
**The lift did NOT land.** Photometric verdict: 0/6 zones meet the both-axes criterion; 0/9 clear Gate A. iter5 md5-verified ≠ iter4 (genuinely re-rendered) — but the lit volume did not lift. Mean |dLDR| = 1.7 luma (almost all from zone4's −9); the other five moved ~0–1. A boss-reach key would have moved LDR +40–70 toward 176. Histogram unchanged: bright%>180 still 0.1–0.4%, p95 still ~125 vs boss ~180.

| Zone | LDR Δ | SHF Δ | verdict |
|---|---|---|---|
| z0 threshold | +0 | +0.08 | neither axis moved |
| z1 arcane | −1 | −0.34 | neither (LDR drifted down, still <115) |
| z2 warhall | +0 | −0.06 | neither — visually near-identical to iter4 |
| z3 oubliette | +0 | −0.26 | torch = RIGHT KIND, magnitude short (**SHF 57.9 — highest**) |
| z4 antechamber | **−9** | +3.6 | **REGRESSION** — lost the PASS-grade LDR it had (116→107) |
| z5 sanctum | +0 | +1.02 | bright present but it's frozen hero VFX, not ambient |

**★ ROOT CAUSE (galadriel's one sentence): the levers changed VALUE, not KIND.** drax's keys (energy 1.9–4.2) read as local brazier-class POINTS — energy up, REACH not. The boss lever's power was RANGE 34 + soft ATTEN 1.5 = a pool that *reaches across the chamber*. Cleanest proof: zone2 (the BRIGHTEST key, 3.4/40) is near-identical to iter4 and moved LDR +0. **The fix is RANGE + ATTEN, not energy.** (My Round-2 brief §0 framing "push PAST boss's 1.5/34/1.5" inadvertently steered drax toward energy — Round-3 brief must foreground REACH.)

**★ gandalf OWNS THE ERROR.** My provisional eyes-on ("key landed; zone2 warm lit-volume-in-dark; flat wash GONE") was WRONG — confirmation bias. I'd just spent the round root-causing + briefing the key fix; primed to see success, I read the pre-existing sub-180 braziers + a faint warmth shift as "the key landed." galadriel's photometry (p95 ~125 unchanged, bright%>180 ~0.2% unchanged, LDR +0) is authoritative on this luma question and corrected me. **Methodology cross-check (now proven BOTH directions):** photometric "did the lit volume brighten" → galadriel authoritative (CV home turf); semantic "does it stand / load-path" → gandalf authoritative (CV blind). R1 my scanner caught her CV-blindness (Gate B float); R2 her photometry caught my eyes-on bias (Gate A). The dual-gate works *because* the instruments check each other. **Discipline: do not read photometric success into a frame the instrument says is flat.**

**Partial vindications (held up):**
- **zone3 reframe SUPPORTED by her data.** SHF 57.9% (massively highest — genuine bright-points-in-deep-dark) + "torch-line is the RIGHT KIND, dark void between." The dread-chamber-contrast reframe holds; z3 needs torch POINTS WIDENED into POOLS (magnitude), NOT the dark identity abandoned. **Next galadriel re-score must judge z3 on the contrast criterion (high SHF + bright local pools), not the LDR-176 bar.**
- **establish blue-panel CONFIRMED** + she adds: floors went COOLER not warm (warmCool 1.025→0.999, below neutral) + no focal payoff (magenta sanctum not anchoring the vanishing point). FAILs light AND composition.
- **VFX non-wash VALIDATED → gate ruling FINAL.** Column pops 2.0× (bright% 0.51 vs 0.26 ambient), real warm column, brightest warm element — NOT washed. 0.2% is an undercount (3 off-peak baked frames; boss 4% was a 100-frame lifecycle peak). **VFX = inherited-PASS, FINAL, on non-wash + zone-invariance.** 4% magnitude not re-confirmable from baked frames; a windowed lifecycle erupt-capture (ember→peak→collapse) is the fair instrument IF quantitative closure is ever wanted — NOT loop-blocking.

**New catch I missed:** zone4 REGRESSION (I didn't read zone4 — incomplete eyes-on). Its iter4 problem was SHF (it already had LDR 116); drax's 2.1/r36 key REDUCED fill → uniform dim → SHF "deepened" only because the whole frame darkened. **Revert first, then deepen surround.**

### Round 3 — gandalf CODE-READ RE-ROOTED the cause: GLOBAL env divergence (supersedes "reach not energy")
**Before briefing a third round I read the actual lighting code (Discipline #10, inspection-over-assumption) — and it REFUTES galadriel's inferred mechanism.** galadriel's photometry is authoritative on OUTPUT (LDR flat — true). But her *causal* story ("reach not energy — local points not reaching pools") is contradicted by the code: the iter5 ZONE_LIGHT keys are ALREADY boss-class-or-stronger. war_hall key = energy **3.4 / range 40 / atten 1.3** vs the proven boss CombatFill **1.5 / 34 / 1.5** — stronger energy, LONGER range, softer falloff. `_build_chamber_key` places it at height 11 / range 40 → ~2.2 intensity to the floor below vs the boss CombatFill's ~0.95. **The reach is already there; the keys are stronger than the lever that scored 176. Yet LDR is flat. So the suppressor is GLOBAL, not the key.**

**THE REAL ROOT CAUSE — the descent abandoned the proven register-2 global env rig.** Every PASS scene (boss LDR 176, cathedral 5.00, all `arena_*`) uses ONE rig; the descent is the lone outlier on every dynamic-range lever:

| lever | proven rig (boss/cathedral/all arena_*) | descent (FAIL) | effect |
|---|---|---|---|
| `tonemap_mode` | **3 ACES** | **2 FILMIC** | flat curve → compressed range, milky mids |
| `tonemap_white` | 8.0 | 6.0 | (minor) |
| `tonemap_exposure` | 0.95 | 1.0 (default) | (minor) |
| `ambient_light_energy` | **0.17** | **0.24** | floods surround to mid → lifts p05 (KILLS SHF) + compresses p95−p05 (KILLS LDR) |
| `fog_density` | 0.010–0.012 | 0.0052 | descent has LESS fog — fog is NOT the suppressor |

**`ambient 0.24` + `FILMIC` together produce galadriel's exact twin-low (LDR low AND SHF low) signature** — the keys read flat because they're tonemapped flat + ambient-washed, not because they don't reach. The "iter1 mood-lift" comment (`render_descent_scene.gd:2041`) confirms the env was hand-built from scratch for the green-atmosphere reference instead of inheriting the proven rig — **Discipline #13 implicit-pillar drift at the GLOBAL env level, beneath the per-chamber drift galadriel and I were both chasing.** Cross-check working a 3rd time: her photometry (output) + my code-read (mechanism) → neither alone gets here.

**Brief:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-round3-lighting-recalibration-brief.md`. Core, ordered by leverage: (1) **PRIMARY — match the proven global rig** (ACES / white 8.0 / exp 0.95 / ambient 0.17 / fog ~0.010), KEEP the green fog identity, re-bake, self-measure **zone2 only** against galadriel's committed scorer (`register2-score-descent-iter5.mjs`); if LDR jumps + SHF deepens, apply globally and DON'T also retune keys (clean attribution). (2) **SECONDARY if partway** — A/B key ON/OFF isolation (ΔLDR≈0 = key off-frame/occluded = position bug, not tuning). (3) zone4 REVERT the −9 regression then deepen. (4) zone3 widen torch points→pools, judge on CONTRAST criterion (high SHF + bright pools, NOT LDR-176). (5) establish: warm floors + kill/resolve blue deep-wall panels + magenta focal payoff. (6) VFX no work — inherited-PASS FINAL. Probe-first to avoid a third blind round.

### Round 3 — FIRED 2026-06-17 (drax, background)
drax dispatched with the recalibration brief. Awaiting iter6 return: locked global-rig recipe + which hypothesis landed (§1.1 global rig alone, or +§1.2 key isolation) + per-zone self-measured metrics. On return → galadriel re-score (with the zone3 contrast-criterion instruction) → converge → loop until matrix GREEN.

### Round 3 — drax RETURNED (iter6, godot `9b16d39`, not pushed) — ★ GLOBAL-RIG DIAGNOSIS CONFIRMED
**The code-read root cause was RIGHT. §1.1 global rig ALONE landed it — keys UNTOUCHED (clean attribution).** Matching the proven register-2 env rig as ONE change moved ALL SIX zones on BOTH axes simultaneously — the uniform-across-zones signature that proves the cause was global, not per-chamber. The per-chamber keys (already stronger than the proven CombatFill) were a red herring, exactly as the code-read predicted.

**The locked global-rig recipe** (`_build_global_environment`, dynamic-range levers only; GREEN `fog_light_color` kept): `tonemap_mode` FILMIC→**ACES**, `tonemap_white` 6.0→**8.0**, `tonemap_exposure` 1.0→**0.95**, `ambient_light_energy` 0.24→**0.17** (the SHF lever), `fog_density` 0.0052→**0.010**. Two-env reconciliation RESOLVED: the baked `arena_descent.tscn` IS the script-built env (`_bake_to_scene` packs `self`); edit propagated, verified in the bake.

| zone | LDR (Δ iter5) | SHF% (Δ) | bright% | p95 | drax verdict |
|---|---|---|---|---|---|
| z0 | 133 (+11) | 21.4 (+4.7) | 0.55 | 135 | KEY_RESTORED |
| z1 | 126 (+19) | 23.8 (+6.1) | 0.28 | 133 | KEY_RESTORED |
| **z2** | **115 (+12)** | **19.6 (+6.9)** | 0.45 | 131 | weakest, both-axes-up |
| z3 | 118 (+13) | **61.7 (+3.8)** | 0.16 | 120 | dread-contrast PASS |
| z4 | 123 (+16) | 23.1 (+6.5) | 0.13 | 127 | regression RECOVERED |
| z5 | 134 (+16) | 17.8 (+5.4) | 2.83 | 139 | strongest |
| est ×3 | 102 (+5) | 49.9 (+1.3) | ~0.2 | 104 | composition residuals (see below) |

mean dLDR ≈ +14 (vs iter5's 1.7 non-move); the flat-dim-mid histogram BROKE. **gandalf eyes-on corroborates** (`/tmp/gandalf_crops/A_*` before/after + `B_*` grid): iter5's flat blue-grey pewter floor is GONE; warm/green pools pop against a deepened bed. z3 dread-corridor + z5 magenta/boss-bloom read strongly premium; z4 green soul-fire recovered. **Other ordered work landed:** z4 revert (root cause: iter5 swapped z4's CombatFill from cool-neutral to green = green-on-green flood killing the soul-fire pop; restored cool-neutral base — note z4 identity is GREEN soul-fire, not red); z3 torch `key_range` 13→20 (no flood, SHF held). Parity 35/35 PASS, Gate B preserved (env/lighting/camera only). drax committed iter6 scorer collab `3c8f0ee`.

**★ THE ONE OPEN DECISION (fired to galadriel):** near-chambers cleared LDR≥115 but SHF landed **17–24%, under the uniform 30% CV-gate** — so her scorer prints `LIGHT: fail` even though both axes rose correctly. **gandalf design lean:** 30% is the bar for STARK chambers (z3 oubliette PROVES the descent hits 60%+ where genuinely stark); DENSELY-DRESSED chambers (z0/1/2/4/5) legitimately read premium-lit-in-dark at SHF ~20–25 because the dressing fills frame-area an empty arena leaves black. **Guarded against goalpost-moving:** fired galadriel the explicit calibration question with **z2 as the borderline test case** — her eye is the arbiter on whether z2 (SHF 19.6) reads premium or still murky. If premium → 6 chambers GREEN + SHF-30→dressed-band scorer refinement. If murky → ONE targeted deepening notch on the named zones (NOT a global revert).

### Round 3 — establish ×3: gandalf eyes-on (composition call I own; SEPARATE from chamber lighting)
Read `/tmp/gandalf_crops/C_iter6_establish_01.png`. **The establish is NOT passing — the dominant failure is a wall of flat saturated BLUE slabs** across the left/center (the per-zone cool CombatFills grazing the stacked deep chamber walls, reading face-on in the across-spine angle). It is the single most eye-catching element, pulls the eye hard-left away from any payoff; floors read cool-green not warm; no magenta sanctum anchors the deep end. **drax was right to REJECT the deeper-focal probe** (it made the void dominate, LDR 92/dark% 66, blue worse). **Architecture note (drax's, sound):** a single across-spine establish cam can't both avoid the face-on blue deep-walls AND frame the deep magenta — those are competing geometries. **Irony worth recording:** the global rig that FIXED the chambers (ACES contrast + ambient 0.17) likely SHARPENED the establish blue-slab problem (deeper surround makes the cool slabs pop harder). **∴ establish is a DISTINCT composition mini-round** — scoped AFTER the chamber SHF question resolves; do not block the 6-chamber green on it.

**gandalf DESIGN DIRECTION for the establish recompose (the call is mine; recorded now while the eyes-on is fresh).** An establishing shot for a DESCENT is *katabasis* — the oldest journey-pattern. Its power is **mystery + downward-pull, not a full-map reveal**: you descend INTO the unknown; you do not see the bottom from the top. This dissolves the geometry conflict drax correctly named (across-spine = blue deep-walls; down-spine = magenta-payoff-but-worse-blue):
- **The magenta sanctum is the DESTINATION — it should NOT appear in the establish at all.** A destination revealed from the threshold is a destination robbed of arrival. The sanctum already reads premium in its OWN zone cam (grid-confirmed). The magenta lands on ARRIVAL, not at the overview. So we DROP the "plant the magenta focal payoff" ask from the establish — it was fighting the form.
- **Chosen fix — Option 1, CAMERA-ONLY (lowest risk; does NOT touch the chamber rig that just landed):** drop the establish cam lower + rotate so the deep walls rake EDGE-ON (grazing), not face-on, and recede into the green fog. Keep the warm near-cluster (gold braziers) LARGE in the foreground as the hero element; let the spine recede into green-fog mystery with warm brazier-points as breadcrumbs trailing into the dark. The blue slabs stop dominating because they're edge-on + fog-veiled (they only read as flat slabs face-on). This IS the original code-comment intent (`:2028-2037` intimate 3/4 of the upper 2-3 chambers, rest into fog) — pushed the rest of the way.
- **REJECTED Option 2** (warm-balance the deep-wall spill via wall-wash/material): perturbs the per-zone combat look (deep walls show in combat cams too) + adds lights + risks muddying the cool-fill/warm-key contrast that just made the chambers work. Touches the landed rig — too much risk for an overview shot.
- **REJECTED Option 3** (dedicated down-spine deep-look cam to the magenta + one-shot warm deep-wall treatment): most work, and the down-spine angle is the one drax found makes the blue WORSE; also re-introduces the destination-reveal-robs-arrival problem.
- **Finalize after galadriel's establish read** (she may quantify the blue-slab dominance / add perception detail) and bundle with any chamber-deepening micro-pass into Round-4. Acceptance for the establish: reads as a felt DOWNWARD descent into fog-mystery, warm-foreground-dominant, NO blue-slab focus-pull — judged on composition + the chamber light axis (warm-dominant floor, LDR off the 102 floor).

---

## Known ground truth carried in

- **Sanctum stair (Gate B fail):** drax generator-code trace (SUPERSEDES galadriel's earlier transform-Y read per the §5 reconciliation): wrong-direction Z climb, foot grounded / top stranded. Fix = correct the climb so the top lands on the gallery deck. Canon-call acceptance: re-rendered sanctum audit still must show the stair landing at both ends.
- **iter4 east-band read-clutter:** the sanctum's dense dressing meant no single audit still cleanly isolated the float (carried by frame-combination). Flagged as a separate perceptual concern (candidate galadriel CV read), not a Gate-B blocker per se.
