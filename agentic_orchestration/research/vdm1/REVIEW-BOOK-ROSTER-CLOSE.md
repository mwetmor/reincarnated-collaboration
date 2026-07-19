# VDM-1 REVIEW BOOK — ROSTER APPENDIX: CLOSE (347 kits)

**Generated from `kit_mapping` (readonly) 2026-07-18 · steward gandalf.** Grade meaning: engine reproduces the kit with a MINOR documented deviation; identity intact.
**Per-game:** chronicon 4 · d2 33 · d3 34 · d4 36 · di 10 · gd 23 · hades2 4 · hot 8 · la 41 · le 22 · mcd 3 · poe1 62 · poe2 27 · tl1 1 · tl2 2 · tli 5 · tq 12 · tq2 3 · undecember 5 · vs 12

---


## chronicon (4)

### chr-fire-berserker — Fire Avatar Berserker
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Fire Avatar form-swap transformation is a mode-swap-identity mechanic (GX-02) not representable in engine skill-loop without form-transition support. Burning ground DoT approximated as ground_targeted_circle; burn ailment not emitted (zone DoT vs on-enemy status distinction). Player gets a recognizable fire-explosion melee build, missing the avatar transformation peak state.

### chr-firestorm-warlock — Sun & Moon Firestorm Warlock
**CLOSE · MAPPED** · elements: fire+water · ailments: (none)
> Sun+Moon bidirectional cross-proc (fire cast → 3x frost amp for 7s; frost cast → 3x fire amp for 7s) exceeds engine trigger_grammar depth — single-direction apply-consume-pair is the best approximation; the cross-reinforcement loop is source-unique. Ritual of Souls soul-stack to 480% scaling has no direct engine analog. Player gets a fire large-AoE spam build, missing the cross-proc peak-state amplification.

### chr-fulmination-templar — Fulmination Holy Reckoning Templar
**CLOSE · MAPPED** · elements: holy+lightning · ailments: (none)
> mechanics claim UNSUPPORTED at verify; lightning element rests on dossier payload descriptor ('lightning proc events') not a direct 'deals lightning damage' anchor; player familiar with Fulmination's typed identity would recognize but the fetch language is indirect

### chr-plague-curse-warlock — Plague Mage / Desecrator Curse Warlock
**CLOSE · MAPPED** · elements: shadow · ailments: curse:amplify, fear, poison
> Era UNSUPPORTED; 'Desecration Weakness' stack mechanic (9-10x accumulator) has no direct engine analog for curse-stack depth; spirit of torment cascade spread approximated as circle; fear ailment on Spirit of Torment not attested — suppressed


## d2 (33)

### d2-auradin — Auradin
**CLOSE · MAPPED** · elements: fire+lightning · ailments: curse:sap
> Player would miss: dual-aura stack identity texture and the no-reservation free-aura economy feel; engine aura-pulse approximates but stack-doubling flavor is absent. Physical Zeal layer fully approximated. Item-dependence noted.

### d2-avenger — Avenger
**CLOSE · MAPPED** · elements: fire+lightning · ailments: curse:sap
> Player would miss: cold as third simultaneous element (mapped fire+lightning only); engine 7×7 covers two; tri-ele simultaneous feel is approximated.

### d2-berserker — Berserker
**CLOSE · MAPPED** · elements: (silent) · ailments: fear
> Player would miss: magic damage conversion (engine has no magic element family; approximated as element-neutral physical with DEFENSIVE_TRADEOFF trade); Hork loot-economy identity loop not capturable in engine scope.

### d2-bonemancer — Bonemancer
**CLOSE · MAPPED** · elements: shadow · ailments: root
> Player would miss: Bone Spirit seeking feel (engine delivers seeking via delivery_notes only; no native seeking geometry in 26-enum); Bone Prison cage shape (mapped circle; cage-wall feel partially approximated).

### d2-bowazon — Bowazon
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: IAS breakpoint identity (weapon-speed-as-identity not directly mappable; approximated via cadence_scale economy note); Strafe animation-lock feel; Valkyrie companion pet layer (GAP-noted but rider not core loop).

### d2-bvc — BvC
**CLOSE · MAPPED** · elements: (silent) · ailments: knockback
> Player would miss: PvP context (engine is solo PvE — WW mechanics map but caster-hunting purpose is context); Enigma teleport repositioning layer (item-dependent mobility).

### d2-charger — Charger
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: must-create-separation-before-recharge constraint (loop-pacing texture unique to Charge; engine dash_attack approximates but lacks re-trigger gate); Fanaticism IAS non-interaction detail.

### d2-conc-barb — Concentrate Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: uninterruptible swing feel — engine melee_strike approximates but no native 'cannot be interrupted' mechanic; the safety-vs-damage identity is approximated via DEFENSIVE_TRADEOFF T4.

### d2-daggermancer — Daggermancer
**CLOSE · MAPPED** · elements: earth · ailments: curse:amplify, poison
> Player would miss: Crushing Blow identity layer (on-kill threshold mechanic; approximated via execute T4 door note but not mapped as ailment — no fetched 'execute' language); adjacency-only melee range constraint (approximated by melee_strike geometry).

### d2-enchantress — Enchantress
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Source Enchantress wraps a buff-economy into a melee kit via oskill — the buff-recast loop and melee-strike delivery are both present, but the double-Fire-Mastery application trigger and the prebuff window are minor texture losses. Player feels 'fire melee with big buff' — that build, slightly worse.

### d2-fire-druid — Fire Druid
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Body-attached Armageddon (meteor shower that moves with caster) has no direct engine analog; circle+moving-emitter note carries it as texture rather than a distinct geometry. Player feels 'zone fire caster who walks into packs' — that build, slight delivery texture loss on the moving meteor rain.

### d2-fireclaw-wolf — Fireclaws Wolf
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Body-attached Armageddon (moving meteor circle) and form-lock are texture losses. Feral Rage→Fire Claws switch pattern approximated as self_buff prelude. Player feels 'fire melee werewolf' — that build, slight delivery texture loss on moving Armageddon.

### d2-fishyzon — Fishyzon
**CLOSE · MAPPED** · elements: lightning+water · ailments: (none)
> The javelin-lightning-arc shape of Lightning Fury (thrown javelin that spawns radiating lightning bolts) approximates as fork geometry — no exact 'thrown-projectile-spawns-radial-bolts' token. The physical javelin delivery vehicle is minor texture. Player feels 'lightning javelin thrower who freezes immunes' — that build, slight lightning-arc-spawn texture loss.

### d2-fohdin — FoHdin
**CLOSE · MAPPED** · elements: holy+lightning · ailments: curse:sap
> Holy bolt shrapnel spray as a secondary AoE element from the same cast is approximated as dual-element delivery note. Engine single_target geometry doesn't natively carry 'lightning bolt + radial shrapnel' dual-shape without delivery_notes. Player feels 'holy lightning cursor-caster with resist-shred aura' — that build, minor shrapnel-shape texture loss.

### d2-frenzy-barb — Frenzy Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical melee with speed-ramp self-buff is well-covered; minor texture loss on the dual-weapon alternating-hit feel and the 'frenzy state' escalating intensity. No ailment attestation means the on-hit bleed possibility from Gore Rider (item-layer) doesn't enter mapping_json. Player feels 'fast physical dual-wield melee brawler' — that build, slight intensity-escalation texture loss.

### d2-frost-bowazon — Frostmaiden
**CLOSE · MAPPED** · elements: water · ailments: freeze
> Pierce-enabled chain detonation (each pierced enemy independently detonates the AoE) is a geometry-multiply texture with no direct engine token; carried in delivery_notes. Player feels 'freeze-and-shatter ranged cold controller' — that build, minor pierce-chain texture loss.

### d2-frozen-orb-sorc — Frozen Orb Sorceress
**CLOSE · MAPPED** · elements: water · ailments: (none)
> The traveling-orb-that-emits-radially is approximated as orbit — the kit's defining shape (advancing emitter, not stationary orbit) is a delivery texture loss. Player feels 'cold orb sorceress who blankets areas with ice' — that build, slight advancing-vs-stationary orbit texture loss.

### d2-ghost-pvp — Ghost Assassin (WW/Trap)
**CLOSE · MAPPED** · elements: lightning+shadow · ailments: stun
> Ghost Assassin's identity fuses trap-zone control + mobility burst + CC-chain in PvP — the PvP meta-context (CC-lock dueling) is texture in fidelity_notes per engine solo-PvE scope. WW + trap combo is well-captured; minor loss on the precision positioning game of PvP dueling. Player feels 'trap-layer who teleports in and CC-bursts' — that build, PvP context excluded.

### d2-hammerdin — Hammerdin
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) hammers travel in fixed spiral paths — coverage is position-dependent, not true ring/orbit; the spiral-arc placement puzzle is mechanically distinct from a maintained orbital. Orbit token is the best available approximation.

### d2-hydra-sorc — Hydra Sorceress
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Source player would miss: the 6-turret simultaneous stacking density is the build's power multiplier; mapping captures placed-turret identity but not the specific up-to-6 count scaling texture.

### d2-kicksin — Kicksin
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Source player would miss: (1) Crushing Blow percent-HP shred is the boss-kill engine — approximated via melee_strike but the percent-HP damage mechanic has no ailment analog; (2) Mosaic runeword charge-maintenance shifts the kit from LoD to D2R identity significantly.

### d2-meteorb — Meteorb
**CLOSE · MAPPED** · elements: fire+water · ailments: (none)
> Immunity-driven tree-partition motive has no engine lane. Fireball is primary spam; Meteor is secondary burst-on-stationary — skill relative weight noted. Engine loses the 'which element do I cast now?' immunity-check loop that defined meteorb gameplay every 3 seconds.

### d2-nova-sorc — Nova Sorceress
**CLOSE · MAPPED** · elements: lightning · ailments: stun
> Source player lived inside melee range by design — proximity requirement for ring center has no engine enforcement. Stun cadence at spell speed (not melee speed) = unusual delivery feel preserved via ring geometry. Static Field percent-HP shred loses precision mapping.

### d2-poison-javazon — Poison Javazon
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Overlapping-zone stacking identity (throw to two sides simultaneously) has no engine enforcement — player spatial tactic, not a mechanic. Patient kill-confirmation loop (DoT, wait, confirm) is mood/pacing that engine captures only via DoT uptime, not timing UI.

### d2-poison-nova-necro — Poison Nova Necromancer
**CLOSE · MAPPED** · elements: shadow · ailments: curse:sap, poison
> Corpse Explosion's corpse-consumer identity loses fidelity — corpse_nodes rider note captures the gap. Immune cleanup via CE has no engine corpse-resource analogue. Engine ring geometry + DoT correctly captures Nova identity. Lower Resist → curse:sap loses the poison-resistance-specific flavor.

### d2-singer — Singer
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> Small-radius constraint (notably smaller than other War Cries) has no engine enforcement. The inversion pleasure (barbarian as caster) is player-experience texture the engine cannot encode. Engine stun + circle geometry captures the loop correctly.

### d2-smiter — Smiter
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Auto-hit guarantee (no miss chance) has no engine encoding — engine has standard accuracy model. Crushing blow percent-HP shred maps to execute threshold only approximately (execute is kill-threshold, not damage-as-percent-HP). What the source smiter player felt was the reliable-hit certainty vs uber bosses; engine misses the 'no matter what, this lands' feel.

### d2-throw-barb — Throw Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player gets ranged dual-throw weapon feel with Amplify Damage on-hit as a core tactical layer (weapon choice IS the kit); engine approximates via on-hit trigger rider. Mana leech (gear-sourced) is not a native resource key — noted as gear-mediated sustain.

### d2-wind-druid — Wind Druid
**CLOSE · MAPPED** · elements: water · ailments: chill
> Tornado's erratic wandering path is a player-skill expression unique to d2; engine circle/zone + drift note approximates the wander but loses the manual aim challenge that is the skill expression of this build.

### d2-wl-abyss — Abyss Warlock
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Abyss pull-detonate is a composite mechanic (pull + DoT + detonate) that maps to vortex_pull but loses the DoT phase between pull and detonate. Engine vortex_pull is a CC delivery; the damage-DoT-then-explode texture is fidelity loss.

### d2-wl-echoing-strike — Echoing Strike Warlock
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Echoing out-and-return path is a unique mechanical feel (double-hit line) that the engine's line geometry approximates but loses the return-pass damage texture. FCR-gated attack rate (not mana cost) as primary cadence gate is partially absorbed into economy note.

### d2-ww-sin — Whirlwind Assassin
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Claw-speed weapon-math produces different WW feel than barb version (faster claw ticks vs slower weapon pool); source player experiences this speed-math difference. Engine whirlwind geometry does not differentiate weapon-speed-math — noted as fidelity delta.

### d2-zealot — Zealot
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Commitment-lock animation (cannot cancel mid-Zeal) is the build's defining mechanical feel; engine melee_strike does not carry an animation-lock mechanic. Source player experiences this as a tactical trade; engine approximates the 5-hit flurry output without the lock consequence.


## d3 (34)

### d3-akkhan-condemn — Akkhan Condemn
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Holy element unatttested in dossier text (probe-only); player would miss the holy-damage flavor label. No ailments attested — player building ailment synergies would find none mapped. Avatar-trigger (Phalanx→Condemn) approximated via trigger_grammar; no full proxy-fidelity.

### d3-aov-foth — AoV Fist of the Heavens
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Holy/lightning element unatttested in dossier text; player loses element-family flavor label. No ailments mapped. Heaven's Fury secondary beam fidelity limited by probe-class sourcing of the beam-swap detail.

### d3-arachyr-firebats — Arachyr Firebats
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Fire element unatttested (player loses element flavor). No ailments mapped. Horrify fear unatttested in dossier — player seeking fear synergy finds none. Rooted channel feel preserved via delivery_notes.

### d3-dashing-strike-monk — Dashing Strike Monk
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Cold element unatttested; player loses cold-flavor labeling. Obsolescence flag: kit is historically attested but non-competitive; player building for current meta would find this off-meta.

### d3-dmo-twister — DMO Energy Twister
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Element null means player loses arcane/shadow flavor labeling. Wandering twister drift feel preserved via R-M6 circle geometry + drift notes but no direct engine equivalent for merging-twisters mechanic.

### d3-firebird — Firebird Ignite
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Fire/arcane element unatttested. Burn ailment not mapped (Firebird Ignite is a proprietary mark, not the burn status). Player loses element flavor and ailment synergy hooks.

### d3-god-hungering — GoD Hungering Arrow
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical element null. GoD 2pc auto-fire-during-Strafe identity well-captured via trigger_grammar + moving-channel note. Momentum stacks not mapped (no engine Momentum lane) — noted in TEMPORAL_CHARGE T4 door.

### d3-inarius-bonestorm — Inarius Bone Storm
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Player would miss: (1) the mandatory proximity/melee-range loop feel — this is a walk-into-mobs identity not well-expressed by standard orbit token alone; (2) the Bone Armor activation prerequisite gating the orbit (engine has no conditional-activation orbital); (3) CoE rotation alignment as burst-texture layer.

### d3-jade-harvester — Jade Harvester
**CLOSE · MAPPED** · elements: earth+shadow · ailments: poison
> Player would miss: (1) the precise DoT-duration-banking mechanic (Jade 2pc stacks thousands of seconds of duration into reapplication — no engine analog for duration-as-currency); (2) the geographic requirement that Soul Harvest hits the DoT'd enemies in its radius — player must maneuver between apply and harvest phases.

### d3-leapquake — Leapquake
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: (1) the three-jump charge mechanic as a feel-differentiator — engine leap_strike is single-use per cast; multi-charge rhythm of Lut Socks (3 charges on cooldown) has no native analog; (2) the 80% damage-reduction burst-window on Leap landing (Band of Might defensive proc) fusing offense and defense in the same verb.

### d3-lod-bazooka — LoD Bazooka Meteor
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Player would miss: (1) the multi-step choreography identity — bank, swap-buff, dump — is a timing ritual that engine resource_economy keys approximate but don't enforce as a loop pattern; (2) the Archon swap-out mechanic (transform then intentionally exit) has no engine form-swap analog; (3) Area Damage secondary-proc texture lost.

### d3-lon-bombardment — LoN Bombardment
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: (1) the off-screen boulder drop identity — Bombardment's visual and feel is boulders falling from above at cursor, which engine ground_targeted_circle approximates but doesn't distinguish from other ground abilities; (2) Norvald's Fervor mounted-set mobility burst (15-second Steed Charge windows) as a distinct speed-phase identity.

### d3-m6-sentries — Marauder Sentries
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Player would miss: (1) the 5-sentry simultaneous-fire identity — engine totem fires independently; here all 5 fire on-cast-linked in exact sync with player; the simultaneity is the identity; (2) pack-positioning relative to placed turrets as the primary skill expression — kiting enemies into pre-placed kill zones is the gameplay loop that engine can approximate but not enforce.

### d3-masquerade-spear — Masquerade Bone Spear
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Player would miss: (1) the triple-projectile-per-cast feel — engine line geometry is single projectile; three-simultaneous via clone mirrors has no native expression; DUAL_PROXY covers the delegation but not the synchronized volley feel; (2) Simulacrum spatial positioning (clones stand where spawned, creating three distinct spatial origins for spear delivery) — engine proxy positions are not separately addressable.

