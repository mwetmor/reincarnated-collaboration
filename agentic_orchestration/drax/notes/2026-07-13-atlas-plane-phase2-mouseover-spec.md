# /atlas plane — Phase 2 interactive-mouseover spec (GATED, not built)

**Author:** drax (presentation seam) · 2026-07-13
**Commission:** surface the RULED V1.2 Stratified Plane View on Glance `/atlas`, two phases.
**Phase 1:** LANDED (static DB-derived SVG + provenance stamp — tag `glance/v1.10-atlas-plane-1`).
**Phase 2:** THIS DOC — spec only. Build when the two upstream gates close.
**Contract:** `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`
(founding law: DERIVED not authored · no LLM in truth path · no hand-drawn state).

---

## 1. What Phase 2 delivers

Each kit-dot on the plane shows, on hover (desktop) / tap (touch), a
**customer/analyst-facing naming-law label**. This is TEAM tooling — Glance is not
player-facing, so the §7.1 public-labels naming law does NOT gate the surface; but the
*content of the tooltip* is the §7.1 label so the team reads what a customer would read.

To carry per-dot metadata, the plane must be rendered **from DATA, not a flat image** —
the Phase 1 static SVG has no per-dot addressability. So Phase 2 replaces (or augments)
the `<img>` with a plane rendered client-side from a per-dot JSON.

## 2. GATES (both upstream — do not build until closed)

- **Gate (a) — per-dot data JSON.** The plane render (`render_v1_2_stratified.py` class,
  gandalf/star-lord seam) must ALSO emit a per-dot JSON (`render(DB)` → data, same
  provenance class as the SVG). gandalf owns the **label-derivation rule** (§7.1). Until
  this lands, drax has no addressable dots.
- **Gate (b) — elrond S1 columns.** `era_year` + `stabilization_patch` columns from the
  elrond S1 rebuild, for full-precision labels. Until then the label renders NULL-honest
  (mechanical half + game-id NOW; era_year + patch fill in when the columns land).

Neither gate is drax's to close. Flag to KR to route (a)→gandalf, (b)→elrond.

## 3. Data contract — the per-dot JSON (what drax consumes)

The render emits an array of dots (one object per placed kit). Proposed shape — gandalf
owns the authoritative schema; this is drax's consumer-side ask:

```jsonc
{
  "generated_at": "ISO-8601",
  "source_commit": "…",              // git-derived, like plane-provenance.json
  "rule": "movement × delivery × amp-tempo (Q19 LOCKED 2026-07-13)",
  "dots": [{
    "cell": "FREE-MOVE × PROJECTILE",   // §10 cell address = permanent kit identity
    "stratum": "FLAT",                  // FLAT | SPIKY | VAR (amp-tempo band)
    "x": 0.0, "y": 0.0,                 // normalized plane coords (0..1) OR px in the render's viewBox
    "kit_id": "d2-nova-sorc",
    "internal_name": "Nova Sorc",       // internal kit name — fine on Glance (team tooling)
    "public_label": "…",               // §7.1 naming law (see §4); NULL-honest until gate (b)
    "game": "D2",
    "era_year": null,                   // fills in on elrond S1 gate (b)
    "stabilization_patch": null         // fills in on elrond S1 gate (b)
  }]
}
```

**Coordinate discipline:** the dots must carry the SAME coordinate space the SVG uses so
the overlay registers exactly. Cleanest: the render emits both the SVG and the JSON in one
pass (`render(DB)` → {svg, dots}) with a shared viewBox, so dot (x,y) map 1:1 onto SVG
user-space. drax will render the interactive layer against that viewBox.

## 4. public_label — the §7.1 naming law (render rule)

`public_label = "[game-id]-[era year] (v[patch]) + [mechanical description]"`, **NULL-honest**:

- **Renders immediately (Phase-1 data):** `[game-id]` + `[mechanical description]` (the
  mechanical half is derivable from the plane cell + kit facts NOW).
- **Fills in on gate (b):** `[era year]` + `(v[patch])` once elrond S1 adds the columns.
- **NULL-honest rule:** never fabricate era_year/patch. If null, render the label WITHOUT
  that segment (e.g. `D2 + orbital nova burst`), not with a placeholder. gandalf's
  label-derivation rule is authoritative; drax renders exactly what the JSON carries.

## 5. Build approach (drax layout call — decided, not yet executed)

- **Render:** replace the `<img>` in `AtlasPlaneView` with an inline SVG (or a thin
  overlay of positioned dots on top of the static SVG using the shared viewBox). Inline
  SVG is preferred — one DOM tree, dots are real elements, tooltips attach natively.
- **Tooltip mechanism — phone-first:**
  - Desktop hover: native SVG `<title>` on each dot (zero-JS, zero-dependency — the
    "boring on purpose" architecture holds) OR a lightweight positioned overlay if we want
    styled multi-line labels.
  - Touch: `<title>` does NOT fire on tap. Add tap-to-reveal — tap a dot → a small
    pinned label card near the dot (dismiss on next tap / tap-elsewhere). This is the
    load-bearing mobile affordance; native `<title>` alone fails touch.
- **Density guard:** cells with many co-located dots (e.g. FREE-MOVE × PROJECTILE × FLAT =
  53 kits) need jitter/packing so dots are individually tappable at 44px touch targets, or
  a cell-level drill (tap cell → list). Decide against real dot-density from the JSON.
- **Provenance:** same stamp as Phase 1 (source_commit from the JSON), plus a per-dot
  file+line deep-link to the kit's DB/roster source where available (Tier-2 discipline).
- **No LLM, no hand-drawn state:** dots + labels come only from the emitted JSON. drax
  renders; drax does not synthesize labels.

## 6. Sequencing

1. KR routes gate (a) to gandalf (per-dot JSON + label-derivation rule) and gate (b) to
   elrond (S1 era_year + stabilization_patch).
2. When gate (a) lands: drax builds the interactive render against the JSON; labels render
   NULL-honest (mechanical + game-id).
3. When gate (b) lands: labels reach full precision automatically (the JSON carries the new
   columns; zero drax code change if the schema in §3 holds).

Tag on Phase-2 completion per convention (e.g. `glance/v1.11-atlas-plane-2`).
