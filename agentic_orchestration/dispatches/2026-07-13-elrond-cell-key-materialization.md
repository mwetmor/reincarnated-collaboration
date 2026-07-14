# Dispatch — 2026-07-13 — elrond — Materialize the ratified cell key (gates gamora dedup)

**From:** knight-rider (sequencing)
**To:** elrond (data steward — `agentic_orchestration/research/curated/corpus.db` + curation seam)
**Spec author:** gandalf (CANON-STEWARD) — full build spec at `agentic_orchestration/gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md`
**Approved by:** Matt 2026-07-13 — cell key RATIFIED (strict-13-tuple, exact-match, first; coarsen with the data second), register §6.1. Completeness gate S4 is OPEN (all 13 Class-A coords resolved). This is execution of a Matt-ratified canon spec within elrond's stewarded corpus DB — routes under the standing data-steward mandate.
**Pattern:** B (schema + data curation on corpus.db; own session memory; ~half a day)
**Independence:** Orthogonal to the loot BUILD gate (batch-2 close + gauntlet redesign) and to race-emission (E10 Leg 3). This is data/schema, not sim compute — it waits on neither.

## ⛔ SOLE-WRITER PRECONDITION (read first)

`corpus.db` is untracked (no git signal on writes). The prior gandalf-prompted elrond session (Wave-A returns Fold 1 + mint-dossier Fold 2) has **landed and closed** — verified by KR: 9 mint kits carry `era_year`, all 9 are keyed into `canon_engine_key`, `le-ring-of-shields` re-keyed. **Do NOT launch this dispatch while any other elrond session is live on corpus.db** — that reproduces the 2026-07-11 double-writer anti-pattern the Gate-1 note flagged. One writer at a time on corpus.db. Confirm no concurrent elrond session before you write.

## Context

