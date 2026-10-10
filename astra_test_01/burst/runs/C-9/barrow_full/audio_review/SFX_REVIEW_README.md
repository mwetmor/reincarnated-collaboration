# SFX listening review

Open `SFX_REVIEW.html` in Chrome or Safari by double-clicking it. It is a single
offline HTML document with embedded audio: no server, login, or dependencies.
Choose an action from the left, play its current sound(s) and alternatives,
then select **Keep current**, an alternative, **Mute**, or **None fit — find more**.
Playing a preview alone does not select it. Add notes when needed.

Choices save in browser localStorage under
`barrow.sfx.review.v1.<catalog_sha256>`; schema `barrow_sfx_selections_v1`
contains the current manifest/catalogue digests and per-cue choice + notes.
Storage availability for local files varies by browser. **Export selections**
downloads `barrow-sfx-selections.json`, the durable handoff/backup. Send that file
back for integration. **Import selections** restores it on the same review.
Files from a different catalogue are rejected without replacing existing choices.

This covers all 31 live cue mappings, including shared physical attacks and hits,
with current rotations preserved as one choice. Exact source paths and SHA-256s
are recorded in the catalogue and export. Alternatives are shortlists based on
source names, awaiting Matt's listening verdict. Preview conversion is full-length
MP3, stereo 48 kHz / 160 kbps, without gain normalization or trimming. This is
an isolated audition, not the game's actor-specific mix. Whirlwind alternatives
require a loop-seam check before integration.

Feedback recorded: music accepted for now; character SFX need review; most monster
casts rejected pending review; some creature voices loved but not yet identified.
No individual SFX is pre-approved. Game mappings and the delivered PC ZIP stay
at their existing baseline until the selection handoff.

Rebuild from the original, read-only demo audio (ffmpeg already installed):

```sh
python3 /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py C9-SFX-REVIEW -- python3 /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full/tools/arena_sfx_review.py
```

The generated HTML and MP3 cache remain local, like other media artifacts.
The generator, HTML template, and source catalogue are tracked. This private
review document is not a public standalone redistribution of the sound packs.

Verification: opened the generated `file://` document in an isolated Chrome
profile and inspected its rendered layout. All 126 embedded MP3s decoded in
Chrome; playback loaded with a valid duration; selecting an alternative and
adding notes persisted across reload. Keep-current, mute, find-more, search,
JSON export/import, and rejection of a different catalogue passed with zero
JavaScript errors. No audition verdicts were inferred from those technical checks.
