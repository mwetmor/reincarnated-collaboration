# Corpus curation log — Edition-III Stage A: pull-7 re-insertion + keying completion

> **STATUS:** CURRENT (record of a completed re-insert + keying batch). Edition-III Stage A.
> **Author:** elrond (data steward) · **Date:** 2026-07-15
> **Store:** `agentic_orchestration/research/curated/corpus.db` (elrond-owned, gitignored — this log is the committed record)
> **Batch class:** RE-INSERT + KEY-COMPLETION (post-census-freeze). Additive; NO treatment=hybrid keys.
> **Script:** `agentic_orchestration/research/scripts/corpus_edition3_stageA_pull7_2026_07_15.py`
> **Backup-before-batch:** `corpus.db.pre-edition3-2026-07-15-backup` (644 corpus / 618 engine_key).
> **Commission:** `agentic_orchestration/gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md` §1.

---

## 0. Ground-truth reconciliation (the state I actually inherited)

The commission brief §0 states corpus=651 with the 7 pull-tranche rows "IN but keying deferred."
**The on-disk truth at Stage-A start was corpus=644, the 7 rows OUT** — because the Edition-II
census-freeze REVERT (`corpus-curation-pull-tranche-deferred-2026-07-15-log.md`) removed them. The
brief's "651" was the pre-revert count. Honest inheritance: **644 / 618 / 469 frozen survivors**;
Stage A RE-INSERTS the 7 rows (they were curated + reverted, not merely deferred) and COMPLETES
their keying.

## 1. Survivor-baseline reconciliation (why a new script, not the old insert re-run)

The Edition-II Stage-1 insert script carries a hard-coded `SURVIVOR_SHA_BASELINE = ce67bfba…` that
is the **PRE-Stage-3 survivor digest**. Since it was written, the Edition-II Stage-3 pull re-keys
FIRED (`d3-zbarb` none→pull, `di-cyclone-monk-pvp` knockback→pull) — both are survivor rows, so the
469-survivor digest legitimately moved to `fdd7fbfa…`. Re-running the old script fails its guard
BEFORE (correctly — its baseline predates Stage-3). I did NOT bypass the guard. Instead the
Edition-III Stage-A script:
- **proved the baseline shift is fully accounted** (not blind drift): the current survivor state ==
  the pre-edition2 survivor state EXCEPT exactly the two documented Stage-3 re-keys, each at
  cell_key slot #5b only (`none`→`pull`, `knockback`→`pull`). Fail-loud on any UNaccounted diff.
- guards against the CURRENT (post-Stage-3) baseline;
- reuses the SAME 7-row manifest + enrichment from the Stage-1 module (single source of truth for
  the row data — no drift);
- asserts each of the 7 intended cell_keys byte-exact (the keying is COMPLETED, not deferred).

The Stage-1 insert script is left unmutated as the reverted-batch's historical artifact.

## 2. The 7 rows inserted + keyed (full completeness)

| kit_id | treatment | function | cell_key |
|---|---|---|---|
| `la-destroyer-vortex-gravity` | damage | **pull** | rooted\|melee\|spiky\|vortex_pull\|damage\|pull\|tank\|cooldown\|solo\|melee\|high\|instant\|active\|one-shot |
| `la-destroyer-gravity-impact` | damage | **pull** | rooted\|melee\|flat\|vortex_pull\|damage\|pull\|tank\|generator-spender\|solo\|melee\|med\|channel\|active\|build→spend |
| `la-destroyer-gravity-force` | damage | **pull** | walk\|melee\|flat\|line\|damage\|pull\|mitigate\|generator-spender\|solo\|melee\|med\|wind-up\|active\|build→spend |
| `la-destroyer-gravity-compression` | damage | **none** | rooted\|melee\|spiky\|ground_targeted_circle\|damage\|none\|mitigate\|generator-spender\|solo\|melee\|med\|channel\|active\|build→spend |
| `d4-spiritborn-vortex` | damage | **pull** | **blank**\|at-target\|spiky\|vortex_pull\|damage\|pull\|evade\|generator-spender\|solo\|mid\|med\|instant\|active\|build→spend |
| `d3-wizard-black-hole` | damage | **pull** | rooted\|at-target\|spiky\|vortex_pull\|damage\|pull\|glass\|spend\|solo\|ranged\|med\|instant\|active\|one-shot |
| `di-cyclone-strike-monk-base` | damage | **pull** | rooted\|melee\|flat\|vortex_pull\|damage\|pull\|evade\|cooldown\|solo\|melee\|med\|wind-up\|active\|one-shot |

