# GANDALF CONTINUATION BRIEF — expansion census + re-key prep (non-top-model session)

> **PASTE INTO EXACTLY ONE SESSION** — a fresh gandalf session on a cheaper model (Matt's usage-offload directive 2026-07-12: conserve top-model spend). Adopt the gandalf role (read `.claude/agents/gandalf.md` + OP skill), run OP §1 session-start LIGHTLY (ground-state + serial-content-emission tracker thirteenth entry only), then THIS brief governs. **Mechanical execution ONLY: no Matt-facing elicitation, no new rulings, no vocabulary invention.**

## Binding rulings (2026-07-12 — violating any of these is the failure mode)

1. **Engine frame = schema of record**; corpus re-keys INTO the engine key. Spec: `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` (read in full).
2. **RETIRED vocabulary:** "core" (for the founding 35+13) · "anchor"/"pilot" · kit-rank grades · **any numeric roster target**. Use: founding roster / expansion roster; cell-status = occupied-by-us / genre-attested / genre-negative / whitespace.
3. **Selection principle (Matt verbatim):** *"simple coverage of the count of genre kits, weighted by the longevity/lineage."* The census DESCRIBES this surface; Matt selects. Never propose roster counts.
4. Measured-vs-projected law (corpus rows never carry measured values) · name-lineage ≠ cell-lineage (separate columns, divergence never silent) · no season-N framing · no sleep/timezone framing · renderer law chart=render(data).
5. **Method laws (V4/V4-r2, verbatim):** wildcard test `set(x) <= {'_'}` (multi-char abstain) · **completeness filters precede ranking everywhere** · positives-only matching, negatives tallied separately · comparable-slot minima (R1≥5, R2≥4, R3≥3) · `assert len(axes)==6` on every roster row.

## Read-first (self-contained; do NOT broad-walk the archive)

`views/corpus-rekey-spec-v1.md` · `views/README.md` · `views/V4r2-roster-adjacency-rebuilt.md` · `views/roster-atlas-rebuilt-v1.csv` · `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv` + `rdr-kit-atlas-generator.py` (code vocabularies).

## Unit A — Expansion census (fires first)

Deterministic script over v3 CSV **canon rows only** (exclude mobile roster/bench source rows; count negatives separately, never in coverage):

- Bucket by the 6-slot engine prefix (bc6) — report also a 5-slot ex-commitment rollup where commitment is abstained.
- **Per cell:** kit count · distinct games · tier mix · **longevity = distinct-era count** (flag cross-decade recurrence, e.g. d2→poe2) · lineage-chain presence · GX families present · negative count (separate column).
- **Status join** vs `roster-atlas-rebuilt-v1.csv`: occupied-by-us / genre-attested / genre-negative / whitespace.
- **Ruled-weight column (transparent first cut, Matt's eyeball governs):** `kit_count × distinct_era_count`, cross-decade flag alongside. Do not invent fancier weights.
- **Mechanics cut** (feeds V3 + Matt's "I may choose all mechanics if I can"): per GX family — cells attested, games spanned, whether any founding-roster kit occupies them.

**Outputs:** `views/expansion-census-v1.csv` + `views/expansion-census-findings.md` (≤2 pages: top unoccupied genre-attested cells by ruled weight; GX/mechanics coverage table; med/var-skew context note carried from V4-r2 F2).

## Unit B — Six re-key prep surfaces (decision surfaces for Matt sessions)

One doc each at `views/rekey-prep/<slot>-prep.md` (≤2 pages each), slots: **geo · ctrl · mob · def · econ · elem**. Per doc:

1. Corpus code frequency table (from v3 CSV, decoded via the generator's maps)
2. Engine vocabulary of record — locate by grep in `~/Games/reincarnated-engine/src/reincarnated/`: geo → 16-type geometry palette (generation seam); ctrl → role-orientation taxonomy (damage/support/control/hybrid, 2026-05-08); mob → move-policy/movement-verb surfaces; econ → `_ENERGY_CONFIGS` + doc-48 assigner + Axis-5 cost-TYPE bins + T4 doors; elem → `STAT_ELEMENT_POOLS` (8-element mapping ruling is QUEUED — present options only); def → **greenfield**: survey engine mitigation surfaces (`canonical/reap-die-rise-engine/` mechanical-reality doc §3) and present a candidate vocabulary
3. PROPOSED mapping table with per-mapping confidence + explicit residue rows
4. Open forks as **options + tradeoffs + genre precedent, UNRESOLVED** (ELICIT shape — Matt rules later; resolving them yourself is the failure)
5. econ prep additionally emits the **mechanics-gap census**: unmappable econ codes (ammo/reserve/draft/recipe/harvest…) = candidate engine mechanics → feeds pause-2/V3

## Unit C (optional, if budget remains) — V7 seed refresh

`views/V7-seed.md`: the rebuilt whitespace set (K3 · K19 · the med/var block) with NN± textures from V4-r2 §2, classified frontier-vs-warning per views README V7 rule.

## Report + hygiene

- Auto-commit per CLAUDE.md (no push). Append ONE line to the serial-content-emission tracker thirteenth entry recording artifacts landed (do NOT restructure the tracker; do NOT touch PART F body — §F.4 is Matt-gated).
- Final note: `views/continuation-report-2026-07-12.md` (≤1 page): artifacts, anomalies, open items for Matt-session gandalf.
