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


    """GETTERS"""
    def get_codec(self) -> str:
        return self._codec

    
    def get_commit_hash(self) -> str:
        return self._commit_hash


    def get_encoder_path(self) -> str:
        return self._encoder_path
    
    
    def get_decoder_path(self) -> str:
        return self._decoder_path
    

    def get_qp(self) -> int:
        return self._options_encoder["qp"] 

    
    def get_preset(self) -> str:
        return self._options_encoder["preset"]
    

    def get_num_frames(self) -> int:
        return self._options_encoder["frames"]


    def get_video(self):
        return self._video
    

    """SETTERS"""
    def set_qp(self, val) -> None:
        self._options_encoder["qp"] = val


    def set_encoder_option(self, name, val) -> None:
        self._options_encoder[name] = val
   
    
    def set_decoder_option(self, name, val) -> None:
        self._options_encoder[name] = val


    def set_commit_hash(self, commit_hash: str) -> None:
        self._commit_hash = commit_hash

    
    def set_num_frames(self, val) -> None:
        self._options_encoder["frames"] = val
    

    def set_preset(self, val) -> None:
        self._options_encoder["preset"] = val

    
    def set_video(self, video) -> None:
        self._video = video


    """ABSTRACT METHODS"""
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
    def parse_extra(self):
        pass


    @abstractmethod
    def get_unique_attrs(self):
        pass


    @abstractmethod
    def add_to_csv(self):
        pass