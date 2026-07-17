# DR 2-kit per-fight economy re-classification — 2026-07-17

**Author:** elrond, corpus.db single-writer, autonomous atlas-parity run (Matt delegation 2026-07-16).
**Commissioner:** gandalf-prime (autonomous-run, veto-open at Matt read).
**Concurrent processes:** gandalf-prime DRIFT-CRITIC + jack-ryan Gate-1 on Wave-D spec (`canonical/reap-die-rise-engine/wave-d-drain-fidelity-engine-spec.md`).
**Charge date:** 2026-07-17.
**Ruling:** BOTH KITS NR-LAND (elrond call; Matt veto-open).

---

## §1 Scope

Two kits carried `econ_gaps=["DR"]` in canon_engine_key after Census V11 landed 558/564 = 98.94%:

| kit_id | folk | source_game | pre econ_status | pre econ_gaps |
|---|---|---|---|---|
| `hot-norseman-frost-avalanche` | Frost Avalanche Norseman | Halls of Torment | `gap` | `["DR"]` |
| `vs-queen-sigma` | Queen Sigma | Vampire Survivors | `gap` | `["DR"]` |

The Wave-D spec (§3-§4 + §11.a + DRIFT-CRITIC rulings annex at §11 tail, collab commit `af31d358`) established from DB truth that "DR" on these kits is LEGACY VOCAB for **draft/pool-management** (roguelite meta-layer), NOT a per-fight drain: `econ_meter_type=n/a`, `economy_model=unknown` on both; mech_note verbatim "DR in old vocab = draft/pool-management." Engine will build NOTHING for DR (spec §11.a DEFER).

The question this eval owns: **does the PER-FIGHT economy of these 2 kits land honestly in landed vocabulary?**

---

## §2 Evidence base

### 2.1 Megaprobe extraction — verbatim (2026-07-12)

**`hot-facts.jsonl` line 8** (hot-norseman-frost-avalanche):
```json
{
  "movement": {"verbs": ["auto-fire-while-moving"], "policy_while_casting": "full-move",
               "skill_is_movement": false, "conf": 0.92},
  "economy": {"resource_verbatim": "offer-pool-hygiene (DR — intentional narrow draft path)",
              "model": "draft", "meter_type": "n/a", "builder_source": "n/a",
              "plain_text": "DR = draft/offer-pool. The build economy is CHOOSING WHAT NOT TO TAKE
                             — skipping all non-Frost-Avalanche upgrades keeps the offer pool pure.
                             The strategic depth is negative selection in the draft.",
              "conf": 0.82}
}
```

**`vs-facts.jsonl` line 17** (vs-queen-sigma):
```json
{
  "movement": {"verbs": ["auto-fire-while-moving"], "policy_while_casting": "full-move",
               "skill_is_movement": false, "conf": 0.95},
  "economy": {"resource_verbatim": "pre-converged-draft (100% completion unlock + per-level scaling)",
              "model": "draft", "meter_type": "n/a", "builder_source": "n/a",
              "plain_text": "DR = draft/pre-converged. The character STARTS with the draft position
                             — no build-toward needed. Per-level Might+Growth scaling = the economy
                             compounds with level rather than weapon choices.",
              "conf": 0.82}
}
```

**Reading:** both kits carry the `auto-fire-while-moving` movement verb (survivor-genre bullet-heaven signature). Both extractions give `economy.model="draft"` with `meter_type="n/a"` and `plain_text` EXPLICITLY disambiguating that "DR" = draft/offer-pool / draft/pre-converged — meta-layer commentary about **draft-pool investment** or **per-run convergence**, not per-fight resource mechanics.

### 2.2 vs-phieraggi precedent (same batch, same genre-family)

The prior econ-recrawl-2026-07-17 batch (elrond application at collab commit `0d4479e4`, artifact `agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/`) ruled `vs-phieraggi` as **NR / auto-fire** with rationale "genre-typical for VS / bullet-heavens generally." The post-batch DB state on `vs-phieraggi`:

