# KC2-MC Lap D-12 — Diversion Decode (petAngerTransference + Bernoulli key semantics)

**Author:** legolas (returned 2026-08-25; prose verdict conductor-captured verbatim-in-substance from the lap return — the harness blocked the lap's own report write; evidence in this directory was committed by the lap itself at `f0077dce`: 17 listings, 2 CSVs, digests).
**Commission:** gandalf RUN-CONDUCTOR, R-L65-3 (MD-B3app-5). Fold of record: run charter L-67.

---

## § 1 — Q-A: `petAngerTransference` share arithmetic — **DECODED. D-3 R-4 closes.**

- Lives on the **monster's** `ControllerMonster` record at **`+0x57c`** as a **float fraction = DBR int × 0.01** (`Load@ControllerMonster` `0xf7a5c–0xf7a7f` — the non-scalar store D-3 could not resolve is `int → cvtdq2ps → mulss 0.01`).
- **One consumer image-wide:** `UnderAttack@ControllerMonster` `0xfc3e8`.
- Arithmetic: a **SPLIT of one grant** — `(1−t)·AttackedAnger` to the attacker's threat entry, `t·AttackedAnger` to the attacker's `GetLeader()`. **Not** a transfer, **not** a multiplier. **Inert for non-pet attackers** (both legs land on the same id).
- Roster values: `t` modal **0.17**; `AttackedAnger = 15.0` on **77/77**; throttled to one grant per **500 ms** per monster.

## § 2 — Q-B: diversion-Bernoulli key semantics — **DECODED: `PER_INSTANCE`. `PER_RECORD` is decoded-FALSE.**

- The ignore-pets latch is **per-object** (`+0x574` / `+0x578`, re-rolled on `this` at `0xf634d`) — parameters live per record, **state lives per instance**.
- The threat table is `std::map<uint32 entityId, Entry>` — no record-level key ever reaches the subsystem.

## § 3 — The finding under both (contradicts the commission's premise)

`causesAnger = False` on the summon body makes `ShouldRemoveEnemy` (`0xfff0`, `CausesAnger` vslot `+0x428`) return TRUE, so **every `AddAnger` writes nothing**; `FindEnemy` is only `GetNewTarget` over that table. Verified from ARZ: **both Guardian summons `causesAnger = False`, `angerMultiplier = 0.0`.**

Census (2,009 rows): `Class=Pet` **753/765 True** (those tank); `PetPlayerScaling` 1,166 False — the 78 True are all Mortar Traps.

**Consequences:**
- **The Guardians cannot divert.** They never enter the threat table; enemies never select them. `DIVERT_MAX` bounds a **non-mechanism**; `D-B3app-3` (count-insensitivity) is explained.
- L-65/F-13's *"the residual lever is DIVERSION"* **does not survive** the decode.
- The decoded sign is **opposite**: **+2.55 anger to the PLAYER** (`0.17 × 15.0`) per throttled Guardian hit — summons slightly *attract* attacks to their owner.

## § 4 — Sim implications (conductor rulings at charter L-67)

Replace the diversion Bernoulli with the decoded anger-split term; retire DIVERT arms graded `decoded-false-mechanism`; baton rows: summons draw no aggro / feed player threat / genre pets that tank exist (753/765) but ours are not among them.

## § 5 — UNRESOLVED (six, paths named in the lap evidence)

Chiefly: `SetDistanceAngerComparator` has **no call site** in `Game.dll`. See lap listings for the full six.
