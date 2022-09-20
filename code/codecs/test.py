from VVcodec import VVcodec
from SVT import svt_codec
from EVC import EVC
from MetricsCalculator import MetricsCalculator
import matplotlib.pyplot as plt
import json

"""
The goal of these tests is to generate MS-SSIM figures for VVenc, HEVC and SVT-AV1 with the purpose of plotting their results on a graph
"""

qps = [22, 27, 32, 37]

video_in = "BasketballPass_416x240_50"
bin_out = "out_BasketballPass"
preset = "faster"
decoded_vvenc = "vvenc_BasketballPass"
#decoded_av1 = "av1_BasketballPass"
decoded_evc = "evc_BasketballPass"

metrics = MetricsCalculator()

vvenc = VVcodec()
#av1 = svt_codec()
evc = EVC()

rvvenc = list()
rav1 = list()
revc = list()

for qp in qps:
    vvenc.encode(video_in, bin_out, preset)
    vvenc.decode(bin_out, decoded_vvenc, preset)

    # need to initialize av1's constructor, no arguments needed on encode()
    #av1.encode()
    #av1.decode()

    # no preset for evc?
    evc.encode(video_in, bin_out, preset)
    evc.decode(bin_out, decoded_evc, preset)

    # need to install all 3 of them for this to work
    
    
    rvvenc.append(metrics.msssim(video_in, decoded_vvenc))
    #rav1.append(metrics.msssim(video_in, decoded_av1))
    revc.append(metrics.msssim(video_in, decoded_evc))

# plotting the graph
plt.figure(figsize=(15, 8))
plt.xlabel("Quantization Parameters")
plt.ylabel("MS-SSIM")
plt.title("MS-SSIM Comparison for VVENC, HEVC and SVT-AV1")
#plt.plot(qps, rav1, "g--")
plt.plot(qps, rvvenc, "b:")
plt.plot(qps, revc, "r-")

print('end of tests')