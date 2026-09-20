# KC2-PLAY · G-IMG — the first frame (MOCK)

> **Gate:** charter § 6.1 / ledger **KP-3** — Matt's first-image gate. **No Astra/codex burst
> of this run fires until Matt has seen this frame and read the burst plan.**
> **Author:** drax (presentation seam), Wave 1, 2026-09-20. **Nothing pushed.**

## What these two files are

| file | preset | figure | `ppm` |
|---|---|---:|---:|
| `01_G-IMG_mock_ZOOM-GD_1920x1080.png` | **`ZOOM-GD`** (F4 default, 8.02 % figure) | 86.616 px | **75.668** px/m |
| `02_G-IMG_mock_ZOOM-HOUSE_1920x1080.png` | **`ZOOM-HOUSE`** (F4 toggle, 17 % figure) | 183.600 px | **160.394** px/m |

Open them side by side — that pair **is** the F4 toggle, and it is a camera change, not two sets of art.

## How they were made

`make_g_img_mock.py` — PIL composition. **No Astra/codex burst. No Godot launched
(the heavy lock was never taken). No new art minted.** The Keeper is a first-party
cell already on disk (`cliffside_v45/sprites/idle/S/idle_S_00.png`, copied, never moved).

**Every screen dimension is COMPUTED in the script from the spec's own formulae.
None is typed.** The only typed numbers are the constants of record at § 0 of the
script, each with its citation: `alpha` 52.9535411256029° (2D spec § 1.1, GL-10),
`h_fig` 1.9 m (Corrigendum-Forward 1 + KP-0e), the two F4 fractions, the `u` window,
and the Banner's 8.0 m (R-KP-0f).

### Derivation self-check (runs on every invocation; the script exits non-zero on a miss)

```
ppm_gd         derived      75.6684   published     75.668   OK
ppm_house      derived     160.3944   published    160.394   OK
fig_px_gd      derived      86.6160   published     86.616   OK
fig_px_house   derived     183.6000   published    183.600   OK
eor_semi_x_gd  derived     227.0052   published    227.000   OK
eor_semi_y_gd  derived     181.1836   published    181.200   OK
tan_alpha      derived     1.324808   lane-ruled  1.32481   OK   (80.31/60.62)
```

The last row is the § 1.1 free cross-check: the lane's two independently-ruled px/m
figures reproduce `tan α` to five significant figures. The projection law is not being
imposed on the lane — it is the law the lane already draws under.

### Substrate, digest-gated before use (GL-6)

- arena geometry `crucible-arena-geometry-v1.json` — sha256 `68d895d75702…` **verified**
- model pack v3.1 — `pack_digest` **re-derived from the manifest** (`2c7fc61f6a6f…`) per the
  manifest's own `pack_digest_law`, then the member digest for each file read. A mismatch
  aborts; it does not warn.
- `EoR radius_m = 3.0` is read from `model/player_kit.json` (`PRV-BATON-V1`, precedence 0),
  never typed — GL-10.

### The registered `u`

