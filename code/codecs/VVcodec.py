from Codec import Codec
import os
from pathlib import Path
import csv

class VVcodec(Codec):
    def __init__(self, vidpath):
        super().__init__("vvcodec", vidpath)

    """
    The methods below should probably be in the super class as they are reused in other classes
    """
    def gen_config(self):
        pass

    def get_options_decoder(self):
        return self.__options_decoder
    
    def get_outtime(self):
        return self.__outtime
    """
    The methods above should probably be in the super class as they are reused in other classes
    """

    def encode(self, input, output, preset):
        os.system(f'{self.get_encoder()} -i {self.get_raw()}/{input} --frames {self.get_framesnumber()} \
            --output {self.get_bitstream()}/{output} {self.get_options_encoder()} --preset {preset} > {self.get_txts()}/{preset}_{input}.txt')

    def decode(self, input, output, preset):
        os.system(f'{self.get_decoder()} -b {self.get_bitstream()}/{input} -o {self.get_decoded()}/{preset}_{output}')
    
    def parse(self, input, preset):
        p = Path('~').expanduser()
        txtoutput = f"{self.get_txts()}/{preset}_{input}"
        txtoutput = txtoutput.replace('~', str(p))

        with open(txtoutput, 'r') as txt:
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
    
    def add_to_csv(self, bitrate, psnr, timems):
        outputcsvpath = self.get_csvs()
        outputcsv = outputcsvpath + '/' + self.get_videoname() +'_'+ self.get_qp() + ".csv"
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["VVENC",self.get_videoname(),self.get_resolution(),self.get_fps(),self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])
            metrics_file.close()
        
        os.system("cat " + outputcsv)