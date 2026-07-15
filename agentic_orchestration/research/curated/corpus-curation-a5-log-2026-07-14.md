# Corpus curation batch A.5 — the atlas-derivation data snapshot — 2026-07-14

**Author:** elrond (data steward)
**Authorization:** Matt-authorized autonomous run 2026-07-14 ("proceed autonomously… until a decision is warranted"); Matt-ratified binding (d) of the 2026-07-13 direction analysis; re-confirmed under the atlas-derivation charter ("adopted. let's proceed.").
**Inputs read:** `gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` §A.2/§A.3/§A.5 · `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §5 Stage 0 · prior elrond logs (ingest 07-12, cell-key 07-13).
**Script:** `agentic_orchestration/research/scripts/corpus_curation_a5_2026_07_14.py` (idempotent; ADDITIVE; reuses the survivors' exact keying functions from `corpus_cell_key_materialize_2026_07_13.py`).
**Backup:** `agentic_orchestration/research/curated/corpus.db.pre-A5-2026-07-14-backup` (integrity ok; captured 470 combat-kit / 470 cell_keys pre-batch).
**Schema marker:** `corpus_schema_meta` version `atlas-prereg-2026-07-14` — **this is the tagged state the derivation pipeline runs against.**

## One line

Five hygiene+negatives items landed against the corpus DB, additively, without touching the 469 clean survivor keys (SHA256 `6ac89754…` byte-identical before/after) — the graveyard is now keyed, provenance-tagged, and self-documenting-excluded from the combat denominator, and the mech_note truncation is repaired to the limit the harvest allows.

## Hard-constraint proof (survivors untouched)

`SELECT k.kit_id, k.cell_key … WHERE row_class='combat-kit' AND negative=0 ORDER BY kit_id` →
**SHA256 `6ac897549ff0e8d6d724ad76a3046e8ac845d6a45c63846e3340fa8a90a86dcd`** — identical pre- and post-batch. 469 survivors, 0 altered. No survivor-key edits made (see §item-3 anomaly-log: none found).

---

## Item 1 — mech_note 140-char truncation

**Path taken: LOCAL RE-EXTRACTION from the committed megaprobe facts JSONL.** No external re-crawl.

The dispatch hypothesis (raw_json carries verbatim mech_note → local UPDATE from raw_json) is **FALSE**:
- `canon_engine_key.raw_json` has **no mech_note field** (the engine-key JSONL never carried it).
- The v3 CSV `rdr-kit-atlas-v3.csv` (the DB's mech_note source at ingest) is **itself truncated at 140** — max length 140, 446 rows at ~140, identical mid-word tails to the DB. Truncation is **upstream of my ingest.**

The **untruncated source** is the legolas megaprobe per-game facts JSONL (`agentic_orchestration/legolas/research/megaprobe-2026-07-12/*-facts.jsonl` + `mint-dossiers-reexpressed.jsonl`): positives store the postmortem in `mechanics_notes` (up to **739 chars**); negatives store it in a `mech_note` field. Re-extracted grow-only (a shorter facts note = whitespace/em-dash normalization, never applied).

- **237 rows repaired (grown)**; 14 of them negatives.
- **211 rows remain at exactly 140** — these are rows where even the facts source is ≤140 (natural length) or itself 140-capped at the mobile-harvest primary-capture step. **Genuinely unrepairable without a Legolas Mode-B re-crawl of the original build-guide prose** (documented residual, not a batch failure).
- Only non-match: `le-ring-of-shields` (mint kit, mech_note already NULL, positive — out of scope).

---

## Item 2 — d2-sacrifice fill-or-quarantine → **FILL**

d2-sacrifice is `negative=1`, `mint=1`; its mech_note was NULL in the DB (no CSV row — it is a mint kit) but a **real postmortem exists** in `mint-dossiers-reexpressed.jsonl`. Decision rule (dispatch): real postmortem present → **fill + re-key properly**.

- mech_note filled from the mint dossier (0 → **275 chars**).
- Re-keyed by the same negative-keying rules as item 3 (recoverable coords land; passives NULL). Its old junk key `walk|blank|spiky|melee_strike|blank|unknown|…` is **overwritten** with a proper negative key `blank|at-target|spiky|blank|blank|blank|blank|blank|solo|melee|med|blank|active|one-shot`.
- **Denominator exit mechanism (self-documenting):** rather than a bespoke quarantine flag, d2-sacrifice is excluded from the combat denominator by the **`negative=0` filter** now on `v_combat_kits` (and it was always excluded from `v_corpus_substrate`, which already carried `AND negative=0`). Read `WHERE row_class='combat-kit' AND negative=0` = the 469 clean denominator; d2-sacrifice is not in it. **Verified:** the 470→469 denominator drop and the 457→456 cell drop are *exactly* the d2-sacrifice leak removal — 0 survivors held its junk cell_key, so no survivor cell was lost.

This unifies item 2 with item 3: d2-sacrifice is simply the 38th negative, keyed identically and excluded identically.

---

## Item 3 — re-key the 37 unkeyed negatives (38 total with d2-sacrifice; deduped)

**Structural finding:** the negative facts rows are **sparse** — they carry only `delivery`, `footprint`, `atlas_key`, and a postmortem + `why_negative`. They **lack** the `control` / `defense` / `economy` / `movement` / full `prefix_claims` dicts the positives carried. So most cell_key coordinates are genuinely unrecoverable at positive fidelity, exactly as charter §5 Stage 0 anticipates (unknown coords = passive).

**Recoverability matrix (verified against source):**

| coord | source | outcome | fill n/38 |
|---|---|---|---|
| #2 delivery_value | facts.delivery.value | recoverable | 38 |
| #3 amp_val | canon_corpus (atlas decode) | recoverable | 37 |
| #8 proxy_val | canon_corpus | recoverable | 36 |
| #9 range_val | canon_corpus | recoverable | 36 |
| #10 tempo_val | canon_corpus | recoverable | 36 |
| #11 commit_val | canon_corpus | recoverable | 35 |
| #12 activation_val | (repaired) mech_note text-tells | recoverable | 38 |
| #13 dependency_val | (repaired) mech_note text-tells | recoverable | 38 |
| #1 mob_policy_while_casting | facts.movement **absent** | **NULL (passive)** | 0 |
| #4 geometry_value | delivery+footprint **ambiguous for all 37** | **NULL (passive)** | 0 |
| #5a ctrl_treatment | facts.control **absent** | **NULL (passive)** | 0 |
| #5b ctrl_function | facts.control **absent** | **NULL (passive)** | 0 |
| #6 def_bin | facts.defense **absent** | **NULL (passive)** | 0 |
| #7 economy_model | facts.economy **absent** | **NULL (passive)** | 0 |

**Geometry NULL rationale (the load-bearing steward call):** geometry_value for the positives came from gandalf's engine-key judgment (R-rules with rich context), not a mechanical decode. I built the deterministic `(delivery, footprint) → geometry` map from the 478 positive engine-key rows: only 16 of 34 pairs are single-geometry. **Every one of the 37 negatives lands on an AMBIGUOUS pair** (e.g. `at-target|point` → {single_target, melee_strike, dash_attack, totem, vortex_pull, teleport}). Guessing would violate the never-invent discipline AND the dispatch's explicit NULL-not-guess rule → geometry NULL for all 37. The atlas_key does **not** deterministically encode geometry either (seg1[:2] patterns overlap across geometries — checked).

- **38 negatives keyed** (37 combat-kit with a proper 14-field cell_key + 1 system-record).
- All 37 combat-kit negative cell_keys are well-formed (14 pipe-fields, exactly one per coord with #5 double).
- They stay `negative=1`, **supplementary-only** — they NEVER shape the denominator or the axes (charter §5).

**One classification correction (flag to gandalf, resolved by me per §A.2):** `vs-golden-egg-scaling` is keyed `row_class='system-record'` (route `loot-economy/degeneracy-evidence`), **not** combat-kit — §A.2 pattern 11 classes it a system-level evidence record, not a kit. It gets NO cell_key (out of the combat denominator, matching the survivor system-record rule). This is the same kit the ingest log flagged as "absent from engine-key"; it now has a system-record row.

---

## Item 4 — the 5 no-rule-matched pipeline TODOs

`d2-impale-zon`, `gd-reap-spirit`, `d2-grim-ward-barb`, `d2-leap-attack-barb`, `hot-blood-catcher`. Confirmed (item-1 re-extraction): **all 5 carry real genre postmortems** → they are genre-negatives, not a provenance class. **All 5 are in the 37** and were keyed by item 3 (natural dedupe). `hot-blood-catcher` grew 140→277 chars in item 1; the other 4 were already ≤140 (not truncated). "No rule matched" was a keying-pipeline TODO flag, now resolved.

---

## Item 5 — death_class provenance column

**`canon_corpus.death_class TEXT`** added (ADDITIVE), CHECK-equivalent via two BEFORE-INSERT/UPDATE triggers rejecting non-enum non-NULL writes (SQLite can't ALTER-ADD a CHECK). Enum verified enforced (a `'bogus-value'` write was rejected; the row kept its value).

Enum (per §A.5-5): `extrinsic-tuning / extrinsic-itemization / extrinsic-split-scaling / extrinsic-no-lever / extrinsic-content-mix / intrinsic-red / system-evidence`.

**Assignment: 26 of 38 assigned per the §A.2 pattern→class map; 12 NULL (left for gandalf, each flagged).**

| death_class | n | members |
|---|---|---|
| extrinsic-tuning | 6 | d2-inferno-sorc, d2-blade-sin, tl2-arc-beam, d3-shield-bash, poe2-wall-of-shields, poe2-chronomancer-01 |
| intrinsic-red | 5 | d2-blaze-sorc, poe1-charged-dash, d2-leap-attack-barb, poe1-reaper, vs-gatti-amari |
| extrinsic-itemization | 5 | d3-firebomb, d3-wave-of-force, d4-wind-shear, d4-kick, le-shield-bash-le |
| extrinsic-split-scaling | 3 | d2-golemancer, gd-reap-spirit, le-soul-feast |
| extrinsic-no-lever | 3 | poe1-wild-strike, le-tempest-strike, gd-stun-jacks |
| system-evidence | 2 | hot-blood-catcher, vs-golden-egg-scaling |
| extrinsic-content-mix | 2 | gd-blade-trap, poe1-glacial-hammer |
| **NULL → gandalf** | **12** | (see below) |

**The 12 NULL corpses — each with a `flags` note on `canon_engine_key` (do NOT invent; gandalf adjudicates):**

- `d3-spectral-blade` — §A.2 patterns 2(itemization)+10(sibling-shadowed, no class); no dominant.
- `d4-blade-shift` — patterns 2(itemization, extrinsic)+4(movement-pretense, intrinsic-red); **incompatible classes.**
- `poe2-perfect-strike-01` — patterns 8(pricing-law, no class)+12(port-context, no enum value).
- `tq-calculated-strike` — pattern 8 only (pricing law — no death= provenance class in §A.2).
- `d2-impale-zon` — patterns 8+9 (both structural/pricing — no death= class).
- `poe1-cleave`, `poe1-sweep`, `tq-flame-surge` — pattern 10 only (sibling-shadowed isotope losers — validation, not corpse; no death= class).
- `poe2-concoction` — pattern 12 only (port-context death; **§A.2 provides no matching enum value** — candidate `extrinsic-port`).
- `d2-grim-ward-barb` — not a named member of any §A.2 pattern list (buffed-because-dead in-joke; was a keying-TODO).
- `d4-incinerate` — cited in §A.3 CONTESTED (rooted-channel, tuning-adjacent) but **not a §A.2 pattern MEMBER**.
- `d2-sacrifice` — §A.1 classes it an "unfilled record" (leaked mint kit), not a §A.2 failure-pattern member.

**Multi-tag resolution rule applied:** where §A.2 names a kit's dominant `death=` line unambiguously, it was assigned; where the prose leaves it split between two incompatible classes (extrinsic vs intrinsic) OR the only pattern is a no-class one (pricing-law 8, isotope 10, port-context 12-with-no-enum), it was left NULL. One explicit override: `poe1-glacial-hammer` → `extrinsic-content-mix` (§A.2-9 lists it as a content-mix ST member; the pattern-10 dual is secondary).

---

## Final counts (post-batch, verified)

- `canon_corpus`: **524** · negatives **38**.
- `canon_engine_key`: **524** (was 487; +37 = the newly-keyed negatives, d2-sacrifice already had a row).
- combat-kit (raw): **506** · system-record (raw): **18** (was 17; +vs-golden-egg-scaling).
- **COMBAT DENOMINATOR** (`combat-kit AND negative=0`): **469** — = `v_combat_kits` (amended `+AND c.negative=0`).
- Denominator distinct cell_key: **456 / 469** (was 457/470; the −1 is the d2-sacrifice leak removal, confirmed unique).
- Negatives keyed: **38/38** · with cell_key (combat-kit negs): **37** · as system-record: **1**.
- death_class: **26 assigned / 12 NULL**.
- DB integrity: **ok**.

## Survivor-key anomalies logged

**None.** The hard-constraint SHA256 is byte-identical; no wrong survivor key was discovered during the negatives pass. (Had one been found, per dispatch I would log-not-fix here.)

## ADR-004 / Principle-6 boundary

**No round-trip owed.** All writes are additive columns/rows inside elrond-stewarded `corpus.db`; no `canon_engine_key.raw_json`-carried engine field, no star-lord telemetry schema, no `fight_log`/`export`/`loadout` packet touched. `v_corpus_substrate` unchanged (already `negative=0`). Star-lord-side MIGRATION.md unaffected.

## Reproducibility (Discipline #11)

Idempotent — re-run → item 1 grows 0 (repairs persist), negatives re-key to identical values, marker rewritten. Clean rebuild sequence (now FIVE committed scripts):

```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_cell_key_materialize_2026_07_13.py
python3 agentic_orchestration/research/scripts/corpus_curation_a5_2026_07_14.py   # THIS
```

corpus.db stays gitignored; the script + this log + the MIGRATION entry are the committed truth.

## Left for gandalf (leftovers, not enactments)

1. **12 NULL death_class corpses** (listed above; each flagged on `canon_engine_key.flags`). Notably: does the enum want an **`extrinsic-port`** value (poe2-concoction, the cleanest port-context exhibit)? And should the incompatible-class kits (d4-blade-shift: itemization vs movement-red) carry both tags or a dominant?
2. **211 mech_note rows still ≤140** — a Legolas Mode-B re-crawl of build-guide prose is the only path to full postmortems for these (a re-harvest commission, not an elrond curation step).
3. **geometry (+ ctrl/def/econ/mob) NULL on all 37 negatives** — if the collision/CONTESTED analysis wants these corpses placed geometrically, a targeted Legolas re-probe of the negatives' full mechanics (not just delivery+footprint) would be needed; today they are honestly passive.
