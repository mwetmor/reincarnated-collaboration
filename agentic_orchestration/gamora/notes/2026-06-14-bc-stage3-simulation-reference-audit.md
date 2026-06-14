# BC-coordinate cutover Stage 3 — simulation-seam reference-audit + elemental zero-label proof

**Type:** reference-audit (gamora seam) — the §2 carve for the simulation seam + the §3.1 proof run.
**Date:** 2026-06-14
**Author:** gamora
**Authority:** Matt-ruled NARROW Stage 3 (2026-06-14); gandalf scoping ruling `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md` (§2 carve, §3.1 proof).
**Status:** READ-ONLY prereq. NO production symbol deleted or modified. GATES the deletion; does not perform it.
**Companion:** rocket parallel generation-side audit (ARCHETYPE_TEMPLATES / legacy_archetype_shim / classify_archetype / V-D residents); KR synthesizes the combined set.
**Proof artifact:** `reincarnated-engine/output/bc-stage3-zero-label-proof-20260614_214135.json` (full 12-class season; PASS).
**Harness:** `reincarnated-engine/scripts/gamora_bc_stage3_zero_label_proof_2026_06_14.py` (attribution-instrumented; monkeypatch-only, touches no production symbol).

---

## 0. TL;DR

- The simulation-seam label-input firing sites are reached ONLY by `bc_target`-ABSENT combatants. Per the
  reference-audit, that is: experimental kits, weird kits (not generated in the live loop), monsters, trials, packs.
- **PHYSICAL kits carry a `bc_target`** (computed at `class_generator.py:433`, stamped at `:553`) even though
  generation routes them to the legacy b6 builder for kit CONTENT. At the SIMULATION instrument they therefore
  pilot via BINS (PRIMARY path), NOT via the label fallback. This corrects gandalf's prior reason for HELDing
  `ARCHETYPE_ROLE_PRIORITY` (see §3).
- **Zero-label proof: PASS.** Full 12-class season (10 elemental + 1 live physical `rogue` + 1 experimental).
  `site1 (ARCHETYPE_ROLE_PRIORITY)` and `site2 (_PLAYER_CONTROLLER_ARCHETYPES)` BOTH never fired.
  ELEMENTAL_LEAK = 0, PHYSICAL_LEAK = 0. No elemental leak → does NOT block Stage 3.
