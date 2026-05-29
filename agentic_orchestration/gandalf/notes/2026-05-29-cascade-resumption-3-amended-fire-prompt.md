# Cascade-Resumption-3 AMENDED — KR Fire Prompt (S7 Addition: Substrate Multi-Sample + Lineage/Period Propagation)

> **STATUS:** CURRENT (operational artifact as of 2026-05-29 evening) — paste-ready prompt Matt sends to NEW KR session for cascade-resumption-3 AMENDED with S7 insertion BEFORE S2. **Supersedes the prior cascade-resumption-3 fire prompt** at `2026-05-29-cascade-resumption-3-fire-prompt.md`. The prior KR session that received the unamended fire prompt should be HALTED (close session); this prompt fires a fresh KR session.

**Date:** 2026-05-29 evening
**Author:** gandalf (story-and-design steward)
**Status:** OPERATIONAL — paste-ready
**Authority:** Matt 2026-05-29 evening: "halt KR session and amend authorization" (in response to gandalf S0 empirical verification finding: substrate IS wired at Phase 2 but 1:1 binding + lineage/period fields not in SELECT query → S7 work needed BEFORE S2 gauntlet mechanical cycling)

---

## 0. How to use this artifact

1. Halt the existing KR session that received the prior unamended cascade-resumption-3 fire prompt (close the Claude Code session window cleanly; KR exits gracefully)
2. Launch new `claude --agent knight-rider` session
3. Copy the prompt below (between `---PROMPT BEGINS---` and `---PROMPT ENDS---` markers)
4. Paste as first message to the new KR session

KR onboards via required first reads + drives Steps S1 → S7 → S2 → S3 → S5 → S6 → A2-1 RE-FIRE-3 → cascade A2-2 → A2-7 + D13 parallel.

---

## ---PROMPT BEGINS---

