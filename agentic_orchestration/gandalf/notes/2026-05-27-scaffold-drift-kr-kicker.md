# Scaffold-Drift Corrective Package — Knight-Rider Kicker

> **STATUS:** CURRENT — orchestration signal for knight-rider to consume the consolidated scaffold-drift package and package three dispatches per § 5 routing.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27
**Recipient:** knight-rider (Cycle 14 hive-mind cycle orchestrator)
**Authority:** Matt 2026-05-27 — (a) three-fix substrate recommendation ratified inline; (b) recognition that 16-character cohort + 12-skill 3-chain grid are real drift cases (not false patterns); (c) "author all three as one consolidated document" directive
**Source doc:** `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` (685 lines)
**Position relative to current hive state:** mid-cycle intervention — does NOT displace Wave 1 in-flight; INSERTS Wave 1.5 BEFORE Wave 2; gates Wave 5 production gauntlet per § 5.3 prerequisite assertion

---

## 0. TL;DR

Three scaffold-drift cases surfaced 2026-05-27 (substrate weapon family imbalance + 16-character cohort drift + 12-skill 3-chain grid drift). Consolidated recognition + corrective package authored. KR packages THREE dispatches per the consolidated doc § 5.2, surfaces ONE Matt-ratification gating question (class-roster sub-decision § 3.5 Option C), and enforces the pre-Wave-5-gauntlet prerequisite assertion (§ 5.3).

---

## 1. Read this first

**`agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md`** in full. Section map:

| § | Content |
|---|---|
| 0 | TL;DR — three drift cases + meta-corrective |
| 1 | Recognition — scaffold-drift meta-pattern; three concrete instances; why Wave 5 is the deadline |
| 2 | Corrective Part 1 — Substrate sidecar (Fix A hygiene + Fix B STR rebalancing + Fix C caster kind audit) |
| 3 | Corrective Part 2 — Wave 1.5 Skill-Tree Architecture + Season Cardinality canonical decision |
| 4 | Corrective Part 3 — Discipline #40 candidate (scaffold-values-require-canonical-decision) |
| 5 | Sequencing + Routing — three dispatches; pre-Wave-5-gauntlet prerequisite |
| 6 | Cross-references |
| 7 | Sign-off |

---

## 2. Three dispatches to package

### Dispatch 1 — Substrate sidecar (Part 1)

