# galadriel charge — Edition-III atlas render: E2.3 head on the ratified Edition-III emission

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Authority:** Matt 2026-07-16 (verbatim): *"(a) - ratify Edition III now"* + *"Agreed. Ratify Edition III"* — the Edition-III freeze is RATIFIED. The public atlas re-vendors from Edition-II to Edition-III data; **your render is the artifact drax vendors** (in a combined pass with the loadout table-column fix). Fix-pass lineage: E2.1 → E2.2 → E2.3 (rail arrows) → **this** (edition boundary).

## Inputs (ground truth, gandalf-probed)

- **Data:** `agentic_orchestration/research/curated/atlas/atlas-edition3.json` — elrond emission `c5d44a39`, gandalf audit 24/24 ACCEPT, Matt freeze-ratified. Top-level fields confirmed present: `edition: 3`, `register_ref` (v1.3), `fit_layer_frozen_vs`, `counts`, `ghost_field`, `emitted_alongside`, `basis`, `points`, `loadings`.
- **Head:** `agentic_orchestration/galadriel/pipeline/atlas-edition2-e23-render.mjs` — the E2.3 head whose artifacts I verified this session. Rail arrows are CORRECT in this head (`↑ DEPLOY` / `PERFORM ↓` — source glyphs that render OUTWARD under rotate(-90); verified by un-rotated crops). Do not "fix" them.
- **Edition-II artifacts + capture dirs stay BYTE-UNTOUCHED** — they are the served truth until drax re-vendors. Emit ALONGSIDE, never over (same law elrond ran).

## The charge — edition boundary per spec §10 law (new head, enumerated diff)

Cut **`atlas-edition3-render.mjs`** as a byte-copy of the E2.3 head with ONLY the edition-boundary diff. **Every diverging line ENUMERATED in your return.** Edition-bound sites my grep found (you own finding the rest — e.g., the plate title string, which didn't surface in my literal grep):

1. **L173 `ATLAS_PATH`** → `atlas-edition3.json`.
2. **L183 `DEFAULT_OUT_DIR`** → `../captures/2026-07-16-atlas-edition3`.
3. **L344 register gate** — currently fail-louds unless `ghost_field.register_ref == 'feasibility-cuts-register-v1.2'`. Edition-III binds **v1.3**. Re-bind; keep it fail-loud (do NOT loosen to a warning).
4. **L1418 ghost-ledger header** — "… · Edition II lattice" → Edition-III wording. Derive the roman numeral from the emitted `edition` field where feasible; if you keep a literal, the acceptance grep (below) is its guard — state which you chose.
5. **Output filenames** (L1546–1570, 1866–67, 2327 vicinity) → `atlas-edition3-<skin>.svg/png`.
6. **Acceptance greps** (L2103: body must include 'Edition II' + v1.2; L2211–2215 edition-token dedupe counting `Edition-II` / `· Edition II(?!I)`) → re-target to Edition III + v1.3. Note the E2 regex used `(?!I)` to keep "Edition III" from matching "Edition II" — the Edition-III variants need the same anti-substring care in reverse ("Edition III" must not be counted by an "Edition II" pattern, and your new pattern must not accidentally match a future "Edition IIII"— use word/token boundaries).
7. **L2479 integrity-check message** references `atlas-edition2.json` → edition3.
8. **L2518 lit-fraction smoke `≈ 1.7%`** — a CARRIED Edition-II expectation. Edition-III moves it (occupied meso 193→202, pull-lit 2→4). **Re-derive the expected value from the emission's own counts** (litCells/denomMesoFeasible computed from `atlas-edition3.json`), do not carry 1.7 and do not delete the smoke.
9. **Plate title** → **`Build Horizon — Edition III`** (find the title site; same derived-vs-literal rule as item 4).
10. **R7/E2 freeze-regression baselines** (L186–192 FIT_BASE_DIR / E2_PREFIX_DIR / R7_FREEZE_DIR) — the §10.4.3 EDITION REGRESSION LAW crosses this boundary the same way it crossed I→II: **the FIT layer (basis + 506 points + tombstones + axis names) must be independently re-verified BYTE-FROZEN** (`atlas-edition3.json[basis|points]` ≡ `atlas-edition2.json[basis|points]` — elrond asserted it in Stage D; you re-assert renderer-side, fail-loud). Census overlay + ghost field + footer stamp re-emit wholesale — that is what makes it an edition. State how you re-targeted the regression baselines (E2.3 artifacts become the prior-edition reference where the law compares across the boundary).

## Numbers of record (from the ratified emission — acceptance anchors)

corpus **709** · engine_key 683 · active 628 · corpse 38 · system-record 18 · unresolved 39 · pull-function **10** · hybrid **0** · occupied meso **202** · pull-lit **4** · denominators BYTE-IDENTICAL to v1.2: exact **767,411,820** / meso **11,160** / sealed **1,314** / pull **1,080+54**.

Anti-stale greps: `767,411,820` MUST appear in both skins' footers; `819,439,740` MUST NOT appear anywhere; register ref reads v1.3; edition token reads Edition III exactly once per the dedupe law.

## Deliverables

1. Both skins SVG + PNG + provenance JSON → `agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition3/`; **sha256s in the return.**
2. **Enumerated head diff** — every line where `atlas-edition3-render.mjs` diverges from the E2.3 head, with one-line why each.
3. **Check crops, both skins:** (a) both rails — arrows must still read OUTWARD on screen (left on west, right on east); **also emit UN-ROTATED rail crops** (crop the label region, rotate 90° CW so letters read upright — the arrow glyph is then unambiguous: west must read `↑ DEPLOY`, east `PERFORM ↓`); (b) the title plate (`Build Horizon — Edition III`); (c) a NEW-CONTENT cell — the black-hole ROOTED/ZONE pull cell (pull-lit went 2→4; locate lit pull cells from the emission); (d) the footer stamp/denominator line.
4. Acceptance run receipts (the head's own smoke suite, re-targeted, ALL PASS) + the anti-stale grep results.
5. Auto-commit to collab repo. **NO push. NO vendoring into loadout** — drax consumes; your return names exact paths.

## HALT conditions (surface, don't improvise)

`edition` field absent/≠3 → HALT · FIT-layer byte-drift vs Edition-II → HALT · denominator ≠ 767,411,820 or `819,439,740` present → HALT · census counts mismatch the numbers of record → HALT · old arrow strings (`← DEPLOY` / `PERFORM →`) reappear → HALT · any smoke fails after honest re-derivation → HALT with the failing receipt.

**Signed:** gandalf — operationalizing Matt's Edition-III ratification; drax's combined vendor+column pass consumes your output; my verify gates it.
