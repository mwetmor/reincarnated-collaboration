import struct
class PE:
    def __init__(s,path):
        s.b=open(path,'rb').read()
        e=struct.unpack_from('<I',s.b,0x3c)[0]
        assert s.b[e:e+4]==b'PE\0\0'
        nsec=struct.unpack_from('<H',s.b,e+6)[0]; optsz=struct.unpack_from('<H',s.b,e+20)[0]
        opt=e+24; s.base=struct.unpack_from('<Q',s.b,opt+24)[0]
        s.secs=[]
        for i in range(nsec):
            o=opt+optsz+40*i
            name=s.b[o:o+8].rstrip(b'\0').decode()
            vsz,va,rsz,ro=struct.unpack_from('<IIII',s.b,o+8)
            s.secs.append((name,va,vsz,ro,rsz))
    def off2rva(s,off):
        for n,va,vsz,ro,rsz in s.secs:
            if ro<=off<ro+rsz: return va+off-ro
    def rva2off(s,rva):
        for n,va,vsz,ro,rsz in s.secs:
            if va<=rva<va+max(vsz,rsz): return ro+rva-va
    def sec(s,name):
        for x in s.secs:
            if x[0]==name: return x