### d3-mundunugu-sb — Mundunugu Spirit Barrage
**CLOSE · MAPPED** · elements: water · ailments: (none)
> Player would miss: (1) the Phantasm-accumulate-then-release ritual (place 3, wait, place 3 more to detonate) has no exact engine analog — two-tier accumulator approximates but The Barber's instant-all-burst at second Phantasm cast is a specific timing mechanic; (2) Big Bad Voodoo mandatory uptime as a prerequisite multiplier gate — engine has no conditional-prerequisite T4 lock; (3) Manitou overhead auto-targeting as distinct from player-aimed Phantasm placement.

### d3-natalya-rov — Natalya Rain of Vengeance
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Moving-channel Strafe + at-target-zone RoV are both present but Natalya's CDR-reset-on-Strafe-hit has no native engine analog — approximated via PERSISTENCE_ENGINE_uptime door. No engine equivalent to 'cooldown reset on specific-skill hit' at Wave-B.

### d3-poj-tempest-rush — PoJ Tempest Rush
**CLOSE · MAPPED** · elements: water · ailments: blind
> Flurry 100-stack→release approximated as whirlwind+TEMPORAL_CHARGE; no exact engine moving-channel-with-stack-release-AoE. The moving-channel feel (PoJ's identity) maps well but losing the Flurry stack-to-icy-explosion rhythm degrades the fantasy.

### d3-raekor-boulder — Raekor Boulder Toss
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Charge-accumulate-then-Fury-dump two-tier pattern is approximated via TEMPORAL_CHARGE + RESOURCE_CONVERSION. The Raekor stack multiplier riding on charge-count (item-defined) has no exact engine analog. Source player would miss the 'charge more to hit harder' proportional scaling.

### d3-raiment-shenlong — Raiment Generator
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Shenlong's Spirit inverted-resource (full-bar depletion triggers damage burst) approximated via RESOURCE_CONVERSION + TEMPORAL_CHARGE; no exact engine 'Spirit-bar-dumps-to-zero-for-multiplier' analog. Crippling Wave Mangle rune adds fire damage — secondary element not loaded (only top-2 by scaling weight; lightning is the corpus-confirmed primary).

### d3-rolands — Roland's Sweep
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Roland's 375% AS engine reaching attack-speed cap has no exact engine analog. The Sweep Attack identity is sound but the attack-speed-cap-as-identity feel cannot be fully reproduced without a matching AS ceiling mechanic. Source player would miss the 'everything blurs into a spin' sensation.

### d3-s6-impale — Shadow Impale
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Karlei's Point near-infinite Hatred sustain (refund on cast = resource-neutral loop) approximated; no engine exact analog for 'cost refunded on each cast.' Shadow 6pc first-hit multiplier is set-scaler only. The melee-DH identity (close-range knife assassin) maps well to single_target geometry.

### d3-shield-bash — Shield Bash
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Weak set support noted in dossier ('not even worth mentioning') reflects the negative classification context. The kit maps coherently as a single-target directional burst with Wrath economy; the design constraint (weak legendaries) is fidelity texture. No stun emitted — stun was a kb-class claim (INADMISSIBLE) not attested in fetched dossier text.

### d3-sotl-hammer — SotL Blessed Hammer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> The 30-hammer density orbit has no direct engine orbit-count analog (numbers are steward-owned family accruals). PERSISTENCE_ENGINE_uptime approximates the 'maintain orbital hammer field' loop. Faithful Memory stacking damage marks approximate via trigger_grammar; no native 'stack-per-orbit-pass' engine mechanic.

### d3-spectral-blade — Spectral Blade
**CLOSE · MAPPED** · elements: shadow · ailments: (none) · **negative-canon (trap-kit)**
> ERRATA-43 redeemed form maps as CLOSE. The Spectral Blade free-spam inside Slow Time zone is a coherent geometry+zone-control loop. Without DMO the kit would be GAPPED. The mapping reflects the DMO-equipped build; the negative classification story rides the review book.

### d3-sunwuko-wol — Sunwuko Wave of Light
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Sunwuko clone multiplication of bell drops (clones appear from set mechanic and each casts Wave of Light) approximated via trigger_grammar; no engine 'set-spawned-clone-casts-your-primary' analog. The bell-drop identity and holy element map cleanly; the clone-multiplication layer is the approximation source.

### d3-tal-meteor — Tal Rasha Meteor
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Cold/lightning/arcane cycling elements unatttested as independent skill identities — player loses those filler-element flavor labels. No burn ailment attested. Meteor-only element identity mapped as fire; four-element rotation captured via trigger_grammar/element_rotation_window.

### d3-trag-nova — Trag'Oul Death Nova
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical element null — player loses blood/shadow flavor label. Drain ailment not mapped (verbatim status word absent from anchor quotes). Life-spend economy identity preserved via hp_cost_scale and SACRIFICE_ASCENDANCY door.

### d3-typhon-hydra — Typhon Hydra
**CLOSE · MAPPED** · elements: water · ailments: (none)
> No freeze or chill ailment attested (water element ≠ cold status; no status word in fetched rows). Player would miss ailment synergy hooks. Dual-Hydra multi-head ramp is approximated via PROXY_ASCENSION door; placed-proxy-count accrual filed.

### d3-ue-multishot — UE Multishot
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical element null. No ailment attested. UE ×2339 magnitude is review-book texture only. Discipline-as-damage-scalar identity preserved via resource_economy key.

### d3-uliana-ep — Uliana Exploding Palm
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical element null. No ailment attested. Mark-detonate identity well-captured via trigger_grammar apply-consume-pair. Teleporting SSS multi-hop approximated as dash_attack; exact D3 hop-to-each-target mechanic has no direct equivalent.

### d3-vyr-archon — Vyr Chantodo Archon
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Arcane/shadow element approximation (default mapping row applied). No ailment attested. Form-swap feel approximated via self_buff + PHASE_MOMENTUM door; in-Archon full kit replacement has no direct engine analog.

### d3-ww-wastes — Whirlwind Wastes
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Bleed ailment not mapped (verbatim 'bleed' absent from anchor_quotes despite mech_note probe reference). Player loses bleed synergy hooks. Moving-WW-with-Dust-Devils identity well-captured. Physical element null.

### d3-zbarb — zBarb
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:amplify
> Support-role approximation: engine has no party-support lane natively; solo-PvE scope means party utility is context-only. curse:weaken attested for Falter. Rage Flip 'pull and gather' identity preserved via vortex_pull. Globe generation has no engine lane (loot-economy adjacent).

### d3-znec — zNec
**CLOSE · MAPPED** · elements: water · ailments: curse:decrepify, execute, freeze
> Party-support mechanics approximated in solo scope (party buffs become self-applicable mechanical analogs). Command Skeletons pet-rider unengineable (summoner GAP) — approximated as totem. Freeze-screen CDR-loop identity well-captured via cooldown economy + freeze ailment.


## d4 (36)

### d4-andariel-flurry — Andariel Flurry Rogue
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Current Cold Imbuement variant identity lost — player using the cold-meta build would notice the element shift. Kit maps the item-defined Andariel poison form which is the kit_id's declared identity.

### d4-auradin-paladin — Auradin Paladin
**CLOSE · MAPPED** · elements: fire+holy · ailments: consecrate
> Paladin resource (Faith/Resolve) contested — resource_economy empty per do-not-populate erratum; player would notice the missing economy spec. Arbiter Form amplification captured only as fidelity note — insufficient fetched language for independent row.

### d4-ball-lightning — Ball Lightning Sorcerer
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> Element null — source player would expect lightning as the element identity but no explicit 'lightning damage' language is attested in store rows (MW3: skill name ≠ element ground). The orbit geometry and Mana economy map cleanly; only the element slot is gapped.

### d4-blazing-abyss-warlock — Blazing Abyss Warlock
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Warlock resource economy empty (cooldown-only; contested-field erratum). Shadowform invisibility/immortality frame not mapped as ailment — no ailment registry entry for stealth/invisibility. Player would miss the Shadowform defensive texture.

### d4-blood-lance — Blood Lance Necromancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null (blood/physical = element-neutral); source player would expect a physical or shadow identity but no explicit damage-type language attested. Overpower burst captured as fidelity note rather than primary consequence_type.

### d4-blood-wave — Blood Wave Necromancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Corpse Tendrils row sparse — no dedicated dossier rows; based solely on verify_ledger core_skills mention. Physical element null across both skills; source player would expect physical/blood identity. Wave geometry uses ground_targeted_circle as best-fit approximation for rolling tidal zone.

### d4-bone-spear — Bone Spear Necromancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Shadow element applied via crosswalk deterministic row (bone→shadow) rather than explicit fetched 'shadow damage' language — mapper judgment per §7.1. Corpse Tendrils not mapped (no dossier row). No ailments attested despite shadow/bone-damage identity.

### d4-bouldercane — Bouldercane Druid
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null on both skills (physical/earth boulders — no explicit element-damage language attested; THE PHYSICAL RULE applies). Hurricane ailment (chill) not attested — demoted to null. Source player would expect earth or physical element identity and a chill/slow from Hurricane.

### d4-cataclysm — Cataclysm Druid
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> No ailment mapped (no status word in fetched anchors). Secondary Werebear-form (Claw) flavor lost; form-locked access not a gap per form law (§CROSS row 3) when the primary loop is mapped.

### d4-chain-lightning — Chain Lightning Sorcerer
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> No ailment mapped (chain-lightning visual implies shock but 'shock' only attested as skill-category name). Crackling Energy as pickup-orb economy texture approximated via self_buff; no dedicated lane for pickup-orb resource fills.

### d4-dance-of-knives — Dance of Knives Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Poison ailment not mapped (skill-name only, no verbatim poison-status language). Physical element null. Fan of Knives shotgun burst variant approximated in scaffold; core loop is channel-spin identity.

### d4-death-trap — Death Trap Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null (physical/shadow only in probe, inadmissible). No ailment mapped. Vacuum-pull texture captured in delivery_notes; not mapped as independent geometry row — player loses explicit vortex pull geometry hook.

### d4-earthquake-barb — Earthquake Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null (physical only in probe). No ailment. Zone-detonation trigger grammar approximated via apply-only / earthquake_zone_active mark; no native placed-zone-trigger lane for the HotA-detonates-Earthquake mechanic.

### d4-evade-sb — Evade Spiritborn
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null. No ailment. Evade-as-damage-verb has no direct engine geometry parallel — defensive_dash + trigger_grammar captures intent but the mapped 'Evade IS the attack' identity is approximated.

### d4-flame-shield-immortal — Immortal Flame Shield
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Burn ailment not mapped (DoT delivery language ≠ ailment status token per basin-2 DoT-timing rule). Player would miss burn-status synergy hooks. Defensive immortality identity cleanly captured via SACRIFICE_ASCENDANCY.

### d4-hammerdin-paladin — Hammerdin Paladin
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null (ERRATA-46 — holy import struck; no d4 element attestation). No ailment. Disciple's Halo orbit-follow behavior (R-M8 pursuit delta) approximated in delivery_notes; no direct engine lane for orbit-with-pursuit.

### d4-heartseeker — Heartseeker Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element null. No ailment. Paingorger echo-propagation approximated via trigger_grammar + GEOMETRY_PROPAGATION_overkill door; no native 'echo every hit to surrounding enemies' lane. Seeking behavior preserved in delivery_notes.

### d4-hota — HotA Barbarian
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Ancients as cast-mimicking proxy approximated as totem; full autonomous-combatant Ancients behavior has no engine lane (summoner-GAP partial rider). Overpower burst_window not an ailment. Aspect of Limitless Rage 900% cap is scaler-only.

### d4-ice-shards — Ice Shards Sorcerer
**CLOSE · MAPPED** · elements: water · ailments: freeze
> Conditional re-seek trigger grammar has no exact engine primitive; mapped as proc_trigger_condition=target-frozen which approximates the seek-the-frozen retarget. Frost Nova is a setup enabler whose reservation-free toggle role is lost in scaffold (that build, somewhat worse).

### d4-incinerate — Incinerate Sorcerer
**CLOSE · MAPPED** · elements: fire · ailments: (none) · **negative-canon (trap-kit)**
> Overheating timed damage buff mapped as burst_window trigger consequence; exact 2s ramp duration is fidelity texture not engine-capturable. Mobility penalty (rooted while channeling) = fidelity note only. Player would feel the stationary constraint is present but underweighted.

### d4-kick — Kick Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Fury-scaled spike finisher has no direct engine primitive for 'entire pool as damage multiplier'; TEMPORAL_CHARGE approximates the accumulate-to-release shape. Stack-ramp rotation → finisher cycle loses some precision vs APPROX threshold but player would recognize it as 'that build, somewhat worse' — CLOSE holds.

### d4-lightning-spear — Lightning Spear Sorcerer
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> Conjured-spear proxy identity approximated via PROXY_ASCENSION; engine proxy lanes are autonomous combatants (summoner gap), not transient seeking projectile-entities. Player would feel the autonomous spear hunt behavior is present but underweighted vs full summoner treatment. Evade-Teleport as trigger verb has no exact proc_trigger_condition primitive.

### d4-mighty-throw — Mighty Throw Barbarian
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Auto-throw every 0.5s via item interaction has no direct engine primitive; trigger_grammar approximates the periodic proc. Placed pulsing zone shape is CLOSE to ground_targeted_circle but loses the 'shockwave radiates from point' texture. Player would feel the zone placement identity is present but the rhythmic auto-throw loop is underweighted.

### d4-payback-sb — Payback Spiritborn
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Skill footprint unknown from store: single_target is a reasonable default but the actual geometry of Payback (cone? point? AoE?) is unverified. Inverted-Vigor loop has no perfect engine primitive; RESOURCE_CONVERSION approximates the spend-restore identity. Player would feel the spam-loop is present but the exact geometry may differ.

### d4-pen-shot — Penetrating Shot Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Cold/Poison variant duality cannot be fully captured in one row; primary line-pierce form mapped, variants in fidelity. Boomerang bounce (Eaglehorn) is a delivery variant that changes the loop feel significantly — noted but not mapped as alternate geometry per variant-scope law.

### d4-quill-volley — Quill Volley Spiritborn
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Spiritborn spirit-guardian stacking mechanic (Berú of the Multitude 4-guardian synergy) has no engine primitive; scaffold records item-defined identity but engine cannot reproduce the 4-guardian combo bonus. Partial Vigor restore (40-50%, not 100%) means this is a less extreme version of payback-sb's inverted loop — economy approximated.

### d4-rabies-lacerate — Rabies Lacerate Druid
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Source player would miss: (1) the precise Spirit-cost curve; (2) the Debilitating Roar upkeep shout as a support action in the rotation; (3) Hurricane as persistent defensive layer — these are scaffold/fidelity texture, not identity loss.

### d4-rapid-fire — Rapid Fire Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) imbuement element choice is the build's actual feel differentiator — mapping defaults to no fixed element; (2) precise energy-regen interaction with Heartseeker filler; (3) Scoundrel's Kiss / Crown of Lucion item contributions — numeric scalers only.

### d4-shadowblight — Shadowblight Necromancer
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Source player would miss: (1) Shadowblight pulse threshold mechanic (8th hit count) is identity-core but maps only as trigger note; (2) corpse-node economy gap — the spatial-consumable-resource-node docket class has no native lane; (3) Shroud of False Death + Heir of Perdition mythic defense layers are scaler-only.

### d4-thorns-barb — Thorns Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) the precise Thorns-stat scaling curve via Razorplate Masterwork; (2) Barbed Carapace key-passive interaction as the central trigger condition; (3) the defensive feel of standing still in groups — 'damage-by-getting-hit' loop feel is fidelity texture beyond the reflect-damage lane.

### d4-tornado-werewolf — Tornado Werewolf
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) Spirit economy crunch — 2-set talisman is mandatory for smooth gameplay; (2) Tornado drift behavior (seek-then-wild + Fleshrender return arc) is the build's feel differentiator; (3) Werewolf form persistence as loop prerequisite.

### d4-touch-of-death — Touch of Death Spiritborn
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Source player would miss: (1) Scourge fear variant is a meaningful support option but variant-scope excludes it from core row; (2) swarm cap-3 replacement behavior is the feel differentiator; (3) Vigor refund loop via Ring of Midnight Sun is economy-critical but dossier detail is thin.

### d4-twisting-blades — Twisting Blades Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) the delayed-return arc is the entire identity feel — maps only as delivery_notes; (2) Poison Imbuement variant excluded from core row by variant-scope law; (3) mobility requirement (Dash + Shadow Step) is the loop prerequisite that makes the return hits land.

### d4-wind-shear — Wind Shear Druid
**CLOSE · MAPPED** · elements: (silent) · ailments: poison · **negative-canon (trap-kit)**
> Source player would miss: (1) element null is counter-intuitive given Storm tag — but no lightning/wind damage verb in dossier; (2) tag-inheritance scalar chain (Storm+Basic enabling Moonrise/Adaptability/Thunderstruck) is the identity differentiator; (3) Werebear-form upkeep requirement is a secondary loop prerequisite.

### d4-wing-strike-arbiter — Wing Strike Arbiter Paladin
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player would miss: (1) holy element feel is intuitive but unattested — element null is the honest call; (2) near-passive playstyle ('Wing Strikes do all the work') is the loop feel differentiator; (3) resource identity (Faith vs Resolve) remains contested — do-not-populate per erratum.