**`u = 0.285` m per native minimap px — the REGISTERED choice, conductor ledger KP-6**
(galadriel's W1 rider folded, 2026-09-20). It is **asserted in-window** at run time against
the window of record **`[0.22277, 0.3663]`** (R-L3-2 / D-W1-1), and both the value and the
window are printed on the frame. The geometry file's own point estimate **0.1981 is EXCLUDED
by that window and is not used** (WARN-8). `u` is read from **one symbol**, so a later pin
move is a one-line change and a camera re-gate — not a re-authoring (§ 1.4).

> **Supersession, recorded rather than silent:** this mock's first cut used the window
> **midpoint** `0.294535`, per the Wave-1 brief. KP-6 supersedes it. The midpoint is kept in
> the script as `U_SUPERSEDED_MIDPOINT` so the change is legible.
>
> ⚠ **Provenance flag for the conductor:** drax received KP-6 in a message **addressed to
> galadriel**, not in a dispatch to this seat. It is acted on because a ruling of record
> governs whoever consumes it — but per the charter's own conflict rule (*"a posture
> communicated to one session is not a posture the wave has"*), **u = 0.285 should be
> ratified against the WAVE**, not only in the seat that received it. Every figure below that
> depends on `u` moves with it.

## What is true on the frame, and what is not

**TRUE (computed):** the EoR ring at the pack's 3.0 m (227.0 × 181.2 px semi-axes at GD);
the Banner aura's 8.0 m radius; the 177-vertex outer ring, 4 islands and 6 green zones,
projected under § 1.1 from the file's own native-px vertices; the two unwalked north arcs
(vertex spans `[0→8]` and `[174→176]`) drawn **dashed and flagged, never smoothed**;
`interpolated_segments == []`; the north-gate landmark **asserted** to render above the
centroid (the script raises if it does not); the zone radii as **labelled upper bounds**.

**DECLARED, NOT DECODED (GL-12) — and the frame says so on its face:**

- **Monster body radii.** v3.1's `model/monsters.json` carries **no** radius / size / body /
  footprint key (31 distinct keys, zero matching). The token footprints are drawn at a
  **placeholder** radius anchored on the 0.62 m figure that appears in 2D spec § 2.1's example
  snapshot. Silhouette **heights** are pure art. → **routed to the conductor**, because
  **R2D-5 requires the token radius asserted against a pack value and v3.1 has none.**
- **The Vanguard Banner's PLACEMENT** (its 8.0 m radius is model-bound) — R-KP-0f.

> ⚑ **Banner magnitude corrected at ledger KP-7 — the frame shows ×1.0319, not ×2.0.**
> Conductor, verbatim: *"the Vanguard Banner is ×1.0319, NOT ×2.0 (`banner_additive=True` is of
> record; +100 % lands on a sheet already carrying +3036 % physical) … the feel case shrinks to
> ≈ 3 % and **drax must not build ×2.0**."* The 8 m radius, MODEL-BOUND status, per-tick /
> no-hysteresis behaviour and the § 4.4 probe row all **stand**; only the multiplier moved.
> The superseded 2.0 is kept in source as `BANNER_MULT_SUPERSEDED` and named **on the frame**,
> so the correction is legible and cannot be quietly re-quoted downstream.
- Silhouette shapes, tints, HUD layout, ground dressing, dressed margin.
- HP / energy figures are the 2D spec § 2.1 snapshot example, not a simulated state.

## The finding the frame makes visible

**At `ZOOM-GD` with the registered `u = 0.285`, the ring is 2.26 × the viewport wide and
4.29 × tall; standing at the arena centroid, no wall is in frame at all.** At `ZOOM-HOUSE`
it is 4.79 × and 9.09 ×. This is the § 1.3 consequence — *the arena does not fit on the
screen, and should not* — arriving larger than the spec's own figures (1.79 × / 3.37 ×,
Corrigendum-Forward 2) because those were computed at the superseded `u = 0.1981`.

Both figures are **printed on the frame by the script, re-derived from the formula at build**,
never copied from this prose — so they move with `u` on their own.

That is why each frame carries an **ARENA OVERVIEW** inset: the whole ring under the **same**
§ 1.1 projection law at a **declared** display scale, with the true `ZOOM-GD` viewport drawn
on it to relative scale. The inset is how the geometry is shown without the main frame lying
about what the camera sees.

## Reproduce

```bash
python3 make_g_img_mock.py     # rewrites both PNGs + receipt.json, ~10 s
```

`receipt.json` records the constants, the derivations, the substrate digests and the
declared-not-decoded list for this composition.

---

*Filed by drax, run KC2-PLAY Wave 1. Nothing under `astra_test_01/burst/` was written —
the Keeper cell was read only. No burst fired. No Godot launched. Nothing pushed.*
