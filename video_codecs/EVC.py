from .Codec import Codec
import os
import re
import csv
from pathlib import Path
from GlobalPaths import GlobalPaths
from Logger import Logger


#FIXME: EVC not detecting bowing in the path (to fix, add / before home in the path, parsing needs to be fixed)
class EVC(Codec):

    def __init__(self, config_path, commit_hash, encoding_config, video):
        super().__init__('evc', config_path, commit_hash, encoding_config)
        self._video = video
        self.__paths = GlobalPaths().get_paths()


    def encode(self, force_rerun = 0) -> str:
        log = Logger()
        log.info("ENCODING EVC...")
        paths = GlobalPaths().get_paths()     
        
        # setting path variables 
        base_output_name = "_".join([
            self._video.get_name(), str(self.encoding_config.qp) + "qp", str(self._encoding_config.nFrames) + "fr",
            self._encoding_config.fps + "fps", self.encoding_config.preset + "-preset", self._encoding_config.nThreads + "t"
        ]); log.debug("base output name (encode):", base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__report_path = os.path.join(paths[self._codec]["report_dir"], base_output_name + ".txt")
        # self.__report_path2 = os.path.join(paths[self._codec]["report_dir"], base_output_name + "_parsed.txt")
        self.__csv_path = os.path.join(paths[self._codec]["csv_dir"],base_output_name + ".csv")

        # checking rerun
        if not force_rerun and os.path.isfile(self.__report_path):
            try:
                self.parse()
                return
            except:
                log.info("EVC: Error parsing " + self.__report_path + " re-encoding")

        # setting up encoding command
        cmdline = f'{self.get_encoder_path()} -i {self._video.get_abs_path()} '
        cmdline += self.__append_to_cmdline()
        cmdline += f'--output {self.__bitstream_path} > {self.__report_path}'

        # executing command
        os.system(cmdline)
        log.debug("EXECUTED DECODING COMMAND: ", cmdline)


    def decode(self):
        log = Logger()
        log.info("DECODING VVCODEC...")
        paths = GlobalPaths().get_paths()

        base_output_name = "_".join([
            self._video.get_name(), str(self.encoding_config.qp) + "qp", str(self._encoding_config.nFrames) + "fr",
            self._encoding_config.fps + "fps", self.encoding_config.preset + "-preset", self._encoding_config.nThreads + "t"
        ]); log.debug("base output name (encode):", base_output_name)
        self.__bitstream_path = os.path.join(paths[self._codec]["bitstream_dir"], base_output_name + ".bin")
        self.__decoded_path = os.path.join(paths[self._codec]["decoded_dir"], base_output_name + ".y4m")

        bitstream_path = self.__bitstream_path
        if not os.path.exists(bitstream_path):
            log.info("Bitstream path does not exist.")
        
        part1 = f'{self.get_decoder_path()} -i {self.__bitstream_path} '
        part2 = f'-o {self.__decoded_path}'

        os.system(part1+part2)
        return self.__decoded_path


    def parse(self):        
        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        pattern2 = re.compile(r"\d+\.\d+\skbps")
        parameter_lines = []
        
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
                parameter_lines.append((parsed_data))
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
            psnr = ((6*PSNR_Y_fullvideo)+(PSNR_U_fullvideo)+(PSNR_V_fullvideo))/8
            psnr = float(f'{psnr:.4f}')
            bitrate = float(text[-6].split()[2])*1024
            bitrate = f'{bitrate:.4f}'
            total_frames = text[-5].split()[4]
            time = text[-4].split()[6]
            geral_parameters = [name,resolution,fps,total_frames,QP,PSNR_Y_fullvideo,PSNR_U_fullvideo,PSNR_V_fullvideo,psnr,Brate_fullvideo]
            # FIXME: the last return is supposed to be the energyConsumption, which is not yet implemented
            return bitrate, psnr, time, PSNR_Y_fullvideo, PSNR_U_fullvideo, PSNR_V_fullvideo, 0


    # FIXME: the following method is deprecated and needs to be updated.
    # avoid using it if possible
    def add_to_csv(self):
        
        bitrate, psnryuv, time_s, psnry, psnru, psnrv = self.parse()

        with open(self.__csv_path, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['codec','video','resolution','fps','number of frames','qp','ypsnr','upsnr','vpsnr', 'psnr','bitrate', 'time(s)','optional settings'])
            metrics_writer.writerow(["EVC",self._video.get_name(),self._video.get_resolution(),self._video.get_fps(),
                                        self.get_num_frames(),self.get_qp(),psnry,psnru,psnrv,psnryuv,bitrate,time_s,self.get_unique_config()])
            metrics_file.close()


    def get_csv_path(self):
        return self.__csv_path        


    def get_csvs_path(self):
        self.__csvs_path = os.path.join(self.__paths[self._codec]["csv_dir"])
        return self.__csvs_path


    def get_decodeds_path(self):
        return os.path.join(self.__paths[self._codec]["decoded_dir"])            
