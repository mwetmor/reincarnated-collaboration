# Gate-2 Finding — EAA-2 Engine skip-flag pattern for R8 + cosmological_vocabulary

**Date:** 2026-06-02
**Reviewer:** jack-ryan (DEV-MODE Gate-2)
**Commit:** `c56db88` (tag: `rocket/v1.4-eaa-2-skip-flag-1`)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-02-eaa-2-engine-skip-flag-retirement.md`
**Implementing agent:** rocket (primary) + co-author star-lord coordination noted; star-lord LLM call infrastructure not modified (no cosmological_vocabulary.py changes needed — flag is evaluated before reaching star-lord's call)
**Authority:** Matt 2026-06-02 + Locks A-P + LOCK M Stage 1

---

## VERDICT: PASS

EAA-2 Stage 1 skip-flag implementation is clean. All acceptance criteria met. No BLOCKs or WARNs. Two INFOs surfaced below — neither blocking.

---

## Acceptance criteria audit (dispatch § 6)

| Criterion | Status |
|---|---|
| 1. Skip flag(s) added to engine (two separate flags) | PASS — `skip_theme_coalescence` + `skip_cosmological_vocabulary` on `generate_season()` and `SeasonOutput` |
| 2. Skip-flag bypass confirmed via single-kit smoke test | PASS — full balance-loop smoke test (5 classes, 30 fights, no_coalesce mode): `season_theme_element=None`, `skip_theme_coalescence=True`, `skip_cosmological_vocabulary=True`, `cosmological_vocabulary=None`, `classes=5`. Exit code 0. |
| 3. No regressions in legacy-path (flag=false reproduces prior behavior) | PASS (structural) — legacy code paths unchanged; `elif` guards preserve existing behavior when skip=False. Legacy reproduction documented in both parameter docstrings and CLI `--legacy-*` flags. |
| 4. MIGRATION.md authored for schema-tolerance extension | PASS — ADR-004 entry appended at tail of `MIGRATION.md`; covers new `generate_season()` params, `SeasonOutput` fields, manifest schema extension, downstream consumer impact table, escape clause status, smoke results. |
| 5. jack-ryan Gate-2 PASS | This finding |

---

## Implementation findings

**[INFO-1] `skip_cosmological_vocabulary` gate structure — minor logic improvement opportunity (non-blocking)**

The gate was restructured from:
```python
if generation_mode == "baseline" and self.llm and not skip_cosmological_vocabulary:
```
to:
```python
if skip_cosmological_vocabulary:
    _log("SKIPPED...")
elif generation_mode == "baseline" and self.llm:
```

This structure is correct and readable. However: when `skip_cosmological_vocabulary=True` AND `generation_mode != "baseline"`, the skip-log fires even though the vocabulary would not have been generated anyway (it was never generated for inverted / no_coalesce modes). The log line is slightly misleading in that edge case ("SKIPPED" implies something that would have run was stopped).

**Disposition:** Non-blocking. The log is informational and doesn't affect behavior. The misleading-log edge case arises only when a caller passes `skip_cosmological_vocabulary=True` (the default) with a non-baseline mode, which will be the overwhelmingly common new-generation path. Suggesting rocket fix if a future patch touches that code path; not worth a separate commit now.

**[INFO-2] CLI `--generation-mode` flag absence — legacy-reproduction is incomplete via CLI alone**

The `--legacy-theme-coalescence` flag help text instructs "Use with `--generation-mode=inverted`" but no `--generation-mode` CLI flag exists. The existing CLI flags are `--theme-input` (selects baseline) and `--no-coalesce` (selects no_coalesce). The `inverted` mode is the CLI default; there is no explicit `--inverted` flag to pair with `--legacy-theme-coalescence`.

This means: legacy reproduction via CLI for inverted mode works implicitly (pass `--legacy-theme-coalescence` with no mode flags → CLI default is inverted → skip disabled → coalescence fires). The help text suggesting `--generation-mode=inverted` could confuse users who look for that flag.

**Disposition:** Non-blocking for EAA-2. The behavior is correct; the help text is slightly misleading. Recommend updating the `--legacy-theme-coalescence` help text in a future patch to say "Pass without mode flags — CLI default is inverted mode" rather than "Use with `--generation-mode=inverted`." Not tracked as a separate dispatch; note for rocket at next cli.py touch.

---

## Discipline review

- **Disc #1 (math-before-code):** No math hotspot in EAA-2 — skip-flag gating is pure boolean control flow with no balance constants or distribution weights. Satisfied.
- **Disc #2 (smoke-test):** Full smoke test executed (5 classes, 30 fights, no_coalesce + skip flags); structural static checks executed (AST + dataclass inspection + gate expression verification). PASS.
- **ADR-004 (cross-seam MIGRATION):** `MIGRATION.md` entry authored; downstream consumer table includes star-lord / drax / elrond / gamora with explicit per-consumer impact and action-required. PASS.
- **LOCK M Stage 1 scope:** Old code paths PRESERVED; only flag gating added; Stage 2 code removal correctly DEFERRED. Scope boundary respected.
- **Principle 6 (additive-only cross-seam):** Manifest schema extension is additive (two new keys; no existing keys removed or semantically changed). Existing consumers using `getattr(..., None)` are unaffected. PASS.

---

## Downstream coordination note

The star-lord co-owner seam (LLM call infrastructure) has no code changes in this commit — correct. `generate_cosmological_vocabulary()` and `_coalesce_seasonal_theme()` are not called when the flags are True (the new default). Star-lord's LLM infrastructure is unmodified and remains available if legacy flags are passed. No star-lord Gate-2 required for this commit.

EAA-5 generation fire: both skip flags default True — EAA-5 will fire with skip-flag-active default without any explicit flag passing. EAA-1 WS1A.4-lite (per-skill flavor naming) composes with skip flags active — Phase B LLM naming still fires when llm_client is available; it handles `cosmological_vocabulary=None` gracefully (existing behavior preserved).

---

## Escape clause status

Confirmed NOT triggered. No downstream hard-dependency on non-null `theme_element` or `cosmological_vocabulary` surfaced. `season_theme_element=None` was already handled by all consumers (no_coalesce mode precedent). `cosmological_vocabulary=None` was already handled by Phase B naming (graceful fallback). Legacy code paths intact.

---

**Gate-2 verdict: PASS**

EAA-2 is COMPLETE. Rocket may update wave-state.md and append dispatch completion record.

**End of Gate-2 finding.**
