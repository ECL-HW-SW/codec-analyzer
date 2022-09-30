from EVC import EVC
from SVT import svt_codec
from VVcodec import VVcodec
from MetricsCalculator import MetricsCalculator
from Video import Video
import csv
from pathlib import Path

QP = 32
metrics = MetricsCalculator()
video = Video()

svt = svt_codec()
evc = EVC()
vvcodec = VVcodec()

csv_path = "~/VC/tests/csv/threads.csv"
p = Path('~').expanduser()
csv_path = csv_path.replace('~', str(p))

with open(csv_path, 'a') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    info = ['codec', 'sequence', 'threads', 'total time', 'qp']
    writer.writerow(info)

    threads = [2**i for i in range(4)] # 1, 2, 4, 8

    for codec in (svt, evc, vvcodec):
        for t in threads:
            codec.set_threads(t)
            codec.set_qp(QP)
            codec.encode()
            _, _, time = codec.parse()

            data = [codec.get_codec(), codec.get_videoname(), codec.get_threads(), time, codec.get_qp()]
            writer.writerow(data)
            
    csv_file.close()    

