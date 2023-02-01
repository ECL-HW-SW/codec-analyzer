from GlobalPaths import GlobalPaths
import os
import csv
from .Codec import Codec
from Logger import Logger

class svt_codec(Codec):

    def __init__(self, config_path, commit_hash, video):
        super().__init__('svt', config_path, commit_hash=commit_hash)
        self._video = video
        self.__threads = self._options_encoder["threads"]
        self.__paths = GlobalPaths().get_paths()

    #############################GETTERS & SETTERS###########################################
    def get_threads(self) -> str:
        return self.__threads

    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["threads"] = str(threads)
    
    def get_qp(self):
        return self._options_encoder["qp"] 

    def set_qp(self, val):
        self._options_encoder["qp"] = val

    def get_csv_path(self):
        return self.__csv_path          

    def get_decodeds_path(self):
        return os.path.join(self.__paths[self._codec]["decoded_dir"])

    def get_csvs_path(self):
        self.__csvs_path = os.path.join(self.__paths[self._codec]["csv_dir"])
        return self.__csvs_path

    def get_preset(self) -> str:
        return self._options_encoder["preset"]
        
    def set_preset(self, val):
        self._options_encoder["preset"] = val

    def get_num_frames(self):
        return self._options_encoder["frames"]

    def set_num_frames(self, val):
        self._options_encoder["frames"] = val

    def get_unique_config(self) -> str:
        return "_".join([
            self._video.get_name(), str(self.get_qp()) + "qp", str(self.get_num_frames()) + "fr",
            self._video.get_fps() + "fps", self.get_preset() + "-preset", self.get_threads() + "t"
        ])

    def set_video(self, video) -> None:
        self._video = video

    def get_video(self):
        return self._video
    ####################################################################################################

    def encode(self, force_rerun = 0) -> str:
        log = Logger()
        log.info("ENCODING SVTAV1...")
        paths = GlobalPaths().get_paths()


        ##############SETTING PATHS VARIABLES################
        base_output_name = self.get_unique_config()
        log.info(base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__report_path_time = os.path.join(paths[self._codec]["report_dir"], base_output_name + "_time.txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"], base_output_name + ".csv")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name + ".yuv")
        ######################################################

        ####################CHECK RERUN#######################
        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("Error parsing " + self.__report_path + " re-encoding")
        #######################################################
        
        ##############ENCODER OPTIONS##########################
        frames = self._options_encoder["frames"]
        threads = self._options_encoder["threads"]
        preset = {
            "slower" : lambda x: 1,
            "slow" : lambda x: 4,
            "medium" : lambda x: 7,
            "fast" : lambda x: 10,
            "faster" : lambda x: 12,
        }[self._options_encoder["preset"]](self._options_encoder["preset"])
        #########################################################

        ###########COMMAND LINE ASSEMBLY##########################
        part1 = f"{self.get_encoder_path()} --enable-stat-report 1 --stat-file {self.__report_path} "
        part2 = f"--crf {self.get_qp()} --lp {threads} -n {frames} --preset {preset} -i {self._video.get_abs_path()} "
        part3 = f"--output {self.__bitstream_path} 2> {self.__report_path_time}"
        cmdline = part1+part2+part3
        ##########################################################

        ####################CALLING OS TO ENCODE##################
        print(cmdline)
        os.system(cmdline)
        log.info(cmdline) 
        ##########################################################

    def decode(self):     
        log = Logger()
        log.info("\nDECODING VVCODEC...\n")
        paths = GlobalPaths().get_paths()

        base_output_name = self.get_unique_config()
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name +".yuv")

        bitstream_path = self.__bitstream_path
        if not os.path.exists(bitstream_path):
            log.info("Bitstream path does not exist.")

        part1 = f"{self.get_decoder_path()} {self._options_decoder} -i {bitstream_path} " #@TODO fix options encoder
        part2 = f"-o {self.__decoded_path}"
        cmdline = part1+part2

        os.system(cmdline)
        return self.__decoded_path

    def parse(self) -> tuple:
        outgen = self.__report_path
        outtime = self.__report_path_time
        
        bitrate, psnryuv, psnry, psnru, psnrv, timems = self._parse_svt_output(outgen,outtime)
        return bitrate, psnryuv, psnry, psnru, psnrv, timems/1000

    def add_to_csv(self):

        bitrate, psnryuv, psnry, psnru, psnrv, time_s = self.parse()

        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr', 'psnr','bitrate', 'time(s)','optional settings'])
            metrics_writer.writerow(["VVENC",self._video.get_name(),self._video.get_resolution(),self._video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),psnry,psnru,psnrv,psnryuv,bitrate,time_s,self.get_unique_config()])
            metrics_file.close()

    def _parse_svt_output(self,pt1,pt2):

        BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
        with open(pt1, 'r') as output_text:
            out_string = output_text.readlines()
            results_index = (out_string.index(BR_STRING) + 1)
            bitrate = float(out_string[results_index].split()[20])
            psnry = float(out_string[results_index].split()[2])
            psnru = float(out_string[results_index].split()[4])
            psnrv = float(out_string[results_index].split()[6])
            psnryuv = float("{:.2f}".format((4*psnry + psnru +psnrv)/6))

        with open(pt2, 'rt') as outtime_text:
            outtime_string = outtime_text.readlines()
        for strtime in outtime_string:
            if not strtime.startswith("Total Encoding Time"):
                continue
            timems = float(strtime.split()[3])
        return bitrate*1024, psnryuv, psnry, psnru, psnrv, timems