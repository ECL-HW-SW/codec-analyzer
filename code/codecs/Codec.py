from abc import ABC, abstractmethod
import json


class Codec(ABC):
    def __init__(self,codec):
        codec = codec.lower()
        with open('/home/edulodi/video-coding/codec-research/code/codecs/AV1/JSON_files/paths.JSON') as json_file:
            data = json.load(json_file)
            self.__raw_path = data['raw']
            self.__encoder = data[codec]['encoder']
            self.__bitstream_path = data[codec]['bitstream']
            self.__decoded_path = data[codec]['decoded']
            self.__txts_path = data[codec]['txt']
            self.__csvs_path = data[codec]['csv']
            self.__images_path = data[codec]['images']

    def get_raw(self):
        return self.__raw_path

    def get_encoder(self):
        return self.__encoder

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

