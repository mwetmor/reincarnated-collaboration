# Re-key prep — CTRL slot (design session #2)

**Date:** 2026-07-12 · gandalf (mechanical prep; **elicits, does not rule**) · Spec: `corpus-rekey-spec-v1.md` §2 — ctrl RETIRES → raw descriptor; engine target = **role-orientation taxonomy** (damage / support / control / hybrid, 2026-05-08).

## 1. Corpus code frequency (v3 CSV canon positives, n=478)

| code | meaning | count | % |
|---|---|---|---|
| D | damage | 333 | 70% |
| M | mixed | 123 | 26% |
| _ | unspec | 17 | 4% |
| C | control-pure | 5 | 1% |

**3 live codes.** (decoded via generator `code_ctrl`.)

## 2. Engine vocabulary of record — role-orientation

Source: `foundation/substrate_identity_loader.py::CANONICAL_ROLES = {"damage", "support", "control", "hybrid"}` (all 4 required; validated). Also `gear_generation.py::_ALL_ROLE_ORIENTATIONS`.

## 3. PROPOSED mapping (corpus → engine) + residue

| corpus | → engine role | confidence | note |
|---|---|---|---|
| D damage | `damage` | HIGH | 1:1 |
| C control-pure | `control` | HIGH | 1:1 (but only 5 corpus kits) |
| M mixed | `hybrid` OR `damage`+control-ailments | MED | **ambiguous — see Fork C1** |
| _ unspec | (unmappable) | — | drop / probe |

**Residue — engine role with NO corpus code:** `support`. The corpus never coded a support kit (control-pure=5, no support at all). Engine's 4th orientation has ZERO corpus attestation.

## 4. Open forks (UNRESOLVED — Matt rules)

- **Fork C1 — what is corpus "mixed" (26%, 123 kits)?** Two readings: (a) mixed = engine `hybrid` (dual-role: damage+support or dual-element); (b) mixed = a damage kit that also applies control ailments — which the engine would key as `damage` with an element-application rider, NOT as a separate orientation. **These map to DIFFERENT engine slots.** Genre precedent: most ARPG "mixed" kits (D2 Blizzard-Sorc, PoE Cold-snap) are *damage kits that chill* — orientation=damage, control is a side effect. True role-hybrids (D4 support-Necro, PoE aura-carry) are rarer. **Lean:** corpus "mixed" is mostly (b) → re-key mixed→`damage` with a `control_rider` flag, reserving `hybrid` for genuine dual-role. But this is a 123-kit ruling — Matt should eyeball a sample.
- **Fork C2 — is `support` genre-rare or a corpus blindspot?** Zero corpus support kits. Either (a) solo-ARPG canon genuinely has almost no pure-support builds (support = party-play PoE aura-bots, MF-cullers — a multiplayer artifact), or (b) the crawl under-sampled them. **Genre precedent** leans (a): D2/D3/D4/GD single-player builds are damage-or-control; pure support only emerges in group PoE. Since RDR is **solo gameplay only** (confirmed design intent), a near-empty support orientation may be *correct for the frame*. **Lean:** accept support as genre-thin; do not force corpus kits into it. Flag for Matt whether `support` should even be a generated orientation in a solo game, or a T4-door flavor.

## 5. RULINGS (Matt 2026-07-12 — session batch, ruling 2 of 6)

- **C0 — dissolved into the probe** (gandalf over-ask, owned: D→`damage` and C→`control` are 1:1 ratifications, not forks; presenting them as a ruling was noise). Provisional mapping stands; the mega-probe re-verifies per-kit anyway.
- **C1 — probe resolves** (Matt: *"I cannot know what mixed is as Claude from Mobile derived it. Probably, it meant (b), but re-probe is needed to resolve."*). **Prior registered = (b)** damage + control-rider; the probe collects per-kit control-application facts (ailments + centrality); mapping applies kit-by-kit post-probe. No blanket re-key of the 123.
- **C2 — RULED: support accepted as genre-thin** (Matt: *"Yes"*). **Post-probe decision registered:** if the probe's pure-support existence sweep confirms zero solo-context support canon, Matt either (i) leaves `support` at 0 kits or (ii) **retires the `support` label from the engine role-orientation taxonomy** — an amendment to the locked 2026-05-08 taxonomy, empirically gated on probe results (recognition → validate → commit shape). Probe carries a directed support-existence sweep.
