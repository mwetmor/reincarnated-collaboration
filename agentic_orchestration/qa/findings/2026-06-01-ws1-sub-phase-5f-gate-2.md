# Finding — 2026-06-01 — WS1 Sub-Phase 5f Pool.json Migration — Gate-2

**Reviewer:** jack-ryan
**Severity:** WARN (PASS-with-WARN)
**Target:** engine repo `fcc4887` + meta-repo `d1beb95`
**Developer:** elrond (data steward seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-test / quality criterion), 3 (cross-seam impact), 4 (decisions-log truth), 5 (severity matters), 6 (cross-seam round-trip)
**Authority:** Matt 2026-06-01 post-wave-close directive + WS1 Gate-1 PASS-with-INFO + critique-pair Gate-2 BLOCK authority per ADR-004

---

## Verdict: PASS-with-WARN

**Final classification:** PASS-with-WARN

WS1 wave-closes. Amendment-pass on canonical source docs is REQUIRED before WS1A.3/WS1A.4 fire (see § Ambiguity 1 remediation below). Migration itself is structurally correct; the discrepancy is in the source-doc wording inherited pre-migration.

---

## Migration completeness check: PASS

**Independent cardinality verification (performed independently — not deferred to elrond):**

Summing PG-3 § 1 verbatim per-primary entry lists directly:

| Primary | Entries | Verified count |
|---|---|---:|
| fire | ember/cinder/blaze/scorch/inferno/ignite/fira/lava/magma/charcoal/char/brand/flare/fusion/thermal/combustion | 16 |
| water | tide/torrent/glacial/brine/aqua/frost/chill/mist/ice/glacier/wave/marsh/hydro/hydraulic | 14 |
| earth | stone/granite/marble/clay/sand/iron/gold/silver/lead/gem/crystal/obsidian/amber/quake/tremor/thorn/seismic/tectonic | 18 |
| wind | tempest/cyclone/whirlwind/gale/gust/squall/hurricane/zephyr/hail/sleet/cloud/sonic/shockwave | 13 |
| lightning | arc/static/surge/volt/bolt/shock/spark/thunder/plasma/flash/ion/voltage/tesla | 13 |
| holy | radiance/radiant/dawn/aura/divine/sacred/blessed/lux/celestial/stellar/solar/photon/laser/prismatic | 14 |
| shadow | void/shade/wraith/drain/necrotic/abyss/shadow/lich/blackhole/singularity/darkmatter/soul | 12 |
| **ROTATING TOTAL** | | **100** |
| physical | piercing/slashing/bludgeoning/force + pierce/slash/sever/strike + bleed | 9 |
| **GRAND TOTAL** | | **109** |

**Result: 100 rotating + 9 physical = 109 total.** PG-3 § 1.9 / canonical lock § 0 / canonical lock § 2.9 / decisions-log assert "109 rotating + 9 physical = 118 total" — this is a sub-totaling editorial error. The number 109 appears in source docs as the rotating count, but the actual rotating count per verbatim lists is 100. The physical count (9) is correct. Total is 109, not 118.

Migration honored verbatim entry lists: 100 lock entries in pool.json, all 7 per-primary verbatim counts verified entry-by-entry by querying migrated pool.json. **Migration completeness: PASS.**

**Pool.json verification results:**
- Total pool.json entries: 214 (100 locked allow-list + 114 legacy quarantine). PASS.
- Lock cohort (ws1a_q18_lock_date=2026-06-01) per-primary: fire=16/water=14/earth=18/wind=13/lightning=13/holy=14/shadow=12 = 100. PASS.
- Each per-primary entry-set is an exact verbatim match to PG-3 § 1 lists. PASS.
- Legacy quarantine count: 114. PASS (per dispatch § 4.1 / canonical lock § 9.3 "audited + extended, NOT retired" discipline).
- stormtide: NOT present in pool.json. PASS (no-op disposition correct; see Ambiguity 3).

---

## Schema extension check: PASS

**4 additive fields in PoolElement:**

