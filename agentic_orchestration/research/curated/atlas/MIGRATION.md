# MIGRATION — Atlas fit/ghost-field layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema + fact-honesty migrations for the atlas fit artifacts under `agentic_orchestration/research/curated/atlas/` (editions, refit candidates, ghost-field ledgers, comparison reports). Parallels the top-level `../MIGRATION.md` (corpus/register data layer) and star-lord's engine-side `MIGRATION.md` per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

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
