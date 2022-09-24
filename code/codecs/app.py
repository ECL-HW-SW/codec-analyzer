from EVC import EVC
from CodecComparator import CodecComparator
from SVT import svt_codec
from VVcodec import VVcodec
qps = [22,27,32,37]

svt = svt_codec()
evc = EVC()
vvenc = VVcodec()
for qp in qps:
    svt.set_qp(qp)
    svt.encode()
    svt.add_to_csv()
    
    vvenc.set_qp(qp)
    vvenc.encode()
    vvenc.add_to_csv
    
    # a = svt.parse()
    evc.set_qp(qp)
    evc.encode()
    a = evc.parse()
    evc.add_to_csv(a)

comp = CodecComparator()
print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))
print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
