# Kit-to-Star-Sign Assignment — Forward Implementation Spec

> **STATUS:** FORWARD IMPLEMENTATION SPEC (Fable-5 Phase 2 author phase) — design-spec-as-math handoff per Discipline #18. This document is the SOLE input to the implementer. It is written to require zero clarification questions.

**Date:** 2026-06-10
**Author:** gandalf (story-and-design steward)
**Discipline frame:** Discipline #18 (design-spec-as-math); Discipline #40 (scaffold values flagged, § 9); Discipline #41 (substrate-led; § 1.2); Discipline #25 (semantic-layer rep-audit inherited at the corpus-pool filter, § 3.3)

---

## 0. Canonical-source-consultation declaration

Read **in full** before authoring:

1. `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` — the Branch A kit↔star-sign binding architecture (kits bind **1:1** to star-signs; Branch B "multiple kits per sign" is the rejected branch).
2. `agentic_orchestration/gandalf/notes/2026-06-09-3-kit-to-star-sign-canonical-mappings.md` — Phase 1 hand-curation (the 3 authoritative anchor mappings).
3. `agentic_orchestration/dispatches/2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md` — the kit-to-star-sign MVP commission (scope discipline; "rest will be random"; methodology-lock deferral).
4. `agentic_orchestration/elrond/notes/2026-06-09-kit-to-star-sign-mvp-assignment-close.md` — Phase 2 close (implemented MVP state; sidecar pattern decision; the 4 observed RANDOM-tier collisions flagged as methodology hotspot § 3.1).
5. `agentic_orchestration/elrond/scripts/kit_to_star_sign_mvp_assignment.py` — the implemented MVP script (established hash/seed/filter conventions this spec extends).

Read in **targeted sections** (declared honestly as partial reads):

6. `canonical/story/2026-06-05-cosmograph-pivot.md` §§ 9–10 — kit-as-constellation substrate architecture + the 2026-06-09 § 10 amendment ratifying Branch A as a CURRENT load-bearing canonical commitment.
7. `canonical/00-ground-state.md` — workstream status rows for the kit-to-star-sign lineage.

