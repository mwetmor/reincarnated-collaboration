# Phase-1 P1 Coordination Matrix

**Authored:** 2026-05-17 by knight-rider at hive activation.
**Status:** Live; updated continuously by knight-rider as work advances.
**Purpose:** Per-deliverable seam mapping + cross-seam dependency DAG + concurrent-edit hot-spots.
**Companion:** `scope-of-work-phase-1-p1.md` (deliverable definitions); `phase-1-p1-log.md` (hive log); `hive-mind-protocol-2026-05-17.md` § 6.

---

## § 1 — Seam × deliverable matrix

Legend: **OWNER** (executes work); reads (consumes outputs); reviews (oversees correctness); — (no involvement); ✅ (complete).

| # | Deliverable | Rocket | Gamora | Star-lord | Drax | Jack-ryan | Gandalf |
|---|---|---|---|---|---|---|---|
| 1 | Substrate identity loader + YAML extraction | **OWNER** | reads | reads | reads | reviews | spec author ✅ |
| 2 | Substrate expansion engine refactor (13 coupling sites) | **OWNER (8 sites)** | **OWNER (1 site)** | **OWNER (3 sites)** | reads | reviews | input |
| 3 | Path-a archetype-template combinatorial refactor | reads | **OWNER** | reads | reads | reviews | input |
| 4 | Role registry refactor (`config/roles.yaml`) | **OWNER** | consumer | consumer | consumer | reviews | — |
| 5 | Ailment registry refactor (`config/ailments.yaml`) | **OWNER schema** | consumer | consumer | — | reviews | input (ailment design) |
| 6 | LLM prompt structure refactor (CRITICAL) | reads | reads | **OWNER** | reads | reviews | scaffold input |
| 7 | Resistance matrix 7×7 + math note | reads | **OWNER** | — | — | reviews math | input |
| 8 | Trait-floor extension (3 new classes) | reads | **OWNER impl** | — | reads | reviews | **OWNER design** |
| 9 | Gear-affix gating extension | reads | **OWNER impl** | — | reads | reviews | **OWNER design** |
| 10 | Substrate-coherent generation rules | reads | **OWNER** | reads | reads | reviews | input |
| 11 | Pool D1 re-score under substrate_native | ✅ | — | — | — | — | — |
| 12 | Layer 1 operational | (subsumed by D1) | | | | | |
| 13 | Layer 2 operational | (subsumed by D3) | | | | | |
| 14 | Layer 3 mirror-match diversity gate | reads | **OWNER** | — | — | reviews | metric spec author |
| 15 | Layer 4 LLM flavor diversifier | reads | reads | **OWNER** | reads | reviews | scaffold input |
| 16 | Layer 5 telemetry feedback | DEFERRED to Phase-2 | | | | | |
| 17 | Court of Forms vessel | **OWNER persistence** | reads | **OWNER Spirit-Guide voice** | **OWNER browser surface** | reviews | input |
| 18 | Spirit Guide voice amendment | — | — | **OWNER LLM integration** | — | reviews | **OWNER canonical authoring** |
| 19 | VFX library extension (canonical-7) | — | — | — | **OWNER** | reviews | input (substrate visual identity) |
| 20 | Grouping-vocab extension (lightning/holy/shadow labels) | — | — | reads | — | reviews | **OWNER** |
| 21 | Substrate browser (loadout app) | — | — | — | **OWNER** | reviews | input |
| 22 | Embodiment-display substrate extension | — | reads | **OWNER manifest** | **OWNER display** | reviews | input |
| 23 | Decisions-log entry (substrate expansion) | — | — | — | — | **OWNER Gate 1** | reviews |
| 24 | Decisions-log entry (Court-as-grace) | — | — | — | — | **OWNER Gate 1** | reviews |
| 25 | Decisions-log entry (hive-mind activation) | — | — | — | — | **OWNER Gate 1** | reviews |
| 26 | Cross-doc updates (cosmology / Spirit-Guide / Court) | — | — | — | — | reviews | **OWNER** |
| 27 | Perception test execution | — | — | — | **OWNER session-runner** | **OWNER measurement protocol + analysis** | **OWNER experiment design + pair generation** + Matt/son (subjects) |

**Knight-rider role across all deliverables:** harmonizes; updates this matrix; surfaces L2/L3 decisions in hive log; authors daily state-of-hive.

**Decisions-log entries (D23–D25)** are knight-rider-drafted with jack-ryan Gate 1; knight-rider is the OWNER of authoring the draft, jack-ryan is the OWNER of the Gate 1 pass. Matrix shows jack-ryan as Gate-1 OWNER for clarity.

