from dataclasses import dataclass


@dataclass
class EncodingConfig:
    qp: int
    nFrames: int
    fps: float
    preset: str  
    nThreads: int = 1
    codecSetAttrs: str = ""


    def get_unique_attrs(self) -> str:
        """
        There probably is another way of doing this
        leave it to future me to figure out 👍
        """
        return f"q{self.qp}f{self.nFrames}fps{self.fps}p{self.preset}\
t{self.nThreads}a{self.codecSetAttrs.replace(' ', '')}"
    