# Research — Whirlwind revolution rates + sweep-VFX conventions (D2 / D3 / D4 / GD) — 2026-08-12

**Mode:** A (analytical, unmapped-territory probe)
**Commissioner:** gandalf (RUN-CONDUCTOR, SB-1 scene run), on Matt's word
**Scope:** verify-or-correct the 0.30–0.50 s/rev broad band and 0.33–0.40 s/rev endgame band; harvest sweep-VFX conventions
**Depth budget:** quick probe (~40 min). Where sources are thin, they are marked **THIN** rather than padded.
**Governing rule:** GL-17 — reference governs, never copies. Numbers below are *shape study*, not values to import.

---

## Summary

1. **No game in the set publishes a "revolution rate."** Every documented number across all four titles is a **damage-tick / hit-check interval**, not a visual spin period. Any s/rev figure — including Matt's phone result — is a derivation someone made from tick data or from eyeballing footage. This is the single most important framing correction in this note.
2. **Diablo 2 is the one game where the mechanic→visual bridge is defensible**, because D2R's Whirlwind frame formula is *literally derived from the character's standard attack animation length* (`A1_Action_Length`). That gives a hard, source-grounded anchor: **9 frames = 0.36 s for two-handed non-swords** (axes/maces/polearms — the SB-1 weapon class).
3. **Matt's broad band (0.30–0.50 s/rev) is CONFIRMED as the typical/central band, but it is not the full range.** The real span runs ~0.16 s (D2 dual-wield floor) to ~0.56 s (D2 unaided slow 2H).
4. **Matt's endgame band (0.33–0.40 s/rev) is CORRECT — but only for two-handed.** It is wrong for one-handed/dual-wield, which goes materially faster (0.16–0.24 s). The band is **weapon-class-dependent, and every game that models the distinction makes 2H slower.** Since SB-1 renders a 2H hammer, Matt's endgame band happens to be the right one for our case.
5. **Grim Dawn was resolved from primary source**, not from the web: the vendored `.arz` yields `Skill_AttackRadiusSpin` with `timeBetweenAttacks = 200` ms, stable across all four vendored editions. This **contradicts** the widely-repeated community figure of 0.16 s. Engine value governs.
6. **Spark-arc precedent: FOUND, in two games, as an explicit two-layer convention** (continuous weapon-mounted trail + discrete contact burst). Dark/smoky volume contrast: also found. Details in § 6.

---

## 1. Per-game table

Engine-frame conversions at each game's native tick base. **Tick** = documented damage interval. **Rev** = visual revolution period (derived; confidence marked).

| Game | Mechanic | Attack-speed scaling | Documented tick | Derived visual rev period | Confidence |
|---|---|---|---|---|---|
| **Diablo 2 / D2R** | Frame-based hit-checks at 25 fps. `WW_FPA = [256 × A1_Action_Length / [256 × Speed_Multiplier]]` | Weapon speed + IAS → discrete FPA breakpoints. **D2R 2.4.3 folded ALL IAS sources + slow effects into WW rate** (classic D2 counted weapon-borne IAS only) | 14 → 4 FPA = **0.56 → 0.16 s** | **2H non-sword neutral = 0.36 s** (A1 = 9 frames); geared 2H ≈ 0.24–0.32 s; 1H/2H-sword floor = 0.16 s (A1 = 7 frames) | **HIGH** — tick *is* the animation cycle |
| **Diablo 3** | Channeled; discrete damage ticks, each tick a full damage application (proc coefficient 1) | Ticks scale with weapon APS. Dual-wield combines **harmonically**, not by average: `2/(1/a + 1/b)` — e.g. 1.0 + 1.5 APS → 1.2 effective, not 1.25 | ~1.0 s at 1.0 APS reference (30 frames @ 30 fps; 25 frames = 0.833 s at +20% AS) | Visual spin is **decoupled and faster** than the tick. No authoritative rev figure found | **THIN** for visual; MEDIUM for tick |
| **Diablo 4** | Channeled spender | **SOURCES CONFLICT — see § 3.** Maxroll (authoritative): channeled skills get *no* benefit from Attack Speed. Secondary sources: weapon APS does drive tick rate | Weapon base APS: **2H axe/polearm/mace 0.9; 1H axe/mace/sword 1.1; 1H flail 1.2**. Low-quality sources claim "6–10 ticks/sec" | Not derivable from available sources | **THIN** — thinnest of the four, as anticipated |
| **Grim Dawn (EoR)** | `Skill_AttackRadiusSpin` — radial damage pulse, `skillTargetRadius = 3.0` | Linear with attack speed, **no breakpoints**; GD attack-speed cap 200% | **`timeBetweenAttacks = 200` ms** (primary source, `.arz`) → 0.20 s base, **0.10 s floor at the 200% cap** | Tick floor of 0.10 s is far faster than the observed spin ⇒ **multiple ticks per revolution**; ~2–4 ticks/rev puts rev ≈ **0.30–0.40 s** | **HIGH** for tick (primary source); MEDIUM-INFERRED for rev |

