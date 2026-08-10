# Minigame Editor & Scenario Contracts — recognition record

> **STATUS: RECOGNITION RECORD** — architectural commitments deferred; the graduation gate (§ 5)
> is the empirical criterion that unlocks them. Authored 2026-08-10 by gandalf
> (SPEC-AUTHOR + STORYWRIGHT sidebar) from the 2026-08-10 Matt strategy session.
> **Lineage:** Q51 ruling F-V2-1 (wave-arena endgame-mode CANDIDATE,
> `current-to-end-state-game.md`) · `arcade-minigame-taxonomy-spec.md` ·
> `one-realm-mvp-scope.md` (THE DENOMINATOR — nothing here may grow the MVP) ·
> `operating-procedures/software-factory.md` (companion strategy doc).

---

## 1 · The recognition

The software factory's **New Run form** and the eventual **minigame editor** are the same
machine seen from two sides. Both do exactly this: *pick kit / checkpoint / waves / arena /
seed → launch a specified run → watch it → judge the result against recorded stats.* Matt
configuring a factory run and a player authoring a wave-arena scenario differ in skin, not
spine.

**Doctrine: two skins, one spine.** The shared asset is the **CONTRACT layer** — schemas and
gates — never the pixels. We do not build a player-facing editor now; we build the factory UI
so that its run form *is* the proto-editor, and every hour Matt spends driving it is
elicitation evidence for the wave-arena design grill.

## 2 · The four breaks in the isomorphism

Where the two skins genuinely differ — each break is a reason product-grade is deferred:

| # | Break | Shop side | Product side |
|---|---|---|---|
| B1 | **Audience** | Matt, operator, trusted | Player, untrusted input |
| B2 | **Trust boundary** | Configs are Matt-authored | UGC — the **gate wall becomes the scenario VALIDATOR** (66-gate posture, re-aimed) |
| B3 | **Register** | Shop console; receipts and reds | Diegetic product surface (§ 6 — Glitch Archive fold, grill-pending) |
| B4 | **Stakes** | Run receipts, costs | Player progression, ladders, anti-cheat |

## 3 · The four shared contracts

1. **Scenario schema** — the parameter set that specifies a run (kit / checkpoint / waves /
   arena / seed / …). Engine-side custody (star-lord; drax countersign where consumed).
2. **Baton format** — `baton_v1` and successors; the run's emitted record.
3. **Receipts** — what happened, what it cost, what went red (factory SQLite; § SF-7).
4. **Gate wall as validator** — the same claim-gate machinery that judges factory phases
   judges scenario admissibility. A gate that cannot run returns FAIL, never green.

**Corrigenda-freedom clause:** until graduation (§ 5), every contract may break compatibility
freely and without ceremony. Shop-only fields are namespaced **`x_shop_*`** so the eventual
product schema sheds them mechanically. Nothing in the proto phase is a compatibility promise.

## 4 · Ruling — proto NOW, product DEFERRED

- **NOW:** the proto-editor = the factory UI's New Run form
  (`gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md`, surfaces tagged
  **PROTO-PRODUCT**). Matt's iterative use during development is the point: it surfaces the
  scenario parameters the grill needs ruled.
- **DEFERRED:** product-grade editor, behind the **graduation gate** (§ 5). No player-facing
  build, no diegetic skin, no ladder machinery before it.
- **Denominator guard:** the One Realm MVP scope is unchanged by this doc. The proto-editor
  is shop tooling that happens to have product lineage — it adds zero MVP surface.

## 5 · Graduation gate (the empirical criterion)

Product-grade commitment unlocks only when **both** hold:

1. The **wave-arena ELICITOR grill** has run (already queued in the game tracker: after the
   EoR endgame fixture + Crucible render exhibit exist as its substrate), and
2. **Matt has ruled** the wave-arena endgame mode IN (it is today a CANDIDATE, F-V2-1).

Until then, this doc licenses no editor-shaped production work beyond Spec B's form.

## 6 · Named, not taken (grill agenda)

- **Diegetic machine-room fold** — the editor as an object inside the Glitch Archive frame
  (the scenario-console a player finds, not a menu). STORYWRIGHT lean: strong; the frame
  already casts runs as archive replays, so an in-world console that *specifies* replays is
  native, not bolted. **Agenda item for the grill, not a commitment.**
- **Verified-ladder digest replays** — determinism digests (KC2 practice: identical OFF/ON
  digests as evidence) as the anti-cheat spine for any ranked scenario ladder.
- **Stat-screen skin** — receipts views re-skinned as player-facing post-run stats.

## 7 · Registered predictions (validated or falsified at the grill)

- **P-ME-1:** Matt's proto-editor use will surface ≥1 scenario parameter the sim schema
  lacks, before the grill sits.
- **P-ME-2:** the gate wall will reject ≥1 hand-authored scenario for a reason a player
  editor would have to surface in-UI — the rejection UX is discovered shop-side first.
- **P-ME-3:** digest-replay determinism becomes the accepted anti-cheat mechanism for
  verified ladders, with no additional server trust required.

## 8 · Cross-references

`operating-procedures/software-factory.md` (strategy + UI tiers + dual-audience tags) ·
`gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md` (the form this doc governs) ·
`current-to-end-state-game.md` SESSION-DELTA 2026-08-10 (tracker linkage) ·
`arcade-minigame-taxonomy-spec.md` · `one-realm-mvp-scope.md`.

**Signed:** gandalf, 2026-08-10.
