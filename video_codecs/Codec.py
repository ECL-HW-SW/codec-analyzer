from abc import ABC, abstractmethod
import json
from GlobalPaths import GlobalPaths
import os
import EncodingConfig


class Codec(ABC):

    def __init__(self, codec, codec_config, commit_hash, encoding_config):
        self._codec = codec
        self._commit_hash = commit_hash
        self._encoding_config = encoding_config
        paths = GlobalPaths().get_paths()
        with open(codec_config, "r") as json_file:
            data = json.load(json_file)
            self._encoder_path = os.path.join(paths["codecs_path"], data['encoder_path'])
            self._decoder_path = os.path.join(paths["codecs_path"], data['decoder_path'])
            self._options_encoder = data['options_encoder']
            self._base_attrs = data['base_attrs_encoder']
            self._options_decoder = data['options_decoder']


    def to_dict(self):
        return {
            "name": self.get_codec(),
            "commitHash": self.get_commit_hash(),
            "codecAttrs": self.get_base_attrs(),
        }

    
    def get_results(self) -> dict:
        bitrate, yuvpsnr, timems, ypsnr, upsnr, vpsnr, energy_consumption = self.parse_extra()
        return {
            "ypsnr": ypsnr,
            "upsnr": upsnr,
            "vpsnr": vpsnr,
            "yuvpsnr": yuvpsnr,
            "bitrate": bitrate,
            "time": timems,
            "energyConsumption": energy_consumption
        }

    
    def __append_to_cmdline(self) -> str:
        """
        This is equivalent to a switch case, which is only introduced in Python3.10 -- a pain to install and use
        so i'll just let this stay here as a method that can be specified to each codec. It'll probably go into the 
        parent class soon enough
        """

        # FIXME: this is not scalable and needs to be fixed properly.
        equivalents = {
            "qp": f"--qp {self._encoding_config.qp}",
            "nFrames": f"-f {self._encoding_config.nFrames}",
            "preset": f"--preset {self._encoding_config.preset}",
            "fps": f"--fps {self._encoding_config.fps}",
            "nThreads": f"--threads {self._encoding_config.nThreads}",
            "codecSetAttrs": f"{self._encoding_config.codecSetAttrs}"}
        attrs = [a for a in dir(self._encoding_config) if not a.startswith("__")]
        for a in attrs:
            if a != "uniqueAttrs" and a != "get_unique_attrs" and a != "to_dict":
                cmdline += equivalents[a] + " "
        return cmdline


    def get_unique_attrs(self) -> str:
        return self._encoding_config.get_unique_attrs()
    

    # TODO: look into a "Singleton Dataclass" -- check if this would be better and feasible
    # or if it makes any sense at all really
    def set_encoding_config(self, encoding_config: EncodingConfig) -> None:
        self._encoding_config = encoding_config

    
    def get_encoding_config(self) -> EncodingConfig:
        return self._encoding_config


    # TODO: 
    def get_base_attrs(self) -> str:
        return self._base_attrs


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


    """GETTERS"""
    def get_base_attrs(self) -> str:
        return self._base_attrs


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
