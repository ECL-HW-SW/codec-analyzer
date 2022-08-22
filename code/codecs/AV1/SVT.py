import os
import json
import av1_outparse
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
        svtpath = self.data["paths"]["svt_enc"]
        options_svte = self.data["paths"]["svt_options_enc"]
        encoded_out = self.data["paths"]["svt_encoded"]+"/svtenc_"+self.name
        outgen = self.data["paths"]["svt_outgen"]+"/"+self.name+".log"
        outtime = self.data["paths"]["svt_outtime"]+"/"+self.name+".txt"
        cmdline = svtpath + ' --enable-stat-report 1 --stat-file ' + outgen  + ' ' + options_svte
        cmdline += ' -i ' + self.__raw["path"] + ' -b ' + encoded_out + ' 2> ' + outtime 
        print(cmdline)
        os.system(cmdline)

    def decode(self):
        svtpath = self.data["paths"]["svt_dec"]
        options_svtd = self.data["paths"]["svt_options_dec"]
        encoded_out = self.data["paths"]["svt_encoded"]+"/svtenc_"+self.name
        decoded_out = self.data["paths"]['svt_bitstream']+"/svtdec_"+self.name
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        os.system(cmdline)

    def parse(self):
        outgen = self.data["paths"]["svt_outgen"]+"/"+self.name+".log"
        outtime = self.data["paths"]["svt_outtime"]+"/"+self.name+".txt"
        p = Path('~').expanduser()
        outgen=outgen.replace("~",str(p))
        outtime=outtime.replace("~",str(p))
        bitrate, psnr, timems = av1_outparse.parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems

    def parsed2csv(self):
        outputcsvpapth = self.data['paths']['svt_outcsv']
        outputcsv = outputcsvpapth + '/' + self.name + ".csv"
        print(outputcsv)
        bitrate,psnr,timems = self.parse()
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["SVT-AV1",self.name,self.__raw["resolution"],self.__raw["fps"],self.__raw["framesnumber"],'',bitrate,psnr,timems,self.data["paths"]["svt_options_enc"]])


x = svt_codec('code/codecs/AV1/JSON_files/video.JSON', 'code/codecs/AV1/JSON_files/svt.JSON')
x.encode()
x.decode()
x.parsed2csv()