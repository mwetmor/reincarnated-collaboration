# SB-1 CP-A · SYNTY ENEMY-TYPE BODY CENSUS (drax)

**Ledger row:** A1b-6 / **R-CPA-2** · **Date:** 2026-08-12 · **Author:** drax (presentation seam)
**Commissioned by:** Matt, at the SB-1 CP-A close.
**Companion:** `agentic_orchestration/drax/notes/2026-08-12-sb1-a1b-statics-landing.md` (the six
dresses this census is measured against; R-CPA-1 KEEPS them).
**Register:** Crucible-adjacent dark fantasy (K-2 ruling; 2026-08-01 render-exhibit lineage).
**Mode:** reconnaissance + judgment. **NOT a build.** Read-only on the asset tree; the only write
is this file.

**Targets under test:** **163** (the baton's own measured distinct-`display_name` count across the
344-actor roster of E-s09-cp150) · **32** (galadriel R2 threat-grammar lap 2026-08-08: the Grim
Dawn reference's on-camera named-body count in the priority band — Matt's minimum floor) · **6**
(current).

---

## 0 · HEADLINE

| measure | count |
|---|---|
| distinct Synty character bodies on this Mac (deduped) | **383** |
| **(a) enemy-type outright** | **137** — of which **88 are Tier-1** (core dark-fantasy register, needs no argument) |
| **(b) conscriptable** (civilian/neutral, dresses as a combatant) | **94** |
| **(c) out-of-register** | **152** |
| already proven to animate in this repo | **16** distinct bodies across 18 `scenes/rigs/mobs/*.tscn` |
| honest augmented ceiling, Tier-1 only, today's rig grammar | **~350–530** distinct identities |
| honest augmented ceiling, all 137 enemy-type | **~550–820** |

**The finding that changes the question: there is no remainder to fill.**
137 enemy-type bodies + 26 of the 94 conscriptables = **163 distinct base bodies, 1:1 against the
163 names, with ZERO augmentation.** Holding to Tier-1 purity alone (88 bodies), a **single**
palette axis (the authored `_01_A/B/C` atlas alts, already same-layout verified) reaches
88 × 2 = 176 > 163.

Matt's augmentation proposal was scoped as a gap-filler. **The census says the gap does not
exist.** My recommendation is therefore to HOLD the augmentation axes rather than spend them — and
to route the real blocker, which is **not assets**. See § 5.

---

## 1 · METHOD, AND ITS BASIS (stated per pack)

**Basis is EXHAUSTIVE, not sampled** — the tree was small enough to walk completely. Two
enumeration paths, because Synty ships characters two ways:

1. **Per-body FBX** — `SK_Chr_*`, `SK_Character_*`, `SK_BR_Character_*`, `SK_Dungeon_*`. Counted by
   distinct basename.
2. **Combined character FBX** — packs that ship one `Characters.fbx` with every body as a node
   inside it (dark-fortress, goblin-war-camp, viking-realm, dungeon-realms, ancient-egypt,
   samurai-empire, fantasy-village). Node names extracted with `strings -n 6` and filtered.
   Verified against a known case: goblin-war-camp `Characters.fbx` → 15 bodies + 2 hood/shawl
   attachments, matching the pack's published roster.

**Dedupe rules applied, in order:**

| rule | effect |
|---|---|
| `SK_Chr_X` ≡ `Chr_X` ≡ `SK_Character_Human_X` | same body, per-body export vs combined-FBX node name vs older naming |
| mirror packs dropped | `polygon-dark-fantasy-01`, `-dungeon-pack`, `-fantasy-characters-pack`, `-modular-fantasy-hero-characters`, `-animation-goblin-locomotion`, `-dwarven-dungeon-map` — verified identical FBX name-sets to their twins |
| non-bodies stripped | `SM_Chr_Attach_*`, `SK_Wep_*`, `SK_Prop_*`, `SK_Veh_*`, `_Wing_`, `SkinCluster`, loose limb/hair/beard parts |
| modular parts packs excluded from the body count | see § 1.1 — they are not bodies, they are an augmentation engine |

**Reproduction:** three scripts, all read-only on `Assets/` —
`census_bodies.sh` (enumerate) → `census_dedupe.sh` (normalise; emits
`census/bodies_distinct.tsv`, **383 rows**) and `rig_probe.sh` (skeleton-family probe). They live at
`/tmp/drax-census-2026-08-12/`, **outside every repo**.

