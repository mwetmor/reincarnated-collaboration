# Dispatch — 2026-06-13 — rocket — Season 001010 generation RUN (keystone corpus)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-13 — fires on Gate-2 PASS (jack-ryan cleared the Session 3/4 cascade 2026-06-13, no BLOCK). In-scope to the authorized BC-measurement keystone. KR fires; push-to-remote is Matt's only gate, at keystone-close.
**Status:** CLEARED (Gate-2 PASS). Fire per the resource-discipline sequencing below (project → smoke → full).
**Estimated effort:** dominated by the full-corpus generation wall-clock + LLM identity calls — project before firing (see resource discipline).
**Acceptance:** A generated Season 001010 KIT corpus from the live Session 3/4 cascade (the corpus the rocket-generation-handoff held-criteria, line 172, names — NOT the stale 2026-05-16 `exports/season_001010/` spatial corpus, which is a naming collision). Generation-time fields populated across the corpus; the cognitive-load + coupling-depth distribution surfaced as an explicit deliverable (the gandalf early win).

## Context

The Session 3/4 generation cascade is Gate-2-cleared (jack-ryan 2026-06-13: 180 tests re-verified, vestigial-ontology zero-branches confirmed, commits on engine main). KR's ground-truth pass established that the new-cascade Season 001010 corpus has NOT been generated (the kit_space chronicle's last event is 2026-06-02 QDX-5, pre-cascade). This RUN produces it.

This corpus is the keystone's generation link. It feeds three things:
- **EARLY WIN (no build dependency):** the `cognitive_load_score` + `coupling_depth` distribution across the corpus is GENERATION-TIME data (Items 3 + 5). gandalf's Gate 2 (Q4 coupling — whether coupled kits cluster near LOW/MEDIUM/HIGH cognitive-load bin boundaries) resolves from THIS distribution alone, WITHOUT waiting for the gamora BC-measurement build. Surface it explicitly.
- **Downstream (held until gamora BC pipeline lands):** Items 7 (investment_profile) + 8 (vestigial-label reachability report) read MEASURED bins — they fire AFTER both this corpus AND gamora's BC-measurement pipeline exist. This RUN does NOT execute the measurement-time items; it only produces the corpus + generation-time fields.
- **Unblocks gamora live-wiring:** if the corpus contains a charge-stack kit (`energy_type == 'charge-stack'`) and/or companion records, that unblocks gamora's Part B kit→CombatantState wiring + proxy-kernel companion/MONSTER_PACT follow-ons (currently dead code — golden-master 0/60 — because the existing corpus predates those types). Flag their presence/absence in the completion record.

## Soft dependency — elrond faction table (coordinate, do not hard-block)

elrond's Q10 FACTION_LOOKUP_TABLE redraw (`2026-06-13-elrond-q10-faction-lookup-table-redraw.md`, Gate-1 PASS, ~1–2h) ideally lands BEFORE this RUN so identity generation emits real factions instead of UNASSIGNED. KR is sequencing elrond first. If the table is populated when you fire: factions are live. If not: factions emit UNASSIGNED + nearest-match log (honest, backfillable) — the early-win distribution and corpus are unaffected. Confirm faction-table state with KR before the FULL fire; the SMOKE can run regardless.

## Resource discipline (Discipline #1.1 + #2.1 — REQUIRED, this is a large RUN)

1. **Pre-fire resource-bounds projection (#1.1):** before the full fire, project peak memory, LLM cost, and wall-clock for the target corpus size. Anchor to measured priors: the QDX-5 37-kit run was $1.14 / 10.6 min; Phase-5 per-kit LLM identity calls are the LLM-scaling surface (gamora flag). Faction-completeness floors (Item 9: ≥10 in-band/faction, ≥20 NPC/faction, ≥40 monster/binding-category across ~8–9 factions) imply a large corpus — verify the projected cost/wall-clock against host bounds and surface to KR if it exceeds a routine envelope BEFORE firing.
2. **Smoke first (#2.1):** smoke-test the full cascade end-to-end on a small subset — validate that all generation-time fields populate, the cognitive_load/coupling distribution has sane shape, and the Item 11 cognitive-load prior (HIGH ≥~8%, ≤50% of HIGH carries RESONANCE_LOOP) is trackable. No parallel full regens of the same seed; tag intermediate states.
3. **Then full RUN.**

## Required reading before starting

- `agentic_orchestration/dispatches/2026-06-12-rocket-generation-handoff.md` (the full cascade spec — all items; § 13 sequencing; held-criteria line 172; pass/fail per item)
- Your own completion record at the bottom of that dispatch + the Gate-2 handoff note `rocket/notes/2026-06-12-session-3-4-generation-cascade-gate-2-handoff.md`
- `gandalf/notes/2026-06-12-session-3-core-combat-mechanics-spec.md` § 6 (cognitive load) + § 7 (Q4) — the early-win deliverable
- Faction-table state: coordinate with KR / check `data/identity/faction_lookup_table.json` `records[]` (populated vs empty)

## Deliverables (completion record)

- The Season 001010 corpus (kit_space chronicle event + kit JSONs), tagged
- **The cognitive_load_score + coupling_depth distribution across the corpus** (the gandalf Gate-2 / Q4 early win) — as a table or report KR routes to gandalf
- Item 11 prior check: HIGH cognitive-load bin ≥~8% of in-band corpus? ≤50% of HIGH carries RESONANCE_LOOP? (flag-only; do NOT self-adjust T4 weights)
- Item 9 faction-completeness distribution (flag floors unmet to gandalf/KR; do NOT self-adjust sampling weights)
- Presence/absence flags: charge-stack kit? companion records? bridge-bearing summoner (Golem/Mimic) — the last feeds gandalf's Gate 3 (bridge math) conditional
- Faction state at fire-time (live vs UNASSIGNED-backfill)

## Out of scope

- Measurement-time items 7/8 RUN (held until gamora BC-measurement pipeline lands — separate sequencing)
- The gamora BC-measurement build (simulation seam)
- Any change to the Gate-2-cleared cascade code (this is a RUN, not a code change)
- The weapon/substrate BC clustering line (Cycle 14/15 — different work)

## Tag intent

`rocket/v-season-001010-gen-<n>`. Auto-commit per standing pattern (generation work-product + chronicle event). Push at keystone-close, Matt's gate.

## Gate-2

jack-ryan gates the RUN outputs per seam protocol (his lane) once the corpus lands.

---

**Author:** knight-rider, 2026-06-13. Anchors: rocket-generation-handoff cascade spec + held-criteria; Gate-2 PASS 2026-06-13; Session-3 §§ 6/7 (early-win deliverable).
