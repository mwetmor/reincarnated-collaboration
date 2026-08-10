# Factory UI + Proto-Editor — build contract (Spec B)

**Date:** 2026-08-10 · **Author:** gandalf (SPEC-AUTHOR/SCENEWRIGHT) · **Builder:** drax
**Review:** gandalf DRIFT-CRITIC · galadriel screenshot-verify on every shipped surface
**Governing docs:** `operating-procedures/software-factory.md` § 7 (tier ladder + UI
disciplines) · `canonical/reap-die-rise-game/minigame-editor-and-scenario-contracts.md`
(dual-audience doctrine + graduation gate)
**Status:** BUILD-CONTRACT — **build gate not yet open** (§ 6); drax's near-term scope is stack
pick + skeleton, not build.

---

## 1 · Purpose

Tier-2 glance dashboard over the factory receipts DB, answering exactly four questions:
**what's running? · what's red? · what did it cost? · what's waiting on Matt?**
Plus the **New Run form** — which IS the proto-minigame-editor (two skins, one spine).

## 2 · Dual-audience tags (every surface carries one)

| Surface | Tag |
|---|---|
| New Run form (scenario compose → launch) | **PROTO-PRODUCT** |
| Run watch (phase status stream) | **PROTO-PRODUCT** |
| Post-run stats view | **PROTO-PRODUCT** (stat-screen lineage, grill-pending) |
| Receipts / cost / token views | **SHOP-ONLY** |
| Red-gate forensics (envelope + gate reports) | **SHOP-ONLY** |
| Matt-queue panel (waiting-on-Matt) | **SHOP-ONLY** |

PROTO-PRODUCT surfaces obey the corrigenda-freedom clause (recognition record § 3): break
freely until graduation; shop-only fields namespaced `x_shop_*`.

## 3 · New Run form contract (the proto-editor)

Fields: **kit / checkpoint / waves / arena / seed** (+ whatever the scenario schema grows —
the form renders the schema, it does not define it). Flow: compose → **launch** (writes
through the spine's queue machinery, NEVER direct process spawn from the UI) → **watch**
(phase/gate status) → **stats** (from receipts) → link to the session dir for forensics.
Matt's iterative use of this form during development is elicitation evidence for the
wave-arena grill — log every launched config to receipts so the grill can read what he
actually reached for (prediction P-ME-1).

## 4 · One data path

The UI reads the **same SQLite the gates write** — `factory/receipts.db`, WAL mode, read-only
connection, polling via `select … where rowid > ?` per table. No second store, no cache layer
that can disagree, no UI-side derivation of a verdict that receipts don't hold. **The view is
never truth.** A green pixel with a red exit code underneath is the named ancestor bug
(strategy § 6 — observability theater); galadriel's screenshot-verify exists to catch exactly
this class.

## 5 · Read-mostly

The UI's only write verbs are: enqueue run (via spine queue) · annotate (Matt notes, receipts
`events` table). No gate mutation, no receipt edits, no config edits from the UI in v1.

## 6 · Build gate

Tier-2 build fires only when **receipts schema has held stable across ≥2 compiled workflows**
(F1's founding workflow + one more). Until then: pick the stack, stand the skeleton, wire
nothing to fake data — **no dashboard before receipts** (strategy § 7 discipline 3; a mock-fed
dashboard is observability theater by construction).

## 7 · Constraints

- **Local-only, Mac-served.** No deployment, no auth surface, no cloud in v1.
- **Stack:** drax's pick within existing React/Vite competence (loadout-app lineage);
  no new framework adoption for this.
- **No product skin.** The diegetic machine-room fold (Glitch Archive console) is a grill
  agenda item — building it now would pre-empt a Matt ruling (recognition record § 6).
- **Engine tree untouched** — this UI lives meta-repo-side against receipts + session dirs.

**Signed:** gandalf, 2026-08-10.
