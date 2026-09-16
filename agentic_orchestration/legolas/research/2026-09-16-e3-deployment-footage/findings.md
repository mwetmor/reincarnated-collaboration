# Research — E3 deployment footage + source deployment facts — 2026-09-16

> **STATUS:** CURRENT — legolas Mode A (UNKNOWN-RESEARCHER), commissioned by gandalf (RUN-CONDUCTOR, Run C-5) on Matt's ruling 2026-09-16: *"Start with gathering the footage on the missing skills… Then build them based on the video references."*

**Evidence classes:** VERIFIED (primary source read first-hand — shipped game data or developer-authored text) · MEASURED (first-hand measurement, method stated) · DERIVED (computed from VERIFIED/MEASURED, arithmetic shown) · SECONDARY (wiki / database site) · TERTIARY (forum, build guide) · INFERRED (reasoned, not read) · UNKNOWN.

---

## 0. READ THIS FIRST — three findings that change the build, not just the numbers

**(a) `healing_hands` is not a G4 aura loop. The grammar assignment is wrong, not merely mistuned.**
Base Healing Hands is a **one-shot instantaneous burst placed at the CURSOR GROUND POINT**, cooldown 0, no loop, no pulse train. The spec's 4.0 s / six-pulse / `caster_root` / `owner-tracking` model describes a skill that does not exist. Source: EHG's own documentation (§ 5). The likeliest origin of the error is named there — it is a recognisable mis-read, not a random one.

**(b) The sources are metronomes. The FF-08 jitter in the specs is HOUSE STYLE, not observation.**
Every source cadence I could reach in shipped data is **perfectly regular**: Frozen Orb emits **every single frame** (`Param1 frequency = 1`); Blackwater's pool ticks on a **flat 1000 ms `targetInterval`**. The specs carry irregular schedules with `tick_cv_min 0.25` whose provenance strings read *"source observation (conductor memory) — VERIFY"*. That string conflates two different things: the **delivery facts** (which the sources do supply) and the **anti-metronome rule** (which is ours). FF-08 may well be right for our register — but it should be adopted as a **declared deviation from source**, not inherited as though the source showed it. This is the T4x *"{2,3} jitter contract proven impossible"* problem one level up.

**(c) No download was needed for the deployment facts, and footage would have been the weaker evidence anyway.**
Sourcing option **c′** (no downloads) was honoured throughout — `yt-dlp` is not installed on this host, which settled it. But four of the six skills turned out to be answerable from **shipped game data or developer-authored text**, which is strictly better evidence than eyeballing a compressed video: it gives exact frame counts, intervals, radii in metres and per-rank scaling that no frame-step can recover. Footage is still required for the genuinely visual questions (body extents in BH, glass-shard presence, bolt width), and those are listed for Matt in § 9.

**A standing caution on everything below.** I could not watch video **on the first pass**. **Every footage quality verdict in § 1 is INFERRED from title, description, chapter markers, duration and channel habit — not one is a visual observation.** They are triage for a human frame-step, nothing more.

> ⛑ **SUPERSEDED IN PART, 2026-09-16 (second pass).** Under Matt's sourcing ruling (b), the clips were downloaded and measured privately. **§ 12 is the frame-measurement record and it outranks § 1's inferred quality verdicts and every UNKNOWN in Tables A and B that it names.** Read § 12.4 and § 12.5 for exactly which rows moved. Three corrections a reader should carry: **(i)** `alt_EbMkJBxIVaI_0204` is a **Poseidon** run, not Zeus — the usable 60 fps Zeus footage is `alt_XPs-jypdwx8`; **(ii)** `clip_AMXRR3QVpFY_0029`'s dummy section is an endgame build whose bolt is fully chained — the single-bolt measurements came from `alt2_vQGkaa0Uax0_end`; **(iii)** `clip_ZRVed04RsJE_0023` turned out to be better than advertised — it is **pre-ascendancy with only Poisonous Concoction on the bar**, which is exactly the control Matt's puddle question needed.

---
## 1. Sources — footage candidates (§ 1a) and data sources (§ 1b)

### 1a. Footage — recommended first watch per skill

One row per skill: the single best candidate for isolating ONE cast. Runners-up are in each skill's section. **Timestamp CONFIRMED = read from the uploader's own chapter list or description; ESTIMATED = inferred.** Quality verdicts are INFERRED (nobody watched anything).

