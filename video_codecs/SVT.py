from GlobalPaths import GlobalPaths
import os
import csv
from .Codec import Codec
from Logger import Logger


class SVT(Codec):

    def __init__(self, codec_config, commit_hash, encoding_config, video):
        super().__init__("svt-av1", codec_config, commit_hash, encoding_config)
        self._video = video
        self.__paths = GlobalPaths().get_paths()


    def encode(self, force_rerun = 0) -> str:
        log = Logger()
        log.info("ENCODING SVTAV1...")
        paths = GlobalPaths().get_paths()

        # setting the relevant paths 
        base_output_name = "_".join([
            self._video.get_name(), str(self.encoding_config.qp) + "qp", str(self._encoding_config.nFrames) + "fr",
            self._encoding_config.fps + "fps", self.encoding_config.preset + "-preset", self._encoding_config.nThreads + "t"
        ]); log.debug("base output name (encode):", base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__report_path_time = os.path.join(paths[self._codec]["report_dir"], base_output_name + "_time.txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"], base_output_name + ".csv")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name + ".yuv")

        # used to check whether the encoding process should rerun
        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("Error parsing " + self.__report_path + " re-encoding")
        
        # setting up command line 
        cmdline = f'{self._encoder_path} -i {self._video.get_abs_path()} --enable-stat-report 1 '
        cmdline += f'--stat-file {self.__report_path} ' + self.__append_to_cmdline()
        cmdline += f'--output {self.__bitstream_path} 2> {self.__report_path_time} '

        # finally, encoding
        os.system(cmdline)
        log.debug(cmdline) 


    def decode(self):     
        log = Logger()
        log.info("DECODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        base_output_name = "_".join([
            self._video.get_name(), str(self.encoding_config.qp) + "qp", str(self._encoding_config.nFrames) + "fr",
            self._encoding_config.fps + "fps", self.encoding_config.preset + "-preset", self._encoding_config.nThreads + "t"
        ]); log.debug("base output name (encode):", base_output_name)
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
        # FIXME: the last return is supposed to be the energyConsumption, not yet implemented
        return bitrate, psnryuv, psnry, psnru, psnrv, timems/1000, 0

    
    #FIXME: this method, as it stands, is currently is deprecated and not updated
    def add_to_csv(self):

        bitrate, psnryuv, psnry, psnru, psnrv, time_s, _ = self.parse()

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
            psnryuv = float("{:.2f}".format((6*psnry + psnru +psnrv)/8))

        with open(pt2, 'rt') as outtime_text:
            outtime_string = outtime_text.readlines()
        for strtime in outtime_string:
            if not strtime.startswith("Total Encoding Time"):
                continue
            timems = float(strtime.split()[3])
        return bitrate*1024, psnryuv, psnry, psnru, psnrv, timems


    def __append_to_cmdline(self) -> str:
        """
        This is equivalent to a switch case, which is only introduced in Python3.10 -- a pain to install and use
        so i'll just let this stay here as a method that can be specified to each codec. It'll probably go into the 
        parent class soon enough
        """

        # FIXME: this is not scalable and needs to be fixed properly.
        equivalents = {
            "qp": f"--crf {self._encoding_config.qp}",
            "nFrames": f"-n {self._encoding_config.nFrames}",
            "preset": f"--preset {self._encoding_config.preset}",
            "fps": f"--fps {self._encoding_config.fps}",
            "nThreads": f"--lp {self._encoding_config.nThreads}",
            "codecSetAttrs": f"{self._encoding_config.codecSetAttrs}"}
        attrs = [a for a in dir(self._encoding_config) if not a.startswith("__")]
        for a in attrs:
            if a != "uniqueAttrs" and a != "get_unique_attrs" and a != "to_dict":
                cmdline += equivalents[a] + " "
        return cmdline


    def get_csv_path(self):
        return self.__csv_path    


    def get_decodeds_path(self):
        return os.path.join(self.__paths[self._codec]["decoded_dir"])


    def get_csvs_path(self):
        return self.__csvs_path

