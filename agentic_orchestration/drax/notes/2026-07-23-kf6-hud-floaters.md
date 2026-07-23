# KF-6 — Synty Dark-Fantasy HUD instrument (drax, presentation seam)

**Run:** KIT-FIDELITY (conductor: gandalf, RUN-CONDUCTOR) · **Gate/Lane:** KF-6 (ledgered KFL-15) · **Date:** 2026-07-23
**Repos:** `~/Games/reincarnated-godot` (code + assets) · `~/Games/reincarnated-collaboration` (this report)
**LAW:** commit locally, NEVER push (conductor verifies + pushes). Tree-noise left untouched (project.godot mesh_lod drift, harness_logs/, probe_*, *.uid — all PRE-EXISTING).

---

## Commit SHAs

**Godot (`~/Games/reincarnated-godot`, branch main):**
- `9f130cd` — KF-6 PARTS 2-5 (code): F3 floaters `<amount> (<pct>%)` null-graceful + Synty globes (`replica_hud.gd`) + skill hot-bar + picker-verify harnesses + AGENT_STATE.
- **PART 1 (assets): NO COMMIT — by design.** `/Assets/Synty/` is gitignored per the Synty license rule ("must not share the source files of any Assets outside your team"); NO Synty pack is tracked in the repo (`git ls-files Assets/Synty/…` = empty). The 41 INTERFACE sprites are provisioned on-disk under `Assets/Synty/interface-dark-fantasy-hud/` + imported (`.import` metadata generated headless), exactly like every other Synty pack (polygon-dungeon-pack, etc.). The code commit references them by `res://` path; they resolve locally. This is the established license-compliance posture, not an omission.

**Collab (`~/Games/reincarnated-collaboration`):** this report (commit pending; never pushed).

---

## What I built (per part)

### PART 1 — Synty INTERFACE import (substrate, Matt directive)
Source: `matt_notes_handoff_docs/recent-synty-packs/Source_Sprites/Sprites/DarkFantasy` (+ `Icons_Status`, `Icons_Elements`).
The pack's literal naming is `SPR_DarkFantasy_*` (not the bare `Frame_Orb_*`/`Sigil_*` of the charter inventory — same substrate, Synty's SPR_ prefix). **SELECTIVE** import (41 files, NOT the 2,195) into `Assets/Synty/interface-dark-fantasy-hud/`:
- `globes/` (14): `Frame_Orb_01/02_{Left,Right,Glass,Sheen}`, `Ring_Large_01/02` + `_Background`, `Frame_Ring_Large_01/02`.
- `bars/` (7): `Frame_Bar_05/12` + `_Background`, `Bar_05/08/12` fill strips.
- `hotbar/` (12): `Box_Hotbar_01-04`, `Frame_HotBar_01` + bg, `Frame_Box_Small_01` + bg + mask, `Frame_Diamond_Small_01` + bg, `Greeble_Cross_01`.
- `icons_status/` (4): `Health_01_{Clean,Stroke,Underlay}`, `FortifiedHealth_01_Clean`.
- `icons_elements/` (4): `Air/Earth/Fire/Ice_01_Clean` (the only 4 element families the pack ships).

Godot headless `--import` pass ran → **41 `.png.import` files generated** (metadata landed). Format audit: all RGBA/8-bit; `Ring_Large_01` center alpha=0 (hollow ornate ring), `Ring_Large_01_Background` center alpha=255 (opaque socket disc) → the globe layering (socket → liquid → ring → glass) is byte-verified, not assumed.

