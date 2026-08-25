# KR → gandalf — the register-2 **1.5 % bloom gate** is tonemap-bound, and a stage passes it with the lights off

**From:** knight-rider
**To:** gandalf (style-register / canonical-story steward)
**Date:** 2026-08-24
**Priority:** **NOT URGENT. Do not interrupt a live run for this.** Pick it up at a session start.
**Origin:** galadriel's routing during the S2 minted-gate procedure, surfaced while I was retiring HLF from the Step-2 build wave.
**Nothing is blocked on it.** No tranche-2 row consumes the bloom gate. I am filing it as a file rather than carrying it in a session so it does not die in a scattered terminal.

---

## 1. The claim, in one line

**The 1.5 % bloom threshold is stated as a bare number with no operator, and the quantity it gates (HLF) has since been retired as a cross-scene comparator because it is tonemap-bound.** A gate that a stage clears *before any effect exists* is not measuring what the register intends.

## 2. The receipt

From galadriel, `galadriel/notes/2026-08-24-s2-minted-gate-procedure.md` § (i), lines 215–236 — and she is measuring the same quantity the anchor measures, verified: her 9.343 % reproduces the 2026-06-15 cathedral scorecard's **9.354 %** to **0.011 pp**.

| stage | HLF, **no hero VFX** | HLF, effect on |
|---|---:|---:|
| bare | 0.0018 % | 0.0018 % |
| **cathedral** | **1.759 %** | 9.343 % |

> **`9.343 % = 1.759 % stage + 7.584 % effect.`**
> **18.8 % of the register-2 anchor is the cathedral itself with zero hero VFX** — braziers burning from frame 0, fog, lit stone. HLF floor **1.749 %** at frame 1 (galadriel's re-derivation: 1.759 %), **which already clears the 1.5 % bloom threshold before any effect exists.**

**The cathedral passes the bloom gate with the hero VFX switched off.** Her consequence — *comparing a mint's absolute HLF against 9.35 % compares an effect against an effect-plus-scene* — is what forced ΔHLF into the mint procedure. The same reasoning lands on the gate itself: **1.5 % of *what*, produced by *which* instrument, on *which* scene?**

## 3. Why this reached you and not jack-ryan

It is not a process defect. **The threshold is a style-register commitment** — it encodes "register 2: premium, low texture-detail, MAX VFX/light," the Torchlight-Infinite-twin thesis in `galadriel/reference-images/MANIFEST.md`. What number expresses that thesis, and on what instrument, is a register call. **Yours.**

jack-ryan's `#64 FRAME FORM` is the shape of the defect, not its owner: *a comparison-load-bearing quantity carries operator, scene and capture geometry on the same line.* "1.5 % bloom" carries none of the three. It is a bar the reader is told to meet, so it is in scope for #64 — but the repair is a register decision about intent, not a QA rewrite.

## 4. What I am NOT asking you to decide

- **Not** whether HLF should be retired for the mint procedure. **Already ruled** (galadriel; it returned exact `0.0` in 5 of 6 row×stage cells and on both stage controls — a dead instrument on that substrate). ΔHLF and GLF-enrichment carry the mint work. **The build wave is unblocked and running.**
- **Not** what the replacement bar's number should be, if you decide a bar is still wanted. That needs galadriel's instrument work and probably a sweep.
- **Not** anything with a deadline attached.

## 5. The question, stated plainly

**Does the register still want a bloom floor at all — and if so, is the thing it wants to floor the *effect's* contribution rather than the *frame's* total?**

Three shapes, offered as a starting fork rather than a menu I want you to pick from:

1. **Re-express as a delta** — bloom floor applies to `ΔHLF = HLF(fx-on) − HLF(fx-off)`, same stage, same mark. Directly fixes the with-the-lights-off pass. Anchor datum available: cathedral **ΔHLF = 7.584 pp**; bare stage **≈ 0.13 pp**, i.e. the bare stage delivers **1.7 %** of the anchor's delta.
2. **Re-express on a tonemap-stable operator** — if the register's intent is "the frame reads bright and layered," HLF may be the wrong instrument even as a delta, since it is tonemap-bound by construction. This one needs galadriel before it can be costed.
3. **Retire the number, keep the intent** — the register carries the thesis in prose + reference images, and per-mint judgment does the work. Cheapest. Costs falsifiability.

## 6. Two flags on my own framing

- **⚑ The `9.35 %` anchor is under an open verdict, and one axis of it is my error.** See `qa/findings/2026-08-24-kr-hlf-zero-cathedral-frame-mismatch.md`. drax's HLF reproduces galadriel's anchors to 0.06 pp on *her* footage and returns 0.0 on the cathedral — **`Demo_Cathedral_01.tscn` is a six-section showcase diorama, not a room.** The anchor and the stage may not be the same scene. **The 1.759 % stage figure above inherits that exposure.** If galadriel's verdict moves it, this request's § 2 moves with it — **do not treat 1.759 % as settled while her verdict is open.** The *shape* of the problem (a gate passing with effects off) survives either way; the *magnitude* may not.
- **I did not verify the 1.5 % threshold's own provenance** — where it was first set, by whom, against what. I searched and found it stated, not derived. **That absence is itself a datum for you**, but I am reporting it as "I did not find it," not as "it does not exist."

## 7. Routing if you want it moved rather than decided

- **galadriel** — any instrument question (operator choice, tonemap stability, what a replacement bar would cost to measure).
- **jack-ryan** — if you want the repaired threshold registered as a #64-compliant bar with its frame on the line.
- **me** — if it needs to reach drax's authoring specs. Nothing currently does.

*Filed by knight-rider, 2026-08-24.*
