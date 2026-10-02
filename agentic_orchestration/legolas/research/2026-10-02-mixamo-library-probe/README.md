# Research — Mixamo library probe for barbarian, sorceress and dark knight — 2026-10-02

**Mode:** A (analytical). Read-only. No logins, no FBX downloads.
**Commissioner:** gandalf (Run C-9 conductor), on Matt's question: *"Should I also gather Mixamo packs for the sorceress? How about other states like idle? Maybe we should run a research probe into the Mixamo library to plan?"* The coordinator added Matt's ruling R-C9-129 partway through: no jump, no free strafing, no universal dodge-roll. Each class gets its own movement skill (barbarian LEAP, dark knight BLITZ, sorceress TELEPORT). Strafes are needed only for locked-facing states.
**Author:** legolas (UNKNOWN-RESEARCHER). Access date for every source: 2026-10-01.

## Confidence key

Every claim carries one of these tags.

| Tag | Meaning |
|---|---|
| **[M]** | Checked against Mixamo itself: the public catalogue API that mixamo.com's Browse page uses, read without logging in. The API gives the name, the description, *supports In-Place*, *loopable* and the duration. |
| **[L]** | Checked locally against the Great Sword Pack that Matt downloaded (`~/Downloads/Great Sword Pack`, 51 FBX plus `X Bot.fbx`). I read the FBX headers only. Nothing was copied anywhere. |
| **[T]** | Read by eye from Mixamo's animated preview thumbnail (220x260 GIF). This is reliable for gross pose. It is moderate for which hand does what and for stance width. |
| **[1]** | Single secondary source. |
| **[I]** | My inference. |

---

## 1. What Matt should download, in order

**Short answer to Matt: yes, get packs for the sorceress, and yes, other states such as idles are worth gathering.** Mixamo currently offers **38 packs [M]**. Only 3 more are needed, plus about 40 single animations. The order below puts first the downloads that unblock the most work.

| # | Download | Count | For | Why it's at this position |
|---|---|---|---|---|
| 1 | **Pro Magic Pack** | 56 clips [M] | Sorceress, both loadouts | This is the only caster pack that has everything. It contains 1H casts (forward, upward, sweep), 2H casts (forward, sustained, area or ground, upward pull), an 8-way caster walk and run, a sprint, turn-in-place, 4 idles, 8 directional hit reacts, 4 directional deaths, and a block. **It is a strict superset of Magic Spell Pack, Lite Magic Pack and Magic Locomotion Pack [M, by product id]. Don't download those three.** |
| 2 | **Pro Melee Axe Pack** | 47 clips [M] | Barbarian (axe + shield, dual wield, signature moves) | The axe is in the **right** hand and the left hand is free [T]. It has idles with fidgets, a 4-way walk, a run forward and back, turn-in-place, 3 combos, a downward strike, a horizontal strike, a backhand strike, **360 High and 360 Low spin attacks**, **Battlecry**, **Chest Thump**, 3 hit reacts, block, draw and sheathe. It also has **Standing Melee Run Jump Attack, which is the barbarian LEAP**. It includes an unarmed locomotion and idle set as well. |
| 3 | **Pro Sword and Shield Pack** | 51 clips [M] | Barbarian axe + round shield | The shield is on the left forearm and the weapon is in the right hand [T]. It has guard locomotion, **walk and run strafes (needed for the locked-facing guard state)**, block start/idle/end, blocked and unblocked impacts, 2 deaths, Power Up, and turns. **It is a strict superset of Sword and Shield Pack (49) and Lite Sword and Shield Pack (17) [M]; the extra clips are the 2 draw clips. Pick "Pro".** |
| 4 | **Torch locomotion set** (singles, 16 clips, listed in § 3.2) | singles | Sorceress (wand + open book) | This is the only full locomotion set in the library with an object held up in the **left** hand. Its description reads *"Lighting Torch With Right Hand"* [M], and the thumbnails show the left forearm raised [T]. The gait was captured with the left arm not swinging, which suits a held book [I]. |
| 5 | **General-states singles** (§ 3.4) | ~22 clips | All three | Relaxed idles, stun, knockdown and get-up, deaths, victory and emotes, starts and stops. None of the weapon packs has starts or stops [M]. |
| 6 | **Barbarian and dark-knight singles** (§ 3.1, § 3.3) | ~12 clips | Barbarian, dark knight | Dual Weapon Combo, Two Hand Club Combo, Heavy Weapon Swing, Mutant Jump Attack, Roar, and the alternates for war cry and spin. |
| — | **Dark knight: download nothing first.** | — | Dark knight | Matt already owns its BLITZ clips and three unused upright idles in the Great Sword Pack (§ 3.3). Check those before downloading anything. |

**Don't download these:** Magic Spell, Lite Magic and Magic Locomotion packs (subsets of Pro Magic). Sword and Shield and Lite Sword and Shield packs (subsets of Pro). Locomotion, Basic Locomotion and Male Locomotion packs (unarmed jumps and strafes that R-C9-129 removes). Longbow, rifle and shooter packs. [M]

### 1.1 Download settings

| Setting | Use | Evidence |
|---|---|---|
| Format | **FBX Binary (.fbx)** | [L] The received clips are `Kaydara FBX Binary`, version 7700. |
| Frames per second | **30** | [L] FBX `TimeMode` = 6, which is eFrames30. The frame counts match Mixamo's durations at 30 fps. |
| Keyframe reduction | **none** | [1] This is what the C-9 ledger records for the Great Sword download. I can't see the dialog without logging in. |
| Skin | Pack: what Matt used before. The clips arrived **without skin**, plus one skinned character file (`X Bot.fbx`). Singles: **Without Skin**. | [L] The clip FBX has 0 Geometry nodes. `X Bot.fbx` has meshes and deformers. |
| Pose of the character file | **T-pose** | [1] The C-9 ledger records the T-pose option on the Great Sword download. |
| **In Place** | **Leave it OFF** so root motion is kept. | [L] The pack clips arrived **with** root motion. The ledger measured −1.74 m of hip travel on the backward run, which is how the lane caught it. Root motion is the cheapest test for a backward or mirrored clip, and the lane can strip it. For singles, the checkbox only appears where Mixamo says the clip supports In-Place. The tables below give that per clip [M]. |
| Mirror | Off by default. Use it only where a table says **"mirror"**. | [M] Every export request has a `mirror` parameter (`gms_hash.mirror`). [I] It is presented as a checkbox in the editor. Confirm it on screen. |
| Trim / Overdrive / Arm-Space | Defaults | [M] These are parameters in `gms_hash`. Arm-Space can widen arms for bulky characters. It may be worth trying on the barbarian [I]. |

**Packs are still downloadable as packs [M+L].** The public catalogue lists 38 `MotionPack` products, and Matt received the Great Sword Pack as a zip on 2026-10-01.

### 1.2 How a pack zip names its files (verified, and it matters)

**Rule:** inside a pack zip, each clip is named after its Mixamo name in lower case. The first clip with a given name has no suffix. Each later clip with the same name gets ` (2)`, ` (3)` and so on, **in the pack's own listing order**.

