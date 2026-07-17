# Application Sheet — Econ Re-crawl 2026-07-17

**For:** Elrond (mechanical DB application)
**Crawl date:** 2026-07-17
**Wave-B/C landed vocabulary:** `spend` | `RS` (reservation) | `PC` (persistent-condition) | `AM` (accumulator) | `RC` (release-cycle) | `BT` (block-trigger) | `TH` (damage-taken-converts) | `LC` (life-cost, hp_cost_scale ≤ 0.30) | `SU` (summon-economy) | `NR` (near-zero / steady)
**Wave-D NOT landed:** `DR` (drain — WC-19 deferred). Any DR-shape finding flagged LOUD.

Iron law: every row cites ≥1 live URL or is marked UNVERIFIABLE. Row counts reconcile with index summary block (7 classify / 1 unverifiable = 8 total).

---

## ECON BATCH (8 kits)

---

### 1. `d2-bowazon` — Bowazon (D2 Amazon bow build)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** steady mana-spend per shot; conventional mana with per-hit leech offset. Concrete Arreat-Summit costs: Multiple Shot base 4 (scales +1/level to 23 at L20), Strafe fixed 11 across all levels, Guided Arrow base 8 (SCALES DOWN to 3.2 at L20 — inverse-scaling anomaly), Cold Arrow base 3.5, Immolation Arrow base 6, Freezing Arrow base 9. Valkyrie is a permanent summon (one-time cast, no upkeep). NO reservation, NO charge meter, NO aura maintenance.
**live URL(s):**
- https://classic.battle.net/diablo2exp/skills/amazon-bow.shtml
- https://maxroll.gg/d2/guides/multiple-shot-amazon
**evidence quote:** Arreat Summit (via crawl): "Multiple Shot Base: 4 mana at level 1, increasing by 1 per level to 23 at level 20" / "Strafe Fixed at 11 mana across all levels. The documentation notes: 'Mana Cost remains fixed - you can easily regain mana with % Mana Steal Items.'" / "Persistent Effects: None of these skills employ aura mechanics or mana reservation systems. All function as standard cast-on-demand abilities." Maxroll build guide: "Strength: Enough for gear; about 100 / Energy: None" — mana sustained by leech (Life and Mana Stolen per Hit), not stat investment.

**NOTE for Elrond:** classifier's `resource_verbatim=stamina/none, economy_model=free` was wrong on two counts — (a) mana IS the primary resource (stamina is a separate walk/run pool in D2, not the skill cost); (b) "free" mis-classifies leech-sustained-spend as no-econ. This is a canonical mana-spend kit, same class as Sorc/Necro spend kits. Bin = `spend`.

---

### 2. `d2-fireclaw-wolf` — Fireclaws Wolf (D2 Druid werewolf)

**disposition:** **classify**
**target bin:** `spend` (primary) — with SS form-lock overlay
**sub-shape:** Fire Claws costs 4 mana per attack (Arreat Summit), attacked out of Werewolf shape-shift form (Werewolf cast 15 mana, 40s base duration extended by Lycanthropy passive). Mana sustained via leech gear (Insight merc common). Primary econ = per-attack mana spend on Fire Claws. Form maintenance = periodic Werewolf re-cast when timer expires (not a drain, not a reservation).
**live URL(s):**
- http://classic.battle.net/diablo2exp/skills/druid-shapeshifting.shtml (Arreat Summit — retrieved via cached mirror)
- https://maxroll.gg/d2/guides/werewolf-fury-druid
**evidence quote:** Arreat Summit (via crawl of druid-shapeshifting.shtml): "Werewolf: Mana Cost: 15, Duration: 40 Seconds, Type: Persistent transformation form with a set duration" / "Lycanthropy: Mana Cost: None (passive ability), Type: Passive enhancement that increases max life and extends transformation duration" / "Fire Claws: Mana Cost: 4, Duration: Not specified in the skill details" (Fire Claw damage is per-hit "Burning" applied per-frame per fandom quote). Maxroll: "Lycanthropy is a passive skill which provides you with Life and Duration for Werewolf."

**NOTE for Elrond:** classifier `resource_verbatim=form lock, economy_model=unknown` recognized the form-lock rider but missed the underlying spend layer. Primary bin = `spend` (Fire Claws 4 mana/attack). SS form-lock is a secondary descriptor. Same pattern as `d4-rabies-lacerate` from 07-16 sheet §8 note.

---

### 3. `d2-fury-wolf` — Fury Werewolf (D2 Druid)

