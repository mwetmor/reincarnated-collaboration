# Gate-2 Finding — EAA-3 + EAA-4 elrond-side bundle review (FK format reconciliation)

**Date:** 2026-06-02
**Reviewer:** jack-ryan (DEV-MODE Gate-2 with BLOCK authority)
**Routed by:** knight-rider (after EAA-3 + EAA-4 elrond-side completion notifications surfaced contradictory FK formats)
**Bundle under review:**
- `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md`
- `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md`
- `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`
- `agentic_orchestration/research/curated/MIGRATION.md` § v1.8 + § v1.9

**Authority:** Matt 2026-06-02 + Locks A-P + LOCK K schema design authority + escape clause #6 cross-seam contract semantic changes (assessed: NOT triggered; documentation-drift only)

---

## VERDICT: BLOCK on joint-spec § 1.1–1.2 UUID-hex drift

Single-file amendment by elrond resolves the BLOCK. All other bundle items PASS. Gate-2 closes to PASS-with-INFO once joint-spec § 1.1–1.2 is amended and elrond confirms.

---

## Canonical FK format disposition

**CANONICAL FORMAT:** SEQ-3 — `kse_<YYYYMMDD>_<seq3>` / regex `^kse_\d{8}_\d{3}$`

**Grounds:**
1. `CHRONICLE_SCHEMA.md` § 3 uses SEQ-3 form (implementation)
2. `MIGRATION.md` v1.9 uses SEQ-3 form and names the locked regex explicitly + supersedes UUID-hex
3. `eaa-3-eaa-4-coordination` doc is self-labelled SUPERSEDED and its format table restates SEQ-3
4. Smoke 9/9 PASS is against SEQ-3 implementation

**UUID-hex appears ONLY in joint spec § 1.1–1.2 body text.** That body text is documentation-drift: the joint spec § 1.0 header claims to ADOPT the pre-existing coordination doc, but was authored at a point when that doc still held UUID-hex. The coordination doc was subsequently reconciled to SEQ-3 AND marked SUPERSEDED, while the joint spec body text was never amended. **Empirical-current-truth is unambiguously SEQ-3.**

---

## Reconciliation pathway

**REQUIRED before EAA-5 fire (one file):**

- **joint-spec § 1.1**: replace UUID-hex format block + regex + example with SEQ-3 equivalents (format `kse_<YYYYMMDD>_<seq3>`; regex `^kse_\d{8}_\d{3}$`; example `kse_20260602_001`).
- **joint-spec § 1.2**: replace UUID-hex rationale bullets with SEQ-3 rationale (mirrors CHRONICLE_SCHEMA.md § 3 language; emphasise seq query at emit-time, 999/day bound, human-inspectable ordering). Remove distributed-safe / collision-resistant bullets — those were UUID-hex-specific and do not apply.
- **Amending agent:** elrond (joint-spec author; data steward; LOCK K seam authority).
- **No code change required.** CHRONICLE_SCHEMA.md, MIGRATION v1.9, and the coordination doc are already consistent with SEQ-3.

**ALREADY CLEAN (no action needed):**
- `CHRONICLE_SCHEMA.md` § 3: SEQ-3 — correct
- `MIGRATION.md` v1.9 format table: SEQ-3 — correct
- `eaa-3-eaa-4-coordination` doc format table: SEQ-3 — correct (status = SUPERSEDED is navigation-pointer; format table rows are accurate)

---

## Disposition severity: BLOCK

Joint spec § 1 is the document rocket reads as the "authoritative format verdict" per its own header. As long as § 1.1 body text shows UUID-hex with a 27-char regex, rocket's combined fire may emit UUID-hex `kit_space_expansion_event_id` fields. Those will fail the `CHRONICLE_SCHEMA.md` § 3 FK regex at EAA-5 first-fire.

**Cross-seam FK contract clarity** = Review Principle 5 + Discipline #8 (schema validation at boundaries). The joint spec § 1 amendment is a single-file documentation correction within elrond's seam authority (ADR-002 direct-approve tier), but it must land BEFORE rocket's EAA-3 schema spec finalizes.

**Cited disciplines:** Discipline #8 (schema validation at boundaries), ADR-004 (cross-seam MIGRATION discipline), Review Principle 5 (severity matters).

---

## Rocket coordination

**Recommended:** **(b) send mid-stream signal NOW.** Knight-rider should surface to rocket's in-flight session:

> "canonical FK = SEQ-3 (`kse_<YYYYMMDD>_<seq3>` / `^kse_\d{8}_\d{3}$`). Joint spec § 1.1 body text shows UUID-hex — that is documentation drift; IGNORE it. Binding sources are CHRONICLE_SCHEMA.md § 3 + MIGRATION v1.9."

Do NOT wait for wave-close. If rocket has already written UUID-hex into the EAA-3 schema draft, that field must be corrected before EAA-3 ships. Do NOT block rocket entirely — let it continue with the correct format in hand.

---

## ADR-002 escape-clause check

**Documentation-drift correction only.** No semantic change to the format — SEQ-3 was locked by elrond as EAA-4 primary owner; the joint spec body text simply failed to track the reconciliation. This is within elrond's seam authority to amend directly (ADR-002 documentation-only tier). **Matt escalation NOT required.** KR routes elrond amendment as a micro-task concurrent with rocket's in-flight work.

---

## Other Gate-2 topics (bundle review)

- **Chronicle storage medium** (joint spec § 3, Option α + β-light): PASS. Flat JSON source-of-truth + rebuildable shadow tables is consistent with ADR-004 (MIGRATION pattern) and LOCK K (additive/reversible). No concern.
- **Emit-order discipline** (CHRONICLE_SCHEMA.md § 5, chronicle FIRST → per-kit SECOND, atomic `.tmp` → `os.replace`): PASS for EAA-5 first-fire safety. Atomic write prevents partial state; chronicle-first ensures FK exists before referencing record. Sufficient.
- **kit_id format** (`kit_<primary>_<seq6>`): PASS. Composes with engine kit-naming; regex locked consistently across all three canonical artifacts. No drift observed.
- **Out-of-scope reaffirmations** (telemetry boundary, realm-expansion `re_` prefix reserved, per-kit player engagement deferred): PASS. All boundaries clean and consistent with dispatch scope per LOCK K + ADR-006.

---

## Disposition

BLOCK on joint-spec § 1.1–1.2 UUID-hex drift. Single-file amendment by elrond under direct-approve authority. Mid-stream signal to rocket required now. All other bundle items PASS. **Gate-2 re-fire required** after elrond amendment lands + rocket DRAFT verifies FK-correct.

**Next gate logic:**
- Elrond amends joint spec § 1.1–1.2 (concurrent micro-task)
- Rocket combined fire continues with mid-stream signal in hand
- After both: jack-ryan Gate-2 re-fire on the converged bundle → expected PASS-with-INFO
- Then: star-lord fires for EAA-3 § 3.3 emit + EAA-4 § 3.3 chronicle emit integration

**End of Gate-2 BLOCK finding.**
