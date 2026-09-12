K3-chk-02 — registered Keeper idle-S only

Scope: idle_S_00.png through idle_S_07.png in K3-reg-02. Walk is absent in this registration and explicitly SKIPPED. Other directions and cast are outside this check's scope. The generic frozen runner enumerates them, but its out-of-scope envelopes are excluded from checks.json.

Master: idle_S_00.png. Input frame hashes all match the supplied registration.json. Dimensions 512x512 RGBA and atlas pivot (256,400) are registration metadata; per-frame image content and alpha>=128 measurements are evaluated by the frozen gates.

Exact measurement invocation (stdout captured as JSON; bytecode writes disabled):
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -c 'import json; from pathlib import Path; from gates import run_gates, drift48; root=Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/frames"); frames=sorted((root/"idle/S").glob("*.png")); print(json.dumps({"rows":run_gates.run(root,frames[0]),"g11":drift48.evaluate(frames,frames[4],"idle/S")},allow_nan=False))'

Exact provenance commands:
shasum -a 256 /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/frames/idle/S/idle_S_*.png /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/registration.json
cat /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/registration.json

Reporting:
- checks.json is a list of SPEC section 1 result envelopes.
- G1, G3, G9, silhouette64 and both G6 instruments preserve frozen gate results.
- G5 literal requires cast05, which is absent: passed=null. Its eight 512px adjacent-and-seam MAD measurements are reported as g5_pair_mad, with no substituted G5 comparator.
- G11 uses frame 0 versus frame 4 as explicitly registered. Frozen drift48 calls its comparator parameter cast05 and its notes field cross_cast_05; the report relabels that comparator accurately. The loop result and all eight pair values, including 7→0, are included. Per-pair booleans apply the same frozen strict less-than comparator.
- G6 literal uses minimum internal MAD; G6b uses median internal MAD. Neither is substituted for the other.
- Fresh alpha>=128 bbox/height/sole rows come from the frozen common.measure output embedded in G3. The alpha>0 bbox/height/bottom rows are the supplied registration's measurements, linked to the actual input bytes by matching SHA256. Both support conventions and both spreads are explicit.
- Alpha>=128 sole row is a support-bbox proxy, not reviewed anatomical planted-sole contact. Root/planted G2 verdicts are not inferred.
- Plate uniformity is N/A for these matted RGBA inputs.
- G9 dark-fringe numeric verdict is null: no calibrated dark_threshold supplied; localized halo absence is not established.
- Silhouette64 distances are measured, with null verdicts because no calibrated shape threshold is supplied.
- The named frozen gates do not emit PNG evidence. Seam-diff and drift-strip PNGs could not be produced within the frozen-tools-only constraint. No custom code files or renderer were created. Evidence arrays are empty.

Assembly: captured frozen JSON envelopes were scoped to idle/S, supplemented with per-pair entries and explicitly sourced registration measurements, and serialized to checks.json using the orchestration tool. This text records the exact measurement and provenance shell commands; data files were written with apply_patch. Inputs and frozen tools were not edited.

Verification command:
jq -e 'type == "array" and all(.[]; (keys | sort) == (["id","subject","passed","value","threshold","op","unit","evidence","notes"] | sort))' out/checks.json
shasum -a 256 out/checks.json out/checks_readme.txt