| Skill | URL | Title / channel | Timestamp | Conf. | Quality (inferred) |
|---|---|---|---|---|---|
| Frozen Orb | [b5a-iIras34](https://www.youtube.com/watch?v=b5a-iIras34) | *D2R — Sorceress Walkthrough — FULL GAME — HELL (No Commentary)* · Infinite Gaming | **≈ 3025 s** (already in use) | prior work | CLEAN — no commentary, no webcam, native UI |
| Frozen Orb (alt) | [RPJK4SSFZ0c](https://www.youtube.com/watch?v=RPJK4SSFZ0c) | *D2R Sorceress Skill Frozen Orb* · Fallen | whole clip | ESTIMATED | Dedicated single-skill clip. **Thumbnail fetched and viewed: it is a TITLE CARD**, gameplay behind it |
| Blackwater Cocktail | [ThO5dWZzyzY](https://www.youtube.com/watch?v=ThO5dWZzyzY) | *Grim Dawn \| DEMOLITIONIST skills showcase* · Grim Donny | **3:17–4:43** | **CONFIRMED** (chapter `Blackwater cocktail usage` @197200 ms) | CLEAN — author: *"a VERY BASIC demonstration… to see what they look like"* |
| Poisonous Concoction | [ZRVed04RsJE](https://www.youtube.com/watch?v=ZRVed04RsJE) | *[3.17] Poisonous Concoction beginner guide, Act 2 walkthrough* · Ashimar | **0:23–2:30** | **CONFIRMED** (chapter `Old Fields 0:23`) | CLEAN — open grassland, sparse packs, pre-ascendancy |
| Lightning Blast | [AMXRR3QVpFY](https://www.youtube.com/watch?v=AMXRR3QVpFY) | *Lightning Blast Sorcerer Endgame Build Guide* · Action RPG | **0:29** (dummy) | **CONFIRMED** (chapter `Dummy`) | CLEAN — one caster, one stationary target |
| Healing Hands | [n-IYQnoqpV8](https://www.youtube.com/watch?v=n-IYQnoqpV8) | *LE 1.0 Healing hands ward gain nodes bug* · Kos TIme | ~0:10–1:45 | ESTIMATED | Likely CLEAN — bug-repro format = one skill, dummy, no clutter |
| Zeus chain | — | see § 7 | — | — | — |

**Two footage caveats that outrank the table.**
- **Last Epoch changed the Healing Hands VFX in patch 1.4 (2026-03-26).** *Every* Healing Hands candidate found predates it. They are authoritative for delivery class only — and the official text settles delivery class better than video could anyway. For **appearance**, none of this footage is current.
- **Lightning Blast's un-chained single bolt appears only on the first cast after a ≥ 4 s pause** (§ 4). Any spammed cast in any footage already shows 1–2 chains regardless of skill tree. Tell whoever watches to look for a cast that follows a lull.

### 1b. Data sources — where the real answers came from

| Skill | Source | Grade |
|---|---|---|
| Frozen Orb | D2 1.13 `Missiles.txt`, `Skills.txt`, `CharStats.txt`, `Overlay.txt` — [fabd/diablo2 @ `code/d2_113_data/`](https://github.com/fabd/diablo2) | **VERIFIED (shipped game data)** |
| Blackwater Cocktail | Grim Dawn `database.arz` read live on disk via the team's own TQIT/LZ4 parser; cross-checked across two editions (34,114 / 34,171 records) — **byte-identical on every value** | **VERIFIED (shipped game data)** |
| Poisonous Concoction | [RePoE `gems.json`](https://github.com/lvlvllvlvllvlvl/RePoE) + [PoB `act_dex.lua`](https://github.com/PathOfBuildingCommunity/PathOfBuilding) — two independent extractions, agree exactly | **VERIFIED (game data)** |
| Lightning Blast · Healing Hands | EHG's own help centre via the open Zendesk API (`support.lastepoch.com/api/v2/help_center/…`) — machine-generated skill + node data, edited 2026-02/03 | **VERIFIED (developer-authored)** |

**Three lane findings worth keeping** (they will save the next probe a day):
- **`poewiki.net` is no longer agent-fetchable** — Anubis proof-of-work on every endpoint including `api.php`. The substitute lane (RePoE + PoB + poedb) is *better* than the wiki was.
- **`lastepochtools.com` and `lastepoch.fandom.com` are Cloudflare-blocked**, but **EHG's Zendesk API is wide open** and is a primary source. Route all Last Epoch lookups there.
- **`lastepoch.fandom.com` is stale by ~6 years on Lightning Blast and will actively mislead** — several node *names* survived with *inverted* effects, which is the dangerous failure mode: a name-match lookup returns a confident wrong answer.

---
## 2. Body-height (BH) scale — how every BH figure below was derived

BH is the only scale-free unit here, so the conversion is stated once and used throughout. **Where a game does not publish a character height, the BH figure is INFERRED and flagged at every use.**

| Game | World unit | Body height | Grade |
|---|---|---|---|
| **Diablo II** | yard = sub-tile corner-to-corner = 32 px horizontal | **1 BH = 2.055 yards** — from `RunVelocity 9` (VERIFIED) ÷ the team's measured 4.4 BH/s | **DERIVED** from VERIFIED + MEASURED |
| **Grim Dawn** | **1 unit = 1 tooltip metre**, verified (`projectileExplosionRadius 5.8` ↔ tooltip *"5.8 Meter Radius"*) | **≈ 1.8 m** | **INFERRED** — `actorHeight 3.0` in the `.arz` is a collision capsule quantised to 1/2/3, *not* a model height |
| **Path of Exile** | 1 unit = 0.1 m | **1.5–2.0 m** (*"most character models are in the range of 15–20 units tall"*) | SECONDARY |
| **Last Epoch** | metre (EHG publishes *"2.7 meters"*, *"7 meter radius"*) | **≈ 1.8 m** assumed | **INFERRED** — undocumented |

**The GD 1.8 m inference cross-validates.** At 1.8 m it implies a GD run of 6.8 m/s, which sits just below D2's VERIFIED 9 yd/s ≈ 8.2 m/s — exactly the ordering the team's independent run-speed measurement found (GD 3.78 BH/s vs D2 4.4 BH/s). That is a consistency check, not a proof.

**Where px appear below, they assume 1 BH = 130 px** (the Keeper reference from `2026-09-13-arpg-run-speeds`). If the C-5 px space uses a different body height, re-scale from the BH column, which is the authoritative one.

---

## 3. Frozen Orb — Diablo II *(CONFIRM commission — all three questions answered from data)*

**Grammar G1 (projectile-that-emits): CONFIRMED, and more exactly than the spec claims it.**

### The three questions

**Q1. Does the orb expire as a radial nova of bolts, with no impact body? — YES, emphatically. (VERIFIED)**

`frozenorb` carries `HitSubMissile1 = frozenorbnova` and `AlwaysExplode = 1` — the nova fires on expiry even with no collision. **16 radial bolts**, derived from `sHitPar1 = 4` (direction increment) over a 64-unit circle, and **independently corroborated**: *"Upon expiring or hitting an obstacle, a nova of 16 damaging bolts is released… These bolts are also destroyed on collision"* ([diablo2.io](https://diablo2.io/skills/frozen-orb-t4076.html)).

> **A first-of-kind observation the spec should record.** An impact-body asset **exists in the shipped data and is wired to nothing**: `frozenorbexplode` (`CelFile = IceOrbExplode`, 16 frames, `Explosion = 1`). I searched all 171 columns of every row in `Missiles.txt` — **no row references it**, and `frozenorb` has no `ExplosionMissile` field (`icebolt`, by contrast, has `ExplosionMissile = iceexplode`). Blizzard authored an orb-explosion sprite and then shipped the skill without it. **The spec's "no impact body" choice is not an approximation of D2 — it is exactly what D2 does, and D2 appears to have decided it late.**

**Q2. Travel speed and range in BH. (VERIFIED units → DERIVED BH)**

`Vel = MaxVel = 10`, `Accel` empty → **constant speed, no decay**. `Range = 30` frames; D2's game clock is 25 fps.

| | Source value | BH | px @130 |
|---|---|---|---|
| Orb speed | 10 yd/s (= **1.11 × the Sorceress's own run speed of 9**) | **4.87 BH/s** | 632 px/s |
| Orb flight time | 30 frames ÷ 25 fps | — | **1.20 s** |
| Orb travel distance | 12 yards | **5.84 BH** | 759 px |
| Travel bolt | Vel 18, Range 25 fr | 8.76 BH/s, **8.76 BH** max, 1.00 s life | 1138 px/s |
| Nova bolt | Vel 24, Range 25 fr | 11.68 BH/s, **11.68 BH** max, 1.00 s life | 1518 px/s |

**Q3. Bolt emission cadence — every single frame, perfectly regular. (VERIFIED)**

`Param1 = 1` (*"frequency"*) → one bolt **per game frame** = **25 bolts/s**, for all 30 frames ≈ **29–30 bolts per cast**. Corroborated verbatim: *"the orb fires one damaging bolt in each frame of its 30 frame existence"* (diablo2.io). `Param2 = 19` (*"direction increment"*) over a 64-unit circle → **106.9° between consecutive bolts = 3.37 bolts per revolution** (the spec's "3 per revolution" is right, and the exact figure is 3.37).

> **There is no jitter in the source. None.** The cadence is a 25 Hz metronome.

### What the data shows that a text description misses

- **The orb itself deals no damage.** `frozenorb` has **no `Skill` field**; `frozenorbbolt` and `frozenorbnova` both carry `Skill = Frozen Orb`. The orb is a *pure emitter* — a moving spawner with a sprite. This is G1 in its purest form and worth saying out loud in the spec.
- **The orb does not die on contact with monsters** (`CollideKill` unset, unlike both bolt types which have `CollideKill = 1`) but **does stop at obstacles**. So `pierce: -1` is right for actors, wrong for walls.
- **Cast telegraph exists:** `delay = 25` frames = **1.0 s cast delay** (corroborated: *"Casting Delay: 1 Second"*, [purediablo](https://purediablo.com/d2wiki/Frozen_Orb)), plus `castoverlay = ice_cast_3` — 15 frames, `Radius 9`, RGB (81,81,255), single-direction. **≈ 0.60 s** at 25 fps (DERIVED; the overlay animrate convention is unconfirmed).
- Orb RGB tint is (81,81,255) on all three missiles — one hue, shared.

**Still UNKNOWN from data:** the orb's on-screen **body size** (spec says 0.9 BH). `Size = 1` is a collision class, not a sprite dimension. **Footage-only** → § 9.

---
## 4. Blackwater Cocktail — Grim Dawn *(G2 lobbed field: CONFIRMED)*

**Grammar G2 (lobbed field): CONFIRMED.** This is the one skill of the six whose spec grammar is simply right. Everything below is **VERIFIED** from the shipped `database.arz`, cross-checked byte-identical across two editions on disk.

Record chain: `skills/playerclass02/blackwater1.dbr` (`Skill_AttackProjectile`) → `fx/skillsother/projectile_aoe/molotov{1..4}_projectilefx01.dbr` (`ProjectileGrenade`) → `molotov{1..4}_aoe_projectile01.dbr` (`ProjectileAreaEffect`) → `molotov{1..4}_aoe_fx.dbr` → `decal_groundimpact_blackwater01_{med,lg}.dbr`.

| Fact | Value |
|---|---|
| **Aim** | `skillProjectileTargetGroundOnly = True` → **cast at the CURSOR POINT**, not an enemy target |
| **Delivery** | FX class **`ProjectileGrenade`**, `launchAngle = 18.0°`, anim `Throw` → **a real lob, not instant placement** |
| **Flight** | `projectileVelocity = 18` m/s, `projectileDistance = 15` m → **0.83 s at max range**; shorter throws scale linearly |
| **Range** | **15 m = 8.33 BH** (INFERRED BH) |
| **Field radius** | **one field only** — `projectileExplosionRadius`; impact burst and lingering pool **share it** |
| **Tick cadence** | `targetInterval = **1000 ms**` — a flat 1 Hz metronome |
| **Cooldown** | **none** on the base skill (High Potency adds 3.8 s) |

**Per-rank scaling** (22 ranks; the spec must pick one and say which):

| Rank | Radius | Pool duration | Field diameter (BH, inferred) |
|---|---|---|---|
| 1 | 2.5 m | 2.5 s | **2.78 BH** |
| 12 (max base) | 5.8 m | 4.5 s | **6.44 BH** |
| 22 (max ult) | 6.4 m | 6.5 s | **7.11 BH** |

### What the data shows that a text description misses

- **The flask is a physics body that can BOUNCE.** `physicsRestitution = 1.0`, `physicsFriction = 16.0`, and a dedicated `projectileBounceSound`. The spec models a clean arc-and-shatter; the source can skip the flask off the ground first.
- **The scorch decal massively outlives the flames.** Decal `life = 12.0 s`, `fadeAfter = 11.0 s`, `fadeIn = 0.1 s` — against a pool that burns for only 2.5–6.5 s. **The spec's `residue: scorch decal 1.0 s` is off by more than 10×.**
- **The pool is a ground decal + particles, not a volumetric cloud.** `terrainOnly = True`, texture `groundimpact_charredearth01.tex`, shader `decal_glow.ssh`; the AoE's own mesh is `sphere.msh`, an invisible damage collider. Decal quads: med 8×8, lg 12×12, xlg 16×16 (ranks 1–2 med, 3–4 lg).
- **The projectile mesh is literally a booze bottle** — `fx/meshfx/boozebottle_molotov01.msh`, held at `R Hand` — and the bounce/impact sound is the **potion-drop sound**. Strong circumstantial support for the spec's "material glass flask, RGB, not value-index" choice.
- **Burn duration is a flat 3.0 s regardless of rank** and is **not** the pool duration — two different clocks that the spec currently conflates into one.
- Impact `cameraShakeAmplitude 0.25` / `duration 0.5`; the cast itself shakes 0.12.

> **⚠ The wiki is a version behind, and grimtools-tier numbers will mislead.** Fandom (stamped v1.1.9.0) matches shipped data on **radius and energy for all 12 ranks** but diverges on **duration from rank 5** (4.0 s vs **4.5 s**) and **damage from rank 2**, and caps ultimate duration at 4.0 s where shipped data scales to **6.5 s**. High Potency: wiki +5 s / 165%, `.arz` **3.8 s / 125%**. **Use the `.arz`.** (This is the same class of defect as the 2026-07-23 grimtools-vs-`.arz` 60-rank/26-rank contradiction — same source, same failure.)

**Still UNKNOWN:** whether **glass shards** visibly spawn. The bottle mesh and glass sound are strong circumstantial evidence, but shard geometry lives in `pfx_molotov_impact0{1..4}.pfx` inside the packed `.arc` archives, which were not opened. **Not observed — do not spec it as fact.** Likewise the **particle flame-lick cadence**, which is *not* locked to the 1 Hz damage interval and is unread. → § 9.

---

## 5. Poisonous Concoction — Path of Exile 1 *(G2 lobbed field: **BROKEN** — there is no field)*

> ### ⚠ GRAMMAR BREAK — the persisting cloud does not exist.
> The spec models a `density_cloud` field with `duration_s 2.0`, a 5-tick schedule and a 1.5 s puddle residue. **Base Poisonous Concoction produces an instantaneous area burst and NOTHING ELSE.** No cloud, no ground, no duration, no ticks. It is a **lobbed BURST (G1-at-a-point)**, not a lobbed field.

**This is VERIFIED from game data, structurally, against the exact comparison the commission named:**

| | Poisonous Concoction | Caustic Arrow |
|---|---|---|
| Skill types | Attack, RangedAttack, **Area**, Chaos, Projectile… | …**Duration**, **DamageOverTime**… |
| `base_skill_effect_duration` | **absent** | **2000** (2.00 s) |
| DoT stat | **absent** | `base_chaos_damage_to_deal_per_minute` |
| Terminal behaviour | **`projectile_behaviour_only_explode = 1`** | spreads caustic ground |

`projectile_behaviour_only_explode = 1` is decisive: the projectile's *entire* terminal behaviour is "explode." **No support gem or passive changes this** — a sweep of every support gem for ground-effect text returned **zero hits**; area supports scale the burst *radius* only.

| Fact | Value | Grade |
|---|---|---|
| **Aim** | **ground-targeted at the cursor** — *"fires projectiles at the ground near the player's cursor"* | SECONDARY (poewiki via index), corroborated by `console_skill_dont_chase = 1` |
| **but** | the bottle **can directly collide with an enemy body mid-flight** — it is not guaranteed to reach the ground | SECONDARY |
| **Speed** | 120 units/s = **12 m/s** = 6.67 BH/s | SECONDARY (poedb) |
| **Flight time** | distance ÷ 12 m/s. At the spec's 480 px (≈ 6.6 m): **0.55 s** | DERIVED |
| **Burst radius** | `active_skill_base_area_of_effect_radius = 18` units = **1.8 m ≈ 1.0 BH radius / 2.0 BH diameter** | **VERIFIED (game data, two independent dumps agree)** |
| **Duration** | **NONE — no duration stat of any kind on the gem** | **VERIFIED** |
| **Projectile count** | **1** — no projectile-count stat exists on the gem | **VERIFIED** |
| **Colour** | **`visual_hit_effect_chaos_is_green = 1`** — the engine's green-chaos flag, not an inference from the chaos tag | **VERIFIED** |
| **Flask model** | *"An… Poisonous Flask will now be visually attached to your Character's Belt"* | **VERIFIED** (GGG 3.16.0 notes) |
| Base attack time | 1.0 s with `attackSpeedMultiplier 15` → ≈ 0.87 s | VERIFIED |

> **⚠ The trap that will mislead anyone reading this footage.** **Alchemist's Mark** — a separate curse gem commonly slotted in PoC builds — *does* create **Caustic Ground, base duration 4.00 s**, when your hit poisons. **Plague Bearer** and map ground effects do likewise. **Any green lingering ground in a PoC video is almost certainly not the skill.** If the spec's `density_cloud` came from watching footage, this is the single most likely source of the error.

**Two premise corrections:** the gem shipped in **3.16 Scourge (Oct 2021), not 3.19** — so the clean single-skill showcase wave is late 2021, and every "first look" video predates launch and contains no gameplay. And it requires **character level 12**, so Act 1 footage is mostly pre-gem — **target Act 2**.

**Still UNKNOWN:** **trajectory shape (arc height vs flat)** — no source anywhere describes it, and the documented mid-flight body collision argues *against* a high lob. And **glass shards**: no source. Both → § 9.

---
## 6. Lightning Blast — Last Epoch *(G3 instant bolt-chain: CONFIRMED)*

**Grammar G3: CONFIRMED.** This is a genuinely instant, target-snapped bolt — the spec's `instant: true` and `aim_rule: target-tracking` are both right.

**Verbatim official description (VERIFIED, EHG):**
> *"Hurl a bolt of lightning at the target. It chains to an additional enemy for each time it has been directly cast in the last 4 seconds, up to 2 times."*
> Mana 3 · Cooldown 0 s · **Base Speed 1.467/s** (→ 0.682 s/cast) · Base Damage 21 Lightning

**Four independent lines of evidence that it is NOT a projectile:**
1. **The word "projectile" appears ZERO times in Lightning Blast's entire 27-node tree** — against 18 mentions for Fireball and 10 for Frost Claw.
2. EHG's own copy distinguishes the classes in the same article: Fireball *"Cast a **ball of fire** towards the target"*; Frost Claw *"**Three projectiles arc** to the target location"*; **Lightning Blast — *"Hurl a bolt of lightning at the target."*** No projectile noun, no "towards."
3. Its machine-data effect line — *"Hit nearest enemies every 0.1 seconds in 7 meter radius"* — appears on only three Mage skills, **all instant** (Lightning Blast, Elemental Nova, Static), and on **none** of the three real projectile skills.
4. Alpha 0.5.4 VFX bugfix (2018): *"Fixed a bug where the lightning blast vfx would briefly start off **stretched to the left before moving its proper position**."* A VFX that is *stretched* then *repositioned* is an arc drawn between two known endpoints.

| Fact | Value | Grade |
|---|---|---|
| Delivery | instant, target-snapped, **homing** (*"The lightning is homing, I don't need to aim"*) | VERIFIED |
| Needs a target? | **Yes.** Falls through to crates/barrels if no enemy. `Focal Blast` is the one node that fires *forward from the player* in a line | VERIFIED |
| **Base chains** | **0 on a cold cast**, +1 per direct cast in the last 4 s, **cap +2** | **VERIFIED** |
| Hop delay | **≈ 0.10 s** — from the *"every 0.1 seconds"* stat line | **INFERRED** (semantics undocumented) |
| Hop range | **6–7 m ≈ 3.3–3.9 BH** — LE's lightning-family hop distance (Static *"spread range: 7 meters"*; Arcane Current *"within 6 meters"*) | **INFERRED** |
| Cast rate | 1.467/s base, scales with cast speed | VERIFIED |
| Forking | **does not fork at base** — forking is node-granted (`Divergence`) | INFERRED, high confidence |
| Bolt width | **UNKNOWN** — no source states one | UNKNOWN |

> **The chain ramp is the finding that matters for a one-cast reference.** The spec's `chain.count: 1` is not a fixed property: it is **0, then 1, then 2** depending on how recently you last cast. **The un-chained single bolt exists only on the first cast after a ≥ 4 s pause** — it is not gated behind node choices, so any footage at any level can show it if the caster pauses.

**Still UNKNOWN:** whether the *rendered* VFX shows a brief sweep/whip-out over 1–3 frames between caster and target. The engine model is target-snapped; the presentation layer may animate a sweep anyway. **Do not read "not a projectile" as "appears with zero motion."** → § 9. Also unknown: base impact flash, bolt width, branch count, and behaviour when cast at empty ground.

> ⚠ **Do not use `lastepoch.fandom.com` for this skill.** It is stale by ~6 years (still banners `Beta 0.7.7`), lists 18 nodes against the live 27, and — the dangerous part — **several node names survived with inverted effects** (`Volatile Lightning` is a chaining node there, a shock-chance node live; `Arcing Power` is a damage node there, a chain-count node live). A name-match lookup returns a confident wrong answer. Route LE lookups to EHG's Zendesk API.

---

## 7. Healing Hands — Last Epoch *(G4 self aura loop: **BROKEN** — every element is wrong)*

> ### ⚠ THE LARGEST CORRECTION IN THIS COMMISSION.
> The spec models a **4.0 s aura loop, six pulses, `origin_socket: caster_root`, `aim_rule: owner-tracking`, ring orbiting at the caster's feet, seal decal underneath.** Base Healing Hands is a **ONE-SHOT INSTANTANEOUS BURST placed at the CURSOR GROUND POINT**, cooldown **0**, with **no loop, no pulse train and no 4-second window**. The skill the spec describes does not exist.

**Verbatim official description (VERIFIED — EHG, article *Paladin Skills*, edited 2026-02-18):**
> *"Heals all allies in a target area for 50 health and applies a lingering warmth which heals 80 health over the next 3 seconds. The lingering warmth cannot stack on the same target."*
> Mana 11 · **Cooldown: 0 seconds** · Base Speed 1.467/s (→ **≈ 0.682 s cast**) · Attunement: +5% healing effectiveness per point

| Spec assumption | Reality | Grade |
|---|---|---|
| Self-centred (`caster_root`, owner-tracking) | **Cast at a chosen target location under the cursor** | **VERIFIED** |
| 4.0 s duration | **Instantaneous.** Cooldown 0 → spammable, but each press is a discrete self-contained burst | **VERIFIED** |
| 6 pulses, CV ≥ 0.25 | **No pulses at all** | **VERIFIED** |
| (implicitly) damages enemies | **Base skill does NO damage.** Requires the `Searing Light` node: *"Healing Hands **now** hits enemies…"* | **VERIFIED** ×3 |

**The decisive evidence on targeting is a node that exists solely to patch it:**
> **Homeward** — *"If Healing Hands would not affect any allied players at the chosen target location, it is cast **centered on you instead**."*

A node granting "cast centered on you" proves the base skill is not. Corroborated by the indirect-cast nodes, which all speak of a target — `Cleric's Hammer`: *"cast Healing Hands **around the target**"*; `Hand of Aurelus`: *"**around the target location**"* — and by build-guide practice: *"you want to be up close and personal to make sure you're getting healed"*, i.e. self-healing is a **positioning problem**, which it would not be for a self-centred cast. (EHG's own blurb does say the burst heals *"all allies… including yourself"* — the caster is usually inside it, but the cast is *placed*.)

**The "3 seconds" in the description is a heal-over-time buff on the recipients** — non-stacking, refreshable — **not a persisting ground area and not a pulse sequence.** No base node creates ground persistence.

> **Where the error most likely came from — two named candidates, both recognisable:**
> - **`Unbroken Prayer`** turns Healing Hands into a **channeled** ability casting **4 times per second**. Watching a channeled build looks exactly like a pulse loop. **Most manual-cast footage of this skill is the channeled variant**, because the meta build is Rive/Smite + `Cleric's Hammer` proc.
> - **`Judgement`** — a *different* Paladin skill — *"leaves an area of **Consecrated Ground for 4 seconds**"*, healing *"50 health each second"* at *"Interval: 0.32 seconds."* That is the spec's model almost exactly: a 4-second pulsing ground area.
>
> Also: **there is no `Sigil`, `Consecrated Ground`, `Prayer`, `Faith's Reward` or `Holy Aura` node in the Healing Hands tree.** `Holy Aura` is a separate Paladin mastery skill; `Consecrated Ground` belongs to Judgement. If the spec drew on those names, it crossed skills.

**Visual (SECONDARY, thin):** the only sourced description is *"Healing Hands starts as a **golden ring**…"* — golden/holy palette, a ground-plane **ring** at the target location. **No source describes a glyph, seal, hexagram or rune.** The spec's "interrupted seal decal under the caster (MIX, ground)" is unsupported in both position and form.

> ⚠ **Freshness:** patch **1.4 "Shattered Omens" (2026-03-26)** contains *"Updated the visual effect for Healing Hands."* **Every footage candidate predates it.** They are authoritative for delivery class only — and the official text settles that better than video could.

**Still UNKNOWN: the base radius.** EHG does not publish it, while *explicitly* listing radii for sibling skills in the same article (Judgement's Consecrated Ground: *"Radius: 2.7 meters"*), so the omission is EHG's, not a retrieval failure. Fandom's infobox has no radius field either. Qualitative bound: EHG calls it *"a **medium sized** area of effect."* Area nodes: `Blessed Parish` +15%/pt, `Virtue of Patience` +16%/pt. **A ~3–4 m radius is a working assumption, INFERRED — do not spec it as fact.** → § 9.

> ⚠ And one warning that is directly relevant to a VFX spec: an unresolved community bug report claims **area-increase modifiers enlarge the *animation* without enlarging the *effective* radius**. **LE's own VFX radius may not match its gameplay radius** — so measuring the ring off footage may not give the real number either.

---
## 8. Zeus chain — Hades *(G3 instant bolt-chain: **BROKEN on delivery AND on treatment**)*

**Yes, the player's Zeus boon genuinely chains hop-to-hop — and it is the ordinary Attack boon.** Hades 1 splits Zeus into two mechanically distinct families:

| Family | Projectile `Type` | Behaviour | Boons |
|---|---|---|---|
| **chain-lightning** | `HOMING` / `STRAIGHT` | a travelling ball that **hops enemy→enemy** | **Lightning Strike** (Attack), **Electric Shot** (Cast), Splitting Bolt, Lightning Phalanx |
| **lightning bolt** | `SKY` | a bolt falls from above onto a point, ground AoE, **no hops** | Thunder Flourish, Thunder Dash, Zeus' Aid, Heaven's Vengeance, Lightning Reflexes, Lightning Rod |

> **Lightning Strike** — *"Your **Attack** emits chain-lightning when you damage a foe."* (`Bounces: 4`)

### ⚠ The finding most likely to change the build

> **Hades 1's chain lightning is NOT a drawn polyline between enemies.** It is a small **additive sprite ball** (`Graphic = ProjectileLightningBall`, `Scale 0.45`) riding at `OffsetZ 70` (**0.51 BH above the ground**) with a real dynamic light, travelling at **1500 units/s ≈ 10.8 BH/s**, shedding a **randomly chosen jagged sprite (`LightningPieceA`–`F`) every ~0.07 s**, and flashing `ProjectileLightningBallEnd` (28 frames @ 60 fps = **0.47 s**, Scale 0.55) on each impact.
>
> **The jagged drawn-bolt look everyone pictures belongs to the SKY family** — the one Theseus uses, and the one the team's existing `ijwA_J29j1k` @ 1745.6 s reference already shows. The spec's `"P05 chain link ×N along a jittered polyline + branch junctions + needle prongs"` describes the **wrong Zeus family**.
>
> Supergiant solved hop-readability with **a fast travelling emitter plus per-hop impact flashes**, not with a rendered arc. **If the team wants a drawn chain arc, Hades 1 is the wrong precedent and should be cited as a deliberate counter-example, not a source.**

### The data (VERIFIED — `Game/Projectiles/PlayerProjectiles.sjson`, `TraitData.lua`, `PlayerWeapons.sjson`, `Fx.sjson`)

| Fact | Value | BH |
|---|---|---|
| **Origin — at the struck enemy** | `ZeusWeaponTrait` → `OnDamageWeaponProperties = { FirstHitOnly = true, **FireFromVictimLocation = true** }` | — |
| **Bolt from the player?** | **NO — nothing is drawn player→enemy.** The melee swing is the only link | — |
| **Hop count** | `NumJumps = **4**` (Storm Lightning adds +2/+4/+6/+8) | — |
| **Hop range** | `JumpRange = **620** u` | **4.48 BH** |
| Projectile speed | `Speed = 1500` u/s | **10.83 BH/s** |
| Total travel budget | `Range = 520` u | **3.76 BH** |
| **Hop timing** | **NO DELAY FIELD EXISTS.** Hop cadence is **pure travel time** | ~**0.13 s** @200 u · **0.20 s** @300 u · **0.41 s** @620 u |
| Proc cap | `Cooldown = **0.167 s**` on the `ChainLightning` weapon → **max ~6 procs/s** | — |
| Damage falloff | `JumpDamageMultiplier = **0.8**`, compounding: 10 → 8 → 6.4 → 5.12 → 4.1 | — |
| Ball height | `OffsetZ = 70` u | **0.51 BH** |
| Fuse | 0.3 s | — |

**Hop timing is VERIFIED by exhaustion, not by absence of searching.** Every jump-related key across both `PlayerProjectiles.sjson` and `EnemyProjectiles.sjson` was enumerated: `NumJumps`, `JumpRange`, `JumpSpeedMultiplier`, `JumpRequiresLos`, `JumpDamageMultiplier`, `ExpireWhenOutOfJumps`, `NoJumpTargetRandomSpread`, `FinalJumpToOwner`, `BounceWhenOutOfJumpTargets`. **No `JumpDelay` / `ChainDelay` exists anywhere in the engine's vocabulary.** So the spec's authored `hop_delay_s: [0.06, 0.11, 0.08, 0.13]` has no counterpart in the source at all — and at 0.38 s total it is roughly **half** the source's ~0.8 s for four hops.

### Corrections to the commission's premises

- **Double Strike does NOT chain.** `ZeusBonusBoltTrait`'s `PropertyChanges` touch only SKY-bolt weapons — **`ChainLightning` is absent from its list.**
- **Splitting Bolt is not the bounce boon.** The bounce boon is **Storm Lightning** (`ZeusBonusBounceTrait`). Splitting Bolt (`ZeusChargedBoltTrait`) adds a *second, separate* spark per lightning hit (`LightningSpark`, `NumJumps 5`, Speed 500 — deliberately ~3× slower, reads as a drifting mote).
- **Lightning Reflexes does not chain** — SKY bolt on perfect-dash.
- **Static Discharge does not build-and-discharge** — that is a Hades II model. In Hades 1 it applies **Jolted**: *"the victim's next attack calls lightning down on itself, dealing area damage"* (`ZeusAttackPenalty`, `Duration 10`, `IsVulnerabilityEffect = true`).

### What the data reveals that boon text does not

- **`ChainLightning` omits `ExpireWhenOutOfJumps`** (which `ZeusProjectile` and `LightningSpark` both set `true`) → **the Attack ball persists after its jumps are spent**, dying to `Range`/`Fuse` instead of vanishing.
- **It also omits `MultipleUnitCollisions = false`** → INFERRED: the Attack chain **can re-hit a foe it already hit**, ping-ponging in sparse encounters. The Cast chain cannot.
- `CheckObstacleImpact = false` — the Attack chain **ignores terrain**. The Cast version does not.
- `MaxAdjustRate = 100` (Attack) vs `60` (Cast) — the Attack ball **turns nearly twice as hard**.
- **Cut content:** `ZeusReflectSparkTrait` defines a deflect-triggered `ZeusReflectChainLightning` that **nothing in `LootData.lua` grants**. Orphaned and unshipped — the same species of finding as D2's unwired `frozenorbexplode`.
- ⚠ **Wiki error:** Fandom lists Lightning Strike's *"Bounce Range: 520"*. **The data says `JumpRange = 620`**; 520 is `Range`, the total travel budget. The transcriber grabbed the wrong field. (Fandom gets Electric Shot right — 720 — where `Range` is 1100, so the two didn't collide.)

**Version caveat:** the dump is **v1.0 (Aug 2020)**; retail is v1.38. The wiki, maintained against retail, independently reports the same bounce counts, ranges and spark speed, so these did not drift — but that is corroboration, not a retail-build read.

**For footage, Electric Shot (Cast) is the better reference than Lightning Strike:** it is a Cast, so the ball is on screen from launch through every hop rather than emerging mid-swing from inside an enemy.

**Footage candidates** — top pick **[1V9Qkmoaxng](https://www.youtube.com/watch?v=1V9Qkmoaxng)** *HADES | Boon Guide | Zeus, God of Thunder* · Voxel Star · 10:26, with **CONFIRMED** chapters `0:59 Lightning Strike` · `1:36 Electric Shot` · `4:43 Static Discharge`. Runner-up **[EbMkJBxIVaI](https://www.youtube.com/watch?v=EbMkJBxIVaI)** (Haelian) with CONFIRMED `02:04 Poseidon Sword + Electric Shot` and `14:16 Eris Rail + Zeus Attack`. Dark horse **[y4iXv6oY3cc](https://www.youtube.com/watch?v=y4iXv6oY3cc)** — the uploader's own description says *"Zeus however, doesn't care to help with this video"*, i.e. the run never rolled Storm Lightning / Double Strike / Splitting Bolt, so **the base chain shows unmuddied**. Short clips: [XPs-jypdwx8](https://www.youtube.com/watch?v=XPs-jypdwx8) (3:00, spear — visually quiet), [JzOp9I3V9vs](https://www.youtube.com/watch?v=JzOp9I3V9vs) (0:58, but Aspect of Zeus adds its own bash-bolt VFX).
**Rejected so nobody re-finds them:** `hP0LMnfeAbc`, `yYbNOJJw7-8`, `oQqffStHfn8`, `bwiOXXHZdv4`, `4t0g8i0qXxI` (all **Lightning Rod** duo — lodged-Cast pulses, not chain) · `wrfDgyqJXk0`, `TsuWYCfk7Cc`, `773D5Qibaq0`, `FSTrLSKhQ_8`, `7O3pCiwGJLo`, `dzSRXl8iolQ`, `ymw-L2R22oE` (Hades II) · `yY_LoPhRnMA` (VERIFIED as running the `hades-OneGodOnly` mod) · `QvYp_SWney8` (exact boon match but **40 Heat**).

---
## TABLE A — deployment facts as observed (one row per skill)

`BH` figures carry the grade of their scale anchor (§ 2): D2 and Hades are DERIVED from VERIFIED+MEASURED anchors; GD, PoE and LE body heights are INFERRED.

| # | Game · Skill | Source URL (best footage) | Timestamp | Footage verdict | **DELIVERY** | **ORIGIN** | Telegraph | Flight/travel | Footprint (BH) | Duration | **Cadence** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | D2 · **Frozen Orb** | [b5a-iIras34](https://www.youtube.com/watch?v=b5a-iIras34) | ≈3025 s | CLEAN (in use) | **projectile** (constant speed, no decay; pierces actors, stops at obstacles) | **caster socket** (`cast_release`) | **Y — 1.0 s cast delay** + `ice_cast_3` overlay 15 fr ≈0.60 s | **4.87 BH/s · 5.84 BH · 1.20 s** | orb body UNKNOWN; travel bolt 8.76 BH max, nova bolt 11.68 BH max | orb 1.20 s; bolts 1.00 s | **25 Hz — every single frame, PERFECTLY REGULAR**; 3.37 bolts/revolution; expiry = **16 radial bolts** |
| 2 | GD · **Blackwater Cocktail** | [ThO5dWZzyzY](https://www.youtube.com/watch?v=ThO5dWZzyzY) | **3:17** ✅ | CLEAN (inferred) | **lobbed-to-point** (`ProjectileGrenade`, `launchAngle 18°`; **can bounce**) | **cursor point** (`TargetGroundOnly = True`) | Y — `Throw` anim; cast shake 0.12 | **18 m/s; 0.83 s @ max range 15 m = 8.33 BH** | field dia **2.78 BH** (r1) → **6.44 BH** (r12) → **7.11 BH** (r22) | pool **2.5 / 4.5 / 6.5 s** by rank; **scorch decal 12.0 s** | **1 Hz flat (`targetInterval 1000 ms`), PERFECTLY REGULAR**; particle lick cadence UNKNOWN |
| 3 | PoE · **Poisonous Concoction** | [ZRVed04RsJE](https://www.youtube.com/watch?v=ZRVed04RsJE) | **0:23** ✅ | CLEAN (inferred) | **lobbed-to-point**, **but can collide with an enemy body mid-flight**; trajectory shape UNKNOWN | **cursor point** (ground-targeted) | Y — attack anim ≈0.87 s | 12 m/s; **0.55 s** at ≈6.6 m; cap 15 m = 8.33 BH | burst **1.00 BH radius / 2.00 BH diameter** (18 u = 1.8 m) | **INSTANT — no duration of any kind** | **N/A — single burst, no ticks** |
| 4 | LE · **Lightning Blast** | [AMXRR3QVpFY](https://www.youtube.com/watch?v=AMXRR3QVpFY) | **0:29** ✅ | CLEAN (inferred) | **instant-target** (target-snapped, homing; arc drawn between endpoints) | **caster → struck enemy** (needs a target; falls through to crates) | minimal; 0.682 s cast | **none — instant** | bolt width **UNKNOWN**; hop range **3.3–3.9 BH** (6–7 m, INFERRED) | bolt life UNKNOWN | **0 chains cold → +1 per cast in last 4 s → cap +2**; hop delay ≈**0.10 s** (INFERRED) |
| 5 | LE · **Healing Hands** | [n-IYQnoqpV8](https://www.youtube.com/watch?v=n-IYQnoqpV8) | ~0:10 | likely CLEAN | **instant burst at a TARGET POINT** — *not* self-cast, *not* an aura | **cursor ground point** (`Homeward` node exists to force self-centring) | Y — 0.682 s cast | none | radius **UNKNOWN** (EHG does not publish it; *"medium sized"*) | **INSTANT.** Cooldown 0. The 3 s is a **HoT buff on recipients** | **N/A — one shot, no pulses** |
| 6 | Hades · **Zeus chain** (Lightning Strike) | [1V9Qkmoaxng](https://www.youtube.com/watch?v=1V9Qkmoaxng) | **0:59 / 1:36** ✅ | UNKNOWN | **on-hit proc → travelling HOMING ball** (**not** instant, **not** a drawn arc) | **struck enemy** (`FireFromVictimLocation = true`); **no bolt from the player** | none — procs off the melee swing | **10.83 BH/s**; total budget 3.76 BH | **no beam, no width** — sprite ball `Scale 0.45` at `OffsetZ 70` = **0.51 BH** above ground; hop range **4.48 BH** | ball persists past its jumps (`Fuse 0.3 s`); impact flash **0.47 s** | **4 hops**; **no delay field exists** — cadence is **travel time**: ~0.13 s @200 u, **0.20 s @300 u**, 0.41 s @620 u. Proc cap 6/s |

### What the source shows that a text description misses

| # | Skill | The thing you only learn from the data/footage |
|---|---|---|
| 1 | Frozen Orb | **The orb itself deals no damage** — no `Skill` field; it is a *pure emitter*. And **an impact-body sprite exists in the shipped data wired to nothing** (`frozenorbexplode` / `IceOrbExplode`, 16 frames). |
| 2 | Blackwater | **The flask is a physics body that can BOUNCE** (`physicsRestitution 1.0`). **The scorch decal outlives the flames by >10×** (12 s vs a 2.5–6.5 s pool). Burn duration (flat 3 s) and pool duration are **two different clocks**. |
| 3 | Poisonous Concoction | **There is no cloud.** `projectile_behaviour_only_explode = 1`. Any green ground in footage is **Alchemist's Mark / Plague Bearer / map ground**. Green is an engine flag (`visual_hit_effect_chaos_is_green = 1`), not an inference. |
| 4 | Lightning Blast | **The chain count is not a constant** — it ramps 0→1→2 with recent casts. The single bolt only appears after a ≥4 s pause. |
| 5 | Healing Hands | **It is placed, not centred.** Proven by the existence of a node whose whole job is to centre it on you when the placement finds no ally. |
| 6 | Zeus chain | **It is a sprite BALL, not an arc** — and it **ignores terrain**, **turns twice as hard as the Cast version**, **persists after its jumps are spent**, and can **re-hit a foe it already hit**. |

---

## TABLE B — spec vs source

> **⚠ SPEC BASELINE — the specs moved under me while I worked.** I read all six at **≈ 10:07** and compared against that state. The conductor edited three of them concurrently: `frozen_orb.json` and `poisonous_concoction.json` at **10:13**, `healing_hands.json` at **10:19** (verified by mtime + `git diff`; my own access was read-only `cat` throughout). **The edits are rendering-level and none of them changes a verdict below** — `frozen_orb` moved its jitter from `{2,3}` to `{2,4}` balanced shuffle and added `expiry_mode: nova` / `expiry_decal: false` (which my § 3 finding **CONFIRMS**); `healing_hands` narrowed `radius_px` 220 → 160; `poisonous_concoction` gained cloud-rendering parameters.
>
> **That last one is worth pausing on.** `poisonous_concoction` acquired `rendered_cloud`, `density 0.6`, `erode_noise 0.4`, `roil_uv_per_s 0.05` — further investment in **a cloud the source does not have** (§ 5). The drift makes that finding more urgent, not less: the longer the cloud is tuned, the more expensive removing it becomes. Re-check the live files against this table before re-authoring.


**CONFIRMED** = source agrees · **CORRECT-TO(x)** = source disagrees, x is the sourced value · **UNKNOWN** = not resolvable from any source reached · **HOUSE** = a deliberate deviation of ours, not a source fact (must be re-declared as such, not carried as "source observation").

px columns assume **1 BH = 130 px**; re-scale from BH if the C-5 px space differs.

### 1 · `frozen_orb` — grammar **G1 CONFIRMED**

| Field | Spec | Verdict |
|---|---|---|
| `grammar` G1 / `origin_socket` cast_release / `aim_rule` release-locked | — | **CONFIRMED** |
| `speed_px_s` 420 | | **CORRECT-TO(4.87 BH/s ≈ 632 px/s)** |
| `range_px` 630 | | **CORRECT-TO(5.84 BH ≈ 759 px)** |
| `expiry.time_s` 1.5 | | **CORRECT-TO(1.20 s)** — 30 frames @ 25 fps |
| `emission.schedule` "every 2–3 frames (seeded jitter, FF-08)" | | **CORRECT-TO(every 1 frame, 25 Hz, PERFECTLY REGULAR)** · the jitter is **HOUSE** |
| `emission` "3 per revolution" | | **CONFIRMED** — exactly 3.37 (`Param2 = 19` of 64) |
| `child_speed_px_s` 900 | | **CORRECT-TO(8.76 BH/s ≈ 1138 px/s)** |
| `child_range_px` 260 | | **CORRECT-TO(8.76 BH ≈ 1138 px max)** — bolts die on first contact, so 260 px may be right *in practice*; as a **max** it is 4.4× low |
| `child_life` 0.3 s | | **CORRECT-TO(1.00 s max)** |
| `on_expiry` "shard_burst 16 radial" | | **CONFIRMED** — exactly 16 |
| impact body: none | | **CONFIRMED** — and D2's own unused `frozenorbexplode` asset corroborates the choice |
| `pierce` -1 | | **CONFIRMED for actors; CORRECT-TO(stops at obstacles/walls)** |
| `expiry_burst` 3.0 BH | | **CORRECT-TO** — not a fixed body; 16 bolts spraying to **11.68 BH** |
| `residue` P_ice_crown 0.6 s | | **UNKNOWN** — no residue/decal in D2 data for this skill |
| orb body 0.9 BH | | **UNKNOWN** — `Size = 1` is a collision class, not a sprite dimension → footage |

### 2 · `blackwater_cocktail` — grammar **G2 CONFIRMED**

| Field | Spec | Verdict |
|---|---|---|
| `grammar` G2 / `aim_rule` ground-locked / lobbed | — | **CONFIRMED** (`TargetGroundOnly = True`, `ProjectileGrenade`, `launchAngle 18°`) |
| `range_px` 520 | | **CORRECT-TO(15 m = 8.33 BH ≈ 1083 px)** |
| `arc.flight_s` 0.55 | | **CONFIRMED at the spec's own range**; **CORRECT-TO(0.83 s)** at max range. Flight = distance ÷ 18 m/s |
| `arc.apex_px` 180 | | **UNKNOWN** — `launchAngle 18°` is the only arc datum |
| `field.radius_px` 150 (dia 2.3 BH) | | **CORRECT-TO(2.78 BH @rank 1 / 6.44 BH @rank 12 / 7.11 BH @rank 22)** — **spec must state a rank** |
| `field.duration_s` 3.0 | | **CORRECT-TO(2.5 / 4.5 / 6.5 s by rank)** — 3.0 matches no rank |
| `tick_schedule_s` [0,.3,.95,1.25,2,2.7], `tick_cv_min` 0.25 | | **CORRECT-TO(flat 1000 ms, CV = 0)** · the CV floor is **HOUSE** |
| impact/field share one radius | | **CONFIRMED** — only one radius field exists |
| `residue` scorch decal 1.0 s | | **CORRECT-TO(12.0 s, fadeAfter 11.0 s)** — off by >10× |
| `projectile` "RGB flask, material glass" | | **CONFIRMED** — mesh is literally `boozebottle_molotov01.msh`, sound is the potion-drop sound |
| `impact` "3 glass shards" | | **UNKNOWN** — shard geometry is in unopened `.pfx` inside the `.arc` |
| `field` "P03 body + 3 P01 licks pulsing on the tick schedule" | | **CORRECT-TO** — field is a **ground decal + particles** (`terrainOnly = True`), and the **lick cadence is NOT the damage cadence** |
| bounce | *not modelled* | **ADD — the flask can bounce** (`physicsRestitution 1.0`) |

### 3 · `poisonous_concoction` — grammar **G2 BROKEN**

| Field | Spec | Verdict |
|---|---|---|
| `grammar` **G2 (lobbed field)** | | ⚠ **CORRECT-TO(lobbed BURST — no field)** |
| `aim_rule` ground-locked | | **CONFIRMED**, with the caveat that it **can hit a body mid-flight** |
| `field.kind` "density_cloud" | | ⚠ **CORRECT-TO(none — no cloud exists)** |
| `field.duration_s` 2.0 | | ⚠ **CORRECT-TO(0 — no duration stat on the gem)** |
| `tick_schedule_s` (5 ticks), `tick_cv_min` 0.25 | | ⚠ **CORRECT-TO(no ticks — single instantaneous burst)** |
| `field.radius_px` 170 / `cloud_diameter` 2.6 BH | | **CORRECT-TO(1.00 BH radius / 2.00 BH diameter)** — 18 units = 1.8 m. Closest of all the spec's geometry |
| `range_px` 480 | | **CONFIRMED as plausible** (≈6.6 m); hard cap is 15 m = 8.33 BH. Ground-target clamp **UNKNOWN** |
| `arc.flight_s` 0.5 | | **CONFIRMED** — 6.6 m ÷ 12 m/s = 0.55 s |
| `arc.apex_px` 160 | | **UNKNOWN** — and the mid-flight body collision argues *against* a high lob |
| `residue` puddle decal 1.5 s | | ⚠ **CORRECT-TO(none)** — a puddle in footage is Alchemist's Mark / Plague Bearer |
| `projectile` "RGB flask (green glass)" | | **CONFIRMED** — flask is visually attached to the belt; green is an engine flag |
| `impact` "viscous lobes ×4" | | **UNKNOWN** — GGG's own MTX copy calls the default explosion a **mist**, not a splash |
| projectile count 1 | | **CONFIRMED** — no projectile-count stat exists on the gem |

### 4 · `lightning_blast` — grammar **G3 CONFIRMED**

| Field | Spec | Verdict |
|---|---|---|
| `grammar` G3 / `instant: true` / `aim_rule` target-tracking | | **CONFIRMED** (four independent lines of evidence) |
| `chain.count` 1 | | **CORRECT-TO(0 cold → +1 per direct cast in last 4 s → cap +2)** — not a constant |
| `chain.hop_delay_s` 0.05 | | **CORRECT-TO(≈0.10 s)** — INFERRED from *"every 0.1 seconds"* |
| `chain.hop_range_px` 220 (1.69 BH) | | **CORRECT-TO(≈3.3–3.9 BH, 6–7 m)** — INFERRED |
| `range_px` 560 (4.31 BH ≈ 7.8 m) | | **CONFIRMED as plausible** — target-search radius is 7 m |
| `width_px` 22 (0.17 BH) | | **UNKNOWN** — no source states a bolt width → footage |
| bolt = jittered polyline + branch junctions | | **UNKNOWN for art**; base skill **does not fork** (forking is `Divergence`) — so *branching* is unsupported |
| `residue` none, afterimage 0.15 s | | **UNKNOWN** |
| `bolt_life` 0.12 s | | **UNKNOWN** |
| cast rate | *not in spec* | **ADD — 1.467/s (0.682 s per cast)** |

### 5 · `zeus_chain` — grammar **G3 BROKEN (delivery and treatment)**

| Field | Spec | Verdict |
|---|---|---|
| `origin` = struck enemy, on-hit proc | | ✅ **CONFIRMED** (`FireFromVictimLocation = true`) |
| no bolt from the player | | ✅ **CONFIRMED** |
| `chain.count` 4 | | ✅ **CONFIRMED** (`NumJumps = 4`) |
| `instant: true` | | ⚠ **CORRECT-TO(NOT instant — a travelling HOMING projectile at 10.83 BH/s)** |
| bolt = "P05 chain link ×N along a jittered polyline" | | ⚠ **CORRECT-TO(no polyline — an additive sprite BALL, `Scale 0.45`, at 0.51 BH above ground, shedding a random jagged sprite every ~0.07 s)**. The drawn-bolt look is Hades' **SKY** family |
| `width_px` 30 (0.23 BH) | | ⚠ **N/A — there is no beam, so there is no width** |
| `hop_delay_s` [0.06,0.11,0.08,0.13] (Σ 0.38), `hop_delay_cv_min` 0.25 | | ⚠ **CORRECT-TO(no delay field exists; cadence = travel time ≈0.13–0.41 s/hop, ~0.20 s typical)** · the authored CV is **HOUSE** |
| `hop_range_px` 260 (2.0 BH) | | **CORRECT-TO(4.48 BH ≈ 582 px)** — `JumpRange 620` u |
| `range_px` 520 | | **CONFIRMED** — `Range = 520` u = 3.76 BH ≈ 488 px (near-coincidence of numeral and value) |
| `phase_envelope.total` 0.65 s | | **CORRECT-TO(≈0.8 s for four hops at ~0.2 s, plus a 0.47 s impact flash per hop)** |
| `impact per hop` strike flash + 2 prongs | | **CORRECT-TO(`ProjectileLightningBallEnd`, 28 frames @60 fps = 0.47 s, Scale 0.55)** |
| `target_order` "events (nearest unhit)" | | **CORRECT-TO** — the Attack chain omits `MultipleUnitCollisions = false`, so it **can re-hit an already-hit foe** |
| damage falloff | *not in spec* | **ADD — `JumpDamageMultiplier 0.8`, compounding** |
| proc rate | *not in spec* | **ADD — `Cooldown 0.167 s` → max ~6 procs/s** |

### 6 · `healing_hands` — grammar **G4 BROKEN (every element)**

| Field | Spec | Verdict |
|---|---|---|
| `grammar` **G4 (self aura loop)** | | ⚠ **CORRECT-TO(one-shot instant burst at a target point)** |
| `origin_socket` caster_root / `aim_rule` owner-tracking | | ⚠ **CORRECT-TO(cursor ground point)** — proven by the `Homeward` node |
| `duration_s` 4.0 | | ⚠ **CORRECT-TO(instantaneous; cooldown 0)** |
| `pulse_schedule_s` (6 pulses), `pulse_cv_min` 0.25 | | ⚠ **CORRECT-TO(no pulses at all)** · the CV floor is **HOUSE** |
| `stack` refresh | | **CONFIRMED in spirit** — the 3 s "lingering warmth" HoT is non-stacking and refreshes |
| `radius_px` 220 (ring dia 3.4 BH) | | **UNKNOWN** — EHG does not publish it; *"medium sized"*; ~3–4 m is a working guess only |
| `aura body` P06 broken ring ×5 orbiting at the feet, `ring_orbit_period` 2.6 s | | ⚠ **CORRECT-TO** — a **golden ring at the target location**; no orbit, no loop (SECONDARY, thin) |
| `seal` "interrupted seal decal under the caster" | | ⚠ **UNKNOWN / unsupported** — no source describes a glyph, seal or rune; and it is not under the caster |
| `pulse` P_holy_ray petals ×6 rising per pulse | | ⚠ **CORRECT-TO(single burst, one visual)** |
| enemy damage | *implied* | ⚠ **CORRECT-TO(none at base)** — requires the `Searing Light` node |
| cast time | *not in spec* | **ADD — 0.682 s (Base Speed 1.467/s), cooldown 0** |

---
## 9. FOR MATT TO SOURCE — what a human still has to look at

Matt offered to source. **Nothing on this list is a footage-hunting failure** — every one of the six skills has a usable candidate with a timestamp. These are the questions that *cannot* be answered from any text or data source and genuinely need eyes on a frame (or, in two cases, a machine that owns the game).

**A. Frame-step questions — a person with the YouTube player, at the timestamps in § 1a.** (Under option c′: pause, then `,` / `.` to step.)

| # | Skill | Question | Where |
|---|---|---|---|
| 1 | Frozen Orb | **Orb body size in BH** (spec says 0.9). `Size = 1` is a collision class, not a sprite dimension | [b5a-iIras34](https://www.youtube.com/watch?v=b5a-iIras34) @≈3025 s |
| 2 | Lightning Blast | **Does the bolt show a visible sweep/whip-out over 1–3 frames, or does it appear fully formed?** The engine is target-snapped, but the presentation layer may animate anyway — **do not read "not a projectile" as "zero motion"** | [AMXRR3QVpFY](https://www.youtube.com/watch?v=AMXRR3QVpFY) @0:29 (dummy) |
| 3 | Lightning Blast | **Bolt width vs the figure**, and whether the art branches | same |
| 4 | Blackwater | **Do glass shards visibly spawn on shatter?** And the **particle flame-lick cadence**, which is *not* the 1 Hz damage tick | [ThO5dWZzyzY](https://www.youtube.com/watch?v=ThO5dWZzyzY) @3:17 |
| 5 | Poisonous Concoction | **Trajectory shape — high lob or flat?** No source anywhere describes it, and the documented mid-flight body collision argues against a high lob | [ZRVed04RsJE](https://www.youtube.com/watch?v=ZRVed04RsJE) @0:23 |
| 6 | Zeus chain | **Confirm the ball reading** — that hops are a travelling mote, not a drawn arc | [1V9Qkmoaxng](https://www.youtube.com/watch?v=1V9Qkmoaxng) @0:59 / 1:36 |

**B. Two numbers that need the game, not a video.**

| # | Skill | Question | Cheapest route |
|---|---|---|---|
| 7 | **Healing Hands — base radius** | The one load-bearing number nobody publishes. EHG omits it while listing radii for sibling skills in the same article, so it is a deliberate omission, not a retrieval failure | **Read the in-game tooltip**, or open [lastepochtools.com/skills/healing_hands](https://www.lastepochtools.com/skills/healing_hands) **in a browser** (Cloudflare-blocked to agents, fine for a human) |
| 8 | **Healing Hands — post-1.4 appearance** | Patch 1.4 (2026-03-26) says *"Updated the visual effect for Healing Hands"* and describes nothing. **All findable footage predates it** | Cast it in-game, or find post-2026-03-26 Paladin footage |

**C. One judgement call that is Matt's or gandalf's, not mine.**

| # | Question |
|---|---|
| 9 | **Is FF-08's anti-metronome jitter still wanted, now that we know every source cadence is a clean metronome?** See § 0(b) and § 10. This is a register decision, not a research finding — I can only report that the sources do not support it. |

**Two things I could NOT find, stated plainly:**
- **No official developer video exists showing Healing Hands or Lightning Blast.** EHG's channel has a soundtrack track and two 2021/2022 dev streams; the Feb 2024 skill-tree reveal shipped as a **forum blog post, not a video**, which is why the four "reveal" videos are blog readthroughs with planner screenshots and no gameplay. **Crate likewise has no Blackwater skill-showcase video** — their channel is interviews and community Let's Plays.
- **No dedicated "one clean cast per new gem" showcase exists for PoE 3.16.** The channel that makes that format did 3.15 but not 3.16. No hideout/target-dummy isolation test was found for Poisonous Concoction.

---

## 10. Knowledge gaps not resolved

1. **The FF-08 jitter has no source basis** (§ 0b). Frozen Orb: every frame, 25 Hz, regular. Blackwater: flat 1000 ms. Neither shows jitter; Poisonous Concoction and Healing Hands have no repeating cadence at all to jitter. **Three of the four spec files carrying a `*_cv_min: 0.25` describe a cadence the source does not have — and two of them describe a cadence that does not exist.**
2. **Body height is undocumented in three of the four source games** (GD, PoE, LE). D2 and Hades have solid anchors; the rest are INFERRED at ~1.8 m and every BH figure derived from them inherits that. **The meter/unit mapping is VERIFIED in all three**, so re-scaling is one multiplication if a better height appears.
3. **Particle-level detail is unread in two games.** Grim Dawn's `.pfx` files live inside packed `.arc` archives that were not opened (flame-lick cadence, glass shards). A follow-on probe could open them — it is the same lane as the 2026-07-23 `.arz` work and would be mapped territory, i.e. crawler-shaped rather than mine.
4. **Hades data is v1.0 (Aug 2020); retail is v1.38.** The wiki independently corroborates bounce counts, ranges and spark speed, so no drift is evident — but that is corroboration, not a retail read.
5. **Lightning Blast's base chain range and hop delay are both INFERRED** from a stat line (*"Hit nearest enemies every 0.1 seconds in 7 meter radius"*) whose semantics EHG does not document, and which also appears on Elemental Nova where it plainly is not a chain range.
6. **Healing Hands' VFX radius may not equal its gameplay radius** — an unresolved community bug report claims area modifiers grow the animation without growing the effect. **So measuring the ring off footage may not yield the real number either.**
7. **PoE ground-target throw clamp** — only the engine-wide 15 m projectile cap is documented; whether the cursor clamp is tighter is unknown.

## 11. Lane notes (for whoever researches these sources next)

- **`poewiki.net` is dead to agents** — Anubis proof-of-work on every endpoint including `api.php`. **Not circumvented** (that would be defeating an anti-bot control). Substitute lane: **RePoE + Path of Building dumps for mechanics, poedb for patch history, search-index snippets for wiki prose** — which outperformed the wiki on this probe anyway.
- **Last Epoch: `lastepochtools.com` and `lastepoch.fandom.com` are Cloudflare-blocked, but EHG's Zendesk API is wide open** and is a *primary* source: `support.lastepoch.com/api/v2/help_center/en-us/articles/<id>.json`. Mage Skills `46363062648987` · Mage Skill Tree `46362122141467` · Paladin Skills `46363175035035` · Paladin Skill Tree `46362493169691` · Common Terminology `46361668314523`. **Route all LE lookups here.**
- **`lastepoch.fandom.com` is ~6 years stale and actively dangerous** — node names survive with inverted effects.
- **Hades wiki HTML returns 402; `?action=parse&prop=wikitext` works.**
- **YouTube watch pages return only the SPA shell to `WebFetch`.** What works: **the oEmbed endpoint** (`youtube.com/oembed?url=…&format=json` — title + channel, reliable) and **curl + parsing `ytInitialPlayerResponse` / `ytInitialData`** for duration, upload date, description and chapter markers. Pinned comments remain unreadable.
- **Published thumbnails (`i.ytimg.com/vi/<id>/maxresdefault.jpg`) are fetchable and viewable** and are within the already-authorised evidence class — but **they are frequently title cards**. Verified this session on `RPJK4SSFZ0c`, which is a title card. Low yield; use only to confirm a video is a dedicated single-skill clip.
- ~~**`yt-dlp` is not installed on this host**, which is what settled option c′ in practice.~~ ⛑ **CORRECTED 2026-09-16 (second pass): it IS installed, as a module.** `which yt-dlp` fails; `python3 -m yt_dlp --version` returns **2026.08.19**. The original line was true of `PATH` and false of the host — an instrument answering a narrower question than the one asked. `ffmpeg` is present (`/opt/homebrew/bin/ffmpeg`), as is `ffprobe`; `numpy` 2.4.6 and `PIL` 10.3.0 are available for numeric frame measurement.

---

## 12. Frame measurements (downloaded, class E)

> **ADDENDUM, 2026-09-16 (second pass).** legolas Mode A, commissioned by gandalf (RUN-CONDUCTOR, Run C-5). This section is the resumption of the run that was STOPPED for filling the disk. It answers the § 9-A frame-step questions (1–6), the § 9-B appearance question (8), and Matt's added question about the dark lingering ground under Poisonous Concoction.
>
> **Sourcing class:** Matt 2026-09-12 option **(b)** — private measurement only. Clips live on the Desktop under `~/Desktop/class-E/2026-09-16-e3-deployment/`, never in the repo, never a burst input (`canonical/matt_decision_needed/2026-08-25-youtube-frame-extraction-sourcing-class.md`). **No frame, clip or derivative is copied into any repo.** Everything below is a *number or a description* derived from private viewing.
>
> **Disk discipline honoured.** `df -h /` before every extraction; free space never below 46 GB (floor was 20 GB). **No new downloads were needed** — every clip required was already on disk from the first pass. Frames were JPEG (`-q:v 3`/`-q:v 2`), windowed, and pruned to ≤ 12 keepers per question immediately after measurement. **Total added: ~33 MB** against a 2 GB budget.
>
> **Lane-note correction to § 11.** `yt-dlp` **is** on this host after all — not on `PATH`, but installed as a module: `python3 -m yt_dlp` reports **2026.08.19**. § 11's *"`yt-dlp` is not installed on this host"* was true of `which yt-dlp` and false of the host. It did not matter this pass (nothing needed downloading), but the next probe should not re-derive it.

### 12.0 Method, and what "MEASURED" means here

**Instruments.** `ffmpeg` for windowed JPEG extraction and for contact-sheet montages (`tile=`); `numpy`/`PIL` for thresholded bounding boxes, per-column thickness profiles, and brightness time-series; detrended autocorrelation for cadence. Eyeball readings were taken only off zoomed crops carrying a **drawn scale bar of known pixel length** composited by `ffmpeg` before cropping, so every "eyeball" figure is a comparison against a ruler, not a guess.

**BH is measured per clip, from that clip's own player sprite** (head-top to lowest foot), because every capture has its own camera zoom. These anchors carry every BH figure in this section:

| Clip | Game | Capture | **BH (px)** | How |
|---|---|---|---|---|
| `alt_RPJK4SSFZ0c_full.mp4` | D2R | 1920×1080 | **228 ± 5** | scale bar, standing Sorceress @26 s |
| `clip_ThO5dWZzyzY_0317.mp4` | Grim Dawn | 1920×1080 | **83 ± 4** | scale bar, standing Inquisitor on sand @12 s |
| `clip_ZRVed04RsJE_0023.mp4` | PoE | 1920×1080 | **137 ± 5** | scale bar, standing Ranger @8 s |
| `alt2_vQGkaa0Uax0_end.mp4` + `alt_vQGkaa0Uax0_intro.mp4` (same video) | Last Epoch | 1920×1080 | **134 ± 6** | scale bar, standing Mage @intro 30 s |
| `clip_n-IYQnoqpV8_full.mp4` | Last Epoch | 1920×1080 | **119 ± 5** | scale bar, standing Paladin @88.7 s |
| `alt_XPs-jypdwx8.mp4` | Hades | 1920×1080 | **180 ± 15** | scale bar, Zagreus in the Hades dialogue @34 s |

**Confidence scale used in the tables:** **HIGH** = numeric, repeated across ≥3 frames, uncontaminated background · **MED** = numeric but single-cast, or contaminated by overlapping VFX · **LOW** = visual class only, or a figure whose anchor is itself shaky.

**A caution that outranks every number below.** Every game here composites VFX with bloom. A thresholded bounding box measures **what the player sees**, which is the right quantity for a presentation spec — but it is *not* the hitbox, and where the source data gives a hitbox (Poisonous Concoction, Blackwater) the two are reported side by side and they differ.

---

### 12.1 Per-question results

| # | Question | Clip | Frames (t, s) | **Measurement** | Conf. |
|---|---|---|---|---|---|
| **1a** | **Frozen Orb — orb body size in BH** | `alt_RPJK4SSFZ0c_full` | 21.67–21.92 (7 consecutive @23.976 fps) | Cyan ring bbox stabilises at **182 × 170 px**. BH 228 → **0.80 BH wide × 0.75 BH tall**. Reaches full extent in ~5 frames (**0.21 s**) from spawn. Spec's `0.9 BH` is **~12 % high**. | **HIGH** |
| **1b** | **Frozen Orb — the expiry nova's look** | same | 22.88 / 22.96 / 23.04 | A radial spray of **discrete faceted ice DARTS** — kite/arrowhead crystal heads with a glowing tapered tail — leaving a bright core flash, all hugging the ground plane. **No expanding ring, no shockwave disc, no ground decal.** One dart ≈ **153 × 27 px = 0.67 BH long × 0.12 BH wide**. | **HIGH** (form) / **MED** (dart dims) |
| **2** | **Lightning Blast — sweep/whip-out, or fully formed?** | `alt2_vQGkaa0Uax0_end` (60 fps) | 28.017 → 28.033 | **Fully formed. No sweep, no whip-out.** Bright-pixel count in a 460×120 box well beyond the caster goes **24 → 2 866 in ONE 16.7 ms frame**, then 3 600–4 100 for eight more. There is no partial-extension frame. **New fact the spec does not carry: the polyline is RE-RANDOMISED every frame** — the path differs frame-to-frame for the whole life of the bolt. Life: **0.150 s at full brightness, fading to zero by ≈0.22 s**. | **HIGH** |
| **3** | **Lightning Blast — bolt width vs figure; branching?** | same | 28.047 (6 x-slices, 3 thresholds) | Hard core **3–6 px**; the visible strand band incl. filaments **8–16 px**; up to **24 px** where two strands overlap. BH 134 → **core 0.02–0.05 BH, band 0.06–0.12 BH**. Spec's `22 px / 0.17 BH` is **too wide for a strand, about right for the whole band**. **Branching: YES in the art** — short filaments fork off and **rejoin**, with 2–3 near-parallel strands at the caster end. There is **no tree to separate endpoints** (that remains `Divergence`-only, § 6). | **HIGH** (width) / **MED** (branch classification) |
| **4a** | **Blackwater — glass shards on shatter?** | `clip_ThO5dWZzyzY_0317` (60 fps) | 14.35–14.60, incl. gamma-lifted zooms | **NOT RESOLVABLE at 1080p/60.** The shatter reads as a white-hot bloom + radiating light streaks + **an expanding pale elliptical GROUND RING (shockwave)**, resolving into flame. Two or three small dark slivers are present but cannot be separated from scene debris or mob gibs. **Footage has now been tried and has failed** — the remaining route is the `.pfx` inside the packed `.arc` (§ 10.3). | **LOW** (as a negative) |
| **4b** | **Blackwater — particle flame-lick cadence** | same | 15.5–18.83 (200 frames @60 fps) | Fire-pixel count, detrended (31-frame MA), autocorrelated: first zero-crossing **lag 5 (0.083 s)**, trough **lag 9 (0.150 s)**, secondary peaks at **lag 18 (0.300 s)**, **lag 33–34 (0.55–0.57 s)**, **lag 67 (1.117 s)**. → characteristic period **≈ 0.28–0.30 s (≈ 3.3–3.6 Hz)**, with **low coherence** (repeat-lag autocorrelation only +0.10 to +0.25). **It is turbulent flicker with a characteristic timescale, not a pulse train** — and it is emphatically **NOT** the 1 Hz damage tick. | **MED** |
| **4c** | **Blackwater — pool look** | `alt_jRLXuRw9VIA_skilldisplay` | 108.0 / 110.5 | A **low, dense, boiling disc** of orange-yellow flame with a **white-hot centre**, ragged orange fringe, **short turbulent tongues rather than tall discrete licks**, and a red-orange outer glow. Measured ≈ **279 px across vs a ≈71 px figure → ≈ 3.9 BH** at that build's (unknown) rank. After burnout the **scorch decal is an irregular dark smudge with soft edges** — *not* a clean circle — with faint smoke wisps and a few residual flame licks; ≈ **229 px vs ≈53 px figure → ≈ 4.3 BH**. | **MED** (form) / **LOW** (BH figures — the anchor in that clip is coarse) |
| **5a** | **PConc — lob height / trajectory** | `clip_ZRVed04RsJE_0023` (60 fps) | 98.32–98.40 | The flask's trail is a **single tapered comet streak**, visible for only **2–4 frames**, entering the impact at a **shallow screen angle (≈25–30° below horizontal)** from the throwing side. **No high overhead drop; no steep descent.** This corroborates § 5's inference from the documented mid-flight body collision. The projectile body itself is 1–2 px and could not be tracked to an apex. | **MED** |
| **5b** | **PConc — the burst look** | same | 96.85–97.20 | An **instantaneous acid-green bloom**: a **vertical geyser of jagged green plumes** at the contact point, **plus long curved green whip-arcs sweeping outward along the ground**, with a bright yellow-green core where it hit. **No cloud. No ground decal. No puddle.** Green-pixel count **0 → 44 341 in ≤1 frame**, under 5 % of peak by **0.25 s**, at background by **0.30–0.35 s**. Peak VFX extent **473 × 404 px** (bright body 408 × 373). BH 137 → **3.45 × 2.95 BH** full / **3.0 × 2.7 BH** bright — against a documented **damage diameter of 2.00 BH**. **The VFX is ≈1.5–1.7× the hitbox.** | **HIGH** |
| **5c** | **PConc — Matt's question: what makes the dark lingering ground?** | control: `clip_ZRVed04RsJE_0023` · endgame: `alt_eErJwp8iP0w_mapping` | control 96.85–99.8 · endgame 138–156, 186–187 | **See § 12.3 below — it is Plague Bearer, and it is not a ground effect at all.** | **MED–HIGH** |
| **6a** | **Zeus — travelling ball, or drawn arc?** | `alt_XPs-jypdwx8` (60 fps) | 44.50–44.62 (8 consecutive) | **TRAVELLING BALL — confirmed decisively.** A solid round yellow sphere with a white-hot core, translating in a straight line, **casting its own dark shadow on the ground directly beneath it**, with a jagged black-and-yellow lightning-bolt sprite **shed BEHIND it and lagging** — the trail follows the ball, it does **not** connect two enemies. The § 8 reading is right and the spec's "P05 chain link ×N along a jittered polyline" is wrong. | **HIGH** |
| **6b** | **Zeus — ball size in BH** | same | 44.50 | Saturated yellow disc **67 × 64 px**. BH 180 → **0.37 BH diameter**. Ball centre sits **≈43 px above its own shadow's centre = 0.24 BH in screen space** (world height 0.51 BH from the Hades data implies a camera-pitch factor ≈0.47 — internally consistent). **The shadow is drawn and is a build requirement: it is what sells the ball as airborne.** | **MED** (BH anchor ±15 px) |
| **6c** | **Zeus — impact flash look** | same | 45.18–45.31 | A **yellow-white spiky starburst** (5–8 radiating spikes) with a soft bloom. **No ring decal, no ground residue.** Consistent with the data's `ProjectileLightningBallEnd` (28 frames @60 fps = 0.47 s, Scale 0.55). | **MED** |
| **7** | **Healing Hands — the burst's look (PRE-1.4)** | `clip_n-IYQnoqpV8_full` (30 fps) ⚠ **PRE-1.4** | 88.75–89.15 (13 consecutive) | A **filled golden-white DOME / HEMISPHERE of light** rising from the ground: a bright hemispherical bubble with a **hard glowing rim arc** at its top edge, filled with **rising flame-like golden plumes**. **Not a ring. Not a broken ring. No orbiting elements. No seal or glyph decal. No petals.** Onset **0 → 9 224 bright px in ONE frame**; peak at **≈0.15 s** (29 400 px); **gone by 0.40 s**. Max extent **431 × 240 px**; BH 119 → **3.6 BH wide × 2.0 BH tall** (typical frames ≈400 px → 3.4 BH). | **HIGH** (form + timing) / **MED** (BH) |

**⚠ Standing caveat on row 7.** Patch **1.4 (2026-03-26) replaced the Healing Hands visual effect** and describes nothing (§ 7, § 9-B item 8). **Everything in row 7 is pre-1.4 and is marked as such wherever it is used.** It is authoritative for *what the skill looked like when the spec's source memory was formed*, which is exactly what the spec needs — but it is not current Last Epoch.

---

### 12.2 One number the conductor should see before re-authoring `healing_hands`

The spec's **original** `radius_px 220` (ring dia **3.4 BH**) matches the measured pre-1.4 dome (**3.4–3.6 BH**) almost exactly. The **2026-09-16 narrowing to `radius_px 160` (2.46 BH)** moves *away* from the footage, not toward it.

Two things blunt that, and both must travel with the number:
- **§ 10.6 stands** — a community bug report claims the Healing Hands VFX radius does not equal its gameplay radius. So 3.4 BH is a **VFX** figure, and EHG still publishes **no gameplay radius at all** (§ 9-B item 7, still open).
- **The dome is pre-1.4 art.** If the build is chasing *current* Last Epoch, this number is the wrong target; if it is chasing the register the spec was written from, it is the right one. **That is gandalf's call, not mine.**

**Also worth recording:** in the one cast measured, the dome's x-centre (917 px) sat **13 px from the player** and **113 px from the dummy** — i.e. this cast landed essentially on the caster. **This neither confirms nor refutes the placement finding**; § 7's proof that the skill is *placed, not centred* rests on the `Homeward` node's existence and stays exactly as strong as it was.

---

### 12.3 Matt's question — the dark lingering ground under Poisonous Concoction

**The short answer: it is Plague Bearer, and it is not a ground effect. Poisonous Concoction leaves nothing.**

**The control.** `clip_ZRVed04RsJE_0023` is a level-≈30 Act-3 character with the Labyrinth quest still unstarted — **no ascendancy** — whose skill bar carries **Poisonous Concoction and one movement skill, and nothing else**. Measured over a continuous 3 s window at 60 fps spanning four casts: every burst decays to background within **0.30–0.35 s** and **leaves nothing behind**. Residual green counts between casts (130–500 px) resolve to on-screen text and a corpse, not to ground. **In a build without Plague Bearer there is no lingering ground of any colour.**

**The endgame case.** `alt_eErJwp8iP0w_mapping` (Sentinel league, 4 078 life, full flask set) *does* show a large **dark-olive-to-black miasma with saturated green curved tendrils** persisting for seconds — this is the thing the question is about. Three observations identify it:

1. **It is player-anchored, not ground-anchored.** Sampled at 147 → 155 s, the green mass **translates with the player** and reforms as a **ring of curved tendrils centred on him**. A cast-point decal cannot do that.
2. **The build's skill bar carries a Plague Bearer gem** (the green swirling-miasma icon, top row of the bar, read off a 3× zoom of the skill bar at 151.5 s). The player-centred swirling-tendril ring is Plague Bearer's *Infecting* presentation.
3. **"Alchemist's Mark" is ruled out at source.** PoE's Pathfinder node is **Master Alchemist**, and it grants ailment application and ailment removal on flask use — **it creates no caustic ground**. There is no "Alchemist's Mark" node; the name appears to be a conflation.

**Measured, so the spec can name what it is NOT building:** the Plague Bearer miasma runs roughly **600 × 420 px at 1920** in that capture, a **dark olive/near-black body with a saturated green rim of long curved tendrils**, **multi-second**, and **present whenever the buff is up — not once per cast**. (Its per-cast independence is the decisive part: it does not pulse with the PConc cast rate, it simply persists.)

**What this means for the build — stated plainly, because it is a spec change and not a measurement.** The thing we measured for Poisonous Concoction is **the burst and only the burst**: instantaneous, ~0.3 s, acid-green, a vertical jagged plume plus curved ground whip-arcs, **3.0–3.5 BH of VFX over a 2.0 BH hitbox**, and **nothing left on the ground**. If C-5 wants a dark lingering ground under Poisonous Concoction, that is a **HOUSE addition** — a deliberate borrow from a *different skill in the same builds* — and it should be declared as one, in the same way § 0(b) asks FF-08's jitter to be declared. It should **not** be carried as a Poisonous Concoction source fact, because it is not one. This is the same defect shape as the `rendered_cloud` parameters flagged in the Table B preamble: **investment accumulating on a feature the source does not have.**

---

### 12.4 Table A rows that change from INFERRED / UNKNOWN to MEASURED

| # | Game · Skill | Column | Was | **Now** |
|---|---|---|---|---|
| 1 | D2 · Frozen Orb | Footprint (BH) | *"orb body UNKNOWN"* | **orb body 0.80 BH wide × 0.75 BH tall** (MEASURED) · spin-up to full extent 0.21 s |
| 1 | D2 · Frozen Orb | Cadence / expiry | *"expiry = 16 radial bolts"* (count VERIFIED, look unknown) | **look MEASURED: faceted ice darts, 0.67 × 0.12 BH each, from a core flash; no ring, no decal** |
| 2 | GD · Blackwater | Cadence | *"particle lick cadence UNKNOWN"* | **≈ 0.28–0.30 s characteristic period (3.3–3.6 Hz), LOW coherence — turbulent, not a pulse train** (MEASURED) |
| 2 | GD · Blackwater | Footprint / residue | field dia from data; residue look unknown | **field reads ≈3.9 BH at that build's rank; scorch decal is an irregular soft-edged smudge ≈4.3 BH** (MEASURED, LOW conf.) |
| 3 | PoE · PConc | Flight/travel | *"trajectory shape UNKNOWN"* | **shallow comet-trail entry ≈25–30° below horizontal; no high lob** (MEASURED-partial) |
| 3 | PoE · PConc | Footprint (BH) | burst 1.00 BH radius (damage, VERIFIED) | **VFX 3.0–3.5 BH across — ≈1.5–1.7× the hitbox** (MEASURED); **burst VFX life 0.30–0.35 s** |
| 4 | LE · Lightning Blast | Footprint (BH) | *"bolt width UNKNOWN"* | **core 0.02–0.05 BH; strand band 0.06–0.12 BH** (MEASURED) |
| 4 | LE · Lightning Blast | Duration | *"bolt life UNKNOWN"* | **0.150 s full + fade to ≈0.22 s** (MEASURED) · **appears fully formed in ≤1/60 s** · **polyline re-randomised every frame** |
| 5 | LE · Healing Hands | Footprint (BH) | *"radius UNKNOWN"* | **VFX dome 3.4–3.6 BH wide × 2.0 BH tall — PRE-1.4** (MEASURED) |
| 5 | LE · Healing Hands | Duration | *"INSTANT"* (gameplay, VERIFIED) | **VFX life 0.40 s: 1-frame onset, peak at 0.15 s, gone by 0.40 s** (MEASURED) — the gameplay is still instantaneous |
| 6 | Hades · Zeus chain | Footprint / Flight | ball reading DERIVED from data; footage verdict UNKNOWN | **ball CONFIRMED on frames: 0.37 BH sphere, 0.24 BH above its own DRAWN ground shadow, trail shed behind** (MEASURED) |

### 12.5 Table B rows that change

**1 · `frozen_orb`**

| Field | Was | **Now** |
|---|---|---|
| orb body 0.9 BH | **UNKNOWN** → footage | **CORRECT-TO(0.80 BH w × 0.75 BH h)** — MEASURED, HIGH |
| `on_expiry` "shard_burst 16 radial" | CONFIRMED (count) | **CONFIRMED and characterised** — faceted ice darts, not streaks; no ring; no decal in the 0.3 s observed (*not* an exhaustive residue check — `residue` stays UNKNOWN) |

**2 · `blackwater_cocktail`**

| Field | Was | **Now** |
|---|---|---|
| `field` "3 P01 licks pulsing on the tick schedule" | CORRECT-TO (cadence unknown) | **CORRECT-TO(≈3.3–3.6 Hz turbulent flicker, low coherence — and NOT the 1 Hz damage tick)** — MEASURED |
| `impact` "3 glass shards" | **UNKNOWN** → footage | **STILL UNKNOWN — footage tried and failed.** Not resolvable at 1080p/60; the shatter is bloom + light streaks + an expanding pale ground ring. Remaining route: the `.pfx` inside the `.arc` |
| `residue` scorch decal | CORRECT-TO(12.0 s) | **form MEASURED: irregular soft-edged dark smudge, not a clean circle; smoke wisps + residual licks** |

**3 · `poisonous_concoction`**

| Field | Was | **Now** |
|---|---|---|
| `arc.apex_px` 160 | **UNKNOWN** | **CORRECT-TO(low/flat — shallow ≈25–30° comet-trail entry)** — MEASURED-partial, MED |
| `impact` "viscous lobes ×4" | **UNKNOWN** | **CORRECT-TO(vertical jagged plume geyser + curved ground whip-arcs, acid-green, bright core)** — MEASURED |
| `residue` puddle decal 1.5 s | CORRECT-TO(none) — *reasoned* | **CORRECT-TO(none) — now MEASURED.** Four casts, 60 fps, ascendancy-free build: nothing survives 0.35 s. The dark ground in endgame footage is **Plague Bearer** (§ 12.3) |
| `field.radius_px` 170 / `cloud_diameter` 2.6 BH | CORRECT-TO(2.00 BH damage dia) | **unchanged for damage; ADD — VFX reads 3.0–3.5 BH, ≈1.5–1.7× the hitbox.** If the spec wants the *look*, 2.6 BH is closer than the hitbox figure — say which one the number is |
| `rendered_cloud` / `density` / `erode_noise` / `roil_uv_per_s` (conductor's 10:13 edit) | flagged as drift | **flag upheld and strengthened** — four casts measured, no cloud, no residue, nothing to roil |

**4 · `lightning_blast`**

| Field | Was | **Now** |
|---|---|---|
| `width_px` 22 (0.17 BH) | **UNKNOWN** | **CORRECT-TO(band 0.06–0.12 BH ≈ 8–16 px; core 0.02–0.05 BH ≈ 3–6 px)** — MEASURED, HIGH |
| bolt = jittered polyline + branch junctions | **UNKNOWN for art** | **CONFIRMED for art** — short filaments fork and **rejoin**, 2–3 parallel strands at the caster end. (Gameplay forking is still `Divergence`-only.) |
| `bolt_life` 0.12 s | **UNKNOWN** | **CORRECT-TO(0.150 s full + fade to ≈0.22 s)** — MEASURED |
| `instant: true` | CONFIRMED (four text lines) | **CONFIRMED on frames at 60 fps** — 24 → 2 866 bright px in one frame; no partial-extension frame exists |
| per-frame jitter | *not in spec* | **ADD — the polyline is re-randomised EVERY frame for the bolt's whole life.** This is a first-order look fact and the spec does not carry it |

**5 · `zeus_chain`**

| Field | Was | **Now** |
|---|---|---|
| bolt = "P05 chain link ×N along a jittered polyline" | CORRECT-TO(sprite ball) — from data | **CONFIRMED ON FRAMES.** Round sphere, straight-line travel, jagged bolt sprite shed *behind* and lagging |
| ball size | data `Scale 0.45` | **ADD — 0.37 BH measured diameter** (MED; BH anchor ±15 px) |
| ball height | data `OffsetZ 70` = 0.51 BH world | **ADD — 0.24 BH above its own shadow in screen space, and THE SHADOW IS DRAWN.** The shadow is what sells the ball as airborne; the spec does not mention it |
| `impact per hop` | CORRECT-TO(28 fr / 0.47 s) | **form MEASURED — yellow-white spiky starburst, 5–8 spikes, soft bloom, no ring, no residue** |

**6 · `healing_hands`** *(all rows PRE-1.4)*

| Field | Was | **Now** |
|---|---|---|
| `radius_px` 220 → 160 | **UNKNOWN** | **MEASURED(VFX dome 3.4–3.6 BH dia, pre-1.4)** — the original 220 matched; the narrowing to 160 does not. See § 12.2 for the two caveats that must travel with this |
| `aura body` P06 broken ring ×5 orbiting at the feet | CORRECT-TO (thin SECONDARY) | **CORRECT-TO(a FILLED golden-white dome/hemisphere with a hard rim arc and rising flame-like plumes) — no ring, no orbit, no broken elements** — MEASURED, HIGH |
| `duration_s` 4.0 | CORRECT-TO(instantaneous) | **unchanged for gameplay; ADD — VFX life 0.40 s (1-frame onset, peak 0.15 s)** |
| `seal` "interrupted seal decal under the caster" | UNKNOWN / unsupported | **CORRECT-TO(none observed)** — no glyph, seal, rune or ground decal in any of the 13 frames |
| `pulse` P_holy_ray petals ×6 rising per pulse | CORRECT-TO(single burst) | **CORRECT-TO(one dome bloom: 1-frame onset → 0.15 s peak → 0.40 s out)** — MEASURED |
| `ring_orbit_period` 2.6 s | — | **N/A — there is no ring and nothing orbits** |

---

### 12.6 Class-E files (Desktop only — nothing here is in any repo)

Root: `/Users/admin/Desktop/class-E/2026-09-16-e3-deployment/`

| Skill folder | Clips (first pass, unchanged) | Frames folder (this pass) | Keepers | Folder total |
|---|---|---|---|---|
| `frozen_orb/` | `alt_RPJK4SSFZ0c_full.mp4` (16 MB) · `clip_b5a-iIras34_3025s.mp4` (20 MB) | `frames_q1/` **3.5 MB** | 10 | **38 MB** |
| `lightning_blast/` | `clip_AMXRR3QVpFY_0029.mp4` (34 MB) · `alt_vQGkaa0Uax0_intro.mp4` (42 MB) · `alt2_vQGkaa0Uax0_end.mp4` (66 MB) | `frames_q23/` **4.4 MB** | 8 | **140 MB** |
| `blackwater_cocktail/` | `clip_ThO5dWZzyzY_0317.mp4` (40 MB) · `alt_jRLXuRw9VIA_skilldisplay.mp4` (92 MB) | `frames_q4/` **6.8 MB** | 11 | **133 MB** |
| `poisonous_concoction/` | `clip_ZRVed04RsJE_0023.mp4` (98 MB) · `alt_eErJwp8iP0w_mapping.mp4` (246 MB) · `alt2_23danGZ17b0_mapping.mp4` (296 MB) | `frames_q5/` **6.4 MB** | 12 | **617 MB** |
| `zeus_chain/` | `clip_1V9Qkmoaxng_0059.mp4` (31 MB) · `alt_XPs-jypdwx8.mp4` (112 MB) · `alt_EbMkJBxIVaI_0204.mp4` (45 MB) · `alt_JzOp9I3V9vs.mp4` (15 MB) | `frames_q6/` **8.6 MB** | 10 | **201 MB** |
| `healing_hands/` | `clip_n-IYQnoqpV8_full.mp4` (14 MB) · `alt_5jfYuuosJM0_full.mp4` (54 MB) | `frames_q7/` **3.0 MB** | 10 | **68 MB** |

**Frames added this pass: ~33 MB** (budget 2 GB). **Everything else on disk predates this pass.** Every `frames_*` working set (full-rate sequences, contact sheets used only for locating casts, superseded crops) was deleted immediately after its measurement; only annotated/keeper frames remain, ≤ 12 per question.

**`du -sh ~/Desktop/class-E` → `1.2G`** · `df -h /` at close: **47 GB free** (floor 20 GB, never approached).

### 12.7 What is still not answered

1. **Blackwater glass shards (§ 9-A item 4, first half).** Footage has now been tried and has **failed** — bloom and 1080p compression swallow anything at that scale. The `.pfx` inside the `.arc` is the only remaining route, and it is crawler-shaped, not mine (§ 10.3).
2. **Healing Hands base radius (§ 9-B item 7).** Still needs the in-game tooltip or a browser. The 3.4–3.6 BH here is a **VFX** measurement and § 10.6 warns the two may differ.
3. **Healing Hands post-1.4 appearance (§ 9-B item 8).** Unchanged — **everything in row 7 is pre-1.4**. No post-2026-03-26 Paladin footage was found on this pass either.
4. **PConc lob apex.** The trail angle is measured; the projectile body is 1–2 px and was never tracked to an apex. A build-mode capture with a paused frame would settle it; footage probably cannot.
5. **Zeus ball speed.** One partial track gave ≈5.9 BH/s against the data's 10.83 BH/s. The track ran through a heavily-contaminated frame and is **not** offered as a correction — the data figure stands. Flagged only so nobody re-derives it and thinks they have found a discrepancy.
6. **FF-08 (§ 9-C item 9) is untouched by this pass** and remains gandalf's and Matt's register call — though the Blackwater lick measurement now adds one data point *for* irregularity at the **particle** layer (3.3 Hz, low coherence) even while the **damage** layer stays a perfect 1 Hz metronome. **Those are two different clocks and the spec should say which one FF-08 governs.**

---

## 13. Source list (all accessed 2026-09-16)

> **Renumbered 2026-09-16 (second pass)** from § 12 so that the commissioned addendum could take the § 12 heading it was asked for. Content unchanged.

**Shipped game data (VERIFIED):** [fabd/diablo2](https://github.com/fabd/diablo2) @ `code/d2_113_data/{Missiles,Skills,CharStats,Overlay}.txt` (D2 1.13) · Grim Dawn `database.arz`, read on disk via the team's TQIT/LZ4 parser `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`, cross-checked across two editions · [RePoE](https://github.com/lvlvllvlvllvlvl/RePoE) `gems.json` + [Path of Building](https://github.com/PathOfBuildingCommunity/PathOfBuilding) `src/Data/Skills/act_dex.lua` · [xuqifzz/hades-mod-tutorial](https://github.com/xuqifzz/hades-mod-tutorial) (`PlayerProjectiles.sjson`, `PlayerWeapons.sjson`, `TraitData.lua`, `Fx.sjson`, v1.0)

**Developer-authored (VERIFIED):** EHG Help Centre via Zendesk API — [Paladin Skills](https://support.lastepoch.com/hc/en-us/articles/46363175035035-Paladin-Skills) · [Paladin Skill Tree](https://support.lastepoch.com/hc/en-us/articles/46362493169691-Paladin-Skill-Tree) · [Mage Skills](https://support.lastepoch.com/hc/en-us/articles/46363062648987-Mage-Skills) · [Mage Skill Tree](https://support.lastepoch.com/hc/en-us/articles/46362122141467-Mage-Skill-Tree) · [Common Terminology](https://support.lastepoch.com/hc/en-us/articles/46361668314523) · [Shattered Omens 1.4 patch notes](https://forum.lastepoch.com/t/last-epoch-shattered-omens-patch-notes/80571) · [Healing Hands tree dev post](https://forum.lastepoch.com/t/healing-hands-skill-tree-coming-to-last-epoch-february-21st/62387) · [Alpha 0.5.4 notes](https://forum.lastepoch.com/t/alpha-0-5-4-patch-notes/10762) · GGG [3.16.0 Scourge patch notes](https://www.pathofexile.com/forum/view-thread/3186390) · [pathofexile.com/scourge](https://www.pathofexile.com/scourge) · [Demonic Poisonous Concoction Effect](https://www.pathofexile.com/forum/view-thread/3285407)

**Secondary:** [diablo2.io Frozen Orb](https://diablo2.io/skills/frozen-orb-t4076.html) · [purediablo Frozen Orb](https://purediablo.com/d2wiki/Frozen_Orb) · [poedb Poisonous Concoction](https://poedb.tw/us/Poisonous_Concoction) · hades.fandom.com (via `action=parse&prop=wikitext`) · lastepoch.fandom.com (via `api.php`; **flagged stale**) · grimdawn.fandom.com (**flagged stale**) · poewiki.net (search-index snippets only; direct fetch blocked)

**Tertiary:** [forum.lastepoch.com Healing Hands area size](https://forum.lastepoch.com/t/healing-hands-area-size/66808) · [forum.lastepoch.com LB chain questions](https://forum.lastepoch.com/t/some-questions-about-lightning-blast-mage-skill-chain-convergence-and-spark-charge-chance/61628) · maxroll / Icy Veins / lastepochtools build guides

**Internal:** `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md` · `…/2026-09-13-arpg-run-speeds/findings.md` · `…/2026-09-13-hades-run-speed/findings.md` · `astra_test_01/burst/runs/C-5/specs/*.json` (read, **not edited**) · `canonical/matt_decision_needed/2026-08-25-youtube-frame-extraction-sourcing-class.md`

**Footage — FIRST PASS (candidates only — none watched, nothing downloaded):** all YouTube IDs cited inline in §§ 1a, 3–8.

**Footage — SECOND PASS (downloaded and measured under Matt's option (b), class E):** `b5a-iIras34` · `RPJK4SSFZ0c` · `ThO5dWZzyzY` · `jRLXuRw9VIA` · `ZRVed04RsJE` · `eErJwp8iP0w` · `23danGZ17b0` · `AMXRR3QVpFY` · `vQGkaa0Uax0` · `1V9Qkmoaxng` · `XPs-jypdwx8` · `EbMkJBxIVaI` · `JzOp9I3V9vs` · `n-IYQnoqpV8` · `5jfYuuosJM0`. **All clips and frames live only at `~/Desktop/class-E/2026-09-16-e3-deployment/` with their sidecars; nothing is in any repo and nothing is a burst input.** Measurements are in § 12.

**Web (second pass, to adjudicate Matt's puddle question):** PoE Pathfinder **Master Alchemist** node description (search-index summary; `pathofexile.fandom.com`, `poedb.tw`) — used only to rule OUT flask-created caustic ground. **Graded SECONDARY**; the identification in § 12.3 rests on the frames, not on this.

**Sourcing compliance — FIRST PASS:** option **c′** honoured — **no video downloaded, no frames extracted**. `yt-dlp` is absent from this host. Metadata came from oEmbed and page-embedded JSON; two published thumbnails were fetched and viewed (the already-authorised class). Read-only throughout; nothing written outside this directory.

**Sourcing compliance — SECOND PASS (2026-09-16):** Matt's option **(b)** honoured — clips and JPEG frames on the Desktop under `class-E/` only, **never copied into a repo, never a burst input**. Read-only throughout; nothing written outside this directory. Disk rules honoured in full: `df -h /` before every extraction (floor 20 GB, never below 46 GB), **no new downloads at all**, JPEG-only extraction in windows around measured casts, each working set deleted immediately after measurement, ≤ 12 keeper frames per question. **Frames added: ~33 MB of a 2 GB budget. `du -sh ~/Desktop/class-E` = 1.2G.**