---

## 2. Diablo 2 — the load-bearing find

The D2R breakpoint work gives the formula outright:

```
Whirlwind_FPA = [256 * A1_Action_Length / [256 * Speed_Multiplier]]
```

where `A1_Action_Length` is *"the number of frames for the standard attack for the character class and weapon"* — **7** for barbarian 1H and 2H swords, **9** for all other 2H weapons (axes, maces, polearms).

**Why this matters more than any other number in this note:** the Whirlwind hit interval is not an arbitrary skill constant. It is the character's ordinary swing animation, re-clocked. One hit-check ≈ one swing ≈ **one weapon sweep**. That is the only place in the four-game set where a published mechanic legitimately licenses a *visual* revolution period.

Seconds at 25 fps:

| FPA | 4 | 6 | 7 | 8 | **9** | 10 | 12 | 14 |
|---|---|---|---|---|---|---|---|---|
| seconds | 0.16 | 0.24 | 0.28 | 0.32 | **0.36** | 0.40 | 0.48 | 0.56 |

- **2H non-sword (our case):** unaided slow 2H sits at 14 FPA = 0.56 s. Heavy IAS drives it down toward 6 FPA = 0.24 s. **4 FPA is explicitly marked N/A for 2H non-swords** — the 0.16 s floor is unreachable with a maul. A realistically geared 2H WW barb lands ~7–9 FPA = **0.28–0.36 s**.
- **1H / 2H swords:** reach the 4 FPA = 0.16 s floor at 41 effective IAS.
- Post-2.4.3 there is 1 free hit check at frame 4, after which hit-checks occur strictly at the frame interval.

**Version conflict worth carrying:** classic D2 counted only weapon-borne IAS for Whirlwind; D2R 2.4.3 incorporates all IAS sources and slow effects. Any pre-2022 community number describes different mechanics. Do not blend the two.

---

## 3. Diablo 4 — thin, and the sources disagree

Reporting the conflict rather than averaging it, per source-adjudication discipline:

- **Maxroll's attack-speed mechanics resource** states plainly: *"Certain skills, such as channeled abilities, do not benefit from Attack Speed in any way."* Whirlwind is a channeled ability. Maxroll also gives the formula `ApS = Weapon APS × (100% + AS%)` and two separate 100% caps (gear/paragon/tempering; cast speed) for 200% total.
- **Secondary sources** (Power Up Gaming, Sportskeeda, boosting blogs) assert the opposite in part: gear AS affixes don't change WW tick rate but *weapon APS does*.

These are reconcilable only if "attack speed" means different things in each — plausible, but **not established by any source I found**. No authoritative D4 tick interval or revolution period exists in the accessible record. **D4 contributes its weapon base-APS table and nothing more.** Marked THIN; I did not pad it.

The one solid D4 number for our purposes: **2H maces/axes/polearms are 0.9 base APS vs 1.1–1.2 for one-handers** — i.e. D4 independently reproduces the 2H-is-slower rule.

---

## 4. Grim Dawn — resolved from primary source

Web sources were consulted and then **superseded by direct extraction** from the vendored `.arz` archives using the LZ4/TQIT adapter established 2026-07-23.