**Hybrid gate:** both proposed hybrids (`la-destroyer-vortex-gravity`, `di-cyclone-strike-monk-base`)
key `ctrl_treatment=damage`, `ctrl_function=pull` per `hybrid-assignment-criteria-2026-07-15.md` §4
(gandalf-adopted, brief §0). **Corpus stays hybrid-EMPTY** — the T5 frontier honest.

Enrichment re-applied on the 2 existing rows (`di-cyclone-monk-pvp`, `d3-zbarb`) — mech_note
fact-append; cell_key untouched (the enrichment text was removed by the Edition-II revert's verbatim
restore; Stage-3 re-keyed only the function; this stage restores the enrichment provenance).

## 3. The four live flags (brief §1) — dispositions

- **(a) `la-destroyer-gravity-compression` pull INFERRED → function=none.** RE-VERIFIED against the
  tranche source row (`2026-07-15-pull-intrinsic-classkit-tranche.md` line 24): the row's own
  `treatment` field says *"damage-primary (no explicit pull on living enemies in base description)"*
  and the mech_note says the pull is *"implicit … rather than an explicit 'enemies moved toward
  caster' description."* Never-invent governs → `function=none`, `pull_pending_vocab=0`. The
  `d4-spiritborn-vortex` movement is likewise source-silent (line 25: *"unknown (not documented in
  available sources)"*) → `mob=blank` honest-NULL (cell will not light on the movement gate). CONFIRMED.
- **(c) Destroyer cell-distinctness ACROSS GRAINS.** The 4 pull-tranche Destroyer rows are SKILL
  grain (individual skills); the LA-tranche `la-destroyer-rage-hammer` + `la-destroyer-gravity-training`
  are ENGRAVING/identity grain (Stage B). DIFFERENT grains of the same class — both legitimate rows
  measuring different objects (a skill vs an identity path). **Grain-of-record adjudication:** the 4
  skill-grain rows carry atlas cell placement here; the 2 engraving-grain rows carry placement in
  Stage B; they do NOT collide (their cell_keys differ — skill-grain uses `delivery=melee` + specific
  geometries; engraving-grain uses `delivery=at-target` + `melee_strike`). Among the 4 skill-grain
  rows, all 4 cell_keys are DISTINCT (asserted in-script): they differ on {geometry, commit,
  dependency, amp}. No two collapse.
- **(d) `di-cyclone-strike-monk-base` vs `di-cyclone-monk-pvp`.** Distinct cells (asserted in-script):
  movement rooted vs walk, delivery melee vs self-origin, commit wind-up vs instant.
- **(e) Undecember Illusion Hook bounded re-check.** AFFIRM EXCLUSION. The tranche's empty-verdict
  line (line 102) rules it EMPTY per the intrinsic bar (classless rune-assembled, not
  class-intrinsic). In-corpus evidence is decisive: `ud-illusion-family` already carries the HOOK as
  a weapon-type variant of an ECHO-COPY skill (`geometry=multi_projectile`, `damage × none`), NOT a
  grappling pull. No new `ud-` row. (Bounded to existing evidence — no new crawl, per brief.)

## 4. Proofs (in-script, all PASS)

| proof | result |
|---|---|
| baseline-accounted | current survivor state == pre-edition2 EXCEPT the 2 documented Stage-3 re-keys (#5b only) |
| keying-completed | all 7 intended cell_keys asserted byte-exact |
| flag (c) distinctness | 4 Destroyer skill-grain rows → 4 distinct cells |
| flag (d) distinctness | di-base ≠ di-pvp (distinct cells) |
| survivor-guard | 469 survivors byte-identical before+after (`fdd7fbfa…`) |
| counts | corpus 644→**651** (+7); engine_key 618→**625** (+7); hybrid rows **0** |

WAL checkpointed; integrity_check = ok.

## 5. Reversibility

Every row is source-anchored to the pull-intrinsic tranche table + the criteria memo §4. The insert
is idempotent (re-run to byte-identical state). The raw provenance is in the manifest + this log +
the (unmutated) Stage-1 module. Backup `corpus.db.pre-edition3-2026-07-15-backup` preserves the
pre-batch state.

---

**Signed:** elrond (data steward) — the deferral expired; the 7 rows are keyed at full completeness
on evidence, the hybrid frontier stays honestly empty, and the survivor baseline shift is proven to
be exactly the two Edition-II re-keys, nothing hidden.
