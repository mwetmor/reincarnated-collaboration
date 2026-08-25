# MATT DECISION NEEDED — `spark`: does lightning keep its best word, or has wind already spent it?

> **Raised:** 2026-08-24, Step-2 VFX build-wave close. jack-ryan ruling batch, item 4 — mechanical half APPROVED to rocket (report-only predicate), **vocabulary half routed to gandalf to draft and Matt to rule.**
> **Severity:** WARN. Blocks nothing now. **Gating criterion: the next season-emission run.** Any emission fired before you rule may burn the name.
> **Drafted by:** gandalf (SPEC-AUTHOR / journey-shaper). Every number below re-derived from the live artifacts, not inherited from the finding (Discipline #76 clause 2). **Nothing here is pre-committed. No pool data was changed.**
> **Authority this touches:** `canonical/reap-die-rise-engine/substrate-expansion-decision-2026-05-17.md` § 7.1 — a doc you ruled (Branch A, 2026-05-17). Amending its frozen list is above ADR-002 documentation-tier, which is why it is here and not decided in-seam.

---

## § 0 — The one-paragraph version

`spark` is lightning vocabulary sitting in the **wind** slot of live season emission, at 2× sampling weight, today. jack-ryan graded this a fifth instance of the substrate-leak class that § 7.1's own `bolt` row describes — correctly. But the origin is not a design judgement anybody made: **`spark` was a `fire` word with a `wind` flex until 2026-06-01, when the WS1A Q18 lock re-slotted it to `lightning` and left the wind flex behind.** It is the only one of 39 frozen-primary entries carrying a live-substrate flex, and the only pre-existing entry that lock re-slotted. **My lean: strip the wind flex, change nothing else** — a one-field repair of an incomplete migration, costing no vocabulary and creating no new standing constraint. The alternatives, including demotion, all cost more and buy less.

---

## § 1 — What is true, re-derived

All figures from `data/seasonal_elements/pool.json` + `vfx_coverage_manifest.json` + `data/kit_space/kits/` at engine `9307b46b`, verified by loading the pool through `load_element_pool()` rather than reading the file at rest.

**`spark` today:**

| Field | Value |
|---|---|
| `primary_slot` / `substrate_native` | `lightning` (a frozen substrate) |
| `flex_slots` | `["wind"]` — **live** |
| `d1_status` at rest **and after load** | `allow-list` |
| `vfx_mapping_tier` / `clean` | **A / true** (via manifest join) |
| `tags` | `["electrical", "brief", "small"]` |
| Sampling | `D1_ALLOW_LIST_WEIGHT = 2` (`element/selector.py:63`) |
| Selectable? | **Yes** — `selector.py:555` admits `primary_slot == slot or slot in flex_slots`; wind is a live slot |

**It is alone.** Of 39 entries with `primary_slot ∈ {lightning, holy, shadow}`, `spark` is:
- the **only one that survives `load_element_pool()` at `allow-list`** (the other 38 auto-demote to `eligible` on the Drift-14 gate, because they are absent from the VFX manifest); and
- the **only one with a non-empty `flex_slots`.** All 38 others are `[]`.

So the class jack-ryan named has, in the live artifact, exactly one member. That is not a reason to dismiss it — it is a reason the remedy can be small.

---

## § 2 — Where the wind flex came from (this is the part that changes the decision)

I traced the entry through `pool.json` history:

| Date | commit | `primary_slot` | `flex_slots` | `substrate_native` |
|---|---|---|---|---|
| 2026-05-08 | `c14d94ef` | **fire** | `["wind"]` | — |
| 2026-05-17 | `65e6d77e` | **fire** | `["wind"]` | — |
| 2026-06-01 | `fcc48872` | **lightning** | `["wind"]` | lightning |

**`spark` was a fire word.** Sparks fly off a forge, off flint, off a grinder — and a fire word with a wind flex is unremarkable: embers blow. That flex was coherent for the twenty-four days it existed under `fire`.

On 2026-06-01 the WS1A Q18 lock re-slotted it to `lightning`. Derived from the same two commits: that lock **added 38 new frozen-primary entries (every one with `flex_slots: []`) and re-slotted exactly one pre-existing entry — `spark` — carrying its obsolete flex across unchanged.**

**Nobody ever judged that lightning-spark is wind-coherent.** The wind flex is residue from a slot assignment that no longer exists. That reframes the ruling: this is not "demote live working vocabulary to protect an unshipped substrate." It is "finish a migration that stopped one field short."

**Corroborating: the same lock left three other stale artifacts in one file.** `vfx_coverage_manifest.json` disagrees with `pool.json` on `substrate_native` for exactly three entries — `frost`, `mist`, `spark` — and those are exactly the three entries that lock re-slotted. The manifest was never re-graded after it. The fourth stale artifact in that same file is the `vocab_freeze_note`, whose "none currently in pool.json" went false on that same date and stayed false for twelve weeks. One migration, one file, four stale artifacts. `spark`'s flex is the fifth.

> **A trap I fell into and am flagging so you do not:** the manifest says `spark`'s `substrate_native` is `fire`, with rationale *"Pimen fire-spell-effect direct; spark/ignition register."* I initially read that as an independent artist-side vote that `spark` is semantically a fire word, and drafted a re-slot-to-fire recommendation on it. **It is not a vote — it is a stale grade taken before the re-slot, and it is a claim about which catalogue folder holds the covering asset, not about the word's meaning.** The two fields share a name and carry different referents (Discipline #64). I withdrew the recommendation. Flagged because the field will mislead the next reader the same way.

---

## § 3 — The register question: whose word is `spark`?

You asked the real question underneath: **when lightning lands as a substrate, does it arrive to find its best vocabulary already spent as wind flavour?**

I measured it rather than asserting it. The kit-space corpus (411 kits, `data/kit_space/kits/`) already generates against all seven substrates and records `ws1a4_flavor_word_used`:

| substrate | uses | distinct words | distribution |
|---|---|---|---|
| **lightning** | 31 | 7 | **`spark`:7**, `surge`:6, `volt`:6, `static`:5, `thunder`:4, `plasma`:2, `flash`:1 |
| holy | 8 | 2 | `radiant`:6, `blessed`:2 |
| shadow | 27 | 5 | `void`:9, `necrotic`:7, `shade`:6, `soul`:3, `wraith`:2 |
| fire | 31 | 7 | `scorch`:12, `blaze`:6, `inferno`:6, `ignite`:3, `cinder`:2, `flare`:1, `combustion`:1 |
| wind | 33 | 7 | `cyclone`:9, `zephyr`:8, `gust`:5, `squall`:4, `gale`:4, `tempest`:2, `hurricane`:1 |

**`spark` is already lightning's most-used flavour word — 7 of 31, the modal choice — and appears in zero fire kits and zero wind kits.** The substrate-expansion build has already spent it on lightning and the corpus agrees with `pool.json`, not with the stale manifest field.

So the answer to your register question is: **not yet, but only just.** Lightning's word-space is genuinely good — `arc`, `bolt`, `flash`, `ion`, `plasma`, `shock`, `static`, `surge`, `tesla`, `thunder`, `volt`, `voltage` — twelve unambiguous words behind `spark`. Lightning is not starving. But `spark` is the one word in that set that a player would accept in three different elements, which is precisely why it is the one at risk and the one worth being deliberate about.

**The genre reads it the same way.** Diablo II's Sorceress line separated `Charged Bolt` / `Static Field` / `Lightning` / `Chain Lightning` and never used "spark" for a wind or cold skill; Path of Exile keeps `Spark` as a *lightning* projectile gem and has held that binding for eleven years; Last Epoch's Sorcerer uses `Static Orb` and reserves the spark register for its lightning tree. Where "spark" appears outside lightning it is almost always a *fire-ignition* word (Grim Dawn's `Flashbang`-adjacent fire tooling, Diablo IV's Sorcerer `Spark` is lightning again). **Nowhere in the genre is "spark" a wind word.** The current flex is the one assignment with no precedent anywhere.

**And one thing worth seeing about the whole set.** Holy has two words in use where shadow has five and lightning seven. `radiant` and `blessed` are doing the work of an entire substrate. If the six-substrate expansion is going to land with holy owning its word-space, holy's vocabulary is a thinner problem than anything happening to `spark`. That is not this ruling — I am flagging it so it does not surface later as a surprise.

---

## § 4 — The forks

### Fork A (THE RULING) — what happens to `spark`?

| | Option | What changes | Cost | Verdict |
|---|---|---|---|---|
| **A1** | **Strip the wind flex.** `flex_slots: ["wind"] → []`. Nothing else. | `spark` leaves live season emission (its only live slot was wind). Keeps `allow-list`, keeps tier A / clean, keeps `substrate_native: lightning`. | Wind's live allow-list candidate pool goes **7 → 6** (`cloud`, `gale`, `gust`, `hail`, `sleet`, `zephyr`). | **★ LEAN** |
| A2 | **Demote to `eligible`.** | Drops to 1× weight, stays wind-selectable. | Loses a tier-A graded asset's status *and* does not stop the leak — `spark` still lands in wind, just less often. Half a fix. | Reject |
| A3 | **Re-slot to `fire`** (restore its pre-2026-06-01 home). | Fire pool 13 → 14; wind 7 → 6. | Contradicted by the `electrical` tag and by 7 lightning kits / 0 fire kits. This was my first draft and the evidence killed it. | Reject |
| A4 | **Add `spark` to `_VOCAB_FREEZE_IDS`.** | Mechanical demote at load. | jack-ryan already rejected this: it repeats the enumerate-instead-of-derive defect one entry at a time — #76 instance 4 arriving as its own remedy. | Reject |
| A5 | **Let it stand** — rule `spark` genuinely wind-coherent. | Nothing. | Defensible only on "wind is thin and it's working." But no genre precedent exists for spark-as-wind, and the flex was never a judgement in the first place. | Reject |

**Why A1 and not the others, in one line each:**

- **It costs no vocabulary.** `spark` is not demoted, deleted, or degraded. It keeps `allow-list` and its tier-A clean grade, so when lightning goes live at Phase-1 P1 it arrives **already promoted, already graded, already lightning's leading word** — zero re-promotion work. This is the option that *banks* the asset instead of spending or freezing it.
- **It creates no new standing constraint.** A1 is a fact, not a rule with an exit condition somebody has to remember. Given that this entire item exists because a standing constraint got stranded for eight weeks (§ 5 below), adding a fifth freeze would be the wrong lesson to draw from it.
- **It does not touch your 2026-05-17 ruling.** § 7.1's seven names are unchanged. A1 repairs a data row, it does not widen a freeze.
- **The wind cost is real and I am not hiding it.** Wind is already the thinnest live slot (7 vs fire 13, water 15, earth 15). A1 makes it 6. But the kit corpus shows wind's *actual* working vocabulary is `cyclone`/`zephyr`/`gust`/`squall`/`gale`/`tempest`/`hurricane` — words largely outside the live allow-list. **Wind's thinness is a real problem and it should be solved with wind-native words, not by keeping an electrical word on loan.** I have queued that as Fork C.

**Player consequence, concretely.** Under A5/status-quo, roughly one wind-slot season in six is titled from `spark` — a season whose displacement/impulse mode is named for a thing that does not move anything, presented to the player in the same register that will later name the lightning substrate. That is the exact "substrate-leak" your `bolt` row was written to prevent: the player learns "spark = wind flavour," and then Phase-1 P1 asks them to unlearn it. Under A1 the player never forms the wrong binding, and meets `spark` for the first time when lightning arrives.

**→ RULE: A1 / A2 / A3 / A4 / A5 / other.**

---

### Fork B (SECONDARY, related, please rule alongside) — the 38 that are held out by accident

The other 38 frozen-primary entries sit at `d1_status: allow-list` **on disk** and are held out of season selection only *incidentally*, by the Drift-14 gate firing on their absence from the VFX manifest. Nothing about the freeze is doing that work. The X-3 pass nearly graded them, which would have promoted 35 of them into live selection — rocket correctly declined, and that decline is what surfaced this whole item.

That is a stored value that is not the truth, held correct by an unrelated gate (Discipline #74 territory). **The fix is to set those 38 rows to `d1_status: eligible` at rest**, so the file states what is actually true and the Drift-14 gate stops being load-bearing for a job it was not designed for.

I have **not** done this and am not treating it as in-seam. It is a 38-row data change to entries created by your WS1A Q18 lock, and jack-ryan's ruling 2 established the principle that a seam-owner may not move the scope of a Matt-ruled decision by changing stored values. It is also not urgent — the current state is safe, just fragile.

**→ RULE: (B1) set the 38 to `eligible` at rest · (B2) leave as-is and rely on the Drift-14 gate · (B3) defer to Phase-1 P1 scoping.** My lean is **B1**.

---

### Fork C (FLAG ONLY — no ruling needed now) — wind is the thin slot

Live allow-list candidates per slot: fire 13, water 15, earth 15, **wind 7**. Under A1, wind 6. Meanwhile the kit corpus is happily using `cyclone`, `squall`, `tempest`, `hurricane` for wind — words that are not in the live allow-list. Wind's season-emission vocabulary is narrower than its generation vocabulary for no designed reason.

Not a decision for this ruling. Logged so that A1's cost has a named remedy rather than sitting as an unaddressed objection. Belongs in Phase-1 P1 pool scoping (§ 5.5 re-score).

---

## § 5 — Why this reached you at all

`spark` is not on § 7.1's list. § 7.1's `bolt` row states the rule the list enumerates — *premature promotion under wind/earth flex would create substrate-leak* — and `spark` satisfies it. The enumeration was implemented faithfully (`_VOCAB_FREEZE_IDS` is 4 of 4) and **the rule leaked.**

That is now **Discipline #76 instance 4** (*derive, don't enumerate*), ratified 2026-08-24 — and it is the instance that reaches furthest back and sits inside a canonical decision-record you personally ruled.

**The WARN survives both readings of what `spark` is.** If `spark` is lightning, the wind flex is a lightning→wind leak. If `spark` is fire (the stale manifest's claim), the wind flex is a fire→wind leak. Either way the flex is wrong, so the finding does not depend on resolving § 2's ambiguity. I checked this specifically because "the WARN is noise" was a refutation condition I was asked to test. **It is not noise.**

**Companion item, already actioned:** the document carrying § 7 had no live home for eight weeks while 17 files cited it. Restored to `canonical/reap-die-rise-engine/substrate-expansion-decision-2026-05-17.md` with a restoration record. The governance defect that allowed it (the prune-safe predicate does not grep code) is a rule change and is routed to jack-ryan for ratification, not decided here.

---

## § 6 — What is NOT pre-committed by this document

- No change to `pool.json`, `vfx_coverage_manifest.json`, `pool.py`, or `selector.py`.
- No change to § 7.1's seven-name frozen list.
- No change to `_VOCAB_FREEZE_IDS`.
- rocket's report-only predicate (jack-ryan's approved mechanical half) is unaffected either way and does not wait on this.

**On your ruling:** A1 is a one-field edit to one `pool.json` row → rocket, with a smoke-test showing `spark` no longer appears in any wind-slot candidate set. B1 is a 38-row status edit → rocket, same pass.

---

*Drafted 2026-08-24 by gandalf. Vocabulary half of jack-ryan's ruling-batch item 4. Every figure re-derived at drafting time from the live artifacts (#11, #75, #76 clause 2); one recommendation withdrawn mid-draft when the evidence refuted it (§ 2 note).*

**Tracker-delta:** new open decision → `current-to-end-state-engine.md` (`spark` vocabulary ruling + the 38-row at-rest status question; gates on Matt; due at next season-emission run).
