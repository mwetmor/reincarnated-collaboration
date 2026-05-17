# Dispatch — 2026-05-16 — legolas — HD-2D shipped-game screenshot ground-truth measurement (Section 3 closure)

**From:** knight-rider (authored per legolas pixel-scale research completion 2026-05-16; Section 3 findings-blocker surfaced — Spriters Resource HTTP 403, no public px-measurement source)
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4 ("fire all three follow-ons")
**Status:** PENDING
**Mode:** A (analytical; screenshot measurement)
**Estimated effort:** 30-45 min; hard cap at 45 min
**Budget:** $0 LLM

**Gate-1 bypass rationale:** Matt-directed, single-seam (legolas-only), read-only research, very small scope, bounded time. Per CHANGELOG rubric.

**Acceptance summary:** Section 3 of `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` upgraded from PARTIAL to COMPLETE. At least two of the three HD-2D reference titles get measured px-heights at known display resolution. Internal-vs-displayed pixel semantic clarified (Sea of Stars 640×360 internal vs 1080p output ratio confirmed; same check on Octopath + Eiyuden if data accessible).

---

## Why this dispatch exists

Your prior pixel-scale research surfaced a Section 3 findings-blocker:

> "Spriters Resource returned HTTP 403 on all asset pages — the canonical source for sprite sheet dimensions is inaccessible. No forum, developer interview, or technical blog documents exact on-screen character pixel heights. Derived estimates provided; local screenshot measurement (30 min) would close this gap definitively."

This dispatch executes the 30-min local-screenshot measurement option.

**Gandalf will use this data** to resolve a semantic question: does his "80-100 px HD-2D target" refer to internal sprite pixel count or displayed pixel count? Without the ground-truth measurements, gandalf's per-character + per-monster lookup-table recommendations may be off by a 3× factor (the SoS internal-to-displayed ratio).

## Cross-seam contract change?

**Round-trip: not applicable** — research output is a doc; no schema or contract change; no production state modified. Per R11(b) Principle 6.

## What this dispatch produces

Amendment to Section 3 of `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`.

### Required measurements

For each of the three HD-2D reference titles (Sea of Stars / Octopath Traveler / Eiyuden Chronicle: Hundred Heroes), document:

1. **Source identification** — what screenshot / video / gameplay capture used? Include direct URL + timestamp for traceability.
2. **Display resolution confirmation** — 1080p / 1440p / 4K display? Internal render resolution if known (e.g., Sea of Stars 640×360 internal × 3 upscale).
3. **Character px-height at displayed pixels** — measured feet-to-top-of-head (exclude hair/hat protrusions); ±5 px tolerance acceptable.
4. **Character px-height at internal pixels** — if internal-rendering resolution differs from display, compute the corresponding internal-pixel-count.
5. **Source / methodology note** — how was the measurement taken (gameplay screenshot via Steam / YouTube frame-grab / reviewer screenshot / etc.)?

### Required interpretation

Add a closing paragraph to Section 3 addressing:

- Which px-count gandalf should anchor on: **internal sprite px-count** or **displayed px-count**
- Implication for the synthesis table in Section 4 (does it need a scale-factor revision based on the semantic clarification?)
- Confidence band on the 80-100 px range claim — is it well-supported by 2-3 reference titles, or only weakly?

### Two viable methods

**Method A — Public screenshots.** YouTube gameplay videos at confirmed 1080p, Steam reviewer screenshots, dev-blog screenshots. Lower confidence but accessible.

**Method B — Local game install (if any title is on Matt's machine).** Highest confidence — direct measurement at known display resolution. Matt has NOT yet authorized game purchases for this purpose; do NOT recommend purchase. Use Method A unless Matt already owns one of the titles on accessible install.

### Findings-blocker fallback

If Method A still fails (paywall, no usable screenshots at confirmed resolution): document the blocker, deliver best-effort estimate with confidence caveat, and STOP. Time cap is 45 min hard. Better to deliver partial Section 3 with a clear note than to expand scope.

## Out of scope (explicit)

- **NO new vendor catalogue work.** Mode A scope is screenshot measurement only.
- **NO sprite-sheet-acquisition recommendations.** Out of scope; design / catalogue concern.
- **NO scale-factor recommendations beyond the Section 4 synthesis amendment.** The lookup-table authorship is gandalf's; you supply the empirical anchor.
- **NO commentary on whether to expand to additional HD-2D titles.** Three titles are sufficient; if any fails, stop at two.
- **NO recommendation on Matt purchasing game installs.** Out of scope.

## Required reading

- Your prior research doc: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — Section 3 + Section 4 synthesis to be amended
- `agentic_orchestration/gandalf/requests/2026-05-16-legolas-character-monster-pixel-scale-research.md` — original commission

## Acceptance criteria

- [ ] Section 3 amendment filed in the existing research doc (modify in-place; preserve other sections)
- [ ] At least 2 of 3 reference titles measured (Sea of Stars priority; Octopath secondary; Eiyuden tertiary)
- [ ] Internal-vs-displayed px semantic resolved with recommended gandalf anchor
- [ ] Section 4 synthesis table updated if recommendation revises scale factors
- [ ] Time cap honored (≤ 45 min)
- [ ] Knight-rider notified with: section completeness status, gandalf-anchor recommendation, any new findings-blockers

## Tag policy

- **No git tag** (research persona; file timestamp suffices)

---

## Completion record

**Completed:** 2026-05-16
**Titles measured:** 2 (Sea of Stars, Octopath Traveler). Eiyuden Chronicle tertiary — not measured per dispatch priority.
**Internal-vs-displayed recommendation:** DISPLAYED pixels at 1080p is the correct anchor for gandalf's 80–100px target. At overworld/exploration camera distance: SoS 75–90px, OT 80–90px — both in range. OT battle camera: 120–130px (above range; clarification needed from gandalf on which camera context the target applies to).
**Scale-factor revisions in Section 4:** Section 4a/4b/4c scale numbers NOT revised (remain valid). Section 4d ADDED: semantic implications of the measured ground-truth. Prior Section 3 "79px internal → 237px displayed" framing corrected — this was a mis-application of the 3× upscale factor to perspective-rendered sprites.
**Time spent:** ~43 min
**Findings-blockers (if any):** Sprite TEXTURE heights (the original art canvas the artist drew) remain unconfirmed for both titles — Spriters Resource 403-blocked, SoS modding community has no documented sprite dimensions. The display-pixel measurements are confirmed; texture-pixel heights would require game file extraction not possible from public screenshots.
**Notes for knight-rider:** The "3× factor is the load-bearing question" from the dispatch is now resolved: the 3× is a DISPLAY upscale of the entire 640×360 rendered frame, NOT a direct indicator of sprite texture size. Gandalf's 80–100px target should be interpreted as displayed px at 1080p. One open question remains: battle vs overworld camera context for the target — OT battle exceeds the range at 120–130px. Recommend flagging this to gandalf.
