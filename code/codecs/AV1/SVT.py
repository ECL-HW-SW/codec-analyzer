import os
import json
import av1_outparse
import csv

class svt_codec:

    def __init__(self,rawvideo,configs):
        self.__raw = rawvideo
        self.name = rawvideo.split('_')[0]
        with open(configs,'r') as cfg:
            self.data = json.load(cfg)
        

    def encode(self):
        svtpath = self.data["paths"]["svt_enc"]
        options_svte = self.data["paths"]["svt_options_enc"]
        encoded_out = self.data["paths"]["svt_encoded"]+"/"+self.name
        outgen = self.data["paths"]["svt_outgen"]+"/"+self.name+".log"
        outtime = self.data["paths"]["svt_outtime"]+"/"+self.name+".txt"
        cmdline = svtpath + ' --enable-stat-report 1 --stat-file ' + outgen  + ' ' + options_svte
        cmdline += ' -i ' + self.__raw + ' -b ' + encoded_out + ' 2> ' + outtime 
        print(cmdline)
        #os.system(cmdline)

    def decode(self):
        svtpath = self.data["paths"]["svt_dec"]
        options_svtd = self.data["paths"]["svt_options_dec"]
        encoded_out = self.data["paths"]["svt_encoded"]+"/"+self.name
        decoded_out = self.data["paths"]['svt_bitstream']+"/"+self.name
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        #os.system(cmdline)

    def parse(self):
        outgen = self.data["paths"]["svt_outgen"]
        outtime = self.data["paths"]["svt_outtime"]
        bitrate, psnr, timems = av1_outparse.parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems

    def parsed2csv(self):
        outputcsvpapth = self.data['paths']['svt_outcsv']
        outputcsv = outputcsvpapth + '/' + self.name + ".csv"
        print(outputcsv)
        bitrate,psnr,timems = self.parse()
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['bitrate, psnr, timems'])
            metrics_writer.writerow([bitrate,psnr,timems])


x = svt_codec('path_cif.y4m', 'final_codes/JSON_files/svt.JSON')
x.encode()
x.decode()
x.parsed2csv()