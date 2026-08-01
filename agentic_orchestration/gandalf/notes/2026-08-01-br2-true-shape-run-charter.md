# BR-2 — TRUE-SHAPE run charter (the fight the substrate already describes)

**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-08-01 · **Pattern:** desirable-run
(`operating-procedures/desirable-run-pattern.md`; F1–F4 audited in §0)
**Ledger of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — Scopes 1–43 bind. This
charter composes them; it does not restate them.
**Predecessor:** BR-1 (BATON-RENDER), closed 2026-08-01, exit review
`gandalf/notes/2026-08-01-br1-exit-review.md`.
**Matt authorization:** 2026-08-01 — *"please write the charter with pre-registered gates and process
it all, sequentially as an autonomous run, pushing commits as you go."*

---

## §0 — Fit audit + the intent sentence (rubric law, applied to ourselves first)

**§0 INTENT, in one sentence:** *render the fight the substrate has been describing all along — the
true shapes, the true motion, the player's whole kit, and the HUD Matt chose — and cut one watch
that proves it.*

| Fit | Verdict |
|---|---|
| **F1 — enumerable?** | YES. 200 current-generation traces; 13 census recommendations; 6 Matt list-items A–F, all ruled; 1 pinned HUD reference image; 1 naming table of 7 rows. Countable, listable, diffable. |
| **F2 — decidable?** | YES. Every gate in §4 is a count, a measured distance, a grep with an expected zero, or a byte-diff. |
| **F3 — pre-drainable?** | YES — drained across Scopes 40/40-a/40-b/41/42/42-a/43 before this charter existed. Two residual forks are ruled in-run below (R-BR-32, R-BR-33), veto-open. |
| **F4 — authority-resident?** | YES for the residual reasoning-boundaries (shape fidelity, VFX composition, HUD binding honesty). Taste cuts, push, and charter amendment remain Matt's. |

**Predicate-vs-intent diff (rubric law, §6 obs 3).** What the gates in §4 do NOT measure, said out
loud: whether the fight *feels* dramatic, whether the blood reads as violence rather than decoration,
whether the HUD is beautiful. Those are M-EYE questions and no gate substitutes for them. The gates
measure **truth** — that what is drawn is what the substrate says. A run can pass every gate here and
still be judged flat, and if that happens the gates were right and the run still failed.

---

## §1 — Bounded substrate (frozen at launch)

- **S-1 — traces:** 200 replay traces at `~/Games/reincarnated-godot/tmp/wr3acc/traces/`, schema
  `g5-replay-trace/v1`, 90,508 records, 1,556 telegraphs. Watch seed **74000909**
  (`boss__FULL__seed74000909.jsonl`, 361 ticks, 98 events).
- **S-2 — the census:** `legolas/research/2026-08-01-trace-descriptor-census.md` — 13 ranked
  recommendations, tiered by cost in Scope 43.8.
- **S-3 — the rulings:** Scopes 40 (M-1…M-4), 40-a (naming), 40-b (HUD-FIX-1 reconciliation), 41
  (D+E), 42 + 42-a (HUD), 43 (census synthesis). Rulings R-BR-1…R-BR-31.
- **S-4 — the HUD spec:** `gandalf/reference/2026-08-01-hud-bakeoff-MATT-CHOICE.png` + Scope 42's
  two amendments + Scope 42-a's slot table and copy ruling.
- **S-5 — the scene:** `reincarnated-godot` at `ba3276e` (post-HUD-FIX-1), crypt corner,
  CAM-LOCK GD camera, PC-LIGHT lighting, Scope 12–21 lighting cosmology inherited and NOT reopened.
- **S-6 — the emission code:** `reincarnated-engine/src/reincarnated/simulation/`
  (`gd_nova.py`, `gd_boss_kit.py`, `spatial_gauntlet/spatial_telemetry.py`).
- **S-7 — the naming table:** Scope 40-a, 7 rows, element + role.

**Frozen means frozen.** Discoveries beyond this substrate are logged as findings for BR-3, never as
silent scope growth. The run cannot move its own goalposts (§5.1 standing safety).

## §2 — Decidable target-state

**T-1 — one integrated watch MP4** of the seed-74000909 fight in the crypt corner at the GD camera,
in which ALL of the following are present and verified per-cell before the cut:

1. **Nova** draws 16 discrete prongs at 22.5°, travelling outward at 14.0 m/s over 0.857 s, phased
   per cast by `spoke_offset_rad` — and its ring intensity **ramps outward** (hot rim, cool core).
