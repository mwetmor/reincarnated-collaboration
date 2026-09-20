# KC2-PLAY RUN — charter + ruling ledger (desirable-run pattern)

> **STATUS:** v0.1 DRAFT — **NOT LAUNCHED.** Awaits (1) jack-ryan Gate-1, (2) Matt's launch sheet answers (§ 6), (3) Matt's launch word. Conductor: gandalf `RUN-CONDUCTOR` (charter's author conducts — intent residency). Successor to the **KC2 LIFT RUN** (CLOSED L-19, 2026-08-26).
> **Pattern authority:** `agentic_orchestration/operating-procedures/desirable-run-pattern.md`. **Fit test: § 3 below.**
> **Elicitation of record:** `2026-09-20-kc2-play-architect-pass.md` (ARCHITECT pass + § 6 corrigenda — the corrigenda govern) · Q81 F1–F7 RULED 2026-09-20 (Matt verbatim: *"Agreed - accept all"*) · Q66 closed via F1.
> **P0 returns (frozen inputs):** P0-a gamora census `gamora/notes/2026-09-20-kc2-play-p0a-traceability-census.md` · P0-b 2D re-target spec `gandalf/notes/2026-09-20-kc2-play-2d-retarget-spec.md` (`6cc64e5d`) · P0-c drax census `drax/notes/2026-09-20-kc2-play-p0c-scene-capability-census.md` (`05b0f4ab`) · P0-d architect pass § 5.

---

## § 0 — Intent (whose words, what outcome)

**Matt, verbatim (2026-09-20):** *"make that a fully playable sim that we can build out in an Astra 2D scene with our 2D animated character with monsters having animation placeholders and the player character and monsters having placeholder VFX. I want to play the game and compare how accurately we can get it to my video of playing the game in Grim Dawn on the EOR warlord."*

**Terminal artifact:** a **desktop build Matt can launch** — Crucible waves 150–160, the Keeper as the EoR warlord, GD-faithful mouse binds, geometry-true placeholders — sitting on a **headless GDScript runtime whose fidelity to the Python oracle is already graded (T-A)** and which writes the telemetry from which his play is compared to his footage (T-B). **The autonomous run ENDS at the handoff.** T-B play sessions, the feel round and T-C side-by-side need Matt's hands and eye; they are HITL sessions after the run, never inside it.

## § 1 — Bounded substrate (count it, list it, diff it) — FROZEN AT LAUNCH

| # | Substrate | Count | Pin |
|---|---|---|---|
| S-1 | baton-v3.1 model + reference pack pair | 12 + members | model `2c7fc61f…f4a7` / reference `f50e5e25…4ed6` (derived at use, never retyped) |
| S-2 | **The P0-a census** — every behaviour the runtime must perform | **72 rows: 17 IN-PACK · 41 PYTHON-ONLY · 14 ABSENT** | the committed note |
| S-3 | **v3.2 lift scope** (census § 2) | **Tier 1 V0–V9 (10 items, ≈ 90 law rows + ≈ 2,000 per-record) · Tier 2 V10–V19 (12 items, ≈ 75 rows) · the cited-excerpt list** | the committed note |
| S-4 | Runtime acceptance | SKIRT **R-1…R-9** + 2D delta **R2D-1…n** (as enumerated in the P0-b spec § 7) | the two August specs + `6cc64e5d` |
| S-5 | Scene gap list (P0-c § 2) | HUD · enemy tokens · arena plate · held-channel body · telemetry recorder · projection/y-sort · GD input · Camera2D zoom gate · restart · exporter `--vendor` · macOS preset | `05b0f4ab` |
| S-6 | Sealed oracle cells (K-7: hash-verify only, NEVER re-run) | M-POL-2 `ad61ad2a…` · mech `20b05cb4…` · W1 walls `7a992c81…` | census § 3b |
| S-7 | Arena geometry | 177-vertex ring · 4 islands · 2 unwalked arcs · 6 zones | `crucible-arena-geometry-v1.json` `68d895d7…481f` |

Discoveries beyond these are FINDINGS for the next lap, never silent scope growth. **Named out-of-scope, pre-declared:** sim siblings **S1–S6** (census § 3e — dodgeability A/B, pool-DoT-live cell, summons-positioned, interrupts-armed, draw-site census, cold-start band) · the 43-state AI graph (the oracle never ran it) · `ABS-CRIT-ROLL-RULE` (oracle's choice = no player crit, buildable today) · loot / levelling / meta (Q81-F6) · Web/phone delivery (Q81-F3) · any painted asset minting.

## § 2 — The central design: ONE runtime, TWO configurations, a DIVERGENCE REGISTER

The P0 returns show the oracle and the thing Matt wants to play are *deliberately not the same fight* (walls ring vs circle, pools 0.0 vs D-LIFT, 0.15 roll vs the flag). The run holds them apart by construction:

- **`ORACLE` config** — the fold/limb set of record (v3.2 **V0**), exactly as the sealed cell ran: wall = `CIRCLE R = 43.758… m`, pool magnitude 0.0, uniform 0.15 cast-interrupt roll, fire-time damage resolution, summons leader-coincident/positionless/immortal, no player crit, scripted pilot (PM1 + M-POL-2 channel policy). **T-A is graded under this config and no other.**
- **`PLAY` config** — what Matt plays: video-measured ring at a registered `u`, pools per **D-LIFT-1/2**, the **`interrupts_channel` flag** (D-CP2-2), human input.
- **The DIVERGENCE REGISTER** — every switch by which `PLAY` differs from `ORACLE` is one enumerated row (id, ORACLE value, PLAY value, authority, how it is tested since T-A cannot grade it). The config id + register hash are stamped into every telemetry file. **A T-B miss is then attributable to exactly one of: port (excluded by T-A) · declared divergence · model gap · pilot.** A difference that is in none of those classes is a defect in the register.

**Conductor rulings made at charter (veto-open — Matt's one word reverses any):**
- **R-KP-0a · Damage resolves at FIRE TIME in both configs for this lap.** Strafing does not dodge (census § 1.3: there is no arrival hit-test in the oracle, and an arrival rule is undecoded — Law 3). It is divergence-register row 0 *as a non-divergence carried with its confound named*; the arrival hit-test is next-lap, behind sibling S1. *Player consequence:* projectiles you side-step will still land. The referent sat at full health 42.84 % of the fight; he was not dodging for a living.
- **R-KP-0b · Summons in PLAY keep the oracle's law** (coincident, immortal, basics-only); the view draws them beside the player as a registered presentation choice.
- **R-KP-0c · The arena is a swappable data object**; the wall-less hull is retired as a scale-pin target; `u` for PLAY is a registered runtime choice inside `[0.22277, 0.3663]`, rider routed to galadriel. A tighter walled arena than the sealed spread is a **declared expectation**.
- **R-KP-0d · Census hazard (c-2)** (pack says monster-side mitigation unmodelled; oracle applies it per body) is NOT adjudicated by the conductor — gamora runs her named one-record refuting test as the first act of W1, and V6 is written to its answer.

## § 3 — Fit test (desirable-run-pattern § 3)

- **F1 Enumerable? YES** — § 1: 72 census rows, 22 lift items, R-1…R-9 + R2D-n, 11 scene gaps, 3 sealed cells, 1 geometry file.
- **F2 Decidable? YES** — § 4 evaluates without Matt; every judgment-shaped doneness (feel, "looks like GD") is converted to the post-run HITL boundary, not left inside the run.
- **F3 Pre-drainable? YES — drained:** Q81 F1–F7, Q66, D-CP2-1..3, D-LIFT-1/2, R-KP-0a..d. Residual forks are reasoning-boundaries (lift-row shape, module layout, token look). **One residual Matt item does not block launch:** P0-b OQ-1 (held-RMB auto-resume) — see § 6.
- **F4 Authority-resident? YES** — the conductor authored SKIRT, F-5 and the 2D delta and holds the KC2 lineage. ⚠ `SPEC-AUTHOR → DRIFT-CRITIC` applies at every fold judged against those specs; jack-ryan Gate-2 is the independent check.

## § 4 — Decidable target-state (the run is DONE when every row evaluates, without Matt)

1. **baton-v3.2 CUT** — Tier 1 V0–V9 each **LIFTED** (rows-not-fields, `(value, scope, provenance)` triples, DR-1/2/3) **or HONEST-FAIL** as a named absence with pin + what-was-searched; Tier 2 likewise; census PRE == POST; digests derived; v3.1 superseded FORWARD (additive — every v3.1 member path survives). jack-ryan Gate-2: no BLOCK outstanding.
2. **Runtime T-0** — `reincarnated-godot/kc2_runtime/` loads v3.2 under the SKIRT § 1 gate sequence headless; **all test vectors reproduced** to declared precision; rule census + runtime-choice ledger emitted; both channel DO-NOTs mechanically enforced; **zero `Input`, zero `res://` art, zero scene-tree dependency** asserted by scan.
3. **T-A graded** under `ORACLE` config, 5 salts per arm, against **pre-registered bands** (prereg committed ALONE before the first graded run — D4): terminal-wave 5-vector · per-wave durations · the five-state census on the **constructed denominator** · release duty / plant ratio · the deferred-arrival **conservation identity → 0** · the **inertness relations** (NULL arm ≡ base) as structural rows. **PASS, or FAIL-WITH-NUMBERS filed as findings** — a T-A FAIL is a processable finding (honorable fallback), it does not hold the handoff; it caps what may be *quoted* from T-B.
4. **Scene** — own Godot project (not `cliffside_v*`); runtime vendored by sha (refuse-on-mismatch); headless probes green: **geometry-true** (every MODEL-BOUND dimension of every VFX/telegraph asserted against pack values) · **no `CollisionObject2D` under any token** · **no combat duration handed to a 60-Hz grammar** · the three arena traps by assertion · Camera2D zoom gate · recorder writes one tick-stamped stream, config id + register hash in the header.
5. **Desktop build** launches on the Mac (macOS preset, unsigned local `.app`); a scripted 60-s smoke session produces a valid telemetry file. **Fallback:** the Godot editor on Matt's Mac for feel-only sessions — never a Web build.
6. **Handoff packet** — build + one-page how-to-play (binds) + the divergence register + the T-A report + the T-B grader ready to run on his first session + findings harvest. Gate-2 on the whole.

## § 5 — Seats + wave plan (seams execute; conductor writes no production code)

| Wave | Seat | Piece | Gate |
|---|---|---|---|
| **1** | gamora | (c-2) refuting test → **v3.2 rows** Tier 1 then Tier 2 (math-note/prereg ALONE first — D4) | § 4.1 |
| 1 | drax | runtime **skeleton** (loader + digest gates, tick + F1 rider, own RNG at declared sites, view-contract types, config + divergence-register plumbing) · macOS preset + `build_desktop.sh` | compiles `--check-only`; smoke transcript |
| 1 | galadriel | HP saw-tooth re-query (P0-b B-19; committed data, no video) · the `u` rider (R-KP-0c) | findings note; T-B expected-values table |
| 1 | gandalf sub-agent (SPEC-AUTHOR) | **T-A prereg** (bands from census § 3c, decision rules, the denominator law) · the divergence-register v0 | prereg on record before any graded run |
| **2** | star-lord | **baton-v3.2 cut** + receipt + MIGRATION | § 4.1; then jack-ryan Gate-2 |
| 2 | Astra lane (codex bursts; drax as fallback seat) | scene on a **canned event stream**: exporter `--vendor`, plate, projection, tokens, HUD, input, recorder — in its own tree, **no writes under `burst/`** (see § 7.3) | § 4.4 probes |
| **3** | drax | runtime **full build** against v3.2 → T-0 → `ORACLE` scripted pilot | § 4.2 |
| 3 | gamora | grades T-A against the prereg (her oracle, her denominators) | § 4.3 |
| **4** | drax + Astra lane | integration · desktop build · smoke session | § 4.5 |
| 4 | jack-ryan | Gate-2 on the handoff | § 4.6 |

Sub-agents commit (`git status --porcelain -- <paths>` pre · `git commit --only <paths>` · `git show --stat HEAD` post · never `add -A`), **never push — the conductor releases per fold** under whatever posture Matt sets at § 6.

## § 6 — Matt interface (LAUNCH SHEET — one word each)

| # | Item | Recommendation |
|---|---|---|
| **L1** | Push posture — the runtime lives in `reincarnated-godot`, which the standing push pattern does not cover | **Push-as-you-go on `collaboration` + `engine` + `godot` for this run; `loadout`/`demo` untouched** |
| **L2** | Checkpoints | **Owner-eye checkpoint at each wave seal** (W2 seal = first thing you can *see*: the scene on canned data; W4 = the build). Red-flag pings only between |
| **L3** | Astra/codex labour ceiling (it has halted two runs) | **If a scene burst VOIDs on usage twice, the scene seat falls to drax hand-authoring — no wait, no credit purchase without your word** |
| **L4** | R-KP-0a — fire-time resolution this lap, dodging next lap | **accept** |
| ~~**L5**~~ | ✓ **ANSWERED 2026-09-20 by Matt's testimony — see ledger KP-1.** P0-b OQ-1 (held-RMB across a cast interrupt) | **Type-B: AUTO-RESUME while RMB is held. Type-A: the hand's release; resumes on the player's input only.** |

**HALT-to-Matt boundaries:** any product-seam commitment · charter amendment · jack-ryan BLOCK · any result that would move a sealed grade of record (K-7) · taste/naming · external-state danger (disk, usage, credentials) · two consecutive failed attempts at the same gate by the same seat.

## § 7 — Standing laws carried in (cite-by-name)

1. **KC2 lineage:** K-7 · Law 3 (no fitted constants, no invented rules) · GL-6/7/10/12/13 · DR-1/2/3 · D4 prereg-alone · bands-not-tape (R-L91-4) · ship-ratios (D-MPOL2-2) · G5 = 0.0960 · digests derived-never-retyped · D-LIFT layer law · close-out-derived-from-ledger · corrigenda-forward · OP § 4.11 value-set sweep at every value-changing fold.
2. **From P0-c (architect pass § 6.5):** generated projects are artifacts, never edited · exclusion of the grammars' hit resolver **by assertion** · the sim starts and cancels every combat-timed effect · runtime home `kc2_runtime/`, headless `--script` runners.
3. **Concurrency with Runs C-6 / C-7** (they own the burst lane's TOOLING + freeze): KC2-PLAY **writes nothing under `astra_test_01/burst/`**; its scene tree is `astra_test_01/kc2play/`, consuming the burst exporter read-only at a **pinned MANIFEST sha**; all heavy work (headless Godot, suites) under `~/astra-burst/.heavy.lock` via `heavy_lock.py`; a needed change *inside* `burst/` is a **request to the C-7 conductor**, never a write. *First W2 act is a feasibility probe of this arrangement; if the wrapper cannot run a burst outside `burst/`, the scene seat falls to drax (L3's fallback) and that is a finding, not a halt.*
4. **Figure hygiene:** no T-B figure is quoted as fidelity until T-A is graded (Q81-F7); HP expected shape is *mostly-full, shallow fast saw-tooth, rare deep excursions* — never "living on leech."

## § 8 — Ruling ledger (append-only; veto-open unless class `matt`)

| # | Date | Class | Ruling |
|---|---|---|---|
| KP-0 | 2026-09-20 | matt | Q81 F1–F7 as recommended (*"Agreed - accept all"*); Q66 (A) + player-kinematics rider |
| KP-0a..d | 2026-09-20 | conductor | § 2 rulings (fire-time resolution · summons oracle-law · arena swappable / hull retired · (c-2) to gamora) |
| KP-0e | 2026-09-20 | conductor | P0-b OQ-2..6 dispositions (architect pass § 6.7) |
| **KP-1** | 2026-09-20 | matt (testimony) → conductor ruling, veto-open | **Matt verbatim:** *"I don't recall anything interrupting the spin. I believe it was continuous, except for when I stopped it, thinking I might save some mana/energy."* **Reading, per the L-84 discipline (testimony is a hypothesis source; a measurement refutes an execution, never the testimony):** the footage MEASURES eight ≈0.60 s Type-B breaks (5 Blitz, 3 Vire's Might; range 0.53–0.67 s) — and the pilot did not perceive one of them. **A break the hand never noticed is a break the hand never repaired: he did not re-press.** → **OQ-1 RULED: Type-B releases AUTO-RESUME while RMB remains held** (the 0.60 s is a mechanical lockout the game serves and ends by itself). His second clause names the OTHER population: deliberate releases — **Type-A is the hand letting go; it resumes only on input.** ⚑ Two things this testimony does NOT do, recorded so nobody does them later: (i) it does not delete the Type-B population — the breaks are measured and the `interrupts_channel` flag (D-CP2-2) stands; (ii) it does not revive `energy_gated_release` — his *reason* was energy, the *measured trigger* was the wave transition (every release began ≥ 0.846 of ceiling; H-MC-1 stays REFUTED on its trigger). *He was not counting his energy; he was counting the fight* — and believing he was counting his energy. The runtime implements the measurement; the HUD will let him see which it was. |

---

*Filed by gandalf (`ARCHITECT` → `RUN-CONDUCTOR` prep), 2026-09-20. No production code. Not launched.*
