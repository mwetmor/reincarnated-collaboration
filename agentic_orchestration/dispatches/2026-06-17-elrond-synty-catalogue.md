# Dispatch — 2026-06-17 — elrond — Synty gear-substrate catalogue

**From:** knight-rider
**To:** elrond
**Approved by:** Matt — autonomous hive-mode directive 2026-06-17 ("download all assets that could possibly be used and get gandalf all his info")
**Estimated effort:** ~half a session (schema + populate + validate); the corpus is already on disk
**Acceptance:** a queryable SQLite catalogue indexing the downloaded Synty substrate (metadata + filesystem path index; bytes stay on disk, never in the DB), with slot taxonomy, license incorporation_status ledger, and a distinctiveness hook — sufficient for gandalf to resume the gear-spec design session.

## Context

The Synty FBX corpus is downloaded and integrity-verified (knight-rider, 2026-06-17): **136 FBX pack zips, 8.8 GB** at `~/Games/synty-corpus/fbx/`, plus **21 Unity/Unreal `.unitypackage`/zip** for the no-FBX packs at `~/Games/synty-corpus/nonfbx/` (knight-rider is extracting meshes from these; treat them as a second wave). The full enumeration manifest is committed at `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/full-fbx-variant-manifest.jsonl` (620 rows / 157 collections / all variants) with `collections-157.json`.

This is the gear-catalogue substrate for gandalf's **restyle-based** gear-spec generator (see his locked architecture doc). The pattern mirrors the existing `research/curated/catalogue.db` + `research/catalogue/<vendor>/` "select + adapt, not mass-generate" substrate — now extended to 3D character/armor/weapon FBX. **Bytes live on the filesystem; the DB indexes paths + metadata only.**

The corpus has two structural classes (confirmed by knight-rider inspection; galadriel is verifying in parallel):
- **Monolithic packs** (page-1 POLYGON: Adventure, Fantasy Kingdom, Samurai, …): baked whole-character FBX, one mesh per character (`SourceFiles/Character_Files/SK_Character_*.fbx` or `Source_Files/Characters/SK_Chr_*.fbx`). These are **appearance-units** (a whole silhouette), not per-slot.
- **Modular pack** (POLYGON Modular Fantasy Heroes, already at `~/Games/reincarnated-godot/Assets/Synty/polygon-modular-fantasy-heroes/`): genuine per-slot parts (`Chr_<Slot>_<Gender>_<NN>_Static.fbx` across Head/Torso/Hips/ArmUpper L·R/Leg L·R/Hand L·R/…) + attachment sockets. This is the per-slot lane.

Your taxonomy must accommodate BOTH: whole-character appearance-units AND modular per-slot parts.

