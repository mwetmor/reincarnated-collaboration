# E3 re-spec **v2** — the six drafts reconciled against what landed after 13:18

> **STATUS:** DRAFT for Run C-7's P0 filing — gandalf (SPEC-AUTHOR sub-agent), 2026-09-16.
> **NOT APPLIED anywhere.** Nothing under `astra_test_01/` or `canonical/` was written. These seven files live only in this scratchpad.
>
> **What v2 is.** The v1 drafts were authored **13:12–13:18** against the audit's §§ 1–12. Four things landed **after** them and none is in v1:
> 1. **R-C5-125** (21:20) — Poisonous Concoction is the **full Occultist combo**, and the C-7 skill order.
> 2. **Legolas § 13** (the combo as played, third pass) — the measurements that combo is built from.
> 3. **R-C5-106 / 112** — the Blackwater **lane** spec: the 520 px touch range, the walkable landing clamp, rank-1 baked.
> 4. **R-C5-122 / 124** — the fire vocabulary moved to **`fire_burst_e0p_v3`** + the FL-5 ending. v1 still named `v2`.
> Plus **R-C5-96** (the canonical capsule collider), which v1 carried in no file, and **charter F1/F3**, which v1 marked only as loose prose `"pending F4"`.
>
> **Every number still traces to a named row or is boxed HOUSE / AUTHORED.** No number was invented and nothing is carried from conductor memory. Where a figure could not be sourced it is `null` with the reason (see `lightning_blast.polyline.fork.filament_count`).

**Scale.** 130 px = 1 BH throughout. § 13's rows were measured at BH = 90 px (3.16 clip) / 93 px (3.19); § 12's at BH = 137 px (PoE), 134 (LE Mage), 119 (LE Paladin), 228 (D2R), 180 (Hades), 83 (GD). All report **BH**, so all convert at ×130 into the C-5 px space. This is stated in every file's `scale.note`.

**Source-tag key.** `TBL-A` / `TBL-B §n` = the findings' Table A / Table B skill section · `§n` = findings section · `§12.1 row n` / `§13.4 <cell>` = frame measurement · `R-C5-nn` = ledger ruling · `HOUSE` = declared deviation · `AUTHORED` = a register choice matched to a measurement but not sourced to a gameplay figure · `DERIVED` = arithmetic off a named row, shown.

---

## Cross-cutting changes (all six files)

| Change | v1 | v2 | Why | Source |
|---|---|---|---|---|
| **FF-08 handling** | prose `provenance.ff08: "pending F4"`; `*_cv_min` kept | **charter F1 recommendation (a) authored as the DEFAULT**: mechanics cadences are source metronomes with `cadence_kind`; `*_cv_min` kept as a non-satisfied HOUSE key; a top-level **`pending_rulings`** map names every governed key | one grep (`pending_rulings`) flips the whole commission if Matt rules (b) or (c) | Charter § 4 F1 · Q80 F4 |
| **`pending_rulings` key** | absent | **new top-level object**, key-path → ruling id | scalar keys cannot each carry an inline marker without ambiguity (healing_hands needs **two different** pendings in one file). A path map marks every key, is greppable, and adds exactly one top-level key per file | this pass |
| **`exporter_needs` array** | absent (the TOOLING list lived only in the prose table) | **new top-level array per file** | charter § 2 names E3-r1 as the TOOLING gate; the capability list must ride with the file, not with a scratchpad table | Charter § 2 |
| **`collision` (R-C5-96)** | **absent from all six** | present in all six: capsule where a projectile exists (frozen_orb children + darts, poisonous_concoction flask, zeus_chain ball), explicit **`null` + note** where none does (lightning_blast, healing_hands), explicit "none in flight" for blackwater | R-C5-96 made the capsule the canonical collider and retired painted envelopes from collision. A spec that omits it re-opens the defect it closed | R-C5-96 |
| **`v1_delta` provenance line** | — | added to every file | so the conductor can see at a glance whether a file changed materially or only gained marks | this pass |

---

