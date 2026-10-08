from xref import *
import capstone,sys
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); md.detail=False
def dis(start,end):
    off=start-va
    for ins in md.disasm(text[off:end-va],start):
        yield ins
def show(start,end):
    for ins in dis(start,end): print(hex(ins.address),ins.mnemonic,ins.op_str)
if __name__=='__main__':
    show(int(sys.argv[1],16),int(sys.argv[2],16))
_pd=p.sec('.pdata')
FUNCS=[struct.unpack_from('<III',p.b,_pd[3]+12*k) for k in range(_pd[2]//12)]
def func_of(rva):
    best=[f for f in FUNCS if f[0]<=rva<f[1]]
    return best
