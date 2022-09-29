from EVC import EVC
from SVT import svt_codec
from VVcodec import VVcodec
from MetricsCalculator import MetricsCalculator
from Video import Video

QP = 32
metrics = MetricsCalculator()
video = Video()

svt = svt_codec()
evc = EVC()
vvcodec = VVcodec()

svt.set_qp(QP)
svt.encode()
svt.set_threads(3)
svt.encode()

