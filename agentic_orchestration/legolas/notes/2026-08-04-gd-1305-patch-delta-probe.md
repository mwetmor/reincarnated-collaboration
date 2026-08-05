# GD v1.3.0.1 → v1.3.0.5 patch-delta probe — what moved under the EoR Warlord sitting

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-04 · **Mode:** A (analytical), read-only
**Commissioned by:** gandalf (story-and-design steward), KIT-CAL-2 lane
**Class:** evidentiary — primary-source extraction from the developer's own patch record
**Amends:** `legolas/notes/2026-08-01-eor-endgame-build-of-record.md` § 1.8 (patch-currency) and § 2.2 (GD Stash)
**Serves:** `gandalf/notes/2026-08-01-eor-warlord-playtest-directions-v3.md` (§ 1.1, § 2, § 6)
**Trigger:** Matt's client reports **v1.3.0.5 (x64)**; the corpus of record is pinned to the Edition-II
depot fetch of 2026-07-24 = **1.3.0.0** (`gandalf/notes/2026-07-24-gd-edition-II-cut-record.md`).

**Grading key:** **M** = MEASURED (verbatim from primary source) · **D** = DERIVED (inference, operator
stated) · **U** = UNRESOLVED.

---

## §0 — Headline

**The EoR Warlord build is untouched. The werewolf referent is not.**

Across all five hotfixes, the seven watched classes produce **exactly three** changes that reach this
sitting, and none of them is in the build:

1. **Zero touches on any Soldier or Oathkeeper skill, and zero touches on any devotion.** The
   1.3.0.4 `Class & Skills` section names three masteries — Demolitionist, Shaman, Berserker — and
   there is no `[Devotion]` section in any of the five patches. The 1.3.0.0 tailwinds the fixture
   rests on (EoR weapon scaling to 39%/50%; monster armour −17% / armour absorption −20%) are
   **intact at 1.3.0.5**. § 2.
2. **The endgame windows survive.** W1 (SoT, Ultimate, L100) and W2 (Crucible, Gladiator, waves
   150–170) take one Crucible change between them, and it is at **wave 200** — outside the window.
   § 2.4, § 2.5.
3. **The werewolf referent moved twice, materially.** 1.3.0.1 reduced boss health at **levels 1–35**
   — the referent is L13 — and 1.3.0.4 ran a second early-game boss pass plus **shrank the Werewolf
   and Wereraven hitboxes**. § 2.7.

