# Demo-VFX `archetype_tag` coupling sweep — Stage-3 BC-cutover pre-check (READ-ONLY)

**Type:** read-only audit (presentation surface). No behavior change. Re-pointing, if needed, is a follow-up.
**Date:** 2026-06-14
**Author:** drax
**Authority:** gandalf §3.2 + §4 (`agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md`)
**Gates:** Stage-3 irreversible deletion of the start-of-pipe legacy `archetype_tag` machinery.
**Surface swept:** `reincarnated-demo/` (Pixi.js — the LIVE player surface; Godot is a spike, not a commit).

---

## 0. TL;DR — the gate answer

**NO demo VFX coupling would break the rendered scene on legacy `archetype_tag` deletion.**

There is exactly ONE code-level coupling that READS the to-be-deleted symbol for a visual decision (the body-silhouette spec lookup in `sprites.ts`/`archetypeRenderer.ts`), and it is already **defensively null-guarded** — it falls through to a procedural fallback when the lookup misses. On the CURRENT live season data (`season_002011`) the player-class tags (`holy_controller`, `lightning_mage`, `physical_grappler`, `experimental`) **already miss** the demo's spec table, so that path is already exercising its fallback in production. Deletion makes the field absent → the same already-live fallback fires. No black screen, no crash.

Two non-visual UI text labels also read the field (class-select card + character sheet) — they would render `undefined` text after deletion. Cosmetic, not a VFX break, but they should be re-pointed to `PlayerClass.name` for cleanliness.

The Layer-2 class-archetype VFX overlays gandalf flagged (Starcaller / Necromancer / Frostwindz — main.ts ~2243 and the cast-dispatch at ~367 / ~1899) are **SAFE**: they key on `PlayerClass.name` + `dominant_element`, NEVER on `archetype_tag`. They are already coordinate/name-clean.

**Verdict: the demo-VFX prereq CLEARS the Stage-3 gate.** No re-point is REQUIRED before the engine deletes. Two cosmetic re-points are RECOMMENDED (follow-up, not gating).

---

## 1. The coupling table

| # | Location | Keys on | Used for | RISK / SAFE | Re-point target |
|---|---|---|---|---|---|
| 1 | `src/visuals/sprites.ts:130` `getSpec(archetypeTag)` — fed from `main.ts:1509` (enemy `slot.spec.sourceData.archetype_tag`) and `main.ts:2108` (player `cls.archetype_tag`) | legacy `archetype_tag` | Selects body-silhouette `BodyKind` (mage/warrior/archer/...) for the procedural sprite | **SAFE-by-fallback** (reads to-be-deleted label, but already null-guarded; already missing on live data) | `dominant_element` + `role` (or `bc_target` coordinate). For player classes, chierit char-sprite path already supersedes this in most cases. |
| 2 | `src/ui/classSelector.ts:131` `new Text(cls.archetype_tag, ...)` | legacy `archetype_tag` | Class-select card subtitle text (`fire_mage` etc.) | **RISK (cosmetic)** — renders `undefined` text after deletion; not a VFX/scene break | `PlayerClass.name` (already shown as card title) — or drop the line; it's redundant with name |
| 3 | `src/ui/characterSheet.ts:170` `_t(cls.archetype_tag, ...)` | legacy `archetype_tag` | Character-sheet header label | **RISK (cosmetic)** — renders `undefined` text after deletion | `dominant_element` + `role`, or drop |
| 4 | `src/main.ts:2098-2102` | (comment only) | Notes the `archetype_tag` subtitle was already REMOVED from normal display (`_playerSubtitle = ''`) per Matt v0.26 playtest | **SAFE (dead reference)** | n/a — already empty string |
| 5 | `src/visuals/frostwindzClassArchetype.ts` `deriveArchetypeKey(className, dominantElement)` — called from `main.ts:367` (`className: caster.name`) + `main.ts:1899` (`className: player.name`, `classElement: player.dominantElement`); prewarm `main.ts:2243` | `PlayerClass.name` (string substring) + `dominant_element` (fallback) | Layer-2 class-archetype VFX overlays (Starcaller / Necromancer / holy / shadow / lightning) — the §7-flagged overlays | **SAFE** — never touches `archetype_tag` | none needed (already name/element-keyed) |
| 6 | `src/visuals/frostwindzClassArchetype.ts:41,246` (comments) | references a FUTURE field `spirit.class_archetype` (VS2b, not yet emitted) | documentation of intended VS2b key | **SAFE** — `class_archetype` is the END-of-pipe composed field, NOT the start-of-pipe `archetype_tag`; distinct symbol | n/a |
| 7 | `src/ui/skillTree/types.ts:57` + `fixtures/sampleTree.ts` (`archetype_tag: 'fire_mage'`) | hardcoded fixture string | Skill-tree FIXTURE/sample data (not engine output) | **SAFE** — synthesized fixture, not real engine output; isolated to dev fixtures | n/a (or scrub fixture if desired) |
| 8 | `src/types/engine.ts:247,285` `archetype_tag: string` | TypeScript type decl | Type shape of consumed `ClassData` / monster data | **SAFE (type only)** — when engine drops the field, mark optional/remove; no runtime read | make optional `archetype_tag?: string` when engine MIGRATION.md lands |

### The "archetype" near-misses that are NOT the legacy label (confirmed SAFE)