**Proof [L+M]:** I read all 51 durations from Matt's local Great Sword FBX headers. Each one matches the Mixamo API's duration for that pack position, within the 1-frame end-inclusive offset. That is 51 of 51. Under this rule, `great sword run.fbx` is Mixamo's *"Great Sword Bacward Run"* (Mixamo's own spelling) and `great sword run (2).fbx` is the forward run. That is exactly what the C-9 lane found by measuring hip travel.

**Consequence:** **the names don't tell you which clip is which; the descriptions do.** In Sword and Shield, `crouch block (2)` is a *Blocked Impact* and `crouching (4)` is an *Unblocked Impact* [M]. **Appendix A gives a decoder table for every recommended pack**: predicted file name, Mixamo description, In-Place support and length. For packs other than Great Sword, the numbering is the same rule applied by inference [I]. The lane can confirm any file by its duration.

**Backward clips with forward-sounding names:** `great sword run.fbx`, `great sword walk (2).fbx`, `sword and shield run (2).fbx`, `sword and shield walk (2).fbx` [M; the first is also L]. The axe and magic packs avoid this trap: their backward clips are explicitly named `… back` [M].

---

## 2. Licence and storage

Source: Adobe's community thread *"Mixamo FAQ: Licensing, Royalties, Ownership, EULA and TOS"*, posted by TylerG 3D on 2022-09-29 [1]. Adobe's own help pages (helpx) and Terms pages returned **HTTP 403** to every non-login fetch, so **I couldn't check this against Adobe's General Terms.**

- **Commercial game use: allowed.** The FAQ says: *"available for free, with no licensing or royalty fees, for unlimited commercial or non commercial use"*. Its "YES" list includes *"Video Games"* and *"DLC or Addon Content for Games"*. **No credit is required.**
- **Storing the files: allowed within the team. Redistributing the raw files: not allowed.** The FAQ says: *"The only thing you cannot do is distribute the raw character and animation files. This does not include collaborating on team-based projects… You may not distribute the files to customers or non-team members."* It also lists *"Any type of free distribution of character or animation raw files"* as a NO.
- **Machine learning is excluded.** The FAQ says: *"The only research application Mixamo content can't be used in is training machine-learning models."*
- **Price changes don't apply backwards.** The FAQ says: *"Your use … is covered under the terms at the time you use it."* It also calls Mixamo *"a limited duration technology preview"*.
- **Where our repos stand [L]:**
  - `reincarnated-collaboration` is **PUBLIC** (`gh repo view`). `reincarnated-godot` is private.
  - The raw FBX files are in `~/Downloads` and outside git.
  - In the public repo, `astra_test_01/.gitignore` ignores `*.glb`, `*.npz` and `*.blend`. No `.fbx`, `.glb` or `.pck` file under `C-9` is tracked.
  - **Risk [I]:** a retargeted clip is still animation data that can be extracted. `git add -f` of a retargeted `.glb` into the **public** repo would be arguably *"free distribution of animation raw files."* Keep retargeted clips out of public git. Shipping them inside a game build is game use, which the FAQ allows.

---

## 3. Per-character tables

Column key: **IP** = Mixamo says the clip supports In-Place [M]. **Len** = duration [M]. **Hand** and **Stance** come from the thumbnail [T] unless tagged otherwise. *Wide/crouched* means feet clearly wider than hips with bent knees. *Upright/narrow* means feet near hip width with straight legs. The id is the first 8 hex digits of Mixamo's product id, so the crawler can re-check any row.

### 3.1 Barbarian

#### (a) One-handed axe + round shield — Pro Sword and Shield Pack for the frame, Pro Melee Axe Pack for the signature moves

| Need | Mixamo clip (pack file) | IP | Len | Hand / stance | Conf. |
|---|---|---|---|---|---|
| Combat idle | Sword And Shield Idle (`sword and shield idle (4)`) | no | 2.53 | Weapon in right hand, shield on left. **Wide/crouched** guard. | M, T |
| Idle fidgets | Look Around Idle `idle`, Sword Play Idle `(2)`, Stretch Idle `(3)` (Sword And Shield) | no | 3.67 / 7.5 / 8.67 | same | M |
| Walk / run fwd | `sword and shield walk`, `sword and shield run` | yes | 1.07 / 0.70 | Upright guard walk, shield forward | M, T |
| Walk / run back | `sword and shield walk (2)`, `run (2)` — **BACKWARD** | yes | 1.23 / 0.53 | | M |
| Strafes (guard state) | `sword and shield strafe` … `(4)`: right walk, left walk, left run, right run | yes | 0.63–1.30 | | M |
| Turn in place | `sword and shield turn` (90 R), `turn (2)` (90 L), `180 turn` (walk), `180 turn (2)` (run) | no | 0.77–0.9 | | M |
| Block | Idle To Block · Block Idle · Block To Idle (`sword and shield block`, `block idle`, `block (2)`) | no | 0.57 / 1.37 / 0.67 | | M |
| Attacks | Downward Slash · Slash Combo (3.53 s) · Cross Slash · Power Slash · High Attack · Low Attack · Hilt Melee · Sparta Kick | no | 1.0–3.53 | Sword arcs. They fit an axe [I]. | M |
| **Axe signature attacks** (Pro Melee Axe) | Standing Melee Attack Downward · Horizontal (right to left) · Backhand (upward) · Combo Ver. 1/2/3 (2 or 3 hits) | no | 2.27–4.67 | Axe in right hand, **left hand free and hanging** [T]. Holding a shield needs a left-arm layer [I]. | M, T |
| War cry | **Standing Taunt Battlecry** (Pro Melee Axe) | no | 2.83 | Arms flung wide, head back [T] | M, T |
| War cry alt | Standing Taunt Chest Thump (axe banged on chest) · Sword And Shield Power Up | no | 2.83 / 2.37 | | M |
| Spin | **Standing Melee Attack 360 High** / **360 Low** (*"Left To Right Spin Attack With Axe"*) | no | 3.17 / 2.47 | One full turn, single (not looping) | M, T |
| Hit | Sword And Shield Blocked / Unblocked / Head Impact · Axe React Large From Left / Right / Gut | no | 0.7–1.77 | | M |
| Death | Sword And Shield Falling Back Death / Falling Forward Death | no | 2.27 / 3.9 | | M |
| **LEAP** | **Standing Melee Run Jump Attack** (*"Running Jump With Attack With Axe"*, Pro Melee Axe). Alternative: Sword And Shield Jump Attack (lands kneeling). | no | 3.67 / 2.3 | The axe is swung **two-handed overhead** in the slam [T], so the free hand leaves the shield. | M, T |

#### (b) Dual wield: sword in the main hand, axe in the off hand

**Finding: Mixamo has NO coherent dual-wield set [M].**
- I swept all 2,444 of the 2,446 catalogue motions plus server-side searches for "dual" and "two weapon".
- The only dual-weapon clip is **Dual Weapon Combo** (*"Dual Weapon Combo Attack"*, id `c9cdb1c3`, 3.63 s, not In-Place). It is a single attack chain in a **wide/crouched** stance, from the same armoured-knight capture family as One Hand Sword Combo and Two Hand Club Combo [T].
- No dual-wield idle, walk, run, hit or death exists.
- The other "dual" hits are cards, dice and pistols [M].

