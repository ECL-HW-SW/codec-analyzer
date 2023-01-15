from dataclasses import dataclass


@dataclass
class EncodingConfig:
    qp: int
    nFrames: int
    fps: float
    preset: str 
    uniqueConfig: str 
    nThreads: int = 1
    codecSetAttrs: str = ""
    