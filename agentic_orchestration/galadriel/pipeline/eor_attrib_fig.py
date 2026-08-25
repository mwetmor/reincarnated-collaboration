#!/usr/bin/env python3
"""eor_attrib_fig.py — MD-B4app-2c evidence figures.

  fig <attrib.json> <releases.json> <outdir>
"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COL = {"2": "#d08b2c", "3": "#3f8fce", "L": "#c0392b"}


def fig(ap, rp, outdir):
    d = json.load(open(ap))
    R = json.load(open(rp))
    conv, rel = d["converse"], R["releases"]
    t0, t1 = d["window"]

    # ---- panel 1: per-cast containing gap, by slot ------------------------
    fig1, ax = plt.subplots(figsize=(9, 5.2))
    for k, s in enumerate(("3", "2", "L")):
        rows = [r for r in conv if r["slot"] == s]
        for r in rows:
            blind = r["gap_cov"] < 0.80 and r["gap"] >= 0.30
            matched = r["release_matched"]
            ax.scatter(r["gap"], k + np.random.uniform(-0.16, 0.16),
                       s=90 if matched else 55,
                       facecolor="none" if blind else COL[s],
                       edgecolor=COL[s], linewidth=1.8 if matched else 1.0,
                       marker="o", zorder=3)
    # the one-frame boundary case: t=748.05, slot L. Its containing gap reads
    # 0.017 s because the cast's first DIM frame lands one frame BEFORE the tick
    # that opens the 0.67 s release it belongs to. Release-matched, gap-unmatched.
    ax.annotate("t=748.05 — one-frame\nboundary case (§ 3.1)",
                xy=(0.017, 2.0), xytext=(0.19, 2.45), fontsize=8, color="#c0392b",
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))
    ax.axvline(0.0834, color="0.35", ls="--", lw=1.2)
    ax.text(0.0834, 2.62, "  baseline inter-tick gap 0.083 s", color="0.35", fontsize=8.5)
    ax.axvline(0.50, color="k", ls="-", lw=1.4)
    ax.text(0.50, 2.62, "  release floor 0.50 s", fontsize=8.5)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["slot 3\n(n=19)", "slot 2\n(n=22)", "slot L\n(n=13)"])
    ax.set_xlabel("channel silence containing the cast (s)")
    ax.set_xlim(-0.03, 1.60)
    ax.set_ylim(-0.6, 2.8)
    ax.set_title("MD-B4app-2c · every cast, and how long the channel stopped around it\n"
                 "filled = release-matched interrupt · hollow = OCR-blind gap · "
                 "slot 3 never crosses 0.25 s", fontsize=10)
    ax.grid(axis="x", alpha=0.25)
    fig1.tight_layout()
    fig1.savefig(f"{outdir}/fig-castgap-by-slot.png", dpi=140)

    # ---- panel 2: the fight, casts and releases ---------------------------
    fig2, ax = plt.subplots(figsize=(13, 3.6))
    for r in rel:
        b = any(abs(c["t"] - r["t_on"]) <= 0.25 for c in conv)
        ax.axvspan(r["t_on"], r["t_off"], color="#c0392b" if b else "#7f8c8d",
                   alpha=0.55 if b else 0.28, lw=0)
    for k, s in enumerate(("2", "3", "L")):
        for r in [x for x in conv if x["slot"] == s]:
            ax.vlines(r["t"], k, k + 0.8, color=COL[s],
                      lw=2.4 if r["release_matched"] else 1.0)
    ax.set_yticks([0.4, 1.4, 2.4]); ax.set_yticklabels(["slot 2", "slot 3", "slot L"])
    ax.set_xlim(t0, t1); ax.set_ylim(-0.2, 3.2)
    ax.set_xlabel("t (s)")
    ax.set_title("54 casts against 19 releases · red shading = Type-B (cast-linked) release · "
                 "thick tick = that cast's interrupt", fontsize=10)
    fig2.tight_layout()
    fig2.savefig(f"{outdir}/fig-cast-timeline.png", dpi=140)
    print("wrote 2 figures")


if __name__ == "__main__":
    np.random.seed(7)
    fig(*sys.argv[2:5]) if sys.argv[1] == "fig" else sys.exit(__doc__)
