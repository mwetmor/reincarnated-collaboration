# VDM-1 basin-2 mapping batch-02 — summary (12 kits, all Grim Dawn)

**Author:** gandalf-seam mapping author · **Date:** 2026-07-18 · **Kits:** basin-2 lines 13–24 · **Law:** main crosswalks + basin-2 addendum (§A populated) + R-M1..R-M9 · **Histogram is ADVISORY (D-2c); steward recounts from committed files.**

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | gd-drain-essence-spellbinder · gd-flames-of-ignaffar-purifier |
| CLOSE | 7 | gd-dee-witch-hunter · gd-devastation-sorcerer · gd-doom-bolt-sentinel · gd-fire-strike-purifier · gd-krieg-death-knight · gd-mortar-purifier · gd-panettis-mage-hunter |
| APPROX | 2 | gd-eor-warlord · gd-forcewave-warlord |
| GAPPED | 1 | gd-pet-conjurer (terminal MAPPED_DOCKET — the only one, R-M7 biconditional) |

## Per-kit one-liners

- **gd-dee-witch-hunter** (CLOSE) — acid eye-bolts → poison pools (ground_targeted_circle, earth, poison) + Bloody Pox spread; fumble/confusion withheld (no rows — see steward questions).
- **gd-devastation-sorcerer** (CLOSE) — name-collision trap honored: mapped ONLY fetched meteor-rain (ground_targeted_circle, 8s zone, hard-cooldown big button); lightning/fire from the aether-energy read; BWC RR → curse:sap; radius-shrink items → GEOMETRY_COLLAPSE.
- **gd-doom-bolt-sentinel** (CLOSE) — fire-converted sky-bolt single_target nuke on hard cooldown; CoF RR → curse:sap; R-M5 applied to the every-20s CDR pulse (resource-fill + greppable token).
- **gd-drain-essence-spellbinder** (EXACT) — beam_channel + behavior-attested drain (built-in leech) + gear chain-hop + tick-cost; both vitality/aether registers land shadow.
- **gd-eor-warlord** (APPROX) — §A row-1 evidence kit: whirlwind spin + Judgment proc-vehicle rider (on-cast-linked) with consequence lawfully NULL (Maul payload unfetched → contributes nothing); physical rule + ELEMENT_CONVERSION_PHYSICAL.
- **gd-fire-strike-purifier** (CLOSE) — §A row-4 replacer + WPS riders; ERRATA-35 economy (energy/attack-replacer) mapped; explosive-line → line; NO burn (never named).
- **gd-flames-of-ignaffar-purifier** (EXACT) — cone + ramp_per_s + tick-cost + verbatim burn ("50% of FoI damage is burn"); cleanest kit in the batch.
- **gd-forcewave-warlord** (APPROX) — physical-rule lane wave (line, Tremor spam, casting-speed cadence); Internal Trauma NAMED but row-less → withheld + steward-filed; era restamp honored.
- **gd-krieg-death-knight** (CLOSE) — Cadence every-3rd-hit → cycle + on-hit-threshold/burst; two-tier-accumulator accrual FILED; Krieg's Wrath name-only → nothing; aether→shadow; chain stays 2.
- **gd-mortar-purifier** (CLOSE) — placed autonomous emitter → native totem; placement+count attested → placed-proxy-count accrual FILED; "the kill box" → ZONE_CONTROL; era restamp honored.
- **gd-panettis-mage-hunter** (CLOSE) — ERRATA-36 governs: tri-elemental fork replication; kb shock STRIPPED (rode the wrong mono-lightning read); tri→2-slot compression (cold dropped, flagged).
- **gd-pet-conjurer** (GAPPED → MAPPED_DOCKET) — pet-CORE per §A row 3: "pets fight autonomously" is the loop-verb → not that build; pet-stat lane ≠ player-stat lane honored (zero player-scaling tokens); docket-candidate filed.

## T4-door frequency (17 doors / 12 kits)

