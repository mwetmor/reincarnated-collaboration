# GD Live Probe — Round 2 synthesis (T9 CLOSED · first L0 datapoints)

> ## ⚠ CORRECTED SAME-DAY — read § 7 before citing any number in § 2–3
> Elrond's full-resolution re-read (schema draft `elrond/notes/2026-07-25-l0-fixture-schema-draft.md`
> § 7.1, spot-verified by gandalf via independent crops) found **nine wrong numbers in § 2 and one
> structurally wrong claim in § 1.2**. The § 7 appendix below is authoritative; § 1–3 retained
> unedited as the record of what the downscaled read produced.

**Author:** gandalf, 2026-07-25. **Source:** Matt's PC sitting #2 — raw notes + 8 screenshots
banked at `research/knowledge/gd/live-probe-2/` (notes verbatim in
`GD-console-notes-v2-raw.md`; capture window 15:17–15:34 by file mtime).

---

## 1. Headlines

1. **Spawn rig CONFIRMED.** `game.Spawn "records/creatures/enemies/zombie_a01.dbr"` spawned
   the zombie (`spawned_zombie.png`). Matt: *"paste was not necessary, typing the text above
   worked"* — the round-1 failure was purely path+quotes, not input method. **Gap 1 CLOSED.**
   The spawn-identity rig is live: we can now place a monster whose controller ground truth
   is fully in hand (zombie_a01: ViewDistance 15.0 · MaxPursuitDistance 75.0 ·
   SightAngerRate 3.0 · WanderDistance 4.0). D-b is identity for spawned fixtures.
2. **The console does not print damage lines — it prints something better.** `LogData true`
   emits **per-entity Action-State transitions**, live: observed this sitting — `Idle`,
   `Fidget`, `Moving`, `Attack`, `Flying`, `Dying` (green lines tagged per entity).
   `colsole-fight-data-test.png` shows the `killMonsters` sweep as a simultaneous mass
   `Dying` broadcast. **This is a live state-machine trace** — the T4 behavior-lane oracle
   is not PlayStats deltas alone; it is a running FSM log. `Fidget` is now LIVE-ATTESTED
   (census row confirmation #4, after AlertBeforePursue / Startup / followtheleader in
   round 1).
3. **First 3 L0 trials executed.** Per-hit damage is not surfaced; the readout is PlayStats
   deltas + Matt's timing/HP notes. All three trials are clean single-kill deltas.
4. **First in-combat DPS-field readings** (the J4 oracle Matt's `PlayStats true` was queued
   to feed): 52.69 (multi-kill window, fight-data test), 19.15 (trial-1 after), ~19.45
   (trial-3 after). Idle readings return to 0.00 — the field is a recent-window meter, not
   a lifetime average.

## 2. Trial data (Matt notes × PlayStats panel deltas)

Panel fields at this resolution carry ±1-digit uncertainty on some counters; full-res
re-read possible from banked PNGs if a number becomes load-bearing.

| Trial | Screens | Play-time Δ | Kills Δ | defaultweaponattack Δ | Fight time (Matt) | HP cost (Matt) | Life-healed Δ |
|---|---|---|---|---|---|---|---|
| 1 | (13)→(14) | ~14 s | +1 | +2 (627→629) | 1–2 s | 0 | ~0 |
| 2 | (15)→(16) | ~55 s | +1 | +2 (~629→631) | 1–2 s | 15–20 | ~+24 (2258.69→2282.66) |
| 3 | (17)→(18) | ~8 s | +1 | +2 (~633→635) | 1–2 s | 0 | ~0 |

**Consistent shape across all three: one zombie = one kill = exactly two basic attacks,
dead in 1–2 s.** Player level 6 (Max-level field). Kick-attack counter essentially static —
`defaultweaponattack.dbr` is the only skill counter that moves; the trial arithmetic is
clean.

Trial 2's HP cost 15–20 co-moves with a Life-healed delta of ~24 (damage taken, then
regenerated) — the panel's healed ledger is a usable *damage-taken proxy* when HP-globe
reading is coarse. Player HP pool 282 (bottom-left globe): 15–20 ≈ a single zombie hit ≈
6–7% of pool at level 6.

## 3. What this calibrates (J4 anchor)

Two-hit kills give the first equation-side anchor: **zombie_a01 effective HP at
charLevel≈6 ∈ (1×, 2×] player basic-hit damage.** With the DPS-field trial readings
(~19.15–19.45 over the observed window) and fight time 1–2 s, plausible per-hit damage
lands in the tens — enough to bracket-test the 720-record HP formula strings once gamora
evaluates them at charLevel 6. That evaluation is now UNBLOCKED: it needs no further live
data, only the banked panel numbers.

## 4. AlertBeforePursue — second timing datapoint

Beat ~3 s, spotted from **far** (round 1: ~2–3 s, close). Beat length stable across spot
distance — consistent with a fixed emote animation gating pursuit, not a distance-scaled
delay. Mode-20 scarcity binding (`EmoteBeforePursuingChance` ≈ 1-in-5) still unfalsified;
two sightings across two sittings is the expected base rate, not evidence against.

## 5. Rig verdict (T9 fully closed)

