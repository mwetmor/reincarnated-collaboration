# JOIN-1 · J2-E2b evidence: § 4.7 instrument v3 (Limb B′, HEAD bound at both ends), NC-J2-8

gamora, 2026-10-07. Prepared for jack-ryan's E2b Gate-2.

**Engine commit:** `b8a9b860`, committed ALONE. It contains three files:

| File | FILE sha256 |
|---|---|
| `simulation/scripts/gamora_join2_s47_v3_2026_10_07.py` | `c435500c762ee71a91bec5167297160b284fc1572f5b4a299335288991c5569a` |
| `simulation/scripts/join2_bprime_witness_hook/sitecustomize.py` | `a7943a20ba1f939fe3882d7365176d4da44426634a2564df00fcdad6df1855cd` |
| `tests/test_join2_s47_v3_bprime.py` | `027a5bb1fad6386f49197e2b0ff0beb6152a6415ddfeb58ab5192f80137ee11e` |

**Fail-first:** the unit tests gave **14 errors** before the script existed, and **14 passed** after.

Every run below was made at HEAD `b8a9b860`, with HEAD and the kc2 tree recorded at start and end and found equal (except nc8e, which moves HEAD on purpose). Command:

`PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 <script> <out> [--control ID]`

## § 4.7 at E2b: **ORACLE BYTE-IDENTICAL** (`s47v3/s47v3_evidence.json`, FILE `1b06d03f…`)

- **HEAD:** start = end = `b8a9b860`. The kc2 tree is `7496a28a` at both ends.
- **Limb A:** sealed `969fbd8d` vs HEAD. The canonical hash is `f04ef6d0…` on both sides, and the sealed tree was clean before and after.
- **Limb B:** 141 `reincarnated` modules loaded; no `kit_compiler`; nothing changed since the seal or dirty against HEAD.
- **Limb B′:** passes on every check.
  - No path or name hits in either the sealed or the HEAD child.
  - The census (29 functions; 63 values = 45 named values + 4 import-frozen defaults + 14 alias or shared-object identities; the E2b commit message says "45 values", which undercounts) is equal between the sealed and HEAD children.
  - The witness shows 2 pids, both direct children of the parent, with no hits.
  - The parent environment had no JOIN keys to strip on this run. Stripping is shown working in the nc8-0-strip control below.
- **Limb C:** 10/10 declared renames applied; the outputs are equal apart from them.

## NC-J2-8 controls

These are NON-GRADED-CONTROL runs. The HEAD and sealed children import only, and no fight is run. The predictions were committed in the script's `CONTROL_PREDICTIONS` before any evidence run.

| control | injection | observed | matches prediction |
|---|---|---|---|
| nc8-0 | none | B′ GREEN; census equal; witness 2/2 | yes |
| **nc8a** | `families.py` loaded as `reincarnated.simulation.join2_ctl_families`, plus a stand-in delegating `threat.mitigate` | **B′ RED.** Path hit on that module and on 2 opened rulebook files. Census differs exactly `['threat.mitigate']`. Witness hit on the HEAD pid | yes |
| **nc8b** (WARN-1(b)/(c)) | `import join2_rulebook` by name, through the editable install's default `sys.path` | **B′ RED.** Name hits on `join2_rulebook` and `join2_rulebook.families`, plus 4 opened-file hits. Census equal. Witness hits | yes (the opened-file hits are additional to the stated hits) |
| nc8c | `JOIN2_LEAK_CONTROL=1` put into the HEAD child, bypassing the strip | **B′ RED** on the witness env check only | yes |
| nc8d | `join1_b0n_hook` placed first on the HEAD child's `PYTHONPATH`, i.e. a foreign `sitecustomize` | **B′ RED.** `sitecustomize` path hit, and witness coverage shows 1 child of 2 expected | yes |
| nc8e | END HEAD read as `HEAD~1` (declared synthetic) | **NO VERDICT**: `b8a9b860` → `fd219ea1` | yes |
| nc8-0-strip | nc8-0 run with `JOIN2_PARENT_STRIP_CTL=1` and `JOIN1_B0N_BINDINGS` set in the **parent** environment | B′ GREEN. Both keys stripped and recorded; no child saw them | positive control (its prediction was written in the run log only, not committed beforehand) |

**What is left for later commits.** Emitter child coverage, meaning the witness hook first on `PYTHONPATH` during a J-S8 emission with 1 + 25 pids expected, is first exercised at E3, on that commit's ORACLE-half re-emission. Here the witness covers the § 4.7 script's own two children only.

**Disk:** 28 GiB free throughout.
