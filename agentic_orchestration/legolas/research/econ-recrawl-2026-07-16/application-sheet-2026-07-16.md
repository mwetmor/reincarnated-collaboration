# Application Sheet — Econ Re-crawl 2026-07-16

**For:** Elrond (mechanical DB application)
**Crawl date:** 2026-07-16
**Wave-B spec bins:** spend (existing) | persistent-condition (PC) | reservation (RS) | charge-stack/accumulator (AM) | charge-stack/cycle (RC) | HP-economy/LC (Wave-C deferred) | damage-taken-converts (Wave-C deferred)
**Ailment map:** existing 8 (bleed/burn/chill/consecrate/drain/knockback/root/shock) + wave-in-flight 4 (sunder/freeze/stun/poison) + wave-c+ (blind/fear/curse-hex/deflect/instant-kill)

Iron law: every row cites ≥1 live URL or is marked UNVERIFIABLE. Row counts reconcile with index summary block (17 classify / 3 unverifiable = 20 total).

---

## ECON BATCH (18 kits)

---

### 1. `d2-wl-abyss` — Abyss Warlock (D2 RotW)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** steady mana-spend (no generator; sustained with Hex: Siphon kill-based mana return + Insight merc Meditation aura)
**live URL(s):**
- https://maxroll.gg/d2/guides/abyss-warlock-build-guide
- https://maxroll.gg/d2/guides/abyss-warlock-leveling-build-guide
**evidence quote:** "Cast Hex: Siphon for passive Life and Mana gain on enemy death. This does not require you to attack with your weapon." / "Insight Giant Thresher for the Meditation Aura to help manage resources" — mana is the spend resource; no generator-skill loop, no reservation, no charge meter.

---

### 2. `d2-wl-echoing-strike` — Echoing Strike Warlock (D2 RotW)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** steady mana-spend with leech sustain (no generator; sustained via Mana Stolen per Hit gear + Insight merc Meditation aura)
**live URL(s):**
- https://maxroll.gg/d2/guides/echoing-strike-warlock-guide
- https://odealo.com/articles/echoing-strike-warlock-build-for-diablo-2-resurrected
**evidence quote:** "Mana is easily sustained through equipment." / "Energy: Nothing — players should not invest in the Energy attribute since mana sustain comes from gear rather than base stats." — pure mana spend; no auras/reservations; no charge meter.

---

### 3. `d2-wl-fire` — Fire Warlock (D2 RotW)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** starved/intensive mana-spend (guide explicitly notes "High Mana Requirements"; early Energy stat investment needed; Insight merc mandatory for regen)
**live URL(s):**
- https://maxroll.gg/d2/guides/fire-warlock-guide
- https://www.icy-veins.com/d2/fire-warlock-build
**evidence quote:** "High Mana Requirements" (listed as con) / "10-15 points in Energy to counteract high Mana Cost (not needed once you have Insight)" — mana spend, intensively managed; nearest existing bin is `starved` (resource-hungry spend variant) but fundamentally still a spend model.

**NOTE for Elrond:** `d2-wl-fire` DB row already carries `ctrl_ailments_mapped=["burn"]` — that is correct per live evidence (Apocalypse + Flame Wave are fire DoT). No ailment gap here.

---

### 4. `d2-wl-void-rift` — Void Rift Warlock (D2 RotW)

**disposition:** **unverifiable**
**target bin:** n/a
**sub-shape:** n/a
**live URL(s):**
- https://maxroll.gg/d2/category/guides/warlock (no Void Rift build listed)
- https://www.icy-veins.com/d2/warlock-class-and-builds (no Void Rift build listed)
- https://egamersworld.com/blog/diablo-ii-resurrected-receives-the-reign-of-the-wa-Izw9xGe7sy
**evidence quote:** "Abyss combined with Void Rift creates massive void zones" (ixbt.games secondary cite) — Void Rift appears in tier-list commentary as a damage style name, not a distinct build with its own guide. No standalone Void Rift build guide found on Maxroll/Icy-Veins/Odealo for Season 13/14. It is likely a Chaos-tree magic/void school variant, same mana-spend economy as Abyss Warlock, but no dedicated guide confirms resource model independently. UNVERIFIABLE pending a dedicated guide landing.

