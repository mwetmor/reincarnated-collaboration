# Whirlwind hit balance — 2026-10-11

Matt accepted the pendulum portion and requested quieter character strikes during
Whirlwind. Reduce only outgoing hero physical contacts while the Whirlwind loop
is playing by 10 dB. Incoming monster hits and physical attacks after release keep
their original gain. This is presentation audio only; no simulation/asset changes.
The six-skill listening page and other hero cues remain pending Matt's verdict.

The approved pendulum loop stays byte-identical:
`2b0dfb7ff1c8dbf16fb0d1b523297f6976f7be4de525a96bed4031b2a417bc60`.
Its voice stays -8 dB. The start cue and all selected clips remain unchanged;
audio manifest remains `e015b2814bde44e206521e089243c9b015963355b64c800ee29cf8345f65427c`.

The real local CoreAudio probe compares the same contact clip before channeling,
during channeling, as an incoming hit, and after release. Measured player levels
are -2 / -12 / -2 dB; incoming enemy voice stays -8 dB. Mixer output is nonzero
(peak 0.38055); loop lifecycle, independent mutes, six scores, accepted/refused
skills, the 11-voice effect cap and simulation snapshot invariance pass.
Evidence: `evidence/whirlwind-hit-balance/native-audio.json`.

Web export gate passes 3,076 actual payloads, 42 kits, all 24 terrain fields
and 50 selected audio clips. Desktop/touch startup, movement, skills, Whirlwind
release, real PCM, independent mutes and missing-pack refusal pass. Combined
WebAudio peaks: 0.43962 desktop / 0.36687 touch; both-muted output is zero.
Vite production build passes (existing large-chunk warning). Hosted release
provenance is appended after publication. This update targets
local source + web; the existing Windows ZIP is the earlier hero/audio release.

## User-visible web parity

Not 100% identical. Gameplay/content and selected sound sources are shared, but:
- Web body strips are half resolution/lossy q82; world bakes are half native
  dimensions and hero rig textures are capped at 1024px.
- WebGL Compatibility and native Forward+ have visible lighting/effect differences.
- Web has a large initial download, requires a browser gesture for playback and
  has occasional first-action/cast hitches.
- Physical-phone/Safari, every later-wave animation and complete physics/visual
  parity are not yet verified. The recorded reachability difference remains.

Prior detailed release evidence: `HERO_SFX_REVISION.md`; open dispositions:
`../tools/WEB_ARENA_BUGS.md`. No claim of pixel-identical appearance or zero lag.
