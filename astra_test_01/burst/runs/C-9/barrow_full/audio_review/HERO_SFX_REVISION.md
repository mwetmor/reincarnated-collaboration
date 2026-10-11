# Barrow hero SFX and web repair — 2026-10-11

Latest War Cry/Might choices and web fidelity bounds: `ELEVENLABS_WEB_REVISION.md`.
The release evidence below records the earlier revision.

The earlier release left four rejected hero cues on their baseline. That omission
is corrected in the local scene, Windows payload and web export. This is drax
presentation work; no delegation/fallback, engine or sealed runtime edits.

## Listening revisions

- Charge: deep weapon-air sweep with restrained metal contact.
- Potion: bottle opening/handling rather than a magical healing cast.
- Might: a lowered magical power-rise candidate.
- Battle Cry: the closest recorded male voice lowered to 63% pitch (~8 semitones)
  and shortened. The vocal performance still needs Matt's listening verdict.
- Whirlwind: eight identical heavy air passes in 3.36 seconds (0.42-second
  spacing), at 70% speed/pitch. Actual monster contacts supply the selected
  mace impacts; the continuous loop no longer alternates fixed metal strikes.
- Haste: Matt's selected Dash02 remains unchanged. Approved monster cues remain.

These are implemented candidates, not inferred artistic approvals. Original
handoff notes and demo files remain unchanged. Only the two poison find-more cues
retain baseline candidates. Fjordstormen retains the requested +8 dB increase
(-20 dB ready / -24 dB combat); score levels are unchanged.

Self-contained listening page: `derived_sfx/HERO_SFX_REVIEW.html` (six skills,
with previous-cue comparisons for the four revisions). Source/filter/output hashes
are in `HERO_SFX_REVISION.json` and `WHIRLWIND_TUNING.json`. Re-importing selections
reapplies both later revisions.

## Web silence and rendering

The fail-first browser test recorded zero PCM at the actual WebAudio destination,
even with 43 decoded SFX, triggered cues and a running 48 kHz context. Streamed
playback repairs the output path and preserves the engine's mixer effects.
Fresh desktop and touch tests check audible signal, both mutes and isolated SFX:

| Test | Desktop peak | Touch peak |
| --- | ---: | ---: |
| Combined output | 0.8904 | 0.5597 |
| Background + SFX muted | 0 | 0 |
| SFX only, background muted | 0.4775 | 0.5387 |

The pilot override skipped the existing Compatibility world color/ambient
correction; the arena now applies it before creating the separately corrected
hero. Enemy VFX palettes and sprite foot-shadow linear colors are encoded once
for Compatibility. Native Forward+ color branches retain their original math.

World bakes retain half the native dimensions rather than a universal 512px:
94 at 512px, 10 at 1024px, two at 2048px. All 106 resized RGBA images pass lossless
WebP decode comparison. Bakes total 19.5 MB compressed / estimated 232.1 MB
RGBA with mips; the largest site pack remains under the 50 MB fence. The overview
painting is unchanged. Captured longhall detail is sharper.

All 2,578 native character strips match current source hashes. One representative
strip per each of 42 web kits matches a fresh current q82 conversion pixel-for-pixel;
this is a sampled freshness check, not an all-strip decoded comparison. Actual pack
audit checks all referenced converted bytes/metadata. Web body strips remain half
resolution/lossy q82. No missing world bakes were reproduced: 113 painted files pass,
57 baked meshes and 62 projected meshes report no missing bakes. Any specific
remaining bare object or incorrect sprite still needs identification/visual acceptance.

## Package and validation

All 50 audio clips (43 SFX, six scores, one environment layer) share manifest
`e015b2814bde44e206521e089243c9b015963355b64c800ee29cf8345f65427c`.
ZIP: 2,506,685,734 bytes; CRC passed. SHA-256:
`f93490a5039e6bfa5d5ec1b9b4b54e1e5fd7115894a5ca2de9d978a818ab207c`.
Windows: `../pc_arena/build/BarrowArena-Windows-x64.zip`; extract the entire ZIP,
then open `BarrowArena.exe`. Packed-input audit passes 3,532 inputs and x64 PE.
Mac packed-scene probe decodes all 42 full-resolution kits, finds 827 meshes,
334 collision shapes and 10 MultiMeshes, and advances 125 reference-solver ticks.
CoreAudio mixed peak is 0.6256; independent mutes, loop lifecycle, six scores,
accepted/cooldown-refused cues and the 11-effect-voice cap pass.

Web actual-pack audit passes 3,076 payloads, including 24 active raw terrain fields,
42 kits and all selected audio. Desktop/touch functional controls, actual PCM and
intentional missing-pack refusal pass. Vite production build passes (existing large
app-chunk warning). Total game export: 472,124,779 bytes before HTTP compression.
This remains a large cold download. Physical phone/Safari and the actual Windows
executable/GPU/performance have not been tested; no zero-lag guarantee.

Public route: https://reincarnated-loadout.vercel.app/playtest/barrow-arena/
Loadout commit: `206b4169d4a1272481c8ccb1b2a361ca722e4055`.
Source implementation commit: `cc79fc924` (documentation completion follows).
Vercel production deployment: `dpl_2Rtd1yHdjEycAZ4nX68yLpW3ijMg`, READY.
All 21 public files download without authentication/cookies and match export hashes.

Fresh unauthenticated Chrome 154 touch test on this M2 Mac mini (8 GB RAM):
actual WebAudio peak 0.60895; all four skill buttons, movement, Whirlwind
hold/release, zoom, mutes and score switching pass. Manifest and world painting
checks pass in the hosted WASM scene; no page/script failures. The rendered canvas
is 2532x1170 at 3x DPR. Sustained combat advances from tick 104 to 536.
RAF-interval estimate: 62.6 FPS, p99 30.4 ms, worst 42.6 ms, two intervals above
33.4 ms across 2,236 intervals. Including initial controls: 61.6 FPS, worst 91.9 ms,
nine intervals above 33.4 ms. These are browser callback timing estimates on this
Mac, not physical-phone or all-wave GPU benchmarks. Startup to arena-up is 84.9 s
in this run; network/cache conditions are not controlled against the earlier release.

Remaining visual limits: character body strips retain the existing half-size/q82
conversion; large sprites can still look softer than native. The Compatibility
palette/shadow repair does not establish pixel-identical native appearance. Further
object/sprite-specific visual acceptance and physical phone/Safari testing remain.

Compact committed evidence: `evidence/hero-web-repair/`. Full public logs/screens:
`../web_arena/build/logs/hero-public-touch-long/`.

Local full evidence: `../web_arena/build/logs/{audio-fail-first,browser-desktop,
browser-touch,browser-fail-pack,art-source-check.json,world_texture_detail.json}`
and `../pc_arena/build/logs/native/`. Previous release evidence remains unchanged.
