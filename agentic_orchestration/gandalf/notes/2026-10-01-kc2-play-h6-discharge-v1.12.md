# KC2-PLAY · H-6 discharge note for T-A prereg v1.12: § F.2k.6 filled from the graded-digest emission

**Date:** 2026-10-01 · **Author:** gamora (builder; prereg author) · **Conductor:** gandalf · **Run:** KC2-PLAY (charter rows KP-168, KP-169, KP-170)
**Discharges:** prereg v1.12 § H **H-6** (R-11 = `TA-X-07` clause (c), § F.2k (L2)), and fills the § F.2k.6 form.
**Prereg of record:** v1.12, `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md`, FILE sha256 `a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854` (recomputed; collab `a6bce6f5c`). **That file is not edited.** This note is where § F.2k.6 says the values go.
**Answers:** jack-ryan's v1.12 pre-read (collab `1e8bcd1e3`) **WARN-2**, **INFO-2**, **INFO-3**, and the Path-B record his action item 6 asks for.
**Computation:** `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-h6-discharge-v1.12/h6_l2_exact.py` (sha256 `c51c95b5b38b071f2fc73bfbb08bd16517508e2152cef7c7967a126a40501b76`), output `results.json` beside it (sha256 `a6bbb0fd0c6bb9f5816bc927b0b4363390da8aba6606cba45f189a833c580289`). Exit 0 iff every pin matches, the census check is green, the probe reference reproduces and (L2) holds on all 25 cells.

