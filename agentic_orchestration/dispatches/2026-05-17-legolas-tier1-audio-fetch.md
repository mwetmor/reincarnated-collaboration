# 2026-05-17 — legolas — Tier 1 audio fetch (~$3.59 + free CC0/public-domain packs)

**Authority:** Matt L3 2026-05-17 late evening — "I authorize legolas for the 3.59 and free tier 1 audio." Explicit acquisition authorization for Tier 1 baseline packs per legolas-4 catalogue.
**Type:** Pattern A — ~30-60 min download + stage + verify; no code changes.
**Predecessor:** Legolas-4 audio vendor catalogue crawl (shipped; Tier 1 baseline identified).

---

## Why this matters

Demo audio pipeline is fully wired in code (Howler.js Tier 2 file-lookup + Tier 1 procedural fallback) but starved of assets. Legolas-4 identified Tier 1 free + ~$3.59 baseline that closes pipeline-unblocking gaps. Matt has authorized acquisition. This dispatch fetches the packs + stages on disk. Drax audio wiring follow-on (after gandalf audio register canon lands) consumes the staged assets.

---

## Required reading

1. **Legolas-4 inventory** — `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/inventory.jsonl` (pack URLs + license info)
2. **Legolas-4 summary** — `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/summary.md` § 7 (Tier 1 acquisition shortlist)
3. **Demo audio infrastructure** — `reincarnated-demo/src/audio/audio.ts` § `getOrLoadSfx()` (Tier 2 file path convention: `/audio/sfx/ability_{geometry}_{element}.{ext}`)
4. **Demo public/audio target** — `reincarnated-demo/public/audio/` (currently has `music/season_001001-005.mp3` only)

---

## Scope — Tier 1 acquisition + staging

### Packs to fetch (per legolas-4 § 7 Tier 1)

1. **Leohpaz RPG Essentials SFX (FREE)** — 48 files; covers all key slots (8 spell elements + 10 UI events + 10 combat events + 7 status effects + enemy death). PRIMARY pipeline-unblocker.
   - URL: leohpaz.itch.io (search for "RPG Essentials" free pack)
   - License: free-no-attribution commercial OR check; flag if attribution-required

2. **Kenney Interface Sounds (CC0)** — UI event coverage; public domain.
   - URL: kenney.nl/assets (search for "interface sounds" or "UI audio")
   - License: CC0 (no attribution; commercially-OK)

3. **Kenney Impact Sounds (CC0)** — impact / hit / death SFX baseline.
   - URL: kenney.nl/assets (search for "impact sounds")
   - License: CC0

4. **OGA RPG Sound Pack (CC0)** — 80+ general RPG SFX; commercial OK.
   - URL: opengameart.org (search "RPG Sound Pack" CC0)
   - License: CC0

5. **TomMusic Free Fantasy 200 (FREE)** — 200 fantasy/RPG SFX; commercial-OK no-attribution.
   - URL: tommusic.itch.io or similar
   - License: free-no-attribution

6. **kmontesdev Fantasy Ambient (CC0; 2 GB)** — hits/ambience/foley/monsters/weapons/spells; HUGE pack.
   - URL: kmontesdev.itch.io
   - License: CC0
   - NOTE: 2 GB is large; download time may be significant; verify disk space first

7. **PixelLoops Ultimate Ambient SFX ($3.59)** — 100 loopable biome ambient loops (Forest/Cave/Dungeon/Swamp/Desert/Ruins/Magic-Temple). 192 MB.
   - URL: pixelloops.itch.io
   - License: commercial single-user perpetual; $3.59 paid acquisition
   - **Matt's authorized this single $3.59 spend.**

8. **Leohpaz Minifantasy Dungeon (FREE)** — supplementary dungeon-themed SFX.
   - URL: leohpaz.itch.io (search Minifantasy Dungeon)
   - License: free

### Staging structure

Stage at `reincarnated-demo/public/audio/sfx/` with organized subdirs:

```
public/audio/sfx/
  ├── leohpaz/                  # Leohpaz RPG Essentials + Minifantasy Dungeon
  ├── kenney/                   # Kenney Interface + Impact
  ├── oga/                      # OGA RPG Sound Pack
  ├── tommusic/                 # TomMusic Free Fantasy 200
  ├── kmontesdev/               # kmontesdev Fantasy Ambient (2 GB)
  ├── pixelloops/               # PixelLoops biome loops
  └── _licenses/                # COPIED license.txt / readme per pack for attribution audit
```

Do NOT rename files yet — gandalf audio register canon (in flight) + elrond audio curation (queued) will produce the file-naming-mapping manifest that drax wires against. You just FETCH + STAGE.

### Acquisition mechanics

Each pack source:
- itch.io packs: typically require an itch.io account; "buy" at $0 for free packs; download zipped pack; extract to staging dir
- OpenGameArt packs: direct download from OGA page; extract
- Kenney.nl: direct download (no account needed); extract
- PixelLoops $3.59: requires payment — itch.io account + $3.59 purchase

**If any pack requires a payment beyond the authorized $3.59 PixelLoops:** STOP that pack acquisition; flag in completion record; do NOT spend without Matt re-authorization.

**If any pack's license file says "non-commercial" or "research-only"**: DO NOT include; flag in completion record.

---

## Out of scope (DO NOT)

- ❌ DO NOT spend beyond authorized $3.59 (PixelLoops single pack)
- ❌ DO NOT rename / restructure pack contents (drax wiring will use elrond's naming manifest)
- ❌ DO NOT touch demo audio.ts code
- ❌ DO NOT fetch Tier 2 ($182 WOW Sound bundle) or higher tiers — those need separate Matt L3
- ❌ DO NOT skip license-file copying — attribution + commercial-clearance audit depends on it
- ❌ DO NOT include vendor packs that surface "AI training prohibited" if Reincarnated planning includes AI-assisted dev (most don't matter; just be aware)

---

## Acceptance criteria

- [ ] All 8 Tier 1 packs staged at `reincarnated-demo/public/audio/sfx/{vendor}/`
- [ ] PixelLoops $3.59 acquired (single Matt-authorized spend)
- [ ] License files preserved + copied to `_licenses/` subdir
- [ ] Disk-size verification: kmontesdev 2 GB pack disk-space check before fetch
- [ ] Completion record documents: total file count per pack; total disk usage; any download failures or license-blocks
- [ ] Hive-log STATE entry
- [ ] HANDOFF → elrond: assets staged; ready for audio-curation manifest authoring (consume staged paths into vfx-layered-architecture-style manifest)
- [ ] HANDOFF → drax: assets ready for wiring after elrond curation + gandalf register canon both land
- [ ] HANDOFF → matt: attribution-required packs flagged (Leohpaz, OGA RPG, TomMusic — confirm tracking)
- [ ] No tag (catalogue fetch; not code)

---

## Coordination

- **Parallel-safe with**: drax v1.13 VS2a Final Sprint (different seam; you only write to public/audio/sfx/, drax writes to src/visuals/); rocket D11.1 implementation (engine); gandalf audio register canon (canonical/story); elrond monster-subset curation (research/curated/)
- **Triggers downstream**: when gandalf audio register + your staged packs both land → elrond audio curation manifest fires (queued); when elrond curation lands → drax audio wiring follow-on dispatch
- **PRE-SIGNAL § 14.1.1** before hive-log append

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 explicit Tier 1 authorization. ~30-60 min. Append completion record when done.*
