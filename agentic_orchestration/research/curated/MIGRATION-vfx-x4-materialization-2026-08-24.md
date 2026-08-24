# MIGRATION — `vfx-x4-materialization-2026-08-24`

**Owner:** elrond (catalogue seam) · **Substrate:** `agentic_orchestration/research/curated/corpus.db`
**Authority:** cross-seam routing **X-4**, VFX archetype-binding run.
Commissioned at charter **L-35** (conductor ruling 1), EXPANDED at **L-38** (the bridge column),
extended at **L-39** (the `aura` finding). Run **SEALED at L-40**.
**Spec of record:** `agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md`
(STATUS: SEALED — filename retained) §§ 3.1a / 3.1b / 4.1.
**Status:** **APPLIED 2026-08-24.**

---

## What happened (one line)

Materialized T-K as the durable view **`v_vfx_kit_skill_binding`** (body verbatim from spec § 4.1),
added a **reciprocal fold bridge** to `vfx_archetype` so the DB-says-27 / spec-says-24 delta closes
from the database alone, and recorded the **`aura` emitter-anchor mis-attestation** (L-39 item 4)
as 13 catalogue findings — measured, not estimated, and **broader than the one Demonologist case**.

---

## Consumer-visible surface changes (the ADR-004 reason this note exists)

| Surface | Change | Breaking? |
|---|---|---|
| `v_vfx_kit_skill_binding` | **NEW view.** 1,134 rows. | No — additive. |
| `vfx_archetype` | **+6 columns:** `fold_status`, `folded_into`, `fold_survives_as`, `fold_receives`, `fold_authority`, `fold_note` | No — `SELECT *` widens; every pre-existing column is byte-identical. |
| `vfx_curation_finding` | **+13 rows** under `curation_run='vfx-x4-materialization-2026-08-24'` | No — append-only table by construction. |
| `vfx_archetype_member` | **NOT TOUCHED. Not one row, not one column.** | — |

**Any consumer that does `SELECT *` on `vfx_archetype` will see six new trailing columns.** That is the
only contract change, and it is why this note exists rather than a log line.

### ⚠ The one trap a consumer must know about

`vfx_archetype.member_skills` / `member_kits` are **PRE-FOLD** and were **deliberately not rewritten** —
rewriting a P1 measurement would destroy the reversibility the vote was built on. So:

- `circle` stores **43 / 43**. Post-fold truth is **93 / 88**.
- `dash_attack` stores **32 / 31**. Post-fold truth is **36 / 35**.

**The authoritative post-fold count is `v_vfx_kit_skill_binding`, never `member_skills`.** This is
stated in each receiving row's own `fold_note`, so a reader who lands on the row is told in place.

---

## (1) `v_vfx_kit_skill_binding` — the T-K materialization

The view **body is the spec's § 4.1 "derivation of record", reproduced verbatim.** No derivation was
invented, extended, or "improved". If it must change, the spec changes first.

The folds are lossless and **the view is the mechanism**: a folded row keeps its lineage in
`archetype_id_prefold` and its distinguishing read in `tier1_layer_flag`. A row that was `ring` is now
`circle` + `annulus`; a row that was `defensive_dash` is now `dash_attack` + `defensive`.

### Verification against the spec's live counts

| Check | Spec § 4.1 claims | Measured at X-4 | |
|---|---|---|---|
| Bound rows | **1,135** | **1,134** | ⚠ **see finding X007** |
| Distinct kits | 511 | **511** | ✅ exact |
| Active archetype values | 24 | **24** | ✅ exact |
| `tier1_layer_flag='annulus'` | 50 | **50** | ✅ exact |
| `tier1_layer_flag='defensive'` | 4 | **4** | ✅ exact |
| `circle` post-fold | 93 / 88 | **93 / 88** | ✅ exact |
| `dash_attack` post-fold | 36 / 35 | **36 / 35** | ✅ exact |
| `knockback` held out | 1 | **1** | ✅ exact |
| **Zero skills lost to the folds** | asserted | **PROVEN** — pre-fold 43+50+32+4 = 129 = post-fold 93+36; and a NOT-EXISTS assert confirms every eligible member row appears in the view | ✅ |

### ⚠ The count mismatch — surfaced, not reconciled (finding **X007**, WARN)

The derivation returns **1,134**, not 1,135. **The delta is exactly one row and its cause is exact:**
the spec's verification-table parenthetical reads *"(= 1,138 skill rows − 3 unassignable)"* = 1,135,
which stops **one clause short of the SQL it is verifying** — the query also carries
`AND m.archetype_id <> 'knockback'`, and the very next line of the same table records
*"knockback excluded: 1 row held out."*

- **1,135** = ASSIGNED skills (P1's number; the denominator in the P1 note's "847 / 1,135 = 74.6%").
- **1,134** = BOUND skills, post-hold — which is what T-K actually is.

