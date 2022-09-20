from abc import ABC, abstractmethod
import json


class Codec(ABC):
    def __init__(self, codec, vidpath):
        codec = codec.lower()
        with open('/home/arthurscarpatto/VC/codec-research/code/codecs/JSON_files/paths.JSON') as json_file:
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
            self.__options_encoder = data[codec]['options_encoder']

            self.__vidpath = vidpath
            vidpath_split = vidpath.split('/')[-1]
            self.__name = vidpath_split[:vidpath.index('_')]
            self.__resolution = vidpath_split[vidpath.index('_')+1:vidpath.rindex('_')]
            self.__fps = vidpath_split[vidpath.rindex('_')+1:vidpath.index('.')]
            self.__framesnumber = data[codec]["nframes"]
            #self.__format = data['format']

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

    def get_raw(self):
        return self.__raw_path

    def get_options_encoder(self):
        return self.__options_encoder

    def get_encoder(self):
        return self.__encoder

    def get_decoder(self):
        return self.__decoder

    def get_bitstream(self):
        return self.__bitstream_path

    def get_decoded(self):
        return self.__decoded_path

    def get_txts(self):
        return self.__txts_path

    def get_csvs(self):
        return self.__csvs_path

    def get_images(self):
        return self.__images_path
##### end of section ##################   
##### set qp ##########################
    def set_qp(self,qps):
        self.__qp = str(qps)
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

    @abstractmethod
    def gen_config(self):
        pass

