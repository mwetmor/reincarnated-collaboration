# Bestiary Race Well — Design (the vessel-race substrate)

> **STATUS:** CURRENT — authored + Matt-ratified in-session 2026-07-09 (Pattern-B design session;
> all four forks ruled: *"Agreed on all above"* + orc-construction ruling). Companion to
> `mob-affix-system-spec-2026-07-09.md` §3.1/§3.1a (which binds admission constraints) and the S2
> ledger ruling (vessel-race = bestiary provenance). Consumed by E10 Leg 3 (build) + S3 (faction
> visibility) + S4 (order-noun grammar) + C4 demo curation.

**Author:** gandalf. **Ruled:** Matt, in-session 2026-07-09 (Forks W1–W4 + orc construction-tier + elf/dwarf frame confirmation; **Q17 Big_Ork-native construction ruled same-day** on spec-sheet review + gandalf skeleton/size decode).
**Empirical grounding:** Synty library survey (this session — `~/Games/reincarnated-godot/Assets/Synty/`, ~60 packs; `catalogue/` crawl exists) + Q7 retarget contract artifacts (`goblin_bone_map.tres`, `anim-goblin-locomotion`) + **drax humanoid-asset inventory** (`agentic_orchestration/research/2026-07-09-synty-humanoid-asset-inventory.md`, d7e2dff — landed mid-session from the autonomous run's Lane 4; cross-checks this slate at file level).

---

## 0. The architecture (Fork W1 — RATIFIED)

**Race = the FRAME (skeletal kind). Register = the DRESSING (cultural-tech expression). Identity cell = race × register.**

The Synty library itself factors this way (one human frame family across viking/samurai/egypt/empire/pirate/western/city register packs), and the engine is already register-rich (culture/period/register LIVE end-to-end via weapon substrate — S1 walk). Matt's founding example decomposes cleanly: **"space orc" = orc × military_modern** — not a race, a cell.

- **Cardinality:** 5 races × 4 registers = up to 20 identity cells from a single-digit well — budget (§3.1a: R ≤ P/(M×F), v1 4–6) satisfied without sacrificing variety.
- **Factions ≈ populated race×register cells** (~700 kits / 20 cells ≈ 35/cell ≈ faction mass M). Sparse — the substrate votes which cells populate; empty cells stay verifiably empty (no force-fill). PM-1 clustering discovers these natively (tech/lineage/tone are already its evidence).
- **Godot scope:** race count = bone-map count; registers are material/prop dressing on existing frames.

## 1. Two-tier admission cost model (Matt orc-construction ruling)

| Tier | Construction | Rig cost | Precedent |
|---|---|---|---|
| **Reskin race** | Human frame + material swap + modular piece variation (bulk/ears/etc.) | **ZERO — rig-conformant by construction** (IS the human rig; full animation library inherited) | **Orc** (Matt: green skin + more robust musculature as modular assets, *"without altering the skeleton's dimensions"*) |
| **Reframe race** | Own skeleton + BoneMap `.tres` + locomotion set | One bone map + animation set per race | **Goblin** (`goblin_bone_map.tres` + `anim-goblin-locomotion` exist because proportions demanded them) |

Readability check (galadriel LOD register): at Camera B′ 20 m / ~8% hero fraction, **color + silhouette are the distance-surviving channels** — reskin races differentiate at gameplay camera (genre precedent: D2 palette-swap families). Mob-side, this keeps the E10 §7 model-visual telegraph channel viable.

## 2. The v1 admitted slate (curated in-session — Matt 2026-07-09)

| Race | Tier | Rig status | Asset evidence | Adjectival |
|---|---|---|---|---|
| **Human** | base frame | **VERIFIED by construction** | deepest coverage (~10+ register packs) | human |
| **Goblin** | reframe | **VERIFIED TODAY** (Q7 artifacts; drax retargets it now) | goblin-war-camp + own locomotion pack | goblin / goblinoid |
| **Orc** | **reskin** | **VERIFIED (bone-dump 2026-07-09):** native `Big_Ork` = 21/21 sidekick-core, standard rest proportions (pelvis 0.876 / spine_03 1.337 — identical to the human frame), binds `sidekick_bone_map.tres`, zero new rig work | **Construction ✓ RULED (Matt 2026-07-09, Q17): native `Big_Ork` body.** Matt conditioned on humanoid skeleton/size after pulling the pack spec sheet (`Character_BR_BigOrk_01.prefab` — 49 bones, bounds 2.92 × 0.84 × 2.08 m); gandalf decode confirmed: 49-bone Sidekick-family humanoid rig (in-Godot probe is the decisive evidence — 21/21 sidekick-core, binds `sidekick_bone_map.tres`, same map render-proven on Wizard/King); **2.08 m = MESH envelope on the human-height skeleton** (head bone 1.663 m, identical to human/elf/dwarf frames); 2.92 m = T-pose arm span. Bulk is mesh-baked; skeleton standard — the reskin contract exactly. drax recommendation + gandalf co-sign adopted: rig cost TIE at zero, **silhouette WINS** at Camera B′ 20 m (monster identity is silhouette-first at ARPG camera), **pattern-consistency WINS** (all three rival races = native body + shared rig). Modular path retired to INTRA-race variety (armor/faction dress), not race identity; the modular-asset enumeration obligation DIES. Probe artifact `agentic_orchestration/research/2026-07-09-drax-race-well-bone-dump-probes.md` | orcish |
| **Elf** | **reskin** | **VERIFIED (bone-dump 2026-07-09):** `DarkElf` = 21/21 sidekick-core, canonical 50-bone Sidekick body, `verified=true` | `DarkElf` body in fantasy-rivals + Matt frame confirmation; probe artifact as above | elven |
| **Dwarf** | **reskin** (open question RESOLVED) | **VERIFIED (bone-dump 2026-07-09):** 21/21 sidekick-core; bone set identical to DarkElf + one non-topological `Belly_01` helper; **rest proportions IDENTICAL to the standard rig — the stubby silhouette is mesh-baked, not skeleton-baked** → textbook reskin, zero new rig cost, no own locomotion set | `Dwarf` body in fantasy-rivals (dwarven-dungeon itself environment-only); probe artifact as above | dwarven |

**Count: 5 — inside the §3.1a budget (4–6).** The well is CLOSED (no LLM race derivation, ever); growth is a curation act.

## 3. Fork rulings W2–W4

- **W2 — undeath is the vessel-STATE, not a race.** Every vessel is a shaped corpse; admitting "skeleton" as a race is a corpse wearing a corpse. Skeleton/zombie/werewolf frames (confirmed on disk: `SK_Dungeon_SkeletonSoldier/Knight`, boss-zombies pack, werewolf pack) serve **MOB-ONLY kinds** — the realm's restless dead, the order's discarded work, beast-tier horrors. *Design-latent, not v1:* "Revenant" = vessels shaped from long-dead stock (bone showing) as a texture tier.
- **W3 — NO race×element coupling kit-side.** Element is a BC-cell coordinate; race bias would fight the certified coordinate space (and telemetry already carries a fire-selection-bias finding). Mob-side race×element affinity lives where it belongs — the E10 §3.1 affinity profiles.
- **W4 — demo realm (One-Realm MVP, enchanted-forest ravine):** **elf-native realm; human crusader-stock common; goblin war-camps in the ravine** (the pack exists); orc/dwarf sparse. Decides the ~20-kit demo race distribution at C4 curation.

## 4. Race-row schema (build target for Leg 3)

| Field | Content | Consumer |
|---|---|---|
| `race_id`, noun / plural / **adjectival form** | §2 table | naming grammar (D7 fill requires the adjective) |
| rig binding | `tier` (reskin\|reframe) + base_frame ref + BoneMap ref (reframe only) + **verified flag** + variant/material space | Godot (Q7 contract) — admission criterion 1 (§3.1a) |
| `becomable` | bool — two-tier bestiary gate | vessel well vs mob-only kinds |
| register affinities | SPARSE weights over the 4-enum — **v1 design seeds (DRAFT; PM-1 evidence refines):** human = all four (baseline) · orc = fantasy + military_modern (the space-orc cell) · elf = fantasy + mythological · dwarf = fantasy + historical · goblin = fantasy + military_modern (scrap-tech) | kit-gen + faction cells |
| affix affinity profile | over the 8 functional families (sparse) | E10 §3.1 mob-side |
| culture seeds | name-morphology guidance for narrow-blank LLM fill — human = register-driven (viking/samurai/… per culture) · orc = hard-consonant guttural · elf = liquid long-vowel · dwarf = stone-compound kennings · goblin = short guttural chatter | Wave B kit names + PM-2 faction labels (S4 noun grammar rides here) |

## 5. Design-latent (named, NOT committed — no v1 scope)

**Well-growth is diegetic for free:** *the order can only shape vessels from kinds it has reaped in numbers* — reap a new kind enough and that vessel becomes shapeable. §12 PURSUE feeds the vessel well; the bestiary (§11a record-of-conquest) doubles as the vessel catalog. v1 well is FIXED at the §2 slate; this fires only as a future curation+build decision.

## 6. What remains before Leg 3 consumes the well

1. **Lane 4a ✓ CLOSED (bone-dump probes LANDED 2026-07-09):** drax's inventory (d7e2dff) + in-Godot probes (`probe_race_well_bones.gd`, godot `1970bcb`; artifact `agentic_orchestration/research/2026-07-09-drax-race-well-bone-dump-probes.md`) — **all three file-inferred races resolve 21/21 sidekick-core, `verified=true`; Dwarf resolves RESKIN; NOTHING blocks.** ~13 conformant candidates remain on the **bench** outside the closed well; admission is a future curation act. **⚖ Orc construction ✓ RULED same-day (Matt: native `Big_Ork` — §2 row; Q17 closed)** + ceiling cross-check ✓ (R=5 inside the §3.1a budget 4–6; 5 races × 4 registers = 20 cells; ~700 kits / 20 ≈ 35/cell = binding faction mass M, consistent with the S2 verification arithmetic 700/140 = 5.0 exact). **NOTHING REMAINS — the well is Leg-3-ready.** (Modular-asset enumeration obligation died with the native ruling.)
2. **Leg 3 build acceptance (adds to mob-affix spec §11):** kit generation consumes ONLY admitted races with `verified=true` rig bindings; adjectival + culture-seed fields present for all five; demo curation draws W4 distribution; mob-only kinds never enter the vessel well.

**Signed:** gandalf, 2026-07-09. Rulings: Matt, in-session. *The well is closed, the frames are counted, and no corpse is worn that was not first reaped.*