**Empirical inspections** (Discipline #11 — counts verified against live substrate at authoring time, 2026-06-10):

- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml` — 423 entries; `sign_id` values verified globally unique; `cultural_sensitivity.flag_level` distribution verified: 339 `none` / 50 `medium` / 5 `low` / 29 `high` / 0 `restricted`.
- `reincarnated-loadout/public/kit-space/faction_assignments.json` — 37 active kit_ids (16 + 18 + 3 across 3 factions).
- `reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json` — implemented MVP sidecar, `schema_version` "1.0".
- `reincarnated-loadout/public/kit-space/kits/kit_shadow_000007.json` — per-kit record schema (top-level fields enumerated in § 2.1).

---

## 1. Scope and design declarations

### 1.1 What this procedure does

A **deterministic, offline-runnable** procedure (no network, no LLM, no database — file inputs only) that assigns every kit in the active kit corpus to exactly one star-sign from the canonical star-sign set, honoring the 3 hand-curated anchor mappings, enforcing the Branch A 1:1 binding constraint, and emitting the result as a sidecar JSON artifact. Runtime target: completes in < 5 seconds on commodity hardware. Implementation language: Python 3.10+ (stdlib `hashlib`, `json` + `PyYAML` are the only dependencies).

### 1.2 Design declaration — there is deliberately NO similarity metric

The required-contents brief for this spec asks for a "distance/similarity metric and why." The canonically correct answer is: **the metric is uniform (no semantic metric), and this is a locked canonical decision, not an omission.**

- Matt 2026-06-09 verbatim (MVP commission authority line): "for now, we only need 3 kits to map cleanly to starsigns. **the rest will be random**."
- MVP commission § 3.3: "uniform random across the … pool. Do NOT pre-weight by cultural-tradition / element / etc. — random IS random."
- MVP commission § 6: "Methodology lock for semantic-similarity / curated rule-table / hybrid approach (**DEFERRED** to future Pattern B)" — full-corpus semantic mapping is Cycle 15+ territory, gated on vertical-slice playtest evidence.

An implementer (or spec author) who introduces an embedding distance, element-affinity score, or any weighting here would **violate the canon**, pre-committing a methodology Matt explicitly deferred (Discipline #41 — substrate-led: when no semantic methodology has been ratified, uniform random is the honest scaffold). The algorithm class in this spec is therefore dictated NOT by a metric but by the **binding-cardinality constraint** (§ 4). See § 10 for how a future metric slots in without changing the constraint architecture.

### 1.3 Design declaration — injectivity is enforced (corrects the MVP relaxation)

The implemented MVP (elrond Phase 2, 2026-06-09) tolerated many-to-one collisions in its RANDOM tier (4 observed pairs, flagged in its close report § 3.1 as a methodology hotspot, with the fix path named: "constrained random sampling without replacement"). The canonical binding architecture is stricter:

- Tal Rasha recognition record § 0, Branch A: "Each KIT binds **1:1** to a star-sign (**constellation = kit**)."
- Branch B — "Star-signs become CLUSTER anchors (**multiple kits per sign**)" — is the explicitly **rejected** alternative. Tolerating collisions re-introduces Branch B locally.
- `cosmograph-pivot.md` § 10 (CURRENT, Matt-ratified 2026-06-09): Branch A is a load-bearing canonical commitment. The Path L creation mechanism (lasso a constellation → resolve to a kit) requires constellation→kit resolution to be **unique**.

This forward spec therefore enforces an **injective** kit→star-sign mapping: every kit gets exactly one sign; no sign hosts more than one kit. This supersedes the MVP's collision tolerance, which the MVP close itself framed as transitional.

### 1.4 What this procedure does NOT do

- ❌ No kit regeneration; no modification of any file under `reincarnated-loadout/public/kit-space/kits/`; no engine-side (`reincarnated-engine/`) touch of any kind.
- ❌ No semantic/weighted assignment (§ 1.2).
- ❌ No reverse star-sign→kit index emission (derivable at query time; out of scope per MVP commission § 6).
- ❌ No visualization/rendering (downstream drax + mantis seams).
- ❌ No LLM calls anywhere (D7 AI-tell line: assignment happens at curation time, offline).

---

## 2. Input data contracts

Three inputs. All paths below are given relative to the two sibling repos; the implementer wires concrete roots via two constants (see § 5.4 step 0).

### 2.1 Input A — active kit list

**File:** `reincarnated-loadout/public/kit-space/faction_assignments.json`

**Shape (fields consumed are bolded; all others present but ignored):**

```json
{
  "event_id": "kse_20260602_008",        // string — ignored
  "schema_version": "1.0",               // string — ignored
  "factions": [                          // CONSUMED
    {
      "faction_id": "f001",              // string — ignored
      "faction_name": "Iron Ground Crushers",  // string — ignored
      "kit_ids": ["kit_physical_000013", ...]  // CONSUMED — array of strings
    },
    ...
  ]
}
```

**Extraction rule:** the active kit set `K_all` = the union of all `kit_ids` arrays across all entries of `factions`, **sorted ascending** by ordinal (byte-wise) string comparison. At authoring time |K_all| = 37 (verified: 16 + 18 + 3). The procedure must NOT hard-code 37 — it must read the count from the file — but must hard-fail on the validation rules in § 6.

**Why this file is the kit-list source (and not alternatives):** this is the kit list the implemented MVP and the established `faction_assignments.json`/sidecar consumption pattern use; it defines the **active** player-facing corpus that the /forge cosmograph renders. The ~1000-kit substrate-trace and the ~150-kit cycle-14 seasons corpus are NOT the assignment domain — the substrate-trace alone (1000 > 423) makes injective binding impossible, and neither is the corpus the creation-moment surface binds to.

**Per-kit JSON records** (`reincarnated-loadout/public/kit-space/kits/<kit_id>.json`; top-level fields: `schema_version`, `kit_id`, `primary_element`, `cultural_tradition`, `period`, `chain_composition`, `t4_selection`, `supporting_chain`, `skills`, `emergent_kit_concept`, `substrate_trace`, `kit_space_expansion_event_id`, `engine_version`, `engine_version_full`, `generation_timestamp`, `lineage_tags`) are **NOT read by this procedure**. The ONLY kit field that feeds the assignment is the `kit_id` string itself (§ 5.1). This is a consequence of § 1.2: with no semantic metric, no kit features participate.

### 2.2 Input B — the star-sign set

**File:** `reincarnated-collaboration/agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml`

A YAML file whose root is a **list** of 423 star-sign entries (at authoring time) spanning 26 cultural traditions. Fields consumed per entry (all others — `system_metadata`, `visual_representation`, `mythic_narrative`, etc. — are present but ignored):

| Field path | Type | Consumed for |
|---|---|---|
| `sign_id` | string (globally unique; verified) | identity / FK / pool ordering |
| `sign_name.primary` | string | denormalized into output |
| `cultural_tradition.primary_culture` | string | denormalized into output |
| `cultural_sensitivity.flag_level` | string ∈ {`none`,`low`,`medium`,`high`,`restricted`} (may be missing/null) | eligibility filter (§ 3.3) |

**Exactly which star-sign set is being assigned to — and why (the canon has multiple candidate sets):** the assignment target is the **Legolas zodiac substrate corpus** (`corpus.yaml`, N=423, 26 cross-cultural traditions), filtered to its cultural-sensitivity-eligible subset per § 3.3. It is NOT the 88-constellation IAU set, NOT the 12-sign Western zodiac, NOT the 27/28 Vedic Nakshatras — those are *traditions inside* the corpus, not the canonical set. Justification: Branch A itself was **triggered by this corpus** — the architectural branching condition was "N (cross-cultural star-sign count) ≥ ~400," satisfied empirically by this corpus's N=423 (Tal Rasha § 0 + § 5 Trigger 1; ratified at cosmograph-pivot § 10). The corpus IS the substrate the architecture stands on; the 3 hand-curated anchors already resolve to its `sign_id` namespace (`vedic-nakshatra-019`, `vedic-nakshatra-003`, `iau-constellations-040-hercules`).

### 2.3 Input C — hand-curated anchor table

Sourced verbatim from gandalf Phase 1 doc (`2026-06-09-3-kit-to-star-sign-canonical-mappings.md`), as resolved to `sign_id`s by the implemented MVP (verified against the live sidecar). These are **authoritative canonical anchors — the algorithm must respect them, never override them**:

| kit_id | star_sign_id | hand_curated_anchor (output string, verbatim) |
|---|---|---|
| `kit_shadow_000007` | `vedic-nakshatra-019` | `Mula — gandalf doc § 1` |
| `kit_holy_000005` | `vedic-nakshatra-003` | `Krittika — gandalf doc § 2` |
| `kit_physical_000026` | `iau-constellations-040-hercules` | `Hercules — gandalf doc § 3` |

Embed this table as a constant in the implementation (the MVP precedent does the same). The three rows above are the complete table at authoring time; the implementation must support N anchor rows generically.

---

## 3. The representation space

### 3.1 What space the assignment operates in

Because there is no semantic metric (§ 1.2), the assignment operates in **identifier space**, not feature space:

- **Kit representation:** the `kit_id` string (UTF-8 encoded for hashing; ASCII in practice).
- **Star-sign representation:** the `sign_id` string, with the eligible pool totally ordered by ascending ordinal string comparison.
- The "geometry" is the discrete uniform distribution over the eligible pool, indexed by a per-kit cryptographic hash.

There are no embeddings, no vectors, no distances. A kit's "position" is the 64-bit integer derived from its `kit_id` (§ 5.2).

### 3.2 Eligibility filter — the assignable pool

Partition corpus entries by `cultural_sensitivity.flag_level`:

| flag_level | Disposition |
|---|---|
| `none`, `low`, `medium` | **ELIGIBLE** for assignment |
| `high` | **DEFERRED** — excluded from the pool (29 entries at authoring time, pending gandalf cultural-sensitivity review) |
| `restricted` | **EXCLUDED** (0 entries at authoring time) |
| missing / null / unrecognized value | **DEFERRED** (conservative default — never silently include) |

At authoring time this yields an eligible set of **394** entries. The implementation must compute this from the data, not hard-code it.

### 3.3 Authority for the filter

This filter policy is inherited verbatim from the MVP commission § 3.4 + the implemented MVP (elrond close § 2.2) and is itself an exercise of Discipline #25 (rep-audit at the corpus-pool layer). The constants must be implemented as named, single-point-of-change sets (`ELIGIBLE_FLAG_LEVELS = {"none","low","medium"}` etc.) because the 29 deferred entries may be promoted after gandalf review, after which a deterministic re-run propagates the expansion.

---

## 4. Constraints — cardinality and what it dictates

### 4.1 The binding constraint (canon)

Branch A (Tal Rasha § 0; cosmograph-pivot § 10, CURRENT): **kit binds 1:1 to star-sign; constellation = kit.** Formally, the assignment is a function

> f : K → S_eligible,  f **injective**

where K is the active kit set and S_eligible the eligible pool. Every kit has exactly one sign (totality); no two kits share a sign (injectivity). Signs without a kit are permitted and expected (|S_eligible| ≫ |K|): unassigned signs remain ambient night-sky substrate.

### 4.2 What the constraint dictates about algorithm class

Injectivity means the assignment is a **without-replacement matching problem**, NOT a set of independent per-kit draws. The MVP's per-kit independent hash draw (`h(kit) mod pool_size`, collisions allowed) is structurally incapable of guaranteeing injectivity — with 34 independent draws from 394 the birthday bound makes collisions *expected* (≈1.5; the MVP observed 4). Any correct algorithm must serialize claims against a shared "taken" set (equivalently: sample without replacement / build a bipartite matching). This spec uses deterministic open addressing (§ 5.2): each kit hashes to a base index in the ordered pool and claims the first unclaimed sign at-or-after it (cyclically). This preserves the MVP's established per-kit-hash convention (same hash construction, same salt-bumpability) while restoring injectivity, and degrades gracefully: a kit's assignment shifts only if its probe path intersects another kit's claim.

### 4.3 Anchors interact with the constraint

The 3 anchors are part of f and count against injectivity: their signs are pre-claimed and **removed from the random pool before any hashing happens** (§ 5.4 step 4). Anchor signs must be pairwise distinct (validated; § 6).

---

## 5. The algorithm

### 5.1 Definitions

- `SALT` — the fixed ASCII string `kit-to-star-sign-injective-v2-2026-06-10` (scaffold value; § 9).
- `A` — the anchor table of § 2.3: a list of (kit_id, star_sign_id, anchor_string) triples. `A_kits` = its kit_ids; `A_signs` = its sign_ids.
- `K_all` — active kit_ids per § 2.1, sorted ascending (ordinal string order). `K_rand` = `K_all` minus `A_kits`, preserving ascending order.
- `E` — eligible corpus entries per § 3.2.
- `P` — the random pool: `sorted([e.sign_id for e in E if e.sign_id ∉ A_signs])`, ascending ordinal string order. `n = |P|`. (At authoring time n = 394 − 3 = **391**.)

### 5.2 The math

For each kit k ∈ K_rand define the base index

> **h(k) = int( SHA256( UTF8(SALT ‖ "::" ‖ k) ).hexdigest()[0:16], 16 ) mod n**

i.e., SHA-256 of the string `SALT + "::" + kit_id`, take the **first 16 hexadecimal characters** of the lowercase hex digest (= the most-significant 8 bytes, big-endian), parse as an unsigned 64-bit integer, reduce mod n. (This is bit-identical to the MVP script's `deterministic_pick_index`; the `"::"` separator is load-bearing — keep it.)

Process kits **in ascending K_rand order**, maintaining a claimed-set C (initialized to A_signs… formally C ⊆ pool-claims; since P already excludes A_signs, initialize C = ∅ over P). For kit k:

> **assign(k) = P[ (h(k) + j*) mod n ]**, where **j\* = min { j ≥ 0 : P[(h(k)+j) mod n] ∉ C }**

then add assign(k) to C. This is open addressing with linear probing, step +1, cyclic wraparound.

**Injectivity guarantee:** each claim removes one slot; since |K_rand| ≤ n is validated up front (§ 6 E1), j* always exists and every assigned sign is distinct. ∎

**Determinism guarantee:** the output is a pure function of (faction_assignments.json content, corpus.yaml content, the anchor table, SALT, the flag-level filter sets). No clock, RNG state, dict-iteration order, filesystem order, or environment value participates. Both sort operations use ordinal (codepoint/byte) string comparison — do NOT use locale-aware collation. Re-running on identical inputs must produce a byte-identical `assignments` array.

**Tie-breaking rule (explicit):** two kits whose base indices collide (or whose probe paths intersect) are resolved by **kit processing order = ascending kit_id**: the lexicographically earlier kit claims the contested slot; the later kit probes onward (+1 cyclic). There is no other tie condition in the algorithm — the hash is total and the probe order is total.

### 5.3 Why this construction (and not alternatives)

- **vs. independent per-kit draws (MVP method):** cannot guarantee injectivity (§ 4.2).
- **vs. seeded global Fisher-Yates shuffle of P, assigning K_rand[i] → shuffled[i]:** deterministic and injective, but maximally brittle — *any* change to the pool or kit list reshuffles *every* assignment. Open addressing localizes churn to intersecting probe paths.
- **vs. Hungarian / optimal bipartite matching:** requires a cost matrix, i.e., a semantic metric — canonically deferred (§ 1.2). When a metric lands (Cycle 15+), the constraint architecture of § 4 is unchanged and the assignment step is swapped for a balanced-assignment solver (§ 10).
- **Accepted trade-off (flagged honestly):** under injectivity, perfect per-kit independence is impossible. Adding/removing a kit or pool entry can shift other kits' assignments where probe paths intersect. RANDOM-tier assignments are declared **scaffold-stable, not contract-stable** (§ 9); only HAND_CURATED anchors are contract-stable.

### 5.4 The procedure (normative step order)

0. **Configuration constants:** two repo-root paths (meta-repo + loadout repo), the three input paths of § 2, the output path of § 7, `SALT`, the anchor table, the three flag-level sets.
1. **Load corpus** (YAML root must be a list — else fail E6). Build `sign_index : sign_id → entry`; fail on any duplicate `sign_id` (E7) or missing `sign_id` (skip-with-no-index is NOT allowed in v2 — a corpus entry lacking `sign_id` is a hard failure E7).
2. **Load kit list**; extract + sort `K_all` (§ 2.1); fail on duplicates or empty/non-string kit_ids (E4, E5).
3. **Partition corpus** into eligible / deferred / excluded per § 3.2; record the three counts.
4. **Validate anchors** (each rule's failure is fatal, § 6 E8–E11): every anchor kit_id ∈ K_all; every anchor sign_id ∈ sign_index; every anchor sign's flag_level ∈ ELIGIBLE_FLAG_LEVELS; anchor kit_ids pairwise distinct; anchor sign_ids pairwise distinct.
5. **Build P** (eligible sign_ids minus A_signs, sorted ascending); compute n; **fail if |K_rand| > n (E1) or n = 0 (E2).**
6. **Assign:** anchors first (method `HAND_CURATED`, anchor string attached), then each k ∈ K_rand in ascending order per § 5.2 (method `RANDOM`, anchor null).
7. **Post-conditions (assert, fail on violation):** |assignments| = |K_all|; HAND_CURATED count = |A|; all 37 (i.e., |K_all|) assigned star_sign_ids pairwise distinct; every RANDOM sign ∈ P.
8. **Emit** the sidecar per § 7. Exit 0. On ANY validation/assert failure: write NOTHING (no partial output, do not touch the existing sidecar), print the specific failure to stderr, exit non-zero.

---

## 6. Edge cases (each row is normative)

| # | Condition | Required behavior |
|---|---|---|
| E1 | **More kits than eligible signs** (|K_rand| > n) — e.g., someone points the script at the 1000-kit substrate-trace, or sensitivity review shrinks the pool below the kit count | HARD FAIL, exit non-zero, no output. Injectivity is canon (§ 4.1); silently degrading to many-to-one re-opens rejected Branch B. Error message must state both counts. |
| E2 | **Empty eligible pool** (n = 0) or empty corpus | HARD FAIL. |
| E3 | **More signs than kits** (the normal case; 391 ≫ 34) | Not an error. Unassigned signs are simply absent from the output; they remain ambient sky. No "unassigned signs" list is emitted (reverse mapping out of scope, § 1.4). |
| E4 | **Duplicate kit_id** across or within factions | HARD FAIL (a kit assigned twice would silently violate totality/injectivity accounting). |
| E5 | **Empty / null / non-string kit_id** | HARD FAIL. Note on "kits with no valid representation": the only representation this procedure consumes is the kit_id string (§ 3.1); a kit whose kit_id is a non-empty string is *always* validly representable. "Degenerate/empty feature vector" cases are vacuous here by construction — there are no feature vectors (§ 1.2). The only degenerate-representation case is a malformed kit_id, handled by this rule. |
| E6 | **corpus.yaml root is not a list** / unparseable / file missing | HARD FAIL. |
| E7 | **Duplicate or missing `sign_id`** in corpus | HARD FAIL. |
| E8 | **Anchor kit_id not in K_all** | HARD FAIL (anchor table and kit list have drifted; human attention required). |
| E9 | **Anchor sign_id not in corpus** | HARD FAIL. |
| E10 | **Anchor sign flag_level ∉ {none, low, medium}** (or missing) | HARD FAIL with message directing surface-to-gandalf (a sensitivity re-flag of an anchor sign is a design event, not a data event). |
| E11 | **Two anchors share a sign_id, or one kit appears twice in the anchor table** | HARD FAIL (anchor-layer injectivity violation). |
| E12 | **Entry missing `sign_name.primary` or `cultural_tradition.primary_culture`** for an *assigned* sign | Emit empty string `""` for the missing denormalized field (matches MVP behavior); do NOT fail. These are display denormalizations, not identity. |
| E13 | **Missing/unknown `cultural_sensitivity.flag_level`** | Treat as DEFERRED — excluded from pool (§ 3.2). Never fail, never include. |

---

## 7. Output schema

### 7.1 Where the result lands

**File (the complete, only output):** `reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json`

**Clarification on "season-output JSON":** the assignment result does NOT land in the engine's season-output JSON, and the implementer must not touch any engine output file. The canonical landing zone for kit-level metadata on the player-facing surface is the **kit-space sidecar family** (`faction_assignments.json` precedent, cycle-18 Issue 5A; ratified for star-signs by elrond close § 2.1, which explicitly considered and REJECTED per-kit-JSON and engine-side placement). The kit-space directory is the season-corpus consumption surface that drax /forge fetches; this sidecar is that surface's assignment artifact. Overwriting the existing v1.0 sidecar at this path is the intended behavior (it is reproducible from sources by design).

### 7.2 Exact schema (field names and types; top-level key order as listed)

```json
{
  "schema_version": "1.1",                          // string — bumped from "1.0": injectivity semantics + methodology fields added
  "artifact_kind": "kit_star_sign_assignments",     // string — fixed literal
  "generated_at_utc": "<ISO-8601 UTC timestamp>",   // string — the ONLY non-deterministic field
  "spec": "agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md",  // string — fixed literal (this doc)
  "phase1_hand_curation_doc": "agentic_orchestration/gandalf/notes/2026-06-09-3-kit-to-star-sign-canonical-mappings.md",  // string — fixed literal
  "source_corpus": "agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml",  // string — fixed literal (meta-repo-relative)
  "source_kit_list": "reincarnated-loadout/public/kit-space/faction_assignments.json",  // string — fixed literal
  "methodology": {
    "hand_curated_overrides_count": 3,              // integer — computed, not hard-coded
    "random_assignment_count": 34,                  // integer — computed
    "injectivity": "ENFORCED",                      // string — fixed literal (v1.0 lacked this field; Branch A 1:1 binding)
    "random_seed_method": "sha256(salt + '::' + kit_id)[:16hex] mod len(eligible_pool_minus_anchor_signs_sorted_by_sign_id), linear probe +1 cyclic on claimed slots, kits processed in ascending kit_id order",  // string — fixed literal
    "random_seed_salt": "kit-to-star-sign-injective-v2-2026-06-10",  // string — MUST equal SALT
    "cultural_sensitivity_audit": {
      "eligible_pool_size": 394,                    // integer — computed (eligible entries, BEFORE anchor-sign removal)
      "random_pool_size": 391,                      // integer — computed (n; AFTER anchor-sign removal) — NEW in 1.1
      "deferred_for_gandalf_review_count": 29,      // integer — computed
      "excluded_count": 0,                          // integer — computed
      "eligible_flag_levels": ["low", "medium", "none"],   // array<string> — sorted
      "deferred_flag_levels": ["high"],             // array<string> — sorted
      "excluded_flag_levels": ["restricted"]        // array<string> — sorted
    }
  },
  "assignments": [                                  // array — EXACTLY one record per kit in K_all, ordered ascending by kit_id
    {
      "kit_id": "kit_earth_000004",                 // string
      "star_sign_id": "<sign_id>",                  // string — FK into corpus.yaml
      "star_sign_name": "<sign_name.primary>",      // string — denormalized ("" if missing, E12)
      "star_sign_tradition": "<cultural_tradition.primary_culture>",  // string — denormalized ("" if missing)
      "star_sign_assignment_method": "RANDOM",      // string enum — "HAND_CURATED" | "RANDOM" (exactly these two values)
      "hand_curated_anchor": null                   // string | null — the § 2.3 anchor string for HAND_CURATED; null for RANDOM
    }
  ]
}
```

Serialization: JSON, 2-space indent, `ensure_ascii=False` (UTF-8), trailing newline. (Matches MVP emission so diffs against v1.0 are clean.)

All integer counts above show authoring-time expected values for the current substrate state; the implementation computes them.

### 7.3 Downstream-consumer compatibility

The per-assignment record shape is **unchanged from v1.0** — drax /forge and mantis WS1 consumers that read `assignments[]` records require no change. New fields are additive at the `methodology` level only.

---

## 8. Acceptance criteria and smoke test

### 8.1 Self-verification checklist (implementer must verify ALL)

| # | Criterion | How to verify |
|---|---|---|
| 1 | Output file exists at § 7.1 path; parses as JSON; all § 7.2 fields present with stated types; `schema_version == "1.1"` | jq / schema check |
| 2 | `assignments` has exactly one record per kit_id in faction_assignments.json (37 at current state); array sorted ascending by kit_id; no extra records | jq length + set comparison |
| 3 | The 3 anchors are EXACT: `kit_shadow_000007 → vedic-nakshatra-019`, `kit_holy_000005 → vedic-nakshatra-003`, `kit_physical_000026 → iau-constellations-040-hercules`; each `star_sign_assignment_method == "HAND_CURATED"` and `hand_curated_anchor` equals the § 2.3 string verbatim | jq select |
| 4 | **INJECTIVITY:** all `star_sign_id` values in `assignments` are pairwise distinct (37 records → 37 distinct signs). This is the load-bearing criterion v1.0 failed (4 collision pairs); a v1.1 output with ANY duplicate sign is a FAIL | `jq '[.assignments[].star_sign_id] | length == (. | unique | length)'` |
| 5 | Every RANDOM-method `star_sign_id` resolves to a corpus entry with `flag_level ∈ {none, low, medium}` and is none of the 3 anchor signs | script spot-check against corpus |
| 6 | **Determinism:** two consecutive runs produce byte-identical files except `generated_at_utc` | run twice + diff |
| 7 | `star_sign_name` / `star_sign_tradition` match the corpus entry's `sign_name.primary` / `cultural_tradition.primary_culture` for ≥ 5 spot-checked records | manual spot-check |
| 8 | Zero files modified other than the output sidecar — in particular nothing under `kits/`, nothing in `reincarnated-engine/` | `git status` in both repos |
| 9 | E1 hard-fail verified: run against a synthetic kit list larger than the pool (e.g., 400 fabricated kit_ids) → non-zero exit, no output written | synthetic test |
| 10 | E11 hard-fail verified: duplicate a sign_id in a copied anchor table → non-zero exit | synthetic test |
| 11 | Fixture vectors of § 8.2 reproduce exactly | direct comparison |

### 8.2 Reference fixture vectors (computed at authoring time against the live substrate; Discipline #11)

Valid for the substrate state at this spec's commit (corpus 423/394 eligible; 37 kits; SALT as in § 5.1; n = 391). If the corpus or kit list has changed when the implementer runs, fixtures 3–6 may legitimately differ — fixtures 1–2 (pure hash) never change.

1. **Hash fixture:** `SHA256("kit-to-star-sign-injective-v2-2026-06-10::kit_earth_000004")` hex digest begins `95b0730eda58f9f5` → h = 10786247615182338549 → h mod 391 = **234**.
2. **Hash fixture:** same construction for `kit_wind_000006` → digest begins `cbc5413c214d20aa` → mod 391 = **4**.
3. **Pool fixture:** P[0] = `andean-001`; P[390] = `western-zodiac-012`; n = 391.
4. **Assignment fixtures (RANDOM):** `kit_earth_000004 → japanese-junishi-002`; `kit_earth_000005 → mayan-tzolkin-011`; `kit_earth_000006 → chinese-zodiac-005`; `kit_wind_000006 → andean-005`.
5. **Probe fixture (tie-break exercised):** `kit_physical_000016` and `kit_physical_000028` share base index 90 (`chinese-xiu-021`). `kit_physical_000016` sorts earlier → claims `chinese-xiu-021`; `kit_physical_000028` probes j=1 → claims `chinese-xiu-022`. Exactly one probe event occurs in the full authoring-time run.
6. **Distinctness fixture:** full run yields 37 distinct star_sign_ids.

### 8.3 Smoke test (narrative)

Run the script twice from a clean checkout. Confirm: exit 0 both times; output diff is empty except `generated_at_utc`; checklist items 1–7 pass; fixture vectors §8.2 reproduce. Then run the two synthetic hard-fail tests (items 9–10). Total smoke-test time budget: under 10 minutes.

---

## 9. Scaffold values and pending decisions (Discipline #40 — explicit flags)

Every value below is a **scaffold, not a locked canonical decision**:

| Scaffold | Status |
|---|---|
| `SALT = "kit-to-star-sign-injective-v2-2026-06-10"` | Scaffolded by this spec. Any fixed ASCII string is algorithmically valid; bumping it is the sanctioned "fresh randomization" mechanism (MVP precedent). Must be recorded in output. |
| `schema_version = "1.1"` | Scaffolded (additive-change minor bump). If elrond/jack-ryan schema governance prefers "2.0", a one-line change; record shape is unchanged either way. |
| Eligibility flag policy (`high` deferred) | Inherited from MVP, pending gandalf review of the 29 high-flag entries. Promotion → pool grows → RANDOM assignments may shift on re-run (anchors unaffected). |
| RANDOM-tier assignments themselves | Scaffold by canon: Cycle 15+ Pattern B replaces uniform-random with ratified semantic methodology, gated on vertical-slice playtest evidence (MVP commission § 6; elrond close § 3.5). RANDOM assignments are scaffold-stable, NOT contract-stable (§ 5.3). |
| Linear-probe step (+1 cyclic) | Scaffolded design choice by this spec (justified § 5.3); any deterministic total probe order would be valid; +1 cyclic is chosen for simplicity and specified normatively so implementations agree. |

**NOT scaffolds (locked canon):** the 3 anchor mappings (§ 2.3); the 1:1 injective binding (§ 4.1, Branch A ratified at cosmograph-pivot § 10); no-semantic-metric-at-this-stage (§ 1.2, Matt 2026-06-09 verbatim); the corpus as the star-sign set (§ 2.2); the sidecar landing zone (§ 7.1).

---

## 10. Forward-compatibility note (for the eventual semantic upgrade)

When Cycle 15+ Pattern B ratifies a semantic methodology, the constraint architecture of this spec survives intact: the problem becomes **minimum-cost injective bipartite assignment** (anchors fixed; remaining kits matched to distinct eligible signs minimizing total semantic cost — Hungarian algorithm or equivalent), and only § 5.2's claim rule is replaced. Input contracts (§ 2), eligibility filter (§ 3), cardinality constraint (§ 4), output schema (§ 7), and acceptance criteria 1–3/5–8 (§ 8) carry forward unchanged. Implementers should keep pool construction, anchor validation, and emission separable from the claim rule accordingly.

---

## 11. Sign-off

**Authored:** gandalf, 2026-06-10, as the Fable-5 Phase 2 author-phase artifact (design-handoff-fidelity workstream): a forward implementation spec for deterministic, offline kit-to-star-sign assignment.

**Anchor docs:** Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 (Branch A 1:1 binding); cosmograph-pivot § 10 amendment 2026-06-09 (Branch A ratified CURRENT); elrond kit-to-star-sign MVP commission + Phase 2 close 2026-06-09 (established conventions; collision hotspot this spec corrects); gandalf Phase 1 hand-curation 2026-06-09 (the 3 anchors).

**Composition:** preserves all prior canonical commitments; supersedes only the MVP's transitional collision tolerance (elrond close § 3.1, which itself named this fix path). No engine touch; no regeneration; D7 AI-tell line preserved (offline curation-time assignment, no LLM).

**End of spec.**
