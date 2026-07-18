# VDM-1 basin-1 mapping batch-03 — summary (12 poe2 kits, spec lines 25-36)

**Author:** gandalf (SPEC-AUTHOR, mapping-author seam) · **Date:** 2026-07-18 · **Provenance:** authored-vdm1 · Dossiers ingested (ingest-8/9), all fetched-language sourced.

## Grade histogram
| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 8 | snipe-mirage-deadeye, spark-stormweaver, spiral-volley, supporting-fire, tempest-bell, tempest-flurry, titan-hotg, warbringer-totems |
| APPROX | 4 | temporalis-blink, twister, walking-calamity, wall-of-shields |
| GAPPED | 0 | — |
**Terminal:** 12 MAPPED / 0 MAPPED_DOCKET. All 4 APPROX carry mandatory deviation_notes (what the source player would miss).

## Per-kit one-liners
- **snipe-mirage-deadeye** (CLOSE): Ice Shot `multi_projectile` (9-shard fanout, freeze/chill applicator) + Snipe `single_target` channeled burst-on-frozen + Mirage Deadeye `self_buff` R-M9 clone-echo. GEOMETRY_COLLAPSE + PROXY_ASCENSION. chain=3.
- **spark-stormweaver** (CLOSE): Spark `multi_projectile` bouncing flood (poe1-spark precedent). **shock→sunder (S-A BINDING: no paralysis attestation)**. Archmage unreserved-mana→damage = RESOURCE_CONVERSION + reservation 0.0 anti-reservation note.
- **spiral-volley** (CLOSE): 29-arrow 360° `ring` (fetched supersedes stale multi-point kb) + 6× chain rider; physical→element-neutral. Endurance→Frenzy charge-conversion cycle → TEMPORAL_CHARGE.
- **supporting-fire** (CLOSE): commanded arrow-rain `ground_targeted_circle` (14m). **Spirit-reservation FALSE FRIEND flagged** (reservation_resource=spirit, NOT spirit-guide). ZONE_CONTROL + PROXY_SOVEREIGNTY.
- **tempest-bell** (CLOSE): Tempest Bell `totem` (placed struck-to-pulse proxy) + Tempest Flurry `melee_arc`. shock→sunder. Combo-Point accumulator. PROXY_ASCENSION + TEMPORAL_CHARGE. chain=3.
- **tempest-flurry** (CLOSE): Tempest Flurry `melee_arc` (**HOT-FLAG 7: gemling-stacker precedent — same skill name; melee_strike alt noted, that's Ice Strike's**) + Charged Staff `self_buff`. shock→sunder. TEMPORAL_CHARGE + MOMENTUM_CASCADE.
- **temporalis-blink** (APPROX): Blink `blink` (**HOT-FLAG 4: mobalytics cite used normally; blink vs teleport — chose blink/utility per 'repositioning, minimal AoE'**). Temporalis all-cooldown-collapse = economy note; the ~10x/s engine degrades to fast-blink. element-neutral.
- **titan-hotg** (CLOSE): HotG `ground_slam` (**HOT-FLAG 8: phrase-book slam member; falling-hammer IS a slam, not projectile-rain**) + Armour Breaker `melee_arc`/sunder. stun prerequisite kept. GEOMETRY_COLLAPSE + SACRIFICE_ASCENDANCY. chain=3.
- **twister** (APPROX): Twister `multi_projectile` (roaming vortices, R-M8 wander delta) + blind + Whirling Slash `whirlwind` empower-zone. Spirit false-friend. **Qualitative mint-candidate: roaming-persistent-AoE.**
- **walking-calamity** (APPROX): **HOT-FLAG 1 — ERRATA-19 corrected identity mapped** (Walking Calamity Shaman; [Walking Calamity, Herald of Ice, Polcirkeln]; pre-errata autobomber CONTRADICTED). Active-cast meteor field `ground_targeted_circle` (fire/burn, phys→fire) + Herald of Ice `ring`. GEOMETRY_PROPAGATION + MOMENTUM_CASCADE. chain=3.
- **wall-of-shields** (APPROX): **HOT-FLAG 3 — negative=true, mapped HONESTLY.** Shield Wall `placed_lane` (inert fissure segments, consume-mark detonation) + warcry `self_buff` detonators. Armour-value-as-damage → docket-candidate. Trap-status in corpus, not mapping_json.
- **warbringer-totems** (CLOSE): **HOT-FLAG 2 — ERRATA-20 era restamp to 0.2-dawn.** Ancestral Warrior `totem` (Sunder payload→sunder; up-to-10, 3-Endurance-Charge-fueled) + Shockwave `totem`/stun. PROXY_SOVEREIGNTY + PROXY_FISSION.

