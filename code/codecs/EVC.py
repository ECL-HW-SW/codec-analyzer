from . import Codec
import os
import re
import csv

class EVC(Codec):
    def __init__(self,codec):
        super().__init__(codec)
        
    def encode(self,input,output,preset):
        os.system(f'xeve_app -i {self.get_raw_path()}/{input} -v 3 --preset {preset} -o {self.get_bitstream_path()}/{output} > {self.get_txts_path()}/{preset}_{input}.txt')

    def decode(self,input,output,preset):
        os.system(f'xevd_app -i {self.get_bitstream_path()}/{input} -o {self.get_decoded_path()}/{preset}_{output}')
    
    def parse(self,input,preset):
        
        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        pattern2 = re.compile(r"\d+\.\d+\skbps")
        parameters_lines = []

        with open(f'{self.get_txts_path()}/{preset}_{input}.txt') as temp:
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
                    Bitrate = original_data2[0]
                    parsed_data = (POC,Ftype,QP,PSNR_U,PSNR_V,PSNR_Y,Bits,Encode_time,Bitrate)
                    parameters_lines.append((parsed_data))
        temp.close()

        with open(f'{self.get_txts_path()}/{preset}_{input}.txt') as temp:
            text = temp.readlines()
            name = text[2].split('/')[-1]
            preset = text[5].split()[2]
            width = text[6].split()[2]
            height = text[7].split()[2]
            fps = text[8].split()[2]
            PSNR_Y_fullvideo = text[-12].split()[3]
            PSNR_U_fullvideo = text[-11].split()[3]
            PSNR_V_fullvideo = text[-10].split()[3]
            Brate_fullvideo = text[-6].split()[2]
            total_frames = text[-5].split()[4]
            geral_parameters = [name,preset,width,height,fps,PSNR_Y_fullvideo,PSNR_U_fullvideo,PSNR_V_fullvideo,Brate_fullvideo,total_frames]
        return sorted(parameters_lines),geral_parameters

    def add_to_csv(self,input,parameters):
        info = ['name','preset','width','height','FPS', 'PSNR-Y','PSNR-U','PSNR-V','Bitratekbps','frames']
        header=['POC', 'Ftype', 'QP', 'PSNR-Y','PSNR-U','PSNR-V','Bits','EncT(ms)','Bitratekbps']
        with open(f'{self.get_csvs_path()}/{input}parameters_frames.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(info)
            writer.writerow(parameters[1])
            writer.writerow(header)
            for line in parameters[0]:
                writer.writerow(line)
        csvfile.close()

    def gen_config(self):
        pass

