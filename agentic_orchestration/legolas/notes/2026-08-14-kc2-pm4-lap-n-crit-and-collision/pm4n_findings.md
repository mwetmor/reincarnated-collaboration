# RUN KC2-PM4 — Lap N — crit rule (measured) + collision-width semantics (researched)

**Agent** legolas (UNKNOWN-RESEARCHER) · **Date** 2026-08-14 · **Discipline** GL-12 decode-never-estimate
**Firewall** No simulation outcome, target band, gamora note, or run charter was consulted. Sources are
this lap's own measurements, prior **legolas** lap notes, and external/primary material only.

---

## 0 — Headline

| | |
|---|---|
| **PART A verdict** | **M1 FALSIFIED · M3 FALSIFIED · M2 SUPPORTED (form), but its uniform-roll parameterization is CONTRADICTED by the footage.** The game *prints* the effective multiplier; it did not have to be inferred. |
| **PART A number** | Mean crit **tier** = **1.1588** (n=148). M1 forces exactly 1.5000 — **M1 overstates the crit term by 29.4 %**. |
| **PART B verdict** | **`projectileExplosionRadius` does NOT capture targets along the path — and it does not capture them at the terminus either. It is not the path-capture field at all.** Path capture is `actorRadius` + `collisionShape` on the *projectile actor* record. |
| **PART B confidence** | **MODERATE-HIGH** for the negative claim (three independent corpus lines). **UNDECIDED** for where the explosion itself centres on a 100 %-pierce projectile — stated as UNDECIDED, not estimated. |

---

# PART A — THE CRIT RULE, MEASURED FROM THE REFERENT VIDEO

## A.1 The decode that made this cheap

Grim Dawn's floating combat text **prints the effective crit multiplier in the number itself** —
`15380 (x1.67)`. Non-crits print bare (`39331`). So crit-vs-non-crit and the multiplier value are
both *read*, not inferred. Nothing in Part A is a model fit.

Visual confirmation (frame t = 750.0 s) shows crits and non-crits are the **same colour** (cream,
mean RGB 228/209/172). The `(xN.NN)` suffix is the *only* discriminator — colour carries no crit
signal. Red text (R/G ≥ 1.6) is damage *taken*.

## A.2 Sampling method

| item | value |
|---|---|
| referent | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (located via Lap H-2 README) |
| container | 1920×1080, 60/1 fps, 1034.10 s, 62 046 frames |
| combat span located by | 1 frame / 10 s pre-scan across the whole file → FCT present **690–800 s** and **830–860 s**; span padded to **680–870 s** |
| **FCT lifetime measured** | **~1.2–1.5 s**, by tracking single strings across a 10 fps burst at t = 749–753 s (`15380 (x1.67)` persists L009→L015 = 0.6 s clean + partials; `23106 (x1.77)` L024→L031) |
| sampling cadence | **fps = 1/2 → 2.0 s**, chosen **> measured FCT lifetime** so each FCT event is sampled **at most once** |
| dedup verification | 1 adjacent-frame repeat of an identical `(damage, mult)` pair in 90 strict reads |
| sample frames | **95**, `F0000…F0094`, timestamp `t = 680 + 2·index` s |
| OCR | Apple **Vision** `VNRecognizeTextRequest`, `.accurate`, language correction **OFF** (`ocr.swift`, compiled locally) |
| colour probe | mean RGB of the brightest 12 % of pixels inside each OCR bounding box (glyph strokes, not background) |

**Yield:** 2 328 OCR text observations → **64 clean crit reads (conf 1.0)** → **154 crit-multiplier
tokens** once merged/garbled lines are re-tokenised (a single OCR line can fuse two overlapping FCT
strings, e.g. `99294 (x1,99) 8499 (x2.09)` — both events are recovered).

## A.3 The measured multiplier distribution

```
   x1.39     2      x1.79    29        off-lattice OCR noise:
   x1.42     1      x1.87     5           x1.42, x1.51, x1.70   (3 of 154 = 1.9 %)
   x1.51     1      x1.89    30
   x1.67    46      x1.97     1
   x1.70     1      x1.99     5
   x1.77    31      x2.09     1
```

**98.1 % of all tokens (151/154) fall on a lattice of spacing exactly 0.10**, in **two offset
families** distinguished by their residue mod 0.10:

| family | residue | values observed | n |
|---|---|---|---|
| **A** | `.07` | 1.67 · 1.77 · 1.87 · 1.97 | 84 |
| **B** | `.09` | 1.79 · 1.89 · 1.99 · 2.09 | 67 |

