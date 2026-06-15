# Godot spike Phase-0 — free-validation design session (drax kickoff)

**Type:** design session / spike kickoff brief (gandalf seam → drax, fired direct per Matt 2026-06-14 "draft and fire a design session for the Godot spike").
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B). Matt purchased + downloaded the **Synty Sidekick Modular Characters FREE Starter Pack** + the **jgillich "Sidekick Creator for Godot"** plugin (at `/Users/admin/Games/reincarnated-collaboration/sidekick_creator`) + Godot 4.6.3 standard. "Draft and fire a design session for the Godot spike."
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-14-drax-godot-vertical-slice-spike-brief.md` — the FULL vertical-slice spike (Phase 1; register-2 lift + galadriel rubric + paid packs + dual-machine). This Phase-0 session is the **free, Mac-only precursor** that validates the path BEFORE the $200 spend + Phase-1 register work.
- `agentic_orchestration/research/knowledge/godot-3d-pivot/2026-06-14-synty-godot-purchase-de-risk.md` — legolas purchase-de-risk (buy-direct-not-Asset-Store; free-validate-first; 4.6.3 standard).
- `canonical/story/style-register.md` § "Register pivot" — the pivot this whole spike serves.

---

## 0. TL;DR — what Phase 0 is, and the finding that re-scopes it

> **STATUS (2026-06-14): COMPLETE — all four gates GREEN. See § 6 for results.** Gate #2 (auto-retarget crux) + gate #4 (runtime spirit-swap mechanism) both PASS on the Mac at $0. The two load-bearing cruxes the 2D path could not clear are proven in Godot 3D. Only the visual register (flat-color floor) remains — that is the paid Phase-1 vertical-slice spike's A-vs-B question, deliberately out of Phase-0 scope.

**Phase 0 = the FREE architecture validation.** Before any paid pack ($199.99 ea) or any register-2 lighting/VFX lift, prove the *pipeline mechanics* work end-to-end on the Mac with the free assets Matt already has: Godot 4.6.3 + jgillich plugin + Synty Free Starter Pack. **This is the $0 gate before the paid Phase-1 spend.**

**The re-scoping finding (gandalf code-read of `sidekick_character.gd`, 2026-06-14):** the central open design call from the pivot — *is composition bake-time-only, or runtime-callable?* — is **answered in the plugin code: runtime composition is available.** `combine()` runs against runtime-safe APIs (`load`/`instantiate`/`reparent`/`Skeleton3D`); the only editor-specific lines (`owner = EditorInterface...`) are guarded by `if Engine.is_editor_hint()` and simply skip at runtime. The plugin is `@tool ... extends Node3D` with a runtime `_ready()` that opens its SQLite DB. **So spirit-swap has BOTH paths available: runtime live-compose OR pre-baked `.scn` load.** Phase 0 *confirms* this empirically (don't assume the edge cases — blend-shape baking has a known Godot #10402 caveat the plugin flags); it is no longer a RISK, it is a "very likely works, prove it."

**Two more findings from the same read:**
- **Auto-retarget (the load-bearing crux) is plugin-automated.** `import_plugin.gd` (an `EditorScenePostImportPlugin`) auto-applies `retarget/bone_map` + `bone_renamer/skeleton_name` on FBX import. The "can't hand-rig infinity" crux that broke the 2D path is handled at import time by the plugin.
- **Species extensibility is in-code.** `enum Species { Human = 1, Goblin }` — Goblin (Tier-1 bipedal monster) is already wired; the community `Skeleton = 4` patch (Matt's reviewer note) is a one-line enum extension. The plugin is built to grow Synty species packs → Tier-1 bestiary rides this when the paid creature packs are bought (Phase 1+).

## 1. The Phase-0 pass gate (what "validated" means)

Phase 0 PASSES when ALL of these are demonstrated on the Mac with FREE assets:

1. **Project + plugin + DB install works.** Godot 4.6.3 standard opens a project with the SQLite addon + the jgillich plugin enabled, sidekick root configured, Free Starter Pack imported, no console errors on a composed character.
2. **Import auto-retarget works (crux #1).** An imported Synty FBX gets the bone map applied by the post-import plugin, and the composed character **plays a shared humanoid animation** (a Synty/Mixamo/Godot-retargeted clip) without manual per-mesh rigging. THIS is the de-risk that the whole modular strategy rests on.
3. **Editor (bake-time) composition works.** A `SidekickCharacter` node configured via inspector composes a coherent character; saved as `.scn` it loads as a standalone form. (The documented happy path.)
4. **Runtime composition works (the open-call confirmation).** A GDScript harness instantiates `SidekickCharacter` at runtime, sets `parts`/`colors`, calls `combine()`, and a character composes live in a running scene (not the editor). Capture any edge-case failures (blend-shape #10402, material wiring, performance of a single compose). **This is the spirit-swap-mechanism proof.**

**NOT in Phase 0** (deferred to the paid Phase-1 vertical slice): the register-2 lighting/VFX/material lift + galadriel's ≥3.6 rubric; the dual-machine low-Mac/high-PC workflow; the paid creature packs (Goblin/Skeleton Tier-1, KayKit Tier-2); the fixed-2.5D-camera register capture. Phase 0 is *pipeline mechanics only*, not *premium look*.

## 2. The plugin reality (grounded — drax does NOT re-derive this; drax CONFIRMS it)

From the gandalf code-read (cite, don't re-discover):
- **Composition** = `SidekickCharacter.combine()` in `sidekick_character.gd`. Editor + runtime capable (`@tool`; only `owner`-assignment is `Engine.is_editor_hint()`-guarded).
- **Parts model** = a `parts: Dictionary[Part, String]` + `colors` driven off an SQLite DB (`Proto_Side_Kick_Data`). Parts query by `type` + `ptr_species`. Weapon/gear sockets exist as `Part.Attachment*` → real bones (`part_bones` map).
- **Import retarget** = `import_plugin.gd` post-import plugin, auto bone-map + renamer. **Re-import any Sidekick FBX imported BEFORE enabling the plugin** (jgillich known-issue).
- **Dependency** = the SQLite GDExtension from the Godot asset library (the jgillich "Install SQLite from the asset lib" step) — a standard-build GDExtension, consistent with the locked **standard (non-.NET) Godot 4.6.3**.
- **Caveats to capture, not assume away:** blend-shape duplication (Godot #10402; `combiner_bake_blend` commented out) → body-shape blends at runtime may artifact; `combine()` cost (DB + instantiate + reparent) is fine for an occasional spirit-swap, NOT per-frame.

## 3. Phase-0 task split — agent-executable vs Matt-in-GUI

**drax executes headlessly (the bulk):**
- Scaffold the spike Godot project (`project.godot`, dir layout: `addons/sidekick_creator/`, `Assets/Synty/SidekickCharacters/`). **Recommend the project location** (default suggestion: a sibling `~/Games/reincarnated-godot-spike/` — throwaway-able, graduates to the real `reincarnated-godot/` if Phase 1 passes; flag if collab-subdir is preferred). Do NOT commit Synty binaries to git (license + size) — `.gitignore` the `Assets/Synty/` tree; commit only project + scripts + the test harness.
- Drop the jgillich plugin (already at `/Users/admin/Games/reincarnated-collaboration/sidekick_creator`) into `addons/sidekick_creator/`.
- Author a `.tscn` test scene instantiating a `SidekickCharacter` node with a known-good part configuration (`.tscn` is text — bypasses the GUI for the bake-time case).
- Author a **GDScript runtime-composition harness** (`compose_test.gd`): instantiate `SidekickCharacter`, set `parts`/`colors`, `combine()`, assert the mesh tree composed; drive a shared animation; time a single compose. This is the runtime-path proof (gate item #4).
- Run everything possible via `godot --headless` (project import, script run, scene load) and capture console output.
- Produce a **step-by-step GUI runbook for Matt** for the irreducibly-GUI steps (asset-lib SQLite install; FBX import + re-import; inspector node config) — exact menu paths, what-success-looks-like screenshots-to-take.
- **Report** against the §1 four-item gate: PASS/FAIL each, with evidence + any caveat hit.

**Matt does in-GUI (drax documents, Matt clicks):**
- Install SQLite from the Godot asset library (editor-only download flow).
- Import the Free Starter Pack FBX(s) into `Assets/Synty/SidekickCharacters/` + re-import after plugin enable.
- (Optional, if drax's `.tscn` doesn't fully substitute) eyeball the inspector-composed character.

## 4. Coordinate-clean + weapon-as-identity rhymes (carry-forward, not Phase-0 work)

Two design threads to build *toward*, not to resolve in Phase 0:
- **Coordinate-clean discipline** (Stage-3 cutover § 4): when class VFX overlays land (Phase 1+), key them on the **bc coordinate, never a legacy label** — from the first frame. Phase 0 has no VFX, but the project starts label-free.
- **Weapon-as-identity-surface** (Matt 2026-06-14 lock): the Synty `Attachment*` sockets are the literal home of the identity-bearing weapon. When the asset-architecture doc is authored (post-spike), the weapon-socket model is the bridge between the engine's weapon-substrate (the identity root) and the visual form (the Synty rig). Note it; don't build it in Phase 0.

## 5. Done / routing

- **drax:** execute §3; report against the §1 gate. **gandalf authority to fire this Phase-0 spike direct** (Matt "fire" instruction; Mac-side, drax-owned, no paid-spend). drax auto-commits the spike scaffold + harness + runbook per the team commit discipline (work-product of an authorized task); **does NOT push** without Matt's go (default ADR-006).
- **gandalf:** interpret the Phase-0 report → confirm the free path validates the architecture (the gate before the $200 Phase-1 spend); fold the runtime-composition confirmation into the full spike-brief update; THEN the Phase-1 paid vertical slice fires against galadriel's rubric.
- **KR (awareness, not blocking):** Phase-0 is drax-only (no galadriel captures yet — those are Phase-1). Flag for drax-queue sequencing awareness; galadriel engages at Phase 1.
- **Phase 1 (deferred, gated on Phase-0 PASS + Matt's paid-spend go):** the full `drax-godot-vertical-slice-spike-brief.md` recipe — register-2 lift, paid Tier-1/Tier-2 packs, dual-machine workflow, galadriel ≥3.6 scoring.

---

## 6. Phase-0 RESULTS — ALL FOUR GATES GREEN; spirit-swap mechanism PROVEN on the Mac (drax `b046ff5` + `e6a6582`, 2026-06-14)

**Gate #2 (auto-retarget — the load-bearing crux) PASSED** (gandalf-verified, `~/Games/reincarnated-godot-spike/harness_logs/05_retarget_proof.log`): a Synty base FBX imports to `GeneralSkeleton` (88 bones); the jgillich post-import plugin auto-applied bone_map + bone_renamer; **21/21 humanoid-profile bones resolve**; a shared clip drove 6/6 bones; torso+legs+arms expose the SAME skeleton → **one animation set covers the whole modular wardrobe, no per-mesh hand-rigging, no DB.** The "can't hand-rig infinity" crux that broke the 2D path is dissolved. This is the de-risk that actually decides the pivot — it holds on our own Mac + content.

**Design-coherence note (gandalf):** the shared `GeneralSkeleton` that makes retarget work is the SAME rig that hosts the weapon/gear `Attachment*` sockets named in `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 5 as the visual home of the identity-bearing weapon. Gate #2 therefore validates the asset-layer foundation for BOTH pillars at once: **spirit-swap** (one animation set across infinite forms — the differentiation pillar) AND **weapon-as-identity** (the identity-bearing socket rides the shared rig). The two design threads converge on one honest foundation.

