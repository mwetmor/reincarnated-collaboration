# Research — Unity VFX packs, cross-engine licensing, and Unity→Godot translation feasibility

**Date:** 2026-07-31
**Mode:** A (analytical) — VFX-SCOUT read-only cell of run BR-1
**Conductor:** gandalf (RUN-CONDUCTOR)
**Charter context:** Scope 28, `agentic_orchestration/gandalf/notes/2026-07-30-ambient-refit-fold-in.md` (Matt ruling 2026-07-31)
**Prior art:** `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/synthesis.md` — this run **closes three of its named gaps** (verbatim EULA text; Shuriken-vs-VFX-Graph pipeline per pack; Godot-native depth measured rather than estimated) and **corrects one finding**.
**Constraint:** read-only. No purchases, no downloads of paid content, no external-state changes.
**Sources:** all URLs accessed 2026-07-31 unless noted. Full bibliography § 8.

---

## 1. Executive summary

### 1.1 License verdict — **GREEN. The gate is open.**

The current Unity Asset Store EULA (last updated December 4, 2024; retrieved 2026-07-31) **contains no engine restriction whatsoever.** The license grant at § 2.2.1(a) permits incorporation into "an electronic application or digital media" — engine-agnostic language. The word "Unity" appears in the grant only as a party name. Three clauses make the translation direction affirmatively safe rather than merely un-prohibited:

- **§ 2.2.1(e)** expressly grants the right to **modify** the Assets in connection with incorporation and distribution.
- **§ 6** states flatly: *"END-USER may modify Assets."* The reverse-engineering / decompilation prohibition in that same section is **scoped only to Services SDKs** — so extracting a `.unitypackage` and re-authoring its contents is inside the grant, not a workaround of it.
- Unity's own support desk confirms it in plain language (article last updated 2025-07-02): *"engine choice doesn't matter, but EULA compliance does."*

Four compliance conditions travel with the purchase, and all four are comfortably satisfied by our use:

1. **Non-substantiality (§ 2.2.1(a)).** The Asset must not "comprise a substantial portion of the Licensed Product," and the product must have purpose and function beyond displaying assets. A game whose VFX layer is bought art is fine; an asset viewer is not.
2. **No end-user extraction (§ 2.2.1.1(b)).** Ship the assets baked into the game. Don't ship a modding surface that hands the raw effects back out.
3. **Restricted Assets (§ 2.2.2).** A per-asset check, not a blanket one. Any pack flagged "Restricted Asset" carries its own overriding terms. **None of the shortlist packs below are flagged**, but this must be re-verified on the purchase page at the moment of purchase.
4. **No AI/ML training (§ 2.2.1.1(g)).** Assets may not be used "as inputs for artificial intelligence or machine learning model programs." **This clause bears directly on the MCP idea and needs a bright line drawn:** an MCP that *mechanically parses YAML and emits Godot scenes* is deterministic software transformation and is not implicated. Feeding pack art or effect definitions to a model *to generate new effects* would be squarely inside the prohibition. Build the disassembler as a parser, not as a generator. This is a real constraint on how the tool is designed, and it is cheap to honor if honored from the start.

One correction to the 2026-06-18 run, which recorded this verdict as resting on "community consensus + support FAQ." It does not need to. **The primary text is unambiguous and now captured verbatim** (§ 2.1 below).

### 1.2 Pack shortlist — top 3

