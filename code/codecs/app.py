from SVT import svt_codec
from CodecComparator import CodecComparator

qps = [22,27,32,37]

teste = svt_codec()
for qp in qps:
    teste.set_qp(qp)
    teste.encode()
    teste.add_to_csv()

comp = CodecComparator()
print(comp.bdrate(teste.get_csvs(),teste.get_csvs()))