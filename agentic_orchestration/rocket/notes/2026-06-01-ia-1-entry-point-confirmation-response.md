# IA-1 Entry-Point Confirmation Response

**From:** rocket (engine generation seam)
**Date:** 2026-06-01
**Dispatch:** `agentic_orchestration/dispatches/2026-06-01-rocket-ia-1-entry-point-confirmation.md`
**Authority:** Matt 2026-06-01 strategic reset + pre-commitment ratification LOCK A (rocket autonomous)

---

## 1. Entry-point verdict: CLI-PATH-CONFIRMED

`python -m reincarnated.cli generate-season` (SeasonOrchestrator) is confirmed as the correct IA-1 V1 entry point.

---

## 2. Confirmed invocation + specific arguments

```
python -m reincarnated.cli generate-season --seed 42 --output seasons/
```

**Arguments:**

- `--seed N` (default: 42) — deterministic seed. IA-1 V1 baseline: use default (42) or any integer. No special format required.
- `--output DIR` (default: `seasons/`) — output directory. Written relative to engine cwd. No special format; directory is created if absent.
- `--telemetry-db PATH` (default: `data/telemetry.db`) — telemetry capture. Default is fine for V1.
- `--smoke` (optional) — recommended for pre-V1 sanity pass before full fire (5 classes, 30 fights, ~3-5 min, ~$0.10-0.15).

**No additional arguments required.** CLI default mode is `inverted` (disposition Sub-case 3, 2026-05-19), which is the correct IA-1 V1 mode: mechanical-first + post-convergence coalescence + per-entity LLM naming.

**Do NOT pass `--theme-input` or `--no-coalesce`** — these select non-default modes not suitable for IA-1 V1 baseline.

---

## 3. Pool.json v1.1 consumption — verified

The inverted mode pipeline consumes pool.json v1.1 as follows:

- `select_seasonal_elements()` is NOT called during mechanical generation phase in inverted mode (elements remain null until post-convergence coalescence)
- Post-convergence: `_coalesce_seasonal_theme()` fires — this is where element vocabulary is resolved
- Naming pass: `_name_everything()` called with `elements=None` in inverted mode; Q18 vocabulary enters via `season_theme` string (post-coalescence output element name) + `cosmological_vocabulary` object
- LLM naming picks up pool.json vocabulary through `naming.py` → `elements.slots` dict — this is populated correctly when elements are non-null (baseline mode) or via coalesced theme string (inverted mode)

Pool.json v1.1 reads cleanly. No code changes required. Star-lord's assessment confirmed.

---

## 4. Pre-fire pre-check: canonical library

`foundation/canonical_library.json` EXISTS. CLI checks for this at startup and exits with error if missing. This check passes — no setup required.

---

## 5. Substrate-side V1 pre-fire check

**Generation seam (rocket): READY.**

- `season_orchestrator.py` — operational; inverted mode confirmed end-to-end
- `element/selector.py` + `element/pool.py` — pool.json v1.1 consumed correctly; Drift-14 demote behavior accepted per strategic reset (Option A, star-lord recommendation)
- `anchor/` — `select_seasonal_anchor()` imported and wired at season_orchestrator line 29; READY
- `foundation/` — `_load_foundation()` reads `config/elements.yaml` (canonical-7+1); READY
- `canonical/canonical_library.json` — EXISTS; READY

Drift-14 WARNs at load (58 demoted entries) are expected and acceptable per strategic reset disposition. No rocket-side coordination required beyond this confirmation.

**One operational pre-check for IA-1 V1 fire dispatch:** confirm `ANTHROPIC_API_KEY` is set in execution environment. Without it, CLI falls back to no-LLM mode (WARNING logged, generation proceeds deterministically — no naming). For a properly-named V1 season, key must be present. This is an environment pre-check, not a rocket-seam issue.

---

## 6. Estimated rocket-side wall-clock

0 minutes additional setup. Confirmation-only dispatch. No code changes.

---

## 7. Routing back to KR

**Fire IA-1 V1 immediately at:**

```
python -m reincarnated.cli generate-season --seed 42 --output seasons/
```

Recommended: smoke pass first (`--smoke`) to validate pipeline end-to-end before full regen (~5 min, ~$0.10-0.15). Then full fire without `--smoke` for the V1 artifact (~20 min, ~$0.85-1.00).

No architectural amendment surface. No escape-clause trigger. No rocket-side setup dispatch required.

---

**Signed:** rocket (engine generation seam)
**For:** IA-1 V1 entry-point confirmation; LOCK A authority
