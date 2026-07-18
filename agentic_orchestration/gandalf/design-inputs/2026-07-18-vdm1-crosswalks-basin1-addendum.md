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

## §D — hades2 rows (attested b04, LANDED 2026-07-18)

| Source mechanism (fetched language) | Engine lane | Notes |
|---|---|---|
| **Magick** ("channel +30 additional Magick"; "Magick bar drains on use" — omega-magick, glorious-disaster) | cast-cost resource, mana-register | plain spend/channel pool. NOT reservation, NOT anything engine-magic-adjacent |
| **God boons** (Zeus/Apollo/Demeter/Hephaestus/Ares lineages) | supports→5-lane by what the boon DOES | Volcanic Strike on-attack blast → proc/trigger lane · Ice Strike freeze-on-hit → ailment-granting · Cold Storage duration → param lane |
| **Duo boons** (Glorious Disaster, Hail Storm) | capstone-class combo identity → t4_doors | the duo IS the kit's capstone; route via main-law §5 |
| **Weapon Aspects** (Circe, Medea) + **keepsakes** | capstone/item lanes | aspect = the kit's item-alteration analog |
| **Omega charge-release** ("Hold any attack input to charge Omega variant") | channel/charge economy + geometry per Omega type | Omega Cast "large AoE around Melinoë, explodes after brief period" → self-origin delayed nova (circle/nova + delay note) |
| **Freeze→lightning conversion** ("Freeze at enemy position triggers lightning bolt at that location" — hail-storm) | trigger_grammar: proc_trigger_condition on-ailment-apply | native trigger grammar; NOT a meta-gem chassis (R-M9 not needed) |
| **Winter Harvest** (low-HP frozen enemy explosions) | freeze + execute rows | threshold-burst native |
| **Static Shock armor removal** | sunder (hit-proc shape) | main-law exposure row |
| **Throw-retrieve ammo loop** ("throws shells that explode on hit; special is a lunge that retrieves them" — medea-skull) | approximate projectile + note | accrual candidate to the **out-and-return family** (mint-candidate: spectral-throw class) — retrieve is a second ACTION, not auto-return; file accrual WITHOUT number |
| **Hexes** | — | null-attested in fetched text; no row (§0 rule) |

## §E — tq2 rows (attested b04, LANDED 2026-07-18)

| Source mechanism (fetched language) | Engine lane | Notes |
|---|---|---|
| **Dual-mastery class identity** ("Storm+Earth dual mastery (class name: Elementalist)") | BOTH masteries' capstones route t4_doors; the PAIRING is the class identity | ⚠ corpus class-fields for elementalist/stormblade/whirlwind were kb-WRONG (ingest-9 adjudication) — map from the VERIFIED mastery pair, not the corpus class column |
| **Energy** ("high energy cost") | cast-cost resource | plain pool |
| **Reserved-energy damage scaling** ("Ice Shards… damage scales with reserved energy" — stormblade) | reservation_percent + damage-coupling fidelity_note | WATCH-ITEM: reservation-as-damage-scaler coupling — if no economy key expresses it, candidate |
| **Armor-conversion damage** ("Shield Attack (overwrites damage source to current armor)"; "Armor Eruption (converts all armor to AoE damage)" — bastion-tank) | approximate + note | accrual candidate ADJACENT to docket #4 stun-as-damage-substrate — armor→damage is a DISTINCT stat-as-damage-substrate mechanism; file its own candidate, do not merge |
| **Amplify/Overload stacks** (Roiling Magma) | accumulator | single-tier native |
| **Sentries/traps placement** ("Sentries: placed at target location, fire at enemies in range (autonomous); traps stack up to 8" — forge-turrets) | `totem`-class placed-proxy geometry (PoE1 minion-swarm precedent) + placed-proxy count economy | count-8 → accrual candidate to the placed-proxy-count family (hiero-6-totem mint class); WITHOUT number |
| **Homing projectiles** ("9 shards per cast; homing behavior" — ice-shards) | projectile + pursuit note per R-M8 | homing = behavioral delta (delivery flavor), NOT identity void; 9-count → projectile-count economy |
| **Mobile channel spin** ("mobile during the channel (only skill where you can keep moving while using it)" — whirlwind) | mirror poe1-sweep/cyclone-class spin precedent — query `kit_mapping` for the PoE1 spin geometry token | mobility-while-channeling in fidelity_note |
| **Rage** (whirlwind "Builds Rage fast") | accumulator | |

---
**Lifecycle:** steward extends §A/§B/§D/§E at each audit if new statuses attest. §D/§E LANDED from b04 fetched language — **all basin-1 mapping batches (m01-m04) may fire** once their kits' dossiers are ingested (m01-m02 gate: ingest-8 ✓ · m03-m04 gate: ingest-9).
