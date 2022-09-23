import os
import json
import csv
from pathlib import Path
from Codec import Codec

class libaom_codec(Codec):

    def __init__(self):
        super().__init__('aom')
        with open('code/codecs/JSON_files/paths.JSON') as json_file:
            data = json.load(json_file)
            self.__decoder = data['aom']['decoder']
            self.__options_encoder = data['aom']['options_encoder']
            self.__options_decoder = data['aom']['options_decoder']
            self.__outtime = data['aom']['outtime']

    def get_decoder(self):
        return self.__decoder

    def get_options_encoder(self):
        return self.__options_encoder
    
    def get_options_decoder(self):
        return self.__options_decoder

    def get_outtime(self):
        return self.__outtime

    def gen_config(self):
        pass

    def encode(self):
        aompath = self.get_encoder()
        options_aome = self.get_options_encoder()
        encoded_out = self.get_bitstream() +"/encaom_"+self.get_videoname() + '_' + self.get_qp()
        outgen = self.get_txts() +"/aom"+self.get_videoname()+".log"
        cmdline = aompath + ' --verbose --psnr --cq-level= ' + self.get_qp() +' '+ options_aome 
        cmdline += ' -o ' + encoded_out + ' ' + self.get_videopath()
        cmdline += " > "+ outgen +" 2>&1"
        print(cmdline)      #@fix
        #os.system(cmdline) #@fix

    def decode(self):
        aompath = self.get_decoder()
        options_libaom = self.get_options_decoder()
        encoded_out = self.get_bitstream() +"/encaom_" + self.get_videoname()
        decoded_out = self.get_decoded() +"/decaom_"+self.get_videoname()
        cmdline = aompath + ' ' + options_libaom + ' ' + encoded_out + ' -o ' + decoded_out
        print(cmdline)      #@fix
        #os.system(cmdline) #@fix

    def parse(self):
        outgen = self.get_txts() +"/aom"+self.get_videoname()
        p = Path('~').expanduser()
        outgen = outgen.replace("~",str(p))
        bitrate, psnr, timems = self.parse_aom_output(outgen)
        return bitrate,psnr,timems

    def add_to_csv(self):
        outputcsv = self.get_csvs() + '/' + self.get_videoname() + ".csv"
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        bitrate,psnr,timems = self.parse()
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["LIBAOM-AV1",self.get_videoname(),self.get_resolution(),self.get_fps(),self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])

    def parse_aom_output(st):
        with open(st, 'r') as output_text:
            out_string = output_text.readlines()
            for line in out_string:
                if (line.startswith("Stream")):
                    bitrateaom_string = line.split()[9]
                    psnr_stringaom = line.split()[5]
                    ms_stringaom = line.split()[11]
        return float(bitrateaom_string), float(psnr_stringaom), float(ms_stringaom)        