### PART 2 — F3 damage floaters (the KF-7-critical instrument)
Modified `_spawn_damage_floater` IN `scripts/replica_playback.gd` (same-scene, no fork). Renders EXACTLY `<amount> (<pct>%)` reading STRAIGHT from the damage-event fields (§8 zero-derivation):
- **`amount`** = the realized per-hit damage float — the pct's numerator (KF-5 math §172). **Switched OFF `delivered` ONTO `amount`** — the prior floater showed `delivered` (HP actually removed, capped), but the KF-5 gauge anchors pct to `amount` (the roll). This is the load-bearing field correction.
- **pct field per side:** DEALT reads `pct` (= `pct_postmit`); RECEIVED (target == player) reads `pct_received`.
- **NULL-GRACEFUL (required feature, not fallback):** pct JSON `null`/absent/non-finite → `(—)`. Thousands-formatted amount always shows.
- **DEALT vs RECEIVED distinct (my presentation call):** DEALT = element-tinted, size 42, floats up-and-out. RECEIVED = red-alarm `Color(1.0,0.42,0.38)`, size 50, leading `◆`, rises higher/faster — Matt reads at a glance who's taking the hit.

**Proven on BOTH frame generations** (harness `check_floater_format.gd`, exact-string assert):
- OLD pre-gauge frames (on disk now): `281,205 (—)` — amount + null-graceful.
- SYNTH gauge-bearing DEALT: `12,500 (87%)` — exact spec format.
- SYNTH RECEIVED null-pct: `◆ 3,400 (—)` — distinct + null-graceful.
When gamora's gauge-bearing re-emission lands, the `(—)` becomes `(87%)` with **ZERO drax code change** (pure data swap — the fields are simply present+non-null on new frames).

### PART 3 — Health globes (KFL-6c)
**FIELD AUDIT (frame v1):** per-entity HP lives on the tick-frame entity record as `hp` (float, live current); roster carries `max_hp`. Damage events also carry `target_hp_after` (redundant cross-check). So the live fill is built from `hp`/`max_hp` with ZERO derivation (a display ratio, not a game computation).
Built in `scripts/replica_hud.gd` — two genre-idiom globes from `Ring_Large_Background` (socket) + color-liquid fill (bottom-up clip) + `Ring_Large` ornate ring + `Frame_Orb_Glass` sheen:
- **Player globe** (bottom-left, blood-red): live current/max, centered `14,795 / 15,130` readout.
- **Mob-aggregate globe** (bottom-right, blue — opposing side, visually distinct): sum of living-mob `hp` / roster mob-hp total.

**NAMED GAP (max-HP fidelity %):** the spec also wants max-HP fidelity vs source-expected HP. **Frame v1 carries NO expected-hp field** — only realized `max_hp`. Shipped the globe with **live fill only**; the fidelity-% overlay is a NAMED GAP for a gamora micro-emission (an `expected_max_hp`/`source_hp` field on the header roster). I never derive it.

### PART 4 — Skill hot-bar (KFL-6d)
**FIELD AUDIT:** frame v1 carries NO distinct skill-use/cast event. BUT a `damage` event carries `skill_idx` — an honest flash-on-use driver (the sim chose this skill for this hit). Built the hot-bar in `replica_hud.gd` from `Box_Hotbar`/`Frame_Box_Small` sigil frames: one slot per player skill (up to 8), element badge from `Icons_Elements` where the skill names one (Air/Fire/Earth/Ice, restrained), slot-number badge, and a glow overlay that **flashes on the DEALT hit's `skill_idx`** (0.35 s ease-out decay).
**NAMED GAP (cooldown/channel state):** a true cooldown/channel-progress ring needs an additive per-tick `skill_cooldowns`/`cast_progress` field the frame doesn't carry. Flash-on-use is honest today; the cooldown fill is a NAMED GAP for an additive field (I do not infer cooldown from damage cadence — that would be derivation).

### PART 5 — Fight-picker verify
**State: WORKING (verified).** The REPLICA-1 "app ends after the second fight" defect does **NOT reproduce**. The runtime `_cycle_fight()` path was already made reload-safe by the KT-4 work (kill()-first FX-tween teardown + `queue_free` (never hard-`.free()`) of in-frame meshes — documented in `_clear_fx`/`_build_entities`). New harness `scripts/check_picker_advance.gd` drives the LIVE scene's `_cycle_fight()` the way `[`/`]` does: **advanced across 7 distinct fights, scene ALIVE = PASS** (headless). No in-seam fix needed. (Headless verification; the original crash bit under Metal — the two Metal captures below cycled/loaded fights and rendered clean, corroborating.)

