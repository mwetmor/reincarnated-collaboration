# E4 Commitment Axis — Design Note (bc_commitment → cast-time as PRICED risk/reward)

**Author:** gandalf. **Ratified:** Matt, in-session 2026-07-09 — ALL SIX forks closed in two rounds
(ruling record: `2026-07-09-e4-casttime-axis-fork-elicitation.md` §RULINGS-RECEIVED + §round-2).
**Feeds:** the **rocket + gamora dispatch PAIR** (cross-seam — ADR-004 MIGRATION.md; KR sequences).
The held-dispatch precondition is CLEARED by this note landing. Ledger row **E4**
(`canonical/current-to-end-state/surface-ledger.md`); roster row **H6** (serial tracker PART F).
**Discipline:** design-spec-as-math (Disc #18 — gandalf authors intent + acceptance; rocket/gamora
derive exact values math-note-FIRST, Disc #1).

---

## 0. Scope and boundaries

**E4 is:** cast-time / wind-up / charge texture as a **THROUGHPUT-ACTIVE risk/reward axis**, sourced
from a **NEW catalog coordinate `bc_commitment`** (bins snap / wind-up / channel), made mechanically
real by a **NEW sim consumer**. Today `timing.params.cast_time_seconds` is emitted tier-varying
(`_CAST_TIME = {1:0.3, 2:0.5, 3:0.7, 4:1.0}`, `per_skill_emitter.py:194, :689, :744-745`) and
**never read by the sim** (source-verified, elicitation §0b: cadence derives from `cooldown_seconds`
alone at `spatial_engine.py:2414-2416`; the readiness gate reads only `action_available_at` :1281;
damage applies instantly at :2402). E4's build is therefore a **PAIR**: rocket (coordinate + emitter
layer + pricing) + gamora (sim consumer + measurement + regime-mix cert). It was never "cheapest of
the four" — that ledger lean died at §0b.

**E4 is NOT:**
- economy — **E2**, landed + AXIS CLOSED (`d99635a`; Q14 composite ruled 2026-07-09);
- geometry — **E1**, landed (`bfc94eb`);
- hybrid dual-scaling — **E3** (own design pass, queued after E4);
- resource-model / regen — the **`bc_tempo` seam, already wired** (`_BC_TEMPO_TO_RESOURCE` /
  `_infer_resource_model`, `season_generation_pipeline.py:250, :681-683`) and range-determined
  (Beat-B attribution scan, 0 flips). E4 does not annex tempo;
- damage-interrupt / stagger — **NAMED v1.1 re-entry** (own design pass; see §1.2).

**The spine is sacred.** `TIER_COEFFICIENTS`, `_DAMAGE_MULTIPLIER`, `BASE_SPELL_DAMAGE_L50`, base
`_ENERGY_COST` / `_COOLDOWN`: untouched. **`_CAST_TIME` is a LAYER table, not spine** — it is inert
today; whether the bin layer composes with it or supersedes it is the math note's call (flag the
choice, don't fake continuity).

## 1. Ruled semantics (Matt 2026-07-09, two rounds — all six forks)

### 1.1 The coordinate (Q-E4-4 (b) + Q-E4-6)

**`bc_commitment` joins the catalog as the sixth BC coordinate.** Bins: **snap / wind-up /
channel** — D7-clean, genre-precedented, no coinages. Space of record grows: 68,040 × 3 =
**204,120** cells (bookkeeping updates wherever the space-size is cited).

- **CellDef identity pins** where the kit's name demands it: **K1 Heavy Barbarian = wind-up · K7
  Archer = snap · K19 Channeling Cleric = channel.** All other named cells: rocket proposes
  pin-vs-rolled per cell in the math note; Matt curates at roster grain (curation ≠ authorship).
- **Sampler integration:** the coordinate samples like the other five; batch-2
  sample-vs-pin-defaults is a KR sequencing fork (§4).
- **Channel consistency LAW:** "channel" is ONE mechanic everywhere it appears — this bin, the
  rotational family's `while_channeling` persistence mode (F-substrate), and the spin-channel
  re-cert (bench B12). One name, one mechanic. A divergent second "channel" implementation is a
  cert-blocking defect.

### 1.2 Throughput-ACTIVE + the v1 risk channel (Q-E4-2 (b) — THE load-bearing ruling)

Cast-time is a **REAL lever**, ruled against the registered neutral lean with the costs on the
table. A committed cast pays a premium **only if it lands**; the risk must be real, not fictional:

| v1 risk component | Mechanism |
|---|---|
| **Motion-whiff** | damage resolves at cast **COMPLETION** against world positions **at that time** — the sim has real positions, so wind-ups genuinely whiff against targets that moved |
| **Fight-truncation** | a cast in flight when the fight ends is lost throughput (already real in the sim) |
| **Channel-lock exposure** | a channeling actor is position-committed for the channel's duration |
| ~~Damage-interrupt~~ | **v1.1 named re-entry** — needs a stagger design pass of its own; NOT smuggled into v1 |

