from video_codecs.EVC import EVC
from CodecComparator import CodecComparator
from video_codecs.VVcodec import VVcodec
from video_codecs.SVT import svt_codec
from Logger import Logger
from GlobalPaths import GlobalPaths
import utils
from Video import Video

qps = [22,27,32,37]
num_frames = 30
paths = GlobalPaths("config/Paths.JSON").get_paths()
video = Video("config/Bowing.JSON")

svt = svt_codec("config/SVT.JSON","COMMIT_HASH", video)
#evc = EVC("config/EVC.JSON")
vvenc = VVcodec("config/VVEnc.JSON","COMMIT_HASH",video)
codecs = [vvenc, svt]

tests = {}
for codec in codecs:
    for preset in ["fast", "medium", "slow"]:
        utils.create_output_dirs(paths, codec.get_codec(), preset)
        tests[preset] = {}
        for qp in qps:
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)
            codec.encode(1)
            codec.add_to_csv()
            tests[preset][qp] = codec.get_csv_path()
    


#####
comp = CodecComparator()
# print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))
# print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
# print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
