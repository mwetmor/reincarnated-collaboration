# Dispatch — 2026-06-01 — elrond — WS1A.Q18 sub-phase 5f pool.json migration (POST-WAVE)

**From:** knight-rider (post-wave orchestrator)
**To:** elrond (data steward seam — schema + ingest) + star-lord (downstream consumer touches if any) + jack-ryan Gate-1 pre-fire review
**Approved by:** Matt 2026-06-01 verbatim post-wave-close directive (transmitted via gandalf Pattern B close); WS1A.Q18 wave-close sub-phase 5f explicit deferral; KR discretion to fire
**Workstream tag:** `WS1A.Q18-sub-phase-5f-pool-migration`
**Phase / phase-gate:** Sub-phase 5f (POST-WAVE; sibling-of-wave-close operational migration)
**Estimated effort:** 1 wave (~3-5 sessions): schema extension + 118-entry migration + lineage tag application + cross-seam MIGRATION.md
**Acceptance:** pool.json migrated per PG-3 ratification + jack-ryan Gate-2 PASS on schema-extension + ADR-004 MIGRATION.md committed

---

## 1. Context

WS1A.Q18 wave closed 2026-06-01 at PG-4 PASS-with-INFO. Architecture A locked: 7-primary rotating flavor pools + physical-as-taxonomy-sibling; 118 entries committed across 8 primaries. The pool.json schema migration was explicitly deferred to sub-phase 5f POST-WAVE per PG-3 § 4 + wave-close record § 5.

This dispatch operationalizes the deferred migration. Sub-phase 5f is the cross-seam contract change moment per ADR-004 MIGRATION discipline.

**Authoritative readings:**
- **PG-3 ratification (THE LOCK; binding for schema + entries + lineage tags):** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`
- **Canonical lock doc:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Wave-close record (deferral spec § 5):** `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md`
- **Jack-ryan Gate-2 finding (INFO-1 on lineage-tag reconciliation):** `agentic_orchestration/qa/findings/2026-06-01-q18-flavor-pool-lock-gate-2.md`
- **Existing pool.json (the migration target):** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (156 entries; current 4-primary asymmetric coverage 22/20/11/7 for earth/fire/water/wind + 0 for lightning/holy/shadow + absent for physical)
- **Canonical-7+1 catalog:** `~/Games/reincarnated-engine/config/elements.yaml`
- **ADR-004 cross-seam MIGRATION discipline:** `agentic_orchestration/GOVERNANCE.md` § ADR-004
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (esp. #41 substrate-led + #49 substrate-silence ≠ substrate-validation)

---

## 2. Scope (per PG-3 § 4 + § 5)

### 2.1 Schema extension (3 new fields per PG-3 § 4)

Add to pool.json entry schema:

- **`substrate_validation_lineage`** (string enum) — anchor for the 5 lineage categories below
- **`vocabulary_commonness`** (numeric or enum sub-property; per matt-demote-2026-05-12 directive)
- **`slot_unambiguous`** (boolean; per smoke-as-fire vs smoke-as-wind precedent)

Decision authority on enum values + numeric vs enum for `vocabulary_commonness` + default values for missing/legacy entries is YOURS per elrond schema-design seam authority.

### 2.2 Entry migration (109 rotating-primary entries + 9 physical entries)

**Rotating primaries (109 entries):** apply Architecture A 7-rotating lock; entries per `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 3:

| Primary | Final entries (count) | Source |
|---|---|---|
| fire | 16 | canonical lock § 3.1 |
| water | 14 | canonical lock § 3.2 |
| earth | 18 | canonical lock § 3.3 |
| wind | 13 | canonical lock § 3.4 |
| lightning | 13 | canonical lock § 3.5 |
| holy | 14 | canonical lock § 3.6 |
| shadow | 12 | canonical lock § 3.7 |

**Per-entry lineage tag application** — IMPORTANT: per jack-ryan Gate-2 INFO-1, **PG-3 § 5 is authoritative** for per-tag count aggregates (65 substrate-validated / 24 substrate-silent / 19 designer-curation-modern-scientific / 1 designer-curation-mystical-fantasy / 9 architecture-A-taxonomy-registry = 118 total). The canonical doc § 7.1 per-primary breakdown distribution is illustrative-only; the binding source for per-entry tag application is PG-3 § 5 aggregate.

If you observe ambiguity in which specific entries map to which lineage tag (e.g., is `dawn` substrate-validated or substrate-silent?), surface to KR via report-back — do NOT silently resolve.

### 2.3 Physical taxonomy registry (9 entries; separate surface)

**Architecture A: physical is NOT in pool.json flavor pool.** Migrate 9 physical entries to a separate taxonomy registry surface.

**Decision authority on registry location is yours (elrond seam):** options include:
- Separate file `~/Games/reincarnated-engine/data/seasonal_elements/physical_taxonomy.json`
- Section within `config/elements.yaml` under physical
- Engine-side schema field (rocket coordination required)

Per the canonical lock, the 9 entries are:
- Damage sub-type field (weapon + skill schema): `piercing`, `slashing`, `bludgeoning`, `force`
- Mechanical action vocabulary (skill schema): `pierce`, `slash`, `sever`, `strike`
- Ailment (already locked in `config/elements.yaml`): `bleed`

**Physical kits OPT OUT of WS1A.4 LLM judgment;** skill naming via mechanical-schema templates. The registry exists for engine-consumer reference, NOT for LLM-prompt-context insertion.

### 2.4 Cross-seam MIGRATION.md (per ADR-004)