**Best assembly [I]:**

| Need | Use | Notes |
|---|---|---|
| Idle, walk, run, turns, hit, death | **Pro Melee Axe Pack** locomotion | The main hand is right [T]. The off-hand weapon hangs from the free left hand. |
| Main-hand attacks | Pro Melee Axe attacks, One Hand Sword Combo (`c9cdaeb2`, 4.53 s), Stable Sword Inward / Outward Slash (`c9c72f80`, `c9c7303c`, ~2.0 s, *"standing stable"*) | Each is one-handed. |
| Off-hand attacks | The same attacks exported with **Mirror** | The left hand leads in the mirrored clip. Mirror the whole clip, then let the lane decide whether to layer arms only [I]. |
| Two-weapon flourish | **Dual Weapon Combo** | Not In-Place |
| Spin | 360 High / Low | The free arm swings wide [T]. An off-hand weapon would read as a two-weapon spin [I]. |

**Missing:** a dual-wield idle, dual-wield locomotion, an alternating left-right attack chain, a dual block, and a dual war cry.

#### (c) Two-handed maul — Great Sword Pack (owned) covers it

Better or extra heavy 2H options [M; thumbnails T]:

| Clip | id | Len | Notes |
|---|---|---|---|
| **Two Hand Club Combo** | `c9cdb104` | 5.4 s | 2H overhead club combo. Wide stance. Same capture family as Dual Weapon Combo. |
| **Heavy Weapon Swing** | `c9c789d5` | 5.03 s | *"Two Handed Heavy Weapon Swing"*. Big horizontal wind-up. |
| Bash | `c9c87a20` | 4.17 s | *"Overhead Bashing Swing"*. Upright, near-narrow stance. |
| 2hand Idle | `c9c87b9c` | 2.5 s | *"Two Handed Weapon Stance"*. Hands together at the hip. Wide. |
| **Standing Melee Run Jump Attack** (Pro Melee Axe) | `c9cedc5b` | 3.67 s | Two-handed overhead slam. **LEAP for the maul too.** |
| Great Sword Jump Attack From Run (owned) | `c9cc8bd6` | 2.17 s | LEAP alternative for 2H |

**Whirlwind / spin:** Mixamo has **no looping whirlwind or spin-to-win clip**. The keyword sweep for spin/whirl/twirl/360/tornado found only these single spins:
- Great Sword High Spin Attack From Run (owned, 1.87 s)
- 360 High and 360 Low (axe)
- Spin In Place (a casual spin, not a combat spin [T])

A spin that moves needs a looped mid-spin segment plus procedural yaw over a lower-body walk [I].

**Shouts / war cries / power-ups:**

| Clip | id | Len | Notes |
|---|---|---|---|
| Standing Taunt Battlecry (axe) | | 2.83 | |
| Roar | `c9c79f59` | 6.23 | *"Belting Out A Load Roar"*. Crouch-forward roar, unarmed. |
| Mutant Roaring | `c9ccb4c2` | 5.4 | Monster: very wide and hunched |
| Yelling Out | `c9c91437` | 4.27 | *"Stepping Forward And Yelling Out"* |
| Standing Yell | `c9cb7b9a`, `c9cb7a15` | 4.07 | *"Short Yell While Standing"*, 2 variants |
| Yelling | `c9c6fcc0` | 8.07 | *"Yelling In Anger"* |
| Taunt — Flexing Muscles | `c9c706d2` | 3.97 | |
| Great Sword Power Up | (owned) | | |
| Sword And Shield Power Up | | | |

**Brute locomotion alternates, unarmed, In-Place capable:**
- Orc Walk (*"Male Orc Walk Forward"*, `c9cd254a`, 1.2 s)
- Walking (*"Male Brutal Walk"*, `c9c60a8c`, 1.4 s)
- Mutant Walking and Mutant Run (`c9c93a8c`, `c9c93cdc`)

**LEAP without a weapon:** Mutant Jump Attack (*"To Ready Pose"* `c9c95cf0` / *"To Idle"* `c9c95db7`, 1.4 s). It is a leap that lands in a two-fist slam, wide and brute [T]. Hard Landing (`c9c99c82`, 2.5 s) can serve as a landing tail [M].

### 3.2 Sorceress

#### Pro Magic Pack — what it gives [M; pose T]

**Read this first — the posture [T]:**
- Every Pro Magic clip uses a stylised "spell-ready" posture: the **right hand is raised palm-up at head height**, the left hand is low and clawed, and the knees are bent in a **wide/crouched** stance. This holds through idle, walk and run.
- With a wand this may read well, because the wand is held up.
- It is a **style risk in the same family as the barbarian stance width issue**. It may look crouched against an upright sorceress [I].

| Need | Clip | IP | Len | Hand / notes |
|---|---|---|---|---|
| Caster idle | Standing Idle (*"Ready To Cast Spell"*) | no | 1.87 | Wide/crouched |
| Idle fidgets | Standing Idle 02 (looking around) · 03 (*"Playing With Magic"*) · 04 (*"Windup… And The Pitch… BOOM"*) | no | 5.17 / 11.4 / 7.43 | |
| Walk / run / sprint | Standing Walk Forward / Run Forward / Sprint Forward | yes | 1.13 / 0.73 / 0.57 | The right hand stays raised [T] |
| Back + strafes | Standing Walk Back · Run Back · Walk Left/Right · Run Left/Right | yes | | Use strafes only for the locked-facing channel state (R-C9-129) |
| Turn in place | Standing Turn Left 90 / Right 90 | no | 1.83 / 1.63 | |
| **Fire Ball (projectile)** | **Standing 1H Magic Attack 01** (*"One Handed Casting Spell Fowards"* [sic]) | no | 2.27 | Looks like the **right** hand thrown forward with about a 90° body turn to the left [T, low]. Preview it, and use Mirror if it is left. Wide lunge. |
| **Meteor (sky cast)** | **Standing 1H Cast Spell 01** (*"One Handed Casting Spell Upwards"*) | no | 2.27 | **Right** arm straight overhead [T]. The left arm stays low and slightly out, so it fits the book better than the others [T]. |
| Sweep casts | 1H Magic Attack 02 (sweep right to left, deep lunge) · 03 (upward sweep) | no | 2.2 / 2.27 | 03 is right-handed [T]. 02 swings both arms wide [T]. |
| Channel (2H) | 2H Magic Attack 03 / 04 (*"Forwards Sustained"*) | no | 4.3 / 3.3 | Both hands, so **only for the staff loadout** |
| Sky / area (2H) | 2H Cast Spell 01 (*"Upward Pull"*, both arms overhead) · 2H Magic Area Attack 01 (*"Towards Ground"*, drops to one knee) · Area Attack 02 (*"Pull In Blast Out"*) | no | 2.13 / 2.93 / 3.23 | Staff loadout |
| Buff (2H) | 2H Magic Attack 05 (*"Pull Up And Clap Hands"*) | no | 3.53 | Staff loadout |
| Hit | React Small and Large × Front/Back/Left/Right (8 clips) | no | 0.97–1.67 | |
| Death | React Death Backward / Forward / Left / Right | no | 3.5–3.67 | |
| Block | Block Start / Idle / React Large / End | no | | *"Blocking With Both Arms Out"* |

