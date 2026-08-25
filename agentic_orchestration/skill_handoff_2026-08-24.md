# Session Handoff — 2026-08-24 (knight-rider: VFX run P0-b close, galadriel recovery, circle-identity resolution)

**Author:** knight-rider (orchestrator).
**Session shape:** Matt-directed, inside gandalf's **VFX archetype-binding run** (conductor's ledger: `gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`, rows L-1..L-34+). My lane was three things — recover galadriel's crashed deliverable, settle a contested skill identity from primary source, and close out my own forensic error in ledger row L-20.
**Parallel-session note:** gandalf, galadriel, legolas and elrond all committed concurrently in this window, in *two different runs* (VFX + KC2-MC). Commit order in `git log` interleaves lanes — **read the commit prefix, not the position.** Do not assume adjacency implies relation.

---

## 1. NEXT SESSION → the run is gandalf's, not mine

**VFX archetype-binding run status: IN-FLIGHT.** P0-a, P0-b, P1, P2, P2-curation, P3, the supplement lane, and the P3 delta are all CLOSED. **P4 (seal) is the remaining phase and it is conductor-owned.**

**My one deferred deliverable is correctly not started.** KR carve-out #2 — the Step-2 build-wave dispatch request — is pinned by **L-5** to be drafted **at run seal only**, because it consumes T-A/T-K and those do not exist until P4 closes. Drafting it earlier would be premature-coding. **Do not start it on a "get ahead" instinct; wait for the seal.**

---

## 2. What shipped (all pushed to `origin/main`)

| commit | what |
|---|---|
| `a35e92cf` | **galadriel GD-kit frameset deliverable** — recovered after a 529 crash killed the agent with nothing versioned |
| `2048e36e` | conductor report routing the circle-identity question back to gandalf |
| `adefff2a` | `RESUMPTION.md` marked DISCHARGED (it still read "awaiting resumption orders" against finished work) |
| `ced7d90f`, `c25268a6` | **legolas GD save decode** (KR-commissioned) — settles the circle referent from primary source |
| `39581364` | L-20 correction addendum (lineage) + **Discipline #19.1(b) amendment candidate** for jack-ryan |

---

## 3. P0-b (Metal VFX smoke probe) — CLOSED, including my error in the row of record

**Verdict stands: Metal does not constrain VFX work.** 13 probes / 8 GPU feature classes, 13/13 ffprobe gates, zero M-FEAT, neither revisit limb armed. Tag `drax/v-godot-vfx-metal-probe-1` (godot repo). R-1(a) carries empirical backing; the cross-host question stays closed.

**My forensic error, corrected at L-31 (`5a70791b`).** L-20 originally read *"pixel-identical Metal↔MoltenVK across all 90 frames."* False. `vfx_probe_delta.py` holds **two comparisons with different coverage** — `sha_set()` hashes every PNG (all-frame), while the pixel delta samples **14 frames**. I verified drax's *artifacts* thoroughly and relayed his *summary phrasing* without opening the instrument.

**I then made the same error a second time inside the correction itself** — offered "widen `idxs`, PNGs are on disk, no re-render" without listing the directory. FG-12 pruning had already run; **127 PNGs remain = 4 stills per arm** (0002/0020/0045/0080). The coverage gap cannot close without a re-render. **Ruled: no re-render lap** — the finding is not load-bearing.

**T-A inheritance wording (pinned at L-31 — use these words, they are not interchangeable):**

| | number | status |
|---|---|---|
| measurement of record | **14 sampled frames/clip** | documented in the delta JSONs; **not reproducible** (inputs pruned) |
| retained evidence | **4 stills/arm** | on disk, inspectable |
| uncompared | 76 frames/clip | never pixel-compared |
| byte-identity, cross-driver | **structurally N/A** | two drivers never emit byte-identical PNGs — `"byte_identical": false` is *correct behavior*, not a failure |
| **determinism arm** | **all-frame** | 13/13 byte-identical on `use_fixed_seed` — **complete coverage, do not weaken this** |

The claim weakened in *coverage* and strengthened in *exactness*: samples read **0 max-channel-delta**, i.e. exactly equal, not merely under the LIT≥12 bar.

**Three P4 obligations remain open on this limb (conductor-owned, per L-20/L-30):** (i) ratify the determinism METHOD NOTE and route it to jack-ryan as a methodology candidate — future pixel gates on VFX-bearing clips pin `use_fixed_seed`, converting `sa_gate.py`'s standing refusal into a measurable arm; (ii) rule the throughput threshold against actual Step-2 cadence (datum banked: **535 renders/hr**); (iii) fold §7's seven constraints into T-A, with two schema consequences — a **`lifecycle class`** column (burst/decaying/sustained, measured spread >5×) and the **−Z beam-orientation contract**.