- **Live physical kits DO appear in current-season generation** (physical is the last element in the rotation
  pool, `season_orchestrator.py:1527`). This run generated 1 (`rogue`). They are coordinate-bearing, so the
  physical fallback at the SIMULATION seam is already inert for them — but the GENERATION-side physical fork
  (rocket's seam) is still load-bearing, which is why Stage 3b stays parked.

---

## 1. Method

The simulator MEASURES a kit by PILOTING it (§7.5 discrimination-law-at-the-instrument). The "label-input" at this
seam is any consultation of a label-keyed AI table to decide the rotation. Full inventory of simulation-seam
label-keyed machinery (grep `--include='*.py' src/reincarnated/simulation/`):

| Symbol | Site | Kind |
|---|---|---|
| `_PLAYER_CONTROLLER_ARCHETYPES` | `ai_strategies.py:45` (frozenset), tested `:460` | label membership → control-first gate |
| `ARCHETYPE_ROLE_PRIORITY` | `ai_strategies.py:52` (dict), looked up `:377/:378` | label → role-priority ordering |
| `_PREFERRED_BEHAVIOR_ROLES` | `ai_strategies.py:356` (local dict) | monster R3 behavior → ordering (NOT label-keyed) |
| `_REGISTRY_DEFAULT_PRIORITY` / `_ROLE_REGISTRY` | `ai_strategies.py:149/155` | registry-derived default (NOT label-keyed) |
| `CombatantState.archetype` (field) | `combatant.py:109` | the carried label string |
| `ARCHETYPE_TEMPLATES[archetype_tag]` (consumed) | `balance_loop.py:1886/1948/2030/2183` | label → kit-template, for element-redistribution/role-swap during balancing |

Consumer trace (every caller, grepped at source):
- `bc_target_role_priority` + `get_priority_roles`: **zero external callers** — only called from within `ai_strategies.py`
  (`_scripted:503`, `get_priority_roles` internal). So the only live entry to the label tables is via `_scripted`
  / `_common`, both of which hold the combatant.
- `combatant.archetype` read sites engine-wide: `ai_strategies.py:460` (the `_PCA` membership) and `:504`
  (the `get_priority_roles` arg). No other `.archetype` field read in simulation.

The tri-state (Stage-2 landed) gates BOTH label sites behind `bc_target is None`:
- `get_priority_roles` (`:336`): `bc_target is not None` → bin ordering returned BEFORE `ARCHETYPE_ROLE_PRIORITY`
  is ever consulted; the label table is reached only when `bc_target` is None/malformed AND no `preferred_behavior`.
- `_common` (`:453/:460`): the `_PLAYER_CONTROLLER_ARCHETYPES` membership is an `elif` reached only when
  `bc_target is None`.

## 2. The carve — simulation-seam elemental-only-deletion-set vs HELD-set

Principle (gandalf §2): DELETE if referenced ONLY by the elemental/coordinate path; HOLD if the physical fallback
(or any other still-live consumer) still touches it. Refined empirically: the simulation-seam label sites are
reached by `bc_target=None` combatants, which is NOT the physical population (physical carries bc_target) but IS
the experimental/weird/monster/trial population.

| Symbol (simulation seam) | Classification | Reached by (consumer trace) | Verdict |
|---|---|---|---|
| `_PLAYER_CONTROLLER_ARCHETYPES` | **HELD (→ Stage 3b)** | `_common:460` elif, only when `bc_target is None`. Members include `physical_grappler`. Currently UNEXERCISED at the live instrument (no live `bc_target=None` kit is a controller archetype — experimental→`"experimental"`, weird not generated), but it is the demoted fallback contract for any future bc_target-absent controller (pre-cutover replays, weird, support/hybrid post-3b). | HOLD — it is the Stage-2 demoted fallback, not elemental-only; deleting it now removes the tri-state's FALLBACK leg before the absent-population is gone. |
| `ARCHETYPE_ROLE_PRIORITY` | **HELD (→ Stage 3b)** | `get_priority_roles:377/378`, only when `bc_target is None` AND `preferred_behavior` unhandled. Live consumers of the `bc_target=None` path = **monsters** (`from_monster`, `ai_strategy="scripted"`, no bc_target) + experimental kits. Validated at boot by `_load_and_validate_registry:135`. | HOLD — confirmed HELD, but the CORRECT REASON is monster/experimental keying, NOT physical (see §3). Deleting it would break the monster scripted path. |
| `_PREFERRED_BEHAVIOR_ROLES` | **HELD (orthogonal)** | `get_priority_roles:366/367` (monster R3 path). Never label-keyed; not part of the cutover. | HOLD — out of scope; monster-path machinery. |
| `_REGISTRY_DEFAULT_PRIORITY` / `_ROLE_REGISTRY` | **HELD (orthogonal)** | Registry-derived loud-default for unknown archetypes (`:387`) + boot validation. Trials route here (`archetype="trial"` → registry default). Not label-keyed. | HOLD — out of scope; the Pattern-P7 loud default. |
| `CombatantState.archetype` (field) | **HELD (shared infra)** | Set for ALL combatants incl. monsters/trials/packs (`combatant.py:741/803/903/955`). Read by the two label sites AND consumed downstream by export/telemetry (`export/*.py`, `telemetry/recorder.py` reference `archetype`/`archetype_tag` — star-lord seam). | HOLD — shared infrastructure; not a Stage-3 target at all (the field stays; only the label-KEYED machinery is in scope). |
| `ARCHETYPE_TEMPLATES[archetype_tag]` consumption in `balance_loop.py` | **HELD (physical-shared)** | 4 sites (`:1886/:1948/:2030/:2183`) key the generation `ARCHETYPE_TEMPLATES` by `archetype_tag` for element-redistribution + role-swap during balancing; applies to elemental AND physical kits (graceful `None` skip). `ARCHETYPE_TEMPLATES` is also rocket's physical-fork dependency (`class_generator.py:642`). | HOLD — `ARCHETYPE_TEMPLATES` is rocket-owned and physical-shared; the simulation-seam consumption is brownfield-safe (template None → skip) but the table itself is HELD by both seams. |

**Simulation-seam elemental-only-deletion-set: EMPTY.** No simulation-seam label-keyed symbol is elemental-only.
Every one is HELD — either as the Stage-2 demoted fallback for the still-live `bc_target=None` population
(monsters/experimental/weird/pre-cutover), as orthogonal monster/registry machinery, as shared infrastructure
(the `archetype` field), or as a rocket-owned physical-shared table.

This is consistent with the cut being NARROW: the elemental-abandoned start-of-pipe machinery to delete lives in
ROCKET's seam (the elemental `ARCHETYPE_TEMPLATES` entries, V-D residents, classify_archetype on the elemental
path). The SIMULATION seam holds nothing elemental-only — it was already converted to a tri-state in Stage 2
where the label tables are the DEMOTED FALLBACK, and the fallback's consumers (monsters/experimental) are not the
elemental path and are not going away in narrow Stage 3.

## 3. Correction to gandalf's prior on ARCHETYPE_ROLE_PRIORITY (semantic precision — Disc #12)

