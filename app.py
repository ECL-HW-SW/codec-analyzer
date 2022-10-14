#from EVC import EVC
from CodecComparator import CodecComparator
#from SVT import svt_codec
from video_codecs.VVcodec import VVcodec
from Logger import Logger
from GlobalPaths import GlobalPaths
import utils
from Video import Video

qps = [22,27,32,37]
num_frames = 30
paths = GlobalPaths("config/Paths.JSON").get_paths()


vvenc = VVcodec("config/VVEnc.JSON")
codecs = [vvenc]

video = Video("config/Bowing.JSON")
tests = {}
for codec in codecs:
    for preset in ["faster", "fast", "medium", "slow", "slower"]:
        utils.create_output_dirs(paths, codec.get_codec(), preset)
        tests[preset] = {}
        for qp in qps:
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)
            codec.encode(video)
            codec.add_to_csv(video)
            tests[preset][qp] = codec.get_csv_path()
    


#####
comp = CodecComparator()
# print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))
# print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
# print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
