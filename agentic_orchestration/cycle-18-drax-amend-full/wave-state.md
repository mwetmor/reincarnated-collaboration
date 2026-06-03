# Cycle 18 — Drax QDX-7-AMEND-FULL — Comprehensive Fix-Forward + Renaming + Faction Integration — Wave State

**STATUS:** 🟢 OPEN (Phase 1 firing 2026-06-02)
**Date opened:** 2026-06-02
**Owner:** knight-rider (orchestrator)
**Authority:** Matt 2026-06-02 verbatim "yes, let's do it all" → gandalf transmission with comprehensive 5-issue routing across 3 seams + KR phasing
**Cycle directory:** `agentic_orchestration/cycle-18-drax-amend-full/`
**Total chain horizon:** ~4-6 sessions wall-clock per gandalf transmission § ESTIMATED HORIZON
**Wave-close criterion:** Phase 4 KR fix-forward record + Vercel preview URL + Matt signal

---

## 0. Architectural directive (verbatim from gandalf transmission 2026-06-02)

QDX-7 drax MVP delivered kit_space consumer integration but with multiple UX + content surface issues. This comprehensive cycle bundles **5 issues across 3 seams** (gandalf + star-lord/rocket + drax) with proper phasing to avoid same-seam collision.

**End state at chain close:**
- All 37 QDX-5 kits have LLM-renamed `emergent_kit_concept` (no Q18 flavor element words; no generic archetype labels)
- `data/kit_space/faction_assignments.json` exported with all 37 kit_ids mapped to 3 factions
- `/loadout` repointed to consume QDX-5 kit_space; `/kit-space` removed/redirected
- Visual hierarchy: primary canonical element FLAG prominent; flavor word secondary annotation
- Featured Characters section at top of `/loadout` with top-5 + top-1 emphasis
- Faction badge + filter UI operational
- Season pages deprecated from active navigation
- Vercel preview deployed and signaled to Matt

---

## 1. Pre-commitment package (Locks A-T preserved)

Locks A-T from IA + EAA + QDX chains remain ACTIVE. Key locks for this cycle:

- **LOCK Q** ADDITIVE-ONLY integration discipline (Issue 5A faction_assignments.json emit; star-lord+rocket cross-seam)
- **LOCK L** iteration discipline (Issue 4 LLM rename quality; 2+ Gate-2 BLOCKs → Matt escalation)
- **LOCK O** drax MVP-discipline — **AMENDED 2026-06-02 (canonical amendment):** "Repoint EXISTING pages; do not create parallel pages. Primary canonical element styling = flag prominence; flavor word styling = secondary annotation. Reuse existing card/badge/filter component patterns; do not create new component shells. Emergent kit identity names DO NOT use Q18 flavor element words OR generic archetype labels."
- **LOCK G** Vercel auto-deploy on drax push
- **LOCK H** standard gandalf design-quality audit at workstream close (note-only)
- **LOCK T** drax + engine page MVP refresh per LOCK O pattern

### Escape clause

KR escalates to Matt for:
1. Issue 4 LLM rename produces 2+ Gate-2 BLOCK-class output (template-repeat post-rename / generic archetype labels remaining / Q18 word leakage)
2. Issue 5A schema design surfaces semantic amendments to existing engine modules (LOCK Q escape)
3. Drax Phase 2 surfaces fundamental incompatibility with existing component patterns (LOCK O escape; gandalf transmission says reuse where possible)
4. Cost overrun: Issue 4 actual cost >2× projection ($0.60+ vs ~$0.30 target)
5. Strategic direction questions outside cycle-18 scope

---

## 2. Workstream decomposition (5 issues; 4 phases)

### Phase 1 — Engine + content prep (parallel fire)

#### Issue 4 — LLM renaming pass on all 37 kits (gandalf-as-subagent)