gandalf's §2 prior: `ARCHETYPE_ROLE_PRIORITY` is HELD because "physical kits still key against it via the fallback."

**Empirical finding:** physical kits do NOT key against the simulation-seam fallback. They carry a `bc_target`
(computed unconditionally in the standard generation branch at `class_generator.py:433`, including for physical
coordinates BEFORE the physical-fork routes content to b6), so at the SIMULATION instrument they take the bin
PRIMARY path and never reach `ARCHETYPE_ROLE_PRIORITY[label]`. The proof run confirms: 1 live physical kit
(`rogue`, bc_target present) → 0 PHYSICAL_LEAK.

**Same verdict (HELD), corrected mechanism:** `ARCHETYPE_ROLE_PRIORITY` is HELD because **monsters** (and the
experimental observation slot) key against it via the `bc_target=None` scripted path — `from_monster` sets
`archetype` and no `bc_target`. This is a STRONGER hold than the physical-fallback reason: monsters are a
permanent population unaffected by the physical-pool-expansion that gates Stage 3b. (Note the §3.1 run showed even
monsters mostly route via `preferred_behavior`/registry-default in current content; a monster WITHOUT
`preferred_behavior` and with an archetype in the table would still hit `ARCHETYPE_ROLE_PRIORITY` — so it remains
load-bearing as the demoted fallback.)

Routing for KR/gandalf: the symbol stays HELD; the JUSTIFICATION in any Stage-3 / Stage-3b record should read
"demoted fallback for the bc_target-absent population (monsters + experimental), NOT the physical kit path" so the
deletion criterion for Stage 3b is correctly framed (it is gated on the bc_target-absent population shrinking, not
specifically on physical-pool expansion).

## 4. §3.1 proof run — full-season elemental zero-label, attribution-instrumented

- **Run:** `generation_mode="no_coalesce"` (ZERO LLM), `smoke_test=False`, n_classes=12, fights/matchup=4, seed=20260614.
  (Fights minimized to make the spatial-gauntlet full season tractable; attribution logic is fight-count-independent —
  every kit pilots against the gauntlet at least once. Discipline #2: smoke-validated the harness on a 6-class run
  first, also PASS.)
- **Instrumentation (discrimination-law-at-the-instrument):** monkeypatch wrappers on `_scripted` + `_common`
  (the only live entries to the label tables) attribute each label-table consultation to ELEMENTAL_LEAK /
  PHYSICAL_LEAK (coordinate-bearing kit → a leak) vs EXPERIMENTAL_OR_WEIRD / MONSTER_OR_TRIAL (bc_target-absent →
  expected/legitimate). Wrappers OBSERVE only; they call through to the originals (no behavior change).
- **Census:** 10 elemental (bc_target present) + **1 live physical** (`rogue`, bc_target present) + 1 experimental
  (bc_target None).
- **Result:** `site1_ARCHETYPE_ROLE_PRIORITY` never fired; `site2_PLAYER_CONTROLLER_ARCHETYPES` never fired.
  **ELEMENTAL_LEAK = 0, PHYSICAL_LEAK = 0 → PASS.**
- **Interpretation:** no coordinate-bearing kit (elemental OR physical) reaches a simulation-seam label table.
  The elemental path is structurally clean at the instrument; an elemental leak (which would BLOCK Stage 3) does
  not exist in current generation.

## 5. Side-benefit (gandalf): do live physical kits appear?

**YES.** Physical is the last element in the season rotation pool (`season_orchestrator.py:1527`:
`elements = [rotating...] + ["physical"]`). The 12-class run generated 1 live physical kit (`rogue`). Implication
for Stage 3b timing: the GENERATION-side physical fork (rocket: `class_generator.py:636-714` PHYSICAL-FORK ROUTING
→ legacy b6) is still load-bearing for live physical kits, so the physical fallback in ROCKET's seam stays HELD
until physical-pool expansion lands. The SIMULATION-seam label fallback is already inert for physical (they carry
bc_target), but that does not unblock Stage 3b — Stage 3b is gated by the generation-side physical pool, not the
simulation seam.

## 6. Disposition

- **(a) Simulation-seam elemental-only-deletion-set: EMPTY.** HELD-set: all six rows in §2.
- **(b) Proof: PASS** — elemental label-input firing = 0; physical = 0; attribution broken out by path.
- **(c) Live physical kits present: YES** (1 `rogue` this season).
- **(d) Elemental leak: NONE found** → does NOT block Stage 3.
- **(e) Blocker: none** from the simulation seam. The narrow Stage-3 deletion target is entirely in rocket's
  generation seam; gamora's seam contributes no deletable symbol (already a clean tri-state from Stage 2).

HALT per dispatch — no deletion. Stage-3 deletion is a separate Matt-final-go dispatch.

---

**Signed:** gamora, 2026-06-14
