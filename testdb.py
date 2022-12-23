from HttpContent import HttpContent
import json

http = HttpContent("http://localhost:8080/api/codec-database")

info = {
            "codec": "SVT-AV1",
            "video": "bowling_cif",
            "resolution": "ANKARA MESSI RESOLUTION",
            "fps": 29.97,
            "nFrames": 300,
            "qp": 27,
            "ypsnr": 32.05,
            "upsnr": 39.78,
            "vpsnr": 31.423,
            "yuvpsnr": 37.32193728,
            "bitrate": 2178327.32,
            "time": 2.5
        }

print(http.DELETE("526b7f8a-5d09-4287-acdd-0d860c7cfd23"))

from CodecComparator import CodecComparator
from video_codecs.VVcodec import VVcodec
from Logger import Logger
from GlobalPaths import GlobalPaths
import utils
from Video import Video
from HttpContent import HttpContent

qps = [22, 27, 32, 37]
vvenc = VVcodec("config/VVEnc.JSON")
video = Video("config/Bowing.JSON")
http = HttpContent("http://localhost:8080/api/codec-database")
paths = GlobalPaths("config/Paths.JSON").get_paths()
num_frames = 30

vvenc.set_num_frames(num_frames)

for preset in ["faster", "fast", "medium", "slow", "slower"]:
    utils.create_output_dirs(paths, vvenc.get_codec(), preset)
    for qp in qps:
        vvenc.set_qp(qp)
        vvenc.set_preset(preset)
        vvenc.encode(video)
        vvenc.add_to_csv(video)
        info = vvenc.get_encoding_info()
        http.POST(info)

all = http.GET()
for stat in all:
    print(stat)
