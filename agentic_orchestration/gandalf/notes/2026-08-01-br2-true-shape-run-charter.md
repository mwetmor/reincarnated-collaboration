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

---

## ADDENDUM 1 — cell 1 landed; cell 1b inserted (conductor, 2026-08-01)

### Cell 1 — TRACE-FILL-1: **G-1 PASS, G-1b PASS, G-9 verified**

`bce46fd9` + `2a9ebb02` (engine), `a5b03e14` (meta), all confirmed present on `origin/main`.

**G-1 came back stronger than it was asked for.** The gate wanted one trace; gamora produced three
limbs: (1) a **control arm** — seed 74000909 regenerated at the pre-change HEAD is byte-identical to
the banked trace, md5 `6c4baeb…`, which proves the *generator* is reproducible and therefore
attributes the whole post-change delta to this change alone; (2) a whole-battery diff — **90,708
records, exactly three differing paths**, `projectile_velocity_ms` 1,086 · `prong_count` 570 ·
`engine_git_hash` 200, no fourth path anywhere; (3) 200 fights re-run reproducing `wr3_acc.json`
digit-for-digit and re-selecting the same seed. **No RNG moved.**

The SIMULATION/PROVENANCE split was written into the math note *before* the run rather than carved
out after — `engine_git_hash` **must** change, because that field's entire job is to say which code
ran, and reproducing the old hash would have been the defect. Pre-registering the exception is the
difference between a principled carve-out and an excuse.

G-1b as counts, not adjectives: **516/516** wave · **570/570** blizzard velocity · **570/570**
blizzard `prong_count` · **470/470** nova controls unmoved. 1,556 total — legolas's own denominator.

⚑ **For cell 2:** the emitted float is **`11.428571428571429`**, not the census's rounded `11.4286`.
An equality test against the rounded value matches nothing.

⚑ **Semantic shift drax must not generalise over.** `projectile_velocity_ms` now carries a
**per-family axis** — radial (nova) / forward (wave) / **downward** (blizzard) — and the header's
`frame` block does not declare that axis. Applying the nova's closed form to the blizzard draws an
expanding ground circle: **a different lie from the static one, not a smaller one.** `prong_count` is
per *launch event*, not per cast.

### ⚑ THE FINDING THAT FORCED CELL 1b — and my own fallback was written on a false premise. Again.

G-2c asks for 24 orbs in 4 volleys 2.0 s apart across an 8.0 s window. **After cell 1 that is still
not satisfiable from the trace.** `prong_count = 6` is not multipliable by anything a consumer can
read: `n_volleys` (4), `volley_interval_s` (2.0) and `active_duration_s` (8.0) live in
`BlizzardParams` and reach **no** consumer. A renderer can honestly draw **one volley of six** and
has no trace-sourced basis for the other eighteen — while `radius_m 8.0` goes on representing all of
it.

**My declared G-2c fallback — "render 6 orbs per volley with volley rhythm intact" — cannot be
executed, because the rhythm is exactly what is missing.** I wrote a fallback that assumed a field I
had not verified existed.

**This is the second time in three days.** R-BR-3 declared *"travel is ABSENT from schema"* and on
that false premise refused 39 travel-bearing effects; it was reversed as R-BR-24 only because Matt
asked me to open the packet. Now a pre-registered fallback rests on a rhythm the schema never
carried. Same shape both times: **I ruled on what the data does, from memory of the data, without
re-reading it.**

**Standing discipline, minted here (R-BR-34):** *any ruling or fallback whose validity depends on a
field existing must cite the census line or the probe that confirms it, in the ruling itself.* A
ruling that names no evidence is a recollection wearing a ruling's clothes.

### Cell 1b — TRACE-STAGE-1 (gamora, engine) — INSERTED, and why this is not goalpost movement

**Ruled: this is sequence extension inside the frozen substrate, not a charter amendment.** The
fields being added are **census recommendations 3, 4 and the §3d per-drop radius** — all of them
already inside S-2, which was frozen at launch. G-1 is closed with a recorded PASS; nothing about it
moves. What changes is that one more cell stands between here and G-2c. Stated with the veto open;
one word from Matt collapses it back to the honest single volley.

**The alternative I rejected, and why.** Rendering one volley of six is honest and cheap — but the
blizzard is *the* headline defect this run exists to fix (8.0 s reading as 0.857 s), and a quarter of
it is not a fix. Declaring 4/2.0/8.0 on frame as declared-not-sourced is worse: it puts numbers on
screen that the substrate refuses to say, which is the exact thing R-BR-24 and the rubric law were
written against.

**Scope of 1b — four nullable fields, emission-only:**
- `duration_s` on the telegraph (nova 0.857 · wave 1.4 · **blizzard 8.0**) — census rec 3, *"the
  single biggest omission"*: a renderer currently cannot know how long to hold a danger zone.
- `stage_count` (blizzard 4) + `stage_interval_s` (blizzard 2.0) — census rec 4.
- **`hit_radius_m` per drop (blizzard 1.32)** — census §3d. Without it the renderer must treat the
  **8.0 m scatter radius as lethal area**, overstating per-drop danger by roughly **6× in area**.
  That is a legibility lie of the same class as the nova's reverse falloff, which this run already
  committed to fixing under R-BR-28. Fixing one and shipping the other would be incoherent.

**Pre-registered gates for 1b** (pinned now, before results):
- **G-1c — emission purity, again.** Regenerated battery differs from the cell-1 battery in **exactly
  these four paths plus `engine_git_hash`**, no fifth path. Same three-limb evidence standard.
- **G-1d — coverage as counts.** `duration_s` non-null on 100 % of all three families at the stated
  values; `stage_count`/`stage_interval_s` on 100 % of blizzard; `hit_radius_m` on 100 % of blizzard;
  null elsewhere, deliberately.
- **G-1e — MIGRATION + schema version handled**, and cell 1's `traces_PREFILL_ddbdebc8/` preserved.
- **Fallback:** G-1c FAIL → stop, keep the cell-1 battery, and G-2c falls back to **one honest volley
  of six** with the reduction named on frame and in the note.

**G-2c is amended to match what 1b makes available** — 24 orbs, 4 volleys, 2.0 s ± 0.05, 8.0 s
window ± 0.1, **per-drop impact drawn at 1.32 m, scatter drawn as scatter and not as lethal area.**

### Banked to BR-3, not fixed here

The pre-existing engine test baseline: **10,024 passed / 60 failed / 21 errors**, and the identical
60/21 reproduce on a stashed clean tree (generation, kit-space, foundation, season-generation seams;
**zero in `spatial_gauntlet`**). Not this run's seam, not this run's substrate — but measured rather
than assumed, and routed to knight-rider for the owning seams.

Also BR-3: the `-dirty` stamp near-miss (a battery nearly shipped stamped `ddbdebc8-dirty`, a hash
naming no commit — **commit before generate** is now a standing order for any trace-regenerating
cell), and gamora's `NullInstrument` guard, which is the null-instrument tripwire from Scope 40-b
independently implemented one cell later. Two seams reaching the same discipline unprompted is the
strongest evidence it is real.

