# Drax /forge Phase 5 AMENDMENT — Cycling Text-List UI + Cosmograph Response

**STATUS:** ACTIVE (commission ready to fire)
**Date:** 2026-06-10
**Author:** gandalf
**Authority:** Matt 2026-06-10 — "fire A then prompt B via KR then prompt C via DH" + § 12 canonical lock (commit 861403d)
**Mode:** Mode L (loadout React/Vite/Tailwind/Vercel; /forge sub-route extension; Phase 5 ADDS to Phase 4 amended GREEN baseline)
**Audience:** drax (executor), gandalf (design-review at Vercel preview), Matt (architectural feedback)
**Companion docs (read first):**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 12 (CANONICAL lock 2026-06-10)
- `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-4-AMENDMENT-rune-per-group-two-tier.md` (Phase 4 amended GREEN; superseded for icon scope by § 12)
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-4-amended-close-report.md` (Phase 4 close; 29 placeholder icons flagged)

---

## 0. TL;DR

**Mission:** Refactor Phase 4 amended Tier 2 panels from placeholder-icon shells to **text-list cycling UI** per § 12 canonical lock. Add **cosmograph response animation** to highlighted text-list options. Implement **cluster spatial layout** for 7 sky regions per § 12.3.

**Empirical trigger:** Earth-Avatar Creation Moment Architecture § 12 addendum 2026-06-10 LOCKED — per-primitive iconography RETIRED at prior framing scope; 29 placeholder icons DEPRECATED; iPad-text + sky-runes-only split CANONICAL.

**Substrate consumed:** existing /forge Phase 4 amended baseline (6 rune-anchors; force-directed positioning; current kit corpus) + § 12 7-anchor canonical list + cascade text vocabulary (drax discretion within bounds per § 2.3 + § 12.13 open refinement deferred).

**Estimated wall-clock:** 2-4 wall-clock days; deployable to Vercel preview per sub-phase milestone.

---

## 1. Architectural pattern to implement (per § 12)

### 1.1 Cognitive load split CANONICAL (§ 12.2)

| Surface | Carries |
|---|---|
| **iPad screen** | Text labels at every cascade layer; spirit guide narration zone; HD-2D pixel typography per style-register |
| **Cosmograph** | Sky cluster regions; rune-anchors per § 11.2 Tal Rasha § 4.2 (large + atmospheric + light-edge brush-stroke + no color) |

**Per-primitive iconography RETIRED.** Remove all 29 placeholder icons from Phase 4 amended deployment.

### 1.2 7 Tier 1 anchors CANONICAL (§ 12.3)

iPad opening question (spirit guide voice): *"What is most important for your journey this season?"*

| # | Anchor (text label) | Sky cluster response |
|---|---|---|
| 1 | Race / ancestry | Race-tribal sub-clusters illuminate |
| 2 | Element / flow | Element-cluster region illuminates |
| 3 | Weapon / craft | Weapon-form cluster region illuminates |
| 4 | Power / mastery | T4-strategy clusters illuminate |
| 5 | Style / way | Target-Pattern + Depth-vs-Breadth clusters illuminate |
| 6 | Harvest / rewards | Speedfarming + Loot-Focus sub-clusters illuminate |
| 7 | Horizon / goal | Progression-Stage clusters illuminate |

### 1.3 Cycling-preview UX vocabulary CANONICAL (§ 12.4)

1. iPad displays text-only cycling list at current cascade layer
2. Player cycles via touch-drag / swipe / arrow taps
3. **Soft preview:** cosmograph sky region corresponding to highlighted option illuminates; camera focuses; other regions dim
4. **Cycling != committing** (browse freely)
5. Commit via tap; cosmograph LOCKS focus
6. Spirit guide narrates on commit only (not during cycling)
7. iPad refreshes to next cascade layer

### 1.4 Nested cascade (§ 12.5)

Same cycling mechanic at every layer. 3-5 layers deep typically. Player commitments cascade until nearest-kit-centroid emerges. Final emergence narrated by spirit guide.

### 1.5 7 sky cluster regions spatial layout

Drax discretion within § 12.3 + style-register coherence; surface tradeoffs in close report. Cosmograph view should allow camera fly-through between regions per cycling-preview.

---

## 2. Scope per sub-phase

### Phase 5.1 — Remove 29 placeholder icons + text-list Tier 2 UI
- Delete 29 placeholder icons from Tier 2 panels per § 12.10 DEPRECATION
- Implement text-list UI at Tier 2 (cycling-touch-friendly; readable typography per style-register HD-2D pixel)
- Composes with Phase 4 amended rune-anchors (rune layer preserved; Tier 2 panel layer refactored)
- Deploy to Vercel preview
- **Acceptance:** placeholder icons removed; text-list Tier 2 cycling functional; rune-anchor layer unchanged

### Phase 5.2 — 7 Tier 1 anchor list + opening question
- Implement spirit guide opening question text: *"What is most important for your journey this season?"*
- Implement 7-anchor cycling list per § 12.3
- Cycling produces soft-preview state (no commit)
- Tap commits to anchor
- Deploy to Vercel preview
- **Acceptance:** opening question displays; 7 anchors cyclable; tap commits + cascade fires to Tier 2

### Phase 5.3 — Cosmograph response animation
- As player cycles Tier 1 anchor, cosmograph camera focuses on corresponding sky cluster region
- Other regions dim; selected region illuminates
- Smooth animation (~0.3-0.5 sec transitions per § 12.4)
- 7 sky cluster regions mapped per drax discretion within § 12.3
- Composes with Phase 4 amended cosmograph rendering
- Deploy to Vercel preview
- **Acceptance:** cycling produces cosmograph response; animation smooth; 7 regions distinguishable

### Phase 5.4 — Nested cascade (recursion to Tier 2+)
- After Tier 1 commit, iPad refreshes to Tier 2 question + options
- Cycling mechanic recurses identically
- Cosmograph zooms further into sub-cluster on Tier 2 option highlight
- Cascade continues 3-5 layers deep
- Final emergence: spirit guide narrates matched-kit identity
- Deploy to Vercel preview
- **Acceptance:** cascade recursion functional; minimum 3 layers deep; final emergence narration displays matched-kit

### Phase 5.5 — Phase 5 close report
- Per-acceptance-criterion verdict
- Cluster spatial layout final + tradeoff observations
- Cascade text vocabulary draft (Tier 2/3 question phrasings — drax discretion within § 12.13 open refinement)
- Cycling animation timing tuning observations
- Methodology hotspots flagged for elrond consultation
- Phase 5 GREEN / YELLOW / RED verdict
- Gap notes for UE-port scope (spherical-shell geometry deferred per § 2.6)

---

## 3. Acceptance criteria

| # | Criterion |
|---|---|
| 1 | 29 placeholder icons removed from Phase 4 amended Tier 2 panels |
| 2 | Text-list cycling UI implemented at every cascade layer |
| 3 | 7 Tier 1 anchors operational (Race / Element / Weapon / Power / Style / Harvest / Horizon) |
| 4 | Spirit guide opening question displays |
| 5 | Cycling produces cosmograph response animation (~0.3-0.5 sec smooth transitions) |
| 6 | 7 sky cluster regions spatially distinguishable in cosmograph |
| 7 | Nested cascade recursion functional (minimum 3 layers deep) |
| 8 | Final emergence narration displays matched-kit identity |
| 9 | Path L (lasso) + Path I (drop-ingredients) unified via cycling-preview per § 12.8 |
| 10 | Phase 4 amended rune-anchor layer preserved (sky runes visual register per § 11.2 + § 12.2) |
| 11 | Style-register coherence preserved (HD-2D pixel typography for iPad text per style-register.md) |
| 12 | Mobile-responsive at iPad-class viewport (D8); touch-input cycling functional |

---

## 4. Discipline citations

- **Discipline #41 (substrate-led)** — text-list cycling is substrate-led at UX layer per § 12.7
- **Discipline #25 (semantic-layer rep-audit)** — cluster naming + cascade text vocabulary audit at gandalf review (Phase 5.3 + 5.4 milestones)
- **D7 AI-tell line** — spirit guide narration templated; no raw LLM dialogue
- **D8 mobile-friendly** — text-list + touch-cycling natively mobile-friendly
- **Recognition-validate-commit** — Phase 5 IS empirical validation of § 12 canonical architecture at player surface

---

## 5. Out of scope

- ❌ Per-primitive iconography (RETIRED per § 12.10)
- ❌ Replacement canonical icons for the 29 deprecated placeholders (NOT NEEDED per § 12.10)
- ❌ Spherical-shell celestial geometry (UE-port scope per § 2.6)
- ❌ Niagara VFX rendering (UE-port scope; WS2 commission)
- ❌ AAA fidelity visual register (UE-port scope)
- ❌ Cluster naming canonical lock (deferred to Pattern B per § 12.13)
- ❌ Spirit guide voice character canonical lock (deferred per § 12.13)

---

## 6. Composition with prior work

| Prior work | Composition |
|---|---|
| Phase 4 amended GREEN (`170dd23` / `e1c9046`) | Phase 5 EXTENDS; rune-anchor layer preserved; Tier 2 placeholder-icon shells refactored to text-list |
| Earth-Avatar Creation Moment Architecture § 12 (commit `861403d`) | Phase 5 IS the player-surface validation of § 12 canonical architecture |
| Tal Rasha glyphic primitive-anchor architecture recognition | Rune visual register per § 11.2 preserved |
| Style register (HD-2D pixel-art) | iPad text typography per style-register.md |

---

## 7. Deliverables

1. Vercel preview deployment at each sub-phase milestone (5.1 → 5.5)
2. Phase 5 close report at `agentic_orchestration/drax/notes/2026-06-XX-forge-phase-5-amendment-close-report.md`
3. Code changes in `reincarnated-loadout/` per drax seam; auto-commit per CLAUDE.md addendum

---

## 8. Sign-off

**Authored:** gandalf 2026-06-10 per Matt directive ("fire A") + § 12 canonical lock.
**Authority:** gandalf design-side commission authority + Matt direct authorization.
**Routing:** drax executes; per-sub-phase Vercel preview deployments for gandalf review; Phase 5 close routes to gandalf + Matt.
**Empirical-evidence triggers:** Phase 5 close GREEN → vertical-slice spike commission amendment absorbs Phase 5 findings; § 12 canonical lock empirically validated.
**Composition:** all prior canonical commitments preserved.
**End of commission.**