#### (a) Great staff, two-handed caster

**Finding: Mixamo has no staff pack and no staff locomotion [M].** A search for "staff" returns two clips: *"Smash With Back Of Rifle Or Staff"* and *"Body Spin On Staff Tip"* (acrobatic).

**Plan [I]:**
- Use **Pro Magic Pack** throughout. Hold the staff upright in the raised right hand during idle and locomotion; that pose naturally grips a vertical staff [T].
- Use the **2H casts** for channel, area and sky casts.
- **Already owned:** Great Sword Pack's `great sword casting` (*"Great Sword Spell Casting"*, 4.77 s) and `spell cast` (*"Spell Casting With A Two Handed Sword"*, 1.10 s). These are two-handed-weapon casts with a real grip [M]. They are worth testing for a two-hand staff thrust.

#### (b) Wand in the right hand + open spellbook in the left hand (1H casting essential)

**Finding: no wand, book or reading-while-walking clip exists [M].** Searches for "wand" and "book" match unrelated clips. "Reading" returns 4 clips, none standing and none walking.

**Plan [I]:**
- **Casts:** Pro Magic **1H Cast Spell 01** (Meteor), **1H Magic Attack 01** (Fire Ball; check the hand), **1H Magic Attack 03**, and the singles below.
- **The left arm needs an arm-only override layer holding the book in every clip.** No Mixamo cast keeps the left arm still. Even the "1H" casts move it [T].

| Need | Clip | id | IP | Len | Notes |
|---|---|---|---|---|---|
| Buff cast | **Magic Heal** (*"Casting A Healing Spell With One Hand"*) | `c9c80212` | no | 2.83 | **Right** hand pushed out with a body turn [T, moderate] |
| Buff / summon | Spell Casting (*"Casting A Ressurection Or Summon Spell"*) | `c9c80157` | no | 4.17 | |
| 1H cast | Magic Spell Casting (*"Casting A Spell With One Hand"*) | `c9c802f0` | no | 4.17 | Hand: check in preview |
| Channel, 1H | **No dedicated 1H channel exists [M].** Hold the extended frame of 1H Magic Attack 01 or Magic Heal and loop it [I]. | | | | |
| Book-hand locomotion | **Torch set**: Standing Torch Idle 01–04 · Walk Forward/Back/Left/Right · Run Forward/Back/Left/Right · Turn Left/Right 90 · Turn Left/Right 180 · Walk Forward Stop · Run Forward Stop | e.g. `e8c2c8c3`, `0d90567f`, `b5b82299` | walk/run yes | 0.6–9.3 | **The torch is in the LEFT hand** [M desc + T]. The left forearm is raised with the fist at shoulder height. A book would sit lower, so the override is still needed. **Upright/narrow, female-styled gait** [T]. |
| Book-hand alt | Holding Idle / Holding Walk / Holding Turn Left / Right (*"Holding An Object…"*) | `c9cda11a`, `c9cda1e7`, `c9cda2af`, `c9cda378` | walk yes | 6.0 / 1.37 | One arm bent at the waist [T, low]. Preview it. |
| Upright female locomotion | **Female Locomotion Pack** (10: feminine walk, run, walk and run strafes, turns, idle) · Female Walk `c9c68b91` · Female Run Forward `c9ccfb22` · Female Walk Backwards `c9ccf998` · Female Start / Stop Walking `c9c68c4c` / `c9c68d24` | | yes | | Upright/narrow [T]. Use these if the Pro Magic crouch is rejected. |
| **TELEPORT** | **No teleport, blink or vanish clip exists [M]** ("teleport" and "vanish" both return 0). Quick 1H gestures, best first: **1H Magic Attack 01**, trimmed to the thrust · **Magic Heal**, trimmed · Dismissing Gesture (*"Dismissing With Back Hand"*, `c9c8f19f`) · Angry Point (*"Quickly Pointing Angrily Forward"*, `c9c916ce`) | | no | 2.2–2.4 untrimmed | All are right-hand. The gesture needs about 0.3–0.5 s under the VFX [I]. |

### 3.3 Dark knight — gaps only (Great Sword Pack is already owned)

| Gap | Recommendation | Conf. |
|---|---|---|
| **Upright idle** | **Check the owned clips first.** `great sword idle (4)`, now in use, is Mixamo's *"Great Sword Admiring Idle"* [L+M]. Three unused idles are already on disk: `(2)` Look Around Idle (3.70 s), `(3)` Strike A Pose Idle (3.63 s), `(5)` Look Around Idle, long version (7.53 s) [M]. If all of them lean, take an **upright/narrow unarmed lower body** from Breathing Idle `c9c6d0d5` (8.67 s), Neutral Idle `c9c80e28` (4.17 s) or Standard Idle `c9cccb71` (3.0 s) and layer the great-sword arms over it. All three are upright/narrow [T]. 2hand Idle `c9c87b9c` is wide. | M, L, T, I |
| **Spin while moving** | No looping spin exists. The best 2H source is **Great Sword High Spin Attack From Run** (owned, 1.87 s). Use the owned **Great Sword strafes** (`strafe` … `(4)`) as the lower body for the locked-facing spin state (R-C9-129) [I]. | M, I |
| **War cry** | **Already in use:** `great sword power up` stands in as the war cry (C-9 ledger) [L]. Alternatives: Roar `c9c79f59`, Yelling Out `c9c91437`, Battlecry (axe, one-handed) | L, M |
| **BLITZ** (charge or dash with weapon impact) | **Owned:** `great sword run (2)` (forward run) into **Great Sword Jump Attack From Run** (2.17 s), **Low Slide Attack From Run** (2.1 s) or **High Spin Attack From Run** (1.87 s). All three are built to start from a run [M]. Nothing extra is needed. Running To Tackle (`c9cc27cd`) is an American-football tackle dive [T]; it is not suitable. | M, T |
| Naming note | `great sword slash (3)`, the chosen attack, is Mixamo's *"Great Sword Low Slash"*. `great sword attack` is *"Great Sword Hilt Melee"* [L+M]. Both are consistent with what the lane measured. | L, M |

### 3.4 General states (all three)