**And one thing the commission did not ask for, which is the largest finding here.** The 2026-07-26
Primordian capture that our own HP-table re-grade is built on was taken **~16 hours after v1.3.0.1
went live**, against a `.arz` pinned at 1.3.0.0. v1.3.0.1's one-line `Reduced Boss health at levels
1-35` is the same shape, sign, and level band as the **unexplained −15.000 pp boss-only constant**
that re-grade had to introduce to reconcile the model with the pixels. **This is a hypothesis, not a
finding** — but it is testable, and the test is an Edition-III cut. § 4.

---

## §1 — The version record, and a gap in it

| Patch | Live | Primary source | Steam mirror | Notes length |
|---|---|---|---|---|
| **v1.3.0.1** Hotfix 1 | 2026-07-25 23:37 UTC | Zantai, forum **155979 #88**, also folded into the OP | [announcement](https://steamcommunity.com/games/219990/announcements/detail/674001285755701848) (marketing wrapper only) | 2,714 chars |
| **v1.3.0.2** Hotfix 2 | ~2026-07-27 | Zantai, folded into **155979 OP** only — never a standalone post | **NONE** | 78 chars |
| **v1.3.0.3** Hotfix 3 | ~2026-07-29 | **NOT POSTED BY CRATE ON THE FORUM.** Relayed by user `Metalhead`, **155979 #137**, sourced "Steam forum" | **NONE** | 1 line |
| **v1.3.0.4** | 2026-07-31 21:12 UTC | Zantai, forum **157189 #1** | **NONE** | 6,353 chars |
| **v1.3.0.5** | 2026-08-03 18:26 UTC | Zantai, prepended to **157189 #1**; also #119 | [announcement](https://steamcommunity.com/games/219990/announcements/detail/717912016810936266) (wrapper: *"For the full list of changes, stop by the forums"*) | 244 chars |

**M — The secondary mirror is not a mirror.** Steam carries announcements for **only** 1.3.0.1 and
1.3.0.5, and both are marketing copy that defer to the forum. There is no Steam news post for
1.3.0.2, 1.3.0.3, or 1.3.0.4.

**M — 1.3.0.3 has no Crate-published notes anywhere we can reach.** Forum user `Sir_Mac`, 155979
#135, 2026-07-29, verbatim: *"Excuse me, what is the 'hotfix #3' (judging by the game version
1.3.0.3) about? There is no mention about it here in this very topic!"* Zantai never answered. The
only text that exists is `Metalhead`'s relay (#137) of a Steam *discussion-forum* post:

> **V1.3.0.3 Hotfix 3** / [Tech] / *"Added new Steam Deck/Linux compatibility launch option."*

**Confidence: tertiary.** Consistent with the 1.3.0.1/1.3.0.2 tech-only pattern and uncontradicted in
208 subsequent posts, but it is a community relay and is graded as such. **U-P1.**

---

## §2 — Per-patch change table, restricted to the seven watched classes

"**no touches**" below means: the full patch text was grep-swept for every term in the class
(skill names, devotion names, `Armor|Absorption|Defensive Ability|Offensive Ability|Retaliation|
Physical Resist`, `Crucible|wave|Tribute|Blessing|Banner|checkpoint|tier`, `Torment|hero|Champion|
spawn|density|Nemesis|ambush`, `save|\.arz|database|Modding|format|Stash`, `Werewolf|Wereraven|
Wereform|Berserker|Asterkarn`) and returned nothing in scope.

### 2.1 — v1.3.0.1 (2026-07-25) — source: [155979 #88](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979)

| # | Class | Verdict | Verbatim |
|---|---|---|---|
| 1 | Build's active skills | **no touches** | — |
| 2 | Devotions / procs | **no touches** | — |
| 3 | Global combat math | **TOUCHED (out-of-band)** | *"Reduced burst potential of some early game bosses at lower levels (ex. Queen Ravna, Zarthuzellan, Bonehunter, Yurra, Blackheart)."* · *"**Reduced Boss health at levels 1-35.**"* · *"Necromancer's Skeletons now have an additional 10% Life Leech Resist."* |
| 4 | Crucible | **no touches** | — |
| 5 | SoT / campaign density | **TOUCHED (out-of-band)** | *"Slightly reduced the base chance the Dread appears in Ascendant Mode and increased the minimum kills before it can spawn again…"* · *"Fixed an issue where the Source of the Corruption Kurn Channelers would not all respawn…"* |
| 6 | Save format / modding | **no touches** — no `[Modding]` section exists | — |
| 7 | Werewolf / transformation | **TOUCHED** | *"Fixed an issue where **Werewolf and Wereraven forms could results in crashes in Multiplayer**."* · *"Fixed an issue with some **inconsistent behavior in Werewolf and Wereraven animations, in regards to whether they hit with the main hand or both hands**."* · *"Fixed an issue with controller hot slot toggle to only include one wereform bar per wereform."* |

**Class-3 note.** `Reduced Boss health at levels 1-35` is explicitly level-banded. It cannot reach W1
or W2 (both L100). It lands squarely on the L13 werewolf referent. Same for the named early-game
bosses — Ravna, Zarthuzellan, Bonehunter, Yurra, Blackheart are all Act-1/2.

### 2.2 — v1.3.0.2 (~2026-07-27) — source: [155979 OP](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979)

Complete patch text, verbatim and in full:

> **V1.3.0.2 Hotfix 2** — **[Tech]** — *"Updated the Steam SDK for compatibility purposes."*

| Class | Verdict |
|---|---|
| 1–7, all seven | **no touches.** |

### 2.3 — v1.3.0.3 (~2026-07-29) — source: [155979 #137](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979) (tertiary relay)

Complete patch text, verbatim and in full:

> **V1.3.0.3 Hotfix 3** — **[Tech]** — *"Added new Steam Deck/Linux compatibility launch option."*

| Class | Verdict |
|---|---|
| 1–7, all seven | **no touches.** |

### 2.4 — v1.3.0.4 (2026-07-31) — source: [157189 #1](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189)

| # | Class | Verdict | Verbatim |
|---|---|---|---|
| 1 | Build's active skills | **no touches.** `Class & Skills` names only **Demolitionist, Shaman, Berserker** | *"Quick Jacks: now reduces skill cooldowns by a flat amount instead of a %."* · *"Thunderous Strike: now reduces skill cooldowns by a flat amount instead of a %."* — neither is in the build |
| 2 | Devotions / procs | **no touches.** No `[Devotion]` section exists | — |
| 3 | Global combat math | **TOUCHED (out-of-band)** | *"A balancing pass has been performed on all early game bosses to bring them closer to their pre v1.3.0 tuning, **particularly at lower levels**. Bosses with high burst potential in particular should be much more manageable."* · *"A balancing pass has been performed on Fangs of Asterkarn enemies, **particularly at low levels**… Some bosses have received **additional Normal/Elite variants to tune them independently of Ultimate/Ascendant**."* · *"Yurra Voideye, Drudd Blackheart and Chieftain Gruldir have had their burst potential reduced, particulaly at lower levels."* · *"The Dread's health has been reduced by ~12%."* · *"Slightly reduced the health of a certain Uber individual."* · *"Reduced Monster Healing by 25% in Ascendant Mode"* · *"Amplicorum and Saunginis potion modifiers now also boost **Retaliation** damage."* |
| 4 | Crucible | **TOUCHED — one line, outside the window** | *"**Grava'Thull is no longer a guaranteed spawn in the 200th wave of the Crucible.**"* — **nothing** on wave tuning, difficulty modifiers, tribute/blessing/banner costs, checkpoints, or tiers 18–20 |
| 5 | SoT / campaign density | **no touches on Steps of Torment or on hero/champion spawn rates.** Adjacent (out-of-band): | *"Increased Kill count for Nemesis re-spawns in Ascendant mode."* · *"Boss encounters that need to fully reset between attempts now have their boss arenas locked once the encounter begins…"* · *"Reduced the length of the Black Lodge special level in the Shattered Realm…"* |
| 6 | Save format / modding | **no touches.** No `[Modding]` section exists (1.3.0.0 had one). No save-format line anywhere | — |
| 7 | Werewolf / transformation | **TOUCHED — the biggest werewolf change in the series** | *"**Werewolf and Wereraven hitboxes have been shrunk down to match the human player form.**"* · *"Updated all Berserker and Wereform SFX from stereo to mono, to match skill SFX from prior expansions."* · *"Fixed additional inconsistencies with Werewolf and Wereraven animation hits."* |

**Class-3 note — the "independently of Ultimate/Ascendant" clause is the load-bearing one.** Crate
created **new Normal/Elite DB variants** specifically so the low-difficulty nerf would *not* touch
Ultimate/Ascendant. That is direct evidence that L100-Ultimate boss tuning survives 1.3.0.4, and
corroborating dev testimony exists — **Zantai, [157189 #82](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189), 2026-08-01**, verbatim:

> *"**The only real nerf to Ascendant was the Dread's health being slightly reduced.** The rest is
> fine-tuning rewards and repetition, where both the Dread and Nemesis bosses were spawning too
> often without boosting them in the altar."*

Neither the Dread nor the unnamed "certain Uber individual" appears in W1 or W2.

**Class-5 note — one unadjudicated community claim.** `Plague_Doctor`, 157189 #147, 2026-08-02:
*"did you remove the 'Chthonian ambushes' when looting random loot spots with patch 1.3.0.4? They
were consistently and frequently present in 1.3.0.0, but now they're GONE!"* **Single report, no
dev reply, no corroboration in 60 subsequent posts, and no patch-note line matches it.** Recorded as
**U-P2** because it is a campaign-*density* claim and W1 measures concurrency — but it concerns
loot-spot ambushes, not the scripted SoT floor-5 wave.

### 2.5 — v1.3.0.5 (2026-08-03) — source: [157189 #1 / #119](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189)

Complete patch text, verbatim and in full:

> **V1.3.0.5** — *"Fixed critical crash in the Frostveil Highlands."* · *"Fixed several text tag
> issues."* · *"Fixed broken bounty for Yura Voideye."* · *"Fixed missing cauldron in Ugdenbog."* ·
> *"Fixed inconsistent spawning of Aetherial and Aetherial Vanguard Nemesises."*

| # | Class | Verdict |
|---|---|---|
| 1 | Build's active skills | **no touches** |
| 2 | Devotions / procs | **no touches** |
| 3 | Global combat math | **no touches** |
| 4 | Crucible | **no touches** |
| 5 | SoT / campaign density | **TOUCHED, marginally** — *"Fixed inconsistent spawning of Aetherial and Aetherial Vanguard Nemesises."* Nemesis-tier only; no hero/champion rate change; SoT not named |
| 6 | Save format / modding | **no touches** |
| 7 | Werewolf / transformation | **no touches** |

### 2.6 — Cumulative roll-up, 1.3.0.0 → 1.3.0.5

| Class | Net delta to the sitting |
|---|---|
| 1 — Build's active skills | **ZERO.** Every 1.3.0.0 buff in probe § 1.8 (EoR 39%/50%, Soulfire, Judgment, Warborn Bastion) stands unamended |
| 2 — Devotions / procs | **ZERO.** No devotion section in any of the five. Maul / Ulzaad's Decree / Crab / Divine Mandate bindings unaffected |
| 3 — Global combat math | **Monster armour −17% and armour absorption −20% (1.3.0.0) survive untouched** — the tailwind that names Eye of Reckoning in its own patch note is intact. Boss-health +32%-at-L100 survives for W1. Changes are level-banded to 1–35, or Dread/Uber/Ascendant-specific |
| 4 — Crucible | **ONE change, at wave 200.** Waves 150–170 untouched. Checkpoints, tributes, blessings, banners, difficulty modifiers, tiers 18–20: no touches |
| 5 — SoT / campaign density | **ZERO on Steps of Torment.** No hero/champion spawn-rate change anywhere. One unadjudicated ambush claim (U-P2) |
| 6 — Save format / modding | **ZERO.** No `[Modding]` section and no save-format line in any of the five |
| 7 — Werewolf / transformation | **THREE changes across two patches** — hitboxes shrunk to human size, main-hand/both-hand animation-hit behaviour fixed twice, SFX stereo→mono |

---

## §3 — VERDICT

### V1 — Does any change require a new DECLARED CONFOUND in the v3 playtest directions?

**YES — but zero for W1 and W2, and the most urgent item is not a confound at all, it is a
stop-instruction that will now misfire.**

| ID | Target | Severity | Ruling |
|---|---|---|---|
| **C-1** | **v3 § 1 item 1** | **BLOCKING — fix before the sitting** | The instruction reads *"If Steam patched Grim Dawn after 2026-07-24, STOP and tell us before playing."* Steam has patched **five times** since. As written this halts the sitting on a condition that is already true and already adjudicated. **Replace with: "Write the version down. Expected: v1.3.0.5. If it reads anything OTHER than 1.3.0.5, stop and tell us."** The co-pinning rule survives; only its trigger needs re-aiming |
| **C-2** | **v3 § 6, werewolf referent** | **DECLARE** | *"The L13 werewolf referent is not comparable to the 2026-07-26 werewolf capture. Between them, v1.3.0.1 reduced boss health at levels 1–35 and reduced early-game boss burst; v1.3.0.4 ran a second early-game pass adding new Normal/Elite boss variants; and v1.3.0.4 shrank the Werewolf and Wereraven hitboxes to human size. Any TTK, boss-HP, or hit-rate comparison across the two sittings is confounded."* The hitbox change is the sharpest of the three: it alters the player's own collision volume and therefore incoming-hit rate |
| **C-3** | **v3 Part II / our side** | **DECLARE** | *"Client 1.3.0.5 vs corpus 1.3.0.0. Endgame kit and devotion joins are safe (zero deltas). Monster-HP joins below level 36, any Berserker/wereform record, and Crucible wave-200 spawns are NOT safe against Edition-II."* See V2 |
| **C-4** | **W1 / W2** | **NO CONFOUND NEEDED** | Both endgame windows are clean. This is a positive finding and should be stated as one — the fixture's whole premise (1.3.0.0 reversed the build's decay) is unamended at 1.3.0.5 |

### V2 — Re-fetch the `.arz` at 1.3.0.5 (an Edition-III cut) before sim-side joins consume the sitting?

**Ruling: 1.3.0.0 remains JOIN-SAFE for this sitting's data. Cut Edition III anyway — but for the
werewolf family, and cut it as an experiment rather than as housekeeping.**

**The `.arz` demonstrably moved.** 1.3.0.4 alone changes Dread health (−12%), monster healing in
Ascendant (−25%), boss records (new Normal/Elite variants), `Quick Jacks`, `Thunderous Strike`,
werewolf/wereraven hitboxes, four item records, and a Crucible wave-200 spawn table. Every one of
those is a DB record. **D — Edition-II's `database.arz` / `GDX3.arz` / `SurvivalMode3.arz` are all
stale at 1.3.0.5.**

| Join surface | Edition-II (1.3.0.0) status at 1.3.0.5 | Blocking? |
|---|---|---|
| Soldier / Oathkeeper skill records (the build's kit) | **SAFE — zero deltas** | no |
| Devotion records + proc bindings | **SAFE — zero deltas** | no |
| Monster HP / armour, **level ≥ 36**, Ultimate | **SAFE** — changes are level-banded or Dread/Uber-specific | no |
| Crucible wave tables, **tiers 15–17 (waves 150–170)** | **SAFE** | no |
| Crucible wave 200 spawn table (tier 20) | **STALE** — Grava'Thull no longer guaranteed | not for this sitting (v3 stops at 170) |
| Monster HP, **levels 1–35** | **STALE** — twice over (1.3.0.1, 1.3.0.4) | **yes, for the werewolf family** |
| Berserker / wereform records | **STALE** — hitbox geometry changed | **yes, for the werewolf family** |

**The reason to cut Edition III now is that it is a controlled experiment we can no longer run
later.** Our own `2026-07-28-kitcal1-hp-table-regrade.md` had to introduce a **−15.000 pp
boss-only constant** to reconcile the 1.3.0.0 chain with the measured Primordian pixels — trash and
champion tiers needed no correction at all. § 4 shows the capture post-dates v1.3.0.1 by ~16 hours,
and v1.3.0.1's one relevant line is `Reduced Boss health at levels 1-35`. **A 1.3.0.0-vs-1.3.0.5
record diff on the Primordian's `characterLifeModifier` either confirms that the constant is a real
patch delta or falsifies it and sends us back to the model.** Either result is worth the fetch. The
procedure is proven and additive (Edition-II was a 190 MB DepotDownloader run).

**Sequencing recommendation:** cut Edition III **before** the sitting's data lands, so the whole
KIT-CAL-2 corpus shares one pin — but do **not** hold the sitting for it. The sitting's own numbers
join safely against Edition-II today.

**Concrete first action, before any download:** re-enumerate the depot manifests and diff against the
Edition-II table in `gandalf/notes/2026-07-24-gd-edition-II-cut-record.md` § 2. That table's own
finding — *"identical manifests predict identical bytes… 11/11 IDENTICAL"* — means the manifest diff
tells us exactly which archives moved before a byte is fetched. **U-P3: not performed here.** No
`steamcmd` on this host, and SteamDB is Cloudflare-blocked to agent fetches. It is a Matt-side
authenticated step, same as the original fetch.

### V3 — Is GD Stash 1.8.2g safe on 1.3.0.5 saves?

**Ruling: VERIFIED — field-verified on 1.3.0.5 specifically, dated today. With three named operational
caveats that belong in v3 § 2.**

Four independent legs:

| # | Evidence | Grade |
|---|---|---|
| 1 | **The save format did not move.** No `[Modding]` section and no save-format line in any of 1.3.0.1–1.3.0.5. 1.8.2g's certification — *"Version 1.82 — Support for the GD 1.3.0.0 save file formats"* — is still the correct certification | **M** |
| 2 | **1.8.2g is still current.** `mamba`, [29036 #8578](https://forums.crateentertainment.com/t/tool-gd-stash/29036), 2026-07-26: *"Version 1.8.2g released"*. OP last edited 2026-07-26T03:21 UTC. Thread now at post 8,626 (last posted 2026-08-04T23:58 UTC) with **no later release announcement** | **M** |
| 3 | **Direct 1.3.0.5 field report — today.** `Tenzor`, [29036 #8625](https://forums.crateentertainment.com/t/tool-gd-stash/29036), 2026-08-04T23:06 UTC, verbatim: *"**I'm on GD 1.3.0.5 and using the latest build of GDstath 1.8.2g** I wanted to add a few skeleton keys, went to the crafting tab, picked the skelKey, Dragged into the stash, Saved the stash then went to stash transfer tab, saw the skelkey there and saved also the stash transfer… I'm missing something?"* — **and it was not a compatibility failure.** `mamba` #8626: *"they are automatically getting collected in the second tab of the in-game transfer stash where materials are being auto-collected"* | **M** |
| 4 | **No compatibility reports.** `mamba` answering in-thread continuously through 2026-08-04. Zero 1.3.0.4 or 1.3.0.5 incompatibility reports across the tail of the thread | **M** |

Leg 3 is worth naming precisely: **the exact operation v3 § 2 asks Matt to perform — grant a Skeleton
Key via GD Stash — was performed by a stranger on 1.3.0.5 fourteen hours ago, and it worked.**

**Caveats — all three belong in v3 § 2 as instruction text, not as risk language:**

| ID | Caveat | Source |
|---|---|---|
| **G-1** | **A granted Skeleton Key will not appear where Matt looks for it.** FoA's new dedicated Component / Crafting-Material stash pages auto-collect these items. *"they are automatically getting collected in the **second tab** of the in-game transfer stash where materials are being auto-collected"* — mamba #8626. Corroborated at #8593/#8594 (*"I kept putting a component into my stash and it would disappear… then I looked at the new component page in the stash and I had 100's of the thing"*). **Without this line, Matt will conclude GD Stash failed and abandon Path B mid-sitting** | 29036 #8593/#8594/#8626 |
| **G-2** | **The 1.3 update can silently re-enable Steam cloud save.** `minh_pham` #8589: *"Hmm cloud save is indeed turn on. Just turned it off."* `GIJW` #8587: *"Sometimes they do unfortunately."* mamba attributes the reported rename-wipes to cloud save, not the tool (#8621). **This strengthens v3 § 1.5 from a precaution to a re-check: verify cloud is off AFTER the client has patched to 1.3.0.5, not before** | 29036 #8585–8589, #8620/#8621 |
| **G-3** | **GD Stash cannot write the shared stash while a character is loaded in-world.** mamba #8598: *"you can have the game running too, you 'just' cannot have a character in game."* Slightly looser than probe § 2.2 step 8 (which said close GD Stash entirely) — but keep the stricter rule; it is a superset | 29036 #8597/#8598 |

**Out of scope, stated so it is not mistaken for a gap:** 1.8.2g does **not** support the new FoA
Ascended Affix mechanic. mamba, #8608, 2026-07-31: *"I am looking into the affix, have not decided
what to do with it yet… Chances are I will add it, but no estimate."* The build-of-record uses no
ascended affixes; irrelevant here.

---

## §4 — Unbilled finding: a three-way version skew on the werewolf family, and what it may explain

**This was not commissioned. It surfaced from the same patch record and it is larger than the brief.**

| Artifact | Version it actually reflects | Recorded? |
|---|---|---|
| `.arz` corpus (Edition-II, 2026-07-24) | **1.3.0.0** | yes, pinned |
| The 2026-07-26 Primordian / werewolf capture | **1.3.0.1 or later** (D) | **NO — the client version was never recorded** |
| The upcoming § 6 werewolf referent | **1.3.0.5** | will be, per C-1 |

**The derivation, stated so it can be attacked.** v1.3.0.1 went live **2026-07-25T23:37:01 UTC**
(Zantai, 155979 #88, `created_at`). The `play-test-v1` screenshot corpus that G-8 read carries
filesystem timestamps **2026-07-26 16:03 → 17:29** local on
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/`. Even at the most
conservative timezone reading, the session runs **after** the hotfix. Steam auto-updates by default.
**D, not M** — mtimes could be copy-times, and no version was written down. **U-P4.**

