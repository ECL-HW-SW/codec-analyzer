#from EVC import EVC
from CodecComparator import CodecComparator
from video_codecs.VVcodec import VVcodec
from video_codecs.SVT import svt_codec
from Logger import Logger
from GlobalPaths import GlobalPaths
import utils
from Video import Video
from HttpContent import HttpContent



qps = [22,27,32,37]
num_frames = 30
paths = GlobalPaths("config/Paths.JSON").get_paths()
http = HttpContent("http://localhost:8080/api/codec-database")
video = Video("config/Bowing.JSON")
vvenc = VVcodec("config/VVEnc.JSON", "ec44ee022959410f9596175b9424d9fe1ece9bc8", video=video)
codecs = [vvenc]


tests = {}
for codec in codecs:
    codec.set_threads(4)
    for preset in ["faster", "fast", "medium", "slow", "slower"]:
        utils.create_output_dirs(paths, codec.get_codec(), preset)
        tests[preset] = {}
        for qp in qps:
            codec.set_qp(qp)
            codec.set_num_frames(num_frames)
            codec.set_preset(preset)

            # hasEntry returns bytes, which need to be converted to integer (this operation returns an ASCII value, hence the -48)
            response_bytes = http.hasEntry(codec.get_unique_config(), codec.get_commit_hash())
            entry_exists = int.from_bytes(response_bytes, "big") - 48

            if not entry_exists:
                codec.encode(video, force_rerun=1)
                codec.add_to_csv(video)
                tests[preset][qp] = codec.get_csv_path()
                info = codec.get_encoding_info()
                response = http.POST(info)
                print(response)
                with open("LOG_INFO.txt", "a") as file:
                    file.write(str(info))
                    file.write("\n")


#####
# comp = CodecComparator()
# print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))
# print("VVENC-EVC BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))
# print("VVENC-SVT BDRATE:", comp.bdrate(vvenc.get_csvs(), evc.get_csvs()))