### d4-ww-dust-devils — Whirlwind Dust Devils
**CLOSE · MAPPED** · elements: (silent) · ailments: knockback
> Source player would miss: (1) the Shoutgun S10 variant's Chaos Perk dependency is a meaningful variant branch; (2) Fury economy crunch without Tibault's Will is a real feel differentiator; (3) Dust Devil drift behavior (wander) is the damage delivery mechanism.


## di (10)

### di-cyclone-strike-monk-base — DI Monk — Cyclone Strike (base)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Single-skill base cell maps cleanly. Minor loss: Monk Spirit resource economy unnamed (UNSUPPORTED). Pull geometry maps to vortex_pull which is the closest 26-enum approximation.

### di-draw-quarter-crusader — Draw and Quarter Horse Crusader
**CLOSE · MAPPED** · elements: (silent) · ailments: root
> Draw and Quarter maps well as dash_attack + root. Minor loss: the 6-second mounted-state duration and persistent drag-while-riding texture have no engine lane (movement channel with sustained damage = gap note). Engine maps the hit-and-drag as a dash_attack but the sustained drag is a delivery texture deviation.

### di-frenzy-barb — Frenzy Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Maps well. Minor loss: Restless Demon ultimate uptime noted in verify_ledger anchor ('Frenzy seems to be designed to be played around high Restless Demon uptime') but ultimate/ability name only with no mechanics in store — omitted per name-only law. Sprint ERRATA-52 excluded correctly.

### di-hota-wotb-barb — HotA Burst Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> Maps cleanly. Minor loss: WotB item variant (Broken Soul crit-chance swap) and Lasting Hate duration extension are item-layer scalers not in skills[]. HotA magnitude and WotB duration purely numeric; fidelity notes carry.

### di-meteor-wizard — Meteor/Stealth Wizard
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Wind-up skillshot timing + PvP preposition context are notable texture losses. No DI resource key emitted (ERRATA sweep; UNSUPPORTED mechanics claim). Fire-pool DoT duration/uptime is engine-approximated.

### di-monk-sss — Seven-Sided Strike Monk
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Multi-point teleport burst (SSS) approximated as melee_strike — the 7-position radial delivery pattern is not natively represented. No ailments attested despite CC-adjacent kit feel (inward pull, stun-adjacency in PvP copy). DI resource unreliable.

### di-multishot-dh — Multishot Demon Hunter
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical kit with no attested ailments — ailment-sparse mapping. Knockback Shot behavior unattested beyond name (near-miss logged). DI resource unreliable.

### di-ray-of-frost-wizard — Ray of Frost Wizard
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Freeze and stun unattested in core channel loop (near-misses). Chill-stacking-to-Freeze is the experiential identity but only chill maps honestly. Ice Crystal AoE reflection is item-defined; fidelity note only.

### di-vengeance-strafe-dh — Strafe Weave DH
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical kit, no attested ailments. Channel energy economy approximated without resource key (ERRATA sweep). Blacktalon pierce behavior is item-defined — fidelity note only.

### di-whirlwind-barb — Whirlwind Barbarian
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Physical kit, no attested ailments. Bleed near-miss on Lacerate (name-only, no verb). Resource economy omitted per ERRATA sweep. Whirlwind energy drain/recover texture not captured in resource_economy keys.


## gd (23)

### gd-aar-spellbinder — Albrecht's Aether Ray Spellbinder
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> minor drift: the source player experiences a hard energy-management pressure and a rooted-while-channeling commitment; PERSISTENCE_ENGINE_uptime approximates the sustained-beam identity but the engine has no literal aether-ray, so the beam is mapped as a channeled piercing line. No status lost (none attested).

### gd-aegis-paladin — Aegis of Menhir Paladin
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> minor drift: the out-and-return boomerang leg is a signature the source player feels (shield comes back) but the engine ricochet_bounce geometry does not model the return path -- filed as out-and-return accrual, geometry approximates the outbound hop only. No status lost (none attested).

### gd-belgothian-blademaster — Belgothian Blademaster
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> minor drift: the WPS suite is the source player's core texture (a rotating pool of weapon procs firing every swing) but the engine models it as a single on-hit-threshold burst rider rather than a named pool of distinct procs, since no individual WPS payload was fetched. Blade Spirit's autonomy is under-attested, mapped as orbit rather than pet. No status lost.

### gd-bloody-pox-conjurer — Bloody Pox Conjurer
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> minor drift: the signature the source player feels is the plague JUMPING through a dense pack (contagion), which the engine single_target geometry does not model -- mapped as single-cast + spread note per precedent. Two near-misses withheld (no forcing): a vitality-decay DoT status (not named in fetched -- theme != status) and Curse of Frailty's RR token (application shape unanchored). No status emitted.

### gd-bwc-demolitionist — Blackwater Cocktail Demolitionist
**CLOSE · MAPPED** · elements: fire · ailments: blind
> minor drift: the source player lays overlapping burning ground carpets and debuffs with fumble + RR -- blind (fumble) is captured, but the fire-DoT's 'burn' flavor is withheld (not named as a status) and Thermite's RR token is withheld (application shape unanchored). The molotov-carpet ground zone maps cleanly to ground_targeted_circle; the two withholds are near-misses, not silent drops.

### gd-cadence-witchblade — Cadence Witchblade
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> minor drift: the source player feels the swing-count rhythm building to a periodic detonation (every 3rd swing) -- the engine has no native every-Nth-swing accumulator, so it is filed as a two-tier-accumulator family accrual and approximated via trigger_grammar, not delivered natively. Curse of Frailty's RR token is withheld (shape unanchored). No status emitted. Stays terminal MAPPED (CLOSE with a family-accrual candidate) per R-M7.

### gd-callidors-tempest-templar — Callidor's Tempest Templar
**CLOSE · MAPPED** · elements: fire+lightning · ailments: burn
> minor drift: the source player accepts a hard range/target-size restriction (must be point-blank; only hits human-sized mobs) as the cost of a strong pulse -- the engine ring geometry delivers the point-blank burst but does not model the human-size gate. The aether-fire composite is compressed to fire-primary + lightning-secondary. burn is captured (named). Minor composite-element drift.

### gd-canister-saboteur — Canister Bomb Saboteur
**CLOSE · MAPPED** · elements: fire · ailments: bleed
> minor drift: the source player uses Flashbang as a hard CC/debuff (community calls it 'Insane') and stun-locks packs -- but the engine emits NO CC token for it because the fetched anchor names only 'debuff' (stun/blind live in probe/claim-paraphrase, both inadmissible). Canister's cluster-scatter maps to multi_projectile and internal-trauma to bleed cleanly. The withheld Flashbang CC + Thermite RR are near-misses, not silent drops.

### gd-dee-witch-hunter — Dreeg's Evil Eye Witch Hunter
**CLOSE · MAPPED** · elements: earth · ailments: poison
> minor drift: the two-stage projectile-then-pool delivery is compressed to the pool geometry with the bolt as delivery flavor; the fumble-curse accuracy layer and confusion layer are withheld pending steward rows (near-misses, not silent drops).

### gd-devastation-sorcerer — Devastation Sorcerer
**CLOSE · MAPPED** · elements: fire+lightning · ailments: curse:sap
> minor drift: discrete falling-meteor impacts homogenize to zone-tick damage in ground_targeted_circle; the devotion-proc layer is empty (payloads unfetched).

### gd-doom-bolt-sentinel — Doom Bolt Sentinel
**CLOSE · MAPPED** · elements: fire · ailments: curse:sap
> minor drift: hard-cooldown nuke rhythm + timer-based CDR pulse ride on cadence keys rather than a native cooldown primitive; the acid/chaos DoT carry is element-flavor only (no statuses named -> no tokens).

### gd-fire-strike-purifier — Fire Strike Purifier
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> minor drift: the WPS attack-variety layer is structurally present but payload-thin (unfetched); line compresses shot-plus-burst into the attested explosive-line footprint.

### gd-forcewave-warlord — Forcewave Warlord
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Lane-wave spam loop, cast-root rhythm, casting-speed tempo land natively; Internal Trauma DoT layer now ROUTED (bleed) under the m02-audit steward ruling (GD trauma -> bleed, phys-DoT lineage). Residual drift: bleed-vs-trauma flavor register + ZONE_CONTROL door weak fit (accepted-weak at audit). [STEWARD AUDIT 2026-07-18: regraded APPROX->CLOSE in-place; the sole stated deviation was the pending row ruling, now resolved.]

### gd-krieg-death-knight — Krieg Death Knight
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> minor drift: the counted every-3rd-hit texture is approximated by the native cycle + threshold surfaces (accrual filed for the exact two-tier shape); Krieg's Wrath set-proc layer is empty (name-only).

### gd-mortar-purifier — Mortar Trap Purifier
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> minor drift: turret aggro-targeting autonomy and overlap-count multiplication are softened onto the native placed-emitter; the exact count-stacking shape lives in the filed accrual.

### gd-panettis-mage-hunter — Panetti's Missile Mage Hunter
**CLOSE · MAPPED** · elements: fire+lightning · ailments: (none)
> minor drift: equal-thirds tri-elemental compresses to a 2-slot hybrid (cold dropped per hybrid law -- the source player would see one-third of the rainbow missing its color, damage carried but flavor narrowed).

### gd-primal-strike-vindicator — Primal Strike Vindicator
**CLOSE · MAPPED** · elements: lightning · ailments: curse:sap
> Wind Devil wanders; engine totem is stationary (R-M8-adjacent mobile-emitter drift; qual mint-candidate filed). Storm Totem unfetched — omitted rather than memory-supplemented.

### gd-roh-infiltrator — Rune of Hagarrad Infiltrator
**CLOSE · MAPPED** · elements: water · ailments: (none)
> Trap arms on enemy contact; engine ground-circle bursts/ticks on placement — the arm-and-lure timing texture is lost (qual mint-candidate filed). Still that build, slightly worse: place-under-enemies loop survives.

### gd-shadow-strike-infiltrator — Shadow Strike Infiltrator
**CLOSE · MAPPED** · elements: water · ailments: (none)
> Movement and nuke are fused in one button; engine teleport is an offensive reposition whose strike payload on arrival is noted, not asserted native (arc-b01 discipline). Fusion texture may render as reposition-then-hit.

### gd-trozan-druid — Trozan's Sky Shard Druid
**CLOSE · MAPPED** · elements: lightning+water · ailments: (none)
> Cold/lightning HYBRID collapsed to element_primary water + secondary lightning per §1 top-2 rule; the Codex hybrid's cold->lightning conversion identity carried by ELEMENT_CONVERSION_HYBRID door. Source player of the pure-cold Skybreach variant loses the lightning slot — noted as variant, dominant published loop is the cold caster.

### gd-vitality-conjurer — Vitality Conjurer
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> The build's POST-PATCH dominant form is the Dark One's Gift totem-sigil hybrid (weak-Sigil-to-dominant-totem transformation is explicit in fetched text) — mapped as the totem-forward form. Source player loses: the RR-curse (Curse of Frailty) mapped as un-tokened support (shape-silent withhold), and the totem's leech-sustain flavor is economy-noted not ailment-tokened. [STEWARD AUDIT 2026-07-18: blind token struck (anchor-splice; OA-reduction unattested) — debuff-texture understatement now includes the OA-tax flavor.]

### gd-wendigo-totem-ritualist — Wendigo Totem Ritualist
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Totem-army is a placed-proxy delivery that engine supports as `totem` — but the AUTONOMY of the leech-totems (they tick independently while player kites) is a mild summoner-deferral flavor; here the totems are PLACED emitters (map cleanly), not autonomous combatants (no pet GAP). Source player loses the RR/control ailment tokens (both withheld on attestation grounds), which understates the debuff-stacking texture.

### gd-word-of-pain-tactician — Word of Pain Tactician
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Multi-variant element identity (chaos/lightning/pierce) collapsed to the dominant PIERCE build -> element-neutral. Source player of the chaos (shadow) WoP Vampirris variant loses their element slot. The devotion-proc payloads (Flame Torrent etc.) are the kit's real damage flavor but map to nothing — names only, no fetched behavior — so the mapping understates proc-driven output. 'Elemental agony' brand has no tokenable status.


## hades2 (4)

### hades2-glorious-disaster — Glorious Disaster (Zeus+Apollo duo)
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> A Glorious Disaster player gets the channel-a-lightning-zone boss-shredder faithfully -- placed zone + Magick tick-cost channel + lightning-echo capstone door. Drift: the exact '20 dmg / 0.13s while channeling, scaling with +30 Magick invested' TIGHT COUPLING of channel-duration-to-strike-count is carried as a tick-cost channel rather than a first-class Magick-investment-to-output multiplier; you channel for damage, but the precise Magick-fed escalation curve is approximated. That build, worse -> CLOSE.

### hades2-hail-storm — Hail Storm (Zeus+Demeter duo)
**CLOSE · MAPPED** · elements: lightning+water · ailments: freeze
> A Hail Storm player gets the freeze-triggers-lightning engine faithfully via on-ailment-application -> linked-cast (the cleanest possible map for 'control converts to damage'). Minor drift: the cross-element cadence where longer freeze-lock = MORE lightning triggers (Cold Storage extending the trigger window) is carried as a freeze-duration trait rather than a first-class freeze-uptime-to-lightning-frequency coupling; the throughput scales, but the 'hold the freeze longer to fire more bolts' curve is approximated. That build, worse -> CLOSE.

### hades2-hephaestus-blast — Hephaestus Blast Core
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> A Hephaestus blast player gets the weapon-independent periodic fire blast faithfully -- ground_slam + cooldown-gated on-hit burst + fire-propagation door. Drift: the 'damage completely independent of weapon base' property (the blast pays out a flat 400 no matter what you equip, so low-base weapons like Aspect of Selene punch hit as hard as heavy swings) has no first-class engine expression -- damage still routes through the skill/scaling substrate, so the 'weapon doesn't matter, only the blast' identity is approximated. That build, worse -> CLOSE.

### hades2-omega-magick — Omega/Magick Commitment Grammar
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · `is_system`
> The Omega/Magick charge-commitment grammar maps faithfully -- Magick meter (focus) + charge-release burst + self-origin delayed Cast nova. Drift: (1) the COMMITMENT RISK identity (standing STATIONARY and vulnerable during the charge, trading safety for a bigger payload) is carried as an activation-toggle windup, not a first-class channel-vulnerability state; (2) 'every verb has an Omega variant' is a system-wide grammar collapsed to one representative Cast geometry (Attack=line / Special=multi_projectile noted). That build, worse -> CLOSE (the charge-commit loop is playable; the per-verb breadth + stationary-risk texture are approximated).


## hot (8)

### hot-archer — Archer (multishot)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element-neutral mapping drops the flavor of the archer ranged-glass-cannon feel; player would notice the absence of any elemental specialization that HoT traits can provide through variants. Core cone+pierce geometry maps cleanly.

### hot-astronomer-orbs — Astronomer's Orbs
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Movement-speed orbit coupling is unusual and not expressible in current geometry vocabulary — player would miss the movement-build synergy path. Otherwise orbit geometry maps cleanly.

### hot-cleric-radiant — Radiant Aura Cleric
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Element-neutral mapping misses the cleric-holy thematic register; player would notice the absence of holy identity. Mechanically clean: aura+heal loop maps well.

