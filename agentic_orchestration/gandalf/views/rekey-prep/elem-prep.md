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

## 6. RULINGS (Matt 2026-07-12 — session batch, rulings 5–6 of 6)

- **EL-mech — NEITHER A nor B. RULED: there is NO corpus→engine element mapping table, ever.** Matt verbatim: *"we will allow the pipeline to determine the elements and the LLM to determine the flavor elements when the API is called for naming. This is a flavor only call and it can simply be disregarded."* Consequences: `elem_raw` is **provenance-only, permanently** (not awaiting-rekey — no mapping is coming; elrond ingest schema should mark it so). **Element is a FREE AXIS in the rebuild** — a genre kit's element label is not part of its lineage identity; the pipeline assigns element at generation; the LLM naming call flavors it (disregardable). The corpus's own convergence structure anticipated this: V2's elem-masked rung (V5 fold) is where cross-game convergence lives — the genre itself converges on mechanics with element rotated out.
- **EL2 — RULED: engine element `water` RENAMES to `ice`, and the cold/frost AILMENT is adopted.** Matt verbatim: *"let's change our water element to Ice and adopt the cold/frost ailment. The genre's corpus has spoken."* The locked-8 amends (substrate-led) to **fire · ice · earth · wind · lightning · holy · shadow · physical**; INT pool reads {fire, ice, lightning, shadow} — the classic mage quartet. Matt's aside recorded: corpus cold kits are NOT pinned to Ice at emission — *"if we run enough iterations across time, we will see these kits in their Ice Elemental version"* (the free-axis law again). **Engine implementation routed rocket via KR** (elements.yaml · STAT_ELEMENT_POOLS · element-name vocab pools — note `rime`'s prior demotion may warrant revisit under an ice register · resistance/ailment surfaces gamora-adjacent). Design adjacency flagged: the DEFERRED thematic-ailment-signatures proposal (water cold-burn) now has a ruled anchor — chill/freeze as ice's control ailment.
- **EL1 — DISSOLVED by EL-mech.** With no element mapping, poison's label is provenance; its DoT nature is captured by the probe's `damage_mode` + econ dot-walk facts. Residual question (does the ENGINE want a poison-family DoT ailment?) routes to ailment-layer design (with the thematic-ailment-signatures proposal), not re-key.
- **EL3 — unchanged:** WIS-element thinness stays empirically gated on batch-2 WIS fingerprints.