---

### 5. `d4-blazing-abyss-warlock` — Blazing Abyss Warlock / Blazing Scream Warlock (D4)

**disposition:** **classify**
**target bin:** `spend` (generator-spender)
**sub-shape:** Wrath generator-spender; Command Fallen generates Wrath; Blazing Scream spends Wrath until depleted; cycle repeats
**live URL(s):**
- https://maxroll.gg/d4/build-guides/blazing-scream-warlock-leveling-guide
- https://www.icy-veins.com/d4/guides/blazing-abyss-warlock-build/
**evidence quote:** "Command Fallen is the total package for generating both of your Primary Resources... generate tons of Wrath." / "Blazing Scream consumes Wrath to cast repeatedly: 'You can cast as many in a row as you have Wrath and attack speed to manage!'" / build described as "Resource Hungry" — canonical generator-spender on Wrath resource.

**NOTE:** DB folk_name was "Blazing Abyss Warlock" but meta-name evolved to "Blazing Scream"; Icy-Veins guide still uses "Blazing Abyss." Both confirmed same build. The Shadowform stack mechanic (Icy-Veins guide) is a secondary stealth layer on top of the Wrath generator-spender core. Primary econ = spend.

---

### 6. `d4-dread-claws-warlock` — Dread Claws Warlock (D4)

**disposition:** **classify**
**target bin:** `charge-stack` sub-shape: `accumulator` (AM)
**sub-shape:** Shadowform stacks accumulate via Metamorphosis (4 stacks/second from Terror Demon); Dread Claws consumes stacks; secondary resource Dominance fuels Rampage
**live URL(s):**
- https://maxroll.gg/d4/build-guides/dread-claws-warlock-guide
- https://www.icy-veins.com/d4/guides/dread-claws-warlock-build/
**evidence quote:** "Shadowform is generated by Metamorphosis Terror Demon, Nether Step, Command Laalish & Sigil of Subversion, and is consumed by movement & casting Dread Claws. Terror Demon Metamorphosis gives 4 stacks of Shadowform every second." — fill-from-event (timed + skill-use), discharge on Dread Claws activation = AM accumulator pattern.

**NOTABLE FIND — contradiction-flag for Elrond/gandalf:** D4 Shadowform stack system does not cleanly map to Wave-B AM `accumulator_fill_trigger` enum. The fill is TIME-BASED (4 stacks/s from a persistent passive demon) rather than `on-kill`, `on-hit-taken`, `on-hit-dealt`, `on-evolution-condition-met`, or `on-corpse-consume`. The Wave-B spec §4.4 `accumulator_fill_trigger` enum does not include `on-time-tick`. This is NOT a contradiction of the bin definition (AM = fills from external events, discharges on activation — the passive demon IS an external event generator), but the fill trigger sub-value has no current enum match. Flagged for spec-author (gandalf) attention: Wave-B AM spec §4.4 may need `on-passive-aura` or `on-time-tick` added to `accumulator_fill_trigger` to cover this corpus shape. Bin classification (AM accumulator) remains correct; the sub-field gap is a spec extension.

---

### 7. `d4-hammerdin-paladin` — Hammerdin Paladin (D4)

**disposition:** **classify**
**target bin:** `spend` (generator-spender)
**sub-shape:** Faith generator-spender; Rally generates Faith; Blessed Hammer (and aura maintenance) spends Faith
**live URL(s):**
- https://maxroll.gg/d4/build-guides/blessed-hammer-paladin-guide
- https://www.icy-veins.com/d4/guides/blessed-hammer-paladin-build/
**evidence quote:** "Ring of Starless Skies is mandatory to sustain our Faith... with Ring of Starless Skies + Argent Veil, one Faith per Second Affix is just enough to sustain Faith" / "Rally is cast to regenerate Faith whenever necessary" — Faith is the named D4 Paladin resource; generator-spender pattern on Faith. Auras are present (Fanaticism, Defiance) but their maintenance is cooldown/CD-stacked, not reservation. Primary econ = spend (Faith).

---

### 8. `d4-rabies-lacerate` — Rabies Lacerate Druid (D4)

