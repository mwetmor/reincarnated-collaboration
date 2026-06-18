# Ruling — Synty Asset Acquisition Run (KR)

**STATUS:** RULING (gandalf design-steward verdict on the acquisition run)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 — "rule on the KR synty asset run."
**Subject:** the KR-orchestrated Synty asset acquisition + catalogue workstream (Matt directive: *"download all assets that could possibly be used and get gandalf all his info"*).
**Method discipline:** ruled against DISK, not prose — KR's report carried one stale fact, and my own first-pass reconciliation carried one error; both were caught against disk before this ruling committed (§ 1). This is the same reconcile-against-disk discipline v2 § 0.1 mandates — applied to my own draft, not just KR's report.
**Companions:** `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/` (the catalogue); `slice-verification-2026-06-17.md` (galadriel); `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` (the consumer architecture); `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` (the §7.6 ruling the acquisition fed).

---

## 0. TL;DR — the verdict

**ACCEPT the acquisition run.** Complete, sound, zero failures, and *design-sufficient with deep margin*. The completist scope ("download all") was the CORRECT call given the irreversibility (subscription-gated; you cannot re-acquire after lapse — over-acquire is cheap, under-acquire is fatal). The run passes the only test that ultimately matters for an acquisition — **fit-for-purpose: it already enabled the downstream design work** (the gear-spec §7.2 restyle-leaf is BUILDING off it, engine `5f85014`). 