**The spec is internally correct everywhere else.** Its own § 3.1a index sums to exactly **1,134**
across the 24 active rows, and `SUM(member_skills)` over the 26 non-held archetypes is also exactly
**1,134** (1,135 including `knockback`). **This is a headline/derivation off-by-one in two printed
cells — not a substrate defect, not a lost skill, and not a re-ruling.** Routed to gandalf as an
editorial correction to two cells.

---

## (2) The fold bridge — closing DB-says-27 / spec-says-24

`27 = 24 active + 2 folded + 1 held`, and **that arithmetic now resolves from `vfx_archetype` alone**
without reading the ledger.

| archetype | `fold_status` | `folded_into` | `fold_survives_as` | authority |
|---|---|---|---|---|
| `ring` (50 / 47) | `folded` | `circle` | `annulus` | L-29(1) |
| `defensive_dash` (4 / 4) | `folded` | `dash_attack` | `defensive` | L-29(2) |
| `knockback` (1 / 1) | **`held`** | **NULL — by intent** | — | L-14 + L-29 (F-3) |
| `circle` | `active` | — | `fold_receives = ring (…)` | — |
| `dash_attack` | `active` | — | `fold_receives = defensive_dash (…)` | — |

### HELD is not a fold, and the schema enforces it

L-38's shorthand was "ring→circle, defensive_dash→dash_attack, **knockback→HELD**". Rendering that
literally would put `HELD` in `folded_into` and **collapse two different states into one column**.
`knockback`'s members moved **nowhere**; it has zero corpus and the run deliberately refused to name a
destination for it. So:

- `folded_into` is **NULL** for `knockback`, and a commit-time assert fails the migration if a `held`
  row ever carries a fold target.
- The state lives in `fold_status`, which is `CHECK`-constrained to `('active','folded','held')`.

### The bridge is reciprocal

A one-way bridge only half-closes the gap: a reader approaching from `circle` would read
`member_skills = 43` and be wrong by 50 skills. So the fold **targets** carry `fold_receives` plus a
`fold_note` stating the pre-fold caveat in place. A commit-time assert fails the migration if any
`folded_into` points at a row that does not declare what it received.

### Losslessness is inspectable, not merely claimed

Pre-fold identity is recoverable **three independent ways**, none of which requires the ledger:
`v_vfx_kit_skill_binding.archetype_id_prefold` · `tier1_layer_flag` · and
`vfx_archetype_member.archetype_id`, which was never rewritten.

---

## (3) The `aura` emitter-anchor finding (L-39 item 4)

**Recorded as a catalogue finding. NOT a grain change and not proposed as one** — the `geometry_value`
key grain was Matt-audited and CONFIRMED at L-39; reopening it is a HALT to Matt, not elrond's call.

**L-39 asked about one case. Measured, it is six.** Of the 73 skills attested `aura` — which T-A
§ 3.1.8 defines as a *caster-centred persistent field* — **6 (8.2%) carry an emitter anchored
somewhere other than the caster**, on two distinct sub-shapes:

- **A · placed / world-anchored (n=4)** — `d2-summon-druid#3` and `d2-wind-druid#3` (Oak Sage ×2),
  `d3-mundunugu-sb#3` (Big Bad Voodoo), `di-crusader-banner-support#0` (Holy Banner). These are
  **`totem` emitter geometry** (two-layered: delegate body + emitted effect).
  Oak Sage is the sharp one: the curator **named the anchor** — *"Oak Sage is stationary placed
  emitter = maps as aura (not summoner GAP)"* — and routed it to `aura` anyway. That is a **deliberate
  call to disagree with, not an oversight**, and it is recorded as such.
- **B · delegate-carried / distributed (n=2)** — `poe2-infernal-legion#0`, `chr-demon-legion-warlock#1`.

Two further rows (`tli-iris2-thunder-magus#1`, `tli-moto-bots#1`) are **composite and mutually
contradictory** — the same skill name, `Machine Army`, is attested as *"summons front-line guard"* in
one kit and *"= buff aura"* in the other. Carried as a **ceiling of 8/73 = 11.0%**, not as confirmed,
because this finding will not resolve a source contradiction by preference.

### Three things the measurement turned up that L-39 did not anticipate

1. **The seed case is the weakest of the six.** `poe2-infernal-legion` states its own anchor outright
   (*"the MINIONS are the delivery vehicle… per-minion aura… the player positions the swarm"*) — real
   field, wrong anchor. The Demonologist's 39 demons arguably have **no field at all**; `aura` is
   standing in for *swarm coverage*, an **area outcome produced by independent bodies**. A VFX built
   to T-A § 4.3's `aura` binding (radius ring + influence particles) would **render a field where the
   game shows a crowd** — a Step-2-visible consequence, which the other five do not have.