## 1 · `blackwater_cocktail` — the lane convention restored, the fire vocabulary caught up

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `mechanics.range_px` | 1083 | **520** | v1 authored the **source** range and dropped the lane's touch convention | **HOUSE** per R-C5-92 (no aim assist; drag-to-aim accepted) + R-C5-106/112 lane spec |
| `mechanics.range_max_source_px` | *absent* | **1083** | the source figure is preserved, not lost | TBL-B §2 (VERIFIED .arz) |
| `mechanics.arc.flight_s` | 0.83 | **0.40** | DERIVED at 520: 520 ÷ (18 m/s × 72.2 px/m) | R-C5-112 (baked) + TBL-B §2 velocity |
| `mechanics.arc.apex_px` | 88 | **42** | DERIVED at 520: 520·tan 18° ÷ 4 | `launchAngle 18.0°` VERIFIED |
| `mechanics.arc.flight_scales_with_landing_distance` | *absent* | **true** | the clamp shortens real flights | R-C5-112 |
| `mechanics.landing_clamp` | **absent** | **`walkable_union`** | **v1 missed a lane fact already in the build** — F-C5-35 (pool in the sky / on the void) was closed by this clamp | R-C5-106 (defect) / R-C5-112 (fix) |
| `mechanics.collision` | absent | **`{in_flight: none}` + note** | states why the capsule does *not* apply here but *does* on PConc | R-C5-96 |
| `presentation…impact` | `fire_burst_e0p_v2` at 0.7 | **`fire_burst_e0p_v3` at 0.7 + the FL-5 ending** (small central white-core painted decal that subsides, tighter embers, smoky fog shrouding them; interleave 5–7, gaps ≤40°) | v1's fire vocabulary is a lap behind Matt's eye | R-C5-122 (Matt on v40) + R-C5-124 (FL-5 Part E); verified against `vfx_kits/v9/fire_burst_e0p_v3/kit.json` — `interleave.count [5,7]`, `core_residue 0.6 BH / 0.5 s`, `smoke 0.8 BH / 0.9 s`, tightened `ember_ending` |
| `mechanics.field.tick_*` | metronome [0,1,2] | **unchanged**, + `pending_rulings` ×4 | already right at v1; now flippable in one pass | §4 / §0(b) `targetInterval 1000 ms` (VERIFIED) |
| `g2_mode` | *absent* | **`lobbed_field`** | distinguishes it from PConc's `lobbed_burst` in the same grammar | TBL-B §2 vs §3 |
| `provenance.ff08` | "pending F4" | **names the exemption**: `lick_flicker_hz` is MEASURED SOURCE, **not** house jitter, and survives any F1 ruling — so it is *not* marked pending | the one thing a careless F1(b) "drop FF-08" could delete by mistake | §12.1 row 4b (MEASURED) |
| everything else (rank 1, 181 px / 2.78 BH, 2.5 s, burn 3.0 s, residue 12 s smudge, licks 3.3–3.6 Hz, bounce false HOUSE, shards HOUSE) | — | **unchanged** | v1 was correct | TBL-B §2 · §12.1 rows 4a–4c |

---

## 2 · `poisonous_concoction` — rebuilt as the three-component Occultist combo