| State | Weapon-pack source | Unarmed singles (In-Place / Len) [M] | Notes |
|---|---|---|---|
| Combat idle | Each weapon pack's idle | Ready Idle `c9c6b803` (fists up) | |
| **Relaxed idle** | — | **Breathing Idle** `c9c6d0d5` (8.67) · **Neutral Idle** `c9c80e28` (4.17) · Idle *"Standing Idle"* `c9c972d1` (8.33) · Female Idle `c9ccf750` (10.0) | Upright/narrow [T] |
| Idle fidgets | Pack look-around and stretch idles (see the tables above) | Weight Shift `c9c908f7` (9.4) · Looking Around `c9c6cdf7` (5.07) · Warrior Idle *"Warrior Stretching Idle"* `c9c72bad` (11.67) · Bored `c9c79d1f` (4.9) | |
| Relaxed ↔ combat | — | Standing Idle To Fight Idle `c9cce7b7` · Fight Idle To Standing Idle `c9cce97f` · Standing Idle To Action Idle `c9cce89d` (about 1 s each) | |
| Turn in place | Every pack has 90° turns. Sword and Shield and Great Sword also have 180° turns. The torch set has 90° and 180°. | Left / Right Turn *"Standing Left/Right Turn"* `c9c9841d` / `c9c98676` (1.17) · Quick 180 Turn `c9c8c959` (1.3) | |
| Strafes | **Only for locked-facing states** (R-C9-129): barbarian guard (Sword And Shield strafes), dark-knight spin-move (Great Sword strafes, owned), sorceress channel-move (Pro Magic Walk Left/Right) | — | |
| **Starts / stops** | **No weapon pack has starts or stops [M]**, except the torch set's Walk Forward Stop and Run Forward Stop | Start Walking `c9c8b661` (2.9) · Stop Walking `c9c8d966` (3.0) · Female Start / Stop Walking (1.87 / 1.53) · Run To Stop *"Fast Stop From Full Run"* `c9c9a5a7` (0.9) | Unarmed. The arms need the weapon layer [I]. |
| **Stun** | — | **Dizzy Idle** *"Rocking Back And Forth As If Dizzy"* `c9c69efe` (4.27, loop) | Upright [T] |
| **Knockdown → get-up** | — | **Falling Down** *"Knocked Over And Falling To The Ground"* `c9c91079` (2.27) → **Getting Up** *"From Being Knocked Down On The Ground"* `c9c90823` (2.7). Also Knocked Down (to stomach) `c9c8a565` (2.77) → Getting Up From Stomach `c9c71f39` (6.67, long) · Sweep Fall `c9c7f722` (2.33) · Kip Up `c9ca7e66` (2.0, acrobatic) | The `c9c91079` + `c9c90823` pair is the shortest round trip [I] |
| Hit (generic) | Pack reacts | Big Stomach Hit `c9cafc81` · Reaction left / right side `c9c60e0e` / `c9c60d2e` · Head Hit (9 variants) | |
| Death (generic) | Pack deaths | Falling Back Death `c9cdb348` (2.17) · Flying Back Death `c9cdb4c8` (3.0) · Death From Standing Idle `c9c899a0` (3.0) | |
| **Victory / emotes** | Great Sword *"Strike A Pose Idle"* (owned) | **Victory** *"Celebrating After A Win"* `c9c714c2` (6.67) · **Cheering** *"Two Fists Pump"* `c9c66dfd` (2.9) · Fist Pump `c9cb6ccd` (1.93) · Standing Fist Pump `c9cb708b` (3.73) · Victory Idle ×3 (`c9cd9927` / `c9cd953a` / `c9cd9162`, about 1.8 s loops) · Taunt Flexing `c9c706d2` | Victory Idle variants are named after Mixamo stock characters ("Aj", "Big Vegas", "Sporty Granny") |
| Jumps | **Not needed** (R-C9-129). Every weapon pack contains jumps. Ignore them. | — | |

---

## 4. Gaps and risks

1. **Dual wield is the biggest gap.** There is one dual attack (Dual Weapon Combo) and nothing else [M]. Off-hand moves need **Mirror** exports, and dual locomotion has to be assembled from one-handed sets [I].
2. **There is no staff, wand or book content** [M]. The sorceress depends on an **arm-only override layer** (left arm holding the book) on top of every clip, including the "1H" casts, because their off arm moves [T].
3. **The Pro Magic posture is a style risk.** The whole pack is wide/crouched with the right hand raised [T]. Under an upright sorceress it may read as hunched. This is the same kind of issue that led to the barbarian stance ruling [I]. The fallback is upright female locomotion plus Pro Magic casts.
4. **No looping spin and no teleport** [M]. Both must be built (loop a segment plus procedural yaw; a short gesture under VFX) [I].
5. **Clips from different capture families mixed on one character** will show different stance widths and arm-space [T]. The armoured-knight combo family (Dual / Two Hand Club / One Hand Sword) is wide and crouched; Bash and the idles are upright [T].
6. **Hand-of-cast readings are from 220x260 thumbnails** [T]. They are moderate confidence for Magic Heal and 1H Cast Spell 01, and **low for 1H Magic Attack 01**. Preview each clip on Mixamo before downloading, and set Mirror if the cast is left-handed.
7. **Duplicate names will mislead.** Use Appendix A. Keep **In Place OFF** so the lane can catch a backward clip by its root travel [L].
8. **Licence is checked against one secondary source only** [1]. The Adobe helpx and Terms pages were 403. Matt can read the official FAQ while logged in. **The public repo must never take a retargeted `.glb` by `git add -f`** [I].
9. **Mixamo calls itself a "limited duration technology preview"** [1]. Terms are locked at the time of use, but availability isn't guaranteed. Download what the plan needs now rather than later [I].
10. **Catalogue coverage is 2,444 of 2,446** [M]. Two motions were lost to unstable API page ordering; server-side keyword searches back-filled everything I looked for. Any clip that doesn't contain the searched words could be in that gap of 2.

## 5. Knowledge gaps not resolved

- **The exact pack-download dialog options** (whether it offers an In-Place choice, and what the default skin is). They can't be seen without logging in. The settings above are reconstructed from Matt's received files plus the ledger.
- **Whether Mirror is shown as a checkbox in the editor** (the API parameter is confirmed).
- **Which hand casts in 1H Magic Attack 01**, Magic Spell Casting and Spell Casting (thumbnail resolution).
- **Adobe's General Terms text for Mixamo** (403).

## 6. Method and sources