---

## § 2 — Cross-seam dependency DAG

Arrows: A → B means "A's output is required input for B's start."

```
                                 ┌─────────────────────────────────────────────────┐
                                 │                                                 │
              ┌──────────────────▼──────────────────┐                              │
              │ D1: Substrate Identity Loader       │                              │
              │ (rocket) — foundation               │                              │
              └─────────────┬───────────────────────┘                              │
                            │                                                      │
                ┌───────────┼───────────┬─────────────┬─────────────┐              │
                │           │           │             │             │              │
                ▼           ▼           ▼             ▼             ▼              │
        ┌────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────────┐    │
        │ D4: Role   │ │ D5: Ail. │ │ D6: LLM │ │ D20: Grp │ │ D17: Court    │    │
        │ Registry   │ │ Registry │ │ Prompt  │ │ Vocab    │ │ vessel        │    │
        │ (rocket)   │ │ (rocket) │ │ Refactr │ │ (gandalf │ │ (rocket/drax/ │    │
        │            │ │          │ │ (s-lord)│ │  1 day)  │ │  s-lord)      │    │
        └─────┬──────┘ └────┬─────┘ └────┬────┘ └────┬─────┘ └───────┬───────┘    │
              │             │            │           │                │            │
              └──────┬──────┘            │           │                │            │
                     ▼                   │           ▼                ▼            │
            ┌──────────────────┐         │  ┌─────────────┐  ┌───────────────────┐ │
            │ D3: Path-a       │         │  │ D6 cont.    │  │ D18: Spirit-Guide │ │
            │ Archetype Refac. │         └─►│ (consumes   │  │ voice amendment    │ │
            │ (gamora)         │            │  D20)       │  │ (gandalf + s-lord) │ │
            └────────┬─────────┘            └──────┬──────┘  └────────────────────┘ │
                     │                             │                                 │
                     ▼                             │                                 │
            ┌──────────────────┐                   │                                 │
            │ D2: Substrate    │                   │                                 │
            │ Expansion 13     │                   │                                 │
            │ Coupling Sites   │                   │                                 │
            │ (multi-seam)     │                   │                                 │
            └────────┬─────────┘                   │                                 │
                     │                             │                                 │
        ┌────────────┼─────────────┐               │                                 │
        │            │             │               │                                 │
        ▼            ▼             ▼               │                                 │
   ┌────────┐  ┌──────────┐  ┌──────────┐         │                                 │
   │ D7:    │  │ D8:      │  │ D9:      │         │                                 │
   │ Resist │  │ Trait    │  │ Gear-    │         │                                 │
   │ Matrix │  │ Floor    │  │ Affix    │         │                                 │
   │ 7×7    │  │ Ext.     │  │ Ext.     │         │                                 │
   │(gamora)│  │ (gan/gam)│  │ (gan/gam)│         │                                 │
   └────┬───┘  └──────────┘  └──────────┘         │                                 │
        │                                          │                                 │
        ▼                                          │                                 │
   ┌────────────────────────────┐                  │                                 │
   │ D10: Substrate-coherent    │                  │                                 │
   │ Generation Rules (gamora)  │                  │                                 │
   └────────────┬───────────────┘                  │                                 │
                │                                  │                                 │
                ▼                                  │                                 │
   ┌──────────────────────────────────┐            │                                 │
   │ D14: Layer 3 Diversity Gate      │            │                                 │
   │ (gamora) — BLOCKED on D27 perc.  │            │                                 │
   │ test result (metric grounding)   │            │                                 │
   └─────────────┬────────────────────┘            │                                 │
                 │                                 │                                 │
                 ▼                                 │                                 │
   ┌──────────────────────────────────────────────▼──────┐                          │
   │ D15: Layer 4 LLM Flavor Diversifier (star-lord)     │                          │
   │ — consumes D6 LLM prompt structure + D1 declarations │                          │
   └─────────────┬────────────────────────────────────────┘                          │
                 │                                                                   │
                 ▼                                                                   │
   ┌─────────────────────────────────┐                                              │
   │ D19: VFX Library Extension      │ ◄─── BLOCKED on Matt vendor acquisitions    │
   │ (drax) + D21: Substrate Browser │       (CraftPix premium, Fellor Crystal,    │
   │ (drax) + D22: Embodiment Disp.  │        Frostwindz Deathbringer)             │
   │ (drax + star-lord)              │                                              │
   └─────────────┬───────────────────┘                                              │
                 │                                                                   │
                 ▼                                                                   │
   ┌─────────────────────────────────┐                                              │
   │ D23/D24/D25: Decisions-log      │                                              │
   │ entries (knight-rider + j-ryan) │                                              │
   │ + D26: Cross-doc updates (gan)  │                                              │
   └─────────────┬───────────────────┘                                              │
                 │                                                                   │
                 ▼                                                                   │
        ┌──────────────────┐                                                         │
        │ SHIP GATE        │ ◄─── Matt L3 approval; tag `v1.0-phase-1-p1`           │
        └──────────────────┘                                                         │
                                                                                     │
   ┌────────────────────────────┐                                                    │
   │ D27: Perception Test       │ ◄─── parallel; ~3-4 days end-to-end ──────────────┘
   │ (drax+gandalf+Matt+jack-ry)│
   │ Phase-1 P1a PREREQUISITE   │
   │ to D14 Layer 3 metric      │
   └────────────────────────────┘
```

