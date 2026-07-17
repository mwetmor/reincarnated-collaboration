# MIGRATION — Catalogue Data Layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema migrations for non-engine data layers under `agentic_orchestration/research/curated/`. Currently: catalogue.db + synty_catalogue.db + (NEW v1.8 / v1.9) engine `data/kit_space/` chronicle (cross-seam co-ownership with star-lord per LOCK K) + (NEW v1.14 LANDED) corpus.db three-layer ingest.
**Pattern:** parallels star-lord's engine-side `MIGRATION.md` files per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

---

## econ-unknown-audit-2026-07-16 — econ:UNKNOWN bucket audit (38 kits classified; 5 fills applied; scoreboard bucket UNKNOWN drops 38 → 33) — 2026-07-16 — **APPLIED**

### What changed (one line)
Audit of the **38-kit econ:UNKNOWN bucket** identified in S2 census V7 §2/§3 (gandalf-prime charge, dc295719). Each of the 38 kit-grain positive UNKNOWN rows was re-read against raw_json (probe.economy + geo_text + mechanics_notes + delivery.evidence + corpus.mech_note) and classified into **(a) DERIVABLE with existing rules — 5 fills**, **(b) needs a NEW mapping rule — 15 kits (rule NOT minted; iron law: no new rules mid-run)**, or **(c) evidence-thin / re-crawl candidate — 18 kits**. WRITE SCOPE strictly limited to the 38 UNKNOWN rows' cell_key economy slot + canon_corpus.flags per iron law 2 — the parallel gandalf Wave-B spec drafter reads PC/RS/AM/RC/LC/DR rows in this same window, and those rows were NOT touched (verified: PC=44, RS=42, AM=16, RC=16, LC=3, DR=2 all unchanged, matching S2 census exactly). Total corpus / kit_grain / cell_key_resolved / dossier_owed all held identical PRE + POST. Post-audit: bucket UNKNOWN=33 (5 kits flipped to expressible — 2 native spend + 3 SU-family which are Wave-A landed).

### Class (a) — 5 fills applied using EXISTING bin vocabulary only

Every fill cites the specific existing rule + evidence phrase. No new bin symbols minted (all target bins already present in `canon_engine_key.economy_model`: `spend` 183-kit precedent; `summon-uptime` 2-kit precedent; SU gap-ledger has 6 prior precedents — 1 solo + 4 RS+SU + 1 HV+SU).

| # | kit_id | new economy_model | new status | new econ_gaps | rule cited | evidence phrase (verbatim from raw) |
|---|---|---|---|---|---|---|
| 1 | `chr-bleed-berserker` | `spend` | native | `[]` | `apply-rules-v1.0.py §4 line 444: if sub in ('spend','cooldown','self-cost'): status='native'` | probe.plain_text: **"Rage spend to activate bleed-strike skills"**; resource_verbatim=`Rage` |
| 2 | `chr-high-ranger-warden` | `spend` | native | `[]` | `apply-rules-v1.0.py §4 line 444` (same rule) | probe.plain_text: **"Focus spent on arrow activation; bleed sustains between shots. Hybrid spend+drain model"**; resource_verbatim=`Focus` |
| 3 | `poe1-baron-zombies` | `summon-uptime` | gap | `["SU"]` | `apply-rules-v1.0.py §4 line 505: SU-mapping (model=summon OR 'minion' in bs_lower OR is_jsum)` + §1 R0b summon_verbs (includes 'zombie'/'minion') + army_horde ('army') | probe.mechanics_notes: **"The Baron helm feeds the caster's stacked STRENGTH into zombie power and life-leech-per-minion — a gear stat on YOUR sheet becomes the ARMY"**; resource_verbatim=`stat→army` |
| 4 | `poe1-siege-ballista` | `summon-uptime` | gap | `["SU"]` | `apply-rules-v1.0.py §1 R0b line 620 is_totem_trap ('turret' keyword)` + §4 SU rule spirit (totem/turret-summons); corroborated by census §5 board 1 (`SU mechanics-demand = 48 (totem-keyed + J-SUM-resolved)`) | probe.mechanics_notes: **"Iron Commander grants +1 ballista per 200 DEX — the attribute stack literally COUNTS your turret army; stat-as-army-size"**; geom=totem (R0b already fired) |
| 5 | `gd-pet-conjurer` | `summon-uptime` | gap | `["SU"]` | `apply-rules-v1.0.py §4 line 505 SU-mapping (summon keyword in delivery.evidence)` + §1 R0b summon_verbs (includes 'summon') | probe.delivery.evidence: **"Full pet menagerie summoned at various positions; fight independently"**; probe.mechanics_notes: "Bysmiel devotion beasts under pet-scaled gear where YOUR stats mean nothing and THEIRS mean everything"; resource_verbatim=`pet-stat` |

**Interpretation of "under-derived at mapping time":** the raw evidence (mech prose, delivery.evidence, or probe.plain_text) contains one of the existing rule's TOKENS or KEYWORDS in an unambiguous economy-context; the probe encoder set `model='other'` (or `model='unknown'`), which triggered §4 line 480 (`elif sub in ('other','unknown'): gaps.append('UNKNOWN')`). The rule itself was correct — the probe was under-derived. Fills apply the rule token that the evidence supports. **No new bin values introduced.**

### Class (b) — 15 kits blocked pending SPEC AMENDMENT (rules NOT minted this pass)

Per iron law "no new mapping rules mid-run", the following kits stay UNKNOWN. They are queued as **amendment-candidate rule sketches** for a future gandalf spec pass:

| # | kit_id | resource_verbatim | proposed rule sketch |
|---|---|---|---|
| 1 | `d2-fireclaw-wolf` | `form lock` | New rule: shapeshift-form-lock economy → SS bin (form-lock as identity) OR native (spend on mana beneath form). Cross-cuts `mechanic:shapeshift` (GX-02 docket). |
| 2 | `d2-fury-wolf` | `form lock` | Same as #1 (shapeshift-form-lock family). |
| 3 | `d2-rabies-wolf` | `form lock` | Same as #1. |
| 4 | `d3-invoker-thorns` | `stat→damage` | New rule: retaliation-thorns economy (aura-pulse delivery + `stat→damage` resource_verbatim + damage-BY-being-hit prose) → TH bin (thorns-retaliation, novel bin). |
| 5 | `d3-lod-archetype` | `item-count` | New rule: itemization-multiplier meta-economy (per-ancient-legendary scaling) → IT bin (itemization-meta, novel). Really a meta-progression economy. |
| 6 | `d4-thorns-barb` | `stat→damage` | Same as #4 (thorns-retaliation family). |
| 7 | `gd-retaliation-warlord` | `stat→damage` | Same as #4. |
| 8 | `poe1-whispering-ice` | `stat→damage` | New rule: item-granted stat-scaled auto-cast (Icestorm autocast at INT threshold; staff-borne skill) → SC bin (stat-scaled auto-cast). Different from #4 (offensive, not retaliation). |
| 9 | `vs-phieraggi` | `revive-stock-as-power` | New rule (vs-specific): revive-stock-as-power (unspent extra lives = damage multiplier) → RV bin (revive-multiplier). |
| 10 | `vs-red-death` | `unlock-trophy` | New rule (vs-specific): unlock-trophy character (meta-economy: unlock requirement is the "investment"; per-run is SP-base auto-fire) → UT bin. |
| 11 | `vs-vlad-dracula` | `unlock-trophy` (Castlevania DLC) | Same as #10. |
| 12 | `d2-bowazon` | `stamina/none` | New rule: no-separate-resource weapon kit (probe encoded 'none'; underlying is mana-spend on Multishot/Strafe) → NR bin (no-resource; weapon-only cadence) OR reclassify as native spend on mana. |
| 13 | `d2-kicksin` | `none` | Same as #12 (Dragon Talon has mana cost). |
| 14 | `d2-smiter` | `none` | Same as #12 (Smite has mana cost). |
| 15 | `d2-zealot` | `none` | Same as #12 (Zeal has mana cost). |

**Spec-amendment sketch families identified:**

- **SS (shapeshift-form-lock)** — 3 kits (d2 wolves); cross-cuts mechanic:shapeshift (GX-02 docket). Rule sketch: `resource_verbatim='form lock' → SS OR native (mana beneath form)`.
- **TH (thorns-retaliation)** — 3 kits (d3-invoker-thorns, d4-thorns-barb, gd-retaliation-warlord). Rule sketch: `aura-pulse delivery + stat→damage resource + "damage BY being hit" / "retaliation" prose → TH`.
- **SC (stat-scaled auto-cast)** — 1 kit (poe1-whispering-ice). Rule sketch: `item-granted skill + stat→damage resource + auto-cast prose → SC`.
- **IT (itemization-meta)** — 1 kit (d3-lod-archetype). Rule sketch: `item-count resource_verbatim (per-legendary scaling) → IT meta-bin`.
- **RV (revive-multiplier)** — 1 kit (vs-phieraggi). Rule sketch: vs-specific `revive-stock resource → RV`.
- **UT (unlock-trophy)** — 2 kits (vs-red-death, vs-vlad-dracula). Rule sketch: vs-specific `unlock-trophy resource → UT meta-bin (per-run underlying is SP-base auto-fire)`.
- **NR (no-resource weapon)** — 4 kits (d2-bowazon, d2-kicksin, d2-smiter, d2-zealot). Rule sketch: `resource_verbatim in ('none','stamina/none') + weapon-attack kit → NR (accept 'free' bin already in cell_key precedent, 48 kits) OR reclassify as native spend on mana`. Note: cell_key economy slot for these 4 kits already reads `free` (a legacy artifact from a different pipeline) — the econ_gaps ledger conflicts. Amendment should ratify `free` as an accepted native bin OR redirect these to spend.

**No new bin symbol minted in this pass.** Gandalf-side spec author reviews and rules on which sketches to promote (each of SS/TH/SC/IT/RV/UT/NR would require rule-table extension in `apply-rules-v1.0.py §4`).

### Class (c) — 18 evidence-thin kits (flagged `econ-audit-ambiguous-2026-07-16`)

The following kits carry conf<0.5 economy probes OR explicit dossier-owed / SEARCH-DERIVED / POST-CUTOFF language in mech_note. Evidence at rule-time was insufficient to derive economy; a re-crawl is the resolution path.

All 18 kits received `flags += 'econ-audit-ambiguous-2026-07-16'` on canon_corpus.

**Re-crawl candidates for a future Legolas batch (18 econ-audit + 2 unknown-ailment = 20 total):**

Econ-audit (18):
- `d2-wl-abyss` — Warlock magic-school (RotW post-cutoff)
- `d2-wl-echoing-strike` — Warlock flagship melee (RotW post-cutoff)
- `d2-wl-fire` — Warlock fire-school (RotW post-cutoff)
- `d2-wl-void-rift` — Warlock void-rift (RotW post-cutoff; mechanics unharvested)
- `d4-blazing-abyss-warlock` — Warlock caster path (fire zones + Hell Fracture; post-cutoff)
- `d4-dread-claws-warlock` — Warlock melee-caster (hatred/abyss resource fantasy; post-cutoff)
- `d4-hammerdin-paladin` — Blessed Hammer (post-cutoff; details thin)
- `d4-rabies-lacerate` — Rabies+Lacerate druid (post-cutoff; also shapeshift-adjacent)
- `gd-berserker-wereforms` — FoA mastery (post-cutoff; also shapeshift GX-02 docket)
- `poe1-heavy-strike-stun` — 3.28 stun-scaling (post-cutoff; details thin)
- `poe1-kinetic-fusillade` — 3.27 wand-rework build (post-cutoff; dossier owed)
- `poe2-archmage-totems` — PoE2 mana-scaled totems ("no cost" reference; post-cutoff)
- `poe2-shaman-bear` — PoE2 druid bear-shapeshift (post-cutoff)
- `poe2-snipe-mirage-deadeye` — PoE2 channeled sniper ("channeled" in tertiary cite; post-cutoff)
- `poe2-spiral-volley` — PoE2 spear archetype (post-cutoff)
- `poe2-walking-calamity` — PoE2 autobomber (post-cutoff)
- `poe2-whirling-assault-ma` — PoE2 martial-artist (post-cutoff)
- `vs-out-of-bounds-freeze` — VS 1.13+ arcana-slot investment (post-cutoff era caveat)

Unknown-ailment companion list (2, per charge — no action this pass; listed for the same future batch):
- `di-warlock-launch` — Warlock (launch state)
- `di-spiritform-druid-pvp` — Spirit-Form Druid (complaint-tier)

### Bucket-count deltas vs S2 census V7 (baseline dc295719)

| Bucket | V7 (pre-audit) | Post-audit | Δ | Status |
|---|---|---|---|---|
| econ:UNKNOWN | 38 | **33** | **−5** | 5 kits fill/unblock |
| econ:SU | 6 | 9 | +3 | 3 SU-fills (Wave-A landed → expressible-now) |
| econ:PC | 44 | 44 | 0 | FROZEN per iron law 2 (unchanged, verified) |
| econ:RS | 42 | 42 | 0 | FROZEN (unchanged, verified) |
| econ:AM | 16 | 16 | 0 | FROZEN (unchanged, verified) |
| econ:RC | 16 | 16 | 0 | FROZEN (unchanged, verified) |
| econ:LC | 3 | 3 | 0 | FROZEN (unchanged, verified) |
| econ:DR | 2 | 2 | 0 | FROZEN (unchanged, verified) |
| econ:HV | 4 | 4 | 0 | Wave-A landed (unchanged) |
| econ:BT | 8 | 8 | 0 | Unchanged (small-add bucket) |

**Scoreboard impact (V8 rerun projection):** 2 kits flip to expressible-now (chr-bleed-berserker, chr-high-ranger-warden = spend/native); 3 kits flip to expressible-now (poe1-baron-zombies, poe1-siege-ballista, gd-pet-conjurer = SU / Wave-A landed). Corpus expressible: 213/523 → 218/523 (+5 → 41.7%). Total expressible: 258/568 → 263/568 (46.3%).

### Iron-law + HALT compliance
- **Backup filename:** `corpus.db.pre-econ-audit-2026-07-16-backup` (integrity_check=ok verified pre-run).
- **PRE + POST asserts held identical:** total_corpus=585, total_engine_key=585, kit_grain=566, null_grain=19, cell_key_resolved=562, bt_sentinel=1, orphans=0/0, dossier_owed=4. Transactional; rollback on any breach.
- **Write scope strictly limited:** 5 canon_engine_key rows (cell_key economy slot + economy_model + econ_status + econ_gaps) + 18 canon_corpus.flags appends. Nothing else touched. The parallel gandalf Wave-B PC/RS/AM/RC/LC/DR reader window is preserved (bucket counts verified unchanged).
- **No new mapping rules minted.** 15 amendment-candidate sketches queued for gandalf spec drafter (list above).
- **Every fill carries evidence citation** (verbatim raw text quoted in the table above; rule citations point to specific line numbers in `apply-rules-v1.0.py §4`).
- **Auditability:** every affected kit has `corpus_schema_meta` marker `econ-unknown-audit-2026-07-16`; ambiguous-class kits carry a `flags`-column trail; class (a) fills reproducible via the (rule, evidence) pair.
- **ADR-004:** no engine-telemetry change; star-lord-side MIGRATION.md unaffected. Push deferred to gandalf's verify-gate per charge terms.

### Artifacts (this entry)
- **Script:** `scripts/corpus_econ_unknown_audit_2026_07_16.py`
- **Backup:** `corpus.db.pre-econ-audit-2026-07-16-backup` (integrity_check=ok)
- **Schema-meta marker:** `econ-unknown-audit-2026-07-16` in `corpus_schema_meta`
- **Flags trail:** `econ-audit-ambiguous-2026-07-16` on 18 canon_corpus rows (class c)

---

## refit-candidate-1-2026-07-16 — REFIT CANDIDATE 1: game-code normalization (R0) + full re-derivation on the 628-active corpus (Lost Ark + pull/MELEE live) — 2026-07-16 — **EMITTED (comparison artifact; Matt adoption pending)**

### What changed (one line)
A **comparison EXPERIMENT, not an Edition** (Matt 2026-07-16: *"run the full Tier 3 with Last Ark and Pull/Gravity … I want to see both versions so we can make a decision."*). The atlas FIT is fully RE-DERIVED on the CURRENT 628-active corpus (incl. 62 Lost Ark + pull as a live feature column), emitted ALONGSIDE Edition III as **`Refit-Candidate-1`**. The string "Edition IV" appears NOWHERE. Same pre-registered methodology, same SEED 20260714, FUSE_MIN=10 unchanged. **Edition III and every served artifact are READ-ONLY — git confirms all served atlas files byte-unchanged.** Register v1.3 lattice byte-identical (the SPACE did not move; only the FIT projection did). Gates A–D re-run as EVIDENCE (not emission blockers): **A FAIL 0.451 · B FAIL k=12 · C gandalf-rules R²=0.168 PERMDISP-sig · D PASS 2.26%.**

### R0 — game-code normalization (elrond's parked to-do, now load-bearing)
The active set carried long-form `canon_corpus.game` codes that orphan the derivation's `FRANCHISE_ROLLUP` (stage-0 HALTs on them). Normalized full-table (idempotent): `lost-ark`→`la` (62), `diablo-4`→`d4` (1), `diablo-3`→`d3` (1), `diablo-immortal`→`di` (1) = **65 rows updated**. `mcd` (already short) left. No `cell_key`/`kit_id` touched (game absent from cell_key → frozen Edition-I fit unaffected; served Edition-III reconstruction unperturbed). Post-asserts (no long form survives; every active game short-code; merge accounting balances) PASSED. Schema-meta marker `gamecode-normalize-2026-07-16` stamped.
- **Script:** `scripts/corpus_gamecode_normalize_2026_07_16.py` · **Log:** `corpus-curation-gamecode-normalize-2026-07-16-log.md` · **Backup:** `corpus.db.pre-gamecode-normalize-2026-07-16-backup` (gitignored safety net; the LOG is the record).

### R1 — the derivation fork (surgical deltas only)
`scripts/atlas_refit_candidate_2026_07_16.py` forks `atlas_derivation_2026_07_14.py`. ONLY changes: N re-derived from predicate (628, fetch==COUNT asserted); `FRANCHISE_ROLLUP += la→"LostArk", mcd→"mcd"` (13 franchises, zero orphans); **PULL pre-assert** (function=pull active=**10 = FUSE_MIN exactly**, zero margin → survives Greenacre fusing, earns a fit column; would HALT if it fused — FUSE_MIN never lowered); **MELEE per-field parse** (delivery=melee=**31** earns a column; naive `LIKE '%|melee|%'`=271 confirmed as the range=melee collision — NOT used); Gate-A 86 labels asserted present; output paths → refit-candidate names (served CSVs never over); Gate-A/B/C/D re-run+report as evidence; durable `refit-candidate-1-fit-cellkeys.csv` (628 keys) emitted for the ghost-field rebuild. DB tables written refit-suffixed (`atlas_gateA_labels_refit_candidate_1`, `atlas_franchise_rollup_refit_candidate_1` — Edition-I's tables untouched).
- **Key derivation findings:** retained dims **17** (vs Edition-I 14); plane corrected-inertia **8.903%** (vs 8.36%); plane diameter 5.295. Gate report: `refit-candidate-1-gate-report.md`; full stdout: `refit-candidate-1-derivation-run.log`.

### R2 — supplementary graveyard projection
The **37** projectable negatives (unchanged; re-asserted) projected into the NEW 17-dim retained space via the same CA supplementary transition formula → `refit-candidate-1-coordinates-supplementary.csv`. Gate-B intrinsic-red pool grew 5→12 (more corpses project cleanly in the larger space).

### R3 — ghost field, refit basis (pull + MELEE UN-MASKED)
`scripts/ghost_field_refit_candidate_1.py` forks the ghost-field machinery at the module level: builds the fit from the 628 snapshot (NOT the frozen 469), projects the SAME register v1.3 lattice through the NEW basis. **`REG2FIT["function"]["pull"]="pull"`** (un-masked — pull now has a real fit column) and **`REG2FIT["delivery"]["MELEE"]="melee"`** (un-masked — MELEE ghost-image collapse partially closes). **Denominators asserted BYTE-IDENTICAL to v1.3:** meso feasible **11,160** / sealed **1,314** (L1 756 + L2 558) / depth_sum **767,411,820** / pull slice 1,080+54. Un-masking relocates WHERE pull/MELEE cells land (honest coords for 1,080 pull + 1,674 MELEE feasible cells), not HOW MANY exist. Lit census read live: 202 lit / 4 pull-lit / 0 melee-lit / 114 unmapped / 94 off-plane — all identical to Edition-III (same corpus).

### R4 — emission
`scripts/build_atlas_refit_candidate_1_json.py` (forks the edition3 emitter but does NOT freeze-against-E1 — the fit MOVED). Emits `atlas-refit-candidate-1.json` (4.25 MB, schema-compatible with `atlas-edition3.json`: basis/counts/loadings/points/ghost_field/register_ref + stamps; `atlas_version="Refit-Candidate-1"`, `ghost_field.edition="Refit-Candidate-1"`, `unratified_comparison_artifact=true`, `emitted_alongside="atlas-edition3.json (served truth; Matt comparison pending)"`; counts **628/37/665**) + `refit-candidate-1-coordinates.csv` (slim diff). Fail-loud guards: refuses to write any served artifact path; depth_sum must equal v1.3 exact.

### R5 — comparison report (THE decision surface)
`atlas/refit-candidate-1-comparison-report.md` — numbers only (gandalf synthesizes). Headlines: **plane (dim1×dim2) Procrustes congruence 0.468** (RMS displacement **19.94% of plane diameter** on the 469 shared actives — the 2D plane moved substantially) BUT **full 14-dim congruence 0.860** (the high-dim structure is far more preserved than the plane); axis-identity correlations E1-dim1↔refit-dim1=0.64 with off-diagonals ~−0.40 (axes rotated/mixed); 6 gateA centroid shifts (WHIRLWIND 33% / CHANNELED-BEAM 31% highest, TRAP-MINE 5.6% lowest); LA landings (6 Destroyer skill-grain w/ 5 nearest neighbors each — the recon's "4" was an estimate; 56 class-grain centroid (−1.24,−0.19) spread 8.6%); the 10 pull kits mean pairwise 12.6% of diameter, 23.8th percentile of a random-10 null (modestly cohesive); fuse-table delta (geometry=aura un-fuses; pull absent from E1's 469 vocabulary now earns a column); gates old-vs-new; ghost-field deltas.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. All work is collab-side curation (elrond research tree). Read-only on every served artifact — **git status confirms zero modification** to atlas.json / atlas-edition2.json / atlas-edition3.json / atlas-coordinates-*.csv / atlas-loadings.csv / atlas-frozen-fit-cellkeys-edition1.csv / 2026-07-14-gate-report.md.
- **Reversibility:** the refit is fully reproducible from version-controlled scripts + the fit-cellkeys snapshot; R0 preserves original long forms in this log + the migration script (idempotent); corpus.db backup is a local safety net (gitignored — scripts+logs guarantee rebuild).
- **Naming discipline:** "Edition IV"/"edition4" appears in NO code/artifact/stamp/log. If Matt adopts after comparison, adoption ratifies Refit-Candidate-1 as Edition IV by Matt's authority (separately scoped; §7 sim-falsification waiver recorded at that time per gandalf's spec).
- Auto-committed per project discipline (Matt-authorized Tier-3 comparison work). Push deferred to KR's gate.

---

## edition-3-2026-07-15 — EDITION III: pull-7 re-insertion + Lost Ark 58 curation + register v1.3 + Edition-III emission (ONE BATCH) — 2026-07-15 — **LANDED (awaiting Matt freeze-ratify)**

### What changed (one line)
Edition-III is a **census-population edition** (Matt: *"Edition 3: one batch"*): the census-freeze lifted, the 7 pull-tranche rows RE-INSERTED + keyed, the **Lost Ark 58-row class-engraving tranche** curated + keyed, the register re-derived v1.2→v1.3 (lattice UNCHANGED — census grew), and the Edition-III ghost field emitted ALONGSIDE Edition-II. **The FIT layer is byte-frozen vs Edition-I: basis + all 506 point coords + tombstones + axis names untouched; the +65 census rows PROJECT into the frozen basis (not active fit points).** All 24 Edition-III acceptance criteria PASS; P-DF-1 = PASS. Edition-II stays served truth until Matt ratifies the Edition-III freeze.

### Backup
`corpus.db.pre-edition3-2026-07-15-backup` (644 corpus / 618 engine_key). WAL-checkpointed. Local safety net (gitignored per curation discipline); the committed scripts + logs guarantee byte-identical rebuild.

### Stage A — pull-7 re-insertion + keying completion (the DEFERRED tranche)
The 7 pull-tranche rows (inserted-then-reverted under the Edition-II census freeze) RE-INSERTED at full completeness. Corpus 644→651; engine_key 618→625.
- **Ground-truth reconciliation:** brief §0 said corpus=651 (rows "IN, keying deferred"); on-disk truth was **644, rows OUT** (Edition-II revert removed them). Stage A re-inserts + keys.
- **Survivor-baseline reconciliation (why a new script):** the Stage-1 insert script's hard-coded `SURVIVOR_SHA_BASELINE=ce67bfba…` predates the Edition-II Stage-3 pull re-keys (`d3-zbarb`/`di-cyclone-monk-pvp` #5b→pull), so the current survivor digest is `fdd7fbfa…`. The guard fails BEFORE (correctly). NOT bypassed — the new script (`scripts/corpus_edition3_stageA_pull7_2026_07_15.py`) PROVES the shift is fully accounted (current == pre-edition2 EXCEPT exactly the 2 Stage-3 re-keys, #5b only), guards the post-Stage-3 baseline, reuses the Stage-1 manifest (single source), and asserts all 7 cell_keys byte-exact. The Stage-1 module is left unmutated (reverted-batch artifact).
- **Hybrid gate:** both proposed hybrids → `damage`/`pull` per `hybrid-assignment-criteria-2026-07-15.md` §4 (gandalf-adopted). Corpus stays **hybrid-EMPTY**.
- **Four flags:** (a) `la-destroyer-gravity-compression` pull INFERRED → `function=none` (re-verified vs source: "no explicit pull on living enemies"; d4-spiritborn movement source-silent → `mob=blank`); (c) 4 Destroyer SKILL-grain rows distinct + separate grain from the 2 LA engraving-grain rows (grain-of-record adjudicated); (d) `di-cyclone-strike-monk-base` ≠ `di-cyclone-monk-pvp` (distinct cells); (e) Undecember Illusion Hook AFFIRMED EXCLUDED (echo-copy, not pull; bounded to existing evidence).
- **Committed record:** `corpus-curation-edition3-stageA-pull7-2026-07-15-log.md`.

### Stage B — Lost Ark 58-row class-engraving curation
58 rows (29 classes × 2 identity paths, `la-` prefix) keyed at full completeness. Corpus 651→709; engine_key 625→683. Script: `scripts/corpus_edition3_stageB_lostark58_2026_07_15.py`. Raw JSONL preserved verbatim in `raw_json`.
- **Honing-economy confound law (every row):** `amp_val`/`tempo_val` keyed from CLASS-DESIGN cadence (BURST→spiky/high; SUSTAINED→flat/med), NEVER from honing-scaled magnitude prose. Confound carried in `flags` + `mech_note`; never leaks into treatment/function.
- **Six normalizations (with provenance in flags + mech_note; raw preserved):** (1-2) `group_context` absent→false on destroyer×2 + slayer×2; (3) `pull_carrier` absent→false on slayer×2; (4-5) `la-souleater-*` ×2 `legacy_engraving_system` false→**TRUE** (legacy_engraving_name present + Global Dec 2023 debut; Ark-Passive natives are Valkyrie/Guardianknight/Wildsoul ONLY); (6) `la-sorceress-reflux` `pull_carrier` null→**FALSE** RESOLVED via bounded search ("…Reverse Gravity vacuum pull skill"): Reverse Gravity is a tripod-conditioned lift-and-slam (vertical + vacuum-group side effect, framed push/lift), NOT an intrinsic horizontal pull under the register boundary rule + intrinsic bar. PENDING provenance preserved; raw `pull` token kept.
- **Pull census EXACT (2 carriers):** `la-destroyer-rage-hammer` + `la-destroyer-gravity-training` key `ctrl_function=pull` (RIDER on damage identity); all 56 others NOT pull (asserted).
- **Group-support (6, C2):** `la-artist-full-bloom`, `la-bard-desperate-salvation`, `la-bard-true-courage`, `la-gunlancer-combat-readiness`, `la-paladin-blessed-aura`, `la-valkyrie-liberator` keyed **combat-kit with `group_context=true` preserved** (solo-legible identity keyed; NOT dropped/negated). Asserted == index census 6.
- **Isotope collapse (flag-c verdict):** 58 rows → 43 distinct cells (34 singleton + 6×2 + 1×3 + 1×4 + 1×5). Same-cell coexistence at atlas grain is LEGITIMATE (element-free key); all 58 rows persist distinct with full provenance; the cell carries `kit_count`. Cross-grain: 6 Destroyer rows all distinct (skill-grain `delivery=melee` vs engraving-grain `at-target`).
- **UPGRADE-OWED conf bands carried in flags** (Valkyrie/Guardianknight ≤0.8, Wildsoul 0.75-0.8, Souleater 0.85, Aeromancer tier-uncited); categorical keys not blocked; backfill = REGISTERED future legolas item.
- **Naming:** Dragonknight = Guardianknight (index resolution stands).
- **Treatment×function (58):** damage/knockback 33 · damage/none 18 · damage/stun 3 · damage/expose 2 · damage/pull 2. All damage-primary — no forced hybrid/control.
- **Committed record:** `corpus-curation-edition3-stageB-lostark58-2026-07-15-log.md`.

### Stage C — register v1.2 → v1.3 (census population; lattice UNCHANGED)
Generator: `scripts/feasibility_cuts_register_v1_3_2026_07_15.py`. Artifacts: `atlas/feasibility-cuts-register-v1.3.{md,csv,json}` + `atlas_feasibility_ladder_v1_3_2026_07_15` table.
- **The load-bearing property:** LA class-kits add NO coordinate value → enumeration base + cut ledger UNCHANGED → **feasible-lattice denominators BYTE-IDENTICAL to v1.2** (independently re-derived first-principles): exact **767,411,820** / meso **11,160** / sealed **1,314** (L1′ 756 + L2 558) / pull slice **1,080 feasible + 54 sealed**. Denominators RE-ASSERTED, not superseded (charter §6 frozen-frame/versioned-occupancy).
- **Census population (the ONLY delta):** corpus 644→709; active 563→628; occupied meso 193→**202** (+9); pull-lit 2→**4** (+2); unmapped 108→**114** (+6 documented: 1 honest-NULL movement d4-spiritborn + 5 MELEE-collapse — delivery=melee has no meso ghost image).
- **Pull-slice re-vet under larger census:** all 4 lit pull cells FEASIBLE; **`new_law_needed=0`, HALT=False**. No new law needed (asserted). No HALT branches.
- **Re-keys forced on existing rows: NONE** (batch additive; LA engraving-grain cross-refs skill-grain but does not contradict; Edition-II Stage-3 re-keys stand).
- **Schema change: NONE** (additive analysis table only; no engine-side migration owed).

### Stage D — Edition-III ghost-field emission (ALONGSIDE Edition-II)
Emitters: `scripts/ghost_field_edition3.py` + `scripts/build_atlas_json_edition3.py` → `atlas/atlas-edition3.json` (7.49 MB). Acceptance: `scripts/edition3_acceptance_2026_07_15.py` (**24/24 PASS**).
- **Frozen-basis gate RESPECTED (charter §6):** new rows PROJECT into the frozen Edition-I basis via CA supplementary formula (pull/silence/hybrid/MELEE/SUMMON masked-like — no fit column, cannot bend an axis); basis NOT re-derived. The +65 census rows are NOT active fit points (fit stays 469 active / 506 total, Edition-I-frozen).
- **FIT layer byte-frozen ASSERTED in-script (receipts, all PASS):** basis block byte-identical to `atlas.json`; all 506 point coords byte-identical; tombstone `death_class` strings byte-identical; active==469; total==506.
- **Edition-II preserved (never overwritten):** `atlas-edition2.json` asserted present + Edition-II before emit; confirmed byte-untouched vs git HEAD (git-clean on edition2.json + register-v1.2). Edition-II stays SERVED TRUTH until Matt's freeze-ratify + re-vendor.
- **Lattice + pull integrity (receipts):** depth_sum == **767,411,820** (unchanged); lit reproduces (202); 10 pull kits all intrinsic-evidence; **ZERO mcd-lit**.
- **Emitted ghost field:** 11,160 feasible + 1,314 sealed; **202 lit** (was 193); **4 pull-lit** (was 2); drill-in 172,312 sub-feasible + 10,136 RED-3- sealed; off-plane N=94; **P-DF-1 PASS**.
- **Committed record:** `corpus-curation-edition3-stageCD-register-emission-2026-07-15-log.md`.

