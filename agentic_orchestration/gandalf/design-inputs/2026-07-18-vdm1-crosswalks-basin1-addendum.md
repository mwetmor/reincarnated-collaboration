# VDM-1 crosswalks — basin-1 (post-cutoff) addendum

> **Authored 2026-07-18, gandalf (steward, SPEC-AUTHOR).** EXTENDS `2026-07-18-vdm1-crosswalks.md` (THE LAW) for the poe2/hades2/tq2 basin. Where this doc is silent, the main law governs unchanged. **§0 attestation rule:** every row here is grounded in basin-1 FETCHED dossier language (batch cited) — never memory of post-cutoff games. A mapper hitting a source status/mechanic covered by NEITHER doc files it to the steward in the batch summary; do not improvise a row (Despair-b01 lesson).

## §A — PoE2 ailment/status rows (attested b01-b02)

| Source status (fetched language) | Engine ailment | Trap notes |
|---|---|---|
| poe2 **Impale** ("Impale debuff from shard hits amplifies subsequent attack damage" — bonestorm b01) | **sunder** | same reasoning as PoE1 shock→sunder: hit-applied damage-taken amp window. NOT bleed (no DoT component in fetched text) |
| poe2 **armour break** ("Armour Piercing Rounds" — galvanic-shards b01) | **sunder** (hit-proc) | main-law exposure row governs: hit-proc window → sunder; only aura/hex-shaped shred → curse:sap |
| poe2 **Time Freeze** ("stopping time for all enemies for 3 seconds" — chronomancer b01) | **stun** (mass, duration-capped) + fidelity_note | NOT freeze — freeze is cold-thematic shatter-carrier; time-stop is element-neutral hard CC. Approximation, note the flavor loss |
| poe2 **aggravated Bleed** (rake-ritualist b02) | **bleed** | variant magnitude in param_ranges; no new ailment |
| poe2 **Ignite / Poison / Freeze / Shock** | per main law | unchanged from PoE1 rows (incl. shock→sunder FALSE FRIEND — verify per-kit whether fetched text means damage-amp or arc-CC before routing) |

**Un-attested so far (do NOT map from memory):** electrocute, pin. If b03/b04 fetched text surfaces them, steward adds rows at audit.

## §B — PoE2 resource/economy rows (attested b01-b02)

| Source mechanism | Engine lane | Notes |
|---|---|---|
| **Spirit reservation** ("Reserve 30 Spirit" grim-feast; "Reserve Spirit to maintain minions" infernal-legion, minion-infernalist — b02) | `reservation_resource: spirit` + reservation_percent/flat | ⚠ FALSE FRIEND: poe2 Spirit is a RESERVATION POOL. It has NOTHING to do with the engine's spirit-guide system — never route Spirit-reserving kits toward spirit_guide surfaces |
| **Combo Points / Power Charges finisher** ("build Combo Points (up to 4). Release… finisher spending" — ice-strike-invoker b02) | accumulator economy keys + trigger_grammar `consequence_type: spend-burst` | PoE1 charge precedent carries; builder-spender shape is native |
| **Weapon Heat** (smith-ignite b02) · **Rage** (shaman-bear b02) | accumulator | single-tier: native |
| **Rage→Glory two-tier accumulator** ("At max Rage, additional generation builds Glory. Glory cap triggers Walking Calamity" — shaman-bear b02) | approximate as ONE accumulator + threshold-proc; fidelity_note the second tier | WATCH-ITEM: 2nd two-tier-accumulator accrual anywhere in basin-1+ → qualitative mint-candidate question (steward counts; do not number accruals) |
| **ES overleech above max** ("healing above max life to 150%" blood-mage b01; ES-overleech-above-cap grim-feast b02) | nearest overheal/leech economy keys + note | WATCH-ITEM: overheal-above-cap class — if no economy key expresses above-cap buffer, file docket-candidate (steward consolidates) |
| **Cooldown-reset burst** ("Time Snap: resets all ability cooldowns" — chronomancer b01) | cooldown/recovery economy keys if expressible; else docket-candidate | do not silently drop — this IS the kit's loop (Snap resets Freeze) |
| **Demonflame ramp + life-drain-in-form** (demon-form b01) | hp_cost_scale-class self-damage + accumulator | hp_cost_scale 0.30 ceiling LOCKED — clamp + note if source rate exceeds; accrues to the standing review-book clamp list |
| **Life-remnant kill-vacuum** (blood-mage b01, grim-feast b02) | on-kill recovery economy keys | kill-harvest loop; map to nearest on_kill key, note the pickup-radius flavor |
| **Attribute-stacking → flat damage** (HoWA howa-invoker/gemling-stacker b02) | trait/affix lanes + economy; fidelity_note | NOT an accrual to docket #8 (siege-ballista is stat→proxy-COUNT; HoWA is stat→damage — different mechanism). If gapped, file as its own candidate |

## §C — PoE2 mapping guidance (binding for basin-1 mapping batches)

1. **Form-swap kits (demon-form, shaman-bear):** map the in-form kit per R-M rules; form-ENTRY itself is the GX-02 form-swap gate class — flag `GX-02` in fidelity_notes (steward accrues to the standing 10-flag register; do not number).
2. **Meta-gem triggers (Cast on Freeze — cof-comet b01):** R-M9 carries directly — geometry `self_buff`, chassis in trigger_grammar, note. MAX_CHAIN_DEPTH=1 still LOCKED.
3. **Timed-release channels (Perfect Timing window — perfect-strike b02):** skill-NATIVE timing window, NOT a proc window — do NOT emit the R-M5 accrual token (whispering-ice precedent; write "R-M5 considered, not applicable" without the literal token).
4. **Two-stage geometries (gas-arrow cloud→detonate b01 · frostbolt→Comet b01 · galvanic fragments→beams b01 · lightning-spear impact-fanout b02):** main-law §7.2 dominant-loop rule governs — the geometry is what the player does every 3 seconds; note the alternative stage. R-M6 (drift-tick orb → circle + note) carries.
5. **Dash-to-target (Rake b02):** follow the PoE1 flicker-strike precedent — query `kit_mapping` for poe1-flicker's geometry_value and mirror its shape; note the bleed-builder difference.
6. **poe2-erasure-edc-lich:** "Erasure" is a PHANTOM-MECHANIC candidate (404 on poe2db, absent all fetched sources; elrond investigating). Map from Essence Drain + Contagion ONLY; fidelity_note the phantom; grade as if Erasure does not exist.
7. **poe2-grim-feast:** identity = the 0.2-dawn ES-overleech variant (era adjudication ingest-8); map THAT identity, not the post-0.3 rework.
8. **poe2-archmage-totems:** the 3-way combo is single-source-unconfirmed (conf 0.45) — map components per dossier, fidelity_note the joint-attestation weakness.
9. **Ascendancy → t4_doors:** poe2 ascendancy notables route via main-law §5 exactly as PoE1 ascendancies did (capstone identity → 1-3 ENGINE tokens; R-M1 vocabulary law).

## §D — hades2 rows — **PENDING batch-04 fetched language** (do not map hades2 kits before this section lands)

## §E — tq2 rows — **PENDING batch-04 fetched language** (do not map tq2 kits before this section lands)

---
**Lifecycle:** steward extends §A/§B at each crawl-batch audit if new statuses attest; §D/§E land after b04 recount. Mapping batches for poe2 kits (m01-m03) may fire once ingest-8 lands; the b04 mixed batch maps only after §D/§E.