```
canon_engine_key: econ_status=native · econ_gaps=[] · econ_meter_type=n/a · economy_model=unknown
canon_corpus.flags: 'econ-recrawl-application-2026-07-17:f4110f20:NR/auto-fire (VS-genre-native).
                    1.4s CD auto-fire; base 15 damage/4 amount/7 pierce; Revival is passive
                    run-state multiplier (+1 dmg + +1 amount per Revival, cap +10 each),
                    NOT consumable per-fire (Revival is spent only on death). Sources: ...'
```

`vs-queen-sigma` is the same game (Vampire Survivors); `hot-norseman-frost-avalanche` is the same genre-family (Halls of Torment is a survivor-genre HoT/VS descendant). Both are **structurally identical** to `vs-phieraggi` at the per-fight layer: auto-fire while moving, no per-cast resource pay, distinct meta-layer scaling.

The distinct meta-descriptors:
- `vs-phieraggi`: Revival stacks (per-run state multiplier)
- `vs-queen-sigma`: per-level +1% Might/+1% Growth compound scaling (per-level meta)
- `hot-norseman-frost-avalanche`: offer-pool-hygiene (negative-selection meta at draft layer)

All three are **per-fight NR + META-LAYER SCALING DESCRIPTOR** — the meta-layer descriptor is distinct per kit, but the per-fight economy identity is identical.

### 2.3 SS form-lock precedent (same batch, NOTABLE find 2)

The econ-recrawl-2026-07-17 batch established the pattern for **secondary economies that are real but NOT bins**: they record as descriptive lineage/gx metadata via a flag token, not as an econ bin re-classification. The DB carries `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence` tokens on `d2-fireclaw-wolf`, `d2-fury-wolf`, `d2-rabies-wolf` alongside their `spend/steady-mana` primary bin. The overlay token is **descriptor at the flag layer**, not a bin classification.

The draft-meta shape here (`offer-pool-hygiene` on hot / `pre-converged-draft` on vs-queen-sigma) is the analogous overlay: real, distinguishable, worth preserving in provenance, but **not a bin**.

### 2.4 Wave-D spec sub-option C.1 (SPEC-AUTHOR routing)

Wave-D spec §4.2 sub-option **C.1 — DEFER with re-classification signal to elrond** explicitly names this lane:

> If elrond agrees, both kits' `econ_gaps` re-key from `["DR"]` to a corpus-labelled bucket like `["draft-meta"]` or `["session-meta"]` and drop from the census "blocked on econ" bucket entirely (they'd move to a "roguelite meta-progression" OUT lane parallel to `mechanic:shapeshift` and `unknown-ailment`).