| Property | Value |
|---|---|
| **Owner** | gandalf-as-subagent (via KR routing) |
| **Status** | 🟢 FIRING (Phase 1) |
| **Dispatch** | `dispatches/2026-06-02-cycle-18-issue-4-llm-rename-all-37-kits.md` |
| **Scope** | Replace `emergent_kit_concept` field in all 37 kit JSONs (event `kse_20260602_008`); LLM prompt embedded with Q18 avoid-list + generic-archetype avoid-list + etymological-family avoidance (umbra/umbral/penumbra) + invented-unique-archetype-per-kit rule |
| **Cost projection** | ~$0.30 (37 × ~$0.008 per Wave B-style rename) |
| **Auto-commit** | per established cycle-push pattern |
| **Estimated** | ~0.5-1 session |

#### Issue 5A — faction_assignments.json export (star-lord + rocket)

| Property | Value |
|---|---|
| **Owner** | star-lord + rocket per LOCK Q |
| **Status** | 🟢 FIRING (Phase 1) |
| **Dispatch** | `dispatches/2026-06-02-cycle-18-issue-5a-faction-assignments-emit.md` |
| **Scope** | Export Phase 5a clustering data for event `kse_20260602_008` to `data/kit_space/faction_assignments.json`; schema per gandalf transmission (event_id + factions array with faction_id/faction_name/kit_ids); cross-seam MIGRATION.md per ADR-004 |
| **LOCK Q ADDITIVE-ONLY** | new file emitted; no semantic changes to existing engine modules |
| **Estimated** | ~1 session |

#### Gate-1 critique-pair (jack-ryan)

| Property | Value |
|---|---|
| **Owner** | jack-ryan DESIGN-MODE |
| **Status** | 🟢 FIRING (Phase 1; parallel review of all cycle-18 dispatches) |
| **Output** | `qa/findings/2026-06-02-cycle-18-drax-amend-full-gate-1.md` |

### Phase 2 — Drax full UX work (sequential after Phase 1 PASS)

#### Issues 1 + 2 + 3 + 5B — Drax consolidated dispatch

| Property | Value |
|---|---|
| **Owner** | drax per LOCK O (AMENDED) + LOCK T |
| **Status** | ❌ NOT STARTED (gates on Phase 1 PASS) |
| **Dispatch** | `dispatches/2026-06-02-cycle-18-issues-1-2-3-5b-drax-consolidated.md` |
| **Issue 1 scope** | Repoint `/loadout` to consume `public/kit-space/` (renamed kit JSONs from Issue 4); merge KitSpace.tsx features; delete KitSpace.tsx + remove `/kit-space` route; deprecate season-data Loadout view |
| **Issue 2 scope** | Visual hierarchy fix — primary canonical element FLAG prominent (kit + skill level via SUBSTRATE_COLORS); flavor word secondary muted annotation |
| **Issue 3 scope** | Featured Characters section at top of `/loadout` rendering top-5 + top-1 per gandalf curation artifact `2026-06-02-qdx-5-top-5-character-curation.md`; kit_id stable reference; consume current emergent_kit_concept (post-rename) |
| **Issue 5B scope** | Consume `faction_assignments.json` from Issue 5A; render faction badge per kit card; faction filter UI operational |
| **Gates** | jack-ryan Gate-2 acceptance verification |
| **Estimated** | ~2-3 sessions |

### Phase 3 — Acceptance verification (sequential)

#### jack-ryan Gate-2 acceptance verification

| Property | Value |
|---|---|
| **Owner** | jack-ryan DEV-MODE |
| **Status** | ❌ NOT STARTED (gates on Phase 2 PASS) |
| **Scope** | 10-criteria acceptance verification per gandalf transmission § ACCEPTANCE CRITERIA |
| **Estimated** | ~0.5-1 session |

### Phase 4 — Close-out

#### KR fix-forward record + Matt signal

| Property | Value |
|---|---|
| **Owner** | KR |
| **Status** | ❌ NOT STARTED (gates on Phase 3 PASS) |
| **Scope** | Fix-forward record + Vercel preview URL + Matt strategic signal |
| **Estimated** | ~0.5 session |

---

## 3. Sequencing