**Read-before-result attestation.** No graded run exists under v1.12; attempts used 0 of 2. I read godot **only through git objects** (`git show <rev>:<path>`, `git ls-tree`, `git grep <rev>`) at `ada8048` (the runtime) and `e40a4fc` (drax's `AGENT_STATE.md`, which carries the operands). Nothing was checked out, run or written in godot or the engine. No tolerance or expected value is touched: clause (a) stays 1e-12; the 5 / 28 / 1 / 19 / 3 expectations are not read, let alone moved.

---

## Verdict

> **H-6: DISCHARGED.** § F.2k (L2) holds on **all 25 cells** of the runtime at godot `ada8048` (tree FILE `fda00e28…`), evaluated independently in exact rationals. All four antecedents hold on every cell.
>
> **Worst cell:** `M0 · 0` (and `M-POL-2-NULL · 0`, which emits identical operands): **β = 3.582525e-14**, margin **1e-12 / β = ×27.91** (first-order `M` = 27.91, `Λ` = 322.69). Best margin ×44.63.
>
> **drax's figures: CONFIRMED** on every cell to every printed digit (β to 5 s.f., `Λ` and `M` to 2 d.p.). One disagreement with drax's *prose*, not his (L2) figures: his line "19 cells 0.0" for `ρ̂` (repeated in KP-170 as "19 cells exactly 0") does not match his own emission, which has **21** cells at 0.0 and **4** non-zero (§ 4). Clause (a) is not graded here, so no verdict depends on it.

---

## 1 · Method (INFO-2: β is evaluated in exact rationals)

Every emitted float string is parsed to its binary64 value and lifted **exactly** with `fractions.Fraction(float(s))`. `u = Fraction(1, 2**53)`, `γ_k = k·u / (1 − k·u)`, and the tolerance is the decimal `Fraction(1, 10**12)`. No floating-point operation sits between the emitted operands and the comparison `β ≤ 1e-12`. The exact β of the worst cell is a fraction with a 1,630-bit numerator, recorded in `results.json`.

The law is evaluated **as written** in § F.2k.3 (no coefficient, term or antecedent altered):

* `A⁺_k = Â_k / (1 − u − γ²_{n_k−1})` for the seven accumulators. For the two inner Σ|term| sums, the `n` in this correction is the **run-level** inner term count (`inner_totals.stream_terms`, `…pcl_terms`), because `inner_stream_abs` / `inner_pcl_abs` are single Neumaier sums over the whole run. That is the larger, correct count. It moves no printed digit.
* `B⁺ = Σ_{k∈K}(u + γ²_{n_k−1})·A⁺_k + (u + γ²₅)·Σ_{j∈sinks}(1 + u + γ²_{n_j−1})·A⁺_j + Σ_I (u + γ²_{N_I−1})·A⁺_I + φ·Σ_{k: q_k>0} A⁺_k`, with `N_I` = the emitted `N_inner` (largest term count of any one inner sum) and `q_k` as emitted.
* `φ = γ_{2·f_max}`, `f_max = max(R + 4, 2N, 2K + 3)` from the census's CHAINS block and the cell's emitted `census_counters` (R = `pkt_rows_max`, N = `dot_buckets_max`, K = `burn_n_due_max`).
* `β = (1 + u)²·B⁺ / max(1, |Ô|)`.
* `Λ` and `M = (1e-12/u)/Λ` per § F.2k.5, on `Â`, printed only, never graded.

**Where B comes from.** On every cell the `φ` term is 98.5–99.1 % of `B⁺`. The seven accumulators contribute about 0.6–1.0 %, the six-way sum about 0.3–0.5 %, and the inner sums under 0.01 %. So, as drax said, the margin is set by the census chain lengths, in practice the DoT increment chain (`2N` = 100–160 at `N` = 50–80). Depth plays no part.

---

## 2 · The § F.2k.6 form, filled

`φ` is printed as its index, `γ_{2·f_max}`. `ρ̂` is clause (a)'s statistic as emitted. It is printed because the form has a column for it, and **it is not graded here** (it is graded only in the attempt).

| arm · salt | `n_k` (off/app/drp/voi/pt/pcl/cp) | `N_I` (s/p) | `q_k` (off/app/drp/voi/pt/pcl/cp) | R/N/K → `f_max`; `φ` | `Λ` | `β` (exact, 7 s.f.) | margin 1e-12/β | `M` | (L2) | `ρ̂` (not graded here) |
|---|---|---|---|---|---|---|---|---|---|---|
| M0 · 0 | 6777/12239/755/6682/12239/218/5804 | 44/2 | 0/4600/261/6682/12239/218/0 | 6/80/1 → 160; γ_320 | 322.69 | 3.582525e-14 | ×27.91 | 27.91 | HOLDS | 0.0 |
| M0 · 1 | 1519/2882/198/1368/2882/25/1801 | 14/2 | 0/1484/86/1368/2882/25/0 | 7/50/1 → 100; γ_200 | 201.98 | 2.242461e-14 | ×44.59 | 44.59 | HOLDS | 0.0 |
| M0 · 2 | 1409/2583/172/1314/2583/21/1537 | 12/1 | 0/1188/75/1314/2583/21/0 | 9/50/1 → 100; γ_200 | 202.72 | 2.250669e-14 | ×44.43 | 44.43 | HOLDS | 0.0 |
| M0 · 3 | 1391/2636/160/1274/2636/26/1477 | 16/2 | 0/987/62/1274/2636/26/0 | 8/50/1 → 100; γ_200 | 202.15 | 2.244279e-14 | ×44.56 | 44.56 | HOLDS | 2.2138341115505915e-16 |
| M0 · 4 | 998/1584/257/895/1584/20/744 | 13/2 | 0/709/35/895/1584/20/0 | 7/50/1 → 100; γ_200 | 202.15 | 2.244354e-14 | ×44.56 | 44.56 | HOLDS | 1.679114046989827e-16 |
| M-POL-2 · 0 | 1076/1581/239/949/1581/19/986 | 11/1 | 0/698/31/949/1581/19/0 | 7/50/1 → 100; γ_200 | 201.81 | 2.240545e-14 | ×44.63 | 44.63 | HOLDS | 0.0 |
| M-POL-2 · 1 | 6616/11942/470/6528/11942/200/5288 | 31/2 | 0/3936/242/6528/11942/200/0 | 6/50/1 → 100; γ_200 | 202.55 | 2.248760e-14 | ×44.47 | 44.47 | HOLDS | 0.0 |
| M-POL-2 · 2 | 1428/2746/174/1319/2746/22/1717 | 12/1 | 0/1288/73/1319/2746/22/0 | 9/50/1 → 100; γ_200 | 202.70 | 2.250391e-14 | ×44.44 | 44.44 | HOLDS | 0.0 |
| M-POL-2 · 3 | 1411/2711/170/1289/2711/27/1682 | 16/2 | 0/1039/69/1289/2711/27/0 | 8/50/1 → 100; γ_200 | 202.15 | 2.244306e-14 | ×44.56 | 44.56 | HOLDS | 0.0 |
| M-POL-2 · 4 | 1046/1607/305/929/1607/20/766 | 13/1 | 0/689/33/929/1607/20/0 | 7/60/1 → 120; γ_240 | 241.87 | 2.685285e-14 | ×37.24 | 37.24 | HOLDS | 0.0 |
| M-POL-2-NULL · 0 | 6777/12239/755/6682/12239/218/5804 | 44/2 | 0/4600/261/6682/12239/218/0 | 6/80/1 → 160; γ_320 | 322.69 | 3.582525e-14 | ×27.91 | 27.91 | HOLDS | 0.0 |
| M-POL-2-NULL · 1 | 1519/2882/198/1368/2882/25/1801 | 14/2 | 0/1484/86/1368/2882/25/0 | 7/50/1 → 100; γ_200 | 201.98 | 2.242461e-14 | ×44.59 | 44.59 | HOLDS | 0.0 |
| M-POL-2-NULL · 2 | 1409/2583/172/1314/2583/21/1537 | 12/1 | 0/1188/75/1314/2583/21/0 | 9/50/1 → 100; γ_200 | 202.72 | 2.250669e-14 | ×44.43 | 44.43 | HOLDS | 0.0 |
| M-POL-2-NULL · 3 | 1391/2636/160/1274/2636/26/1477 | 16/2 | 0/987/62/1274/2636/26/0 | 8/50/1 → 100; γ_200 | 202.15 | 2.244279e-14 | ×44.56 | 44.56 | HOLDS | 2.2138341115505915e-16 |
| M-POL-2-NULL · 4 | 998/1584/257/895/1584/20/744 | 13/2 | 0/709/35/895/1584/20/0 | 7/50/1 → 100; γ_200 | 202.15 | 2.244354e-14 | ×44.56 | 44.56 | HOLDS | 1.679114046989827e-16 |
| W1 · 0 | 1076/1581/239/949/1581/19/986 | 11/1 | 0/698/31/949/1581/19/0 | 7/50/1 → 100; γ_200 | 201.81 | 2.240545e-14 | ×44.63 | 44.63 | HOLDS | 0.0 |
| W1 · 1 | 6539/11975/465/6342/11975/181/5306 | 26/2 | 0/3824/216/6342/11975/181/0 | 6/80/1 → 160; γ_320 | 322.27 | 3.577962e-14 | ×27.95 | 27.95 | HOLDS | 0.0 |
| W1 · 2 | 1428/2746/174/1319/2746/22/1717 | 12/1 | 0/1288/73/1319/2746/22/0 | 9/50/1 → 100; γ_200 | 202.70 | 2.250391e-14 | ×44.44 | 44.44 | HOLDS | 0.0 |
| W1 · 3 | 1400/2427/167/1288/2427/26/1684 | 14/2 | 0/992/68/1288/2427/26/0 | 8/50/1 → 100; γ_200 | 202.16 | 2.244445e-14 | ×44.55 | 44.55 | HOLDS | 0.0 |
| W1 · 4 | 953/1520/230/878/1520/19/794 | 13/1 | 0/559/30/878/1520/19/0 | 7/50/1 → 100; γ_200 | 202.11 | 2.243822e-14 | ×44.57 | 44.57 | HOLDS | 0.0 |
| W1-NULL · 0 | 1076/1581/239/949/1581/19/986 | 11/1 | 0/698/31/949/1581/19/0 | 7/50/1 → 100; γ_200 | 201.81 | 2.240545e-14 | ×44.63 | 44.63 | HOLDS | 0.0 |
| W1-NULL · 1 | 6616/11942/470/6528/11942/200/5288 | 31/2 | 0/3936/242/6528/11942/200/0 | 6/50/1 → 100; γ_200 | 202.55 | 2.248760e-14 | ×44.47 | 44.47 | HOLDS | 0.0 |
| W1-NULL · 2 | 1428/2746/174/1319/2746/22/1717 | 12/1 | 0/1288/73/1319/2746/22/0 | 9/50/1 → 100; γ_200 | 202.70 | 2.250391e-14 | ×44.44 | 44.44 | HOLDS | 0.0 |
| W1-NULL · 3 | 1411/2711/170/1289/2711/27/1682 | 16/2 | 0/1039/69/1289/2711/27/0 | 8/50/1 → 100; γ_200 | 202.15 | 2.244306e-14 | ×44.56 | 44.56 | HOLDS | 0.0 |
| W1-NULL · 4 | 1046/1607/305/929/1607/20/766 | 13/1 | 0/689/33/929/1607/20/0 | 7/60/1 → 120; γ_240 | 241.87 | 2.685285e-14 | ×37.24 | 37.24 | HOLDS | 0.0 |

**The `Â` operands as emitted** (lossless CPython-repr strings, copied from the parsed JSON lines at godot `e40a4fc:AGENT_STATE.md`):

| arm · salt | `Â_k` off / app / drp / voi / pt / pcl / cp (CPython repr, as emitted) | `Â_I` stream / pcl | `Ô` |
|---|---|---|---|
| M0 · 0 | 191028961.69028333 / 132886740.66214536 / 328990.4607615127 / 50294264.537524536 / 7322510.813374652 / 0.0 / 446533.84198746673 | 1926196.400550133 / 293193.7015954483 | 191028961.69028333 |
| M0 · 1 | 34004515.35815023 / 26080195.463634636 / 200081.63190498273 / 5989352.053371543 / 1559959.8997877713 / 0.0 / 177586.3614921103 | 333525.08272404614 / 60235.073928259575 | 34004515.35815023 |
| M0 · 2 | 33916351.52036713 / 26324256.23810337 / 160721.01362877135 / 5720299.102325066 / 1660910.7129783256 / 0.0 / 152693.0716989413 | 350974.7360869565 / 57497.05900589747 | 33916351.52036713 |
| M0 · 3 | 33654647.19353054 / 26030384.201507587 / 82169.62590913892 / 5845156.8484339295 / 1551369.005567597 / 0.0 / 145697.51211228006 | 337931.8799112688 / 57975.844597892516 | 33654647.19353054 |
| M0 · 4 | 22186046.892647333 / 16936440.335288685 / 167792.98353791895 / 3979957.8682318926 / 1006486.0701652141 / 0.0 / 114582.45253098392 | 212210.6713664596 / 42031.898835119966 | 22186046.892647333 |
| M-POL-2 · 0 | 22844273.331537917 / 17263853.067011457 / 246650.94720790698 / 4196153.496452058 / 1000408.7813818583 / 0.0 / 137337.03948463683 | 227716.80527950308 / 37770.3373580816 | 22844273.331537917 |
| M-POL-2 · 1 | 183921023.63466296 / 128083050.27452424 / 231194.43027210922 / 48292203.7964301 / 6889465.22213752 / 0.0 / 432483.9677142367 | 2023023.0757231587 / 275254.0770636808 | 183921023.63466296 |
| M-POL-2 · 2 | 33894098.83500898 / 26332309.44551996 / 152864.05668106384 / 5722456.003248882 / 1632018.452640719 / 0.0 / 160204.59936733468 | 356572.81064773735 / 57494.9557217003 | 33894098.83500898 |
| M-POL-2 · 3 | 33711877.144325115 / 26031050.867463786 / 101995.13179491676 / 5877071.552722513 / 1556333.432827265 / 0.0 / 145556.15951663206 | 339010.13721384207 / 61636.10111034 | 33711877.144325115 |
| M-POL-2 · 4 | 22379443.524372373 / 16945307.420777675 / 238231.58586001382 / 4069342.1538301264 / 1019767.3924957749 / 0.0 / 126007.78851614607 | 237676.45322981366 / 42288.18211946968 | 22379443.524372373 |
| M-POL-2-NULL · 0 | 191028961.69028333 / 132886740.66214536 / 328990.4607615127 / 50294264.537524536 / 7322510.813374652 / 0.0 / 446533.84198746673 | 1926196.400550133 / 293193.7015954483 | 191028961.69028333 |
| M-POL-2-NULL · 1 | 34004515.35815023 / 26080195.463634636 / 200081.63190498273 / 5989352.053371543 / 1559959.8997877713 / 0.0 / 177586.3614921103 | 333525.08272404614 / 60235.073928259575 | 34004515.35815023 |
| M-POL-2-NULL · 2 | 33916351.52036713 / 26324256.23810337 / 160721.01362877135 / 5720299.102325066 / 1660910.7129783256 / 0.0 / 152693.0716989413 | 350974.7360869565 / 57497.05900589747 | 33916351.52036713 |
| M-POL-2-NULL · 3 | 33654647.19353054 / 26030384.201507587 / 82169.62590913892 / 5845156.8484339295 / 1551369.005567597 / 0.0 / 145697.51211228006 | 337931.8799112688 / 57975.844597892516 | 33654647.19353054 |
| M-POL-2-NULL · 4 | 22186046.892647333 / 16936440.335288685 / 167792.98353791895 / 3979957.8682318926 / 1006486.0701652141 / 0.0 / 114582.45253098392 | 212210.6713664596 / 42031.898835119966 | 22186046.892647333 |
| W1 · 0 | 22844273.331537917 / 17263853.067011457 / 246650.94720790698 / 4196153.496452058 / 1000408.7813818583 / 0.0 / 137337.03948463683 | 227716.80527950308 / 37770.3373580816 | 22844273.331537917 |
| W1 · 1 | 180013759.78073004 / 125182518.73544931 / 236698.5226844488 / 47584094.00612402 / 6595062.369779788 / 0.0 / 422890.2031077374 | 2002270.6176397514 / 248579.70805615713 | 180013759.78073004 |
| W1 · 2 | 33894098.83500898 / 26332309.44551996 / 152864.05668106384 / 5722456.003248882 / 1632018.452640719 / 0.0 / 160204.59936733468 | 356572.81064773735 / 57494.9557217003 | 33894098.83500898 |
| W1 · 3 | 33698735.15878359 / 26031122.88266682 / 99229.541115847 / 5862777.882937786 / 1562327.0088703 / 0.0 / 143407.84319283997 | 344982.73175687663 / 57673.64646157058 | 33698735.15878359 |
| W1 · 4 | 21963679.629717875 / 16771756.434350254 / 161905.68402303522 / 3847952.237957156 / 1082268.1156895084 / 0.0 / 118879.97480528645 | 228210.74955634426 / 47735.83280899215 | 21963679.629717875 |
| W1-NULL · 0 | 22844273.331537917 / 17263853.067011457 / 246650.94720790698 / 4196153.496452058 / 1000408.7813818583 / 0.0 / 137337.03948463683 | 227716.80527950308 / 37770.3373580816 | 22844273.331537917 |
| W1-NULL · 1 | 183921023.63466296 / 128083050.27452424 / 231194.43027210922 / 48292203.7964301 / 6889465.22213752 / 0.0 / 432483.9677142367 | 2023023.0757231587 / 275254.0770636808 | 183921023.63466296 |
| W1-NULL · 2 | 33894098.83500898 / 26332309.44551996 / 152864.05668106384 / 5722456.003248882 / 1632018.452640719 / 0.0 / 160204.59936733468 | 356572.81064773735 / 57494.9557217003 | 33894098.83500898 |
| W1-NULL · 3 | 33711877.144325115 / 26031050.867463786 / 101995.13179491676 / 5877071.552722513 / 1556333.432827265 / 0.0 / 145556.15951663206 | 339010.13721384207 / 61636.10111034 | 33711877.144325115 |
| W1-NULL · 4 | 22379443.524372373 / 16945307.420777675 / 238231.58586001382 / 4069342.1538301264 / 1019767.3924957749 / 0.0 / 126007.78851614607 | 237676.45322981366 / 42288.18211946968 | 22379443.524372373 |

**Sensitivity (not the law; § 7):** β_stress with 2φ charged on all seven accumulators.

| arm · salt | β_stress (2φ on all seven) | holds |
|---|---|---|
| M0 · 0 | 1.4254e-13 | True |
| M0 · 1 | 8.9156e-14 | True |
| M0 · 2 | 8.9287e-14 | True |
| M0 · 3 | 8.9152e-14 | True |
| M0 · 4 | 8.9191e-14 | True |
| M-POL-2 · 0 | 8.9152e-14 | True |
| M-POL-2 · 1 | 8.9154e-14 | True |
| M-POL-2 · 2 | 8.9292e-14 | True |
| M-POL-2 · 3 | 8.9152e-14 | True |
| M-POL-2 · 4 | 1.0696e-13 | True |
| M-POL-2-NULL · 0 | 1.4254e-13 | True |
| M-POL-2-NULL · 1 | 8.9156e-14 | True |
| M-POL-2-NULL · 2 | 8.9287e-14 | True |
| M-POL-2-NULL · 3 | 8.9152e-14 | True |
| M-POL-2-NULL · 4 | 8.9191e-14 | True |
| W1 · 0 | 8.9152e-14 | True |
| W1 · 1 | 1.4245e-13 | True |
| W1 · 2 | 8.9292e-14 | True |
| W1 · 3 | 8.9152e-14 | True |
| W1 · 4 | 8.9191e-14 | True |
| W1-NULL · 0 | 8.9152e-14 | True |
| W1-NULL · 1 | 8.9154e-14 | True |
| W1-NULL · 2 | 8.9292e-14 | True |
| W1-NULL · 3 | 8.9152e-14 | True |
| W1-NULL · 4 | 1.0696e-13 | True |

---

## 3 · The antecedents, per cell

| (L2) item | check | result |
|---|---|---|
| **1 · lossless emission** | Every float operand (`Â_k` ×7, `Â_I` ×2, `Ô`) satisfies `repr(float(s)) == s` and is finite. Every count (`n_k` ×7, `q_k` ×7, `N_I` ×2) is a JSON integer. The key sets equal the seven accumulators. `final_sum_n_terms = 6` and `sink_terms_present = 6`. The emitter (`kc2rt_fight.gd:6643–6672` at `ada8048`) writes `Kc2RtExactNum.py_repr` strings, and `Â` is `fl(s + c)` of the Σ|x| Neumaier pair, which is exactly the law's `Â`. | **25 / 25** |
| **2 · census filed at the graded digest** | `kc2_runtime/tests/kc2rt_booking_census.gd` at `ada8048` = FILE `ecdea42e…`, a MANIFEST member of tree `fda00e28…`. I re-ran its `verify()` independently in Python against `kc2rt_fight.gd` `5dfb865c…`: **47 rows over 35 sites; T 28 · S 11 · F 8** (the figures in the brief). Each row's code matches its source line verbatim. The site set equals the census's own `GIT_GREP` command, run with `git grep <rev>` (35 = 35), with no uncensused site and no stale row. Every S row is flagged `, true)`; every F row carries a flag (`, true)` or `cnt > 0, cnt`). No T row is unconditionally flagged. The two T rows at `:5576` are the PLAY-path `_land` callers, whose conditional flag sees `carried = 0`; the ORACLE arms never take them. Closure: 29 terminal paths, each ending in named sinks. The unbound-PCL path is shown unreachable: `n_unbound_pcl_rows = 0` on all 25 cells. `φ` is taken from the census rule. | **filed; green; 25 / 25** |
| **3 · n·u < 1** | The largest count on any cell is 12,239 (`applied` / `pool_truncated`, `M0·0`). Every γ is defined; the bound is 9·10¹⁵. | **25 / 25** |
| **4 · β ≤ 1e-12** | § 2 | **25 / 25** |

**H-6 (d), the fail-first Neumaier probe.** I rebuilt the probe vector from its definition (`tests/kc2rt_v3p7p1_probes.gd:585–640` at `ada8048`: an LCG with seed 20261001, 1,011 terms) and recomputed the **Python half**. Neumaier gives `c4e02c678b219c80`, equal to `math.fsum`. The naive sum gives `c4e02c678b219c7e` (2 ulps off). Neumaier on |x| gives `4517dfbddad11c7f`. These are the reference bits the port is asserted against. **The port half is drax-reported** (`AGENT_STATE`: port `c4e02c678b219c80`; suite v3.7.1 13/13). I did not run Godot.

---

## 4 · Against drax's figures

* **β, Λ, M:** I agree on **all 25 cells**, at drax's printed precision. The `f_max` per cell also agrees (160 on `M0·0`, `M-POL-2-NULL·0` and `W1·1`; 120 on `M-POL-2·4` and `W1-NULL·4`; 100 elsewhere). His worst β of 3.58e-14 at `M0·0`, margin ×27.9: **confirmed** (×27.913).
* **One disagreement, in prose only:** drax's `AGENT_STATE` line *"max residual_relative … 2.2138341115505915e-16 (M0·3 / M-POL-2-NULL·3); 19 cells 0.0"*, carried into KP-170 as *"19 cells exactly 0"*. His own 25 operand lines give **21 cells at `0.0`**. The four non-zero cells are `M0·3` and `M-POL-2-NULL·3` (2.2138341115505915e-16) and `M0·4` and `M-POL-2-NULL·4` (1.679114046989827e-16). The maximum he quotes is right. **No verdict moves:** clause (a) is graded only in the attempt, and all four are below 1e-12 by ×4,500 or more. The ledger count needs a one-word correction at the next KP row.

---

## 5 · Re-pins (v1.12 item 9 / jack-ryan must 8, PENDING in v1.12, now filled)

Every digest below was recomputed by the script from git objects at `ada8048`, and again at `e40a4fc` (identical at both).

| object | path (godot) | sha256 (FILE) | matches drax / brief |
|---|---|---|---|
| fight | `kc2_runtime/sim/kc2rt_fight.gd` | `5dfb865cf4d4bb0431db17e2ebd00f47bf0eb8455a6aecefd34be391ebbabbcb` | ✓ |
| laws | `kc2_runtime/sim/kc2rt_laws.gd` | `c234376e9cbadc2d6f69549966112ec4fc1da7df46069831c7f1b80e3f581a9c` | ✓ (unchanged since `933b438`, the READ pin) |
| G3 port tool | `kc2_runtime/tools/kc2rt_g3_loop_trace.gd` | `50908a225430b3e9ed67dff098d8a730f50c40f25cc91f436ff88ec353e40443` | ✓ |
| G3 oracle tool | `kc2_runtime/tools/kc2rt_g3_oracle_trace.py` | `90a036201acab154eed70c43bacbd83f729c6435568d20757fee3016564e5179` | ✓ |
| booking census | `kc2_runtime/tests/kc2rt_booking_census.gd` | `ecdea42edc35b1e04ac725907ba6fc6a877cada3bfe129a1aff3d81bacde7a54` | ✓ |
| **runtime tree** | `kc2_runtime/MANIFEST.json` law: sha256 of the newline-joined `<relpath>  <sha256>` lines, sorted | **`fda00e2876405cec4ff73d8ab836679539ca96b1e77b22a47750cbd598c09a86`** | ✓ recomputed from all **82** members' blobs, each matching its MANIFEST digest (0 failures). Every tracked file under `kc2_runtime/` is a member except `MANIFEST.json` itself. All five files above are members. The MANIFEST is byte-identical at `e40a4fc`. |

Since v1.12 pinned `kc2rt_fight.gd` at `2277cc89…` (`933b438`, READ), the file has moved to `5dfb865c…`. **(N1)–(N8) re-verified at `5dfb865c…`, in the parts the law reads:** `_cons_add` (Neumaier; Σ|x| Neumaier; a conditional flag count `n_round`) and `_offer` are as read. The inner sums still offer `fl(s + c)`. The emission carries `n` / `Â` / `q` / `N_inner` / `inner_totals` / `final_sum_n_terms`. The stale (N8) labels (`n_terms_note`, `accumulation_budget_terms_v1p7`) are still emitted, and they are not read here. This sub-check covers only what (L2) consumes. The full R-1…R-22 read belongs to jack-ryan's repair Gate-2.

---

## 6 · How (L1) carries the packet path under Path B (jack-ryan action 6; KP-169 Ruling 1)

v1.12's (L1) is applied **as written**. Following Ruling 1, the packet path's roundings are charged through `q_k` and `φ`:

* **The runtime flags them (emission only).** `_land` receives `carried = _pkt_roundings(n_rows, direct, pcl) + _cp_last_roundings` and books `applied` with `carried > 0, carried` (`:5576`). `_pkt_roundings` = (rows − 1) + 1 if both direct and PCL are non-zero. `_cp_absorb` counts its remainder subtractions. The after-death and wave-close drops (`:4136`, `:4172`) and the dead-pool burns (`:4734`) flag their carried counts too.
* **The census classes them F(f)**, with eight rows: `:4136` dropped F(R) · `:4172` dropped F(R) · `:4638` dropped F(2N) (DOT_INC) · `:4734` dropped F(2K−1) · `:5576` applied ← `_land_attack_packet` F(R+4) · ← `_land_dying_packet` F(R) · ← `_defer_arrivals` F(R+4) · ← `_burn_dots` F(2K+3). Hence `f_max = max(R + 4, 2N, 2K + 3)`.
* **What `q_k` counts.** At `5dfb865c…`, `_cons_add` (`:6540`) adds `max(1, n_round)` to `_cons_split[k]`, so the emitted `q_k` is a **count of flagged roundings**, not of flagged terms as § F.2k.3 words it. (L1) reads `q_k` only through the indicator `[q_k > 0]`, and a flagged term contributes at least 1 under either reading, so the indicator and β are the same. Recorded so nobody reads `q_applied = 4600` as a term count.
* **Result:** `q_applied` and `q_dropped` are > 0 on every cell, so `φ` reaches the two accumulators that receive packet and burn mass. That is the indicator gap BLOCK-1 named. `q_voided`, `q_pool_truncated` and `q_pcl_reclaim` are > 0 through S rows. `q_offered = 0` (offered has only T rows). `q_counterplay_absorbed = 0` (see § 7).

### 7 · INFO for jack-ryan's repair Gate-2 (verdict-neutral; I do not rule on the census)

**(a) `counterplay_absorbed` receives carried-chain mass and has `q = 0`.** The census classes `:3968` (`cut`) and `:3990` (`taken`) as T: the booked float is the one subtracted, and the remainder's rounding is counted downstream on `applied`. That is right for the remainder. It does not cover **the roundings already on `dmg` when it enters `_cp_absorb`**: the packet sum (R) on `_land_attack_packet` and `_defer_arrivals`, and the burn aggregation on `_burn_dots`.
* When a packet is **absorbed whole** (`d2 ≤ 0`, `:4106–4107`, `:4151–4152`), no downstream booking exists, so the carried roundings are flagged nowhere.
* When it is absorbed **in part**, the carried error scales with the whole packet, but `φ` is charged only on the landed share.

His Path-B text named flags on `counterplay_absorbed`; drax's census argues them away. **(b) The DOT_INC row (`:4638`) is a difference** `per_tick·n − inc_total`. Its rounding error scales with `mit_total`, not with `|x|` as § F.2k.3's F(f) premise (`≤ γ_f·|x|`) states. Under cancellation the per-term premise does not hold literally.

**Why neither can change H-6.** Both are covered with room to spare by `B`'s own slack: `φ = γ_{2f}` against one-sided chains of at most `γ_f`, and `Â_applied` is 126–298 times `Â_cp` on every cell. To check rather than argue, the script also prints a deliberately coarse **sensitivity bound** that is *not* the law. It charges **2φ on all seven accumulators**, which includes `counterplay_absorbed` and `offered`. Worst cell `M0·0`: **β_stress = 1.4254e-13 ≤ 1e-12 (×7.0)**, and all 25 hold. So no reclassification of these rows (cp → F(R+4), or DOT_INC charged on its full mass) can make a cell ungradeable. Whether the census should be re-classed for the record is jack-ryan's call at the repair Gate-2.


---

## 8 · WARN-2, named: a relaxation, authorised by Matt's Q92 (Discipline #12)

**Under v1.12, five cells that the retired 4,500-term budget made `UNGRADEABLE` become gradeable.** On the pass-3b runtime (godot `90a2c3c` `AGENT_STATE`, ledger KP-167), five cells had more than 4,500 offered terms. Under v1.11's clause (c) that count made each of them `UNGRADEABLE`. The offered counts are unchanged at the graded runtime:

| cell | offered terms | under v1.11 (c) | under v1.12 (L2): β | margin |
|---|---|---|---|---|
| `M0 · 0` | 6,777 | UNGRADEABLE (> 4,500) | 3.582525e-14 | ×27.91 |
| `M-POL-2-NULL · 0` | 6,777 | UNGRADEABLE | 3.582525e-14 | ×27.91 |
| `M-POL-2 · 1` | 6,616 | UNGRADEABLE | 2.248760e-14 | ×44.47 |
| `W1-NULL · 1` | 6,616 | UNGRADEABLE | 2.248760e-14 | ×44.47 |
| `W1 · 1` | 6,539 | UNGRADEABLE | 3.577962e-14 | ×27.95 |

**This is a relaxation, and it runs in the direction that admits cells to grading.** v1.12 § 0.2's sentence that the re-keying "can only produce `UNGRADEABLE`, never green" is one-sided. Clause (c) never turns a row green by itself. But these five cells now reach clause (a), and clause (a) can grade them GREEN. **Authority:** Matt's Q92, ruled "(a) Compensated sum" (KP-155), with the budget "restated only as the derivation gives it". The derivation gives no term budget (§ F.2k.5), so the budget is retired, not re-sized. What did not relax:
* clause (a)'s 1e-12 is unchanged;
* no expected value moves;
* (L2) is stricter than v1.11's clause (c) in its inputs: all seven accumulators, Σ|term| with negatives counted, lossless operands and the census.

Recorded here, as WARN-2 asks. The conductor's next ledger row should name it too.

## 9 · INFO-3, the exposure note

§ J of v1.12 says the law was "written before the numbers it will judge". That is true of the **graded** numbers: this runtime did not exist when v1.12 was committed (`a6bce6f5c`, 02:33; drax's `ab7792f`…`ada8048` came after). It is **not** true that the author was blind to the scale of the operands. The pass-3b counts were on the ledger at KP-167 before v1.12 was written: offered 953–6,777, five cells over 4,500, deepest sink 12,239 terms, final sum 6. **That exposure cannot have bent (L2).** The law has **no free constant**: `u`, the γ's, the coefficients of `B` and the 1e-12 tolerance are all fixed by the standard result and by clause (a). `φ` comes from a census rule stated in terms of emitted counters, not from a chosen number. Nor was the law tuned after these values: v1.12 is unedited (FILE `a0454776…`), and nothing in this note alters a coefficient (§ F.2k.7).

## 10 · What this note does not do

* It does not grade clause (a), and it does not start an attempt. Attempt 1 of 2 under v1.12 still waits on **jack-ryan's repair Gate-2** (R-1…R-22, the census against his WARN-1 criteria and the BLOCK-1 indicator check, G3 ×25, H-4). § 7 is offered as input to that gate.
* It changes no tolerance, no expected value, and no line of the prereg.
* It does not re-run G3, G2 or the suite. Those figures are drax's (KP-170). Only the Python half of the probe was reproduced.

## Reproduce

```
python3 agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-h6-discharge-v1.12/h6_l2_exact.py
```
Read-only on `~/Games/reincarnated-godot` (git objects at `ada8048` / `e40a4fc`). Prints the pins, the census check, the probe, and the per-cell (L2) table with drax's figures beside each row. Writes `results.json`. Exit 0 = discharged.