**Why it matters beyond bookkeeping.** `legolas/notes/2026-07-28-kitcal1-hp-table-regrade.md` § 0
records that the boss tier — and *only* the boss tier — needed a correction, and that the correction
*"is not a ratio — it is a constant… a flat **−15.000 pp** stage"*, while *"the trash and champion
tiers needed no correction at all"*. The G-5a ledger is Act 1, **Normal**, 1 player, level 12.

v1.3.0.1's relevant line, verbatim and complete: *"**Reduced Boss health at levels 1-35.**"

**Same tier selectivity (boss-only, trash unaffected). Same sign. Same level band.** That is four
independent agreements. It does not prove the constant is the patch — a flat −15pp additive stage is
a plausible modelling artifact too — but it means we currently cannot distinguish "our composition
model has a boss-tier bug" from "our DB is one hotfix stale." **The Edition-III diff separates them
in a single record lookup.** That is the strongest argument in V2, and it is why V2 says "cut it as
an experiment."

**Second-order consequence, flagged for gandalf, not ruled by me:** the 1.3.0.4 clause *"Some bosses
have received **additional Normal/Elite variants** to tune them independently of Ultimate/Ascendant"*
means the low-difficulty boss records the werewolf family joins against may now be **different
records**, not merely different values. A re-fetch would need to re-resolve identity, not just
re-read fields.

