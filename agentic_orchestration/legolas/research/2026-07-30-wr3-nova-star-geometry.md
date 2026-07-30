# Research — WR3 nova geometry: is Primordian's ice nova a ring or a star? — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR, WR3-KITE-COMMIT run)
**Access mode:** read-only throughout. No game file modified; the game was never launched. Writes
confined to this note and `legolas/scratch/2026-07-30-wr3-nova/`.

**Grading key:** **M** = MEASURED (read verbatim from a pinned binary) · **C** = COMPUTED (from M
inputs under a named operator) · **U** = UNRESOLVED.

**Parent artifact:** `legolas/research/2026-07-30-wr3-stage2-referent-extraction.md` (this note is a
targeted deepening of its §2.3). **Companion:** `legolas/research/2026-07-30-gd-l13-reference-envelope.md`.

---

## VERDICT

**Matt's observation is CONFIRMED, with one bounded correction and one caveat that decides the
stage-2 build.**

The nova is **16 discrete projectiles launched over a 360° arc — 22.5° apart** (M). It is not a
solid expanding ring. It is a 16-prong star, and the prongs are *narrow*: each is a
**0.10-unit-radius sphere** (M), so against a 0.32-unit player the threat corridor is only 0.84
units wide while the prongs are 22.5° apart.

**The correction:** the gaps are not open everywhere. They **close inside r ≈ 2.15 u** (C) — at
melee-hug range the sixteen corridors merge and the star behaves exactly like the solid ring we
currently model. The star grammar is a *mid-and-outer-range* grammar.

**The caveat that matters more than the geometry:** the prongs travel at **14.0 u/s** (M) against a
player at ~7.97 u/s. **Radial outrun is arithmetically impossible from anywhere inside r ≈ 8 u** (C).
Our sim's current escape verb — "outrun it" — is not the referent's escape verb at the ranges this
skill is actually cast at. The referent's only escape is **angular**, and it is *cheap*: 0.07–0.25 s
of lateral movement inside a 0.80 s telegraph (C).

---

## 1. Provenance and the extraction chain

**Pin correction (worth recording):** the commission names
`~/Games/reincarnated-engine/vendor/grim-dawn/`. **That path does not exist.** The two real pins are:

| pin | holds | used for |
|---|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` | `database/database.arz` + `gdx1/2/3` DBs | every field below |
| `/Users/admin/Games/vendor/grim-dawn/` | legacy install; `database/templates.arc`, `resources/Creatures.arc` | template semantics, `.anm` |

`database.arz` SHA-256 **`8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f`** —
byte-identical to the pin used by the parent artifact and every prior GD note. Same game build.
GDX1/GDX2/GDX3 databases are all present and were all swept; **no expansion overrides any record in
this chain.** Nothing here was blocked on the pending GDX3 asset pull.

**The chain, link by link (all M):**

```
records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr     ← "Primorian the Forgotten One"
  └ specialAttack2SkillName / skillName7
    = records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr
        Class = Skill_AttackProjectileRing
        templateName = database/templates/skill_attackprojectilering.tpl
      └ skillProjectileName
        = records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr
            Class = ProjectileFireballLike
            templateName = database/templates/projectilefireballlike.tpl
              └ include templatebase/projectilebase.tpl → include database/templates/actor.tpl