```
KR — Phase A2 cascade-resumption-3 AMENDED entry. The prior
cascade-resumption-3 fire prompt has been SUPERSEDED with this
amended version — S7 (NEW) inserted BEFORE S2 per gandalf S0
empirical verification finding.

OPTIMIZATION TARGET: Matt re-engages ONLY at the hard-surface
conditions enumerated in this prompt + at A2-7 v1 tag ratification
(cascade-complete final surface).

S0 EMPIRICAL FINDING (gandalf 2026-05-29 evening, in-thread):
Substrate weapon library IS wired at Phase 2 BC discovery per
substrate_weapon_binding.py:716 call. All 18 empirical kits have
populated substrate_weapon_binding dicts (Lance head / Sword /
Mjölnir / Whip / Wurrog Staff / Khakkhara / etc.). BUT:
(1) 1:1 binding (1 substrate weapon per BC cell; rng.choice() over
    qualifying rows; 18 cells → 18 substrate weapons)
(2) cultural_lineage_canonical + historical_period_canonical +
    register_canonical + cultural_lineage_confidence +
    named_mythological_match fields EXIST on weapon_knowledge_entries
    schema (14-enum + 9-enum + 6-enum + REAL + TEXT) but are NOT in
    the SELECT query at substrate_weapon_binding.py:316
(3) weapon_type_family empirically collapses to 4 attribute-keyed
    buckets (martial-heavy / ranged / caster-arcane / caster-faith)
    across 18 kits — no diverse-family spread

S7 (NEW) wires the missing lineage/period/register fields AND adds
multi-sample substrate selection (N=3-5 samples per BC cell).
~1-2d engineering. Inserted BEFORE S2 so gauntlet mechanical cycling
operates on substrate-diverse base.

REQUIRED FIRST READS IN ORDER (read all eight before any dispatch):

1. agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md
   — AUTHORITATIVE authorization with AMENDMENT 1 header + § 2.5 NEW
   S7 specification + per-substream effort table + acceptance criteria
   + pre-ratified contingent decisions + surface-to-Matt edge cases.
   Read this FIRST.

2. agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md
   — Matt 2026-05-27 verbatim recommitment; S1 IS the operational
   application

3. canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md
   — recognition record; § 0.1 Amendment 2 (root-cause catalog finding)

4. agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md
   — Instance 6 + root-cause sub-case (catalog level)

5. agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md
   — Concern #3 P3c routing (LANDED in cascade-resumption-2);
   carry-forward pre-ratifications PRESERVED

6. agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md
   — original Phase A2 resolution plan + § 1.5 D13 parallel-fire

7. canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md
   — § 4 Wave A + § 5 Wave B + § 6 F-C prompts + § 0.1 Amendment 1
   (S4 audit) + § 2.5 substrate-input purity precondition

8. agentic_orchestration/cycle-14-hive-mind-state.md — live state file

CASCADE-RESUMPTION-3 AMENDED WORK PROGRAM (R48.4 strict single-seam;
S7 inserted before S2):

Stream S1 — Class-concept eradication at substrate-input layer
  Owner: rocket (primary)
  Effort: ~1-2d
  Scope: strip class taxonomy from endgame_encounter_catalog.py +
         downstream surfaces
  Preserve: cohort_archetype + BC tuple + T4 Capstone architecture
  Acceptance: zero class-name strings remaining in catalog

Stream S7 (NEW) — Phase 2 multi-sample substrate consumption +
  lineage/period propagation
  Owner: rocket + elrond consultation on substrate library schema
  Effort: ~1-2d
  Dependency: S1
  Scope (per authorization § 2.5):
    - Extend SQL query at substrate_weapon_binding.py:316 to also
      SELECT cultural_lineage_canonical, historical_period_canonical,
      register_canonical, cultural_lineage_confidence,
      named_mythological_match
    - Extend _build_weapon_binding() to include new fields in
      substrate_binding dict (11+ fields)
    - Refactor select_and_bind_substrate_weapon() to support
      multi-sample selection (default N=3 per BC cell)
    - Refactor w5r1_generate_kit_candidates() to generate N kits per
      BC cell from N substrate samples (was: 1 kit per BC cell)
    - Propagate lineage/period/register to kit top-level for
      downstream Phase 3 PM-1 + Phase 5 Wave A consumption
    - Update Phase 3 PM-1 input to consume new lineage/period/register
      fields as multimodal vector axes
    - Phase 5 Wave A modal_cultural_lineage now sources from kit
      lineage aggregates (not placeholder)
  Acceptance:
    - substrate_binding dict carries 11+ fields
    - Phase 2 generates N kits per BC cell (N=3 default) → 54+ kits
    - ≥5 distinct cultural_lineage_canonical values season-wide
    - ≥5 distinct weapon_type_family values season-wide
    - Phase 5 Wave A modal_cultural_lineage sources from kit aggregates
  Pre-ratified contingent decisions (KR routes WITHOUT re-asking):
    - N=3 default; KR can elect N=5 if substrate density supports per
      elrond consultation; surface only if N=10+ OR substrate density
      issues
    - Substrate library SELECT extension: 5 new fields per scope
      table; surface if schema gaps surface beyond these 5
    - Multi-sample selection method: seeded rng without replacement
      (simple)
    - Lineage/period field placement: kit top-level (not just
      substrate_binding)

Stream S2 — Gauntlet variant enumeration expansion
  Owner: rocket + gamora
  Effort: ~1-2d
  Dependency: S7 (was S1 pre-amendment)
  Scope: cycle T4 strategy variants (6 Layer 2 strategies per doc 47
         § 4.6) + investment scaling profiles (low/mid/max per doc 51
         Patterns 1+2) + optional skill tree variants
  Goal: build mechanical variants on top of substrate-diverse Phase 2
        base (54+ kits → 100-300+ post-S2 mechanical variants)
  Acceptance: ≥22 unique kit-variant rows in gauntlet output (likely
        much higher post-S7)

Stream S3 — Phase 4 archive variant preservation
  Owner: rocket
  Effort: ~0.5-1d
  Dependency: S2
  Scope: change kit_archive insertion to preserve variant tuples as
         distinct rows; PM-1 input consumes variant population

Stream S4 — Phase 5 LLM prompt audit ✅ COMPLETE 2026-05-29 in-thread
  per commit 13822ba; canonical doc § 0.1 Amendment 1 + § 2.5 +
  W-A10 / W-B8 / F-C13 runtime substrate-purity grep acceptance
  criteria all landed.

Stream S5 — Wave B FULL implementation per canonical § 5
  Owner: star-lord (primary) + rocket (integration)
  Effort: ~1-1.5d
  Dependency: S3 + S4 (S4 done) + S7 propagation chain
  Scope: implement run_wave_b_async() per canonical § 5 spec +
         Phase5WaveBResult dataclass + per-kit prompt execution +
         integrate Wave B in wave5_season_orchestrator.py Phase 5
         hook + persist to kit_archive.cohesion_data (unhardcode {})
         + wire Phase 7 cohesion-judge gate consumption

Stream S6 — Integration + jack-ryan Gate-2 + A2-1 RE-FIRE-3
  Owner: rocket + gamora + star-lord + jack-ryan
  Effort: ~1-1.5d
  Dependency: S1-S7-S2-S3-S5 all closed (S4 already done)
  Scope: smoke test + Disc #11 audit + jack-ryan Gate-2 (Pattern E
         pre-auth) + A2-1 RE-FIRE-3 full season_001 production
  Acceptance:
    - A2-1 RE-FIRE-3 ≥12/18 shipped_worthy (or higher if N>1 kits
      per BC cell post-S7 changes the shipping threshold)
    - PM-1 produces ≥4-6 emergent clusters (NOT k=3 fallback
      degenerate)
    - Wave A faction labels grounded in real cultural_lineage values
    - Wave B per-kit identities populated with substrate-anchored
      cultural/period vocabulary

REALISTIC TOTAL TO A2-1 RE-FIRE-3 PASS: ~7-12 days
(was ~6-10d pre-S7-amendment; S7 adds ~1-2d)

Cascade through A2-2 → A2-7 + D13 parallel-fire per existing
Phase A2 sequence AFTER A2-1 RE-FIRE-3 PASS.

LOCKED AUTHORIZATIONS (Matt-ratified across prior sessions; ALL
carry forward to this session):

- GATE (a) Phase A1 closure record RATIFIED as-is
- GATE (b) $50 SOFT CAP for total Wave 5 cascade LLM spend
- GATE (c) A2-1 through A2-7 sequence CONFIRMED + D13 parallel-fire
  RATIFIED
- PUSH per-workstream pattern
- PATTERN E PRE-AUTHORIZATION for all Wave 5 Gate-2 reviews
- CONCERN #3 PRE-RATIFIED P3c routing (LANDED)
- CASCADE-RESUMPTION-3 PRE-RATIFIED contingent decisions
- S7 PRE-RATIFIED contingent decisions per authorization § 2.5

OPERATIONAL CONSTRAINTS (ACTIVE throughout):

- Discipline #48 R48.4 single-seam
- Discipline #42a framing-audit at every dispatch consumption gate
- Discipline #43 design-quality audit at each Gate-2 review
- Discipline #41 substrate-led vocabulary lock (LOAD-BEARING for S1)
- Discipline #45 vocabulary lock
- Discipline #11 empirical inspection
- Discipline #18 math hotspot consultation
- Auto-commit per CLAUDE.md addendum 2026-05-25

SURFACE TO MATT AT (and ONLY at):

- S1 audit surfaces class taxonomy in unexpected engine surfaces
- S7 substrate library schema gap surfaces (cultural_lineage missing
  OR sparse across attribute buckets)
- S7 multi-sample selection produces NO additional cluster spread
  post-PM-1 (variant count up; cluster count still ~3-4 fallback)
- S7 effort exceeds ~3d (substantial complexity surfaced)
- S2 variant cycling methodology multi-option
- S3 PM-1 still produces degenerate fallback at 50+ variants
- S5 Wave B implementation surfaces canonical § 5 spec gaps
- A2-1 RE-FIRE-3 returns another material fail
- LLM cost projection toward $30/season
- Phase 7 cohesion_judge_confidence systematically below 0.75
- Wave A/Wave B cohesion-quality systematically poor
- Framing-audit catches at any dispatch consumption gate
- R48.4 pre-flight check FAIL
- Substantial unexpected failure mode
- A2-7 Matt v1 tag ratification (FINAL surface)

DO NOT surface for:

- Routine in-scope sequencing decisions
- Concern #3 pre-ratified P3c routing (LANDED)
- S7 pre-ratified contingent decisions (N=3 default; SELECT extension;
  multi-sample method; field placement) — KR routes per § 2.5
- Cascade-resumption-3 pre-ratified contingent decisions
- Auto-commit of work-products
- Per-season Gate-2 PASS-with-WARN/INFO (Pattern E fire-and-continue)
- Per-workstream push after Gate-2 PASS
- D13 parallel-fire P1-P9 items
- Legolas Mode A research POST-cascade-close
- A2-5 A/B comparison protocol execution by gandalf
- A2-6 jack-ryan disciplines batched canonical-write

ANCHORS (unchanged):

- Engine first / game second / phase third (CLAUDE.md)
- Substrate-led discipline (S1 + S7 ARE the substrate-led operational
  applications at substrate-input + substrate-consumption layers)
- Recognition → empirical validation → commit
- Math-before-code at math hotspots
- Right tool for the validation question
- Host-RAM-aware operational concurrency
- Framing-audit at dispatch consumption
- Design-quality audit at wave close
- Vocabulary lock
- Hive-mind decision-routing

YOUR FIRST OUTPUT THIS SESSION:

1. Acknowledge Phase A2 cascade-resumption-3 AMENDED entry (S7
   inserted; supersedes prior unamended cascade-resumption-3 fire
   prompt)

2. Report pre-flight verification:
   - vm_stat shows free + reclaimable RAM (R48.4 health check)
   - kit_archive.db intact at cycle-14-wave-5-season-001/
   - cascade artifacts intact at cycle-14-wave-5-season-001/
   - No leftover EGL log accumulation
   - No active sub-agent processes from prior session
   - git status clean (cascade-resumption-3 amendment + new fire
     prompt committed by gandalf prior session)
   - Confirm prior KR session (unamended cascade-resumption-3) closed

3. Author + fire Stream S1 (rocket class-eradication refactor) under
   R48.4 single-seam per authorization § 2 Stream S1

4. Cascade-resumption-3 AMENDED proceeds S1 → S7 → S2 → S3 → S5 → S6
   → A2-1 RE-FIRE-3

5. S4 (Phase 5 LLM prompt audit) is ALREADY COMPLETE per
   commit 13822ba; canonical doc consumed at S5 prep time

Phase A2 cascade-resumption-3 AMENDED target: Cycle 14 v1 MVP close
at D9 RATIFIED close-criterion.

Operate per discipline architecture above. Drive cascade-resumption-3
S1 → S7 → S2 → S3 → S5 → S6 → A2-1 RE-FIRE-3 → cascade through A2-7
+ D13 parallel to Cycle 14 v1 MVP D9 close.
```

