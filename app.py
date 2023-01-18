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
evc = EVC("config/EVC.JSON", "COMMIT_HASH", video)
vvenc = VVcodec("config/VVEnc.JSON","COMMIT_HASH",video)
codecs = [vvenc,svt,evc]

#TODO: change the output directories model to one where all the files are kept inside a folder with the name of the video, during the process i noticed that
#the directories are being named with a _dir (refering to the JSON key instead of the value), the problem seems to be in the utils.py file.
#TODO: test all the methods used for computing methods, from the CodecComparator.py and MetricsCalculator.py files.
tests = {}
for codec in codecs:
    for preset in ["fast", "medium", "slow"]:
        utils.create_output_dirs(paths, codec.get_codec(),video.get_name(), preset)
        tests[preset] = {}
        for qp in qps:
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)
            codec.encode(1)
            codec.add_to_csv()
            codec.decode()
            tests[preset][qp] = codec.get_csv_path()
    


#####
comp = CodecComparator()
# print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))
# print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
# print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