### hot-kugelblitz — Kugelblitz (wandering ball lightning)
**CLOSE · MAPPED** · elements: lightning · ailments: stun
> Electrify ailment (the kit's secondary status identity) drops entirely — player would miss the stacking voltage mechanic that is central to the achievement/mastery path. Stun-only capture is weaker than the source identity.

### hot-norseman-frost-avalanche — Frost Avalanche Norseman
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Dual-threshold structure (250-hit nova trigger AND 20-stack per-enemy explosion) partially maps to TEMPORAL_CHARGE + cascade pair but the two-tier accumulator shape is steward-accrual territory. Player who expects independent nova-and-explode timing control will notice the approximation.

### hot-sage-ring-blades — Ring Blades Sage
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Low-conf dossier (Sage 1.1-2026 post-cutoff); Fragile debuff has no registry lane and cannot be emitted as ailment; player building around Fragile application will notice the gap.

### hot-shieldmaiden-block — Block-Stack Shieldmaiden
**CLOSE · MAPPED** · elements: (silent) · ailments: burn, chill
> Stat-as-damage-substrate (Block Strength → Shield Bash damage) is a steward-accrual shape with no exact engine lane. Player building for block-conversion offense will notice the stat-to-damage translation is approximated. Burn is item-sourced; chill is sourced from a block-charge interaction note, making both ailment attributions indirect.

### hot-warlock — Warlock (summon caster)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Summon-projectile chain has no exact engine analog: chain geometry maps the targeting behavior; proxy/summon layer maps the 'summoned entity' flavor; but a fired-projectile-that-is-also-a-summon-entity is an approximation. Player expecting persistent autonomous summons (not fired projectiles) will notice the delivery difference.


## la (41)

### la-arthetinean-skill-machinist — Arthetinean Skill Machinist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Engine has no battery-drone-weave analog; constant-rotation weave without a meter-activate Z-button maps reasonably to TEMPORAL_CHARGE build-momentum pattern but the source player would note absence of the transformation/identity burst button (Hypersync is attested but suboptimal — the identity is genuinely the weave, not a burst release). CLOSE not EXACT: economy key is novel-vocabulary ('battery') and drone/joint skill distinction has no direct geometry analog.

### la-asuras-path-breaker — Asura's Path Breaker
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Attested identity maps cleanly as gauge-accumulate + timed burst_window with front-attack positional. CLOSE (not EXACT) because the dual-gauge alternation (Stamina and Shock as two named sub-gauges feeding one Asura Energy pool) is a novel economy shape the engine vocabulary doesn't fully name — source player would notice the two-sub-gauge generator structure is flattened to a single asura_energy key.

### la-barrage-enhancement-artillerist — Barrage Enhancement Artillerist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Barrage Mode is a player-transforms-into-turret mechanic — not a placed totem proxy. The immobile-bombardment shape is the best available geometry but the source player would notice the player-body-as-turret nuance is lost. Economy maps cleanly as accumulate-release. CLOSE not APPROX because the dominant loop (build→burst→exit→repeat) lands correctly; the geometry approximation is delivery texture, not loop identity.

### la-brawl-king-storm-breaker — Brawl King Storm Breaker
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Dual stamina/shock gauge alternation maps to resource_economy as two named keys but the perpetual-generator-not-accumulate-to-Z shape differs from the standard build-then-burst loop — both gauges are always in motion (one fills as the other depletes). Source player would note the dual-gauge perpetual rhythm isn't fully captured by the simpler accumulate-release framing. CLOSE: the dominant loop (alternation) maps, the burst-blows consequence maps, the novelty is in the dual-gauge simultaneity.

### la-control-glaivier — Control Glaivier
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Single-stance flat-damage approach maps cleanly; CLOSE because the Dual Meter as buff-on-specific-skills (not a full identity release) is an unusual economy shape that the engine's resource_economy doesn't natively express as 'buff three specific skills with meter but do not release the meter as a burst'. Source player would notice the meter's limited/modified role.

### la-death-strike-sharpshooter — Death Strike Sharpshooter
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:amplify
> Silverhawk as deployed debuff-hawk has partial totem fit but differs in that the hawk also defines the 'NOT summoned' damage window as its own separate state (12% damage while hawk absent creates a second timing loop the engine doesn't directly express). Source player would notice the 'hawk absent = bonus' logic is lost. CLOSE: dominant loop (build meter, deploy hawk for debuff burst, rebuild) maps cleanly.

### la-deathblow-striker — Deathblow Striker
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> 3-orb strict all-consume gate maps as resource_economy accumulate-release but the 'all orbs consumed simultaneously for multiplicative burst' nuance differs from a simple spend-one-at-a-time meter. Source player would note the strict orb-count gate and multiplicative per-orb damage scaling are characteristic but not fully representable. CLOSE: the build-and-detonate loop identity maps cleanly.

### la-demonic-impulse-shadowhunter — Demonic Impulse Shadowhunter
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Near-permanent demon form economy (Eternal Blood) maps as self_buff steady-state, but the 'enter form → stay in form almost permanently' pattern is a standing transformation not a repeated build-spend cycle — source player would notice the rhythm difference from a standard gauge-release loop. CLOSE: the identity (demon form as primary combat state) maps; the cycle rhythm is approximated.

### la-drizzle-aeromancer — Drizzle Aeromancer
**CLOSE · MAPPED** · elements: (silent) · ailments: chill, curse:amplify, curse:weaken
> Stale values omitted (shape only); Barrage-class turret n/a. STEWARD-CORRECTED: 3 enemy-directed ailments restored (chill + curse:weaken on Sun Shower, curse:amplify on Tornado) — original under-emission. Otherwise clean gauge→burst_window debuff-support identity.

### la-energy-overflow-soulfist — Energy Overflow Soulfist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Inner-energy floor mechanic (Energy Overflow = gauge never empties) is a novel resource inversion; resource_economy carries the shape but the floor semantics are imprecise. Hype level-scaling (L2 40s sustained vs L3 20s burst) maps as two-depth burst_window shape in delivery_notes.

### la-esoteric-flurry-striker — Esoteric Flurry Striker
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Back-attack positioning constraint (back attacks = +10% Crit Rate +5% Damage) is an orientation-requirement the engine cannot express natively — delivery_notes only. Otherwise clean orb-generate-and-spend mapping.

### la-esoteric-skill-wardancer — Esoteric Skill Enhancement Wardancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Per-orb-count damage scalar at cast (+6% per orb) is a graduated multiplier with no direct engine token — approximated via resource_economy + delivery_notes. Weakness Exposure (raid-break) cannot be expressed as 16-ailment.

### la-evolutionary-legacy-machinist — Evolutionary Legacy Machinist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Sync Zero cooldown-reset-on-use mechanic (Quantum Assembly Beam resets other Sync skill cooldowns) has no direct engine token — expressed in delivery_notes. Two-battery system (Core → Sync Zero Battery) approximated in resource_economy keys.

### la-ferality-wildsoul — Ferality Wildsoul
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Dual-form stack-build economy (Fox/Bear both feeding same Ferality stack cap) approximated via resource_economy; form-specific skill availability is a delivery constraint the engine cannot express natively. Ark Passive fox/bear node paths → capstone_alterations.

### la-first-intention-wardancer — First Intention Wardancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Esoteric Origin empower window (orb-spend → empowered next-N-skills) is a mark-consume trigger the engine approximates but cannot fully express. Distinction from ESE (window vs per-orb scalar) is fidelity-noted.

### la-full-moon-souleater — Full Moon Harvester Souleater
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:amplify
> Two-resource chain (Soul Stones → Possession Meter → Deathlord Mode) approximated in resource_economy; the two-step fill relationship is expressed in keys but the sequential dependency is a fidelity-noted approximation. Amplified Damage curse:amplify mapped per DIRECTION LAW (enemies take more) — values omitted (stale).

### la-grace-empress-arcanist — Grace of the Empress Arcanist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE not EXACT: Card Deck stochastic-variance layer (up to 2 simultaneous cards, 3 card types each modifying detonation differently) has no engine expression — source player would notice the probabilistic shortcut (Judgment card = instant 4-stack) and crit amplifier (Cull) are absent from the mapping. The core apply-consume-pair loop lands correctly; the variance texture is lost.

### la-gravity-training-destroyer — Gravity Training Destroyer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE not EXACT: two-stage meter economy (cores then gauge) is a novel economy shape the single resource_economy key set approximates but does not fully model — source player would notice the distinct core-spend → gauge-fill two-step is flattened. Left-click basic attack as primary damage form inside Hypergravity has no direct analog to a named skill; the basic-attack-dominant window loses fidelity vs a skill-dominant rotation. Dominant loop (accumulate→burst→damage→repeat) maps correctly.

### la-hunger-reaper — Hunger Reaper
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE not EXACT: Chaos Mode refresh-on-hit mechanic (duration extension per Dagger hit or Shadow skill use) is a novel refresh-shape the engine burst_window consequence_type does not natively express — source player would note the pseudo-permanent uptime dynamic is flattened. Back-attack positional discipline has no engine analog. Core loop maps correctly.

### la-igniter-sorceress — Igniter Sorceress
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> CLOSE not EXACT: pre-cast timing discipline (Doomsday must be cast before Arcane Rupture activation so meteor lands inside burst buff) is a sequencing nuance with no engine trigger analog. Incomplete Combustion variant (alternate Ark Grid config) is a meaningful build fork; mapping covers dominant Standard loop. Fire attestation lands correctly; Weak Point boss-break correctly omitted.

### la-loyal-companion-sharpshooter — Loyal Companion Sharpshooter
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> CLOSE not EXACT: companion-uptime-as-damage-delivery has no engine companion loop analog beyond COMPANION_CONTRACT T4 door — source player would note the hawk's persistent damage contribution is not modeled. The self-buff package (+12% boss damage self-only) maps as a conditional self_buff but the companion-presence condition (hawk must be summoned) is lost. Negative kit distinction (C-tier community rating) rides the review book per negative-flag caution.

### la-lunar-voice-reaper — Lunar Voice Reaper
**CLOSE · MAPPED** · elements: (silent) · ailments: poison
> CLOSE not EXACT: Persona window empowers next Swoop Skill only (single-skill burst payoff with +170% damage) — the concentration-of-burst-into-one-skill shape is an unusual trigger consequence the burst_window token captures in shape but not specificity. Back-attack positional discipline (Ambush Master engraving — DEAD axis) is delivery texture lost in mapping. Poison DoT from Shadow Vortex lands correctly (only attested ailment in-basin).

### la-mayhem-berserker — Mayhem Berserker
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE not EXACT: the permanent HP-lock economy (HP locked at 25% as a standing identity constraint) is a novel self-state the engine self_buff key captures in shape but not specificity — source player would note the HP-floor constraint and its -60% healing cost are absent from the mapping. The nested Red Dust timed burst_window inside a permanent buff state is a two-layer structure the trigger_grammar flattens to one consequence_type. Dominant loop (permanent damage identity + nested timed burst) lands correctly. DEFENSIVE_TRADEOFF + SACRIFICE_ASCENDANCY T4 doors capture the HP-trade identity.

### la-nights-edge-souleater — Night's Edge Souleater
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Soul Snatch window CDR-stack mechanism (Spirit-analog) loses quantitative depth; burst_window captures SHAPE. 'Soul Decapitation as terminator' is delivery texture, not mapped as separate grammar node.

### la-order-emperor-arcanist — Order of the Emperor Arcanist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Delayed-damage timing window (buff pre-load → detonation) has no direct engine grammar slot; captured in delivery_notes. Card-draw card-type system (Emperor/Chancellor/Royal identity) loses card-type granularity — map shape as card_deck_meter gauge cycle.

### la-perfect-suppression-shadowhunter — Perfect Suppression Shadowhunter
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Perfect Suppression's 'permanent suppression of Demonize' shape (vs n01 Demonic Impulse TIMED form) is the defining differentiation — captured via PHASE_MOMENTUM + economy note. The priority-list system (vs strict rotation) cannot be fully modeled in trigger_grammar but is noted in motion_frame.

### la-phantom-beast-awakening-wildsoul — Phantom Beast Awakening Wildsoul
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> GX-02 form-swap gap applies (Fox/Bear dual-skill-family identity may have deeper form-mechanic than attested in dossier). Spirit stack CDR mechanism loses quantitative depth. Mapped SHAPE: burst_window with CDR-stack cycling.

### la-pinnacle-glaivier — Pinnacle Glaivier
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Buff values explicitly stale (CONTRADICTED verify_ledger row) — mapped shape only per addendum. Stance-alternation identity (swap IS the economy trigger) maps as PHASE_MOMENTUM + Dual Meter cycle; per-stance skill partitioning (Focus=spear vs Flurry=glaive) loses granularity in flat skills[]. Back-attack positioning critical — noted delivery_notes per skill.

### la-predator-slayer — Predator Slayer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Fatigue→Exhaustion reduction mechanic (stacks shortening downtime, not amplifying burst) is an unusual inverted-ramp shape; MOMENTUM_CASCADE captures it imperfectly — noted. 'Volcanic Eruption'/'Flame Deathblade' element strictly struck by D4 NAME-ONLY LAW (no damage-typing in text).

### la-punisher-slayer — Punisher Slayer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Punisher vs Predator distinction (shorter Burst windows vs sustained uptime; Specialization vs Swiftness stat profile) is an economy-texture difference within the same Fury→Burst shell; cannot be fully mapped without per-kit stat scaling parameters. PHASE_MOMENTUM captures cycle-variant shape imperfectly.

### la-rage-hammer-destroyer — Rage Hammer Destroyer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> 'Gravity' mechanic vocabulary (Gravity Cores, Gravity Release) is class-specific and maps to accumulate-spend cycle; not an element family. 3-core threshold spend is a compact RESOURCE_CONVERSION shape. Mobile identity (vs GT locked Hypergravity) is economy texture only — noted in motion_frame.

### la-rage-hammer-destroyer-bt — Berserker's Technique vs Mayhem (negative twin note)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Negative slot maps ATTESTED BT identity per addendum §E.5 negative-flag caution. Malformed slot (mech_note: 'NOT a record') — the contradiction story rides the review book. Red Dust self_buff direction-tested and correctly NOT emitted as curse. Class is Berserker (BT), not Destroyer despite kit_id containing 'rage-hammer-destroyer-bt' — corpus folk_name confirms Berserker's Technique Berserker class.

### la-recurrence-artist — Recurrence Artist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> Skill geometry is attested at class-pose level only; no individual damage-skill geometries named in store. Motion frame reconstructed from loop field verbatim. Core skill set blank (no names in fetched dossier). Player consequence: identity loop and sustained feel correct; specific skill shapes absent.

### la-reflux-sorceress — Reflux Sorceress
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Individual skill geometries inferred from names / notes — not damage-typed in store. Element consistently null across all skills. Sub-variant Destiny distinction (Palpatine vs Instacast) carried in fidelity_notes only; the two Ark Passive paths collapse to same mapping_json shape.

### la-remaining-energy-deathblade — Remaining Energy Deathblade
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> 30s Death Trance maps as burst_window (timed) — player consequence correct. Orb tier attack-power scaling is number (stale-SHAPE only; do not map the specific percentages). Ark Passive Destiny riders in trigger mark_identity note only.

### la-robust-spirit-soulfist — Robust Spirit Soulfist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Conviction/Judgment synergy pair is attested but has no direct engine lane (resource_economy partial capture); fidelity_notes carry. Lightning Palm name-only element null confirmed. Hype 3 burst_window shape correct; player consequence: correct feel of instant-access burst vs Energy Overflow's ramp identity.

### la-shining-knight-valkyrie — Shining Knight Valkyrie
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:amplify
> Synergy → curse:amplify mapping is correct per DIRECTION LAW; the self-side 35% Holy Blade boost is modeled separately in economy charges. Requiem Ash/Rain geometry inferred from name class — not explicitly stated in store. Light Meter 15-cast fill mechanism correctly models the identity-gauge economy.

### la-shock-training-scrapper — Shock Training Scrapper
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Shock gauge builder/spender correctly modeled. The '5/10/20% Shock Energy return' is a number (stale-SHAPE only per §LA §0.1); shape is 'partial refund on consumption' → modeled in resource_economy. Dual Stamina/Shock gauge nature of Scrapper noted in economy; Stamina not independently modeled as the fetched text focuses on Shock gauge.

### la-taijutsu-scrapper — Taijutsu Scrapper
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:amplify
> Z consequence modeled as self_buff (sustained uptime) vs burst_window (Shock Training) — this is the key design distinction between the two Scrapper specs. Stagger boss-break not mapped to ailment per §LA row 4. Synergy → curse:amplify. Gem priority skills name-only element null throughout.

### la-time-to-hunt-gunslinger — Time to Hunt Gunslinger
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Two-stance identity maps cleanly without mode-swap-identity docket (dominant loop exists). Quick Scope accumulator + Rose Blossom threshold correctly modeled. Handgun CDR economy noted. Crit Rate value not modeled (number = stale-SHAPE; shape captured as 'significant crit-focus').

### la-wind-fury-aeromancer — Wind Fury Aeromancer
**CLOSE · MAPPED** · elements: (silent) · ailments: chill, curse:amplify
> Multiple element near-misses (Thunderwind, Tornado, Piercing Wind, Gale Slash, Wind Gimlet) all null — correct per D4 NAME-ONLY LAW but the player would feel wind-themed. Sun Shower enemy slow → chill is the only ailment attested for this kit. Party speed buff modeled as self_buff (DIRECTION LAW), not a curse. Raindrop Meter economy correctly typed.


## le (22)

### le-bladestorm-bd — Bladestorm Bladedancer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Bladestorm's placed spinning-blade entity is not a perfect 26-enum fit — `totem` captures placed-emitter honesty but loses the spinning/whirlwind visual texture (whirlwind rejected: it implies player-centered spin, fetched explicitly denies this). Source player loses no mechanic, only the geometry-flavor precision. Low-Life stacking mapped as economy note, not a §B inversion row (attestation gap).

### le-bomb-lance-falconer — Explosive Ballista Falconer
**CLOSE · MAPPED** · elements: water · ailments: (none)
> Fire element not attested in non-abstained dossier rows (brief hot-fact references 'inflicting fire damage' but this phrase not found in fetched abstained=0 text); mapping as water-only with fidelity note. Dual placed-proxy identity (Trap+Ballista both placed) is richer than a single totem; DUAL_PROXY T4 captures this. Falcon companion following vs placed nuance: companion lane not a T4 door class but noted in delivery.

### le-chthonic-fissure-warlock — Chthonic Fissure Warlock
**CLOSE · MAPPED** · elements: fire+shadow · ailments: (none)
> The signature 'fire damage over time' of Chthonic Fissure almost certainly IS the Ignite ailment in-game, but the guide never names the status, so burn is withheld under strict §0.1 — a source player would feel the DoT as their core damage and our map understates it (no burn token). Seeking-spirit pursuit is a behavioral delta noted but not minted (not the sole identity loop).

### le-detonating-arrow-mm — Detonating Arrow Marksman
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> The kit's real identity is a trigger-driven proc-multiplication engine (traps proc DA explosions), not a manually-fired arrow spam — mapped via GEOMETRY_PROPAGATION_cascade + linked-cast trigger grammar. Source player feels a screen-filling explosion storm; our chain_count=2 + single door understate the density of the proc-multiply (accrual-adjacent, but no numbers filed — the proc COUNT is not a family member yet). No status token despite 'explosive' theme.

### le-erasing-strike-vk — Erasing Strike Void Knight
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Core loop (one telegraphed void cleave, spammed via cooldown-removal + Mana regen) maps cleanly as melee_arc + RESOURCE_CONVERSION. Two texture losses: (a) Mark of Rot's boss-hit payload is un-tokened (name-only, unfetched); (b) Anomaly's time-replay/echo utility has no engine analog and maps only as a generic self_buff — a source player loses the 'replay your interactions' feel, but it is buff-utility, not damage identity.

### le-explosive-trap-falconer — Explosive Trap Falconer
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Trap+Ballista both map `totem` (placed-proxy) — clean, but the DEPLOY-AND-DETONATE tempo (pre-place, then chain-trigger) is a placed-detonator rhythm that `totem` (a persistent emitter) approximates rather than nails. The falcon companion is a pet-rider gap (autonomous strikes not deliverable). Source player loses the falcon chip-damage and the precise trigger-detonation timing feel, but the trap-carpet identity is deliverable.

### le-fire-aura-spellblade — Fire Aura Spellblade
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Aura-pulse damage delivery maps clean. Source player would miss the depth-3 DPS cascade (Firebrand -> Frost Claw -> Ice Barrage), which the engine caps at chain-depth 1 — a real scaling delta, though not the core identity loop. Fire->cold Freezing-Aura conversion is captured by ELEMENT_CONVERSION_MONO. Flame Ward burst-defense button has no aura-identity role and is a rider.

### le-flame-reave-spellblade — Flame Reave Spellblade
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> Cone melee AoE maps directly. Source player would miss (1) the Sunwreath cone->giant-circle transform that redefines clear geometry (approximated by GEOMETRY_COLLAPSE, not a native cone->ring swap), and (2) the aura-consume-for-mana self-refund loop (Flame Drinker) — an unusual sustain cadence the engine notes but does not natively model as an aura-spend.

### le-frost-claw — Frost Claw Sorcerer
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Cold projectile-barrage with chill/freeze maps clean. Source player would miss (1) the Elemental Nova free-proc-per-cast cascade (an on-cast linked-cast the engine approximates, not a dedicated proc-Nova), and (2) Frostbite stacking DoT — a cold damage-over-time status with no engine registry token (chill/freeze cover the CC but not the DoT). ELEMENTAL_ECHO stands in for the doubled cold-hit cadence.

### le-frost-wall-rm — Frost Wall Runemaster
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Placed ice-lane with guaranteed freeze maps clean. Source player would miss (1) the wall physically blocking enemy projectiles/movement (engine placed_lane is a hit-lane, not a collision barrier), and (2) the Pyroglass fire-conversion -> Brand of Trespass -> damage-multiplier Runemaster chain (a rune-interaction rider with no native lane). Control identity preserved via ZONE_CONTROL + freeze/chill.

### le-ghostflame-warlock — Ghostflame Warlock
**CLOSE · MAPPED** · elements: fire+shadow · ailments: (none)
> Channeled fire+necrotic cone maps clean (cone + channel tick-cost economy carry the sustained-DoT identity; PERSISTENCE_ENGINE_uptime door). [STEWARD REGRADE 2026-07-18: APPROX -> CLOSE — the APPROX rationale rested on the withheld ailment ('the ailment-free row does not carry the DoT payload'), which the m04-audit damage-type-over-time RULING dissolves: 'fire and necrotic damage over time' attests delivery TIMING, not a status; dossier attests DoT only to 'enemies in cone path' during the stream (no lingering/stacking-beyond-channel language) — the engine channel-tick cone IS that shape. Forcewave-regrade precedent.] Remaining texture drift: the defensive-channel inversion (Disdain damage-reduction-while-channeling) and the Bone Curse variant-silent aura (no curse effect fetched) are riders the engine gestures at — noted, minor.

### le-hammer-throw-paladin — Hammer Throw Paladin
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Orbiting physical hammers map cleanly to orbit. Source player would miss the geometry POLYMORPHISM across variants: the mapped core is orbit, but Nova Hammerdin (Enra's + Avatar of the Spire) converts to a screen-wide nova and DISABLES orbit — the engine picks one geometry, not a stance-swap between orbit and nova. PERSISTENCE_ENGINE_uptime (audit-corrected door) carries the always-on orbit-field identity but not the orbit<->nova fork. Physical-neutral element loses the 'holy hammerdin' flavor (carried in element-slot flavor only).

### le-harvest-lich — Harvest Death Seal Lich
**CLOSE · MAPPED** · elements: shadow+water · ailments: (none)
> Two-variant identity (Harvest Flay cold vs Death Seal necrotic) means any single motion_frame undersells one variant. The combined folk name is a mapping convenience, not a verified single build. DEFENSIVE_TRADEOFF covers Death Seal's Low Life tradeoff identity; cold melee Reaper Form maps cleanly to water + melee_arc. Grade CLOSE reflects good geometry and element coverage but the split-build nature introduces fidelity loss.

### le-healing-hands-paladin — Healing Hands Paladin
**CLOSE · MAPPED** · elements: fire+holy · ailments: (none)
> Proc-on-melee ring burst + on-hit trigger maps clean. Source player would miss the heal-as-weapon DUALITY: the primary damage skill is a HEAL that also strikes — the engine ring carries the fire/holy hit and the trigger carries the proc, but the healing payload doubling as DPS is an identity the engine represents as self-sustain, not as a heal-that-is-your-damage. Rahyeh's Chariot turning Healing Hands into a MOVEMENT skill is a role-conversion rider with no core-geometry home.

### le-judgement-paladin — Judgement Paladin
**CLOSE · MAPPED** · elements: fire+holy · ailments: consecrate
> Ground-targeted consecrate zone maps clean. Source player would miss the ZONE-STACKING accumulation (Lingering Force multiplying overlapping Consecrated Grounds for compounding damage+healing) — the engine ground_targeted_circle places a zone but does not natively model overlapping-zone multiplication; ZONE_CONTROL approximates the control-density, not the stack-multiplier. The self-heal-within-zone duality (offense + sustain in one patch) is captured by consecrate but not the healing-scaling.

### le-lightning-blast — Lightning Blast
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> Chain-projectile spam maps clean. Source player would miss (1) the Spark Charge self-cascading proc-engine (Lightning Blast procs charges that proc more — an on-cast proc-loop the engine only approximates via chain, not a dedicated charge-cascade), and (2) the Reowyn's Frostguard on-cast Ward burst (Runemaster variant) — a defensive on-cast rider with no native engine lane. Neither breaks the core loop; both are riders. ELEMENTAL_ECHO gestures at the repeated-hit lightning identity.

### le-shift-bladedancer — Shift Bladedancer
**CLOSE · MAPPED** · elements: (silent) · ailments: execute
> Minor drift: Shadow Daggers stack payoff unexpressed (no home) and Umbral Blades rider unmapped (name-only); core loop - blink traversal with on-arrival ring payload, linked-cast riders, execute threshold - is native.

### le-smite-paladin — Smite Paladin
**CLOSE · MAPPED** · elements: holy+lightning · ailments: (none)
> Minor drift: missing-Mana damage substrate approximated via gear-numeric lane pending steward candidate; holy is carried by the aura skill while Smite itself rides lightning. The proc-storm loop (hit -> sky-bolt at target) is native trigger grammar.

### le-storm-totem-shaman — Storm Totem Shaman
**CLOSE · MAPPED** · elements: lightning+wind · ailments: (none)
> Minor drift: tornado-as-mobile-weather flavor rides a stationary placed-emitter token (no wandering behavior attested, so no pursuit delta); autonomous per-zone bolt targeting is texture inside the emitter grammar. Placement loop, multi-zone coverage, and lightning payload are native.

### le-swarmblade-druid — Swarmblade Druid
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Swarm-entity texture thinned: Swarm Strike 360-finisher maps as ring; Locust Swarm cycle is shape-silent (null row); Tornado proc payload carried as rider note; form-entry moment compressed into self_buff chassis. Loop verb (in-form melee spam + nova finisher + Rage pressure) survives intact -- that build.

### le-warpath-vk — Warpath Void Knight
**CLOSE · MAPPED** · elements: shadow · ailments: (none)
> Void Essence -> Void Well sub-resource feedback compressed into regen_shape note; auto-cast-on-move nearest-mapped (AUTOCAST_ON_MOVE token); Anomaly/Symbols buff-layer texture thinned. Core loop (move-while-spinning tick-drain field + orbiting orb + ramp) maps near-natively -- that build.

### le-werebear-druid — Werebear Druid
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Bear-form visual + Rampage traversal texture thinned; Earthquake-as-idol-scaler compressed into a delivery note; chance-roll proc kept as threshold trigger. In-form loop (melee arc spam + proc quakes + Rage pressure + DR stacking) survives intact -- that build.


## mcd (3)

### mcd-dynamo-torment — Dynamo Roll-Shoot (Standstill/Rolling Torment)
**CLOSE · MAPPED** · elements: (silent) · ailments: knockback
> MCD enchantment-loadout identity lacks mastery/ascendancy layer; stack-unload approximates TEMPORAL_CHARGE but MCD has no on-kill propagation, chain, or node-tree depth. A player familiar with PoE Seismic Trap or D4 charge builders would recognize the core pattern but miss the enchantment-slot granularity.

### mcd-fireworks — Fireworks Arrow Artillery
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> No direct 'cooldown-as-resource' engine lane; CD reduction via armor enchant approximates resource_economy cadence_scale. Explosion AoE radius is not quantified in fetched text, so circle footprint is directionally correct but unscaled. Player familiar with ARPGs would recognize trap/artillery loop.

### mcd-soul — Soul Build (Corrupted Beacon economy)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Soul resource has an accumulate-then-spend duality not captured by tick-cost alone; the beam is the drain and killing is the fill — the engine's PERSISTENCE_ENGINE_uptime approximates this but the two-phase loop (gather vs burn) is richer than a simple toggle. Player would feel the core beam+soul-economy identity.


## poe1 (62)

### poe1-aegis-max-block — Aegis Max Block
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> Block-chance stacking to a ~75% cap and 'ES recovered per block' are numeric magnitudes the engine expresses via def-bin block rider + on-block trigger, not a bespoke mechanism; identity intact, the exact 'infinite shield vs blockable damage' feel is a numeric-tuning outcome. Delivery-agnostic offense means the offensive geometry is a placeholder, not a source-fixed skill.

### poe1-arc — Arc
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> STEWARD AUDIT (DRIFT-CRITIC 25% sample): downgraded EXACT->CLOSE. Engine chain fan-out DECAYS per hop (_CHAIN_DEFAULT_DECAY=0.7, primary+3 arcs default); PoE Arc GROWS damage per remaining chain (+15% more) across 7-10 hops. Scaling direction inverted + hop count compressed — the player of the original would feel pack-clear invert (engine chain strongest on first target; Arc strongest deep in the pack). Identity (chaining lightning bolt + sunder) intact. Quantitative mint-candidate ledgered: per-kit chain-decay override >1.0.

### poe1-archmage — Archmage Mana Stacker
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> The mana-stack resource identity (RESOURCE_CONVERSION) and MoM/Indigon economy warps land cleanly, but Ball Lightning's signature 'slow-drift + 150ms tick + inverse-velocity (slower orb = more hits = more damage)' has no matching 26-geometry; approximated as a circle tick-AoE. A player would keep the mana-as-weapon feel but lose the positional skill of drifting the orb through a pack for max hits.

### poe1-armageddon-brand — Armageddon Brand
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The attach-emitter-mark + periodic meteor lands via trigger-grammar (mark_identity + burst-damage) and ground_targeted_circle, but the meteor's TIMED proc-while-attached has no exact proc_trigger_condition enum member (approximated to on-mark-apply). The distinctive 'run freely while brands auto-bombard the marked target' feel is preserved; the exact cadence-while-attached timing is a numeric property the trigger enum doesn't name.

### poe1-aurastacker — Solo Aurastacker
**CLOSE · MAPPED** · elements: water · ailments: (none)
> The self-stacking aura identity lands cleanly (NETWORK_AMPLIFIER, solo-viable unlike Aurabot), but the source reserves ~100% of the pool (via Aul's Uprising free-aura) which exceeds the engine's 0.75 LOCKED reservation cap — clamped in the map. A player would keep the 'walking-buff-tower who deals damage by existing' feel; the extreme near-total reservation magnitude is capped below the source's.

### poe1-ball-lightning — Ball Lightning
**CLOSE · MAPPED** · elements: lightning · ailments: blind, sunder
> Ball Lightning's signature 'slow drift + 150ms tick + inverse-velocity (slower = more hits)' has no matching 26-geometry — approximated as a circle tick-AoE, same as the archmage BL delivery. The mine throw/detonate chassis is modeled via trigger-grammar + activation-toggle. A player would keep the orb-zap and mine-laying feel but lose the fine positional skill of drifting the orb slowly through a pack to maximize hits.

### poe1-bane — Bane
**CLOSE · MAPPED** · elements: shadow · ailments: curse:amplify, curse:decrepify, curse:weaken, drain
> The chaos-DoT-plus-curse-bundle and per-curse damage multiplier land via the drain ailment + curse: variants + NETWORK_AMPLIFIER, but the source's defining 'ONE cast applies ALL linked curses simultaneously' is expressed as the kit carrying multiple curse-ailments rather than a single bundled-cast primitive. Outcome-faithful; a player keeps the 'cast once, everything is cursed and melting' feel, though the engine models the curses as co-applied discrete ailments.

### poe1-baron-zombies — Baron Zombies
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> The str-stacked zombie army maps via PROXY_ASCENSION + attribute-affix scaling (Strength -> minion count/power) + TH leech, but 'a specific gear stat (STR) on your sheet becoming the army's scaling axis' is abstracted to generic attribute-stacking-of-minions rather than a bespoke Baron-helm mechanic. Outcome-faithful (stack STR, army grows); a player keeps the str-stack-summoner identity, though the flavor of one helm welding STR to zombie power is generalized.

### poe1-blade-flurry — Blade Flurry
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed, poison
> The channel-stack-release identity lands via PC tick-cost channel + charge-stack accumulator + TEMPORAL_CHARGE, but the frontal close-range AoE geometry ('circle in front of player') has no exact 26-type — approximated to melee_arc (neither the whirlwind-spin nor cone-breath fit). A player keeps the build-6-stages-and-detonate commitment feel; the precise frontal-circle footprint is generalized to a wide melee arc.

### poe1-blood-magic-kit — Blood Magic Life-as-Resource
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Life-as-resource lands on the purpose-built RS/LC lane (reservation_resource=hp + hp_cost_scale — the engine even names the guard after this kit). Minor identity drift: PoE Blood Magic is TOTAL and uncapped (max mana=0, any cost can exceed your life), engine clamps to 0.30 max-HP/cast LOCKED and keeps a mana pool. The 'no safety rail, cast can kill you' danger that defines the keystone's feel is bounded by the guard. Keystone-not-active-skill => geometry is a degenerate placeholder.

### poe1-boneshatter — Boneshatter
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> Trauma maps cleanly as a charge-stack accumulator (on-hit-dealt fill, cap 9) paired with hp_cost_scale self-damage — the exact 'more damage AND more self-harm per stack' coupling, both native. Drift: the identity's SOUL is the reset-cliff risk-management (ride toward 9, dread the 10th-stack reset, self-damage climbing quadratically 194*(N+1)); the engine accumulator caps-and-holds rather than modelling the overflow-reset threat, and hp_cost_scale 0.30 LOCKED clamps the escalating self-hit magnitude. Damage ramp intact; the knife-edge cap-tension is approximated.

### poe1-caustic-arrow — Caustic Arrow
**CLOSE · MAPPED** · elements: shadow · ailments: poison
> Clean map to ground_targeted_circle + poison (crosswalk-mandated chaos->shadow+poison home); the hit-independent 'only the ground cloud matters' identity is native to a zone-occupancy DoT. Minor drift: PoE Caustic Arrow is a fixed-tick chaos DAMAGE-OVER-TIME cloud, while the engine `poison` ailment is stack-additive (cap 5-10); the DoT-cloud-vs-stacking-ailment nuance is smoothed by the mandated lane. Wither-totem chaos-taken amp routed as ailment-scaling debuff, noted.

### poe1-coc-ice-nova — CoC Ice Nova
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> on-crit -> linked-cast is native and IS the CoC identity (Cyclone crit machine-guns Ice Nova). Two smoothings: (1) Cospri's Malice is a SECOND parallel on-crit trigger (socketed spells fire too) — parallel depth-1 fan-out, but only one proc_trigger_condition primitive is modelled, so the double-trigger is a noted parallel not a chain; (2) 'attack-rate BECOMES cast-rate' via CDR breakpoints (14% CDR = ~one trigger/server-tick) is carried as cadence_scale, an approximation of a precise server-tick timing mechanic. Identity intact.

### poe1-cold-dot-occ — Cold DoT Occultist
**CLOSE · MAPPED** · elements: water · ailments: chill
> Twin structure to caustic-arrow: two ground_targeted_circle cold-DoT pools + chill (water family), self-anchored Vortex-at-feet. Drift: PoE cold DoT is a fixed-tick DAMAGE-OVER-TIME pool scaled by DoT-multiplier with reapply-not-spam cadence; the engine carries 'cold DoT' via water + chill ailment + ground_targeted_circle, but the pure-DoT-uptime damage model is approximated (PERSISTENCE_ENGINE_uptime at capstone). The CI/ES-facetank safety identity is a def-bin/trait rider, not a geometry.

### poe1-deaths-oath — Death's Oath
**CLOSE · MAPPED** · elements: shadow · ailments: drain
> The reserved-aura constant-chaos-DoT identity + zero-button uptime lands cleanly via aura geometry + drain ailment + PERSISTENCE_ENGINE_uptime + reservation economy. Minor drift: the item's signature 'chaos-damage-to-wearer-per-kill' self-harm loop (which forces the chaos-res investment that defines gearing) is expressed as a defensive-tax trait rather than a bespoke self-damage primitive; and the probe-attested 'wither' amp-debuff has no clean ailment lane. A player keeps the walk-and-melt feel; the self-damage-gearing-tension is generalized.

### poe1-discharge — Discharge
**CLOSE · MAPPED** · elements: fire+lightning · ailments: burn
> The 'build the stack, dump the stack' charge-consume-all identity lands NATIVELY via accumulator + discharge_threshold, and ring nova is exact. Minor drift: Discharge is intrinsically TRI-element (lightning-per-power / fire-per-endurance / cold-per-frenzy, each charge-count scaling its own damage type simultaneously) — the engine's 2 element slots keep the top-2 (fire+lightning), dropping the cold-per-frenzy contribution. A player keeps the charge-dump nova feel; the three-elements-at-once-partitioned-by-charge-type flavor is compressed to a dual-element nova.

### poe1-divine-ire — Divine Ire
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> The channel-gather-then-release-beam identity lands cleanly: beam_channel geometry + native accumulator-discharge (stage-build via on-hit-dealt, fire at 10-stage cap) + tick-cost channel + shock->sunder. Minor drift: the beam's fixed-length-immune-to-area-mods property and the secondary on-release damage-bubble are behavioral details the geometry enum doesn't separately model. A player keeps the full gather-then-lance rhythm; only the beam's area-scaling-immunity nuance is generalized.

### poe1-ea-ballista — Explosive Arrow Ballista
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The totem-delivered fuse-stack-then-detonate identity lands well: totem geometry (dominant loop) + native accumulator (20-fuse cap, fill-per-arrow, detonate-at-cap-or-on-death) + ground_targeted_circle burst + fire/burn. Minor drift: the fuse-stack accumulates on the TARGET from MULTIPLE autonomous totems' arrows (a shared on-defender accumulator fed by proxies), which the engine models as a single-target accumulator filled by hit-events rather than a bespoke multi-totem-shared-fuse primitive; and the 'detonate instantly the moment the target dies' is one accumulator discharge condition among the cap. A player keeps the place-totems-and-watch-it-erupt feel; the multi-totem-shared-fuse bookkeeping is generalized.

### poe1-earthquake — Earthquake
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> The plant-and-payoff delayed-aftershock slam lands well: ground_slam + native `delayed` timing (delay_seconds, engine-verified) whose non-stacking single-delayed-hit matches EQ's one-aftershock-per-slam exactly + physical-neutral + stun. Minor drift: the aftershock's LARGER radius than the initial hit is a behavioral property carried by the geometry+timing note rather than a separate scaled-geometry field; and physical is element-neutral (flavor only) per the physical rule. A player keeps the slam-then-delayed-bigger-boom rhythm faithfully.

### poe1-earthshatter — Earthshatter
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> The plant-then-detonate identity lands via ground_slam + apply-consume-pair trigger grammar (spikes = mark:consumption applied by slam, consumed by warcry for burst-damage) + spike-count accumulator, at chain-depth 1. Minor drift: the source has TWO valid detonators (warcry OR a follow-up slam) — the map fixes on the warcry-cast trigger (on-cast-linked), the dominant Berserker loop; and physical is element-neutral. The phantom 'Foulborn Ghostwrithe' alias is correctly ignored (no source fact). A player keeps the raise-spikes-then-shatter payoff rhythm.

### poe1-facebreaker — Facebreaker Unarmed
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> The unarmed physical-punch identity lands via melee_strike + physical-neutral (physical rule) + ELEMENT_CONVERSION_PHYSICAL, with the Facebreaker 600-1000%-more-unarmed multiplier expressed as the dominant unarmed-physical gear-affix/trait scaler. Minor drift: 'no weapon equipped, the gloves ARE the weapon' is abstracted to a large unarmed-damage affix rather than a bespoke empty-weapon-slot primitive; and physical is element-neutral. A player keeps the bare-fisted-bruiser feel and the item-defines-everything scaling, though the empty-weapon-slot flavor is generalized to an affix.

### poe1-flameblast — Flameblast
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Flameblast maps nearly losslessly — the purest charge-and-detonate: circle expanding-nova geometry + native accumulator-discharge (10-stage build via on-passive-tick, release at cap, and native sub-threshold release = the 'earlier release = weaker' behavior) + tick-cost rooted channel + fire/burn. Only minor flavor drift: the exact +0.3m-per-stage radius growth and 165%-more-per-stage magnitude are numeric tuning the geometry/accumulator carry as scaling rather than named fields; and 'circle' (filled expanding disc) is chosen over 'ring' for the self-origin grow-out. A player keeps the full channel-grow-release commitment faithfully.

### poe1-flicker — Flicker Strike
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> The teleport-strike + charge-fuelled auto-chaining lands via dash_attack + charge-cycle economy + TEMPORAL_CHARGE, but two behavioral signatures generalize: (a) Flicker teleports to a RANDOM nearby enemy each hop (dash_attack models a directed reposition, not random target-hop selection); (b) the hard dependency where running out of charges STOPS the build cold is a numeric-sustain property, not a bespoke mechanism. A player keeps the 'blink-strike a screen while holding one button' feel; the frantic random-hop chaos and the charge-starvation failure state are approximated.

### poe1-freezing-pulse — Freezing Pulse
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> The piercing cold bolt + chill/freeze lands via line geometry + water + the freeze/shatter pair, but Freezing Pulse's defining 'damage and freeze-chance DECAY with distance -- stand close for max output' has no matching 26-geometry (distance-falloff is a numeric projectile property the enum does not carry). A player keeps the piercing-cold-caster feel but loses the core positional discipline of hugging targets to hit the damage/freeze breakpoints before the pulse fades.

### poe1-frost-blades — Frost Blades
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> The melee-strike-spawns-icy-projectiles identity lands as a two-geometry composite (melee_strike + multi_projectile) with GEOMETRY_PROPAGATION_cascade for the hit-to-fan propagation, but the engine expresses it as two discrete geometries rather than a single unified 'strike that emits a projectile fan' primitive. The 30%-less-damage fan and the exact 'behind the first target' spawn geometry are behavioral properties. A player keeps the engage-in-melee / damage-projects-behind feel; the tight coupling of one attack producing both hits is generalized to two linked geometries.

### poe1-generals-cry — General's Cry
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> The corpse-summon -> transient-proxies-execute-your-linked-strike identity lands via PROXY_FISSION + on-cast-linked/linked-cast trigger-grammar at depth-1, but two properties generalize: (a) the mirages perform an EXERTED (warcry-boosted) copy of the player's SPECIFIC linked skill -- the engine models a generic linked-cast, not a faithful clone of an arbitrary chosen strike; (b) the corpse-consumption gate (no corpses = no warriors) is a resource dependency the economy lane approximates rather than a hard summon-fuel primitive. A player keeps the 'warcry erupts a mirage squad that all attack at once' feel; the exact skill-cloning and corpse-gating are abstracted.

### poe1-glacial-cascade-mines — Glacial Cascade Mines
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze, knockback
> The marching 4-burst ice cascade + knockback + freeze/shatter lands via line + GEOMETRY_PROPAGATION_cascade + the mine trigger-chassis, but two properties generalize: (a) the precise '4 discrete sequential bursts each bigger/final-burst-double-radius' cadence is a numeric multi-hit property line geometry doesn't enumerate; (b) the mine throw/detonate delivery is approximated via trigger-grammar + activation-toggle rather than a native mine primitive. A player keeps the 'lay mines, erupt a shoving line of ice that shatters the pack' feel; the exact burst-count/overlap-tuning and mine cadence are abstracted.

### poe1-glacial-hammer — Glacial Hammer
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze · **negative-canon (trap-kit)**
> The phys->cold single-target striker + freeze/shatter lands cleanly via melee_strike + ELEMENT_CONVERSION_PHYSICAL + the engine's NATIVE shatter (a direct match to shatter-frozen-low-life), but the 'every 3rd successive hit deals 200-390% more damage' cadence-counter has no enum carrier -- it is a behavioral property noted in traits, not modeled as a mechanism. A player keeps the freeze-a-target-then-shatter-it cold-mace identity; the rhythmic every-3rd-hit power-stroke pacing is generalized to flat strike output.

### poe1-golementalist — Golementalist
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The 8-golem menagerie (flame golems kill, other golem types buff the squad via jewels) maps via PROXY_ASCENSION + PROXY_CONVERGENCE + two proxy skill-entries, but the SPECIFIC engine of it -- Primordial Harmony cooldown-resets as the flame-golem DPS multiplier and Primordial Eminence as a per-golem-type effectiveness aura -- is abstracted to minion-cast-speed + golem-effectiveness affixes rather than a bespoke 'jewel-driven cooldown-reset + menagerie-buff' primitive. A player keeps the 'command a diverse golem squad where support-golems empower the killers' identity; the exact Primordial-jewel scaling loop is generalized to proxy traits.

### poe1-hexblast-mines — Hexblast Mines
**CLOSE · MAPPED** · elements: shadow · ailments: curse:amplify
> The consume-a-hex-for-amplified-chaos identity lands cleanly via on-mark-consume/consume-mark trigger-grammar + curse:amplify + NETWORK_AMPLIFIER + circle, but the full loop depends on an EXTERNAL curse-automation source (Impending Doom / hex-on-hit / Asenath's Mark) continuously re-applying the hex that Hexblast then consumes -- the apply half sits outside the kit's own skill and is captured in the economy lane rather than as a self-contained apply-consume primitive (MAX_CHAIN_DEPTH=1 keeps the consume as the modeled step). A player keeps the 'blast the curse off for a huge hit' feel; the automated re-cursing that sustains the loop is noted, not mechanized.

### poe1-hoag — Herald of Agony
**CLOSE · MAPPED** · elements: shadow · ailments: poison
> The your-hits-only-feed-a-pet-that-does-everything identity lands via PROXY_ASCENSION/PROXY_SOVEREIGNTY + the Virulence accumulator + two skill-entries (crawler proxy + Cyclone feeder), but the specific coupling -- the Agony Crawler's attack-speed/damage scaling CONTINUOUSLY off the live Virulence count, and the crawler DYING the instant Virulence hits 0 -- is a behavioral property of the accumulator noted in economy rather than a bespoke 'stack-count-drives-proxy-power-and-lifespan' primitive. A player keeps the feed-the-scorpion identity; the exact stack-to-proxy-power curve and the death-at-empty failure state are abstracted.

### poe1-ice-shot — Ice Shot
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> The cold-arrow-with-cone-splash-behind-target identity lands cleanly via cone geometry + water + ELEMENT_CONVERSION_PHYSICAL + freeze/shatter, with only minor drift: the skill is a two-part hit (partial phys->cold ON the target, then TOTAL phys->cold in the cone behind it) and the engine expresses the dominant cone while the on-target partial-conversion hit is folded into the cone-delivery note rather than modeled as a separate strike. A player keeps the aim-the-cone-through-the-pack cold-archer feel; the exact split between the single-target arrow hit and the full-conversion cone is generalized to the cone as the identity footprint.

### poe1-icicle-mines — Icicle Mines
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Mine throw/detonate chassis is approximated via trigger-grammar + activation-toggle (engine has no mine primitive -- b04-established approximation, not re-docketed); the detonation-sequence projectile-count growth and the quick-dissipate range falloff are behavioral/numeric properties multi_projectile does not enumerate; the converge-from-multiple-points field generalizes toward a single volley origin. Player keeps throw-then-detonate cold volleys with shatter.

### poe1-incinerate — Incinerate
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Cone-vs-beam: the stage-expanding cone footprint is folded into beam_channel (channel dominance per s7.2) -- a player would see a straighter stream than the source's widening fan. Stage count, per-stage cone-angle growth, and the release-wave multiplier are numeric properties with no enum carriers. 1.x-era 3-stage vs modern 8-stage numeric drift noted (mechanism identical).

### poe1-kinetic-fusillade — Kinetic Fusillade
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> The hovering-projectile halo visual, the 0.05s sequential-release rhythm, and the per-impact explosion AoE generalize to a standard multi-projectile volley with accumulator economy; the per-prior-projectile damage crescendo rides the door, not a per-projectile carrier. Source data is post-cutoff thin (delivery conf 0.3, econ 'unknown') -- re-check if a deeper dossier lands.

### poe1-lacerate-glad — Bleed Gladiator
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> The left-right double-slash choreography and its overlap double-hit zone generalize to a single melee_arc footprint (a Lacerate player would miss the positioning-for-overlap micro-game); the stance pair carries as a generic activation-toggle (mode re-tuning is behavioral); Gladiator max-block lives in the def-bin, not the mapping.

### poe1-lightning-arrow — Lightning Arrow
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Simultaneous-splash-to-3 vs sequential decaying chain hops is the visible drift (pack-clear cadence, not per-target damage, is what a LA player would notice); the 18u fixed splash radius and up-to-3 cap are numeric properties chain does not enumerate.

### poe1-lightning-conduit — Lightning Conduit
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> The consumed-magnitude coupling (damage read off the shock's effect value at consume time) generalizes -- engine consume-mark fires a burst but does not read the cleared ailment's magnitude; and Orb of Storms' periodic-zap cadence generalizes to totem behavior. The apply-then-cash-in loop, the sunder amp window, and the removal-on-consume all land.

### poe1-lightning-strike — Lightning Strike
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> The strike-spawns-fan identity lands as a two-geometry composite, but the engine expresses two discrete geometries rather than a unified strike-that-emits primitive (same generalization as b04 frost-blades); the ~85-degree forward arc, the fan's 50%-less ratio, and the cannot-miss coupling are un-enumerated properties. A LS player keeps melee-and-ranged-in-one-button.

### poe1-low-life-shavs — Low-Life Shavronne's
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The reservation warp, the sacrifice-for-power trade, and the aura-stack payload all land on literal engine keys/doors; what generalizes: (a) the ES-pool-substitution survival texture (living on a second pool while life is floored) -- engine defense bins differ, the near-death-but-safe FEEL is approximated by the tradeoff doors; (b) the below-35%-threshold CONDITIONAL structure flattens to a permanent static trade (faithful to lived play, since reservation pins the state); (c) the era-variable damage slot is mapped representatively (fire/RF register), not as a specific spell. A LL-Shavs player would say 'low-life auras, worse' -- the frame holds.

### poe1-mjolner — Mjölner
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> The swings-pour-out-spells identity lands via on-hit-threshold/linked-cast + proc-loop at depth-1; what generalizes: (a) the 0.25s internal cooldown (trigger-rate cap) has no engine carrier -- engine trigger cadence follows the host's hit rate uncapped; (b) the triggered-payload-costs-0 economy has no per-payload cost knob; (c) socket-order rotation between TWO socketed spells (Arc + Ball Lightning alternating) collapses to one modeled payload. Inherits the arc-b01 chain-decay drift on the payload.

### poe1-molten-strike — Molten Strike
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Two-geometry composite generalization (as frost-blades/lightning-strike): no unified strike-emits-projectiles primitive. The ball-overlap boss-shotgun (the identity payoff) is an emergent splash-overlap behavior the engine's multi_projectile does not guarantee; the 2-25-unit variable scatter and 60%-less ball ratio are un-enumerated numerics. A Molten Strike player keeps hammer-the-boss-under-a-magma-fountain.

### poe1-pconc — Poisonous Concoction
**CLOSE · MAPPED** · elements: earth · ailments: poison
> The flask-charge ammo economy and poison payload land on literal engine carriers (charge cycle + native stacking poison); what generalizes: (a) the FLASK-item coupling -- damage read off a gear-consumable's recovery stat becomes a generic resource-conversion door, losing the 'my healing potion is my weapon' flavor; (b) the unarmed weapon-slot requirement has no lane (flavor only); (c) charge_max=10/recharge=time are representative values for an unattested exact charge pool. A PConc player keeps sprint-and-lob poison-blast rhythm with charges gating throws.

### poe1-pizza-sticks — Pizza Sticks
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The per-stage EXPANDING blast radius (the circle visibly grows 3m per stage as the totem channels, and early detonation at partial stages trades size for cadence) has no live stack->geometry carrier — folded into circle + accumulator with notes; a player of the original loses watching the pizza slices grow and the partial-stage detonation texture. Place-totems-they-nuke identity fully intact.

### poe1-poets-pen-vd — Poet's Pen Volatile Dead
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Two spells triggered from ONE attack (dual-wand simultaneity) generalizes to the engine's one-trigger -> linked-cast shape — mapped as the spell pair sharing the attack trigger at depth-1; a purist loses the strict both-wands-fire-together texture. The 0.25s hard trigger-cooldown is carried as an economy note, not an enum. Corpse-seeking orb locomotion is behavioral.

### poe1-poison-bv — Poison Blade Vortex
**CLOSE · MAPPED** · elements: shadow · ailments: poison
> Blade-COUNT-scales-HIT-FREQUENCY (each added blade makes everyone in radius get hit FASTER, not harder) is a bespoke cadence coupling the engine orbit does not carry — landed as accumulator + notes. Plague Bearer's store-fraction-then-release pool is approximated as accumulator-spend into an aura (the incubate/release toggle rhythm noted). Walk-the-blender identity intact.

### poe1-righteous-fire — Righteous Fire
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Self-burn intensity clamped by the LOCKED 0.30 hp-cost ceiling: the source's knife-edge 'your own skill is actively killing you and one gear mistake means you burn to death' tension softens to a strong-but-survivable tick. Walk-forward burning-aura identity, zero-button loop, and the regen race itself are intact.

### poe1-skeleton-mages — Skeleton Mages
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Per-mage random element (fire/cold/lightning roulette) flattened to the mono-cold meta endpoint — the pre-conversion rainbow-squad texture is lost (docket accrual filed, kit graded un-minted). Squad-formation multi-point delivery carried by the proxy frame around single_target bolts.

### poe1-soulrend — Soulrend
**CLOSE · MAPPED** · elements: shadow · ailments: drain
> The damage-FEEDS-defense loop (per-hit spell-leech -> energy shield) has no resource_economy key — the TH lane converts damage TAKEN, not dealt; carried via the defense probe (ES primary), trait lane, and the RESOURCE_CONVERSION door. A player of the original misses the mechanical per-pack shield-refill pulse; homing-turn and the DoT-area-around-the-projectile are behavioral notes on the line pierce.

### poe1-spark — Spark
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Terrain-aware bouncing + stochastic wander — the properties that make ROOM GEOMETRY the build's real damage variable (corridors strong, open fields weak) — are behavioral with no 26-type carrier; a player keeps the spark-flood but loses the walls mattering. Duration/150-unit travel caps are numeric notes.

### poe1-spectral-helix — Spectral Helix
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> The corkscrew signature — the literal helix path, hits distributed along ~4.25 rotations, and the density-at-spiral-crossings texture (near-origin overlap shotgunning) — collapses to a line + wide-swath note; the player keeps 'throw spinning blades that grind through packs at attack speed', loses the helix choreography itself. Wall-bounce behavioral.

### poe1-split-arrow-bleed — Split Arrow Bleed
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Minor drift: 5-9 arrow count scaling, the no-double-hit-per-attack rule, and explosion magnitude tuning are behavioral; bleed, fan, swap-rotation, and on-kill pops all land on native lanes.

### poe1-sst — Spectral Shield Throw
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Minor drift: primary-vs-secondary pierce split and shard-count patch history are behavioral; defence-scaling approximated via door + affix lane. The throw-and-shatter loop itself lands cleanly.

### poe1-storm-brand — Storm Brand
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: 80%-more-to-branded-target split, 0.5s activation cadence, and multi-brand juggling are behavioral; the set-and-forget chained-lightning-while-you-move identity lands on chain + proc-loop + full-move chassis (mine/brand-chassis-via-trigger-grammar per b04 precedent).

### poe1-sweep — Sweep
**CLOSE · MAPPED** · elements: (silent) · ailments: knockback · **negative-canon (trap-kit)**
> Minor drift: 360-degree full circle rendered as wide melee arc (nearest member, noted); hit-cap and leveling-skill register are flavor. The stand-and-sweep knockback loop lands.

### poe1-tectonic-slam — Tectonic Slam
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Minor drift: every-3rd-slam charge cadence and the random branch-fissure spray are behavioral; charge-fed converted fire slam lands on native slam + charge-cycle + conversion lanes.

### poe1-tornado-shot — Tornado Shot
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Minor drift: no-double-hit-per-burst and secondary-range-from-projectile-speed are behavioral; the fire-at-point-then-radial-burst clear identity lands as multi_projectile propagation.

### poe1-toxic-rain — Toxic Rain
**CLOSE · MAPPED** · elements: earth · ailments: chill, poison
> Minor drift: per-pod stacking-slow cap, the 5-pod overlap breakpoint, and pod-burst timing are behavioral density parameters on one ground-DoT zone lane; the rain-pods-blanket-and-run identity lands (saturation door carries stack-density).

### poe1-viper-poison — Poison Assassin (Viper/Pestilent)
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Minor drift only: Pestilent's kill-burst consumes-remaining-poison math simplified to on-kill cascade; poison instance bookkeeping approximated by native stack cap. Identity (stack poison fast, kills pop the pack) intact.

### poe1-warchief — Ancestral Warchief
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Minor drift: the proximity-coaching buff becomes flavor (engine has no player-adjacency-buffs-proxy primitive); multi-totem count rides the proxy door rather than an Ancestral Bond analog. A Warchief player still recognizes plant-stand-slam.

### poe1-winter-orb — Winter Orb
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Minor drift: turret-projectile behavior vs orbit contact presence (noted, R-M6-spirit nearest-geometry call); decay pacing approximated. A Winter Orb player still recognizes channel-charge, run, personal blizzard turret.

### poe1-woc-ignite — Wave of Conviction Ignite
**CLOSE · MAPPED** · elements: fire · ailments: burn, sunder
> Minor drift: the one-touch-per-wave rule and the single-giant-ignite cap are simplified against engine burn application; exposure timing window approximated by sunder duration band. Identity (walk, cast one wave, one huge burn per body) intact.


## poe2 (27)

### poe2-blood-mage — Blood Mage
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed, sunder
> Minor drift: the 150%-of-max-life OVERHEAL buffer (the survivability core of the build -- you bank effective HP above your bar) is not expressible as a native key, so it degrades to a note + docket-candidate; the clamp of hp_cost_scale to 0.30 may under-state the source's Life pressure. Geometry+ailment+on-kill loop otherwise map cleanly, so CLOSE not APPROX.

### poe2-bonestorm — Bonestorm
**CLOSE · MAPPED** · elements: (silent) · ailments: root, sunder
> Minor drift: Bone Cage's exact shape is under-specified in source (only 'defensive panic button'), so its placed_lane+root mapping is a reasonable-but-thin inference. The core Bonestorm channel-release-Impale loop maps cleanly (geometry+sunder+accumulator), so CLOSE.

### poe2-cof-comet — Cast on Freeze Comet
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Minor drift: the two-layer trigger-ENERGY economy (freeze builds trigger energy that discharges Comet -- the exact mechanic 0.1.0d nerfed) is expressed only as 'free proc-cast', losing the energy-accumulation gate between freezes. The freeze->trigger->Comet loop and shatter payoff otherwise map cleanly via R-M9, so CLOSE.

### poe2-concoction — Concoction Pathfinder
**CLOSE · MAPPED** · elements: earth · ailments: poison · **negative-canon (trap-kit)**
> Minor drift: the flask-charge-as-ammo economy (your damage skill literally spends flask charges, gated by charge-recovery mods) maps to a cycle-shape + note but loses the tight flask-sustain-vs-fire-rate tension that IS the Pathfinder identity; the RNG element-variant framing (Poison/Fire/Ice from one Concoction chassis) is collapsed to the confirmed poison variant. Core throw-poison loop maps cleanly, so CLOSE.

### poe2-erasure-edc-lich — Erasure DoT Contagion Lich
**CLOSE · MAPPED** · elements: shadow · ailments: curse:amplify, drain
> Minor drift, and it is CLEAN: with the Erasure phantom removed per binding, the kit IS classic Essence-Drain/Contagion -- a chaos-DoT projectile + on-kill AoE-spread propagation -- which maps to GEOMETRY_PROPAGATION + drain almost exactly. The only loss is the unverifiable 'Erasure amplifies the spread chain' claim, which by ruling we grade as nonexistent. If Erasure is later confirmed real this may need revisit, but on current source CLOSE is honest.

### poe2-galvanic-shards — Galvanic Shards Merc
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: the two-stage projectile->beam transformation (bolts that BECOME chaining beams mid-flight) has no single 26-geometry member that carries both the fan-out AND the beam-chain, so fork (stage 1, dominant) + a GEOMETRY_PROPAGATION door (stage 2) approximate it -- the source player loses the visual of fragments morphing into forking beams as one continuous emission. The shotgun fan, lightning, shock, and armour-break-sunder all map cleanly, so CLOSE.

### poe2-gas-arrow-ignite — Gas Arrow Detonation
**CLOSE · MAPPED** · elements: earth+fire · ailments: burn, poison
> Minor drift: the two-stage place-then-detonate mechanic (a cloud you plant and then must IGNITE with a second skill) maps to a single ground_targeted_circle (the detonation) + an arming-stage note -- the source player loses the deliberate two-input setup/payoff rhythm and the cloud-expansion-over-time window (1.8m growing +80%). The detonation blast, hybrid fire/poison, and conversion all map cleanly, so CLOSE.

### poe2-howa-invoker — HoWA Invoker
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> A HoWA player would get flat-lightning melee that scales on GEAR AFFIXES rather than on an attribute-TOTAL -- the identity 'my stat page is my weapon' (damage as a linear function of stacked INT+DEX) is softened to a static added-damage affix. Playable output preserved (CLOSE); the missing coupling is a qualitative mint-candidate for steward review, kit graded un-minted.

### poe2-ice-strike-invoker — Ice Strike Invoker
**CLOSE · MAPPED** · elements: lightning+water · ailments: chill, freeze
> A minor drift: the two distinct accumulators the source exposes (Combo Points on Ice Strike AND Power Charges spent by Charged Staff) are modeled as one builder-spender accumulator + spend-burst; the player keeps the freeze->shatter payoff and the bank-then-dump feel, so the drift is the second charge-type's separate identity.

### poe2-infernal-legion — Infernal Legion Minions
**CLOSE · MAPPED** · elements: fire · ailments: burn
> The self-immolation-as-damage-source flavor (minions burn THEMSELVES to deal damage; their deaths are the payoff) is softened -- engine minion-proxy damage is the minion's own attacks, not a self-sacrifice burn loop. Proxy identity is expressible (CLOSE); the deviation is the suicide-burn mechanism reading as ordinary proxy damage.

### poe2-lightning-arrow-deadeye — Lightning Arrow Deadeye
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Two verified drifts noted: (1) engine chain hops sequentially and decays 0.7x/hop, whereas Lightning Arrow's beam splash is simultaneous at full damage to up to 3 targets -- a LA player's screen-clear is slightly weaker per-hop; (2) Lightning Rod's placed boss-zone is approximated as ground_targeted_circle rather than a shot-empowered rod. Both preserve the run-and-gun chain identity.

### poe2-lightning-spear-amazon — Lightning Spear Amazon
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: the secondary-bolt cascade is modeled as a multi_projectile shotgun + on-hit propagation; the source's specific crit-engine-triggers-on-fork-bolts amplification (crit density scaling off the secondaries) is carried in traits, not as a distinct mechanic -- the fanout clear identity is preserved.

### poe2-minion-infernalist — Minion Infernalist
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Behavioral delta (R-M8-adjacent): engine totems are STATIONARY while these minions PURSUE targets across the encounter -- the roaming-army feel is delivery flavor the stationary-totem geometry cannot fully carry. Proxy-army identity is expressible (CLOSE); the deviation is the mobility of the proxies.

### poe2-perfect-strike-01 — Perfect Strike (launch)
**CLOSE · MAPPED** · elements: fire · ailments: burn · **negative-canon (trap-kit)**
> A 0.1-launch player would 'miss' the specific pre-nerf degeneracy (always-Ignite at 45% base speed on a trivially-timed window) -- but that is a TUNING artifact, not a mappable mechanism; the engine has no 'trivially-timed window' anti-pattern to reproduce. The channel-charge-release fire-wave mechanism maps cleanly (CLOSE); the deviation is that the trap was balance, not a missing feature.

### poe2-poison-pathfinder — Poison Pathfinder
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Minor drift: the Pathfinder flask-charge-on-kill engine (extra charges on kill -> near-permanent flask uptime that POWERS poison scaling) is approximated as an on_kill recovery key + flask-effect traits; the specific flask-uptime-drives-damage coupling is softened. The one-button poison-explosion clear + place/detonate boss burst identity is preserved.

### poe2-rake-ritualist — Bleed Ritualist
**CLOSE · MAPPED** · elements: (silent) · ailments: bleed
> Drift from the flicker precedent: dash_attack captures the delivery, but the engine has no native 'apply-then-Disengage-OUT' hit-and-run RETREAT half of the loop -- the dash is modeled as an attack-approach, the strategic dash-away (the survival core of a Ritualist Rake) is delivery flavor. The dash-bleed-builder + Blood Hunt execution identity is preserved.

### poe2-smith-ignite — Smith of Kitava Ignite
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Minor drift: Weapon Heat maps cleanly as an accumulator, but the specific 'heat is generated by CRAFTING interactions' flavor (a forge-ascendancy meta-loop OUTSIDE combat) has no engine analog -- the accumulator is fed by in-combat proxies instead. The in-combat heat->ignite-magnitude behavior and the slam-ignite identity are faithful.

### poe2-snipe-mirage-deadeye — Snipe Mirage Deadeye
**CLOSE · MAPPED** · elements: water · ailments: freeze
> Minor drift: the freeze->Snipe interaction is a cross-skill setup (Ice Shot freezes, Snipe cashes the frozen-target bonus) that the engine models as two independent skills + a GEOMETRY_COLLAPSE door rather than a first-class 'bonus-vs-frozen' coupling; the player keeps the freeze-then-burst rhythm. Mirage Deadeye's clone-echo (repeat-my-attack) collapses to a self_buff+linked-cast trigger rather than spawned autonomous clones -- the 'my shots get doubled by ghosts' fantasy reads as a linked-cast proc. Both are recognizable-but-slightly-hollow, not identity-breaking.

### poe2-spark-stormweaver — Spark Stormweaver
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: (1) poe2 shock's damage-amp identity maps to sunder, so a Stormweaver player loses the specific 'shock = more-damage-taken from a lightning ailment' flavor read (functionally preserved as sunder's damage_taken_percent, the exact PoE band). (2) Archmage's 'my entire mana bar IS my damage number' coupling is expressed as a RESOURCE_CONVERSION door + an anti-reservation economy note rather than a bespoke mana-total->spell-damage scaler; the build's headline fantasy (stack mana, watch damage soar) is recognizable but its precise magnitude-coupling is door-level, not a first-class economy key. Kept CLOSE (not APPROX): the bouncing-projectile-flood core maps EXACT and the mana-coupling is a genuine strategy door, not an unmodelable gap.

### poe2-spiral-volley — Spiral Volley
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Minor drift: the Endurance->Frenzy charge-CONVERSION (build one charge type via Armour Break, transmute it to another via a keystone, spend that on the nova) is a two-currency laundering loop the engine models as a single charge-stack cycle + consume-mark; the player keeps the bank-then-dump burst rhythm but loses the specific 'wrong-charge-into-right-charge' conversion identity. The ring+6x-chain coverage maps cleanly. Kept CLOSE.

### poe2-supporting-fire — Supporting Fire Tactician
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Minor drift: the kit's minion-mediated delivery (minions physically loose the arrows on command) is compressed into a player-cast ground_targeted_circle with a PROXY_SOVEREIGNTY door -- the player keeps the 'designate zone, arrows rain' loop but loses the visible 'my squad fires on my command' proxy texture. The banner/squad-tactics fantasy (corpus mech_note) is thinner than a true commanded-proxy system would render it, but the every-3-seconds ACTION (place a 14m volley) maps cleanly. Kept CLOSE.

### poe2-tempest-bell — Tempest Bell Monk
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: Tempest Bell's defining texture -- a placed proxy that does nothing on its own and only pulses WHEN YOUR OWN MELEE HITS IT -- collapses into a totem (placed proxy) whose proc is expressed via trigger_grammar (on-hit-threshold -> resource-fill/pulse). The engine's totem is more autonomous than the bell's 'you must ring it yourself' dependency, so the player's 'I attack my own bell to weaponize it' loop reads as a more self-sufficient sentry. The dual-currency (Combo Points to summon + Power Charges to Falling-Thunder) is modeled as one accumulator + a charge bank. Recognizable, slightly-hollowed proxy identity -> CLOSE.

### poe2-tempest-flurry — Tempest Flurry Monk
**CLOSE · MAPPED** · elements: lightning · ailments: sunder
> Minor drift: the 4-hit RHYTHM cadence (each hit in the combo escalates, the 4th erupts) is the flurry's signature feel, and while melee_arc + a MOMENTUM_CASCADE door capture 'ramping repeated swings culminating in a burst', the engine has no first-class '4th-hit-of-a-fixed-combo erupts' beat -- the eruption reads as a generic finisher rather than a metered rhythm payoff. The dual Combo/Power-Charge currencies compress to one accumulator. The core melee-flurry-into-lightning-burst maps cleanly -> CLOSE.

### poe2-titan-hotg — Hammer of the Gods Titan
**CLOSE · MAPPED** · elements: (silent) · ailments: stun, sunder
> Minor drift: HotG's identity is a SETUP-GATED single nuke -- its full damage REQUIRES a fully-broken-armor + heavy-stunned target, a cross-skill prerequisite chain (Armour Breaker + Earthshatter + warcries -> then Hammer). The engine maps the pieces (ground_slam + sunder + stun + a GEOMETRY_COLLAPSE door) but expresses the 'HotG deals MORE into broken armor' coupling as a generic burst rather than a first-class conditional-damage gate; the player keeps the slow-wind-up-into-massive-slam feel and the break-then-hammer sequence, but the precise 'broken-armor multiplier' is door/trait-level. The colossal-slam core maps cleanly -> CLOSE.

### poe2-warbringer-totems — Ancestral Totem Warrior
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Minor drift: (1) the ENDURANCE-CHARGE-FUELED totem economy -- each totem COSTS 3 Endurance Charges to raise, coupling a defensive charge type to proxy deployment -- is expressed as an accumulator spend + a placed-proxy-count note rather than a first-class 'charges-buy-proxies' key; the player keeps the drop-totems-and-wait loop. (2) the up-to-10-simultaneous-totem swarm is a placed-proxy-COUNT extremum (accrual candidate to the placed-proxy-count family) that PROXY_FISSION approximates. (3) Wooden Wall's 'redirect my incoming damage TO my totems' proxy-tanking is noted but not first-class. The heavy-proxy identity (totems do all the work, Warrior tanks) maps cleanly via PROXY_SOVEREIGNTY -> CLOSE (recognizable, minor economy/count compression).

### poe2-whirling-assault-ma — Whirling Assault Martial Artist
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> A Hollow Form MA player gets a faithful spin-AoE with a charge-fueled proxy loop, but the CLONE MULTIPLICITY (multiple images each spinning simultaneously = output-multiplication by clone count) is softened: the engine models one whirlwind geometry + a linked-cast trigger, so the 'my clones spin for me and I just tap the button' identity lands as a single spin with a charge-accumulator feed rather than N parallel spinning bodies. That build, worse (R-M7) -> CLOSE; playable, the clone-count damage-multiplier is the fidelity loss noted.

### poe2-witchhunter-grenades — Grenadier Witchhunter
**CLOSE · MAPPED** · elements: fire · ailments: stun, sunder
> A grenade Witchhunter gets the kill-zone loop faithfully -- lob, pre-stack, detonate -- via ground_targeted_circle + ammo economy + burst-damage trigger. Minor drift: the FUSE-TIMING skill expression (grenades that sit and burn down before exploding, rewarding pre-placement) is carried as a burst-damage linked-cast rather than a first-class delayed-detonation timer; the engine has no native fuse-delay primitive, so 'time your throws so they all pop together' is approximated. That build, worse -> CLOSE, playable.


## tl1 (1)

### tl1-ricochet-vanquisher — Ricochet Vanquisher
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Wall-bounce detail (angle/reflect mechanic) not directly expressible in engine; ricochet_bounce geometry captures the shape. Explosive Shot secondary loop thinner than source.


## tl2 (2)

### tl2-arc-beam — Arc Beam Embermage (as primary)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none) · **negative-canon (trap-kit)**
> CLOSE not EXACT: the kit's negative identity and absence of element make it a real but thin mapping — no T4 doors, no ailments, no element. The source player would expect an Embermage kit and find a beam with no elemental scaling — which is exactly the attested identity.

### tl2-glaive-outlander — Glaive Outlander
**CLOSE · MAPPED** · elements: earth · ailments: poison
> CLOSE: Venomous Hail poison attested only in dossier payload characterization ('supplemental poison AoE'), not a direct game-text quote with 'deals poison damage' structure. The geometry+economy of the primary loop (ricochet physical glaive + charge) is EXACT; the poison element on the secondary skill is the approximation margin.


## tli (5)

### tli-carino2-lethal-flash — Carino 2 Lethal Flash
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Out-and-return double-hit trajectory has no direct engine geometry; multi_projectile captures the volley shape; return pass noted. Ammo reload economy approximated via cycle sub-shape.

### tli-erika3-vendetta — Erika 3 Vendetta's Sting
**CLOSE · MAPPED** · elements: water · ailments: freeze
> Frostbite 100-stack → instant freeze not directly expressible; engine freeze is binary. Vendetta auto-teleport + auto-trigger is a unique mode-shift mechanic approximated as dash_attack.

### tli-gemma-frost-caster — Gemma Frost Caster
**CLOSE · MAPPED** · elements: water · ailments: freeze
> Frostbite stacking threshold mechanic (0→100 → freeze burst) approximated; engine freeze is binary CC not a 100-stack ramp. Ice-Fire Fusion dual-element variant dropped (dominant cold loop wins per §7.2).

### tli-rehan-berserker — Rehan Berserker Melee
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Rage-auto-Berserk threshold mechanic approximated by charge-accumulator; exact Berserk stat-buff duration not expressible. Fire convert is T4 door variant, not base identity.

### tli-sage-elixir — Sage Elixir Kit
**CLOSE · MAPPED** · elements: fire+water · ailments: (none)
> Tri-element identity (all 3 equally weighted) loses one element in 2-slot mapping; fire+water chosen by genre convention (cold and fire as the most common pair). Lightning dropped noted.


## tq (12)

### tq-battlemage-warfare-earth — Battlemage
**CLOSE · MAPPED** · elements: fire · ailments: burn
> Physical melee component is present (Onslaught strikes) but maps no-family; a player used to a pure fire caster identity would feel the melee-physical half under-represented if engine surfaces only fire. T4 ELEMENT_CONVERSION_PHYSICAL captures the hybrid conversion door but the physical output itself is lost at element level.

### tq-distortion-templar — Distortion Wave Templar
**CLOSE · MAPPED** · elements: shadow · ailments: stun
> Shadow element derived from vitality→shadow crosswalk which the player would not intuitively recognize as 'shadow' — the game says 'vitality damage.' TQ players would miss the shadow labeling. Physical component (also present on Distortion Wave) is lost at element-slot level; identity is expressed through stun ailment + ring geometry.

### tq-druid-squall-caster — Druid Storm Caster
**CLOSE · MAPPED** · elements: lightning · ailments: blind
> Squall's lightning association is STRUCK (name-only); a TQ Druid player would expect lightning to feature prominently given the Storm mastery. The mapping surfaces lightning via Lightning Bolt but not Squall's zone. Blind from accuracy reduction is a source-mechanism inference — the store says 'reduce accuracy' not 'blind.'

### tq-elementalist-volcanic-storm — Elementalist Nuker
**CLOSE · MAPPED** · elements: fire+water · ailments: burn, chill
> Lightning from Storm mastery (Storm Surge passive procs) is not emitted — no damage-type descriptor found in fetched text for lightning on this kit specifically. A player would miss the Storm mastery feel. Stun from Fragmentation fragments is a real secondary output not carried in ailment list.

### tq-onslaught-assassin — Onslaught Dual-Wield Assassin
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Engine lacks the WPS-proc-pool mechanism (weighted auto-attack variant pool); mapped as on-hit-threshold trigger chain. Player would feel loss of the 'multiple weapon-swap variants' feel but core 'fast melee + poison overlay' identity is captured.

### tq-phantom-strike-dreamkiller — Phantom Strike Dreamkiller
**CLOSE · MAPPED** · elements: earth · ailments: drain, poison, stun
> Engine dash_attack captures teleport-strike feel. Dream Stealer 360-arc as trigger-linked ring burst is approximate (source pairs them inseparably; engine would model as chain depth 1). Player would feel the teleport-burst loop but miss the precise 'vanish→reposition' stealth feel.

### tq-ranger-hunting-nature — Ranger
**CLOSE · MAPPED** · elements: (silent) · ailments: curse:sap
> Pierce ranger maps cleanly to line geometry + companion proxy. Engine lacks TQ's 'pierce ratio' scaling system (gear affixes cover part of it). Player would feel the ranged loop but miss the deep pierce-ratio itemization identity.

### tq-rune-weapon-thunderer — Rune Weapon Thunderer
**CLOSE · MAPPED** · elements: lightning · ailments: shock
> Lightning melee converter maps well. Rune Weapon toggle-reserve is a close analog to engine tick-cost. Player would feel the lightning-enchant loop but miss TQ's unique 'Transmutation physical→elemental conversion' scaling system depth.

### tq-shield-charge-conqueror — Shield Charge Conqueror
**CLOSE · MAPPED** · elements: (silent) · ailments: stun
> Charge-tank maps cleanly. Engine dash_attack captures lane-charge. Player would feel the engage→sustain loop but miss TQ's deep block-stat itemization and the 'skill disruption' mechanic (no engine analog).

### tq-ternion-bone-charmer — Ternion Bone Charmer
**CLOSE · MAPPED** · elements: shadow · ailments: chill, curse:sap
> Shadow (vitality) triple-projectile caster maps well. Player would feel the projectile-spam loop with resistance-debuff layer. Miss: vitality damage as a distinct game mechanic (life-drain register nuance), and the staff-weapon identity constraint.

### tq-thane-storm-warfare — Thane Storm-Warrior
**CLOSE · MAPPED** · elements: lightning · ailments: stun
> Lightning dual-wield warrior maps well. Engine captures the enchanted-melee + zone combo. Player would feel the fast melee with lightning explosions but miss TQ's DW proc pool depth and the Spellbreaker nerf context that makes this build more fragile.

### tq-warlock-poison-vitality — Warlock (Rogue+Spirit)
**CLOSE · MAPPED** · elements: earth+shadow · ailments: chill, curse:sap, drain, poison
> Dual-DoT caster (earth+shadow) maps cleanly. Player would feel the poison-spray + vitality sustain loop. Miss: construct immunity interaction (design fallback mechanic) and TQ's vitality resistance reduction stacking depth.


## tq2 (3)

### tq2-elementalist — Elementalist (TQ2)
**CLOSE · MAPPED** · elements: fire+lightning · ailments: (none)
> A TQ2 Elementalist (Storm+Earth) gets the dual-element stack-nuker faithfully -- big fire AoE + chunky lightning zone + Amplify/Overload accumulator + cross-element echo door. Minor drift: the Amplify+Overload TWO-STACK-SYSTEM interplay (Roiling Magma dumps both, Call Lightning charges Amplify, Cyclone must cleanse Overload to avoid a downside) is carried as a single accumulator + apply-mark; the engine models one stack meter cleanly but the two-resource management texture (build Amplify, dump/cleanse Overload) is simplified. That build, worse -> CLOSE.

### tq2-forge-turrets — Forge Turrets
**CLOSE · MAPPED** · elements: fire · ailments: (none)
> A Forge turret player gets the placed autonomous fire-proxy screen faithfully -- totem geometry + proxy-ascension doors + count economy. Drift: the SPECIFIC 8-trap concurrent-stack CAP (the density identity: lay MORE devices for MORE coverage, up to 8) exceeds the engine's default placed-proxy count and accrues to the placed-proxy-count family (already a mint class); mapped un-minted, so 'stack a big screen of 8 devices' is carried as a placed-proxy accumulator rather than a first-class 8-count cap. That build, worse -> CLOSE (playable proxy screen; the exact 8-count density is the accrual).

### tq2-whirlwind-rogue — Whirlwind Rogue
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> A TQ2 Whirlwind (Warfare) player gets the mobile spin-to-win faithfully -- whirlwind geometry (poe1-cyclone precedent, full-movement-during-channel is native) + tick-cost channel + Rage accumulator + spin-momentum doors. Minor drift: 'the ONLY skill where you can keep moving while channeling' is a game-relative uniqueness that the engine can't express as special (many engine channels may allow movement), so the standout 'mobile-while-everyone-else-is-rooted' identity is carried as a normal mobile channel -- the feel is right, the game-relative distinctiveness is flattened. That build, worse -> CLOSE.


## undecember (5)

### ud-cwc-spin-caster — Whirlwind CwC Blizzard (Ya55)
**CLOSE · MAPPED** · elements: water · ailments: chill, freeze
> Engine maps two discrete skills (whirlwind + ground circle). Source player would recognize the CwC proc trigger shape but the physical/cold split across two geometry slots may feel less fluid than the original spin-and-trigger single experience.

### ud-illusion-family — Illusion Family (Arrow/Axe/Hook)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Source player expects weapon-type flavor differentiation (Arrow vs Axe vs Hook) with distinct range profiles per variant. Engine maps two geometry slots which captures the ranged/melee split but loses the three-way weapon-type identity granularity.

### ud-lightning-vortex — Lightning Vortex Mapper
**CLOSE · MAPPED** · elements: lightning · ailments: (none)
> Lightning element cannot be attested from the rune page; source player of this build expects a lightning identity. Melee-arc+zone is a genuine map of the swing+vortex mechanic but the absence of lightning element loses the elemental flavor the build creator intends.

### ud-seal-veil-daimonios — Seal/Veil Resource Build (Daimonios)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Kit identity is the reservation-economy lattice supporting Lightning Vortex; standalone mapping without the LV primary damage loop gives an incomplete player picture. Source player would miss that this is a support-system kit, not a standalone build.

### ud-toxic-flame — Toxic Flame DoT
**CLOSE · MAPPED** · elements: earth · ailments: poison
> Corpus claimed small-AOE and dual-element (poison+fire); attested identity is piercing-line poison-only. Source player would recognize the hit-and-walk DoT pattern but the range/spread difference from AOE splash is material.


## vs (12)

### vs-bloody-tear — Bloody Tear (Whip evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Engine lacks the precise 'heal-on-crit' trigger chain natively; mapped as on-crit resource-fill which captures intent. Crit system approximated via proc_trigger_condition. No ailments in VS roguelite context.

### vs-death-spiral — Death Spiral (Axe evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Engine orbit geometry maps the delivery well. Pool-limit saturation mechanic (50 active persistent projectiles) approximated via PERSISTENCE_ENGINE_saturation — engine has no direct pool-limit analog; fidelity note required.

### vs-fuwalafuwaloo — Fuwalafuwaloo (Vento Sacro+Bloody Tear union)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Dual geometry (melee_arc + orbit simultaneously) is non-standard; engine skill chains are sequential not simultaneous — approximated as two skill entries. Movement-damage ramp approximated via MOMENTUM_CASCADE.

### vs-heaven-sword — Heaven Sword (Cross evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: knockback
> out-and-return boomerang double-pierce is approximated via placed_lane — engine does not natively distinguish outbound vs return-path pierce. Extreme knockback is attested and emitted. Minor fidelity loss on the double-traversal nuance.

### vs-hellfire — Hellfire (Fire Wand evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Identity maps well to placed_lane large-projectile delivery. Primary fidelity loss: fire+burn theme is visible to players but structurally absent from mapping per law. Engine representation is geometry-pure, missing the expected elemental feel.

### vs-holy-wand — Holy Wand (Magic Wand evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> single_target maps the non-pierce nearest-enemy delivery. No ailments, no element. Primary fidelity loss: holy name registers as holy-identity to players but is structurally absent per law.

### vs-la-borra — La Borra (Santa Water evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> Mobile growing puddle behavior (follow player, grow in travel) is approximated by ground_targeted_circle — engine has static circles, not self-relocating ones. Minor fidelity loss on the 'follows player' component.

### vs-phieraggi — Phieraggi (guns union)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE: engine orbit geometry captures rotating laser ring well. What source player misses: the revive-stock-as-power economy has no direct engine analog — the nearest T4 (RESOURCE_CONVERSION) approximates the conversion shape but not the stock-as-amplitude escalation.

### vs-runetracer-no-future — No Future (Runetracer evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE: ricochet_bounce geometry and cascade T4 door capture the identity. What source player misses: the dual explosion trigger (wall bounce AND enemy hit) creates a richer cascade geometry than single-condition ricochet; Armor-as-explosion-scalar is an atypical stat routing not in the engine economy.

### vs-soul-eater — Soul Eater (Garlic evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: drain
> CLOSE: circle aura geometry and drain ailment capture the identity. What source player misses: the lifesteal-to-damage ramp mechanic (HP-healed as damage accumulator) has no direct engine analog; the cap-gated ramp shape (60 HP per +1 damage, cap +60) is more nuanced than the engine's ramp_per_s key.

### vs-thunder-loop — Thunder Loop (Lightning Ring evo)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE: single_target geometry captures at-target random-strike delivery. What source player misses: the double-hit 'loop' mechanic (second strike same location with delay) has no engine analog — it reads as doubled hit-count, but the spatial lingering creates a zone-presence effect the engine cannot represent.

### vs-vandalier — Vandalier (Peachone+Ebony Wings union)
**CLOSE · MAPPED** · elements: (silent) · ailments: (none)
> CLOSE: orbit + companion geometry captures the flying-bird-with-bomb-zones identity. What source player misses: slot liberation (freeing a weapon slot by fusing two weapons into one) is a VS-specific loadout-economy mechanic with no engine analog; the dual CW/CCW bomb zones create a symmetric orbit pattern the engine orbit geometry does not distinguish.

