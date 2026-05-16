# `research/` — Knowledge gathering and data curation surface

This directory is the shared output surface for **Legolas** (researcher) and **Elrond** (data steward), plus commissions targeted at them.

## Directory structure

| Path | Owner | Purpose |
|---|---|---|
| `commissions/` | knight-rider + gandalf (commissioners) | Active and historical research commission briefs. Format: `<YYYY-MM-DD>-<commissioner>-<topic>.md`. Legolas and Elrond read these as their work queues. |
| `knowledge/` | Legolas (Mode A output) | Analytical research findings. Subdirectory per topic. Files named `<YYYY-MM-DD>-<slug>.md`. |
| `catalogue/` | Legolas (Mode B output) | Systematic catalogue crawl raw output. Subdirectory per source. JSON Lines or CSV. |
| `curated/` | Elrond | Curated state of research data (cleaned, structured, queryable). Includes Elrond's `MIGRATION.md` for schema versioning on non-engine data layers. |
| `scripts/` | Elrond | Tool scripts for curation, migration, abstraction analysis. Not production code. |

## Ownership boundary with engine telemetry

- **Engine telemetry** (`reincarnated-engine/src/reincarnated/telemetry/`, `data/telemetry.db`) — owned by **star-lord**
- **External / cross-cutting data** (everything under this directory) — owned by **Elrond**
- Cross-DB joins require coordination via ADR-004 (MIGRATION.md on both sides)

## Commission flow

1. **Commissioner** (knight-rider, Gandalf, or other agent) drafts a commission file in `commissions/`
2. **Legolas** picks up at session start; executes; outputs to `knowledge/` or `catalogue/`
3. **Elrond** (if applicable) curates raw output into `curated/`; runs abstraction analysis
4. **Commissioner** reads findings and proceeds

Findings are append-only; old findings stay for historical reference. New work re-runs rather than overwrites.
