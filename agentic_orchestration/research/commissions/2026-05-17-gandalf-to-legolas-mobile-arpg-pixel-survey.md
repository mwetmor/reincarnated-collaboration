# 2026-05-17 — gandalf → legolas — Mobile ARPG Pixel Sizing Survey (Mode B enrichment)

**Authority:** Pre-authorized by knight-rider per the gandalf mobile-pixel commission dispatch (`2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md` § "Legolas sub-commission authorization"). Sub-commission scope: web-crawl enrichment of 4 mobile-ARPG titles where gandalf's offline Maiar-knowledge is sparse.
**Type:** Legolas Mode B (web-crawl analytical research; no engine modifications).
**Priority:** Enrichment pass (not blocking). Gandalf's v1.7 canon at `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` is shipped from a 4-anchor solid-knowledge cluster (Diablo Immortal / Torchlight Infinite / Eternium / Diablo III Switch port). This sub-commission tightens the cluster by adding 4 titles to the survey base.
**Estimated effort:** 6-12 hours web-crawl + measurement notes.
**Output destination:** `agentic_orchestration/research/2026-05-17-mobile-arpg-pixel-sizing-survey/` (per-title sub-directories).
**Consumer:** gandalf — reviews findings; folds into v1.7b refinement of the canonical doc if material deviations (>±15% from 4-anchor cluster centroid for any value) emerge.

---

## § 1 — Why this sub-commission exists

Gandalf's offline Maiar-knowledge anchors the cluster centroid on 4 titles (DI / Torchlight / Eternium / D3 Switch). The dispatch's named survey list includes 4 more titles where gandalf's offline knowledge is partial-to-sparse:

- **Anima ARPG** — gandalf-knowledge sparse
- **Oniro ARPG** — gandalf-knowledge sparse
- **Dungeon of Exile** — gandalf-knowledge sparse (Matt highlight: *"this is a good one"* — high-priority comparison)
- **Dungeon Hunter 6** — gandalf-knowledge partial (franchise design language known; current-build specifics unconfirmed)

These titles could either confirm the 4-anchor cluster (table stays as authored), or shift the cluster (table gets a v1.7b refinement). Cannot tell which without empirical data.

**Why not block on this:** the dispatch is forward-looking (VS2b territory; not VS2a-gating). The 4-anchor cluster is already implementable for drax's eventual mobile dispatch. Enrichment is high-value but optional.

---

## § 2 — Per-title scope

For each of the 4 titles below, capture (at 1080p-mobile-equivalent reference, with screenshots / video references):

| Object | Note |
|---|---|
| Player sprite height (px) | At default zoom; representative still frame mid-combat |
| Trash monster height (px) | Representative typical-pack mob |
| Elite / champion monster height (px) | Where present |
| Boss height (px) | In-zone boss; not raid-tier world boss |
| Ability button diameter (px) | Single core ability slot in default hotbar |
| Ultimate / signature ability button (px) | Where structurally distinct from core abilities |
| Potion / consumable button (px) | HP-potion equivalent |
| Joystick outer ring (px) | Movement joystick if present |
| Joystick inner thumb (px) | Movement thumb if present |
| Tile / floor texture repeat (px) | Where pixel-cell-bound; note "atlas-based" if not |
| Gear drop sprite (px) | Sword / staff / armor piece on floor |
| Currency / gold pile (px) | Floor-display |
| Treasure chest — small (px) | Common rarity |
| Treasure chest — large / legendary (px) | Rare-spawn rarity |
| Destructible: vase / urn (px) | Per title's biome variants |
| Destructible: barrel / crate (px) | Per title's biome variants |
| Tap-target affordance ring (yes / no + sizing) | Glow-outline when in-range of interactable |
| Loot beam / name-plate auto-display (pattern) | Rarity coloring + persistence |

### § 2.1 — Anima ARPG

**Maiar context:** Reportedly Diablo-clone-style mobile ARPG; indie publisher pattern (DragonArmy or similar). Likely sits inside the Immortal cluster (3D rendered, conventional ARPG UI) but may represent a distinct indie sub-cluster (smaller sprites, larger UI panels for low-fidelity hardware).

**Specific flags to watch for:**
- Whether Anima sits at the cluster centroid (~100 px player) or in a low-fidelity indie sub-cluster (~75-85 px player)
- Whether UI elements are oversized (smaller sprites + bigger buttons; the *legacy mobile ARPG* anti-pattern)
- Whether art register is rendered-3D or stylized-2D (relevant to our HD-2D pixel-art register applicability)

### § 2.2 — Oniro ARPG

**Maiar context:** Mobile-first indie ARPG with possibly-stylized art direction (Eastward-adjacent? Or conventional Diablo-clone?). Knowledge sparse.

**Specific flags:**
- Art register — if Oniro is HD-2D-shaped / hand-drawn-pixel (i.e., **closer to our locked register**), the sizing data is **highest-priority Reincarnated-applicable**
- Whether Oniro uses standard radial-arc ability layout or experiments with alternative HUD patterns
- Player-sprite size relative to cluster centroid

### § 2.3 — Dungeon of Exile (Matt high-priority)

**Maiar context:** Likely PoE-adjacent indie mobile ARPG (name pattern deliberately positions against Path of Exile). Matt flagged this title as "a good one." Knowledge sparse — likely a niche / smaller-installed-base title that Matt has played and found notable.

