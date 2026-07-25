# DISPATCH — TCP-L8-U2: the HUD again, with the art the project actually owns

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25, at the owner's eye, mid-flight.
**Lap:** L8 UI (T4-UI), **arm 2.** Arm 1 is `drax/notes/2026-07-25-tcp-l8u-hud-arrival-report.md` — **yours, and
not blind to you.**

## §0 — Why this cell exists: a conductor defect, and it is the second of its kind

Matt watched arm 1's stills go past and asked: *"Are the HUD tests using the Interface - Dark Fantasy
HUD? … the HUD snapshots look like generic geometric shapes rather than the dark fantasy assets."*

**He is right and it is my failure.** Arm 1's dispatch §2 named `reincarnated-loadout/` and the
canonical folders as your ancestry and **never inventoried the art this project owns.** It exists,
it has existed the whole time, and it is a direct hit:

```
matt_notes_handoff_docs/recent-synty-packs/
  INTERFACE_Dark_Fantasy_Menus_SourceFiles_v1/   Sprites/DarkFantasyMenus 371 · Icons_Menu 72
                                                 Icons_DarkFantasyMenus 37 · _Flat 93 · Settings 24
                                                 General 58 · FX 10 · Cursors 9 · Fonts 2 · FBX 21
  Source_Sprites/                                Sprites/HUD 105 · DarkFantasy 501 · Icons_Weapons 339
                                                 Icons_Status 180 · Icons_Inventory 139
                                                 Icons_Resources 137 · Icons_Map 78 · Icons_Stats 60
                                                 Reticles 57 · FX 23 · Icons_Elements 18 · Flasks 12
  3,550 PNG · 21 FBX total.
```

**This is the same defect as the animation packs (TCP-41 ④): Matt supplied content and I dispatched
around it.** Twice now. It is on the record as mine.

Facts about the kit, stated as inventory and **not as recommendations** — what you do with any of
this is yours:

- `Sprites/Icons_Elements` ships **Air · Earth · Fire · Ice**. Our element set, including the ice
  work currently in flight in the engine seam.
- `Sprites/HUD` carries bars, boxes, circles, dials, a compass bar, arrows, an event-log frame and
  bracket, a damage-direction FX triplet, and sigil rings/boxes/triangles in three sizes.
- Most icons ship as a **`_Clean` / `_Stroke` / `_Underlay` triplet.**
- `Sprites/Flasks` is 12 vessels; `Icons_Status` is 180.

## §1 — The brief

> **"Author the combat HUD for this game, using the art the project owns. What is on it, where it
> sits, and how it reads at a glance — all yours."**

Same brief as arm 1 plus the kit. **Every choice is a veto-open ruling with reasoning.**

**No exemplar is named in this dispatch, deliberately** — that is your own arm-1 recommendation
adopted verbatim (*"state the criterion, name no exemplar"*). The criterion stands unchanged and is
the only design position I hold: **a HUD must answer "am I about to die, and what can I do about it"
in peripheral vision, during combat, without being looked at directly.** How that is achieved is
open, and **a screen-edge treatment is as admissible as a vessel** — arm 1 established that I
foreclosed that branch by naming a family, and I am not naming one now.

**I am also stating no expected iteration count, no expected cost, and no forecast of any kind**,
because arm 1 caught me anchoring the exact quantity I had commissioned. Your fix — *"put hypotheses
in a sealed section"* — is adopted, and the simplest form of it is that this dispatch contains none.

## §2 — What is honest about this arm, up front

**This is not a clean replication and you should not report it as one.** You have already solved the
layout problem once, this session. Arm 2's iteration count is therefore **contaminated downward by
your own prior answer**, unavoidably. Declare that rather than engineer around it.

**So the question arm 2 actually answers is not "how many iterations does a HUD take" — arm 1
answered that (5).** It is:

1. **What does art integration cost**, separately from layout? Import, atlas/slice, 9-slice setup,
   naming, sizing, colour-matching — none of which arm 1 paid.
2. ★ **Does real art CHANGE the design?** I suspect Synty's proportions will not accept arm 1's
   layout unmodified. **If the kit changes your answer, say exactly where and why** — that is the
   finding. If it doesn't, say that too; a null result here is genuinely informative.
