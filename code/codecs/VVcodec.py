import os

class VVcodec:
    def __init__(self):
        pass

    def encode(self, video_in, binpath, frames,
                qsize, txtoutpath, other_args):
        os.system(f"~/VC/tools/vvenc/bin/release-static/vvencapp {other_args} -i \
            ~/VC/tools/video-samples/{video_in}.yuv --output={binpath} \
            --frames {frames} --qp {qsize} > {txtoutpath}")

    def decode(self, video_out, binpath, outdir):
        os.system(f"~/VC/tools/vvdec/bin/release-static/vvdecapp -b {binpath} \
            -o {outdir + video_out + '.yuv'}")