**⚑ Containment note, stated because I got it wrong first.** I initially wrote these scripts into
`reincarnated-godot/tmp/`, which took that repo's porcelain from 236 → 240. This is a
**reconnaissance cell with no write mandate on the Godot tree**, so scratch scripts do not belong
there. Moved out; porcelain back to **236**, and all four artifacts verified gone.
**236 is not the 233 L-0 pin, and the 3-line delta is NOT from this cell** — it is
`tmp/br2watch/measure/census.json` (modified, BR2-WATCH lineage, commit `1c55f88`) plus
`scripts/_tmp_skirt_probe.gd` and `scenes/_tmp_skirt_probe.tscn`. All three predate this cell's
first command. Recorded rather than quietly absorbed, and **routable to whoever owns the skirt
probe** — it is loose in `scripts/` and `scenes/`, not in `tmp/`.

### 1.1 · Excluded from the body count: the two modular engines

Neither is a set of bodies. Both are combinatorial part libraries, and **neither is referenced by
any scene or script in the repo today** (0 rigs).

| pack | inventory | note |
|---|---|---|
| `polygon-modular-fantasy-heroes` | **1,494 part FBX across 25 slots** — 72 heads · 58 torsos · 58 hips · 42+42 upper arms · 40+40 legs · 38 hair · 38+38 lower arms · 36+36 hands · 28 head coverings · 21+21 shoulder attach · 18 facial hair · 17 eyebrow · 15 back attach · 13 helmet attach · 12 hips attach · 11+11 knee · 6+6 elbow · 3 ear · + 20 shields | heroic-fantasy register; combinatorially unbounded |
| `SidekickCharacters` | `SK_HUMN_BASE_01` (22 base slots) + `SK_FANT_KNGT_17` (23-slot knight armour set) | the Sidekick modular system; the base-locomotion clips on disk are authored **for this rig** |

These are the honest answer to "how far could augmentation go if we committed to it" — the ceiling
is effectively unbounded. They are also **unproven in this repo**, on a different assembly
paradigm from `mob_rig.gd`, and adopting either is its own cell of work. Recorded, not counted.

---

## 2 · COUNTS BY PACK

Classification rule, stated once and applied uniformly:

- **(a) enemy-type outright** — monstrous / undead / demonic, **OR** an armed-and-armoured combatant
  that already reads hostile in a dark register (Matt's brief names "knights-as-hostiles"
  explicitly).
- **(b) conscriptable** — humanoid civilian/neutral whose silhouette works but which needs armour,
  a weapon, or a palette to read hostile.
- **(c) out-of-register** — modern / sci-fi / cartoon-bright / anthropomorphic-cute / wrong
  proportion. Cannot wear the Crucible register without fighting it.

### Tier-1 — core dark-fantasy register (no argument needed)

| pack | bodies | (a) enemy | (b) consc. | (c) out | per-body SK export? | notes |
|---|---|---|---|---|---|---|
| `polygon-dark-fantasy` | 15 | **15** | 0 | 0 | YES (`Unreal_Characters/`) | **the register anchor.** 5 of the 6 current dresses come from here |
| `polygon-dungeon` | 16 | **16** | 0 | 0 | YES | ghosts · goblins ×6 · rock golem · skeletons ×4 · tormented soul · 2 knights |
| `polygon-dark-fortress` | 13 | **13** | 0 | 0 | combined only | apothecary · barbarian · behemoth · colossus · corpse · inquisitor · knight · necromancer · plague · plague lord · undead ×2 · wraith |
| `polygon-fantasy-rivals-pack` | 20 | **20** | 0 | 0 | YES | giants/golems/trolls/demons. **⚑ Big-Rig skeleton risk — see § 3.3** |
| `polygon-goblin-war-camp` | 15 | **11** | 4 | 0 | combined only | cook + 3 prisoners are the conscriptables |
| `polygon-dungeon-realms` | 21 | **7** | 14 | 0 | combined only | demon · skeletons ×3 · undead knight · dwarf soldiers ×2 |
| `polygon-boss-zombies` | 4 | **4** | 0 | 0 | YES | blobber · brute · slobber · wretch |
| `polygon-werewolf` | 2 | **2** | 0 | 0 | YES | werewolf · undead werewolf |
| **Tier-1 subtotal** | **106** | **88** | **18** | **0** | | |

