# War Cry, Might and web fidelity — 2026-10-11

## Current follow-up — user-selected Might (2026-10-11)

Matt replaced the Fortify candidate with the supplied
`ElevenLabs_audio_elevenlabs-sound-effects-v2_Deep male bass-_2026-10-11T16_38_03.mp3`.
The original four-second MP3 is copied to `selected_sfx/might_elevenlabs.mp3`
and beside the soundtracks in `pc_arena/build/SFX_and_Sound_Selections/`.
SHA-256: `1db4e2f682613e0981d9c5362654364f7c15ee7c4cc8fad9dc993d4a34031066`.
No pitch, timing, filter or normalization changes. The only changed cue is
`vires_might`; other active clip metadata and all mix settings match the prior
release. Might and War Cry are now user-selected; Charge/Potion remain candidates.
The six-skill audition embeds the exact selected MP3.

Local CoreAudio passes all 43 SFX, six scores, Might playback, lifecycle/mute and
simulation invariance gates. Peak 0.38347. Manifest SHA:
`c3a66faf8017ca6bcd4de04893606881bdbd96579832a8c938730f22175fff2e`.
Evidence: `evidence/might-selected-local.json`.
The web audio pack and main manifest were re-exported; the pack audit passes
3,076 payloads, 42 kits, 24 terrain fields and 50 audio clips. Ordered isolated
pack mounting passes. The Vite production build passes. Textures, renderer,
mobile controls and the prior performance limits are unchanged. Windows ZIP
has not been rebuilt for this follow-up.

Local packaged Chrome touch emulation passes startup, all four skills (including
Might), movement, Whirlwind release, zoom, score and mute controls. Real WebAudio
output is nonzero (peak 0.41945), with no script/page/network failures. Physical
phone behavior remains untested. Evidence: `evidence/might-selected-release.json`.

The remainder of this document records the preceding Fortify-candidate release.


Matt selected the supplied 2.48-second ElevenLabs deep male bass MP3 for War Cry.
The local scene plays the original MP3 bytes, without pitch, time, filter or
normalization changes. Its SHA-256 is
`adf412b8e02d28f01a1d02a5013946af4b08a154db9612933781f09b7148de3e`.
A copy is alongside the soundtracks in `pc_arena/build/SFX_and_Sound_Selections/`;
a small reproducible source is committed at `selected_sfx/war_cry_elevenlabs.mp3`.
The original handoff file is preserved.

Might now uses `PM_SPELL_Buff28_Fortify.wav`, a different source from the rejected
Star Power. Processing is a 60 Hz high-pass, 5 kHz low-pass and 0.80 peak target;
no pitch shift. This candidate remains pending Matt's listening approval.
The six-skill review page is regenerated at `derived_sfx/HERO_SFX_REVIEW.html`.
Other approved cues, the pendulum loop, quieter Whirlwind contact gain,
Fjordstormen level and music choices are preserved.

Local CoreAudio passes 43 SFX, six scores, loop lifecycle, independent mutes,
accepted/refused casts, 11 effect voices, real-combat impacts and simulation
snapshot invariance. Mixed output is nonzero (peak 0.37193). Manifest SHA:
`f9a98d93da157be0b9ef93601bce6a3983c9ea7ee8d498ecc746b6b2df2bef2d`.
Evidence: `evidence/elevenlabs-local-audio.json`.

## Web changes and limits

The new export uses original sprite dimensions, frame sizes, anchors and scale
instead of the earlier half-size strips. WebP quality increases from 82 to 95.
This restores animation detail but still uses lossy compression: it is not a
pixel-identical encoding. Refresh now checks recipe and source/output hashes;
it cannot silently retain the older texture conversion.

World bakes use native dimensions up to 2048px and lossless WebP: 104 of 106 bakes
keep every original pixel; the two 4096px bakes remain reduced. Hero rig texture
cap rises from 1024 to 2048px. Original native textures are not altered.
Oversized export packs are split into bounded files; every member is checked
before/after splitting. The main pack is re-exported with the final mount list.
Animation atlases wider than 4096px are rearranged into narrower frame grids,
without shrinking frames or changing their pixels before encoding. The converter
compares every rearranged frame, and the byte audit normalizes only the verified
grid column count while retaining all animation timings, anchors and scales.