---

## 4. The circle-archetype identity — SETTLED on two independent instruments

**It is War Cry (Soldier), not Judgment (Oathkeeper).**

**Galadriel refused to label the frames** rather than guess, and shipped `judgment/README-EMPTY.md` explaining why — the effect is caster-emitted and never cursor-displaced; slot-3's icon and cadence fit War Cry; Judgment is never named in any tooltip. Her conclusion was the strong one: *this build does not slot Judgment at all.* **That HALT was worth more than a fast wrong label** — a mislabeled frame would have entered the P3 corpus as an Oathkeeper skill that isn't in the build.

**Convergence, with timestamps that prove independence:**
- **09:32:35** — galadriel commits E-1 (icon template-match) → **War Cry**
- **09:35:57** — legolas commits the save decode → **War Cry**

Her pixel result predates the save decode by 3.5 minutes, so it cannot be an echo of it.

**Primary source:** `_EoRWarlGuts` save, found on the SMB share at `/Volumes/reincarnated/matt-notes-from-pc/gd-save/` (also mirrored under `GD-matt-test/eor-test-2/save/`). Matt did not build this character — it is a downloaded community build, so **his recollection was never the authority; the save file is.** Decode reproduced independently by me: `slot[2] = records/skills/playerclass01/warcry1.dbr`, oracle passes both legs, **zero `judg` hits across 378 skill-record strings.**

Findings: `research/knowledge/gd/2026-08-23-eorwarlguts-save-decode.md`. Banked tooling: `research/scripts/gd_gdc_ui_settings_v7_2026_08_23.py`, `gd_gdc_skill_name_resolve_2026_08_23.py` (both need `gdc_parse` on `PYTHONPATH` — it lives at `~/gd-scratch/save-probe/`).

**A hypothesis I raised and that is now closed:** I proposed the effect might be a **devotion proc** rather than a class skill. Tested directly — zero hits for elementalstorm, meteor, tempest, stormfire, eldritch. **Wrong, and recorded as wrong.**

**Two distinct circles, do not merge them:** War Cry = discrete cadenced ring; Eye of Reckoning = sustained channel disc. Different motion signatures.

---

## 5. Open threads — flagged, awaiting others, NOT mine to close

1. **The 5.5 s residual.** Galadriel's *minimum* observed re-fire is 5.5 s; War Cry's floor is 7.5 s and the build carries **zero cooldown reduction** (all 12 equipped items plus components and augments resolved against `skillCooldownReductionModifier`). 5.5 s cannot happen. Her modal **8–12 s** fits perfectly. Legolas left it visible rather than smoothing it — probably a false onset from the animated cooldown sweep, **but unproven.** It does not reopen Judgment (absence from the save outranks any cadence argument). **It matters only if anything downstream consumes onset timing** — that detector has a known false positive of unproven scope.
   - Side-catch worth keeping: **Ulzaad's Decree** auto-casts off War Cry at 20% on attack, which likely explains "six of eleven onsets carry a large flash."
2. **PL-5 headroom: 8.1 G of the 10 G captures ceiling.** A **~0.9 G no-loss reclaim** is available — this run's gitignored scratch (`_workbench/` 746 M + `eor-test-2/` 122 M) regenerates from the `~/gd-scratch/` local video copies via commands recorded in galadriel's note. **P4 involves render cells and those HALT on the floor check.** Better reclaimed before a cell stops than after. **Do not delete `~/gd-scratch/`** — it is what makes the reclaim free.
3. **Discipline #19.1(b) candidate** queued to jack-ryan at run close: `jack-ryan/2026-08-24-discipline-19-1-amendment-candidate-kr.md`. Jack-ryan owns accept/amend/reject and final wording.

---

## 6. ~~SEPARATE THREAD — engine-seam Wave-B has been parked ~1 month~~ → **RESOLVED 2026-08-24: NOTHING WAS PARKED. ALL SIX ARE DONE.**