| Field | Type | Default | Assessment |
|---|---|---|---|
| `substrate_validation_lineage` | `str = ""` | `""` | PASS — 5-value enum documented; safe default for legacy |
| `vocabulary_commonness` | `str = "unscored"` | `"unscored"` | PASS — 4-value enum; safe default |
| `slot_unambiguous` | `bool = True` | `True` | PASS — conservative default (True = unambiguous) |
| `ws1a_q18_lock_date` | `str = ""` | `""` | PASS — date-marker; safe default; not in PG-3 § 4 spec but additive and sound |

PG-3 § 4 specified 3 fields. Elrond added a 4th (`ws1a_q18_lock_date`) under seam authority. This is within elrond seam authority on schema design (dispatch § 2.1 delegates enum values and field-type decisions to elrond seam). The 4th field is purely a date-marker for lock-cohort traceability. Additive; safe default; non-breaking. ACCEPTED.

**Enum value verification (from migrated data):**

- `substrate_validation_lineage`: 57 substrate-validated / 23 substrate-silent / 19 modern-scientific / 1 mystical-fantasy / 114 empty (legacy). Zero invalid values. PASS.
- `vocabulary_commonness`: 32 common / 68 genre-standard in lock cohort (zero "unscored" in lock cohort — all 100 lock entries scored). PASS.
- `slot_unambiguous=False`: 6 entries flagged (frost/mist/water; tempest/squall/hurricane/sleet/wind). These are flex-candidate entries per PG-3 § 2.3 slot-routing decisions. PASS.

**Backward-compat (per MIGRATION.md engine-side § backward-compat verification):**
- Pre-extension PoolElement reads v1.1 pool.json cleanly. PASS.
- Extended PoolElement reads legacy (v1.0) pool.json cleanly. PASS.
- Round-trip parse verified. PASS.

---

## Cross-seam handling check: PASS

**MIGRATION.md authoring:**
- Engine-side: `reincarnated-engine/src/reincarnated/element/MIGRATION.md` — 2026-06-01 entry present at top, authored per ADR-004 convention. PASS.
- Data-layer-side: `agentic_orchestration/research/curated/MIGRATION.md` v1.7 — present; composes with engine-side per ADR-004 round-trip discipline. PASS.

**Before/after diff documented:** schema before/after in engine-side MIGRATION.md § "Schema diff". PASS.

**Backward-compat path documented:** explicit in engine-side MIGRATION.md § "Backward-compat verification" (4 bullet points). PASS.

**Round-trip ACK mechanism:**
- Engine-side MIGRATION.md names all affected seams: rocket (no-action-required), star-lord (no-action-required), drax (no-action-required), gandalf (future query surface). All three "no-action-required" ACKs are documented with rationale. PASS.
- Tagging deferred pending this Gate-2 (step 6 in migration order, per engine-side MIGRATION.md). CORRECT — tag must not fire until Gate-2 clears. PASS.

**Cross-seam touches (elrond claim: no secondary dispatch required):** VERIFIED.
- rocket: pool.json new fields additive; selector.py + naming.py read by `d1_status`, not new fields. No-action-required is substantiated.
- star-lord: telemetry/recorder.py confirmed does not read pool.json beyond named fields. No-action-required is substantiated.
- drax: consumes engine-generated season artifacts, not pool.json directly. No-action-required is substantiated.

---

## 3 Ambiguities Assessment

### Ambiguity 1 — Cardinality discrepancy (LOAD-BEARING)

**Independent verification result:**

16+14+18+13+13+14+12 = **100 rotating**. PG-3 § 1.9 asserts "109 rotating-primary flavor pool entries." The delta is exactly 9. This is NOT a missing-9-entries error — the verbatim per-primary lists were Gate-2-PASS-verified entry-by-entry at PG-4 wave-close (commit `9889bff`). The 9-delta is an editorial sub-totaling error that originated in PG-3 § 1.9 and propagated forward into:

1. Canonical lock § 0 TL;DR — "109 rotating-primary flavor-pool entries"
2. Canonical lock § 2.9 — "109 rotating-primary flavor-pool entries" and table total 118
3. Wave-close record § 0 TL;DR — "118 entries across 8 primaries"
4. Decisions-log 2026-06-01 entry — "109 entries... totaling 109 entries... 118 entries total"

**What caused the error:** The number 9 appears twice in the source data — once as the physical registry count, and once as a phantom addition to the rotating total. The rotating subtotal 100 was mentally treated as 109 (perhaps the physical 9 was added twice in editorial assembly). This is a pure transcription/sub-totaling error; the per-primary verbatim lists themselves are correct throughout.