2. **Wave** draws an oriented **rect**, 16.0 m × 6.0 m at `orientation_rad`, **sweeping** at
   11.4286 m/s over 1.4 s. Not a cone. Not static.
3. **Blizzard** draws **24 orbs in 4 volleys 2.0 s apart**, falling from altitude at 24.0 m/s across
   an 8.0 s window — and its tell is **the descent**, not a caster glow.
4. **Player kit has visual identity:** claw wind-up glow (red, per Scope 41), a distinct signature
   for `rip_and_tear_r16` (line, 14 m), and a persistent visual for the DoT channel.
5. **Death is blood:** splatter on kill, pool persisting for the room, burn/dissolve retired.
6. **HUD is the ported bake-off layout:** 9 boxes with 6 bound per Scope 42-a A-3, plate spanning all
   9, playstats below the mini-map, copy per A-4, names per S-7.
7. **No vendor string on frame** (R-BR-30), **no `range_m` read by any render path** (R-BR-27).

**T-2 — the truth ledger:** a landing note per cell, and one BR-2 exit review, in which every claim
above names the gate that proved it.

## §3 — Cell sequence (sequential; single-writer godot tree)

| # | Cell | Owner | Repo | Scope |
|---|---|---|---|---|
| 1 | **TRACE-FILL-1** | gamora | engine | Populate `projectile_velocity_ms` (wave 11.4286, blizzard 24.0) + `prong_count` (blizzard 6). Regenerate the S-1 battery. Emission-only; must not perturb simulation. |
| 2 | **VFX-TRUTH-1** | drax | godot | The three true shapes + travel + reverse falloff. Riders: naming table overwrite (S-7), `clip_text` on `tname`. |
| 3 | **COMBAT-JUICE-1** | drax | godot | Scope 41 D+E: claw charge glow, line-skill identity, DoT visual, blood splatter + persistent pools, burn retired. Item F clutter per R-BR-33. |
| 4 | **HUD-PORT-1** | drax | godot | Scope 42 + 42-a in full. The mini-map built REAL or omitted (G-6d). |
| 5 | **BR2-WATCH** | drax | godot | Integrated cut, completeness checklist, owner-eye deliverable. |

Read-only measurement (galadriel) may run in parallel at any step. Every cell opens on **its inlined
scope text, not the 3,400-line ledger** (the r1-stall lesson, Scope 40). Every cell banks its landing
note to the meta-repo and **pushes** (§5).

## §4 — Pre-registered gates (pinned BEFORE results)

**G-1 — TRACE-FILL emission purity.** Regenerated seed-74000909 trace is **byte-identical** to the
current one except for exactly the three added field values. Rationale: the fill writes constants
into emitted records and must consume no RNG. *A diff anywhere else is a FAIL and a finding — it
would mean the emission path is entangled with simulation.*
**G-1b:** across the regenerated battery, `projectile_velocity_ms` non-null on **100 %** of `wave`
and `blizzard` telegraphs at the stated values; `prong_count` = 6 on 100 % of `blizzard`.

**G-2 — true shapes, measured headless.**
- **G-2a nova:** 16 discrete prong instances counted; angular spacing 22.5° ± 0.5°; outermost extent
  reaches 12.0 m ± 0.2 m at t = 0.857 s ± 0.03 s.
- **G-2b wave:** rendered footprint is a rectangle measuring 16.0 × 6.0 m ± 0.3 m, oriented within
  ± 3° of `orientation_rad`; leading edge advances monotonically, total sweep 1.4 s ± 0.05 s.
- **G-2c blizzard:** 24 impact events rendered per cast, in 4 volleys of 6; inter-volley interval
  2.0 s ± 0.05 s; total active window 8.0 s ± 0.1 s.

**G-3 — the extent law (R-BR-27).** `grep` over all render paths returns **0** reads of
`skills[].range_m`. Zero, not few.

**G-4 — reverse falloff (R-BR-28).** Sampled ring intensity is monotonically non-decreasing from
centre to rim, with a visible step at 2.5 m.