### 1.3 The priced premium + three guards (Q-E4-5 — CLOSED, "agreed with the 3 guards"; these are LAW)

The premium is **PRICED from MEASURED completion/whiff rates** (math-note-first). Intent shape:
expected throughput ≈ completion_rate × premium × spine_throughput stays **band-center-in-
tolerance**; **VARIANCE carries the fantasy.** Mispricing in either direction is the named failure
class: D3-Inferno's unpriced wind-ups = dead skills; PoE's priced slams = a real archetype.

1. **Risk-priced premium** — expected value in-band; the payoff is variance, not a strictly-better
   number.
2. **Regime-mix certification** — the gauntlet MUST sample **mobile regimes where wind-ups genuinely
   whiff**. Pricing measured only against stationary targets is dishonest and reopens Matt's
   spiky-caster over-reward concern.
3. **Fairness-band gate at cert stays the arbiter** regardless of bin.

**One shared period model, `k`-aware (the Q-E4-5 form):** E2's amplitude scalar `k` and E4's
cast-time act through ONE period model — E4 math built blind to `k` is how the E2 conservation law
leaks one axis late. Under ACTIVE: period grows with commitment; the premium term (per-hit above
neutral compensation) is the priced payoff. **Hard instruction to the math note: derive jointly with
`k`, never layer blindly.**

### 1.4 Modulation scope (Q-E4-1 (b))

| Slot | Treatment | Why |
|---|---|---|
| primary / secondary attack (T1–T3) | **FULL** — attack slots carry the kit's bin identity | the coordinate is expressed where damage lives |
| control (T1–T3) | **cast-only** — a REAL cast time on the cast; lock magnitude untouched; does NOT define the kit's coordinate | locking someone down costs a commitment window — the anti-free-Teleport guard |
| support / utility | **EXEMPT — instant** | no fantasy in a delayed banner |
| T4 capstone | **per-capstone declaration** (§1.5) | the blanket label dies; each capstone declares honestly |

### 1.5 T4 capstone coordinate-transform law (Q-E4-3 — CLOSED + Matt extension RULED)

The blanket inert `channeled` label (**every** T4 today emits `name="channeled",
cast_time_seconds=1.0`, :744/:848) **DIES**. Every T4 capstone **declares**:

```
(commitment_bin ∈ {snap, wind-up, channel},  amplitude_delta ∈ {none, flatten, invert})
```

