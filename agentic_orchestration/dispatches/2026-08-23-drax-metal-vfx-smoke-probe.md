# Dispatch — 2026-08-23 — drax — Metal VFX smoke probe (charter P0-b)

**From:** knight-rider
**To:** drax (presentation seam — `~/Games/reincarnated-godot/`)
**Approved by:** Matt — pre-authorized as phase **P0-b** of the Matt-launched VFX archetype-binding
run (charter ledger **L-1** launch word, 2026-08-23). No fresh Matt ask; KR sequences per L-4.
**Gate 1:** jack-ryan DESIGN-MODE, 2026-08-23 — **PASS-WITH-CHANGES**; all changes folded in before
publication (determinism grounding, HARNESS anomaly class, conditional NONDET disposition, calibrated
resource projection, tracked lineage table, MCP pre-authorization, MoltenVK pre-flight, pre-registered
revisit-trigger limbs, eye-verification requirement, crash/time-box/suspect-cap HALTs, tag correction).
**Estimated effort:** ~4–6 h (one focused session; 8–12 probe scenes + render passes + findings note)
**Acceptance:** a findings note with a per-effect table (wall-time, determinism measurement, anomaly
class) + the capture set, filed where P4 can consume it.

**Governing ruling:** **R-1(a)** (Matt 2026-08-23) — Mac Metal is renderer of record for the
prototype era. This probe supplies the *empirical* answer to whether Metal actually constrains VFX
work, before any cross-host (PC/Vulkan) infrastructure question reopens.

**Sequencing:** parallel-safe (non-blocking for run phases P1–P3). **Blocking input for P4 close** —
the T-A binding spec folds P0-b emitter/constraint notes in before the run seals. That is the
latest-acceptable landing.

---

## Context

Matt asked whether a PC-SSH-tunnel (Vulkan) lane was needed for VFX work. Gandalf drained the fork
to a ruling — Metal stays renderer of record — and parked the *empirical* half here. This probe
answers two questions with numbers and captures, not impressions:

1. **Feature integrity** — does the Metal renderer fail or visibly degrade any effect class we own
   (GPUParticles collision/turbulence, additive/blend stacking, trail meshes, beam shaders,
   soft-particle depth fade)?
2. **Throughput** — per-effect render wall-time under the standard capture harness. Would a VFX
   bake-off cadence (many candidate renders per session) actually bottleneck on this machine?

The revisit-trigger this arms is narrow: **only** a concrete Metal feature failure **or** wall-times
that measurably bottleneck bake-off cadence reopens the cross-host question. Otherwise the tunnel
stays retired. A "no findings" result is a full-value result — do not manufacture a finding.

**The complete diagnostic brief governs on any divergence from this dispatch:**
`agentic_orchestration/gandalf/notes/2026-08-23-metal-vfx-smoke-probe-brief.md`

---

## Required reading before starting

1. `agentic_orchestration/gandalf/notes/2026-08-23-metal-vfx-smoke-probe-brief.md` — **the brief; governs**
2. `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` § 4 (P0-b), § 5
   (HALT boundaries), § 7 (ruling ledger L-1..L-6)
3. `~/Games/reincarnated-godot/CLAUDE.md` — off-screen render rule, asset/license rule, commit discipline
4. `~/Games/reincarnated-godot/AGENT_STATE.md` — **specifically the 2026-08-01 BR-2 cell-5 entry**
   ("the renderer is NOT deterministic across processes on this clip"). This is load-bearing for
   § "Determinism is measured, not gated" below.
5. `~/Games/reincarnated-godot/scripts/run_spellfx_v1.sh` — the closest existing instrument to the
   pattern you are reproducing (Movie Maker → ffmpeg, Binbun VFX, git-ignored derivative outputs).
   **Read it as a pattern; do not modify it.**

---

## Math-before-code (Discipline #1) — do this first, in the findings note

Before mounting a single scene, write and commit the **selection rationale table**: which 8–12
effects, from which pack, and *which GPU feature class each one is there to stress*. The brief is
explicit that this is **deliberately worst-case, not a fair sample**. The table must show feature
coverage across at least: GPUParticles collision, turbulence/attractor, additive stacking, alpha-blend
stacking, trail mesh, beam/shader-driven, soft-particle depth fade. Any feature class you *cannot*
cover from the owned packs is itself a finding — name it as a coverage gap rather than silently
dropping it.