Both families span the entire combat window (A: 694–864 s, B: 688–864 s), so they are **not** a
timed buff window. Family B carries markedly larger damage numbers (median 46 889 vs 15 111) —
i.e. **two different damage sources with two different crit-damage totals.**

## A.4 Decomposition — and why the offsets are +0.57 / +0.69

Crate's own documentation states the combination is **additive**: *"Equipment and Skills granting
+% Critical damage will be added to PTH Threshold multipliers. For example, with 110 % PTH and
+15 % Critical Damage, you would see 1.25x damage (1.1 + 0.15)."* (Grim Dawn Wiki, Game Mechanics.)

So `displayed = pthDamageModifier_k + critDamageTotal`, with `pthDamageModifier` on the known
1.0/1.1/1.2/1.3/1.4/1.5 ladder (spacing **0.10** — exactly the measured lattice spacing).

The two families differ by 0.02 mod 0.10, so the offset gap is 0.02 + 0.10·k. **The gap is 0.12**,
on two independent grounds:

1. **Shape test.** With gap 0.12 both families occupy the *same* tier support and the *same*
   monotone-decreasing shape. With gap 0.02, family B would have to never once roll the lowest tier
   across 65 events while peaking one rung higher — far less parsimonious.
2. **Corroboration from my own Lap L note** (`2026-08-14-kc2-pm4-lap-l-player-offense/method.md`
   line 151): the Warborn Visor grants **+12 % crit damage** — a 0.12 offset, exactly the measured gap.

| family | crit-damage total | tier support |
|---|---|---|
| A | +0.57 | 1.10 / 1.20 / 1.30 / 1.40 |
| B | +0.69 | 1.10 / 1.20 / 1.30 / 1.40 |

**Measured crit-tier distribution (n = 148):**

| tier | n | share | family A | family B |
|---|---|---|---|---|
| ×1.10 | 75 | **50.7 %** | 46 | 29 |
| ×1.20 | 61 | **41.2 %** | 31 | 30 |
| ×1.30 | 10 | 6.8 % | 5 | 5 |
| ×1.40 | 2 | 1.4 % | 1 | 1 |
| ×1.50 | **0** | **0.0 %** | 0 | 0 |

> Both families independently reproduce the same monotone-decreasing shape. That is a strong internal
> consistency check on the +0.57 / +0.69 split.

**Mean crit tier = 1.1588. Mean displayed effective multiplier = 1.7888 (median 1.77).**

The top rung ×1.50 is **never observed** in 148 lattice-conforming events. `x2.09` (family B, tier
×1.40) is the single highest read in the sample.

## A.5 Verdict against the pre-registered candidates

Candidates as defined in my Lap L note § 6.3.

| candidate | prediction | measurement | verdict |
|---|---|---|---|
| **M1** — deterministic; highest threshold passed ⇒ always ×1.5 | a **single-valued** multiplier, pinned at the top rung | **4 tiers occupied; the top rung is the one that never occurs** | **FALSIFIED** |
| **M3** — separate crit roll gated by the +% crit-damage stat | a **single** crit multiplier `1 + CD` when a crit fires | multi-rung ladder whose spacing is exactly `pthDamageModifier`'s 0.10 | **FALSIFIED** |
| **M2** — roll banded by the PTH thresholds ⇒ tier ladder, expectation strictly between 1.0 and 1.5 | multi-rung ladder on the threshold tiers; mean strictly inside (1.0, 1.5) | ladder confirmed at 98.1 % lattice conformance; **mean tier 1.1588**, strictly inside the bracket | **SUPPORTED (form)** |

**M2 is the supported family.** Its *form* is confirmed. Its usual *parameterization* is not — see A.6.

**Consequence for any consumer:** M1 forces the crit term to 1.5000; the footage says 1.1588.
**M1 overstates the crit multiplier by 29.4 %.** The bracket `critLO = 1.0 / critHI = 1.5` carried by
Lap L as declared-gap **D-L5** is now closed on the measured side: the realised value sits at
**1.159**, i.e. near the *bottom* of that bracket, not its midpoint.

## A.6 ⚑ A material contradiction to surface

Crate's official combat guide gives the roll rule explicitly: *"For PTH 107: 1-89 hits, 90-104
critically hits for 1.1x damage, 105-107 critically hits for 1.2x damage"* — i.e. **`R ~ U(1, PTH)`,
tier selected by which threshold band `R` lands in** (thresholds 70/90/105/120/130/135).