---

## §5 — Unverified / open

| # | Item | Why it matters | What closes it |
|---|---|---|---|
| **U-P1** | v1.3.0.3's notes exist only as a community relay of a Steam discussion post; Crate never published them on the forum | If 1.3.0.3 contained more than the launch option, this probe has a hole | A Crate-published source, or a Zantai reply to 155979 #135 |
| **U-P2** | `Plague_Doctor`'s claim that 1.3.0.4 removed Chthonian ambushes at random loot spots | A campaign-density change with no patch-note line; W1 measures density | Dev reply, corroborating report, or a `.arz` spawn-table diff at Edition III |
| **U-P3** | Whether depot manifests 219991 / 2699230 / 2699231 / 483840-2699231 actually moved since the Edition-II pin | Tells us which archives to re-fetch before spending a byte | Matt-side authenticated DepotDownloader enumeration; no `steamcmd` on this host, SteamDB Cloudflare-blocked |
| **U-P4** | The exact client version of the 2026-07-26 `play-test-v1` session | Determines whether the −15pp constant is a patch delta or a model bug | Nothing now closes it directly — it was never recorded. The Edition-III diff closes the *consequence* without closing the *fact* |
| **U-P5** | Whether the 1.3.0.4 "additional Normal/Elite variants" created new DB record IDs or re-tuned existing ones | Changes an Edition-III re-fetch from a value-refresh to an identity re-resolve | Edition-III record enumeration |
| **U-P6** | Whether GD Stash 1.8.2g can write `greatestSurvivalDifficulty` (carried forward from probe U-14, unchanged) | Only matters if the imported save's Crucible unlock state were ever missing | Char Editor inspection |

