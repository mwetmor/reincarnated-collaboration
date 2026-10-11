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

Eight cues request a new audition and retain the prior cue for now:

- Charge / Blitz: all auditioned choices rejected.
- Potion: bottle opening or pouring requested.
- Might: a more magical effect requested.
- Battle Cry: barbarian yell / shout requested.
- Whirlwind start and repeating body: rotating mace, rushing air and metal.
- Poison cast: new choices needed.
- Poison impact: breaking glass requested.

Footsteps, player death and ranged attack remain unreviewed, so their mappings
also stay at the baseline. `find_more` is not interpreted as `mute`.

The local scene defaults to **Northern Omen** (190 seconds), with **Fjordstormen**
(30 seconds) on a separate environment bus. The original user MP3 bytes are
copied to `audio_review/soundtracks/` outside the disposable build directory.
The score begins with the fight; storm ambience begins while the arena is ready,
and its repeats use a 1.5-second overlap with linear gain crossfade. Score levels
are -22 dB / -28 dB in combat; environment levels are -28 dB / -32 dB in combat.
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

This changes the **local source scene**. The existing Windows ZIP is the prior
audio build and has not been re-exported in this task; its previous package
verification remains historical evidence for that ZIP.
