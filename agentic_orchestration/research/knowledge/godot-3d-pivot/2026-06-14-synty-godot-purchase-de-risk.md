# Research — Synty Godot Purchase De-Risk — 2026-06-14

**Mode:** A (analytical)
**Commissioner:** Matt (direct)
**Sources consulted:** syntystore.com product pages, Unity Asset Store listings, GitHub godotengine/godot issues and PRs, jgillich itch.io Sidekick Creator plugin, FleMo93 GitHub plugin, Flynsarmy GitHub import scripts, Godot forum threads, Godot Engine official release notes, Synty EULA pages
**Scope:** Narrow purchase-decision de-risk. Five questions only. No ecosystem-level synthesis.

---

## Q1 — EXACT PRODUCT ID

### What "Synty Sidekick" is

"Sidekick" is Synty's **current-generation modular character system**, launched around 2023-2024 as the successor to the older POLYGON Modular Fantasy Hero. It is NOT one product — it is a **product line**: a series of themed packs that all plug into a shared character-creator tool and a common underlying rig. Each pack is a separate SKU.

**Key distinction from older products:**
- **Sidekick packs** — newer generation, higher-fidelity, include body blend shapes, facial blend shapes (ARKit-compatible), and are designed to cross-mix across themes. These are the packs Synty is actively expanding.
- **POLYGON - Modular Fantasy Hero Characters** — older product, $149.99, now listed as "Sold out" on the Synty store. Human fantasy heroes only (720 parts, male/female). **Explicitly NOT compatible with Sidekick packs** per Synty FAQ: "POLYGON Fantasy Hero Modular Characters are not compatible with Sidekicks." Separate product family. Source: [Synty FAQ](https://syntystore.com/community/faq).
- **POLYGON series (non-modular)** — the large catalogue of low-poly environment, prop, and character packs (POLYGON Dungeon, POLYGON Adventure, etc.). These are pre-built characters rigged to Mecanim, not a modular system. Different product family entirely.

### Relevant Sidekick SKUs for this project

All individual Sidekick packs are **$199.99 USD** unless otherwise noted. Source: [Sidekick Collection](https://syntystore.com/collections/sidekick-character-packs).

**Player character (humanoid):**
- **Fantasy Knights — Sidekick Modular Characters** ($199.99) — heavy armor parts for human characters. Fully rigged to Unity Humanoid (Mecanim compatible), Unreal Engine Mannequin compatible. Source: [Fantasy Knights page](https://syntystore.com/products/fantasy-knights-sidekick-modular-character-pack).
- **Elven Warriors — Sidekick Modular Characters** ($199.99) — similar human-rig elven parts.
- **Fantasy Villagers — Sidekick Modular Characters** ($199.99) — civilian/NPC human parts.
- **FREE Starter Pack** ($0) — 90+ human base species parts + 50+ Sci-fi Civilian / Fantasy Knights parts. Same humanoid rig as paid packs. Source: [Starter Pack](https://syntystore.com/products/sidekick-modular-characters-starter-pack). **This is available for immediate download to test the pipeline before spending money.**

**Bipedal monster (goblin/skeleton):**
- **Goblin Fighters — Sidekick Modular Characters** ($199.99) — 427 parts total (330 armor/weapon parts + 97 goblin base species parts). Source: [Goblin Fighters page](https://syntystore.com/products/goblin-fighters-sidekick-modular-characters).
- **Fantasy Skeletons — Sidekick Modular Characters** ($199.99) — 100+ parts including skeleton body, armor, and attachment pieces. Source: [Fantasy Skeletons page](https://syntystore.com/products/fantasy-skeletons-sidekick-modular-characters).

**What the store does NOT have (as of June 2026):** No orc-specific or kobold-specific Sidekick pack. The POLYGON (non-Sidekick) series has POLYGON Goblin War Camp and POLYGON Dungeon Realms with Mecanim goblins, but those are non-modular pre-built characters, not part-swappable Sidekick format.

### CRITICAL — Do goblin Sidekick creatures share the humanoid skeleton?

**Finding: YES, with nuance.** Both Goblin Fighters and Fantasy Skeletons are described as "Fully rigged to the Unity Humanoid skeleton (Mecanim compatible)" — the same standard as the human Sidekick packs (Fantasy Knights, Elven Warriors, etc.). Source: [Goblin Fighters page](https://syntystore.com/products/goblin-fighters-sidekick-modular-characters), [Fantasy Skeletons page](https://syntystore.com/products/fantasy-skeletons-sidekick-modular-characters).

**Nuance that limits the "scope win":** Synty's Goblin Locomotion animation pack ships with **"Sidekick-specific versions" as separate files** alongside POLYGON versions, suggesting Synty treats goblin animation as a distinct variant even within the Sidekick line. Source: [Goblin Locomotion Pack](https://syntystore.com/products/animation-goblin-locomotion). Additionally, Synty's FAQ states that "specific parts are locked to work with a specific species" — a human helmet will not fit on a goblin head, even though both are on the humanoid rig. Cross-pack mixing at the species level is constrained.

**Bottom line on goblins:** Goblin Fighters uses the standard Unity Humanoid skeleton. In theory, Mecanim-targeted humanoid animations can be retargeted to goblins. In practice, Synty provides separate goblin-specific animation files, implying the proportional differences matter enough to warrant them. The animation set is shared-architecture but not drop-in identical.

---

## Q2 — GODOT CONVERSION TRACK RECORD

This is the load-bearing question. Summary upfront: **documented conversion evidence exists**, but it is for **Sidekick characters in general** via a community plugin, NOT a published end-to-end account of runtime part-swap fully working at scale. The evidence is partial but meaningfully positive.

### Evidence 1 — jgillich "Sidekick Creator" Godot plugin (itch.io)

A community-authored, standalone Godot plugin called **Sidekick Creator** exists at [jgillich.itch.io/sidekick-creator](https://jgillich.itch.io/sidekick-creator). Key facts:
- Targets: Synty Sidekick packs (requires a valid Sidekicks license from Synty)
- Purpose: replicates the Unity Sidekick Character Creator workflow inside Godot, supporting parts selection, colors, presets, and body shapes
- The plugin **automatically sets up a bone map for all Sidekick skeletons** — this is the critical plumbing step that would otherwise need manual work per-import
- License: Mozilla Public License 2.0 (open source)
- Price: name-your-own-price (free available)
- Last documented changelog entry: 2025-05-03 (blend rig movement, default texture, root config option) — actively maintained as of that date
- **Known limitation:** "Attachment re-positioning for blend shapes is not fully implemented"
- **Known setup friction:** requires a separate SQLite plugin from the Godot asset library; some users report empty character creator options on first setup
- Runtime part-swap: the plugin enables parts selection at the Godot editor level; full runtime (in-game) part-swap is not explicitly confirmed in the documentation, and "attachment re-positioning for blend shapes is not fully implemented" suggests the runtime surface is incomplete

**Assessment:** This is the strongest documented path for Sidekick→Godot. It is community-maintained, not Synty-official. It proves the conversion is possible and that bone mapping works. It does not confirm full runtime part-swap in a shipping context.

### Evidence 2 — FleMo93 Blender→Godot plugin (GitHub)

[github.com/FleMo93/blender-synty-characters-to-godot](https://github.com/FleMo93/blender-synty-characters-to-godot) is a Blender addon that converts Synty character FBX files to glTF for Godot import, performing cleanup on pose and armature. This targets the **older Synty character workflows** (FBX-based, pre-Sidekick or POLYGON Modular Fantasy Hero), NOT specifically the Sidekick line. There is a companion YouTube tutorial ([youtube.com/watch?v=nasSGwC6ef4](https://www.youtube.com/watch?v=nasSGwC6ef4)) titled "Importing Synty Modular Fantasy Heroes into Godot 4" — this covers the **POLYGON Modular Fantasy Hero** pack (the older, now sold-out product), not Sidekick. The video content itself was not extractable via WebFetch, so pipeline details are not confirmed from that source directly.

**Assessment:** FleMo93's tool is for the older POLYGON Modular Fantasy Hero line. It may inform a Sidekick workflow but is not directly applicable.

### Evidence 3 — Flynsarmy Godot import scripts (GitHub)

[github.com/Flynsarmy/gd-synty-fantasy-heroes-import-scripts](https://github.com/Flynsarmy/gd-synty-fantasy-heroes-import-scripts) — GDScript + Python scripts for importing the POLYGON Modular Fantasy Hero pack into Godot. Same caveat as above: targets the older Fantasy Hero product, CC0 licensed, 3 commits total, one open issue. Not Sidekick-specific.

**Assessment:** Confirms the Modular Fantasy Hero line has been imported into Godot (someone built scripts for it). No runtime part-swap confirmation, no Godot version specified.

### Evidence 4 — Facebook Godot group post

One post in the Godot Engine Facebook group ([facebook.com/groups/godotengine/posts/3475451452591424/](https://www.facebook.com/groups/godotengine/posts/3475451452591424/)) reports successfully incorporating "the Synty modular hero pack," cycling between meshes for each piece, with texture variations working. The product name ("modular hero") is ambiguous — could be POLYGON Modular Fantasy Hero or Sidekick. The post was truncated and no Godot version is confirmed. No pipeline details.

**Assessment:** Weak evidence — confirms someone got modular mesh cycling working in Godot, but product identity and method are not confirmed.

### Evidence 5 — Godot forum thread (September 2025)

A Godot forum post from September 2025 ([forum.godotengine.org/t/how-should-i-import-synty-assets-according-to-following-hints/123677](https://forum.godotengine.org/t/how-should-i-import-synty-assets-according-to-following-hints/123677)) discusses importing Synty POLYGON_NatureBiomes assets in Godot 4.5, with texture-matching friction. Not character-specific, not Sidekick-specific. Shows general Synty→Godot workflow activity as of late 2025.

### What is NOT documented

No publicly available forum post, blog post, video, or GitHub repo provides an end-to-end, step-by-step account of:
1. Importing Synty **Sidekick** characters into Godot 4.x
2. Getting **runtime multi-mesh part-swap** (swapping heads/armor/weapons on a shared skeleton mid-game, not just in the editor)
3. Confirming the full workflow on a specific Godot version
4. Doing this with **creature packs** (Goblin Fighters or Fantasy Skeletons)

The jgillich Sidekick Creator plugin is the closest thing, but it addresses editor-time character building rather than confirmed runtime swap in shipping code.

**This absence is a load-bearing finding.** The conversion is not zero-evidence (the plugin exists), but it has not been publicly demonstrated as a complete, working runtime part-swap pipeline by any third party. The friction in Q3 (bone renaming bug) is likely why: 4.3 and 4.4 had a significant skeleton import regression, which would have deterred published tutorials.

---

## Q3 — GODOT VERSION

### Bug #106073 — bone renaming breaking modular skeleton imports

**What it is:** Since Godot 4.3, the GLB/glTF model importer renamed duplicate skeleton bones scene-wide (appending `_2`, `_3`, etc.) even across multiple distinct skeletons in a single file. For modular character systems like Synty Sidekick where multiple body-part meshes share bone names (e.g., "Eyebrows" appears on multiple skeleton instances), this silently corrupted bone maps and broke animation retargeting. Source: [GitHub Issue #106073](https://github.com/godotengine/godot/issues/106073).

**Affected versions:** Godot 4.3.0 through 4.4.1. Godot 4.2.2 was the last version without this regression.

**The fix — PR #106537:** [github.com/godotengine/godot/pull/106537](https://github.com/godotengine/godot/pull/106537) — titled "GLTF: Make skeleton bone names unique per-skeleton instead of scene-wide." This restores Godot 4.2 behavior: bone uniqueness is enforced within each skeleton, not across the entire scene. Merged into `godotengine/godot:master` on **June 10, 2025**. Assigned to the Godot **4.5 milestone** and confirmed released in 4.5.

### Godot release timeline

| Version | Release Date | Relevant Status |
|---|---|---|
| 4.2.2 | (stable prior to 4.3) | Last clean version before bug 106073 |
| 4.3.0 – 4.4.1 | 2024–early 2025 | Bug 106073 active; do not use for Synty modular |
| 4.5.0 | September 15, 2025 | Bug fix merged; skeleton import regression resolved |
| 4.5.1 | October 20, 2025 | Maintenance release |
| 4.6.0 | January 2026 | Feature release; Jolt physics default, new IK system |
| 4.6.3 | May 20, 2026 | Current stable; recommended for adoption |

Sources: [Godot 4.5 release info](https://supermatrix.studio/news/godot-latest-release-stable), [Godot 4.6 release notes](https://godotengine.org/releases/4.6/), [Godot 4.6.3 stable release](https://github.com/godotengine/godot/releases/tag/4.6.3-stable).

### What version to use

**Recommendation based on the evidence:**

- **4.2.2 is NO LONGER the safest pin.** It was the workaround before PR #106537 landed. The fix is in 4.5+ and 4.5 is stable. Pinning to 4.2.2 means foregoing a year of engine improvements for a bug that is now fixed upstream.
- **4.3 and 4.4 are actively dangerous** for Sidekick-style multi-skeleton imports. Avoid.
- **4.5.x or 4.6.x are the rational targets.** The bone-renaming regression is fixed in both. 4.6.3 is the current stable as of June 2026 and includes additional IK and skeleton modifier improvements that are directly useful for an ARPG character pipeline.
- **No documented community consensus** on 4.5 vs 4.6 for Synty Sidekick imports specifically (because the Sidekick→Godot pipeline is not yet widely documented). The jgillich Sidekick Creator plugin references Godot 4.6 compatibility in user comments, suggesting it is tested there.

**Version recommendation: Godot 4.6.3.** It is current stable, includes the bug fix, and the Sidekick Creator plugin has been tested on it per user reports.

---

## Q4 — LICENSE FOR SHIPPING

### Relevant clauses from Synty's One-Time Purchase License

Source: [Synty One-Time Purchase Licence](https://syntystore.com/pages/one-time-purchase-licence).

**Engine lock-in: none.** The license is explicitly "worldwide, and is not limited by game engine, OS, platform or device." You may use assets in Godot.

**Conversion permitted.** The license grants the right "to adapt the Asset for the purpose of doing any of the above" — including incorporating adapted assets into products. No clause restricts exporting from Unity into another format for use in Godot.

**Shipping converted assets in a commercial game: permitted.** The license allows you to "incorporate the Asset into Products produced under your direct control" and "publish, distribute, transmit, broadcast, communicate, show and play the Asset as incorporated into those Products." Shipping a rendered game containing Synty-derived geometry is covered.

**What is prohibited:**
- "You must not share the source files of any Assets outside your team" — you cannot put the converted FBX/GLB files on GitHub or distribute them to anyone outside your development team.
- You cannot "distribute our Assets as stock images or stock art (2D or 3D) or otherwise share them for re-use by third parties."
- You cannot resell edited assets.

**Purchase channel matters.** If you buy through the Unity Asset Store, Synty states "for legal reasons we cannot supply files to you when you have purchased from another store" — meaning you get Unity package files only and converting them is technically a derived workflow from a Unity-only delivery. To get source files (FBX) suitable for Godot conversion, **purchase directly from syntystore.com**, not from the Unity Asset Store. Source: [Synty FAQ](https://syntystore.com/community/faq).

**Summary:** Direct Synty store purchase → receive source FBX files → convert to GLB for Godot → ship in commercial game = permitted. Unity Asset Store purchase → source files not supplied → conversion workflow is murkier. Buy direct.

---

## Q5 — BOTTOM LINE

### What the evidence says

**Positive signals:**
- The jgillich Sidekick Creator plugin (Godot, MPL2, free) proves the Sidekick→Godot import path exists and that bone mapping works.
- Goblin Fighters Sidekick uses the standard Unity Humanoid skeleton — same architecture as human Sidekick packs. Not a separate non-humanoid rig.
- Godot 4.6.3 (current stable) contains the fix for bug #106073 — the skeleton bone-renaming regression that made 4.3/4.4 dangerous for this workflow is resolved.
- Synty's license explicitly permits engine conversion and commercial shipping when purchasing direct.
- The Free Starter Pack is available NOW at no cost to test the Godot import pipeline before committing money.

**Risk signals:**
- Runtime part-swap (swapping parts mid-game in actual gameplay code, not just editor-time character builder) has NOT been publicly documented as working end-to-end. The jgillich plugin handles editor-time character creation; what happens at game runtime is undocumented.
- The Sidekick Creator plugin has known gaps: "attachment re-positioning for blend shapes is not fully implemented."
- No quadruped or serpentine creature exists in the Sidekick product line at all. The Sidekick line is entirely bipedal humanoid.
- The only non-humanoid creature options from Synty are: (a) POLYGON Simple Forest Animals (wolves, bears — pre-built, non-modular, separate rig), or (b) POLYGON Fantasy Rivals "Big Rig" for massive monsters (custom large skeleton, NOT compatible with humanoid animations).
- Synty does not support Godot officially. The entire pipeline relies on community tooling.

### Purchase recommendation

**Godot version: 4.6.3** (current stable; bug #106073 fixed; Sidekick Creator plugin tested on 4.6 per user comments).

**Before spending money — free validation step:**
Download the **Free Starter Pack** from syntystore.com, install the jgillich Sidekick Creator plugin (free, itch.io), and attempt to build a character and fire a test animation in Godot 4.6.3. This costs $0 and resolves the highest-risk unknown (does the plugin actually work for your project's runtime part-swap requirement) before committing $150–200.

**If the free pipeline validates — recommended purchase for the vertical slice:**
- **Goblin Fighters — Sidekick Modular Characters** ($199.99, syntystore.com direct) — gives a bipedal goblin enemy with 427 modular parts on a humanoid rig. This covers player character (via human Sidekick packs in the Free Starter) + goblin monster in one $200 purchase. DO NOT buy Fantasy Knights separately unless the free starter's human parts prove insufficient — the starter already includes Fantasy Knights parts.
- Unity Asset Store purchase is NOT recommended — buy direct from syntystore.com to get source FBX files needed for Godot conversion.

**Non-bipedal / quadruped enemy (serpentine, wolf, etc.):**
This is a separate problem with no clean Synty Sidekick answer. Options:
1. **Kenney.nl** — CC0 3D asset packs include basic animal/creature meshes, no modular system, but free and Godot-friendly.
2. **POLYGON Simple Forest Animals** (Synty, available from their store) — wolves, bears, non-modular pre-built characters. Same POLYGON rig, not Sidekick. Would not share the modular character creator workflow.
3. Defer the non-bipedal enemy to a later sprint and scope the vertical slice to player + goblin only.

**High-friction flag:** The absence of any published end-to-end runtime-part-swap Sidekick→Godot pipeline is a documented gap, not an assertion of impossibility. The architecture (Unity Humanoid rig + bone map + Godot 4.6 skeleton fix + community plugin) supports it in principle. But if the vertical-slice goal requires runtime armor/weapon swapping mid-gameplay, budget meaningful spike time (estimate: 1–2 days) for the Godot plumbing before treating it as solved.

---

## Knowledge gaps not resolved

1. **Runtime part-swap in Godot shipping code.** No published account confirms Synty Sidekick parts swap at runtime (not editor-time) in a Godot 4.x game. This is the highest-value unknown.
2. **Goblin→human cross-species part compatibility in Godot.** Synty's FAQ says species-locked parts exist. Whether goblin bodies can wear human armor pieces (or vice versa) in the Godot plugin is not documented.
3. **jgillich plugin's last tested Godot version.** User comments reference 4.6 but the plugin page does not publish a formal compatibility matrix. Last changelog: 2025-05-03.
4. **FleMo93 Blender plugin current status and target product.** README is sparse; no confirmed Godot version; likely targets POLYGON Modular Fantasy Hero (older, sold-out), not Sidekick.
5. **Whether Goblin Fighters Sidekick source FBX structure is multi-skeleton (triggering bug #106073 in pre-4.5 engines).** Highly likely given the modular design, but not confirmed via teardown.

---

## Source list

- [Sidekick Collection — Synty Store](https://syntystore.com/collections/sidekick-character-packs)
- [Goblin Fighters — Sidekick Modular Characters](https://syntystore.com/products/goblin-fighters-sidekick-modular-characters)
- [Fantasy Skeletons — Sidekick Modular Characters](https://syntystore.com/products/fantasy-skeletons-sidekick-modular-characters)
- [Fantasy Knights — Sidekick Modular Characters](https://syntystore.com/products/fantasy-knights-sidekick-modular-character-pack)
- [Free Starter Pack — Sidekick Modular Characters](https://syntystore.com/products/sidekick-modular-characters-starter-pack)
- [POLYGON - Modular Fantasy Hero Characters](https://syntystore.com/products/polygon-modular-fantasy-hero-characters)
- [POLYGON Fantasy Rivals Pack](https://syntystore.com/products/polygon-fantasy-rivals-pack)
- [Goblin Locomotion Animation Pack — Synty](https://syntystore.com/products/animation-goblin-locomotion)
- [Synty FAQ — Godot support, cross-pack compatibility, license](https://syntystore.com/community/faq)
- [Synty One-Time Purchase Licence](https://syntystore.com/pages/one-time-purchase-licence)
- [Introducing Sidekick Character Creator — Synty Blog](https://syntystore.com/blogs/blog/introducing-sidekick-character-creator)
- [jgillich Sidekick Creator plugin for Godot (itch.io)](https://jgillich.itch.io/sidekick-creator)
- [FleMo93 blender-synty-characters-to-godot (GitHub)](https://github.com/FleMo93/blender-synty-characters-to-godot)
- [Flynsarmy gd-synty-fantasy-heroes-import-scripts (GitHub)](https://github.com/Flynsarmy/gd-synty-fantasy-heroes-import-scripts)
- [Godot Issue #106073 — skeleton bone renaming breaking multi-skeleton imports](https://github.com/godotengine/godot/issues/106073)
- [Godot PR #106537 — fix, merged June 10 2025, targeting 4.5](https://github.com/godotengine/godot/pull/106537)
- [Godot 4.6 release notes](https://godotengine.org/releases/4.6/)
- [Godot 4.6.3 stable release](https://github.com/godotengine/godot/releases/tag/4.6.3-stable)
- [Godot 4.5 release announcement](https://supermatrix.studio/news/godot-latest-release-stable)
- [Godot Engine Wikipedia — version timeline](https://en.wikipedia.org/wiki/Godot_(game_engine))
- [Godot Forum — Synty import thread Sept 2025](https://forum.godotengine.org/t/how-should-i-import-synty-assets-according-to-following-hints/123677)
- [Goblin Fighters on Unity Asset Store](https://assetstore.unity.com/packages/3d/characters/goblin-fighters-sidekick-modular-characters-by-synty-327375)
- [YouTube — Importing Synty Modular Fantasy Heroes into Godot 4](https://www.youtube.com/watch?v=nasSGwC6ef4)
