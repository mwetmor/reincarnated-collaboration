# RT-5 pre-flight — does the Binbun `beam_vfx` pack still load?

**Author:** drax · **Date:** 2026-08-24 · **Status:** COMPLETE
**Gates:** Step-2 build wave T-A rows `beam_channel` (§ 3.1.14), `line` (§ 3.1.10), `placed_lane` (§ 3.1.20)
**Constraint under test:** C-7 — `agentic_orchestration/drax/notes/2026-08-23-metal-vfx-smoke-probe.md` § 7.7, binding via sealed spec § 2.3
**Instrument:** `~/Games/reincarnated-godot/scripts/rt5_beam_uid_probe.gd` (headless load + instantiate, not file-existence)

`Round-trip: none — no cross-seam contract change.`

---

## 0 · Verdict

**`LOADS`** — for everything the three gated rows consume.

**18 of 19 scenes in the pack load AND instantiate clean.** That is all 8 `beam_vfx_0*`,
all 8 `laser_vfx_0*`, `blast_vfx_01`, and `base_beam_vfx` — every consumable effect asset
in the pack, 15 nodes each (12 for `blast`), 8/8 `ShaderMaterial`s carrying non-empty
shader code.

**1 scene fails: `beam_vfx_scene.tscn`** — the *vendor showcase/demo scene* at the pack
root (Environment + DirectionalLight + WorldEnvironment + Ground + 4 SpotLights, with all
17 effects laid out for display). It is not an effect asset and no T-A row consumes it.
The break is **pre-existing, not a regression, and not caused by anything in this run** —
see § 3.

**The three rows are CLEAR to schedule.**

## 1 · The instrument, and why file-existence was not it

```
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . \
  --script scripts/rt5_beam_uid_probe.gd
```

Three arms: (1) walk the pack, `ResourceLoader.load()` + `instantiate()` every `.tscn`;
(2) enumerate `ResourceLoader.get_dependencies()` on `beam_vfx_01.tscn` and record, per
dependency, whether the **literal nested path** is on disk, whether the **uid** is in
cache, and whether it **actually resolves**; (3) walk the instantiated tree and confirm
the `ShaderMaterial`s hold real shader code rather than silent empty stubs.

**Non-mutating, verified.** `.godot/uid_cache.bin` sha256 was
`ad997640861929adcac7ce512fbf2f7830b3f57bb4355375c76b826343284322` before the probe and
byte-identical after. No UID-cache rebuild was performed — that is the exact operation
C-7 warns against. Nothing under `Assets/` was written.

## 2 · C-7 did not bite — and the mechanism it names is not the one that is live

C-7 states the pack "loads **only** because Godot resolves the `uid://` first" and that
"a UID-cache rebuild would break the beam pack." Arm 2 measured this directly:

| dependency of `beam_vfx_01.tscn` | literal path on disk | uid in cache | resolves |
|---|---|---|---|
| `…/src/script/vfx_beam_controller.gd` | true | true | true |
| `…/src/shader/beam_ball.gdshader` | true | true | true |
| `…/src/shader/beam_core.gdshader` | true | true | true |
| `…/src/shader/beam_outer.gdshader` | true | true | true |
| `…/src/shader/beam_flare.gdshader` | true | true | true |
| `…/src/shader/glow_particle.gdshader` | true | true | true |

All six point at the `.gdignore`d nested tree (`res://Assets/Binbun_VFX/assets-5/…`), and
**all six resolve by literal path** — `FileAccess.file_exists()` true, `load()` non-null.
`.gdignore` suppresses the *import scan*; it does not remove the directory from `res://`.
Resource types that need **no import step** — `.gd`, `.gdshader` — therefore load straight
from a `.gdignore`d tree by path, uid or no uid.

**Proposed refinement to C-7 (gandalf owns T-A; § 2.3 is sealed — flagging, not rewriting):**
the uid-rebuild hazard as stated is *overstated* for the 16 effect scenes (their deps are
all import-free types with working literal paths), and it *understates* a different hazard
that is already live: import-**requiring** types referenced by nested-tree path are dead
now, cache intact. That is § 3.

## 3 · The one failure, diagnosed

`beam_vfx_scene.tscn` fails on exactly one of its 18 dependencies:

```
ERROR: Unable to open file: res://.godot/imported/placeholder.png-9e00fca5….s3tc.ctex
ERROR: Failed loading resource: res://Assets/Binbun_VFX/assets-5/BinbunVFX/shared/texture/placeholder.png
ERROR: beam_vfx_scene.tscn:63 - Parse Error: [ext_resource] referenced non-existent resource
```

The other 17 deps are the effect scenes, and they all load. The dead one is a **ground
texture**, and the mechanism is the import step:

| | nested (assets-5) | flat (symlink farm) |
|---|---|---|
| `.png` on disk | yes | yes (→ **assets-14**'s copy) |
| `.import` present | yes (vendor-shipped, Mar 10) | yes (Jul 31) |
| declared uid | `uid://l7d36kr543fa` | `uid://b3abjmsc8ytbq` |
| artifact in `.godot/imported/` | **ABSENT** | present (`.ctex`, `.s3tc.ctex`, `.md5`) |

The nested `.import` is stale metadata naming an artifact that was never produced, because
the tree it lives in is `.gdignore`d and so was never scanned. The scene is the only file
in the pack that references `placeholder.png` at all.

**Not a regression.** The `.gdignore` + symlink-farm layout dates to Jun/Jul; the vendor
`.import` to Mar 10. This has been broken since the symlink refactor. P0-b probed
`beam_vfx_01.tscn` (in the OK column) and never touched the showcase scene — it is
newly-*observed*, not newly-*broken*.

## 4 · Recovery cost — stated, not performed

**Not attempted this session** (`Assets/` is read-only; a fix is a separate authorized
decision). Cost if it is ever wanted:

- **Cheapest, ~1 line:** repoint line 63 of `beam_vfx_scene.tscn` at the flat form
  `res://Assets/BinbunVFX/shared/texture/placeholder.png` (already imported, uid
  `b3abjmsc8ytbq`). Minutes. Requires a write under `Assets/`.
- **Do nothing:** zero cost, zero impact on the build wave. No T-A row consumes a vendor
  showcase scene. **This is my recommendation** — it is a demo scene for a ground plane
  texture, and the effects it showcases all load individually.
- **What NOT to do:** un-`.gdignore` the nested tree to force the import. That re-admits
  ~10 duplicate Binbun package trees to the scan, which is what the `.gdignore` exists to
  prevent, and is the neighbourhood of the UID-cache rebuild C-7 warns against.

## 5 · Scheduling call

| T-A row | spec § | consumes | clear? |
|---|---|---|---|
| `beam_channel` | 3.1.14 | `beam_vfx_01..08` | **CLEAR** — 8/8 load + instantiate |
| `line` | 3.1.10 | `laser_vfx_01..08` | **CLEAR** — 8/8 load + instantiate |
| `placed_lane` | 3.1.20 | beam/laser + `base_beam_vfx` | **CLEAR** — all load + instantiate |

Carry-forward for whoever mints these: C-7's § 7.2 orientation constraint still stands
(beam-class assets are authored along **−Z**; they need an explicit aim-vector→yaw
contract, not a default transform), as does § 7.1 (disable shadow casting on the additive
meshes). Those are unchanged by this pre-flight.

No VFX minting work was started. Pre-flight only.
