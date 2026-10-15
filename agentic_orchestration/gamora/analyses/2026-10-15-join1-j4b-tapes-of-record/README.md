# JOIN-1 · J4b: per-cell tapes OF RECORD (gamora, 2026-10-15)

- **Emitter:** engine `4e6ed5b3`, with failing tests `6f300c60` committed first. It used `N_OF_RECORD`, ran in the dedicated worktree under the courtesy gate, and all J4b suites passed 162/162 at that head.
- **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/j4b-tapes-4e6ed5b3/`, 300 files (25 cells × 12 streams), 402 MB. `manifest.json` sha256 is `7a6cff1b0b13a0747a3de5f6a8172e65cf12329bfccc7bfca254fc0f2423e402`.
- **Streams and N:**

  | Stream(s) | N |
  |---|---|
  | `dmg` / `potion` / `block` / `oculus` / `gethit` `:d2-fire-sorc-c14` | 20,000 each |
  | `pyre` / `softhit` | 50,000 each |
  | `gethit:warlord` | 100,000 |
  | `crit:intake` / `crit:summon` / `crit:player` / `crit:soulfire` | 100,000 each (the same law as `join2_rulebook/crit.py`) |

- **Layout:** `<arm>_s<salt>/<stream_id with ':' → '__'>.json`, in the tape_sample format.
- **Gate:** unserved == 0 means `n_no_tape == 0` AND `n_mismatch == 0` (ADDENDUM-13 CORR-3 § 5).
- **Superseded:** the provisional set `j4b-tapes-provisional-1960d961`. It has older N values, no crit tapes, and the same seeds.
