# Barrow arena release — 2026-10-10

At Matt's request, the local scene and Windows ZIP now use slower, deeper metallic
Whirlwind strikes and a louder Fjordstormen layer. Web content parity is reopened.
This is drax presentation work; the sealed runtime/model pack are unchanged.
No agent delegation or fallback was used.

## Audio and packaging

Whirlwind blends demo sword air with alternating Metal Hit 05/08 at 70% speed/pitch,
six strikes per 4.8-second loop (0.8-second spacing). Original inputs remain read-only.
`WHIRLWIND_TUNING.json` records source/output hashes and conversion details.
Fjordstormen is raised 8 dB: -20 dB ready, -24 dB combat. Score levels remain
-22/-28 dB. Default score preparation moves into loading; music still starts with
combat. All 43 selected SFX, six scores and the environment layer are included.

Local scene: `../godot/scenes/bv2f_arena.tscn`.
Windows deliverable: `../pc_arena/build/BarrowArena-Windows-x64.zip`.
Extract the entire ZIP, then open `BarrowArena.exe`.

ZIP: **2,506,414,675 bytes**; CRC and SHA-256 passed.
SHA-256: `59c7c35c1b5959c2b190cb564c73c1bda220c2ba1cbaf993c4fe68dbaf87266e`.
The actual Windows PCK contains 3,528 byte-verified inputs, including every local
presentation script and original-resolution art. The isolated Mac packed-scene
probe decoded all 42 kits, found 825 meshes, 334 collision shapes and 10 MultiMeshes,
and advanced the reference-solver fight 125 ticks with 3 m of movement.
CoreAudio checked all six scores, independent mutes, accepted/refused skills,
Whirlwind release/reset, ambience crossfade and the 11-effect-voice cap. Mixed peak
was 0.513, below clipping. These are Mac probes of Windows payloads; the Windows
executable/GPU/performance have not been tested on an actual PC.

## Web content and controls

The previous web packs omitted all raw terrain `.f32` inputs and three character
kits. Current packs contain all 24 active terrain fields and all 42 native
catalogue kits, including burrow worm, crawler larva and EOR overlay. Historical
unused levels remain excluded. Actual-pack audit verifies 3,076 payloads: every
retained raw scene input, all local scripts and selected audio, runtime/model
members, kit indexes and strips. Animation metadata matches native after the
intentional texture/anchor scaling. Web textures remain smaller and use WebGL
Compatibility; this is not pixel-identical Forward+ rendering.

The 3D hero receives Compatibility color correction at creation. Its brightness
gain now occurs during lighting, avoiding clamped/bleached armor albedo. First-wave
cells, Whirlwind, snow puffs and both zoom sizes prepare before interactive play,
without changing the fight snapshot. Frame-history accounting is linear.

Real Chrome tests pass mouse/keyboard, movement, Whirlwind hold/release, all four
touch skill buttons, zoom, background/effects mutes and soundtrack switching.
A deliberately missing pack correctly stops startup. Pack/runtime integrity,
3D hero, enemy VFX and audio manifest are checked in the running WASM game.

## Performance and remaining acceptance

Measured in Chrome 154 on this Apple M2 Mac mini, 8 GB RAM; wall-clock RAF intervals.
These are bounded tests, not a zero-lag guarantee or physical-phone benchmarks.

| Scenario | Average FPS | p99 frame | Worst frame | Frames over 33.4 ms |
| --- | ---: | ---: | ---: | ---: |
| Cold desktop interactions | 55.1 | 50.7 ms | 366.8 ms | 6 / 386 |
| Cold touch controls, including every skill | 56.1 | 50.1 ms | 382.1 ms | 7 / 489 |
| Sustained desktop combat | 59.3 | 18.6 ms | 234.4 ms | 6 / 2,228 |
| Sustained 3x-DPR rendering, 2532x1170 | 57.4 | 34.1 ms | 216.5 ms | 41 / 2,160 |

Short first-input/cast/zoom hitches remain. Later-wave performance and every
animation need a full playthrough. Web has 86,653 walk-floor cells, matching native;
29,264 reachable cells versus 29,200 native is a small unresolved platform difference.
Physical phone startup, Safari, audio unlock, memory and speed remain unverified.
The initial web payload is large (461,837,815 bytes before HTTP compression).
Known sealed-reader NUL and WebGL readback-performance warnings are retained;
there are no other page/script failures in the passing tests.

Local full logs/screens: `../web_arena/build/logs/final-*`;
compact records: `evidence/current-web/`. Current package and per-file hashes:
`ARENA_RELEASE_2026-10-10.json`. Bug dispositions: `../tools/WEB_ARENA_BUGS.md`.

## Public release

Public route: https://reincarnated-loadout.vercel.app/playtest/barrow-arena/
Loadout commit: `d137ba995485528ae25ec1b7f5110e7a9209452e` (only these 21 game files).
All staged files match the audited export, and `npm run build` passed.
The first public build passed unauthenticated downloads and desktop/touch tests,
but cold startup took 214.5 / 210.7 seconds. The final loader downloads three
packs concurrently, in bounded batches, and mounts them in stamp order. Every
pack must succeed before the scene opens. Local startup is 56–58 seconds.
Vercel deployment `dpl_EQDyAHh3Ny9JaGJhdeQUAWvuQh8V` is READY on the production alias.
All 21 latest hosted files match the local export SHA-256 hashes without authentication.
The fresh unauthenticated Chrome test passes movement, all four touch skills,
Whirlwind hold/release, zoom, mutes and score switching at 3x DPR (2532x1170).
Cold startup is **145.3 seconds**, down from 214.5 seconds (32% shorter).
Sustained real touch Whirlwind combat: **59.9 FPS**, p99 18.6 ms, worst 34.7 ms,
2/2,138 frames over 33.4 ms. Combat advanced more than 350 ticks, and release passed.
Including cold controls: 58.8 FPS, p99 18.7 ms, worst 400.3 ms, 13/2,621 frames over
33.4 ms. First-action hitches and the large initial download remain real limitations.
Hosted logs/screens: `../web_arena/build/logs/release-public-touch-long/`.
Physical phone and Windows playtests remain unverified.
Preview protection remains enabled; production alias is the intended tester link.
