# Dispatch — 2026-06-13 — elrond — FACTION_LOOKUP_TABLE Q10 redraw + populate

**From:** knight-rider
**To:** elrond
**Approved by:** Matt 2026-06-13 — Q10 is already RULED (ratified 2026-06-12); this is in-scope execution of a locked ruling. KR fires; no further sign-off needed. Push-to-remote is Matt's only gate, at keystone-close.
**Status:** **GATE-1 PASS (jack-ryan, 2026-06-13) — FIRED.** Clean PASS, no INFO, no BLOCK. jack-ryan verified the ownership split against the stub's own `_authoring_note` (elrond maintains `records[]`; rocket owns the loader) and confirmed the "confirm-loader-contract-before-authoring / STOP-and-flag-don't-modify-loader" guard correctly converts the cross-seam risk into halt-and-flag. Cleared to execute.
**Estimated effort:** ~1–2 hours (data curation against a ratified ruling)
**Acceptance:** `data/identity/faction_lookup_table.json` `records[]` populated so every (lineage, period, register) the sampler can produce routes to a real faction home; all 14 lineages have a non-degenerate faction; rocket's loader + nearest-match + Void override (already landed) returns real factions instead of UNASSIGNED. Nearest-match logging remains meaningful as the empirical check that no lineage routes through fallback systematically.

## Context

This is a PARALLEL unblock on the BC-measurement keystone (off the critical path for gates 1–3, but needed so identity generation is fully live before the generation RUN). rocket shipped the FACTION_LOOKUP_TABLE loader + nearest-match + Void Covenant override as an empty stub (`records: []`); every non-void lookup currently returns UNASSIGNED. Q10 was RULED 2026-06-12 — the table content is elrond's to author.

**Q10 ruling (verbatim, ruling record § 1):** "Redraw the 8 faction boundaries so all 14 lineages land non-degenerately; if mesoamerican / sub_saharan_african / south_southeast_asian genuinely don't fit, add ONE composite ninth faction designed as a real home — never absorption-by-default, never token factions. Rocket's nearest-match logging (already dispatched) supplies the routing data for the redraw."

## Required reading before starting

- `agentic_orchestration/dispatches/2026-06-12-rocket-generation-handoff.md` Item 6 (§ 4 identity sampling; § 4.6 faction derivation; Q10 disposition at § 12)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 1 Q10 (the ruling)
- `gandalf/notes/2026-06-12-session-4-kit-identity-generation-spec.md` §§ 4.2–4.6 (14-lineage / 7-period / 9-register closed enums; § 4.5 lineage→period and element×register affinity tables — committed in `f2fee41`; § 4.6 faction derivation + Void override)
- Current stub: `data/identity/faction_lookup_table.json` (schema_version 1.0; void_override fields already set; `records: []`)

## Scope

- Author the `records[]` keyed by (lineage, period, register) per § 4.6, OR the table structure rocket's loader expects — confirm the loader's key contract against rocket's implementation before authoring (do not guess the key shape).
- All 14 lineages get a real faction home. Add ONE composite ninth faction ONLY if mesoamerican / sub_saharan_african / south_southeast_asian genuinely cannot be absorbed non-degenerately — and if so, design it as a real home, never a token/absorption faction.
- Preserve the Void Covenant override (void_liminal lineage; cosmic_horror / void_arcene registers) already in the stub.
- Keep nearest-match fallback ordering (register > lineage > period) functioning — the redraw should MINIMIZE systematic fallback, and the logging is the empirical proof it does.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**No schema change.** This is data-content population of an existing schema (`records[]` within the already-shipped table shape). rocket owns the loader; you own the content. If you find the loader's key contract needs a shape change, STOP and flag to KR — do not modify the loader (rocket's seam).

## Out of scope (do NOT touch)

- rocket's loader / nearest-match / Void-override code (generation seam)
- The identity sampling weights or the § 4.5 affinity tables (gandalf-authored; locked)
- The lineage / period / register closed enums (locked)

## Tag intent

Data-file commit; no seam milestone tag. Auto-commit per standing pattern (elrond substrate-curation work-product). Push at keystone-close, Matt's gate.

---

**Author:** knight-rider, 2026-06-13. Anchors: rocket-generation-handoff Item 6 + § 12 Q10; Session-1 ruling record § 1 Q10; Session-4 identity spec §§ 4.2–4.6.
