import d4b_dis as D, struct, re, sys
pe=D.pe; raw=pe.raw
def str_rvas(s):
    out=[]
    for m in re.finditer(re.escape(s.encode())+b'\x00', raw):
        off=m.start()
        # offset -> rva
        for sec in pe.sections:
            if sec['raddr']<=off<sec['raddr']+sec['rsize']:
                out.append(sec['vaddr']+off-sec['raddr'])
    return out
def xrefs(rva):
    va=rva+D.IB; pat=struct.pack('<I',va); res=[]
    text=[s for s in pe.sections if s['name']=='.text'][0]
    b=raw[text['raddr']:text['raddr']+text['rsize']]
    for m in re.finditer(re.escape(pat), b):
        res.append(text['vaddr']+m.start())
    return res
if __name__=='__main__':
    for s in sys.argv[1:]:
        for r in str_rvas(s):
            print(s, hex(r), [ (hex(x), D.nearest(x)) for x in xrefs(r)])
