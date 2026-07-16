# legolas charge — LOST ARK full run (Mode B, Tier 2b) per pipeline-spec §9.19.2 — FIRED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED
**Authority:** Matt wave-3 ratification 2026-07-16, verbatim: *"I ratify Lost Ark and MCD, conditionally that we take only the best builds and nothing less than."* Logged in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § WAVE 3.
**Governing spec — READ FIRST, IT IS THE LAW:** `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-harvest-pipeline-spec-v2.md` — §1 (identity rule + grain laws G1–G5), §9.19.2 (the LA run spec), §9.19.5 (conditions of ratification), plus the five-stage pipeline (CENSUS→DOSSIER→PROJECTION→RECONCILIATION→AUDIT), POST-CUTOFF LAW, §9.15 sizing-law precedence. Then open ONE existing corpus file in the same dir (`canon-corpus-*.jsonl` — fifteen exist) and match its record form EXACTLY.

## Iron laws (breach-remediation run — this run exists because the last LA ingest bypassed the spec)

1. **BEST-ONLY floor (§9.19.5 law 1, Matt's condition of ratification):** a record enters ONLY if Rank-1-attested (Maxroll LA raid-guide index / `la-builder` planner) or unambiguously community-canonical at the folk-naming bar. When in doubt, leave it out. The floor OUTRANKS the sizing band.
2. **Grain rule:** record = community-named build identity, key `la-{identity}` — NEVER a class, never an item list (§1). *Gravity Training Destroyer* ≠ *Rage Hammer Destroyer*; *Igniter* ≠ *Reflux Sorceress*. Class = HOST rider. Chaos/leveling variants FOLD into the raid parent (G1).
3. **Five stages, in order, with per-stage counts reported.** No stage skipped — the audit trail is the point.
4. **POST-CUTOFF LAW:** era search mandatory. T4/Ark Passive (Oct 2024) = frame reset; post-cutoff classes Wildsoul (2025-02-26) + Valkyrie (2025-08-20); 2026 stratum searched at run. Post-cutoff records c≤0.5 + `dossier-owed`. KR-trunk era-offset: every record stamps WHICH basin (KR vs global) its era refers to.
5. **Riders:** monetization-confound MANDATORY (`spend_stratum`, discounted fame) · support-canonicity signal class (Paladin/Bard/Artist/Valkyrie wing) · negative canon per §9.4 + per-class twin structure.
6. **Sizing:** floor governs — expect ~45–60 if the Rank-1 census holds; under-shoot honest; padding prohibited. HALT + report (don't pad) if the floor yields < 30.
7. **STAGING LAW (§9.19.5 law 3):** output is CATALOGUED-ONLY. Touch NOTHING in the atlas — no corpus.db writes, no fit inputs, no served artifacts. Your emission is the jsonl + report; elrond curates later, and atlas admission waits on the archipelago hold-out pass.

## Emission

- `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-corpus-la.jsonl` — fifteen-corpora form exactly (negatives inline per the form's `negative` flag convention).
- A short run report `canon-run-report-la.md` beside it: per-stage counts, era strata, GX deltas (expected: GX-02 form-shift gains Wildsoul + Shadowhunter Demonic Impulse; GX-19 gauge-economy probe; convergence metric — mature taxonomy predicts ~0 new GX), floor-rejection list (what the BEST-ONLY floor excluded and why — this is Matt's condition made auditable).

## Return contract

≤20 lines: stage counts · records emitted (positive/negative split) · floor-rejections count · era-strata split · GX deltas · new-GX count (convergence check) · paths · commit hash. Auto-commit; if git commit hits index.lock contention (parallel agents active), wait 5s and retry up to 3×. **NO push.** Read-only across the web (Mode B discipline); no atlas writes.

**Signed:** gandalf — fifteen corpora shipped 515/515 valid through this spec; be the sixteenth.