2. **Negative result, banked (X005): `self_buff` is CLEAN — 0 of 6 nominated rows.** The obvious next
   hypothesis is that FIELD-CARRIED archetypes generally absorb summon shapes. **Tested and refuted.**
   Every `self_buff` hit is a deliberate, correctly-reasoned separation of the *activation handle*
   from the summoned consequence — `poe1-generals-cry#0` says it outright: *"the cry itself is a
   self-origin proc-trigger… self_buff = the warcry activation handle; the summoned warriors carry
   the offense."* **This is not a general field-archetype defect.** It is specific to `aura`, and
   specifically to the case where the delegate bodies **are themselves the emitting surface** — the
   one case `self_buff`'s activation-handle convention never has to face.
3. **The lexicon scan is unreliable in both directions (X006), and L-39's regex caution was well
   placed.** A summon lexicon nominated 8 rows: hand-reading confirmed 3 and rejected 4 as false
   positives (`di-blood-knight` — *"Swarm of Bats"* is the **essence name**; `tq-trap-magician` —
   pets are the buff **target**, not the emitter; etc.). It also **missed 3 of the 6 confirmed rows**,
   recovered only by reading the full 73-row cell by eye. **Precision 3/8 = 37.5%, recall 3/6 = 50%.**
   Anyone re-running a lexicon on this cell should expect it to both over- and under-count.

**The axis these rows differ on is EMITTER ANCHOR** (caster-centred / world-placed / delegate-bound),
which the `aura` gloss does not test for and therefore cannot catch. Input to the next kit-mapping
lap; folds naturally into the F-2 re-mapping lap (§ 6.3).

### Findings landed (13 rows, `curation_run='vfx-x4-materialization-2026-08-24'`)

| id | kind | sev |
|---|---|---|
| X001 | `emitter-anchor-mis-attestation` (summary of record) | WARN |
| X002 | sub-shape A, placed/world-anchored, n=4 | WARN |
| X003 | sub-shape B, delegate-carried, n=2 | WARN |
| X004 | `contradictory-cross-kit-attestation` (Machine Army) | WARN |
| X005 | `negative-result` — `self_buff` control is clean | INFO |
| X006 | `method-note` — precision/recall of the lexicon scan | INFO |
| X007 | `derivation-count-discrepancy` — 1,134 vs 1,135 | WARN |
| X010–X015 | `emitter-anchor-row` — per-row evidence, one per confirmed row | INFO |

Every finding carries its own evidence verbatim from the row's `delivery_notes`, per the
source-anchored + no-silent-transformation rules.

---

## Reversibility, safety, iron laws

- **Backup of record:** `corpus.db.pre-vfx-x4-20260824-backup`
  (md5 `5831c8bff5d1b50dc4fd2b0cd96c35c8`, `integrity_check=ok`), md5 pinned in
  `corpus.db.pre-vfx-x4-20260824-backup.md5.txt`.
- **Proven on a throwaway copy BEFORE the live apply**, including the differential digests below.
- **Iron law 1 — `vfx_archetype_member` untouched.** 11-column, 1,158-row ordered digest is
  **byte-identical** to the backup: `008b60d7abc9824f…`
- **Iron law 2 — no pre-existing `vfx_archetype` column mutated.** 21-column, 27-row ordered digest
  over the original columns only is **byte-identical**: `e0643aacf423117e…`
- **Transactional + idempotent** — single `BEGIN`/`COMMIT`, rollback on any assert failure; verified
  by a second live re-run producing identical POST-state.
- **Asserts at commit time:** PRE-state (27 / 1,158 / 1,138 / 1,135) · POST-state (all 10 counts
  above) · losslessness (NOT-EXISTS) · recoverability (no folded row without a layer flag) ·
  HELD-is-not-a-fold · bridge reciprocity · `27 = 24 + 2 + 1`.
- **Rollback:** `cp corpus.db.pre-vfx-x4-20260824-backup corpus.db`. Or non-destructively:
  `DROP VIEW v_vfx_kit_skill_binding` + `DELETE FROM vfx_curation_finding WHERE
  curation_run='vfx-x4-materialization-2026-08-24'`; the six columns are inert if unread.

## Cross-seam

**No engine-side change. Star-lord's engine `MIGRATION.md` files are unaffected** — `corpus.db` is
elrond's seam and the engine does not read it. Engine telemetry was not touched (read-only to me).

**Owed outward:** X007 (the 1,134/1,135 editorial correction) → **gandalf** via KR. The `aura`
finding → next kit-mapping lap (elrond), naturally folded into the F-2 re-mapping lap.

## Script

`../scripts/vfx_x4_materialization_2026_08_24.py` — transactional, idempotent, assert-guarded.

Auto-committed per project discipline (dispatch-authorized). **NO push.**
