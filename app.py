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
codecs = [vvenc]

metrics2calculate = ["VMAF","BDBR","BDPSNR"]

metrics = MetricsCalculator()

#TODO: test all the methods used for computing methods, from the CodecComparator.py and MetricsCalculator.py files.
#TODO: test.py in output/evc/metrics/vmaf/bowing
#TODO: fix vvc decoder outputing files with different bitdepth (detectec during vmaf calculation)
tests = {}
    
for codec in codecs:
    #creates the output directories for the metrics from the MetricsCalculator
    utils.create_output_dirs(paths, codec.get_codec(), video.get_name(),"metrics")
    
    for preset in ["fast", "medium", "slow"]:
        #creates output dirs for each preset and video
        utils.create_output_dirs(paths, codec.get_codec(), video.get_name(),"", preset)
        tests[preset] = {}

        for qp in qps:
            
            #set the configurations for this iteration
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)

            #encode and parse the results into a csv file
            codec.encode()
            codec.add_to_csv()

            #decode the video, returns into decoded_video the full path of the decoded video file. 
            decoded_video = codec.decode()

            #check if the decoded video is in the yuv format or if it hasnt already been converted to y4m, then converts the video if necessary
            if decoded_video.endswith(".yuv") and not os.path.isfile(os.path.splitext(decoded_video)[0]+".y4m"):
                video.to_y4m(decoded_video)

            tests[preset][qp] = codec.get_csv_path()

        #when all the qps have been calculated, iterates trhough all the resulting decoded sequences in order to compare them with the original video using the metricsCalculator
        for decoded_seqs in os.listdir(codec.get_decodeds_path()):
            if (os.path.splitext(decoded_seqs)[1]) == ".y4m":
                outputname = os.path.splitext(decoded_seqs)[0]
                metrics.vmaf(video.get_abs_path(),os.path.join(codec.get_decodeds_path(),decoded_seqs), "./output/"+codec.get_codec()+"/metrics/VMAF/" + video.get_name() +"/"+ outputname)    
                metrics.vmaf_parse("./output/"+codec.get_codec()+"/metrics/VMAF/" + video.get_name())

#####
comp = CodecComparator()
#print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs_path(), evc.get_csvs_path()))
#print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs_path(), evc.get_csvs_path()))
#print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs_path(), evc.get_csvs_path()))



    