**Title:** `2026-05-27-substrate-weapon-family-balance-sidecar.md` (or KR's preferred naming)
**Authority:** Matt 2026-05-27 ratified three-fix recommendation
**Items:**

1. **Fix A — Hygiene filter** (rocket; small; folds into Wave 1 closure window OR small follow-on)
   - Add `wke.weapon_kind IN ('category', 'named_template', 'unique')` to substrate query
   - Eliminates 185 ammo/off-hand contamination rows
   - Module-load assertion verifies count
2. **Fix B — Within-STR family rebalancing** (rocket; Wave 2 candidate; math-note required NOW)
   - 70/30 martial-heavy/ranged for STR; 60/40 ranged/martial-light for DEX
   - Add `WITHIN_ATTRIBUTE_FAMILY_WEIGHT` table per consolidated doc § 2.3
   - Math note: `within-attribute-family-weight-math.md` (Discipline #1)
3. **Fix C — Caster weapon_kind variety audit** (elrond; non-gating; fire anytime)
   - SQL audit per consolidated doc § 2.4
   - Output at `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md`
   - gandalf design-call follow-on only if remediation needed

**Critique-pair:** jack-ryan Gate-1 reviews dispatch; Gate-2 on each fix per closure
**Wave-entry-fire-discipline applies:** after dispatch authoring + commit, KR INVOKES sub-agents via Agent tool — not just drafts and waits

### Dispatch 2 — Wave 1.5 Skill-Tree Architecture (Part 2)

**Title:** `2026-05-27-rocket-cycle-14-wave-1-5-skill-tree-architecture.md` (or KR's preferred naming)
**Position:** INSERTS BEFORE Wave 2 (currently next-in-queue)
**Authority:** Matt 2026-05-27 ratified recognition that 12-skill 3-chain grid is real drift; KR packages dispatch
**Estimated effort:** ~1 week anchor (per framing brief Q10 quality > timeline)
**Owner:** rocket (primary implementer); gandalf design-call partner; jack-ryan Gate-1 + Gate-2
**Scope (5 items per consolidated doc § 3.3):**

1. Per-class chain count (3 or 4) sampled from class metadata
2. T4 count = chain_count − 1 rule (D83)
3. Supporting chain (T3-cap, class-intrinsic; Option C per doc 40 § 6.6.1)
4. Depth-≥4 branching (D69 wide-vs-tall lever)
5. ONE T4 unlocked at a time (D66 active identity discipline; runtime-active marker)

**Math notes required (Discipline #1; 3 notes):**
- `wave-1-5-class-chain-architecture-math.md`
- `wave-1-5-branching-math.md`
- `wave-1-5-active-t4-runtime-math.md`

**Season cardinality canonical decision bundled (§ 3.4):**
- Default `n_kits=40` (within multi-fire extension's 50-cap)
- gandalf authors doc 41 § 4 amendment as part of Wave 1.5 close
- Rocket implements n_kits=40 default

**CRITICAL GATING QUESTION FOR MATT BEFORE DISPATCH FIRES** (consolidated doc § 3.5):
The class-roster sub-decision MUST resolve before KR drafts Wave 1.5. Three options per the consolidated doc:

| Option | Approach | Trade-off |
|---|---|---|
| A | Use Cycle 13 16-archetype list as v1 class roster | Fast; biased by gauntlet-test cohort selection |
| B | gandalf authors first-pass class roster (3-4 weeks design call) | Slow; canonical-quality |
| **C** | **Substrate-evidence audit (elrond) → gandalf design call** | **Substrate-led; defensible — gandalf-recommended** |

**KR action:** SURFACE this to Matt explicitly. Do NOT draft Wave 1.5 dispatch until Matt ratifies Option A/B/C. The dispatch shape depends on the answer.

**Cross-seam impact** (must be in dispatch):
- gamora damage_resolver consumes `active_t4_chain` field; MIGRATION.md entry required
- star-lord Track C transform: character JSON shape adds `active_t4_chain` + `supporting_chain` fields
- elrond: if Option C, runs the substrate class-roster audit as Wave 1.5 prerequisite
- drax: loadout app skill-tree rendering needs updating (supporting chain visually distinct; branch points renderable; active T4 marker visible)

**Critique-pair:** jack-ryan Gate-1 reviews dispatch; Gate-2 at wave close
**Wave-entry-fire-discipline applies**

### Dispatch 3 — Discipline #40 ratification (Part 3)

**Title:** `2026-05-27-jack-ryan-discipline-40-scaffold-values-canonical.md` (or KR's preferred naming)
**Authority:** Matt 2026-05-27 ratified the recognition; jack-ryan ratifies the discipline-form
**Owner:** jack-ryan (engineering-disciplines.md is jack-ryan's territory)
**Scope:**

- Author Discipline #40 entry per consolidated doc § 4.1-4.4
- Operational hooks per § 4.3:
  - Dispatch authoring (KR): out-of-scope section enumerates scaffold values
  - Gate-2 review (jack-ryan): scaffold-flag verification added to checklist
  - Wave close (KR): MIGRATION.md scaffold-status enumeration
  - Roadmap update (KR): ⚠ visual flag for scaffold-pending items
- Cross-references to disciplines #11, #13, #18, #39 per § 4.4
- Sequencing: parallel to KR Wave 1.5; non-gating Cycle 14 substantive work

**Critique-pair:** N/A (jack-ryan is the canonical-write author; KR reviews for cross-cutting impact)

---

## 3. Sequencing summary

```
NOW                                                                 Wave 5
 │                                                                    │
 ├─ Dispatch 1 (substrate sidecar)                                    │
 │    ├─ Fix A: Wave 1 closure window OR small follow-on (rocket)     │
 │    ├─ Fix B: math-note NOW; impl Wave 2 (rocket)                   │
 │    └─ Fix C: audit anytime (elrond)                                │
 │                                                                    │
 ├─ Dispatch 3 (Discipline #40)                                       │
 │    └─ jack-ryan canonical-write (parallel; non-gating)             │
 │                                                                    │
 ├─ ⚠ MATT GATE: class-roster sub-decision § 3.5 Option A/B/C         │
 │    └─ KR surfaces; awaits Matt ratification                        │
 │                                                                    │
 ├─ Dispatch 2 (Wave 1.5 Skill-Tree Architecture)                     │
 │    └─ rocket ~1 week; gates on Matt gate above                     │
 │                                                                    │
 ├─ Wave 2 (Layers 5+8+9) — CURRENTLY NEXT — DELAYED until Wave 1.5   │
 │                                                                    │
 ├─ Wave 3 (Phase 5 cohesion-judge LLM)                               │
 │                                                                    │
 ├─ Wave 4 (T4-attuned gear cohesion)                                 │
 │                                                                    │
 └─ Wave 5 (production gauntlet) — PRE-FIRE CHECKLIST:                ◀┤
       [ ] Fix A landed                                                │
       [ ] Fix B landed                                                │
       [ ] Wave 1.5 landed (chain count + supporting + branching + T4) │
       [ ] Season cardinality ratified (n_kits=40)                     │
       [ ] Discipline #40 canonical-write landed                       │
       (Fix C non-gating — audit-first, remediation only if needed)    │
```

---

## 4. Roadmap update obligation

Per KR OP § 4 step 4 roadmap-update discipline (Matt 2026-05-27 amendment): `canonical/02-roadmap.md` § 3 status icons require update for:

- New entry: **Wave 1.5 Skill-Tree Architecture** (⏳ status, inserted between Wave 1 and Wave 2)
- New entry: **Substrate sidecar** (⏳ status, parallel to Wave 1)
- New entry: **Discipline #40 ratification** (⏳ status, parallel; jack-ryan)
- Update: **Season cardinality** as scaffold-pending → ratification-pending-via-Wave-1.5 close
- Update: **Wave 2** estimated-fire-date pushed back by Wave 1.5 duration

KR updates roadmap at this kicker's intake (initial entry) AND at each wave-close per the discipline.

---

## 5. Hive-mind protocol composition

- **§ 2.2.2 wave-entry-fire-discipline** applies to all three dispatches: KR drafts + commits + pushes AND THEN invokes sub-agents via Agent tool. No hand-off-by-dispatch-authoring-only.
- **§ 4 decision-routing**: KR has full autonomous scope on dispatch authoring per scope-doc § 4.1; the ONE Matt gate is the class-roster sub-decision in Dispatch 2 — KR surfaces this and waits.
- **Critique-pair**: jack-ryan Gate-1 reviews each dispatch before sub-agent fire; Gate-2 at wave close.

---

## 6. What's externally-gated (Matt action required)

| Gate | Resolution path |
|---|---|
| **Class-roster sub-decision** (Wave 1.5 § 3.5) | KR surfaces options A/B/C; Matt ratifies; gandalf-recommends Option C |
| Season cardinality default n_kits=40 | gandalf-recommends; Matt confirms or amends as part of Wave 1.5 close |

No other Matt gates in this corrective package.

---

## 7. What's NOT in scope of this kicker

- Wave 1 in-flight work (rocket implementation continues per existing dispatch); this kicker does NOT pause Wave 1
- Wave 0.5 follow-on (already complete at engine `685dafa`)
- SC-6b enrichment (already complete at `3c95883`)
- Discipline #33-#39 (already ratified at `d148808`)
- The Path A substrate weapon L50 baseline architecture (already ratified at `e0ebd33` / `f053281`)

This kicker EXTENDS the active Cycle 14 hive session with three new dispatches + one Matt gate — it does not restart, displace, or re-scope existing work.

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — KR kicker for scaffold-drift corrective package consumption; three dispatches to package; one Matt gate to surface; pre-Wave-5-gauntlet prerequisite assertion enforced
**Composition:** with `2026-05-27-scaffold-drift-recognition-and-corrective-package.md` (source) + Cycle 14 framing brief Q10 (quality > timeline supports Wave 1.5 insertion) + KR OP § 3.10 (wave-entry-fire-discipline) + KR OP § 4 step 4 (roadmap-update discipline) + hive-mind-protocol § 2.2.2 + § 4

**For:** the consumption of the consolidated scaffold-drift recognition + three-part corrective package. KR packages three dispatches (substrate sidecar; Wave 1.5 skill-tree architecture; Discipline #40 ratification), surfaces ONE Matt gate (class-roster sub-decision § 3.5 Option C recommended), enforces pre-Wave-5-gauntlet prerequisite assertion (§ 5.3), and updates roadmap per KR OP § 4 step 4 roadmap-update discipline. Wave-entry-fire-discipline applies to all three dispatch firings. Wave 1 in-flight work continues unaffected.

**Signed:** gandalf (story-and-design steward)
