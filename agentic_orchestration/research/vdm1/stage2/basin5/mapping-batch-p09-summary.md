# VDM-1 basin-5 mapping batch-p09 summary — vs-b (11 kits)

**Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR) · **Cluster:** Vampire Survivors batch-b

---

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | vs-thousand-edge · vs-unholy-vespers |
| CLOSE | 5 | vs-phieraggi · vs-runetracer-no-future · vs-soul-eater · vs-thunder-loop · vs-vandalier |
| APPROX | 0 | — |
| GAPPED | 4 | vs-out-of-bounds-freeze · vs-queen-sigma · vs-red-death · vs-vlad-dracula |

---

## Per-kit one-liners

| kit_id | Grade | One-liner |
|---|---|---|
| vs-out-of-bounds-freeze | GAPPED | Arcana-slot freeze-weapon loadout modifier; no rotation; freeze ailment kept (VS enemy-status exception); MAPPED_DOCKET |
| vs-phieraggi | CLOSE | Rotating laser orbit ring; revive-stock-as-power economy (RESOURCE_CONVERSION); no element |
| vs-queen-sigma | GAPPED | Collection-completion character; infinite per-level Might/Growth ramp; no rotation; MAPPED_DOCKET |
| vs-red-death | GAPPED | Max-speed orbit character; Death Spiral ring; no rotation; MAPPED_DOCKET |
| vs-runetracer-no-future | CLOSE | Wall-bounce ricochet with explosion cascade; Armor scales explosion; GEOMETRY_PROPAGATION_cascade |
| vs-soul-eater | CLOSE | Body-adjacent circle aura; HP-healed-to-damage ramp; drain ailment; PERSISTENCE_ENGINE_saturation |
| vs-thousand-edge | EXACT | Movement-vector aimed knife stream; multi_projectile; no element; GEOMETRY_INVERSION door |
| vs-thunder-loop | CLOSE | Random-target lightning double-hit; 'thunder/lightning' NAME-ONLY → null; no ailments attested |
| vs-unholy-vespers | EXACT | Clockwise orbit ring; Duration-scaling uptime; 'Unholy' NAME-ONLY → null; PERSISTENCE_ENGINE_uptime |
| vs-vandalier | CLOSE | Companion bird + dual bomb-zone orbit; slot liberation; DUAL_PROXY; no element |
| vs-vlad-dracula | GAPPED | DLC character; damage-cap-at-10 + Curse-as-Might inversion; Wine Glass geometry unattested; MAPPED_DOCKET |

---

## T4-door frequency

| T4 door | Count | Kits |
|---|---|---|
| PERSISTENCE_ENGINE_saturation | 2 | vs-out-of-bounds-freeze · vs-soul-eater |
| PERSISTENCE_ENGINE_uptime | 1 | vs-unholy-vespers |
| RESOURCE_CONVERSION | 1 | vs-phieraggi |
| MOMENTUM_CASCADE | 1 | vs-queen-sigma |
| PHASE_MOMENTUM | 1 | vs-red-death |
| GEOMETRY_PROPAGATION_cascade | 1 | vs-runetracer-no-future |
| GEOMETRY_INVERSION | 1 | vs-thousand-edge |
| DUAL_PROXY | 1 | vs-vandalier |
| DEFENSIVE_TRADEOFF | 1 | vs-vlad-dracula |
| (none) | 1 | vs-thunder-loop |

---

## §0 near-misses — elements/statuses WANTED but could not attest

- **vs-thunder-loop "lightning"**: wanted to emit lightning (the weapon is literally Thunder Loop, fires lightning strikes). Could not: VS has no elemental damage-type system; 'lightning' applies as delivery-flavor name, not a damage-type descriptor on a generic effect noun. NAME-ONLY STRIKE per VS element law. Element = null.
- **vs-unholy-vespers "holy/unholy"**: wanted to emit shadow or holy (thematically "unholy"). Could not: 'Unholy Vespers' is a proper weapon name; no damage-type descriptor on a generic effect noun attested. NAME-ONLY STRIKE. Element = null.
- **vs-vandalier "multicolored"**: no element candidate — correctly silent.
- **vs-phieraggi "blue lasers"**: wanted to consider whether "blue" implied cold/water. Could not: color descriptor on a named weapon, not a damage-type descriptor. NAME-ONLY analog. Element = null.
- **vs-thunder-loop shock/stun**: verify_ledger mechanics verdict notes "shock/stun riders not attested in fetched text" — wanted to emit stun but no source basis.
- **vs-soul-eater "soul"**: 'soul' is thematic resource/flavor — not a shadow-type damage-type descriptor. No shadow emit.

---

## Candidates

**mint-candidates:** none generated (no novel mechanism requiring mint).

**docket-candidates:** 4 kits → MAPPED_DOCKET (see below).

---

## Docket entries summary (roguelite-park loadout structures)

All 4 GAPPED kits are structural roguelite-park dockets:

1. **vs-out-of-bounds-freeze** — arcana-slot + freeze-weapon-loadout identity; mechanism_class = `arcana-slot-modifier`
2. **vs-queen-sigma** — collection-completion gate + unbounded-per-level-compounding identity; mechanism_class = `unlock-gate-compound-ramp`
3. **vs-red-death** — movement-speed-as-identity + orbit-weapon character; mechanism_class = `speed-identity-loadout`
4. **vs-vlad-dracula** — damage-cap-at-10 + Curse-as-Might-inversion economy; mechanism_class = `damage-cap-survivability-inversion`

---

## Anything forced / notable

- **vs-vlad-dracula Wine Glass geometry**: dossier probe claimed "large-zone" delivery; probe facts are ILLEGAL grounds (§0.3); emitted `single_target` as the honest minimal attested geometry. Filed in fidelity_notes.
- **vs-out-of-bounds-freeze freeze ailment KEPT**: the VS element law has one exception — genuine enemy-directed status verbs keep ("Freezing enemies generates explosions" = status verb, attested). This is the only ailment emission across all 11 kits that uses VS data as ailment ground.
- **Gatti-amari**: not in this batch (p09 roster); review-book negative candidate rides forward.
- **Append count**: 10 content appends + 2 summary appends = 12 total (≥6 contract satisfied).