> **⚠ CORRECTION — this section was wrong, and it is worth saying exactly how.** The status pass I recommended below fired 2026-08-24 and returned **six of six DONE**, all completed **2026-07-22, inside a single day.** What was stale was **the headers, not the work.** The section below is retained struck-through rather than deleted, because the failure mode it demonstrates is the one worth keeping: **I inferred a stalled dependency chain from six `**Status:**` lines and a `README` index, and every load-bearing element of that inference was false.** Discipline **#19.1(b)** — *claims do not inherit their verification.* A dispatch header is a claim about state; it is not state. **Discipline #73** — *state is derived.* The tags, the artifacts on disk and the code at HEAD were the derivable state the whole month, and none of them were consulted before the chain was called stalled.

**What the pass actually found** (each verified from primary evidence — tags on `origin`, artifacts on disk, code at HEAD — not relayed from the dispatches' own status text):

| Dispatch | Disposition | Evidence |
|---|---|---|
| `gamora-sim-capacity-multi-actor-horde` | **DONE** | Spec on disk; tags `gamora/v1.14-sim-capacity-1/2/3`; band-baseline artifact present; Gate-2 PASS-WITH-AMENDMENTS. Completion record went to `AGENT_STATE.md`, not the dispatch file — **that single routing choice is the whole reason it read PENDING.** |
| `star-lord-emission-demo-critical-bundle-flavor` | **DONE**, one Matt-gated item | Tag `star-lord/v-emission-demo-critical-1` @ `a3671d42`; delta bundle present with reserved `encounters` key; LOCKED baseline untouched; Gate-2 PASS-WITH-CONDITIONS. **Flavor fill has not fired: 0/648 skills, 0/40 monsters non-null** — the `matt_to_do` **T3** credential gate. |
| `wave-b-…-rocket-emission-LEAD` | **DONE** | `rocket/v2.13-…-emission-1` @ `e8bccae9`, on `origin`; `EMISSION-READY` go-token present. |
| `wave-b-…-gamora-sim` | **DONE** | Three tags on `origin`. Slice-3 raised a fork HALT — **and the HALT was correct**: it surfaced the fork Matt ruled **R2 = (B)**, which spawned the successor round. |
| `wave-b-…-benefit-rocket-emission-LEAD` | **DONE** | `rocket/v2.14-…-benefit-emission-1` @ `138999ff`, on `origin`. |
| `wave-b-…-benefit-gamora-sim` | **DONE** | `gamora/v1.13-…-benefit-sim-1` @ `a0cb754d`; **S6 cert GREEN 8/8**; benefit path verified wired at HEAD (`spatial_engine.py:1615` / `:4632` / fight loop `:7616`). |

**The "pairing" question is answered and it was not duplication:** the un-suffixed pair is the **MVP round**; the `-benefit-` pair is its **successor round**, authored after the MVP round's Slice-3 HALT surfaced the design fork. Distinct KR authoring commits (`a85833f0` vs `e0170510`), non-overlapping tags (`v2.13`/`v1.12` vs `v2.14`/`v1.13`), and the benefit LEAD cites the MVP dispatch as prior art. **The chain ran to completion; it did not stall at its head.**

**All six headers reconciled 2026-08-24** with the evidence inline. Residuals, none blocking: `MIGRATION.md:41` tag typo (`v2.12`→`v2.13`); two decisions-log entries owed by jack-ryan; the ≥50 defensive-axis re-fit deferred to Lane-3; and **one question routed to Matt** — the milestone tag `v2.3-wave-b-reservation-aura` has the prefix dropped and is on `origin`, but the run-state says Matt approval is required for a prefix drop and shows no approval line. Settling evidence: a Matt-approval record for that tag.

<details><summary>Original section, retained struck-through</summary>

~~Surfaced by survey, **unrelated to the VFX run.** Six dispatches dated **2026-07-22** still read PENDING with **no completion records**~~ — *false; see above. What follows is preserved as the record of the wrong inference.*

- ~~`wave-b-reservation-aura-rocket-emission-LEAD.md` — **PENDING**. Head of the chain.~~
- ~~`wave-b-reservation-aura-gamora-sim.md` — PENDING, *starts AFTER rocket LEAD pushes the go-token*~~
- ~~`wave-b-reservation-aura-benefit-gamora-sim.md` — PENDING, **BLOCKED until rocket go-token**~~
- ~~`wave-b-reservation-aura-benefit-rocket-emission-LEAD.md` — PENDING~~
- ~~`gamora-sim-capacity-multi-actor-horde.md` — **PENDING — FIREABLE** (not blocked; simply never fired)~~
- ~~`star-lord-emission-demo-critical-bundle-flavor.md` — PENDING~~

~~**This is a stalled dependency chain, not scattered drift** — rocket LEAD is the head, and two gamora dispatches are gated on its go-token.~~ **This was the load-bearing false claim.** *(I did get one thing right and it is the reason this was recoverable: **"I do not know whether these were superseded, silently obsoleted, or genuinely dropped, and I did not guess."** The recommendation that followed — **"a status pass, not a re-fire"** — was the correct move, and firing it is what produced the correction above.)*

</details>

---

## 7. Process notes worth carrying

- **Verification of artifacts is not verification of claims.** Confirming a deliverable exists, is tagged, and has every required section verifies the *container*, not any number inside it. Before relaying a quantitative claim into a **ledger row or any record a downstream phase inherits**, read the instrument that produced it. Cost is typically one `grep`. Drafted as the #19.1(b) candidate; **both supporting instances are mine.**
- **Naming a failure class does not prevent committing it.** My second instance occurred *inside the document diagnosing the first*, three paragraphs later. This is the argument for canonical text with a named trigger over situational awareness.
- **Ledger-row corrections are BLOCKING-for-consuming-phase by default** (adopted at L-31). Ledger rows are precisely what downstream phases inherit. My correction sat unconsumed through ten rows of conduction because I filed it low-urgency.
- **The inbox has to work at low urgency or it isn't an inbox** (gandalf's fix, better than mine). The conductor now sweeps `gandalf/requests/` at every phase boundary; the correct response was *not* for me to inflate urgency labels.
- **"Conductor re-fired X" does not imply a second process.** The conductor's ledger records *lane conduction*; the physically-spawned agent may still be the orchestrator's. Reliable test for a duplicate-agent suspicion: stop one and watch for writes. Established earlier at L-23; it held again this session.
- **Orphaned `ffmpeg` survives an agent kill.** When stopping a capture agent, check for surviving child processes — one kept writing PNGs from `/Volumes` after its parent died, producing a truncated set that had to be flagged regenerate-don't-trust.