### Numbers of record (post-Edition-III batch)
corpus **709** (+65) · engine_key **683** (+65) · active combat-kit **628** (+65) · corpses **38** (0) · system-records **18** (0) · unresolved **39** (0, all pre-existing) · pull-function rows **10** (+8) · hybrid **0** (frontier honest) · occupied meso **202** (+9) · pull-lit **4** (+2) · feasible lattice **767,411,820** exact / **11,160** meso / **1,314** sealed / pull slice **1,080 + 54** (all frozen).

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. All writes elrond-owned (corpus.db + atlas artifacts). Schema change: NONE (additive analysis table only).
- **Reversibility:** every corpus.db write is a stated source-anchored ingest; raw JSONL preserved in `raw_json`; every normalization records the original value; register v1/v1.1/v1.2 retained in git as lineage. Ghost projection fully reproducible from version-controlled artifacts (frozen-fit snapshot + register + emitters).
- **HALT branches: NONE** (no new-law-needed; the one ambiguous evidence call — Sorceress Reverse Gravity — resolved by bounded search under the register boundary rule, not improvised into a law).
- Auto-committed per project discipline (Matt-authorized cycle work: *"please fire elrond"* / *"Edition 3: one batch"*). **Push deferred** to Matt's gate. gandalf audit-verify + Matt freeze-ratify gate the re-vendor.

---

## edition-2-2026-07-15 — EDITION II: pull vocabulary + census-freeze revert + EAST-half drill-in + lattice re-emission — 2026-07-15 — **LANDED**

### What changed (one line)
Edition-II lands the `pull` function vocabulary (register v1.2), REVERTS the census-freeze-violating 7-row pull-tranche insert, re-keys 2 existing kits to pull on intrinsic evidence, and re-emits the ghost field + EAST-half geometry×commit drill-in + every denominator. **The FIT layer is byte-frozen vs Edition-I (r6): basis + all 506 point coords + tombstones + axis names + RIDER-1 + F-1 untouched.** All acceptance 22-28 PASS; P-DF-1 = PASS.

### Stage 1-R — REVERT the 7-row pull-tranche insert (Matt census-freeze ruling 2026-07-15)
Matt: *"Queue the full Lost Ark tranche post-Edition-II… let's not add gravity or anything until post edition 2."* → CENSUS FREEZE: no new corpus rows this edition; the pull VOCABULARY still enters. The prior agent's insert (`corpus_ingest_pull_tranche_2026_07_15.py`, run twice) was reverted.
- **Reverted batch (4 classes):** 7 rows from `canon_corpus` (651→644) + 7 from `canon_engine_key` (625→618); mech_note suffix-append enrichment on `di-cyclone-monk-pvp` + `d3-zbarb` restored verbatim from the pre-insert backup; both `pull-tranche-edition2-stage1-2026-07-15` schema_meta rows deleted (8→6).
- **Revert script (new, idempotent):** `scripts/corpus_revert_pull_tranche_2026_07_15.py`. Backup-before-batch: `corpus.db.pre-revert-2026-07-15-backup` (651 rows). WAL checkpoint.
- **Survivor-integrity proof (in-script, fail-loud):** full `.dump` diff of the reverted DB vs `corpus.db.pre-edition2-2026-07-15-backup` → **0 removed lines; the ONLY additions are the two legitimate Stage-2 register-v1.2 tables** (`atlas_feasibility_cuts_v1_2_2026_07_15` + `atlas_feasibility_ladder_v1_2_2026_07_15`, 19 additive lines). The census (`canon_corpus` 644 / `canon_engine_key` 618) is byte-identical to pre-insert.
- **Baseline correction (audit note):** the brief assumed "the insert was the only batch since that backup"; verified on disk, the Stage-2 register-v1.2 generator ALSO ran post-backup (materializing those two tables) — legitimate Stage-2, OUT of revert scope, retained. The honest identity invariant is "reverted DB == pre-insert backup + exactly the two v1.2 register tables."
- **Committed record:** `corpus-curation-pull-tranche-deferred-2026-07-15-log.md` (records the insert fired AND was reverted; 7 rows QUEUED post-Edition-II).

