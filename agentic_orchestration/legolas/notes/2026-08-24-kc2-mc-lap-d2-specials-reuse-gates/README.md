# KC2 MODEL-COMPLETION RUN · Wave 1 · **D-2 — REUSE GATES FOR THE SILENT SPECIAL SLOTS**

**Date:** 2026-08-24 · **Seat:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (Wave 1, piece **D-2**)
**Ruling note:** `…/2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` § 2 facet **(c)** — ruled **BOTH** (sim + baton)
**Gate:** per-slot **DECODED** or **UNDECODABLE-FROM-SUBSTRATE**; slot-level table covering every slot **required**
**Discipline:** READ-ONLY on vendor corpus + engine substrate. **Law 3 absolute** — no fitted constants, no invented rules.

---

## 0 · HEADLINE

**Every slot decoded. 65 of 65, no residue.**

The 45/58 "silent specials" are **not a substrate gap**. They are an **extraction-coverage gap**. The reuse
gate for a monster special has never lived on the skill record in Grim Dawn — it lives on the **owner
creature record**, as a four-field group (`specialAttack{N}Chance` · `Delay` · `Timeout` · `Range`) declared
by Grim Dawn's own template `templatebase/monsterskillmanager.tpl` and read by `Game.dll`'s `Monster` class.
`pm2_tg2_attack_slots.csv` extracted that group for the **169 roster bodies only**; the **39 pet bodies** were
never visited. The sim then correctly refused to fire what it could not measure (`threat.py:850`), and
correctly counted the refusal (`pet_special_slots_ungated`). The refusal was right. The gap was upstream.

Reading the same four fields off the pet creature records closes it: **65/65 slots carry `Chance`, `Delay`,
`Timeout` and `Range`** — 100 % population, zero absences, no defaults consulted.

| | count |
|---|---|
| pet special slots enumerated (record × slot) | **65** |
| **DECODED** (Delay present ⇒ a reuse gate exists and is measured) | **65** |
| **UNDECODABLE-FROM-SUBSTRATE** | **0** |
| — of which the sim fires **today** | **14** |
| — of which the sim suppresses **today** (the "silent specials") | **51** |
| distinct pet special **skills** | 57 (13 with own `skillCooldownTime`, 44 without) |
| distinct pet **bodies** carrying a special slot | 39 |
| distinct roster owners that summon them | 27 |

> **Count reconciliation — `threat.py:606-612` is stale by one.** The docstring says *"only 13 of 58 pet
> special SKILLS declare their own `skill_cooldown_s`"* and the run brief inherits **45/58**. Measured against
> the substrate as it stands today (`pm2_tg2_attack_damage.csv` sha `e250089e…`): the grain is **distinct
> skills = 57**, of which **13** declare `skillCooldownTime` and **44** do not; at **slot** grain it is
> **65 = 14 firing + 51 suppressed**, which is also what `LoadReport.pet_special_slots_ungated` returns when
> the loader is actually run (**51**, both `dot_corrections` settings). The "58/45" pair is an off-by-one
> against a *skill*-grain count and does not match the *slot*-grain number the code emits. **This table is
> at slot grain and covers all 65** — a superset of the commissioned 58, so no slot is unrowed. Flagged for
> the docstring, not a decode issue.

---

## 1 · THE STRUCTURAL FINDING — how Grim Dawn actually gates special reuse

Decoded first-of-kind from **Grim Dawn's own template file**, `templatebase/monsterskillmanager.tpl` inside
`database/templates.arc` (sha `679db83f…`) — the authoritative schema, with the developers' own description
strings. Verbatim:

| field | template `type` | template `description` (verbatim) |
|---|---|---|
| `specialAttack{N}SkillName` | `file_dbr` | *(blank)* |
| `specialAttack{N}Chance` | `real` | `[0..100]` |
| `specialAttack{N}Delay` | `real` | `Seconds - delay for special skill use` |
| `specialAttack{N}Timeout` | `real` | `Seconds - time out for all skill use` |
| `specialAttack{N}Range` | `string` | *(enum)* `AnyRange;ShortRange;MediumRange;LongRange` |
| `shortRangeMin` / `shortRangeMax` | `real` | default `0` / `4` |
| `mediumRangeMin` / `mediumRangeMax` | `real` | default `4` / `15` |
| `longRangeMin` / `longRangeMax` | `real` | default `8` / `20` |

