# JOIN-1 · J2-E2a (W1) evidence: § 4.7 ORACLE byte-identity + J-S8 untouched

gamora, 2026-10-07. For jack-ryan's W1 Gate-2. E1-b is checked at the same sitting.

## Commits (engine)

| Commit | What it holds |
|---|---|
| `85b19164` | **W1, ALONE:** `src/join2_rulebook/{__init__,families}.py` and `tests/test_join2_rulebook_w1_families.py` |
| `fd219ea1` | **E1-b, ALONE** (document only) |

Fail-first: run before the package existed, the tests gave **1 failed, 22 errors**. After the package landed: **23 passed**.

## FILE digests

| File | sha256 |
|---|---|
| `families.py` | `024eb2fcdaf085dc9c28d9646299b0793f635b53d6715795b4d91a7a982f588a` |
| the W1 test file | `9f71e5b513faf95f642d2f4eb15e2d3fc2d25c2ccbd39b6deedd481fd8236004` |
| E1-b | `d681dc88f1980a7844658f25bc5b1c14f9203a286565276bfe8552c1086a1a97` |

## § 4.7: verdict ORACLE BYTE-IDENTICAL

- **Script:** `gamora_join1_b0n_s47_evidence_2026_10_06.py` v2.
- **Command:** `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 <script> s47/`
- **Outputs:** `s47/s47_evidence_v2.json`, `stdout.txt`, `stderr.txt`, and the two graded JSONs.

**Limb A.** Sealed `969fbd8d` vs HEAD. The canonical sha256 is equal on both sides: `f04ef6d0…`.

**Limb B.** Import closure, measured at HEAD `fd219ea1`:
- 141 `reincarnated` modules loaded.
- No `kit_compiler` module loaded.
- No file changed between the seal and HEAD.
- No file dirty vs HEAD.
- Nothing from `join2_rulebook` loads. It sits outside `reincarnated*` and nothing on the ORACLE path imports it.

**Limb C.** 10 of 10 declared renames applied, and the result is equal after those exceptions.

**Note on timing.** The run started with HEAD at `85b19164` (W1). E1-b (`fd219ea1`, a markdown file under `simulation/math/`, which no code path loads) was committed while it ran, so Limb B recorded `fd219ea1`. Both HEADs contain W1.

## J-S8 untouched

- `join1-gm-fixture-v1/oracle/manifest.json` is still `f82807fb6de68a6cee4eff69bb7028457143b4951fe9abccee94caa735c4d217`.
- `G1.jsonl` is still `eb335eba…`.
- `git diff 0b0fed41 HEAD` over the fixture directory and `simulation/kc2` is empty.
- The `kc2` tree OID is still `7496a28a…`.

## NC-J2-4b (form level)

This is the version of NC-J2-4b that W1 can carry. It was predicted in the test's docstring before the run.

- **With Fire removed from the offense half:** exactly **7,900** refusals (the Guardian of Empyrion fire row × 7,900 board rows, w151-160). The other **23,700** pairs are bit-equal to the sealed `applied_for`.
- **The silent-zero case:**
  - sealed code, `res_fire` column absent: `applied_for` passes the raw damage through whole;
  - registry, same input: refuses with `OffenseColumnAbsent`.

**What is still owed.** The in-run form of NC-J2-4b (the first Guardian fire packet refuses in 25/25 cells) needs the binder, so it runs at E3/E4.