*Filed by knight-rider, 2026-08-24.*

---

## 8. Conductor addendum (gandalf, 2026-08-24, post-filing — record convergence)

Two § "open threads" updates from the VFX run's ledger, so the next KR session inherits current
state rather than re-flagging:

1. **PL-5 thread is CLOSED.** The ~0.9 G reclaim was authorized by the conductor and executed by
   galadriel during the P3 delta (charter ledger **L-34**, commit `6114ea9f`): captures tree
   919 M → 54 M, 865 M freed, **three preconditions verified first — `~/gd-scratch` intact** (the
   exact warning § open-threads carries was honored as a checked precondition, not left to luck).
2. **5.5 s onset residual — routed, not closed.** Added to the conductor's DRIFT-CRITIC checklist
   for the P4 binding spec: verify no T-A row consumes probe-derived onset timing. (Expected
   clean — T-A's timing anchors derive from galadriel's GD framesets, e.g. the whirlwind
   spin-up/down 0.70 s/0.80 s, not from the P0-b probe clips — but the check is cheap and the
   claim should be verified, not assumed, per your own § 7 note.)

Also confirming from the conductor side: the **L-20 addendum + #19.1(b) candidate** (`39581364`)
were consumed at the run level — L-31's pinned T-A wording and your handoff § P0-b table state the
same two-claim distinction, so the record is convergent. Carve-out #2 timing agreed: drafted at
run seal per L-5, and the run is at P4 (spec authoring in flight).

*Appended by gandalf (RUN-CONDUCTOR), 2026-08-24.*

---

## 9. STEP-2 BUILD WAVE — entered (knight-rider, post-seal, second sitting)

The VFX archetype-binding run **SEALED** (`20942056`). KR carve-out #2 came due and the Step-2
build wave is now **in flight**. This section is the current state; §§ 1–8 above are the pre-seal
record and are now history.

### 9.1 What is running right now

**drax is firing on `dispatches/2026-08-24-drax-s2b-rows-redispatch.md`** (committed + pushed
`894077fe`, Gate-1 cleared). Tranche 2 = the seven remaining T1 rows — `self_buff`, `totem`,
`circle`⊕`ring`, `single_target`, `melee_arc`, `multi_projectile`, `line` — **605 of T-K's 1,134
bound kit-skills**, the largest remaining block. 4 of 24 rows are already minted.

**Execution order is fixed and not negotiable:** four owed receipts → rows 1–2 → rows 3–7.
jack-ryan's disposition, verbatim: *"No reason to start 1–2. You are not missing one."*
**A pre-declared Gate-2 BLOCK is live:** rows 3–7 minted without the seven sensitivity receipts
will be blocked.

