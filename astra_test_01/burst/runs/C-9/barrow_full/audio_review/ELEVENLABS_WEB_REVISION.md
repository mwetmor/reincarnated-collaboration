# War Cry, Might and web fidelity — 2026-10-11

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
