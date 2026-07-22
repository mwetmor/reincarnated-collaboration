# Finding — 2026-07-22 — tier3-encounter-geometry W0 close (Gate-2)

**Reviewer:** jack-ryan
**Mode:** DEV-MODE (Gate-2; gatekeeper, BLOCK authority)
**Severity:** PASS-WITH-CONCERNS
**Target:** W0 substrate freeze + census — elrond commit `f7224485` (harvest freeze on legolas `e1693613` + `f71cc21e`)
**Developer:** elrond (data steward); reclassification proposed by gandalf (`RUN-CONDUCTOR`) via L-8 + conductor leans
**Handoff artifact:** `agentic_orchestration/elrond/notes/2026-07-22-tier3-w0-census-substrate-freeze.md`
**Principles applied:** REVIEW_PROCESS #4 (committed-truth as truth — decisions-log/ledger), #5 (severity matters); Disciplines #14 (tag-don't-encode; schema validation at boundaries), #46 (empirical inspection over assumption); charter §6 (finding-class discipline), §8 (in-run reclassification = jack-ryan territory); run law L-2 (census IS the handoff), L-8 (reclassify-publish-continue).

## Verdict

**PASS-WITH-CONCERNS.** W0 closes. The substrate is frozen, verified, and sound for W1 derivation. The L-8 reclassification is honest — every genre-truth claim that grounds a "hole" is corroborated by the harvest files' own admissions, and zero rows were fabricated to fill any finding. The finding-set count corrects **3→4** (WHIRLWIND-II folds into the R-b2 serving set); that corrected count is a **hard W1 obligation**. Two concerns ride forward as W1 obligations, neither a BLOCK.

## What I found

