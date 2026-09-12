import json
from lane.run_burst import validate_task
from lane.audit import audit,take_snapshot
from gates_helpers import TemporaryTest

TYPES=('TOOLING','GENERATE','CHECK','JUDGE','TRANSCRIBE','LABEL','ANNOTATE','PACK')
def task(typ):
    return dict(text='test',references=[],outputs=[],effort='high',add_dirs=[],
                minutes_cap=40 if typ=='TOOLING' else 15,tool_call_cap=60 if typ=='TOOLING' else 20,
                image_cap={'GENERATE':12,'LABEL':2}.get(typ,0))

class Tests(TemporaryTest):
    def test_validation_boundaries_every_type(self):
        for typ in TYPES:
            with self.subTest(type=typ):
                t=task(typ);validate_task(t,typ)
                for key in ('minutes_cap','tool_call_cap','image_cap'):
                    bad=dict(t);bad[key]+=1
                    with self.assertRaises(ValueError):validate_task(bad,typ)
        with self.assertRaises(ValueError):validate_task(task('CHECK'),'invalid')
    def test_audit_type_caps_and_label_image_permission(self):
        work=self.base/'work';(work/'out').mkdir(parents=True)
        event=work/'out/events.jsonl';event.write_text('')
        snap=take_snapshot(work,work)
        for typ in TYPES:
            with self.subTest(type=typ):
                t=task(typ)
                event.write_text('\n'.join(json.dumps({'type':'item.completed','item':{'id':str(i),'type':'image_generation_call'}}) for i in range(t['image_cap'])))
                self.assertEqual(audit(event,work,snap,t,typ)['violations'],[])
                for key in ('minutes_cap','tool_call_cap','image_cap'):
                    bad=dict(t);bad[key]+=1
                    self.assertTrue(audit(event,work,snap,bad,typ)['violations'])
                event.write_text('\n'.join(json.dumps({'type':'item.completed','item':{'id':str(i),'type':'image_generation_call'}}) for i in range(t['image_cap']+1)))
                self.assertTrue(audit(event,work,snap,t,typ)['violations'])
    def test_audit_observed_tool_overrun(self):
        work=self.base/'work';(work/'out').mkdir(parents=True)
        event=work/'out/events.jsonl';event.write_text('');snap=take_snapshot(work,work)
        for typ in TYPES:
            t=task(typ)
            event.write_text('\n'.join(json.dumps({'type':'item.completed','item':{'id':str(i),'type':'command_execution','command':'true'}}) for i in range(t['tool_call_cap']+1)))
            self.assertIn('tool_call_cap exceeded',audit(event,work,snap,t,typ)['violations'])
