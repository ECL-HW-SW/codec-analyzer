from abc import ABC, abstractmethod
import json
from pathlib import Path

class Codec(ABC):
    def __init__(self, codec, videocfg = '~/VC/codec-research/code/codecs/JSON_files/video.JSON'):
        self.__codec = codec
        
        p1 = Path('~').expanduser()
        videocfg = videocfg.replace('~', str(p1))

        pathfile = "~/VC/codec-research/code/codecs/JSON_files/paths.JSON"
        p2 = Path('~').expanduser()
        pathfile = pathfile.replace("~", str(p2))      
        with open(pathfile) as json_file:
            data = json.load(json_file)
            self.__raw_path = data['raw']
            self.__qp = data['qp']
            self.__encoder = data[codec]['encoder']
            self.__decoder = data[codec]['decoder']
            self.__bitstream_path = data[codec]['bitstream']
            self.__decoded_path = data[codec]['decoded']
            self.__txts_path = data[codec]['txt']
            self.__csvs_path = data[codec]['csv']
            self.__images_path = data[codec]['images']
            self._options_encoder = data[codec]['options_encoder']
            self._options_decoder = data[codec]['options_decoder']
            self.__decoded_images = data[codec]['decoded_images']
            self.__original_images = data[codec]['original_images']
            self.__preset = self._options_encoder["--preset"]

        with open(videocfg) as json_video_file:
            data = json.load(json_video_file)
            self.__name = data['name']
            self.__vidpath = data['path']
            self.__resolution = data['resolution']
            self.__fps = data['fps']
            self.__framesnumber = data['framesnumber']
            self.__format = data['format']


    def get_codec(self):
        return self.__codec

##### get from video.json##########
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
###### end of section ################

###### get from paths.JSON ###########
    def get_qp(self):
        return self.__qp

    def get_preset(self):
        return self.__preset

    def get_original_images(self) -> str:
        return self.__original_images

    def get_decoded_images(self) -> str:
        return self.__decoded_images

    def get_raw(self):
        return self.__raw_path

    def get_encoder(self):
        return self.__encoder
       
    def get_decoder(self):
        return self.__decoder

    def get_options_encoder(self):
        return self._options_encoder

    def get_options_decoder(self):
        return self._options_decoder

    def get_bitstream(self):
        return self.__bitstream_path +'/'+ self.__name

    def get_decoded(self):
        return self.__decoded_path

    def get_txts(self):
        return self.__txts_path

    def get_csvs(self):
        return self.__csvs_path +'/'+ self.__name

    def get_images(self):
        return self.__images_path
##### end of section ##################   

##### setters ##########################
    def set_qp(self, qp: int):
        self.__qp = str(qp)
##### end of section ##################   

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def decode(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def add_to_csv(self):
        pass