- `src/audio/audio.ts` `geometryToArchetype()` — maps `geometry_type` → sonic archetype group (G1-G9). Keys on **geometry**, not the label. SAFE.
- `src/ui/combatHud.ts`, `src/visuals/codeManuVfx.ts`, `src/visuals/frostwindzPhysical.ts` — "archetype" in comments/VFX naming refers to **geometry_type** shape families. SAFE.
- `archetypeRenderer.ts` filename/`getSpec` — the only one that takes the legacy tag as a key (= row 1).

---

## 2. Why no VFX break (the mechanism)

`createCombatantSprite` (`sprites.ts:102`) takes `archetypeTag = 'unknown'` (defaulted) and at line 130 does:

```ts
const spec = getSpec(archetypeTag);
if (spec) { drawBody(body, spec.body, primaryColor); }
else { /* console.warn + procedural circle fallback */ }
```

`getSpec` (`archetypeRenderer.ts:63`) is `return SPECS[archetypeTag] ?? null;` — a pure null-guarded map lookup. The `SPECS` table holds the OLD `{element}_{role}` keys (`fire_mage`, `water_controller`, ...). The CURRENT live season (`season_002011`) emits tags like `holy_controller`, `lightning_mage`, `physical_grappler`, `experimental` — **most already miss the table**, so the procedural fallback is ALREADY the live path for player classes (and the chierit character-sprite path in `characterSprites.ts` supersedes the procedural body for mapped player chars regardless). When the engine deletes `archetype_tag`, the field becomes `undefined` → `getSpec(undefined)` → `null` → same already-live fallback. The deletion changes nothing the player sees.

**This is the discriminator gandalf asked for:** the demo does NOT gate any rendered VFX overlay on the legacy `archetype_tag`. The one place that reads it for a visual is fallback-protected and effectively already inert on live data.

---

## 3. Recommended follow-up (NOT gating — re-point is a separate task)

When the engine ships its `archetype_tag`-deletion MIGRATION.md, drax does a small cleanup pass:
- Row 1: drop the `archetype_tag` argument from the two `createCombatantSprite` call-sites; the body path is already fallback/chierit-driven. (Or re-key on `dominant_element`+`role` if a per-role silhouette is still wanted for monsters.)
- Rows 2-3: re-point the two UI text labels to `PlayerClass.name` / `dominant_element`+`role`, or drop them.
- Row 8: make the type field optional, then remove, tracking engine MIGRATION.md.

None of this blocks the engine deletion. It is post-deletion hygiene. Tracked in `reincarnated-demo/AGENT_STATE.md`.

---

## 4. Portable spec for the Godot co-brief — "VFX-keys-on-coordinate-not-label"

The Pixi sweep and the Godot vertical-slice spike are the SAME move. The principle, stated so the Godot build starts coordinate-clean from frame one:

> **VFX, sprite selection, and any per-class presentation decision key on the END-of-pipe coordinate or the player-facing name — NEVER on the start-of-pipe `archetype_tag` (`{element}_{role}`) label.**

The label is the vestigial symbol the engine is spending three stages to delete. Re-importing it into the renderer re-creates the generation→presentation coupling and re-imports the trap.

### Safe key list (what Godot VFX/sprite logic MAY read)

| Safe key | Source field | What it drives |
|---|---|---|
| `PlayerClass.name` | end-of-pipe LLM-composed nameplate | nameplate text; substring-matched class-archetype VFX overlay (the Frostwindz pattern) |
| `dominant_element` | end-of-pipe element | element glow ring, element particles, element-based VFX-overlay fallback |
| `canonical_element` (per-skill) | per-skill element | per-skill VFX element tint |
| `geometry_type` (per-skill) | per-skill geometry | VFX shape family (burst/beam/arc/point/zone), animation state, audio sonic group |
| `bc_target` (the 8-tuple coordinate) | end-of-pipe BC coordinate | the canonical structural identity; any future coordinate-driven presentation |
| `role` | end-of-pipe role | role-flavored silhouette IF a per-role body is wanted (read role, not `{element}_{role}`) |
| `class_archetype` (VS2b, when emitted) | end-of-pipe composed archetype | the intended future Layer-2 overlay key (distinct symbol from `archetype_tag`) |

### Forbidden key (Godot must NOT read)

| Forbidden | Why |
|---|---|
| `archetype_tag` (`{element}_{role}`) | start-of-pipe legacy label; being deleted root-and-branch (Stage 3). Reading it re-imports the deleted coupling. If a per-role decision is wanted, read `role` directly + `dominant_element` directly — never the concatenated label. |

### Godot ownership note

The Godot vertical-slice spike owner builds against the safe-key list above from the first frame. If drax owns the Godot spike, this principle is the renderer contract for it. If owned elsewhere (mantis/UE or a separate Godot spike owner), this note is handoff-ready: the safe-key table IS the spec — wire VFX/sprite logic to those fields, treat `archetype_tag` as if it does not exist. The Pixi demo proves the pattern works (Layer-2 overlays already run name+element-keyed).

---

## 5. Disposition

- **Gate:** demo-VFX prereq **CLEARS**. No RISK row breaks the rendered scene on `archetype_tag` deletion. Stage-3 deletion is unblocked from the presentation side (still gated on the other prereqs + gamora reference-audit per §3).
- **drax follow-up:** post-deletion cosmetic re-point (rows 1,2,3,8) — non-gating, tracked in AGENT_STATE.md.
- **Godot:** §4 portable spec is the renderer contract — coordinate/name-clean from frame one.

**Signed:** drax, 2026-06-14
