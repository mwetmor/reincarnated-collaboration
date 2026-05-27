# Cycle 14 — Caster-Faith Remediation Verdict (Path A vs B vs Hybrid)

> **STATUS:** VERDICT (Pattern A-deep design-fit verdict per gandalf OP § 2) — design call ratified by gandalf; routes to knight-rider for cross-seam orchestration.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 ratified scaffold-drift consolidated package + hive-mind decision-routing directive (Matt 2026-05-23); KR Pattern-A query 2026-05-27 routed gandalf design call on caster-faith remediation path.
**Anchor docs cited:**
- `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md` (Fix C audit — empirical evidence)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` § 2.1 (the algorithmic classifier rule producing the mace dominance)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3.1 (per-attribute weapon profile — WIS expectations)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3.2 (Option β caster cells — attribute-level match)
- `canonical/story/attribute-system-2026-05-24.md` § 1.3 + § 3 (WIS attribute semantics — internal canonical tension noted below)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 2.4 + § 4 Discipline #40
- `agentic_orchestration/gandalf/notes/2026-05-27-substrate-weapon-family-balance-sidecar-request.md` (Fix A/B/C origination)

---

## 0. TL;DR

**VERDICT: HYBRID (B-now + A-queued, with elrond classifier amendment as A's substrate-side execution).**

- **Wave 2 — Path B** (runtime within-caster-shape sampling adjustment in `substrate_weapon_binding.py`): ships alongside Fix B; rocket-only seam; un-blocks Wave 5 gauntlet from "62% of casters are clerics-with-maces" identity collapse.
- **Cycle 15 (queued) — Path A** (substrate-classifier reclassification with rule amendment): fires AFTER Wave 5 gauntlet evidence confirms within-family identity beat is the load-bearing problem (vs. one of several thinness symptoms a richer C-series fix would address).
- **Discipline #40 invocation:** Path B IS a scaffold-with-pending-decision. MIGRATION.md + roadmap flag required at Wave 2 commit time. The pending decision is "do we keep the cleric-with-mace canon (Path B permanent) or reclassify per Path A (substrate amended)?" That decision gates on Wave 5 + Phase 5 cohesion-judge output.

**Why HYBRID, not pure Path A:**

1. Path A as elrond framed it (move mace-family rows out of caster-faith into martial-heavy/light) is **mechanically right** but **bypasses the actual classifier bug**. The bug is upstream: SC-6 § 2.1's rule says `primary_stat='WIS' → caster-faith` unconditionally. There is no within-WIS discriminator between (focus / censer / talisman / channeling-staff / holy-symbol) and (mace / war-hammer with WIS-divine-channeling). Fixing the symptom (reclassify rows) without fixing the rule (no within-WIS discriminator) means the next ingest pass reproduces the bug.
2. Path A also has a **design-intent ambiguity we have NOT resolved yet** — see § 2 below. The canon (attribute-system doc § 1.3) lists maces under WIS weapon families ("Cleric, Druid, Holy Knight... Maces, holy-symbols, ritual-implements"). The canon (attribute-system § 3) ALSO maps mace as primary=STR/secondary=WIS. Both can't be right. Path A pre-commits to the second interpretation without a design call confirming it.
3. Path B is **non-destructive** (substrate stays as-is; reversible at sampling-weight tunable). If Wave 5 gauntlet output reveals the within-family identity beat is fine once mace sampling is dialed back, Path A becomes unnecessary and we keep the cleric-with-mace canon as a sometimes-sampled archetype. If Wave 5 reveals the deeper problem (faith-instrument substrate is just too thin period), Path C (substrate enrichment via legolas Mode B) is the correct fix, not Path A.

Path B buys empirical evidence at minimum cost; Path A waits for that evidence + a design-intent resolution.

---

## 1. The empirical finding (per elrond Fix C audit § 2.2)

Caster-faith post-Fix-A footprint (146 rows):

| sub-shape | n | % |
|---|---|---|
| **mace_hammer_family** | **90** | **61.6%** |
| other | 25 | 17.1% |
| sacred_symbol_or_ritual_item | 13 | 8.9% |
| incense_ritual_implement | 12 | 8.2% |
| staff_scepter_rod | 6 | 4.1% |

This is the D&D "cleric-carries-a-mace" trope bleeding into the substrate classifier. Uniform sampling produces a mace 62% of the time. The within-WIS identity beat — the canonical *visual* and *mechanical* distinction between a cleric with censer, an oracle with rod, a druid with channeling-staff, a witch doctor with talisman, a holy knight with mace — collapses at the substrate layer to "WIS character = mace, mostly."

This is identical to the kind of substrate-led failure that produced Cycle 13's `_SyntheticPlayerClass` chaos (doc 47 § 1.1 + § 6 Discipline #38 candidate framing): substrate vocabulary inherited a genre-canon trope unfiltered, and the trope dominates downstream sampling because no within-family discriminator exists.

---

## 2. Design-intent ambiguity that Path A pre-commits without resolving

The canonical attribute-system doc carries internal tension on the mace question:

**Attribute-system § 1.3 (WIS — Wisdom):**
> Class archetypes: Cleric, Druid, Holy Knight, Ritualist, Channeler, Oracle, Witch Doctor
> Weapon families: **Maces**, holy-symbols, ritual-implements, channeled-staves, censers, horns

**Attribute-system § 3 (attribute-weapon coupling table):**
> Mace / war-hammer (one-handed): primary=**STR**, secondary=**WIS** — "Holy-warrior pattern; STR-primary, WIS-divine-channeling"

These are inconsistent. § 1.3 lists mace as a WIS family weapon (primary=WIS implicit). § 3 maps mace as primary=STR / secondary=WIS. The substrate's SC-6 § 2.1 classifier rule (`primary_stat='WIS' → caster-faith`) requires the row's `primary_stat` to be WIS already — meaning the substrate row was tagged WIS upstream, not STR-with-WIS-secondary. So the substrate disagrees with § 3 (which says mace primary=STR) and aligns with § 1.3 (which says mace family lives under WIS class archetypes).

**Which interpretation is correct?** I do not know without a design call.

- **Interpretation I (canonical clarification: maces ARE a faith weapon family):** Cleric/holy-knight tradition is the cultural anchor; the mace IS a faith instrument per the D&D + AD&D + historical-ecclesiastical canon. The substrate is right. The within-family identity beat is supposed to include "cleric with mace" as one of several faith-caster archetypes. Path B is correct (dial back over-sampling to ~20-30% rather than 62%); Path A is WRONG (would strip a canonical faith-class archetype).
- **Interpretation II (canonical clarification: mace is a STR weapon that incidentally carries WIS scaling on hybrid kits):** The § 3 table is correct; § 1.3's listing of mace under WIS weapon families is wrong (legacy bleed from D&D-cleric trope without mechanical reconciliation). Path A is correct (substrate misclassified); reclassify maces out of caster-faith.
- **Interpretation III (the genre-precise read):** Both can be true depending on the SPECIFIC mace. Ceremonial maces / blessed maces / censers-evolved-from-flails = faith. Battle maces / flanged maces / spiked maces / siege maces = martial. The substrate's classifier is too coarse — it doesn't distinguish ceremonial-mace from battle-mace.

I lean toward **Interpretation III** (the genre-precise read) as the most faithful to genre canon, but locking it requires a Matt design call. Path A pre-commits to Interpretation II without that call. Path B is interpretation-agnostic (it just under-weights ALL mace-family rows for caster-faith sampling); it preserves the design-intent question for later resolution.

**Cross-genre check** (per gandalf role definition § Tone):
- **D2/D3/D4 + PoE + LE + GD:** mace classifications vary. In D2, maces are EQ'd by Paladin (faith-aligned) but also Barbarian (STR martial). In D4, maces are weapon-type-tag "Mace" used across multiple classes; class-specific weapon-restriction is the gating mechanism, not the weapon's "family." In PoE, maces are STR weapons period (PoE uses attribute requirements on weapons; mace = STR requirement; spell modifiers come from caster weapons like wands/scepters/staves, not maces). In LE, similar to D4 — weapon-type tag with class restriction.
- **Isekai canon:** mace is overwhelmingly a faith-paladin / holy-knight weapon (KonoSuba's Aqua has staff; cleric archetypes typically wield blunt-faith instruments; pure holy-knight hybrids carry mace + holy aura). The mace-as-faith-instrument trope DOES carry across isekai canon — it's not purely D&D-coded.
- **Real-world history:** ecclesiastical maces (mace as bishop's ceremonial regalia; the parliamentary mace; the holy-water sprinkler / "goupillon" / "Holy Water Sprinkler" weapon-flail wielded by warrior-bishops in Crusader-era warfare) ARE historically a faith-class weapon. The substrate is not making this up.

The genre-precise read (III) is supported by all three lenses: there IS a "cleric with mace" canon, but it's a SLICE of caster-faith, not 62%. Path B operationalizes Interpretation III without locking Interpretations I or II prematurely.

---

## 3. Per-option assessment

### 3.1 Path A — Substrate-classifier reclassification

| Dimension | Assessment |
|---|---|
| **Design-intent fidelity** | LOW-MEDIUM. Pre-commits Interpretation II without design call. Strips cleric-with-mace canon from caster-faith entirely. If Interpretation I or III turns out to be correct, this is irreversible without a re-classifier campaign. |
| **Addresses root cause** | PARTIAL. Fixes the OUTPUT (substrate row family tags) but does NOT fix the CLASSIFIER RULE (SC-6 § 2.1's `primary_stat='WIS' → caster-faith` without within-WIS discriminator). Next ingest pass reproduces the bug. To truly fix root cause, the classifier rule must be amended to a within-WIS discriminator (e.g., `WIS + mace_family → martial-heavy; WIS + faith_instrument → caster-faith; WIS + ambiguous → review`). That amendment work IS the actual Path A; elrond's Path A as framed is only the "backfill" half. |
| **Strengths** | Clean substrate vocabulary; aligns weapon_type_family enum with mechanical role; produces sampleable within-family identity beat from substrate as-is. |
| **Weaknesses** | (a) Loses cleric-with-mace canon; (b) requires classifier rule amendment AS WELL AS row reclassification (elrond's framing missed this); (c) caster-faith shrinks 146→~56 rows, leaving a THIN faith-substrate that may not support the within-family identity beat any better than the current state — just thin with diverse shapes instead of dominated by one shape; (d) cross-seam impact is real (rocket main_weapon binding volume; gamora BC measurement on caster-faith subset; gandalf design-intent confirmation; star-lord telemetry refresh). |
| **Cost** | High. Classifier rule amendment (elrond) + row reclassification (~90 rows; elrond) + cross-seam coordination (rocket + gamora + star-lord) + design-call ratification (gandalf + Matt) + MIGRATION.md + roadmap flag. Multi-day. |
| **Reversibility** | Medium. Row reclassification is reversible per `v1_scope_composition_trace` provenance preservation; classifier rule amendment is harder to reverse without re-ingest. |
| **Gandalf-lean** | Defer to Cycle 15 (post-Wave-5 empirical evidence). |

### 3.2 Path B — Runtime within-caster-shape sampling adjustment

| Dimension | Assessment |
|---|---|
| **Design-intent fidelity** | HIGH. Interpretation-agnostic. Operationalizes Interpretation III (dial back mace dominance to ~20-30%) without locking Interpretations I/II. Preserves cleric-with-mace canon as a sometimes-sampled slice. |
| **Addresses root cause** | NO. Symptom-mitigation per elrond audit framing. Substrate stays as-is. Future ingest passes reproduce the underlying mace dominance. |
| **Strengths** | (a) Non-destructive; (b) reversible (sampling weight is a tunable); (c) rocket-only seam touch (matches Fix B's `WITHIN_ATTRIBUTE_FAMILY_WEIGHT` pattern; ships in same dispatch); (d) un-blocks Wave 5 within-family identity-beat collapse without committing to a design-intent resolution; (e) preserves the cleric-with-mace archetype as a recognizable-but-not-dominant pattern. |
| **Weaknesses** | (a) Scaffold-with-pending-decision per Discipline #40 (MIGRATION.md + roadmap flag required); (b) the remaining ~56 non-mace caster-faith rows are heavily weighted to incense_ritual_implement (12 censers/sprinklers/thuribles), which is a NARROW within-family identity beat — the orb/tome/wand/scepter sub-archetypes are absent; (c) Path B doesn't help if the deeper problem (caster-faith staff/scepter/wand sub-archetypes are absent from substrate, not just mace-overshadowed) is real; (d) future substrate consumers (Phase 5 cohesion-judge; Phase 6 visual cohesion) may each need their own within-family adjustment. |
| **Cost** | Low. ~5-10 LOC in `substrate_weapon_binding.py` + a `WITHIN_CASTER_SHAPE_WEIGHT` table + sampling rule. Ships in Wave 2 alongside Fix B. |
| **Reversibility** | High. Sampling weight tunable; revertible per-dispatch. |
| **Gandalf-lean** | FIRE NOW (Wave 2). |

### 3.3 Path C — Substrate library enrichment (legolas Mode B re-crawl)

| Dimension | Assessment |
|---|---|
| **Design-intent fidelity** | HIGH. Addresses the deeper substrate gap (staff/scepter/wand/orb/tome faith-flavor variants are absent; substrate needs ~80-120 non-mace faith-instrument additions). |
| **Addresses root cause** | YES for substrate-thinness root cause (orthogonal to classifier-rule root cause). Path C + Path A classifier-amendment together address both layers. |
| **Strengths** | Expands canonical surface; benefits future consumers; aligns with the Cycle 10 Sidecar B WIS-broad enrichment pattern (already canonical per composition-policy doc § 8.2). |
| **Weaknesses** | Multi-day work; coordination with legolas + jack-ryan Discipline #20 robots.txt verification + Discipline #11 empirical inspection of new rows. Not pre-Wave-5 feasible. |
| **Cost** | Highest. ~1-2 days legolas Mode B + ~half-day elrond schema/curation + design-call ratification. |
| **Gandalf-lean** | Queue for Cycle 15 substrate enrichment cycle alongside the rest of the Sidecar B targets. |

### 3.4 Path B + Path A-queued (HYBRID — my verdict)

| Dimension | Assessment |
|---|---|
| **Design-intent fidelity** | HIGH. Path B is interpretation-agnostic and ships now; Path A is queued for post-Wave-5 empirical-evidence resolution + Matt design call on Interpretations I/II/III. |
| **Addresses root cause** | DEFERS root-cause fix to Cycle 15 with the explicit empirical-criterion gating re-engagement (Wave 5 gauntlet output + Phase 5 cohesion-judge output). Per gandalf OP § 3.4 recognition-validate-commit discipline. |
| **Strengths** | (a) un-blocks Wave 5 at minimum cost; (b) preserves design-intent question for resolution with better evidence; (c) Discipline #40 invocation (MIGRATION.md + roadmap flag) keeps the scaffold visible and prevents drift; (d) composes with Fix B dispatch scope (same pattern, same seam, same Wave 2 ship). |
| **Weaknesses** | Carries scaffold-debt past Wave 5; requires Cycle 15 design call + classifier amendment work; the 8 weeks between Wave 2 ship and Cycle 15 close is a window for downstream consumers to inherit the scaffold-assumption (mitigated by Discipline #40 MIGRATION.md flag). |
| **Cost** | Low-now + Medium-Cycle-15. Wave 2 cost = Path B cost. Cycle 15 cost = Path A cost + Path C cost (if Wave 5 reveals substrate thinness as the load-bearing issue) OR Path A alone (if substrate thinness is acceptable). |

---

## 4. Ranked recommendation (gandalf tier table)

| Tier | Path | Rationale |
|---|---|---|
| **Tier 1 (Wave 2, FIRE-NOW)** | Path B — runtime within-caster-shape sampling adjustment | Un-blocks Wave 5 at minimum cost; interpretation-agnostic; matches Fix B dispatch pattern; rocket-only seam. |
| **Tier 2 (Cycle 15, QUEUED)** | Path A AMENDED — substrate-classifier RULE amendment + row reclassification | Fires AFTER Wave 5 gauntlet evidence + Matt design call on Interpretations I/II/III. Path A as elrond framed it is INCOMPLETE without classifier-rule amendment. |
| **Tier 3 (Cycle 15, QUEUED if Wave 5 reveals substrate thinness)** | Path C — substrate library enrichment via legolas Mode B | Composes with Path A; addresses the orthogonal substrate-thinness root cause. Already canonical per composition-policy doc § 8.2 Sidecar B WIS-broad enrichment. |
| **Reserve** | Pure Path A (no Path B) | REJECTED for Wave 2 — pre-commits Interpretation II without design call; strips cleric-with-mace canon irreversibly. |
| **Reject** | No remediation | REJECTED — Wave 5 gauntlet output would inherit the within-family identity-beat collapse and produce misleading cohesion signal at Phase 5. |

---

## 5. Cross-seam routing recommendation for KR

### 5.1 Wave 2 (FIRE-NOW per HYBRID Tier 1)

**Path B implementation scope:**

- **Owner:** rocket (substrate_weapon_binding.py)
- **Pattern:** identical to Fix B (`WITHIN_ATTRIBUTE_FAMILY_WEIGHT` table)
- **New scope:** add `WITHIN_CASTER_SHAPE_WEIGHT` table + sampling rule within caster-faith
- **Math note:** Discipline #1 — gandalf authors weight ratios in math-note form
  - Suggested ratios (gandalf design call):
    - mace_hammer_family: **0.25** (dial back from 0.62 natural → ~0.20-0.25 effective; preserves cleric-with-mace as sometimes-sampled archetype)
    - sacred_symbol_or_ritual_item: **0.25** (boost from 0.09 → ~0.25; crucifix/rosary/vajra get presence)
    - incense_ritual_implement: **0.25** (boost from 0.08 → ~0.25; censer/sprinkler/thurible get presence)
    - staff_scepter_rod: **0.15** (boost from 0.04 → ~0.15; faith-staff sub-archetype emerges; pairs with caster-arcane staff dominance for cross-family variety)
    - other: **0.10** (mostly noise; downweight)
  - These ratios are GUIDANCE for rocket; final ratios subject to rocket sim-viability check + gandalf design review
- **Cross-seam:**
  - **rocket:** implementation + math note + sim-viability
  - **jack-ryan:** Gate-1 review (Discipline #1 math-before-code + Discipline #11 empirical-inspection on sampling output)
  - **gamora:** consumes resulting weapon shape; no BC measurement refresh needed (substrate stays as-is)
  - **elrond:** consult only; no substrate modification
  - **gandalf:** sign-off on weight ratios; sign-off on Discipline #40 scaffold-with-pending-decision MIGRATION.md
- **Discipline #40 obligation:** MIGRATION.md entry at Wave 2 commit naming:
  - Scaffold: runtime caster-faith mace-suppression via `WITHIN_CASTER_SHAPE_WEIGHT`
  - Pending decision: substrate classifier amendment (Path A) — Interpretation I/II/III resolution
  - Empirical-criterion gate: Wave 5 gauntlet output + Phase 5 cohesion-judge output
  - Roadmap entry: Cycle 15 "caster-faith substrate classifier resolution"

**KR dispatch routing:**

- **Compose with Fix B dispatch** — same seam (rocket), same pattern (`WITHIN_*_WEIGHT` table + sampling rule), same Wave 2 ship. Author as ONE dispatch covering Fix B (STR cross-attribute) + Fix B-prime (WIS within-caster-shape). Reduces dispatch overhead + critique-pair load.
- **Gate-1 with jack-ryan** — both fixes; same gate.
- **Composition with Fix A** — Fix A (hygiene filter) is already independent + landed; Fix B + B-prime ride post-Fix-A footprint.

### 5.2 Cycle 15 (QUEUED per HYBRID Tier 2 + Tier 3)

**Empirical-evidence criterion gating Cycle 15 re-engagement** (per gandalf OP § 3.4):

1. **Wave 5 gauntlet output landed** — per-character JSON sample includes caster-faith characters; visual + mechanical identity-beat assessable.
2. **Phase 5 cohesion-judge output landed** — cohesion narrative across caster-faith characters surfaces whether the within-family identity beat reads as coherent or as collapsed.
3. **Matt design call on Interpretations I/II/III** — locks design-intent for mace-as-faith-weapon question (genre-precise read per § 2 above is gandalf's lean; Matt confirms).

When ALL three criteria resolve:

- **Path A** (classifier-rule amendment + row reclassification per amended rule): elrond execution; cross-seam coordination per elrond audit § 4.
- **Path C** (Sidecar B WIS-broad enrichment for orb/tome/wand/scepter faith sub-archetypes): legolas Mode B; composes with existing canonical scope per composition-policy doc § 8.2.

**Cycle 15 dispatch scope (preview, not authored yet):**
- elrond classifier-rule amendment dispatch (within-WIS discriminator)
- elrond row reclassification dispatch (~90 mace rows → martial-heavy/light per amended rule)
- legolas Mode B WIS-broad enrichment dispatch (~80-120 non-mace faith-instrument rows)
- gamora BC measurement refresh on caster-faith subset
- gandalf canonical doc amendment to attribute-system § 1.3 / § 3 (resolve internal tension)
- star-lord telemetry refresh for caster-faith family

---

## 6. Pre-Wave-5 sequencing

| Item | Wave | Owner | Status |
|---|---|---|---|
| Fix A (hygiene filter) | Wave 1.5 (already in-flight) | rocket | LANDED (per consolidated doc § 4) |
| Fix B (STR cross-attribute sampling) | Wave 2 | rocket | DISPATCH PENDING (Fix C audit just landed; this verdict consumed by KR) |
| **Fix B-prime (WIS within-caster-shape sampling — Path B)** | **Wave 2** | **rocket** | **THIS VERDICT — recommended HYBRID Tier 1 to ship in Fix B dispatch** |
| Wave 5 gauntlet sim | Wave 5 | gamora | PENDING; empirical-evidence gate for Cycle 15 re-engagement |
| Phase 5 cohesion-judge | Wave 5 / Cycle 15 boundary | star-lord + gamora | PENDING; empirical-evidence gate |
| Path A classifier amendment + reclassification | Cycle 15 | elrond + gandalf + Matt | QUEUED per Tier 2 |
| Path C substrate enrichment | Cycle 15 | legolas + elrond | QUEUED per Tier 3 |

Wave 2 dispatch compose Fix B + Fix B-prime ships as ONE dispatch (rocket-only seam; same pattern). Gate-1 ratification fires once for both.

---

## 7. Composition with Cycle 14 disciplines

### 7.1 Discipline #40 (load-bearing — gandalf prior canonical write per consolidated doc § 4)

**Invocation:** Path B IS a scaffold-with-pending-decision. Per Discipline #40, the Wave 2 commit MUST carry:

- MIGRATION.md entry at `~/Games/reincarnated-engine/MIGRATION.md` (rocket seam):
  - **What is the scaffold?** `WITHIN_CASTER_SHAPE_WEIGHT` table in `substrate_weapon_binding.py` under-weights mace-family rows when sampling caster-faith main_weapon.
  - **What is the pending decision?** Substrate-side resolution of caster-faith mace dominance via classifier amendment (Path A) + optional substrate enrichment (Path C).
  - **What is the empirical-criterion that gates re-engagement?** Wave 5 gauntlet output + Phase 5 cohesion-judge output + Matt design call on Interpretation I/II/III.
  - **Where is the resolution queued?** Cycle 15 (caster-faith substrate classifier resolution workstream).
- Roadmap entry at `canonical/02-roadmap.md` Cycle 15 queue:
  - "Caster-faith substrate classifier resolution — Path A (classifier rule amendment + row reclassification) + Path C (Sidecar B WIS-broad enrichment); gated on Wave 5 + Phase 5 empirical evidence + Matt design call on Interpretations I/II/III per gandalf verdict 2026-05-27."

### 7.2 Discipline #11 (empirical inspection over assumption)

**Invocation:** elrond's Fix C audit IS the empirical evidence. The audit's SQL queries are reproducible from `~/Games/reincarnated-loadout/data/telemetry.db`. The 62% mace dominance is not an assumption — it's a count.

This verdict carries the empirical evidence forward into the Wave 2 dispatch + Cycle 15 queue. The audit is canon for the duration; if substrate state changes (Path A or Path C lands), the audit re-runs.

### 7.3 Discipline #18 (methodology-before-execution)

**Invocation:** design call BEFORE Wave 2 implementation — this verdict IS the design call output. Path B implementation does NOT fire until:

- KR ratifies this verdict + integrates into Fix B dispatch scope
- jack-ryan Gate-1 reviews Fix B + Fix B-prime dispatch
- Matt sign-off on Wave 2 dispatch fire

The methodology-consultation for Path B (within-family sampling weights) IS this verdict's § 5.1 weight-ratio suggestions. Rocket consumes; rocket may amend per sim-viability + design-side review.

### 7.4 Discipline #25 (semantic-layer rep-audit — per gandalf OP § 4.4 candidate)

**Invocation:** the caster-faith cluster's semantic identity ("WIS faith-caster") is the cultural-tradition substrate Phase 5 cohesion-judge inherits. Rep-audit at firing per OP § 4.4:

- Pull top-N caster-faith reps post-Fix-B-prime sampling
- Verify reps match the semantic interpretation downstream consumes (faith-caster identity beat — censer + mace + ritual-implement + holy-symbol)
- If reps still over-represent mace family (sampling didn't dial back enough), iterate weights
- If reps surface unexpected rows (Mode B/C/D artifacts per OP § 4.4), flag for Path A amendment

The rep-audit obligation rides on Wave 2 + Wave 5 + Phase 5 — three checkpoints.

---

## 8. Out-of-scope notes (per OP § 2 Pattern A-deep discipline)

This verdict does NOT:

- **Amend canonical docs.** The internal tension in attribute-system doc § 1.3 vs § 3 on mace-as-WIS-vs-STR is flagged (§ 2 above) but NOT resolved here. If verdict adoption requires canonical amendment, KR fires separate canonical-amendment dispatch — likely Cycle 15 scope as part of Path A resolution.
- **Touch substrate library DB.** Substrate stays as-is for Path B (per HYBRID Tier 1). Cycle 15 Path A execution is elrond's seam.
- **Touch substrate_weapon_binding.py.** Implementation is rocket's seam (per HYBRID Tier 1). Wave 2 dispatch fires the implementation.
- **Delay Wave 1.5 Stage 1 elrond audit firing.** Different scope; in parallel.
- **Pre-commit to weight ratios.** § 5.1 weight-ratio suggestions are GUIDANCE; rocket sim-viability + gandalf review at Wave 2 implementation locks final values.

---

## 9. Framing-audit checklist (per gandalf OP § 4.1 — applied to THIS verdict)

| Q | Answer |
|---|---|
| **Q1 — Load-bearing framing assumptions** | (a) elrond's Fix C audit is empirically correct (62% mace dominance is reproducible from DB); (b) within-family identity beat IS load-bearing for Wave 5 character coherence; (c) Interpretation III (genre-precise: ceremonial-mace = faith, battle-mace = martial) is the most faithful read; (d) Wave 5 gauntlet output will surface whether within-family identity beat is actually load-bearing in practice or whether it's downstream-invisible. |
| **Q2 — Refutation evidence in current scope** | (a) elrond audit queries reproducible at any time; (b) attribute-system § 1.3 / § 3 internal tension surfaces unilaterally; (c) doc 47 § 3.1 expectation for WIS = "focus / tome / talisman / channeling staff / holy symbol" is explicit (mace NOT listed) — suggests doc 47 author (gandalf) already implicitly endorsed Interpretation II; (d) Wave 5 gauntlet has not run; the assumption that within-family identity beat is load-bearing at Wave 5 is NOT yet empirically validated — could be a subordinate concern relative to bigger Wave 5 cohesion issues. |
| **Q3 — Refine framing rather than execute?** | NO refinement needed for HYBRID Tier 1 (Path B). HYBRID Tier 2 (Path A) IS the empirical-evidence-deferral that the framing-audit produces. The verdict's HYBRID structure operationalizes Q3 correctly — fire what's interpretation-agnostic now; defer interpretation-locking to empirical evidence + design call. |

**Refutation surface flagged:** doc 47 § 3.1 explicitly excludes mace from the WIS weapon profile list ("focus / tome / talisman / channeling staff / holy symbol"). This is gandalf's own prior canonical write. Reconciling doc 47 § 3.1 against attribute-system § 1.3 (which DOES list mace under WIS class archetypes' weapon families) is a canonical-amendment task for Cycle 15 design call. I flag this NOW so KR can include it in the Cycle 15 queue alongside Path A.

---

## 10. Sign-off

**Verdict:** HYBRID — Path B (within-caster-shape sampling adjustment) fires Wave 2 alongside Fix B; Path A (classifier amendment + row reclassification) queued for Cycle 15 gated on Wave 5 + Phase 5 + Matt design call empirical evidence; Path C (Sidecar B substrate enrichment) queued for Cycle 15 composes with Path A if Wave 5 reveals substrate thinness as load-bearing.

**Discipline invocations:**
- Discipline #40 (scaffold-with-pending-decision): MIGRATION.md + roadmap flag at Wave 2 commit.
- Discipline #11 (empirical inspection): elrond Fix C audit is the empirical anchor.
- Discipline #18 (methodology-before-execution): THIS verdict IS the design call output; Path B implementation does NOT fire until KR + jack-ryan + Matt gate.
- Discipline #25 candidate (semantic-layer rep-audit): rep-audit obligation at Wave 2 + Wave 5 + Phase 5.

**Cross-seam routing for KR:**
- **Wave 2 (NOW):** compose Fix B + Fix B-prime as ONE rocket dispatch; Gate-1 with jack-ryan; Matt sign-off; fire.
- **Cycle 15 (QUEUED):** elrond classifier amendment + row reclassification + legolas Mode B substrate enrichment + canonical doc amendment (attribute-system § 1.3 / § 3 reconciliation + doc 47 § 3.1 cross-check); gated on Wave 5 + Phase 5 empirical evidence + Matt design call on Interpretations I/II/III.

**Out-of-scope deferrals:**
- Canonical doc amendments (KR fires separate dispatch if/when needed).
- Substrate DB modification (Cycle 15; elrond seam).
- substrate_weapon_binding.py modification (Wave 2; rocket seam).

**Anchor docs cited:** elrond Fix C audit; elrond SC-6 audit § 2.1; doc 47 § 3.1; weapon-substrate-composition-policy-v1 § 3.2; attribute-system § 1.3 + § 3; scaffold-drift recognition + Discipline #40; substrate-weapon-family-balance-sidecar-request.

---

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27
**Pattern:** Pattern A-deep design-fit verdict per gandalf OP § 2; hive-mind sub-agent verdict pattern per hive-mind-protocol skill § 5.5.
**Signed:** gandalf
