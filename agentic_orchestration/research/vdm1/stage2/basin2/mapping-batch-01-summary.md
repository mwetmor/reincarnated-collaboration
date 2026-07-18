# VDM-1 basin-2 mapping batch-01 summary (m01, gd 1–12, all Grim Dawn)

**Author:** gandalf (mapping author) · **Date:** 2026-07-18 · **Gate:** ingest-11 (b01 window). Advisory histogram — steward recounts from committed files (D-2c).

## Grade histogram (12 kits)
- EXACT 1 · CLOSE 8 · APPROX 1 · GAPPED 2
- terminal: MAPPED 10 · MAPPED_DOCKET 2 (R-M7 biconditional: both GAPPED)

## T4-door frequency
PERSISTENCE_ENGINE_saturation ×3 · GEOMETRY_COLLAPSE ×2 · PERSISTENCE_ENGINE_uptime ×1 · GEOMETRY_PROPAGATION_overkill ×1 · ELEMENT_CONVERSION_PHYSICAL ×1 · ZONE_CONTROL ×1 · PROXY_FISSION ×1 · MOMENTUM_CASCADE ×1

## Ailments EMITTED (all named-in-fetched)
bleed ×2 (blade-arc: "scaling bleed damage"; canister: "internal trauma" via §A row) · burn ×1 (callidors: "fire and burn modifiers emphasized") · blind ×1 (bwc: "fumble transmuters", §A fumble row, sentence-adjacent) · root ×1 (blade-trap: "immobilizes")