A browser touch check exposed IndexedDB filesystem save failures. The custom
Godot HTML shell now uses session-local memory for playtest telemetry instead
of requiring persistent browser storage. This scene has no saved-progress feature;
native recording remains unchanged.

Web releases unused monster kits periodically, retaining every living/fading
actor's kit and hero overlays, to avoid accumulating all ten waves' full-size
GPU atlases. Native cache behavior is unchanged.

Exact universal player-experience parity is not established. Browser Compatibility
rendering differs from native Forward+, some large textures are reduced, cold
startup downloads remain substantial, and the recorded walk-map reachability
mismatch remains. A Mac browser with emulated touch is not a physical-phone or
Safari performance test. Later-wave visuals and a complete playthrough require
additional acceptance. The existing Windows ZIP predates these changes.

## Verification and publication

Local actual-pack audit passes 3,076 payloads, 42 kits, all 24 terrain fields and
50 audio clips. All 2,578 body strips fit within 4096px; 117 atlases were rearranged.
Export is 28 files, about 649.6 MB uncompressed; largest file 44.4 MB. Hero pack
is split into two byte-verified parts; isolated ordered mounting passes.

Desktop and touch startup/movement/skills/Whirlwind release/zoom/score/mutes pass.
Real WebAudio peaks are 0.45979 desktop / 0.43529 touch; both-muted output is zero
and SFX-only output is positive. No script, page or filesystem-save errors remain.
Missing-pack injection correctly prevents startup. Frame sampling shows occasional
78.9 / 90.9 ms hitches: this is not a zero-lag claim or a physical-phone benchmark.
Compact evidence: `evidence/elevenlabs-web/local-web-gates.json`.
A longer real touch test at device pixel ratio 3 exposed poor sustained rendering
(17.3 FPS on the M2). This blocked publication despite the functional test passing.
The custom HTML shell now preserves CSS/input sizing while bounding the touch
framebuffer to 1.5x density and at most one million pixels (desktop at most 2.1M).
Source textures remain unchanged. The uncapped result is recorded in
`evidence/elevenlabs-web/uncapped-dpr3-performance.json`. New bounded-canvas and
hosted results will be appended after their gates pass.


The bounded canvas passes all controls, two-finger movement/channel hold and
35-second combat (>350 simulation ticks), with native 4x MSAA retained.
Measured crowded combat averages **28.8 FPS** on this Mac at 1266x585 rendering,
versus 17.3 FPS in the uncapped test. These runs use time-seeded encounters and
are not a controlled GPU comparison. Disabling MSAA did not reliably improve
speed (19.9 FPS in a later run), so that experiment is reverted. No texture,
physics or enemy content is removed to conceal lag. Crowded-combat performance
remains an open issue; no zero-lag or physical-phone performance claim is made.


## Published release

Source implementation `155864993afb428c7f4c5a4b7c654445085af155` is pushed.
Loadout release `4b50a63bbf76e0b8ee612f3337c80250baf699d4` is pushed;
Git-triggered production deployment `dpl_E8wCW2FvJnsxZvz9LiiAWURKMjfC` is READY.

Public game: https://reincarnated-loadout.vercel.app/playtest/barrow-arena/
Six-skill audition: https://reincarnated-loadout.vercel.app/playtest/barrow-arena/hero-sfx.html

All 28 public files match the export without authentication or cookies. The
hosted fresh-browser DPR3 touch check passes all four skill buttons, movement,
Whirlwind hold/release, zoom, independent mute controls and score switching.
It also passes second-finger movement while holding Whirlwind, releasing the
movement finger without releasing Whirlwind, and 35 seconds of advancing combat.
Actual WebAudio peak is 0.43651, with running AudioContext and nonzero samples.
No script/page/network failures; the pinned runtime's 78 historical NUL warnings
remain. The audition's War Cry MP3 is byte-identical to Matt's file.

Sustained hosted combat averages **29.7 FPS**, p99 114.3 ms, maximum 255.5 ms.
Crowded-combat lag remains real and recorded. The first download is about 650 MB.
Neither exact native graphics/physics parity nor zero lag nor physical-phone
compatibility is claimed. Evidence: `evidence/elevenlabs-web/production-verification.json`.
