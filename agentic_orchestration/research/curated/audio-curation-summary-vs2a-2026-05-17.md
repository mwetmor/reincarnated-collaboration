# Audio Curation Summary — VS2a (2026-05-17)

**Steward:** elrond | **Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-audio-pack-curation-queued.md` | **Canon:** `canonical/story/audio-register-canon-2026-05-17.md` (gandalf 2026-05-17) | **Legolas catalogue:** `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/`

**Post-fetch ground-truth update 2026-05-17 19:45Z:** legolas Tier-1 fetch SHIPPED 6 of 8 packs ON-DISK. Two packs FLAGGED-NOT-STAGED per legolas Tier-1 completion record: kmontesdev (2GB Google-Drive folder, browser+Google-login required) + PixelLoops ($3.59 spend pre-authorized but itch.io credentials not stored). This curation manifests reflect actual on-disk ground-truth + flag the two Matt-manual-fetch items as NEW Q-MATT-AUDIO-4 below.

## 1. Executive summary

Five per-layer subset manifests (one JSONL per gandalf canonical audio layer) + a coverage matrix + an acquisition shortlist now compress the legolas-4 raw audio catalogue (35 packs / 18 vendors / 4 sonic clusters) into Reincarnated's actionable curation surface under gandalf's HYBRID-cluster lock. The cluster lock is Cluster A retro-pixel for skill SFX, Cluster C HD-cinematic for ambient, Cluster B mid-fi orchestral-synth for music, Cluster D minimal/generic for UI — same hybrid logic as the visual register's HYBRID a3 lock.

The headline finding: **Matt's already-authorized Tier-1 acquisition (~$3.59 + 7 free packs, in flight via legolas) unblocks the pipeline at VS2a but leaves the canonical Cluster A spell-SFX layer under-covered.** The single highest-leverage extension is WSP (WOW Sound Pixel Magic SFX Pack, $49) — closes 7 of 8 elements at the canonical Cluster A retro-pixel register. This is flagged as **Q-MATT-AUDIO-1 IMMEDIATE-FOR-VS2a**. All 5 Layer-1 RED cells (water+slam, earth+beam, holy+slam, physical+beam, physical+aura) are constructible from available Tier-1 + WSP composite recipes; no bespoke commission required.

The D10 music gap (seasons 002011-015 currently silent) is a Matt-pending decision (Q-MATT-2) per gandalf canon § 7. Recommended path: Option A rotation fallback wires NOW as immediate playtest unblocker; Option B Suno Pro per-season generation against canonical retro-JRPG anchor prompt is the primary path (PARKED on game-embedded-clause clarification per § 7.4); Option D Bit By Bit Sound ($77.60 PARKED Q-MATT-3) is the pre-demo-ship attribution-clear alternative.

Holy element is the register-attention zone per canon § 3.2 — no explicit retro-register holy pack exists, but the composite recipe (WSP/WS3 Light at base + Kenney bell-chime ON-DISK transient + pitch-shift to retro-band) is documented in the substrate + foley manifests as drax-wiring-time composite construction. Q-MATT-5 PARKED-default: elrond proceeds Path 1 composite construction unless playtest flags audio-mismatch.

The whole curation respects gandalf's discipline locks: same-file SFX rendering (player vs enemy via mix-bus only, NOT paired files); ~72-slot enumeration via archetype-group reduction (vs 192-cell theoretical matrix); per-layer LUFS targets documented in manifest metadata; license-unclear assets excluded; WEAK sonic-register fits filtered out (only STRONG + MODERATE-with-flag survive curation).

## 2. Layered manifest reference

| Layer | Manifest path | Active rows | Status |
|---|---|---:|---|
| 1 — substrate SFX | `agentic_orchestration/research/curated/audio-substrate-subset-vs2a-2026-05-17.jsonl` | 14 | Cluster A skill SFX + Layer-1 composites |
| 2 — class-archetype SFX | `agentic_orchestration/research/curated/audio-class-archetype-subset-vs2a-2026-05-17.jsonl` | 1 (forward-flag only) | Phase-2 deferred per canon § 4.7 |
| 3 — physical / foley | `agentic_orchestration/research/curated/audio-foley-subset-vs2a-2026-05-17.jsonl` | 7 | Cluster D Kenney + Cluster A foley |
| 4 — atmospheric | `agentic_orchestration/research/curated/audio-atmospheric-subset-vs2a-2026-05-17.jsonl` | 5 | PixelLoops + composites for glowing-cave/sewer |
| 5 — music | `agentic_orchestration/research/curated/audio-music-subset-vs2a-2026-05-17.jsonl` | 5 | Existing 001001-005 + Suno/Option-A/Option-D PARKED-MATT |

Coverage matrix: `agentic_orchestration/research/curated/audio-coverage-matrix-vs2a-2026-05-17.md`
Acquisition shortlist (3-path cost ladder): `agentic_orchestration/research/curated/audio-acquisition-shortlist-vs2a-2026-05-17.md`

Total active rows across 5 layers: **32** (14 + 1 + 7 + 5 + 5)

## 3. Coverage gap snapshot

Per the coverage matrix § 7 summary metrics:

| Layer | GREEN | YELLOW | RED |
|---|---:|---:|---:|
| Layer 1 skill SFX (72 slots) | ~28 | ~39 | 5 (all constructible) |
| Layer 3 foley (~10 slot variants) | ~7 | ~3 | 0 |
| UI events (13) | 7 | 6 | 0 |
| Death tiers (4) | 1 | 3 | 0 |
| Layer 4 ambient biomes (8) | 1 (forest TomMusic ON-DISK) | 7 (PixelLoops + kmontesdev Matt-manual-fetch BLOCKED for primary coverage) | 0 |
| Layer 5 music (3 segments) | 1 | 2 (PARKED-MATT) | 1 currently silent (002011-015 PARKED) |
| Layer 7 ritual stingers (3) | 0 | 3 (composite) | 0 |
| Layer 6 voice | N/A | N/A | N/A (forward-flag) |

**5 Layer-1 RED cells composite-resolution status:** all constructible from Tier-1 + WSP composite recipes per canon § 4.6 + coverage-matrix § Summary. **No bespoke commission required at VS2a.**

**Music RED segment:** D10 002011-015 currently silent in playtest — Q-MATT-2 PARKED. Sub-path A rotation fallback recommended as IMMEDIATE wire while Matt decides Option B vs Option D.

**Holy register-attention zone:** YELLOW across all archetype groups; canon § 3.2 Path 1 composite recipe documented (WSP/WS3 Light base + Kenney impactBell_heavy_*.ogg transient + pitch-shift). Q-MATT-5 PARKED-default: Path 1 by default.

## 4. Acquisition cost summary (3 paths)

| Path | Cost | Coverage | When |
|---|---:|---|---|
| **Path 0 — Matt-already-authorized baseline** | $3.59 in flight | VS2a pipeline-unblock; thin Cluster A spell SFX | Already authorized; legolas Tier-1 fetch in flight |
| **Path 1 — Minimum extension (WSP $49)** | +$49 = $52.59 total | STRONG Cluster A spell SFX; holy composite resolved | **RECOMMENDED for VS2a register-fidelity** — Q-MATT-AUDIO-1 IMMEDIATE |
| **Path 2 — Preferred (WS3 $99 + WS1 $35)** | +$134 over Path 1 = $186.59 | All RED cells composite-resolved high-fidelity; boss-tier death; per-element variance | RECOMMENDED for VS2b ship-readiness — Q-MATT-AUDIO-2 VS2b |
| **Path 3 — Aspirational (Bit By Bit $77.60 + David Dumais $75 + Fusehive $100)** | +$252.60 over Path 2 = $439.19 | Premium Cluster C ambient; demo-ship music alternative; AAA composite-source pool | Pre-demo-ship gate only — Q-MATT-AUDIO-3 + Q-MATT-3 contingent |

Per-vendor invoice line items + Matt-selective-authorization grid: `audio-acquisition-shortlist-vs2a-2026-05-17.md` § Per-vendor invoice line items.

## 5. License posture

| License class | Count of packs in manifests | Notes |
|---|---:|---|
| CC0 (public domain) | 4 (Kenney Interface, Kenney Impact, OGA RPG Sound Pack, kmontesdev Fantasy Ambient) | Zero attribution friction; commercial use unrestricted |
| commercial-free-no-redistribution | 3 (Leohpaz RPG Essentials, Leohpaz Minifantasy Dungeon, TomMusic) | Free; commercial use OK; no asset redistribution outside engine |
| commercial-royalty-free | 2 (PixelLoops Ultimate Ambient, Bit By Bit Sound) | $3.59 + $77.60 respectively; Bit By Bit attribution-required in credits |
| commercial-single-user-unlimited-games | 3 (WSP, WS3, WS1) | $49/$99/$35; commercial use OK in unlimited games |
| CC-BY-3.0 | 1 (Little Robot Fantasy SFX Library) | Attribution required: "Little Robot Sound Factory / littlerobotsoundfactory.com" |
| Suno-Pro-Commercial | 1 (existing 001001-005 + future Option B) | Status PARKED-MATT: game-embedded clause clarification per canon § 7.4 |

**License-unclear / excluded:** **none** in this curation (per dispatch discipline). Legolas-4 flagged no vendor as license-blocked in the audio catalogue (NightBorne, which was flagged in VFX catalogue, has no audio analog).

**Attribution-required vendors (3 total):**
1. Little Robot Sound Factory (CC-BY-3.0) — IF Layer-1 Little Robot row wired (manifest flags as DEFER — re-evaluate post-WSP)
2. Bit By Bit Sound (commercial-royalty-free-attribution-required) — IF Path 3 Option D selected
3. Cyrex Studios (CC-BY-4.0; legolas-4 UI alternative) — NOT in current manifest (Kenney Interface CC0 preferred)

Tier-1 attribution-required-when-wired vendors flagged: legolas-4 inventory notes Leohpaz packs as "no redistribution" but attribution-NOT-required.

## 6. Open Matt-decisions (consolidated decision surface)

Per gandalf canon § 10 + new elrond-curation decisions:

| ID | Decision | Source | Recommendation | Decision-moment |
|---|---|---|---|---|
| Q-MATT-1 | Sonic register cluster lock | canon § 2 | Confirm canon cluster lock | Knight-rider decisions-log canonicalization |
| **Q-MATT-2** | **Music gap 002011-015 path** | canon § 7 | **Option B Suno primary + Option A immediate fallback** | **IMMEDIATE — silent in playtest** |
| Q-MATT-3 | Bit By Bit Sound $77.60 spend | canon § 7 | Authorize at pre-demo-ship gate; contingent on Q-MATT-2 = Option D | Pre-demo-ship gate |
| **Q-MATT-4** | **Canonical Suno prompt anchor lock** | canon § 7 | Lock § 7.3 prompt language as canonical | **IMMEDIATE — drives Q-MATT-2 Option B** |
| Q-MATT-5 | Holy register-attention path | canon § 3 | Path 1 composite default; elrond proceeds unless playtest flags | Elrond curation default (PROCEEDING) |
| **Q-MATT-AUDIO-1 (NEW)** | **WSP $49 acquisition authorization** | this curation | **APPROVE for VS2a register-fidelity** | **IMMEDIATE for VS2a** |
| Q-MATT-AUDIO-2 (NEW) | Path 2 $134 additional acquisition (WS3 + WS1) | this curation | Defer to VS2b gate | VS2b planning |
| Q-MATT-AUDIO-3 (NEW) | Path 3 $252.60 additional (premium ambient + music alternative) | this curation | Defer to pre-demo-ship | Pre-demo-ship gate |
| **Q-MATT-AUDIO-4 (NEW — UNBLOCKS LAYER-4)** | **kmontesdev Google-Drive fetch (~30min Matt browser) + PixelLoops itch.io $3.59 purchase (Matt-pre-authorized; needs credentials)** | legolas Tier-1 completion FLAG 1 + FLAG 2 | **EXECUTE — unblocks Layer-4 ambient coverage from 1 GREEN to 6-8 GREEN** | **IMMEDIATE — blocks Layer-4 ambient deployment at drax wiring** |

**Four IMMEDIATE Matt actions surface today:** Q-MATT-2 (music gap path), Q-MATT-4 (Suno prompt anchor), Q-MATT-AUDIO-1 (WSP $49 for VS2a register-fidelity), and Q-MATT-AUDIO-4 (kmontesdev Google-Drive + PixelLoops itch.io manual fetches — credentials-needed, spend $3.59 pre-authorized).

## 7. Handoffs

### 7.1 → drax — post-acquisition wiring inputs (future-wiring dispatch consumes)

Drax future-wiring dispatch consumes the 5 per-layer manifests + coverage matrix + canon § 9 engineering notes:

- **Manifest paths** (see § 2 above) — JSONL schemas extend the VFX-layered manifest pattern with audio-specific fields (sonic_register_fit, loudness_estimate, player_emitter_variant, composite_construction, composite_recipe).
- **Folder schema** per canon § 9.1: `/audio/sfx/{layer}/{element}_{geometry_archetype}.ogg` (Layer 1) + `/audio/sfx/layer3/{element}_{archetype}.ogg` (Layer 3 foley) + `/audio/sfx/layer4/{biome}_ambient.ogg` (Layer 4 atmospheric) + `/audio/sfx/layer7/{ritual_moment}_stinger.ogg` (Layer 7) + `/audio/music/season_{id}.ogg` (Layer 5 unchanged).
- **Acquired-path references** in manifest rows point to legolas Tier-1 fetch staging paths (`reincarnated-demo/public/audio/sfx/{vendor}/`) — drax wiring reads filesystem at integration time; tolerates legolas fetch-in-flight (manifest paths stable even if files not all on disk yet).
- **5-layer bus structure** per canon § 9.3 — drax wiring implements; Howler.js + Web Audio GainNode tree.
- **Sidechain-compressor rules** per canon § 5.3 — 5 mandatory ducking rules (Layer 1 → Layer 4 / Layer 5 / + voice + ritual variants).
- **Polyphony cap** 8 simultaneous combat SFX channels per canon § 5.4; oldest-drop-on-overflow.
- **Pitched variation** ±100 cents per canon § 5.5 anti-fatigue rule.
- **Composite construction** for 5 RED cells + holy register-attention zone — recipes documented in manifest rows (substrate manifest layer1.construct.* rows + foley manifest layer3.kenney.bell-chime-holy-composite-source row + atmospheric manifest layer4.glowing-cave-composite + layer4.sewer-composite rows). Drax decides composite-at-runtime vs pre-rendered-at-integration.
- **Telemetry events** per canon § 9.4 — 3+1 metrics for star-lord (`music_silent_fallback_fired`, `audio_polyphony_dropped`, `canonical_silence_violated`, optional `sidechain_duck_latency_ms`).

**Drax wiring dispatch auto-fires when:** legolas Tier-1 fetch ships completion record AND this curation ships completion record (per dispatch coordination § AUTO-FIRE TRIGGER inverted: drax wiring fires when curation + legolas-fetch both ship).

### 7.2 → matt — acquisition cost ladder + per-decision matrix

Four IMMEDIATE actions (today):

1. **Q-MATT-2 (canon § 7):** Music gap 002011-015 path. Recommended: Option B Suno per-season generation against canonical retro-JRPG anchor prompt; immediate fallback Option A rotation while Suno game-embedded clause verification proceeds. Sub-paths and license clarifications in `audio-acquisition-shortlist-vs2a-2026-05-17.md` § Music gap special pathing.
2. **Q-MATT-4 (canon § 7):** Lock canonical Suno prompt anchor (canon § 7.3 prompt language). Required if Q-MATT-2 = Option B. Analog to `style-register.md`'s LLM image-generation prompt anchor lock.
3. **Q-MATT-AUDIO-1 (this curation, NEW):** WSP $49 acquisition for VS2a register-fidelity. Per canon § 4.1 Cluster A primary sources includes WSP as canonical retro-pixel skill SFX pack. Closes the spell-SFX coverage gap that Path 0 leaves thin. Per-vendor invoice line item 1 in acquisition shortlist.
4. **Q-MATT-AUDIO-4 (this curation, NEW — UNBLOCKS LAYER-4):** kmontesdev Google-Drive folder download (https://drive.google.com/drive/folders/1tlJMeJp5PabLjmHyc3kTVd5dPycUKSav — browser+Google-login required, ~30 minute Matt action) + PixelLoops itch.io purchase (https://pixelloops.itch.io/ultimate-game-ambient-sound-effects-pack — $3.59 Matt-pre-authorized, needs itch.io credentials, ~5 minute Matt action). Unblocks Layer-4 ambient coverage from current 1 GREEN biome (forest via TomMusic) back to 6-8 GREEN biomes (all canon-named per coverage matrix § 4). Without this, drax wiring at Layer 4 is functionally blocked at TomMusic-only fidelity.

Three DEFERRED decisions (planning horizon):

4. **Q-MATT-3 (canon § 10):** $77.60 Bit By Bit Sound — pre-demo-ship gate; contingent on Q-MATT-2 = Option D.
5. **Q-MATT-AUDIO-2 (this curation, NEW):** Path 2 $134 (WS3 + WS1) — VS2b planning gate.
6. **Q-MATT-AUDIO-3 (this curation, NEW):** Path 3 $252.60 (Bit By Bit + David Dumais + FH) — pre-demo-ship gate.

Two PROCEEDING decisions (no Matt block required unless playtest signals issue):

7. **Q-MATT-5 (canon § 10):** Holy register-attention path — elrond proceeds Path 1 composite by default.
8. **Q-MATT-1 (canon § 10):** Sonic register cluster lock — knight-rider drafts decisions-log entry at next governance pass.

### 7.3 → knight-rider — standard chain coordination

Completion record appended to this dispatch (`agentic_orchestration/dispatches/2026-05-17-elrond-audio-pack-curation-queued.md`). Hive-log STATE + HANDOFFs appended per § 14.1.1 PRE-SIGNAL discipline.

Auto-fire trigger for drax audio wiring follow-on dispatch: BOTH this curation (✓ shipped) AND legolas Tier-1 fetch (IN FLIGHT — coordinate completion record check) ship. Knight-rider monitors and spawns drax when both land.

Knight-rider decisions-log entry drafts: per canon § 11.5 + canon § 10:
- Sonic register cluster lock (Q-MATT-1) at next governance pass
- Music register canonical Suno prompt anchor (Q-MATT-4) at next governance pass
- **NEW from this curation:** WSP $49 Tier-2 acquisition authorization log entry (Q-MATT-AUDIO-1) if Matt approves

### 7.4 → legolas — feedback for in-flight fetch (NON-BLOCKING)

Legolas Tier-1 fetch in flight; per snapshot at this curation's authoring:
- ON-DISK: Kenney (Interface + Impact extracted, 230 ogg files), OGA (RPG Sound Pack 192 wav files)
- STAGED-PARTIAL (empty directories; expected post-fetch): Leohpaz, TomMusic, kmontesdev, PixelLoops

Manifest paths stable regardless. Drax wiring tolerates fetch-in-flight per dispatch coordination directive ("drax wiring reads file system at integration time"). No blocking issue surfaced.

**Optional follow-up question for legolas (post-fetch):** verify legolas-4 inventory.jsonl `file_count` claims against on-disk extracted reality post-fetch completion. Any deviations are curation-data-quality notes; not blocking VS2a.

## 8. Quality discipline applied

Per dispatch acceptance criteria + canon authoring discipline:

- [x] Per-layer subset manifests authored — 5 JSONL files (substrate / class-archetype / foley / atmospheric / music)
- [x] Coverage matrix authored — post-curation GREEN/YELLOW/RED with register-filter applied
- [x] Acquisition shortlist authored — 3 cost paths (minimum / preferred / aspirational); per-vendor invoice line items
- [x] Summary doc authored — this document
- [x] License posture explicit per asset — § 5 above; license_clear field in every manifest row
- [x] No license-unclear assets included — verified; only PARKED items are Suno tracks (existing on-disk; flagged as PARKED-MATT not curation-included)
- [x] All assets pass gandalf sonic register canon — WEAK-fit excluded; MODERATE flagged in render_notes; STRONG preferred (only Little Robot CC-BY MODERATE-with-flag survives Layer-1 contention pending WSP acquisition decision)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append — TO BE PERFORMED at hive-log append step
- [ ] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider — TO BE PERFORMED at hive-log append step

**Dispatch-discipline locks honored:**
- ❌ DID NOT acquire any packs (Matt L3 required for spend) — only documented; Path 0 baseline is legolas Tier-1 in flight under Matt's existing authorization
- ❌ DID NOT modify legolas crawl or gandalf register — consumed both as-is
- ❌ DID NOT touch demo audio.ts code — drax integration follows post-curation
- ❌ DID NOT include any vendor whose license is unclear
- ❌ DID NOT include WEAK sonic-register-fit assets
- ❌ DID NOT extend to voice-over scope — forward-flag preserved per canon § 8

---

*Audio curation summary authored 2026-05-17 by elrond per audio-pack-curation dispatch. 5 per-layer subset manifests + coverage matrix + acquisition shortlist consolidate the legolas-4 catalogue under gandalf's HYBRID cluster lock. 32 active manifest rows; ~28 GREEN Layer-1 slots; all 5 RED cells composite-resolvable from Tier-1 + WSP recipes; D10 music gap PARKED-MATT with Option A immediate fallback + Option B primary path documented. Q-MATT-AUDIO-1 ($49 WSP) flagged as IMMEDIATE for VS2a register-fidelity. Drax wiring follow-on dispatch consumes manifests + canon § 9 engineering notes at integration time.*
