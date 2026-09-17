# Gate-1 re-check — 2026-09-17 — Run C-6 charter v1.2

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 re-check)
**Verdict:** **PASS-WITH-WARNS.** BLOCK-A and BLOCK-B are **discharged on substance** — I re-verified the machinery independently, not on assertion. What remains is **one incomplete value-set sweep with seven hits**, plus two instrument notes and one record-staleness note. None requires judgment; all are text or one-line asserts.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-17-necromancer-run-C-6-charter.md` v1.2 (`sha256[:12] aad5223123c8`), commit `2b315384`
**Continues:** `agentic_orchestration/qa/findings/2026-09-17-run-C-6-charter-gate1.md` (v1.1, BLOCK — narrow)
**Disciplines cited:** **#72** (value-set sweep law — mechanical enumeration), #73, #75 cl. 6 · desirable-run-pattern § 1, § 5

---

## 1. BLOCK-A — **DISCHARGED**, and I verified the artefact rather than the claim

The § 1 lane-tools row now reads *"C-5-owned, LIVE; pinned by sha at every wave, not at launch"*, enumerates the consumed subset, cites the twelve-freezes-in-five-hours evidence, routes mid-run movement to § 7.7, and pins predicate 4 to one recorded sha. § 7.7 states the disposition rule with *"silence is not a disposition"* in terms. Predicate 5 now requires `matrix.html` to carry **the MANIFEST sha each cell was cut under** and any attribution boundary — which converts the remedy from a promise into a checkable artefact. That is the right shape.

**Independently verified** — `astra_test_01/burst/runs/C-6/consumed_shas_at_go.json`:

| check | result |
|---|---|
| `manifest_sha256` | `560e6205…` — the **current** value, not the stale `c8745186…` pin |
| `consumed_tool_paths` | **22** entries (all 19 `oracle/*.py` + `bands_proposed.json` + `export/godot_import.py` + `export/sockets.py`) |
| `consumed_c3` | 11 entries (the copied conductor scripts + `matrix_questions.json`) |
| `c3_cells_v7` | 41 dirs + a `numbers+registration` tree sha `aa28ae59…` |
| `pinned_scene` | `runs/C-5/cliffside_v40` |
| `missing_from_manifest` | `[]` — every consumed path is inside the freeze, so all 22 are pinnable |
| **my own re-hash of every file entry** | **33 of 33 byte-identical, 0 mismatches** |

The enumeration is **mechanical and broader than the charter's prose** (§ 1 names nine `oracle` files *"incl."*; the JSON carries all 22). That ordering is correct per #72 — the instrument output is the authority and the hand list is checked against it, not the reverse. All twelve paths I spot-named exist on disk.

## 2. BLOCK-B — **DISCHARGED on the predicate and the method**

Predicate 3 now carries one rule and states the retirement in terms: *"**No staff rule is reused**: the FL-1a/FL-5 far-tip-along-facing rule is falsified 3/8 (C-5 `F-C5-41`) and FL-5b's ferrule discriminator / hands-centroid fallback do not transfer to a two-handed haft with a blade and a butt-spike."* The script **proposes** (blade-mass extent, haft axis excluded), the **sheet is the authority**, coordinates are `conductor_derived: true` with the script sha in the ledger, and the exporter socket schema is re-read at P5. § 4 P4 matches. § 8 carries the conductor-script rule and names the C-3 Gate-2 item-4 debt as **not discharged**. This is exactly what I asked for, including the part I did not ask for — the reason the staff rules were rejected is preserved rather than deleted, so the next reader learns why.

**But the sweep did not reach § 4 P5** — see WARN-R1, which is the only reason this is not a clean PASS.

## 3. WARN-R1 — the fold changed three values and left seven restatements un-swept (**Discipline #72**)

Three values moved in v1.2: *frozen → live*, *far-tip rule → blade inner curve*, *latest staging → pinned v40*. § 1, § 2 and § 7 were folded; **§ 3 and § 4 were treated as summary surfaces and not swept.** Mechanical enumeration (`grep -n -i` on the charter, pasted, not eye-curated — #72's own clause):

| line | § | residual text | value it restates | severity |
|---|---|---|---|---|
| **56** | **§ 4 P5** | *"`sockets_v2.json` (blade socket, **far-tip rule**, marked audit sheet)"* | the rule predicate 3 just retired | **must fix before P5** |
| 41 | § 3 | *"audited like **FL-5 Part B**"* | same | fix |
| 42 | § 3 | *"the real cliffside scene (**latest** C-5 staged project)"* | § 1 pins v40 | fix |
| 10 | § 1 | heading *"Bounded substrate (**frozen at launch**)"* | the heading BLOCK-A named | fix |
| 3 | header | *"same lane, same **frozen** T3 tools, a second character"* | the falsified lineage claim | fix |
| 55 | § 4 P4 | *"PACK with the **frozen** T3 tools"* | same | fix |
| 76 | § 7.1 | *"The **frozen** tool tree … C-6 consumes the current **freeze**"* | same | fix |

*(Not residuals, correctly retained: line 17's "C-5 re-froze…" and "C-5 freezes; C-6 never re-freezes" describe C-5's behaviour; line 45's "freeze + re-freeze in-run" is C-3's column.)*

**Why line 56 is called out separately.** § 4 is the operational sequence — it is what a conductor reads to execute a phase — and P5 is the phase that **authors `sockets_v2.json`**. A conductor working § 4 top-to-bottom reads *"far-tip rule"* at the exact moment the rule matters, and it contradicts predicate 3 three sections earlier. That is the defect BLOCK-B existed to prevent, surviving in the one surface where it can still act. I do not re-BLOCK, because predicates govern, § 2.3 is unambiguous and emphatic, § 4 P4 (where the landmark method operates) is correct, and the fix carries zero judgment — but **line 56 is a pre-P5 obligation, not a tidy-up.**

**Edit:** the seven cells above, and nothing else. § 1's heading becomes *"Bounded substrate (enumerated at launch; the tool tree is C-5-owned and live)"*; line 56 becomes *"(blade socket per predicate 3, marked audit sheet)"*.

This is #72's founding shape and its fourth recorded instance of the family: a landing fold that corrected the surfaces it was looking at and walked past the ones that merely restate. The charter is the right place for it to be caught, and a grep is what catches it — which is why the law says the enumeration must be mechanical.

## 4. INFO findings

- **INFO-R1 — `clips_seq2.sh` still binds the wave log to a hard-coded session scratchpad UUID.** The C-6 copy is re-pointed (`~/astra-burst/grok/C-6/`, C-6 `grok_clip.sh`, C-6 `cl.py`, first-failure stop, certain-cause branch → `HALT-P3-grok-budget.md` + a `halts` ledger entry) — WARN-3 is otherwise cleared and cleared well. But `S=` is a literal session path, and **only the conductor can confirm it is that session's**. Blast radius is bounded and worth stating: the HALT packet path and the `cl.py` call are absolute repo paths, so a wrong `$S` loses the *log*, not the HALT. **Edit:** one line at the top — `[ -d "$S" ] || { echo "scratchpad missing"; exit 1; }` — asserted at P0 rather than assumed. #75 cl. 6: a re-pointed instrument is not a verified instrument.
- **INFO-R2 — the HALT ledger write can lose the entry the packet survives on.** `clips_seq2.sh` interpolates the Grok error into a JSON string literal after `tr -d '"'`; a backslash, newline or brace in the provider's message yields invalid JSON and the `halts` entry is dropped while `HALT-P3-grok-budget.md` is written — the record failing to follow the state (#73), on the one event F7 makes the run's only budget stop. **Edit:** build the JSON with `python3 -c 'import json,sys;print(json.dumps(...))'` or pass the cause on stdin.
- **INFO-R3 — F8/F9 are now OPEN Matt-gated forks and the account's gate line is stale.** The ARCHITECT table in `2026-09-17-c6-account.md` still reads *"No OPEN Matt-gated fork remains"*; two now do. **Proceeding on (a) pending his word is legitimate for both** and I endorse it: F9(a) is self-executing, costs one discarded clip, and its failure mode is the HALT it was written to find; F8(a) can only *add* a pause on Matt's own eye, never skip it, and the 24-h no-red-flag default means it cannot deadlock the run. **Edit:** stamp the F8 and F9 rows **"OPEN — Matt"** in § 5 so their bold **(a)** is not read as ruled alongside F1–F7, and refresh the account line.

## 5. The deviation put to me — **RATIFIED**

**`~/astra-burst/.heavy.lock` instead of `astra_test_01/burst/.heavy.lock`.** I asked for the lock in the lane tree; the conductor moved it out and gave a reason. The reason is better than my original:

- The lane tree is **C-5-owned** (§ 7.1) and is a **shared working tree with live sessions**. Putting a new untracked file in it adds a path that `git add -A` would sweep — the hazard CLAUDE.md names four times and that C-3 already demonstrated with an untracked `.ledger.lock`. Keeping it out of the repo removes the exposure instead of managing it.
- `~/astra-burst/` is **already the lane's established out-of-repo working area** — C-3's Grok output lives at `~/astra-burst/grok/C-3/` and this charter points C-6 at `~/astra-burst/grok/C-6/`. It is host-level, which is the correct scope for a lock arbitrating two processes on one Mac. Verified present.
- I read `heavy_lock.py`. It is **fail-closed**: `LOCK_EX|LOCK_NB` first, and on `BlockingIOError` it prints the holder and then **blocks** on `LOCK_EX` rather than proceeding. `L.parent.mkdir(exist_ok=True)` removes the first-call failure. `fcntl` locks are released by the kernel when the fd closes, so a `kill -9` cannot leave a deadlock — which is what makes the charter's *"a dead pid is stale by definition"* true rather than aspirational.

The only cost is invisibility to `git status`, and § 7.2 plus `FOR-C-5-CONDUCTOR.md` both name the path. **Ratified as an improvement on the finding it answers.**

## 6. Credit

- `runs/C-6/FOR-C-5-CONDUCTOR.md` is a real two-sided filing, not a gesture: three asks, each scoped so nothing lands on C-5's work, and it closes with what C-6 will *never* do. WARN-6/8/9 are discharged as far as C-6 can discharge them — recording it in C-5's ledger is C-5's act and correctly not claimed here.
- Predicate 6 (`repeatability.json` vs C-3) and the fell-out sentence close the § 6.3 rubric-law gap by **adding an instrument** rather than by narrowing the intent sentence, which is the harder and correct direction.
- Predicate 2 now states its own sliver — *"≤ 12 of 40"* — on the row. A predicate that declares its coverage is worth more than one that quietly has it.

## 7. Action summary

- [ ] **gandalf, before P5 (line 56) and at convenience (the other six):** the WARN-R1 sweep table.
- [ ] gandalf: INFO-R1 `$S` assert · INFO-R2 JSON-safe HALT ledger write · INFO-R3 stamp F8/F9 "OPEN — Matt", refresh the account's gate line.
- [ ] **Matt:** F8 and F9 (unchanged from the first finding's escalations — the P2 eye-gate and the Grok balance). The run may proceed on (a) for both pending his word.

**ADR-002:** all gandalf items are charter text and within-lane conductor tooling — mine to approve, approved.

**Gate-1 re-check verdict: PASS-WITH-WARNS.** Run C-6 is **GO** on R-C6-6. The v1.2 fold answered both BLOCKs with checkable artefacts rather than assertions, and I verified 33 of 33 consumed-path hashes myself. The one thing it did not do is sweep its own summary surfaces — which is the law's own founding failure, caught here at the cheapest possible moment.

## 8. References

- `agentic_orchestration/gandalf/notes/2026-09-17-necromancer-run-C-6-charter.md` (v1.2, `aad5223123c8`, `2b315384`)
- `astra_test_01/burst/runs/C-6/consumed_shas_at_go.json` (22 tool + 11 C-3 + cells_v7 tree + pinned scene; 33/33 re-hashed clean)
- `astra_test_01/burst/runs/C-6/FOR-C-5-CONDUCTOR.md` · `runs/C-6/conductor_scripts/{heavy_lock.py, clips_seq2.sh}`
- `agentic_orchestration/qa/findings/2026-09-17-run-C-6-charter-gate1.md` · `agentic_orchestration/gandalf/notes/2026-09-17-c6-account.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #72, #73, #75 · `operating-procedures/desirable-run-pattern.md` § 6.5

— jack-ryan, Gate-1 re-check, 2026-09-17