---

## §6 — Sources

**Primary — Crate Entertainment (developer-published)**

| Source | URL | Retrieved |
|---|---|---|
| Grim Dawn v1.3.0.0 + Hotfixes — thread OP carries **v1.3.0.2** and **v1.3.0.1** in full | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979 | 2026-08-04 |
| — Zantai #88, v1.3.0.1 Hotfix 1 announcement (`created_at` 2026-07-25T23:37:01Z) | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979/88 | 2026-08-04 |
| Grim Dawn v1.3.0.4 + v1.3.0.5 — thread OP, both patches (`created_at` 2026-07-31T21:12:18Z, `updated_at` 2026-08-03T18:26:30Z) | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189 | 2026-08-04 |
| — Zantai #82, scoping the 1.3.0.4 balance pass (*"The only real nerf to Ascendant was the Dread's health"*) | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189/82 | 2026-08-04 |
| — Zantai #119, v1.3.0.5 live on Steam | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189/119 | 2026-08-04 |
| Steam announcement — v1.3.0.1 Hotfix 1 (wrapper; defers to forum) | https://steamcommunity.com/games/219990/announcements/detail/674001285755701848 | 2026-08-04 |
| Steam announcement — v1.3.0.5 (wrapper; *"For the full list of changes, stop by the forums"*) | https://steamcommunity.com/games/219990/announcements/detail/717912016810936266 | 2026-08-04 |
| Steam news + events enumeration, appid 219990 — establishes **no Steam post exists for 1.3.0.2 / 1.3.0.3 / 1.3.0.4** | `api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=219990` and `store.steampowered.com/events/ajaxgetpartnereventspageable/?appid=219990` | 2026-08-04 |