Two riders, both gandalf-owned, neither blocking the ACCEPT:
1. **The consumption-time partition is the next step** (§ 4) — 157 packs is the right CORPUS but the wrong CONSUMPTION SET; the locked register + genre filter prunes it to a fantasy-ARPG-core for downstream selection. This is my seam (role def: register = consumption-time filter, not crawl-scope constraint). I sketch it here; elrond materializes it.
2. **Cloud backup carries high design-weight** (§ 5) — the corpus is now a load-bearing, irreplaceable design dependency. Recommendation, not authorization (ADR-006 external write = Matt's call).

---

## 1. Reconciliation against disk (KR's report vs. ground truth)

| KR claim | Disk truth | Verdict |
|---|---|---|
| FBX corpus 136/136 (8.8 GB), 0 failures | `~/Games/synty-corpus/fbx/` = **136 zips** confirmed | ✅ TRUE |
| 21/21 no-FBX Unity packs extracted → 8,655 FBX + 11,930 textures | `nonfbx_extracted/` present (23 dirs); extract.log clean | ✅ TRUE (counts not re-tallied; structure consistent) |
| 157 packs / 62,281 mesh assets catalogued | `collections-157.json` = **157 entries**; `full-fbx-variant-manifest.jsonl` present | ✅ TRUE |
| resumption gate: both predictions YES + slice catalogued | `slice-verification-2026-06-17.md` (#2+#3 YES); elrond manifests present | ✅ TRUE |
| **"gandalf's §7.6 ruling doc is still untracked"** | **COMMITTED at `efc29af`**; `git status` clean | ❌ **STALE** — KR's parallel session predated my commit |
| §7.2 build "already moving / PASS-WITH-INFO at `869c31b`" | `869c31b` IS the collab-repo Gate-2 **finding** on §7.2 (jack-ryan, PASS-WITH-INFO); it gates engine build `5f85014` (rocket's restyle-leaf). Two valid hashes, two repos: the build (engine `5f85014`) + its gate-finding (collab `869c31b`). Keystone is engine `7a3cb6b` (Gate-2 PASS, 2 PARK). | ✅ TRUE — KR's hash was correct; my first-pass reconciliation wrongly flagged it (checked only the collab span vs the engine build hash), caught on full cross-repo disk check |

**One stale fact in KR's report (the "untracked" §7.6 doc) — and one apparent discrepancy that resolved, on full cross-repo reconciliation, to MY error not KR's.** I first-pass flagged `869c31b` as a phantom by checking only the collab repo's recent span against the engine build hash; the full disk check shows `869c31b` is the valid collab-repo Gate-2 finding gating engine build `5f85014`. Neither changes the acquisition verdict — but the discipline cut both ways this session: it caught KR's stale doc-status AND caught my own reconciliation slip before either reached a commit. That is the point: **prose reports — mine included — are hypotheses; disk is truth.**

## 2. The fit-for-purpose test (the decisive one)

An acquisition is not judged by tonnage — it is judged by whether the downstream work it exists to serve can now proceed. The chain is INTACT and LIVE on disk:

```
corpus acquired (136 FBX + 21 extracted)  →  slice verified (galadriel #2+#3 YES)
   →  §7.6 StyleProfile ruling fired (gandalf, efc29af)
   →  §7.2 restyle-leaf + accent system BUILT (rocket, engine 5f85014)
   →  keystone live-integration Gate-2 PASS (jack-ryan, engine 7a3cb6b)
```

The acquisition is not a pile awaiting use — it is **already load-bearing in a build that passed a gate.** That is the strongest possible fit-for-purpose signal. ACCEPT is earned, not granted.

(NOTE — I am NOT ruling on §7.2's conformance to my §7.6 ruling here; that is part of the engine run we await, and it routes through my endorse-criterion v2 § 2.5. I review §7.2-honors-§7.6 when the run returns. This ruling is on the ACQUISITION, and the acquisition's job — enabling the build — is demonstrably done.)

## 3. Design-sufficiency — the biome/lane coverage map

The corpus is not merely sufficient; it covers every axis the seasonal-journey ARPG needs, with redundancy where it matters most (the descent biome). Stratified by the design seams that consume it:

**Descent / dark-fantasy biome (the validated register-2 core — directly feeds the run-to-green descent I just closed):** Dark Fantasy, Dark Fortress, Dungeon Pack, Dungeon Realms, Dungeons Map, Dwarven Dungeon Map, Goblin War Camp — **7 dungeon packs**, multiply-redundant. This is the spine of a Diablo-class descent and it is the best-covered stratum. Horror Asylum/Mansion/Carnival sit adjacent (dark-fantasy-tonal).

**Fantasy overworld / hub:** Fantasy Kingdom, Fantasy Village, Fantasy Characters, Fantasy Rivals, Elven Realm, Ancient Empire, Knights — the town/sanctuary + civilized-zone register.

**Outdoor nature biomes (the open-zone analog of the dungeon problem):** Alpine Mountain, Arid Desert, Enchanted Forest, Meadow Forest, Swamp Marshland, Tropical Jungle, Snow Kit, Nature Pack — **8 explicit Nature-Biome packs.** Biome variety is inherent to the seasonal-journey structure; this stratum makes it real.

**The two StyleProfile lanes (the §7.6 ruling's substrate):** per-slot lane = **Modular Fantasy Hero Characters** (the 5-zone mask, galadriel-verified) + the **Sidekick** tool; silhouette lane = Adventure, Samurai/Samurai Empire, Vikings/Viking Realm, Pirate, Knights (whole-atlas named characters). Both lanes the ruling depends on are present and catalogued.

**Seasonal-rotation cultural variety (the atomic-substrate-registry's seasonal-substrate-rotation operator — Tolkien S1 → … → Aztec/Indo-Asian Sn):** Ancient Egypt, Samurai, Vikings, Pirate, Western. The cultural-register rotation has substrate.

**Weapon-corpus lane + loot:** Bow and Crossbow, Pride Crystal Weapons; Legendary Chest. (Weapon coverage is the THINNEST design-core stratum — flag for §4: the gear-spec weapon lane leans more on the 100k-corpus select+adapt path than on Synty, per the architecture record; Synty weapons are supplementary here.)

**Bestiary:** Boss Zombies, City Zombies, Werewolf, Kaiju, Goblin (War Camp + ANIMATION-Goblin-Locomotion).

**Cross-cutting load-bearing non-mesh strata:** ANIMATION (Base Locomotion, Sword Combat, Bow Combat, Goblin Locomotion, Idles, Emotes) — **the character lane is inert without these**; INTERFACE (Dark Fantasy HUD, Fantasy Warrior HUD, Fantasy Menus) — directly our UI register.

**Verdict on sufficiency:** the design-core is covered on every axis, descent-biome redundantly. Weapon-via-Synty is the one thin stratum, and that is BY DESIGN (weapons route through the corpus-adapt path). No gap blocks any design seam.

## 4. The consumption-time partition (next gandalf-owned step — sketched)

157 packs is the correct CORPUS and the wrong CONSUMPTION SET. The acquisition correctly crawled everything (no scope constraint — irreversibility demands completism). My seam now applies the **locked register + genre filter** that turns corpus → selectable design set. This is the catalogue-to-select-from discipline (gear-spec record § 3.6) at corpus scale. The partition:

**Filter 1 — visual register (the locked register-2 target prunes hardest):**
- **POLYGON line (~101 packs)** = the register-2 target (HD low-poly premium-lit; Dark Fantasy is the validated exemplar). **KEEP as the consumption line.**
- **POLYGON MINI (4 packs)** = register-DOWN (hyper-casual/mobile simplification). **SET ASIDE** — wrong register; retain in corpus only.
- **SIMPLE (37 packs)** = a different, flatter register entirely. **SET ASIDE** — wrong register; retain in corpus only.
- *Register filter alone removes ~41 packs from the consumption set without touching the corpus.*

**Filter 2 — genre (within the POLYGON line, fantasy-ARPG-core vs modern/event noise):**
- **DESIGN-CORE (~45-50 POLYGON packs):** the dungeon/fantasy/nature/character/cultural/weapon/bestiary strata enumerated in § 3.
- **OUT-OF-GENRE (retained, deprioritized):** City/Office/Casino/Coffee Shop/Nightclubs/Construction/Heist/Spy/Police/Racer×N/Quad Bike/Stunt Plane; Sci-Fi (City/Cyber/Space/Worlds/Outpost/Horror); Military/War/Battle Royale/Apocalypse; the entire holiday-event stratum (Easter/Halloween/Santa/Xmas/Gingerbread/Gnomes/Valentines/Pride/Celebrations); Kids/Dog/Frog Shrine/Hearse/Wheelchair/Farm/Town. These are NOT deleted — completism is preserved against a future season that might want them (a modern-isekai or apocalypse-season is not impossible) — but they are flagged out-of-current-register so downstream selection does not surface them.

**Cross-cutting KEEP regardless of the two filters:** ANIMATION (all 6 — the rig is inert without them) + the fantasy/dark-fantasy INTERFACE packs.

**What I commission from this partition (not authored here — the materialization):**
- **elrond:** tag each of the 157 packs in the catalogue with `{register: POLYGON|MINI|SIMPLE, genre_lane: design-core|out-of-register, seam: descent|overworld|nature|char-perslot|char-silhouette|weapon|bestiary|anim|ui|n-a}`. This is the substrate-half manifest the §7.6 ruling's consumers select against. Additive to the existing catalogue.
- This partition is a SKETCH (the filter LOGIC + the strata). Exact per-SKU assignment is elrond's catalogue work; I own the filter intent + the register lock.

**This does NOT block anything currently building.** The §7.2 build consumes the Modular Fantasy Hero slice, which is unambiguously design-core; the partition sharpens future selection, it does not gate the in-flight work.

## 5. Disposition of the two open items

**(1) Cloud backup — HIGH design-weight RECOMMENDATION (Matt-authorized; I do not authorize).** The corpus is now a load-bearing design dependency for the ENTIRE Track-B pipeline (gear-spec system, the seasonal-biome-variety requirement, the character lanes) AND it is IRREPLACEABLE (subscription-gated; lapse closes the door). From the design-steward chair I assign this the highest priority among the workstream's open items — the asymmetry is stark: backup cost is trivial, loss cost is a re-acquisition that may be impossible. **But the authorization is yours** (ADR-006 external write). My role is to weight it, and I weight it heavily: this is the kind of irreversible-loss exposure that warrants firing the backup at the next clean moment rather than deferring it against a lapse window whose timing I do not control.

**(2) My §7.6 ruling doc "untracked" — already resolved.** Committed at `efc29af`. KR's flag was a stale parallel-session read. No action; record corrected (§ 1). The downstream that "depends on it" (rocket §7.2) is correctly building against the committed ruling.

## 6. Verdict + what I own next

**ACQUISITION RUN: ACCEPT.** Complete, sound, design-sufficient with descent-biome redundancy, and proven fit-for-purpose by a downstream build that already passed a gate. The completist scope was the right call against irreversibility.

**gandalf owns next (none blocking):**
- The consumption-time partition (§ 4) → commission elrond to tag the catalogue by register + genre-lane + seam. (Track-B adjacent; not in the engine run's critical path.)
- The §7.2-honors-§7.6 conformance review (v2 § 2.5) — when the engine run returns.
- The Synty weapon-lane thinness note (§ 3) — confirm the weapon path leans corpus-adapt not Synty, when the gear-spec weapon leaf is specified.

**Matt owns:** the cloud-backup authorization (§ 5) — weighted HIGH by design.

**Signed:** gandalf, 2026-06-17. Ruling rendered against disk; KR's one stale fact and my own one reconciliation slip both corrected in flight.
