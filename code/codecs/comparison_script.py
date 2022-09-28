from EVC import EVC
from CodecComparator import CodecComparator
from SVT import svt_codec
from VVcodec import VVcodec
from MetricsCalculator import MetricsCalculator
import cv2
import os
from pathlib import Path
from Video import Video

qps = [22,27,32,37]
metrics = MetricsCalculator()
video = Video()

#svt = svt_codec()
evc = EVC()
#vvenc = VVcodec()
for qp in qps:    
    evc.set_qp(qp)
    evc.encode()
    evc.decode()

    decoded_path = f"{evc.get_decoded()}/vvcodec_{evc.get_videoname()}_{evc.get_qp()}"
    p = Path('~').expanduser()
    decoded_path = decoded_path.replace('~', str(p))

    video.yuv_to_y4m(decoded_path, f"{decoded_path}.y4m", evc.get_resolution(), evc.get_fps())
    msssim_list = []
    
    dec = cv2.VideoCapture(f"{decoded_path}.y4m")
    og = cv2.VideoCapture(evc.get_videopath())

    for i in range(int(evc.get_framesnumber())):
        success_og, image_og = og.read()
        success_dec, image_dec = dec.read()
        #print(success_og, success_dec)

        if success_og and success_dec:
            # initializing paths in which frames are to be saved
            impath = evc.get_images()
            p = Path('~').expanduser()
            impath = impath.replace('~', str(p))

            og_impath = f'{impath}/original-images/vvcodec/frame{i}.png'
            dec_impath = f'{impath}/decoded-images/vvcodec/frame{i}.png'

            # writing the arrays into the paths above
            status_og = cv2.imwrite(og_impath, image_og)
            status_de = cv2.imwrite(dec_impath, image_dec)

            msssim = metrics.msssim(og_impath, dec_impath)
            msssim_list.append(msssim)
                         
    print(f"Average MS-SSIM for qp {qp}: {sum(msssim_list)/len(msssim_list)}")
    evc.add_to_csv()
    