**Tertiary — community relay (graded as such in §1)**

| Source | URL | Retrieved |
|---|---|---|
| `Metalhead` #137 — the only text of **v1.3.0.3**, sourced "Steam forum" | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979/137 | 2026-08-04 |
| `Sir_Mac` #135 — establishes Crate never posted 1.3.0.3 to the forum | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979/135 | 2026-08-04 |
| `Plague_Doctor` #147 — the unadjudicated Chthonian-ambush claim (U-P2) | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-4-v1-3-0-5/157189/147 | 2026-08-04 |

**Primary — GD Stash (tool author `mamba`, thread 29036, 8,626 posts, last posted 2026-08-04T23:58Z)**

| Source | URL | Retrieved |
|---|---|---|
| OP + changelog (last edited 2026-07-26T03:21:40Z) — *"Version 1.82 — Support for the GD 1.3.0.0 save file formats"*; download links still read **1.8.2g** | https://forums.crateentertainment.com/t/tool-gd-stash/29036 | 2026-08-04 |
| #8578 mamba — *"Version 1.8.2g released"* (2026-07-26); no later release post exists | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8578 | 2026-08-04 |
| **#8625 Tenzor / #8626 mamba — the 1.3.0.5 + 1.8.2g Skeleton-Key field report (2026-08-04)** | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8625 | 2026-08-04 |
| #8585–#8589, #8620/#8621 — cloud save silently re-enabled by the 1.3 update (G-2) | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8589 | 2026-08-04 |
| #8593/#8594 — FoA component pages auto-collect stashed items (G-1) | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8594 | 2026-08-04 |
| #8597/#8598 — no shared-stash writes with a character in world (G-3) | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8598 | 2026-08-04 |
| #8608 mamba — Ascended Affix support undecided, no estimate | https://forums.crateentertainment.com/t/tool-gd-stash/29036/8608 | 2026-08-04 |

