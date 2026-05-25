# Dispatch — 2026-05-25 — Cycle 10 Sidecar B — Off-Hand Substrate Inclusion

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Sidecar:** B (off-hand items substrate inclusion)
**Lead owner:** elrond (substrate seam; schema extension + existing-source mining)
**Co-owner:** legolas Mode B (targeted crawl for off-hand gaps; parallel-instance OK per legolas OP)
**Curation:** gandalf (30-row cross-category curation review at end)
**From:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 multi-stage dispatch parent (gandalf request 2026-05-23) § 3 Sidecar B + composition policy v1 § 8 + Matt 2026-05-24 Stage 0 design dialogue (Custer-with-Art-of-War scenario surfacing scope gap)
**Status:** FIRE — parallel to main sequence; legolas Mode B crawl fires immediately; elrond mining sequences after Wave 5 Phase 0a/2 to avoid elrond-on-elrond git race per Cycle 9.15 lesson

---

## 0. TL;DR

Extend Cycle 10 substrate-curation scope to include off-hand items (shields + tomes + banners + focuses + horns + talismans) so v1 pipeline supports shield-and-sword tanks + caster-with-focus + dual-wield + signature off-hand-item forms. Cost-once principle — easier to include in active Cycle 10 than retrofit later.

**Pipeline (Path A LOCKED per Matt 2026-05-25):**
- legolas Mode B targeted crawl for OFF-HAND ITEMS ONLY (NOT for main weapon library); ~1 day; background-process per Discipline #19
- elrond existing-source mining from royal_armouries + Met Museum + Wikipedia + Wikidata; ~half-day; sequences after Wave 5 Phase 0a/2
- Approach B single-table schema extension (extend `weapon_knowledge_entries.weapon_kind` enum)
- gandalf 30-row cross-category curation review at end

**Estimated additions:** ~1,400-5,500 raw rows; ~600-1,400 entering v1_scope after Stage 3 re-sample pass

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth)
2. **`canonical/story/off-hand-items-2026-05-24.md`** (off-hand items canonical — Main/Secondary architecture; 6 categories operational definition; Approach B schema; per-cell off-hand usage table)
3. **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 8** (Sidecar B execution scope consolidated)
4. **`agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § 3 Sidecar B** (Sidecar B scope-of-record)
5. `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B — substrate-genre-flagging applies to off-hand items too)
6. `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md` (cycle scope-of-autonomy; Sidecar B in-scope per § 1-3)
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #18 if methodology hotspot surfaces at Stage 4 off-hand axes, #19 + #19.1, #20 robots.txt for crawl, #25 semantic-layer rep-audit)

---

## 2. Inputs