`records/skills/playerclass09/eyeofreckoning1.dbr` — record type **`Skill_AttackRadiusSpin`**, template `database/templates/skill_attackradiusspin.tpl`:

| Field | Value | Reading |
|---|---|---|
| `timeBetweenAttacks` | **200** | ms between damage pulses at base attack speed → 5 pulses/sec |
| `duration` | 0.25 | s; with `useResetsDuration: True`, each channel pulse re-extends the spin |
| `skillTargetRadius` | 3.0 | radial AoE, not a swept arc — the damage shape is a disc |
| `rotationSpeedMultiplier` | 0.35 | character **turn rate** is throttled to 35% while channeling (a steering penalty; *not* the animation spin rate) |
| `canUseWhileMoving` | True | with `delayMovement: True` |
| `skillCastAuraName` | `records/fx/skillclass09/eyeofreckoning_spinfx01.dbr` | the sweep VFX — see § 6 |
| `skillMaxLevel` / `skillUltimateLevel` | 16 / 26 | 26-rank arrays (consistent with the 2026-07-23 finding, not grimtools' 60) |

**Version-delta check (no drift):** `timeBetweenAttacks = 200`, `duration = 0.25`, `rotationSpeedMultiplier = 0.35`, `radius = 3.0` are **byte-identical across all four vendored editions** (`grim-dawn`, edition-I-20260723, edition-II-20260724, edition-III-20260808, spanning 1.2.x → 1.3.x/FoA). The spin timing has not been patched.

**Sibling-skill sweep (answers "anything else whirlwind-style in GD"):** exhaustive scan of every `.arz` in the latest edition for `Skill_AttackRadiusSpin` returns exactly three live records plus one dev artifact —
- `records/skills/playerclass09/eyeofreckoning1.dbr` (tBA 200)
- `records/skills/itemskillsgdx2/relics/hungeringreach.dbr` (tBA 200) — the Hungering Reach relic grants the same spin
- `records/skills/base_template skills/skill_attackradiusspin.dbr` (tBA 200, dur 0.20) — the authoring default
- `records/sandbox/jakub/test_skill_attackradiusspin.dbr` (tBA 500) — a Crate developer sandbox record, shipped in `database.arz`

So **EoR is the only player-facing spin channel in Grim Dawn**; classic (pre-FG) GD has no whirlwind analogue. The 2H-hammer Warlord lineage Matt's reference character played is EoR or nothing.

**CONTRADICTION FLAGGED:** the widely-repeated community figure — *"At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy every 0.16s"* — **disagrees with the shipped engine value of 200 ms.** 0.16 s corresponds to ~125% attack speed, not 100%. Either the community figure was measured on a character whose sheet already read ~125%, or it is simply wrong. **The `.arz` value governs.** This is the same class of error as the grimtools 60-rank/`.arz` 26-rank contradiction: a repeated secondary number that primary extraction does not support.

---

## 5. VERDICT on the two bands

### Broad band 0.30–0.50 s/rev — **CONFIRMED as the central band; NOT the full range**

0.30–0.50 s/rev is a fair description of where a *typical* whirlwind sits across the set. But the honest full envelope is **~0.16 s to ~0.56 s**, both endpoints from D2:
- **fast end 0.16 s** — dual-wield / 1H / 2H-sword at the 4-FPA floor
- **slow end 0.56 s** — an ungeared slow two-hander at 14 FPA

So Matt's band is right about the middle and understates the tails. For a scene-authoring decision, the middle is what matters, so the band is **usable as given**.

### Endgame band 0.33–0.40 s/rev — **CORRECT, and correct specifically for our case (2H)**

This is the finding I'd have been most willing to overturn, and it survived. It is well-supported *for two-handed weapons* and centred almost exactly on D2's hard anchor:

- **D2 2H non-sword `A1_Action_Length` = 9 frames = 0.360 s.** Dead centre of Matt's band, and it is a *shipped animation constant*, not a derivation.
- **GD EoR** at 2–4 ticks/revolution off a 0.10–0.20 s tick lands ~0.30–0.40 s.
- **D4** reproduces the 2H-is-slower rule (0.9 vs 1.1–1.2 base APS) even though it won't yield a rev period.

**The correction Matt should carry:** the endgame band is **not uniform across weapon class**. 0.33–0.40 s/rev is the **two-handed** endgame band. The **one-handed / dual-wield** endgame band is roughly **0.16–0.24 s/rev** — about twice as fast. Every game in the set that distinguishes the two makes 2H slower. Quoting 0.33–0.40 as "the endgame band" without the 2H qualifier would be wrong; quoting it *for SB-1's 2H hammer* is right.

### On the shipped 0.60 s/rev placeholder

0.60 s/rev is **slower than every endgame reference and slower than all but the ungeared-slow-2H corner of D2** (0.56 s at 14 FPA). It is ~1.7× the 2H anchor of 0.36 s. It is not absurd — it reads as a heavy, unhasted maul — but it does not read as *endgame*. If SB-1 wants the sim trace to read as a geared 2H channel, the reference-governed target is **~0.35–0.40 s/rev**, anchored on D2's 9-frame 2H swing.

**Standing caveat (GL-17):** this is shape study. The band above describes what the genre does, not what Reincarnated must do. NO-WIRE-BASIS remains factually true — none of these numbers are wired to our sim; adopting one is still a presentation choice, merely a now-informed one.

---

## 6. Sweep-VFX conventions

**Diablo 2 / D2R.** Classic D2 is 2D sprite-based: the whirl is a pre-rendered blurred spinning barbarian sprite, drawn from the fixed isometric direction set, with no runtime trail geometry, no ground decal, and no per-contact particle — the "sweep" is entirely baked into the sprite sheet's motion blur. There is no separable trail layer to study because the era's tech had none. D2R re-renders the same animation in 3D with modern lighting and adds contemporary weapon-trail treatment, but I found **no developer art-direction source** describing the remaster's WW VFX specifically, so I am not characterising it further. **THIN on art sources; the mechanical record for D2 is excellent, the visual record is not.**

**Diablo 3.** The best-documented of the four, and the most directly useful to SB-1. Per the BlizzCon 2009 Diablo 3 panel (reported via diablowiki), the team judged the Dune Dervish's whirl to look better than the Barbarian's and reworked the latter with **"more blur, and more Barbarian copies in it"** — i.e. explicit multi-afterimage ghosting of the body, not just the weapon. The shipped result has **"the weapon visible tracking around in a circle, leaving a glowing light as it spins"** — a continuous, weapon-mounted luminous trail — and, critically, **"pausing an instant when it makes contact with a hapless enemy."** That is a deliberate impact hitch / hitstop on the sweep. Around the body, **"dust and sand is seen being"** kicked up. The stated design intent is worth quoting whole: *"weight of the weapon + the speed of spinning = very hard hitting impact."* Four separable layers: body afterimages, luminous weapon trail, ground dust volume, per-contact hitch.

**Diablo 4.** The signature element is the **Dust Devil** — the Tornado upgrade spawns literal persistent dust/smoke volumes off the spin, which are simultaneously a VFX motif and a damage entity, and which community guides note cover a **wider area than the base graphic suggests**. That is the clearest **dark/smoky volume** precedent in the set: the spin does not merely raise dust, it sheds discrete smoke bodies that persist and travel. Beyond Dust Devils I found **no developer art-direction source** on D4's whirlwind trail, spark, or ground treatment. **THIN.**

**Grim Dawn.** Resolved from primary source, and the most structurally informative. `eyeofreckoning1.dbr` points `skillCastAuraName` at `records/fx/skillclass09/eyeofreckoning_spinfx01.dbr`, an `EffectEntity` whose **`boneList = ['Bone_R_Weapon', 'Bone_L_Weapon']`** and whose `effectFile` is `fx/particlesystems/skillsclass09/pfx_eyeofreckoning_spinfx_01.pfx`. So GD emits the sweep **from the weapon bones themselves** — a weapon-mounted particle trail, not a body aura, not a ground ring, not a swept mesh. Separately, `eyeofreckoning_impact_fx01.dbr` is a **distinct** `EffectEntity`, *also* bound to `Bone_R_Weapon`/`Bone_L_Weapon`, with `canBeSoft: True`, firing `pfx_eyeofreckoning_impact.pfx` — a discrete contact burst at the weapon, layered over the continuous trail. And GD ships **eight authored variants of the spin trail** — `spinfx01` (base), `acid`, `aether`, `chaos`, `cold`, `fire`, `lightning`, plus `spinredfx01` and `spinfxclassic_01` — establishing the trail as a **recolourable/swappable channel** driven by the build's damage conversion, with a legacy "classic" variant retained.

### Spark-trail-arc precedent — **YES, found, and it is a consistent two-layer convention**

Two independent games implement the same architecture, and it is exactly the thing Matt described:

| Layer | Grim Dawn (primary source) | Diablo 3 (dev panel) |
|---|---|---|
| **Continuous** weapon-mounted trail | `spinfx01` EffectEntity bound to `Bone_R_Weapon`/`Bone_L_Weapon` | "weapon visible tracking around in a circle, leaving a glowing light as it spins" |
| **Discrete** contact burst | *separate* `impact_fx01` EffectEntity, same weapon bones, `canBeSoft: True` | "pausing an instant when it makes contact" (hitch), plus impact treatment |

The convention is: **arc trail is emitted from the weapon bone and runs continuously; the spark/impact event is a separate emitter that fires only on contact.** GD keeps them as two distinct records rather than one combined effect — a deliberate separation. This is direct precedent for spark-trail arcs "as if striking a surface," and it argues for authoring SB-1's trail and spark as **two independently-tunable layers** rather than one baked effect.

### Dark/smoky volume contrast — **YES**

- **D4 Dust Devils** — persistent, travelling smoke bodies shed by the spin. Strongest precedent.
- **D3** — "dust and sand" raised around the barbarian, plus **"more Barbarian copies"**, which functions as a dark-mass afterimage reading against the bright weapon trail. That bright-trail-against-dark-body-mass contrast is precisely the figure/ground effect Matt is after, and D3 arrived at it deliberately.

---

## 7. Oversized-weapon convention — **UNRESOLVED / THIN**

I found **no authoritative published ratio** for 2H weapon length relative to body height in any of the four games — no art-bible excerpt, no developer statement, no measured community study. Searches returned cosplay-prop scaling guides and D&D variant rules, neither of which is evidence about these games.

What I can say without fabricating: the genre convention is visibly *exaggerated but sub-anime* — ARPG mauls read as large without approaching the ~2× body-height proportions of stylised JRPG greatswords, and the exaggeration is carried more by **head mass and silhouette bulk than by haft length**. I am flagging the specific ratio as **not established by this probe**. If the weapon-scale band needs a defensible number, the right next move is direct measurement off screenshots/model files rather than more web search — cheap to do, and it would produce a first-party number instead of a borrowed one. Say the word and I'll run it.

---

## Knowledge gaps not resolved

- **D4 attack-speed applicability to Whirlwind** — Maxroll and secondary sources directly contradict; unresolved. Would need datamining or controlled in-game timing.
- **D3 exact visual revolution period** — the tick rate is documented, the animation loop rate is not. The two are decoupled in D3 and I could not close the gap from public sources.
- **GD's actual spin animation period** — `timeBetweenAttacks` is damage, not animation. The true rev period lives in the character `.anm`/`.mdl` assets inside GD's `.arc` archives, which this probe did not open. **This is closeable**: the `.arc` container is a known format and the `.arz` lane is already established. Estimated 1–2 h to extract and read the Oathkeeper spin animation length, which would convert GD's rev period from MEDIUM-INFERRED to HIGH. Recommend if the number needs to be load-bearing.
- **The `.pfx` particle definitions** (`pfx_eyeofreckoning_spinfx_01.pfx` etc.) also live in `.arc`, not `.arz` — opening them would give exact trail lifetimes, emission rates and colour ramps. Same lane, same estimate.
- **Weapon-scale ratio** — see § 7.
- **D2R visual-remaster art sources** — nothing found describing the WW VFX rework specifically.

---

## Source list

**Primary — direct extraction (this probe)**

| Source | Detail | Accessed |
|---|---|---|
| `~/Games/vendor/grim-dawn-edition-III-20260808/gdx2/database/GDX2.arz` | `records/skills/playerclass09/eyeofreckoning1.dbr` (311 fields), `eyeofreckoning_spinfx01.dbr`, `eyeofreckoning_impact_fx01.dbr`, `eyeofreckoning_fire_spinfx01.dbr`, exhaustive `Skill_AttackRadiusSpin` scan | 2026-08-12 |
| `~/Games/vendor/grim-dawn{,-edition-I-20260723,-edition-II-20260724}` | version-delta confirmation of EoR timing fields across editions | 2026-08-12 |
| `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` | LZ4/TQIT `.arz` reader (lane established 2026-07-23) | 2026-08-12 |

**Secondary — developer statements / community mechanics work**

| Source | URL | Accessed |
|---|---|---|
| Blizzard D2R forums — "Update: Whirlwind breakpoints for all single-wielding (1H and 2H) weapons" (WW FPA formula, `A1_Action_Length`, 2.4.3 behaviour) | https://us.forums.blizzard.com/en/d2r/t/update-whirlwind-breakpoints-for-all-single-wielding-1h-and-2h-weapons/136394 | 2026-08-12 |
| Blizzard D2R forums — "I've figured out the whirlwind breakpoints for slow bases" | https://us.forums.blizzard.com/en/d2r/t/ive-figured-out-the-whirlwind-breakpoints-for-slow-bases/136247 | 2026-08-12 |
| Diablo Wiki (diablowiki.net) — Whirlwind, incl. BlizzCon 2009 D3 panel VFX rework reporting | https://www.diablowiki.net/Whirlwind | 2026-08-12 |
| Diablo Wiki (D2) — Whirlwind hit-check frames, breakpoint sets | https://diablo2.diablowiki.net/Whirlwind | 2026-08-12 (403 on direct fetch; content via search index) |
| Project Diablo 2 wiki — Breakpoints | https://wiki.projectdiablo2.com/wiki/Breakpoints | 2026-08-12 (403 on direct fetch) |
| Maxroll D4 — Attack Speed Mechanics (ApS formula, dual 100% caps, weapon base APS table, channeled-skill exclusion) | https://maxroll.gg/d4/resources/attack-speed-mechanics | 2026-08-12 |
| Blizzard D3 forums — "Dual Wielding and Whirlwind channeling ticks" (harmonic dual-wield APS) | https://us.forums.blizzard.com/en/d3/t/dual-wielding-and-whirlwind-channeling-ticks/3525 | 2026-08-12 |
| Diablo Fandom — Whirlwind (Diablo III) | https://diablo.fandom.com/wiki/Whirlwind_(Diablo_III) | 2026-08-12 |
| Diablo Fandom — Whirlwind (Diablo IV) | https://diablo.fandom.com/wiki/Whirlwind_(Diablo_IV) | 2026-08-12 |
| Maxroll D3 — Waste Set WW Rend Barbarian (Rend frame breakpoints under AS) | https://maxroll.gg/d3/guides/waste-set-ww-rend-barbarian-guide | 2026-08-12 |
| Grim Dawn Fandom — Eye of Reckoning (Skill) | https://grimdawn.fandom.com/wiki/Eye_of_Reckoning_(Skill) | 2026-08-12 |
| Crate forums — "RE: Eye of Reckoning Attack Speed" | https://forums.crateentertainment.com/t/re-eye-of-reckoning-attack-speed/50963 | 2026-08-12 |
| Steam — "Q> Does Eye of Reckoning scale with attack speed?" (source of the contested 0.16 s figure) | https://steamcommunity.com/app/219990/discussions/0/1639789306556979468/ | 2026-08-12 |
| Mobalytics D4 — Whirlwind Dust Devils build (Dust Devil area/VFX characterisation) | https://mobalytics.gg/diablo-4/builds/barbarian-dust-devils | 2026-08-12 |

**Tertiary — consulted, low weight, used only to establish that a claim circulates**
Power Up Gaming and Sportskeeda articles on D4 Whirlwind/attack speed; boostingmarket D4 WW guide ("6–10 ticks/sec"). These are the source of the D4 attack-speed conflict in § 3 and are **not** treated as authoritative.
