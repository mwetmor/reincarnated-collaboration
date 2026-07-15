# Corpus curation — Minecraft Dungeons (MCD) Mode-B ingest + completion — 2026-07-15

**Author:** elrond (data steward)
**Authorization:** Matt INGEST ruling for Minecraft Dungeons (2026-07-15, "Regardless, ingest MCD"), granted on three architectural grains (classless gear-only kit architecture · unconstrained pull economy · closed-feedback-loop power curve). Completion pass authorized to finish a prior elrond run whose API stream timed out mid-execution.
**Inputs read:** `agentic_orchestration/research/knowledge/mcd-pull-mechanic/2026-07-15-mcd-mode-b-crawl-tranche1.md` (the crawl tranche — TABLES are ground truth) · the Mode-A pull-mechanic census that won INGEST · prior elrond logs (ingest 07-12, cell-key 07-13, curation A.5 07-14) · minecraft.wiki (two confirming fetches, see §Drops).
**Scripts (two-stage, both idempotent + additive):**
- `agentic_orchestration/research/scripts/corpus_ingest_mcd_2026_07_15.py` (predecessor — the ingest; ran to completion on the DB even though the agent's stream timed out)
- `agentic_orchestration/research/scripts/corpus_curation_mcd_complete_2026_07_15.py` (THIS pass — the annotation-promotion the timeout skipped)
**Backup:** `agentic_orchestration/research/curated/corpus.db.pre-mcd-2026-07-15-backup` (taken pre-ingest by the predecessor's caller). No re-backup: this completion pass makes NO destructive change (two additive columns, mcd-scoped writes only).
**Schema markers:** `corpus_schema_meta` versions `mcd-ingest-2026-07-15` (predecessor) + `mcd-curation-complete-2026-07-15` (this pass).

## One line

The MCD Mode-B tranche is ingested and curation-complete: 122 tabled kit rows → **120 ingested** (2 base-family bows dropped, both fetch-confirmed), `canon_tier='shallow'` + `architecture='notable'` now first-class-queryable on all 120, the 6 frozen-basis pull kits distinguishable from the 20 thin artifacts via a first-class `pull_pending_vocab` flag, 94 keyable rows already carrying survivor-compatible cell_keys (and already in the displacement/ghost emitter predicate), lattice_coord rekey deferred as off-critical-path — all additive, all 469 survivor cell_keys byte-identical (SHA `c6933deb…`).

## Hard-constraint proof (survivors untouched)

Survivor-key digest `SELECT k.kit_id||'|'||cell_key … WHERE row_class='combat-kit' AND negative=0 AND game!='mcd' ORDER BY kit_id` → **SHA256 `c6933deb633e756f5fab280de7496ef9f0862bf575174bb9138589f8086e823a`**, byte-identical before and after the completion pass (asserted in-script; the run aborts otherwise). Every write in this pass is `WHERE game='mcd'` (or the explicit 6-kit pull set). No survivor row, no non-mcd row, altered.

---

## Counts (tables are truth)

| stage | n | note |
|---|---|---|
| tabled kit rows (tranche §A melee + §B bows/crossbows + §C artifacts) | **122** | 28 melee + 30 bows + 20 crossbows + 44 artifacts. legolas's own census summary said 119 — an arithmetic undercount (bows −2, crossbows −1). The TABLES are ground truth; ingest parses them directly. |
| DROPPED (base-family weapons) | **2** | `mcd-void-bow`, `mcd-twisting-vine-bow` (see §Drops) |
| **ingested (mcd- prefix)** | **120** | corpus total 524 → **644** |

Segment breakdown of the 120: **weapons 76** (74 @ key_completeness=5, 2 @ kc=4) · **artifacts 44** (all @ kc=1). Keyed (cell_key present) **94** = 70 weapons + 24 artifacts. Unresolved **26** = 6 pull + 20 thin artifacts.

## Drops — the 2 rulings (both fetch-confirmed, were UNLOGGED)

The predecessor dropped these deliberately (they are in the tranche's boundary section as gandalf/legolas flags) but did not log the rulings. Both verified against minecraft.wiki this pass; **both drops correct**:

1. **`mcd-void-bow` — DROP.** minecraft.wiki: rarity **COMMON/RARE** (base weapon), unique variant = **Call of the Void**, no pull mechanic. This is a base-family weapon; its unique variant `mcd-call-of-the-void` IS in the tranche and **kept**. Dropping the base while keeping the unique is the exact **Wind Bow precedent** (Wind Bow base excluded; its uniques Burst Gale Bow + Echo of the Valley kept) and honors the Matt-agreed unique-weapon-grain ruling (unique-rarity = kit; base-rarity = not a kit row).

2. **`mcd-twisting-vine-bow` — DROP.** minecraft.wiki: rarity **COMMON/RARE** (base weapon), unique variant = **Weeping Vine Bow**, intrinsic = **Poison trail**, no pull mechanic. Base-family weapon; its unique variant `mcd-weeping-vine-bow` IS in the tranche (confirmed intrinsic Roll Charge I + poison trail) and **kept**. legolas self-flagged the unconfirmed intrinsic (tranche §BOUNDARY note 2); the fetch resolves it (base-rarity + Poison-trail) and **substantiates the predecessor's script-comment claim**, which the tranche table alone did not record. Same precedent as Void Bow / Wind Bow.

## Annotation mappings

| annotation | how it lands | queryable via | status |
|---|---|---|---|
| **depth = shallow** | `canon_tier='shallow'` (first-class column, set at ingest) | `WHERE canon_tier='shallow'` | 120/120 ✓ (predecessor) |
| **architecture = notable** | **`architecture` TEXT — NEW first-class column, set='notable' on all mcd rows** | `WHERE architecture='notable'` → **120** | 120/120 ✓ (this pass) |
| **pull_pending_vocab** (the 6) | **`pull_pending_vocab` INTEGER — NEW first-class column, =1 on the 6 pull kits, =0 else** | `WHERE unresolved=1 AND pull_pending_vocab=1` → **6** | 6 ✓ (this pass) |

**Why `architecture` became a column (the load-bearing steward call).** The INGEST was granted specifically on 3 architectural grains — consumers MUST be able to *find* these rows. At the timeout, the annotation existed ONLY inside the `flags` JSON array (`["depth:shallow","architecture:notable",…]`). That is a fragile substring match, and gandalf's named-column inspection (correctly) reported "notable lands nowhere" — because SQLite named-column queries do not see inside a JSON blob. Per **Discipline #14 (tagged, not encoded)** — semantic meaning belongs in an explicit tag column, not packed in a blob — I promoted it to a first-class column with the same standing `canon_tier='shallow'` already has. The `flags` token is **left in place** (redundant provenance, non-destructive).

**Why `pull_pending_vocab` became a column.** A consumer must distinguish "unresolved because *pull vocabulary* is pending the Edition-II pass" from "unresolved because the *artifact note* is a thin category-page one-liner." Both are `unresolved=1`. The distinction lived only in `flags` (`pull_pending_vocab:true` + `unmapped_pending_curation:pull_pending_vocab`). Promoted to a first-class INTEGER so the two unresolved sub-populations are cleanly separable:
- `unresolved=1 AND pull_pending_vocab=1` → **6** pull-primary kits (mcd-hammer-of-gravity, mcd-encrusted-anchor, mcd-echo-of-the-valley, mcd-burst-gale-bow, mcd-imploding-crossbow, mcd-voidcaller)
- `unresolved=1 AND pull_pending_vocab=0` → **20** thin non-combat artifacts

## The unresolved 26 — rationale

**26 rows carry `unresolved=1`, in two distinct, deliberate populations:**

**(a) 6 pull-primary kits — `pull_pending_vocab=1`, frozen-basis gate.** These deliver INWARD force (Gravity I / wind-helix pull). `pull` is NOT a function level in the Edition-I lattice. The discipline (Matt-agreed, tranche §pull_pending_vocab) is explicit: do **NOT** force-key `function=knockback` — inward force ≠ outward force. They land unresolved with **NO `canon_engine_key` row** (so they stay out of the combat denominator AND the displacement/ghost join) until the **Edition-II vocabulary pass** elevates `pull` to a function. This is the existing unmapped-pending-curation mechanism, now made queryable via the first-class flag. Five are @kc=5, voidcaller @kc=4 (see below).

**(b) 20 thin non-combat artifacts — `pull_pending_vocab=0`, thin-note gate.** These 20 `mcd-art-*` rows are category-page one-liners for non-combat utility (boots, quivers, satchels, tomes, totems of casting/regeneration, gong, light-feather, powershaker, soul-healer, enchanter's-tome, etc.). Their mech_notes carry no deterministically-keyable combat geometry/control/economy signal, so keying them would violate the never-invent discipline. They land unresolved (thin-artifact-note), matching the tranche's own caveat. **Confirmed correct.** (The other 24 artifacts — those carrying a clear control / summon / defensive / definite-delivery signal — ARE keyed.)

## Staging / keying state

- **key_completeness** (count of the 6 prefix coords non-NULL): **5 on 74 weapons · 4 on 2 rows · 1 on 44 artifacts.** Provenance `mcd-mode-b-steward-derived` (prefix_conf_provenance column), steward-derived from tranche prose (MCD lacks the `canon_probe_facts` families the survivors had).
- **kc=5 is the MCD ceiling, not kc=6.** `attr_val` (STR/DEX/INT/WIS) is NULL on **all 120** mcd rows — Minecraft Dungeons is **classless** (grain #1 of the INGEST rationale), so there is no attribute axis to key. Honest structural NULL, not a gap.
- **The 2 rows @ kc=4 — RESOLVED (identified; nothing to complete).** `mcd-mechanized-sawblade` and `mcd-voidcaller`. Both are kc=4 = (ceiling kc=5) − `tempo_val`. `tempo_val` derives from a numeric `speed` stat in the prose; both notes say "**Power unspecified**" / speed-class with no numeric speed, so tempo is honestly NULL. There is no data to key without inventing it (never-invent). Documented, not "filled." (Note: voidcaller is also one of the 6 pull kits — it stays unresolved regardless; its kc=4 is orthogonal to its pull gate.)
- **suffix_rekey_status = 'awaiting-rekey' throughout — left as-is.** MCD carries no `geo_raw/ctrl_raw/def_raw/econ_raw` suffix descriptors (0/120 populated) — it was keyed directly from prose, not from a suffix-descriptor harvest. So the field's *literal* meaning (raw-descriptor rekey pending) is inapplicable to MCD. The default `awaiting-rekey` is harmless and correctly signals "not yet promoted to the survivors' `keyed-v1` lattice standard." No change.

## Rekey decision — DEFERRED (with a precise unblock note for the displacement re-run)

**The `awaiting-rekey → lattice_coord` pass does NOT fire this batch. It is a separate queued step.**

The decisive finding: **the displacement re-run does NOT gate on `lattice_coord`.** Both `displacement_field_edition1.py` (line 185-186) and `ghost_field_edition1.py` (line 254-255) read `canon_engine_key.cell_key` via the predicate `row_class='combat-kit' AND negative=0 AND cell_key IS NOT NULL`. Neither script reads `lattice_coord` — that column is *written* at ingest and consumed by nothing today.

- **On the operative surface (`cell_key`), MCD is ALREADY MAPPED.** All **94** keyable mcd rows carry well-formed 14-field cell_keys built with the survivors' exact `serialize_cell_key` + enums (survivor-compatible vocabulary), and **all 94 already satisfy the displacement/ghost predicate.** A verification query confirms 94/94 mcd rows in the predicate.
- **Therefore the displacement-field re-run (Edition-II drill-in slate confirmation) can move NOW** for the 94 keyable mcd kits — no rekey required to unblock it. The 6 pull kits + 20 thin artifacts correctly stay out (no engine-key row). **This is the actionable message for gandalf: the re-run is not blocked on elrond.**
- **The `lattice_coord` population itself is DEFERRED** as a distinct queued batch, because (a) nothing reads it — it is entirely off the critical path; (b) doing it faithfully requires the same atlas-lattice derivation the survivors received at ingest, best batched with the next atlas-derivation pass to avoid a hand-rolled one-off; (c) firing it now risks divergence from the authoritative, already-done `cell_key`. **Estimate: one focused sub-pass (~30–45 min of steward work) folded into the next atlas-derivation batch;** it changes no downstream field-emitter output (they don't read it), so there is no urgency and no re-run dependency on it.

## Final state (post-completion, verified)

- `canon_corpus`: **644** (was 524; +120 mcd). No re-ingest — the 120 already existed from the predecessor's run.
- mcd `architecture='notable'`: **120/120** · mcd `canon_tier='shallow'`: **120/120**.
- mcd `unresolved=1`: **26** = 6 `pull_pending_vocab=1` + 20 thin (`pull_pending_vocab=0`). `pull_pending_vocab=1` leaked to non-mcd: **0**.
- mcd keyed (`canon_engine_key.cell_key` present): **94** · all 94 in the displacement/ghost predicate.
- mcd `lattice_coord`: **0** (deferred, documented).
- DB integrity: **ok** · survivor cell_keys byte-identical (SHA `c6933deb…`) · both scripts idempotent (re-run → identical, ALL CHECKS PASS).

## ADR-004 / Principle-6 boundary

**No round-trip owed.** Every write is an additive column/value inside elrond-stewarded `corpus.db`. No `canon_engine_key.raw_json`-carried engine field, no star-lord telemetry schema, no `fight_log`/`export`/`loadout` packet touched. Star-lord-side `MIGRATION.md` unaffected. The two new columns (`architecture`, `pull_pending_vocab`) are collab-side curation surface.

## Reproducibility (Discipline #11)

Clean rebuild sequence (corpus.db stays gitignored; the scripts + this log + the MIGRATION entry are the committed truth):

```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_cell_key_materialize_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_curation_a5_2026_07_14.py
python3 agentic_orchestration/research/scripts/corpus_ingest_mcd_2026_07_15.py            # MCD ingest
python3 agentic_orchestration/research/scripts/corpus_curation_mcd_complete_2026_07_15.py # THIS (completion)
```

## Left for downstream (leftovers, not enactments)

1. **Edition-II vocabulary pass** — elevate `pull` to a lattice function level, then the 6 `pull_pending_vocab=1` kits can be keyed (currently correctly unresolved, no engine-key row). Gandalf/Matt own the vocabulary decision; elrond keys once the function exists.
2. **lattice_coord materialization for the 94 keyable mcd rows** — deferred queued batch (see rekey decision); ~30–45 min, no field-emitter dependency, fold into next atlas-derivation pass.
3. **20 thin artifacts** — a Legolas Mode-B re-crawl of the individual artifact wiki pages (not the category page) would be the only path to keyable combat coords for these; today they are honestly unresolved.
