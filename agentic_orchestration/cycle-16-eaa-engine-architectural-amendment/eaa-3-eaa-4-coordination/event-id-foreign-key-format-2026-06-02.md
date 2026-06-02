# EAA-3 / EAA-4 Coordination — `event_id` foreign-key format LOCK — SUPERSEDED

**STATUS:** SUPERSEDED on 2026-06-02 by the joint EAA-3 + EAA-4 design verdict (which is more comprehensive and was authored earlier in the same Phase 1 session). This file is preserved as a navigation pointer.

**Authoritative source for FK format + storage decisions:**
`agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md`

**MIGRATION.md entries:**
- v1.8 (joint design): `agentic_orchestration/research/curated/MIGRATION.md` § v1.8
- v1.9 (EAA-4 implementation slice): `agentic_orchestration/research/curated/MIGRATION.md` § v1.9

**Implementation:**
- Chronicle schema (engine-side): `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`
- Layout README: `reincarnated-engine/data/kit_space/README.md`
- Smoke-test: `agentic_orchestration/research/scripts/eaa_4_chronicle_smoke_2026_06_02.py` (9/9 PASS TempDir + live)

---

## Why this file exists (brief)

Two elrond sessions ran in parallel during the EAA-4 fire window (Phase-1 batch Gate-1 INFO-B recommended joint EAA-3 + EAA-4 format coordination). One session authored the comprehensive joint spec in `elrond/notes/`; the other (this file's origin) authored an FK-only coordination doc here. Both reached LOCK K cross-dispatch coordination conclusions independently but with different format details.

**Reconciliation (data steward discipline):** the joint spec is more comprehensive (covers EAA-3 + EAA-4 together; includes shadow-table DDL; addresses ingest-compat verdict; names iteration points). It was authored first in the session timeline. It composes natively with rocket's EAA-3 work. The joint spec is therefore **authoritative**; this file is preserved as a navigation pointer to it.

**Authoritative format locks (from joint spec § 1 + § 2):**

| Field | Format | Regex |
|---|---|---|
| `event_id` (chronicle) ≡ `kit_space_expansion_event_id` (per-kit FK) | `kse_<YYYYMMDD>_<seq3>` | `^kse_\d{8}_\d{3}$` |
| `kit_id` | `kit_<primary>_<seq6>` | `^kit_(fire\|water\|earth\|wind\|lightning\|holy\|shadow\|physical)_\d{6}$` |
| `primary_element` | lowercase canonical-7+1 | — |
| `period` | `ANCIENT` / `MEDIEVAL` / `MODERN` (nullable) | — |
| `engine_version_sha` | 7-char short SHA | `^[0-9a-f]{7}$` |

**Authoritative storage medium (from joint spec § 3):**
- Option α (source-of-truth): flat `data/kit_space/kit_space_chronicle.json`
- Option β-light (analytical shadow): `engine_kit_space_events` + `engine_kit_index` tables in elrond's catalogue.db

Both EAA-3 and EAA-4 implementation MUST use these formats and this storage layout. Round-trip integrity verified via smoke-test 9/9 PASS.

---

**End of superseded coordination note.**