**So the firing rule of a GD monster special is a four-term gate held by the CASTER, not the skill:**

1. **`Chance` — a usage weight, 0..100**, per offer. (This is the "usage probability field" the brief asked
   for; it exists and it is measured on all 65.)
2. **`Delay` — the per-slot reuse cooldown in seconds.** Measured pet range **1.5 – 50.0 s, median 6.0 s**
   (roster comparison: 482 slots, 0.5 – 240.0 s, median 7.0 s — the two distributions sit in the same band,
   which is *evidence*, not a borrowed constant; nothing was imported across).
3. **`Timeout` — seconds, "time out for **all** skill use".** Measured pet range **0.0 – 6.0 s, mode 3.0 s**.
   This is a *different quantity from `Delay`*: `Delay` re-arms **this slot**, `Timeout` locks out **the kit**.
   ⚠ See § 3 CARRIED-QUESTION-1 — the field's value is decoded; its exact scope is a reading, not a decode.
4. **`Range` — a distance gate, and it RESOLVES TO METRES.** The enum names a band; the **same creature
   record** carries that band's metre annulus in `{short|medium|long}Range{Min|Max}`, and Lap F closed
   *DB length unit == metre, no conversion factor* (`SkillDistanceFormat={%.1f0 {^E}Meter %s1}`;
   `meleeTargetDistance` = 2.4000000953674316 = the sim's `D_ENGAGE_M`). **65/65 pet slots resolve to a
   metre annulus.** Examples: `ShortRange → 0.0–4.0 m` (19 slots), `MediumRange → 2.0–16.0 m` (8),
   `LongRange → 5.0–18.0 m` (2), `AnyRange → 0.0–longRangeMax`.

**Corroboration in the binary.** `vendor/grim-dawn/Game.dll` (sha `4876d6bd…`) carries all forty
`specialAttack1..8 × {SkillName, Chance, Delay, Timeout, Range}` names as a contiguous string block,
immediately adjacent to `Monster::ApplyReplicationData` and `Monster::JoinMe()` diagnostics and directly
followed by `buffSelfSkillName · buffOther*SkillName · healSkillName · healSkillDelay · berserkSkillName ·
initial2SkillName · {short,medium,long}Range{Min,Max} · chainInitialSkill · chainNextSkill · chainBehavior`.
The gate group is read by the **`Monster` class**, not by the skill system. That is the structural fact.

**A second, load-bearing consequence: `range_band` is no longer a label.** `threat.py:1747` records
*"`range_band`: carried for provenance, **NEVER converted to metres** — the corpus contains no metres for the
label (GL-12)"*. That statement is **now falsified by measurement**: the metres are on the creature record,
two fields away from the band name, and they are populated on **164/164 roster bodies and 39/39 pet bodies**.
This unlocks a distance gate the sim has never modelled **on the roster's 412 firing special slots too** —
not just on the 51 silent pet ones.

---

## 2 · THE SLOT TABLE — all 65 (rows 1–51 silent today · rows 52–65 already firing)

`Delay` bolded because it is the field that ends the suppression. `anim s` in parentheses = the
`__spell__` fallback animation rather than a direct `skillSpecialAnimationName` reference; `—` = no
animation timing binds. Full-fidelity rows (including every skill-side timing field, the per-body
`{short,medium,long}Range{Min,Max}` and the animation-binding grade) are in
`d2_special_slot_gates.csv` (sha `c7a14c6d…`).

| # | pet body | slot | skill | fires today | Chance % | Delay s | Timeout s | Range gate (band → m) | skillCooldownTime s | anim s | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `aetherialworm_b01_summon` | special1 | `aetherialworm_poisonspit` | silent | 100.0 | **1.5** | 1.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 2 | `aetherialworm_b01_summon` | special2 | `aetherialworm_poisonburst` | silent | 80.0 | **5.0** | 3.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 3 | `aetherialworm_b02_summon` | special1 | `aetherialworm_firespit` | silent | 100.0 | **1.5** | 1.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 4 | `aetherialworm_b02_summon` | special2 | `aetherialworm_fireburst` | silent | 80.0 | **5.0** | 3.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 5 | `aetherialworm_b03_summon` | special1 | `aetherialworm_icespit` | silent | 100.0 | **1.5** | 1.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 6 | `aetherialworm_b03_summon` | special2 | `aetherialworm_iceburst` | silent | 80.0 | **5.0** | 3.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 7 | `aetherialworm_b04_summon` | special1 | `aetherialworm_lightningspit` | silent | 100.0 | **1.5** | 1.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 8 | `aetherialworm_b04_summon` | special2 | `aetherialworm_lightningburst` | silent | 80.0 | **5.0** | 3.0 | MediumRange → 2.0–16.0 | — | 0.6 | DECODED |
| 9 | `chthoniandevourer_a01_summon` | special1 | `chthoniandevourer_chomp` | silent | 33.0 | **4.0** | 3.0 | MediumRange → 4.0–18.0 | — | 0.8333 | DECODED |
| 10 | `chthoniandevourer_b01_summon` | special1 | `chthoniandevourer_megachomp` | silent | 100.0 | **7.0** | 3.0 | ShortRange → 0.0–3.0 | — | 0.8333 | DECODED |
| 11 | `chthonianleech_a01_summon` | special1 | `chthonianleech_vampiricswipe_01` | silent | 100.0 | **5.0** | 2.0 | ShortRange → 0.0–4.0 | — | — | DECODED |
| 12 | `chthonianminion_b01_summon` | special2 | `chthonicminion_novalifedrain01` | silent | 50.0 | **8.0** | 2.0 | ShortRange → 0.0–4.0 | — | (1.5333) | DECODED |
| 13 | `chthonianminion_b01_summon` | special3 | `attackradius_chaosvortex` | silent | 50.0 | **6.0** | 4.0 | LongRange → 8.0–18.0 | — | (1.5333) | DECODED |
| 14 | `chthonianservitor_a01_summon` | special1 | `chthonianservitor_impale` | silent | 100.0 | **6.0** | 2.0 | ShortRange → 0.0–4.0 | — | 1.2333 | DECODED |
| 15 | `ghost_b01_summon` | special1 | `ghost_phantomblade` | silent | 100.0 | **8.0** | 2.0 | MediumRange → 4.0–15.0 | — | 0.6333 | DECODED |
| 16 | `ghost_b02_summon` | special1 | `ghost_shadowstrike` | silent | 100.0 | **8.0** | 2.0 | LongRange → 7.0–22.0 | — | 0.7 | DECODED |
| 17 | `ghost_b03_summon` | special1 | `ghost_bladearc` | silent | 100.0 | **9.0** | 3.0 | ShortRange → 0.0–4.0 | — | 0.9667 | DECODED |
| 18 | `ghost_b04_summon` | special1 | `ghost_bladearc` | silent | 100.0 | **9.0** | 3.0 | ShortRange → 0.0–4.0 | — | 0.9667 | DECODED |
| 19 | `hellhound_witchgod_b01_summon` | special1 | `hellhound_witchgod_lightningbreath` | silent | 100.0 | **7.0** | 3.0 | ShortRange → 0.0–5.0 | — | 3.0333 | DECODED |
| 20 | `korvaakservant_a01_summon` | special1 | `korvaakservant_triplelightningflail` | silent | 50.0 | **6.0** | 0.0 | ShortRange → 0.0–4.0 | — | 1.2 | DECODED |
| 21 | `korvaakservant_a02_summon` | special1 | `korvaakservant_triplefireflail` | silent | 50.0 | **6.0** | 0.0 | ShortRange → 0.0–4.0 | — | 1.2 | DECODED |
| 22 | `korvaakservant_b01_korvaaksummon` | special1 | `korvaakservant_lightningstream` | silent | 100.0 | **8.0** | 0.0 | MediumRange → 0.0–12.0 | — | 2.7 | DECODED |
| 23 | `korvaakservant_b02_korvaaksummon` | special1 | `korvaakservant_firestream` | silent | 100.0 | **8.0** | 0.0 | MediumRange → 0.0–12.0 | — | 2.7 | DECODED |
| 24 | `livingplant_a01_summon` | special1 | `livingplant_bite` | silent | 90.0 | **3.0** | 1.0 | ShortRange → 0.0–2.5 | — | 1.7 | DECODED |
| 25 | `livingplant_a01_summon` | special2 | `livingplant_venomousseed` | silent | 100.0 | **2.0** | 0.0 | MediumRange → 2.5–22.0 | — | 1.4667 | DECODED |
| 26 | `nemesis_orderdeathsvigil_01_revenantsummon` | special2 | `chthonicminion_novalifedrain01` | silent | 75.0 | **10.0** | 4.0 | ShortRange → 0.0–4.0 | — | (1.3667) | DECODED |
| 27 | `raptor_witchgod_b01_summon` | special1 | `chthonianleech_drainlife` | silent | 100.0 | **8.0** | 3.0 | AnyRange → 0.0–18.0 | — | (1.3667) | DECODED |
| 28 | `raptor_witchgod_b01_summon` | special2 | `raptor_witchgod_chaoswind` | silent | 100.0 | **7.0** | 1.0 | ShortRange → 0.0–8.0 | — | 3.2333 | DECODED |
| 29 | `skeleton_c01_summon` | special1 | `skeleton_fireballnova` | silent | 100.0 | **7.0** | 4.0 | MediumRange → 3.0–12.0 | — | 2.0333 | DECODED |
| 30 | `swampcrab_b01_summon` | special1 | `swampcrab_clawslam` | silent | 100.0 | **4.0** | 0.0 | ShortRange → 0.0–3.0 | — | 0.7 | DECODED |
| 31 | `swampcrab_b01_summon` | special2 | `ghostcrab_waterbreath` | silent | 100.0 | **3.0** | 1.0 | ShortRange → 0.0–3.0 | — | 1.6667 | DECODED |
| 32 | `swampcrab_b01_summon` | special3 | `swampcrab_waterspoutstrike` | silent | 100.0 | **6.0** | 2.0 | ShortRange → 0.0–3.0 | — | 1.1667 | DECODED |
| 33 | `swampcrab_c01_summon` | special1 | `swampcrab_clawslam` | silent | 100.0 | **4.0** | 0.0 | ShortRange → 0.0–5.0 | — | 0.7 | DECODED |
| 34 | `swampcrab_c01_summon` | special2 | `swampcrab_shellspin` | silent | 100.0 | **6.0** | 1.0 | ShortRange → 0.0–5.0 | — | 1.1667 | DECODED |
| 35 | `wraith_a01_summon` | special1 | `wraith_shadowstrike` | silent | 80.0 | **5.0** | 2.0 | LongRange → 5.0–18.0 | — | 1.4667 | DECODED |
| 36 | `wraith_b01_summon` | special1 | `wraith_shadowstrike` | silent | 90.0 | **5.0** | 3.0 | LongRange → 5.0–18.0 | — | 1.4667 | DECODED |
| 37 | `wraith_b01_summon` | special2 | `wraith_leechnova` | silent | 100.0 | **5.0** | 2.0 | ShortRange → 0.0–6.0 | — | (1.2333) | DECODED |
| 38 | `wraith_c01_summon` | special1 | `wraith_soulsiphon_buff` | silent | 100.0 | **8.0** | 2.0 | MediumRange → 0.0–5.0 | — | 1.3667 | DECODED |
| 39 | `wraith_c01_summon` | special2 | `wraith_illomen_buff` | silent | 100.0 | **10.0** | 3.0 | AnyRange → 0.0–22.0 | — | (1.2333) | DECODED |
| 40 | `wraith_c01_summon` | special4 | `wraith_homingwrath` | silent | 80.0 | **14.0** | 6.0 | LongRange → 9.0–22.0 | — | 1.3667 | DECODED |
| 41 | `bladeswarm_a01` | special1 | `bladeswarm_skill_showerofblades` | silent | 100.0 | **3.0** | 5.0 | LongRange → 0.0–10.0 | — | (0.8667) | DECODED |
| 42 | `gabbalthunn_obsidianshard` | special1 | `gabbalthunn_obsidianshard_chaoseruption` | silent | 100.0 | **3.0** | 1.0 | AnyRange → 0.0–15.0 | — | — | DECODED |
| 43 | `pet_celestialeffigy` | special1 | `petskill_celestialeffigy_stormcaller` | silent | 100.0 | **50.0** | 2.0 | AnyRange → 0.0–15.0 | — | — | DECODED |
| 44 | `pet_celestialeffigy_02` | special1 | `petskill_celestialeffigy_stormcaller` | silent | 100.0 | **50.0** | 2.0 | AnyRange → 0.0–15.0 | — | — | DECODED |
| 45 | `dravis_thrall_01` | special1 | `dravisthrall_boneharvest` | silent | 100.0 | **8.0** | 2.0 | MediumRange → 0.0–8.0 | — | (2.0333) | DECODED |
| 46 | `dravis_thrall_01` | special3 | `dravisthrall_icedoubleclaw` | silent | 100.0 | **5.0** | 1.0 | ShortRange → 0.0–4.0 | — | 2.5333 | DECODED |
| 47 | `dravis_thrall_01b` | special1 | `dravisthrall_boneharvest` | silent | 100.0 | **7.0** | 2.0 | MediumRange → 0.0–8.0 | — | (2.0333) | DECODED |
| 48 | `dravis_thrall_01b` | special3 | `dravisthrall_icedoubleclaw` | silent | 100.0 | **4.0** | 1.0 | ShortRange → 0.0–4.0 | — | 2.5333 | DECODED |
| 49 | `dravis_thrall_01b` | special4 | `dravisthrall_soulsiphon_buff` | silent | 100.0 | **10.0** | 3.0 | MediumRange → 0.0–8.0 | — | (2.0333) | DECODED |
| 50 | `mindreaper_summon` | special1 | `mindreaper_01_mirrormeleescissors` | silent | 70.0 | **8.0** | 6.0 | ShortRange → 0.0–4.0 | — | 0.9667 | DECODED |
| 51 | `mindreaper_summon` | special2 | `mindreaper_01_mirrorspinattack` | silent | 70.0 | **6.0** | 4.0 | ShortRange → 0.0–4.0 | — | 0.7667 | DECODED |
| 52 | `bonerat_witchgod_a01_summon` | special1 | `bonerat_witchgod_frenzy` | **FIRES** | 100.0 | **15.0** | 3.0 | ShortRange → 0.0–5.0 | 15.0 | (1.7) | DECODED |
| 53 | `chthoniandevourer_b02_summon` | special1 | `chthoniandevourer_vomit` | **FIRES** | 100.0 | **9.0** | 3.0 | ShortRange → 0.0–4.0 | 3.0 | 1.7 | DECODED |
| 54 | `hellhound_witchgod_b01_summon` | special2 | `hellhound_witchgod_stormcaller` | **FIRES** | 100.0 | **12.0** | 5.0 | MediumRange → 0.0–8.0 | 15.0 | (0.9) | DECODED |
| 55 | `korvaakservant_a01_summon` | special2 | `korvaakservant_lightningorbital` | **FIRES** | 50.0 | **6.0** | 2.0 | ShortRange → 0.0–4.0 | 3.0 | (0.9) | DECODED |
| 56 | `korvaakservant_a02_summon` | special2 | `korvaakservant_fireorbital` | **FIRES** | 50.0 | **6.0** | 2.0 | ShortRange → 0.0–4.0 | 3.0 | (0.9) | DECODED |
| 57 | `skeleton_c01_summon` | special2 | `skeleton_ringofflame1` | **FIRES** | 50.0 | **20.0** | 3.0 | ShortRange → 0.0–4.0 | 20.0 | (1.3667) | DECODED |
| 58 | `wormworldrot_a01_summon` | special1 | `dermapteran_madqueen_spines` | **FIRES** | 100.0 | **1.5** | 1.0 | AnyRange → 0.0–18.0 | 1.0 | (2.0) | DECODED |
| 59 | `wormworldrot_a01_summon` | special2 | `deepdweller_barf` | **FIRES** | 75.0 | **4.0** | 2.0 | MediumRange → 2.0–9.0 | 3.0 | 0.6 | DECODED |
| 60 | `wraith_b01_summon` | special3 | `wraith_dreadaura_buff` | **FIRES** | 80.0 | **14.0** | 3.0 | ShortRange → 0.0–6.0 | 14.0 | (1.2333) | DECODED |
| 61 | `wraith_c01_summon` | special3 | `wraith_despairaura_buff` | **FIRES** | 80.0 | **14.0** | 3.0 | ShortRange → 0.0–4.0 | 14.0 | (1.2333) | DECODED |
| 62 | `firedevil_01` (`nonplayerskills/…/pets/`) | special1 | `firewind_scorchedearth` | **FIRES** | 75.0 | **9.0** | 4.0 | ShortRange → 0.0–8.0 | 3.0 | — | DECODED |
| 63 | `firedevil_01` (`nonplayerskillsgdx1/…/pets/`) | special1 | `firewind_scorchedearth` | **FIRES** | 75.0 | **9.0** | 4.0 | ShortRange → 0.0–8.0 | 3.0 | — | DECODED |
| 64 | `dravis_thrall_01` | special2 | `dravisthrall_chillwind` | **FIRES** | 100.0 | **14.0** | 4.0 | ShortRange → 0.0–4.0 | 1.0 | (2.0333) | DECODED |
| 65 | `dravis_thrall_01b` | special2 | `dravisthrall_chillwind` | **FIRES** | 100.0 | **12.0** | 4.0 | ShortRange → 0.0–4.0 | 1.0 | (2.0333) | DECODED |

*(Rows 62/63 are two distinct pet body records at two archive paths, both `Class = Monster` per IS-3, both
resolving to the same skill name — they are separate bodies and are rowed separately, not deduplicated.)*

**Animation / cast timing (the brief's third ask).** `special_anm_dur_s` measured by direct
`skillSpecialAnimationName → charAnimationTableName → .anm` frame count ÷ 30 fps, same binding chain as the
roster lap: **39/65 DIRECT-REF**, **20/65 `__spell__` fallback only**, **6/65 no animation timing binds at
all** (declared absence, never defaulted). `skillChargeDuration` is populated on **0/65** — no pet special
telegraphs by charge time; `skillActiveDuration` on 13/65.

---

## 3 · CARRIED QUESTIONS — decoded values, undecoded *composition*

Law 3 boundary. The **parameters** are decoded. Three questions about how a runtime **composes** them are
not answered by the substrate and are handed up rather than guessed.

**CARRIED-QUESTION-1 — `Timeout` scope.** GD's own description reads *"Seconds - time out for **all** skill
use"*, which reads as a **kit-wide lockout after any special fires** (a global cooldown), and would explain
why `Timeout` (0–6 s) is an order smaller than `Delay` (1.5–50 s) and roughly tracks the animation duration.
But the template declares a *separate* `Timeout` per slot 1..8, and the description sits only on slot 1
(2..8 are blank). Both readings — per-slot recovery window vs. shared kit lockout keyed to whichever slot
fired — fit the field layout. **The values are DECODED; the scope is a READING.** The sim currently loads
`timeout_s` and **never reads it** (`threat.py:862` writes it; no other line consumes it). Recommend a named
declared reading rather than a silent default.

**CARRIED-QUESTION-2 — `Delay` vs `skillCooldownTime` when both exist.** On the 14 already-firing slots,
both gates are present and they **disagree on 10 of 14**. `AttackSlot.effective_cooldown_s`
(`threat.py:498-500`) prefers `skill_cooldown_s` over `delay_s`, which on those 10 picks the **shorter** gate
7 times (over-firing) and the longer 3 times:

| body | slot | `Delay` s | `skillCooldownTime` s | sim's pick |
|---|---|---|---|---|
| `chthoniandevourer_b02_summon` | special1 | 9.0 | 3.0 | shorter |
| `hellhound_witchgod_b01_summon` | special2 | 12.0 | 15.0 | longer |
| `korvaakservant_a01_summon` | special2 | 6.0 | 3.0 | shorter |
| `korvaakservant_a02_summon` | special2 | 6.0 | 3.0 | shorter |
| `wormworldrot_a01_summon` | special1 | 1.5 | 1.0 | shorter |
| `wormworldrot_a01_summon` | special2 | 4.0 | 3.0 | shorter |
| `firedevil_01` ×2 | special1 | 9.0 | 3.0 | shorter |
| `dravis_thrall_01` | special2 | 14.0 | 1.0 | shorter |
| `dravis_thrall_01b` | special2 | 12.0 | 1.0 | shorter |

They are **different quantities on different records**: `Delay` is the *AI's* re-offer interval on the
caster; `skillCooldownTime` is the *skill's own* engine cooldown. Neither the template nor the `Game.dll`
strings state a composition rule. **Whether a runtime must satisfy both (⇒ the effective gate is the larger)
or only the skill's is UNDECODABLE-FROM-SUBSTRATE.** Naming it because "prefer `skillCooldownTime`" is
currently an unexamined default, and on this evidence it under-gates 7 of 14 firing slots.

**CARRIED-QUESTION-3 — evaluation cadence.** Whether `Chance` is rolled once per attack opportunity or once
per `Delay` expiry, and whether `Delay` measures from cast-start or cast-end, is not stated anywhere in the
records or the binary strings. The sim already carries a **ruled** reading here (R-PM2-1: `delay_s` applied
as *both* initial-availability gate and reuse cooldown, per-opportunity chance roll — declared the
LOWER-damage reading). **That ruling extends to the pet slots unchanged; no new reading is proposed.**

---

## 4 · WHAT THIS HANDS TO WAVE 2 (B-4 "specials firing")

**B-4 is a data backfill, not a mechanism build.** The sim's gate machinery already exists and already
consumes exactly these fields:

- `threat.py:1337-1364 choose_slot` already implements the initial-delay gate + reuse cooldown + `chance_pct`
  roll. It suppresses pet specials at `threat.py:850` *only* because `meta.get((record, slot))` is `None`.
- `d2_special_slot_gates.csv` is emitted **drop-in against `pm2_tg2_attack_slots.csv`'s grain and reading**
  (`(record, slot)` key; `s2_lib.E3.merged` last-wins field merge — the same reading that CSV was extracted
  under). Landing the 65 pet rows into that CSV makes `m is not None` and the suppression branch stops
  firing, with no change to `threat.py` logic.
- **Cross-validation of the field mapping:** re-decoding the **roster's** 484 already-extracted special
  slots straight from the DBRs under this exact mapping reproduces **1,925 of 1,929 cells byte-identically**
  (`delay_s`/`chance_pct`/`timeout_s`/`range_band`). The 4 residual cells are one record,
  `boss&quest/korvaakmessenger_02b.dbr` slot `special5`, and they are a **reading fork**, not a mapping
  error — `gdx2` and `sm2` both carry that record and only `gdx2`'s copy has the `specialAttack5*` group, so
  whole-record-replacement (`winner`) drops it and field-merge (`merged`) keeps it. **On the 65 pet slots the
  two readings are byte-identical (0 differences across all 5 fields × 65 slots)**, so D-2's decode is
  reading-independent. The roster fork is noted for whoever owns that record; it is out of D-2's scope.
- **New capability, needs a ruling before use:** the `Range` metre annulus is a *second, independent* gate
  the sim does not model at all (`choose_slot` gates on `reach_m` only). Turning it on would change roster
  behaviour too. **Do not enable it as a side effect of B-4** — it is a scoped change with its own
  value-set-sweep obligation (Discipline #72).

**Baton (Layer 1) shape implied.** Per monster stat block, per special slot:
`{skill, chance_pct, delay_s, timeout_s, range_band, range_min_m, range_max_m, skill_cooldown_s|null,
anim_dur_s|null, anim_grade}` — every field decoded-with-provenance, plus the three CARRIED-QUESTIONS carried
as declared readings in the provenance block so the Godot runtime is never guessing silently.

---

## 5 · ADJACENT COVERAGE FINDING (unprompted; routes to **D-3**)

The `monsterskillmanager` template declares **more caster-held skill slots than the sim's `SLOT_ORDER`
models**. Censused across the 39 pet bodies and the 164 roster bodies in `pm2_tg2_attack_slots.csv`:

| field | roster bodies | pet bodies | in sim's `SLOT_ORDER`? |
|---|---|---|---|
| `specialAttack6..8SkillName` | **0** | **0** | n/a — **measured zero; the sim's special1..5 enumeration is COMPLETE** |
| `buffSelfSkillName` | 6 | 0 | **NO** |
| `buffOtherSkillName` | 15 | 0 | **NO** |
| `chainBehavior` (`UseOnCurrentEnemy;UseOnLeader;UseOnSelf;UseOnAllies`) | 21 | 0 | partially — `chain_initial`/`chain_next` modelled, the *behaviour* enum is not |
| `initial2SkillName` | 3 | 3 | **NO** (only `initialSkillName` is modelled) |
| `healSkillName` | 4 | 0 | **NO** |
| `healSkillDelay` | 104 | 25 | vestigial — a delay with no `healSkillName` on 100/104 + 25/25 |
| `berserkSkillName` | 0 | 0 | measured zero on this roster |
| `nightBuffSkill` | 0 | 0 | measured zero on this roster |

**No health-threshold field exists in the template at all.** `berserkSkillName` is the only condition-shaped
slot and its *trigger* lives in code, not in the records — and it is **unused by every body on this roster**,
so it is inert here. **The brief's "health thresholds" ask resolves to: no health-threshold gate exists on
GD monster specials.** The full firing condition set is exactly `{Chance, Delay, Timeout, Range}`. That is a
decode, not an absence-of-search.

---

## 6 · METHOD + PROVENANCE

**Slot enumeration** replays `threat.load_profiles`'s own filter chain verbatim (`status == OK`,
`rank_grade == MEASURED`, the 10-tuple exact-duplicate dedup at `threat.py:754-759`, the pet-special
suppression predicate at `threat.py:850`) against `pm2_tg2_attack_damage.csv`, so the 65 rows are *the sim's
own slots*, not a re-derivation. Verified against the running loader: `pet_special_slots_ungated == 51` under
both `dot_corrections` settings.

**Join grain.** 60/65 slots join creature-field → damage row on `skill`; **5 join on `root_skill`** — those
are nested `*_buff.dbr` records reached via `buffSkillName`, where the slot field names the root and the
damage rides the nested child (`wraith_c01_summon` ×3, `wraith_b01_summon` special3,
`dravis_thrall_01b` special4). The **gate belongs to the slot**, so root is the correct key; joining on
`skill` alone reports 5 false failures. Both keys are emitted per row (`join_key`).

**Corpus** — `vendor/grim-dawn-edition-III-20260808`, eight-archive overlay, digests byte-identical to Lap
U / Lap V / Lap Z pins:

| artifact | sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `engine/data/kc2/pm2_tg2_attack_damage.csv` | `e250089e7db3ef90f8a02dc2459c27b5bcc159a559769630aefb0167577bbf3c` |
| `engine/data/kc2/pm2_tg2_attack_slots.csv` | `eb950649576ffc785c570db81f3c9e3e7e716282564589a0c21feaff86b4b0c7` |
| `engine/data/kc2/pm2_tg2_pet_chain.csv` | `e1fa676e067bda955cf61817a3d83d53598157ac2016952a95b32a089999077a` |
| `src/reincarnated/simulation/kc2/threat.py` (read, not modified) | `eddcb6033db45261aef51987c629b3434601580eee0de8ba1e3955c36eb82205` |
| `anm_index.json` (Lap 08-08) | `59919fe2f4e204469370a0d48b92f13bfbd31323b6526a18ecd732ae5202df6d` |

Full manifest incl. this lap's own outputs: `d2_digests.json`.

**Lap artifacts**

| file | what |
|---|---|
| `d2_decode.py` | the harness (read-only; reuses `s2_lib` / `gamora_kc2_c1_closure_ed3` overlay stacks unchanged) |
| `d2_special_slot_gates.csv` | **the 65-row per-slot gate table**, full fidelity (sha `c7a14c6d…`) |
| `d2_summary.json` | counts, verdict census, `specialAttack*` creature-field census, reading-diff check |
| `d2_digests.json` | digest manifest |
| `table.md` | the § 2 table, generated |
| `monsterskillmanager.tpl.txt` | GD's own template, extracted verbatim from `templates.arc` — the § 1 schema source |

**Read-only attestation.** No write outside this directory. No vendor file, engine source, engine data file,
sim checkpoint or baton was modified. `E-s09-cp150` untouched (D5).

---

*legolas · KC2-MC Wave 1 · D-2 · 2026-08-24*