**Third-interpretation test:** Is there any reading where "109 rotating" is correct? No. The verbatim per-primary lists in PG-3 §§ 1.1–1.7 and canonical lock §§ 2.1–2.7 are identical and unambiguous. No hidden entries exist. The 9-delta has no alternative interpretation. This is an editorial error, not a design ambiguity.

**Severity on migration itself:** INFO. Elrond migrated against the verified ground truth (verbatim per-primary lists). The migration is correct. The wording in source docs is wrong.

**Amendment-pass scope (REQUIRED before WS1A.3/WS1A.4 fire):**

| Document | Wording to correct | From | To |
|---|---|---|---|
| PG-3 § 1.9 | Total assertion | "118 entries locked... 109 rotating-primary flavor pool + 9 physical" | "109 entries locked... 100 rotating-primary flavor pool + 9 physical" |
| Canonical lock § 0 TL;DR | Total assertion | "118 entries" / "109 rotating-primary" | "109 entries" / "100 rotating-primary" |
| Canonical lock § 2.9 | Total assertion + table | "118 entries... 109 rotating" | "109 entries... 100 rotating" |
| Canonical lock § 7 header | Count assertion | "118" | "109" |
| Wave-close record § 0 TL;DR | "118 entries across 8 primaries" | "118 entries" | "109 entries" |
| Decisions-log 2026-06-01 | "109 entries... 118 entries total" | both assertions | "100 rotating... 109 total" |

**Recommended path: Option A — canonical-doc amendment-pass (gandalf authors; jack-ryan approves as within-seam documentation change).**

Option B (Matt clarification) is not required — the verbatim per-primary lists are unambiguous and Matt-ratified. The error is editorial. Option C (dual annotation) is inappropriate — preserving a false total as "historical context" alongside the correct total would introduce permanent confusion for downstream consumers (WS1A.3 / WS1A.4 / Q16/Q17/Q19).

**Classification:** WARN. Migration ships. Amendment-pass fires before WS1A.3/WS1A.4. KR routes to gandalf.

### Ambiguity 2 — Lineage tag aggregate reconciliation

**Elrond's resolution path: RATIFIED.**

The arithmetic is unambiguous:

- PG-3 § 5 binding aggregate (65+24+19+1 rotating = 109) overshoots actual rotating total (100) by exactly 9 — same delta as Ambiguity 1. The PG-3 § 5 rotating aggregate is internally inconsistent with the per-primary verbatim lists for the same reason.
- Canonical § 7.1 illustrative col-sum (57+19+23+1 = 100 rotating) DOES reconcile to actual rotating total. However, § 7.1 col shows substrate-silent=19 and modern-scientific=23.
- Canonical § 7 explicit modern-scientific enumeration lists 19 entries verbatim — matching PG-3 § 5's 19, NOT § 7.1 col's 23.
- Elrond's resolution: apply lineage tags per § 7.1 col-sum (which reconciles to 100) BUT honor canonical § 7 explicit modern-sci list (19 entries, not 23) — meaning substrate-silent absorbs the residual: 57 validated + **23** silent + 19 modern-sci + 1 mystical = 100. This is the only internally consistent reading.

**Verification from migrated pool.json:** substrate-validated=57 / substrate-silent=23 / modern-scientific=19 / mystical-fantasy=1 = 100 rotating. This reconciles perfectly. PASS.