**My ruling is a stronger form of C.1**: NR-land at per-fight grain (rather than re-key `econ_gaps` to `["draft-meta"]` leaving `econ_status=gap`). Rationale: the DB truth at the per-fight grain is not "gap on draft-meta"; it is "auto-fire NR, precedent-matched to vs-phieraggi." Landing as NR is more DB-truth-honest AND drops the kits from the blocked bucket entirely (same census outcome as C.1's proposal). The draft-meta descriptor is preserved via a provenance-tagged flag overlay (SS precedent), which is the same information C.1 would have carried in `econ_gaps` but is more accurately located at the flag descriptor layer.

**Engine-side outcome is identical**: engine builds NOTHING for DR (Wave-D §11.a DEFER holds; `_DEFERRED_ECON_BINS` stays empty; no drain surface, no cost_type map entry).

---

## §3 Disposition (elrond ruling — Matt veto-open)

| kit_id | ruling | per-fight econ landed | descriptor overlay |
|---|---|---|---|
| `hot-norseman-frost-avalanche` | **NR-LAND** | `native / [] / n/a / unknown` (NR-shape) | `draft-meta-overlay-2026-07-17:offer-pool-hygiene` |
| `vs-queen-sigma` | **NR-LAND** | `native / [] / n/a / unknown` (NR-shape) | `draft-meta-overlay-2026-07-17:pre-converged-draft` |

Both kits join the existing NR-shape family (8 rows pre-write → 10 rows post-write), which already contains vs-phieraggi + 4 D2/PoE1 self-cost-native kits + 3 thorns/retaliation kits (Legolas-verified genre-native NR patterns).

**No partial disposition** — both kits are precedent-matched and evidence-symmetric.

---

## §4 DB writes ledger

Script: `agentic_orchestration/research/scripts/corpus_dr_reclassify_2026_07_17.py` (idempotent, backup-first, iron-law asserts identical PRE + POST).

### 4.1 canon_engine_key writes (UPDATE-only, 2 rows)

```sql
UPDATE canon_engine_key
   SET econ_status = 'native',
       econ_gaps   = '[]'
 WHERE kit_id = 'hot-norseman-frost-avalanche';
-- econ_meter_type='n/a' UNCHANGED, economy_model='unknown' UNCHANGED

UPDATE canon_engine_key
   SET econ_status = 'native',
       econ_gaps   = '[]'
 WHERE kit_id = 'vs-queen-sigma';
-- econ_meter_type='n/a' UNCHANGED, economy_model='unknown' UNCHANGED
```

### 4.2 canon_corpus.flags writes (UPDATE-only, 2 rows)

Flag convention (per econ-recrawl-apply-2026-07-16 house style): comma-separated tokens; each token is `<tag>:<note>`. Two tokens appended per kit:

**hot-norseman-frost-avalanche flags (post):**
```
dr-reclassify-2026-07-17:elrond-ruling:NR/auto-fire (survivor-genre-native). Per-fight econ = auto-fire-while-moving; no per-cast resource pay; meter n/a. hot = Halls of Torment; structurally identical to vs-phieraggi at per-fight layer. Draft/offer-pool is META-LAYER descriptor (see draft-meta-overlay flag). ELROND classification; Matt veto-open. Wave-D spec §4.2 C.1 stronger form (NR-land vs re-key to draft-meta).,draft-meta-overlay-2026-07-17:offer-pool-hygiene
```

**vs-queen-sigma flags (post):**
```
dr-reclassify-2026-07-17:elrond-ruling:NR/auto-fire (VS-genre-native). Per-fight econ = auto-fire-while-moving (Victory Sword); no per-cast resource pay; meter n/a. Precedent-matched to vs-phieraggi. Pre-converged-draft + per-level +1% Might/+1% Growth compound scaling is META-LAYER (see draft-meta-overlay flag). ELROND classification; Matt veto-open. Wave-D spec §4.2 C.1 stronger form (NR-land vs re-key to draft-meta).,draft-meta-overlay-2026-07-17:pre-converged-draft
```

### 4.3 corpus_schema_meta ledger

```sql
INSERT INTO corpus_schema_meta (version, applied_utc, note)
VALUES ('dr-reclassify-2026-07-17', '2026-07-17T08:32:11.059412+00:00',
        '...elrond DR reclassify note...');
```

### 4.4 Untouched (preserved verbatim)

- `canon_corpus.mech_note` (already carries `"DR in old vocab = draft/pool-management"` verbatim on hot + `"Pre-converged-draft economy: Queen Sigma IS the convergence..."` on vs — extraction-source truth preserved).
- `canon_engine_key.cell_key` (contains `unknown` in econ slot 7 — matches unchanged `economy_model`).
- `canon_engine_key.resource_verbatim` (`offer-pool-hygiene (DR — intentional narrow draft path)` on hot; `pre-converged-draft (100% completion unlock + per-level scaling)` on vs — extraction verbatim preserved).
- `canon_engine_key.raw_json` (raw fidelity preserved).
- `canon_corpus.source_urls` (extraction from 07-12 megaprobe; no new URLs added — no fresh crawl this pass).

### 4.5 Row-count conservation

| metric | PRE | POST | Δ |
|---|---:|---:|---:|
| total canon_corpus rows | 585 | 585 | 0 |
| total canon_engine_key rows | 585 | 585 | 0 |
| orphans_engine (ek without cc) | 0 | 0 | 0 |
| orphans_corpus (cc without ek) | 0 | 0 | 0 |
| dossier_owed=1 rows | 4 | 4 | 0 |
| NR-shape family (native/[]/n/a/unknown) | 8 | 10 | +2 |
| econ:DR blocked (grain=kit + negative=0 + gap contains "DR") | 2 | 0 | -2 |

Row conservation: perfect. No adds, no deletes. UPDATE-only pass.

---

## §5 Reversal SQL (Matt-veto path)

**Full reversal (both kits):**

```sql
BEGIN TRANSACTION;

UPDATE canon_engine_key
   SET econ_status = 'gap',
       econ_gaps   = '["DR"]'
 WHERE kit_id IN ('hot-norseman-frost-avalanche','vs-queen-sigma');

UPDATE canon_corpus
   SET flags = NULL
 WHERE kit_id IN ('hot-norseman-frost-avalanche','vs-queen-sigma');

DELETE FROM corpus_schema_meta WHERE version='dr-reclassify-2026-07-17';

COMMIT;
```

**Partial reversal (per-kit — Matt vetoes one but not the other):**

```sql
-- Reverse hot-norseman-frost-avalanche only:
UPDATE canon_engine_key SET econ_status='gap', econ_gaps='["DR"]'
 WHERE kit_id='hot-norseman-frost-avalanche';
UPDATE canon_corpus SET flags=NULL WHERE kit_id='hot-norseman-frost-avalanche';
-- Leave meta ledger row in place (still valid for the vs-queen-sigma half); or update note to reflect partial reversal.
```

**Pre-write flag state:** both kits carried `flags=NULL` / empty pre-write (verified in PRE-verify block of the script). Setting to `NULL` is the clean reversal to pre-write state.

**Alternative:** restore from backup:

```bash
cp agentic_orchestration/research/curated/corpus.db.pre-dr-reclassify-2026-07-17-backup \
   agentic_orchestration/research/curated/corpus.db
```

Backup md5 = `20040c5ac09ff3091161747a629e927d` (matches pre-write DB exactly).

---

## §6 md5 trail

| file | md5 |
|---|---|
| corpus.db (PRE-write) | `20040c5ac09ff3091161747a629e927d` |
| corpus.db.pre-dr-reclassify-2026-07-17-backup | `20040c5ac09ff3091161747a629e927d` |
| corpus.db (POST-write) | `11f73ab3f000b9ada1492fe496e14e09` |

Confirmed via `md5` command post-execution. Re-run of script produces `Already applied (ledger hit). Post-state verified. No-op — DB unchanged.` — idempotency verified.

---

## §7 Census consequence (V12 projection — NOT authored this pass)

- **Current V11:** 558/564 = 98.94% expressible-now.
- **Post-write projection for V12** (fires after Wave-D Gate-2): **560/564 = 99.29%** expressible-now.
- **Denominator UNCHANGED at 564** (no phantom, no negative flip, no roster change).
- **Blocked bucket delta:** blocked-6 → blocked-4 (shapeshift 3 + unknown-ailment 1; econ:DR bucket disappears).

**I do NOT author V12 in this pass** — that fires after Wave-D Gate-2 per the standard cadence.

---

## §8 Registered census-hygiene debt for V12 authoring

Census V11 §1 shows Blocked=6 with a sub-row `— of which dossier_owed held-out | 4 | 0.71%`. This is misplaced.

**DB truth (verified 2026-07-17):**

- Total `dossier_owed=1` rows: **4**
  - `la-ferality-wildsoul` (Wildsoul; in blocked-6 under `mechanic:shapeshift` bucket)
  - `la-phantom-beast-awakening-wildsoul` (Wildsoul; in blocked-6 under `mechanic:shapeshift` bucket)
  - `la-shining-knight-valkyrie` (Valkyrie; NOT blocked — expressible-now)
  - `la-liberator-valkyrie` (Valkyrie; NOT blocked — expressible-now)
- Of the 4 dossier_owed rows, **only 2 (the LA Wildsoul pair) sit inside blocked-6**. The 2 LA Valkyrie rows are expressible-now despite carrying `dossier_owed=1`.

**V12 §1 correction pattern:**

```
| Blocked                     |     4 | 0.71%  |
| — of which dossier_owed     |     2 | 0.35%  |   ← "in-pool dossier_owed sitting in blocked"
| dossier_owed (full inventory) |   4 | 0.71%  |   ← separate line (independent of Blocked)
```

Or clearer: split the dossier_owed accounting into two rows — the in-pool total (4) as a general-inventory line, and the "of which sit in blocked" (2 = LA Wildsoul pair, both under shapeshift bucket) as a subline of Blocked.

Registered here so V12 authoring picks it up; NOT fixed in V11.

---

## §9 Concurrent-process compatibility (Wave-D DRIFT-CRITIC + Gate-1)

Wave-D spec §11.a DEFER ruling and this NR-LAND ruling are **compatible**:

- **Engine side (Wave-D spec §11.a):** engine builds NOTHING for DR. `_DEFERRED_ECON_BINS` stays empty. No drain surface. No cost_type map entry.
- **Corpus side (this ruling):** per-fight econ lands as NR (landed vocab; matches vs-phieraggi shape). Meta-layer draft-management shape recorded as descriptor overlay (flag token, SS form-lock precedent).

No conflict. No rebase. Wave-D spec's §4.2 sub-option C.1 explicitly reserved this lane for elrond's judgment ("If elrond agrees..."). The stronger form of C.1 (NR-land vs re-key to draft-meta) is what DB truth supports.

**If Matt vetoes this ruling:** Wave-D spec §11.a C.2 (DEFER without re-classification) becomes the fallback — kits stay blocked, census honest at 558/564 = 98.94%. Both engine and corpus deliverables of the atlas-parity run remain unchanged either way.

**If gandalf-prime DRIFT-CRITIC or jack-ryan Gate-1 raises a BLOCK on this ruling:** reversal SQL in §5 restores pre-write state cleanly.

---

## §10 Verification pointers (for Matt / DRIFT-CRITIC / Gate-1 read)

- Script: `agentic_orchestration/research/scripts/corpus_dr_reclassify_2026_07_17.py`
- Backup: `agentic_orchestration/research/curated/corpus.db.pre-dr-reclassify-2026-07-17-backup`
- Live DB: `agentic_orchestration/research/curated/corpus.db`
- Ledger entry: `SELECT version, applied_utc, note FROM corpus_schema_meta WHERE version='dr-reclassify-2026-07-17';`
- Precedent row: `SELECT kit_id, flags FROM canon_corpus WHERE kit_id='vs-phieraggi';`
- Wave-D spec: `canonical/reap-die-rise-engine/wave-d-drain-fidelity-engine-spec.md` (§4.2 sub-option C.1)
- Census V11: `agentic_orchestration/research/curated/atlas/s2-readiness-census-v11-2026-07-17.md`
- Megaprobe evidence: `agentic_orchestration/legolas/research/megaprobe-2026-07-12/hot-facts.jsonl` :8 + `.../vs-facts.jsonl` :17
- Prior econ-recrawl batch: `agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/00-index.md`

---

**End of artifact. Ruling delivered; DB written; Matt gate-open at read; gandalf-prime + jack-ryan gate-open in flight.**