### Tier-2 — in-genre, needs a per-pack register argument (palette / kit), not a per-body one

| pack | bodies | (a) enemy | (b) consc. | (c) out | per-body SK? | register caveat |
|---|---|---|---|---|---|---|
| `polygon-samurai-empire` | 13 | 8 | 5 | 0 | combined only | East-Asian armour silhouette is legible but culturally distinct; tengu is a clean monster |
| `polygon-fantasy-kingdom-pack` | 21 | 6 | 14 | 1 (fairy) | YES | brighter authored palette |
| `polygon-ancient-egypt` | 13 | 6 | 7 | 0 | combined only | 3 mummies are outright; palette is sun-bleached, wants a dark alt |
| `polygon-viking-realm` | 10 | 6 | 4 | 0 | combined only | reads well dark |
| `polygon-fantasy-characters` | 12 | 5 | 7 | 0 | YES | witch/sorcerer/wizard/druid/rogue = cultist casters |
| `polygon-elven-realm` | 11 | 4 | 7 | 0 | YES | knight/soldiers/rogue; dark-elf read needs a palette |
| `polygon-samurai-pack` | 8 | 4 | 4 | 0 | YES | **heavy role-overlap with samurai-empire** — do not double-count as variety |
| `polygon-ancient-empire` | 11 | 3 | 8 | 0 | YES | captain + 2 soldiers |
| `polygon-pirate-pack` | 14 | 3 | 11 | 0 | YES | **3 skeletons are Tier-1-grade.** Tricorns + flintlocks break the register on the other 11 |
| `polygon-adventure-pack` | 5 | 3 | 2 | 0 | YES | knight · warrior · viking |
| `polygon-farm-pack` | 6 | 1 | 5 | 0 | YES | **scarecrow is an excellent Crucible body** |
| `polygon-explorer-kit` | 2 | 0 | 2 | 0 | YES | |
| **Tier-2 subtotal** | **126** | **49** | **76** | **1** | | |

### Tier-3 — out of register

| pack | bodies | why |
|---|---|---|
| `polygon-mini-fantasy-characters` | 60 | **chibi proportion.** Cannot mix with full-proportion bodies at any camera. Usable only as a complete standalone alternate register, all-60-or-none |
| `polygon-fantasy-village` | 26 | 16 anthropomorphic cute animals + 10 cozy villagers; deliberately bright. The 10 villagers are borderline-conscriptable if the pack palette is overridden |
| `polygon-western-frontier-pack` | 21 | Old West. ~8 (bandit, thugs ×2, native warriors ×5) are borderline, but hats + firearms break the silhouette read |
| `polygon-simple-people` | 18 | modern |
| `polygon-city-characters-pack` | 17 | modern |
| `polygon-town-pack` | 9 | modern |
| **Tier-3 subtotal** | **151** | |

### TOTALS

| | bodies |
|---|---|
| (a) enemy-type outright | **137** (Tier-1 **88** + Tier-2 **49**) |
| (b) conscriptable | **94** |
| (c) out-of-register | **152** |
| **all distinct bodies** | **383** |

*(383 = 106 + 126 + 151. The single Tier-2 out-of-register body is the fairy.)*

---

## 3 · WHAT IS ALREADY WIRED, AND WHAT A NEW BODY COSTS

### 3.1 · 16 bodies are already proven — not 6

`scenes/rigs/mobs/` holds **18 rig scenes over 16 distinct bodies** (`SK_Chr_Werewolf_01` is used
twice), drawn from four packs — dark-fantasy 7, dungeon 4, boss-zombies 3, werewolf 2. Each is a
body that imports, retargets, scales, textures and plays the base-locomotion clips **today**.

**The 6 in the CP-A still-set is a dress decision, not an asset ceiling.** I chose 6 because the
wire makes exactly 6 distinctions about what a body IS (the `record_path` pool split). The asset
tree was never the constraint, and my A1b note should not be read as claiming it was.

### 3.2 · The augmentation surface is already parameterised

`scripts/mob_rig.gd` exposes exactly the axes Matt is proposing, as `@export` vars:

| export | axis |
|---|---|
| `body_fbx` | base body |
| `target_height` | **scale** |
| `body_tex` | **palette** (single-atlas `material_override`) |
| `hand_prop_fbx` + `prop_tex` | **attachment** (one `BoneAttachment3D` on `RightHand`) |

