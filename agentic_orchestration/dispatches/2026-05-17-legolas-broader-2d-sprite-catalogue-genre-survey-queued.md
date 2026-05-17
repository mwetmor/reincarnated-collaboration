# 2026-05-17 — legolas — Broader 2D/sprite catalogue genre-fit survey (QUEUED — auto-fires after legolas-1)

**Authority:** Matt L3 2026-05-17 (~21:30 EDT). Commission queued; auto-fires when legolas icon/prop crawl (legolas-1) completes.
**Type:** Pattern B — Mode B systematic catalogue crawl + genre-fit analysis; ~1-2 days.
**Predecessor (gates auto-fire):** legolas icon + interactable-prop catalogue crawl (`agentic_orchestration/dispatches/2026-05-17-legolas-icon-and-prop-catalogue-crawl.md`).
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until legolas-1 ships.** Knight-rider will activate when legolas-1 lands.

---

## Why this matters

Legolas-1 crawled 9 specific asset categories (floor loot + ambient props + UI icons) at the level of category-driven sourcing. This commission **complements** legolas-1 by asking a different question: **what's the broader 2D/sprite catalogue landscape for our genre right now?**

Matt's frame: a wider sweep across 2D/sprite catalogues — what's available, what fits our genre (ARPG / Isekai / pixel-HD-2D register), with cost + link in JSON format.

This serves three purposes:
1. **Vendor landscape mapping** — who are the active 2D/sprite asset vendors for our genre right now? (the curated list informs future commissions)
2. **Opportunity discovery** — packs we don't know exist (character sets, environment tilesets, atmospheric assets, UI kits, animation packs) that fit our register
3. **Cost intelligence** — pack price ranges across vendors; what's premium vs budget; bundle discount patterns

---

## Required reading (when activated)