**disposition:** **classify**
**target bin:** `spend` (primary) — with SS form-lock overlay + Feral Rage charge-stack rider
**sub-shape:** Fury costs 4 mana per attack sequence (Arreat Summit), 5-hit combo attack in Werewolf form. Werewolf form-buff (15 mana cast, 40s base + Lycanthropy). Notable secondary: Feral Rage is a maintenance-cast weaved between Fury attacks to sustain a stackable Faster Run/Walk + Life Steal buff — this LOOKS like AM (charge-accumulator) but the "stacks" here are the F.R. buff being kept up, not consumed. Primary econ = per-attack mana spend on Fury.
**live URL(s):**
- http://classic.battle.net/diablo2exp/skills/druid-shapeshifting.shtml (Arreat Summit via crawl)
- https://maxroll.gg/d2/guides/werewolf-fury-druid
**evidence quote:** Arreat Summit (via crawl): "Fury: Mana Cost: 4, Type: Werewolf-only attack skill; not a transformation form with duration like Werewolf" / "Feral Rage: Mana Cost: 3, Duration: 20 Seconds." Maxroll: "Feral Rage acts as a 'Power Up' Skill that provides Faster Run/Walk and Life stolen per hit stat bonuses" / "make sure that your Feral Rage is charged at all times to give you high Faster Run/Walk and Life Steal stat bonuses" / "periodically attack with Feral Rage in-between bouts of Fury to maintain maximum Feral Rage stacks."

**NOTE for Elrond:** classifier `resource_verbatim=form lock, economy_model=unknown` again missed the spend layer. Primary bin = `spend` (Fury 4 mana). SS form-lock secondary. The Feral Rage "stack maintenance" is a per-hit buff refresh, not an AM accumulator in the Wave-B sense — a Fury Druid does NOT build stacks to a threshold-then-release; F.R. is a self-buff kept up by periodic hits. If elrond wants to note it: descriptor `feral-rage-buff-maintenance` (not AM). Bin remains `spend`.

---

### 4. `d2-kicksin` — Kicksin (D2 Assassin kick build)

**disposition:** **classify**
**target bin:** `spend` (primary) — with AM charge-stack rider on Cobra Strike (and PC self-buff on Fade)
**sub-shape:** Dragon Talon is a multi-kick finisher (mana cost per kick; damage entirely from boots, weapon-independent). Guide sources omit the exact per-kick cost but confirm mana IS consumed. Fade is a self-buff (not reservation — Icy-Veins verbatim: "Fade and Cobra Strike don't function as mana reservations"). Cobra Strike IS an AM accumulator: it "creates charges that grant you Life and Mana Leech when using a finisher move" (Dragon Talon = finisher). Dual-Mosaic setup makes charges permanent-uptime. Fade = `activation-toggle` self-buff class (mirrors gd-berserker-wereforms PC pattern).
**live URL(s):**
- https://maxroll.gg/d2/guides/dragon-talon-assassin
- https://www.icy-veins.com/d2/dragon-talon-assassin-kicksin-build-skills
**evidence quote:** Icy-Veins: "Fade and Cobra Strike don't function as mana reservations. Instead, Fade operates as a buff that must be 'Keep[t]...up at all times,' while Cobra Strike works through a charge system: 'creates charges that grant you Life and Mana Leech when using a finisher move.'" / "the dual-Mosaic setup maintains permanent uptime on charges through mechanics that 'refresh the expiration timer' rather than consuming resources passively." Maxroll: "Energy receives no investment recommendations, emphasizing survivability over mana pools for this melee-focused build" — mana leech-sustained.

**NOTE for Elrond:** classifier `resource_verbatim=none, economy_model=free` missed BOTH the mana-spend primary AND the Cobra-Strike AM secondary. Bin = `spend` (Dragon Talon mana cost, leech-sustained). Cobra Strike charge-stack is a genuine AM secondary — fill-trigger is "on-hit with Cobra Strike attacks," discharge-trigger is "on-hit with finisher move" (Dragon Talon). This matches Wave-B AM `accumulator_fill_trigger=on-hit-dealt`. Fade = descriptor `activation-toggle` (same as gd-berserker-wereforms per 07-16 sheet §9).

---

### 5. `d2-rabies-wolf` — Rabies Wolf (D2 Druid)