```

Tools (read-only, in `legolas/scratch/2026-07-30-wr3-nova/`): `n1_nz.py` (non-zero field dump),
`n2_raw.py` (named-field dump incl. zeros), `n3_ringcensus.py` (299-record corpus census),
`n5_geom.py` (the arithmetic). Reader: `research/scripts/gd_arz_adapter_2026_07_24.py`;
template reader `s5_tpl.py` over `gd_arc_reader_2026_07_26.py`.

---

## 2. Q1 — Projectile count

| field | value | grade |
|---|---|---|
| `projectileLaunchNumber` | **16** | **M** |
| template declaration | `skill_attackprojectilering.tpl`, `type=int`, `default='1'`, description empty | M |
| scalar or per-rank? | **scalar** — a single int, not a 60-element rank array | M |

Sixteen prongs per cast, at every rank. (Contrast: 24 records in the corpus *do* rank-scale this
field as an array — e.g. `rok_voideruption.dbr` goes 12→15. Primordian's does not.)

**No `numberOfProjectiles` or `projectilePiercing` field exists on this record.** The corpus's
piercing field is `projectilePiercingChance` (declared in `templatebase/skill_projectilebase.tpl`),
and it is **absent from `primordian_frigidring.dbr` entirely** → default 0 (M-negative). For
calibration: **119 of the 299 `Skill_AttackProjectileRing` records in the corpus set it to 100.0**.
Crate uses piercing deliberately, and deliberately did *not* use it here.

**⇒ Each prong stops on the first target it touches. A prong cannot hit twice.**

---

## 3. Q2 — Spread geometry

| field | value | grade |
|---|---|---|
| `projectileLaunchRotation` | **360.0** | **M** |
| `useTargetDir` | **absent → default 0** (template desc: *"Shoot towards target instead of in front of caster"*) | M-negative |
| `useHandLaunch` | **absent → default 0** (*"Shoots from hand callback point instead of center of caster"*) | M-negative |
| `launchAttachPointName` | absent | M-negative |

### 3.1 What `projectileLaunchRotation` means — semantics established by corpus census, not assumption

The template carries **no description** for this field, so its meaning was *measured* rather than
assumed. `n3_ringcensus.py` swept all **299** `Skill_AttackProjectileRing` records across all four
databases:

| `projectileLaunchRotation` | count | examples |
|---|---|---|
| 360.0 | 275 | the overwhelming default |
| 350.0 | 17 | `beetle_poisonfumeshake` N=8, `wighthags_fireboltnova` N=8–10 |
| **270.0** | 1 | `witch_arcanemissilenova` **N=18** |
| **240.0** | 2 | `waspboss_lightningbarrage` / `jaron_lightningbarrage` **N=12** |
| **210.0** | 1 | `banezal_chaosburst` N=8 |
| **180.0** | 2 | `uroboruukguardian_chaosboltnova` N=18, `obsidiandefiler_chaosoverload` N=8 |
| **90.0** | 1 | `baldim_chaoswave` N=8 |
| **35.0** | 1 | `bloodclaw_bloodyhook` N=6 |

**Reading (C, decisive):** the field is a **total spread arc in degrees**, independent of the
projectile count. `baldim_chaoswave` fires 8 projectiles into 90° (a tight 12.86° fan);
`bloodclaw_bloodyhook` fires 6 into 35° (a 7° cone). Both are named "wave"/"hook", not "nova". The
field cannot be a per-projectile rotation or an animation angle — those readings do not survive the
90°/35° cases. **360.0 therefore means: a complete circle, closed.**

### 3.2 The resulting geometry — **C from M inputs**

| quantity | value | operator |
|---|---|---|
| angular spacing between adjacent prongs | **22.500°** | `360.0 / 16` |
| half-gap (on-prong → mid-gap) | **11.250°** | `spacing / 2` |
| spacing regular or randomised? | **regular** — no `randAngle`/`randOffset`/spread-variance field exists on this record or its template chain | M-negative |
| ring phase relative to the player | **anchored to caster facing** (`useTargetDir = 0`) | M |
| launch origin | **caster centre** (`useHandLaunch = 0`), boss `actorRadius = 0.45` | M |

**U-1 (named, unresolved, and it is the one gap that matters):** whether prong 0 sits at 0° (dead
ahead, i.e. straight at the player the boss is facing) or offset by half a step (11.25°, i.e. the
player starts in a gap) is **not encoded in the DBR**. It is an engine convention. The two cases
give opposite starting conditions for a stationary player. *Matt's recording is the better evidence
here than the database is* — he reports having to move to survive, which is consistent with prong-0
at 0° and the boss facing him at release. **Recommend modelling prong-0-on-target** (the
player-hostile case) and carrying U-1.

---

## 4. Q3 — Projectile collision size, and the field-adjudication that decides the verdict

Two different radii live in this chain, and **which one is the hit test determines whether Matt's
observation is possible at all.** Reported raw first, interpreted second, per the commission.

### 4.1 Raw fields

| record | field | value | declared in | template description |
|---|---|---|---|---|
| projectile | `actorRadius` | **0.10** | `actor.tpl` | *(empty)* |
| projectile | `collisionShape` | **`Sphere`** | *(engine field, not in `actor.tpl`)* | — |
| projectile | `notificationRadius` | **1.0** (template default 5.0) | `projectilebase.tpl` | *(empty)* |
| projectile | `collidesWithProjectiles` | **False** (template default 1) | `projectilebase.tpl` | *(empty)* |
| projectile | `minimumDistance` | absent → 0 | `projectilefireballlike.tpl` | *"Minimum travel distance before impact registers with a target"* |
| projectile | `explodeOnMiss` | absent → 0 | `projectilefireballlike.tpl` | *(empty)* |
| **skill** | `projectileExplosionRadius` | **1.5** | `skill_projectilebase.tpl` | *(empty)* |
| player | `actorRadius` | **0.32** (`records/creatures/pc/malepc01.dbr`, identical in all four DBs) | `actor.tpl` | — |
| boss | `actorRadius` | **0.45** | `actor.tpl` | — |

### 4.2 Interpretation — which radius is the hit test?

**Reading A — COLLISION (adopted, C, high confidence): the hit test is the projectile's own
`actorRadius = 0.10` sphere; `projectileExplosionRadius = 1.5` is the *splash applied at the point
of detonation*, after a collision has already occurred.** Four independent supports:

1. **103 of the 299** ring skills have **no `projectileExplosionRadius` at all** (M). If that field
   were the hit radius, a third of the corpus's nova projectiles could never hit anything. It is
   optional; the collision volume is not.
2. The projectile record carries its own `collisionShape = 'Sphere'` alongside `actorRadius` — the
   `actor.tpl` collision pair. That is a hit test, and it is on the projectile, not the skill.
3. `explodeOnMiss` exists as a **separate boolean** (`projectilefireballlike.tpl`) — the engine
   distinguishes "hit" from "explode." Two events, two parameters.
4. `projectilePiercingChance` (100.0 on 119 corpus records) is only coherent if collision is a
   per-target contact event with a small volume.

**Reading B — SPLASH (rejected, carried as the named alternative): the effective threat radius is
1.5.** Its only support is the size of the number. **It is also the reading under which Matt's
observation is impossible** — see §7.2. Recorded so the adjudication is auditable, not averaged in.

**U-2 (minor):** `notificationRadius = 1.0` is an explicit override of the template's 5.0 default,
with an empty description, and I could not establish its function. It does not sit in the collision
chain (`actor.tpl`) and is more plausibly an FX/audio or AI-awareness cue. **Flagged, not used.**

### 4.3 Effective threat corridor — **C**

| reading | half-width | corridor width |
|---|---|---|
| **A — collision (adopted)** | `0.10 + 0.32` = **0.42 u** | **0.84 u** |
| B — splash (alternative) | `1.50 + 0.32` = **1.82 u** | 3.64 u |

---

## 5. Q4 — Speed, range, lifetime

| field | value | grade | source |
|---|---|---|---|
| `projectileVelocity` | **14.0 u/s** | **M** | `icebolt_nova_fxprojectile.dbr` |
| `projectileDistance` | **12.0 u** | **M** | idem (`projectilebase.tpl`) |
| `projectileHitTTLMin/Max`, `projectileMissTTLMin/Max` | **0.0 / 0.0 / 0.0 / 0.0** | M | no lifetime override — range governs |
| **time to maximum range** | **0.857 s** | **C** | `12.0 / 14.0` |
| behaviour at max range | **despawns, no detonation** (`explodeOnMiss = 0`) | M-negative | |
| difficulty-pak modifier to projectile speed | **none** — the Normal/1p slice touches attack speed (−10 %), run speed (−18 %), cast speed (−8 %) and nothing projectile-side | **M-negative** | `balancingadjustment_mp+difficulty_enemies01.dbr` |

**Reference frame:** the boss casts at `specialAttack2Range = 'MediumRange'`. `gameengine.dbr`
defines `shortRange 4.75`, `moderateRange 9.0`, `longRange 15.0`, `maximumRange 18.0`, `meleeRange
1.25` (all M). **U-3:** the literal string `MediumRange` has no exact counterpart in that table; it
most plausibly maps to `moderateRange = 9.0`. Reported as interpretation. Either way the cast
trigger sits **inside** the 12.0 u projectile range — the star always reaches the player it is aimed
at, unless the player leaves.

---

## 6. Q5 — Is the payload per-projectile? (the "2× quantum" question)

**Yes — each prong carries the full damage block.** `projectileUsesAllDamage = **True**` (M;
`skill_attackprojectilering.tpl`, `type=bool`, `default='0'`, description empty).

**Interpretation, reported separately from the field:** the natural reading is *each launched
projectile applies the entire damage payload, rather than the payload being divided across the 16*.
Corroboration from the corpus census: only **44 of 299** ring skills set it True (M). It is a
deliberate, sparingly-used flag, not boilerplate — which is what you would expect of a
damage-multiplying switch.

### 6.1 And Crate priced the overlap explicitly

`primordian_frigidring` carries a **distance-banded damage scale** (all M; template descriptions
*"Greater than or equal to" / "Less than" / "Percent scale"*):

| band | range (u) | scale |
|---|---|---|
| `projectileDamageRange1*` | [0.0, **2.5**) | **50 %** |
| `projectileDamageRange2*` | [2.5, **9.0**) | **100 %** |
| `projectileDamageRange3*` | [9.0, **20.0**) | **140 %** |

**This is a corpus-wide pattern, not a one-off:** 214 of 299 ring skills band their damage this way,
and the shape is always the same — close-range *penalty*, long-range *bonus*
(`skeleton_fireballnova` 40/100/150, `aldritch_poisonnova` 50/100/120,
`mogdrogen_lightningorbnova` 70/100/130, `igrixx_frigidring` 50/100/150). **M.**

**Reading (C, and it is the design tell):** the close-range penalty exists *because* the prongs
converge near the origin and multiple can land. Crate is normalising the overlap:

| player radius | prongs that can land | scale each | net |
|---|---|---|---|
| r ≲ 2.15 (melee hug) | **2** | 50 % | **≈ 1.0×** |
| 2.5 ≤ r < 9.0 | 1 | 100 % | 1.0× |
| 9.0 ≤ r ≤ 12.0 | 1 | 140 % | **1.4×** |

**⇒ The "2× quantum" is real but it is *already priced down to 1×* by the 50 % close band.** The
genuinely dangerous band is the *far* one, where a single clean prong hits for 140 %. Our model
should not carry a 2× close-range spike; the referent deliberately does not have one.

### 6.2 Rank and payload

Boss `charLevel = 'charLevel*1+3'` → at Matt's L13, boss level **16**. `skillLevel7 = 'charLevel/4+1'`
→ frigidring at **rank 5** (C from M formulae). Rank-5 payload **per prong**, before the distance
band (all M, index 4 of the 60-element arrays):

| component | rank 5 |
|---|---|
| `offensivePhysicalMin` | 148.0 |
| `offensiveColdMin` | 247.0 |
| `offensiveSlowColdMin` | 77.0 over `offensiveSlowColdDurationMin` **2.0 s** (cold DoT) |
| `offensiveFreezeMin/Max` | **1.3 – 1.8 s freeze** |
| `skillManaCost` | 38.0 |

---

## 7. Q6 — Secondary behaviour

| behaviour | present? | grade |
|---|---|---|
| fragments / sub-munitions | **NO** — `projectileFragmentsName`, `…LaunchNumberMin/Max`, `projectileFragmentRadius` all **absent from the record** (only 2 of 299 corpus ring skills use them) | **M-negative** |
| ground effect / ice patches | **NO** — no `fxPakName`, no `inflightGroundFxPakName`, no drop/ground field anywhere on the record | **M-negative** |
| chained secondary skill / pet skill | **NO** — no secondary-skill reference | **M-negative** |
| splash on detonation | **YES** — `projectileExplosionRadius = 1.5`, but only at an actual impact point (`explodeOnMiss = 0`). **In a solo fight with no second actor this is a no-op:** the only body it can centre on is the player it just hit. | M + C |
| **freeze** | **YES** — 1.3–1.8 s hard freeze at rank 5 | M |
| **slow (cold DoT)** | **YES** — 77 cold damage over 2.0 s | M |
| knockback | ragdoll flags only (`ragDollDirection 'Push'`, `ragDollPush 'None'`) — cosmetic, no displacement value | M |
| camera shake | `cameraShakeAmplitude 0.12` | M |

**The freeze is the sting, not the damage.** A prong that lands roots the player for **1.3–1.8 s** —
longer than the boss's entire 1.369 s melee lock (parent artifact §2.2). Eating one prong hands the
boss a free melee swing. That is the actual cost of failing the angular dodge, and our sim does not
model it.

---

## 8. The arithmetic — gap traversability as a function of radius

Operator (`n5_geom.py`): prongs radiate from the caster centre; a player disc of radius `r_p` at
radius `r` and angular offset `Δθ` from a prong's ray is hit iff `r·sin(Δθ) ≤ r_proj + r_p`.
Chord separation between adjacent prong rays at radius `r` is `2r·sin(11.25°) = 0.39018·r`.

### 8.1 Reading A — COLLISION (adopted). Threat half-width **0.42 u**.

**Gaps close below `r = 0.42 / sin(11.25°) = 2.153 u`.**

| r (u) | chord sep | **clear gap** | safe angular half-window | **safe arc length** |
|---|---|---|---|---|
| 1.0 | 0.390 | −0.450 | — | **no safe angle** |
| 2.0 | 0.780 | −0.060 | — | **no safe angle** |
| 2.5 | 0.975 | 0.135 | 1.58° | 0.069 |
| 3.0 | 1.171 | 0.331 | 3.20° | 0.168 |
| 4.0 | 1.561 | 0.721 | 5.22° | 0.365 |
| 5.0 | 1.951 | 1.111 | 6.43° | 0.561 |
| 6.0 | 2.341 | 1.501 | 7.24° | 0.758 |
| 8.0 | 3.121 | 2.281 | 8.24° | 1.151 |
| **10.0** | **3.902** | **3.062** | **8.84°** | **1.543** |
| 12.0 | 4.682 | 3.842 | 9.24° | 1.936 |

**The commission's gap-at-10 m figure:** at r = 10 u, adjacent prongs are **3.902 u apart**; each
consumes 0.84 u of corridor; **3.06 u of clear gap remains — 4.8× the player's own 0.64 u
diameter.** The player has a **±8.84°** safe window, i.e. **1.54 u of arc either side of dead
centre**. That is not a threading manoeuvre. That is a walk.

### 8.2 Reading B — SPLASH (rejected). Threat half-width **1.82 u**.

Gaps close below `r = 1.82 / sin(11.25°) = **9.329 u**`. Safe gap at r = 10 is only **0.262 u** —
smaller than the player's 0.64 u diameter, so **still unsurvivable**; the first genuinely traversable
radius is ≈ 10.6 u, and the projectiles stop at 12.0 u.

**Reading B is therefore self-refuting against the recording:** it predicts that the nova is
effectively a solid ring at every distance the boss actually casts it from (`MediumRange` ≈ 9.0 u),
and that no gap-walking is possible. Matt walked through a gap. **Reading A is the one consistent
with both the field semantics (§4.2) and the observation.**

### 8.3 Double-hit band — **C, Reading A**

| case | condition | both prongs land while |
|---|---|---|
| worst (player mid-gap, Δθ = 11.25° to each) | `r·sin(11.25°) ≤ 0.42` | **r ≤ 2.153 u** |
| best (player on a prong, neighbours at 22.5°) | `r·sin(22.5°) ≤ 0.42` | r ≤ 1.098 u |
| floor (bodies cannot interpenetrate) | boss 0.45 + player 0.32 | r ≥ 0.77 u |

**⇒ Double-hit band ≈ [0.77, 2.15] u — melee-hug range only, and precisely the band Crate discounts
to 50 % (§6.1).** Three prongs are never possible: that would need `r·sin(22.5°) ≤ 0.42` *and* a
third at 33.75°, i.e. r ≤ 0.76 u — inside the collision floor.

### 8.4 Radial outrun — **C. This is the finding that indicts the current model.**

Prong speed 14.0 u/s. Player speed **7.97 u/s** (Model A, parent artifact §3.3; Model B agrees the
player is slower than the prongs by a wider margin). To survive radially the player must reach
r = 12.0 u before the prong does, in 0.857 s:

| start radius | must cover | required speed | available | verdict |
|---|---|---|---|---|
| r = 2 | 10.0 u | 11.67 u/s | 7.97 | **IMPOSSIBLE** |
| r = 5 | 7.0 u | 8.17 u/s | 7.97 | **IMPOSSIBLE** (by 2.5 %) |
| r = 8 | 4.0 u | 4.67 u/s | 7.97 | possible |

**Radial outrun only works from r ≳ 7.9 u — i.e. from the very outer edge of the cast band.** Our
sim's escape verb is available in a thin sliver of the referent's engagement space and nowhere else.

### 8.5 Angular dodge cost — **C. And this is why it is the *right* verb.**

Lateral travel needed to move from on-prong to a safe angle, at 7.97 u/s, inside the **0.80–0.89 s**
telegraph established in the parent artifact §2.3:

| r (u) | lateral arc to clear the prong | full arc to mid-gap | time at 7.97 u/s | fraction of the 0.80 s telegraph |
|---|---|---|---|---|
| 3 | 0.421 | 0.589 | 0.074 s | 9 % |
| 5 | 0.420 | 0.982 | 0.123 s | 15 % |
| 8 | 0.420 | 1.571 | 0.197 s | 25 % |
| 10 | 0.420 | 1.963 | 0.246 s | 31 % |

**The minimum clearing distance is a constant 0.42 u at every radius** (it is the corridor
half-width; the `r·sin` and the `1/r` cancel). At walk speed that is **0.053 s of lateral movement**
— under 7 % of the telegraph. Matt's Evade (10.0 u in ~0.28 s, parent §1.4) overshoots the
requirement by more than an order of magnitude.

---

## 9. Sanity check — is this the attack whose telegraph was measured, and does Primordian have others?

**Yes to the first, and yes to the second: Primordian has three distinct ranged/AoE attacks.** Full
enumeration from `slith_wightmirecave01.dbr` (all M):

| slot | skill | class | shape | cadence | animation → measured release |
|---|---|---|---|---|---|
| `specialAttackSkillName` | `primordian_wave.dbr` | `Skill_AttackWave` | **directional cone** — `waveStartWidth 3.0` → `waveEndWidth 6.0` over `waveDistance 16.0`, `waveDepth 1.0`, `waveTime 1.4 s` | 100 % chance, 5.0 s delay, 5.0 s timeout, **MediumRange** | `TailLashSunder` → `slith01_attack_special_sunder.anm`, 79 keys, contact f23 @0.90× ⇒ **0.852 s**, total 2.889 s |
| **`specialAttack2SkillName`** | **`primordian_frigidring.dbr`** | **`Skill_AttackProjectileRing`** | **16-prong 360° star** | 80 % chance, 6.0 s delay, 3.0 s timeout, **MediumRange** | **`Roar` → `slith01_cast_buff_01.anm`, 61 keys, `RightHandHit` f30 @1.25× ⇒ 0.800 s (band 0.80–0.89 s), total 1.600 s** |
| `specialAttack3SkillName` | `chillbane_blizzard.dbr` | `Skill_BuffAttackRadiusDrop` | **aerial bombardment** — `dropHeight 20.0`, `dropRadius 15.0`, `dropVariation 3.0`, 6 projectiles per tick, `skillTargetInterval 2.0 s`, `skillActiveDuration 8.0 s`, `skillTargetRadius 8.0`, `projectileExplosionRadius 1.0`, `skillProjectileTargetGroundOnly True` | 100 % chance, 10.0 s delay, 8.0 s timeout, **LongRange** | — |
| `buffSelfSkillName` | `primordian_icearmor.dbr` | `Skill_BuffSelfDuration` | self-buff, `damageAbsorptionPercent 25.0`, 12.0 s duration, 32.0 s cooldown, `instantCast` | — | `BuffQuick` |
| `skillName10` | `primordian_passive.dbr` | `Skill_Passive` | passive | — | — |

**The 0.80–0.89 s telegraph belongs to `primordian_frigidring` — the star. Confirmed, same record,
same `specialAttack2` slot, same `Roar` animation.** The parent artifact's §2.3 figure is measuring
exactly the skill Matt described.

**Could Matt have seen a different attack?** No — the three are visually unmistakable and only one
is a star:

- `primordian_wave` is a **single expanding cone in one direction** (3→6 u wide over 16 u). Its
  escape is "step out of the cone," not "move between prongs." No prongs exist.
- `chillbane_blizzard` is **ice falling from 20 u up in a 15 u scatter** over 8 s. Its escape is
  "leave the area." No radial structure at all.
- `primordian_frigidring` fires **16 `frostorb01.msh` orbs, each trailing `swordfrost_fxtrail`,
  radially outward at 22.5° spacing**. Sixteen frost-trailed orbs leaving a common centre is,
  visually, precisely *"a multi-pronged star ice-shot."* (M on every asset reference.)

**Matt's description is a match to `primordian_frigidring` and to nothing else in the boss's kit.**

---

## 10. What this changes for the stage-2 build

Reported factually; the ruling is the conductor's.

| row | our sim today | GD referent (M/C) | delta |
|---|---|---|---|
| nova shape | radially uniform expanding threat | **16 discrete prongs, 22.5° apart, 0.84 u corridors** | **shape is wrong** |
| dodge grammar | **radial** ("outrun it") | **angular** ("step between prongs"); radial is impossible below r ≈ 7.9 u | **verb is wrong** |
| escape cost | outrun a whole ring | **0.42 u of lateral movement — 0.053 s, ~7 % of the telegraph** | **cost is wrong by ~an order of magnitude** |
| threat is uniform in θ? | yes | **no — 16 hot lines, gaps everywhere else beyond r = 2.15 u** | new axis |
| threat is uniform in r? | yes | **no — 50 % / 100 % / 140 % distance bands at 2.5 u and 9.0 u** | new axis, and it *inverts* the usual "close is worse" |
| double-hit | modelled as a 2× quantum | **real, but confined to r ∈ [0.77, 2.15] u and priced to net ≈1× by the 50 % close band** | **2× spike should be removed** |
| melee-hug behaviour | — | **gaps close; at r ≲ 2.15 u the star IS our uniform ring** | our current model is correct *only* here |
| on-hit rider | none modelled | **1.3–1.8 s freeze + 77 cold over 2.0 s** at rank 5 | **missing, and it is the real punishment** |
| projectile speed | — | **14.0 u/s vs player 7.97 u/s** | the reason radial fails |
| max range / flight | — | **12.0 u in 0.857 s**, then despawn (no end-of-flight blast) | bounds the whole event |

**The one-line statement of the change:** the referent's nova is not a test of *distance*, it is a
test of *bearing* — and it is a cheap test to pass and an expensive one to fail (a freeze longer than
the boss's whole melee commit). Our sim inverts both halves: it makes the test expensive to pass
(outrun a ring) and cheap to fail (damage only).

---

## 11. Knowledge gaps not resolved

| id | gap | why it resisted | impact |
|---|---|---|---|
| **U-1** | Ring phase: is prong 0 at 0° (on the player) or offset 11.25° (player starts in a gap)? | engine convention; not in the DBR, not in the template | decides whether a stationary player is hit by default. **Recommend the hostile assumption.** Matt's recording is better evidence than the DB here. |
| **U-2** | `notificationRadius = 1.0` (explicit override of the 5.0 default), empty description | not in the `actor.tpl` collision chain; no corpus pattern isolates it | not used in any figure above |
| **U-3** | `specialAttack2Range = 'MediumRange'` has no exact match in `gameengine.dbr` (`shortRange 4.75` / `moderateRange 9.0` / `longRange 15.0`) | string enum → numeric mapping is engine-side | affects the cast-trigger radius; `moderateRange = 9.0` assumed |
| **U-4** | Whether `projectileUsesAllDamage = True` means "full payload per prong" (adopted) or something narrower | template description is empty | if wrong, §6 damage magnitudes shift; **the geometry in §8 is unaffected** |
| **U-5** | Whether the 1.5 splash can carry between two nearby actors | no second actor exists in the solo fixture | irrelevant to Matt's session; would matter in a pet/minion build |
| *(carried)* | Player-side werewolf-form animation set is GDX3-`Creatures.arc`-only; all player timings remain **human form** | parent artifact §5 U-1; asset pull still pending | affects §8.5 dodge times, not the star geometry |

---

## 12. Source list

All read-only, all local pinned binaries, accessed 2026-07-30.

| # | source | note |
|---|---|---|
| 1 | `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` | SHA-256 `8cdeff12…ae3f`; every record in the chain resolves here |
| 2 | `…/gdx1/database/GDX1.arz`, `…/gdx2/database/GDX2.arz`, `…/gdx3/database/GDX3.arz` | swept for overrides — **none found** on this chain |
| 3 | `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` | `skill_attackprojectilering.tpl`, `projectilefireballlike.tpl`, `templatebase/skill_projectilebase.tpl`, `templatebase/projectilebase.tpl`, `actor.tpl` |
| 4 | `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` | boss; full skill enumeration §9 |
| 5 | `records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr` | **the nova**; 304 fields |
| 6 | `records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr` | the prong; 32 fields, all listed |
| 7 | `records/skills/nonplayerskills/bossskills/primordian_wave.dbr` · `…/heroskills/chillbane_blizzard.dbr` · `…/bossskills/primordian_icearmor.dbr` · `…/bossskills/primordian_passive.dbr` | sibling-attack disambiguation |
| 8 | `records/creatures/pc/malepc01.dbr` | player `actorRadius = 0.32` |
| 9 | `records/game/gameengine.dbr` | range-band constants |
| 10 | `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` | Normal/1p difficulty slice — no projectile modifier |
| 11 | corpus census of **299** `Skill_AttackProjectileRing` records across all four DBs | established `projectileLaunchRotation` semantics, piercing/fragment/explosion-radius base rates, damage-band pattern |
| 12 | secondary — Matt's screen recording (verbatim report relayed by gandalf) | the claim under test; **corroborated**, not assumed |
