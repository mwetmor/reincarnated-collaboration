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
