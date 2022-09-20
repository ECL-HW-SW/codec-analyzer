from subprocess import run
from skvideo.measure import msssim
import libecl

class MetricsCalculator():
    """ 
    Class for calculating image/video comparison metrics
    such as MSSSIM, VMAF, LPIPS, X-PNSR, and others.
    """

    def __init__(self):
        pass

    def xpsnr(self, videoref: str, videodis: str, output: str) -> float:
        ffmpegpath = ''
        cmdline = ffmpegpath + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -'
        print(cmdline)
        #os.system(cmdline)    

    def vmaf(self, videoref: str , videodis: str, output: str) -> float:
        vmafpath = ''
        cmdline = vmafpath + " -r " + videoref + " -d " + videodis + " -o " + output +  " --csv"
        print(cmdline)
        #os.system(cmdline)

    def lpips(self, videoref: str, videodis: str) -> float:
        cmdline = f"python3.7 ~/VC/tools/PerceptualSimilarity/lpips_2imgs.py \
                        -p0  {videoref} -p1 {videodis}"
        lpips = run([cmdline], shell=True, capture_output=True).stdout\
                    .decode('utf-8').split('\n')[-2].split()[-1]        
        return lpips

    def msssim(self, videoref: str, videodis: str) -> float:
        original_array_luminance = libecl.get_image_array(videoref, "y", "cv2")
        decoded_array_luminance = libecl.get_image_array(videodis, "y", "cv2")

        ssim_ms = msssim(original_array_luminance, decoded_array_luminance, 'product')[0]
        return ssim_ms