**This is the file that changed most.** v1 was the **gem alone plus a HOUSE dark puddle** under the then-live R-C5-80. R-C5-91 rescinded the puddle; **R-C5-125 then widened the skill to the full combo**. v2 is a different spec, not an edit.

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `combo` (new top-level) | — | **three declared components** + a `nothing_black` clause | R-C5-125 requires each element declared with its source | R-C5-125 |
| `mechanics.residue` | `ground_puddle_decal`, 325 px, 4.0 s, HOUSE | **`null`** — deleted, not narrowed | R-C5-91 (Matt: *"The black circles are not part of poisonous concoction builds that I am seeing. Legolas is correct."*), upheld by R-C5-125 | §13.0 / §13.2 — three Occultist clips, no black ground from any source; Profane Ground + flask caustic ground ruled out **at source** |
| `mechanics.vial_fan` | — | **count 5** (source range 4–5), landing scatter **325 px / 2.5 BH**, cluster **676 px / 5.2 BH** | *"that fan, not a larger radius, is what makes an endgame cast look endgame"* | §13.1 (GMP+GV avg **4.5 overlaps**; the one correction owed to §5) · §13.4 **A3** (440–498 px @ BH 90 → 4.9–5.5 BH) · scatter **DERIVED** = 5.2 − 2.7 |
| `mechanics.burst.vfx_diameter_px` | 422 (3.25 BH) | **351 (2.7 BH)** | §13 is the combo reference R-C5-125 names; A2 measures the single cast | §13.4 **A2** (237 × 250 px @ BH 90 → 2.6 × 2.8 BH). **Recorded conflict:** §12.1 row 5b's independent Act-3 control reads 3.0–3.45 BH @ BH 137. The two bracket 2.6–3.45; A2 chosen, both cited |
| `mechanics.burst.colour_rgb` | prose "acid-green" | **[78, 202, 29]** | three greens must be separable by colour in one frame | §13.4 **A1** (MEASURED, HIGH) |
| `mechanics.burst.onset_frames` / `peak_s` | prose | **1 / 0.10** | | §13.4 **A4** |
| `mechanics.burst.life_s` | 0.32 | **0.32 unchanged** | A5 confirms §12 exactly | §13.4 **A5** (0.30–0.35 s, four casts) |
| `mechanics.burst.edge_profile_px` | — | **90 % @ 4 px · 50 % @ 84 px · 10 % @ 182 px, `hard_rim: false`** | *"no hard rim: a plume-and-whip-arc silhouette, not a disc"* | §13.4 **A7** (3 / 58 / 126 px @ BH 90 → 0.033 / 0.644 / 1.40 BH → ×130) |
| `mechanics.burst.hitbox_radius_px` | 130 | **130 unchanged** | the damage row, kept separate from the look row | TBL-A §3 (18 u = 1.8 m = 1.00 BH radius, VERIFIED) |
| `mechanics.profane_bloom` | — | **NEW component**: trigger `struck_body`, anchor = the struck body, **208 px / 1.6 BH**, growth **0.07 s**, life **0.35 s**, fuchsia **[252, 72, 253]**, core 39 px / 50 % 69 px / 10 % 116 px, residue `null`, cascade noted as emergent | R-C5-125 names it; §13.6: *"the ground partner it actually has, which is a **kill-triggered** one, not a cast-triggered one"* | §13.4 **B1 · B2 · B3 · B5 · B6 · B8 · B9** (B4 cascade + B7 recurrence recorded as emergent, not authored) |
| `…profane_bloom.trigger_note` | — | **struck, not killed — and says so** | R-C5-125 words it "struck/killed"; at source the trigger is a **cursed enemy's death**, and **nothing dies in the dummy scene**. Recorded, not smuggled | R-C5-125 + §13.2 rank 2 |
| `mechanics.plague_bearer_field` | — | **NEW component**: **player**-anchored, persistent teal **[91, 152, 135]**, release period **5.5 s**, release field **715 × 377 px (5.5 × 2.9 BH)**, release colour **[112, 165, 26]** | R-C5-125; and §12.3 had already identified this as what the "dark ground" actually was | §13.4 **C1 · C2 · C3 · C4** |
| `presentation.layering` | — | **the bed / inside / outside rule** | three colours separable in one frame; the vial fires *inside* the field, the blooms *outside* at the bodies | §13.4 **C5** |
| `mechanics.landing_clamp` | absent | **`walkable_union`** | a fan of five must not scatter flasks into the void | R-C5-112 (the clamp is a G2 lane fact, not a Blackwater one) |
| `mechanics.collision` | absent | **capsule, R-C5-96** | this flask **can** hit a body mid-flight — the one G2 that needs the collider | R-C5-96 + §5 / TBL-A §3 |
| `pending_rulings` | — | **deliberately empty** | nothing in this file is an FF-08 cadence: a single burst has no tick train; the bloom's 0.45–0.50 s recurrence is a **kill rate**; the 5.5 s release is a **resource window** | §13.4 B7 · C3 |
| `range_px 480`, `arc` (27.5°, apex 62), `cast_time_s 0.87`, `can_hit_body_midflight` | — | **unchanged**, apex still flagged UNRESOLVED | §13.7 item 3: the endgame fan clips are **worse** for the apex, not better — five trails, no single one to track | §12.1 row 5a · §12.7 item 4 · §13.7 item 3 |

---

## 3 · `frozen_orb` — v1 was right; v2 adds the collider it was missing

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `mechanics.collision` | **absent** | **capsule, radius 0.25 BH, applied to the child bolts + the 16 nova darts; orb body explicitly has NO actor collider** | **G1 is precisely the grammar R-C5-96 governs** and v1 carried `pierce` but no collider | R-C5-96 |
| `emission.emission_count_per_cast 30` | present, unexplained | **unchanged, derivation shown** (1.20 s × 25 Hz) | every number traces | DERIVED off TBL-B §1 |
| `pending_rulings` | — | **×3 emission cadence keys** | F1 flip in one pass | Charter F1 |
| `provenance.residue` | "no decal observed" | **adds that residue stays formally UNKNOWN at source** while the spec authors none | §12.5 flags its own window is not an exhaustive residue check | §12.5 §1 |
| every sourced number (632 / 759 / 1.20 s / 25 Hz / 2.4 fr / 106.875° / 1138 ×2 / 1.00 s / 0.80 × 0.75 BH / 0.21 s / 16 darts 0.67 × 0.12 BH / 11.68 BH / nova / no decal / cast 1.0 s / pierce −1 + obstacles) | — | **unchanged** | re-checked row by row against §12.5 §1 and TBL-B §1; no discrepancy found | TBL-B §1 · §3 Q1–Q3 · §12.1 rows 1a/1b |

