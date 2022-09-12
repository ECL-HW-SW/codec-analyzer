import os
import json
import csv
from pathlib import Path

class svt_codec:

    def __init__(self,rawvideo,configs):
        with open(rawvideo, 'r') as video: 
            self.__raw = json.load(video)
        with open(configs,'r') as cfg:
            self.data = json.load(cfg)
        self.name = self.__raw["name"]
        

    def encode(self):
        svtpath = self.data["paths"]["encoder"]
        options_svte = self.data["paths"]["options_encoder"]
        encoded_out = self.data["paths"]["encoded"]+"/svtenc_"+self.name
        outgen = self.data["paths"]["outgen"]+"/"+self.name+".log"
        outtime = self.data["paths"]["outtime"]+"/"+self.name+".txt"
        cmdline = svtpath + ' --enable-stat-report 1 --stat-file ' + outgen  + ' ' + options_svte
        cmdline += ' -i ' + self.__raw["path"] + ' -b ' + encoded_out + ' 2> ' + outtime 
        print(cmdline)
        os.system(cmdline)

    def decode(self):
        svtpath = self.data["paths"]["decoder"]
        options_svtd = self.data["paths"]["options_decoder"]
        encoded_out = self.data["paths"]["encoded"]+"/svtenc_"+self.name
        decoded_out = self.data["paths"]['bitstream']+"/svtdec_"+self.name
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        os.system(cmdline)

    def parse(self):
        outgen = self.data["paths"]["outgen"]+"/"+self.name+".log"
        outtime = self.data["paths"]["outtime"]+"/"+self.name+".txt"
        p = Path('~').expanduser()
        outgen=outgen.replace("~",str(p))
        outtime=outtime.replace("~",str(p))
        bitrate, psnr, timems = self.parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems

    def parsed2csv(self):
        outputcsvpapth = self.data['paths']['outcsv']
        outputcsv = outputcsvpapth + '/' + self.name + ".csv"
        print(outputcsv)
        bitrate,psnr,timems = self.parse()
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["SVT-AV1",self.name,self.__raw["resolution"],self.__raw["fps"],self.__raw["framesnumber"],'',bitrate,psnr,timems,self.data["paths"]["svt_options_enc"]])

    def parse_svt_output(pt1,pt2):

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