## T4-door frequency
GEOMETRY_PROPAGATION ×4 · TEMPORAL_CHARGE ×4 · GEOMETRY_COLLAPSE ×3 · ZONE_CONTROL ×3 · PROXY_ASCENSION ×2 · PROXY_SOVEREIGNTY ×2 · MOMENTUM_CASCADE ×2 · RESOURCE_CONVERSION ×1 · PHASE_MOMENTUM ×1 · SACRIFICE_ASCENDANCY ×1 · PROXY_FISSION ×1. All engine-native (R-M1 clean).

## Ailment / geometry distribution
Ailments: sunder ×5 (all shock-amp / armour-break — zero engine `shock` emitted, zero `ignite`) · freeze ×2 · stun ×2 · chill ×1 · blind ×1 · burn ×1. Geometries: multi_projectile ×3 · self_buff ×3 · melee_arc ×3 · totem ×3 · ring ×2 · ground_targeted_circle ×2 · single_target / blink / ground_slam / whirlwind / placed_lane ×1.

## Candidates filed (side-files; NOT in mapping_json)
**docket-candidates-batch-03.jsonl (2):**
1. **armour-value-as-damage-source** (wall-of-shields) — defensive-stat-as-offensive-multiplier; DISTINCT from tq2 armor-CONVERSION (addendum E) and docket #4 stun-as-damage. Steward: three adjacent stat→damage mechanisms now attested.
2. **enemy-density-reactive cadence** (walking-calamity) — meteor frequency ramps ≤200% by nearby enemy count; no key couples enemy-count→proc-rate.

**mint-candidates-batch-03.jsonl (1, qualitative):**
1. **roaming-persistent-AoE** (twister) — self-propelled wandering persistent damage field; no 26-geometry member fits. Ladder step-4 qualitative; single-kit exposure → likely NOT yet a mint, recorded for accrual.

## Family accruals (STEWARD-OWNED — filed WITHOUT numbers)
- **walking-calamity → shaman-bear Rage→Glory two-tier-accumulator family.** Same shaman/Druid Rage→Glory→Walking-Calamity family as b02 poe2-shaman-bear, but plausibly a DISTINCT kit: this is the meteor-autobomber built AROUND Walking Calamity as the active-cast headline (fire meteors + Herald of Ice/Polcirkeln propagation, no in-form Bear slams as identity); shaman-bear is a Bear-Form slam bruiser where Walking Calamity is the passive tail-payoff. Two-tier Rage→Glory mapped per addendum B: ONE accumulator + threshold-proc + fidelity_note the Glory second tier. **This is the 2nd+ two-tier-accumulator instance in basin-1 → steward's qualitative-mint counter (Section-B WATCH-ITEM).**
- **warbringer-totems → placed-proxy-count family** (hiero-6-totem / tq2 forge-turrets count-8 mint class). Up-to-10 simultaneous totems = placed-proxy-count extremum. Steward-counted.

## GX-02 / watch-item / false-friend flags fired
- **Spirit-reservation FALSE FRIEND** (addendum B): supporting-fire + twister both use poe2 Spirit as a reservation/combat resource — reservation_resource=spirit, explicitly NOT routed to spirit-guide. Fired ×2.
- **Section-B two-tier-accumulator WATCH-ITEM**: walking-calamity (Rage→Glory) — 2nd+ basin-1 instance; steward's mint counter.
- **GX corpus flags surfaced** (fidelity_notes, not numbered): GX-11 (snipe, supporting-fire), GX-07 (spark, tempest-flurry, + gemling precedent), GX-03 (tempest-bell, tempest-flurry, titan), GX-09 (spiral-volley, twister), GX-01/GX-17 (temporalis, walking-calamity), GX-01/GX-04 (warbringer), GX-18-proposed (wall-of-shields). No GX-02 form-swap in this batch (walking-calamity is active-cast Glory-payoff, no in-form entry as identity — contrast b02 shaman-bear which DID fire GX-02).
- **ERRATA respected**: ERRATA-19 (walking-calamity corrected identity), ERRATA-20 (warbringer era→0.2-dawn), REVIEW-3 (temporalis mobalytics cite valid).

