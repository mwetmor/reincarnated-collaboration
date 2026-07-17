# elrond charge — curate LA + MCD re-harvest into corpus.db (catalogue-only, grain='kit') — FIRED

> **RECONCILIATION RULING (gandalf, 2026-07-16, post-HALT):** elrond HALTed per iron law 7 — correctly. `la-monetization-confound` is a **system-record** (class="system archetype", all emission axes abstain, rider anchor — gandalf-verified against jsonl + run report), not a kit; the brief's asserts below double-counted it. **Ruled: Option A** — curate **57 kit-grain + 1 system-record** (`grain=NULL`, `row_class='system-record'`, precedent = the 18 existing e.g. `tli-sage-elixir`). **Corrected asserts: total=585 · kit=566 · NULL=19 · gear=0 · class=0.** Rationale: the anchor is mandated content (the LA run brief's monetization-confound rider), and the E4 refit's `grain='kit'` predicate auto-excludes it from atlas admission — the GRAIN LAW filtering at consumption, exactly as designed. Laws 1–4, 6–7 unchanged. *This HALT is the grain law's first live catch — of its own author's arithmetic.*

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED
**Authority:** Matt wave-4 ruling 2026-07-16 (decision file `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § WAVE 4): Edition IV = anchored-E3 + **curated LA/MCD** — *"LA/MCD enter via elrond curation then the E4 refit behind pre-registered gates."* This charge is the curation half. The refit half is NOT this charge.
**Sources (verify-gated by gandalf, both pushed):** `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-corpus-la.jsonl` (53 records, commit `da003065`) + `canon-corpus-mcd.jsonl` (5 records, commit `14abd361`) + the two run reports beside them.

## Iron laws

1. **Catalogue-only.** Rows enter `corpus.db` as catalogue citizens. **NO fit inputs, NO `atlas-coordinates-*` writes, NO served-artifact touch, NO leiden/affinity recompute.** Atlas admission happens ONLY at the E4 refit behind its pre-registered gates (grain='kit' predicate + source-exclusion + congruence-to-E3-camera on ratified members) — a separate, later charge.
2. **Grain stamp:** all 58 rows `grain='kit'` (ratified curation-time column). Both corpora are loop-identity grain per the GRAIN LAW (*corpus grain = emission grain*): LA = `la-{identity}` community-named build identities; MCD = `mcd-{archetype}` G3 item-defined loops. Zero gear, zero class rows — if any record looks like a bare item list or a class, HALT and report (none should; gandalf gated the form).
3. **Provenance:** each row carries source = §9.19 five-stage run (spec v2.13), run commit (`da003065` LA / `14abd361` MCD), source_date=2026-07-16. These are the spec-valid successors of the deleted 182 — the provenance chain must make that legible.
4. **Negative twins:** the 6 LA negative records carry the corpus `negative=1` convention (same as the 38-negative trap-skill treatment). Do not drop them; do not count them as positives in any census you report.
5. **Post-curation asserts (fail-loud):** total 527→**585**; `grain='kit'` 509→**567**; NULL-grain unchanged at 18; gear=0; class=0; `la-`/`mcd-` key collisions with existing rows = 0 (the delete left zero residue — verify before insert); engine_key mapping intact, 0 orphans.
6. **MIGRATION entry** in `agentic_orchestration/research/curated/atlas/MIGRATION.md`: curation record (counts, provenance, negative split) + **record the wave-4 supersession**: wave-3 staging law's archipelago-holdout clause is superseded — the admission gate re-attaches to the E4 refit (cite decision file § WAVE 4). The GRAIN LAW + INGEST CLASS RULE entries stand unchanged.
7. **HALT conditions:** schema mismatch vs existing corpus rows · any count assert fails · any key collision · any record failing the grain sniff. HALT = stop, report, no partial writes (transactional or backup-first, your call — state which).

## Return contract

≤15 lines: rows inserted (pos/neg split per corpus) · post-curation counts (total/kit/NULL/gear/class) · collision check result · MIGRATION entry line-range · commit hash. Auto-commit; on index.lock contention wait 5s, retry up to 3×. **NO push** — gandalf verify-gates then pushes.

**Signed:** gandalf — the catalogue grows only through the spec now; these 58 are the proof the law works.
