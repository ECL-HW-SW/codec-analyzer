import os
import json
import csv
from pathlib import Path
import Codec

class svt_codec(Codec):

    def __init__(self):
        super().__init__()
        with open('/home/edulodi/videocoding/codec-research/code/codecs/AV1/JSON_files/paths.JSON') as json_file:
            data = json.load(json_file)
            self.__decoder = data['svt']['decoder']
            self.__options_encoder = data['svt']['options_encoder']
            self.__options_decoder = data['svt']['options_decoder']
            self.__outtime = data['svt']['outtime']

        with open('/home/edulodi/videocoding/codec-research/code/codecs/AV1/JSON_files/video.JSON') as json_video_file:
            data = json.load(json_video_file)
            self.__name = data['name']
            self.__vidpath = data['path']
            self.__resolution = data['resolution']
            self.__fps = data['fps']
            self.__framesnumber = data['framesnumber']
            self.__format = data['format']

    def get_videopath(self):
        return self.__vidpath
    
    def  get_resolution(self):
        return self.__resolution
    
    def get_fps(self):
        return self.__fps

    def get_framesnumber(self):
        return self.__framesnumber

    def get_format(self):
        return self.__format

    def get_videoname(self):
        return self.__name

    def get_decoder(self):
        return self.__decoder

    def get_options_encoder(self):
        return self.__options_encoder
    
    def get_options_decoder(self):
        return self.__options_decoder

    def get_outtime(self):
        return self.__outtime

    def encode(self):
        svtpath = self.get_encoder
        options_svte = self.get_options_encoder
        encoded_out = self.get_bitstream+"/svtenc_"+self.get_videoname
        outgen = self.get_txts+"/"+self.get_videoname+".log"
        outtime = self.get_outtime+"/"+self.get_videoname+".txt"
        cmdline = svtpath + ' --enable-stat-report 1 --stat-file ' + outgen  + ' ' + options_svte
        cmdline += ' -i ' + self.get_videopath + ' -b ' + encoded_out + ' 2> ' + outtime 
        print(cmdline)
        #os.system(cmdline)

    def decode(self):
        svtpath = self.get_decoder
        options_svtd = self.get_options_decoder
        encoded_out = self.get_bitstream+"/svtenc_"+self.get_videoname
        decoded_out = self.get_decoded+"/svtdec_"+self.get_videoname
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        #os.system(cmdline)

    def parse(self):
        outgen = self.get_txts+"/"+self.get_videoname+".log"
        outtime = self.get_outtime+"/"+self.get_videoname+".txt"
        p = Path('~').expanduser()
        outgen=outgen.replace("~",str(p))
        outtime=outtime.replace("~",str(p))
        bitrate, psnr, timems = self.parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems

    def parsed2csv(self):
        outputcsvpapth = self.get_csvs
        outputcsv = outputcsvpapth + '/' + self.get_videoname + ".csv"
        print(outputcsv)
        bitrate,psnr,timems = self.parse()
        p = Path('~').expanduser()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["SVT-AV1",self.get_videoname,self.get_resolution,self.get_fps,self.get_framesnumber,'',bitrate,psnr,timems,self.get_options_encoder])

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

test = svt_codec()
test.encode()