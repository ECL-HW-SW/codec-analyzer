from EVC import EVC
from CodecComparator import CodecComparator
from SVT import svt_codec
qps = [22,27,32,37]

svt = svt_codec()
evc = EVC()
# for qp in qps:
#     svt.set_qp(qp)
#     svt.encode()
#     # a = svt.parse()
#     svt.add_to_csv()
#     evc.set_qp(qp)
#     evc.encode()
#     a = evc.parse()
#     evc.add_to_csv(a)


comp = CodecComparator()
print(comp.bdrate(svt.get_csvs(),evc.get_csvs()))
print(comp.bdrate(evc.get_csvs(),svt.get_csvs()))
