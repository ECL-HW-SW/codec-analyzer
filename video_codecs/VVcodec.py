from GlobalPaths import GlobalPaths
from .Codec import Codec
import os
from pathlib import Path
import csv
from Logger import Logger
from .EncodingConfig import EncodingConfig


class VVcodec(Codec):

    def __init__(self, config_path, commit_hash, video):
        super().__init__("vvcodec", config_path, commit_hash=commit_hash)
        self._video = video
        # TODO: fix the initialization below
        self._encoding_config = EncodingConfig(27, 300, 29.97, "medium")


    # TODO: put in parent class probably
    # TODO: look into a "Singleton Dataclass" -- check if this would be better and feasible
    # or if it makes any sense at all really
    def set_encoding_config(
        self, config: EncodingConfig
    ) -> None:
        self._encoding_config = config


    def encode(self, force_rerun = 0, bitdepth = "8") -> str:
        log = Logger()       
        log.info("ENCODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        options_str = ''
        for key, val in self._options_encoder.items():
            options_str += f"--{key} {val} "

        # TODO: change the line below -- base_output_name should be different, probably
        base_output_name = "_".join([self._video.get_name(), str(self._encoding_config.qp) + "qp",
                                    str(self._encoding_config.nFrames) + "fr"])

        log.info(base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"], base_output_name + ".csv")

        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("Error parsing " + self.__report_path + " re-encoding")


        # FIXME: --internal-bitdepth cannot be hardcoded here. It should be within append_to_cmdline() or something like that
        cmdline = f'{self._encoder_path} -i {self._video.get_abs_path()} -v 6 --internal-bitdepth {bitdepth} '
        cmdline = self.__append_to_cmdline(cmdline)
        cmdline += f'--output {self.__bitstream_path} '        
        cmdline += f'> {self.__report_path}'

        os.system(cmdline)
        log.info("EXECUTED ENCODING COMMAND: " + cmdline) 


    def decode(self):
        log = Logger()
        log.info("\nDECODING VVCODEC...\n")
        paths = GlobalPaths().get_paths()

        base_output_name = self.get_unique_config()
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name + ".y4m")

        bitstream_path = self.get_bitstream()
        bitstream_path = bitstream_path.replace('~', p)
        if not os.path.exists(bitstream_path):
            log.info("Bitstream path does not exist.")

        part1 = f'{self.get_decoder_path()} -b {self.__bitstream_path} '
        part2 = f'-v 0 -f {self._video.get_framesnumber()} -o {self.__decoded_path} --y4m'
        cmdline = part1+part2 

        os.system(cmdline)
        log.info("EXECUTED DECODING COMMAND: " + cmdline)


    """
    Parses the txt output from the encode() method.
      
    @returns (bitrate, psnr, total time taken to encode)
    """
    def parse(self) -> tuple:
        with open(self.__report_path, 'r') as txt:
            text = txt.read().split("\n")
            for line in text:
                if "YUV-PSNR" in line.split():
                    data_line = text[text.index(line)+1].split()
                    break
            txt.close()
            bitrate = data_line[2]
            psnr = data_line[6]
            line_time = text[-2].split()
            total_time = line_time[2]

        return bitrate, psnr, total_time


    """
    Parses the .txt output from the encode() method and returns more information than the usual parse()

    @returns (bitrate, yuvpsnr, total time taken to encode, ypsnr, upsnr, vpsnr)
    """
    def parse_extra(self) -> tuple:        
        with open(self.__report_path, 'r') as txt:
            text = txt.read().split("\n")
            for line in text:
                if "YUV-PSNR" in line.split():
                    data_line = text[text.index(line)+1].split()
                    break
            bitrate = float(data_line[2])*1024
            yuvpsnr = data_line[6]
            ypsnr = data_line[3]
            upsnr = data_line[4]
            vpsnr = data_line[5]
            line_time = text[-2].split()
            total_time = line_time[2]

        return bitrate, yuvpsnr, total_time, ypsnr, upsnr, vpsnr
    

    """
    Adds to csv: 
    encoder name | video name | video resolution | fps | frame count | qp | bitrate | PSNR | time taken to encode | optional settings

    These csvs are stored in /VC/data/vvcodec-output/csv/{videoname}/
    """
    def add_to_csv(self, video) -> None:
        bitrate, psnr, timems, ypsnr, upsnr, vpsnr = self.parse_extra()
        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr', 'psnr','bitrate', 'time(s)','optional settings'])
            metrics_writer.writerow(["VVENC",video.get_name(),video.get_resolution(),video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),ypsnr,upsnr,vpsnr,psnr,bitrate,timems,self.get_unique_config()])
            metrics_file.close()
            

    def get_results(self) -> dict:
        bitrate, yuvpsnr, timems, ypsnr, upsnr, vpsnr = self.parse_extra()
        return {
            "ypsnr": ypsnr,
            "upsnr": upsnr,
            "vpsnr": vpsnr,
            "yuvpsnr": yuvpsnr,
            "bitrate": bitrate,
            "time": timems,
            "energyConsumption": 0}


    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["--threads"] = str(threads)
    

    def get_threads(self) -> str:
        return self.__threads


    def get_csv_path(self):
        return self.__csv_path


    """
    EXPERIMENTAL AND STUFF HOMIE DON'T MIND THIS TOO MUCH, YEAH?
    """    
    def __append_to_cmdline(self, cmdline: str) -> str:
        """
        This is equivalent to a switch case, which is only introduced in Python3.10 -- a pain to install and use
        so i'll just let this stay here as a method that can be specified to each codec. It'll probably go into the 
        parent class soon enough
        """

        # TODO: this is not scalable and needs to be fixed properly.
        equivalents = {
            "qp": f"--qp {self._encoding_config.qp}",
            "nFrames": f"-f {self._encoding_config.nFrames}",
            "preset": f"--preset {self._encoding_config.preset}",
            "fps": f"--fps {self._encoding_config.fps}",
            "nThreads": f"--threads {self._encoding_config.nThreads}",
            "codecSetAttrs": f""}
        attrs = [a for a in dir(self._encoding_config) if not a.startswith("__")]
        for a in attrs:
            if a != "uniqueAttrs" and a != "get_unique_attrs":
                cmdline += equivalents[a] + " "
        return cmdline


    def get_unique_attrs(self) -> str:
        return self._encoding_config.get_unique_attrs()

    
    def get_encoding_config(self) -> EncodingConfig:
        return self._encoding_config

    
    # TODO: 
    def get_base_attrs(self) -> str:
        return ""