Under that rule the count in each tier band is proportional to the band's **width** times the
probability that PTH reaches it. Band widths are 15 / 15 / 10 / 5 / (PTH−135). So per-unit-roll
density is a direct readout of the **PTH survival function** `S(r) = P(PTH ≥ r)`:

| roll band | tier | n | density | implied `S(r)` |
|---|---|---|---|---|
| [90, 105) | ×1.10 | 75 | 5.00 | 1.000 |
| [105, 120) | ×1.20 | 61 | 4.07 | 0.813 |
| [120, 130) | ×1.30 | 10 | 1.00 | 0.200 |
| [130, 135) | ×1.40 | 2 | 0.40 | 0.080 |
| [135, …) | ×1.50 | **0** | 0.00 | **~0.000** |

The implied PTH distribution has its **median near ~112** and **essentially no mass at or above 135**.

My own Lap L § 6.3 computed **PTH = 149.2 – 182.2 on every body at every wave**, i.e. above the sixth
threshold everywhere. A uniform roll at PTH ≈ 150 predicts **~25 % of crits at ×1.50**. The footage
shows **0 of 148**. These cannot both describe the same events.

**Two readings, and I cannot discriminate them from video alone:**

* **(i) The PTH figure is too high** for the attacks actually generating this text, or
* **(ii) attribution** — the sampled FCT is not all player-direct-attack. The presence of **two
  distinct crit-damage totals** proves **at least two damage sources** are in the sample (procs,
  devotion, retaliation and pet damage all print FCT and carry their own OA). Under (ii) Lap L's
  player-attack PTH can be correct while most printed crits come from lower-OA sources.

**FCT cannot be attributed to source from video.** I am naming the contradiction, not resolving it.
Routing note: whichever reading holds, **the measured mean crit tier 1.1588 is the realised quantity**
and does not depend on which reading is correct.

## A.7 Crit rate — reported as a BOUND, deliberately not as a point estimate

Restricted to cream (player-dealt) text at OCR confidence 1.0, excluding health readouts and
fixed-position HUD: **87 non-crit vs 57 crit → apparent crit share 39.6 %.**

This is a **LOWER BOUND ONLY**, for a one-directional reason: crits and non-crits are the same
colour, so a crit whose `(xN.NN)` suffix is clipped or overlapped reads as a clean bare number and is
counted as a non-crit. The error can only push the measured share **down**. A second, non-directional
caveat: dense multi-hit moments garble more often and are under-sampled in both classes.
**Grade: INDICATIVE. Do not treat 39.6 % as a calibrated crit rate.**

## A.8 Part A limits

* Single referent run, waves 150–160, one build. Not a general Grim Dawn crit measurement.
* The +0.57 / +0.69 split is **inference** (well-corroborated); the **lattice, its 0.10 spacing, the
  tier count and the multiplier values are direct reads**.
* Sampling captures FCT alive at the sample instant. FCT lifetime is fixed, so this is unbiased with
  respect to multiplier value.
* OCR drops overlapping text. Overlap is spatial/temporal and there is no mechanism by which it would
  correlate with the multiplier rung; treated as unbiased, flagged as an assumption.

---

# PART B — COLLISION-WIDTH SEMANTICS (Mode A)

**Question as commissioned:** for GD projectiles with 100 % pierce, does `projectileExplosionRadius`
capture targets **along the path**, or only **at the terminus/impact point**?

**Finding: the question is mis-specified, and the corpus says so cleanly. `projectileExplosionRadius`
is neither the along-path capture nor the terminus capture — it is not the capture field at all.**

## B.1 What the schema says — nothing

The authoritative field definition lives in `database/templates.arc → templatebase/skill_projectilebase.tpl`
(read with my own ARC reader, `gd_arc_reader_2026_07_26.py`):

```
Variable
{
    name = "projectileExplosionRadius"
    class = "array"
    type = "real"
    description = ""          <-- EMPTY
    value = ""
    defaultValue = ""
}
```

Group context (`Projectile Config`), in template order:
`projectileExplosionRadius · projectileFragmentsName · projectileFragmentsLaunchNumberMin ·
projectileFragmentsLaunchNumberMax · projectileFragmentRadius · projectilePiercingChance`.