The census is faithful to its four source files and to Appendix B. I re-ran `md5 -q` on all four harvest files: the hashes are **byte-identical** to the freeze stamp (§g) — `9b41f22c…`, `f3ae9f6e…`, `b255680354…`, `0dcae6ad…`. Quota verifies (I:20 · II:20 · III:18 · IV:22 = 80; Age IV split 13 PoE2 / 9 LE confirmed against the file's per-row tags). The two-value provenance axis is honest and structured as a TAG column (not encoded into row identity), joinable on `(age, family, derivation_source, provenance)` per §c — Discipline #14 spirit intact; the RDR-NATIVE-DERIVED value is reserved and empty at freeze (0 rows), exactly as it should be before W1 derives. I spot-verified every load-bearing genre-truth claim against the harvest source files (see per-item below); all four "hole" claims and both new findings check out against the files' own admission ledgers.

## Per-item disposition

### (i) THE L-8 RECLASSIFICATION — **SOUND / APPROVED**

The three L-8 cells (f-1 SHAPESHIFT I+III · f-2 DASH-STRIKER I · f-3 CHAIN-BOUNCE IV thin) reclassify honestly from harvest-failure to published finding. Genre-truth claims verified against source:
- **f-1** — Age I file line 75/89 marks SHAPESHIFT "player-class origin / no native monster-analog"; Age III line 75/88 "player-kit origin," Ravager three-form post-game boss logged-and-excluded (A-III.2). Age IV correctly does have a monster-side SHAPESHIFT (row #11 Geonor) so the finding is I+III-specific, not universal — the census states this precisely.
- **f-2** — Age I line 78: "Fanatic-enchanted speed-mod is closest but not a dash-skill." Age III does carry monster-side DASH-STRIKER (#7/#8 Cronley Shadow Strike) → finding is Age-I-specific. Correct.
- **f-3** — Age IV line 97/100: "no dedicated CHAIN-BOUNCE PoE2/LE row found," Scarab (#6) secondary-only; Ages I/II/III each carry a primary (#19/#19/#15). Correct.

**Holes are load-bearing (zero fabricated rows):** confirmed. Every empty cell carries `∅ FINDING` / `— hole` / `THIN` with an explicit Appendix-B expectation; no phantom monster template was invented. The provenance axis is honest and joinable per §c. R-b2 derivation (RDR-NATIVE-DERIVED) is the correct serving mechanism — it makes the derivation *visible and separable* from GENRE-ATTESTED rows rather than laundering a derived template into the attested set. This is the right shape.

### (ii) f-4 / RF-1 — WHIRLWIND Age II — **ADOPT THE FOLD; finding-count 3→4**

I rule: **fold WHIRLWIND-II into the R-b2 serving set.** Not a re-crawl. Rationale:
- The cell is real and of the same class. Age II file line 24 lists WHIRLWIND under "Families ABSENT"; Appendix B B1 records WHIRLWIND=1 (a single record-class KIT membership) for PoE1. The monster-side is empty for the identical root cause as MELEE-STRIKE-II (line 89: PoE1's "0/36" melee/spin deficit — Appendix-B reading 2). Same genre-history mechanism as f-1/f-2/f-3.
- A targeted re-crawl would violate the freeze (§g: any post-freeze harvest edit invalidates the stamp and forces a full re-census) for a **single fresh-single-record cell** with no substrate-integrity payoff (RF-2). The genre truth is that PoE1 has no spin-mob; a re-crawl would either confirm the hole (wasted lap) or surface a boss-tier specimen that the admission discipline already excludes. Deriving via R-b2 is consistent with the three cells L-8 already dispositioned this way.
- **Reclassification authority is mine per §8** — this is exactly the in-run reclassification the charter reserves to Gate-2. I exercise it: WHIRLWIND-II is a **published finding served via RDR-NATIVE-DERIVED**, and the L-8 finding-set corrects from 3→4. Elrond and the conductor flagged-not-decided correctly (RF-1); the flag was routed to the right authority.

### (iii) f-5 / ⚠-D — DASH-STRIKER Age IV — **CONFIRM (fresh-draft non-obligation)**

I confirm the elrond+conductor lean. Appendix B B3 records DASH-STRIKER=1 **fresh-draft** for Age IV; the Age IV harvest supplies zero and logs no admission (verified: the family is absent from the coverage check, lines 87-97). Per **T3-V2**, FRESH-DRAFT is excluded from serving — so a missing DASH-STRIKER-IV row creates **no W1 serving obligation**, no re-crawl obligation, no fabrication. Recorded as finding f-5 for completeness. This is the correct call; fresh-draft is explicitly an input-to-future-dockets tier, not a serving tier. (Minor note for the record, INFO-level: f-5 differs from f-1/f-4 in that no admission was logged at harvest time — the gap surfaced only at census. Not a defect; the census is precisely where it should surface. Flagged so W1 does not mistake f-5 for a servable RDR-NATIVE-DERIVED cell — it is not, unless W1 elects to derive it, which the census correctly frames as optional.)

### (iv) HANDOFF INTEGRITY per L-2 — **VALID**

The census satisfies every predicate for the W0→W1 handoff role:
- **Quota** — sound; 80 rows verified against per-file headers and body counts; no off-by-one; run-state "80" confirmed byte-for-byte.
- **Era×family matrix vs Appendix B** — faithful. Spot-checked: WHIRLWIND-II `⚠∅ (exp:1)` matches B1=1 + Age II ABSENT line; MELEE-STRIKE-II `∅ (exp:—, genre hole)` matches B2's 0/36 + row #8 UNMAPPED-to-honor-hole (line 89); CHANNELED-BEAM-I `— hole` matches B1 (—) + Age I ABSENT line 18; MINION-PET ×4 and IDENTITY-GAUGE ×4 holes match B1/B2 off-spine (—). The present/absent-agreement check (the *meaningful* check — numeric surplus is expected since Appendix B is kit-membership tallies not monster-template counts) holds across all cells; the census states this distinction correctly (§b over-coverage note).
- **Provenance axis** — structured for the W1 join (§c); tag-column not identity-encoded; union admits RDR-NATIVE-DERIVED with no schema change. Discipline #14 satisfied.
- **Freeze stamp** — VALID; I re-ran md5, all four match.
- **UNMAPPED (7) + admissions (21)** — coherent. U-2+U-6 correctly identified as one cross-era resurrection-leader verb candidate (D2 Shaman ↔ GD Dominator). Admission count 21 (4+5+5+7) reconciles the run-state "~20" estimate with a stated rounding note — no admission dropped or double-counted. §h schema-drift observations (header-casing divergence across the L-5 two-agent split; per-row source tag Age-IV-only; Age II soft citation floor; LE 1.0-era staleness) are correctly logged-not-fixed (freeze means freeze) and are genuine W1 ingestion requirements.

## What the W1 grammar spec MUST carry forward

1. **Corrected finding-set count = 4** (not 3). The R-b2 RDR-NATIVE-DERIVED serving set is: **SHAPESHIFT-I, SHAPESHIFT-III, DASH-STRIKER-I, CHAIN-BOUNCE-IV-thin, and WHIRLWIND-II.** (Five cells across four findings — f-1 spans two ages.) W1 must derive these, provenance-flagged RDR-NATIVE-DERIVED, slotting into the `∅ FINDING`/`THIN` matrix cells per §c's join key. This is a **hard obligation** — the count correction is the material output of this gate.
2. **f-5 (DASH-STRIKER-IV) is NOT in the serving set.** Fresh-draft, T3-V2-excluded. W1 must not mistake it for a servable cell (derivation optional only).
3. **Ingestion must normalize header casing** across the two-agent pair-split (§h.1) and **branch source-tag logic** for Age IV (§h.3) — do not assume byte-identical headers or a universal per-row source tag. Read ROW TABLE + SUMMARY as authoritative, not the preamble format (§h.2).
4. **MEDIUM-confidence flags travel with the data:** Age II formation details where the only cite is the Maxroll campaign guide (§h.4); LE rows are 1.0-era, pre-Season-3 (§h.5). W1 MESO/MICRO derivation should carry the confidence tag, not silently promote MEDIUM to firm.
5. **f-6 DOT-AILMENT-II under-density is INFORMATIONAL** — Age II's signature family (15 kit-mass) is present-but-lightly-sampled (3 rows). Within quota, no action, but the W1 SPEC-AUTHOR should know before deriving Age-II MESO formation richness.
6. **Resurrection-leader (U-2+U-6) is one candidate MICRO-verb spanning Ages I+III**, not two isolated UNMAPPEDs — per §d cross-era pattern. A W1 ruling resolves both; family-name canonization stays a Matt HALT (§5) — working labels only in all W1 artifacts.

## Rationale

The reclassification is legitimate under **run law L-8** (Gate-B→F-1 precedent: reclassify, publish, continue) and **charter §6** finding-class discipline. The fold ruling on (ii) is mine to make per **charter §8** (in-run reclassification = jack-ryan Gate-2 territory) — the conductor correctly flagged-not-decided (RF-1). No **committed-truth conflict** (REVIEW_PROCESS #4): the finding-count correction is additive to the ledger, consistent with T3-V2/T3-V3, and touches no locked decision. **Discipline #46** (empirical inspection) drove the source-file spot-verify rather than accepting the census's claims on assertion; **Discipline #14** grounds the provenance-axis-as-tag approval. No red-flag-class item per §6 fires: no commitment-boundary hit, no substrate-integrity danger (RF-2 confirms RATIFIED/DOCKETED families all have ≥1 covered cell where Appendix B expects them, save the L-8-dispositioned f-1/f-2), and this gate resolves rather than escalates. No BLOCK.

## Action

- [x] jack-ryan: L-8 reclassification APPROVED; WHIRLWIND-II fold ADOPTED (finding-count 3→4); f-5 fresh-draft non-obligation CONFIRMED; handoff VALID. W0 closes CLEAN into W1.
- [ ] Conductor: record this gate's finding-count correction (3→4) in the run-state ledger; W1 R-b2 serving scope = the five cells named above.
- [ ] W1 SPEC-AUTHOR (named-gandalf): carry forward obligations 1-6; derive the five RDR-NATIVE-DERIVED cells; do NOT serve working family-labels as canon (§5 Matt HALT).
- [ ] No Matt escalation required — this gate is within §8 in-run-reclassification authority; no commitment-boundary or locked-decision conflict.

## References

- `agentic_orchestration/elrond/notes/2026-07-22-tier3-w0-census-substrate-freeze.md` (the handoff artifact under review)
- `agentic_orchestration/legolas/harvests/2026-07-22-tier3-era-family-mob-harvest/{age-I-diablo2,age-II-poe1,age-III-grim-dawn,age-IV-poe2-le}.md` (source spot-verify; md5 re-run)
- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md` (rulings L-2, L-8; W0 wave-ledger row)
- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` (§4 W0 done-predicate; §6 finding-classes; §7 T3-V1..V7; §8 fallback)
- `canonical/matt_decision_needed/2026-07-22-tier3-encounter-geometry-charter-grill.md` (Appendix B B1-B3 expectation authority)
- `agentic_orchestration/qa/findings/2026-07-22-gate1-tier3-encounter-geometry-launch.md` (my Gate-1 record; commit `9758d7e1`)

*Filed by jack-ryan (DEV-MODE Gate-2), 2026-07-22.*