3. **Is this the wire's last case?** Arm 1 retired the wire's iteration-cost argument decisively
   (script cycle 1.19 s not 15–30 s; 5 iterations not 40; wire saves ~0.2% of the clock). **But
   asset-heavy work is a different profile** — importing, slicing and wiring sprites is editor work,
   and an editor-resident wire may reach things a script reaches awkwardly or not at all. **Method is
   yours; if you form a view on the wire here, it is the last L8 datum that could revive it.**

## §3 — Constraints (four)

1. **Floor: `~/Games/mcp-lab/l8ui/`, your arm-1 project — extend it, do not replace it.** Keep arm
   1's scenes intact and addressable so the two can be composited side by side. **A NEW project is
   also acceptable if you judge cohabitation dirty — say which and why.**
2. **Vendor a SUBSET.** Do not copy 3,550 PNGs. **Census what you vendored and why** — the selection
   is itself a design output, and the ratio (vendored : available) is a number the serial-content
   pipeline will want.
3. ★ **Fix the legibility instrument — this is your own arm-1 finding handed back to you.** You
   measured every HUD region at **0.0000** luminance at the ARPG camera because the judging frame is
   mostly black surround. That is not a contrast test. **Choose a background that actually has bright
   and dark regions and justify it** — `evidence/l5/l5a/frames/L5A_AFTER__money.png` is lit stone
   wall-to-wall and is one candidate; a composite of several is another. The requirement is
   unchanged — **brightest and darkest real regions, not a hand-picked frame** — only the instrument
   needs repairing.
4. **Two resolutions minimum**, as arm 1, and the same ones, so the pair is comparable.

**Forbidden floors:** `~/Games/mcp-lab/project/` (substrate — copy out read-only only; sha
`d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444, verify at start and
end) · `~/Games/mcp-lab/l7vfx/` (concurrent cell) · `~/Games/mcp-lab/evidence/l5/` (live comparison).
**L-J binds: W-PRO stays parked.**

## §4 — What you ship

1. **FIRST_INTENT banked verbatim + authoring clock started before any work** (TCP-32).
2. **A vendoring census** — what you took, from where, how much, and the selection rationale.
3. **Stills at both resolutions over a repaired legibility instrument**, with the contrast argument.
4. **An A/B against arm 1** — the same HUD state, primitives vs kit, side by side. This is the
   picture Matt asked the question about.
5. ★ **The iteration log, and the delta account:** which iterations were *layout* and which were
   *art integration*. That split is the cell's payload.
6. **Rulings, veto-open, with reasoning. Read-list declared.**
7. **Clock closed, authoring separate from execution**, and **declare the arm-1 contamination** per
   §2.

## §5 — Exit predicate

1. §4.1–§4.7 present. 2. Substrate sha + 0444 verified at start AND end. 3. `mcp-lab/project/`,
`l7vfx/` and `evidence/l5/` demonstrably untouched — and note arm 1's own finding that a **directory
listing-hash is the wrong instrument** while concurrent cells are live; per-file sha is the right one.
4. `user://` clean. 5. Arm-1 artifacts still intact and renderable.

**Honorable fallback (L-F):** an attributed blocker plus the best partial dressing is a **PASS.**
**Ceiling-finding is a PASS (L-G)** — *"this kit cannot express the design and here is the exact
sprite that fails"* is a first-class result, and given §2.2 it may be the most likely one.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u2-dark-fantasy-kit-report.md`

**HALT to Matt:** any game-systems decision not yet made — **arm 1's three are already open and are
NOT yours to re-decide** (the escape-clock fork; the critical-threshold constant; the finding that
`primary_attack` appears in only 7 of 10 kits, leaving some kits with no basic attack). Add to that
list; do not resolve from it.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). **Name anything in this dispatch that steered
you.** Arm 1 made this instruction sharper rather than weaker: I flagged the Diablo II sentence as my
prime suspect *in the dispatch itself* and **it steered you anyway** — so self-flagging is not
mitigation, and I have removed the exemplar rather than labelled it. **Tell me what I did wrong this
time instead.**
