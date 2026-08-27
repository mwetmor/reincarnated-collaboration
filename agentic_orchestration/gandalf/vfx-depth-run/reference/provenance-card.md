# PROVENANCE CARD — VFX-depth run true referent (R-28 step-0 law, first application)

> **Law being applied (minted at charter ledger R-28, 2026-08-26):** *REFERENT IDENTITY IS A PRE-REGISTERED FACT — the skill's step 0 is a provenance card (source URL + title + hash) shown to Matt at charter time, BEFORE any seat fires.* This card is that fact. No blind seat (X-5/X-6), no galadriel re-anchor, no bar re-derivation fires until Matt confirms this card.

**Filed:** 2026-08-26 · **Conductor:** gandalf (RUN-CONDUCTOR) · **Status:** ⏳ AWAITING MATT ONE-LINE CONFIRM

---

## § 1 — Identity (verified, not assumed)

| Field | Value | Verified how |
|---|---|---|
| Source URL | `https://www.youtube.com/watch?v=KaMPoPywM40` | Matt's ruling, 2026-08-26: "we need to use this" |
| Title | **"The Whirlwind Barbarian Is Smashing Everything In Diablo 4 Season 14!"** | yt-dlp metadata probe + oEmbed cross-check |
| Uploader | Cliptis | same |
| Duration | 18:43 (1123.5 s) | ffprobe on downloaded file |
| Format | 1920×1080 @ 60fps, AV1 | ffprobe |
| File | `reference/KaMPoPywM40-d4s14-whirlwind-cliptis.mp4` (173 MB — gitignored, host-resident) | on disk |
| sha256 (head) | `70299632ade9a044…` | computed post-download |
| Wrong referent it supersedes | D3 Whirlwind, Blizzard 2012 master (`855bb3d9…`) — preserved as `lap2-gate-evidence/WRONG-REFERENT-d3-2012-master.mp4` | R-28 incident |

## § 2 — Confound map (conductor scout, 2026-08-26; conductor is NOT blind — seats never see this file)

- **~85% of runtime is MENUS** — paragon boards, skill trees, gear tooltips, stat sheets. Build-guide video, not gameplay footage.
- **Facecam** bottom-left in EVERY frame; **"Cliptonian Legion"** branding top-left; **"Diablo Partner Program"** watermark bottom-right.
- Combat substrate: **"The Training Grounds"** vs **"Boss Training Dummy"** targets (golden glowing dummies), Torment X, party members "Subo"/"Aldkin" on screen.
- **Damage-number spam dominates combat frames** (545B, 9,940M, 12.4B) — a major luminance/saturation confound for any pixel-statistics instrument.
- S14 **Dust-Devil** procs ride alongside the core whirlwind — legolas RT-4 finding: subtractable.
- Whirlwind VFX itself: **red/orange circular disc-sweep + fire around the barbarian** — clearest at t=1066. (Note: NOT the steel/dust guess in R-28; this S14 build reads hot.)

Scout evidence in `reference/scout/`: `sheet_01..03.jpg` (15s-interval contact sheets, whole video), `full_t843.jpg`, `full_t1066.jpg`, `combat_zoom.jpg` (t 815–915 @4s), `combat_tail.jpg` (t 1040–1100 @4s).

## § 3 — Proposed extraction treatment (conductor-side, BEFORE seats)

1. **Trim to combat windows:** primary **t ≈ 820–915** (densest whirlwind action) · secondary **t ≈ 1040–1100**.
2. **Crop:** remove facecam region (bottom-left), branding (top-left), watermark (bottom-right) — fixed-position crops, content-independent, safe for blind protocol.
3. **Damage numbers + party UI:** NOT croppable (overlaid mid-frame). Handled at the MEASURE layer — galadriel instruments mask or the confound is named in the anchor note; blind seats see them and that is acceptable (they are part of what the video looks like).
4. Dust-Devil: no pre-subtraction for seats; galadriel applies RT-4 subtractability at measurement only.

## § 4 — The honest referent-quality question (veto-open; the ruling stands unless Matt strikes it)

The named referent yields **~2 minutes of confound-laden training-dummy combat** from an 18:43 build guide. Matt's ruling is taken as written: **KaMPoPywM40 alone IS the reference.** The old selection-gate's dormant "official clean clip as calibration baseline" pairing stays retired unless Matt revives it. The twin skill's job is to reproduce what THIS video's whirlwind looks like, in whatever room it was filmed.

## § 5 — What fires on confirm

Galadriel re-anchor (`vfx_ref_anchor.py` on the trimmed windows) → bar constants re-derived under R-27's lift-form/sign-form → fresh blind seats **X-5/X-6** → superseding lap-2 gate packet re-issuing G-1..G-5 (G-2 re-posed against the true palette).

**Confirm shape:** one line — e.g. `confirmed` / `confirmed, but window X` / `struck: §N`.