---

## Exit predicate — MET

| Predicate | Result |
|---|---|
| Headless gated smoke GREEN | **SMOKE COMPLETE + clean-exit, 0 errors, 0 leaks, parse_errors=0** (aura suppressed under `--smoke` per KTL-6 → no DummyShader line, as expected). |
| Fight loads showing floaters dealt+received (null-graceful) | **PASS** — `check_floater_format.gd`: old `(—)` + synth dealt `12,500 (87%)` + received `◆ 3,400 (—)`. |
| Globes fill live | **PASS** — player+mob globes drain live off tick `hp` (visible in both captures). |
| Hot-bar present | **PASS** — 8 Synty sigil slots, element badges, flash-on-use. |
| Picker advances | **PASS** — 7 distinct fights, scene alive. |
| 1-2 Metal frames (floaters+globes+hot-bar over dressed arena) | **CAPTURED** (below). |

## Captures (Metal, 1920x972; aura-bearing visible path carries the 1 documented Binbun DummyShader shutdown line — KTL-6, NOT a leak)

- `user://kf6_hud_v2_tick51.png` — bowazon BLIND burst tick 51: player globe `14,795/15,130` (red), mob globe (blue), 8-slot Synty hot-bar, dealt floater over the mob cluster, dressed dungeon arena (king register).
- `user://kf6_hud_recv_tick40.png` — poison-javazon AWARE tick 40: **dense green dealt floaters** across the mob column (DoT ticks, each `<amount> (—)`), player globe drained to `~2,170/15,130`, mob globe `~8,550`, hot-bar, dressed arena.
- Resolved FS path: `~/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/kf6_hud_v2_tick51.png` (+ `kf6_hud_recv_tick40.png`). (Working copies under `harness_logs/kf6_captures/` are gitignored tree-noise — NOT committed.)

---

## Named gaps (for gamora micro-emissions — I never derive these)

1. **max-HP fidelity %** (Part 3): frame v1 has no `expected_max_hp`/`source_hp` on the header roster. Globe ships live-fill-only; the fidelity overlay lights up when the field arrives.
2. **skill cooldown/channel progress** (Part 4): frame v1 has no per-tick `skill_cooldowns`/`cast_progress`. Hot-bar flashes on `skill_idx` today; the cooldown ring lights up when the field arrives.
3. **`pct_received`** (Part 2): already a gamora-admitted NAMED GAP (mob skills carry no `_composition` until the KF-3 mob-harvest emits per-skill monster compositions). Received floaters render `<amount> (—)` honestly and light up with zero drax change.

## STOP conditions / upstream notes (NOT drax's to fix)

- **gamora BLOCKER (KF-5 report §BLOCKER):** compiled kits emit effect name `flat_damage`, which the resolver ignores (`name=='damage'` only) → realized `amount==0` for compiled kits → the gauge would read `pct≈0%` everywhere for KF-7's compiled fighters. **This is upstream (conductor/gamora rule the disposition — recommendation (A): one-line `kit_compiler.py:541` rename).** My floaters are correct regardless: they render whatever `amount` the frame carries (0, `(—)`, or full). The REPLICA-1 ref frames on disk carry NON-zero `amount` (the gauge reads fine on them) — the zero only affects the not-yet-emitted compiled-kit frames. No drax action; flagged for the conductor.

## Reproduce

```
BIN=/Applications/Godot.app/Contents/MacOS/Godot; cd ~/Games/reincarnated-godot
$BIN --headless --path . scenes/replica_playback.tscn --quit-after 4000 -- --smoke     # SMOKE COMPLETE + clean-exit
$BIN --headless --path . --script scripts/check_floater_format.gd                       # floater VERDICT: PASS
$BIN --headless --path . --script scripts/check_picker_advance.gd                        # picker RESULT: PASS
$BIN --path . scenes/replica_playback.tscn -- --capture --capture-tick 51 --capture-prefix kf6   # Metal capture
```