## ---PROMPT ENDS---

---

## 1. What this prompt does differently from prior

| Element | Prior cascade-resumption-3 prompt | This amended prompt |
|---|---|---|
| Work program streams | 6 (S1, S2, S3, S4, S5, S6) | 7 (S1, **S7 NEW**, S2, S3, S4 ✅ done, S5, S6) |
| Total effort estimate | ~6-10d before A2-1 RE-FIRE-3 | ~7-12d (S7 adds ~1-2d) |
| Empirical basis for amendment | n/a | S0 verification finding 2026-05-29 evening |
| S2 dependency | S1 | **S7 (was S1)** |
| Required first reads | 8 docs | 8 docs (same; authorization doc has Amendment 1 header) |
| First-output expected | Fire S1 | Fire S1 (same; S7 dispatches after S1 close) |

## 2. What this prompt does NOT do

- Does NOT touch cohort_archetype taxonomy (PRESERVED per Matt scope confirmation)
- Does NOT touch T4 Capstone architecture or BVV framework
- Does NOT touch substrate library SCHEMA (S7 wires existing schema fields; not schema extension)
- Does NOT pre-ratify N>5 substrate samples per BC cell (default N=3; surface if N=10+ warranted)
- Does NOT include time-of-day language
- Does NOT include rest / fatigue editorializing
- Does NOT pre-ratify Cycle 15+ entry scope

## 3. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening direction: "halt KR session and amend authorization" + S0 verification finding empirically grounding S7 insertion

**For:** the operational fire prompt that triggers Phase A2 cascade-resumption-3 AMENDED in a fresh KR session post-halt of prior unamended KR session; composes with cascade-resumption-3 authorization (Amendment 1 header + § 2.5 S7 specification) as complete autonomous-fire package

**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` (authoritative; AMENDED with S7)
- `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-fire-prompt.md` (PRIOR cascade-resumption-3 fire prompt; SUPERSEDED by this amended version)
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` § 0.1 Amendment 1 + § 2.5 (S4 audit already complete)
