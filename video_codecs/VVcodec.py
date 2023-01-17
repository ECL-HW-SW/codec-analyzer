from GlobalPaths import GlobalPaths
from .Codec import Codec
import os
from pathlib import Path
import csv
from Logger import Logger


class VVcodec(Codec):
    
    def __init__(self, config_path, commit_hash, video):
        super().__init__("vvcodec", config_path, commit_hash=commit_hash)
        self._video = video
        self.__threads = self._options_encoder["threads"]
    
    
    
    # TODO: transfer these getters and setters to the parent class if possible to reduce repetition
    # -----------------------------------------------------------------------
    # FIXME: not really anything to fix, i just needed a colourful annotation
    # things i've changed:
    #    1. Video class is now passed in as a constructor parameter, and changing the current video is done via setter
    #        --> this is so the method get_unique_config() works separately from encode()
    #    2. added get_preset() 
    #    3. added more information to the unique_config, for better database integration
    #    4. added get_unique_config() to return the unique_config
    #    5. added hasEntry to HttpContent to make use of the bool and check on app.py whether it should encode with those unique_configs

    ############################GETTERS & SETTERS############################################

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

    ###########################################################################################################

    def encode(self, force_rerun = 0) -> str: 
        log = Logger()       
        log.info("ENCODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        options_str = ''
        for key, val in self._options_encoder.items():
            options_str += f"--{key} {val} "

        # This relates to the "uniqueConfig" column in the codec-database
        # This, together with the commitHash, should be a unique combination that only occurs once in the DB
        # ex: bowing_22qp_30fr_29.97fps_fast-preset
        
        base_output_name = self.get_unique_config()
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


        part1 = f'{self.get_encoder_path()} -i {self._video.get_abs_path()} -q {self.get_qp()} {options_str} '
        part2 = f'--output {self.__bitstream_path} '
        part3 = f'> {self.__report_path}' # TODO: mudar isso dps (o que?)
        cmdline = part1+part2+part3 

        os.system(cmdline)
        log.info(cmdline)


    def decode(self):
        log = Logger()
        log.info("\nDECODING VVCODEC...\n")
        paths = GlobalPaths().get_paths()

        base_output_name = self.get_unique_config()
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name)

        if not os.path.exists(self.__bitstream_path):
            log.info("Bitstream path does not exist.")

        part1 = f'{self.get_decoder_path()} -b {self.__bitstream_path} '
        part2 = f'-v 0 -f {self._video.get_framesnumber()} -o {self.__decoded_path}'
        cmdline = part1+part2 

        os.system(cmdline)
        log.info(cmdline) 


    def parse(self) -> tuple:
        """
        Parses the txt output from the encode() method.
        @returns (bitrate, psnr, total time taken to encode)
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

    
    def parse_extra(self) -> tuple:
        """
        Parses the .txt output from the encode() method and returns more information than the usual parse()
        @returns (bitrate, yuvpsnr, total time taken to encode, ypsnr, upsnr, vpsnr)
        """
        
        with open(self.__report_path, 'r') as txt:
            text = txt.read().split("\n")
            for line in text:
                if "YUV-PSNR" in line.split():
                    data_line = text[text.index(line)+1].split()
                    break
            txt.close()
            bitrate = data_line[2]
            yuvpsnr = data_line[6]
            ypsnr = data_line[3]
            upsnr = data_line[4]
            vpsnr = data_line[5]
            line_time = text[-2].split()
            total_time = line_time[2]

        return bitrate, yuvpsnr, total_time, ypsnr, upsnr, vpsnr
    

    def add_to_csv(self):
        """
        Adds to csv: 
        encoder name | video name | video resolution | fps | frame count | qp | bitrate | PSNR | time taken to encode | optional settings
        These csvs are stored in /VC/data/vvcodec-output/csv/{videoname}/
        """


        bitrate, psnr, timems, ypsnr, upsnr, vpsnr = self.parse_extra()

        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr','bitrate', 'psnr', 'time(s)','optional settings'])
            metrics_writer.writerow(["VVENC",self._video.get_name(),self._video.get_resolution(),self._video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),ypsnr,upsnr,vpsnr,psnr,bitrate,timems,self.get_unique_config()])
            # TODO: I CHANGED video.get_framesnumber() ABOVE TO self.get_num_frames() --
            # CHECK IF THIS IS THE RIGHT THING TO DO OR NOT (I THINK IT IS)
            metrics_file.close()


    def get_encoding_info(self) -> dict:
        """
        Creates a dictionary with the same encoding info that is written to the csv file
        so that it can be sent in an HTTP request and stored into the database
        """

        bitrate, yuvpsnr, timems, ypsnr, upsnr, vpsnr = self.parse_extra()
        info_vvenc = {
            "codec": self.get_codec(),
            "commitHash": self.get_commit_hash(),
            "uniqueConfig": self.get_unique_config(),
            "video": self._video.get_name(),
            "resolution": self._video.get_resolution(),
            "fps": self._video.get_fps(),
            "nFrames": self.get_num_frames(),
            "qp": self.get_qp(),
            "ypsnr": ypsnr,
            "upsnr": upsnr,
            "vpsnr": vpsnr,
            "yuvpsnr": yuvpsnr,
            "bitrate": bitrate,
            "time": timems }
        return info_vvenc

