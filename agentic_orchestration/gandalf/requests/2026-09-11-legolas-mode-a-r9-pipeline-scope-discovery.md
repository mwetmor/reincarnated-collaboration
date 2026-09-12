# Legolas — Mode A commission R9: SCOPE DISCOVERY for a complete painted-2D ARPG art pipeline

> **From:** gandalf. **To:** legolas (a SECOND, independent Mode A instance — do not wait on or duplicate R6–R8). **Date:** 2026-09-11. **Budget:** ≤ 1 session, read-only, primary sources, graded claims, two search passes per thread then record the gap. **File at:** `agentic_orchestration/legolas/research/2026-09-11-r9-pipeline-scope-discovery/findings.md` + `sources.json`.

**Matt's ask (verbatim intent):** *"don't limit yourself to the scopes I've listed. Ultra-think through all known (and research to find unknown) scopes potentially involved within this 2D painted complete game art pipeline."*

**Your input:** gandalf's own sweep — `agentic_orchestration/gandalf/notes/2026-09-11-painted-2d-pipeline-scope-map.md` (read it first; ~70 scopes across 9 groups). **Your job is the complement:** what it MISSES, what it gets WRONG, and evidence for what it marks uncertain.

## Threads
1. **Ground truth from shipped painted/pre-rendered ARPGs and painted 2D action games** — the actual asset inventories and pipeline stages: Diablo II (DC6/DCC/COF composition, palette-shift lighting and item tinting, tile/automap data, 16 vs 8 directions; D2R's remaster pipeline for 4K), Diablo I, Hades / Hades II (Supergiant talks: painted environments, parallax, character pipeline, VFX), Bastion, Darkest Dungeon (Spine parts, FX), Dead Cells (3D→pixel), Torchlight, Titan Quest / Grim Dawn (3D, for the *inventory* of asset classes only), Path of Exile (icon/item/skill-icon counts and UI art scale). Extract **asset classes and process stages** as a checklist; mark each present/absent in gandalf's map.
2. **Modern 2D production stacks** — Aseprite/Spine/Godot 2D/Unity 2D pipelines; what a 2D animator's and environment artist's *deliverable list* looks like; sockets, hitboxes, sort anchors, occlusion masks, normal maps for 2D lights, parallax, decals, atlases, streaming.
3. **AI-era pipelines (2024–2026)** — studios/tools shipping generated 2D game art: what they include that a human pipeline doesn't (prompt libraries, reference locking, regeneration/invalidation, model-version pinning, provenance/C2PA, moderation handling, IP-similarity checks, license terms for commercial use of OpenAI/others' generated images). **Evidence on model-version drift** (a provider updates the image model → assets no longer match): any documented cases or mitigations.
4. **Quality/accessibility/legal scopes** — colorblind-safe VFX/telegraph practice in ARPGs (deuteranopia simulation gates), readability at 4K vs 1080p (asset resolution policy precedents), gore/moderation policy, IP-similarity tooling (perceptual hash / embedding distance against reference corpora), typography rules against AI-rendered text.
5. **Scopes nobody lists** — anything you find in postmortems/GDC talks that consumed art-team time and is absent from the map (e.g., loading-screen art, cursor sets, item-drop beams, ground-item sprites at scale, tooltips art, seasonal/cosmetic sets, photo mode, mod tooling).

## Deliverable
A **gap table**: scope · present in gandalf's map? (Y/N/partial) · precedent (game/tool, cited) · generation method (A/D/E/H) · oracle candidate (deterministic? JUDGE?) · bible field · recommended run (C-1 / C-2 / P / M). Then a ≤ 15-line "what changes in C-1 because of this" list. Grade everything.