**Specific flags:**
- **Match Matt's quality signal** — Dungeon of Exile may be the implicit benchmark for "what Reincarnated mobile should feel like." Capture sizing data with extra detail; flag any patterns that distinguish DoE from DI/Torchlight (sub-cluster identity).
- Whether DoE leans more PC-port-feel or more mobile-native-feel (relevant to our PC-derived demo1 → mobile transformation pattern)
- Specific UI elements DoE handles unusually well (Matt's "good one" judgment is likely anchored to a specific quality signal)

### § 2.4 — Dungeon Hunter 6 (Gameloft, 2023)

**Maiar context:** Gameloft franchise continuation; console-derived ARPG UI conventions. Knowledge partial — franchise design language known; DH6-specific current-build values unconfirmed.

**Specific flags:**
- Whether DH6 sits in the Immortal cluster or in a Gameloft sub-cluster (historically Gameloft has used slightly heavier ability buttons and more text-density)
- 2025+ patch state if recent updates have shifted UI sizing
- Player:monster ratio (Gameloft historically uses slightly *larger* enemies than Blizzard's Immortal)

---

## § 3 — Sources Legolas should prefer

In rough order of pixel-fidelity (highest first):

1. **Official vendor App Store screenshots** (App Store + Google Play hero shots). Highest fidelity; captures the vendor's chosen "presentation" frame.
2. **Official YouTube trailers + gameplay reveals** (vendor-uploaded). 1080p+ frames; recent (2024-2025) preferred.
3. **GameingOnPhone / Pocket Gamer / Touch Arcade screenshot galleries.** Curated mobile-game review sites; reliable resolution.
4. **r/<title> subreddit screenshot threads** (e.g., r/DiabloImmortal). Player-uploaded; resolution varies but provides real-play context (vs vendor-staged hero shots).
5. **MMO-related sites (MMORPG.com, ArkesGames, IGN mobile section).** Editorial screenshots with measurements sometimes called out.
6. **YouTube gameplay videos by mobile-ARPG content creators** (e.g., Wolf4hire, Echohack, Maxroll-mobile). Recent gameplay at 1080p+.

**Avoid:** in-game emulator captures (DPI ratios distorted); old (pre-2023) screenshots (UI may have shifted); third-party "tier list" articles (image quality often degraded).

---

## § 4 — Output format

Per title, in `agentic_orchestration/research/2026-05-17-mobile-arpg-pixel-sizing-survey/<title-slug>/`:

```
<title-slug>/
  README.md          — measurement notes + per-object sizing table + cluster-fit analysis
  screenshots/       — 3-5 reference screenshots used for measurements
  citations.md       — URL list with capture timestamps + permalinks
```

**README.md template per title:**

```markdown
# <Title> — Mobile ARPG Pixel Sizing Survey

**Capture date:** YYYY-MM-DD
**Build / version sampled:** <patch version if known>
**Reference resolution:** 1080p mobile-equivalent (or note actual)

## Per-object sizing

| Object | Pixel size | Ratio to player | Notes |
|---|---|---|---|
| Player sprite | ~X px tall | 1.0 | |
| Trash monster | ~X px | ~X | |
| ... | | | |

## Cluster-fit analysis

- Player sprite vs gandalf 4-anchor centroid (~100 px): [WITHIN / ABOVE / BELOW] by X%
- Ability button vs centroid (115 px): [WITHIN / ABOVE / BELOW] by X%
- Notable deviations: [list]
- Sub-cluster identity (if any): [conventional Immortal-cluster / indie low-fidelity / HD-stylized / other]

## Matt-applicability flags

- Whether this title's design feel maps to Reincarnated's HD-2D pixel-art locked register
- Specific UI patterns worth Matt's awareness
- Quality signal (for Dungeon of Exile specifically, given Matt's "good one" framing)
```

---

## § 5 — Acceptance criteria

- [ ] Per-title sub-directory exists at `agentic_orchestration/research/2026-05-17-mobile-arpg-pixel-sizing-survey/`
- [ ] 4 README.md files (one per title) with per-object sizing tables
- [ ] 3-5 reference screenshots per title
- [ ] Citations file per title with URLs + capture timestamps
- [ ] Cluster-fit analysis section per title (within/above/below gandalf centroid)
- [ ] Summary document at survey root: which titles confirm cluster vs which shift it; suggested gandalf v1.7b refinements if any

---

## § 6 — Consumption pattern (gandalf side)

When legolas surfaces completion:

1. Gandalf reviews each title's cluster-fit analysis
2. If all 4 titles fall within ±10% of 4-anchor centroid: file "cluster confirmed" note; canon v1.7 stays as authoritative; no doc revision
3. If 1-2 titles deviate >±15% on specific values: file "selective refinement" note; gandalf authors v1.7b with adjusted table rows; tag `gandalf/v1.7b-mobile-pc-pixel-sizing-ratios-refined`
4. If 3-4 titles deviate >±15% systemically: re-examine 4-anchor cluster (one anchor may be the outlier, not the survey); possible v1.8 with reset centroid

**Most likely outcome:** scenario (2) — cluster confirmed. Genre canon is mature; mobile-ARPG sizing converged 2022-2025; outlier titles are rare. Sub-commission is high-value-but-likely-confirmatory.

---

*Filed 2026-05-17 by gandalf per pre-authorization in the originating dispatch. Enrichment pass; not blocking. Legolas: take your time on this one — quality of measurement > speed of return. — gandalf*