1. `canonical/story/style-register.md` — locked HD-2D-pixel register (your primary genre-fit criterion)
2. `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf's sizing canon (your sizing-fit criterion)
3. `canonical/29-design-overview.md` — overall game design framing (ARPG / Isekai genre positioning)
4. `agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/` — your own legolas-1 output (avoid re-crawling vendors already deeply mapped)
5. `agentic_orchestration/research/catalogue/pimen/` — pimen catalogue (already crawled; reference for completeness)
6. `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` — Step B Tier-1 vendor candidates (baseline knowledge)
7. `reincarnated-demo/public/assets/` — current acquired inventory (to identify already-acquired vendors)

---

## Scope

### Item 1 — Broader vendor landscape crawl

Survey 2D/sprite catalogue vendors across our genre. Categories of interest:

- **Character sprite packs** — PC + NPC + enemy/boss variants per genre/style
- **Environment tilesets** — dungeon floors, walls, terrain, decorations
- **VFX/effect packs** — beyond what we have (Pimen, CodeManu, CreativeKind)
- **Animation packs** — character actions, monster behaviors, projectile animations
- **UI kits** — beyond just inventory icons; HUD frames, menu backgrounds, font/typography packs
- **Atmospheric / mood packs** — lighting overlays, particle systems, ambient sprites
- **Misc / specialty** — anything that fits our register that doesn't slot above (e.g., crafting station sprites, vendor NPC packs)

For each vendor, capture:
- Vendor name + URL
- Active status (have they shipped in last 12 months?)
- License posture (CC-0 / CC-BY / commercial / mixed)
- Pack count + price range
- Pixel-style alignment with HD-2D-pixel register (yes / no / partial)
- Genre alignment with ARPG/Isekai (yes / no / partial / adjacent)
- Notable packs they ship (a sample of 2-5 per vendor as anchor)

### Item 2 — Genre-fit assessment

Per vendor, rate alignment:

- **STRONG FIT** — pixel-HD-2D register match + ARPG/Isekai genre match + active vendor + license-clean
- **PARTIAL FIT** — meets some criteria; specific packs may fit but vendor breadth is variable
- **WEAK FIT** — register or genre mismatch; specific packs maybe still useful as outliers
- **OUT OF SCOPE** — different style register entirely (e.g., 3D, vector, non-pixel)

### Item 3 — Cost intelligence

Document price ranges per vendor (low / median / high pack prices). Identify:
- Premium vendors (CraftPix-tier) with high quality + commercial license at $5-25/pack
- Budget vendors with mixed quality at $1-5/pack
- Free CC-0 vendors (Kenney-tier) with prolific output but lower per-asset polish
- Bundle discount patterns (sale frequency, bundle-vs-individual savings)

### Item 4 — JSON output (per Matt's spec: "JSON output with cost + link")

File at `agentic_orchestration/research/catalogue/2d-sprite-vendors-genre-survey-2026-05-17/vendors.jsonl`:

```json
{
  "vendor_name": "CraftPix",
  "vendor_url": "https://craftpix.net/",
  "active": true,
  "license_posture": "commercial-license",
  "pack_count_estimated": 200+,
  "price_range_usd": {"low": 5, "median": 15, "high": 50},
  "register_fit": "STRONG",
  "genre_fit": "STRONG",
  "categories_covered": ["character-sprites", "environment-tilesets", "ui-kits", "vfx", "animations"],
  "notable_packs": [
    {"pack_name": "Wood Nature Tileset", "url": "https://craftpix.net/...", "cost_usd": 12.75},
    ...
  ],
  "bundle_discount_pattern": "Occasional 30-50% sales; bundle mega-packs at ~50% individual sum",
  "license_notes": "Royalty-free commercial license; attribution not required",
  "notes": "..."
}
```

### Item 5 — Summary document

At `agentic_orchestration/research/catalogue/2d-sprite-vendors-genre-survey-2026-05-17/summary.md`:

1. Vendor count surveyed
2. STRONG / PARTIAL / WEAK / OUT-OF-SCOPE distribution
3. Top 5 STRONG-FIT vendors with rationale
4. Category coverage gaps (categories where no STRONG vendor covers)
5. Cost intelligence rollup
6. Opportunity flags — packs/vendors worth Matt's review for future acquisition queue

### Item 6 — Cross-references

- Cite gandalf style-register lock
- Cite gandalf mobile-pixel-sizing canon
- Cite Step B Tier-1 review (this commission extends/refreshes that landscape)
- Cite acquired-vendor inventory in `reincarnated-demo/public/assets/`

---

## Out of scope (DO NOT)

- ❌ DO NOT make acquisition recommendations or commission new vendor purchases (Matt-authority)
- ❌ DO NOT duplicate legolas-1 work (you ran legolas-1; build on its vendor list, don't re-crawl)
- ❌ DO NOT extend to 3D / vector / non-pixel assets (register-mismatch by design)
- ❌ DO NOT extend to font/audio/music vendors (separate scope; out of frame)
- ❌ DO NOT extend to per-pack deep evaluation (this is vendor-landscape survey; pack evaluation is per-acquisition work)

---

## Acceptance criteria (when activated)

- [ ] Vendor landscape crawled (~15-30 vendors)
- [ ] Per-vendor JSON row authored
- [ ] STRONG/PARTIAL/WEAK/OUT-OF-SCOPE classification per vendor
- [ ] Cost-intelligence rollup
- [ ] Summary doc authored (top 5 STRONG-fit; category-coverage gaps; opportunity flags)
- [ ] Cross-references to style-register + mobile-pixel-sizing canon
- [ ] Hive-log STATE entry
- [ ] No tag (research/catalogue work; standard authoring discipline)

---

## Coordination

- **AUTO-FIRE TRIGGER:** legolas-1 ships completion record. Knight-rider spawns this commission then.
- **Parallel-safe with elrond curation:** different scopes; legolas-2 surveys broader landscape while elrond curates legolas-1's category-specific output. Both run after legolas-1 lands.
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3. ~1-2 days when activated. Append completion record when done.*

---

## Completion Record

**Completed:** 2026-05-17 by legolas
**Status:** COMPLETE
**Output:** `agentic_orchestration/research/catalogue/2d-sprite-vendors-genre-survey-2026-05-17/vendors.jsonl`

### Summary

- **30 vendors surveyed** across itch.io, CraftPix, OpenGameArt, GameDev Market
- **register_fit:** STRONG 5 | PARTIAL 21 | WEAK 4
- **Acceptance criteria:** all met

### Top 5 STRONG-Fit Vendors

| Rank | Vendor | Why STRONG |
|---|---|---|
| 1 | CraftPix | Broadest catalogue (2100+ assets); $4/mo membership; character/monster/tileset/VFX/UI all covered; commercial license no attribution |
| 2 | CreativeKind | ACQUIRED; hand-drawn-pixel register — strongest style match to locked HD-2D register; boss-class animated sprites (Fire Lord, God of Lightning, Angel Guardian); 25+ character/enemy packs |
| 3 | Pimen | ACQUIRED; VFX-only; hand-drawn-pixel sub-register; Tier-1 spell substrate coverage |
| 4 | Frostwindz | ACQUIRED; hand-drawn-pixel VFX; death/blood/cosmic substrates unique in catalogue |
| 5 | Elthen | 400+ packs; widest enemy/monster variety on itch.io; top-down confirmed; character + tileset + VFX |

### Category Coverage Gaps

1. **Hand-drawn-pixel character sprites (PC class + NPC):** No strong vendor other than CreativeKind. Most character vendors are retro-pixel or JRPG-oriented.
2. **Top-down 8-directional ARPG enemy animations at HD-2D fidelity:** Gap. Penusbmic DARK series is closest aesthetically but retro-pixel register.
3. **ARPG dark-fantasy HUD/UI in hand-drawn-pixel register:** Partial coverage (IndigoLay, CraftPix) — no vendor ships Diablo-chrome HUD in hand-drawn-pixel.
4. **Boss-class animated sprites matching hand-drawn-pixel register:** Only CreativeKind. Major gap for ARPG boss gallery build-out.
5. **Atmospheric mood overlays:** Alenia Studios (CC-BY, 20 effects) uniquely fills this niche — no competing vendor.

### Cost Intelligence Rollup

| Tier | Vendors | Pack Price Range | Notes |
|---|---|---|---|
| Premium all-access | CraftPix | $4/mo annual ($48/yr) | Unlocks 2100+ assets; perpetual license on downloads |
| Premium per-pack | CreativeKind, Frostwindz | $2.70–$9 | Hand-drawn-pixel register; best style match |
| Mid-market | Penusbmic, ELV Games, finalbossblues, Elthen, DithArt | $3–$15/pack | Dark-fantasy genre fit; retro-pixel register |
| Budget itch.io | ansimuz, LuizMelo, Szadi Art, Admurin, kiddolink | $1–$6/pack | High volume; variable quality; retro-pixel |
| Free commercial | Kenney (CC0), brullov (all free), OGA CC0 picks, Anokolisa free | $0 | Floor coverage; retro-pixel register |
| Bundle value | ELV Rogue Adventure World | $31.99 for 10 biome tilesets | Best dungeon-tileset bundle value |

### Opportunity Flags (Matt-authority acquisition decisions)

1. **Penusbmic DARK Series complete bundle** — 40+ packs with code PENUSBMIC (30% off); Diablo dark-gothic aesthetic; professionally credentialed (Dome Keeper, Shogun Showdown); $4.49/pack individual — best dark-ARPG aesthetic genre fit outside acquired vendors
2. **ELV Rogue Adventure World $31.99** — 10 dungeon biome tilesets explicitly Diablo/Dark Souls-inspired; attribution required; broadest dungeon-environment coverage per dollar
3. **Szadi Art RPG Worlds** — 14 biome tilesets at $3-6 each; most permissive license in survey (derivative resale allowed); clean 32x32 top-down pixel art
4. **Alenia Studios atmospheric VFX** — 20 mood overlays (god rays/snow/rain/fireflies/fog/aurora etc.) PWYW free + CC-BY; unique atmospheric niche; 48-frame seamless loops; no competing vendor found
5. **Admurin Top Down Monsters Mega Pack** — $15 for 150+ animated top-down monsters; best enemy volume value; license unverified (must check before acquisition)

### Cross-References

- Style register: `canonical/story/style-register.md` (locked HD-2D hand-drawn pixel; Candidate B)
- Mobile sizing canon: `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (gandalf v1.7)
- Design frame: `canonical/29-design-overview.md` (ARPG/Isekai genre; Diablo-style single-camera room/hallway)
- Step B Tier-1 baseline: `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md`
- Acquired assets: `reincarnated-demo/public/assets/` (CreativeKind, Frostwindz/Deathbringer, Pimen, chierit, GandalfHardcore Samurai, Impact FX/CodeManu, PixelArtRPGVFXLite)
- Legolas-1 predecessor: `agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/summary.md`
