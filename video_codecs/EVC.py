from .Codec import Codec
import os
import re
import csv
from pathlib import Path
from GlobalPaths import GlobalPaths
from Logger import Logger
#@fix EVC not detecting bowing in the path (to fix, add / before home in the path, parsing needs to be fixed)
class EVC(Codec):

    def __init__(self, config_path, commit_hash, video):
        super().__init__('evc', config_path, commit_hash=commit_hash)
        self._video = video
        self.__threads = self._options_encoder["threads"]
        self.__paths = GlobalPaths().get_paths()

################################GETTERS & SETTERS########################################################

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

###########################################################################################################

    def encode(self, force_rerun = 0) -> str:
        log = Logger()
        log.info("ENCODING EVC...")

        paths = GlobalPaths().get_paths()
        options_str = ''
        for key, val in self._options_encoder.items():
            options_str += f"--{key} {val} "        
        
        ##############SETTING PATHS VARIABLES###############
        base_output_name = self.get_unique_config()
        log.info(base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        self.__report_path2 = os.path.join(paths[self._codec]["report_dir"], base_output_name + "_parsed.txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"],base_output_name + ".csv")
        ######################################################

        ####################CHECK RERUN#######################
        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("EVC: Error parsing " + self.__report_path + " re-encoding")
        #######################################################

        part1 = f'{self.get_encoder_path()} -v 3 -i {self._video.get_abs_path()} -q {self.get_qp()} {options_str} '
        part2 = f'--output {self.__bitstream_path} '
        part3 = f'> {self.__report_path}'
        cmdline  = part1+part2+part3 

        print(cmdline)
        os.system(cmdline)

    def decode(self):
        log = Logger()
        log.info("\nDECODING VVCODEC...\n")
        paths = GlobalPaths().get_paths()

        base_output_name = self.get_unique_config()
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name + ".y4m")

        bitstream_path = self.__bitstream_path
        if not os.path.exists(bitstream_path):
            log.info("Bitstream path does not exist.")
        
        part1 = f'{self.get_decoder_path()} -i {self.__bitstream_path} '
        part2 = f'-o {self.__decoded_path}'

        os.system(part1+part2)


    def parse(self):        
        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        pattern2 = re.compile(r"\d+\.\d+\skbps")
        parameters_lines = []
        
        txt_path = self.__report_path

        with open(txt_path) as temp:
            text = temp.read()
            result = pattern.findall(text)
            result2 = pattern2.findall(text)
            for line in range(len(result)):
                original_data = result[line].split()
                original_data2 = result2[line-1].split()
                POC = int(original_data[0])
                Ftype = original_data[2][1]
                QP = original_data[3]
                PSNR_Y = original_data[4]
                PSNR_U = original_data[5]
                PSNR_V = original_data[6]
                Bits = original_data[7]
                Encode_time = original_data[8]
                Bitrate = float(original_data2[0])*1024
                Bitrate = f'{Bitrate:.4f}'
                parsed_data = (POC,Ftype,QP,PSNR_U,PSNR_V,PSNR_Y,Bits,Encode_time,Bitrate)
                parameters_lines.append((parsed_data))
        temp.close()

        new_path = self.__report_path

        with open(new_path) as temp:
            text = temp.readlines()
            name = self._video.get_name()
            # width = text[6].split()[2]
            # height = text[7].split()[2]
            resolution = self._video.get_resolution()
            fps = text[8].split()[2]
            QP= self.get_qp()
            PSNR_Y_fullvideo = float(text[-12].split()[3])
            PSNR_U_fullvideo = float(text[-11].split()[3])
            PSNR_V_fullvideo = float(text[-10].split()[3])
            psnr = ((4*PSNR_Y_fullvideo)+(PSNR_U_fullvideo)+(PSNR_V_fullvideo))/6
            psnr = float(f'{psnr:.4f}')
            Brate_fullvideo = float(text[-6].split()[2])*1024
            Brate_fullvideo = f'{Brate_fullvideo:.4f}'
            total_frames = text[-5].split()[4]
            time = text[-4].split()[6]
            geral_parameters = [name,resolution,fps,total_frames,QP,PSNR_Y_fullvideo,PSNR_U_fullvideo,PSNR_V_fullvideo,psnr,Brate_fullvideo]
            return Brate_fullvideo, psnr, time, PSNR_Y_fullvideo, PSNR_U_fullvideo, PSNR_V_fullvideo
#        return sorted(parameters_lines),geral_parameters, time

    def add_to_csv(self):
        
        bitrate, psnryuv, time_s, psnry, psnru, psnrv = self.parse()

        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr', 'psnr','bitrate', 'time(s)','optional settings'])
            metrics_writer.writerow(["EVC",self._video.get_name(),self._video.get_resolution(),self._video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),psnry,psnru,psnrv,psnryuv,bitrate,time_s,self.get_unique_config()])
            metrics_file.close()




#    def add_to_csv(self): #@fix
#        parameters = self.parse()
#
#        info = ['video','resolution','fps','number of frames','qp', 'PSNR-Y','PSNR-U','PSNR-V','psnr','bitrate']
#        header=['POC', 'Ftype', 'QP', 'PSNR-Y','PSNR-U','PSNR-V','Bits','EncT(ms)','Bitratekbps']
#        
#        csv_path = self.__csv_path
#        
#        with open(csv_path, 'w', newline='') as csvfile:
#            writer = csv.writer(csvfile, delimiter=',')
#            writer.writerow(info)
#            writer.writerow(parameters[1])
#            writer.writerow(header)
#            for line in parameters[0]:
#                writer.writerow(line)
#        csvfile.close()