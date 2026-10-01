# KC2-PLAY · T-A PREREGISTRATION **v1.13**: `TA-X-16` RESTATED PER WAVE PLAYED (Matt Q96.1) · `TA-X-08` IDENTITY 2 RESTATED WITH THE SEAL'S CONTROL TERM (Matt Q96.4) · KEEP 1 ATTEMPT (Q96.2) · THE 28-ROW PRE-ATTEMPT READ IS A PRECONDITION (Q96.3)

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.13, authored 2026-10-01. SUPERSEDES v1.12 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix. The document is dated 2026-10-01.)*
>
> ⚑ **ALL FOUR PARTS OF Q96 ARE RULED (Matt, ledger KP-182 / KP-183), AND THIS FILE CARRIES THEM:**
> * **Q96.1 — "Per played wave."** `TA-X-16` is restated per wave played (§ F.2m).
> * **Q96.2 — "Keep 1 remaining."** The cap is **`1` OF `2` REMAINING**, carried from v1.12 (§ G.1). The next graded run
>   is **v1.13 attempt 2 of 2 (overall attempt 3), the last under the cap.**
> * **Q96.3 — "Yes, as a precondition."** Before attempt 2 fires, all 28 graded rows are read off the candidate build's
>   emission; the expected values and tolerances are frozen **in this file**, before the read (§ G.1a).
> * **Q96.4 — "Add control term."** `TA-X-08` identity 2 is `n_channelling + n_released + n_control_suppressed_channelling = D`,
>   with **`n_released` on D** and **a doubly-suppressed tick counted as released** (gamora's two sub-choices, accepted) (§ F.2n).
>
> ⚑ **THE PACK DOES NOT MOVE AND THE ORACLE DOES NOT MOVE.** v3.7.1, model PACK and reference PACK as v1.12; engine HEAD
> `22cd2288`, no tracked modification under `simulation/kc2`, `export` or `simulation/scripts`. **Every pin v1.12 carries
> was recomputed by script for this version and reproduces** (PINS). **drax's v1.13 counters are re-pinned at their runtime
> (godot `05508a0`)** from git blobs (§ PINS.2).
>
> ⚑ **TWO EXACT ROWS ARE RESTATED, AND BOTH RESTATEMENTS ARE DERIVED FROM THE ORACLE'S LAW, NOT FROM PORT OUTPUT.**
> * **`TA-X-16`**: from `n_pool_picks == 47` over ten waves to a per-wave law over the waves the cell plays, with the
>   vector **derived by script from `waves.json`** (47/54 as its checksum) and pinned here (§ F.2m).
> * **`TA-X-08` identity 2**: from `n_channelling + n_released = D` to the seal's own two-instrument form,
>   `n_channelling + n_released + n_control_suppressed_channelling = D`, with `n_released`'s population **stated: D**
>   (§ F.2n).
>
> ⚑ **BOTH WERE CHECKED ON THE ORACLE'S 25 REFERENCE REALISATIONS BEFORE COMMIT, AND BOTH PASS 25/25**
> (§ F.2m.4, § F.2n.4). The texts they replace fail on the same traces (`TA-X-16`: 0/25; identity 2: 6/25 pass, 19/25 fail),
> exactly as KP-177 and KP-180 found. **No tolerance moved. No expected value was set from a port number.** jack-ryan's
> KP-180 shortfall table and drax's KP-180 oracle-side counters are printed beside the measurement as cross-references;
> both equal it 25/25 and set nothing.
>
> ⚑ **THE ONCE-PER-VERSION LAW (a) AUDIT (KP-178) WAS RUN ON THIS TEXT** (§ K): every EXACT row the oracle can be measured
> on was measured on the 25 reference traces and passes; every other row is cited with its basis. **The oracle passes
> every EXACT row of this file on its graded arms and window.**
>
> ⚑ **ATTEMPT 1 (v1.12) IS NOT RE-GRADED.** It stands `STRUCTURAL` on `TA-X-08` (a genuine port defect, 25/25) regardless of
> `TA-X-16` (jack-ryan, 347ce2e1e, Item 1; KP-178), and it stays on the record, spent.
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN OR THE § G.1a READ EXISTS AGAINST IT IS A HALT TO
> MATT (`WARN-16`).** ⚑ **D4 HELD: committed ALONE, with zero code.** It was made from gamora's draft (collab `0b2fceb06`,
> conductor KP-181) by its § Z procedure; the draft folder `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-prereg-v1.13-DRAFT/` holds the
> instruments that filled every digest and measured number here (none typed).
>
> **Authority:** Matt, Q96.1–Q96.4 (KP-182, KP-183); KP-177 … KP-181; jack-ryan 347ce2e1e and ea0317306. **Carried from
> v1.12 without change:** Q83(b), Q85, Q87, Q91, Q92 (a), KP-115, KP-127, KP-131, KP-132, KP-137, KP-144, KP-146, KP-149,
> KP-150 … KP-155, KP-167, F5, the `C-o` / `C-p` ceilings.
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY. **Decision rules only. NO BAND WIDTH IS MINTED, AND EVERY
> WIDTH IN `P-a` STAYS VOID.** v1.12 (`a0454776…`) and every earlier version are NOT edited.

---

## § 0 · ⚑ THE v1.12 → v1.13 DELTA

