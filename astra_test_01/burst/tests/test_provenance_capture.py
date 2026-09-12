import json
import struct
import tempfile
from pathlib import Path
import unittest
import zlib
from PIL import Image,PngImagePlugin
from lane.provenance_capture import capture,write_sidecar

class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory(dir=Path(__file__).parent/'tmp');self.addCleanup(td.cleanup)
        self.root=Path(td.name)
    def test_text_itxt_ztxt_xmp_and_c2pa(self):
        p=self.root/'image.png';info=PngImagePlugin.PngInfo()
        info.add_itxt('provenance',json.dumps(dict(model='synthetic-model',issuer='fixture',generated_at='2026-09-11')),zip=True)
        info.add_text('Description','compressed description',zip=True)
        info.add_text('Author','fixture author')
        info.add_itxt('XML:com.adobe.xmp','<x:xmpmeta xmlns:x="adobe:ns:meta/"/>')
        Image.new('RGB',(8,8),(0,255,0)).save(p,pnginfo=info)
        raw=p.read_bytes();data=b'opaque JUMBF';chunk=b'caBX'
        injected=struct.pack('>I',len(data))+chunk+data+struct.pack('>I',zlib.crc32(chunk+data)&0xffffffff)
        p.write_bytes(raw[:-12]+injected+raw[-12:])
        r=capture(p);self.assertEqual(r['issuer'],'fixture');self.assertEqual(r['model'],'synthetic-model')
        self.assertEqual(r['generated_at'],'2026-09-11');self.assertTrue(r['c2pa_present']);self.assertTrue(r['xmp_present'])
        self.assertEqual(r['raw_text']['Description'],'compressed description')
        self.assertIn('Author',r['raw_keys'])
        side=write_sidecar(p,self.root);self.assertEqual(side.name,'image.provenance.json')
        self.assertEqual(json.loads(side.read_text()),r)
    def test_bare_and_unreadable(self):
        p=self.root/'bare.png';Image.new('RGB',(2,2)).save(p)
        for value in (p,self.root/'missing.png'):
            r=capture(value)
            self.assertIsNone(r['issuer']);self.assertIsNone(r['model']);self.assertIsNone(r['generated_at'])
            self.assertFalse(r['c2pa_present'])
