# 2026-05-17 — elrond — Audio pack curation (QUEUED — auto-fires after legolas crawl + gandalf audio register)

**Authority:** Matt L3 2026-05-17 late evening — standard scout → register → curate chain.
**Type:** Pattern B — curation + manifest authoring (~0.5-1 day; data-steward work in elrond's seam).
**Predecessors (both gate auto-fire):**
- Legolas audio vendor catalogue crawl (`agentic_orchestration/dispatches/2026-05-17-legolas-audio-vendor-catalogue-crawl.md`)
- Gandalf audio register / sonic identity canon (`agentic_orchestration/dispatches/2026-05-17-gandalf-audio-register-sonic-identity-canon-queued.md`)
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until BOTH predecessors ship completion records.** Knight-rider activates when both land.

---

## Why this matters

Legolas produces raw catalogue (what's available). Gandalf produces canon (what fits). Your job: consume both → produce actionable subset manifests + per-slot acquisition shortlist that drax can wire and Matt can authorize spend on.

Same standard chain you ran for Pimen, icons-and-props, and CraftPix mega-catalogue. Mirror those manifest patterns.

---

## Required reading (when activated)

1. **Legolas audio crawl** — `agentic_orchestration/research/catalogue/audio-vendors-2026-05-17/` (inventory.jsonl + coverage-matrix.md + summary.md)
2. **Gandalf audio register canon** — `canonical/story/audio-register-canon-2026-05-17.md` (your filter criterion — only vendors/packs matching sonic register + layered model survive curation)
3. **Your prior curation patterns** — Pimen subset / icons-and-props subsets / 4-layer VFX architecture (template for this commission)
4. **Demo audio.ts conventions** — `reincarnated-demo/src/audio/audio.ts` (Tier 2 file naming + path convention; manifests must align with code's lookup keys)
5. **Geometry vocabulary** — for SFX × geometry × element coverage matrix

---

## Scope — four deliverables

### Deliverable 1 — Per-slot subset manifests

For each layer in gandalf's audio architecture (likely substrate-tier / UI-tier / ambient-tier / music-tier / death/stinger-tier — gandalf finalizes layer count):

Author one JSONL per layer at `agentic_orchestration/research/curated/audio-{layer}-subset-vs2a-2026-05-17.jsonl`.

Per row (mirror Pimen subset schema):
- asset_id (composite of vendor + pack + filename)
- vendor + pack
- layer (substrate / ui / ambient / music / death)
- slot (specific event/element/geometry/biome the asset fills)
- file_path (target in `public/audio/{layer}/{slot}.{ext}` if Matt approves acquisition)
- license + attribution_class
- pack_origin + cost_usd
- sonic_register_fit (per gandalf register canon: STRONG / MODERATE / WEAK)
- duration_seconds + loudness_estimate
- player_emitter_variant (yes/no if separate file for player vs enemy emitter per gandalf Q5)
- render_notes (any drax-integration consideration)

### Deliverable 2 — Coverage matrix update

Author `agentic_orchestration/research/curated/audio-coverage-matrix-vs2a-2026-05-17.md`:

Per-slot coverage with GREEN/YELLOW/RED (post-curation):
- GREEN: shortlist has acquireable asset
- YELLOW: shortlist asset has caveat (license / cost / register fit)
- RED: no acquireable asset; commission/generation needed

Highlight RED cells as acquisition gaps Matt may need to commission new vendor work on (or accept procedural Tier 1 as permanent for those slots).

### Deliverable 3 — Acquisition shortlist + cost

Author `agentic_orchestration/research/curated/audio-acquisition-shortlist-vs2a-2026-05-17.md`:

- Minimum-cost path (close GREEN+YELLOW only): $X
- Preferred-cost path (close most RED): $Y
- Aspirational-cost path (close all + premium register matches): $Z
- Per-vendor invoice line items (so Matt can authorize selectively)
- Music gap resolution path (per gandalf Q6 recommendation)
- Forward-flag any vendors requiring direct outreach (premium commission)

### Deliverable 4 — Summary doc + handoff

Author `agentic_orchestration/research/curated/audio-curation-summary-vs2a-2026-05-17.md`:

1. Executive summary
2. Layered manifest reference (paths + row counts per manifest)
3. Coverage gap snapshot (GREEN / YELLOW / RED)
4. Acquisition cost summary (3 paths)
5. License posture (CC0 vs CC-BY vs commercial vs unclear)
6. Open Matt-decisions (acquisition authorizations; music gap pragmatic choice; voice-over forward-flag follow-up)
7. Handoffs:
   - → drax: post-acquisition wiring dispatch inputs (manifest paths + audio.ts Tier 2 naming convention + layered-architecture integration plan)
   - → matt: acquisition cost ladder + per-decision matrix
   - → knight-rider: standard chain coordination

---

## Out of scope (DO NOT)

- ❌ DO NOT acquire any packs (Matt L3 required for spend)
- ❌ DO NOT modify legolas crawl or gandalf register (consume only; flag any data-quality issues for follow-on if needed)
- ❌ DO NOT touch demo's audio.ts or any code (drax integration follows post-curation)
- ❌ DO NOT include any vendor whose license is unclear or unverified
- ❌ DO NOT include any asset that fails gandalf's sonic register canon (WEAK fit → exclude)
- ❌ DO NOT extend to voice-over scope (forward-flagged in gandalf register)

---

## Acceptance criteria

- [ ] Per-layer subset manifests authored (one JSONL per gandalf-defined audio layer)
- [ ] Coverage matrix authored (per-slot GREEN/YELLOW/RED)
- [ ] Acquisition shortlist with 3 cost paths (minimum / preferred / aspirational)
- [ ] Summary doc authored
- [ ] License posture explicit per asset
- [ ] No license-unclear assets included
- [ ] All assets pass gandalf sonic register canon
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider

---

## Coordination

- **AUTO-FIRE TRIGGER:** BOTH legolas audio crawl AND gandalf audio register ship completion records. Knight-rider monitors and spawns elrond when both land.
- **Parallel-safe with**: drax/rocket hotfixes (shipped); D11.1 sprint chain (separate concern); CraftPix curation extension (shipped)
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No tag** (curation; not code)

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 audio research authorization. ~0.5-1 day when activated. Append completion record when done.*

---

## COMPLETION RECORD — 2026-05-17 late-evening+4 — elrond

**Status:** SHIPPED. Auto-fire triggered cleanly: both predecessors (legolas-4 audio crawl + gandalf audio register canon) shipped completion records earlier 2026-05-17; this dispatch consumed both as inputs. Legolas Tier-1 fetch ALSO SHIPPED at 19:45Z (6/8 packs ON-DISK; 2 FLAGGED for Matt manual fetch) — providing ground-truth path verification.

**5 deliverables shipped:**

| Deliverable | Path | Status |
|---|---|---|
| 1. Per-layer subset manifest — Layer 1 (substrate) | `agentic_orchestration/research/curated/audio-substrate-subset-vs2a-2026-05-17.jsonl` | 14 active rows (Cluster A skill SFX + composites) |
| 1. Per-layer subset manifest — Layer 2 (class-archetype) | `agentic_orchestration/research/curated/audio-class-archetype-subset-vs2a-2026-05-17.jsonl` | 1 forward-flag row (Phase-2 deferred per canon § 4.7) |
| 1. Per-layer subset manifest — Layer 3 (foley) | `agentic_orchestration/research/curated/audio-foley-subset-vs2a-2026-05-17.jsonl` | 7 active rows (Cluster D Kenney primary + Cluster A foley) |
| 1. Per-layer subset manifest — Layer 4 (atmospheric) | `agentic_orchestration/research/curated/audio-atmospheric-subset-vs2a-2026-05-17.jsonl` | 5 active rows (PixelLoops + TomMusic + kmontesdev + 2 composites) |
| 1. Per-layer subset manifest — Layer 5 (music) | `agentic_orchestration/research/curated/audio-music-subset-vs2a-2026-05-17.jsonl` | 5 active rows (existing 001001-005 + Suno/Option-A/Option-D paths) |
| 2. Coverage matrix (post-curation) | `agentic_orchestration/research/curated/audio-coverage-matrix-vs2a-2026-05-17.md` | GREEN/YELLOW/RED per slot; 5 Layer-1 RED cells all constructible |
| 3. Acquisition shortlist (3 cost paths) | `agentic_orchestration/research/curated/audio-acquisition-shortlist-vs2a-2026-05-17.md` | Path 0 in flight $3.59; Path 1 $52.59 RECOMMENDED VS2a; Path 2 $186.59 VS2b; Path 3 $439.19 pre-demo-ship; Music sub-paths A/B/D detailed |
| 4. Summary doc (8 sections) | `agentic_orchestration/research/curated/audio-curation-summary-vs2a-2026-05-17.md` | Executive summary + layered manifest reference + coverage gap snapshot + acquisition cost summary + license posture + open Matt-decisions + handoffs + quality discipline applied |
| 5. Music gap (002011-015) resolution | Documented in music manifest + acquisition shortlist | Option B Suno per canon § 7.3 PARKED-MATT-IMMEDIATE; canonical Suno prompt anchor (Q-MATT-4) ready to lock; Option A rotation fallback wireable now as engineering-trivial unblocker |

**Total active manifest rows across 5 layers:** 32

**Matt-decision surface created:**
- 5 IMMEDIATE: Q-MATT-2 (music gap path), Q-MATT-4 (Suno prompt anchor), Q-MATT-AUDIO-1 (WSP $49), Q-MATT-AUDIO-4 (kmontesdev + PixelLoops manual fetch — credentials-needed; spend pre-authorized), Q-MATT-1 (cluster lock at decisions-log moment)
- 3 DEFERRED: Q-MATT-3 (Bit By Bit Sound $77.60 pre-demo-ship), Q-MATT-AUDIO-2 (Path 2 WS3+WS1 $134 VS2b), Q-MATT-AUDIO-3 (Path 3 premium $252.60 pre-demo-ship)
- 2 PROCEEDING: Q-MATT-5 (holy composite Path 1 default), cluster-lock canonicalization at knight-rider governance pass

**Acceptance criteria status:**

- [x] Per-layer subset manifests authored (5 JSONL files, one per gandalf-defined audio layer)
- [x] Coverage matrix authored (per-slot GREEN/YELLOW/RED post-curation)
- [x] Acquisition shortlist with 3 cost paths (minimum $52.59 / preferred $186.59 / aspirational $439.19)
- [x] Summary doc authored
- [x] License posture explicit per asset (license_clear field in every manifest row; CC0/CC-BY/commercial classes summarized in summary § 5)
- [x] No license-unclear assets included (Suno tracks marked PARKED-MATT not curation-included; verified)
- [x] All assets pass gandalf sonic register canon (WEAK-fit excluded; MODERATE flagged with rationale; STRONG preferred per canon § 2.5)
- [x] PRE-SIGNAL § 14.1.1 before hive-log append (PERFORMED — git fetch origin executed; HEAD verified; concurrent writers acknowledged)
- [x] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider (PERFORMED — hive-log line 7626 region; 4 HANDOFFs total including legolas non-blocking feedback)
- [x] No tag (curation; not code) — confirmed

**Discipline locks honored:**
- ❌ DID NOT acquire any packs (Matt L3 required for spend) — only documented decision matrix
- ❌ DID NOT modify legolas crawl or gandalf register (consumed as-is)
- ❌ DID NOT touch demo audio.ts code
- ❌ DID NOT include any license-unclear vendor
- ❌ DID NOT include WEAK sonic-register-fit assets
- ❌ DID NOT extend to voice-over scope (forward-flag preserved per canon § 8)

**Coordination outcome:**
- AUTO-FIRE trigger for drax wiring follow-on dispatch: BOTH predecessors (this curation + legolas Tier-1 fetch) now SHIPPED. Knight-rider can spawn drax audio wiring dispatch when ready.
- Parallel-safe with drax v1.13 VS2a Final Sprint + rocket D11.2 planning + gandalf D11 post-mortem (all separate seams; no conflict).

— elrond, 2026-05-17 late-evening+4