**Legend** (v1.12's, plus one): **CARRIED** · **RE-KEYED** · **OPERATIONAL** · **NOTE** · ⚑ **RESTATED** = the row's statistic
is re-written by Matt's ruling after a graded run exists (KP-137; v1.8 § F.2d; here Q96, KP-182/183), derived from the oracle's law and checked on
the oracle's reference realisations before commit (KP-178 law (a)).

### 0.1 · Preconditions

| id | v1.13 | Δ value | why |
|---|---|---|---|
| `P-1`, `P-3`, `P-4`, `P-5` | **CARRIED** (pins recomputed; reproduce) | none | — |
| `P-2` stream disjointness | ⚑ **OPERATIONAL** (§ B.3a): what "a zero-draw no-op fold inserted" requires, and the digest's domain (zero-draw site = absent site). Criterion *"digests identical"* unchanged | none | grade § 2.2; jack-ryan 347ce2e1e INFO-5, ea0317306 INFO-2/INFO-3. **Discipline #12: an operational reading, not a criterion change** |

### 0.2 · EXACT rows (28) and the declared row

| id | v1.13 | Δ expected value | Δ tolerance | note |
|---|---|---|---|---|
| `TA-X-01`, `TA-X-03` … `TA-X-05` | **CARRIED** ⚑ + **OPERATIONAL**: the digest law (zero-draw site = absent site) is printed for them, since one function (`cell_digest`) now serves P-2 and these rows (§ B.3a) | none | none | jack-ryan ea0317306 INFO-3 |
| `TA-X-06` | UNGRADEABLE-declared, closed at exactly `["TA-X-06"]` | — | — | carried |
| `TA-X-07` | **CARRIED** (clause (c) = § F.2k (L2), unchanged) | none | none | — |
| ⚑ `TA-X-08` | ⚑ **identity 1 CARRIED; identity 2 RESTATED** (§ F.2n): `+ n_control_suppressed_channelling`; `n_released` on D, with its population closed by an emitted counter. ⚑ **The census convention made OPERATIONAL** (§ F.2o): the lethal tick is censused alive; one PRE_FIGHT per wave played | identity 2's left side gains a term; no number moves | none (exact) | **Matt Q96.4, "Add control term" (KP-182).** Discipline #12: semantic restatement, named |
| `TA-X-09` … `TA-X-15` | **CARRIED** | none | none | — |
| ⚑ `TA-X-16` | ⚑ **RESTATED PER WAVE PLAYED** (§ F.2m): picks(w) = V11-P06-1[w] on every wave played; `n_pool_picks` = the sum over those waves; `n_spawn_point_6_keys_rolled == 0`; a per-wave filtered-key counter at **key grain**, graded | 47 → Σ over waves played (= 47 exactly on a cell that clears w160) | none (integer) | **Matt Q96.1, "Per played wave" (KP-183).** Discipline #12: declared window → realised window, named |
| `TA-X-17` … `TA-X-30` | **CARRIED** | none | none | `TA-X-23` struck, retired |

**No row added or removed. 28 EXACT rows, the same 28 as v1.12.** Tolerances changed: **none**. Expected values changed:
`TA-X-16`'s constant 47 becomes a per-wave vector whose full sum is 47; `TA-X-08` identity 2 gains a term. **Neither was
fitted: both are read off the oracle's law and then checked on the oracle's own realisations.**

### 0.3 · Configuration, instruments, report face, verdict file

| site | v1.13 | why |
|---|---|---|
| § C.9 G3 | ⚑ **C.9.5a added:** the port's player census equals the oracle's own `actor_state._player_rows` count, and the port's `n_control_suppressed_channelling` equals the oracle trace's count of control `channel` entries on leg A, per cell. **An attempt precondition, not a graded row** (Discipline #12, named) | KP-179 already measures the first; the second is what makes identity 2's new term tested where the port's own generator cannot reach it (§ F.2n.5) |
| § G.1 | ⚑ **`1` of `2` remaining, carried** (Matt Q96.2, "Keep 1 remaining") | the attempt-1 spend was honest (a genuine port defect) |
| § G.1a | ⚑ **NEW: the 28-row pre-attempt read is a precondition** (Matt Q96.3, "Yes, as a precondition"); procedure and seat written | KP-178 law (c) |
| § G.3 | `prereg_version: "v1.13"`; new `ta_x_16` and `ta_x_08` blocks | § G.3 |
| § H | re-listed for attempt 2 | — |

### 0.4 · What v1.13 deliberately does NOT do

1. **It does not re-grade attempt 1.** v1.12 attempt 1 stands `STRUCTURAL`, spent.
2. **It reads no candidate (port) emission as a graded or expected value.** Every expected value in it is the oracle's or the
   pack's. drax's KP-180 G3 evidence is read only for the § C.9.5a precondition and as a cross-reference (§ PINS.2).
3. **It does not decide anything left to the gates:** H-2 … H-8 (§ H) are owed after commit.
4. **It does not fold KP-144 (b) / OQ-14, OQ-15, `C-h`/`OQ-9`, `C-k`/`OQ-11`, C-11b, REFERENT-v2** (carried open, as v1.12).

---

## ⚑ PINS: EVERY PIN v1.12 CARRIES, RECOMPUTED BY SCRIPT; NONE TYPED

> **The standing rule (KP-20, KP-43).** `pins_v1p13.py` recomputes each pin and asserts it equal to the value it
> **extracts** from v1.12's text (by the row the value sits on), so no carried digest is typed anywhere. The packs are
> recomputed with the manifests' own law, every member checked for digest and bytes, the on-disk member sets checked
> equal to the manifests', and the cross-pin checked. The set digests are recomputed through the oracle (`pool466`,
> `load_profiles` under `a8` `IC7-A-0453`'s call, `derive_oracle_speeds`). `TA-X-18` is recomputed on the oracle's own
> `SpawnStructureFold.offset`. The `a8` ROWSETs and the `setup` partition are re-derived from the pack. **The sealed
> cells are hashed only (K-7).** The table below is written into this file by `fill_draft.py` from `pins_v1p13.json`.
>
> ⚑ **Re-run at commit:** this table is the output of the run made immediately before this file was committed.

<!-- FILL:pins -->
| pin | label | **sha256 (recomputed by `pins_v1p13.py`)** | v1.12 → v1.13 |
|---|---|---|---|
| 933b438 G3 oracle tool (READ, lineage) | FILE | `49a044edf2ef2ccefd5987d00707835e5bf21c7ee6436792de60d65b10b1b7d9` | reproduces v1.12 |
| 933b438 G3 port tool (READ, lineage) | FILE | `574facb33a381939cf1254eacb0a82b202829e1d1cb772a3145b624094401d74` | reproduces v1.12 |
| 933b438 kc2rt_fight.gd (READ, lineage) | FILE | `2277cc8940d2c50cde5d819545e4ffe5cfbc2207c8f38cfbfe85e37703190303` | reproduces v1.12 |
| 933b438 kc2rt_laws.gd (READ, lineage) | FILE | `c234376e9cbadc2d6f69549966112ec4fc1da7df46069831c7f1b80e3f581a9c` | reproduces v1.12 |
| FALLBACK-158 | ROWSET | `e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb` | reproduces v1.12 |
| H-10 run v3.7 | FILE | `ff81fc9146e86be6c9fc5ad233ef8841ca22feb1bb50f7e9d5667d9beee85e30` | reproduces v1.12 |
| H-9 M-POL-2 | FILE | `2aedf43f2091d0c575af1d7d07deb0278be87f0b4c917efa5c33d01e77707f61` | reproduces v1.12 |
| H-9 NOTE | FILE | `90717b83926f06b5939a48c01c0cc4973d5f20d7d7eb60007b976d01ebde53e5` | reproduces v1.12 |
| H-9 W1 | FILE | `c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff` | reproduces v1.12 |
| H-9 W1-NULL | FILE | `90b9ea619e8adfd3f8532cc55e16990c15348dd537071c5758000c2edafdf801` | reproduces v1.12 |
| H-9 script | FILE | `eede32e85f362b5d57b136b81344cae1bfd4b804515db2d6f2d66279d1920f55` | reproduces v1.12 |
| NONSWING-10 | ROWSET | `00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10` | reproduces v1.12 |
| P-a | FILE | `1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9` | reproduces v1.12 |
| P-b | FILE | `d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f` | reproduces v1.12 |
| P-c | FILE | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | reproduces v1.12 |
| P-d | FILE | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | reproduces v1.12 |
| P-e | FILE | `4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73` | reproduces v1.12 |
| P-e' | FILE | `27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc` | reproduces v1.12 |
| P-h model PACK | PACK | `48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96` | reproduces v1.12 |
| P-h2 reference PACK | PACK | `1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1` | reproduces v1.12 |
| P-i | FILE | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | reproduces v1.12 |
| P-j | FILE | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` | reproduces v1.12 |
| P-k | FILE | `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` | reproduces v1.12 |
| P-l.c11a | FILE | `4af38999ff0544cc9607b34da4fde29fe2c55324e9829894c516cd9837689445` | reproduces v1.12 |
| P-l.c11aA | FILE | `17a068fe980869e6e344fdf3a652dc275f5cc3a3d65818f2976fe94084d48666` | reproduces v1.12 |
| P-l.c2 | FILE | `b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7` | reproduces v1.12 |
| P-l.c7 | FILE | `072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f` | reproduces v1.12 |
| P-l.nine | FILE | `2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd` | reproduces v1.12 |
| P-l.q91 | FILE | `d68561d59723c3295da3f0456f2fbeaefe8f5f0a30b41d29b5ff0e366966a385` | reproduces v1.12 |
| P-l.q91a | FILE | `b9ada804e17c01b376e64e82b7e45f66a344d1fc2fc75a0fdd1fd76c56e2cddc` | reproduces v1.12 |
| P-l.upn4 | FILE | `787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf` | reproduces v1.12 |
| P-l.upn5 | FILE | `bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7` | reproduces v1.12 |
| P-l.upn5A | FILE | `5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6` | reproduces v1.12 |
| P-n.1 | FILE | `f33ce0c0cbeb00bbed7b47a6f7660f20d4aa2be1694f9f4e2486e37d27b553e2` | reproduces v1.12 |
| P-n.2 | FILE | `cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960` | reproduces v1.12 |
| P-n.3 | FILE | `b6c9e7953f5b5632ec2dc51c2c8602461aef15d4721f69432444e6f777e1141e` | reproduces v1.12 |
| P-n.4 | FILE | `ad018b78a7f85491020a237166af797845bb5de2e562816673fbf925bb41ff1e` | reproduces v1.12 |
| P-o | FILE | `749d58f45eb312e7a284734a1844f2aabcfd69b7219dd1dafc55e4bb6d64792f` | reproduces v1.12 |
| POOL-466 | ROWSET | `33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b` | reproduces v1.12 |
| POST M-POL-2 | FILE | `691ea754633b5ad582c01beb69b0935ef390c803136a76d7b7d6129277423689` | reproduces v1.12 |
| POST M-POL-2-NULL | FILE | `c856f83259ca7ea62a0189031e7bd5a47a9bcba66e441da7fb8e55783a0f1f7f` | reproduces v1.12 |
| POST M0 | FILE | `9cdbd93ca8ca7d35cf39a95ea66eaf9509a89cd430a9f8d415fac4bc7fb7c2fb` | reproduces v1.12 |
| POST W1 | FILE | `a6df79289abe349b7e62e6465b749fea26e35107552348bdd9cfe634258d6b32` | reproduces v1.12 |
| POST W1-NULL | FILE | `c08fd789a5787bc5660197d90413e7ff6da7868a30a552ec4203a867b5494b59` | reproduces v1.12 |
| SWING-456 | ROWSET | `706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0` | reproduces v1.12 |
| TA-X-09 nine vectors | ROWSET | `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78` | reproduces v1.12 |
| a8 M-POL-2 | ROWSET | `e698d5f555a37fcc12e703343286d4e25c12662d8cd35c9571f9a0ac8ae45dbf` | reproduces v1.12 |
| a8 M-POL-2-NULL | ROWSET | `4393a14b56a97960ef42e73909a1cdefc49f3dc1a4cc41e7f20267b661a1a7b6` | reproduces v1.12 |
| a8 M0 | ROWSET | `68549af0608cb9979771fcc4955ae8010f4f3516ad55a97b83922c994f571d12` | reproduces v1.12 |
| a8 W1 | ROWSET | `5188284d198c139422276e8ac92f9a0bee03cea7dbb1cea32c6c7bf1d19a55e8` | reproduces v1.12 |
| a8 W1-NULL | ROWSET | `b2abff6978105bfc1566d678d5f1dea756ea9ef0eab02f8457821f81125a7fdd` | reproduces v1.12 |
| a8 WALK | ROWSET | `63c530edd2e825c05f0f95ce2f629d56dbff98da206ddb45690fc129d7bba0f2` | reproduces v1.12 |
| a8 setup | ROWSET | `c01d1ddaa4a5b7074203662522276a24a150312d9faeceb6634dc5438e0f71f1` | reproduces v1.12 |
| closure instrument | FILE | `e5793c281aa86e18e128983883ee8f26d5e5615e6803a1cf682dc49f13a57284` | reproduces v1.12 |
| discrimination audit | FILE | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` | reproduces v1.12 |
| divergence register v0.3 | FILE | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` | reproduces v1.12 |
| fae29ec kc2rt_fight.gd (lineage) | FILE | `41310e5e5330b3e0e186090dcb4ffb91481da71bebc2b2a3a482e490d9d7c148` | reproduces v1.12 |
| ffb454e kc2rt_fight.gd (lineage) | FILE | `e6903095b6bba83f38359a654380cb5b13516c8e2a437b2a04ae1ff73c72a680` | reproduces v1.12 |
| ffb454e kc2rt_laws.gd (lineage) | FILE | `406ffeca427bf90bb6b998eba834138eb7f68b76917f95e70fabf72ba523e1b3` | reproduces v1.12 |
| grade of record | FILE | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` | reproduces v1.12 |
| model manifest.json | FILE | `be5d256609d3caa231abcbe6fa042fedfa381035c3bea5c219ab5f54ca7717b9` | reproduces v1.12 |
| model/ai_states.json | FILE | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | reproduces v1.12 |
| model/arena.json | FILE | `15078b583364bd1953d8d9480f95a1194a2b01ba8915d87fa9f83dde6e6d75be` | reproduces v1.12 |
| model/config_of_record.json | FILE | `136f3a2072c0f99c8a03a61b1e2ac804d43af3396f588401f9284a5b47412d11` | reproduces v1.12 |
| model/controllers.json | FILE | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | reproduces v1.12 |
| model/input_closure.json | FILE | `13be3550f65ef9b57f14ddee26c43b94296862fe94d221847bdc02c8e22e1b4f` | reproduces v1.12 |
| model/input_closure_v3p7p1.json | FILE | `d1b759800a5709d09170a956c5dea759d80bf69e51a30781db7d16a78e49aadb` | reproduces v1.12 |
| model/math_rules.json | FILE | `3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d` | reproduces v1.12 |
| model/meta.json | FILE | `8fe51d80bd07328ef8ae98c8389f0808062f2059ea5b3139ad725a3c721c2e1b` | reproduces v1.12 |
| model/monster_defense.json | FILE | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | reproduces v1.12 |
| model/monster_kinematics.json | FILE | `b8b1c7b4e491aeb13981b26478c12190ec7efd892eddeeb6eef572f1766bc549` | reproduces v1.12 |
| model/monster_offense.json | FILE | `fad592f5cb1d10030ca4ddd5788f65d3e01c0fc5781a75b73e50693d5f9ea76b` | reproduces v1.12 |
| model/monsters.json | FILE | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | reproduces v1.12 |
| model/player_kit.json | FILE | `2b68af939b6c795c1b4c9f0411aa037fb4d0332f983fa942aa307c85329eeac6` | reproduces v1.12 |
| model/projectiles.json | FILE | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | reproduces v1.12 |
| model/provenance.json | FILE | `1d06e08a1744c8df7e188725f2c2bc5cdbbdf4d1007e75dba01a33fc9f8a0710` | reproduces v1.12 |
| model/rng_contract.json | FILE | `232ad93c6fc982bd5b564ab8f27f684696cd20326a4e3b9f12cc31db39d65fca` | reproduces v1.12 |
| model/summons.json | FILE | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | reproduces v1.12 |
| model/target_selection.json | FILE | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | reproduces v1.12 |
| model/waves.json | FILE | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | reproduces v1.12 |
| prereg v1.10 | FILE | `b1dd68efe2ce6009c2981d1c25bb182aba8c444945ec81f53a5c3c0c8b79061c` | reproduces v1.12 |
| prereg v1.11 | FILE | `312d71aaf3b5a15ca44a8179cbb46c35a50343e5bca23ab5201c73ec9c8278cc` | reproduces v1.12 |
| prereg v1.5 | FILE | `efac4bd51f2d2c1f1130a58c85f37d1c7738e51ac15afd3c70930f7ac3eef143` | reproduces v1.12 |
| prereg v1.6 | FILE | `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` | reproduces v1.12 |
| prereg v1.7 | FILE | `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` | reproduces v1.12 |
| prereg v1.8 | FILE | `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c` | reproduces v1.12 |
| prereg v1.9 | FILE | `b787308c8c331e98fee6221c97174bf8f696a5b55d699611c5ab697625de95dd` | reproduces v1.12 |
| reference manifest.json | FILE | `212b8652523048e1f8ac4697f13132388be22b8c6c4510180712832c5e560346` | reproduces v1.12 |
| reference/acceptance.json | FILE | `f5ce2c174cccf9a253603ac8bfc3f20b872b2e2a92c8d24e461601e64f1f9853` | reproduces v1.12 |
| reference/actors.json | FILE | `ef03536f97fe7122e14b34ae69a26bc7616fe58fcbe5989ab3aa09e7420ea04b` | reproduces v1.12 |
| reference/meta.json | FILE | `25c2be7ef76fef64f8610401196bc3db724c84d62a726ecc8bb596816d0b7d72` | reproduces v1.12 |
| reference/rng_tape.json | FILE | `607bf3bffd6a5a330d2ede97eebcd7139f3c218292954aa56fbf38c34e833ea0` | reproduces v1.12 |
| reference/skill_interrupt_reference.json | FILE | `45522df26b1703ac2489d08e7e7fa6986255ca80e64f057279ca6b492fdf3707` | reproduces v1.12 |
| reference/tracks.json | FILE | `bb3495218fcdeaab11d4d5e9a5d25a2e14f2fd21384bcebc7dd1f93b0b7d9bfd` | reproduces v1.12 |
| reference/u7_heading_conditioning.json | FILE | `5ad6ab0f089d3409506f29293433849f6abcbd1bee2a2242344fe12367287c05` | reproduces v1.12 |
| sealed [M-POL2] | FILE (hashed only, K-7) | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | reproduces v1.12 |
| sealed [MECH] | FILE (hashed only, K-7) | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | reproduces v1.12 |
| sealed [W1W] | FILE (hashed only, K-7) | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | reproduces v1.12 |
| setup C | ROWSET | `207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c` | reproduces v1.12 |
| setup T | ROWSET | `ab3197727b59cc355f479862a297b33bef89e74e6d40dbff14762c701f2c7be0` | reproduces v1.12 |
| v1.11 pre-read | FILE | `b9fd065496d2def98814db9334038aa7f2b466969696d3517a98a0de6f5c89da` | reproduces v1.12 |
| v1.6 pre-read | FILE | `5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0` | reproduces v1.12 |
| v1.7 att1 Gate-2 | FILE | `d2aa93db92122e033927f63ff61c9e6a2c13e1c7cba09a4fff20cb2382de6c37` | reproduces v1.12 |
| v1.7 att1 grade | FILE | `9778b4de4aa05acb2396439d2ff9de264ec590475ebf56aec93f3912ba12505e` | reproduces v1.12 |
| v1.7 att1 verdict | FILE | `9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2` | reproduces v1.12 |
| v1.7 pre-read | FILE | `ff1df4a18e9e60c1a5543edb391eded667b11711b340cd4763f3cdd204cab1ff` | reproduces v1.12 |
| v1.8 pre-read | FILE | `5358cb8cc99dcf1dd998e875e911d6ae53e9046dab0d24abe28a5c83193d5dff` | reproduces v1.12 |
| v3.7 closure AFTER | FILE | `e9a5c05e164172b5514e2fa1c323da243bee6fa7e7dc878ade4f4651eebc3805` | reproduces v1.12 |
| v3.7 closure BEFORE | FILE | `e6eeadb42e6928b9d45d2242b0b6cc81ee720709b95148efe8c17184757253b4` | reproduces v1.12 |
| v3.7 cut prereg | FILE | `ccf17ae6ffd06cb17d72ee88e34657fef8a1a16a70839b8ad091e4fdb1f7db05` | reproduces v1.12 |
| v3.7 cut receipt | FILE | `5de7beb2b4c3ad5ab4325fc372783977c86fd1fcd2750d78ccf94c6514baaf98` | reproduces v1.12 |
| v3.7.1 PRE gate | FILE | `fce6a344860e4f539763b08c6320160260e77c28f007ced00d25af7fa8456cbe` | reproduces v1.12 |
| v3.7.1 cut prereg | FILE | `f96bfade2bb9968a943c42b0639cd5fe7f0aec29ad2cf177983c7896a4d4bf0f` | reproduces v1.12 |
| v3.7.1 cut receipt | FILE | `a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9` | reproduces v1.12 |
| v3.7.1 law | FILE | `2c24ea92dacd259cd4e989fa09cdc08c9f6c91f5b18f49ac17ad6b9b800b008e` | reproduces v1.12 |

**115 of 115 carried pins reproduce v1.12. Failures: none.** Engine HEAD `22cd2288`; tracked modifications under `simulation/kc2`, `export`, `simulation/scripts`: none. `setup` partition re-derived by rule: C = 8, T = 19, C equals v1.12's list: True. Set cardinalities 466 / 456 / 10, partition {'BANDA-DB-CITED': 180, 'FALLBACK': 158, 'LAPR-MEASURED': 128}, `march_base` 3.209466. `TA-X-18` bits ['c00fffffffffffde', 'be9777a5cf72cec6'] (equal to v1.12: True). `TA-X-09`: 9 vectors.

**New documents of record (no v1.12 value exists; computed, not compared):**

| document | label | sha256 |
|---|---|---|
| G3 KP-177 MANIFEST (godot b4c1ff3) | FILE | `78bbcc8dbf39eb30fc8e89b35a7a80b8375394a4ddbe64d39a65b4984d351fcb` |
| G3 oracle tool (godot b4c1ff3) | FILE | `51f46965544683640b6c2949978788fa7b4185305fee2b3cf8a6fcec11d8c83a` |
| attempt-1 (v1.12) grade note | FILE | `d5dec43bb28820615f64ddb03bcf75efa6a2bcb5d881c6a728529d99be91ae21` |
| attempt-1 (v1.12) grade script | FILE | `27eb4079038a5ee1abf895c7806556da2f4226d1e1108d233f38d759e11457f4` |
| attempt-1 (v1.12) verdict file | FILE | `af3754c701f8afb22a5501b0b955fb8b2dc36cf361d5033980daa23e4c86f2f0` |
| jack-ryan grade Gate-2 (347ce2e1e) | FILE | `aa1e31a68d10aaee4e46819825fbded9dd7658494d70d0c58e48f55b0c86957d` |
| jack-ryan repairs Gate-2 (ea0317306) | FILE | `c1323ed7a894ef8b0eef9a64af456899f72b03167819b8dbdc320fb621ba00ae` |
| prereg v1.12 (v1.13's only predecessor) | FILE | `a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854` |
| runtime tree at b4c1ff3 (KP-179 repairs; NOT the attempt-2 runtime) | FILE-SET (make_manifest law, recomputed from git blobs) | `e584477b3d3c8bd6aa69bc43be32a137ab7b875a6c745aae40ccb20bb0e0591a` |
| the oracle hook (v1.13's oracle-side instrument) | FILE | `dce0625d30cd09289c7b073923ac4d1c732763614c5f9f30b08cedc96eab6cd9` |

The runtime-tree row is recomputed from `kc2_runtime/MANIFEST.json` at godot `b4c1ff3` over git blobs (84 members, member failures: none; the MANIFEST's own `tree_digest` reads `e584477b3d3c8bd6aa69bc43be32a137ab7b875a6c745aae40ccb20bb0e0591a`). **It is lineage, not the attempt-2 runtime.** The runtime with v1.13's counters is re-pinned in § PINS.2 (godot `05508a0`); the attempt-2 runtime is the digest the pre-attempt read (§ G.1a) and the attempt run on, after H-4.
<!-- /FILL:pins -->

### ⚑ PINS.2 · drax's v1.13 COUNTERS: THE RUNTIME RE-PINNED AT GODOT `05508a0` (KP-182)

Recomputed by `pins_v1p13.py` from git blobs at godot `05508a0` (the runtime's own `MANIFEST.json` law over its members; `kc2_runtime/` byte-unchanged from `4fd523f`, the commit the KP-180 G3 ran at). **This is the runtime whose counters carry the names of § F.2m.5 and § F.2n.6.** It is **not yet the attempt-2 runtime**: H-4 re-points the harness to this file, which moves the tree; the attempt-2 digest is the one the § G.1a read and the attempt both name.

<!-- FILL:kp180 -->
| artifact (godot `05508a0`) | label | sha256 (recomputed from git blobs) | equals drax's G3 MANIFEST |
|---|---|---|---|
| ⚑ **the runtime tree `kc2_runtime/`** (85 members; member failures: none; unchanged from the G3 run commit: True) | FILE-SET (make_manifest law over git blobs) | `c9a7299e160386f2be34fb33bfab64947b88ba1fc7e110b0efa83a63e3f09ed4` | MANIFEST `tree_digest` equal: True |
| ⚑ G3 evidence `evidence/kc2-play/2026-10-01-g3-25cell-kp180/MANIFEST.json` | FILE | `4347e87debb9982830203e6cd369edd889ba39096388f9bef2231453a48bcb7f` | — |
| `kc2_runtime/sim/kc2rt_board.gd` | FILE | `733b26d04b64d4c4fe9cb00f19a73899485d828537b4d0d4b9c2c1847942a72d` | True |
| `kc2_runtime/sim/kc2rt_fight.gd` | FILE | `bf6915caccda3e20fa7af431c0bcc83b0b66e34ef953fb761c31667217ca0bbf` | True |
| `kc2_runtime/sim/kc2rt_rng.gd` | FILE | `a1ce051f2aad6959118707f1a2eceb2bdee70375a42deaf30fcd42fdf9480e4d` | True |
| `kc2_runtime/sim/kc2rt_roster.gd` | FILE | `c55d37c217be017624663e3a6555eaafcb454c67ae063cfe4352b88abe412337` | True |
| `kc2_runtime/tests/kc2rt_booking_census.gd` | FILE | `73ebc5db15aa1df86ccacd802fc13ad5a034337bf4eede53591cbceae34ae794` | True |
| `kc2_runtime/tests/kc2rt_ta.gd` | FILE | `ae8fa11677bb95d62bf080af5227d7f19c3ecd8bd29b1162bbfaac62645e69a7` | n/a (not listed there) |
| `kc2_runtime/tests/kc2rt_ta_emit.gd` | FILE | `72b87558afea5c77f0a713a76e60466bf60d3eb01c7f7255a5f3797bda7b6d5a` | n/a (not listed there) |
| `kc2_runtime/tools/kc2rt_file_ta_evidence.py` | FILE | `42b1f64c3e917f2f20996b96bcad1e7eeaf9c4ef6781f2aedeff529fedb1690f` | n/a (not listed there) |
| `kc2_runtime/tools/kc2rt_g3_loop_trace.gd` | FILE | `9baa645f0a47d63203878ea60aa4a38a8e471b4b1bc23f8defa49b794c4e14be` | True |
| `kc2_runtime/tools/kc2rt_g3_oracle_trace.py` | FILE | `666db73d0ef0a22924882fa5240fb0c88e736efbd597690dba9015e1dd0eb689` | True |
| `kc2_runtime/tools/kc2rt_side_by_side.gd` | FILE | `bfcf55d223fb70d1b99a9b02e86456cb7dc15f7d7dc37ed60fa23e330d7fbed6` | True |

**drax's G3 at this digest, cross-checked by `check_v1p13_draft.py` against this file's own oracle measurement:**

* drax's oracle-side counters equal this file's oracle measurement: **25/25**
* trace files match drax's MANIFEST: **25/25**
* G3 census equal: **25/25**
* § C.9.5a control term equal (port vs oracle): **25/25**
* G3 passes (port on the oracle's draws): **25/25**
* every TA-X-08 counter equal (port vs oracle): **25/25**
* TA-X-16 per-wave counters equal (port vs oracle): **25/25**
* each KP-180 oracle trace, minus its two new keys, equals the KP-177 trace measured here: **25/25**
<!-- /FILL:kp180 -->

---

## § B.3a · ⚑ `P-2`: THE OPERATIONAL READING, AND THE DIGEST LAW FOR `TA-X-01` / `TA-X-03…05`

**The law is carried unchanged** (v1.8 § B.3): *`M-POL-2` salt 0 run twice, once with a zero-draw no-op fold inserted; the
digests must be identical; `P-2` red → `TA-X-03…05` UNGRADEABLE → `INDETERMINATE`.* **What is new is how it is
evaluated** (Discipline #12: operational, not a criterion change). A `P-2` is GREEN only if all of the following hold;
otherwise it is **NOT RUN** (if (1)–(2) fail) or **RED**:

1. **A real inserted fold.** A fold object in the fight's fold chain, **invoked by the fight loop every tick** at the
   granularity of the existing folds, which **obtains its own stream through `Kc2RtRng.fork_stream` (V9-LAW-1)**.
   ⚑ **Fork order:** it is forked **ahead of at least one live fold's `fork_stream`** (jack-ryan 347ce2e1e INFO-5).
   ⚑ **Stated, so it is not over-read** (jack-ryan ea0317306 INFO-3): `fork_stream` seeds from its `seed_in` alone
   (`kc2rt_rng.gd:314-326`), so no fork-index dependence exists for this ordering to expose at the current runtime. The
   clause is kept because it is what makes the probe sensitive **if** a later runtime introduces such a dependence.
2. **A measured zero.** The inserted fold's own draw counter is read on the stream object and equals `0`, and its
   invocation count equals the number of ticks. A literal `0` is not a measurement.
3. **One digest function for both legs** (`cell_digest`), in which ⚑ **a site with zero draws and an absent site are the
   same stream fact** (zero-draw sites dropped globally). Every other draw count stays in the digest. The digest's
   subject is the terminal, the census `state_counts`, the board counters and the per-site draw counts.
4. **Controls that must go RED by their own clauses:** (a) the inserted fold draws once from a shared stream; (a0) the
   digest alone, at own-draws 0, perturbed; (b) one extra root draw at a live registered site; (c) the attempt-1
   digest law reproducing its false RED. ⚑ **Optional, non-gating** (jack-ryan ea0317306 INFO-2): a control (d) that
   reseeds a live stream at an equal draw count, proving the outcome terms detect a state perturbation.
5. **A fresh pack per leg**, and **no graded cell carries the inserted fold** (no fold key, no probe site).

⚑ **THE DIGEST LAW, PRINTED FOR EVERY ROW THAT USES IT.** `TA-X-01` (self-determinism), `TA-X-03`, `TA-X-04`
(`≡`, byte-exact) and `TA-X-05` (`≢`, one-sided) are evaluated on **the same `cell_digest`**, with **zero-draw = absent**.
This can only add equalities, never remove one: `TA-X-03`/`04` cannot newly fail under it, and `TA-X-05`'s one-sided
inequality is checked on the same function (jack-ryan ea0317306 Item 8). No value moves.

---

## § C.9.5a · ⚑ G3 GAINS TWO EQUALITIES (an attempt precondition, not a graded row)

On each (arm, salt), in addition to C.9.3–C.9.5 (carried):
* **the census:** the port's per-state player census over leg A equals the oracle's own `actor_state._player_rows` count
  for the same cell (KP-179 already measures it: equal 25/25 at `e584477b`);
* ⚑ **the control term:** the port's `n_control_suppressed_channelling` equals the oracle trace's count of control
  `channel` entries on leg A (the G3 oracle tool's `control` list, `kc2rt_g3_oracle_trace.py:83-88`). On the 25 reference
  traces that count equals the oracle's own `n_control_suppressed_channelling` 25/25 (§ F.2n.4).

**Why here and not in a row:** G3 runs the port on the oracle's draws, where 38 of 63 control applications insert. The
graded run uses the port's own generator, where KP-180 measured 0 insertions in 15 cells. A row can only test the new
term on the realisation it is graded on; G3 is where the term is exercised (§ F.2n.5). Discipline #12: this widens an
attempt precondition, and it is named.

---

## § F.2m · ⚑ `TA-X-16` RESTATED PER WAVE PLAYED (Matt Q96.1, KP-183: *"Per played wave."*)

### F.2m.1 · Why v1.12's text cannot stand (one sentence, jack-ryan 347ce2e1e INFO-6)

G3 shows the port bit-faithful to the oracle on the oracle's draws, dying at the oracle's wave and tick on 25/25; the
oracle's terminal waves are w151–w156 on every cell; **so a port bit-faithful on the reference realisation scores
`n_pool_picks == 47` RED on 25/25.** The row rewarded infidelity. Measured here on the oracle itself: **0/25** (§ F.2m.4).

### F.2m.2 · The pinned vector, derived by script from the pack

**Law.** `V11-P06-1[w]` = the number of distinct `spawn_point` values among `model/waves.json :: pools.wave_spawn` rows
with `global_wave == w`, **excluding point 6**, for w = 151 … 160. `P06-KEY[w]` = 1 if point 6 occurs among those rows
at w, else 0. **Checksum:** Σ `V11-P06-1` = 47 and Σ (with point 6) = 54, so Σ `P06-KEY` = 7. The script also asserts that
the vector equals the pack's own `V11-P06-1` row (`rng_contract.json`) and the oracle's own
`wave_engine.pools_for(w, bonus_spawns_enabled=False)` key counts, and that the oracle's filter drops exactly key 6.

<!-- FILL:vector -->
```
law            : V11-P06-1[w] = |{spawn_point of model/waves.json pools.wave_spawn rows with global_wave == w} \ {6}|, w = 151..160
V11-P06-1      : [5, 5, 5, 4, 4, 5, 5, 5, 5, 4]   (w151 … w160)   sum 47
p06 ON (info)  : [5, 6, 6, 4, 5, 6, 6, 6, 5, 5]   sum 54
P06-KEY[w]     : [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]   sum 7   (key grain: one (w, 6) key, or none)
P06-ROWS[w]    : [0, 6, 2, 0, 5, 1, 1, 2, 0, 1]   sum 18   (row grain: NOT graded; printed so the two grains are never confused)
checks         : checksum 47/54 = True; data keys == oracle keys (on) = True; equals the oracle's pools_for(w, False) key counts = True; equals the pack's V11-P06-1 row = True; oracle pools_for(w, True) key counts = vector_on = True; oracle's filter drops exactly key 6 = True; p06 keys = 54 - 47 = 7 = True
```
<!-- /FILL:vector -->

### F.2m.3 · The restated row (per cell; all 25 cells, § B.1a unchanged)

Let `T` be the cell's leg-A terminal wave (the wave of the player's first death, or 160 if the cell clears), and
**`W = {151, …, T}` the waves the cell played.** The board is rolled at each wave's start (`roll_wave`), so every wave in
`W`, the death wave included, has a complete roll.

| clause | statistic | expected | tolerance | grain |
|---|---|---|---|---|
| (a) | for each `w ∈ W`: `pool_picks[w]` | `V11-P06-1[w]` (§ F.2m.2, pinned) | integer, exact, **per wave** | ⚑ **key**: distinct spawn-point keys the board rolls at wave `w` |
| (b) | `n_pool_picks` | `Σ_{w ∈ W} V11-P06-1[w]` | integer, exact | the sum of (a) |
| (c) | `n_spawn_point_6_keys_rolled` (named, per cell; and per wave) | `0` (and `0` on every `w ∈ W`) | integer, exact | key |
| (d) | for each `w ∈ W`: `n_p06_keys_filtered[w]`, **graded** | `P06-KEY[w]` | integer, exact, per wave | ⚑ **key**: a `(w, 6)` key present in the unfiltered table and dropped by the p06-OFF filter counts **once per wave**. ⚑ **Not rows:** the 18 p06 `wave_spawn` rows (`P06-ROWS`) are a different grain; the port's current manifest-grain `picks_suppressed` counts rows and is **not** this counter (jack-ryan 347ce2e1e INFO-2) |

**GREEN iff (a)–(d) hold on every cell.** A cell that clears w160 has `W` = all ten waves and (b) = **47**: the old
constant survives exactly where its premise holds. **(d) is graded, not only emitted**, because a filter with no counter
is indistinguishable from a filter that never fired (v1.5 § F.2c); (d) is what proves the filter fired on the waves where
there was a p06 key to drop.

**Grain declared, and why key:** the oracle's filter acts on spawn-point **keys** (`wave_engine.py:305-307`: `{sp: alts …
if sp != 6}`). A row-grain counter would count a property of the data table, not of the filter.

### F.2m.4 · ⚑ THE ORACLE CHECK: the restated row on the 25 reference realisations

**Instrument.** `check_v1p13_draft.py`, on the 25 filed G3 oracle traces (godot `b4c1ff3`,
`evidence/kc2-play/2026-10-01-g3-25cell-kp177/`, each checked against MANIFEST `78bbcc8d…`) and the 25 hook records of
`oracle_channel_hook.py`, which re-ran drax's **unchanged** oracle tool with read-only hooks on `pools_for` and
`ChannelPolicyFold.observe`. **Every re-run trace is byte-identical to the filed trace (25/25)**, so the hooks perturbed
nothing. `pool_picks[w]` is read at key grain off the oracle's own `roll_wave → pools_for` call; the actor grain is
printed as a cross-check.

<!-- FILL:t16 -->
| cell | terminal | waves played | picks per wave (= V11-P06-1 prefix?) | `n_pool_picks` / Σ expected | p06 keys rolled | filtered keys per wave (= P06-KEY prefix?) | restated | v1.12 text (`== 47`) |
|---|---|---:|---|---|---:|---|---|---|
| M0_s0 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M0_s1 | w151 | 1 | [5] (True) | 5 / 5 | 0 | [0] (True) | **GREEN** | RED |
| M0_s2 | w156 | 6 | [5, 5, 5, 4, 4, 5] (True) | 28 / 28 | 0 | [0, 1, 1, 0, 1, 1] (True) | **GREEN** | RED |
| M0_s3 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M0_s4 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M-POL-2_s0 | w156 | 6 | [5, 5, 5, 4, 4, 5] (True) | 28 / 28 | 0 | [0, 1, 1, 0, 1, 1] (True) | **GREEN** | RED |
| M-POL-2_s1 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| M-POL-2_s2 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M-POL-2_s3 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| M-POL-2_s4 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| M-POL-2-NULL_s0 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M-POL-2-NULL_s1 | w151 | 1 | [5] (True) | 5 / 5 | 0 | [0] (True) | **GREEN** | RED |
| M-POL-2-NULL_s2 | w156 | 6 | [5, 5, 5, 4, 4, 5] (True) | 28 / 28 | 0 | [0, 1, 1, 0, 1, 1] (True) | **GREEN** | RED |
| M-POL-2-NULL_s3 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| M-POL-2-NULL_s4 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| W1_s0 | w156 | 6 | [5, 5, 5, 4, 4, 5] (True) | 28 / 28 | 0 | [0, 1, 1, 0, 1, 1] (True) | **GREEN** | RED |
| W1_s1 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| W1_s2 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| W1_s3 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| W1_s4 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| W1-NULL_s0 | w156 | 6 | [5, 5, 5, 4, 4, 5] (True) | 28 / 28 | 0 | [0, 1, 1, 0, 1, 1] (True) | **GREEN** | RED |
| W1-NULL_s1 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| W1-NULL_s2 | w155 | 5 | [5, 5, 5, 4, 4] (True) | 23 / 23 | 0 | [0, 1, 1, 0, 1] (True) | **GREEN** | RED |
| W1-NULL_s3 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |
| W1-NULL_s4 | w152 | 2 | [5, 5] (True) | 10 / 10 | 0 | [0, 1] (True) | **GREEN** | RED |

**Restated row on the oracle: 25/25. v1.12's text on the oracle: 0/25.** Every roll passed `bonus_spawns_enabled=False`: True. On every wave played the actor grain (distinct `spawn_point_id` among spawned roster actors) equals the key grain and carries no `p06`: True.
<!-- /FILL:t16 -->

**Honest `n`:** the 25 reference cells are **12 distinct oracle realisations** (`check_v1p13_draft.py`, trace digests
minus the arm label): `M0 ≡ M-POL-2-NULL` and `M-POL-2 ≡ W1-NULL` on every salt, and `W1` differs from `M-POL-2` on salts 0
and 4 only. Every "25/25" in this file is 12/12 distinct outcomes. The terminal waves span w151–w156, so clause
(a) is exercised on 1 to 6 waves per cell and **no reference cell exercises w157–w160**; the vector entries for w157–w160
rest on the derivation (§ F.2m.2) and the oracle's `pools_for`, not on a reference fight.

### F.2m.5 · Counters this row requires (drax, emission) — ⚑ LANDED at godot `05508a0` under these names (§ PINS.2)

Per cell: `terminal_wave`; `waves_played` (list); `pool_picks_per_wave` (key grain, one entry per `w ∈ W`);
`n_pool_picks`; `n_spawn_point_6_keys_rolled` and `n_spawn_point_6_keys_rolled_per_wave`;
`n_p06_keys_filtered_per_wave` (key grain) and its sum. Remove the stale prose at `kc2rt_roster.gd:1942` (jack-ryan
ea0317306 INFO-1; removed at `96b1f5a`). drax's commit text calls the filtered counter's grain the "(wave, point) PAIR"
grain: one `(w, 6)` pair per wave, which is this row's **key** grain.

---

## § F.2n · ⚑ `TA-X-08` IDENTITY 2 RESTATED WITH THE SEAL'S OWN TERM (Matt Q96.4, KP-182: *"Add control term"*, with both sub-choices)

### F.2n.1 · Why v1.12's identity 2 cannot stand

Since v3.7 (KP-147) the oracle runs `ControlApplicationFold` natively. On a tick the control fold suppresses the channel
(`_cc["channel"]`), the census records non-channelling (`run.py:2815`: `circle_channel_active = not _cc["channel"] and not
_channel_broken`), and the channel fold's `observe(already_suppressed=True)` returns without consulting its verdict
(`channel_policy.py:386-388`). **If the channel fold's verdict on that tick was "channelling", the tick is in D and in
neither `n_channelling` nor `n_released`.** The seal's own two-instrument identity carries that term
(`n_control_suppressed`); it read 0 on the five sealed salts because the seal predates the native control fold. Measured
here on the oracle itself: identity 2 as written passes **6/25** (§ F.2n.4).

### F.2n.2 · The restated identities (per cell; all 25 cells)

```
(1)  n_player_ticks_observed  =  D + PRE_FIGHT                                              (CARRIED, exact)
(2)  n_channelling + n_released + n_control_suppressed_channelling  =  D                    (RESTATED, exact)
(2p) n_ticks_released  =  n_released + n_released_pre_fight                                 (population closure, exact)
∴    uptime + (n_released + n_control_suppressed_channelling) / D  =  1
```

**Definitions** — every term is over leg A, and **D, PRE_FIGHT and the census are those of § F.2o**:
* `n_channelling` = census `CHANNELLING + CHANNELLING_AND_MOVING` (on D, by construction);
* ⚑ **`n_released` = the number of D ticks on which the channel fold's own verdict is *released*** (`tick_apply`'s
  `released`, `channel_policy.py:297-339`), **whether or not the control fold also suppressed that tick**;
* ⚑ **`n_control_suppressed_channelling` = the number of D ticks on which the control fold suppressed the channel
  (`_cc["channel"]`) AND the channel fold's verdict was *channelling*.** On an arm with no channel fold (`M0`) the verdict
  is channelling by construction, so the term is every control-suppressed D tick;
* `n_ticks_released` = the fold's own counter over **all** observed ticks (PRE_FIGHT included);
  `n_released_pre_fight` = released verdicts on PRE_FIGHT ticks.

**The three terms of (2) partition D** — a D tick is channelling iff neither fold suppresses it; a non-channelling D tick
is either fold-released (counted in `n_released`, whatever the control did) or control-suppressed with the fold
channelling (counted in the new term), never both. **(2) is therefore the oracle's own tick law** (`run.py:2810-2815`),
not a fitted closure.

### F.2n.3 · `n_released`'s population, stated (Q96.4's explicit question; ruled with the term)

⚑ **`n_released` counts D only, not all observed ticks.** Reason, from the law and not from a measurement: identity (2) is
an equation on D, and a PRE_FIGHT tick is outside D (§ F.2o), so a released verdict on a PRE_FIGHT tick cannot be in a
term that sums to D. The fold's counter `n_ticks_released` (v1.1 § C.1's emission requirement; the seal's
`⚑ release_duty_on_observed_ticks` numerator) is over all observed ticks, so **(2p) closes the population on the emission
rather than asserting it**: the runtime emits both counters and `n_released_pre_fight`, and the row checks the three
agree. **Disclosure:** on the 25 reference realisations no PRE_FIGHT tick is released and no control-suppressed D tick is
fold-released (both 0, § F.2n.4), so the reference **cannot discriminate** the two populations, or the two ways of
booking a doubly-suppressed tick. Both choices are fixed here by the oracle's code, not by an outcome.

### F.2n.4 · ⚑ THE ORACLE CHECK: identities (1), (2) as written, (2) restated, (2p), on the 25 reference realisations

`n_channelling` and D are the oracle's own census (`actor_state._player_rows`, as filed in each trace). `n_released`,
`n_released_pre_fight` and `n_control_suppressed_channelling` are read per tick off the oracle's channel fold by the
read-only `observe` hook (the fold's verdict and the `already_suppressed` argument the oracle passes), aligned to the
trace tick by tick. **Independent cross-check:** the trace's own control `channel` entries (the G3 tool's hook on
`ControlApplicationFold.tick`) count the same ticks. **Fold-arm consistency:** on every tick the hook's verdict, the
oracle's return value and the trace's `chan` bit agree; the fold counter `n_ticks_released` equals the released verdicts
on observed ticks.

<!-- FILL:t08 -->
| cell | observed | PF | D | id. 1 | `n_channelling` | `n_released` (D) | released PF ticks | `n_control_suppressed_channelling` | trace control `channel` entries | as written: lhs − D (jack-ryan KP-180) | **restated** |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---|
| M0_s0 | 936 | 5 | 931 | ✓ | 928 | 0 | 0 | 3 | 3 | -3 (-3) | **GREEN** |
| M0_s1 | 161 | 1 | 160 | ✓ | 160 | 0 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| M0_s2 | 1168 | 6 | 1162 | ✓ | 1157 | 0 | 0 | 5 | 5 | -5 (-5) | **GREEN** |
| M0_s3 | 912 | 5 | 907 | ✓ | 906 | 0 | 0 | 1 | 1 | -1 (-1) | **GREEN** |
| M0_s4 | 921 | 5 | 916 | ✓ | 911 | 0 | 0 | 5 | 5 | -5 (-5) | **GREEN** |
| M-POL-2_s0 | 1068 | 6 | 1062 | ✓ | 954 | 104 | 0 | 4 | 4 | -4 (-4) | **GREEN** |
| M-POL-2_s1 | 275 | 2 | 273 | ✓ | 239 | 32 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| M-POL-2_s2 | 956 | 5 | 951 | ✓ | 862 | 87 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| M-POL-2_s3 | 309 | 2 | 307 | ✓ | 261 | 46 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| M-POL-2_s4 | 333 | 2 | 331 | ✓ | 298 | 32 | 0 | 1 | 1 | -1 (-1) | **GREEN** |
| M-POL-2-NULL_s0 | 936 | 5 | 931 | ✓ | 928 | 0 | 0 | 3 | 3 | -3 (-3) | **GREEN** |
| M-POL-2-NULL_s1 | 161 | 1 | 160 | ✓ | 160 | 0 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| M-POL-2-NULL_s2 | 1168 | 6 | 1162 | ✓ | 1157 | 0 | 0 | 5 | 5 | -5 (-5) | **GREEN** |
| M-POL-2-NULL_s3 | 912 | 5 | 907 | ✓ | 906 | 0 | 0 | 1 | 1 | -1 (-1) | **GREEN** |
| M-POL-2-NULL_s4 | 921 | 5 | 916 | ✓ | 911 | 0 | 0 | 5 | 5 | -5 (-5) | **GREEN** |
| W1_s0 | 1119 | 6 | 1113 | ✓ | 1006 | 107 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| W1_s1 | 275 | 2 | 273 | ✓ | 239 | 32 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| W1_s2 | 956 | 5 | 951 | ✓ | 862 | 87 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| W1_s3 | 309 | 2 | 307 | ✓ | 261 | 46 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| W1_s4 | 931 | 5 | 926 | ✓ | 830 | 94 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| W1-NULL_s0 | 1068 | 6 | 1062 | ✓ | 954 | 104 | 0 | 4 | 4 | -4 (-4) | **GREEN** |
| W1-NULL_s1 | 275 | 2 | 273 | ✓ | 239 | 32 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| W1-NULL_s2 | 956 | 5 | 951 | ✓ | 862 | 87 | 0 | 2 | 2 | -2 (-2) | **GREEN** |
| W1-NULL_s3 | 309 | 2 | 307 | ✓ | 261 | 46 | 0 | 0 | 0 | +0 (+0) | **GREEN** |
| W1-NULL_s4 | 333 | 2 | 331 | ✓ | 298 | 32 | 0 | 1 | 1 | -1 (-1) | **GREEN** |

**Summary, measured on the oracle:**

* TA-X-08 identity 1 (oracle passes): **25/25**
* TA-X-08 identity 2 AS WRITTEN (oracle passes): **6/25**
* TA-X-08 identity 2 RESTATED (oracle passes): **25/25**
* identity 2 restated, rival population (all observed ticks): **25/25**
* shortfall == jack-ryan KP-180 table: **25/25**
* shortfall == -(control-suppressed channelling): **25/25**
* independent: trace control `channel` entries (leg A) == n_control_suppressed_channelling: **25/25**
* fold counter n_ticks_released == released on observed ticks (fold arms): **25/25**
* fold aligned + consistent + no desync: **25/25**
* census chan == trace chan on D: **25/25**
* released PRE_FIGHT ticks (all cells): **0**
* control-suppressed PRE_FIGHT ticks (all cells): **0**
* control-suppressed RELEASED ticks on D (all cells): **0**
<!-- /FILL:t08 -->

**(2p) on the oracle:** `n_ticks_released` (the fold's own counter) equals `n_released + n_released_pre_fight` on all 20
fold-arm cells. `M0` has no channel fold: `n_released` and `n_released_pre_fight` are 0 by construction, and the port's
`M0` must emit `n_ticks_released = 0`.

### F.2n.5 · What the restated row can and cannot see on attempt 2 (stated, not resolved)

On the port's own generator KP-180 measured 0–4 control applications per cell, every one resisted to zero (0 insertions in
15 cells). If attempt 2's cells look the same, `n_control_suppressed_channelling` is 0 on every graded cell, and identity
(2) holds there with the new term at 0. **The row is then GREEN on a realisation that does not exercise the term.** That is
a property of the realisation, not of the row: the row is now the oracle's law, which v1.12's was not. **The term is
exercised in G3** (§ C.9.5a: equality with the oracle's count on the oracle's draws, where 38/63 applications insert). A
PASS's report face must say which realisation exercised it (§ F.5 cl. 13).

### F.2n.6 · Counters this row requires (drax, emission) — ⚑ LANDED at godot `05508a0` under these names (§ PINS.2)

Per cell: `n_control_suppressed_channelling` (D population); `n_released` (D population); `n_released_pre_fight`;
`n_ticks_released` (all observed); diagnostic, emitted not graded: `n_control_suppressed_released` (control-suppressed D
ticks the fold had released, counted in `n_released`) and `n_control_suppressed_pre_fight`.

---

## § F.2o · ⚑ THE CENSUS CONVENTION (OPERATIONAL; defines D, PRE_FIGHT and the census for `TA-X-08`)

* **The lethal tick is censused ALIVE**, classified by its own channel and motion verdicts, and is inside D
  (`run.py:4937-4938`: `player_dead_tick = ledger_player[-1][0]`; `actor_state.py:252`: alive iff `rt <= player_dead_tick`).
  `DEAD` applies only to a tick censused after the lethal one, and leg A never reaches one.
* **One `PRE_FIGHT` per wave played**: each wave's first censused tick (`actor_state.py:255-261`), outside D and outside
  `n_channelling` / `n_released` / `n_control_suppressed_channelling`.
* **Excluding the lethal tick is a hollow green** (jack-ryan 347ce2e1e WARN-1): the identities close with D one short of
  the oracle. The convention is enforced against the oracle in G3 (§ C.9.5a, census equality), because an internal
  identity cannot see it.

**Discipline #12:** this is how v1.1 § C.1's D was always meant to be counted (the seal records no DEAD tick); it is now
written down. No value moves. **Checked on the 25 reference realisations:**

<!-- FILL:census -->
| cell | one PRE_FIGHT per wave played | no DEAD | lethal tick censused alive | D = G3 `D_oracle` | PF = G3 `PRE_FIGHT_oracle` |
|---|---|---|---|---|---|
| M0_s0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M0_s1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M0_s2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M0_s3 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M0_s4 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2_s0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2_s1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2_s2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2_s3 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2_s4 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2-NULL_s0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2-NULL_s1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2-NULL_s2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2-NULL_s3 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M-POL-2-NULL_s4 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1_s0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1_s1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1_s2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1_s3 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1_s4 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1-NULL_s0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1-NULL_s1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1-NULL_s2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1-NULL_s3 | ✓ | ✓ | ✓ | ✓ | ✓ |
| W1-NULL_s4 | ✓ | ✓ | ✓ | ✓ | ✓ |

**Census convention on the oracle: 25/25.**
<!-- /FILL:census -->

---

## § F.5 · Report-face rules: thirteen *(twelve carried, version label only; one added)*

13. ⚑ **THE CONTROL-TERM SENTENCE (mandatory on any report under v1.13):** *"`TA-X-08` identity 2 carries
    `n_control_suppressed_channelling`. On this run it was `<Σ over cells>` (max `<max>` on one cell); in G3 it was
    `<Σ>` and equal to the oracle's on every cell. A GREEN `TA-X-08` on a run where the term is 0 everywhere has not
    tested the control path; G3 has."*

---

## § G · FAIL TAXONOMY AND THE GRADED-RUN CAP

**The taxonomy is carried from v1.12 § G unchanged** (`STRUCTURAL → INDETERMINATE → PASS`; no post-hoc widening;
`declared_ungradeable` exactly `["TA-X-06"]`; C1 by G3).

### G.1 · THE GRADED-RUN CAP: **`1` OF `2` REMAINS (Matt Q96.2, KP-182: *"Keep 1 remaining."*)**

**Carried from v1.12, not reset.** v1.7 attempt 1 and v1.12 attempt 1 stay on the record, spent. The allowance is v1.12's
(Matt KP-115, *"Reset to 2"*), carried into v1.13 with one spent. **Naming: the next graded run is v1.13 attempt 2 of 2
(overall attempt 3). It is the last under the cap.**

**Q85's four guards hold:** (1) the budget was ruled from outside the run (Matt); (2) this prereg is committed ALONE, every pin
recomputed, before any graded run against it (D4); (3) every earlier attempt stays on the record, spent; (4)
`substrate_epoch` is declared on every artifact.

**L2 for attempt 2:** every item of § H, **including § G.1a's read**, holds at one runtime digest, and the attempt runs at
that digest. A `STRUCTURAL` attempt 2 exhausts the cap; what follows is Matt's. An `INDETERMINATE` consumes nothing and buys
nothing (carried).

### G.1a · ⚑ THE PRE-ATTEMPT READ OF ALL 28 GRADED ROWS: A PRECONDITION (Matt Q96.3, KP-182: *"Yes, as a precondition."*)

**What is frozen first.** Every expected value, tolerance, population, grain and antecedent the read applies is the one in
**this committed file**. Nothing in it moves after the read. A RED found by the read is repaired **in the port**; a row
change after the read is a `WARN-16` HALT to Matt and a new dated version, never an edit.

**The procedure:**
1. **The candidate.** drax names one runtime digest (FILE, `make_manifest` law) with the harness re-pointed to v1.13 (H-4),
   its G3 PASS on all 25 cells at that digest (§ C.9, incl. § C.9.5a), and a delta Gate-2 on the change from `c9a7299e`.
2. **The emission.** drax runs the T-A harness at that digest exactly as the graded run will (25 cells, the no-run rows, the
   verdict file), into an evidence folder labelled **`PRE-READ — NOT A GRADED RUN`**, with a MANIFEST pinning
   `ta_manifest.json` and `ta_verdict.json`. Nothing in it is a graded artifact or counts against the cap.
3. **The read. Seat: jack-ryan, as a gate document** (`agentic_orchestration/qa/findings/<date>-kc2-play-v1.13-pre-attempt-read.md`).
   He grades **all 28 EXACT rows** as § G would (GREEN / RED / UNGRADEABLE), reading the antecedents that decide gradeability
   on the same emission (`P-1` … `P-5`, `TA-X-07(c)`'s (L2), `TA-X-18`'s lossless-emitter clause), and prints the § G verdict
   the emission **would** take, plus § F.5 cl. 13's control-term sentence. **He does not grade the attempt, and his read is
   not a verdict of record.**
4. **The outcome.**
   * **28/28 GREEN, none UNGRADEABLE:** attempt 2 may fire **at the same digest** (tree FILE equal, checked at boot). The
     read is committed before the attempt and cited by it.
   * **Any RED or UNGRADEABLE:** attempt 2 does **not** fire. The port is repaired, gated (delta Gate-2), re-G3'd, and the read
     is repeated at the new digest. A read consumes nothing.
5. **The attempt.** Run fresh at the read's digest. The port is deterministic (`TA-X-01`), so its emission should reproduce
   the read's byte for byte; **the graded emission governs regardless**, and any difference from the read is printed on the
   report face.

**Why it cannot fit anything:** EXACT rows carry no fitted tolerance, § G forbids post-hoc widening by anyone, and every value
the read applies is pinned here before the read exists. It previews the grade; it protects the last attempt from a knowable
RED (the two attempt-1 reds were both readable off the candidate emission, KP-178).

### G.3 · Verdict file `kc2play.ta_verdict.v1` (v1.13): the fields that change from v1.12 § G.3

```
prereg_version          : "v1.13"
prereg_sha256           : <this file, derived at emission>
attempt                 : "v1.13 attempt 2 of 2" ; overall 3
runtime_digest          : <the attempt-2 runtime: the § G.1a read's digest>
ta_x_16                 : {<arm>|<salt>: {"terminal_wave", "waves_played", "pool_picks_per_wave", "expected_per_wave",
                           "n_pool_picks", "expected_sum", "n_spawn_point_6_keys_rolled", "n_p06_keys_filtered_per_wave",
                           "p06_key_expected_per_wave", "grain": "key", "holds"}, … all 25}, "vector": <§ F.2m.2>
ta_x_08                 : {<arm>|<salt>: {"observed", "PRE_FIGHT", "D", "id1_holds", "n_channelling", "n_released",
                           "n_control_suppressed_channelling", "n_ticks_released", "n_released_pre_fight",
                           "id2_holds", "id2p_holds"}, … all 25}
g3.<cell>.census_equal  : true                     (§ C.9.5a)
g3.<cell>.control_term  : {"port": <n>, "oracle": <n>, "equal": true}   (§ C.9.5a)
pre_attempt_read        : {"finding": <jack-ryan's gate document, FILE>, "runtime_digest": <equal to runtime_digest>,
                           "rows_green": 28, "ungradeable": 0}                 (§ G.1a)
```

Every other field is v1.12 § G.3 unchanged (`r11_bound`, `ta_x_18`, `arm_config_a8`, `set_digests`, `P5_folds`,
`declared_ungradeable`, `hole_closure`, …).

---

## § H · OWED BEFORE ATTEMPT 2 (blocking; in order)

| # | owed | owner | state at commit |
|---|---|---|---|
| H-0 | Matt rules Q96 (1–4); v1.13 committed ALONE | Matt; gamora | **DONE** (KP-182/183; this file) |
| H-1 | the counters of § F.2m.5 and § F.2n.6 per cell; the stale `kc2rt_roster.gd:1942` note removed; G3 on all 25 cells with § C.9.5a's two equalities | drax | **LANDED** at godot `05508a0` (§ PINS.2: G3 25/25, census, control term, `TA-X-08` and `TA-X-16` counters equal to the oracle 25/25) |
| H-2 | (L2) of `TA-X-07(c)` at the attempt-2 digest: operands unchanged or re-evaluated on all 25 cells (§ F.2k) | gamora or jack-ryan | drax reports the operand lines byte-identical to KP-177 at `c9a7299e`; to be confirmed at the attempt-2 digest |
| H-3 | delta Gate-2 on `c9a7299e` (the counter change) and on any later change | jack-ryan | owed |
| H-4 | the harness re-pointed to **this file** (label, `prereg_sha256`, the § G.3 blocks); filing MANIFEST pins both `ta_manifest.json` and `ta_verdict.json`; `runtime_header`'s `equals_P4` and `vendored_runtime_equals_runtime_digest` `true` | drax | filing tool + booleans landed (`12c0786`); the re-point owed |
| H-5 | the hole-closure finding at the graded digest (seal-blocking, not verdict-blocking; carried) | jack-ryan | owed |
| H-6 | **this file's pre-read** (H-7 of the series: the two restated rows, § F.2o, § B.3a, § C.9.5a, § G.1a, § K's audit) | jack-ryan | owed |
| H-7 | ⚑ **the § G.1a pre-attempt read: 28/28 GREEN at the attempt-2 digest** | jack-ryan (gate document) | owed |
| H-8 | Matt's T-C on the graded digest (seal condition; carried) | Matt | owed |

---

## § K · ⚑ THE ONCE-PER-VERSION LAW (a) AUDIT (KP-178): DOES THE ORACLE PASS EVERY EXACT ROW OF THIS TEXT?

**Reference:** the oracle's own five arms × five salts, leg A: the 25 filed G3 traces (re-produced byte-identically by the
hooked oracle re-run, `oracle_channel_hook.py`) and the oracle source at `22cd2288`. **No port outcome enters.**

**Measured on the 25 reference traces by `check_v1p13_draft.py`:**

<!-- FILL:lawa -->
| row | basis | oracle passes? | detail |
|---|---|---|---|
| `TA-X-01` | MEASURED (this draft, 25 reference traces) | **PASS** | oracle re-run byte-identical to the filed trace 25/25 |
| `TA-X-03` | MEASURED (this draft, 25 reference traces) | **PASS** | 5/5 full-trace equality |
| `TA-X-04` | MEASURED (this draft, 25 reference traces) | **PASS** | 5/5 full-trace equality |
| `TA-X-05` | MEASURED (this draft, 25 reference traces) | **PASS** | differ on 5/5 salts (>= 1 required) |
| `TA-X-08 (restated, both identities)` | MEASURED (this draft, 25 reference traces) | **PASS** | 25/25 |
| `TA-X-10` | MEASURED (this draft, 25 reference traces) | **PASS** | W1 max body radius 43.404815 m, max spawn radius 43.588163 m <= 43.758085029822276 |
| `TA-X-12` | MEASURED (this draft, 25 reference traces) | **PASS** | no damage tag containing 'pool' on any leg-A event, 25/25 |
| `TA-X-15(a)` | MEASURED (this draft, 25 reference traces) | **PASS** | p01-p04 at 0.0 s, p05 at 4.0 s (tick 49), every wave played, 25/25 |
| `TA-X-16 (restated)` | MEASURED (this draft, 25 reference traces) | **PASS** | 25/25 |
| `TA-X-17` | MEASURED (this draft, 25 reference traces) | **PASS** | max ‖spawn − anchor‖ = 7.956549 m <= 8.0 |
<!-- /FILL:lawa -->

**Cited, not re-measured here** (the row is structural, a no-run census, or graded on an object the traces do not carry).
The oracle tree is the same object jack-ryan audited for v1.12 (ea0317306 Item 7, at `22cd2288`; this file verified no
tracked modification under `simulation/kc2`, `export`, `simulation/scripts`), and none of these rows changed text:

| row | oracle passes? | basis |
|---|---|---|
| `TA-X-02` | PASS (structural) | the census mapping of the 89 oracle ids; no outcome |
| `TA-X-07` | PASS (structural) | per-packet booking closure; (c)/(L2): reference cells ≤ 1,168 ticks, inside the port's longest passing cell (ea0317306) |
| `TA-X-09` | PASS (no run) | the nine vectors are the oracle's `math_rules`; ROWSET reproduces (PINS) |
| `TA-X-11` | PASS | H-9 (documents of record reproduce, PINS) |
| `TA-X-13` | PASS (structural) | `CritLimb` LO in V0 (`player_offense.py:140`) |
| `TA-X-14` | PASS (structural) | release causes Type A / Type B only (V15-11) |
| `TA-X-15(b)` | PASS (by construction) | no intra-point stagger (`TA-X-15(a)` measured above) |
| `TA-X-18` | PASS | recomputed on the oracle's `SpawnStructureFold.offset`; bits equal (PINS) |
| `TA-X-19` | PASS-vacuous | no arrival limb |
| `TA-X-20` | PASS (structural) | census D7 hit predicate |
| `TA-X-21` | PASS | the oracle's four `round(` sites (1561/1681/1714/2052) are Python 3 half-to-even |
| `TA-X-22` | PASS (structural) | no `interrupts_channel_flag` cause under `ORACLE` (V0; V18+V19) |
| `TA-X-24` | PASS (structural) | V0 attack phase `ENGAGE` |
| `TA-X-25` | PASS (structural) | (a) PLAY-only rule; (b) identity; (c) set digests reproduce (PINS) |
| `TA-X-26` | PASS (no run) | derived from `P-i` by script; `P-i` reproduces (PINS) |
| `TA-X-27` | PASS | (b) CPython; (c) the oracle's draws are the reference (0 mismatches in G3); (a), (d) scan and pack |
| `TA-X-28` | PASS (structural) | no leech cap in the oracle |
| `TA-X-29` | PASS | (e) the oracle's own walk (643/643, KP-175) |
| `TA-X-30` | PASS (structural) | the halt is the oracle's law at `d_engage_m` = 2.4 |

**Result: the oracle passes every EXACT row of this file** (measured rows above + cited rows here). The two rows that
failed the v1.12 audit (`TA-X-16`, `TA-X-08` identity 2) are the two this file restates, and both now pass 25/25.

⚑ **Law (b) (regime change), applied:** the restatements make no new state reachable. Identity 2's new term reads a state
(control suppression with the fold channelling) that KP-147 made reachable; every row reading channel state was re-opened
for this file: `TA-X-14` and `TA-X-22` read release **causes**, not counts (unaffected); `TA-X-07` books packets, not
channel ticks (unaffected).

---

## § L · MATT'S RULINGS ON Q96, AS CARRIED (KP-182, KP-183)

| part | ruling (verbatim) | where |
|---|---|---|
| Q96.1 | *"Per played wave."* | § F.2m |
| Q96.2 | *"Keep 1 remaining."* | § G.1 |
| Q96.3 | *"Yes, as a precondition"* — the 28 graded rows read off the candidate emission before attempt 2; expected values and tolerances frozen in v1.13 first | § G.1a |
| Q96.4 | *"Add control term"* — with `n_released` on D and a doubly-suppressed tick counted as released | § F.2n |

**Not a Q96 part, carried as written:** § C.9.5a widens G3 (an attempt precondition) by two equalities, because if the port's
own generator keeps resisting every control application the new term is exercised only there (§ F.2n.5). Already met at
`05508a0` (§ PINS.2).

⚑ **Context recorded with Q96.1 (KP-182):** the REFERENT (Matt's recorded run) dies at w160; the ORACLE (the Python model T-A
grades the port against) dies at w151–w156, the declared lethality gap. `TA-X-16`'s old "47" was the referent's ten waves
leaking into a port ≡ oracle row. Reaching w160 stays a REFERENT-v2 goal; it is not graded here.

---

## § Z · HOW THIS FILE WAS MADE

From gamora's draft (collab `0b2fceb06`, KP-181) by its § Z: the banner stripped; § G.1 and § G.1a written from Matt's
ruling; `pins_v1p13.py`, `check_v1p13_draft.py` and `fill_draft.py` re-run (all exit 0) with drax's `05508a0` runtime
re-pinned; committed ALONE (D4). The instruments were committed first, separately, in the draft folder.

---

### The instruments and outputs behind every filled block (`agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-prereg-v1.13-DRAFT/`)

<!-- FILL:files -->
| file | sha256 |
|---|---|
| `pins_v1p13.py` | `3a62451fe34b561cea961266ba7c396a5d2ed81ecfe91b148a04ed1fda8af462` |
| `pins_v1p13.json` | `8102fb37eade6fd3d0151c49eb91fb91bd372377b5032aa123801b15913bf8c5` |
| `pins_stdout.txt` | `b3c55fec034234ed711ebbb1f915e5169088ae0b44507d8a3fad3d7536c41fc5` |
| `oracle_channel_hook.py` | `dce0625d30cd09289c7b073923ac4d1c732763614c5f9f30b08cedc96eab6cd9` |
| `check_v1p13_draft.py` | `a222b0d1f2e9b300f945e4b5fd8797f72c99e25dff20129c9e560add38ac1b5f` |
| `results.json` | `1f7e3c8ac93af103b75999fedd676f2f539c6dfa0241f6b58fc6132a095504bb` |
| `run_stdout.txt` | `a255888de29671bd14307566a34df1a8067f2658220ca5a460cc3a6f67752953` |
| `fill_draft.py` | `d0ad4542ecf72a9c34b3a49cb7d536803117d1f1ae25fc229a9bba239d8b0263` |
| `oracle_hook/rerun_trace_sha256.json` | `2cc3f684a6b509289e7a6e66cb35ae9e34650d2c4c81457cb7549741a9e5c602` |
| `oracle_hook/*.hook.json.gz` | 25 files (one per cell; gzip mtime 0) |
<!-- /FILL:files -->

---

## § J · DISCIPLINES THIS VERSION EXERCISED

> ⚑ **A RESTATED ROW IS THE ORACLE'S LAW, CHECKED ON THE ORACLE BEFORE ANYONE GRADES AGAINST IT.** Both restatements were
> written from source (`wave_engine.py:305-307`; `run.py:2810-2815`, `channel_policy.py:297-392`) and then measured on the
> oracle's own 25 realisations. The texts they replace fail the same check. KP-178 law (a), applied first to the rows that
> motivated it.

> ⚑ **AN INSTRUMENT THAT READS THE ORACLE MUST SHOW IT DID NOT TOUCH IT.** The hooked re-run's traces are byte-identical to
> the filed ones, 25/25; the control term is counted two independent ways and they agree 25/25.

> **Carried:** math before code (#1); attribution (#10: every cross-reference named, none used as an expected value);
> empirical inspection (#11: identity 2's operands read per tick, not inferred from totals); semantic shifts named (#12:
> both restatements, the census convention, P-2's reading, § C.9.5a); digests computed by script, never typed; K-7 held
> (sealed cells hashed only).

---

*Filed 2026-10-01 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY; conductor gandalf.

**What v1.13 does:** restates `TA-X-16` per wave played and `TA-X-08` identity 2 with the seal's control term (both by Matt's
ruling, both derived from the oracle's law, both passing on the oracle 25/25 where the texts they replace fail); writes the
census convention, P-2's operational reading and the zero-equals-absent digest law; widens G3 by two equalities; keeps the cap
at **`1` of `2` remaining**; makes the 28-row pre-attempt read a precondition with jack-ryan as its seat. **No tolerance moved.
NO BAND WIDTH MINTED. The declared set is closed at exactly `["TA-X-06"]`. K-7 held.**

**What this session touched, and how:** the oracle only through drax's unchanged G3 oracle tool (run under `runpy` with
read-only hooks; traces verified byte-identical) and the entry points listed in PINS; godot only through `git show`; the packs
read, modified in nothing. **v1.12 and every earlier version are NOT edited.**

⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run or the § G.1a read exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
