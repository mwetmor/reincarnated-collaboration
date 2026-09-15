# Run C-5 — VFX workflow: the six skills in the cliffside register (charter)

> **STATUS:** CHARTER v1.1 (Gate-1 BLOCK-A/B + WARN-1…8 discharged 2026-09-15 — `qa/findings/2026-09-15-run-C-5-charter-gate1.md`) — gandalf (ARCHITECT → RUN-CONDUCTOR on GO), 2026-09-15. Shape: the C-3 charter (`2026-09-13-astra-burst-lane-run-C-3-charter.md`). Design authority: `2026-09-15-vfx-workflow-architecture/03-architecture.md` v2.5 (Q79 RULED in full — § 7a). Lane law: `canonical/reap-die-rise-game/painted-2d-pipeline/{00-system,mechanical-process}.md`. Ledger: `astra_test_01/burst/runs/C-5/ledger.json` (own ledger; C-3 stays closed at R-C3-21, H-C3-2 discharged). Gate-1 (jack-ryan) precedes GO. **Not autonomous:** every checkpoint stops for Matt's eye (V17: *"I will view the scene pictures and updates here and can stop things if needed"*).

## 0. TL;DR + exit predicate

**GOAL (Matt, verbatim intent):** *develop a workflow that can generate VFX similar to the 6 selected VFX but within a register similar to our 2D scene.*

**Exit predicate (decidable):** the six — Frozen Orb (D2) · Blackwater Cocktail (GD) · Poisonous Concoction (PoE) · Lightning Blast (LE) · Zeus chain (Hades) · Healing Hands (LE) — are live in the cliffside web build, each recorded against Matt's fixture verdicts (*same world · grammar reads before the glow · element identifiable · large enough · world response adds weight · painted planes*), with the per-skill measurements filed and the workflow that produced them written up as `canonical/reap-die-rise-game/painted-2d-pipeline/vfx-workflow.md` (canon on Matt's word). **Honourable fallback (V18):** if E1 and E2 both fail after their pre-registered follow-ups, the six ship in whichever *painted* route passed more cells — never a procedural register; if neither, HALT and re-plan with Matt.

**The path:** Phase 0 scene readiness (monster pack in a clearing; shared shader; event-driven effect component; replay + bake; measurement tooling) → E0 (stack proof, bake round-trip, rotation, stepped time, art-step look) + E0-p (fire peak → life, no video) → E1 (painted key-states **A** vs painted primitives **B**, one fire projectile) → E2 (fire × ice, projectile × field — one language) → E3 (the six).

## 1. Authority and interface

| Who | Role in C-5 |
|---|---|
| **Matt** | rules every checkpoint (§ 4 column "Matt sees"); the brake (V17); rules V4 after E0-p's burst is on the Desktop (R-C3-120); medium and bar changes are his alone |
| **gandalf** | RUN-CONDUCTOR: briefs, ledger, glue, DRIFT-CRITIC eyeball, Desktop packets, no production code |
| **Astra** (`gpt-6-astra`, HIGH, profile `astra-burst`) | every GENERATE / EDIT / CHECK / JUDGE / PACK / TOOLING burst — paints the monster pack, the peak stills, the primitives; builds the shader, the component, replay, measurement tooling |
| **drax** | assists on grey-box and Godot systems inside the scene as needed (V10); hand-edits inside exporter-generated trees are handed back as exporter changes |
| **jack-ryan** | Gate-1 on this charter (before GO); Gate-2 on landings; ratifies the CONSULT burst class |
| **knight-rider** | drax charter vocabulary + lane naming (`requests/2026-09-15-kr-drax-charter-reconciliation.md`) — not blocking |
| **Grok** | **shelved** (Matt, Q78(b)); video is the burst fallback only behind E0-p's kill criterion (V15) |

**Matt interface:** one numbered Desktop packet per checkpoint (`~/Desktop/Astra Burst Review - 2026-09-15/<NN> <TITLE> (open …)` — continuing the C-3 numbering from 84), a one-paragraph update in this session at each, red-flag pings only otherwise. Rulings ledgered verbatim as `matt` entries; dispositions `veto_open`. Push-as-we-go (Matt 2026-09-15).

## 2. Register and anchors carried (RULED)