- `weapon_knowledge_entries` — 89,841 active rows (substrate DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`)
- Existing rich sources known to contain off-hand items: royal_armouries (shields heavy), Met Museum (ceremonial off-hand), Wikipedia (broad), Wikidata (broad)
- Per-source schema mapping from prior elrond Phase D + Stage 1.5 work
- Off-hand category enumerations per off-hand-items canonical doc (6 categories: shield, tome, banner, focus, horn, talisman, plus dual-wield-off-hand as 7th composition state)
- For legolas Mode B crawl: per-category gap-source candidate list (gandalf supplies via § 5 below)

---

## 3. Outputs

### 3.1 Schema extension (elrond owns; fires at elrond mining sequence)

```sql
ALTER TABLE weapon_knowledge_entries
DROP CONSTRAINT IF EXISTS check_weapon_kind;

ALTER TABLE weapon_knowledge_entries
ADD CONSTRAINT check_weapon_kind CHECK (
  weapon_kind IN (
    'category', 'unique', 'named_template', 'ammo_or_consumable',
    'shield', 'tome', 'banner', 'focus', 'horn', 'talisman',
    'unknown'
  )
);
```

MIGRATION.md required per ADR-004 because the enum constraint changes. Drafted at deliverable path. Grep-verify zero cross-seam consumers of `weapon_kind` enum (Phase D precedent expects ZERO; document and proceed).

### 3.2 elrond existing-source mining output

- New rows in `weapon_knowledge_entries` from royal_armouries + Met Museum + Wikipedia + Wikidata where they contain off-hand items not yet imported
- Reclassification of EXISTING rows where current `weapon_kind` is misclassified for off-hand items (e.g., shield currently tagged 'category' should be 'shield')
- Per-row Stage 1 + Stage 1.5 columns populated at insert/reclassify time for substrate consistency
- Output artifact: `agentic_orchestration/elrond/research/cycle-10-sidecar-b-2026-05-25/existing-source-mining.md` + companion JSON

### 3.3 legolas Mode B crawl output

- Targeted Mode B catalogue crawl for off-hand items where existing sources thin:
  - **Tomes / books** (tactical/magical/sacred): tactical-treatise lists (Art of War, Book of Five Rings, On War, Strategikon, etc.); D&D + Pathfinder + WoW Classic + Soulslike spellbook lists
  - **Banners / standards**: military museums + heraldry sources + named historical standards (Bratach Sídhe, Raven Banner, Sun-and-Wave Banner, Wessex Wyvern, etc.)
  - **Focuses / orbs / talismans**: ritual-implement catalogues, named-mythological-focus items (Eye of Vecna, Hand of Vecna, ankh, mojo bag, witch's stone, etc.)
  - **Horns / signaling-implements**: military + ceremonial substrate (Gjallarhorn, Oliphant, Olifant, war-horns, signal-horns)
- Per-category target volume: ~50-300 entries per category (driven by source availability; do NOT inflate via crawl-pad)
- Discipline #20 robots.txt compliance; Discipline #19 background-process pattern; resource bounds documented
- Output artifact: `agentic_orchestration/legolas/research/cycle-10-sidecar-b-off-hand-crawl-2026-05-25/` directory with per-category subdirs + manifest + raw + cleaned + per-category README

### 3.4 v1_scope re-sample post-Sidecar B

After Sidecar B substrate lands, Wave 5 Stage 3 sampling executes a RE-SAMPLE pass to include off-hand rows in v1_scope per composition policy. This re-sample is part of Wave 5 Phase 2 retry — knight-rider re-invokes elrond Phase 2 after Sidecar B completes. NOT in scope of this dispatch.

### 3.5 gandalf 30-row cross-category curation review

- After mining + crawl complete, gandalf reviews 30 representative rows spanning all 6 categories (5 per category)
- Pass threshold: ≥ 24/30 sensible per-category classification + cultural-tradition + period
- Output: `agentic_orchestration/gandalf/notes/2026-05-25-sidecar-b-curation-review.md`

---

## 4. Method notes

### 4.1 Existing-source mining first (elrond seam)

Per gandalf request § 3 Sidecar B: ~50-70% of needed off-hand-item substrate likely exists in royal_armouries + Met Museum + Wikipedia + Wikidata. Reclassify via `weapon_kind` enum extension first; this is cheap and covers majority of need.

Query pattern per source:
- royal_armouries: filter `description_text` for shield/buckler/heater/kite/round/etc.
- Met Museum: filter on object-type (existing structured field) for relevant categories
- Wikipedia: name-token regex against canonical_name (shield, tome, banner, focus, talisman, horn + synonyms)
- Wikidata: SPARQL-equivalent filter on entity-class hierarchy where present

### 4.2 Targeted Mode B crawl (legolas seam)

Per Sidecar B § 3 + composition policy § 8.1: legolas Mode B fires for gap-categories where existing-source mining underperforms.

**CRITICAL Path A LOCK per Matt 2026-05-25:** This Mode B crawl is for OFF-HAND ITEMS ONLY. Do NOT crawl for main weapon library substrate. Main weapon library is Path A engine-authored gap-fill scope (Wave 6 territory). Broad weapon-library crawl is preserved for v1.1+ per Stage 3.6 research-replacement notes.

### 4.3 Per-category substrate-coverage estimate (from gandalf request § 3 Sidecar B)

| Category | Estimated rows | Source |
|---|---|---|
| Shields | 500-2,000 | Royal Armouries + Met Museum + Wikipedia |
| Tomes / books (tactical/magical/sacred) | 500-1,500 | Wikipedia + Wikidata + targeted crawl |
| Banners / standards | 100-500 | Military museums + heraldry sources |
| Focuses / orbs / talismans | 200-1,000 | Ritual-object substrate + targeted crawl |
| Horns / signaling-implements | 100-500 | Military + ceremonial substrate |
| **TOTAL** | **~1,400-5,500** | Mixed sources |

### 4.4 Cohesion-coalescence implication (NOT in scope this dispatch; for awareness)

Per gandalf request § 3 Sidecar B + skill-system § 12.3:
- Phase 5 cohesion-coalescence extends to handle TWO-ITEM forms (main weapon + off-hand)
- Discipline already established (3-tier named-bearer + Matt's bi-modal revision); extends to two-item alignment scoring
- Cross-cultural bifurcation accepted as feature when historically/genre-coherent (Custer + Sun Tzu Art of War); rejected as bug when nonsensical
- Skill-system doc § 12.3 will be amended post-Cycle-10 (gandalf canonical authoring queue per ground-state § 5 active workstream)

**This dispatch does NOT touch skill-system canonical doc.** Post-Cycle-10 gandalf work.

### 4.5 Semantic-layer rep-audit (Discipline #25)

Off-hand items have less mode-collapse risk than main weapons (off-hand categories are tighter cultural categories generally). But still apply rep-audit at v1_scope inclusion boundary — does the cluster identity actually contain off-hand items, or has a banner been mis-tagged as "ceremonial weapon" via Mode-C naming allusion? Surface any contamination to knight-rider.

---

## 5. Cross-seam impact

- **Substrate DB schema change** (enum constraint relaxation; additive only; backward-compatible)
- **MIGRATION.md required** per ADR-004 — drafted at deliverable path; grep-verify zero cross-seam consumers expected
- **Round-trip Principle 6:** Round-trip: not applicable — substrate-only schema change; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; no engine code touched
- **No row deletion** — additive only; substrate optionality preserved per Variant C
- **No engine code touched**

---

## 5.5 Acceptance criteria (formal per dispatches/README.md § Acceptance criteria + Principle 6)

### Legolas Mode B crawl
- [ ] Per-category source identified for tomes / banners / focuses / talismans / horns (5 categories) with named source URLs + robots.txt compliance check
- [ ] Per-category target volume documented (50-300 per category); actual yield documented post-crawl
- [ ] Raw + cleaned + manifest artifacts at named research-dir path; Discipline #19 background-process logs
- [ ] Resource-bounds projection up-front (memory + bandwidth + storage); actuals captured post-crawl
- [ ] gandalf cross-category curation review request authored at session-end

### Elrond existing-source mining
- [ ] Schema extension landed via ALTER TABLE; MIGRATION.md drafted; grep-verified zero cross-seam consumers
- [ ] Existing-source mining adds rows OR reclassifies rows for at least 4 of 6 categories
- [ ] Per-row Stage 1 + Stage 1.5 columns populated for new rows
- [ ] Output markdown + JSON artifact at named path with per-category counts + 5-10 row sample per category
- [ ] Pre-mining DB backup at `cycle-10-sidecar-b-2026-05-25/backups/telemetry.db.pre-sidecar-b` (gitignored)
- [ ] **Round-trip: not applicable — substrate-only schema change; no cross-seam contract change per Principle 6 trigger-type table**

### Both
- [ ] gandalf 30-row cross-category curation review PASS ≥ 24/30
- [ ] AGENT_STATE.md updated at session end where seam-maintained
- [ ] Tag: `legolas/cycle-10-sidecar-b-off-hand-crawl-2026-05-25` (legolas commit) + `elrond/cycle-10-sidecar-b-off-hand-mining-2026-05-25` (elrond commit)
- [ ] Auto-commit + auto-push per push-per-wave authorization

---

## 6. Out of scope (explicit)

- **NOT broad crawl for main weapon library** — Path A LOCKED per Matt 2026-05-25; main weapons get engine-authored gap-fill via Wave 6 only; broad crawl deferred to v1.1+ via Stage 3.6 research-replacement notes
- **NOT main-weapon substrate corrections** — Sidecar B is OFF-HAND ITEMS ONLY
- **NOT skill-system canonical doc amendment** — gandalf authors post-Cycle-10 per canonical authoring queue
- **NOT Phase 5 cohesion-judge two-item alignment scoring implementation** — gandalf authors spec post-Cycle-10
- **NOT v1_scope re-sample** — Wave 5 Phase 2 re-sample fires post-Sidecar B completion; not in this dispatch scope
- **NOT engine code changes** — substrate-only
- **NOT Stage 4 mechanical-tagging on off-hand items** — Stage 4 dispatch (Wave 7) handles via legolas Mode A consult prerequisite on off-hand-mechanical-profile patterns

---

## 7. Tag intent

- `legolas/cycle-10-sidecar-b-off-hand-crawl-2026-05-25` after Mode B crawl completion
- `elrond/cycle-10-sidecar-b-off-hand-mining-2026-05-25` after existing-source mining + schema extension + gandalf curation review

Intermediate tag (seam-prefixed) per project convention. NO Matt-approved milestone prefix.

---

## 8. Smoke-test expectation

### Legolas Mode B crawl smoke
- Per Discipline #19.1 cheapest-refuting-test: per-category, smoke-test a single source URL with 5-10-row sample BEFORE firing full crawl; verify the source actually contains off-hand items with the expected schema shape
- If per-category smoke fails → revise source list before full crawl fires
- Per Discipline #1.1 resource-bounds: project memory + bandwidth + storage UP-FRONT; verify against host capacity (8GB RAM ceiling)
- Per Discipline #20 robots.txt: per-source robots.txt check; rate-limit per source

### Elrond existing-source mining smoke
- Per source, pre-mining: SELECT 10 candidate rows from each source matching off-hand-item filter; gandalf 10-row spot-check ≥ 8/10 sensible classification before full mining fires
- Schema extension smoke: ALTER TABLE; ROLLBACK; verify constraint relaxation; re-apply
- Post-mining smoke: per-category SELECT 5 rows; SQL assertion that all new rows have `weapon_kind` IN the extended enum

---

## 9. Discipline checklist

- [x] **#1 + #1.1 math-before-code + resource-bounds:** legolas Mode B per-source bandwidth/memory/storage projection; elrond mining row-volume + DB-write projection
- [x] **#1.2 math-note code-citation:** scripts cite composition policy § 8 + off-hand-items canonical doc § sections
- [x] **#2 + #2.1 smoke + resource-scaling rehearsal:** § 8 above
- [x] **#11 empirical inspection:** rep-audit per § 4.5 at v1_scope inclusion boundary
- [x] **#18 (conditional):** if Stage 4 off-hand mechanical-tagging surfaces a hotspot, legolas Mode A consult fires; NOT pre-fired this dispatch
- [x] **#19 + #19.1 background processes + cheapest-refuting-test:** crawl runs background; per-category smoke is cheapest-refuting-test
- [x] **#20 robots.txt:** legolas Mode B per-source compliance
- [x] **#25 semantic-layer rep-audit:** per § 4.5

---

## 10. Open questions for the agent to resolve

- Per-category source URL final list (legolas owns; gandalf consults if cultural-sensitivity ambiguity surfaces)
- Per-category target volume (50-300 range; legolas decides per source-availability empirical evidence)
- Whether to fire all 5 categories in parallel sub-processes or sequence — legolas decides per resource-bounds + robots.txt rate-limit constraints
- Schema extension exact rollout pattern (ALTER TABLE in single transaction vs phased migration) — elrond decides per Phase D precedent
- gandalf curation review timing — defer until both mining + crawl complete vs per-stream review — knight-rider proposes deferred (single batch ≥ 24/30 pass); elrond + legolas concur or escalate

---

## 11. References

- Sidecar B parent: `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § 3 Sidecar B
- Composition policy v1 § 8: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- Off-hand items canonical: `canonical/story/off-hand-items-2026-05-24.md`
- Cycle 10 scope-doc: `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Wave 5 Stage 3 dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md`

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 scope-doc § 1-3 (in-scope autonomous decisions + executions + commits) + composition policy v1 § 8 + Sidecar B parent dispatch § 3
**Status:** **FIRE** — legolas Mode B crawl fires immediately in parallel with Wave 5 Phase 1 (different scope; non-overlapping work-product); elrond existing-source mining sequences after Wave 5 Phase 2 to avoid elrond-on-elrond git race per Cycle 9.15 parallel-commit-race lesson

**Gate-1 critique-pair posture:** Sidecar B is scope-extension of Cycle 10 substrate-curation. Composition policy v1 § 8 + Sidecar B parent dispatch § 3 + off-hand-items canonical doc together constitute the locked design substrate; Gate-1 not re-fired per scope-doc § 1 in-scope autonomous decisions (dispatch authoring within Cycle-10 scope). If specialist returns surface a design-fit issue, route to gandalf for Pattern A-light verdict at integration time.

**Owners:** elrond (lead — schema + mining) + legolas Mode B (crawl) + gandalf (curation review)
