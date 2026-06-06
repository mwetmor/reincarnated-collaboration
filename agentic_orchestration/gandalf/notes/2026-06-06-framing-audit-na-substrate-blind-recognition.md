# Recognition Record — Framing-Audit Catches NA-Substrate-Blind Framing on Cosmograph Commission

**STATUS:** CURRENT (recognition record; load-bearing discipline-canonicalization)
**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 directive: "Do we not have live weapons to determine culture, period and magic vs physical (range vs close), etc?"
**Type:** discipline-affirmation recognition — framing-audit catches load-bearing assumption pre-commission at minimum cost; second canonical example for OP § 4.5

---

## 0. TL;DR

In the elrond commission scoping for the cosmograph, gandalf imported the "QDX-5 governance lapse → NA on cultural_tradition + period" framing without auditing it against substrate availability. Matt's one-question audit (`Do we not have live weapons to determine culture, period and magic vs physical (range vs close), etc?`) cheaply refuted the framing. **The 89,839-row weapon substrate underneath kits carries cultural_tradition + period + form-class at the weapon level; kits inherit derivable signatures via weapon-palette aggregation.** The governance lapse was about cohesion-judge enforcement at composition time, NOT about substrate availability.

This is the SECOND canonical example of the framing-audit discipline (OP § 4.1) catching a pre-imposed-assumption failure on authored scope before downstream work fires against bad framing. First example: Question A verdict § 12.1 (gamora Pattern-A query, 2026-05-23 evening). Cost of refutation in this case: ~30 seconds of Matt-question + ~4 minutes of gandalf evidence-check.

---

## 1. The framing failure

### 1.1 What gandalf imported

From the 2026-06-05 next-session plan § Phase 3:

> "Field-cleanup notes: governance lapse on QDX-5 means cultural_tradition + period are NA; include these columns with NA values rather than omitting (drax may want to surface 'substrate-thin' indicator)"

Re-stated in the 2026-06-06 onboarding-resume response:

> "Honesty columns | `cultural_tradition`, `period` — included as NA rather than omitted (QDX-5 governance lapse honesty) | substrate-thin flag"

### 1.2 The load-bearing assumption

The framing assumed: **QDX-5 governance lapse on kit-level cultural_tradition + period = NO derivable cultural_tradition + period at the kit level.**

The assumption was substrate-blind. It treated the kit as the lowest queryable layer when the kit COMPOSITION contains weapon references that join to a 89,839-row weapon substrate library where cultural_tradition + period ARE tagged.

### 1.3 The cheap refutation

Matt's one question: `Do we not have live weapons to determine culture, period and magic vs physical (range vs close), etc?`

