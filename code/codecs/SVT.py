import os
import json
import csv
from pathlib import Path
from Codec import Codec

class svt_codec(Codec):

    def __init__(self):
        super().__init__('svt')
        with open('code/codecs/JSON_files/paths.JSON') as json_file:
            data = json.load(json_file)
            self.__decoder = data['svt']['decoder']
            self.__options_encoder = data['svt']['options_encoder']
            self.__options_decoder = data['svt']['options_decoder']
            self.__outtime = data['svt']['outtime']

    def gen_config(self):
        pass

    def get_decoder(self):
        return self.__decoder

    def get_options_encoder(self):
        return self.__options_encoder
    
    def get_options_decoder(self):
        return self.__options_decoder

    def get_outtime(self):
        return self.__outtime

    def encode(self):
        svtpath = self.get_encoder()
        options_svte = '--crf '+self.get_qp() + ' ' + self.get_options_encoder()
        bitstream_path = self.get_bitstream()
        p = Path('~').expanduser()
        bitstream_path = bitstream_path.replace("~",str(p))
        if not(os.path.exists(bitstream_path)):
            os.mkdir(bitstream_path)
        encoded_out = self.get_bitstream() + "/svtenc_" + self.get_videoname() + "_" + self.get_qp()
        outgen = self.get_txts()+"/"+self.get_videoname()+"_stat.txt"
        outtime = self.get_outtime()+"/"+self.get_videoname()+"_time.txt"
        cmdline = svtpath + ' --enable-stat-report 1  --stat-file ' + outgen  + ' ' + options_svte
        cmdline += ' -i ' + self.get_videopath() + ' -b ' + encoded_out + ' 2> ' + outtime 
        print(cmdline)    #@fix
        os.system(cmdline)    #@fix

    def decode(self):
        svtpath = self.get_decoder()
        options_svtd = self.get_options_decoder()
        encoded_out = self.get_bitstream()+"/svtenc_"+self.get_videoname()
        decoded_out = self.get_decoded()+"/svtdec_"+self.get_videoname()
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)     #@fix
        os.system(cmdline)    #@fix

    def parse(self):
        outgen = self.get_txts()+"/"+self.get_videoname()+"_stat.txt"
        outtime = self.get_outtime()+"/"+self.get_videoname()+"_time.txt"
        p = Path('~').expanduser()
        outgen=outgen.replace("~",str(p))
        outtime=outtime.replace("~",str(p))
        bitrate, psnr, timems = self.parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems

    def add_to_csv(self):
        outputcsvpath = self.get_csvs()
        p = Path('~').expanduser()
        outputcsvpath = outputcsvpath.replace("~",str(p))
        if not(os.path.exists(outputcsvpath)):
            os.mkdir(outputcsvpath)
        outputcsv = outputcsvpath + '/' + self.get_videoname() +'_'+ self.get_qp() + ".csv"
        bitrate,psnr,timems = self.parse()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["SVT-AV1",self.get_videoname(),self.get_resolution(),self.get_fps(),self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])
            metrics_file.close()

    def parse_svt_output(self,pt1,pt2):

        BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
        with open(pt1, 'r') as output_text:
            out_string = output_text.readlines()
            results_index = (out_string.index(BR_STRING) + 1)
            bitrate_string = out_string[results_index].split()[20]
            psnr_string = out_string[results_index].split()[2]
        with open(pt2, 'rt') as outtime_text:
            outtime_string = outtime_text.readlines()
        for strtime in outtime_string:
            if not strtime.startswith("Total Encoding Time"):
                continue
            timems_string = strtime.split()[3]
        return float(bitrate_string)*1024, float(psnr_string) , float(timems_string)

