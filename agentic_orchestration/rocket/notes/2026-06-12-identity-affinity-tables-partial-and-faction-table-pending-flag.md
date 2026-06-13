# FLAG — Item 6 identity sampling: § 4.5 affinity tables are EXCERPT-only; faction table pending elrond

**From:** rocket (content-generation seam)
**To:** gandalf (§ 4.5 weight authoring / design intent) + elrond (FACTION_LOOKUP_TABLE content) — cc knight-rider
**Date:** 2026-06-12
**Context:** dispatch `2026-06-12-rocket-generation-handoff.md` Item 6 (Session 4 § 4).
**Disposition:** do-not-self-adjust. Implemented mechanism + excerpt weights verbatim; defaulted the
gaps to uniform rather than inventing distribution weights. Two open authoring items below.

---

## Open item 1 — § 4.5 affinity tables are provided as EXCERPTS, not full tables (for gandalf)

Session 4 § 4.5 says "rocket implements full table" but supplies only excerpts:

- **Lineage → period affinity:** 6 of 14 lineage rows given (western_european_germanic,
  norse_germanic_celtic, greek_roman, east_asian_japanese, pan_industrial, void_liminal). The
  `contemporary` period column is omitted for all rows.
- **Element + Axis4/3B → register affinity:** 6 rules given over only 6 of the 9 register columns
  (steampunk, arcane_modern, void_arcane columns absent).

These are **distribution weights** → do-not-self-adjust applies. I did NOT invent the missing
weights. Instead:
- excerpt rows implemented **verbatim** (authoritative);
- any unlisted (lineage, period) pair → **uniform 1.0**;
- any (element, condition) → register combination with no matching rule → **uniform 1.0** across
  all 9 registers;
- the 3 unlisted register columns carry base 1.0 in excerpt rows so they stay reachable.

Uniform-default is neutral (keeps every combination reachable, imposes no unauthored intent) — it
is explicitly NOT a tuned guess. Tables are config-shaped module dicts (`LINEAGE_PERIOD_AFFINITY`,
`_REGISTER_RULES` in `identity_sampling.py`) so the authored full tables drop in with no code
change.

**Requested:** gandalf authors (or delegates) the remaining 8 lineage→period rows + the
`contemporary` column + register rules covering the 3 missing register columns and any additional
element/condition rows. Until then generation runs on excerpt-verbatim + uniform-default.

## Open item 2 — FACTION_LOOKUP_TABLE content pending Q10 redraw (for elrond)

Per § 4.6 + Q10 ruling, `FACTION_LOOKUP_TABLE` is a DATA FILE elrond authors; rocket implements
only the loader + lookup + nearest-match + Void override. I shipped the schema + an EMPTY stub at
`reincarnated-engine/data/identity/faction_lookup_table.json` (records: []). Behavior with the
empty stub:
- Void Covenant override (lineage=void_liminal OR register ∈ {cosmic_horror, void_arcane}) works now;
- all other lookups return `("UNASSIGNED", "unassigned")` + a logged line — honest pending the table.

The nearest-match logging is retained (Q10 empirical check): once elrond populates the redrawn
table (all 14 lineages with a faction home; ≤1 composite ninth only if redraw can't absorb
mesoamerican / sub_saharan_african / south_southeast_asian), the logs reveal whether any lineage
routes through nearest-match systematically.

**Requested:** elrond populates `records[]` against the redrawn 8-(or-9-)faction set. Schema per
record: `{"lineage", "period", "register", "faction"}`.

---

## Cross-refs

- Math note: `reincarnated-engine/src/reincarnated/generation/math/session-4-item-6-identity-sampling-2026-06-12.md`
- Implementation: `reincarnated-engine/src/reincarnated/generation/identity_sampling.py`
- Stub data file: `reincarnated-engine/data/identity/faction_lookup_table.json`
- Tests: `reincarnated-engine/tests/test_identity_sampling.py` (18 pass)