**The description string is empty.** The other four `explosionRadius` variables in the template set
are likewise blank except one (`skill_attackradiusgrow.tpl`) reading only `"Max radius"`.
**The schema does not document the semantics.** The official *Grim Dawn Modding Guide* PDF (shipped
with the game, `Grim Dawn Modding Guide.pdf`) is a workflow guide, not a field reference — it never
mentions the field; its only projectile/pierce text is *"You can assign a custom projectile as well
as a chance for the weapon attacks to pierce through enemies."*

## B.2 The discriminator — path capture is a *different field, on a different record*

Skill records point at an FX projectile record via `skillProjectileName`. Those actor records carry
their own collision geometry:

```
records/fx/skillsother/orbital/hammer_projectileorbitalfx01.dbr   (projectileorbiting.tpl)
    actorRadius     = 1.2
    collisionShape  = 'Sphere'
```

I joined **every** `projectilePiercingChance = 100` skill to its FX projectile record across all four
pinned archives of GD edition III (`database.arz`, `GDX1/2/3.arz`; 93 385 records scanned):

| measure | result |
|---|---|
| pierce-100 skills resolved to an FX projectile record | **308** (1 unresolved) |
| `collisionShape` on those FX records | Sphere 197 · Box 113 · None 34 |
| `actorRadius` | **always > 0** — median 0.50, min 0.10, max 2.00 |
| `projectileExplosionRadius` | median 0.25, **zero on 103 of 308 (33.4 %)** |
| `explosionRadius == actorRadius` exactly | **8 / 308 = 2.6 %** |
| Pearson r(explosionRadius, actorRadius), n = 205 | **−0.168** (no relationship) |

**Three independent lines, all pointing the same way:**

1. **103 of 308** piercing projectile skills have **no explosion radius at all** — yet they spawn
   projectiles that demonstrably damage what they pass through. Independent count over
   `projectilePiercingChance > 0` with `skillProjectileName` set and no radius: **129 records**,
   including shipped, functional item skills — `item_bladeofkorvoran`, `item_phantomblade`,
   `item_lightningspike`, `item_siegebreaker`, `item_slayersblades`, devotion `tier1_01e_skill`,
   `tier2_06g_skill`, and boss skills such as `fabius_bladenova_proc`. **Pass-through damage does not
   require `projectileExplosionRadius`.**
2. **`actorRadius` is always present** on the projectile actor, alongside an explicit
   `collisionShape`. That is the swept collision body.
3. The two quantities are **uncorrelated** (r = −0.168) and coincide in only 2.6 % of records. They
   are independent authoring dimensions, not two names for one thing.

**Conclusion (MODERATE-HIGH confidence): targets along a piercing projectile's path are captured by
the projectile actor's `actorRadius` / `collisionShape`, evaluated as the actor moves.
`projectileExplosionRadius` is a separate, optional area-effect term layered on top.**

For a simulator this is the load-bearing correction: **`projectileExplosionRadius` must not be
modelled as the width that sweeps up targets along the path.** If a path-width term is needed, the
field to read is `actorRadius` on the record named by `skillProjectileName`.

## B.3 What remains UNDECIDED — stated plainly

**Where the explosion itself is centred on a 100 %-pierce projectile — at each pass-through contact,
or once at terminal expiry — is NOT decidable from any source I could reach.** I did not estimate it.

Sources exhausted without an answer: the `.tpl` description (empty); the official modding guide (does
not cover the field); the official combat guide and the game's own settings/modding guides; the
Crate forum modding sections; the shipped editor binaries (`DBREditor.exe`, `AssetManager.exe`,
`Editor.exe` — no field-tooltip strings recoverable); no dev (Zantai/Crate) post located. The one
forum thread that looked on-point (*"Eon band's skill projectile radius too large"*,
forums.crateentertainment.com/t/…/158275) contains **no staff reply and no mechanical explanation**.

**Evidence that leans — but does not settle — toward path-associated application:**

* **Authoring regime split.** `projectileExplosionRadius` where pierce = 100: median **0.50 m**,
  **45.6 %** at ≤ 0.25 m. Where pierce = 0: median **2.00 m**, only **2.5 %** at ≤ 0.25 m. A terminal
  blast is a terminal blast; there is no reason for pierce status to shrink the authored radius
  fourfold — unless the field is doing something path-associated when the projectile pierces.
* **The orbiting class.** 69 pierce-100 records on `skill_attackprojectileorbiting.tpl`, median radius
  0.25 m. An orbiting projectile that pierces 100 % has no impact terminus; a 0.25 m blast at an
  arbitrary mid-orbit expiry point would be functionally nil.