**G-5 — combat identity.**
- **G-5a:** claw wind-up glow present on ≥ 90 % of the fight's cone-geometry damage events.
- **G-5b:** `rip_and_tear_r16` has an on-frame signature distinguishable from the claw on **all**
  line-geometry events (pixel-diff against a claw-only control ≠ 0 in the skill's own frames).
- **G-5c:** a DoT visual is present on a target for ≥ 90 % of frames in which that target carries the
  `bleed` ailment.
- **G-5d:** **0** burn/dissolve frames. Blood pool present on frame from each death to the final
  frame of the watch.

**G-6 — HUD.**
- **G-6a:** 9 boxes present; boxes 1–6 bound per A-3; 7–9 blank/open. Cooldown fill drives boxes 2–3
  from `skill_cooldowns`.
- **G-6b:** 0 px of any skill box outside the backing plate (the 9-slice span); crest remains centred.
- **G-6c:** copy census returns **0** occurrences of `TOO HOT`, `page 12`, `STRUCTURE II`, `treasure
  room`; context line reads `Battle Simulation Arena`; energy label reads `ENERGY` (R-BR-32).
- **G-6d — mini-map:** built from real `x_m`/`y_m` over the arena bounds, or **omitted**. A
  decorative mini-map is a FAIL. (Rubric law: a sim render does not draw fake instruments.)
- **G-6e:** re-run G-M3 census — **0** vendor tokens over all distinct on-screen strings; every
  displayed name matches the S-7 table exactly.
- **G-6f:** playstats slab renders below the mini-map, 0 px overlap with it or the target panel.

**G-7 — no regression.** R-BR-19 framemap identity holds (worst |Δt| = 0). G-M2 re-run: 0 orphan
sweep pixels. G-M4 re-run: 0 dead-actor widget-frames.

**G-8 — watch completeness.** Every T-1 item 1–7 present on frame at least once; checklist enumerated
in the BR2-WATCH landing note, item by item, with the frame index that proves it.

**G-9 — push truth (red-main tripwire, §6 obs 4).** Each cell's commits are pushed AND verified
present on the remote before the next cell opens. The run is not done at commit; it is done at
verified remote state.

**Gate FAIL = processable finding, never a terminal event.**

### Honorable fallbacks (declared now, not improvised later)

- **G-1 FAIL** → the fill is entangled with simulation. **HALT the regeneration**, keep the S-1
  traces as they are, and render wave/blizzard motion from constants **declared on frame as
  declared-not-sourced**. Cells 2–5 proceed; the entanglement becomes BR-2's headline finding.
- **G-2c infeasible at 24 orbs** → render 6 orbs per volley with volley rhythm intact and name the
  reduction in the landing note. Rhythm outranks count.
- **G-6d unbuildable in-cell** → **omit** the mini-map. Never fake it.
- **Any cell exceeding two relaunches** → park it, carry its scope to BR-3, and continue the
  sequence. A stuck cell must not stall the run.

## §5 — Matt interface

- **Push:** Matt's *"pushing commits as you go"* is read as authorizing push for **all three repos**
  as the run proceeds. **Stated fact, not a choice:** godot history is linear, so pushing BR-2's
  godot commits necessarily pushes the **20 accumulated local commits** from BR-1 and the fix pass.
  Flagged here rather than performed silently; one word reverses it.
- **Owner-eye checkpoints (§6 obs 2), pre-registered:** a clip is emitted to Matt after **cell 2**
  (true shapes) and after **cell 4** (HUD). The run **does not halt** for them — it continues, and a
  Matt veto arriving at any time is treated as a processable finding that reopens the named cell.
  This preserves autonomy without putting his eyes only at the end, which is the failure §6 obs 2
  was written from.
- **Commitment-boundaries that still HALT:** any purchase; any charter amendment; any change to the
  locked lighting cosmology or CAM-LOCK; taste vetoes (veto-open by construction).
- **Red-flag pings only** mid-run.
- **Out of BR-2 scope, parked to BR-3:** the R-BR-21 body verdict, parity grade, beam-glow re-judge,
  music/camera taste, the F-BR-5 principle, and the ~8.6 GB `tmp/` prune.

## §6 — Residual forks ruled in-run (veto-open)

- **R-BR-32 — the energy orb reads `ENERGY`.** The mock says `41 MANA`; our field is `energy`; we do
  not simulate mana. Under the standing law that an on-screen number must name what it is, the label
  changes. One word reverses it.
- **R-BR-33 — the arena is LIVED-IN.** Item F, the clutter/blood-persistence/slits question, ruled as
  one word: **lived-in.** Bone piles return; blood pools persist for the room; the slits stay
  ceiling-less and are not explained. Reasoning: Scope 41 already ruled blood persists *so the room
  accumulates the record of what the player has done* — clutter and persistence are the same
  argument, and a Battle Simulation Arena that shows wear is a stronger frame than a clean box,
  because it says this has happened before and will happen again. That is the death-faith frame doing
  work in set dressing. One word reverses it.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-08-01.
