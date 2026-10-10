# Demo audio reuse — Barrow arena

Inventory: 2026-10-10. Read-only source: `/Users/admin/Games/reincarnated-demo/public/audio`.
The Pixi demo was not modified. Reproduce with `tools/arena_audio_inventory.py --output audio_review`.

## What is actually present

- **2,004 valid audio files**, 3.91 GB, after excluding 96 AppleDouble metadata files masquerading as WAVs.
- 1,358 WAV, 535 OGG, 111 MP3. All files inspected by WAV parsing or ffprobe; no unreadable audio found.
- 2,000 distinct byte hashes. Four exact duplicate pairs. Many additional files are alternate formats of the same sound.
- **1,598 pack/basename identities** after grouping alternate formats. This is filename grouping, not a claim of 1,598 acoustically distinct effects.
- Every file referenced by the demo's live audio manifest exists: 72 skill slots, 27 foley/UI slots, eight biome slots, and all five season tracks. Inventory JSON/CSV include paths, durations, formats, sizes and SHA-256s.

The strongest reusable groups are Pixel Magic (404 magic files), Kenney (230 impacts/UI/footsteps),
OGA (96 RPG effects), Leohpaz (112 combat/heal/movement effects), TomMusic (204 names in WAV/OGG),
and PixelLoops ambience (102 names across formats). Additional folders include 69 creature clips,
61 footsteps, 54 battle sounds, 40 sword sounds, 58 magic/weapon sounds, 31 dragon clips,
42 human ambience clips, and several environment collections.

## Added to the existing Godot arena

**42 SFX clips + five original music tracks**, 47 files / approximately 62.3 MB. The small
`godot/data/audio/arena_audio.json` manifest records original source paths and hashes. Run
`tools/arena_stage_audio.py` to copy them into ignored `.bin` files; no conversion, new sound generation,
or source-library edits. Godot decodes these original bytes at runtime; export auditing checks them.

One otherwise valid 24-bit bow WAV was rejected by Godot's WAV loader; the shipped bow launch
uses TomMusic's existing OGG instead. The full inventory establishes readable audio with WAV/ffprobe
tools, not that every vendor WAV header can be used in Godot without conversion.

- Hero: sword swings/contact, Charge, Potion, Might, Battle Cry rally effect, Haste, Whirlwind start and looping body, death, and insufficient-energy feedback.
- Monsters: physical swings and bow launches; fire, cold, lightning, poison, aether and vitality casts/impacts; ghost attack variations; ghost/ghoul/golem/orc deaths, with a generic death fallback.
- Movement: five rotating snow footsteps, driven by distance actually travelled, suppressed while charging. Surface-specific switching remains a presentation follow-up.
- Music: all five original MP3s, with **Ossuary Procession** as the provisional default. Starts with the fight, ducks beneath combat and Whirlwind, and loops at track end.
- Controls: **M** toggles music, **K** toggles effects, **B** switches soundtrack. Current track/mute status appears in the HUD.

The adapter consumes accepted cast/hit/death/channel events, so cooldown-rejected input does not
play a successful cast. The presentation-only slash uses its existing visual start/contact callbacks.
Enemy sound tails have six voices; hero feedback has four reserved voices plus a separate Whirlwind
loop. Repeated impacts are throttled. Separate music/effects buses feed a -1 dB limiter.
The simulation, sealed runtime, model pack and combat RNG are unchanged.

## Soundtracks

- **Black Salt Depths** (`season_001001.mp3`): 8:00. Title suggests the coast/cave side of Barrow.
- **Catacomb Ember** (`season_001002.mp3`): 4:46. Candidate for a dungeon or hotter combat setting.
- **Ossuary Procession** (`season_001003.mp3`): 5:51. Provisional Barrow default because the burial theme fits the setting.
- **Mercury Throne** (`season_001004.mp3`): 2:50. Alternative to audition for more concentrated arena play.
- **Dirt Road Echoes** (`season_001005.mp3`): 4:04. Candidate for travelling/exploration.

