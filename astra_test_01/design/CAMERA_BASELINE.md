# Godot camera evidence and proposed next-suite baseline

Recorded: 2026-09-10. Read-only investigation of existing Godot code, run logs,
Gandalf/Galadriel notes, and the three videos supplied by Matt.

Status: recovered settings and a recommendation for the new test suite. No Godot
settings or canonical camera decisions were changed. The August camera has prior
owner approval for the named SB-1/VFX work; a new scene still needs visual review.

**Subsequent user clarification, 2026-09-10:** treat every recovered 3D setting
as a starting candidate only. Compare native Diablo II, PoE1, Grim Dawn and Last
Epoch footage before selecting a projection for painted 2D assets on a painted
2D floor. The recommendation below is historical advice, not an adopted camera
lock for the new suite. Current plan: [START_HERE](START_HERE.md).

## Recovered candidate profile: player_lock, k = 0.665

This is the camera used by both supplied whirlwind videos. Gandalf's
[August 16 handoff](../../agentic_orchestration/gandalf/notes/2026-08-16-sb1-session-handoff.md)
records both the still and motion approval gates as complete, with the camera
then labelled PROVISIONAL-CANON pending run-close writes. The
[August 25 VFX-depth charter](../../agentic_orchestration/gandalf/notes/2026-08-25-vfx-depth-run-charter.md)
explicitly requires this camera for judging and the Cathedral as its standard
venue (R-15).

| Property | Recovered value |
|---|---|
| Projection | Perspective/pinhole |
| Downward pitch | 52.95354112560294 degrees |
| World yaw | 47 degrees |
| Roll | Zero |
| Vertical FOV | 31.78610183061007 degrees |
| FOV policy | `Camera3D.KEEP_HEIGHT` |
| Reference aspect | 16:9 |
| Baseline review resolution | 1920 x 1080 |
| Dolly multiplier | `k = 0.665` |
| Camera minus player-ground position | `(9.7929267883301, 18.8840122222900, 9.1654367446899)` m |
| Camera-to-player-ground distance | 23.1627407073975 m |
| Camera height above player ground | 18.8840122222900 m |
| Player-ground screen anchor, measured | `(0.501041450500488, 0.550925123426649)` of viewport |
| Anchor at 1080p, rounded | `(962, 595)` px; 55 px below screen centre |
| Following | Fixed offset and orientation, following the rendered player-ground position; no easing/deadzone in this profile |

Implementation sources:

- [Camera constants and provenance](/Users/admin/Games/reincarnated-godot/scripts/kc2_cpb_clip.gd:281).
- [WW7 capture runner](/Users/admin/Games/reincarnated-godot/scripts/run_ww7_gate2_clip.sh:9).
- [Cathedral capture log](/Users/admin/Games/reincarnated-godot/harness_logs/kc2_2026-08-25-w2b-acath/render.txt).
- [Original player-lock construction and following rules](/Users/admin/Games/reincarnated-godot/scripts/wr2_playback.gd:1720).

The multiplier scales the full offset vector. It does not change the FOV or
rotation. Preserve the basis and ground anchor; aiming a camera directly at the
player's feet would centre the feet and lose the recorded composition.
Pitch is stated here as positive downward elevation; do not paste that sign
blindly into an Euler rotation field. Port the existing construction and verify
the projected anchor.

The capture code explicitly sets a 600 m far clip; that is a harness property,
not a recommended universal performance setting. Near clipping was not explicitly
set in the inspected camera constructor. The next profile should record actual
runtime near/far planes instead of inheriting undocumented defaults.

## Other cameras that must not be confused with this profile

### The supplied ice-golem fight: player_lock at k = 1

`/Users/admin/Desktop/level-18-ice-golem-simulation.mp4` is byte-identical to
`/Users/admin/Games/reincarnated-godot/tmp/br2watch/BR2W.mp4`.
Its stored [camera audit](/Users/admin/Games/reincarnated-godot/tmp/br2watch/m6/pl_audit.json)
records the same pitch, yaw, vertical FOV and ground anchor, with the unscaled
offset `(14.7262048721313, 28.3970108032227, 13.7826108932495)` m.
Stand-off is 34.8311882019043 m; height is 28.3970108032227 m.

The whirlwind camera closes this distance to 66.5% while retaining the lens and
angle. Apparent character-size differences between these videos cannot be
attributed entirely to the camera: the bodies, poses and equipment also differ.

The August 16 handoff records an unresolved mismatch between the WR2 werewolf's
reported body dimensions and measured silhouette. It separately validates the
arena camera with a known-height probe. Treat the ice-golem video as an identified
visual reference; do not use its old body-height label as a calibration standard.

### July Camera B-prime: a separate, still-present play-shell profile

The [game tracker](../../canonical/current-to-end-state/current-to-end-state-game.md)
and [play-shell constants](/Users/admin/Games/reincarnated-godot/scripts/playshell.gd:46)
record FOV 40 degrees, pitch -55 degrees, yaw 47 degrees and distance 20 m.
That rig aims 1.2 m above the floor with a 1 m ground-forward lead. Its reported
8.02% hero height belongs to the 2.123 m King fixture.

