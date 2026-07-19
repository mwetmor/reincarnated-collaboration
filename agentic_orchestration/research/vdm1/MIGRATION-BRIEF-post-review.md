# VDM-1 — POST-REVIEW MIGRATION BRIEF (elrond execution spec)

> **STATUS:** CURRENT (execution spec, 2026-07-19). Author: gandalf (run steward · SPEC-AUTHOR). Executor: **elrond** (single writer, `research/curated/corpus.db`). **All eleven rulings D-1…D-11 are Matt-ratified** (REVIEW-BOOK.md § 2 + Matt's margins 2026-07-19). This brief translates the rulings into exact DB operations. Nothing here re-opens a ruling.

**Companion authorities (read before executing):** `REVIEW-BOOK.md` § 2/§ 4/§ 5/§ 10 · `errata-ledger.md` (format + last id = ERRATA-55) · `stage5/BLIND-RIDER-DIVERGENCE-REPORT.md` (D-1 anchors) · `2026-07-18-vdm1-crosswalks.md` (element/ailment law).

**Execution law:** ONE migration, one `MIGRATION-vdm1-post-review-<date>.md` doc. **Back up first. Do NOT git-commit** — the steward does the single pathspec commit after an independent read-only verify battery. `corpus.db` is gitignored-local; your git-tracked outputs are the MIGRATION doc, errata-ledger entries, and the regenerated compendium. Work in a transaction where the engine allows; report exactly what changed per item so the verify battery can check each.

---

## 0. BACKUP (first, non-negotiable)

`cp corpus.db corpus.db.pre-review-ratification-<UTC>` + write its md5 sidecar (match the existing `.bak-*.md5.txt` convention). Record pre-migration md5 in the MIGRATION doc.

---

## D-1 — Blind-rider errata (4 kits) → ERRATA-56…59

Apply all four (Matt: "apply all 4"). Each = one `errata-ledger.md` entry (next ids 56→59) **and** the corresponding `kit_mapping` attested-set edit. Anchors are in the blind-rider report § 1–2; cite them.

| ERRATA | kit_id | change | old → new (attested set) | anchor |
|---|---|---|---|---|
| **56** | `d2-avenger` | element **+water** | `{fire,lightning}` → `{fire,lightning,water}` | *"Fire, lightning **and cold** damage are added to each successful attack"* — cold→water (tri-element explicit) |
| **57** | `le-runic-invocation` | element **+fire +water** | `{lightning}` → `{lightning,fire,water}` | outputs *"fire burst, ice storm, lightning fork"* (multi-element) |
| **58** | `d2-ghost-pvp` | element **−shadow** | `{lightning,shadow}` → `{lightning}` | "shadow" = *Shadow Discipline* **tree name** → name-only over-attest under the D4 law (moderate confidence) |
| **59** | `gd-bwc-demolitionist` | ailment **+burn** | `{blind,curse:sap}` → `{blind,curse:sap,burn}` | burning-tar DoT explicitly attested (union, not replace) |

- These are **attestation-set corrections**, not identity changes → **do not re-derive grade** unless the set change crosses a grade boundary (it should not; judge per kit and note if it does).
- Follow standing errata law (D-8.3): ledger is authoritative; set DB `errata_applied` on the touched rows; these promote to `verified-v1.1` as clean post-correction.

---

## D-3 — Mint-all + three-tier evidence stamp (`mint_ledger`)

Matt: **"(a) mint-all, but stamp each qualitative mint with an evidence tier."** Two operations:

**(1) Add two columns** (or your preferred structured equivalent): `evidence_tier TEXT CHECK(evidence_tier IN ('A-attested','B-quantitative','C-provisional'))` + `build_authorized INTEGER` (1/0). Set every mint row `status='matt-ratified'`.

**(2) Stamp the 6 existing candidates AND promote the held accrual families to new rows.** Tier law: **A-attested** = qualitative primitive forced by ≥3 independent kits → `build_authorized=1`. **B-quantitative** = numeric range-extension (not a new primitive), free track → `build_authorized=1`. **C-provisional** = qualitative primitive forced by 1–2 kits → `build_authorized=0`, VDM-2 corroborate-or-drop watch-list.

| mint | class | forcing kits | tier | build_authorized |
|---|---|---|---|---|
| #1 chain fan-out >1.0 | quant | poe1-arc | **B** | 1 |
| #2 stack-parameterizes-geometry | qual | crackling-lance · pizza-sticks · venom-gyre (GRADUATED-3) | **A** | 1 |
| #3 out-and-return path | qual | spectral-throw +5 siblings (6-kit) | **A** | 1 |
| #4 temp-minion swarm ~20 | quant | poe1-srs | **B** | 1 |
| #5 placed-proxy (totem) count | quant | totem-hierophant +accruals | **B** | 1 |
| #6 enemy-seeking mobile AoE | qual | vaal-blade-vortex (1 kit) | **C** | 0 |
| **two-tier-accumulator** (NEW row) | qual | ~10 kits (shaman-bear, walking-calamity, cadence×2, tempest-strike×2, runic-invocation, raekor/shenlong, vyr-archon, d3 family) | **A** | 1 |
| **roaming-persistent-AoE / twister** (NEW) | qual | twister (~1) | **C** | 0 |
| **HoWA attribute-total-as-flat-damage** (NEW) | qual | HoWA/gemling (~1–2) | **C** | 0 |
| **GD wandering-emitter** (NEW) | qual | wind-devil (~1) | **C** | 0 |
| **GD enemy-attached-emitter** (NEW) | qual | stormbox (~1) | **C** | 0 |
| **GD proximity-armed-trigger** (NEW) | qual | rune-of-hagarrad (~1) | **C** | 0 |

New rows carry mechanism text + forcing-kit list + `provenance='book§4-accrual'`. **The R-M5 trigger-enum gaps** (`AUTOCAST_ON_MOVE`, `COMBO_BEAT_NTH`, `MINION_CONSUME`) are enum gaps, **not mints** — leave as recorded; do not add mint rows for them.

---

## D-4 — Docket ratifications + § 5 family consolidation (`mechanic_gap_docket`)

Matt: ratify as written. Operations:

1. **8 DB rows → `status='matt-ratified'`** (permanent gap record).
2. **Four "mint-or-declare" forks → `disposition='engine-design-intake'`** (NOT ruled in-book): entity-as-consumable-resource-pool (row 1), world-entity-capture (row 7, spectres), attribute→proxy-count (row 8, siege-ballista), and stun-magnitude-as-damage's declare-half (row 4).
3. **Two intentional-guard collisions → `disposition='working-as-intended'`**: perma-stunlock floor (row 4's collision half, heavy-strike-stun) + MAX_CHAIN_DEPTH=1 vs ward-loop (row 6). The engine refusing those identities is a **design position, not a gap**.
4. **Consolidate the 87 held rows → the § 5.2 taxonomy (~15 families).** Ingest the family structure as the canonical docket taxonomy; family-tag the held rows (or roll to family rows with member lists — your schema call). Keep the **stat-as-damage-substrate 6-way split intact** (DO-NOT-MERGE: armour-value · armor-conversion · stun-substrate · block-chance · max-Mana→minion · missing-Mana→spell). Side-files freeze as lineage after ingest.

---

## D-5 — Summoner un-deferral (disposition flip, NO kit re-mapping)

Matt overturned the book's reaffirm-lean: **"amend deferral; based on the count of kits this can no longer be deferred."** Operation:

- The **summoner-deferral family** (§ 5.2, ~23 rows incl. army-GAP CotA/garg) disposition flips **`deferred/Phase-5/evidence-bank` → `matt-ratified` / `disposition='engine-design-intake'`**.
- **Cross-link** each (or the family row) to `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` — **RESOLVED 2026-07-06, Matt ruled Option 1** (build the summon-skill *generation* path). D-5 is the **mapping-side** twin of that **emission-side** commit; the mapped corpus summoners become validation targets for the built gen-path.
- **NO kit re-mapping.** The ~21 summoner GAPPED kits stay mapped-to-deferral in the VDM-1 snapshot (correct — the primitive did not exist at map-time). Only the docket *disposition* changes.

---

## D-6 — No ailment-registry expansion (no DB write)

Matt: no expansion. The 16-closed registry stands. The six no-home statuses (GD confusion/electrocute/frostburn, LE Frostbite, LE Time Rot, LE Shadow Daggers) are recorded as **permanent crosswalk footnotes** in `2026-07-18-vdm1-crosswalks.md` § 8 (**gandalf-authored, this batch — not your write**). No `config/ailments.yaml` change, no DB change. Note for the record: Shadow Daggers ≈ stack-payoff = D-3 two-tier mint territory (not an ailment); Time Rot ≈ drain+chill compound.

---

## D-7 — Kit-level annotations (`kit_mapping` deviation_notes)

Seven kits (Matt ruled each). All are annotations on already-committed evidence — **no re-crawl, no legolas**.

1. **d2-wl-void-rift** → **keep-as-ghost** annotation: "kb-hallucination-class ghost; harvest FAILED all four families (honest-negative); retained as documented negative, not excised (deletion is Matt-tier)."
2. **di-bombardment** → annotate: "d3→di misapplication flag; mapped identity is the attested di one; kept."
3. **d4-spiritborn-vortex** → annotate **component-class**: "skill, not archetype; kept mapped as component-class."
4. **d2-spiritform-druid-pvp** → **relabel** the mis-specified-mechanic negative claim (correct the negative's target); keep kit.
5. **le-harvest-lich** → **SPLIT** the chimera into **two** `deviation_notes` entries — **Harvest Flay** + **Death Seal Lich** — each citing the existing basin-2 dossier anchor. Matt: "split at migration time, **no legolas re-fire**." This is an annotation refinement on held evidence, not a new-evidence fetch; the kit row itself stays one row (VDM-2 does any true two-kit split on LE re-crawl).
6. **poe1-earthshatter** → **strike** the phantom alias "Foulborn Ghostwrithe zerker(3.28)" (REVIEW-1 resolved).
7. **poe2-erasure** → **keep** the possible-phantom annotation; **no deletion** (REVIEW-2; deletion is Matt-only).

---

## D-8 — Normalizations (+ D-11d)

1. **corpus_bucket duplicate Diablo tokens** → normalize each pair to one canonical token: `diablo-3→d3`, `diablo-4→d4`, `diablo-immortal→di` (your canonical-token choice; the short form matches the per-game matrix).
2. **REVIEW-numbering collision** → basin-qualify all REVIEW ids (basin-1 "REVIEW-2" vs poe1 "REVIEW-2" → `b1-REVIEW-2` / `poe1-REVIEW-2`).
3. **Errata bookkeeping law** (standing): `errata-ledger.md` authoritative; DB `errata_applied` counter subordinate, excludes policy-restamps. Ensure the counter reflects it.
4. **D-11d suffix_rekey_status** → the 107 rows still `'awaiting-rekey'` normalize to complete/moot (the awaited re-key **IS** `kit_mapping`, now complete).

---

## D-10 — Corpus v1.1 stamp

`corpus_schema_meta`: stamp **`v1.1-verified`** (rides on D-1/D-7/D-8 ratification). Record post-migration `corpus.db` md5 in both the meta table and the MIGRATION doc. (Tracker writes are gandalf-side, post-verify.)

---

## D-11 — One-representation consolidation

- **D-11a — `kit_master` VIEW + compendium regen.** CREATE the assembled VIEW: identity ⋈ `kit_mapping`(grade, terminal, elements, ailments, deviations) ⋈ citation aggregate `{url, archive_url, site, author_handle, cite_class}` **non-quarantined** ⋈ verify C/X/U tallies ⋈ dossier row-count. Live-computed → cannot drift. Then **regenerate the compendium FROM the view, post-errata**: per-game `.md` + one `.jsonl`, stamped with the post-migration md5 + `v1.1`. This supersedes the 4 review rosters (which carry no citations). **`kit_master` must NOT expose mobile-era raw descriptors** (`elem_raw`, suffix raws) — provenance-only.
- **D-11b — DROP dead columns.** Verify 0 populated, then `ALTER TABLE canon_corpus DROP COLUMN` for **`motion_frame`, `t4_doors`, `option_c_substrate_flags`** (superseded by `kit_mapping`).
- **D-11c — deprecate `canon_corpus.source_urls`.** All 60 rows redundant with `kit_citations` (0 kit-level orphan). **Freeze + comment-deprecate** (do not drop the data; mark deprecated in schema meta; `kit_citations` is sole citation authority).
- **D-11d** — folded into D-8.4 above.
- **D-11e — close the citation orphan.** `ud-snowstorm-frost` — **gandalf is firing a legolas micro-fetch in parallel.** If it returns an admissible citation → ingest into `kit_citations` (→ **574/574**). If it returns empty (the kit is fully/near-unattested per § 9.6) → record the honest **573/574** residue in the MIGRATION doc; the compendium regenerates either way (re-stamp is cheap if a citation lands later).
- **D-11f — inversion.** Ensure the view/authority reflects: post-v1.1, `corpus.db` + compendium govern. The declaring **README at `research/vdm1/` is gandalf-authored** (this batch). You need only ensure `kit_master` reads truth from the normalized tables, never from frozen raws.

---

## Execution order (single migration)

1. Backup + pre-md5.
2. D-1 errata (ledger + kit_mapping) → D-7 annotations (incl .5 split, .6 strike) → D-3 mint stamps + accrual rows → D-4 docket ratify + § 5 consolidation → D-5 summoner flip → D-8 normalizations + D-11d.
3. D-11b drop cols → D-11c deprecate source_urls → D-11e fold citation (if legolas returned).
4. D-11a create `kit_master` view → regenerate compendium from it → stamp md5.
5. D-10 v1.1 stamp (corpus_schema_meta) + post-md5.
6. Write `MIGRATION-vdm1-post-review-<date>.md` (per-item what-changed + counts + pre/post md5). **Do NOT git-commit.**

Return a per-item report so the steward verify battery can independently recount each. Any item that can't execute cleanly: STOP that item, report it, continue the rest — do not improvise a ruling.

---

**Signed:** gandalf (run steward · SPEC-AUTHOR) · post-review migration brief · every operation traces to a Matt-ratified ruling.