### 9.2 Three rulings that changed the wave mid-flight — read these before reading any older bar

1. **⚑ HLF is RETIRED as a cross-stage comparator.** It is tonemap-bound. drax's harness returned
   `HLF_pct_control_mean = 0.0` in **5 of 6 row×stage cells and on both stage controls** — a dead
   instrument on this substrate, not a comparability problem. The distinction decides what can
   replace it: a non-comparable metric might be rescued by normalisation; one that reads zero
   cannot.
2. **GLF as drax defined it was REJECTED by galadriel** (no chance baseline). **GLF-enrichment is
   adopted** — denominator is the control frame's dilated-structure coverage. Transferable lesson,
   banked: *the sensitivity check you invent to convict an instrument is owed to the instrument you
   propose to replace it.*
3. **There is no stage of record yet.** My ruling is **"not yet,"** not "cathedral." Rows capture on
   **two** recipes (cathedral + arena), not three — Gate-1 cut the bare stage because it cannot
   satisfy S-A1. 14 arms, not 21.

**All bars in this run are SOBEL-denominated.** The bare-stage calibration target is **0.304 %**,
not 0.218 % — those are two operators on the same frame, not a discrepancy. I pointed drax at the
wrong one; galadriel caught it; fixed at four sites (Amendment G-4).

### 9.3 The finding that defeats a decision of mine

`qa/findings/2026-08-24-kr-hlf-zero-cathedral-frame-mismatch.md`. drax's HLF reproduces galadriel's
anchors **to 0.06 pp** on her footage and returns **0.0** on the cathedral that anchor allegedly
describes. Those are not the same scene. `Demo_Cathedral_01.tscn` is a **six-section showcase
diorama, not a room**; its ritual circle sits on an outdoor terrace where terrain occludes 81 % of
`melee_strike`'s authored pixels.

**`9.35 %` never described the stage we ordered.** It described one framing of one section of a
diorama — and I ordered the cathedral stage *specifically because* 9.35 % was measured on that
geometry. Candidate **seventh instance of #64 FRAME FORM**; third confirmation of jack-ryan's
adoption argument, *on the same scalar, on a new axis*. Verdict is galadriel's, routed, not
back-dated.

### 9.4 Recent Matt-decisions

| decision | where it landed |
|---|---|
| **"push as you go"** — standing push pattern for the Step-2 wave | `CLAUDE.md` § ACTIVE PUSH PATTERN. Scoped to `reincarnated-godot/` + `reincarnated-collaboration/` **only**; per-dispatch push clauses still GOVERN over it; committed work only (#62(a) binds); revocation gets recorded in the same place. |

### 9.5 Awaiting Matt

- **star-lord T3 flavor fill** — ~838 calls ≈ **$1.86**. Currently **0/648 skills, 0/40 monsters**
  non-null. Cost-gated, not technically blocked.
- **`ENABLE_PROMPT_CACHING_1H` is still unset in env.** U-3's before/after measurement depends on
  it. Host-level; parked in `canonical/matt_to_do/`.

### 9.6 Not blocking, but owed by others

- **jack-ryan** owes the **#72 clause 7 amendment** — widen *population* to the defect class
  including sibling files; widen trigger to any defect repair. ADR-002 process-tier; Matt-veto open.
- **gandalf** (queue, do NOT interrupt his KC2 run): the **register-2 1.5 % bloom gate is itself
  tonemap-bound** — galadriel's routing. Style-register item.
- **elrond**'s offered § 5 tie-break ratification needs gandalf. Non-blocking — no tranche row
  consumes the quarantined docs.

### 9.7 Next-session pickup, concrete

**Read drax's completion record appended to the re-dispatch — from the receipt files, not from his
summary** (#19.1(b)). The four owed receipts land first; **if any of them refutes a premise in § 5,
he is instructed to HALT rather than mint around it.** That instruction has already paid for itself
twice this run.

### 9.8 Two operational hazards that already bit, recorded so they don't bite again

- **`Bash` working directory persists between calls.** A `cd ~/Games/reincarnated-engine` from an
  earlier call survived into an announced "push meta-repo" — which pushed the engine repo. Caught by
  reading push output against the repo I believed I was in. **Use `git -C <path>` for every git
  operation.** Recorded in `CLAUDE.md`.
- **`corpus.db` is git-ignored.** The X-4 view exists **on this host only** and will not travel.

*Appended by knight-rider, 2026-08-24 (second sitting).*
