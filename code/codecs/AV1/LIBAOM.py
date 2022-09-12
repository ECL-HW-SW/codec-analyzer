import os
import json
import csv
from pathlib import Path

class libaom_codec:

    def __init__(self,rawvideo,configs):
        with open(rawvideo, 'r') as video: 
            self.__raw = json.load(video)
        with open(configs,'r') as cfg:
            self.data = json.load(cfg)
        self.name = self.__raw["name"]

    def encode(self):
        aompath = self.data['paths']["encoder"]
        options_aome = self.data['paths']["options_encoder"]
        encoded_out = self.data['paths']["encoded"] +"/encaom_"+self.name
        outgen = self.data['paths']["outgen"] +"/aom"+self.name+".log"
        cmdline = aompath + ' --verbose --psnr ' + options_aome 
        cmdline += ' -o ' + encoded_out + ' ' + self.__raw["path"]
        cmdline += " > "+ outgen +" 2>&1"
        print(cmdline)
        os.system(cmdline)

    def decode(self):
        aompath = self.data['paths']['decoder']
        options_libaom = self.data['paths']['options_decoder']
        encoded_out = self.data['paths']['encoded'] +"/encaom_"+self.name
        decoded_out = self.data['paths']['bitstream'] +"/decaom_"+self.name
        cmdline = aompath + ' ' + options_libaom + ' ' + encoded_out + ' -o ' + decoded_out
        print(cmdline)
        os.system(cmdline)

    def parse(self):
        outgen = self.data['paths']['outgen'] +"/aom"+self.name
        p = Path('~').expanduser()
        outgen = outgen.replace("~",str(p))
        bitrate, psnr, timems = self.parse_aom_output(outgen)
        return bitrate,psnr,timems

    def parsed2csv(self):
        outputcsvpapth = self.data['paths']['outcsv']
        outputcsv = outputcsvpapth + '/' + self.name + ".csv"
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        bitrate,psnr,timems = self.parse()
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["LIBAOM-AV1",self.name,self.__raw["resolution"],self.__raw["fps"],self.__raw["framesnumber"],'',bitrate,psnr,timems,self.data["paths"]["options_encoder"]])

    def parse_aom_output(st):
        with open(st, 'r') as output_text:
            out_string = output_text.readlines()
            for line in out_string:
                if (line.startswith("Stream")):
                    bitrateaom_string = line.split()[9]
                    psnr_stringaom = line.split()[5]
                    ms_stringaom = line.split()[11]
        return float(bitrateaom_string), float(psnr_stringaom), float(ms_stringaom)        
