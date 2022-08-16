import os
import json
import av1_outparse
import csv

class libaom_codec:

    def __init__(self,rawvideo,configs):
        self.__raw = rawvideo
        self.name = rawvideo.split('_')[0]
        with open(configs,'r') as cfg:
            self.data = json.load(cfg)
    
    def encode(self):
        aompath = self.data['paths']["libaom_enc"]
        options_aome = self.data['paths']["libaom_options_enc"]
        encoded_out = self.data['paths']["libaom_encoded"] +"/"+self.name
        outgen = self.data['paths']["libaom_outgen"] +"/"+self.name
        cmdline = aompath + ' --verbose --psnr ' + options_aome 
        cmdline += ' -o ' + encoded_out + ' ' + self.__raw
        cmdline += " > "+ outgen +" 2>&1"
        print(cmdline)
        #os.system(cmdline)

    def decode(self):
        aompath = self.data['paths']['libaom_dec']
        options_libaom = self.data['paths']['libaom_options_dec']
        encoded_out = self.data['paths']['libaom_encoded'] +"/"+self.name
        decoded_out = self.data['paths']['libaom_bitstream'] +"/"+self.name
        cmdline = aompath + ' ' + options_libaom + ' ' + encoded_out + ' -o ' + decoded_out
        print(cmdline)
        #os.system(cmdline)

    def parse(self):
        outgen = self.data['paths']['libaom_outgen']
        bitrate, psnr, timems = av1_outparse.parse_aom_output(outgen)
        return bitrate,psnr,timems

    def csv_parsed_data(self):
        outputcsvpapth = self.data['paths']['libaom_outcsv']
        outputcsv = outputcsvpapth + '/' + self.name + ".csv"
        print(outputcsv)
        bitrate,psnr,timems = self.parse()
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['bitrate, psnr, timems'])
            metrics_writer.writerow([bitrate,psnr,timems])