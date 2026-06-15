# Visual-Register Scorecard — Parametric ArenaRoom 6-Room Corpus vs Register-2 Rubric + Readability-Axis Proposal

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf "spec-driven multi-footprint A-holds extension" canon call)
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING + READABILITY-AXIS PROPOSAL. Measures drax's single **parametric** ArenaRoom (godot `3855b6b`) — which reads `arena.py::ALL_SCENARIOS` as data and renders all 6 battle footprints off ONE constant lift rig — against galadriel's register-2 rubric, lifecycle-sampled. Plus the first draft of an additive **fight-readability axis** (deferred from the Build #1 scorecard until 3+ rooms existed; the loop now delivers all six). Does **NOT** make the canon call — that is gandalf's, on this evidence.
**The design claim under test:** *"one spec-driven room holds the register across EVERY footprint."*
**Brief:** parametric-ArenaRoom scoring increment (self-contained invocation, 2026-06-15). drax run-log: `reincarnated-godot/harness_logs/14_arena_room_parametric.log`.
**Companion:** instrument `agentic_orchestration/galadriel/pipeline/lifecycle-score-corpus.mjs` (+ shared `register-metrics.mjs` defs); raw scores `pipeline/lifecycle-scores-corpus.json`. Capture frames + contact-sheet are **git-ignored Synty-derivative IP — local evidence only** (not committed; described here). Precedents (CALIBRATION baselines, NOT pass bars): graybox lift 4.50, Synty cathedral 5.00, Build #1 boss-arena 4.00.

---

## 0. What was scored

- **Corpus:** `reincarnated-godot/harness_logs/arena_<scenario>_01..100.png` — 6 scenarios × 100-frame motion sequences, 1152×648, Godot Movie Maker. Glob confirmed self (harness-owner): all 6 corpora present, 100 frames each. Scenarios: `boss_with_adds` (30×30), `elite_pack` (28×28), `mini_boss` (30×30), `open_arena` (50×50), `magic_pack` (32.7×14), `chokepoint_corridor` (10×50).
- **Architecture (the load-bearing property):** ONE parametric room (`render_arena_room.gd` + `arena_room.tscn`) consumes the same `ALL_SCENARIOS` spec the `SpatialFightEngine` runs — parity-by-construction (six bespoke scenes could drift; one parametric reader cannot). Constant lift rig across all rooms (NOT re-tuned per room). Camera-aspect rule (3 branches: near-square / wide-shallow / long-corridor). Hero-VFX anchor rule: most-threatening present entity, else **room-center bloom** for the two all-swarm rooms.
- **Scoring method:** CV instruments run **across the full 100-frame lifecycle per room**, NOT a single still (galadriel F1: stills under-represent VFX, the highest-leverage axis). Gate-relevant reads are whole-sequence LDR/SHF means + floors and HLF peak. Each room's HLF curve votes its own lifecycle markers (ignition / peak / collapse capture-frame). Manual axis scores authored from direct inspection of peak-bloom + calm(ember) frames per room.
- **Parametric parity check:** the `boss_with_adds` re-render through the parametric path reproduces Build #1 within tolerance — LDR 175.93 (vs Build #1 175.97), HLF peak 3.838% (vs 4.013%), SHF 42.51% (vs 42.74%). Parity-by-construction **confirmed at the register level**; the parametric path is loss-less to the validated baseline.

## 1. The rubric (UNCHANGED from lift / cathedral / Build #1)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY**.

| Axis | Target | Instrument (CV-assist) |
|---|---|---|
| Lighting drama | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% |
| VFX presence | manual ≥ 4 | ≥ 1 hero bloom, HLF ≥ 1.5% |
| Material-shading | manual ≥ 4 | gradient/light-response, NOT flat per-face |
| Geometry register | manual ≥ 3 | low-poly fine; silhouettes legible |

NOT targets: high-frequency-detail / strong-edge%. Premium ≠ detail-density. Same rubric applied to all prior scorecards → directly comparable. **Fight-readability is scored SEPARATELY (§ 5) — additive, not folded into the register composite.**

## 2. CV instrument values (lifecycle-sampled, whole-sequence)

Instrument defs **BYTE-IDENTICAL** to `register-metrics.mjs` / all prior scorers (960w inside-fit, gray luma, raw RGB sat; HLF>0.80, SHF<0.12, LDR=p95−p05). HLF markers: ignition = first frame HLF crosses 1.5% rising; peak = argmax; collapse = last frame ≥1.5%.

| Scenario | class | LDR mean | LDR floor | SHF % | HLF peak | ×thr | LMV | ign/pk/col |
|---|---|---|---|---|---|---|---|---|
| boss_with_adds | near-square | 175.9 | 148 | 42.51 | 3.838 | 2.56× | 32.66 | 9/61/87 |
| elite_pack | near-square | **181.6** | 155 | 41.44 | **4.004** | 2.67× | **35.47** | 9/74/87 |
| mini_boss | near-square | 173.1 | 149 | 42.52 | 3.038 | 2.03× | 32.16 | 9/61/87 |
| open_arena | large near-square | **129.7** | **113** | 46.99 | **1.884** | **1.26×** | **23.60** | 11/78/86 |
| magic_pack | wide-shallow ⚠ | 171.0 | 138 | **76.09** | 2.377 | 1.58× | **16.44** | 11/85/87 |
| chokepoint_corridor | long-corridor ⚠ | 140.3 | 119 | **81.31** | 2.447 | 1.63× | **17.08** | 9/73/87 |

**CV-assist gate check** (LDR mean&floor ≥115 | SHF mean ≥30% | HLF peak ≥1.5%):

- **boss_with_adds / elite_pack / mini_boss:** ALL PASS, comfortable margins (HLF 2.0–2.7×).
- **magic_pack / chokepoint_corridor:** PASS all CV checks (HLF 1.58–1.63×; very high SHF = very dark).
- **open_arena:** LDR **floor 113 < 115** (mean 129.7 passes); HLF peak **1.26×** — the corpus minimum on both lighting drama and bloom strength.

## 3. Per-room manual scores + gates

Manual axis scores from direct frame inspection (peak-bloom + ember per room); CV table § 2 is the evidence basis.

| Scenario | Lighting | VFX | Material | Geometry | **Composite** | Gates (L≥4 ∧ V≥4) | **Verdict** |
|---|---|---|---|---|---|---|---|
| boss_with_adds | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** |
| elite_pack | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** (corpus-strongest CV) |
| mini_boss | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** |
| magic_pack ⚠ | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS | **PASS** (weak) |
| chokepoint_corridor ⚠ | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS | **PASS** (weak) |
| open_arena | 4 | **3** | **3** | 4 | **3.50** | PASS ∧ **FAIL** | **FAIL** |

**Per-room rationale (the deltas that matter):**

- **boss_with_adds / mini_boss (4.00):** clean near-square rooms; anchor entity (boss/mini-boss) carries a body-anchored column (HLF 2.0–2.6×); 4 combatants in a readable spread; LMV 32 (Base-kit band). Identical profile to the validated Build #1.
- **elite_pack (4.00, corpus-strongest):** highest LDR (181.6), highest HLF (2.67×), highest LMV (35.47 — approaching the cathedral's 36.4). The 28×28 footprint fills the frame densely with combatants + lit floor; the elite ANCHOR (not a magic add) correctly takes the marquee column (confirms the elite>magic anchor rule). Held at 4/4/4/4 for rubric consistency (still Base-kit surface, not carved-cathedral), but it is the strongest room in the corpus on every CV axis.
- **magic_pack (3.75, weak PASS — RISKY footprint):** clears both mandatory gates (lighting 4 @ LDR 171/SHF 76%; VFX 4 — the caster-leader column anchors at HLF 1.58×). **Material drops to 3:** the wide-shallow camera (fov 55, stepped back for the 32.7m width over a shallow 14m depth) leaves ~76% of the frame as black void — the lit tray "floats" in black, dragging whole-frame LMV to 16.44 (corpus min). The premium-surface quality is real but confined to a small lit band. Composite 3.75 holds the register; the material/framing is the soft spot. **Combatant readability is GOOD** (figures reasonably sized + separable; § 5) — the black surround is a *premium-framing* issue, not a readability one.
- **chokepoint_corridor (3.75, weak PASS — RISKY footprint):** clears both gates (lighting 4 @ LDR 140/SHF 81%; VFX 4 — room-center bloom at HLF 1.63×, **placed at the choke** — a readability bonus). **Material 3:** same black-surround dilution (81% dark, LMV 17.08). **Geometry is a WIN:** the interior choke geometry (two wall stubs narrowing 10m→5m bottleneck) renders + reads clearly as a bottleneck — the one room with fight-relevant *interior* geometry, and it is legible. The engagement-band camera (high, steep tilt) frames the near fight readably; deep swarmers go small (expected — this prefigures the playable follow-cam). **PASS, and the choke legibility is the standout positive of the corpus.**
- **open_arena (3.50, FAIL):** the lone failure. **Lighting holds at 4** (LDR mean 129.7 clears the instrument; SHF 47% + perimeter braziers + dark surround give a lit-volume-in-dark read — the *weakest* of the corpus but it clears). **VFX FAILS at 3:** the room-center bloom in the full-footprint 50×50 frame reads as a small distant flare — HLF peak 1.26×, roughly HALF the relative magnitude of every other room; it does not carry register-2 without an entity anchor AND without tight framing. **Material 3:** the large mid-lit empty floor dominates (LMV 23.6). **Geometry 4** (the room itself is clean + legible — the failure is combatant SCALE, which is readability, not geometry-register). Composite 3.50 < 3.6 AND VFX gate fails → **register-2 FAIL.**

## 4. Corpus roll-up — the verdict on the design claim

**The claim "one spec-driven room holds the register across EVERY footprint" is ALMOST proven — it holds on 5 of 6 footprints and FAILS on exactly one (open_arena, 50×50 all-swarm), for an isolable, footprint-driven, NON-generic reason.**

- **5/6 PASS** register-2 (composite ≥3.6 + both mandatory gates): all three near-square rooms (4.00) + **both flagged-risky footprints** (magic_pack 3.75, chokepoint 3.75). That the two *predicted-hardest* footprints both PASS is the strong result: the single parametric camera-aspect rule + one lift rig **does** generalize across radically different shapes (near-square, wide-shallow, long-corridor).
- **1/6 FAIL** (open_arena), and the failure ISOLATES cleanly:
  - **Failing axis: VFX** (3 < 4) — the room-center bloom is too small in the full-50×50 frame to carry register-2.
  - **Footprint-driven, NOT a generic recipe miss.** The proof: `chokepoint_corridor` is ALSO all-swarm with the SAME room-center-bloom rule — and it PASSES VFX (HLF 1.63×) because its engagement-band camera frames the bloom tightly. The ONLY difference is the camera branch: open_arena's "contain all 50×50" choice shrinks the central bloom (and the combatants) below carrying strength; the corridor's "frame the engagement band" choice rescues it. **The single point of failure is the open_arena camera branch, not the recipe and not the swarm-anchor rule.**
  - **Isolable fix path (galadriel evidence; the call is drax's/gandalf's):** apply the corridor's engagement-band framing philosophy to open_arena — frame the swarm CLUSTER, not the whole 50×50 footprint. That would lift the bloom fraction (VFX), enlarge the combatants (readability — see § 5), and increase lit-surface fraction (material). One camera-branch change, no recipe touch. The "contain the whole footprint" instinct is what breaks at 50×50.

**Roll-up verdict:** the parametric recipe is **sound and footprint-general** — it carries register-2 across near-square, wide-shallow, and long-corridor footprints off one rig. The open_arena failure is a **camera-branch finding**, not a recipe finding: the largest footprint needs engagement-band framing (like the corridor) rather than full-footprint containment. **gandalf's canon call** (does this extend A-holds to "spec-driven multi-footprint") should weigh that 5/6 is a strong generalization result with the 1 failure isolated to a fixable camera branch — not a recipe-level register failure.

## 5. The 2 risky footprints — focused reading

The brief flagged `magic_pack` and `chokepoint_corridor` as the empirically-risky footprints (they stress the single parametric camera-aspect rule + one lighting rig hardest). **Both PASS register-2.** Neither dropped below the gate; both landed at composite 3.75 (weak PASS). The shared soft spot is **material-shading (3)**, and it is the SAME footprint-driven cause in both: the non-square camera (wide-shallow step-back / corridor steep-tilt) leaves the majority of the frame as black void (SHF 76% / 81%), so the lit surface is a small band and whole-frame LMV collapses to ~16–17 (vs the near-square rooms' 32–35). **This is a premium-FRAMING artifact, not a material-QUALITY failure** — the lit band itself shades correctly; the black surround drags the frame-average down. Neither room's combatant-readability suffers from it (§ 5-readability below).

- **magic_pack:** the wider/lower camera angle actually gives reasonably-sized, separable figures; threat tiers (caster leader vs swarm) are distinguishable; the caster-leader column anchors the VFX cleanly. The concern is purely the "floating tray in black" composition weakening the premium-enclosed-room read.
- **chokepoint_corridor:** the choke geometry is the corpus's best *interior* geometry read; the bloom-at-the-choke is a genuine readability asset. Black surround same as magic_pack.

**Risky-footprint verdict: the predicted-hardest shapes hold register-2.** If the black-surround material dilution is to be tightened later, the lever is the non-square camera framing (pull the lit band to fill more of the frame) — a framing refinement, not a recipe change. Non-blocking.

## 6. Marketing-render caveat (carried 1:1)

The Synty marketing frames are a MOOD/CALIBRATION anchor, NOT a pass bar. Every score here is the BUILD against the RUBRIC, lifecycle-sampled, never pixel-matched. Prior scorecards (lift 4.50, cathedral 5.00, Build #1 4.00) are CALIBRATION baselines only. **Caveat: SATISFIED.**

## 7. Readability-axis proposal (NEW — additive; v0 across the corpus)

This 6-room corpus is the first material to define a **fight-readability axis distinct from premium-render register** (deferred from the Build #1 scorecard § 8 until 3+ rooms existed). The axis answers: *can the player parse the encounter?* — independent of whether the room looks premium. The two axes are genuinely orthogonal, and this corpus PROVES it: `magic_pack`/`chokepoint` are weak on register-material but strong on readability; `open_arena` fails BOTH — for the same root cause.

### 7.1 Proposed sub-criteria + metric definitions

| Sub-axis | Question | Proposed instrument (automated v1) |
|---|---|---|
| **R1 — Entity-vs-floor separation** | Can each combatant's silhouette be separated from the floor it stands on? | Project each spawn world-pos → screen; sample a patch at the entity centroid vs a floor annulus around it; Weber contrast \|L_ent−L_floor\|/L_floor + local edge energy at the silhouette boundary. **Aggregate = MIN across entities** (the least-visible combatant gates readability — the player must parse ALL of them). |
| **R2 — Parse-ability / angular size** | Is each combatant large enough on screen to parse as a figure (not a dot)? | Projected screen-space figure height (px) of the SMALLEST combatant; floor ≈ 12–15px below which figures become unparseable. **This is the metric that fails open_arena.** |
| **R3 — Threat-tier contrast** | Are threat tiers (boss vs elite vs swarm) visually separable? | Screen-space scale ratio between tiers (the figure-scale formula 1.3+0.6·r already encodes this) + marquee-anchor-VFX presence (boss/elite/mini-boss carry the column = a tier signal; swarm rooms get a room-center bloom = NO per-entity tier signal → tier-read degrades). |
| **R4 — Engagement-geometry legibility** | Is the fight-relevant geometry (choke, spawn spread, room shape) parseable? | Structural/manual: does the choke read as a bottleneck; does the spawn spread read as a coherent encounter shape vs undifferentiated sprawl. |

**v0 computation honesty (Discipline #4 — right tool; #11 — empirical):** R1 + R2 require projecting world spawn coords → screen space using the **exact per-scenario camera transform**. The near-square camera is documented exactly (pos(15,19,42)/look_at(15,1.2,16)/fov 39); the wide-shallow + corridor cameras are described only qualitatively in the run-log (fov 55 step-back; high steep tilt) — NOT as exact pos/look_at/fov. **A reproducible AUTOMATED v0 needs drax to emit the exact per-scenario camera transforms** (cheap, non-blocking — the loader already computes them; they just need logging). Pending that, this pass provides a **v0 MANUAL readability scoring** (galadriel looking carefully — defensible per my rubric methodology: manual 1–5 + rationale + frame evidence), plus the instrument spec above for the automated v1.

### 7.2 v0 readability scores (manual; 1–5)

| Scenario | R-read | Rationale (frame evidence) |
|---|---|---|
| boss_with_adds | **5** | 4 combatants, perfect spread (player front-center / boss back-center / adds at flanks), distinct silhouettes, ample size; column backlights the boss (R3 tier-signal present). |
| elite_pack | **5** | 4 combatants clearly separable; elite anchor + 2 casters + player at readable sizes; tier-read clean (elite column vs unmarked casters). |
| mini_boss | **5** | 4 combatants, clear spread + sizes; mini-boss column anchors the tier read. |
| magic_pack | **4** | Figures reasonably sized + separable against the warm lit floor; caster-leader vs swarm tier-read works; black surround is neutral to combat-parse. R2/R3 good; R4 (wide-shallow shape) reads. |
| chokepoint_corridor | **4** | **R4 standout** — choke reads instantly as a bottleneck (best interior-geometry legibility in the corpus); near combatants readable; far swarmers go small (R2 degrades with corridor depth — the follow-cam's job). |
| open_arena | **2** | **The outlier.** Swarmers are tiny scattered dots (R2 fails — full-footprint camera shrinks figures below parse size); hard to count or parse threat; room-center bloom gives no per-entity tier signal (R3 weak); 50×50 sprawl has no encounter shape to read (R4 weak). |

**Readability cross-finding (load-bearing):** open_arena fails BOTH register-2 (VFX) AND readability (R2 parse-ability) — and BOTH for the **SAME root cause: the full-footprint 50×50 camera.** The fix that rescues VFX (engagement-band framing, per the corridor) is the SAME fix that rescues readability (enlarges the figures). This is the strongest evidence that **readability and premium-register, while orthogonal as axes, share camera-framing as a common lever** — and that the open_arena camera branch is a single, high-leverage fix point. The other five rooms confirm the axes are orthogonal (magic_pack/chokepoint: weak-material + strong-readability), which is exactly why readability deserves to be a SEPARATE axis, not folded into the composite.

### 7.3 Recommendation on adopting the axis

Adopt R1–R4 as a formal additive readability axis for battle-room scoring, scored alongside (not inside) the register composite. **Gate request to unblock the automated v1:** drax emits exact per-scenario camera transforms to the run-log (non-blocking; one log line per scenario). Until then, manual v0 stands. Do NOT retrofit readability into the register composite — the corpus proves they diverge.

## 8. drax CV self-sanity & honest caveats

- **Parametric parity:** the parametric `boss_with_adds` re-render matches Build #1 within tolerance (§ 0) — parity-by-construction confirmed at register level.
- **open_arena FAIL is a camera-branch finding, not a recipe failure** (§ 4). Stated plainly so the roll-up is not mis-read as "the recipe doesn't generalize" — it generalizes on 5/6 including both risky shapes; the 50×50 needs engagement-band framing.
- **Readability v0 is MANUAL** (§ 7.2) — the automated v1 awaits exact camera transforms. Honest scope: galadriel-scored, defensible, reproducible-by-inspection; not yet instrument-reproducible.
- **Bootstrap JSON:** drax's `data/arena_scenarios.json` is a documented hand-copy of read-only engine data pending an engine-side emitter (rocket/star-lord, Matt-routed, NON-BLOCKING). Scored rooms reflect the spec faithfully; if the emitter later shifts any dimension, re-score is a single corpus re-run.
- **No HUD/UI chrome** (carried) — a live combat HUD would ADD readability load; out of scope here.
- **Cape-attachment pack gap** (carried from Build #1) — figures render cape-less (non-fatal); does not affect scores.

## 9. One-line read (evidence FOR gandalf's canon call, NOT the call)

**drax's single parametric ArenaRoom holds register-2 across 5 of 6 spec-driven footprints — all three near-square rooms (4.00) AND both predicted-hardest footprints (magic_pack 3.75, chokepoint 3.75, weak but clean PASSES) — off ONE constant lift rig + a 3-branch camera-aspect rule, with parity-by-construction to the validated Build #1. The lone FAIL (open_arena, 50×50 all-swarm, composite 3.50, VFX gate) isolates cleanly to the open_arena CAMERA BRANCH (full-footprint containment shrinks the room-center bloom below carrying strength), NOT the recipe and NOT the swarm-anchor rule — proven by the corridor, which uses the same room-center-bloom rule and PASSES because it frames the engagement band tightly. The new additive readability axis (R1 entity-vs-floor / R2 parse-ability / R3 threat-tier / R4 engagement-geometry; v0 manual) ranks the corpus boss=elite=mini_boss(5) > magic_pack=chokepoint(4) > open_arena(2), and reveals open_arena fails register AND readability for the SAME camera-framing root cause — high-leverage, single-fix-point. The design claim "one spec-driven room holds the register across every footprint" is proven for 5/6 with the 6th isolated to a fixable camera branch.**

## 10. Reproducibility

- Instrument: `pipeline/lifecycle-score-corpus.mjs` (loops all 6 prefixes; byte-identical instrument defs to `register-metrics.mjs` + all prior scorers; gate reads = whole-sequence means + floors + HLF peak; HLF markers vote per room).
- Raw scores: `pipeline/lifecycle-scores-corpus.json` (per-frame + whole-sequence + dark-window + rubric extracts, per scenario).
- Visual evidence (git-ignored Synty-derivative IP, LOCAL only — NOT committed): `harness_logs/arena_corpus_peak_contactsheet.png` (6 peak frames). Representative frames inspected: peak (boss 61, elite 74, mini_boss 61, open_arena 78, magic_pack 85, chokepoint 73) + ember (frame 1, all 6).
- Given the same 6×100 frames + this instrument, another galadriel-instance reproduces the CV values exactly (deterministic). Manual axis + readability scores are reproducible-by-inspection per the stated rationale; readability automated-v1 awaits exact per-scenario camera transforms (§ 7.2).

---

*galadriel SCORES. The canon call — whether the parametric room extends A-holds to "spec-driven multi-footprint" (5/6 register-2, both risky footprints holding, the 1 failure isolated to a fixable camera branch) — is gandalf's, on this evidence. Recognition fires on the SCORE, not the build.*

---

# ADDENDUM — RE-SCORE of drax's open_arena fix (godot `909364b`, captures 14:49)

**Trigger:** Matt re-fired galadriel after drax's brief `e3cd053` / log `15_arena_bake_and_open_arena_fix.log` — three changes to `render_arena_room.gd` only: (1) bake-to-scene, (2) open_arena camera + swarm-centroid bloom anchor, (3) ritual-circle placeholder flag → `false`. All 6 rooms re-captured. This addendum re-scores the FRESH corpus and SUPERSEDES §§ 3–4 above for the `909364b` captures (the original scores stand for the `3855b6b` captures).

## A.1 The fix-target (open_arena camera) WORKED — but the corpus REGRESSED

**Headline: all 6 rooms now FAIL the VFX gate. The corpus went from 5/6 PASS → 0/6 PASS.** This is a regression, not a fix landing. The hero-VFX bloom (HLF) collapsed to ~25–35% of its prior magnitude across EVERY room, including the three near-square rooms whose cameras were explicitly UNCHANGED ("EXACT Build #1 parity").

| Room | HLF peak prior (`3855b6b`) | HLF peak now (`909364b`) | LDR mean prior → now | VFX gate |
|---|---|---|---|---|
| boss_with_adds | 3.838 (2.56×) | **0.985 (0.66×)** | 175.9 → 165.2 | PASS → **FAIL** |
| elite_pack | 4.004 (2.67×) | **1.215 (0.81×)** | 181.6 → 171.6 | PASS → **FAIL** |
| mini_boss | 3.038 (2.03×) | **1.159 (0.77×)** | 173.1 → 166.2 | PASS → **FAIL** |
| open_arena | 1.884 (1.26×) | **0.568 (0.38×)** | 129.7 → 125.4 | FAIL → **FAIL (worse)** |
| magic_pack | 2.377 (1.58×) | **1.008 (0.67×)** | 171.0 → 162.9 | PASS → **FAIL** |
| chokepoint | 2.447 (1.63×) | **0.448 (0.30×)** | 140.3 → 123.2 | PASS → **FAIL** |

## A.2 Causal isolation — the regression source is Change 3, NOT Change 2

**Clean isolation by construction:** Change 2 (camera + swarm-centroid) touched ONLY open_arena's camera branch + the open_arena/chokepoint marquee anchor. boss_with_adds, elite_pack, mini_boss cameras are byte-for-byte unchanged ("EXACT Build #1 parity," log §2a). Yet those three rooms' HLF dropped ~70%. **The only change that touched all six rooms is Change 3** — the ritual-circle placeholder flag (`USE_RITUAL_CIRCLE_PLACEHOLDER := false`) + the `_process()` glow-ramp decouple. Therefore the corpus-wide bloom collapse originates in Change 3.

The brief asserted "the DURABLE hero-VFX stay ON unconditionally." The empirical evidence contradicts this: the durable bloom (SummonGlow + SummonFireColumn) is now emitting ~⅓ of its prior highlight contribution. Either the now-disabled ritual-circle red ground decal + sigil was a far larger HLF contributor than the brief assumed, OR the glow-ramp decouple changed the column/glow intensity, OR the bake-freeze-at-CHARGE logic altered the capture-path erupt state. **Root cause is drax's to diagnose** (galadriel observes, does not modify) — but the data points squarely at the Change-3 block.

## A.3 What the picture SHOWS (empirical inspection, peak frames)

- **boss_with_adds f45 (peak):** braziers + cool CombatFill pool intact; the hero fire-column behind the boss is a **thin reddish wisp**, not the prior erupting bloom. The dark-mood register and figure-readability hold; the VFX is gutted.
- **open_arena f85 (peak):** the camera fix is **visibly working** — the engagement band (player bottom-edge → swarm cluster upper-center) is now framed at readable scale, and the bloom sits ON the swarm centroid, not the empty geometric center. But the bloom is a small faint warm patch. Change 2's framing succeeded; Change 3 starved the bloom it was meant to showcase.

## A.4 open_arena re-score (the fix-target room)

| Axis | Prior (`3855b6b`) | Now (`909364b`) | Note |
|---|---|---|---|
| Lighting drama | 4 | 4 | LDR mean 125 (>115), SHF 32.5% (>30); LDR floor 106 dips below 115 — borderline |
| VFX presence | 3 | **2** | HLF peak 0.38× — a wisp; the bloom regressed despite better framing |
| Material-shading | 3 | 3 | LMV 20.4 (large floor + black surround at pull-back) |
| Geometry register | 4 | 4 | Arena reads coherent; engagement band now legible |
| **Composite** | **3.50** | **3.25** | **FAIL** (VFX gate 2<4; composite 3.25<3.6) |

**open_arena net: framing improved, VFX magnitude regressed, composite DOWN 3.50 → 3.25.** The camera change is the right fix and should be KEPT; it is being masked by the corpus-wide Change-3 bloom regression.

## A.5 Recommendation (evidence FOR gandalf/drax, NOT the call)

1. **KEEP Change 2** (open_arena camera + swarm-centroid anchor) — proven to work; the engagement band is legible and the bloom is correctly placed.
2. **REVISIT Change 3** — the ritual-circle flag + glow-ramp decouple dimmed the durable hero-VFX ~70% corpus-wide, dropping all six rooms below the mandatory VFX gate. The durable SummonFireColumn/SummonGlow needs to carry the highlight contribution the disabled ritual-circle decal was evidently providing (raise column emission / glow energy / bloom strength so HLF peak clears ~1.5× across the corpus, as it did at `3855b6b`).
3. **Re-fire galadriel** after the Change-3 bloom is restored — a single corpus re-run re-validates all 6. The canon call on "one spec-driven room holds register across every footprint" should wait for that pass; on the `909364b` captures the answer is **0/6** and the design claim is NOT currently met.

**Mirror voice:** the camera learned to find the fire — and in the same stroke the fire was turned down. The eye is now pointed at the right place in every room; what it finds there has gone faint. Restore the bloom the circle was quietly carrying, and the corpus that held at 5/6 will hold again — this time with the sixth room finally framed to show it.

*Re-score authored on `909364b` captures. CV reproducible via `pipeline/lifecycle-score-corpus.mjs`; fresh raw scores in `pipeline/lifecycle-scores-corpus.json` (overwrote the `3855b6b` run — prior values preserved in git at the parent commit). Manual axis scores reproducible-by-inspection per the rationale above.*
