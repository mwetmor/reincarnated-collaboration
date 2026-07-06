# Glance

One URL that shows the true state of the project — trackers, queues, blockers,
your-move items — **derived from canon on every push, authored by no one.**

Founding principle: **the glance layer is DERIVED, never authored.** Canon stays
in git as markdown; a deterministic parser emits a state model on every push; a
thin static app renders it. **No DB, no server, no LLM anywhere in the truth path.**

Owner: drax (web seam). Contract: `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`
(§ 3 state.json) + `canonical-doc-format.md` § 7 (the five legislated shapes,
RATIFIED jack-ryan 2026-07-06) + engineering-disciplines Discipline #60 (CI-fail-loud).

## Architecture (boring on purpose)

```
push to canonical/**  →  GitHub Action  →  parser (parser/parse.mjs, deterministic)
                                            ├── app/public/state.json  (§ 3 contract)
                                            ├── MALFORMED shape  → CI FAIL (file+line)  [Discipline #60]
                                            └── dangling gates-on → warning badge (not a failure)
                          →  static deploy (Vercel — the loadout stack)
```

- **`parser/parse.mjs`** — the deterministic canon → `state.json` parser. NO LLM,
  NO network, NO judgment. Reads ONLY the four `canonical/current-to-end-state/`
  trackers + `canonical/matt_decision_needed/README.md` + `canonical/matt_to_do/README.md`.
  **Never touches the engine tree.**
  - `node parser/parse.mjs` — write state.json; exit 1 on any MALFORMED.
  - `node parser/parse.mjs --report` — list ALL malformed findings in one pass
    (the reconciliation surface), then exit non-zero.
- **`app/`** — Vite + React 18 + Tailwind static SPA. Renders Tiers 0–2.

## The parse contract — the five legislated shapes (canonical-doc-format § 7)

1. **STATUS banner** — first `**STATUS:**` blockquote (stamp + date + raw line).
2. **SESSION-DELTA LOG** — `### YYYY-MM-DD — headline`, newest-first, latest governs.
3. **Queue rows** — table (or modeled bullet) whose first cell begins with a row ID,
   carrying a status prefix (`✓ ⛔ ⚖ PARKED IN-FLIGHT OPEN`).
4. **`gates-on:` tokens** — `gates-on: <token> [(qual)] [· <token> …]` (AND-semantics).
5. **Matt queues** — Q/T-style IDs in the two README indexes; struck/appendix = resolved.

### CI severity split (Discipline #60 / § 7.6) — the discipline that makes CI livable

- **MALFORMED** (exactly 3 conditions: broken table structure on an ID-bearing row;
  unparseable delta date; duplicate row ID within one board) → **CI BUILD FAILURE**, file+line.
- **UNRESOLVED** (dangling `gates-on:` token) → **warning badge** + global counter. Visible debt, not a broken build.
- **ABSENCE** is never an error — a doc with no delta log, a table that isn't a queue: fine, rendered as prose.

## Tiers (v1 = Tiers 0–2, Matt ruling)

- **Tier 0 — the glance** (`Glance` in App.tsx): header strip (your-move pixel =
  open matt_decision_needed count · matt_to_do · last-commit age · dangling count),
  four tracker cards, "Since you last looked" (localStorage watermark = max delta-date seen).
- **Tier 1 — the drill** (`Drill`): queues as sortable/filterable tables (status/owner/sort),
  delta timeline (latest full, older collapsed), rendered under the § 4 supersession law
  (STATUS banner → latest delta → older → body). Parser enforces ORDER + BANNERS only.
- **Tier 2 — the source** (`Source`): modeled render + every claim deep-links to
  file+line on GitHub + client-side search.

## Staged — NOT built in v1 (§ 7 of the spec; clean seams left, no implementation)

- **Tier 3 — dependency graph** (`gates-on:` tokens as a live graph). Entry criterion:
  one full board cycle where new/edited open rows carry tokens + dangling rate < ~10%.
  Seam: `state.json.dangling_gates` + every row's `gates_on[]` already carry the graph edges.
- **RUN-STATE pane** (emission runs / registry / cert status). Entry criterion: the W1 #8
  run registry exists with ≥1 registered run. Seam: a second top-level view alongside `glance`.

## Local dev

```bash
cd app
npm install
npm run parse        # regenerate public/state.json from live canon
npm run dev          # vite dev server
npm run build        # parser (fail-loud) + tsc + vite build  → dist/
npm run build:preview  # tolerant build (writes state.json even on MALFORMED) for local preview
```

## Deploy

Standalone Vercel project, Root Directory = `glance/app`. `vercel.json` sets the
SPA rewrite (all routes → index.html) — smoke-tested locally before every deploy
(the May-12 missing-rewrite 404 lesson). Production deploys are Matt-authorized (ADR-006).