**Gate #1 (DB-half) / #3 / #4 — UNBLOCK PATH TRACED (was the wall Matt hit):** the `Proto_Side_Kick_Data` DB the plugin reads is NOT in the free pack and the plugin cannot build it. drax traced it to a **free public Synty release** (`SyntyStudios/SidekicksToolRelease` 1.0.39 → raw `Synty_Sidekick.db`, 2.25 MB) — Synty's Unity `ToolDownloader.cs` auto-fetches it; the Godot plugin does not; jgillich's itch page never documents it (another user, DRY1994, hit the identical wall, no author reply). drax confirmed in-session: schema-correct, contains every free-pack part, `part_location` matches the extraction layout → drop-in. Two fixups: (a) `part_location` Windows-backslash → forward-slash; (b) `combine()` hardcodes a consolidated `SK_BaseModel.fbx` absent from the free pack → repoint `sk_base_model` at `SK_HUMN_BASE_01_10TORS_HU01.fbx` (within-seam plugin tweak).

**Gate #1 (DB-half) RESOLVED + #3 + #4 PASSED (Matt-authorized option 1; drax `e6a6582`):** the official public `Synty_Sidekick.db` (release 1.0.39, 2,252,800 bytes) installed at `Assets/Synty/SidekicksToolRelease/.../Database/Proto_Side_Kick_Data`; fixup (a) backslash→slash applied (zero backslash rows remain). drax chose base-model fix (i) — repoint `sk_base_model` at the real `SK_HUMN_BASE_01_10TORS_HU01.fbx` (one greppable line, no duplicated binary, Synty tree stays single-source) — and found a **third** paid-pack-only hardcode the brief didn't list (`get_material()` loads `T_ColorMap.png`, absent from free pack → repointed to per-species `T_HumanSpecies_01ColorMap.png`). All three patches `// TODO(drax)`-annotated as Phase-1 fork-points.