---

## 4 · `lightning_blast` — the two measured look-facts promoted out of prose

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `presentation.polyline` (new block) | the facts lived inside the `bolt` **prose string** | **structured**: `rerandomise_hz 60`, `rerandomise_scope`, `onset`, `fork{kind, rejoins_trunk, filament_count, separate_endpoints}`, `strands_at_caster [2,3]` | `exporter_needs` lists per-frame polyline + fork/rejoin as TOOLING; the exporter cannot be built against a sentence | §12.1 row 2 (re-randomise, MEASURED HIGH) · row 3 (fork+rejoin, 2–3 strands, MED) |
| `…fork.filament_count` | — | **`null` + note** | §12.1 row 3 describes the filaments and **never counts them**. Left null rather than invented | NOT MEASURED — stated |
| `…fork.separate_endpoints` | prose caveat | **`false` + note** | keeps a build from drawing a second strike; gameplay forking is Divergence-only | §6 / TBL-B §4 |
| `mechanics.collision` | absent | **`null` + note** | an instant bolt has no projectile body, so R-C5-96 does not apply. Explicit so nobody reads it as forgotten | R-C5-96 · §12.1 row 2 |
| `pending_rulings` | — | **×3 hop-cadence keys**; `polyline.rerandomise_hz` deliberately **not** marked | the per-frame re-randomisation is **MEASURED SOURCE**, not FF-08 house jitter — an F1(b) "drop FF-08" must not delete it | §12.1 row 2 |
| every sourced number (instant, 505, 12/5 px, 0.15 + 0.07 → 0.22, afterimage 0.07, chain rule 0→2, hop 468 px / 0.10 s, cast 0.682, cooldown 0, requires_target) | — | **unchanged** | re-checked against §12.5 §4 and TBL-B §4 | §12.1 rows 2–3 · TBL-B §4 · §6 |

---

## 5 · `zeus_chain` — v1 was right; v2 adds the collider and names an F1 hazard

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `mechanics.collision` | **absent** | **capsule (R-C5-96) with `ahead_of_socket_gate: false`** + note | a projectile exists, so the capsule applies — but the ahead-of-socket clause is a **forward-cast** rule and this projectile spawns **at the victim** and homes. Disabled explicitly, not silently dropped | R-C5-96 |
| `provenance.ff08` | "pending F4" | **names the skill-specific hazard**: under F1(c) "keep universal", a CV floor here would jitter a **travel time** — i.e. make the ball fly at inconsistent speed. That is a different and worse thing than jittering a tick train | the conductor should see it before ruling | §8 (cadence is physics, VERIFIED BY EXHAUSTION) |
| `presentation…shadow` / `ground_shadow true` | present | **unchanged; also listed in `exporter_needs` as REQUIRED** | §12.1 row 6b: *"THE SHADOW IS DRAWN and is a build requirement"* | §12.1 row 6b |
| `pending_rulings` | — | **×3 hop-cadence keys** | F1 flip in one pass | Charter F1 |
| every sourced number (ball mode, 1408, 488, 582, 4 hops, ×0.8, fuse 0.3, proc 0.167, 0.37 BH, 0.24/0.51 BH, trail 0.07 s, impact 0.47 s, ignores terrain, may re-hit, total 1.27 s, `width_px` removed) | — | **unchanged** | re-checked against §12.5 §5, TBL-A §6 and TBL-B §5; no discrepancy found. The §12.7 item 5 speed non-correction is carried in provenance so nobody re-derives it | TBL-B §5 · §8 · §12.1 rows 6a–6c |

---

## 6 · `healing_hands` — graded, marked, and one conflict surfaced

