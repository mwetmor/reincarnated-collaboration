# Corpus cell-key materialization — curation log — 2026-07-13

**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-07-13-elrond-cell-key-materialization.md`
**Spec:** `agentic_orchestration/gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md`
**Canon:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §3 / §3A / §3A.1 / §3B / §6.1 / §7 / §8
**Script:** `agentic_orchestration/research/scripts/corpus_cell_key_materialize_2026_07_13.py` (idempotent; D6 slot 4/4)
**Schema:** corpus.db `corpus_schema_meta` 2.2 → 2.3

## One line

Materialized the Matt-ratified strict-13 cell key: promoted the 4 non-column coordinates (#5b ctrl_function, #7 economy_model, #12 activation_val, #13 dependency_val) to keyed columns on `canon_engine_key`, added `resource_verbatim` (display, out-of-key), and serialized `cell_key` — the canonical ordered 13-tuple (#5 = two slots; unknown/blank = literal) — for the 470 combat-kit rows. **This is the single execution gate between the ratified key and gamora's dedup v1.** Dedup NOT run (gamora's separate blocked dispatch).

## Headline result

**470 combat-kit rows → 457 distinct cells** (strict-13 exact-match). The first read of the collapse structure: shallow, as a strict key should be (split-late beats merge-wrong; §6.1). 12 multi-kit cells absorbed 13 rows. 49 rows carry at least one `unknown`/`blank` literal slot (the never-merge-on-absence footprint).

## The 4 new keyed columns — populated counts + null/unknown footprint

Population = 470 combat-kit rows. system-records (17) NULL on all new columns + cell_key (out of the combat denominator).

### #5b `ctrl_function` ∈ {hard-stop, stun, taunt, fear, blind, knockback, expose, hex, silence, none, unknown}
| value | n |
|---|---|
| none | 311 |
| hard-stop | 44 |
| hex | 28 |
| stun | 27 |
| knockback | 20 |
| expose | 12 |
| taunt | 11 |
| blind | 7 |
| unknown | 7 |
| fear | 3 |
| silence | 0 |

- **7 unknown** = the 7 mint kits with no `control` probe fact (genuine absence → literal `unknown`, never coalesced). kit_ids: poe1-totem-hierophant, d3-call-of-the-ancients, le-ring-of-shields, d3-dashing-strike-monk, le-shift-bladedancer, poe1-vaal-blade-vortex, d2-sacrifice.
- **`silence` = 0**: no source ailment token maps to it; reserved enum slot, correctly empty.
- **Derivation (§3):** the corpus `control.ailments` array mixes Layer-1 element-neutral CONTROL tokens (Class A) with Layer-2 ELEMENTAL ailments (Class B damage-DoT). Only Layer-1 tokens set a function; multiple → highest-priority (hard-stop > taunt > fear > silence > blind > knockback > stun > expose > hex). Layer-2-only or `slow`-only kit → `none`. Full token→function map in the script header.

### #7 `economy_model` ∈ {spend, cooldown, generator-spender, reserve, self-cost, finite, free, unknown} + literal COMPOUNDS
| value | n |
|---|---|
| spend | 182 |
| cooldown | 61 |
| free | 48 |
| reserve | 47 |
| unknown | 43 |
| generator-spender | 37 |
| finite | 35 |
| self-cost | 15 |
| spend+finite | 1 |
| spend+cooldown | 1 |

- **2 literal compounds** (`spend+finite`, `spend+cooldown`) — hybrids kept as literal compounds, never collapsed (guardrail 4). (The raw compound tokens were `spend+ammo`→`spend+finite` and `spend+cooldown`.)
- **43 unknown breakdown:** 28 raw-`other` (conservatively unresolved — see disposition below), 7 no-probe (mint), 6 raw-`unknown`, 2 raw-`draft` (spec-gap — see below).
- **`econ_status` / `econ_meter_type` UNTOUCHED** (463 each still populated) — `economy_model` is additive (guardrail 6 / register §7).
- **`generator-spender` sub-structure** `{continuous·combo·stack}` from `meter_type` is NOT forked into a column (§3B strong-hypothesis, split-at-keying); it remains available on the `economy` probe fact's `meter_type` for the Stage-2 review.

### #12 `activation_val` ∈ {active, triggered, unknown}
| value | n |
|---|---|
| active | 376 |
| triggered | 87 |
| unknown | 7 |

- **Derivation (§3A.1):** intrinsic-trigger tell in `mech_note` (on-crit / on-hit / on-timer / autonomous / proc-econ / spell-on-attack…) AND no gear-source tell → `triggered`; else `active` (player pulls the trigger each cast). 7 unknown = mint kits with empty `mech_note`. 87 triggered brackets the §5 gap-map "~60 intrinsic-trigger" estimate (proc-econ tell widens it).

### #13 `dependency_val` ∈ {one-shot, build→spend, apply→detonate, unknown}
| value | n |
|---|---|
| one-shot | 359 |
| apply→detonate | 60 |
| build→spend | 44 |
| unknown | 7 |

- **Derivation (§3A):** detonate tells (detonate / corpse-explode / trap / totem / mine / mark-consume / delayed-kill…) → `apply→detonate`; build-tells (charge-up / ramp / stacking / generator / combo-point / finisher-consume…) → `build→spend`; else `one-shot`. 7 unknown = empty mech_note. 104 setup-payoff (60+44) brackets the §5 "~70 setup-payoff" estimate (text-derived first pass runs a touch high; a Stage-2 refinement candidate).

### aux `resource_verbatim` (display; OUT of cell_key)
- 1:1 verbatim from the `economy` family `resource_verbatim` field. Populated 461/470 combat-kit (the 7 mint no-probe rows + 2 genuinely-null economy rows are NULL). Never coalesced, never rolled — pure recognition anchor (§3B). NOT a cell_key slot.

## cell_key — the serialization

- **Storage mechanism: MATERIALIZED COLUMN** `canon_engine_key.cell_key` (not a view). **Decision rationale:** gamora needs a stable `GROUP BY cell_key` target; a materialized column gives a single deterministic index-able string, survives the two-table join being frozen at materialization time, and does not re-execute the cross-table join on every dedup query. A view would re-join `canon_engine_key ⋈ canon_corpus` on each read and expose gamora to any mid-flight coord edit — the materialized column is the stable contract. Re-materialize (re-run this idempotent script) if any of the 13 source coords change.
- **Format:** pipe-joined lowercase tokens, canonical coord order 1→13, **#5 = two slots** (treatment | function). All 470 rows verified to carry exactly **14 pipe-fields** (13 coords + #5 double). Example: `rooted|projectile|flat|cone|control|hard-stop|absorb|spend|solo|dual|high|instant|triggered|one-shot`.
- **Coord-order & source table:**
  1 mob_policy_while_casting (cek) · 2 delivery_value (cek) · 3 amp_val (cc) · 4 geometry_value (cek) · 5a ctrl_treatment (cek) · 5b ctrl_function (cek-NEW) · 6 def_bin (cek) · 7 economy_model (cek-NEW) · 8 proxy_val (cc) · 9 range_val (cc) · 10 tempo_val (cc) · 11 commit_val (cc) · 12 activation_val (cek-NEW) · 13 dependency_val (cek-NEW).
  (cek = canon_engine_key; cc = canon_corpus; joined on kit_id.)
- **Unknown/blank = literal** (guardrail 2): a genuinely-absent slot (SQL NULL / '') → literal `blank`; a source that itself carries the string `unknown` → stays `unknown`. Both are literal values — they NEVER coalesce with each other or with a real value. This is the never-merge-on-absence guarantee.
- **Row scope: combat-kit only.** The 17 system-records are OUT of the combat denominator (row_class discipline) → their cell_key + 4 new columns are **NULL (not excluded-by-filter)**. Decision: NULL (not a sentinel string) so a naive `GROUP BY cell_key` over the whole table cannot accidentally mint a phantom "NULL-cell"; gamora filters `row_class='combat-kit' AND cell_key IS NOT NULL`.

## Smoke (dispatch acceptance)

```
SELECT count(DISTINCT cell_key), count(*)
FROM canon_engine_key WHERE row_class='combat-kit' AND cell_key IS NOT NULL;
-- 457 | 470
rows carrying any unknown/blank slot: 49
```

## The collapse (first read — 12 multi-kit cells, 13 rows absorbed)

Genuine cross-game/intra-game isotope pairs, e.g.:
- `poe1-ea-ballista / poe1-fire-trap / poe1-pizza-sticks` (3-kit cell — totem/ballista trap builds).
- `poe1-cyclone / d3-ww-wastes` (Cyclone vs Whirlwind — channeled spin-melee; textbook cross-game isotope).
- `di-draw-quarter-crusader / tq-shield-charge-conqueror` (shield-charge knockback dash, cross-game).
- `d3-dashing-strike-monk / le-shift-bladedancer` — **flag to gamora:** these two mint kits collapse largely on shared `blank`/`unknown` literal slots (sparse FOLD-2 data), NOT full mechanical identity. Legitimate exact-match under the never-merge-on-absence rule (both genuinely blank in the same slots), but it is a data-completeness artifact, not a confirmed isotope. gamora's tiebreak keeps both as isotopes regardless (never deleted), so no action needed — noted for cluster-review awareness.

## Dispositions the dispatch asked me to document

- **`draft` (2 rows) — SPEC GAP, flagged; kept `unknown`, NOT `finite`.** Handoff mapped `draft→finite` low-confidence, confirm. Inspecting the 2 rows (`vs-queen-sigma`, `hot-norseman-frost-avalanche`): both are roguelite **draft/offer-pool BUILD-SELECTION** economies (Vampire-Survivors-style — "the economy is CHOOSING WHAT NOT TO TAKE" / "STARTS with the draft position, no build-toward"). This is NOT a consumable-input `finite` economy (ammo/charges/corpses/recipe). Folding it into `finite` would wrong-merge a build-selection mechanic with consumable-input mechanics. **Conservative call: `unknown` literal** (never-invent), pending gandalf ruling. Candidate resolutions for gandalf: (a) a new `draft`/`offer-pool` model value; (b) `free` residual (no per-cast resource); (c) confirm `finite`. FLAGGED — did not guess past it.
- **`other` (38 raw; 28 land on combat-kit) — mostly `unknown`, 2-ish → `free`.** Only genuinely no-economy resources (`resource_verbatim ∈ {none, stamina/none}`) map to `free` residual; all other `other` rows (stat→damage, form-lock, item-count, unlock-trophy, pet-stat, arcana-stack…) stay `unknown` literal. Conservative: never invents a model from an ambiguous resource string.
- **`unknown` (6 raw) → `unknown`** literal (conservative, per handoff).
- **system-record scope call:** NULL (not excluded-by-string-sentinel), combat-kit only — see cell_key section.

## Round-trip disposition (Principle 6 / ADR-004)

**NOT APPLICABLE — confirmed.** All writes are additive columns on `canon_engine_key` inside elrond's stewarded curation DB (corpus.db). No star-lord engine-telemetry boundary is touched: no `fight_log` / `loadout` / `export` packet field, no engine schema. The sole downstream consumer is gamora's dedup, which reads `cell_key` within the curation/analysis layer. No MIGRATION.md against star-lord required. No star-lord-boundary column implicated — no STOP-and-flag triggered.

## Guardrails honored (all 5 from the handoff + the KR econ-distinctness note)

1. ✅ Strict exact-match FIRST — the key is the full 13-tuple, never pre-coarsened. Stage-2 coarsening is gamora+gandalf+Matt's separate reviewed pass.
2. ✅ Unknown/blank = literal, never coalesced.
3. ✅ #5 = treatment AND function (two slots; all 470 rows = 14 fields verified).
4. ✅ Hybrid economies as literal compounds (`spend+finite`, `spend+cooldown`).
5. ✅ `resource_verbatim` out of the cell_key.
6. ✅ `economy_model` additive; `econ_status`/`econ_meter_type` untouched (463 each still populated).
7. ✅ Dedup NOT run (gamora's dispatch).

## Reproducibility (Discipline #11)

- Idempotent: re-run → byte-identical (`shasum 9e158f59…` of the full combat-kit key projection stable across re-run).
- Full clean rebuild from scratch (base ingest → s1 → fold12 → this) reproduces the same `9e158f59…` hash and 457/470 smoke.
- Raw columns untouched; all derivations re-computed from committed source (probe_facts / mech_note / the 9 already-present coord columns) every run.

## D6 rebuild sequence (now FOUR committed scripts)

```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py            # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py      # S1 completion (idempotent)
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py             # mint-dossier fold (idempotent)
python3 agentic_orchestration/research/scripts/corpus_cell_key_materialize_2026_07_13.py  # THIS — cell-key materialize (idempotent)
```

corpus.db stays gitignored; the scripts + this log + the MIGRATION entry are the committed truth.

## Spec gaps flagged to gandalf (do not guess past)

1. **`draft` economy model (2 rows)** — build-selection/offer-pool economy, not consumable-`finite`. Kept `unknown` literal pending ruling (candidates: new draft value / free residual / confirm finite).
2. **Minor:** `dependency_val` text-derivation runs a touch above the §5 "~70 setup-payoff" estimate (104 = 60 detonate + 44 build). Not a gap — a Stage-2 refinement candidate (text tells over-fire slightly; the strict-key collapse is robust to it since dependency is a never-demote core coord).