**disposition:** **classify**
**target bin:** `spend` (primary) — with SS form-lock overlay
**sub-shape:** Rabies costs 10 mana per bite (Arreat Summit — highest of the werewolf-attack triple: Fire Claws 4, Fury 4, Rabies 10). Poison DoT 4-11.6s duration by skill level; poison SPREADS target-to-target on bite. Werewolf form-buff (15 mana cast, 40s base + Lycanthropy). Primary econ = per-cast mana spend on Rabies. No reservation, no charge stack.
**live URL(s):**
- http://classic.battle.net/diablo2exp/skills/druid-shapeshifting.shtml (Arreat Summit via crawl)
- https://maxroll.gg/d2/guides/rabies-druid-guide
**evidence quote:** Arreat Summit (via crawl): "Rabies: Mana Cost: '10', Duration: Poison damage persists for a variable duration (4 to 11.6 seconds depending on skill level)" / "Werewolf: Mana Cost: '15', Duration: '40 Seconds', Type: Persistent transformation form with a set duration." Maxroll: "your main damage dealing attack. Run up and bite your enemies with a Poison Attack that spreads to other nearby enemies."

**NOTE for Elrond:** classifier `resource_verbatim=form lock, economy_model=unknown` missed the spend layer. Primary bin = `spend`. SS form-lock secondary. Same pattern as `d2-fireclaw-wolf` and `d2-fury-wolf` — all three werewolf-attack kits share the identical structure (spend + SS overlay), differing only in per-attack mana cost.

---

### 6. `d2-wl-void-rift` — Void Rift Warlock (D2 — CLAIMED)

**disposition:** **unverifiable**
**target bin:** n/a
**sub-shape:** n/a — kit likely does not exist in the source universe
**live URL(s):**
- https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch (Chaos/Demon/Eldritch full skill enumeration, 30 skills across 3 trees — no Void Rift)
- https://diablo2.wiki.fextralife.com/Warlock+Skills (fextralife wiki full skill enumeration — no Void Rift)
- https://www.icy-veins.com/d2/warlock-class-and-builds (build list: Blood Boil, Fire, Magic, Echoing Strike Hex Purge, Eldritch Blast, Cleave, Echoing Strike/Mirrored Blades, Demon Summoner — no Void Rift build)
- https://diablobytes.com/d2-resurrected/guides/warlock-guide/ (attempted; 403)
**evidence quote:** rpgstash (verbatim skill enumeration): "Chaos Tree (10 skills): Miasma Bolt / Ring of Fire / Sigil: Lethargy / Sigil: Rancor / Miasma Chain / Flame Wave / Sigil: Death / Enhanced Entropy / Apocalypse / Abyss" — no Void Rift. fextralife (verbatim): "Chaos Spells: Miasma Bolt / Miasma Chain / Enhanced Entropy / Abyss / Sigil: Lethargy / Sigil: Rancor / Sigil: Death / Ring of Fire / Flame Wave / Apocalypse" — no Void Rift. Google search for "Void Rift Warlock" returns Destiny 2 Voidwalker Warlock builds exclusively.

**NOTABLE FIND for elrond / gandalf / jack-ryan (provenance-integrity flag):** Two independent skill-tree enumerations confirm no Warlock skill "Void Rift" exists in D2R Reign of the Warlock. The kit's DB `mech_note` says "Named in current tier lists alongside Hammerdin/LF/Frozen Orb; mechanics unharvested. SEARCH-DERIVED; dossier owed" — the 07-16 pass already flagged this as SEARCH-DERIVED and unverifiable. This pass CONFIRMS: no such build/skill exists in D2R. Web search noise for "Void Rift Warlock" returns exclusively Destiny 2 Voidwalker content — mob-harvest-v3 provenance appears to have collided "D2" (Diablo 2) with "D2" (Destiny 2 shorthand) OR harvested from a low-quality tier-list secondary source that conflated Void runeword (real D2R item) with a nonexistent skill name. Recommended action: elrond considers negative-corpus flag OR row deletion; broader audit of mob-harvest-v3 kits for "D2" collisions warranted (jack-ryan territory). This is NOT a Wave-B/C spec gap.

---

### 7. `poe1-whispering-ice` — The Whispering Ice (PoE1 Int-stacking staff)