There are **five**, not six, season soundtracks in this demo. Other MP3s are door/ambient sound effects.
All five music files are stereo, 48 kHz, tagged `mhwetmore`, `[Instrumental]`, and `made with suno`.
Technical reuse is verified by decoding, not by a subjective listening review. The thematic recommendations
above are inferred from titles; the canvas provides 20-second excerpts from 45 seconds into each track
for audition. Final music selection, volume balance and track/Whirlwind loop seams need a listening pass.

## Gaps and next refinements

- No explicitly named skeleton, spider or insect sound sets found. Barrow's larvae, tentacles, exploding creatures and other distinctive bodies still need individual attack/hurt/death identities or an auditioned match from generic clips.
- Battle Cry currently uses a magical rally effect. A short, clean voiced warlord shout would give it a stronger identity; the library's human screams are not automatically a good substitute.
- Dedicated poison effects **are present** and used. Aether currently borrows light/holy magic; a custom aether identity remains provisional.
- Physical ranged attacks use a bow launch; thrown axes/rocks and heavy slam/boss attacks would benefit from more specific assignments. Their generic physical fallback is functional.
- Snow footsteps work now; wood, water, ice and other surface variants exist but need ground-surface routing. Environmental wind/sea/cave ambience exists but is not mixed into this combat pass.
- Confirm long MP3 loop transitions and the Whirlwind body seam by ear; source clips are not assumed to be seamless just because looping is enabled.

## Provenance carried forward

Kenney and OGA have local CC0 notices. Leohpaz has local commercial-game-use notices. TomMusic's
local pack notices and PixelLoops' actual packaged `LICENSE.txt` permit game use; PixelLoops forbids
redistributing a standalone sound library. Some older `_licenses/` staging-status notes are stale:
the actual packs are now present. Pixel Magic's purchase is recorded in the demo's `AGENT_STATE.md`
and audio manifest; no separate license text was found beside its WAVs. Root-level creature/weapon
folders are attributed to the staged kmontesdev collection by the demo manifest; preserve the original
notices rather than treating that mapping as a new licensing audit.

The five music files record their Suno provenance, but their original generation/subscription receipts
are not in the audio folder. This review establishes technical reuse; it does not establish a new
commercial rights determination. Existing source notices are included with the PC game's audio credits.

The previously recorded web/mobile visual, physics, art and deployment-access bugs remain deferred
in `../tools/WEB_ARENA_BUGS.md`; no web deployment or mobile compatibility fix is included here.


## Verification result

`AUDIO_VERIFICATION.json` records the source and packed probes. All 42 SFX and all
five MP3s decode in Godot 4.6.3. A real ten-second packed fight, using the existing
GDScript reference solver and CoreAudio on Mac, yielded 480,256 mixed frames with
a maximum amplitude of 0.441226 (-7.1 dBFS). Checks passed for accepted versus
cooldown-rejected Potion casts, all hero cue bindings, unchanged snapshot during
audio consumption, Whirlwind release/reset/terminal stops, independent mutes, and
bounded voice pools. No script errors. Existing sealed-data NUL and renderer
shutdown leak diagnostics persist separately.

The updated Windows ZIP passed 3,449 pinned/raw payload checks and complete ZIP
CRC/hash verification. Windows executable launch/audio output remain unverified;
this was a Mac test of the actual packed payload. Subjective mix/loop audition
is still needed.

Godot APIs checked against the official documentation: [WAV runtime loading](https://docs.godotengine.org/en/stable/classes/class_audiostreamwav.html),
[Ogg runtime loading](https://docs.godotengine.org/en/stable/classes/class_audiostreamoggvorbis.html),
[MP3 runtime loading](https://docs.godotengine.org/en/stable/classes/class_audiostreammp3.html),
and [mix capture](https://docs.godotengine.org/en/stable/classes/class_audioeffectcapture.html).
