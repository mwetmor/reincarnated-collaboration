# Finding — 2026-10-08 — JOIN-1 D-L5 decode (Gate-1, DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**)
**Target:** collab `647423dae` — `agentic_orchestration/legolas/research/2026-10-08-gd-crit-roll-rule-dl5/`
**Developer:** legolas (research) · consumer: gamora J3a prereg AMENDMENT-2 (KP-369)
**Principles applied:** 1 (math before code), 3 (cross-seam impact), 5 (severity matters) · Discipline #10 (empirical inspection over assumption)

## Verdict

**GO for the roll rule as rulebook basis.** I re-ran the read-only tools against `Game.dll` (sha256 `07775a29…529387` re-hashed, matches) and every PRIMARY claim holds. The crit-damage-additive claim stands at MEDIUM-HIGH. **Four WARNs**, none of them against the rule. They concern its **inputs** and the README's **corroboration claims**. WARN-3 and WARN-4 must be resolved inside AMENDMENT-2 before a profile value is committed. WARN-1 and WARN-2 are framing and errata corrections.

## What I verified independently (INFO-1)

| Claim | Check | Result |
|---|---|---|
| `+0x27c = 100.0f` is the roll range | ctor `0x10893c` qword-stores `0x42c80000` (100.0f; the store also zeroes `+0x280`). The loader `0x109080` reads no field into `+0x27c`; its 13 `lea` strings resolve to `pthMinimum`, `pthThreshold1..6` and `pthDamageModifier1..6` exactly. In `0x10d810` it is used twice: `ROLL = maxss(100, PTH)·u`, and `PTH ≥ [+0x27c]` skips the miss test. Its role comes from how it is **used**, not from a name. Other `+0x27c` writers in `.text` (`0xd3f30`, `0xd5640`, `0x373e20`, `0x55d250`, `0x55d380`) belong to other classes' constructors. The CombatManager offset map (`+0x248` PTH equation, `+0x270` normalPTH equation, `+0x278…+0x2ac`) is consistent across ctor, loader, PTH function and roll function. | **HOLDS** |
| `ROLL = max(100,PTH)·u`, one draw for hit and tier | `0x10d878–0x10d88d`. `xmm6=u` and `xmm8=PTH` per the call sites. All three resolver sites (melee `0x10afaa`, ranged `0x10b3fa`, direct `0x10b716`) do a Park–Miller step (`0x41a7`, Schrage `0x69c16bd`), then `cvtsi2ss`, then multiply by float 4.6566129e-10, and pass one `u`. | **HOLDS** |
| No upper PTH clamp | `0x10e490`: one `comiss`/`ja` against `+0x278` (lower bound only). | **HOLDS** |
| No actor-type branch | The whole of `0x10d810` compares only PTH vs 100, ROLL vs PTH, PTH vs thr1, and ROLL vs thr6..thr2. The resolver's `pet*Style` branches only choose display styles. | **HOLDS** (for the roll function, as claimed) |
| Tier = highest `ROLL > thr_i` | `0x10d98e–0x10da0b`, strict `comiss/jbe` cascade 6→2, else `mod1`. thr1 is used only as the `PTH ≤ 70` gate. | **HOLDS** |
| Crit iff mult > 1.0 | `xmm12` is loaded from a `1.0f` constant at `0x10ab0e`. `0x10bfdd` uses `comiss xmm10, xmm12`. | **HOLDS** |
| Debug strings | All resolve as the README states (`PTH %f, Rand Value %f`, `PTH Missed Hit`, `PTH Uber Hit`, `PTH Modifier value %f`, plus `PTH Modifier Equation result %f` on the sub-70 path). The 0.75 fallback is confirmed. | **HOLDS** |

## Findings

**WARN-1 — the README overstates the Lap N tier-shape "strong independent match" (§ 1.4).**
I applied the decoded rule to the board's 95 `p2m_pth_effective` rows (103.54–124.89, w151–160). It predicts these tier shares given a crit: ×1.1 0.59–0.64, ×1.2 0.35–0.39, ×1.3 0.014, ×1.4 0 (equal-weighted or actor-weighted). The footage reads 0.507 / 0.412 / 0.068 / 0.014.
- ×1.3 and ×1.4 together: **12 observed against about 2.1 expected**, Poisson P ≈ 2×10⁻⁶.
- **×1.4 (n=2) needs PTH > 130, but the board's maximum is 124.89.**

