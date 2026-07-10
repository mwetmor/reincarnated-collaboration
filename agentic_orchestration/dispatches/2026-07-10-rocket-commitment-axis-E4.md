# Dispatch — rocket: Commitment-axis (E4) — bc_commitment → cast-time as PRICED risk/reward (PAIR, emitter + math-note lead)

**From:** knight-rider → **To:** rocket (generation seam)
**Date:** 2026-07-10
**Pattern:** B (multi-hour cross-seam build; math-before-code) — **Gate-1 (critique pair: jack-ryan + gandalf) REQUIRED before fire**
**Authority (ONE build authority — note + addendum together):**
1. `agentic_orchestration/gandalf/notes/2026-07-10-e4-commitment-axis-design-note.md` — all six 2026-07-09 forks RULED (Matt, two rounds).
2. `agentic_orchestration/gandalf/notes/2026-07-10-e4-runtime-interaction-and-pressure-addendum.md` — addendum forks **F-0 / F-1(b) / F-2(b) / F-4 / F-5(a) RATIFIED** (Matt 2026-07-10); **F-3 ADOPT+DEFER**. Where the addendum extends the note, **the addendum governs**.

Surface-ledger **E4** (`canonical/current-to-end-state/surface-ledger.md`; OPEN queued → IN-FLIGHT on fire); roster row **H6** (Charge-up Caster — this is the row E4 redeems). Fourth axis of the full-spec main line (E1→E2→**E4**→E3).