* **The "spines" cluster.** Linear pierce-100 skills with 0.10–0.50 m radii are dominated by
  ground-line skills — `venomspines`, `widowspine`, `*_groundspines`, `clonepoison_poisonspines`,
  `ghoul_harvoul_earthshatter`, `outlaw_dreadraven` — whose in-game behaviour is a line that damages
  along its length.
* **Crate's own player-facing text** on records that carry pierce = 100 **and** a radius:
  * `item_defenselightningorb_01.dbr` (radius 1.0) — *"Retaliates with an orb of lightning launched in
    the attacker's direction, **damaging and stunning all in its path**."*
  * `bloodmist.dbr` (radius 1.5) — *"A mist of blood corrupts the **very air it passes through**."*

  These confirm the **skills** damage along the path. Per B.2 they do **not** establish that the
  *explosion radius* is the mechanism — `actorRadius` already accounts for it.

**Grade: UNDECIDED on the centring question.** An honest UNDECIDED is the landing; no in-engine
behavioural test was available (read-only mandate, and the Wine-absent finding of
`2026-07-23-gd-mac-extraction-viability.md` still stands, so the game cannot be run on this host).

## B.4 One terminology trap worth flagging

The corpus contains **two unrelated "pierce" families** and they are easy to conflate:

* `projectilePiercingChance` — chance the projectile **passes through** an enemy (geometry). This is
  the Part B subject.
* `offensivePierce*` / `offensivePierceRatio*` — **Pierce, the armour-ignoring damage type**. Nothing
  to do with projectile geometry. Every record inspected in B.2 carries a full block of these at 0.0.

---

## Files

| file | contents |
|---|---|
| `pm4n_fct_events.csv` | 2 328 rows — **every** OCR text observation across the 95 sample frames: frame, timestamp, raw text, OCR confidence, class (`crit` / `crit_garbled` / `bare` / `health_readout` / `hud` / `other`), parsed damage + multiplier, all multiplier tokens, bounding box, sampled RGB, R/G, colour class |
| `pm4n_crit_multipliers.csv` | 154 rows — one row per crit-multiplier token: frame, t, confidence, clean-read flag, damage, multiplier, residue, offset family, implied tier, source text |
| `pm4n_digests.json` | full 64-hex sha256 + row counts (GL-6: never truncated) |

## Sources

**Primary — local, pinned, read-only**
* Referent footage: `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`
* `~/Games/vendor/grim-dawn/database/templates.arc` → `templatebase/skill_projectilebase.tpl`
* `~/Games/vendor/grim-dawn-edition-III-20260808/{database,gdx1,gdx2,gdx3}/**/*.arz` (93 385 records)
* `~/Games/vendor/grim-dawn/**/Text_EN.arc` (20 322 EN tag strings)
* `~/Games/vendor/grim-dawn/Grim Dawn Modding Guide.pdf` (official, Crate)
* Shipped editor binaries (`DBREditor.exe`, `AssetManager.exe`, `Editor.exe`) — negative result

**Primary — official, web** (accessed 2026-08-14)
* Grim Dawn official combat guide — https://www.grimdawn.com/guide/gameplay/combat/
* Grim Dawn official modding guide PDF — https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf

**Secondary** (accessed 2026-08-14)
* Grim Dawn Wiki, *Game Mechanics* — https://grimdawn.fandom.com/wiki/Game_Mechanics (crit-damage additivity)
* Grim Dawn Wiki archive, *Game Mechanics* — https://grimdawn-archive.fandom.com/wiki/Game_Mechanics

**Tertiary / negative results**
* Crate forum, *Eon band's skill projectile radius too large* — https://forums.crateentertainment.com/t/eon-bands-skill-projectile-radius-too-large/158275 (no staff reply, no mechanics)
* Crate forum modding sections — no field-level statement on `projectileExplosionRadius` located

**Own prior lap notes** (the only internal sources consulted, per firewall)
* `2026-08-13-kc2-pm4-lap-h2-video-match/README.md` — referent video location
* `2026-08-14-kc2-pm4-lap-l-player-offense/method.md` — M1/M2/M3 definitions (§ 6.3), D-L5, Warborn Visor +12 % crit damage
* `2026-07-23-gd-mac-extraction-viability.md` — Wine absent on this host
* `2026-07-23-gd-arz-extraction-probe.md`, `2026-07-26-gd-displayname-bridge.md` — ARZ/ARC format lineage