- **Scene register (canon):** D2 weight + Bastion painted pole + H1 line; the cliffside is a **1:1 linearly-filtered painting** (5376×4096 canvas, 1920×1080 camera, `default_texture_filter = 2`; Keeper 240-px painted, scale 0.5417 → 130 px). **V2 = 1: effects match the scene** — painted at 1× or larger, downsampled linearly like the Keeper; no nearest-neighbour step; `pixel_scale` retired; **1 BH = 130 screen px; 3–6 BH burst envelope = 390–780 px (V19 ratified)**.
- Camera yaw 47° / pitch 52.95°; ground squash 0.58 once, unprojected ground geometry only; ground rotation before projection.
- Style card v0.2 rules carried as *hypotheses under test*: no white bodies (white only as ≤ 0.1 s strong-contact flash), halo + floor light default with the dark duplicate a per-preset option (V6 — E0(a) renders both), painted planes.
- Anchor package ("VFX chunk_A") built in-run: three constructions (directional / radial / ground-bound) as paint-overs of fixture instants over the real scene, isolated bodies, enlargements, boards — the *recomposed runtime capture* is the anchor; the first fire paint-over is provisional until E1's moving result.
- Scene references (R-C3-113/114/115): Diablo 2 scene weight; Bastion painted pole; Secret of Evermore feel; **Earthbound never as a visual reference.** Third-party atlas samples (`~/Games/vendor/vfx-atlas/`) are study-only — never in a brief.

## 3. Forks ruled (Q79, Matt 2026-09-15) — the substrate is fixed

V1 **A and B, never C** · V2 **1 (match the scene)** · V3 sequencing accepted · V4 **conditional — ruled after E0-p's burst is seen** · V5 flask + lob kept · V6 halo + floor light default, dark duplicate an option · V7 no video as shipping frames · V8 Pixel FX Designer deferred · V9 **compat-preferred, register-first; non-compat path kept** · V10 **Astra paints the monster pack into a clearing in the current scene; drax assists** · V11 world response before motif · V12 readability first · V13 3–2 = inconclusive · V14 ~12 = review trigger · V15 **no-video first for bursts** · V16 **the goal is the six** · V17 **no ceiling — Matt's eye is the brake** · V18 stop criterion (painted routes only) · V19 3–6 BH envelope ratified · V20 **no image budget — counted, reported, never gated**.

## 4. Sequence (phases; TOOLING serial; each checkpoint stops for Matt)