This is a different lens, target and fixture. A search finding "20 m" in canon
does not establish the camera in the supplied August clips. Keep both profiles
named until a deliberate production reconciliation is made.

### The original painted ASTRA test

The [original brief](../../codex-3d-modeling/ASTRA%20TEST%2001%20painted%20character%20vfx.md)
specifies roughly 45-degree elevation and a 2:1 dimetric ground grid, with
512 x 512 cells, a `(256, 400)` asset pivot and approximately 240 px standing
height in the south-facing idle.

That is a different authoring description from the Godot perspective profile.
Do not silently replace it or relabel old test results. The next suite should
version its Godot-aligned camera contract separately. Asset-cell pivot and
on-screen player anchor are different coordinate systems and both are needed.

## Verified video identities and inspection scope

Stream metadata below was read with ffprobe; hashes were computed from the
supplied files. Encoded frame rate is not a live performance measurement.

| Supplied video | Dimensions | FPS | Frames | Duration |
|---|---:|---:|---:|---:|
| Cathedral whirlwind, `acath-hitl-ww-plk0665-60fps-1920x1080.mp4` | 1920 x 1080 | 60 | 210 | 3.500 s |
| Desktop `ww7-gate2-cadence-ab-plk0665-1920x1080.mp4` | 1920 x 1080 | 30 | 658 | 21.933 s |
| Desktop `level-18-ice-golem-simulation.mp4` | 1600 x 900 | 30 | 1211 | 40.367 s |

SHA-256:

```text
Cathedral: 5a5e1514e02750e31ffd376aad6ffa6bedc465c026644777df60564c1883263f
WW7:       7e9764e3fc53096128ef6b64d2a624962c1f3df599ae5e4aaf311347c0b828ca
Ice golem: ea61b0ee3469d8e03cca0f6b23e3dda6411c147b56e522bdb53469f072d981ba
```

The Desktop WW7 also matches the archived August 16 gate-2 clip byte-for-byte.
The Cathedral hash matches its capture log. Frames visually inspected in this
review: Cathedral at 0.5/2.5 s; WW7 at 3/16 s; ice golem at 5/30 s.
This was sampled-frame inspection, not a complete animation-quality review.

The samples demonstrate useful test conditions: whirlwind trails and smoke over
both neutral and strongly coloured floors, and a boss fight with large ground
effects, overlapping actors and substantial HUD coverage. The Cathedral's warm
light and coloured shadows are an existing style candidate. These clips do not
establish one shared lighting setup: the neutral arena and Cathedral visibly
differ. Lighting remains a separate art-direction decision.

## How this should shape the new architecture

1. **Use the approved whirlwind profile as the initial shared viewing condition.**
   Show all four factions in that same view, at the same world scale. Keep a
   separate close-up for face/hair and gear inspection. The
   [newer playable-build spec](../../agentic_orchestration/gandalf/notes/2026-08-25-kc2-mc-w4-godot-runtime-spec.md)
   explicitly requires fresh camera review after scale/assembly (R-9); prior
   approval is a starting point, not an automatic pass for the new content.
2. **Make projection testable before generating a roster.** Record projection,
   basis, offset, ground anchor, viewport, world units, near/far planes and
   following policy in a versioned profile. Check a known-height mannequin and
   ground-distance markers through the actual render camera. Disable optional
   camera shake in this calibration pass and test it separately.
3. **Judge identity at gameplay size.** The existing 2 m calibration probe at
   k=0.665 measured about 102.5 px high at 1080p; the handoff's approximately
   10.133% fighter height is a projection for that fixture, not a universal
   character-height requirement. Body, weapon, hair/gear and VFX bounds must be
   measured separately. Preserve intended stature differences across characters.
4. **Give painted assets an explicit projection strategy.** A single 2:1 grid
   cannot reproduce a perspective scale field. If we use directional sprites
   in the 3D scene, qualify their source view, runtime size, depth/occlusion,
   contacts and attachments at centre and near/far screen positions. Uniform
   sprite scaling alone cannot correct every perspective/view-direction change.
   Do not assume an enlarged sprite-sheet preview proves gameplay readability.
5. **Test VFX in their actual spatial layer.** Ground circles lie on the ground;
   weapon trails follow sockets; vertical effects retain height; camera-facing
   particles use an explicit billboard policy. Test depth sorting, footprint,
   onset/release, character visibility and HUD overlap under the same camera.
   Keep presentation scale out of damage/range calculations.
6. **Separate camera and style experiments.** Begin with the named camera held
   fixed while comparing faction art and lighting. Make later camera changes
   explicit variants and rerun affected scale/readability checks. Use Cathedral
   as an existing integration venue plus a neutral diagnostic venue; select the
   final shared lighting response through the planned faction boards and scene.

Measurement provenance: [GAL-CAM report](../../agentic_orchestration/galadriel/notes/2026-07-30-gal-cam-fixture-camera.md).
Its source-game pitch estimate was assumption-dependent, with a broad uncertainty
band; yaw 47 degrees was a project choice. The many decimal places above are
exact reproducibility operands in our Godot implementation, not a claim of
equivalent accuracy in recovering Grim Dawn's original camera.
