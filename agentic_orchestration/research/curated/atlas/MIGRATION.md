# MIGRATION — Atlas fit/ghost-field layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema + fact-honesty migrations for the atlas fit artifacts under `agentic_orchestration/research/curated/atlas/` (editions, refit candidates, ghost-field ledgers, comparison reports). Parallels the top-level `../MIGRATION.md` (corpus/register data layer) and star-lord's engine-side `MIGRATION.md` per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

---

## s1-data-completion-post-e4-2026-07-16 — S1 data-completion delta pass: era_year backfill on the 61 post-E4 rows (LA + MCD + 3 pull re-keys); other payloads NULL-honest — 2026-07-16 — **APPLIED (gandalf autonomous atlas-parity run, S1 charge; iron-law asserts all held PRE + POST)**

### One line
Executed the S1 delta pass on the post-Edition-IV corpus (585 rows, 566 kit-grain + 19 system-records, 562 cell_key-resolved incl. 1 `-bt` sentinel). Filled `era_year` for the 61 rows that landed after the 2026-07-13 S1 pass (53 LA + 5 MCD + 3 pull re-keys d3/d4/di); all other S1 payloads (roster mob/amp/commit, delivery_value mint kits, poe2 movement-unknowns, void-rift amp, stabilization_patch) yielded ZERO delta fills — each honest-NULL under iron law 3 (no engine source of record, no probe evidence, no live-URL provenance). Row count 585 held; kit/NULL grain 566/19 held; cell_key 562 resolved held; -bt sentinel 1 held; engine_key 1:1 zero orphans held.

### S1 scope per wind-down doc (§3, verbatim; the brief's headline reconciled)
Wind-down doc scope: *"45-roster backfill (movement + amp + commit from engine sources of record — bc_target_cell_sampler.py CellDefs + battle-sim configs); delivery.value probe→keyed column; 6 poe2 movement-unknowns; void-rift amp if resolvable; era_year + stabilization_patch columns (public-register naming feed, §7.1 — era from per-game meta ×19 already landed; patch pin from probe sources_used where present, NULL-honest otherwise)."*

Brief headline (*"45-roster backfill · delivery.value completion · poe2 unknowns · era_year/stabilization_patch columns"*) is a SUBSET — it omits the void-rift amp resolution attempt (a legitimate S1 sub-item; also NULL-honest by evidence) and frames the era_year/stabilization_patch columns as "new" when they were added in the 2026-07-13 pass (Edition-2 era). Doc wins; brief's scope is a compatible subset. **Iron law 6 not tripped:** neither text materially expands or contracts what S1 owes — this pass is the incremental fill on the post-E4 delta population.

### Backup + scripts
- **Backup-first (iron law 1):** `../corpus.db.pre-s1-data-completion-2026-07-16-backup` (created 2026-07-16 pre-run; `integrity_check=ok`; git-ignored). No pending WAL at run time (`lsof` clean).
- **Script:** `../scripts/corpus_s1_data_completion_2026_07_16.py`. Idempotent; guarded by `WHERE era_year IS NULL` predicates; transactional (rolls back on assert breach, does not commit). Parent script: `corpus_completion_s1_2026_07_13.py` (established schema + initial 524-row fill; this script extends `GAME_ERA_YEAR` with LA=2018 + MCD=2024 and runs the 61-row incremental).

### Per-payload fill results
| Payload | Filled (delta) | NULL-remaining (post) | Total | Disposition |
|---|---|---|---|---|
| **P1a** roster_atlas.amp_val         | 0 | 19 | 45 | NULL-honest — CellDefs only supply amp for K1–K25 (26 rows already populated 2026-07-13); K26–K29/H*/B* have no CellDef mapping |
| **P1b** roster_atlas.commit_val      | 0 | 40 | 45 | NULL-honest — only 3 CellDef commitment pins (K1/K7/K19) + 2 roster-explicit (B12/H6) exist; unpinned cells are ROLLED at S7 generation, not fixed at S1 |
| **P1c** roster_atlas.mob_policy_while_casting | 0 | 45 | 45 | NULL-honest — NO S1 engine source of record for movement policy; emitted per-skill at S7 (`per_skill_emitter._MOVE_*`) |
| **P2**  canon_engine_key.delivery_value | 0 | 13  | 585 | 572/585 populated at Edition-IV; 13 NULLs = 6 mint kits (hand-auth provenance owed) + 4 dossier-owed (HANDS-OFF; legolas dossier batch owes fill) + 3 system-records (NULL by design; all axes abstain) |
| **P3**  6 poe2 movement-unknowns     | 0 | 6  | 6   | NULL-honest — probe evidence explicitly *"POST-CUTOFF: live verification required"*; iron law 3 forbids fabrication |
| **P4**  d2-wl-void-rift amp_val      | 0 | 1  | 1   | NULL-honest — probe evidence *"mechanics unharvested"*; no source resolves |
| **P5a** canon_corpus.era_year        | **+61** | 0  | 585 | **585/585 populated post-run.** Delta: d3=+1 (`d3-wizard-black-hole`), d4=+1 (`d4-spiritborn-vortex`), di=+1 (`di-cyclone-strike-monk-base`), la=+53, mcd=+5 |
| **P5b** canon_corpus.stabilization_patch | 0 | 568 | 585 | 17/585 populated (10 chronicon 1.52 + 7 mint hand-authored); no delta fill — `sources_used` probe field carries source-name tags (kb/iv/ph/dw/maxroll), NOT patch pins; LA/MCD 9.19 harvest's v2.13.0 = HARVEST cadence, NOT game patch. NULL-honest per iron law 3; naming-law display contract (§7.1 refinement 5) omits the patch segment where absent |

### Provenance convention
- **Column `era_year`** (INTEGER, no separate provenance column on `canon_corpus` for this axis): fills carry implicit provenance via the schema-meta ledger entry `corpus_schema_meta` v2.2 (this pass) — recording that era_year values are the per-game canonical release-year canon (source: `matt_notes_handoff_docs/gemini-steam-mothership-research-and-kit-naming-advice-for-devlog` §7.1 naming-law feed + per-game public-release timelines; LA=2018 Smilegate/Amazon Games release, MCD=2024 publisher release). The existing pattern (S1 v2.1 pass 2026-07-13) records era_year provenance at the schema-meta ledger level, NOT per-row — matched.
- **Post-cutoff claims:** wind-down doc §7.1 refinement 5 requires patch pins to derive from probe `sources_used` where present — none available. LA/MCD live-URL provenance for stabilization_patch was not carried in the 9.19 harvest (harvest cadence tag ≠ game patch); a future legolas Mode-B pass or Matt-authorized live-web mission would be required. This pass files the gap rather than inventing.

### Asserts (iron law 4 — held PRE + POST)
| Assert | Expected | PRE | POST |
|---|---|---|---|
| total_corpus | 585 | 585 | 585 |
| total_engine_key | 585 | 585 | 585 |
| kit_grain | 566 | 566 | 566 |
| null_grain | 19 | 19 | 19 |
| cell_key_resolved (incl. 1 `-bt` sentinel) | 562 | 562 | 562 |
| bt_sentinel | 1 | 1 | 1 |
| orphans engine→corpus | 0 | 0 | 0 |
| orphans corpus→engine | 0 | 0 | 0 |
| dossier_owed=1 | 4 | 4 | 4 |

**Zero drift.** Wildsoul ×2 + Valkyrie ×2 (dossier_owed=1) untouched per brief.

### Schema-meta bump
`corpus_schema_meta` v2.2 inserted (`2026-07-16T00:00:00Z`) with note: *"S1 data-completion delta pass (elrond, post-E4). era_year +61 fills (LA=2018, MCD=2024, 3 pull re-key stragglers). P1/P2/P3/P4/P5-patch NULL-honest (no engine/probe/live source; iron law 3 preserved). Row counts hold at 585 corpus + 585 engine_key + 45 roster + 4780 probe_facts + 562 cell_keys."*

### Iron laws honored
1. **Backup-first**: `corpus.db.pre-s1-data-completion-2026-07-16-backup` created before any write; filename in return.
2. **Data-completion ONLY**: no row inserts/deletes, no cell_key touches, no atlas artifact writes, no served-surface changes, no dossier_owed flag changes (4 held).
3. **Provenance + NULL-honest**: every value filled carries provenance (schema-meta ledger convention matched); every unfillable value NULL + counted + named. Zero fabrication.
4. **Asserts fail-loud**: 9 asserts checked PRE, executed as barrier BEFORE any writes; POST recheck + transactional; no drift. Script self-halts on breach with `sys.exit` non-zero.
5. **MIGRATION.md entry**: this entry.
6. **HALT discipline**: brief-vs-doc reconciliation surfaced (brief headline is compatible subset; iron law 6 not tripped). No partial commit; all writes gated on POST asserts pass.

