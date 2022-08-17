import os

class VTM:
    def __init__(self):
        pass
    
    def encode(self, video_in, cfgdirpath,
                binpath, frames, qsize,
                txtoutpath, other_args):
        os.system(f"~/VC/tools/VTM/bin/EncoderAppStatic {other_args} -c \
            ~/VC/tools/VTM/cfg/encoder_randomaccess_vtm.cfg -b {binpath} \
            -c {cfgdirpath + video_in + '.cfg'} -f {frames} -q {qsize} > {txtoutpath}")

    def decode(self, video_out, binpath, outdir):
        os.system(f"~/VC/tools/VTM/bin/DecoderAppStatic -b {binpath} \
            -o {outdir + video_out + '.yuv'}")
    