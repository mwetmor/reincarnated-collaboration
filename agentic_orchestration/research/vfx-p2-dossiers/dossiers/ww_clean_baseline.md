# VFX Reference Dossier — whirlwind (clean-baseline verification + supplement)

## Part 1: 3BnHvNZ_4YM verification
- whirlwind_timestamp: UNKNOWN — [Blizzard’s accompanying article](https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021) explicitly identifies Whirlwind as appearing in the embedded video; [GameSpot’s compilation](https://www.youtube.com/watch?v=Ygz21oiv20A&t=322s) places the complete “Combat Improvements” segment at 05:22–06:55, but no accessible source identifies the exact frame time within `3BnHvNZ_4YM`.
- max_resolution: UNKNOWN — the YouTube quality menu/format manifest was unavailable; the missing `maxresdefault` thumbnail alone cannot distinguish 720p from lower encodes.
- frame_extraction_adequate: Y — Blizzard describes visible gameplay-camera footage of the spinning blade, environmental lighting, and kicked-up dust, so it is gameplay rather than concept art or title cards, although the low/unknown resolution limits fine-particle analysis.

## Candidate 1: Whirlwind — unmodified core-skill clip (Diablo III)
- source_game: Diablo III
- skill_or_mtx_name: Whirlwind, core skill unmodified by runes
- primary_url: https://www.bluetracker.gg/diablo3/topic/us-en/4737240-in-development-class-skill-videos-continued/
- secondary_urls: https://www.4gamer.net/games/008/G000817/20120329030/
- media_type: video
- temporal_coverage: windup=N; active=Y; impact=Y
- confounds: Cyclone/tornado add-ons are explicitly absent—the Blizzard post says these core-skill videos are “unmodified by runes.” Wrath of the Wastes is absent because this predates that set. Wing/backpiece absence could not be independently frame-checked from the text-only archive; the footage is presented as a basic official skill capture.
- why_it_fits: This is Blizzard’s March 2012 reference for base Whirlwind at the normal gameplay camera. It is a discrete Whirlwind clip rather than a longer compilation, so the reference begins at 00:00.
- readability_notes: The official skill-video format was intended to isolate and demonstrate the cast and enemy contact. The surviving URL is archival, so playback availability should be checked before adopting it as the extraction master.

## Candidate 2: Whirlwind — pre-rune skill demonstration (Diablo III)
- source_game: Diablo III, 2008 pre-release build
- skill_or_mtx_name: Whirlwind, original pre-rune implementation
- primary_url: https://www.youtube.com/watch?v=swOroVI1UaM&t=0s
- secondary_urls: (optional)
- media_type: video
- temporal_coverage: windup=N; active=Y; impact=Y
- confounds: Cyclone/tornado add-ons are absent because this footage predates Diablo III’s runestone system; Wrath of the Wastes and later cosmetic wing systems are likewise absent. It is a dedicated skill demonstration rather than an endgame build showcase.
- why_it_fits: The entire clip demonstrates the Barbarian’s original Whirlwind; timestamp 00:00. It supplies a historically clean gameplay-camera read of the continuous spin and adjacent-enemy contact.
- readability_notes: The character-centered rotation and weapon envelope are legible, but the 2008-era image quality is suitable mainly for silhouette, cadence, and radius—not fine particles or material response.

## Search log
- Searched `"3BnHvNZ_4YM" Whirlwind`, transcript, chapters, duration, 720p/1080p, format manifests, and coverage articles; found Blizzard’s explicit confirmation and GameSpot’s 05:22 “Combat Improvements” chapter, but no frame-exact original timestamp or authoritative resolution listing.
- Checked the official Diablo IV Barbarian trailer; the prominent spin near 00:21 is identified as Iron Maelstrom, not Whirlwind, so it was rejected.
- Checked LeyzarGamingViews’ Diablo IV beta Whirlwind dungeon video (`XKBZXf9akXc`); metadata did not establish whether Dust Devil’s Aspect was equipped, so it was rejected as a verified clean baseline.
- Checked Blizzard’s Diablo III runestone preview (`8cTBZMWN9qg`); rejected because it uses a black presentation backdrop rather than the gameplay camera and includes rune variants with added twisters.
- Searched Blizzard’s March 2012 “core class skills, unmodified by runes” release and historical Diablo3Inc uploads; retained the official archival skill clip and the dedicated 2008 pre-rune demonstration.