# Returns adjudication — Elrond S1 + Legolas mint dossiers (2026-07-13)

Gandalf steward adjudication of the two commissions. Rulings below are steward-authority; the one Matt-gated item is flagged.

---

## Elrond — S1 corpus data-completion (schema_meta 2.0 → 2.1, commit `feb69650`)

**ACCEPTED.** One idempotent rebuild, five payloads, zero row-count change (524 / 4,780 / 478 / 45 hold). Cone Path-2 split reproduces (5 BEAM / 6 PROJECTILE). V1.2 plane render reproduces from rebuilt DB.

### Ratifications (mine)
- **Finding 3 — stabilization_patch source scope:** signal lives in `eras` (10 tokens), not `sources_used` (1); extractor unions both. **RATIFIED** — unioning both is correct steward scope.
- **Finding 4 — chronicon era-year discrepancy** (era_range 2020 vs release_era 2021; Elrond chose 2020): **RATIFIED 2020** (era_range is the more specific canonical signal). Low stakes; revisable if Matt objects.

### Absorbed pipeline correction (Findings 1 + 2) — MATERIAL
- `roster commit_val`: 5/45 filled (K1/K7/K19 CellDef pins + B12/H6 explicit); **40 NULL because commit is rolled at generation (S7), not a static S1 column.** My commission premise was wrong.
- `roster mob_policy`: **0/45 — movement is emitted per-skill at S7; there is no S1 source of record.** Also contradicts commission premise.
- **Consequence for the atlas plane:** the **45-kit roster overlay cannot be placed on the movement axis until S7 emits per-skill movement** (or we derive a roster-level movement summary). Today the plane is populated by the **corpus** (478 engine_key rows with `mob_policy_while_casting`); the roster overlay renders **UNMAPPED** on movement. This is not a bug — it is a real S7-dependency.
  - **Seam item logged:** the mouseover Phase-2 roster dots need movement values → gated on S7 emission (or a derived summary). Adds to the two existing Phase-2 gates (gandalf per-dot JSON + public_label; elrond era_year/patch — now landed via P5).

### Render-spec amendment (mine, non-urgent)
`render_v1_2_stratified.py` may now read the **keyed `engine_key.delivery_value` column** directly instead of re-parsing the delivery JSON. Apply on next renderer touch — D6 single-source alignment. Render reproduces correctly either way, so no rush.

### Push
Committed, not pushed (awaiting Matt/KR authorization). Standing.

---

## Legolas — 9 mint dossiers + URL backfill (commit `aaa519d6`)

### CORRECTION AUTHORIZED (→ elrond curation)
- **`poe1-ring-of-shields` → `le-ring-of-shields`.** Game-attribution error, confirmed 2-source (lastepoch.fandom.com + lastepochtools.com): this is a Last Epoch Sentinel→Forge Guard skill, not PoE1. **kit_id + game field correct poe1 → le.**
  - **Consequence:** the poe1 totem-hole closure now rests **solely on `poe1-totem-hierophant`** (dossier 01 confirms Ancestral Warchief / Hierophant, 2016 — legitimately poe1). Still covered, thinner than assumed.
  - Ring-of-shields moves to the LE column → **LE proxy/summon coverage is now strong** (Falconer + Shift Bladedancer + Ring of Shields).

### RECONCILE ruling (→ elrond)
- **`d3-call-of-the-ancients` vs any existing `d3-ik-hota`: RULED DISTINCT — both stand.** CotA = summon-3-ancients (proxy-economy exhibit, Wave-A relevant); IK-HotA = melee slam. Shared Immortal King set is **not** a dedup trigger — different skill, different delivery, different plane address.

### Ratifications (mine)
- **`d3-dashing-strike-monk`: NOT negative-canon** (agree with Legolas — archetype is genre-real; durable descendants, e.g. LE Shift Bladedancer).
- **`poe1-vaal-blade-vortex` stabilization_patch NULL** (PoE wiki 403): honest-NULL accepted.
- **URL-backfill manifest:** accepted.

### SURFACED to Matt (steward lean, Matt rules)
- **`d2-sacrifice` negative-canon flag.** Never meta-viable; founding self-cost melee archetype; GX-06 evidential value; D2R v2.4 reduced self-damage scaling.
  - **Gandalf lean: KEEP + annotate as historical-exhibit (negative-canon), ship in the dev log.** For a veteran-gamer dev-log audience, negative-canon exhibits carry value — they show the genre's designed dead-ends. Annotate as **not a balance target** (excluded from S6 certification population), but present in the catalogue. Matt's ruling.

### Standing collection note
- **PoE wiki 403 (bot-blocked)** is a recurring Mode-A/B limitation. Non-blocking; flagged so downstream expects PoE-wiki-sourced fields to lean NULL.

---

## Routing summary
- **→ elrond (data corrections, next cycle):** (1) `poe1-ring-of-shields` → `le-ring-of-shields`; (2) CotA/IK-HotA distinct — no dedup; (3) ingest the 9 dossier era_year/patch + URL backfill.
- **→ Matt (1 ruling):** `d2-sacrifice` negative-canon keep/annotate (lean: keep).
- **→ gandalf (mine, queued):** render-spec keyed-column amendment; roster-movement S7-dependency logged into Phase-2 mouseover gates.
- **→ push:** elrond `feb69650` + legolas `aaa519d6` await Matt/KR push authorization.