## Required reading before starting
- This dispatch.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/CRAWL-METHOD-CRACKED-2026-06-17.md` (corpus shape + download mechanism).
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/full-fbx-variant-manifest.jsonl` + `collections-157.json`.
- `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — gandalf's locked architecture; §7.1 names the elrond catalogue/ledger acceptance hook. Build to that hook.
- `research/curated/catalogue.db` schema + a `research/catalogue/<vendor>/` folder — to match the existing substrate metadata shape.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/slice-verification-2026-06-17.md` (galadriel's output — may land while you work; incorporate its UV/socket verdict into the distinctiveness/slot fields if present, else leave the hook).

## Scope
- [ ] **SLICE-FIRST checkpoint (do this BEFORE the full populate).** gandalf's resumption gate (§4) needs only a representative *slice* catalogued — not all 136 packs. Populate + path-verify a slice first (a few whole-character appearance-unit packs spanning distinct themes — e.g. Adventure, Fantasy Kingdom, Samurai — plus the modular per-slot pack and at least one weapon-bearing pack), surface it as an explicit checkpoint, and signal that gandalf can resume against it. THEN proceed to the full 136-pack populate. (Gate-1 jack-ryan 2026-06-17.)
- [ ] **Schema design.** Tables at minimum:
  - `packs` — collection_id, collection_name, variant availability (has_fbx/unity/unreal/godot), source path, license `incorporation_status` (default `NOT_INCORPORATED`; `INCORPORATED` carries season/build + ISO timestamp), structural_class (`monolithic` | `modular`).
  - `assets` — one row per usable mesh FBX inside a pack: pack FK, file path (relative to corpus root), asset_type (`character` | `weapon` | `armor_part` | `prop` | `other`), slot (nullable; for modular: head/torso/hips/arm_upper_l/…; for monolithic: `whole_character`), gender if encoded, distinctiveness_score (nullable hook — galadriel scores later per gandalf §7.4), notes.
  - `textures` (optional but recommended) — mask textures per pack (the `_Texture_Mask` recolor lever), path + channel-region mapping if galadriel reports it.
- [ ] **Populate** by scanning the on-disk zips (`unzip -l` to index member FBX without extracting bytes) for the 136 FBX packs, plus the modular pack's extracted parts, plus the 21 no-FBX packs once knight-rider's extraction lands (second wave — design the schema so a second populate pass is clean).
- [ ] **incorporation_status ledger** semantics per Matt's stipulation: assets not INCORPORATED before the subscription lapses cannot be used afterward. Default everything NOT_INCORPORATED; provide an update path to stamp INCORPORATED + season/build + timestamp.
- [ ] **Path index integrity check:** every assets.path must resolve to a real file on disk; report any misses.
- [ ] Smoke: a few example queries (e.g., "all whole-character appearance-units", "all modular torso parts", "all weapons", "packs still NOT_INCORPORATED").
- [ ] MIGRATION.md if this changes the existing `research/curated/catalogue.db` shape (if you build a separate `synty_catalogue.db`, note the relationship).
- [ ] AGENT_STATE updated if you keep one.

## Cross-seam contract change? (Principle 6 gate — knight-rider completed at authoring)
Round-trip: **not applicable** — this builds a standalone research/catalogue DB; it does not add/modify/rename any telemetry schema table, fight_log/loadout/export fixture key, or other inter-seam engine fixture. The boundary with star-lord (engine telemetry, ADR-004) is NOT touched. If you choose to extend the existing `research/curated/catalogue.db` rather than create a new DB, write a MIGRATION note describing the schema delta for any downstream reader.

## Acceptance criteria
- [ ] SQLite catalogue exists, populated for the 136 FBX packs + modular per-slot parts, path-index-verified.
- [ ] Slot taxonomy handles both whole-character appearance-units and modular per-slot parts.
- [ ] incorporation_status ledger present with default NOT_INCORPORATED + stamp path.
- [ ] distinctiveness_score hook present (nullable) for galadriel's later pass.
- [ ] Example queries demonstrated.
- [ ] Round-trip: not applicable (standalone research catalogue; no cross-seam fixture change).

## Out of scope (explicit non-goals)
- Do NOT compute distinctiveness scores (galadriel's seam per gandalf §7.4) — only provide the column/hook.
- Do NOT render thumbnails or run CV (galadriel).
- Do NOT design the StyleProfile output shape (gandalf rules that in §7.6 after UV verification).
- Do NOT move/re-host bytes (Pi migration is a separate knight-rider op).
- Do NOT extract the 21 unitypackages (knight-rider is doing that; you index the results).
- Do NOT write to any Synty-side state.

## Open questions for the agent to resolve + document
- Separate `synty_catalogue.db` vs extend `research/curated/catalogue.db`? Pick and justify; the existing vendor-catalogue precedent should guide it.
- Slot vocabulary: reconcile the modular pack's slot names (Chr_<Slot>) with a clean canonical slot set gandalf can design against (chest/legs/boots/hands/head/shoulders/back/weapon/…). Document the mapping.

## References
- knight-rider autonomous hive-mode session 2026-06-17.
- `CRAWL-METHOD-CRACKED-2026-06-17.md`, `full-fbx-variant-manifest.jsonl`, `collections-157.json`.
- gandalf locked architecture `gear-spec-generation-deferred-architecture-2026-06-16.md` §7.1 (elrond hook).
- Existing substrate precedent: `research/curated/catalogue.db`, `research/catalogue/`.
