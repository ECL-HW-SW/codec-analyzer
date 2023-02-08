from GlobalPaths import GlobalPaths
from .Codec import Codec
import os
from pathlib import Path
import csv
from Logger import Logger
from .EncodingConfig import EncodingConfig


class VVcodec(Codec):

    def __init__(self, config_path, commit_hash, encoding_config, video):
        super().__init__("vvcodec", config_path, commit_hash, encoding_config)
        self._video = video


    def encode(self, force_rerun = 0, bitdepth = "8") -> str:
        log = Logger()       
        log.info("ENCODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        # TODO: change the line below -- base_output_name should be different, probably
        # FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
        base_output_name = "_".join([
            self._video.get_name(), str(self.encoding_config.qp) + "qp", str(self._encoding_config.nFrames) + "fr",
            self._encoding_config.fps + "fps", self.encoding_config.preset + "-preset", self._encoding_config.nThreads + "t"
        ]); log.debug("base output name (encode):", base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"], base_output_name + ".csv")

        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse_extra()
                return
            except:
                log.info("Error parsing " + self.__report_path + " re-encoding")


        # FIXME: --internal-bitdepth cannot be hardcoded here. It should be within append_to_cmdline() or something like that
        cmdline = f'{self._encoder_path} -i {self._video.get_abs_path()} -v 6 --internal-bitdepth {bitdepth} '
        cmdline += self.__append_to_cmdline(cmdline)
        cmdline += f'--output {self.__bitstream_path} '        
        cmdline += f'> {self.__report_path}'

        os.system(cmdline)
        log.debug("EXECUTED ENCODING COMMAND: " + cmdline) 


    def decode(self):
        log = Logger()
        log.info("\nDECODING VVCODEC...\n")
        paths = GlobalPaths().get_paths()

        base_output_name = "_".join([
            self._video.get_name(), str(self.get_qp()) + "qp", str(self.get_num_frames()) + "fr",
            self._video.get_fps() + "fps", self.get_preset() + "-preset", self.get_threads() + "t"
        ]); log.debug("base output name (decode):", base_output_name)
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
    # TODO: make parse_extra the default parse and remove the other one
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

        # FIXME: the last return is supposed to be the energyConsumption, which is not yet implemented
        return bitrate, yuvpsnr, total_time, ypsnr, upsnr, vpsnr, 0 
    

    """
    Adds to csv: 
    encoder name | video name | video resolution | fps | frame count | qp | bitrate | PSNR | time taken to encode | optional settings

    These csvs are stored in /VC/data/vvcodec-output/csv/{videoname}/
    #FIXME: this method, as it stands, is currently not updated and deprecated
    """
    def add_to_csv(self, video) -> None:
        bitrate, psnr, timems, ypsnr, upsnr, vpsnr, _ = self.parse_extra()
        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr', 'psnr','bitrate', 'time(s)','optional settings'])
            # FIXME: this is all wrong
            metrics_writer.writerow(["VVENC",video.get_name(),video.get_resolution(),video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),ypsnr,upsnr,vpsnr,psnr,bitrate,timems,self._encoding_config()])
            metrics_file.close()