| Field | v1 | **v2** | Why | Source |
|---|---|---|---|---|
| `mechanics.radius_px` | 220 | **220 unchanged**, + `radius_grade: "AUTHORED"`, + `pending_rulings["mechanics.radius_px"] = "C-7 F3"` | charter F3 (a): *"220 px authored (matches the pre-1.4 dome), marked AUTHORED"* | Charter § 4 F3 · §12.2 (MEASURED dome 3.4–3.6 BH; the 160 px narrowing moved **away** from the footage) |
| **⚑ F3 vs F5 conflict** | not noticed | **surfaced in provenance** | **Charter F3 says 220 px; Q80 F5 recommends "1.5 BH radius (≈ 200 px)".** They differ by 20 px **and by which quantity they name** — 220 px is a *diameter* match at 3.4 BH; 200 px is stated as a *radius* at 1.5 BH = 3.0 BH diameter. **The conductor must reconcile F3 and F5 in ONE ruling, not two.** | Charter § 4 F3 vs Q80 F5 |
| `presentation…seal` | "REMOVED — pending F3" in the string | **`pending_rulings["presentation.primitive_bindings.seal"] = "Q80 F3"`** | two different pendings in one file is exactly why the marks are a path map | Q80 F3 rec. (a) · §12.5 §6 (no glyph in any of 13 frames) |
| Charter §1's "F3 moot" note | — | **contested in provenance**: not fully moot — the painted hexagram asset exists and F3 decides whether it survives in the alphabet for a future aura | Q80 F3's alternatives (b)/(c) are still live choices | Q80 F3 |
| `mechanics.collision` | absent | **`null` + note** | no projectile; explicit | R-C5-96 |
| `pending_rulings` FF-08 | — | **deliberately absent** — `pulse_cv_min` is vestigial on an empty schedule; nothing for F1 to flip | | §7 / TBL-B §6 |
| `look_vintage` PRE-1.4 caveat, dome form, 0.4 s / 0.15 s peak / 1-frame onset, cursor_ground, HoT 3 s, no damage, cast 0.682 | — | **unchanged** | v1 was correct | §12.1 row 7 · §12.5 §6 · §7 |

---

## OPEN FOR THE CONDUCTOR — what I could not source or could not decide

1. **⚑ Healing Hands radius: charter F3 (220 px) vs Q80 F5 (≈200 px, "1.5 BH radius").** Two live recommendations, different numbers, and **different quantities** (diameter-match vs radius). I authored **220** because the charter is later and the task directed it — but this needs **one** ruling covering both forks, not two rulings that disagree.
2. **PConc range: 480 px vs the 520 px touch convention.** Blackwater carries `range_px 520` HOUSE per R-C5-92. PConc's 480 is "CONFIRMED as plausible" at source with the cursor clamp UNKNOWN (§10.7). I left **480** because the task's touch-range instruction was scoped to Blackwater — but if 520 is the lane-wide touch default, PConc (also ground-locked G2) should probably adopt it. **Conductor's call, not a source question.**
3. **⚑ `fire_bolt_e1.json` still names `fire_burst_e0p_v2`** (line 30, `primitive_bindings.impact`), while Blackwater v2 now names **v3** per R-C5-122/124 and the `v3` kit on disk already carries the FL-5 ending (`interleave.count [5,7]`, `core_residue`, `smoke`, tightened `ember_ending`). **The lane's own fire spec is behind its own kit.** Reconcile before P1, or Blackwater and fire will name different vocabularies for the same ending.
4. **PConc fan count: 4 or 5.** §13.1 gives GMP+GV at **avg 4.5 overlaps**, range 4–5. I authored **5** (top of band) and recorded 4 as equally sourced. A HOUSE choice inside a measured band — flip freely.
5. **Profane Bloom trigger: struck vs killed.** R-C5-125 says "struck/killed"; the source trigger is a **cursed enemy's death**; **nothing dies in the dummy scene**, so the build trigger must be *struck*. Recorded in the file. When real kills exist, the trigger should move — that is a future amendment, not a v2 number.
6. **Profane Bloom's damage geometry is unknown.** §13.7 item 4: only the VFX was measured; no game-data explosion radius was sought. 1.6 BH is a **look** number with no hitbox beside it — unlike PConc's burst, which has both.
7. **PConc lob apex (62 px / 27.5°) remains UNRESOLVED** across three passes (§12.7 item 4, §13.7 item 3). Footage probably cannot settle it; a build-mode paused frame could.
8. **Lightning Blast filament count** is `null` — §12.1 row 3 never counted them. The exporter must pick, and whatever it picks is HOUSE.
9. **Blackwater glass shards** remain HOUSE and STILL UNKNOWN (§12.7 item 1). The only route left is the `.pfx` inside the packed `.arc` — crawler-shaped work, not in this run.
10. **Healing Hands is pre-1.4 art throughout** (§9-B item 8, §12.7 item 3). If E3 is chasing *current* Last Epoch, the whole file is the wrong target. Carried in the file's `provenance.open`, unburied.
11. **`pending_rulings` is a new key shape** I chose (path → ruling id) because scalar keys cannot each carry an inline marker unambiguously — healing_hands needs two different pendings in one file. If the conductor wants inline markers instead, the map converts mechanically.
12. **`residue: null` and `collision: null`** will fail any exact-set `_keys` validator that does not admit them. Listed in each file's `exporter_needs`, but flagged here because a null is easy to read as "not authored yet" rather than "authored as absent".