Bodies are retargeted to Godot's `GeneralSkeleton` via the `sidekick_bone_map` import subresource,
and the base-locomotion clips are humanoid-profile bound — they **"bind onto any retargeted body by
bone name."** That is why the usable pool is large: it is not per-body animation authoring.

### 3.3 · The two real per-body costs

**Cost A — combined-FBX packs.** dark-fortress (13), goblin-war-camp (15), dungeon-realms (21),
viking-realm (10), ancient-egypt (13), samurai-empire (13) = **85 bodies** ship no per-body export.
`mob_rig.gd` takes a whole-FBX path and would need a `keep_mesh` name parameter.
**This pattern is already proven in-repo** — `scripts/build_ravine_carved.gd` does exactly this
(`GOBLIN_KEEP_MESH := "SM_Chr_Warrior_Male_01"`), and `scripts/apply_hero_retarget.py` already
retargets the combined goblin FBX to `GeneralSkeleton`. So this is one bounded change to
`mob_rig.gd`, not a per-body pipeline.

**Cost B — Big-Rig skeleton divergence. ⚑ UNVERIFIED BY ME.** Measured, not assumed:
`CharactersBR.fbx` carries **65 LimbNodes**; `SK_Chr_Skeleton_01.fbx` carries **55**. Different
skeletons. The 20 `polygon-fantasy-rivals-pack` bodies (giants, golems, trolls) are BR-class and
**may not bind the base-locomotion clips**. I did not test a retarget — this census is
reconnaissance, and asserting a retarget I did not run would be the same error jack-ryan caught in
JR-A1a-2. Corroborating evidence that this is a known seam: a second animation pack
(`anim-goblin-locomotion`, `A_MOD_GBL_*` / `A_POLY_GBL_*`) exists on disk precisely for the
non-standard bodies, and `scripts/probe_rig_matrix.gd` exists to probe bone-sets. **Treat 20 of
the 137 as at-risk until a retarget is run.** Conservative enemy-type count if all 20 fail: **117**.

---

## 4 · AUGMENTATION MATH — HONEST MULTIPLIERS AT GAMEPLAY-CAMERA DISTANCE

**Framing:** galadriel R2 framing — Crucible-ish top-down / three-quarter camera, not close-up.
**Distinctness criterion (GL-16, judge at watch distance):** two variants count as distinct only if
**silhouette OR palette is separable at watch distance**. Face detail, texture detail, weapon
type-within-class, and sub-10 % scale differences are all **below** the threshold and score 0.

### (i) Armour / attachment swaps

**Measured inventory:** 141 weapon meshes and **201 `SM_Chr_Attach_*` meshes** across the six
in-register packs alone (dark-fantasy 31 · dark-fortress 21 · goblin-war-camp 41 · dungeon-realms
70 · viking-realm 38 · dungeon 0).

**Honest multiplier is NOT 201.** At watch distance a held weapon collapses into ~4 readable
silhouette classes, not 24: *unarmed · one-hand · big-two-hander/polearm · ranged/bow · staff*.
Sword-versus-axe is invisible. With today's single `RightHand` socket:

> **×3 today** (unarmed / one-hand / large-two-hand-or-polearm). Bow and staff are real but overlap
> the one-hand read from behind and above.

Adding a **head socket** is the single highest-value change available, and it is a small one — a
`BoneAttachment3D` on `Head`, exactly the pattern `hand_r` already uses. Silhouette above the
shoulders (bare skull / hood / horned helm / crown) is the most legible watch-distance cue there is,
and 201 attachments are sitting on disk unused.

> **×6 with a head socket added** (3 hand states × 2 head states).

### (ii) Palette / tint

**Measured, not assumed:** `PolygonDarkFantasy_Texture_01_A/B/C.png` are all **4096×4096**, same
atlas layout, three authored colourways. Same for `PolygonDarkFortress_*` and
`PolygonGoblinWarCamp_*` (12 atlases each = 4 atlas families × 3 colourways). Character meshes are
UV'd for atlas **01**, so the usable set per character is **01_A / 01_B / 01_C**.

> **×3 from authored atlas alts.** Free, zero risk, already the exact mechanism `body_tex` uses.

