from abc import ABC, abstractmethod
import json
from GlobalPaths import GlobalPaths
import os

class Codec(ABC):
    def __init__(self, codec, codec_config):
        self._codec = codec
        paths = GlobalPaths().get_paths()

        # TODO: add hash dos codecs (erro se n tiver)
 
        with open(codec_config, "r") as json_file:
            data = json.load(json_file)
            self._encoder_path = os.path.join(paths["codecs_path"], data['encoder_path'])
            self._decoder_path = os.path.join(paths["codecs_path"], data['decoder_path'])
            self._options_encoder = data['options_encoder']
            self._options_decoder = data['options_decoder']


    def get_codec(self):
        return self._codec
    def get_encoder_path(self):
        return self._encoder_path
    def get_decoder_path(self):
        return self._decoder_path
    
##### setters ##########################
    def set_encoder_option(self, name, val):
        self._options_encoder[name] = val
   
    def set_decoder_option(self, name, val):
        self._options_encoder[name] = val

    @abstractmethod
    def set_qp(self, val):
        pass
    
    @abstractmethod
    def set_num_frames(self, val):
        pass

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