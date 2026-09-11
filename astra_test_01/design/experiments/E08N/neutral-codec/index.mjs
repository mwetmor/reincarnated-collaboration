// Engine-neutral byte contract. No rendering or simulation imports.
export async function sha256(bytes) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
}
export function validateHeader(asset) {
  const n=asset.deformation_normals;
  if(n.record_stride_bytes!==16 || n.byte_order!=='little' || n.required_vertex_buffer_sha256!==asset.vertex_buffer.sha256 || n.required_palette_buffer_sha256!==asset.palette_buffer.sha256) throw Error('Incompatible normal/source binding');
  if(!Array.isArray(n.chunks)||n.chunks.length!==6||new Set(n.chunks.map(c=>c.id)).size!==6) throw Error('Invalid chunk inventory');
}
export async function decodeChunk(encoded, descriptor) {
  if(descriptor.encoding!=='zlib-deflate') throw Error('Unsupported codec');
  if(!Number.isSafeInteger(descriptor.decoded_bytes)||descriptor.decoded_bytes<=0||descriptor.decoded_bytes>12000000||descriptor.decoded_bytes%16) throw Error('Invalid decoded bound');
  if(encoded.byteLength!==descriptor.bytes||encoded.byteLength>8000000) throw Error('Encoded byte count mismatch');
  if(await sha256(encoded)!==descriptor.sha256) throw Error('Encoded hash mismatch');
  if(typeof DecompressionStream!=='function') throw Error('Native deflate decoder unavailable');
  const reader=new Blob([encoded]).stream().pipeThrough(new DecompressionStream('deflate')).getReader();
  const pieces=[];let size=0;
  try {
    while(true){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;if(size>descriptor.decoded_bytes)throw Error('Decoded byte bound exceeded');pieces.push(value);}
  } catch(error){await reader.cancel().catch(()=>{});throw error;}
  if(size!==descriptor.decoded_bytes) throw Error('Decoded byte count mismatch');
  const decoded=new Uint8Array(size);let offset=0;
  for(const piece of pieces){decoded.set(piece,offset);offset+=piece.byteLength;}
  if(await sha256(decoded)!==descriptor.decoded_sha256) throw Error('Decoded hash mismatch');
  return decoded.buffer;
}
export function applyCorrections(view, pose, target, vertexCount, enabled=true) {
  if(target.length!==vertexCount*4)throw Error('Invalid target shape');
  const {byte_offset:offset,record_count:count}=pose;
  if(!Number.isSafeInteger(offset)||offset<0||offset%16||!Number.isSafeInteger(count)||count<0||count>vertexCount||offset+count*16>view.byteLength)throw Error('Invalid pose record range');
  target.fill(0);
  if(!enabled)return 0;
  let previous=-1;
  for(let k=0;k<count;k++){
    const at=offset+k*16,index=view.getUint32(at,true);if(index>=vertexCount||index<=previous)throw Error('Invalid normal vertex index');previous=index;
    const x=view.getFloat32(at+4,true),y=view.getFloat32(at+8,true),z=view.getFloat32(at+12,true);
    if(![x,y,z].every(Number.isFinite)||Math.abs(Math.hypot(x,y,z)-1)>1e-4)throw Error('Invalid unit normal');
    target.set([x,y,z,1],index*4);
  }
  return count;
}
export function createChunkCache(asset, baseURL, fetchBytes=async url=>{const r=await fetch(url);if(!r.ok)throw Error('Chunk fetch failed: '+r.status);return r.arrayBuffer();}) {
  validateHeader(asset);
  const descriptors=new Map(asset.deformation_normals.chunks.map(c=>[c.id,c])),cache=new Map();
  let queue=Promise.resolve();const metrics={hits:0,misses:0,evictions:0,peak_cached_bytes:0,loads:[]};
  const snapshot=()=>({...metrics,loads:[...metrics.loads],cached_ids:[...cache.keys()],cached_decoded_bytes:[...cache.values()].reduce((n,v)=>n+v.byteLength,0)});
  function get(id){const task=queue.catch(()=>{}).then(async()=>{
    if(!descriptors.has(id))throw Error('Missing normal chunk');
    if(cache.has(id)){const value=cache.get(id);cache.delete(id);cache.set(id,value);metrics.hits++;return new DataView(value);}
    if(cache.size>=2){cache.delete(cache.keys().next().value);metrics.evictions++;}
    const d=descriptors.get(id),start=performance.now();metrics.misses++;
    const encoded=await fetchBytes(new URL(d.path,baseURL)),decoded=await decodeChunk(encoded,d);
    cache.set(id,decoded);metrics.peak_cached_bytes=Math.max(metrics.peak_cached_bytes,snapshot().cached_decoded_bytes);metrics.loads.push({id,encoded_bytes:encoded.byteLength,decoded_bytes:decoded.byteLength,fetch_decode_hash_ms:performance.now()-start});
    return new DataView(decoded);
  });queue=task;return task;}
  return {get,snapshot};
}
