# How the Engine Names Things — A Family Reading Guide

**For Matt + son.** Companion to `character-loadouts.md`. Walks through the cascade of how the engine generates all the evocative names you see — anchor names, element flavors, class names, ability names, monster names, gear names — and how they all end up feeling like they belong together.

## Why this is interesting

When you read a class name like *"Trenchwind Pitch-Caster"* in season *"The Deep Trench"* and notice how every part of that season — classes, abilities, monsters, gear — uses words like *"trench"*, *"abyss"*, *"pitch"*, *"basalt"*, *"thrum"* — that's not a coincidence. The engine builds names in a deliberate **top-down cascade**, where each layer of names inherits context from the layers above it. That's how the seasonal feel stays coherent.

This document walks the cascade from the very top (the season anchor) down to the smallest detail (a single gear item's name).

## The cascade — top-down

Each layer feeds context to the layer below it. The LLM gets richer prompts as we descend.

```
   1. SEASON ANCHOR (curated)
        ↓
   2. SEASON ELEMENT FLAVORS (LLM, ~1 call)
        ↓
   3. ARCHETYPE CHOICE (engine, deterministic)
        ↓
   4. CLASS NAMES (LLM, ~10 calls)
        ↓
   5. SKILL NAMES (LLM, ~50 calls per season)
        ↓
   6. MONSTER NAMES + SKILLS (LLM, ~160 calls)
        ↓
   7. TRIAL BOSS + SKILLS (LLM, ~6 calls)
        ↓
   8. GEAR NAMES (template common/uncommon/rare, LLM epic/legendary, ~80 calls)
```

Each layer's output flows downstream as input context. The LLM never sees the player; it sees structured prompts that grow more specific as we descend.

---

## Layer 1 — Season anchor (curated)

**The starting point of every season.** An anchor is a hand-curated thematic concept — a place, building, or situation with strong atmosphere. Examples from your 5 seasons:

- *The Deep Trench* — "the place in the sea where light has never reached; what lives there has never seen"
- *The Crypt of the First Saint* — "a sealed crypt where the founding holy figure was entombed"
- *The Cathedral of Bone* — "the temple built entirely from the relics of saints"
- *The Throne Room of the Mad King* — "where a sovereign issues commands no one understands"
- *The Ghost Town of the Gold Strike* — "where a mining boom died fast, leaving everything behind"

These come from a **fixed library inside the engine** (in a config file). The engine doesn't generate them — humans wrote them. Each anchor has a category (cathedrals, ghost towns, etc.), tags, and a brief description.

When generating a new season, the engine picks an anchor based on what hasn't been used recently. That's why your 6 seasons all had different anchors (well, except 1005 and 1006 because of the parallel-run issue we fixed).

**The anchor is the gravitational center of the entire season.** Everything else cascades from it.

---

## Layer 2 — Season element flavors (LLM)

**One call per season.** The engine sends the anchor + currently-known element pool to the LLM and asks: *"For this season, what should fire/wind/water/earth be called? Suggest seasonal names that fit the anchor's atmosphere."*

The LLM responds with 4 thematic names (one per canonical element). These are short, evocative, and atmospheric. Examples from your seasons:

| Anchor | fire → | water → | wind → | earth → |
|---|---|---|---|---|
| The Deep Trench | **pitch** (black, viscous) | **brine** (salt, bitter) | **thrum** (deep, vibrating) | **basalt** (volcanic) |
| The Crypt of the First Saint | **wax** (burning, melting) | **tear** (held, sacred) | **exhalation** (final breath) | **marrow** (bone, deep) |
| The Cathedral of Bone | **torch** (handheld, bright) | **milk** (white, nurturing) | **breath** (vital, warm) | **bone** (white, hard) |
| The Throne Room of the Mad King | **char** (burnt, blackened) | **mercury** (mad, unstable) | **draft** (cold, lonely) | **throne** (cold, weighty) |
| The Ghost Town of the Gold Strike | **coal** (dirty, abandoned) | **slick** (oil-water) | **dust** (bone-dry, motes) | **gold** (precious, ruinous) |

The LLM also has access to the **persistent element pool** — every name proposed so far across all past seasons. This lets it avoid duplicates. Over 100+ seasons, the pool grows; cross-season variety stays high.

**These four names become the vocabulary the rest of the season is built on.** Every layer below this references them.

---

## Layer 3 — Archetype choice (engine, deterministic)

**No LLM calls here.** The engine picks 10–11 dimensional class profiles for the season:
- Each gets an `energy_type` (mana / rage / focus / combo / stamina)
- Each gets a `range_profile` (close / medium / long)
- Each gets a `role_orientation` (damage / control / hybrid)
- Each gets a `damage_type` (physical / fire / wind / water / earth / hybrid)
- Each gets a `dominant_element` (one of the season's 4 element flavors)

Plus 2 of the 11 are picked as **act-bosses** (intentional outliers — one undertuned, one overtuned).

This is all dimensional generation — the same Phase 1–3 work from the dimensional refactor. The engine isn't being creative here; it's combinatorially producing distinct dimensional profiles.

These profiles become the input prompt for the next layer.

---

## Layer 4 — Class names (LLM, ~10 calls per season)

**One call per class.** The LLM is given:
- The season's anchor name + description
- The 4 element flavor names
- The class's dimensional profile (archetype, dominant_element, role, range)
- A request: *"Name this class evocatively. Use the anchor's atmosphere and the seasonal element name."*

The LLM then produces evocative names like:
- *"Trenchwind Pitch-Caster"* (fire mage, pitch-element, in the Deep Trench)
- *"Drowned Torch Keeper"* (fire mage, torch-element, in the Cathedral of Bone)
- *"Char-Crowned Usurper"* (fire mage, char-element, in the Mad King's Throne Room)

Notice how the SAME archetype (fire mage) gets completely different names across seasons because the anchor + element flavor differ. The dimensional profile is consistent; the *flavor* shifts with context.

The LLM also writes **flavor text** for each class — a paragraph capturing who they are and why they're in that season. That's the "atmospheric prose" you saw in the character-loadouts doc. It's not used mechanically; it's just there to make the class feel like a real character.

---

## Layer 5 — Skill names (LLM, ~5 per class × 10 classes = ~50 per season)

**One call per skill.** The LLM is given:
- The class's name + flavor text
- The skill's geometry + element + role (mechanically generated by the engine)
- A request: *"Name this skill, fitting the class's identity and the season's vocabulary."*

This produces ability names like:
- *"Trench Pitch Ignition"* (Trenchwind Pitch-Caster's burst-damage skill)
- *"Drowned Torch Vigil"* (Drowned Torch Keeper's defensive skill)

The skill names cascade down from the class identity — same as how the class names cascade down from the season identity.

**Known limitation:** the skill-naming prompt currently doesn't see the *other skills already named for this same class*, so a class can end up with duplicate skill names (e.g., "Trench Pitch Ignition" appearing 3× in one class's kit). This is in the polish backlog — fixing it is just adding a "previously-named skills for this class" deduplication context to the LLM call.

---

## Layer 6 — Monster names + their skills (LLM, ~160 calls per season)

**One call per monster (~40 per season) + ~3 calls per monster's skills.** Same pattern as classes:
- LLM gets anchor + element flavors + monster's tier + dimensional profile
- Produces names like *"Pitch Trench Crusher"* (trash-tier earth monster), *"Basalt Thrumcolossus"* (boss-tier wind monster), *"Drowned Doorkeeper"* (water_controller act-boss-equivalent)
- Each monster's skills then get named with similar prompts

Monsters are tiered (trash → standard → elite → mini-boss → boss). Higher-tier monsters tend to get more dramatic names ("Sovereign", "Colossus", "Wraith") while trash monsters get simpler names ("Crusher", "Sniper", "Caller").

**This is the bulk of LLM calls per season** — 40 monsters + 120 monster skills = ~160 calls, more than half of every season's LLM volume.

---

## Layer 7 — Trial boss + their skills (LLM, ~6 calls per season)

**The season's signature boss encounter.** Lower volume but higher stakes — the trial boss is the season's most identity-rich opponent.

Examples from your seasons:
- Season 001003 trial: *"Milkblood Penitent"* (water-themed, fits Cathedral of Bone)
- Season 001005 trial: *"Slickwater Claim Wraith"* (water-themed, fits Gold Strike Ghost Town)

The trial boss has 4–5 skills (vs ~3 for regular monsters), often phase-gated for dramatic difficulty curves.

---

## Layer 8 — Gear names (template + LLM, ~80 calls per season)

**This layer has TWO different naming approaches** depending on tier:

### Template-named (no LLM cost): common, uncommon, rare

These are the bulk of gear (~120 of 200 items per season). Names follow a fixed template:

- **Common:** `<Material> <SlotType>` — e.g., *"Iron Sword"*, *"Linen Hood"*
- **Uncommon:** `<Adjective> <Material> <SlotType> of <Element>` — e.g., *"Sturdy Iron Sword of Pitch"*, *"Polished Steel Hood of Brine"*
- **Rare:** Same template but with a richer adjective list (Heirloom, Master-Forged, Renowned, Etched, etc.) — e.g., *"Heirloom Steel Sword of Pitch"*

Template naming is **deterministic from the season's seed** — same items, same names, every time. No LLM cost.

### LLM-named: epic and legendary (~80 calls per season)

These are the special items — 80 of 200 per season. Each gets one consolidated LLM call producing:
- A unique name
- Evocative flavor text
- A visual prompt (for future Meshy/AI-art pipelines)
- For legendaries only: a `color_signature` hex code

The LLM gets:
- The gear's tier, base type (sword/staff/etc.), element flavor
- The season's anchor + element vocabulary
- A color label from the engine's color spectrum
- A summary of the gear's mechanical content (what it does)

This produces epic/legendary names like:
- *"Thrumming Trench Caller"* (legendary weapon, season 001001)
- *"Pitchthrum Abyssal Orb"* (epic off-hand, season 001001)
- *"Breath of Sainted Marrow"* (legendary weapon, season 001003)

**Why split tiers between template and LLM?** Template names parse fast (good for high-volume keep/vendor decisions on rare drops). LLM names are evocative (good for the epic+ items players actually remember). Mixing them keeps cognitive load manageable while preserving the "this is special" signal at the top tiers.

---

## Why the cascade produces coherence

Each layer inherits its parent's vocabulary. The result: a season feels like it was *written by one author*, even though it's hundreds of LLM calls each making local decisions. Specifically:

1. **The anchor sets atmosphere.** "The Deep Trench" gives a darkness/water/pressure mood.
2. **Element flavors translate atmosphere to vocabulary.** Pitch, brine, thrum, basalt — these become the words the season speaks in.
3. **Classes inherit vocabulary.** A fire mage becomes a *"Pitch-Caster"*, a water controller becomes a *"Tidecaller"*.
4. **Skills inherit class identity.** A Pitch-Caster's abilities use "Pitch", "Trench", "Trenchwind" — words that belong to its class.
5. **Monsters inherit anchor + tier weight.** Trash monsters get punchy short names; bosses get dramatic ones — but all use the season's vocabulary.
6. **Gear inherits everything.** A legendary in season 001001 is named with the same words as the classes who carry it. *"Thrumming Trench Caller"* could only exist in this season.

The cascade is what makes a season feel like a single coherent place rather than a procedurally-generated content blob. Each LLM call is small (cheap, fast), but the structured context-passing ensures all decisions land in the same imaginative space.

---

## Cost summary for naming, per season

| Layer | LLM calls | ~Cost |
|---|---|---|
| Element flavors | 1 | $0.01 |
| Class names | ~10 | $0.04 |
| Skill names | ~50 | $0.04 |
| Monster names | ~40 | $0.02 |
| Monster skill names | ~120 | $0.06 |
| Trial naming (boss + skills) | ~6 | $0.01 |
| Gear naming (epic + legendary) | ~80 | $0.04 |
| **Total** | **~307 calls** | **~$0.85 per season** |

Roughly $1 per season for naming. Empirically verified across the 5 generated seasons.

---

## What's NOT named by LLM

These are deterministic / fixed:
- The anchor itself (curated library, picked by selection logic)
- All gear at common / uncommon / rare tiers (templated)
- Mechanical fields like `geometry_type`, `range_profile`, `damage_type` (categorical, no naming needed)
- Engine-internal IDs (`class_0001`, `monster_0023`, `skill_0156`)

So roughly **5%** of the engine's output is template-or-fixed; **95%** flows through the LLM cascade. The LLM is the engine's "creative director" — but operating on a tightly-structured input that constrains it to coherent output.

---

## Cross-references

If you want to dig deeper on specific aspects:
- **`design_context.md`** in each season export — the dimensional vocabulary glossary (energy types, range profiles, etc.)
- **`character-loadouts.md`** (this folder) — the family-review document showing all 53 classes
- **`canonical/19-llm-call-map.md`** — the technical engine-side reference for where LLM calls happen
- **`canonical/17-gear-and-spirit-guide-design.md`** § "Tier gradient" + § "Affix coherence" — gear-specific naming + affix rules
- **`engine-repo/src/reincarnated/llm/naming.py`** — the actual code that builds these prompts and calls the LLM