All prices are US list, verified from the live Asset Store product records on 2026-07-31. **None are currently on sale**, so these are the real numbers, not promo figures. (The 2026-06-18 run's "$24 Hovl" was a sale price; list is $48.)

| # | Pack | Publisher | Price | Pipeline | Register | Verdict |
|---|---|---|---|---|---|---|
| **1** | **Polygon Arsenal** | Archanor VFX | **$40** | Built-in RP / **Shuriken** | low-poly stylized — **native Synty register** | **Buy this one.** Covers both hero needs outright. |
| **2** | **Magic Arsenal** | Archanor VFX | **$30** | Built-in RP / **Shuriken** (publisher-stated) | stylized, spell-drama | Best second pack. Deepest spell coverage, most translation-friendly text on the store. |
| **3** | **Epic Toon FX** | Archanor VFX | **$40** | Built-in RP / **Shuriken** | cartoony — **under-register** | Volume play only (1,323 effects). Buy last, or skip. |

**The single pack that best covers boss-ultimate + melee-impact is Polygon Arsenal, and it is not close.** Its published contents list ships, by name:

- **`Ground Slam`** — the boss AoE-ultimate primitive, literally that name
- **`Nova (9 types)`** — including `FrostNova`, `LifeNova`, `HolyNova`, `ShadowNova` added in v2.03
- **`Melee & Sword (14 types)`** + **`Cleave`** — the swipe/claw need
- plus `Surface Explosion (10)`, `Ground Spikes (7)`, `Explosions (32)`, `Gore (11)`, `Death (8)`, `Dash`, `Shield`, `Charge`

1,383 total prefabs, 250+ unique FX, **100+ custom meshes**, 80+ materials, across 8 elemental themes (Fire / Frost / Holy / Life / Lightning / Nature / Shadow / Storm). Rated 5.0 (98 ratings). Actively maintained — v2.07, 15 May 2025, Unity 6000.0 LTS.

**Hovl Studio's RPG VFX Bundle ($48) is deliberately demoted from the 2026-06-18 run's #1 Unity slot.** It remains beautiful, and if we were shipping in Unity it would likely still be the pick. But it is the *wrong purchase for a translation workflow*, and the reason is § 1.3.

### 1.3 Translation-feasibility verdict — **FEASIBLE, and the pack choice is what makes it feasible.**

The decisive technical finding of this run is that **"translatability" is not a property of Unity in general — it is a property of the individual pack**, and it varies enormously. It turns on one question: *does the effect's appearance live in the art, or in the shader?*

- **Archanor packs put it in the art.** Magic Arsenal's store page states outright: *"All particle effects are created with the Shuriken particle system"* and *"The particles use Unity's standard particle shaders in both available pipelines"* — with only three custom URP shaders in the whole 450-effect pack. Polygon Arsenal says the same in weaker form: *"a mix of Unity's standard particle shaders and custom shaders made with Amplify Shader Editor."* And because Polygon Arsenal is a **low-poly** pack, its look is carried by **100+ custom meshes**, not by flipbook trickery. Meshes port losslessly. Unity's stock particle shader is a billboarded additive/alpha-blend with vertex-colour tint — that is `StandardMaterial3D` with `BLEND_MODE_ADD` + `BILLBOARD_ENABLED` in Godot. A near-1:1 mapping.
- **Hovl puts it in the shader.** The publish notes record *"V.5.2.0. Shaders replaced to Shader Graph"* and the pack ships bespoke `HS_SoftNoise`, `Blend_TwoSides`, `Blend_Distort`, `LightGlow`, `ShockWave` shaders. Those are HLSL node graphs. They do not port. Harvest a Hovl pack and you get textures plus a rebuild bill for the thing that actually made it look good.

So: **buy the mesh-and-stock-shader pack, not the shader-graph pack.** That inverts the previous run's ranking, and it is the single most actionable finding here.

The mechanical pipeline is proven at every step, with no unknowns:

1. **`.unitypackage` is a gzipped tar.** Verified from the source of `Cobertos/unitypackage_extractor` (680 stars) — it opens the file with `tarsafe.open()` and walks GUID-named directories each containing `asset`, `pathname`, `asset.meta`. No Unity install, no Unity licence, no proprietary format. ~20 lines of Python.
2. **`.prefab` is plain-text YAML.** Force Text is the **default** Asset Serialization mode for new Unity projects. Effects serialize as `!u!198` (ParticleSystem) and `!u!199` (ParticleSystemRenderer) — class IDs confirmed against Unity's YAML Class ID Reference. Every Shuriken module's parameters are readable as nested maps. (One known wrinkle: Unity's `!u!` tag-plus-anchor lines are not strictly valid YAML 1.1 and need a one-line preprocessing regex. Well-documented, not an obstacle.)
3. **Meshes and textures import to Godot natively.** Godot 4.3+ imports FBX directly via the built-in **ufbx** importer. No conversion step, no external tool.
4. **Behaviour is re-authored, not converted.** This is the real cost and it is irreducible — but the YAML gives you the exact source numbers to author *against*, which turns a taste problem into a transcription problem.

**On the custom MCP:** it is a genuine, buildable lane, not a fantasy. Steps 1–2 are deterministic parsing over open formats; step 4 is a mechanical field-mapping. The honest scoping note is that ~14 of Shuriken's 23 modules map cleanly to Godot's `ParticleProcessMaterial` (which exposes 107 properties), a handful map partially, and three do not map at all (§ 4.3). A tool that nails the clean 14 and reports the rest as TODO would remove most of the tedium while leaving the artistry to hand.

**No existing tool does this.** Unidot Importer (V-Sekai, 939 stars, last pushed 2024-11-12) is the closest thing and it explicitly lists **Shader as Unsupported** and does not list ParticleSystem among its supported asset types at all. Its value to us is bulk texture/mesh/material conversion — real, but adjacent. Nothing in the surveyed ecosystem translates Shuriken behaviour. If we want it, we build it. (§ 4.2)

### 1.4 Native-Godot verdict — **the native pool is exhausted, and this is now measured rather than estimated.**

The 2026-06-18 run compared the pools by inspection. This run counted them, on disk and at source.

- **The official Godot Asset Library returns 7 results for `particle` and 1 for `vfx` — and not one is an ARPG effect content pack.** All seven are authoring tools (YParticles3D, UniParticles3D, vkaParticleTool, Particle scene compositor, BurstParticles2D, Fancy particles) plus Kenney's CC0 2D particle textures. Three of the tools are already installed in `reincarnated-godot/addons/`.
- **Matt already owns essentially the entire Godot-native commercial pool.** `reincarnated-godot/Assets/Binbun_VFX/` holds **49 pack directories / 390 effect scenes**, plus `addons/vfx_library` (35 effects), `brackeys_vfx_bundle`, `Particle_FX`, and `ThirdParty/rpicster-vfx-textures`. That is the deepest and best-parameterized library the Godot ecosystem has, and it is the library that produced the bake-off Matt judged *"far too few and not quite the correct ARPG register/feel."* **The judgment was rendered against a near-complete sample of what Godot-native has to offer.** That is what makes it decisive rather than provisional.
- **Both hero needs score literal zero against the installed library.** A filename search across `Assets/` and `addons/` for `nova|slam|shockwave|quake|eruption|crater` returns only Synty *terrain meshes* and Binbun *loot beams*. A search for `claw|slash|swipe|swing|cleave|melee` returns only Synty *weapon meshes* and a trail-renderer demo scene. There is no boss nova and no melee swipe anywhere in the installed set.
- **Scale comparison:** Polygon Arsenal alone is **1,383 prefabs / 250+ unique FX for $40** — roughly 3.5× the *total* effect-scene count Matt currently has, from a single purchase, in the correct register, with both hero needs covered by name.

**One honest qualifier, and it matters.** The native pool is not *quite* fully drawn. The installed Binbun set covers beams, muzzle flashes, magic orbs, magic areas, poison, fire, ice, loot, projectiles, impacts, portals, smoke, skies, transitions — but **Binbun's `Battle FX` pack is NOT installed**, and per the 2026-06-18 survey it ships *6 flying slashes, 6 swings, **6 claws**, 12 shields, 6 charges* for ~$6. For a werewolf's swipe, that is the cheapest possible shot on goal and it should be taken regardless of the Unity decision — it is a $6 experiment against a named miss. It does **not** change the verdict, because nothing in the Binbun line addresses the boss nova / ground-slam at ARPG scale.

*(Source caveat: itch.io was returning HTTP 521 site-wide throughout this run, so Binbun's current pricing and any post-June releases could not be re-verified today. The Battle FX contents figure is carried forward from the 2026-06-18 run and is flagged accordingly.)*

### 1.5 What I'd tell Matt in one paragraph

The licence is clear and the direction is sound, but the pack to buy is not the one the June research pointed at. Buy **Polygon Arsenal ($40)** — it is Shuriken-based, mesh-driven, sits natively in the Synty low-poly register, and ships `Ground Slam`, `Nova (9 types)` and `Melee & Sword (14 types)` by name, which is exactly the two named misses. Its mesh-and-stock-shader construction is also what makes it the most translatable pack on the market; the prettier Hovl bundle is a shader-graph pack whose beauty is precisely the part that won't come across. Add **Magic Arsenal ($30)** if the spell layer needs depth. Spend **$6 on Binbun Battle FX first**, today, because it is a native-Godot shot at the swipe problem that costs less than lunch. And note that a meaningful share of "I don't feel the swings" is hit-stop, impact flash and camera impulse rather than particles — the conductor already routed that as the JUICE sub-scope, and no VFX purchase will substitute for it.

---

## 2. Q1 — Unity Asset Store licensing for cross-engine use

### 2.1 The primary text, verbatim

Retrieved 2026-07-31 from `https://unity.com/legal/as-terms`. Document header states **"Last updated: December 4, 2024."** Page footer: "Copyright © 2026 Unity Technologies."

*(Note on method: `unity.com/legal/as-terms` returns HTTP 403 to the WebFetch tool but serves normally to a standard browser user-agent over `curl`. The text below is the live page.)*

> **2.2.1 Non-Restricted Assets.** The following concerns only Assets that are not Restricted Assets: Subject to the restrictions set forth in this EULA, Licensor hereby grants to the END-USER a non-exclusive, non-transferable, worldwide, and perpetual license to the Asset solely:
>
> (a) to incorporate the Asset, together with substantial, original content not obtained through the Unity Asset Store, into an electronic application or digital media that has a purpose, features, and functions beyond the display, performance, distribution, or use of Assets ("**Licensed Product**") as an embedded component of that Licensed Product, such that the Asset does not comprise a substantial portion of the Licensed Product;
>
> (b) to reproduce, publicly display, publicly perform, transmit, and distribute the Asset as incorporated and embedded in that Licensed Product;
>
> (c) to incorporate the Asset into physical advertising materials […] solely for marketing purposes with respect to the Licensed Product;
>
> (d) monetize the Asset within and for use within a Licensed Product, including via in-app purchases; and
>
> (e) except as set forth in 2.2.1.1 below, **modify the Assets** in connection with (a), (b), (c), and (d).

**The operative observation: there is no engine term anywhere in the grant.** "Licensed Product" is defined by *purpose and function*, not by runtime. Nothing conditions the licence on the Unity Editor, the Unity Runtime, or a Unity build target.

The modification right is then restated even more plainly in a section whose title might otherwise be read as hostile:

> **6. Reverse Engineering, Decompilation, and Disassembly**
> END-USER may modify Assets. END-USER shall not reverse engineer, decompile, or disassemble **Services SDKs**, except and only to the extent that such activity is expressly permitted under mandatory statutory applicable law.

This is worth dwelling on, because it is the clause a cautious reader would fear. It cuts the other way. The prohibition is **scoped to Services SDKs** — Unity's own live-service integrations. For an art asset, the section's first five words are an affirmative grant. Extracting a `.unitypackage` to get at its textures and meshes is not "disassembly of a Services SDK"; it is modification of an Asset, expressly permitted.

### 2.2 The four conditions that do bind

**§ 2.2.1.1 Limitations on License** — the clauses relevant to us:

> (b) enable a customer or user of a Licensed Product to sell, transfer, distribute, lease, or lend the Assets for commercial gain or commercialize Assets within a Licensed Product,
>
> (d) use, reproduce, duplicate, publicly display, publicly perform, copy, modify, adapt, translate, prepare derivative works of, distribute, transfer, license, sublicense, rent, lease, lend, sell, trade, resell, or otherwise commercialize or monetize any Asset **except as expressly permitted in this EULA**,
>
> (g) use the Unity Asset Store or Assets for purposes such as **training an artificial intelligence or machine learning model** without the express consent from the Provider and/or Unity. This restriction includes the gathering, aggregation, extraction, scraping or any usage of the Unity Asset Store and/or Assets for dissemination, sale, or distribution, as well as using such Assets and/or the Unity Asset Store for data sets, in the creation process, or as inputs for artificial intelligence or machine learning model programs, whether for commercial or non-commercial purposes.

Note that (d) contains the word **"translate"** in its list of restricted acts — but the clause is expressly subject to "except as expressly permitted in this EULA," and § 2.2.1(e) permits modification in connection with incorporation into a Licensed Product. Translating an effect into Godot *for our own shipped game* is permitted; translating it to distribute the translation is not. That is the same line § 2.2.1.1(b) draws from the other side.

**§ 2.2.1.1(g) is the clause that most deserves the team's attention**, because it lands directly on the MCP proposal. The design rule that follows from it:

- ✅ **Permitted:** a deterministic parser/transformer. Read tar.gz → read YAML → map fields → emit `.tscn`. This is compilation, not learning.
- ❌ **Prohibited without consent:** using pack contents as training data, fine-tuning inputs, or generative conditioning to *synthesise* new effects.
- ⚠️ **Grey, and worth avoiding:** pasting effect definitions into an LLM to have it author the Godot equivalent. Arguably "as inputs for artificial intelligence… model programs." Cheap to sidestep by keeping the mapping in code.

**§ 2.2.2 Restricted Assets** — a per-asset check that must be done at purchase time:

> Restricted Assets have license terms different from other Assets. Those license terms are found in the materials accompanying Restricted Assets ("Restricted Asset Terms"). For clarity, to the extent Restricted Asset Terms are different from this EULA, the Restricted Asset Terms will control […]

Definition, § 2.9: *"any Asset licensed hereunder that is designated (on prior written approval from Unity) as a 'Restricted Asset' in any materials accompanying the Asset."* None of the shortlist packs carries this designation on its store page as of 2026-07-31, but the check costs seconds and should be repeated at the moment of purchase.

**§ 1.4** is a useful piece of context for who we are actually contracting with: for third-party packs the **Provider is the Licensor**, not Unity. Archanor VFX is our counterparty. This matters if a publisher ever attaches supplemental terms — worth a glance at the pack's own README after download.

### 2.3 Unity's own support desk

`support.unity.com` article "Can I use assets from the Asset Store with other engines?" — **last updated 2025-07-02**, i.e. current. Its summary line:

> "The core principle: engine choice doesn't matter, but EULA compliance does."

Prohibited uses per the article: redistributing assets as standalone items or in a form allowing extraction from the final product; forum pooling; monetizing UGC platforms without creator permission; making the asset the primary purpose of the project. Caveats named: Restricted Assets may carry separate terms, and open-source components inside a pack are governed by their own licences, which take precedence.

This corroborates the primary text on every point and adds nothing adverse.

### 2.4 The one carve-out to stay clear of

**Unity Companion License.** Assets published by **Unity Technologies itself** (URP/HDRP sample content, official tutorial assets) ship under the UCL, which *does* restrict use to Unity projects. This is not a hidden trap — it is a different licence attaching to a different class of asset. Practical rule: **verify the publisher is a third party, not Unity Technologies.** All three shortlist packs are Archanor VFX. Clear.

### 2.5 Verdict

**GO.** The gate is open on primary text, corroborated by the vendor's own support desk, with four named conditions all of which our use satisfies. The direction does not die here.

---

## 3. Q2 — Unity VFX pack shortlist (Shuriken-based; VFX Graph excluded)

### 3.1 Screening rule applied

Per commission: **VFX Graph is poorly translatable and is excluded.** The rule is well-founded — VFX Graph is a GPU-simulated node graph compiled to compute shaders, with no readable per-parameter serialization of the kind Shuriken offers. Everything below is **Built-in Render Pipeline / Shuriken**, verified from each product's own `compatibilityInfo` or `keyFeatures` field.

The generalist read on the split (2026 roundups) is that *"most new effects released on the Asset Store are built with URP as the primary target"* — which is precisely why the age of these packs is a feature, not a defect. Packs authored in the Built-in pipeline are Shuriken by construction, and Shuriken is the readable one.

### 3.2 The shortlist

#### **#1 — Polygon Arsenal · Archanor VFX · $40 · ★5.0 (98)**

`https://assetstore.unity.com/packages/vfx/particles/polygon-arsenal-109286`

| Field | Value |
|---|---|
| **Pipeline** | *"Created in the Built-in Render Pipeline with an included URP Upgrade package."* → **Shuriken** |
| **Shaders** | *"a mix of Unity's standard particle shaders and custom shaders made with Amplify Shader Editor"* |
| **Contents** | 250+ unique FX · **1,383 prefabs** · **100+ custom meshes** · 80+ materials · 80+ sound FX |
| **Elements** | Fire · Frost/Ice · Holy · Life · Lightning · Nature · Shadow · Storm |
| **First published** | 2018-02-13 · **latest v2.07, 2025-05-15** (Unity 6000.0.23f1 LTS+) |
| **Register** | *"low-poly styled VFX"* — **the Synty register exactly** |

**Combat contents, verbatim from the store listing:** Aura (6) · Barrage (2) · Beams · Chains (2) · Channel · Charge (2) · **Cleave** · Curses (9) · Debuffs (9) · Dash · Death (8) · Enchant (8) · Entangle (3) · Explosions (32) · Flamethrower (2) · Gore (11) · **Ground Slam** · Ground Spikes (7) · **Melee & Sword (14)** · Missiles (25) · Muzzleflash (30) · Necromancy (6) · **Nova (9)** · Orbital Beam · Regenerate (2) · Shield · Surface Explosion (10) · Surface Impact (7).

Plus Environment (Fire, Smoke, Sparks, Tornado, Godrays, Lightrays, Weather, Dust…) and Interactive (Portal, Loot, Powerups, Beam Up, Black Hole, Healing, Spawn, Treasure…).

**Why it wins both hero needs.** The commission asks for a boss AoE-ultimate ground-slam/nova and melee swipe/claw with impact register. This pack ships a category *named* `Ground Slam`, a category of nine `Nova` variants (`FrostNova`, `LifeNova`, `HolyNova`, `ShadowNova` explicitly added in v2.03 alongside `Club Slam (4 prefabs)`), and fourteen `Melee & Sword` types plus `Cleave`. There is no interpretation step between the need and the contents.

**Why it wins on translation.** Two properties compound:
- **Low-poly means mesh-driven.** 100+ custom meshes carry the silhouette. Meshes port losslessly to Godot via native ufbx import — zero fidelity loss, zero rebuild.
- **Stock shaders mean portable materials.** Unity's standard particle shader is billboard + additive/alpha blend + vertex colour. That is a `StandardMaterial3D` in Godot with three checkboxes set. The Amplify custom shaders are the minority case.

The change record also reads like a maintained product rather than an abandoned one: v2.03 (2022) added Club Slam / four Novas / Firewall; v2.04 (2023) added Lightning Strike, Necromancy Corpse Explosion, Lightning Wave; v2.06 (2024) *"Fixed rotations in nova effects"*; v2.07 (2025) tuned URP colours.

**Caveats, honestly stated:** the "low-poly" register is a genuine two-sided call. It composites perfectly over Synty geometry — but Diablo 4 and PoE are *not* low-poly, and Matt's target is "stylized-3D but ARPG-grade layered." Polygon Arsenal will need emission cranked and layers stacked to reach that density. The store page notes *"works best with bloom enabled."* **This is the one thing I could not resolve without eyes on it** — see § 6.1.

---

#### **#2 — Magic Arsenal · Archanor VFX · $30 · ★5.0 (249)**

`https://assetstore.unity.com/packages/vfx/particles/spells/magic-arsenal-20869`

| Field | Value |
|---|---|
| **Pipeline** | Built-in RP + URP Upgrade. **Publisher states explicitly: *"All particle effects are created with the Shuriken particle system."*** |
| **Shaders** | *"The particles use Unity's standard particle shaders in both available pipelines. The asset includes three custom shaders for URP."* |
| **Contents** | **450 effects** |
| **First published** | 2014-08-18 · latest v2.75, 2024-12-06 |

**Contents:** Area Damage · Aura Cast (2) · Aura (4) · Beams · Beam Blast · Charge · **Cleave** · Curse · Damage over Time · Enchant · Explosion/Impact (4) · Flames · Mesh Glow · Missile (4) · Muzzleflash/Cast (2) · **Nova** · Orbit Sphere · **Pillar Blast** · Rain (2) · Shield (2) · **Slash** · **Slash Hit** · Sphere Blast · Spray · Wall (Circle & Line).

**This is the most translation-friendly pack found in the entire survey**, and it says so itself. "Shuriken" stated outright; "Unity's standard particle shaders" for the whole set; exactly **three** custom shaders across 450 effects. Almost nothing is locked behind a graph. It is also the only pack whose store page volunteers the exact fact a translator needs to know.

Register runs more "classic fantasy spell" than low-poly — a slightly different voice from Polygon Arsenal, which is arguably useful (spell-drama layer vs. physical-impact layer) but does mean it is a second purchase, not a substitute.

Note the age: first published 2014. Still patched into 2024, but it is the oldest thing on this list.

---

#### **#3 — Epic Toon FX · Archanor VFX · $40 · ★5.0 (245)**

`https://assetstore.unity.com/packages/vfx/particles/epic-toon-fx-57772`

| Field | Value |
|---|---|
| **Pipeline** | *"created in the built-in render pipeline… comes with an URP Upgrade package"* → **Shuriken** |
| **Shaders** | *"particles mostly use Unity's standard particle shaders and a few custom shaders made with Amplify Shader Editor"* · *"Bloom is not required"* |
| **Contents** | **1,323 effects** |
| **First published** | 2016-03-22 |

**Relevant contents:** **Nova (4)** · **Sword (12)** · **Brawling (10)** · Explosions (40) · Explosions Misc (18) · **Decals (8)** · Blood (13) · Death (10) · Gore/Giblets (6) · Magic (12) · Missiles (30) · Muzzleflash (26) · Flamethrower (3) · Shield.

Genuinely enormous, genuinely cheap per effect, genuinely well-rated, and technically the same friendly Shuriken/stock-shader construction as its siblings. **But the register is wrong.** Its own elevator pitch says *"1323 cartoony particle effects"* and *"Bloom is not required"* — bloom-optional is a fair proxy for "not juicy." Matt's complaint was that the current catalogue is *not ARPG enough*; a cartoon pack pushes further in the direction he rejected.

Its one distinctive asset is the **8 ground decals** (blood/scorch), which the Godot-native pool lacks entirely and which Polygon Arsenal does not list. That is a real gap-filler — but an $40 gap-filler for eight decals is poor value.

**Recommendation: skip unless volume becomes the objective.**

---

### 3.3 Considered and demoted

**Hovl Studio — RPG VFX Bundle · $48 · ★5.0 (52)** — `…/spells/rpg-vfx-bundle-133704`. Supported Unity: 2020.3.18 → 6000.0.67; maintained through v6.0.5. Contents: *"AAA Magic Circles and Shields, AAA Stylized Projectiles, AOE Magic spells Vol.1, 3D Lasers Pack, Map Track Markers VFX."* Textures 2048² down to 64².

Ranked **#1 Unity harvest in the 2026-06-18 run. Demoted here on new evidence.** The publish notes record **`V.5.2.0. Shaders replaced to Shader Graph`**, and the pack's identity is carried by bespoke shaders — `HS_SoftNoise`, `Blend_TwoSides`, `Blend_Distort`, `HDRP_LightGlow`, `ShockWave` (names taken from the sibling Sword-slashes-PRO change record). Under a *Unity* workflow this is a strength: the shaders are the craft. Under a *translation* workflow it is the defect, because the shaders are the part that cannot come across. You would pay $48 (+$5 for Hovl's separate URP/HDRP support package) largely for textures and a rebuild bill.

Also note: at **$48 list** it is the most expensive option, and the June figure of $24 was a sale price.

**Hovl Studio — Sword slashes PRO · $20** — 22 unique slash effects + 11 combo skills / 28 prefabs / **12 custom shaders**. On paper this is the melee-swipe pack. In practice 12 custom shaders across 28 prefabs is the worst art-to-shader ratio on this list — it is a shader pack wearing a slash pack's clothes. **Not recommended for translation.** Polygon Arsenal's 14 Melee & Sword types come free with a purchase we want anyway.

**kripto289 — Mesh Effects · $23** — `…/spells/mesh-effects-67803`, first published 2016, v1.5.0a. Interesting edge case: **mesh-based rather than particle-based**, which is *more* portable in principle (animated meshes + shaders port better than emitter graphs). Publisher's change log is heavy on URP/HDRP/VR shader fixes, implying meaningful shader dependence. Worth a look if a second melee/impact voice is wanted; not a first purchase. kripto289's *Impacts and Muzzle Flashes* is $18.

**Gabriel Aguiar Prod** — named in the commission. Excluded: his output is predominantly **free YouTube tutorials plus VFX-Graph-era work**, and I could not identify a Shuriken-based ARPG pack of the required scope on the Asset Store within this run's bounds. His tutorials remain a good *authoring* reference for building effects natively in Godot. Flagged as an unresolved gap (§ 6.3).

**Piloto Studio "Realistic ARPG" line** — carried forward from June: register over-shoots (semi-real/HDRP-targeted) against flat-shaded Synty geometry. Not re-examined this run.

### 3.4 The pattern worth naming

All three shortlist packs are from **one publisher**. That is not sloppiness in the sampling — it is the finding. **Archanor VFX is systematically the most translation-friendly publisher on the Unity Asset Store**, because their house style is Built-in-pipeline Shuriken driven by stock particle shaders and custom meshes, and they *document* it on every product page. Publishers who compete on shader sophistication (Hovl, Piloto) build packs whose value is structurally non-portable.

**A translation strategy should select for publisher construction philosophy, not for demo-reel beauty.** The prettiest Unity pack is, reliably, the worst Unity pack to translate.

---

## 4. Q3 — Prior art on Unity→Godot particle translation

### 4.1 Format facts (all verified this run)

| Layer | Format | Verification |
|---|---|---|
| `.unitypackage` | **gzipped tar**; entries are GUID-named dirs each holding `asset`, `pathname`, `asset.meta` | Read the source of `Cobertos/unitypackage_extractor` — `tarsafe.open(name=packagePath)` then `os.scandir` over GUID dirs, requiring `pathname` + `asset` |
| `.prefab` / `.unity` / `.mat` | **YAML text**, `%YAML 1.1` + `%TAG !u! tag:unity3d.com,2011:`, objects tagged `!u!<classID> &<fileID>` | Unity Manual, YAML Scene Example |
| Serialization default | **Force Text is the default for new Unity projects** | Unity Blog + JetBrains Rider docs |
| ParticleSystem | **class ID 198**; ParticleSystemRenderer **199** | Unity YAML Class ID Reference |
| FBX → Godot | **native**, via built-in **ufbx** importer, Godot **4.3+** | Godot docs, "Available formats" |

**Consequence:** every layer between a purchased `.unitypackage` and a readable Shuriken parameter set is an open, documented, plain-text format. No proprietary binary. No Unity install required. No Unity licence required to *read* what you bought. This is the strongest possible substrate for a custom tool, and it is why the MCP idea is sound rather than speculative.

One practical wrinkle: Unity's `!u!` tag-with-anchor lines are not strictly valid YAML 1.1 and choke naive parsers. The standard fix is a one-line regex preprocess before handing to PyYAML. Widely documented; not a blocker.

### 4.2 What exists, and what it does not do

| Tool | Status (checked 2026-07-31) | Does it help? |
|---|---|---|
| **Unidot Importer** (V-Sekai) | 939★ · last pushed **2024-11-12** · not archived | **Partly.** Supported: Mesh/MeshRenderer, **Material (standard shader only)**, Texture2D, AnimationClip, AnimatorController, PrefabInstance, AudioClip, Terrain. Unsupported, verbatim: *"Shader… porting must be done by hand"*, *"MonoBehaviour"*, *"Anything not listed above."* **ParticleSystem does not appear in the supported list.** Use it for bulk texture/mesh/material conversion; it will not translate an effect. |
| **Cobertos/unitypackage_extractor** | 680★ · last pushed 2023-02-09 · Python | **Yes, for step 1.** Small, readable, does exactly one thing. Slightly stale but the format hasn't changed. |
| **SamarthMP/unitypackage-extractor** | 37★ · pushed **2025-01-07** · Python, GUI+CLI | Freshest extractor. Same job. |
| **paulbartrum/UnityPackageExtractor** | 4★ · pushed 2024-02-19 · C# | Minimal traction. |
| **Anthogonyst/UnityToGodot** | 196★ · pushed 2024-02-09 · C# | Project-level asset prep. No particle path. Effectively dormant. |
| **AssetRipper** | active | Wrong tool — targets *compiled game builds*, not `.unitypackage`. Not applicable. |

**Finding: no Shuriken→Godot particle translator exists, anywhere, in any state of repair.** Not abandoned — never built. The gap in the ecosystem is real and un-filled.

### 4.3 Which Shuriken modules map cleanly to Godot 4

> **Method + epistemic status.** No published Shuriken→Godot mapping exists (searched; the closest results are generic tutorials). What follows is **my own synthesis**, constructed by cross-walking two enumerated property sets: Unity's 23 `ParticleSystem` module properties (from the Unity 6000.0 Scripting API reference) against Godot's 107 `ParticleProcessMaterial` properties (from the Godot stable class reference). Both enumerations are cited fact; **the mapping judgments are mine and are inference.** They are offered as a scoping estimate for the MCP, not as a verified conversion table. Anything built on this should be validated against a real effect early.

**Clean (≈14 of 23) — direct property-to-property:**

| Shuriken module | Godot `ParticleProcessMaterial` |
|---|---|
| `main` (lifetime, start speed/size/rotation/colour, gravity) | `lifetime`, `initial_velocity_min/max`, `scale_min/max`, `angle_min/max`, `color`, `gravity` |
| `emission` (rate) | `GPUParticles3D.amount` + `emission_curve` |
| `shape` (sphere/box/cone/ring/mesh) | `emission_shape` + `emission_sphere_radius` / `emission_box_extents` / `emission_ring_*` |
| `colorOverLifetime` | `color_ramp` |
| `sizeOverLifetime` | `scale_curve` |
| `rotationOverLifetime` | `angular_velocity_*` / `rotation_velocity_3d_*` |
| `velocityOverLifetime` | `directional_velocity_curve`, `orbit_velocity_*`, `radial_velocity_*` |
| `forceOverLifetime` | `linear_accel_*`, `radial_accel_*`, `tangential_accel_*` |
| `limitVelocityOverLifetime` | `velocity_limit_curve`, `damping_*` |
| `noise` | `turbulence_*` (9 properties) |
| `collision` | `collision_mode`, `collision_bounce`, `collision_friction` |
| `subEmitters` | `sub_emitter_mode` + `sub_emitter_amount_at_start/end/collision` |
| `textureSheetAnimation` | `anim_speed_*`, `anim_offset_*` + `particles_anim_h/v_frames` |
| `inheritVelocity` | `inherit_velocity_ratio` |

**Partial (≈6) — approximable with loss:** `sizeBySpeed` / `colorBySpeed` / `rotationBySpeed` (Godot has `scale_over_velocity_curve` but no colour- or rotation-by-speed); `trails` (Godot trails exist but differ structurally); `externalForces` (Godot attractors are nodes, not a material flag — `attractor_interaction_enabled` only gates participation); `lights` (re-author as child `OmniLight3D`).

**No mapping (3):** `customData` (per-particle custom streams — needs a custom particle shader using `INSTANCE_CUSTOM`); `trigger` (no Godot equivalent); `lifetimeByEmitterSpeed` (no equivalent).

**And the part no table can capture:** the **Renderer** module (`ParticleSystemRenderer`, class 199) — billboard mode, render alignment, sort mode, blend mode, and *which material* — is where a great deal of the visual identity actually lives, and it maps to a mixture of Godot `GPUParticles3D` flags and `StandardMaterial3D` settings. For an Archanor pack this is easy (stock shader). For a Hovl pack it is the whole ballgame.

**Scoping read:** a tool that converts the clean 14 and emits a TODO manifest for the rest would remove the great majority of the transcription labour. That is a genuinely attractive build. It does **not** eliminate hand-authoring, and it should not be sold internally as if it did.

---

## 5. Q4 — Godot-native alternative (honest depth comparison)

### 5.1 The official library, measured

Godot Asset Library API, queried 2026-07-31 against `godot_version=4.5`:

- `filter=particle` → **7 results.** YParticles3D · UniParticles3D · Particle scene compositor · BurstParticles2D · vkaParticleTool · Kenney Particle Pack · Fancy particles
- `filter=vfx` → **1 result.** "Select By Type" (a Tools-category addon, matched on description text — not a VFX asset at all)

**Six of the seven are authoring tools. The seventh is Kenney's CC0 2D particle textures.** The official Godot library contains **zero** 3D ARPG-register VFX content packs. Three of the tools (`YParticles3D`, `UniParticles3D`, `vkaParticleTool`) are already installed in `reincarnated-godot/addons/`.

### 5.2 What is already on disk

`~/Games/reincarnated-godot/`:

| Location | Contents |
|---|---|
| `Assets/Binbun_VFX/` | **49 pack directories** |
| `Assets/Binbun_VFX/` + `Assets/BinbunVFX/` | **390 `.tscn` effect scenes** |
| Binbun categories installed | beam_vfx · muzzle_flash · magic_orbs · magic_areas · poison_effects · fire_effects · loot_effects · magic_projectiles · impact_explosions · portal_vfx · smoke_effects · ice_effects · skies · transitions · card_effects · hologram |
| `addons/vfx_library` (haowg) | 35+ particle effects · 17+ shaders |
| also | `brackeys_vfx_bundle` · `Particle_FX` · `Demo2D_VFX` · `ThirdParty/rpicster-vfx-textures` · `Synty/particle-fx-shapes` |

Binbun is the deepest and best-parameterized library in the Godot ecosystem (the 2026-06-18 run measured 5/6 parametric axes exposed via tool script, CC0 licensed). **Matt owns 49 of its packs.** The bake-off Matt judged *"best assets so far but likely far too few and not quite the correct ARPG register/feel"* was run against this. **The verdict was rendered on a near-complete sample of what Godot-native has to offer** — which is what elevates it from a provisional impression to a finding.

### 5.3 The two hero needs, scored against what's installed

Filename search across `Assets/` and `addons/`:

- **`nova|slam|shockwave|shock_wave|quake|eruption|crater|ground`** → matches are **Synty terrain meshes** (`SM_Env_Ground_Dirt_01`…) and **Binbun loot beams** (`ground_loot_vfx_legendary`…). **No nova. No ground slam. No shockwave.**
- **`claw|slash|swipe|swing|cleave|sword|melee`** → matches are **Synty weapon meshes** (`SM_Wep_Sword_01`, `SM_Wep_Cleaver_01`) and one `TrailRenderer/Samples/sword_demo.tscn`. **No claw. No slash VFX. No swipe.**

**Both named misses score literal zero against the installed native library.** Matt's two complaints are not tuning problems. They are absences.

### 5.4 The remaining native headroom — and why it doesn't change the verdict

Honesty requires naming what has *not* been tried. Binbun packs **not** installed include **`Battle FX`**, which per the 2026-06-18 survey ships *12 shields · 6 flying slashes · **6 swings** · **6 claws** · 6 charges* for ~$5.94 CC0. Also absent: `Hit FX` (28 impact presets), `Status FX`, `Electric FX`, `Dark Magic FX`, `Flame FX`.

**`Battle FX` is a direct, cheap shot at hero need #2** and should be bought regardless of what happens with Unity — six dollars against a named miss is not a decision, it's a reflex. If it lands, the swipe problem may be substantially cheaper than the Unity route suggests.

It does **not** move the overall verdict, because:
- Nothing in the Binbun line — installed or not — addresses a **boss nova / ground-slam at ARPG scale**. That gap is ecosystem-wide, not inventory-specific.
- Matt's register complaint was aimed at Binbun's *house style*, which `Battle FX` shares. More Binbun is more of the thing that was judged not-quite-right.

### 5.5 Depth comparison

| | Godot-native | Unity |
|---|---|---|
| Official-library ARPG VFX packs | **0** | hundreds |
| Practical commercial pool | Binbun (~20 packs) + Bukkbeek + a thin free tail | Archanor, Hovl, Piloto, kripto289, GAPH, Vefects, EpicToonFX, … |
| Deepest single pack | Binbun Vol. 1 — 300+ effects, $26.25 | **Polygon Arsenal — 1,383 prefabs / 250+ FX, $40** |
| Already owned by Matt | **essentially all of it** (49 packs / 390 scenes) | none |
| Boss nova / ground slam | **absent from the ecosystem** | `Ground Slam` + `Nova (9)` named in one $40 pack |
| Melee claw / swipe | Binbun `Battle FX` (~$6, **not yet tried**) | `Melee & Sword (14)` + `Cleave` in the same $40 pack |
| Licensing | CC0 — frictionless | perpetual commercial, cross-engine permitted, four conditions |
| Integration cost | zero | high per effect; amortizes across the pipeline |

**Verdict: the native pool is not deep enough, and translation infrastructure is therefore justified — but only because it is now demonstrated rather than assumed.** The strength of this conclusion rests on the fact that Matt already bought and tested the native ceiling. Buy `Battle FX` for $6 first anyway; it is the cheapest possible falsification test of half the thesis.

---

## 6. Q5 — Blender's realistic role

**Short version: much narrower than the framing assumes, and one of its two presumed jobs is already obsolete.**

### What Blender genuinely does for this

1. **Flipbook baking — the real job.** Rendering an animated 3D sim (fire, smoke, energy churn) to an image sequence and packing it into a sprite-sheet atlas for use as a particle texture. Actively-maintained 2026 tooling exists: **Sequenced Bake** (Blender Extensions, v1.1.6, 2026-05-09 — explicitly *"supports flipbook textures, particle atlases, and engine-ready sprite sheets"*), **Spritehandler** (Superhive, updated for Blender 5.2 in May 2026), **SpriteSheet Animator** (BlendAtlas), **Sprite Atlas Addon**. Godot consumes these directly via `ParticleProcessMaterial` H/V frames.
2. **Mesh repair.** Pivot/origin correction, axis conventions, scale normalization, cleanup on trail/beam/cone geometry that imports badly. Real but occasional.
3. **Authoring net-new geometry** in the Polygon Arsenal style — low-poly nova rings, shockwave cones, slash arcs. For a *low-poly* register this is genuinely tractable: these are simple lathed and extruded forms. Worth noting as a fallback if the purchase is declined.

### What Blender does not do

1. **It cannot read `.unitypackage`.** No importer exists, and none is likely — the format is a Unity-project archive, not an interchange format.
2. **It cannot read Shuriken.** There is no Blender importer for Unity particle definitions, and the concept doesn't map: Blender's particle system is a different model with different semantics. **Any mental picture of "Unity → Blender → Godot" for the *behaviour* layer is wrong.** Behaviour goes Unity-YAML → parser → Godot, and never touches Blender.
3. **It is no longer needed as an FBX waystation.** This is the finding that shrinks its role. Godot's docs: *"By default any FBX file added to a Godot project in Godot 4.3 or later will use the ufbx import method."* Godot 4 natively imports glTF 2.0, `.blend`, DAE, OBJ **and FBX**. The FBX → Blender → glTF dance that the 2026-06-18 run specified as pipeline Step 3 is **obsolete**; drop the FBX straight into Godot.

### Corrected pipeline shape

```
.unitypackage ──(python tarfile)──► raw Assets/ tree
    ├── Textures/ (PNG/TGA)  ──────────────────────────────► Godot import  [direct]
    ├── Meshes/  (FBX)       ──────────────────────────────► Godot ufbx    [direct, 4.3+]
    └── *.prefab (YAML !u!198/199) ──(parser)──► params ───► Godot .tscn   [the MCP]

Blender enters ONLY here:  ⤷ flipbook baking (Sequenced Bake / Spritehandler)
                           ⤷ mesh pivot/axis repair (exception path)
                           ⤷ authoring net-new low-poly VFX geometry
```

**Verdict: Blender is a useful side-tool for texture and geometry work. It is not on the critical path, and it has no role at all in translating particle behaviour.** Do not scope it as a translation component.

---

## 7. Knowledge gaps not resolved

1. **Polygon Arsenal's actual visual register — the most important open question.** Its contents match the two hero needs by name, and its construction is ideal for translation. But "low-poly stylized" against a target of "stylized-3D with ARPG-grade layered density" is a judgment call I cannot make from a product page. **Matt should watch the WebGL demo and the video before purchasing** (`https://assetstore.unity.com/packages/vfx/particles/polygon-arsenal-109286` — the listing links a live WebGL demo, which is the fastest possible check and costs nothing). The specific thing to look at: do the Nova and Ground Slam effects read as *heavy* — layered, bloomed, with impact weight — or as *clean and light*? If the latter, they will need substantial emission/layer work and the value proposition weakens.

2. **Binbun `Battle FX` current price and contents — could not re-verify.** itch.io returned **HTTP 521 site-wide** for the entire duration of this run (all `binbun3d.itch.io` pages and `itch.io/s/...` sale pages, via both curl and WebFetch). The figures used here (~$5.94; 6 slashes / 6 swings / 6 claws / 12 shields / 6 charges) are **carried forward from the 2026-06-18 run and are not fresh**. Two named-but-unverified items also surfaced in search: a "GODOT VFX Summer Sale 2026" and a "Godot VFX Bundle — 700+ Assets" listing. **Re-check when itch.io recovers** — the 700+ figure, if real, is materially larger than the Vol.1/Vol.2 numbers on record and would deserve a second look at the native verdict.

3. **Gabriel Aguiar Prod — not properly surveyed.** Named in the commission; my URL guesses missed and I did not have bounded budget to enumerate his store. My understanding is that his output skews to free tutorials and VFX-Graph-era work, but **this is unverified** and should not be treated as a finding. If a fourth pack is wanted, this is the first place to look.

4. **The Shuriken→Godot module mapping (§ 4.3) is my inference, not documented fact.** Both property enumerations are cited primary sources; the cross-walk between them is mine. No published mapping exists to check it against. Validate against one real effect before scoping a build on these numbers.

5. **Restricted-Asset status not verifiable pre-purchase.** § 2.2.2 terms live "in materials accompanying the Asset" — i.e. visible after download. No shortlist pack shows the designation on its store page, but this cannot be fully confirmed until purchase. Low risk; non-zero.

6. **Publisher supplemental terms unread.** Archanor's own README/licence inside the packages was not accessible (would require purchase). § 1.4 makes the Provider the Licensor, so a publisher *could* attach terms. Worth a glance post-download.

7. **Not attempted, and deliberately so:** no `.unitypackage` was downloaded, no paid content acquired, no purchase made. All pack contents above are from publisher-published product descriptions. Cell was read-only per commission.

---

## 8. Source list

All accessed **2026-07-31** unless otherwise noted.

**Licensing (primary):**
- Unity Asset Store Terms of Service and EULA — `https://unity.com/legal/as-terms` (doc header: "Last updated: December 4, 2024"; retrieved via browser UA — returns 403 to some automated clients)
- Unity Support, "Can I use assets from the Asset Store with other engines?" — `https://support.unity.com/hc/en-us/articles/34387186019988-Can-I-use-assets-from-the-Asset-Store-with-other-engines` (article last updated 2025-07-02)
- Unity Asset Store EULA FAQ — `https://assetstore.unity.com/browse/eula-faq`
- Unity Support, "Who is covered by the Asset Store EULA?" — `https://support.unity.com/hc/en-us/articles/360013082232`
- Unity Asset Store Terms — Legacy — `https://unity.com/legal/as-terms-legacy`

**Packs (Unity Asset Store product records):**
- Polygon Arsenal (Archanor VFX) — `https://assetstore.unity.com/packages/vfx/particles/polygon-arsenal-109286`
- Magic Arsenal (Archanor VFX) — `https://assetstore.unity.com/packages/vfx/particles/spells/magic-arsenal-20869`
- Epic Toon FX (Archanor VFX) — `https://assetstore.unity.com/packages/vfx/particles/epic-toon-fx-57772`
- RPG VFX Bundle (Hovl Studio) — `https://assetstore.unity.com/packages/vfx/particles/spells/rpg-vfx-bundle-133704`
- Sword slashes PRO (Hovl Studio) — `https://assetstore.unity.com/packages/vfx/particles/sword-slashes-pro-173450`
- Mesh Effects (kripto289) — `https://assetstore.unity.com/packages/vfx/particles/spells/mesh-effects-67803`
- Impacts and Muzzle Flashes (kripto289) — `https://assetstore.unity.com/packages/vfx/particles/impacts-and-muzzle-flashes-57010`
- kripto289 publisher page — `https://assetstore.unity.com/publishers/5224`
- Archanor assets index — `https://archanor.com/assets.html`
- "20 Best Unity Effect Assets (2026): URP, HDRP, VFX Graph & More" — `https://unityasset.soldier.jp/en/unity-effect-assets/`

**Engine references:**
- Unity ParticleSystem Scripting API (module enumeration) — `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/ParticleSystem.html`
- Unity Particle System component reference — `https://docs.unity3d.com/6000.0/Documentation/Manual/class-ParticleSystem.html` (page built 2026-07-30)
- Unity YAML Class ID Reference — `https://docs.unity3d.com/6000.0/Documentation/Manual/ClassIDReference.html`
- Unity YAML Scene Example — `https://docs.unity3d.com/6000.0/Documentation/Manual/YAMLSceneExample.html`
- Unity, "Understanding Unity's serialization language, YAML" — `https://unity.com/blog/engine-platform/understanding-unitys-serialization-language-yaml`
- JetBrains Rider, Asset serialization mode — `https://www.jetbrains.com/help/rider/Asset-serialization-mode.html`
- Godot `ParticleProcessMaterial` class reference (107 properties) — `https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html`
- Godot `GPUParticles3D` class reference — `https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html`
- Godot, Importing 3D scenes — available formats (ufbx) — `https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html`

**Tooling:**
- Unidot Importer (V-Sekai) — `https://github.com/V-Sekai/unidot_importer` · Asset Library `https://godotengine.org/asset-library/asset/2427` · docs `https://docs.unidot.org/`
- Cobertos/unitypackage_extractor — `https://github.com/Cobertos/unitypackage_extractor`
- SamarthMP/unitypackage-extractor — `https://github.com/SamarthMP/unitypackage-extractor`
- paulbartrum/UnityPackageExtractor — `https://github.com/paulbartrum/UnityPackageExtractor`
- Anthogonyst/UnityToGodot — `https://github.com/Anthogonyst/UnityToGodot`
- AssetRipper — `https://assetripper.org/`
- Godot Asset Library API — `https://godotengine.org/asset-library/api/asset?filter=particle&godot_version=4.5`

**Blender / flipbook:**
- Sequenced Bake — `https://extensions.blender.org/add-ons/sequenced-bake/` (v1.1.6, 2026-05-09)
- Spritehandler — `https://superhivemarket.com/products/spritehandler`
- SpriteSheet Animator — `https://blendatlas.com/products/spritesheet-animator-node`
- Mattline1/SpriteAtlasAddon — `https://github.com/Mattline1/SpriteAtlasAddon`
- VFXDoc, Flipbooks and Texture Sheets — `https://vfxdoc.readthedocs.io/en/latest/textures/flipbooks/`

**Godot-native pool:**
- Binbun itch.io store — `https://binbun3d.itch.io/` — **HTTP 521 throughout this run; not re-verified**
- haowg/GODOT-VFX-LIBRARY — `https://github.com/haowg/GODOT-VFX-LIBRARY`
- gdquest-demos/godot-4-VFX-assets — `https://github.com/gdquest-demos/godot-4-VFX-assets`
- iHoshiii/Godot-VFX — `https://github.com/iHoshiii/Godot-VFX`
- 80.lv, "Purchase This Ultimate Godot VFX Pack" — `https://80.lv/articles/get-over-60-customizable-stylized-vfx-for-your-godot-project`

**Local evidence (this machine, 2026-07-31):**
- `~/Games/reincarnated-godot/Assets/Binbun_VFX/` — 49 pack directories
- `~/Games/reincarnated-godot/Assets/{Binbun_VFX,BinbunVFX}/**/*.tscn` — 390 effect scenes
- `~/Games/reincarnated-godot/addons/{vfx_library,vkaParticleTool,UniParticles3D,yparticles3d}/`
- Hero-need filename searches across `Assets/` + `addons/` — zero matches for nova/slam/shockwave and for claw/slash/swipe

---

*Research artifact authored 2026-07-31 · Mode A analytical · VFX-SCOUT cell of run BR-1 · conductor: gandalf*
*Legolas — researcher and scout. Read-only throughout: no purchases, no paid downloads, no external-state changes.*