**⚑ Hard constraint, learned the expensive way.** Cross-pack atlas application is **UV-invalid** —
this is the "rainbow plinth" defect recorded in my A1b landing note § 5: the DarkFortress alts atlas
forced onto a mesh UV'd for a different atlas came back painted with the palette *strip*. Palette
variants must stay **inside the body's own pack atlas family.**

Beyond the authored alts, a per-instance albedo modulate is available. But a tint on a Synty atlas
shifts **every** colour band including skin and bone, so it reads as "recolour" rather than "different
enemy." I would spend at most one disciplined faction hue before it becomes visible padding:

> **×3 honest · ×6 aggressive (and the aggressive half looks cheap).**

### (iii) Scale steps — ⚑ THE AXIS IS ALREADY SPENT

Matt asked me to flag this and it deserves the loudest line in the section.

**Scale in this build already carries RANK.** My A1b row 6 set nemesis at **2.05 m** for exactly one
stated reason: so nemesis reads taller than boss at **1.85 m**. Trash is 1.70, hero 1.75, devotion
1.65, bounty 1.75. The height column *is* the tier ladder.

**A signal cannot carry two meanings.** If scale also encodes variety, then a 2.05 m body no longer
means "nemesis" — it means "some big one," and the rank read I built the ladder for is destroyed.

> **×1 for variety. Zero. The axis is not available.**

A ±5 % organic crowd jitter is fine and I would take it — but it is *deliberately* below the
distinctness threshold, so by construction it adds **0** distinct identities. It buys life, not
variety. Do not count it.

### Combined multiplier, with the de-rating stated

The axes are **not independent**: a bare-handed 01_B skeleton and a bare-handed 01_C skeleton are
separable, but weakly. Not every cell of the 3 × 3 grid is separable from every other cell.

| grammar | nominal | **honest, de-rated** |
|---|---|---|
| today (hand socket + authored alts, no scale) | 3 × 3 = ×9 | **×4 conservative · ×6 realistic** |
| + head socket (small, bounded change) | 6 × 3 = ×18 | **×8 conservative · ×10 realistic** |

---

## 5 · VERDICT vs THE THREE TARGETS

### 5.1 · The arithmetic