## Per-kit one-liners
1. **aar-spellbinder** CLOSE — beam_channel; aether→lightning (energy-ray §1); era errata (AoM not base). No ailment.
2. **aegis-paladin** CLOSE — ricochet_bounce; fire; RETURN leg → out-and-return accrual. No ailment.
3. **belgothian-blademaster** CLOSE — §A replacer+WPS: Cadence-default NATIVE melee_strike, WPS→trigger riders (on-hit burst); pierce=element-neutral; ELEMENT_CONVERSION_PHYSICAL.
4. **berserker-wereforms** GAPPED/DOCKET — ×6 abstained; FoA UNSHIPPED; nothing legal to map; row = the gap (BACKFILL-2).
5. **blade-arc-warder** EXACT — melee_arc + bleed (named); phys-DoT; PERSISTENCE_saturation.
6. **blade-trap** APPROX — negative ATTESTED (corpus flag, not grade driver); single_target (cast-ON-enemy, NOT ground) + root; era restamped base-2016;aom-2017.
7. **blight-fiend-ritualist** GAPPED/DOCKET — pet-CORE summoner-deferral; null pet-geometry + ring death-burst; pet-death-payload own docket; shadow (necro acid).
8. **bloody-pox-conjurer** CLOSE — single_target+contagion note (m02 dee precedent); shadow (vitality); Wendigo totem; CoF RR + vitality-DoT status both WITHHELD.
9. **bwc-demolitionist** CLOSE — ground_targeted_circle + blind (fumble, §A, adjacent); burn WITHHELD (theme-adjective); Thermite RR withheld.
10. **cadence-witchblade** CLOSE — melee_strike; every-3rd-swing → two-tier-accumulator accrual (#3, same as krieg-m02); Blitz dash_attack; CoF RR withheld.
11. **callidors-tempest-templar** CLOSE — ring point-blank pulse + burn (named); fire-primary/lightning-secondary (aether); era errata (FG-only, Oathkeeper).
12. **canister-saboteur** CLOSE — multi_projectile + bleed (internal trauma §A); Flashbang stun+blind WITHHELD (probe/claim-only); fire.

## §0 near-misses — statuses/tokens WANTED but could not attest (per kit)
- **aar** — wanted `shock` from aether/energy ray; NOT named (theme≠status, §0.1). Withheld.
- **aegis** — wanted `burn` from fire shield; NOT named. Withheld. (out-and-return return-leg is a geometry near-miss, filed as accrual not a status.)
- **belgothian** — none status-wise; each WPS proc's individual payload unfetched (§0.4) → no per-WPS skill rows (not a status withhold, a granularity limit).
- **berserker** — everything (×6 abstain); no near-miss possible, the whole kit is the gap.
- **blade-arc** — none (bleed cleanly named).
- **blade-trap** — `root` emitted via "immobilizes" (extraction); no other status. (The blade-proc-in-radius payload is a geometry near-miss, not a status.)
- **blight-fiend** — wanted `poison` from acid theme; acid is DAMAGE-typed (Ghol conversion), no "poison" status named → withheld (§0.1).
- **bloody-pox** — (1) wanted a vitality-decay DoT status (`drain`/`poison`/`bleed`) — plague is a DoT but NO registry status named → withheld; (2) `curse:sap` from Curse of Frailty RR — application shape unanchored (shape-silent) → withheld per §2 RR-branch reminder.
- **bwc** — (1) `burn` — "burning tar carpet"+"ground DoT" is theme-adjective, "Burn" not named as status → withheld (conservative, §0.1); (2) Thermite Mine `curse:sap`/`sunder` RR — shape-silent → withheld. `blind` (fumble) EMITTED (adjacency satisfied).
- **cadence** — `curse:sap` from Curse of Frailty RR — shape-silent → withheld (consistent w/ bloody-pox).
- **callidors** — none status-wise (`burn` named + emitted). Dropped a non-canonical element-ternary key in cleanup (aether/fire composite compressed to primary+secondary).
- **canister** — (1) Flashbang `stun` — present ONLY in verify_ledger claim-paraphrase + probe (both inadmissible, §0.2) → withheld; (2) Flashbang `blind` — name-collision, fetched anchor says only "debuff" (§0.4) → withheld; (3) Thermite RR token → withheld (shape-silent). `bleed` (internal trauma) EMITTED (§A row).

## Candidates
- **mint-candidates-batch-01.jsonl** (1): two-tier-accumulator family accrual — Cadence every-3rd-swing (gd-cadence-witchblade); **#3 attestation** (WATCH-ITEM fired at 2); same-mechanism as krieg-m02's krieg-death-knight filing. Filed WITHOUT numbers (steward-owned). Kit graded un-minted (CLOSE/MAPPED).
- **docket-candidates-batch-01.jsonl** (2): (a) unshipped-source-content gap — berserker-wereforms (BACKFILL-2, NOT engine gap); (b) pet-death-payload (corpse-as-payload) — blight-fiend, distinct attested shape per §A pet-row trap note, first basin-2 attestation.

## Anything that felt forced / judgment flags (LOUD)
- **blade-trap geometry** — `single_target` chosen over totem/ground_targeted BECAUSE fetched explicitly says "cast directly on enemies rather than placed on ground." The trap-that-procs-blades-in-radius is a genuine composite the base geometry only partly holds → APPROX honestly. ZONE_CONTROL T4 is a weak fit.
- **blight-fiend element** — shadow (necro-corruption) vs earth (acid-venom) is a real §1 split; Blight Fiend is a Necromancer summon dealing Ghol-converted acid → shadow chosen, earth noted as the live alternative. Flag for steward.
- **bwc `burn` withhold** — the most debatable withhold in the batch: a fire ground-DoT mechanically IS a burn, but "Burn" is not the named status (only "burning tar"/"ground DoT"). Held conservative to the run's m04 strictness; steward may overturn if fire-ground-DoT is ruled burn-attesting.
- **canister element** — fetched core-skill language emphasizes pierce+internal-trauma (physical); fire kept as base-identity slot (elem_raw/Demolitionist family) with bleed carrying the phys ailment. Element-neutral was the alternative.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18 — D-2c recount from committed files)