- mode-shift / toggle → **snap** · conjure-summon → **wind-up** (the 1.0 s "deliberate act of
  conjuring" becomes honest) · sustained-output → **channel** with real channel-lock.
- **`invert`** = whole-kit rhythm inversion (all main skills fire through the channel stance) → the
  kit's **EXPRESSED post-T4 coordinate flips spiky→flat** (Matt: *"the kit should flip its BC axis
  coordinates… right?"* → YES). A single sustained skill woven among burst skills declares `flatten`
  or `none` — legal, but NOT an inversion capstone.
- **Certification fires at the EXPRESSED coordinate**: the measured band must CONFIRM the
  declaration; **mismatch = cert FAIL** (substrate votes).
- **Bookkeeping:** the generation cell (sampler address, roster K-number) stays stable; the cert
  record carries **native + post-T4 expressed** coordinates. Precedent: the K13→K12 artillery fold.
  **E6 (proxy T4 suite) consumes this grammar.**

## 2. Mechanical shape (stated intent — the PAIR derives exact values math-note-first)

- **Emitter (rocket):** bin → per-skill cast_time per the §1.4 scope table + the premium term above
  neutral compensation. Genre bands as illustrative constraint, not values: snap ≈ at-or-below the
  perceptibility floor; wind-up ≈ 0.6–1.0 s committed pre-cast; channel = sustained (T4 1.0 s
  precedent). Constraints the math note must show: **felt-difference floor** (a wind-up must read
  distinctly heavier than a snap; sub-~0.3 s is invisible — D2 FCR deltas perceptible ~200 ms),
  **fight-completion ceiling** (≥2 completed casts of the slowest modulated skill inside a
  representative gauntlet fight — a wind-up that rarely completes is a dead slot),
  **action-cadence floor** (snap must not collapse below the sim's effective action cadence).
- **Sim consumer (gamora):** cast initiation → commitment window (actor committed; the world keeps
  moving) → resolution at completion against positions-at-completion; channel = sustained cast with
  lock exposure; truncation kills in-flight casts. **No interrupt/stagger in v1.** Instrumentation:
  completion/whiff telemetry per (bin, regime) — the pricing input.
- **The pricing loop is the pair's coupling point:** gamora measures completion/whiff rates across
  the certified regime mix → rocket prices the premium from them. This is ONE math-note
  conversation, not two independent notes.

## 3. Acceptance criteria (the dispatch pair's verdict instruments)

1. **Math note FIRST** (Disc #1), jointly authored or explicitly paired:
   `generation/math/commitment-axis-e4-<date>.md` (coordinate, bins, assignment, `_CAST_TIME` fate,
   `k`-aware period model, premium pricing) + gamora's consumer note (whiff-resolution semantics,
   channel-lock, telemetry). **MIGRATION.md** (ADR-004) for the cross-seam contract.
2. **Coordinate lands:** `bc_commitment` (snap/wind-up/channel) in
   `endgame_encounter_catalog.py`; space-of-record 204,120 bookkeeping; sampler integration;
   CellDef pins K1/K7/K19; D7-clean docstrings.
3. **Sim consumer real:** `cast_time_seconds` is READ; the three v1 risk components mechanically
   present; completion/whiff telemetry instrumented per (bin, regime).
4. **Priced-premium verification:** premium derived from measured rates over the certified regime
   mix; certified expected throughput in fairness band; **variance report shows wind-up variance >
   snap variance** (the fantasy is real, not cosmetic).
5. **Regime-mix certification:** the gauntlet samples mobile regimes (mobility mix pinned in the
   math note); pricing derives ONLY from the certified mix (guard 2 as law).
6. **Scope conformance:** attacks full; control cast-only with kit coordinate unaffected; support
   byte-identical; T4 carries per-capstone declarations.
7. **Capstone transform law:** declaration schema on every T4; expressed-coordinate cert path
   (declaration-vs-measured mismatch = FAIL); cert record carries native + expressed; K-number/cell
   stability verified.
8. **Channel consistency:** one channel mechanic across bin / `while_channeling` persistence / spin
   re-cert — divergence is cert-blocking.
9. **Round-trip smoke on real kits** (E1 #2-FF pattern): emit K1 (wind-up), K7 (snap), K19
   (channel) + one `invert`-declaring capstone kit; print per-skill (cast_time, per_hit, period,
   premium) before/after; verify exempt slots byte-identical; verify the invert kit's expressed
   coordinate flips.
10. **Provenance:** applied bin + premium recoverable from the emitted skill record (cert honesty —
    visible downstream, never folded invisibly).
11. **Table integrity:** zero diffs to the balance spine; `_CAST_TIME`'s fate (composed vs
    superseded) explicitly documented in the math note as a layer-table decision.
12. **Band expectation is ACTIVE-shaped:** encounter KPM WILL move (this axis is a lever, not
    texture). Per the Q14 composite ruling there is **no immediate post-E4 re-fit** — deltas are
    measured and reported, and the **ONE end-of-axis-run band re-anchor (post-E3/E4, Matt-gated,
    de-censored instrument)** absorbs them. The dispatch reports the measured deltas; it does not
    re-anchor.

## 4. Sequencing (KR-visible)

- **Precondition MET:** E2 axis CLOSED (Q14 composite, 2026-07-09). Sequence lean unchanged:
  **E4 → E3**, then the F/P dialects emit, then the ONE Q14 re-anchor.
- **Dispatch shape:** a rocket + gamora **PAIR** with MIGRATION.md — NOT emitter-only. The pricing
  loop (§2) is the coupling point; KR should sequence the two seams against one shared math-note
  conversation.
- **Batch-2 fork (KR + Matt):** does batch-2 SAMPLE `bc_commitment` or pin defaults? Named, not
  resolved here. Composes with the standing **K9 coordinate-drift reconcile** — the
  expressed-coordinate machinery (§1.5) may be the reconcile vehicle; flag, don't fold.
- **Named re-entries:** damage-interrupt/stagger risk component (v1.1, own design pass); E6
  consumes the capstone declaration grammar; H6 (Charge-up Caster) is the roster row this axis
  redeems — its kit emits once the pair lands.

## 5. Player consequence (why this axis exists)

Today every cast in the game fires the instant it is chosen — there is no weight of commitment
anywhere in the hands. After E4, the same cell produces a **snap** hand (reactive, mobile,
metronome) and a **wind-up** hand (commit, watch the world move, land the big one) as a **real
priced gamble** — the premium exists only if you complete casts, and mobile enemies genuinely make
you miss. That is the D2 Smiter / PoE slammer archetype arriving as mechanics, not costume. Control
stops being a free lock — committing to the lock is the cost. And T4 channel capstones become
honest: a channel that inverts a kit's whole rhythm is certified at the rhythm it actually plays.
Matt ruled the heavier, truer fantasy over the cheap texture, with the costs on the table — this
note is those costs, itemized.

**Signed:** gandalf, 2026-07-10. Rulings: Matt, 2026-07-09 (two rounds, all six forks).