**Critical path traversal:** D1 → D3 → D7 → D10 → D14 → D15 → SHIP. Per scope-of-work § 3: ~6–8 weeks estimate.

**Major parallel tracks:** D17/D18 (Court vessel); D19/D21/D22 (player-facing); D6 (LLM prompt refactor — runs in parallel with D7+D10 once D20 lands); D27 (perception test — runs parallel with D1–D10).

---

## § 3 — Concurrent-edit hot-spots

Files multiple seams will need to touch concurrently. Coordinate via hive log STATE+HANDOFF entries before edits.

| File | Touching seams | Coordination |
|---|---|---|
| `src/reincarnated/foundation/__init__.py` | rocket (D1 loader integration), gamora (D2 Coupling #7) | rocket lands first (D1); gamora reads-and-extends |
| `src/reincarnated/generation/b6_archetype_templates.py` | rocket (D2 Coupling #3 — refactor hardcoded ELEMENT_AFFINITY), gamora (D3 Path-a refactor — replaces entire 14-template dict) | rocket's D2 work is subsumed by gamora D3; **gamora owns this file post-D3**. Rocket coordinates Coupling #3 changes into D3 staging branch via hive-feature-branch if timing requires. |
| `src/reincarnated/generation/element_biases.py` | rocket (D2 various Couplings), gamora (D3 stat_allocator, D5 ailment_registry consumer) | sequential: rocket refactors first; gamora consumes |
| `src/reincarnated/element/schema.py` | rocket (D2 Coupling #1 SeasonalElements refactor; D11 ✅ pool schema already-touched) | rocket-only seam; no concurrency |
| `src/reincarnated/element/selector.py` | rocket (D2 Coupling #2 VALID_SLOTS; D11 ✅ selector hard-floor already-touched) | rocket-only seam; no concurrency |
| `src/reincarnated/llm/cosmological_vocabulary.py` | star-lord (D6 CRITICAL refactor) | star-lord-only seam |
| `src/reincarnated/llm/naming.py` | star-lord (D2 Coupling #8 fail-loud + D6 prompt refactor) | star-lord-only seam |
| `src/reincarnated/telemetry/recorder.py` | star-lord (D2 Coupling #9 dict-keyed lookup post-D1) | star-lord-only seam |
| `src/reincarnated/simulation/balance_loop.py` | gamora (D2 Coupling #7 registry-passing + D7 resistance matrix + D14 diversity gate) | gamora-only seam |
| `src/reincarnated/simulation/damage_resolver.py` | gamora (D7 7×7 matrix consumer) | gamora-only seam |
| `src/reincarnated/generation/monster_generator.py` | rocket (D2 Coupling #4) | rocket-only seam |
| `src/reincarnated/generation/trial_generator.py` | rocket (D2 Coupling #5) | rocket-only seam |
| `src/reincarnated/generation/season_orchestrator.py` | rocket (D2 Coupling #10 — GOOD PATTERN reference; D10 substrate-rotation) | rocket-only seam |
| `src/reincarnated/generation/gear_catalog.py` | rocket (D2 Coupling #11 ✅ GOOD PATTERN); gamora (D9 gear-affix gating extension at boundary) | sequential: rocket confirms pattern; gamora extends gating logic via composition. |
| `src/reincarnated/generation/role_constraints.py` | rocket (D4 role registry consumer refactor) | rocket-only seam |
| `src/reincarnated/generation/class_generator.py` | rocket (D4 role registry consumer; D2 Coupling #4 action/role-function via D3) | rocket-only seam (D4 first; D3 subsumes) |
| `src/reincarnated/simulation/ai_strategies.py` | gamora (D4 role registry consumer) | gamora-only seam |
| `src/reincarnated/generation/ability_grammar.py` | rocket (D4 role registry consumer + D5 ailment registry consumer) | rocket-only seam |
| `config/elements.yaml` (existing) | rocket (becomes `substrate_identities/*.yaml` per D1; existing file deprecated post-D1) | rocket migrates; deprecation note in MIGRATION.md |
| **NEW: `config/substrate_identities/*.yaml`** (7 files) | rocket creates (D1); ALL seams read | rocket-only authorship; consumers read-only |
| **NEW: `config/roles.yaml`** | rocket creates (D4); ALL seams read | rocket-only authorship; consumers read-only |
| **NEW: `config/ailments.yaml`** | rocket creates (D5); ALL seams read | rocket-only authorship; consumers read-only |
| `canonical/story/grouping-layer-vocabulary.md` | gandalf (D20 extension); star-lord reads (D6) | gandalf-only authorship; star-lord reads after D20 lands |
| `canonical/story/spirit-guide-voice.md` | gandalf (D18 + D26 amendments) | gandalf-only authorship |
| `canonical/story/cosmology-reincarnated.md` | gandalf (D26 substrate-section amendment) | gandalf-only authorship |
| `canonical/story/court-of-forms.md` | gandalf (D26 elevation to architectural commitment) | gandalf-only authorship |
| `reincarnated-engine/design/decisions/decisions-log.md` | knight-rider (D23/D24/D25 drafts); jack-ryan (Gate-1 review staging into `qa/pending/`); Matt (approval) | knight-rider stages in `qa/pending/`; commits after Matt approval; specialists do NOT touch directly |
| `reincarnated-loadout/src/...` (loadout app) | drax (D17 browser, D21 substrate browser, D22 embodiment display) | drax-only seam |
| `reincarnated-demo/src/...` (demo) | drax (D19 VFX integration, D22 demo embodiment, D27 perception-test session runner) | drax-only seam |

**Race-condition prevention (per CHANGELOG 2026-05-16 lesson):**
- All specialists stage by explicit file path (`git add <path>`); NO `-A` / `.` / `-am`
- Knight-rider does not commit engine files while specialist sessions are committing
- Commit messages describe ONLY the seam's own staged changes
- If two seams need to commit to the same repo within the same minute window, second seam waits + reads first commit before staging

---

## § 4 — Cross-seam contract authoring (MIGRATION.md cadence)

Per protocol § 6.2: MIGRATION.md authoring is **concurrent** with the producing seam's work. Each producing-seam MIGRATION.md location:

| Seam | MIGRATION.md path | Phase-1 P1 entries expected |
|---|---|---|
| rocket | `src/reincarnated/generation/MIGRATION.md` | D1 (foundation integration); D2 substrate-keyed coupling fixes; D4 role registry; D5 ailment registry |
| rocket | `src/reincarnated/element/MIGRATION.md` | D2 Couplings #1, #2 (element seam) |
| gamora | `src/reincarnated/simulation/MIGRATION.md` | D3 archetype refactor; D7 resistance matrix; D10 generation rules; D14 diversity gate |
| star-lord | `src/reincarnated/export/MIGRATION.md` | D2 Coupling #9 (telemetry recorder); D6 LLM prompt structure refactor; D15 LLM flavor extension |
| drax (loadout) | `reincarnated-loadout/MIGRATION.md` | D17 browser; D19 VFX consumption from engine emission; D21 substrate browser data shape; D22 embodiment display |
| drax (demo) | `reincarnated-demo/MIGRATION.md` (or per-module) | D19 VFX rendering integration; D22 demo embodiment; D27 perception-test runner |

Jack-ryan continuously verifies MIGRATION.md ↔ schema-change coherence (per protocol § 6.4). Mismatches surface as hive log OBSERVATION entries with WARN tag.

---

## § 5 — Maintenance protocol

Knight-rider updates this matrix when:
- A deliverable status changes (in flight, blocked, completed)
- A cross-seam dependency emerges that wasn't in the original DAG
- A concurrent-edit hot-spot surfaces
- A new file enters the matrix (e.g., new module under refactor)

Updates land via direct edits; significant restructures surface in hive log as AMENDMENT entries.

---

*Authored 2026-05-17 by knight-rider at Phase-1 P1 hive activation. The coordination atlas. Consult before touching cross-seam-impacting work.*
