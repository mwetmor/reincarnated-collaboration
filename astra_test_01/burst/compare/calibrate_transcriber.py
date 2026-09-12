"""X0-T deterministic scorer. Threshold calibration: conductor hand PART
inventory plus independent transcriber bursts, including absent PART controls.
P/R >= .9, counts within +/-1 on >= .8, controls absent AND zero on 100%.
No model call. The default control list is the hand inventory's absent parts;
explicit controls may instead be supplied. Empty calibration never certifies.
"""
import argparse
import json
from pathlib import Path
import sys
if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oracles.common import report

PRESENCE_PRECISION_MIN = .9
PRESENCE_RECALL_MIN = .9
COUNT_WITHIN_ONE_MIN = .8
CONTROL_CATCH_MIN = 1.
COUNT_TOLERANCE = 1


def _validate(inventory, parts=None):
    if not isinstance(inventory,dict) or not inventory:
        raise ValueError('Nonempty closed inventory required')
    if parts is not None and set(inventory)!=set(parts):
        raise ValueError('Inventory must answer the entire closed list, including controls')
    for part,item in inventory.items():
        if not isinstance(part,str) or not isinstance(item,dict) or set(item)!={'present','count'}:
            raise ValueError('Inventory is presence/count only')
        if type(item['present']) is not bool or type(item['count']) is not int or item['count']<0:
            raise ValueError('Invalid presence/count type or negative count')


def score(hand_inventory, answers, *, controls=None,
          presence_precision_min=PRESENCE_PRECISION_MIN,
          presence_recall_min=PRESENCE_RECALL_MIN,
          count_within_one_min=COUNT_WITHIN_ONE_MIN,
          control_catch_min=CONTROL_CATCH_MIN, count_tolerance=COUNT_TOLERANCE,
          subject=''):
    _validate(hand_inventory)
    for item in hand_inventory.values():
        if item['present'] != (item['count']>0):
            raise ValueError('Hand inventory presence/count is inconsistent')
    controls=([p for p,v in hand_inventory.items() if not v['present']]
              if controls is None else list(controls))
    if len(controls)!=len(set(controls)) or any(p not in hand_inventory or
            hand_inventory[p]['present'] or hand_inventory[p]['count']!=0 for p in controls):
        raise ValueError('Controls must be unique, hand-declared absent and zero')
    limits=dict(presence_precision=presence_precision_min,presence_recall=presence_recall_min,
                count_within_one_fraction=count_within_one_min,control_catch_rate=control_catch_min)
    if any(not 0<=v<=1 for v in limits.values()) or type(count_tolerance) is not int or count_tolerance<0:
        raise ValueError('Invalid X0-T thresholds')
    answers=list(answers);bursts=[];totals=dict(tp=0,fp=0,fn=0,within=0,caught=0,parts=0,controls=0)
    disagreements={p:dict(hand=hand_inventory[p],presence_disagreements=0,
        count_disagreements=0,counts_outside_tolerance=0,observed=[]) for p in hand_inventory}
    def summarize(t):
        precision=t['tp']/(t['tp']+t['fp']) if t['tp']+t['fp'] else 1.
        recall=t['tp']/(t['tp']+t['fn']) if t['tp']+t['fn'] else 1.
        return dict(presence_precision=precision,presence_recall=recall,
            presence_f1=2*precision*recall/(precision+recall) if precision+recall else 0.,
            count_within_one_fraction=t['within']/t['parts'] if t['parts'] else None,
            control_catch_rate=t['caught']/t['controls'] if t['controls'] else None)
    def envelopes(values,label):
        return [report('X0-T.'+k,label,values[k],v,op='>=',unit='fraction',
                reason=('N=0: no transcriber bursts' if not answers else 'No declared-absent controls') if values[k] is None else '') for k,v in limits.items()]
    for i,a in enumerate(answers):
        _validate(a,hand_inventory);t=dict(tp=0,fp=0,fn=0,within=0,caught=0,
                                         parts=len(a),controls=len(controls))
        for p,h in hand_inventory.items():
            v=a[p];t['tp']+=int(h['present'] and v['present'])
            t['fp']+=int(not h['present'] and v['present'])
            t['fn']+=int(h['present'] and not v['present'])
            within=abs(v['count']-h['count'])<=count_tolerance;t['within']+=int(within)
            t['caught']+=int(p in controls and not v['present'] and v['count']==0)
            d=disagreements[p];d['presence_disagreements']+=int(v['present']!=h['present'])
            d['count_disagreements']+=int(v['count']!=h['count'])
            d['counts_outside_tolerance']+=int(not within);d['observed'].append(dict(burst=i,**v))
        values=summarize(t);rows=envelopes(values,str(i))
        burst_passed=None if any(r['passed'] is None for r in rows) else all(r['passed'] for r in rows)
        bursts.append(dict(index=i,**values,results=rows,passed=burst_passed))
        for k in totals:totals[k]+=t[k]
    aggregate=summarize(totals) if answers else {k:None for k in list(limits)+['presence_f1']}
    rows=envelopes(aggregate,'aggregate')
    reason='N=0: at least one transcriber burst required' if not answers else ('No declared-absent controls' if not controls else '')
    violations=sum(r['passed'] is False for r in rows)
    aggregate['passed']=None if reason else violations==0
    return report('X0-T',subject,None if reason else violations,0,unit='violations',reason=reason,
        metrics=dict(n=len(answers),per_burst=bursts,aggregate=aggregate,results=rows,
                     per_part_disagreement=disagreements,controls=controls,count_tolerance=count_tolerance))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--hand',required=True)
    parser.add_argument('--answers',nargs='+',required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    result=score(json.loads(Path(args.hand).read_text()),
                 [json.loads(Path(p).read_text()) for p in args.answers])
    Path(args.out).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':main()
