# Re-key prep — ELEM slot (design session #6) — MAPPING QUEUED, OPTIONS ONLY

**Date:** 2026-07-12 · gandalf (mechanical prep) · Spec: `corpus-rekey-spec-v1.md` §2 — elem (17 codes) RETIRES → raw descriptor; engine target = **8-element mapping (QUEUED Matt ruling)**. **Per brief: present OPTIONS only. Resolving the 8-element mapping here is the failure mode.**

## 1. Corpus element frequency (v3 CSV canon positives, n=478)

| code | element | n | | code | element | n |
|---|---|---|---|---|---|---|
| PH | physical | 151 | | HO | holy | 11 |
| FI | fire | 73 | | SH | shadow | 10 |
| __ | none/unknown | 72 | | VI | vitality | 7 |
| LI | lightning | 53 | | PI | pierce | 5 |
| CO | cold/frost | 38 | | AE | aether | 4 |
| CH | chaos | 21 | | NE | necrotic | 4 |
| PO | poison | 14 | | MA | magic | 4 · AC acid 3 · VO void 3 · AR arcane 3 · BL bleed 2 |

**~17 damage types** in the corpus (decoded via `code_elem`). Raw-residue confirmed: NE=necrotic, MA=magic, AC=acid, VO=void.

## 2. Engine vocabulary of record — the locked 8

Source: `generation/season_generation_pipeline.py::STAT_ELEMENT_POOLS` + `config/elements.yaml`. **The 8 are LOCKED:** `fire · water · earth · wind · lightning · holy · shadow · physical`. Attribute pools: INT→{fire,water,lightning,shadow} · WIS→{earth,wind,holy} · STR→{physical} · DEX→all 8. Locked drift-guard: **`flavor element`** = thematic variant of a primary `canonical_element` (pure naming/visual; does NOT change damage_scaling / affinity / resistance).

## 3. The asymmetry (the reason this is a real ruling, not a lookup)

- **Clean 1:1 (5 of 8):** fire→fire · lightning→lightning · holy→holy · shadow→shadow · physical→physical.
- **Engine elements with NO clean corpus code (3 of 8):** `water`, `earth`, `wind` — the entire WIS pool minus holy. The corpus (D2/PoE-shaped) barely codes earth/wind as damage types; it uses physical/nature instead. **RDR's WIS elemental identity is genre-thin — coherent with the WIS med/var whitespace in census §3.**
- **Corpus elements with NO engine slot (~9):** chaos(21) · poison(14) · vitality(7) · aether(4) · necrotic(4) · magic(4) · acid(3) · void(3) · arcane(3) · bleed(2) · pierce(5). Plus cold/frost(38) which the engine folds into water.

## 4. Options for the QUEUED ruling (Matt rules — NOT resolved here)

**Option A — flavor-element absorption (the locked mechanism does the work).** Map each surplus corpus element to a primary-8 element as a *flavor variant* (naming/visual only, damage_scaling inherited):
- cold/frost → **water**-flavor · chaos/void/necrotic → **shadow**-flavor · poison/acid → **shadow**- or **earth**-flavor · arcane/aether/magic → **lightning**- or **fire**-flavor · vitality → **holy**-flavor · bleed/pierce → **physical**-flavor.
- *Pro:* uses the already-locked flavor-element layer; keeps the 8 intact; genre-honest (PoE's "chaos" is mechanically shadow-like DoT). *Con:* poison-as-flavor loses poison's DoT identity unless the damage_scaling_type carries it (poison is a *mechanic* as much as an element — see Fork).

**Option B — collapse-to-nearest (hard 8-way key, no flavor layer).** Force every corpus element into one of 8 at key time; discard the surplus label. *Pro:* simplest key. *Con:* throws away thematic data the flavor layer could keep; irreversible.

**Option C — surplus-signals-insufficiency.** Treat the ~9 unmapped corpus elements as evidence the locked-8 is too thin for full genre coverage. *Blocked:* the 8 is LOCKED (drift-guard); this option reopens a closed decision — flag only, do not pursue without explicit Matt reopening.

## 5. Open forks (UNRESOLVED — Matt rules)

- **Fork EL1 — is poison an element or a mechanic?** Poison (14 kits) + acid + bleed are DoT-mechanics as much as damage-types. Under Option A they'd be flavor of shadow/earth/physical, but their *identity* is the damage-over-time economy (econ=dot-walk, DW). **Genre precedent:** PoE splits Chaos (element) from Poison (ailment); D3 poison is its own resist; GD has a full Vitality/Bleed/Acid resist table. **The element ruling and the ailment/econ ruling are coupled for these three.** Lean is NOT offered — this is a genuine Matt fork spanning elem + econ.
- **Fork EL2 — cold=water, or cold as water-flavor?** 38 corpus cold kits. (a) cold IS water (rename at key). (b) cold is a *flavor* of water (chill/freeze visual, water scaling). **Genre precedent:** most ARPGs call it cold/frost/ice, none call it "water" — RDR's "water" is already the outlier name. Lean deferred to Matt (naming register call).
- **Fork EL3 — the WIS-element thinness.** earth/wind have near-zero corpus attestation as damage. Is RDR's WIS-elemental identity (earth/wind) a deliberate frontier (census §3 med/var fork, reading a), or does it signal the WIS pool needs re-examination? **Empirical resolution:** batch-2 WIS-kit fingerprints. Do not rule pre-substrate.
- **Residue for legolas:** NE/MA/AC/VO (~14 kits) are raw-fallback codes — a Mode-A re-characterization probe would confirm their intended canonical element before any mapping locks.
