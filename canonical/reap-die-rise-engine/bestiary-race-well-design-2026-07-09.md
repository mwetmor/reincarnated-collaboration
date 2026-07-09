# Bestiary Race Well — Design (the vessel-race substrate)

> **STATUS:** CURRENT — authored + Matt-ratified in-session 2026-07-09 (Pattern-B design session;
> all four forks ruled: *"Agreed on all above"* + orc-construction ruling). Companion to
> `mob-affix-system-spec-2026-07-09.md` §3.1/§3.1a (which binds admission constraints) and the S2
> ledger ruling (vessel-race = bestiary provenance). Consumed by E10 Leg 3 (build) + S3 (faction
> visibility) + S4 (order-noun grammar) + C4 demo curation.

**Author:** gandalf. **Ruled:** Matt, in-session 2026-07-09 (Forks W1–W4 + orc construction + elf/dwarf frame confirmation).
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
| **Orc** | **reskin** | **VERIFIED by construction** (Matt ruling: human frame + green material + bulk modular pieces) | asset work = drax enumeration (materials + pieces); **native `Big_Ork` body also on disk** (fantasy-rivals, file-inferred conformant) — Lane 4a weighs modular-reskin vs native body; both rig-conformant | orcish |
| **Elf** | reskin-likely | **file-inferred CONFORMANT** (drax inventory: `DarkElf` ships in the proven Sidekick rig family) — in-Godot bone-dump probe pending (Lane 4a) | `DarkElf` body in fantasy-rivals (drax-verified on disk) + Matt frame confirmation | elven |
| **Dwarf** | reskin-or-reframe (the open one) | **file-inferred CONFORMANT** (drax: `Dwarf` body in the Sidekick rig family — existing bone map likely covers it); bone-dump resolves the tier (mesh-baked proportions → reskin-class cost) | `Dwarf` body in fantasy-rivals (drax-verified on disk; dwarven-dungeon itself is environment-only — verified this session) | dwarven |

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

1. **Lane 4a (in-flight, autonomous run):** drax's read-only inventory **LANDED mid-session** (d7e2dff) — elf (`DarkElf`) + dwarf bodies confirmed on disk in the proven Sidekick rig family; ~13 conformant race-type candidates total (Troll already rig-PROVEN on the goblin map) sit on the **bench** outside the closed well; admission is a future curation act. Remaining before Leg 3: in-Godot bone-dump probes (`scripts/dump_bones.gd`) for DarkElf/Dwarf (+ `Big_Ork` if the native body is chosen over modular reskin), orc modular-asset enumeration (materials + bulk pieces), final ceiling math cross-check. The curation memo's function is now **verification of THIS slate**, not proposal.
2. **Leg 3 build acceptance (adds to mob-affix spec §11):** kit generation consumes ONLY admitted races with `verified=true` rig bindings; adjectival + culture-seed fields present for all five; demo curation draws W4 distribution; mob-only kinds never enter the vessel well.

**Signed:** gandalf, 2026-07-09. Rulings: Matt, in-session. *The well is closed, the frames are counted, and no corpse is worn that was not first reaped.*