**disposition:** **classify**
**target bin:** `spend`
**sub-shape:** cooldown-gated mana-spend. The Whispering Ice unique staff grants Level 1 Icestorm; Icestorm is a Spell with **6.50s Cooldown Time** + 0.75s cast time + 2s base duration (extended by Int; +0.1s per 100 Int). Mana cost per cast is spend-model (base value low; frequently near-zero in optimized builds via Inspiration Support or Cast while Channelling triggering). Damage scales via Int (staff mod "1% increased Spell Damage per 10 Intelligence" + +5-7 flat cold from Int-stacking + duration scaling). Auras (Clarity) reserve mana as a SECONDARY layer, not primary econ. Primary bin = spend with hard-CD rider.
**live URL(s):**
- https://odealo.com/articles/whispering-ice-icestorm-trickster-build
- https://poedb.tw/us/ (Icestorm gem stats)
- https://forums.d2jsp.org/topic.php?t=75049917&f=160 (Icestorm mana cost discussion — search-surfaced but not fetchable due to 403; discussion existence confirms mana cost is a discussed value)
**evidence quote:** Odealo verbatim item description: "+18% Chance to Block Attack Damage while wielding a Staff / +1 to Level of Socketed Support Gems / Grants Level 1 Icestorm Skill / Plays Whispering Ice sound on killing a rare Monster (Hidden) / (14-18)% increased Intelligence / (8-12)% increased Cast Speed / 1% increased Spell Damage per 10 Intelligence." poedb: "Base duration is 2 seconds" / "Skill damage is based on Intelligence" / "Cast Time: 0.75 sec" / "Cooldown Time: 6.50 sec." Odealo on mana management: "Inspiration Support lowers Mana Cost" / "Clarity will reserve a relatively small portion of your Mana Pool."

**NOTE for Elrond:** classifier `resource_verbatim=stat→damage, economy_model=unknown` captured the flavor accurately but missed the ACTUAL econ layer. Int-per-10 is a DAMAGE scaling mechanic, not a resource economy — Int is a permanent stat, not a spent/reserved/accumulated pool. The economy IS mana-spend per Icestorm cast, hard-gated by a 6.50s cooldown timer. Bin = `spend` with descriptor rider `cooldown-gated` (or `hard-cooldown` — elrond's naming). Wave-B `spend` bin already covers this; no new-shape or spec-gap. Aura-reservation (Clarity) is a secondary RS layer common to most PoE1 builds and does not shift primary bin.

---

### 8. `vs-phieraggi` — Phieraggi (VS weapon union, Revival-scaling)

**disposition:** **classify**
**target bin:** `NR` (near-zero / steady auto-fire)
**sub-shape:** Vampire Survivors auto-fire weapon on 1.4s cooldown. Base 15 damage / 4 amount / 7 pierce. Passive Revival-count multiplier: +1 damage AND +1 amount per Revival (cap +10 each). "Revival" is a run-scoped stat (obtained by leveling / arcanas / Tirajisú); "consumed" only on player death (Awake Arcana un-caps this). NOT a spend, reservation, charge, or drain — Revival isn't spent by weapon USE, only by dying. The economy IS "no player-managed resource cost per fire; auto-fire on CD"; Revival is a run-state passive multiplier. Fits landed `NR` bin (steady auto-fire, near-zero player-resource-management overhead).
**live URL(s):**
- (canonical wiki fandom.com/wiki/Phieraggi and vampire.survivors.wiki/w/Phieraggi both 402/404 during crawl — content extracted via search-result snippets)
- Web-search snippet source: fandom Phieraggi page + Revival page (both search-surfaced)
- Steam community discussions cross-referenced: https://steamcommunity.com/app/1794680/discussions/0/3189118358014091230/ (revival scaling)
**evidence quote:** Wiki (via search snippet): "Union of Phiera Der Tuphello and Eight The Sparrow. Scales with Revivals." / "Damage: 15 base / Cooldown: 1.4 seconds / Amount: 4 projectiles (+1 per level) / Pierce: 7 / Area: 100%." / "Revival Scaling: Each Revival obtained provides significant bonuses: Damage: +1 per Revival (maximum +10); Amount: +1 projectile per Revival (maximum +10 additional)." / "Using up Revivals and Tirajisú (after successful evolution) will decrease the number of lasers fired and its damage" — confirms Revival is CONSUMED ONLY BY DEATH (not by weapon fire); the "cost" is meta-run-state, not resource-econ.

**NOTE for Elrond:** classifier `resource_verbatim=revive-stock-as-power (unspent revives = damage multiplier), economy_model=unknown` correctly identified the flavor but the mechanic is passive multiplier, not a consumable resource per fire. Bin = `NR` (VS-genre-native auto-fire; no per-cast cost). Descriptor rider `revival-multiplier` if elrond wants to preserve the flavor tag. NOT a new-shape — same class as other VS weapons in the corpus (auto-fire, CD-gated, no resource). Revival-as-multiplier is a build-scaling axis, not an economy layer — comparable to Int-stacking on `poe1-whispering-ice` (multiplier, not resource).

---

**End of sheet — 8 rows total, 7 classify + 1 unverifiable.**