Author `MIGRATION.md` at appropriate scope (engine repo seam boundary):
- Before/after schema diff
- Impact analysis: who reads pool.json downstream? (WS1A.3 + WS1A.4 implementations; engine generation; possibly star-lord telemetry export)
- Backward-compat guidance: do legacy reads still work? Are missing-field defaults defined?
- Migration order: schema-extend first (additive) → entry-migrate → consumer-side optional adoption of new fields

### 2.5 Cull-tag dispositions per PG-3 § 3

Apply the following to existing pool.json entries:

- **`drift-14-wind-storm-cluster-collapse`:** DISSOLVE (cyclone / whirlwind / squall / hurricane promoted to wind allow-list)
- **`drift-14-plant-anatomical`:** DISSOLVE-for-thorn (thorn substrate-confirmed; promoted to earth allow-list)
- **`drift-14-biological-organic`:** KEEP (substrate-silent)
- **`drift-14-alternative-liquid`:** KEEP
- **`drift-14-auditory-non-visual`:** KEEP
- **`drift-14-conceptual-not-substance`:** KEEP

### 2.6 Concrete slot routing (per PG-3 § 2.3 + canonical doc § 4)

Apply slot routing for previously-ambiguous candidates:
- `mist` → WATER
- `vortex` → WIND
- `hurricane` / `squall` / `stormtide` / `tempest` → WIND
- `njord` → WATER

---

## 3. Decision authority

Per hive-mind decision-routing (Matt 2026-05-23): schema design + ingest pipeline + entry migration mechanics + lineage-tag-resolution decisions are YOURS per elrond seam authority. Matt is LAST-resort escalation for:
- Cross-seam contract-change scope amendment (e.g., adding a 4th schema field beyond the 3 ratified at PG-3)
- Push to remote (default per ADR-006)
- Physical registry location if cross-seam touches rocket/star-lord/drax (escalate to Matt if cross-repo coordination beyond elrond seam needed)

Star-lord coordination: if you need star-lord to update downstream consumer touches (e.g., telemetry export packets that read pool.json fields), surface via report-back; KR routes secondary dispatch.

---

## 4. Acceptance criteria

- [ ] Schema extended with 3 new fields per PG-3 § 4
- [ ] 109 rotating-primary entries migrated per canonical lock § 3 + cull-tag dispositions § 2.5 + slot routing § 2.6
- [ ] 9 physical entries migrated to taxonomy registry (location decided by elrond)
- [ ] Per-entry lineage tags applied per PG-3 § 5 aggregate (65/24/19/1/9)
- [ ] Cross-seam MIGRATION.md authored
- [ ] Backward-compat verified (legacy pool.json readers still work OR explicit migration path documented)
- [ ] Schema-extension validation: parse pool.json successfully; field types respected; enum values valid
- [ ] jack-ryan Gate-2 review PASS on schema-extension + entry migration + MIGRATION.md (BLOCK authority)
- [ ] Auto-commit per CLAUDE.md addendum 2026-05-25

---

## 5. Cross-seam contract change check (Principle 6 — IS APPLICABLE)

**Answer:** YES — this dispatch IS a cross-seam contract change per ADR-004 (the wave-close 5f deferral was explicitly named cross-seam).

**Affected seams:**
- **elrond:** owns schema design + ingest (primary scope)
- **star-lord:** if telemetry/export reads pool.json fields, update accordingly (secondary scope; surface in MIGRATION.md)
- **rocket:** if engine generation reads pool.json fields, verify backward-compat or coordinate amendment (secondary scope; surface in MIGRATION.md)
- **drax:** loadout app may consume pool.json indirectly via engine outputs (tertiary; surface in MIGRATION.md if relevant)

**Round-trip:** required per ADR-004 if star-lord/rocket touch is non-trivial. Author MIGRATION.md + obtain seam-owner ACK before tagging the migration.

---

## 6. Out of scope

- WS2 modern-caster substrate-coverage audit (separate dispatch)
- WS3 sub-element mapping (separate workstream; Matt-authorization pending)
- WS4 engine gen refresh (separate workstream; Matt-authorization + Q16/Q17/Q19 prerequisites pending)
- Q16 / Q17 / Q19 hard-blocker wave openings (Matt-authorization pending)

---

## 7. References

- **PG-3 ratification:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`
- **Canonical lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Wave-close record:** `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md`
- **Gate-2 finding (INFO-1 on lineage tag reconciliation):** `agentic_orchestration/qa/findings/2026-06-01-q18-flavor-pool-lock-gate-2.md`
- **Workstream queue:** `agentic_orchestration/post-q18-workstream-queue-2026-06-01.md`
- **Elrond OP:** `agentic_orchestration/operating-procedures/elrond.md`
- **ADR-004 cross-seam MIGRATION discipline:** `agentic_orchestration/GOVERNANCE.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Schema extension committed:** path + commit
**Pool.json migration committed:** path + commit
**Physical taxonomy registry location:** path + commit
**MIGRATION.md location + path:** path + commit
**Backward-compat verified:** yes/no
**Lineage-tag resolution surface (per-entry tag mapping):** clean / surfaced N ambiguities
**Cross-seam touches surfaced for follow-on:** none / star-lord / rocket / drax
**Routing back to KR:** "proceed to jack-ryan Gate-2 (schema + migration review)" / surface issue
```

After completion record append, KR routes Gate-2 jack-ryan review.

---

**End of WS1 sub-phase 5f pool migration dispatch.**