### ADR compliance
- **ADR-004**: this entry on the atlas MIGRATION.md. No engine-telemetry change; star-lord side unaffected. Parallel corpus/register `../MIGRATION.md` unaffected (this is a fit-input-adjacent completion, kept adjacent to the E4 entry it depends on).
- **Reversibility**: full run reproducible from backup + `corpus_s1_data_completion_2026_07_16.py`; idempotent (WHERE IS NULL predicates); pure UPDATEs from a stated canonical table (`GAME_ERA_YEAR`).
- **Auto-committed** per project discipline (Matt-authorized S1 charge under gandalf-prime's autonomous atlas-parity run). **Push DEFERRED to gandalf's verify-gates + KR's gate.**

---

## edition4-run-2026-07-16 — Edition IV emitted: curated LA/MCD + 3 pull re-keys admitted as supplementary points into the frozen Edition-I basis (Path A) — 2026-07-16 — **APPLIED (spec RATIFIED "Agreed, path A"; gates ALL PASS; NOTHING SERVED — gandalf verify-gates → galadriel render → Matt ratifies before cutover)**

### One line
Executed the ratified Edition-IV run (`edition4-refit-spec.md` §§ 3–10, Path A supplementary admission). Derived cell_keys for the 53 admissible curated LA/MCD rows (D1), admitted them + the 3 speced pull re-keys as **supplementary points** into the byte-frozen Edition-I MCA basis, and emitted `atlas-edition4.json` = **562 points** (469 active + 93 supplementary). The frozen basis and all 506 Edition-III point coords are byte-identical (G-3). corpus.db mutated ONLY by the D1 derivation (cell_key/unresolved/death_class); the artifact is nothing-served.

### Scripts (all new; TOOL scripts, not engine code)
- `../scripts/corpus_derive_cellkey_e4_la_mcd_2026_07_16.py` — D1/D2/D3 + R-2. Derives the 9 engine-key coords (full loadings-block vocabulary) from §9.19 `proj` + mech prose + `core_skills`; assembles the 14-field cell_key (ratified `serialize_cell_key`); flips `unresolved` 1→0; seats `death_class` on the genuine trap-identity negatives. Backup-first (`corpus.db.pre-e4-cellkey-derive-2026-07-16-backup`), transactional (rolled back once on a `def_bin` CHECK, then corrected: abstained coords write **NULL** to the column / `blank` in the key — parity with the 509).
- `../scripts/atlas_frozen_basis_reconstruct.py` — reconstructs the frozen Edition-I MCA basis from the durable snapshot `atlas-frozen-fit-cellkeys-edition1.csv` using `atlas_derivation_2026_07_14`'s EXACT machinery (`build_indicator`/`mca_greenacre`/Stage-0c fuse). Exposes `project_point_xy` / `cos2_one` / `level_flatten`. **Self-smoke: reproduces the 469 served active to 4.94e-08 and the 37 served tombstones to 3.94e-08 — the projection surface IS the frozen camera.**
- `../scripts/build_atlas_json_edition4.py` — emitter (parent `build_atlas_json_edition3.py`, cited in header). Frozen 506 carried byte-identical; 56 new supplementary projected; § 9 cos² + NEW-LEVEL CENSUS + P-3 trigger; gate_report block; predictions.

### D1 derivation (owed-work, spec §4) — the fidelity layer
- **57 curated rows → 53 derived** (47 positive + 6 negative), **4 held out** (T4/P-1 dossier holdout: `la-ferality-wildsoul`, `la-phantom-beast-awakening-wildsoul`, `la-shining-knight-valkyrie`, `la-liberator-valkyrie`).
- **Geometry fidelity (P-E4-5 ACCEPTANCE — PASS):** both Destroyer rows (`la-rage-hammer-destroyer`, `la-gravity-training-destroyer`) derive **`geometry=vortex_pull`**. Their §9.19 `proj.geo='small-AOE'` + `proj.ctrl='damage-pure'` FLATTEN the gravity-pull verb; it is recovered from the ratified **pull-carrier census** (Destroyer ×2 — the same index-EXACT census the la-mcd curation normalized + the stageB/pull-tranche precedents keyed `pull`), never from a naive core_skills keyword scan (which would over-fire on the "Blood Vortex"/"Maelstrom" SKILL names carried by `la-demonic-impulse-shadowhunter`/`la-remaining-energy-deathblade` — those are NOT pull identities; the abstain-not-force-fit discipline holds).
- **No new mapping rules (iron law 3):** every coord rule is a stated rule over the record's own fields anchored to an existing precedent (stageB `corpus_edition3_stageB_lostark58` map_*; the pull-tranche keying; the register v1.2 pull boundary). Where §9.19 offers no signal, the coord abstains (`blank` token / NULL column) and is named — never invented.
- **Abstention (LOUD):** 4 MCD rows abstain on `def_bin` (their `proj.def` carries `abstain:true`); the non-record placeholder `la-rage-hammer-destroyer-bt` abstains on 6 coords (all its `proj` axes carry `abstain:true` — see R-2).

### Economy fidelity (spec §9(b) / P-E4-6) — the NEW-LEVEL CENSUS by design
The LA/MCD identity-gauge / uptime / stance economies are **preserved as their own levels** (not collapsed to the lookalike frozen `generator-spender`) so the NEW-LEVEL CENSUS can SEE the flattening. Collapsing would HIDE the very loss the spec commissions me to disclose. Only genuinely-cooldown economies (`cooldown-economy`/`cooldown-uptime`, whose §9.19 note asserts the cooldown mechanic) fold to the frozen `cooldown`.

### Gates (pre-registered; ALL PASS — immutable at run)
- **G-1 grain: PASS** — staged population 100% `grain='kit'`; zero system/gear/class rows.
- **G-2 provenance: PASS** — breach-path tripwire VACUOUS (zero grain=kit rows from any non-speced / non-9.19 / non-E1-lineage / non-pull-tranche provenance). Non-silent.
- **G-3 congruence: PASS (by construction, vacuous-with-teeth)** — E3 basis block + all **506** E3 point coords **byte-identical** in E4 (0 drift, independently re-verified). The check RAN. Reconstruction smoke: 469 active reproduced to 4.94e-08, 37 tombstones to 3.94e-08.
- **G-4 census: PASS** — staged **562** = 469 active-basis + 37 legacy tombstones (incl. `hot-blood-catcher`, R-3) + 47 new positives (42 LA + 5 MCD) + 3 R-1 pull re-keys + 6 new tombstones. Every delta named; 19 T1-excluded system-records + 4 T4-held-out dossier-owed accounted.

### Reconciliations (named, no silent disposition — G-4)
- **R-1 (RESOLVED — ADMIT):** the 3 keyed-not-in-E3 rows `d4-spiritborn-vortex` / `d3-wizard-black-hole` / `di-cyclone-strike-monk-base` are the **pull re-keys** (provenance `pull-tranche-edition2-2026-07-15`; speced Diablo corpora — d3/d4/di are among the fifteen reference corpora with 49/46/21 resolved members each). **T2 PASSES** (speced-ingest clause; the breach tripwire is vacuous — the deleted-182 breach was LA/MCD, these survived as legitimate Diablo kits). Admitted as supplementary → the **562** plate (spec §2's "562 if the 3 pull re-keys pass T2").
- **R-2 (SEATED + NAMED):** 6 new negatives admitted as tombstones (T5). **5 are genuine community-tier-underperformance trap-identities** (D-tier/C-tier build played strictly weaker than its positive twin — viable-but-meta-penalized) → `death_class='extrinsic-tuning'` (the closest faithful enum value; the design-taxonomy final call — is community-tier-underperformance its own death-class? — is NAMED for gandalf). **The 6th (`la-rage-hammer-destroyer-bt`) is a NON-RECORD placeholder** — its own `mech_summary` reads *"NOT a record — both Berserker identities are positive canon; co-viable"* and ALL its `proj` axes abstain. It carries `negative=1` in the DB (ratified by the la-mcd curation) so T5 admits it, but it is NOT a genuine trap-skill → `death_class` stays the sentinel (`unknown-pending-recrawl`); the source-vs-flag tension is surfaced (mirrors the la-mcd Destroyer `grain_note` discipline). Its heavily-masked projection is itself the diagnostic: it is the ONE twin that lands FAR from its positive (P-E4-3, below).
- **R-3 (NAMED — no action):** the one pre-existing kit row with `unresolved=1` AND a cell_key is **`hot-blood-catcher`** — a patched-bug relic ("hundred-billion damage compounding relic interaction, developer-fixed"; `death_class=system-evidence`), already keyed + admitted as one of the 37 E3 tombstones. Its `unresolved=1` is a **provenance re-verification flag orthogonal to fit-input resolution** (the row is fully keyed and seated). Carried forward unchanged; touching it is out of scope.

### § 9 disclosures (Path A's honest cost, empirical — both instruments)
- **(a) cos² (weak expression of KNOWN levels):** admitted-cohort median plane-cos² = **0.1056** vs E1-active median **0.1685** (ratio **0.626**). The frozen plane expresses the LA/MCD cohort's variance at ~63% of the active baseline — LA is an entirely new franchise the basis never learned (zero LA rows in the frozen 469).
- **(b) NEW-LEVEL CENSUS (silent flattening of ABSENT levels):** top hits — **`economy:identity-gauge`=31** (30 LA + 1 MCD; the predicted P-E4-6 ~30) · `function:pull`=5 (2 Destroyers + 3 pull re-keys; `pull` is a post-E1 function level with no frozen column) · `economy:buff-uptime`=5 · `range:mid`=3 · `economy:stance-rotation`=3 · `economy:summon-uptime`=2 · `delivery:melee`=1 · `economy:soul-economy`=1. Per-point `level_flattened` stamps in the artifact.
- **P-3 REFIT TRIGGER: E5 FIRES (arm 2).** arm-1 (expression): admitted median 0.1056 ≥ 0.5×active (0.0843) → does NOT fire. arm-2 (vocabulary): `identity-gauge`=31 ≥ 20 → **FIRES**. E5 Path-B refit is triggered — exactly the spec's honest forecast ("if the LA cohort admits with the gauge census at ~30, arm 2 is already near its line"). Disclosure, not a gate; the refit law (§6) is already pre-registered.

### Prediction grades (spec §8; graded at run where computable — verdicts are numbers, interpretation is gandalf's/Matt's)
- **P-E4-1 FAIL** — `mcd-summoner`'s nearest ratified family (full-space nearest active seed) = **TOTEM-SENTRY** (`poe1-siege-ballista`, dist 0.864), NOT MINION-PET. Honest result; the flattened §9.19 geometry seats summoners toward totem-like placement on the frozen plane.
- **P-E4-2 PASS** — LA gauge-melee identities mutually condense (mean pairwise full-space dist below corpus mean).
- **P-E4-3 PARTIAL** — 5/6 negative twins land nearer their positive twin than corpus median NN (0.678). The ONE failure is the non-record `la-rage-hammer-destroyer-bt` (all-mask projection, dist 0.845) — a diagnostic confirmation of R-2, not a substantive miss. The 5 genuine trap-identities all pass.
- **P-E4-4 PASS** — admitted median cos² (0.1056) within 2× of E1-active median (0.1685); ratio 0.626. (Note: within 2× ≠ well-expressed; arm-2 still fires on vocabulary.)
- **P-E4-5 PASS** — both Destroyers derive `geometry=vortex_pull` (the D1-fidelity acceptance bar).
- **P-E4-6 PASS** — `identity-gauge` economy is the largest absent-from-basis level (31 exhibits; > the 20 arm-2 line).

### corpus.db mutation (D3 — the ONLY DB write; §4 scope)
53 rows: 9 engine-key coords + `cell_key` written, `unresolved` 1→0, `death_class` seated on 5 negatives. Idempotent (additive; re-derives to identical values). 1:1 corpus↔engine_key invariant held (585/585, 0 orphans). Resolved cell_keys 509→562. Backup: `corpus.db.pre-e4-cellkey-derive-2026-07-16-backup`. Raw `raw_json` untouched (non-destructive; every derived value reproducible from source).

### Artifact contract (spec §10)
`atlas-edition4.json` (7.51 MB): E3's key set + `edition:4` + `path` + per-point `edition_admitted:4` on the 56 new points + `cos2` + `level_flattened` stamps + full `gate_report` block (G-1..G-4 + predictions + section9 cos²/census/trigger) + ghost_field (live census; lattice byte-identical, `depth_sum_check`=767,411,820; `edition4_change` note) + pull-slice integrity (7 pull kits, all intrinsic, zero mcd-lit; `INTRINSIC_PULL_KITS` refreshed to the live Destroyer kit_ids).

### Iron laws honored
- **Path A ONLY** — frozen Edition-I basis; supplementary projection (the tombstone mechanism); NO refit, NO basis mutation, NO Procrustes. G-3 byte-identity RAN.
- **NOTHING SERVED** — no vendor copy, no glance touch, no served-artifact write. Edition III (`atlas-edition3.json`) READ-ONLY, untouched (mtime pre-run; still edition=3/506 points). Refit-Candidate-1 + all other served artifacts untouched.
- **HALT discipline** — fail-loud on every gate + P-E4-5 + schema mismatch + unnamed delta + unprojectable admit; a G-4 term-count bug HALTED cleanly (no partial emit) and was fixed before emission.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected. All work is collab-side curation (elrond data layer + atlas tree). The parallel corpus/register `../MIGRATION.md` unaffected (D3 is a fit-input resolution on the atlas layer; the la-mcd catalogue entry there stands).
- **Reversibility:** the full run is reproducible from the 3 scripts + `atlas-frozen-fit-cellkeys-edition1.csv` + `corpus.db`; deterministic (seed 20260716 for the prediction nulls). Raw preserved.
- **Auto-committed** per project discipline (Matt-authorized run under the ratified spec). **Push DEFERRED to gandalf's verify-gates + KR's gate.**

---

## la-mcd-curation-9.19-2026-07-16 — curate the 58 §9.19 re-harvest records into `corpus.db` (catalogue-only; 57 kit-grain + 1 system-record) + WAVE-4 supersession of the staging law's holdout clause — 2026-07-16 — **APPLIED (gandalf Option-A ruling, post-HALT execute pass)**

### What was curated (one line)
The 58 spec-valid successors of the deleted 182 (`dual-hard-delete-2026-07-16`) — Legolas's §9.19 five-stage re-harvest of both games — entered `corpus.db` as **catalogue citizens**: **57 at `grain='kit'`** (LA 46 positive + 6 negative twins + MCD 5 positive → `row_class='combat-kit'`) + **1 system-record** `la-monetization-confound` (`grain=NULL`, `row_class='system-record'`; precedent = the 18 existing, e.g. `tli-sage-elixir`). **Catalogue-only**: every new `canon_engine_key.cell_key = NULL` (NO fit input; the fit gate is `cell_key IS NOT NULL`), `unresolved=1` (cell_key derivation owed to E4). NO refit, NO leiden/affinity, NO `atlas-coordinates-*`, NO served-artifact touch. `corpus.db` was the ONLY mutation surface.

### HALT → ruling lineage (one line)
A prior elrond run HALTed per iron law 7 (zero writes; corpus quiescent) — correctly: `la-monetization-confound` is a **system-record** (`class="system archetype"`, all emission axes abstain, `econ='spend-as-progression'` rider anchor — gandalf-verified vs jsonl + run report), not a kit, and the brief's original asserts (kit=567 · NULL=18) double-counted it among the "47 positive." gandalf **RULED Option A** (curate 57 kit + 1 system-record; corrected asserts **total=585 · kit=566 · NULL=19 · gear=0 · class=0**), rationale: the anchor is mandated content (the LA run's monetization-confound rider) and the E4 refit's `grain='kit'` predicate auto-excludes it — GRAIN LAW filtering at consumption, exactly as designed. *This HALT is the grain law's first live catch — of its own author's arithmetic.* This entry is the execute pass of that ruling.

### Authority
Matt **WAVE 4** ruling 2026-07-16 (`canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md § WAVE 4`, verbatim): *"Edition IV = anchored-E3 + curated LA/MCD … LA/MCD enter via elrond curation then the E4 refit behind pre-registered gates (grain='kit' predicate + source-exclusion + congruence-to-E3-camera on ratified members)."* This charge is the **curation half**; the E4 refit is a separate, later charge. gandalf's reconciliation ruling authorizes the 57+1 split (brief top-blockquote, `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-la-mcd-curation-brief.md`).

### Provenance (source-anchored + reversible)
- **Sources:** `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-corpus-la.jsonl` (53 records, run commit `da003065`) + `canon-corpus-mcd.jsonl` (5 records, run commit `14abd361`), both §9.19 five-stage (pipeline-spec v2.13), both gandalf verify-gated + pushed. Run reports beside them.
- **Per row:** `source='canon'`, `provenance_tag='canon-harvest-9.19-{la|mcd}-2026-07-16'`, `source_date='2026-07-16'`, `prov='legolas-mode-b-9.19;elrond-curated'`, run commit + spec recorded in `flags` + `provenance_json`. The provenance chain makes these legible as the spec-valid replacements of the deleted 182.
- **Prefix coords** (`attr/range/tempo/amp/proxy/commit` on `canon_corpus`): taken from `proj.<axis>.v` IFF the axis does not abstain; abstain (`v='n/a'`) → NULL. Surveyed: ZERO non-abstain `proj` values are out-of-enum, so the rule reduces to write-v-or-NULL. The system-record abstains on all six → all NULL.
- **Raw JSONL row preserved verbatim** in `canon_engine_key.raw_json` (NOT NULL) — nothing destructively transformed; fully reversible.
- **Negatives:** the 6 LA negative twins carry the corpus `negative=1` convention (same as the 38-negative trap-skills). Not dropped; not counted as positives (new-negative count asserted = 6).

### Pos / neg / system split
| corpus | positive-kit | negative-kit (`negative=1`) | system-record | total |
|---|---|---|---|---|
| LA (`la-`) | 46 | 6 | 1 (`la-monetization-confound`) | 53 |
| MCD (`mcd-`) | 5 | 0 | 0 | 5 |
| **kit-grain inserted** | **51** | **6** | — | **57** |
| **system-record inserted** | — | — | **1** | **1** |

### Pre-insert collision check (fail-loud; brief iron law 5 — re-verified, cheap)
Incoming 58 ids all distinct; **0** id-collisions in `canon_corpus`, **0** in `canon_engine_key`; **0** `la-`/`mcd-` residue in `canon_corpus`, **0** in `canon_engine_key`, **0** in `canon_probe_facts`. The dual-delete left zero residue (confirmed). HALT-guarded (would abort before backup on any collision).

### Backup-first + transactional (no partial writes)
- **Pre-curation backup:** `../corpus.db.pre-la-mcd-curation-2026-07-16-backup` (527 rows, `integrity_check=ok`; taken BEFORE any write). git-ignored (binary DB), on disk.
- **Single BEGIN/COMMIT** wrapping both-table inserts + the schema-meta marker + all post-asserts; on ANY assert failure the txn ROLLS BACK and the DB is restored from the backup — no partial writes survive. (Validated on a scratch copy before the live run.)

### Post-curation asserts (fail-loud; ruling-corrected — all PASSED, independently re-queried)
- **Grain census:** total=**585** · `kit`=**566** · NULL=**19** · `gear`=**0** · `class`=**0**. ✓ (509→566 kit = +57; 18→19 NULL = +1.)
- **`canon_engine_key`:** 527→**585** rows; clean **1:1** with `canon_corpus` — forward orphans **0**, reverse orphans **0** (every corpus row has exactly one engine-key child; the ratified never-orphan invariant preserved).
- **NO fit input:** all 58 new `canon_engine_key` rows carry `cell_key=NULL` (asserted new-rows-with-cell_key = 0). Fit-excluded by the served predicate `row_class='combat-kit' AND cell_key IS NOT NULL AND negative=0` (verified in `../scripts/atlas_refit_candidate_2026_07_16.py`).
- **grain↔row_class partition intact:** `kit`↔`combat-kit` (566), `NULL`↔`system-record` (19); 0 rows violate.
- **Additive:** the 527 survivors' `kit_id|grain|negative` signature byte-unchanged before/after. `PRAGMA integrity_check=ok`.

### THE STAGING LAW — WAVE-4 supersession (recorded per brief iron law 6)
The `dual-hard-delete-2026-07-16` STAGING LAW's **archipelago-holdout clause is SUPERSEDED** by Matt's WAVE 4 ruling (decision file § WAVE 4). The no-admission-without-a-passed-gate **intent survives**, re-attached to the **E4 refit** behind **pre-registered gates** (`grain='kit'` predicate + source-exclusion + congruence-to-E3-camera on ratified members). Re-harvested LA/MCD no longer wait on an archipelago hold-out pass; they land catalogued-only (this entry) and enter atlas fits ONLY at the E4 refit through those gates. THE GRAIN LAW + INGEST CLASS RULE entries below **stand unchanged** — grain still makes the exclusion structural; the E4 gates make re-admission explicit.

### Iron laws honored
- **Edition III + every served artifact READ-ONLY** — byte-verified untouched (`atlas-edition3.json`, `atlas-refit-candidate-1.json`, `atlas-frozen-fit-cellkeys-edition1.csv`, `atlas-archipelago-mock.json` all `git diff HEAD` clean).
- **NO re-fit / NO re-emission / NO leiden/affinity recompute / NO atlas-coordinate write.** `corpus.db` was the ONLY mutation (58 additive INSERTs into `canon_corpus` + `canon_engine_key`).
- **Catalogue-only:** atlas admission is deferred to the E4 refit behind WAVE-4 gates (a separate charge).

### Reversibility + reproducibility
Executed by `../scripts/corpus_curation_la_mcd_2026_07_16.py` (idempotent additive upsert keyed on `kit_id`; backup-first; transactional with restore-on-failure; fail-loud asserting the pre-state 527/509/18/527, the collision/residue = 0, and the post census 585/566/19/0/0 + 1:1 engine-key + no-cell_key + partition + additive-survivor + `integrity_check`). Fully reversible from `../corpus.db.pre-la-mcd-curation-2026-07-16-backup` + the verbatim JSONL preserved in `raw_json`.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected. Collab-side curation only (elrond data layer).
- Auto-committed per project discipline (Matt-authorized curation under the WAVE-4 ruling + gandalf's reconciliation ruling). **Push deferred to gandalf's verify-then-push gate.**

---

## dual-hard-delete-2026-07-16 — IMMEDIATE hard-delete of all 182 spec-orphaned rows (62 LA + 120 mcd) from `corpus.db` + ingest-provenance census + THE STAGING LAW — 2026-07-16 — **APPLIED (Matt-ruled; never-purge carve-out EXERCISED — real DELETE)**

### THE STAGING LAW (ratified — recorded alongside THE GRAIN LAW below)
> *The real archipelago derivation builds on the post-deletion kit-grain corpus WITHOUT LA/MCD. Re-harvested LA/MCD corpora land **catalogued-only** and enter atlas fits ONLY AFTER the archipelago passes its pre-registered hold-out gates; admission then = **new-Edition refit**.*

Spec cross-ref: `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-harvest-pipeline-spec-v2.md` §9.19.5. This law composes with THE GRAIN LAW (below): grain made the exclusion *structural* (a predicate cannot forget it); the STAGING LAW makes the *re-admission path* explicit (no LA/MCD re-entry without passing the gates and a new-Edition refit). Together they close the failure class that contaminated Refit-Candidate-1 — manual fit-stage holds do not survive predicate rewrites, and re-harvested data must not silently re-leak.

### Authority (Matt rulings 2026-07-16, verbatim)
- **Wave-3:** *"I also recommend the immediate deletion of the old MCD and Lost Ark data."*
- **Wave-2 (composed):** *"I recommend that we delete the entire Lost Ark corpus."*

Both logged in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md § RULING + WAVE 3`. The catalogue never-purge philosophy's **Matt's-word carve-out is hereby EXERCISED** — this is a real `DELETE`, not an inert `grain` flag. The GRAIN LAW's INERT-catalogue reading (score/filter at consumption, never purge) held until Matt's word arrived; the word arrived, and the carve-out fires once, on the record.

### What was deleted (the permanent record — these rows no longer exist)
**182 rows from `canon_corpus`** + **156 cascade children from `canon_engine_key`** (FK enforcement was OFF, `PRAGMA foreign_keys=0`; children deleted explicitly to honor the never-orphan discipline — a parent-only delete would have left 156 dangling engine-key rows). No `canon_probe_facts` (0 for the set), no `roster_atlas`/`roster_lineage_enrichment` (0 for the set), no `atlas_gateA_labels*` (0 for the set — consistent with zero-E1-membership). Views are derived; nothing stored to delete.

**Delete-set composition (asserted EXACT before delete — HALT if mismatch):**

| game | grain | n | provenance_tag (ingest path) | engine-key child |
|---|---|---|---|---|
| la | class | 56 | `lost-ark-classkit-edition3-2026-07-15` | all keyed |
| la | kit | 2 | `lost-ark-classkit-edition3-2026-07-15` (engraving-grain Destroyer) | all keyed |
| la | kit | 4 | `pull-tranche-edition2-2026-07-15` (skill-grain Destroyer) | all keyed |
| mcd | gear | 94 | `mcd-mode-b-2026-07-15` (keyed) | all keyed |
| mcd | gear | 26 | `mcd-mode-b-2026-07-15` (no-key / `unresolved=1`) | none |
| **TOTAL** | | **182** | | **156** |

All 182: `source='canon'`, `source_date='2026-07-15'`, `lineage=NULL`, `gx=NULL`. Provenance/grain split cross-cuts: the 62 LA = 56 class + 6 Destroyer kit **by grain** = 58 Stage-B + 4 pull-tranche **by ingest**; the 2 engraving-grain Destroyers (`la-destroyer-rage-hammer`, `la-destroyer-gravity-training`) rode the Stage-B 58-batch. The 6 Destroyer kit-grain rows that the GRAIN LAW *kept* under the grain reading are deleted here under Matt's wave-2/3 *whole-corpus* word — the ruling escalated from grain-exclusion to full deletion.

#### Per-row archive — 62 Lost Ark (kit_id | folk_name | grain)
**6 Destroyer (kit):** `la-destroyer-gravity-training` (Gravity Training Destroyer) · `la-destroyer-rage-hammer` (Rage Hammer Destroyer) · `la-destroyer-gravity-compression` (Destroyer — Gravity Compression) · `la-destroyer-gravity-force` (Destroyer — Gravity Force) · `la-destroyer-gravity-impact` (Destroyer — Gravity Impact) · `la-destroyer-vortex-gravity` (Destroyer — Vortex Gravity).
**56 class-engraving (class), 29 classes × 2 identity paths:** `la-aeromancer-drizzle` (Drizzle Aeromancer) · `la-aeromancer-wind-fury` (Wind Fury Aeromancer) · `la-arcanist-empresss-grace` (Empress's Grace Arcanist) · `la-arcanist-order-of-the-emperor` (Order of the Emperor Arcanist) · `la-artillerist-barrage-enhancement` · `la-artillerist-firepower-enhancement` · `la-artist-full-bloom` · `la-artist-recurrence` · `la-bard-desperate-salvation` · `la-bard-true-courage` · `la-berserker-berserkers-technique` · `la-berserker-mayhem` · `la-breaker-asuras-path` · `la-breaker-kingfist` · `la-deadeye-enhanced-weapon` · `la-deadeye-pistoleer` · `la-deathblade-remaining-energy` · `la-deathblade-surge` · `la-glaivier-control` · `la-glaivier-pinnacle` · `la-guardianknight-dreadful-roar` · `la-guardianknight-hellfire-successor` · `la-gunlancer-combat-readiness` · `la-gunlancer-lone-knight` · `la-gunslinger-peacemaker` · `la-gunslinger-time-to-hunt` · `la-machinist-arthetinean-skill` · `la-machinist-evolutionary-legacy` · `la-paladin-blessed-aura` · `la-paladin-judgment` · `la-reaper-hunger` · `la-reaper-lunar-voice` · `la-scrapper-shock-training` · `la-scrapper-ultimate-skill-taijutsu` · `la-shadowhunter-demonic-impulse` · `la-shadowhunter-perfect-suppression` · `la-sharpshooter-death-strike` · `la-sharpshooter-loyal-companion` · `la-slayer-predator` · `la-slayer-punisher` · `la-sorceress-igniter` · `la-sorceress-reflux` · `la-souleater-full-moon-harvester` · `la-souleater-nights-edge` · `la-soulfist-energy-overflow` · `la-soulfist-robust-spirit` · `la-striker-deathblow` · `la-striker-esoteric-flurry` · `la-summoner-communication-overflow` · `la-summoner-master-summoner` · `la-valkyrie-liberator` · `la-valkyrie-shining-knight` · `la-wardancer-esoteric-skill-enhancement` · `la-wardancer-first-intention` · `la-wildsoul-phantom-beast-awakening` · `la-wildsoul-wild-instincts`.

#### Per-row archive — 120 Minecraft Dungeons (all `grain=gear`, `mcd-mode-b-2026-07-15`)
**94 keyed (had `canon_engine_key` child + cell_key):** mcd-ancient-bow, mcd-art-blast-fungus, mcd-art-buzzy-nest, mcd-art-corrupted-beacon, mcd-art-corrupted-seeds, mcd-art-enchanted-grass, mcd-art-eye-of-the-guardian, mcd-art-fishing-rod, mcd-art-ghost-cloak, mcd-art-golem-kit, mcd-art-harvester, mcd-art-ice-wand, mcd-art-iron-hide-amulet, mcd-art-lightning-rod, mcd-art-love-medallion, mcd-art-scatter-mines, mcd-art-shadow-shifter, mcd-art-shock-powder, mcd-art-soul-lantern, mcd-art-spinblade, mcd-art-tasty-bone, mcd-art-totem-of-shielding, mcd-art-vexing-chant, mcd-art-wind-horn, mcd-art-wonderful-wheat, mcd-auto-crossbow, mcd-azure-seeker, mcd-baby-crossbows, mcd-battlestaff-of-terror, mcd-bone-cudgel, mcd-bonebow, mcd-bow-of-lost-souls, mcd-broadsword, mcd-bubble-burster, mcd-butterfly-crossbow, mcd-call-of-the-void, mcd-corrupted-crossbow, mcd-dancers-sword, mcd-diamond-pickaxe, mcd-doom-crossbow, mcd-elite-power-bow, mcd-fangs-of-frost, mcd-feral-soul-crossbow, mcd-fighters-bindings, mcd-firebolt-thrower, mcd-firebrand, mcd-flail, mcd-gloopy-bow, mcd-grave-bane, mcd-great-axeblade, mcd-growing-staff, mcd-guardian-bow, mcd-harp-crossbow, mcd-haunted-bow, mcd-heartstealer, mcd-highland-axe, mcd-hunters-promise, mcd-lightning-harp-crossbow, mcd-love-spell-bow, mcd-masters-bow, mcd-mechanical-shortbow, mcd-mechanized-sawblade, mcd-moon-daggers, mcd-nameless-blade, mcd-nautical-crossbow, mcd-nightmare-bite, mcd-nocturnal-bow, mcd-phantom-bow, mcd-pride-of-the-piglins, mcd-purple-storm, mcd-red-snake, mcd-sabrewing, mcd-sheer-daggers, mcd-shivering-bow, mcd-shrieking-crossbow, mcd-slayer-crossbow, mcd-soul-hunter-crossbow, mcd-spellbound-crossbows, mcd-sponge-striker, mcd-stormlander, mcd-sugar-rush, mcd-suns-grace, mcd-swift-striker, mcd-the-green-menace, mcd-the-last-laugh, mcd-the-pink-scoundrel, mcd-the-slicer, mcd-the-starless-night, mcd-twin-bow, mcd-veiled-crossbow, mcd-venom-glaive, mcd-webbed-bow, mcd-weeping-vine-bow, mcd-winters-touch.
**26 no-key (`unresolved=1`, no engine-key child — the brief's "26 no-key"):** mcd-art-boots-of-swiftness, mcd-art-death-cap-mushroom, mcd-art-enchanters-tome, mcd-art-fireworks-arrow, mcd-art-flaming-quiver, mcd-art-gong-of-weakening, mcd-art-harpoon-quiver, mcd-art-light-feather, mcd-art-powershaker, mcd-art-satchel-of-elements, mcd-art-satchel-of-elixirs, mcd-art-satchel-of-snacks, mcd-art-soul-healer, mcd-art-thundering-quiver, mcd-art-tome-of-duplication, mcd-art-torment-quiver, mcd-art-totem-of-casting, mcd-art-totem-of-regeneration, mcd-art-updraft-tome, mcd-art-void-quiver, mcd-burst-gale-bow, mcd-echo-of-the-valley, mcd-encrusted-anchor, mcd-hammer-of-gravity, mcd-imploding-crossbow, mcd-voidcaller.

### THE 182-ROW INGEST-PROVENANCE CENSUS (owed since wave-2 — *how did 182 spec-orphaned rows enter?*)
Facts only. Root-cause ruling (spec-stewardship failure; Legolas exonerated) is already canon; this census answers only the mechanical *how*. Three ingest paths, all elrond-run curation scripts on 2026-07-15, all confirmed against the §9.19.1 breach record (no §2 seating, no §4 sources row, no five-stage pipeline — these entered as direct curation inserts, not through the canon-harvest pipeline):

1. **mcd 120 (gear)** — `../scripts/corpus_ingest_mcd_2026_07_15.py` (base MCD Mode-B ingest; 120 inserted, 2 dropped as base-rarity unique-weapon-grain) + `../scripts/corpus_curation_mcd_complete_2026_07_15.py` (finished the timed-out run; promoted `architecture='notable'` + `pull_pending_vocab` to first-class columns). MIGRATION anchors: `mcd-ingest-2026-07-15`, `mcd-curation-complete-2026-07-15` (top-level `../MIGRATION.md`). 94 keyed via `canon_engine_key` combat-kit + cell_key; 26 unresolved (20 thin-artifact + 6 pull_pending_vocab). Coords steward-derived from tranche prose (MCD lacks `canon_probe_facts`).
2. **LA 56 class + 2 engraving-Destroyer kit (58)** — `../scripts/corpus_edition3_stageB_lostark58_2026_07_15.py` (Edition-III Stage B; 29 classes × 2 identity paths; HONING-ECONOMY CONFOUND LAW on every row). MIGRATION anchor: `edition3-stageB-lostark58-2026-07-15`.
3. **LA 4 skill-Destroyer kit** — `../scripts/corpus_ingest_pull_tranche_2026_07_15.py` (pull-tranche edition-2 ingest) → re-inserted/keyed at full completeness by `../scripts/corpus_edition3_stageA_pull7_2026_07_15.py` (Edition-III Stage A pull-7, `function=pull` register v1.2). MIGRATION anchor: `edition3-stageA-pull7-2026-07-15`.

Grain labels for all 182 were assigned later by `../scripts/corpus_grain_ratification_2026_07_16.py` (commit `6d742c7e`; the GRAIN LAW entry below). **§9.19.1 breach confirmed:** none of the three paths ran through the canon-harvest five-stage pipeline; all were direct additive curation inserts against `canon_corpus`. That is the mechanical reason 182 rows existed in the corpus without spec seating — and precisely why the STAGING LAW now routes any future LA/MCD re-harvest through catalogued-only staging + gate-passing + new-Edition refit before atlas admission.

### Pre-delete integrity gate (all asserted BEFORE the DELETE — HALT on any failure; all PASSED)
- **Delete-set counts EXACT:** LA=62 (56 class + 6 kit), mcd=120 (all gear), total=182. ✓
- **Zero E1-469 members in the delete set** — asserted two ways against `atlas-frozen-fit-cellkeys-edition1.csv` (the 469 frozen-fit members): `grep` for `la-`/`mcd-` prefixes = **0**, and `comm -12` of the 182 delete-set kit_ids vs the 469 E1 members = **empty intersection**. All 182 carry `source_date='2026-07-15'`, i.e. post-E1 growth. This is the archipelago-mock step-0 assertion (*"LA composition 0; 0 mcd; post-E1 growth"*) discharged at delete time. ✓
- **Provenance fully archivable** — every provenance column (`kit_id`, `folk_name`, `game`, `source`, `grain`, `provenance_tag`, `source_date`, engine-key child state) captured above for all 182. No un-archivable column. ✓
- **Pre-delete backup:** `../corpus.db.pre-dual-hard-delete-2026-07-16-backup` (709 rows, `integrity_check=ok`, sha256 `a47e6cf8…`). Deletion fully reversible from this snapshot + the archive above.

### Post-delete asserts (fail-loud; numbers recorded)
- **Grain census:** `kit`=**509** · NULL=**18** · `gear`=**0** · `class`=**0** · total=**527**. ✓ (509 kit = prior 515 − 6 Destroyer.)
- **`canon_engine_key`:** 683 − 156 = **527** rows; clean 1:1 with `canon_corpus` (every surviving corpus row has exactly one engine-key child; zero orphans). ✓
- **`canon_corpus` total:** 709 − 182 = **527**. ✓
- **Zero `la`/`mcd` rows remain** in `canon_corpus` (and zero in `canon_engine_key`). ✓
- **Served + evidence artifacts byte-untouched** (sha256 verified identical pre/post): `atlas-edition3.json` `38c3bc00…` · `atlas-refit-candidate-1.json` `758126a8…` · `atlas-archipelago-mock.json` `141153bf…` · `atlas-frozen-fit-cellkeys-edition1.csv` `e79042441…`. ✓

### Iron laws honored
- **Edition III + every served artifact READ-ONLY** — byte-verified untouched.
- **Refit-Candidate-1 artifacts READ-ONLY** (permanent evidence exhibit) — byte-verified untouched.
- **archipelago-mock artifacts READ-ONLY** — byte-verified untouched.
- **corpus.db was the ONLY mutation surface.** No re-fit, no re-emission, no atlas artifact touch. The only mutations: `DELETE` of 182 `canon_corpus` + 156 `canon_engine_key` rows.

### Reversibility + reproducibility
Executed by `../scripts/corpus_dual_hard_delete_2026_07_16.py` (fail-loud: asserts the 62/120 counts + zero-E1-membership + provenance-archivable BEFORE deleting; asserts the 527/509/18/0/0 census + 1:1 engine-key + served-artifact byte-equality AFTER; HALTs and rolls back on any mismatch). Fully reversible from `../corpus.db.pre-dual-hard-delete-2026-07-16-backup` + this per-row archive. Deletion is a real state change (carve-out); the archive above is the permanent record that lets the deleted set be reconstructed or re-harvested under the STAGING LAW.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected. Collab-side curation only (elrond data layer).
- Auto-committed per project discipline (Matt-authorized deletion under the wave-2/3 rulings). **Push deferred to gandalf's verify-then-push gate.**

---

## archipelago-mock-2026-07-16 — throwaway census/shape exhibit on E1-469 — 2026-07-16 — **MOCK (ratified:false; nothing served, nothing vendored)**

### What it is (one line)
A **throwaway-class** archipelago mock on Edition-I's 469 active kits, emitting `atlas-archipelago-mock.json` + `archipelago-mock-report.md`. Answers Matt's membership-census question with real numbers and shows the territory-surface shape. **NOT a served artifact; NOT an atlas edition; no G1/G2/G3 gates run.** Both files stamped `mock:true, ratified:false`. Logged here for provenance only — this is not a schema migration; no corpus.db change (consumes Part A's `grain` column read-only + the E1 coordinates CSV).

### Census headline (the deliverable)
Of 469: **cores 130** (27.7%, the six named islands) · **islets 213** (45.4%, 27 unnamed U-n clusters size>=3) · **straits 0** · **drifters 126** (26.9%, the mainland at sea). Per-family cores: TOTEM-SENTRY 46 · TRAP-MINE 43 · WHIRLWIND 15 · AURA 10 · CHANNELED-BEAM 9 · MINION-PET 7. Ghost: **76 shallows / 263 deep**.

### Method (disclosed, all pinned to SEED=20260716; deterministic — md5-stable across runs)
- **Stage 0 corpus assert (fail-loud, uses Part A `grain`):** all 469 `grain='kit'`; **0 mcd**; **LA composition 0** (post-E1 growth). Kit-grain-clean by construction; no HALT.
- **Clustering:** full 14-dim MCA space (`dim1..dim14`, retained-dims, NOT the 2D plane). **Leiden-CPM consensus** on kNN(k=10), 60 seeds @ res=0.3 (existing `atlas_derivation_2026_07_14.leiden_consensus`). **66 clusters, biggest 4.5%** — no degeneracy. **HDBSCAN tried and REJECTED** (degenerate giant cluster 65-72% at mcs 5-10 — the dense MCA core lumps; would trip the >60% HALT). Disclosed.
- **Family labels + tau:** seeded from the 86 gateA ratified labels (6 families). **tau = ABSOLUTE affinity threshold** (distance to nearest same-family seed), **calibrated on a stratified 20% gateA holdout** (18/86) maximizing accuracy x coverage x (1 - mainland-admit). **Chosen tau=0.8**, holdout accuracy 1.000, coverage 0.889, mainland-admit 0.107. *Key correction: a vote-share tau force-assigned the whole mainland and flooded two families to 130-160 members; the absolute-distance tau abstains the mainland as drifters and yields a real archipelago.*
- **Five strata:** core (affinity<=tau) / islet (coherent unseeded cluster size>=3, else drifter) / strait (two families within m=0.15 AND both within tau — **fired 0×**, families are mechanically well-separated) / drifter (below-tau mainland) / ghost (shallows vs deep by family-affinity radius, MOCK approximation over the 469's own footprint — NOT the charter 11,160-cell meso projection).
- **Seating (designed-for-legibility, disclosed as such IN the JSON — NOT measured):** MDS on cluster centroids (full-space euclidean) + within-island local MDS layout + water by fiat. **Tombstones:** E1-469 has 0 negative kits → Finding F-1 (tombstones on HOME island) honored **vacuously**, mechanism disclosed.

### Iron laws honored
No served artifact touched · no existing atlas artifact re-fit/re-emitted · corpus.db unchanged (grain read-only) · Edition III + Refit-Candidate-1 READ-ONLY. **Reproducible** from `../scripts/atlas_archipelago_mock_2026_07_16.py` + `corpus.db` (grain column) + `atlas-coordinates-active.csv`. Auto-committed; push deferred to KR's gate.

---

## grain-law-ratification-2026-07-16 — `grain` column added to `canon_corpus` (kit|gear|class) + THE GRAIN LAW — 2026-07-16 — **APPLIED (Matt-ruled; column ratified)**

### THE GRAIN LAW (ratified — Matt rulings 2026-07-16, verbatim)
> *corpus grain = emission grain. The engine emits kits; the atlas plots what the engine can emit. **Every future fit-stage predicate MUST include `grain = 'kit'`.***

Two Matt rulings, ONE law. Verbatim:
1. **mcd:** *"Exclude the Minecraft Dungeons kits entirely."* → the 120 `mcd-` rows are **gear** grain.
2. **Lost Ark:** *"On Lost Ark, yes we CANNOT emit full classes… I would recommend deleting these entirely rather than decomposing."* → the 56 LA class-engraving rows are **class** grain (excluded from fits). The 6 Destroyer skill-grain rows (`la-destroyer-*`) are **kit** grain and survive. **This is a grain-based reading, not source-based** (gandalf's flagged interpretation — source-based exclusion of the whole `la` source is one predicate change away if Matt prefers; the ruling as written keeps the 6).

Both rulings are recorded in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md § RULING`. One law implements both and closes the failure class that contaminated Refit-Candidate-1: **manual fit-stage holds do not survive predicate rewrites; a ratified column does.** The 94 mcd gear-grain rows leaked into Refit-Candidate-1 precisely because the exclusion lived only in a hand-written stage predicate, not in the data. A `grain` column that every fit predicate references makes the exclusion structural and un-forgettable.

### What changed (one line)
Two additive columns on `canon_corpus`: **`grain` (TEXT ∈ {kit, gear, class}, NULL for non-emittable system-records)** and **`grain_note` (TEXT, provenance/flag annotation)**. Backfilled by provenance-anchored derivation. **Zero deletes** — catalogue philosophy: score/filter at consumption, never purge. Rows stay catalogued **INERT**; only the fit-STAGE predicate filters them out (`grain='kit'`, composed with the existing `row_class='combat-kit' ∧ negative=0 ∧ cell_key NOT NULL`).

### Derivation rules (provenance-anchored — derived per row, never assumed)
Applied in order; the branches are provably disjoint (no `la-destroyer-*` or `mcd` row is a system-record — asserted):
| Rule | Selector | grain | n |
|---|---|---|---|
| Minecraft Dungeons | `game='mcd'` (all `architecture='notable'`) | `gear` | 120 |
| LA Destroyer skill-grain | `game='la' AND kit_id LIKE 'la-destroyer-%'` | `kit` | 6 |
| LA class-engraving | `game='la'` (remainder; all `architecture='class-engraving'`) | `class` | 56 |
| System-record | `row_class='system-record'` (non-mcd/la) | `NULL` | 18 |
| Default (combat-kit) | everything else | `kit` | 509 |

**GRAIN CENSUS (709 rows):** `kit`=**515** · `gear`=**120** · `class`=**56** · `NULL`(system-record)=**18**. (The 515 kit includes the 6 LA Destroyer + 509 other-game combat-kits.)

### The NULL choice for system-records (deterministic, NOT ambiguous)
The 18 `row_class='system-record'` rows (loot-economy / progression / mobility-grammar / modifier-grammar cross-game infrastructure records — e.g. `di-inferno-ladder`, `ud-link-rune-grammar`, `poe1-blood-magic-kit`) are **none of kit/gear/class** on the emission axis. The vocabulary is fixed at `kit|gear|class`; forcing any of them onto a system-record would be a silent lie (a loot-economy record is not a "kit"). They are left **NULL with `grain_note`** — a deterministic, reproducible, documented NULL, **not** an ambiguity flag. They are already excluded from every fit by `row_class='combat-kit'`, so the composite GRAIN LAW predicate (`grain='kit' AND row_class='combat-kit'`) never depends on their grain value. Marking them `kit` for tidiness was rejected: honesty over convenience (Discipline #14 spirit — do not encode a value the data does not support).

### FLAG LIST (grain-ambiguous, resolved-per-ruling — 2 rows, under HALT threshold 20)
Two Destroyer rows carry conflicting provenance signals:
- `la-destroyer-rage-hammer` ("Rage Hammer Destroyer")
- `la-destroyer-gravity-training` ("Gravity Training Destroyer")

Their **kit_id prefix** (`la-destroyer-*`) says skill-grain → `kit`; their **architecture column** (`class-engraving`) says `class`; and their **folk_name pattern** (`<Build> Destroyer`, suffix form) matches the 56 class-grain rows, unlike the other 4 Destroyer rows (`Destroyer — <Skill>`, em-dash form, `architecture` empty). Matt's ruling is explicit and authoritative that **all 6 Destroyer rows are kit-grain citizens**, and the kit_id-prefix reading yields exactly the ruled 6/56 split. Both rows are therefore set `grain='kit'` **per the ruling**, each carrying a `grain_note` recording the architecture conflict so the source-vs-grain tension stays visible on inspection. If Matt prefers the architecture-column reading (58 class / 4 kit), it is a one-line re-derivation; the ruling as written (6 kit) is implemented.

### Reversibility + reproducibility
`grain` is fully re-derivable from provenance columns (`game`, `kit_id`, `architecture`, `canon_engine_key.row_class`) via `../scripts/corpus_grain_ratification_2026_07_16.py`, which is idempotent (re-running re-derives to identical values) and fail-loud (asserts the ruling arithmetic: gear=120, class=56, LA-kit=6, vocab-clean, flags≤20, zero non-system NULLs). No raw value is destroyed; the column is additive.

### Iron laws honored
- **Edition III + every served artifact READ-ONLY** — untouched.
- **Refit-Candidate-1 artifacts READ-ONLY** (permanent evidence exhibit; Matt's mcd ruling makes it never-adoptable) — untouched.
- **No re-fit / no re-emission** of any existing atlas artifact in this migration. The only mutation is the additive `grain`/`grain_note` backfill on `corpus.db`.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected. All work is collab-side curation (elrond data layer).
- Auto-committed per project discipline (Matt-authorized implementation under the GRAIN LAW rulings). Push deferred to KR's gate.
- **Consumer note for every future fit author:** the fit-stage predicate is now `grain='kit' AND row_class='combat-kit' AND negative=0 AND cell_key IS NOT NULL`. Do not hand-hold the mcd/LA exclusion in the predicate text — reference the ratified `grain` column. That is the whole point of the law.

---

## refit-candidate-1-ledger-honesty-2026-07-16 — surgical fit-relative ghost-field ledger correction (emission-side only) — 2026-07-16 — **APPLIED (comparison artifact; Matt adoption still pending)**

### What changed (one line)
Two ghost-field census ledgers in `atlas-refit-candidate-1.json` were carried byte-verbatim from Edition III into an emission whose FIT membership had changed. `off_plane_corpus` (declared 94 off-plane) was FALSE — all 94 `mcd-` gear-grain kits are on-plane points in the refit — and was RE-DERIVED to the honest fit-relative value (**26**). `unmapped_pending_curation` (114) was investigated and found NOT stale — it is a *lit-map census*, TRUE by re-derivation — but was rendering misreadably on the plate, so a **`unmapped_pending_curation_disclosure`** semantics field was ADDED (count + list bytes untouched). Emission-side ONLY: no coordinate, fit, drill-in, `p_df_1`, `plane_alignment`, or lattice change. Lattice byte-identical (`depth_sum_check` = 767,411,820). No "Edition IV"/"edition4" string introduced.

### The defect and the non-defect (provenance)
- **Ledger 1 — `off_plane_corpus`: STALE fit-relative fact.** Edition III served `{gate_rejected_keyed: 94, kits: [94 mcd gear kits], n: 94}`. The refit's stage predicate (**combat-kit ∧ cell_key NOT NULL ∧ negative=0 → 628**) ADMITTED all 94 keyed gear-grain kits as on-plane points (94/94 overlap with `points[].kit_id`). Honest re-derivation: `gate_rejected_keyed: 0` (the stage gate rejected none of the keyed 94) · `n = kits = 26` (the mcd rows carrying no cell key — they never entered the fit; 0/26 overlap with points) · `n_mcd_total: 120` · `unresolved_no_key: 26`. The `kits` list is now the 26 no-key kit_ids (identical to `unresolved_no_key_kits`, which is correct: under this fit the off-plane kits ARE exactly the no-key kits).
- **Ledger 2 — `unmapped_pending_curation`: NOT stale (register/lattice-level census, TRUE by construction).** The 114 are kits lacking a `fit2reg_movement` mapping (movement=blank) and thus absent from the lit-lattice census — re-derived from the refit's OWN `lit_map` to the byte-identical set of 114. "Unmapped" = not present in the lit-map, NOT off-plane; all 114 are nonetheless plotted as on-plane points. The count is genuinely TRUE. It went *misreadable* (not false) in the refit because in Edition III 94 of the 114 weren't plotted there, so the footer wasn't ambiguous; in the refit all 114 are plotted, so the plate needed the fit-relative `..._disclosure` field to prevent "unmapped" being read as "off-plane".
- **Third-stale-field audit: NEGATIVE.** `unmapped_would_seal_excluded/_kits` (0/[]) re-derived correct; `depth_by_delivery` (lattice-level) byte-equal and correct; `red3_note` already refit-specific. No further carried-over field is false.

### THE THREE-CLASS FACT RULE (state this so the next auditor does not repeat the error)
A ghost-field emission carries facts of three distinct provenance classes. Byte-equality across fits is a DIFFERENT correctness question for each:

1. **Corpus-level facts** — properties of the corpus rows independent of any fit (e.g. `n_mcd_total = 120`; the 26 no-cell-key mcd rows). **May carry across fits byte-equal.** Byte-equality is fine.
2. **Fit-relative facts** — WHO is on-plane / which kits the stage predicate admitted (e.g. `off_plane_corpus.n`, `.kits`, `.gate_rejected_keyed`). **MUST re-derive per fit against that fit's actual membership.** Byte-carrying these is the defect this entry corrects. Iff you change the fit, you must recompute these.
3. **Register/lattice-level facts** — properties of the register v1.3 lattice + the reg-to-fit mapping census (e.g. the lit-map census / `unmapped_pending_curation`, `depth_by_delivery`, `depth_sum_check`, sealed/feasible denominators). **Byte-equality is CORRECT BY CONSTRUCTION** — the lattice did not move; only the FIT projection of it did. Do NOT "re-derive to a new number"; verify byte-equality and, if the same TRUE number can be *misread* under the new fit's plotting, add a fit-relative disclosure (as done here for the 114).

### Case lineage (why the misdiagnosis happened)
The original charge operated on a **two-class taxonomy** (corpus-level carry vs fit-relative re-derive) and predicted `unmapped_pending_curation` would re-derive to `0 + []` under the refit. That prediction was WRONG: the 114 is a class-3 register/lattice-level census, not a class-2 fit-relative fact. The re-derivation at the HALT surfaced the missing third class. gandalf's RULING added class 3 to the taxonomy precisely because the two-class model caused gandalf's own initial misdiagnosis of the 114. The lesson: before declaring a carried-over census "stale," classify its provenance — a register/lattice census that is byte-equal by construction is not stale, it is correct, and the fix is disclosure (not re-derivation).

### The fix (surgical text replacement — NOT `json.dump`)
The artifact is 6.8 MB (628 points with coordinates). A full `json.dump` re-serialization would drift float formatting across the whole file. The fix was applied as a **byte-level text replacement** of exactly the `off_plane_corpus` block plus a single inserted `unmapped_pending_curation_disclosure` line, with formatting (6-space key indent, 8-space list indent, literal em-dash) matched to the surrounding emission.
- **Fail-loud asserts before write (all PASSED):** `set(off_plane_corpus.kits) ∩ set(points[].kit_id) == ∅` (0 overlap) · `n == len(kits) == 26` · `unresolved_no_key == len(unresolved_no_key_kits) == 26` · `gate_rejected_keyed == 0` · `n_mcd_total == 120` · `unmapped_pending_curation == 114` and its `_kits` list byte-identical to the pre-fix emission · the ONLY new ghost_field key is `unmapped_pending_curation_disclosure`.
- **Rest-of-JSON byte-identical proof:** JSON minus the (replaced) `off_plane_corpus` block minus the (added) `unmapped_pending_curation_disclosure` line == the pre-fix JSON minus its `off_plane_corpus` block, byte-for-byte (SHA-256 `e3d407f8…` on both). Nothing else drifted; `points`/coords/loadings/ghost projections/`drill_in`/`p_df_1`/`plane_alignment`/lattice all BYTE-UNTOUCHED.

### The two disclosure strings (they render verbatim on the plate for Matt's eyes)
- **`off_plane_corpus.disclosure`:** *"94 gear-grain kits (mcd-) were ADMITTED at kit grain by this refit's stage predicate (combat-kit ∧ cell_key NOT NULL ∧ negative=0) and are plotted as on-plane points; the E1-era deferred grain ruling is thereby exercised implicitly and remains OPEN for Matt. 26 mcd rows carry no cell key and remain genuinely off-plane — they are the kits listed here."* (Three mandatory facts: admitted-94 / ruling-OPEN / 26-off-plane.)
- **`unmapped_pending_curation_disclosure`:** *"lit-map census — these 114 kits lack a fit2reg_movement mapping (movement=blank) and are therefore absent from the lit-lattice census; ALL 114 are nonetheless plotted as on-plane points in this refit. 'Unmapped' means not present in the lit-map, NOT off-plane."* (Two mandatory facts: lit-map-predicate meaning / all-114-plotted.)

### Companion corrections
- **Comparison report** `refit-candidate-1-comparison-report.md`: §8 census-table row `off_plane_corpus N` refit column `94 → **26**`; added a "Census note — off_plane_corpus honesty correction" paragraph (the correction + grain-admission disclosure + the 114 lit-map-census clarification + the TRUE 159 new-actives split: **94 mcd gear-grain + 62 Lost Ark [56 class-grain + 6 Destroyer skill-grain] + 3 pull re-keys (d3/di/d4)**, 0 dropped vs Edition-I's 469).
- **Diagnostic script committed:** `../scripts/refit_ledger_honesty_verify_2026_07_16.py` — verify-only (no writes); reproduces the 628-point fit membership from `corpus.db`, cross-checks both carried ledgers, and derives the honest values. Committed WITH this fix as the provenance of both the defect (ledger 1) and the non-defect (ledger 2).

### Not in this charge (routed elsewhere)
- **galadriel re-render + assert #24 retune** — the render fork is galadriel's staged r2 charge (gandalf's chain, amended). No galadriel render script was touched by this fix.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. All work is collab-side curation (elrond atlas tree). Edition III + every served artifact READ-ONLY — untouched.
- **Reversibility:** the honest values are fully reproducible from `../scripts/refit_ledger_honesty_verify_2026_07_16.py` + `corpus.db` + the 628-point set; the correction is a documented, deterministic re-derivation, not a destructive edit.
- **Naming discipline:** "Edition IV"/"edition4" appears in NO code/artifact/stamp/log touched by this fix.
- Auto-committed per project discipline (Matt-authorized surgical fix under gandalf's RULING). Push deferred to KR's gate.