ELEMENT_CONVERSION_MONO ×4 · ZONE_CONTROL ×3 · PERSISTENCE_ENGINE_uptime ×3 · PERSISTENCE_ENGINE_saturation ×1 · GEOMETRY_COLLAPSE ×1 · ELEMENT_CONVERSION_PHYSICAL ×1 · ELEMENT_CONVERSION_HYBRID ×1 · TEMPORAL_CHARGE ×1 · PROXY_ASCENSION ×1 · DUAL_PROXY ×1. (Conversion doors on 7/12 kits — GD's item-conversion chassis is the basin signature so far.)

## Candidates filed

- `docket-candidates-batch-02.jsonl` — 1 row: autonomous-combatant pet core (summoner-deferral), evidence gd-pet-conjurer, destination mechanic_gap_docket.
- `mint-candidates-batch-02.jsonl` — 2 rows, both FAMILY ACCRUALS (no numbers, §C.2): two-tier-accumulator (gd-krieg-death-knight — strengthens the FIRED watch-item) · placed-proxy-count (gd-mortar-purifier).
- Maintenance-reservation explicitly NOT filed: no reservation language in gd-pet-conjurer's own dossier ("low resource overhead") — that class stays with skeleton-ritualist evidence.

## §0 near-misses (wanted, could not attest — per kit)

- **gd-dee-witch-hunter:** blind (fetched "fumble curses" — semantics match engine accuracy-tax but the §2 blind row is vision-register; no fumble row) · fear (fetched "confusion effects that neutralize threats" — no confusion row; not a fear naming).
- **gd-devastation-sorcerer:** none (devotion-proc payloads unfetched → nothing wanted).
- **gd-doom-bolt-sentinel:** poison ("acid/chaos DoTs carry between nukes" — DoT named generically, no status word; acid ≠ poison token).
- **gd-drain-essence-spellbinder:** none.
- **gd-eor-warlord:** stun (the "Maul" name tempts it — §0.3/0.4 poster child; payload unfetched → nothing).
- **gd-fire-strike-purifier:** burn (fire flavor saturates the text — "spitting fire" — but burn/ignite never named).
- **gd-flames-of-ignaffar-purifier:** none (burn cleanly attested).
- **gd-forcewave-warlord:** bleed-for-trauma ("Internal Trauma" IS named; no crosswalk row → withheld — this is a ROW gap, not an attestation gap; see steward questions).
- **gd-krieg-death-knight:** none (no statuses named; ADCtH = sustain scaler, not drain).
- **gd-mortar-purifier:** none ("BWC/FoI for additional debuffing" — nothing named).
- **gd-panettis-mage-hunter:** shock (kb-derived, errata-stripped with the mono-lightning read; zero fetched shock language).
- **gd-pet-conjurer:** curse:<variant> (Curse of Frailty named only "for debuffs" HERE — variant unattestable; contrast doom-bolt where RR was fetched and routed curse:sap).

## Steward questions / what felt forced

1. **GD Internal Trauma → bleed?** Named on gd-forcewave-warlord ("emphasis on internal trauma"); §2 bleed row lists bleed/lacerate/rupture only; both docs silent → token withheld, kit held at APPROX. A row would likely lift it to CLOSE.
2. **GD fumble → blind?** Named on gd-dee-witch-hunter ("fumble curses"); engine blind semantics (accuracy-tax only) match exactly, but the row's source register is vision-based. Row-extension is steward's call; withheld.
3. **GD confusion → (fear? nothing?)** — "confusion effects that neutralize threats" (dee). No row anywhere; not emitted.
4. **Forcewave's ZONE_CONTROL door is a weak fit** — no §5 row addresses a spam lane-wave; flagged rather than improvised.
5. **Panettis secondary-slot choice at equal tri-elemental thirds** — lightning chosen over cold arbitrarily (both legal at 1/3 each); steward preference welcome.
6. **Judgment's AoE shape** (eor-warlord) — role fetched ("proc vehicle"), shape not → minimal `circle` token carried a shape-underspecified cast; felt forced but honest.
7. **Timer-based procs have no proc_trigger_condition enum value** (doom-bolt every-20s CDR pulse) — mapped R-M5-style to consequence resource-fill + greppable token `timed-cooldown-refund-pulse` with condition null; an on-timer enum value would remove the wobble.

## Discipline attestations

- Errata honored: ERRATA-35 (fire-strike economy), ERRATA-36 (panettis tri-elemental + shock strip), era restamps (fire-strike/forcewave/mortar/panettis floors), pet-conjurer core-skills correction (Call of the Beast, not Call of the Grave).
- §0.3 payload-nulls: Maul (eor) · WPS individual payloads (fire-strike) · Krieg's Wrath (krieg) · devotion procs (devastation, foi, doom-bolt) · Wind Devil (pet-conjurer) · Time Dilation (devastation, §A residual).
- R-M5 never negated; applied once (doom-bolt), "considered, not applicable" elsewhere.
- DB read-only throughout; probe facts used for orientation only; zero probe-cited tokens.