The two medians agreeing (112 vs 111.83) does not make the distributions agree. This does **not** threaten the rule: d100 M2 predicts 100 % ×1.1 and is falsified either way. It does show that the **realised in-run PTH sits above the board's static PTH** (DA shred, temporary OA, or a higher-OA source; family B is a candidate). Under the decoded rule, the best two-point fit to the footage is 80 % at PTH 116.5 and 20 % at PTH 132, which implies a crit share of **22–27 %** (≈95 % LR band). The board-fed profile gives 20.8–21.9 %.
*Action:* legolas amends the § 1.4 wording. gamora's AMENDMENT-2 states that the board-fed decoded profile is the **lower-side estimate** relative to the referent footage, and either carries the footage-implied PTH lift as a sensitivity or declares it as a named input gap.

**WARN-2 — the README's monster PTH range "66–85" (§ 3, § 5.2) is wrong for the sealed intake lane.**
At w151–160 the lane reads `m2p_pth_effective` from `pm4o_oa_da.csv` through `measured_board.pth_for` (`threat.py` ≈1868–1875). That range is **77.15–99.98**, with **55 of 95 rows in the crit band [90,100)**. ("66–85" matches the sim's own dex-absent `effective_oa` PTH, about −12.9, which is only the incumbent fallback.)
The conclusions still hold:
- The range cap does not bind, though the margin is **0.02 PTH**, not 15.
- **"≤ 1 pp" is correct.** Max |Δhit| is 0.984 pp and max |Δcrit| is 0.990 pp. The sealed hit chance is `floor(p)/100` against the binary's `p/100`; the sealed crit chance is `(floor(p)−89)/100` against `(p−90)/100`.

The bias is **one-signed**: per swing, the sealed intake expectation is a **mean −0.58 % (range −1.08 % to +0.10 %)** against the binary. That direction flatters the Warlord.
*Action:* legolas corrects the range. The conductor's V2-INTAKE-ROLL note carries the sign and magnitude. **JOIN predicate:** `m2p` is keyed to the Warlord's DA 2591, so a joined kit with lower DA pushes rows to PTH ≥ 100, where the d100 cap **does** bind. Record this before any kit with DA below about 2591 faces this board.

**WARN-3 — `pm4o_oa_da.csv` `p2m_*` crit, tier and expected-multiplier columns encode a third parameterisation.**
These columns are neither M2 nor the decoded rule. Tier mass is taken out of 100, and the non-crit share is set to 100 − crit. Example, row 1 at p = 120.25: the CSV gives crit 30.25 % and E|hit 1.0458; the decoded rule gives 25.16 % and 1.0381. Across the board the CSV's crit runs 13.54–34.89 % against the decoded 13.07–27.94 %. `mech_lift.py:1038` emits `expected_crit_multiplier_range` from `p2m_expected_mult_given_hit`, and MIGRATION ≈L14077 cites the CSV's crit range.
*Action:* AMENDMENT-2 derives per-body crit **only** from per-body PTH plus the decoded rule, and asserts that it never reads these columns. The stale-column note goes to their owners (star-lord for data, MIGRATION). `simulation/kc2/**` is not touched.

**WARN-4 — the crit-damage total is not assigned to a hit source.**
That the displayed multiplier is additive is well supported (INFO-3). Which total applies to the **modelled** Warlord hit is not. Family B (+0.69) carries the larger numbers: median 46,889 against 15,111. At DA 2011 the 0.12 gap moves E[mult/hit] from 1.207 to **1.241**.
*Action:* AMENDMENT-2 names the crit-damage total per modelled ability with its provenance (JUDGED), brackets the other family, and prints both. This is the profile's single judged component.

**INFO-2 — `worked_example.py` reproduces the § 4 table exactly** (PTH 124.8878 / 103.5368; crit 0.2794 / 0.1307; E[tier|crit] 1.1710 / 1.1000; E|hit 1.04777 / 1.01307, and 1.20701 / 1.08760 at +57 %). I checked the arithmetic by hand: (15·1.1 + 15·1.2 + 4.888·1.3)/34.888 = 1.1710; 1.04777 + 0.57·0.2794 = 1.20702. The PTH equation is the DBR's `probabilityToHitEquation`, character for character. M2 at 1.011 and 1.0737 is confirmed, and the KP-369 sizing of +9 % to +21 % is confirmed.

**INFO-3 — crit-damage additivity: MEDIUM-HIGH is defensible.** It splits into two parts:
- **The displayed multiplier's form is close to HIGH.** 151 tokens land on a 0.10-spaced lattice. A multiplicative form `tier·(1+CD)` would give 0.10·(1+CD) spacing, so it is excluded unless CD = 0. The +0.57 offset independently matches the sheet's +57 %.
- **Display = application, and scope (DoT, per-skill CD), are MEDIUM.**

What would raise the grade:
- (a) A binary trace of the `DamageAttributeAbsMod_CritDamageModifier` apply step (README gap 1).
- (b) A footage **damage-ratio** test: within one source, crit damage divided by non-crit damage should cluster at tier + CD. This would test application, not just display.
- (c) A controlled in-game A/B in which CD is changed by a known amount and the offset shifts by exactly that amount. This needs Matt, so it goes to `matt_to_do` if wanted.

**INFO-4 — the Lap N crit-share tension does not threaten the rule.**
- 57 of 144 is 39.6 %, which is **z = 1.6 above the 33.3 % cap** even if the samples are treated as independent; frame-clustered sampling weakens it further.
- Against the footage-fit share of 22–27 % it is about 3σ, so a selection effect has to be present.
- Lap N's claim that the bias runs downward only rests on an **unverified assumption**. FCT lifetime was measured only on crit strings (`15380 (x1.67)`, `23106 (x1.77)`). If crit text persists longer, snapshot sampling over-counts crits (length bias). Small-number FCT filtering and confidence-1.0 OCR on bare numbers versus suffixed numbers are other upward routes.

The binary code is direct evidence and footage share cannot override it. *Action:* 39.6 % must not enter any calibration. The README's "bias runs downward" should be re-graded as an assumption.

**INFO-5 — consistent with P-J2-5 (KP-368).** The decoded PTH at OA 3259 and DA* 2897.2555 is 99.9999997, so DA* is exactly the PTH = 100 boundary. The tightest body (p 106.18, or 102.55 at DA + E_L) recomputes. The binary skips the miss test at PTH ≥ 100 (`comiss`/`jae`), so HIT_CHANCE = 1.0 holds under the decoded rule. **Scope note:** the resolver has **pre-roll miss channels separate from PTH**: `Fumble Chance (%f) caused a miss`, `Defender Dodged Attack`, and `Defender Deflected Attack` (ranged). The theorem only covers PTH misses. If `Fumble` or `ProjectileFumble` debuffs (`control_states.py:342`) or monster dodge reach the Warlord, they are a separate miss route. Also, `Debuff Attack` never calls the roll; README § 7.3 lists only Retaliation and Reflection.

**INFO-6 — minor precision.** The float32 multiplier is exactly 2⁻³¹, not 1/(2³¹−1). So `u` lies in (0, 1], with P(u = 1) ≈ 3×10⁻⁸ and a granularity of about 2⁻²⁴ near 1. This has no effect at distribution level.

## Action
- [ ] gamora (AMENDMENT-2, alone): handle WARN-3 (derive per-body crit from PTH + rule; assert the `p2m_*` crit columns are never read) and WARN-4 (name the CD per ability and bracket the other family). State WARN-1's lower-side framing.
- [ ] legolas (README errata, non-blocking): § 1.4 wording (WARN-1); monster PTH range (WARN-2); grade the Lap N bias as an assumption (INFO-4); add Debuff Attack to § 7.3 (INFO-5).
- [ ] conductor: V2-INTAKE-ROLL note carries the −0.58 % mean, one-signed (WARN-2). Record the JOIN low-DA kit predicate.
- [ ] Matt: none required. The optional raiser INFO-3(c) is an in-game A/B; add it to `matt_to_do` only if the conductor wants CD above MEDIUM-HIGH.

## References
- `agentic_orchestration/legolas/research/2026-10-08-gd-crit-roll-rule-dl5/{README.md, captures/game-dll-x64-disasm-excerpts.txt, captures/worked_example.py, captures/re/*.py}`
- `/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll` (read-only; funcs `0x1087c0`, `0x109080`, `0x10a650`, `0x10d810`, `0x10e3e0`, `0x10e490`)
- `reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` (339–405, 1855–1880); `measured_board.py` (241–280); `mech_lift.py` (1026–1060). All read-only.
- `reincarnated-engine/data/kc2/pm4o_oa_da.csv`, `pm2_hit_math_constants.json`
- `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_findings.md` § A.3–A.8
- `agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i16-measured-board-landing.md` § 2–3
- Ledger KP-358 / 361 / 365 / 367 / 368 / 369
