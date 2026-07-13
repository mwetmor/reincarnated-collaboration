# Atlas plane — per-dot JSON + public-label derivation contract

**Author:** gandalf · **Date:** 2026-07-13 · **Purpose:** un-gate the Atlas Stratified View mouseover (Drax Phase-2, `2026-07-13-atlas-plane-phase2-mouseover-spec.md`).
**This clears gate (a)** — the gandalf-owned half of the Phase-2 gate. Gate (b) — elrond `era_year` — **LANDED this session** (S1 P5, 524/524). So both Phase-2 upstream gates are now cleared for corpus dots.

D6-aligned: this is a **derived** artifact. The render emits it deterministically from `corpus.db`; no authored content, no LLM in the truth path. Drax consumes it; Glance stays a static projection.

---

## 1 — Emitter

`render_v1_2_stratified.py` (gandalf-owned) emits, alongside the SVG/PNG, a sibling **`plane_dots_v1_2.json`** — one record per rendered dot. Committed as a render artifact; Drax's `stage-assets.mjs` copies it to `public/atlas/` exactly like the SVG.

## 2 — Per-dot record schema

```json
{
  "dot_id": "d2-fireball-sorc",            // internal kit_id — team-tooling key, NOT rendered to the public label
  "source": "corpus",                       // "corpus" (478 engine_key) | "roster" (45 overlay)
  "cell": {
    "movement": "FREE-MOVE",                // FREE-MOVE | WALK | ROOTED | UNMAPPED
    "delivery": "PROJECTILE",               // PROJECTILE|ORBITAL|NOVA|ZONE|BEAM|MELEE|SUMMON
    "amp": "SPIKY"                           // FLAT | SPIKY | VAR | null
  },
  "cell_confident": true,                   // false when any axis is UNMAPPED/null (see §5)
  "public_label": "d2-2001 · projectile, spiky tempo",   // derived, see §3; null-honest
  "label_parts": {                          // exposed so Drax can style/segment the hover
    "game_id": "d2",
    "era_year": 2001,
    "stabilization_patch": "v1.10",         // may be null
    "mechanical_desc": "projectile, spiky tempo"
  },
  "negative_canon": false                   // true → render a muted/"historical exhibit" hover treatment
}
```

## 3 — `public_label` derivation rule (naming law §7.1)

Format: **`[game_id]-[era_year] (v[stabilization_patch]) · [mechanical_desc]`** — NULL-honest, two-register, **never renders a trademarked class/skill name.** The internal `dot_id` stays in `dot_id`; it is NOT part of the public string.

- `game_id`: from `canon_corpus.game`. Always present.
- `era_year`: from `canon_corpus.era_year` (P5, 524/524). Always present now.
- `stabilization_patch`: from `canon_corpus.stabilization_patch`. **Sparse (10/524 + 9 mint).** When null → **omit the `(v…)` segment entirely** (do not render "(vnull)").
- `mechanical_desc`: derived from the cell address + strata — a short human phrase, NOT a skill name:
  - movement → "free-move" / "walk-cast" / "rooted" (omit if UNMAPPED)
  - delivery → "projectile" / "orbital" / "nova" / "zone" / "beam" / "melee" / "summon"
  - amp → "flat tempo" / "spiky tempo" / "variable tempo" (omit if null)
  - Wave-A absorption kits (C2a dual-address): append "· proxy-absorbed" so the bridge identity is legible.
  - Join with commas: e.g. `"free-move beam, flat tempo"`, `"rooted summon, variable tempo · proxy-absorbed"`.

**Examples**
- Full: `d2-2001 (v1.10) · rooted projectile, spiky tempo`
- No patch: `poe1-2016 · free-move beam, flat tempo`
- Roster/UNMAPPED movement: `le-2024 · summon, variable tempo` *(movement segment omitted — see §5)*

## 4 — What is rendered on hover (Drax)

The **`public_label`**. Optionally the segmented `label_parts` for two-line styling (title line = `game_id-era (v…)`; subtitle = `mechanical_desc`). **Never render `dot_id`** in the public/customer/analyst view — that is the internal register. (Glance is team tooling, so internal names are *permitted*; but Matt asked specifically for the **public-facing** name on hover, so this contract renders the public register.)

## 5 — The roster movement caveat (from elrond S1 finding)

Roster movement is **S7-emitted**; the 45 roster overlay dots are `movement: "UNMAPPED"` until S7 lands. Consequence for the mouseover:
- **Their labels are fully derivable NOW** (game/era/patch/delivery/amp all present) — hover **works**, with the movement word omitted and `cell_confident: false`.
- Only their **plane position on the movement axis** is pending S7 — not their name.
- The **478 corpus dots** carry `mob_policy_while_casting` → `cell_confident: true`, full label. These are the bulk of the plane and are 100% ready.

**Net: mouseover NAMES un-gate for the whole plane now. Roster POSITIONAL accuracy on the movement axis follows S7.**

## 6 — Sequencing to un-gate
1. gandalf: add `plane_dots_v1_2.json` emission to `render_v1_2_stratified.py` (this contract). ~1 render-code touch.
2. Drax: Phase-2 build — consume the JSON, wire hover targets over the plane. (Static raster can't hover per-dot, so Phase-2 overlays hover hotspots from the JSON coordinates, or moves to a data-driven render — Drax's call per his Phase-2 spec.)
3. Ship. Roster positions refine when S7 emits movement.
