# VDM-1 basin-2 mapping batch-03 — summary (12 kits, all Grim Dawn)

**Author:** gandalf-seam mapping author · **Date:** 2026-07-18 · **Files:** `mapping-batch-03.jsonl` · `mint-candidates-batch-03.jsonl` (3) · `docket-candidates-batch-03.jsonl` (3)

## Grade histogram (advisory — steward recounts from committed files, D-2c)

| Grade | Count | Kits |
|---|---|---|
| EXACT | 5 | phantasmal-blades-witch-hunter · ravenous-earth-oppressor · righteous-fervor-dervish · savagery-warder · stun-jacks |
| CLOSE | 3 | primal-strike-vindicator · roh-infiltrator · shadow-strike-infiltrator |
| APPROX | 1 | stormbox-elementalist |
| GAPPED | 3 | reap-spirit · retaliation-warlord · skeleton-ritualist |

Terminal: 9 MAPPED · 3 MAPPED_DOCKET (R-M7 biconditional held — the APPROX kit with mint-candidates stays MAPPED).

## Per-kit one-liners

- **gd-phantasmal-blades-witch-hunter** — EXACT. multi_projectile fan spam, shadow/earth (vitality primary; era-anchored acid form via Venomlance → ELEMENT_CONVERSION_MONO).
- **gd-primal-strike-vindicator** — CLOSE. §A replacer-native melee_strike with AoE rider; Wind Devil → totem + curse:sap with wander drift (mint filed). Era restamped (base-2016 CONTRADICTED); Storm Totem unfetched → omitted.
- **gd-ravenous-earth-oppressor** — EXACT. ground_targeted_circle decay patches, shadow + drain (§2 'decay' row — judgment flagged for audit) + mastery RR aura → curse:sap.
- **gd-reap-spirit** — GAPPED/DOCKET. Pet-CORE recast-spirits loop (§A pet row); negative_canon ATTESTED (dual-scale split) recorded as context; count-shape → placed-proxy-count accrual.
- **gd-retaliation-warlord** — GAPPED/DOCKET. §A retaliation-substrate evidence kit; loop-verb IS stand-and-tank-return — no delivery token, aura-pulse NOT stretched; TH reflect + on-damage-taken trigger + EoR whirlwind map as riders only.
- **gd-righteous-fervor-dervish** — EXACT. §A replacer-row verbatim kit: melee_strike acid (earth), WPS riders via on-hit-threshold trigger, fervor accumulator, Night's Chill → curse:sap (no chill — name only).
- **gd-roh-infiltrator** — CLOSE. Cold rune trap → ground_targeted_circle (water); proximity-arming drift (mint filed); WoR self_buff. No freeze/chill — nothing fetched.
- **gd-savagery-warder** — EXACT. Replacer melee_strike + charge accumulator + native Wendigo totem; single-tier ramp (deliberately NOT a two-tier-accumulator filing); bleed withheld as variant-scoped.
- **gd-shadow-strike-infiltrator** — CLOSE. Fused move+nuke → teleport with strike-on-arrival noted (not asserted native, arc-b01); Morgoneth lightning→cold → ELEMENT_CONVERSION_MONO. Era restamped.
- **gd-skeleton-ritualist** — GAPPED/DOCKET. Pet-CORE army (~90% damage via autonomous combatants); Wendigo Totem alone native; maintenance-reservation own candidate; army-count → placed-proxy-count accrual; chain_count 3.
- **gd-stormbox-elementalist** — APPROX. Enemy-attached tether beacon → chain + mandatory deviation note (persistent attachment lost); identity WATCH irrelevant to mapping; electrocute = no token.
- **gd-stun-jacks** — EXACT. §0.3 poster child: 180° multi_projectile lightning spam, energy-hungry; NO stun token (name only); negative_canon UNSUPPORTED → excluded from mapping input.

## T4-door frequency

