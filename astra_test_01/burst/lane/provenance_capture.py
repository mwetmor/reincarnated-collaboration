"""Capture embedded PNG provenance at ingest, BEFORE any pixel transformation.

Reads tEXt/iTXt/zTXt, XMP and C2PA caBX presence using stdlib. Presence is NOT
signature verification. Opaque JUMBF/C2PA issuer/model/time remain null unless
exposed in readable metadata; never infer provenance from a filename. Retains
raw text keys/values and chunk names. Malformed/absent metadata is descriptive,
never a reason to lose an otherwise auditable generated-image record.
"""
import hashlib
import json
from pathlib import Path
import struct
import zlib
import xml.etree.ElementTree as ET

PNG_SIGNATURE=b'\x89PNG\r\n\x1a\n'
MAX_METADATA_BYTES=16*1024*1024  # Parser resource bound, not an art threshold.
ALIASES={
    'issuer': {'issuer','claim_generator','claim_generator_info','softwareagent'},
    'model': {'model','model_name','modelname','generative_model','generativemodel'},
    'generated_at': {'generated_at','generatedat','creation_time','creationtime',
                     'createdate','datecreated','datetimeoriginal'},
}


def _inflate(value):
    obj=zlib.decompressobj()
    raw=obj.decompress(value,MAX_METADATA_BYTES+1)
    if len(raw)>MAX_METADATA_BYTES or obj.unconsumed_tail:
        raise ValueError('Metadata exceeds parser limit')
    return raw


def _text(kind,data):
    key,rest=data.split(b'\0',1)
    if kind==b'tEXt':return key.decode('latin1'),rest.decode('latin1')
    if kind==b'zTXt':
        if not rest or rest[0]!=0:raise ValueError('Unknown zTXt compression')
        return key.decode('latin1'),_inflate(rest[1:]).decode('latin1')
    if len(rest)<2 or rest[0] not in (0,1) or rest[1]!=0:
        raise ValueError('Invalid iTXt compression')
    compressed=rest[0];language,translated,value=rest[2:].split(b'\0',2)
    return key.decode('latin1'),(_inflate(value) if compressed else value).decode('utf8')


def capture(png_path):
    path=Path(png_path)
    result=dict(path=str(path),sha256=None,issuer=None,model=None,generated_at=None,
                c2pa_present=False,xmp_present=False,raw_keys=[],raw_text={},chunks=[],notes=[])
    try:
        # Hash streaming: IDAT need not be retained or decoded.
        digest=hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
        result['sha256']=digest.hexdigest()
        with path.open('rb') as stream:
            if stream.read(8)!=PNG_SIGNATURE:
                result['notes'].append('Not a PNG signature; no embedded metadata read')
                return result
            while True:
                header=stream.read(8)
                if not header:break
                if len(header)!=8:raise ValueError('Truncated chunk header')
                length,kind=struct.unpack('>I4s',header)
                name=kind.decode('latin1');result['chunks'].append(name)
                if kind==b'caBX':result['c2pa_present']=True
                if kind in (b'tEXt',b'iTXt',b'zTXt'):
                    if length>MAX_METADATA_BYTES:raise ValueError('Metadata chunk exceeds parser limit')
                    data=stream.read(length);crc=stream.read(4)
                    if len(data)!=length or len(crc)!=4:raise ValueError('Truncated text chunk')
                    if zlib.crc32(kind+data)&0xffffffff!=struct.unpack('>I',crc)[0]:
                        result['notes'].append(f'{name}: invalid CRC; ignored');continue
                    try:
                        key,value=_text(kind,data)
                        result['raw_text'][key]=value
                    except (ValueError,UnicodeError,zlib.error) as exc:
                        result['notes'].append(f'{name}: {exc}')
                else:
                    stream.seek(length+4,1)
                if kind==b'IEND':break
        result['raw_keys']=sorted(result['raw_text'])
        def collect(key,value):
            local=key.rsplit('}',1)[-1].rsplit(':',1)[-1].lower().replace('-','_')
            for field,aliases in ALIASES.items():
                if local in aliases and result[field] is None:
                    if isinstance(value,(str,int,float)):
                        result[field]=str(value)
                    elif field=='issuer' and isinstance(value,list) and value and isinstance(value[0],dict):
                        result[field]=value[0].get('name')
            if isinstance(value,dict):
                for k,v in value.items():collect(k,v)
            elif isinstance(value,list):
                for v in value:
                    if isinstance(v,dict):collect('',v)
        for key,value in result['raw_text'].items():
            collect(key,value)
            lower=key.lower()
            if 'c2pa' in lower:result['c2pa_present']=True
            if 'xmp' in lower or 'adobe:ns:meta' in value:
                result['xmp_present']=True
                try:
                    for element in ET.fromstring(value).iter():
                        if element.text and element.text.strip():collect(element.tag,element.text.strip())
                        for k,v in element.attrib.items():collect(k,v)
                except ET.ParseError as exc:result['notes'].append('XMP parse: '+str(exc))
            try:collect('',json.loads(value))
            except (ValueError,TypeError):pass
    except (OSError,ValueError,struct.error) as exc:
        result['notes'].append(str(exc))
    if result['c2pa_present']:
        result['notes'].append('C2PA presence only; signatures and opaque JUMBF fields not verified')
    return result


def write_sidecar(png_path,out_dir):
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    target=out/(Path(png_path).stem+'.provenance.json')
    target.write_text(json.dumps(capture(png_path),indent=2,ensure_ascii=False)+'\n')
    return target
