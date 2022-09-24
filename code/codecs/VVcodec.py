from Codec import Codec
import os
from pathlib import Path
import csv

class VVcodec(Codec):
    def __init__(self):
        super().__init__("vvcodec")

    def encode(self):
        bitstream_path = self.get_bitstream()
        if not os.path.exists(bitstream_path):
            os.mkdir(bitstream_path)
        
        part1 = f'{self.get_encoder()} -i {self.get_videopath()} -q {self.get_qp()} {self.get_options_encoder()} '
        part2 = f'--output {self.get_bitstream()}/vvcodec_{self.get_videoname()}_{self.get_qp()}'
        part3 = f'> {self.get_txts()}/{self.get_videoname()}.txt' # TODO: mudar isso dps
        
        os.system(part1+part2+part3) 

    def decode(self):
        bitstream_path = self.get_bitstream()
        if not os.path.exists(bitstream_path):
            print("Bitstream path does not exist.")

        part1 = f'{self.get_decoder()} -i {self.get_bitstream()}/vvcodec_{self.get_videoname}_{self.get_qp()} {self.get_options_decoder()} '
        part2 = f'-o {self.get_decoded()}/vvcodec_{self.get_videoname()}_{self.get_qp()}'

        os.system(part1+part2)

    def _parse(self):
        p = Path('~').expanduser()
        txtoutput = f"{self.get_txts()}/{self.get_videoname()}.txt" # TODO: mudar isso dps
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
    
    def add_to_csv(self):
        outputcsvpath = self.get_csvs()
        if not os.path.exists(outputcsvpath):
            os.mkdir(outputcsvpath)

        outputcsv = outputcsvpath + '/' + self.get_videoname() +'_'+ self.get_qp() + ".csv"
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))

        bitrate, psnr, timems = self._parse()

        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["VVENC",self.get_videoname(),self.get_resolution(),self.get_fps(),self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])
            metrics_file.close()