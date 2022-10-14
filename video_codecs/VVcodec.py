from GlobalPaths import GlobalPaths
from .Codec import Codec
import os
from pathlib import Path
import csv
from Logger import Logger

class VVcodec(Codec):
    def __init__(self, config_path):
        super().__init__("vvcodec", config_path)
    
    def set_qp(self, val):
        self._options_encoder["qp"] = val
    
    def get_qp(self):
        return self._options_encoder["qp"] 

    def set_num_frames(self, val):
        self._options_encoder["frames"] = val
    
    def set_preset(self, val):
        self._options_encoder["preset"] = val
    
    def get_num_frames(self):
        return self._options_encoder["frames"]

    def encode(self, video, force_rerun = 0) -> str: 
        log = Logger()       
        log.info("ENCODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        options_str = ''
        for key, val in self._options_encoder.items():
            options_str += f"--{key} {val} "

        base_output_name = "_".join([video.get_name(), str(self.get_qp()) + "qp", str(self.get_num_frames()) + "fr"])
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"], base_output_name + ".csv")

        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("Error parsing " + self.__report_path + " re-encoding")


        part1 = f'{self._encoder_path} -i {video.get_abs_path()} -q {self.get_qp()} {options_str} '
        part2 = f'--output {self.__bitstream_path} '
        part3 = f'> {self.__report_path}' # TODO: mudar isso dps
        cmdline  =part1+part2+part3 

        os.system(cmdline)
        log.info(cmdline) 

    def decode(self):
        print("\nDECODING VVCODEC...\n")

        p = str(Path('~').expanduser())

        decoded_path = self.get_decoded()
        decoded_path = decoded_path.replace('~', p)

        bitstream_path = self.get_bitstream()
        bitstream_path = bitstream_path.replace('~', p)
        if not os.path.exists(bitstream_path):
            print("Bitstream path does not exist.")

        part1 = f'{self.get_decoder()} -b {bitstream_path}/vvcodec_{self.get_videoname()}_{self.get_qp()} {self.get_options_decoder()} '
        part2 = f'-v 0 -f {self.get_framesnumber()} -o {decoded_path}/vvcodec_{self.get_videoname()}_{self.get_qp()}'
        cmdline = part1+part2 

        os.system(cmdline)
        print(cmdline) 

    def parse(self) -> tuple:
        """
        Parses the txt output from the encode() method.

        @return (bitrate, psnr, total time taken to encode)
        """

        

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
    
    def add_to_csv(self, video):
        """
        Adds to csv: 
        encoder name | video name | video resolution | fps | frame count | qp | bitrate | PSNR | time taken to encode | optional settings

        These csvs are stored in /VC/data/vvcodec-output/csv/{videoname}/
        """


        bitrate, psnr, timems = self.parse()

        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["VVENC",video.get_name(),video.get_resolution(),video.get_fps(),
                                        video.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self._options_encoder])
            metrics_file.close()

    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["--threads"] = str(threads)
    
    def get_threads(self) -> str:
        return self.__threads

    def get_csv_path(self):
        return self.__csv_path