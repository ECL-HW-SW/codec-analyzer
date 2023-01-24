from video_codecs.EVC import EVC
from CodecComparator import CodecComparator
from MetricsCalculator import MetricsCalculator
from video_codecs.VVcodec import VVcodec
from video_codecs.SVT import svt_codec
from Logger import Logger
from GlobalPaths import GlobalPaths
import utils
import os
from Video import Video

qps = [22,27,32,37]
num_frames = 30
paths = GlobalPaths("config/Paths.JSON").get_paths()
video = Video("config/Bowing.JSON")

svt = svt_codec("config/SVT.JSON","COMMIT_HASH", video)
evc = EVC("config/EVC.JSON", "COMMIT_HASH", video)
vvenc = VVcodec("config/VVEnc.JSON","COMMIT_HASH",video)
codecs = [svt,evc,vvenc]

metrics = MetricsCalculator()

#TODO: test all the methods used for computing methods, from the CodecComparator.py and MetricsCalculator.py files.
tests = {}
for codec in codecs:
    utils.create_output_dirs(paths, codec.get_codec(), video.get_name(),"metrics")
    for preset in ["fast", "medium", "slow"]:
        utils.create_output_dirs(paths, codec.get_codec(), video.get_name(),"", preset)
        tests[preset] = {}
        for qp in qps:
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)
            codec.encode()
            codec.add_to_csv()
            decoded_video = codec.decode()
            print(decoded_video)
            if decoded_video.endswith(".yuv"):
                video.to_y4m(decoded_video)
            tests[preset][qp] = codec.get_csv_path()
            for decoded_seqs in os.listdir(codec.get_decodeds_path()):
                if (os.path.splitext(decoded_seqs)[1]) == ".y4m":
                    outputname = os.path.splitext(decoded_seqs)[0]
                    metrics.vmaf(video.get_abs_path(),os.path.join(codec.get_decodeds_path(),decoded_seqs), "./output/"+codec.get_codec()+"/metrics/VMAF/" + video.get_name() +"/"+ outputname)    


#####
comp = CodecComparator()
#print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs_path(), evc.get_csvs_path()))
#print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs_path(), evc.get_csvs_path()))
#print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs_path(), evc.get_csvs_path()))



    