```
Phase 1 (parallel fire):
  Issue 4 (gandalf-as-subagent LLM rename) — FIRING
  Issue 5A (star-lord+rocket faction_assignments emit) — FIRING
  jack-ryan Gate-1 critique-pair on dispatches — FIRING
        ↓
Phase 2 (sequential after Phase 1 PASS):
  Drax consolidated (Issues 1+2+3+5B)
        ↓
Phase 3 (sequential after Phase 2 PASS):
  jack-ryan Gate-2 acceptance verification (10-criteria)
        ↓
Phase 4 (close-out):
  KR fix-forward record + Vercel preview URL + Matt signal
```

---

## 4. Cost + horizon summary

| Phase | Wall-clock | LLM cost |
|---|---|---|
| Phase 1 (Issue 4 + 5A + Gate-1 parallel) | ~1-2 sessions | ~$0.30 (Issue 4 rename) |
| Phase 2 (drax consolidated) | ~2-3 sessions | minimal |
| Phase 3 (jack-ryan Gate-2) | ~0.5-1 session | minimal |
| Phase 4 (KR close-out) | ~0.5 session | minimal |
| **TOTAL** | **~4-6 sessions** | **~$0.30 LLM** |

---

## 5. Acceptance criteria (jack-ryan Gate-2 verification target)

### Content criteria
1. `emergent_kit_concept` on all 37 kits does NOT contain any Q18 flavor element word (verify against full Q18 allow-list per gandalf transmission prompt)
2. `emergent_kit_concept` on all 37 kits does NOT contain umbra/umbral/penumbra (etymological family of removed PG-3 entries)
3. `emergent_kit_concept` on all 37 kits does NOT contain generic archetype words (Caster, Cleric, Mage, Warrior, Knight, Bearer, Fighter, Warden, Champion, Master, Adept)
4. `faction_assignments.json` present at `data/kit_space/`; all 37 QDX-5 kit_ids accounted for; `faction_name` populated per cluster

### UX criteria
5. `/loadout` renders QDX-5 kit_space output by default; `/kit-space` route removed (or 301-redirect to `/loadout`)
6. Per-skill: primary canonical element visually dominant; flavor word visually subordinate
7. "Featured Characters" section renders top-5 picks at top of `/loadout` with renamed identities; top-1 has visual emphasis
8. Faction badge renders per kit card; faction filter operational
9. Old season pages removed from active navigation
10. Vercel preview deploys successfully

---

## 6. Cross-references

### Composes with (preserved canon)
- `canonical/story/2026-06-02-qdx-chain-wave-close-record.md` (QDX chain CLOSED; cycle-18 amends QDX-7 output)
- `canonical/00-ground-state.md` § 1 (canonical "current" kit_space = event `kse_20260602_008`)
- `agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md` (Issue 3 authoritative artifact)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary; consumed inverted by Issue 4 prompt as avoid-list)
- `agentic_orchestration/CHANGELOG.md` (3 ratified disciplines #56/#57/#59)

### LOCK O canonical amendment 2026-06-02
"Repoint EXISTING pages; do not create parallel pages. Primary canonical element styling = flag prominence; flavor word styling = secondary annotation. Reuse existing card/badge/filter component patterns; do not create new component shells. Emergent kit identity names DO NOT use Q18 flavor element words OR generic archetype labels."

---

## 7. Status log

| Date | Event |
|---|---|
| 2026-06-02 | Wave-state authored by KR (this file) |
| 2026-06-02 | Wave-open dispatch authored |
| 2026-06-02 | Issue 4 + Issue 5A + drax consolidated dispatches authored |
| 2026-06-02 | jack-ryan Gate-1 routed on cycle-18 dispatches |
| 2026-06-02 | Phase 1 fired in parallel (gandalf Issue 4 + star-lord Issue 5A) |

---

**Authority composition:**
- Matt 2026-06-02 verbatim "yes, let's do it all" → gandalf comprehensive transmission with phasing
- KR orchestration (this file + dispatches + Gate-1 routing + phase sequencing)
- Critique-pair coverage (jack-ryan Gate-1 + Gate-2 + LOCK L iteration)
- Specialist execution (gandalf Issue 4 + star-lord/rocket Issue 5A + drax Issues 1+2+3+5B)
- LOCK O canonical amendment captures the QDX-7 fix-forward learnings

**End of cycle-18 wave-state file (current).**
