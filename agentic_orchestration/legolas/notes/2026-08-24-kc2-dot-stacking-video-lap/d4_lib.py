"""D-4 DoT-stacking video-measurement lap — shared instrument library.
READ-ONLY on all sources. Basis: Lap K pm4k_full_trace.csv (exact printed integer HP, 60 fps).
"""
import csv, os
LAPK = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-k-death-anchor/pm4k_full_trace.csv'
LAPI = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/pm4i_dot_riders.csv'
FPS = 60.0

def load_trace(hp_max_filter=20005):
    rows = list(csv.DictReader(open(LAPK)))
    out = {}
    for r in rows:
        if not r['hp_cur'] or not r['hp_max']:
            continue
        if hp_max_filter is not None and int(r['hp_max']) != hp_max_filter:
            continue
        t = float(r['t_s'])
        out[round(t*FPS)] = (round(t,4), int(r['hp_cur']))
    return out

def contiguous_blocks(frames):
    """Maximal runs of consecutive frame indices present in the trace."""
    ks = sorted(frames); blocks=[]; s=ks[0]; p=ks[0]
    for k in ks[1:]:
        if k != p+1:
            blocks.append((s,p)); s=k
        p=k
    blocks.append((s,p)); return blocks

def deltas(frames):
    """(frame_index, t, hp, delta_from_prev) for adjacent-frame pairs only."""
    ks = sorted(frames); out=[]
    for i in range(1,len(ks)):
        if ks[i] == ks[i-1]+1:
            out.append((ks[i], frames[ks[i]][0], frames[ks[i]][1],
                        frames[ks[i]][1]-frames[ks[i-1]][1]))
    return out
