# Cell-key materialization → elrond handoff (gates gamora dedup)

**From:** gandalf (CANON-STEWARD / SPEC-AUTHOR) · **To:** elrond (execution), via knight-rider (sequencing) · **Date:** 2026-07-13
**Canon:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6.1 (ratified cell key) + §8 (elrond hook) + §3/§3A/§3B (coord definitions).
**Ratified (Matt 2026-07-13):** cell key = **strict 13-tuple, exact-match, first; coarsen with the data second** (§6.1). Completeness gate is OPEN — all 13 coords resolved.

KR: cover-sheet. One build target (elrond), one downstream consumer (gamora). This is the last thing between the matured key and dedup.

---

## What this is
The 13 coordinates are *designed* and CLOSED. They are not yet *runnable* as a key: 4 of 13 coordinate values are not queryable columns, and `cell_key` is not serialized. gamora cannot `GROUP BY` a key that isn't materialized. This brief specifies exactly what elrond builds.

## The 13-coord → source map (verified against corpus 2026-07-13)

| # | Coordinate | Cell-key value source | State |
|---|---|---|---|
| 1 | movement | `canon_engine_key.mob_policy_while_casting` | ✓ column |
| 2 | delivery | `canon_engine_key.delivery_value` | ✓ column |
| 3 | amp | `canon_corpus.amp_val` | ✓ column |
| 4 | geometry | `canon_engine_key.geometry_value` | ✓ column |
| 5a | control-treatment | `canon_engine_key.ctrl_treatment` | ✓ column |
| **5b** | **control-function** | **NEW `ctrl_function`** ← `canon_probe_facts` control family / `mech_note` (§3) | **✗ BUILD** |
| 6 | defense | `canon_engine_key.def_bin` | ✓ column |
| **7** | **economy-model** | **NEW `economy_model`** ← `canon_probe_facts` economy family (§3B) | **✗ BUILD** |
| 8 | proxy | `canon_corpus.proxy_val` | ✓ column |
| 9 | range | `canon_corpus.range_val` | ✓ column |
| 10 | tempo | `canon_corpus.tempo_val` | ✓ column |
| 11 | commit | `canon_corpus.commit_val` | ✓ column |
| **12** | **activation** | **NEW `activation_val`** ← `mech_note` per §3A.1 discriminator | **✗ BUILD** |
| **13** | **dependency** | **NEW `dependency_val`** ← `mech_note` / raw per §3A | **✗ BUILD** |
| aux | resource-name | **NEW `resource_verbatim`** ← `canon_probe_facts` economy family (§3B) | **✗ BUILD** (display; OUT of cell key) |

9 coords are already columns (split across two tables). 4 need building, + 1 display column.

## The 4 new keyed columns — enums

- **`ctrl_function`** ∈ {hard-stop, stun, taunt, fear, blind, knockback, expose, hex, silence, **none**} — element-neutral control functions (§3). `none` for pure-damage kits (ctrl_treatment=damage).
- **`economy_model`** ∈ {spend, cooldown, generator-spender, reserve, self-cost, finite, free} (§3B). Consolidate the raw `economy.model` tokens:
  | raw token | → 7-value | note |
  |---|---|---|
  | spend | spend | |
  | cooldown | cooldown | |
  | meter | generator-spender | carry `{continuous·combo·stack}` as a **sub-annotation, NOT a column fork** (§3B strong hypothesis, split at keying) |
  | reserve | reserve | |
  | channel | reserve | §3B de-conflict (commit=channel lives on #11) |
  | self-cost | self-cost | |
  | recipe / ammo / harvest / charges / corpses | finite | |
  | draft | finite | low-confidence — confirm |
  | proc | free | §3B de-conflict (activation=triggered lives on #12) |
  | other / unknown | free (residual) / `unknown` literal | keep `unknown` literal — conservative |
  **Hybrids** (hatred+discipline, mana+combo…) → key as the **literal compound** (e.g. `generator-spender+spend`). Conservative: a compound never merges with a pure model. Do NOT collapse hybrids.
- **`activation_val`** ∈ {active, triggered} (§3A). Discriminator (§3A.1): intrinsic trigger → `triggered`; gear-granted reactivity → `active`. Tell: `mech_note` "Cast-on-Crit **gem**" = intrinsic → `triggered`; "the **helm** IS the build" = gear → `active`.
- **`dependency_val`** ∈ {one-shot, build→spend, apply→detonate} (§3A).

## The `cell_key` serialization

- **Canonical ordered 13-tuple**, coord order 1→13. #5 contributes **two** slots (treatment, function). Suggested string form: pipe-joined lowercase enum tokens, e.g. `rooted|projectile|spiky|circle|damage|none|glass|spend|solo|ranged|mid|instant|active|one-shot`.
- **Unknown / blank = its own literal value** (`unknown`, `blank`) — never coalesced. This is the "never-merge-on-absence" guarantee (§6.1 Stage 1).
- **Cross-table join:** `cell_key` spans `canon_engine_key` (#1/#2/#4/#5a/#5b-new/#6/#7-new/#12-new/#13-new) ⋈ `canon_corpus` (#3/#8/#9/#10/#11) on `kit_id`. Recommend `cell_key` lives on `canon_engine_key` (the keyed table), populated by the join. elrond's call on storage.

## What it unblocks + sequencing
1. **elrond** builds the 4 columns + `resource_verbatim` + serializes `cell_key`.
2. **gamora** runs dedup v1 = strict `GROUP BY cell_key` (§6.1 Stage 1) → cells + isotope stacks. Representative-selection = the §6 tiebreak (lineage-longevity → recency; losers kept as isotopes, never deleted) — grain-independent, no new decision.
3. **cluster review** (gandalf + gamora + Matt) → **Stage-2 coarsening**: demote texture coords to isotope-status where clusters show over-split. Never-demote core = #2/#5/#8/#1/#12/#13; demotable-with-evidence = #3/#4/#6/#7/#9/#10/#11 (§6.1).

## Guardrails (non-negotiable)
1. Strict exact-match first — **never** pre-coarsen the key (§6.1; split-late beats merge-wrong).
2. Unknown/blank = literal value, never coalesced.
3. #5 = treatment **and** function (two slots).
4. Hybrid economy models keyed as literal compounds, never collapsed.
5. `resource_verbatim` is 1:1-preserved lineage — verbatim from source, **out** of `cell_key`.
