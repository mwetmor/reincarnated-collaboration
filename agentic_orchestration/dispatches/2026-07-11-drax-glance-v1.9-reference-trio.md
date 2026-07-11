# Dispatch — 2026-07-11 — drax — Glance v1.9 reference TRIO (`/coordinates` + `/mechanics` + `/atlas`)

**From:** knight-rider
**To:** drax
**Approved by:** Matt (relay authorization 2026-07-11 — gandalf Lane-2 amendment relay, contract §7.7 amended + committed)
**Estimated effort:** ~2–4 hours (three pages, same machinery as §7.3–§7.6; render-only, zero new parse shapes)
**Acceptance:** nine-page Glance builds and deploys; the three new pages each lead with a FLOW bar parsing their source doc, render the verbatim payload tables/fences, carry TRIPLE-LAW cross-links, and drill-through to `## §N` headings; tag `glance/v1.9-reference-trio-1` shipped.

## Context

v1.8 (`/minigames`, tag `glance/v1.8-minigames-page-1`) shipped. v1.9 is the only outstanding Glance delta. Matt's mobile-track three-layer ruling created a reference TRIO: `/coordinates` (the LATTICE — where a kit can sit), `/mechanics` (the CODEX — what the engine expresses), and `/atlas` (the PROJECTION — how the two map). Everything upstream is done: contract §7.7 is amended and committed, all three source docs carry authored `## FLOW` blocks (verified: substrate L32, mechanical L31, atlas L26), heading conformance is pre-verified (`## §N` counts: substrate 9, mechanical 9, atlas 6 — matching the FLOW stage counts), and TRIPLE-LAW cross-reference language is in all three doc headers.

This is **render-only, locked-decision execution.** Zero new parse shapes — the only parser change is adding three files to the read set. No format-law amendment, no new grammar (if you hit a parse ambiguity the contract doesn't answer, flag via KR — do not improvise grammar).

## Required reading before starting (in order)

1. `agentic_orchestration/gandalf/notes/2026-07-11-lane2-glance-v1.9-amendment-relay.md` — the authoritative v1.9 delta (8-row table + render notes). Self-contained; this dispatch mirrors it.
2. `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` **§7.7 (v1.9, trio form)** — governing contract; also §7.3–§7.6 (page machinery precedent), §7.5/§7.6 (MATT-FACING class), §2.7 (FLOW grammar + quiet rule).
3. The three source docs (your new parser fixtures):
   - `canonical/current-to-end-state/substrate-coordinates.md` (LATTICE — 9 stages, LADDER → SEARCH PROCESS)
   - `canonical/current-to-end-state/mechanical-reality.md` (CODEX — 9 stages, kit anatomy → BUILD LADDER)
   - `canonical/current-to-end-state/projection-atlas.md` (PROJECTION — 6 stages, TRIPLE LAW → fold obligations)
4. Prior Glance build prompt `agentic_orchestration/gandalf/notes/2026-07-09-drax-glance-build-prompt.md` — founding-law recap (derived-never-authored; no LLM in truth path; no server/DB; parse scope).

## Math-before-code

Not applicable — render-only web build, no algorithm/balance math.

## Cross-seam contract change? (Principle 6 gate)

**NO.** Web seam only. No telemetry schema, fight_log key, loadout dict, or export-packet change. The only parser change is a **parse-scope line** — adding three `canonical/current-to-end-state/*.md` files to the parser's own read set (the parser's internal scope, not an inter-seam fixture).

**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

## Scope