- **Gate #3 (bake-time composition) PASS:** the 13-part Human composes, saves to a standalone `baked_form_01.scn`, reloads in a fresh context **with no creator/DB in play** — carries the 88-bone skeleton + 13 SK_ mesh parts + 13 surfaces. Evidence: `harness_logs/08_baketime_compose_db_installed.log`.
- **Gate #4 (runtime composition = the spirit-swap mechanism) PASS:** 13 parts compose live in a headless SceneTree, then the **entire wardrobe** spirit-swaps on the **same live node** (bare human base → Starter knight armor; 13 parts re-confirmed post-swap). Timing on the M2 Mac: first compose ~15 ms; cold swap to a never-loaded wardrobe ~150 ms (one-time FBX import); **warm spirit-swap ~7.5 ms, consistent** — that warm number is the real in-game swap cost. Rendered visuals (`09_composed_base_render.png` bare body, `10_composed_knight_render.png` post-swap knight) show single body + single shadow; drax viewed both — geometry, rigging, and the live swap are coherent.

**Design-coherence read (gandalf):** gate #4 is the empirical proof of the **spirit-swap differentiation pillar** (Matt-confirmed load-bearing) at the asset layer — a character is recomposed at runtime from `parts` + `colors` + `combine()` on one live rig, at ~7.5 ms warm. The differentiation pillar's "one body, swap the spirit" fantasy is now mechanism-proven on our own hardware, not assumed. Combined with gate #2 (one animation set across the wardrobe), the two load-bearing cruxes the 2D path could not clear are both GREEN in Godot 3D.