**Pre-fire resource-bounds projection (Discipline #1.1) — required before the first render.**
Declare, in the note, the projected capture footprint for both the PNG intermediate and the encoded
mp4, over `effects × renders-per-effect (≥2) × clip-seconds × fps` — **plus the MoltenVK cross-check
passes**, which are renders too and are easy to forget in the budget.

**Calibrate `frame-size`; do not assume it.** A scalar bytes-per-frame will mis-project by a large
factor here: lossless PNG of a neutral floor and of a full-screen additive bloom are not remotely the
same size, and you are deliberately selecting the blooms. Render **one** real effect first, measure
actual bytes/frame, then project from the measurement.

**Measure current occupancy yourself — do not inherit a stale number.** The 6.69 G-of-10 G PL-5
figure in the CP-B entry is stale; the galadriel capture tree measures **7.2 G** as of this dispatch
(with `reincarnated-godot/harness_logs/` a further 2.8 G). Real headroom is ~2.8 G and shrinking.
If your calibrated projection does not fit with headroom, the answer is **shorter clips and PNG
cleanup after encode**, not a bigger budget. State the measured footprint at the end against the
projection.

---

## Determinism is MEASURED, not GATED (read this before you write the gate)

**This is the one place this dispatch consciously diverges from the brief's literal wording, and it
diverges toward the brief's own intent.**

The brief § 3 asks for the house evidence chain including "SHA-256 determinism ×2." Your own
2026-08-01 BR-2 cell-5 finding says the renderer is **not** byte-deterministic across processes once
**runtime-spawned** VFX are in the frame — up to 2,305 lit px of drift from frame 100 onward, 58× the
40 px on-frame bar, surviving `--nodust --noambient --nohud`. Your unproven-but-fitting hypothesis:
`_cj_load` seeds emitters *at load*, and a node instanced at runtime cannot be seeded by a pass that
already ran.

A probe whose entire subject matter is VFX will therefore trip a hard SHA-256 gate for reasons that
have **nothing to do with Metal**. If that trip is logged as an anomaly, this probe produces a false
"Metal is broken" signal and the R-1(a) empirical track is poisoned at its source.

**Two entries in your own state file make this more than a judgment call** — the harness *does*
produce byte-clean output once free-running terms are peeled, and the VFX term is already isolated
by name:

- `AGENT_STATE.md:231` — with `--noking`, the same stage is **byte-identical across 3 processes and
  settle-invariant** (sha `fe9d95e2…`). The standing rule recorded there: any check that doesn't
  peel the free-running term "will read nondeterministic for a reason that has nothing to do with
  what it is testing." That is exactly this probe's exposure.
- `AGENT_STATE.md:3547` — `GPUParticles3D` per-launch nondeterminism is carried as a known term,
  "now peelable with `--nofx`."

Your probe scenes — neutral floor, no king, no dust, no HUD — are the cleanest isolation of that
third term anyone on this project has built. That is a side-benefit worth harvesting, not a hazard
to route around.

**This divergence is a METHOD NOTE in your findings, not a brief amendment.** gandalf ratifies it at
P4. No Matt ask, no run HALT — but state it plainly in the note so the ratification is a decision
and not an oversight.

**Therefore:**

- Run the render **twice per effect** as the brief says. Keep the SHA-256 comparison — it is free.
- A SHA-256 mismatch is **not a failure and not an anomaly**. It is a **datum**. Quantify it with
  `scripts/sa_gate.py` (`SA_REPEAT=<prefix>`, which measures the floor on the clip rather than
  reporting a pass) and record the **lit-px delta**, not just "differs."
- **If any effect is byte-identical ×2, that is itself a reportable finding** — it would bound the
  BR-2 hypothesis (load-seeded vs runtime-instanced) on a clean minimal substrate, which the
  full-scene clip could never do. Note which mounting style (preloaded in the scene vs instanced at
  runtime) each probe scene used, so the two cases are separable.
- **ffprobe gates stay hard** — frame count, duration, codec, resolution. Those are deterministic and
  a failure there is a real failure.

## Anomaly taxonomy — classify every anomaly into exactly one bucket

An unclassified anomaly is worthless to P4. Every anomaly you record gets exactly one of:

| Class | Meaning | Disposition |
|---|---|---|
| **M-FEAT** | Metal feature failure or visible degrade (missing particles, wrong blend, broken shader) | MoltenVK cross-check REQUIRED |
| **M-PERF** | Renders correctly, but wall-time is bake-off-hostile | No cross-check; report the number |
| **SCENE** | Our probe scene is wrong (bad transform, wrong camera, unlit, mis-scaled) | Fix the scene, re-render, don't report as Metal |
| **HARNESS** | The **new instrument** is wrong — ffmpeg args, Movie Maker settings, exit/watchdog | Fix the instrument; never a renderer signal |
| **NONDET** | Cross-process render variance per BR-2 cell 5 | Quantify in lit-px; **not** a Metal signal — *unless* MoltenVK is byte-stable on the same scene where Metal is not, which promotes it to M-FEAT |
| **ASSET** | The source asset is itself broken/authored-for-another-engine | Report; not a renderer signal |

**HARNESS is the most likely anomaly class in this run** and the easiest to misfile as M-FEAT — the
instrument is new and unproven, while everything else here is battle-tested. Known trap already paid
for once (`AGENT_STATE.md:2184`): **`--quit-after` is FRAMES, not seconds**, and the busy-gated
capture framerate is slow, so Godot idles long past capture-complete. The fix on record is an
explicit `get_tree().quit()` on phase-complete. Inherit that; do not rediscover it.

Note the NONDET disposition is conditional, not absolute. "Metal-specific nondeterminism" is a real
possible finding and the taxonomy must not define it out of existence by fiat — if MoltenVK is
byte-stable where Metal is not, on the same scene, that is an M-FEAT result.

**Cheapest refuting test per claim (Discipline #19.1):** before writing "Metal fails at X," name the
one test that would refute it. For M-FEAT that test is the MoltenVK re-render of the *same scene*
(`--rendering-driver vulkan`) — this disambiguates "our scene is wrong" from "Metal quirk" without any
PC involvement, which is exactly why the brief put it there. Suspects only; do not cross-check the
whole set.

---

## Pre-flight — resolve these two BEFORE authoring any probe scene

**1. Blind CLI is PRE-AUTHORIZED for this dispatch. Do not halt for MCP.**

`reincarnated-godot/CLAUDE.md:13–49` makes the godot-MCP live editor connection the default for "any
scene / node / rig / transform / alignment work," binds those tools at **process startup**, and
orders you to **STOP rather than fall back to blind CLI** when they're absent. By the letter,
mounting an effect with a fixed camera is transform-shaped, and you would be right to halt.

This dispatch invokes the same file's lines 67–71 carve-out — batch render sweeps and probe scripts
where **there is genuinely nothing to align**. A neutral floor, a fixed camera, and one effect is
that case. **Blind CLI `--rendering-driver metal` is authorized here; no editor required, no
relaunch.** If you hit something genuinely alignment-shaped mid-probe, that is a signal your probe
scene got too complicated — simplify it rather than reaching for MCP.

**2. Prove MoltenVK exists before you depend on it.** One throwaway `--rendering-driver vulkan`
render, first, before scene authoring. There is no evidence in-repo that this has ever run on this
machine — and it is the **only** refuting test for the entire M-FEAT class. If you discover it's
unavailable *after* collecting M-FEAT suspects, the acceptance criterion "or an explicit reason it
could not run" silently degrades into a rubber stamp on every Metal claim you make. Find out while
it's still cheap. If unavailable: that is a **finding** (it bounds the method), report it, and do
**not** substitute a PC lane.

---

## Cross-seam contract change? (Principle 6 gate — completed by knight-rider at authoring time)

Does this dispatch add, modify, rename, or remove any field on a telemetry schema table, a
`fight_log` dict key, a loadout dict key, an export packet structure, or any other inter-seam
fixture dict?

**NO.** `Round-trip: not applicable — no cross-seam contract change in this dispatch.` This is a
read-only diagnostic in the presentation repo. It touches no engine seam, no schema, no fixture.

---

## Scope

- [ ] MoltenVK pre-flight render (one throwaway) — before scene authoring
- [ ] Selection rationale table (8–12 worst-case effects + GPU-feature coverage + gaps) written FIRST
- [ ] Resource-bounds projection, calibrated on one real render + measured current occupancy;
      measured footprint compared at end
- [ ] One **new** minimal probe scene per effect — fixed camera, neutral floor, one effect per scene
- [ ] One **new** probe instrument script (`scripts/run_vfx_metal_probe.sh` or similar); patterned on
      `run_spellfx_v1.sh`, **not a modification of it**
- [ ] Renders via `--rendering-driver metal` (headless FORBIDDEN for renders — repo law), Movie Maker
      PNG → ffmpeg h264
- [ ] Per-effect: wall-time (scene-load / render / encode split if cheap), SHA-256 ×2 + lit-px delta,
      anomaly class per the taxonomy above
- [ ] MoltenVK `--rendering-driver vulkan` re-render of **M-FEAT suspects only, capped at ≤4**;
      side-by-side pair filed
- [ ] Eye-verification pass: name the specific frames you actually looked at, per anomaly row
- [ ] Findings note + capture set filed (see Deliverables)
- [ ] `AGENT_STATE.md` updated at session end
- [ ] Tag: `drax/v-godot-vfx-metal-probe-1`

## Acceptance criteria

- [ ] Every one of the 8–12 effects has a row: wall-time, determinism datum, anomaly class (or NONE)
- [ ] Every M-FEAT claim carries its MoltenVK cross-check pair (pre-flight having proven the method
      available), or the pre-flight's recorded reason it could not run
- [ ] **Every anomaly row names the frames eye-read.** Question 1 is "does anything *visibly*
      degrade" — a self-reported verdict with no frame citation is not evidence. gandalf eye-verifies
      the pairs at P4 before folding anything into T-A.
- [ ] The two brief questions each get a **direct, stated answer** — feature integrity, and whether a
      bake-off cadence bottlenecks on this machine. Answer question 2 with a projected
      renders-per-hour number, not an adjective. Report cold-run and warm-run separately (shader
      compile is a first-run cost, not a steady-state cost).
- [ ] Revisit-trigger status stated explicitly per limb, per the pre-registration below
- [ ] Emitter/constraint notes usable by gandalf at P4 for the T-A table (what a VFX author on this
      stack must respect)
- [ ] Resource footprint measured against the calibrated projection and against real headroom
- [ ] `Round-trip: not applicable — no cross-seam contract change in this dispatch.`

### Revisit-trigger — pre-registered, so it can't be set after seeing the data

The charter runs on pre-registered gates (§ 4). The revisit-trigger has two limbs and they are **not**
symmetric:

- **Limb 1 (feature failure) — YOURS to arm.** A confirmed M-FEAT result (MoltenVK-cross-checked)
  ARMS the trigger. State it.
- **Limb 2 (throughput bottleneck) — NOT yours to arm.** No renders-per-hour threshold for
  "bake-off-hostile" exists anywhere in the project, and inventing one after seeing your own numbers
  is a post-hoc gate. **Report the measured renders/hour and mark limb 2 NOT-ARMED-by-default.**
  gandalf rules limb 2 at P4 against the actual step-2 bake-off cadence, which is the only place the
  needed number will exist. You may *propose* a threshold — clearly labelled a proposal.

---

## Deliverables + where they land

- **Findings note:** `agentic_orchestration/drax/notes/2026-08-23-metal-vfx-smoke-probe.md`
  (meta-repo, tracked). This is what gandalf consumes at P4.
- **Captures:** `agentic_orchestration/galadriel/captures/2026-08-23-metal-vfx-probe/` — Class E,
  **UNTRACKED**, for galadriel consumption. This is a **deliberate divergence** from the godot repo's
  `harness_logs/<task>_<date>/` convention (`CLAUDE.md:101`), taken because galadriel is a named
  downstream consumer here. Note the divergence in your findings so it doesn't read as drift.
- **Probe scenes + instrument:** in `~/Games/reincarnated-godot/` (tracked — code only).

### License lineage tagging — REQUIRED on this capture set

Same-date Synty EULA finding (gandalf+legolas, commits `158875bd` / `d27e2c75`) wrote a **license
lineage gate** into the ensemble spec Stage-4: a lane survives only if **no Synty-derived pixels enter
the 3D-generation input chain**. These probe captures render Synty (`Assets/Particle_FX`,
`Assets/Synty/`) and Binbun/other-vendor content, and they are landing in the galadriel capture tree
where reference/judge corpora also live.

**The lineage table goes in the TRACKED findings note** — pack + vendor per effect. A `LINEAGE.md`
sidecar in an untracked Class-E capture dir is *itself untracked*, which means the license-lineage
evidence isn't durable or auditable in git — precisely what a Stage-4 clearance gate needs it to be.
Keep the sidecar as a convenience if you like; the tracked note is the record.

State in the note, in one line: **these captures are diagnostic evidence, excluded by construction
from any reference/judge corpus and from any 3D-gen input chain.** Co-location in the galadriel
capture tree is a real vector, but a directory-name convention is the wrong place to gate it — the
durable gate is at the consuming end (charter § 4 P3 selection, and Stage-4 clearance). Flag the
note to P3 consumers so the exclusion travels with the data.

Repo law reminder: **never commit Synty binaries** (`/Assets/Synty/`, `/Assets/Particle_FX/`).
Derivative render outputs stay git-ignored / untracked per the existing `run_spellfx_v1.sh`
convention.

---

## Out of scope (explicit non-goals)

- **Any contact with SB-1 surfaces.** Separate scene paths, separate capture dirs. Full stop.
- **Any modification of existing `run_*.sh` instruments** — they are pre-registered gates (U-7(b) law).
  New instrument only.
- **Any write to `Assets/`.** Read-only.
- Any PC / cross-host / SSH-tunnel work. The tunnel is retired; this probe only decides whether the
  *question* reopens. If your findings arm the trigger, you **report that** — you do not act on it.
- Any VFX authoring, minting, selection, or archetype opinion. That is the run's P1–P4 and the
  separate step-2 build wave. You are producing a **constraint envelope**, not content.
- Fixing the BR-2 cell-5 nondeterminism. Measure it, bound it, do not chase it.
- Fixing any SCENE-class or ASSET-class defect beyond what the probe itself needs.

## HALT conditions (stop and report; do not improvise)

- Any pressure to touch an SB-1 surface or an existing instrument to get the probe working
- Resource projection that cannot fit under real headroom even with shorter clips + PNG cleanup
- **Hard crash or non-terminating render on an effect:** ONE retry, then record it as an M-FEAT
  candidate and move on. Do **not** debug the harness into the ground — a crash *is* a datum, and
  chasing it converts a bounded diagnostic into an open-ended one.
- **Time-box:** if the session runs long, **file partial findings** rather than running open-ended.
  This is a P4-blocking input; a partial table that lands beats a complete table that doesn't. Say
  which effects went unmeasured.
- More than 4 M-FEAT suspects: cap the cross-checks at 4, HALT, and report the overflow. A suspect
  set that large is itself the headline finding and needs gandalf/Matt before you spend the session
  on it.
- Findings that arm limb 1 of the revisit-trigger: **land the note, HALT, escalate to Matt via KR.**
  The cross-host question is Matt's to reopen, not the probe's.

## Open questions for you to resolve and document

- Which mounting style each probe scene uses (scene-preloaded vs runtime-instanced) — pick
  deliberately, because it is the variable that bounds the BR-2 nondeterminism hypothesis
- Clip length and fps for the probe (shortest that still exercises the effect's full lifecycle —
  windup / active / impact); justify it against the resource projection
- Warm/cold wall-time: **one cold run and one warm run, no third.** Shader-cache warmup is a separate
  line item — a first-run compile cost is not a steady-state cost, and the bake-off-cadence answer
  depends on which one you quote.

## Commit / push discipline

- Commit code (scenes, instrument, `AGENT_STATE.md`) and the findings note as you go — authorized
  work-product of an authorized run phase (CLAUDE.md team addendum).
- **On `CLAUDE.md:101`** ("sub-agents produce render PNGs; gandalf or the human eye-verifies, then
  commits"): that designated verifier is **out of the loop by ruling** here — charter ledger **L-4**
  states gandalf does not conduct P0-b. You commit. But the *substance* of that line is preserved,
  not waived: the eye-verification requirement moves into your acceptance criteria (name the frames)
  and gandalf verifies the pairs at P4 before folding anything into T-A.
- **Push: AUTHORIZED** for this run per charter ledger **L-2** (Matt: "push as you go — authorized
  for this run"). P0-b is a charter phase of that run.
- Captures stay untracked (Class E) — do not force-add them.
- Godot rewrites `project.godot` on launch (strips the `[rendering]` LOD line):
  `git restore project.godot` before committing unless the rewrite is intended.

## References

- Brief: `agentic_orchestration/gandalf/notes/2026-08-23-metal-vfx-smoke-probe-brief.md` (governs)
- Charter: `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` (§4 P0-b, §5, L-1..L-6)
- Gandalf's dispatch request (KR carve-out #1, ledger L-4):
  `agentic_orchestration/gandalf/requests/2026-08-23-knight-rider-metal-vfx-smoke-probe-dispatch.md`
- Ruling R-1(a): Metal renderer of record, prototype era (charter § 2)
- Disciplines #1 (math-before-code), #1.1 (resource-bounds projection), #2.1 (smoke-test resource
  scaling), #19.1 (cheapest refuting test per claim) —
  `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Repo law: `~/Games/reincarnated-godot/CLAUDE.md` (off-screen render rule, asset/license rule)
- Prior art: `~/Games/reincarnated-godot/scripts/run_spellfx_v1.sh`
- `AGENT_STATE.md` load-bearing lines: **:231** (`--noking` byte-identical ×3), **:2184**
  (`--quit-after` is FRAMES; explicit `get_tree().quit()`), **:3547** (`GPUParticles3D` per-launch
  nondeterminism peelable with `--nofx`), and the 2026-08-01 BR-2 cell-5 entry (cross-process drift)
