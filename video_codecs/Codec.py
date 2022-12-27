from abc import ABC, abstractmethod
import json
from GlobalPaths import GlobalPaths
import os



class Codec(ABC):

    def __init__(self, codec, codec_config, commit_hash):
        self._codec = codec
        self._commit_hash = commit_hash
        paths = GlobalPaths().get_paths()
        with open(codec_config, "r") as json_file:
            data = json.load(json_file)
            self._encoder_path = os.path.join(paths["codecs_path"], data['encoder_path'])
            self._decoder_path = os.path.join(paths["codecs_path"], data['decoder_path'])
            self._options_encoder = data['options_encoder']
            self._options_decoder = data['options_decoder']

    # TODO: add hash dos codecs (erro se n tiver)

    """GETTERS"""
    def get_codec(self) -> str:
        return self._codec

    
    def get_commit_hash(self) -> str:
        return self._commit_hash


    def get_encoder_path(self) -> str:
        return self._encoder_path
    
    
    def get_decoder_path(self) -> str:
        return self._decoder_path
    

    """SETTERS"""
    def set_encoder_option(self, name, val) -> None:
        self._options_encoder[name] = val
   
    
    def set_decoder_option(self, name, val) -> None:
        self._options_encoder[name] = val


    def set_commit_hash(self, commit_hash: str) -> None:
        self._commit_hash = commit_hash

    """ABSTRACT METHODS"""
    @abstractmethod
    def set_qp(self, val):
        pass
    
    
    @abstractmethod
    def set_num_frames(self, val):
        pass


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