---

## ADDENDUM 2 — the arsenal re-opens; cell 1c inserted (Matt authorized, 2026-08-01)

**Matt:** *"go, and definitely add this into the run."*

### The finding, cited (R-BR-34 applied to myself)

`drax/notes/2026-08-01-arsenal-harvest.md` §5, verbatim: **`Barrage/Nova` (14)** — *"Nova-shaped
barrages of **flying** projectiles. **R-BR-3 forbids invented travel** — our schema has no projectile
flight, so these would render a mechanic that does not exist."* And **`Missiles` (25)**, `Beams`,
`Chains`, `Flamethrower`, `Orbital Beam` — *"Travel- or channel-bearing. Same R-BR-3 bar."*

**That is the 39.** R-BR-3 was false; the schema has carried `projectile_velocity_ms` and
`t_launch_s` all along, and R-BR-24 reversed it. *Nova-shaped barrages of flying projectiles* is a
literal description of `primordian_frigidring_star_r5`. **We refused the folder that contains the
answer, because I misremembered our own schema.**

A second tier was never refused at all — §5 records it as *"Queued, not refused"*, one manifest edit
away now the pipeline runs in a single command: **Aura (6) · Curses (9) · Debuffs (9) · Enchant (8) ·
Necromancy (6) · Death (8) · Gore (11) · Explosions (32) · Muzzleflash (30) = 119.**

**39 + 119 = 158 effects**, in a pack we own, through a pipeline that already gated **33/33 config**
and **33/33 pixel** with an in-run empty-stage control, EULA honoured by construction (the
transcriber is a parser, never a generator; no pack content was ever fed to a model).

### R-BR-35 — THE PACK SUPPLIES MATERIAL; THE TRACE SUPPLIES GEOMETRY

Standing law for all VFX work from here. A pack effect is authored at its own scale, its own count,
its own speed — **none of which we adopt.** We take its *material* (mesh, texture, shader, colour,
fade) and drive **how many, at what angle, how fast, how far** from the trace: `prong_count`,
`spoke_offset_rad`, `projectile_velocity_ms`, `radius_m`, `orientation_rad`, `duration_s`,
`stage_count`, `stage_interval_s`, `hit_radius_m`.

**Why this makes the asset problem small.** The source itself uses **one mesh — `frostorb01.msh` —
for both the nova prong and the blizzard drop**, at scale 1.0 and 1.2 (census §3c). We do not need a
nova effect and a blizzard effect. We need **one good ice projectile** and the numbers we now have.

### Cell 1c — ARSENAL-2 (drax, godot) — INSERTED, runs in parallel with 1b

**No contention, stated explicitly:** gamora (cell 1b) works in `reincarnated-engine` and writes
traces to the **untracked** `reincarnated-godot/tmp/wr3acc/`. ARSENAL-2 works in **tracked** godot
paths only, must **not read `tmp/wr3acc/` at all** (gamora is rewriting it), and must commit named
paths rather than `-A`. Single-writer on tracked files is preserved.

**The eight material needs, and where each is sourced:**