**Internal — amended or consumed**

| Artifact | Path |
|---|---|
| Probe of record (§ 1.5 devotions, § 1.8 patch-currency, § 2.2 GD Stash) | `agentic_orchestration/legolas/notes/2026-08-01-eor-endgame-build-of-record.md` |
| Playtest spec of record (§ 1.1 stop-instruction, § 2, § 6) | `agentic_orchestration/gandalf/notes/2026-08-01-eor-warlord-playtest-directions-v3.md` |
| Corpus pin + manifest table (the V2 diff baseline) | `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-II-cut-record.md` |
| The −15 pp boss constant | `agentic_orchestration/legolas/notes/2026-07-28-kitcal1-hp-table-regrade.md` § 0 |
| L12 opposition ledger (Act 1, **Normal**, 1 player) | `agentic_orchestration/legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` |
| G-8 pixel ground truth (`play-test-v1` screenshot corpus) | `agentic_orchestration/galadriel/notes/2026-07-28-kitcal1-g8-death2-primordian-stats.md` |

**Blocked / not fetched**

- `steamdb.info` — Cloudflare challenge to agent fetches. Manifest history not obtained (U-P3).
- No `steamcmd` on this host; depot enumeration is a Matt-side authenticated step.
- `grimtools.com` — still robots-disallowed for `ClaudeBot` / `Claude-User`. Not fetched, not quoted.

---

**Signed:** legolas, 2026-08-04. The commission asked whether five hotfixes moved the ground under an
EoR Warlord sitting. For the sitting itself the answer is a clean no — the build takes zero touches
across all five, the armour cut that resurrected it is intact, and both endgame rooms are unchanged
inside the windows v3 plays. The one instruction that needs fixing is the stop-instruction, which as
written would halt the sitting on a condition that is now permanently true. What the sweep turned up
that nobody asked for is on the other half of the run: the werewolf referent has been patched twice,
including a hitbox change that alters the player's own collision volume — and the 2026-07-26 capture
we already graded against it was taken sixteen hours after a hotfix that reduced boss health in
exactly that level band, against a database pinned before it. Our unexplained −15 pp boss constant
and that patch line have the same sign, the same tier selectivity, and the same level band. That is
not proof. It is a testable coincidence, and the test is one record lookup in an Edition-III cut.