**Status:** FIRE-READY — Gate-1 critique pair PASS. gandalf **CONCUR-WITH-AMENDMENTS** (fidelity check, all folded: §8 `tick_tracking` field slot); jack-ryan **PASS-WITH-AMENDMENTS** (all folded: §0 line-verify note, §3.6 Disc #17 citation). Cleared to execute.

**This is the EMITTER half of a rocket + gamora PAIR.** Companion dispatch: `2026-07-10-gamora-commitment-axis-E4.md` (sim consumer). The two build against ONE shared math note and ONE versioned packet contract (ADR-004 MIGRATION.md at the seam). **You lead the math note; gamora co-signs as consumer — ONE math-note conversation, not two.**

---

## 0. Why this axis exists (design note §0, §5)

Today `timing.params.cast_time_seconds` is emitted tier-varying (`_CAST_TIME = {1:0.3, 2:0.5, 3:0.7, 4:1.0}`, `per_skill_emitter.py:194, :776, :852-853, :956` — line numbers re-verified 2026-07-10; supersede the design note §0 cites) and **never read by the sim** — cadence derives from `cooldown_seconds` alone (`spatial_engine.py` §readiness gate; damage applies instantly at cast). There is no weight of commitment anywhere in the hands. E4 makes cast-time a **THROUGHPUT-ACTIVE, PRICED risk/reward axis**: the same BC cell produces a **snap** hand (reactive, mobile, metronome) and a **wind-up** hand (commit, watch the world move, land the big one) as a **real priced gamble** — the premium exists only if you complete casts, and mobile enemies genuinely make you whiff. This is the D2-Smiter / PoE-slammer archetype arriving as mechanics, not costume. **"Cheapest of the four" died at §0b — this is a mid-size cross-seam build.**

## 1. Target seams + the change

- **`generation/endgame_encounter_catalog.py`** (yours) — new sixth catalog coordinate.
- **`generation/per_skill_emitter.py`** (yours) — commitment fields + premium term + coupling enforcement + capstone declaration.
- **`generation/season_generation_pipeline.py`** (yours) — sampler integration + coupling binding at the SAMPLER + summon-act fifth scope row.
- **`generation/math/commitment-axis-e4-2026-07.md`** (NEW, yours — the shared math note; gamora co-signs).
- **The seam boundary** — the ONE versioned packet contract consumed by gamora (sim) + drax (Godot/loadout). **MIGRATION.md REQUIRED** (ADR-004; §9).

## 2. THE SPINE IS SACRED (design note §0) — hard constraint

**Zero diffs to** `TIER_COEFFICIENTS`, `_DAMAGE_MULTIPLIER`, `BASE_SPELL_DAMAGE_L50`, base `_ENERGY_COST` / `_COOLDOWN`. The premium is a scalar LAYER at emission, never an edit to a spine table. **`_CAST_TIME` is a LAYER table, not spine** — it is inert today; whether the bin layer **composes with it or supersedes it is YOUR math note's call** (flag the choice explicitly as a layer-table decision, acceptance §11 — do not fake continuity).

## 3. MATH-BEFORE-CODE (Discipline #1) — REQUIRED, precedes ALL pair code

**No pair code fires — yours OR gamora's — before this note closes.** Author `generation/math/commitment-axis-e4-2026-07.md` FIRST. It is the pricing loop's derivation and MUST derive, each with arithmetic shown:

1. **The shared period model, `k`-AWARE (design note §1.3, the Q-E4-5 form — HARD instruction).** E2's amplitude scalar `k` and E4's cast-time act through **ONE period model**. Derive jointly with `k`, **never layer blindly** — "E4 math built blind to `k` is how the E2 conservation law leaks one axis late." Under ACTIVE: period grows with commitment; the premium term (per-hit above neutral compensation) is the priced payoff.
2. **The risk-PRICED premium formula (design note §1.3 guard 1).** Expected throughput ≈ `completion_rate × premium × spine_throughput` stays **band-center-in-tolerance**; the payoff is **VARIANCE, not a strictly-better number**. Premium is derived from **MEASURED completion/whiff rates** (gamora's telemetry over the certified regime mix — §C.5 addendum). Mispricing in either direction is the named failure class (D3-Inferno unpriced wind-ups = dead skills; PoE priced slams = a real archetype).
3. **F-1(b) forced-break threshold Y%/W (addendum §C.2, §B.5; RATIFIED).** Cumulative incoming damage ≥ **Y% max-HP within window W** forces a channel break. Derive Y and W — **Discipline #17 empirically calibrated** (not guessed). Plus the recovery-lockout guidance (0.3–0.5 s) + no-refund-of-broken-tick.
4. **F-2(b) ramp + break-reset curve (addendum §B.6, §C.2; RATIFIED).** Channel reward ramps; a forced break RESETS the ramp — that is what gives the break rule TEETH (without ramp, a break costs a fraction of a tick and prices at ~0). Derive the ramp curve + reset behavior; total channel throughput stays in-band, ticks are the delivery texture.
5. **Drain economics against the resource-economy axis bins (addendum §B.3, §D.3; economy-coupling guard).** Channel pays per tick (`drain_rate`/s); wind-up + snap pay on commit (whiff forfeits the cost — the economic leg of the risk). Derive drain per **(economy bin, `k`)**. **`overflow` × channel = LEGAL-GUARDED**: drain must be sized to BIND (an overflow-economy kit whose drain never approaches regen has a free, unpriceable lock). **`starved` × channel = double-starve: legal, FLAGGED, expect low sustain uptime as the identity.**
6. **`tick_interval_seconds` band [0.25, 0.5] s (addendum §B.2)** — per-tick damage share from the k-aware period model. The chosen value is **Disc #17 empirically calibrated** (not guessed) — like every calibrated number in this note.
7. **`_CAST_TIME` fate** — composed-vs-superseded, documented as a layer-table decision (acceptance §11).
8. **The genre-band constraints as CONSTRAINTS not values (design note §2):** felt-difference floor (a wind-up reads distinctly heavier than a snap; sub-~0.3 s is invisible — D2 FCR perceptible ~200 ms), fight-completion ceiling (≥2 completed casts of the slowest modulated skill in a representative gauntlet fight — a wind-up that rarely completes is a dead slot), action-cadence floor (snap must not collapse below the sim's effective action cadence).

**Cross-seam note-authoring:** gamora co-signs the consumer half (whiff-resolution semantics, channel-lock, cast-state-machine params it will consume, telemetry field list). ONE conversation. The **pricing loop is the coupling point**: gamora measures completion/whiff → you price the premium from those rates.

## 4. The coordinate (design note §1.1, §1.5; addendum §D.1)

- **`bc_commitment` joins the CellDef as the sixth coordinate** — bins **snap / wind-up / channel** (D7-clean, genre-precedented, no coinages). CellDef today is 5-tuple (`endgame_encounter_catalog.py:130-134`: `bc_range / bc_tempo / bc_amplitude / bc_attribute / bc_proxy_density`).
- **Space of record: catalog 324 → 972 lattice** (`endgame_encounter_catalog.py`; live = the 25–31 roster CellDefs, each taking one commitment value, pinned or rolled). **Bookkeeping correction of record (addendum §D.1):** all prior "68,040 × 3 = 204,120" cites are RETRACTED — that grafted the coordinate onto the 8-axis QD archive, the wrong space. QD ninth-axis admission is **deferred (F-3 ADOPT+DEFER)**; the pair builds against the **catalog 324 → 972** space under either resolution and is **NOT gated on F-3**.
- **CellDef identity pins where the kit's name demands it:** **K1 Heavy Barbarian = wind-up · K7 Archer = snap · K19 Channeling Cleric = channel.** All other named cells: **you propose pin-vs-rolled per cell in the math note; Matt curates at roster grain** (curation ≠ authorship — do not self-approve the roster).
- **Channel-consistency LAW (design note §1.1):** "channel" is ONE mechanic everywhere — this bin, the rotational family's `while_channeling` persistence mode (F-substrate), and the spin-channel re-cert (bench B12). One name, one mechanic. **A divergent second "channel" implementation is a cert-blocking defect.**

## 5. Modulation scope (design note §1.4) — apply EXACTLY

| Slot | Treatment |
|---|---|
| primary / secondary attack (T1–T3) | **FULL** — attack slots carry the kit's bin identity |
| control (T1–T3) | **cast-only** — a REAL cast time on the cast; lock magnitude UNTOUCHED; does NOT define the kit's coordinate (anti-free-Teleport guard) |
| support / utility | **EXEMPT — instant** (byte-identical pre/post) |
| T4 capstone | **per-capstone declaration** (§6) |
| **summon-act (13th appended skill)** | **carries commitment (F-4 RATIFIED)** — conjure defaults **wind-up**; snap-summon legal; channel-summon ONLY as `while_channeling` tether (§7 coupling) |
| **control-pure kits (Axis-2B)** | commitment expressed via the **attack-complement (F-5(a) RATIFIED)** — not on the control skills |

## 6. T4 capstone coordinate-transform law (design note §1.5) — the blanket `channeled` label DIES

Every T4 today emits `name="channeled", cast_time_seconds=1.0` (`per_skill_emitter.py:852-853, :956`). That blanket label is retired. Every T4 capstone **declares**:

```
(commitment_bin ∈ {snap, wind-up, channel},  amplitude_delta ∈ {none, flatten, invert})
```

- mode-shift/toggle → **snap** · conjure-summon → **wind-up** (the 1.0 s becomes an honest "deliberate act of conjuring") · sustained-output → **channel** with real channel-lock.
- **`invert`** = whole-kit rhythm inversion (all main skills fire through the channel stance) → the kit's **EXPRESSED post-T4 coordinate flips spiky→flat**. A single sustained skill woven among burst skills declares `flatten` or `none` (legal, NOT an inversion capstone).
- **Emit the declaration on every T4 as `(commitment_bin, amplitude_delta)`.** Certification fires at the **EXPRESSED** coordinate (gamora's job) — declaration-vs-measured mismatch = cert FAIL. The generation cell (sampler address, K-number) stays stable; the cert record carries **native + post-T4 expressed** (precedent: K13→K12 artillery fold). **E6 (proxy T4 suite) consumes this grammar** — build it clean.

## 7. Coupling-table enforcement at the SAMPLER (addendum §D.3) — bind the sampler + pricing, NOT the archive

Empty cells are MAP-Elites' native answer; the archive needs no pruning. The **SAMPLER and the PRICING law** (the things that actively fill cells) enforce:

| Coupling | Enforcement |
|---|---|
| amplitude **flat × wind-up** | **HARD CUT** — the premium expresses as per-hit size (spiky by construction); flat wind-up cannot exist in tolerance |
| amplitude **spiky × channel** | **HARD CUT at v1** — a pure tick train is flat by construction (staged-release F-2c is the later unlock, NOT v1) |
| **charge-stack ≠ wind-up BOUNDARY LAW** | charge-stack (accumulate-N-then-spend, resource-axis bin) and wind-up (cast-time commitment) must NEVER be conflated by generators or cert; the archive reserves charge-up-skill as a cross-axis mechanic |
| **proxy ≥ light × channel** | CONDITIONAL — legal ONLY as `while_channeling` tether (the lock is the proxies' lifeline); fire-and-forget proxies + channel = nonsense (risk-free premium) → cut |
| defensive **dodger × channel** | CONDITIONAL — legal only with `move_policy ≠ rooted` (spin class) or accepted vulnerability-window identity |
| **summon-act fifth scope row** | conjure defaults wind-up; channel-summon tether-only (§5, §6) |

## 8. The versioned packet contract — per-skill commitment fields (addendum §A, §B)

Emit ONCE; sim consumes mechanical fields, Godot consumes mechanical + presentation, loadout consumes descriptive projection. **One version bump, all fields** (rides criterion 10 provenance). Fields:

- **Cast-state-machine params:** commitment_bin; `cast_time_seconds` (now READ); for channel: `tick_interval_seconds`, ramp/break-reset params (F-2b), forced-break threshold (Y%/W, F-1b), and **`tick_tracking ∈ {tracking | fixed}`** — the field that declares beam-tracks-vs-tether-static per-tick resolution (addendum §B.2). This is DISTINCT from `move_policy` (a `rooted` beam still tracks; a `full_move` tether still doesn't) — gamora's "the packet declares which" must have a real contract slot to read.
- **Economics:** `drain_rate` (channel, per-tick) / pay-on-commit flag (wind-up + snap); sized per §3.5.
- **`move_policy` enum** `{ rooted | walk(pct) | full_move }` (addendum §B.4) — rooted default for beams/tethers; walk = curated exception (~40–60%); full_move = spin class (B12 re-cert) + the dodger×channel resolution.
- **Break rules:** voluntary release (free, any tick boundary), wind-up move-cancel (legal, forfeits cast + committed cost, no refund), forced-break (F-1b).
- **Animation/UX enum (presentation-only; sim IGNORES):** `charge_pose_id`, `channel_loop_id`, `release_anim_id`, `cast_bar {duration, interruptible}`, `channel_meter {drain_rate, sustain_s}` — a **CLOSED ENUM declared per weapon-manifestation-class** (E7 identity layer: 2H overhead wind-up, bow draw-hold, staff gather, tether stance). Kits inherit their weapon class's set; generators pick, **never invent** (keeps drax's Synty library finite, star-lord's enum closed, the D7 line intact — no LLM inventing animation names).

## 9. Cross-seam contract (ADR-004) — MIGRATION.md REQUIRED

This dispatch **adds the versioned packet contract fields** (§8) consumed by gamora (sim) and drax (Godot/loadout). This is a cross-seam contract change → **MIGRATION.md REQUIRED + Matt before tagging.** Document: the field list + version bump; the sim-consumed subset (mechanical) vs presentation subset; the read-honesty guarantee (sim and game describe the same channel because there is one description). **Note as downstream consumers in the MIGRATION.md** (do NOT draft their work): (a) **B12 spin-channel re-cert** — fires at pair-landing → G3 zero-behavioral-diff migration audit → re-cert at channel bin under `full_move`; (b) star-lord telemetry fields (addendum §C.5). **Round-trip clause is MANDATORY** (Principle 6 — §11).

## 10. Round-trip smoke on real kits (design note acceptance §9; E1 #2-FF pattern) — MANDATORY

Emit **K1 (wind-up), K7 (snap), K19 (channel)** + one **`invert`-declaring capstone kit**; print per-skill `(cast_time, per_hit, period, premium)` before/after; verify:
- **exempt slots (support/utility) byte-identical** pre/post;
- the **invert kit's EXPRESSED coordinate flips** spiky→flat;
- the applied bin + premium are **recoverable from the emitted skill record** (provenance, acceptance §10 — cert honesty, never folded invisibly);
- **zero diffs to the balance spine** (§2, acceptance §11).

## 11. #2-FF fields (MANDATORY)

- **Verdict-rendering instrument named:** the round-trip smoke (§10) + the invariance/spine-zero-diff check + the provenance read-back.
- **One-command pre-fire verification exercising the PATH:** e.g. a single command printing the current `_CAST_TIME` table + confirming `cast_time_seconds` is emitted-but-unread pre-change (the inert artifact you are activating). State the expected post-change first-log line (e.g. "K1 wind-up: cast_time=0.8s READ; premium=+X%; completion-priced; spine Δ=0").
- **Precondition state cited:** design note + addendum (this dispatch's authority); surface-ledger E4; E2 landed (`d99635a`, Q14 composite ruled); E1 landed (`bfc94eb`).

## 12. Acceptance criteria (design note §3 (1–12) + addendum §E (13–19) — these BIND)

Design note §3: 1 (math note FIRST) · 2 (coordinate lands + 324→972 bookkeeping + sampler + K1/K7/K19 pins + D7-clean docstrings) · 3 (sim reads cast_time; three v1 risk components; completion/whiff telemetry) · 4 (priced-premium verification; variance report: wind-up variance > snap variance) · 5 (regime-mix cert; pricing from certified mix only) · 6 (scope conformance: attacks full / control cast-only / support byte-identical / T4 per-capstone) · 7 (capstone transform law; expressed-coordinate cert; native+expressed record; K-number stability) · 8 (channel consistency; divergence cert-blocking) · 9 (round-trip smoke) · 10 (provenance) · 11 (table integrity + `_CAST_TIME` fate documented) · 12 (band expectation is ACTIVE-shaped; report measured KPM deltas, do NOT re-anchor — the ONE post-E3/E4 re-anchor absorbs them).

Addendum §E: 13 (cast-state machine + per-tick resolution — gamora) · 14 (drain + pay-on-commit k-aware AND economy-aware; overflow-binding guard demonstrated) · 15 (move-policy enum emitted + honored; spin certifies under full_move) · 16 (v1 forced-break rule + telemetry, Disc #17) · 17 (three-honesty-axes regime matrix — gamora) · 18 (pilot-competence floor + blind-vs-competent completion-rate delta report — gamora) · 19 (perf bound: ≥30 fights/s with state machine + ticks; baseline 36; regression >17% blocks).

**Tag (yours, emitter):** `rocket/v<X.Y>-commitment-axis-4` (seam prefix — intermediate; Matt approves any prefix drop).

## 13. Explicitly OUT OF SCOPE (prevents scope creep)

- **The sim-side build** — cast-state machine, ticks, forced-break implementation, pilot floor, regime matrix, telemetry: **gamora's half** (companion dispatch). You emit the fields + price the premium against her measured rates.
- **E3 (hybrid dual-scaling)** — own design pass, queued after E4.
- **resource-model / regen shapes** (`bc_tempo` seam, already wired) — E4 does not annex tempo.
- **damage-interrupt / stagger for wind-ups** — v1.1 named re-entry; wind-up stays un-interruptible at v1 (adding interrupt without the full stagger design double-charges the bin).
- **band tables / re-fit** — the ONE post-E3/E4 Matt-gated re-anchor; do NOT touch bands.
- **B12 spin-channel re-cert** — downstream consumer; NOTE in MIGRATION.md, do not draft.
- **QD ninth-axis admission (F-3)** — deferred to its arity stress-test; build against the 324→972 catalog space.

## 14. FLAGGED — pending KR+Matt decision (do NOT resolve in this build)

**Batch-2 sample-vs-pin `bc_commitment` fork (design note §4):** does batch-2 SAMPLE `bc_commitment` or pin defaults? This is a named **KR + Matt** sequencing decision — **FLAG it in your math note / MIGRATION.md as pending; do NOT resolve it.** It composes with the standing **K9 coordinate-drift reconcile** (the expressed-coordinate machinery §6 may be the reconcile vehicle) — flag, don't fold.

---

**Required reading (rocket, at session start):**
1. This dispatch.
2. `agentic_orchestration/gandalf/notes/2026-07-10-e4-commitment-axis-design-note.md` (§3 acceptance BINDS).
3. `agentic_orchestration/gandalf/notes/2026-07-10-e4-runtime-interaction-and-pressure-addendum.md` (§B field-level design; §C interruption honesty; §D coupling audit; §E criteria 13–19; §F RULINGS RECEIVED).
4. `generation/math/economy-axis-e2-<date>.md` — the E2 math note (`k` amplitude scalar you build the joint period model against).
5. `2026-07-10-gamora-commitment-axis-E4.md` — the companion sim-consumer dispatch (co-sign the math note against it).
6. `canonical/current-to-end-state/surface-ledger.md` — E4 row + spine-sacred discipline.

**Sign-off:** knight-rider, 2026-07-10 (FIRE-READY — Gate-1 critique pair PASS, all 10 amendments folded). The pair that prices commitment honestly is the pair that lets channel kits exist.