- [ ] **Three new pages** — `/coordinates` + `/mechanics` + `/atlas` (nine total). Same page machinery as §7.3–§7.6; no new page primitives.
- [ ] **Parse-scope only:** add the three source docs to the parser read set. Each page's lead FLOW bar parses its doc's `## FLOW` block via the existing §2.7 grammar.
- [ ] **Quiet-bar honesty:** all three docs are REFERENCE REGISTERS with no §2.3 queue rows → bars render all-`quiet` BY DESIGN (§2.7 quiet rule). Navigation, not state. Do NOT invent coloring.
- [ ] **Verbatim payload:** render fenced blocks + tables verbatim (the lattice tables `substrate-coordinates.md` §0/§2; the resolver walkers `mechanical-reality.md` §4; the projection table `projection-atlas.md` §2). These are payload — do NOT parse them.
- [ ] **Per-stage drill-through:** standard §2.7 tap → section deep-link; `## §N — …` headings are the targets (pre-verified `##`, v1.7 Defect-2 class).
- [ ] **TRIPLE-LAW cross-links** near each FLOW bar — each page links the other two, labeled by layer: `/coordinates` "WHERE a kit can sit" ↔ `/mechanics` "WHAT the engine expresses" ↔ `/atlas` "how the two map". `/atlas` is the connective page; its two links are the most load-bearing.
- [ ] **`/` index link tiles** lean for the three reference pages (suggested: one grouped "kit-design reference" tile row; full cards acceptable — your layout call).
- [ ] **`/atlas` renders NO occupancy numbers** — REALIZED ATLAS emission harness is not built (`projection-atlas.md` §4). Render the §2 projection table verbatim; never hand-derive occupancy.
- [ ] **MATT-FACING class** (§7.5/§7.6 precedent): purge-exempt, same-commit stamp law.
- [ ] **Nav order** (if configurable): seat the trio adjacent as `/coordinates` → `/atlas` → `/mechanics` (sample the coordinate → project the fields → verify the surfaces).
- [ ] CI parse passes on the three new globs.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `glance/v1.9-reference-trio-1`.

## Acceptance criteria

- [ ] Nine-page Glance builds + deploys; three new pages routable.
- [ ] Each new page leads with a FLOW bar parsing its source doc's `## FLOW` block; bars render all-`quiet` (correct, not a defect).
- [ ] Verbatim payload tables/fences render unparsed.
- [ ] Per-stage tap drill-through reaches the correct `## §N` heading on all three pages.
- [ ] TRIPLE-LAW cross-links present + correctly labeled on all three pages; `/atlas` links both siblings.
- [ ] `/` index carries lean tiles for the trio.
- [ ] `/atlas` shows the §2 projection table verbatim with NO occupancy numbers.
- [ ] Round-trip: not applicable — no cross-seam contract change in this dispatch.

## Out of scope (explicit non-goals)

- Do NOT build the REALIZED ATLAS emission harness (`projection-atlas.md` §4) or derive any occupancy count.
- Do NOT parse the payload tables/fences/resolver walkers — render verbatim.
- Do NOT invent bar coloring for the quiet reference registers.
- Do NOT add new §2 grammar or amend format-law (flag ambiguities via KR → jack-ryan instead).
- Do NOT block on `projection-atlas.md`'s two pending fold obligations (Matt's mobile Codex doc + mobile Projection-skeleton package). The FLOW block + § structure are stable; folds arrive as content inside existing sections and re-render automatically.
- No dependency on / interaction with the E3, ninth-axis, or ratification lanes.

## Open questions for drax to resolve (document your call)

- Index tile treatment for the trio — grouped "kit-design reference" row vs. full cards (§7.7 rule 5 delegates to you).
- Nav ordering + adjacency mechanism if configurable (recommended `/coordinates` → `/atlas` → `/mechanics`).

## References

- Contract: `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` §7.7 (v1.9, trio form)
- Relay: `agentic_orchestration/gandalf/notes/2026-07-11-lane2-glance-v1.9-amendment-relay.md`
- Prior tags: `glance/v1.8-minigames-page-1`, `glance/v1.7-story-game-pipeline-repoint`, `glance/v1.6-pipeline-flow-1`, `glance/v1.5-kits-page-1`, `glance/v1.4-four-page-split-1`
- App home: `glance/app` (Vite; `App.tsx` / `state.ts` / `md.tsx` / `components.tsx`); parser at `glance/parser`