- **Spawn rig:** works, typed, quoted forward-slash path. Backups untested (not needed).
- **Reset:** `game.killMonsters` — proven again (mass-Dying broadcast on the log).
- **Readout stack:** PlayStats panel (aggregate ledger + recent-window DPS) +
  LogData FSM trace + screenshots. **No per-hit damage anywhere** — L0 fixture schema must
  be designed around *delta-and-trace* observables, not hit logs. This is a schema
  constraint, not a loss: our sim can emit the same observable surface for comparison.
- **T9 status: DONE — both rounds.** Every remaining live-game need is a bounded
  *trial session*, not a *probe* session.

## 6. What it unlocks (routing)

1. **L0 fixture schema (gap 5) is now the bottleneck** — trial data exists with nowhere
   structured to live. elrond + gandalf; schema fields fall straight out of § 2's table:
   per-trial {monster record FK, before/after panel captures, kills Δ, per-skill Δs,
   fight-seconds, HP-cost band, life-healed Δ, FSM-trace states observed, DPS-field
   reading, player level, location}.
2. **Q47 approaches its re-surface trigger** ("first L0 fixture bank") — three fixtures
   are one schema away from being that bank.
3. **J4 formula evaluation** at charLevel 6 vs the two-hit anchor — gamora, agent-side,
   nothing live needed.
4. **Grill session unchanged** — sheet ready; nothing in round 2 alters the six forks
   (G-4's corpse-ordering measurement and G-3's cost sheet stand as written).

**Signed:** gandalf. The oracle spoke in state names, not damage numbers — and state names
are our native tongue.

---

## 7. CORRECTION APPENDIX (gandalf, same day — DRIFT-CRITIC on own artifact)

Elrond re-read all six panels at native 1920×1080 while drafting the fixture schema; I
independently re-cropped and confirmed every spot-check. **His § 7.1 table supersedes my § 2
table entirely.** The corrections, by severity:

### 7.1 Withdrawn claim — `Fidget` is NOT a census confirmation

§ 1.2's *"`Fidget` is now LIVE-ATTESTED (census row confirmation #4)"* is **withdrawn**.
`Fidget`, `Flying`, and `Moving` appear in **none** of the 40 `ControllerMonster` rows
(grep-verified). The `LogData` console and the anger overlay speak **two different
vocabularies** — overlay emits controller states (the thing our sim also emits); LogData
appears to emit from an animation/actor-state layer. Round 1's three confirmations
(AlertBeforePursue / Startup / followtheleader) stand — they came from the overlay channel.
The LogData trace remains valuable, but comparing it to sim controller output requires a
`trace_token → controller_state` mapping table, each row its own inference — **new G1-C
scope, added to the gap register (gap 9)**.

### 7.2 Corrected numbers (full-res, elrond § 7.1 authoritative)

- `defaultweaponattack` series: **427/429/429/431/433/435** (I misread the hundreds digit
  as 6). The **+2-per-trial delta survives** — the two-hit-kill finding stands.
- Play times: **137–142 min**, not 157–162. T1 and T3 each spanned **6 s** of play time.
- **The player levelled 5→6 between T1 and T2** (and changed area). The three trials are
  **two fixture sets (N=1 + N=2), not one N=3 spread** — pooling them would fold a level-up
  into Q47's variance.
- **Ledger discontinuity between T2-after and T3-before**: +1 kill, +2 attacks, +18.51
  healed happened *off-trial*. Invisible in a delta table; visible only because readings
  were re-read. T3 is contamination-flagged (`ledger-discontinuity`) in the fixture rows.
- T2 `life_healed` delta is **+34.77**, not ~+24 — and it disagrees ~2× with Matt's
  hand-noted 15–20 HP cost (window includes post-fight regen; both readings stand,
  unreconciled, per schema O-7).
- T2-after DPS reads **0.00** — the recent window had *expired* by capture time (55 s
  trial span). The DPS field is conditionally valid on capture latency; a naive store
  would have banked a false zero.

### 7.3 J4 anchor RE-STATED (conditional — do not fire gamora's evaluation on § 3 as written)

§ 3's *"zombie_a01 effective HP at charLevel≈6"* embeds **two unattested assumptions**:
(a) **monster identity** — no note or nameplate ties the three trials to `zombie_a01`; the
spawn confirmation and the trials sit under separate headings in Matt's notes; and
(b) **monster level** — GD monster HP is a bio-formula in the **monster's own** `charLevel`
(e.g. `((charLevel*18)^1.50)-20`), which is NOT the player's level (which was 5 for T1
anyway). A level-4 vs level-8 zombie differs ~2.6× in HP under that formula. The honest
anchor: *an unidentified Devil's-Crossing-area zombie died to exactly 2 basic attacks from
a level-5-then-6 character, across two areas* — a **robustness** observation, not a
controlled fixture. gamora's formula evaluation should bracket across plausible area-band
monster levels, or wait for nameplate attestation (next-sitting sheet line).

### 7.4 What survives intact

Spawn confirmed · two-hit kills (now across two character levels — arguably stronger) ·
kick counter static · no per-hit damage anywhere · delta-and-trace observable surface ·
AlertBeforePursue ~3 s beat from far · killMonsters mass-`Dying` broadcast · DPS field as
recent-window meter (with the validity caveat sharpened).

**Method lesson (banked):** my § 2 was read from Read-tool-downscaled images with a
"±1 digit" caveat — then quoted without the caveat's consequences. The schema's answer is
structural (`read_method = 'screenshot-downscaled'` rows can't certify anything); mine is
behavioral: **full-res crop before banking any panel digit.** Elrond's crop one-liner is
now the standard instrument.
