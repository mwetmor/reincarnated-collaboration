const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=__dirname,html=fs.readFileSync(path.join(root,'preview/index.html'),'utf8');
const script=html.split('<script>')[1].split('</script>')[0];new vm.Script(script);
const clock=script.slice(script.indexOf('const SPAWN='),script.indexOf('function sprite('));
const state=vm.runInNewContext(clock+';combinedState');
const spawn=5/16,impact=spawn+.6,end=impact+.5,epsilon=1e-7;
assert.equal(state(spawn-epsilon).travel,null);assert.equal(state(spawn).character,5);assert.equal(state(spawn).travel,0);
assert.equal(state(2/16-epsilon).flare,null);assert.equal(state(2/16).flare,0);
assert.equal(state(impact-epsilon).impact,null);assert.equal(state(impact).travel,null);assert.equal(state(impact).impact,0);
assert.equal(state(end-epsilon).impact,9);assert.equal(state(end).impact,null);
for(const lane of ['character','vfx']){
 const atlas=JSON.parse(fs.readFileSync(path.join(root,lane,'atlas.json'),'utf8'));
 for(const a of Object.values(atlas.animations||atlas.modules))for(const frame of a.frames){assert(fs.existsSync(path.join(root,lane,frame.file)),frame.file);assert(frame.rect.every(Number.isFinite));}
}
const evidence={syntax:'PASS',spawn_before_index5:'absent',spawn_at_index5:'present',spawn_ms:spawn*1000,flare_start_ms:125,impact_start_ms:impact*1000,impact_end_ms:end*1000,source_files:'PASS',browser_playback:'UNVERIFIED'};
fs.writeFileSync(path.join(root,'evidence/preview_timing_checks.json'),JSON.stringify(evidence,null,2)+'\n');console.log(evidence);
