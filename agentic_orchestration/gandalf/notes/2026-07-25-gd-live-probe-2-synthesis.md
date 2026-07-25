# GD Live Probe — Round 2 synthesis (T9 CLOSED · first L0 datapoints)

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