### Stage 2 — register v1.2 (`pull` function level)
`pull` = inward displacement force (knockback's inverse). function coordinate 10 → 11 levels. Law ledger UNCHANGED and wholly inherited; pull vets under the ratified ledger with **ZERO new laws** (L1′ cannot seal pull since pull≠none; L2 seals SUMMON×solo×pull = 54). **HALT=False.**
- **Independently re-derived (acceptance 22 audit bar), all exact:** exact raw **990,186,120** · post-logical **819,439,740** · post-red-law **767,411,820**; meso raw **12,474** · feasible **11,160** · sealed **1,314** (L1′-composed 756 + L2-composed 558). Pull slice: **1,080 feasible + 54 sealed** (all L2). Numbers reproduce the register generator + JSON EXACTLY.
- **Register v1.2 artifacts:** `atlas/feasibility-cuts-register-v1.2.{md,csv,json}` (md authored this stage; csv/json by the prior agent's `scripts/feasibility_cuts_register_v1_2_2026_07_15.py`). v1/v1.1 retained in git as lineage.
- **Per-cut marginal convention (inherited from v1.1, documented in v1.2 §3/§4):** the `per_cut_removed_*` fields report each cut's ORIGINAL (pre-amendment) predicate footprint on the raw box (a legibility/lineage figure, NOT a denominator). The load-bearing ladder + sealed decomposition + pull slice use the AMENDED predicates via composed survivors and reproduce exactly. Verified: v1.1's published per-cut marginals are the same pre-amendment convention at function=10; v1.2 scales to function=11 (L1′ meso 4,158→4,536; RED-3′ exact 76.2M→83.8M). Not a v1.2 defect.

### Stage 3 — existing-kit pull re-keys (NARROWED to corrections, not additions; C3-style reversible)
- **`d3-zbarb`: function none → pull (FIRED).** Evidence: Ground Stomp Wrenching Smash is a RUNE (intrinsic), 24y radial-nova pull-to-self, 40% CC-res. Treatment stays `damage` (pull is the rune rider). The pull slice's first on-plane light.
- **`di-cyclone-monk-pvp`: function knockback → pull (FIRED).** Evidence: base Cyclone Strike pull is INTRINSIC (no Legendary); the existing `knockback` is the DI engine's force-direction-blind label; the inward vortex IS pull (register v1.2 boundary rule). Treatment stays `control`.
- **`d3-dmo-twister`: DECLINED** (prior ruling stands; asserted untouched, function=none).
- **6 MCD pull kits (mcd-):** flag-resolved (pull vocab landed) + `function=pull` recorded at the DESCRIPTOR level (flags JSON + mech_note). They have NO engine-key row (classless-gear; deferred docket) → NO engine-key row created (freeze), REMAIN off-plane. Key-hygiene, not plane admission (spec §10.1.6).
- **Re-key script (new):** `scripts/corpus_rekey_pull_stage3_2026_07_15.py`. Backup: `corpus.db.pre-stage3-rekey-2026-07-15-backup` (644). Positional cell_key splice (#5b only) — every other slot byte-preserved.
- **Proofs (in-script, all PASS):** 467 survivors byte-identical (only d3-zbarb + di-cyclone-monk-pvp changed, each ONLY at cell_key #5b→pull); declined row untouched; 6 MCD still no engine-key row; counts unchanged (644/618); `lattice_coord` unchanged for re-keyed rows (function ∉ the BC6 prefix — the "lattice_coord batch update" is vacuous for function re-keys, asserted).

### Stage 4 — EAST-half drill-in + full lattice re-emission (census 644 + 2 re-keys)
- **Edition-II ghost emitter (new):** `scripts/ghost_field_edition2.py` — extends Edition-I: `pull` added to REG function vocab; `REG2FIT["function"]["pull"]=None` (masked-like — the frozen fit never saw pull, so it has no column-standard coordinate; projects on the other 6 core coords, EXACTLY as silence/hybrid/MELEE/SUMMON → **basis stays byte-frozen**). New v1.2 denominators; off-plane MCD disclosure; EAST-half drill-in; P-DF-1 scoring.
- **Edition-II atlas.json builder (new):** `scripts/build_atlas_json_edition2.py` → `atlas/atlas-edition2.json` (7.49 MB; Edition-I `atlas.json` preserved as the archived Edition-I artifact). Reads the SAME frozen basis CSVs (never regenerates them). atlas_version "Edition-II"; register_ref v1.2; P-DF-1 verdict.
- **Ghost field (lattice):** 11,160 feasible + 1,314 sealed (L1′ 756 + L2 558) meso cells; **193 lit** (was 192; +1 net); **2 pull-lit cells** = d3-zbarb `[FREE-MOVE,ZONE,damage,pull,solo,active,one-shot]` + di-cyclone-monk-pvp `[WALK,NOVA,control,pull,solo,active,one-shot]`; depth Σ = **767,411,820** exact.
- **EAST-half geometry×commit drill-in (slate #1 ES + #2 EN):** 5,068 EAST-half parent cells (x≥0); **172,312 sub-feasible + 10,136 RED-3- sealed** sub-cells. Grain-scoped seal enum {L1-, L2-, **RED-3-**} — RED-3′ SURFACES here (geometry∈{dash_attack}×commit≠instant), absent at meso. Emission form (steward decision, §10.4.1 intent + §9.1 coincident-aggregation + §10.3.3 ~21× glyph-field law + atlas.json practicality): exact counts + 23-vertex reach hull + render-grid glyph field (distinct @2dp + multiplicity) + seal ledger (pattern) + P-DF-1 extremal; the full 172,312-cell enumeration is reproducible from the emitter (renders as dark GROUND, coincident glyphs aggregated).
- **Off-plane corpus disclosure (§10.4.4):** N=**94** — the keyed MCD gear kits held off by the movement gate (movement=blank); N computed from gate rejections, never hard-coded. (26 unresolved MCD reported separately.)
- **Denominator supersession:** Edition-I `693,146,160` / `10,080` appear ONLY inside the labeled `superseded_edition1` block; anti-`422445240` carries forward. Grep-verified.
- **P-DF-1 (§10.5) scored mechanically at render: VERDICT = PASS.** S_max 2.841 > K_max 1.874 along û=normalize(mean(c_whirlwind,c_channel)); 14 beyond-horizon kits (matches the displacement memo). The EAST drill-in extends the dark BEYOND the whirlwind/beam kits (x-reach 1.258→2.308, y-reach −1.817→−2.436). INTERIOR-1 stays closed (not falsified).
- **Acceptance suite (new):** `scripts/edition2_acceptance_2026_07_15.py` — **25/25 PASS** across criteria 22-28, incl. doctored-input proofs BOTH grains (RED-3- surfaces at drill-in, absent at meso) + the real mcd-forced-past-gate HALT proof (a doctored mcd row lighting a pull cell → emitter RAISES; run on a /tmp DB copy, live corpus.db untouched). Emitter deterministic (byte-identical modulo `emitted_at`).

### Corpus.db final state
`canon_corpus` **644** · `canon_engine_key` **618** · pull-function rows **2** (d3-zbarb, di-cyclone-monk-pvp). WAL checkpointed; integrity_check = ok.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. The Edition-II ghost emitter + atlas.json builder are collab-side curation artifacts (elrond-owned research tree); the FIT layer (star-lord's frozen basis CSVs) is READ-ONLY. No engine consumer contract reshaped.
- **Reversibility:** the revert restores the pre-insert census byte-for-byte; the 2 re-keys are C3-style (from-value recorded in flags + this log + the re-key script); the 7 tranche rows are QUEUED (idempotent re-insert post-Edition-II). Register v1/v1.1 + Edition-I atlas.json retained. Full re-emission reproducible from version-controlled scripts + frozen artifacts.
- Analysis tables `atlas_feasibility_*_v1_2_2026_07_15` (elrond-owned, gitignored) present from Stage 2; no new schema. Auto-committed per project discipline (Matt-authorized Edition-II chain). Push deferred to KR's gate.

---

## displacement-rerun-mcd-confirm-2026-07-15 — Edition-II slate CONFIRMATION re-run over grown corpus (READ-ONLY on frozen layer) — 2026-07-15 — **LANDED**

### What changed (one line)
Re-ran the frozen-Edition-I displacement decomposition over the **grown** corpus (survivors + 94 keyed MCD rows) to CONFIRM gandalf's pre-registered Edition-II drill-in slate. **VERDICT: SLATE HOLDS, unchanged and mcd-invariant** (max |grown − survivor-only| over all 8 regions = **0.0** on mass and n; geometry remains #1 promotable in all 8 regions; P-DF-1 unaffected). **No schema change. No DB write. Every frozen input read-only; survivors byte-reproduced (worst drift 0.00e+00); pre-registration artifacts + r5/r6 captures UNTOUCHED; new files only.**
- **Emitter (new; reproducible, idempotent):** `agentic_orchestration/research/scripts/displacement_field_edition1_rerun_mcd_2026_07_15.py` — imports the original `displacement_field_edition1.py` wholesale (frozen machinery byte-identical), adds only mcd masked-like projection + census. Re-run → identical MD5.
- **New artifacts:** `atlas/atlas-displacement-field-edition1-rerun-mcd.csv` (455 rows + `origin`/`beyond_horizon` cols) + `.json` (rows + regions + mcd census + gate diagnosis). **Confirmation memo:** `atlas/2026-07-15-displacement-rerun-mcd-confirm.md`.
- **Freeze anchors reproduced:** 455 survivor rows exact · ghost hull 22 vtx / 7128 pos / east 1.2581 · survivor beyond-horizon 14 (ids match r5 census verbatim) · r_split 0.434249. All identical to pre-registration commit `c7804393`.

### The load-bearing finding — MCD is predicate-satisfied but PLANE-unmapped (corrects a phrase in the MCD log)
The 94 keyed MCD rows satisfy the SQL predicate (`row_class='combat-kit' AND negative=0 AND cell_key IS NOT NULL`) — the predicate the MCD curation log verified 94/94 — but they are **rejected by the emitter's second gate** (`kit_core_tuple` register-meso crosswalk, applied AFTER the SQL fetch). **0 of 94 light a ghost cell.** Two independent gates:
- **Primary (all 94):** `movement='blank'` → `fit2reg_movement` returns None (maps only full-move/walk/rooted). MCD is **classless twin-stick action-RPG**; a gear item carries no per-kit movement stance in-source, so movement is honestly `blank` — but `movement` is one of the 7 CORE meso slots the join hard-requires. (Structurally the same class as the `attr_val`-NULL the MCD log documents; that one is non-core, this one is core.)
- **Secondary (26 of 94):** `delivery='melee'` → `fit2reg_delivery` has no `melee` image. The MCD melee weapons.
- **Counterfactual (DB not mutated):** if movement were assigned, **68** would map; **26** (melee) would still not. A movement fix is necessary-not-sufficient AND would require inventing a value the source lacks (never-invent). MCD is correctly out.
- **Census:** MCD region distribution N/A (0 mapped). MCD beyond-horizon **0** (verified: all 14 survivor beyond-horizon kits are `commit=channel`; MCD commit dist over all 94 keyed = instant 58 · blank 24 · wind-up 10 · channel 2 — overwhelmingly instant, only 2 channel, neither maps). coresub-on-mcd **0** (vacuous + structural: no separate pre-C3 frozen key for MCD).
- **No number in the MCD log is wrong** — only the phrase "already satisfy the displacement/ghost predicate" over-reaches (SQL predicate ≠ plane-membership). Documented here + in the memo + in the emitter's inline rationale.

### Consequence (Edition-II vocabulary-pass docket)
Two gates would admit up to 68 of the 94 MCD weapons to the displacement plane: (1) a `movement=blank`/classless-gear treatment; (2) admitting `delivery=melee` to the register-meso vocabulary. Both are Edition-II vocabulary decisions (gandalf/Matt own; elrond re-keys once the vocabulary exists) — the same deferral class as the 6 `pull_pending_vocab` kits. Recommended for the Edition-II docket.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. Pure collab-side analytical artifact (elrond-owned research tree); reshapes no engine consumer contract. Auto-committed per project commit discipline (Matt-approved confirmation-gate commission). Push deferred to KR's gate.
- **Reversibility:** read-only on every frozen input; survivors byte-reproduced under runtime assertion (run HALTS on any drift); pre-registration + captures untouched; fully re-runnable (idempotent, identical MD5).

---

## mcd-curation-complete-2026-07-15 — corpus.db +2 FIRST-CLASS COLUMNS + MCD Mode-B ingest completion — 2026-07-15 — **LANDED**

### What changed (one line)
Completed the Minecraft Dungeons Mode-B curation that `corpus_ingest_mcd_2026_07_15.py` began (the predecessor's agent stream timed out mid-run; the DB write itself had landed). This pass promotes two annotations from the `flags` JSON blob to **first-class queryable columns** on the 120 mcd rows: **`architecture` TEXT** (='notable' on all 120 — the INGEST-granting 3-grain label) and **`pull_pending_vocab` INTEGER** (=1 on the 6 frozen-basis pull kits, 0 else). **Additive; every write `WHERE game='mcd'`; all 469 survivor cell_keys byte-identical (SHA `c6933deb…`).** No re-ingest. corpus.db is gitignored; the two scripts + the curation log + this entry are the committed record.
- **Scripts:** `agentic_orchestration/research/scripts/corpus_ingest_mcd_2026_07_15.py` (predecessor ingest) + `agentic_orchestration/research/scripts/corpus_curation_mcd_complete_2026_07_15.py` (this completion pass; idempotent). **Full curation log:** `agentic_orchestration/research/curated/corpus-curation-mcd-2026-07-15-log.md`.
- **Counts:** 122 tabled kit rows → **120 ingested** (2 base-family bows dropped: `mcd-void-bow` + `mcd-twisting-vine-bow`, both fetch-confirmed COMMON/RARE with kept unique variants — Wind-Bow precedent). corpus total 524 → **644**.
- **Annotation landings:** `canon_tier='shallow'` 120/120 (predecessor) · `architecture='notable'` 120/120 (this pass, `WHERE architecture='notable'` → 120) · `pull_pending_vocab=1` on the 6 pull kits (`WHERE unresolved=1 AND pull_pending_vocab=1` → 6; the other 20 unresolved are thin artifacts, `pull_pending_vocab=0`).
- **Unresolved 26** = 6 pull-primary (frozen-basis: inward force, `pull` not an Edition-I function, NOT force-keyed knockback, NO engine-key row) + 20 thin non-combat artifacts. **Keyed 94** carry survivor-compatible 14-field cell_keys.
- **Rekey (`lattice_coord`) DEFERRED** — off critical path. The displacement + ghost field emitters read `canon_engine_key.cell_key` (which MCD's 94 keyable rows ALREADY have, all 94 already in the emitter predicate), NOT `lattice_coord` (consumed by nothing today). The displacement-field re-run is therefore **not blocked on elrond**; lattice_coord materialization is a ~30–45 min queued sub-pass folded into the next atlas-derivation batch, with no field-emitter dependency.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. Pure collab-side curation surface (elrond-owned research tree); the two new columns reshape no engine consumer contract. Auto-committed per project commit discipline (Matt-authorized INGEST commission). Push deferred to KR's gate.
- **Reversibility:** additive columns only; no coordinate value destructively transformed; the `flags` JSON tokens left in place as redundant provenance. Fully re-runnable (idempotent).

---

## displacement-field-edition1-2026-07-15 — atlas displacement field + drill-in slate (READ-ONLY on frozen layer) — 2026-07-15 — **LANDED**

### What changed (one line)
Emitted the **displacement field** over frozen Atlas Edition-I — Δ(kit)=kit_position−own_cell_position for all 455 mapped active kits — the reconstruction error of the 7-core meso instrument at every lit point, plus the pre-registered Edition-II drill-in slate. **No schema change. No DB write. Every frozen input read-only** (atlas.json, atlas-frozen-fit-cellkeys-edition1.csv, atlas-loadings.csv, ghost_field_edition1.py, atlas_derivation pipeline). This entry certifies the freeze was honored: no re-fit, no basis change, new files only.
- **Script (reproducible, deterministic):** `agentic_orchestration/research/scripts/displacement_field_edition1.py`. Reconstructs the frozen fit from the pre-C3 snapshot (reproduces all 469 kit positions to 0.00), reads cell positions from the published `atlas.json → ghost_field.feasible_cells`, reuses `ghost_field_edition1.lit_map` crosswalk verbatim for the join. Re-run → byte-identical CSV + JSON.
- **Deliverables (new files, additive):** `atlas/atlas-displacement-field-edition1.csv` (455 rows × 46 cols: per-kit Δx/Δy/|Δ| + three-part attribution) · `atlas/atlas-displacement-field-edition1.json` (rows + region aggregation + provenance sidecar) · `atlas/2026-07-15-displacement-field-drill-in-slate.md` (memo: method, region ranking, slate, formalized prediction P-DF-1, unmapped list, anomalies).
- **Attribution law:** exact three-part additive decomposition Δ = (A) per-non-core direct pull + (B) core-dilution + (C) core-substitution [frozen-position-key vs live-lighting-key drift]; verified to reconstruct every kit's Δ to 0.0 (machine precision). Term (C) is a curation signal on 70 kits (C3 treatment re-keys + `other-rare` delivery fusions), not a promotable drill-in target — documented in the memo §7.
- **Sanity anchors held (all):** ghost x max 1.25805961; 22-vertex hull; 14 beyond-horizon kits reproduced independently (all +Δx dominated by commit=channel + geometry∈{whirlwind,cone}); 455 rows = 469 − 14 unmapped (unmapped set identical to ghost emitter's).

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. Pure collab-side analytical artifact (elrond-owned research tree), read-only on all frozen Edition-I inputs. Auto-committed per project discipline (Matt-authorized commission). Push deferred to KR's gate.

---

## feasibility-cuts-register-v1-2026-07-14 — corpus.db +2 ANALYSIS TABLES (enumerated feasible lattice) — 2026-07-14 — **LANDED**

### What changed (one line)
The feasibility-cuts register (tracker IV.x-b) enumerated the **feasible kit-identity lattice** (SPACE) from the 13-coordinate register cardinalities minus ratified cut classes, and materialized **2 additive analysis tables** into corpus.db (`atlas_feasibility_cuts_2026_07_14`, `atlas_feasibility_ladder_2026_07_14`). **Zero rows in any existing table altered.** `corpus_schema_meta` NOT bumped (analysis-output tables, not a curation-state change). corpus.db is gitignored; the register `.md` + `.csv` + `.json` + script + this entry are the committed record.
**Script (single reproducible entrypoint):** `agentic_orchestration/research/scripts/feasibility_cuts_register_2026_07_14.py` (regenerates counts ladder, CSV, JSON, and both corpus.db tables from one command).
**Deliverables:** `agentic_orchestration/research/curated/atlas/feasibility-cuts-register-v1.{md,csv,json}`.

### Counts ladder (exact-lattice)
raw naive box **900,169,200** → post-logical (4 cuts) **461,515,320** → post-red-law (1 lattice cut) **422,445,240** = the feasible lattice (coverage denominator). Meso-grain (register rollup / never-demote core): 11,340 → 6,840 (post-cut). Cut classes: **4 logical**, **1 red-law lattice-expressible** (RED-3 movement-damage carve-out; RED-1 co-location + RED-2 anti-synergy stay generation/curation filters — key-invisible, NOT force-fit), **5 taste-CANDIDATES** (proposed, never applied — Matt ratifies one by one).

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. **No engine-telemetry change; star-lord-side MIGRATION.md unaffected.** No engine-side migration owed.
- **Cross-seam contract change?** No — additive analysis tables on elrond-owned corpus.db; no consumer-contract reshape. The register consumes the RATIFIED coordinate-register §2 (untouched) as read-only input.
- **Reversibility:** every cut is a stated predicate; no coordinate value destructively transformed; raw naive box preserved in-register with its R2 pre-cut caveat. Fully re-runnable from script.
- **Distinction preserved:** this is the 13-coord CORPUS-IDENTITY lattice, NOT the engine-native substrate lattice (`substrate-coordinates.md` L4≈1.284e9 / banned box 2.57e9). The two naive boxes are different objects; documented in-register §0.
- Push to remote deferred to KR's gate (Matt authorization). Auto-commit fires (register doc + table) per team commit discipline.

---

## atlas-derivation-2026-07-14 — corpus.db +2 ANALYSIS TABLES (atlas-derivation pipeline artifacts) — 2026-07-14 — **LANDED**

### What changed (one line)
The atlas-derivation pipeline (pinned pre-registration v1.1, all seven jack-ryan Gate-1 amendments applied) executed against the `atlas-prereg-2026-07-14` snapshot and materialized **2 additive analysis tables** into corpus.db, plus a directory of file artifacts. **Zero rows in any existing table were altered** — the 469 survivor cell_keys, the 37 keyed negatives, and every prior column are untouched. `corpus_schema_meta` is NOT bumped (these are analysis-output tables, not a curation-state change; the snapshot marker `atlas-prereg-2026-07-14` remains the data-state of record). corpus.db itself is gitignored; the file artifacts + script + this entry are the committed record.
**Script (single reproducible entrypoint):** `agentic_orchestration/research/scripts/atlas_derivation_2026_07_14.py` (pinned seed 20260714; lineage of `family-discovery-poc-rerank.py`; every gate-report number regenerates from `python3 atlas_derivation_2026_07_14.py`).
**Gate report + artifacts:** `agentic_orchestration/research/curated/atlas/` (`2026-07-14-gate-report.md` + 4 CSVs; no basis draft — see verdict).

### Additive schema deltas (no destructive change; zero existing-row rewrites)
- **`atlas_gateA_labels_2026_07_14`** (kit_id PK, `"group"`, group_intent_rationale) — the frozen Gate-A ground-truth [A1] loaded BYTE-VERBATIM from `agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-a-group-labels.csv`. 86 rows; 6 groups (WHIRLWIND 15 · TOTEM-SENTRY 24 · TRAP-MINE 23 · CHANNELED-BEAM 9 · AURA 8 · MINION-PET 7). Table is DROP-and-recreate on each run (deterministic; content-identical).
- **`atlas_franchise_rollup`** (kit_id PK, game, franchise_rollup) — the [A2] game-series rollup materialized for Gates C/D. 469 rows; 11 franchises (Diablo 156 · PoE 121 · gd 38 · le 34 · TitanQuest 24 · vs 21 · Torchlight 20 · chronicon 17 · hot 16 · undecember 11 · Hades 11). DROP-and-recreate on each run.

### File artifacts (in `curated/atlas/`, committed; corpus.db is gitignored)
- `2026-07-14-gate-report.md` — Stage-0 verification, Stage-1 diagnostics, Stage-2 four-family results, Stage-3 four gates with exact numbers + PASS/FAIL, §amendments (NONE), gate summary. **Numbers only — interpretation is gandalf's (DRIFT-CRITIC).**
- `atlas-coordinates-active.csv` (469 kits: 14 retained MCA dims + Leiden cluster + LCA class + franchise + Gate-A group), `atlas-coordinates-supplementary.csv` (37 projected negatives + death_class), `atlas-loadings.csv` (top-12 |loading| coord=level per retained dim — gandalf names axes from these), `atlas-bootstrap-summary.csv` (per-kit median displacement).
- **`atlas-basis-edition-1-draft.json` NOT emitted** — the decision rule gates basis-draft on all-four-pass; Gate B failed. Per prereg §5 this is the honorable-fallback branch (gandalf/Matt rule, not elrond).

### Result of record (executor reports numbers; does not interpret)
Gate A **PASS** (ARI 0.668; all 6 group silhouettes ≥0.2). Gate B **FAIL** (pooled intrinsic-red k=5 mean-pairwise 2.44 vs null 1.85; p_lower 0.9638 — the 5 red corpses are *dispersed*, not clustered). Gate C **PASS** (franchise R² 0.0757 ≤0.15; PERMDISP p 0.066 ≥0.05 so R² pass-interpretable). Gate D **PASS** (bootstrap 3.60% of plane diameter ≤10%; all 11 LOFO congruences ≥0.968; reweight 0.985). **ALL FOUR PASS: NO.** MCA parallel-analysis retained all 14 dimensions (corrected inertia > null-95 at every dim — high-dimensional association). Leiden-CPM produced 132–469 communities across the entire pinned resolution sweep 0.5–2.0 (no non-degenerate plateau near the 6-group scale) — a numeric result of the pinned parameters, NOT a Louvain substitution (A7 clause: leidenalg+python-igraph were installed and used). §amendments = NONE.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. **No engine-telemetry change** — both tables additive inside elrond-owned corpus.db; no `fight_log`/`export`/`loadout`/telemetry-schema field touched. Star-lord-side MIGRATION.md unaffected. No cross-seam round-trip owed (Principle 6) — the `atlas.json` derived-basis block is NOT emitted (gates did not all pass), so the star-lord/drax renderer contract is unchanged this run.
- **A7 dependency pin:** `leidenalg` 0.12.0 + `python-igraph` 1.0.0 + `stepmix` 3.0.0 user-level-installed this session (were absent); CPM-with-`community_leiden` verified before the clustering stage. No substitution performed → no §amendment triggered.
- **Reversibility (schema principle):** both tables are pure functions of the frozen snapshot + the frozen label CSV; re-run reproduces byte-identically (pinned seed). No raw data transformed.
- Push to remote deferred to KR's gate (Matt authorization).

---

## atlas-prereg-2026-07-14 — corpus.db CURATION BATCH A.5 (the atlas-derivation data snapshot) — 2026-07-14 — **LANDED**

### What changed (one line)
Five hygiene+negatives items landed **additively** on corpus.db to produce the pre-registered data snapshot the atlas-derivation pipeline runs against: (1) mech_note truncation repaired grow-only from the untruncated megaprobe facts JSONL; (2) d2-sacrifice filled + re-keyed off its mint dossier; (3) the 38 negatives keyed through the Layer-3 pipeline (survivor keying fns reused); (4) the 5 no-rule-matched TODOs resolved (all in the 38); (5) a `death_class` provenance column (7-value enum, CHECK-equivalent triggers) tagged per the §A.2 pattern→class map. **The 469 clean survivor cell_keys are byte-identical** (SHA256 `6ac89754…`). `corpus_schema_meta` gets marker version `atlas-prereg-2026-07-14`. Backup: `corpus.db.pre-A5-2026-07-14-backup`.
**Script:** `agentic_orchestration/research/scripts/corpus_curation_a5_2026_07_14.py` (idempotent; imports the survivors' keying functions from `corpus_cell_key_materialize_2026_07_13.py` so negatives key by identical rules).
**Full log:** `agentic_orchestration/research/curated/corpus-curation-a5-log-2026-07-14.md`.

### Additive schema deltas (no destructive change; zero survivor-row rewrites)
- **`canon_corpus.death_class TEXT`** (nullable) + two BEFORE-INSERT/UPDATE triggers (`trg_death_class_enum` / `_ins`) enforcing the 7-value enum (SQLite can't ALTER-ADD a CHECK). Enum: `extrinsic-tuning / extrinsic-itemization / extrinsic-split-scaling / extrinsic-no-lever / extrinsic-content-mix / intrinsic-red / system-evidence`. 26 negatives assigned, 12 NULL (gandalf adjudicates; each flagged on `canon_engine_key.flags`).
- **`canon_engine_key`: +37 rows** (the newly-keyed negatives; d2-sacrifice already had a row → its junk key overwritten). 37 land `row_class='combat-kit'` with a proper 14-field cell_key; `vs-golden-egg-scaling` lands `row_class='system-record'` (§A.2 pattern 11 — evidence, not a kit; NULL cell_key).
- **`v_combat_kits` amended:** `+ AND c.negative = 0`. The combat denominator is now self-documenting: `WHERE row_class='combat-kit' AND negative=0` = **469**. (`v_corpus_substrate` was already `negative=0` — unchanged.)
- **`canon_corpus.mech_note`:** 237 rows grown (grow-only re-extraction from megaprobe facts JSONL; 14 negatives among them). Not a schema change — a value repair.

### Negative-keying discipline (charter §5 Stage 0 — passive categories)
Negative facts rows are **sparse** (delivery + footprint + postmortem only). Recoverable coords land (#2 delivery, #3 amp, #8 proxy, #9 range, #10 tempo, #11 commit, #12 activation, #13 dependency); genuinely-unrecoverable coords are **LEFT NULL (passive)**, never guessed (#1 mob, #4 geometry, #5a/#5b ctrl, #6 def, #7 econ). Geometry is NULL for **all 37** because every negative lands on an ambiguous `(delivery, footprint)` pair (verified against the 478 positive engine-key rows; the atlas_key does not deterministically encode geometry either). Negatives stay `negative=1`, **supplementary-only** — they never shape the denominator or the derived axes.

### Denominator reconciliation (the d2-sacrifice leak)
470→469 combat denominator and 457→456 distinct cells are **exactly the d2-sacrifice leak removal** — 0 survivors held its old junk cell_key `walk|blank|spiky|melee_strike|…`, so the −1 cell is unique to it and no survivor cell was lost. This is the §D.2-4 "the table caught the d2-sacrifice leak" finding, now enacted.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. **No engine-telemetry change** — all writes additive inside elrond-owned corpus.db; no `fight_log`/`export`/`loadout`/telemetry-schema field touched. Star-lord-side MIGRATION.md unaffected. No round-trip owed (Principle 6).
- **Cross-seam contract change?** The combat-denominator read contract changes from `row_class='combat-kit'` to `row_class='combat-kit' AND negative=0`. Downstream consumers (gamora dedup, the derivation pipeline) must adopt the `negative=0` filter — documented here + in the schema-meta note + the curation log. The derivation pipeline is the immediate consumer and treats negatives as supplementary-only by design (charter §5), so it filters natively.
- **Reversibility (schema principle):** raw values preserved (grow-only mech_note; additive columns/rows). Re-runnable from the committed script to byte-identical state. Backup taken pre-batch.
- Push to remote deferred to KR's gate (Matt authorization).

### Leftovers surfaced to gandalf
1. The **12 NULL death_class** corpses (incompatible-class or no-enum-value cases; candidate new value `extrinsic-port` for poe2-concoction).
2. **211 mech_note rows still ≤140** — a Legolas Mode-B re-crawl is the only path to fuller postmortems (re-harvest commission, not a curation step).
3. **geometry/ctrl/def/econ/mob NULL on the 37 negatives** — a targeted Legolas re-probe of the negatives' full mechanics would be needed to place them geometrically; today they are honestly passive.

---

## v2.3 — corpus.db CELL-KEY MATERIALIZATION (strict-13 key → gamora dedup gate) — 2026-07-13 — **LANDED**

### What changed (one line)
Materialized the Matt-ratified **strict-13 cell key** (register §6.1): promoted the 4 non-column coordinates to keyed columns on `canon_engine_key` (`ctrl_function` #5b, `economy_model` #7, `activation_val` #12, `dependency_val` #13), added `resource_verbatim` (display; OUT of key), and serialized `cell_key` — the canonical ordered 13-tuple (#5 = two slots; unknown/blank = literal) — for the **470 combat-kit rows**. **Additive only** (6 new nullable columns; no existing column touched — `econ_status`/`econ_meter_type` explicitly preserved). This is the single execution gate between the ratified key and gamora's dedup v1 (a separate BLOCKED dispatch — dedup NOT run here). `corpus_schema_meta` bumped `2.2 → 2.3`.

### Headline result
**470 combat-kit rows → 457 distinct cells** (strict-13 exact-match — the first read of the collapse structure; 12 multi-kit cells absorbed 13 rows). 49 rows carry ≥1 `unknown`/`blank` literal slot (the never-merge-on-absence footprint). Full detail + per-column distributions + derivation logic + spec-gap flags: `corpus-cell-key-log-2026-07-13.md`.

### Columns added (all `canon_engine_key`, all nullable, combat-kit populated / system-record NULL)
| column | in cell_key? | source | populated (of 470 combat-kit) |
|---|---|---|---|
| `ctrl_function` | yes (#5b) | probe `control` family ailments → §3 element-neutral fn map | 470 (7 `unknown` = mint no-probe) |
| `economy_model` | yes (#7) | probe `economy` family model → §3B 7-value + literal compounds | 470 (43 `unknown`; 2 compounds) |
| `activation_val` | yes (#12) | `mech_note` §3A.1 discriminator | 470 (7 `unknown`) |
| `dependency_val` | yes (#13) | `mech_note` §3A tells | 470 (7 `unknown`) |
| `resource_verbatim` | **NO** (display) | probe `economy` `resource_verbatim` 1:1 | 461 (verbatim, never coalesced) |
| `cell_key` | (the serialization) | 13-tuple join `canon_engine_key ⋈ canon_corpus` on kit_id | 470 combat-kit; 17 system-record NULL |

### cell_key storage decision
**Materialized column** (not a view). gamora needs a stable, index-able `GROUP BY cell_key` target frozen at materialization; a view would re-execute the two-table join per read and expose gamora to mid-flight coord edits. Re-materialize (re-run the idempotent script) if any of the 13 source coords change. `#5` contributes TWO slots — all 470 rows verified = 14 pipe-fields.

### Guardrails honored (handoff §67-72 + KR econ-distinctness note)
Strict-first (never pre-coarsened) · unknown/blank = literal (never coalesced) · #5 = 2 slots · hybrids as literal compounds (`spend+finite`, `spend+cooldown`) · `resource_verbatim` out of key · `economy_model` additive (`econ_status`/`econ_meter_type` untouched: 463 each still populated) · dedup NOT run.

### Spec gaps flagged to gandalf (did NOT guess past)
1. **`draft` economy (2 rows)** — kept `unknown` literal, NOT `finite`. The 2 draft rows are roguelite **draft/offer-pool build-SELECTION** economies (VS-style), not consumable-input `finite`; folding to `finite` would wrong-merge. Candidates for gandalf ruling: new `draft` value / `free` residual / confirm finite.
2. **`dependency_val`** text-derivation runs slightly above the §5 "~70 setup-payoff" estimate (104). Not a gap — a Stage-2 refinement candidate; robust to the strict-key collapse (dependency is a never-demote core coord).

### Verification (idempotent + clean-rebuild reproducible)
- Re-run → byte-identical (`shasum 9e158f59…` of the combat-kit key projection).
- Full clean rebuild from scratch (base → s1 → fold12 → **this**) reproduces the same hash + 457/470 smoke.
- Raw columns untouched; derivations re-computed from committed source every run.

### D6 rebuild sequence (now FOUR committed scripts)
```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py             # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py       # S1 completion (idempotent)
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py              # mint-dossier fold (idempotent)
python3 agentic_orchestration/research/scripts/corpus_cell_key_materialize_2026_07_13.py  # THIS — cell-key materialize (idempotent)
```
corpus.db stays gitignored; scripts + `corpus-cell-key-log-2026-07-13.md` + this entry are the committed truth.

### ADR compliance
- **ADR-004:** this entry. Additive columns on elrond-owned corpus.db; **no engine-telemetry change** → star-lord-side MIGRATION.md unaffected. **Round-trip: NOT APPLICABLE** (no star-lord boundary column implicated — confirmed; no STOP-and-flag triggered).
- **ADR-006:** commit scripts + log + this entry; **NO push** (Matt-gated). corpus.db binary stays gitignored.
- **Reversibility:** all changes re-derived from committed inputs at materialization time; raw columns untouched; re-runnable to byte-identical state.

### Downstream unblock
gamora's dedup v1 (`dispatches/2026-07-13-gamora-cell-key-dedup-v1-BLOCKED.md`) is now UNBLOCKED — `cell_key` is a stable `GROUP BY` target on the 470 combat-kit rows. Stage-2 coarsening (gandalf + gamora + Matt) rides on top of the Stage-1 output; NOT this dispatch's scope.

---

## v2.2 — corpus.db MINT-DOSSIER FOLD 1+2 (corrections + plane-keying) — 2026-07-13 — **LANDED**

### What changed (one line)
Two folds from gandalf's returns-adjudication of the S1 pass: **FOLD 1** data corrections (ring-of-shields game-attribution fix, d2-sacrifice negative-canon, 9-dossier era/patch/URL ingest) + **FOLD 2** keys the 9 mint kits into `canon_engine_key` so they PLOT on the atlas plane. Added 2 nullable columns to `canon_corpus`; inserted 9 `canon_engine_key` rows (7 combat-kit + 2 system-record). Corpus row-count UNCHANGED (524); `corpus_schema_meta` bumped `2.1 → 2.2`.

### D6 rebuild sequence (now THREE committed scripts)
```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py        # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py  # S1 completion (idempotent)
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py         # this fold (idempotent)
```
All deterministic. Clean rebuild from scratch verified byte-reproducible (all 12 gates pass). corpus.db stays gitignored; scripts + this entry are the committed truth.

### FOLD 1 — data corrections
- **1a — `poe1-ring-of-shields` → `le-ring-of-shields`** (kit_id + `game` poe1→le). 2-source-confirmed game-attribution error (Last Epoch Forge Guard summon skill, NOT poe1). Cascaded across canon_corpus / canon_probe_facts / canon_engine_key. **era_year corrected 2013 (stale poe1 game-level) → 2024 (le game-level; also matches dossier).**
- **1b — `d3-call-of-the-ancients` vs `d3-ik-hota`: RULED DISTINCT — NO dedup.** Both stand (verified present). CotA = summon-3-ancients (proxy economy); IK-HotA = melee slam. Shared Immortal King set is not a dedup trigger.
- **1c — `d2-sacrifice` `negative=1`** (KEEP). Joins the negative-canon family (now 38); excluded from S6 certification population, NOT deleted. Founding self-cost melee archetype; GX-06 evidential value.
- **1d — 9-dossier ingest.** Added `canon_corpus.skill_debut_year` + `source_urls` (JSON array). Backfilled: `stabilization_patch` **7/9** (2 honest-NULL: VBV + Sacrifice — patch unconfirmed at source); `skill_debut_year` 9/9; `source_urls` 9/9 (URL-backfill manifest); `dossier_owed` cleared 9/9.

### FOLD 2 — plane-keying (9 canon_engine_key rows; geometry traced to dossier text)
| kit_id | row_class | geometry_value | mob_policy | plane cell |
|---|---|---|---|---|
| poe1-totem-hierophant | combat-kit | `totem` | full-move | FREE-MOVE×SUMMON |
| d3-call-of-the-ancients | combat-kit | `totem` | full-move | FREE-MOVE×SUMMON |
| le-ring-of-shields | combat-kit | NULL + `gx-candidate:orbit` | full-move | ORBITAL\* |
| d3-dashing-strike-monk | combat-kit | `dash_attack` | full-move | FREE-MOVE×MELEE |
| le-shift-bladedancer | combat-kit | `dash_attack` | full-move | FREE-MOVE×MELEE |
| poe1-vaal-blade-vortex | combat-kit | NULL + `gx-candidate:orbit` | full-move | ORBITAL\* |
| d2-sacrifice | combat-kit | `melee_strike` | walk | WALK×MELEE (neg=1) |
| poe1-blood-magic-kit | system-record | NULL (route=`resource-economy`) | full-move | off-plane (not a delivery skill) |
| d2-teleport-sorc | system-record | NULL (route=`mobility-grammar`) | full-move | off-plane (movement identity) |

**7 keyed cleanly; 2 off-plane by design.** The 2 system-records are NOT delivery skills (keystone economy / pure-mobility identity) — honest non-combat classification, not a hole. \* The 2 orbit kits key legally (DDL: geometry-NULL legal with `gx-candidate:orbit`) but render **UNMAPPED** until gandalf adds them to the renderer's `UNMAPPED_COL` hardcode (render-spec FLAG below).

### Verification (all 12 gates passed; clean-rebuild-from-scratch confirmed)
- corpus 524 (unchanged) · engine_key 478→**487** · combat-kit 463→**470** · system-record 15→**17** · negative 37→**38**.
- **CANON combat denominator preserved: `combat-kit AND mint=0` still = 463.** The 7 new combat rows are `mint=1`/`source='mint'` → board consumers filtering canon get the untouched 463; the renderer plots them as ★ mint dots.
- **cone Path-2 split UNTOUCHED (5 BEAM / 6 PROJECTILE)** — no new row is a cone.
- **V1.2 render reproduces from rebuilt DB** (470 combat / 38 negative / 45 roster; 515 dots). The 5 non-orbit combat mint kits place on-plane; 2 orbit UNMAPPED (expected); 2 system-records correctly absent (renderer filters `row_class='combat-kit'`).

### Steward decisions surfaced (flagged to gandalf for ratification)
1. **era_year semantics — NOT overridden with dossier skill-debut years.** FOLD 1d names "era_year", but P5 already filled it corpus-wide as per-GAME release year. Dossiers carry a per-SKILL debut year (e.g. CotA 2017 vs d3-2012; Sacrifice 2001 vs d2-2000). Mixing both semantics in one column would corrupt it, so the dossier signal is captured in the NEW `skill_debut_year` column and `era_year` stays game-level (consistent). The one exception is a correction, not a semantic shift: le-ring-of-shields era_year moved 2013→2024 to track its post-rename `game=le` level. **Steward call; reversible; flagged.**
2. **patch tokens stored BARE** (`2.6.1`, not `v2.6.1`) — the renderer's `build_public_label()` prepends `v`; a stored `v` double-renders (`vv2.6.1`). Bare storage matches the render convention.

### Render-spec FLAGS to gandalf (follow-ups; NOT elrond's to change)
- **Orbital mint kits need `UNMAPPED_COL` entries.** `le-ring-of-shields` + `poe1-vaal-blade-vortex` key legally as `gx-candidate:orbit` but render UNMAPPED until added to the renderer's `UNMAPPED_COL` hardcode (→ `"ORBITAL"`), mirroring `poe1-poison-bv`. Data is correct; the render override is gandalf's.
- **d2-sacrifice is the first kit that is BOTH `negative=1` AND combat-keyed.** It plots as an on-plane mint ★ dot (WALK×MELEE) AND appears in the negative-overlay annotation. The data is correct (its melee delivery IS determinable AND it is negative-canon); **render precedence** (exclude negatives from the combat JOIN, or accept dual representation) is gandalf's call.

### ADR compliance
- **ADR-004:** this entry. Additive columns + rows on elrond-owned corpus.db; **no engine-telemetry change** → star-lord-side MIGRATION.md unaffected.
- **Reversibility:** all changes re-derived from committed inputs (v3 CSV + engine-key/probe/roster/lineage JSONL + per-game-meta + the 9 dossiers + URL manifest, all committed) at fold time; raw columns untouched; re-runnable to byte-identical state.
- **ADR-006:** auto-commit (in-scope cycle work-product); push deferred to Matt/KR authorization.

### Artifacts
- `scripts/corpus_fold12_2026_07_13.py` — idempotent FOLD 1+2 pass (the new committed source).
- `curated/corpus-fold12-log-2026-07-13.md` — full fold log (per-kit trace + render verification + flags).
- `curated/corpus.db` — rebuilt (gitignored; schema_meta 2.2).

---

## v2.1 — corpus.db S1 DATA-COMPLETION (five payloads) — 2026-07-13 — **LANDED**

### What changed (one line)
Additive S1 data-completion pass per gandalf wind-down §3: added 6 nullable columns across three tables and backfilled from ENGINE + probe sources of record, with strict honest-NULL where source genuinely absent. **Zero row-count change** (524 / 4,780 / 478 / 45 all hold); `corpus_schema_meta` bumped `2.0 → 2.1`.

### D6 rebuild sequence (now TWO committed scripts)
```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py       # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py # this S1 completion pass (idempotent)
```
Both deterministic from committed inputs. The completion script is **idempotent** (`ADD COLUMN` guarded by pragma check; all backfills are pure UPDATEs from source) — safe to re-run. corpus.db stays gitignored; scripts + this entry are the committed truth.

### The five payloads + fill census (honest-NULL discipline)

| # | Table.column(s) added | Source of record | Fill rate | Honest-NULL |
|---|---|---|---|---|
| **P1** | `roster_atlas.amp_val` | expand engine-sourced atlas amp code (S/F/V → spiky/flat/var) | **26/45** | 19 (undeclared `_`) |
| P1 | `roster_atlas.commit_val` + `commit_provenance` | expand atlas commit code (W/I/C → wind-up/instant/channel) | **5/45** | 40 (rolled at S7, not fixed at S1) |
| P1 | `roster_atlas.mob_policy_while_casting` | — (no S1 source) | **0/45** | 45 (emitted per-skill at S7) |
| **P2** | `canon_engine_key.delivery_value` | promote probe `delivery.value` → keyed column | **478/478** | 0 |
| **P5** | `canon_corpus.era_year` | per-game canonical release year (per-game-meta.jsonl `release_era`) | **524/524** | 0 |
| P5 | `canon_corpus.stabilization_patch` | `current-X.Y` token, eras ∪ sources_used | **10/524** | 514 (naming law omits segment where absent, §7.1) |

**P3** (6 poe2 movement-unknowns) and **P4** (d2-wl-void-rift amp) are **census-only** — no schema change. All 6 poe2 remain `mob_policy_while_casting='unknown'` (unresolved in engine-key + probe + megaprobe re-probe → honest-NULL). d2-wl-void-rift `amp_val` remains NULL (no amp code in atlas_key; probe/megaprobe supply none).

### Verification (all gates passed)
- **Row counts hold:** canon_corpus 524 · canon_probe_facts 4,780 · canon_engine_key 478 · roster_atlas 45.
- **P2 cone Path-2 split reproduces exactly** — 5 BEAM {gd-flames-of-ignaffar-purifier, hot-dragons-breath, hot-exterminator-burn, poe1-incinerate, ud-flamethrower-channel} / 6 PROJECTILE {di-multishot-dh, di-vengeance-strafe-dh, le-frost-claw, poe2-galvanic-shards, tl2-shotgonne-outlander, tq-ternion-bone-charmer}.
- **P1 amp validated 25/26 exact vs CellDef amplitude** (`bc_target_cell_sampler.py` CELL_DEFINITIONS). Sole divergence K9f (flat vs cell9 target var) is the legitimate "fired-leg" engine emission — kept as-emitted, NOT overridden.
- **V1.2 plane render reproduces from rebuilt DB** (`gandalf/views/v1-plane/render_v1_2_stratified.py`, exit 0; 463 combat / 37 negative / 45 roster; cone Path-2 verified). The additive `delivery_value` column does NOT change render output (render still parses delivery via JSON subquery — see render-spec FLAG below).

### Discipline #11 findings surfaced (empirical inspection contradicts commission assumptions)
1. **Roster movement is genuinely absent at S1.** The commission assumed engine sources (CellDefs/battle-sim) carry roster movement; empirically move_policy is emitted **per-skill at generation (S7)** via `per_skill_emitter.py` `_MOVE_ROOTED/_MOVE_WALK/_MOVE_FULL` — there is no static per-roster-kit movement source of record. All 45 → honest-NULL.
2. **Roster commit is mostly rolled, not fixed.** Only CellDef-PINNED cells carry a fixed commitment (K1=wind-up, K7=snap/instant, K19=channel) + 2 roster-explicit (B12=channel, H6=wind-up). Unpinned cells are "rolled" at S7 → NULL, never snap-invented.
3. **stabilization_patch signal lives in `eras`, not `sources_used`.** Commission scoped P5 patch to sources_used (1 clean `current-` token); the richer signal is the eras field (10 tokens). Extractor unions both with provenance. **STEWARD SCOPE NOTE — flagged to gandalf for ratification** (data-domain steward call; reversible; non-inventing).
4. **chronicon era-year source discrepancy.** `era_range` token says `1.0-2020`; `release_era` field says `1.0 2021`. era_year=2020 chosen (matches era_range + real release); flagged for Matt/gandalf.

### Render-spec FLAGS to gandalf (follow-ups; NOT elrond's to change)
- **delivery_value column now exists** — `render_v1_2_stratified.py` line ~116-119 still parses `json_extract(pf.facts_json,'$.value')` for delivery. It MAY now read `canon_engine_key.delivery_value` directly (simpler, schema-derivable). Render-spec change is gandalf's call, not elrond's.
- Roster placement in the render is hardcoded UNMAPPED (movement-derived rows use engine-key movement, not roster columns), so the P1 roster backfill does not alter render output — as expected.

### ADR compliance
- **ADR-004:** this entry. Additive columns on elrond-owned corpus.db; **no engine-telemetry change** → star-lord-side MIGRATION.md unaffected. Cross-repo reads of `bc_target_cell_sampler.py` were READ-ONLY (values embedded as documented literals for a self-contained collab-repo rebuild).
- **Reversibility:** raw columns preserved (roster `amp`/`commit_slot` codes, `eras` untouched); all new columns derived at completion time from committed source; re-runnable to byte-identical state.
- **ADR-006:** auto-commit (in-scope cycle work-product); push deferred to Matt/KR authorization.

### Artifacts
- `scripts/corpus_completion_s1_2026_07_13.py` — idempotent S1 completion pass (the new committed source).
- `curated/corpus-completion-s1-log-2026-07-13.md` — full per-payload log + honest-NULL census + findings.
- `curated/corpus.db` — rebuilt (gitignored; schema_meta 2.1).

---

## v1.14 — corpus.db THREE-LAYER INGEST (DELTA v2 + Q24 rulings) — 2026-07-12 — **LANDED**

### What changed (one line)

Executed the full three-layer corpus ingest per gandalf DELTA v2 brief (2026-07-12) and Matt Q24(a)/(b)/(c) rulings: created `agentic_orchestration/research/curated/corpus.db` (gitignored; DDL+scripts = committed truth) with 524 rows in `canon_corpus`, 4780 rows in `canon_probe_facts`, 478 in `canon_engine_key`, 45 each in `roster_atlas` and `roster_lineage_enrichment`. v1.13 entry (PROPOSED schema) superseded; all schema amendments per DELTA v2 applied in DDL v2.0.

### Why (one line)

Q24 rulings lifted the ingest gate: housing=new DB, roster/bench 48 rows SKIPPED and replaced with rebuilt roster (Q24(b)), HoT tier confirmed T3 (Q24(c)). Three-layer architecture reflects that the re-key is per-kit (probe+judgment), not per-raw-value — the six `rekey_<slot>` tables from v1.0 are retired permanently.

### Schema v2.0 shape (DDL: `scripts/catalogue_migrations/corpus_v2_0_three_layer.sql`)

- **Layer 1 — `canon_corpus`** (524 rows): 515 from CSV (canon source) + 9 mint kits from mint-dossiers (source='mint', mint=1, dossier_owed=1). Q24(c): HoT 19 rows, tier='T3', tier_confirm_pending=0. is_system=18 (SYS key_group). negative=37. suffix_rekey_status: 'keyed-v1' for kits in engine-key (geo/ctrl/def/econ); mob/elem permanently 'descriptor-final' (schema-by-omission, no rekey_mob/elem tables ever).
- **Layer 2 — `canon_probe_facts`** (4780 rows): 478 positive kits × 10 families each. Negatives ingest Layer-1 only. post_cutoff_cap + dossier_owed per kit.
- **Layer 3 — `canon_engine_key`** (478 rows): mapping-pass output verbatim (JSONL ingested as-is; zero re-derivation). row_class: combat-kit=463, system-record=15. ctrl.treatment CHECK: 'support' never legal (Q22). def_bin: NULL for 14 FLAGGED rows (engine-key stores None, not literal 'FLAGGED').
- **Roster — `roster_atlas`** (45 rows) + **`roster_lineage_enrichment`** (45 rows): Q24(b) replacement for 48 retired mobile CSV rows. FK: all 45 lineage enrichment rows resolved against roster_atlas; all lineage target corpus_kit_ids resolved against canon_corpus.

### Laws permanently hardened (schema-by-omission)

- No `rekey_mob` or `rekey_elem` table may EVER exist. element=free axis; mobility=emergent.
- No measured column on `canon_corpus`. Measured = gauntlet fingerprints (engine-side store only).
- ctrl.treatment CHECK: damage / control / hybrid. 'support' never legal per Q22 ruling.

### Post-ingest asserts (all passed)

canon_corpus=524 (515+9 mint); source=canon 515; is_system=18; negative=37; HoT=19 (T3,pending=0); mint=9; probe_facts=4780/478 kits; engine_key=478 (combat=463, system=15); roster_atlas=45; roster_lineage_enrichment=45.

### Acceptance harness result (D6)

All Board 2 geometry counts: MATCH. SU demand 48: MATCH. damage-amp 97: MATCH. stun 36: MATCH. poison-dot 36: MATCH. orbit 4: MATCH. def-bin tank 215/mitigate 84/glass 67/evade 66/absorb 28/FLAGGED(NULL) 14/post-cutoff-deferred 4: all MATCH.

**Two harness mismatches (source-data findings, not DB errors):**

1. **Board2 walls = 2 (not 3):** `le-frost-wall-rm` appears in boards-v1.md wall list but has `flags=[]` and `geometry=totem` in the engine-key (no J-GEO:placed-lane flag). DB stores what the engine-key provides. The wall kit classification in the board may have used a different signal than the flags column. Curation finding: le-frost-wall-rm flag gap in engine-key — forward work for gandalf/star-lord.
2. **Board3 freeze = 42 (not 43):** The engine-key has exactly 42 distinct combat kits with `GAP-AILMENT:freeze`. boards-v1.md says 43. The 1-kit discrepancy is between the board generator's output and the delivered engine-key JSONL. DB ingests faithfully; data was not adjusted to match the board. Curation finding: one freeze-gap kit appears in the board count but is absent from the engine-key — forward work for gandalf.

### D4 Reconciliation (CSV is_system=18 vs EK system-record=15)

Overlap: 12 kits (both CSV-SYS and EK-system-record).
CSV-sys-only (mapped as combat-kit in EK): chr-crown-proc-engine, d3-lod-archetype, le-low-life-ward, poe2-grim-feast, poe2-temporalis-blink, vs-golden-egg-scaling (6 kits).
EK-sys-only (system-record in EK, not SYS-flagged in CSV): tli-sage-elixir, ud-multishot-link, vs-big-trouser (3 kits).
Note: vs-golden-egg-scaling is CSV-SYS but absent from engine-key entirely (not in the 478-row JSONL).
Layer-3 row_class governs all combat denominators.

### Deliverables (this entry)

- `scripts/catalogue_migrations/corpus_v2_0_three_layer.sql` — DDL v2.0 (three layers + roster tables + views; rekey_* tables retired)
- `scripts/corpus_ingest_2026_07_12.py` — deterministic ingest script (clean rebuild = identical state)
- `curated/corpus.db` — the DB (gitignored; rebuilt from DDL + script)
- `curated/corpus-ingest-log-2026-07-12.md` — full ingest log with findings

### Cross-seam ADR compliance

ADR-004: elrond-seam data layer only. ADR-006: no remote push; DB gitignored. No engine-telemetry touch; no measured columns. Boundary with star-lord respected.

### Status

**LANDED — 2026-07-12.** v1.13 PROPOSED entry is superseded.

---

## v1.13 — canon-corpus.db INITIAL SCHEMA (engine-frame schema of record) — 2026-07-12 — **SUPERSEDED by v1.14**

### What changed (one line)

Proposed the v1.0 schema + staged-ingest plan for a **NEW data store** representing the 563-row mobile ARPG canon corpus **under the engine coordinate frame as schema of record** (Matt inversion ruling 2026-07-12; authority `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` §2 fate table). **This entry is PROPOSED paper-work: schema + MIGRATION doc are ungated, but no DB is created and no rows are ingested until Matt's corpus-housing D-ruling + ADR-006 authorization land.**

### Why (one line)

The mobile atlas key is a hybrid: its 6-slot prefix (attr/range/tempo/amp/proxy/commit) is the engine lattice **1:1**; its suffix (mob/geo/ctrl/def/econ/elem) is mobile-invented vocabulary that never passed a design gate. The harvest authorizes the DATA, not the key — so we KEEP the prefix as typed lattice coordinates and RETIRE the suffix to raw descriptors *awaiting-rekey*, ready for six design sessions to map in later.

### Schema shape (per the §2 fate table)

- **PREFIX KEPT** — `attr/range/tempo/amp/proxy/commit` as `<slot>_val` enum + `<slot>_conf` real, `{value, confidence}` per slot; `lattice_coord` = 6-char prefix code (engine coord 1:1). Commit enum **of record `instant`/`wind-up`/`channel`**.
- **SUFFIX RETIRED→RAW** — `mob_raw/geo_raw/ctrl_raw/def_raw/econ_raw/elem_raw`, `suffix_rekey_status='awaiting-rekey'`. **No mappings invented.** Six empty `rekey_*` mapping tables + `v_canon_corpus_rekeyed` LEFT-JOIN view let sessions join engine values **without rewriting rows**.
- **MEASURED-VS-PROJECTED LAW hardened by omission** — `canon_corpus` has **no** measured column. Measured axes = gauntlet fingerprints only (separate engine-side store). Corpus rows can never carry measured values.
- **ADD engine-native** — `motion_frame/t4_doors/option_c_substrate_flags/commit_provenance`, NULL at ingest, authored at re-key time.
- **Identity/provenance** — `atlas_key_orig` preserved verbatim; `provenance_tag='mobile-harvest-v3'`; `source_date`; `game` = game-of-record (NOT harvest `corpus_bucket`); HoT is its own game (`game='hot'`, tier lean T3, `tier_confirm_pending=1`).

### Curation findings surfaced (read-only dry-run)

1. **Lossy projection.** v3 CSV drops raw attr/range/tempo/amp + raw ctrl/def; the prefix is decoded from `atlas_key` positional codes. `ctrl_raw`/`def_raw` recoverable only as coarse code-tokens → `ctrl_def_from_code=1` honesty flag.
2. **Confidence collapse.** Only `avg_conf` (mean of proxy/geo/commit) survives for canon rows; true per-slot `{v,c}` lives only in `rdr-roster-kits.jsonl` (48 roster/bench). Canon ingests `prefix_conf_provenance='avg-collapsed'` unless the `canon-corpus-*.jsonl` sources are recovered (Open Q1).
3. **`game` ≠ `corpus`.** Harvest bucket `hades`→games `hades1/hades2`; `tl`→`tl1/tl2/tli`. 13 rows would corrupt if `corpus` were used as game. Schema stores `game` as identity, `corpus_bucket` as provenance.

### Dry-run counts (READ-ONLY validator — 0 ERROR, 0 WARN)

`563 rows · 563/563 unique kit_id` → 496 canon substrate · 48 roster/bench (provenance-only) · 18 SYS-annex · 1 UNRESOLVED. 20 games-of-record. HoT = 19.

### Deliverables (this entry)

- `scripts/catalogue_migrations/corpus_v1_0_canon_corpus.sql` — DDL (canon_corpus + corpus_schema_meta + 6 rekey_* + 2 views). NOT executed.
- `scripts/corpus_ingest_dryrun_2026_07_12.py` — READ-ONLY dry-run + row-level validator (writes nothing).
- `curated/corpus-db-schema-proposal-2026-07-12.md` — full proposal, staged plan, §4 open questions (Q1 confidence provenance · Q2 housing · Q3 roster in/out · Q4 HoT tier confirm · Q5 SYS/UNRESOLVED handling).

### Cross-seam ADR compliance

ADR-004: this is elrond-seam data-layer schema (external research), no engine-telemetry touch — measured law hardened by *omission*, boundary with star-lord respected (read-only on telemetry, no measured columns here). ADR-006: read-only-by-default honored — no DB writes, no remote push; ingest deferred to explicit Matt authorization. Housing (Q2) is a Matt D-ruling per spec §5.

### Status

**PROPOSED — ingest-gated.** On Matt housing D-ruling + authorization: execute §3c staged order, then this entry flips to LANDED with post-ingest assert results appended.

---

## v1.12 — synty_catalogue.db schema 1.1→1.2: gandalf axis-3/4 rep-audit curation (Option A consumption rule + frontier-western value-split) — 2026-06-17

### What changed (one line)

gandalf curated elrond's axis-3/4 PROPOSALS at the semantic-layer rep-audit (ruling `agentic_orchestration/gandalf/notes/2026-06-17-synty-gear-spec-upstream-wiring-ruling.md` §1.3/§1.4/§1.6, closing Q2 gate 1 of the Synty gear-spec upstream-wiring call). Axis 3 (`time_period`): **ACCEPTED as-proposed — no change.** Axis 4 (`cultural_identity`): **TWO additive corrections** materialized here — (1) the **Option A consumption rule** (read-time binding gate, NOT a data migration) and (2) the **`modern-western` → `frontier-western` value-split** (touches data, additively). synty_catalogue internal schema_meta `1.1 → 1.2`. **No schema-column churn, no destructive change.**

### Correction 1 — Option A consumption rule (READ-TIME gate; ruling §1.3 / §1.6) — NOT a data migration

gandalf ruled **Option A** over Option B (physical column split): the `cultural_mode_flag` column (written at 1.1) **already partitions** the rows, so the fix is a consumption rule, not a migration. **Nothing in the data changes.** The durable rule:

> `cultural_identity_proposed` is binding as a **cultural-tradition substrate ONLY for rows where `cultural_mode_flag ∈ {A, B}`.**
> - **Mode A/B** → the value IS a cultural-tradition read (egyptian, east-asian, norse, greco-roman, w-euro-medieval, **frontier-western**). Bind it.
> - **Mode C** → the value is a `register_default_skin` (genre-default: generic-fantasy / sci-fi / modern-western-urban — **NOT a culture**).
> - **Mode D** → null cultural read (nature biomes).
> - **unresolved** (`?`) → no cultural home; do NOT force one.

Downstream cultural-rotation / faction surfaces (the `canonical/48` seasonal-rotation operator; any Fate-genre faction-architecture surface) read cultural-tradition **ONLY from Mode-A/B rows**, and never inherit `generic-fantasy` / `sci-fi` / `modern-western` as a culture. This is the exact **Mode-C artifact** the §4.4 rep-audit discipline exists to catch — a label that passes the name-token vote but fails semantic cultural-coherence (the S.-American-Indigenous-Shotgun-Cluster failure mode).

**Recorded durably in three places** (the .db is gitignored — script + this entry are the committed source-of-truth): (a) the `CULTURE_BINDING_MODES` constant + `is_cultural_tradition_binding()` helper + `CONSUMPTION RULE` docblock in `scripts/tag_synty_multiaxis_2026_06_17.py`; (b) a quoted CONSUMPTION-RULE block atop the **Axis 4** section of the regenerated `multiaxis-tags-2026-06-17.md`, which now renders Mode-A/B (binding) strata separately from Mode-C/D (non-binding); (c) this MIGRATION entry. **No column added, no row re-typed for this rule** — it is read-time semantics over existing data.

### Correction 2 — `modern-western` homonym split → `frontier-western` (ruling §1.4) — additive, touches data

`modern-western` was a homonym doing double duty: **Mode-B** (Western Frontier / Western Pack = the American-frontier cultural tradition, cowboys — a REAL cultural read) vs **Mode-C** (Apocalypse / City / Battle Royale = modern-western-urban register-default). The Mode-B rows are split to the new value **`frontier-western`** (cultural-tradition); the Mode-C rows retain **`modern-western`** in the register-default sense (already de-fanged by Option A's mode gate).

**Verified row count (ruling estimated ~2): exactly 2 Mode-B rows split** —

| collection_id | pack | 1.1 value | 1.2 value | mode |
|---|---|---|---|---|
| 154809 | `POLYGON - Western Frontier Pack` | `modern-western` | **`frontier-western`** | B |
| 154810 | `POLYGON - Western Pack` | `modern-western` | **`frontier-western`** | B |

The 30 Mode-C `modern-western` rows (Apocalypse / City / Battle Royale / Apocalypse-HUD / Military-Combat-HUD …) are **unchanged**. Post-split authoritative field-value counts (verified against the regenerated JSONL, by field value not substring): `frontier-western` = **2** (both mode B); `modern-western` = **30** (all mode C); 157 total rows preserved. `cultural_basis` on the 2 split rows updated to name the new value + cite the ruling (descriptive text, not identity).

### Reversibility / regeneration (source-anchored discipline)

`synty_catalogue.db` stays **gitignored** (`curated/.gitignore` ignores `*.db`). The value-split is encoded in the `western` entry of `CULTURE_RULES` in `scripts/tag_synty_multiaxis_2026_06_17.py` (`("western", "frontier-western", "B", …)`), so a **from-scratch deterministic rebuild lands directly at the curated 1.2 state** — the curation is reproducible from committed source, not a one-off DB mutation:
```
python3 build_synty_catalogue_2026_06_17.py full      # WAVE 1 (136 zip packs)
python3 build_synty_catalogue_2026_06_17.py nonfbx    # WAVE 2 (21 extracted packs)
python3 tag_synty_multiaxis_2026_06_17.py all          # 5-axis tag + gandalf-curated axis-4 (1.2) + regen JSONL/MD
```
The live DB for this entry was updated surgically (a 2-row additive `UPDATE` + schema_meta 1.2 row) rather than a full re-tag, to keep the touch minimal; the script reproduces the identical curated state on any clean rebuild. The `tag … all` schema_meta insert records BOTH the 1.1 (multi-axis) and 1.2 (curation) version rows for lineage.

### Deliverables touched

- `agentic_orchestration/research/scripts/tag_synty_multiaxis_2026_06_17.py` — `CULTURE_RULES` western entry → `frontier-western`; `CULTURE_BINDING_MODES` + `is_cultural_tradition_binding()` + CONSUMPTION-RULE docblock added; `NEW_SCHEMA_VERSION` 1.1→1.2; schema_meta now records both version rows; report renders Mode-A/B binding vs Mode-C/D non-binding strata + the Option A block.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.jsonl` — regenerated; the 2 Mode-B rows carry `axis4_cultural_identity_proposed='frontier-western'`.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.md` — regenerated; Axis 4 section carries the Option A consumption rule + value-split notes + binding/non-binding stratum split.
- `synty_catalogue.db` (gitignored) — 2-row value-split applied; schema_meta `1.2` row inserted.

### Downstream hooks

- **gandalf** — axis-3/4 curation now materialized; this closes the consumption-rule handoff from ruling §1.4/§5. The wiring-call half (fantasy-first + silhouette degrade) is gandalf/rocket-side, not in this data-layer entry. **gandalf holds the push** (ADR-006) — this entry is committed but NOT pushed by elrond.
- **Any cultural-rotation / faction-architecture consumer** — read cultural-tradition via `is_cultural_tradition_binding(cultural_mode_flag)` (i.e. `cultural_mode_flag IN ('A','B')`) before inheriting `cultural_identity_proposed`. Mode-C is `register_default_skin`, not a culture.
- **Incorporation ledger** — unchanged; no incorporation event in this entry.

---

## v1.11.1 — synty_catalogue.db WAVE 2: 21 extracted-unitypackage packs indexed (no schema change) — 2026-06-17

### What changed (one line)

The 21 no-FBX Synty packs (variant=Unity, native `has_fbx=0`) were downloaded as `.unitypackage` files and **knight-rider extracted their meshes into a LOOSE FBX TREE** (not zips) at `~/Games/synty-corpus/nonfbx_extracted/<PACK_FOLDER>/Assets/Synty/.../Models/*.fbx` (8,655 FBX + 11,930 textures, 2.8 GB). The populate script gained a **second scan path** (`nonfbx` mode — walks the directory tree instead of `unzip -l`-ing zips) and a WAVE-2 classifier (`classify_asset_loose`). All 21 packs + 8,655 mesh assets are now indexed. **No schema change** — `packs`/`assets`/`textures`/`schema_meta` are unchanged at v1.0; this is a pure data-population pass keyed on the existing `(collection_id, download_id)` identity, so it is idempotent and additive to the WAVE-1 136 packs (which stay untouched).

### Catalogue totals after WAVE 2

- **Packs: 157** (136 WAVE-1 zip-backed `source='synty-store'` + 21 WAVE-2 loose-tree `source='synty-store-unitypackage'`).
- **Assets: 62,281** (53,626 WAVE-1 + 8,655 WAVE-2).
- **structural_class: 156 monolithic / 1 modular** (the lone modular pack remains the WAVE-1 Modular Fantasy Hero pack; all 21 WAVE-2 packs are monolithic — none ship per-slot body parts or `_Texture_Mask`).

### Integrity (path-index + count check) — PASS

Every WAVE-2 `assets` row resolves to a real file under `nonfbx_extracted/`: **8,655 paths checked, 0 misses.** Per-pack FBX counts **match `~/Games/synty-corpus/extract.log` exactly for all 21 packs** (the integrity target). `verify` mode now runs both waves: WAVE-1 zip-backed (157→packs reported as 157 incl. WAVE-2 by the zip-existence pass, 0 zip-misses for WAVE-1 source) + WAVE-2 loose-tree (21 packs / 8,655 assets / 0 path-misses).

### WAVE-2 naming convention differs from WAVE-1 SourceFiles (why a second classifier)

Unity-export FBX lack the `SK_` skeletal prefix that the WAVE-1 SourceFiles packs use. The WAVE-2 conventions, all handled by `classify_asset_loose` (the WAVE-1 `classify_asset` is left untouched):

| WAVE-2 pattern | asset_type | note |
|---|---|---|
| `Characters.fbx` / `Generic_Characters.fbx` / `Characters_<Variant>.fbx` | character (slot=whole_character) | baked monolithic appearance-unit (Unity export bakes the whole char into one FBX) |
| `SM_(Gen_)Chr_Attach_*` | armor_part + **is_accent=1** | the silhouette-breaker accent layer — hats / hair / beards / masks / glasses |
| `SM_(Gen_)Wep_*` | weapon | |
| `SM_(Gen_)<Bld\|Env\|Veh\|Fol\|Tree\|Tile>_*` | environment | |
| `SM_(Gen_)<Prop\|Item>_*` | prop | |
| `SM_(Gen_)<UI\|FX\|...>_*`, `FX_*`, `Sphere*`, `Animations*` | other | |
| OLDER SIMPLE-line bare prefixes (`Building_`/`Vehicle_`/`Env_`/`road`/`Prop_`/`Item_`/`Sign*`…) | environment / prop | the SIMPLE packs predate the `SM_` prefix |
| `SI_Letter`/`SI_Symbol`/`SI_Number`/`*Icon` | other | Props-pack 2D-icon-as-mesh family |
| Shop-Interiors `SI_*` / Simple-Temples `ST_*` | prop | product-line prefixes (icon check fires first to resolve the `SI_` collision) |

### Provenance (source-anchored discipline)

Every WAVE-2 pack is stamped `source='synty-store-unitypackage'` (distinct from WAVE-1 `'synty-store'`) and `corpus_rel_path='nonfbx_extracted/<folder>'`; each pack `notes` records `extracted-from-unitypackage (variant=Unity, native has_fbx=0); meshes extracted by knight-rider 2026-06-17`. Each WAVE-2 asset `notes='extracted-from-unitypackage'`. The `has_fbx` flag stays **0** on these packs (it reflects NATIVE Synty variant availability per the manifest — these never shipped a native FBX SourceFiles download; the indexed meshes are extracted, not native). `has_unity=1`. This keeps the variant-availability columns truthful while the path index points at the extracted tree.

### Survey-accurate findings (reporting what EXISTS, not what "should" be there)

- **POLYGON MINI - Fantasy Pack ships ZERO character meshes** in this extraction. The dispatch hint listed it character-relevant (`Generic_Characters.fbx` expected), but the extracted tree is entirely `SM_Bld_*` / `SM_Tile_*` / `SM_Env_*` / `SM_Prop_*` + FX (892 FBX, 0 character, 0 accent). It populates as an environment/prop pack — which is what is actually on disk. (The MINI product-line character minis were evidently not in this no-FBX Unity download.)
- **The shared `PolygonGeneric` module rides along in nearly every POLYGON pack.** Even environment-leaning packs (Nature Pack) carry `Generic_Characters.fbx` (1 character mesh) + ~22 `SM_Gen_Chr_Attach_*` generic accents because the Generic module is bundled. This produces a baseline of ~1 generic character + ~22 generic accents per POLYGON pack on top of each pack's themed content. Kids Pack (184 accents) and Battle Royale (89) carry large pack-specific accent sets on top of the generic baseline.
- **No `_Texture_Mask` in any WAVE-2 pack** (verified) → all `recolor_scheme='whole_atlas_swap'`, consistent with the page-1 named monolithic packs. The per-region 5-zone mask lever stays unique to the WAVE-1 Modular Fantasy Hero pack.

### Regeneration

`synty_catalogue.db` stays **gitignored** (`curated/.gitignore` ignores `*.db`). Committed source-of-truth is the populate script + this MIGRATION entry. Full deterministic rebuild from on-disk corpus + committed manifest:
```
python3 build_synty_catalogue_2026_06_17.py full     # WAVE 1 (136 zip packs)
python3 build_synty_catalogue_2026_06_17.py nonfbx   # WAVE 2 (21 extracted packs)
```
Both modes are idempotent (upsert-keyed on `(collection_id, download_id)`); order-independent.

### Downstream hooks (unchanged from v1.11)

All WAVE-2 packs default `incorporation_status='NOT_INCORPORATED'`; `distinctiveness_score` NULL (galadriel's seam — hook only). No incorporation event has occurred.

---

## v1.11 — synty_catalogue.db landed (Synty 3D gear-substrate catalogue; NEW standalone DB) — 2026-06-17

### What changed (one line)

Created a **new standalone SQLite DB** `agentic_orchestration/research/curated/synty_catalogue.db` (schema v1.0) indexing the downloaded Synty FBX corpus — **136 FBX packs, 53,626 mesh assets** — as metadata + filesystem path index ONLY (bytes stay on disk in the corpus zips at `~/Games/synty-corpus/fbx/`; the DB never holds mesh bytes). Tables: `packs` (collection/variant/structural_class/recolor_scheme/license-incorporation ledger), `assets` (one row per FBX mesh; slot taxonomy + asset_type + distinctiveness hook), `textures` (recolor mask + palette-atlas index), `schema_meta`. Populate script: `agentic_orchestration/research/scripts/build_synty_catalogue_2026_06_17.py` (re-runnable: `schema|slice|full|verify|queries`).

### Why (one line)

Materializes the **gandalf §7.1 elrond acceptance hook** in `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — the substrate catalogue + license ledger that resumes the deferred gear-spec generation design session. Dispatch: `agentic_orchestration/dispatches/2026-06-17-elrond-synty-catalogue.md` (Gate-1-cleared, 837dd7f).

### SEPARATE DB vs extend catalogue.db — decision + justification

**Decision: separate `synty_catalogue.db`, NOT an extension of `catalogue.db`.**

Rationale — the two catalogues have near-zero schema overlap and orthogonal shapes:
- `catalogue.db` is a **2D-sprite STYLE-RUBRIC** catalogue: six-axis pixel-art register scoring (resolution_band / palette_size / shading_technique / linework_style / animation_frame_density / derived_register), embodiment tags, abstraction groupings, multi-vendor `catalogue_sources` + `crawl_sessions` provenance. It answers *"what visual register is this 2D sprite asset?"*
- `synty_catalogue.db` is a **3D-FBX MESH** catalogue: per-mesh slot taxonomy, structural_class (monolithic vs modular), license incorporation ledger, recolor-lever class, filesystem path index into corpus zips. It answers *"which mesh fills which gear slot, and is it license-incorporated?"*

Forcing 3D-mesh fields onto the sprite-rubric tables (the six-axis CHECKs do not apply to FBX meshes; `crawl_sessions` is a Legolas-crawl construct that does not model a knight-rider corpus download) — or vice versa — would muddy both schemas and break the existing 2D consumers' assumptions. The **vendor-catalogue precedent already separates concerns by folder** (`research/catalogue/<vendor>/`); we separate by DB *file* here because the overlap is near-zero rather than partial. Cross-DB linkage, if ever needed, is by the stable string key `collection_id` (Synty's). This is the lower-coupling, lower-risk choice and preserves `catalogue.db`'s consumers untouched.

### Schema shape (v1.0)

- `packs` — `collection_id` + `download_id` (identity is the PAIR; a collection MAY ship >1 FBX download — Water Guns ships two), `collection_name`, `zip_name`, `corpus_rel_path`, `size_mb`; variant flags `has_fbx/has_unity/has_unreal/has_godot` (joined from `full-fbx-variant-manifest.jsonl`); `structural_class` ∈ {monolithic, modular}; `recolor_scheme` ∈ {per_region_mask, whole_atlas_swap, unknown}; license ledger `incorporation_status` (default `NOT_INCORPORATED`; `INCORPORATED` carries `incorporated_season` + ISO `incorporated_at`); `source`, `source_date`, `added_at`, `notes`.
- `assets` — one row per FBX mesh: `pack_id` FK, `zip_rel_path` + `member_path` + `file_name` (the path index — bytes resolve at `<corpus_root>/<zip_rel_path> :: <member_path>`, never in DB); `asset_type` ∈ {character, weapon, armor_part, prop, environment, other}; `slot` (nullable; monolithic→`whole_character`, modular→canonical slot, weapon→`weapon`, prop/env→NULL); `is_accent`, `is_modular_part`, `gender`; `distinctiveness_score` (**nullable hook — DO NOT populate; galadriel scores later per gandalf §7.4**); `added_at`, `notes`.
- `textures` — recolor mask + palette-atlas index per pack: `texture_role` ∈ {region_mask, palette_atlas, base_atlas, other}; `channel_region_map` JSON (modular pack's 5-zone RGB-corner scheme from galadriel slice-verification 2026-06-17 §3.1; semantic per-zone labels marked expected-but-unrendered per galadriel §5).

### Slot vocabulary — modular `Chr_<Slot>` → canonical slot mapping (gandalf open-question §2)

Reconciled the modular pack's raw token names to a clean canonical slot set gandalf designs against:

| Synty modular token | canonical slot | layer |
|---|---|---|
| Torso | chest | body |
| Hips | hips | body |
| LegLeft / LegRight | leg_l / leg_r | body |
| ArmUpperLeft/Right | arm_upper_l / arm_upper_r | body |
| ArmLowerLeft/Right | arm_lower_l / arm_lower_r | body |
| HandLeft / HandRight | hand_l / hand_r | body |
| Head | head | body |
| Hair / FacialHair / Eyebrow / Ear | hair / facial_hair / eyebrow / ear | cosmetic |
| HeadCoverings | head_covering | **accent** |
| HelmetAttachment | helmet_accent | **accent** |
| ShoulderAttachLeft/Right | shoulder_accent_l / shoulder_accent_r | **accent** |
| ElbowAttachLeft/Right | elbow_accent_l / elbow_accent_r | **accent** |
| KneeAttachLeft/Right | knee_accent_l / knee_accent_r | **accent** |
| HipsAttachment | hips_accent | **accent** |
| BackAttachment | back_accent | **accent** |

Accent slots are flagged `is_accent=1` — they mount to the rig's named `All_NN_` sockets (galadriel §2) and are the silhouette-breaker layer (gandalf §3.6 "accents SECOND"). Monolithic packs' named-character capes (`SK_Chr_<Name>_Cape_NN`) are also classed `back_accent` (a hint of accent-modularity even in the silhouette lane).

### Galadriel slice-verification (2026-06-17) findings folded in

- **`recolor_scheme` per-pack field** captures galadriel's load-bearing §3.3 bifurcation: the per-region `_Texture_Mask` lever is **modular-pack-specific** (Modular Fantasy Heroes = `per_region_mask`); page-1 named-character packs (Adventure, Fantasy Kingdom, Samurai) ship coarser whole-atlas palette-swaps = `whole_atlas_swap`.
- **CAVEAT for consumers:** 15 packs carry `recolor_scheme=per_region_mask` because they *ship a mask texture*, but most are **environment** packs (Dungeon, Horror Asylum, Palm City, Sci-Fi Worlds, etc.) whose masks recolor props, NOT character armor. For the **armor restyle lane** specifically, only the **Modular Fantasy Hero Characters** pack's mask is character-relevant (it is also the sole `structural_class=modular` pack). Filter on `structural_class='modular'` (not `recolor_scheme`) to isolate the per-region armor-recolor lane. This is survey-mode accurate: the field reports what EXISTS (a mask ships), not what it is FOR.
- **`textures.channel_region_map`** carries the modular pack's verified 5-zone RGB-corner scheme (WHITE/CYAN/BLUE/YELLOW/MAGENTA); per-zone semantic labels (primary/secondary/metal/leather/accent) marked expected-but-unrendered per galadriel §5 — galadriel locks them on a later render pass.
- **distinctiveness_score** left NULL across all 53,626 assets — galadriel's seam (§7.4), hook only.

### Who's affected

- **Gandalf** — design-resumption consumer. The slice checkpoint (5 packs: Adventure, Fantasy Kingdom, Samurai, Modular Fantasy Heroes, Bow and Crossbow) + galadriel's geometry verdict clear the §4 resumption gate. The full 136-pack catalogue is the substrate for the §7.6 StyleProfile output-shape ruling. Slot vocabulary + structural_class + recolor_scheme are the design-facing fields.
- **Galadriel** — distinctiveness scoring (§7.4): `assets.distinctiveness_score` is the nullable target column; runs on a working subset, not the full corpus. The per-zone semantic-label render pass (§5 follow-up) updates `textures.channel_region_map`.
- **Knight-rider** — second-wave hook: the 21 no-FBX `.unitypackage` extractions (in progress, `~/Games/synty-corpus/nonfbx/`) populate as a clean second `full` pass once extracted to FBX (the populate script is re-runnable + upsert-keyed on (collection_id, download_id), so a second pass is idempotent for existing packs + additive for new ones).
- **Rocket** — L2 restyle leaf (§7.2): the modular pack's slot set + mask scheme are the build target; reads `synty_catalogue.db`, no write dependency.
- **Star-lord** — engine telemetry NOT affected. This is a standalone research catalogue; no telemetry table / fixture / export key touched (Principle 6 round-trip: not applicable, confirmed by KR at dispatch authoring).

### License incorporation ledger semantics (Matt stipulation)

Every pack defaults `incorporation_status='NOT_INCORPORATED'`. Assets not INCORPORATED before the Synty-Pass subscription lapses cannot be used afterward. The stamp path (smoke-tested): `UPDATE packs SET incorporation_status='INCORPORATED', incorporated_season='<season/build>', incorporated_at='<ISO>' WHERE …`. All 136 packs are NOT_INCORPORATED at landing (no incorporation event has occurred).

### Path-index integrity

`verify` pass: **136 packs, 53,626 assets, 0 zip-misses** — every `packs.zip_name` resolves to a real file on disk. (Asset-level paths are zip MEMBERS verified via `unzip -l` at index time; the zip-existence check is the on-disk integrity gate since members are not extracted.)

### DB is a build artifact (gitignored; regenerable — matches catalogue.db precedent)

`synty_catalogue.db` is **gitignored** (`curated/.gitignore` ignores `*.db`), exactly as `catalogue.db` is. The committed source-of-truth is the **populate script** `agentic_orchestration/research/scripts/build_synty_catalogue_2026_06_17.py` + this MIGRATION entry. The DB regenerates deterministically from the on-disk corpus + the committed `full-fbx-variant-manifest.jsonl` via `python3 build_synty_catalogue_2026_06_17.py full`. This honors the reversibility principle (curation reproducible from raw input) and the existing vendor-catalogue precedent (schema/script committed, `.db` regenerable). A consumer that needs the DB and does not have the local corpus should request the regenerated `.db` or the corpus location from elrond.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. New standalone DB; relationship to `catalogue.db` documented above (separate, low-coupling, cross-link by `collection_id`).
- **Cross-seam contract change?** No — standalone research catalogue; no engine-telemetry / fixture / export-key change (KR-confirmed not-applicable at dispatch authoring).
- Push to remote deferred to Matt's gate (auto-commit fired per team commit discipline).

---

## v1.10 — kit_star_sign_assignments.json sidecar landed (kit-to-star-sign MVP Phase 2) — 2026-06-09

### What changed (one line)

Landed `reincarnated-loadout/public/kit-space/kit_star_sign_assignments.json` (schema v1.0; artifact_kind `kit_star_sign_assignments`) — a parallel sidecar to `faction_assignments.json` carrying per-kit `star_sign_id` + `star_sign_name` + `star_sign_tradition` + `star_sign_assignment_method` (HAND_CURATED | RANDOM) + optional `hand_curated_anchor` for the active 37-kit corpus. Source corpus: Legolas 423-entry zodiac substrate at `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml`. 3 hand-curated overrides (Duskweaver→Mula; Cannonade Cleric→Krittika; Stonefist→Hercules per gandalf Phase 1 doc) + 34 deterministic-random assignments from a 394-entry filtered pool (29 high-flag-level entries deferred to gandalf review; 0 restricted).

### Why (one line)

Operationalizes the kit-binds-1:1-to-star-sign architectural commitment (Branch A half per Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09) at MVP scope per Matt 2026-06-09 directive ("3 kits map cleanly; rest random"); unblocks drax /forge cosmograph kits-as-constellations rendering + downstream mantis UE port WS1 DataTable ingestion of `star_sign_id` without pre-committing to full-corpus canonical semantic mapping methodology (deferred to Cycle 15+ Pattern B once empirical vertical-slice playtest informs).

### Who's affected

- **Drax** — `/forge` cosmograph consumer: read `public/kit-space/kit_star_sign_assignments.json` alongside existing `faction_assignments.json` + per-kit JSONs; `star_sign_id` is the FK into the Legolas zodiac corpus (sign_id key); `star_sign_name` + `star_sign_tradition` are denormalized for direct display without corpus-load dependency. Rendering kits-as-constellations is a separate Phase 5 or amendment dispatch — this MIGRATION lands the data surface, not the rendering.
- **Mantis (PC seam; downstream)** — UE port WS1 absorbs `star_sign_id` via DataTable ingestion when WS1 scope is authored. No immediate action; surface for awareness.
- **Gandalf** — design-review surface: 29 high-sensitivity-flag corpus entries deferred to gandalf review per dispatch § 3.4 (substrate-cleanliness-over-volume default applied). If gandalf reviews + decides any subset should be includable in the random pool, bump filter policy in script and re-run (deterministic; only affected RANDOM assignments shift).
- **Star-lord** — engine emit is NOT affected. The kit JSON files at `public/kit-space/kits/` were NOT modified (no kit regeneration triggered). Engine-side telemetry has no new write path.
- **Rocket** — engine-side generation has no new dependency. Kit corpus generation continues to emit the existing schema; the sidecar is purely an elrond-seam additive curation pass on top of generated kit IDs.
- **Knight-rider** — wave-close routing surface: this commission is the Phase 2 closure of dispatch `2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md`. Phase 1 (gandalf hand-curation) committed prior at `7d334d7`.
- **Legolas** — substrate-source-of-truth: 423-entry zodiac corpus is the canonical source-of-truth for sign_id resolution; future corpus updates (per-tradition additions; sensitivity-flag refinements) will require Phase 2 re-run to propagate.
- **Matt** — no action required; commission MVP scope satisfied per dispatch acceptance criteria.

### What downstream consumers need to do

**Drax (when /forge cosmograph rendering phase fires):**
1. Load `kit_star_sign_assignments.json` alongside `faction_assignments.json` (parallel sidecar pattern; same loading discipline)
2. Use `star_sign_id` as FK into Legolas corpus for full sign data (mythic_narrative, star_coordinates, asterism_schematic, etc.); use `star_sign_name` + `star_sign_tradition` denormalized fields for tooltip/label rendering without corpus dependency
3. Distinguish HAND_CURATED vs RANDOM assignments in UI presentation if narrative-richness emphasis is desired (e.g., HAND_CURATED kits get prominent star-sign narrative overlay; RANDOM kits get minimal sign-name binding)
4. The 3 HAND_CURATED mappings have `hand_curated_anchor` field referencing gandalf doc § anchors for traceability

**Mantis (when UE port WS1 commission fires):**
1. Add `star_sign_id` (string FK) + `star_sign_assignment_method` (enum string) columns to kit DataTable schema
2. Ingest from `kit_star_sign_assignments.json` at import time; reverse-lookup against zodiac corpus for full sign data
3. No engine-side runtime LLM dependency (D7 AI-tell line preserved)

**Gandalf (downstream review of deferred high-flag-level entries):**
1. Review the 29 high-sensitivity-flag corpus entries (any of the 423 zodiac entries with `cultural_sensitivity.flag_level == "high"`)
2. Per-entry include/exclude decision; for any entries promoted from deferred to eligible, document rationale per Discipline #25 (semantic-layer rep-audit) and bump script `ELIGIBLE_FLAG_LEVELS` or `DEFERRED_FLAG_LEVELS` constants accordingly
3. Re-run script; deterministic — only RANDOM-method assignments shift (HAND_CURATED unaffected)

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema):** sidecar pattern parallels the established `faction_assignments.json` precedent (event_id `kse_20260602_008`); no NEW cross-seam contract — same sidecar discipline as cycle-18 Issue 5A. No Matt re-approval required; covered by parent dispatch `2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md` authorization (Matt 2026-06-09 directive).
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the requirement. Drax-side does not need a parallel MIGRATION; consumption is loadout-app data-ingestion (parallel to existing faction_assignments.json consumption pattern). Mantis-side adds a MIGRATION when WS1 ingestion lands.
- **ADR-006 (external-systems writes require authorization):** the write is to a meta-repo-adjacent loadout-public asset under elrond-domain authority for catalogue/abstraction-analysis data. Push to remote remains Matt-explicit-authorization per CLAUDE.md addendum; this entry covers auto-commit only.
- **Discipline #59 (substrate-coverage honesty):** flagged in close report — random assignment WILL produce kit-pairs sharing the same star_sign_id (birthday-paradox math: 34 picks from 394 pool → ~1.5 expected collisions). Two collision-pairs observed empirically (`andean-001 Yacana` hit by fire_000006 + wind_000004; `aztec-tonalpohualli-004 Cuetzpallin` hit by physical_000019 + water_000006; `iau-constellations-033-dorado` hit by physical_000014 + wind_000005; `western-zodiac-005 Leo` hit by earth_000006 + wind_000006). Uniqueness was NOT a dispatch requirement — many-to-one mapping is architecturally acceptable at MVP scope (cosmograph visualization layer; multiple kits can orbit one star-sign). Surfaced as observation for Phase 3 design review.

### Open follow-ons (not blocking the lock)

1. **Gandalf review of 29 high-flag-level deferred entries** — non-blocking; default exclusion preserved substrate-cleanliness; review can promote subset to eligible if appropriate per culture-specific assessment; re-run script propagates.
2. **Cycle 15+ Pattern B canonical semantic mapping** — replaces RANDOM assignments with semantic methodology (similarity / curated rule-table / hybrid) per dispatch § 1; gated on vertical-slice spike playtest empirical signal informing methodology choice.
3. **Star-sign-to-kit reverse-mapping** — out of scope per dispatch § 6; can be derived at query time from forward mapping if needed by drax /forge.
4. **Seasonal-substrate-rotation operator integration** — per atomic-substrate-registry Layer 0.5; the 3 hand-curated mappings have per-season cultural-variant alternatives documented in gandalf Phase 1 doc § 4.3 (Krittika → Pleiades/Matariki/Mǎo; Hercules → Gilgamesh/Thor/Bhima; Mula → Ketu/Scorpius/Andean dark-cloud). Operator design is downstream of this MVP.
5. **Cross-tradition collision-handling** — the 4 observed RANDOM-collision pairs are MVP-acceptable but worth surfacing if cosmograph visualization makes the same-star-sign coupling visually awkward; uniqueness constraint can be added in a future re-run if desired (constrained random sampling without replacement up to pool size).

---

## v1.9 — EAA-4 chronicle implementation slice — `kit_space_chronicle.json` source-of-truth landed + smoke 9/9 PASS — 2026-06-02

### What changed (one line)

Implemented the EAA-4 chronicle source-of-truth layer per the v1.8 joint design verdict: authored `CHRONICLE_SCHEMA.md` v1.0 (per-event entry shape + 4-field lineage_tags substructure + emit-order discipline) at `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`, landed empty `kit_space_chronicle.json` source-of-truth file ready for EAA-5 first-fire, landed kit_space/ directory layout (`README.md` + `kits/` empty dir), authored smoke-test script verifying 9/9 round-trip checks PASS (TempDir + live), verified cleanup discipline (live dir returns to clean ready state).

### Why (one line)

Operationalizes the v1.8 joint design verdict for the EAA-4 chronicle-implementation slice specifically (the v1.8 entry authored the joint EAA-3 + EAA-4 design + format locks + shadow-table DDL; this entry lands the chronicle source-of-truth surface + smoke-test that downstream — EAA-5 first-fire — consumes); composes natively with EAA-3 per-kit JSON (rocket) on the locked FK format (`kse_<YYYYMMDD>_<seq3>`).

### Who's affected

- **Star-lord** — engine emit integration (per CHRONICLE_SCHEMA.md § 5 emit-order discipline): mint `event_id` per joint spec § 1.3 → append chronicle event entry FIRST to `kit_space_chronicle.json` (atomic write) → emit per-kit JSONs SECOND. Engine-side companion MIGRATION.md entry SHOULD be authored at `reincarnated-engine/src/reincarnated/output/MIGRATION.md` or `export/MIGRATION.md` when emit-integration commit lands.
- **Rocket** — EAA-3 per-kit JSON schema MUST adopt the locked FK format for `kit_space_expansion_event_id` per joint spec § 1; per-kit JSON lands under `data/kit_space/kits/kit_<primary>_<seq6>.json` per joint spec § 5.
- **Drax** — EAA-7 engine page reframe (LOCK O scope): consumes `data/kit_space/kit_space_chronicle.json` via single `fetch()`; flat JSON shape per CHRONICLE_SCHEMA.md § 4. Not blocking EAA-5.
- **Elrond (self; future post-EAA-5)** — shadow-table CREATE + ingest scripts deferred to post-EAA-5 (the joint spec § 3.5 authored the DDL; ingest implementation fires when first real chronicle data exists). Rebuildable from filesystem per joint spec § 3.2.
- **Gandalf** — design steward; chronicle's `substrate_inputs_changed` + `event_scope` + `lineage_tags` fields surface design narrative for engine-page rendering (EAA-7). Not load-bearing at this phase.
- **Jack-ryan** — Gate-2 review on this implementation + v1.8 joint design + smoke results.
- **Knight-rider** — receives EAA-4 completion report; routes Gate-2.
- **Matt** — no action; LOCK K + cycle-push pre-authorized.

### What downstream consumers need to do

**Star-lord (REQUIRED before or coincident with EAA-5 fire):**
1. Implement emit-order discipline per CHRONICLE_SCHEMA.md § 5: chronicle entry FIRST → per-kit JSONs SECOND
2. Use joint spec § 1.3 reference impl for `event_id` minting: query chronicle for `prior_today_count`; `+1`; format `kse_YYYYMMDD_seq3`
3. Use atomic-write convention: write to `.tmp` → `os.replace`
4. Author engine-side companion MIGRATION.md entry per ADR-004 round-trip
5. Surface `engine_version_sha` as 7-char short (`git rev-parse --short=7 HEAD`)

**Rocket (REQUIRED for EAA-3 schema spec):** include `kit_space_expansion_event_id` field per joint spec § 4.1; format MUST match `^kse_\d{8}_\d{3}$`. Per-kit JSON lands at `data/kit_space/kits/<kit_id>.json`. Per-skill `flavor_decision` + `flavor_word_used` cross-coupling per EAA-1 § 3 + joint spec § 4.3.

**Drax (EAA-7 scope; not blocking EAA-5):** consume `kit_space_chronicle.json` via `fetch('/data/kit_space/kit_space_chronicle.json')`; render `events[]` via existing `EngineStatePipelineFlow` component pattern per LOCK O.

**Jack-ryan (Gate-2):** review chronicle schema (`reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`) + smoke results (9/9 PASS TempDir + 9/9 PASS live; cleanup verified clean state) + this v1.9 entry composing on v1.8 design verdict.

### Schema diff or example before/after

**Before this implementation slice:** v1.8 design verdict authored format locks + storage medium choice + shadow-table DDL; NO chronicle source-of-truth file existed; NO directory layout existed; NO smoke-test existed.

**After this implementation slice:**

```
reincarnated-engine/data/kit_space/
├── README.md                                # NEW; directory layout + consumer guide
├── chronicle/
│   └── CHRONICLE_SCHEMA.md                  # NEW; per-event entry schema v1.0 + emit-order discipline
├── kit_space_chronicle.json                 # NEW; empty source-of-truth (events: []) ready for first emit
└── kits/                                    # NEW; empty dir (EAA-3 populates per-kit JSONs; star-lord emit fills)
```

**Chronicle file shape (per joint spec § 3.4 + CHRONICLE_SCHEMA.md § 4):** `{schema_version, schema_notes, events: [event-entry...]}` where each event-entry has required fields `event_id`, `event_type`, `event_timestamp`, `event_date_utc`, `event_scope`, `substrate_inputs_changed`, `engine_version_sha`, `kit_ids_generated`, `kit_count`; optional fields `engine_version_full`, `skip_flags_active`, `lineage_tags`, `generation_parameters`, `substrate_trace_summary`, `notes`.

**Format locks (re-stating from joint spec § 1 + § 2; preserved verbatim):**

| Field | Format | Regex |
|---|---|---|
| `event_id` | `kse_<YYYYMMDD>_<seq3>` | `^kse_\d{8}_\d{3}$` |
| `kit_id` | `kit_<primary>_<seq6>` | `^kit_(fire\|water\|earth\|wind\|lightning\|holy\|shadow\|physical)_\d{6}$` |
| `primary_element` | lowercase canonical-7+1 | — |
| `period` | uppercase enum nullable | — |
| `engine_version_sha` | 7-char short SHA | `^[0-9a-f]{7}$` |

### Smoke-test results (Discipline #2)

Script: `agentic_orchestration/research/scripts/eaa_4_chronicle_smoke_2026_06_02.py`

Modes verified:
- `python3 eaa_4_chronicle_smoke_2026_06_02.py` — TempDir dry-run: **9/9 PASS**
- `python3 eaa_4_chronicle_smoke_2026_06_02.py --live` — write to live engine `data/kit_space/`: **9/9 PASS**
- `python3 eaa_4_chronicle_smoke_2026_06_02.py --cleanup-live` — remove smoke artifacts: **verified clean state** (chronicle returned to `events: []`; smoke kit JSON removed; ready for EAA-5)

Round-trip checks (all 9 PASS both TempDir + live):
1. event_id regex match (`^kse_\d{8}_\d{3}$`)
2. kit_id regex match (`^kit_(canonical-7+1)_\d{6}$`)
3. chronicle JSON round-trips through `json.load`
4. chronicle contains target event (event_id appended correctly)
5. chronicle event's `kit_ids_generated` contains kit_id
6. per-kit JSON exists + round-trips
7. per-kit FK matches chronicle event_id
8. per-kit `primary_element` matches kit_id encoding (FK integrity in two-direction)
9. chronicle `event_date_utc` matches event_id date segment (denormalization consistency)

Smoke uses reserved seq6 range (kit_shadow_999xxx) to avoid colliding with real generation; smoke kits + events tagged with sentinel `_smoke_test_stub: true` for safe cleanup identification.

### Storage medium decision (re-stating v1.8 joint spec § 3.1)

Per joint spec § 3.1: **Option α (source-of-truth) + Option β-light (analytical shadow)**.

- Option α: flat `data/kit_space/kit_space_chronicle.json` (this v1.9 implements)
- Option β-light: `engine_kit_space_events` + `engine_kit_index` in elrond's catalogue.db (DDL authored in joint spec § 3.5; ingest implementation deferred to post-EAA-5)

This v1.9 lands the source-of-truth surface only. Shadow-table CREATE + ingest scripts are queued for post-EAA-5 (when first real chronicle data exists to ingest).

### Backward compatibility

- This implementation is **NEW + ADDITIVE** per LOCK J + LOCK K
- Existing `seasons/season_*` (season_000001-200) preserved as historical per Path α — not migrated
- Engine emit branches on EAA-2 skip flags: skip-flags-active → emit to `data/kit_space/`; skip-flags-inactive → emit to legacy `seasons/season_*` per pre-EAA convention
- Drax consumes BOTH layouts; data-shape distinguishable by directory location
- Verified via smoke-test cleanup: live `data/kit_space/` returns to clean ready state (chronicle `events: []`); no irreversible state introduced

### Coordination with EAA-3 (rocket primary) — FK format compose

The locked FK format (`kse_<YYYYMMDD>_<seq3>`) is **shared verbatim** between EAA-3 per-kit JSON `kit_space_expansion_event_id` field and EAA-4 chronicle `event_id` field. Authoritative source: joint spec § 1. Rocket's EAA-3 schema spec MUST adopt this format. This v1.9 implementation respects the format; smoke-test verifies it.

A prior `eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md` doc was authored in parallel proposing an alternative `kse_<YYYYMMDD>_<HHMMSS>_<6hex>` format; that doc has been **SUPERSEDED** and now redirects to the joint spec as authoritative.

### Files committed (this v1.9 entry)

- `reincarnated-engine/data/kit_space/README.md` — NEW; directory layout + consumer guide + format-lock summary
- `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md` — NEW; chronicle schema v1.0 spec
- `reincarnated-engine/data/kit_space/kit_space_chronicle.json` — NEW; empty source-of-truth (`events: []`) ready for EAA-5
- `reincarnated-engine/data/kit_space/kits/` — NEW empty dir (rocket EAA-3 populates)
- `agentic_orchestration/research/scripts/eaa_4_chronicle_smoke_2026_06_02.py` — NEW; smoke-test (9/9 PASS verified)
- `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md` — SUPERSEDED (redirects to joint spec)
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.9; composing on v1.8)

### Related canonical docs + disciplines

- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.4 (chronicle commitment)
- `agentic_orchestration/dispatches/2026-06-02-eaa-4-kit-space-chronicle-infrastructure.md` (this dispatch)
- `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` (authoritative joint design verdict; v1.8 MIGRATION entry covers)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-phase-1-batch-gate-1.md` (Phase-1 batch Gate-1; recommended amendment 2 — FK format coordination — fulfilled by joint spec + this implementation)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (wave-open INFO-3 — per-kit engagement telemetry out-of-scope — respected in CHRONICLE_SCHEMA.md § 9)
- Discipline #2 (smoke-gate; 9/9 PASS satisfies), #6 (cross-seam contract; satisfied via joint spec + this v1.9 round-trip), #8 (schema validation at boundaries; chronicle schema versioned + atomic-write), #10 (attribution clarity; engine_version_sha + lineage_tags), #11 (empirical inspection; smoke verifies live dir state)
- ADR-004 (cross-seam MIGRATION) + ADR-006 (read-only-by-default external systems; engine owns kit_space/ writes; elrond owns catalogue.db shadow-table writes per joint spec § 3.5; no remote pushes from this step)

### Routing back to KR

- Joint design verdict v1.8 authored + LOCKED (FK format + kit_id format + storage medium + shadow-table DDL + 5 iteration points named for rocket EAA-3)
- Chronicle source-of-truth layer LANDED (CHRONICLE_SCHEMA.md + empty chronicle JSON + layout README)
- Smoke-test 9/9 PASS TempDir + 9/9 PASS live + cleanup verified clean state
- Live `data/kit_space/` ready for EAA-5 first-fire consumption (empty chronicle; star-lord emit-integration may co-fire with EAA-5)
- Cross-dispatch FK format LOCKED + SUPERSEDED-coord-doc redirects to joint spec
- Star-lord engine-emit integration (per CHRONICLE_SCHEMA.md § 5) is the named NEXT cross-seam touch; companion MIGRATION.md entry recommended on engine-emit commit
- Routing back: **proceed to jack-ryan Gate-2** on v1.8 joint design + v1.9 implementation slice + smoke results; EAA-4 acceptance criteria 1, 2, 4, 5, 6 satisfied; AC #3 (engine emit path) lands at star-lord integration

---

## v1.8 — EAA-3 + EAA-4 — engine kit_space shadow tables (engine_kit_index + engine_kit_space_events) — 2026-06-02

### What changed (one line)

Authored ELROND-SIDE schema for cycle-16 EAA-3 (per-kit JSON output) + EAA-4 (kit-space chronicle infrastructure) as joint cross-dispatch spec: locked `kit_id` format (`kit_<primary>_<seq6>`) + `kit_space_expansion_event_id` format (`kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` per pre-existing coordination note at `cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md`); chose Option α (filesystem source-of-truth at `reincarnated-engine/data/kit_space/`) + Option β-light (additive shadow tables `engine_kit_index` + `engine_kit_space_events` in curated catalogue.db) as analytical-index for cross-cutting joins; confirmed elrond ingest-compat against rocket DRAFT per-kit JSON schema with 5 iteration points named for joint resolution.

### Why (one line)

Operationalizes canonical record `2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4 (continuous kit space + parameter-expansion-event chronicle); replaces per-season manifest as engine output unit (additive; historical seasons preserved per Path α); composes EAA-3 + EAA-4 elrond-side decisions before either rocket spec (EAA-3) or elrond chronicle implementation (EAA-4) finalizes, per Phase 1 batch Gate-1 INFO-B amendment (jack-ryan).

### Who's affected

- **Rocket** — owns engine emit (per-kit JSON shape, EAA-3 primary); MUST consume FK format lock (§ 1 of joint spec note) + kit_id format lock (§ 2); MUST align engine-side enum casing on 5 iteration points named in joint spec note § 4.4 (primary_element lowercase / period uppercase enum / engine_version short-sha format / emit ordering chronicle-first / flavor_decision+flavor_word_used integrity at per-skill level).
- **Star-lord** — owns engine output pipeline (EAA-3 + EAA-4 co-owner on emit); MUST implement chronicle event emit FIRST then per-kit JSONs SECOND (atomicity discipline § 5 of joint spec note); MUST emit `engine_version` short-sha consistently; MAY trigger elrond shadow ingest as post-emit hook.
- **Drax** — LOCK O scope (EAA-6 + EAA-7); consumes kit space output + chronicle for loadout app + engine page reframe; NOT impacted by this MIGRATION (consumption deferred to those workstreams).
- **Gandalf** — design steward; new chronicle event log provides design-narrative substrate for engine page + Realm-Expansion-targeting-underplayed-kits future workstream; new shadow tables enable cross-cutting analytical queries.
- **Jack-ryan** — Gate-2 review (BLOCK authority) on EAA-3 + EAA-4 schema spec including this MIGRATION; verifies FK format consistency across dispatches + LOCK K ADDITIVE-AND-REVERSIBLE discipline + cross-seam contract reversibility.
- **Knight-rider** — receives report-back; routes Gate-2; sequences EAA-5 first-fire to consume EAA-3 + EAA-4 infrastructure.
- **Legolas** — no action.
- **Matt** — LAST-resort escalation if (a) rocket DRAFT diverges substantially from joint spec § 4 on any of 5 iteration points AND iteration cycle fails to converge OR (b) cross-seam contract reversibility surfaces unexpected coupling.

### What downstream consumers need to do

**Rocket (EAA-3 implementation):**
- Author per-kit JSON schema as DRAFT (per joint spec note § 4); iterate against five iteration points if engine-side surfaces divergence
- Engine-side `primary_element` enum: lowercase canonical-7+1 only (`fire`, `water`, `earth`, `wind`, `lightning`, `holy`, `shadow`, `physical`)
- Engine-side `period` enum: uppercase WS2.P2 substrate values (`ANCIENT`, `MEDIEVAL`, `MODERN`) when populated; nullable when substrate doesn't supply
- Engine emit `kit_id` using `mint_kit_id(primary, prior_primary_count)` rule (joint spec § 2.4)
- Engine emit `kit_space_expansion_event_id` using `mint_kit_space_expansion_event_id(event_date_utc, prior_today_count)` rule (joint spec § 1.3)
- Engine emit `lineage_tags` 4-field substructure: `kit_space_lineage` / `engine_provenance` / `substrate_provenance` / `generation_cohort_date`

**Star-lord (EAA-3 + EAA-4 emit pipeline):**
- Implement emit-order discipline: chronicle event entry FIRST, then per-kit JSON entries (so FK target exists in chronicle when shadow ingest runs)
- Implement chronicle JSON shape per joint spec § 3.4 (events array; schema_version present)
- Source `engine_version_sha` from `git rev-parse --short=7 HEAD` at fire-time; commit at emit-time
- Path discipline: `data/kit_space/kit_space_chronicle.json` + `data/kit_space/kits/<kit_id>.json` per kit; optional `data/kit_space/kits_index.json`

**Elrond (this MIGRATION + EAA-3/4 implementation):**
- Author shadow-table CREATE script (DDL at joint spec § 3.5)
- Author ingest script: walks `data/kit_space/`; upserts to `engine_kit_index` + `engine_kit_space_events`; tolerates partial emissions (skips kit if FK target missing; surfaces warning)
- Rebuildable: truncate + reload = deterministic
- Smoke-test against EAA-5 first-fire output (joint spec § 7)

**Drax / Gandalf (no immediate action; future workstreams):**
- Drax EAA-6 (loadout MVP) + EAA-7 (engine page MVP) consume kit space + chronicle via LOCK O existing-components-only discipline; deferred
- Gandalf has new analytical surface for substrate-led discipline at content-engagement layer (Disc #41 composition; future Realm Expansion targeting underplayed-kit telemetry)

### Schema diff or example before/after

**Old (per-season manifest path; legacy; PRESERVED for historical seasons per Path α):**
- `seasons/season_NNNNNN/manifest.json` — per-season summary + theme element + cosmological_vocabulary + class JSON refs
- `seasons/season_NNNNNN/classes/class_NNNN.json` — per-class skill + stat data; season-anchored numbering
- No cross-file foreign key; class id is season-scoped

**New (per-kit + chronicle path; ADDITIVE; emitted when EAA-2 skip flags active):**
- `data/kit_space/kit_space_chronicle.json` — append-only event list; `events: [{event_id, event_type, event_timestamp, event_scope, substrate_inputs_changed, engine_version_sha, kit_ids_generated, kit_count, skip_flags_active, lineage_tags}]`
- `data/kit_space/kits/kit_<primary>_<seq6>.json` — per-kit; `{kit_id, primary_element, cultural_tradition, period, chain_composition, t4_selection, supporting_chain, skills, emergent_kit_concept, substrate_trace, kit_space_expansion_event_id, engine_version, generation_timestamp, lineage_tags}`
- Foreign key: per-kit `kit_space_expansion_event_id` → chronicle `event_id` (format: `kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>`; regex `^kse_\d{8}_\d{6}_[0-9a-f]{6}$`; per pre-existing coordination note)
- Per-skill EAA-1 metadata: each `skills[]` entry carries `flavor_decision: bool` + `flavor_word_used: str | null` (cross-coupled per EAA-1 § 3 plus joint spec § 4.3)

**New shadow tables (elrond catalogue.db; ADDITIVE; rebuildable from filesystem):**

```sql
-- engine_kit_space_events: per-chronicle-event row indexed by event_id
CREATE TABLE engine_kit_space_events (
    event_id                TEXT PRIMARY KEY,                      -- kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>
                                                                   -- regex: ^kse_\d{8}_\d{6}_[0-9a-f]{6}$ (27 chars)
    event_uuid_full         TEXT,                                  -- full UUID4 source for the 6-char-hex suffix (nullable; provenance trace)
    event_type              TEXT NOT NULL DEFAULT 'kit-space-expansion'
                            CHECK (event_type IN ('kit-space-expansion', 'realm-expansion', 'reserved-future')),
    event_timestamp         TEXT NOT NULL,                         -- ISO-8601 UTC
    event_date_utc          TEXT NOT NULL,                         -- ISO date
    event_scope             TEXT NOT NULL,
    substrate_inputs_changed_json TEXT NOT NULL,
    engine_version_sha      TEXT NOT NULL,
    engine_version_full     TEXT,
    kit_count               INTEGER NOT NULL CHECK (kit_count >= 0),
    skip_flags_active_json  TEXT,
    lineage_tags_json       TEXT,
    source_chronicle_path   TEXT NOT NULL,
    ingest_timestamp        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kse_event_date ON engine_kit_space_events(event_date_utc);
CREATE INDEX idx_kse_event_type ON engine_kit_space_events(event_type);

-- engine_kit_index: per-kit row indexed by kit_id
CREATE TABLE engine_kit_index (
    kit_id                          TEXT PRIMARY KEY,                  -- kit_<primary>_<seq6>
    primary_element                 TEXT NOT NULL
                                    CHECK (primary_element IN ('fire', 'water', 'earth', 'wind', 'lightning', 'holy', 'shadow', 'physical')),
    cultural_tradition              TEXT,
    period                          TEXT
                                    CHECK (period IS NULL OR period IN ('ANCIENT', 'MEDIEVAL', 'MODERN')),
    emergent_kit_concept            TEXT,
    chain_composition_json          TEXT,
    t4_selection_json               TEXT,
    supporting_chain_json           TEXT,
    skill_count                     INTEGER NOT NULL CHECK (skill_count >= 0),
    skills_summary_json             TEXT NOT NULL,
    substrate_trace_json            TEXT NOT NULL,
    kit_space_expansion_event_id    TEXT NOT NULL REFERENCES engine_kit_space_events(event_id),
    engine_version_sha              TEXT NOT NULL,
    generation_timestamp            TEXT NOT NULL,
    lineage_tags_json               TEXT,
    source_kit_json_path            TEXT NOT NULL,
    ingest_timestamp                TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kit_primary ON engine_kit_index(primary_element);
CREATE INDEX idx_kit_event ON engine_kit_index(kit_space_expansion_event_id);
CREATE INDEX idx_kit_period ON engine_kit_index(period);
CREATE INDEX idx_kit_cultural_tradition ON engine_kit_index(cultural_tradition);
```

**schema_meta entry:**
```sql
INSERT INTO schema_meta (version, applied_at, description) VALUES (
    'v1.8-eaa-3-plus-4-engine-kit-shadow-tables',
    CURRENT_TIMESTAMP,
    'EAA-3 + EAA-4: engine_kit_index + engine_kit_space_events shadow tables; additive; rebuildable from kit_space/ filesystem; source-of-truth lives at reincarnated-engine/data/kit_space/*.json.'
);
```

### Format locks (cross-dispatch coordination per Phase 1 batch Gate-1 INFO-B amendment)

**LOCKED jointly between EAA-3 (rocket) + EAA-4 (elrond) per LOCK K:**

| Field | Format | Owner |
|---|---|---|
| `kit_id` | `kit_<primary>_<seq6>` (e.g., `kit_shadow_000001`) | elrond decision per LOCK K; rocket implements emit |
| `kit_space_expansion_event_id` | `kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` (e.g., `kse_20260602_143052_a1b2c3`); per pre-existing coordination note | elrond decision per LOCK K (pre-existing coordination artifact); rocket + star-lord implement emit |
| `primary_element` | lowercase canonical-7+1 (`fire`, `water`, `earth`, `wind`, `lightning`, `holy`, `shadow`, `physical`) | upstream canonical-7+1 lock; rocket emit must match |
| `period` | uppercase `ANCIENT` / `MEDIEVAL` / `MODERN` (nullable when substrate doesn't supply) | WS2.P2 substrate convention; rocket emit must match |
| `engine_version_sha` | 7-char short sha (`git rev-parse --short=7 HEAD`) | star-lord seam; consistent across emit |
| `lineage_tags` substructure | 4-field object (`kit_space_lineage` / `engine_provenance` / `substrate_provenance` / `generation_cohort_date`) per pool.json v1.1 pattern | elrond decision per LOCK K; rocket + star-lord populate |

### Migration verification (deferred to EAA-3 + EAA-4 implementation; this MIGRATION authors design)

Acceptance criteria (verified at jack-ryan Gate-2 + EAA-5 smoke-test):
- [ ] Rocket per-kit JSON schema spec PASSES Gate-2 with format locks applied
- [ ] Star-lord chronicle emit + per-kit emit lands in `data/kit_space/` per § 5 layout
- [ ] elrond shadow-table CREATE script runs against catalogue.db; idempotent
- [ ] elrond ingest script populates shadow tables from filesystem; deterministic rebuild
- [ ] Single-event-single-kit smoke (§ 7 joint spec) passes end-to-end
- [ ] FK integrity: every `engine_kit_index.kit_space_expansion_event_id` resolves to `engine_kit_space_events.event_id`
- [ ] Backward-compat: existing season manifests + class JSONs at `seasons/` unchanged
- [ ] Reversibility (LOCK J): dropping shadow tables and deleting `kit_space/` directory both restore prior-state cleanly

### Files committed (this MIGRATION authoring step)

- `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` — joint elrond-side spec (10 sections; LOCKED kit_id + event_id formats; shadow-table DDL; ingest-compat verdict)
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.8)

**Deferred to EAA-3 + EAA-4 implementation phase (post-Gate-2):**
- `agentic_orchestration/research/scripts/eaa_3_4_create_kit_shadow_tables_2026_06_02.py` — shadow-table CREATE script
- `agentic_orchestration/research/scripts/eaa_3_4_ingest_kit_space_2026_06_02.py` — ingest from filesystem
- Smoke-test scripts (single-event-single-kit; rebuild determinism; FK integrity)
- Engine-side EAA-3 schema implementation (rocket); engine-side EAA-4 chronicle emit (star-lord)

### Related canonical docs + disciplines

- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4 (binding architectural commitment)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary lock; consumed by per-skill flavor naming + lineage tag substrate provenance)
- `agentic_orchestration/dispatches/2026-06-02-eaa-3-kit-space-output-schema.md` (rocket primary + elrond co-owner)
- `agentic_orchestration/dispatches/2026-06-02-eaa-4-kit-space-chronicle-infrastructure.md` (elrond primary + star-lord co-owner)
- `agentic_orchestration/qa/findings/2026-06-02-eaa-phase-1-batch-gate-1.md` (Phase 1 batch Gate-1 PASS-with-INFO; INFO-B amendment composed into this entry)
- `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md` (workstream status)
- Locks A-P (per gandalf transmission 2026-06-02; LOCK K active for engine schema design authority; LOCK J ADDITIVE-AND-REVERSIBLE heuristic governs both shadow tables and filesystem layout)
- Discipline #41 substrate-led (kit space is the substrate; engine emits per-kit entries; analytical layer reads substrate truth not pre-imposed taxonomy)
- ADR-004 (cross-seam MIGRATION discipline; this entry is the elrond-side artifact composing with future rocket-side engine emit MIGRATION)
- ADR-006 (read-only-by-default external systems; elrond owns curated catalogue.db writes; engine remains source-of-truth)

### Routing back to KR

- Joint spec authored ✅
- `kit_space_expansion_event_id` format LOCKED (§ 1) ✅
- `kit_id` format LOCKED (§ 2) ✅
- Chronicle storage medium LOCKED (§ 3) ✅
- elrond ingest-compat CONFIRMED (§ 4.4) ✅
- Five iteration points named for rocket DRAFT alignment (§ 4.4) — needs rocket acknowledgment
- Cross-seam MIGRATION.md COMMITTED at elrond seam boundary (this entry)
- Backward-compat statement complete (§ 6 of joint spec); historical seasons preserved
- Routing back: **proceed to rocket DRAFT review + jack-ryan Gate-2** (schema + MIGRATION) with format locks attached for joint verification

---

## v1.7 — WS1A.Q18 sub-phase 5f — pool.json v1.1 migration + physical_taxonomy.json — 2026-06-01

### What changed (one line)

Executed POST-WAVE pool.json v1.0→v1.1 schema-extension-and-data-migration per WS1A.Q18 PG-3 ratification: extended `PoolElement` with 4 additive fields, migrated `data/seasonal_elements/pool.json` from 156 → 214 entries (100 Architecture-A locked allow-list + 114 legacy preserved-as-quarantined), created `data/seasonal_elements/physical_taxonomy.json` as separate Architecture-A taxonomy-sibling registry (9 physical entries), authored engine-side ADR-004 MIGRATION.md companion entry.

### Why (one line)

Operationalizes WS1A.Q18 wave-close architectural commitment (Architecture A LOCKED 2026-06-01: 7 rotating primaries with substrate-honest flavor pools + physical-as-Architecture-A-taxonomy-sibling); deferred from wave-scope to sub-phase 5f POST-WAVE per ADR-004 cross-seam contract change discipline.

### Who's affected

- **Rocket** — owns engine generation; no immediate action required (backward-compat preserved); MAY consume new fields in future WS1A.3 theme-coherence gating per deferred-commitments item 5.1.1.
- **Star-lord** — owns telemetry/export; no immediate action required (telemetry packets do not currently read pool.json beyond named fields); MAY surface lineage tags in future telemetry-audit work.
- **Drax** — owns loadout/demo; zero impact (consumes engine-generated artifacts, not pool.json directly).
- **Gandalf** — design steward; new lineage tags enable per-tag distribution audit queries; useful surface for deferred-commitments items 5.1.1 (theme-coherence) + 5.1.2 (modern-caster substrate-gap).
- **Jack-ryan** — Gate-2 review (BLOCK authority) on this migration per dispatch § 4 acceptance criteria.
- **Knight-rider** — receives report-back; routes Gate-2; sequences cardinality-discrepancy ambiguity-surface for resolution.
- **Legolas** — no action.
- **Matt** — LAST-resort escalation for cardinality ambiguity surfaced below (internal inconsistency in canonical lock cardinality assertions vs verbatim per-primary lists).

### What downstream consumers need to do

**Rocket (no immediate action):** v1.1 schema is fully backward-compatible; existing selector.py + naming.py readers absorb new fields silently. Future lineage-tag-aware sub-element selection is a separate dispatch.

**Star-lord (no immediate action):** export packet schema unchanged. Future telemetry extension to surface lineage tags would be a separate dispatch.

**Drax (no action):** zero impact.

**Gandalf (no action; future query surface enabled):** new lineage tag enum supports per-tag-distribution queries.

### Schema diff or example before/after

**Engine-side MIGRATION.md companion entry** (authoritative engine-side schema spec): `reincarnated-engine/src/reincarnated/element/MIGRATION.md` § "[2026-06-01] WS1A.Q18 sub-phase 5f". Contains before/after schema diff, enum value spec, backward-compat verification, and migration order. This data-layer-side entry COMPOSES with the engine-side entry per ADR-004 round-trip discipline.

**Pool.json v1.1 file-level diff:**
- `version`: "1.0" → "1.1"
- New top-level fields: `schema_version: "1.1"`, `schema_notes`
- `elements` array: 156 → 214 entries (100 Architecture-A locked + 114 legacy preserved)

**New file: `data/seasonal_elements/physical_taxonomy.json`** — 9-entry Architecture-A taxonomy-sibling registry (4 damage_sub_type + 4 mechanical_action_vocabulary + 1 ailment). Physical kits opt out of WS1A.4 LLM judgment per canonical lock § 4.

### Cardinality discrepancies surfaced (NOT silently resolved — per dispatch ambiguity-surface protocol)

**Ambiguity 1 — Canonical lock cardinality (109 claimed vs 100 enumerated):** canonical lock + PG-3 ratification both assert "109 rotating-primary + 9 physical = 118 total", but per-primary verbatim entry lists (Gate-2-PASS-verified entry-by-entry) sum to 16+14+18+13+13+14+12 = **100**, not 109. Elrond seam decision: migrate against the verified verbatim per-primary lists; surface to KR for resolution by canonical-doc steward (gandalf) and/or PG-3 ratification author (Matt). Final lineage tag application targets adjusted to reconcile with 100-entry actual total.

**Ambiguity 2 — Lineage tag aggregate reconciliation:** PG-3 § 5 binding aggregate (65/24/19/1/9 = 118) does NOT reconcile with 100 actual rotating-primary entries. Canonical § 7.1 illustrative col-sum (57/19/23/1/9 = 109) DOES reconcile with 100 actual rotating-primary entries. Canonical § 7 explicit modern-scientific enumeration is 19 entries (matches PG-3 § 5; not § 7.1 col 23). Elrond seam decision: apply lineage tags per § 7.1 col-sum reconciliation BUT honor canonical § 7 explicit overlay enumeration → final per-entry distribution: 57/23/19/1 = 100 rotating + 9 physical = 109 actual total. Documented + traceable in migration script.

**Ambiguity 3 — INFO-1 `stormtide`:** stormtide appears in slot-routing decisions but NOT in the 109-entry rotating-primary lock NOR in v1.0 pool.json. Elrond seam decision: no-op (no entry to route; slot-routing decision preserved in script for future reference).

### Migration verification

- ✅ Schema-extended PoolElement reads v1.1 pool.json cleanly (all 214 entries parse)
- ✅ Pre-extension PoolElement reads v1.1 pool.json cleanly (backward-compat)
- ✅ Round-trip JSON parse OK for pool.json + physical_taxonomy.json
- ✅ Lineage-tag aggregate matches § 7.1 col-sums: 57+23+19+1 = 100 rotating + 9 physical = 109
- ✅ Slot routing applied: mist → water primary (was wind)
- ✅ Cull-tag dispositions applied: thorn promoted (drift-14-plant-anatomical dissolved-for-thorn); cyclone/whirlwind/squall/hurricane cull-tag dissolved (entries now in lock); typhoon legacy with cull-tag preserved
- ✅ Drift-14 invariant validator still fires for new entries that lack VFX manifest coverage (expected; future surface)

### Files committed (this MIGRATION)

- `reincarnated-engine/src/reincarnated/element/schema.py` — PoolElement extended with 4 additive fields
- `reincarnated-engine/src/reincarnated/element/pool.py` — add_element_to_pool() preserves new fields
- `reincarnated-engine/src/reincarnated/element/MIGRATION.md` — engine-side cross-seam MIGRATION entry
- `reincarnated-engine/data/seasonal_elements/pool.json` — v1.0 → v1.1 (156 → 214 entries)
- `reincarnated-engine/data/seasonal_elements/pool.json.pre-q18-2026-06-01-backup` — pre-migration snapshot
- `reincarnated-engine/data/seasonal_elements/physical_taxonomy.json` — NEW Architecture-A taxonomy registry
- `agentic_orchestration/research/scripts/q18_pool_migration_2026_06_01.py` — migration script
- `agentic_orchestration/research/curated/MIGRATION.md` — THIS entry (v1.7)

### Related canonical docs + disciplines

- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Architecture A LOCK)
- `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md` (wave-close record)
- `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` (PG-3 ratification)
- `agentic_orchestration/dispatches/2026-06-01-elrond-cycle-15-ws1a-q18-sub-phase-5f-pool-migration.md` (this dispatch)
- Discipline #41 (substrate-led) + #49 (substrate-silence ≠ substrate-validation; the 23 substrate-silent lineage tags here are this discipline's first operational application) + #50 (3-test inclusion gate) + #51 (synthesis-draft adversarial Pattern B critique)
- ADR-004 (cross-seam MIGRATION discipline) + ADR-006 (read-only-by-default external systems)

### Routing back to KR

- Migration COMMITTED per acceptance criteria § 4
- Cross-seam MIGRATION.md COMMITTED at engine-side seam boundary
- Backward-compat VERIFIED (pre-extension + extended schemas both parse pool.json v1.1 cleanly)
- Per-entry lineage tag application: clean per § 7.1 col-sum reconciliation; 3 ambiguities surfaced — see above; do NOT silently resolved
- Cross-seam touches surfaced for follow-on: NONE require secondary dispatch (rocket + star-lord + drax all confirmed no-action-required)
- Routing back: **proceed to jack-ryan Gate-2 (schema + migration review)** with cardinality-discrepancy ambiguity-surface attached for joint resolution

---

## v1.6 — Pattern A: Tier 5.1/5.2 final curation — additive schema spec + manifest extension — 2026-05-18

### What changed (one line)

Authored additive catalogue-DB schema spec (`catalogue-db-schema-v2-2026-05-18.md`) introducing `usage_recommendation` + `license_class` enum columns on `catalogue_assets` per Matt L3 Tier 5.2 approval; extended `ambient-props-subset-vs2a-2026-05-17.jsonl` with 8 new prop rows (Tier 5.1 prop pool extension); authored consolidated drax v1.21+ handoff brief covering icons + props + credits.txt + schema cross-reference.

### Why (one line)

Closes Tier 5.1 (Game-icons.net SIL-1.1 / consistent prop scale 0.75× / medium decoration density / single credits.txt) + Tier 5.2 (additive schema rubber-stamp); operationalizes the dungeon-objects audit § 6 curation lesson at schema level (per-file `usage_recommendation` prevents shred-defect class); enables programmatic credits.txt generation via `license_class` per-asset specific-license tracking.

### Who's affected

- **Drax** — receives `tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` as consumption-ready brief for v1.21+ wire-in (queued post-mobile-chain + post-chierit-monster-wiring; lowest VS2a polish priority). Brief covers 28-icon game-icons.net role mapping, `PROP_RENDER_SCALE_OVERRIDE = 0.75` application, 8 new prop descriptors with source coords, complete credits.txt verbatim text, schema cross-reference. No drax-side schema consumption required in v1.21+ pass (schema is upstream-curator-facing; future passes populate the new columns).
- **Legolas** — no action; future Mode B crawls can populate `usage_recommendation` per persona-rule extension if knight-rider sequences. Optional addition to legolas.md per-row output format.
- **Gandalf** — schema additions enable license-risk + per-class-substrate queries; surfaces for any future cipher-width / cluster-clarity sensitivity that wants to factor license-class exposure.
- **Star-lord** — no engine-side impact; ADR-004 satisfied via elrond-side MIGRATION.md v1.6 only.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + handoff-brief + schema spec + manifest extension + AGENT_STATE update. Sequences drax v1.21+ at lowest VS2a polish priority; sequences future elrond v1.12 schema-execution dispatch when convenient.
- **Matt** — Tier 5.1 + Tier 5.2 lock satisfied at the curation seam; no further upstream action needed for this loop.

### What downstream consumers need to do

**Drax (v1.21+ when fired):**

1. Download 28 game-icons.net icons (SIL-1.1; zero spend) per handoff brief § 1.3 role mapping.
2. Apply `PROP_RENDER_SCALE_OVERRIDE = 0.75` multiplier per handoff brief § 2.1.
3. Append 8 new prop descriptors to `STATIC_PROP_DESCS` per handoff brief § 2.3.
4. Extend `dungeonPropsForRoom()` to per-room-size variable density per handoff brief § 2.2.
5. Deploy verbatim `credits.txt` text per handoff brief § 3.1.
6. Acceptance criteria per handoff brief § 5; out-of-scope guards per § 6.

**Star-lord:** no action.

**Gandalf:** schema additions enable license-class + usage-recommendation queries when next abstraction-analysis pass benefits.

**Legolas:** future Mode B crawls may populate `usage_recommendation` per-row optionally; persona.md addition not in scope for this dispatch.

### Schema diff or example before/after

**catalogue.db schema:** NO CHANGE EXECUTED IN THIS DISPATCH. v1.1 schema columns hold. v1.6 spec is authored and approved but execution is deferred to a future elrond v1.12 dispatch (per `catalogue-db-schema-v2-2026-05-18.md` § 7).

**catalogue.db data:** NO CHANGE. v1.5 data state (3 sources / 3 packs / 48 assets / 461 tags / 1 session) holds.

**Curated-layer artifacts:**

| Artifact | Before | After |
|---|---|---|
| `ambient-props-subset-vs2a-2026-05-17.jsonl` row count | 26 (1 meta + 25 rows) | **35** (1 meta + 25 rows + **1 addendum-meta + 8 new rows**) |
| `catalogue-db-schema-v2-2026-05-18.md` | did not exist | **NEW** — spec for `usage_recommendation` + `license_class` columns + indexes + v1.6 schema_meta row |
| `tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` | did not exist | **NEW** — consolidated 4-deliverable brief (icons + props + credits + schema cross-ref) |
| `MIGRATION.md` | v1.5 latest | **v1.6 entry appended** |

**Schema-spec-only mutations (NOT yet applied to catalogue.db):**

| Aspect | Spec'd v1.6 | Execution |
|---|---|---|
| New column `usage_recommendation TEXT NULL CHECK (...)` on `catalogue_assets` | spec'd | deferred to elrond v1.12 |
| New column `license_class TEXT NULL CHECK (...)` on `catalogue_assets` | spec'd | deferred to elrond v1.12 |
| Partial indexes on new columns | spec'd | deferred |
| `schema_meta` v1.6 row | spec'd | deferred |
| Migration script `v1_6_usage_recommendation_license_class.sql` | NOT yet authored (spec-only) | future dispatch |

### Tier 5.1 / 5.2 Matt-lock satisfaction record

| Tier 5.1 lock | Satisfied by |
|---|---|
| Game-icons.net (SIL-1.1) | Handoff brief § 1 (role mapping for 28 icons + license posture + on-disk placement spec) |
| Consistent prop scale | Handoff brief § 2.1 (`PROP_RENDER_SCALE_OVERRIDE = 0.75` per gandalf v1.7 canon) |
| Medium decoration density | Handoff brief § 2.2 (4-6-8 per-room-size density rules + within-room uniqueness) |
| Single credits.txt | Handoff brief § 3.1 (complete verbatim file content for drax deployment) |

| Tier 5.2 lock | Satisfied by |
|---|---|
| Defer mega-pack-02 | No mega-pack-02 work in this dispatch; pass-through |
| Rubber-stamp HD-cinematic | Pass-through (no elrond surface) |
| Approve catalogue-DB additive schema | Schema spec authored at `catalogue-db-schema-v2-2026-05-18.md`; v1.6 design-locked, execution deferred |

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** Matt L3 2026-05-18 explicit approval of additive schema. v1.6 spec is within scope.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. Engine telemetry untouched.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`). No drax/demo/loadout code touched. No tag push.
- **ADR-007 (survey-mode):** handoff brief separates "what to wire" from "what NOT to wire" (§ 6 out-of-scope guards explicit).

### Files changed

- `agentic_orchestration/research/curated/catalogue-db-schema-v2-2026-05-18.md` (NEW)
- `agentic_orchestration/research/curated/tier-5-1-5-2-drax-v1.21-handoff-brief-2026-05-18.md` (NEW)
- `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` (EXTENDED — 26 → 35 lines)
- `agentic_orchestration/research/curated/MIGRATION.md` (THIS FILE — v1.6 entry)
- `agentic_orchestration/research/curated/AGENT_STATE.md` (UPDATED — Pattern A Tier 5.1/5.2 completion record)

### Files intentionally NOT changed

- `agentic_orchestration/research/curated/catalogue.db` — schema execution deferred per § Schema diff
- `agentic_orchestration/research/scripts/catalogue_migrations/v1_6_*.sql` — migration script NOT yet authored (future dispatch)
- `reincarnated-demo/public/credits.txt` — drax v1.21+ seam (this dispatch authors text only)
- `reincarnated-demo/src/visuals/ambientPropsExtension.ts` — drax v1.21+ seam
- `reincarnated-demo/src/visuals/gameIcons.ts` — drax v1.21+ seam (new module)
- Other curated artifacts (`dungeon-objects-quality-audit-2026-05-18.md` etc.) — unchanged

### Reversibility

Spec-only mutation:
- Three new docs (`catalogue-db-schema-v2-*`, `tier-5-1-5-2-drax-v1.21-handoff-brief-*`, MIGRATION.md v1.6 entry) — revertible by `rm` + git-reset
- Manifest extension (`ambient-props-subset-vs2a-2026-05-17.jsonl`) — revertible by `head -n 26` (the addendum-meta + 8 rows are contiguous at the file tail)
- No catalogue.db mutation in this dispatch; no DB backup needed.

### Out-of-scope follow-ons (for knight-rider sequencing)

1. **elrond v1.12 — execute v1.6 schema migration** — author `v1_6_usage_recommendation_license_class.sql`; apply to catalogue.db; create pre-v1.6 backup. Estimated 30-45 min.
2. **elrond v1.13 — back-fill existing 48 rows with `usage_recommendation` + `license_class`** — single curator pass over the corpus. Estimated 1-2 hours.
3. **drax v1.21+ — wire-in per handoff brief** — Tier 5.1 surfaces (icons + props + credits.txt). Estimated 2-3 hours when sequenced.
4. **legolas persona.md extension** — optional addition of `usage_recommendation` field to Mode B crawl output schema. Knight-rider sequences.
5. **future curation passes consume `license_class`** — credits.txt generator script (research/scripts/) when corpus crosses ~100 attribution surfaces and hand-curation becomes brittle.

### Tag

`elrond/v1.11-tier-5-1-5-2-final-curation-1` (local; no push per ADR-006)

---

## v1.5 — Pattern A: Pixogen catalogue loop closure (HOLD → APPROVED-WITH-ATTRIBUTION) — 2026-05-16

### What changed (one line)

Pixogen vendor row inserted into `catalogue_sources` (data migration v1.2 against schema v1.1; no schema change); curated JSONL `pixogen-catalogue-curated-2026-05-16.jsonl` filed with HOLD-to-APPROVED-WITH-ATTRIBUTION flag transitions for both Full and Lite SKUs; pricing/access metadata corrected (Full €19.99 paid not-yet-acquired; Lite €0 acquired); attribution-required flag carried per AFGameAssets license § 3.A.1.

### Why (one line)

Closes Pixogen Path-A loop per Matt license-file verification 2026-05-16 (downloaded Lite pack; read 18kB AFGameAssets license) + drax v0.19 Void Shield demo wiring with attribution credit. Prior state: legolas Mode B raw extraction carried `license_unverified: true` + `consumption_hold: HOLD`; cipher-width-inclusion analysis excluded Pixogen; pivot-insurance-ledger flagged Pixogen as SPOF for technology-vfx substrate. Verification cleared HOLD; substrate-evidence may now re-include Pixogen (separate downstream re-analysis dispatch).

### Who's affected

- **Drax** — Pixogen Void Shield wired v0.19 (already done; this dispatch attests upstream catalogue state). Future Pixogen-asset consumption: query `catalogue_sources WHERE source='itch-pixogen'` returns vendor row with `default_license='commercial-royalty-free'` + notes carrying `attribution_required` clause. Per-pack/per-asset rows NOT yet curated in catalogue.db (out of scope for this dispatch); the curated JSONL serves as interim reference for the two SKUs.
- **Legolas** — PARALLEL dispatch updates `pixogen/findings-summary-2026-05-16.md` with verified `license_terms_verbatim` (license file full text). Coordinate via this MIGRATION.md timestamp (2026-05-17T02:11:09Z, the catalogue.db schema_meta v1.2 applied_at). Legolas's raw extraction file at `catalogue/pixogen/full-2026-05-16.jsonl` is INTENTIONALLY UNTOUCHED by this dispatch per ownership-boundary discipline — raw extraction is a snapshot artifact; curated state lives in `curated/pixogen-catalogue-curated-2026-05-16.jsonl`.
- **Gandalf** — Pixogen substrate evidence (void-spatial + technology-vfx) is now re-includable in any future cipher-width / cluster-clarity sensitivity analysis. Pivot-insurance-ledger line 136 + cross-vendor substrate inventory still carry HOLD-era exclusion language; UPDATE NOT MADE in this dispatch (downstream document update is a separate gandalf-or-elrond sequencing call). Reversal-path documented in pivot-insurance-ledger line 145 is now ACTIVATED — when next emergent-grouping analysis is run, Pixogen rows can be re-included.
- **Star-lord** — no engine-side impact; ADR-004 satisfied via elrond-side MIGRATION.md v1.5 only. No cross-DB ATTACH pattern changes.
- **Rocket** — unaffected.
- **Knight-rider** — Pixogen Path-A loop CLOSED; consumption is APPROVED-WITH-ATTRIBUTION per AFGameAssets license § 3.A.1. Sequences any follow-on Pixogen pack-curation dispatches (Lite per-animation curation; Full acquisition decision; void/technology re-inclusion in cipher-width analysis).
- **Matt** — license verification action complete; no further upstream action needed for this loop. Full pack (€19.99) acquisition is a future commission decision; flagged in vendor notes.

### What downstream consumers need to do

**Drax:**
1. Continue Void Shield consumption per v0.19. When sourcing additional Pixogen assets, ensure attribution credit is maintained in demo + loadout per AFGameAssets license § 3.A.1.
2. If consuming additional Lite animations (Water/Fire/Wind/Holy/Electric/Fireworks/Explosions), reference `curated/pixogen-catalogue-curated-2026-05-16.jsonl` for asset metadata until per-pack catalogue_assets curation lands.

**Star-lord:** no action.

**Gandalf:**
1. When commissioning next cipher-width or cluster-clarity sensitivity pass, request Pixogen re-inclusion. Substrate-evidence weights change: void-spatial gains a confirming row (n=2 with CraftPix Black Hole already present); technology-vfx becomes attested (n=1; Pixogen-exclusive).
2. Consider sequencing a `pivot-insurance-ledger.md` + `cross-vendor-substrate-inventory-2026-05-16.jsonl` HOLD-language refresh dispatch (elrond can author once gandalf signals timing).

**Legolas:** author parallel `pixogen/findings-summary-2026-05-16.md` update populating `license_terms_verbatim` from license file inspection. Timestamp coordination via this v1.5 entry. Raw extraction file (`catalogue/pixogen/full-2026-05-16.jsonl`) remains untouched per legolas ownership.

### Schema diff or example before/after

**catalogue.db schema:** NO CHANGE (v1.1 holds). This is a DATA migration only.

**catalogue.db data:**

| Aspect | Before (v1.4 / data migration v1.1 applied) | After (v1.5 / data migration v1.2 applied) |
|---|---|---|
| `catalogue_sources` rows | 2 (itch-pimen, craftpix) | 3 (**+itch-pixogen** — individual-creator, hand-drawn-pixel, commercial-royalty-free, register_mixed=0) |
| `catalogue_packs` rows | 3 (pimen) | 3 (**no change** — Pixogen pack curation out of scope per dispatch) |
| `catalogue_assets` rows | 48 (pimen) | 48 (**no change** — Pixogen asset curation out of scope per dispatch) |
| `schema_meta` rows | 2 (v1.0, v1.1) | 3 (**+v1.2** data-migration entry) |
| `pixogen-catalogue-curated-2026-05-16.jsonl` | did not exist | **NEW** — 2 rows (Full + Lite) with HOLD-cleared flag state |

**Curated JSONL flag transitions (per row):**

| Field | Before (legolas raw extraction) | After (elrond curated) |
|---|---|---|
| `license_unverified` | `true` | `false` |
| `consumption_hold` | (implicit HOLD; HOLD literal in legolas findings-summary) | `APPROVED-WITH-ATTRIBUTION` |
| `license_verified_date` | (absent) | `2026-05-16` |
| `license_verified_by` | (absent) | `matt` |
| `license_verification_method` | (absent) | `lite-pack-download-license-file-inspection` (Full) / `lite-pack-download-license-file-direct-inspection` (Lite) |
| `attribution_required` | (absent) | `true` |
| `attribution_recipient` | (absent) | `Pixogen / AFGameAssets / Antoine Fauville` |
| `cost_currency` | (absent for Full; absent for Lite) | `EUR` (Full) / `EUR` (Lite, €0) |
| `cost_usd_approx` | (absent) | `21.59` (Full) / `0.0` (Lite) |
| `cost_acquired_by_project` | (absent) | `false` (Full) / `true` (Lite) |
| `cost_acquired_note` | (absent) | corrected pricing/access metadata (Full not-yet-acquired; Lite acquired) |
| `c2_license_flag` | `true` | `false` |
| `c2_license_outcome` | "LICENSE UNVERIFIED..." | "CLEARED 2026-05-16 — License verified clean..." |
| `license` | `proprietary-pending-verification` | `commercial-royalty-free` |
| `license_terms_verbatim` | "License of AFGameAssets — terms in downloadable 18 kB file; NOT publicly readable..." | "AFGameAssets license (Antoine Fauville) — distributed as 18kB file with each pack. Verified terms: commercial use permitted; modification permitted; Pixi.js runtime tinting permitted per § 2.A.4; attribution REQUIRED per § 3.A.1. (Full verbatim license text held by legolas in pixogen findings-summary update; this row carries verified-status flags only.)" |

**Sequencing note on `license_terms_verbatim`:** elrond carries the abbreviated verified-state summary in the curated jsonl; legolas (parallel dispatch) authors the full verbatim license text in `pixogen/findings-summary-2026-05-16.md`. This split mirrors the ownership boundary: legolas's findings-summary is the canonical full-text reference; elrond's curated jsonl carries operational state. If both touch this field on the same row at the same time, MIGRATION.md timestamps (2026-05-17T02:11:09Z for elrond) are the conflict-resolution reference.

### Pricing/access correction (dispatch item 3)

Prior catalogue metadata referenced "Pixogen Lite free version" framing — Matt clarified the actual structure:

| SKU | Cost | Acquisition path | Project acquisition state |
|---|---|---|---|
| Pixel Art RPG VFX (Full Pack) | **€19.99** | itch.io direct purchase OR Mega Pack (€59.99) | **NOT YET ACQUIRED** (future commission decision) |
| Pixel Art RPG VFX Lite | **€0** | itch.io separate download | **ACQUIRED 2026-05-16** (Matt download; license verification vector) |

The Lite is **not a free version of the Full** — it is a separate standalone free download with a reduced category set (8 categories vs Full's 11). Categories missing from Lite: Technology, Attack Slash, Ice. This distinction is now captured in vendor `notes` + per-SKU `cost_acquired_note` fields.

### Files changed

- `agentic_orchestration/research/curated/catalogue.db` (mutated — schema_meta v1.2 row + catalogue_sources itch-pixogen row inserted)
- `agentic_orchestration/research/curated/catalogue.db.pre-pixogen-2026-05-16-backup` (NEW — pre-migration safety snapshot; ~1 week soft-retention)
- `agentic_orchestration/research/curated/pixogen-catalogue-curated-2026-05-16.jsonl` (NEW — 2 rows; verified-state flag transitions)
- `agentic_orchestration/research/scripts/catalogue_migrations/v1_2_pixogen_vendor_insert.sql` (NEW — idempotent? NO — INSERT with no ON CONFLICT clause; re-run will fail on UNIQUE constraint, which is the intended replay safety)
- `agentic_orchestration/research/curated/MIGRATION.md` (THIS FILE — v1.5 entry)
- `agentic_orchestration/research/curated/AGENT_STATE.md` (UPDATED — Pattern A Pixogen dispatch completion)

### Files intentionally NOT changed

- `agentic_orchestration/research/catalogue/pixogen/full-2026-05-16.jsonl` (legolas's raw extraction; ownership boundary — untouched)
- `agentic_orchestration/research/catalogue/pixogen/findings-summary-2026-05-16.md` (legolas parallel dispatch updates `license_terms_verbatim`)
- `agentic_orchestration/research/catalogue/pixogen/geometry-signatures-2026-05-16.jsonl` (geometry signatures unchanged by license verification)
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (carries HOLD-era exclusion language; refresh deferred per dispatch scope — separate gandalf-sequencing call)
- `agentic_orchestration/research/curated/pivot-insurance-ledger.md` (carries HOLD-era exclusion language at line 136 + reversal-path at line 145; refresh deferred per dispatch scope)
- `agentic_orchestration/research/curated/cipher-width-inclusion-flags-2026-05-16.jsonl` (Pixogen-exclusion flags from HOLD era; refresh deferred per dispatch scope)
- `agentic_orchestration/research/curated/post-step-b-cleanup-2026-05-16.md` (HOLD-era operational state record; historical artifact, not updated)

### Out-of-scope follow-ons (for knight-rider sequencing)

1. **Pixogen Lite per-pack curation** — 8 Lite animations × catalogue_packs row + 8 catalogue_assets rows; requires curator visual inspection of frames. Estimated: 1-2 hours.
2. **Pixogen Full acquisition decision** — Matt + knight-rider; €19.99 purchase OR Mega Pack at €59.99. Substrate-coverage argument (technology-vfx is Pixogen-exclusive) may motivate.
3. **Cipher-width / cluster-clarity sensitivity re-run with Pixogen re-included** — elrond dispatch; substrate-evidence weights will shift (void-spatial gains confirming row; technology-vfx becomes attested).
4. **HOLD-era language refresh in downstream documents** — pivot-insurance-ledger line 136 + line 145, cross-vendor substrate inventory Pixogen-exclusion blocks, cipher-width inclusion flags. Combined elrond dispatch; estimated 1 hour.
5. **Decisions-log entry** — knight-rider sequences; codifies Pixogen license-verification + first-vendor-consumption pattern (vendor onboarding playbook precedent).

### Reversibility

Pure data INSERT into `catalogue_sources`. Reverse via:
```sql
DELETE FROM catalogue_sources WHERE source='itch-pixogen';
DELETE FROM schema_meta WHERE version='1.2';
```
Safe while no downstream `catalogue_packs` / `catalogue_assets` rows reference `itch-pixogen` (FK constraints block deletion once downstream rows land). Curated jsonl is a flat file; `rm` reverses. Backup at `catalogue.db.pre-pixogen-2026-05-16-backup` is canonical pre-migration snapshot.

---

## v1.4 — Pattern A combined: bundle-pipeline follow-up + register-mixed schema amendment — 2026-05-16

### What changed (one line)

Schema bumped to v1.1 (per-vendor `register_mixed` convenience flag + per-product `deliverable_register` field per Drift-13 / Pattern P8 prescription (d)); CraftPix vendor record added as canonical first cross-register instance; three curation amendments landed on Pimen rows in response to drax bundle-pipeline follow-on items (slug-collision disambiguation hints, new bundle-internal-only Icons sub-pack curated, explosion-effect matcher-correction tags).

### Why (one line)

Closes the Pattern A dispatch ("yes to all 7" Matt-authorization 2026-05-16, decisions #2 + #5): Track A unblocks drax's bundle-pipeline matcher on the slug-collision case + brings the Icons sub-pack into the catalogue + corrects an explosion-VFX misread; Track B operationalizes the Drift-13 / Pattern P8 (d) prevention prescription at the catalogue-db schema layer, with CraftPix as the canonical first cross-register vendor.

### Who's affected

- **Drax** — bundle-pipeline matcher can now consult `bundle-folder-hint:*` tags + `subpack-organization-style:*` tags + `_amendment_2026_05_16_bundle_folder_hint` JSON overlay to resolve the slug-collision case + the per-animation-subfolders style-B case. Existing matcher logic continues to work for the simple slug↔folder cases; the new hints are advisory upgrades. Schema additions (`deliverable_register`, `register_mixed`) consumed at downstream filtering time — drax cross-register safety query in §5.5 of catalogue-schema.md applies once schema doc is amended.
- **Legolas** — Track B's per-product `deliverable_register` field aligns with persona-rule extension landed today (`legolas.md` line 34). Future Mode B catalogue dispatches populate the field per product line. Pimen rows are NOT retroactively backfilled (Pimen is single-register; `register_mixed=0` holds; field remains NULL for pimen rows, which is valid per CHECK).
- **Gandalf** — Track B closes the Drift-13 / Pattern P8 prevention prescription (d) (downstream-consumption safety net). Track A's Icons curation extends UI/icon coverage for VS2a/VS2b scene composition. CraftPix vendor record is now schema-attestable as cross-register (queryable via `SELECT register_mixed FROM catalogue_sources WHERE source='craftpix';`).
- **Star-lord** — no immediate action; cross-store ATTACH pattern unchanged. The new columns are queryable via standard SQLite ATTACH.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; sequences `catalogue-schema.md` v1.1 doc-update follow-on (schema diff captured here is canonical; the design doc should reflect by next session).

### What downstream consumers need to do

**Drax:**

1. Bundle-pipeline matcher upgrades (recommendations in `pimen-bundle-follow-up-2026-05-16.md` §§ 1, 2, 3):
   - Read `_amendment_2026_05_16_bundle_folder_hint` from `source_metadata_raw` OR scan `asset_style_tags WHERE tag LIKE 'bundle-folder-hint:%'` to disambiguate slug-collision cases.
   - Consult `animations_count` + new `subpack-organization-style:*` tags before classifying folder structure as "sub-packs" vs "per-animation-subfolders."
   - Treat `bundle-internal-only:<bundle_id>` tagged rows as bundle-sourced-only (no standalone-product URL applies).
2. Cross-register-safety query (Track B): when sourcing assets from a vendor with `register_mixed=1`, check `deliverable_register` at the per-row level. CraftPix is the only current `register_mixed=1` vendor; future ones inherit the pattern automatically.
3. The Icons sub-pack row (`source_asset_id='mega-pack-elemental-icons'`) is `quality_flag='deferred'` until visual inspection completes. Default consumption filter (which requires `quality_flag='pass'`) excludes it for now. Use a `quality_flag IN ('pass','deferred')` widened filter if early-prototype UI work needs the icons before inspection lands.

**Star-lord:** no action. The ATTACH pattern in `catalogue-schema.md` §5.1 continues to work; the new columns are additive.

**Gandalf:**

1. Track A Icons curation widens UI/icon coverage. When VS2a/VS2b design surfaces element-identity-rendering needs, the catalogue row provides the canonical reference.
2. Track B's `register_mixed=1` CraftPix row attests the Drift-13 instance in schema. Cross-register-safety queries are now expressible — useful for any future register-validation pass against the catalogue.

**Legolas:** no action. Future Mode B crawls populate `deliverable_register` per persona-rule extension; the field is OPTIONAL/NULL-allowed so persona compliance is checked at curation, not at extraction.

### Schema diff or example before/after

**catalogue.db schema:**

| Aspect | Before (v1.0) | After (v1.1) |
|---|---|---|
| `catalogue_sources` columns | 7 (source, display_name, url, vendor_type, primary_register_hint, default_license, notes, added_at) | **+1**: `register_mixed INTEGER NOT NULL DEFAULT 0 CHECK (register_mixed IN (0,1))` |
| `catalogue_assets` columns | 37 (see v1_0_initial.sql) | **+1**: `deliverable_register TEXT NULL CHECK (deliverable_register IN ('pixel-art-raster', 'vector-ai', 'vector-eps', 'vector-svg', 'hand-drawn-pixel', 'painterly-raster', 'photographic', 'audio', 'font', 'mixed', 'not-applicable', 'unknown'))` |
| Indexes | 9 on catalogue_assets | **+1**: `idx_catalogue_assets_deliverable_register` (partial, WHERE NOT NULL) |
| `catalogue_sources` rows | 1 (itch-pimen) | 2 (itch-pimen `register_mixed=0`, craftpix `register_mixed=1`) |
| `catalogue_assets` rows | 47 | 48 (Track A item 2 added `mega-pack-elemental-icons`) |
| `asset_style_tags` rows | 444 | 461 (+4 bundle-folder-hint amendments + 11 icon tags + 2 explosion matcher-correction) |
| Schema version | 1.0 | 1.1 |

**Track A non-schema mutations:**

- 2 `catalogue_assets` rows had `source_metadata_raw` JSON amended in-place via additive overlay key `_amendment_2026_05_16_bundle_folder_hint` (the existing `_curation_overlay_2026_05_16` key preserved untouched). Append-only intent: this is an additive metadata layer, not a curation supersession.
- 1 row had matcher-correction tags appended without metadata mutation (`explosion-effect`).
- 1 new row inserted (`mega-pack-elemental-icons` — bundle-internal-only sub-pack).

**JSONL snapshot:**

- `pimen-catalogue-curated-2026-05-16.jsonl`: 47 → 48 rows (icon row appended; 2 rows updated in-place with amendment overlay; 1 row updated in-place with 2 new tags).

### Track A — bundle-pipeline follow-up summary

| Item | Drax surface | Elrond resolution |
|---|---|---|
| Slug collision (`Earth Spell 03` vs `Earth Effect 03`) | Both fuzzy-match `earth-spell-effect-03`; ambiguous | Same pack in 2 formats inside bundle. Canonical = `Earth Spell 03`; fallback = `Earth Effect 03`. Amendment overlay + 4 bundle-folder-hint tags added. |
| Icons sub-pack out-of-band | Not curated; inspect + decide | INCLUDED — 10 PNGs (5 elements × 2 variants); curated as `mega-pack-elemental-icons` with `bundle-internal-only` flag; quality_flag=deferred + manual_review_queued=1 |
| 30 explosion VFX out-of-band | Inspect + recommend subset OR all-out-of-band | MISIDENTIFIED — they ARE the 30 animations of curated `explosion-effect`. 2 matcher-correction tags added; no new curation. |

Full detail: `agentic_orchestration/research/curated/pimen-bundle-follow-up-2026-05-16.md`.

### Track B — schema amendment summary

Per Drift-13 / Pattern P8 prescription (d) (`canonical/story/drift-audit.md`), the catalogue.db schema now exposes register-mixedness at two layers:

1. **Per-product (source-of-truth)** — `catalogue_assets.deliverable_register TEXT NULL` with closed CHECK enum capturing observed vendor-shipping-register vocabulary (`pixel-art-raster`, `vector-ai`, `vector-eps`, `vector-svg`, `hand-drawn-pixel`, `painterly-raster`, `photographic`, `audio`, `font`, `mixed`, `not-applicable`, `unknown`). Populated per-row by curators at curation time. NULL allowed because single-register vendors (where the vendor row's `register_mixed=0` holds) don't require per-row inspection.
2. **Per-vendor (convenience aggregate)** — `catalogue_sources.register_mixed INTEGER NOT NULL DEFAULT 0 CHECK (register_mixed IN (0,1))`. Set to 1 when any product carries a register different from `primary_register_hint`. Downstream consumers can quickly filter cross-register vendors without scanning per-product rows.

CraftPix added as canonical first instance:
```
source='craftpix', vendor_type='aggregator-marketplace',
primary_register_hint='mixed', default_license='mixed', register_mixed=1,
notes='Cross-register vendor (Drift-13 / Pattern P8 canonical first instance). ...'
```

Distinction from existing `derived_register`:
- `derived_register` (v1.0): curator's inferred VISUAL register from six-axis rubric (hand-drawn-pixel / retro-16bit / clean-vector / painterly-raster / anime-cel / manual-review). Output of rule cascade.
- `deliverable_register` (v1.1): vendor's SHIPPING register as delivered per product (PNG/PSD pixel-art / AI vector / EPS vector / etc.). Source-of-truth for cross-register routing.
- Both overlap on happy path; diverge when vendor mislabels OR ships rare formats OR delivers mixed in one product. The two columns together let consumers reason about both visual-register-fit AND shipping-format-fit.

### Pre-migration backup

`agentic_orchestration/research/curated/catalogue.db.pre-v1.1-backup` — byte-identical snapshot of catalogue.db before v1.1 migration applied. Retain until v1.1 has been consumed by drax + gandalf in downstream work, then prune at next housekeeping pass (suggest: 1-week soft-retention).

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** Matt authorized 2026-05-16 ("yes to all 7" — decisions #2 + #5). Schema migration v1.1 applied within authorization scope.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement for both Track A (data mutations) + Track B (schema mutation). No engine-telemetry or other-seam schema changed. Drax-side response (matcher updates) is drax-internal; no companion MIGRATION required unless drax declares it.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`, `research/scripts/*`, `catalogue.db`). No engine-side mutation. The pre-v1.1 backup is an additional safety layer (not required by ADR but elected here given schema migration is the rarer operation).
- **ADR-007 (survey-mode):** the bundle-follow-up findings doc reports what exists (inspection findings, decisions, action taken) without interleaving prescriptive content beyond the explicit "Recommendation to drax" subsections.

### Verification

```
$ python3 agentic_orchestration/research/scripts/amend_pimen_bundle_folder_hints_2026_05_16.py
[jsonl] {'total_rows': 47, 'amended': 2}
[db]    {'db_updates': 2, 'tags_inserted': 4, 'tags_already_present': 0}

$ python3 agentic_orchestration/research/scripts/curate_pimen_elemental_icons_2026_05_16.py
[db] {'inserted': 1, 'asset_uid': 48, 'tags_inserted': 11}
[jsonl] appended row for mega-pack-elemental-icons

$ sqlite3 catalogue.db < agentic_orchestration/research/scripts/catalogue_migrations/v1_1_register_mixed_flag.sql
(no output — transaction committed cleanly)

$ sqlite3 catalogue.db "SELECT version, applied_at FROM schema_meta ORDER BY applied_at;"
1.0|2026-05-16T04:14:38Z
1.1|2026-05-17T00:29:04Z

$ sqlite3 catalogue.db "SELECT source, vendor_type, primary_register_hint, register_mixed FROM catalogue_sources;"
itch-pimen|individual-creator|hand-drawn-pixel|0
craftpix|aggregator-marketplace|mixed|1

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_assets;"
48

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM asset_style_tags;"
461

$ sqlite3 catalogue.db "INSERT INTO catalogue_sources (source, display_name, url, vendor_type, primary_register_hint, default_license, notes, added_at, register_mixed) VALUES ('test', 'test', 'http://x', 'individual-creator', 'unknown', 'unknown', 't', 't', 2);"
Error: stepping, CHECK constraint failed: register_mixed IN (0, 1)   ← CHECK enforced

$ sqlite3 catalogue.db "UPDATE catalogue_assets SET deliverable_register='BOGUS-VALUE' WHERE asset_uid=1;"
Error: stepping, CHECK constraint failed: deliverable_register IN (...)   ← CHECK enforced
```

Schema v1.1 holds under empirical 48-row pressure with all CHECK constraints enforced. The 47 existing v1.0 rows are preserved (no back-fill required; `deliverable_register=NULL` is valid).

### Open follow-ons (NOT elrond-blocking)

1. **catalogue-schema.md v1.1 doc update** — design doc should be amended to reflect: § 3.2 (`register_mixed` column on catalogue_sources), § 3.4 (`deliverable_register` column on catalogue_assets), § 4 (deliverable_register enum value-set table parallel to license taxonomy), § 5 (new worked-example query for cross-register-safety). Knight-rider sequences — small doc update; ~30 min effort.
2. **CraftPix vendor curation crawl** — Legolas Mode B dispatch to populate the 7 known CraftPix products (5 pixel-art-raster VFX + 2 vector-ai character; per `craftpix/full-2026-05-16.jsonl`) into catalogue.db, with per-product `deliverable_register` populated per persona-rule extension. Not in this dispatch's scope; queued for future activation.
3. **Drax bundle-pipeline matcher updates** — per recommendations in `pimen-bundle-follow-up-2026-05-16.md` §§ 1.recommendation, 2.recommendation, 3.recommendation. Drax-side implementation; knight-rider sequences if drax wants a focused matcher-improvement dispatch.
4. **Backfill `subpack_organization_style` + `bundle_folder_hint` at next curation pipeline pass** — both surfaced as amendment-time additions in this dispatch. Next pipeline pass (per v1.3 open follow-on #2) should promote to first-class curation-time fields.
5. **Visual-inspection queue grew to 23 rows** (was 22 in catalogue.db post-v1.3 — minor discrepancy with v1.3 curation-log's "21" claim worth noting; the 22-vs-21 delta predates this dispatch and is not investigated here). Icons sub-pack added at MEDIUM priority (bundle-internal; no incremental acquisition decision).
6. **Pre-v1.1 backup pruning** — `catalogue.db.pre-v1.1-backup` retained until next housekeeping pass (~1 week soft-retention).
7. **Generalization of `bundle-internal-only` operational pattern** — this is the first instance. Future bundle-inspections should reuse the `bundle_internal_only: true` + `bundle-internal-only:<bundle_id>` tag pair. Eventually candidate for first-class schema field if the pattern recurs.

---

## v1.3 — First live curation pass (Pimen full-catalogue, 47 rows) — 2026-05-16

### What changed (one line)

First end-to-end live application of the v1.0 catalogue schema: Pimen full-crawl raw extraction (46 rows) → curated rows (47 after category split) → ingest into `catalogue.db`; the four dispatch pre-processor rules + CC-BY tagging + bundle relationships + category split all landed without schema rework.

### Why (one line)

Closes the `2026-05-16-elrond-pimen-full-catalogue-curation` dispatch; first empirical validation that the v1.0 schema + rubric R5 cascade + curator-tagging conventions hold under live-data pressure; produces the first queryable catalogue dataset available to drax/star-lord/gandalf via the cross-store ATTACH pattern.

### Who's affected

- **Drax** — can now query `catalogue.db` for Pimen consumption (see `catalogue-schema.md` § 5.3 worked example). **Caveat:** outline-profile secondary tags (`outline-profile:hard-1px` vs `outline-profile:soft-or-variable`) are NOT yet populated for any Pimen row because `linework_style` is universally `unknown` until post-acquisition visual inspection — scene-coherence filter on outline-profile cannot constrain Pimen rows at this curation pass.
- **Gandalf** — viability-gate design-track queries are now executable against real Pimen data. Sample-time threshold (>20% `license = 'unknown'`) cleared trivially (0% unknown in Pimen).
- **Star-lord** — no immediate action; cross-store ATTACH pattern unchanged.
- **Legolas** — Pimen Mode B extraction format passed curation with 0 extraction errors. The format is operationally correct for downstream consumption; future Pimen crawls or other vendor crawls can use this as the reference shape.
- **Rocket** — unaffected.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; sequences post-acquisition visual-inspection follow-on when Matt makes acquisition decisions on the 21 visual-inspection-queued rows.

### What downstream consumers need to do

**Drax:** query patterns per `catalogue-schema.md` § 5.3 work today. Constraining queries by outline-profile is currently a no-op for Pimen — flag for awareness. The locked-register query (`derived_register = 'hand-drawn-pixel'` + `license IN (commercial-OK set)` + `embodiment_tag != 'pending-amendment'` + `superseded_at IS NULL`) returns 27 rows; `quality_flag = 'pass'` filter is currently 0 (post-acquisition inspection promotes to `pass`).

**Star-lord:** no action.

**Gandalf:** when Pimen-acquisition decisions surface, design-track read of the queue's 21 visual-inspection rows is a candidate input. No active dispatch.

**Legolas:** Mode B format works. Future crawls can use this Pimen pass as the reference for "what shape elrond's curation accepts cleanly."

### Schema diff or example before/after

**Before:** `catalogue.db` empty (v1.0 schema applied but no data). `archive/` populated with retired stores (research.db + Yomi snapshot).

**After:**

```
catalogue.db
├── schema_meta            : 1 row (v1.0)
├── catalogue_sources      : 1 row  (itch-pimen)
├── crawl_sessions         : 1 row  (legolas-pimen-mode-b-full-2026-05-16)
├── catalogue_packs        : 3 rows (mega-pack-01, mega-pack-02, earth-spell-effect-03)
├── catalogue_assets       : 47 rows
├── asset_style_tags       : 444 rows (328 legolas-inferred + 116 elrond-curated)
├── catalogue_rejections   : 0 rows
└── abstraction_groupings  : 0 rows (stub)
```

**New files under `research/curated/`:**

- `pimen-catalogue-curated-2026-05-16.jsonl` (47 lines, JSON Lines format; one curated row per line)
- `pimen-bundle-relationships-2026-05-16.json` (2 bundles registered)
- `pimen-curation-log-2026-05-16.md` (full per-row decisions, queue disposition, schema verification)
- `pimen-full-catalogue-snapshot-2026-05-16-rows-only.txt` (auxiliary diagnostic — not committed)

**New file under `research/scripts/`:**

- `curate_pimen_full_2026_05_16.py` (one-shot curation tool; ~470 lines; stdlib only)

### Pre-processor rules applied (per dispatch)

1. **R5 derivation cascade** — `style_register: "pixel-art"` parent value resolves to one of `hand-drawn-pixel` (28), `retro-16bit` (2), or `manual-review` (17). Cascade prioritizes positive style_tags (`hand-drawn-pixel`, `retro` + band-coherence) over Legolas-flagged uncertainty (`sub-register-uncertain`). One vendor-hint-inferred case (`fantasy-skeleton-enemies`).
2. **`pimen_element` → source_metadata_raw + queryable tag** — 23 of 46 raw rows had non-null pimen_element; emitted as `asset_style_tags.tag = 'pimen-element:<value>'`. Vendor-namespaced prefix generalizes to future crawls.
3. **`file_format` prose parser** — closed-enum cascade with vendor-heuristic fallback for pimen's RAR-only strings; aseprite-negation guard ("No Aseprite files" correctly classified as `has_aseprite_source = false`). 25 `png-spritesheet` + 22 `png`.
4. **`requires_visual_inspection` flag** — 21 of 47 curated rows (20 `resolution_band = unknown` raw rows + 1 inherited by the split sister); queryable via `asset_style_tags.tag = 'requires-visual-inspection'` + `manual_review_queued = 1`.

### Operational decisions captured (curation log § 6)

- **Visual-inspection queue Option (b)** — 21 rows filed as sub-list with priority guidance (4 paid rows = HIGH, 16 free rows = MEDIUM, 1 split sister = HIGH, 2 mega-packs = LOW per constituent-coverage); deferred to a later inspection step paired with Matt's acquisition decision.
- **CC-BY 4.0 attribution** — 2 rows (`pixel-battle-effects`, `cutting-and-healing`) tagged via curation_attribution overlay + 3 queryable tags (`attribution-required`, `attribution-acquired-yet:false`, `license-specifics:cc-by-4.0`).
- **Bundle relationships** — both external JSON file + inline `in-bundle:<bundle_id>` tags (redundancy + queryability). Bundle-01 = 9 constituents ($34.21 sum, $12.75 sale = 63% discount); bundle-02 = 5 constituents (3 overlap with bundle-01 + 2 new) ($24.95 sum, $20.40 sale = 18% discount). Version-drift caveat surfaced (mega-02 may ship different versions of overlap rows).
- **Category split** (`earth-spell-effect-03`) — 1 row → 2 rows (vfx + enemy sister), shared `pack_id`. Sister tagged `embodiment_tag = 'pending-amendment'` with hint `'elemental humanoid form'` (per the narrative-layer amendment protocol).

### Pipeline rules NOT applied (deferred — curation log § 7)

- R6 outline-profile secondary tag (linework_style universally unknown until post-acquisition inspection)
- R7 boundary-cluster borderline default (no rows trigger R7 in this corpus)
- Pivot-insurance ledger format finalization (single-vendor data not yet pivot-meaningful)
- Standing `manual-review-queue.md` and `pipeline-runs.md` (deferred until first multi-pass cycle)

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** no schema change in this pass; v1.0 lock holds.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. No engine-telemetry or other-seam schema changed.
- **ADR-006 (external system writes require authorization):** writes confined to elrond-owned paths (`research/curated/*`, `research/scripts/*`, `catalogue.db`). No engine-side mutation.
- **ADR-007 (survey-mode):** the curation log reports what exists (47 curated rows, decisions per row); separates "what is" (§§ 1-5) from "what's queued" (§ 2 visual-inspection) from "what's deferred" (§ 7).

### Verification

```
$ python3 agentic_orchestration/research/scripts/curate_pimen_full_2026_05_16.py
[load] 46 raw rows from full-2026-05-16.jsonl
[curate] 47 rows after category split
[write] .../pimen-catalogue-curated-2026-05-16.jsonl
[write] .../pimen-bundle-relationships-2026-05-16.json
[ingest] {'assets_inserted': 47, 'tags_inserted': 444, 'packs_registered': 3}
[summary] derived_register: {'manual-review': 17, 'hand-drawn-pixel': 28, 'retro-16bit': 2}
[summary] quality_flag:     {'deferred': 17, 'unreviewed': 29, 'borderline': 1}
[summary] license:          {'commercial-royalty-free': 45, 'CC-BY': 2}

$ sqlite3 catalogue.db "SELECT COUNT(*) FROM catalogue_assets;"
47

$ sqlite3 catalogue.db "SELECT version FROM schema_meta;"
1.0
```

Schema v1.0 holds under empirical 47-row pressure with 0 CHECK-constraint failures.

### Open follow-ons (NOT elrond-blocking)

1. **Visual-inspection queue drain** — 21 rows queued in catalogue.db (`manual_review_queued = 1`). Paired with Matt's acquisition decision moment, OR knight-rider sequences as separate dispatch. ~2 min per asset.
2. **Curation-pipeline generalization** — this pass is one-shot for Pimen. Future vendor crawls (CraftPix, CreativeKind) want a generalized `curate_catalogue.py` per `curation-pipeline.md` § 10. Estimated 1-2 days when the second-vendor crawl lands.
3. **Pivot-insurance ledger format finalization** — deferred until a second-register vendor (e.g., a retro-16bit source) lands. Pimen-only is pivot-meaningless.
4. **`embodiment-narrative-layer.md` cross-reference for `elemental` form** — gandalf-owned. Pressure low (one row); will accumulate.
5. **Post-acquisition visual-inspection workflow** — single-batch session per acquired pack, backfills axes 2-4 + finalizes resolution_band + clears manual_review_queued + promotes quality_flag from `unreviewed` to `pass`/`borderline`/`fail`.

---

## v1.2 — Yomi (season_002328) archive (Dispatch B Option 3) — 2026-05-16

### What changed (one line)

Archived `reincarnated-loadout/data/season_002328/` (Yomi season — 10 classes + manifest + gear_pool, 556 KB total) into elrond's `archive/yomi-season_002328-2026-05-13/` for four-deep redundancy on design-vocabulary-bearing data, complementing the loadout remote push (Option 2) earlier same session.

### Why (one line)

Closes the residual Yomi-specific redundancy gap surfaced by the provenance audit (`yomi-provenance-audit-2026-05-16.md`); applies the same four-deep redundancy standard the research.db retirement established to a second category of historical/design data; gives gandalf / drax / engine pipeline a stable file-system referent for Yomi independent of loadout app evolution.

### Who's affected

- **Gandalf** — Yomi remains a stable referent for design vocabulary (Lantern-Keeper, Pomegranate, miasma/lantern/brine/bone elements) even if the loadout app data evolves.
- **Drax** — no immediate action; the loadout app continues consuming `reincarnated-loadout/data/season_002328/` as before. The archive is a parallel copy, not a redirected source.
- **Star-lord** — the c1f02ca deterministic-replay fragility is documented in the provenance audit § 7 + this archive's companion markdown. Knight-rider sequences the engine-side note on `export/MIGRATION.md`.
- **Knight-rider** — receives this MIGRATION entry + archive completion notification; may draft a decisions-log entry codifying the side-seed-archive-on-import discipline if Matt wants it as a standing rule.

### What downstream consumers need to do

**No required action.** The archive is a redundancy layer, not a redirected source. Existing consumers continue reading from their existing paths:

- Loadout app: continues consuming `reincarnated-loadout/data/season_002328/` (working tree of loadout repo)
- Design docs in `canonical/story/`: continue prose-level references to Yomi (no path change)
- Engine pipeline: if/when Yomi is ever needed engine-side, either re-generate from seed=2328 (lossy — produces A Yomi, not THIS Yomi) or read THIS Yomi from the elrond archive

### Schema diff or example before/after

**Before:** `archive/` directory contained the research.db retirement archive only.

**After:**

```
agentic_orchestration/research/curated/archive/
├── research-db-2026-05-07.db                          (existing — research.db binary)
├── research-db-narrative-archive-2026-05-16.md        (existing — narrative archive)
├── yomi-season_002328-2026-05-13/                     (NEW — Yomi season data tree)
│   ├── manifest.json
│   ├── gear_pool.json
│   └── classes/class_0001.json ... class_0010.json
└── yomi-season_002328-2026-05-13.md                   (NEW — companion archive doc)
```

### Convention extension (v1.2)

The v1.1 archive convention established `archive/<store>-<as-of-date>.db` for SQLite binary preservation. v1.2 extends to directory-tree archives:

- **Filename pattern (directory tree):** `archive/<store>-<as-of-date>/` (no extension) + companion markdown `archive/<store>-<as-of-date>.md`
- **Filename pattern (SQLite binary):** `archive/<store>-<as-of-date>.db` (as v1.1) + companion markdown `archive/<store>-narrative-archive-<archive-date>.md`
- **`.gitignore` exception:** `!archive/*.db` (v1.1) covers binary case; directory-tree archives are not affected by `*.db` rule so no additional exception needed
- **Companion markdown required** in both cases — captures provenance, integrity hashes, status footer

### Cross-seam ADR compliance

- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. No engine-telemetry or other-seam schema changed.
- **ADR-006 (external system writes require authorization):** the source `cp -r` is a read from loadout (permitted) + write to elrond seam (permitted, within own domain). No destructive ops on the source — loadout `data/season_002328/` is unmodified.
- **ADR-007 (survey-mode):** the companion markdown reports what exists (manifest values, class roster, integrity hashes) without interleaving prescriptive content.

### Verification

```
$ find archive/yomi-season_002328-2026-05-13 -type f | wc -l
12

$ diff <(find loadout/data/season_002328 -type f -exec shasum -a 256 {} \; | sort)
       <(find archive/yomi-season_002328-2026-05-13 -type f -exec shasum -a 256 {} \; | sort)
# (no output — byte-identical)

$ du -sh archive/yomi-season_002328-2026-05-13/
556K
```

### Housekeeping in same pass

- Removed WAL/SHM siblings (`research-db-2026-05-07.db-shm`, `-wal`) that had been auto-created on the research-db archive during my earlier SQL verification queries. They were operational noise, not canonical archive content. Post-removal, the research-db archive .db SHA-256 unchanged (`3846b98b…f96351e`).

### Open follow-ons (NOT elrond-blocking)

1. **Knight-rider decisions-log entry (optional)** — codifies side-seed-archive-on-import as standing discipline, if Matt wants it as a rule.
2. **Star-lord note** on `reincarnated-engine/src/reincarnated/export/MIGRATION.md` re: the c1f02ca deterministic-replay's silent assumption on `seasons/<id>/gear/catalog.json` persistence (the fragility that bit Yomi). Knight-rider sequences.
3. **Audit § 3.6 update** — points at the provenance audit + this archive. Folded into this pass.

---

## v1.1 — Archive directory + research.db retirement (Phase-1 cleanup, COMPLETE on elrond side) — 2026-05-16

### What changed (one line)

Added `archive/` subdirectory for durable historical SQLite snapshots; archived dormant `reincarnated-engine/research.db` (binary + narrative markdown); audit § 3.4 updated; Matt-authorized destructive removal of research.db + WAL/SHM siblings + empty engine-root telemetry.db executed 2026-05-16.

### Why (one line)

Closes the 2026-05-07 decisions-log deferral on research.db consolidation (Phase-1 cleanup per data-architecture audit § 7); establishes the `archive/` pattern for future historical preservation of retired data stores.

### Who's affected

- **Star-lord** — `scripts/db.py` and `scripts/capture-regression-baseline.py` still reference research.db; updates flow through knight-rider per ADR-004. Recommended one-liner for star-lord's MIGRATION.md captured in archive markdown § E.
- **Knight-rider** — drafts decisions-log entry per dispatch A item 3 ("research.db deprecation: archived to research/curated/archive/, removed from repo. Supersedes 2026-05-07 deferral").
- **All agents** — future references to research.db content should point at the archive markdown or binary snapshot, not the engine-repo path.
- **Elrond (self)** — `.gitignore` now contains `!archive/*.db` exception permitting intentional historical snapshots; future archived DBs follow the `archive/<store>-<as-of-date>.db` filename pattern.

### What downstream consumers need to do

**Star-lord:** at next session, remove research.db references from `scripts/db.py` (DB_PATH, init banner, docstring) and `scripts/capture-regression-baseline.py` (copy step, schema dump step, docstring listing). The script-level refactor is small (~10-line cleanup); a star-lord-side MIGRATION.md entry should accompany.

**Knight-rider:** draft decisions-log entry; sequence star-lord script cleanup.

**Other agents:** when referencing research.db content historically, link to `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` (or the binary snapshot for structural recovery).

### Schema diff or example before/after

**Before:** No `archive/` directory under `research/curated/`. `reincarnated-engine/research.db` was the sole copy of the early-May Phase-0 research data.

**After:**

```
agentic_orchestration/research/curated/
├── archive/                                          (NEW directory)
│   ├── research-db-2026-05-07.db                     (NEW — binary snapshot, 2.6 MB)
│   └── research-db-narrative-archive-2026-05-16.md   (NEW — verbatim narrative + structural inventory)
├── .gitignore                                        (UPDATED — !archive/*.db exception added)
└── (existing files unchanged)
```

`reincarnated-engine/research.db` — UNCHANGED at archive time. PENDING Matt's `rm` authorization per ADR-006.

### Archive convention (new pattern established v1.1)

- **Path:** `agentic_orchestration/research/curated/archive/<store>-<as-of-date>.<ext>`
- **Companion markdown:** `archive/<store>-narrative-archive-<archive-date>.md` (provenance header, narrative content verbatim, structural-table schemas + counts, integrity hash, status section)
- **`.gitignore` rule:** `!archive/*.db` (intentional preservation; archives are durable historical records, not runtime DBs)
- **Integrity:** SHA-256 captured in companion markdown at archive time

### Cross-seam ADR compliance

- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry fulfills the elrond-side requirement. Star-lord-side MIGRATION.md update is the cross-seam companion (knight-rider sequences with star-lord).
- **ADR-006 (external system writes require authorization):** the binary copy `cp research.db → archive/research-db-2026-05-07.db` is a read-from-engine + write-to-elrond-domain operation. The read is permitted; the write lands in elrond's owned path. The destructive `rm` on engine-side is held at the authorization gate.
- **ADR-007 (survey-mode):** the audit-update subsection § 3.4.1 reports what exists and what is pending; does not interleave "should" statements with descriptive findings.

### Verification

```
$ ls /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/archive/
research-db-2026-05-07.db
research-db-narrative-archive-2026-05-16.md

$ shasum -a 256 .../archive/research-db-2026-05-07.db
3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e

$ sqlite3 .../archive/research-db-2026-05-07.db ".tables"
   (returns the same 11-table inventory as the source)
```

### Destructive-op completion log (Matt-authorized 2026-05-16, ADR-006)

Authorization scope: explicit per-statement go-ahead on the four-file removal window. Executed by elrond, 2026-05-16:

```
rm /Users/admin/Games/reincarnated-engine/research.db        ✓ removed
rm /Users/admin/Games/reincarnated-engine/research.db-wal    ✓ removed
rm /Users/admin/Games/reincarnated-engine/research.db-shm    ✓ removed
rm /Users/admin/Games/reincarnated-engine/telemetry.db       ✓ removed (the empty 0 B root-of-repo orphan from audit § 3.1; bundled into the same authorization window)
```

Post-rm verification:
- All four file paths return "No such file or directory"
- `data/telemetry.db` (15.7 GB canonical telemetry) UNTOUCHED
- `git -C reincarnated-engine status --short` reports no new untracked artifacts (all four were `.gitignore`d; removal does not perturb git state)
- Archive at `agentic_orchestration/research/curated/archive/research-db-2026-05-07.db` remains the canonical historical record

### Open follow-ons (still pending — not elrond-blocking)

1. **Star-lord script cleanup** (scripts/db.py, scripts/capture-regression-baseline.py) — knight-rider sequences. Engine-side MIGRATION.md update accompanies. ~10-line cleanup.
2. **Knight-rider decisions-log entry** — closes the 2026-05-07 deferral.

---

## v1.0 — Initial catalogue schema lock — 2026-05-16

### What changed (one line)

Initial catalogue database schema and six-axis style register rubric locked v1.0 post-gandalf dialogue.

### Why (one line)

Operationalizes the locked HD-2D-pixel style register (`canonical/story/style-register.md`) into curator-checkable axes + DB schema, unblocking Legolas Pimen Mode B sample dispatch and downstream catalogue work.

### Who's affected

- **Legolas** — Mode B catalogue output now has a defined target schema. Pimen sample dispatch can proceed (was held pending this work).
- **Gandalf** — viability-gate design-track now has a queryable catalogue (once curated) for sample review.
- **Drax** — eventual consumption-time filter consumer; no immediate action.
- **Star-lord** — no immediate action; cross-store ATTACH-read-only pattern documented in `catalogue-schema.md` § 5.
- **Knight-rider** — receives this MIGRATION + dispatch-completion notification; draft decisions-log entry for the rubric lock per gandalf's commission item 5 + ADR-002 (cross-seam schema = Matt approval).

### What downstream consumers need to do

**Legolas:** continue Mode B output in JSON Lines per `~/.claude/agents/legolas.md` spec. Output is consumed by elrond curation script (forthcoming) which maps to catalogue.db. No schema changes Legolas-side.

**Gandalf:** at viability-gate sample-time, use queries in `catalogue-schema.md` § 5 (the default consumption filter and the form-bias case study) for design-track review. Strengthened sample threshold: >20% `license = 'unknown'` fails design track on data-hygiene grounds.

**Drax:** when first sample is curated and a downstream consumption need arises, query catalogue.db via the patterns in `catalogue-schema.md` § 5.3. The default filter includes `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` constraint per scene — see `catalogue-rubric-schema.md` § 3.1.

**Star-lord:** no action. ATTACH-read-only pattern documented for future cross-store work.

### Schema diff or example before/after

**Before:** No catalogue.db. The curated/ directory contained only the data-architecture audit doc.

**After:** Five new design docs + one new DB file:

```
agentic_orchestration/research/curated/
├── data-architecture-audit-2026-05-16.md   (existing)
├── AGENT_STATE.md                          (existing — updated)
├── catalogue-rubric-schema.md              (NEW — six-axis rubric, locked v1.0)
├── catalogue-schema.md                     (NEW — DB schema, locked v1.0 design)
├── curator-tagging-guide.md                (NEW — per-axis curator instructions)
├── catalogue-rubric-validation-2026-05-16.md (NEW — validation pass on empirical vendors)
├── curation-pipeline.md                    (NEW — operational flow)
├── pivot-insurance-ledger.md               (NEW — pivot-insurance monitoring stub)
├── MIGRATION.md                            (NEW — this file)
└── catalogue.db                            (NEW — empty SQLite; gitignored)

agentic_orchestration/research/scripts/
└── catalogue_migrations/
    └── v1_0_initial.sql                    (NEW — migration script for the schema)

agentic_orchestration/research/curated/.gitignore
└── catalogue.db, *.db-wal, *.db-shm        (NEW — gitignore for SQLite files)
```

### Key design decisions baked in this v1.0 lock

Per post-dialogue lock with gandalf (full record in `catalogue-rubric-schema.md` § 9):

1. **Six-axis rubric** — five mechanically-checkable axes + one rule-derived. Closed enum value sets for two-curator convergence. Reasonable boundary cases captured in rules R6 (CreativeKind hard-outlined hand-drawn-pixel) and R7 (Foozle higher-tier boundary cluster with `quality_flag = 'borderline'` default).
2. **Per-asset granularity, not per-pack or per-vendor.** Schema tags each asset on all six axes. Pack-level `pack_register_consistency` is advisory only.
3. **Outline-profile secondary tag** auto-applied by curation pipeline on R6 outputs. Scene-level consumption filters constrain to one outline-profile (`hard-1px` vs `soft-or-variable`).
4. **Embodiment taxonomy v1.0** — eight starter forms (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant) + `not-applicable` + `unknown` + `pending-amendment` (with `pending_amendment_hint` for curator-recorded form-read). New embodiments enter via narrative-layer amendment, NOT by pre-loading the catalogue.
5. **License taxonomy v1.0** — `commercial-license` split into four narrower values; `itch-standard` dropped (curators must read actual license); `unknown` license at >20% of sample fails viability-gate design track.
6. **Pivot-insurance ledger** — curation pipeline emits monitoring summary at each run, tracking per-register / per-embodiment coverage to surface silent pivot-insurance erosion.
7. **Curator-override threshold** — overrides exceeding 10% of corpus or clustering >5 on a single rule clause surface as rule-bug to elrond.
8. **`gandalf-call` reserved for register-genuinely-ambiguous cases**, not curator-vs-rule disagreements (those use `override`).

### Migration script

Schema applied to empty catalogue.db via `agentic_orchestration/research/scripts/catalogue_migrations/v1_0_initial.sql`. Reproducible — re-running on an empty DB produces the same schema.

### Verification

`sqlite3 agentic_orchestration/research/curated/catalogue.db .schema` produces the v1.0 schema as documented in `catalogue-schema.md` § 3.

`SELECT * FROM schema_meta;` returns the v1.0 row:
```
1.0|2026-05-16T<applied_at>Z|Initial catalogue schema; six-axis style rubric v1.0; embodiment tag aligned to embodiment-narrative-layer.md v1.0|catalogue_migrations/v1_0_initial.sql
```

### Cross-seam ADR compliance

- **ADR-002 (cross-seam schema = Matt approval):** the schema is **design-locked v1.0 but pending Matt approval** before live application to the project's curation workflow. The empty DB has been created in this dispatch to validate the schema applies cleanly; production use awaits Matt's go-ahead.
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this file fulfills the requirement. star-lord-side telemetry MIGRATION.md is unaffected (no engine-telemetry change in this work).
- **ADR-006 (external system writes require authorization):** the empty catalogue.db file creation is a one-time elrond-domain operation in elrond's owned path; no engine telemetry or other seam DB was touched.

### Drax wiring-track flag responses (resolved in v1.0)

Per drax's wiring-track review at `agentic_orchestration/qa/findings/2026-05-16-drax-elrond-schema-wiring-review.md` (verdict: PASS WITH FLAGS):

- **Flag 1 — `file_format` underspecified for sprite-sheet consumption.** RESOLVED IN v1.0. Added CHECK constraint with closed enum to `catalogue_assets.file_format`: `'png'`, `'png-spritesheet'`, `'aseprite'`, `'svg'`, `'gif'`, `'jpg'`, `'mp4'`, `'webm'`, `'json-atlas'`, `'tmx'`, `'wav'`, `'mp3'`, `'ogg'`, `'ttf'`, `'otf'`, `'other'`, `'unknown'`. Curators cannot diverge on format strings; demo wiring can rely on enum-stable values. Smoke-tested: `INSERT ... file_format = 'BOGUS-FORMAT'` rejected by CHECK; `'png-spritesheet'` succeeds.

- **Flag 2 — Confidence threshold convention for loadout tag display.** DEFERRED. Per drax's own recommendation ("low priority; defer to drax S1 dispatch"). When catalogue tags surface in the loadout app UI, drax authors the rendering convention. No schema change.

- **Flag 3 — `'itch-standard'` still in `catalogue_sources.default_license` CHECK + `catalogue_packs.pack_license` CHECK.** RESOLVED IN v1.0. The migration SQL (v1_0_initial.sql) had already dropped `'itch-standard'` from both — gandalf dialogue Topic 5 outcome was applied consistently. The catalogue-schema.md design doc had a stale earlier-draft reference in two places; both updated. Smoke-tested: `INSERT INTO catalogue_sources VALUES (..., default_license='itch-standard', ...)` rejected by CHECK.

### Open follow-ons (not blocking the lock)

1. **`embodiment-narrative-layer.md` cross-reference update** — gandalf to author a cross-reference acknowledging the catalogue's `pending-amendment` pattern as the schema-side companion to the narrative-layer amendment protocol. Elrond surfaces this to knight-rider; not done unilaterally (gandalf owns that doc).
2. **Knight-rider decisions-log entry** — per gandalf's commission item 5 + ADR-002, the rubric lock + cross-seam schema needs decisions-log capture. Knight-rider drafts when this dispatch is acknowledged.
3. **Legolas Pimen sample dispatch release** — was held pending this rubric lock. Now unblocked. Knight-rider sequences release at convenient time.
4. **Curation script implementation** — `research/scripts/curate_catalogue.py` (per `curation-pipeline.md` § Tool). Implementation deferred until first Legolas sample lands (no point implementing curator pipeline before there's data to curate).
5. **Form-bias gap-fill consideration** — validation pass surfaces thin coverage in `hand-drawn-pixel` for slime / swarm / plant / dragonling / construct / spirit embodiments. Form-bias work (doc 37 § 4) should sequence either targeted Legolas commissions, LLM image generation, or deferred non-humanoid coverage. Surfaced as input, not blocked.

---

## 2026-06-13 — FACTION_LOOKUP_TABLE Q10 redraw populated (schema_version 1.0 -> 1.1)

**Dispatch:** `agentic_orchestration/dispatches/2026-06-13-elrond-q10-faction-lookup-table-redraw.md` (Gate-1 PASS).
**Owned data layer:** `reincarnated-engine/data/identity/faction_lookup_table.json` (elrond owns `records[]` content; rocket owns the loader `src/reincarnated/generation/identity_sampling.py`).
**Builder script (reproducible):** `agentic_orchestration/research/scripts/build_faction_lookup_table_q10_2026_06_13.py` — re-run to regenerate the table verbatim.

### What changed
- `records[]` populated from empty stub to **637 records** (one exact `(lineage, period, register)` entry per non-void cell the sampler can produce).
- `schema_version` bumped `1.0 -> 1.1` (content population; NO schema-shape change — the record key contract `{lineage, period, register, faction}` is rocket's existing loader contract, confirmed unchanged before authoring).
- Added a `factions[]` roster field (9 factions) for legibility; void_override_* fields preserved verbatim from the stub.

### Q10 redraw (Matt-ratified 2026-06-12; executed 2026-06-13)
8 redrawn faction homes + 1 composite ninth. Faction is **lineage-anchored** per Session 2 § 7.2 (cultural lineage is the primary key; period/register are secondary descriptors):

| Faction | Lineage(s) homed |
|---|---|
| Iron Covenant | western_european_germanic |
| Shadow Courts | western_european_gothic |
| Rune-Clans | norse_germanic_celtic |
| Bronze Sanctum | greek_roman |
| Sunfire Dominion | middle_eastern_persian, north_african_egyptian |
| Eternal Dynasties | east_asian_chinese, east_asian_japanese, east_asian_korean |
| Forge Republics | pan_industrial |
| **Solar Pantheon (composite ninth)** | mesoamerican, sub_saharan_african, south_southeast_asian |
| Void Covenant (override, not in records) | void_liminal lineage + cosmic_horror/void_arcane registers |

**Why a composite ninth (Solar Pantheon) was needed, not absorption:** the three formerly-homeless lineages are cosmologically distinct from each other AND from the existing eight; the Q10 ruling itself rejects absorbing them (e.g. obsidian-priest -> Sunfire Dominion by tie-break). They share one real, non-token thread — divine-kingship + ancestral pantheons + sun/serpent cosmology rendered in stone and bronze, outside the Euro-Sinitic-MENA axes. Solar Pantheon is a real home with mythological / high_fantasy / primal_shamanic register coherence.

### Loader contract confirmation (cross-seam discipline — done BEFORE authoring)
Read rocket's `derive_faction` / `FactionTable` in `identity_sampling.py`. Contract: exact index on `(lineage, period, register)`; Void override fires FIRST (before records); nearest-match score `register*4 + lineage*2 + period*1`. **Satisfiable with content alone — no loader shape change needed.** Did NOT touch rocket's loader.

- `void_liminal` lineage + `cosmic_horror`/`void_arcane` registers are **intentionally absent** from records (consumed by the Void Covenant override before record lookup). Emitting them would be dead cells.

### Empirical check (Q10 acceptance — nearest-match never reached by construction)
Exercised rocket's real loader (`load_faction_table` + `derive_faction`) over the full 14×7×9 = **882-cell** sampler space:
- exact: **637** | override (Void): **245** | nearest: **0** | unassigned: **0**
- distinct factions produced: **9** (all 8 record-factions + Void Covenant)
- **0 nearest-match cells, 0 UNASSIGNED** — no lineage routes through fallback by construction. rocket's nearest-match logging is the standing empirical proof.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. Loader-contract confirmation logged; no engine-telemetry change; star-lord-side MIGRATION.md unaffected.
- **Cross-seam contract change?** No — content population of an existing schema shape; rocket's loader untouched.
- Push to remote deferred to keystone-close (Matt's gate).

---

## 2026-06-17 — Synty catalogue multi-axis tagging (synty_catalogue.db 1.0 -> 1.1, ADDITIVE)

**Commission:** `agentic_orchestration/gandalf/requests/2026-06-17-elrond-catalogue-multiaxis-tagging.md` (Q2 gate 1 — gear-spec upstream-wiring decision).
**Owned data layer:** `agentic_orchestration/research/curated/synty_catalogue.db` (separate DB; gitignored/regenerable).
**Tagging script (reproducible):** `agentic_orchestration/research/scripts/tag_synty_multiaxis_2026_06_17.py` — re-run `all` to reproduce verbatim. Idempotent; ADDITIVE only.
**Deliverables:** `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.{jsonl,md}`.

### What changed (ADDITIVE — no destructive change)
- Added 10 nullable columns to `packs` via `ALTER TABLE ADD COLUMN` (zero existing-row rewrites; 62,281 asset rows untouched):
  `register`, `contribution_role`, `contribution_basis`, `time_period_proposed`, `time_period_basis`,
  `cultural_identity_proposed`, `cultural_mode_flag`, `cultural_basis`, `seam`, `tagged_at`.
- Tagged **all 157 pack rows** (156 content collections; Water Guns ships 2 FBX packs) on 5 axes. Zero nulls — every pack routes.
- `synty_catalogue` schema_meta bumped `1.0 -> 1.1`. (Distinct from the sprite-rubric `catalogue.db` schema lineage above — separate DB, separate schema_meta.)

### Axis discipline (substrate-led split — brief §2)
- **Axes 1 (register) + 5 (seam): substrate-GIVEN** — parsed from Synty pack naming + light curation. AUTHORITATIVE.
- **Axis 2 (contribution_role): doc-DERIVED** — gear-spec asset-class × skinned/static split. Every pack routes:
  environment 89 / armor-base-skinned 38 / ui 8 / bestiary 7 / anim 6 / accent-attach-static 6 / weapon-base-static 3.
  The 34 POLYGON armor-base-skinned packs = the consumption-line restyle base (register filter keeps POLYGON; MINI+SIMPLE corpus-retained, set-aside).
- **Axes 3 (time_period) + 4 (cultural_identity): substrate-VOTED — PROPOSALS ONLY.** The DB holds elrond's proposed
  stratum + a `*_basis` evidence column (the name-token the proposal rests on); the MD deliverable carries rep examples
  per stratum. **gandalf curates the final semantic label at a rep-audit** (semantic-layer rep-audit discipline #25 — substrate
  vote binds at the geometry layer, NOT the semantic layer). Period/culture-agnostic packs (animation, ui, weapon-only, FX,
  seasonal, animal, generic-interior) carry `unresolved` — intentionally NOT hand-labeled; flagged for gandalf.
- `cultural_mode_flag` guards the Mode A/B/C/D collapse: A=geographic-origin, B=cultural-tradition, C=naming-allusion
  (NOT a real culture — e.g. dwarven/elven/sci-fi), D=metadata/no-cultural-read.

### Density-map findings (the gap-fill routing surface — brief §3)
- **Finding 1 (headline):** POLYGON sci-fi humanoid skinned-character coverage EXISTS (~110 chars: Sci-Fi City 40, Space 52,
  Cyber City 18). Brief premise ("only SIMPLE-Space-Characters") REFUTED by substrate. sci-fi-body does NOT require full
  gap-fill. UPDATES prior-canon "sci-fi = zero coverage, deferred v1.1+" entry.
- **Finding 2:** cultural coverage is ASYMMETRIC by layer — Egypt (0 chars / 28 weapons), Vikings (0-1 chars / 215 weapons),
  Samurai-Empire, Goblin, Knights ship rich environment+weapon but HOLLOW skinned-character base → character gap-fill forced.
- **Finding 3:** ZERO-coverage cultural registers (full image-to-3D/Sidekick route): Mesoamerican/Aztec, Indo-Asian,
  Persian/MENA, Sub-Saharan African — all 0 packs. Matches `canonical/48` non-Euro-Sinitic roster homes.
- **Finding 4:** Victorian-steampunk = 0 packs; industrial thin (WWI map + Trains only).
- **Finding 5:** Sidekick Character Creator (157753) is the gap-fill MECHANISM, not a content pack (correctly absent from 157 DB rows).
  WAVE-2 extracted packs contribute the accent silhouette-breaker layer; WAVE-1 FBX packs the skinned-armor bases.

### ADR compliance
- **ADR-004 (MIGRATION.md for cross-seam handoff):** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected.
- **Cross-seam contract change?** No — additive tagging on elrond-owned synty_catalogue.db; no consumer-contract reshape.
  Axes 3+4 are PROPOSALS pending gandalf rep-audit curation (Tier-2 escalation, NOT elrond-decided).
- **Reversibility (schema principle):** raw asset classification preserved; contribution_role routing corrects above the
  upstream SK_Veh_/SK_Bld_ false-positive without rewriting asset rows. Re-runnable from script.
- Push to remote deferred to KR's gate (Matt authorization).

---

## 2026-07-15 — feasibility register v1.1 + atlas.json ghost_field + census re-crawl ingest (elrond)

**Context:** Matt-ratified Q30a (feasibility-cut amendments) + Q30b (taste slate: ZERO cuts). gandalf audit
`gandalf/design-inputs/2026-07-15-feasibility-register-audit-and-taste-slate.md`. Three tasks: regenerate the
feasibility-cuts register as v1.1 under the ratified amendments; emit the ghost_field into atlas.json (charter §4);
ingest the legolas census re-crawl (`legolas/research/census-recrawl-2026-07-14/findings.jsonl`, commit c906a039).

### corpus.db writes (elrond-owned; legolas PROPOSED, elrond JUDGED — all writes elrond's)
- **12 death_class verdicts** -> `canon_corpus.death_class` (enum-trigger validated each). ALL 12 ACCEPTED as proposed
  (evidence trails precise; each distinguishes intrinsic-structural from extrinsic-tuning correctly). Weakest =
  `tq-calculated-strike` (med conf, 1-in-4 cadence borderline-tuning) — accepted: near-zero between-proc contribution
  is a structural design property, not a magnitude dial. No downgrades. Closes "unknown-pending-recrawl" (the 12
  supplementary corpses; anticipated by the Edition-I freeze).
- **32 tranche-1 mech_note recoveries** -> `canon_corpus.mech_note` (replaced 140-char mobile-harvest truncations).
- **9 active control×none kits** -> `canon_engine_key.ctrl_treatment` control->damage (+ cell_key treatment slot rebuilt).
  JUDGMENT (differs from a naive "assign a function" reading): the 9 carry DoT-damage ailments (burn/bleed/poison/
  ignite/shock/electrify) that are NOT in the register's control-function vocabulary. Assigning a fabricated control
  function would violate no-silent-transformation. HONEST RESOLUTION = treatment re-classification (these ARE damage
  kits); resolves the L1′ incoherence at its root; all 9 now light a coherent damage×none meso cell. Result: 0 kits
  remain control×none; 0 function-unassignable-for-lighting.
- **2 corpse geometry re-keys** (`d2-leap-attack-barb`, `poe1-charged-dash`): `geometry_value`/`geo_raw` blank->dash_attack,
  `geometry_rule_fired='elrond-2026-07-15-corpse-movement-verb-rekey'`. **corpus.db ONLY, Edition-II-bound — NO Edition-I
  point re-projected.** (`d4-blade-shift` verified: geo_raw='single', no engine-key row, died extrinsic-itemization ->
  correctly left as-is, NOT sealed by RED-3′.)
- **`atlas_feasibility_cuts_2026_07_14` + `atlas_feasibility_ladder_2026_07_14`** analysis tables refreshed under v1.1
  amendments (DROP+CREATE; gitignored, elrond-owned).

### Register v1.1 artifacts (new; v1 retained in git as lineage)
- `atlas/feasibility-cuts-register-v1.1.{md,csv,json}` — regenerated by `scripts/feasibility_cuts_register_2026_07_14.py`
  (amended: L1′ only {control,hybrid}×none incoherent — damage×function coherent; L4″ only PROJECTILE×melee cut —
  BEAM & ORBITAL spared; RED-3′ tempo conjunct dropped. Slips fixed: T5 meso composed-on-survivors, §2 prose
  "post-logical survivors". Taste slate RULED-KEEP, zero cuts, recorded as lineage.)
- Numbers reproduce gandalf's independent derivation EXACTLY: post-logical **740,139,120** · post-red-law
  **693,146,160** · meso feasible **10,080** · sealed **1,260** (L1′-composed 756 + L2-composed 504).

### atlas.json ghost_field block (charter §4) — additive; byte-identity preserved
- **Emitter extended minimally:** `scripts/build_atlas_json_edition1.py` (star-lord-built) imports the new
  `scripts/ghost_field_edition1.py` (elrond) and appends one `ghost_field` top-level key. No other emitter logic touched.
- **HARD byte-identity regression PROVEN:** `basis` block + `loadings` byte-identical; all 506 points identical EXCEPT
  the 12 supplementary `death_class` label fills (sentinel->verdict; labels ONLY, coordinates NEVER touched);
  `counts.null_death_class_sentineled` 12->0; sole new top-level key = `ghost_field`. Emitter deterministic
  (byte-stable modulo `emitted_at`).
- **ghost_field content:** 10,080 feasible meso cells {core-tuple, x, y, lit, kit_count, depth} + 1,260 SEALED cells
  {core-tuple, cut_id} (L1=756, L2=504). Depth badges delivery-keyed (MELEE/PROJECTILE=55,755; others=74,340;
  Σ=693,146,160 exact). 192 lit cells; 455 kits mapped + 14 unmapped_pending_curation + 0 would-seal = 469.
  RED-3′ seals noted as geometry-drill-in (not meso plane).
- **Frozen-basis discipline (decoupling law — VERIFIED):** the Edition-I MCA fit was computed on PRE-C3 cell_keys; the
  C3 treatment re-key would move dim2 (~1.0) if used for the fit. So the ghost projection reconstructs the frozen fit
  from a durable snapshot `atlas/atlas-frozen-fit-cellkeys-edition1.csv` (pre-C3; verified to reproduce frozen active
  dim1/dim2 to 0.00e+00), while lighting from the LIVE (post-C3) corpus AT EMISSION TIME. Frozen frame, versioned
  occupancy (Edition law §6). New artifact: `atlas/atlas-frozen-fit-cellkeys-edition1.csv` (469 rows).

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. The emitter is a
  collab-side curation artifact (elrond-owned research tree); the ghost_field extension is a minimal additive touch
  on the star-lord-built emitter, logged here per the cross-seam-touch convention.
- **Reversibility:** every corpus.db write is a stated proposed-value ingest; the 9 treatment re-keys preserve the
  original control value in this log + the ingest script; v1 register retained in git. Ghost projection fully
  reproducible from version-controlled artifacts (frozen-fit snapshot + register + pipeline).
- Auto-committed per project discipline (Matt-authorized cycle work). Push deferred to KR's gate.

---

## 2026-07-16 — Refit-Candidate-1 R3-ADDENDUM completion: item A axis-sign alignment **HALTED** (rotated/swapped plane)

**Charge:** `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-refit-addendum-completion-brief.md`
(items A axis-sign alignment · B verbatim EAST-half drill-in · C P-DF-1 · D §10 beyond-horizon census).
**Baseline:** the Tier-3 refit run at commit a087bfbd emitted `atlas-refit-candidate-1.json` (unratified
comparison artifact) WITHOUT drill_in / p_df_1 / hull / census; this charge was to complete that layer.
Item A is FIRST and everything downstream keys on it. **It HALTED. Nothing was emitted; no served or refit
artifact coordinate was changed.**

### Item A finding — the sign is NOT determinable by the reflection-only corr rule
- Brief item A commands RAW same-index correlations (E1-frozen `atlas-coordinates-active.csv` vs
  `refit-candidate-1-coordinates-active.csv`), explicitly NOT Procrustes-transformed. On the 469 shared
  actives:
  - `corr(E1_dim1, refit_dim1)` = **+0.0446** — |corr| **< 0.10** (the brief's stated HALT tripwire fires).
  - `corr(E1_dim2, refit_dim2)` = **+0.4277** — determinable.
- The full RAW 2×2 correlation matrix is **off-diagonal dominant**: `|E1_d1 × refit_d2|` = **0.6697** (large)
  vs the same-index diagonal 0.0446. i.e. **refit_dim2 tracks Edition-I dim1** — the axes are effectively
  **swapped**.
- The optimal orthogonal transform mapping refit→E1 is a **reflection + ~117° rotation** (det(Ω) = **−1.0**).
  The refit plane is ROTATED relative to Edition-I, **not merely sign-flipped**.
- The brief's stated expectation (`dim1 ≈ 0.64, dim2 ≈ 0.27`, "both determinable") is drawn from
  comparison-report **§2, which reports the POST-PROCRUSTES aligned correlations** (proc dim1 = 0.6364,
  proc dim2 = 0.2692 — reproduced exactly). Item A forbids that rotation and commands the RAW frame; in the
  raw frame the axes have **not survived in place**.

### Why HALT (not guess)
A reflection-only sign alignment — the brief's mandated and only-permitted operation ("Pure reflection, never
rotation") — **cannot anchor a rotated/swapped plane.** Flipping refit_dim1's sign would only turn its 0.0446
same-index correlation into −0.0446; its true Edition-I counterpart is refit_dim2. The sign of refit_dim1 is
genuinely undetermined by the corr rule. Per the brief HALT list ("|corr| < 0.10 either dim") + elrond
discipline (no silent transformation; surface what the data says; escalate through knight-rider, never
improvise a transform), item A HALTS.

### Downstream items B/C/D — BLOCKED (not executed)
The region pin "EAST-half (projected x≥0; PERFORM side)" is meaningful **only on an aligned plane** (brief:
"Without this, 'EAST-half x≥0 = PERFORM side' can silently mean the opposite side of the refit plane").
Because the alignment could not be established:
- **B (drill-in fork):** not run — the EAST-half region would land on an un-anchored plane.
- **C (P-DF-1 re-score):** the û construction machinery itself is intact (verified: `geometry/whirlwind` and
  `commit/channel` columns BOTH present in the 628-active refit fit — the verbatim û could run and would NOT
  HALT on vocabulary), but K_max beyond-horizon membership + the "does EAST-half cover the overshoot" verdict
  are frame-relative and un-anchored without A.
- **D (§10 beyond-horizon census):** the coverage verdict vs the EAST-half pin is un-anchored without A. (The
  hull + beyond-horizon-N quantities themselves are reflection/rotation-invariant and CAN be computed
  frame-free; but the brief's §10 requires the coverage-vs-pin verdict, which cannot be stated pre-alignment.)

### What was verified in passing (de-risks the resolution pass)
- **P-DF-1 vocabulary is safe:** the refit fit HAS both û columns (`geometry/whirlwind`, `commit/channel`) —
  the verbatim Edition-III û construction runs against refit loadings without HALT.
- **Drill-in vocabulary delta CONFIRMED (as the brief predicted):** the refit's geometry fit-columns are the
  Edition-III promoted set **plus `aura`** (13 vs 12 levels; `aura` un-fuses at 628, n=8→earns a column).
  Commit fit-columns unchanged (channel, instant, wind-up). So once A is resolved, B's `promoted_geometry_levels`
  gains exactly one level (`aura`) vs Edition-III.

### Resolution needed (gandalf's call at the verify gate — routed via knight-rider)
Two coherent paths, both outside elrond's steward authority to choose (the brief pre-committed to
reflection-only and did not authorize a rotation):
1. **Permit an orthogonal-Procrustes alignment** of the refit plane into Edition-I's frame for the
   region-pinned machinery (rotation, not reflection) — makes "EAST-half = PERFORM side" meaningful in the
   Edition-I sense but departs from the brief's "never rotation" law; OR
2. **Re-pin the drill-in region on the refit's OWN axes** (the refit is its own honest fit; its dim1 is its
   own PERFORM-analog) — keeps within-fit purity but the region is no longer the Edition-I EAST-half, so B/C/D
   become "refit-native drill-in," not a like-for-like comparison against Edition-III's EAST-half.
The census's beyond-horizon quantities (N-beyond-meso-hull, N-beyond-charted-hull, per-direction overshoot)
are frame-invariant and could be emitted independently of the region choice if gandalf wants the numbers
ahead of the ruling.

### Artifacts (this entry)
- `scripts/axis_sign_alignment_refit_candidate_1_2026_07_16.py` — reproducible item-A diagnostic (read-only;
  emits nothing to any artifact). Deterministic; re-run to reproduce every number above.
- **No change** to `atlas-refit-candidate-1.json`, any refit CSV, `atlas-edition3.json`, `atlas.json`, or any
  served/frozen artifact. The refit JSON still lacks drill_in/p_df_1/census (unchanged from a087bfbd) —
  correctly, since the layer keys on the un-resolvable alignment.

### ADR compliance
- **ADR-004:** no engine-telemetry change; star-lord-side MIGRATION.md unaffected. Cross-seam escalation
  (alignment-law ruling) routes to gandalf via knight-rider — elrond has no parallel-escalation privilege and
  does not choose the alignment law.
- **Reversibility:** trivially satisfied — nothing was written to any data artifact; the diagnostic is a pure
  read.
- Auto-committed per project discipline (Matt-authorized charge work). Push deferred to KR's gate.

> **RESOLUTION (2026-07-16):** gandalf ruled at the verify gate (brief "RULING" section, commit 0bc3b9da) — item
> A is AMENDED to **A′**: in-plane orthogonal Procrustes alignment (rotation+reflection, NO scaling, NO
> translation), applied atomically to every plane coordinate, stamped `plane_alignment`. Path 1 of the two above
> (permit orthogonal alignment) was chosen but as a *disclosed presentation transform*, not a fit distortion —
> distances/spreads/congruence/gates/plane-inertia are Q-invariant; only the arbitrary MCA/SVD orientation
> convention rotates, and it is headlined. This HALT record stands as lineage. See the next entry for the A′
> resolution + items B/C/D completion.

---

## 2026-07-16 — Refit-Candidate-1 R3-ADDENDUM RESOLVED: item A′ plane_alignment + drill-in + P-DF-1 + §10 census (elrond)

**Charge:** `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-refit-addendum-completion-brief.md` (AMENDED — the
"RULING at the verify gate" section is the operative law; item A → A′). **Authority:** gandalf verify-gate ruling
(commit 0bc3b9da), following elrond's correct item-A HALT (commit 90f839de). **No engine-telemetry change; no
served-artifact write.** Only refit-candidate artifacts + fork scripts touched.

### Item A′ — in-plane orthogonal Procrustes plane_alignment (replaces the reflection-only axis_sign_alignment)
- **Q** = optimal orthogonal 2×2 map minimizing ‖E1 − refit·Q‖² over the 469 shared actives, computed from the
  CENTERED clouds (orientation-only, translation-free — corr is translation-invariant, so centering isolates the
  pure orientation map; both fits are barycenter-origin per the ruling). **Q = [[−0.459389, −0.888235],
  [−0.888235, 0.459389]]**, **det = −1.0** (reflection component), **rotation_deg = −117.3477**.
- **Diagonal-dominance flip (the ruling's assert + HALT gate):** RAW same-index corr matrix is ANTI-diagonal
  dominant (sum|diag| 0.4723 < sum|anti| 0.7148; largest entry off-diagonal |E1_d1×refit_d2| = 0.6697). POST-Q it
  is DIAGONAL-dominant (sum|diag| 0.9055 > sum|anti| 0.8015; largest entry 0.6364 on the diagonal). Test =
  {sum|diag| > sum|anti|} AND {max-|entry| on-diagonal}. Asserted in the emitter (fail-loud HALT) + the comparison
  script. **Disclosed structural finding:** aligned dim2 tracks E1_dim2 only weakly (0.2692, below its off-diagonal
  0.4003) — the refit's 2nd axis does not survive the ~117° rotation cleanly; reported, not smoothed.
- **Atomic application (one Q, everywhere):** applied to all 665 point coords, every ghost feasible-cell coord, the
  pull/MELEE honest-coord tables, the drill-in (hull + glyph field + S_argmax), P-DF-1 (û = û_raw·Q as a direction;
  S_argmax), and the emitted plane CSVs. S_max/K_max/verdict are Q-INVARIANT (projections onto correspondingly-
  rotated directions); only the emitted coordinate presentation rotates. The `plane_alignment` stamp carries Q,
  det, rotation_deg, raw_corr_before, corr_after, both diagonal-dominance flags, rationale, invariance_note.
- **Single source of Q:** `scripts/axis_sign_alignment_refit_candidate_1_2026_07_16.py` (rewritten item A → A′;
  exposes `compute_Q()`); the emitter + comparison script + ghost module all import the identical Q. Deterministic.

### Item B — EAST-half drill-in fork (refit fit/vocab; ALIGNED coords), region pin VERBATIM
- Region pin verbatim: **"EAST-half (projected x≥0; PERFORM side)"** — applied to the ALIGNED x (meaningful only
  post-alignment). Promoted pair geometry×commit VERBATIM; RED-3 seal law identical (dash_attack × commit≠instant).
- **Vocabulary delta (auto-follows the refit fit):** `promoted_geometry_levels` gains **`aura`** — **13 levels**
  (refit) vs **12** (Edition-III); `aura` un-fuses at 628 (n=8 → earns a fit column). `promoted_commit_levels`
  unchanged (channel, instant, wind-up). n_east_parent_cells = 3312 (aligned EAST side; differs from E3's 5068 —
  the EAST/PERFORM half is defined by the ROTATED x). n_sub_feasible = 122,544; n_sub_sealed = 6624 (= 3312 × 2,
  dash_attack × {channel, wind-up}, all RED-3-). Emitted `ghost_field.drill_in` with the EXACT Edition-III key set
  (17 keys; verified equal, zero missing/extra).

### Item C — P-DF-1 re-score (verbatim û against refit loadings; aligned frame)
- û = normalize(mean(c_whirlwind, c_channel)) VERBATIM — both columns present in the refit fit (verified; no
  vocab HALT). **verdict PASS**: S_max = 1.90823161 > K_max_beyond_horizon = 1.15472813; û (aligned) =
  [0.84378, −0.53669]; n_beyond_horizon_kits = 13. S_argmax lies inside the drill-in reach hull (internal
  consistency: points/loadings/cells/hull all carry the same Q). Emitted `ghost_field.p_df_1` with the EXACT
  Edition-III key set (10 keys; verified equal).

### Item D — §10 beyond-horizon census (appended to refit-candidate-1-comparison-report.md; ALIGNED; ALL 628)
- Hulls computed-not-constant (aligned): meso-only hull 21 vertices; charted hull (meso feasible ∪ drill-in
  sub-feasible reach) 25 vertices. Method reproduces Edition-III's baselines exactly (E3 meso-hull-beyond=14,
  charted-beyond=0 confirmed on the served artifact).
- **N beyond meso-only hull = 13** (Edition-era baseline 14 — that baseline is over E3's 469 in the E3 frame; this
  is all 628 in the aligned refit frame). **N beyond charted hull = 0** (Edition-III baseline 0). Full 13-kit
  beyond-meso list (positions + overshoot + octant + bearing + gateA + franchise) + per-quadrant (EAST-N 9, EAST-S
  4) + per-octant (NE 9, SE 4) breakdown in the report.
- **Coverage verdict:** P-DF-1 PASS is the evidence; ALL 13 beyond-meso overshoot kits are EAST-side (pinned);
  WEST-side overshoot = 0; charted hull contains every active. **Uncovered overshoot directions: NONE** — the
  EAST-half drill-in covers the overshoot; no drill-in-expansion direction is forced by the census (gandalf's call).

### Comparison report re-run (ruling: printed coords must match the aligned artifact)
- §2 rewritten: explicit Q + rotation_deg + det + RAW and POST corr matrices + before/after diagonal-dominance
  (replacing the old scipy-procrustes-with-scaling §2). §§1/4/5/8/9 now print ALIGNED coords. **Report-vs-artifact
  coord max L1 mismatch = 1.13e-07** (same Q, one frame — cross-checked in-script). §1 Procrustes congruence
  (0.4677) / RMS displacement (19.94% diam) are reflection/rotation-invariant — unchanged; gates unchanged (fit-
  structure quantities, not re-run).

### Artifacts (this entry)
- **Scripts (modified):** `scripts/axis_sign_alignment_refit_candidate_1_2026_07_16.py` (A → A′; single source of
  Q), `scripts/ghost_field_refit_candidate_1.py` (+drill_in +p_df_1 +Q-application +plane_alignment stamp),
  `scripts/build_atlas_refit_candidate_1_json.py` (+Q on points, +top-level headline, +aligned CSVs),
  `scripts/refit_candidate_1_comparison_2026_07_16.py` (+§2 rewrite, +§10 census, aligned coords).
- **Artifacts (re-emitted):** `atlas/atlas-refit-candidate-1.json` (now carries drill_in + p_df_1 + plane_alignment;
  all coords aligned; 7.14 MB), `atlas/refit-candidate-1-coordinates.csv` (aligned x,y),
  `atlas/refit-candidate-1-comparison-report.md` (§2 rewrite + §10 census).
- **Artifacts (new):** `atlas/refit-candidate-1-coordinates-active-aligned.csv` (628),
  `atlas/refit-candidate-1-coordinates-supplementary-aligned.csv` (37). The RAW `refit-candidate-1-coordinates-
  active/-supplementary.csv` (dim1..dim17) stay RAW as the reproducible fit record (Q is a plane-only presentation
  transform; rotating dim1/dim2 in place would corrupt higher-dim relations + Q-reproducibility).

### Iron-law + HALT compliance
- **Edition III + every served artifact READ-ONLY:** verified byte-untouched (git status shows only refit artifacts;
  served mtimes unchanged; emitter fail-loud guard on served paths intact). No "Edition IV"/"edition4" anywhere.
- **Lattice byte-identical (v1.3):** feasible 11,160 / sealed 1,314 / depth_sum 767,411,820 asserted (no drift).
- **HALT conditions (none tripped):** û construction ran verbatim; no served write; no lattice drift; post-alignment
  corr IS diagonal-dominant (asserted).
- **ADR-004:** no engine-telemetry change; star-lord-side MIGRATION.md unaffected. **Reversibility:** the refit
  artifacts regenerate deterministically from the fork scripts (SEED 20260714; Q from the two raw CSVs); RAW
  derivation CSVs preserved. Auto-committed per project discipline (Matt-authorized charge). **Push deferred to
  gandalf's gate.**

---