| # | Need | Target folder | Status |
|---|---|---|---|
| 1 | ice projectile + flight trail (nova prong AND blizzard drop) | `Barrage/Nova` (14), `Missiles` (25) | **un-refused** |
| 2 | projectile impact burst (×24 blizzard, ×16 nova) | `Explosions` (32) | queued |
| 3 | sweeping cold wall (the 16×6 m rect) | `Beams`, `Flamethrower`, + harvested `LightningWave` | un-refused |
| 4 | claw wind-up glow (Matt's item D) | harvested `SwordChargeUp` + `Muzzleflash` (30) | ⚑ see debt |
| 5 | line-skill signature (`rip_and_tear`, 14 m) | `Chains`, `Beams`, harvested sword trails | un-refused |
| 6 | blood splatter + persistent pool (item E) | **`Gore` (11)**, `Death` (8) | queued |
| 7 | DoT / ailment channel (`bleed`, 10,913 frames) | `Debuffs` (9), `Curses` (9) | queued |
| 8 | icearmor aura (live 7,200 frames, invisible) | `Aura` (6) | queued |

### Pre-registered gates for 1c

- **G-10 — harvest gates hold at the established standard:** config gate + pixel gate **100 %** of
  newly harvested effects, each against an **in-run empty-stage control**, counts reported per effect.
- **G-11 — the moving-host test (a debt this cell pays).** The trail class passed the pixel gate at
  **7 / 139 / 232** lit pixels (`SwordTrailShadow` / `SwordChargeUp` / `SwordTrail`) against
  12,000–47,000 for hero effects, because Unity draws ribbons behind a **moving** host and a static
  stage gives them nothing to streak along. `SwordChargeUp` **is** Matt's item-D charge glow. PASS =
  lit-pixel count on a moving-host rig materially exceeds its static baseline; FAIL = the effect is
  named unusable and item D sources elsewhere. *"Not broken and not proven" is not a state we ship.*
- **G-12 — licence method unchanged.** Parser-never-generator; per-effect provenance manifest where
  every emitted number traces to a line in a source prefab. Any effect that cannot be traced is
  **refused, not faked** (the harvest's own `unmapped` vs `partial` discipline).
- **G-13 — coverage, the gate that outranks accuracy** (§6 obs 1): **every one of the eight needs
  above has ≥ 1 gate-passing candidate**, or the gap is named. A harvest that lands 100 effects and
  misses blood has failed this run.

**Fallback:** any family failing G-10/G-11 → named gap, and cell 2 composes from what passed. A gap
is a finding; a silent substitution is not.

**Purchase remains OUT.** Matt's call, deliberately deferred: buying before we know which families
read thin is how one buys the wrong assets. Revisit after the cell-2 owner-eye clip, when the
question is specific.

### §3 cell table amended

| # | Cell | Owner | Repo |
|---|---|---|---|
| 1 | TRACE-FILL-1 | gamora | engine | **LANDED, G-1/G-1b PASS** |
| 1b | TRACE-STAGE-1 | gamora | engine | in flight |
| **1c** | **ARSENAL-2** | **drax** | **godot** | **inserted here, parallel with 1b** |
| 2 | VFX-TRUTH-1 | drax | godot | opens when 1b + 1c land |
| 3 | COMBAT-JUICE-1 | drax | godot | |
| 4 | HUD-PORT-1 | drax | godot | |
| 5 | BR2-WATCH | drax | godot | |

---

## ADDENDUM 3 — cell 1b landed; three rulings; one probe outstanding (conductor, 2026-08-01)

### Cell 1b — TRACE-STAGE-1: **G-1c PASS, G-1d PASS, G-9 verified**

Engine `5b8c724b` + `28eddef4`, meta `efa8b2ab`, all on `origin/main`.

The control limb came back **stronger than cell 1's**: the whole 200-trace battery regenerated at
pre-change HEAD, **90,708 records, ZERO simulation paths differing** — and the only moving field,
`engine_git_hash`, was reconciled by `git diff --stat` showing the intervening commit touched
`AGENT_STATE.md` and nothing else. Post-change: four sim paths at exactly 1,556 each (470 + 516 +
570), `engine_git_hash` at 200, **no fifth path in 90,708 records.**

G-1d as counts *including the nulls*, which is the part that matters: `stage_count` /
`stage_interval_s` / `hit_radius_m` at **570/570** blizzard and **986 null elsewhere with 0
non-null** — and **`absent_key` 0 in every cell**, which is the R-WR3-40(2) guard: a mistyped field
name would show as 1,556 absent, not as null. The instrument can tell "deliberately empty" from
"never arrived."

### ⚑ THE INSERTION WAS NOT OPTIONAL — Scope 43.1 was wrong

I banked in Scope 43.1 that the blizzard's 24 drops were *"already individually addressed… renderable
today without a schema change"* via the `attack_id` string. **False.** Only **156 of 570** casts
produce any damage record at all — a drop that hits nothing leaves no trace of itself, and per-volley
counts decay 87 → 60 → 25 → 14 as the player leaves the scatter. Parsing `attack_id` would have
rendered a blizzard that **thins as it goes and vanishes when the player dodges well.**

Cell 1b was not a nicety. It was the only honest route. And this is R-BR-34's third confirmation in a
week: I asserted a field's usefulness from a structural reading without probing what fraction of the
records actually existed.

### R-BR-36 — `duration_s` is LIVENESS; sweep time is TRAVEL. They are different quantities.

The wave ships `duration_s = 1.4874999999999998`, not 1.4. Gamora derived it under **one uniform
definition across all three families** — `event.t_expiry − fire_time_s`, no family branch — which is
the deliberate opposite of `projectile_velocity_ms`'s per-family axis, and it is the right call: a
field whose meaning forks per family is the defect we have now found three times.

**The 0.0875 is real** — the wave's band is 1.0 m deep, so the trailing edge clears the far end after
the leading edge arrives. **G-2b is amended: the sweep is graded from `range_m ÷
projectile_velocity_ms` = 16.0 ÷ 11.428571428571429 = 1.4 s, NOT from `duration_s`.** A renderer that
animates the front from `duration_s` fails G-2b by 0.0375 s, and would deserve to.

⚑ **This is the same defect class for the third time**, and it is worth naming as a class:
`range_m` carried AI-trigger *and* extent; `wind_up_s` carried charge-up *and* fall time; now
`duration_s` would carry liveness *and* travel. **One scalar per telegraph cannot answer both "how
long is this dangerous" and "how long does the front take."** Standing distinction: **liveness comes
from `duration_s`; travel is always derived from velocity and extent.**

### R-BR-37 — G-2c re-pinned to the measured rhythm, and the 8.0 s is not a defect

Measured (R-BR-34, evidence cited): **186 blizzard damage events land at offsets exactly
{0.0, 2.0, 4.0, 6.0} from their own `fire_t_s`, zero variance.** Cast→last-impact 6.8333 s;
first→last **6.0 s**. `duration_s` = 8.0 over-bounds the last impact by exactly one volley interval —
**which is correct, not a bug**: four volleys on 2.0 s centres occupy a half-open [0, 8.0) schedule
whose last member fires at 6.0.

**G-2c re-pinned:** 4 volleys × 6 orbs = 24; impact times at `fire_t_s` + {0, 2, 4, 6} **± 0.05 s**;
first→last **6.0 s ± 0.05**. The old "8.0 s window ± 0.1" is **retired as a visual criterion** —
holding a danger decal for 2.0 s after the last orb teaches the player to fear an empty floor, which
is the reverse-falloff error wearing different clothes. **Draw the danger for the danger; the 8.0 s
is scheduling, not threat.**

### ⚑ RULING DEFERRED PENDING PROBE — the wave's 3.0 → 6.0 taper

Gamora reports the source lane widens **3.0 → 6.0 m** while the telegraph emits only the **end**
width, so a uniform 16.0 × 6.0 rect **overstates the lane 2× at the origin** — and the origin end is
exactly where the player stands, since his primary skill is a 2.0 m cone. This is census rec 13, in
substrate, and it is the same class as the `hit_radius_m` overstatement I pulled forward.

**But I am NOT firing a cell 1d yet, because the obvious fix may be a lie in the other direction.**
The governing question is not what the *source* says — it is **what our simulation resolves damage
against.** If our sim hit-tests a uniform 6.0 m rect, then a uniform 6.0 m rect is the true danger
zone *in our game*, and drawing a trapezoid would misinform the player about the sim they are
actually playing. In that case `start_width_m` is a **simulation-fidelity** question for BR-3, not a
presentation fix for BR-2.

R-BR-24's principle, stated generally: **we render what the sim does, not what the source says.**
Probe sent to gamora. Cell 2's brief carries the uniform rect until it answers.

**Cell 2 opens when ARSENAL-2 (1c) lands.**

---

## ADDENDUM 4 — the probe answered (a); cell 1d inserted, and generalized (conductor, 2026-08-01)

### The answer: the simulation TAPERS. `start_width_m` is on the damage path.

`gd_boss_kit.py:645` — `(start_width_m + (end_width_m − start_width_m) · u / distance_m) · 0.5` —
read by the lateral test at `:680`, reached from `wave_hits` `:860`. **A linearly tapering lane,
evaluated per-target at that target's own along-axis position.**

`full_width(u) = 3.0 + 0.1875·u`, reaching 6.0 **only at u = 16.0 m — the lane's terminal point.**
Overstatement of the drawn uniform 6.0: **2.00× at u=0 · 1.78× at u=2 · 1.33× at u=8 · 1.00× only at
16.** The area figure (96 vs 72 m², 1.33× overall) *understates* the problem, because the error is
**front-loaded onto the dodge band** — worst everywhere the player stands, zero only where he never
is. And the resolver adds `target_radius_m` to the *target*, not the lane, so the shape to draw is
the bare trapezoid.

**Routing: (a) — presentation gap. The taper is what the sim resolves; the trace under-describes it.**

⚑ **And the null-instrument tripwire produced a genuinely informative zero.** `_gd_wave_half_width_m`
— the alias `spatial_engine.py:717` imports — has **1 reference and 0 call-sites**, while the
identical selector shape returns 3 on the unaliased helper and 2 on `wave_hits`. An unused import
that *reads like a dropped taper and isn't one*. The selector proved it could find call sites before
it was allowed to report none. That is the discipline working exactly as designed, on a question
where the wrong answer would have sent this run down a false path.

### ⚑ THE PROBE'S REAL LESSON — I asked about one skill and should have asked about all three

I asked: *does the sim taper the wave?* The answer was yes. But the **question generalizes**, and the
generalized version is much larger:

**For each family, does the drawn shape match the predicate the resolver actually evaluates?**

The census already tells us it may not, in a place that matters more than the wave:

- **NOVA** — §3d lists a **prong corridor half-width of 0.42 m** and a splash radius of 1.5 m. If the
  resolver tests *sixteen 0.84 m corridors* rather than a 12 m disc, then **the gaps between the
  prongs are SAFE**, and every frame we have ever rendered has told the player the opposite. That is
  not a fidelity nicety — it is the difference between "run out" and "stand in a gap," and it is a
  bigger legibility error than the wave's.
- **NOVA distance bands** — ×0.50 / ×1.00 / ×1.40 (R-BR-28, already ruled) belong to the same
  predicate.
- **BLIZZARD** — `hit_radius_m` 1.32 within an 8.0 m scatter: already emitted by cell 1b.

So cell 1d is chartered as the **general** form, not the one-field patch.

### Cell 1d — RESOLVE-TRUTH-1 (gamora, engine): *the telegraph describes the resolver's predicate*

**Scope, bounded hard:** for the three telegraphing families, audit the actual damage-resolution
hit-test and emit exactly the fields required to reconstruct that predicate from the telegraph alone.
Wave: `start_width_m`. Nova: whatever the corridor/splash/band test actually reads. Blizzard: confirm
cell 1b's fields close it. **Nothing outside those three predicates.** Discoveries beyond → BR-3.

⚑ **`shape` must stop lying, and this is the cheapest moment it will ever be.** The wave's `shape`
reads `rect` and the resolver evaluates a trapezoid. We have now found a field carrying the wrong
quantity **four times** — `range_m`, `wind_up_s`, `duration_s`, and now `shape`. **Ship
`shape: "trapezoid"`** unless there is a strong argument against, and make the argument if so. The
only consumer is a renderer being written this week; there will never be a cheaper time to correct
an enum.

**Pre-registered gates:**
- **G-1f — emission purity**, three-limb standard, as cells 1 and 1b. No fifth path.
- **G-1g — coverage as counts**, with null counts and `absent_key` as their own evidence.
- **G-1h — PREDICATE RECONSTRUCTION.** *An independent function that consumes ONLY telegraph fields
  must reproduce hit/no-hit against the trace's own recorded damage events on **100 %** of resolvable
  cases, per family, with the denominator stated.* This is the gate that makes "the telegraph
  describes the resolver" a checkable fact rather than a hope. It is also the strongest gate this run
  has written, and it is the one to fight for.
- **Fallback:** if reconstruction cannot reach 100 %, emit what *is* provable, state the residual
  fraction and its cause, and the renderer draws only the reconstructible part. **A named residual is
  a finding; a rounded-up "verified" is the rubric-law failure that killed KIT-FIDELITY.**

**G-2a and G-2b are amended on landing** to whatever the resolver turns out to test. If the nova's
predicate is corridors, the T-1 target-state changes with it — and that change is a *finding
propagating correctly*, not scope drift, because the intent sentence was always *render the fight the
substrate has been describing*.

Cell 1d runs in the engine, parallel-safe with ARSENAL-2 in godot (same contention rules as 1b/1c).
**Cell 2 opens when 1c and 1d have both landed.**

---

## ADDENDUM 5 — cell 1c landed; five rulings, two disciplines minted (conductor, 2026-08-01)

### Cell 1c — ARSENAL-2: **G-10 PASS, G-12 PASS, G-13 PASS (8/8), G-11 FAIL, G-9 verified**

godot `68d0ca8` · meta `9798aa6a`, both confirmed present on `origin/main`. Landing note:
`drax/notes/2026-08-01-arsenal-2.md`. **27 new effects / 98 new emitters** → harvest now **60
effects / 217 emitters / 23 meshes / 10 textures**, G-10 at **60/60 config · 60/60 pixel** against an
in-run empty-stage control of **0**.

**G-13 — coverage, the gate that outranks accuracy: 8 COVERED / 0 THIN / 0 GAP.** Every one of the
eight material needs has ≥1 gate-passing candidate, most have three or more. The redundancy was not
decoration — need 4 consumed it within the hour (below). Machine-generated from the need→effect
manifest joined against the pixel gate's own JSON, not asserted by hand.

**The 39 refused effects were the answer.** `BarrageNovaIce` (7,538 lit px) and `BarrageRainIce`
(7,148) — the two strongest need-1 candidates — came out of `Barrage/Nova`, the folder R-BR-3 refused
on a false premise. *Nova-shaped barrages of flying projectiles* was a literal description of what we
needed and we had banned reading it. Reversing a bad ruling recovered the run's single most important
material.

### ⚑ G-11 FAIL — and the FAIL is the cell's best work

| effect | static | moving | ratio |
|---|---|---|---|
| `SwordChargeUp` (item D candidate) | 9 | **6** | **×0.67** |
| `SwordTrail` | 207 | **134** | ×0.65 |
| `SwordTrailShadow` | 8 | **9** | ×1.12 |
| non-trail control, n=57 | | | median **×1.073** |

The moving-host hypothesis was **mine** — I reasoned that Unity ribbons look dead on a static stage
because they have nothing to streak along. Two of three went *down* on a moving host; the third sits
on the non-trail median. **The bar was "materially exceeds" and drax did not move it after seeing the
number.** That is the preregistration safety (§5.1) working against the conductor's own hypothesis,
which is the only direction in which it is worth anything.

And the instrument proved it was alive before it was allowed to report a negative: `min peak yaw
69.62° (declared 70.0) · min mount travel 3.385 m`, asserted across all 60 in `_finish` *before* any
verdict may print, with `FlamethrowerSprayBlue` at **×4.56** in the same run showing the treatment
bites. Reproduced bit-for-bit across two full runs. This is the null-instrument tripwire (Scope 40-b)
now independently implemented in a **third** seam.

**Per the declared fallback: `SwordChargeUp` is named unusable, item D sources elsewhere, cell 2
composes from what passed.** No silent substitution.

---

### R-BR-38 — A SUBPROCESS INSTRUMENT MUST ASSERT `returncode == 0` BEFORE ITS OUTPUT MAY BE READ

Drax's own verification probe returned a clean **"0 effects differ."** It was false: the probe's patch
produced a comment inside a call expression, `pa_emit.py` crashed, `capture_output=True` swallowed the
traceback, and nothing checked the return code. A **null instrument built inside the cell that shipped
two tripwires against exactly this.** The corrected probe asserts the return code first and then found
**4**.

Standing law, all seams: **an instrument that shells out has not reported until it has proved the
shell succeeded.** A silent non-zero exit is indistinguishable from a clean negative, and a clean
negative is the most dangerous output any instrument can produce. This is the same organism as
R-BR-34 (*a ruling that cites no evidence is a recollection wearing a ruling's clothes*) — here the
recollection is the shell's, and it is a lie by omission.

### R-BR-39 — THE PIXEL GATE IS A THRESHOLD INSTRUMENT, NOT A MEASUREMENT

`SwordChargeUp` measured **139** lit px in ARSENAL-HARVEST and **16** in both ARSENAL-2 runs, on a
**byte-identical transcription** (`git diff` on `pa_emit.py` shows only the root-translation edit;
the effect is not among the 4 changed scenes). The gate is sound at its PASS bar of ≥500 against a
control of 0. It is **not** reproducible at low counts.

**Therefore: counts below the gate's noise floor may not be compared, ranked, or cited as evidence of
anything except "did not pass."** The 139 never supported a conclusion, and any future finding of the
form "effect A is brighter than effect B" must be at magnitudes the gate can actually resolve. This
retroactively validates the G-11 handling — the ×0.67 was read as *did not pass*, not as *got dimmer
by a third*, which the instrument cannot support.

---

### Rulings on the cell's four escalations (veto-open)

**F-A2-1 — the claw wind-up. RULED: it is two beats, not one choice.**
`ChargeSphereRed` (2,029) is the **wind-up**, mounted per-hand on the claw bones and scaled down;
`MuzzleFireballRed` (4,044) is the **strike flash** at the damage event. Reasoning: a muzzle flash is
a *release* — instantaneous, the wrong temporal grammar for anticipation. A charge sphere accumulates,
holds, releases, which is exactly what a wind-up tell must teach. Under R-BR-35 we take the material
and set our own scale, so "sphere" does not commit us to a caster's orb — two small gathering points
on a beast's hands is the same material at our geometry. `MuzzleSkullRed` is refused: necromantic
iconography on a werewolf is a register error, and it is also the dimmest of the three.
**This is a taste call and it goes to Matt at the cell-2 owner-eye clip** — I am ruling so cell 2 is
not blocked, not so the ruling is final. One word reverses it.

**F-A2-2 — displaced effects passed the pixel gate. ACCEPTED, with a consequence.**
`NovaLife` (0.29 m) and `NovaLightningWave` (1.28 m) shipped displaced in ARSENAL-HARVEST and the
pixel gate passed them, **because the pixel gate asks whether something lit up, not whether it lit up
where it should have.** Fixed in this cell. Two consequences bank: (1) **the register clip Matt
already judged contained the displaced versions** — his verdict on those two effects is void, not
wrong; (2) position is not a harvest-gate question at all, it is a cell-2 question, and **G-2a/G-2b
already measure it** (angular spacing ±0.5°, footprint ±0.3 m, orientation ±3°). The gap closes
downstream by construction. No new gate.

**F-A2-3 — ACCEPTED as amendment, not reversal**, exactly as drax routed it. The original citation
was wrong; the conclusion survives on the new `PolyAura4` evidence (rotation bit-identical to the
prefab root, position unrelated → rotation preserved, position replaced). Correcting the citation
while preserving the conclusion is the right disposition, and volunteering that your own earlier
evidence was wrong when the conclusion still holds is the harder half of the discipline.

**F-A2-5 — NOT an exception. The grammar's domain was mis-stated.**
`polygore_atlas_red.png` at chroma 0.5052 has its colour baked and is not gradient-retintable — and
that is correct, because **the element grammar governs elemental families; gore is not an element.**
Blood is red because blood is red. Nothing to reconcile.

**The `Beams` refusal — UPHELD, and it is the right kind of refusal.** `PolyBeamStaticBlue` and
`BeamBlue` carry **zero ParticleSystems** — LineRenderers driven by C#, nothing our parser can
transcribe. G-12 says an effect that cannot be traced is refused, not faked. Needs 3 and 5 are served
from `Wall` / `Flamethrower` / `Chains` instead, **stated rather than silently substituted**, and
`Orbital Beam` / `Channel` recorded as **UNPROBED** rather than folded into the negative. Recording
the difference between "we looked and it isn't there" and "we did not look" is the whole of honest
coverage.

**Persistent blood pools — the pack has none (0 of 1,597 prefabs), and it does not need to.**
`SurfacePoolSplat` is the mechanism; **persistence is ours, not the pack's** — a decal we keep alive
for the room. That is R-BR-35 read correctly: the pack supplies material, we supply duration. The
hue is our recolour and is declared as the cell's only non-pack tint.

### ⚑ F-BR-6 — THE DANGLING GUID IS CELL 2's FIRST ACT, NOT AN ACCEPTED DEBT

`68d05d7c…` resolves to nothing, leaving **`PolyIce.mat` + `PolyBubbleWater.mat` untextured** — and
those hit needs **1, 2 and 3**, which is to say **the boss's entire signature kit**. Drax named it and
did not measure it, correctly, because measuring it is a render question and this was a harvest cell.

**Ruled: cell 2 opens by rendering one `BarrageNovaIce` at scene scale and judging the untextured
material on frame, before composing anything on top of it.** Untextured may read as acceptable — flat
pale ice is not an absurd look for ice — or it may read as grey plastic. We do not know, and composing
16 prongs and 24 drops on an unmeasured material is how a cell discovers at the watch that its
headline shape looks like a toy. **Fallback if it reads unusable: we author the material ourselves.**
Meshes are the pack's; shaders were never in its gift. `21 of 60 effects lose `SubModule`` (including
both need-1 ice barrages, at 4 each) rides the same measurement.

### §3 cell table amended

| # | Cell | Owner | Repo | State |
|---|---|---|---|---|
| 1 | TRACE-FILL-1 | gamora | engine | **LANDED** — G-1 / G-1b PASS |
| 1b | TRACE-STAGE-1 | gamora | engine | **LANDED** — G-1c / G-1d PASS |
| 1c | ARSENAL-2 | drax | godot | **LANDED** — G-10 / G-12 / G-13 PASS, G-11 FAIL (processed) |
| 1d | RESOLVE-TRUTH-1 | gamora | engine | in flight |
| 2 | VFX-TRUTH-1 | drax | godot | opens on 1d; **first act = F-BR-6 material measurement** |
| 3 | COMBAT-JUICE-1 | drax | godot | |
| 4 | HUD-PORT-1 | drax | godot | |
| 5 | BR2-WATCH | drax | godot | |

**Banked to BR-3:** the `--headless --import` `[rendering]` strip (third occurrence, guard caught it,
`git diff project.godot` empty — a recurring Godot-CLI behaviour that deserves a permanent fix rather
than a permanent guard), and `Orbital Beam` / `Channel` as unprobed families.

---

## ADDENDUM 6 — cell 1d landed. **THE NOVA IS A STAR.** T-1 and G-2a amend on a finding.
### (conductor, 2026-08-01)

### Cell 1d — RESOLVE-TRUTH-1: **G-1f / G-1g / G-1h PASS, G-9 verified**

Battery of record `~/Games/reincarnated-godot/tmp/wr3acc/traces/`, stamped `16fa7e8d`. Landing note
`gamora/notes/2026-08-01-resolve-truth-1.md`; math note
`reincarnated-engine/…/simulation/math/br2-resolve-truth-1-2026-08-01.md`.

**G-1h — predicate reconstruction — passed at 100 % on all four arms, FP 0 / FN 0.** Nova 470/470 ·
wave 516/516 · blizzard 570/570 telegraphs · **13,680/13,680 individual drops.** The reconstructor
imports nothing from `reincarnated` — asserted, not asserted-about. This was the strongest gate this
run has written and it is now a fact rather than a hope: **a consumer holding only the telegraph record
can reproduce the resolver's own hit/no-hit, on every case, in every family.**

And the gate nearly certified nothing. Its **degenerate-predictor tripwire fired during development**:
a predictor that answers "always miss" scores **48 % / 81 % / 98.6 %** on the three families and
*reads like a pass*. A reconstruction gate without a degenerate control measures class imbalance and
calls it fidelity — the KIT-FIDELITY failure in a new costume. It was caught by the instrument's own
design.

G-1f held the three-limb standard a third time: control arm at `28eddef4`, 90,708 records, the only
moving field `engine_git_hash`, reconciled to an intervening commit touching `AGENT_STATE.md` alone.
Post-change: **exactly seven simulation paths**, six new fields at n=1,556 and `shape` at **n=986 =
470 nova + 516 wave, blizzard's 570 deliberately untouched.** No eighth path. The instrument also
grades fields that *failed to move* — the `family`-died-at-the-seam mode — and found zero.

---

### ⚑⚑ THE FINDING: 48.5 % OF THE NOVA'S CROSSINGS DEALT ZERO DAMAGE, AND EVERY ONE WAS A GAP

`gd_nova.py:666` (`n_realized`, gated at `spatial_engine.py:6559`) tests **sixteen 0.84 m lanes.
Not a 12 m disc.**

- **226 of 466 resolved crossings — 48.5 % — dealt zero damage. Not one was out of range.**
- Gapless only inside **2.1528 m**. At r = 9 m, **76.2 % of bearings are safe.**
- The disc we have been drawing is **3.076× the lethal area** of the thing that actually kills.
- The 1.5 m splash is **predicate-dead** — it exists and does nothing. (Null-instrument control:
  the same selector found 3 live sites on `hit_half_width` before being allowed to report zero.)

**Sit with what that means for the player, because it is worse than a fidelity error.** Half the time
the nova swept over him, it did nothing — and the screen showed a solid disc of fire passing through
his body. From inside the fight, the nova is a hazard that *sometimes hurts and sometimes doesn't,
for no visible reason.* That is not difficulty. That is **noise**, and noise is the one thing an ARPG
floor must never be: the entire genre from Diablo II's Blood Moor to PoE's degen-carpets rests on the
covenant that **the floor tells the truth about the floor.** We broke that covenant in the boss's
signature ability and then measured 48.5 % of it as unexplained variance.

**And the mechanic underneath is better than the one we thought we had.** A 12 m expanding disc is a
pure reaction test — see it, run out, no decision. Sixteen phased lanes with `spoke_offset_rad`
rotating the gaps *between casts* is a **read-and-step** mechanic: you cannot camp a bearing, you must
re-read the floor each cast. That is the good version, the Diablo-lineage floor-literacy that
separates a player who survives from a player who reacts. **The simulation has been playing a better
game than the renderer has been showing for as long as this fight has existed.**

**One tension, named rather than smoothed:** the gapless radius is 2.1528 m and the player's primary
skill is a **2.0 m cone**. Melee range sits *inside* the gapless core. So the nova is, correctly, a
**melee-eviction pull** — it says leave the body, read the star, step a lane, come back. That is a
rhythm, and it is the fight's rhythm; it was invisible.

### R-BR-40 — MATCH ON `family`, NEVER ON `shape`

Gamora's own summary line, promoted to standing law. `shape` is a *drawing hint*; `family` is the
*contract*. Any consumer branching on `shape` breaks the moment an enum is corrected — which has now
happened twice in one cell.

### `shape` — executed, extended, and argued back on. All three accepted.

- **Wave → `trapezoid`.** Agreed, no argument against; **18 false positives in 516 measured** by the
  old rect.
- **Nova → `star`.** Gamora extended my ruling to the family I had not named, and it is the larger
  error of the two.
- **Blizzard keeps `circle` — and this is the part I asked for.** I told gamora to argue rather than
  comply if the ruling was wrong, and on the third family it was: the blizzard's `radius_m`
  *truthfully* names its scatter disc and its primitive genuinely **is** a circle test. The defect
  there is **cardinality** — one telegraph record standing for 24 instances — not shape. Correctly
  decomposed, correctly routed to BR-3 as multi-instance enums. A sub-agent that takes two thirds of
  a ruling and refuses the third with a reason is worth more than one that takes all three.

**Self-caught, and worth recording:** `PRIMORDIAN_FRIGIDRING` is the rank-4 pre-stage-2 nova
(`hit_half_width` **1.5**); the shipping ability is `PRIMORDIAN_FRIGIDRING_STAR_R5` (**0.42**).
**3.57× apart, one suffix apart.** The test draft reached for the obvious name and the value pins
caught it. Every near-miss this run has caught has had the same shape: *the obvious reading of a
familiar name.*

---

### AMENDMENTS — findings propagating correctly, not scope drift

The intent sentence was always *render the fight the substrate has been describing.* The substrate
turned out to describe something different from what we pinned, so the pins move to it.

**T-1 item 1 replaced:**
> **Nova** draws **16 discrete lanes at 22.5°**, each **0.84 m wide**, travelling outward at 14.0 m/s
> over 0.857 s, phased per cast by `spoke_offset_rad` — **with the gaps between lanes drawn as
> unambiguously safe beyond 2.15 m** — and its danger shading **inverted per the emitted bands**
> (hub ×0.50, rim ×1.40).

**G-2a re-pinned:**
- 16 lane instances counted; angular spacing 22.5° ± 0.5°; outer extent 12.0 m ± 0.2 m at 0.857 s ±
  0.03 s (unchanged).
- **NEW — lane width:** rendered corridor half-width **0.42 m ± 0.05** at all radii.
- **NEW — and this is the gate that matters: ZERO rendered danger pixels in the gaps beyond 2.15 m.**
  A soft glow bridging the lanes fails this gate. The gaps are the mechanic; anything drawn in them
  re-tells the lie in a prettier font.

**G-4 re-pinned to the emitted fields:** band shading is graded against `band_bounds_m` / `band_scales`
as emitted, not against the remembered 2.5 m step.

**G-2b confirmed:** trapezoid, `start_width_m` 3.0 → `end_width_m` 6.0, `depth_m` 1.0 band, **sweep
timed 1.4 s from range ÷ velocity, never from `duration_s`** (R-BR-36).

**G-2c refined:** 24 discs of 1.32 m at the emitted `impact_points_xy`. **1.36 % of drops hit** —
so the blizzard's threat is **positional pressure, not damage**, and the renderer must therefore make
the *scatter legible* rather than the *impacts dramatic*. Drawing 24 spectacular explosions for a
1.36 % hit rate would teach fear of a floor that is 98.6 % safe — the reverse-falloff error again.

**Banked to BR-3:** the **body-radius asymmetry** (the wave adds the live target's radius; nova and
blizzard bake the referent's 0.32 m in — on a 0.5-radius player, two of three families resolve
against a body **0.18 m too small**); the dead 1.5 m splash (wire it or delete it); multi-instance
shape enums.

**Cell 2 — VFX-TRUTH-1 — is OPEN.**

---

## ADDENDUM 7 — cell 2 landed. The star is drawn true; the ARENA is too small for the kit.
### (conductor, 2026-08-01)

### Cell 2 — VFX-TRUTH-1: **G-2c / G-3 / G-4 PASS · G-2a 4/6 · G-2b FAIL by 0.050 m · G-9 verified**

Landing note `drax/notes/2026-08-01-vfx-truth-1.md`. Clip:
`~/Games/reincarnated-godot/tmp/vfxtruth1/VFXTRUTH1_BEFORE_AFTER.mp4` (36 s, seed 74000909, all three
casts of all three families, before/after). Baseline frame 5 max diff **0** — nothing moved that
wasn't asked to move.

**F-BR-6 — USABLE. No material authored, and the reasoning is better than the verdict.**
`BarrageNovaIce` carries **0 of 5 materials with an albedo texture** and reads as flat pale faceted
ice anyway, because the shader is `Rimlight/Transparent` on **mesh** renderers — silhouette and facets
carry the look, and the crypt's cold ambient tints the white vertex colour for free. Then closed by
the camera's own arithmetic: **at 23.0 px/m a 0.19 m shard subtends 4.3 px.** There is no texture
detail a four-pixel shard could carry. That is the right way to close a material question — not "it
looks fine" but "the pixel budget forbids the difference from existing." The `SubModule` debt rides
the same verdict and dissolves with it.

**The star is drawn true.** Spacing **22.5000° exactly, min = max, 6/6 phases.** Extent 12.0000 /
12.0000 / 11.9500 m against ±0.2. Corridor half-width **0.4080** (min 0.3850, max 0.4300) against
0.42 ±0.05. **And on the only cast whose star fits inside the arena, the gaps are clean: 0 danger
pixels of 2,945 and 0 of 2,998.** The mechanic nobody has ever seen is on frame.

**G-4 PASS — the reverse falloff is dead.** Band luma **104.29 → 121.06 → 134.59**, monotonically
brightening centre→rim. The nova now tells the player the rim is the dangerous part, which it always
was.

---

### ⚑ G-2a's FAIL is unresolved, and I am not going to guess it away

**31 of 2,564 and 43 of 2,684 danger pixels in classified gaps on nova #1, all at the boss's own
capsule base — and drax did not widen the exclusion pad to sweep them.** That refusal is the whole
value of the gate. Moving a pad to clear a FAIL is goalpost movement wearing a bug-fix's clothes.

The verdict turns on **one number I do not have**: the radius of those pixels.
- If **r < 2.1528 m** they are inside the gapless core, where the lanes genuinely merge — they are
  **TRUE danger**, and the gate's gap-classifier is missing a radius qualifier. The render is right
  and the instrument is wrong.
- If **r ≥ 2.1528 m** they are a render defect at the boss capsule and cell 3 fixes them.

**Ruled: cell 3's first act measures it.** Same pattern as F-BR-6 — one cheap measurement before
anything composes on top. I will not rule a gate PASS on the plausible reading of "at the capsule
base."

### ⚑⚑ THE REAL FINDING: G-2b's FAIL AND FINDING #2 ARE THE SAME PHENOMENON

Drax pinned G-2b's cause with a structural argument rather than a tolerance nudge: the trapezoid
measures **5.6498 m at u=16** against 6.000 ±0.3 — a miss of **0.050 m** — because the cut at
u = 15.80 is **one-sided**. The −edge lands exact (−3.00 vs −2.981); the +edge stops at ≈ +2.41.
**A symmetric quad cannot be asymmetrically narrow. The mesh is right; the cut is occluded.**
Leave-one-out recovers 2.9724 → 5.9825, printed as *diagnosis, not verdict* — which is the correct
epistemic placement and the discipline this run has been demanding all week.

**What occludes it is the east wall.** Finding #2: a 16 m wave from (32.10, 8.08) ends at
**(44.4, 18.1) in a 36 m room**, and two of three novas put a 12 m star through the east wall.

So: **the boss's kit is authored for a larger arena than the one we fight in** — or, more precisely
and more cheaply, **the boss is fighting in a corner.** A 12 m nova and a 16 m wave are unremarkable
in a 36 m room *if the fight happens near its centre*. At (32.10, 8.08) the boss is pinned against a
wall, so a large fraction of every telegraph's area lands where no one can stand. The ability scale
is not the defect. **The fighting position is.**

**Ruled for BR-2: draw it truthfully, do not clip.** Clipping a decal at a wall would require the
renderer to carry the arena's collision — a new dependency, in service of hiding a real mismatch. The
danger genuinely does extend there; there is simply nowhere to stand. Honest and slightly absurd beats
tidy and false.

**Ruled OUT of BR-2, and it is a commitment-boundary, not a preference:** moving the fight position
touches CAM-LOCK, which §5 reserves to Matt. **Banked as the headline BR-3 finding.** It is also the
first finding of this run that is neither a presentation gap nor an emission gap — it is an
**encounter-space** question, and it is the interesting kind.

**G-2b's residual disposition:** re-measure on a cast whose lane fits the room, applying the exact
discipline drax used for the nova ("the only cast whose star fits the arena"). Cell 3's second act.
Until then G-2b stands **FAILED with cause pinned** — a named residual is a finding; a rounded-up
"verified" is the rubric-law failure that killed KIT-FIDELITY.

### R-BR-40 was violated by our own existing code, and it broke exactly as predicted

`_ps_tg_verdict` **branched on `shape`**. Cell 1d's enum correction broke it (it printed `?` on the
nova) — and *before* that break it had been **over-claiming 3.076×**. Fixed in-cell. Drax's
instruction stands and is promoted to a gate:

**G-3b — the `shape`-branch audit.** Every remaining consumer of telegraph records is grepped for
`shape`-branching; the count is **zero**, or each survivor is justified in writing. R-BR-40 is a law
whose first violation was already in the tree when it was written.

### Standing riders for cell 3 (from cell 2's own findings)

- **Fog inverted the danger grade** until `fog_disabled`. Anything cell 3 adds to the marker layer
  needs the same treatment, and needs it verified rather than assumed.
- **`Werewolf (player)` is wired and drawn NOWHERE** — 34 on-screen strings censused. That is a
  cell-4 (HUD-PORT) item and it is now a named requirement, not a discovery waiting to happen.

### §3 cell table

| # | Cell | Owner | State |
|---|---|---|---|
| 1 · 1b · 1c · 1d | TRACE-FILL · TRACE-STAGE · ARSENAL-2 · RESOLVE-TRUTH | gamora / drax | **LANDED** |
| 2 | VFX-TRUTH-1 | drax | **LANDED** — G-2c/G-3/G-4 PASS, G-2a 4/6, G-2b FAIL cause-pinned |
| 3 | COMBAT-JUICE-1 | drax | **OPEN** — opens with the two residual measurements |
| 4 | HUD-PORT-1 | drax | |
| 5 | BR2-WATCH | drax | |

**Owner-eye checkpoint fired:** the cell-2 clip goes to Matt. The run does not halt for it.

---

## ADDENDUM 8 — the cell-2 owner-eye checkpoint fired. Matt ruled 3 changes; one REVERSES me.
### (conductor, 2026-08-01)

**Matt, on `VFXTRUTH1_BEFORE_AFTER.mp4`:** *"VFX truth is looking good, only a couple of changes:
(1) the telegraph ground fields should not pass through the walls (happens with one new conical
zone). (2) Is the consistently appearing circle around the boss just its wind up for its swings? If
so, we can remove that entirely as we can see the swings and the words wind up. (3) We need to make
the telegraph zones much more translucent and use textures/colors to match to the actual VFX skills
they're casting."*

**This is §6 obs 2 paying for itself.** The owner-eye checkpoint was pre-registered as a mid-run gate
precisely so his eye would land before downstream cells built on unviewed state. It landed, it caught
three things, and one of them overturns a ruling I made **in the previous addendum**. That is the
checkpoint working, not the run faltering.

### R-BR-41 — TELEGRAPH FIELDS CLIP AT THE ARENA BOUNDS. **My Addendum-7 ruling is REVERSED.**

I ruled, one addendum ago: *"draw it truthfully, do not clip… honest and slightly absurd beats tidy
and false."* **Matt vetoed it, and he is right — I weighed the wrong two things against each other.**

My argument was information-preservation: the danger genuinely does extend past the wall, so drawing
it is truthful. But **no information is lost by clipping, because no actor can ever stand there** —
the clipped region is empty of consequence by construction. So the trade I framed as truth-vs-tidiness
was never that. It was truth-vs-**nothing**, against a real cost on the other side:

**A danger field crossing a solid wall teaches the player that the wall is not real.** Walls are the
one class of object in an arena that a player must be able to trust absolutely — they are the
substrate of every positional decision he makes. An effect that visibly ignores one says *geometry
here is decorative*, and that lesson contaminates every future read of the room, not just this cast.
I optimised a local truth and paid for it with the room's global credibility.

**Implementation note (cheapest honest route):** this does **not** require the renderer to carry
arbitrary collision — which was my stated objection and was also wrong. The arena is a known
rectangular extent; clip the decal to the **floor mesh footprint**, not to scene collision. Matt names
*"one new conical zone"* — that is the wave's trapezoid, the widest overrunner.

### R-BR-42 — IDENTIFY THE RING BEFORE REMOVING IT (and it may already be measured)

Matt: *"the consistently appearing circle around the boss."* His removal reasoning is sound on its own
terms — the swing animation and the on-screen wind-up text already carry the tell, and a third channel
saying the same thing is clutter, not redundancy.

**But I will not remove a ring I have not identified**, because one of the candidates is
**load-bearing**: the nova's **gapless hub** (r < 2.1528 m, where the sixteen lanes genuinely merge)
is TRUE danger and is the exact thing this run just spent four cells surfacing. Deleting it would
re-break what cell 2 fixed. The other candidates — a melee wind-up decal, or a leftover full-disc from
the pre-star rendering — are clutter and go.

⚑ **Discriminator, from the frequency Matt himself observed:** *"consistently appearing."* The nova
fires **three times** in seed 74000909. Consistent appearance is basic-attack cadence, not nova
cadence. That points hard at a melee wind-up decal — but it is a *point*, not a measurement, and
R-BR-34 says a ruling that names no evidence is a recollection wearing a ruling's clothes.

⚑ **And it may already be under the instrument.** Cell 3's §0(A) is measuring the **radius** of
G-2a's 31 and 43 failing pixels, which drax located *"at the boss's own capsule base."* If that ring
is a melee decal bleeding into the nova's gap classification, then **the same measurement identifies
the ring AND closes G-2a at 6/6, and removing the ring fixes the gate for free.** Two open items
collapsing into one measurement is worth waiting one cell for.

### R-BR-43 — TELEGRAPHS DRESS AS THEIR ABILITY, WITH A LEGIBILITY FLOOR

Matt's item 3 is the most substantial of the three and it is a genre-level call, so it gets a
genre-level answer.

**The convention he is rejecting is the Diablo III / Lost Ark generic red zone** — one danger palette
for every ability, maximally legible and completely flat. It reads as **UI painted on the floor**
rather than as something happening in the world. The convention he is asking for is Diablo IV's:
telegraphs share material language with the ability that casts them, so Lilith's ground-tells are made
of the same stuff as Lilith. All three of our boss abilities are **ice**. The telegraph palette
therefore goes cold — pale blue, white, frost — sampled from the materials we already harvested
(`PolyIce.mat`, `BarrageNovaIce`, `ExplosionIceBig`). **R-BR-35 extended to decals: the pack supplies
the material, the trace supplies the geometry.**

⚑ **The floor this ruling must not fall through — and it is a real risk, not a caveat.** Danger reads
as danger because of **hard edges and motion**, not because of fill opacity. Drop the fill too far and
we lose the gap contrast that G-2a exists to protect — the sixteen lanes only teach *read-and-step*
if lane and gap are distinguishable. **So: fill opacity drops, rim/edge definition does NOT.**

That constraint composes *favourably* with what cell 2 already landed. G-4 grades the bands
**brightening outward** (104.29 → 121.06 → 134.59), so the contrast already lives at the rim.
Reducing fill while holding the rim **strengthens** the reverse-falloff read rather than fighting it.
The three changes reinforce; they do not trade off.

**New gate, G-4b — the legibility floor:** after re-dressing, the measured lane-vs-gap contrast in the
nova's outer band is **≥ 80 %** of its cell-2 value, and G-2a's zero-pixels-in-gaps result still
holds. Translucency that costs us the gaps is a FAIL, and it is the one way item 3 could go wrong.

### Cell 2b — TELL-DRESS-1 — QUEUED, not fired

Items 1–3 are cell-2 territory reopened by a Matt veto, which §5 pre-declares as *"a processable
finding that reopens the named cell."* **Cell 3 (COMBAT-JUICE-1) is in flight in the godot tree and
will not be interrupted** — single-writer holds, and mid-cell scope injection is the r1-stall failure
mode. Cell 2b fires the moment cell 3 lands, carrying R-BR-41, R-BR-42, R-BR-43 and gate G-4b.

### The encounter-space question, answered to Matt (not ruled — his call)

*"How do you want to change the room/size? I'm not following."* — put to him as options with costs
in the session reply. **The BR-2 position is unchanged and unaffected by his answer:** clip the
decals (R-BR-41) and render where the sim says. Repositioning touches CAM-LOCK and is his.

### §3 cell table

| # | Cell | Owner | State |
|---|---|---|---|
| 1 · 1b · 1c · 1d · 2 | fill · stage · arsenal · resolve · vfx-truth | gamora / drax | **LANDED** |
| 3 | COMBAT-JUICE-1 | drax | **IN FLIGHT** |
| **2b** | **TELL-DRESS-1** | **drax** | **QUEUED — fires on cell 3's landing** |
| 4 | HUD-PORT-1 | drax | |
| 5 | BR2-WATCH | drax | |