| path | distinct identities | vs 163 | vs 32 | vs 6 |
|---|---|---|---|---|
| today, shipped | **6** | 4 % | 19 % | — |
| **already-proven rigs, zero new work** | **16** | 10 % | 50 % | 2.7× |
| Tier-1 bodies, **no augmentation** | **88** | 54 % | **2.8×** | 15× |
| **all enemy-type bodies, no augmentation** | **137** | 84 % | **4.3×** | 23× |
| **137 enemy + 26 conscripted, no augmentation** | **163** | **100 %, 1:1** | 5.1× | 27× |
| Tier-1 88 × ×2 (one palette axis only) | **176** | **108 %** | 5.5× | 29× |
| Tier-1 88 × ×4…×6 (today's grammar) | **352 – 528** | 2.2× – 3.2× | 11× – 16× | — |
| all 137 × ×4…×6 | **548 – 822** | 3.4× – 5.0× | 17× – 26× | — |
| conservative floor (all 20 BR bodies fail) 117 × ×4 | **468** | 2.9× | 15× | — |

### 5.2 · The verdict

**All three targets are reachable. 163 is reachable WITHOUT augmentation at all.**

The premise of Matt's question — *"depending on the assessed count… it may make sense to look at
augmenting armour size/colour to fill out the remainder"* — assumed a shortfall. **There is no
shortfall.** 137 enemy-type bodies against 163 names is 84 % on base bodies alone, and the 94
conscriptables cover the last 26 twice over. The 32-body fallback floor is cleared **5.1×** by base
bodies and **2.8×** by Tier-1 alone.

**We did not fall short in Synty assets. We fell short in rigging throughput, and that is a
different problem with a different fix.**

### 5.3 · RECOMMENDATION, with the lean

**Lean: target 163 as the end state. Stage it in three steps. Do NOT spend the augmentation axes
yet — bank them.**

**Step 1 — 6 → 16, immediately, zero new asset work.** The 16 rigs in `scenes/rigs/mobs/` already
import, retarget, scale, texture and animate. Nothing needs to be built; the dresses need to be
*assigned*. This alone clears half the 32 floor and would visibly break the clone-army read that my
own CP-A framing sentence called out. Cheapest available win in the whole cell.

**Step 2 — 16 → 32+, from Tier-1 only.** 88 Tier-1 bodies are available; 72 are un-rigged. This
needs (a) the `keep_mesh` parameter on `mob_rig.gd` for the 85 combined-FBX bodies, and (b) a
per-body import + AABB height + atlas + smoke frame. Bounded, mechanical, no design conversation.
Meets Matt's stated minimum floor with pure register and no argument required.

**Step 3 — 163. Gated on the catalogue-side extraction, NOT on assets.**

> **Yes — the 163 target wants the parked elrond + legolas name→family extraction, and I would call
> it the actual blocker.**

The argument is the same one my A1b note already made, sharpened by this census. I deliberately
refused to use `archetype_tag` (167 distinct; the wire declares it *"GROUPS NOTHING"*) and
`display_name` (163 distinct) to pick bodies, because a name→body table is an extraction that does
not exist yet. **The census does not change that. It makes it urgent.**

With 6 dresses, a wrong body is invisible — everything is already generic. With 163 bodies assigned
**randomly** to 163 names, every mismatch becomes loud and specific: "Rotting Corpse" standing over
a pirate captain, "Bone Deacon" on a goblin cook. That is strictly worse than the honest clone
army, because it teaches the player that the visuals are **noise** — and once a player learns the
art does not mean anything, they stop reading it, and every body we add after that is wasted.

**163 distinct forms without the extraction is 163 distinct WRONG forms.** The extraction is what
turns an asset count into an identity system. Route it as the gate.

**On augmentation specifically — my recommendation is HOLD, and here is why it is not laziness.**

1. **We do not need it.** Base bodies reach 163 on their own. Augmentation was proposed to fill a
   gap that the census says does not exist.
2. **Spending an axis for variety burns it for meaning.** Palette is the natural carrier for
   **faction** or **affix/rare-tier** legibility — the thing an ARPG genuinely needs a player to read
   at a glance. If A/B/C is already consumed making three skeletons look like three skeletons, there
   is no palette left when we want "this one is a champion."
3. **Scale is already spent on rank** (§ 4 iii). Reusing it would break the 1.65/1.70/1.75/1.85/2.05
   ladder I built for exactly that read.
4. **Attachments are the exception, and I would take that one now.** The head socket is a small,
   bounded change against 201 unused meshes on disk, and it improves the *existing* 16 rigs
   immediately without waiting for anything upstream. That is the one augmentation I would spend.

**Summary lean, one sentence:** ship **16 now** for free, drive to **32+ from Tier-1** as bounded
mechanical work, add the **head socket** because it is cheap and it helps today, and hold **163**
behind the name→family extraction — because the assets are already there and the meaning is not.

---

## 6 · WHAT THIS CENSUS DOES NOT ESTABLISH

Stated plainly, so no downstream cell leans on something I did not measure.

1. **No retarget was run.** Every "usable" claim rests on the `GeneralSkeleton` retarget pattern
   working for bodies beyond the 16 already proven. Measured bone-count divergence (55 vs 65
   LimbNodes) says **it will not hold universally**. § 3.3 names the at-risk set (20 BR bodies).
2. **No body was rendered for this census.** Register classification in § 2 is judgment from mesh
   names, pack identity and the packs' authored palettes — not from frames at watch distance. GL-16
   says judge at watch distance; **I did not.** The Tier-1/Tier-2 split is the axis most likely to
   move under actual frames, and Tier-2 is where it will move.
3. **The multipliers in § 4 are estimates, not measurements.** No A/B still-set was captured to test
   whether a 01_B skeleton is separable from a 01_C skeleton at the R2 camera. The honest way to
   settle it is a galadriel-side distinctness lap — a small still-set at gameplay framing — and I
   would rather that number came from her pipeline than from my estimate.
4. **The 163 target is name-count fidelity, not correctness.** This census counts *forms available*.
   It says nothing about which form belongs to which name. That is § 5.3's gate, and it is upstream
   of me.

---

**Ledger disposition:** R-CPA-2 answered. **R-CPA-1 (keep the six dresses) is unaffected** — the six
remain the honest read of what the *wire* distinguishes. Everything above is about what the *asset
tree* could distinguish if a producer-side species/family carrier ever lands.

**Veto-open.** Every number carries its basis; every judgment call is labelled as one.