- **Mixamo public catalogue API** (the endpoint behind mixamo.com's Browse page, no login): `https://www.mixamo.com/api/v1/products?type=MotionPack|Motion&query=…` and `…/api/v1/products/<id>?similar=0`.
  - All 38 packs with full clip lists.
  - 2,444 of 2,446 motions, from 26 listing pages plus 92 keyword searches.
  - About 470 detail records (In-Place, loop, duration, `gms_hash` export parameters).
  - Polite rate: about 1 request per second, with backoff. I found no `robots.txt` (404).
- **Mixamo animated thumbnails** (`d99n9xvb9513w.cloudfront.net/thumbnails/motions/<n>/animated.gif`). About 60 clips viewed as frame strips for hand and stance.
- **Local:** `~/Downloads/Great Sword Pack`. FBX headers (version, TimeMode, LocalTime, geometry count) only, read-only.
- **C-9 records:** `astra_test_01/burst/runs/C-9/ledger.json` and `wl_e1/export/final_k_cand/clip_sources.json`.
- **Licence:** <https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775> (TylerG 3D, 2022-09-29).
  - Not reachable: <https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html> (403).
- **Repo visibility:** `gh repo view` (collaboration PUBLIC, godot PRIVATE). Tracked files checked with `git ls-files` and `astra_test_01/.gitignore`.
- **General web search was not available.** The session's WebSearch budget was already spent. Every finding comes from Mixamo itself, local files, or the one Adobe community page fetched directly.

---

## Appendix A — Pack file-name decoders

The predicted file name follows the § 1.2 rule; it was verified 51 of 51 on Great Sword. The description, In-Place support and length come from Mixamo's API [M]. Confirm any file by its length (±1 frame). Rows tagged **BACKWARD** are backward-travelling clips; the dangerous ones are those whose file name doesn't say so.

#### Pro Melee Axe Pack — 47 clips

| File in the zip (predicted) | Mixamo description | In-Place capable | Length |
|---|---|---|---|
| `crouch idle.fbx` | Crouch Idle With Axe | no | 1.67 s |
| `crouch to standing idle.fbx` | Transition From Crouch To Standing Idle | no | 0.60 s |
| `standing block idle.fbx` | Blocking An Attack With Axe | no | 1.83 s |
| `standing block react large.fbx` | Large Block Reaction With Axe | no | 1.33 s |
| `standing disarm underarm.fbx` | Disarming Axe Underarm | no | 1.70 s |
| `standing disarm over shoulder.fbx` | Disarming Axe Over The Shoulder | no | 1.67 s |
| `standing idle.fbx` | Standing Idle With Axe | no | 1.83 s |
| `standing idle looking ver. 1.fbx` | Looking Around With Axe | no | 11.23 s |
| `standing idle looking ver. 2.fbx` | Looking Around With Axe | no | 7.83 s |
| `standing melee attack backhand.fbx` | Backhanded Upward Attack With Axe | no | 3.17 s |
| `standing melee attack downward.fbx` | Downward Attack With Axe | no | 2.27 s |
| `standing melee attack horizontal.fbx` | Right To Left Attack With Axe | no | 2.40 s |
| `standing melee attack 360 high.fbx` | Left To Right Spin Attack With Axe | no | 3.17 s |
| `standing melee attack 360 low.fbx` | Left To Right Spin Attack With Axe | no | 2.47 s |
| `standing melee attack kick ver. 1.fbx` | Kick With Right Foot Holding Axe | no | 1.83 s |
| `standing melee attack kick ver. 2.fbx` | Kick With Right Foot Holding Axe | no | 1.40 s |
| `standing melee combo attack ver. 1.fbx` | Two Hit Combo Attack With Axe | no | 4.67 s |
| `standing melee combo attack ver. 2.fbx` | Three Hit Combo Attack With Axe | no | 4.20 s |
| `standing melee combo attack ver. 3.fbx` | Two Hit Combo Attack With Axe | no | 2.73 s |
| `standing melee run jump attack.fbx` | Running Jump With Attack With Axe | no | 3.67 s |
| `standing react large from left.fbx` | Hit Reaction From The Left With Axe | no | 1.03 s |
| `standing react large from right.fbx` | Hit Reaction From The Right With Axe | no | 1.77 s |
| `standing react large gut.fbx` | Hit Reaction From Gut Shot With Axe | no | 1.57 s |
| `standing run back.fbx` | Running Backwards With Axe — **BACKWARD** (named) | yes | 0.77 s |
| `standing run forward.fbx` | Running Forward With Axe | yes | 0.73 s |
| `standing taunt battlecry.fbx` | Battlecry With Axe | no | 2.83 s |
| `standing taunt chest thump.fbx` | Banging Axe On Chest | no | 2.83 s |
| `standing turn left 90.fbx` | Turning 90 Degrees Left With Axe | no | 1.73 s |
| `standing turn right 90.fbx` | Turning 90 Degrees Right With Axe | no | 1.63 s |
| `standing walk back.fbx` | Walking Backwards With Axe — **BACKWARD** (named) | yes | 1.33 s |
| `standing walk forward.fbx` | Walking Forward With Axe | yes | 1.30 s |
| `standing walk left.fbx` | Walking Left With Axe | yes | 1.20 s |
| `standing walk right.fbx` | Walking Right With Axe | yes | 1.27 s |
| `unarmed equip underarm.fbx` | Equipping Axe Underarm | no | 1.23 s |
| `unarmed equip over shoulder.fbx` | Equipping Axe Over The Shoulder | no | 1.67 s |
| `unarmed idle.fbx` | Standing Idle- Loop | no | 1.90 s |
| `unarmed idle looking ver. 1.fbx` | Looking Around | no | 11.23 s |
| `unarmed idle looking ver. 2.fbx` | Looking Around | no | 7.83 s |
| `unarmed jump.fbx` | Jumping And Landing In Place | no | 2.33 s |
| `unarmed jump running.fbx` | Running Jump And Landing | yes | 1.37 s |
| `unarmed run back.fbx` | Running Backwards — **BACKWARD** (named) | yes | 0.73 s |
| `unarmed run forward.fbx` | Running Forward | yes | 0.77 s |
| `unarmed turn left 90.fbx` | Turning 90 Degrees Left | no | 1.50 s |
| `unarmed turn right 90.fbx` | Turning 90 Degrees Right | no | 1.50 s |
| `unarmed walk back.fbx` | Walking Backwards — **BACKWARD** (named) | yes | 1.27 s |
| `unarmed walk forward.fbx` | Walking Forward | yes | 1.33 s |
| `standing jump.fbx` | Jumping And Landing In Place With Axe | no | 1.87 s |

#### Pro Sword and Shield Pack — 51 clips

| File in the zip (predicted) | Mixamo description | In-Place capable | Length |
|---|---|---|---|
| `sword and shield walk.fbx` | Sword And Shield Walk | yes | 1.07 s |
| `sword and shield run.fbx` | Sword And Shield Run | yes | 0.70 s |
| `sword and shield jump.fbx` | Sword And Shield Running Jump | yes | 0.83 s |
| `sword and shield jump (2).fbx` | Sword And Shield Jump From Idle | no | 0.97 s |
| `sword and shield strafe.fbx` | Sword And Shield Right Strafe Walk | yes | 1.13 s |
| `sword and shield strafe (2).fbx` | Sword And Shield Left Strafe Walk | yes | 1.30 s |
| `sword and shield walk (2).fbx` | Sword And Shield Backward Walk — **BACKWARD** (name says walk) | yes | 1.23 s |
| `sword and shield 180 turn.fbx` | Sword And Shield Walk 180 Turn | no | 0.77 s |
| `sword and shield strafe (3).fbx` | Sword And Shield Left Run Strafe | yes | 0.63 s |
| `sword and shield strafe (4).fbx` | Sword And Shield Right Run Strafe | yes | 0.70 s |
| `sword and shield 180 turn (2).fbx` | Sword And Shield Run 180 Turn | no | 0.80 s |
| `sword and shield run (2).fbx` | Sword And Shield Backward Run — **BACKWARD** (name says run) | yes | 0.53 s |
| `sword and shield slash.fbx` | Sword And Shield Downward Slash | no | 1.50 s |
| `sword and shield slash (2).fbx` | Sword And Shield Slash Combo | no | 3.53 s |
| `sword and shield slash (3).fbx` | Sword And Shield Cross Slash | no | 1.67 s |
| `sword and shield slash (4).fbx` | Sword And Shield Power Slash | no | 2.43 s |
| `sword and shield block.fbx` | Sword And Shield Idle To Block | no | 0.57 s |
| `sword and shield block idle.fbx` | Sword And Shield Block Idle | no | 1.37 s |
| `sword and shield block (2).fbx` | Sword And Shield Block To Idle | no | 0.67 s |
| `sword and shield impact.fbx` | Sword And Shield Blocked Impact | no | 0.77 s |
| `sword and shield impact (2).fbx` | Sword And Shield Unblocked Impact | no | 0.77 s |
| `sword and shield impact (3).fbx` | Sword And Shield Head Impact | no | 0.70 s |
| `sword and shield crouch.fbx` | Sword And Shield Stand To Crouch | no | 0.53 s |
| `sword and shield crouching.fbx` | Sword And Shield Crouch To Stand | no | 0.47 s |
| `sword and shield crouch idle.fbx` | Sword And Shield Left Crouch Idle- Loop | no | 2.40 s |
| `sword and shield slash (5).fbx` | Sword And Shield Crouch Slash | no | 1.37 s |
| `sword and shield crouch block.fbx` | Sword And Shield Left Crouch  To Block | no | 0.50 s |
| `sword and shield crouch block idle.fbx` | Sword And Shield Crouch Block Idle | no | 0.50 s |
| `sword and shield crouching (2).fbx` | Sword And Shield Block To Crouch | no | 0.60 s |
| `sword and shield crouch block (2).fbx` | Sword And Shield Blocked Impact | no | 0.80 s |
| `sword and shield crouching (3).fbx` | Sword And Shield Unblocked Impact | no | 0.63 s |
| `sword and shield attack.fbx` | Sword And Shield Jump Attack | no | 2.30 s |
| `sword and shield attack (2).fbx` | Sword And Shield High Attack | no | 1.30 s |
| `sword and shield attack (3).fbx` | Sword And Shield Low Attack | no | 1.73 s |
| `sword and shield idle.fbx` | Sword And Shield Look Around Idle | no | 3.67 s |
| `sword and shield idle (2).fbx` | Sword And Shield Sword Play Idle | no | 7.50 s |
| `sword and shield idle (3).fbx` | Sword And Shield Stretch Idle | no | 8.67 s |
| `sword and shield kick.fbx` | Sword And Shield Sparta Kick | no | 1.17 s |
| `sword and shield casting.fbx` | Sword And Shield Spell Casting | no | 2.93 s |
| `sword and shield attack (4).fbx` | Sword And Shield Hilt Melee | no | 1.00 s |
| `sword and shield power up.fbx` | Sword And Shield Powering Up | no | 2.37 s |
| `sword and shield death.fbx` | Sword And Shield Falling Back Death | no | 2.27 s |
| `sword and shield death (2).fbx` | Sword And Shield Falling Forward Death | no | 3.90 s |
| `sword and shield turn.fbx` | Sword And Shield 90 Degree Right Turn | no | 0.90 s |
| `sword and shield turn (2).fbx` | Sword And Shield 90 Degree Left Turn | no | 0.90 s |
| `sword and shield idle (4).fbx` | Sword And Shield Idle | no | 2.53 s |
| `sword and shield casting (2).fbx` | Sword And Shield Spell Casting | no | 1.00 s |
| `draw sword 1.fbx` | Transition From Standing To Drawing Sword | no | 0.47 s |
| `draw sword 2.fbx` | Transition From Standing To Drawing Sword | no | 0.73 s |
| `sheath sword 1.fbx` | Combat To Sheathing Sword | no | 1.27 s |
| `sheath sword 2.fbx` | Sheath Pose To Standing | no | 0.83 s |

#### Pro Magic Pack — 56 clips

| File in the zip (predicted) | Mixamo description | In-Place capable | Length |
|---|---|---|---|
| `standing 1H cast spell 01.fbx` | One Handed Casting Spell Upwards | no | 2.27 s |
| `standing idle.fbx` | Standing Idle Ready To Cast Spell | no | 1.87 s |
| `Standing 1H Magic Attack 01.fbx` | One Handed Casting Spell Fowards | no | 2.27 s |
| `Standing 1H Magic Attack 02.fbx` | One Handed Casting Spell Sweep Right To Left | no | 2.20 s |
| `Standing 1H Magic Attack 03.fbx` | One Handed Casting Spell Upward Sweep | no | 2.27 s |
| `Standing 2H Cast Spell 01.fbx` | Two Handed Casting Spell Upward Pull | no | 2.13 s |
| `Standing 2H Magic Area Attack 01.fbx` | Two Handed Casting Spell Towards Ground | no | 2.93 s |
| `Standing 2H Magic Area Attack 02.fbx` | Two Handed Casting Spell Pull In Blast Out | no | 3.23 s |
| `Standing 2H Magic Attack 01.fbx` | Two Handed Casting Spell Fowards | no | 2.70 s |
| `Standing 2H Magic Attack 02.fbx` | Two Handed Casting Spell Fowards | no | 2.63 s |
| `Standing 2H Magic Attack 03.fbx` | Two Handed Casting Spell Forwards Sustained | no | 4.30 s |
| `Standing 2H Magic Attack 04.fbx` | Two Handed Casting Spell Forwards Sustained | no | 3.30 s |
| `Standing 2H Magic Attack 05.fbx` | Two Handed Casting Spell Pull Up And Clap Hands | no | 3.53 s |
| `standing idle 02.fbx` | Standing Idle Looking Around | no | 5.17 s |
| `Crouch Idle.fbx` | Crouch Idle | no | 1.33 s |
| `Crouch To Standing Idle.fbx` | Transition From Crouch To Standing Idle | no | 1.00 s |
| `Crouch Turn Left 90.fbx` | Turning 90 Degrees Left | no | 1.83 s |
| `Crouch Turn Right 90.fbx` | Turning 90 Degrees Right | no | 1.63 s |
| `Crouch Walk Back.fbx` | Walking Backwards While Crouched | yes | 1.20 s |
| `Crouch Walk Forward.fbx` | Walking Forward While Crouched | yes | 1.13 s |
| `Crouch Walk Left.fbx` | Walking Left While Crouched | yes | 1.13 s |
| `Crouch Walk Right.fbx` | Walking Right While Crouched | yes | 1.23 s |
| `Standing Block Idle.fbx` | Blocking With Both Arms Out | no | 2.73 s |
| `Standing Block React Large.fbx` | Block Reaction | no | 1.33 s |
| `Standing Block End.fbx` | Transition From Block Idle To Standing Idle | no | 1.27 s |
| `Standing Block Start.fbx` | Transition From Standing Idle To Block Idle | no | 0.50 s |
| `Standing Idle 03.fbx` | Playing With Magic | no | 11.40 s |
| `Standing Idle 04.fbx` | Here'S The Windup…And The Pitch…BOOM | no | 7.43 s |
| `Standing Idle To Crouch.fbx` | Transition From Standing Idle To Crouch Idle | no | 1.00 s |
| `Standing Jump.fbx` | Jumping And Landing In Place | no | 2.33 s |
| `Standing Jump Running.fbx` | Jumping While Running | no | 1.03 s |
| `Standing Jump Running Landing.fbx` | Landing From Running  Jump Into Run Forward | no | 1.37 s |
| `Standing Land To Standing Idle.fbx` | Landing From Running Jump Into Standing Idle | no | 1.10 s |
| `Standing React Death Backward.fbx` | Death Falling Backwards | no | 3.60 s |
| `Standing React Death Forward.fbx` | Death Falling Forwards | no | 3.67 s |
| `Standing React Death Left.fbx` | Death Falling To The Left | no | 3.60 s |
| `Standing React Death Right.fbx` | Death Falling To The Right | no | 3.50 s |
| `Standing React Large From Back.fbx` | Large Hit Reaction From The Back | no | 1.67 s |
| `Standing React Large From Front.fbx` | Large Hit Reaction From The Front | no | 1.37 s |
| `Standing React Large From Left.fbx` | Large Hit Reaction From The Left | no | 1.53 s |
| `Standing React Large From Right.fbx` | Large Hit Reaction From The Right | no | 1.63 s |
| `Standing React Small From Back.fbx` | Small Hit Reaction From The Back | no | 1.23 s |
| `Standing React Small From Front.fbx` | Small Hit Reaction From The Front | no | 1.17 s |
| `Standing React Small From Left.fbx` | Small Hit Reaction From The Left | no | 1.17 s |
| `Standing React Small From Right.fbx` | Small Hit Reaction From The Right | no | 0.97 s |
| `Standing Run Back.fbx` | Running Backwards (named) | yes | 0.60 s |
| `Standing Run Forward.fbx` | Running Forwards | yes | 0.73 s |
| `Standing Run Left.fbx` | Running Left | yes | 0.73 s |
| `Standing Run Right.fbx` | Running Right | yes | 0.77 s |
| `Standing Sprint Forward.fbx` | Sprinting Forward | yes | 0.57 s |
| `Standing Turn Left 90.fbx` | Turning 90 Degrees Left | no | 1.83 s |
| `Standing Turn Right 90.fbx` | Turning 90 Degrees Right | no | 1.63 s |
| `Standing Walk Back.fbx` | Walking Backwards (named) | yes | 1.20 s |
| `Standing Walk Forward.fbx` | Walking Forwards | yes | 1.13 s |
| `Standing Walk Left.fbx` | Walking Left | yes | 1.13 s |
| `Standing Walk Right.fbx` | Walking Right | yes | 1.17 s |

The case of Pro Magic file names is as Mixamo lists them, which is mixed case [M]. Whether the zip lower-cases them is unverified [I].

#### Great Sword Pack — 51 clips (owned; verified 51 of 51 against the local files [L+M])

| File in the zip | Mixamo description | In-Place capable | Length |
|---|---|---|---|
| `great sword idle.fbx` | Great Sword Idle | no | 2.00 s |
| `great sword walk.fbx` | Great Sword Walk | yes | 1.33 s |
| `great sword walk (2).fbx` | Great Sword Backward Walk — **BACKWARD** | yes | 1.27 s |
| `great sword strafe.fbx` | Great Sword Strafe Left Walk | yes | 1.07 s |
| `great sword strafe (2).fbx` | Great Sword Strafe Right Walk | yes | 1.13 s |
| `great sword 180 turn.fbx` | Great Sword Walk 180 Turn | no | 0.77 s |
| `great sword turn.fbx` | Great Sword 90 Degree Right Turn | no | 0.70 s |
| `great sword turn (2).fbx` | Great Sword 90 Degree Left Turn | no | 0.80 s |
| `great sword run.fbx` | Great Sword Bacward Run — **BACKWARD** | yes | 0.70 s |
| `great sword 180 turn (2).fbx` | Great Sword Run 180 Turn | no | 0.53 s |
| `great sword strafe (3).fbx` | Great Sword Strafe Left Run | yes | 0.57 s |
| `great sword strafe (4).fbx` | Great Sword Strafe Right Run | yes | 0.63 s |
| `great sword jump.fbx` | Great Sword Running Jump | yes | 0.63 s |
| `great sword jump (2).fbx` | Great Sword Jump | no | 0.90 s |
| `great sword slash.fbx` | Great Sword Downward Slash | no | 1.27 s |
| `great sword slash (2).fbx` | Great Sword Combo Slash | no | 3.50 s |
| `great sword slash (3).fbx` | Great Sword Low Slash | no | 1.80 s |
| `great sword slash (4).fbx` | Great Sword Power Slash | no | 1.77 s |
| `great sword blocking.fbx` | Great Sword Standing To Block | no | 0.50 s |
| `great sword blocking (2).fbx` | Great Sword Blocking Idle | no | 0.93 s |
| `great sword blocking (3).fbx` | Great Sword Block To Standing | no | 0.50 s |
| `great sword impact.fbx` | Great Sword Blocked Impact | no | 0.83 s |
| `great sword impact (2).fbx` | Great Sword Unblocked Impact | no | 1.17 s |
| `great sword impact (3).fbx` | Great Sword Head Impact | no | 1.23 s |
| `great sword crouching.fbx` | Great Sword Stand To Crouch | no | 0.67 s |
| `great sword crouching (2).fbx` | Great Sword Crouch To Stand | no | 0.70 s |
| `great sword crouching (3).fbx` | Great Sword Crouch Idle | no | 1.83 s |
| `great sword slash (5).fbx` | Great Sword Crouching Slash | no | 1.43 s |
| `great sword crouching (4).fbx` | Great Sword Crouch To Block | no | 0.37 s |
| `great sword crouching (5).fbx` | Great Sword Crouching Block Idle | no | 1.40 s |
| `great sword crouching (6).fbx` | Great Sword Block To Crouch | no | 0.47 s |
| `great sword impact (4).fbx` | Great Sword Crouching Blocked Impact | no | 0.63 s |
| `great sword impact (5).fbx` | Great Sword Crouching Unblocked Impact | no | 0.93 s |
| `great sword jump attack.fbx` | Great Sword Jump Attack From Run | no | 2.17 s |
| `great sword slide attack.fbx` | Great Sword Low Slide Attack From Run | no | 2.10 s |
| `great sword high spin attack.fbx` | Great Sword High Spin Attack From Run | no | 1.87 s |
| `great sword kick.fbx` | Great Sword Spin Kick | no | 1.50 s |
| `great sword kick (2).fbx` | Great Sword Side Kick | no | 1.73 s |
| `great sword idle (2).fbx` | Great Sword Look Around Idle | no | 3.70 s |
| `great sword idle (3).fbx` | Great Sword Strike A Pose Idle | no | 3.63 s |
| `great sword idle (4).fbx` | Great Sword Admiring Idle | no | 3.73 s |
| `great sword idle (5).fbx` | Great Sword Look Around Idle | no | 7.53 s |
| `great sword casting.fbx` | Great Sword Spell Casting | no | 4.77 s |
| `great sword power up.fbx` | Great Sword Powering Up | no | 3.50 s |
| `great sword attack.fbx` | Great Sword Hilt Melee | no | 1.17 s |
| `two handed sword death.fbx` | Falling Back Death | no | 2.40 s |
| `draw a great sword 1.fbx` | Transition From Standing To Drawing Great Sword | no | 0.50 s |
| `draw a great sword 2.fbx` | Transition From Standing To Drawing A Great Sword | no | 0.77 s |
| `two handed sword death (2).fbx` | Falling Forward Death | no | 2.57 s |
| `spell cast.fbx` | Spell Casting With A Two Handed Sword | no | 1.10 s |
| `great sword run (2).fbx` | Great Sword Run (the FORWARD run) | yes | 0.60 s |
