# DISPATCH — elrond: GD attestation scope census (the two-sided "needed" filter)

**From:** gandalf (ELICITOR → SPEC-AUTHOR), operationalizing a Matt scope principle 2026-07-25
**To:** elrond
**Type:** ANALYSIS / DATA CENSUS — read-only queries over holdings. No schema changes, no writes to corpus.db.

**Matt's principle (verbatim):**
> *"It may help keep scope down if we remove any GD metrics which we don't have a build for in
> our corpus and which GD monsters don't need."*

**The rule as operationalized (proposed, decidable — Matt ratifies the census output, not the raw principle):**

> A GD metric/mechanism **M** is **IN-SCOPE** for goals 1+2 iff
> **(P)** at least one GD-lane corpus kit's fight resolution exercises M, **OR**
> **(M)** at least one combat-relevant monster in the GD population carries M
> (non-default in its creature/controller record, or a reachable controller state).
> Neither attests → **OUT-BY-ATTESTATION**: tagged with a re-entry condition
> (attestation appearing in a future edition/kit), never deleted — annex precedent.

This rule composes with Matt's same-day build ruling (*"we build it in — we don't work around
it"*): **build everything attested; remove everything unattested.** The census output becomes
the proposed G1-B scope roster.

---

## 1. Substrate (all in holdings — no acquisition)

| Side | Source | Authority |
|---|---|---|
| Monster (TRUE SOURCE) | Edition-II `.arz` creature + controller records (`~/Games/vendor/grim-dawn-edition-II-20260724/` + prior extraction lanes; TSF6/VDM spatial-field work is precedent) | governs |
| Monster (corroborating) | `agentic_orchestration/research/datamine-acquisition/gd/raw/` — `all_monsters.js` (2,716 entries: resists, classification, specialAttack slots), `all_skills.js`, `monster_adjustments.js`, `engine.js` | secondary — per TRUE-SOURCES discipline, never overrides the `.arz`; divergences FLAGGED not resolved |
| Player-build | corpus.db GD-lane kits (41 + any gdx3 rows), `kit_numeric` / `kit_dossier` / KF-2 rule tables | governs for (P) |
| Mechanism vocabulary | `research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md` (40 states) + gamora's G1-A audit family structure (`agentic_orchestration/gamora/notes/2026-07-25-gd-40-state-coverage-audit.md`) | the row list to census |

## 2. The census

For each row in the mechanism/metric vocabulary — the 40 controller states, the TSF6 spatial
parameters (`ViewDistance`, `MaxPursuitDistance`, `distressCallRange`, `fleeDistance`,
anger rates, etc.), and the monster-stat metric families (resist channels, OA/DA, speeds,
special-attack slots) — report:

1. **Monster-side attestation count** — how many combat-relevant monsters carry it non-default.
   Distinguish three classes: **DATA-ATTESTED** (parameter present/non-default in records),
   **ENGINE-UNIVERSAL** (any monster can enter the state regardless of data — e.g. `Stunned`
   exists wherever CC exists; mark these attested-by-construction), **UNREACHED** (no record
   configures it).
2. **Player-side attestation** — does any GD-lane kit's resolution exercise it (kit fields,
   KF-2 formula anchors, dossier mechanics rows). YES(kit-ids) / NO.
3. **Verdict:** IN (P) / IN (M) / IN (both) / **OUT-BY-ATTESTATION** / NEEDS-JOIN (you can't
   resolve it from data alone — name what's missing; do NOT infer).
4. **Combat-relevance filter note** — how you excluded quest-NPC/cosmetic records; state the
   filter predicate explicitly so it's auditable.

**Known joins to respect:** the parameter↔creature join at width >1 is still inference (D-b);
where your verdict depends on it, mark NEEDS-JOIN rather than banking. The five
banked-inference failures this week are the reason this instruction exists.

## 3. Output

`agentic_orchestration/elrond/notes/2026-07-25-gd-attestation-scope-census.md`:
- The census matrix (one row per metric/state/parameter)
- Headline: how many of the 40 states / how many parameters fall OUT-BY-ATTESTATION
- The proposed G1-B scope roster (IN-list) for Matt's ratification
- Per-family attestation density (feeds build-queue prioritization: a family carried by 60%
  of the bestiary outranks one carried by 3 monsters)
- Divergence flags (.arz vs grimtools), NEEDS-JOIN list

Auto-commit per team discipline (this dispatch is authorization). Findings only.

**Signed:** gandalf, 2026-07-25. Substrate votes; scope follows attestation.
