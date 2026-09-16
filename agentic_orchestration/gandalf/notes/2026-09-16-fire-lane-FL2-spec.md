# Fire lane — FL-2 spec: the "other rounds" on the fire bolt (light · particles · shader) — DRAFT v0.1

> gandalf (SPEC-AUTHOR), 2026-09-16. Matt ruled the pivot: *"go ahead with the pivot to full fire lane until completed with fire."* DONE list in Q80 § Fire lane. This is round 2 of that list — item (c) — authored against the kit as it stands (`fire_bolt_e1_B` → impact `fire_burst_e0p_v2`, template `burst_v2`). Numbers marked ⚑ are to be set from the FL-1 8-direction sheets (PACK v31) before the brief is cut; everything else is the design.

## What exists (kit + runtime, read 2026-09-16)
- Layers on both kits: `flash` (2 frames, α .8, 1.04→1.0) · `glow` (α .2, ×1.02) · `floor_light` (120 px, 0.15 s, linear fade) · `dark_duplicate` ON (ruled) · `victim_tint` · `hit_stop` · `contact_label` (enabled_layers).
- Travel: P01 head (1.2 BH) + P02 streak (2.0 BH), `tail_s` .15, rest hold 3 f. Cast: "flash + halo (runtime)" — `CastHalo` = head × 1.15.
- Burst: 11 shards, hold 2 f, 1400 px/s, residue .6 s at 20 % (ember heart), `erode_noise` .4 outside-in, key states expanded@19 / spent@40, palette maroon → red → orange → cream.
- No ember motes anywhere yet (the "living embers" tests cover the glow sampling, not particles). No trail. Floor light is a flat disc with a linear fade.

## The round (five moves, each a named kit/spec field so a TOOLING burst can build it without inference)
1. **Cast half** — at release: the existing flash+halo, plus a **muzzle puff**: P01 head at 0.45 scale, 4 frames, α 1→0, at the socket, oriented along the aim; a **caster floor light** 0.8 BH for 6 frames at α .5. Fields: `cast.muzzle_puff {scale .45, frames 4}`, `cast.floor_light {radius_bh .8, frames 6, alpha .5}`.
2. **Flight** — **head flicker**: palette band 3 ↔ 2 swap every 2 frames on the head only (`travel.flicker_frames 2`); **ember trail**: 5 motes/s shed from the head's rear socket, 3–4 px, band 2, life .35 s, drift up 30 px/s + lateral noise ±10 px, additive (`travel.trail {rate_per_s 5, size_px [3,4], life_s .35, rise_px_s 30}`); streak tail `erode_noise` .3 (currently 0).
3. **Contact** — floor light: radius 1.2 BH ⚑, **0.35 s with an ease-out curve** (not linear), tinted band 2 at α .6 (`floor_light {radius_px ⚑, duration_s .35, curve ease_out, tint palette_2}`); flash stays 2 frames; `hit_stop` 3 frames (verify present) ; camera shake 2 px / 6 frames ⚑ (exists in the world script — confirm amplitude on phone).
4. **Burst residue — living embers**: 8–12 motes rising from the residue heart for the residue's life (.6 s → **.8 s**), band 2/3, size 3–5 px, life .5–.9 s, rise 40 px/s with noise, additive, fading; `pieces.residue_s .8`, `pieces.embers {count [8,12], size_px [3,5], life_s [.5,.9], rise_px_s 40}`.
5. **Palette / shader** — keep the four bands (the cream flare reads right on sand); add a **heat halo** on the burst peak only: the existing `glow` at α .35 ×1.06 for the 4 expanded-hold frames (`glow.peak {alpha .35, scale 1.06}`). No new shader; `erode_noise` continuous noise texture as T4h.

## Acceptance shape (for the brief)
Headless: mote counts and lifetimes traced; floor-light alpha curve sampled at 0/.1/.2/.35 s; all 16 other kits byte-identical; the two fire kits validate; suite green on the named tests. Rendered (conductor): PACK v32 → 8-direction sheets (FL-1 chain re-run) → phone (web12, Matt's word). Matt's eye = the gate (DONE (f)).

## Not in this round
Sound (out of scope for the run); directional shadows; the "cast half" animation on the Keeper (cells are C-3's); any change to burst_v2's motion (Matt: "motion is right, size is right").
