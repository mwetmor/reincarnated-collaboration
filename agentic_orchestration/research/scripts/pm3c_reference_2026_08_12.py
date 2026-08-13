#!/usr/bin/env python3
"""KC2-PM3 Lap C -- emit the MEASURED reference-truth wave timeline (charter Law 4). READ-ONLY.

METHOD (fully declared; see `pm3c_video_2026_08_12` for the frame basis IS-V1..IS-V4)

  The Crucible HUD carries a PERSISTENT wave counter -- red digits in a gold ring immediately
  left of the minimap, full-res box (1580, 134, 64, 34). It is not a 2-3 s banner; it is on
  screen every frame of the run, which makes 1 Hz sampling comfortably sufficient and removes
  the need for banner-flash detection entirely.

  IS-R1  Digit isolation. The counter is rendered in a saturated red on a dark ring. Per frame
         the crop is thresholded  (R>110) & (R-G>55) & (R-B>55)  into a boolean glyph mask.
         Basis: 218 frames, t = 682..899. 5 frames are UNREADABLE (VFX bloom over the ring):
         t = 769, 780, 782 (partial) and t = 868, 869 (screen is black -- the death fade).
  IS-R2  Classification is whole-number template IoU against ten exemplar masks, one per wave
         151..160, each taken at a second whose value was READ BY EYE off the upscaled crop
         (151<-690, 152<-700, 153<-720, 154<-735, 155<-750, 156<-770, 157<-790, 158<-805,
         159<-820, 160<-860). Accept threshold: best IoU > 0.80 AND margin over 2nd > 0.10.
         213 of 218 frames clear it; the 5 that do not are listed above and are bridged by the
         monotone run structure, not by guessing.
  IS-R3  A wave's START is the FIRST second at which the counter reads that wave. Because the
         sample is 1 Hz, true onset lies in [t-1, t]: every start below carries +/- 1 s.
  IS-R4  Wall-clock anchor: video_t = wallclock - 21:37:25 (verified EXACT at t=470, IS-V2).

WHAT THIS FALSIFIES / PINS
  * Matt remembered "died wave 159 or 160". MEASURED: the counter reads 160 from t=839 to the
    end, and at t=880 the on-screen objective reads "You have failed, your Compensation awaits
    in the Treasure Chamber". => DIED ON WAVE 160. Waves 151-159 CLEARED (9), died on the 10th.
  * The fight begins at t=682 (Lokarr's "Start on Wave 150" option is highlighted under the
    cursor at t=680 and the counter flips 0 -> 151 at t=682).
  * Death fade-to-black at t = 868 (6 fps sub-sampling puts the fade onset in [867.8, 868.2]).
"""
import csv
import pathlib

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-12-kc2-pm3-lap-c-blessings-reference-dot")

FIGHT_START = 682          # first second the counter reads 151
DEATH_T = 868              # fade-to-black; player death
CAPTURE_EPOCH = "2026-08-05 21:37:25"

# MEASURED wave onsets (video seconds). See IS-R1..IS-R3.
STARTS = [(151, 682), (152, 698), (153, 715), (154, 730), (155, 744),
          (156, 760), (157, 780), (158, 799), (159, 813), (160, 839)]

# setup-phase events, all measured from the same 1 Hz frame set
SETUP = [
    (446, "first readable tribute reading after arena load: 145"),
    (477, "PURCHASE 1 -- Deathchill Beacon  (tribute 145 -> 140)"),
    (484, "PURCHASE 2 -- Stormcaller Beacon (tribute 140 -> 135)"),
    (502, "PURCHASE 3 -- Inferno Beacon     (tribute 135 -> 130)"),
    (510, "PURCHASE 4 -- Vanguard Banner    (tribute 130 -> 125)"),
    (680, "Lokarr dialog open, 'Start on Wave 150' highlighted under cursor"),
    (682, "FIGHT START -- wave counter 0 -> 151"),
    (868, "DEATH -- fade to black"),
    (880, "objective reads 'You have failed, your Compensation awaits in the Treasure Chamber'"),
]


def hhmmss(t):
    return f"21:{37 + (25 + t) // 60:02d}:{(25 + t) % 60:02d}" if (25 + t) // 60 < 23 else ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, (w, t) in enumerate(STARTS):
        nxt = STARTS[i + 1][1] if i + 1 < len(STARTS) else DEATH_T
        rows.append(dict(wave=w,
                         video_t_start_s=t,
                         elapsed_from_first_wave_s=t - FIGHT_START,
                         wave_duration_s=nxt - t,
                         terminal="DEATH" if i == len(STARTS) - 1 else "CLEARED",
                         wallclock_start=hhmmss(t),
                         onset_uncertainty_s="+/-1 (1 Hz sample, IS-R3)"))
    fp = OUT / "measured-reference-truth.csv"
    with fp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(fp, len(rows), "rows")

    fp2 = OUT / "measured-reference-events.csv"
    with fp2.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["video_t_s", "wallclock", "event"])
        for t, e in SETUP:
            w.writerow([t, hhmmss(t), e])
    print(fp2, len(SETUP), "rows")

    d = [r["wave_duration_s"] for r in rows]
    print(f"  fight window {FIGHT_START}..{DEATH_T} s = {DEATH_T - FIGHT_START} s over "
          f"{len(rows)} waves")
    print(f"  wave duration min/median/max = {min(d)} / {sorted(d)[len(d)//2]} / {max(d)} s")
    print(f"  capture epoch {CAPTURE_EPOCH}; death wallclock {hhmmss(DEATH_T)}")


if __name__ == "__main__":
    main()
