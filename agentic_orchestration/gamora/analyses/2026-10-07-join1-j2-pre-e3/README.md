# JOIN-1 · J2 pre-E3 evidence: the E2c/E2e Gate-2 owed items (KP-328)

gamora, 2026-10-07. Finding: collab `f24a93b93`. jack-ryan checks these as a delta at E3's Gate-2.

## Engine commits, each ALONE

| Commit | Contents |
|---|---|
| `6626f664` (INSTRUMENT) | `gamora_join2_s47_v4_2026_10_07.py`, `join2_bprime_witness_hook_v2/sitecustomize.py`, `tests/test_join2_s47_v4_warn12.py`. Fail-first: 4 new tests failed against the committed instrument; now 22 passed, or 35 including v3's B′ tests |
| `b5a01125` (FORMS) | `src/join2_rulebook/{families,forms,hooks}.py`, `tests/test_join2_rulebook_e2c_forms.py`. Fail-first: 3 new tests failed; now 28 passed, or 51 including W1's |

## What changed

- **BLOCK-1:** `fingerprint()` follows `__wrapped__` only for a non-function wrapper (the sealed `lru_cache` loaders). A plain function or method is fingerprinted as itself. `has___wrapped__` is part of the fingerprint, and a function wrapper's inner object goes under `wrapped`.
- **WARN-E2e-1:** `pin_status()` checks every instrument file at START and at END: tracked, clean, and `hash-object` == `rev-parse HEAD:path`. A failure gives NO VERDICT. Limb B's exclusion now removes only the "changed since the seal" clause, and records the blob. `WITNESS_SHA` is the sha256 of the **committed** blob.
- **INFO-E2e-1:** the witness records opens of **any** extension under the forbidden directories (`opened_forbidden`), and the checker reads them. `FORBIDDEN_DIRS` is asserted equal to the script's list. Import-event *file* hits are not cited as an independent limb (INFO-E2e-2).
- **WARN-E2c-1, route chosen:**
  - `summon_applied` takes the SEALED `applied_damage` captured at `bind()`, so a summon physical packet never reaches an installed row-5 form.
  - Refusals now name their lane: `player->monster/summon` and `player->monster/player-stream`.
  - Tested: with row 5 installed and `registry_without('Physical')`, a summon physical packet refuses naming the summon lane, and row 5 is called 0 times.
- **Corrigenda:**
  - L-11 is re-attributed as gamora's PROVISIONAL default.
  - L-17's ratification venue is J4b.
  - The E2c test count is 25. The corrigendum is appended to the E2c README.
- **INFO-E2c-2** (row 16 installed as `staticmethod`, parity checked through an instance) belongs to E3's installer.

## § 4.7 at `b5a01125`: **ORACLE BYTE-IDENTICAL** (`s47v4/`)

- **HEAD and pin:** HEAD fixed; instrument pinned at start and end.
- **Limb A:** `f04ef6d0…` equal.
- **Limb B and B′:** both pass. B′'s census is equal under the fixed fingerprint; exact s47 tree.

## Controls at `b5a01125` (`controls/`; predictions committed in `6626f664` before these runs)

| control | observed | matches prediction |
|---|---|---|
| nc8f | census differs `['threat.resolve_hit']`; witness fingerprint hit only | yes |
| nc8g | census differs `['threat.probability_to_hit']`; witness fingerprint hit only | yes |
| **nc8h** (`functools.wraps` delegate on `mitigate`) | census differs exactly `['threat.mitigate']`; path GREEN; witness fingerprint hit on the HEAD pid only | **yes. BLOCK-1's control is RED** |
| **nc8i** (comment-only dirty witness edit) | `instrument_pinned` False → NO VERDICT; B′ RED, with a `sitecustomize` sha hit in **both** children; census equal; the witness file restored (`status --porcelain` empty afterwards) | yes |

**Known label imprecision.** A control report prints the shared `NO_VERDICT` constant, whose text reads "HEAD moved during the run". For nc8i the cause is in `head.instrument_pinned = false`; HEAD did not move. The non-control verdict path reports the right reason. The label will be corrected at E3's instrument touch.

Disk: 33 GiB free.
