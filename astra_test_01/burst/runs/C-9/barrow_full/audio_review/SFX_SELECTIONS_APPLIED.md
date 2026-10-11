# Local playable scene: approved audio handoff

`APPROVED_SFX_SELECTIONS.json` is Matt's exported handoff from
`pc_arena/build/SFX_and_Sound_Selections/`. `SELECTION_APPLICATION.json` records
the exact input hash, reviewed baseline, changes, and unresolved requests.
`ARENA_AUDIO_REVIEW_BASELINE.json` preserves the original audition mapping;
rebuilding the review page continues to use that same catalogue and choices.

Applied 13 replacement mappings and retained seven explicitly approved current
mappings. The physical hit uses Matt's chosen source because it fits the hero's
mace; the source filename says sword, but its label does not define gameplay.
Ghost attacks rotate vocal A/B as requested. Generic deaths rotate Goblin,
Demon, Troll, Minotaur, and Fire Elemental deaths; the approved ghost, ghoul,
golem and orc family death cues remain unchanged. Rotation is presentation-only
and does not consume simulation RNG.

The original application left four rejected hero cues at their baseline; Matt's
follow-up identifies this as unfinished work. `HERO_SFX_REVISION.json` now
supersedes those deferrals with implemented listening revisions:

- Charge / Blitz: lower weapon-air rush with a restrained metal strike.
- Potion: the demo's bottle opening/handling Foley, replacing the healing spell.
- Might: a new Star Power cast, lowered and kept at roughly its original duration.
- Battle Cry: the closest male voice from the review, lowered about eight
  semitones and shortened to 1.16 seconds; the rejected magical rally is removed.

These revisions are not marked artistically approved. In particular, lowering
an existing scream does not prove it has the requested barbarian delivery.
Listen to `derived_sfx/HERO_SFX_REVIEW.html` to compare the live revised cues
against their previous sounds. Haste retains Matt's approved Dash02; Whirlwind
now follows Matt's later rotating-pendulum direction. Reapply preserves both revision recipes.

Two monster cues remain unresolved and retain the prior cue:

- Poison cast: new choices needed.
- Poison impact: breaking glass requested.

Footsteps, player death and ranged attack remain unreviewed, so their mappings
also stay at the baseline. `find_more` is not interpreted as `mute`.

The local scene defaults to **Northern Omen** (190 seconds), with **Fjordstormen**
(30 seconds) on a separate environment bus. The original user MP3 bytes are
copied to `audio_review/soundtracks/` outside the disposable build directory.
The score begins with the fight; storm ambience begins while the arena is ready,
and its repeats use a 1.5-second overlap with linear gain crossfade. Score levels
are -22 dB / -28 dB in combat; environment levels are -20 dB / -24 dB in combat
(raised 8 dB at Matt's follow-up request).
The existing SFX mix and limiter stay intact. M mutes both background layers,
K mutes effects, B changes the score while keeping the storm layer.

New selected WAV sources are kept read-only and staged as plain PCM16 WAVs at
48 kHz; their source hashes, conversion recipes and staged hashes are recorded.
Raw `.bin` payloads remain exportable. Restage under the shared heavy lock with
`tools/arena_stage_audio.py`; reapply the handoff with
`tools/arena_apply_audio_selections.py` under that same lock.

Verified in the real Godot arena with CoreAudio and the reference solver:
43 SFX decoded; six score tracks decoded; environment loaded and loop handoff
passed; accepted/rejected skill cues, independent background/effects mutes,
Whirlwind release/reset and the 11-voice effects cap passed. A 10-second combat
capture measured 480,768 frames and a peak of 0.5703 (below clipping).
The adapter preserved the exact combat snapshot. Evidence is locally retained at
`audio_review/evidence/selected_audio_probe.json`. Existing sealed-reader NUL
warnings and Godot shutdown resource warnings remain outside this audio change.

Matt's latest follow-up changes Whirlwind to heavy pendulum-like weapon-air
passes at a faster circular pace: eight sweeps across 3.36 seconds, spaced
0.42 seconds apart, with low overlapping tails. The initial cue has a quiet
metal onset. Mace impacts come from actual accepted physical contact events. Source hashes, gains,
conversion and output hashes are in `WHIRLWIND_TUNING.json`; regenerate with
`tools/arena_tune_audio.py`. Reapplying the handoff preserves this later tuning.
The default score is prepared during loading to reduce first-input work.

The current release rebuilds Windows and web from this same audio manifest.
See `ARENA_RELEASE_2026-10-10.md` for current package and browser evidence;
the earlier probe measurements above remain historical.

Current 2026-10-11 voice/Might revision: `ELEVENLABS_WEB_REVISION.md`. War Cry now
uses Matt's supplied ElevenLabs MP3 unchanged, copied alongside the soundtrack
selections. Might uses Fortify instead of the rejected Star Power; artistic
approval remains pending. The six-skill page is regenerated; approved pendulum
and quieter Whirlwind contacts are preserved.