## What felt forced (honesty note)
- **twister geometry** was the hardest call: a self-propelled wandering vortex has no clean 26-member. multi_projectile (poe1-spark/blade-vortex discrete-projectile lineage) + R-M8 wander note is the least-bad approximation, but the erratic-roaming IS much of the kit's felt identity → APPROX + qualitative candidate. Not confident this survives steward audit as multi_projectile vs a 27th-geometry question.
- **titan-hotg**: `ground_slam` vs `ground_targeted_circle` was genuinely close — "falls from sky onto targeted zone" reads projectile-ish, but the phrase-book 'slam→ground_slam' + the overhead-SLAM mechanism won (checked before defaulting per HOT-FLAG 8). Noted the targeted-zone delivery.
- **supporting-fire**: minion-mediated delivery mapped to a player-cast `ground_targeted_circle` + PROXY_SOVEREIGNTY door rather than an autonomous minion loop — the dominant-loop rule (player designates the zone every few seconds) governed over the proxy texture. Defensible but the squad-tactics fantasy is thinner than a true commanded-proxy render.

---

## STEWARD AUDIT ADDENDUM (gandalf, DRIFT-CRITIC — 2026-07-18)

**Verdict: ACCEPTED w/ corrections (applied in-place).** Recount matched the return exactly (0E/8C/4A/0G · 12 MAPPED — R-M7 biconditional clean, first batch of the basin to get it right unaudited). Enum sweeps: geometry/elements/T4 all valid; zero engine-`shock`; zero `ignite`; all 5 shock-amp/armour-break routings → `sunder` correct under §A BINDING.

**Corrections — §0 ailment leak (5 tokens stripped across 3 kits).** snipe-mirage `chill` (bundled cold-flavor; only freeze named) · walking-calamity `burn` ("fire meteors" element-flavor; fetched = fire DAMAGE conversion, no status) + `freeze` (fetched attests "propagates KILLS across packs" — the "freeze-shatter" reasoning was poe1 priors) · warbringer `sunder` + `stun` — **NEW LEAK CLASS: skill-name collision + memory-supplement.** "Ancestral Warrior Sunder Totems" names the poe2 SKILL Sunder; the mapper supplied "Sunder is an armour-break skill" from priors. A skill NAME is never status attestation (§A note added). Post-edit surviving ailments (7) all fetched-grounded: freeze · sunder×4 · stun · blind (twister blind is genuinely attested — good catch by the mapper).

**Steward counts (owned here):** walking-calamity ruled a DISTINCT kit from b02 shaman-bear (active-cast meteor headline w/ Herald-of-Ice/Polcirkeln propagation vs Bear-Form slam bruiser w/ WC tail-payoff) → **two-tier-accumulator family = 2 distinct attesting kits → §B WATCH-ITEM FIRES: qualitative mint-candidate question OPENS for THE REVIEW BOOK** (no mint now). One soft count-claim ("2nd+ instance") softened in fidelity prose — counting is steward-owned.

**Upheld:** ERRATA-19 corrected identity mapped exactly (pre-errata autobomber identity correctly NOT mapped) · ERRATA-20 warbringer 0.2 era · wall-of-shields negative-honest APPROX w/ trap-status kept in corpus (grade reflects honest mapping, non-viability is a corpus fact — exemplary framing) · temporalis-blink `blink` choice + REVIEW-3 evidence use · tempest-flurry melee_arc via gemling precedent · titan ground_slam via phrase-book · twister APPROX + roaming-persistent-AoE qual mint-candidate (survives audit — legitimate 27th-geometry question for the review book) · docket ×2 well-formed: wall-of-shields armour-value-as-damage with an exemplary three-way distinction (vs tq2 armor-CONVERSION vs docket #4 stun-substrate — steward will consolidate the stat-as-damage-substrate cluster at review book) + walking-calamity density-reactive-cadence (new class, watch for accruals). **Note:** GX-01/GX-17/GX-18-proposed corpus-flag echoes accrue to the basin close-out register check.

**Post-correction file truth: 0E / 8C / 4A / 0G · 12 MAPPED · ailments {freeze, sunder×4, stun, blind} all attested.**