The refutation evidence is in canonical and operational record:
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839 weapons with cultural_tradition + period + form-class tags
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` — substrate-led discipline + 4-mode tagging caveats
- `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json` — pre-existing weapon-form lookup infrastructure
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy work already established at the right layer

---

## 2. What this surfaces — discipline performance vs application slip

### 2.1 The discipline held

The framing-audit checklist (OP § 4.1) explicitly targets this failure mode:

| Q | Question | This case |
|---|---|---|
| Q1 | What load-bearing framing assumptions does this work depend on? | "Kit-level NA = no derivable cultural_tradition + period" |
| Q2 | What evidence currently in hand could refute these assumptions? | Weapon substrate library availability (4-minute check) |
| Q3 | If refutation evidence exists, is the right move to refine the framing rather than execute the work as-framed? | YES — derive from weapon-substrate join, not declare NA |

The discipline is correctly designed; the discipline would have caught this had gandalf applied it.

### 2.2 The application slipped

gandalf imported the NA framing from the 2026-06-05 next-session plan into the 2026-06-06 onboarding-resume response **without re-running the framing-audit on the new session.** The next-session plan WAS the latest gandalf authorship; gandalf inherited his own prior framing without auditing.

This surfaces a real failure mode: **same-author framing-inheritance bypasses framing-audit by feeling like "current state" rather than "load-bearing assumption."**

### 2.3 Matt as senior-designer doing the audit

Matt's question is exactly the framing-audit Q2 applied externally. The substrate-led discipline says "what does the data underneath actually contain?" — Matt asked that, gandalf hadn't.

This composes with the hive-mind decision-routing directive (Matt 2026-05-23, verbatim — seam-owner decides; Matt is LAST-resort escalation): **Matt-as-audit-trigger is GOOD operational signal, not bad operational signal.** It's the senior-designer noticing that the seam-owner's framing has substrate-blindness. The right response is to re-scope, not defend the framing.

---

## 3. Discipline-amendment proposal — framing-audit triggers on same-author state-imports

**Proposal:** the framing-audit checklist (OP § 4.1) fires NOT ONLY on new authoring, but also on **same-author state-imports** where prior framing carries forward into new scope.

Specifically: when gandalf carries forward a framing claim from a prior recognition record / next-session plan / dispatch authoring into a current commission spec or design call, the framing claim is RE-AUDITED at the import boundary, not treated as settled-because-self-authored.

**When to apply:**
- Any commission spec authoring that inherits framing from prior gandalf-authored docs
- Any dispatch authoring that inherits framing from prior recognition records
- Any next-session-plan execution where the plan's framing claims are now load-bearing on real commission specs

**Operational rule of thumb:**

> "If I wrote it yesterday, audit it today as if a peer wrote it."

This counters the same-author state-inheritance bypass.

### 3.1 How this composes with OP § 4.1

OP § 4.1 originally targeted framing-audit at NEW dispatch authoring AND ratification-firing AND work-unit start. This amendment ADDS: same-author state-inheritance crossing scope boundaries (prior-doc → current-commission) is a framing-audit trigger.

### 3.2 OP file-update target

Amend `~/Games/reincarnated-collaboration/.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` § 4.1 to add this trigger explicitly. Future operating procedure refinement task.

---

## 4. What changes downstream

### 4.1 Elrond commission re-scoped

Originally: NA on cultural_tradition + period (governance-lapse-blind framing).

Revised: **derive cultural_tradition + period signatures from weapon-substrate join.** Per-kit columns:
- `cultural_tradition_mode` (statistical mode across kit's weapon palette)
- `cultural_tradition_entropy` (within-kit variance — low = coherent; high = mixed)
- `period_mode` + `period_entropy`
- `magic_share` / `physical_share` (form-class proportions)
- `range_profile_derived` (cross-check against Tier 1 axis)
- `substrate_coherence_score` (composite of within-kit entropies)
- 4-mode rep-audit flag for Mode B/C/D risk per marginal-lineage caveat

### 4.2 Cosmograph design upgraded

The cosmograph axes become RICHER, not poorer. Cultural / period / magic-vs-physical signatures become first-class cosmograph properties players see and feel. D10 (genre-checkpoint) and D7 (AI-tell line via human-curated museum/Wikidata provenance) get reinforced.

### 4.3 DP8 resolves honestly

Substrate-thin indicator is NOT "NA columns" — it's `substrate_coherence_score` as a derived signal that the QDX-5 cohesion-judge governance underperformed. The cosmograph can honestly show coherence variation across the substrate without hiding behind NA.

### 4.4 4-mode tagging caveat still applies

The marginal-lineage-tagging-pattern doc's semantic-layer rep-audit caveat still binds: cultural_tradition derivation from weapon substrate needs rep-audit at firing if the cosmograph side-panel surfaces cultural-tradition claims as player-facing labels. Elrond's cycle-10 composition policy work covered much of this; gap analysis at commission time.

---

## 5. Composition with prior canonical

This recognition COMPOSES WITH:
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 5 (pre-milestone scoping; DP1-DP5)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` § 2.4 (semantic-layer rep-audit caveat)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (composition policy at the right layer)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` (89,839-row substrate state)
- `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` § 4.1 (framing-audit checklist)
- `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` § 4.5 (first canonical example — gamora Pattern-A query)

This recognition does NOT supersede:
- The cosmograph architectural commitment (2026-06-05) — pivot stays locked
- DP1-DP5 locks (cosmograph data source, axes, encoding, lasso, hosting) — refined, not reversed
- Substrate-led discipline — reinforced

---

## 6. Sign-off

**Authored:** gandalf 2026-06-06 per Matt audit-question + gandalf evidence-check
**Empirical-evidence trigger for OP § 4.1 same-author-state-import amendment:** when next gandalf operating-procedure refinement task fires, this recognition + the 2026-05-23 first canonical example (§ 4.5) together inform the discipline-amendment text
**Routing:** informs revised elrond commission spec authoring (NEXT in this session); informs cosmograph DP8 disposition; informs OP § 4.1 amendment task

**This is the second canonical example of framing-audit catching pre-imposed-assumption failure before downstream commission fires.** First was gamora Pattern-A query catching W1.13 H1-H5 baseline absence (~120 sec). This is Matt-question catching NA-substrate-blind framing (~30 sec Matt + ~4 min gandalf check). Pattern is consistent: cheap empirical refutation catches load-bearing assumption pre-execution at minimum cost.

**End of recognition record.**