**Recount: 12 rows · 1 EXACT / 8 CLOSE / 1 APPROX / 2 GAPPED · 10 MAPPED / 2 MAPPED_DOCKET — advisory EXACT.** R-M7 clean. Re-fire executed the incremental-emission discipline (31 tool-uses, ~half the dead run's wall-time) — the overflow mitigation is validated.

**ADJUDICATION 1 — verify-anchor admissibility (template §0.2 amended):** `verify_ledger.anchor_quote` verbatim is **LEGAL attestation grounds** — fetched-class, steward-audited at crawl, errata-governed. `verify_ledger.claim_text` remains **INADMISSIBLE** (the kb-derived claim under test — same class as probe facts). This ratifies the mapper's own implicit split: canister's Flashbang stun was withheld as "claim-paraphrase, inadmissible" while canister's `bleed` rode the mechanics ANCHOR "non transmutable internal trauma" (named, → §A trauma row) — that model is now explicit law.

**LEAK — bwc `blind` probe-cited (first §0.2 leak of the basin-2 mapping wave), STRUCK + RE-GROUNDED, emission survives:** the cited "fumble transmuters" line lives in `canon_probe_facts.facts_json` (mirrored in `mech_note`) — kb-derived, INADMISSIBLE; the claimed "sentence-adjacency satisfied" was computed on illegal text. Legal ground EXISTS: verify_ledger identity anchor "BWC provide[s] a significant OA reduction to enemies" — OA-reduction is GD's accuracy-tax substrate, within the m02-widened blind register. Row corrected in-place with audit stamp; grade CLOSE unchanged. **Root cause named: STORE-NOT-STYLE trap** — probe prose reads like guide verbatim; admissibility is decided by store, not styling (template §0.2 now carries the warning). Leak-class tally, basin-2 mapping wave: 1 caught / 36 kits (vs basin-1's 22/48).

**Ailment audit (5 emissions, all verified to legal stores):** blade-arc `bleed` — "applying bleed DoT; bleed continues ticking" (dossier, decisive) · canister `bleed` — mechanics anchor via Adjudication 1 + §A trauma row · blade-trap `root` — "trap immobilizes" (dossier; boss-immune honestly noted) · callidors `burn` — "fire-and-burn focus" word-present (contrast m02 fire-strike's flavor-only withhold — the line holds) · bwc `blind` — re-grounded above. **Withhold discipline strong:** RR shape-silent ×4 (bloody-pox, cadence, bwc Thermite, canister Thermite — §2 branch reminder applied consistently) · aar shock theme≠status · blight-fiend acid-as-damage-type · bwc burn zone-description.

**Structural rulings:** (a) **berserker empty-projection convention RATIFIED** — all-six-family abstention maps as the honest empty shell (skills=[], doors=[], motion UNMAPPABLE) + GAPPED/DOCKET + BACKFILL-2 docket; zero doors is LEGAL on zero-evidence kits (R-M1's 1–3 is the floor for evidenced kits); never invent from folk-name. (b) aegis `ricochet_bounce` over chain upheld — "bounces on monsters / ricochets to multiple nearby enemies" in both stores; **out-and-return accrual FILING MISS caught** — named in fidelity + near-miss but absent from the mint file; steward records it directly: **out-and-return family +1 (aegis return-leg, first GD attestation)**. (c) blade-trap composite APPROX honest (cast-ON-enemy trap ≠ ground trap; single_target+root partial hold; negative ATTESTED context carried; era restamp honored).

**Counts (steward-owned):** two-tier-accumulator — **mechanism #3 (Cadence) now at its eponymous source kit** (cadence-witchblade) + krieg-m02 same-mechanism evidence; count stays 3 mechanisms. out-and-return +1 (aegis). placed-proxy-count unchanged this batch. Dockets: berserker BACKFILL-2 + blight-fiend pet-death-payload (first basin-2 attestation of the b01-anticipated shape — §A pet-row trap note discharged).

**Verdict: ACCEPTED (with one leak struck + re-grounded, one filing miss steward-recorded).**

**W1 CLOSE (36/36 kits, all-GD):** post-audit histogram **8 EXACT / 20 CLOSE / 2 APPROX / 6 GAPPED** · 30 MAPPED / 6 MAPPED_DOCKET · leak-class strikes: 1 (re-grounded, survived) · steward additions: 1 (forcewave bleed) · regrades: 1 (APPROX→CLOSE) · §A rows added at audits: 2 · conventions minted: gapped-pet two-lane geometry · empty-projection · store-not-style · adjacency micro-ruling.
