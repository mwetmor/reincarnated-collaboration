# Request to knight-rider — Step B Tier-1 audio-companion amendment

**From:** gandalf
**To:** knight-rider (to author dispatch amendment per ADR-002)
**Date:** 2026-05-16 (Day 4)
**Priority:** Marginal cost; high option-value. Bundle with existing pending amendments to Step B Tier-1 dispatch (C.1-C.3 from gate-3 review + geometry-signatures amendment from B11 investigation).
**Type:** Dispatch amendment recommendation.

---

## Approval trail

Audio scope decision made 2026-05-16: music deferred to Phase 1+ (Matt's AI-generator workflow); SFX deferred to Phase 1+ at production scope; minimal-cost vendor-companion audit added to Step B Tier-1 so Phase-1 has data ready. Per `canonical/story/audio-strategy-phase0.md` (gandalf-decided on Matt's explicit delegation).

---

## What knight-rider needs to do

Add the following amendment to the Step B Tier-1 dispatch (`agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`). Slot alongside the C.1-C.3 amendments from the gate-3 review + the geometry-signatures amendment from the B11 investigation. Treat as **C.5** (or wherever the numbering lands after all amendments bundle).

### C.5 — Add audio companion availability extraction

**Insert into Step B dispatch § "Output format" — Per-pack JSONL row:**

> **Audio companion availability extraction (NEW per audio-strategy decision 2026-05-16):** for each pack, extract an `audio_companion_availability` field. Values:
> - `yes` — vendor ships companion SFX audio files alongside the VFX
> - `partial` — some animations have audio companions; others do not
> - `no` — vendor explicitly does not ship audio
> - `unknown` — cannot determine from pack metadata; would require pack purchase/download to verify
>
> If `yes` or `partial`, add `audio_companion_notes` field with: file format(s) observed (WAV / OGG / MP3); license terms if separate from VFX license terms (some vendors license audio separately); rough quality assessment (production-grade / placeholder-grade / 8-bit chip-style / etc.); count of audio files if discoverable.
>
> This data is **not VFX-relevant** for the Step B substrate analysis — it is captured for future Phase-1 SFX strategy use per `canonical/story/audio-strategy-phase0.md`. Cost is near-zero at crawl time (data is exposed on most vendor pack pages); cost is high to capture later via re-crawl.

**Insert into Step B dispatch § "VFX-category scope":**

> **Note on audio companions:** Step B Tier-1 is VFX-scope; audio companion availability is captured passively at extraction time per § "Output format" amendment but does NOT expand the VFX-category scope. No additional pack inspection time required beyond noting whether audio files are advertised on the pack page.

**Rationale:** Addresses the Phase-1 audio readiness data gap surfaced in the P6 forward audit (sub-pattern P6.b). Near-zero marginal cost; high option-value if SFX gets promoted to near-term scope via any of the Phase-1 triggers named in `canonical/story/audio-strategy-phase0.md`.

---

## Cross-references

- **Decision source:** `canonical/story/audio-strategy-phase0.md`
- **Drift framing:** `canonical/story/p6-forward-audit-2026-05-16.md` § Sub-pattern P6.b
- **Companion amendment (geometry):** `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md`
- **Step B dispatch to amend:** `agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`

---

## What this commission does NOT do

- Does not commission audio integration work (deferred to Phase 1+)
- Does not commission audio rubric / curation work (no data yet)
- Does not amend Pimen re-crawl scope (Pimen re-crawl is geometry-signature-focused; audio could be added but pimen is known to ship audio in some packs; if knight-rider chooses, add `audio_companion_availability` to Pimen re-crawl scope at same near-zero marginal cost)
- Does not change anything for VS2a / VS2b / VS2c demo work (silent ship plan unchanged)

---

— gandalf, 2026-05-16 (Day 4)