**Elrond seam decision is sound:** it applies the canonical § 7 explicit modern-scientific enumeration (ground truth for that tag) and lets substrate-silent be the residual (the "absorbing" category, which is correct per Discipline #49 — substrate-silent entries are D1-pool carry-forwards with no explicit research outcome, so their count is mechanically residual after subtracting confirmed overlay categories). Full rationale traceable in migration script.

**Recommendation:** No BLOCK. The § 7.1 table discrepancy (silent=19 vs actual-applied=23; modern-sci=23 vs actual-applied=19) is a side-effect of the same +9 editorial error in Ambiguity 1. When gandalf authors the Ambiguity 1 amendment-pass, § 7.1 lineage distribution table should also be corrected to show the applied distribution (57/23/19/1) and labeled as authoritative (not "aggregated for readability"). The PG-3 § 5 aggregate should also be corrected to the applied distribution (57/23/19/1/9=109).

**Classification:** INFO within the overall WARN. Elrond resolution is ratified. Amendment-pass on § 7.1 wording is bundled with Ambiguity 1 correction.

### Ambiguity 3 — stormtide INFO-1

**Elrond's no-op disposition: CORRECT.**

stormtide appears in canonical lock § 3.3 and PG-3 § 2.3 slot-routing decisions ("stormtide → WIND, water flex"). It does NOT exist in PG-3 §§ 1.1–1.7 verbatim entry lists. It does NOT exist in v1.0 pool.json. It does NOT exist in v1.1 pool.json post-migration.

The slot-routing decision in PG-3 § 2.3 was authored for completeness (it preserves a routing intent in case stormtide is added to a future allow-list or enters pool.json as a novel word proposal). It is not a commitment to include stormtide in the Architecture A lock.

**Appropriate disposition:** no-op. The slot-routing decision is preserved in the migration script's SLOT_ROUTING map for future reference. No pool entry exists to route. No action required.

**Should stormtide be added to the wind allow-list?** Not at this Gate-2. That would require a PG-3-level design decision (Matt authority per ADR-002 Tier A). The canonical lock is currently closed. If stormtide is desired in a future v1.1+ lock extension, that is a separate design surface — likely WS1A.3 or a Q18 lock v1.1+ amendment.

**Should the slot-routing reference be removed from PG-3 § 2.3 and canonical lock § 3.3?** Recommend: NO. The routing intent is not harmful and may be useful if stormtide is subsequently submitted as a novel word proposal. Retain in canonical docs as a forward routing note, not as a lock commitment. Add a brief annotation "stormtide: not in v1.0 lock; routing preserved for future reference" at the amendment-pass pass.

**Classification:** INFO. No action blocking WS1 wave-close.

---

## Drift-14 invariant validator disposition

**Finding:** Elrond correctly surfaces that new lock entries (inferno, ignite, fira, fusion, thermal, combustion, and others) will auto-demote from allow-list → eligible at load until `vfx_coverage_manifest.json` is extended. This is EXPECTED behavior per the existing Drift-14 pool-load invariant gate (MIGRATION.md 2026-05-17 entry).

**Assessment:** OUT-OF-WS1-SCOPE. The migration itself is structurally correct. The auto-demote is a downstream load-time behavior that reflects a genuine gap (VFX manifest does not yet cover the new lock entries). Extending vfx_coverage_manifest.json is the correct fix; it is a separate surface.

**Forward note for WS1A.3 implementation:** Before WS1A.3 fires, vfx_coverage_manifest.json must be extended to cover the new lock cohort entries; otherwise sub-element selection will draw from "eligible" pool (effective allow-list minus VFX-coverage gate) rather than "allow-list." This is a WS1A.3 prerequisite, not a WS1 blocking issue.

**Does Drift-14 auto-demote affect WS1 wave-close?** NO. The migration is structurally correct. The auto-demote is a pre-existing invariant that correctly applies to new lock entries pending VFX manifest extension. WS1 wave-closes.

**Action for KR:** Add vfx_coverage_manifest.json extension to WS1A.3 implementation dispatch prerequisites.

---

## KR-cumulative-pattern-surface watch

- Elrond did NOT silently absorb the cardinality discrepancy — surfaced explicitly via report-back with "NOT silently resolved" discipline. PASS. This is the correct application of ADR-007 (honesty in surface) and dispatch § 2.2 ambiguity-surface protocol.
- Elrond seam authority on schema design honored throughout (4th field, enum values, physical taxonomy registry location — all within elrond seam authority). PASS.
- Lineage-tag aggregate resolution fully documented in MIGRATION.md with rationale. Traceable per migration script. PASS.

---

## Principle checks

**Principle 1 (math-before-code):** Migration was executed against verified verbatim per-primary entry lists (Gate-2-PASS-verified at commit `9889bff`). Math grounded in the correct source. The source doc wording (not the migration) contains the arithmetic error. PASS.

**Principle 2 (smoke-test / quality criterion):** 10-test smoke suite PASSES (per MIGRATION.md engine-side § "Backward-compat verification" 4 checkpoints + data-layer MIGRATION.md v1.7 § "Migration verification" 7 checkpoints). All checks green. PASS.

**Principle 3 (cross-seam impact):** ADR-004 MIGRATION.md authored both engine-side and data-layer-side. All affected seams enumerated. Round-trip ACKs documented. PASS.

**Principle 4 (decisions-log truth):** Decisions-log 2026-06-01 entry contains the "118 entries total" wording (inheriting from wave-close). Amendment-pass will correct this. Does NOT block WS1 wave-close — the architectural decision itself (Architecture A LOCKED) is correctly stated; only the cardinality wording requires correction. PASS on migration; WARN on wording.

**Principle 5 (severity matters):** WARN appropriate. Migration is correct; source-doc wording error does not block WS1 wave-close but MUST be corrected before downstream consumers (WS1A.3/WS1A.4) fire against the pool count. PASS.

**Principle 6 (cross-seam round-trip):** This IS the cross-seam contract change. Round-trip requirements met: MIGRATION.md at seam boundary, seam-owner ACK for all affected seams, tag deferred pending Gate-2 PASS. PASS.

---

## Summary

| Check | Result |
|---|---|
| Migration completeness (100 rotating per verbatim lists) | PASS |
| Schema extension (4 additive fields + safe defaults) | PASS |
| Cross-seam handling (MIGRATION.md × 2 + ACKs) | PASS |
| Backward-compat verification | PASS |
| Ambiguity 1 (cardinality discrepancy) | WARN — amendment-pass required pre-WS1A.3 |
| Ambiguity 2 (lineage tag aggregate) | INFO — elrond resolution RATIFIED |
| Ambiguity 3 (stormtide no-op) | INFO — no-op CORRECT |
| Drift-14 auto-demote | INFO — out-of-scope; forward note for WS1A.3 |

---

## Action items

- [ ] **Gandalf:** Author amendment-pass on 6 source-doc locations (PG-3 § 1.9, canonical lock § 0/§ 2.9/§ 7 header, wave-close record § 0, decisions-log 2026-06-01 entry) — correct "109 rotating / 118 total" to "100 rotating / 109 total" + correct § 7.1 lineage distribution to applied values (57/23/19/1). Add stormtide annotation in canonical lock § 3.3. Jack-ryan approves as within-seam documentation amendment (ADR-002 jack-ryan direct-approval authority on documentation-only changes).
- [ ] **KR:** Route elrond tagging (`elrond/v1.7-q18-pool-migration`) — tag CLEARS per this Gate-2 PASS-with-WARN. Tag does not require amendment-pass completion.
- [ ] **KR:** Add vfx_coverage_manifest.json extension to WS1A.3 dispatch prerequisites (Drift-14 forward note).
- [ ] **KR:** Route amendment-pass dispatch to gandalf (separate fire from WS1 routing). Amendment-pass REQUIRED before WS1A.3/WS1A.4 fire; does NOT block Q16/Q17/Q19 wave-fire.
- [ ] **KR:** WS2.P2+ / WS3 / WS4 / Q16/Q17/Q19 routing is unchanged — these are separate Matt-authorization items per workstream queue.

---

## References

- `/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json` (v1.1 migrated — reviewed)
- `/Users/admin/Games/reincarnated-engine/data/seasonal_elements/physical_taxonomy.json` (new Architecture-A registry — reviewed)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/element/schema.py` (PoolElement extended — reviewed)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/element/MIGRATION.md` (engine-side — reviewed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/MIGRATION.md` v1.7 (data-layer-side — reviewed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` (cardinality source — reviewed)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (cardinality source — reviewed)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md` (reviewed)
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` 2026-06-01 entry (reviewed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-06-01-q18-flavor-pool-lock-gate-2.md` (prior Gate-2)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-06-01-ws1-sub-phase-5f-gate-1.md` (prior Gate-1)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/post-q18-workstream-queue-2026-06-01.md` (workstream state)

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**For:** Gate-2 DEV-MODE review of WS1 sub-phase 5f pool.json migration (elrond; engine `fcc4887` + meta `d1beb95`). Cross-seam contract change per ADR-004.