ELEMENT_CONVERSION_MONO 5 · ZONE_CONTROL 2 · PROXY_ASCENSION 2 · MOMENTUM_CASCADE 2 · PERSISTENCE_ENGINE_saturation 1 · PERSISTENCE_ENGINE_uptime 1 · RETRIBUTION_ENGINE 1 · DEFENSIVE_TRADEOFF 1 · PROXY_SOVEREIGNTY 1 · TEMPORAL_CHARGE 1 · RESONANCE_LOOP 1 · GEOMETRY_COLLAPSE 1

## Candidates

**Docket (3):** retaliation-substrate (4th stat-as-damage mechanism; own row per §A, not merged with armour cluster) · autonomous-pet-core (2 evidence kits, summoner-deferral) · maintenance-reservation (own class per steward — not merged with basin-1 reservation-as-damage-scaler).

**Mint, all qualitative (3):** wandering-mobile-emitter (Wind Devil, R-M8) · enemy-attached-persistent-emitter (Storm Box) · proximity-armed-trigger (Rune of Hagarrad).

**Family accruals (steward-owned, NO numbers):** placed-proxy-count ← skeleton-ritualist army-count shape; reap-spirit recast-count shape. No two-tier-accumulator filing this batch (Savagery is single-tier).

## §0 near-misses (statuses WANTED but not attestable, per kit)

- **phantasmal-blades:** poison ('acid/poison' only as damage-type/build-title language — no DoT-status behavior fetched); drain ('life-drinking' is extractor compression, no named status).
- **primal-strike:** none.
- **ravenous-earth:** none withheld — but the EMITTED drain is a §2-row judgment call ('decay'/'rot' named); flagged for steward audit.
- **reap-spirit:** none.
- **retaliation-warlord:** none.
- **righteous-fervor:** chill (skill NAME 'Night's Chill'; fetched behavior is RR → curse:sap emitted instead); poison (acid = damage type only).
- **roh-infiltrator:** freeze/chill ('cold shards' is element flavor; prior knowledge of the skill's CC is the memory-supplement leak class — not used).
- **savagery-warder:** bleed (ATTESTED but variant-scoped: 'lightning/bleeding build', 'Bull/Bear for physical/bleed' — withheld from the mapped lightning primary loop, noted in fidelity).
- **shadow-strike:** chill/freeze (cold flavor only).
- **skeleton-ritualist:** curse:sap/sunder (Manticore/Rattosh '-53% vitality resistance' attested but application SHAPE unfetched → cannot pick the §2 branch). bleed EMITTED — pet-inflicted, 'Rend on skeletons for bleeding' named.
- **stormbox:** shock (electrocute = GD lightning-DoT; engine shock requires CC); curse/sunder RR (Thermite Mines 'for RR' — shape unfetched).
- **stun-jacks:** stun (name only, §0.3); shock (electrocute, as above).

## What felt forced / for the steward

1. **totem as nearest-token on GAPPED pet skills** (reap-spirit, skeleton army, Primal Spirit): rows say explicitly it is NOT a fit claim, but the 26-enum forces SOME geometry_value; a null-geometry convention for gapped skills would be cleaner.
2. **drain on ravenous-earth**: deterministic per §2 ('decay' listed verbatim) yet the fetched language describes zone damage, not a named enemy status — the emit-vs-withhold line is thinner than the row implies. Audit welcome.
3. **RR application-shape test** (§2 curse-vs-sunder branch) repeatedly hinges on one word ('aura', 'presence'); two kits withheld for shape-silence (skeleton-ritualist, stormbox) while three emitted on clear aura/entity anchors — consistent, but the branch is doing heavy lifting this basin (GD RR is ubiquitous).

## 3 hardest kits

1. **gd-retaliation-warlord** — the identity lives entirely in a stat substrate with no delivery token; the work was resisting the aura-pulse stretch while still letting TH economy + EoR/Counter Strike riders carry what honestly maps.
2. **gd-skeleton-ritualist** — one kit spanning native (Wendigo Totem), gapped (autonomous army), and two candidate classes (maintenance-reservation, count-accrual) without letting the native fragment soften the R-M7 verdict.
3. **gd-stormbox-elementalist** — enemy-attached persistent tether has no geometry home; deciding chain-APPROX ("that build, worse") over GAPPED under the player test, with the mandatory deviation note carrying the loss.