**disposition:** **classify**
**target bin:** `spend` (generator-spender with persistent form rider)
**sub-shape:** Spirit generator-spender; Rabies costs 30 Spirit; Lacerate costs 100 Spirit (made Core by Mad Wolf's Glee); Spirit generated via Gift of the Stag, Blood Howl, Energize; persistent Werewolf form maintained via Dark Howl (form-lock is mechanical necessity, not a separate economy bin — it preserves Talisman Set buffs)
**live URL(s):**
- https://www.icy-veins.com/d4/guides/rabies-lacerate-druid-build/
- https://mobalytics.gg/diablo-4/builds/druid-rabies-endgame
**evidence quote:** "Lacerate costs 100 Spirit (enabled by Mad Wolf's Glee unique)... Gift of the Stag Spirit Boon gives 5 Spirit Generation... Spirit-intensive build" — canonical generator-spender on Spirit. Werewolf form persistence is a buff-preservation mechanic layered on top, not a separate PC/RS bin in its own right.

**NOTE for Elrond/gandalf:** The form-lock component is GX-02 docket (shapeshift-form-lock economy). The MIGRATION class-(b) sketch family `SS (shapeshift-form-lock)` from the prior audit applies here. Primary econ classification is `spend` (Spirit generator-spender). If SS is ever minted as a new bin, this kit may carry a secondary `["spend", "SS"]` overlap. For now: `spend`.

---

### 9. `gd-berserker-wereforms` — Berserker (FoA mastery, Grim Dawn)

**disposition:** **classify**
**target bin:** `persistent-condition` (PC)
**sub-shape:** `activation-toggle` — wereform (werewolf / wereraven) is a temporary-but-toggleable transformation state that persists while active; duration extendable to permanent via items/passives; no per-tick drain stated; Winds of Asterkarn cold-infused weapon attacks are wereform-state-enabled
**live URL(s):**
- https://www.grimdawn.com/guide/character/masteries/berserker/
- https://massivelyop.com/2026/06/01/grim-dawns-fangs-of-asterkarn-expansion-adds-a-frosty-new-realm-and-a-shapeshifting-mastery-line-july-23/
- https://grimdawn.fandom.com/wiki/Fangs_of_Asterkarn
**evidence quote:** "assume the form of a bloodthirsty werewolf, or an enigmatic wereraven, each offering unique advantages in the thick of battle" / "Transformations are temporary, and Berserker has means to extend their duration or even to make them permanent" / "harness the bitter unforgiving winds of Asterkarn to infuse their weapons and shatter their foes" — persistent toggle-state form; cold-infused weapon attacks while in form.

**NOTE on ailment:** DB row already carries `ctrl_ailments_mapped=["chill"]`, `ctrl_ailment_gaps=["GAP-AILMENT:freeze"]`. Cold/frost weapon infusion strongly implies frostbite or freeze adjacency. GD uses "Frostbite" (a damage resistance reduction debuff) and "Freeze" as distinct ailments. Wereraven is explicitly ranged + ice magic. Evidence is consistent with freeze application but no explicit source lists "Freeze" vs "Frostbite" for the specific kit. The `GAP-AILMENT:freeze` flag stands — econ (PC/activation-toggle) is classified; ailment gap for freeze is NOT resolved by this pass (insufficient specificity from available sources).

---

### 10. `poe1-heavy-strike-stun` — Heavy Strike Stun Berserker (PoE1 3.28)

**disposition:** **classify**
**target bin:** `charge-stack` sub-shape: `accumulator` (AM)
**sub-shape:** Rage accumulates passively + through attacks; Trauma stacks also accumulate on Heavy Strike hits (via Trauma Support); Berserk activated when stacked — discharge burst; endurance charges from Enduring Cry and Melee Stun Support are secondary riders
**live URL(s):**
- https://mobalytics.gg/poe/builds/stun-heavy-strike-berserker
- https://www.mmoexp.com/News/path-of-exile-the-complete-guide-to-the-sir-bongsalot-stun-build.html
**evidence quote:** "Build trauma stacks (targeting 40+) and rage through continuous Heavy Strike attacks" / "With 114 rage and 110% increased rage effect from Berserk and Right of Ruin, the total damage multiplier reaches 239% more damage" — Rage accumulates through attacks (on-hit-dealt fill trigger), discharges via Berserk activation = AM accumulator. Mana exists but is minimal concern ("Mana Mastery for reduced mana costs").

**NOTE on ailment:** DB row carries `ctrl_ailment_gaps=["GAP-AILMENT:stun"]`. Heavy Strike Berserker is a stun-primary build. Stun is a wave-in-flight ailment. Classification: `stun` (confirmed). Elrond may choose to write this ailment gap alongside the econ fill.

---

### 11. `poe1-kinetic-fusillade` — Kinetic Fusillade (PoE1 3.27/3.28)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** steady mana-spend (mana cost 4–6 per activation, scales with gem level; aura reservation layer — Wrath/Clarity used, noted as significant; no charge meter for the skill itself)
**live URL(s):**
- https://maxroll.gg/poe/build-guides/kinetic-fusillade-ballista-hierophant-league-starter
- https://www.pathofexile.com/forum/view-thread/3876136
**evidence quote:** "Kinetic Fusillade is an Attack, Projectile, Duration, AoE skill with a mana cost of (4-6)" / "Wrath, spellslinger tornado... reserve mana but provide damage scaling" / "Clarity auras help with mana, but make sure you don't level it too high or your reservation might be too high" — primary econ is mana spend per cast; aura reservation is a secondary support layer. Primary bin = `spend`.

**NOTE:** The aura reservation (Wrath + Clarity) is an `RS` rider on top of the `spend` core — the kit's primary bin classification remains `spend` per the single-bin-per-kit contract (§5.3 Wave-B spec). RS is the support layer, not the main economy loop.

---

### 12. `poe2-archmage-totems` — Archmage Totems Oracle (PoE2 0.5)

**disposition:** **classify**
**target bin:** `reservation` (RS)
**sub-shape:** flat spirit reservation per totem (Ancestral Bond: 75 Spirit per totem reserved; reducible to 63 via Efficient Inscriptions); Archmage adds mana-as-damage-scaling (not a mana-spend cost — mana is a stat, not a resource depleted per cast)
**live URL(s):**
- https://maxroll.gg/poe2/build-guides/grim-pillars-spell-totem-oracle-build-guide
- https://allthings.how/path-of-exile-2-oracle-spell-totem-build-how-the-spirit-trick-works/
**evidence quote:** "Each Spell Totem then reserves 75 Spirit" / "Archmage adds extra lightning damage based on your maximum Mana... with a large enough Mana pool, that bonus pushes past 100% extra damage" — Spirit reservation per totem is the core cost structure. Mana is a damage-scaling stat amplified by Archmage, not a per-cast spend. Bin = RS (flat reservation, spirit pool).

**NOTE for gandalf/spec-author:** this is the first RS corpus case where the reserved RESOURCE is Spirit (a PoE2-specific summon/reservation pool), not mana or focus. The Wave-B spec §3.4 `reservation_resource` field currently enumerates `{"mana", "focus", "stamina-as-resource", "rage"}`. Spirit is absent. This is NOT a bin contradiction — RS is correct — but the `reservation_resource` enum needs a `spirit` value to represent this kit. Flagged as spec extension (not a blocker for classification).

---

### 13. `poe2-shaman-bear` — Shaman Bear (PoE2 0.5)

**disposition:** **classify**
**target bin:** `persistent-condition` (PC)
**sub-shape:** `activation-toggle` — Bear Form is a persistent shapeshift state; Rampage (bear auto-attack) generates Rage; Furious Wellspring prevents Rage decay (makes form-state sustainable); spirit reservation layer (140+ spirit for aura gems: Clarity, Herbalism, etc.) is a secondary RS rider; Glory accumulates when Rage is full (secondary AM rider for Walking Calamity, but the BUILD's primary identity is the PC bear-form state)
**live URL(s):**
- https://maxroll.gg/poe2/build-guides/demon-calamity-bear-shaman-build-guide
- https://overgear.com/guides/poe-2/shaman-bear-druid/
**evidence quote:** "Furious Wellspring... stops you from ever losing Rage, meaning you start every encounter with full damage bonus" / "Bear runs on Rage" / "a total of 360 spirit BEFORE the keystone" for aura reservation — Bear Form is the persistent toggle state. Rage fuels within-form attacks. Spirit reservation maintains auras while in form.

**NOTE for Elrond:** this kit has overlapping bin signals: PC (bear form), RS (spirit aura reservation), AM (glory accumulation for Walking Calamity). Per §5.3 single-bin contract, the primary bin for this kit's corpus classification is PC (the defining economy identity is the persistent bear form toggle). The RS and AM layers are riders.

---

### 14. `poe2-snipe-mirage-deadeye` — Snipe Mirage Deadeye (PoE2 0.5)

**disposition:** **unverifiable**
**target bin:** n/a
**sub-shape:** n/a
**live URL(s):**
- https://pathofexile2.wiki.fextralife.com/Mirage+Deadeye+(Meta+Skill)
- https://www.poe2wiki.net/wiki/Snipe
**evidence quote:** Snipe costs "(17-118) Mana per second" as a channeled skill / Mirage Deadeye is a meta-skill buff (10s cooldown) that causes mirages to fire when player fires ranged attacks — including channeled skills as of 0.5. However, no dedicated Snipe Mirage Deadeye build guide was found with a clear economy classification. The interaction is: Snipe channels (mana/second cost), Mirage Deadeye buffs are persistent (PC activation-toggle) that triggers mirage copies. Snipe's own economy is `spend` (mana/second channeled). But the BUILD identity as "Snipe Mirage Deadeye" conflates the skill (Snipe = spend) with the buff layer (Mirage Deadeye = PC). No single authoritative build guide identifies which layer is economically dominant (Snipe with low mana? Or Mirage Deadeye PC as the defining mechanic?). UNVERIFIABLE for single-bin classification — the build name represents a two-mechanism interaction and no guide resolves the primary economy identity.

**NOTE:** If Elrond can resolve from raw_json which mechanism was corpus-captured as primary (Snipe the channel skill vs Mirage the meta-skill buff), classification may be possible without further crawl. Evidence is present for both layers; the bin resolution requires editorial judgment, not additional evidence.

---

### 15. `poe2-spiral-volley` — Spiral Volley (PoE2 0.5)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** intensive mana-spend (mana cost 6–64 scaling with gem level; mana per kill recommended on gear; frenzy charges are a damage-scaling layer not a cost resource)
**live URL(s):**
- https://maxroll.gg/poe2/build-guides/spiral-volley-deadeye-build-guide
- https://www.poe2wiki.net/wiki/Spiral_Volley
**evidence quote:** "Spiral Volley is an Attack, Projectile skill with a mana cost of (6-64) based on level" / "Mana can be a problem on this build... solutions include mana flasks, Jewels providing 'Recover 2% of Mana on Kill'" — direct mana-spend per cast. Frenzy charge generation (via charge conversion passive) is a damage buff, not a cost resource. Spirit reservation (Herald of Thunder, Wind Dancer) is present but passive; primary economy = spend.

---

### 16. `poe2-walking-calamity` — Walking Calamity Autobomber (PoE2 0.5 Shaman)

**disposition:** **classify**
**target bin:** `charge-stack` sub-shape: `accumulator` (AM)
**sub-shape:** Glory accumulates when Rage is at maximum and further Rage is gained; 50 Glory consumed to activate Walking Calamity; WC then runs for 20+ seconds autonomously
**live URL(s):**
- https://maxroll.gg/poe2/build-guides/walking-calamity-shaman-build-guide
- https://www.mmoexp.com/News/path-of-exile-2-walking-calamity-druid-build-guide.html
**evidence quote:** "Walking Calamity requires 50 Glory to use. You gain Glory while having full Rage." / "Activate it to cause large meteors to constantly rain down from the sky for over 20 seconds" — Glory accumulates from Rage-overflow events (on-max-rage-overflow fill trigger); discharged by Walking Calamity activation. Classic AM accumulator: world-driven fill (Rage overflow = world event), player-triggered discharge.

**NOTABLE FIND — spec extension flag:** The `accumulator_fill_trigger` enum in Wave-B spec §4.4 (`{"on-kill", "on-hit-taken", "on-hit-dealt", "on-evolution-condition-met", "on-corpse-consume"}`) does not include `on-resource-overflow`. The Glory accumulation triggers on Rage-at-max + additional-Rage events, which is a resource-overflow trigger pattern. Same gap flagged on `d4-dread-claws-warlock` (time-based passive) — both suggest `accumulator_fill_trigger` enum needs `on-resource-overflow` and/or `on-passive-tick` additions. **This is the clearest Wave-B spec bin-definition tension in the batch: AM accumulator is the right bin, but the fill-trigger sub-field enum is incomplete for these D4/PoE2 corpus shapes.**

---

### 17. `poe2-whirling-assault-ma` — Whirling Assault Martial Artist (PoE2 0.5)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** mana-spend per activation (Whirling Assault has high mana cost, managed via Conservative Casting support + mana sustain gear); power charges are a secondary damage layer (generated via Devour, spent for damage buffs), not the primary economy resource; spirit reservation for support auras is a minor RS rider
**live URL(s):**
- https://maxroll.gg/poe2/build-guides/whirling-assault-martial-artist-build-guide
- https://boostmatch.gg/blog/poe-2/articles/poe2-martial-artist-monk-whirling-assault-build-guide
**evidence quote:** "skills ramped mana consumption extremely high... temporarily add Conservative Casting for its Mana Cost Efficiency if you struggle for Mana sustain" / "generate Power Charges... spending Power Charges will summon 2 additional clones" — mana is the operating cost (spend); power charges are a damage-multiplier mechanic, not the primary resource. Primary bin = `spend`.

---

### 18. `vs-out-of-bounds-freeze` — Out of Bounds Freeze Build (VS)

**disposition:** **classify**
**target bin:** `persistent-condition` (PC)
**sub-shape:** `activation-toggle` — arcana slot is occupied for entire run duration; no per-tick drain; Out of Bounds is "always on" once selected (persistent run-state flag); the build invests in the arcana slot as its economy (the cost IS the arcana-slot opportunity cost, analogous to D2 Warlock aura taking up a skill slot)
**live URL(s):**
- https://vampire.survivors.wiki/w/Out_of_Bounds_(XII)
- https://vampire-survivors.fandom.com/wiki/Out_of_Bounds_(XII)
**evidence quote:** "Once active, the effect persists throughout the run without charge depletion or maintenance costs" / "Selecting Out of Bounds (XII) Arcana allows the freezing beam to create explosions when they hit enemies" — arcana slot = the upfront investment; run-persistent passive = activation-toggle PC shape. DB resource_verbatim reads "arcana-authored stack (arcana slot investment)" which matches.

**NOTE on ailment:** Out of Bounds does NOT apply freeze — it REACTS to freeze applied by other weapons (Clock Lancet, Celestial Voulge, Icebrand, Orologions). The VS kit's ailment identity as "freeze build" refers to the weapon layer (freeze is applied by the carry weapon), not the arcana itself. DB `ctrl_ailment_gaps=["GAP-AILMENT:freeze"]` on this kit is correctly flagged — the arcana amplifies freeze but doesn't emit it. The freeze ailment is attributed to the weapon complement, not this build-slot entry. Elrond's discretion on whether to resolve the gap as "freeze" (weapon-layer) or leave it as unemitted-by-this-mechanic.

---

## AILMENT BATCH (2 kits)

---

### 19. `di-warlock-launch` — Warlock launch state (Diablo Immortal, Update 5.0 June 2026)

**disposition:** **classify**
**ailment(s):** `burn`, `bleed`, `stun`, `knockback`
**live URL(s):**
- https://news.blizzard.com/en-us/article/24277443/introducing-diablo-immortals-newest-class-warlock
- https://mmokb.com/diablo-immortal-warlock-class-guide/ (403; evidence from Blizzard official page)
**evidence quote:** "Infernal Plague (damage-over-time, spreads via defeated enemies)" / "Burning Ascent" / "Blood Offering: applying bleed to nearby enemies" / "Stun (loss of control)" / "Knockback/Knockup (displacement effects)" — launch skill set applies burn (fire DoT), bleed (DoT), stun (hard CC), knockback (displacement). The Warlock also has life-tap mechanics (Spiteful Sacrifice, Devouring Darkness consume health — LC-adjacent) but econ is already DB-classified as `cooldown/native` and is outside this batch's scope.

**NOTE:** DB row already has `ctrl_ailments_mapped=[]` and `ctrl_ailment_gaps=["GAP-AILMENT:unknown-ailment"]`. This row resolves the unknown-ailment gap. Mapped ailments from live evidence: burn + bleed + stun + knockback. Stun and burn are in the active ailment taxonomy (wave-in-flight and existing-8 respectively). Bleed is existing-8. Knockback is existing-8. No novel ailments; all map to existing taxonomy.

---

### 20. `di-spiritform-druid-pvp` — Spirit-Form Druid PVP (Diablo Immortal, complaint-tier)

**disposition:** **unverifiable**
**ailment(s):** n/a
**live URL(s):**
- https://blizzardwatch.com/2025/06/26/diablo-immortal-druid-class/
- https://news.blizzard.com/en-us/article/24216435/introducing-diablo-immortals-newest-class-druid
- https://diablo.fandom.com/wiki/Druid_(Diablo_Immortal) (402 access denied)
**evidence quote:** "No Spirit Form skill is mentioned" (multiple sources) / Druid skills listed: Ferocious Strike, Landslide, Fire Tornado, Stag Charge, Summon Wolves, Earthquake, Raven Swarm, Thorn Armor, Summon Grizzly, Summon Oak Sage, Circle of Life, Surging Stone, Rabid Might + Werewolf + Werebear transformations — no skill named "Spirit Form" exists in any official or community source found. The folk_name "Spirit-Form Druid (complaint-tier)" appears to be a community-coined PVP build label referring to a specific gear/skill combination, not an official skill name. Without knowing which Druid skills constitute this PVP build, ailment identity cannot be resolved. UNVERIFIABLE.

**NOTE for Elrond/gandalf:** Druid does apply stun (Werebear roar, Summon Grizzly), immobilize (Summon Oak Sage), slow (Stag Charge), bleed (Summon Wolves + Werewolf Swipe), burn (Fire Tornado). If the "Spirit-Form Druid PVP" is a Druid build centered on Werebear or transformation + particular skills, the ailment would likely be stun. But without build-specific documentation, this is speculative. UNVERIFIABLE stands; recommend a targeted community-source crawl (reddit r/DiabloImmortal, DiabloFans build listings for DI Druid PVP) to resolve.

---

## Row count audit

Total rows: 20
Rows marked `**classify**`: 17 (rows 1–3, 5–13, 15–19)
Rows marked `**unverifiable**`: 3 (rows 4, 14, 20)
Sum: 20. Reconciles with index summary block (17 classified + 3 unverifiable = 20). Iron law satisfied.

## Notable spec tension — LOUD FLAG

**Wave-B AM `accumulator_fill_trigger` enum is incomplete for D4/PoE2 corpus shapes.** Two kits in this batch (d4-dread-claws-warlock, poe2-walking-calamity) classified as AM accumulator use fill triggers not present in the Wave-B spec §4.4 enum:
- `d4-dread-claws-warlock`: fill via time-based passive demon (4 stacks/s) → no `on-passive-tick` or `on-time-tick` in enum
- `poe2-walking-calamity`: fill via Rage-overflow event → no `on-resource-overflow` in enum

The Wave-B spec bin definition (AM = fills from external events, discharges on activation) CORRECTLY covers both. The gap is in the sub-field `accumulator_fill_trigger` enum, not the bin definition itself. This does not invalidate the classifications; it flags a necessary spec extension before rocket implements the field. Recommend gandalf note in Wave-B spec §4.4 errata: add `on-passive-tick` (timed passive generator) and `on-resource-overflow` (resource-at-cap overflow conversion) to `accumulator_fill_trigger` enum.

**PoE2 `reservation_resource` enum gap.** `poe2-archmage-totems` uses Spirit (PoE2's summon/reservation pool) as the reserved resource. Wave-B spec §3.4 `reservation_resource` enum `{"mana", "focus", "stamina-as-resource", "rage"}` omits `spirit`. Recommend adding `spirit` as a valid enum value.
