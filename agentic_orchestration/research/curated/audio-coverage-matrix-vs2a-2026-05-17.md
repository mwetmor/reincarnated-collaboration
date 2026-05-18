# Audio Coverage Matrix — Post-Curation VS2a (2026-05-17)

**Steward:** elrond | **Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-audio-pack-curation-queued.md` | **Canon:** `canonical/story/audio-register-canon-2026-05-17.md` (gandalf, 2026-05-17)

This matrix is the POST-CURATION coverage view: legolas-4's raw matrix (`audio-vendors-2026-05-17/coverage-matrix.md`) filtered through gandalf's register canon § 2.1 cluster-lock (Cluster A skill SFX + Cluster C ambient + Cluster B music + Cluster D UI). RED cells reflect register-filtered gaps; WEAK-fit vendors are excluded per gandalf canon authoring discipline.

**Key:**
- GREEN — shortlist has acquireable Cluster-A-or-canon-fit asset
- YELLOW — shortlist asset has caveat (Tier 2 cost / composite construction / register-attention-zone)
- RED — no acquireable asset; commission or canon-recipe construction required

**Post-fetch ground-truth update 2026-05-17 19:45Z:** legolas Tier-1 fetch SHIPPED with 6 of 8 packs ON-DISK (Kenney, OGA, Leohpaz x2, TomMusic). Two packs FLAGGED-NOT-STAGED requiring Matt manual fetch: kmontesdev (Google-Drive folder, browser+Google-login required) + PixelLoops ($3.59 spend pre-authorized BUT itch.io account credentials not stored). This shifts Layer-4 ambient coverage from 6 GREEN / 2 YELLOW-constructible to 1 GREEN / 7 YELLOW-blocked-on-Matt-fetch (TomMusic provides forest GREEN; all other biomes need PixelLoops primary OR kmontesdev fallback). Coverage section 4 reflects updated status.

**Sonic-register filter applied:**
- Skill SFX (Layer 1): Cluster A only at primary; Cluster D foley under
- Foley (Layer 3): Cluster D primary + Cluster A foley underlayers
- Ambient (Layer 4): Cluster C HD-cinematic primary; mid-fi tolerated
- Music (Layer 5): Cluster B mid-fi orchestral-synth only
- UI (Layer outside-stack): Cluster D minimal/generic + thin Cluster A rarity-chime accents

---

## Section 1 — Skill SFX (Layer 1 substrate × archetype-group × element)

Per canon § 4.6: 72 sonic slots (9 archetype groups × 8 elements). Geometry-types-sharing-sonic-signature collapse to archetype groups (G1-G9 per legolas-4 coverage-matrix § 1).

| Element \ Group | G1 PROJECTILE | G2 MELEE | G3 SINGLE-TARGET | G4 AREA | G5 BEAM | G6 MOVEMENT | G7 AURA | G8 SLAM | G9 BUFF |
|---|---|---|---|---|---|---|---|---|---|
| **fire** | GREEN — WSP (T2 $49) + Leohpaz T1 free | YELLOW — Leohpaz combat-foley + WSP cast-layer composite | GREEN — WSP + Leohpaz fallback | GREEN — WSP + Leohpaz | GREEN — WSP fire-beam variant | YELLOW — WSP wind reuse cross-element | GREEN — WSP fire aura loop | YELLOW — WSP-earth-slam + WS3 fire-impact composite | GREEN — Leohpaz buff + WSP cast |
| **water** | GREEN — WSP (T2; 4-file thin but workable) + WS3 ice variant if T2 | YELLOW — Leohpaz combat + WSP cast composite | GREEN — WSP water-cast | YELLOW — WSP + composite for AOE-water | YELLOW — WSP water-beam if present; else WS3 T2 | YELLOW — WSP wind cross-route | YELLOW — WSP water sparse for sustained aura | RED — water+slam: composite per canon § 4.6 (WS3 water + WSP earth-slam underlay) | YELLOW — Leohpaz heal-status |
| **earth** | YELLOW — WSP earth 6-file thin; Leohpaz fallback | YELLOW — composite from foley + WSP cast | YELLOW — WSP earth + Leohpaz | GREEN — WSP earth ground AoE strong | RED — earth+beam: composite per coverage-matrix § Summary (WS3 earth + FH stone-atmosphere if T2) | YELLOW — WSP wind reuse | YELLOW — WSP earth-hum | GREEN — WSP earth-slam primary | YELLOW — Leohpaz status |
| **wind** | GREEN — WSP wind 21-file rich | YELLOW — composite | GREEN — WSP wind-cast | GREEN — WSP wind AoE | YELLOW — WSP wind-beam if present | GREEN — WSP wind = G6 displacement primary | YELLOW — WSP wind sustained | YELLOW — composite | YELLOW — WSP wind-buff |
| **lightning** | GREEN — WSP electric 17-file | YELLOW — composite | GREEN — WSP electric chain | GREEN — WSP electric-storm AoE | GREEN — WSP electric beam | YELLOW — WSP electric discharge | GREEN — WSP electric aura | YELLOW — composite | YELLOW — WSP electric buff |
| **holy** | YELLOW — REGISTER-ATTENTION-ZONE (canon § 3.2) — WSP Light composite + Kenney bell-chime T1 ON-DISK + pitch-shift recipe | YELLOW — composite | YELLOW — composite | YELLOW — composite | YELLOW — WSP Light-beam composite | YELLOW — composite | YELLOW — WSP Light aura composite | RED — holy+slam: composite per coverage-matrix § Summary (FH divine-impact + WS3 earth-slam if T2) | GREEN — Leohpaz heal + WSP buff |
| **shadow** | GREEN — WSP dark 34-file (largest single-element WSP allocation) | YELLOW — composite | GREEN — WSP dark-cast | GREEN — WSP dark explosion | GREEN — WSP dark-beam | YELLOW — WSP dark-teleport | GREEN — WSP dark aura | YELLOW — WSP-dark + earth-slam composite | YELLOW — Leohpaz debuff |
| **physical** | GREEN — Kenney Impact T1 ON-DISK + OGA sword/swing | GREEN — Leohpaz Dungeon (FETCH-IN-FLIGHT) + Kenney Impact + OGA sword | YELLOW — Kenney + Leohpaz | YELLOW — Kenney Impact + composite | RED — physical+beam: composite (Kenney + WS1 impacts if T2) | YELLOW — Leohpaz dash + OGA swing | RED — physical+aura: composite (Kenney + generic tone) | GREEN — Kenney Impact ground hits + Leohpaz Dungeon | YELLOW — Kenney + Leohpaz status |

### RED-cell summary — Layer 1 skill SFX

5 RED cells; all constructible per canon § 4.6 + coverage-matrix § Summary:

| Slot | Composite recipe | Source-pack tier prerequisites |
|---|---|---|
| **water+slam** (G8.water) | WSP earth-slam (-6dB base) + WS3 water-impact (overlay) + 300ms reverb tail | T2 WS3 ($99) ideal; T1-only fallback uses WSP water-impact at reduced fidelity |
| **earth+beam** (G5.earth) | WS3 earth + FH stone-atmosphere overlay | T2 WS3 ($99) + FH ($100) ideal; T1-only fallback uses WSP earth-sustained at thin fidelity |
| **holy+slam** (G8.holy) | FH divine-impact + WS3 earth-slam (cross-cluster composite — register-attention zone) | T2 WS3 ($99) + FH ($100); T1-only fallback uses Kenney bell-chime + WSP earth-slam |
| **physical+beam** (G5.physical) | Kenney Impact + WS1 impacts (sustained loop construction) | T2 WS1 ($35) helpful; T1-only fallback Kenney + tone-stack |
| **physical+aura** (G7.physical) | Kenney Impact + generic tone-layer (sustained loop) | T1-only fallback usable; quality acceptable |

**Post-curation RED-cell count:** 5 (same as legolas-4 raw matrix — register-filter does not introduce new RED cells; composite recipes preserved).

### YELLOW cells — primary register concerns

- All G2 MELEE × element-non-physical cells are YELLOW because Cluster A retro-pixel packs label spell cast/impact but NOT element-melee. Construction: layer Layer-1 cast + Layer-3 Kenney/Leohpaz physical-impact-foley. Genre-canon (Octopath Traveler / FFVI spell-cast + sword-hit composition).
- Holy element across ALL groups is YELLOW per canon § 3.2 register-attention zone. Composite construction (WSP Light + Kenney bell-chime + pitch-shift) is the canonical resolution.

---

## Section 2 — UI Events (Layer outside-stack)

Per canon § 4.3 + § 2.1: UI register is Cluster D minimal/generic deliberately (NOT Cluster A retro-pixel — would fatigue). Thin Cluster A accents at rarity-tier chimes only.

| UI Event | Status | Candidate vendors (post-canon-filter) |
|---|---|---|
| button-click | GREEN | Kenney Interface T1 ON-DISK (CC0; correct Cluster D register) |
| menu-open | GREEN | Kenney Interface T1 ON-DISK + Leohpaz Retro RPG UI Tier 1.5 ($3.49) if Matt approves |
| menu-close | GREEN | Same |
| inventory-open | GREEN | Leohpaz RPG Essentials T1 (FETCH-IN-FLIGHT) |
| equip | GREEN | Leohpaz RPG Essentials T1 + Leohpaz Retro RPG UI Tier 1.5 |
| drop (item drop) | YELLOW | Leohpaz RPG Essentials T1 partial; Kenney drop_*.ogg variants ON-DISK as fallback |
| chest-open | YELLOW | TomMusic T1 (FETCH-IN-FLIGHT) + Leohpaz Dungeon T1 (FETCH-IN-FLIGHT) |
| pot-break | YELLOW | TomMusic foley partial; Kenney impactGlass_*.ogg ON-DISK as fallback |
| loot-pickup (chime) | GREEN | Leohpaz RPG Essentials T1 + OGA RPG Sound Pack T1 ON-DISK |
| level-up | GREEN | Leohpaz RPG Essentials T1 |
| error | YELLOW | Leohpaz RPG Essentials T1 + Kenney error_*.ogg ON-DISK (Cluster D; not fantasy-coded — fine per canon § 2.1) |
| dash / dodge-iframe-pulse | YELLOW | Leohpaz Dungeon dash + WSP wind-displacement (T2) for elemental iframe-pulse |
| loot-rarity-tier chime (common/rare/epic/legendary) | YELLOW | OGA Fantasy SFX jingles + Leohpaz 16-bit achievement — per canon § 2.1 thin Cluster A accents acceptable here only |

**RED UI events:** none after register filter — Cluster D placeholder-grade is CORRECT per canon § 2.1 lock.

---

## Section 3 — Death Tiers

Death tiers carry dramaturgical weight per canon § 4.4 ritual-canonical-silence anchor and per `passage-moment-ritual.md` coupling.

| Tier | Status | Candidate vendors (post-canon-filter) |
|---|---|---|
| trash (common enemy death) | GREEN | Leohpaz RPG Essentials T1 (enemy death confirmed) + OGA RPG Sound Pack T1 ON-DISK + Leohpaz Dungeon |
| elite (powerful enemy death) | YELLOW | Leohpaz Elemental Creatures Tier 1.5 ($2.49) + composite (Layer-1 elemental impact + Layer-3 Kenney heavy-impact) |
| boss (act boss death) | YELLOW | Composite construction: WS1 layered impact (T2 $35) + FH dark/lava impacts (T2 $100) OR T1-only composite from Kenney + ritual stinger |
| player (player death) | YELLOW | Composite: Leohpaz RPG Essentials partial + Layer-7 ritual stinger (custom construction; canon § 4.4 ritual register) |

**RED death tiers:** none strictly RED. Boss + player-death YELLOW per coverage-matrix § 3 dramaturgical-weight note. Per canon § 4.4 these route to Layer 7 ritual stinger bus with 4.0s frequency cap.

---

## Section 4 — Ambient Biomes (Layer 4)

Per canon § 4.5 biome thematic mapping. Cluster C HD-cinematic preferred; PixelLoops $3.59 mid-fi-tolerated is VS2a pipeline-unblocker.

| Biome | Status | Candidate vendors (post-canon-filter) |
|---|---|---|
| dungeon | YELLOW (PixelLoops PENDING-MATT-FETCH) | PixelLoops T1 ($3.59 FLAGGED-NOT-STAGED — Matt itch.io purchase required per legolas Tier-1 FLAG 2) + TomMusic T1 ambient ON-DISK + kmontesdev FLAGGED-NOT-STAGED (Matt Google-Drive fetch FLAG 1) — TomMusic-only fallback workable but reduced fidelity |
| cave | YELLOW (PixelLoops PENDING-MATT-FETCH) | Same vendor list; PixelLoops primary blocked; TomMusic fallback ON-DISK |
| swamp | YELLOW (PixelLoops PENDING-MATT-FETCH) | PixelLoops primary blocked Matt-fetch; no TomMusic swamp explicit |
| ruined-temple | YELLOW (PixelLoops PENDING-MATT-FETCH) | PixelLoops primary blocked Matt-fetch |
| forest | GREEN | TomMusic T1 ambient ON-DISK + PixelLoops PENDING-MATT-FETCH (upgrade path) |
| desert | YELLOW (PixelLoops PENDING-MATT-FETCH) | PixelLoops primary blocked Matt-fetch |
| glowing-cave | YELLOW (CONSTRUCTIBLE — BLOCKED on PixelLoops) | Composite: PixelLoops cave base + magic/temple overlay (recipe in atmospheric manifest row layer4.glowing-cave-composite); BLOCKED on PixelLoops Matt-manual-fetch; Tier-2 David Dumais lava+underwater premium alternative |
| sewer | YELLOW (CONSTRUCTIBLE — PARTIAL) | Composite: PixelLoops cave + Sea/River overlay (PixelLoops blocked Matt-fetch); TomMusic-river-only partial composite available at reduced fidelity; Tier-2 David Dumais tar/mud premium alternative |

**RED biomes:** none. All 8 canon-named biomes GREEN or YELLOW-constructible from Tier-1.

---

## Section 5 — Music (Layer 5; per-season)

Per canon § 7 music gap pragmatic recommendation.

| Slot | Status | Notes |
|---|---|---|
| 001001-005 (existing on-disk) | GREEN | 5 mp3 tracks already wired; PARKED-MATT Suno license clarification |
| 002011-015 (D10 silent gap) | YELLOW (PARKED-MATT-DECISION) | Canon § 7.3 recommends Option B Suno Pro ($10/mo while generating); immediate-unblock fallback Option A rotation; demo-ship-readiness Option D Bit By Bit Sound ($77.60 PARKED Q-MATT-3) |
| Future seasons (002016+) | YELLOW | Same path as 002011-015 — Q-MATT-2 decision determines |

**RED music slots:** 002011-015 are currently silent fallback in production, so functionally RED at runtime; canon § 7 establishes 4 resolution paths (A/B/D primary + C/E rejected). PARKED-MATT decision space.

---

## Section 6 — Ritual stingers (Layer 7) + Voice (Layer 6 forward-flag)

| Layer | Slot | Status | Notes |
|---|---|---|---|
| Layer 7 ritual stinger | Trial moment | YELLOW | Composite from Cluster A ritual transients (WSP buffs + Kenney impact) — drax wiring time |
| Layer 7 ritual stinger | Passage moment | YELLOW | Per canon § 4.4 canonical-silence active during Passage phases 2-4 — STINGER ONLY at phase boundaries; rest is silence |
| Layer 7 ritual stinger | Ascension moment | YELLOW | Composite |
| Layer 6 voice (Spirit Guide) | All Spirit Guide lines | FORWARD-FLAG | Per canon § 8: Phase-1 mid-cycle future-dispatch; register Cluster B-adjacent intimate close-mic; not VS2a scope |

---

## Section 7 — Summary metrics

| Layer | Total slots | GREEN (post-curation) | YELLOW | RED |
|---|---:|---:|---:|---:|
| Layer 1 skill SFX | 72 (9 archetypes × 8 elements) | ~28 | ~39 | 5 (all constructible) |
| Layer 3 foley | ~10 (slot variants) | ~7 | ~3 | 0 |
| UI events | 13 | 7 | 6 | 0 |
| Death tiers | 4 | 1 | 3 | 0 |
| Layer 4 ambient biomes | 8 | 1 (forest TomMusic ON-DISK) | 7 (PixelLoops Matt-fetch BLOCKED for primary; TomMusic fallback partial) | 0 |
| Layer 5 music | 3 segments | 1 (existing tracks) | 2 (PARKED-MATT) | 1 currently silent (002011-015 — PARKED) |
| Layer 7 ritual stingers | 3 moments | 0 | 3 (composite) | 0 |
| Layer 6 voice | N/A (forward-flag) | N/A | N/A | N/A |

**Per canon § 4.6:** all 5 RED Layer-1 cells constructible from available YELLOW-or-better vendors via layer composition. **No bespoke commission required at VS2a.** Composite recipes documented in substrate + atmospheric manifest rows + this matrix § 1 RED-cell-summary.

---

## Section 8 — Register-coherence audit recommendations

Per canon § 2.5 score-don't-filter principle: WEAK-register-fit vendors excluded at this manifest authoring; MODERATE-fit vendors flagged for integration-time audition vs STRONG-fit acquisitions.

Integration-time gate items (drax wiring dispatch should verify):

1. **Little Robot Fantasy SFX (CC-BY)** — kept in Layer-1 manifest at MODERATE rating; canon § 2.2 register placement is Cluster B-adjacent. If WSP acquired (Tier 2 $49), Little Robot becomes redundant or relegated to Layer-3 underlayer support. If WSP NOT acquired, Little Robot is a CC-BY-attribution Layer-1 spell-supplement fallback.
2. **TomMusic Fantasy 200 at Layer-1 routing** — only for water G2/G3 where WSP+Leohpaz both thin. Primary TomMusic value is Layer-3 foley + Layer-4 ambient.
3. **kmontesdev 2GB pack** — per-file register audit required post-extraction. CC0 license enables liberal use; per-file Cluster A/D vs Cluster C routing decision deferred to drax wiring.
4. **Holy register-attention zone** — Q-MATT-5 PARKED. Composite Path 1 default. Drax wiring produces composite at integration. Playtest signal may escalate to Path 2 register-mismatch-acceptance or Path 3 commission.

---

*Coverage matrix authored 2026-05-17 by elrond per audio-pack-curation dispatch. Companion to per-layer subset manifests at `audio-{substrate,class-archetype,foley,atmospheric,music}-subset-vs2a-2026-05-17.jsonl`. Canon-filter applied per gandalf canon § 2.1 cluster lock. 5 Layer-1 RED cells constructible per § 4.6 + § Summary recipes — no bespoke commission required at VS2a.*