| Phase | What | Bursts | Matt sees |
|---|---|---|---|
| **P0-a Monster pack** | Astra dresses a clearing in **`runs/C-3/cliffside_v18`** (source tree; C-5 exports land as `runs/C-5/cliffside_v19+`, numbering continued) with **6–8 static dummies** spanning size classes (rat / hound / humanoid / brute / large) in the H1 register — dress-then-isolate (IMAGE 2 = Keeper scale figures, IMAGE 3 = projected size chart; scene-builder § 3 step 6) → object sheets → isolation on `#00ff00` → CHECK catalogue with `kind`, px size, footprint, sort line, **`target` tag + `collide`** → `props.json` → PACK → headless proof | GENERATE ×(1–3) · GENERATE-in-EDIT-mode ×(2–4) · CHECK ×1 · PACK ×1 | **Packet 84 — the clearing, dressed** (stills + walk clip); rules the dummy set |
| **P0-b Shader + component** | **T4a** shared `ShaderMaterial` · **T4b** G1 event-driven effect component + targeting rule + effect-age clock + grey/painted substitution + cold-cast fix, emitted by the exporter · **T4c** replay + bake · **T4d** measurement (VO namespace, clean-plate white differencing + baseline, VO3 palest-band, event-trace comparator) — § 5 rows | TOOLING ×4, serial, ≤ 40 min each; re-freeze after each | Packet 85 — **grey-body G1 fire bolt at a dummy, 3-second clip** (the first motion-fixture look: origin → path → hit; size in BH; contact reads?) |
| **E0** | (a) layer-stack proof on an **asymmetric painted head** (the fire peak's head — E0-p step 1 supplies it), both presets (± dark duplicate), on Compatibility **and** the browser export · (b) bake round-trip (two bakes compared; four backgrounds) · (c) rotation survival 360° · (d) stepped time look (R-C3-90(3) closed; a look, not a re-opening) · (e) art-step look, 1 vs 3, in motion (V2 ruled 1 — confirmation by eye) | GENERATE ×1 (head) · CHECK ×2 · PACK ×1 | Packet 86 — E0 sheet + clips; rules V6 on sight |
| **E0-p** | fire impact **peak still** → T4e decomposition into pieces → burst template flies/erodes/dissolves them (§ 6) → VO1/VO3/VO8 on the bake → Matt's eye → key states (expanded, spent) over transformed guides with correspondence + boil tests | GENERATE ×1 · TOOLING ×1 (T4e) · GENERATE-in-EDIT-mode ×2+ · CHECK ×1 · PACK ×1 | Packet 87 — **the burst, alive** (raw pieces vs key-stated), in the E0 stack at a dummy; **V4 ruled here** (R-C3-120) |
| **E1** | one fire projectile (G1) at a dummy — **A** painted key states vs **B** painted primitives composed at runtime; same events/seed/palette/stack; fixture values (§ 6) **approved by Matt at the P0-b clip first** | GENERATE (incl. edit mode) as needed (counted) · TOOLING ×1 (exporter amendment) · JUDGE ×1 (control) · PACK ×1 | Packet 88 — five order-randomised A/B pairs (dirt, foliage, direction changes); **ruling: A / B / inconclusive (V13) / both fail (V18)** |
| **E2** | fire / ice × G1 projectile / G2 ground field (field placed directly) — one language | GENERATE/EDIT (counted) · JUDGE ×1 (control, unlabeled identification) · PACK ×1 | Packet 89 — four clips, four-cast synchronised + staggered, glow-off; **three verdicts** (one language · distinct without glow · strike ≠ field) |
| **E3** | the six, each through the loop (§ 6), judged in the Tab-picker harness beside the others; material-glass gate at BWC/PConc; density gate at PConc; web redeploy per batch (`build_playtest.sh`) | per skill: GENERATE/EDIT (counted) · CHECK · PACK · JUDGE | Packets 90+ — one per skill + the six together on the phone; **exit predicate evaluated** |

## 5. TOOLING rows (acceptance clauses that can go RED — jack-ryan #80)

| Burst | Instruments | Acceptance (RED if violated) |
|---|---|---|
| **T4a — shared VFX `ShaderMaterial`** | `export/vfx_material.gdshader` + builder support: 4-band value-index palette lookup (index levels 0/85/170/255 → per-treatment RGBA ramp; **index 0 may be opaque**), independent coverage alpha, centre-out erosion by a distance field supplied as a texture, band-step dissolve, blend mode (MIX / ADD / PREMULT) and 2D-light participation as material params; runs on `gl_compatibility` | synthetic 4-band test texture renders the exact ramp colours (Δ ≤ 1/255) with index 0 **opaque**; erosion at 0 / 50 / 100 % removes 0 / 50±3 / 100 % of coverage; the same texture drawn ADD and as a black MIX duplicate beneath composites in one scene; **RED**: any dark index rendered transparent, or the material failing to load on Compatibility; the existing `white_core_keep` path is **removed** and a fixture that relied on it fails loudly |
| **T4b — G1 event-driven effect component + targeting** | `export/godot_import.py` emits `scenes/vfx/g1_projectile.tscn` + `scripts/vfx_g1.gd`: release / contact / expire / cancel events with **effect-age timestamps** (60 Hz), pooled `AnimatedSprite2D` head + `Line2D` trail, contact on collision with a `target`-tagged prop (nearest in facing cone, or tap), grey/painted material substitution flag, **cast-ready gate** for the first cast; the seven legacy `vfx_*_bolt.gd` retire (read-compat only); T3o picker unchanged | headless probe fires release → contact at a dummy with contact stamped **≤ 1 frame** after collision; **cold first cast registers its impact** (the v17 defect); event log written to `out/events.json`; **RED**: any contact > 1 frame late, any first-cast miss, any effect spawning without a target rule resolving |
| **T4c — deterministic replay + bake** | fixed-seed reset-and-replay to frame N; Movie Maker bake (`--write-movie out.png --fixed-fps 60`, `Rendering > Transparent Background`) under an **effect-only visibility configuration** (scene, Keeper, dummies hidden; floor light, victim tint, hit-stop, shake left live) at native crop ≤ 512²; Spritesheet assembly | two consecutive bakes of the same effect are **byte-identical**; the baked flipbook replayed over the original ground and over three other backgrounds matches the live effect within VO1 ± 5 %; **report-not-stop** (V17): if determinism is not achievable, E0(b) is dropped and the dial claim recorded as untested |
| **T4d — measurement** | `oracle/vfx_measure.py` renamed outputs **VO1…VO10** (never bare); VO3 re-pointed at style card v0.2 *palest saturated band*; **clean-plate white differencing** (classifier `V > 0.95 ∧ S < 0.20`; crop 960×540 centred on the impact; peak frame and clip mean; flash on/off; total / baseline / attributable printed separately); **baseline white of the empty crop on dirt and on foliage measured and filed**; event-trace comparator for field/aura gates (boundary vs radius; activation/expiry vs events; attachment drift; **interval CV per FF-08 — a fixed-period schedule is CV 0.000 and trips at CV < 0.25**) | the Frozen Orb v3 bake re-measures byte-identical to R-C3-112 under the VO names; the empty-crop baselines exist in `out/`; a synthetic effect with a known 4 % white peak reports 4.0 ± 0.2 % attributable; **RED**: any bare `O1`-style name left in output; baseline missing |
| **T4e — peak decomposition** | `oracle/peak_pieces.py`: isolate a painted peak (RGBA or keyed) → connected components split along painted-plane boundaries → per piece: mask, pivot, radial angle + distance from the burst centre, band index; `pieces.json` consumed by the burst template | the fire peak yields ≥ 6 and ≤ 40 pieces whose union equals the source coverage (± 0.5 %); every piece has a pivot inside its own mask; **RED**: a piece crossing a plane boundary, or union ≠ source |

## 6. Skill specs, fixture values, brief templates

- **Six `VfxSkillSpec` files** at `runs/C-5/specs/<skill>.json` (03- § 2.1 fields; provenance per field = source-game observation or Matt ruling). Written before each skill's phase; Matt approves identity-changing fields only.
- **E1 fixture values (conductor-chosen, UNPROVENANCED — Matt approves or amends at Packet 85 before either arm is painted; the Packet 85 card shows the proposed **8 BH/s** beside the shipped Frozen Orb v3 **≈ 4.9 BH/s** and the Hades band 6.5–11.6 so Matt approves a comparison, not a number):** context 0.25 s → anticipation 0.15 s → travel 0.5 s over 4 BH at 8 BH/s (Hades band 6.5–11.6; shipped Frozen Orb v3 ≈ 4.9) → contact ≤ 1 frame → half-peak ~4 frames → residue 0.6 s; impact envelope 3 BH.
- **Burst template (E0-p):** onset flash (runtime) → intact peak hold 1–2 frames → pieces fly outward on per-piece velocity/rotation curves (scale within ±15 %, linear filtering) → centre-out erosion + band-step dissolve → residue **by erosion** to 15–25 % coverage for 0.3–1.0 s. Key states: expanded + spent, painted over the tooling-transformed piece arrangement; correspondence (piece ↔ source within 1 px after transform) + boil (VO8 in band; shard count constant; contour thickening ≤ 1 px).
- **Briefs** follow `02c-` § 6 templates: asset role first · what is already approved · three images with stated roles (guide / approved exemplar / scene-and-scale board with Keeper at 130 px) · one requested change · canvas + occupied bounds + pivot + plane · exporter responsibilities · acceptance + one diagnosed retry. Painted extent declared in **screen px** (art step 1). No prohibition lists; the haze fix is representational (*"paint the opaque banded body representing the emission; light spill is a runtime layer"*). Dummies: `CS-dress-clearing`, `CS-objsheets-dummies`, `CS-objiso-dummies`, `CS-assets-dummies` (props method). Peak: `VF-peak-fire-impact`. Head: `VF-prim-fire-head`.

## 7. Gates — report, never verdict

Every gate names its instrument (03- § 4 table). BUILT after P0-b: VO1–VO6/VO8/VO10 on alpha bakes; white differencing + baselines; event traces. **PROVISIONAL:** `field_v1` / `aura_loop_v1` envelopes (Matt-approved fixture numbers, labelled) until the frame-extraction sourcing class is ruled. **JUDGE bursts** carry a known-bad control in every batch; a JUDGE passing its control twice is a HALT. Matt's eye rules over every number (I-2). Rejection criterion: a candidate meeting bounds only by destructive clipping or unapproved distortion is rejected. Coherence tripwire from E2 on: frozen cross-family reference set + mixed-vintage playback on every addition; **FF-08: any tick / hop / pulse schedule with interval CV < 0.25 trips (metronome)**. **VO7 (projectile speed) and VO9 (layer budget) are OUT OF SCOPE for C-5** — speed is an eye-check at Packet 85 against the shipped figure; no instrument claims otherwise.

## 8. HALTs (to Matt; the run does not decide) — `mechanical-process.md § 1.6`, restated

- two consecutive experiment FAILs (an experiment = E0(a–e) / E0-p / E1 / E2 / an E3 skill)
- two VOIDs in a row
- a JUDGE passing its control twice
- three rate-limit backoffs
- any write outside `out/`
- ~~run image cap (250)~~ **UN-ENFORCED for C-5 by a SENTINEL** (`images_cap: 999999` in the ledger — Matt V20 *"no image budget"*; `run_burst.py:158` integer-compares the field, so the waiver is a sentinel, not a null; `ledger.empty()` still hard-codes 250 and must never be used to rebuild C-5's ledger) — images counted and reported at every packet, never gated
- **any medium or bar change** — medium = painted-2D (C struck by V1); bars = the pre-registered gates in § 5/§ 7 and 03- § 6; the conductor may not re-scope a halt rule in-run (H-C3-2 lesson, R-C3-22)
- **plus (this run):** deterministic replay not achievable (report, then Matt decides whether E0(b) is dropped); a register bar reachable only outside Compatibility (report; Matt decides per V9); E1 3–2 (V13: one pre-registered follow-up, named in the ledger, or stop)

**Honourable fallbacks:** T4c indeterminism → E0(b) dropped, dial untested, recorded · a peak that fails RGBA and the one key-plate fallback → E0-p reports the failure and Matt chooses re-paint or video fallback (V15) · E1/E2 both fail → V18.

## 9. Ledger and records

**EDIT is not a burst type** — every "edit" above is a **GENERATE burst whose task uses image_gen EDIT mode** (as C-3's `CS-dress-*` were); LABEL stays the ≤ 2-image edit class. `runs/C-5/ledger.json` (keys as C-3: bursts · images_used · images_cap = 999999 sentinel (V20) · experiments · milestones · halts · rulings · grok_calls (expected 0) · run · charter · charter_sha256_12 · notes). Rulings `R-C5-n`, class `matt` / `conductor` / `reasoning`, `veto_open`. Milestones `M-C5-*`. Every packet number recorded. Briefs `astra_test_01/burst/briefs/C-5/`. Conductor glue `runs/C-5/conductor_scripts/` (seeded from C-3's: `wave.sh`, `cl.py`, `freeze.sh`, `restamp.py`, `mk_*`). Freeze after every TOOLING burst; `MANIFEST.sha256` + `00-system.md § 7 SYNC` restamped. Specs `runs/C-5/specs/`. **Decisions-log entry** for the C-5 commitment set (V1 route · V2 register · V9 platform · V16 scope) proposed to jack-ryan **at E1's ruling**, not at E3. Commits `--only` over named paths; push as we go.

## 10. ARCHITECT PASS — open-questions gate (every decision the run will hit)

| Decision | Status |
|---|---|
| Q79 V1–V20 | **RESOLVED** (Matt, 2026-09-15) |
| V4 hybrid oracle | **GATED** — Matt rules at Packet 87 (E0-p burst seen; R-C3-120) |
| `field_v1` / `aura_loop_v1` bands | **GATED** — frame-extraction sourcing class (`2026-08-25-…`, Matt); provisional envelopes meanwhile |
| Q78(a) H-C3-2 | **RESOLVED** — supersession (Matt) |
| Q78(b–g) | **PARKED** — not hit by C-5 |
| Q68 G-4 (body-alpha vs occlusion) | **OPEN, Matt's — distinct from V12.** V12 = build priority when register, density and perf conflict (readability first). G-4 = the FF-15 lit-smear trade: how much of the *caster's* body alpha is spent when the caster overlaps the effect (R-25: Matt's alone). C-5 does not hit G-4 before E3 (Zeus self-cast); flagged there |
| drax charter vocabulary | **OPEN, KR** — not blocking under V10 (Astra lane, drax assists) |
| CONSULT burst class row | **OPEN, jack-ryan** — not blocking (no consults planned in-run) |
| E1 fixture values | **GATED in-run** — Matt at Packet 85 |
| Renderer parity claims (probe 2 "VERIFIED" = read) | **E0 gates**, not facts |
| Disk (20 GiB free) | bakes at native crop ≤ 512²; capture directories untracked; report at each packet |
| Memory (8 GB) | TOOLING serial; no video decoding; one Godot instance at a time |

**Gate: CLEAN-or-GATED.** No OPEN item is on the run's path before its named checkpoint.

## 11. Restart prompt (paste into a FRESH `claude --agent gandalf` session; launches on Matt's GO after jack-ryan Gate-1)

> Read `agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` and `2026-09-15-vfx-workflow-architecture/03-architecture.md` § 7a, then `runs/C-5/ledger.json` if it exists. You are RUN-CONDUCTOR of Run C-5. Seed conductor glue from `runs/C-3/conductor_scripts/` into the scratchpad with `--run C-5`. Begin at Phase P0-a (the monster pack). Stop at every "Matt sees" checkpoint; file a Desktop packet and a one-paragraph update. Never re-scope a HALT rule.

— gandalf (ARCHITECT), 2026-09-15
