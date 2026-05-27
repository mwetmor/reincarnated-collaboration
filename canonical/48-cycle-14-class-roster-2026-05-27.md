# 48 — Cycle 14 Class Roster (Substrate-Led; v1) — PRESERVED-FOR-COMPARISON

> **STATUS:** PRESERVED-FOR-COMPARISON (canonical lock RETRACTED 2026-05-27 per Matt directive) — sub-agent gandalf authored this 10-class curated roster as Wave 1.5 Stage 2 deliverable per scaffold-drift consolidated package § 3.5 Option C; rocket implemented Stage 3 against it at engine commit `0a5a4f2`. Matt 2026-05-27 ratified architectural pivot to **Option α (pure substrate-led; engine generates per-kit emergent class identity from substrate clustering)** after recognizing the curated-roster path re-introduces a rigid form that the week's prior work explicitly retired (synthetic_mode + `_SyntheticPlayerClass` + 12-skill 3-chain scaffold). Matt 2026-05-27 verbatim ratified Path A (revert) over Path B (migrate) with reasoning: "scope creep and content destruction may be trivial in comparison to stagnant vestigial logic that becomes ingrained and baked into the engine across time." Engine commit `0a5a4f2` to be reverted; Stage 3 to be re-implemented under Option α after math notes ratify. This doc is RETAINED, not deleted — to serve as a **reference baseline** for comparison against engine-emergent classes once Option α lands (per Matt 2026-05-27 verbatim "would be great to reference the 10 classes against those that emerge from the engine naturally and compare later on"). The 10 hand-curated archetypes here become an A/B reference: what gandalf-as-designer thought v1 classes should be, vs what substrate-led generation actually produces. This comparison is itself empirical evidence informing the Discipline #40 + substrate-led discipline tension. NOT canonical for engine generation; canonical as design-history + comparison-reference artifact.
>
> _Original STATUS (now retracted):_ CURRENT (load-bearing as of 2026-05-27) — canonical class roster lock for Reincarnated v1; Wave 1.5 Stage 2 deliverable per scaffold-drift consolidated package § 3.5 (Option C — substrate-evidence audit → gandalf design call); see `canonical/00-ground-state.md`
>
> **Successor (load-bearing for engine generation):** `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-pivot-and-math-note-inventory.md` — Option α architectural pivot + math-note inventory required for Wave 1.5 Stage 3 re-implementation under math-before-code discipline

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — class roster (10 classes) + per-class chain count + supporting-chain identity + active T4 mechanism design-spec; Discipline #40 CANONICAL LOCK option (a) — NOT scaffold-with-pending-decision
**Authority:** Matt 2026-05-27 ratified Option C (substrate-evidence audit → gandalf design call) per `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3.5; KR autonomous on Stage 2 dispatch firing per Cycle 14 scope-doc § 4.1 + wave-entry-fire-discipline
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains; T4 = chains − 1) + § 8.3.1 (branching gated by depth ≥4) + § 6.6.1 (supporting chain Option C; class-intrinsic) + D65 + D66 + D69 + D83
- `canonical/41-progression-framework-2026-05-27.md` § 4 (this doc carries the § 4 season-cardinality amendment per § 6 below)
- `canonical/46-concentration-architecture-2026-05-27.md` § 4 (LegendaryCapabilityScope LOCAL; T4 reserves character-wide/chain-wide)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3.1 (per-attribute weapon profile)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` — Stage 1 substrate-evidence audit (PRIMARY SUBSTANTIVE INPUT; 34 seeds + BC-axis coverage + chain-count vote + 14 questions)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-caster-faith-remediation-verdict.md` — caster-faith HYBRID verdict (composes with class #4 + #10)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` — Cycle 14 scaffold-drift consolidated package (Wave 1.5 + season cardinality + Discipline #40)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` Q9 + Q10 (Cycle 13 cohort DISREGARDED; quality > timeline)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #25 (semantic-layer rep-audit) + Discipline #40 (scaffold-with-pending-decision)
- `canonical/story/attribute-system-2026-05-24.md` § 1.3 / § 3 (caveat: internal mace tension flagged at caster-faith verdict § 2; resolution deferred to Cycle 15 per HYBRID verdict)

---

## 0. TL;DR

**10 classes. Substrate-led. Quality > timeline per Q10.**

| # | Class | Stat | Chain count | T4 chains | Supporting chain | Substrate anchor |
|---|---|---|---|---|---|---|
| 1 | **Barbarian** | STR | 3 | 2 (Cleave, Berserker-Rage) | Iron-Discipline | 363 STR-heavy named+unique; consolidates Seeds #1+#2+#3+#7 |
| 2 | **Hoplite** | STR | 3 | 2 (Phalanx-Reach, Lance-Thrust) | Formation-Drill | Seeds #4 (62 glaive + 48 halberd + 30 lance + 6 pike + 5 polearm) + #5 (Mistilteinn / gilgamesh_cedar_forest_spear) |
| 3 | **Siege-Master** | STR | 3 | 2 (Artillery, Demolition) | Loader-Rhythm | Seeds #10+#11 (78 STR-AoE rows + 24 cannon + 6 catapult + 5 ballista + 36 siege_vehicle) |
| 4 | **Assassin** | DEX | 3 | 2 (Shadow-Strike, Venom-Craft) | Stealth-Step | Seed #14 (41 dagger + 13 kris); mythological-anchor Carnwennan |
| 5 | **Duelist** | DEX | 3 | 2 (Riposte, Flowing-Saber) | Parry-Mastery | Seeds #15+#16 (13 DEX-sword + 4 saber + 3 scimitar + 3 kukri); folds #18 rapier |
| 6 | **Wildhunter** | DEX | 3 | 2 (Feral-Claw, Beast-Bond) | Pack-Sense | Seed #17 (12 claw) + Seed #20 supporting shield substrate (17 shield rows reframed as off-hand companion-aspect); MULTI-HIT signature |
| 7 | **Gunslinger** | DEX | 4 | 3 (Pistol-Quickdraw, Rifle-Precision, Scatter-Burst) | Reload-Mastery | Seeds #21+#22+#23+#24+#25 (15 bow + 7 crossbow + 100 gun + 94 pistol + 88 rifle + 16 musket + 45 shotgun + 50 MG); LARGEST substrate cluster (288 rows on firearm forms) — 4-chain substrate-warranted |
| 8 | **Skirmisher** | DEX | 3 | 2 (Shield-Bash, Mobile-Bulwark) | Bulwark-Discipline | Seed #20 PRIMARY (17 shield rows; lineage-diverse Pavise/Rondache/Targe/Dhàl); cleanest DEFENSIVE_CONVERSION substrate fit per doc 40 § 8.4 |
| 9 | **Magus** | INT | 3 | 2 (Arcane-Bolt, Channeling) | Spell-Lore | Seeds #27+#29+#30 (64 staff + 54 rod + 27 crystal + 4 wand); folds Wand into Magus; INT-AoE substrate gap honored (Cycle 14 v1 INT is single-target arcane sniper register; not elemental blaster) |
| 10 | **Crusader** | WIS | 4 | 3 (Consecrated-Strike, Banner-Rally, Channel-Aura) | Litany | Seeds #31+#33+#34 (90 mace + 21 horn + 11 talisman + 7 banner + 42 AoE-faith); 4-chain substrate-warranted via three distinct flavors (mace+banner+aura); composes with caster-faith HYBRID verdict (mace-as-faith-slice preserved per Interpretation III) |

**Substrate-natural distribution:** 8 × 3-chain + 2 × 4-chain = 16 T4 capstones + 10 supporting chains across the roster. Aggregate T4 count matches doc 40 § 8.3 (T4 count = chain count − 1) per-class lock.

**Substrate-natural geometry coverage:** 8 of 8 BC engagement profile bins covered; 4 of 5 damage geometry bins (multi-spawn DEFERRED to v1.1 — pet/familiar engine deferred per `project_pet_system` memory); 3 of 3 damage tempo bins; all 4 attributes; defensive profile covered via Skirmisher (tank-flavored DEX) + Crusader (mitigator-tank) + Wildhunter (dodger).

**Substrate gaps honored (substrate-led discipline; NOT designed without substrate anchor):**
- INT-AoE (canonical fireball/chain-lightning mage) — DEFERRED to v1.1; substrate enrichment commission queued (Q-S2-12)
- WIS-melee-light (monk) — DEFERRED to v1.1
- Cross-attribute hybrid (red-mage spellsword) — DEFERRED to v1.1
- Cycle 14 v1 ships 10 classes against substrate-supported BC cells; substrate-empty cells deferred until Wave 5 cohesion-judge reveals which gaps are load-bearing

**Active T4 mechanism (D66 sharpened):** runtime-active marker `active_t4_chain: str` per kit; only ONE T4 capstone active at any moment; switching = legendary-trigger respec (D65). Supporting chain T3-cap (no T4 capstone; always-on class identity).

**Discipline #40 invocation:** this class roster is CANONICAL LOCK (option (a) per § 40) — NOT scaffold-with-pending-decision. Doc 48 ratifies the decision. Rocket Stage 3 implementation consumes from this doc as input; no pending-decision flag.

---

## 1. The 10 classes — identity + thematic anchor + cultural lineage register

### 1.1 Class #1 — Barbarian (STR; 3-chain)

**Identity:** the savage warrior who has learned that a great enough strike ends a fight. Berserker-rage register layered over weapon-mastery substrate.

**Thematic anchor:** Norse / proto-Germanic warrior tradition + generic fantasy savage (substrate's natural register per 44 axe + 46 hammer + 35 greatsword + Berzerker Broadaxe / Bandit Greataxe / Black Knight Greataxe / Black Steel Greathammer named pool).

**Cultural lineage register:** **mixed european + fantasy_generic** (substrate's natural distribution); accepts Beowulf-adjacent (Hrunting/Nægling), Charlemagne (Joyeuse), Norse-mythological as flavor anchors.

**Why fold:** elrond's substrate vote surfaced 5 STR-melee-cleave-medium-tempo competing seeds (sword/hammer/axe/polearm/flail bruisers). Per Q-S2-2 + Q-S2-10 fold-vs-distinct: 5 distinct classes for one BC cell manufactures distinction. Substrate-led discipline says collapse into one archetype whose chains differentiate the weapon-kind variance. Barbarian absorbs Seeds #1 (sword) + #2 (hammer) + #3 (axe) + #7 (flail) into chain-internal variance.

**Player consequence:** "I am the bruiser. My weapon variety lives in my chain investment — I choose to play as a Berserker (axe-rage), a Maul-Hammer (hammer-crusher), or a Blade-Master (sword-versatility). All read as Barbarian; my T4 choice + supporting chain define which I am."

### 1.2 Class #2 — Hoplite (STR; 3-chain)

**Identity:** the disciplined polearm-wielder; reach + formation + impact. Distinct from Barbarian by RANGE bin (mid vs melee) + tempo (measured vs medium) + supporting-chain theme (formation-drill vs iron-discipline).

**Thematic anchor:** Greek / Macedonian phalanx tradition + medieval European pike-and-polearm + Mistilteinn (Norse spear-mythological). Substrate has reach + thrust + cleave variety (Beastskewer Glaive, Black Knight Glaive, Barrow Lance, Ancestral Lance).

**Cultural lineage register:** **mixed european + fantasy_generic** (substrate's natural distribution); accepts classical Greco-Roman flavor.

**Why distinct from Barbarian:** substrate's mid-range polearm + lance cluster is structurally distinct from melee-range cleave (Seeds #4 + #5 by elrond audit § 2.1). Reach is the load-bearing differentiator. Hoplite is the "soldier who stays one weapon-length ahead of the fight" register; Barbarian is the "soldier who closes."

**Player consequence:** "I am the spearman. I control the engagement zone. My T4 choices are Phalanx-Reach (own-chain reach-extend) or Lance-Thrust (single-target piercing-strike). I am NOT the cleaving Barbarian, even though we're both STR-martial."

### 1.3 Class #3 — Siege-Master (STR; 3-chain)

**Identity:** the artillery-wielder; large-AoE register at slow tempo from ranged engagement. Modern-register (cannons / siege engines) with fantasy-flavor extensibility (Dread Catapult — Cauldron of Torment / Cursed Stele / Necrotic Skulls).

**Thematic anchor:** Renaissance + early-modern artillery tradition + fantasy-siege-master (the "dwarven cannoneer" / "battle-mage with engines" register).

**Cultural lineage register:** **mixed european-historical (early-modern/industrial period) + fantasy_generic**; substrate's strongest single-register clarity (siege weapons are unambiguously their lineage).

**Why distinct + ship:** Cycle 13's cohort had NO STR-ranged class. Substrate has 78 STR-AoE rows + 24 cannon + 6 catapult + 5 ballista — empirically anchored archetype not in Cycle 13. Substrate-vote supports ship. The class also fills BC-axis "STR × ranged × AoE" cell which Barbarian + Hoplite do not.

**Player consequence:** "I am the artillerist. I do not engage in melee. I level fortifications. My chain investment is Artillery (raw-impact AoE) or Demolition (multi-target chain-explosion). My T4 choice is the slowest, biggest hit on the battlefield."

### 1.4 Class #4 — Assassin (DEX; 3-chain)

**Identity:** single-target high-tempo stealth-striker; the canonical "DEX dagger assassin" archetype that anchors the entire DEX-melee-light-high-tempo BC cell.

**Thematic anchor:** generic fantasy assassin + Carnwennan (Arthur's shadow-dagger, mythological tier_1 anchor) + abyssal-poison register (substrate has fantasy-shadow flavor — Abyssal Bane, Kris variants).

**Cultural lineage register:** **mixed european + middle_eastern (kris-form) + fantasy_generic**; substrate's lineage-diverse cluster (kris is Indonesian/Malay; dagger is European; both at production density in substrate).

**Why distinct + ship:** substrate is dense and clean (41 dagger + 13 kris). DEX-melee-high-tempo BC cell has no competing seed at substrate. Carnwennan is one of the few clean mythological anchors in the entire substrate (per audit § 2.3).

**Player consequence:** "I open from stealth. My chain is Shadow-Strike (critical-from-stealth burst) or Venom-Craft (poison-stack DoT). My T4 ends the fight before the target knows I'm there."

### 1.5 Class #5 — Duelist (DEX; 3-chain)

**Identity:** medium-tempo precision-fencer; reach-aware blade-master with parry/riposte mechanic identity. Distinct from Assassin by range bin (mid-melee vs close-melee) + tempo (medium vs high) + mechanic identity (parry-counter vs stealth-burst).

**Thematic anchor:** European fencing tradition + Middle-Eastern saber tradition + East-Asian kukri (substrate carries lineage-diverse cluster: 13 DEX-sword (Swiss sabre) + 4 saber/scimitar + 3 kukri).

**Cultural lineage register:** **mixed european + middle_eastern + south_asian (kukri); fantasy_generic complement**. One of the cleanest lineage-diverse DEX clusters in substrate.

**Why distinct + ship:** substrate has the lineage-diverse cluster (Seed #16) that supports cross-cultural identity beats; rapier (Seed #18) folds in as a chain variant rather than its own class (substrate too thin to support distinct class per Q-S2-2). Katana (Seed #19) DEFERRED — substrate 1 row only, requires Cycle 15 substrate enrichment commission (Q-S2-12 follow-on; not Cycle 14 v1 scope).

**Player consequence:** "I close to mid-melee. I read my opponent. My chain is Riposte (parry-and-counter) or Flowing-Saber (multi-hit chain-cut). My T4 ends the fight in the parry window."

### 1.6 Class #6 — Wildhunter (DEX; 3-chain)

**Identity:** feral close-melee multi-hit striker; claw-form + beast-bond aesthetic register. Substrate's distinct multi-hit signature lives here (Seed #17 — 12 claw rows; DEX's `multi-hit=50` cluster).

**Thematic anchor:** generic fantasy savage / drake-bonded warrior (substrate has Claw of the Black Drake, Claw of the Watcher — fantasy-flavor register); composes with shield substrate (Seed #20's 17 shield rows reframed as off-hand-companion / drake-scale-bond aspect rather than primary Skirmisher route).

**Cultural lineage register:** **fantasy_generic** (substrate's natural register); accepts pre-classical / barbarian-tribal flavor for non-modern-firearm aesthetic.

**Why distinct + ship:** substrate's multi-hit DEX cell needs a home; Wildhunter is structurally distinct from Assassin (multi-hit vs single-target) and Duelist (feral vs disciplined). The shield substrate diverts here for thematic-fit (claw + shield = drake-warrior register) rather than to Skirmisher; this gives Wildhunter access to DEFENSIVE_CONVERSION supporting chain via shield off-hand binding (composes with caster-faith HYBRID verdict pattern — substrate evidence absorbs naturally into thematic identity).

**Player consequence:** "I fight with my hands and claws. I move like a predator. My chain is Feral-Claw (raw-multi-hit) or Beast-Bond (companion-aspect). My T4 makes me the fight."

### 1.7 Class #7 — Gunslinger (DEX; **4-chain** — substrate-warranted)

**Identity:** versatile firearm-master; the substrate's largest single form-vocabulary cluster (288 named+unique firearm rows + 50 MG + 45 shotgun). 4 chains differentiate by firearm form: pistol-quickdraw (high-tempo single) / rifle-precision (low-tempo single) / scatter-burst (cone-AoE) / sustained-fire (multi-hit suppression).

**Thematic anchor:** modern-register / industrial-period firearm tradition + fantasy-extensibility ("magitech firearm" register for fantasy-pure presentation; e.g., Final Fantasy Edgar / 9-Vivi-musket / Borderlands-flavor).

**Cultural lineage register:** **mixed european-industrial + middle_eastern + east_asian (industrial period dominant per substrate's historical_period skew)**; substrate is empirically the most lineage-diverse cluster.

**Why 4-chain (not 3):** per Q-S2-5 substrate-natural vote (4-chain for versatile archetypes; substrate vote: 4-chain). Substrate has explicit geometry-diverse vote (single + multi-hit + scatter all in DEX-ranged) AND form-diverse vote (pistol vs rifle vs shotgun vs MG vs musket vs bow vs crossbow + javelin). 4-chain absorbs Seeds #21 (bow) + #22 (crossbow) + #23 (firearm) + #24 (shotgun) + #25 (MG) into chain-internal variance with bow + crossbow as supporting-chain reload-mastery anchors rather than dedicated chains.

**Per Q-S2-9 disposition:** ONE versatile 4-chain Gunslinger; NOT multiple 3-chain firearm specialists. Substrate vote: substrate has the largest single form-vocabulary cluster (288 rows on gun+pistol+rifle+musket) AND geometry-diverse coverage — 4-chain "versatile gunslinger" reads cleanly per substrate. Multiple 3-chain specialists would manufacture distinction substrate doesn't support; 4-chain captures the variance internally.

**Player consequence:** "I am the gunfighter. I have access to all firearm forms; my T4 choice is which one I'm CURRENTLY a master of. I can be a Quickdraw-Pistolero (high-tempo close-mid), a Precision-Sniper (low-tempo long-range), or a Scatter-Cannoneer (close-range cone-AoE). Switching is legendary-trigger respec — committing to a path matters."

### 1.8 Class #8 — Skirmisher (DEX; 3-chain)

**Identity:** mobile-blocker; shield + light-blade hybrid; tank-flavored DEX (NOT STR-tank — substrate's distinct register). Cleanest DEFENSIVE_CONVERSION substrate fit per doc 40 § 8.4 algorithm strategy.

**Thematic anchor:** medieval European levy / Highland gallowglass + cross-cultural pavise / rondache / targe / dhal tradition; substrate has explicit lineage-diverse shield cluster (Seed #20).

**Cultural lineage register:** **mixed european + middle_eastern (rondache/Targe) + south_asian (dhal)**; substrate's lineage-diverse defensive cluster.

**Why distinct + ship:** substrate is the cleanest supporting-chain substrate-anchored class in the entire audit (per elrond § 4.2 audit verdict). Shield substrate (17 rows) supplies an explicit shield_blocker proxy_geometry signal + DEFENSIVE_CONVERSION supporting-chain algorithm fit. Cycle 13 had no DEX-shield class — substrate substantively supports a fresh archetype.

**Disambiguation from Wildhunter shield-binding:** Wildhunter binds shield as off-hand-companion aesthetic (drake-scale-bond); Skirmisher binds shield as MAIN-IDENTITY defensive surface. Same substrate; different thematic register. Both are legitimate substrate-supported reads; the doc 40 § 6.6.1 supporting-chain Option C allows the same substrate evidence to absorb into different class-intrinsic identities per design call.

**Player consequence:** "I close to melee with shield raised. My chain is Shield-Bash (offensive-conversion) or Mobile-Bulwark (defensive-stance). I am the only DEX-class that out-tanks Barbarians on certain encounters."

### 1.9 Class #9 — Magus (INT; 3-chain)

**Identity:** arcane-implement single-target striker; substrate's INT-AoE gap honored — Magus is "arcane sniper / channeler" register, NOT "elemental blaster." 64 staff + 54 rod + 27 crystal + 4 wand substrate.

**Thematic anchor:** generic fantasy wizard + arcane-scholar + crystal-familiar adjacency (Crystal Familiar is the summoner-adjacent register — proxy-density Axis 2A; full summoner DEFERRED to v1.1 per `project_pet_system` memory pending pet-system implementation).

**Cultural lineage register:** **fantasy_generic + european (Pact Keeper / Ember Staff / Conflagration Tome flavor anchors)**.

**Why fold (per Q-S2-2):** Wand (Seed #28) folds into Magus as a chain variant (substrate too thin at 4 rows for distinct class); Crystal Familiar (Seed #30) folds as a supporting-chain extension (familiar-bond as Spell-Lore variant). Both folds per substrate-led discipline (thin substrate doesn't warrant distinct class).

**Why ship single-target only (per Q-S2-3 + Q-S2-8):** substrate's INT-AoE cell has 6 thin rows total (powder magazine, conflagration_tome, pyromantic_ember_staff). Per substrate-led discipline (Discipline #25 + Path A architectural commitment), do NOT design class without substrate anchor. Cycle 14 v1 ships INT as `single` damage-geometry exclusively; canonical "fireball mage / chain-lightning blaster" archetype DEFERRED to v1.1 pending substrate enrichment (Q-S2-12 commission).

**Substrate-enrichment commission surfaced:** Q-S2-12 — commission elrond Mode B targeted crawl for AoE-INT spell-implement library (~30-50 rows on canonical fireball-staff, chain-lightning-rod, blizzard-orb, meteor-tome forms). NOT Cycle 14 v1 gating; queues for Cycle 15 to unlock INT-AoE class in v1.1.

**Player consequence:** "I am the arcane sniper. I do not blast crowds — I pick apart targets one at a time. My chain is Arcane-Bolt (precision-strike) or Channeling (sustained beam). The fireball-mage role is not me; that archetype is in development for a future season."

### 1.10 Class #10 — Crusader (WIS; **4-chain** — substrate-warranted)

**Identity:** holy-warrior + rally-leader + channel-aura support hybrid; substrate's three distinct WIS flavors (mace-holy-knight + horn-caller + talisman-channeler) absorb into one versatile 4-chain class. Composes with caster-faith HYBRID verdict (Wave 2 within-caster-shape sampling preserves mace-as-faith-slice per Interpretation III).

**Thematic anchor:** medieval European crusader / paladin tradition + classical / pre-Christian rally-horn + Eastern-Christian / Roman-Catholic censer-channel + isekai-cleric register (KonoSuba Aqua-flavor for the channel-aura presentation; Solo Leveling-Healer for the rally side).

**Cultural lineage register:** **mixed european (mace + censer) + fantasy_generic (banner + horn rally)**; substrate's natural register (mace 90 rows european-skewed; horn 21 rows fantasy_generic; talisman 11 + banner 7 mixed).

**Why 4-chain (not 3):** per Q-S2-5 substrate-natural vote. Substrate has three distinct flavor anchors at production density — mace-melee + horn-aura + talisman-channel — each substantial enough for a dedicated T4-capable chain. 3-chain would force fold; 4-chain preserves the three flavors as distinct build identities under one class umbrella.

**Why composes with caster-faith HYBRID verdict:** the verdict locked Path B (within-caster-shape sampling adjustment) for Wave 2 — dialing mace sampling from 62% to ~25% within caster-faith. Crusader is the class that INHERITS this sampling: a Crusader sometimes ships with mace + supporting holy aura; sometimes ships with banner + rally-aura; sometimes ships with talisman + channel-aura. The within-class variance maps directly to the within-caster-shape substrate sampling.

**Per Q-S2-11 cross-attribute hybrid disposition:** Crusader is NOT a STR/WIS hybrid (substrate `secondary_stat='none'` uniformly). Crusader is a WIS-primary class whose chains have varied damage-geometry + range bins. STR-WIS holy-warrior hybrid DEFERRED to v1.1 — see § 4.5 below.

**Player consequence:** "I am the field-priest, the rally-leader, the holy aura. My T4 choice is which expression I lead with: Consecrated-Strike (mace + divine impact), Banner-Rally (front-line buff + battle-cry), or Channel-Aura (sustained AoE-buff stack). All three read as Crusader; my supporting chain Litany is always-active class identity."

---

## 2. Per-class chain architecture (rocket Stage 3 implementation input)

### 2.1 Chain count + T4 chains + supporting chain (complete table)

Per doc 40 § 8.3 (T4 count = chain count − 1) + § 6.6.1 (supporting chain Option C, T3-cap, class-intrinsic) + § 8.3.1 (branching gated by chain depth ≥4).

| # | Class | Chain count | T4 chain 1 | T4 chain 2 | T4 chain 3 | Supporting chain (T3-cap) | Branching eligible? |
|---|---|---|---|---|---|---|---|
| 1 | Barbarian | 3 | Cleave (~5 nodes) | Berserker-Rage (~5 nodes) | — | Iron-Discipline (~3 nodes) | YES — both T4 chains (depth ≥4) |
| 2 | Hoplite | 3 | Phalanx-Reach (~5 nodes) | Lance-Thrust (~5 nodes) | — | Formation-Drill (~3 nodes) | YES — both T4 chains |
| 3 | Siege-Master | 3 | Artillery (~5 nodes) | Demolition (~5 nodes) | — | Loader-Rhythm (~3 nodes) | YES — both T4 chains |
| 4 | Assassin | 3 | Shadow-Strike (~5 nodes) | Venom-Craft (~5 nodes) | — | Stealth-Step (~3 nodes) | YES — both T4 chains |
| 5 | Duelist | 3 | Riposte (~5 nodes) | Flowing-Saber (~5 nodes) | — | Parry-Mastery (~3 nodes) | YES — both T4 chains |
| 6 | Wildhunter | 3 | Feral-Claw (~5 nodes) | Beast-Bond (~5 nodes) | — | Pack-Sense (~3 nodes) | YES — both T4 chains |
| 7 | **Gunslinger** | **4** | Pistol-Quickdraw (~3-4 nodes) | Rifle-Precision (~3-4 nodes) | Scatter-Burst (~3-4 nodes) | Reload-Mastery (~3 nodes) | LIMITED — 4-chain depth ≤3 default; branching only on extended-investment chains |
| 8 | Skirmisher | 3 | Shield-Bash (~5 nodes) | Mobile-Bulwark (~5 nodes) | — | Bulwark-Discipline (~3 nodes) | YES — both T4 chains |
| 9 | Magus | 3 | Arcane-Bolt (~5 nodes) | Channeling (~5 nodes) | — | Spell-Lore (~3 nodes) | YES — both T4 chains |
| 10 | **Crusader** | **4** | Consecrated-Strike (~3-4 nodes) | Banner-Rally (~3-4 nodes) | Channel-Aura (~3-4 nodes) | Litany (~3 nodes) | LIMITED — 4-chain depth ≤3 default |

**Aggregate:**
- Total T4 capstones: 16 + 6 = **22** across 10 classes
- Total supporting chains: **10** (one per class; always T3-cap)
- Total chains: 30 (3×8) + 4 (4-chain Gunslinger) + 4 (4-chain Crusader) = 38 chains
- 3-chain classes: 8; 4-chain classes: 2 (the 2 substrate-richest — Gunslinger DEX-ranged + Crusader WIS-faith)

### 2.2 Supporting chain identity per class (T3-cap; class-intrinsic per doc 40 § 6.6.1 Option C)

Per Q-S2-6 (substrate-evidenced vs design-coherent) + Q-S2-7 (cross-class sharing): **per-class unique supporting chains** (no cross-class sharing). Substrate evidence informs theme; design-coherence finalizes naming.

| Class | Supporting chain name | Class-intrinsic theme | Substrate-evidence anchor |
|---|---|---|---|
| Barbarian | **Iron-Discipline** | Rage-control / battle-trance / weapon-mastery baseline | Per elrond § 4.1 Seed #1+#3 supporting evidence; mythological + savage register synthesis |
| Hoplite | **Formation-Drill** | Armor-piercing baseline / shield-wall positioning / formation-bonus | Per elrond § 4.1 Seed #4 supporting evidence; european-medieval pole-weapon corpus |
| Siege-Master | **Loader-Rhythm** | Reload-cadence / ammunition-craft / engine-maintenance baseline | Per elrond § 4.1 Seed #10+#11 supporting evidence; siege/artillery operator register |
| Assassin | **Stealth-Step** | Critical-from-stealth / poison-application baseline / shadow-step | Per elrond § 4.2 Seed #14 supporting evidence; mythological Carnwennan anchor |
| Duelist | **Parry-Mastery** | Parry-window / riposte-stance / blade-reading baseline | Per elrond § 4.2 Seed #15 supporting evidence; european fencing tradition |
| Wildhunter | **Pack-Sense** | Feral-instinct / track-prey / companion-bond baseline | Per elrond § 4.2 Seed #17 supporting evidence + Seed #20 shield-off-hand absorption per design call (NEW supporting-chain absorption pattern; substrate evidence carries; semantic identity refined per gandalf design call) |
| Gunslinger | **Reload-Mastery** | Reload-rhythm / quick-draw / firearm-maintenance / bow+crossbow-reload baseline (absorbs Seeds #21+#22 bow+crossbow as supporting variance rather than dedicated chains) | Per elrond § 4.2 Seed #23 supporting evidence (#23 is the substrate's largest cluster); composes with Seeds #21+#22 absorption |
| Skirmisher | **Bulwark-Discipline** | Block-timing / mobile-block / shield-positioning baseline | Per elrond § 4.2 Seed #20 supporting evidence (cleanest substrate-anchored supporting chain per audit verdict) |
| Magus | **Spell-Lore** | Mana-channel / arcane-recall / spell-efficiency baseline | Per elrond § 4.3 Seed #27 supporting evidence; lineage signal (Pact Keeper / Ember Staff / Conflagration Tome) |
| Crusader | **Litany** | Consecration-aura / channel-uninterrupted / divine-presence baseline | Per elrond § 4.4 Seed #31+#34 supporting evidence; substrate-evidenced uniformly AoE-low-tempo (no rapid-cleric — substrate vote against high-tempo support) |

**Discipline #25 (semantic-layer rep-audit) applied at firing time:** when rocket Stage 3 implementation reaches T3 supporting-chain skill emission, rep-audit the substrate rows feeding the chain per gandalf OP § 4.4. If reps contradict class-intrinsic identity at any class, flag for design-call follow-on (this carries forward as Wave 5 cohesion-judge rep-audit obligation; composes with caster-faith HYBRID verdict § 7.4 obligation).

### 2.3 Active T4 mechanism design-spec (D66 + D65)

Per doc 40 § 8.1 + D66 sharpened (active identity discipline) + D65 (respec-with-legendary-trigger).

**Runtime-active marker:**
- Field name: `active_t4_chain: str | None`
- Type: chain identifier (e.g., `"shadow_strike"` for Assassin's T4 chain 1; `None` for L1-L30 pre-T4 state)
- Set: at chain-investment threshold reach (70% chain max per doc 40 D71 / D83 unlock); set to the FIRST T4 capstone reached if multiple chains cross threshold simultaneously
- Persists across save/load
- Read by gamora damage_resolver per consolidated doc § 3.6 for damage routing

**Switching mechanism (D65 respec-via-legendary-trigger):**
- Player legendary drop EVENT triggers spirit-guide-presented respec offer (per D75 + doc 41 § 5.4)
- Spirit-guide pacing: data-oracle voice neutral observation per Discipline #28; e.g., "Your current T4: Shadow-Strike. Projected KPM 75. Available T4 capstones in your chains: Venom-Craft (projected KPM 71). Switching costs: full respec point reallocation."
- Player chooses: keep active T4 / swap T4 (free if legendary-triggered window) / full respec (always available; cost per doc 40 D73 amendment - DEFERRED to Cycle 14+ per § 4.5)
- If swap: `active_t4_chain` updates; non-active T4 capstones REMAIN UNLOCKED (their chain investment is preserved; they are just not the active one per D66)

**Validation rules:**
- Only ONE T4 capstone may have `active=True` at any moment per kit (D66 sharpening)
- Supporting chain has NO T4 capstone; supporting chain skills are ALWAYS active (not gated by `active_t4_chain`)
- Non-active T4 chains' T1-T3 skills are ALWAYS active (only the T4 capstone is gated by `active_t4_chain`)
- Cross-chain T1-T3 skill access is NOT restricted (the 8-active-skill flat budget per D82 is the only constraint)

**Cross-seam impact (Stage 3 rocket MIGRATION.md):**
- Character JSON schema adds `active_t4_chain: str | None` + `supporting_chain: str` fields per consolidated doc § 3.6
- gamora damage_resolver consumes `active_t4_chain` for T4 damage routing per doc 47 § 4.1 fight-engine logic
- star-lord telemetry captures T4 swap events for cross-season learning loop (D25 + doc 41 § 5.3)
- drax loadout-app UI displays current active T4 + available swap T4s per D75 spirit-guide-as-surface pattern

---

## 3. BC-axis coverage map (Q-S2-8 + Q-S2-9 + Q-S2-10 + Q-S2-11 closure)

Per `reincarnated-substrate-vector-cheatsheet` 8-axis cell-address mapping.

### 3.1 Coverage matrix (10 classes × 8 BC axes)

| Class | Engagement | Damage geometry | Proxy density | Control density | Damage tempo | Amplitude variance | Defensive profile | Resource economy |
|---|---|---|---|---|---|---|---|---|
| Barbarian | close-fast | small-AOE (cleave) | solo | damage-pure | medium | variable | tank | charge-stack (rage) |
| Hoplite | mid-slow | small-AOE + single-target | solo | mixed (reach control) | low | flat | mitigator | steady |
| Siege-Master | ranged-slow | large-AOE | solo (proxy-light if multi-shell) | damage-pure | low | spiky | glass | generator-spender (loader-rhythm) |
| Assassin | close-fast | single-target | solo | mixed (stealth + poison-control) | high | spiky | dodger | charge-stack (stealth) |
| Duelist | mid-fast | single-target (chain on Flowing-Saber) | solo | mixed (parry-control) | medium | variable | dodger | generator-spender (parry-window) |
| Wildhunter | close-fast | single-target (multi-hit signature) | solo (proxy-light w/ Beast-Bond T4) | damage-pure | high | flat | dodger | steady |
| Gunslinger | mid-fast / ranged-fast | varies by T4 (single / scatter / multi-hit) | solo | damage-pure | varies by T4 (high pistol / low rifle / medium shotgun) | varies by T4 | glass | generator-spender (ammo/reload) |
| Skirmisher | close-slow | single-target + shield_blocker | solo | mixed (shield-bash control) | medium | flat | tank | damage-taken-converts (shield-block-to-resource) |
| Magus | mid-slow / ranged-slow | single-target | solo (proxy-light w/ Crystal-Familiar supporting variance) | damage-pure | medium | flat | glass | overflow (mana-pool) |
| Crusader | melee+mid (Consecrated-Strike) / mid+ranged (Banner-Rally / Channel-Aura) | varies by T4 (single / large-AOE buff / large-AOE channel) | solo | varies by T4 (damage-pure mace / control-pure rally) | low (measured) | flat | mitigator | HP-economy (Channel-Aura) / overflow (Banner-Rally) |

### 3.2 BC-cell gaps DEFERRED to v1.1 (substrate-led discipline; substrate-empty cells NOT designed without anchor)

| Gap cell | Substrate state | v1.1 path |
|---|---|---|
| **INT × AoE damage-geometry** | 6 thin rows | Q-S2-12 substrate-enrichment commission queued for Cycle 15; v1.1 unlocks "Elementalist" class (fireball/chain-lightning/blizzard) |
| **INT × high-tempo** | 0 rows | Combine with INT-AoE enrichment for "Battle-Mage" register; v1.1 |
| **WIS × high-tempo** | 0 rows | Substrate vote against rapid-cleric; v1.1 considers if cohesion-judge surfaces design-pressure |
| **WIS × melee-light (monk)** | 0 rows | Substrate-empty; v1.1 substrate enrichment for unarmed/staff-monk forms |
| **STR × thrown** | 0 javelin-on-STR | Substrate-empty; v1.1 substrate enrichment for "Marauder" register |
| **STR × high-tempo** | 33 rows (flail-anchored) | Absorbed into Barbarian Berserker-Rage chain as variance; not a separate class |
| **DEX × AoE (non-firearm)** | 33 rows (firearm-scatter-dominant) | Covered by Gunslinger Scatter-Burst chain; no separate class warranted |
| **Cross-attribute hybrid (red-mage / spellsword / paladin-STR-WIS)** | substrate `secondary_stat='none'` uniformly | Q-S2-14 substrate-enrichment commission queued; v1.1+ |
| **Multi-spawn / proxy-heavy (summoner)** | engine deferred per `project_pet_system` memory | v1.1+ pending pet-system implementation |

### 3.3 BC-cell over-saturation resolution (Q-S2-10 closure)

Per elrond audit § 3.3, 4 over-saturated cells in 34-seed substrate. Resolution:

| Over-saturated cell | Seeds | Resolution |
|---|---|---|
| **STR-melee-cleave-medium-tempo** | #1+#2+#3+#4+#7 | FOLD into 2 distinct classes (Barbarian = #1+#2+#3+#7 by mechanic absorption; Hoplite = #4 distinct by reach-bin) |
| **DEX-melee-single-high-tempo** | #14, partial #15, partial #16 | FOLD #15+#16 into Duelist (medium-tempo via subset selection); Assassin owns high-tempo single (Seed #14) |
| **DEX-ranged-single-medium** | #21+#22+#23+#26 | FOLD #21+#22+#26 into Gunslinger Reload-Mastery supporting chain as variance (bow+crossbow+javelin are sub-archetypes); #23 anchors Pistol-Quickdraw / Rifle-Precision T4 chains |
| **INT-mid-ranged-single-medium** | #27+#28+#29 | FOLD #28 (wand) into Magus as chain variant; #27+#29 distinct T4 chains within Magus |

**Substrate-led discipline check:** all folds preserve substrate evidence at class-internal variance level. No seed evidence is discarded; substrate's vote at the geometry layer is honored. Semantic-interpretation is the design-call (per Discipline #25 — gandalf curates which substrate cluster absorbs into which class identity).

---

## 4. Substrate-evidence anchoring per class (audit cross-reference)

Per dispatch § Item 7 § 4 — cross-reference elrond Stage 1 audit § 2 seed numbers per class.

### 4.1 Anchoring table

| # | Class | Primary substrate seeds (from elrond audit § 2) | Total named+unique rows anchored | Lineage signal source |
|---|---|---|---|---|
| 1 | Barbarian | Seeds #1 (119 sword) + #2 (46 hammer) + #3 (44 axe + 19 club) + #7 (9 flail + 2 morningstar) + folds #8 (7 pick) + #9 (3 mace-STR) | ~249 rows | european-historical + fantasy_generic (named) + european category lineage |
| 2 | Hoplite | Seeds #4 (62 glaive + 48 halberd + 30 lance + 6 pike + 5 polearm = 151 rows) + #5 (7 spear) | ~158 rows | european-medieval (named) + classical-Greco-Roman (thematic anchor) |
| 3 | Siege-Master | Seeds #10 (78 STR-AoE) + #11 (24 cannon + 6 catapult + 5 ballista + 36 siege_vehicle) | ~149 rows | european-industrial / modern (substrate's natural register) + fantasy-flavor extensibility (Dread Catapult) |
| 4 | Assassin | Seed #14 (41 dagger + 13 kris) | 54 rows | european + middle_eastern (kris) + mythological Carnwennan |
| 5 | Duelist | Seeds #15 (13 sword + 2 shortsword) + #16 (4 saber + 3 scimitar + 3 kukri) + folds #18 (2 rapier) | 27 rows | european + middle_eastern + south_asian (kukri) — lineage-diverse |
| 6 | Wildhunter | Seed #17 (12 claw) + Seed #20 substrate absorption (17 shield rows reframed as off-hand-companion) | 29 rows | fantasy_generic (claw) + lineage-diverse (shield) |
| 7 | Gunslinger | Seeds #21 (15 bow) + #22 (7 crossbow) + #23 (100 gun + 94 pistol + 88 rifle + 16 musket = 298 rows) + #24 (45 shotgun) + #25 (50 MG) + #26 (53 javelin in supporting variance) | ~468 rows (LARGEST cluster) | european + middle_eastern + east_asian (industrial period dominant) |
| 8 | Skirmisher | Seed #20 PRIMARY (17 shield rows; Pavise / Rondache / Targe / Dhàl / Shield of Saint George / Rhos Rydd Shield) | 17 rows | european + middle_eastern (Rondache/Targe) + south_asian (Dhàl) — cleanest lineage-diverse defensive cluster |
| 9 | Magus | Seeds #27 (64 staff) + #28 (4 wand fold) + #29 (54 rod) + #30 (27 crystal fold) | 149 rows | fantasy_generic + european (Pact Keeper / Ember Staff / Conflagration Tome) |
| 10 | Crusader | Seeds #31 (90 mace) + #33 (21 horn) + #34 (11 talisman + 7 banner + 42 AoE-faith Aegis/Censer/Holy Water Sprinkler) | ~171 rows | european (mace + censer) + fantasy_generic (banner + horn rally) |

**Aggregate:** ~1,470 named+unique rows anchor the 10 classes out of 969 total substrate named+unique. Apparent over-anchoring (1,470 > 969) reflects substrate sharing across classes (e.g., shield substrate anchors both Wildhunter off-hand and Skirmisher main-identity — different thematic registers consume same substrate) — substrate-led discipline applied.

### 4.2 Per Q-S2-4 lineage architecture disposition

Cycle 14 v1 ships **substrate-natural distribution** (no lineage-balance imposed). Substrate's named pool is 95% fantasy_generic; this becomes the natural Cycle 14 v1 register. Lineage diversity flavors emerge naturally where substrate carries signal:
- Assassin (kris middle_eastern flavor)
- Duelist (saber + scimitar + kukri lineage-diverse)
- Skirmisher (Pavise + Rondache + Dhàl lineage-diverse shields)
- Gunslinger (european-industrial + middle_eastern + east_asian)
- Crusader (european + fantasy_generic mixed)

**Cycle 15 substrate-enrichment commission candidate (Q-S2-13):** named-pool re-tagging pass (95% fantasy_generic → lineage-conscious tags via cross-reference to category-pool's 823 european + 119 east_asian + 52 south_asian signal) NOT FIRED for Cycle 14 v1. Re-tagging is a Cycle 15 v1.1+ enrichment if Wave 5 cohesion-judge surfaces lineage-collapse identity issues. Per gandalf OP § 4.4 semantic-layer rep-audit discipline — substrate's geometry vote is binding (cluster purity); semantic-layer use of lineage tags requires rep-audit at firing.

---

## 5. Substrate-enrichment commissions surfaced (Q-S2-12 / Q-S2-13 / Q-S2-14)

Per dispatch § Item 5; commissions to elrond for Cycle 15 (NOT Cycle 14 v1 gating).

### 5.1 Q-S2-12 — INT-AoE spell-implement enrichment (QUEUED for Cycle 15)

**Need:** unblock v1.1 "Elementalist" class (canonical fireball / chain-lightning / blizzard mage); current substrate has 6 thin INT-AoE rows.

**Scope:** ~30-50 row enrichment pass for AoE-INT spell-implement forms:
- Fireball-staff / pyromancer-rod / conflagration-grimoire variants (~10-12 rows)
- Chain-lightning-staff / storm-rod / tempest-orb variants (~10-12 rows)
- Blizzard-orb / frost-tome / icicle-wand variants (~10-12 rows)
- Meteor-tome / arcane-blast-rod / arcane-explosion-staff variants (~8-10 rows)

**Effort estimate:** ~3-5 hours elrond curation (per SC-6b precedent) + ~half-hour cross-seam rocket sanity-check + ~half-hour gandalf design review.

**Owner:** elrond (Mode B targeted crawl or curation pass); legolas if external research needed.

**Cycle 15 dispatch route:** KR authors after Cycle 14 Wave 5 cohesion-judge confirms v1.1 INT-AoE class is design-pressure (vs. Magus single-target arcane sniper register being sufficient).

### 5.2 Q-S2-13 — Named-pool lineage re-tagging pass (DEFERRED; not fired)

**Need:** v1.1+ lineage-conscious archetype design (e.g., "katana-samurai" / "claymore-highlander" / "khanjar-bedouin" cultural-tradition variants of existing classes).

**Status:** NOT fired for Cycle 14 v1. Substrate-led discipline says substrate's natural distribution (95% fantasy_generic) is the Cycle 14 v1 register; lineage-conscious archetypes are a v1.1+ refinement.

**Empirical trigger for Cycle 15 re-engagement:** Wave 5 cohesion-judge output reveals lineage-collapse identity issues across classes; OR Matt design-call surfaces lineage-conscious archetype as v1.1 priority.

**Effort estimate:** ~6-10 hours elrond curation + LLM-assisted name parsing per consolidated doc § 5.

**Owner:** elrond (with LLM-assistance via star-lord coordination if needed).

### 5.3 Q-S2-14 — Hybrid-attribute substrate enrichment (DEFERRED; not fired)

**Need:** v1.1+ cross-attribute hybrid classes (red-mage spellsword INT+DEX; paladin holy-warrior STR+WIS; battle-mage INT+STR).

**Status:** NOT fired for Cycle 14 v1. Cycle 13 `int_04_red_mage_spellsword` exposed the gap; substrate is empirically empty (`secondary_stat='none'` uniformly). Design-call decision per Q-S2-11: DEFER to v1.1.

**Cycle 14 v1 implication:** Crusader is NOT a STR/WIS hybrid; it is a WIS-primary class. The "holy knight with mace" register lives WITHIN Crusader as the Consecrated-Strike T4 chain (uses WIS scaling + mace weapon-binding per caster-faith HYBRID verdict Path B Wave 2 sampling adjustment), NOT as cross-attribute scaling.

**Empirical trigger for Cycle 15 re-engagement:** Wave 5 + Phase 5 cohesion-judge output + Matt design-call on cross-attribute hybrid as v1.1 priority. Composes with caster-faith HYBRID verdict Cycle 15 queued Path A classifier amendment (within-WIS discriminator may unlock hybrid classes if amended carefully).

**Effort estimate:** ~5-8 hours legolas Mode B + ~half-day elrond schema/curation + design-call ratification per consolidated doc § 5.4.

**Owner:** elrond + legolas + gandalf (design-call) + rocket (damage-routing implications per doc 47).

---

## 6. Doc 41 § 4 amendment — Season cardinality canonical decision

Per dispatch § Item 6; consolidated doc § 3.4 Option 2.

### 6.1 The amendment

**Doc 41 (`canonical/41-progression-framework-2026-05-27.md`) § 4 receives a new entry:**

> **§ 4.6 — Season cardinality (CYCLE 14 RATIFICATION; per consolidated doc § 3.4 + class roster doc 48)**
>
> Reincarnated v1 Cycle 14 production season ships **Option 2 — Multi-fire extension to 30-50 base kits**.
>
> - **Default `n_kits=40`** (within `bc_target_subspace_generator.py` multi-fire extension cap 50)
> - **Class distribution:** 40 base kits across 10 classes (per doc 48) = **average ~4 kits per class** with within-class variance via T4 + supporting-chain composition + lineage flavor (substrate-natural)
> - **Gauntlet PASS rate target:** ~70-80% pass-through (40 base → ~28-32 surviving characters per season)
> - **Composition with L50 hybrid framework:** ~28-32 characters per ~30-day season aligns with the "maximal quantity of characters who are unique/playable/balanced/thematically coherent to faction and season" intent (per Matt's stated season-quality target)
> - **Composition with doc 46 Layer 6 cohesion architecture:** cohesion-judge layered architecture operates against ~28-32 surviving characters per season; LLM cohesion-narrative generation budget aligned per star-lord pipeline planning
> - **Composition with doc 47 § 3 weapon profile + class roster doc 48 distribution:** Wave 5 production season generates kits with substrate-bound weapons per attribute profile + chain-aligned mechanical content per per-class architecture
>
> **Why Option 2 (not Option 1 22-base; not Option 3 open-ended faction-driven):** Option 1 (22 base) matches BC-cell base enumeration but is too narrow for "maximal quantity" intent; Option 3 (open-ended faction-driven) is production-scale but depends on faction-architecture decisions DEFERRED per recognition record `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`. Option 2 surfaces meaningful within-cell variety + gives the gauntlet a meaningful filter to do (~70-80% pass-through is genre-meaningful — every season has some failed candidates that didn't reach the band).
>
> **Empirical trigger for v1.1+ re-engagement:** Wave 5 telemetry data + cross-season learning loop (D25) feedback per `canonical/41-progression-framework-2026-05-27.md` § 5.3 star-lord telemetry framework. If gauntlet PASS rate drifts outside ~70-80% target, n_kits default tunes upward or downward per empirical evidence.

### 6.2 Amendment fires

I will append this amendment to doc 41 as a new § 4.6 entry below — see § 7.2 of this doc for the canonical amendment text.

### 6.3 Rocket Stage 3 implementation input

Rocket Stage 3 implementation amends `bc_target_subspace_generator.py` L173: `def generate(self, n_kits: int = 40)` (was 22). Multi-fire extension cap 50 preserved. Per consolidated doc § 3.3 implementation scope.

---

## 7. Stage 3 implementation guidance for rocket

### 7.1 Per-class implementation summary (Stage 3 input)

| # | Class | Implementation atoms | Per-class scope |
|---|---|---|---|
| 1-10 | All classes | Add class-roster registry data | One per row per § 1; `class_archetype` field + chain_count + T4 chain IDs + supporting chain ID + substrate weapon-binding hints (primary_stat + weapon_type_family preference list) |
| All | `per_skill_emitter.py` L130-152 | REPLACE hardcoded `["chain_A", "chain_B", "chain_C"]` + `[1,2,3,4]` flat grid | Per-class chain_count + per-chain T4-eligibility flag + per-chain target depth + supporting-chain T3-cap enforcement |
| All | `per_skill_emitter.py` _CHAIN_ROLE | REPLACE flat role-per-tier mapping | Per-class supporting-chain role identification; T4 capstone gating per active_t4_chain runtime marker |
| All | Character JSON schema | ADD `active_t4_chain: str \| None` + `supporting_chain: str` + `class_archetype: str` | Stage 3 MIGRATION.md entry per consolidated doc § 3.6 |
| Gunslinger + Crusader | 4-chain branching constraint | Implement depth ≤3 default for 4-chain classes; branching only on player-extended investment per doc 40 § 8.3.1 | 4-chain math-note required (rocket Stage 3 produces) |

### 7.2 Doc 41 § 4 amendment text (KR-routed if rocket Stage 3 cannot self-amend canonical docs)

The amendment text in § 6.1 above is authored canonically by me (gandalf) and lands at `canonical/41-progression-framework-2026-05-27.md` § 4.6 (new entry) as part of this Stage 2 close. See § 7.2 amendment-application step at session close.

### 7.3 Cross-seam contract changes (Stage 3 MIGRATION.md scope)

Per consolidated doc § 3.6 + this doc § 2.3:

- **rocket → gamora:** character JSON adds `active_t4_chain` + `supporting_chain` + `class_archetype` fields; gamora damage_resolver consumes for T4 damage routing
- **rocket → star-lord:** telemetry captures T4 swap events (active_t4_chain transitions); cross-season learning loop input
- **rocket → drax:** loadout-app schema-extension consumes class_archetype + active_t4_chain for character UI rendering; supporting chain visually distinct from T4 chains
- **gamora damage_resolver:** consumes `active_t4_chain` per doc 47 § 4.1 damage-routing logic
- **star-lord cohesion-judge LLM:** consumes class_archetype + supporting_chain for cohesion-narrative LLM prompting (Wave 3 cohesion-judge scope)

### 7.4 Active T4 mechanism implementation atoms (rocket Stage 3 math-note 3 input)

Per consolidated doc § 3.3 Item 5 — math note `wave-1-5-active-t4-runtime-math.md`:

- Active T4 runtime marker `active_t4_chain` set at chain-investment-threshold reach (70% chain max per doc 40 D71/D83)
- Switching mechanism: legendary-trigger respec per D65; spirit-guide-presented per D75 (data-oracle voice per Discipline #28)
- Non-active T4 chains' T1-T3 skills remain active (only the T4 capstone is gated by `active_t4_chain`)
- Supporting chain skills always active (T3-cap; no T4 gating)
- Validation: only ONE active T4 capstone per kit at any moment (D66 active identity discipline)

---

## 8. Q-S2 question resolution log (14 + 3 = 17 questions closed)

### 8.1 Elrond Stage 1 audit questions (14)

| Q | Question | Resolution |
|---|---|---|
| **Q-S2-1** | Roster cardinality (N classes) | **10 classes** — substrate-supported + thematic coherence + within L50 hybrid + n_kits=40 ~4 kits/class distribution |
| **Q-S2-2** | Fold-vs-distinct (STR-melee 5-seed over-saturation; thin substrate folds) | **FOLD per substrate-led discipline:** Barbarian absorbs Seeds #1+#2+#3+#7+#8+#9; Magus folds Wand (#28) + Crystal-Familiar (#30); Duelist folds Rapier (#18); Gunslinger folds Bow (#21) + Crossbow (#22) + Javelin (#26) into supporting variance |
| **Q-S2-3** | Substrate-gap closure (Cycle 13's 5 exposed gaps) | **DEFER all 5 to v1.1 per substrate-led discipline:** INT-AoE / red_mage_spellsword / STR-light-fighter / WIS-storm-caller / WIS-monk. Substrate-enrichment commission Q-S2-12 queued for Cycle 15 (INT-AoE); others queued empirically (gated on Wave 5 cohesion-judge output) |
| **Q-S2-4** | Lineage architecture (named pool 95% fantasy_generic) | **Substrate-natural distribution for Cycle 14 v1.** Cycle 15 Q-S2-13 re-tagging pass DEFERRED (not fired); empirical trigger = Wave 5 cohesion-judge identifies lineage-collapse identity issues |
| **Q-S2-5** | Per-class chain count assignment | **Substrate-natural (per elrond § 4.5 substrate vote):** 8 classes × 3-chain + 2 classes × 4-chain (Gunslinger + Crusader). Substrate's natural distribution honored; not imposing uniform chain count |
| **Q-S2-6** | Supporting chain identity (substrate-evidenced vs design-coherent) | **Substrate-evidenced primary + design-coherent finalization per § 2.2 table.** All 10 supporting chains carry substrate-evidence anchor (per elrond § 4); design-coherence finalizes naming + theme |
| **Q-S2-7** | Cross-class supporting-chain sharing | **Per-class unique** (no cross-class sharing). Design-coherence supports variety; substrate vote supports per-class identity. Iron-Discipline / Formation-Drill / Loader-Rhythm / Stealth-Step / Parry-Mastery / Pack-Sense / Reload-Mastery / Bulwark-Discipline / Spell-Lore / Litany — 10 distinct identities |
| **Q-S2-8** | INT-AoE substrate gap | **DEFER to v1.1.** Cycle 14 v1 ships Magus as `single` damage-geometry only (substrate-led per § 1.9). Q-S2-12 substrate-enrichment commission queued for Cycle 15 |
| **Q-S2-9** | DEX-firearm class architecture (one versatile vs multiple specialists) | **ONE versatile 4-chain Gunslinger.** Substrate has largest single form-vocabulary cluster (288 rows on gun+pistol+rifle+musket) AND geometry-diverse coverage; substrate-vote supports 4-chain versatility over multiple-3-chain specialists (would manufacture distinction) |
| **Q-S2-10** | STR-melee over-saturated cell (5 competing seeds) | **FOLD per § 3.3 over-saturation resolution table:** 5 seeds → 2 distinct classes (Barbarian by mechanic absorption #1+#2+#3+#7; Hoplite by reach-bin distinction #4) |
| **Q-S2-11** | Cross-attribute hybrid classes | **DEFER all to v1.1.** Substrate `secondary_stat='none'` uniformly; no substrate vote for hybrid. Q-S2-14 commission queued for Cycle 15 + Matt design-call empirical trigger |
| **Q-S2-12** | INT-AoE enrichment commission | **QUEUED for Cycle 15.** ~30-50 rows AoE-INT spell-implement forms; effort ~3-5 hours; gates on Wave 5 cohesion-judge output confirming Magus single-target alone is design-pressure |
| **Q-S2-13** | Named-pool lineage re-tagging | **DEFER to v1.1.** Cycle 14 v1 uses substrate-natural distribution; re-tagging Cycle 15 candidate gated on Wave 5 cohesion-judge lineage-collapse identification |
| **Q-S2-14** | Hybrid-attribute substrate enrichment | **DEFER to v1.1.** Composes with Q-S2-11 cross-attribute deferral + caster-faith HYBRID verdict Cycle 15 queued Path A classifier amendment |

### 8.2 Dispatch open questions (3)

| Q | Question | Resolution |
|---|---|---|
| **Q-S2-15** | If Q-S2-11 ships hybrid classes, how does this compose with rocket Wave 1 LegendaryCapabilityScope enum (5 local scopes; no character_wide/chain_wide)? | **N/A for Cycle 14 v1** — no hybrid classes shipped per Q-S2-11 deferral. 5 local scopes (slot-bound / trigger-bound / skill-specific / item-family / state-conditioned per doc 46 § 4) are sufficient for the 10 non-hybrid classes. character_wide / chain_wide remain reserved for T4 per doc 46 § 4.3. For v1.1+ hybrid classes (if shipped post Q-S2-14 enrichment): scope-extension would be evaluated at Cycle 15+ design call; HYBRID classes may need a new scope type (e.g., `attribute_bound`) or absorb into existing scopes per attribute-tagged capability. Defer to Cycle 15 design-call when Q-S2-11 / Q-S2-14 land. |
| **Q-S2-16** | Class-roster naming convention (human-readable vs fantasy-evocative vs Latin/genre-trope) | **Human-readable genre-canonical names** for Cycle 14 v1 (Barbarian / Hoplite / Siege-Master / Assassin / Duelist / Wildhunter / Gunslinger / Skirmisher / Magus / Crusader). Composes with D7 AI-tell discipline — Wave 3 cohesion-judge LLM consumes class names; human-readable genre-canonical names produce predictable LLM-narration anchors. Fantasy-evocative variants (e.g., "Wolfborn" / "Stormcaller") DEFERRED to v1.1+ if season-thematic register surfaces design-pressure (e.g., a "Wolves of Fenris" themed season may re-skin Wildhunter as Wolfborn). |
| **Q-S2-17** | Per-class equip restrictions (weapon-family restrictions vs substrate-suggested player flexibility) | **Substrate-suggested with player flexibility** for Cycle 14 v1. Class metadata declares preferred `weapon_type_family` per attribute profile (per doc 47 § 3.1); substrate weapon-binding per Wave 0.5 generates per-class-aligned defaults; player flexibility preserved at gear-pickup level (player can equip any compatible weapon — e.g., Barbarian can equip a DEX-light dagger, but loses STR-primary scaling). Composes with doc 47 hybrid-scaling per-skill design (skills declare scaling-attribute; weapon misalignment surfaces as suboptimal-not-broken). v1.1+ may introduce stricter class-weapon restrictions if Wave 5 telemetry reveals player-confusion or balance-distortion from cross-class equipping. |

---

## 9. Composition with Cycle 14 disciplines + caster-faith HYBRID verdict

### 9.1 Discipline #40 (LOAD-BEARING) — canonical lock option (a)

Per consolidated doc § 4. **This doc IS the canonical decision per Discipline #40 option (a).** Class roster is RATIFIED-AS-CANONICAL — NOT SCAFFOLD-WITH-PENDING-DECISION. No MIGRATION.md flag needed for class-roster scaffold-debt; rocket Stage 3 implementation consumes from this doc as canonical input.

Substrate-enrichment commissions (Q-S2-12 / Q-S2-13 / Q-S2-14) are NOT class-roster scaffold-debt — they are v1.1+ feature deferrals with empirical-evidence triggers per gandalf OP § 3.4 recognition-validate-commit discipline.

### 9.2 Discipline #25 (semantic-layer rep-audit) — applied at Wave 5 + Phase 5

Per gandalf OP § 4.4 + caster-faith HYBRID verdict § 7.4. At Wave 5 cohesion-judge firing + Phase 5 thematic-coherence assessment:

- Rep-audit each class's substrate anchoring per § 4.1 table
- Verify top-N reps match the class identity downstream consumes (e.g., Crusader's mace-faith substrate per HYBRID Wave 2 sampling adjustment; Wildhunter's claw+shield substrate per § 1.6 absorption pattern)
- If reps contradict class identity, flag for design-call follow-on per Cycle 15 queued items

### 9.3 Discipline #18 (methodology-before-execution) — design call complete

This doc IS the design-call output for class-roster curation. Rocket Stage 3 implementation does NOT fire until:
- KR ratifies this doc + integrates into Stage 3 dispatch
- Doc 41 § 4.6 amendment lands (see § 7.2)
- jack-ryan Gate-1 reviews Stage 3 rocket dispatch
- Matt sign-off on Stage 3 dispatch fire

### 9.4 Composition with caster-faith HYBRID verdict (38d0d73 awaiting Matt sign-off)

Crusader class (§ 1.10) inherits the HYBRID verdict's Path B (Wave 2 within-caster-shape sampling adjustment). Within Crusader:
- Consecrated-Strike T4 chain: substrate-bound to mace + war-hammer family (per Interpretation III mace-as-faith-slice preservation; ~25% of caster-faith sampling per Path B weight)
- Banner-Rally T4 chain: substrate-bound to banner + horn family (~25% sampling weight)
- Channel-Aura T4 chain: substrate-bound to talisman + censer + holy-water-sprinkler family (~25% sampling weight)
- Supporting chain Litany: substrate-bound to staff-scepter-rod faith-variant + sacred-symbol family (~15% sampling weight)

If Matt signs off the HYBRID verdict for Wave 2 (Fix B + Fix B-prime dispatch), Crusader implementation gets the substrate-sampling support automatically. If Matt rejects the HYBRID verdict (unlikely per verdict's gandalf-lean), Crusader implementation falls back to substrate-natural 62% mace-dominance for Wave 5 — Wave 5 cohesion-judge would surface the cleric-with-mace identity collapse and Cycle 15 Path A reclassification commission would fire.

### 9.5 Composition with framing brief Q10 (quality > timeline)

Per Matt 2026-05-27 verbatim "extend timeline as needed for Wave 0.5 and all waves. The goal is not to ship something but to ship a game (playable characters that run the gauntlet in band)." This doc honors Q10 by:
- NOT manufacturing classes without substrate anchor (substrate-led discipline)
- DEFERRING v1.1 substrate gaps (INT-AoE / monk / spellsword / etc.) rather than designing thin classes
- ENRICHING substrate via Cycle 15 commission rather than synthesizing class identity at design time
- Per Q9 Cycle 13 cohort DISREGARDED — class roster is fresh-substrate-led; Cycle 13's 16 archetype names are NOT carried forward (the 10 names here are derived from substrate vote + thematic coherence, not from Cycle 13 cohort)

---

## 10. Framing-audit checklist (per gandalf OP § 4.1 — applied to this verdict)

| Q | Answer |
|---|---|
| **Q1 — Load-bearing framing assumptions** | (a) Elrond Stage 1 audit's 34 seeds + BC-axis coverage + chain-count vote are empirically correct (reproducible from DB queries); (b) substrate-led discipline (Discipline #25) is load-bearing for class-roster decisions — semantic-layer choices made by gandalf, geometry-layer votes made by substrate; (c) the 10-class cardinality target is design-call territory (not substrate-imposed); substrate supports anywhere from 6 to 18 classes depending on fold-distinct decisions; (d) the L50 hybrid framework + n_kits=40 distribution composes cleanly with ~10 classes × ~4 kits/class; (e) Discipline #40 canonical-lock option (a) is operative — this is NOT scaffold-with-pending-decision |
| **Q2 — Refutation evidence in current scope** | (a) elrond audit queries reproducible at any time (substrate state stable); (b) caster-faith HYBRID verdict's Path B sampling adjustment is empirical hypothesis (Wave 2 sampling weight tunable); (c) Wave 5 cohesion-judge output will surface whether 10 classes is correct cardinality OR whether substrate gaps (INT-AoE / monk / hybrid) are load-bearing; (d) Discipline #40 RATIFIED canonical-lock is testable: rocket Stage 3 implementation consumes this doc; if rocket surfaces architectural friction, doc is amendable per Discipline #1 math-before-code |
| **Q3 — Refine framing rather than execute?** | NO — execute per § 1-§ 9 design-spec. Refinement triggers ARE captured: (a) Wave 5 cohesion-judge empirical evidence gates substrate-enrichment commissions Q-S2-12/13/14; (b) caster-faith HYBRID verdict gates Cycle 15 Path A classifier amendment + Crusader within-class sampling validation; (c) all v1.1+ substrate gaps (INT-AoE / monk / spellsword) carry explicit empirical-evidence triggers per gandalf OP § 3.4 recognition-validate-commit discipline; (d) rocket Stage 3 implementation surfaces architectural friction → return to design call. Refinement is post-empirical-evidence, not pre-execution |

**Refutation surface flagged:** the 10-class cardinality is gandalf design-call territory (NOT substrate-imposed). Substrate supports 6-18 classes per fold-distinct decisions. I chose 10 because (a) it provides clean BC-axis coverage without manufacturing distinction at over-saturated cells, (b) ~4 kits/class at n_kits=40 produces meaningful within-class variance for the gauntlet to filter, (c) it composes with L50 hybrid framework + ~30-day season target, (d) Cycle 13's 16-cohort is too many (manufactured distinction at substrate-empty cells) and 8 classes would be too few (loses BC-axis variety). 10 is the substrate-supported sweet spot, but Matt may amend if season-cardinality empirical evidence reveals different. Per Discipline #40 option (a), this is the canonical lock; amendments fire per future cycle empirical evidence.

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — v1 canonical class roster lock; Discipline #40 option (a) ratification; Wave 1.5 Stage 2 deliverable
**Authority:** Matt 2026-05-27 ratified Option C path per scaffold-drift consolidated package § 3.5; KR autonomous on Stage 2 dispatch firing per Cycle 14 scope-doc § 4.1; Discipline #40 LOAD-BEARING (gandalf prior canonical write `b282966`)
**Composition:** with doc 38 (delivery strategy), doc 39 (engine workflow), doc 40 § 8.3 / § 8.3.1 / § 6.6.1 / D65 / D66 / D69 / D83 (chain architecture + supporting chain + active T4 mechanism), doc 41 § 4.6 NEW amendment (season cardinality Option 2 n_kits=40), doc 46 § 4 (LegendaryCapabilityScope LOCAL; T4 reserves character-wide/chain-wide), doc 47 § 3.1 (per-attribute weapon profile), caster-faith HYBRID verdict (Crusader composition), Cycle 14 framing brief Q9 + Q10 (Cycle 13 DISREGARDED; quality > timeline), elrond Stage 1 audit (34 seeds + 14 questions), scaffold-drift consolidated package (Option C path)

**For:** the canonical class roster for Reincarnated v1 Cycle 14 (10 classes) + per-class chain architecture (chain count + T4 chains + supporting chain identity) + active T4 mechanism design-spec (D66 + D65) + BC-axis coverage map + substrate-evidence anchoring per class + substrate-enrichment commissions surfaced for Cycle 15 + doc 41 § 4.6 season cardinality canonical amendment (Option 2 n_kits=40 default) + Stage 3 rocket implementation guidance + 17 question resolutions (14 elrond + 3 dispatch). Substrate-led discipline applied throughout (substrate vote binding at geometry; semantic-layer curation by gandalf design call). Discipline #40 canonical lock option (a) — NOT scaffold-with-pending-decision.

**Signed:** gandalf (story-and-design steward)