The 13 kit-identity coordinates are *designed and CLOSED* (register §2/§3/§3A/§3B; #7 economy + #8 summon-economy folded this session, commits `4ae22901` + `fdfe220c`). Matt then ratified the **cell/dedup key** itself: strict 13-tuple, exact-match, first — then coarsen with the cluster data (§6.1). But the key is **not yet runnable**: 4 of 13 coordinate values are not queryable columns, and `cell_key` is not serialized. gamora cannot `GROUP BY` a key that isn't materialized. This dispatch is the **single execution gate** between the ratified key and first dedup. Downstream (gamora dedup v1) is registered as a follow-on, HARD-BLOCKED on this dispatch (see companion doc `2026-07-13-gamora-cell-key-dedup-v1-BLOCKED.md`).

## Required reading before starting

- **The build spec (primary):** `agentic_orchestration/gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md` — the 13-coord→source map, the 4 new columns + enums, the raw-economy-token→7-value consolidation map, `resource_verbatim`, and the `cell_key` serialization contract. **Build straight off this.**
- **Canon backing:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — §6.1 (ratified key — strict-first, never pre-coarsen), §7 (presentation contract — your row + gamora's), §3/§3A/§3A.1/§3B (coord definitions + the activation discriminator + the economy-model taxonomy).
- ADR-004 (MIGRATION) / ADR-006 (read-only-by-default — these writes are to YOUR stewarded corpus DB, in-scope; NOT engine production telemetry).

## The build (per the handoff spec — this is the authoritative summary, not a re-derivation)

### The 4 new keyed columns on `canon_engine_key` (+ 1 display column)

All read from tables already present. `mech_note` lives on `canon_corpus`; control/economy families live on `canon_probe_facts` (478 rows each, confirmed present).

- **`ctrl_function`** ∈ {hard-stop, stun, taunt, fear, blind, knockback, expose, hex, silence, **none**} — element-neutral control functions (§3). `none` for pure-damage kits (`ctrl_treatment='damage'`). Source: `canon_probe_facts` control family / `mech_note`.
- **`economy_model`** ∈ {spend, cooldown, generator-spender, reserve, self-cost, finite, free} (§3B). Source: `canon_probe_facts` economy family. **Consolidate the raw `economy.model` tokens per the handoff map** (meter→generator-spender carrying `{continuous·combo·stack}` as a **sub-annotation, not a column fork**; channel→reserve; proc→free; recipe/ammo/harvest/charges/corpses→finite; draft→finite *low-confidence, confirm*; other/unknown→`unknown` literal). **Hybrids** (hatred+discipline, mana+combo…) → key as the **literal compound** (e.g. `generator-spender+spend`); never collapse a hybrid into a pure model.
  - **⚠ KR build-note (distinctness):** `economy_model` is a **NEW column**. The existing `canon_engine_key.econ_status` / `econ_meter_type` columns are separate provenance — **do not overwrite them.** Register §7 explicitly: economy-model is "distinct from the existing econ_status."
- **`activation_val`** ∈ {active, triggered} (§3A). Discriminator §3A.1: intrinsic trigger → `triggered`; gear-granted reactivity → `active`. Tell in `mech_note`: "Cast-on-Crit **gem**" = intrinsic → `triggered`; "the **helm** IS the build" = gear → `active`.
- **`dependency_val`** ∈ {one-shot, build→spend, apply→detonate} (§3A). Source: `mech_note` / raw per §3A.
- **`resource_verbatim`** (display; **OUT of the cell key**) — 1:1-preserved lineage, verbatim from source (`canon_probe_facts` economy family). Not coalesced.

### Serialize `cell_key`

- **Canonical ordered 13-tuple**, coord order 1→13. **#5 contributes TWO slots** (treatment, function). Pipe-joined lowercase enum tokens, e.g.
  `rooted|projectile|spiky|circle|damage|none|glass|spend|solo|ranged|mid|instant|active|one-shot`.
- **Unknown / blank = its own literal value** (`unknown`, `blank`) — **never coalesced.** This is the never-merge-on-absence guarantee (§6.1 Stage 1).
- **Cross-table join:** `cell_key` spans `canon_engine_key` (#1 mob_policy_while_casting / #2 delivery_value / #4 geometry_value / #5a ctrl_treatment / #5b ctrl_function-new / #6 def_bin / #7 economy_model-new / #12 activation_val-new / #13 dependency_val-new) ⋈ `canon_corpus` (#3 amp_val / #8 proxy_val / #9 range_val / #10 tempo_val / #11 commit_val) on `kit_id`. **Store `cell_key` on `canon_engine_key`** (the keyed table), populated by the join — your call on storage mechanism (materialized column vs. view), but gamora needs a stable `GROUP BY cell_key` target.
- **⚠ KR build-note (row scope):** serialize `cell_key` for **`row_class='combat-kit'` rows** (470 confirmed) — these are the dedup population. `system-record` rows (17) are out of the combat denominator (row_class discipline) — leave their `cell_key` NULL or excluded, your call, but state which. This keeps gamora's Stage-1 `GROUP BY` clean.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**Round-trip: not applicable** — no engine cross-seam contract is touched. New columns land on `canon_engine_key` inside elrond's stewarded curation DB (`corpus.db`); the sole downstream consumer is gamora's dedup, which reads `cell_key` within the curation/analysis layer. This is **NOT** the star-lord engine-telemetry boundary (ADR-004) — no engine schema, no fight_log/loadout/export packet field changes. No MIGRATION.md against star-lord required. If, contrary to this assessment, you find a star-lord-boundary column implicated, STOP and flag to KR before writing.

## Scope

- [ ] `ctrl_function` column built + populated (enum-validated; `none` for damage kits).
- [ ] `economy_model` column built + populated via the consolidation map; hybrids as literal compounds; `econ_status`/`econ_meter_type` left intact; `draft` and `other/unknown` dispositions documented.
- [ ] `activation_val` column built + populated via §3A.1 discriminator.
- [ ] `dependency_val` column built + populated.
- [ ] `resource_verbatim` display column built + populated (1:1, out of cell key).
- [ ] `cell_key` serialized (13-tuple, #5 = two slots, unknown/blank = literal) for combat-kit rows; join across the two tables on `kit_id`.
- [ ] Smoke: `SELECT count(DISTINCT cell_key), count(*) FROM <combat-kit population>` runs; report cell count + total + how many rows carry any `unknown`/`blank` slot (the never-merge-on-absence footprint).
- [ ] Round-trip disposition stated (not-applicable justification above confirmed, or MIGRATION note if a boundary column is implicated).
- [ ] Auto-commit curation artifacts; **NO push** (Matt-gated per ADR-006). Note: `corpus.db` itself is untracked — commit any schema-def/migration scripts + a curation log, not the binary, unless the seam convention says otherwise.

## Acceptance criteria

- [ ] All 4 keyed columns + `resource_verbatim` populated with enum-valid values across the combat-kit population; no NULLs except where the source is genuinely absent (→ `unknown`/`blank` literal, per guardrail).
- [ ] `cell_key` is a stable, `GROUP BY`-able serialization for the 470 combat-kit rows; #5 verifiably contributes both treatment and function slots.
- [ ] Guardrails honored (all 5 from the handoff): strict exact-match, never pre-coarsen; unknown/blank = literal, never coalesced; #5 = two slots; hybrid economies as literal compounds; `resource_verbatim` out of the key.
- [ ] Completion record states: the cell-count vs row-count (the first read of the collapse structure), the `draft`/`other`/`unknown` economy dispositions, the row-scope decision for system-records, and the round-trip disposition.

## Out of scope (explicit non-goals)

- **Do NOT run the dedup.** You materialize + serialize; gamora runs Stage-1 `GROUP BY cell_key`. (Separate BLOCKED dispatch.)
- **Do NOT coarsen / project the key.** Strict 13-tuple only — Stage-2 coarsening is a later reviewed pass (gandalf + gamora + Matt), NOT this dispatch (§6.1: split-late beats merge-wrong).
- **Do NOT overwrite `econ_status` / `econ_meter_type`** — `economy_model` is additive.
- No changes to engine telemetry / production systems (star-lord seam; Matt-gated).
- No representative-selection or isotope-stack computation — that rides gamora's dedup on the §6 tiebreak (grain-independent).

## Open questions for the agent to resolve (document your call)

- Storage of `cell_key`: materialized column on `canon_engine_key` vs. a view. Pick the one that gives gamora a stable `GROUP BY` target; state which.
- `draft`→finite is low-confidence in the handoff — confirm against the actual `draft`-tokened rows and document.
- `system-record` row `cell_key`: NULL vs. excluded — state which and why.

## References

- Build spec: `gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md`
- Canon: `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6.1, §7, §3/§3A/§3A.1/§3B
- Ratification: register commit `fdfe220c` (cell key RATIFIED + elrond materialization spec)
- Downstream (BLOCKED on this): `dispatches/2026-07-13-gamora-cell-key-dedup-v1-BLOCKED.md`

## Completion record
_(append: each new column's populated-count + null/unknown footprint; the cell-count vs 470-row-count; economy `draft`/`other`/`unknown` dispositions; system-record scope call; `cell_key` storage mechanism; smoke output; round-trip disposition; commit hash(es); any spec gap found + flagged to gandalf)_

---

### COMPLETE — elrond — 2026-07-13 — **LANDED**

**Sole-writer confirmed** before write (1 elrond session = this one; no concurrent corpus.db writer). All 8 scope items ✅. Full detail: `agentic_orchestration/research/curated/corpus-cell-key-log-2026-07-13.md`; MIGRATION `v2.3`; script `scripts/corpus_cell_key_materialize_2026_07_13.py` (idempotent, D6 slot 4/4).

**Headline: 470 combat-kit rows → 457 distinct cells** (strict-13 exact-match — first read of the collapse structure). Shallow, as a strict key should be. 49 rows carry ≥1 `unknown`/`blank` literal slot (never-merge-on-absence footprint). 12 multi-kit cells absorbed 13 rows (genuine isotope pairs: Cyclone/Whirlwind, shield-charge cross-game, PoE trap trio, etc.).

**Columns built (all `canon_engine_key`, additive, combat-kit populated / system-record NULL):**
| column | in key? | populated / 470 | null/unknown footprint |
|---|---|---|---|
| `ctrl_function` #5b | yes | 470 | 7 `unknown` (mint no-probe); `silence`=0 (reserved, no source token) |
| `economy_model` #7 | yes | 470 | 43 `unknown` (28 raw-`other`, 7 no-probe, 6 raw-`unknown`, 2 `draft`); 2 literal compounds |
| `activation_val` #12 | yes | 470 | 7 `unknown` (empty mech_note) — 87 triggered / 376 active |
| `dependency_val` #13 | yes | 470 | 7 `unknown` — 359 one-shot / 60 apply→detonate / 44 build→spend |
| `resource_verbatim` | **NO** (display) | 461 | 1:1 verbatim, never coalesced |
| `cell_key` | serialization | 470 | 17 system-record NULL |

**Smoke:** `SELECT count(DISTINCT cell_key), count(*) FROM canon_engine_key WHERE row_class='combat-kit' AND cell_key IS NOT NULL;` → **457 | 470**. 49 rows carry an unknown/blank slot.

**Economy dispositions:**
- **`draft` (2 rows) → SPEC GAP flagged; kept `unknown`, NOT `finite`.** The 2 draft rows are roguelite **draft/offer-pool build-SELECTION** economies (VS-style — "choosing what NOT to take" / "starts with the draft position"), not consumable-input `finite`. Folding to `finite` would wrong-merge. Candidates for gandalf: new `draft` value / `free` residual / confirm finite. **Did not guess past it.**
- **`other` (28 on combat-kit) → mostly `unknown`, only genuine no-economy (`none`/`stamina/none` resource) → `free`.** Conservative never-invent.
- **`unknown` (6 raw) → `unknown`** literal.

**system-record scope call: NULL (not excluded-by-sentinel), combat-kit only.** 17/17 system-records have the 4 new cols + cell_key NULL. NULL (not a sentinel string) so a naive whole-table `GROUP BY` cannot mint a phantom NULL-cell; gamora filters `row_class='combat-kit' AND cell_key IS NOT NULL`.

**cell_key storage mechanism: MATERIALIZED COLUMN** (not a view) — stable index-able `GROUP BY` target frozen at materialization; a view would re-execute the two-table join per read + expose gamora to mid-flight coord edits. Re-run the idempotent script to re-materialize if any of the 13 source coords change. #5 = TWO slots verified (all 470 rows = 14 pipe-fields).

**Round-trip disposition: NOT APPLICABLE — confirmed.** All writes additive on elrond-owned corpus.db; no star-lord engine-telemetry boundary column implicated; no STOP-and-flag triggered. No MIGRATION.md against star-lord required.

**Guardrails (all honored):** strict-first (never pre-coarsened) · unknown/blank = literal (never coalesced) · #5 = 2 slots · hybrids as literal compounds (`spend+finite`, `spend+cooldown`) · `resource_verbatim` out of key · `economy_model` additive (`econ_status`/`econ_meter_type` untouched — 463 each) · dedup NOT run.

**Reproducibility:** idempotent (re-run → byte-identical `shasum 9e158f59…`); full clean rebuild from scratch (base → s1 → fold12 → this) reproduces the same hash + 457/470 smoke.

**Spec gaps flagged to gandalf:** (1) `draft` economy model — build-selection economy, not consumable-finite (kept `unknown`, awaiting ruling). (2) minor — `dependency_val` text-derivation runs a touch above the §5 "~70" estimate (104); a Stage-2 refinement candidate, not a gap.

**Downstream:** gamora dedup v1 (`dispatches/2026-07-13-gamora-cell-key-dedup-v1-BLOCKED.md`) is now UNBLOCKED — stable `GROUP BY cell_key` target on 470 combat-kit rows.

**Commit:** _(see commit hash below)_

**ADR-006:** committed scripts + logs; **NO push** (Matt-gated).