**The one honest caveat — and it is the RIGHT caveat:** the swapped-in knight armor renders **flat red.** `get_material()` is per-face albedo atlas-paint and the repointed colormap is the species/skin atlas, not the Starter-outfit atlas. This is **exactly the register-1 floor** — composition/rigging/swap are perfect; only the outfit albedo is wrong. Phase-0 proves the MECHANISM; it deliberately does not touch the VISUAL REGISTER. Clearing flat-color → perceived register-2 is precisely the A-vs-B question the paid vertical-slice spike (the drax Godot brief) is scoped to answer via the GI-lighting + `GPUParticles3D`-VFX + material-shading lift. The flat-red knight is not a failure — it is the register-1 starting line the Phase-1 lift runs from.

**Not exercised (correctly scoped out of Phase-0):** blend-shape Godot #10402 (no `body_shape_preset` set; flagged for the Phase-1 body-variety test). One root-cause recorded for Phase-1 callers: `SidekickCharacter.parts` is a typed `Dictionary[Part, String]` — assigning an untyped dict via `set()` is silently rejected by Godot; the harness now passes typed dicts as a real engine caller would.

**IP hygiene (verified):** committed local-only (`e6a6582`) — project source, harnesses, scenes, docs, TEXT logs only. **No Synty IP committed** — DB, FBX, render PNGs, and the baked `.scn` are all gitignored and confirmed absent from the tree. Spike is a local throwaway repo — no remote; nothing to push.

---

**Signed:** gandalf, 2026-06-14
**For:** the Godot spike Phase-0 free-validation design session — prove the Godot 4.6.3 + jgillich-plugin + Synty-Free-Starter-Pack pipeline works end-to-end on the Mac (install, auto-retarget import, bake-time AND the code-evident runtime composition that confirms the spirit-swap mechanism) at $0 before the paid Phase-1 register-2 vertical slice; drax scaffolds + harnesses + runbooks headlessly, Matt clicks the irreducibly-GUI steps, gandalf interprets the gate.
